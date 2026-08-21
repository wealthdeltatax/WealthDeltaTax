"""
pages/site_index.py — machine-readable static endpoints.

Generates the WDT navigation index plus a flat, searchable section index.

The public endpoint is:
    /site-index.json

The JSON keeps the existing navigation structure under ``papers`` and ``anchors``,
and adds ``search`` records consumed by right-panel-search.html.

Search records are built from the generated Quarto .qmd files in ``_build``.
This keeps the search index tied to exactly the text that is about to be rendered,
rather than maintaining a second copy of paper prose.
"""

from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import (
    ANCHORS_YML,
    REFERENCES_JSON,
    ROOT_DIR,
    SITE_URL,
)

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


_HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*$", re.MULTILINE)
_HTML_RE = re.compile(r"<[^>]+>")
_FENCE_RE = re.compile(r"^(```|~~~)", re.MULTILINE)


def _format_date(raw_date: Any) -> str | None:
    if not raw_date or len(str(raw_date)) != 6:
        return None
    s = str(raw_date)
    try:
        return f"20{s[0:2]}-{s[2:4]}-{s[4:6]}"
    except Exception:
        return None


def _normalise_heading(text: str) -> str:
    """Normalise a Markdown heading for comparison with contents.yml titles."""
    text = _HTML_RE.sub("", text)
    text = re.sub(r"\{#[-\w.]+\}\s*$", "", text)
    text = re.sub(r"^\s*(?:[0-9]+(?:\.[0-9]+)*|[A-Z])[\.\s]+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().casefold()


def _plain_text(text: str) -> str:
    """Turn Markdown-ish section content into compact searchable text."""
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = _HTML_RE.sub(" ", text)

    # Remove fenced code/diagram blocks; these are not useful search targets.
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"~~~.*?~~~", " ", text, flags=re.DOTALL)

    # Images and links: retain link text, discard URLs/markup.
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    # Markdown emphasis / blockquote / list markers.
    text = re.sub(r"[*_`~]", "", text)
    text = re.sub(r"^\s{0,3}(?:[-+*]|\d+\.)\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE)

    # Collapse whitespace.
    return re.sub(r"\s+", " ", text).strip()


def _extract_sections(markdown: str) -> dict[str, str]:
    """
    Extract body text keyed by normalised heading title.

    A section includes all nested subsections until the next heading of the same
    or higher level. This gives a useful full-text search corpus while preserving
    the section-level result destination.
    """
    matches = list(_HEADING_RE.finditer(markdown))
    out: dict[str, str] = {}

    for i, match in enumerate(matches):
        heading = match.group(2).strip()
        level = len(match.group(1))
        key = _normalise_heading(heading)

        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(markdown)

        # Include nested headings/content, but stop at the next heading at the
        # same or higher level.
        j = i + 1
        while j < len(matches):
            next_level = len(matches[j].group(1))
            if next_level <= level:
                end = matches[j].start()
                break
            j += 1

        body = _plain_text(markdown[start:end])
        if key:
            if key in out and body:
                out[key] = f"{out[key]} {body}".strip()
            else:
                out[key] = body

    return out


def _load_search_text(build: Path, page: str) -> dict[str, str]:
    """
    Read the generated .qmd corresponding to a rendered page.

    Example:
        wp.html -> _build/wp.qmd
        lr-a.html -> _build/lr-a.qmd

    Returning an empty mapping is deliberately non-fatal: navigation/search by
    title and section heading still works if a generated file is unavailable.
    """
    qmd = build / Path(page).with_suffix(".qmd").name
    if not qmd.exists():
        return {}

    try:
        return _extract_sections(qmd.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"  ! Could not read {qmd.name} for search indexing: {exc}")
        return {}


def _build_search_records(
    build: Path,
    contents: dict[str, Any],
    anchor_map: dict[str, str],
    papers_out: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build the flat search corpus consumed by the right-hand search widget."""
    records: list[dict[str, Any]] = []

    for paper in papers_out:
        shortcode = paper["shortcode"]
        page = Path(paper["url"]).name
        section_text = _load_search_text(build, page)

        # Paper-level record: useful for title searches and papers with sparse
        # section metadata.
        records.append({
            "kind": "paper",
            "shortcode": shortcode,
            "title": paper["title"],
            "section": "",
            "text": paper["title"],
            "href": paper["url"],
        })

        contents_entry = contents.get(shortcode, {})
        for section in paper.get("sections", []):
            title = section["title"]
            text = section_text.get(_normalise_heading(title), "")

            records.append({
                "kind": "section",
                "shortcode": shortcode,
                "title": paper["title"],
                "section": title,
                "text": text,
                "href": section["url"],
            })

    return records


def generate_site_index(
    build: Path,
    refs_data: dict[str, Any],
    anchor_map: dict[str, str],
    contents: dict[str, Any],
    link_map: dict[str, str],
) -> None:
    """
    Write site-index.json to build/.

    Existing navigation fields are retained. A new flat ``search`` array is
    added for the right-panel search widget.
    """
    internal_papers = {
        p["shortcode"]: p
        for p in refs_data.get("internal_papers", [])
    }

    papers_out: list[dict[str, Any]] = []

    for shortcode, entry in contents.items():
        page = entry.get("page", f"{shortcode.lower()}.html")
        url = f"{SITE_URL}/{page}"
        meta = internal_papers.get(shortcode, {})

        sections: list[dict[str, Any]] = []
        for key, title in entry.get("sections", {}).items():
            anchor_key = f"{shortcode}§{key}"
            anchor = anchor_map.get(anchor_key, page)
            sections.append({
                "key": str(key),
                "title": title,
                "anchor": anchor,
                "url": f"{SITE_URL}/{anchor}",
            })

        papers_out.append({
            "shortcode": shortcode,
            "title": entry.get("title", meta.get("title", shortcode)),
            "url": url,
            "version": meta.get("version", ""),
            "version_date": _format_date(meta.get("version_date")) or "",
            "status": meta.get("status", "active"),
            "outbound_internal": meta.get("outbound_internal", []),
            "inbound_internal": meta.get("inbound_internal", []),
            "sections": sections,
        })

    search_records = _build_search_records(
        build, contents, anchor_map, papers_out
    )

    index = {
        "meta": {
            "generated": datetime.now(tz=timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "site": SITE_URL,
            "papers": len(papers_out),
            "anchors": len(anchor_map),
            "search_records": len(search_records),
            "description": (
                "Single-fetch navigation and search index for the Wealth Delta Tax "
                "research programme. Contains paper metadata, section hierarchy, "
                "resolved anchor URLs, and searchable section text. Generated by "
                "preprocess.py at each site build."
            ),
        },
        "papers": papers_out,
        "anchors": anchor_map,
        "search": search_records,
    }

    dest = build / "site-index.json"
    dest.write_text(
        json.dumps(index, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(
        f"  ✓ Generated site-index.json "
        f"({len(papers_out)} papers, {len(anchor_map)} anchors, "
        f"{len(search_records)} search records)"
    )


def copy_machine_readable_assets(
    build: Path,
    refs_data: dict[str, Any],
    anchor_map: dict[str, str],
    contents: dict[str, Any],
    link_map: dict[str, str],
) -> None:
    """
    Copy source-of-truth data files into _build/ as static endpoints,
    then generate site-index.json.

    Endpoints served:
      /references.json
      /anchors.yml
      /wdt-contents.yml
      /references.bib
      /site-index.json
    """
    assets = [
        (REFERENCES_JSON, build / "references.json"),
        (ROOT_DIR / "registry" / "anchors.yml", build / "anchors.yml"),
        (ROOT_DIR / "registry" / "contents.yml", build / "wdt-contents.yml"),
        (ROOT_DIR / "registry" / "references.bib", build / "references.bib"),
    ]

    for src, dst in assets:
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✓ {src.name} → {dst.name}")
        else:
            print(f"  ! {src.name} not found — skipping")

    generate_site_index(
        build,
        refs_data,
        anchor_map,
        contents,
        link_map,
    )
