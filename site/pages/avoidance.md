---
title: "How to Legally Avoid Tax Under the WDT"
description: >
  A taxpayer's guide to minimising lifetime WDT liability under Route C.
  Five optimisation strategies examined with live calculator to test each one.
toc: true
---

```{=html}
<div class="avoid-intro">
<p>This is a serious instruction manual.</p>
<p>If you are a taxpayer subject to the Wealth Delta Tax and your objective is to minimise
the amount of WDT you pay, this page tells you how to do it. We will not conceal strategies,
cite anti-avoidance provisions as a substitute for analysis, or ask you to trust enforcement
to close gaps we have not thought through.</p>
<p>Instead: here are the equations, the optimisation variables, and the known strategies.
Here is what each one actually produces. Here is what you cannot avoid, and why.</p>
<p><strong>The purpose is not to claim the WDT makes avoidance impossible.</strong>
The purpose is to make that claim falsifiable. If a strategy we have not anticipated
produces a meaningful economic advantage, that is a defect in the mechanism — and
publishing this page is how we find it.</p>
<p style="margin-bottom:0"><em>If you find something we have missed: <a href="mailto:wealthdeltatax@gmail.com">we want to know</a>.</em></p>
</div>
```

## How the WDT is calculated

The WDT taxes changes in declared net wealth, not wealth itself. In each period, you declare a wealth figure W. The tax due is:

```
L = τ(W) × ΔW    where ΔW = W_current − W_previous
```

The rate function τ(W) is a logistic curve rising from a floor τ₀ (15% at canonical parameters) toward a ceiling τ_m (70%), above an entry threshold W_min (£2m). It is calibrated so that the effective rate on any given pound of wealth increase rises continuously with declared wealth — there are no bands or cliff edges.

When wealth falls, ΔW is negative. The system pays you a refund at the same rate. This symmetry is not a loophole: it is load-bearing. The refund is what makes honest declaration incentive-compatible over a full market cycle. Any strategy that generates a large refund will also trigger a tax when the position subsequently recovers.

At the terminal sell year, alpha drops out entirely: W_sell = f_N × V_sell, where f_N is the retained equity fraction accumulated over the holding period. The declaration ratio cannot influence the sell-year basis.

## The optimisation variables

A taxpayer under Route C has five levers. The strategies below work through each one.

---

### Strategy 1 — Declaration ratio α: understating wealth each period {#strategy-1}

::: strategy-block

::: wdt-domain-header
[1]{.strategy-number} Declaration ratio α — understating wealth each period
:::

::: strategy-body

The declaration ratio α scales your declared wealth relative to true wealth. At α = 1 you are honest. At α = 0.5 you declare half your true wealth each period. This reduces ΔW in growth years, cutting the tax due. It looks like the obvious play.

::: mechanic

**What actually happens**

Understatement depletes your retained equity fraction f. Each period you hold back declaration, the system records a lower basis — but your true asset value has grown. When you sell, W_sell = f_N × V_sell with alpha removed. You receive a smaller fraction of sale proceeds because f_N has been eroded by the cumulative under-declaration. The sell-year refund (which would have partially compensated you for prior overpayment) is also smaller.

:::

The net result across a full holding period: understaters pay less in annual taxes but also receive smaller refunds, and their sell proceeds are reduced by the f erosion. The model shows the advantage is real but modest — typically low single-digit percentage points of lifetime effective rate at α = 0.5, narrowing further for shorter holding periods and negative-growth years.

::: mechanic

**Try it in the calculator below**

Set α to 0.5. Compare Net_settled and TW_settled against the honest baseline. Then switch to a historical series that includes a market crash (try 2000 or 2007) and observe how the refund asymmetry behaves when growth turns negative.

:::

::: {.verdict-box .moderate}

**Verdict — limited advantage**

Understating declaration produces a real but self-limiting tax reduction. The mechanism that cuts your tax payments also cuts your sell-year proceeds. The advantage erodes further under volatile returns and disappears almost entirely if the WDT is applied with a valuation purchase option (Route A/B), which anchors W to a third-party-agreed value.

:::

[Simulate α < 1 in the calculator ↓](#the-calculator){.pdf-download}

:::

:::

---

### Strategy 2 — Holding period N: how long you hold before selling {#strategy-2}

::: strategy-block

::: wdt-domain-header
[2]{.strategy-number} Holding period N — how long you hold before selling
:::

::: strategy-body

The WDT is a flow tax. You only pay when declared wealth increases. If you never sell and never grow, you pay nothing. The question is how holding period length interacts with the rate function.

::: mechanic

**What actually happens**

At steady growth, extending N increases cumulative tax roughly linearly — each additional period adds another year of taxable growth. There is no bunching advantage from selling late, because the basis carried forward at the sell year is the prior declared value, not the original purchase price. You cannot defer a large one-time gain and benefit from a low rate on the total — each year's increment is taxed as it accrues.

:::

Under volatile historical returns, holding period selection matters differently: a holding period that ends during a market trough generates a large refund at the sell year (negative ΔW = large negative L_sell). But you cannot know in advance when the trough will be, and deliberately timing a sale to a crash year means accepting depressed proceeds.

::: mechanic

**Try it in the calculator below**

Hold all other parameters constant and sweep N from 10 to 50. Observe that effective rate (Net_settled / TW_settled) is relatively stable across N — the flow structure prevents the accumulation effect that makes deferral valuable under capital gains tax.

:::

::: {.verdict-box .limited}

**Verdict — not a useful lever**

Holding period length does not produce a systematic tax advantage under the WDT. This is by design: the flow structure eliminates the deferral benefit that makes hold-to-death strategies valuable under realisation-based capital gains tax.

:::

[Simulate holding period in the calculator ↓](#the-calculator){.pdf-download}

:::

:::

---

### Strategy 3 — Overstatement α > 1: declaring more wealth than you own {#strategy-3}

::: strategy-block

::: wdt-domain-header
[3]{.strategy-number} Overstatement α > 1 — declaring more wealth than you own
:::

::: strategy-body

This sounds counterintuitive, but the mathematics make it worth examining. If you declare more wealth than you actually own in years of high growth, you pay more tax — but you also accumulate a larger negative cumulative position, which generates a larger refund when growth turns negative or at sale.

::: mechanic

**What actually happens**

At the sell year, alpha drops out. If you have been overstating by α = 1.5 throughout, your prior declared basis (f_N × α × V_N) typically exceeds your true sell proceeds (f_N × V_sell) when growth is moderate. This generates a large negative delta_sell — a substantial refund. Post-sale, the settlement mechanism iterates on the resulting cash position, taxing back the refund if it produces a positive delta again, until convergence.

:::

The net effect is that overstatement provides a very small advantage for specific return profiles, and a disadvantage for others. The settle_tw() function converges this residual within a few iterations for honest and moderate overstaters; large overstaters at high growth see more iterations. In all cases the lifetime advantage is economically small — well under 1% of TW_settled at canonical parameters.

::: mechanic

**Try it in the calculator below**

Set α to 1.5 at steady g = 10%. Compare Net_settled to the honest baseline. Then try α = 1.5 at g = 5%. Note how the advantage/disadvantage reverses. The settle_n counter shows how many post-sale settlement iterations convergence required.

:::

::: {.verdict-box .blocked}

**Verdict — negligible and unreliable**

Overstatement does not produce a reliable tax advantage. The sell-year alpha drop-out and the post-sale settlement mechanism converge the position toward the honest outcome. At high growth rates, overstatement is a net disadvantage. This is not a viable avoidance strategy.

:::

[Simulate α > 1 in the calculator ↓](#the-calculator){.pdf-download}

:::

:::

---

### Strategy 4 — Staying below W_min: keeping declared wealth under the entry threshold {#strategy-4}

::: strategy-block

::: wdt-domain-header
[4]{.strategy-number} Staying below W_min — keeping declared wealth under the entry threshold
:::

::: strategy-body

The WDT applies only above W_min (£2m at canonical parameters). Wealth below this threshold pays nothing. If you can keep declared wealth below W_min every period, your liability is zero.

::: mechanic

**What actually happens**

This is a real and intentional feature, not a gap. The W_min threshold is a design choice: the WDT is not intended to reach small wealth holders. The question is whether a wealth holder above the threshold can restructure to move below it. Under Route C (equity transfer), W reflects retained equity in underlying assets. Splitting holdings across multiple structures does not reduce the attribution — the WDT consolidates beneficial ownership, not legal title. A £10m holding split across five entities is still attributed to one person as £10m.

:::

For genuine wealth just above the threshold (£2–5m), moderate growth volatility can produce years where declared wealth dips below W_min — paying no tax in that period. This is mechanically correct behaviour, not avoidance. The rate function is continuous at W_min (it returns zero below, and τ₀ ≈ 0 just above), so there is no cliff-edge incentive to manipulate.

::: {.verdict-box .limited}

**Verdict — applies only to genuine boundary cases**

Sub-threshold status is real zero tax. But it requires actually having sub-threshold wealth on a beneficial-ownership basis. Attribution rules prevent artificial fragmentation. For taxpayers well above W_min, this strategy is unavailable.

:::

:::

:::

---

### Strategy 5 — Timing losses: selling or declaring in crash years {#strategy-5}

::: strategy-block

::: wdt-domain-header
[5]{.strategy-number} Timing losses — selling or declaring in crash years
:::

::: strategy-body

If your wealth falls in a given year, the WDT pays you a refund. A strategy that concentrates declarations of wealth in years of negative return — and avoids triggering taxable events in growth years — would, in principle, extract refunds without paying commensurate taxes.

::: mechanic

**What actually happens**

The cumulative position prevents this. The refund in a crash year is bounded by the cumulative tax paid to date (the lifetime cap). If you have paid very little tax — because you understated in growth years — your refund capacity is correspondingly small. The system does not pay refunds that exceed what you have contributed. A taxpayer who paid nothing throughout cannot extract a refund at a crash.

:::

What you can do: hold through a cycle and receive a natural refund when the next decline arrives. But the refund is automatically netted against the taxes already paid on the prior growth. The symmetry is exact: you are returned, at the same marginal rate, the same amount you paid on the gain. The refund is a reversal, not a bonus.

::: {.verdict-box .blocked}

**Verdict — blocked by the cumulative cap**

Loss-timing strategies are structurally prevented. Refunds cannot exceed cumulative contributions. The symmetry between taxes and refunds is the mechanism, not a limitation to be gamed.

:::

[Switch to historical series from 2000 or 2007 ↓](#the-calculator){.pdf-download}

:::

:::

---

## What you cannot avoid — and why

Across all five strategies, the pattern is the same. Every mechanism that reduces tax payments in growth years also reduces the value recovered at the terminal event. The WDT is a tax on the increment of wealth, not on its stock. Reducing the declared increment reduces both the tax and the basis — you pay less, but you also walk away with less. The net lifetime position, expressed as Net_settled / TW_settled, is substantially more stable across declaration strategies than either figure alone.

This is not accidental. The retained equity fraction f, which links declaration history to sell-year proceeds, is what closes the loop. A taxpayer who understates throughout accumulates a depleted f. At the sell year, alpha drops out and the depletion is fully exposed. There is no way to understate during the holding period and then declare honestly at sale — the basis is already set.

The residual advantage of understating (low single digits as a percentage of effective rate) is real, but it shrinks under realistic return volatility and disappears when valuation is anchored by a third-party purchase option. The model shows the mechanism is robust to the strategies most likely to be attempted.

If you find a strategy that produces a meaningful and durable advantage under canonical parameters — one that survives volatile returns and does not depend on implausible inputs — [that is a design defect and we want to know about it](mailto:wealthdeltatax@gmail.com). This page is the mechanism by which that finding reaches us.

## The calculator {#the-calculator}

Set your parameters and run the simulation. The honest baseline (α = 1) is always shown alongside your chosen scenario so the comparison is immediate. Use the period-by-period table to trace exactly where the tax and refund flows occur.

The model runs the full Route C simulation from `wdt_core.py` — the same code used in the research papers, loaded unmodified in your browser.

```{=html}
<div class="wdt-tool-panel">
<div class="wdt-tool-inner">

<h2>Try it: simulate your WDT position</h2>
<p class="subtitle">
  Set V₀, α, growth rate and holding period. The honest baseline (α = 1) is always shown alongside your chosen scenario.
</p>

<div id="loading">
  <h2>Initialising Python runtime…</h2>
  <div id="progress-bar-wrap"><div id="progress-bar"></div></div>
  <div id="progress-label">Loading Pyodide…</div>
  <div id="error-msg"></div>
</div>

<div id="main">

  <div class="controls">

    <div class="control-group">
      <label>Starting net wealth (V₀)</label>
      <div class="slider-row">
        <input type="range" id="v0-slider" min="-1" max="5" step="0.01" value="1.301">
        <span class="val" id="v0-display">£20m</span>
      </div>
      <span class="note">Log scale: £0.5m – £100,000m</span>
    </div>

    <div class="control-group">
      <label>Holding period (N)</label>
      <div class="slider-row">
        <input type="range" id="n-slider" min="1" max="65" step="1" value="29">
        <span class="val" id="n-display">29 years</span>
      </div>
      <span class="note">Periods before terminal sale</span>
    </div>

    <div class="control-group">
      <label>Declaration ratio (α)</label>
      <div class="slider-row">
        <input type="range" id="alpha-slider" min="0.1" max="2.0" step="0.05" value="1.0">
        <span class="val" id="alpha-display">1.00</span>
      </div>
      <span class="note">α &lt; 1 = understatement · α &gt; 1 = overstatement · α = 1 = honest</span>
    </div>

    <div class="control-group">
      <label>Growth scenario</label>
      <div class="mode-toggle">
        <button id="btn-steady" class="active" onclick="setMode('steady')">Steady g</button>
        <button id="btn-hist" onclick="setMode('hist')">Historical series</button>
      </div>
      <div class="slider-row" id="g-slider-row" style="margin-top:0.4rem;">
        <input type="range" id="g-slider" min="-0.10" max="0.35" step="0.001" value="0.1045">
        <span class="val" id="g-display">10.45%</span>
      </div>
      <div id="year-select-row">
        <label for="start-year-select">Start year:</label>
        <select id="start-year-select"></select>
        <span id="g-mean-note" style="font-size:0.78rem;color:#888;display:none;"></span>
      </div>
      <span class="note" id="g-note">Annual total return applied uniformly each period</span>
    </div>

  </div>

  <details>
    <summary>Advanced — rate function parameters</summary>
    <div class="advanced-grid">
      <div class="control-group">
        <label>τ₀ — floor rate</label>
        <div class="slider-row">
          <input type="range" id="tau0-slider" min="0.01" max="0.50" step="0.01" value="0.15">
          <span class="val" id="tau0-display">15.0%</span>
        </div>
      </div>
      <div class="control-group">
        <label>τ_m — ceiling rate</label>
        <div class="slider-row">
          <input type="range" id="taum-slider" min="0.10" max="1.00" step="0.01" value="0.70">
          <span class="val" id="taum-display">70.0%</span>
        </div>
      </div>
      <div class="control-group">
        <label>k — steepness (per £m)</label>
        <div class="slider-row">
          <input type="range" id="k-slider" min="-4" max="0" step="0.01" value="-3">
          <span class="val" id="k-display">0.001</span>
        </div>
        <span class="note">Log₁₀ scale</span>
      </div>
      <div class="control-group">
        <label>W_min — entry point (£m)</label>
        <div class="slider-row">
          <input type="range" id="wmin-slider" min="0.5" max="20" step="0.5" value="2.0">
          <span class="val" id="wmin-display">£2.0m</span>
        </div>
      </div>
    </div>
  </details>

  <div style="display:flex;align-items:center;margin-top:1rem;">
    <button id="run-btn" onclick="runCalc()">▶ Calculate</button>
    <span class="running-msg" id="running-msg">Running…</span>
  </div>

  <div class="results" id="results" style="display:none">
    <div class="panel honest">
      <h3>Honest declaration (α = 1)</h3>
      <div id="stats-honest"></div>
    </div>
    <div class="panel alpha-panel">
      <h3 id="alpha-panel-title">Selected α</h3>
      <div id="stats-alpha"></div>
    </div>
  </div>

  <div class="table-wrap" id="table-wrap" style="display:none">
    <h3>Period-by-period detail</h3>
    <div id="table-container"></div>
  </div>

</div><!-- /main -->

</div><!-- /wdt-tool-inner -->
</div><!-- /wdt-tool-panel -->

<script src="https://cdn.jsdelivr.net/pyodide/v0.27.5/full/pyodide.js"></script>
<script>
function setProgress(pct, label) {
  document.getElementById('progress-bar').style.width = pct + '%';
  document.getElementById('progress-label').textContent = label;
}
function showError(msg) {
  const el = document.getElementById('error-msg');
  el.textContent = msg; el.style.display = 'block';
}

const v0Slider    = document.getElementById('v0-slider');
const nSlider     = document.getElementById('n-slider');
const alphaSlider = document.getElementById('alpha-slider');
const gSlider     = document.getElementById('g-slider');
const tau0Slider  = document.getElementById('tau0-slider');
const taumSlider  = document.getElementById('taum-slider');
const kSlider     = document.getElementById('k-slider');
const wminSlider  = document.getElementById('wmin-slider');

function fmtV0(logval) {
  const v = Math.pow(10, parseFloat(logval));
  if (v >= 1000) return '£' + (v/1000).toFixed(0) + 'b';
  if (v >= 1) return '£' + v.toFixed(1) + 'm';
  return '£' + (v*1000).toFixed(0) + 'k';
}

v0Slider.addEventListener('input',    () => { document.getElementById('v0-display').textContent    = fmtV0(v0Slider.value); });
nSlider.addEventListener('input',     () => { document.getElementById('n-display').textContent     = nSlider.value + ' years'; });
alphaSlider.addEventListener('input', () => { document.getElementById('alpha-display').textContent = parseFloat(alphaSlider.value).toFixed(2); });
gSlider.addEventListener('input',     () => { document.getElementById('g-display').textContent     = (parseFloat(gSlider.value)*100).toFixed(1) + '%'; });
tau0Slider.addEventListener('input',  () => { document.getElementById('tau0-display').textContent  = (parseFloat(tau0Slider.value)*100).toFixed(1) + '%'; });
taumSlider.addEventListener('input',  () => { document.getElementById('taum-display').textContent  = (parseFloat(taumSlider.value)*100).toFixed(1) + '%'; });
kSlider.addEventListener('input',     () => { document.getElementById('k-display').textContent     = Math.pow(10, parseFloat(kSlider.value)).toFixed(4); });
wminSlider.addEventListener('input',  () => { document.getElementById('wmin-display').textContent  = '£' + parseFloat(wminSlider.value).toFixed(1) + 'm'; });

let mode = 'steady';
function setMode(m) {
  mode = m;
  document.getElementById('btn-steady').classList.toggle('active', m === 'steady');
  document.getElementById('btn-hist').classList.toggle('active', m === 'hist');
  document.getElementById('g-slider-row').style.display = m === 'steady' ? 'flex' : 'none';
  document.getElementById('year-select-row').classList.toggle('visible', m === 'hist');
  document.getElementById('g-note').textContent = m === 'steady'
    ? 'Annual total return applied uniformly each period'
    : 'Historical UK equity return series; N periods from selected start year';
}

const yearSel = document.getElementById('start-year-select');
Array.from({length: 73}, (_, i) => 1947 + i).forEach(y => {
  const opt = document.createElement('option');
  opt.value = y; opt.textContent = y;
  yearSel.appendChild(opt);
});
yearSel.value = 2007;

let pyodide = null;
let pyReady = false;

async function initPyodide() {
  try {
    setProgress(5, 'Loading Pyodide runtime (first load ~10s, cached thereafter)…');
    pyodide = await loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.27.5/full/' });
    setProgress(40, 'Runtime loaded. Fetching model files…');
    const [coreText, tomlText] = await Promise.all([
      fetch('tools/wdt_core.py').then(r => { if (!r.ok) throw new Error('wdt_core.py not found'); return r.text(); }),
      fetch('tools/260812_WDT_Params.toml').then(r => { if (!r.ok) throw new Error('TOML not found'); return r.text(); }),
    ]);
    setProgress(65, 'Writing files to virtual filesystem…');
    pyodide.FS.writeFile('/wdt_core.py',            coreText);
    pyodide.FS.writeFile('/260812_WDT_Params.toml', tomlText);
    setProgress(75, 'Importing WDT core module…');
    await pyodide.runPythonAsync(`
import sys
sys.path.insert(0, '/')
from wdt_core import load_params, run_sim, run_sim_hist
`);
    setProgress(90, 'Loading parameters…');
    await pyodide.runPythonAsync(`p = load_params('/260812_WDT_Params.toml')`);
    setProgress(100, 'Ready.');
    pyReady = true;
    document.getElementById('loading').style.display = 'none';
    document.getElementById('main').style.display = 'block';
  } catch (err) {
    setProgress(0, 'Failed.');
    showError('Error: ' + err.message);
    console.error(err);
  }
}

async function runCalc() {
  if (!pyReady) return;
  const btn = document.getElementById('run-btn');
  const msg = document.getElementById('running-msg');
  btn.disabled = true; msg.style.display = 'inline';

  const V0    = Math.pow(10, parseFloat(v0Slider.value));
  const N     = parseInt(nSlider.value);
  const alpha = parseFloat(alphaSlider.value);
  const g     = parseFloat(gSlider.value);
  const tau0  = parseFloat(tau0Slider.value);
  const taum  = parseFloat(taumSlider.value);
  const k     = Math.pow(10, parseFloat(kSlider.value));
  const wmin  = parseFloat(wminSlider.value);
  const startYear = parseInt(yearSel.value);

  try {
    const pyCode = `
import json
p_ui = dict(p)
p_ui['tau_0'] = ${tau0}
p_ui['tau_m'] = ${taum}
p_ui['k']     = ${k}
p_ui['W_min'] = ${wmin}
p_ui['V0_m']  = ${V0}
${mode === 'hist' ? `
base_year = p_ui['series_base_year']
canon = p_ui['canonical_returns']
offset = (${startYear} - base_year) % len(canon)
p_ui['returns'] = canon[offset:] + canon[:offset]
` : ''}
${mode === 'steady' ? `
r_honest = run_sim(p_ui, alpha=1.0, N=${N}, g=${g})
r_alpha  = run_sim(p_ui, alpha=${alpha}, N=${N}, g=${g})
g_use_honest = ${g}
g_use_alpha  = ${g}
` : `
r_honest = run_sim_hist(p_ui, alpha=1.0, N=${N})
r_alpha  = run_sim_hist(p_ui, alpha=${alpha}, N=${N})
g_use_honest = r_honest['g_mean']
g_use_alpha  = r_alpha['g_mean']
`}
def sim_to_rows(r):
    rows = []
    for rec in r['records'][1:]:
        rows.append({'t': rec['t'], 'V': rec['V'], 'W': rec['W'], 'L': rec['L'], 'cum': rec['cum'], 'rate': rec['rate'], 'delta': rec['delta'], 'f': rec['f'], 'q': rec['q']})
    s = r['sell']
    rows.append({'t': s['t'], 'V': s['V_sell'], 'W': s['W_sell'], 'L': s['L_sell'], 'cum': s['cum_after'], 'rate': s['rate_sell'], 'delta': s['delta_sell'], 'f': s['f_N'], 'q': None, 'sell': True})
    return rows
def make_entry(r, g_use):
    return {
        'TW':         r['TW'],
        'TW_settled': r['TW_settled'],
        'settle_n':   r['settle_iters'],
        'TTP':        r['TTP'],
        'Refunds':    r['Refunds'],
        'Net':        r['Net'],
        'Net_settled':r['Net_settled'],
        'g_use':      g_use,
        'rows':       sim_to_rows(r),
    }
result = {
    'honest': make_entry(r_honest, g_use_honest),
    'alpha':  make_entry(r_alpha,  g_use_alpha),
}
json.dumps(result)
`;
    const jsonStr = await pyodide.runPythonAsync(pyCode);
    renderResults(JSON.parse(jsonStr), V0, alpha, N, mode, startYear);
  } catch (err) {
    alert('Simulation error: ' + err.message);
    console.error(err);
  }
  btn.disabled = false; msg.style.display = 'none';
}

function fmt_m(v, dp=2) { if (Math.abs(v) >= 1000) return '£' + (v/1000).toFixed(1) + 'b'; return '£' + v.toFixed(dp) + 'm'; }
function fmt_pct(v) { return (v*100).toFixed(2) + '%'; }
function fmt_rate(v) { return v === null ? '—' : (v*100).toFixed(2) + '%'; }

function renderStats(container, d, V0) {
  const settled_TW = d.TW_settled;
  const settleNote = d.settle_n === 0 ? 'already settled at sell'
                   : d.settle_n >= 2000 ? 'cap reached (2000 periods)'
                   : `settled after ${d.settle_n} period${d.settle_n === 1 ? '' : 's'}`;

  const rows = [
    ['Starting wealth (V₀)',              fmt_m(V0),                 'neutral'],
    ['TW at sell year',                   fmt_m(d.TW),               'neutral'],
    [`TW_settled (${settleNote})`,         fmt_m(settled_TW),         'neutral'],
    ['Gross taxes paid (TTP)',             fmt_m(d.TTP),              d.TTP > 0  ? 'positive' : 'zero'],
    ['Gross refunds received',             fmt_m(d.Refunds),          d.Refunds < 0 ? 'negative' : 'zero'],
    ['Net lifetime tax (settled)',         fmt_m(d.Net_settled),      d.Net_settled > 0 ? 'positive' : (d.Net_settled < 0 ? 'negative' : 'zero')],
    ['Eff. rate (Net_settled/TW_settled)', fmt_pct(d.Net_settled / settled_TW), d.Net_settled > 0 ? 'positive' : 'zero'],
    ['Mean return used',                   fmt_pct(d.g_use),          'neutral'],
  ];
  container.innerHTML = rows.map(([lbl, num, cls]) =>
    `<div class="stat-row"><span class="lbl">${lbl}</span><span class="num ${cls}">${num}</span></div>`
  ).join('');
}

function renderTable(rows) {
  const header = `<tr>
    <th>Period</th><th>True value V (£m)</th><th>Decl. wealth W (£m)</th>
    <th>Δ W (£m)</th><th>Rate τ(W)</th><th>Tax / refund L (£m)</th>
    <th>Cumulative (£m)</th><th>Retained f</th>
  </tr>`;
  const trs = rows.map(r => {
    const deltaClass = r.delta > 0.0001 ? 'pos' : r.delta < -0.0001 ? 'neg' : 'zero';
    const lClass = r.L > 0.0001 ? 'pos' : r.L < -0.0001 ? 'neg' : 'zero';
    return `<tr${r.sell ? ' class="sell-row"' : ''}>
      <td>${r.sell ? r.t + ' (sell)' : r.t}</td>
      <td>${r.V.toFixed(3)}</td><td>${r.W.toFixed(3)}</td>
      <td class="${deltaClass}">${r.delta.toFixed(3)}</td>
      <td>${fmt_rate(r.rate)}</td>
      <td class="${lClass}">${r.L.toFixed(4)}</td>
      <td>${r.cum.toFixed(4)}</td><td>${r.f.toFixed(4)}</td>
    </tr>`;
  }).join('');
  return `<table><thead>${header}</thead><tbody>${trs}</tbody></table>`;
}

function renderResults(data, V0, alpha, N, mode, startYear) {
  document.getElementById('results').style.display = 'grid';
  document.getElementById('table-wrap').style.display = 'block';
  renderStats(document.getElementById('stats-honest'), data.honest, V0);
  renderStats(document.getElementById('stats-alpha'),  data.alpha,  V0);
  document.getElementById('alpha-panel-title').textContent = alpha === 1.0
    ? 'α = 1.00 (same as honest baseline)'
    : `α = ${alpha.toFixed(2)} (${alpha < 1 ? 'understatement' : 'overstatement'})`;
  const gMeanNote = document.getElementById('g-mean-note');
  if (mode === 'hist') {
    gMeanNote.textContent = `Mean return: ${(data.honest.g_use * 100).toFixed(2)}%`;
    gMeanNote.style.display = 'inline';
  } else {
    gMeanNote.style.display = 'none';
  }
  const modeLabel = mode === 'hist'
    ? `Historical series from ${startYear}, N=${N}`
    : `Steady g=${(data.honest.g_use*100).toFixed(2)}%, N=${N}`;
  document.getElementById('table-container').innerHTML = `
    <p style="font-size:0.8rem;color:#888;margin-bottom:0.5rem;font-family:Arial,Helvetica,sans-serif;">${modeLabel}</p>
    <details open>
      <summary style="cursor:pointer;font-size:0.85rem;color:#555;margin-bottom:0.4rem;font-family:Arial,Helvetica,sans-serif;">
        Honest baseline (α = 1) — ${data.honest.rows.length} periods
      </summary>
      ${renderTable(data.honest.rows)}
    </details>
    ${alpha !== 1.0 ? `
    <details open style="margin-top:1rem">
      <summary style="cursor:pointer;font-size:0.85rem;color:#555;margin-bottom:0.4rem;font-family:Arial,Helvetica,sans-serif;">
        α = ${alpha.toFixed(2)} — ${data.alpha.rows.length} periods
      </summary>
      ${renderTable(data.alpha.rows)}
    </details>` : ''}`;
}

initPyodide();
</script>
```

---

Found a strategy this page does not cover? Identified a parameter combination that produces a surprising result? [Contact the project](mailto:wealthdeltatax@gmail.com) — this page is maintained as a live document and will be updated as new strategies are identified.