# NCRR demo webpage

Live demo: <https://bvilhjal.github.io/ncrr-demo-webpage/>

Demo redesign of the NCRR website (https://ncrr.au.dk/) for the National
Centre for Register-based Research, now at the Department of Public Health
(Institut for Folkesundhed), Aarhus University. Plain HTML/CSS/JS — no build
step, no dependencies.

## What changed vs. the live site

- Full visual redesign (AU-inspired navy/gold palette, hero, cards, accordions).
- Location updated: NCRR is now at Institut for Folkesundhed, Bartholins Allé 2,
  bygning 1260, 8000 Aarhus C — the old site's directions still describe the
  Fuglesangs Allé campus (buildings R2640–R2641). Photos of the new building
  are included (supplied for this demo; replace with official photos before
  going live).
- New "Featured research" section on the front page with news-style commentary
  on two recent papers.
- Dedicated staff page with live search/filter; registers page with filter.
- All content captured from the live site (about, research incl. major
  projects and all eight research themes, Danish register list, newest
  publications, staff directory, links). Register descriptions and the full
  publication list still link back to ncrr.au.dk.

## Layout

```
index.html            front page: hero, stats, featured research, projects
about.html            about the centre + milestones
research.html         overview, major projects, eight research themes
registers.html        Danish registers list (filterable)
publications.html     200 most recent publications (filterable, numbered)
staff.html            staff directory (filterable)
find-us.html          new address, directions, photos, map
links.html            external resources
assets/css/style.css  all styling
assets/js/main.js     footer year + list filters
assets/img/           building photos (supplied for the demo), campus photos,
                      icon sprite, QR code
tools/fetch_publications.py  regenerates the publication list from OpenAlex
assets/data/publications.json  normalized publication data
```

## Publication data

`publications.html` lists the 200 most recent NCRR publications, fetched from
the [OpenAlex](https://openalex.org) API (affiliation search, sorted by
publication date) because the live site's Pure feed was unavailable. To
refresh:

```sh
python3 tools/fetch_publications.py 200
```

## Image credits

- Bartholins Allé 2 photos: supplied for this demo; replace with official AU
  photography before going live.
- `campus-main-building.jpg`: Villy Fink Isaksen / Wikimedia Commons, CC BY-SA 4.0.
- `campus-lakes.jpg`: RhinoMind / Wikimedia Commons, CC BY-SA 4.0.
- Icons: hand-drawn feather-style SVG sprite (MIT-style, in-repo).

## Run locally

Open `index.html` directly in a browser, or serve the directory:

```sh
python3 -m http.server 8123
```

then visit http://127.0.0.1:8123.

## Deploy

Fully static: copy the files to any static host (GitHub Pages, university web
server, etc.). No build or environment setup is required.

## Editing notes

- Colors and spacing are defined once as CSS variables at the top of
  `assets/css/style.css`.
- The header/footer markup is duplicated on every page — change it in all
  eight files (or move to includes/templating if this grows beyond a demo).
- Staff building/room numbers from the old site were dropped: they refer to
  the old Fuglesangs Allé buildings and are being re-assigned after the move.
