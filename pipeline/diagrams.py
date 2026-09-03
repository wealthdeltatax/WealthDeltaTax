"""
diagrams.py — Mermaid diagram rendering and flowcharts.qmd generation.

Renders .mmd source files from site/diagrams/ to PNG via mmdc,
then generates flowcharts.qmd in _build/ referencing those PNGs.

To add a diagram: add a .mmd to site/diagrams/ and an entry to DIAGRAMS.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from config import AUTHOR, DIAGRAMS_DIR

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
    (
        "260812_WDT_Bidirectional_LR.mmd",
        "WDT — Bidirectional Flow",
        "The core mechanic: private wealth rising triggers a contribution; "
        "falling triggers a symmetric refund. Both flow through the public wealth fund.",
    ),
]


# ── Structural metrics (derived from mmd source; update if diagrams change) ──
# Counted from the .mmd files: node IDs defined before a shape delimiter,
# decision diamonds {}, and --> edge occurrences.

_METRICS = {
    "wdt_full":  {"nodes": 68,  "decisions": 18, "edges": 78,  "regimes": 1},
    "uk_full":   {"nodes": 107, "decisions": 37, "edges": 140, "regimes": 12},
    "wdt_skel":  {"nodes": 28},
    "uk_skel":   {"nodes": 73},
}


# ── PNG rendering ─────────────────────────────────────────────────────────────

def render_pngs(build: Path) -> None:
    """
    Render each .mmd file to PNG via mmdc and write to _build/diagrams/.

    In CI (GitHub Actions), the PUPPETEER_CONFIG env var points at a JSON file
    that disables the Chrome sandbox (required on Linux runners). mmdc does not
    read this env var automatically, so we pass it explicitly via
    --puppeteerConfigFile when the env var is set and the file exists.
    On Windows (local builds) the env var is not set, so the flag is omitted.
    """
    out_dir = build / "diagrams"
    out_dir.mkdir(parents=True, exist_ok=True)

    puppeteer_config = os.environ.get("PUPPETEER_CONFIG")

    for filename, title, _ in DIAGRAMS:
        src = DIAGRAMS_DIR / filename
        if not src.exists():
            print(f"  ! diagram source not found: {src} — skipping")
            continue

        out = out_dir / Path(filename).with_suffix(".png").name

        cmd = [
            "mmdc",
            "-i", str(src),
            "-o", str(out),
            "--width", "3600",
            "--backgroundColor", "white",
        ]

        if puppeteer_config and Path(puppeteer_config).exists():
            cmd += ["--puppeteerConfigFile", puppeteer_config]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=_SHELL,
        )

        if result.returncode != 0:
            print(f"  ✗ mmdc FAILED for {filename}:")
            if result.stderr:
                print(f"    stderr: {result.stderr[:500]}")
            if result.stdout:
                print(f"    stdout: {result.stdout[:500]}")
        else:
            size = out.stat().st_size if out.exists() else 0
            if size == 0:
                print(f"  ✗ mmdc produced empty output for {filename}")
            else:
                print(f"  ✓ {out.name} ({size:,} bytes)")


# ── flowcharts.qmd generation ─────────────────────────────────────────────────

_LIGHTBOX_JS = """\
```{=html}
<script>
(function () {
  /* Lightbox: click any diagram image to expand; ESC or click overlay to close. */
  var overlay = null;

  function buildOverlay() {
    overlay = document.createElement('div');
    overlay.id = 'wdt-lightbox';
    Object.assign(overlay.style, {
      display:        'none',
      position:       'fixed',
      inset:          '0',
      background:     'rgba(0,0,0,0.85)',
      zIndex:         '9999',
      cursor:         'zoom-out',
      overflow:       'auto',
      alignItems:     'center',
      justifyContent: 'center',
    });

    var img = document.createElement('img');
    img.id  = 'wdt-lightbox-img';
    Object.assign(img.style, {
      maxWidth:  '95vw',
      maxHeight: '90vh',
      margin:    'auto',
      display:   'block',
      boxShadow: '0 0 40px rgba(0,0,0,0.6)',
    });
    overlay.appendChild(img);

    var close = document.createElement('button');
    close.textContent = '✕';
    Object.assign(close.style, {
      position:   'fixed',
      top:        '1rem',
      right:      '1.25rem',
      background: 'none',
      border:     'none',
      color:      '#fff',
      fontSize:   '1.75rem',
      cursor:     'pointer',
      lineHeight: '1',
    });
    close.setAttribute('aria-label', 'Close');
    overlay.appendChild(close);

    document.body.appendChild(overlay);

    function closeLightbox() {
      overlay.style.display = 'none';
      img.src = '';
    }
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay || e.target === close) closeLightbox();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeLightbox();
    });
  }

  function init() {
    buildOverlay();
    var img_lb = document.getElementById('wdt-lightbox-img');

    document.querySelectorAll('.wdt-diagram-pair img, .wdt-diagram-solo img').forEach(function (img) {
      img.style.cursor = 'zoom-in';
      img.setAttribute('title', 'Click to enlarge');
      img.addEventListener('click', function () {
        img_lb.src = img.src;
        overlay.style.display = 'flex';
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
</script>
```"""


_PAIR_CSS = """\
```{=html}
<style>
.wdt-diagram-pair {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  align-items: start;
  margin: 1.5rem 0 2rem;
}
.wdt-diagram-pair figure,
.wdt-diagram-solo figure {
  margin: 0;
}
.wdt-diagram-pair img,
.wdt-diagram-solo img {
  width: 100%;
  height: auto;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
}
.wdt-diagram-label {
  font-size: 0.8rem;
  color: #64748b;
  text-align: center;
  margin-top: 0.4rem;
  font-style: italic;
}
.wdt-metrics-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
  margin: 1rem 0 1.5rem;
}
.wdt-metrics-table th {
  text-align: left;
  padding: 0.4rem 0.75rem;
  background: #f8fafc;
  border-bottom: 2px solid #e2e8f0;
}
.wdt-metrics-table td {
  padding: 0.4rem 0.75rem;
  border-bottom: 1px solid #e2e8f0;
}
.wdt-metrics-table td:not(:first-child) {
  text-align: right;
  font-variant-numeric: tabular-nums;
}
.wdt-metrics-table tr:last-child td { border-bottom: none; }
.wdt-argument-box {
  border-left: 3px solid #2C5F8A;
  padding: 0.75rem 1rem;
  margin: 1rem 0 1.5rem;
  background: #f0f7ff;
  font-size: 0.95rem;
  line-height: 1.6;
}
@media (max-width: 700px) {
  .wdt-diagram-pair { grid-template-columns: 1fr; }
}
</style>
```"""


def _pair_html(left_png: str, left_label: str, right_png: str, right_label: str) -> str:
    """Return a raw HTML block with two diagrams side by side."""
    return f"""\
```{{=html}}
<div class="wdt-diagram-pair">
  <figure>
    <img src="diagrams/{left_png}" alt="{left_label}" />
    <p class="wdt-diagram-label">{left_label}</p>
  </figure>
  <figure>
    <img src="diagrams/{right_png}" alt="{right_label}" />
    <p class="wdt-diagram-label">{right_label}</p>
  </figure>
</div>
```"""


def _solo_html(png: str, label: str) -> str:
    return f"""\
```{{=html}}
<div class="wdt-diagram-solo">
  <figure>
    <img src="diagrams/{png}" alt="{label}" />
    <p class="wdt-diagram-label">{label}</p>
  </figure>
</div>
```"""


def generate_flowcharts_qmd(build: Path) -> None:
    """
    Render all diagrams to PNG, then write _build/flowcharts.qmd with:
      - editorial framing + structural metrics table
      - skeleton-first, side-by-side layout
      - full-detail side-by-side layout
      - lightbox JS for click-to-expand
    """
    render_pngs(build)

    m = _METRICS
    wdt = m["wdt_full"]
    uk  = m["uk_full"]

    lines = [
        "---",
        'title: "Taxpayer Journey Flowcharts"',
        'description: "Side-by-side structural comparison of the WDT taxpayer journey and the current UK tax system."',
        f'author: "{AUTHOR}"',
        "---",
        "",
        # ── inject CSS + lightbox JS ──────────────────────────────────────
        _PAIR_CSS,
        "",
        _LIGHTBOX_JS,
        "",

        # ── Section 1: Framing argument ───────────────────────────────────
        "## Complexity compared {#complexity}",
        "",
        "The diagrams below map two systems: the WDT taxpayer journey and the current "
        "UK tax system. They are shown side by side so the structural comparison is "
        "immediate rather than something the reader has to reconstruct from memory.",
        "",
        "The UK system's complexity is a historical artifact — Income Tax, NICs, CGT, "
        "IHT, Corporation Tax, VAT, and SDLT each evolved separately, governed by "
        "different logics, on different schedules, with different definitions of "
        "the same underlying concepts. Nobody designed it as a whole.",
        "",
        "The WDT is also complex. But its complexity is the complexity of a complete "
        "system: every branch has a reason, and the reasons connect. The valuation "
        "routes exist because assets differ in liquidity. The privacy election exists "
        "because disclosure has social costs that the rate schedule should price. "
        "The lifetime envelope exists because refunds must be bounded to prevent "
        "gaming. Dense flowcharts do not, by themselves, indicate poor design.",
        "",
        "```{=html}",
        '<table class="wdt-metrics-table">',
        "  <thead>",
        "    <tr><th>Metric</th><th>WDT</th><th>Current UK system</th></tr>",
        "  </thead>",
        "  <tbody>",
        f"    <tr><td>Nodes (full chart)</td><td>{wdt['nodes']}</td><td>{uk['nodes']}</td></tr>",
        f"    <tr><td>Decision points</td><td>{wdt['decisions']}</td><td>{uk['decisions']}</td></tr>",
        f"    <tr><td>Edges</td><td>{wdt['edges']}</td><td>{uk['edges']}</td></tr>",
        f"    <tr><td>Distinct tax regimes</td><td>{wdt['regimes']}</td><td>{uk['regimes']}</td></tr>",
        "  </tbody>",
        "</table>",
        "```",
        "",
        "Click any diagram to expand it. Right-click → *Open Image in New Tab* for "
        "the full-resolution version.",
        "",

        # ── Section 2: Skeletons side by side ────────────────────────────
        "## Overview: ten steps vs a year of taxes {#overview}",
        "",
        "Start here. The skeletons strip each system to its spine — enough to "
        "understand the shape before the detail becomes legible.",
        "",
        _pair_html(
            "260812_WDT_Skeleton_LR.png",
            f"WDT overview — {m['wdt_skel']['nodes']} nodes",
            "260812_UK_Skeleton_LR.png",
            f"UK system overview — {m['uk_skel']['nodes']} nodes",
        ),
        "",
        "The WDT skeleton traces a single continuous journey: open a window, assign "
        "routes, value assets, calculate the delta, settle, loop. The UK skeleton "
        "branches immediately into parallel income streams — employment, self-employment, "
        "savings, dividends, rental, pension — each with its own loss rules, reliefs, "
        "and deadlines, before they converge in the income pool and then fan out again "
        "through CGT, IHT, Corporation Tax, VAT, and SDLT.",
        "",

        # ── Section 3: Full detail side by side ──────────────────────────
        "## Full detail {#full-detail}",
        "",
        "The full charts add every decision branch: valuation disputes, route-specific "
        "settlement mechanics, the corporate levy credit system, the Route D auction "
        "trigger, and all four closure events on the WDT side; share schemes, "
        "remittance basis, pension annual allowance tapering, all CGT asset classes, "
        "the BPR/APR cap, three VAT schemes, three SDLT jurisdictions, and the "
        "full HMRC enquiry and penalty ladder on the UK side.",
        "",
        _pair_html(
            "260812_WDT_Flowchart_LR.png",
            f"WDT full detail — {wdt['nodes']} nodes · {wdt['decisions']} decisions · {wdt['edges']} edges · {wdt['regimes']} tax",
            "260812_UK_Tax_Flowchart_LR.png",
            f"UK system full detail — {uk['nodes']} nodes · {uk['decisions']} decisions · {uk['edges']} edges · {uk['regimes']} tax regimes",
        ),
        "",

        # ── Section 4: Bidirectional (solo, with context) ─────────────────
        "## The core mechanic {#core-mechanic}",
        "",
        "Before either flowchart is relevant, the underlying logic is this: "
        "the state shares in wealth movement symmetrically, in both directions, "
        "through a public fund that pre-finances the refund obligation.",
        "",
        _solo_html(
            "260812_WDT_Bidirectional_LR.png",
            "WDT bidirectional flow — private wealth ↔ public wealth fund",
        ),
        "",
    ]

    dest = build / "flowcharts.qmd"
    dest.write_text("\n".join(lines), encoding="utf-8")
    print(f"  ✓ Generated flowcharts.qmd ({len(DIAGRAMS)} diagrams, side-by-side layout)")