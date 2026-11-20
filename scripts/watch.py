"""Add new papers to the list: search arXiv since the last finished run, keep what is in scope, file each in its section.

Runs every two weeks in the GitHub Action, after refresh.py. The search window starts WINDOW_OVERLAP before the last run that
finished (data/watch.yaml), because arXiv lists a paper only once it is announced, at times days after its submission date; papers
already in data/papers.yaml, data/not_included.yaml or data/excluded.yaml are skipped. If arXiv fails, the run fails and records
nothing, so the next run covers the window again. (The window rule follows the weekly scanner of Papers With No Code.)

A new paper enters as an arXiv preprint in the section scripts/scope.py gives it, with its code repository when the comment or the
abstract names one. If Crossref already lists it at a known venue, it enters with that venue instead, in the list or in
not_included.yaml as the inclusion rule decides. Titles that match a pattern in the WATCH_HOLD environment variable (one regular
expression per line, kept in a repository secret) are left out and never printed. Each run also dates the list (meta.updated in
data/resources.yaml), which the site shows.

Usage: python scripts/watch.py [--dry-run] [--since YYYY-MM-DD]
"""
import argparse, datetime as dt, os, re, sys, time

import yaml

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import arxiv_sweep
import policy
import refresh
import scope

ROOT = policy.ROOT
WINDOW_OVERLAP = dt.timedelta(days=10)
FIRST_LOOKBACK = dt.timedelta(days=45)
MAX_LOOKBACK = dt.timedelta(days=60)
EMPTY_PAGE_RETRIES = 2
STATE = ROOT / "data" / "watch.yaml"
norm = refresh.norm
REPO = re.compile(r"(?:https?://)?(?:www\.)?github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)", re.I)


def window_start(today, last_complete):
    if last_complete is None:
        return today - FIRST_LOOKBACK
    return max(last_complete - WINDOW_OVERLAP, today - MAX_LOOKBACK)


def short_authors(names):
    return "" if not names else names[0] + (" et al." if len(names) > 1 else "")


def code_link(comment, abstract):
    for text in (comment, abstract):
        m = REPO.search(text or "")
        if m:
            owner, repo = m.group(1), re.sub(r"\.git$", "", m.group(2).rstrip("."))
            return f"https://github.com/{owner}/{repo}"
    return None


def held(title, patterns):
    return any(re.search(p, title, re.I) for p in patterns)


def entry_from(rec):
    section, dataset = scope.section_for(rec["title"], rec.get("summary", ""))
    e = {"title": rec["title"], "authors": short_authors(rec["authors"]), "year": int(rec["published"][:4]), "venue": "arXiv",
         "category": section, "arxiv": rec["arxiv"], "date": rec["published"]}
    code = code_link(rec.get("comment"), rec.get("summary"))
    if code:
        e["code"] = code
    if dataset:
        e["dataset"] = True
    return e


def published_version(e, table, lookup=refresh.published):
    """The entry with its published venue when Crossref lists it at a venue in data/venues.yaml, else the entry unchanged."""
    hit = lookup(e["title"])
    if not hit or hit[0] not in table:
        return e
    name, year, doi, _ = hit
    out = dict(e, venue=name, year=year or e["year"], paper="https://doi.org/" + doi)
    out.pop("date", None)
    return out


def stamp(today):
    """Set meta.updated in data/resources.yaml to today, keeping the file's comments."""
    path = ROOT / "data" / "resources.yaml"
    text, n = re.subn(r'^(\s*updated:\s*)"[^"]*"(.*)$', lambda m: f'{m.group(1)}"{today}"{m.group(2)}', path.read_text(encoding="utf-8"), count=1, flags=re.M)
    if n != 1:
        raise SystemExit("no meta.updated line in data/resources.yaml")
    path.write_text(text, encoding="utf-8")


def sweep(since):
    """Every arXiv record since `since` whose title or abstract carries one of the sweep's keywords, newest first."""
    found = {}
    for field in ("ti", "abs"):
        for kw in arxiv_sweep.KEYWORDS:
            start = 0
            while True:
                batch = list(arxiv_sweep.records(arxiv_sweep.fetch(arxiv_sweep.query(kw, field), start)))
                for _ in range(EMPTY_PAGE_RETRIES if start == 0 and not batch else 0):   # arXiv at times answers with an empty page
                    time.sleep(5)
                    batch = list(arxiv_sweep.records(arxiv_sweep.fetch(arxiv_sweep.query(kw, field), start)))
                    if batch:
                        break
                new = [r for r in batch if r["published"] >= since]
                for r in new:
                    found.setdefault(r["arxiv"], r)
                if len(batch) < 200 or len(new) < len(batch):
                    break
                start += 200
                time.sleep(3)
            time.sleep(3)
    return sorted(found.values(), key=lambda r: r["published"], reverse=True)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--since", default="")
    a = ap.parse_args()
    today, table = dt.date.today(), policy.venues()
    state = (yaml.safe_load(STATE.read_text(encoding="utf-8")) if STATE.exists() else None) or {}
    last = state.get("last_complete")
    since = a.since or str(window_start(today, dt.date.fromisoformat(str(last)) if last else None))
    holds = [l.strip() for l in os.environ.get("WATCH_HOLD", "").splitlines() if l.strip()]

    papers, out = refresh.load("papers.yaml"), refresh.load("not_included.yaml")
    excluded = refresh.load("excluded.yaml") if (ROOT / "data" / "excluded.yaml").exists() else []
    known_ids = {str(p.get("arxiv")) for p in papers + out + excluded if p.get("arxiv")}
    known_titles = {norm(p["title"]) for p in papers + out + excluded if p.get("title")}

    records = sweep(since)
    added, parked, skipped, n_held = [], [], [], 0
    for r in records:
        if r["arxiv"] in known_ids or norm(r["title"]) in known_titles:
            continue
        if held(r["title"], holds):
            n_held += 1
            continue
        if not scope.in_scope(r["title"], r.get("summary", "")):
            skipped.append(r)
            continue
        e = published_version(entry_from(r), table)
        time.sleep(1)
        why = policy.reason_out(e, table, today)
        if why:
            e["reason"] = why; out.append(e); parked.append(e)
        else:
            papers.append(e); added.append(e)
        known_ids.add(r["arxiv"]); known_titles.add(norm(r["title"]))

    print(f"## Watch: arXiv since {since}\n")
    print(f"{len(records)} records with a comics keyword, {len(added)} added, {len(parked)} kept out by the inclusion rule, "
          f"{len(skipped)} out of scope" + (f", {n_held} held" if n_held else "") + ".\n")
    for e in added:
        print(f"- added to **{e['category']}**: [{e['title']}](https://arxiv.org/abs/{e['arxiv']}) ({e['venue']})")
    for e in parked:
        print(f"- not included: {e['title']} ({e['reason']})")
    if skipped:   # so a reader can check what the scope rule left out, and add a paper it missed by hand
        print("\n<details><summary>Out of scope</summary>\n")
        for r in skipped:
            print(f"- [{r['title']}](https://arxiv.org/abs/{r['arxiv']}): comics named {scope.comic_mentions(r.get('summary', ''))} times in the abstract")
        print("\n</details>")
    if a.dry_run:
        print("\n(dry run, nothing written)")
        return
    head = lambda name: "".join(l for l in (ROOT / "data" / name).read_text(encoding="utf-8").splitlines(True) if l.startswith("#"))
    refresh.dump("papers.yaml", papers, head("papers.yaml"))
    refresh.dump("not_included.yaml", out, head("not_included.yaml"))
    stamp(today)
    STATE.write_text("# Written by scripts/watch.py: the day of the last run whose arXiv search finished. The next run searches from\n"
                     f"# {WINDOW_OVERLAP.days} days before it, because arXiv announces some papers days after their submission date.\n"
                     f"last_complete: '{today}'\n", encoding="utf-8")


if __name__ == "__main__":
    main()
