# Privacy Alternatives

A browsable directory of **389 privacy-respecting tools**, grouped by the mainstream product each one
replaces — so instead of asking "what should I use?", you look up what you already use and see what stands
in for it. Gmail → Proton Mail, LastPass → Bitwarden, and 387 more, across 13 categories and 91 swap-outs.

**Live site:** https://subashjaganathan.github.io/privacy-alternatives/

## What it's for

- Finding a replacement for a specific app or service you want to move off
- Comparing the options in one category — password managers, VPNs, browsers, email, note apps — with the
  trade-offs and warnings the maintainers actually wrote down
- Checking what a tool declares before you install it: open source, an independent security audit,
  anonymous payment, mobile apps, and its terms-of-service rating
- Building your own shortlist and sharing a link to any tool or section with someone else

## Three ways to read it

| Page | Best for |
|------|----------|
| [Index](https://subashjaganathan.github.io/privacy-alternatives/) (`index.html`) | Everyday use. Sidebar navigation, collapsible swap-outs, instant search, filters, saved picks and coverage charts. |
| [Atlas](https://subashjaganathan.github.io/privacy-alternatives/atlas.html) (`atlas.html`) | Exploring. Card gallery, command palette, and a detail panel for each tool. |
| [Plain list](https://subashjaganathan.github.io/privacy-alternatives/list.html) (`list.html`) | Reading or printing. One column, no motion, everything on the page at once. |

## How to use it

**Search** — type in the box at the top. It matches tool names, descriptions, category names, section names
and the products being replaced, so `gmail`, `password`, and `finance` all work. Press `/` to jump to the
search box, `Esc` to clear it. In the Atlas, press `Ctrl`/`Cmd` + `K` for the command palette.

**Filter** — the chips narrow the list and combine: *Open source*, *Audited*, *Takes crypto*, *Mobile app*
and *Saved*. Counts update everywhere as you filter.

**Browse** — click a category in the sidebar, or a band in the coverage chart, to jump to it. Each swap-out
starts collapsed; click its header to open it. `A–Z` switches between alphabetical and the maintainers'
own ordering.

**Save** — the star on a listing keeps it in your shortlist. Saved picks live in your browser's local
storage only; they are never uploaded, and clearing site data clears them.

**Share** — hover a section or a tool and use *Link* / *Copy link* to copy a direct URL
(`…/index.html#s-encrypted-email`, `…/index.html#t-signal--encrypted-messaging`). Opening that URL scrolls
to the entry and expands it.

**Print** — printing the Index expands every section, drops the interface chrome, and prints each link's
destination next to it, so a paper copy stays usable.

Everything runs in the page. There is no account, no analytics and no tracking, and no network request
except the Google Fonts stylesheet used by two of the three pages.

## Run it yourself

Each page is a single self-contained HTML file — open one from disk, or copy the `docs/` folder to any
static host.

To rebuild from the dataset:

```bash
pip install pyyaml
python build.py            # build from the dataset in src/
python build.py --refresh  # download the latest dataset first, then build
```

`build.py` converts `src/awesome-privacy.yml` to JSON, renders the Markdown in each description, and inlines
the result into the templates in `src/`, writing `docs/index.html`, `docs/atlas.html` and `docs/list.html`.
The footer of every page shows the build date, so you can tell how current a copy is.

```
src/awesome-privacy.yml   the dataset
src/*.tpl.html            one template per page
build.py                  the generator
docs/                     build output — GitHub Pages serves this folder
```

## Licence

Code in this repository is released under the **MIT Licence** — see [LICENSE](LICENSE).

The listings come from [Awesome Privacy](https://github.com/Lissy93/awesome-privacy) by
[Alicia Sykes](https://aliciasykes.com), licensed **CC0-1.0**; `src/awesome-privacy.yml` is a copy of that
dataset.

Being listed is not an endorsement. Check each project's own documentation, audits and threat model before
you switch.
