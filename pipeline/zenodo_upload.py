"""
zenodo_upload.py — Bulk upload all WDT papers to Zenodo.

Reads metadata directly from source .md files via config.extract_paper_meta()
so titles, keywords, versions, and dates are always in sync with the pipeline.
Abstracts are extracted from the paper body (# Abstract section).
After a successful publish the script writes the real DOI back into the
source file's zenodo_doi: frontmatter field so the site pipeline picks it up.

Usage:
    python pipeline/zenodo_upload.py --sandbox                    # test run (safe)
    python pipeline/zenodo_upload.py --sandbox --dry-run          # validate only
    python pipeline/zenodo_upload.py --publish                    # live — permanent
    python pipeline/zenodo_upload.py --publish --only WP CORP CORP.A
    python pipeline/zenodo_upload.py --publish --update-metadata   # cross-link pass

Typical workflow:
    1. python zenodo_upload.py --sandbox --dry-run    # check all PDFs/metadata found
    2. python zenodo_upload.py --publish              # upload all papers
    3. python zenodo_upload.py --publish --update-metadata  # add cross-links + site URLs

Requirements:
    pip install requests pyyaml
    (yaml is already a pipeline dependency)

Token setup:
    Sandbox : https://sandbox.zenodo.org/account/settings/applications/
    Live    : https://zenodo.org/account/settings/applications/
    Scopes required: deposit:write  deposit:actions

    Set tokens below or via environment variables:
        ZENODO_SANDBOX_TOKEN  /  ZENODO_LIVE_TOKEN

Output:
    zenodo_dois.json  — written after every successful paper; maps
                        shortcode → DOI. Re-runs skip already-published
                        shortcodes automatically.
    zenodo_upload.log — append-only run log.

Metadata included per paper:
    - Title, abstract, keywords, version, publication date
    - JEL subject codes (from jel: frontmatter field)
    - Plain-text APA references (from references.bib + cite keys in body)
    - Related identifiers: site HTML URL + all sibling paper DOIs (--update-metadata)
    - Publisher: Wealth Delta Tax Research Programme
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import requests
import yaml

# ── Locate pipeline/ and project root ────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent   # pipeline/
sys.path.insert(0, str(SCRIPT_DIR))           # so we can import config

import config as cfg

# ── Token configuration ───────────────────────────────────────────────────────
SANDBOX_TOKEN = os.environ.get("ZENODO_SANDBOX_TOKEN", "0UxvCowgreWMq5mtcGSpsMzry9YaveZbs2eV0Yx4xASHIzoW0EZvGXfcjp0O")
LIVE_TOKEN    = os.environ.get("ZENODO_LIVE_TOKEN",    "CHANGE_ME_LIVE")

SANDBOX_BASE  = "https://sandbox.zenodo.org/api"
LIVE_BASE     = "https://zenodo.org/api"

# ── Shared metadata (same across all papers) ──────────────────────────────────
SHARED = {
    "upload_type":        "publication",
    "publication_type":   "workingpaper",
    "access_right":       "open",
    "license":            "cc-by-4.0",
    "language":           "eng",
    "imprint_publisher":  "Wealth Delta Tax Research Programme",
    "creators": [
        {
            "name":        "Ogata, K.",
            "affiliation": cfg.AFFILIATION,
        }
    ],
    # Uncomment once a Zenodo community is created:
    # "communities": [{"identifier": "wdt"}],
}

# ── PDF output directory ──────────────────────────────────────────────────────
# pdf.py writes to print/YYMMDD/. We find the most recent dated subfolder.
PRINT_DIR = cfg.ROOT_DIR / "print"


def _normalise(s: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace."""
    s = re.sub(r'[^\w\s]', '', s).lower()
    return re.sub(r'\s+', ' ', s).strip()


def _find_pdf(shortcode: str, pdf_dir: Path, paper_meta: dict[str, Any] | None = None) -> Path | None:
    """
    Locate the PDF for a given shortcode in a dated print/ subfolder.

    pdf.py names files:
        The Wealth Delta Tax - {Group} - {Short Title}.pdf
    Appendix companions include "Appendix" in their short title, so their PDF
    stem ends with the appendix keyword, e.g.:
        "The Wealth Delta Tax - Mechanism and Valuation - Valuing Wealth.pdf"
        "The Wealth Delta Tax - Mechanism and Valuation - Valuing Wealth Mathematical and Simulation Appendix.pdf"

    Title normalisation (lowercased, punctuation stripped) is shared between
    this function and pdf.py's _pdf_filename(), so em-dashes and colons in
    paper titles do not cause mismatches.

    Matching strategy:
      1. Exact normalised-title match on the third segment of the PDF stem
         (everything after "The Wealth Delta Tax - Group - ") — highest confidence.
      2. Substring match + appendix-awareness:
           Non-appendix shortcodes (no .A / .B / .C suffix): prefer PDFs whose
             stem does NOT contain "appendix"; fall back to any substring match.
           Appendix shortcodes (.A / .B / .C suffix): prefer PDFs whose stem
             DOES contain "appendix".
      3. Shortcode fallback (sc_dash anywhere in stem).

    Returns the best single match, or None.
    """
    if not pdf_dir.exists():
        return None

    # Is this shortcode an appendix paper?
    is_appendix = bool(re.search(r'\.[ABC]$', shortcode))

    # Build normalised short title from YAML title
    short_title: str | None = None
    if paper_meta:
        title = paper_meta.get("title", "")
        stripped = re.sub(
            r'^the\s+wealth\s+delta\s+tax\s*[:\-\u2013\u2014]\s*',
            "", title, flags=re.IGNORECASE
        ).strip()
        short_title = _normalise(stripped)

    sc_dash = _normalise(shortcode.replace(".", "-"))

    exact: list[Path] = []
    preferred: list[Path] = []
    fallback: list[Path] = []

    for pdf in sorted(pdf_dir.glob("*.pdf")):
        stem = _normalise(pdf.stem)
        has_appendix_word = "appendix" in stem

        # 1. Exact match on short title
        if short_title:
            # Remove group segment: stem is "wdt - group - short title"
            # Take everything after the second " - " as the title segment
            parts = re.split(r'\s+-\s+', pdf.stem, maxsplit=2)
            stem_title = _normalise(parts[-1]) if len(parts) >= 2 else stem
            if stem_title == short_title:
                exact.append(pdf)
                continue

        # 2 & 3. Substring + appendix-awareness
        if short_title and short_title in stem:
            if is_appendix and has_appendix_word:
                preferred.append(pdf)
            elif not is_appendix and not has_appendix_word:
                preferred.append(pdf)
            else:
                fallback.append(pdf)
            continue

        # 4. Shortcode fallback
        if sc_dash in stem:
            fallback.append(pdf)

    for bucket in (exact, preferred, fallback):
        if len(bucket) == 1:
            return bucket[0]
        if len(bucket) > 1:
            # Multiple candidates — return the shortest filename (closest match)
            return min(bucket, key=lambda p: len(p.stem))

    return None


def _find_latest_print_dir() -> Path | None:
    """Return the most recently created dated subfolder under print/."""
    if not PRINT_DIR.exists():
        return None
    candidates = sorted(
        (d for d in PRINT_DIR.iterdir() if d.is_dir() and re.match(r'^\d{6}$', d.name)),
        reverse=True,
    )
    return candidates[0] if candidates else None


# ── Abstract extraction ───────────────────────────────────────────────────────

# Match the Abstract section: heading + everything up to the next heading or EOF.
# Strips inline Quarto/markdown formatting before returning.
_ABSTRACT_RE = re.compile(
    r'#\s+Abstract[^\n]*\n+'   # heading line
    r'(.*?)'                   # body (captured)
    r'(?=\n#|\Z)',             # stop at next heading or EOF
    re.DOTALL | re.IGNORECASE,
)

def _clean_md(text: str) -> str:
    """
    Strip markdown formatting and LaTeX commands from abstract text,
    preserving readable plain-text content for Zenodo.

    Handles:
      - **bold** / *italic*  → plain text
      - [link text](url)     → link text only
      - {.attr} Quarto attrs → removed
      - `inline code`        → removed
      - \\newpage, \\tableofcontents, and other LaTeX commands → removed
      - Trailing blank lines produced by the above removals → collapsed
    """
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*',    r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'\{[^}]*\}', '', text)
    text = re.sub(r'`[^`]*`', '', text)
    # Strip LaTeX commands (e.g. \newpage, \tableofcontents, \medskip)
    # These appear at the tail of the abstract block before the next heading.
    text = re.sub(r'\\[a-zA-Z]+(?:\{[^}]*\})*', '', text)
    # Collapse runs of blank lines left by the removals above
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def extract_abstract(src_path: Path) -> str | None:
    """
    Extract the Abstract section from a source .md file.
    Returns cleaned plain text, or None if no Abstract section is found.
    """
    try:
        text = src_path.read_text(encoding="utf-8")
    except OSError:
        return None

    # Skip YAML frontmatter
    fm_end = re.search(r'^---\s*\n.*?^---\s*\n', text, re.DOTALL | re.MULTILINE)
    body = text[fm_end.end():] if fm_end else text

    m = _ABSTRACT_RE.search(body)
    if not m:
        return None

    raw = m.group(1).strip()
    if not raw:
        return None

    return _clean_md(raw)


# ── DOI writeback ─────────────────────────────────────────────────────────────

def _write_doi_to_source(src_path: Path, doi: str) -> None:
    """
    Write the published DOI back into the source file's zenodo_doi: field.
    Creates the field if absent; updates it if present.
    Preserves the rest of the file exactly.
    """
    try:
        text = src_path.read_text(encoding="utf-8")
    except OSError as e:
        log.warning(f"  Could not read {src_path} for DOI writeback: {e}")
        return

    fm_match = re.match(r'^---\s*\n(.*?)^---\s*\n', text, re.DOTALL | re.MULTILINE)
    if not fm_match:
        log.warning(f"  No frontmatter in {src_path.name} — DOI not written back")
        return

    fm_text = fm_match.group(1)
    body    = text[fm_match.end():]

    # Update existing zenodo_doi line or append it
    if re.search(r'^zenodo_doi\s*:', fm_text, re.MULTILINE):
        fm_text = re.sub(
            r'^(zenodo_doi\s*:).*$',
            f'zenodo_doi: "{doi}"',
            fm_text,
            flags=re.MULTILINE,
        )
    else:
        fm_text = fm_text.rstrip('\n') + f'\nzenodo_doi: "{doi}"\n'

    src_path.write_text(f"---\n{fm_text}---\n{body}", encoding="utf-8")
    log.info(f"  ✓ DOI written back to {src_path.name}")


# ── Logging ───────────────────────────────────────────────────────────────────
import io as _io

# Force UTF-8 on the console stream — Windows PowerShell defaults to cp1252
# which can't encode the Unicode box-drawing and tick characters we use.
_console = _io.TextIOWrapper(
    sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    handlers=[
        logging.StreamHandler(_console),
        logging.FileHandler(SCRIPT_DIR.parent / "print" / "zenodo_upload.log", mode="a", encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)

DOIS_FILE = SCRIPT_DIR.parent / "print" / "zenodo_dois.json"


def load_dois() -> dict:
    if DOIS_FILE.exists():
        return json.loads(DOIS_FILE.read_text())
    return {}


def save_dois(dois: dict) -> None:
    DOIS_FILE.write_text(json.dumps(dois, indent=2))


# ── Zenodo API helpers ────────────────────────────────────────────────────────

def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _json_headers(token: str) -> dict:
    return {**_auth_headers(token), "Content-Type": "application/json"}


def create_deposition(base: str, token: str) -> dict:
    r = requests.post(
        f"{base}/deposit/depositions",
        json={},
        headers=_json_headers(token),
    )
    r.raise_for_status()
    return r.json()


def upload_file(bucket_url: str, pdf_path: Path, token: str) -> dict:
    with open(pdf_path, "rb") as fh:
        r = requests.put(
            f"{bucket_url}/{pdf_path.name}",
            data=fh,
            headers=_auth_headers(token),
        )
    r.raise_for_status()
    return r.json()


def set_metadata(base: str, dep_id: int, meta: dict, token: str) -> dict:
    r = requests.put(
        f"{base}/deposit/depositions/{dep_id}",
        json={"metadata": meta},
        headers=_json_headers(token),
    )
    r.raise_for_status()
    return r.json()


def publish_deposition(base: str, dep_id: int, token: str) -> dict:
    r = requests.post(
        f"{base}/deposit/depositions/{dep_id}/actions/publish",
        headers=_auth_headers(token),
    )
    r.raise_for_status()
    return r.json()


# ── BibTeX reference formatter ────────────────────────────────────────────────

def _load_bib(bib_path: Path) -> dict[str, dict]:
    """
    Parse a .bib file into a dict keyed by cite key.
    Returns {key: {field: value, ...}} with field names lowercased.
    Values are raw BibTeX strings (not de-LaTeXed).
    """
    if not bib_path.exists():
        return {}

    entries: dict[str, dict] = {}
    text = bib_path.read_text(encoding="utf-8")

    # Match @type{key, ...} blocks
    for entry_match in re.finditer(
        r'@(\w+)\s*\{\s*([^,]+),\s*(.*?)\n\}',
        text, re.DOTALL
    ):
        entry_type = entry_match.group(1).lower()
        key        = entry_match.group(2).strip()
        body_text  = entry_match.group(3)

        fields: dict[str, str] = {"entry_type": entry_type}
        # Match field = {value} or field = "value" or field = bare_number
        for fmatch in re.finditer(
            r'(\w+)\s*=\s*(?:\{((?:[^{}]|\{[^{}]*\})*)\}|"([^"]*)"|([\w\d]+))',
            body_text
        ):
            fname = fmatch.group(1).lower()
            fval  = (fmatch.group(2) or fmatch.group(3) or fmatch.group(4) or "").strip()
            fields[fname] = fval

        entries[key] = fields

    return entries


def _strip_latex(s: str) -> str:
    """
    Remove common LaTeX markup from a BibTeX field value for plain-text display.
    Handles: {\'e} → e, {\\"o} → o, {\\~n} → n, {text} → text, \\cmd → removed.
    Not a full LaTeX parser — covers the common cases in academic .bib files.
    """
    # Accented characters: {\'x}, {\`x}, {\"x}, {\~x}, {\^x}, {\cx} etc.
    s = re.sub(r'\{\\[`\'"^~=.cbdruv]\s*(\w)\}', r'\1', s)
    s = re.sub(r'\\[`\'"^~=.cbdruv]\s*\{?(\w)\}?', r'\1', s)
    # {\ss} → ss, etc.
    s = re.sub(r'\{\\(\w+)\}', r'\1', s)
    # Remaining braces
    s = s.replace('{', '').replace('}', '')
    # LaTeX commands like \& → &, \textit{x} already handled above
    s = re.sub(r'\\&', '&', s)
    s = re.sub(r'\\%', '%', s)
    s = re.sub(r'\\([a-zA-Z]+)\s*', '', s)
    # Collapse extra whitespace
    s = re.sub(r'\s+', ' ', s).strip()
    return s


# JEL code → description mapping (covers codes used across WDT papers)
_JEL_DESCRIPTIONS: dict[str, str] = {
    "D31": "Personal Income, Wealth, and Their Distributions",
    "D63": "Justice; Equality; Inequality",
    "D72": "Political Processes: Rent-seeking, Lobbying, Elections",
    "D82": "Asymmetric and Private Information",
    "E21": "Macroeconomics: Consumption, Saving, Wealth",
    "E22": "Capital; Investment; Capacity",
    "E62": "Fiscal Policy; Government Expenditures and Related Policies",
    "G11": "Portfolio Choice; Investment Decisions",
    "G12": "Asset Pricing",
    "G18": "Government Policy and Regulation (Financial Markets)",
    "G32": "Financing Policy; Capital and Ownership Structure",
    "H20": "Taxation, Subsidies, and Revenue: General",
    "H21": "Efficiency; Optimal Taxation",
    "H22": "Incidence",
    "H24": "Personal Income and Other Nonbusiness Taxes and Subsidies",
    "H25": "Business Taxes and Subsidies",
    "H26": "Tax Evasion and Avoidance",
    "H41": "Public Goods",
    "H55": "Social Security and Public Pensions",
    "H56": "National Security and War",
    "H63": "Debt; Debt Management; Sovereign Debt",
    "H87": "International Fiscal Issues",
    "K34": "Tax Law",
    "K40": "Legal Procedure, the Legal System, and Illegal Behavior: General",
    "L51": "Economics of Regulation",
    "N40": "Government, War, Law, International Relations (Economic History): General",
    "P16": "Political Economy",
    "P48": "Political Economy: Other",
    "Q50": "Environmental Economics: General",
    "Q58": "Environmental Economics: Government Policy",
}


def _format_reference(key: str, fields: dict) -> str | None:
    """
    Format a BibTeX entry as a plain-text APA-style reference string.
    Returns None if the entry lacks enough information to be useful.
    """
    entry_type = fields.get("entry_type", "misc")
    author  = _strip_latex(fields.get("author", ""))
    title   = _strip_latex(fields.get("title", ""))
    year    = _strip_latex(fields.get("year", ""))

    if not (author and title and year):
        return None

    # Normalise author: "Last, F. and Last, F." → "Last, F., & Last, F."
    authors = re.split(r'\s+and\s+', author, flags=re.IGNORECASE)
    if len(authors) > 1:
        author_str = ", ".join(authors[:-1]) + ", & " + authors[-1]
    else:
        author_str = authors[0]

    if entry_type in ("article",):
        journal = _strip_latex(fields.get("journal", ""))
        vol     = fields.get("volume", "")
        num     = fields.get("number", "")
        pages   = fields.get("pages", "").replace("--", "–")
        doi     = fields.get("doi", "")
        vol_str = f", {vol}" if vol else ""
        num_str = f"({num})" if num else ""
        page_str = f", {pages}" if pages else ""
        doi_str  = f" https://doi.org/{doi}" if doi else ""
        return f"{author_str} ({year}). {title}. {journal}{vol_str}{num_str}{page_str}.{doi_str}"

    elif entry_type == "book":
        publisher = _strip_latex(fields.get("publisher", ""))
        return f"{author_str} ({year}). {title}. {publisher}."

    elif entry_type in ("techreport", "unpublished"):
        institution = _strip_latex(fields.get("institution", ""))
        number      = fields.get("number", "")
        doi         = fields.get("doi", "")
        inst_str    = f" {institution}," if institution else ""
        num_str     = f" No. {number}." if number else "."
        doi_str     = f" https://doi.org/{doi}" if doi else ""
        return f"{author_str} ({year}). {title}.{inst_str}{num_str}{doi_str}"

    elif entry_type == "incollection":
        booktitle = _strip_latex(fields.get("booktitle", ""))
        editor    = _strip_latex(fields.get("editor", ""))
        publisher = _strip_latex(fields.get("publisher", ""))
        pages     = fields.get("pages", "").replace("--", "–")
        ed_str    = f" In {editor} (Ed.), " if editor else " In "
        page_str  = f" (pp. {pages})." if pages else "."
        return f"{author_str} ({year}). {title}.{ed_str}{booktitle}{page_str} {publisher}."

    else:  # misc, etc.
        howpublished = _strip_latex(fields.get("howpublished", ""))
        url          = fields.get("url", "")
        pub_str      = f" {howpublished}." if howpublished else "."
        url_str      = f" {url}" if url else ""
        return f"{author_str} ({year}). {title}.{pub_str}{url_str}"


def build_references_list(cite_keys: list[str], bib: dict[str, dict]) -> list[str]:
    """
    Return a list of plain-text APA-style reference strings for the given
    cite keys, in alphabetical order. Keys not found in the bib are skipped.
    """
    refs = []
    for key in sorted(cite_keys):
        fields = bib.get(key)
        if not fields:
            continue
        formatted = _format_reference(key, fields)
        if formatted:
            refs.append(formatted)
    return refs


# ── Related identifiers ───────────────────────────────────────────────────────

def build_related_identifiers(
    shortcode: str,
    all_dois: dict[str, str],
    site_page: str,
) -> list[dict]:
    """
    Build the related_identifiers list for one paper:
      - Its HTML page on the site  (isIdenticalTo, url)
      - All sibling papers         (isPartOf, doi)
    """
    related: list[dict] = []

    # Link to the HTML version on the site
    if site_page:
        related.append({
            "identifier":    site_page,
            "relation":      "isIdenticalTo",
            "scheme":        "url",
            "resource_type": "other",
        })

    # Cross-link to all other papers in the series
    for sibling_sc, sibling_doi in sorted(all_dois.items()):
        if sibling_sc == shortcode:
            continue
        related.append({
            "identifier":    sibling_doi,
            "relation":      "isPartOf",
            "scheme":        "doi",
            "resource_type": "publication-workingpaper",
        })

    return related


# ── Zenodo API: new version / metadata update ─────────────────────────────────

def get_deposition_id(base: str, doi: str, token: str) -> int | None:
    """
    Look up a deposition by DOI and return its integer ID.
    Works for both published records (via /records) and drafts.
    """
    # Extract the Zenodo record ID from the DOI (10.5281/zenodo.NNNNNN)
    m = re.search(r'zenodo\.(\d+)', doi)
    if not m:
        return None
    record_id = m.group(1)

    # Fetch the published record to get the latest recid
    r = requests.get(
        f"{base}/records/{record_id}",
        headers=_auth_headers(token),
    )
    if not r.ok:
        return None
    return r.json().get("id")


def unlock_for_edit(base: str, dep_id: int, token: str) -> dict:
    """
    Reopen a published deposition for metadata editing. Keeps the same DOI and
    does not create a new version. If it is already unlocked, return it as-is.
    """
    r = requests.post(
        f"{base}/deposit/depositions/{dep_id}/actions/edit",
        headers=_auth_headers(token),
    )
    if r.status_code == 409:  # already in edit state
        r = requests.get(
            f"{base}/deposit/depositions/{dep_id}",
            headers=_auth_headers(token),
        )
    r.raise_for_status()
    return r.json()


# ── Build Zenodo metadata from extract_paper_meta() output ───────────────────

def build_zenodo_meta(
    paper_meta: dict[str, Any],
    abstract: str | None,
    bib: dict[str, dict] | None = None,
    all_dois: dict[str, str] | None = None,
    site_link_map: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    Assemble the Zenodo metadata payload from pipeline-extracted paper_meta.

    paper_meta keys used:
        title           — from YAML frontmatter title:
        keywords        — from YAML frontmatter keywords:
        jel             — list of JEL code strings from frontmatter
        cite_keys       — list of @cite keys found in the body
        version         — from revision history table (latest row)
        version_date    — ISO date string from revision history
        shortcode       — e.g. "CORP.A"

    Optional enrichment:
        bib             — parsed .bib dict for reference formatting
        all_dois        — {shortcode: doi} map for cross-linking
        site_link_map   — {shortcode: "page.html"} for site URL links
    """
    title     = paper_meta["title"]
    keywords  = paper_meta.get("keywords", [])
    jel_codes = paper_meta.get("jel", [])
    cite_keys = paper_meta.get("cite_keys", [])
    version   = paper_meta.get("version", "")
    iso_date  = paper_meta.get("version_date", "")
    shortcode = paper_meta["shortcode"]

    # Ensure "Wealth Delta Tax" and shortcode are always in keywords
    kw = list(dict.fromkeys(["Wealth Delta Tax", shortcode] + keywords))

    description = abstract or (
        f"Working paper ({shortcode}) from the Wealth Delta Tax research programme."
    )

    # ── JEL subjects ──────────────────────────────────────────────────────
    subjects: list[dict] = []
    for code in jel_codes:
        term = _JEL_DESCRIPTIONS.get(code, code)
        subjects.append({
            "term":       f"{code} {term}",
            "identifier": f"https://www.aeaweb.org/econlit/jelCodes.php?view=jel#{code}",
            "scheme":     "url",
        })
    # Zenodo's record page does not reliably display subjects, so also expose
    # the codes as searchable keywords.
    kw = list(dict.fromkeys(kw + [f"JEL {code}" for code in jel_codes]))

    # ── Related identifiers: site URL + sibling DOIs ──────────────────────
    related: list[dict] = []
    if site_link_map and shortcode in site_link_map:
        page_path = site_link_map[shortcode]
        site_url  = f"{cfg.SITE_URL}/{page_path}"
        related = build_related_identifiers(shortcode, all_dois or {}, site_url)
    elif all_dois:
        related = build_related_identifiers(shortcode, all_dois, "")

    # ── Plain-text references ─────────────────────────────────────────────
    ref_strings: list[str] = []
    if bib and cite_keys:
        ref_strings = build_references_list(cite_keys, bib)

    meta: dict[str, Any] = {
        **SHARED,
        "title":          title,
        "description":    description,
        "keywords":       kw,
        "version":        version,
        "prereserve_doi": True,
        "notes": (
            f"Shortcode: ({shortcode}). "
            "Part of the Wealth Delta Tax working paper series. "
            f"{cfg.SITE_URL}"
        ),
    }

    if iso_date:
        meta["publication_date"] = iso_date
    if subjects:
        meta["subjects"] = subjects
    if related:
        meta["related_identifiers"] = related
    if ref_strings:
        meta["references"] = ref_strings

    return meta


# ── Per-paper upload ──────────────────────────────────────────────────────────

def upload_paper(
    src_path: Path,
    paper_meta: dict[str, Any],
    abstract: str | None,
    pdf_path: Path,
    base: str,
    token: str,
    dry_run: bool,
    write_doi_back: bool,
    bib: dict[str, dict] | None = None,
    all_dois: dict[str, str] | None = None,
    site_link_map: dict[str, str] | None = None,
) -> str | None:
    """
    Upload and publish one paper. Returns the DOI string on success, None on
    skip/failure. On dry_run=True, validates paths and logs intent only.
    """
    shortcode = paper_meta["shortcode"]

    if not pdf_path.exists():
        log.error(f"[{shortcode}] PDF not found: {pdf_path} — SKIPPED")
        return None

    if dry_run:
        jel   = paper_meta.get("jel", [])
        nrefs = len(build_references_list(paper_meta.get("cite_keys", []), bib or {}))
        log.info(
            f"[{shortcode}] DRY RUN — PDF: {pdf_path.name} "
            f"({pdf_path.stat().st_size:,} bytes)  "
            f"abstract: {'✓' if abstract else '✗ MISSING'}  "
            f"JEL: {len(jel)}  refs: {nrefs}"
        )
        if not abstract:
            log.warning(f"[{shortcode}] No abstract found — would use fallback description")
        return "dry-run-doi"

    zenodo_meta = build_zenodo_meta(
        paper_meta, abstract,
        bib=bib,
        all_dois=all_dois,
        site_link_map=site_link_map,
    )
    log.info(
        f"[{shortcode}] subjects: {len(zenodo_meta.get('subjects', []))}  "
        f"references: {len(zenodo_meta.get('references', []))}  "
        f"related: {len(zenodo_meta.get('related_identifiers', []))}"
    )

    # 1. Create empty deposition
    log.info(f"[{shortcode}] Creating deposition …")
    dep        = create_deposition(base, token)
    dep_id     = dep["id"]
    bucket_url = dep["links"]["bucket"]
    log.info(f"[{shortcode}] Deposition ID: {dep_id}")

    # 2. Upload PDF
    size_mb = pdf_path.stat().st_size / 1_048_576
    log.info(f"[{shortcode}] Uploading {pdf_path.name} ({size_mb:.1f} MB) …")
    upload_file(bucket_url, pdf_path, token)

    # 3. Set metadata (reserves DOI)
    log.info(f"[{shortcode}] Setting metadata …")
    updated     = set_metadata(base, dep_id, zenodo_meta, token)
    reserved    = (
        updated.get("metadata", {})
               .get("prereserve_doi", {})
               .get("doi", f"10.5281/zenodo.{dep_id}")
    )
    log.info(f"[{shortcode}] Reserved DOI: {reserved}")

    # 4. Publish
    log.info(f"[{shortcode}] Publishing …")
    result = publish_deposition(base, dep_id, token)
    doi    = result.get("doi", reserved)
    log.info(f"[{shortcode}] ✓ Published — DOI: {doi}")

    # 5. Write DOI back to source file
    if write_doi_back:
        _write_doi_to_source(src_path, doi)

    return doi


# ── Post-publish metadata update ─────────────────────────────────────────────

def update_published_metadata(
    paper_inputs: dict[str, tuple[dict, str | None]],
    dois: dict[str, str],
    base: str,
    token: str,
    dry_run: bool,
    site_link_map: dict[str, str],
    bib: dict[str, dict],
) -> None:
    """
    Refresh the full metadata of every already-published record: JEL subjects,
    references, related identifiers (siblings + site URL), keywords, etc.

    Uses Zenodo's edit action, so DOIs and versions do not change. Safe to
    re-run. paper_inputs maps shortcode -> (paper_meta, abstract).
    """
    log.info(f"\nRefreshing metadata for {len(dois)} published papers ...\n")

    for i, (shortcode, doi) in enumerate(sorted(dois.items()), 1):
        log.info(f"[{i}/{len(dois)}] {shortcode}  DOI: {doi}")

        if shortcode not in paper_inputs:
            log.warning(f"  [{shortcode}] No source metadata found - skipping")
            continue
        paper_meta, abstract = paper_inputs[shortcode]

        meta = build_zenodo_meta(
            paper_meta, abstract,
            bib=bib, all_dois=dois, site_link_map=site_link_map,
        )
        meta.pop("prereserve_doi", None)   # record already has its DOI

        log.info(
            f"  subjects: {len(meta.get('subjects', []))}  "
            f"references: {len(meta.get('references', []))}  "
            f"related: {len(meta.get('related_identifiers', []))}"
        )

        if dry_run:
            continue

        try:
            dep_id = get_deposition_id(base, doi, token)
            if not dep_id:
                log.warning(f"  [{shortcode}] Could not resolve deposition ID - skipping")
                continue

            unlock_for_edit(base, dep_id, token)
            set_metadata(base, dep_id, meta, token)
            publish_deposition(base, dep_id, token)
            log.info(f"  [{shortcode}] updated")

        except requests.HTTPError as exc:
            body = exc.response.text[:400]
            log.error(f"  [{shortcode}] HTTP {exc.response.status_code}: {body}")
        except Exception as exc:
            log.error(f"  [{shortcode}] Unexpected error: {exc}")

        if i < len(dois):
            time.sleep(2)

    log.info("\nMetadata refresh complete.\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bulk upload WDT papers to Zenodo using pipeline metadata."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--sandbox",
        action="store_true",
        help="Use sandbox.zenodo.org (safe for testing).",
    )
    mode.add_argument(
        "--publish",
        action="store_true",
        help="Use zenodo.org (LIVE). Records are permanent once published.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate paths and metadata; make no API calls.",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        metavar="SHORTCODE",
        help="Upload only these shortcodes (e.g. --only WP CORP CORP.A).",
    )
    parser.add_argument(
        "--pdf-dir",
        type=Path,
        default=None,
        metavar="DIR",
        help=(
            "Path to the dated print/ subfolder containing PDFs. "
            "Defaults to the most recent print/YYMMDD/ folder."
        ),
    )
    parser.add_argument(
        "--no-doi-writeback",
        action="store_true",
        help="Do not write the published DOI back into source .md frontmatter.",
    )
    parser.add_argument(
        "--update-metadata", "--update-related",
        dest="update_metadata",
        action="store_true",
        help=(
            "Post-publish pass: rebuild the full metadata (JEL, references, "
            "related identifiers, keywords) for every DOI in zenodo_dois.json "
            "and update the records in place. DOIs and versions do not change. "
            "Safe to re-run."
        ),
    )
    parser.add_argument(
        "--bib",
        type=Path,
        default=cfg.ROOT_DIR / "registry" / "references.bib",
        metavar="PATH",
        help="Path to the references.bib file (default: pipeline/references.bib).",
    )
    args = parser.parse_args()

    base  = SANDBOX_BASE if args.sandbox else LIVE_BASE
    token = SANDBOX_TOKEN if args.sandbox else LIVE_TOKEN

    if token in ("CHANGE_ME_SANDBOX", "CHANGE_ME_LIVE"):
        log.error(
            "No API token set. Edit SANDBOX_TOKEN / LIVE_TOKEN at the top "
            "of this file, or set ZENODO_SANDBOX_TOKEN / ZENODO_LIVE_TOKEN "
            "environment variables."
        )
        sys.exit(1)

    # Resolve PDF directory
    pdf_dir = args.pdf_dir or _find_latest_print_dir()
    if not pdf_dir or not pdf_dir.exists():
        log.error(
            f"No PDF directory found. Run pdf.py first, or pass --pdf-dir."
        )
        sys.exit(1)

    env_label = "SANDBOX" if args.sandbox else "LIVE ⚠️"
    log.info("─" * 60)
    log.info(f"Zenodo bulk upload — environment: {env_label}")
    log.info(f"PDF directory:      {pdf_dir}")
    log.info(f"Dry run:            {args.dry_run}")
    if args.only:
        log.info(f"Filter:             {args.only}")
    log.info("─" * 60)

    # ── Load papers registry ──────────────────────────────────────────────
    if not cfg.REGISTRY_YML.exists():
        log.error(f"registry/papers.yml not found at {cfg.REGISTRY_YML}")
        sys.exit(1)

    with cfg.REGISTRY_YML.open(encoding="utf-8") as fh:
        registry: list[dict] = yaml.safe_load(fh)

    # ── Load BibTeX database ──────────────────────────────────────────────
    bib_path = args.bib
    if bib_path.exists():
        bib = _load_bib(bib_path)
        log.info(f"BibTeX:             {bib_path.name} ({len(bib)} entries)")
    else:
        bib = {}
        log.warning(f"BibTeX not found at {bib_path} — references will be omitted")

    # ── Build site link map from contents.yml ────────────────────────────
    site_link_map: dict[str, str] = {}
    if cfg.CONTENTS_YML.exists():
        with cfg.CONTENTS_YML.open(encoding="utf-8") as fh:
            contents = yaml.safe_load(fh) or {}
        site_link_map = {sc: v["page"] for sc, v in contents.items() if "page" in v}

    # ── --update-metadata branch ──────────────────────────────────────────
    if args.update_metadata:
        dois = load_dois()
        if not dois:
            log.error("zenodo_dois.json is empty - run a full upload first.")
            sys.exit(1)

        paper_inputs: dict[str, tuple[dict, str | None]] = {}
        for entry in registry:
            src = cfg.SOURCE_DIR / entry["source"]
            if not src.exists():
                continue
            m = cfg.extract_paper_meta(src)
            if not m:
                continue
            if args.only and m["shortcode"] not in args.only:
                continue
            paper_inputs[m["shortcode"]] = (m, extract_abstract(src))

        if args.only:
            dois = {k: v for k, v in dois.items() if k in args.only}

        update_published_metadata(
            paper_inputs=paper_inputs,
            dois=dois,
            base=base,
            token=token,
            dry_run=args.dry_run,
            site_link_map=site_link_map,
            bib=bib,
        )
        return

    # ── Extract metadata from all source files ────────────────────────────
    papers: list[tuple[Path, dict, str | None, Path]] = []
    # Each entry: (src_path, paper_meta, abstract, pdf_path)

    for entry in registry:
        src_path = cfg.SOURCE_DIR / entry["source"]
        if not src_path.exists():
            log.warning(f"Source not found: {entry['source']} — skipping")
            continue

        meta = cfg.extract_paper_meta(src_path)
        if not meta:
            log.warning(f"Metadata extraction failed: {entry['source']} — skipping")
            continue

        shortcode = meta["shortcode"]

        if args.only and shortcode not in args.only:
            continue

        abstract = extract_abstract(src_path)
        pdf_path = _find_pdf(shortcode, pdf_dir, paper_meta=meta)

        if pdf_path is None:
            log.warning(
                f"[{shortcode}] No PDF found in {pdf_dir} — "
                f"will fail unless --dry-run"
            )
            pdf_path = pdf_dir / f"{shortcode}.pdf"  # placeholder for dry-run

        papers.append((src_path, meta, abstract, pdf_path))

    if not papers:
        log.error("No papers to process.")
        sys.exit(1)

    log.info(f"\nPapers to process: {len(papers)}\n")

    # ── Upload loop ───────────────────────────────────────────────────────
    dois = load_dois()
    results: dict[str, list[str]] = {"success": [], "skipped": [], "failed": []}

    for i, (src_path, meta, abstract, pdf_path) in enumerate(papers, 1):
        shortcode = meta["shortcode"]
        log.info(f"\n[{i}/{len(papers)}] {shortcode}  —  {meta['title'][:60]}")

        if shortcode in dois and not args.dry_run:
            log.info(f"  Already published: {dois[shortcode]} — skipping")
            results["skipped"].append(shortcode)
            continue

        try:
            doi = upload_paper(
                src_path=src_path,
                paper_meta=meta,
                abstract=abstract,
                pdf_path=pdf_path,
                base=base,
                token=token,
                dry_run=args.dry_run,
                write_doi_back=not args.no_doi_writeback,
                bib=bib,
                all_dois=dois,
                site_link_map=site_link_map,
            )
            if doi and not args.dry_run:
                dois[shortcode] = doi
                save_dois(dois)        # write after every paper — safe to interrupt
            if doi:
                results["success"].append(shortcode)
            else:
                results["failed"].append(shortcode)

        except requests.HTTPError as exc:
            body = exc.response.text[:400]
            log.error(f"  HTTP {exc.response.status_code}: {body}")
            results["failed"].append(shortcode)
        except Exception as exc:
            log.error(f"  Unexpected error: {exc}")
            results["failed"].append(shortcode)

        # Stay within Zenodo's 100 req/min authenticated rate limit
        if i < len(papers) and not args.dry_run:
            time.sleep(2)

    # ── Summary ───────────────────────────────────────────────────────────
    log.info("\n" + "─" * 60)
    log.info(
        f"Done.  ✓ {len(results['success'])}  "
        f"↷ {len(results['skipped'])} skipped  "
        f"✗ {len(results['failed'])} failed"
    )
    if results["failed"]:
        log.warning(f"Failed: {results['failed']}")
    if not args.dry_run and results["success"]:
        log.info(f"DOI map: {DOIS_FILE.resolve()}")
        log.info(
            "Tip: run with --update-metadata to cross-link all papers "
            "once the full upload is complete."
        )
    log.info("─" * 60 + "\n")


if __name__ == "__main__":
    main()
