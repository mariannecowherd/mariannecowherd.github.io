# Snow and Climate Group — lab website (Marianne Cowherd, Montana State University)

A single static page — plain HTML/CSS, no build step, no framework. Body type is
[Open Sans](https://fonts.google.com/specimen/Open+Sans), headings are
[Source Serif 4](https://fonts.google.com/specimen/Source+Serif+4), icons are
[Font Awesome Free](https://fontawesome.com/) 5.15.4. Same design as imalsky.github.io.

**Local only** — no GitHub remote yet. See `CLAUDE.md` for the full maintenance guide
(how to pull new papers, citation metrics, figure extraction, style rules).

## Structure
```
index.html                     # the whole site (hero, research, group, teaching, publications, news, footer)
assets/css/style.css           # all styling
images/headshot.jpg            # web-sized headshot (800×800, displays as a circle)
images/research/*.jpg          # figure thumbnails for the research cards
files/Marianne_Cowherd_CV.pdf  # CV linked from the nav and buttons
scripts/check_updates.py       # finds new papers + current metrics (stdlib only)
```

## Preview locally
```
python3 -m http.server 8766
```
then open http://localhost:8766

## Check for new papers / metrics
```
python3 scripts/check_updates.py
```
