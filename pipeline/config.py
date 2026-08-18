"""
config.py — site constants and registry loading.

Call load() once in main(); pass the returned SiteConfig to every function
that needs it.  No side-effects on import.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

# ── Path constants ────────────────────────────────────────────────────────────
# Resolved relative to this file's location (pipeline/).
SCRIPT_DIR = Path(__file__).resolve().parent   # wdt-site/pipeline/
ROOT_DIR   = SCRIPT_DIR.parent                 # wdt-site/

SITE_DIR        = ROOT_DIR / "site"
SOURCE_DIR      = ROOT_DIR / "source"
BUILD_DIR       = ROOT_DIR / "_build"
DIAGRAMS_DIR    = SITE_DIR / "diagrams"

CONTENTS_YML    = ROOT_DIR / "registry" / "contents.yml"
ANCHORS_YML     = ROOT_DIR / "registry" / "anchors.yml"
REFERENCES_JSON = ROOT_DIR / "registry" / "references.json"
REGISTRY_YML    = ROOT_DIR / "registry" / "papers.yml"

# ── Site-wide constants ───────────────────────────────────────────────────────
SITE_URL = "https://wealthdeltatax.org"
AUTHOR   = "K. Ogata"


# ── Config object ─────────────────────────────────────────────────────────────

@dataclass
class SiteConfig:
    """All registry data loaded from disk, plus the derived link_map."""

    # contents[SHORTCODE] = {page, title, sections}
    contents: dict[str, Any]

    # link_map[SHORTCODE] = "page.html"
    link_map: dict[str, str]

    # anchor_map["WP§3.5"] = "wp.html#the-symmetric-loss-refund-mechanism"
    anchor_map: dict[str, str]

    # paper_meta[SHORTCODE] = internal-paper record from references.json
    paper_meta: dict[str, Any]

    # full parsed references.json (needed by references.qmd and site-index)
    refs_data: dict[str, Any]


def load() -> SiteConfig:
    """
    Read the three registry files and return a SiteConfig.
    Raises FileNotFoundError if contents.yml or anchors.yml is missing.
    references.json is optional — an empty structure is used if absent.
    """
    if not CONTENTS_YML.exists():
        raise FileNotFoundError(f"contents.yml not found at {CONTENTS_YML}")

    with CONTENTS_YML.open(encoding="utf-8") as fh:
        contents: dict[str, Any] = yaml.safe_load(fh)

    link_map: dict[str, str] = {
        shortcode: paper["page"]
        for shortcode, paper in contents.items()
    }

    with ANCHORS_YML.open(encoding="utf-8") as fh:
        anchor_map: dict[str, str] = yaml.safe_load(fh)

    paper_meta: dict[str, Any] = {}
    refs_data: dict[str, Any] = {}

    if REFERENCES_JSON.exists():
        with REFERENCES_JSON.open(encoding="utf-8") as fh:
            refs_data = json.load(fh)
        for p in refs_data.get("internal_papers", []):
            paper_meta[p["shortcode"]] = p
        print(f"Loaded metadata for {len(paper_meta)} papers from {REFERENCES_JSON}")
    else:
        print(f"  ! {REFERENCES_JSON} not found — skipping metadata injection")

    return SiteConfig(
        contents=contents,
        link_map=link_map,
        anchor_map=anchor_map,
        paper_meta=paper_meta,
        refs_data=refs_data,
    )
