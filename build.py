#!/usr/bin/env python3
"""Build the three privacy-alternatives pages from the Awesome Privacy dataset.

  python build.py            # build from the checked-in src/awesome-privacy.yml
  python build.py --refresh  # re-download the dataset first, then build

Each page is one self-contained HTML file in docs/ with the data inlined,
so it works from the filesystem, from GitHub Pages (which serves the docs/ folder), or any static host.
"""

import argparse
import base64
import hashlib
import html
import json
import os
import re
import sys
import urllib.request
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "docs")
DATA_FILE = os.path.join(SRC, "awesome-privacy.yml")
UPSTREAM = "https://raw.githubusercontent.com/Lissy93/awesome-privacy/main/awesome-privacy.yml"

PAGES = [
    ("index.tpl.html", "index.html"),   # Privacy Index  - the main build
    ("atlas.tpl.html", "atlas.html"),   # Privacy Atlas  - the graphical build
    ("list.tpl.html", "list.html"),     # Private Alternatives - the plain build
]


def refresh():
    print("downloading " + UPSTREAM)
    with urllib.request.urlopen(UPSTREAM, timeout=60) as r:
        body = r.read()
    with open(DATA_FILE, "wb") as f:
        f.write(body)
    print("saved {} ({:,} bytes)".format(os.path.relpath(DATA_FILE, ROOT), len(body)))


ONES = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def words(n):
    """399 -> 'three hundred and ninety-nine' (British style, for the Index intro)."""
    if n < 20:
        return ONES[n] or "zero"
    if n < 100:
        return TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")
    if n < 1000:
        return ONES[n // 100] + " hundred" + (" and " + words(n % 100) if n % 100 else "")
    return "{:,}".format(n)


SCRIPT_RE = re.compile(r"<script(?P<attrs>[^>]*)>(?P<body>.*?)</script>", re.S)


def harden(page):
    """Give the page a proper document head and lock it down.

    Standards mode, a mobile viewport, no referrer sent to the listed sites, and a
    Content-Security-Policy that runs only this page's own inline script (by SHA-256)
    and loads nothing from any other origin. The JSON data block is never executed,
    so it needs no hash.
    """
    hashes = []
    for m in SCRIPT_RE.finditer(page):
        if "application/json" in m.group("attrs"):
            continue
        digest = hashlib.sha256(m.group("body").encode("utf-8")).digest()
        hashes.append("'sha256-{}'".format(base64.b64encode(digest).decode()))
    csp = ("default-src 'none'; script-src {}; style-src 'unsafe-inline'; font-src 'self'; "
           "img-src 'self' data:; base-uri 'none'; form-action 'none'").format(" ".join(hashes) or "'none'")
    return ('<!doctype html>\n<html lang="en">\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<meta name="referrer" content="no-referrer">\n'
            '<meta http-equiv="Content-Security-Policy" content="{}">\n'.format(csp) + page)


def md(t):
    """The dataset holds Markdown; render the inline subset we use."""
    if not t:
        return ""
    t = " ".join(str(t).split())
    t = html.escape(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
               r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w/])_([^_]+)_(?![\w])", r"<em>\1</em>", t)
    t = re.sub(r"&lt;br\s*/?&gt;", "<br>", t)
    return t


def mentions(v):
    """notableMentions is either prose or a list of {name,url,description}."""
    if not v:
        return {"text": "", "items": []}
    if isinstance(v, str):
        return {"text": md(v), "items": []}
    items = []
    for m in v:
        if isinstance(m, dict):
            items.append({"n": m.get("name", ""), "u": m.get("url", ""), "d": md(m.get("description"))})
        else:
            items.append({"n": str(m), "u": "", "d": ""})
    return {"text": "", "items": items}


def dataset():
    try:
        import yaml
    except ImportError:
        sys.exit("PyYAML is required:  pip install pyyaml")
    with open(DATA_FILE, encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    out = []
    for c in raw["categories"]:
        cat = {"name": c["name"], "sections": []}
        for s in c["sections"]:
            sec = {
                "name": s["name"],
                "alt": s.get("alternativeTo") or [],
                "intro": md(s.get("intro")),
                "warn": md(s.get("wordOfWarning")),
                "info": md(s.get("furtherInfo")),
                "mentions": mentions(s.get("notableMentions")),
                "services": [],
            }
            for x in (s.get("services") or []):
                repo = None
                if x.get("github"):
                    repo = ["GitHub", "https://github.com/" + x["github"]]
                elif x.get("codeberg"):
                    repo = ["Codeberg", "https://codeberg.org/" + x["codeberg"]]
                elif x.get("git"):
                    repo = ["Source", x["git"]]
                sec["services"].append({
                    "n": x["name"],
                    "u": x["url"],
                    "d": md(x.get("description")),
                    "f": x.get("followWith") or "",
                    "os": bool(x.get("openSource")),
                    "au": bool(x.get("securityAudited")),
                    "cr": bool(x.get("acceptsCrypto")),
                    "repo": repo,
                    "tos": x.get("tosdrId"),
                    "ios": x.get("iosApp") or "",
                    "and": x.get("androidApp") or "",
                })
            cat["sections"].append(sec)
        out.append(cat)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--refresh", action="store_true", help="re-download the dataset before building")
    args = ap.parse_args()

    if args.refresh:
        refresh()

    data = dataset()
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    if "</script>" in payload:  # would close the inline data block early
        payload = payload.replace("</script>", "<\\/script>")

    tools = sum(len(s["services"]) for c in data for s in c["sections"])
    sections = sum(len(c["sections"]) for c in data)
    stamp = date.today().isoformat()

    os.makedirs(OUT, exist_ok=True)
    for tpl_name, out_name in PAGES:
        with open(os.path.join(SRC, tpl_name), encoding="utf-8") as f:
            tpl = f.read()
        # counts first, so the inlined data can never be touched by a placeholder
        for key, value in (("__TOOLS_WORDS__", words(tools).capitalize()), ("__TOOLS__", str(tools)),
                           ("__SECTIONS__", str(sections)), ("__CATEGORIES__", str(len(data))),
                           ("__BUILT__", stamp)):
            tpl = tpl.replace(key, value)
        page = harden(tpl.replace("__DATA__", payload))
        path = os.path.join(OUT, out_name)
        with open(path, "w", encoding="utf-8", newline="\n") as f:  # same bytes on every OS
            f.write(page)
        print("wrote docs/{} ({:,} bytes)".format(out_name, os.path.getsize(path)))

    print("{} tools across {} sections in {} categories, built {}".format(
        tools, sections, len(data), stamp))


if __name__ == "__main__":
    main()
