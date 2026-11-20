"""Which new papers the watcher adds, and to which section. watch.py uses it; tests/test_scope.py measures it on the hand-sorted list.

in_scope(): comics must be the subject or the main test bed. A title that names comics (also inside a name such as MangaNinja) is
enough; otherwise the abstract must name them at least three times. A cartoon counts only as a print form (political, editorial,
single-panel, newspaper or gag cartoons): most cartoon papers are about animation.

section_for(): ordered rules over the title, then over the abstract when no title rule fires. The first rule that matches wins, so
the narrow sections (accessibility, translation, colorization) come before the broad ones (generation, analysis, understanding).
"""
import re

COMIC = re.compile(r"\b(comic|comics|manga|mangas|webtoons?|manhwa|manhua|bandes? dessin\w*|graphic novels?|comic strips?|speech balloons?|"
                   r"screentones?|manga109|4-?koma|yonkoma|motion comics?|(political|editorial|single[- ]panel|newspaper|gag) cartoons?|"
                   r"new yorker|cartoon strips?)\b", re.I)
# names built on the word, such as MangaNinja, ComicGAN or OpenManga; not words that merely contain it, such as manganese
INSIDE = re.compile(r"\b(Comic|Manga|Webtoon|Manhwa|Screentone)s?(?=[A-Z0-9])|[a-z0-9](Comic|Manga|Webtoon)s?\b")


def _named(title):
    """True when the title names comics. In a title that is not set in capitals, a capitalised COMIC or MANGA is an acronym."""
    caps = sum(c.isupper() for c in title) > 0.6 * sum(c.isalpha() for c in title)
    words = [m.group(0) for m in COMIC.finditer(title)]
    return any(caps or not w.isupper() for w in words) or bool(INSIDE.search(title))


def comic_mentions(text):
    """How often the text names comics, not counting a capitalised acronym such as COMIC."""
    return sum(not m.group(0).isupper() for m in COMIC.finditer(text or ""))


def in_scope(title, abstract=""):
    return _named(title) or comic_mentions(abstract) >= 3


# (section, title pattern). Order matters: see the module docstring.
_RULES = [
    ("surveys", r"\b(survey|literature review|systematic review|a review|overview of)\b"),
    ("accessibility", r"\b(accessib\w*|blind|low[- ]vision|visually impaired|screen readers?|audio descriptions?)\b"),
    ("probe", r"\b(jailbreak\w*|safety|harmful|red[- ]teaming|safety alignment|gaze heads|attention heads|structured visual storytelling)\b"),
    ("translation", r"\b(translat\w*|locali[sz]\w*)\b(?<!photo-to-manga translation)"),
    ("generation", r"\b(video|movie|film|animation)\w*\s*(2|to|into)\s*(comic|manga)|video2comics|movie2comics|comixify|keyframes|comic-like video"),
    ("animation", r"\b(animat\w*|motion comics?|speech synthesis|speech generation|voices?|music|audio\w*|sound\w*|camera movement|single-speaker)\b"),
    ("retrieval", r"\b(retriev(?!al[- ]augmented)\w*|recommend\w*|search\w*)\b"),
    ("restoration", r"\b(inpaint\w*|restor\w*|super[- ]resolution|vectori[sz]\w*|retarget\w*|dewarp\w*|compression|denois\w*|editing|upscal\w*|deblur\w*)\b"),
    ("creation", r"\b(colori[sz]\w*|line[- ]?art|screen(ing|tones?)|rescreen\w*|shading|structural lines|flat colo\w*|from sketch\w*|onomatopoeia generation|manga creation workflow)\b"),
    ("identity", r"\b(re-?identif\w*|character (recognition|identification|clustering|retrieval)|identity|character analysis)\b"),
    ("hci", r"\b(education\w*|teaching|pedagog\w*|students?|learners?|classroom|data comics?|graph comics|charts?|dashboards?|user study|authoring|storyboarding|creativity|co-creat\w*|youth|platform|cursor|conversations?|programming|computing|cs1|vr)\b"),
    ("studies", r"\b(at scale|four-scene|physiological|define manga|panel transitions|story pattern|insights from)\b"),
    ("generation", r"\b(comic|manga|webtoon)s? generation\b|\bgenerating (comics?|manga|webtoons?)\b|\btext-to-(image|comic)\w*"),
    ("text", r"\b(text(?!-to-)|texts|balloons?|bubbles?|speakers?|dialogu?e?s?|transcri\w*|onomatopoe\w*|furigana|ideophones?|serif\w*|ocr|lettering)\b"),
    ("generation", r"\b(generat\w*|synthes\w*|gan|diffusion|text-to-image|stylization|style transfer|photo-to-manga|layout-controllable|stylistic manga layout|manga-style layout|customi[sz]ed|b-roll|single panel cartoons)\b"),
    ("vlm", r"\b(vision[- ]language|vlms?|lmms?|mllms?|multimodal (large )?language|llms?|large (multimodal|language)|question[- ]answer\w*|qa|vqa)\b"),
    ("datasets", r"\b(dataset|datasets|corpus|annotations|benchmark)\b"),
    ("vlm", r"\b(reasoning|understanding|humou?r\w*|captions?|captioning|narratives?|cloze|complement|comprehen\w*|grounding|bert|decoding|inferences)\b"),
    ("studies", r"\b(analysis based|content analysis|genre analysis)\b"),
    ("analysis", r"\b(detect\w*|segment\w*|panels?|frames?|layouts?|depth|pose|faces?|landmarks?|genre|style|classif\w*|extract\w*|reading order|object|domain|exclamation|multi-?task|page stream|reconfigure)\b"),
]
RULES = [(name, re.compile(pat, re.I)) for name, pat in _RULES]
BENCHMARK = re.compile(r"\b(benchmark\w*|dataset\w*|corpus)\b", re.I)


def section_for(title, abstract=""):
    """(section id, dataset flag) for a new paper."""
    for text in (title, abstract):
        for section, pat in RULES:
            if pat.search(text or ""):
                return section, section not in ("datasets",) and bool(BENCHMARK.search(title))
    return "analysis", False
