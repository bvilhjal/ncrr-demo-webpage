# NCRR demo webpage

Static demo webpage for NCRR. Plain HTML/CSS/JS — no build step, no
dependencies.

## Layout

```
index.html            main page (About / Demo / Contact sections)
assets/css/style.css  all styling
assets/js/main.js     small scripts (footer year, smooth scrolling)
```

All visible text is placeholder content.

## Run locally

Open `index.html` directly in a browser, or serve the directory:

```sh
python3 -m http.server 8000
```

then visit http://127.0.0.1:8000.

## Deploy

It is a fully static site: copy the files to any static host (GitHub Pages,
university web server, etc.). No build or environment setup is required.

## Editing notes

- Colors and spacing are defined once as CSS variables at the top of
  `assets/css/style.css`.
- The page is responsive; check narrow widths after layout changes.
