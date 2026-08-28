#!/usr/bin/env python3
"""Fetch NCRR's most recent publications from the OpenAlex API and
regenerate the publication list inside publications.html.

The live ncrr.au.dk publication feed (Pure) was unavailable when this demo
was built, so the list is sourced from OpenAlex
(https://openalex.org), searching raw affiliation strings for
"National Centre for Register-based Research" and sorting by publication
date, descending.

Usage:
    python3 tools/fetch_publications.py [N]     # N = number of pubs (default 200)

Replaces the HTML between <!-- BEGIN-PUBS --> and <!-- END-PUBS --> in
publications.html and writes the normalized data to
assets/data/publications.json.
"""

import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

AFFILIATION = '"National Centre for Register-based Research"'
API = "https://api.openalex.org/works"
CONTACT = "ncrr-demo-webpage/1.0 (mailto:bjarni.vilhjalmsson@gmail.com)"
ROOT = Path(__file__).resolve().parent.parent
PAGE_FILE = ROOT / "publications.html"
DATA_FILE = ROOT / "assets" / "data" / "publications.json"
MARK_BEGIN = "<!-- BEGIN-PUBS -->"
MARK_END = "<!-- END-PUBS -->"


def fetch(count):
    per_page = 100
    works = []
    for page in range(1, count // per_page + 1):
        url = "{}?filter=raw_affiliation_strings.search:{}&sort=publication_date:desc&per-page={}&page={}".format(
            API, urllib.parse.quote(AFFILIATION), per_page, page
        )
        req = urllib.request.Request(url, headers={"User-Agent": CONTACT})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.load(r)
        works.extend(data["results"])
        if len(data["results"]) < per_page:
            break
    return works[:count]


def initials(given_names):
    parts = re.split(r"[\s-]+", given_names.strip())
    return " ".join(p[0].upper() + "." for p in parts if p)


def format_authors(authorships, max_shown=6):
    names = []
    for a in authorships:
        display = a["author"]["display_name"] or ""
        tokens = display.split()
        if len(tokens) == 1:
            names.append(tokens[0])
        else:
            names.append("{}, {}".format(tokens[-1], initials(" ".join(tokens[:-1]))))
    if len(names) <= max_shown:
        return ", ".join(names[:-1]) + " & " + names[-1] if len(names) > 1 else (names[0] if names else "")
    return ", ".join(names[:max_shown]) + " et al."


def normalize(work):
    source = ((work.get("primary_location") or {}).get("source") or {})
    biblio = work.get("biblio") or {}
    vol = biblio.get("volume")
    issue = biblio.get("issue")
    first = biblio.get("first_page")
    last = biblio.get("last_page")
    venue = source.get("display_name") or ""
    ref = ""
    if vol:
        ref = "<em>{}</em>".format(vol)
        if issue:
            ref += "({})".format(issue)
        if first:
            ref += ", " + first + ("–" + last if last else "")
        ref += "."
    elif venue:
        ref = ""
    return {
        "year": work.get("publication_year"),
        "title": (work.get("title") or "").strip(),
        "authors": format_authors(work.get("authorships") or []),
        "venue": venue,
        "ref": ref,
        "doi": (work.get("doi") or "").replace("https://doi.org/", ""),
        "type": work.get("type") or "",
    }


def li(pub):
    venue = ". <em>{}</em>".format(pub["venue"]) if pub["venue"] else ""
    doi = (' <a href="https://doi.org/{0}" target="_blank" rel="noopener">doi:{0}</a>'.format(pub["doi"])) if pub["doi"] else ""
    year = '<span class="pub-year">{}</span>'.format(pub["year"]) if pub["year"] else ""
    return (
        '        <li data-filter-item>{}\n'
        '          <div class="pub-title">{}</div>\n'
        '          <div class="pub-meta">{} ({}){}{}{}</div>\n'
        '        </li>'
    ).format(year, pub["title"], pub["authors"], pub["year"], venue, (". " + pub["ref"]) if pub["ref"] else "", doi)


def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    works = fetch(count)
    pubs = [normalize(w) for w in works]
    pubs = [p for p in pubs if p["title"]]

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(pubs, indent=1, ensure_ascii=False))

    html = PAGE_FILE.read_text()
    if MARK_BEGIN not in html or MARK_END not in html:
        sys.exit("markers not found in publications.html")
    block = MARK_BEGIN + "\n" + "\n".join(li(p) for p in pubs) + "\n      " + MARK_END
    PAGE_FILE.write_text(
        html[: html.index(MARK_BEGIN)] + block + html[html.index(MARK_END) + len(MARK_END):]
    )
    print("wrote {} publications to {} and {}".format(len(pubs), PAGE_FILE.name, DATA_FILE))


if __name__ == "__main__":
    main()
