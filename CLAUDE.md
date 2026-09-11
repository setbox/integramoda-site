# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development

No build step. Open `index.html` directly in a browser or serve with any static server:

```bash
npx serve .
# or
python3 -m http.server 8080
```

Tailwind CSS and Inter font load via CDN — no npm install required.

## Architecture

Single-page static marketing site for **Integra Moda** (PLM↔ERP integration platform by Setbox).

- `index.html` — entire site, one file, structured as sequential sections
- `assets/` — brand assets, partner and product logos (PNG/SVG)
- `assets/brand/` — brand source and generators (`gen_svg.py`, `gen_icons.py`), see `assets/brand/README.md`
- `DESIGN.md` — design reference (entire.io analysis used as visual inspiration)
- Screenshots referenced from `../docs/biblioteca/prints/` (outside this repo)

## Asset Placement Rules

Where a file lives is decided by **who asks for it**, not by what it is.

**Root is reserved** for files a browser or OS fetches at a fixed path without reading the HTML:

| File | Who asks for it |
|---|---|
| `favicon.ico` | Browser requests `/favicon.ico` blindly — feeds, error pages, tab before HTML parses |
| `apple-touch-icon.png` | iOS probes `/apple-touch-icon.png` at root when it finds no `<link>` |
| `browserconfig.xml` | Legacy Edge/IE requests `/browserconfig.xml` at root by default |
| `site.webmanifest` | Must be same-origin; root by convention |
| `og-image.png` | Stays at root because the URL is already in shared links — moving it breaks the preview on re-scrape |

**Everything else goes under `assets/`**, because it is reached through a declared path:

- `assets/favicon/` — PNG favicons, android-chrome icons, maskable icon, mstile
- `assets/` — brand SVG/PNG (`icon.svg`, `logo-simbolo*`, `logo-horizontal*`, `safari-pinned-tab.svg`), partner logos
- `assets/brand/` — brand source and generators, not served
- `assets/screenshots/` — product screenshots

Rules to keep:

- Never duplicate an icon in two places. One file, one path, referenced from wherever it is needed. This repo already shipped a broken manifest once by keeping copies in both root and `assets/favicon/`.
- Icons are **generated, never hand-edited**: run `python3 assets/brand/gen_icons.py`. Editing a PNG by hand is lost on the next run.
- Moving an icon means updating three places: the `<head>` of all three pages, `site.webmanifest` and `browserconfig.xml`.
- Adding a page means copying the full `<head>` icon block from an existing page — the block is identical across all three.
- After touching any path, serve locally and confirm every reference returns 200.

## Design System

**Color tokens in use:**

| Token | Value | Use |
|---|---|---|
| bg | `#FAFAFA` | Page background |
| text | `#111111` | Primary text |
| muted | `#555555–#888888` | Secondary text |
| accent | `#F97316` | Orange — CTAs, bullets, labels |
| accent-hover | `#EA580C` | Hover state for orange buttons |
| border | `#E5E5E5` | Section dividers, card borders |

**Typography:** Inter (Google Fonts). Heading weights 700–800, body 400–500. `tracking-tight` on large headings.

**Layout:** `max-w-5xl` container, `px-8` horizontal padding. Two-column `grid grid-cols-2 gap-16` for feature sections.

## Content Conventions

- Language: Brazilian Portuguese
- Never use em dash (—). Use hyphen (-) or comma instead.
- All CTAs point to `mailto:contato@integramoda.com.br`
- Partner logos use `.logo-partner` class (grayscale → color on hover)
- Status badges: `text-green-700 bg-green-100` for "Disponível", `text-blue-700 bg-blue-50` for "Em breve"
- Section labels: `text-[11px] text-[#F97316] font-semibold tracking-wide uppercase`
