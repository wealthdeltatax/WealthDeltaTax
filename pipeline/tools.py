"""
pipeline/tools.py — WDT interactive tool page generator.

Reads calculator fragment HTML files from site/tools/, wraps each one in a
Quarto .qmd page (front matter + {=html} pass-through block), and writes the
result to _build/model/.

Called by preprocess.py as part of the main build.  Can also be run standalone
for debugging: python pipeline/tools.py

Calculator fragments (site/tools/*_calc.html) are pure HTML body content:
  - No <!DOCTYPE>, <html>, <head>, or <body> shell
  - No .wdt-tool-header (Quarto provides navbar and footer)
  - No .wdt-tool-panel / .wdt-tool-inner (Quarto provides the content area)
  - The Pyodide <script src> lives in the body — browsers handle this fine
  - CSS classes come from the global site theme (tools.css, styles.css)

The Pyodide fetch() calls inside each fragment use bare filenames
('wdt_core.py', '260812_WDT_Params.toml').  These resolve correctly because
the runtime files are deployed alongside the rendered pages in _site/model/.
"""

from __future__ import annotations

import re
from pathlib import Path

# ── Tool registry ─────────────────────────────────────────────────────────────
# Each entry defines one calculator page.
#   source  — filename in site/tools/ (relative, no directory prefix)
#   output  — filename stem for _build/model/*.qmd (Quarto renders to *.html)
#   title   — Quarto page title (also used as the <h1> via Quarto's title block)
#   description — Quarto page description (used in <meta> and OG tags)
#
# To add a new calculator:
#   1. Create site/tools/{name}_calc.html as a clean body fragment
#   2. Add an entry to TOOLS below
#   3. Add the output page to the navbar/sidebar in site/_quarto.yml
#   4. Link to it from site/pages/calculator_index.md

TOOLS: list[dict] = [
    {
        "source":      "taxpayer_calc.html",
        "output":      "taxpayer",
        "title":       "WDT — Individual Taxpayer Calculator",
        "description": (
            "Route C simulation: equity-transfer mechanism over N holding periods "
            "plus terminal sell year. Results always shown alongside the "
            "honest-declaration (α = 1) baseline."
        ),
    },
    {
        "source":      "revenue_calc.html",
        "output":      "revenue",
        "title":       "WDT — National Revenue Calculator",
        "description": (
            "Aggregate WDT revenue modelled across the full UK taxable wealth "
            "distribution (Taxpayer Cohort Model). Four return tiers "
            "(Fagereng et al. 2020). UK equity return series 1947–2019."
        ),
    },
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _strip_html_shell(html: str) -> str:
    """
    Remove the outer <!DOCTYPE>/<html>/<head>/<body> shell if present,
    returning the body content as a clean fragment.

    Fragments that have no shell (the normal case for calc files) are
    returned unchanged.
    """
    # Strip everything up to and including </head>, plus optional <body> tag.
    stripped = re.sub(
        r"(?is)^.*?</head>\s*(?:<body[^>]*>)?",
        "",
        html,
        count=1,
    )
    # Strip trailing </body> and </html>.
    stripped = re.sub(r"(?is)\s*</body>\s*</html>\s*$", "", stripped)
    return stripped.strip()


def _wrap_as_qmd(fragment: str, title: str, description: str) -> str:
    """
    Wrap a body fragment in Quarto front matter and a raw HTML pass-through
    block.

    Front matter:
      title       — rendered as the page <h1> by Quarto's title block
      description — used in <meta description> and OG tags
      toc         — false: calculators have no section hierarchy to navigate
      subtitle    — omitted intentionally; the calc fragment has its own
                    subtitle paragraph immediately after the h1

    The {=html} block with quarto-disable-processing=true tells Quarto to
    pass the HTML through verbatim without attempting Markdown processing,
    link rewriting, or figure handling inside the block.
    """
    # Escape any double-quotes in title/description for YAML safety.
    safe_title = title.replace('"', '\\"')
    safe_desc  = description.replace('"', '\\"')

    return (
        f'---\n'
        f'title: "{safe_title}"\n'
        f'description: "{safe_desc}"\n'
        f'toc: false\n'
        f'---\n\n'
        f'```{{=html}}\n'
        f'<!-- quarto-disable-processing=true -->\n'
        f'{fragment}\n'
        f'```\n'
    )


# ── Public API ────────────────────────────────────────────────────────────────

def generate_tool_pages(
    tools_src_dir: Path,
    build_model_dir: Path,
) -> None:
    """
    Generate a .qmd page in build_model_dir for each entry in TOOLS.

    Args:
        tools_src_dir:   Path to site/tools/ — where *_calc.html files live.
        build_model_dir: Path to _build/model/ — where *.qmd files are written.
                         Created if it does not exist.
    """
    build_model_dir.mkdir(parents=True, exist_ok=True)

    for tool in TOOLS:
        src = tools_src_dir / tool["source"]
        if not src.exists():
            print(f"  ! tools/{tool['source']} not found — skipping {tool['output']}.qmd")
            continue

        html = src.read_text(encoding="utf-8")
        fragment = _strip_html_shell(html)
        qmd_text = _wrap_as_qmd(fragment, tool["title"], tool["description"])

        dest = build_model_dir / f"{tool['output']}.qmd"
        dest.write_text(qmd_text, encoding="utf-8")
        print(f"  ✓ tools/{tool['source']} → _build/model/{tool['output']}.qmd")


# ── Standalone entry point (for debugging) ────────────────────────────────────

if __name__ == "__main__":
    import sys
    # Resolve paths relative to this file (pipeline/tools.py → repo root)
    pipeline_dir = Path(__file__).resolve().parent
    root_dir     = pipeline_dir.parent
    tools_src    = root_dir / "site" / "tools"
    build_model  = root_dir / "_build" / "model"

    if not tools_src.exists():
        print(f"ERROR: site/tools/ not found at {tools_src}")
        sys.exit(1)

    generate_tool_pages(tools_src, build_model)
    print("Done.")
