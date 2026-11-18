"""Find arXiv papers about comics, manga, webtoons and related forms.

Queries the arXiv API for papers whose title contains one of the keywords, in the computing categories, and writes one JSON record
per paper (id, title, authors, dates, categories, comment, journal reference). The list is curated by hand from these records; the
sweep only finds candidates. Run it monthly (the GitHub Action does) and review what is new against data/papers.yaml.

Usage: python scripts/arxiv_sweep.py OUT.json [--since YYYY-MM-DD]
"""
import argparse, json, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

KEYWORDS = ["comic", "comics", "manga", "webtoon", "webtoons", "manhwa", "manhua", "cartoon", "cartoons", "bande dessinée",
            "graphic novel", "graphic novels", "speech balloon", "speech balloons", "screentone", "screentones"]
CATS = ["cs.CV", "cs.CL", "cs.MM", "cs.AI", "cs.LG", "cs.GR", "cs.HC", "cs.IR", "cs.DL", "eess.IV"]
API = "http://export.arxiv.org/api/query"
NS = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}


def query(kw, field="ti"):
    phrase = f'{field}:"{kw}"' if " " in kw else f"{field}:{kw}"
    return f"{phrase} AND (" + " OR ".join(f"cat:{c}" for c in CATS) + ")"


def fetch(q, start, size=200):
    url = API + "?" + urllib.parse.urlencode({"search_query": q, "start": start, "max_results": size,
                                               "sortBy": "submittedDate", "sortOrder": "descending"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "awesome-comics-ai-sweep"}), timeout=60) as r:
                return ET.fromstring(r.read())
        except Exception as e:  # the API is slow and sometimes resets; back off and retry
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"arXiv API failed for {q!r} at {start}")


def records(feed):
    for e in feed.findall("a:entry", NS):
        aid = e.findtext("a:id", "", NS).rsplit("/abs/", 1)[-1]
        yield {"arxiv": aid.split("v")[0] if "v" in aid else aid, "version_id": aid,
               "title": " ".join(e.findtext("a:title", "", NS).split()),
               "authors": [a.findtext("a:name", "", NS) for a in e.findall("a:author", NS)],
               "published": e.findtext("a:published", "", NS)[:10], "updated": e.findtext("a:updated", "", NS)[:10],
               "primary": (e.find("x:primary_category", NS).get("term") if e.find("x:primary_category", NS) is not None else ""),
               "categories": [c.get("term") for c in e.findall("a:category", NS)],
               "comment": " ".join((e.findtext("x:comment", "", NS) or "").split()),
               "journal_ref": " ".join((e.findtext("x:journal_ref", "", NS) or "").split()),
               "summary": " ".join(e.findtext("a:summary", "", NS).split())}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("out"); ap.add_argument("--since", default="")
    ap.add_argument("--field", default="ti", choices=["ti", "abs"], help="search titles (default) or abstracts")
    a = ap.parse_args()
    found = {}
    for kw in KEYWORDS:
        start = 0
        while True:
            feed = fetch(query(kw, a.field), start)
            batch = list(records(feed))
            new = [r for r in batch if r["published"] >= a.since]
            for r in new:
                found.setdefault(r["arxiv"], dict(r, keywords=[], field=a.field))["keywords"].append(kw)
            print(f"{kw!r}: start {start}, {len(batch)} records", file=sys.stderr)
            if len(batch) < 200 or len(new) < len(batch):
                break
            start += 200
            time.sleep(3)
        time.sleep(3)
    out = sorted(found.values(), key=lambda r: r["published"], reverse=True)
    json.dump(out, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{len(out)} papers", file=sys.stderr)


if __name__ == "__main__":
    main()
