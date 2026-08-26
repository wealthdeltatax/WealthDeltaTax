"""
pipeline/tools.py
Step 12 of the WDT preprocessing pipeline.

Transforms standalone tool HTML files (tools/*.html) into Quarto-renderable
.qmd files and writes them to _build/tools/. Also copies the Python runtime
files (wdt_core.py, rates_model.py, *.toml) verbatim so the browser-side
fetch() calls resolve correctly at runtime.

Each HTML tool page is transformed as follows:
  1. Strip the outer HTML skeleton (<!DOCTYPE> through <body>, </body></html>).
  2. Strip the .wdt-tool-header div (Quarto navbar replaces it).
  3. Strip the <style> block (CSS now lives in site/style/styles.css).
  4. Insert Quarto front matter (title, description, toc: false).
  5. Wrap the remaining body content in a raw {=html} pass-through block.

The Pyodide <script src="..."> tag is left inside the {=html} block — Quarto
passes raw HTML blocks through verbatim, so it reaches the browser unchanged.

Internal links are rewritten so they resolve correctly from the tools/ subdirectory:
  href="../index.html"  →  href="/"         (brand link back to site root)
  href="index.html"     →  href="index.html" (unchanged — tools index)
  href="revenue.html"   →  href="revenue.html" (unchanged — sibling tool)
  href="taxpayer.html"  →  href="taxpayer.html" (unchanged — sibling tool)
These are already correct for a tools/ subdirectory; no rewriting needed for
sibling links.  Only the brand "Wealth Delta Tax" link needs updating from
../index.html to /.
"""

import re
import shutil
from pathlib import Path

# ── Tool metadata ─────────────────────────────────────────────────────────────
# Maps source filename stem → (qmd output filename, title, description)
TOOL_META: dict[str, tuple[str, str, str]] = {
    "index": (
        "index.qmd",
        "WDT — Interactive Tools",
        "Computational tools for exploring the Wealth Delta Tax mechanism. "
        "Both calculators run the Python model directly in your browser via Pyodide — "
        "no data is sent to any server.",
    ),
    "revenue": (
        "revenue.qmd",
        "WDT — National Revenue Calculator",
        "Aggregate WDT revenue modelled across the full UK taxable wealth distribution "
        "(Taxpayer Cohort Model). Four return tiers (Fagereng et al. 2020). "
        "UK equity return series 1947–2019.",
    ),
    "taxpayer": (
        "taxpayer.qmd",
        "WDT — Individual Taxpayer Calculator",
        "Route C simulation: equity-transfer mechanism over N holding periods plus "
        "terminal sell year. Results always shown alongside the honest-declaration "
        "(α = 1) baseline.",
    ),
}

# Runtime files that must be co-located with the rendered HTML so that
# browser-side fetch('wdt_core.py') etc. resolve correctly.
RUNTIME_FILES = [
    "wdt_core.py",
    "rates_model.py",
    "260812_WDT_Params.toml",
]

# ── Regex patterns ────────────────────────────────────────────────────────────
# Matches the opening HTML skeleton up to and including <body ...> or <body>
_RE_OPEN_SKELETON = re.compile(
    r"^.*?<body[^>]*>\s*",
    re.DOTALL | re.IGNORECASE,
)

# Matches the closing skeleton
_RE_CLOSE_SKELETON = re.compile(
    r"\s*</body>\s*</html>\s*$",
    re.DOTALL | re.IGNORECASE,
)

# Matches the .wdt-tool-header div (single-level, no nested divs inside it)
_RE_TOOL_HEADER = re.compile(
    r'<div\s+class="wdt-tool-header"[^>]*>.*?</div>',
    re.DOTALL | re.IGNORECASE,
)

# Matches the <style> block
_RE_STYLE_BLOCK = re.compile(
    r"<style[^>]*>.*?</style>",
    re.DOTALL | re.IGNORECASE,
)

# Rewrites the brand link from ../index.html to /
_RE_BRAND_LINK = re.compile(
    r'href=["\']\.\.\/index\.html["\']',
    re.IGNORECASE,
)


def _strip_and_wrap(html: str, title: str, description: str) -> str:
    """
    Transform a standalone tool HTML file into a Quarto .qmd file.

    Returns the full .qmd content as a string.
    """
    # 1. Strip opening skeleton
    html = _RE_OPEN_SKELETON.sub("", html)

    # 2. Strip closing skeleton
    html = _RE_CLOSE_SKELETON.sub("", html)

    # 3. Strip .wdt-tool-header (Quarto navbar replaces it)
    html = _RE_TOOL_HEADER.sub("", html)

    # 4. Strip <style> block (CSS is now in styles.css)
    html = _RE_STYLE_BLOCK.sub("", html)

    # 5. Rewrite brand link
    html = _RE_BRAND_LINK.sub('href="/"', html)

    # 6. Collapse leading/trailing blank lines
    html = html.strip()

    # 7. Build .qmd with front matter + raw HTML pass-through
    qmd = f"""---
title: "{title}"
description: "{description}"
toc: false
---

```{{=html}}
{html}
```
"""
    return qmd


def generate_tools(tools_dir: Path, build: Path) -> None:
    """
    Transform all tool HTML pages and copy runtime files into _build/tools/.

    Args:
        tools_dir:  Path to wdt-site/tools/ (source directory).
        build:      Path to _build/ (the Quarto project root).
    """
    out_dir = build / "tools"
    out_dir.mkdir(parents=True, exist_ok=True)

    if not tools_dir.exists():
        print(f"  ! tools/ directory not found at {tools_dir} — skipping tool pages")
        return

    transformed = 0
    for stem, (output_name, title, description) in TOOL_META.items():
        src = tools_dir / f"{stem}.html"
        if not src.exists():
            print(f"  – tools/{stem}.html not found (skipped)")
            continue

        html = src.read_text(encoding="utf-8")
        qmd  = _strip_and_wrap(html, title, description)
        dest = out_dir / output_name
        dest.write_text(qmd, encoding="utf-8")
        print(f"  ✓ tools/{stem}.html  →  _build/tools/{output_name}")
        transformed += 1

    # Copy runtime files verbatim so fetch() calls resolve at runtime
    copied_runtime = 0
    for fname in RUNTIME_FILES:
        src = tools_dir / fname
        if src.exists():
            shutil.copy2(src, out_dir / fname)
            copied_runtime += 1
        else:
            print(f"  ! tools/{fname} not found — fetch() calls may fail at runtime")

    print(
        f"  Tools: {transformed} page(s) transformed, "
        f"{copied_runtime} runtime file(s) copied to _build/tools/"
    )
