#!/usr/bin/env python3
"""
build_glossary.py  (v2)

For each WDT markdown paper in --papers:
  1. Locate the paper's own # Glossary section (if present)
  2. Extract term + definition pairs from that section ONLY
  3. Deduplicate across papers (longer definition wins)
  4. For every term, search every section of every paper for mentions
  5. Attach cross-reference links  (PAPER §section)  to each entry
  6. Output a combined alphabetical master glossary

No seed file. No scraping of non-glossary bold text.

Usage:
    python build_glossary.py --papers /path/to/papers --contents contents.yml --out glossary.md
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_md(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")


def load_contents(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def normalise(s: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace — for fuzzy matching."""
    s = s.lower()
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


# ---------------------------------------------------------------------------
# 1. Map a markdown file to its paper code via YAML front-matter title
# ---------------------------------------------------------------------------

FRONTMATTER_TITLE_RE = re.compile(r'^title:\s*["\']?(.+?)["\']?\s*$', re.MULTILINE)


def md_to_paper_code(md_text: str, contents: dict) -> str | None:
    title_lookup = {normalise(str(v.get("title", ""))): code
                    for code, v in contents.items() if v.get("title")}
    m = FRONTMATTER_TITLE_RE.search(md_text[:2000])
    if not m:
        return None
    doc_title = m.group(1).strip().strip('"\'')
    doc_norm = normalise(doc_title)
    # Exact match first
    if doc_norm in title_lookup:
        return title_lookup[doc_norm]
    # Partial match
    for t, code in title_lookup.items():
        if t and (t in doc_norm or doc_norm in t):
            return code
    return None


# ---------------------------------------------------------------------------
# 2. Extract glossary entries from a paper's # Glossary section ONLY
# ---------------------------------------------------------------------------

GLOSS_HEADING_RE = re.compile(
    r'^(#{1,6})\s+Glossary(?:\s*\{[^}]*\})?\s*$', re.MULTILINE | re.IGNORECASE
)
# **Term:** or **Term** at line start
TERM_LINE_RE = re.compile(r'^\*\*(.+?)\*\*[:\s]*(.*)')


def extract_glossary_entries(md_text: str) -> list[dict]:
    """
    Returns [{"term": str, "definition": str}, ...]
    Only reads within the paper's Glossary heading block.
    Returns [] if no Glossary heading found.
    """
    m = GLOSS_HEADING_RE.search(md_text)
    if not m:
        return []

    gloss_start = m.end()
    heading_level = len(m.group(1))  # number of # chars

    # Find where the glossary section ends: next heading at same or higher level
    next_heading_re = re.compile(
        r'^#{1,' + str(heading_level) + r'}\s', re.MULTILINE
    )
    nm = next_heading_re.search(md_text, gloss_start)
    gloss_end = nm.start() if nm else len(md_text)
    gloss_text = md_text[gloss_start:gloss_end]

    entries = []
    current_term = None
    current_def_lines = []

    def flush():
        if current_term is not None:
            defn = " ".join(current_def_lines).strip()
            # Strip trailing cross-link arrows already in source
            defn = re.sub(r'\s*→\s*[\(\[].*', '', defn).strip()
            # Strip LaTeX commands (e.g. \newpage )
            defn = re.sub(r'\\[a-zA-Z]+\*?(\{[^}]*\})?', '', defn).strip()
            entries.append({"term": current_term, "definition": defn})

    for line in gloss_text.splitlines():
        tm = TERM_LINE_RE.match(line.strip())
        if tm:
            flush()
            current_term = tm.group(1).strip().rstrip(":")
            inline_def = tm.group(2).strip()
            current_def_lines = [inline_def] if inline_def else []
        elif current_term is not None:
            stripped = line.strip()
            # Skip blank separators, horizontal rules, and pure LaTeX lines
            if stripped and not stripped.startswith('---') and not re.match(r'^\\[a-zA-Z]', stripped):
                current_def_lines.append(stripped)

    flush()
    return entries


# ---------------------------------------------------------------------------
# 3. Parse a paper into sections (for cross-reference search)
# ---------------------------------------------------------------------------

HEADING_RE = re.compile(r'^(#{1,6})\s+(.+?)(?:\s*\{[^}]*\})?\s*$', re.MULTILINE)
SECTION_PREFIX_RE = re.compile(r'^[0-9A-Za-z]+(?:\.[0-9A-Za-z]+)*\.?\s+')


def parse_sections(md_text: str) -> list[dict]:
    matches = list(HEADING_RE.finditer(md_text))
    sections = []
    for i, m in enumerate(matches):
        sections.append({
            "level": len(m.group(1)),
            "raw_title": m.group(2).strip(),
            "start": m.start(),
        })
    sections.insert(0, {"level": 0, "raw_title": "__preamble__", "start": 0})
    return sections


def build_section_lookup(paper_code: str, contents: dict) -> dict[str, str]:
    paper_data = contents.get(paper_code, {})
    lookup = {}
    for num, title in paper_data.get("sections", {}).items():
        lookup[normalise(str(title))] = str(num)
    return lookup


def resolve_section_number(raw_title: str, lookup: dict) -> str | None:
    for candidate in [
        raw_title,
        SECTION_PREFIX_RE.sub("", raw_title).strip(),
        re.sub(r'\s*\{[^}]*\}', '', raw_title).strip(),
        SECTION_PREFIX_RE.sub("", re.sub(r'\s*\{[^}]*\}', '', raw_title).strip()).strip(),
    ]:
        result = lookup.get(normalise(candidate))
        if result:
            return result
    return None


# ---------------------------------------------------------------------------
# 4. Search every section of a paper for a term, return cross-ref strings
# ---------------------------------------------------------------------------

def term_variants(term: str) -> list[str]:
    """
    Generate search variants for a term:
    - Strip any trailing colon (glossary format artefact)
    - Exact term, all-lowercase, sentence-case (first letter lower)
    - If acronym present in parentheses: the acronym itself + base phrase without it
    - Naive plural (append 's') of each of the above
    """
    # Strip trailing colon — glossary entries are stored as "Term:" in source
    term = term.rstrip(":")

    variants = {term, term.lower()}

    # Sentence-case: lowercase just the first character
    # Handles terms used mid-sentence where the leading capital is dropped
    if term and term[0].isupper():
        variants.add(term[0].lower() + term[1:])

    # Acronym in parentheses e.g. "Sovereign Wealth Fund (SWF)" → add "SWF", "swf", base phrase
    acro = re.search(r'\(([A-Z]{2,})\)', term)
    if acro:
        a = acro.group(1)
        variants.update([a, a.lower()])
        base = re.sub(r'\s*\([A-Z]+\)', '', term).strip()
        variants.update([base, base.lower(), base[0].lower() + base[1:] if base else ""])

    # Naive plural of every current variant
    for v in list(variants):
        if v:
            variants.add(v + 's')

    return [v for v in variants if v]  # drop any empty strings


def find_term_in_sections(term: str, paper_code: str, md_text: str, contents: dict) -> list[str]:
    lookup = build_section_lookup(paper_code, contents)
    sections = parse_sections(md_text)
    variants_lower = [v.lower() for v in term_variants(term)]

    # Resolve section numbers with character positions
    resolved = []
    for i, sec in enumerate(sections):
        if sec["raw_title"] == "__preamble__":
            continue
        num = resolve_section_number(sec["raw_title"], lookup)
        if num is None:
            continue
        body_start = sec["start"]
        body_end = sections[i + 1]["start"] if i + 1 < len(sections) else len(md_text)
        resolved.append((num, body_start, body_end))

    if not resolved:
        return []

    def depth(num_str: str) -> int:
        return num_str.count(".") + 1

    md_lower = md_text.lower()
    hits = []
    seen = set()

    for i, (num, start, _) in enumerate(resolved):
        # Scope = from this section's start to the start of the next
        # section at same or shallower depth (includes all nested subsections)
        end = len(md_text)
        for j in range(i + 1, len(resolved)):
            if depth(resolved[j][0]) <= depth(num):
                end = resolved[j][1]
                break
        scope = md_lower[start:end]
        if any(v in scope for v in variants_lower) and num not in seen:
            seen.add(num)
            hits.append(f"({paper_code} \u00a7{num})")

    return hits


# ---------------------------------------------------------------------------
# 5. Main
# ---------------------------------------------------------------------------

def build_glossary(papers_dir: str, contents_path: str, out_path: str):
    contents = load_contents(contents_path)
    md_files = sorted(Path(papers_dir).glob("*.md"))

    if not md_files:
        print(f"No .md files found in {papers_dir}", file=sys.stderr)
        sys.exit(1)

    # Step 1: collect glossary entries from each paper's Glossary section
    all_entries: dict[str, dict] = {}   # normalised_term -> {term, definition}

    for md_file in md_files:
        md_text = read_md(md_file)
        paper_code = md_to_paper_code(md_text, contents)
        entries = extract_glossary_entries(md_text)
        if not entries:
            print(f"  [glossary] {md_file.name}: no Glossary section found", file=sys.stderr)
            continue
        print(f"  [glossary] {md_file.name} ({paper_code}): {len(entries)} entries", file=sys.stderr)
        for entry in entries:
            key = normalise(entry["term"])
            if key not in all_entries:
                all_entries[key] = {"term": entry["term"], "definition": entry["definition"]}
            elif len(entry["definition"]) > len(all_entries[key]["definition"]):
                # Prefer longer / richer definition
                all_entries[key]["definition"] = entry["definition"]

    print(f"\nTotal unique glossary terms: {len(all_entries)}", file=sys.stderr)

    # Step 2: search every paper for every term
    term_xrefs: dict[str, list[str]] = defaultdict(list)

    for md_file in md_files:
        md_text = read_md(md_file)
        paper_code = md_to_paper_code(md_text, contents)
        if paper_code is None:
            print(f"  [search] {md_file.name}: no paper code — skipping", file=sys.stderr)
            continue
        print(f"  [search] {md_file.name} ({paper_code})", file=sys.stderr)
        for key, entry in all_entries.items():
            hits = find_term_in_sections(entry["term"], paper_code, md_text, contents)
            term_xrefs[key].extend(hits)

    # Step 3: deduplicate cross-refs
    for key in term_xrefs:
        seen: set[str] = set()
        deduped = []
        for ref in term_xrefs[key]:
            if ref not in seen:
                seen.add(ref)
                deduped.append(ref)
        term_xrefs[key] = deduped

    # Step 4: render
    sorted_keys = sorted(all_entries.keys(), key=lambda k: all_entries[k]["term"].lstrip("$").lower())

    # Build the set of first letters that actually appear, for the jump bar
    first_letters: list[str] = []
    seen_letters: set[str] = set()
    for key in sorted_keys:
        term = all_entries[key]["term"].lstrip("$")
        fl = term[0].upper() if term else ""
        if fl and fl.isalpha() and fl not in seen_letters:
            first_letters.append(fl)
            seen_letters.add(fl)

    # Build jump bar HTML — only letters that have entries get links
    jump_links = " &nbsp; ".join(
        f'<a href="#glossary-{letter.lower()}">{letter}</a>'
        for letter in first_letters
    )
    jump_bar = (
        "\n```{=html}\n"
        '<div class="wdt-glossary-jumpbar">\n'
        f"{jump_links}\n"
        "</div>\n"
        "```\n"
    )

    lines = [
        "---",
        'title: "Glossary"',
        'description: "Definitions of key terms used across the Wealth Delta Tax research programme."',
        "---",
        "",
        "This glossary defines terms that recur across the WDT paper series. "
        "Each entry links to every section where the term appears.",
        "",
        jump_bar,
        "",
        "---",
        "",
    ]

    current_letter = ""
    for key in sorted_keys:
        entry = all_entries[key]
        term = entry["term"]
        defn = entry["definition"]
        xrefs = term_xrefs.get(key, [])

        # Emit a letter heading anchor when the first letter changes
        fl = term.lstrip("$")[0].upper() if term.lstrip("$") else ""
        if fl.isalpha() and fl != current_letter:
            current_letter = fl
            # Raw HTML anchor so Quarto doesn't mangle it
            lines.append(
                f'\n```{{=html}}\n'
                f'<h3 id="glossary-{fl.lower()}" class="wdt-glossary-letter">{fl}</h3>\n'
                f'```\n'
            )

        lines.append(f"**{term}**")
        if defn and xrefs:
            lines.append(f"{defn} \u2192 {', '.join(xrefs)}")
        elif defn:
            lines.append(defn)
        elif xrefs:
            lines.append(f"\u2192 {', '.join(xrefs)}")
        lines.append("")

    Path(out_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"\nGlossary written to {out_path}  ({len(all_entries)} terms)", file=sys.stderr)


# ---------------------------------------------------------------------------
# 6. Registry mode (brief 064s): registry/glossary.yml -> page + lookup file
# ---------------------------------------------------------------------------

REG_FIELDS = ("term", "definition", "owner", "aliases", "source", "status")
REG_STATUSES = ("seeded", "written")
REG_OWNER_TYPES = ("spoke", "hub", "appendix", "standalone")
HOOK_RE = re.compile(r"\{\{\s*[oi]:[^}]*\}\}")
TYPED_FIGURE_RE = re.compile(r"\d+(?:\.\d+)?\s*(?:%|pp\b)")
LOOKUP_SCHEMA = "wdt-glossary/1"


def slugify(term: str) -> str:
    """Anchor on the glossary page: glossary.html#<slug>."""
    return re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")


def _key(s) -> str:
    return str(s).strip().lower()


def load_registry(path) -> list:
    with open(path, "r", encoding="utf-8") as f:
        rows = yaml.safe_load(f)
    return rows if rows is not None else []


def validate_registry(rows, pages, root=None) -> list[str]:
    """Return error strings, each naming the row's term. Empty list means valid."""
    root = Path(root) if root else Path(".")
    page_type = {r.get("id"): r.get("type") for r in pages}
    errors: list[str] = []
    if not isinstance(rows, list):
        return ["registry: top level must be a list of rows"]

    seen_terms: dict[str, str] = {}
    seen_aliases: dict[str, str] = {}      # alias key -> term that owns it
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"row {i + 1}: not a mapping")
            continue
        term = str(row.get("term", f"row {i + 1}")).strip()
        label = f"{term}"
        for f in REG_FIELDS:
            if f not in row:
                errors.append(f"{label}: missing field '{f}'")
        for f in row:
            if f not in REG_FIELDS:
                errors.append(f"{label}: unknown field '{f}'")
        if "term" in row:
            k = _key(row["term"])
            if not k:
                errors.append(f"{label}: empty term")
            elif k in seen_terms:
                errors.append(f"{label}: duplicate term (also row '{seen_terms[k]}')")
            else:
                seen_terms[k] = term

        owner = row.get("owner")
        if "owner" in row:
            if owner not in page_type:
                errors.append(f"{label}: owner '{owner}' is not in pages.yml")
            elif page_type[owner] not in REG_OWNER_TYPES:
                errors.append(f"{label}: owner '{owner}' has type '{page_type[owner]}', which cannot own a definition")

        status = row.get("status")
        if "status" in row and status not in REG_STATUSES:
            errors.append(f"{label}: status '{status}' is not one of {', '.join(REG_STATUSES)}")

        if "source" in row:
            src = row.get("source")
            if status == "seeded" and not src:
                errors.append(f"{label}: seeded row has no source")
            elif src:
                path = str(src).split(",")[0].strip()
                if not (root / path).is_file():
                    errors.append(f"{label}: source file '{path}' does not exist")

        defn = row.get("definition")
        if "definition" in row:
            if not isinstance(defn, str) or not defn.strip():
                errors.append(f"{label}: empty definition")
            elif TYPED_FIGURE_RE.search(HOOK_RE.sub("", defn)):
                errors.append(f"{label}: definition has a typed figure; use a hook")

        aliases = row.get("aliases", [])
        if "aliases" in row:
            if not isinstance(aliases, list):
                errors.append(f"{label}: aliases must be a list")
                aliases = []
            own = _key(row.get("term", ""))
            for a in aliases:
                ak = _key(a)
                if ak == own:
                    errors.append(f"{label}: alias '{a}' equals its own term")
                elif ak in seen_aliases:
                    errors.append(f"{label}: alias '{a}' collides with an alias of '{seen_aliases[ak]}'")
                else:
                    seen_aliases[ak] = term

    # An alias equal to another row's term (any order of rows).
    for ak, owner_term in seen_aliases.items():
        if ak in seen_terms and seen_terms[ak] != owner_term:
            errors.append(f"{owner_term}: alias '{ak}' collides with the term '{seen_terms[ak]}'")
    return errors


def page_links(pages) -> dict:
    """page id -> (label, url) for the "Defined on" link."""
    out = {}
    for r in pages:
        label = r.get("label") or r.get("title") or r.get("id")
        out[r.get("id")] = (str(label), str(r.get("url", "")))
    return out


def build_lookup(rows) -> dict:
    terms = [
        {"term": r["term"], "owner": r["owner"], "aliases": list(r.get("aliases") or []), "slug": slugify(r["term"])}
        for r in sorted(rows, key=lambda r: r["term"].lstrip("$").lower())
    ]
    return {"schema": LOOKUP_SCHEMA, "terms": terms}


def render_registry_page(rows, pages, xrefs=None) -> str:
    """The glossary page, in the legacy front matter and entry markup. xrefs: term -> list of strings, or None."""
    links = page_links(pages)
    ordered = sorted(rows, key=lambda r: r["term"].lstrip("$").lower())

    letters: list[str] = []
    for r in ordered:
        t = r["term"].lstrip("$")
        fl = t[0].upper() if t else ""
        if fl.isalpha() and fl not in letters:
            letters.append(fl)
    jump_links = " &nbsp; ".join(f'<a href="#glossary-{l.lower()}">{l}</a>' for l in letters)

    lines = [
        "---",
        'title: "Glossary"',
        'description: "Definitions of key terms used across the Wealth Delta Tax research programme."',
        "---",
        "",
        "This glossary defines terms that recur across the WDT pages. Each entry links to the page that defines it."
        + ("" if xrefs is not None else " Lists of the pages that use each term are not built yet."),
        "",
        "\n```{=html}\n"
        '<div class="wdt-glossary-jumpbar">\n'
        f"{jump_links}\n"
        "</div>\n"
        "```\n",
        "",
        "---",
        "",
    ]
    current = ""
    for r in ordered:
        term, defn = r["term"], r["definition"].strip()
        t = term.lstrip("$")
        fl = t[0].upper() if t else ""
        if fl.isalpha() and fl != current:
            current = fl
            lines.append(
                f'\n```{{=html}}\n<h3 id="glossary-{fl.lower()}" class="wdt-glossary-letter">{fl}</h3>\n```\n'
            )
        label, url = links[r["owner"]]
        lines.append(f"::: {{#{slugify(term)} .wdt-glossary-entry}}")
        lines.append(f"**{term}**")
        lines.append("")
        lines.append(defn)
        lines.append("")
        lines.append(f"Defined on [{label}]({url})")
        if xrefs and xrefs.get(term):
            lines.append("")
            lines.append("Used in " + ", ".join(xrefs[term]))
        lines.append(":::")
        lines.append("")
    return "\n".join(lines)


def build_registry(registry_path, pages_path, out_path, lookup_path=None,
                   papers_dir=None, contents_path=None) -> int:
    rows = load_registry(registry_path)
    with open(pages_path, "r", encoding="utf-8") as f:
        pages = yaml.safe_load(f)
    errors = validate_registry(rows, pages, root=Path(registry_path).resolve().parent.parent)
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        return 1

    xrefs = None
    if papers_dir and contents_path:
        contents = load_contents(contents_path)
        xrefs = {}
        for md_file in sorted(Path(papers_dir).glob("*.md")):
            md_text = read_md(md_file)
            code = md_to_paper_code(md_text, contents)
            if code is None:
                continue
            for r in rows:
                hits = []
                for t in [r["term"], *(r.get("aliases") or [])]:
                    hits.extend(find_term_in_sections(t, code, md_text, contents))
                xrefs.setdefault(r["term"], []).extend(h for h in dict.fromkeys(hits))
        for k in xrefs:
            xrefs[k] = list(dict.fromkeys(xrefs[k]))

    Path(out_path).write_text(render_registry_page(rows, pages, xrefs), encoding="utf-8")
    if lookup_path:
        Path(lookup_path).write_text(json.dumps(build_lookup(rows), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Glossary written to {out_path}  ({len(rows)} terms)", file=sys.stderr)
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Build WDT master glossary with cross-references from paper Glossary sections."
    )
    parser.add_argument("--papers",   help="Directory containing .md paper files")
    parser.add_argument("--contents", help="Path to contents.yml")
    parser.add_argument("--out",      default="glossary_auto.md", help="Output path")
    parser.add_argument("--registry", help="Registry mode: path to registry/glossary.yml")
    parser.add_argument("--pages",    help="Registry mode: path to registry/pages.yml")
    parser.add_argument("--lookup",   help="Registry mode: path of the lookup JSON to write")
    args = parser.parse_args()
    if args.registry:
        if not args.pages:
            parser.error("--registry needs --pages")
        if bool(args.papers) != bool(args.contents):
            parser.error("usage lists need both --papers and --contents")
        sys.exit(build_registry(args.registry, args.pages, args.out, args.lookup, args.papers, args.contents))
    if not (args.papers and args.contents):
        parser.error("legacy mode needs --papers and --contents")
    build_glossary(args.papers, args.contents, args.out)


if __name__ == "__main__":
    main()
