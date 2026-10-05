# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development

No build step. Open `index.html` directly in a browser or serve with any static server:

```bash
npx serve .
# or
python3 -m http.server 8080
```

Tailwind CSS and Manrope font load via CDN — no npm install required.

## Architecture

Single-page static marketing site for **Integra Moda** (PLM↔ERP integration platform by Setbox).

- `index.html` — home, structured as sequential sections; `integracoes.html`, `faq.html` and `privacidade.html` (privacy policy, LGPD) are the other pages
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
- `assets/` — brand SVG/PNG (`icon.svg`, `logo-simbolo*`, `logo-horizontal*`, `safari-pinned-tab.svg`, `setbox-lockup-escuro.svg`), partner logos
- `assets/brand/` — brand source and generators, not served
- `assets/screenshots/` — product screenshots

Rules to keep:

- Never duplicate an icon in two places. One file, one path, referenced from wherever it is needed. This repo already shipped a broken manifest once by keeping copies in both root and `assets/favicon/`.
- Icons are **generated, never hand-edited**: run `python3 assets/brand/gen_icons.py`. Editing a PNG by hand is lost on the next run.
- Moving an icon means updating three places: the `<head>` of every page, `site.webmanifest` and `browserconfig.xml`.
- Adding a page means copying the full `<head>` icon block from an existing page — the block is identical across every page.
- After touching any path, serve locally and confirm every reference returns 200.

## Design System

**Color tokens in use:**

| Token | Value | Use |
|---|---|---|
| bg | `#FAFAFA` | Page background |
| text | `#111111` | Primary text |
| muted | `#555555–#888888` | Secondary text |
| accent | `#AF0914` | Setbox red 30p: CTAs, bullets, labels, links, active nav item |
| accent-hover | `#8C0710` | Hover state for red buttons |
| brand | `#FB0D1C` | Logo, icons, card hover border. Never small text or button fill |
| accent-dark | `#E10C19` | Button on the grafite home hero |
| dark | `#111111` | Home hero and footer background |
| border | `#E5E5E5` | Section dividers, card borders |

Colors, font and components follow the Setbox brand guide (`~/obsidian/setbox/marca/identidade-visual.md`) since 2026-10-05: Integra Moda is a Setbox product, endorsed brand. No shadows; button radius 6, card radius 12. Inner pages use the sticky light nav. On the home the nav is fixed and glass over the grafite hero, turning solid `#FAFAFA` on scroll (same script as setbox.com.br). The home hero is grafite (`#111111`) and fills the first screen on desktop (`lg:min-h-[100svh]`): text on the left, the app screenshot on the right in 3D perspective (`lg:[perspective:1800px]`, `rotateY(-16deg) rotateX(6deg) rotateZ(-2deg)`, 230% of its column wide, `lg:-mb-48` so it bleeds past the bottom, cropped by the section's `overflow-hidden` on the right and bottom); below `lg` the screenshot stacks under the text, flat. Hero button `#E10C19`, hover `#AF0914`. "Um produto Setbox" with `setbox-lockup-escuro.svg` closes the hero text.

Nav links: Como funciona, Integrações, Preços, FAQ, then Entrar and the CTA. ERPs is not in the nav: it is a section of the home, reached from the footer. Footer columns: Produto, Clientes (Entrar na plataforma, Suporte), Empresa (Setbox, Contato, Política de privacidade). Below `md` the nav links collapse into a hamburger menu (`#nav-toggle` / `#nav-menu`, same markup as setbox.com.br); on the home, opening it forces the nav solid. No link to a page that does not exist (no `href="#"`).

**Typography:** Manrope (Google Fonts). Heading weights 700–800, body 400–500. `tracking-tight` on large headings.

**Layout:** `max-w-5xl` container, `px-8` horizontal padding. Two-column `grid grid-cols-2 gap-16` for feature sections.

## Content Conventions

- Language: Brazilian Portuguese
- Before changing any public text, read `~/obsidian/setbox/produtos/integramoda/decisoes-de-discurso-comercial.md` and `glossario-e-fronteiras.md`. Never publish hours, setup price, price tiers, or field-level mapping detail.
- Never use em dash (—). Use hyphen (-) or comma instead.
- All CTAs point to `mailto:contato@setbox.com.br`
- Partner logos use `.logo-partner` class (grayscale → color on hover)
- Status badges: `text-[#16794A] bg-[#E3F4EA]` for "Disponível"/"Sucesso", `text-[#AF0914] bg-[#FEE7E8]` for "Falha", `text-blue-700 bg-blue-50` for "Em breve"
- Section labels: `text-[11px] text-[#AF0914] font-semibold tracking-wide uppercase`
