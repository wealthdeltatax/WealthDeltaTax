"""
pages/corpus.py — generate the Papers index page (corpus.qmd).

Reads paper metadata and contents from the SiteConfig; writes one .qmd file.
Call generate_corpus_qmd(dest_path, cfg).
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from config import AUTHOR, SITE_URL, _format_date

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
# These appear in the corpus table but their links go nowhere (404 or redirect).
# They are rendered as plain text rather than hyperlinks.
_NO_PAGE: frozenset[str] = frozenset()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _yymmdd_to_display(raw: Any) -> str:
    """Convert YYMMDD → human-readable date string, e.g. '15 Aug 2026'."""
    iso = _format_date(raw)
    if not iso:
        return "—"
    try:
        dt = datetime.strptime(iso, "%Y-%m-%d")
        return dt.strftime("%-d %b %Y")
    except Exception:
        try:
            dt = datetime.strptime(iso, "%Y-%m-%d")
            return dt.strftime("%d %b %Y").lstrip("0")
        except Exception:
            return iso


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
        lines.append("| Paper | Title | Version | Updated | Status |")
        lines.append("|-------|-------|---------|---------|--------|")

        for sc in present:
            page   = link_map[sc]
            meta   = paper_meta.get(sc, {})
            title  = meta.get("title", sc).replace("The Wealth Delta Tax: ", "")
            ver    = meta.get("version", "—")
            date   = _yymmdd_to_display(meta.get("version_date"))
            status = meta.get("status", "—")
            status_label = _STATUS_LABEL.get(status, status)
            # Papers with no rendered page: plain text shortcode, no link
            if sc in _NO_PAGE:
                sc_cell = f"{sc} *(no page)*"
            else:
                sc_cell = f"[{sc}]({page})"
            lines.append(f"| {sc_cell} | {title} | v{ver} | {date} | {status_label} |")

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
        "See also the [Start Here](start-here.html) guide.",
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
