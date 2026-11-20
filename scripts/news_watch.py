"""Add industry news about AI and comics to data/news.yaml: the home page's "Around the field" section.

Runs every two weeks in the GitHub Action, after watch.py, with the same search window: from 10 days before the last run that
finished (news_last_complete in data/watch.yaml). Every source is read over the whole window, not only its latest posts:
  - first-party newsrooms: WEBTOON Entertainment's press releases (numbered; the last one read is kept in data/watch.yaml),
    KADOKAWA's news releases, Kodansha USA's site search;
  - Anime News Network's monthly newsroom pages;
  - ICv2's news pages and Publishers Weekly's comics feed;
  - the site search of The Beat, K-Comics Beat and other outlets that run WordPress, and Popverse's feed;
  - Bleeding Cool, which is often first but less careful: a story only it reports does not enter.

A story is kept when a headline names AI (the word in capitals, or generative AI, machine translation and the like) and it is
about comics: a headline names manga, webtoons or comic books, or a headline names no other medium (anime, games, film, TV,
music) and the summary names comics. Reports of one story by several outlets are judged together, and the story enters once,
cited from the most reliable outlet that reported it (SOURCES gives the order), with that outlet's headline, the first sentence
of its own summary, its date and its link, as kind "industry". Stories already in data/news.yaml or data/excluded.yaml are
skipped, and titles that match WATCH_HOLD are left out unprinted, as in watch.py. A source that fails is skipped and named in the
run summary, and the window then stays where it was, so the next run reads those days again.

Usage: python scripts/news_watch.py [--dry-run] [--since YYYY-MM-DD]
"""
import argparse, datetime as dt, email.utils, gzip, html, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

import yaml

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import policy
import watch

ROOT = policy.ROOT
UA = {"User-Agent": "awesome-comics-ai-news"}
ANN = "https://www.animenewsnetwork.com"
# Every source, most reliable first: a story reported by several is cited from the first of them.
SOURCES = ["WEBTOON Entertainment", "KADOKAWA", "Kodansha USA", "Anime News Network", "ICv2", "Publishers Weekly", "The Beat",
           "K-Comics Beat", "Popverse", "ComicBook.com", "Automaton West", "Anime Herald", "Anime Hunch", "Otaku USA", "Slator",
           "Bleeding Cool"]
CONFIRM = {"Bleeding Cool"}          # a story only these report does not enter
WORDPRESS = [("Kodansha USA", "https://kodansha.us"), ("The Beat", "https://www.comicsbeat.com"), ("K-Comics Beat", "https://kcomicsbeat.com"),
             ("ComicBook.com", "https://comicbook.com"), ("Automaton West", "https://automaton-media.com/en"),
             ("Anime Herald", "https://www.animeherald.com"), ("Anime Hunch", "https://animehunch.com"), ("Otaku USA", "https://otakuusamagazine.com"),
             ("Slator", "https://slator.com"), ("Bleeding Cool", "https://bleedingcool.com")]
FEEDS = [("Publishers Weekly", "https://www.publishersweekly.com/pw/feeds/section/comics/index.xml"), ("Popverse", "https://www.thepopverse.com/feed")]
SEARCH_TERMS = ["generative", "artificial intelligence", "AI-generated", "AI-powered", "machine translation", "OpenAI"]
WEBTOON_FIRST = 240                  # the first WEBTOON press release to read when data/watch.yaml has no record yet

AI_CS = re.compile(r"\b(AI|LLMs?|GenAI)\b(?! no\b)|\bAI-|\bA\.I\.(?!\w)")          # "AI no ..." is a Japanese title, not AI
AI_CI = re.compile(r"artificial intelligence|generative|machine[- ]translat\w*|\bOpenAI\b|ChatGPT|Midjourney|Stable Diffusion", re.I)
STRONG = re.compile(r"\b(manga|mangas|mangaka|webtoons?|manhwa|manhua|comic books?|comics|graphic novels?|comic strips?|"
                    r"bandes? dessin\w*|doujinshi|4-?koma|trade paperbacks?)\b", re.I)
COMIC = re.compile(STRONG.pattern + r"|\bcomic\b|\bcomic-", re.I)
OTHER = re.compile(r"\b(anime|trailers?|games?|gaming|films?|movies?|episodes?|videos?|voice|actors?|actress|reboot|TV|music|album|songs?)\b", re.I)
WORD = re.compile(r"\b[A-Za-z][A-Za-z'’]{2,}\b")
COMMON = {"ai", "the", "and", "for", "with", "new", "how", "why", "what", "after", "over", "from", "into", "its", "his", "her", "their",
          "manga", "webtoon", "webtoons", "comic", "comics", "anime", "japan", "japanese", "korean", "says", "uses", "used", "gets",
          "launches", "announces", "updated", "first", "series", "story", "stories"}


def ai_headline(title):
    return bool(AI_CS.search(title) or AI_CI.search(title))


def relevant(title, excerpt):
    if not ai_headline(title):
        return False
    if STRONG.search(title):
        return True
    if OTHER.search(title):
        return False
    return bool(COMIC.search(title) or COMIC.search(excerpt or ""))


def first_sentence(raw, limit=220):
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw or ""))
    text = re.sub(r"The post .*? appeared first on .*", "", text, flags=re.S)
    text = re.sub(r"\s*(\[(…|\.\.\.)\]|…|Continue reading.*|Read more.*)\s*$", "", " ".join(text.split()))
    m = re.match(r"(.+?[.!?])(\s|$)", text)
    out = (m.group(1) if m else text).strip()
    if len(out) > limit:
        out = out[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    return out if not out or out[-1] in ".!?…" else out + "."


def _names(title):
    """The headline's names, each with a weight: 2 for a brand-like name (a capital inside it, such as byUs or GlobalComix), else 1."""
    out = {}
    for w in WORD.findall(title):
        if w.lower() in COMMON or not any(c.isupper() for c in w):
            continue
        out[w.lower()] = 2 if any(c.isupper() for c in w[1:]) and not w.isupper() else 1
    return out


def same_story(a, b):
    na, nb = _names(a), _names(b)
    return sum(max(na[k], nb[k]) for k in na.keys() & nb.keys()) >= 2


def near(a, b, days=10):
    return abs((dt.date.fromisoformat(a) - dt.date.fromisoformat(b)).days) <= days


def stories(items, known):
    """Group the reports into stories, judge each story on all its reports, and return one news item per new story.

    items: reports whose headline names AI; known: (title, date) of the items already on the page."""
    rank = {s: i for i, s in enumerate(SOURCES)}
    groups = []
    for it in sorted(items, key=lambda i: (rank.get(i["source"], len(SOURCES)), i["date"])):
        for g in groups:
            if any(near(it["date"], o["date"]) and same_story(it["title"], o["title"]) for o in g):
                g.append(it); break
        else:
            groups.append([it])
    out = []
    for g in groups:
        if not any(relevant(o["title"], o.get("excerpt", "")) for o in g) or all(o["source"] in CONFIRM for o in g):
            continue
        if any(near(o["date"], d) and same_story(o["title"], t) for o in g for t, d in known):
            continue
        best = g[0]
        note = next((first_sentence(o["excerpt"]) for o in [best] + g if o.get("excerpt") and first_sentence(o["excerpt"])), "")
        out.append({"kind": "industry", "title": best["title"], "note": note or f"Reported by {best['source']}.", "source": best["source"],
                    "date": best["date"], "url": best["url"]})
    return sorted(out, key=lambda n: n["date"], reverse=True)


# ---- readers: each turns one page into a list of {source, date, title, url, excerpt} ----

def _text(s):
    s = re.sub(r"<!\[CDATA\[|\]\]>", "", s or "")             # CDATA first, or the tag pattern swallows the text inside it
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def _day(s):
    s = s.strip()
    try:
        return email.utils.parsedate_to_datetime(s).date().isoformat()
    except (TypeError, ValueError):
        pass
    for fmt in ("%B %d, %Y", "%b %d, %Y", "%m/%d/%Y"):
        try:
            return dt.datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            pass
    return s[:10]


def ann_items(page, since):
    out, seen = [], set()
    for href, day, inner in re.findall(r'<a href="(/(?:news|press-release|interest|daily-briefs)/(\d{4}-\d{2}-\d{2})/[^"]+)"[^>]*>(.*?)</a>', page, re.S):
        title = _text(inner)
        if title and day >= since and href not in seen:
            seen.add(href)
            out.append({"source": "Anime News Network", "date": day, "title": title, "url": ANN + href, "excerpt": ""})
    return out


def icv2_items(page, since):
    out = []
    for href, title, rest in re.findall(r'<div class="title-text"><a href="(https://icv2\.com/articles/news/view/\d+/[^"]+)">(.*?)</a></div>(.*?)(?=<div class="title-text">|$)', page, re.S):
        d = re.search(r'<div class="date-text">(.*?)</div>', rest)
        ex = re.search(r'<div class="abstract-text">(.*?)</div>', rest, re.S)
        day = _day(d.group(1)) if d else ""
        if day >= since:
            out.append({"source": "ICv2", "date": day, "title": _text(title), "url": href, "excerpt": ex.group(1) if ex else ""})
    return out


def kadokawa_items(page, since):
    out = []
    for href, block in re.findall(r'<a[^>]+href="(https://group\.kadokawa\.co\.jp/global/information/news_release/\d+_en\.html)"[^>]*>(.*?)</a>', page, re.S):
        t = re.search(r'<time[^>]*>(.*?)</time>', block)
        p = re.search(r'<p class="text[^"]*"[^>]*>(.*?)</p>', block, re.S)
        day = _day(t.group(1)) if t else ""
        if p and day >= since:
            out.append({"source": "KADOKAWA", "date": day, "title": _text(p.group(1)), "url": href, "excerpt": ""})
    return out


def rss_items(xml, source, since):
    out = []
    for it in re.findall(r"<item>(.*?)</item>", xml, re.S):
        get_ = lambda tag: (re.findall(rf"<{tag}[^>]*>(.*?)</{tag}>", it, re.S) or [""])[0]
        day = _day(_text(get_("pubDate")))
        if day >= since:
            out.append({"source": source, "date": day, "title": _text(get_("title")), "url": _text(get_("link")), "excerpt": get_("description")})
    return out


def get(url, as_json=False, missing_ok=False):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                body = r.read()
            if body[:2] == b"\x1f\x8b":
                body = gzip.decompress(body)
            return json.loads(body) if as_json else body.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if missing_ok and e.code == 404:
                return None
            time.sleep(5 * (attempt + 1))
        except Exception:
            time.sleep(5 * (attempt + 1))
    raise RuntimeError("request failed: " + url)


def description(url):
    """The page's own summary (its og:description), for a report whose source gives none."""
    try:
        page = get(url)
    except RuntimeError:
        return ""
    m = re.search(r'<meta[^>]+(?:property="og:description"|name="description")[^>]+content="([^"]*)"', page or "")
    return html.unescape(m.group(1)) if m else ""


def webtoon_items(first, since):
    """WEBTOON Entertainment's press releases from number `first` on, until two numbers in a row are missing; and the last read."""
    out, n, misses, last = [], first, 0, first - 1
    while misses < 2:
        page = get(f"https://about.webtoon.com/press-release/{n}", missing_ok=True)
        if page and "WEBTOON" in page:
            misses, last = 0, n
            t = re.search(r"<title>(.*?)</title>", page, re.S)
            d = re.search(r"\b(\d{2}/\d{2}/\d{4})\b", page)
            day = _day(d.group(1)) if d else ""
            if t and day >= since:
                out.append({"source": "WEBTOON Entertainment", "date": day, "title": _text(t.group(1)).replace(" | WEBTOON Entertainment", ""),
                            "url": f"https://about.webtoon.com/press-release/{n}", "excerpt": ""})
        else:
            misses += 1
        n += 1
        time.sleep(1)
    return out, last


def collect(since, webtoon_first):
    """Every report in the window, the sources that failed, and the last WEBTOON press release read. A source that fails is
    skipped and named; main() then keeps the window where it was, so the next run reads those days again."""
    items, failed = [], []
    start, today = dt.date.fromisoformat(since), dt.date.today()

    def read(name, fn):
        try:
            items.extend(fn())
        except Exception as e:                       # one outlet down must not stop the others, or the paper update
            failed.append(f"{name} ({type(e).__name__})")

    months = sorted({(d.year, d.month) for d in (start + dt.timedelta(days=k) for k in range((today - start).days + 1))})
    for y, m in months:
        read("Anime News Network", lambda: ann_items(get(f"{ANN}/newsroom/{y}/{m:02d}"), since)); time.sleep(2)

    def icv2():
        out = []
        for page_no in range(1, 121):                # ICv2's news pages, newest first, until the window is passed
            got = icv2_items(get(f"https://icv2.com/articles/news?page={page_no}"), "0000")
            out += [i for i in got if i["date"] >= since]
            if not got or min(i["date"] for i in got) < since:
                return out
            time.sleep(1)
        return out
    read("ICv2", icv2)
    read("KADOKAWA", lambda: kadokawa_items(get("https://group.kadokawa.co.jp/global/information/news_release/"), since))
    for name, url in FEEDS:
        read(name, lambda: rss_items(get(url), name, since))
    for name, base in WORDPRESS:
        def wp():
            out = []
            for term in SEARCH_TERMS:
                q = urllib.parse.urlencode({"search": term, "after": since + "T00:00:00", "per_page": 50, "_fields": "date,link,title,excerpt"})
                for r in get(f"{base}/wp-json/wp/v2/posts?{q}", as_json=True):
                    out.append({"source": name, "date": r["date"][:10], "url": r["link"], "title": _text(r["title"]["rendered"]),
                                "excerpt": r["excerpt"]["rendered"]})
                time.sleep(1)
            return out
        read(name, wp)
    last = webtoon_first - 1
    try:
        wt, last = webtoon_items(webtoon_first, since)
        items.extend(wt)
    except Exception as e:
        failed.append(f"WEBTOON Entertainment ({type(e).__name__})")
    for it in items:                                 # some feeds still give http links; every one of these sites serves https
        if it["url"].startswith("http://"):
            it["url"] = "https://" + it["url"][7:]
    return items, failed, last


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--since", default="")
    a = ap.parse_args()
    today = dt.date.today()
    state = (yaml.safe_load(watch.STATE.read_text(encoding="utf-8")) if watch.STATE.exists() else None) or {}
    last = state.get("news_last_complete")
    since = a.since or str(watch.window_start(today, dt.date.fromisoformat(str(last)) if last else None))
    holds = [l.strip() for l in os.environ.get("WATCH_HOLD", "").splitlines() if l.strip()]

    path = ROOT / "data" / "news.yaml"
    head = "".join(l for l in path.read_text(encoding="utf-8").splitlines(True) if l.startswith("#"))
    news = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    excluded = yaml.safe_load((ROOT / "data" / "excluded.yaml").read_text(encoding="utf-8")) or []
    known_urls = {str(n.get("url")) for n in news + excluded if n.get("url")}
    known = [(n["title"], str(n["date"])) for n in news] + [(n["title"], str(n.get("date", "1900-01-01"))) for n in excluded if n.get("url")]

    reports, failed, webtoon_last = collect(since, int(state.get("webtoon_press_last", WEBTOON_FIRST - 1)) + 1)
    reports = [r for r in reports if ai_headline(r["title"]) and r["url"] not in known_urls]
    n_held = sum(watch.held(r["title"], holds) for r in reports)
    reports = [r for r in reports if not watch.held(r["title"], holds)]
    for r in reports:                                # a report with no summary of its own: read the page's
        if not r["excerpt"] and not STRONG.search(r["title"]) and not OTHER.search(r["title"]):
            r["excerpt"] = description(r["url"]); time.sleep(1)
    added = stories(reports, known)
    for n in added:
        if n["note"].startswith("Reported by "):
            n["note"] = first_sentence(description(n["url"])) or n["note"]

    print(f"## News: since {since}\n")
    print(f"{len(reports)} reports with AI in the headline, {len(added)} stories added" + (f", {n_held} held" if n_held else "") + ".\n")
    for n in added:
        print(f"- added: [{n['title']}]({n['url']}) ({n['source']}, {n['date']})")
    if failed:
        print("\nNot read this time, so the next run reads these days again: " + ", ".join(failed) + ".")
    if a.dry_run:
        print("\n(dry run, nothing written)")
        return
    news = sorted(news + added, key=lambda n: str(n["date"]), reverse=True)
    path.write_text(head + yaml.safe_dump(news, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    text = watch.STATE.read_text(encoding="utf-8")
    for key in ("news_last_complete", "webtoon_press_last"):
        text = re.sub(rf"^{key}:.*\n?", "", text, flags=re.M)
    done = last if failed else str(today)          # a source that failed keeps the window where it was
    text = text.rstrip("\n") + (f"\nnews_last_complete: '{done}'" if done else "") + f"\nwebtoon_press_last: {webtoon_last}\n"
    watch.STATE.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
