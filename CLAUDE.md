# Snow and Climate Group — Marianne Cowherd's lab website

Single static page, plain HTML/CSS, no build step. Same design as `../Website`
(imalsky.github.io). **Local only for now — do NOT push or add a remote unless
explicitly asked.** When it eventually deploys, the repo would be named
`mariannecowherd.github.io` under her GitHub account.

This is a LAB GROUP site for a professor, not a personal postdoc page. The group is
branded **"Cowherd Inc."** (her choice — use it in the nav, hero, title, and footer).
Section order is Research → Group → Teaching → Publications → News. The Group section
has a "Current members" label (PI entry with her VERBATIM three-paragraph bio from her
old site's /group/ page — don't paraphrase it) and a short "Prospective students" note.
When students join the lab, add them as `.member` entries (name, role line, short bio)
under "Current members".

## Identity constants (use these, don't re-derive)

| What | Value |
|---|---|
| Email | marianne.cowherd@montana.edu |
| ORCID | 0000-0002-3165-4504 |
| Google Scholar user | RN_5PCcAAAAJ |
| Semantic Scholar author ID | 1379599255 |
| GitHub | mariannecowherd |
| Position | Assistant Professor, Dept. of Earth Sciences, Montana State University (2025–present); leads the Snow and Climate Group |
| Affiliations | Central Sierra Snow Laboratory (2022–); Lawrence Berkeley National Laboratory (2023–) |
| Education | PhD UC Berkeley ESPM 2025 (DOE CSGF fellow); M.S. 2020 + B.S. 2019 Stanford |

## Updating the site (the common task)

Run the checker first — it compares live publication data against what's on the page:

```
python3 scripts/check_updates.py
```

It prints current metrics (citations, h-index) and any DOIs found in Semantic
Scholar / Crossref / ORCID that are missing from `index.html`. Then:

1. **Verify** each candidate DOI resolves: `curl -sI https://doi.org/<doi>` → expect 302.
   Skip conference abstracts (EGU/AGU), datasets, and joke preprints (arXiv:2104.00147
   is an April Fools paper — never list it).
2. **Add** real papers to `#publications`: one `<li class="pub">` per paper — year,
   linked title (DOI url), author line (`Cowherd, M.` bolded via `<strong>`). ONE merged
   list, newest first — do NOT split first-author vs co-authored (her preference).
3. **News**: new first-author papers, major press, and position changes also get a
   one-line dated entry at the TOP of `#news`. Prune anything stale or broken.
4. A major new first-author paper can also become a research card (see below).

### Citation metrics (h-index etc.)

Metrics are deliberately NOT shown on the page (they live in the CV; strong academic
sites link out instead). To fetch current numbers when asked:

- Semantic Scholar (reliable, no key):
  `curl -s "https://api.semanticscholar.org/graph/v1/author/1379599255?fields=citationCount,hIndex,paperCount"`
- Google Scholar (higher counts; page often blocks bots — use WebFetch on
  `https://scholar.google.com/citations?user=RN_5PCcAAAAJ` and quote the source)
- Crossref works list: `https://api.crossref.org/works?filter=orcid:0000-0002-3165-4504&rows=100`
- ORCID works: `https://pub.orcid.org/v3.0/0000-0002-3165-4504/works` (Accept: application/json)

Reference values, 2026-07-01: Scholar 291 citations / h-index 6; Semantic Scholar 218 / 5.
(Scholar always reads higher — it counts preprints and grey literature.)

## Research cards

Each card in `#research` = figure + eyebrow (venue · year) + linked title + a one-to-two
sentence blurb that states the FINDING (not the method), in her voice.

Getting figures (publisher sites often bot-wall direct downloads):
1. Best source: her own GitHub repos — most papers have a repo with a `figures/` dir
   (`caldor-snow`, `snow_drought`, `wus-snow-drought`, `resilient-snowpack-estimation`,
   `efml`). Fetch via `https://raw.githubusercontent.com/mariannecowherd/<repo>/main/figures/<file>`.
2. Open-access PDFs: Nature journals allow direct `.pdf` curl; AMS/BAMS too. IOP and
   Wiley block curl AND headless Chrome — for those use Unpaywall
   (`https://api.unpaywall.org/v2/<doi>?email=<any email>`), DOE OSTI
   (`https://www.osti.gov/api/v1/records?doi=<doi>` — works when a coauthor is at a DOE lab),
   or the Stanford EFML page (`https://web.stanford.edu/~fringer/publications.html`) for
   her estuary papers.
3. Extract: `pdftoppm -png -r 110 -f <page> -l <page> paper.pdf out`, crop the figure
   region with PIL, auto-trim white borders, save JPG quality 86, max width 1400 px,
   into `images/research/<slug>.jpg`.

## Voice / style rules (from her own writing)

- First person, short declarative sentences, no hype. One plain-English opener
  ("I study climate science and the cryosphere.") before any technical register.
- Her framing word is **nonstationarity** — change in snow and water systems, "both the
  problems this causes and the potential solutions."
- Blurbs state findings; concrete places (Caldor Fire, Sierra Nevada, South San
  Francisco Bay) over abstractions. Em dashes sparingly (she writes `--`).
- Section headings stay plain: Research / Group / Teaching / Publications / News.
- Group voice is "we"; PI-specific facts (education, quotes, profiles) say
  "Dr. Cowherd". Teaching entries are list rows (term column · course · venue).

## Files

```
index.html                     # the whole site (hero, research, group, teaching, publications, news, footer)
assets/css/style.css           # all styling (shared design + .news/.trio additions at the bottom)
images/headshot.jpg            # 800×800 center crop; source is headshot2026.local.jpeg (gitignored)
images/research/*.jpg          # figure thumbnails, one per research card
files/Marianne_Cowherd_CV.pdf  # from https://mariannecowherd.github.io/files/marianne_cv_public.pdf
scripts/check_updates.py       # stdlib-only; compares page DOIs vs live APIs, prints metrics
```

## Preview locally

```
python3 -m http.server 8766
```
then open http://localhost:8766. Verify with a headless-Chrome screenshot before
declaring done; note old headless clamps viewport width to 500 px minimum, so mobile
"overflow" at 390 px is usually an artifact.
