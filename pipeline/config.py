"""
config.py — site constants and registry loading.

Call load() once in main(); pass the returned SiteConfig to every function
that needs it.  No side-effects on import.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

# ── Path constants ────────────────────────────────────────────────────────────
# Resolved relative to this file's location (pipeline/).
SCRIPT_DIR = Path(__file__).resolve().parent   # wdt-site/pipeline/
ROOT_DIR   = SCRIPT_DIR.parent                 # wdt-site/

SITE_DIR        = ROOT_DIR / "site"
TOOLS_DIR       = ROOT_DIR / "tools"
SOURCE_DIR      = ROOT_DIR / "source"
BUILD_DIR       = ROOT_DIR / "_build"
DIAGRAMS_DIR    = SITE_DIR / "diagrams"

CONTENTS_YML    = ROOT_DIR / "registry" / "contents.yml"
ANCHORS_YML     = ROOT_DIR / "registry" / "anchors.yml"
REFERENCES_JSON = ROOT_DIR / "registry" / "references.json"
REGISTRY_YML    = ROOT_DIR / "registry" / "papers.yml"

# ── Site-wide constants ───────────────────────────────────────────────────────
SITE_URL     = "https://wealthdeltatax.org"
AUTHOR       = "K. Ogata"
AFFILIATION  = "Independent Researcher"
DISCLOSURE   = (
    "### Author Disclosure {.unnumbered .unlisted}\n\n"
    "Portions of the drafting, editing, literature organisation, and structural "
    "review of this paper were assisted by publicly available large language models, "
    "including Anthropic's Claude and OpenAI's ChatGPT. These tools were used as aids "
    "to the author's research and writing process; the substantive arguments, analysis, "
    "interpretations, and conclusions are the author's own.\n\n"
    "This work received no external funding, sponsorship, or other financial support. "
    "The author is solely responsible for the content of the paper and for any errors "
    "that remain."
)


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

    # paper_meta[SHORTCODE] = extracted metadata record
    paper_meta: dict[str, Any]

    # full parsed references.json (needed by references.qmd and site-index)
    refs_data: dict[str, Any]


# ── Date helpers ──────────────────────────────────────────────────────────────

# Month names as they appear in revision history tables
_MONTH_MAP: dict[str, int] = {
    "january": 1,  "february": 2,  "march": 3,     "april": 4,
    "may": 5,      "june": 6,      "july": 7,       "august": 8,
    "september": 9,"october": 10,  "november": 11,  "december": 12,
    "jan": 1,      "feb": 2,       "mar": 3,        "apr": 4,
    "jun": 6,      "jul": 7,       "aug": 8,        "sep": 9,
    "oct": 10,     "nov": 11,      "dec": 12,
}

def parse_human_date(raw: str) -> str | None:
    """
    Convert a human-readable date string to ISO format (YYYY-MM-DD).

    Accepts:
        "15 August 2026"   → "2026-08-15"
        "1 Jan 2026"       → "2026-01-01"
        "31 May 2026"      → "2026-05-31"
    Returns None if the string cannot be parsed.
    """
    raw = raw.strip()
    m = re.match(r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})", raw)
    if not m:
        return None
    day, month_str, year = int(m.group(1)), m.group(2).lower(), int(m.group(3))
    month = _MONTH_MAP.get(month_str)
    if not month:
        return None
    try:
        return datetime(year, month, day).strftime("%Y-%m-%d")
    except ValueError:
        return None


def format_iso_date(iso: str) -> str | None:
    """
    Format an ISO date string (YYYY-MM-DD) for display, e.g. "15 Aug 2026".
    Returns None if parsing fails.
    """
    try:
        dt = datetime.strptime(iso, "%Y-%m-%d")
        return dt.strftime("%-d %b %Y")
    except Exception:
        try:
            dt = datetime.strptime(iso, "%Y-%m-%d")
            return dt.strftime("%d %b %Y").lstrip("0")
        except Exception:
            return None


def _format_date(raw_date: Any) -> str | None:
    """
    Legacy helper: convert YYMMDD int/str (e.g. 260815) → ISO date string.
    Retained for external bibliography processing in references.json.
    Do not use for internal paper metadata.
    """
    if not raw_date or len(str(raw_date)) != 6:
        return None
    s = str(raw_date)
    try:
        return f"20{s[0:2]}-{s[2:4]}-{s[4:6]}"
    except Exception:
        return None


# ── Paper metadata extraction ─────────────────────────────────────────────────

# Matches the last data row of the revision history table.
# Table format:  | 1.00  | 15 August 2026  | Published to website |
_REVHISTORY_ROW_RE = re.compile(
    r"^\|\s*([\d.]+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
    re.MULTILINE,
)

# Matches numbered section headings: # 1, ## 1.1, ### 1.1.1 etc.
# Excludes lettered appendix headings (A, A.1, B …) and unnumbered headings.
_NUMBERED_HEADING_RE = re.compile(
    r"^#{1,6}\s+\d+[\d.]*\s",
    re.MULTILINE,
)

# Matches any heading that starts with # (to detect appendix boundary A, B …)
_APPENDIX_HEADING_RE = re.compile(
    r"^#{1,6}\s+[A-Z][\s.]",
    re.MULTILINE,
)

_YAML_FENCE_RE = re.compile(r"^---\s*\n(.*?)^---\s*\n", re.DOTALL | re.MULTILINE)


def _count_words_numbered_sections(body: str) -> int:
    """
    Count words in numbered sections only (Introduction through Conclusion).

    Includes: heading text, body paragraphs, figure captions within those sections.
    Excludes: YAML front matter, Abstract, Glossary, unnumbered sections,
              lettered appendix sections (A, B, …) and everything after them.
    """
    # Find where the first numbered heading starts
    first_num = _NUMBERED_HEADING_RE.search(body)
    if not first_num:
        return 0

    text = body[first_num.start():]

    # Truncate at first lettered appendix heading if present
    first_app = _APPENDIX_HEADING_RE.search(text)
    if first_app:
        text = text[:first_app.start()]

    return len(text.split())


def extract_paper_meta(src_path: Path) -> dict[str, Any] | None:
    """
    Read a source .md file and extract all metadata needed by the pipeline.

    Returns a dict with keys:
        shortcode, title, status, keywords,
        version, version_date (ISO), version_date_display,
        word_count
    Returns None if the file cannot be parsed (missing YAML or shortcode).
    """
    try:
        text = src_path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"  ! Could not read {src_path.name}: {e}")
        return None

    # ── Parse YAML front matter ───────────────────────────────────────────
    fm_match = _YAML_FENCE_RE.match(text)
    if not fm_match:
        print(f"  ! {src_path.name}: no YAML front matter found")
        return None

    try:
        fm = yaml.safe_load(fm_match.group(1)) or {}
    except yaml.YAMLError as e:
        print(f"  ! {src_path.name}: YAML parse error: {e}")
        return None

    shortcode = fm.get("shortcode")
    if not shortcode:
        print(f"  ! {src_path.name}: no shortcode in front matter")
        return None

    title    = fm.get("title", shortcode)
    status   = fm.get("status", "draft")
    keywords = fm.get("keywords", [])
    if isinstance(keywords, str):
        # handle comma-separated string fallback
        keywords = [k.strip() for k in keywords.split(",")]

    # ── Extract version and date from revision history table ──────────────
    body = text[fm_match.end():]
    all_rows = _REVHISTORY_ROW_RE.findall(body)

    version              = "—"
    version_date         = None   # ISO string
    version_date_display = "—"

    if all_rows:
        last_row = all_rows[-1]
        version  = last_row[0].strip()
        raw_date = last_row[1].strip()
        iso      = parse_human_date(raw_date)
        if iso:
            version_date         = iso
            version_date_display = format_iso_date(iso) or raw_date
        else:
            print(f"  ! {src_path.name}: could not parse date '{raw_date}' in revision history")
            version_date_display = raw_date
    else:
        print(f"  ! {src_path.name}: no revision history rows found")

    # ── Word count (numbered sections only) ───────────────────────────────
    word_count = _count_words_numbered_sections(body)

    return {
        "shortcode":            shortcode,
        "title":                title,
        "status":               status,
        "keywords":             keywords,
        "version":              version,
        "version_date":         version_date,         # ISO or None
        "version_date_display": version_date_display, # human-readable
        "word_count":           word_count,
    }


# ── Registry loader ───────────────────────────────────────────────────────────

def load(paper_meta: dict[str, Any] | None = None) -> SiteConfig:
    """
    Read the registry files and return a SiteConfig.

    paper_meta should be passed in from preprocess.py after running
    extract_paper_meta() across all source files.  If omitted (e.g. in
    tests), an empty dict is used and a warning is printed.
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

    refs_data: dict[str, Any] = {}
    if REFERENCES_JSON.exists():
        with REFERENCES_JSON.open(encoding="utf-8") as fh:
            refs_data = json.load(fh)

    if paper_meta is None:
        print("  ! load() called without paper_meta — no internal paper metadata available")
        paper_meta = {}

    return SiteConfig(
        contents=contents,
        link_map=link_map,
        anchor_map=anchor_map,
        paper_meta=paper_meta,
        refs_data=refs_data,
    )
