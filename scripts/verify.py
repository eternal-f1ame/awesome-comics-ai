"""Check data/papers.yaml.

Offline (default): every entry has a title, year, venue, section and at least one link; the section exists; no two entries share a
title; arXiv ids are well formed; links are https; and the entry meets the inclusion rule in scripts/policy.py. A preprint past its
window is only a warning here (the monthly refresh retires it); any other failure of the rule is an error. Online (--online): each
arXiv id resolves on the arXiv API to the listed title.

Usage: python scripts/verify.py [--online]
"""
import argparse, pathlib, re, sys, time, urllib.error, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import policy

ROOT = pathlib.Path(__file__).resolve().parent.parent
REQUIRED = ("title", "year", "venue", "category")
norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
warnings = []


def offline(papers, sections):
    errors, seen = [], {}
    table = policy.venues()
    ids = {s["id"] for s in sections}
    for i, p in enumerate(papers):
        where = f"entry {i} ({p.get('title', '?')[:60]})"
        for k in REQUIRED:
            if not p.get(k):
                errors.append(f"{where}: missing {k}")
        if p.get("category") not in ids:
            errors.append(f"{where}: unknown section {p.get('category')!r}")
        if not any(p.get(k) for k in ("paper", "arxiv")):
            errors.append(f"{where}: needs a paper link or an arXiv id")
        if p.get("arxiv") and not re.fullmatch(r"\d{4}\.\d{4,5}", str(p["arxiv"])):
            errors.append(f"{where}: malformed arXiv id {p['arxiv']!r}")
        for k in ("paper", "code", "project"):
            if p.get(k) and not str(p[k]).startswith("https://"):
                errors.append(f"{where}: {k} link is not https")
        if isinstance(p.get("year"), int) and not 1990 <= p["year"] <= 2100:
            errors.append(f"{where}: implausible year {p['year']}")
        key = norm(p.get("title", ""))
        if key in seen:
            errors.append(f"{where}: duplicate of entry {seen[key]}")
        seen[key] = i
        why = policy.reason_out(p, table)
        if why and why.startswith("arXiv preprint from"):
            warnings.append(f"{where}: {why} (scripts/refresh.py retires it)")
        elif why:
            errors.append(f"{where}: does not meet the inclusion rule: {why}")
    return errors


def online(papers):
    errors = []
    ax = [p for p in papers if p.get("arxiv")]
    for k in range(0, len(ax), 50):
        chunk = ax[k:k + 50]
        url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"id_list": ",".join(str(p["arxiv"]) for p in chunk), "max_results": 50})
        for attempt in range(5):        # the API answers 429 when asked too fast; wait and try again
            try:
                feed = ET.fromstring(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "awesome-comics-ai-verify"}), timeout=60).read())
                break
            except urllib.error.HTTPError as e:
                if e.code != 429 or attempt == 4:
                    raise
                time.sleep(20 * (attempt + 1))
        ns = {"a": "http://www.w3.org/2005/Atom"}
        got = {}
        for e in feed.findall("a:entry", ns):
            aid = e.findtext("a:id", "", ns).rsplit("/abs/", 1)[-1].split("v")[0]
            got[aid] = " ".join(e.findtext("a:title", "", ns).split())
        for p in chunk:
            t = got.get(str(p["arxiv"]))
            if t is None:
                errors.append(f"arXiv {p['arxiv']} not found ({p['title'][:60]})")
            elif norm(t) != norm(p["title"]):
                errors.append(f"arXiv {p['arxiv']} title differs: listed {p['title'][:60]!r}, arXiv {t[:60]!r}")
        time.sleep(3)
    return errors


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--online", action="store_true")
    a = ap.parse_args()
    papers = yaml.safe_load((ROOT / "data" / "papers.yaml").read_text(encoding="utf-8")) or []
    sections = yaml.safe_load((ROOT / "data" / "sections.yaml").read_text(encoding="utf-8"))
    errors = offline(papers, sections) + (online(papers) if a.online else [])
    for w in warnings:
        print("warning:", w)
    for e in errors:
        print(e)
    print(f"{len(papers)} entries, {len(errors)} problems, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
