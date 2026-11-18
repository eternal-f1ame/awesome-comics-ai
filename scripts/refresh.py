"""Apply the preprint rule: promote published preprints, retire expired ones, and bring back retired ones that were published.

For every arXiv preprint in data/papers.yaml older than the preprint window, and every retired preprint in data/not_included.yaml,
search Crossref for the title. An exact title match at a venue that meets the rule (scripts/policy.py) moves the paper into, or keeps
it in, the list with its published venue, year and DOI. A preprint past the window with no such match moves to not_included.yaml.
Run monthly (the GitHub Action does), then run build.py. Prints what changed.

Usage: python scripts/refresh.py [--dry-run]
"""
import argparse, datetime as dt, json, re, sys, time, urllib.parse, urllib.request

import yaml

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import policy
from venue_names import short

ROOT = policy.ROOT
norm = lambda t: re.sub(r"[^a-z0-9]", "", (t or "").lower())
UA = {"User-Agent": "awesome-comics-ai-refresh"}


def published(title):
    """The first Crossref record with exactly this title that is not a preprint: (short venue, year, DOI) or None."""
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode({"query.title": title, "rows": 5,
                                                                      "select": "DOI,title,container-title,issued,type,event"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                items = json.load(r)["message"]["items"]
            break
        except Exception:
            time.sleep(5 * (attempt + 1))
    else:
        raise RuntimeError("Crossref request failed for " + title)
    for x in items:
        if not x.get("title") or norm(x["title"][0]) != norm(title) or x.get("type") in ("posted-content", "peer-review"):
            continue
        conts = x.get("container-title") or []
        raw = (x.get("event") or {}).get("name") or (conts[1] if len(conts) > 1 and conts[0] == "Lecture Notes in Computer Science" else (conts or [None])[0])
        name = short(raw) if raw else None
        year = ((x.get("issued") or {}).get("date-parts") or [[None]])[0][0]
        m = re.search(r"\b(19[89]\d|20[0-3]\d)\b", raw or "")
        return name, int(m.group(1)) if m else year, x["DOI"], raw
    return None


def citations(arxiv_id):
    """The larger citation count that Semantic Scholar and OpenAlex give for an arXiv paper, or None if neither answers."""
    counts = []
    for url, key in ((f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}?fields=citationCount", "citationCount"),
                     (f"https://api.openalex.org/works/doi:10.48550/arXiv.{arxiv_id}?select=cited_by_count", "cited_by_count")):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                counts.append(int(json.load(r)[key]))
        except Exception:
            pass
        time.sleep(2)
    return max(counts) if counts else None


def load(name):
    return yaml.safe_load((ROOT / "data" / name).read_text(encoding="utf-8")) or []


def dump(name, rows, head):
    rows.sort(key=lambda e: (e["category"], -e["year"], e["title"].lower()))
    text = yaml.safe_dump(rows, allow_unicode=True, sort_keys=False, width=200)
    (ROOT / "data" / name).write_text(head + text, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    table, today = policy.venues(), dt.date.today()
    cutoff = policy.preprint_cutoff(today)
    papers, out = load("papers.yaml"), load("not_included.yaml")
    head = lambda name: "".join(l for l in (ROOT / "data" / name).read_text(encoding="utf-8").splitlines(True) if l.startswith("#"))
    head_p, head_o = head("papers.yaml"), head("not_included.yaml")
    log = []

    def try_publish(e):
        hit = published(e["title"]); time.sleep(1)
        if not hit:
            return False
        name, year, doi, raw = hit
        if name is None or name not in table:
            log.append(f"CHECK venue name: {e['title'][:70]} was published in {raw!r}; add it to venue_names.py and venues.yaml")
            return False
        cand = dict(e, venue=name, year=year, paper="https://doi.org/" + doi); cand.pop("date", None); cand.pop("reason", None)
        if policy.reason_out(cand, table, today) is None:
            e.clear(); e.update(cand)
            return True
        return False

    # surveys: refresh the citation count of every survey preprint, in the list or out of it
    for e in papers + out:
        if e.get("category") == "surveys" and e.get("venue") == "arXiv" and e.get("arxiv"):
            c = citations(e["arxiv"])
            if c is not None and c != e.get("citations"):
                log.append(f"CITATIONS: {e['title'][:70]}: {e.get('citations')} -> {c}")
                e["citations"], e["citations_source"] = c, f"Semantic Scholar or OpenAlex, {today}"
    for e in list(out):
        if e.get("category") == "surveys" and policy.reason_out(e, table, today) is None:
            out.remove(e); e.pop("reason", None); papers.append(e)
            log.append(f"SURVEY back in the list: {e['title'][:70]} ({e.get('citations')} citations)")

    keep, retired_now = [], set()
    for e in papers:
        if e.get("category") == "surveys":
            why = policy.reason_out(e, table, today)
            if why:
                e["reason"] = why; out.append(e); retired_now.add(e["title"]); log.append(f"SURVEY out: {e['title'][:70]} ({why})")
            else:
                keep.append(e)
            continue
        if e.get("venue") == "arXiv" and e.get("date") and dt.date.fromisoformat(str(e["date"])) < cutoff:
            if try_publish(e):
                log.append(f"PUBLISHED, kept: {e['title'][:70]} -> {e['venue']} {e['year']}")
                keep.append(e)
            else:
                e["reason"] = policy.reason_out(e, table, today)
                out.append(e); retired_now.add(e["title"])
                log.append(f"RETIRED: {e['title'][:70]} ({e['date']})")
        else:
            keep.append(e)
    rest = []
    for e in out:
        if e.get("venue") == "arXiv" and e["title"] not in retired_now and e.get("reason", "").startswith("arXiv preprint") and try_publish(e):
            keep.append(e); log.append(f"PUBLISHED, back in the list: {e['title'][:70]} -> {e['venue']} {e['year']}")
        else:
            rest.append(e)
    for line in log:
        print(line)
    print(f"{len(keep)} in the list, {len(rest)} not included" + (" (dry run, nothing written)" if a.dry_run else ""))
    if not a.dry_run:
        dump("papers.yaml", keep, head_p)
        dump("not_included.yaml", rest, head_o)


if __name__ == "__main__":
    main()
