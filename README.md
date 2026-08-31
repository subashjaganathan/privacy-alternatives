# Privacy Alternatives

Three self-contained web pages that present the [Awesome Privacy](https://github.com/Lissy93/awesome-privacy)
dataset — 389 privacy-respecting tools across 13 categories — grouped by the mainstream product each one
replaces. Same data, three interfaces:

| Page | What it is |
|------|------------|
| [`docs/index.html`](docs/index.html) | **Privacy Index** — the main build. Sidebar navigation, collapsible swap-outs, instant search, filters, saved picks, category charts and coverage gauges. |
| [`docs/atlas.html`](docs/atlas.html) | **Privacy Atlas** — the graphical build. Animated hero, ambient canvas field, command palette (`Ctrl`/`Cmd` + `K`), detail drawers, card and compact layouts. |
| [`docs/list.html`](docs/list.html) | **Private Alternatives** — the plain build. One column, system fonts, no motion, a search box and an open-source filter. |

Each page is a single HTML file with the data inlined and no runtime dependencies. Open one from disk, or
serve the `docs/` folder from any static host. Nothing is tracked, and no request leaves the page except the
Google Fonts stylesheet used by two of the three builds.

## Build

```bash
pip install pyyaml
python build.py            # build from the checked-in dataset
python build.py --refresh  # pull the latest upstream dataset first, then build
```

`build.py` reads `src/awesome-privacy.yml`, converts it to JSON (rendering the Markdown in each description),
and inlines it into the three templates in `src/`, writing the results to `docs/`. The footer of every page
carries the build date so you can tell how fresh a copy is.

```
src/awesome-privacy.yml   the dataset (CC0, from upstream)
src/*.tpl.html            one template per page; __DATA__ is the inlined dataset
build.py                  the generator
docs/                     build output — GitHub Pages serves this folder
```

## Features in the Index build

- Search across tool names, descriptions, categories, section names and the products being replaced
- Filters for open source, published audit, anonymous payment and mobile apps, which compose
- A–Z or source ordering, saved picks stored in `localStorage` (this browser only, never uploaded)
- Shareable links: every section and every tool has a stable anchor, with a copy control on hover
  (`#s-encrypted-email`, `#t-signal--encrypted-messaging`)
- Category coverage strip, ring gauges, per-section magnitude bars, sidebar scroll-spy
- Light and dark themes, keyboard focus states, `prefers-reduced-motion` support, and a print stylesheet
  that expands every section and prints link targets

## Credits and licence

The listings are from [Awesome Privacy](https://github.com/Lissy93/awesome-privacy) by
[Alicia Sykes](https://aliciasykes.com), licensed **CC0-1.0**. The dataset file in `src/` is a copy of that
work; refresh it with `python build.py --refresh`.

The templates, generator and interface code in this repository are licensed **MIT** — see [LICENSE](LICENSE).

Being listed is not an endorsement. Check each project's own documentation, audits and threat model before
you switch.
