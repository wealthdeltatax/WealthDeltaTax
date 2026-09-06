"""
pipeline/link_map.py

Generates _build/link-map.qmd — the interactive WDT paper cross-reference
graph, embedded within the Quarto site frame (navbar, footer, etc.).

The output is a .qmd file using page-layout: full so the graph canvas
gets the full viewport width without Quarto's sidebar or TOC competing
for space. The Quarto navbar and footer are always present.

Called by preprocess.py as step (12), after all other page generators.
preprocess.py passes dest_path as _build/link-map.html; this module
writes to _build/link-map.qmd instead (via .with_suffix).

Key exports:
    generate_link_map_html(dest_path, refs_data, link_map)
"""

from __future__ import annotations
import json
from pathlib import Path


# ── Group assignment ──────────────────────────────────────────────────────────
# Maps each shortcode to its display group. Must be updated when a new paper
# is added. Groups match the corpus.py SECTION_ORDER and _quarto.yml sidebar.

_GROUPS: dict[str, str] = {
    "WP":       "Core",
    "MF":       "Core",
    "LR":       "Literature",
    "LR.A":     "Literature",
    "LR.B":     "Literature",
    "JUR":      "Literature",
    "VAL":      "Valuation",
    "VAL.A":    "Valuation",
    "VAL.B":    "Valuation",
    "CORP":     "Corporate",
    "CORP.A":   "Corporate",
    "GOV":      "Corporate",
    "GOV.A":    "Corporate",
    "GOV.B":    "Corporate",
    "RATES":    "Revenue",
    "RATES.A":  "Revenue",
    "SWEEPS":   "Revenue",
    "SWEEPS.A": "Revenue",
    "BEHAV":    "Implementation",
    "CLOSE":    "Implementation",
    "POL":      "Implementation",
    "PHASE1":   "Implementation",
    "ENV":      "Analysis",
    "FM":       "Analysis",
    "MOD":      "Analysis",
    "SCOPE":    "Analysis",
    "ADD":      "Analysis",
}

# Canonical group order (matches sidebar / corpus table)
_GROUP_ORDER = [
    "Core", "Literature", "Valuation", "Corporate",
    "Revenue", "Implementation", "Analysis",
]


def _build_paper_data(refs_data: dict, link_map: dict) -> list[dict]:
    """
    Build the PAPER_DATA list from internal_papers in refs_data.

    Each record:
        sc      — shortcode
        title   — short display title (WDT prefix stripped)
        group   — display group from _GROUPS (fallback: "Analysis")
        url     — resolved page URL from link_map (fallback: "corpus.html")
        status  — "active" | "superseded" | "draft"
        out     — list of outbound internal shortcodes
        in      — list of inbound internal shortcodes
    """
    papers = refs_data.get("internal_papers", [])
    records = []

    for p in papers:
        sc = p.get("shortcode", "")
        if not sc:
            continue

        title = p.get("title", sc)
        # Strip verbose series prefix for display
        for prefix in (
            "The Wealth Delta Tax: ",
            "Wealth Delta Tax: ",
        ):
            if title.startswith(prefix):
                title = title[len(prefix):]
                break

        records.append({
            "sc":     sc,
            "title":  title,
            "group":  _GROUPS.get(sc, "Analysis"),
            "url":    link_map.get(sc, "corpus.html"),
            "status": p.get("status", "active"),
            "out":    p.get("outbound_internal", []),
            "in":     p.get("inbound_internal", []),
        })

    # Sort by group order, then shortcode within group
    group_idx = {g: i for i, g in enumerate(_GROUP_ORDER)}
    records.sort(key=lambda r: (group_idx.get(r["group"], 99), r["sc"]))
    return records


# ── QMD front matter ──────────────────────────────────────────────────────────
# page-layout: full suppresses Quarto's sidebar and TOC for this page only,
# giving the canvas the full viewport width. The navbar and footer are
# always present because they come from the site-level _quarto.yml.

_FRONT_MATTER = """\
---
title: "WDT Paper Link Map"
description: "Interactive cross-reference graph of all 26 WDT papers — hover to explore connections, click to open."
page-layout: full
toc: false
---
"""

# ── Body fragment (no <!DOCTYPE>, <html>, <head>, or <body> tags) ─────────────
# __PAPER_DATA__ and __GROUP_ORDER__ are replaced at generation time.
# CSS note: body{} and html{} rules are removed — Quarto controls those.
# #header div is removed — the page title comes from Quarto's front matter.
# #main uses a viewport-relative height so the graph fills the screen below
# the Quarto navbar (~56px) without overflowing.

_BODY_TEMPLATE = r"""
```{=html}
<!-- quarto-disable-processing=true -->
<style>
  /* ── Link map scoped styles ──────────────────────────────────────────── */
  /* These are scoped to the link-map page only. They do not override the  */
  /* site-wide styles.css because they target IDs / classes unique to this */
  /* page. The :root vars are already defined by styles.css.               */

  #lm-wrap {
    display: flex;
    /* Full viewport height minus Quarto navbar (~56px) and a small gap.
       Adjust the offset if the navbar height changes. */
    height: calc(100vh - 70px);
    min-height: 500px;
    margin: 0 -1.5rem -1.25rem; /* bleed to content panel edges */
    overflow: hidden;
  }

  /* Graph controls sidebar */
  #lm-sidebar {
    width: 190px;
    min-width: 190px;
    background: var(--wdt-purple);
    border-right: 2px solid var(--wdt-gold-dim);
    padding: 12px 10px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    overflow-y: auto;
    flex-shrink: 0;
  }

  .lm-ctrl-section {
    border: 1px inset var(--wdt-gold-dim);
    background: var(--wdt-purple-deep);
    padding: 8px;
  }

  .lm-ctrl-section h3 {
    font-size: 0.68rem;
    color: var(--wdt-gold);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 0 0 7px 0;
    border-bottom: 1px solid var(--wdt-gold-dim);
    padding-bottom: 3px;
    font-family: Arial, Helvetica, sans-serif;
    font-weight: bold;
  }

  .lm-group-filter { display: flex; flex-direction: column; gap: 5px; }
  .lm-group-filter label {
    display: flex; align-items: center; gap: 6px;
    font-size: 0.7rem; cursor: pointer;
    color: var(--wdt-silver);
    font-family: Arial, Helvetica, sans-serif;
  }
  .lm-group-filter label:hover { color: var(--wdt-gold); }

  .lm-group-dot {
    width: 10px; height: 10px;
    border: 1px solid rgba(255,255,255,0.3);
    flex-shrink: 0;
  }

  .lm-edge-mode { display: flex; flex-direction: column; gap: 5px; }
  .lm-edge-mode label {
    display: flex; align-items: center; gap: 6px;
    font-size: 0.7rem; cursor: pointer;
    color: var(--wdt-silver);
    font-family: Arial, Helvetica, sans-serif;
  }
  .lm-edge-mode label:hover { color: var(--wdt-gold); }

  .lm-ctrl-btn {
    display: block; width: 100%;
    background: var(--wdt-purple-mid); color: var(--wdt-gold);
    border: 2px outset var(--wdt-gold-dim);
    font-family: "Times New Roman", Times, serif;
    font-size: 0.7rem; padding: 4px 6px;
    cursor: pointer; text-align: center; margin-bottom: 4px;
  }
  .lm-ctrl-btn:hover { background: var(--wdt-purple); border-style: inset; }

  .lm-legend-item {
    display: flex; align-items: center; gap: 6px;
    font-size: 0.67rem; color: var(--wdt-silver); margin-bottom: 4px;
    font-family: Arial, Helvetica, sans-serif;
  }
  .lm-legend-line { width: 24px; height: 2px; flex-shrink: 0; }

  #lm-stats {
    font-size: 0.67rem; color: var(--wdt-silver); line-height: 1.7;
    font-family: Arial, Helvetica, sans-serif;
  }
  #lm-stats span { color: var(--wdt-gold); }

  #lm-subtitle {
    font-size: 0.67rem; color: var(--wdt-silver); font-style: italic;
    font-family: Arial, Helvetica, sans-serif; line-height: 1.5;
    padding: 4px 0;
  }

  /* Canvas area */
  #lm-canvas-wrap {
    flex: 1;
    position: relative;
    overflow: hidden;
    background-color: var(--wdt-purple-deep);
    background-image: repeating-linear-gradient(
      45deg, transparent, transparent 3px,
      rgba(255,215,0,0.03) 3px, rgba(255,215,0,0.03) 6px
    );
  }

  #lm-graph-svg { width: 100%; height: 100%; display: block; }

  /* SVG elements */
  .lm-node-group { cursor: pointer; }
  .lm-node-label {
    font-family: "Times New Roman", Times, serif;
    font-size: 11px; font-weight: bold;
    pointer-events: none; dominant-baseline: central; text-anchor: middle;
  }
  .lm-link-line { stroke-width: 1.5; fill: none; }

  /* Info panel */
  #lm-info-panel {
    position: absolute; right: 12px; top: 12px; width: 210px;
    background: var(--wdt-purple); border: 2px inset var(--wdt-gold-dim);
    padding: 10px 12px; display: none;
    font-family: Arial, Helvetica, sans-serif;
  }
  #lm-info-panel.visible { display: block; }
  #lm-info-title {
    color: var(--wdt-gold); font-size: 0.85rem; font-weight: bold;
    border-bottom: 1px solid var(--wdt-gold-dim); padding-bottom: 5px; margin-bottom: 8px;
  }
  #lm-info-body { font-size: 0.72rem; line-height: 1.6; color: var(--wdt-silver); }
  #lm-info-body .lm-info-row { margin-bottom: 5px; }
  #lm-info-body .lm-info-lbl {
    color: var(--wdt-gold-dim); display: block;
    font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.06em;
  }
  #lm-info-link {
    display: block; margin-top: 10px;
    color: var(--wdt-gold); font-size: 0.72rem; text-align: center;
    border: 1px solid var(--wdt-gold-dim); padding: 4px;
    text-decoration: none; background: var(--wdt-purple-deep);
  }
  #lm-info-link:hover { background: var(--wdt-purple-mid); color: #fff; }

  /* Tooltip */
  #lm-tooltip {
    position: absolute; background: var(--wdt-purple-deep);
    border: 1px solid var(--wdt-gold); color: var(--wdt-silver);
    font-size: 0.68rem; padding: 4px 8px;
    pointer-events: none; display: none; max-width: 180px;
    line-height: 1.5; z-index: 10;
    font-family: Arial, Helvetica, sans-serif;
  }

  #lm-zoom-hint {
    position: absolute; bottom: 8px; left: 50%; transform: translateX(-50%);
    font-size: 0.65rem; color: rgba(192,192,192,0.45);
    pointer-events: none; font-style: italic;
    font-family: Arial, Helvetica, sans-serif;
    white-space: nowrap;
  }

  /* Quarto's content panel adds padding we bleed into above;
     ensure the h1 injected by Quarto from the front matter title
     still looks right — it sits above #lm-wrap. */
  #quarto-document-content > h1:first-child,
  .content > h1:first-child {
    /* Quarto already styles this; no override needed.
       Left here as an anchor comment in case tweaks are required. */
  }
</style>

<div id="lm-wrap">

  <!-- ── Controls sidebar ───────────────────────────────────────────── -->
  <div id="lm-sidebar">

    <div class="lm-ctrl-section">
      <div id="lm-subtitle">Loading&hellip;</div>
    </div>

    <div class="lm-ctrl-section">
      <h3>Filter by Group</h3>
      <div class="lm-group-filter" id="lm-group-filters"></div>
    </div>

    <div class="lm-ctrl-section">
      <h3>Edge Direction</h3>
      <div class="lm-edge-mode">
        <label><input type="radio" name="lmedgemode" value="all" checked> All edges</label>
        <label><input type="radio" name="lmedgemode" value="out"> Outbound only</label>
        <label><input type="radio" name="lmedgemode" value="in"> Inbound only</label>
      </div>
    </div>

    <div class="lm-ctrl-section">
      <h3>Layout</h3>
      <button class="lm-ctrl-btn" id="lm-btn-reset">&#x21BA; Reset layout</button>
      <button class="lm-ctrl-btn" id="lm-btn-freeze">&#x2758;&#x2758; Freeze</button>
    </div>

    <div class="lm-ctrl-section">
      <h3>Legend</h3>
      <div class="lm-legend-item">
        <div class="lm-legend-line" style="background:#FFD700;"></div>
        <span>Outbound ref</span>
      </div>
      <div class="lm-legend-item">
        <div class="lm-legend-line" style="background:#888;"></div>
        <span>Inbound ref</span>
      </div>
    </div>

    <div class="lm-ctrl-section">
      <h3>Graph</h3>
      <div id="lm-stats">
        Papers: <span id="lm-stat-papers">&#x2014;</span><br>
        Links: <span id="lm-stat-links">&#x2014;</span><br>
        Shown: <span id="lm-stat-shown">&#x2014;</span>
      </div>
    </div>

  </div><!-- /#lm-sidebar -->

  <!-- ── Canvas ─────────────────────────────────────────────────────── -->
  <div id="lm-canvas-wrap">
    <svg id="lm-graph-svg">
      <defs>
        <marker id="lm-arrow-gold" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="#C0A000"/>
        </marker>
        <marker id="lm-arrow-silver" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="#888"/>
        </marker>
        <marker id="lm-arrow-highlight" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="#FFD700"/>
        </marker>
      </defs>
      <g id="lm-zoom-g">
        <g id="lm-links-layer"></g>
        <g id="lm-nodes-layer"></g>
      </g>
    </svg>
    <div id="lm-tooltip"></div>
    <div id="lm-zoom-hint">scroll to zoom &middot; drag to pan &middot; drag nodes to reposition</div>
  </div><!-- /#lm-canvas-wrap -->

  <!-- ── Info panel ─────────────────────────────────────────────────── -->
  <div id="lm-info-panel">
    <div id="lm-info-title">&#x2014;</div>
    <div id="lm-info-body"></div>
    <a id="lm-info-link" href="#" target="_blank">Open paper &#x2192;</a>
  </div>

</div><!-- /#lm-wrap -->

<script>
// ── Injected at build time by pipeline/link_map.py ────────────────────────
const LM_PAPER_DATA  = __PAPER_DATA__;
const LM_GROUP_ORDER = __GROUP_ORDER__;

// ── Group colour palette ──────────────────────────────────────────────────
const LM_GROUP_COLORS = {
  "Core":           { fill:"#2B0055", stroke:"#FFD700", label:"#FFD700"  },
  "Literature":     { fill:"#1a3300", stroke:"#88cc44", label:"#aaddaa"  },
  "Valuation":      { fill:"#003366", stroke:"#4499ff", label:"#99ccff"  },
  "Corporate":      { fill:"#330033", stroke:"#cc66cc", label:"#ddaadd"  },
  "Revenue":        { fill:"#332200", stroke:"#cc8800", label:"#ffcc66"  },
  "Implementation": { fill:"#003322", stroke:"#44cc99", label:"#aaffdd"  },
  "Analysis":       { fill:"#220033", stroke:"#9966cc", label:"#ccaaff"  },
};

// ── State ─────────────────────────────────────────────────────────────────
let lmNodes = LM_PAPER_DATA.map(d => ({ ...d, x:0, y:0, vx:0, vy:0 }));
let lmLinks = [];
let lmActiveGroups = new Set(LM_GROUP_ORDER);
let lmEdgeMode = "all";
let lmHoveredSc = null;
let lmSelectedSc = null;
let lmFrozen = false;
let lmAnimId = null;

const LM_NODE_W = 72, LM_NODE_H = 32;
const LM_ATTRACT = 0.004, LM_DAMP = 0.97, LM_CENTER_F = 0.003;

// ── Build links ───────────────────────────────────────────────────────────
function lmBuildLinks() {
  const seen = new Set();
  lmLinks = [];
  for (const n of lmNodes) {
    for (const tsc of (n.out || [])) {
      const key = n.sc + "\u2192" + tsc;
      if (!seen.has(key)) {
        seen.add(key);
        const target = lmNodes.find(x => x.sc === tsc);
        if (target) lmLinks.push({ source: n, target, type: "out" });
      }
    }
  }
}

// ── Filtered views ────────────────────────────────────────────────────────
function lmVisibleNodes() { return lmNodes.filter(n => lmActiveGroups.has(n.group)); }

function lmVisibleLinks() {
  const vns = new Set(lmVisibleNodes().map(n => n.sc));
  return lmLinks.filter(l => {
    if (!vns.has(l.source.sc) || !vns.has(l.target.sc)) return false;
    if (lmEdgeMode === "out") return l.type === "out";
    if (lmEdgeMode === "in")  return l.type === "in";
    return true;
  });
}

// ── Layout: force simulation ──────────────────────────────────────────────
function lmInitLayout() {
  const svg = document.getElementById("lm-graph-svg");
  const W = svg.clientWidth || 900, H = svg.clientHeight || 600;
  const vn = lmVisibleNodes();
  const step = (2 * Math.PI) / vn.length;
  const r = Math.min(W, H) * 0.35;
  vn.forEach((n, i) => {
    n.x = W/2 + r * Math.cos(i * step);
    n.y = H/2 + r * Math.sin(i * step);
    n.vx = 0; n.vy = 0;
  });
}

function lmTick() {
  if (lmFrozen) return;
  const svg = document.getElementById("lm-graph-svg");
  const W = svg.clientWidth || 900, H = svg.clientHeight || 600;
  const cx = W/2, cy = H/2;
  const vn = lmVisibleNodes();
  const vl = lmVisibleLinks();

  // Repulsion
  for (let i = 0; i < vn.length; i++) {
    for (let j = i+1; j < vn.length; j++) {
      const a = vn[i], b = vn[j];
      const dx = b.x - a.x, dy = b.y - a.y;
      const dist = Math.sqrt(dx*dx + dy*dy) || 1;
      const IDEAL_DIST = 130;
      const f = Math.max(0, IDEAL_DIST - dist) * 0.4;
      const fx = (dx/dist)*f, fy = (dy/dist)*f;
      a.vx -= fx; a.vy -= fy;
      b.vx += fx; b.vy += fy;
    }
  }

  // Attraction along edges
  for (const l of vl) {
    const dx = l.target.x - l.source.x, dy = l.target.y - l.source.y;
    l.source.vx += dx * LM_ATTRACT; l.source.vy += dy * LM_ATTRACT;
    l.target.vx -= dx * LM_ATTRACT; l.target.vy -= dy * LM_ATTRACT;
  }

  // Centre pull + integrate
  let energy = 0;
  for (const n of vn) {
    n.vx += (cx - n.x) * LM_CENTER_F;
    n.vy += (cy - n.y) * LM_CENTER_F;
    n.vx *= LM_DAMP; n.vy *= LM_DAMP;
    n.x  += n.vx; n.y  += n.vy;
    energy += n.vx*n.vx + n.vy*n.vy;
    n.x = Math.max(LM_NODE_W/2+10, Math.min(W-LM_NODE_W/2-10, n.x));
    n.y = Math.max(LM_NODE_H/2+10, Math.min(H-LM_NODE_H/2-10, n.y));
  }

  lmRender();

  if (energy < 0.08) {
    lmFrozen = true;
    document.getElementById("lm-btn-freeze").textContent = "\u25B6 Resume";
    return;
  }
  lmAnimId = requestAnimationFrame(lmTick);
}

// ── Render ────────────────────────────────────────────────────────────────
const LM_SVG_NS = "http://www.w3.org/2000/svg";
function lmEl(tag, attrs={}) {
  const e = document.createElementNS(LM_SVG_NS, tag);
  for (const [k,v] of Object.entries(attrs)) e.setAttribute(k,v);
  return e;
}

function lmRender() {
  const linksLayer = document.getElementById("lm-links-layer");
  const nodesLayer = document.getElementById("lm-nodes-layer");
  linksLayer.innerHTML = "";
  nodesLayer.innerHTML = "";

  const vl = lmVisibleLinks();
  const vn = lmVisibleNodes();
  const hovConn = lmHoveredSc ? lmGetConnected(lmHoveredSc) : null;

  // Links
  for (const l of vl) {
    const sx=l.source.x, sy=l.source.y, tx=l.target.x, ty=l.target.y;
    const dx=tx-sx, dy=ty-sy, dist=Math.sqrt(dx*dx+dy*dy)||1;
    const ex=tx-(dx/dist)*(LM_NODE_W/2+8), ey=ty-(dy/dist)*(LM_NODE_H/2+8);
    const mx=(sx+tx)/2-dy*0.15, my=(sy+ty)/2+dx*0.15;

    const isHov = hovConn && (
      (l.source.sc===lmHoveredSc && hovConn.out.has(l.target.sc)) ||
      (l.target.sc===lmHoveredSc && hovConn.in.has(l.source.sc))
    );
    const isDim = lmHoveredSc && !isHov;

    linksLayer.appendChild(lmEl("path", {
      d: `M${sx},${sy} Q${mx},${my} ${ex},${ey}`,
      class: "lm-link-line",
      stroke: isHov ? "#FFD700" : (l.type === "out" ? "#C0A000" : "#888"),
      "stroke-width": isHov ? 2.5 : 1.5,
      opacity: isDim ? 0.06 : isHov ? 1 : 0.4,
      "marker-end": isHov ? "url(#lm-arrow-highlight)" : (l.type === "out" ? "url(#lm-arrow-gold)" : "url(#lm-arrow-silver)"),
    }));
  }

  // Nodes
  for (const n of vn) {
    const col = LM_GROUP_COLORS[n.group] || LM_GROUP_COLORS["Analysis"];
    const isHov = n.sc === lmHoveredSc;
    const isSel = n.sc === lmSelectedSc;
    const isDim = lmHoveredSc && !isHov &&
      !(hovConn && (hovConn.out.has(n.sc) || hovConn.in.has(n.sc)));

    const g = lmEl("g", {
      class: "lm-node-group",
      transform: `translate(${n.x-LM_NODE_W/2},${n.y-LM_NODE_H/2})`,
      opacity: isDim ? 0.18 : 1,
    });

    // Drop shadow
    if (!isDim) g.appendChild(lmEl("rect", {
      x:3, y:3, width:LM_NODE_W, height:LM_NODE_H, fill:"rgba(0,0,0,0.6)"
    }));

    // Body
    g.appendChild(lmEl("rect", {
      x:0, y:0, width:LM_NODE_W, height:LM_NODE_H,
      fill: col.fill,
      stroke: (isHov||isSel) ? "#FFD700" : col.stroke,
      "stroke-width": (isHov||isSel) ? 2.5 : 1.5,
    }));

    // Shortcode label
    const lbl = lmEl("text", {
      x:LM_NODE_W/2, y:LM_NODE_H/2, class:"lm-node-label", fill:col.label
    });
    lbl.textContent = n.sc;
    g.appendChild(lbl);

    // Superseded dot
    if (n.status === "superseded") g.appendChild(lmEl("circle", {
      cx:LM_NODE_W-5, cy:5, r:3, fill:"#cc0000"
    }));

    // Hit area (transparent — handles all mouse events)
    const hit = lmEl("rect", { x:0, y:0, width:LM_NODE_W, height:LM_NODE_H, fill:"transparent" });
    hit.addEventListener("mouseenter", e => lmOnHover(n, e));
    hit.addEventListener("mouseleave", lmOnLeave);
    hit.addEventListener("click", () => lmOnClick(n));
    hit.addEventListener("mousedown", e => lmStartDrag(n, e));
    g.appendChild(hit);

    nodesLayer.appendChild(g);
  }

  lmApplyZoom();
}

// ── Graph helpers ─────────────────────────────────────────────────────────
function lmGetConnected(sc) {
  const out = new Set(), inn = new Set();
  for (const l of lmVisibleLinks()) {
    if (l.source.sc === sc) out.add(l.target.sc);
    if (l.target.sc === sc) inn.add(l.source.sc);
  }
  return { out, in: inn };
}

// ── Drag ──────────────────────────────────────────────────────────────────
let lmDragging = null, lmDragOff = { x:0, y:0 };

function lmStartDrag(n, e) {
  lmDragging = n;
  const r = document.getElementById("lm-graph-svg").getBoundingClientRect();
  lmDragOff.x = (e.clientX - r.left - lmZoom.x) / lmZoom.k - n.x;
  lmDragOff.y = (e.clientY - r.top  - lmZoom.y) / lmZoom.k - n.y;
  e.stopPropagation();
}

document.addEventListener("mousemove", e => {
  if (lmDragging) {
    const r = document.getElementById("lm-graph-svg").getBoundingClientRect();
    lmDragging.x = (e.clientX - r.left - lmZoom.x) / lmZoom.k - lmDragOff.x;
    lmDragging.y = (e.clientY - r.top  - lmZoom.y) / lmZoom.k - lmDragOff.y;
    lmDragging.vx = 0; lmDragging.vy = 0;
    if (lmFrozen) lmRender();
  } else if (lmIsPanning) {
    lmZoom.x += e.clientX - lmPanStart.x;
    lmZoom.y += e.clientY - lmPanStart.y;
    lmPanStart = { x:e.clientX, y:e.clientY };
    lmApplyZoom();
  }
});

document.addEventListener("mouseup", () => { lmDragging = null; lmIsPanning = false; });

// ── Pan & zoom ────────────────────────────────────────────────────────────
let lmZoom = { x:0, y:0, k:1 };
let lmIsPanning = false, lmPanStart = { x:0, y:0 };

document.getElementById("lm-canvas-wrap").addEventListener("mousedown", e => {
  if (e.target.id === "lm-graph-svg" || e.target.id === "lm-zoom-g") {
    lmIsPanning = true; lmPanStart = { x:e.clientX, y:e.clientY };
  }
});

document.getElementById("lm-canvas-wrap").addEventListener("wheel", e => {
  e.preventDefault();
  const r = document.getElementById("lm-graph-svg").getBoundingClientRect();
  const mx = e.clientX - r.left, my = e.clientY - r.top;
  const d = e.deltaY > 0 ? 0.85 : 1.18;
  lmZoom.x = mx - (mx - lmZoom.x)*d;
  lmZoom.y = my - (my - lmZoom.y)*d;
  lmZoom.k = Math.max(0.2, Math.min(4, lmZoom.k * d));
  lmApplyZoom();
}, { passive:false });

function lmApplyZoom() {
  document.getElementById("lm-zoom-g").setAttribute(
    "transform", `translate(${lmZoom.x},${lmZoom.y}) scale(${lmZoom.k})`
  );
}

// ── Node events ───────────────────────────────────────────────────────────
const lmTooltip = document.getElementById("lm-tooltip");

function lmOnHover(n, e) {
  lmHoveredSc = n.sc;
  const c = lmGetConnected(n.sc);
  lmTooltip.innerHTML =
    `<strong style="color:#FFD700">${n.sc}</strong><br>${n.title}<br>` +
    `<span style="color:#aaa">&#x2197; ${c.out.size} out &middot; &#x2199; ${c.in.size} in</span>`;
  lmTooltip.style.display = "block";
  if (!lmFrozen) return;
  lmRender();
}

function lmOnLeave() {
  lmHoveredSc = null;
  lmTooltip.style.display = "none";
  if (lmFrozen) lmRender();
}

document.getElementById("lm-canvas-wrap").addEventListener("mousemove", e => {
  if (lmTooltip.style.display !== "block") return;
  const wrap = document.getElementById("lm-canvas-wrap").getBoundingClientRect();
  let tx = e.clientX - wrap.left + 14;
  let ty = e.clientY - wrap.top  - 10;
  if (tx + 190 > wrap.width) tx -= 200;
  lmTooltip.style.left = tx + "px";
  lmTooltip.style.top  = ty + "px";
});

function lmOnClick(n) {
  lmSelectedSc = lmSelectedSc === n.sc ? null : n.sc;
  if (lmSelectedSc) lmShowInfo(n);
  else document.getElementById("lm-info-panel").classList.remove("visible");
  if (lmFrozen) lmRender();
}

function lmShowInfo(n) {
  const c = lmGetConnected(n.sc);
  document.getElementById("lm-info-title").textContent = n.sc + " \u2014 " + n.group;
  let html = `<div class="lm-info-row"><span class="lm-info-lbl">Title</span>${n.title}</div>`;
  html += `<div class="lm-info-row"><span class="lm-info-lbl">Cites (${c.out.size})</span>${c.out.size ? [...c.out].join(", ") : "\u2014"}</div>`;
  html += `<div class="lm-info-row"><span class="lm-info-lbl">Cited by (${c.in.size})</span>${c.in.size ? [...c.in].join(", ") : "\u2014"}</div>`;
  if (n.status === "superseded") html += `<div class="lm-info-row" style="color:#cc4444">\u26A0 Superseded</div>`;
  document.getElementById("lm-info-body").innerHTML = html;
  document.getElementById("lm-info-link").href = n.url;
  document.getElementById("lm-info-panel").classList.add("visible");
}

document.getElementById("lm-graph-svg").addEventListener("click", e => {
  if (e.target.id === "lm-graph-svg") {
    lmSelectedSc = null;
    document.getElementById("lm-info-panel").classList.remove("visible");
    if (lmFrozen) lmRender();
  }
});

// ── Sidebar controls ──────────────────────────────────────────────────────
function lmBuildFilters() {
  const container = document.getElementById("lm-group-filters");
  for (const g of LM_GROUP_ORDER) {
    const col = LM_GROUP_COLORS[g] || { fill:"#222", stroke:"#aaa" };
    const wrap = document.createElement("label");
    const cb = document.createElement("input");
    cb.type = "checkbox"; cb.checked = true; cb.dataset.group = g;
    cb.addEventListener("change", () => {
      cb.checked ? lmActiveGroups.add(g) : lmActiveGroups.delete(g);
      lmUpdateStats();
      if (lmFrozen) lmRender();
    });
    const dot = document.createElement("span");
    dot.className = "lm-group-dot";
    dot.style.cssText = `background:${col.fill};border-color:${col.stroke};`;
    wrap.appendChild(cb);
    wrap.appendChild(dot);
    wrap.appendChild(document.createTextNode(" " + g));
    container.appendChild(wrap);
  }
}

document.querySelectorAll('input[name="lmedgemode"]').forEach(r =>
  r.addEventListener("change", e => {
    lmEdgeMode = e.target.value;
    lmUpdateStats();
    if (lmFrozen) lmRender();
  })
);

document.getElementById("lm-btn-reset").addEventListener("click", () => {
  lmFrozen = false;
  document.getElementById("lm-btn-freeze").textContent = "\u2758\u2758 Freeze";
  cancelAnimationFrame(lmAnimId);
  lmInitLayout();
  lmAnimId = requestAnimationFrame(lmTick);
});

document.getElementById("lm-btn-freeze").addEventListener("click", () => {
  lmFrozen = !lmFrozen;
  document.getElementById("lm-btn-freeze").textContent =
    lmFrozen ? "\u25B6 Resume" : "\u2758\u2758 Freeze";
  if (!lmFrozen) lmAnimId = requestAnimationFrame(lmTick);
});

function lmUpdateStats() {
  const vn = lmVisibleNodes(), vl = lmVisibleLinks();
  document.getElementById("lm-stat-papers").textContent = lmNodes.length;
  document.getElementById("lm-stat-links").textContent  = lmLinks.length;
  document.getElementById("lm-stat-shown").textContent  = `${vn.length}p / ${vl.length}l`;
  document.getElementById("lm-subtitle").textContent =
    `${lmNodes.length} papers \u00B7 ${lmLinks.length} links \u00B7 hover to explore \u00B7 click to open`;
}

// ── Init ──────────────────────────────────────────────────────────────────
window.addEventListener("load", () => {
  lmBuildLinks();
  lmBuildFilters();
  lmUpdateStats();
  lmInitLayout();
  lmAnimId = requestAnimationFrame(lmTick);
});
</script>
```
"""

# ── Generator ─────────────────────────────────────────────────────────────────


def generate_link_map_html(
    dest_path: Path,
    refs_data: dict,
    link_map: dict,
) -> None:
    """
    Generate _build/link-map.qmd from internal_papers data.

    The output is a Quarto .qmd file (page-layout: full) so the graph renders
    inside the Quarto site frame — navbar and footer are present, Quarto's
    sidebar and TOC are suppressed for this page only to maximise canvas width.

    Args:
        dest_path:  Nominal output path (e.g. _build/link-map.html).
                    The .html suffix is replaced with .qmd automatically.
        refs_data:  Parsed references.json dict (from config.SiteConfig.refs_data)
        link_map:   {SHORTCODE: "page.html"} (from config.SiteConfig.link_map)
    """
    paper_data  = _build_paper_data(refs_data, link_map)
    group_order = _GROUP_ORDER

    # Serialise as compact JS literals — valid JS array/object syntax
    paper_data_js  = json.dumps(paper_data,  ensure_ascii=False, separators=(",", ":"))
    group_order_js = json.dumps(group_order, ensure_ascii=False)

    body = _BODY_TEMPLATE.replace("__PAPER_DATA__",  paper_data_js)
    body = body.replace("__GROUP_ORDER__", group_order_js)

    qmd_content = _FRONT_MATTER + body

    # Always write as .qmd regardless of the suffix in dest_path
    dest_qmd = Path(dest_path).with_suffix(".qmd")
    dest_qmd.parent.mkdir(parents=True, exist_ok=True)
    dest_qmd.write_text(qmd_content, encoding="utf-8")
    print(f"  [link_map] wrote {dest_qmd} ({len(paper_data)} papers)")