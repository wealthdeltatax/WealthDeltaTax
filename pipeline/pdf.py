"""
pdf.py — standalone PDF build pipeline for WDT papers.

Applies a PDF-specific transform chain to each source .md and calls
pandoc + lualatex to produce a dated folder of PDFs under print/.

Reuses shared transforms from transforms.py (fix_image_paths,
convert_crossrefs, convert_internal_bibliography, inject_front_matter)
but applies a PDF-specific LaTeX strip that preserves \\newpage and
\\tableofcontents, and removes Quarto-only block syntax before pandoc
sees the file.

Usage:
    python pipeline/pdf.py              # all papers
    python pipeline/pdf.py WP MF        # specific shortcodes only
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import datetime
from pathlib import Path
from typing import Any

import yaml

from config import (
    AUTHOR,
    DISCLOSURE,
    ROOT_DIR,
    SOURCE_DIR,
    extract_paper_meta,
    load,
)

from transforms import (
    fix_image_paths,
    convert_crossrefs,
    convert_internal_bibliography,
    inject_front_matter,
)

PRINT_DIR   = ROOT_DIR / "print"
TEMPLATE    = PRINT_DIR / "template.tex"
LUA_FILTER  = PRINT_DIR / "tabularx.lua"
BIB_PATH    = ROOT_DIR / "registry" / "references.bib"
CSL_PATH    = ROOT_DIR / "site" / "style" / "apa.csl"
FIGURES_DIR = ROOT_DIR / "model" / "OUTPUTS"


# ── 1. PDF-specific LaTeX strip ────────────────────────────────────────────────
#
# The web pipeline (transforms.strip_latex) strips \newpage and
# \tableofcontents because Quarto handles TOC and page breaks itself.
# For PDF we want to keep both:
#   \newpage     — section breaks between major sections
#   \tableofcontents — positioned in source after Glossary, before § 1
#
# Everything else in the web strip list is still removed.

_PDF_LATEX_STRIP = re.compile(
    r"\\medskip"
    r"|\\bigskip"
    r"|\\smallskip"
    r"|\\\\(?!\w)"          # bare \\ (line break) but not \\command
    r"|\\maketitle"
    r"|\\begin\{center\}"
    r"|\\end\{center\}"
    r"|\\noindent"
    r"|\\clearpage"
    r"|\\vspace\*?\{[^}]+\}"
    r"|\\hspace\*?\{[^}]+\}"
    r"|\\setcounter\{[^}]+\}\{[^}]+\}"
    # \newpage and \tableofcontents are intentionally NOT listed here
)


def _strip_latex_pdf(text: str) -> str:
    """Strip LaTeX artifacts while preserving \\newpage and \\tableofcontents."""
    return _PDF_LATEX_STRIP.sub("", text)


# ── 2. Quarto block removal ────────────────────────────────────────────────────
#
# The web pipeline injects Quarto-specific syntax that pandoc for PDF
# either rejects or renders as garbage:
#
#   ```{=html} ... ```      raw HTML blocks (JSON-LD, under-construction banner)
#   ::: {.class} ... :::    fenced divs (.paper-meta, .paper-disclosure,
#                           .internal-bibliography, .wdt-under-construction)
#   {.unnumbered .unlisted} heading attribute syntax
#
# All are stripped entirely. The internal-bibliography content (the
# [CODE] lines) is left as plain bold text after the ::: wrappers are
# removed, which renders acceptably in PDF.

def _strip_quarto_blocks(text: str) -> str:
    # Remove ```{=html} ... ``` raw blocks entirely (JSON-LD, banners, etc.)
    text = re.sub(
        r"^```\{=html\}.*?^```[ \t]*$",
        "",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    # Remove ::: {.class} ... ::: fenced divs entirely
    # Handles both class-attributed openers (::: {.foo}) and bare closers (:::)
    text = re.sub(
        r"^:::[ \t]*\{[^}]*\}.*?^:::[ \t]*$",
        "",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    # Remove any bare ::: lines that survived (orphaned closers)
    text = re.sub(r"^:::[ \t]*$", "", text, flags=re.MULTILINE)
    # Remove Quarto heading attributes: {.unnumbered}, {.unlisted}, combinations
    text = re.sub(r"[ \t]*\{[^}]*\.unnumbered[^}]*\}", "", text)
    text = re.sub(r"[ \t]*\{[^}]*\.unlisted[^}]*\}", "", text)
    # Collapse runs of 3+ blank lines to 2 (artefact of block removal)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text


# ── 3. PDF disclosure injection ────────────────────────────────────────────────
#
# inject_front_matter() inserts the disclosure as ::: {.paper-disclosure} :::
# which _strip_quarto_blocks() then removes (correct — the div syntax crashes
# lualatex). This function re-injects the disclosure as plain italic paragraph
# text immediately after the YAML front matter fence, so it appears in the PDF.
#
# Note: the template.tex renders version/date/word_count via YAML variables
# ($if(version)$ … $endif$). The meta_line below is therefore redundant for
# papers where inject_front_matter puts those fields into the YAML. Remove it
# if you see duplication on the title page.

_YAML_FENCE_END_RE = re.compile(r"^---\s*\n", re.MULTILINE)


def _inject_pdf_disclosure(text: str, shortcode: str, paper_meta: dict) -> str:
    """
    Inject the AI/funding disclosure as a plain paragraph after the YAML
    front matter. Runs after _strip_quarto_blocks() has removed the div form.
    """
    meta = paper_meta.get(shortcode)
    if not meta:
        return text

    version      = meta.get("version", "—")
    date_display = meta.get("version_date_display", "—")
    word_count   = meta.get("word_count", 0)

    try:
        word_count_fmt = f"{int(word_count):,}"
    except (TypeError, ValueError):
        word_count_fmt = str(word_count)

    meta_line = (
        f"**Version {version}** | {date_display} | "
        f"{word_count_fmt} words (excl. front matter)\n\n"
    )
    disclosure_para = f"*{DISCLOSURE}*\n\n"

    # Find the end of the YAML front matter (second --- fence)
    matches = list(_YAML_FENCE_END_RE.finditer(text))
    if len(matches) >= 2:
        insert_pos = matches[1].end()
        return (
            text[:insert_pos]
            + "\n"
            + meta_line
            + disclosure_para
            + text[insert_pos:]
        )
    # Fallback: prepend to entire body
    return meta_line + disclosure_para + text


# ── 4. Output filename ─────────────────────────────────────────────────────────

def _pdf_filename(shortcode: str, stem: str, paper_meta: dict[str, Any]) -> str:
    """
    Build a PDF filename from the paper's YAML title field.
    Spaces → hyphens; characters unsafe in filenames are stripped.
    Falls back to SC_stem.pdf if no title is available.
    e.g. "The Wealth Delta Tax: Valuing Wealth" → "The-Wealth-Delta-Tax-Valuing-Wealth.pdf"
    """
    meta = paper_meta.get(shortcode, {})
    title = meta.get("title", "").strip()
    if title:
        safe = re.sub(r'[^\w\s\-]', '', title)   # keep word chars, spaces, hyphens
        safe = re.sub(r'\s+', '-', safe.strip())  # spaces → hyphens
        safe = re.sub(r'-{2,}', '-', safe)        # collapse multiple hyphens
        return f"{safe}.pdf"
    sc_safe = shortcode.replace(".", "-")
    return f"{sc_safe}_{stem}.pdf"


# ── 5. Figure flattening ───────────────────────────────────────────────────────
#
# fix_image_paths() rewrites all image src to figures/<filename>.
# Pandoc's --resource-path searches each directory in the path for the
# *full relative path* as written in the source — so for figures/foo.png
# pandoc looks for <dir>/figures/foo.png in each resource-path entry.
#
# Strategy: create a figures/ subdir inside the temp dir and copy all
# images there, then add the temp dir root (not the figures/ subdir) to
# --resource-path. Pandoc will find figures/foo.png at <tmp>/figures/foo.png.

def _flatten_figures() -> Path:
    """
    Copy all figures from model/OUTPUTS/**/* into <tmp>/figures/.
    Returns the temp dir root (not the figures/ subdir).
    Uses system temp rather than a project subdirectory, avoiding OneDrive
    sync locks on Windows.
    Caller must clean up with shutil.rmtree(path, ignore_errors=True).
    """
    tmp = Path(tempfile.mkdtemp(prefix="wdt_pdf_figs_"))
    figures_subdir = tmp / "figures"
    figures_subdir.mkdir()
    if not FIGURES_DIR.exists():
        print(f"  ⚠ FIGURES_DIR not found: {FIGURES_DIR} — PDFs will have no figures")
        return tmp
    copied = 0
    for src in FIGURES_DIR.rglob("*"):
        if src.suffix.lower() in {".png", ".jpg", ".jpeg", ".pdf", ".svg", ".eps"}:
            dest = figures_subdir / src.name
            if not dest.exists():
                shutil.copy2(src, dest)
                copied += 1
    print(f"  Flattened {copied} figures → {figures_subdir}")
    return tmp


# ── 6. Per-paper PDF transform chain ──────────────────────────────────────────

def _fix_double_hash(text: str) -> str:
    """Fix ## in markdown link URLs produced by convert_crossrefs when an
    anchor already contains a # and the URL gets double-hashed."""
    return re.sub(r'\]\(([^)]*?)##', r'](\1#', text)


def _transform_for_pdf(
    text: str,
    shortcode: str,
    paper_meta: dict[str, Any],
    link_map: dict[str, str],
    anchor_map: dict[str, str],
) -> str:
    """
    Apply the PDF-specific transform chain to raw source text.

    Order:
      1. _strip_latex_pdf         (preserves \\newpage, \\tableofcontents)
      2. fix_image_paths          (shared — rewrites src to figures/<filename>)
      3. convert_crossrefs        (shared — cross-refs → [TEXT](URL))
      4. _fix_double_hash         (fix ## artefacts in cross-ref URLs)
      5. convert_internal_bibliography (shared — [CODE] lines → bold text + div)
      6. inject_front_matter      (shared — enriches YAML, injects meta/disclosure divs)
      7. _strip_quarto_blocks     (PDF-only — removes divs, raw HTML, heading attrs)
      8. _inject_pdf_disclosure   (PDF-only — re-injects disclosure as plain text)
      9. append "# References"   (bibliography anchor for --citeproc)
    """
    text  = _strip_latex_pdf(text)
    text  = fix_image_paths(text)
    text  = convert_crossrefs(text, link_map, anchor_map)
    text  = _fix_double_hash(text)
    lines = convert_internal_bibliography(text.splitlines(keepends=True))
    text  = "".join(lines)
    text  = inject_front_matter(text, shortcode, paper_meta)
    # _strip_quarto_blocks must run after inject_front_matter because
    # inject_front_matter inserts ::: {.paper-meta} and ::: {.paper-disclosure}
    text  = _strip_quarto_blocks(text)
    text  = _inject_pdf_disclosure(text, shortcode, paper_meta)
    text  = text.rstrip("\n") + "\n\n# References\n"
    return text


# ── 7. Pandoc invocation ───────────────────────────────────────────────────────

def _build_pdf(
    staging_file: Path,
    pdf_path: Path,
    figures_root: Path,
) -> bool:
    """
    Call pandoc + lualatex to render staging_file to pdf_path.
    Returns True on success, False on failure (error already printed).

    Note: --toc is intentionally omitted. \\tableofcontents in the source
    file controls TOC placement (after Glossary, before § 1). Passing --toc
    would produce a second TOC at the document top.
    """
    cmd = [
        "pandoc", str(staging_file),
        "--standalone",
        "--pdf-engine=lualatex",
        "--citeproc",
        f"--template={TEMPLATE}",
        f"--lua-filter={LUA_FILTER}",
        f"--bibliography={BIB_PATH}",
        f"--csl={CSL_PATH}",
        # resource-path: staging dir first, then figures root (contains figures/ subdir)
        f"--resource-path=.;{staging_file.parent};{figures_root}",
        "-o", str(pdf_path),
    ]
    result = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        # Print the last 3000 chars of stderr — the actual LaTeX error is at the end
        print(f"\n    ✗ FAILED")
        print(result.stderr[-3000:])
        return False
    return True


# ── 8. Main build loop ────────────────────────────────────────────────────────

def build_pdfs(shortcode_filter: list[str] | None = None) -> None:
    """
    Build PDFs for all papers (or a filtered subset by shortcode).
    Output goes to print/YYMMDD/  (date-stamped, created fresh each run).
    Staging files and the flat figures temp dir are cleaned up on exit.
    """

    # Load papers registry
    papers_yml = ROOT_DIR / "registry" / "papers.yml"
    with open(papers_yml, encoding="utf-8") as f:
        papers: list[dict] = yaml.safe_load(f)

    # Extract metadata from every source file (same as preprocess.py step 0.5)
    paper_meta: dict[str, Any] = {}
    for entry in papers:
        src = SOURCE_DIR / entry["source"]
        if not src.exists():
            continue
        meta = extract_paper_meta(src)
        if meta:
            paper_meta[meta["shortcode"]] = meta

    # Build SiteConfig for link_map and anchor_map
    cfg = load(paper_meta=paper_meta)

    # Date-stamped output folder
    date_tag = datetime.datetime.now().strftime("%y%m%d")
    out_dir  = PRINT_DIR / date_tag
    out_dir.mkdir(parents=True, exist_ok=True)

    # Staging dir for transformed .md files (cleaned up in finally)
    staging_dir = Path(tempfile.mkdtemp(prefix="wdt_pdf_staging_"))

    # Figures temp dir — contains figures/ subdir (cleaned up in finally)
    figures_root = _flatten_figures()

    built = skipped = failed = 0

    try:
        for entry in papers:
            src = SOURCE_DIR / entry["source"]
            if not src.exists():
                print(f"  ⚠ source not found: {entry['source']} — skipping")
                skipped += 1
                continue

            # Resolve shortcode from the file's own front matter
            sc_meta = extract_paper_meta(src)
            if not sc_meta:
                print(f"  ⚠ could not extract metadata from {src.name} — skipping")
                skipped += 1
                continue
            sc = sc_meta["shortcode"]

            if shortcode_filter and sc not in shortcode_filter:
                skipped += 1
                continue

            stem         = Path(entry["output"]).stem
            staging_file = staging_dir / f"{stem}.md"
            pdf_name     = _pdf_filename(sc, stem, paper_meta)
            pdf_path     = out_dir / pdf_name

            print(f"  {sc:12s} {src.name} ...", end="", flush=True)

            # Transform
            text = src.read_text(encoding="utf-8")
            text = _transform_for_pdf(
                text, sc, paper_meta, cfg.link_map, cfg.anchor_map
            )
            staging_file.write_text(text, encoding="utf-8")

            # Render
            ok = _build_pdf(staging_file, pdf_path, figures_root)
            if ok:
                print(f" ✓  →  {pdf_name}")
                built += 1
            else:
                failed += 1

    finally:
        shutil.rmtree(staging_dir,  ignore_errors=True)
        shutil.rmtree(figures_root, ignore_errors=True)

        print()
        print("=" * 50)
        print(f"  Built:   {built}")
        print(f"  Failed:  {failed}")
        print(f"  Skipped: {skipped}")
        print(f"  Output:  {out_dir}")
        print("=" * 50)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    filters = sys.argv[1:] if len(sys.argv) > 1 else None
    if filters:
        print(f"Building PDFs for: {', '.join(filters)}")
    else:
        print("Building PDFs for all papers...")
    print()
    build_pdfs(shortcode_filter=filters)
