"""Every page links site.css and site.js with a version taken from the file's content, so a browser that holds an older copy
(GitHub Pages lets it keep one for ten minutes) fetches the new one as soon as the page changes."""
import hashlib, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import build  # noqa: E402

PAGE = '<link rel="stylesheet" href="assets/site.css">\n<script src="assets/site.js" defer></script>\n'


def test_a_page_gets_the_version_of_each_file():
    out = build.stamp_assets(PAGE, {"site.css": "aaaa1111", "site.js": "bbbb2222"})
    assert 'href="assets/site.css?v=aaaa1111"' in out
    assert 'src="assets/site.js?v=bbbb2222"' in out


def test_an_old_version_is_replaced_not_added_to():
    old = build.stamp_assets(PAGE, {"site.css": "aaaa1111", "site.js": "bbbb2222"})
    out = build.stamp_assets(old, {"site.css": "cccc3333", "site.js": "bbbb2222"})
    assert 'href="assets/site.css?v=cccc3333"' in out
    assert "aaaa1111" not in out and out.count("?v=") == 2


def test_every_published_page_carries_the_current_versions():
    versions = build.asset_versions()
    for f in ("site.css", "site.js"):
        assert versions[f] == hashlib.sha256((ROOT / "docs" / "assets" / f).read_bytes()).hexdigest()[:10]
    for page in sorted((ROOT / "docs").glob("*.html")):
        text = page.read_text(encoding="utf-8")
        for f, v in versions.items():
            for link in re.findall(r'assets/%s(?:\?v=[0-9a-f]+)?"' % re.escape(f), text):
                assert link == f'assets/{f}?v={v}"', f"{page.name} links {link}"
