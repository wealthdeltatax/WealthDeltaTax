"""
scrape_contents.py — WDT pipeline utility
==========================================
Scans source/*.md and keeps registry/contents.yml representative of the
headings actually in the papers.

contents.yml feeds build_anchors.py, which feeds every (PAPER §N) link target,
so a stale entry here becomes a wrong anchor downstream.

Run modes
---------
  --report   (default)  Summarise what differs between the headings and
                        contents.yml, per paper. Writes nothing.
  --dry-run             Show the YAML diff that --write would produce.
  --write               Sync contents.yml to the headings (see "Sync rules").

Options
-------
  SHORTCODE ...         Limit to these papers (default: all in papers.yml).
  --additive            Legacy behaviour: add missing keys only; never update
                        a title or remove a key.
  --suggest-map PATH    Write PAPER§OLD: PAPER§NEW lines for sections whose
                        number changed but whose title did not. A starting
                        point for `wdt_crosslinks.py remap`; review before use.
  --verbose             Also list every clean entry.

Sync rules (default mode)
-------------------------
For each paper being synced, `sections` is rebuilt in document order:
  - A heading's key and title are taken from the heading itself.
  - Key in headings, not in contents.yml  -> added.
  - Key in both, titles differ            -> contents.yml title replaced.
  - Key in contents.yml, not in headings  -> removed.
  - Heading contains math ($...$)         -> existing contents.yml title is
        KEPT. Anchors depend on the title text, and math headings need a
        hand-written plain-text title (e.g. "tau 0 = 10%"). A math heading
        with no existing entry is added with its raw text and flagged.
  - Paper has edge-case headings (no parseable key): stale keys that an edge
        heading could own are kept and flagged, not removed. An edge h1 can
        own only undotted keys; an edge h2+ can own any key. Resolve the edge
        case, then re-run.
  - Duplicate section number in one paper: that paper is NOT synced (error,
        exit code 1). Fix the heading first.
  - `page` and `title` of a paper entry are only set when missing.
  - Papers in contents.yml but not in papers.yml are left untouched.

Heading parsing
---------------
Front matter and fenced code blocks are skipped. Levels 1-6 are read.

CLEAN — key extracted automatically:
  # 1. Introduction          ->  "1"    : Introduction
  # A. Chambers {.appendix}  ->  "A"    : Chambers
  # J The Deferred Delta     ->  "J"    : The Deferred Delta   (J-Z, no dot)
  ## 1.1 The Tax Base        ->  "1.1"  : The Tax Base
  ## A.1 Purpose             ->  "A.1"  : Purpose
  ### 3.4.1 Detail           ->  "3.4.1": Detail

SKIPPED — never written:
  Any heading with {.unnumbered} or {.unlisted}; Abstract, Glossary, etc.

EDGE CASE — reported, needs a manual decision:
  # Prose title {.appendix}  — appendix h1 with no letter prefix
  Any other heading with no numeric/letter prefix.

Parsing is kept aligned with wdt_crosslinks.py so both tools see the same
section index. If they disagree, trust neither until you know why.
"""

import argparse
import difflib
import re
import sys
from collections import defaultdict
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
    level: int
    raw: str
    key: str | None
    title: str | None
    is_skip: bool = False
    is_edge: bool = False
    edge_reason: str = ""

    @property
    def has_math(self) -> bool:
        return "$" in self.raw


@dataclass
class PaperResult:
    shortcode: str
    source_file: Path | None
    front_matter_title: str | None
    clean: list[HeadingEntry] = field(default_factory=list)
    edge: list[HeadingEntry] = field(default_factory=list)
    skipped: list[HeadingEntry] = field(default_factory=list)


@dataclass
class Plan:
    shortcode: str
    new_sections: dict = field(default_factory=dict)
    added: list = field(default_factory=list)        # (key, title)
    retitled: list = field(default_factory=list)     # (key, old, new)
    removed: list = field(default_factory=list)      # (key, title)
    renumbered: list = field(default_factory=list)   # (old_key, new_key, title)
    added_math: list = field(default_factory=list)   # keys needing a hand-written title
    math_kept: int = 0
    retained: list = field(default_factory=list)     # stale keys kept because of edge cases
    blocked: str | None = None

    @property
    def n_changes(self) -> int:
        return (len(self.added) + len(self.retitled) + len(self.removed)
                + len(self.renumbered))

# ---------------------------------------------------------------------------
# Regexes
# ---------------------------------------------------------------------------

RE_ATTRS      = re.compile(r"\s*\{[^}]*\}")
RE_UNNUMBERED = re.compile(r"\{[^}]*(unnumbered|unlisted)[^}]*\}", re.I)
RE_FRONT      = re.compile(r"^---\s*\n(.*?)\n---[ \t]*(?:\n|$)", re.DOTALL)

# Priority order matters — more specific first.
RE_LETTER_DOT_NUM = re.compile(r"^([A-Z]\.\d+(?:\.\d+)*)\s+(.*)")   # A.1, A.4.4.1
RE_NUM_DOTTED     = re.compile(r"^(\d+(?:\.\d+)+)\s+(.*)")           # 1.1, 3.4.1
RE_NUM_DOT        = re.compile(r"^(\d+)\.\s+(.*)")                   # 1. Title
RE_LETTER_DOT     = re.compile(r"^([A-Z])\.\s+(.*)")                 # A. Title
RE_LETTER_NUM_SUB = re.compile(r"^([A-Z]\d+(?:\.\d+)*)\s+(.*)")      # A1.2
RE_LETTER_BARE    = re.compile(r"^([J-Z])\s+(.*)")                   # J Title (VAL.B style)

SKIP_TEXTS = {
    "abstract", "glossary", "internal bibliography",
    "revision history", "keywords", "author disclosure",
}

# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def strip_attrs(text: str) -> str:
    return RE_ATTRS.sub("", text).strip()


def parse_headings(md_text: str):
    """Return (front_matter_title, shortcode, list[HeadingEntry])."""
    fm_title = fm_shortcode = None
    body = md_text
    fm = RE_FRONT.match(md_text)
    if fm:
        block = fm.group(1)
        t = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', block, re.M)
        if t:
            fm_title = t.group(1).strip().strip("\"'")
        s = re.search(r'^shortcode:\s*["\']?(.+?)["\']?\s*$', block, re.M)
        if s:
            fm_shortcode = s.group(1).strip().strip("\"'")
        body = md_text[fm.end():]

    entries: list[HeadingEntry] = []
    in_fence = False
    for line in body.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if not m:
            continue
        level, raw = len(m.group(1)), m.group(2).strip()

        if RE_UNNUMBERED.search(raw):
            entries.append(HeadingEntry(level, raw, None, None, is_skip=True))
            continue
        cleaned = strip_attrs(raw)
        if cleaned.lower() in SKIP_TEXTS:
            entries.append(HeadingEntry(level, raw, None, None, is_skip=True))
            continue

        key, title = _extract_key(cleaned)
        if key is not None:
            entries.append(HeadingEntry(level, raw, key, title))
        else:
            entries.append(HeadingEntry(level, raw, None, cleaned, is_edge=True,
                                        edge_reason=_edge_reason(level, raw)))
    return fm_title, fm_shortcode, entries


def _extract_key(text: str):
    for pat in (RE_LETTER_DOT_NUM, RE_NUM_DOTTED, RE_NUM_DOT, RE_LETTER_DOT,
                RE_LETTER_NUM_SUB, RE_LETTER_BARE):
        m = pat.match(text)
        if m:
            return m.group(1), strip_attrs(m.group(2).strip())
    return None, None


def _edge_reason(level: int, raw: str) -> str:
    if level == 1:
        if re.search(r"\{[^}]*appendix[^}]*\}", raw, re.I):
            return "appendix h1 with no letter prefix: key must be set by hand"
        return "prose h1 with no numeric/letter prefix"
    return f"h{level} with no recognised key prefix"

# ---------------------------------------------------------------------------
# papers.yml / source loading
# ---------------------------------------------------------------------------

def load_papers() -> list[dict]:
    if not PAPERS_YML.exists():
        sys.exit(f"ERROR: {PAPERS_YML} not found.")
    with PAPERS_YML.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, list):
        sys.exit(f"ERROR: {PAPERS_YML} should be a YAML list.")
    return data


def resolve_source(source_name: str) -> Path | None:
    path = SOURCE_DIR / source_name
    return path if path.exists() else None


def classify(entries):
    clean, edge, skipped = [], [], []
    for e in entries:
        (skipped if e.is_skip else edge if e.is_edge else clean).append(e)
    return clean, edge, skipped

# ---------------------------------------------------------------------------
# contents.yml load / dump
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

# ---------------------------------------------------------------------------
# Planning: compare headings with contents.yml
# ---------------------------------------------------------------------------

def norm(t: str) -> str:
    return re.sub(r"\s+", " ", str(t)).strip().casefold()


def plan_paper(r: PaperResult, old: dict, additive: bool) -> Plan:
    p = Plan(r.shortcode)
    old = {str(k): str(v) for k, v in (old or {}).items()}

    keys = [e.key for e in r.clean]
    dupes = sorted({k for k in keys if keys.count(k) > 1})
    if dupes:
        p.blocked = "duplicate section number(s): " + ", ".join(dupes)
        p.new_sections = dict(old)
        return p

    new: dict = {}
    for e in r.clean:
        if e.key in old:
            if e.has_math:
                new[e.key] = old[e.key]
                p.math_kept += 1
            elif additive:
                new[e.key] = old[e.key]
            else:
                new[e.key] = e.title
                if norm(old[e.key]) != norm(e.title):
                    p.retitled.append((e.key, old[e.key], e.title))
        else:
            new[e.key] = e.title
            p.added.append((e.key, e.title))
            if e.has_math:
                p.added_math.append(e.key)

    scraped = set(new)
    stale = [k for k in old if k not in scraped]
    if additive:
        protected = stale
    elif r.edge:
        owns_any = any(e.level > 1 for e in r.edge)
        protected = stale if owns_any else [k for k in stale if "." not in k]
    else:
        protected = []
    for k in protected:
        new[k] = old[k]
    p.retained = protected
    if not additive:
        p.removed = [(k, old[k]) for k in stale if k not in protected]

    # Renumbering: same title (unique on both sides) under a different key.
    rm, ad = defaultdict(list), defaultdict(list)
    for k, t in p.removed:
        rm[norm(t)].append(k)
    for k, t in p.added:
        ad[norm(t)].append(k)
    for t, olds in rm.items():
        if len(olds) == 1 and len(ad.get(t, [])) == 1:
            ok, nk = olds[0], ad[t][0]
            title = next(x for k, x in p.removed if k == ok)
            p.renumbered.append((ok, nk, title))
    moved_old = {o for o, _, _ in p.renumbered}
    moved_new = {n for _, n, _ in p.renumbered}
    p.removed = [(k, t) for k, t in p.removed if k not in moved_old]
    p.added = [(k, t) for k, t in p.added if k not in moved_new]

    p.new_sections = new
    return p

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def print_report(results, plans, contents, verbose, scoped):
    for r in results:
        print(f"\n{'=' * 64}")
        if r.source_file is None:
            print(f"  {r.shortcode}  —  SOURCE FILE NOT FOUND (skipped)")
            continue
        p = plans[r.shortcode]
        state = (f"BLOCKED: {p.blocked}" if p.blocked
                 else "in sync" if p.n_changes == 0 and not p.retained
                 else f"{p.n_changes} change(s)")
        print(f"  {r.shortcode}  —  {r.source_file.name}")
        print(f"  {len(r.clean)} sections | {len(r.edge)} edge | "
              f"{len(r.skipped)} skipped | {state}")
        print(f"{'=' * 64}")

        for k, t in p.added:
            print(f"    +  {k:<10} {t}")
        for k, old, new in p.retitled:
            print(f"    ~  {k:<10} {old!r}  ->  {new!r}")
        for o, n, t in p.renumbered:
            print(f"    >  {o:<10} -> {n:<10} {t}   (renumbered, title unchanged)")
        for k, t in p.removed:
            print(f"    -  {k:<10} {t}")
        if p.added_math:
            print(f"    !  math heading(s) added with raw LaTeX titles; hand-write a "
                  f"plain-text title in contents.yml: {', '.join(p.added_math)}")
        if p.math_kept and verbose:
            print(f"    i  {p.math_kept} math heading(s): existing contents.yml titles kept")
        if p.retained:
            print(f"    !  kept despite no matching heading (paper has edge cases): "
                  f"{', '.join(p.retained)}")
        for e in r.edge:
            print(f"    ?  EDGE [{e.edge_reason}]  {e.raw!r}")
        if verbose:
            for e in r.clean:
                print(f"       {'#' * e.level:<6} {e.key:<10} {e.title}")

    if not scoped:
        listed = {r.shortcode for r in results}
        extra = [k for k in contents if k not in listed]
        if extra:
            print(f"\nNote: in contents.yml but not in papers.yml (left untouched): "
                  f"{', '.join(extra)}")

# ---------------------------------------------------------------------------
# Write
# ---------------------------------------------------------------------------

def apply_plans(results, plans, contents, dry_run):
    old_yaml = dump_yaml(contents)
    new_contents = {k: (dict(v) if isinstance(v, dict) else v) for k, v in contents.items()}

    for r in results:
        if r.source_file is None:
            continue
        p = plans[r.shortcode]
        if p.blocked:
            print(f"\n✗  {r.shortcode} NOT synced: {p.blocked}")
            continue
        entry = new_contents.get(r.shortcode) or {}
        entry.setdefault("page", shortcode_to_page(r.shortcode))
        entry.setdefault("title", r.front_matter_title or r.shortcode)
        entry["sections"] = p.new_sections
        new_contents[r.shortcode] = entry

    new_yaml = dump_yaml(new_contents)

    if dry_run:
        diff = "".join(difflib.unified_diff(
            old_yaml.splitlines(keepends=True), new_yaml.splitlines(keepends=True),
            fromfile="contents.yml (current)", tofile="contents.yml (proposed)", n=2))
        print("\n=== DRY RUN diff ===")
        print(diff or "(no changes)")
    elif new_yaml != old_yaml:
        CONTENTS_YML.write_text(new_yaml, encoding="utf-8")
        print(f"\n✓  Written: {CONTENTS_YML}")
        print("   Next: python pipeline/build_anchors.py, then "
              "python pipeline/wdt_crosslinks.py check --baseline <base.json>")
    else:
        blocked = [c for c, pl in plans.items() if pl.blocked]
        note = f" (except blocked: {', '.join(blocked)})" if blocked else ""
        print(f"\n✓  {CONTENTS_YML} already matches the headings{note}; nothing written.")


def write_suggest_map(path, plans):
    lines = [f"{code}§{o}: {code}§{n}"
             for code, p in plans.items() for o, n, _ in p.renumbered]
    Path(path).write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    print(f"\nSuggested renumber map ({len(lines)} line(s)) -> {path}")
    if lines:
        print("   Title-match only. Review, then: "
              "python pipeline/wdt_crosslinks.py remap --map <file>   (dry run first)")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Sync registry/contents.yml to the headings in source/*.md")
    ap.add_argument("shortcodes", nargs="*", metavar="SHORTCODE",
                    help="Limit to these shortcodes. Default: all.")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--report", action="store_true",
                      help="Summarise differences; write nothing (default).")
    mode.add_argument("--write", action="store_true",
                      help="Sync contents.yml to the headings.")
    mode.add_argument("--dry-run", action="store_true",
                      help="Show the YAML diff --write would produce.")
    ap.add_argument("--additive", action="store_true",
                    help="Legacy: add missing keys only.")
    ap.add_argument("--suggest-map", metavar="PATH",
                    help="Write suggested renumber map for wdt_crosslinks remap.")
    ap.add_argument("--verbose", action="store_true", help="List every clean entry.")
    args = ap.parse_args()

    filter_set = set(args.shortcodes) if args.shortcodes else None
    contents = load_contents()
    results: list[PaperResult] = []

    for paper in load_papers():
        name = paper["source"]
        src = resolve_source(name)
        if src is None:
            if not filter_set:
                results.append(PaperResult(name, None, None))
            continue
        fm_title, fm_code, entries = parse_headings(src.read_text(encoding="utf-8"))
        if not fm_code:
            print(f"  ! {name}: no shortcode in front matter — skipping")
            continue
        if filter_set and fm_code not in filter_set:
            continue
        clean, edge, skipped = classify(entries)
        results.append(PaperResult(fm_code, src, fm_title, clean, edge, skipped))

    plans = {}
    for r in results:
        if r.source_file is None:
            continue
        old = (contents.get(r.shortcode) or {}).get("sections", {})
        plans[r.shortcode] = plan_paper(r, old, args.additive)

    print_report(results, plans, contents, args.verbose, scoped=bool(filter_set))

    if args.suggest_map:
        write_suggest_map(args.suggest_map, plans)
    if args.write or args.dry_run:
        apply_plans(results, plans, contents, dry_run=args.dry_run)

    sys.exit(1 if any(p.blocked for p in plans.values()) else 0)


if __name__ == "__main__":
    main()
