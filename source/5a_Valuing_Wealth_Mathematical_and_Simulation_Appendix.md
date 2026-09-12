---
title: "The Wealth Delta Tax: Valuing Wealth — Mathematical and Simulation Appendix"
shortcode: "VAL.A"
status: "active"
keywords:
    - Wealth Delta Tax
    - wealth taxation
    - accrual taxation
    - mathematical modelling
    - numerical simulation
    - declaration equilibrium
    - valuation incentives
    - self-assessed valuation
    - overstatement
    - understatement
    - growth-dependent tax incentives
    - parameter sensitivity
    - N-crossing
    - Route D auction
---

### Revision History {.unnumbered .unlisted}

| Revision | Date            | Details                  |
|:--------:|:---------------:|--------------------------|
| 0.01      | 13 June 2026     | First Draft          |
| 1.00      | 15 August 2026  | Published to website |
| 1.01      | 19 August 2026  | SWEEPS integration: §A.2.4 and §A.2.5 updated with N-crossing language, $\tau_0$ sensitivity caveat, and three practical consequences in full; §A.5.4 Proposition 4 extended with temporal crossing mechanism, N-invariance of plateau inflection, and $\tau_0$-sensitivity of self-limiting property; (VAL.A §A.6) Declaration Equilibrium extended with N-crossing as the mechanism for self-limiting, tolerant zone as k-calibration property, and parameter-conditional qualification on $\tau_0$; §C.1 and §C.9 structural claims updated with SWEEPS-precise language throughout |
| 1.02 | 29 August 2026 | §E.4 Route D auction mechanism field updated to reflect three-pathway classification; §E.4.1 event table extended with corrective under- and over-declaration rows, voluntary hard-reset rows, inheritance downward discovery row, and no-bid outcome row; §D.6 added as new mechanism case illustrating corrective over-declaration with retain and no-bid variants; (VAL.A §A.6) two references to Route D auction updated to reflect three-pathway architecture |
| 1.03 | 30 August 2026 | TW refined to TW_settled throughout (post-sale oscillation now included in terminal figure); §A.2.4 updated with C.11 decomposition result and ~6:1 refund-to-cost ratio for mild overstatement; §A.2.5 cap figures updated to per-α values (2.6pp at α=1.2 through 13.0pp at α=2.0); §A.4.4 extended with §A.4.4.2 defining TW_settled and the decomposition identity (A.4.17); §A.5.6 proposition table updated for Propositions 4 and 6; (VAL.A §A.6) cap figures corrected and C.11d cited; §B.4 output metrics table extended with TW_settled decomposition row |
| 1.04 | 30 August 2026 | §B.2.1 formula note added documenting additive vs multiplicative β discrepancy and demoting β extension to speculative/uncalibrated; §C.3 structural claim updated to reference additive form and confirm no main-paper arguments depend on β; §C.9 saturation boundary threshold corrected from $g$ ≥ 15% to $g$ ≈ 16–18% per Python model |
| 1.05 | 31 August 2026 | §A.2.4, §A.2.5, §A.5.4 Proposition 4 interpretation, §A.5.6 Propositions 4 and 6 rows, (VAL.A §A.6) Declaration Equilibrium, §C.11d and §C.11e footnotes: corrected throughout to reflect that the nominal TW_settled advantage of mild overstatement (C.11d) does not survive NPV adjustment (C.12) and is not a genuine economic return to overstatement. Population equilibrium recharacterised as α ≈ 1.1 driven by refund-protection asymmetry under valuation uncertainty, not as α ≈ 1.2–1.5 driven by a stable TW advantage. |
| 1.06 | 11 September 2026 | §B.3 parameter table: N baseline corrected from 29 to 30 (canonical holding period — average time spent as a WDT taxpayer in the Balanced scenario). §C tables replaced with N = 30 output (C.1–C.12), resolving the N = 29 error from v1.03–v1.05. §C preamble updated to state N = 30 as canonical with rationale. §C.10 start-year corrected from 2006/2007 to 2000; C.10.2 crash-entry N references corrected. §C.1 structural claim: note added on theoretical plateau inflection at g ≈ 17.3% vs observed ≈19.1% at N = 30. |
| 1.07 | 12 September 2026 | §A.2.5 (Finding 5), §A.5.4 (Proposition 4), §A.5.6 (Propositions 4 and 6), §A.6 (Declaration Equilibrium), §C.1 (structural claim): reframed throughout to replace mild-overstatement-as-equilibrium with tolerant-zone / asymmetry / conditional-bias structure. (i) Tolerant zone (α ≈ 0.8–1.5) established as the primary result. (ii) Asymmetry within the zone made explicit — understatement loses refund protection in loss years (C.6), overstatement preserves it. (iii) Mild upward declaration bias (α ≈ 1.1) characterised as a conditional model-implied prediction, not a population equilibrium. (iv) α = 1.2 and α = 1.5 recharacterised as illustrative points on the overstatement side of the tolerant zone, not as equilibrium values. (v) Stale C.1 claim corrected — at N = 30 all four overstater levels cross into nominal net-cost territory at approximately g ≈ 7%, including α = 1.2 and α = 1.5, consistent with Figure 7.6 annotations. (vi) Proposition 6 rewritten. (vii) 'Population equilibrium' language replaced with 'model-implied behavioural centre' or 'conditional mild upward declaration bias' throughout. |

\newpage

# A. Mathematical Model and Incentive Analysis

## A.1 Purpose

This appendix formalises the incentive structure of the WDT under self-declared valuation routes, establishing the conditions under which declaration strategies create or reverse advantages relative to honest declaration. It does not estimate behaviour directly.

A declared value establishes the recognised basis from which future wealth changes are measured; deviations create consequences that persist through the holding period and resolve through future taxation, settlement, or transfer.

The model examines declaration strategies using the parameter:

$\alpha = \frac{\text{Declared Net Worth}}{\text{True Net Worth}}$

where $\alpha$ = 1 represents honest declaration, $\alpha$ < 1 represents understatement, and $\alpha$ > 1 represents overstatement.

**Interpretation of $\alpha$ as a portfolio-level aggregate.** The WDT operates on declared net worth as a whole, not on per-asset declaration ratios. $\alpha$ is therefore correctly understood as a portfolio-level aggregate declaration ratio — the ratio of total declared net worth to total true net worth. How that aggregate arises internally is irrelevant to the mechanism. A taxpayer with 60% of wealth on professionally valued Routes A/B (where $\alpha$ = 1 by construction, since professional valuation is taken as the reference) and 40% on self-declared Routes C/D at an asset-level ratio of 1.5 would have a portfolio-level $\alpha$ of 1.2. A taxpayer with 100% of wealth on Route C at asset-level $\alpha$ = 1.2 is in an identical position from the mechanism's perspective. The model is indifferent to the internal decomposition. This is not a simplifying assumption requiring qualification: the WDT taxes declared net worth, and $\alpha$ is the exact right quantity to characterise how declared net worth relates to true net worth, regardless of the portfolio composition that produces it.

The model does not assume honest declaration is globally optimal. It identifies the conditions under which it forms a locally stable region and where alternative strategies may become advantageous.

## A.2 Main Findings

Five principal findings follow.

### A.2.1 Finding 1: Honest declaration lies within a locally stable region

Around $\alpha$ = 1, small deviations generate offsetting costs through future basis and rate effects, producing a locally stabilising incentive structure rather than a persistent arbitrage opportunity. Full analysis is in Proposition 1.

### A.2.2 Finding 2: Overstatement cost increases with the progressive rate parameter k

Higher declarations enter higher tax brackets more rapidly as $k$ increases, constraining deliberate inflation. Non-tax signalling benefits are outside this model. Full analysis is in Proposition 2.

### A.2.3 Finding 3: Understatement produces a growth-rate-dependent trade-off

For moderate growth rates and policy-relevant holding periods (g = 2–12%), understatement consistently increases lifetime tax burdens through accumulated basis gaps. The penalty escalates steeply between $g$ ≈ 10% and $g$ ≈ 17%, then plateaus: the rate function's logistic ceiling stops the marginal deterrent from increasing further, but it does not reverse. The penalty ceiling scales with the degree of understatement and is reached at approximately the same growth rate across all $\alpha$ values. Full analysis is in Propositions 3a and 3b, with quantitative outcomes in (VAL.A §C.1) and (VAL.A §C.1).

### A.2.4 Finding 4: Understater penalties plateau once the rate function reaches saturation; aggressive overstatement is self-limiting through a temporal crossing mechanism

For understaters, the marginal penalty stops escalating once the progressive tax function approaches its maximum rate — the ceiling is set by $\alpha$, not by further growth. The plateau inflection at $g$ ≈ 17.3% is a rate-function property that is approximately constant across all understatement levels and N-invariant above the plateau: four-panel simulation at N ∈ {10, 20, 29, 50} confirms that the plateau shape at N = 29 and N = 50 are visually identical, establishing that the ceiling is determined by the rate function rather than by the simulation horizon (SWEEPS §2.3, Fig S3.1b).

For overstaters the picture differs by degree. Mild overstatement ($\alpha$ ≤ 1.5) produces a nominal TW_settled advantage across the full tested growth range — the sell-year refund benefit from the inflated basis exceeds the f_N erosion and post-sale damping costs by approximately 6:1 at canonical parameters, confirmed by the C.11 decomposition. However, this nominal advantage does not represent a genuine economic return: (VAL.A §C.12) shows that once all tax cash flows are discounted at ρ = 5%, the advantage collapses or reverses in the low-growth band where it nominally exists, because periodic outflows precede the sell-year refund by the full holding period. The mild-overstatement nominal advantage is a timing artefact. Aggressive overstatement ($\alpha$ ≥ 1.8) additionally faces a contemporaneous net-cost corridor at $g$ ≈ 9–17%, and the temporal N-crossing correction: at canonical parameters ($\tau_0$ = 15%), the $\alpha$ = 2.0 N-crossing threshold arrives at N ≈ 30, and the $\alpha$ = 1.8 crossing at N ≈ 32 (SWEEPS.A §A.5). $\alpha$ = 1.5 does not cross within the tested range at canonical parameters, but its nominal advantage is still eliminated by discounting. This N-crossing is $\tau_0$-sensitive: the crossing migrates to longer horizons as $\tau_0$ rises, and disappears entirely for realistic holding periods above $\tau_0$ ≈ 29–32% (SWEEPS §3.1, Table A.6). The self-limiting properties hold as stated at canonical parameters but are parameter-conditional results. Full analysis is in Proposition 4.

### A.2.5 Finding 5: The mechanism produces a broad tolerant zone with an asymmetric incentive structure and a conditional mild upward declaration bias

The model does not require exact valuation accuracy. At canonical parameters and the historical mean growth rate, declarations spanning approximately $\alpha$ = 0.8 to $\alpha$ = 1.5 produce lifetime tax outcomes economically close to honest declaration (|C.1| < 2pp). This is the tolerant zone. It is a design feature: the mechanism concentrates deterrence at the tails and leaves the centre forgiving, because attempting to force exact accuracy would impose large costs on taxpayers whose valuation uncertainty happens to land them slightly off-centre.

Within the tolerant zone, consequences are asymmetric. Understatement reduces refund protection in negative-growth states: at $g$ = −4.5%, $\alpha$ = 0.8 retains only 97.88% of the honest declarer's terminal wealth, while $\alpha$ = 1.2 and $\alpha$ = 1.5 retain 100% (VAL.A §C.6). This asymmetry is the key behavioural implication. A risk-averse taxpayer facing ±10–20% valuation uncertainty rationally centres their declaration slightly above their central estimate — near $\alpha$ ≈ 1.1 rather than exactly 1.0 — so that the lower end of their uncertainty band still lands in overstatement territory, preserving a larger refund entitlement in a loss year. This produces a model-implied behavioural centre near $\alpha$ ≈ 1.1. It is a conditional prediction contingent on the assumed uncertainty and risk preferences, not an empirical estimate and not a dominant strategy.

The nominal TW_settled figures for the overstatement side of the tolerant zone ($\alpha$ = 1.2, 1.5) are illustrative data points, not evidence for a wealth-maximising equilibrium. (VAL.A §C.12) establishes that the nominal advantage does not survive discounting at ρ = 5%. Further, at N = 30, C.1 turns positive (the declared strategy costs more than honest declaration) above approximately $g$ ≈ 7% for both $\alpha$ = 1.2 and $\alpha$ = 1.5: the nominal advantage is confined to the low-growth tail. These figures are therefore correctly labelled as illustrative points on the overstatement side of the tolerant zone, not as the definition of a population equilibrium.

Understatement has the opposite refund-protection property: systematic understaters lose meaningful downside protection, reinforcing the incentive against low declarations beyond the direct compounding cost.

Three practical consequences follow from the predicted mild upward bias. First, the declared tax base likely slightly exceeds true values, collecting modestly more than exact honesty would produce in nominal terms. Second, refund exposure in loss years is correspondingly larger than a model assuming exact honesty would predict, since refunds are calculated on declared bases. The SRR floor calibration implication is identified as (ENV §9.2.1) and cannot be quantified before Phase One data establishes where the population centre sits. Third, the public register likely carries systematically inflated declared values during holding periods, creating a credit-expansion effect on private asset-backed lending; there is currently no instrument through which the Governing Council can observe or respond to drift in the population distribution of $\alpha$, which is a named monitoring gap addressed in (VAL.A §A.6).

| **Parameter** | **Effect on Understatement Cost** | **Effect on Overstatement Cost** |
|:---|:---|:---|
| **Growth rate (g)** | Generally increases the impact of understatement by enlarging the difference between declared basis and realised value. At extreme growth rates, progressive taxation can create nonlinear effects. | Can have limited direct tax effect under the base mechanism, but higher growth increases the interaction between declaration strategy and progressive rates. |
| **Holding period (N)** | Increases basis divergence during the compounding phase. At very long holding periods, progressive tax saturation can reduce or reverse the observed advantage. | Increases the effect of an inflated basis over time. Differences may initially persist before being constrained by progressive taxation. |
| **Rate steepness (k)** | Can reduce understatement advantages by causing later taxable appreciation to enter higher marginal rates more quickly. | Increases the cost of maintaining inflated declarations by accelerating exposure to higher tax rates. |
| **Asset volatility** | Ambiguous. Volatility may alter timing effects, realisation events, and the relationship between declared basis and realised value. | Ambiguous. Volatility may change both the value of signalling and the timing of progressive tax exposure. |
| **Ownership retention (f)** | Higher retention increases the duration over which basis differences can compound, increasing potential divergence before saturation. | Higher retention increases exposure to progressive taxation on accumulated appreciation. |
| **Tax saturation boundary** | Sets the penalty ceiling for understaters: the marginal deterrent stops escalating at $g$ ≈ 17.3%, but the penalty does not reverse. The ceiling scales with the degree of understatement and the inflection is N-invariant above the plateau — a rate-function property, not a compounding artefact of holding period. | Determines the N-crossing timing for aggressive overstaters and the C.1 sign-reversal threshold for mild overstaters. At N = 30, all four tested overstater levels ($\alpha$ = 1.2, 1.5, 1.8, 2.0) cross into nominal net-cost territory (C.1 > 0) at approximately $g$ ≈ 7%, confirming that even the overstatement side of the tolerant zone is in nominal net-cost territory at the historical mean growth rate. The nominal advantage at low growth is a timing artefact that does not survive NPV adjustment (VAL.A §C.12). Aggressive overstatement ($\alpha$ ≥ 1.8) additionally faces a contemporaneous net-cost corridor in the $g$ ≈ 9–17% range where the rate penalty dominates, plus a temporal N-crossing correction with threshold migrating as $\tau_0$ changes (see Finding 4). |

## A.3 Model Assumptions and Notation

All monetary values are in real terms. Subscript t is the assessment period index; t = 0 is system entry.

| **Symbol** | **Definition** |
|:--:|:---|
| $W_{t}$ | Declared net worth at the end of assessment period t. Governs all calculations in period t. |
| $W_{t}^{true}$ | True net worth at end of period t. Unobservable by the system. Used only for limit analysis. |
| $B_{t}$ | Recognised basis at end of period t. Equals $W_{t}$ after assessment. Starting point for the delta calculation in period t+1. |
| $\Delta_{t}$ | Taxable delta in period t: $\Delta_{t} = W_{t} - B_{(t-1)}$. |
| $\tau(W)$ | Marginal WDT rate as a function of declared net worth W. Defined below. |
| $L_{t}$ | Tax liability in period t when $\Delta_{t} > 0$. $L_{t} = \tau(W_{t}) \cdot \Delta_{t}$. |
| $R_{t}$ | Refund entitlement in period t when $\Delta_{t} < 0$. $R_{t} = \tau(W_{t}) \cdot |\Delta_{t}|$. |
| $s_{t}$ | Equity fraction of a fungible asset transferred to the state in settlement of $L_t$ under Route C. $s_{t} = \frac{L_{t}}{W_{t}^{(asset)}}$. |
| $n$ | Assessment window length, in years. n $\in$ {1, 2, 3, 5, 7}. |
| $r$ | Deferral charge rate. A government borrowing benchmark rate applied to unpaid tax liabilities under windows n > 1. |
| $\varphi(n)$ | Flexibility levy rate for window length n. $\varphi(1) = 0$. Increasing in n. |
| $T$ | Period of realisation. For Route C: the period of arm's-length sale or transfer. For Route D: the period of sale, inheritance auction, or voluntary settlement. |
| $P_{T}$ | Realisation price at period T. Observable market price established by arm's-length transaction or public auction. |
| $W_t^{(d)}$ | Declared transfer value of a derivative position at assessment date $t$. Enters the net worth calculation alongside all other assets and liabilities. Negative where the position is an obligation to the counterparty. |
| $B_{t-1}^{(d)}$ | Recognised basis of a derivative position carried from the prior assessment period. Set at $W_{t-1}^{(d)}$ after each assessment, consistent with the general basis update rule (A.3.3). |
| $\Delta_t^{(d)}$ | Taxable delta for a derivative position in period $t$: $\Delta_t^{(d)} = W_t^{(d)} - B_{t-1}^{(d)} + CF_{out,t} - CF_{in,t}$. Positive generates a liability; negative generates a refund entitlement under the symmetric mechanism. |
| $CF_{out,t}$ | Cash flows paid out of a derivative position during assessment period $t$: margin calls, settlement payments, option premiums paid. Increases the effective cost of holding the position; enters the delta calculation as a positive term. |
| $CF_{in,t}$ | Cash flows received into a derivative position during assessment period $t$: premiums received, settlement receipts, coupon payments. Reduces the effective cost of holding the position; enters the delta calculation as a negative term. |

### A.3.1 The Rate Function $\tau$(W)

The marginal WDT rate is a logistic S-curve function of declared net worth W:

$\tau(W) = \frac{\tau_{m}}{\left( 1 + A \cdot \exp\left( - $k$ \cdot \left( W - W_{\min} \right) \right) \right)}$ (A.3.1)

where $A = \frac{(\tau_{m} - \tau_{0})}{\tau_{0}}$, $\tau_0$ is the baseline marginal rate at the exemption threshold $W_{min}$, $\tau_m$ is the asymptotic maximum marginal rate, and $k$ > 0 is the rate escalation parameter.

Properties: (1) $\tau(W_{\min}) = \tau_{0} > 0$; (2) $\tau'(W) > 0$ — strictly increasing in declared net worth; (3) $\tau''(W)$ changes sign at $W_{\min} + \frac{1}{k}\ln\left(\frac{\tau_{m} - \tau_{0}}{\tau_{0}}\right)$, convex below and concave above; (4) bounded above by $\tau_m$, approaching $\tau_0$ from above as W → $W_{min}$.

k governs the steepness of rate progression. For Proposition 2, the key property is that the rate penalty from overstatement grows with both the degree of overstatement and the level of underlying net worth.

### A.3.2 The Delta and Tax Calculation

At the end of each assessment period t, the taxpayer declares net worth W_t. The taxable delta is:

$\Delta_{t} = W_{t} - B_{(t-1)}$ (A.3.2)

where $B_{(t-1)}$ is the recognised basis from the previous period. At system entry, B_0 is the grandfathered entry declaration. No tax is owed at entry.

If $\Delta_{t} > 0$: $L_{t} = \tau(W_{t}) \cdot \Delta_{t}$ [tax due] (A.3.3)

If $\Delta_{t} < 0$: $R_{t} = \tau(W_{t}) \cdot |\Delta_{t}|$ [refund due] (A.3.4)

If $\Delta_{t} = 0$: no liability, no refund (A.3.5)

The lifetime refund cap applies: cumulative refunds cannot exceed cumulative taxes paid over the same period. Where the cap binds, the refund is set to the maximum permissible amount and excess entitlement is forfeited.

Design note: current-period net worth governs the rate in both gain and loss years — both (A.3.3) and (A.3.4) apply $\tau(W_t)$. Applying $W_{t-1}$ instead has intuitive appeal but creates a strategic problem: a taxpayer anticipating a loss in period t can overstate $W_{t-1}$ to inflate the refund rate. A midpoint adds complexity without improvement.

The current-period rule accepts a residual asymmetry: a taxpayer falling from high to low net worth receives a refund at the lower rate, so the state captured the prior gain at a higher marginal rate than it shares the corresponding loss. This is accepted on two grounds: rate exposure should reflect current economic position, and the mild-overstatement equilibrium in (VAL.A §A.6) partially offsets the effect in practice by carrying W_t in loss years above strict honest declaration.

### A.3.3 The Basis Update Rule

After assessment:

$B_{t} = W_{t}$ (A.3.6)

The basis is not adjusted for tax paid or refunds received. Understatement in period t establishes a low recognised basis, enlarging the taxable delta in subsequent periods when declared values rise. The post-sale assessment recovers accumulated basis gaps through ordinary delta mechanics; no retrospective correction of prior declarations occurs.

### A.3.4 Net Worth Evolution

Declared net worth at t+1 reflects total holdings at that date, incorporating asset value changes, tax payments, and refunds received:

$W_{(t+1)} = W_{t} + \Delta(assets)_{(t,t+1)} - L_{t} + R_{t} + otherflows$ (A.3.7)

For Route D assets, no $L_t$ or $R_t$ flows arise during the holding period.

## A.4 Multi-Period Incentive Model

The system computes each period independently from the declared basis. The multi-period model represents taxpayer incentives across the full holding period; these are distinct calculations serving different purposes.

### A.4.1 Additional Notation

| **Symbol** | **Definition** |
|:--:|:---|
| $f_{t}$ | Retained fraction of the portfolio at end of period t. f_0 = 1 at system entry. |
| $\alpha$ | Declaration ratio: $W_{t} = \alpha \cdot f_{(t-1)} \cdot V_{t}$. $\alpha$ = 1 is honest declaration. $\alpha$ < 1 is understatement. $\alpha$ > 1 is overstatement. |
| $q_{t}$ | Fraction of holding transferred to the state in period t. $q_{t} = \tau(W_{t}) \cdot \frac{\Delta_{t}}{W_{t}}$. |
| $g$ | True value growth rate per period. |
| $\rho$ | Taxpayer's personal discount rate for present value calculations. |
| $N$ | Number of holding periods before sale. |
| $PV_{t}(\cdot)$ | Present value operator, discounting at rate ρ back to period 0. |
| $\tau_{0}$ | Baseline marginal rate at exemption threshold $W_{min}$. |
| $k$ | Rate escalation parameter in the logistic rate function. |

### A.4.2 Per-Period Sequence

Step 1 (True value):

$V_{t} = V_{t-1} \cdot (1 + g_{t})$ (A.4.1)

where $g_t$ is the growth rate for period t. For constant $g$ this reduces to $V_t = V_0 \cdot (1+g)^t$; the recursive form is used throughout so that variable-g series (such as the historical return sequence in (VAL.A §C.10) are handled correctly.

Step 2 (Declared net worth):

$W_{t} = f_{(t-1)} \cdot \alpha \cdot V_{t}$ (A.4.2)

Step 3 (Delta):

$\Delta_{t} = W_{t} - B_{(t-1)} = f_{(t-1)} \cdot \alpha \cdot V_{t} - B_{(t-1)}$ (A.4.3)

Step 4 (Marginal rate):

$\tau(W_{t}) = \frac{\tau_{m}}{\left( 1 + A \cdot \exp\left( - $k$ \cdot \left( W_{t} - W_{\min} \right) \right) \right)}$ (A.4.4)

Step 5 (Settlement):

The simulation uses a single signed quantity $L_t$ (positive = tax due, negative = refund due):

$L_{t} = \max\!\left(-\sum_{s=1}^{t-1} L_{s},\ \tau(W_{t}) \cdot \Delta_{t}\right) \quad \text{if } \Delta_{t} > 0 \text{ or } \sum_{s=1}^{t-1} L_{s} > 0, \text{ else } 0$ (A.4.5)

The max with $-\mathrm{cum}_{t-1}$ enforces the lifetime refund cap. When $\Delta_t < 0$, the uncapped claim is $\tau(W_t) \cdot \Delta_t$ (negative) and the cap floor is $-\mathrm{cum}_{t-1}$ (also negative); if the claim would exceed cumulative tax paid, the max binds and the refund is capped at the amount paid to date. Where $\Delta_t = 0$ and $\mathrm{cum}_{t-1} = 0$, the condition is false and $L_t = 0$.

Step 6 (Transfer fraction):

$q_{t} = \frac{L_{t}}{W_{t}}$ (A.4.6)

$q_t$ is positive when $L_t > 0$ (state acquires equity) and negative when $L_t < 0$ (state returns equity). The formula is identical in both cases.

Step 7 (Retained fraction update):

$f_{t} = f_{(t-1)} \cdot (1 - q_{t})$ (A.4.7)

When $q_t > 0$ the retained fraction falls; when $q_t < 0$ it rises, reflecting equity returned to the taxpayer in a refund period.

Step 8 (Basis update):

$B_{t} = W_{t}$ (A.4.8)

The basis update is unconditional: it applies after every period regardless of the sign of $\Delta_t$ and is not adjusted for tax paid or refunds received.

### A.4.3 Initialisation

$f_{0} = 1$ (A.4.9)

$B_{0} = \alpha \cdot V_{0}$ (A.4.10)

$L_{0} = 0$ (A.4.11)

### A.4.4 Post-Sale Assessment at Period N+1

The sell event is a distinct period with its own growth step applied to the final holding-period value:

$V_{sell} = V_{N} \cdot (1 + g_{sell})$ (A.4.12)

where $g_{sell}$ is the sell-year growth rate (equal to $g$ in constant-g runs). Sale proceeds at $V_{sell}$ are cash, automatically priced with no declaration ambiguity. At period N+1 the taxpayer declares the retained fraction of those proceeds:

$W_{(N+1)} = f_{N} \cdot V_{sell}$ (A.4.13)

#### A.4.4.1 Post-sale delta

The basis carried into the sell period is $B_N = W_N = f_{N-1} \cdot \alpha \cdot V_N$. The post-sale delta is therefore:

$\Delta_{(N+1)} = f_{N} \cdot V_{sell} - f_{(N-1)} \cdot \alpha \cdot V_{N}$ (A.4.14)

In constant-g runs $V_{sell} = V_N \cdot (1+g)$, so the delta incorporates both sell-year growth and the accumulated basis gap. Three qualitative cases: $\alpha$ = 1 produces a small refund from single-period growth; $\alpha$ < 1 produces a positive delta recovering the deferred liability; $\alpha$ > 1 produces a negative delta reflecting the excess paid across the holding period.

#### A.4.4.2 TW_settled and the decomposition identity

TW_settled is terminal net worth after the post-sale tax or refund oscillation is settled — the correct measure of lifetime outcome. The oscillation arises because the sell-year delta produces a liability or refund ($L_{sell}$), and the resulting cash position then generates a small further delta in the following period as the basis resets to the cash proceeds. TW_settled is therefore:

$TW_{settled} = f_N \cdot V_{sell} - L_{sell} + \text{settle adjustment}$ (A.4.16)

The TW_settled advantage over honest declaration decomposes into three additive terms verified to machine precision across all tested ($\alpha$, $g$) pairs:

$TW_{adv} = W_{sell\_delta} - \text{refund\_delta} - \text{settle\_delta}$ (A.4.17)

where $W_{sell\_delta} = f_N(\alpha) \cdot V_{sell} - f_N(1) \cdot V_{sell} \leq 0$ (f_N erosion cost: overstater holds a smaller stake at sale); $\text{refund\_delta} = L_{sell}(\alpha) - L_{sell}(1) \leq 0$ (sell-year refund benefit: inflated basis generates a larger refund or smaller tax at sale); and $\text{settle\_delta} \geq 0$ (post-sale damping cost: the larger refund creates a positive basis oscillation that is partially taxed back). At canonical parameters the refund benefit exceeds the erosion and damping costs by approximately 6:1, making the TW_settled advantage structurally positive for all tested overstater strategies. Note that excess periodic tax paid during the holding period is not additive in this identity — it feeds into TW_adv indirectly through f_N erosion, but is approximately 6× larger than |W_sell_delta| because most of the excess is returned via the sell-year refund. Full decomposition tables are in (VAL.A §C.11).

### A.4.5 Cumulative Retained Fraction

$f_{N} = \prod_{t=1}^{N} (1 - q_{t})$ (A.4.15)

Under understatement ($\alpha$ < 1), $\tau(\alpha \cdot f \cdot V_{t}) < \tau(f \cdot V_{t})$ because $\tau$ is increasing, so $q_{t}(\alpha) < q_{t}(1)$: less equity is transferred per period. In the simplified incentive model the dominant understatement cost channel is the terminal delta; additional dilution effects may arise depending on settlement mechanics and holding period length.

## A.5 Scope of the Arguments

The propositions below establish local and structural properties of the model, not universal behavioural predictions. The optimal declaration strategy depends on taxpayer circumstances: expected holding period, growth expectations, signalling effects, and liquidity constraints.

### A.5.1 Proposition 1: Local Convexity Around Honest Declaration

**Proposition.** For sufficiently small deviations around $\alpha$ = 1, the taxpayer's expected lifetime cost function is locally convex.

**Interpretation.** Understatement reduces the initial taxable base but increases future basis exposure; overstatement raises exposure to progressive rates. Simulations indicate these offsetting effects do not create a stable arbitrage opportunity from small deviations, though the result does not extend to all extreme scenarios.

### A.5.2 Proposition 2: Overstatement Cost Diverges as $k$ Increases

**Proposition.** The cost of maintaining an inflated declaration increases as the progressive rate parameter $k$ increases.

**Interpretation.** Higher $k$ steepens the rate curve, causing inflated declarations to enter higher brackets sooner. The primary constraint on overstatement is the interaction between declared wealth and progressive rates, not the basis mechanism alone. External signalling benefits are outside this model.

### A.5.3 Propositions 3a and 3b: Understatement Boundary Conditions

**Proposition 3a: Understatement cost increases with growth.** As asset growth increases, the difference between declared basis and realised value becomes larger.

**Interpretation.** Growth strengthens the mechanism because the deferred difference compounds over time. At extreme growth levels, progressive taxation may produce nonlinear effects that alter the relationship between declaration strategy and final outcomes.

**Proposition 3b: Understatement effects increase with holding period until tax saturation.** As holding period increases, declaration differences have more time to compound.

**Interpretation.** Two regions operate in practice: over short to intermediate horizons, basis differences compound and post-tax outcomes diverge; at extended horizons with high growth, the rate ceiling constrains further escalation. For understaters the penalty does not reverse within the tested range — it plateaus at approximately $g$ ≈ 17%, above all four RATES TCM tier differentials. At RATES-aligned calibration ($\tau_0$ = 15%, $\tau_m$ = 70%, $g$ = 7%), the mechanism operates in the compounding divergence phase throughout the tested holding period range. The plateau manifests within the tested horizon only at growth rates well above the historical mean.

### A.5.4 Proposition 4: Understater Penalties Plateau at the Rate Ceiling; Aggressive Overstatement Is Self-Limiting through a Temporal Crossing Mechanism

**Proposition.** Where the progressive tax function contains an upper marginal rate boundary, the understater's marginal penalty stops escalating once the rate ceiling is approached. The penalty does not reverse — it plateaus at a ceiling determined by $\alpha$, reached at approximately $g$ ≈ 17.3% across all understatement levels. This inflection is N-invariant above the plateau: simulation at N ∈ {10, 20, 29, 50} confirms that the plateau shape at N = 29 and N = 50 are visually identical, establishing that the ceiling is a property of the rate function rather than of compounding dynamics over long horizons (SWEEPS §2.3, Fig S3.1b).

For overstaters, outcomes diverge by degree and by time. At N = 30, the C.1 metric crosses from negative (apparent advantage) to positive (net-cost territory) at approximately $g$ ≈ 7% for all four tested overstater levels ($\alpha$ = 1.2, 1.5, 1.8, 2.0). The mild overstatement levels ($\alpha$ = 1.2, 1.5) are therefore in nominal net-cost territory at the historical mean growth rate (10.4%). Their nominal advantage is confined to the low-growth tail (g ≲ 7%) and even there does not survive present-value adjustment: (VAL.A §C.12) shows that discounting at ρ = 5% collapses or reverses the apparent advantage in the growth band where it nominally exists. Aggressive overstatement ($\alpha$ ≥ 1.8) additionally faces a contemporaneous net-cost corridor at $g$ ≈ 9–17% and a temporal N-crossing mechanism: at canonical parameters ($\tau_0$ = 15%), the $\alpha$ = 2.0 N-crossing arrives at N ≈ 30 and the $\alpha$ = 1.8 crossing at N ≈ 32 (SWEEPS.A §B.4.5). This temporal correction is $\tau_0$-sensitive: the crossing migrates to later horizons as $\tau_0$ rises, reaching N ≈ 41 by $\tau_0$ = 29% and disappearing entirely for realistic holding periods above $\tau_0$ ≈ 29–32%. The self-limiting properties hold at canonical parameters but are parameter-conditional results.

**Interpretation.** The inflection at $g$ ≈ 17.3% is a rate-function property, approximately constant across all $\alpha$. Deterrence against understatement is fully effective throughout the policy-relevant growth range (g = 2–17%); the plateau sets a ceiling on punishment, not a reversal.

For overstaters: no overstatement level constitutes a genuine present-value wealth-maximising strategy. The mild overstater levels ($\alpha$ = 1.2, 1.5) fall within the tolerant zone in the sense that their C.1 values are small in magnitude — but their nominal advantage at low growth is a timing artefact, and they are already in nominal net-cost territory at the historical mean. The $\alpha$ = 1.8 and $\alpha$ = 2.0 levels additionally enter a contemporaneous net-cost corridor at $g$ ≈ 9–10% and face an N-crossing accumulating cost at long horizons. Aggressive overstatement is a losing strategy in both nominal and present-value terms for most taxpayers under most conditions at canonical parameters — though the strength of this correction depends on $\tau_0$ remaining at or near its canonical value.

The plateau property follows from the bounded logistic rate structure. It does not generalise to unbounded tax schedules.

The model produces two operative regions for understaters:

| | |
|:---|:---|
| **Compounding region** | Basis differences accumulate and widen the gap between strategies. Dominant regime at RATES-aligned parameters across the full tested holding period range at moderate growth. |
| **Plateau region** | The progressive tax boundary limits further escalation of the understater penalty. Reached at approximately $g$ ≈ 17.3% across all $\alpha$; the penalty stabilises at a ceiling set by the degree of understatement. The inflection point is N-invariant above the plateau. |

### A.5.5 Proposition 5: Optimal Declaration Strategy Is Horizon-Dependent

**Proposition.** The economically optimal declaration strategy under WDT depends on the interaction between expected holding period, asset growth, progressive tax parameters, and any external economic effects associated with the declared valuation. It is not determined solely by minimising current tax liability.

**Interpretation.** The WDT creates a dynamic declaration problem:

$Optimal\ Declaration = f(Expected\ Growth,\ Holding\ Period,\ Tax\ Structure,\ External\ Effects)$

At short horizons, declaration differences have limited time to compound. Over intermediate horizons, basis differences accumulate and produce measurable terminal differences. At very long horizons, progressive tax saturation eventually constrains those differences.

Propositions 4 and 5 together establish that the WDT changes the nature of strategic declaration behaviour rather than eliminating it: the dominant conventional incentive — reducing declared wealth — is replaced by a horizon-dependent optimisation across expected future outcomes.

### A.5.6 Cost Functions and Indifference Conditions

C($\alpha$) is the total economic consequence of selecting declaration strategy $\alpha$ relative to honest declaration, covering lifetime tax differences, present value effects, dilution, and terminal settlement.

The indifference boundaries $\alpha$_low and $\alpha$_high are strategies where C($\alpha$) = 0. Their existence confirms no universal incentive toward either direction: the preferred strategy depends on growth, holding period, progressive rate escalation, and external economic effects.

| **Proposition** | **Result** | **Interpretation** |
|----|----|----|
| **Proposition 1** | Local convexity around $\alpha$ = 1 | Simulations indicate a locally stabilising incentive structure: small deviations create offsetting economic consequences rather than a persistent arbitrage opportunity. |
| **Proposition 2** | Overstatement effects increase with progressive rate steepness (k) | Progressive rates constrain persistent inflation of declared wealth by increasing exposure to higher marginal taxation. |
| **Proposition 3a** | Understatement effects increase with growth during the compounding phase | Higher growth amplifies the difference between declared basis and realised value, increasing the economic significance of understatement. |
| **Proposition 3b** | Understatement effects increase with holding period until tax saturation | Longer holding periods allow basis differences to compound, but the relationship is not unlimited; progressive tax saturation eventually constrains further divergence. |
| **Proposition 4** | Understater penalties plateau at the rate ceiling; all tested overstater levels cross into nominal net-cost territory above g ≈ 7% at N = 30; no overstatement level produces a genuine present-value return | The inflection at $g$ ≈ 17.3% is a rate-function property, N-invariant above the plateau and constant across all $\alpha$. Understater penalties plateau rather than reverse. At N = 30, C.1 turns positive (net-cost territory) at approximately $g$ ≈ 7% for all four tested overstater levels including $\alpha$ = 1.2 and $\alpha$ = 1.5; the nominal advantage is confined to the low-growth tail. The NPV-adjusted metric (VAL.A §C.12) eliminates or reverses this advantage throughout the low-growth band — it is a timing artefact. Aggressive overstatement ($\alpha$ ≥ 1.8) additionally faces a contemporaneous net-cost corridor at $g$ ≈ 9–17% and an N-crossing threshold ($\alpha$ = 2.0 at N ≈ 30, $\alpha$ = 1.8 at N ≈ 32) that imposes accumulating costs at long horizons; both the corridor and the crossing are $\tau_0$-sensitive. |
| **Proposition 5** | Optimal declaration strategy is horizon-dependent | The economically preferred declaration depends on expected holding period, growth assumptions, external signalling effects, and the structure of the progressive tax schedule. |
| **Proposition 6** | The declaration mechanism produces a broad tolerant zone with an asymmetric incentive structure and a conditional mild upward declaration bias | At canonical parameters, declarations approximately within $\alpha$ = 0.8–1.5 produce lifetime tax outcomes economically close to honest declaration (the tolerant zone). Within the zone, consequences are asymmetric: understatement reduces refund protection in loss years (VAL.A §C.6), while overstatement preserves it. Under valuation uncertainty and risk aversion, this asymmetry gives taxpayers an incentive to centre their declaration slightly above their central estimate, producing a model-implied behavioural centre near $\alpha$ ≈ 1.1. This is a conditional prediction, not an empirical estimate. The nominal TW_settled advantage associated with the overstatement side of the tolerant zone ($\alpha$ = 1.2, 1.5) is a timing artefact that does not survive NPV adjustment (VAL.A §C.12) and does not represent a wealth-maximising rationale. Aggressive overstatement is self-limiting through the contemporaneous growth-corridor mechanism and the temporal N-crossing. Understatement carries definite compounding costs and a refund-protection loss. |

## A.6 The Declaration Equilibrium: A Broad Tolerant Zone with a Conditional Mild Upward Bias

The analysis in (VAL.A §A.5) uses $\alpha$ = 1 as reference, which is correct for establishing local convexity and proposition structure. This section addresses the broader question of where declarations are expected to cluster in practice. The answer separates two distinct concepts that have sometimes been conflated in prior drafts: the range of declarations the mechanism tolerates, and the declaration level the model predicts taxpayers will choose.

**Concept 1: The tolerant zone.** At canonical parameters and the historical mean growth rate, declarations spanning approximately $\alpha$ = 0.8 to $\alpha$ = 1.5 produce lifetime tax outcomes within approximately 2pp of honest declaration (|C.1| < 2pp threshold, based on the C.1 table at $g$ = 10.4%). This is the tolerant zone. Both sides of honest declaration are included: mild understatement ($\alpha$ = 0.8) and the overstatement side ($\alpha$ = 1.2, 1.5) both land within this band. The zone is a design feature governed primarily by $k$: at $k$ = 0.0001 it spans nearly the full tested $\alpha$ range; at $k$ = 0.005 it narrows substantially (SWEEPS §2.1, SWEEPS §5.1, Fig S3.1c).

**Concept 2: The asymmetry within the tolerant zone.** While both sides of the tolerant zone produce similar net-tax outcomes, they produce different risk profiles. Understatement reduces refund protection in negative-growth states: at $g$ = −4.5%, $\alpha$ = 0.8 retains only 97.88% of the honest declarer's terminal wealth; $\alpha$ = 0.5 retains 93.76%; $\alpha$ = 0.1 retains 88.27% (VAL.A §C.6). Overstatement at $\alpha$ = 1.2 and $\alpha$ = 1.5 retains 100% in the same scenario — the lifetime cap prevents refunds exceeding prior contributions, but the larger contribution history from higher declarations means refund entitlement is never binding from above. An understater who is wrong in a bad year recovers materially less; an overstater in the same scenario recovers fully.

**Concept 3: The conditional behavioural prediction.** A taxpayer who does not know the precise value of their asset faces a declaration problem with a natural error band — typically ±10–20% for illiquid private assets. Under this uncertainty, the asymmetry in Concept 2 gives a risk-averse taxpayer an incentive to bias their declaration slightly upward: if they declare at their central estimate ($\alpha$ = 1.0 by assumption), the lower tail of their uncertainty band could land in understatement territory, reducing their refund protection in a loss year. Centring at approximately $\alpha$ ≈ 1.1 instead ensures the lower tail remains in overstatement territory. This does not require a growth forecast; it is a conservative response to valuation uncertainty. The model-implied behavioural centre is therefore near $\alpha$ ≈ 1.1. This prediction is conditional on the assumed uncertainty band and risk preference, and it is not an empirically estimated population parameter.

**What the nominal C.1 data do and do not show.** The C.1 table at N = 30 shows that $\alpha$ = 1.2 and $\alpha$ = 1.5 produce negative C.1 values (apparent advantage over honest declaration) at low growth ($g$ ≤ 5.9%) and positive C.1 values (net-cost territory) above approximately $g$ ≈ 7%. This means both strategies cross into nominal net-cost territory well below the historical mean growth rate. The apparent advantage at low growth is a timing artefact: periodic outflows are real early money; the sell-year refund is inflated late money. (VAL.A §C.12) confirms that once all cash flows are discounted at ρ = 5%, the apparent low-g advantage collapses or reverses. The $\alpha$ = 1.2 and $\alpha$ = 1.5 values in the tolerant zone are therefore illustrative points on the overstatement side of a symmetric zone, not evidence for a wealth-maximising equilibrium. The earlier claim in prior drafts that "the C.1 metric for $\alpha$ = 1.2 and $\alpha$ = 1.5 stays negative across the full tested growth range" is incorrect at N = 30 and has been removed.

**Why aggressive overstatement is self-limiting.** $\alpha$ = 1.8 and $\alpha$ = 2.0 exit the tolerant zone and face a contemporaneous net-cost corridor at $g$ ≈ 9–17% — the range containing the historical mean (10.45%) and all four RATES TCM tier differentials. Within the corridor the rate bracket penalty exceeds the basis benefit in each period. In addition, a temporal N-crossing mechanism operates independently: at canonical parameters, the $\alpha$ = 2.0 crossing arrives at N ≈ 30 and the $\alpha$ = 1.8 crossing at N ≈ 32 (SWEEPS.A §B.4.5, Fig S3.1a). The maximum nominal TW_settled benefit is bounded by degree — approximately 2.4pp at $\alpha$ = 1.2, 6.0pp at $\alpha$ = 1.5, 9.6pp at $\alpha$ = 1.8, and 12.0pp at $\alpha$ = 2.0 at the canonical intersection — with each ceiling set by rate-function saturation (VAL.A §C.11d); none survive NPV adjustment. This N-crossing is $\tau_0$-sensitive: the crossing migrates to later horizons as $\tau_0$ rises, reaching N ≈ 41 by $\tau_0$ = 29% and disappearing entirely for realistic holding periods above $\tau_0$ ≈ 29–32%. The self-limiting properties hold at canonical parameters but are parameter-conditional results.

**A parameter-conditional qualification.** The N-crossing threshold is $\tau_0$-sensitive. The tolerant zone width is $k$-sensitive. The conditional behavioural prediction of $\alpha$ ≈ 1.1 is sensitive to the assumed uncertainty band. None of these are unconditional structural properties. Both claims — that aggressive overstatement is self-limiting, and that risk-averse taxpayers under valuation uncertainty centre slightly above $\alpha$ = 1 — are stated with their relevant conditions.

**Summary: the correct conceptual hierarchy.**

$$
\text{Tolerant zone: } \alpha \approx 0.8\text{–}1.5 \rightarrow \text{asymmetric downside (understatement loses refund protection)} \rightarrow \text{conditional upward bias: } \alpha^* \approx 1.1 \rightarrow \text{aggressive overstatement self-limiting beyond the zone}
$$

**Consequences for mechanism design.** On revenue: the declared tax base likely slightly exceeds true values, collecting modestly more than exact honesty would produce in nominal terms, partially offsetting pre-behavioural overstatement in RATES. The C.12 discounting correction narrows this effect in present-value terms. On refund credibility: higher declared values generate larger contribution histories and potential refund entitlements. On audit triggers: a population concentrated near $\alpha$ = 1.1 produces few low-end outliers; the corrective Route D auction fires only against egregious outlier declarations in either direction.

**Three complications.** First, the SRR calibration implication. RATES calculates reserve requirements assuming declared values track true values. If the population centre sits at $\alpha$ ≈ 1.1, refund exposure in loss years is correspondingly larger. The magnitude cannot be quantified before Phase One data establishes where the population centre sits; (ENV §9.2.1) identifies the SRR floor adjustment as open question ENV-1.

Second, the public register carries systematically inflated declared values during holding periods if the upward bias materialises. A declared £12m on an asset worth £10m generates a correct negative delta and refund when it eventually sells, but the register entry is inflated throughout. Lenders and counterparties working from the register work from figures above true values — a credit-expansion effect on private asset-backed lending. The Administrator's consistency-credential architecture has no mechanism for surfacing the population distribution of $\alpha$ or signalling systematic drift in declared values. This is a monitoring gap; Phase One data on declared values relative to subsequent realisation prices is the primary detection instrument, and the Governing Council's SRR floor authority is the primary response instrument (SWEEPS §3.1) (RATES §6).

Third, a slow-drift risk. If new entrants anchor partly to prior register declarations, the population centre could drift gradually upward without any individual taxpayer making an unusual declaration. SRR exposure and register inflation compound with the drift. The absence of an observable instrument for the population distribution of $\alpha$ means drift is visible only ex post through the realisation price comparison.

\newpage

# B. Simulation Methodology

## B.1 Purpose

This appendix converts the recursive equations in (VAL.A §A) into a discrete period-by-period calculation executable across parameter grids where closed-form solutions are unavailable. The simulation models Route C incentives throughout; Route D mechanism cases are in (VAL.A §A). No additional theoretical assumptions are introduced.

## B.2 Simulation Algorithm

**Initialisation at t = 0:**

$f_{0} = 1$

$B_{0} = \alpha \cdot V_{0}$

$L_{0} = 0$

$Cumulative_{tax} = 0$

$Cumulative_{refund} = 0$

### B.2.1 For each period t = 1 to N

Where β = 0 (base case): $V_{t} = V_{0} \cdot (1 + $g$)^{t}$

Where β ≠ 0 (VAL.A §C.3) exploratory extension only): $V_{t} = V_{0} \cdot (1 + g_{eff})^{t}$, where

$g_{eff} = $g$ + \beta \cdot \ln(\alpha)$

The effective growth rate is the base rate plus an additive supplement proportional to ln($\alpha$). β is the per-period growth supplement from signalling, scaled by ln($\alpha$) so that honest declaration ($\alpha$ = 1) receives zero supplement. The supplement applies only where β ≠ 0; the base simulation uses β = 0 throughout.

**Formula note.** An earlier draft of this section stated the multiplicative form $g_{eff} = g \times (1 + \beta \cdot \ln(\alpha))$. The Python model uses the additive form above throughout. The two forms differ materially at large β values. The discrepancy is noted here rather than corrected because the β extension is speculative: the signalling channel it represents has some theoretical merit but is empirically uncalibrated and no claims in the main papers rest on it. The C.3 table is sensitivity illustration only.

$W_{t} = f_{(t-1)} \cdot \alpha \cdot V_{t}$

$\Delta_{t} = W_{t} - B_{(t-1)}$

$\tau_{t} = \frac{\tau_{m}}{\left( 1 + A \cdot \exp\left( - $k$ \cdot \left( W_{t} - W_{\min} \right) \right) \right)}$

$where\ A = \frac{(\tau_{m} - \tau_{0})}{\tau_{0}}$

If $\Delta_{t} > 0$:

$L_{t} = \tau_{t} \cdot \Delta_{t}$

$q_{t} = \frac{L_{t}}{W_{t}}$

$f_{t} = f_{(t-1)} \cdot (1 - q_{t})$

$Cumulative_{tax} + L_{t}$

If $\Delta_{t} < 0$:

$R_{t} = \tau_{t} \cdot |\Delta_{t}|$

$R_{t} = \min(R_{t},\ Cumulative_{tax} - Cumulative_{refund})\ [lifetime\ cap]$

$f_{t} = f_{(t-1)}$

$Cumulative_{refund} + R_{t}$

If $\Delta_{t} = 0$:

$f_{t} = f_{(t-1)}$

$B_{t} = W_{t}$

### B.2.2 Post-sale assessment at period N+1

$W_{(N+1)} = f_{N} \cdot V_{N}$

$\Delta_{(N+1)} = W_{(N+1)} - B_{N}$

$\tau_{(N+1)} = \frac{\tau_{m}}{\left( 1 + A \cdot \exp\left( - $k$ \cdot \left( W_{(N+1)} - W_{\min} \right) \right) \right)}$

If $\Delta_{(N+1)} > 0$:

$L_{(N+1)} = \tau_{(N+1)} \cdot \Delta_{(N+1)}$

$Cumulative_{tax} + L_{(N+1)}$

If $\Delta_{(N+1)} < 0$:

$R_{(N+1)} = \tau_{(N+1)} \cdot |\Delta_{(N+1)}|$

$R_{(N+1)} = \min(R_{(N+1)},\ Cumulative_{tax} - Cumulative_{refund})\ [cap]$

$Cumulative_{refund} + R_{(N+1)}$

$Terminal = f_{N} \cdot V_{N} - L_{(N+1)} + R_{(N+1)}$

The same loop runs for $\alpha$ = 1.0 at every parameter combination. All output metrics are expressed relative to this benchmark unless stated otherwise.

## B.3 Parameter Table

| **Symbol** | **Definition** | **Baseline** | **Sweep range** |
|:--:|----|----|----|
| $V_{0}$ | Initial declared net worth at entry | £20m | Fixed |
| $N$ | Holding period in annual assessment periods | 29 | 5 to 60 |
| $g$ | Annual true value growth rate | 7% | −10% to +15% |
| $k$ | Rate escalation parameter | 0.001 | 0.00001 to 0.1 |
| $\alpha$ | Portfolio-level aggregate declaration ratio: total declared net worth / total true net worth. See note below. | 1.0 (honest) | 0.1 to 2.0 |
| $\beta$ | Signalling growth supplement; additive: $g_{eff} = $g$ + \beta \cdot \ln(\alpha)$. Zero for base simulation; swept in (VAL.A §C.3) only. | 0% | Swept in (VAL.A §C.3) only |
| $\tau_{0}$ | Baseline marginal rate at $W_{min}$ | 15% | Fixed |
| $\tau_{m}$ | Asymptotic maximum marginal rate | 70% | Fixed |
| $\rho$ | Taxpayer discount rate | 5% | Fixed |
| $W_{\min}$ | Exemption threshold | £2m | Fixed |

Parameters are aligned with the Balanced transition scenario in (RATES). The 29-year reference holding period is the canonical horizon for that scenario, providing a common parameter set across the project's quantitative work.

**Note on $\alpha$ as a portfolio-level aggregate.** The WDT operates on total declared net worth, not on per-asset declaration ratios. $\alpha$ therefore represents the ratio of total declared net worth to total true net worth across the whole portfolio. How that aggregate arises — whether through uniform declaration across a pure Route C portfolio, or through professional valuation anchoring part of the portfolio at $\alpha$ = 1 while Route C/D assets are declared at a higher ratio — is irrelevant to the mechanism and to this model. A taxpayer with 50% of wealth professionally valued and 50% self-declared at an asset-level ratio of 2.0 has a portfolio-level $\alpha$ of 1.5, and is correctly modelled by the $\alpha$ = 1.5 row of every table in (VAL.A §C). The simulation models a single-asset portfolio as a tractable representation; the results apply equally to any portfolio composition producing the same aggregate $\alpha$, because the mechanism operates on declared net worth in total.

The lifetime refund cap is a hard constraint within the loop. It binds primarily in negative growth scenarios where an overstater's inflated basis would otherwise generate refunds exceeding prior tax contributions.

## B.4 Output Metrics

| **Metric** | **Formula** | **Table** | **Interpretation** |
|----|:--:|----|----|
| **Net tax difference / terminal net worth** | $\frac{(Net(\alpha) - Net(1)}{TW(\alpha)}$ | C.1, C.7 | Primary incentive metric. Positive: $\alpha$ pays more net tax than honest. Negative: $\alpha$ pays less. TW here is TW_settled (see below). |
| **Terminal wealth retention fraction** | $\frac{TW(\alpha)}{TW_{gross}}$ | C.2 | Post-tax terminal net worth as share of gross terminal net worth. |
| **Effective lifetime tax rate** | $\frac{Total\ tax}{(TW_{gross} - V_{0})}$ | C.4 | Total WDT as share of lifetime wealth generated. $\alpha$ = 1 throughout. |
| **Refund multiple vs honest** | $\frac{Total\ refunds(\alpha)}{Total\ refunds(1)}$ | C.6 | Effect of declaration strategy on symmetric protection in negative growth scenarios. |
| **TW_settled advantage decomposition** | See (A.4.17) | C.11 | Decomposes the overstater TW_settled advantage into: (1) W_sell_delta — f_N erosion cost; (2) refund_delta — sell-year refund benefit; (3) settle_delta — post-sale damping cost. The identity tw_adv = W_sell_delta − refund_delta − settle_delta holds to machine precision. Excess periodic tax is informational only and not additive. |

## B.5 Scope and Limitations

The simulation models a single-asset portfolio with constant growth and a fixed holding period. Real portfolios are multi-asset with varying holding periods and non-constant growth. The assessment window premium, flexibility levy, deferral charge, and rolling average smoothing are not modelled; the simulation assumes annual formal assessment throughout. These omissions likely overstate variance in the tax base and therefore the incentive to game.

The Route D auction mechanism (VAL.A §D), the public register, and professional costs of maintaining inconsistent valuations are not modelled. Where those deterrence mechanisms operate, the net benefit of misdeclaration would be lower than the tables show. The tables are an upper bound on gaming payoff under the self-declaration mechanism alone.

\newpage

# C. WDT Valuation Analysis: Summary Tables

**Validation status:** All figures in this section are from Python model v1.0 (standalone, no Excel dependency), confirmed 0 FAILs across all primary matrices. Parameters unified to $k$ = 0.001, N = 30, $\tau_0$ = 15% across all companion papers. Table C.3 carries deviations up to 13% at extreme $\alpha$×β values (threshold 15%; 0 FAILs); see (VAL.A §C.3) note.

Unless otherwise stated, all figures use base parameters: $V_0$ = £20m, N = 30, $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, $W_{min}$ = £2m, $g$ = 10.45%, $\alpha$ = 1, β = 0%. These are the Balanced transition scenario parameters from (RATES).

## C.1 Total Tax Paid (TTP) Difference Relative to Honest Declaration, as Share of Terminal Net Worth (TW)

**Metric:** (Net($\alpha$) − Net(1) / TW($\alpha$). Positive values indicate $\alpha$ pays more net tax than honest; negative values indicate less.

$\frac{Net(\alpha) - Net(1)}{TW(\alpha)}$

**Structural claim:** Understatement is more costly than honest declaration across the policy-relevant growth range. The penalty escalates steeply between $g$ ≈ 10% and $g$ ≈ 17.3%, then plateaus at a ceiling set by $\alpha$; the marginal deterrent stops escalating but does not reverse. The plateau inflection at $g$ ≈ 17.3% is a rate-function property that is approximately constant across all $\alpha$ and N-invariant above the plateau — simulation confirms that the plateau shape at N = 29 and N = 50 are visually identical (SWEEPS §2.3, Fig S3.1b). The C.1 metric for $\alpha$ = 0.1 exceeds 100% at approximately $g$ = 23–24% — the understater's excess tax exceeds their terminal wealth — but this is a normalisation artefact (the denominator, the understater's own TW, compresses at high growth), not a sign reversal in the penalty. For mild overstatement ($\alpha$ ≤ 1.5), overstatement produces a tax saving at moderate positive growth, with no reversal within the tested range at canonical parameters. For aggressive overstatement ($\alpha$ ≥ 1.8), the saving reverses in the $g$ ≈ 9–17% corridor containing the historical mean and recovers only above $g$ ≈ 17%; the self-limiting mechanism also operates temporally through the N-crossing described in §A.5.4. In negative growth scenarios the refund cap binds for understaters, reducing their net-tax advantage.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.28% | 12.34% | 3.97% | 2.23% | 1.35% | 1.07% | 0.66% | 0.68% | 1.71% | 6.21% |
| **0.2** | 11.55% | 10.81% | 3.45% | 1.91% | 1.13% | 0.88% | 0.49% | 0.45% | 1.21% | 4.67% |
| **0.5** | 6.65% | 6.47% | 2.03% | 1.08% | 0.58% | 0.41% | 0.12% | 0.01% | 0.22% | 1.48% |
| **0.8** | 2.17% | 2.48% | 0.76% | 0.39% | 0.19% | 0.11% | -0.02% | -0.10% | -0.11% | 0.10% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -0.95% | -0.70% | -0.34% | -0.13% | -0.05% | 0.10% | 0.22% | 0.35% | 0.46% |
| **1.5** | 0.00% | -0.91% | -1.66% | -0.75% | -0.22% | -0.02% | 0.40% | 0.76% | 1.28% | 2.04% |
| **1.8** | 0.00% | -0.86% | -2.51% | -1.06% | -0.21% | 0.12% | 0.86% | 1.53% | 2.65% | 4.49% |
| **2.0** | 0.00% | -0.83% | -3.02% | -1.22% | -0.15% | 0.28% | 1.25% | 2.17% | 3.77% | 6.51% |

Table C.1: TTP difference relative to honest declaration, as share of TW. $\alpha$ = 1.0 row is zero by construction. Positive values indicate understater pays more lifetime tax. $V_0$ = £20m, $k$ = 0.001, N = 30, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.2 Effective Lifetime Tax Rate Difference from Honest Declaration

**Metric:** Net($\alpha$)/TW($\alpha$) − Net(1)/TW(1). Positive values indicate $\alpha$ has a higher effective lifetime rate than the honest declarer.

$\frac{Net(\alpha)}{TW(\alpha)} - \frac{Net(1)}{TW(1)}$

**Structural claim:** Effective lifetime tax rate differences are directionally consistent with C.1 but larger in magnitude, because the formula normalises by TW($\alpha$) and TW(1) separately rather than by a common denominator. Understaters face materially higher effective rates than honest declarers across all tested growth rates; overstaters face lower rates at moderate growth. The differential is largest at low and high growth extremes, reflecting refund protection loss and saturation effects respectively.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.28% | 12.50% | 5.22% | 3.71% | 2.96% | 2.74% | 2.44% | 2.58% | 3.88% | 9.27% |
| **0.2** | 11.55% | 10.94% | 4.55% | 3.21% | 2.54% | 2.33% | 2.04% | 2.11% | 3.09% | 7.27% |
| **0.5** | 6.65% | 6.55% | 2.68% | 1.86% | 1.43% | 1.28% | 1.05% | 0.99% | 1.31% | 2.90% |
| **0.8** | 2.17% | 2.51% | 1.02% | 0.69% | 0.51% | 0.45% | 0.33% | 0.28% | 0.30% | 0.60% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -0.97% | -0.94% | -0.62% | -0.44% | -0.37% | -0.23% | -0.13% | -0.03% | 0.03% |
| **1.5** | 0.00% | -0.93% | -2.24% | -1.43% | -0.96% | -0.79% | -0.40% | -0.08% | 0.39% | 1.07% |
| **1.8** | 0.00% | -0.88% | -3.40% | -2.12% | -1.35% | -1.05% | -0.38% | 0.24% | 1.29% | 3.07% |
| **2.0** | 0.00% | -0.85% | -4.10% | -2.51% | -1.54% | -1.16% | -0.26% | 0.60% | 2.14% | 4.83% |

Table C.2: Effective lifetime tax rate difference from honest declaration. $\alpha$ = 1.0 row is zero by construction. $V_0$ = £20m, $k$ = 0.001, N = 30, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

*Note: this table measures the difference in effective lifetime tax rate relative to honest declaration, not an absolute rate.*

## C.3 Exploratory Extension: Investor Confidence Effects β (Overstatement Only)

*This section is exploratory and not required for the operation of WDT. The beta mechanism is not empirically calibrated. Results are sensitivity testing, not prediction.*

**Metric:** (Net($\alpha$,β) − Net(1,β=0) / TW($\alpha$,β). β swept over the same numeric values as the $g$ columns in C.1/C.2; $g$ fixed at 10.45%.

$\frac{Net(\alpha, \beta) - Net(1, \beta=0)}{TW(\alpha, \beta)}$

**Structural claim:** β represents the sensitivity of true asset growth to declared valuation via $g_{eff} = g + \beta \cdot \ln(\alpha)$ (see (VAL.A §B.2.1) and (VAL.A §B.2.2). A positive β partially offsets the declaration cost where overstatement contributes to confidence formation. Scope is overstatement only ($\alpha$ ≥ 1.0); understater cells are omitted. Deviations at high $\alpha$×β values (up to 13%) reflect exponential compounding of g_eff over N = 30; directional claims are unaffected. No empirical calibration for β exists.

| $\alpha$ \ β | β=-4.5% | β=0.4% | β=5.9% | β=8.4% | β=10.4% | β=11.4% | β=13.9% | β=16.4% | β=20.4% | β=25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | -2.43% | 0.08% | 2.46% | 3.44% | 4.19% | 4.53% | 5.38% | 6.20% | 7.39% | 8.74% |
| **1.5** | -5.88% | 0.25% | 5.15% | 6.95% | 8.27% | 8.85% | 10.26% | 11.58% | 13.50% | 15.80% |
| **1.8** | -9.18% | 0.49% | 7.31% | 9.68% | 11.41% | 12.17% | 14.08% | 15.99% | 19.12% | 23.64% |
| **2.0** | -11.32% | 0.70% | 8.65% | 11.39% | 13.45% | 14.37% | 16.79% | 19.37% | 23.96% | 30.88% |

Table C.3: Investor confidence β sensitivity (overstatement only). Sign convention: positive = $\alpha$ pays more than honest. β column values are the same numeric sweep as $g$ in C.1/C.2; $g$ fixed at 10.45%, N=30 throughout. Deviations increase at high $\alpha$×β due to exponential compounding; max deviation vs Excel 13% (threshold 15%; 0 FAILs). $V_0$ = £20m, $k$ = 0.001, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.4 Effective Lifetime Tax Rate by $k$ Parameter and Initial Wealth ($V_0$)

**Metric:** TTP($\alpha$=1) / TW($\alpha$=1). Honest declaration throughout. Rows = k; columns = $V_0$ (£m).

$\frac{TTP(\alpha=1)}{TW(\alpha=1)}$

**Structural claim:** The S-curve rate function produces an effective lifetime rate that is low at small $V_0$ and rises toward $\tau_m$ at very large $V_0$ × high $k$ combinations. The policy-relevant $k$ range is approximately 1e-04 to 1e-03; values above 5e-03 are analytically extreme and included for completeness only. The rate ceiling of approximately 60.67% reflects the logistic bound at $\tau_m$ = 70% over N = 30 years.

| $k$ \ $V_0$ | £1m | £10m | £50m | £100m | £250m | £500m | £1000m | £2500m | £5000m | £10000m |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1e-04 | 10.72% | 12.56% | 12.69% | 12.86% | 13.38% | 14.27% | 16.10% | 21.71% | 29.89% | 40.02% |
| 2e-04 | 10.72% | 12.59% | 12.86% | 13.21% | 14.27% | 16.10% | 19.85% | 29.89% | 40.02% | 47.43% |
| 5e-04 | 10.73% | 12.68% | 13.38% | 14.26% | 17.03% | 21.70% | 29.88% | 42.92% | 48.70% | 49.99% |
| 1e-03 | 10.74% | 12.85% | 14.25% | 16.08% | 21.69% | 29.87% | 40.01% | 48.69% | 49.99% | 50.05% |
| 2e-03 | 10.75% | 13.17% | 16.06% | 19.81% | 29.85% | 40.00% | 47.43% | 49.99% | 50.05% | 50.05% |
| 5e-03 | 10.81% | 14.17% | 21.60% | 29.80% | 42.88% | 48.69% | 49.99% | 50.05% | 50.05% | 50.05% |
| 1e-02 | 10.90% | 15.89% | 29.71% | 39.91% | 48.67% | 49.99% | 50.05% | 50.05% | 50.05% | 50.05% |
| 5e-02 | 11.63% | 28.97% | 48.58% | 49.99% | 50.05% | 50.05% | 50.05% | 50.05% | 50.05% | 50.05% |
| 1e-01 | 12.58% | 38.83% | 49.98% | 50.05% | 50.05% | 50.05% | 50.05% | 50.05% | 50.05% | 50.05% |

Table C.4: Effective lifetime tax rate by $k$ and $V_0$. All at $\alpha$=1, β=0, $g$=10.45%, N=30. $k$ values above 1e-03 are analytically extreme; included for completeness.

## C.5 Sensitivity of $k$ and Alpha: Terminal Net Worth Difference vs Honest

**Metric:** (TW($\alpha$,k) − TW(1,k) / TW(1,k). Positive values indicate $\alpha$ retains more terminal net worth than honest; negative values indicate less.

$\frac{TW(\alpha,k) - TW(1,k)}{TW(1,k)}$

**Structural claim:** TW differences are directionally consistent across the tested $k$ range. Understater penalties scale with $k$ up to the logistic saturation boundary, beyond which further increases have diminishing effect. The overstater advantage follows the same pattern, accelerating at high $k$ ($k$ ≥ 1e-02) as the rate function's bracket ascent steepens. $k$ values above 1e-03 are analytically extreme.

| $\alpha$ \ $k$ | 1e-04 | 2e-04 | 5e-04 | 1e-03 | 2e-03 | 5e-03 | 1e-02 | 5e-02 | 1e-01 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | -10.90% | -10.91% | -10.96% | -11.05% | -11.27% | -12.20% | -14.66% | -22.78% | -5.46% |
| **0.2** | -9.68% | -9.70% | -9.74% | -9.81% | -9.99% | -10.74% | -12.67% | -17.99% | -7.19% |
| **0.5** | -6.05% | -6.06% | -6.08% | -6.11% | -6.19% | -6.51% | -7.28% | -9.09% | -8.59% |
| **0.8** | -2.42% | -2.42% | -2.43% | -2.44% | -2.46% | -2.53% | -2.69% | -3.39% | -4.47% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 2.42% | 2.42% | 2.42% | 2.42% | 2.43% | 2.43% | 2.43% | 3.38% | 5.37% |
| **1.5** | 6.04% | 6.04% | 6.04% | 6.04% | 6.02% | 5.91% | 5.67% | 8.68% | 14.58% |
| **1.8** | 9.67% | 9.67% | 9.65% | 9.63% | 9.56% | 9.21% | 8.52% | 14.40% | 24.66% |
| **2.0** | 12.08% | 12.08% | 12.06% | 12.01% | 11.88% | 11.30% | 10.25% | 18.49% | 31.67% |

Table C.5: TW difference vs honest, by $k$ and $\alpha$. $\alpha$ = 1.0 row is zero by construction. $g$ = 10.45%, N = 30 throughout.

## C.6 Terminal Net Worth After Refunds: Refund Protection Ratio

**Metric:** TW($\alpha$) / TW(1). Values below 100% indicate reduced TW relative to honest. Negative $g$ scenarios only.

$\frac{TW(\alpha)}{TW(1)}$

**Structural claim:** Understaters receive materially reduced terminal wealth in negative growth scenarios because the refund is calculated on the declared basis, not the true value. The protection loss is determined almost entirely by the entry declaration and is stable across negative growth rates for each $\alpha$ — the ratio at $g$ = −4.5% characterises the full negative-$g$ regime. Overstaters show 100% throughout: the lifetime cap prevents refunds exceeding prior contributions, which in a purely negative growth environment are zero for all strategies.

| $\alpha$ \ $g$ | -4.5% |
|:---:|:---:|
| **0.1** | 88.27% |
| **0.2** | 89.65% |
| **0.5** | 93.76% |
| **0.8** | 97.88% |
| **1.0** | 100.00% |
| **1.2** | 100.00% |
| **1.5** | 100.00% |
| **1.8** | 100.00% |
| **2.0** | 100.00% |

Table C.6: Refund protection ratio vs honest declaration. Negative $g$ scenarios only. $\alpha$ = 1.0 is 100% by construction. Understater protection loss proportional to basis gap at entry. $V_0$ = £20m, $k$ = 0.001, N = 30, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.7 Total Tax Paid Compared to Honest Taxpayer, Adjusted for N

**Metric:** (Net($\alpha$,N) − Net(1,N) / Net(1,N). Positive values indicate $\alpha$ pays more net tax than honest. N values shown are actual simulation N (5 to 60). Earlier Excel display showed N-5 in column headers; corrected here.

$\frac{Net(\alpha,N) - Net(1,N)}{Net(1,N)}$

**Structural claim:** Understatement imposes a persistent and substantial net-tax penalty across all holding periods tested. The penalty is largest at short horizons (N = 5) where the basis gap recovery dominates a small total tax base, and compresses as the holding period extends. For overstatement, the initial advantage narrows and can reverse at extended horizons where the honest declarer has accumulated more basis history. Understater N = 5 penalties above 100% reflect the realisation delta dominating a near-zero prior-year contribution.

| $\alpha$ \ N | 5 | 10 | 15 | 20 | 25 | 30 | 35 | 40 | 45 | 50 | 55 | 60 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 105.67% | 40.00% | 17.61% | 7.86% | 3.85% | 3.47% | 6.25% | 12.68% | 24.00% | 41.38% | 61.99% | 73.51% |
| **0.2** | 93.79% | 35.35% | 15.38% | 6.58% | 2.82% | 2.18% | 4.16% | 9.08% | 17.77% | 30.87% | 45.68% | 52.60% |
| **0.5** | 58.35% | 21.72% | 9.08% | 3.35% | 0.64% | -0.34% | 0.01% | 1.63% | 4.68% | 9.05% | 13.24% | 13.86% |
| **0.8** | 23.23% | 8.54% | 3.42% | 1.03% | -0.20% | -0.81% | -1.02% | -0.91% | -0.51% | 0.10% | 0.61% | 0.54% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | -23.09% | -8.34% | -3.14% | -0.62% | 0.80% | 1.70% | 2.36% | 2.90% | 3.37% | 3.70% | 3.78% | 3.52% |
| **1.5** | -57.45% | -20.46% | -7.31% | -0.79% | 3.11% | 5.92% | 8.35% | 10.77% | 13.14% | 14.90% | 15.17% | 13.55% |
| **1.8** | -80.00% | -32.13% | -10.84% | -0.05% | 6.77% | 12.10% | 17.17% | 22.52% | 27.73% | 31.18% | 31.05% | 26.97% |
| **2.0** | -77.69% | -39.66% | -12.84% | 0.96% | 9.95% | 17.29% | 24.57% | 32.33% | 39.69% | 44.12% | 43.25% | 37.04% |

Table C.7: Net tax compared to honest taxpayer, adjusted for N. $\alpha$ = 1.0 row is zero by construction. $g$ = 10.45% throughout. $V_0$ = £20m, $k$ = 0.001, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.8 Terminal Net Worth Compared to Honest Taxpayer, Adjusted for N

**Metric:** (TW($\alpha$,N) − TW(1,N) / TW(1,N). Negative values indicate $\alpha$ retains less TW than honest. N correction as C.7 — actual N shown.

$\frac{TW(\alpha,N) - TW(1,N)}{TW(1,N)}$

**Structural claim:** TW differences widen materially as N rises — the basis gap compounds into more pronounced divergence at $k$ = 0.001 than at lower k. The understater penalty at $\alpha$ = 0.1 grows from −12.76% at N = 5 to −41.99% at N = 60. Overstater advantages widen on the same trajectory. No convergence toward zero occurs within realistic holding periods at $g$ = 10.45%.

| $\alpha$ \ N | 5 | 10 | 15 | 20 | 25 | 30 | 35 | 40 | 45 | 50 | 55 | 60 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | -11.03% | -11.04% | -11.04% | -11.06% | -11.09% | -11.19% | -11.41% | -11.96% | -13.26% | -16.04% | -20.30% | -21.96% |
| **0.2** | -9.81% | -9.81% | -9.81% | -9.82% | -9.84% | -9.90% | -10.06% | -10.46% | -11.41% | -13.43% | -16.37% | -17.09% |
| **0.5** | -6.13% | -6.12% | -6.12% | -6.11% | -6.10% | -6.11% | -6.13% | -6.23% | -6.49% | -7.04% | -7.71% | -7.43% |
| **0.8** | -2.45% | -2.45% | -2.44% | -2.43% | -2.42% | -2.41% | -2.39% | -2.38% | -2.37% | -2.39% | -2.39% | -2.23% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 2.45% | 2.44% | 2.43% | 2.42% | 2.40% | 2.37% | 2.32% | 2.24% | 2.12% | 1.96% | 1.79% | 1.69% |
| **1.5** | 6.12% | 6.10% | 6.07% | 6.03% | 5.96% | 5.85% | 5.66% | 5.35% | 4.90% | 4.30% | 3.77% | 3.62% |
| **1.8** | 9.07% | 9.75% | 9.70% | 9.61% | 9.47% | 9.23% | 8.84% | 8.22% | 7.28% | 6.15% | 5.22% | 5.15% |
| **2.0** | 9.97% | 12.18% | 12.10% | 11.98% | 11.78% | 11.44% | 10.89% | 9.99% | 8.70% | 7.18% | 6.01% | 6.04% |

Table C.8: TW compared to honest taxpayer, adjusted for N. $\alpha$ = 1.0 row is zero by construction. $g$ = 10.45% throughout. $V_0$ = £20m, $k$ = 0.001, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.9 Summary of Declaration Incentives Across Growth Regimes

**Metric:** TW(£m) and Net tax (£m) at $\alpha$ ∈ {2.0, 1.0, 0.1} across the $g$ sweep; ratios vs honest. N = 30 throughout.

**Structural claim:** The mechanism's fundamental properties hold across the full tested growth range. Understatement consistently costs more than honest declaration in absolute net-tax terms at every positive $g$ tested. The understater penalty escalates steeply between $g$ ≈ 10% and $g$ ≈ 17.3%, then plateaus — the rate ceiling stops further escalation but does not reverse it. The plateau ceiling scales with the degree of understatement: $\alpha$ = 0.1 plateaus near 98% of true wealth, $\alpha$ = 0.2 near 70%, $\alpha$ = 0.5 near 24%, $\alpha$ = 0.8 near 6%. The inflection at $g$ ≈ 17.3% is a rate-function property, approximately constant across all $\alpha$ and N-invariant above the plateau (see §A.5.4 and SWEEPS §2.3, Fig S3.1b). For overstaters, this table captures the contemporaneous growth-corridor effect for aggressive overstatement; the temporal N-crossing correction operates across holding periods and is documented in §C.8 and SWEEPS.A §A.4. The TW(0.1)/TW(1) ratio declines from approximately 86–87% at moderate growth to 63.2% at $g$ = 25.4%, reflecting compounding basis gap effects consistent with the penalty plateau. The C.1 metric exceeding 100% at $g$ = 25.4% for $\alpha$ = 0.1 is a normalisation artefact: it means the excess tax exceeds the understater's terminal wealth, not that the penalty reverses.

| $g$ | TW($\alpha$=2) £m | TW($\alpha$=1) £m | TW($\alpha$=0.1) £m | Net($\alpha$=2) £m | Net($\alpha$=1) £m | Net($\alpha$=0.1) £m | TW(0.1)/TW(1) | Net(0.1)/Net(1) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 25.4% | 1038.4 | 959.4 | 842.4 | 279.3 | 211.7 | 264.0 | 87.8% | — |
| 20.4% | 545.9 | 495.9 | 442.3 | 109.1 | 88.5 | 96.1 | 89.2% | — |
| 16.4% | 311.2 | 280.2 | 250.1 | 50.9 | 44.2 | 45.9 | 89.3% | — |
| 13.9% | 213.6 | 191.6 | 170.8 | 30.7 | 28.0 | 29.2 | 89.2% | — |
| 11.4% | 146.0 | 130.5 | 116.2 | 18.0 | 17.6 | 18.9 | 89.0% | — |
| 10.4% | 126.0 | 112.5 | 100.1 | 14.4 | 14.6 | 16.0 | 88.9% | — |
| 8.4% | 91.2 | 81.3 | 72.2 | 8.4 | 9.6 | 11.2 | 88.8% | — |
| 5.9% | 61.0 | 54.2 | 48.0 | 3.4 | 5.3 | 7.2 | 88.6% | — |
| 0.4% | 22.0 | 21.6 | 19.1 | 0.1 | 0.2 | 2.6 | 88.2% | — |

Table C.9: Summary of declaration incentives across growth regimes. TW and Net tax in £m. N = 30 throughout. Net($\alpha$=0.1)/Net($\alpha$=1) shown only where Net < 0 (refund scenario, negative $g$); '—' at positive $g$ where both Net values are positive. $V_0$ = £20m, $k$ = 0.001, N = 30, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

## C.10 2000 Historical Return Series — Reference Scenario Results

**Source:** RATES Balanced worst-case reference scenario (p['returns'] rotated to 2000 start year). $V_0$ = £20m, $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, $W_{min}$ = £2m. No β adjustment applied.

**Purpose:** Locates the RATES worst-case scenario within the analytical space of C.1–C.9. The 2000 series spans the dot-com crash, the 2008 financial crisis, and subsequent recovery. The realised mean growth rate across N = 30 periods is 7.05%, below the 10.45% historical mean used in C.1–C.9; results here represent a harder test than the constant-$g$ tables.

### C.10.1 Declaration strategy comparison ($\alpha$ sweep, N = 30)

Each row uses p['returns'][:N] as the holding-period series and p['returns'][N] as the sell-year rate. The g_mean column is the arithmetic mean of the N holding-period returns.

| $\alpha$ | TW (£m) | TTP (£m) | Net (£m) | Eff rate | TW vs honest | Net vs honest |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 57.87 | 10.13 | 8.79 | 15.19% | -11.03% | +25.82% |
| **0.2** | 58.67 | 9.84 | 8.57 | 14.61% | -9.80% | +22.71% |
| **0.5** | 61.07 | 9.01 | 7.95 | 13.01% | -6.11% | +13.75% |
| **0.8** | 63.46 | 8.21 | 7.36 | 11.59% | -2.44% | +5.32% |
| **1.0** | 65.05 | 7.71 | 6.99 | 10.74% | +0.00% | +0.00% ← honest |
| **1.2** | 66.63 | 8.24 | 6.63 | 9.95% | +2.44% | -5.08% |
| **1.5** | 69.00 | 10.39 | 6.13 | 8.88% | +6.08% | -12.25% |
| **1.8** | 71.36 | 12.57 | 5.67 | 7.94% | +9.71% | -18.88% |
| **2.0** | 72.93 | 14.04 | 5.38 | 7.38% | +12.12% | -23.00% |

Table C.10.1: Declaration strategy comparison, 2000 historical return series, N = 30. $\alpha$ = 1.0 row is the honest baseline; TW vs honest and Net vs honest are zero by construction. Positive Net vs honest = understater pays more net tax than honest under the historical series.

### C.10.2 Honest declarer trajectory by N ($\alpha$ = 1.0)

Each row uses p['returns'][:N] as the holding-period series and p['returns'][N] as the sell-year rate. The g_mean column is the arithmetic mean of the N holding-period returns; it shifts as more years of the 2000 series are included, most notably around N = 9 (2008 crash enters) and N = 10 (2009 recovery enters).

| N | TW (£m) | Net (£m) | Mean $g$ of series[:N] |
|:---:|:---:|:---:|:---:|
| 5 | 33.18 | 2.02 | 9.89% |
| 10 | 40.90 | 3.21 | 7.77% |
| 15 | 52.35 | 4.99 | 7.42% |
| 20 | 65.99 | 7.13 | 7.14% |
| 25 | 69.46 | 7.68 | 6.01% |
| **30** | **89.36** | **10.86** | **5.99%** |

Table C.10.2: Honest declarer trajectory under 2000 historical return series by holding period. N = 30 row is the RATES reference scenario. TW and Net grow with N as additional years of compounding and WDT payments accumulate. Unlike C.7/C.8 (constant $g$ throughout), each row reflects a different prefix of the realised return history, making path-dependence explicit.

## C.11 Overstater TW Advantage Decomposition

**Purpose:** Identifies the three mechanical sources of the overstater TW advantage shown in C.8. For each ($\alpha$, $g$) cell the TW advantage relative to honest declaration is split into: (1) excess periodic net tax paid during the holding period, (2) the sell-year settlement delta, and (3) the post-sale oscillation delta. These three terms sum to the C.8 figure (sign-adjusted). An additional sub-table shows $f_N$ — the retained equity fraction at end of holding period — as a ratio to the honest declarer's $f_N$, quantifying the dilution cost of overstatement.

**Identity (corrected):** TW_settled($\alpha$) $-$ TW_settled(1) $=$ W_sell_delta $-$ RefundDelta $-$ SettleDelta  (verified to machine precision across all tested $(\alpha, g)$ pairs).  W_sell_delta $\leq 0$: f_N erosion reduces sell-year proceeds.  RefundDelta $\leq 0$: overstater receives a larger sell-year refund.  SettleDelta $\geq 0$: post-sale oscillation taxes back part of the refund.  Note: ExcessPeriodic (holding-period net tax difference) is **not** additive in this identity — it feeds into TW_advantage indirectly through f_N erosion and is shown in C.11.1 for reference only.

**Scope:** Overstaters only ($\alpha$ ≥ 1.0). All values at canonical N = 30, $k$ = 0.001, $V_0$ = £20m. Rows = $\alpha$; columns = $g$ (same grid as C.1). Sub-tables C.11.1–C.11.4 expressed as % of TW_settled(1); C.11.5 is dimensionless.

### C.11.1 — W_sell_delta as % of Honest TW_settled  [Additive Term 1]

**Formula:** (W_sell($\alpha$) $-$ W_sell(1)) / TW_settled(1)  $\leq 0$ for $\alpha > 1$.  W_sell $= f_N \times V_{sell}$; the overstater's f_N is depleted faster by higher periodic tax, reducing the sell-year declared value.  This is the f_N erosion cost of overstatement: the overstater owns a smaller fraction of the asset at sale.  Note: ExcessPeriodic (holding-period net tax difference) is related but **not** equal to W_sell_delta — the excess periodic tax is approximately 6× larger than |W_sell_delta| at canonical parameters because most of the excess is returned via the sell-year refund (C.11.2).  ExcessPeriodic is shown separately in C.11.6 for reference.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -0.00% | -0.07% | -0.12% | -0.19% | -0.22% | -0.35% | -0.54% | -1.01% | -2.10% |
| **1.5** | 0.00% | -0.01% | -0.17% | -0.31% | -0.47% | -0.56% | -0.87% | -1.34% | -2.51% | -5.12% |
| **1.8** | 0.00% | -0.01% | -0.27% | -0.49% | -0.75% | -0.89% | -1.39% | -2.14% | -3.99% | -7.98% |
| **2.0** | 0.00% | -0.02% | -0.34% | -0.62% | -0.93% | -1.12% | -1.74% | -2.67% | -4.96% | -9.78% |

Table C.11.1: W_sell_delta as % of honest TW_settled (additive term 1). Always $\leq 0$ for $\alpha > 1$: f_N erosion reduces sell-year proceeds. $V_0$ = £20m, $k$ = 0.001, N = 30.

*Always $\leq 0$ for $\alpha > 1$: the overstater surrenders more equity as periodic tax, depressing the sell-year declared value.  The magnitude grows with both $\alpha$ and $g$ but is much smaller than the refund benefit (C.11.2) — this is why the net TW advantage (C.11.4) remains positive across the tested range.*

### C.11.2 — Sell-Year Settlement Delta as % of Honest TW_settled

**Formula:** ($L_{sell}$($\alpha$) $-$ $L_{sell}$(1)) / TW_settled(1)  · Negative = overstater receives a larger refund (or smaller tax) at sale. The declared basis at sale always exceeds true proceeds for $\alpha$ > 1 at any finite $g$, generating a refund that partially offsets the periodic cost.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.37% | -2.99% | -3.00% | -3.04% | -3.06% | -3.16% | -3.34% | -3.86% | -5.27% |
| **1.5** | 0.00% | -1.70% | -7.48% | -7.50% | -7.57% | -7.63% | -7.87% | -8.28% | -9.49% | -12.62% |
| **1.8** | 0.00% | -2.04% | -11.95% | -11.98% | -12.09% | -12.17% | -12.52% | -13.14% | -14.91% | -19.38% |
| **2.0** | 0.00% | -2.27% | -14.93% | -14.95% | -15.08% | -15.18% | -15.59% | -16.33% | -18.43% | -23.58% |

Table C.11.2: Sell-year settlement delta as % of honest TW_settled. Negative = overstater received a larger refund at sale. $V_0$ = £20m, $k$ = 0.001, N = 30.

*Negative throughout (refund benefit) for all $\alpha$ > 1. Magnitude grows with $\alpha$ but is bounded by the lifetime cap. At high $g$ the honest declarer also pays a large sell-year tax, compressing the relative benefit.*

### C.11.3 — Post-Sale Settlement Delta as % of Honest TW_settled

**Formula:** (net_settle_tax($\alpha$) $-$ net_settle_tax(1)) / TW_settled(1)  · Positive = the post-sale oscillation taxes back more of the overstater's sell-year refund than it does for the honest declarer. This is the damping cost: a larger sell-year refund creates a larger positive delta in the first post-sale period, which is taxed back.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | 0.18% | 0.40% | 0.41% | 0.43% | 0.44% | 0.47% | 0.52% | 0.69% | 1.18% |
| **1.5** | 0.00% | 0.23% | 1.01% | 1.04% | 1.07% | 1.09% | 1.17% | 1.31% | 1.71% | 2.89% |
| **1.8** | 0.00% | 0.27% | 1.62% | 1.66% | 1.71% | 1.74% | 1.87% | 2.09% | 2.71% | 4.52% |
| **2.0** | 0.00% | 0.30% | 2.03% | 2.07% | 2.14% | 2.18% | 2.34% | 2.61% | 3.38% | 5.57% |

Table C.11.3: Post-sale settlement delta as % of honest TW_settled. Positive = oscillation recovered more from overstater's refund. $V_0$ = £20m, $k$ = 0.001, N = 30.

*Positive throughout for $\alpha$ > 1: the settle_tw() oscillation always recovers some of the sell-year refund via subsequent tax. The damping cost is smaller than the refund benefit (C.11.2) in all tested cases — the net refund position remains favourable.*

### C.11.4 — Total TW Advantage as % of Honest TW_settled (Cross-Check)

**Formula:** (TW_settled($\alpha$) $-$ TW_settled(1)) / TW_settled(1)  · Should equal C.8 at the canonical N column. Values here are computed from the full decomposition and serve as an internal consistency check on C.11.1–C.11.3.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | 1.18% | 2.52% | 2.47% | 2.42% | 2.40% | 2.35% | 2.28% | 2.17% | 1.99% |
| **1.5** | 0.00% | 1.47% | 6.29% | 6.16% | 6.04% | 5.98% | 5.82% | 5.64% | 5.27% | 4.62% |
| **1.8** | 0.00% | 1.76% | 10.05% | 9.83% | 9.63% | 9.53% | 9.25% | 8.91% | 8.21% | 6.88% |
| **2.0** | 0.00% | 1.95% | 12.56% | 12.26% | 12.01% | 11.88% | 11.51% | 11.06% | 10.08% | 8.23% |

Table C.11.4: Total TW advantage as % of honest TW_settled. Should match C.5 (at canonical $k$) and C.8 (at canonical N) for each $\alpha$. $V_0$ = £20m, $k$ = 0.001, N = 30.

*Should match C.5 (at canonical $k$) and C.8 (at canonical N) for each $\alpha$. Any discrepancy exceeding 0.01pp indicates a decomposition error.*

### C.11.5 — Retained Equity Fraction Ratio at End of Holding Period

**Formula:** $f_N$($\alpha$) / $f_N$(1)  · Values below 1.0 indicate the overstater has surrendered more equity as tax during the holding period. This is the dilution cost: the overstater owns a smaller fraction of their asset at sale, which is why the sell-year declared value ($f_N \times V_{sell}$) is lower than it would otherwise be. The $f_N$ ratio is independent of $g$ within holding periods but shifts across $g$ because the progressive rate responds to declared wealth level.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| **1.2** | 1.0000 | 1.0000 | 0.9993 | 0.9988 | 0.9982 | 0.9978 | 0.9966 | 0.9948 | 0.9902 | 0.9798 |
| **1.5** | 1.0000 | 0.9999 | 0.9983 | 0.9970 | 0.9954 | 0.9945 | 0.9914 | 0.9869 | 0.9756 | 0.9508 |
| **1.8** | 1.0000 | 0.9999 | 0.9973 | 0.9951 | 0.9926 | 0.9912 | 0.9863 | 0.9790 | 0.9611 | 0.9233 |
| **2.0** | 1.0000 | 0.9998 | 0.9966 | 0.9939 | 0.9908 | 0.9890 | 0.9828 | 0.9738 | 0.9517 | 0.9059 |

Table C.11.5: Retained equity fraction ratio $f_N$($\alpha$) / $f_N$(1). Values below 1.0 = overstater surrendered more equity during holding period. $V_0$ = £20m, $k$ = 0.001, N = 30.

*Always < 1.0 for $\alpha$ > 1: the overstater's retained fraction is lower at every $g$. The ratio shrinks with $\alpha$ (more dilution) and with $g$ (higher declared wealth pushes the rate function higher, increasing $q$ each period). The $f_N$ ratio is the mechanism through which the declared basis at sale falls below $\alpha \times$ true value — it is not $\alpha \times f_N$(honest) $\times V_{sell}$ but rather $f_N$($\alpha$) $\times V_{sell}$, where $f_N$($\alpha$) < $f_N$(honest).*

*Key design implication: the overstater cannot manufacture a TW advantage by overstatement alone. The advantage in C.11.4 / C.8 persists because the sell-year refund benefit (C.11.2) swamps the f_N erosion cost (C.11.1) and the damping cost (C.11.3) across all tested ($\alpha$, $g$) — by a factor of approximately 6:1 at canonical parameters. Whether this relationship holds beyond the tested range — particularly at very high $g$ where $f_N$ is heavily depleted — requires extension of the $g$ sweep above 25%.*

### C.11.6 — Excess Periodic Net Tax as % of Honest TW_settled  [Informational]

**Formula:** (Net_holding($\alpha$) $-$ Net_holding(1)) / TW_settled(1)  · Positive = overstater paid more net tax during the holding period.  **This term is NOT additive in the C.11 identity** — it is shown for reference only.  ExcessPeriodic feeds into tw_advantage indirectly through f_N erosion (higher periodic tax depletes f faster, reducing W_sell), but ExcessPeriodic $\gg$ |W_sell_delta| because most of the excess is returned as a sell-year refund (C.11.2).  The correct additive decomposition uses W_sell_delta (C.11.1), not ExcessPeriodic.

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | 0.34% | 2.43% | 2.85% | 3.20% | 3.38% | 4.05% | 5.12% | 7.30% | 8.40% |
| **1.5** | 0.00% | 0.86% | 6.13% | 7.25% | 8.18% | 8.69% | 10.50% | 13.29% | 18.25% | 20.26% |
| **1.8** | 0.00% | 1.38% | 9.90% | 11.77% | 13.37% | 14.26% | 17.36% | 21.91% | 29.04% | 31.41% |
| **2.0** | 0.00% | 1.73% | 12.45% | 14.87% | 16.95% | 18.11% | 22.14% | 27.83% | 36.09% | 38.51% |

Table C.11.6: Excess periodic net tax as % of honest TW_settled (informational). Positive = overstater paid more net tax during holding period. Compare with C.11.1 (W_sell_delta): ExcessPeriodic is approximately 6× larger in magnitude, confirming that most of the periodic overpayment is recovered via the sell-year refund. $V_0$ = £20m, $k$ = 0.001, N = 30.

*Positive throughout at $g$ \geq ~8\%: the overstater pays more every period due to a larger declared delta and higher progressive rate. Despite this persistent periodic cost, the sell-year refund (C.11.2) exceeds both the erosion cost (C.11.1) and the damping cost (C.11.3), producing the net TW advantage shown in C.11.4.*

## C.12 NPV-Adjusted Tax Position: Present Value of Tax Difference vs Honest

**Purpose:** Adjusts the C.1 nominal tax-difference metric for the time value of money. The C.1 metric treats £1 of tax paid in year 1 as equivalent to £1 received as a refund in year N+1. C.12 corrects this by discounting all cash flows to t=0 at a common rate ρ. The comparison reveals whether the apparent nominal advantage to mild overstaters survives discounting — or whether it is an artefact of comparing early real outflows against a late nominal refund.

**Metric:** $(NPV_{tax}(\alpha) - NPV_{tax}(1))$ / TW_settled(1), where $NPV_{tax}(\alpha) = \sum_{t=1}^{N+1} L_t / (1+\rho)^t$ and $\rho = 5\%$.

$\frac{NPV_{tax}(\alpha) - NPV_{tax}(1)}{TW_{settled}(1)}$

**Sign convention:** Positive = alpha pays more in present-value terms than honest (understater disadvantage). Negative = alpha pays less in PV terms (overstater advantage). Same as C.1, so tables are directly comparable.

**Structural claim:** Two regimes are visible when C.1 and C.12 are compared. At ρ = 5%, a cash flow at year 30 is worth approximately 23 pence on the pound relative to a year-1 payment, so the discount penalises late flows heavily. **Low-g regime (g $\lesssim$ 8%):** these are the cells where C.1 shows a genuine nominal advantage for overstaters (negative values). In C.12 those values compress sharply toward zero or reverse sign. At low g, the sell-year refund is large relative to periodic payments and arrives heavily discounted; the earlier periodic costs are smaller but weighted at shorter horizons. Discounting closes the gap: the apparent nominal advantage is a timing artefact. **Mid/high-g regime (g $\gtrsim$ 8%):** overstaters already pay more than honest declarers in C.1 (positive values). C.12 is larger still in this regime because the bulk of periodic overpayment concentrates in later holding years (when declared wealth is largest), but the sell-year refund is also late and discounted at the same rate; the net effect is that discounting penalises the refund more than the distributed periodic costs, pushing the C.12 value above C.1. **Understaters:** C.12 is systematically smaller in magnitude than C.1 at mid/high g. Understaters declare a lower basis and pay smaller periodic taxes early; their larger settlement at sale is discounted, partially offsetting their nominal penalty. At low g and high understatement, C.12 can turn negative (understater appears to benefit in PV terms because the refund on a very low basis is received early relative to the honest declarer's larger late settlement). The core design claim is preserved and strengthened: the low-g overstater advantage, which motivates the §A.6 population-equilibrium argument, is a nominal timing artefact that collapses once discounted. In PV terms it is approximately neutral or negative, making the design's tolerance of mild overstatement even more defensible than the nominal analysis suggests.

**Scope:** Full α grid (same as C.1). All values at canonical N = 30, $k$ = 0.001, $V_0$ = £20m, $\rho$ = 5%, $\tau_0$ = 15%, $\tau_m$ = 70%. Rows = α; columns = g (same grid as C.1).

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 5.08% | 4.53% | 0.25% | -0.48% | -0.79% | -0.86% | -0.90% | -0.73% | 0.00% | 2.42% |
| **0.2** | 4.49% | 4.02% | 0.21% | -0.45% | -0.72% | -0.79% | -0.84% | -0.71% | -0.11% | 1.87% |
| **0.5** | 2.70% | 2.51% | 0.11% | -0.31% | -0.49% | -0.54% | -0.60% | -0.55% | -0.28% | 0.66% |
| **0.8** | 0.92% | 1.00% | 0.04% | -0.14% | -0.22% | -0.24% | -0.27% | -0.26% | -0.19% | 0.07% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -0.38% | -0.02% | 0.15% | 0.24% | 0.27% | 0.31% | 0.32% | 0.30% | 0.18% |
| **1.5** | 0.00% | -0.29% | -0.04% | 0.42% | 0.64% | 0.71% | 0.84% | 0.91% | 0.95% | 0.86% |
| **1.8** | 0.00% | -0.20% | -0.03% | 0.72% | 1.10% | 1.22% | 1.47% | 1.63% | 1.83% | 1.99% |
| **2.0** | 0.00% | -0.14% | -0.01% | 0.94% | 1.43% | 1.60% | 1.93% | 2.18% | 2.54% | 2.95% |

Table C.12: NPV-adjusted tax difference vs honest declaration, as % of honest TW_settled. $\alpha$ = 1.0 row is zero by construction. Compare directly with C.1: values closer to zero indicate the nominal C.1 advantage/disadvantage is a timing artefact; sign reversals indicate the PV position is opposite to the nominal position. $\rho$ = 5%, $V_0$ = £20m, $k$ = 0.001, N = 30, $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

*Key reading:* Compare C.12 with C.1 column by column. Where C.1 shows a negative value for overstaters (advantage) and C.12 shows a value close to zero or positive, the nominal advantage is a timing artefact: the overstater pays early and is refunded late, and the time value of early payment approximately cancels or reverses the apparent gain. Where C.1 and C.12 agree in sign and magnitude for understaters, the penalty is real in both nominal and PV terms — understaters face genuine excess cost regardless of the discount rate applied.
