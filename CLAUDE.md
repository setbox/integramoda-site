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
- `assets/` — partner and product logos (PNG/SVG)
- `DESIGN.md` — design reference (entire.io analysis used as visual inspiration)
- Screenshots referenced from `../docs/biblioteca/prints/` (outside this repo)

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
