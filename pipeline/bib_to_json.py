"""
bib_to_json.py — generate registry/references.json from registry/references.bib
               + registry/internal.json.

Called automatically by preprocess.py at the top of every build.
Can also be run standalone:  python pipeline/bib_to_json.py

Inputs:
    registry/references.bib     — canonical external bibliographic data
    registry/internal.json      — hand-maintained: internal_papers, citations, flags,
                                  alt_author_overrides

Output:
    registry/references.json    — fully generated; safe to delete and regenerate at any time

Mapping rules
─────────────
BibTeX @type          → JSON type
@article              → journal_article
@book                 → book
@incollection         → book_chapter
@unpublished          → working_paper
@techreport           → working_paper  (if institution contains NBER/CESifo/WID,
                                        or entry has type = "Working Paper")
                      → report         (all other @techreport)
@misc                 → institutional_report

BibTeX field          → JSON field
author                → authors[]  (parsed last/first; institutional = last only)
year                  → year (int)
title                 → title (LaTeX braces stripped, diacritics decoded)
journal               → journal
volume                → volume (str)
number                → issue  for @article; number for @techreport
pages                 → pages (-- → –)
doi                   → doi
url                   → url
publisher /
  institution /
  howpublished        → publisher (first non-null wins)
series                → series

note field parsing:
    "Verified YYYY-MM-DD[.]..." → verified=True, verified_date=YYMMDD
    "Flag N: ..."               → flag_ids += ["flag_NN"]  (cross-checked against
                                  internal.json flags — only ids present there are kept)
    remainder                   → verification_notes (stripped of LaTeX)

Fields populated from internal.json at merge time:
    citation_ids[]   — derived from citations array (refs where ref_id == this entry's id)
    flag_ids[]       — merged: bib-note flags + any already in internal flags.affects_refs
    alt_author_forms — from alt_author_overrides dict
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

# ── Paths ─────────────────────────────────────────────────────────────────────

SCRIPT_DIR   = Path(__file__).resolve().parent        # pipeline/
ROOT_DIR     = SCRIPT_DIR.parent                      # wdt-site/
REGISTRY_DIR = ROOT_DIR / "registry"

BIB_PATH      = REGISTRY_DIR / "references.bib"
INTERNAL_PATH = REGISTRY_DIR / "internal.json"
OUTPUT_PATH   = REGISTRY_DIR / "references.json"


# ── BibTeX type → JSON type ───────────────────────────────────────────────────

# Institutions whose @techreport entries are working papers, not formal reports
_WORKING_PAPER_INSTITUTIONS = {
    "national bureau of economic research",
    "nber",
    "cesifo",
    "cesifo",
    "wid",
    "wid world",
}

def _bib_type_to_json(entry: dict) -> str:
    btype = entry["ENTRYTYPE"].lower()
    if btype == "article":
        return "journal_article"
    if btype == "book":
        return "book"
    if btype == "incollection":
        return "book_chapter"
    if btype == "unpublished":
        return "working_paper"
    if btype == "misc":
        return "institutional_report"
    if btype == "techreport":
        entry_type = entry.get("type", "").strip().lower()
        institution = entry.get("institution", "").strip().lower()
        if entry_type == "working paper":
            return "working_paper"
        if any(wp in institution for wp in _WORKING_PAPER_INSTITUTIONS):
            return "working_paper"
        return "report"
    # fallback
    return btype


# ── LaTeX cleaning ────────────────────────────────────────────────────────────

# Strip protective braces used in BibTeX titles: {German} → German
_BRACE_RE = re.compile(r"\{([^{}]+)\}")

# Common LaTeX diacritic commands → unicode
_LATEX_DIACRITICS = [
    (r"\\`([aeiouAEIOU])",   lambda m: {
        "a":"à","e":"è","i":"ì","o":"ò","u":"ù",
        "A":"À","E":"È","I":"Ì","O":"Ò","U":"Ù"
    }.get(m.group(1), m.group(0))),
    (r"\\'([aeiouAEIOU])",   lambda m: {
        "a":"á","e":"é","i":"í","o":"ó","u":"ú",
        "A":"Á","E":"É","I":"Í","O":"Ó","U":"Ú"
    }.get(m.group(1), m.group(0))),
    (r'\\"([aeiouAEIOU])',   lambda m: {
        "a":"ä","e":"ë","i":"ï","o":"ö","u":"ü",
        "A":"Ä","E":"Ë","I":"Ï","O":"Ö","U":"Ü"
    }.get(m.group(1), m.group(0))),
    (r"\\~([aeiounAEIOUN])", lambda m: {
        "a":"ã","e":"ẽ","i":"ĩ","o":"õ","u":"ũ","n":"ñ",
        "A":"Ã","E":"Ẽ","I":"Ĩ","O":"Õ","U":"Ũ","N":"Ñ"
    }.get(m.group(1), m.group(0))),
    (r"\\c\{?([cC])\}?",    lambda m: "ç" if m.group(1)=="c" else "Ç"),
    (r"\\\^([aeiouAEIOU])",  lambda m: {
        "a":"â","e":"ê","i":"î","o":"ô","u":"û",
        "A":"Â","E":"Ê","I":"Î","O":"Ô","U":"Û"
    }.get(m.group(1), m.group(0))),
    (r"\\o\b",               lambda m: "ø"),
    (r"\\O\b",               lambda m: "Ø"),
    (r"\\aa\b",              lambda m: "å"),
    (r"\\AA\b",              lambda m: "Å"),
    (r"\\ae\b",              lambda m: "æ"),
    (r"\\AE\b",              lambda m: "Æ"),
    (r"\\ss\b",              lambda m: "ß"),
    (r"\\textit\{([^}]+)\}", lambda m: m.group(1)),
    (r"\\emph\{([^}]+)\}",  lambda m: m.group(1)),
    (r"\\&",                 lambda m: "&"),
    (r"\\`\{([^}]+)\}",     lambda m: m.group(1)),  # fallback braced accent
]

def _clean_latex(text: str) -> str:
    """Strip LaTeX markup from a string, decode diacritics to unicode."""
    if not text:
        return text
    for pattern, repl in _LATEX_DIACRITICS:
        text = re.sub(pattern, repl, text)
    # strip remaining protective braces
    prev = None
    while prev != text:
        prev = text
        text = _BRACE_RE.sub(r"\1", text)
    # collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ── Author parsing ────────────────────────────────────────────────────────────

def _parse_authors(raw: str) -> list[dict[str, str | None]]:
    """
    Parse a BibTeX author string into [{last, first}, ...].

    After convert_to_unicode, protective braces around institutional names
    are stripped.  We detect institutional authors by the absence of any
    comma in the full string: genuine personal-name lists always contain
    commas ('Last, First and Last, First'); institutional names never do.
    """
    if not raw:
        return []

    # No comma anywhere → entire string is one institutional author
    if "," not in raw:
        return [{"last": _clean_latex(raw.strip()), "first": None}]

    # Split on ' and ' to get individual authors
    parts = re.split(r"\s+and\s+", raw, flags=re.IGNORECASE)
    result = []
    for part in parts:
        part = part.strip()
        # Residual braces (bibtexparser sometimes leaves them)
        if part.startswith("{") and part.endswith("}"):
            result.append({"last": _clean_latex(part[1:-1]), "first": None})
            continue
        if "," in part:
            last, _, first = part.partition(",")
            result.append({
                "last":  _clean_latex(last.strip()),
                "first": _clean_latex(first.strip()) or None,
            })
        else:
            # Single token or "First Last" form (very rare in this bib)
            tokens = part.split()
            if len(tokens) >= 2:
                result.append({
                    "last":  _clean_latex(tokens[-1]),
                    "first": _clean_latex(" ".join(tokens[:-1])),
                })
            else:
                result.append({"last": _clean_latex(part), "first": None})
    return result


# ── Pages normalisation ───────────────────────────────────────────────────────

def _clean_pages(raw: str | None) -> str | None:
    if not raw:
        return None
    # BibTeX double-dash → en-dash
    return raw.replace("--", "–").strip()


# ── Note field parser ─────────────────────────────────────────────────────────

_VERIFIED_DATE_RE = re.compile(
    r"Verified\s+(\d{4})-(\d{2})-(\d{2})",
    re.IGNORECASE,
)
_FLAG_RE = re.compile(r"\bFlag\s+(\d+)", re.IGNORECASE)
# Strip LaTeX commands from notes before storing as verification_notes
_LATEX_CMD_RE = re.compile(
    r"\\(?:textit|emph|textbf|S|section)\{([^}]*)\}|\\[a-zA-Z]+\s*|\{|\}"
)

def _parse_note(raw: str | None) -> tuple[bool, str | None, list[str], str | None]:
    """
    Returns (verified, verified_date_YYMMDD, flag_ids_from_note, verification_notes).
    """
    if not raw:
        return False, None, [], None

    raw = raw.strip()
    verified = False
    verified_date = None
    flag_ids: list[str] = []

    # Extract verified date
    vm = _VERIFIED_DATE_RE.search(raw)
    if vm:
        verified = True
        yy = vm.group(1)[2:]   # 2026 → 26
        mm = vm.group(2)
        dd = vm.group(3)
        verified_date = f"{yy}{mm}{dd}"

    # Extract flag numbers
    for fm in _FLAG_RE.finditer(raw):
        flag_ids.append(f"flag_{int(fm.group(1)):02d}")

    # Build verification_notes: strip the "Verified DATE." sentence and Flag lines,
    # keep whatever substantive content remains.
    notes_text = raw
    # Remove "Verified YYYY-MM-DD[.]" clause
    notes_text = re.sub(r"Verified\s+\d{4}-\d{2}-\d{2}\.?\s*", "", notes_text, flags=re.IGNORECASE)
    # Remove lines that are purely flag notices (start with "Flag N:")
    lines = notes_text.splitlines()
    kept = []
    skip_continuation = False
    for line in lines:
        stripped = line.strip()
        if re.match(r"Flag\s+\d+", stripped, re.IGNORECASE):
            skip_continuation = True
            continue
        # A continuation line of a flag block is indented or starts lowercase
        if skip_continuation and stripped and (line.startswith(" ") or (stripped[0].islower())):
            continue
        skip_continuation = False
        if stripped:
            kept.append(stripped)

    notes_text = " ".join(kept).strip()

    # Strip remaining LaTeX markup from notes
    notes_text = _LATEX_CMD_RE.sub(lambda m: m.group(1) or "", notes_text)
    notes_text = re.sub(r"\s+", " ", notes_text).strip()

    verification_notes = notes_text if notes_text else None
    return verified, verified_date, flag_ids, verification_notes


# ── Main conversion ───────────────────────────────────────────────────────────

def _entry_to_ref(entry: dict) -> dict[str, Any]:
    """Convert one bibtexparser entry dict to a references.json external_ref record."""
    btype = entry["ENTRYTYPE"]
    key   = entry["ID"]

    verified, verified_date, flag_ids_from_note, verification_notes = \
        _parse_note(entry.get("note"))

    # Publisher: first non-empty of publisher / institution / howpublished
    publisher = (
        entry.get("publisher") or
        entry.get("institution") or
        entry.get("howpublished") or
        None
    )
    if publisher:
        publisher = _clean_latex(publisher)

    # number field: issue for articles, report number for techreports
    raw_number = entry.get("number")
    is_article = btype == "article"
    issue  = raw_number if is_article else None
    number = raw_number if not is_article else None

    return {
        "id":                 key,
        "type":               _bib_type_to_json(entry),
        "authors":            _parse_authors(entry.get("author", "")),
        "year":               int(entry["year"]) if entry.get("year") else None,
        "title":              _clean_latex(entry.get("title", "")),
        "publisher":          publisher,
        "journal":            _clean_latex(entry.get("journal")) if entry.get("journal") else None,
        "volume":             entry.get("volume") or None,
        "issue":              issue,
        "pages":              _clean_pages(entry.get("pages")),
        "series":             _clean_latex(entry.get("series")) if entry.get("series") else None,
        "number":             number,
        "doi":                entry.get("doi") or None,
        "url":                entry.get("url") or None,
        "verified":           verified,
        "verified_date":      verified_date,
        "verification_notes": verification_notes,
        "alt_author_forms":   [],          # filled during merge
        "citation_ids":       [],          # filled during merge
        "flag_ids":           flag_ids_from_note,  # may gain more during merge
    }


def load_bib(path: Path) -> list[dict[str, Any]]:
    parser = BibTexParser(common_strings=True)
    parser.customization = convert_to_unicode
    with path.open(encoding="utf-8") as f:
        db = bibtexparser.load(f, parser=parser)
    refs = [_entry_to_ref(e) for e in db.entries]
    # Sort alphabetically by id (matches existing JSON ordering)
    refs.sort(key=lambda r: r["id"])
    return refs


def merge(
    ext_refs: list[dict],
    internal: dict,
) -> dict[str, Any]:
    """
    Merge external_references (from bib) with internal.json to produce
    the complete references.json structure.
    """
    citations:  list[dict] = internal["citations"]
    flags:      list[dict] = internal["flags"]
    alt_map:    dict       = internal.get("alt_author_overrides", {})

    # Build lookup: ref_id → list of citation_ids
    citation_index: dict[str, list[str]] = {}
    for c in citations:
        rid = c["ref_id"]
        citation_index.setdefault(rid, []).append(c["id"])

    # Build lookup: ref_id → set of flag_ids (from flags.affects_refs)
    flag_index: dict[str, set[str]] = {}
    for fl in flags:
        for rid in fl.get("affects_refs", []):
            flag_index.setdefault(rid, set()).add(fl["id"])

    # All valid flag ids (so we don't invent phantom ones from note text)
    valid_flag_ids = {fl["id"] for fl in flags}

    for ref in ext_refs:
        rid = ref["id"]
        # citation_ids
        ref["citation_ids"] = sorted(citation_index.get(rid, []))
        # flag_ids: merge note-parsed + flag_index, keep only valid ones, dedup, sort
        merged_flags = set(ref["flag_ids"]) | flag_index.get(rid, set())
        ref["flag_ids"] = sorted(f for f in merged_flags if f in valid_flag_ids)
        # alt_author_forms
        ref["alt_author_forms"] = alt_map.get(rid, [])

    today = date.today().strftime("%y%m%d")  # YYMMDD

    return {
        "meta": {
            "version":              "0.1",
            "date":                 today,
            "generated_by":         "pipeline/bib_to_json.py",
            "source_bib":           "registry/references.bib",
            "source_internal":      "registry/internal.json",
            "total_external_refs":  len(ext_refs),
            "total_internal_papers": len(internal["internal_papers"]),
            "total_citations":      len(citations),
            "total_flags":          len(flags),
        },
        "external_references": ext_refs,
        "internal_papers":     internal["internal_papers"],
        "citations":           citations,
        "flags":               flags,
    }


def run(
    bib_path:      Path = BIB_PATH,
    internal_path: Path = INTERNAL_PATH,
    output_path:   Path = OUTPUT_PATH,
) -> None:
    if not bib_path.exists():
        print(f"ERROR: {bib_path} not found", file=sys.stderr)
        sys.exit(1)
    if not internal_path.exists():
        print(f"ERROR: {internal_path} not found", file=sys.stderr)
        sys.exit(1)

    print(f"  Reading {bib_path.name}...")
    ext_refs = load_bib(bib_path)

    print(f"  Reading {internal_path.name}...")
    with internal_path.open(encoding="utf-8") as f:
        internal = json.load(f)

    print(f"  Merging ({len(ext_refs)} external refs, "
          f"{len(internal['internal_papers'])} papers, "
          f"{len(internal['citations'])} citations, "
          f"{len(internal['flags'])} flags)...")

    result = merge(ext_refs, internal)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"  ✓ {output_path.name} written ({len(ext_refs)} external refs)")


if __name__ == "__main__":
    run()
