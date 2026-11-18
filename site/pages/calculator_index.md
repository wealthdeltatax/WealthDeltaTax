---
title: "WDT — Interactive Calculators"
description: "Computational tools for exploring the Wealth Delta Tax mechanism. All calculators load their model code directly from the research codebase. Parameters are read from `WDT_Params.toml`. No server-side computation — all model code runs locally via [Pyodide](https://pyodide.org). The first load takes around 10 seconds to initialise the runtime; subsequent calculations are fast."
toc: false
---

```{=html}
<div class="wdt-retired-model-note" role="note" style="margin:0 0 1.25rem 0;padding:0.75rem 1rem;border:1px solid #CC6600;border-left-width:6px;border-radius:4px;background:rgba(204,102,0,0.08);">
  <strong>Based on the retired model.</strong> All three calculators below run the earlier (version 1) model that the new series is replacing, so their results are not the newest model's results. They will be updated when the newest model is finished.
  <a href="/retired.html">About the retired model and where its papers went</a>.
</div>

```

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

<a class="tool-card" href="model/ldw.html">
  <span class="tag tag-green">Welfare</span>
  <h2>Labour Dividend Calculator</h2>
  <p>
    Purchasing power gain for a given salary under a mature WDT. Models full
    labour tax displacement (income tax and employee NICs removed from the
    payslip), VAT displacement, and SWF energy bill reduction. Employer NICs
    saving shown separately. 2025/26 tax rates; VAT and energy figures are
    illustrative and adjustable.
  </p>
</a>
```