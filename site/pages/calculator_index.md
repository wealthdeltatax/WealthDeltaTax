---
title: "WDT — Interactive Calculators"
description: "Computational tools for exploring the Wealth Delta Tax mechanism. Both calculators run the WDT Python model unmodified in your browser via Pyodide — no data leaves your machine."
toc: false
---

Both calculators load `wdt_core.py` and `rates_model.py` directly from the
research codebase. Parameters are read from `260812_WDT_Params.toml`. No
server-side computation — all model code runs locally via
[Pyodide](https://pyodide.org). The first load takes around 10 seconds to
initialise the runtime; subsequent calculations are fast.

```{=html}
<a class="tool-card" href="model/taxpayer.html">
  <span class="tag tag-blue">Individual</span>
  <h2>Taxpayer Calculator</h2>
  <p>
    Simulate the WDT tax profile for a single taxpayer under Route C
    (equity-transfer mechanism). Set starting wealth, growth rate or historical
    return series, holding period, and declaration ratio α. The
    honest-declaration baseline (α = 1) is always shown alongside your chosen
    scenario.
  </p>
</a>

<a class="tool-card" href="model/revenue.html">
  <span class="tag tag-purple">National</span>
  <h2>Revenue Calculator</h2>
  <p>
    Aggregate WDT revenue across the full UK taxable wealth distribution — 10
    wealth brackets, four return tiers, UK equity series 1947–2019. Set rate
    parameters, growth scenario, and SWF sizing. Modelled revenue is shown
    alongside current UK tax receipts for direct comparison.
  </p>
</a>
```
