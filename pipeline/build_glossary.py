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
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Build WDT master glossary with cross-references from paper Glossary sections."
    )
    parser.add_argument("--papers",   required=True, help="Directory containing .md paper files")
    parser.add_argument("--contents", required=True, help="Path to contents.yml")
    parser.add_argument("--out",      default="glossary_auto.md", help="Output path")
    args = parser.parse_args()
    build_glossary(args.papers, args.contents, args.out)


if __name__ == "__main__":
    main()
