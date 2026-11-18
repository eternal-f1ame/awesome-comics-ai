"""Look up titles on Crossref, for papers that DBLP does not index (many workshop and journal papers).

Keeps a Crossref record only when its normalized title equals the entry's title, and returns its DOI, container (venue), year and
authors. Titles with no exact match are reported, never guessed.

Usage: python scripts/crossref_lookup.py IN.json OUT.json   (IN: a list of objects with a "title")
"""
import json, re, sys, time, urllib.parse, urllib.request

norm = lambda t: re.sub(r"[^a-z0-9]", "", re.sub(r"<[^>]+>", "", t).lower())


def main():
    items = json.load(open(sys.argv[1], encoding="utf-8")); path = sys.argv[2]
    try:                                   # resume: keep what an earlier, interrupted run already found
        out = {k: v for k, v in json.load(open(path, encoding="utf-8")).items() if "error" not in v}
    except (FileNotFoundError, ValueError):
        out = {}
    for i, it in enumerate(items):
        if it["title"] in out:
            continue
        url = "https://api.crossref.org/works?" + urllib.parse.urlencode({"query.title": it["title"], "rows": 5,
                                                                          "select": "DOI,title,container-title,issued,author,type,event"})
        recs = []
        for attempt in range(4):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "awesome-comics-ai-verify"}), timeout=30) as r:
                    items_ = json.load(r)["message"]["items"]
                break
            except Exception:
                items_ = None; time.sleep(4 * (attempt + 1))
        for x in items_ or []:
            if not x.get("title") or norm(x["title"][0]) != norm(it["title"]):
                continue
            year = (x.get("issued", {}).get("date-parts") or [[None]])[0][0]
            recs.append({"doi": x.get("DOI"), "venue": (x.get("container-title") or [None])[0], "event": (x.get("event") or {}).get("name"),
                         "year": year, "type": x.get("type"),
                         "authors": [" ".join(filter(None, [a.get("given"), a.get("family")])) for a in x.get("author", [])]})
        out[it["title"]] = {"records": recs} if items_ is not None else {"error": "request failed"}
        if i % 10 == 0:
            json.dump(out, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
            print(f"{i}/{len(items)}", file=sys.stderr, flush=True)
        time.sleep(1)
    json.dump(out, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{sum(1 for v in out.values() if v.get('records'))} of {len(items)} titles matched on Crossref", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()
