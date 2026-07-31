#!/usr/bin/env python3
"""Check for new publications and current citation metrics for Marianne Cowherd.

Stdlib only. Compares DOIs already on index.html against Semantic Scholar,
Crossref, and ORCID, prints anything missing plus current metrics.

Usage:  python3 scripts/check_updates.py
"""

import json
import re
import ssl
import sys
import urllib.request
from pathlib import Path

ORCID = "0000-0002-3165-4504"
S2_AUTHOR = "1379599255"

# Items that are indexed but do not belong on the site (abstracts, joke preprints,
# pre-career work). Add DOIs here to silence them.
IGNORE_DOIS = {
    "10.59720/15-031",            # high-school JEI paper, not on her curated list
    "10.5194/egusphere-egu26-8134",  # EGU conference abstract
    "10.5194/epsc-dps2025-420",   # conference abstract
}
IGNORE_TITLE_WORDS = ("erratum", "correction to", "reply to", "atmospheric ghost")

ROOT = Path(__file__).resolve().parent.parent
CTX = ssl.create_default_context()


def fetch_json(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "cowherd-site-updater", **(headers or {})})
    with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
        return json.load(r)


def page_dois():
    html = (ROOT / "index.html").read_text()
    return {m.lower() for m in re.findall(r"doi\.org/(10\.[^\"'\s<>]+)", html)}


def s2_metrics_and_papers():
    author = fetch_json(
        f"https://api.semanticscholar.org/graph/v1/author/{S2_AUTHOR}"
        "?fields=name,citationCount,hIndex,paperCount"
    )
    papers = fetch_json(
        f"https://api.semanticscholar.org/graph/v1/author/{S2_AUTHOR}/papers"
        "?fields=title,year,venue,externalIds&limit=100"
    ).get("data", [])
    results = []
    for p in papers:
        doi = (p.get("externalIds") or {}).get("DOI")
        results.append((doi.lower() if doi else None, p.get("title", ""), p.get("year"), p.get("venue", "")))
    return author, results


def crossref_papers():
    data = fetch_json(f"https://api.crossref.org/works?filter=orcid:{ORCID}&rows=100")
    out = []
    for it in data.get("message", {}).get("items", []):
        title = (it.get("title") or [""])[0]
        year = (it.get("issued", {}).get("date-parts") or [[None]])[0][0]
        venue = (it.get("container-title") or [""])[0]
        out.append((it.get("DOI", "").lower(), title, year, venue))
    return out


def orcid_papers():
    data = fetch_json(f"https://pub.orcid.org/v3.0/{ORCID}/works", headers={"Accept": "application/json"})
    out = []
    for g in data.get("group", []):
        summary = g.get("work-summary", [{}])[0]
        title = summary.get("title", {}).get("title", {}).get("value", "")
        year = (summary.get("publication-date") or {}).get("year", {}) or {}
        year = year.get("value")
        doi = None
        for eid in (g.get("external-ids", {}) or {}).get("external-id", []):
            if eid.get("external-id-type") == "doi":
                doi = eid.get("external-id-value", "").lower()
        out.append((doi, title, year, ""))
    return out


def main():
    on_page = page_dois()
    print(f"DOIs currently on index.html: {len(on_page)}")

    try:
        author, s2 = s2_metrics_and_papers()
        print(
            f"\nSemantic Scholar metrics: {author.get('citationCount')} citations, "
            f"h-index {author.get('hIndex')}, {author.get('paperCount')} papers"
        )
        print("Google Scholar (higher counts, fetch manually): "
              "https://scholar.google.com/citations?user=RN_5PCcAAAAJ")
    except Exception as e:  # noqa: BLE001
        print(f"\nSemantic Scholar unavailable: {e}")
        s2 = []

    sources = [("Semantic Scholar", s2)]
    for name, fn in (("Crossref", crossref_papers), ("ORCID", orcid_papers)):
        try:
            sources.append((name, fn()))
        except Exception as e:  # noqa: BLE001
            print(f"{name} unavailable: {e}")

    seen, missing = set(), []
    for source, papers in sources:
        for doi, title, year, venue in papers:
            if not doi or doi in on_page or doi in IGNORE_DOIS or doi in seen:
                continue
            if any(w in title.lower() for w in IGNORE_TITLE_WORDS):
                continue
            seen.add(doi)
            missing.append((year, doi, title, venue, source))

    if missing:
        print(f"\n{len(missing)} indexed paper(s) NOT on the page — verify before adding:")
        for year, doi, title, venue, source in sorted(missing, key=lambda x: str(x[0] or ""), reverse=True):
            print(f"  [{year}] {title[:80]}")
            print(f"         {venue}  ·  https://doi.org/{doi}  ({source})")
        print("\nVerify each with: curl -sI https://doi.org/<doi>  (expect HTTP 302).")
        print("Skip conference abstracts and datasets; see CLAUDE.md for placement rules.")
    else:
        print("\nNo missing papers found — the page is up to date.")


if __name__ == "__main__":
    sys.exit(main())
