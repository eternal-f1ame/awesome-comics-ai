"""List the papers from an arXiv sweep that are not in the list yet, as Markdown for an issue.

Keeps a sweep record when its title names comics (also inside names such as MangaNinja) or its abstract names them at least twice,
and drops it when its arXiv id or its title is already in data/papers.yaml.

Usage: python scripts/new_candidates.py SWEEP.json > issue.md
"""
import json, pathlib, re, sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
COMIC = re.compile(r"\b(comic|comics|manga|webtoons?|manhwa|manhua|bande dessin\w*|graphic novels?|speech balloons?|screentones?|manga109|4-?koma|yonkoma)\b", re.I)
INSIDE = re.compile(r"(comic|manga|webtoon|screentone)", re.I)
norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())


def main():
    sweep = json.load(open(sys.argv[1], encoding="utf-8"))
    papers = yaml.safe_load((ROOT / "data" / "papers.yaml").read_text(encoding="utf-8")) or []
    have_ids = {str(p.get("arxiv")) for p in papers if p.get("arxiv")}
    have_titles = {norm(p["title"]) for p in papers}
    new = [r for r in sweep if r["arxiv"] not in have_ids and norm(r["title"]) not in have_titles
           and (INSIDE.search(r["title"]) or len(COMIC.findall(r.get("summary", ""))) >= 2)]
    print(f"The monthly arXiv sweep found {len(new)} paper(s) that may belong in the list. Add the ones that do to `data/papers.yaml`.\n")
    for r in new:
        print(f"- [ ] [{r['title']}](https://arxiv.org/abs/{r['arxiv']}) ({r['published']}, {r['primary']})")


if __name__ == "__main__":
    main()
