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

PRINT_DIR    = ROOT_DIR / "print"
TEMPLATE     = PRINT_DIR / "template.tex"
LUA_FILTER   = PRINT_DIR / "tabularx.lua"
BIB_PATH     = ROOT_DIR / "registry" / "references.bib"
CSL_PATH     = ROOT_DIR / "site" / "style" / "apa.csl"
# fix_image_paths() rewrites all image srcs to figures/<filename>.
# Pandoc's --resource-path resolves that as <dir>/figures/<filename>, so
# FIGURES_ROOT must be the *parent* of the figures/ directory, not figures/ itself.
# wdt-site/_build/figures/ is the pre-flattened directory Quarto already maintains.
FIGURES_ROOT = ROOT_DIR / "_build"


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
# Most divs are stripped entirely. The exception is figure divs: any fenced
# div that contains an image line is a Quarto figure block. We extract the
# image line and caption paragraph and re-emit them as plain markdown so the
# PDF pipeline sees them. The ::: wrappers themselves are dropped.
#
# Figure div pattern (Quarto):
#   ::: {#fig-label .class ...}
#   ![alt](figures/file.png){width=X%}
#
#   Caption text here.
#   :::

_IMAGE_LINE_RE = re.compile(r'^!\[.*?\]\([^)]+\)', re.MULTILINE)


def _rescue_figure_divs(text: str) -> str:
    """
    For each ::: {…} … ::: block that contains an image line, extract and
    re-emit the image line and any caption paragraph as plain markdown.
    Non-figure divs are left for the general stripping pass.
    """
    # Match any fenced div: ::: {attrs} ... :::  (non-greedy, anchored at line start)
    div_re = re.compile(
        r'^(:::[ \t]*\{[^}]*\})(.*?)(^:::[ \t]*$)',
        re.MULTILINE | re.DOTALL,
    )

    def _replace(m: re.Match) -> str:
        body = m.group(2)
        if not _IMAGE_LINE_RE.search(body):
            # Not a figure div — leave it intact for the general strip pass.
            return m.group(0)

        # It's a figure div. Extract:
        #   1. The image line(s) — keep as-is
        #   2. Any non-blank, non-image paragraphs → the caption
        lines = body.splitlines()
        image_lines = []
        caption_lines = []
        in_caption = False
        for line in lines:
            if re.match(r'^!\[', line):
                image_lines.append(line)
                in_caption = False
            elif line.strip() == "":
                if image_lines:
                    in_caption = True
            elif in_caption:
                caption_lines.append(line)

        parts = []
        if image_lines:
            parts.append("\n".join(image_lines))
        if caption_lines:
            # Wrap caption in inline raw_tex size/italic commands.
            # Pandoc processes the markdown content normally (links, math, bold)
            # before the surrounding LaTeX commands reach lualatex — so markdown
            # links with # anchors are converted to \href{} and never hit LaTeX raw.
            # \begingroup…\endgroup scopes the font change to this paragraph only.
            caption_text = "\n".join(caption_lines)
            caption_block = (
                r"`\begingroup\small\itshape`{=latex} "
                + caption_text + " "
                + r"`\endgroup`{=latex}"
            )
            parts.append(caption_block)
        return "\n\n".join(parts) + "\n"

    return div_re.sub(_replace, text)


def _strip_quarto_blocks(text: str) -> str:
    # First: rescue figure divs before the general strip removes them.
    text = _rescue_figure_divs(text)

    # Remove ```{=html} ... ``` raw blocks entirely (JSON-LD, banners, etc.)
    text = re.sub(
        r"^```\{=html\}.*?^```[ \t]*$",
        "",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    # Remove ::: {.class} ... ::: fenced divs entirely (non-figure ones remain)
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
# which _strip_quarto_blocks() then removes. This function re-injects it as
# plain pandoc markdown after the YAML fence.
#
# Version/date/word_count are NOT re-injected here — the template's
# $if(version)$ block renders those from YAML, and \maketitle renders the
# date field; duplicating them here caused triple-date output.
#
# Disclosure wrapping: DISCLOSURE may contain ### headings. Wrapping the whole
# string in *...* causes pandoc to swallow the heading marker, producing a
# stray * and no heading. Instead: strip heading markers (convert to bold
# inline), collapse any paragraph breaks so the whole thing is one italic span.

_YAML_FENCE_END_RE = re.compile(r"^---\s*\n", re.MULTILINE)


def _render_disclosure() -> str:
    """
    Convert DISCLOSURE to a single italic pandoc paragraph.
    ### Heading lines → **Heading** (bold, safe inside *...*)
    Blank lines collapsed to a space so *...* spans the whole block.
    """
    lines = DISCLOSURE.strip().splitlines()
    rendered = []
    for line in lines:
        m = re.match(r'^#{1,6}\s+(.*)', line.strip())
        if m:
            rendered.append(f"**{m.group(1)}**")
        elif line.strip():
            rendered.append(line.strip())
        # blank lines dropped — they'd break the italic span
    return "*" + " ".join(rendered) + "*\n\n"


def _inject_pdf_disclosure(text: str, shortcode: str, paper_meta: dict) -> str:
    """
    Inject the disclosure as a plain italic paragraph after the YAML front
    matter. Runs after _strip_quarto_blocks() has removed the div form.
    """
    if not paper_meta.get(shortcode):
        return text

    disclosure_para = _render_disclosure()

    matches = list(_YAML_FENCE_END_RE.finditer(text))
    if len(matches) >= 2:
        insert_pos = matches[1].end()
        return text[:insert_pos] + "\n" + disclosure_para + text[insert_pos:]
    return disclosure_para + text


# ── 4. Output filename ─────────────────────────────────────────────────────────

# Flat lookup: shortcode → group name (built once from SECTION_ORDER)
SECTION_ORDER: list[tuple[str, list[str]]] = [
    ("Core",                     ["WP", "MF"]),
    ("Prior Literature",         ["LR.A", "LR.B"]),
    ("Jurisdiction",             ["JUR"]),
    ("Mechanism and Valuation",  ["VAL", "VAL.A", "VAL.B", "CORP", "CORP.A", "GOV", "GOV.A", "GOV.B"]),
    ("Revenue Modelling",        ["RATES", "RATES.A", "SWEEPS", "SWEEPS.A"]),
    ("Robustness and Limits",    ["BEHAV", "BEHAV.A", "FAL", "SCOPE"]),
    ("Welfare and Distribution", ["WFR", "WFR.A", "LDW", "ENV"]),
    ("Implementation",           ["CLOSE", "PHASE1"]),
    ("Political and Strategic",  ["POL", "FM", "MOD", "INST", "ADD"]),
]

_SHORTCODE_TO_GROUP: dict[str, str] = {
    sc: group
    for group, shortcodes in SECTION_ORDER
    for sc in shortcodes
}

# Prefix stripped from YAML titles before use in filenames
_WDT_TITLE_PREFIX = re.compile(r'^the\s+wealth\s+delta\s+tax\s*[:\-–—]\s*', re.IGNORECASE)


def _pdf_filename(shortcode: str, stem: str, paper_meta: dict[str, Any]) -> str:
    """
    Build a PDF filename in the format:
        The Wealth Delta Tax - {Group} - {Short Title}.pdf

    The YAML title has any leading "The Wealth Delta Tax: " prefix stripped
    to avoid repetition. Special characters are removed; spaces preserved.
    Falls back to "Uncategorised" for papers not in SECTION_ORDER.
    Falls back to SC_stem.pdf if no title is available at all.
    """
    meta  = paper_meta.get(shortcode, {})
    title = meta.get("title", "").strip()

    if not title:
        sc_safe = shortcode.replace(".", "-")
        return f"{sc_safe}_{stem}.pdf"

    # Strip leading "The Wealth Delta Tax: " / "- " / "– " variants
    short_title = _WDT_TITLE_PREFIX.sub("", title).strip()

    # Sanitise: remove special chars only, preserve spaces
    short_title = re.sub(r'[^\w\s\-]', '', short_title)
    short_title = re.sub(r'\s+', ' ', short_title.strip())

    group = _SHORTCODE_TO_GROUP.get(shortcode, "Uncategorised")

    return f"The Wealth Delta Tax - {group} - {short_title}.pdf"


# ── 5. PDF-specific image transforms ──────────────────────────────────────────
#
# Two problems with figures in the PDF pipeline:
#
# A) PATH NORMALISATION
#    Source files reference figures as ../figures/<name>.png (relative to the
#    source file's location inside the source tree). fix_image_paths() from
#    transforms.py may not handle the ../ prefix. After fix_image_paths runs,
#    any remaining path that still contains /figures/ is rewritten to the bare
#    figures/<name>.png that pandoc's --resource-path can resolve.
#
# B) CAPTION EXTRACTION (Pattern B)
#    The papers use two figure patterns:
#
#    Pattern A (Quarto div — handled by _rescue_figure_divs):
#      ::: {#fig-label}
#      ![](figures/file.png){width=100%}
#
#      Figure N.Na: Caption text.
#      :::
#
#    Pattern B (bare image — handled here):
#      ![Figure N.Na: Caption text. **(CODE §ref)**](../figures/file.png){width=100%}
#
#    With implicit_figures disabled, pandoc renders Pattern B as a plain
#    \includegraphics with no caption — the alt text is simply dropped.
#    This function detects Pattern B images (alt text beginning with "Figure"
#    or "Figure"), strips the alt text from the image marker (so the image
#    renders cleanly inline), and appends the alt text as a plain paragraph
#    immediately below the image line. The paragraph is what becomes the
#    visible caption in the PDF.
#
#    The bold cross-reference suffix **(CODE §ref)** embedded in the alt text
#    is valid pandoc markdown and renders as bold inline in the caption paragraph.

# Matches: ![any alt text](any/path/file.ext){optional attrs}
# Groups:  1=alt text  2=path  3=optional {attrs}
_IMG_FULL_RE = re.compile(
    r'^(!\[)(.*?)(\]\([^)]+\)(?:\{[^}]*\})?)',
    re.MULTILINE | re.DOTALL,
)

# Matches a path containing /figures/ or starting with figures/
_FIG_PATH_RE = re.compile(r'(?:.*[/\\])?figures[/\\]([^)\s]+)')


def _fix_image_paths_pdf(text: str) -> str:
    """
    Normalise all image paths to figures/<filename> regardless of prefix.
    Handles ../figures/, ./figures/, ../../figures/, bare figures/, etc.
    Runs after fix_image_paths() from transforms.py as a safety net.

    The path is extracted by anchoring at the ]( delimiter that separates
    the alt text from the path, so parentheses inside alt text (e.g.
    "(basis points)" or "($\\text{CEW}$)") do not confuse the match.
    """
    # Capture groups: 1=everything up to and including ](  2=path  3=rest
    _IMG_PATH_CAPTURE = re.compile(
        r'(!\[(?:[^\[\]]|\[[^\]]*\])*\]\()([^)]+)(\)(?:\{[^}]*\})?)'
    )

    def _rewrite(m: re.Match) -> str:
        prefix        = m.group(1)   # ![alt](
        original_path = m.group(2)   # ../figures/file.png
        suffix        = m.group(3)   # ){width=100%}
        fig_m = _FIG_PATH_RE.match(original_path.strip())
        if fig_m:
            return prefix + "figures/" + fig_m.group(1) + suffix
        return m.group(0)

    return _IMG_PATH_CAPTURE.sub(_rewrite, text)


def _extract_image_captions(text: str) -> str:
    """
    For Pattern B figures: move the alt text out of ![alt](path) and emit it
    as a plain paragraph below the image.

    Transforms:
      ![Figure N: Caption text](figures/file.png){width=100%}
    into:
      ![](figures/file.png){width=100%}

      Figure N: Caption text

    Only fires when the alt text begins with "Figure" (case-insensitive) —
    these are the hand-written captions. Empty alt text and short descriptive
    alt text (accessibility labels, not captions) are left alone.

    Captions are emitted as a normal markdown paragraph bracketed by inline
    raw_tex commands (\\begingroup\\small\\itshape … \\endgroup). Pandoc
    processes the markdown content — links, math, bold — before the surrounding
    LaTeX commands reach lualatex, so # anchors in cross-ref URLs are never
    exposed as bare characters in LaTeX horizontal mode.
    """
    # Process line by line to avoid multiline confusion; image lines that span
    # multiple lines (alt text with \n) are handled by re.DOTALL on the inner match.
    lines = text.split('\n')
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Quick pre-check: does this line start a Pattern B image?
        if line.lstrip().startswith('!['):
            # Try to match a complete image tag (may span lines if alt text is long)
            # Reconstruct a lookahead block of up to 5 lines to handle multiline alt
            block = '\n'.join(lines[i:i+5])
            m = re.match(
                r'^(!\[)(.*?)(\]\(([^)]+)\)(\{[^}]*\})?)',
                block,
                re.DOTALL,
            )
            if m:
                alt   = m.group(2).strip()
                path  = m.group(4)
                attrs = m.group(5) or ''
                # Count lines consumed by the full match
                consumed = m.group(0).count('\n')
                if re.match(r'(?i)^figure\b', alt):
                    # Emit image with empty alt, then caption as a markdown paragraph
                    # wrapped in inline raw_tex size/italic commands.
                    # Pandoc processes the caption markdown normally (resolving links,
                    # math, bold) before the LaTeX commands reach lualatex — so
                    # markdown links with # anchors become \href{} and never hit
                    # LaTeX as bare # characters. Normalise internal newlines first.
                    caption = re.sub(r'\s+', ' ', alt)
                    out.append(f'![]({path}){attrs}')
                    out.append('')
                    out.append(
                        r'`\begingroup\small\itshape`{=latex} '
                        + caption + ' '
                        + r'`\endgroup`{=latex}'
                    )
                    i += consumed + 1
                    continue
        out.append(line)
        i += 1
    return '\n'.join(out)


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
      3. _fix_image_paths_pdf     (PDF safety net — normalises ../figures/ etc.)
      4. _extract_image_captions  (PDF-only — Pattern B: moves alt text to paragraph)
      5. convert_crossrefs        (shared — cross-refs → [TEXT](URL))
      6. _fix_double_hash         (fix ## artefacts in cross-ref URLs)
      7. convert_internal_bibliography (shared — [CODE] lines → bold text + div)
      8. inject_front_matter      (shared — enriches YAML, injects meta/disclosure divs)
      9. _strip_quarto_blocks     (PDF-only — rescues figure divs, removes other divs,
                                   raw HTML, and heading attrs)
     10. _inject_pdf_disclosure   (PDF-only — re-injects disclosure as plain italic)
     11. append "# References"   (bibliography anchor for --citeproc)

    Note: implicit_figures is disabled in the pandoc call (-f markdown-implicit_figures)
    so images are never promoted to LaTeX figure floats. Captions are emitted as
    plain paragraphs below each image by _extract_image_captions (Pattern B) or
    _rescue_figure_divs inside _strip_quarto_blocks (Pattern A / Quarto div).
    """
    text  = _strip_latex_pdf(text)
    text  = fix_image_paths(text)
    text  = _fix_image_paths_pdf(text)
    text  = _extract_image_captions(text)
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


# ── 8. Pandoc invocation ───────────────────────────────────────────────────────

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
        # Disable implicit_figures: prevents pandoc from wrapping lone images in
        # \begin{figure}...\caption{alt}...\end{figure} floats. Without this,
        # any image with non-empty alt text gets a "Figure N:" auto-counter and
        # the alt text becomes a LaTeX caption — producing double captions when
        # the source also has a manual caption paragraph. With the extension off,
        # images render inline (\includegraphics only) and captions remain as
        # ordinary paragraphs immediately below each image.
        "-f", "markdown-implicit_figures",
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


# ── 9. Main build loop ────────────────────────────────────────────────────────

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

    # Pre-built figures dir — Quarto maintains wdt-site/_build/figures/ already.
    # No copy needed; never deleted (it's a live project directory).
    figures_root = FIGURES_ROOT
    if not figures_root.exists():
        print(f"  ⚠ FIGURES_ROOT not found: {figures_root} — PDFs will have no figures")

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
        shutil.rmtree(staging_dir, ignore_errors=True)  # temp only; figures_root is live

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
