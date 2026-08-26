"""
transforms.py — per-paper text processing pipeline.

Each function is a pure(-ish) transform: text in, text out.
process_file() applies all five steps in order and writes the result.

Steps:
  1. strip_latex        — remove LaTeX spacing/layout commands
  2. convert_crossrefs  — (PAPER §X.Y) / PAPER §X.Y  →  markdown hyperlink
  3. convert_internal_bibliography — [CODE] lines → styled ::: div
  4. inject_front_matter — enrich YAML front matter from paper_meta
  5. build_jsonld       — append JSON-LD ScholarlyArticle block
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

from config import AUTHOR, SITE_URL, _format_date


# ── 1. LaTeX artifact stripping ───────────────────────────────────────────────

_LATEX_PATTERNS = [
    r"\\newpage", r"\\medskip", r"\\bigskip", r"\\smallskip",
    r"\\tableofcontents", r"\s*\{\.appendix\}", r"\\maketitle",
    r"\\begin\{center\}", r"\\end\{center\}",
    r"\\noindent", r"\\clearpage",
    r"\\vspace\*?\{[^}]+\}", r"\\hspace\*?\{[^}]+\}",
    r"\\setcounter\{[^}]+\}\{[^}]+\}",
]

_LATEX_RE = re.compile("|".join(_LATEX_PATTERNS))


def strip_latex(text: str) -> str:
    return _LATEX_RE.sub("", text)


# ── 2. Cross-reference conversion ─────────────────────────────────────────────

_CROSSREF_RE = re.compile(
    r"\(([A-Z][A-Z0-9]*(?:\.[A-Z][A-Z0-9]*)?)(?:\s+§([\d.A-Za-z]+))?\)"
    r"|"
    r"\b([A-Z][A-Z0-9]*(?:\.[A-Z][A-Z0-9]*)?)\s+§([\d.A-Za-z]+)"
)


def convert_crossrefs(
    text: str,
    link_map: dict[str, str],
    anchor_map: dict[str, str],
) -> str:
    def replace(m: re.Match) -> str:
        shortcode = m.group(1) or m.group(3)
        section   = (m.group(2) or m.group(4) or "").rstrip(".")
        full      = m.group(0)

        if shortcode not in link_map:
            return full

        if section:
            key = f"{shortcode}§{section}"
            url = anchor_map.get(key)
            if url:
                return f"[{full}]({url})"
            print(f"  ⚠ section not in anchors.yml: {key}")
            return f"[{full}]({link_map[shortcode]})"

        return f"[{full}]({link_map[shortcode]})"

    return _CROSSREF_RE.sub(replace, text)


# ── 3. Internal bibliography conversion ───────────────────────────────────────

_INTBIB_LINE_RE = re.compile(
    r"^\[([A-Z][A-Z0-9]*(?:\.[A-Z][A-Z0-9]*)?)\]\s+(.+)$"
)


def convert_internal_bibliography(lines: list[str]) -> list[str]:
    result: list[str] = []
    in_block = False

    for line in lines:
        m = _INTBIB_LINE_RE.match(line.rstrip())
        if m:
            if not in_block:
                result.append("\n::: {.internal-bibliography}\n")
                in_block = True
            code, rest = m.group(1), m.group(2)
            result.append(f"**[{code}]** {rest}\n")
        else:
            if in_block:
                result.append(":::\n")
                in_block = False
            result.append(line)

    if in_block:
        result.append(":::\n")

    return result


# ── 4. Front matter injection ─────────────────────────────────────────────────

_YAML_FENCE_RE = re.compile(r"^---\s*\n(.*?)^---\s*\n", re.DOTALL | re.MULTILINE)

def inject_front_matter(
    text: str,
    shortcode: str,
    paper_meta: dict[str, Any],
) -> str:
    """Enrich or create YAML front matter with metadata from paper_meta."""
    meta = paper_meta.get(shortcode)
    if not meta:
        return text

    fm_match = _YAML_FENCE_RE.match(text)
    if fm_match:
        try:
            fm = yaml.safe_load(fm_match.group(1)) or {}
        except Exception:
            fm = {}
        body = text[fm_match.end():]
    else:
        fm = {}
        body = text

    if "description" not in fm:
        fm["description"] = meta.get("title", "")
    if "author" not in fm:
        fm["author"] = AUTHOR
    if "date" not in fm:
        iso = _format_date(meta.get("version_date"))
        if iso:
            fm["date"] = iso
    if "version" not in fm:
        fm["version"] = meta.get("version", "")
    if "keywords" not in fm:
        related = meta.get("outbound_internal", [])[:4]
        kws = ["Wealth Delta Tax", "WDT", shortcode] + related
        fm["keywords"] = ", ".join(kws)

    new_fm = yaml.dump(
        fm, default_flow_style=False, allow_unicode=True, sort_keys=False
    )
    return f"---\n{new_fm}---\n{body}"

def inject_under_construction(text: str, shortcode: str, paper_meta: dict) -> str:
    """Prepend an under-construction banner if paper version < 1.0."""
    meta = paper_meta.get(shortcode)
    if not meta:
        return text
    version = str(meta.get("version", "1.0"))
    if version.startswith("0."):
        banner = (
            '\n```{=html}\n'
            '<div class="wdt-under-construction">\n'
            '  🚧 &nbsp; THIS PAPER IS UNDER CONSTRUCTION &nbsp; 🚧\n'
            '</div>\n'
            '```\n\n'
        )
        # Insert after the YAML front matter block
        import re
        fm_end = re.search(r'^---\s*\n.*?^---\s*\n', text, re.DOTALL | re.MULTILINE)
        if fm_end:
            insert_pos = fm_end.end()
            return text[:insert_pos] + banner + text[insert_pos:]
    return text


# ── 5. JSON-LD injection ──────────────────────────────────────────────────────

def build_jsonld(
    shortcode: str,
    paper_meta: dict[str, Any],
    link_map: dict[str, str],
) -> str:
    """Return a Quarto raw HTML block containing JSON-LD for this paper."""
    meta = paper_meta.get(shortcode)
    if not meta:
        return ""

    page_html = link_map.get(shortcode, f"{shortcode.lower()}.html")
    url       = f"{SITE_URL}/{page_html}"
    title     = meta.get("title", shortcode)
    version   = meta.get("version", "")
    iso_date  = _format_date(meta.get("version_date")) or ""
    status    = meta.get("status", "active")

    related_codes = list(dict.fromkeys(
        meta.get("outbound_internal", []) + meta.get("inbound_internal", [])
    ))
    related_urls = [
        f"{SITE_URL}/{link_map[r]}"
        for r in related_codes
        if r in link_map
    ]

    ld: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "name": title,
        "author": {"@type": "Person", "name": AUTHOR},
        "url": url,
        "isPartOf": {
            "@type": "Book",
            "name": "The Wealth Delta Tax Research Programme",
            "url": SITE_URL,
        },
        "version": version,
        "creativeWorkStatus": status,
        "keywords": ["Wealth Delta Tax", "WDT", "wealth taxation", shortcode],
    }
    if iso_date:
        ld["dateModified"] = iso_date
    if related_urls:
        ld["relatedLink"] = related_urls

    ld_json = json.dumps(ld, indent=2, ensure_ascii=False)
    return (
        "\n```{=html}\n"
        f"<script type=\"application/ld+json\">\n{ld_json}\n</script>\n"
        "```\n"
    )


# ── Orchestrator ──────────────────────────────────────────────────────────────

def process_file(
    src_path: Path,
    dest_path: Path,
    shortcode: str,
    link_map: dict[str, str],
    anchor_map: dict[str, str],
    paper_meta: dict[str, Any],
) -> None:
    """Apply all five transforms to one source file and write the result."""
    text = src_path.read_text(encoding="utf-8")

    text  = strip_latex(text)
    text  = convert_crossrefs(text, link_map, anchor_map)
    lines = convert_internal_bibliography(text.splitlines(keepends=True))
    text  = "".join(lines)
    text  = inject_front_matter(text, shortcode, paper_meta)
    text = inject_under_construction(text, shortcode, paper_meta)
    text  = text.rstrip("\n") + "\n" + build_jsonld(shortcode, paper_meta, link_map)

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(text, encoding="utf-8")
    print(f"  ✓ {src_path.name} → {dest_path.name}")
