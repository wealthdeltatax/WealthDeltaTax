"""
WDT site preprocessing pipeline.
Reads .md source files, processes them for HTML rendering, writes .qmd to _build/.
Run this before every `quarto render _build`.
"""

import os, re, shutil
from pathlib import Path
import yaml

# ── SET THIS TO YOUR SOURCE FOLDER ──────────────────────────────────────────
SOURCE_DIR = "source_md"   # <-- edit this line
BUILD_DIR  = "_build"
CROSSLINKS = "cross_links.yml"
# ────────────────────────────────────────────────────────────────────────────

with open(CROSSLINKS, encoding="utf-8") as f:
    link_map = yaml.safe_load(f)

# Matches (WP), (VAL §3.7), (CORP.A §F.9), etc.
CROSSREF_RE = re.compile(
    r'\(([A-Z][A-Z0-9]*(?:\.[A-Z][A-Z0-9]*)?)(?:\s+§[\d.A-Za-z]+)?\)'
)

LATEX_STRIP = [
    r'\\newpage', r'\\medskip', r'\\bigskip', r'\\smallskip',
    r'\\tableofcontents', r'\\appendix', r'\\maketitle',
    r'\\begin\{center\}', r'\\end\{center\}',
    r'\\noindent', r'\\clearpage',
    r'\\vspace\*?\{[^}]+\}', r'\\hspace\*?\{[^}]+\}',
    r'\\setcounter\{[^}]+\}\{[^}]+\}',
]
LATEX_RE = re.compile('|'.join(LATEX_STRIP))

INTBIB_LINE_RE = re.compile(r'^\[([A-Z][A-Z0-9]*(?:\.[A-Z][A-Z0-9]*)?)\]\s+(.+)$')


def convert_crossrefs(text):
    def replace(m):
        full  = m.group(0)
        code  = m.group(1)
        if code in link_map:
            return f'[{full}]({link_map[code]})'
        return full
    return CROSSREF_RE.sub(replace, text)


def convert_internal_bibliography(lines):
    result, in_block = [], False
    for line in lines:
        m = INTBIB_LINE_RE.match(line.rstrip())
        if m:
            if not in_block:
                result.append('\n::: {.internal-bibliography}\n')
                in_block = True
            code, rest = m.group(1), m.group(2)
            result.append(f'**[{code}]** {rest}\n')
        else:
            if in_block:
                result.append(':::\n')
                in_block = False
            result.append(line)
    if in_block:
        result.append(':::\n')
    return result


def process_file(src_path, dest_path):
    text = src_path.read_text(encoding="utf-8")
    text = LATEX_RE.sub('', text)
    text = convert_crossrefs(text)
    lines = convert_internal_bibliography(text.splitlines(keepends=True))
    text = ''.join(lines)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(text, encoding="utf-8")
    print(f"  ✓ {src_path.name} → {dest_path.name}")


def main():
    build  = Path(BUILD_DIR)
    source = Path(SOURCE_DIR)

    if build.exists():
        shutil.rmtree(build, ignore_errors=True)
    build.mkdir(exist_ok=True)

    for fname in ["_quarto.yml", "styles.css", "wdt_references.bib", "index.qmd", "apa.csl"]:
        p = Path(fname)
        if p.exists():
            shutil.copy(p, build / fname)
        else:
            if fname != "wdt_references.bib":   # bib is optional until Stage 1.5
                print(f"  ! Missing: {fname}")

    registry_path = Path("paper_registry.yml")
    if not registry_path.exists():
        print("ERROR: paper_registry.yml not found.")
        return

    with open(registry_path, encoding="utf-8") as f:
        registry = yaml.safe_load(f)

    found, missing = 0, 0
    for entry in registry:
        shortcode   = entry["shortcode"]
        source_glob = entry["source_glob"]
        output_name = entry["output"]

        matches = sorted(source.glob(source_glob))
        if not matches:
            print(f"  – {shortcode}: no file found (skipped)")
            missing += 1
            continue
        if len(matches) > 1:
            print(f"  ! {shortcode}: multiple matches, using {matches[-1].name}")

        process_file(matches[-1], build / output_name)
        found += 1

    print(f"\nDone. {found} papers staged, {missing} not yet available.")
    print(f"Run: quarto render {BUILD_DIR}")


if __name__ == "__main__":
    main()