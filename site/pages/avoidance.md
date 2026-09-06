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
<style>
  .avoid-calc-frame {
    width: 100%;
    height: 900px;
    border: 2px inset var(--wdt-gold-dim);
    display: block;
    background: var(--wdt-purple-deep);
  }
  .avoid-calc-fallback {
    font-size: 0.8rem;
    color: var(--wdt-silver);
    margin-top: 0.5rem;
    font-family: Arial, Helvetica, sans-serif;
  }
</style>
<iframe
  src="tools/taxpayer.html"
  class="avoid-calc-frame"
  title="WDT Individual Taxpayer Calculator"
  loading="lazy"
  sandbox="allow-scripts allow-same-origin">
</iframe>
<p class="avoid-calc-fallback">
  Calculator not loading?
  <a href="tools/taxpayer.html" target="_blank">Open it in a new tab &#x2197;</a>
</p>
```

---

Found a strategy this page does not cover? Identified a parameter combination that produces a surprising result? [Contact the project](mailto:wealthdeltatax@gmail.com) — this page is maintained as a live document and will be updated as new strategies are identified.