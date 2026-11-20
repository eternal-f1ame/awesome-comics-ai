"""Build README.md and the site from data/*.yaml.

data/papers.yaml is the single source of the list; data/sections.yaml gives the sections in order; data/resources.yaml holds the
tools, workshops and related lists; data/posts.yaml lists the blog posts (each post is its own page in docs/). This script writes README.md and docs/papers.json (which the site pages in docs/ read). Run it after
every change to the data, and commit its output with the change. `--check` exits non-zero when the committed output is stale.

Usage: python scripts/build.py [--check]
"""
import argparse, json, pathlib, sys
from collections import Counter

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import policy as POLICY

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load():
    papers = yaml.safe_load((DATA / "papers.yaml").read_text(encoding="utf-8")) or []
    sections = yaml.safe_load((DATA / "sections.yaml").read_text(encoding="utf-8"))
    resources = yaml.safe_load((DATA / "resources.yaml").read_text(encoding="utf-8"))
    posts = yaml.safe_load((DATA / "posts.yaml").read_text(encoding="utf-8")) if (DATA / "posts.yaml").exists() else []
    return papers, sections, resources, posts or []


def anchor(title):
    return "".join(c for c in title.lower().replace(" ", "-") if c.isalnum() or c == "-")


def links(p):
    out = []
    if p.get("paper"):
        out.append(f"[paper]({p['paper']})")
    if p.get("arxiv") and f"arxiv.org/abs/{p['arxiv']}" not in (p.get("paper") or ""):
        out.append(f"[arXiv](https://arxiv.org/abs/{p['arxiv']})")
    if p.get("code"):
        out.append(f"[code]({p['code']})")
    if p.get("project"):
        out.append(f"[project]({p['project']})")
    return " · ".join(out)


def cell(text):
    return str(text).replace("|", "\\|")


def readme(papers, sections, resources):
    by = {s["id"]: [] for s in sections}
    for p in papers:
        by[p["category"]].append(p)
    years = Counter(p["year"] for p in papers)
    recent = sum(n for y, n in years.items() if y >= max(years) - 1)
    L = [
        "# Awesome Comics & Manga AI [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)",
        "",
        "A curated, maintained map of research on comics in computer vision, language and graphics: manga, manhwa, manhua, "
        "webtoons, bandes dessinées, comic strips, graphic novels and single-panel cartoons. It covers how models read, "
        "search, translate, describe, create and reason about them, and the datasets, benchmarks and tools behind that work. "
        "It lists work from top venues and their workshops, the datasets the field builds on, and the newest preprints "
        "([inclusion rule](#inclusion-rule)).",
        "",
        f"**{len(papers)} papers** in {len(sections)} sections, {recent} of them from {max(years) - 1}–{max(years)}. "
        "Every entry is checked against arXiv, Crossref or the venue's own pages, and the list updates itself every two weeks "
        "([how the list stays current](#how-the-list-stays-current))." + (f" Browse and search it on the [site]({resources['meta']['site_url']})." if resources["meta"].get("site_url") else ""),
        "",
        "## Contents",
        "",
    ]
    sections = [s for s in sections if by[s["id"]]]          # a section with no paper under the rule is left out
    for s in sections:
        L.append(f"- [{s['title']}](#{anchor(s['title'])}) ({len(by[s['id']])})")
    for extra in ("Tools and models", "Workshops and competitions", "Related lists", "Inclusion rule", "How the list stays current", "Contributing"):
        L.append(f"- [{extra}](#{anchor(extra)})")
    L.append("")
    for s in sections:
        L += [f"## {s['title']}", "", s["blurb"], "", "| Year | Venue | Title | Links |", "|:---:|:---|:---|:---|"]
        for p in sorted(by[s["id"]], key=lambda p: (-p["year"], p["title"].lower())):
            L.append(f"| {p['year']} | {cell(p['venue'])} | {cell(p['title'])} | {links(p)} |")
        L.append("")
    L += ["## Tools and models", "", "| Tool | What it does | Links |", "|:---|:---|:---|"]
    for t in resources["tools"]:
        L.append(f"| {cell(t['name'])} | {cell(t['what'])} | [code]({t['url']}) |")
    L += ["", "## Workshops and competitions", ""]
    for w in resources["workshops"]:
        L.append(f"- **{w['name']}**: {w['what']} [{w['link_text']}]({w['url']})")
    L += ["", "## Related lists", ""]
    for r in resources["related"]:
        L.append(f"- [{r['name']}]({r['url']}): {r['what']}")
    L += ["", "## Inclusion rule", "",
          "A paper is in the list when it meets one of these conditions:", "",
          "1. It appeared at a conference or in a journal ranked **A\\* or A by CORE** (CORE2023 for conferences, CORE2020 for "
          "journals). `data/venues.yaml` gives every venue's rank.",
          "2. It appeared at a **workshop** of any conference, or in a peer-reviewed track of an A\\* or A conference (Findings, "
          "technical briefs, extended abstracts).",
          "3. It is a **dataset or benchmark paper**, at any published venue.",
          f"4. It is an **arXiv preprint** whose first version is at most {POLICY.PREPRINT_MONTHS} months old. After that, it stays "
          "only if a venue that meets conditions 1–3 has published it.", "",
          f"Surveys follow their own rule: a survey of comics is listed when it is peer-reviewed at any venue, or when it is a "
          f"preprint with at least {POLICY.SURVEY_MIN_CITATIONS} citations. The four-month window does not apply to surveys.", "",
          "Verified papers that do not meet the rule are kept, with the reason, in `data/not_included.yaml`, so a later "
          "publication brings them back.", "",
          "## How the list stays current", "",
          "- `data/papers.yaml` is the single source. `scripts/build.py` writes this README and the site from it, so the two never drift.",
          "- `scripts/verify.py` checks every entry: required fields, a known section, no duplicate titles, and, with `--online`, that each "
          "arXiv id resolves to the listed title.",
          "- Every two weeks (the 1st and the 15th of each month) a GitHub Action updates the list with no one at the keyboard, and "
          "commits the change to `main`; the site follows.",
          "- In that Action, `scripts/refresh.py` promotes preprints that have been published, retires those past "
          f"the {POLICY.PREPRINT_MONTHS}-month window, brings back retired ones published since and refreshes the citation counts of survey preprints.",
          "- Then `scripts/watch.py` searches arXiv from shortly before the last run and adds each new paper whose title names comics, "
          "manga or webtoons (or whose abstract names them at least three times), in the section that `scripts/scope.py` gives it, with its "
          "code repository when the paper names one. The run's summary lists what it added and what it left out.",
          "- A paper filed in the wrong section is fixed by editing its entry. A paper that does not belong is moved to `data/excluded.yaml`, "
          "and the watcher never adds it again. `python scripts/watch.py --dry-run` shows what the next run would add.",
          "", "## Contributing", "",
          "Additions and corrections are welcome. Add or edit an entry in `data/papers.yaml`, run `python scripts/build.py`, and open a "
          "pull request; [CONTRIBUTING.md](CONTRIBUTING.md) gives the fields and the scope. A paper belongs here when comics are its "
          "subject or its main test bed.", "",
          "## License", "", "[CC0 1.0](LICENSE): to the extent possible under law, the maintainers waive all copyright to this list.", ""]
    return "\n".join(L)


def site_json(papers, sections, resources, posts):
    sections = [s for s in sections if any(p["category"] == s["id"] for p in papers)]
    return json.dumps({"sections": sections, "papers": sorted(papers, key=lambda p: (-p["year"], p["title"].lower())),
                       "resources": resources, "posts": posts}, ensure_ascii=False, indent=1) + "\n"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    papers, sections, resources, posts = load()
    missing = [q["file"] for q in posts if not (ROOT / "docs" / q["file"]).exists()]
    if missing:
        sys.exit(f"a post in data/posts.yaml has no page in docs/: {missing}")
    ids = {s["id"] for s in sections}
    bad = [p["title"] for p in papers if p.get("category") not in ids]
    if bad:
        sys.exit(f"unknown section for: {bad[:5]}")
    outputs = {ROOT / "README.md": readme(papers, sections, resources), ROOT / "docs" / "papers.json": site_json(papers, sections, resources, posts)}
    stale = [p for p, text in outputs.items() if not p.exists() or p.read_text(encoding="utf-8") != text]
    if a.check:
        if stale:
            sys.exit("stale: " + ", ".join(str(p.relative_to(ROOT)) for p in stale) + " (run python scripts/build.py)")
        print("up to date"); return
    for p, text in outputs.items():
        p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding="utf-8")
    print(f"wrote README.md and docs/papers.json: {len(papers)} papers")


if __name__ == "__main__":
    main()
