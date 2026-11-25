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
# Resolved relative to this file's location (website/build/).
SCRIPT_DIR = Path(__file__).resolve().parent   # wdt-site/pipeline/
ROOT_DIR   = SCRIPT_DIR.parent.parent          # repository root

SITE_DIR        = ROOT_DIR / "website" / "site"
SOURCE_DIR      = ROOT_DIR / "papers" / "legacy"
BUILD_DIR       = ROOT_DIR / "_build"
DIAGRAMS_DIR    = SITE_DIR / "diagrams"

CONTENTS_YML    = ROOT_DIR / "website" / "registry" / "contents.yml"
ANCHORS_YML     = ROOT_DIR / "website" / "registry" / "anchors.yml"
REFERENCES_JSON = ROOT_DIR / "registry" / "references.json"
REGISTRY_YML    = ROOT_DIR / "website" / "registry" / "papers.yml"   # legacy source for the 33 papers (zenodo, pdf, scrape); retires at cutover
PAGES_YML       = ROOT_DIR / "website" / "registry" / "pages.yml"    # the page list the site build reads

# ── Site-wide constants ───────────────────────────────────────────────────────
SITE_URL     = "https://wealthdeltatax.org"
AUTHOR       = "K. Ogata"
AFFILIATION  = "Independent Researcher"
DISCLOSURE   = (
    "### Author Disclosure\n\n"
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

# Step 1: match the entire revision history block (heading + all pipe rows).
# This scopes extraction to the right table before we look at individual rows,
# preventing _REVHISTORY_ROW_RE from matching rows in later tables and causing
# all_rows[-1] to return the last row of the last table in the document.
_REVHISTORY_BLOCK_RE = re.compile(
    r"###\s+Revision\s+History[^\n]*\n"  # heading line (any trailing text)
    r"(?:[^\n]*\n)*?"                    # optional blank / caption lines (non-greedy)
    r"((?:\|[^\n]*\n)+)",                # capture group: all consecutive pipe rows
    re.IGNORECASE,
)

# Step 2: within the captured block, match data rows (not separator rows like |---|).
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

_YAML_FENCE_RE = re.compile(r"^---\s*\n(.*?)^---\s*\n", re.DOTALL | re.MULTILINE)


# Matches lettered appendix headings: # A, ## A.1, # B … (standalone appendix papers)
_LETTERED_HEADING_RE = re.compile(
    r"^#{1,6}\s+[A-Z][\s.]",
    re.MULTILINE,
)


def _count_words_body_sections(body: str) -> int:
    """
    Count words from the first content heading to the end of the body.

    For regular papers: starts at the first numbered heading (# 1, ## 1.1 …).
    For standalone appendix papers (no numbered sections): starts at the first
    lettered heading (# A, ## A.1 …).

    Excludes: YAML front matter, Abstract, Glossary, and any unnumbered
              preamble before the first heading.

    Side effect: papers with an internal appendix (e.g. WP) will have those
    words included in the total.  This is acceptable — the count covers all
    substantive authored content.
    """
    first_num = _NUMBERED_HEADING_RE.search(body)
    if first_num:
        return len(body[first_num.start():].split())

    # Standalone appendix paper — no numbered sections at all
    first_letter = _LETTERED_HEADING_RE.search(body)
    if first_letter:
        return len(body[first_letter.start():].split())

    return 0


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

    # JEL codes — strip inline comments (e.g. "H24   # Personal income…")
    raw_jel = fm.get("jel", []) or []
    jel: list[str] = []
    for entry in raw_jel:
        code = str(entry).split("#")[0].strip()
        if code:
            jel.append(code)

    # ── Extract version and date from revision history table ──────────────
    body = text[fm_match.end():]

    # Scope to the revision history block first, then extract rows from within
    # it.  Without this, findall over the full body returns rows from every
    # pipe table in the document, and [-1] picks the last row of the last
    # table rather than the last revision entry.
    revhist_block_match = _REVHISTORY_BLOCK_RE.search(body)
    block = revhist_block_match.group(1) if revhist_block_match else body
    all_rows = _REVHISTORY_ROW_RE.findall(block)

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

    # ── Word count (numbered + appendix sections) ────────────────────────
    word_count = _count_words_body_sections(body)

    # ── Citation keys used in this paper ─────────────────────────────────
    # Matches @CiteKey in the body (pandoc/Quarto citation syntax).
    # Captures the bare key; ignores @wdt- internal cross-references.
    cite_keys: list[str] = sorted(set(re.findall(r'@([A-Za-z][A-Za-z0-9_:\-]*)', body)))

    return {
        "shortcode":            shortcode,
        "title":                title,
        "status":               status,
        "keywords":             keywords,
        "jel":                  jel,
        "version":              version,
        "version_date":         version_date,         # ISO or None
        "version_date_display": version_date_display, # human-readable
        "word_count":           word_count,
        "zenodo_doi":           fm.get("zenodo_doi", ""),
        "cite_keys":            cite_keys,
    }


# ── Page registry (website/registry/pages.yml) ────────────────────────────────────────
# One row per page.  Fields: id, type, title, url, source, status, parent,
# aliases, label, order  (website/notes/site/ids.md rule 7, site.md section 2).

PAGE_TYPES    = {"hub", "spoke", "appendix", "standalone", "legacy",
                 "pending", "calculator", "site"}
PAGE_STATUSES = {"draft", "author-review", "accepted", "legacy"}
# Spoke-kind rows take title and status from their own front matter (site.md R4).
SPOKE_KINDS   = {"spoke", "appendix"}
# A page is live at its URL today when its status is one of these; a draft is
# never published over a live URL (site.md Q1).
LIVE_STATUSES = {"legacy", "accepted"}
# Types built from a paper in source/ by the per-paper pipeline today.
PAPER_TYPES   = {"legacy", "standalone"}


def load_pages(path: Path | None = None) -> list[dict[str, Any]]:
    """Read pages.yml; every row gets all ten fields (None, or [] for aliases)."""
    path = path or PAGES_YML
    with path.open(encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or []
    rows: list[dict[str, Any]] = []
    for r in raw:
        row = {k: None for k in ("id", "type", "title", "url", "source",
                                 "status", "parent", "label", "order")}
        row["aliases"] = []
        row.update(r)
        row["aliases"] = row["aliases"] or []
        rows.append(row)
    return rows


def _norm_url(u: str) -> str:
    return "/" + u.lstrip("/")


def validate_pages(rows: list[dict[str, Any]]) -> list[str]:
    """Return a list of error strings (empty when the registry is valid)."""
    errors: list[str] = []
    ids: dict[str, dict[str, Any]] = {}
    for r in rows:
        rid = r.get("id")
        if not rid:
            errors.append(f"row without id: {r}")
            continue
        if rid in ids:
            errors.append(f"{rid}: duplicate id")
        ids[rid] = r

    orders: dict[int, str] = {}
    for rid, r in ids.items():
        if r["type"] not in PAGE_TYPES:
            errors.append(f"{rid}: unknown type {r['type']!r}")
        if not r["url"]:
            errors.append(f"{rid}: no url")
        elif not str(r["url"]).startswith("/"):
            errors.append(f"{rid}: url must start with '/': {r['url']}")
        if r["type"] in SPOKE_KINDS:
            for f in ("title", "status"):
                if r[f] is not None:
                    errors.append(f"{rid}: a {r['type']} row must not set {f} (it comes from front matter)")
        else:
            if not r["title"]:
                errors.append(f"{rid}: no title")
            if r["status"] not in PAGE_STATUSES:
                errors.append(f"{rid}: status {r['status']!r} not in {sorted(PAGE_STATUSES)}")
        if r["type"] == "appendix":
            parent = ids.get(r["parent"])
            if parent is None:
                errors.append(f"{rid}: parent {r['parent']!r} does not exist")
            elif parent["type"] != "spoke" or parent["order"] is None:
                errors.append(f"{rid}: parent {r['parent']} must be a menu spoke")
        elif r["parent"] is not None:
            if r["parent"] not in ids:
                errors.append(f"{rid}: parent {r['parent']!r} does not exist")
            else:
                errors.append(f"{rid}: only an appendix row has a parent")
        if r["order"] is not None:
            if r["type"] != "spoke":
                errors.append(f"{rid}: only a menu spoke has order")
            if not r["label"]:
                errors.append(f"{rid}: order without label")
            if r["order"] in orders:
                errors.append(f"{rid}: order {r['order']} also used by {orders[r['order']]}")
            orders[r["order"]] = rid
        elif r["label"] is not None:
            errors.append(f"{rid}: label without order")
    return errors


def find_url_collisions(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Report every URL (a row's url or one of its aliases) claimed by two or more rows.

    Each item: {"url", "ids", "live": [ids with a live status], "held": [other ids]}.
    A held row is never published over the live one; two live rows on one URL is a
    real conflict (`live` has more than one id).
    """
    claims: dict[str, list[str]] = {}
    for r in rows:
        urls = {_norm_url(r["url"])} | {_norm_url(a) for a in r["aliases"]} if r["url"] else set()
        for u in sorted(urls):
            claims.setdefault(u, []).append(r["id"])
    by_id = {r["id"]: r for r in rows}
    out = []
    for url, ids in sorted(claims.items()):
        if len(ids) < 2:
            continue
        live = [i for i in ids if by_id[i]["status"] in LIVE_STATUSES]
        out.append({"url": url, "ids": ids, "live": live,
                    "held": [i for i in ids if i not in live]})
    return out


def paper_registry(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    """
    Source-to-output entries for the per-paper pipeline, in the shape papers.yml has:
    [{"source": "<file in papers/legacy/>", "output": "<stem>.qmd"}].
    Only live paper rows (legacy and standalone papers) are built; a held row
    that collides with a live URL is never in the list.
    """
    held = {i for c in find_url_collisions(rows) for i in c["held"]}
    entries = []
    for r in rows:
        if (r["type"] in PAPER_TYPES and r["status"] in LIVE_STATUSES
                and r["id"] not in held
                and r["source"] and r["source"].startswith("papers/legacy/")):
            entries.append({
                "source": r["source"][len("papers/legacy/"):],
                "output": Path(r["url"]).stem + ".qmd",
            })
    return entries


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