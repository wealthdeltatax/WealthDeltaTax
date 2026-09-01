"""
diagrams.py — Mermaid diagram rendering and flowcharts.qmd generation.

Renders .mmd source files from site/diagrams/ to PNG via mmdc,
then generates flowcharts.qmd in _build/ referencing those PNGs.

To add a diagram: add a .mmd to site/diagrams/ and an entry to DIAGRAMS.
To restyle: edit classDef lines in the .mmd file directly.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from config import AUTHOR, DIAGRAMS_DIR

# On Windows, npm .cmd files need shell=True to resolve correctly.
_SHELL = sys.platform == "win32"


# ── Diagram registry ──────────────────────────────────────────────────────────
# (source filename, section heading title, prose description)

DIAGRAMS = [
    (
        "260812_WDT_Flowchart_LR.mmd",
        "WDT Taxpayer Journey — Full Detail",
        "Every decision branch: window election, route assignment, privacy election, "
        "valuation sub-routes and disputes, net worth and threshold, rate and delta, "
        "tax or symmetric refund, settlement by route, corporate levy credits, "
        "administrator credentialling, SWF allocation, Route D auction, annual loop, "
        "and all four closure events.",
    ),
    (
        "260812_WDT_Skeleton_LR.mmd",
        "WDT Taxpayer Journey — Overview",
        "Ten-step skeleton of the WDT journey for orientation before reading the full chart.",
    ),
    (
        "260812_UK_Tax_Flowchart_LR.mmd",
        "UK Tax System (Comparison) — Full Detail",
        "The current UK system shown as a structural comparator. "
        "Each tax year is assessed independently with no carry-forward of wealth position.",
    ),
    (
        "260812_UK_Skeleton_LR.mmd",
        "UK Tax System (Comparison) — Overview",
        "Skeleton overview of the UK system for side-by-side comparison with the WDT.",
    ),
]


# ── PNG rendering ─────────────────────────────────────────────────────────────

def render_pngs(build: Path) -> None:
    """
    Render each .mmd file to PNG via mmdc and write to _build/diagrams/.
    Called once per build from generate_flowcharts_qmd().
    """
    out_dir = build.parent / "site" / "diagrams"   # wdt-site/site/diagrams/
    out_dir.mkdir(parents=True, exist_ok=True)

    for filename, title, _ in DIAGRAMS:
        src = DIAGRAMS_DIR / filename
        if not src.exists():
            print(f"  ! diagram source not found: {src} — skipping")
            continue

        out = out_dir / Path(filename).with_suffix(".png").name
        print(f"  Rendering {filename} → diagrams/{out.name}")

        result = subprocess.run(
            f'mmdc -i "{src}" -o "{out}" --width 3600 --backgroundColor white',
            capture_output=True,
            text=True,
            shell=True,
        )

        if result.returncode != 0:
            print(f"  ! mmdc failed for {filename}:")
            print(result.stderr)
        else:
            print(f"  ✓ {out.name}")


# ── flowcharts.qmd generation ─────────────────────────────────────────────────

def generate_flowcharts_qmd(build: Path) -> None:
    """
    Render all diagrams to PNG, then write _build/flowcharts.qmd
    referencing those PNGs as plain images.
    """
    render_pngs(build)

    lines = [
        "---",
        'title: "Taxpayer Journey Flowcharts"',
        'description: "Flowcharts mapping the WDT taxpayer journey and the current UK tax system."',
        f'author: "{AUTHOR}"',
        "---",
        "",
        "Two versions of each diagram are provided: a full detail chart covering every "
        "decision branch, and a skeleton overview for orientation. "
        "The WDT and UK diagrams are shown side by side for structural comparison.",
        "",
        "---",
        "",
    ]

    for filename, title, description in DIAGRAMS:
        png_name = Path(filename).with_suffix(".png").name
        lines += [
            f"## {title}",
            "",
            description,
            "",
            f"![{title}](diagrams/{png_name})",
            "",
            "---",
            "",
        ]

    dest = build / "flowcharts.qmd"
    dest.write_text("\n".join(lines), encoding="utf-8")
    print(f"  ✓ Generated flowcharts.qmd ({len(DIAGRAMS)} diagrams)")