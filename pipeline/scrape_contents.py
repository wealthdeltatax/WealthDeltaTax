"""
scrape_contents.py — WDT pipeline utility
==========================================
Scans source/*.md files and produces a report of what it found in each file,
split into:
  - CLEAN entries  : unambiguous key + title, ready to write to contents.yml
  - EDGE CASES     : headings that need manual resolution before writing

Run modes
---------
  --report   (default)  Print the full report for each paper; write nothing.
  --write                Write CLEAN entries to contents.yml; flag edge cases
                         in a separate review block at the top of the output.
  --dry-run              Like --write but print the proposed YAML diff instead
                         of touching the file.

Heading parsing rules
---------------------
Uses Markdown level (# / ## / ###) as the primary signal.

CLEAN — key extracted automatically:
  # 1. Introduction          →  "1"  : Introduction
  # 10. Conclusion           →  "10" : Conclusion
  # A. Appendix {.appendix}  →  "A"  : Appendix
  # B. Simulation ...        →  "B"  : Simulation Methodology
  ## 1.1 The Tax Base        →  "1.1": The Tax Base
  ## A.1 Purpose             →  "A.1": Purpose
  ### 3.4.1 Detail           →  "3.4.1": Detail

SKIPPED — never written:
  Any heading with {.unnumbered} or {.unlisted}
  # Abstract   # Glossary   ## Internal Bibliography

EDGE CASE — flagged for manual review:
  # Prose title {.appendix}  — appendix h1 with no letter prefix;
                               key cannot be inferred from this heading alone,
                               but its ##-children may reveal it (reported).
  Any other h1 with no numeric/letter prefix.
"""

import argparse
import glob
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required.  pip install pyyaml --break-system-packages")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT_DIR     = Path(__file__).resolve().parent.parent
SOURCE_DIR   = ROOT_DIR / "source"
REGISTRY_DIR = ROOT_DIR / "registry"
PAPERS_YML   = REGISTRY_DIR / "papers.yml"
CONTENTS_YML = REGISTRY_DIR / "contents.yml"

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class HeadingEntry:
    level: int          # 1, 2, 3 (from # count)
    raw: str            # original heading line text (no leading #s)
    key: str | None     # extracted section key, or None if edge case
    title: str | None   # extracted title text, or None if skipped/edge
    is_skip: bool = False
    is_edge: bool = False
    edge_reason: str = ""

@dataclass
class PaperResult:
    shortcode: str
    source_file: Path | None
    front_matter_title: str | None
    clean: list[HeadingEntry] = field(default_factory=list)
    edge:  list[HeadingEntry] = field(default_factory=list)
    skipped: list[HeadingEntry] = field(default_factory=list)

# ---------------------------------------------------------------------------
# Regexes
# ---------------------------------------------------------------------------

# Strip Quarto class attributes like {.appendix} {.unnumbered .unlisted}
RE_ATTRS      = re.compile(r"\s*\{[^}]*\}")
RE_UNNUMBERED = re.compile(r"\{[^}]*(unnumbered|unlisted)[^}]*\}", re.I)

# Key patterns (applied to cleaned heading text, no attrs)
# Priority order matters — more specific first.
RE_LETTER_DOT_NUM = re.compile(r"^([A-Z]\.\d+(?:\.\d+)*)\s+(.*)")   # A.1, A.4.4.1
RE_NUM_DOTTED     = re.compile(r"^(\d+(?:\.\d+)+)\s+(.*)")           # 1.1, 3.4.1
RE_NUM_DOT        = re.compile(r"^(\d+)\.\s+(.*)")                   # 1. Title  (top-level numeric)
RE_LETTER_DOT     = re.compile(r"^([A-Z])\.\s+(.*)")                 # A. Title
RE_LETTER_NUM_SUB = re.compile(r"^([A-Z]\d+(?:\.\d+)*)\s+(.*)")     # A1.2 (uncommon but safe)

SKIP_TEXTS = {
    "abstract", "glossary", "internal bibliography",
    "revision history", "keywords", "author disclosure",
}

# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def strip_attrs(text: str) -> str:
    return RE_ATTRS.sub("", text).strip()

def parse_headings(md_text: str) -> tuple[str | None, list[HeadingEntry]]:
    """Return (front_matter_title, list[HeadingEntry])."""
    entries: list[HeadingEntry] = []

    # Extract YAML front matter title if present
    fm_title: str | None = None
    fm_match = re.match(r"^---\s*\n(.*?)\n---", md_text, re.DOTALL)
    if fm_match:
        fm_block = fm_match.group(1)
        t = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', fm_block, re.M)
        if t:
            fm_title = t.group(1).strip().strip('"\'')

    for line in md_text.splitlines():
        m = re.match(r"^(#{1,4})\s+(.*)", line)
        if not m:
            continue
        level = len(m.group(1))
        raw   = m.group(2).strip()

        # --- SKIP: unnumbered/unlisted ---
        if RE_UNNUMBERED.search(raw):
            entries.append(HeadingEntry(level=level, raw=raw, key=None, title=None, is_skip=True))
            continue

        cleaned = strip_attrs(raw)

        # --- SKIP: known prose-only titles ---
        if cleaned.lower() in SKIP_TEXTS:
            entries.append(HeadingEntry(level=level, raw=raw, key=None, title=None, is_skip=True))
            continue

        # --- Try key patterns ---
        key, title = _extract_key(cleaned)

        if key is not None:
            entries.append(HeadingEntry(level=level, raw=raw, key=key, title=title))
        else:
            # Edge case: no key found
            reason = _edge_reason(level, cleaned)
            entries.append(HeadingEntry(
                level=level, raw=raw, key=None, title=cleaned,
                is_edge=True, edge_reason=reason,
            ))

    return fm_title, entries


def _extract_key(text: str) -> tuple[str | None, str | None]:
    """Try each pattern in priority order. Return (key, title) or (None, None)."""
    for pat in (RE_LETTER_DOT_NUM, RE_NUM_DOTTED, RE_NUM_DOT,
                RE_LETTER_DOT, RE_LETTER_NUM_SUB):
        m = pat.match(text)
        if m:
            return m.group(1), strip_attrs(m.group(2).strip())
    return None, None


def _edge_reason(level: int, text: str) -> str:
    if level == 1:
        if "{.appendix}" in text or re.search(r"\{[^}]*appendix[^}]*\}", text, re.I):
            return "appendix h1 with no letter prefix — key must be inferred from children"
        return "prose h1 with no numeric/letter prefix"
    return f"h{level} with no recognised key prefix"

# ---------------------------------------------------------------------------
# papers.yml loader
# ---------------------------------------------------------------------------

def load_papers() -> list[dict]:
    if not PAPERS_YML.exists():
        sys.exit(f"ERROR: {PAPERS_YML} not found.")
    with PAPERS_YML.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, list):
        sys.exit(f"ERROR: {PAPERS_YML} should be a YAML list.")
    return data

def resolve_source(glob_pat: str) -> Path | None:
    matches = glob.glob(str(SOURCE_DIR / glob_pat))
    if not matches:
        return None
    if len(matches) > 1:
        print(f"  WARNING: multiple matches for '{glob_pat}', using {Path(matches[0]).name}")
    return Path(matches[0])

# ---------------------------------------------------------------------------
# Classify headings into clean / edge / skipped
# ---------------------------------------------------------------------------

def classify(fm_title: str | None, entries: list[HeadingEntry]) -> tuple[
        list[HeadingEntry], list[HeadingEntry], list[HeadingEntry]]:
    clean, edge, skipped = [], [], []
    for e in entries:
        if e.is_skip:
            skipped.append(e)
        elif e.is_edge:
            edge.append(e)
        else:
            clean.append(e)
    return clean, edge, skipped

# ---------------------------------------------------------------------------
# Report printer
# ---------------------------------------------------------------------------

def print_report(results: list[PaperResult]) -> None:
    edge_summary: list[tuple[str, HeadingEntry]] = []

    for r in results:
        if r.source_file is None:
            print(f"\n{'='*60}")
            print(f"  {r.shortcode}  —  SOURCE FILE NOT FOUND")
            print(f"{'='*60}")
            continue

        total_edge  = len(r.edge)
        total_clean = len(r.clean)

        print(f"\n{'='*60}")
        print(f"  {r.shortcode}  —  {r.source_file.name}")
        if r.front_matter_title:
            print(f"  Front-matter title: \"{r.front_matter_title}\"")
        print(f"  {total_clean} clean  |  {total_edge} edge cases  |  {len(r.skipped)} skipped")
        print(f"{'='*60}")

        if r.clean:
            print("\n  CLEAN (will be written):")
            for e in r.clean:
                level_str = "#" * e.level
                print(f"    {level_str:<4}  key={e.key!r:<12}  title={e.title!r}")

        if r.edge:
            print("\n  EDGE CASES (need manual resolution):")
            for e in r.edge:
                level_str = "#" * e.level
                print(f"    {level_str:<4}  [{e.edge_reason}]")
                print(f"          raw:  {e.raw!r}")
                edge_summary.append((r.shortcode, e))

        if r.skipped:
            print(f"\n  SKIPPED ({len(r.skipped)} unnumbered/prose headings — not shown)")

    # Global edge case summary at the end
    if edge_summary:
        print(f"\n\n{'#'*60}")
        print(f"  EDGE CASE SUMMARY  ({len(edge_summary)} total)")
        print(f"{'#'*60}")
        print("  These need manual resolution in contents.yml:\n")
        for shortcode, e in edge_summary:
            print(f"  [{shortcode}]  {e.edge_reason}")
            print(f"    Raw heading:  {e.raw!r}")
            print()

# ---------------------------------------------------------------------------
# contents.yml load / write
# ---------------------------------------------------------------------------

def load_contents() -> dict:
    if not CONTENTS_YML.exists():
        return {}
    with CONTENTS_YML.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def shortcode_to_page(shortcode: str) -> str:
    return shortcode.lower().replace(".", "-") + ".html"

class _QuotedStr(str):
    pass

def _q_repr(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style='"')
yaml.add_representer(_QuotedStr, _q_repr)

def _needs_quoting(s: str) -> bool:
    return bool(re.match(r'^[{\[&*!|>\'"%@`]', s)) or ": " in s or s.endswith(":")

def _prep(obj):
    if isinstance(obj, dict):
        return {k: _prep(v) for k, v in obj.items()}
    if isinstance(obj, str) and _needs_quoting(obj):
        return _QuotedStr(obj)
    return obj

def dump_yaml(contents: dict) -> str:
    return yaml.dump(_prep(contents), allow_unicode=True,
                     default_flow_style=False, sort_keys=False, width=120)

def write_clean(results: list[PaperResult], dry_run: bool) -> None:
    contents = load_contents()
    old_yaml = dump_yaml(contents)

    for r in results:
        if not r.clean and r.source_file is not None:
            continue
        if r.source_file is None:
            continue

        shortcode = r.shortcode
        entry = contents.get(shortcode, {})

        if "page" not in entry:
            entry["page"] = shortcode_to_page(shortcode)
        if "title" not in entry:
            entry["title"] = r.front_matter_title or shortcode

        existing_sections = entry.get("sections", {})
        merged = dict(existing_sections)  # preserve existing
        for e in r.clean:
            if e.key not in merged:          # don't clobber manual overrides
                merged[e.key] = e.title
        entry["sections"] = merged
        contents[shortcode] = entry

    new_yaml = dump_yaml(contents)

    # Edge case notice
    all_edge = [(r.shortcode, e) for r in results for e in r.edge]
    if all_edge:
        print(f"\n⚠  {len(all_edge)} edge case(s) NOT written — manual action required:")
        for shortcode, e in all_edge:
            print(f"   [{shortcode}]  {e.raw!r}  →  {e.edge_reason}")

    if dry_run:
        import difflib
        diff = "".join(difflib.unified_diff(
            old_yaml.splitlines(keepends=True),
            new_yaml.splitlines(keepends=True),
            fromfile="contents.yml (current)",
            tofile="contents.yml (proposed)",
            n=3,
        ))
        print("\n=== DRY RUN diff ===")
        print(diff or "(no changes)")
    else:
        CONTENTS_YML.write_text(new_yaml, encoding="utf-8")
        if new_yaml != old_yaml:
            print(f"\n✓  Written: {CONTENTS_YML}")
            print("   Run  python pipeline/build_anchors.py  to regenerate anchors.yml")
        else:
            print(f"\n✓  {CONTENTS_YML} is already up to date — no changes written.")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Scrape .md headings and report / update contents.yml"
    )
    parser.add_argument("shortcodes", nargs="*", metavar="SHORTCODE",
                        help="Limit to these shortcodes. Default: all.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--report",  action="store_true",
                      help="Print report only (default if no mode given).")
    mode.add_argument("--write",   action="store_true",
                      help="Write clean entries to contents.yml.")
    mode.add_argument("--dry-run", action="store_true",
                      help="Show what --write would change without writing.")
    args = parser.parse_args()

    # Default mode is --report
    if not args.write and not args.dry_run:
        args.report = True

    papers = load_papers()
    filter_set = set(args.shortcodes) if args.shortcodes else None

    results: list[PaperResult] = []

    for paper in papers:
        shortcode = paper["shortcode"]
        if filter_set and shortcode not in filter_set:
            continue

        src = resolve_source(paper["source_glob"])
        if src is None:
            results.append(PaperResult(shortcode=shortcode, source_file=None,
                                       front_matter_title=None))
            continue

        text = src.read_text(encoding="utf-8")
        fm_title, entries = parse_headings(text)
        clean, edge, skipped = classify(fm_title, entries)

        results.append(PaperResult(
            shortcode=shortcode,
            source_file=src,
            front_matter_title=fm_title,
            clean=clean,
            edge=edge,
            skipped=skipped,
        ))

    if args.report:
        print_report(results)
    else:
        print_report(results)
        write_clean(results, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
