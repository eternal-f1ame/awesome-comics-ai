"""The watcher's pieces that need no network: the search window, entries built from arXiv records, code links, holds."""
import datetime as dt, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import policy  # noqa: E402
import watch  # noqa: E402

D = dt.date


def test_window_reaches_back_past_the_last_finished_run():
    assert watch.window_start(D(2026, 12, 1), D(2026, 11, 15)) == D(2026, 11, 5)


def test_window_without_a_finished_run_and_its_cap():
    assert watch.window_start(D(2026, 12, 1), None) == D(2026, 10, 17)
    assert watch.window_start(D(2026, 12, 1), D(2026, 6, 1)) == D(2026, 10, 2)


def test_authors_are_the_first_author_then_et_al():
    assert watch.short_authors(["Ada Lovelace", "Alan Turing"]) == "Ada Lovelace et al."
    assert watch.short_authors(["Ada Lovelace"]) == "Ada Lovelace"
    assert watch.short_authors([]) == ""


def test_code_link_is_the_first_repository_named_in_the_comment_or_abstract():
    assert watch.code_link("Code: https://github.com/foo/bar-baz.", "") == "https://github.com/foo/bar-baz"
    assert watch.code_link("", "Our code is at github.com/Foo/Bar.git and the data at https://huggingface.co/x") == "https://github.com/Foo/Bar"
    assert watch.code_link("Project page: https://foo.github.io/bar", "no repository here") is None


def test_hold_patterns_match_titles_without_revealing_them():
    assert watch.held("A Secret Benchmark: Reading Comics", ["secret benchmark"]) is True
    assert watch.held("Another Comic Paper", ["secret benchmark"]) is False
    assert watch.held("Anything", []) is False


RECORD = {"arxiv": "2611.01234", "title": "Speech Balloon Detection in Webtoons", "authors": ["Ada Lovelace", "Alan Turing"],
          "published": "2026-11-10", "comment": "Code: https://github.com/ada/balloons", "summary": "We detect balloons in webtoons.",
          "journal_ref": ""}


def test_a_new_record_becomes_a_preprint_entry_in_its_section():
    e = watch.entry_from(RECORD)
    assert e == {"title": "Speech Balloon Detection in Webtoons", "authors": "Ada Lovelace et al.", "year": 2026, "venue": "arXiv",
                 "category": "text", "arxiv": "2611.01234", "date": "2026-11-10", "code": "https://github.com/ada/balloons"}
    assert policy.reason_out(e, policy.venues(), D(2026, 12, 1)) is None


def test_a_record_already_published_takes_its_venue():
    lookup = lambda title: ("ICDAR Workshops", 2026, "10.1007/xyz", "ICDAR 2026 Workshops")
    e = watch.published_version(watch.entry_from(RECORD), policy.venues(), lookup)
    assert (e["venue"], e["year"], e["paper"]) == ("ICDAR Workshops", 2026, "https://doi.org/10.1007/xyz")
    assert "date" not in e


def test_a_record_with_no_or_unknown_publication_stays_a_preprint():
    e = watch.entry_from(RECORD)
    assert watch.published_version(dict(e), policy.venues(), lambda t: None) == e
    assert watch.published_version(dict(e), policy.venues(), lambda t: (None, 2026, "10.1/x", "Some Unknown Venue")) == e


def test_an_empty_first_page_is_asked_again_before_it_is_believed(monkeypatch):
    calls = []
    rec = dict(RECORD, published="2026-11-15")

    def fetch(q, start):                                  # the record is found only by the title query, and only when asked again
        calls.append(q)
        title_calls = [c for c in calls if c.startswith("ti:")]
        return [rec] if q.startswith("ti:") and len(title_calls) == 2 else []
    monkeypatch.setattr(watch.arxiv_sweep, "fetch", fetch)
    monkeypatch.setattr(watch.arxiv_sweep, "records", lambda feed: feed)
    monkeypatch.setattr(watch.arxiv_sweep, "KEYWORDS", ["manga"])
    monkeypatch.setattr(watch.time, "sleep", lambda s: None)
    out = watch.sweep("2026-11-01")
    assert [r["arxiv"] for r in out] == ["2611.01234"]
