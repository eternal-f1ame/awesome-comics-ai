# Contributing

Thank you for helping keep this map current. Additions, corrections and new sections are all welcome.

## Scope

A paper belongs here when comics are its subject or its main test bed. "Comics" is meant broadly: manga, manhwa, manhua, webtoons, bandes dessinées, comic strips, graphic novels and single-panel cartoons. Work on anime or general illustration fits better in [AwesomeAnimeResearch](https://github.com/SerialLain3170/AwesomeAnimeResearch), and work on story visualization goes in the adjacent section only when it targets comic-like output.

It must also meet the [inclusion rule](README.md#inclusion-rule): an A\* or A venue by CORE, a workshop or a peer-reviewed track of such a conference, a dataset or benchmark paper at any published venue (mark a benchmark outside the Datasets section with `dataset: true`), or an arXiv preprint at most four months old. `python scripts/verify.py` checks this. If your venue is missing from `data/venues.yaml`, add it there with its CORE rank and a link to the CORE entry in the pull request.

## Add or fix an entry

1. Edit `data/papers.yaml`. Each entry looks like this:

   ```yaml
   - title: "The Amazing Mysteries of the Gutter: Drawing Inferences Between Panels in Comic Book Narratives"
     authors: Mohit Iyyer et al.   # the first author, then "et al." when there are more
     year: 2017
     venue: CVPR                   # the published venue, or arXiv
     category: vlm                 # a section id from data/sections.yaml
     paper: https://doi.org/10.1109/cvpr.2017.686   # the DOI of the published version, if there is one
     arxiv: "1611.05118"           # optional
     code: https://github.com/miyyer/comics         # optional
     # project: https://...        # optional, a project page
   ```

   For a preprint, set `venue: arXiv` and add `date:` with the day of its first arXiv version (YYYY-MM-DD). The monthly refresh replaces it with the published version when one appears, or retires it after four months.

   Use the published venue and year when the paper has one, and `arXiv` otherwise. Copy the title exactly as the paper prints it.

2. Run `pip install pyyaml`, then `python scripts/verify.py --online` and `python scripts/build.py`. The first checks the entry, and the second writes `README.md` and the site data.

3. Open a pull request with the three changed files. The check on the pull request runs the same two scripts.

## Report a problem

Open an issue for a wrong link, a wrong venue, a missing paper or a section that should exist. A link to the paper is enough.
