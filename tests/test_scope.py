"""The watcher's scope and section rules, measured on the hand-sorted list (titles only, so the test needs no network)."""
import pathlib, sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import scope  # noqa: E402

ROWS = [p for name in ("papers.yaml", "not_included.yaml") for p in yaml.safe_load((ROOT / "data" / name).read_text(encoding="utf-8"))]


def test_every_listed_title_that_names_comics_is_in_scope():
    named = [p for p in ROWS if scope.COMIC.search(p["title"]) or scope.INSIDE.search(p["title"])]
    assert len(named) > 150
    assert all(scope.in_scope(p["title"]) for p in named)


def test_one_passing_mention_in_the_abstract_is_not_enough():
    assert not scope.in_scope("Efficient video diffusion", "We test on films, cartoons and natural videos.")
    assert scope.in_scope("Efficient panel reading", "A manga page ... manga panels ... on Manga109.")


def test_sections_from_titles_alone_match_the_hand_sorting():
    # story visualization is reachable only by hand: those papers do not name comics, so the watcher never finds them
    rows = [p for p in ROWS if p["category"] != "storyviz"]
    hits = sum(scope.section_for(p["title"])[0] == p["category"] for p in rows)
    assert hits / len(rows) >= 0.85, f"{hits}/{len(rows)}"


def test_narrow_sections_win_over_broad_ones():
    assert scope.section_for("Reference-Guided Line Art Colorization for Manga")[0] == "creation"
    assert scope.section_for("Text-to-Comic Generation with Diffusion")[0] == "generation"
    assert scope.section_for("Speech Balloon Detection in Comics")[0] == "text"
    assert scope.section_for("Open-Set Comic Character Re-Identification")[0] == "identity"
    assert scope.section_for("Retrieval-Augmented Manga Colorization")[0] == "creation"
    assert scope.section_for("Translating Manga with the Page in View")[0] == "translation"


def test_benchmarks_outside_the_datasets_section_are_flagged():
    section, dataset = scope.section_for("A Manga Question Answering Benchmark for Vision-Language Models")
    assert (section, dataset) == ("vlm", True)
    assert scope.section_for("ComicScene154: A Scene Dataset for Comic Analysis") == ("datasets", False)


def test_animation_cartoons_and_acronyms_are_not_comics():
    # three real arXiv papers from 2026 that an earlier version of the rule would have added
    assert not scope.in_scope("Dynamic Skinning: Kinematics-Driven Cartoon Effects for Articulated Characters")
    assert not scope.in_scope("Brain-Aligned Multimodal LLMs for Social and Emotional Understanding of Cartoon Movies")
    assert not scope.in_scope("COMIC: Reference-Aware Safety Gating for Multimodal Large Language Models")
    assert not scope.in_scope("Manganese Oxide Catalysts Screened with Graph Neural Networks")


def test_print_cartoons_and_compound_names_still_count():
    assert scope.in_scope("Searching Digital Political Cartoons")
    assert scope.in_scope("An Interactive Web-Based System for Creating Single Panel Cartoons with Visually Valid Compositions")
    assert scope.in_scope("MangaNinja: Line Art Colorization with Precise Reference Following")
    assert scope.in_scope("MANGAN: ASSISTING COLORIZATION OF MANGA CHARACTERS CONCEPT ART USING CONDITIONAL GAN")
