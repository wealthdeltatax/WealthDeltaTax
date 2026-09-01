---
title: "The Wealth Delta Tax: Parameter Sweeps and Governing Council Calibration — Appendix"
shortcode: "SWEEPS.A"
status: "active"
keywords:
    - Wealth Delta Tax
    - wealth taxation
    - parameter sweeps
    - parameter sensitivity
    - tax-rate calibration
    - numerical simulation
    - declaration incentives
    - fiscal outcomes
    - sensitivity analysis
    - joint parameter surface
    - N-crossing
    - tolerant zone
    - Sovereign Wealth Fund capitalisation
    - reproducible research
---

### Revision History {.unnumbered .unlisted}

| Revision | Date            | Details                  |
|:--------:|:---------------:|--------------------------|
| 0.01      | 12 August 2026     | First Draft          |
| 1.00      | 15 August 2026  | Published to website |
| 1.01 | 31 August 2026 | Numerical and argumentative update to match confirmed SWEEPS.A canonical tables |

\newpage

# A. Appendix Tables {.appendix}

This appendix is in two parts. Part 1 (this section) describes each table group: what it measures, how its axes are structured, and the key pattern visible in the data. Part 2 contains the tables themselves; it is assembled separately and appended manually.

**Part 1 — Table Descriptions**

This section describes each table group in the appendix. For each rate-function parameter, the VAL.S and RATES.S tables are treated together so that the declaration-incentive and fiscal dimensions of the same lever are visible side by side. Tables with no RATES.S counterpart — the N sweep, $V_0$ sweep, joint surfaces, and figure index — are described individually.

**Metrics and Canonical Parameters**

The metric throughout VAL.S is the C.1 statistic: $(Net(\alpha) - Net(1) / TW(\alpha)$, where $Net(\alpha)$ is total lifetime tax paid net of refunds under declaration ratio $\alpha$, and $TW(\alpha)$ is terminal wealth under $\alpha$. A positive C.1 value means the $\alpha$ strategy results in more net tax paid than honest declaration, relative to terminal wealth; a negative value means less. The $\alpha = 1.0$ row is zero by construction. Understater rows ($\alpha < 1.0$) are positive when the mechanism is working as intended; overstater rows ($\alpha > 1.0$) are positive when the self-limiting correction has activated (overstater pays more than honest), and near-zero or negative at short holding horizons when the advantage is still active.

The metric throughout RATES.S is the set of transition outcomes across 73 historical start years (1947–2019 UK equity return series): SSM coverage ratio, TCM coverage ratio, LRR fill year, SRR fill year, and LRR surplus at fill. The SSM applies the correlated-shock assumption — all taxpayers experience the same return simultaneously — producing the worst-case revenue floor. The TCM applies four persistent heterogeneous growth tier differentials, producing the persistent-heterogeneity ceiling. Together they bracket the plausible revenue range.

All VAL.S tables use the canonical parameters $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, $W_{min}$ = £2m, N = 29, $V_0$ = £20m, $g$ = 10.45%, except for the parameter being swept. All RATES.S tables hold the non-swept parameters at the Balanced baseline: $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, $W_{min}$ = £2m.

\newpage

## A.1 RATES.S §1 — $\tau_0$ Sweep

**What the tables show.** A.1 contains six C.1 heatmaps (sub-tables A.1.1–A.1.6) at $\tau_0$ values of 10%, 15%, 20%, 30%, 40%, and 50%. Each sub-table holds $\alpha$ (declaration ratio, rows) against $g$ (growth rate, columns), with all other parameters at canonical values. (RATES.S §1) contains the 73-year distribution summary and 2006 worst-case row for ten $\tau_0$ values swept from 5% to 50%.

**VAL.S key pattern.** The most consequential effect of $\tau_0$ is on the overstater rows ($\alpha \geq 1.5$) at moderate-to-high growth rates. At all tested $\tau_0$ values, the $\alpha = 2.0$ row at $g = 10.4\%$ shows positive C.1 values at $N = 29$: the self-limiting correction is active throughout the sweep. At $\tau_0$ = 10%, the cell reads +1.51%; as $\tau_0$ rises to 30% it reaches +4.54%, and at 50% it reaches +7.97%. The correction intensifies as $\tau_0$ rises, consistent with the joint surface showing the N-crossing arriving earlier at higher floor rates. Understater rows ($\alpha < 1.0$) also intensify monotonically with $\tau_0$: higher $\tau_0$ raises the floor from which the understater's deferred penalty compounds, producing larger positive C.1 values throughout. At high $\tau_0$ and negative or low growth rates, understater rows in the leftmost columns turn negative — reflecting the rate compression at the floor producing over-correction relative to honest declaration in loss scenarios.

**RATES.S key pattern.** $\tau_0$ dominates the fiscal outcome hierarchy. Median TCM coverage rises from 26.8% at $\tau_0$ = 5% to 64.4% at $\tau_0$ = 50% — a 37.6pp range driven by a single parameter. The median LRR fill year falls from 22 years at $\tau_0$ = 5% to 9 years at $\tau_0$ = 50%. The SRR fill year is invariant at 3 across the full sweep, confirming that the refund reserve capitalises quickly regardless of floor rate. In the 2006 worst-case scenario, LRR fill ranges from 39 years at $\tau_0$ = 5% to 20 years at $\tau_0$ = 50%; the SRR breach flag first appears at $\tau_0$ = 25%. At $\tau_0$ = 20% the 2006 LRR surplus is £1,999b, dropping to £973b at $\tau_0$ = 25% — a compression that reflects the capitalisation window closing into a lower-return portion of the 2006 sequence without substantially advancing fill timing.

**Cross-dataset reading.** The two datasets are broadly aligned on $\tau_0$: higher floor rates accelerate both fiscal capitalisation and the self-limiting correction for overstaters. The residual calibration question is about pace and entry burden — higher $\tau_0$ compresses both timelines and raises the cost to taxpayers throughout the distribution. There is no setting where the fiscal and mechanism-integrity dimensions pull in opposite directions; rather, both dimensions favour higher $\tau_0$ while the cooperative-entry rationale favours lower. That is the trade-off the Council faces.

\newpage

## A.2 RATES.S §2 — $\tau_m$ Sweep

**What the tables show.** A.2 contains four C.1 heatmaps (sub-tables A.2.1–A.2.4) at $\tau_m$ values of 50%, 60%, 70% (canonical), and 80%. (RATES.S §2) contains the 73-year distribution summary and 2006 worst-case row for eleven $\tau_m$ values swept from 50% to 100%.

**VAL.S key pattern.** $\tau_m$ has a concentrated effect on the extreme understater rows ($\alpha = 0.1$, $\alpha = 0.2$) at high growth rates, and near-zero effect on everything else. At $g = 20.4\%$, the $\alpha = 0.1$ penalty rises from 11.86% at $\tau_m$ = 50% to 34.54% at $\tau_m$ = 80%; at the highest tested growth rate ($g = 25.4\%$) the corresponding values are 9.89% and 62.50% — a pronounced amplification of the plateau ceiling at very high growth. The $\alpha = 0.8$ row (mild understatement) is barely affected across the full $\tau_m$ range at any growth rate, confirming that the ceiling rate operates specifically at the egregious tail. Overstater rows ($\alpha \geq 1.2$) show almost no response to $\tau_m$ changes, and the tolerant zone boundaries are stable across all four panels. The N-crossing threshold for $\alpha = 2.0$ shifts by approximately 4 years across the full $\tau_m$ sweep from 50% to 80%, confirming that $\tau_m$ has substantially less leverage on overstater self-correction timing than $\tau_0$.

**RATES.S key pattern.** $\tau_m$ is fiscally inert across the full sweep. SSM and TCM coverage ratios, LRR fill year, SRR fill year, and LRR surplus are essentially unchanged from $\tau_m$ = 50% to $\tau_m$ = 100% — coverage moves by less than 0.1pp and the LRR fill year does not move in the distribution medians. The 2006 LRR surplus rises from £471b at $\tau_m$ = 50% to £494b at $\tau_m$ = 100%, a 5% change negligible relative to the surplus magnitude. This reflects canonical $k$ placing all modelled wealth brackets far below the logistic midpoint during the capitalisation window; no bracket approaches wealth levels where $\tau_m$ constrains the effective rate.

**Cross-dataset reading.** $\tau_m$ is the one rate parameter where the two datasets give non-conflicting guidance. On the declaration side it is the egregious-understater deterrence lever, with a clean, monotonic effect concentrated entirely at the extreme tail. On the fiscal side it is inert for the current modelled population. A Council adjusting $\tau_m$ is setting tail deterrence strength at essentially zero fiscal cost or benefit — the clearest instance of parameter separability in the sweep results.

\newpage

## A.3 RATES.S §3 — $k$ Sweep

**What the tables show.** A.3 contains nine C.1 heatmaps (sub-tables A.3.1–A.3.9) at $k$ values of 0.0001, 0.0002, 0.0005, 0.001 (canonical), 0.002, 0.005, 0.01, 0.05, and 0.1 — log-spaced across three orders of magnitude. (RATES.S §3) contains the 73-year distribution summary and 2006 worst-case row for the same nine $k$ values.

**VAL.S key pattern.** $k$ is the primary lever for the width and depth of the declaration incentive landscape. At $k$ = 0.0001 the heatmap is nearly flat: interior cells are close to zero throughout, and even the largest understater penalty at $g = 25.4\%$ and $\alpha = 0.1$ is only 3.28%. As $k$ rises, the tails intensify first. By $k$ = 0.005 the $\alpha = 0.1$ penalty at $g = 25.4\%$ has reached 19.16%, and the overstater at $\alpha = 2.0$ and $g = 10.4\%$ shows +8.50% (correction fully active at $N = 29$ and intensifying). At $k$ = 0.05 and $k$ = 0.1 the $\alpha = 0.1$ row reaches C.1 values above 40% at moderate growth rates, and overstater rows show strongly positive C.1 values across almost all growth rates — the rate curve is steep enough that the correction operates throughout the distribution rather than only at extreme wealth. The $k$ × $V_0$ joint surface (A.8) shows that this intensification is wealth-dependent: near-threshold taxpayers at $V_0$ = £20m are substantially less affected by $k$ changes than wealthy taxpayers at $V_0$ = £500m, where the rate curve's slope is encountered.

**RATES.S key pattern.** $k$ has limited fiscal consequence within the policy-relevant range. From $k$ = 0.0001 to $k$ = 0.01, median TCM coverage moves from 40.1% to 40.7% — a 0.6pp shift across two orders of magnitude. LRR fill year medians are stable at 13 years throughout this range. Success remains 100% across all nine tested $k$ values; the prior finding of reduced success at $k$ = 0.05 (96%) and $k$ = 0.1 (90%) was an artefact of the since-corrected budget_growth = 4.51%. The 2006 LRR fill year falls from 29 years at $k$ = 0.0001 to 26 years at $k$ = 0.1, and an SRR breach flag appears from $k$ = 0.005 onward in the 2006 scenario.

**Cross-dataset reading.** k's mechanism-integrity effects are substantial within the policy-relevant range, while its fiscal effects are modest until $k$ reaches values that begin to compromise the 100% success rate. Within the canonical neighbourhood the parameter is doing largely separable work on the two dimensions: a Council raising $k$ to sharpen the tails is not simultaneously making a fiscal bet. The exception is at the upper extreme (k ≥ 0.05), where fiscal reliability begins to deteriorate — but that range lies well above canonical values.

\newpage

## A.4 RATES.S §4 — $W_{min}$ Sweep

**What the tables show.** A.8 contains six C.1 heatmaps (sub-tables A.8.1–A.8.6) at $W_{min}$ values of £0m, £1m, £2m (canonical), £5m, £10m, and £50m, plus a summary N-crossing threshold table (A.8.5) comparing crossing times across five $W_{min}$ values for $\alpha \in \{1.5, 1.8, 2.0\}$. (RATES.S §4) contains the 73-year distribution summary and 2006 worst-case row for nine $W_{min}$ values from £0.1m to £10m.

**VAL.S key pattern.** $W_{min}$ has near-zero leverage on the C.1 landscape for a taxpayer with $V_0$ = £20m across most of the sweep range. Sub-tables A.8.1 through A.8.5 ($W_{min}$ = £0m to £10m) are nearly identical — C.1 values differ only in the second decimal place, and the N-crossing thresholds in the summary table (B.8.5) are stable at approximately 20.8 years for $\alpha = 1.5$, 20.0 years for $\alpha = 1.8$, and 19.5 years for $\alpha = 2.0$ across all five values. The mechanism does the same thing to the same taxpayer regardless of where the threshold sits, because $V_0$ = £20m is already well above any of these $W_{min}$ values and the rate curve's shape above $W_{min}$ is unchanged. The exception is A.8.6 ($W_{min}$ = £50m), where the taxpayer at $V_0$ = £20m pays nothing under negative-growth scenarios (C.1 = 0% in the left columns), because $V_0$ falls below $W_{min}$. Within the in-scope cells at $W_{min}$ = £50m, understater penalties at high growth are amplified and the N-crossing pattern differs, reflecting the different position on the logistic curve when the taxpayer enters at the top of the logistic function's near-flat region.

**RATES.S key pattern.** $W_{min}$ is the second fiscal lever after $\tau_0$. Median TCM coverage falls from 45.1% at $W_{min}$ = £0.1m to approximately 33% at $W_{min}$ = £7.5m, with a slight recovery to 34.3% at $W_{min}$ = £10m. The partial recovery reflects concentration of the remaining taxable population in upper brackets with high per-taxpayer revenue, combined with a later capitalisation window that shifts the denominator. Median LRR fill year rises from 10 years at $W_{min}$ = £0.1m to 22 years at $W_{min}$ = £10m — the single largest horizon range of any parameter sweep. The 2006 LRR fill year rises from 25 years at $W_{min}$ = £0.1m to 38 years at $W_{min}$ = £10m; the SRR breach flag does not appear in the 2006 scenario at any $W_{min}$ value in this sweep. LRR surplus at fill is very large at high $W_{min}$ values (£2,710b at $W_{min}$ = £10m, 2006), reflecting concentrated revenue landing in a capitalisation window that opens later in the return sequence.

**Cross-dataset reading.** $W_{min}$ is the scope lever. It has the largest effect on LRR fill speed of any parameter in the RATES.S sweep, and almost no effect on the C.1 incentive landscape for taxpayers already comfortably above the threshold. The two datasets are not in tension here: a Council moving $W_{min}$ is making a decision about how broadly to draw the taxable population and how quickly to fill the LRR, without materially altering what the mechanism does to those it covers.

\newpage

## A.5 VAL.S §1 — N Sweep

**What the tables show.** A.4 contains four per-taxpayer summary tables (A.4.1–A.4.4) at holding periods N = 10, 20, 34 (canonical), and 50 years, each reporting C.1, terminal wealth, net tax, and effective rate at $g = 10.45\%$ for the full $\alpha$ range. A.4.5 is a summary table of N-crossing thresholds for $\alpha \in \{1.5, 1.8, 2.0\}$ at canonical parameters.

**Key pattern.** The N sweep isolates the temporal dimension of the declaration incentive. At N = 10, the overstater advantage is active: $\alpha = 2.0$ shows C.1 = −3.35%, meaning the aggressive overstater pays less net tax than honest declaration. At N = 20 the advantage has compressed substantially: $\alpha = 2.0$ shows +0.11% — the self-limiting correction has already activated. At N = 29 (canonical) the correction has deepened: $\alpha = 2.0$ shows +2.21%, $\alpha = 1.8$ shows +1.58%, and $\alpha = 1.5$ shows +0.79%. All three overstater levels are paying more than honest declaration at the canonical horizon. At N = 50, the correction is fully developed throughout: understater penalties are very large ($\alpha = 0.1$ at 12.57%), and the aggressive overstater at $\alpha = 2.0$ shows C.1 = 10.50% — the correction has imposed a substantial cost above honest declaration at long horizons. The N-crossing summary (B.4.5) places the $\alpha = 1.5$ threshold at N = 20.8, $\alpha = 1.8$ at N = 20.0, and $\alpha = 2.0$ at N = 19.5 at canonical parameters; all three cross well within realistic holding horizons.

\newpage

## A.6 VAL.S §2 — $V_0$ Sweep

**What the tables show.** A.5 contains seven per-taxpayer summary tables (A.5.1–A.5.7) at entry wealth $V_0$ = £5m, £20m (canonical), £100m, £500m, £1,000m, £5,000m, and £10,000m, each at $g = 10.45\%$ and $N = 29$ for the full $\alpha$ range.

**Key pattern.** The $V_0$ sweep shows that the C.1 incentive structure is not uniform across the wealth distribution. At $V_0$ = £5m, all declaration strategies produce C.1 values within a narrow band: the understater penalty reaches 1.85% ($\alpha = 0.1$) and overstater rows show small positive values ($\alpha = 1.8$: +0.76%) — the correction is active but modest at near-threshold wealth. At $V_0$ = £100m the pattern has sharpened: the understater penalty at $\alpha = 0.1$ reaches 9.66% and the overstater correction at $\alpha = 2.0$ reaches +8.50%. At $V_0$ = £500m the landscape is dramatically steeper: understater penalties reach approximately 32pp ($\alpha = 0.1$) and overstater corrections reach approximately 10pp ($\alpha = 2.0$). Above $V_0$ = £1,000m the C.1 values in the understater rows compress toward a plateau, reflecting the rate function ceiling — effective rates are approaching $\tau_m$ across the full holding period and the marginal deterrent from additional wealth has saturated. The effective rate column confirms the intensification with wealth: at $V_0$ = £5,000m and $\alpha = 1.0$ (honest), the lifetime effective rate is 57.94%, compared to 15.54% at $V_0$ = £20m. The $V_0$ sweep is the primary caution against treating single-reference-taxpayer results as population-representative: mechanism intensity increases substantially with entry wealth.

\newpage

## A.7 VAL.S §3 — $\tau_0$ × N Joint Surface

**What the table shows.** A.6 is a two-dimensional grid with $\tau_0$ on the column axis (5% to 41% in 3pp steps) and N sweep ceiling on the row axis (10 to 70 years in 5-year steps). Each cell contains the first N at which $Net(\alpha = 2.0)$ exceeds $Net(\alpha = 1.0)$ at $g = 10.4\%$ — the N-crossing threshold for aggressive overstatement — or "—" where no crossing is found within the sweep ceiling.

**Key pattern.** The table makes the $\tau_0$ effect on N-crossing precise. At $\tau_0$ = 5–8%, the crossing arrives at N = 21 and does not move regardless of how high the sweep ceiling is extended — the correction activates early and robustly at low floor rates. As $\tau_0$ rises, the crossing threshold moves earlier: $\tau_0$ = 14% gives N = 20, $\tau_0$ = 17–20% gives N = 19. By $\tau_0$ = 35–41% the crossing has moved to N = 16–17. Crossings are present throughout the full tested range — no column shows "—" cells regardless of how far N is extended. The table shows that raising $\tau_0$ is simultaneously a decision to bring the self-correction earlier: the transition is monotone from N = 21 at the floor to N = 16 at the ceiling of the tested range.

\newpage

## A.8 VAL.S §5 — $k$ × $V_0$ Joint Surface

**What the table shows.** A.7 is a two-dimensional grid with $V_0$ on the column axis (£5m to £500m) and $k$ on the row axis (0.0001 to 0.1, log-spaced). Each cell contains C.1 for $\alpha = 1.8$ at $g = 10.4\%$, $N = 29$ — the correction penalty for aggressive overstatement at the interaction of steepness and entry wealth. Positive values indicate the correction is active (overstater pays more than honest declaration); values near zero indicate the correction is negligible at this horizon.

**Key pattern.** The correction (positive C.1) is present across the full $k$ × $V_0$ surface at N = 29: every tested combination shows the overstater paying more than honest declaration at this holding horizon. Values are smallest in the upper-left (low k, low $V_0$) region, where the canonical cell at $k$ = 0.001, $V_0$ = £20m reads +1.58pp. Values rise toward the lower-right (high k, high $V_0$) as steepness concentrates bracket effects on wealthier positions. The surface shows non-monotonicity at intermediate $k$ values for some $V_0$ levels, reflecting the interaction between where on the logistic curve the taxpayer sits and the temporal profile of the self-limiting correction. The absence of negative cells (overstater advantage) across the surface confirms that at N = 29, the correction is active for $\alpha$ = 1.8 at all tested steepness and wealth combinations.

\newpage

## B. VAL.S Figure Index

Section B lists the twenty figures generated by the VAL.S output scripts, each identified by filename, title, axis specifications, fixed parameter values, and a cross-reference to the corresponding VAL.A section. The figures visualise the same data as tables A.1–A.8 in heatmap, line-chart, and joint-surface formats that make distributional patterns and boundary regions visible at a glance.

The VAL.A cross-reference column directs the reader to the canonical-parameter treatment of the same metric in the mathematical companion paper. Where a figure overlays VAL.A reference values (e.g. SS2.1c and SS3.1c annotate the tolerant-zone boundaries from (VAL.A §A.6) as reference lines), the underlying simulation engine is shared and the canonical cell in the sweep figure should reproduce the VAL.A value to within floating-point rounding.

Figures are grouped by the parameter swept: SS2.x for rate parameters ($\tau_0$, $\tau_m$, k, $W_{min}$), SS3.x for horizon and wealth parameters (N, $V_0$), SS4.x for joint surfaces. Within each group, the suffix letter distinguishes the visualisation type: (a) heatmap grids, (b) line charts of a derived quantity across the swept parameter, (c) tolerant-zone or bracket-penalty overlays. The calibration summary figure (SS4.3) collects all three mechanism-integrity properties — tolerant-zone width, N-crossing threshold for $\alpha = 1.8$, and understater plateau ceiling at $\alpha = 0.1$ — across all parameter variants in a single three-panel chart, providing the unified cross-parameter view that the individual sweep figures distribute across eight table groups.

**VAL.S — Appendix Tables**

**Generated:** 2026-08-30
**Model:** Python v1.0 standalone via wdt_core.py 
    -  Canonical: $\tau_0$=15%, $\tau_m$=70%, k=0.001, $W_{min}$=£2m, N=29, $V_0$=£20m, $g$=10.45%

**Metric (all tables unless stated):** C.1 = (Net($\alpha$) − Net(1) / TW($\alpha$).  Positive = $\alpha$ pays more net tax than honest declaration.  $\alpha$ = 1.0 row is zero by construction.

**Consistency check:** simulation engine determinism — PASSED.
**Note on VAL.A alignment:** the live TOML canonical values differ slightly from the (VAL.A §C.1) printed snapshot (generated at a different TOML state during v2.4 unification). VAL.S uses the live TOML as its reference throughout; any figures that overlay VAL.A values should note this snapshot offset.

---

## B.1  $\tau_0$ Sweep — C.1 metric across $\alpha$ and $g$

**Metric:** (Net($\alpha$) − Net(1) / TW($\alpha$) 
    -  $\tau_m$ = 70%, $k$ = 0.001, N = 29, $V_0$ = £20m.  $\alpha$ = 1.0 row is zero by construction.

### B.1.1  $\tau_0$ = 10%

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 8.88% | 7.92% | 1.52% | 0.87% | 0.94% | 1.17% | 2.73% | 7.47% | 34.85% | 31.33% |
| **0.2** | 7.76% | 6.97% | 1.31% | 0.70% | 0.72% | 0.89% | 2.09% | 5.75% | 25.33% | 20.92% |
| **0.5** | 4.54% | 4.23% | 0.73% | 0.31% | 0.23% | 0.26% | 0.69% | 2.05% | 8.03% | 5.07% |
| **0.8** | 1.50% | 1.64% | 0.26% | 0.07% | 0.01% | -0.01% | 0.04% | 0.27% | 1.18% | 0.47% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.03% | -0.22% | -0.01% | 0.10% | 0.15% | 0.26% | 0.38% | 0.54% | 0.57% |
| **1.5** | 0.00% | -0.99% | -0.49% | 0.09% | 0.45% | 0.62% | 1.16% | 2.02% | 3.44% | 2.50% |
| **1.8** | 0.00% | -0.96% | -0.67% | 0.32% | 1.02% | 1.38% | 2.64% | 4.73% | 7.88% | 5.11% |
| **2.0** | 0.00% | -0.94% | -0.75% | 0.54% | 1.51% | 2.03% | 3.93% | 7.02% | 11.36% | 7.04% |

### B.1.2  $\tau_0$ = 15%  *(canonical)*

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.25% | 11.80% | 1.91% | 0.73% | 0.58% | 0.74% | 2.15% | 6.22% | 25.65% | 30.18% |
| **0.2** | 11.52% | 10.34% | 1.63% | 0.55% | 0.36% | 0.47% | 1.51% | 4.58% | 18.39% | 19.84% |
| **0.5** | 6.64% | 6.18% | 0.90% | 0.18% | -0.04% | -0.05% | 0.24% | 1.29% | 5.38% | 4.33% |
| **0.8** | 2.16% | 2.37% | 0.31% | 0.01% | -0.12% | -0.15% | -0.15% | -0.02% | 0.55% | 0.14% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.39% | -0.26% | 0.06% | 0.23% | 0.30% | 0.45% | 0.61% | 0.83% | 0.90% |
| **1.5** | 0.00% | -1.32% | -0.56% | 0.29% | 0.79% | 1.01% | 1.63% | 2.45% | 3.76% | 3.31% |
| **1.8** | 0.00% | -1.25% | -0.75% | 0.66% | 1.58% | 2.00% | 3.33% | 5.18% | 7.96% | 6.33% |
| **2.0** | 0.00% | -1.21% | -0.83% | 0.97% | 2.21% | 2.81% | 4.72% | 7.39% | 11.19% | 8.50% |

### B.1.3  $\tau_0$ = 20%

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 17.58% | 15.64% | 2.08% | 0.27% | -0.19% | -0.14% | 0.95% | 4.20% | 18.20% | 27.08% |
| **0.2** | 15.21% | 13.62% | 1.77% | 0.14% | -0.33% | -0.32% | 0.43% | 2.84% | 12.74% | 17.45% |
| **0.5** | 8.64% | 8.04% | 0.95% | -0.09% | -0.48% | -0.55% | -0.42% | 0.31% | 3.16% | 3.23% |
| **0.8** | 2.78% | 3.05% | 0.33% | -0.10% | -0.29% | -0.34% | -0.41% | -0.35% | -0.01% | -0.23% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.69% | -0.26% | 0.17% | 0.40% | 0.49% | 0.68% | 0.86% | 1.11% | 1.23% |
| **1.5** | 0.00% | -1.57% | -0.55% | 0.56% | 1.20% | 1.46% | 2.14% | 2.93% | 4.15% | 4.06% |
| **1.8** | 0.00% | -1.46% | -0.73% | 1.07% | 2.19% | 2.67% | 4.04% | 5.71% | 8.23% | 7.43% |
| **2.0** | 0.00% | -1.38% | -0.79% | 1.48% | 2.95% | 3.60% | 5.51% | 7.88% | 11.30% | 9.79% |

### B.1.4  $\tau_0$ = 30%

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 26.09% | 23.15% | 1.91% | -1.42% | -2.70% | -2.97% | -2.74% | -0.96% | 6.37% | 16.16% |
| **0.2** | 22.35% | 19.99% | 1.59% | -1.33% | -2.51% | -2.77% | -2.73% | -1.51% | 3.62% | 9.46% |
| **0.5** | 12.36% | 11.50% | 0.81% | -0.95% | -1.74% | -1.96% | -2.19% | -1.96% | -0.63% | 0.14% |
| **0.8** | 3.89% | 4.26% | 0.26% | -0.42% | -0.75% | -0.86% | -1.04% | -1.10% | -1.03% | -1.12% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -2.10% | -0.20% | 0.47% | 0.81% | 0.94% | 1.20% | 1.42% | 1.71% | 1.90% |
| **1.5** | 0.00% | -1.89% | -0.38% | 1.24% | 2.13% | 2.47% | 3.26% | 4.02% | 5.10% | 5.46% |
| **1.8** | 0.00% | -1.68% | -0.46% | 2.08% | 3.55% | 4.13% | 5.56% | 7.01% | 9.12% | 9.35% |
| **2.0** | 0.00% | -1.54% | -0.45% | 2.68% | 4.54% | 5.29% | 7.19% | 9.18% | 12.00% | 11.98% |

### B.1.5  $\tau_0$ = 40%

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 34.42% | 30.49% | 1.13% | -3.98% | -6.29% | -6.95% | -7.70% | -7.17% | -3.63% | 2.95% |
| **0.2** | 29.22% | 26.08% | 0.91% | -3.51% | -5.54% | -6.14% | -6.90% | -6.65% | -4.26% | -0.22% |
| **0.5** | 15.77% | 14.65% | 0.42% | -2.15% | -3.38% | -3.77% | -4.39% | -4.56% | -4.12% | -3.55% |
| **0.8** | 4.85% | 5.32% | 0.12% | -0.84% | -1.33% | -1.49% | -1.78% | -1.94% | -2.03% | -2.12% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -2.37% | -0.06% | 0.83% | 1.30% | 1.46% | 1.80% | 2.05% | 2.34% | 2.56% |
| **1.5** | 0.00% | -2.05% | -0.07% | 2.04% | 3.19% | 3.61% | 4.51% | 5.25% | 6.22% | 6.76% |
| **1.8** | 0.00% | -1.73% | 0.00% | 3.23% | 5.03% | 5.71% | 7.22% | 8.55% | 10.33% | 11.01% |
| **2.0** | 0.00% | -1.53% | 0.09% | 4.01% | 6.23% | 7.08% | 9.03% | 10.78% | 13.11% | 13.78% |

### B.1.6  $\tau_0$ = 50%

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 42.58% | 37.63% | -0.15% | -7.28% | -10.79% | -11.91% | -13.73% | -14.31% | -13.22% | -9.97% |
| **0.2** | 35.81% | 31.92% | -0.18% | -6.27% | -9.29% | -10.26% | -11.89% | -12.49% | -11.91% | -9.94% |
| **0.5** | 18.88% | 17.53% | -0.18% | -3.59% | -5.32% | -5.90% | -6.93% | -7.45% | -7.60% | -7.44% |
| **0.8** | 5.71% | 6.26% | -0.09% | -1.33% | -1.98% | -2.20% | -2.61% | -2.86% | -3.05% | -3.19% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -2.53% | 0.11% | 1.23% | 1.82% | 2.03% | 2.44% | 2.73% | 3.03% | 3.25% |
| **1.5** | 0.00% | -2.10% | 0.32% | 2.91% | 4.31% | 4.81% | 5.84% | 6.60% | 7.47% | 8.02% |
| **1.8** | 0.00% | -1.68% | 0.55% | 4.43% | 6.57% | 7.34% | 8.98% | 10.25% | 11.74% | 12.54% |
| **2.0** | 0.00% | -1.40% | 0.72% | 5.38% | 7.97% | 8.92% | 10.95% | 12.57% | 14.48% | 15.37% |

## B.2  $\tau_m$ Sweep — C.1 metric across $\alpha$ and $g$

**Metric:** (Net($\alpha$) − Net(1) / TW($\alpha$) 
    -  $\tau_0$ = 15%, $k$ = 0.001, N = 29, $V_0$ = £20m.

### B.2.1  $\tau_m$ = 50%

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.25% | 11.78% | 1.86% | 0.63% | 0.39% | 0.49% | 1.49% | 4.13% | 11.86% | 9.89% |
| **0.2** | 11.52% | 10.32% | 1.59% | 0.48% | 0.22% | 0.27% | 0.99% | 2.98% | 8.52% | 6.19% |
| **0.5** | 6.64% | 6.17% | 0.88% | 0.15% | -0.09% | -0.12% | 0.05% | 0.70% | 2.28% | 0.65% |
| **0.8** | 2.16% | 2.37% | 0.31% | 0.01% | -0.12% | -0.16% | -0.18% | -0.12% | 0.05% | -0.38% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.39% | -0.26% | 0.06% | 0.22% | 0.28% | 0.42% | 0.55% | 0.72% | 0.78% |
| **1.5** | 0.00% | -1.32% | -0.57% | 0.25% | 0.73% | 0.92% | 1.45% | 2.05% | 2.73% | 2.34% |
| **1.8** | 0.00% | -1.25% | -0.79% | 0.57% | 1.42% | 1.80% | 2.88% | 4.17% | 5.42% | 4.09% |
| **2.0** | 0.00% | -1.21% | -0.89% | 0.84% | 1.97% | 2.49% | 4.02% | 5.86% | 7.43% | 5.29% |

### B.2.2  $\tau_m$ = 60%

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.25% | 11.80% | 1.89% | 0.69% | 0.50% | 0.63% | 1.86% | 5.25% | 18.11% | 16.77% |
| **0.2** | 11.52% | 10.33% | 1.61% | 0.52% | 0.30% | 0.38% | 1.28% | 3.84% | 13.07% | 11.03% |
| **0.5** | 6.64% | 6.18% | 0.89% | 0.17% | -0.06% | -0.08% | 0.16% | 1.01% | 3.75% | 2.02% |
| **0.8** | 2.16% | 2.37% | 0.31% | 0.01% | -0.12% | -0.15% | -0.17% | -0.07% | 0.28% | -0.19% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.39% | -0.26% | 0.06% | 0.23% | 0.29% | 0.44% | 0.59% | 0.78% | 0.86% |
| **1.5** | 0.00% | -1.32% | -0.56% | 0.27% | 0.77% | 0.97% | 1.55% | 2.27% | 3.26% | 2.79% |
| **1.8** | 0.00% | -1.25% | -0.77% | 0.62% | 1.51% | 1.92% | 3.13% | 4.72% | 6.71% | 5.09% |
| **2.0** | 0.00% | -1.21% | -0.86% | 0.92% | 2.11% | 2.67% | 4.42% | 6.69% | 9.33% | 6.70% |

### B.2.3  $\tau_m$ = 70%  *(canonical)*

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.25% | 11.80% | 1.91% | 0.73% | 0.58% | 0.74% | 2.15% | 6.22% | 25.65% | 30.18% |
| **0.2** | 11.52% | 10.34% | 1.63% | 0.55% | 0.36% | 0.47% | 1.51% | 4.58% | 18.39% | 19.84% |
| **0.5** | 6.64% | 6.18% | 0.90% | 0.18% | -0.04% | -0.05% | 0.24% | 1.29% | 5.38% | 4.33% |
| **0.8** | 2.16% | 2.37% | 0.31% | 0.01% | -0.12% | -0.15% | -0.15% | -0.02% | 0.55% | 0.14% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.39% | -0.26% | 0.06% | 0.23% | 0.30% | 0.45% | 0.61% | 0.83% | 0.90% |
| **1.5** | 0.00% | -1.32% | -0.56% | 0.29% | 0.79% | 1.01% | 1.63% | 2.45% | 3.76% | 3.31% |
| **1.8** | 0.00% | -1.25% | -0.75% | 0.66% | 1.58% | 2.00% | 3.33% | 5.18% | 7.96% | 6.33% |
| **2.0** | 0.00% | -1.21% | -0.83% | 0.97% | 2.21% | 2.81% | 4.72% | 7.39% | 11.19% | 8.50% |

### B.2.4  $\tau_m$ = 80%

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.25% | 11.81% | 1.92% | 0.76% | 0.64% | 0.83% | 2.39% | 7.05% | 34.54% | 62.50% |
| **0.2** | 11.52% | 10.34% | 1.64% | 0.58% | 0.41% | 0.53% | 1.69% | 5.22% | 24.47% | 39.04% |
| **0.5** | 6.64% | 6.18% | 0.90% | 0.19% | -0.02% | -0.03% | 0.31% | 1.52% | 7.14% | 8.58% |
| **0.8** | 2.16% | 2.37% | 0.31% | 0.01% | -0.11% | -0.14% | -0.14% | 0.02% | 0.83% | 0.76% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.39% | -0.26% | 0.07% | 0.24% | 0.30% | 0.46% | 0.63% | 0.86% | 0.92% |
| **1.5** | 0.00% | -1.32% | -0.55% | 0.30% | 0.81% | 1.04% | 1.70% | 2.60% | 4.23% | 3.97% |
| **1.8** | 0.00% | -1.25% | -0.74% | 0.68% | 1.63% | 2.07% | 3.49% | 5.56% | 9.15% | 8.05% |
| **2.0** | 0.00% | -1.21% | -0.81% | 1.01% | 2.29% | 2.92% | 4.97% | 7.97% | 12.97% | 11.05% |

## B.3  $k$ Sweep — C.1 metric across $\alpha$ and $g$

**Metric:** (Net($\alpha$) − Net(1) / TW($\alpha$) 
    -  $\tau_0$ = 15%, $\tau_m$ = 70%, N = 29, $V_0$ = £20m.

### B.3.1  $k$ = 0.0001

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.22% | 11.63% | 1.54% | 0.04% | -0.60% | -0.78% | -1.03% | -1.00% | -0.32% | 3.28% |
| **0.2** | 11.50% | 10.19% | 1.34% | 0.03% | -0.54% | -0.70% | -0.93% | -0.93% | -0.41% | 2.40% |
| **0.5** | 6.62% | 6.10% | 0.80% | 0.00% | -0.35% | -0.45% | -0.61% | -0.65% | -0.48% | 0.60% |
| **0.8** | 2.16% | 2.34% | 0.30% | -0.00% | -0.14% | -0.19% | -0.26% | -0.29% | -0.28% | -0.08% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.38% | -0.29% | 0.01% | 0.15% | 0.19% | 0.27% | 0.32% | 0.38% | 0.46% |
| **1.5** | 0.00% | -1.31% | -0.68% | 0.04% | 0.38% | 0.49% | 0.70% | 0.85% | 1.12% | 1.78% |
| **1.8** | 0.00% | -1.25% | -1.04% | 0.08% | 0.61% | 0.79% | 1.15% | 1.45% | 2.05% | 3.75% |
| **2.0** | 0.00% | -1.20% | -1.27% | 0.11% | 0.77% | 1.00% | 1.46% | 1.87% | 2.77% | 5.36% |

### B.3.2  $k$ = 0.0002

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.23% | 11.65% | 1.57% | 0.11% | -0.48% | -0.64% | -0.76% | -0.47% | 1.33% | 11.75% |
| **0.2** | 11.50% | 10.21% | 1.37% | 0.08% | -0.45% | -0.59% | -0.72% | -0.52% | 0.87% | 8.78% |
| **0.5** | 6.63% | 6.11% | 0.81% | 0.02% | -0.32% | -0.41% | -0.54% | -0.50% | -0.01% | 2.84% |
| **0.8** | 2.16% | 2.35% | 0.30% | -0.00% | -0.14% | -0.18% | -0.25% | -0.27% | -0.20% | 0.29% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.38% | -0.28% | 0.02% | 0.16% | 0.20% | 0.29% | 0.35% | 0.44% | 0.58% |
| **1.5** | 0.00% | -1.31% | -0.67% | 0.07% | 0.42% | 0.54% | 0.79% | 1.02% | 1.52% | 2.70% |
| **1.8** | 0.00% | -1.25% | -1.01% | 0.14% | 0.71% | 0.92% | 1.37% | 1.84% | 3.03% | 5.94% |
| **2.0** | 0.00% | -1.20% | -1.22% | 0.20% | 0.92% | 1.19% | 1.79% | 2.47% | 4.25% | 8.56% |

### B.3.3  $k$ = 0.0005

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.24% | 11.71% | 1.70% | 0.33% | -0.11% | -0.16% | 0.18% | 1.52% | 8.80% | 36.09% |
| **0.2** | 11.51% | 10.25% | 1.47% | 0.25% | -0.17% | -0.23% | 0.00% | 1.02% | 6.54% | 25.24% |
| **0.5** | 6.63% | 6.14% | 0.84% | 0.08% | -0.22% | -0.29% | -0.29% | 0.05% | 1.99% | 7.04% |
| **0.8** | 2.16% | 2.36% | 0.31% | 0.00% | -0.13% | -0.17% | -0.22% | -0.20% | 0.11% | 0.78% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.39% | -0.27% | 0.03% | 0.19% | 0.24% | 0.35% | 0.45% | 0.63% | 0.76% |
| **1.5** | 0.00% | -1.32% | -0.63% | 0.15% | 0.55% | 0.71% | 1.09% | 1.56% | 2.67% | 3.65% |
| **1.8** | 0.00% | -1.25% | -0.92% | 0.33% | 1.02% | 1.31% | 2.08% | 3.12% | 5.73% | 7.73% |
| **2.0** | 0.00% | -1.20% | -1.08% | 0.48% | 1.39% | 1.77% | 2.86% | 4.39% | 8.19% | 10.82% |

### B.3.4  $k$ = 0.001  *(canonical)*

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.25% | 11.80% | 1.91% | 0.73% | 0.58% | 0.74% | 2.15% | 6.22% | 25.65% | 30.18% |
| **0.2** | 11.52% | 10.34% | 1.63% | 0.55% | 0.36% | 0.47% | 1.51% | 4.58% | 18.39% | 19.84% |
| **0.5** | 6.64% | 6.18% | 0.90% | 0.18% | -0.04% | -0.05% | 0.24% | 1.29% | 5.38% | 4.33% |
| **0.8** | 2.16% | 2.37% | 0.31% | 0.01% | -0.12% | -0.15% | -0.15% | -0.02% | 0.55% | 0.14% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.39% | -0.26% | 0.06% | 0.23% | 0.30% | 0.45% | 0.61% | 0.83% | 0.90% |
| **1.5** | 0.00% | -1.32% | -0.56% | 0.29% | 0.79% | 1.01% | 1.63% | 2.45% | 3.76% | 3.31% |
| **1.8** | 0.00% | -1.25% | -0.75% | 0.66% | 1.58% | 2.00% | 3.33% | 5.18% | 7.96% | 6.33% |
| **2.0** | 0.00% | -1.21% | -0.83% | 0.97% | 2.21% | 2.81% | 4.72% | 7.39% | 11.19% | 8.50% |

### B.3.5  $k$ = 0.002

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.28% | 12.00% | 2.35% | 1.61% | 2.25% | 3.03% | 7.67% | 19.51% | 37.11% | 19.33% |
| **0.2** | 11.55% | 10.50% | 1.97% | 1.23% | 1.64% | 2.21% | 5.66% | 14.12% | 24.95% | 11.59% |
| **0.5** | 6.65% | 6.27% | 1.02% | 0.41% | 0.39% | 0.55% | 1.64% | 4.14% | 6.04% | 1.46% |
| **0.8** | 2.17% | 2.40% | 0.33% | 0.03% | -0.07% | -0.08% | 0.03% | 0.34% | 0.42% | -0.40% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.41% | -0.23% | 0.13% | 0.34% | 0.43% | 0.65% | 0.86% | 0.98% | 0.98% |
| **1.5** | 0.00% | -1.33% | -0.41% | 0.59% | 1.30% | 1.65% | 2.67% | 3.71% | 3.93% | 2.98% |
| **1.8** | 0.00% | -1.26% | -0.41% | 1.35% | 2.75% | 3.46% | 5.65% | 7.79% | 7.81% | 5.24% |
| **2.0** | 0.00% | -1.21% | -0.32% | 2.01% | 3.94% | 4.96% | 8.05% | 10.96% | 10.67% | 6.79% |

### B.3.6  $k$ = 0.005

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.38% | 12.59% | 3.93% | 5.15% | 9.68% | 13.56% | 29.39% | 36.63% | 19.91% | 19.16% |
| **0.2** | 11.63% | 11.00% | 3.18% | 3.91% | 7.18% | 9.94% | 20.57% | 24.31% | 12.04% | 10.23% |
| **0.5** | 6.69% | 6.54% | 1.43% | 1.30% | 2.18% | 2.95% | 5.53% | 5.57% | 1.47% | 0.87% |
| **0.8** | 2.18% | 2.49% | 0.37% | 0.12% | 0.13% | 0.19% | 0.42% | 0.26% | -0.46% | -0.52% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.45% | -0.13% | 0.33% | 0.65% | 0.78% | 1.03% | 1.11% | 1.08% | 1.04% |
| **1.5** | 0.00% | -1.36% | 0.07% | 1.57% | 2.78% | 3.31% | 4.30% | 4.19% | 3.27% | 3.06% |
| **1.8** | 0.00% | -1.28% | 0.71% | 3.55% | 5.95% | 7.00% | 8.79% | 8.14% | 5.73% | 5.28% |
| **2.0** | 0.00% | -1.22% | 1.35% | 5.21% | 8.50% | 9.91% | 12.18% | 11.02% | 7.41% | 6.78% |

### B.3.7  $k$ = 0.01

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.54% | 13.62% | 7.40% | 13.89% | 26.24% | 32.45% | 35.04% | 22.02% | 18.21% | 19.22% |
| **0.2** | 11.76% | 11.88% | 5.80% | 10.28% | 18.53% | 22.39% | 22.80% | 13.51% | 9.75% | 9.93% |
| **0.5** | 6.77% | 7.01% | 2.31% | 3.22% | 5.09% | 5.77% | 4.81% | 1.80% | 0.52% | 0.65% |
| **0.8** | 2.20% | 2.65% | 0.47% | 0.31% | 0.38% | 0.38% | 0.05% | -0.47% | -0.66% | -0.61% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.52% | 0.05% | 0.65% | 1.01% | 1.11% | 1.20% | 1.18% | 1.17% | 1.13% |
| **1.5** | 0.00% | -1.41% | 0.94% | 2.99% | 4.19% | 4.47% | 4.24% | 3.60% | 3.36% | 3.28% |
| **1.8** | 0.00% | -1.30% | 2.66% | 6.48% | 8.61% | 9.00% | 8.02% | 6.33% | 5.74% | 5.64% |
| **2.0** | 0.00% | -1.22% | 4.17% | 9.26% | 11.97% | 12.38% | 10.71% | 8.20% | 7.33% | 7.22% |

### B.3.8  $k$ = 0.05

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 14.86% | 24.47% | 39.53% | 27.68% | 17.91% | 16.52% | 16.26% | 16.62% | 16.75% | 16.92% |
| **0.2** | 12.89% | 20.81% | 26.61% | 16.94% | 9.91% | 8.58% | 7.47% | 7.22% | 7.15% | 7.28% |
| **0.5** | 7.37% | 11.47% | 6.64% | 2.45% | 0.02% | -0.53% | -1.14% | -1.36% | -1.48% | -1.45% |
| **0.8** | 2.39% | 4.08% | 0.61% | -0.45% | -0.99% | -1.12% | -1.33% | -1.43% | -1.50% | -1.51% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.96% | 0.74% | 1.25% | 1.50% | 1.60% | 1.79% | 1.92% | 2.01% | 2.05% |
| **1.5** | 0.00% | -1.61% | 3.11% | 3.71% | 4.10% | 4.32% | 4.82% | 5.15% | 5.42% | 5.53% |
| **1.8** | 0.00% | -1.22% | 6.04% | 6.28% | 6.73% | 7.07% | 7.88% | 8.44% | 8.92% | 9.14% |
| **2.0** | 0.00% | -0.94% | 8.01% | 7.91% | 8.41% | 8.82% | 9.85% | 10.57% | 11.19% | 11.49% |

### B.3.9  $k$ = 0.1

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 16.66% | 43.78% | 26.76% | 15.54% | 14.31% | 14.21% | 13.95% | 13.62% | 13.32% | 13.30% |
| **0.2** | 14.41% | 35.74% | 16.28% | 7.59% | 5.57% | 5.07% | 4.19% | 3.66% | 3.27% | 3.20% |
| **0.5** | 8.18% | 17.74% | 2.57% | -1.15% | -2.48% | -2.89% | -3.65% | -4.13% | -4.52% | -4.68% |
| **0.8** | 2.63% | 5.82% | -0.13% | -1.27% | -1.80% | -1.98% | -2.33% | -2.56% | -2.75% | -2.85% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -2.25% | 0.60% | 1.56% | 2.11% | 2.30% | 2.69% | 2.94% | 3.16% | 3.28% |
| **1.5** | 0.00% | -1.64% | 1.63% | 3.93% | 5.29% | 5.78% | 6.75% | 7.38% | 7.96% | 8.28% |
| **1.8** | 0.00% | -1.03% | 2.50% | 6.06% | 8.20% | 8.97% | 10.49% | 11.50% | 12.41% | 12.94% |
| **2.0** | 0.00% | -0.64% | 2.97% | 7.32% | 9.94% | 10.88% | 12.74% | 13.98% | 15.10% | 15.75% |

## B.4  N Sweep — C.1 metric at four holding periods

**Metric:** (Net($\alpha$,N) − Net(1,N) / TW($\alpha$,N) 
    -  $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, $V_0$ = £20m, $g$ = 10.45% throughout.  $\alpha$ = 1.0 row is zero by construction.

### B.4.1  N = 10

| $\alpha$ | C.1 at $g$ = 10.45% | TW (£m) | Net (£m) | Eff rate |
|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 4.26% | 46.11 | 6.87 | 14.90% |
| **0.2** | 3.71% | 46.74 | 6.64 | 14.21% |
| **0.5** | 2.19% | 48.65 | 5.97 | 12.28% |
| **0.8** | 0.83% | 50.56 | 5.33 | 10.54% |
| **1.0** | 0.00% | 51.83 | 4.91 | 9.47% |
| **1.2** | -0.77% | 53.09 | 4.50 | 8.47% |
| **1.5** | -1.83% | 54.99 | 3.90 | 7.10% |
| **1.8** | -2.77% | 56.88 | 3.33 | 5.86% |
| **2.0** | -3.35% | 58.14 | 2.96 | 5.09% |

### B.4.2  N = 20

| $\alpha$ | C.1 at $g$ = 10.45% | TW (£m) | Net (£m) | Eff rate |
|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 1.17% | 109.04 | 17.57 | 16.11% |
| **0.2** | 0.97% | 110.56 | 17.36 | 15.70% |
| **0.5** | 0.47% | 115.10 | 16.83 | 14.62% |
| **0.8** | 0.14% | 119.61 | 16.45 | 13.76% |
| **1.0** | 0.00% | 122.59 | 16.29 | 13.28% |
| **1.2** | -0.08% | 125.56 | 16.18 | 12.89% |
| **1.5** | -0.10% | 129.98 | 16.16 | 12.43% |
| **1.8** | -0.01% | 134.37 | 16.28 | 12.11% |
| **2.0** | 0.11% | 137.28 | 16.44 | 11.98% |

### B.4.3  N = 29  *(canonical)*

| $\alpha$ | C.1 at $g$ = 10.45% | TW (£m) | Net (£m) | Eff rate |
|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 0.58% | 234.30 | 42.32 | 18.06% |
| **0.2** | 0.36% | 237.67 | 41.83 | 17.60% |
| **0.5** | -0.04% | 247.63 | 40.87 | 16.51% |
| **0.8** | -0.12% | 257.37 | 40.68 | 15.81% |
| **1.0** | 0.00% | 263.73 | 40.98 | 15.54% |
| **1.2** | 0.23% | 270.00 | 41.61 | 15.41% |
| **1.5** | 0.79% | 279.22 | 43.19 | 15.47% |
| **1.8** | 1.58% | 288.23 | 45.52 | 15.79% |
| **2.0** | 2.21% | 294.12 | 47.48 | 16.14% |

### B.4.4  N = 50

| $\alpha$ | C.1 at $g$ = 10.45% | TW (£m) | Net (£m) | Eff rate |
|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 12.57% | 1184.45 | 508.74 | 42.95% |
| **0.2** | 9.09% | 1221.24 | 470.90 | 38.56% |
| **0.5** | 2.48% | 1311.37 | 392.41 | 29.92% |
| **0.8** | 0.03% | 1377.06 | 360.19 | 26.16% |
| **1.0** | 0.00% | 1410.75 | 359.83 | 25.51% |
| **1.2** | 0.93% | 1438.38 | 373.16 | 25.94% |
| **1.5** | 3.64% | 1471.45 | 413.46 | 28.10% |
| **1.8** | 7.49% | 1497.45 | 472.04 | 31.52% |
| **2.0** | 10.50% | 1512.07 | 518.58 | 34.30% |

### B.4.5  N-crossing thresholds at canonical parameters

First N at which overstater Net > honest Net, at $g$ = 10.4%. Interpolated to one decimal place; "—" = no crossing within N = 5–65.

| $\alpha$ | N-crossing |
|:---:|:---:|
| **1.5** | 20.8 |
| **1.8** | 20.0 |
| **2.0** | 19.5 |

## B.5  $V_0$ Sweep — C.1 metric at four wealth levels

**Metric:** (Net($\alpha$) − Net(1) / TW($\alpha$) at $g$ = 10.45%.  $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, N = 29.

### B.5.1  $V_0$ = £5m

| $\alpha$ | C.1 | TW (£m) | Net (£m) | Eff rate |
|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 1.85% | 70.45 | 10.91 | 15.48% |
| **0.2** | 0.62% | 65.46 | 10.01 | 15.30% |
| **0.5** | -0.30% | 63.20 | 9.42 | 14.90% |
| **0.8** | -0.14% | 65.64 | 9.51 | 14.49% |
| **1.0** | 0.00% | 67.26 | 9.61 | 14.28% |
| **1.2** | 0.16% | 68.88 | 9.72 | 14.11% |
| **1.5** | 0.44% | 71.30 | 9.92 | 13.91% |
| **1.8** | 0.76% | 73.71 | 10.17 | 13.79% |
| **2.0** | 1.00% | 75.31 | 10.36 | 13.75% |

### B.5.2  $V_0$ = £20m  *(canonical)*

| $\alpha$ | C.1 | TW (£m) | Net (£m) | Eff rate |
|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 0.58% | 234.30 | 42.32 | 18.06% |
| **0.2** | 0.36% | 237.67 | 41.83 | 17.60% |
| **0.5** | -0.04% | 247.63 | 40.87 | 16.51% |
| **0.8** | -0.12% | 257.37 | 40.68 | 15.81% |
| **1.0** | 0.00% | 263.73 | 40.98 | 15.54% |
| **1.2** | 0.23% | 270.00 | 41.61 | 15.41% |
| **1.5** | 0.79% | 279.22 | 43.19 | 15.47% |
| **1.8** | 1.58% | 288.23 | 45.52 | 15.79% |
| **2.0** | 2.21% | 294.12 | 47.48 | 16.14% |

### B.5.3  $V_0$ = £100m

| $\alpha$ | C.1 | TW (£m) | Net (£m) | Eff rate |
|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 9.66% | 1006.85 | 363.46 | 36.10% |
| **0.2** | 7.16% | 1032.96 | 340.12 | 32.93% |
| **0.5** | 2.17% | 1100.64 | 290.04 | 26.35% |
| **0.8** | 0.12% | 1154.66 | 267.62 | 23.18% |
| **1.0** | 0.00% | 1184.56 | 266.18 | 22.47% |
| **1.2** | 0.65% | 1210.51 | 274.09 | 22.64% |
| **1.5** | 2.78% | 1243.56 | 300.79 | 24.19% |
| **1.8** | 5.95% | 1271.28 | 341.88 | 26.89% |
| **2.0** | 8.50% | 1287.55 | 375.63 | 29.17% |

### B.5.4  $V_0$ = £500m

| $\alpha$ | C.1 | TW (£m) | Net (£m) | Eff rate |
|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 32.09% | 3563.31 | 2969.61 | 83.34% |
| **0.2** | 20.31% | 3699.71 | 2577.60 | 69.67% |
| **0.5** | 3.69% | 3923.19 | 1970.74 | 50.23% |
| **0.8** | -0.23% | 4080.55 | 1816.78 | 44.52% |
| **1.0** | 0.00% | 4183.23 | 1826.13 | 43.65% |
| **1.2** | 1.30% | 4288.74 | 1882.03 | 43.88% |
| **1.5** | 4.24% | 4454.43 | 2015.16 | 45.24% |
| **1.8** | 7.65% | 4629.86 | 2180.53 | 47.10% |
| **2.0** | 9.98% | 4752.28 | 2300.59 | 48.41% |

### B.5.5  $V_0$ = £1000m

| $\alpha$ | C.1 | TW (£m) | Net (£m) | Eff rate |
|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 17.11% | 7406.52 | 4904.00 | 66.21% |
| **0.2** | 9.24% | 7053.89 | 4288.47 | 60.80% |
| **0.5** | -0.30% | 6676.54 | 3616.56 | 54.17% |
| **0.8** | -1.08% | 6801.78 | 3562.90 | 52.38% |
| **1.0** | 0.00% | 7001.28 | 3636.40 | 51.94% |
| **1.2** | 1.57% | 7254.24 | 3750.12 | 51.70% |
| **1.5** | 4.23% | 7701.89 | 3962.04 | 51.44% |
| **1.8** | 6.89% | 8207.94 | 4201.72 | 51.19% |
| **2.0** | 8.57% | 8569.84 | 4370.70 | 51.00% |

### B.5.6  $V_0$ = £5000m

| $\alpha$ | C.1 | TW (£m) | Net (£m) | Eff rate |
|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 3.07% | 26859.45 | 17703.49 | 65.91% |
| **0.2** | -6.00% | 23870.82 | 15445.35 | 64.70% |
| **0.5** | -8.28% | 24009.88 | 14891.15 | 62.02% |
| **0.8** | -3.29% | 26903.75 | 15994.42 | 59.45% |
| **1.0** | 0.00% | 29131.53 | 16878.42 | 57.94% |
| **1.2** | 2.89% | 31417.75 | 17787.61 | 56.62% |
| **1.5** | 6.55% | 34877.38 | 19163.17 | 54.94% |
| **1.8** | 9.55% | 38345.64 | 20541.75 | 53.57% |
| **2.0** | 11.27% | 40658.83 | 21461.11 | 52.78% |

### B.5.7  $V_0$ = £10000m

| $\alpha$ | C.1 | TW (£m) | Net (£m) | Eff rate |
|:---:|:---:|:---:|:---:|:---:|
| **0.1** | -7.83% | 44957.95 | 30206.33 | 67.19% |
| **0.2** | -14.45% | 41900.11 | 27671.15 | 66.04% |
| **0.5** | -9.78% | 46679.53 | 29162.01 | 62.47% |
| **0.8** | -3.43% | 53557.47 | 31889.64 | 59.54% |
| **1.0** | 0.00% | 58182.59 | 33727.74 | 57.97% |
| **1.2** | 2.93% | 62809.38 | 35566.56 | 56.63% |
| **1.5** | 6.59% | 69749.85 | 38324.90 | 54.95% |
| **1.8** | 9.59% | 76690.35 | 41083.24 | 53.57% |
| **2.0** | 11.31% | 81317.35 | 42922.14 | 52.78% |

### B.5.8  $V_0$ = £50000m

| $\alpha$ | C.1 | TW (£m) | Net (£m) | Eff rate |
|:---:|:---:|:---:|:---:|:---:|
| **0.1** | -22.03% | 187063.50 | 127430.79 | 68.12% |
| **0.2** | -18.54% | 198372.64 | 131860.77 | 66.47% |
| **0.5** | -9.86% | 233074.35 | 145652.04 | 62.49% |
| **0.8** | -3.43% | 267776.82 | 159443.78 | 59.54% |
| **1.0** | 0.00% | 290911.81 | 168638.26 | 57.97% |
| **1.2** | 2.93% | 314046.79 | 177832.75 | 56.63% |
| **1.5** | 6.59% | 348749.27 | 191624.49 | 54.95% |
| **1.8** | 9.59% | 383451.74 | 205416.22 | 53.57% |
| **2.0** | 11.31% | 406586.73 | 214610.71 | 52.78% |

## B.6  $\tau_0$ × N Joint Surface — N-crossing for $\alpha$ = 2.0

**Metric:** First N at which Net($\alpha$=2.0) > Net($\alpha$=1.0) at $g$ = 10.4%.  $\tau_m$ = 70%, $k$ = 0.001, $V_0$ = £20m.  "—" = no crossing found within N sweep ceiling.

| N ceiling \ $\tau_0$ | $\tau_0$=5% | $\tau_0$=8% | $\tau_0$=11% | $\tau_0$=14% | $\tau_0$=17% | $\tau_0$=20% | $\tau_0$=23% | $\tau_0$=26% | $\tau_0$=29% | $\tau_0$=32% | $\tau_0$=35% | $\tau_0$=38% | $\tau_0$=41% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 10 | — | — | — | — | — | — | — | — | — | — | — | — | — |
| 15 | — | — | — | — | — | — | — | — | — | — | — | — | — |
| 20 | — | — | — | 20 | 19 | 19 | 18 | 18 | 18 | 17 | 17 | 17 | 16 |
| 25 | 21 | 21 | 20 | 20 | 19 | 19 | 18 | 18 | 18 | 17 | 17 | 17 | 16 |
| 30 | 21 | 21 | 20 | 20 | 19 | 19 | 18 | 18 | 18 | 17 | 17 | 17 | 16 |
| 35 | 21 | 21 | 20 | 20 | 19 | 19 | 18 | 18 | 18 | 17 | 17 | 17 | 16 |
| 40 | 21 | 21 | 20 | 20 | 19 | 19 | 18 | 18 | 18 | 17 | 17 | 17 | 16 |
| 45 | 21 | 21 | 20 | 20 | 19 | 19 | 18 | 18 | 18 | 17 | 17 | 17 | 16 |
| 50 | 21 | 21 | 20 | 20 | 19 | 19 | 18 | 18 | 18 | 17 | 17 | 17 | 16 |
| 55 | 21 | 21 | 20 | 20 | 19 | 19 | 18 | 18 | 18 | 17 | 17 | 17 | 16 |
| 60 | 21 | 21 | 20 | 20 | 19 | 19 | 18 | 18 | 18 | 17 | 17 | 17 | 16 |
| 65 | 21 | 21 | 20 | 20 | 19 | 19 | 18 | 18 | 18 | 17 | 17 | 17 | 16 |
| 70 | 21 | 21 | 20 | 20 | 19 | 19 | 18 | 18 | 18 | 17 | 17 | 17 | 16 |

*Canonical cell: $\tau_0$ = 15%, N ceiling = 29. At $\tau_0$ = 15%, the $\alpha$ = 2.0 crossing first appears at N = 19 (row "20" ceiling, column $\tau_0$ = 14%) and stabilises at N = 19–20 regardless of how far the ceiling is extended, confirming the correction activates well within the capitalisation window.*

## B.7  $k$ × $V_0$ Joint Surface — C.1 Bracket Penalty for $\alpha$ = 1.8

**Metric:** (Net(1.8) − Net(1.0) / TW(1.8) at $g$ = 10.4%, N = 29.  $\tau_0$ = 15%, $\tau_m$ = 70%.  Positive = overstater pays more than honest (correction active); near-zero = correction negligible at this horizon.

| $k$ \ $V_0$ | £5m | £10m | £20m | £50m | £100m | £200m | £500m |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.0001 | 0.54% | 0.56% | 0.61% | 0.76% | 1.03% | 1.58% | 3.34% |
| 0.0002 | 0.56% | 0.61% | 0.71% | 1.03% | 1.58% | 2.75% | 5.96% |
| 0.0005 | 0.64% | 0.76% | 1.02% | 1.86% | 3.34% | 5.96% | 8.96% |
| 0.001 | 0.76% | 1.02% | 1.58% | 3.34% | 5.95% | 8.61% | 7.65% |
| 0.002 | 1.02% | 1.57% | 2.75% | 5.95% | 8.61% | 8.35% | 6.88% |
| 0.005 | 1.85% | 3.33% | 5.95% | 8.96% | 7.65% | 6.87% | 8.89% |
| 0.01 | 3.32% | 5.94% | 8.61% | 7.64% | 6.86% | 8.39% | 9.55% |
| 0.05 | 8.98% | 7.59% | 6.73% | 8.83% | 9.55% | 9.59% | 9.59% |
| 0.1 | 7.53% | 6.57% | 8.20% | 9.55% | 9.59% | 9.59% | 9.59% |

*Canonical cell: $k$ = 0.001, $V_0$ = £20m.*

## B.8  $W_{min}$ Sweep — C.1 metric across $\alpha$ and $g$

**Metric:** (Net($\alpha$) − Net(1) / TW($\alpha$)) 
    -  $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, N = 29, $V_0$ = £20m, $g$ = 10.45% throughout.  $W_{min}$ is the entry threshold of the logistic rate function; below this wealth level $\tau$ = 0.  $\alpha$ = 1.0 row is zero by construction.

### B.8.1  $W_{min}$ = £0m

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.27% | 11.82% | 1.91% | 0.73% | 0.57% | 0.74% | 2.15% | 6.21% | 25.62% | 30.18% |
| **0.2** | 11.54% | 10.35% | 1.63% | 0.55% | 0.36% | 0.47% | 1.51% | 4.58% | 18.36% | 19.84% |
| **0.5** | 6.64% | 6.19% | 0.90% | 0.18% | -0.04% | -0.05% | 0.24% | 1.28% | 5.37% | 4.33% |
| **0.8** | 2.16% | 2.37% | 0.31% | 0.01% | -0.12% | -0.15% | -0.16% | -0.02% | 0.55% | 0.14% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.39% | -0.26% | 0.06% | 0.24% | 0.30% | 0.45% | 0.61% | 0.83% | 0.91% |
| **1.5** | 0.00% | -1.32% | -0.56% | 0.29% | 0.79% | 1.01% | 1.63% | 2.45% | 3.76% | 3.31% |
| **1.8** | 0.00% | -1.25% | -0.75% | 0.66% | 1.58% | 2.01% | 3.34% | 5.18% | 7.96% | 6.33% |
| **2.0** | 0.00% | -1.21% | -0.83% | 0.97% | 2.21% | 2.81% | 4.73% | 7.39% | 11.19% | 8.50% |

### B.8.2  $W_{min}$ = £1m

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.26% | 11.81% | 1.91% | 0.73% | 0.57% | 0.74% | 2.15% | 6.21% | 25.63% | 30.18% |
| **0.2** | 11.53% | 10.34% | 1.63% | 0.55% | 0.36% | 0.47% | 1.51% | 4.58% | 18.37% | 19.84% |
| **0.5** | 6.64% | 6.19% | 0.90% | 0.18% | -0.04% | -0.05% | 0.24% | 1.28% | 5.37% | 4.33% |
| **0.8** | 2.16% | 2.37% | 0.31% | 0.01% | -0.12% | -0.15% | -0.16% | -0.02% | 0.55% | 0.14% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.39% | -0.26% | 0.06% | 0.24% | 0.30% | 0.45% | 0.61% | 0.83% | 0.91% |
| **1.5** | 0.00% | -1.32% | -0.56% | 0.29% | 0.79% | 1.01% | 1.63% | 2.45% | 3.76% | 3.31% |
| **1.8** | 0.00% | -1.25% | -0.75% | 0.66% | 1.58% | 2.01% | 3.34% | 5.18% | 7.96% | 6.33% |
| **2.0** | 0.00% | -1.21% | -0.83% | 0.97% | 2.21% | 2.81% | 4.72% | 7.39% | 11.19% | 8.50% |

### B.8.3  $W_{min}$ = £2m  *(canonical)*

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.25% | 11.80% | 1.91% | 0.73% | 0.58% | 0.74% | 2.15% | 6.22% | 25.65% | 30.18% |
| **0.2** | 11.52% | 10.34% | 1.63% | 0.55% | 0.36% | 0.47% | 1.51% | 4.58% | 18.39% | 19.84% |
| **0.5** | 6.64% | 6.18% | 0.90% | 0.18% | -0.04% | -0.05% | 0.24% | 1.29% | 5.38% | 4.33% |
| **0.8** | 2.16% | 2.37% | 0.31% | 0.01% | -0.12% | -0.15% | -0.15% | -0.02% | 0.55% | 0.14% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.39% | -0.26% | 0.06% | 0.23% | 0.30% | 0.45% | 0.61% | 0.83% | 0.90% |
| **1.5** | 0.00% | -1.32% | -0.56% | 0.29% | 0.79% | 1.01% | 1.63% | 2.45% | 3.76% | 3.31% |
| **1.8** | 0.00% | -1.25% | -0.75% | 0.66% | 1.58% | 2.00% | 3.33% | 5.18% | 7.96% | 6.33% |
| **2.0** | 0.00% | -1.21% | -0.83% | 0.97% | 2.21% | 2.81% | 4.72% | 7.39% | 11.19% | 8.50% |

### B.8.4  $W_{min}$ = £5m

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 0.00% | 11.63% | 3.01% | 2.39% | 2.65% | 2.95% | 5.28% | 10.96% | 32.80% | 32.37% |
| **0.2** | 0.00% | 9.99% | 1.81% | 0.84% | 0.81% | 1.00% | 1.94% | 5.31% | 19.93% | 19.86% |
| **0.5** | 0.00% | 6.17% | 0.90% | 0.18% | -0.04% | -0.05% | 0.25% | 1.29% | 5.39% | 4.34% |
| **0.8** | 0.00% | 2.37% | 0.31% | 0.01% | -0.11% | -0.15% | -0.15% | -0.02% | 0.55% | 0.15% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.39% | -0.26% | 0.06% | 0.23% | 0.30% | 0.45% | 0.61% | 0.82% | 0.90% |
| **1.5** | 0.00% | -1.32% | -0.56% | 0.29% | 0.79% | 1.01% | 1.63% | 2.45% | 3.75% | 3.30% |
| **1.8** | 0.00% | -1.25% | -0.75% | 0.65% | 1.57% | 2.00% | 3.33% | 5.18% | 7.95% | 6.32% |
| **2.0** | 0.00% | -1.20% | -0.83% | 0.97% | 2.21% | 2.80% | 4.72% | 7.38% | 11.19% | 8.49% |

### B.8.5  $W_{min}$ = £10m

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 0.00% | 11.59% | 3.47% | 3.32% | 4.03% | 4.44% | 7.42% | 14.17% | 39.70% | 33.65% |
| **0.2** | 0.00% | 9.95% | 2.27% | 1.92% | 2.21% | 2.48% | 4.40% | 8.87% | 24.41% | 22.82% |
| **0.5** | 0.00% | 6.15% | 0.89% | 0.18% | -0.03% | -0.04% | 0.25% | 1.30% | 5.42% | 4.35% |
| **0.8** | 0.00% | 2.36% | 0.31% | 0.01% | -0.11% | -0.14% | -0.15% | -0.01% | 0.56% | 0.15% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.39% | -0.26% | 0.06% | 0.23% | 0.30% | 0.45% | 0.61% | 0.82% | 0.90% |
| **1.5** | 0.00% | -1.32% | -0.56% | 0.29% | 0.79% | 1.00% | 1.62% | 2.44% | 3.75% | 3.29% |
| **1.8** | 0.00% | -1.25% | -0.75% | 0.65% | 1.56% | 1.99% | 3.32% | 5.17% | 7.95% | 6.31% |
| **2.0** | 0.00% | -1.20% | -0.83% | 0.96% | 2.20% | 2.80% | 4.71% | 7.38% | 11.19% | 8.47% |

### B.8.6  $W_{min}$ = £50m

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 0.00% | 0.00% | 5.85% | 4.42% | 5.23% | 6.29% | 10.42% | 20.69% | 50.04% | 32.53% |
| **0.2** | 0.00% | 0.00% | 4.32% | 2.80% | 3.48% | 4.12% | 6.95% | 13.29% | 33.33% | 22.90% |
| **0.5** | 0.00% | 0.00% | 0.28% | 0.83% | 1.06% | 1.25% | 2.17% | 4.03% | 10.07% | 6.98% |
| **0.8** | 0.00% | 0.00% | 0.05% | 0.08% | 0.18% | 0.22% | 0.24% | 0.58% | 2.39% | 1.27% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | 0.00% | -0.02% | 0.00% | 0.05% | 0.04% | -0.07% | -0.28% | -0.03% | -0.35% |
| **1.5** | 0.00% | 0.00% | 0.22% | 0.32% | 0.44% | 0.50% | 0.62% | 1.17% | 2.10% | 0.74% |
| **1.8** | 0.00% | 0.00% | 0.51% | 0.77% | 1.14% | 1.38% | 2.11% | 3.53% | 5.51% | 2.53% |
| **2.0** | 0.00% | 0.00% | 0.84% | 1.28% | 1.74% | 2.11% | 3.26% | 5.31% | 8.79% | 3.57% |

### B.8.5  N-crossing thresholds by $W_{min}$ at canonical parameters

First N at which overstater Net > honest Net, at $g$ = 10.4%. Interpolated to one decimal place; "—" = no crossing within N = 5–65.

| $W_{min}$ | $\alpha$ = 1.5 | $\alpha$ = 1.8 | $\alpha$ = 2.0 |
|:---:|:---:|:---:|:---:|
| **£0m** | 20.8 | 20.0 | 19.5 |
| **£1m** | 20.8 | 20.0 | 19.5 |
| **£2m** *(canon)* | 20.8 | 20.0 | 19.5 |
| **£5m** | 20.9 | 20.0 | 19.5 |
| **£10m** | 20.9 | 20.0 | 19.6 |
| **£50m** | — | — | — |

## B.9  Figure Index

All figures are generated by the VAL.S output scripts (`val_s_rate_sweeps.py`, `val_s_horizon_sweeps.py`, `val_s_interactions.py`) and share `wdt_core.py` as the simulation engine with no modifications. VAL.A cross-references indicate which (SWEEPS.A §A) or (SWEEPS.A §B) subsection covers the same metric at canonical parameters.

| Fig | File | Title | Axes | Parameters | VAL.A ref |
|:---:|:---:|:---:|:---:|:---:|:---:|
| SS2.1a | val_s_fig_s2_1a_tau0_heatmaps.png | C.1 advantage landscape across $\tau_0$ values — 4-panel heatmap grid | Rows = $\alpha$ ∈ {0.1,0.2,0.5,0.8,1.0,1.2,1.5,1.8,2.0}; cols = $g$ ∈ G_VALS; colour = C.1 (pp) | $\tau_m$=70%, k=0.001, N=29, $V_0$=£20m; $\tau_0$ swept across panels | C.1 |
| SS2.1b | val_s_fig_s2_1b_tau0_n_crossings.png | N-crossing thresholds for $\alpha$ ∈ {1.5, 1.8, 2.0} as a function of $\tau_0$ | x = $\tau_0$ (%); y = N at which overstater first pays more than honest; line per $\alpha$ | $\tau_m$=70%, k=0.001, $V_0$=£20m, $g$=10.4% | C.7, B.5.6 |
| SS2.1c | val_s_fig_s2_1c_tau0_tolerant_zone.png | Tolerant-zone (|C.1| < 2pp) $\alpha$ boundaries as a function of $\tau_0$ | x = $\tau_0$ (%); y = $\alpha$; filled band = tolerant zone; dashed lines = VAL.A canonical bounds | $\tau_m$=70%, k=0.001, N=29, $g$=10.4% | B.6 |
| SS2.2a | val_s_fig_s2_2a_taum_heatmaps.png | C.1 advantage landscape across $\tau_m$ values — 4-panel heatmap grid | As S2.1a; $\tau_m$ swept across panels | $\tau_0$=15%, k=0.001, N=29, $V_0$=£20m | C.1 |
| SS2.2b | val_s_fig_s2_2b_taum_penalty_plateaus.png | Understater penalty plateau ceiling by $\alpha$, as a function of $\tau_m$ | x = $\alpha$ (understater range); y = plateau ceiling of C.1 (pp); line per $\tau_m$ | $\tau_0$=15%, k=0.001, N=29; plateau evaluated at $g$ = 18–40% | C.9, B.5.4 |
| SS2.2c | val_s_fig_s2_2c_taum_n_crossings.png | N-crossing thresholds for aggressive overstaters as a function of $\tau_m$ | x = $\tau_m$ (%); y = N at crossing; line per $\alpha$ ∈ {1.5, 1.8, 2.0} | $\tau_0$=15%, k=0.001, $V_0$=£20m, $g$=10.4% | C.7, B.5.4 |
| SS2.3a | val_s_fig_s2_3a_k_rate_curves.png | Rate curve $\tau(W)$ overlaid for four $k$ values | x = W (£m, log); y = $\tau(W)$ (%); line per k; $V_0$ reference vline | $\tau_0$=15%, $\tau_m$=70%, $W_{min}$=£2m | B.3.1, Fig 5.1 in VAL |
| SS2.3b | val_s_fig_s2_3b_k_heatmaps.png | C.1 advantage landscape across $k$ values — 4-panel heatmap grid | As S2.1a; $k$ swept across panels | $\tau_0$=15%, $\tau_m$=70%, N=29, $V_0$=£20m | C.1, C.5 |
| SS2.3c | val_s_fig_s2_3c_k_bracket_penalty.png | Bracket penalty for $\alpha$ = 1.8 at W = {£20m, £100m, £500m} as a function of $k$ | x = k; y = C.1 (pp) at $\alpha$=1.8; line per $V_0$ level | $\tau_0$=15%, $\tau_m$=70%, N=29, $g$=10.4% | C.1, B.5.2 |
| SS3.1a | val_s_fig_s3_1a_n_crossing_annotated.png | Overstater advantage erosion and N-crossing thresholds (two-panel) | Left: x = N, y = Net($\alpha$)−Net(honest) £m, line per $\alpha$. Right: bar chart of crossing N per $\alpha$. | $\tau_0$=15%, $\tau_m$=70%, k=0.001, $V_0$=£20m, $g$=10.4% | C.7, B.6, Fig 7.1 in VAL |
| SS3.1b | val_s_fig_s3_1b_n_understater_panels.png | Understater C.1 penalty profile by $g$ at N ∈ {10, 20, 29, 50} — 4-panel | x = $g$ (%); y = C.1 (pp); line per understater $\alpha$; panel per N | $\tau_0$=15%, $\tau_m$=70%, k=0.001, $V_0$=£20m | C.9, B.5.3, Fig 7.4 in VAL |
| SS3.1c | val_s_fig_s3_1c_n_tolerant_zone.png | Tolerant-zone (|C.1| < 2pp) $\alpha$ boundaries across N values | x = N (years); y = $\alpha$; filled band = tolerant zone; VAL.A bounds annotated | $\tau_0$=15%, $\tau_m$=70%, k=0.001, $g$=10.4% | B.6 |
| SS3.2a | val_s_fig_s3_2a_v0_c1_curves.png | C.1 incentive structure by $V_0$ entry wealth — overlaid curves | x = $\alpha$ (%); y = C.1 (pp); line per $V_0$; $g$ = canonical | $\tau_0$=15%, $\tau_m$=70%, k=0.001, N=29, $g$=10.4% | C.1, Fig 7.2 in VAL |
| SS3.2b | val_s_fig_s3_2b_v0_entry_rate.png | Entry rate $\tau(V_0)$ at four wealth levels annotated on the rate curve | x = W (£m, log); y = $\tau(W)$ (%); markers at $V_0$ ∈ {£5m, £20m, £100m, £500m} | $\tau_0$=15%, $\tau_m$=70%, k=0.001 | B.3.1, Fig 5.1 in VAL |
| SS3.2c | val_s_fig_s3_2c_v0_heatmaps.png | C.1 advantage landscape across $V_0$ entry wealth levels — 4-panel heatmap grid | As S2.1a; $V_0$ swept across panels | $\tau_0$=15%, $\tau_m$=70%, k=0.001, N=29 | C.1 |
| SS2.4a | val_s_fig_s2_4a_wmin_rate_curves.png | Rate curve $\tau(W)$ overlaid for four $W_{min}$ values — onset-shift comparison | x = W (£m, log); y = $\tau(W)$ (%); line per $W_{min}$; $V_0$ reference vline; $W_{min}$ onset vlines | $\tau_0$=15%, $\tau_m$=70%, k=0.001; $W_{min}$ swept | B.3.1, Fig 5.1 in VAL |
| SS2.4b | val_s_fig_s2_4b_wmin_heatmaps.png | C.1 advantage landscape across $W_{min}$ values — 4-panel heatmap grid | As S2.1a; $W_{min}$ swept across panels | $\tau_0$=15%, $\tau_m$=70%, k=0.001, N=29, $V_0$=£20m | C.1 |
| SS2.4c | val_s_fig_s2_4c_wmin_n_crossings.png | N-crossing thresholds for $\alpha$ ∈ {1.5, 1.8, 2.0} as a function of $W_{min}$ | x = $W_{min}$ (£m); y = N at crossing; line per $\alpha$; $V_0$ reference vline | $\tau_0$=15%, $\tau_m$=70%, k=0.001, $V_0$=£20m, $g$=10.4% | C.7, B.5.4 |
| SS4.1 | val_s_fig_s4_1_tau0_n_surface.png | Joint surface: N-crossing for $\alpha$ = 2.0 across ($\tau_0$, N ceiling) | x = $\tau_0$ (%); y = N sweep ceiling (years); colour = N-crossing value (crossings present throughout full range) | $\tau_m$=70%, k=0.001, $V_0$=£20m, $g$=10.4% | C.7, B.5.4, B.6 |
| SS4.2 | val_s_fig_s4_2_k_v0_surface.png | Joint surface: C.1 bracket penalty for $\alpha$ = 1.8 across (k, $V_0$) | x = $V_0$ (£m); y = k; colour = C.1 (pp) at $\alpha$=1.8; border = canonical cell | $\tau_0$=15%, $\tau_m$=70%, N=29, $g$=10.4% | C.1, C.5 |
| SS4.3 | val_s_fig_s4_3_calibration_summary.png | Governing Council calibration summary — three mechanism properties by parameter variant | Three bar-chart panels: tolerant-zone width, N-crossing for $\alpha$=1.8, plateau ceiling at $\alpha$=0.1 | N=29, $V_0$=£20m, $g$=10.4%; all $\tau_0$/$\tau_m$/k/$W_{min}$ variants shown together | B.6, C.9, (SWEEPS §5) calibration discussion |

# D. WDT Rate Parameter Sensitivity Sweep

**Run date:** 2026-08-30  
**Model version:** v6 (rates_model.py / wdt_core.py)  
**Parameters file:** `260812_WDT_Params.toml`  

## D.1 Purpose

This document sweeps each of the four WDT rate-function parameters independently, holding the other three at Balanced baseline values, and reports how key transition metrics vary across the full 73-year historical start-year sweep (1947–2019 UK equity return series). It is intended as orientation material for future Governing Council calibration work, not as a scenario recommendation. Parameter interactions are not modelled here; joint sweeps are a natural second-order extension.

### D.1.1 The Rate Function

The WDT logistic marginal rate function is:

$$\tau(W) = \frac{\tau_m}{1 + \left(\frac{\tau_m - \tau_0}{\tau_0}\right)e^{-k(W - W_{\min})}}, \quad \tau(W) = 0 \text{ if } W < W_{\min}$$

Note: the docstring in `rates_model.py` contains a typographical error writing $(1-\tau_0)/\tau_0$ as the denominator coefficient. The implementation in `wdt_core.tau()` correctly uses $(\tau_m - \tau_0)/\tau_0$. All results here use the correct formula.

### D.1.2 Balanced Baseline Parameters

| Parameter | Baseline value | Role |
|---|---|---|
| $\tau_0$ (floor rate) | 15% | Marginal rate at W = W_min; determines tax on the smallest deltas |
| $\tau_m$ (ceiling rate) | 70% | Asymptotic ceiling; determines the maximum rate as W → ∞ |
| k (steepness, per £m) | 0.001 | Controls how rapidly the rate climbs through the wealth distribution |
| W_min (£m) | £2.0m | Entry point; below this the rate is zero regardless of δ |

**SWF sizing parameters (Balanced baseline; swept in §§5–6):**

| Parameter | Baseline value | Role |
|---|---|---|
| SRR capitalisation ratio | 3.0× | SRR target = ratio × (cumulative net income / N); sets how long before the refund guarantee is credible |
| LRR floor | 3.0 years of expenditure | LRR target = lrr_years × prevailing government expenditure; sets the Phase Two viability threshold |

**Non-SWF parameters (held constant throughout all sweeps):**

| Parameter | Value |
|---|---|
| Budget base (£b) | £1,157.4b |
| Budget growth (p.a.) | 4.51% |
| Historical mean return | 10.45% |
| Wealth brackets | 10 |
| Growth tiers | 4 |

### D.1.3 Metrics

**Success:** LRR fills within the 71-year modelling window AND (SRR never breaches OR SRR breach is fully covered by LRR balance at time of breach).

**SSM coverage ratio:** Average annual net SSM income over the capitalisation window (SRR fill to LRR fill) divided by average annual government expenditure over the same window. Applies the correlated-shock assumption (all taxpayers experience the same return simultaneously) — the worst-case floor.

**TCM coverage ratio:** Average annual TCM revenue over the same capitalisation window divided by average annual government expenditure. Applies four persistent heterogeneous growth tier differentials — the persistent-heterogeneity ceiling. Together the SSM and TCM ratios bracket the plausible revenue range.

**LRR fill year:** First year the LRR balance reaches the 3× expenditure floor. The primary transition-speed metric; gates full Phase Two fiscal replacement.

**SRR fill year:** First year the SRR reaches its capitalisation target. Should be invariant at ~3 across most calibrations.

**LRR surplus at fill:** LRR balance minus LRR target at the fill year, in £D. Safety margin above the floor at the breakeven point.

*All distributions are across the 73 historical start years 1947–2019. The 2006 start year is extracted separately as the worst-case historical scenario (longest LRR fill time at Balanced parameters).*

## D.2 Floor Rate (τ_0)

τ_0 sets the marginal rate at W = W_min. A higher floor raises effective rates across the entire taxable population (since every taxpayer above W_min pays at least τ_0 on their first pound of delta); a lower floor concentrates the rate gradient in the upper distribution.

### D.2.1 τ_0 sweep

Other parameters held at Balanced baseline: τ_m = 70%,  k = 0.001,  W_min = £2.0m.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSM cov (min/med/mean/max) | TCM cov (min/med/mean/max) | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 5% | 100% | 14.6% / 24.3% / 28.5% / 56.4% | 21.6% / 26.8% / 32.3% / 57.7% | 10 / 22 / 24 / 42 | 3 | 10 / 911 |
| 10% | 100% | 17.1% / 33.1% / 37.8% / 86.8% | 21.6% / 35.7% / 41.0% / 88.6% | 8 / 16 / 18 / 34 | 3 | 27 / 886 |
| 15% ◄ | 100% | 19.0% / 39.7% / 47.0% / 130.5% | 24.0% / 40.3% / 50.0% / 134.5% | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| 20% | 100% | 17.9% / 42.2% / 53.3% / 140.9% | 23.3% / 43.8% / 56.2% / 136.8% | 6 / 12 / 14 / 27 | 3 | 13 / 908 |
| 25% | 100% | 20.3% / 48.0% / 58.4% / 169.9% | 25.5% / 48.5% / 61.2% / 164.8% | 6 / 11 / 13 / 26 | 3 | 77 / 692 |
| 30% | 100% | 19.4% / 52.4% / 63.3% / 162.7% | 24.9% / 49.8% / 66.2% / 191.3% | 5 / 10 / 12 / 25 | 3 | 4 / 822 |
| 35% | 100% | 21.5% / 57.3% / 70.7% / 186.2% | 25.7% / 53.2% / 72.9% / 219.3% | 5 / 10 / 11 / 24 | 3 | 37 / 1095 |
| 40% | 100% | 20.1% / 61.4% / 74.3% / 203.6% | 23.9% / 57.4% / 74.9% / 208.5% | 5 / 10 / 11 / 24 | 3 | 30 / 1124 |
| 45% | 100% | 19.7% / 67.4% / 80.6% / 224.7% | 23.6% / 61.6% / 79.7% / 230.4% | 5 / 9 / 10 / 21 | 3 | 8 / 849 |
| 50% | 100% | 21.1% / 68.8% / 83.0% / 204.7% | 25.0% / 64.4% / 81.3% / 204.1% | 5 / 9 / 10 / 20 | 3 | 24 / 688 |

*◄ = Balanced baseline value. Coverage ratios: capitalisation-window averages (SRR fill to LRR fill). Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSM cov | TCM cov | LRR fill yr | LRR surplus £b | SRR breach covered |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 5% | 16.4% | 23.7% | 39 | 1595 | — (no breach) |
| 10% | 18.0% | 24.6% | 34 | 1229 | — (no breach) |
| 15% ◄ | 20.8% | 27.1% | 29 | 523 | — (no breach) |
| 20% | 22.3% | 28.3% | 26 | 1999 | — (no breach) |
| 25% | 20.3% | 25.5% | 25 | 973 | YES |
| 30% | 24.6% | 28.8% | 25 | 2606 | YES |
| 35% | 29.7% | 29.6% | 21 | 411 | YES |
| 40% | 36.0% | 32.4% | 21 | 1277 | YES |
| 45% | 39.5% | 35.1% | 21 | 2075 | YES |
| 50% | 38.0% | 31.2% | 20 | 434 | YES |

## D.3 Ceiling Rate (τ_m)

τ_m is the asymptotic ceiling the marginal rate approaches but never reaches. Its primary effect is on the top brackets where W >> W_min; the logistic function brings effective rates close to τ_m only at very high declared wealth levels. Raising τ_m increases revenue from the highest-wealth, highest-growth cells disproportionately, since those cells also generate the largest absolute deltas.

### D.3.1 τ_m sweep

Other parameters held at Balanced baseline: τ_0 = 15%,  k = 0.001,  W_min = £2.0m.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSM cov (min/med/mean/max) | TCM cov (min/med/mean/max) | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 50% | 100% | 19.0% / 39.7% / 47.0% / 130.4% | 24.0% / 40.2% / 49.9% / 134.4% | 7 / 13 / 15 / 29 | 3 | 3 / 911 |
| 55% | 100% | 19.0% / 39.7% / 47.0% / 130.5% | 24.0% / 40.2% / 49.9% / 134.5% | 7 / 13 / 15 / 29 | 3 | 4 / 914 |
| 60% | 100% | 19.0% / 39.7% / 47.0% / 130.5% | 24.0% / 40.2% / 50.0% / 134.5% | 7 / 13 / 15 / 29 | 3 | 4 / 916 |
| 65% | 100% | 19.0% / 39.7% / 47.0% / 130.5% | 24.0% / 40.2% / 50.0% / 134.5% | 7 / 13 / 15 / 29 | 3 | 5 / 918 |
| 70% ◄ | 100% | 19.0% / 39.7% / 47.0% / 130.5% | 24.0% / 40.3% / 50.0% / 134.5% | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| 75% | 100% | 19.0% / 39.8% / 47.0% / 130.5% | 24.0% / 40.3% / 50.0% / 134.5% | 7 / 13 / 15 / 29 | 3 | 6 / 920 |
| 80% | 100% | 19.0% / 39.8% / 47.0% / 130.6% | 24.0% / 40.3% / 50.0% / 134.6% | 7 / 13 / 15 / 29 | 3 | 7 / 921 |
| 85% | 100% | 19.0% / 39.8% / 47.0% / 130.6% | 24.0% / 40.3% / 50.0% / 134.6% | 7 / 13 / 15 / 29 | 3 | 7 / 922 |
| 90% | 100% | 19.0% / 39.8% / 47.0% / 130.6% | 24.0% / 40.3% / 50.0% / 134.6% | 7 / 13 / 15 / 29 | 3 | 7 / 923 |
| 95% | 100% | 19.0% / 39.8% / 47.0% / 130.6% | 24.0% / 40.3% / 50.0% / 134.6% | 7 / 13 / 15 / 29 | 3 | 8 / 924 |
| 100% | 100% | 19.0% / 39.8% / 47.0% / 130.6% | 24.0% / 40.3% / 50.0% / 134.6% | 7 / 13 / 15 / 29 | 3 | 8 / 925 |

*◄ = Balanced baseline value. Coverage ratios: capitalisation-window averages (SRR fill to LRR fill). Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSM cov | TCM cov | LRR fill yr | LRR surplus £b | SRR breach covered |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 50% | 20.8% | 27.0% | 29 | 514 | — (no breach) |
| 55% | 20.8% | 27.0% | 29 | 517 | — (no breach) |
| 60% | 20.8% | 27.1% | 29 | 519 | — (no breach) |
| 65% | 20.8% | 27.1% | 29 | 521 | — (no breach) |
| 70% ◄ | 20.8% | 27.1% | 29 | 523 | — (no breach) |
| 75% | 20.8% | 27.1% | 29 | 524 | — (no breach) |
| 80% | 20.8% | 27.1% | 29 | 525 | — (no breach) |
| 85% | 20.8% | 27.1% | 29 | 526 | — (no breach) |
| 90% | 20.8% | 27.1% | 29 | 527 | — (no breach) |
| 95% | 20.8% | 27.1% | 29 | 528 | — (no breach) |
| 100% | 20.8% | 27.1% | 29 | 529 | — (no breach) |

## D.4 Steepness (k)

k (per £m) controls how rapidly the marginal rate climbs from τ_0 toward τ_m through the wealth distribution. Low k produces a shallow gradient — most taxpayers face rates close to τ_0 even at high wealth levels, with τ_m approached only at very large holdings. High k produces a steep step — the rate reaches τ_m quickly above W_min, compressing the gradient into a narrow wealth band.

*Sweep is log-spaced: 0.0001, 0.0002, 0.0005, 0.0010, 0.0020, 0.0050, 0.0100, 0.0500, 0.1000*

### D.4.1 k sweep (log-spaced)

Other parameters held at Balanced baseline: τ_0 = 15%,  τ_m = 70%,  W_min = £2.0m.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSM cov (min/med/mean/max) | TCM cov (min/med/mean/max) | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.0001 | 100% | 18.9% / 39.6% / 46.8% / 129.9% | 23.8% / 40.1% / 49.6% / 133.8% | 7 / 13 / 15 / 29 | 3 | 14 / 859 |
| 0.0002 | 100% | 18.9% / 39.6% / 46.8% / 129.9% | 23.8% / 40.1% / 49.6% / 133.9% | 7 / 13 / 15 / 29 | 3 | 17 / 866 |
| 0.0005 | 100% | 18.9% / 39.6% / 46.9% / 130.2% | 23.9% / 40.1% / 49.7% / 134.1% | 7 / 13 / 15 / 29 | 3 | 29 / 886 |
| 0.0010 ◄ | 100% | 19.0% / 39.7% / 47.0% / 130.5% | 24.0% / 40.3% / 50.0% / 134.5% | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| 0.0020 | 100% | 19.1% / 40.0% / 47.2% / 131.3% | 24.2% / 40.5% / 50.1% / 135.3% | 7 / 13 / 15 / 29 | 3 | 0 / 939 |
| 0.0050 | 100% | 19.2% / 40.6% / 47.1% / 112.2% | 24.0% / 41.1% / 50.0% / 109.3% | 6 / 13 / 15 / 29 | 3 | 22 / 727 |
| 0.0100 | 100% | 18.9% / 41.2% / 47.7% / 115.0% | 24.7% / 40.7% / 50.7% / 112.1% | 6 / 13 / 15 / 29 | 3 | 4 / 718 |
| 0.0500 | 100% | 16.7% / 41.5% / 51.9% / 133.4% | 22.6% / 44.2% / 55.0% / 131.0% | 6 / 12 / 14 / 27 | 3 | 3 / 845 |
| 0.1000 | 100% | 18.4% / 43.1% / 55.7% / 151.3% | 23.5% / 44.9% / 59.0% / 149.2% | 6 / 12 / 14 / 27 | 3 | 70 / 1067 |

*◄ = Balanced baseline value. Coverage ratios: capitalisation-window averages (SRR fill to LRR fill). Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSM cov | TCM cov | LRR fill yr | LRR surplus £b | SRR breach covered |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.0001 | 20.7% | 26.9% | 29 | 457 | — (no breach) |
| 0.0002 | 20.7% | 26.9% | 29 | 464 | — (no breach) |
| 0.0005 | 20.7% | 27.0% | 29 | 486 | — (no breach) |
| 0.0010 ◄ | 20.8% | 27.1% | 29 | 523 | — (no breach) |
| 0.0020 | 20.9% | 27.3% | 29 | 596 | — (no breach) |
| 0.0050 | 21.3% | 27.9% | 29 | 809 | YES |
| 0.0100 | 21.8% | 28.7% | 29 | 1136 | YES |
| 0.0500 | 21.3% | 28.1% | 26 | 1442 | YES |
| 0.1000 | 25.3% | 31.8% | 26 | 2820 | YES |

## D.5 Entry Point (W_min)

W_min (£m) is the wealth level below which the rate function produces zero liability. It is a rate design parameter, not a population boundary — all UK adults are within the taxable population regardless of W_min. Lower W_min pulls more of the 50th–80th percentile brackets into material liability; higher W_min concentrates the tax on the top percentiles. W_min also affects refund exposure in loss years, since a taxpayer below W_min receives no refund even if their delta is negative.

### D.5.1 W_min sweep

Other parameters held at Balanced baseline: τ_0 = 15%,  τ_m = 70%,  k = 0.001.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSM cov (min/med/mean/max) | TCM cov (min/med/mean/max) | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| £0.1m | 100% | 19.8% / 47.6% / 58.9% / 141.3% | 22.8% / 45.1% / 60.4% / 142.4% | 6 / 10 / 12 / 26 | 3 | 1 / 557 |
| £0.25m | 100% | 19.8% / 47.6% / 58.9% / 141.3% | 22.8% / 45.1% / 60.4% / 142.4% | 6 / 10 / 12 / 26 | 3 | 1 / 557 |
| £0.5m | 100% | 19.8% / 47.6% / 59.1% / 141.2% | 22.9% / 45.3% / 60.5% / 142.4% | 6 / 11 / 12 / 26 | 3 | 49 / 545 |
| £1.0m | 100% | 18.6% / 44.1% / 56.3% / 137.5% | 22.0% / 45.4% / 58.4% / 136.6% | 6 / 11 / 13 / 27 | 3 | 2 / 895 |
| £2.0m ◄ | 100% | 19.0% / 39.7% / 47.0% / 130.5% | 24.0% / 40.3% / 50.0% / 134.5% | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| £3.0m | 100% | 18.0% / 33.9% / 39.2% / 89.8% | 24.9% / 38.0% / 44.0% / 98.9% | 8 / 15 / 17 / 33 | 3 | 52 / 976 |
| £5.0m | 100% | 15.7% / 27.8% / 33.0% / 72.2% | 23.5% / 34.0% / 39.9% / 79.9% | 9 / 18 / 20 / 35 | 3 | 72 / 1210 |
| £7.5m | 100% | 14.2% / 24.8% / 29.5% / 61.3% | 20.7% / 32.9% / 36.9% / 62.7% | 10 / 21 / 22 / 37 | 3 | 12 / 1001 |
| £10.0m | 100% | 13.4% / 23.3% / 26.9% / 51.8% | 21.9% / 34.3% / 36.4% / 63.2% | 11 / 22 / 24 / 39 | 3 | 79 / 1250 |

*◄ = Balanced baseline value. Coverage ratios: capitalisation-window averages (SRR fill to LRR fill). Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSM cov | TCM cov | LRR fill yr | LRR surplus £b | SRR breach covered |
|:---:|:---:|:---:|:---:|:---:|:---:|
| £0.1m | 20.6% | 23.1% | 25 | 267 | — (no breach) |
| £0.25m | 20.6% | 23.1% | 25 | 266 | — (no breach) |
| £0.5m | 20.4% | 23.0% | 25 | 207 | — (no breach) |
| £1.0m | 23.2% | 26.7% | 26 | 1779 | — (no breach) |
| £2.0m ◄ | 20.8% | 27.1% | 29 | 523 | — (no breach) |
| £3.0m | 19.2% | 28.1% | 32 | 961 | — (no breach) |
| £5.0m | 19.5% | 31.6% | 35 | 4518 | — (no breach) |
| £7.5m | 14.2% | 26.4% | 35 | 115 | — (no breach) |
| £10.0m | 14.0% | 30.1% | 38 | 2710 | — (no breach) |

## D.6 SRR Capitalisation Ratio (srr_ratio)

srr_ratio sets the SRR capitalisation target as a multiple of average annual net WDT income. A higher ratio means the SRR must accumulate more before it is considered fully capitalised, which delays SRR fill and thereby reduces the flow into the LRR during the early accumulation period. A lower ratio allows faster SRR fill and faster LRR accumulation, but at the cost of a thinner refund buffer. The Governing Council recommended floor is 3×; the working SSM-derived value is 3×.

*Note: srr_ratio does not affect the rate function or individual taxpayer burden — it affects only the milestone timing (SRR fill year and LRR fill year). The burden distribution panel in the chart companion is flat across this sweep.*

### D.6.1 srr_ratio sweep

Other parameters held at Balanced baseline: τ_0 = 15%,  τ_m = 70%,  k = 0.001,  W_min = £2.0m,  lrr_years = 3.0.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSM cov (min/med/mean/max) | TCM cov (min/med/mean/max) | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1.0× | 100% | 18.5% / 32.1% / 37.7% / 78.0% | 21.2% / 33.9% / 39.2% / 87.1% | 5 / 12 / 14 / 28 | 1 | 10 / 641 |
| 1.5× | 100% | 18.6% / 33.8% / 40.0% / 89.4% | 21.8% / 35.7% / 42.1% / 91.4% | 6 / 12 / 14 / 28 | 2 | 0 / 580 |
| 2.0× | 100% | 18.5% / 36.7% / 42.1% / 90.3% | 23.1% / 38.2% / 44.2% / 88.7% | 6 / 13 / 15 / 29 | 2 | 17 / 654 |
| 2.5× | 100% | 18.8% / 39.3% / 45.2% / 110.0% | 23.4% / 38.4% / 47.5% / 107.0% | 6 / 13 / 15 / 29 | 3 | 17 / 657 |
| 3.0× ◄ | 100% | 19.0% / 39.7% / 47.0% / 130.5% | 24.0% / 40.3% / 50.0% / 134.5% | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| 4.0× | 100% | 18.8% / 44.6% / 52.2% / 126.9% | 24.5% / 50.5% / 56.3% / 132.3% | 8 / 14 / 16 / 29 | 4 | 28 / 956 |
| 5.0× | 100% | 18.7% / 45.6% / 57.8% / 149.5% | 24.5% / 50.4% / 62.1% / 152.5% | 8 / 15 / 17 / 30 | 5 | 2 / 831 |
| 6.0× | 100% | 20.7% / 50.5% / 63.2% / 157.9% | 28.4% / 49.9% / 68.2% / 165.7% | 9 / 16 / 18 / 31 | 6 | 31 / 840 |
| 8.0× | 100% | 21.5% / 61.2% / 77.8% / 238.7% | 29.9% / 65.1% / 84.3% / 245.1% | 11 / 17 / 19 / 33 | 8 | 4 / 1026 |
| 10.0× | 100% | 22.8% / 65.1% / 91.7% / 276.3% | 31.9% / 62.8% / 99.6% / 287.3% | 13 / 19 / 21 / 34 | 10 | 2 / 1073 |

*◄ = Balanced baseline value. Coverage ratios: capitalisation-window averages (SRR fill to LRR fill). Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSM cov | TCM cov | LRR fill yr | LRR surplus £b | SRR breach covered |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 1.0× | 18.5% | 21.6% | 26 | 282 | YES |
| 1.5× | 18.6% | 21.8% | 26 | 67 | YES |
| 2.0× | 20.9% | 26.3% | 29 | 1002 | YES |
| 2.5× | 21.7% | 27.1% | 29 | 762 | — (no breach) |
| 3.0× ◄ | 20.8% | 27.1% | 29 | 523 | — (no breach) |
| 4.0× | 21.1% | 27.5% | 29 | 43 | — (no breach) |
| 5.0× | 22.0% | 30.1% | 30 | 1146 | — (no breach) |
| 6.0× | 22.6% | 30.7% | 30 | 601 | — (no breach) |
| 8.0× | 24.0% | 33.2% | 32 | 768 | — (no breach) |
| 10.0× | 26.1% | 36.4% | 34 | 2489 | — (no breach) |

## D.7 LRR Floor (lrr_years)

lrr_years sets the LRR floor as a multiple of prevailing government expenditure. The LRR target therefore grows over time as nominal expenditure grows at 4.51% p.a. A higher floor requires the LRR to accumulate more before Phase Two becomes viable, directly extending the LRR fill year. A lower floor brings LRR fill earlier but with a thinner buffer against sustained drawdown post-fill. The recommended minimum is 3 years.

*Note: lrr_years does not affect the rate function or individual taxpayer burden — it affects only the LRR milestone timing and the safety margin above the floor. The burden distribution panel in the chart companion is flat across this sweep.*

### D.7.1 lrr_years sweep

Other parameters held at Balanced baseline: τ_0 = 15%,  τ_m = 70%,  k = 0.001,  W_min = £2.0m,  srr_ratio = 3.0×.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSM cov (min/med/mean/max) | TCM cov (min/med/mean/max) | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.5 yrs | 100% | -0.4% / 20.3% / 26.3% / 109.8% | -0.0% / 20.7% / 27.6% / 107.8% | 4 / 6 / 7 / 12 | 3 | 3 / 192 |
| 1.0 yrs | 100% | 7.5% / 25.4% / 32.3% / 93.2% | 10.0% / 27.8% / 33.3% / 96.7% | 5 / 8 / 9 / 19 | 3 | 4 / 311 |
| 1.5 yrs | 100% | 10.5% / 28.4% / 35.7% / 88.1% | 13.8% / 27.9% / 37.7% / 102.7% | 5 / 10 / 11 / 24 | 3 | 6 / 582 |
| 2.0 yrs | 100% | 13.3% / 29.9% / 38.6% / 110.0% | 17.4% / 33.1% / 41.2% / 107.0% | 6 / 11 / 13 / 26 | 3 | 16 / 421 |
| 2.5 yrs | 100% | 14.2% / 35.0% / 43.4% / 110.0% | 18.8% / 37.2% / 45.9% / 107.0% | 6 / 12 / 14 / 27 | 3 | 4 / 685 |
| 3.0 yrs ◄ | 100% | 19.0% / 39.7% / 47.0% / 130.5% | 24.0% / 40.3% / 50.0% / 134.5% | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| 4.0 yrs | 100% | 23.7% / 45.0% / 51.6% / 122.0% | 29.7% / 48.8% / 55.5% / 124.3% | 8 / 15 / 18 / 34 | 3 | 6 / 895 |
| 5.0 yrs | 100% | 27.6% / 51.9% / 57.9% / 126.6% | 34.9% / 53.6% / 61.8% / 127.2% | 8 / 17 / 20 / 36 | 3 | 39 / 1220 |
| 6.0 yrs | 100% | 32.9% / 55.9% / 65.0% / 134.0% | 39.1% / 57.5% / 69.4% / 141.1% | 9 / 20 / 22 / 39 | 3 | 62 / 1383 |
| 8.0 yrs | 100% | 43.2% / 63.8% / 75.8% / 147.2% | 55.9% / 68.6% / 82.4% / 150.3% | 10 / 24 / 25 / 42 | 3 | 20 / 2037 |

*◄ = Balanced baseline value. Coverage ratios: capitalisation-window averages (SRR fill to LRR fill). Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSM cov | TCM cov | LRR fill yr | LRR surplus £b | SRR breach covered |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.5 yrs | 12.4% | 13.6% | 9 | 13 | — (no breach) |
| 1.0 yrs | 15.6% | 15.4% | 13 | 108 | — (no breach) |
| 1.5 yrs | 12.5% | 15.4% | 21 | 309 | — (no breach) |
| 2.0 yrs | 13.5% | 17.4% | 25 | 583 | — (no breach) |
| 2.5 yrs | 17.6% | 22.5% | 26 | 1166 | — (no breach) |
| 3.0 yrs ◄ | 20.8% | 27.1% | 29 | 523 | — (no breach) |
| 4.0 yrs | 25.1% | 33.6% | 34 | 2595 | — (no breach) |
| 5.0 yrs | 29.0% | 38.6% | 35 | 2708 | — (no breach) |
| 6.0 yrs | 34.6% | 44.1% | 38 | 5138 | — (no breach) |
| 8.0 yrs | 44.0% | 56.2% | 39 | 150 | — (no breach) |

# C. Reading Notes

**Coverage ratio direction.** SSM and TCM coverage ratios move together when a parameter raises or lowers the rate on the bulk of the distribution. The gap between them (TCM − SSM) measures the sensitivity of revenue to persistent growth heterogeneity; a wide gap means higher-tier taxpayers contribute disproportionately more than the correlated-shock assumption would imply.

**Success rate at 100%.** The Balanced baseline achieves 100% success across all 73 start years. Parameters that reduce revenue significantly may bring the success rate below 100%, meaning the LRR fails to fill within the 71-year window for some historical starting conditions. This is the primary solvency constraint.

**SRR fill year.** Should remain ~3 across most calibrations. If it rises significantly, the refund guarantee becomes credible only after more than one political cycle, which is a materially different political position.

**LRR surplus.** A near-zero surplus at fill (see e.g. the 1953 start year at Balanced parameters, £28b surplus) indicates the mechanism passed its solvency test narrowly. A calibration that systematically reduces surplus increases the risk that a slightly worse return sequence would cause LRR non-fill.

**Pre-behavioural baseline.** All figures are pre-behavioural. Behavioural responses — migration, restructuring, avoidance — are not modelled and will reduce actual revenue by an unknown amount. See RATES §9.1 and BEHAV.

**Joint calibration.** These sweeps vary one parameter at a time. In practice, τ_0 and τ_m jointly determine both the level and shape of revenue; W_min and k jointly determine where in the wealth distribution the gradient falls. A second-order analysis (e.g. a τ_0 × τ_m grid, or a k × W_min grid) would capture interaction effects but is outside this document.

**SRR and LRR interaction.** The SRR and LRR sizing parameters interact: a higher srr_ratio diverts more net income into SRR accumulation before any surplus flows to the LRR, so rising srr_ratio extends the LRR fill year even when lrr_years is held constant. Conversely, a lower srr_ratio accelerates LRR accumulation but leaves a thinner refund buffer. The single-parameter-at-a-time sweeps in §§5–6 capture the first-order effect of each; a joint srr_ratio × lrr_years grid would expose the interaction surface and is a natural second-order extension.

**Rate parameters vs. SWF sizing parameters.** The sweeps in §§1–4 vary the rate function and therefore affect both revenue generation and individual taxpayer burden. The sweeps in §§5–6 vary only the capitalisation thresholds for the SRR and LRR; they do not alter the rate function or any individual tax liability. The burden distribution is therefore invariant across §§5–6 — those panels are flat by design, not an artefact. The sole effect is on when the SWF milestones are reached.

---

*Generated by `rates_param_sweep.py`. Source: `rates_model.py` / `wdt_core.py` / `7_4_…_Params.toml`. No existing project files were modified.*