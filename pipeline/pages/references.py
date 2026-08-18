"""
pages/references.py — generate the External References bibliography page.

Reads external_references and citations from refs_data; writes references.qmd.
Call generate_references_qmd(dest_path, refs_data, link_map).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from config import AUTHOR, SITE_URL


# ── Helpers ───────────────────────────────────────────────────────────────────

def _ref_link(ref: dict[str, Any]) -> str | None:
    doi = ref.get("doi")
    url = ref.get("url")
    if doi:
        return f"https://doi.org/{doi}"
    return url or None


def _format_authors(authors: list[dict[str, str]]) -> str:
    if not authors:
        return "—"
    parts = []
    for a in authors:
        last  = a.get("last", "")
        first = a.get("first", "")
        parts.append(f"{last}, {first[0]}." if first else last)
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + " & " + parts[-1]


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


def _cited_in_labels(
    ref_id: str,
    citations: list[dict[str, Any]],
) -> list[str]:
    """Return sorted list of paper shortcodes that cite this reference."""
    return sorted({
        c["paper_id"]
        for c in citations
        if c["ref_id"] == ref_id
    })


# ── Generator ─────────────────────────────────────────────────────────────────

def generate_references_qmd(
    dest_path: Path,
    refs_data: dict[str, Any],
    link_map: dict[str, str],
) -> None:
    """Write references.qmd — flat alphabetical list of all external references."""
    external_refs: list[dict[str, Any]] = refs_data.get("external_references", [])
    citations: list[dict[str, Any]]     = refs_data.get("citations", [])

    def sort_key(r: dict[str, Any]) -> tuple[str, int]:
        authors    = r.get("authors", [])
        first_last = authors[0].get("last", "ZZZ") if authors else "ZZZ"
        return (first_last.lower(), r.get("year", 0))

    sorted_refs = sorted(external_refs, key=sort_key)

    lines: list[str] = [
        "---",
        'title: "External References"',
        'description: "Complete bibliography of external sources cited across'
        ' the Wealth Delta Tax research programme."',
        f'author: "{AUTHOR}"',
        "---",
        "",
        f"This page lists all {len(external_refs)} external sources cited across the "
        "Wealth Delta Tax research programme. Each entry shows which papers cite it. "
        "Links go to the DOI or publisher page where available.",
        "",
        "The full reference database including citation relationships is available as "
        "[machine-readable JSON](/references.json).",
        "",
        "---",
        "",
    ]

    for ref in sorted_refs:
        ref_id   = ref["id"]
        authors  = _format_authors(ref.get("authors", []))
        year     = ref.get("year", "—")
        title    = ref.get("title", "—")
        rtype    = _ref_type_label(ref.get("type"))
        link     = _ref_link(ref)
        verified = ref.get("verified", False)

        # Journal / publisher details
        details_parts: list[str] = []
        if ref.get("journal"):
            details_parts.append(f"*{ref['journal']}*")
            if ref.get("volume"):
                vol = ref["volume"]
                iss = ref.get("issue")
                details_parts.append(f"*{vol}*({iss})" if iss else f"*{vol}*")
            if ref.get("pages"):
                details_parts.append(ref["pages"])
        elif ref.get("publisher"):
            details_parts.append(ref["publisher"])
        if ref.get("series") and ref.get("number"):
            details_parts.append(f"{ref['series']} No. {ref['number']}")
        elif ref.get("series"):
            details_parts.append(ref["series"])
        details = ", ".join(details_parts) if details_parts else ""

        # Cited-in links
        cited_in = _cited_in_labels(ref_id, citations)
        if cited_in:
            cited_links = [
                f"[{sc}]({link_map[sc]})" if sc in link_map else sc
                for sc in cited_in
            ]
            cited_str = "Cited in: " + " · ".join(cited_links)
        else:
            cited_str = ""

        verified_badge = " ✓" if verified else ""
        title_md = f"[{title}]({link})" if link else title

        lines.append(f"**{authors} ({year}).** {title_md}{verified_badge}  ")
        if details:
            lines.append(f"{details}  ")
        lines.append(f"`{rtype}`")
        if cited_str:
            lines.append(f"<small>{cited_str}</small>")
        lines.append("")  # blank line between entries

    dest_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  ✓ Generated references.qmd ({len(sorted_refs)} entries)")
