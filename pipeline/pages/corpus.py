"""
pages/corpus.py — generate the Papers index page (corpus.qmd).

Reads paper metadata and contents from the SiteConfig; writes one .qmd file.
Call generate_corpus_qmd(dest_path, cfg).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from config import AUTHOR, SITE_URL

# ── Section ordering for the index table ─────────────────────────────────────

SECTION_ORDER: list[tuple[str, list[str]]] = [
    ("Core Papers",              ["WP", "MF"]),
    ("Literature",               ["LR.A", "LR.B", "JUR"]),
    ("Valuation",                ["VAL", "VAL.A", "VAL.B"]),
    ("Corporate & Governance",   ["CORP", "CORP.A", "GOV", "GOV.A", "GOV.B"]),
    ("Revenue & Behaviour",      ["RATES", "RATES.A", "SWEEPS", "SWEEPS.A", "BEHAV"]),
    ("Implementation",           ["CLOSE", "PHASE1"]),
    ("Analysis",                 ["POL", "ENV", "FM", "MOD"]),
    ("Reference",                ["SCOPE", "ADD"]),
]

_STATUS_LABEL: dict[str, str] = {
    "active":     "✓ Active",
    "superseded": "↩ Superseded",
    "draft":      "⚙ Draft",
}

# Shortcodes that have no rendered paper page on the site.
_NO_PAGE: frozenset[str] = frozenset()


# ── Table rendering ──────────────────────────────────────────────────────────
# Emit raw HTML tables so column widths are enforced via <col style="width:X%">.
# Pandoc sizes markdown tables independently per-table from content width, so
# no markdown approach (padding, tbl-colwidths) produces uniform columns across
# separate tables. Raw HTML is the only reliable mechanism.
#
# Column percentages (must sum to 100):
#   Paper 10%, Title 48%, Version 8%, Updated 11%, Words 7%, Status 16%

_COL_WIDTHS = [10, 48, 8, 11, 7, 16]   # percentages, must sum to 100
_COL_HEADERS = ["Paper", "Title", "Version", "Updated", "Words", "Status"]
_COL_ALIGN   = ["left", "left", "left", "left", "right", "left"]


def _html_table(rows: list[tuple[str, ...]]) -> str:
    """Return a raw HTML table with fixed column widths and an HTML passthrough fence."""
    col_tags = "".join(
        f'    <col style="width:{w}%">\n'
        for w in _COL_WIDTHS
    )
    header_cells = "".join(
        f"      <th>{h}</th>\n" for h in _COL_HEADERS
    )
    body_rows = ""
    for row in rows:
        cells = ""
        for cell, align in zip(row, _COL_ALIGN):
            style = f' style="text-align:{align}"' if align != "left" else ""
            cells += f"      <td{style}>{cell}</td>\n"
        body_rows += f"    <tr>\n{cells}    </tr>\n"

    html = (
        '<table style="width:100%; table-layout:fixed; border-collapse:collapse">\n'
        f"{col_tags}"
        "  <thead>\n"
        f"    <tr>\n{header_cells}    </tr>\n"
        "  </thead>\n"
        "  <tbody>\n"
        f"{body_rows}"
        "  </tbody>\n"
        "</table>"
    )
    return f"```{{=html}}\n{html}\n```"


# ── Generator ─────────────────────────────────────────────────────────────────

def generate_corpus_qmd(
    dest_path: Path,
    link_map: dict[str, str],
    paper_meta: dict[str, Any],
) -> None:
    """Write corpus.qmd to dest_path."""
    lines: list[str] = []

    lines += [
        "---",
        'title: "Papers"',
        'description: "Complete index of the Wealth Delta Tax research programme'
        " — all papers with version history and relationships.\"",
        f'author: "{AUTHOR}"',
        "---",
        "",
        "This page is the authoritative index of the Wealth Delta Tax research programme. "
        "The HTML versions of these papers, as published at this site, are the current "
        "authoritative versions. Version numbers and dates are updated on each revision.",
        "",
        f"The programme currently comprises **{len(paper_meta)} working papers**.",
        "",
    ]

    # Collection-level JSON-LD
    collection_ld: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Collection",
        "name": "The Wealth Delta Tax Research Programme",
        "url": SITE_URL,
        "author": {"@type": "Person", "name": AUTHOR},
        "hasPart": [
            {
                "@type": "ScholarlyArticle",
                "name": meta.get("title", sc),
                "url": f"{SITE_URL}/{link_map.get(sc, f'{sc.lower()}.html')}",
                "version": meta.get("version", ""),
            }
            for sc, meta in paper_meta.items()
        ],
    }
    ld_json = json.dumps(collection_ld, indent=2, ensure_ascii=False)
    lines += ["```{=html}", f"<script type=\"application/ld+json\">\n{ld_json}\n</script>", "```", ""]

    # Per-section tables
    for section_name, shortcodes in SECTION_ORDER:
        present = [s for s in shortcodes if s in link_map]
        if not present:
            continue

        lines.append(f"## {section_name}")
        lines.append("")

        table_rows = []
        for sc in present:
            page   = link_map[sc]
            meta   = paper_meta.get(sc, {})
            title  = meta.get("title", sc).replace("The Wealth Delta Tax: ", "")
            ver    = meta.get("version", "—")
            date         = meta.get("version_date_display", "—")
            status       = meta.get("status", "—")
            status_label = _STATUS_LABEL.get(status, status)
            wc           = meta.get("word_count", 0)
            words        = f"{wc:,}" if wc else "—"

            if sc in _NO_PAGE:
                sc_cell = f"{sc} <em>(no page)</em>"
            else:
                sc_cell = f'<a href="{page}">{sc}</a>'
            table_rows.append((sc_cell, title, f"v{ver}", date, words, status_label))

        lines.append(_html_table(table_rows))
        lines.append("")

    lines += [
        "---",
        "",
        "## Reading dependencies",
        "",
        "Most papers assume familiarity with the [White Paper (WP)](wp.html). "
        "The valuation appendices (VAL.A), (VAL.B) assume familiarity with (VAL). "
        "The governance appendices (GOV.A), (GOV.B) assume familiarity with (GOV). "
        "The rates appendix (RATES.A) assumes familiarity with (RATES).",
        "",
        "For first-time readers, the recommended sequence is: "
        "[WP](wp.html) → [MF](mf.html) → [VAL](val.html) → "
        "[GOV](gov.html) → [RATES](rates.html). "
        "See also the [Welcome](index.l) guide.",
        "",
        "---",
        "",
        "## About this index",
        "",
        "This page is generated automatically from the project reference database "
        "at each site build. The HTML papers at this site are the authoritative "
        "current versions; PDF versions archived at Zenodo may lag by one or more revisions.",
    ]

    dest_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  ✓ Generated corpus.qmd ({len(paper_meta)} papers)")