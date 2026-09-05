"""
pipeline/pages/link_map.py

Generates _build/link-map.html — the interactive WDT paper cross-reference
graph. Reads paper records from refs_data (registry/references.json) and
injects them as a JS data block into the HTML template.

Called by preprocess.py as step (12), after all other page generators.

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


# ── HTML template ─────────────────────────────────────────────────────────────
# __PAPER_DATA__ is replaced with the serialised JS array at generation time.
# __GROUP_ORDER__ is replaced with the serialised group name list.

_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WDT Paper Link Map</title>
<style>
  :root {
    --wdt-purple-deep: #1a0033;
    --wdt-purple:      #2B0055;
    --wdt-purple-mid:  #3d0080;
    --wdt-gold:        #FFD700;
    --wdt-gold-dim:    #C0A000;
    --wdt-silver:      #C0C0C0;
    --wdt-lavender:    #F5F0FF;
    --wdt-green:       #16a34a;
    --wdt-red:         #cc0000;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background-color: var(--wdt-purple-deep);
    background-image: repeating-linear-gradient(
      45deg, transparent, transparent 3px,
      rgba(255,215,0,0.04) 3px, rgba(255,215,0,0.04) 6px
    );
    background-attachment: fixed;
    font-family: "Times New Roman", Times, serif;
    color: var(--wdt-silver);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  /* Header */
  #header {
    background: var(--wdt-purple);
    border-bottom: 3px double var(--wdt-gold);
    padding: 10px 16px;
    display: flex;
    align-items: baseline;
    gap: 16px;
    flex-wrap: wrap;
  }
  #header h1 { font-size: 1.25rem; color: var(--wdt-gold); white-space: nowrap; }
  #header .subtitle { font-size: 0.8rem; color: var(--wdt-silver); font-style: italic; }

  /* Layout */
  #main { display: flex; flex: 1; min-height: 0; }

  /* Sidebar */
  #sidebar {
    width: 200px; min-width: 200px;
    background: var(--wdt-purple);
    border-right: 2px solid var(--wdt-gold-dim);
    padding: 12px 10px;
    display: flex; flex-direction: column; gap: 14px;
    overflow-y: auto;
  }
  .ctrl-section {
    border: 1px inset var(--wdt-gold-dim);
    background: var(--wdt-purple-deep);
    padding: 8px;
  }
  .ctrl-section h3 {
    font-size: 0.7rem; color: var(--wdt-gold);
    text-transform: uppercase; letter-spacing: 0.08em;
    margin-bottom: 7px;
    border-bottom: 1px solid var(--wdt-gold-dim); padding-bottom: 3px;
  }
  .group-filter { display: flex; flex-direction: column; gap: 5px; }
  .group-filter label {
    display: flex; align-items: center; gap: 6px;
    font-size: 0.72rem; cursor: pointer; color: var(--wdt-silver);
  }
  .group-filter label:hover { color: var(--wdt-gold); }
  .group-dot { width: 10px; height: 10px; border: 1px solid rgba(255,255,255,0.3); flex-shrink: 0; }
  .edge-mode { display: flex; flex-direction: column; gap: 5px; }
  .edge-mode label {
    display: flex; align-items: center; gap: 6px;
    font-size: 0.72rem; cursor: pointer; color: var(--wdt-silver);
  }
  .edge-mode label:hover { color: var(--wdt-gold); }
  .ctrl-btn {
    display: block; width: 100%;
    background: var(--wdt-purple-mid); color: var(--wdt-gold);
    border: 2px outset var(--wdt-gold-dim);
    font-family: "Times New Roman", Times, serif;
    font-size: 0.72rem; padding: 4px 6px;
    cursor: pointer; text-align: center; margin-bottom: 4px;
  }
  .ctrl-btn:hover { background: var(--wdt-purple); border-style: inset; }
  .legend-item { display: flex; align-items: center; gap: 6px; font-size: 0.68rem; color: var(--wdt-silver); margin-bottom: 4px; }
  .legend-line { width: 24px; height: 2px; flex-shrink: 0; }
  #stats { font-size: 0.68rem; color: var(--wdt-silver); line-height: 1.7; }
  #stats span { color: var(--wdt-gold); }

  /* Canvas */
  #canvas-wrap { flex: 1; position: relative; overflow: hidden; }
  #graph-svg { width: 100%; height: 100%; display: block; }

  /* SVG elements */
  .node-group { cursor: pointer; }
  .node-label {
    font-family: "Times New Roman", Times, serif; font-size: 11px; font-weight: bold;
    pointer-events: none; dominant-baseline: central; text-anchor: middle;
  }
  .link-line { stroke-width: 1.5; fill: none; }

  /* Info panel */
  #info-panel {
    position: absolute; right: 12px; top: 12px; width: 210px;
    background: var(--wdt-purple); border: 2px inset var(--wdt-gold-dim);
    padding: 10px 12px; display: none;
  }
  #info-panel.visible { display: block; }
  #info-title { color: var(--wdt-gold); font-size: 0.85rem; font-weight: bold; border-bottom: 1px solid var(--wdt-gold-dim); padding-bottom: 5px; margin-bottom: 8px; }
  #info-body { font-size: 0.72rem; line-height: 1.6; color: var(--wdt-silver); }
  #info-body .info-row { margin-bottom: 5px; }
  #info-body .info-lbl { color: var(--wdt-gold-dim); display: block; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.06em; }
  #info-link { display: block; margin-top: 10px; color: var(--wdt-gold); font-size: 0.72rem; text-align: center; border: 1px solid var(--wdt-gold-dim); padding: 4px; text-decoration: none; background: var(--wdt-purple-deep); }
  #info-link:hover { background: var(--wdt-purple-mid); }

  /* Tooltip */
  #tooltip {
    position: absolute; background: var(--wdt-purple-deep); border: 1px solid var(--wdt-gold);
    color: var(--wdt-silver); font-size: 0.68rem; padding: 4px 8px;
    pointer-events: none; display: none; max-width: 180px; line-height: 1.5; z-index: 10;
  }

  #zoom-hint {
    position: absolute; bottom: 8px; left: 50%; transform: translateX(-50%);
    font-size: 0.65rem; color: rgba(192,192,192,0.5); pointer-events: none; font-style: italic;
  }
</style>
</head>
<body>

<div id="header">
  <h1>&#x2B21; WDT Paper Link Map</h1>
  <span class="subtitle" id="header-subtitle">Loading&hellip;</span>
</div>

<div id="main">
  <div id="sidebar">
    <div class="ctrl-section">
      <h3>Filter by Group</h3>
      <div class="group-filter" id="group-filters"></div>
    </div>
    <div class="ctrl-section">
      <h3>Edge Direction</h3>
      <div class="edge-mode">
        <label><input type="radio" name="edgemode" value="all" checked> All edges</label>
        <label><input type="radio" name="edgemode" value="out"> Outbound only</label>
        <label><input type="radio" name="edgemode" value="in"> Inbound only</label>
      </div>
    </div>
    <div class="ctrl-section">
      <h3>Layout</h3>
      <button class="ctrl-btn" id="btn-reset">&#x21BA; Reset layout</button>
      <button class="ctrl-btn" id="btn-freeze">&#x2758;&#x2758; Freeze</button>
    </div>
    <div class="ctrl-section">
      <h3>Legend</h3>
      <div class="legend-item"><div class="legend-line" style="background:#FFD700;"></div><span>Outbound ref</span></div>
      <div class="legend-item"><div class="legend-line" style="background:#888;"></div><span>Inbound ref</span></div>
    </div>
    <div class="ctrl-section">
      <h3>Graph</h3>
      <div id="stats">Papers: <span id="stat-papers">&#x2014;</span><br>Links: <span id="stat-links">&#x2014;</span><br>Shown: <span id="stat-shown">&#x2014;</span></div>
    </div>
  </div>

  <div id="canvas-wrap">
    <svg id="graph-svg">
      <defs>
        <marker id="arrow-gold" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="#C0A000"/>
        </marker>
        <marker id="arrow-silver" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="#888"/>
        </marker>
        <marker id="arrow-highlight" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
          <path d="M0,0 L0,6 L8,3 z" fill="#FFD700"/>
        </marker>
      </defs>
      <g id="zoom-g">
        <g id="links-layer"></g>
        <g id="nodes-layer"></g>
      </g>
    </svg>
    <div id="tooltip"></div>
    <div id="zoom-hint">scroll to zoom &middot; drag to pan &middot; drag nodes to reposition</div>
  </div>

  <div id="info-panel">
    <div id="info-title">&#x2014;</div>
    <div id="info-body"></div>
    <a id="info-link" href="#" target="_blank">Open paper &#x2192;</a>
  </div>
</div>

<script>
// ── Injected at build time by pipeline/pages/link_map.py ──────────────────
const PAPER_DATA  = __PAPER_DATA__;
const GROUP_ORDER = __GROUP_ORDER__;

// ── Group colour palette ──────────────────────────────────────────────────
const GROUP_COLORS = {
  "Core":           { fill:"#2B0055", stroke:"#FFD700",  label:"#FFD700"  },
  "Literature":     { fill:"#1a3300", stroke:"#88cc44",  label:"#aaddaa"  },
  "Valuation":      { fill:"#003366", stroke:"#4499ff",  label:"#99ccff"  },
  "Corporate":      { fill:"#330033", stroke:"#cc66cc",  label:"#ddaadd"  },
  "Revenue":        { fill:"#332200", stroke:"#cc8800",  label:"#ffcc66"  },
  "Implementation": { fill:"#003322", stroke:"#44cc99",  label:"#aaffdd"  },
  "Analysis":       { fill:"#220033", stroke:"#9966cc",  label:"#ccaaff"  },
};

// ── State ─────────────────────────────────────────────────────────────────
let nodes = PAPER_DATA.map(d => ({ ...d, x:0, y:0, vx:0, vy:0 }));
let links = [];
let activeGroups = new Set(GROUP_ORDER);
let edgeMode = "all";
let hoveredSc = null;
let selectedSc = null;
let frozen = false;
let animId = null;

const NODE_W = 72, NODE_H = 32;
const REPEL = 1800, ATTRACT = 0.012, DAMP = 0.94, CENTER_F = 0.006;

// ── Build links ───────────────────────────────────────────────────────────
function buildLinks() {
  const seen = new Set();
  links = [];
  for (const n of nodes) {
    for (const tsc of (n.out || [])) {
      const key = n.sc + "\u2192" + tsc;
      if (!seen.has(key)) {
        seen.add(key);
        const target = nodes.find(x => x.sc === tsc);
        if (target) links.push({ source: n, target, type: "out" });
      }
    }
  }
}

// ── Filtered views ────────────────────────────────────────────────────────
function visibleNodes() { return nodes.filter(n => activeGroups.has(n.group)); }

function visibleLinks() {
  const vns = new Set(visibleNodes().map(n => n.sc));
  return links.filter(l => {
    if (!vns.has(l.source.sc) || !vns.has(l.target.sc)) return false;
    if (edgeMode === "out") return l.type === "out";
    if (edgeMode === "in")  return l.type === "in";
    return true;
  });
}

// ── Layout: force simulation ──────────────────────────────────────────────
function initLayout() {
  const svg = document.getElementById("graph-svg");
  const W = svg.clientWidth || 900, H = svg.clientHeight || 600;
  const vn = visibleNodes();
  const step = (2 * Math.PI) / vn.length;
  const r = Math.min(W, H) * 0.35;
  vn.forEach((n, i) => {
    n.x = W/2 + r * Math.cos(i * step);
    n.y = H/2 + r * Math.sin(i * step);
    n.vx = 0; n.vy = 0;
  });
}

function tick() {
  if (frozen) return;
  const svg = document.getElementById("graph-svg");
  const W = svg.clientWidth || 900, H = svg.clientHeight || 600;
  const cx = W/2, cy = H/2;
  const vn = visibleNodes();
  const vl = visibleLinks();

  // Repulsion
  for (let i = 0; i < vn.length; i++) {
    for (let j = i+1; j < vn.length; j++) {
      const a = vn[i], b = vn[j];
      const dx = b.x - a.x, dy = b.y - a.y;
      const dist = Math.sqrt(dx*dx + dy*dy) || 1;
      const f = REPEL / (dist * dist);
      const fx = (dx/dist)*f, fy = (dy/dist)*f;
      a.vx -= fx; a.vy -= fy;
      b.vx += fx; b.vy += fy;
    }
  }

  // Attraction along edges
  for (const l of vl) {
    const dx = l.target.x - l.source.x, dy = l.target.y - l.source.y;
    l.source.vx += dx * ATTRACT; l.source.vy += dy * ATTRACT;
    l.target.vx -= dx * ATTRACT; l.target.vy -= dy * ATTRACT;
  }

  // Centre pull + integrate
  let energy = 0;
  for (const n of vn) {
    n.vx += (cx - n.x) * CENTER_F;
    n.vy += (cy - n.y) * CENTER_F;
    n.vx *= DAMP; n.vy *= DAMP;
    n.x  += n.vx; n.y  += n.vy;
    energy += n.vx*n.vx + n.vy*n.vy;
    n.x = Math.max(NODE_W/2+10, Math.min(W-NODE_W/2-10, n.x));
    n.y = Math.max(NODE_H/2+10, Math.min(H-NODE_H/2-10, n.y));
  }

  render();

  if (energy < 0.08) {
    frozen = true;
    document.getElementById("btn-freeze").textContent = "\u25B6 Resume";
    return;
  }
  animId = requestAnimationFrame(tick);
}

// ── Render ────────────────────────────────────────────────────────────────
const svgNS = "http://www.w3.org/2000/svg";
function el(tag, attrs={}) {
  const e = document.createElementNS(svgNS, tag);
  for (const [k,v] of Object.entries(attrs)) e.setAttribute(k,v);
  return e;
}

function render() {
  const linksLayer = document.getElementById("links-layer");
  const nodesLayer = document.getElementById("nodes-layer");
  linksLayer.innerHTML = "";
  nodesLayer.innerHTML = "";

  const vl = visibleLinks();
  const vn = visibleNodes();
  const hovConn = hoveredSc ? getConnected(hoveredSc) : null;

  // Links
  for (const l of vl) {
    const sx=l.source.x, sy=l.source.y, tx=l.target.x, ty=l.target.y;
    const dx=tx-sx, dy=ty-sy, dist=Math.sqrt(dx*dx+dy*dy)||1;
    const ex=tx-(dx/dist)*(NODE_W/2+8), ey=ty-(dy/dist)*(NODE_H/2+8);
    const mx=(sx+tx)/2-dy*0.15, my=(sy+ty)/2+dx*0.15;

    const isHov = hovConn && (
      (l.source.sc===hoveredSc && hovConn.out.has(l.target.sc)) ||
      (l.target.sc===hoveredSc && hovConn.in.has(l.source.sc))
    );
    const isDim = hoveredSc && !isHov;

    linksLayer.appendChild(el("path", {
      d: `M${sx},${sy} Q${mx},${my} ${ex},${ey}`,
      class: "link-line",
      stroke: isHov ? "#FFD700" : "#888",
      "stroke-width": isHov ? 2.5 : 1.5,
      opacity: isDim ? 0.06 : isHov ? 1 : 0.4,
      "marker-end": isHov ? "url(#arrow-highlight)" : "url(#arrow-silver)",
    }));
  }

  // Nodes
  for (const n of vn) {
    const col = GROUP_COLORS[n.group] || GROUP_COLORS["Analysis"];
    const isHov = n.sc === hoveredSc;
    const isSel = n.sc === selectedSc;
    const isDim = hoveredSc && !isHov &&
      !(hovConn && (hovConn.out.has(n.sc) || hovConn.in.has(n.sc)));

    const g = el("g", {
      class: "node-group",
      transform: `translate(${n.x-NODE_W/2},${n.y-NODE_H/2})`,
      opacity: isDim ? 0.18 : 1,
    });

    // Drop shadow
    if (!isDim) g.appendChild(el("rect", { x:3, y:3, width:NODE_W, height:NODE_H, fill:"rgba(0,0,0,0.6)" }));

    // Body
    g.appendChild(el("rect", {
      x:0, y:0, width:NODE_W, height:NODE_H,
      fill: col.fill,
      stroke: (isHov||isSel) ? "#FFD700" : col.stroke,
      "stroke-width": (isHov||isSel) ? 2.5 : 1.5,
    }));

    // Shortcode
    const lbl = el("text", { x:NODE_W/2, y:NODE_H/2, class:"node-label", fill:col.label });
    lbl.textContent = n.sc;
    g.appendChild(lbl);

    // Superseded dot
    if (n.status === "superseded") g.appendChild(el("circle", { cx:NODE_W-5, cy:5, r:3, fill:"#cc0000" }));

    // Hit area
    const hit = el("rect", { x:0, y:0, width:NODE_W, height:NODE_H, fill:"transparent" });
    hit.addEventListener("mouseenter", e => onHover(n, e));
    hit.addEventListener("mouseleave", onLeave);
    hit.addEventListener("click", () => onClick(n));
    hit.addEventListener("mousedown", e => startDrag(n, e));
    g.appendChild(hit);

    nodesLayer.appendChild(g);
  }

  applyZoom();
}

// ── Graph helpers ─────────────────────────────────────────────────────────
function getConnected(sc) {
  const out = new Set(), inn = new Set();
  for (const l of visibleLinks()) {
    if (l.source.sc === sc) out.add(l.target.sc);
    if (l.target.sc === sc) inn.add(l.source.sc);
  }
  return { out, in: inn };
}

// ── Drag ──────────────────────────────────────────────────────────────────
let dragging = null, dragOff = { x:0, y:0 };

function startDrag(n, e) {
  dragging = n;
  const r = document.getElementById("graph-svg").getBoundingClientRect();
  dragOff.x = (e.clientX - r.left - zoom.x) / zoom.k - n.x;
  dragOff.y = (e.clientY - r.top  - zoom.y) / zoom.k - n.y;
  e.stopPropagation();
}

document.addEventListener("mousemove", e => {
  if (dragging) {
    const r = document.getElementById("graph-svg").getBoundingClientRect();
    dragging.x = (e.clientX - r.left - zoom.x) / zoom.k - dragOff.x;
    dragging.y = (e.clientY - r.top  - zoom.y) / zoom.k - dragOff.y;
    dragging.vx = 0; dragging.vy = 0;
    if (frozen) render();
  } else if (isPanning) {
    zoom.x += e.clientX - panStart.x;
    zoom.y += e.clientY - panStart.y;
    panStart = { x:e.clientX, y:e.clientY };
    applyZoom();
  }
});

document.addEventListener("mouseup", () => { dragging = null; isPanning = false; });

// ── Pan & zoom ────────────────────────────────────────────────────────────
let zoom = { x:0, y:0, k:1 };
let isPanning = false, panStart = { x:0, y:0 };

document.getElementById("canvas-wrap").addEventListener("mousedown", e => {
  if (e.target.id === "graph-svg" || e.target.id === "zoom-g") {
    isPanning = true; panStart = { x:e.clientX, y:e.clientY };
  }
});

document.getElementById("canvas-wrap").addEventListener("wheel", e => {
  e.preventDefault();
  const r = document.getElementById("graph-svg").getBoundingClientRect();
  const mx = e.clientX - r.left, my = e.clientY - r.top;
  const d = e.deltaY > 0 ? 0.85 : 1.18;
  zoom.x = mx - (mx - zoom.x)*d;
  zoom.y = my - (my - zoom.y)*d;
  zoom.k = Math.max(0.2, Math.min(4, zoom.k * d));
  applyZoom();
}, { passive:false });

function applyZoom() {
  document.getElementById("zoom-g").setAttribute(
    "transform", `translate(${zoom.x},${zoom.y}) scale(${zoom.k})`
  );
}

// ── Node events ───────────────────────────────────────────────────────────
const tooltip = document.getElementById("tooltip");

function onHover(n, e) {
  hoveredSc = n.sc;
  const c = getConnected(n.sc);
  tooltip.innerHTML = `<strong style="color:#FFD700">${n.sc}</strong><br>${n.title}<br>
    <span style="color:#aaa">&#x2197; ${c.out.size} out &middot; &#x2199; ${c.in.size} in</span>`;
  tooltip.style.display = "block";
  if (!frozen) return; // tick() will render; only manual render if frozen
  render();
}

function onLeave() {
  hoveredSc = null;
  tooltip.style.display = "none";
  if (frozen) render();
}

document.getElementById("canvas-wrap").addEventListener("mousemove", e => {
  if (tooltip.style.display !== "block") return;
  const wrap = document.getElementById("canvas-wrap").getBoundingClientRect();
  let tx = e.clientX - wrap.left + 14;
  let ty = e.clientY - wrap.top  - 10;
  if (tx + 190 > wrap.width) tx -= 200;
  tooltip.style.left = tx + "px";
  tooltip.style.top  = ty + "px";
});

function onClick(n) {
  selectedSc = selectedSc === n.sc ? null : n.sc;
  if (selectedSc) showInfo(n);
  else document.getElementById("info-panel").classList.remove("visible");
  if (frozen) render();
}

function showInfo(n) {
  const c = getConnected(n.sc);
  document.getElementById("info-title").textContent = n.sc + " \u2014 " + n.group;
  let html = `<div class="info-row"><span class="info-lbl">Title</span>${n.title}</div>`;
  html += `<div class="info-row"><span class="info-lbl">Cites (${c.out.size})</span>${c.out.size ? [...c.out].join(", ") : "\u2014"}</div>`;
  html += `<div class="info-row"><span class="info-lbl">Cited by (${c.in.size})</span>${c.in.size ? [...c.in].join(", ") : "\u2014"}</div>`;
  if (n.status === "superseded") html += `<div class="info-row" style="color:#cc4444">\u26A0 Superseded</div>`;
  document.getElementById("info-body").innerHTML = html;
  document.getElementById("info-link").href = n.url;
  document.getElementById("info-panel").classList.add("visible");
}

document.getElementById("graph-svg").addEventListener("click", e => {
  if (e.target.id === "graph-svg") {
    selectedSc = null;
    document.getElementById("info-panel").classList.remove("visible");
    if (frozen) render();
  }
});

// ── Sidebar controls ──────────────────────────────────────────────────────
function buildFilters() {
  const container = document.getElementById("group-filters");
  for (const g of GROUP_ORDER) {
    const col = GROUP_COLORS[g] || { fill:"#222", stroke:"#aaa" };
    const wrap = document.createElement("label");
    const cb = document.createElement("input");
    cb.type = "checkbox"; cb.checked = true; cb.dataset.group = g;
    cb.addEventListener("change", () => {
      cb.checked ? activeGroups.add(g) : activeGroups.delete(g);
      updateStats(); if (frozen) render();
    });
    const dot = document.createElement("span");
    dot.className = "group-dot";
    dot.style.cssText = `background:${col.fill};border-color:${col.stroke};`;
    wrap.appendChild(cb); wrap.appendChild(dot); wrap.appendChild(document.createTextNode(" " + g));
    container.appendChild(wrap);
  }
}

document.querySelectorAll('input[name="edgemode"]').forEach(r =>
  r.addEventListener("change", e => { edgeMode = e.target.value; updateStats(); if (frozen) render(); })
);

document.getElementById("btn-reset").addEventListener("click", () => {
  frozen = false;
  document.getElementById("btn-freeze").textContent = "\u2758\u2758 Freeze";
  cancelAnimationFrame(animId);
  initLayout();
  animId = requestAnimationFrame(tick);
});

document.getElementById("btn-freeze").addEventListener("click", () => {
  frozen = !frozen;
  document.getElementById("btn-freeze").textContent = frozen ? "\u25B6 Resume" : "\u2758\u2758 Freeze";
  if (!frozen) animId = requestAnimationFrame(tick);
});

function updateStats() {
  const vn = visibleNodes(), vl = visibleLinks();
  document.getElementById("stat-papers").textContent = nodes.length;
  document.getElementById("stat-links").textContent = links.length;
  document.getElementById("stat-shown").textContent = `${vn.length}p / ${vl.length}l`;
  document.getElementById("header-subtitle").textContent =
    `Internal cross-reference graph \u00B7 ${nodes.length} papers \u00B7 ${links.length} links \u00B7 hover to explore \u00B7 click to open`;
}

// ── Init ──────────────────────────────────────────────────────────────────
window.addEventListener("load", () => {
  buildLinks();
  buildFilters();
  updateStats();
  initLayout();
  animId = requestAnimationFrame(tick);
});
</script>
</body>
</html>
"""


def generate_link_map_html(
    dest_path: Path,
    refs_data: dict,
    link_map: dict,
) -> None:
    """
    Generate _build/link-map.html from internal_papers data.

    Args:
        dest_path:  Full path to write the output file (e.g. _build/link-map.html)
        refs_data:  Parsed references.json dict (from config.SiteConfig.refs_data)
        link_map:   {SHORTCODE: "page.html"} (from config.SiteConfig.link_map)
    """
    paper_data = _build_paper_data(refs_data, link_map)
    group_order = _GROUP_ORDER

    # Serialise as compact JS literals — no trailing comma, valid JS array syntax
    paper_data_js = json.dumps(paper_data, ensure_ascii=False, separators=(",", ":"))
    group_order_js = json.dumps(group_order, ensure_ascii=False)

    html = _TEMPLATE.replace("__PAPER_DATA__", paper_data_js)
    html = html.replace("__GROUP_ORDER__", group_order_js)

    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(html, encoding="utf-8")
    print(f"  [link_map] wrote {dest_path} ({len(paper_data)} papers)")
