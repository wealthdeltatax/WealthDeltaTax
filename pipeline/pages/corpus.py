"""
pages/corpus.py — generate the Papers index page (corpus.qmd).

Reads paper metadata from the pipeline; writes one .qmd file containing:
  • A configurable reading-path selector with estimated reading times
  • A coloured domain chip map (highlight/dim on path selection)
  • A word-count / reading-time toggle
  • Condensed per-section tables (4 columns)

Call: generate_corpus_qmd(dest_path, link_map, paper_meta)

──────────────────────────────────────────────────────────────────────────────
READING PATHS — edit freely.
Each entry in READING_PATHS is a dict with:
  id        str   unique JS identifier (no spaces)
  label     str   tab text shown to the reader
  desc      str   short phrase shown in the sequence strip (audience + intent)
  papers    list  ordered list of shortcodes for this path
──────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from config import AUTHOR, SITE_URL

# ── Reading speed (words per minute) ─────────────────────────────────────────
# Academic prose; adjust if your audience skews faster / slower.
WPM = 250

# ── Reading paths — configure here ───────────────────────────────────────────

READING_PATHS: list[dict] = [
    {
        "id": "new",
        "label": "New reader",
        "desc": "First encounter with WDT — core mechanism and governance",
        "papers": ["WP", "MF", "VAL", "GOV", "RATES"],
    },
    {
        "id": "serious",
        "label": "Serious reader",
        "desc": "Full picture — mechanism, behaviour, politics, transition",
        "papers": ["WP", "MF", "VAL", "CORP", "GOV", "RATES", "BEHAV", "POL", "PHASE1"],
    },
    {
        "id": "economist",
        "label": "Economist",
        "desc": "Technical scrutiny — revenue model, robustness, international",
        "papers": [
            "WP", "MF", "LR.A", "LR.B",
            "VAL", "VAL.A", "VAL.B",
            "CORP", "CORP.A",
            "RATES", "RATES.A",
            "SWEEPS", "SWEEPS.A",
            "BEHAV", "CLOSE", "FM", "MOD",
        ],
    },
    {
        "id": "legal",
        "label": "Legal / institutional",
        "desc": "Constitutional and jurisdictional scrutiny",
        "papers": [
            "WP", "MF", "VAL", "CORP", "GOV", "RATES", "BEHAV", "POL", "PHASE1",
            "JUR", "CORP.A", "GOV.A", "GOV.B", "SCOPE",
        ],
    },
    {
        "id": "political",
        "label": "Political / policy",
        "desc": "Legitimacy, adoption, international strategy",
        "papers": [
            "WP", "MF", "VAL", "CORP", "GOV", "RATES", "BEHAV", "POL", "PHASE1",
            "JUR", "GOV.A", "GOV.B", "FM", "MOD", "SCOPE",
        ],
    },
    {
        "id": "full",
        "label": "Full review",
        "desc": "All papers — appendices after parent papers",
        "papers": [
            "WP", "MF",
            "LR.A", "LR.B",
            "JUR",
            "VAL", "VAL.A", "VAL.B",
            "CORP", "CORP.A",
            "GOV", "GOV.A", "GOV.B",
            "RATES", "RATES.A",
            "SWEEPS", "SWEEPS.A",
            "BEHAV", "BEHAV.A",
            "FAL", "SCOPE",
            "WFR", "WFR.A", "LDW", "ENV",
            "CLOSE", "PHASE1",
            "POL", "FM", "MOD", "INST", "ADD",
        ],
    },
]

# ── Section ordering for tables and chip map ──────────────────────────────────

SECTION_ORDER: list[tuple[str, str, list[str]]] = [
    # (section_name, css_class_suffix, shortcodes)
    ("Core",                   "core",  ["WP", "MF"]),
    ("Prior literature",       "lit",   ["LR.A", "LR.B"]),
    ("Jurisdiction",           "jur",   ["JUR"]),
    ("Valuation",              "mech",  ["VAL", "VAL.A", "VAL.B", "CORP", "CORP.A",
                                          "GOV", "GOV.A", "GOV.B"]),
    ("Revenue modelling",      "rev",   ["RATES", "RATES.A", "SWEEPS", "SWEEPS.A"]),
    ("Robustness & limits",    "rob",   ["BEHAV", "BEHAV.A", "FAL", "SCOPE"]),
    ("Welfare & distribution", "welf",  ["WFR", "WFR.A", "LDW", "ENV"]),
    ("Implementation",         "impl",  ["CLOSE", "PHASE1"]),
    ("Political & strategic",  "pol",   ["POL", "FM", "MOD", "INST", "ADD"]),
]

_STATUS_LABEL: dict[str, str] = {
    "active":     "&#10003; Active",
    "superseded": "&#8617; Superseded",
    "draft":      "&#9881; Draft",
}

# Shortcodes that have no rendered paper page on the site.
_NO_PAGE: frozenset[str] = frozenset()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _reading_time(words: int) -> str:
    """Return 'N min' string from word count."""
    if not words:
        return "—"
    mins = max(1, round(words / WPM))
    return f"{mins} min"


def _path_total_words(path_papers: list[str], paper_meta: dict[str, Any]) -> int:
    seen: set[str] = set()
    total = 0
    for sc in path_papers:
        if sc in paper_meta and sc not in seen:
            total += paper_meta[sc].get("word_count", 0) or 0
            seen.add(sc)
    return total


def _path_reading_time_range(words: int) -> str:
    """Return '~N–M hrs' or '~N min' string with ±10% band."""
    if not words:
        return "—"
    mins_mid = words / WPM
    lo = max(1, round(mins_mid * 0.9))
    hi = round(mins_mid * 1.1)
    if hi >= 60:
        lo_h = lo / 60
        hi_h = hi / 60
        # Format as hours with one decimal if < 10 hrs
        def fmt(h: float) -> str:
            return f"{h:.1f}".rstrip("0").rstrip(".") + " hr"
        return f"~{fmt(lo_h)}–{fmt(hi_h)}"
    return f"~{lo}–{hi} min"


# ── Inline CSS scoped to corpus page ─────────────────────────────────────────
# Uses existing site variables/colours from styles.css where possible.

CORPUS_CSS = """
/* corpus.qmd scoped styles */

/* ── Path selector ── */
.cp-path-bar {
  margin: 0 0 1.2rem;
}
.cp-path-bar-label {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 11px;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: .07em;
  color: #2B0055;
  margin: 0 0 .4rem;
}
.cp-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: .6rem;
}
.cp-tab {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 12px;
  padding: 3px 10px;
  border: 2px outset #808080;
  background-color: #C0C0C0;
  color: #000;
  cursor: pointer;
  text-decoration: none;
}
.cp-tab:hover {
  background-color: #A0A0A0;
}
.cp-tab.cp-active {
  background-color: #2B0055;
  color: #FFD700;
  border-style: inset;
}

/* Path strip */
.cp-strip {
  background-color: #F5F0FF;
  border-left: 4px solid #2B0055;
  border-top: 1px solid #C0C0C0;
  border-right: 1px solid #C0C0C0;
  border-bottom: 1px solid #C0C0C0;
  padding: 7px 12px;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 12px;
  color: #2B0055;
  display: none;
  flex-wrap: wrap;
  align-items: center;
  gap: 5px;
  margin-bottom: .9rem;
}
.cp-strip.cp-visible {
  display: flex;
}
.cp-strip-desc {
  font-weight: bold;
  margin-right: 4px;
  white-space: nowrap;
}
.cp-strip-time {
  margin-left: auto;
  font-style: italic;
  color: #3d0080;
  white-space: nowrap;
  font-size: 11px;
}
.cp-sc-chip {
  display: inline-block;
  background-color: #2B0055;
  color: #FFD700;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 11px;
  font-weight: bold;
  padding: 1px 6px;
  border: 1px solid #1A0033;
}
.cp-arrow {
  color: #888;
  font-size: 11px;
}

/* ── Domain chip map ── */
.cp-map {
  margin: 1rem 0 1.4rem;
  border: 2px solid #2B0055;
  background-color: #F5F0FF;
  padding: 10px 12px;
}
.cp-map-title {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 11px;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: .07em;
  color: #2B0055;
  margin: 0 0 .7rem;
  border-bottom: 1px solid #C0C0C0;
  padding-bottom: .3rem;
}
.cp-domain-row {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 6px;
}
.cp-domain-label {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 11px;
  color: #555;
  width: 120px;
  flex-shrink: 0;
  padding-top: 3px;
}
.cp-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

/* Domain chip colours — background / text / border */
.cp-chip {
  display: inline-block;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 11px;
  font-weight: bold;
  padding: 2px 7px;
  border: 1px solid;
  cursor: default;
  transition: opacity .12s, outline .12s;
  text-decoration: none;
}
.cp-chip a { color: inherit; text-decoration: none; }
.cp-chip:hover { text-decoration: underline; }

/* Colour by domain */
.cc-core  { background:#2B0055; color:#FFD700; border-color:#1A0033; }
.cc-lit   { background:#C0DD97; color:#173404; border-color:#639922; }
.cc-jur   { background:#C0C0C0; color:#2C2C2A; border-color:#888;    }
.cc-mech  { background:#B5D4F4; color:#042C53; border-color:#378ADD; }
.cc-rev   { background:#FAC775; color:#412402; border-color:#BA7517; }
.cc-rob   { background:#F5C4B3; color:#4A1B0C; border-color:#D85A30; }
.cc-welf  { background:#9FE1CB; color:#04342C; border-color:#1D9E75; }
.cc-impl  { background:#F4C0D1; color:#4B1528; border-color:#D4537E; }
.cc-pol   { background:#D3D1C7; color:#2C2C2A; border-color:#888780; }

/* Highlight / dim states */
.cp-chip.cp-on-path  { outline: 2px solid #2B0055; outline-offset: 1px; }
.cp-chip.cp-off-path { opacity: .28; }

/* Legend */
.cp-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 14px;
  margin-bottom: .8rem;
}
.cp-legend-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 11px;
  color: #333;
}
.cp-legend-swatch {
  width: 12px;
  height: 12px;
  border: 1px solid;
  display: inline-block;
  flex-shrink: 0;
}

/* ── Word count / reading time toggle ── */
.cp-wc-toggle {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 11px;
  color: #2B0055;
  cursor: pointer;
  text-decoration: underline;
  background: none;
  border: none;
  padding: 0;
  margin-bottom: .3rem;
  display: inline-block;
}
.cp-wc-toggle:hover { color: #CC0000; }

/* ── Section tables ── */
.cp-section { margin-bottom: 1.6rem; }
.cp-section-name {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 12px;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: .06em;
  color: #2B0055;
  margin: 0 0 .25rem;
  border-bottom: 1px solid #2B0055;
  padding-bottom: .15rem;
}
/* Override global table styles for corpus tables */
.cp-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  margin: 0;
  border: 1px solid #C0C0C0;
}
.cp-table th {
  background-color: #2B0055;
  color: #FFD700;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 11px;
  font-weight: bold;
  padding: 4px 8px;
  border: 1px solid #1A0033;
  text-align: left;
  letter-spacing: .03em;
}
.cp-table td {
  padding: 3px 8px;
  border: 1px solid #D0D0D0;
  vertical-align: middle;
  font-size: 12px;
}
.cp-table tr:nth-child(even) td { background-color: #F8F8F8; }
.cp-table tr:hover td { background-color: #E8E0FF; }
.cp-table td:first-child {
  font-family: Arial, Helvetica, sans-serif;
  font-weight: bold;
  white-space: nowrap;
}
.cp-status-active     { color: #16a34a; font-weight: bold; }
.cp-status-draft      { color: #BA7517; font-weight: bold; }
.cp-status-superseded { color: #888; }

/* Show/hide word count vs reading time via body class */
.cp-words { display: inline; }
.cp-rtime { display: none;   }
body.cp-show-rtime .cp-words { display: none; }
body.cp-show-rtime .cp-rtime { display: inline; }

/* Tables panel toggle */
.cp-tables-toggle {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 12px;
  background-color: #2B0055;
  color: #FFD700;
  border: 2px outset #808080;
  padding: 3px 12px;
  cursor: pointer;
  margin-bottom: .8rem;
  display: inline-block;
}
.cp-tables-toggle:hover { background-color: #3d0080; border-style: inset; }
"""


# ── JavaScript ────────────────────────────────────────────────────────────────

def _build_js(reading_paths: list[dict], paper_meta: dict[str, Any]) -> str:
    # Serialise paths with precomputed reading-time ranges into JS.
    js_paths: list[dict] = []
    for p in reading_paths:
        words = _path_total_words(p["papers"], paper_meta)
        js_paths.append({
            "id": p["id"],
            "desc": p["desc"],
            "papers": p["papers"],
            "timeRange": _path_reading_time_range(words),
        })

    paths_json = json.dumps(js_paths, ensure_ascii=False)

    return f"""
const CP_PATHS = {paths_json};

function cpApplyPath(id) {{
  const path = CP_PATHS.find(p => p.id === id);
  const chips = document.querySelectorAll('.cp-chip');
  const strip = document.getElementById('cp-strip');
  const tabs  = document.querySelectorAll('.cp-tab');

  tabs.forEach(t => t.classList.toggle('cp-active', t.dataset.path === id));

  if (!path || id === 'all') {{
    chips.forEach(c => {{ c.classList.remove('cp-on-path','cp-off-path'); }});
    strip.classList.remove('cp-visible');
    strip.innerHTML = '';
    return;
  }}

  const onSet = new Set(path.papers);
  chips.forEach(c => {{
    const sc = c.dataset.sc;
    if (onSet.has(sc)) {{
      c.classList.add('cp-on-path');
      c.classList.remove('cp-off-path');
    }} else {{
      c.classList.add('cp-off-path');
      c.classList.remove('cp-on-path');
    }}
  }});

  // Build strip
  let html = '<span class="cp-strip-desc">' + path.desc + '</span>';
  path.papers.forEach((sc, i) => {{
    if (i > 0) html += '<span class="cp-arrow">&#8594;</span>';
    html += '<span class="cp-sc-chip">' + sc + '</span>';
  }});
  if (path.timeRange) {{
    html += '<span class="cp-strip-time">' + path.timeRange + '</span>';
  }}
  strip.innerHTML = html;
  strip.classList.add('cp-visible');
}}

document.getElementById('cp-tabs').addEventListener('click', e => {{
  const tab = e.target.closest('.cp-tab');
  if (tab) cpApplyPath(tab.dataset.path);
}});

function cpToggleTables() {{
  const panel = document.getElementById('cp-tables-panel');
  const btn   = document.getElementById('cp-tables-btn');
  const open  = panel.style.display === 'none' || panel.style.display === '';
  panel.style.display = open ? 'block' : 'none';
  btn.textContent = open ? '&#9660; Hide full index' : '&#9658; Show full index';
}}

function cpToggleWc() {{
  const show = document.body.classList.toggle('cp-show-rtime');
  document.getElementById('cp-wc-btn').textContent =
    show ? 'Show word count' : 'Show reading time';
}}
"""


# ── HTML builders ─────────────────────────────────────────────────────────────

def _legend_html() -> str:
    items = [
        ("cc-core",  "#2B0055", "#1A0033", "Core"),
        ("cc-lit",   "#C0DD97", "#639922", "Prior literature"),
        ("cc-jur",   "#C0C0C0", "#888",    "Jurisdiction"),
        ("cc-mech",  "#B5D4F4", "#378ADD", "Mechanism & valuation"),
        ("cc-rev",   "#FAC775", "#BA7517", "Revenue modelling"),
        ("cc-rob",   "#F5C4B3", "#D85A30", "Robustness & limits"),
        ("cc-welf",  "#9FE1CB", "#1D9E75", "Welfare & distribution"),
        ("cc-impl",  "#F4C0D1", "#D4537E", "Implementation"),
        ("cc-pol",   "#D3D1C7", "#888780", "Political & strategic"),
    ]
    parts = []
    for cls, bg, border, label in items:
        parts.append(
            f'<span class="cp-legend-item">'
            f'<span class="cp-legend-swatch" style="background:{bg};border-color:{border}"></span>'
            f'{label}</span>'
        )
    return '<div class="cp-legend">' + "".join(parts) + "</div>"


def _chip_map_html(section_order: list[tuple], link_map: dict, paper_meta: dict) -> str:
    rows = []
    for section_name, cls_suffix, shortcodes in section_order:
        present = [s for s in shortcodes if s in paper_meta or s in link_map]
        if not present:
            continue
        chips = []
        for sc in present:
            page = link_map.get(sc, "")
            href = f' href="{page}"' if page and sc not in _NO_PAGE else ""
            tag = "a" if href else "span"
            chips.append(
                f'<{tag} class="cp-chip cc-{cls_suffix}" data-sc="{sc}"{href}>{sc}</{tag}>'
            )
        rows.append(
            f'<div class="cp-domain-row">'
            f'<div class="cp-domain-label">{section_name}</div>'
            f'<div class="cp-chips">{"".join(chips)}</div>'
            f'</div>'
        )
    return (
        '<div class="cp-map">'
        '<div class="cp-map-title">Papers by domain</div>'
        + "".join(rows)
        + "</div>"
    )


def _path_tabs_html(reading_paths: list[dict]) -> str:
    tabs = ['<button class="cp-tab cp-active" data-path="all">All papers</button>']
    for p in reading_paths:
        tabs.append(
            f'<button class="cp-tab" data-path="{p["id"]}">{p["label"]}</button>'
        )
    return (
        '<div class="cp-path-bar">'
        '<div class="cp-path-bar-label">Reading path</div>'
        '<div class="cp-tabs" id="cp-tabs">'
        + "".join(tabs)
        + "</div></div>"
        '<div class="cp-strip" id="cp-strip"></div>'
    )


def _section_table_html(
    section_name: str,
    shortcodes: list[str],
    link_map: dict,
    paper_meta: dict,
) -> str:
    present = [s for s in shortcodes if s in paper_meta or s in link_map]
    if not present:
        return ""

    rows = []
    for sc in present:
        page   = link_map.get(sc, "")
        meta   = paper_meta.get(sc, {})
        title  = meta.get("title", sc).replace("The Wealth Delta Tax: ", "")
        ver    = meta.get("version", "—")
        status = meta.get("status", "active")
        wc     = meta.get("word_count", 0) or 0
        rt     = _reading_time(wc)
        wc_str = f"{wc:,}" if wc else "—"
        status_cls = {
            "active": "cp-status-active",
            "draft": "cp-status-draft",
            "superseded": "cp-status-superseded",
        }.get(status, "")
        status_lbl = _STATUS_LABEL.get(status, status)

        if sc in _NO_PAGE or not page:
            sc_cell = f"<strong>{sc}</strong>"
        else:
            sc_cell = f'<a href="{page}"><strong>{sc}</strong></a>'

        rows.append(
            f"<tr>"
            f"<td>{sc_cell}</td>"
            f"<td>{title}</td>"
            f"<td>v{ver}</td>"
            f'<td><span class="cp-words">{wc_str}</span>'
            f'<span class="cp-rtime">{rt}</span></td>'
            f'<td class="{status_cls}">{status_lbl}</td>'
            f"</tr>"
        )

    header = (
        "<tr>"
        "<th>Paper</th>"
        "<th>Title</th>"
        "<th>Version</th>"
        '<th id="cp-wc-col">Words</th>'
        "<th>Status</th>"
        "</tr>"
    )

    return (
        f'<div class="cp-section">'
        f'<div class="cp-section-name">{section_name}</div>'
        f'<table class="cp-table"><thead>{header}</thead><tbody>'
        + "".join(rows)
        + "</tbody></table></div>"
    )


# ── Main generator ────────────────────────────────────────────────────────────

def generate_corpus_qmd(
    dest_path: Path,
    link_map: dict[str, Any],
    paper_meta: dict[str, Any],
) -> None:
    """Write corpus.qmd to dest_path."""

    n_papers = len(paper_meta)

    # ── All paper shortcodes that exist ──
    all_scs: set[str] = set(link_map.keys()) | set(paper_meta.keys())

    # ── Collection-level JSON-LD ──
    collection_ld: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Collection",
        "name": "The Wealth Delta Tax Research Programme",
        "url": SITE_URL,
        "author": {"@type": "Person", "name": AUTHOR},
        "hasPart": [
            {
                "@type": "ScholarlyArticle",
                "name": meta.get("title", sc),
                "url": f"{SITE_URL}/{link_map.get(sc, f'{sc.lower()}.html')}",
                "version": meta.get("version", ""),
            }
            for sc, meta in paper_meta.items()
        ],
    }
    ld_json = json.dumps(collection_ld, indent=2, ensure_ascii=False)

    # ── Section tables HTML ──
    tables_html = ""
    for section_name, _cls, shortcodes in SECTION_ORDER:
        tables_html += _section_table_html(section_name, shortcodes, link_map, paper_meta)

    # ── JS ──
    js = _build_js(READING_PATHS, paper_meta)

    # ── Assemble full page ──
    # Delivered as a raw HTML passthrough block so Quarto doesn't touch it.
    # The page intro text above the block is plain markdown so Quarto renders it.

    intro_md = (
        f"This page is the authoritative index of the Wealth Delta Tax research "
        f"programme. The HTML versions of these papers, as published at this site, "
        f"are the current authoritative versions. Version numbers and dates are "
        f"updated on each revision.\n\n"
        f"The programme currently comprises **{n_papers} working papers**.\n"
    )

    html_block = f"""```{{=html}}
<script type="application/ld+json">
{ld_json}
</script>

<style>
{CORPUS_CSS}
</style>

{_path_tabs_html(READING_PATHS)}

{_legend_html()}

{_chip_map_html(SECTION_ORDER, link_map, paper_meta)}

<hr>

<button class="cp-wc-btn cp-wc-toggle" id="cp-wc-btn"
        onclick="cpToggleWc()">Show reading time</button>

<button class="cp-tables-toggle" id="cp-tables-btn"
        onclick="cpToggleTables()">&#9658; Show full index</button>

<div id="cp-tables-panel" style="display:none">
{tables_html}
</div>

<script>
{js}
</script>
```"""

    dependencies_md = """
---

## Reading dependencies

Most papers assume familiarity with (WP).
(RATES) and (SWEEPS) assume familiarity with (VAL).
(BEHAV) assumes familiarity with (VAL) and (GOV).
(WFR) assumes familiarity with (RATES).
(POL) assumes familiarity with (GOV).
(CLOSE) assumes familiarity with (VAL) and (GOV).
(INST) assumes familiarity with (POL) and (GOV).
(FM) assumes familiarity with (POL) and (RATES).
(ENV) assumes familiarity with (RATES) and (BEHAV).
(LDW) assumes familiarity with (RATES).
(FAL) assumes familiarity with (VAL), (RATES), and (BEHAV).

The recommended first-time sequence is: (WP) → (MF) → (VAL) → (GOV) → (RATES).
See also the [reading guide by interest](research.html#reading-guide-by-interest).

---

## About this index

The HTML papers on this site are the authoritative current versions.
PDF versions archived at [Zenodo](https://doi.org/10.5281/zenodo.21964119)
may lag by one or more revisions.
This page is updated manually at each site build;
the [Project Map](Project-Map.html) is the authoritative source
for paper status and open questions.
"""

    qmd = "\n".join([
        "---",
        'title: "Papers"',
        'description: "Complete index of the Wealth Delta Tax research programme'
        ' — all papers with version history and relationships."',
        f'author: "{AUTHOR}"',
        "---",
        "",
        intro_md,
        html_block,
        dependencies_md,
    ])

    dest_path.write_text(qmd, encoding="utf-8")
    print(f"  ✓ Generated corpus.qmd ({n_papers} papers, {len(READING_PATHS)} reading paths)")
