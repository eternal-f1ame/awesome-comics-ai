"""The news watcher's rules, on real headlines from 2026 (the dry run of 2026-11-20 found them)."""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import news_watch as nw  # noqa: E402


def test_ai_must_be_in_the_headline_as_a_word():
    assert nw.ai_headline("GlobalComix's AI-Powered Refresh Looks a Lot Like Its Competition")
    assert nw.ai_headline("Art Spiegelman Uses A.I. On His Comic, Gail Simone Responds")
    assert nw.ai_headline("Shueisha calls generative tools a risk to manga")
    assert not nw.ai_headline("AI no Idenshi's Kyūri Yamada Launches New Manga")       # a Japanese title: "The Gene of AI"
    assert not nw.ai_headline("Oshi no Ko's Ai Hoshino Gets a Figure")
    assert not nw.ai_headline("Kodansha Announces Fall Manga Lineup")


def test_kept_stories_are_about_comics():
    keep = [("Kakao, OpenAI Collaborate on AI-Generated Short Animation Based on Ryan Begins Webtoon", ""),
            ("Getbackers Manga Gets Comic Anime From AI Platform MangaNow Studio", ""),
            ("Vinland Saga Creator Makoto Yukimura Addresses Comments on AI Imagery", "The Vinland Saga manga author responded to readers."),
            ("BATMAN: DARK PATTERNS reprinted after accusations of AI generated trade synopsis", "The trade paperback has been reprinted."),
            ("GlobalComix's AI-Powered Refresh Looks a Lot Like Its Competition", "The update adds automated comic-page descriptions.")]
    for title, excerpt in keep:
        assert nw.relevant(title, excerpt), title


def test_games_film_and_anime_stories_are_left_out():
    drop = [("GDC State of the Game Industry Report - Insights on Job Market, AI, Next-Gen and More", ""),
            ("GetBackers “comic anime” series reboot draws criticism over suspected generative AI use in trailer", "A manga reboot."),
            ("Major Japanese broadcaster Fuji TV plans to use generative AI in all its live-action series by the end of 2027", ""),
            ("Official SUPERGIRL video made private after AI allegations", "DC's film studio removed the video."),
            ("[UPDATED] SDCC ’26: AVATAR AANG ChatGPT controversy, explained", "A slide at the panel cited ChatGPT, prompting controversy for the film."),
            ("Over 85% of Japanese game developers use generative AI in game development", "")]
    for title, excerpt in drop:
        assert not nw.relevant(title, excerpt), title


def test_comics_must_be_named_in_the_headline_or_the_summary():
    assert not nw.relevant("Japan adopts new guidelines urging AI companies to disclose training data", "Publishers welcomed the move.")
    assert nw.relevant("Japan adopts new guidelines urging AI companies to disclose training data", "Manga publishers welcomed the move.")


def item(source, title, excerpt="", date="2026-10-26"):
    return {"source": source, "title": title, "excerpt": excerpt, "date": date, "url": "https://example.org/" + source.replace(" ", "")}


def test_a_story_is_cited_from_the_most_reliable_outlet_that_reported_it():
    beat = item("The Beat", "Art Spiegelman used AI for sticker on IN THE SHADOW OF NO TOWERS", "Maus author Art Spiegelman disclosed using AI.")
    bc = item("Bleeding Cool", "Art Spiegelman Uses A.I. On His Comic, Gail Simone Responds", "The creator of Maus used generative AI.")
    stories = nw.stories([bc, beat], known=[])
    assert [s["source"] for s in stories] == ["The Beat"]          # Bleeding Cool confirms it is about comics; The Beat is cited


def test_bleeding_cool_alone_is_not_enough():
    only = item("Bleeding Cool", "\"Creating\" A.I. Graphic Novels At NYCC And Frankfurt Book Fair", "Generative A.I. is the bane of the comic book industry.")
    assert nw.stories([only], known=[]) == []


def test_a_story_already_on_the_page_is_not_added_again():
    ann = item("Anime News Network", "WEBTOON Launches AI Story Chat Service byUs Featuring Creator-Approved Webtoon IP", date="2026-07-11")
    assert nw.stories([ann], known=[("Naver Webtoon opens byUs, an AI story chat", "2026-07-01")]) == []
    assert [s["source"] for s in nw.stories([ann], known=[])] == ["Anime News Network"]


def test_the_note_is_the_first_sentence_without_the_feed_footer():
    raw = "<p>Maus author Art Spiegelman disclosed using AI. It spurred debate.</p><p>The post Art Spiegelman used AI appeared first on The Beat.</p>"
    assert nw.first_sentence(raw) == "Maus author Art Spiegelman disclosed using AI."
    assert nw.first_sentence("<p>A long summary [&hellip;]</p>") == "A long summary."
    assert len(nw.first_sentence("word " * 200)) <= 220


def test_two_outlets_on_one_story_count_once():
    assert nw.same_story("Art Spiegelman used AI for sticker on IN THE SHADOW OF NO TOWERS",
                         "Art Spiegelman Uses A.I. On His Comic, Gail Simone Responds")
    assert nw.same_story("Naver Webtoon opens byUs, an AI story chat", "WEBTOON Launches AI Story Chat Service byUs Featuring Creator-Approved Webtoon IP")
    assert not nw.same_story("WEBTOON adds opt-in AI translation to CANVAS", "WEBTOON and Genies turn comic characters into 3D avatars")


def test_the_monthly_newsroom_page_is_read_into_dated_items():
    page = ('<a href="/news/2026-11-14/kakao-openai/.243600">Kakao, OpenAI Collaborate on AI-Generated Short Animation</a>'
            '<a href="/interest/2026-11-09/vinland/.243400">Vinland Saga Creator <b>Addresses</b> AI</a>'
            '<a href="/news/2026-10-01/old/.200">Old item</a><a href="/encyclopedia/manga.php?id=1">Not news</a>')
    items = nw.ann_items(page, "2026-11-01")
    assert [(i["date"], i["title"]) for i in items] == [("2026-11-14", "Kakao, OpenAI Collaborate on AI-Generated Short Animation"),
                                                         ("2026-11-09", "Vinland Saga Creator Addresses AI")]
    assert items[0]["url"] == "https://www.animenewsnetwork.com/news/2026-11-14/kakao-openai/.243600"


def test_icv2_kadokawa_and_feed_pages_are_read_into_dated_items():
    icv2 = ('<div class="title-text"><a href="https://icv2.com/articles/news/view/63939/three-more">Three More DC Compact Editions</a></div>'
            '<div class="subtitle-text">In July</div><div class="date-text">November 20, 2026</div><div class="abstract-text"><p>DC has solicited three.</p></div>')
    assert nw.icv2_items(icv2, "2026-11-01") == [{"source": "ICv2", "date": "2026-11-20", "title": "Three More DC Compact Editions",
                                                  "url": "https://icv2.com/articles/news/view/63939/three-more", "excerpt": "<p>DC has solicited three.</p>"}]
    kado = ('<a class="x" href="https://group.kadokawa.co.jp/global/information/news_release/2026111601_en.html"><div class="info"><time class="time">'
            'Nov 16, 2026</time></div><p class="text">KADOKAWA and Medialink Agree to Establish Joint Ventures</p></a>')
    assert [(i["date"], i["title"]) for i in nw.kadokawa_items(kado, "2026-11-01")] == [("2026-11-16", "KADOKAWA and Medialink Agree to Establish Joint Ventures")]
    rss = ('<rss><channel><item><title><![CDATA[Rebecca Taylor Named VP]]></title><link>https://pw.org/a</link>'
           '<pubDate>Wed, 18 Nov 2026 10:00:00 GMT</pubDate><description>A new publisher.</description></item>'
           '<item><title>Old</title><link>https://pw.org/b</link><pubDate>2026-04-07T10:00:00+00:00</pubDate></item></channel></rss>')
    assert [(i["date"], i["title"], i["url"]) for i in nw.rss_items(rss, "Publishers Weekly", "2026-11-01")] == [("2026-11-18", "Rebecca Taylor Named VP", "https://pw.org/a")]


def test_a_failing_source_is_named_and_skipped(monkeypatch):
    def fake_get(url, as_json=False, missing_ok=False):
        if "icv2.com" in url:
            raise RuntimeError("down")
        if "about.webtoon.com" in url:
            return None
        if as_json:
            return [{"date": "2026-11-15T10:00:00", "link": "https://www.comicsbeat.com/x", "title": {"rendered": "A manga AI story"},
                     "excerpt": {"rendered": "About manga."}}] if "comicsbeat" in url else []
        return "<rss></rss>" if "feed" in url or url.endswith(".xml") else ""
    monkeypatch.setattr(nw, "get", fake_get)
    monkeypatch.setattr(nw.time, "sleep", lambda s: None)
    items, failed, last = nw.collect("2026-11-10", 262)
    assert failed == ["ICv2 (RuntimeError)"]
    assert any(i["source"] == "The Beat" for i in items) and last == 261
