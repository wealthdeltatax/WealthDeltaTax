"""
pages/references.py — generate the External References bibliography page.

Reads external_references and citations from refs_data; writes references.qmd.
Call generate_references_qmd(dest_path, refs_data, link_map).

Changes from v1:
  - Fix paper_id normalisation: abbreviated IDs (LRA, LRB, CORPA, GOVA, RATESA)
    are mapped to their dotted canonical forms before link_map lookup, so
    "cited in" links work correctly for all papers.
  - APA formatting by type: journal articles, books, book chapters, working
    papers, reports, institutional reports, preprints, misc each render
    correctly. Working papers show series + number (e.g. NBER WP 34512).
  - Institutional authors (first: None) render as bare last name without
    a trailing period.
  - Three pending-decision orphans (references_only only, flags 4/6/9) are
    filtered from the public page and noted in a comment in the output.
  - "Cited in" row uses canonical dotted shortcodes as link text.
  - Verified badge (✓) retained.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from config import AUTHOR, SITE_URL


# ── Paper ID normalisation ────────────────────────────────────────────────────
# Citation records in references.json use abbreviated paper_ids for dotted
# shortcodes (LR.A → LRA, CORP.A → CORPA, etc). link_map uses the dotted
# canonical forms. This map translates before lookup.

_ABBREV_TO_CANONICAL: dict[str, str] = {
    "LRA":     "LR.A",
    "LRB":     "LR.B",
    "CORPA":   "CORP.A",
    "GOVA":    "GOV.A",
    "GOVB":    "GOV.B",
    "RATESA":  "RATES.A",
    "SWEEPSA": "SWEEPS.A",
    "VALA":    "VAL.A",
    "VALB":    "VAL.B",
}

# Refs with only references_only citations, pending author decisions on
_PENDING_ORPHANS: frozenset[str] = frozenset({})

# ── Author formatting ─────────────────────────────────────────────────────────

def _format_authors(authors: list[dict[str, str]]) -> str:
    """
    APA 7th author format: Last, F. M., & Last, F. M.
    Institutional authors (first: None) render as bare name only.
    Handles up to 20 authors; truncates with ellipsis beyond that.
    """
    if not authors:
        return "—"

    parts: list[str] = []
    for a in authors:
        last  = a.get("last", "")
        first = a.get("first")
        if first:
            parts.append(f"{last}, {first}")
        else:
            # Institutional author — no initials, no trailing period
            parts.append(last)

    if len(parts) == 1:
        return parts[0]
    if len(parts) == 2:
        return f"{parts[0]}, & {parts[1]}"
    # 3–20: comma-separated, Oxford comma before &
    return ", ".join(parts[:-1]) + ", & " + parts[-1]


# ── Source details by type ────────────────────────────────────────────────────

def _format_source(ref: dict[str, Any]) -> str:
    """
    Return the source/venue string for a reference, formatted by type.
    Does not include the title (handled separately) or the DOI link.

    Examples by type:
      journal_article   → *Journal Name*, *17*(1), 402–430.
      book              → Publisher.
      book_chapter      → Publisher, pp. 110–144.
      working_paper     → NBER Working Paper No. 34512. / SSRN Working Paper No. 3452274.
      report            → Publisher. / Publisher (Series No. N).
      institutional_report → Publisher.
      preprint          → arXiv preprint.
      misc              → Publisher.
    """
    t = ref.get("type", "")

    if t == "journal_article":
        # Returns markdown with its own italic markers — caller must NOT re-wrap.
        parts: list[str] = []
        if ref.get("journal"):
            parts.append(f"*{ref['journal']}*")
        if ref.get("volume"):
            vol = str(ref["volume"])
            iss = ref.get("issue")
            parts.append(f"*{vol}*({iss})" if iss else f"*{vol}*")
        if ref.get("pages"):
            parts.append(str(ref["pages"]))
        return ", ".join(parts) + "." if parts else ""

    # All other types return plain text — caller wraps in italics.
    if t == "book":
        pub = ref.get("publisher", "")
        return f"{pub}." if pub else ""

    if t == "book_chapter":
        pub = ref.get("publisher", "")
        pages = ref.get("pages", "")
        if pub and pages:
            return f"{pub}, pp. {pages}."
        return f"{pub}." if pub else ""

    if t == "working_paper":
        series = ref.get("series", "")
        number = ref.get("number", "")
        publisher = ref.get("publisher", "")
        if series and number:
            institution = f"{publisher}. " if publisher else ""
            return f"{institution}{series} No. {number}."
        if series:
            return f"{series}."
        return f"{publisher}." if publisher else ""

    if t in ("report", "institutional_report"):
        pub = ref.get("publisher", "")
        series = ref.get("series", "")
        number = ref.get("number", "")
        if series and number:
            return f"{pub}. {series} No. {number}." if pub else f"{series} No. {number}."
        if series:
            return f"{pub}. {series}." if pub else f"{series}."
        return f"{pub}." if pub else ""

    if t == "preprint":
        series = ref.get("series", "")
        return f"{series}." if series else "Preprint."

    # misc and anything else
    pub = ref.get("publisher", "")
    return f"{pub}." if pub else ""


# ── Link helpers ──────────────────────────────────────────────────────────────

def _ref_link(ref: dict[str, Any]) -> str | None:
    doi = ref.get("doi")
    if doi:
        return f"https://doi.org/{doi}"
    return ref.get("url") or None


def _ref_type_label(ref_type: str | None) -> str:
    return {
        "journal_article":      "Article",
        "book":                 "Book",
        "book_chapter":         "Book chapter",
        "working_paper":        "Working paper",
        "report":               "Report",
        "institutional_report": "Institutional report",
        "preprint":             "Preprint",
        "misc":                 "Misc",
    }.get(ref_type or "", ref_type or "—")


# ── Cited-in helper ───────────────────────────────────────────────────────────

def _cited_in(
    ref_id: str,
    citations: list[dict[str, Any]],
    link_map: dict[str, str],
) -> list[tuple[str, str]]:
    """
    Return sorted list of (canonical_shortcode, page_url) pairs for papers
    that cite this reference in-text (relationship: in_text or implicit).

    Normalises abbreviated paper_ids (LRA → LR.A) before looking up link_map.
    """
    shortcodes: set[str] = set()
    for c in citations:
        if c["ref_id"] != ref_id:
            continue
        if c["relationship"] not in ("in_text", "implicit"):
            continue
        raw = c["paper_id"]
        canonical = _ABBREV_TO_CANONICAL.get(raw, raw)
        if canonical in link_map:
            shortcodes.add(canonical)

    return sorted(
        ((sc, link_map[sc]) for sc in shortcodes),
        key=lambda x: x[0],
    )


# ── Sort key ─────────────────────────────────────────────────────────────────

def _sort_key(ref: dict[str, Any]) -> tuple[str, int]:
    authors = ref.get("authors", [])
    first_last = authors[0].get("last", "ZZZ") if authors else "ZZZ"
    return (first_last.lower(), ref.get("year", 0))


# ── Generator ─────────────────────────────────────────────────────────────────

def generate_references_qmd(
    dest_path: Path,
    refs_data: dict[str, Any],
    link_map: dict[str, str],
) -> None:
    """
    Write references.qmd — alphabetical bibliography of all external references
    with type badges, DOI/URL links, and per-paper "cited in" links.

    Three pending-decision orphans (flags 04, 06, 09) are excluded until the
    author resolves whether they belong in the bibliography.
    """
    all_refs: list[dict[str, Any]] = refs_data.get("external_references", [])
    citations: list[dict[str, Any]] = refs_data.get("citations", [])

    # Exclude pending-decision orphans
    refs = [r for r in all_refs if r["id"] not in _PENDING_ORPHANS]
    excluded = [r for r in all_refs if r["id"] in _PENDING_ORPHANS]

    sorted_refs = sorted(refs, key=_sort_key)

    lines: list[str] = [
        "---",
        'title: "External References"',
        'description: "Complete bibliography of external sources cited across'
        " the Wealth Delta Tax research programme.\"",
        f'author: "{AUTHOR}"',
        "---",
        "",
        f"All {len(refs)} external sources cited across the Wealth Delta Tax "
        "research programme, listed alphabetically. "
        "Each entry links to its DOI or publisher page where available, "
        "and shows which papers in the series cite it.",
        "",
        "The full reference database including citation relationships and "
        "bibliographic flags is available as "
        "[machine-readable JSON](/references.json).",
        "",
        "---",
        "",
        '<div class="wdt-references">',
        "",
    ]

    for ref in sorted_refs:
        ref_id   = ref["id"]
        authors  = _format_authors(ref.get("authors", []))
        year     = ref.get("year", "—")
        title    = ref.get("title", "—")
        rtype    = _ref_type_label(ref.get("type"))
        source   = _format_source(ref)
        link     = _ref_link(ref)
        verified = ref.get("verified", False)

        title_md = f"[{title}]({link})" if link else title
        verified_badge = " <span class='wdt-ref-verified' title='Bibliographic details verified'>✓</span>" if verified else ""

        # Cited-in links
        cited_pairs = _cited_in(ref_id, citations, link_map)
        if cited_pairs:
            cited_links = [f"[{sc}]({url})" for sc, url in cited_pairs]
            cited_str = "Cited in: " + " · ".join(cited_links)
        else:
            cited_str = ""

        lines += [
            '<div class="wdt-ref-entry">',
            "",
            f"{authors} ({year}). {title_md}{verified_badge}",
            "",
        ]
        if source:
            # Journal articles: source already contains markdown italic markers.
            # All other types: wrap in italics.
            if ref.get("type") == "journal_article":
                lines += [source, ""]
            else:
                lines += [f"*{source}*", ""]
        lines += [
            f'<span class="wdt-ref-type">{rtype}</span>',
        ]
        if cited_str:
            lines += [
                f'<span class="wdt-ref-cited">{cited_str}</span>',
            ]
        lines += [
            "",
            "</div>",
            "",
        ]

    lines.append("</div>")

    # Note excluded entries for transparency
    if excluded:
        lines += [
            "",
            "---",
            "",
            ":::{.callout-note collapse='true'}",
            "## Entries pending author review",
            "",
            f"{len(excluded)} entries are held pending resolution of open "
            "bibliographic flags and are not shown above:",
            "",
        ]
        for r in sorted(excluded, key=_sort_key):
            flag_ids = ", ".join(r.get("flag_ids", []))
            lines.append(f"- **{r['id']}** ({r.get('year', '—')}) — {flag_ids}")
        lines += ["", ":::"]

    dest_path.write_text("\n".join(lines), encoding="utf-8")
    print(
        f"  ✓ Generated references.qmd "
        f"({len(refs)} entries, {len(excluded)} pending)"
    )
