"""The inclusion rule, in one place. build.py, verify.py and refresh.py all use it.

A paper is in the list when one of these holds:
  1. its venue is a conference or journal ranked A* or A by CORE (data/venues.yaml);
  2. its venue is a workshop, or a peer-reviewed track of such a conference (Findings, briefs, extended abstracts);
  3. it is a dataset or benchmark paper (section "datasets", or `dataset: true`), at any published venue;
  4. it is an arXiv preprint whose first version is at most PREPRINT_MONTHS old.
A preprint older than that leaves the list, unless it has since been published at a venue that meets rule 1 or 2.
Surveys (section "surveys") follow their own rule instead: a survey of comics is listed when it is peer-reviewed at any venue,
or when it is a preprint with at least SURVEY_MIN_CITATIONS citations (the field `citations`, which refresh.py updates).
"""
import datetime as dt
import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
PREPRINT_MONTHS = 4
SURVEY_MIN_CITATIONS = 10


def venues():
    return yaml.safe_load((ROOT / "data" / "venues.yaml").read_text(encoding="utf-8"))


def months_before(day, n):
    y, m = divmod(day.year * 12 + day.month - 1 - n, 12)
    m += 1
    last = (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)).day
    return dt.date(y, m, min(day.day, last))


def preprint_cutoff(today=None):
    return months_before(today or dt.date.today(), PREPRINT_MONTHS)


def reason_out(p, table, today=None):
    """None when the paper meets the rule, else why it does not."""
    v = table.get(p.get("venue"))
    if v is None:
        return f"venue {p.get('venue')!r} is not in data/venues.yaml"
    if p.get("category") == "surveys":
        if v["kind"] in ("conference", "journal", "workshop", "track"):
            return None
        c = p.get("citations")
        if v["kind"] == "preprint" and c is not None and int(c) >= SURVEY_MIN_CITATIONS:
            return None
        return f"survey preprint with {c if c is not None else 'an unknown number of'} citations, fewer than {SURVEY_MIN_CITATIONS}"
    if v["kind"] in ("conference", "journal") and v["rank"] in ("A*", "A"):
        return None
    if v["kind"] in ("workshop", "track"):
        return None
    if v["kind"] == "preprint":
        d = p.get("date")
        if not d:
            return "arXiv preprint without a first-version date"
        if dt.date.fromisoformat(str(d)) >= preprint_cutoff(today):
            return None
        return f"arXiv preprint from {d}, older than {PREPRINT_MONTHS} months and not published at a qualifying venue"
    if p.get("category") == "datasets" or p.get("dataset"):
        return None
    return f"{p['venue']} is {v['rank'] if v['rank'] != 'unranked' else 'not ranked'} by CORE"
