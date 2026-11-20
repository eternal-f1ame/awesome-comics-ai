"""The checks on data/news.yaml, the items in the home page's "Around the field" section."""
import pathlib, sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build  # noqa: E402

GOOD = {"kind": "industry", "title": "A platform ships a tool", "note": "One sentence.", "source": "A paper", "date": "2026-11-16",
        "url": "https://example.org/news"}


def test_the_published_news_passes():
    news = yaml.safe_load((ROOT / "data" / "news.yaml").read_text(encoding="utf-8"))
    assert news and build.check_news(news) == []


def test_a_sponsored_item_must_name_its_sponsor():
    assert build.check_news([dict(GOOD, kind="sponsored")])
    assert build.check_news([dict(GOOD, kind="sponsored", sponsor="A company")]) == []


def test_bad_links_dates_and_kinds_are_caught():
    assert build.check_news([dict(GOOD, url="http://example.org")])
    assert build.check_news([dict(GOOD, date="Nov 2026")])
    assert build.check_news([dict(GOOD, kind="advert")])
    assert build.check_news([{k: v for k, v in GOOD.items() if k != "source"}])
