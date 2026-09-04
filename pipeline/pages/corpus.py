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


# ── Table column widths ───────────────────────────────────────────────────────
# Fixed character widths so all sections render with uniform column proportions.
# Title width is set to the longest paper title:
#   "Parameter Sweeps and Governing Council Calibration — Appendix" (61 chars)
# Paper width covers the longest markdown link: [SWEEPS.A](sweeps_a.html) etc.
# Right-align Words (numeric); left-align everything else.

_COL: dict[str, int] = {
    "Paper":   10,
    "Title":   61,
    "Version":  9,
    "Updated": 13,
    "Words":    7,
    "Status":  14,
}

_TABLE_HEADER = (
    "| "
    + " | ".join(f"{k:{w}}" for k, w in _COL.items())
    + " |"
)
# Words column is right-aligned; all others left-aligned.
_TABLE_SEP = (
    "| "
    + " | ".join(
        ("-" * (w - 1) + ":" if k == "Words" else "-" * w)
        for k, w in _COL.items()
    )
    + " |"
)


def _row(*cells: str) -> str:
    """Format one table row with fixed-width padding per column."""
    widths = list(_COL.values())
    padded = [
        cell.ljust(w) if len(cell) <= w else cell
        for cell, w in zip(cells, widths)
    ]
    return "| " + " | ".join(padded) + " |"


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
        lines.append(_TABLE_HEADER)
        lines.append(_TABLE_SEP)

        for sc in present:
            page   = link_map[sc]
            meta   = paper_meta.get(sc, {})
            title  = meta.get("title", sc).replace("The Wealth Delta Tax: ", "")
            ver    = meta.get("version", "—")
            # Use pre-formatted display date from extraction; fall back gracefully
            date         = meta.get("version_date_display", "—")
            status       = meta.get("status", "—")
            status_label = _STATUS_LABEL.get(status, status)
            wc           = meta.get("word_count", 0)
            words        = f"{wc:,}" if wc else "—"

            sc_cell = f"{sc} *(no page)*" if sc in _NO_PAGE else f"[{sc}]({page})"
            lines.append(_row(sc_cell, title, f"v{ver}", date, words, status_label))

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