Yes — and the page is actually well-suited for this because it already has a clean separation between the prose/strategy content (pure Markdown) and the calculator (pure JS + Pyodide). Here's how I'd structure it:

---

## Target structure

```
wdt-site/model/
├── avoidance-calc.js       ← all JS: sliders, runCalc(), renderResults(), renderTable()
├── avoidance-styles.css    ← all calculator-specific CSS (extracted from the {=html} block)
├── wdt_core.py             ← already there, loaded by Pyodide
└── rates_model.py          ← already there, loaded by Pyodide

site/pages/
└── avoidance.md            ← mostly Markdown; one small {=html} block for the calculator shell
```

---

## What stays in `avoidance.md`

The five strategy sections, all the prose, the verdict boxes — everything currently written as Markdown divs stays exactly as-is. The only `{=html}` blocks become:

**1. The intro div** (lines 9–24) — keep as-is, it's tiny and purely presentational.

**2. The calculator section** — replace the entire 300-line `{=html}` block with a shell:

```html
```{=html}
<div class="wdt-tool-panel">
  <div class="wdt-tool-inner">
    <h2>Try it: simulate your WDT position</h2>
    <p class="subtitle">…</p>
    <div id="loading">…</div>
    <div id="main">
      … all the slider HTML …
    </div>
    <div id="results">…</div>
    <div id="table-wrap">…</div>
  </div>
</div>

<link rel="stylesheet" href="../model/avoidance-styles.css">
<script src="https://cdn.jsdelivr.net/pyodide/v0.27.0/full/pyodide.js"></script>
<script src="../model/avoidance-calc.js"></script>
` ` `
```

The HTML structure (divs, sliders, controls) stays in the `.md` because it's static markup — no JS in it. All the `<script>` and `<style>` content moves out.

---

## What moves to `avoidance-calc.js`

Everything currently inside `<script>…</script>`:
- `initPyodide()`, `runCalc()`, `renderResults()`, `renderTable()`, `renderStats()`
- All the slider event listeners
- The `setMode()` / `setProgress()` / `showError()` helpers

This file is loaded by the `<script src>` tag above — no changes to the logic needed.

---

## What moves to `avoidance-styles.css`

All the `<style>…</style>` content from the `{=html}` block (`.wdt-tool-panel`, `.controls`, `.stat-row`, `.sell-row`, etc.). This file is picked up by the `<link rel="stylesheet">` tag, and also gets copied to `_build/model/` verbatim by the model copy loop — no pipeline changes needed.

---

## Why this works with the existing pipeline

- `avoidance-calc.js` and `avoidance-styles.css` land in `wdt-site/model/` → copied verbatim to `_build/model/` by the model copy loop you just fixed
- The paths `../model/avoidance-calc.js` and `../model/avoidance-styles.css` resolve correctly because `avoidance.html` is rendered at `_site/avoidance.html` (root level)
- Pyodide still loads `wdt_core.py` and `rates_model.py` from `../model/` as before — no change
- Quarto never sees a `<table>` tag in the `.md` source — the warning disappears
- `avoidance.md` becomes ~200 lines of readable Markdown with one modest HTML shell block

---

## One thing to decide

The slider HTML (the `<div id="main">` controls block, ~80 lines) is static markup with no JS in it. It could stay in the `.md` `{=html}` shell, or move to a separate `avoidance-controls.html` fragment that gets `fetch()`-ed and injected by `avoidance-calc.js` at init time. The latter makes the `.md` even cleaner but adds a fetch dependency. I'd leave the controls in the shell for now — the real wins are getting the JS and CSS out.

Want me to draft the split — the revised `avoidance.md` shell and the stub `avoidance-calc.js` with the relocated functions?