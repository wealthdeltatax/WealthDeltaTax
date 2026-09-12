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
| 1.02      | 11 August 2026  | Updated data  |

\newpage

# A. Appendix Tables

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

# VAL.S — Appendix Tables

**Generated:** 2026-09-09
**Model:** Python v1.0 via wdt_core.py  ·  Canonical: $\tau_0$=15%, $\tau_m$=70%, k=0.001, $W_{min}$=£2m, N=30, $V_0$=£20m, $g$=10.45%

**Metric (all tables unless stated):** C.1 = (Net($\alpha$) − Net(1)) / TW($\alpha$).  Positive = $\alpha$ pays more net tax than honest.  $\alpha$ = 1.0 row is zero by construction.

**Note on VAL.A alignment:** the live TOML canonical values may differ slightly from the VAL.A §C.1 printed snapshot (generated at a different TOML state). VAL.S uses the live TOML as its reference throughout.

---

## B.1  $\tau_0$ Sweep — C.1 metric across $\alpha$ and $g$

**Metric:** (Net($\alpha$) − Net(1) / TW($\alpha$)  ·  $\tau_m$ = 70%, $k$ = 0.001, N = 30, $V_0$ = £20m.  $\alpha$ = 1.0 row is zero by construction.

### B.1.1  $\tau_0$ = 10%

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 8.88% | 7.89% | 1.43% | 0.85% | 1.01% | 1.32% | 3.29% | 9.52% | 41.34% | 26.10% |
| **0.2** | 7.76% | 6.94% | 1.23% | 0.68% | 0.77% | 0.99% | 2.52% | 7.31% | 29.51% | 17.23% |
| **0.5** | 4.53% | 4.21% | 0.68% | 0.28% | 0.23% | 0.29% | 0.84% | 2.60% | 8.92% | 3.87% |
| **0.8** | 1.50% | 1.63% | 0.24% | 0.06% | -0.00% | -0.01% | 0.06% | 0.35% | 1.25% | 0.25% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.06% | -0.20% | 0.01% | 0.12% | 0.17% | 0.28% | 0.43% | 0.58% | 0.60% |
| **1.5** | 0.00% | -1.02% | -0.43% | 0.15% | 0.52% | 0.70% | 1.31% | 2.30% | 3.56% | 2.34% |
| **1.8** | 0.00% | -0.99% | -0.57% | 0.42% | 1.16% | 1.55% | 3.00% | 5.36% | 8.05% | 4.60% |
| **2.0** | 0.00% | -0.96% | -0.63% | 0.68% | 1.72% | 2.29% | 4.46% | 7.93% | 11.53% | 6.25% |

### B.1.2  $\tau_0$ = 15%  *(canonical)*

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.25% | 11.75% | 1.76% | 0.66% | 0.62% | 0.86% | 2.65% | 7.83% | 30.53% | 25.40% |
| **0.2** | 11.52% | 10.29% | 1.50% | 0.49% | 0.38% | 0.55% | 1.89% | 5.78% | 21.56% | 16.41% |
| **0.5** | 6.64% | 6.15% | 0.81% | 0.13% | -0.06% | -0.04% | 0.36% | 1.67% | 6.08% | 3.18% |
| **0.8** | 2.16% | 2.36% | 0.28% | -0.01% | -0.13% | -0.16% | -0.15% | 0.03% | 0.61% | -0.07% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.44% | -0.23% | 0.09% | 0.26% | 0.33% | 0.49% | 0.66% | 0.87% | 0.93% |
| **1.5** | 0.00% | -1.36% | -0.47% | 0.37% | 0.88% | 1.11% | 1.79% | 2.70% | 3.92% | 3.16% |
| **1.8** | 0.00% | -1.29% | -0.61% | 0.80% | 1.75% | 2.21% | 3.67% | 5.71% | 8.22% | 5.86% |
| **2.0** | 0.00% | -1.24% | -0.66% | 1.16% | 2.45% | 3.10% | 5.21% | 8.13% | 11.49% | 7.76% |

### B.1.3  $\tau_0$ = 20%

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 17.57% | 15.57% | 1.87% | 0.15% | -0.20% | -0.07% | 1.35% | 5.43% | 21.83% | 23.63% |
| **0.2** | 15.20% | 13.56% | 1.58% | 0.03% | -0.35% | -0.29% | 0.72% | 3.73% | 15.12% | 14.85% |
| **0.5** | 8.64% | 8.00% | 0.84% | -0.17% | -0.52% | -0.57% | -0.35% | 0.58% | 3.69% | 2.28% |
| **0.8** | 2.78% | 3.03% | 0.28% | -0.13% | -0.31% | -0.36% | -0.41% | -0.33% | 0.03% | -0.43% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.74% | -0.22% | 0.21% | 0.44% | 0.52% | 0.72% | 0.92% | 1.16% | 1.27% |
| **1.5** | 0.00% | -1.62% | -0.44% | 0.66% | 1.30% | 1.57% | 2.30% | 3.15% | 4.34% | 3.95% |
| **1.8** | 0.00% | -1.50% | -0.55% | 1.25% | 2.39% | 2.89% | 4.36% | 6.18% | 8.54% | 7.03% |
| **2.0** | 0.00% | -1.43% | -0.56% | 1.71% | 3.21% | 3.91% | 5.96% | 8.52% | 11.67% | 9.16% |

### B.1.4  $\tau_0$ = 30%

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 26.08% | 23.05% | 1.54% | -1.68% | -2.85% | -3.04% | -2.56% | -0.31% | 8.28% | 15.44% |
| **0.2** | 22.35% | 19.90% | 1.27% | -1.57% | -2.64% | -2.86% | -2.62% | -1.05% | 4.88% | 8.68% |
| **0.5** | 12.36% | 11.45% | 0.62% | -1.10% | -1.84% | -2.04% | -2.20% | -1.86% | -0.36% | -0.34% |
| **0.8** | 3.89% | 4.24% | 0.19% | -0.48% | -0.80% | -0.90% | -1.06% | -1.11% | -1.03% | -1.25% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -2.17% | -0.13% | 0.53% | 0.87% | 0.99% | 1.25% | 1.48% | 1.77% | 1.94% |
| **1.5** | 0.00% | -1.95% | -0.21% | 1.39% | 2.28% | 2.62% | 3.42% | 4.21% | 5.30% | 5.43% |
| **1.8** | 0.00% | -1.73% | -0.20% | 2.32% | 3.79% | 4.38% | 5.86% | 7.39% | 9.45% | 9.14% |
| **2.0** | 0.00% | -1.59% | -0.14% | 2.98% | 4.85% | 5.62% | 7.60% | 9.69% | 12.41% | 11.60% |

### B.1.5  $\tau_0$ = 40%

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 34.42% | 30.35% | 0.58% | -4.41% | -6.60% | -7.20% | -7.74% | -6.92% | -2.71% | 3.31% |
| **0.2** | 29.21% | 25.96% | 0.44% | -3.89% | -5.82% | -6.37% | -6.97% | -6.49% | -3.67% | -0.19% |
| **0.5** | 15.76% | 14.58% | 0.14% | -2.37% | -3.56% | -3.92% | -4.48% | -4.57% | -4.02% | -3.75% |
| **0.8** | 4.85% | 5.30% | 0.02% | -0.93% | -1.40% | -1.55% | -1.83% | -1.97% | -2.05% | -2.20% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -2.44% | 0.03% | 0.91% | 1.37% | 1.53% | 1.86% | 2.11% | 2.40% | 2.61% |
| **1.5** | 0.00% | -2.11% | 0.15% | 2.24% | 3.37% | 3.78% | 4.68% | 5.43% | 6.40% | 6.79% |
| **1.8** | 0.00% | -1.78% | 0.33% | 3.53% | 5.31% | 5.99% | 7.51% | 8.88% | 10.62% | 10.95% |
| **2.0** | 0.00% | -1.57% | 0.48% | 4.38% | 6.59% | 7.44% | 9.41% | 11.21% | 13.48% | 13.63% |

### B.1.6  $\tau_0$ = 50%

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 42.58% | 37.46% | -0.90% | -7.91% | -11.29% | -12.35% | -13.99% | -14.36% | -12.90% | -9.61% |
| **0.2** | 35.81% | 31.77% | -0.81% | -6.81% | -9.72% | -10.64% | -12.13% | -12.57% | -11.72% | -9.82% |
| **0.5** | 18.88% | 17.45% | -0.53% | -3.90% | -5.58% | -6.13% | -7.09% | -7.54% | -7.62% | -7.55% |
| **0.8** | 5.71% | 6.23% | -0.22% | -1.45% | -2.07% | -2.28% | -2.68% | -2.91% | -3.09% | -3.24% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -2.60% | 0.23% | 1.33% | 1.91% | 2.11% | 2.51% | 2.79% | 3.08% | 3.29% |
| **1.5** | 0.00% | -2.16% | 0.58% | 3.15% | 4.52% | 5.01% | 6.02% | 6.77% | 7.62% | 8.09% |
| **1.8** | 0.00% | -1.72% | 0.95% | 4.79% | 6.89% | 7.66% | 9.27% | 10.53% | 11.99% | 12.59% |
| **2.0** | 0.00% | -1.44% | 1.20% | 5.82% | 8.37% | 9.31% | 11.32% | 12.93% | 14.80% | 15.37% |

## B.2  $\tau_m$ Sweep — C.1 metric across $\alpha$ and $g$

**Metric:** (Net($\alpha$) − Net(1) / TW($\alpha$)  ·  $\tau_0$ = 15%, $k$ = 0.001, N = 30, $V_0$ = £20m.

### B.2.1  $\tau_m$ = 50%

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.25% | 11.73% | 1.71% | 0.55% | 0.41% | 0.57% | 1.83% | 5.05% | 12.75% | 9.31% |
| **0.2** | 11.52% | 10.27% | 1.46% | 0.41% | 0.22% | 0.32% | 1.25% | 3.66% | 9.06% | 5.53% |
| **0.5** | 6.63% | 6.14% | 0.80% | 0.10% | -0.11% | -0.12% | 0.13% | 0.91% | 2.31% | 0.31% |
| **0.8** | 2.16% | 2.36% | 0.28% | -0.02% | -0.14% | -0.17% | -0.18% | -0.10% | 0.01% | -0.45% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.43% | -0.23% | 0.09% | 0.25% | 0.31% | 0.45% | 0.59% | 0.75% | 0.79% |
| **1.5** | 0.00% | -1.36% | -0.49% | 0.33% | 0.81% | 1.01% | 1.57% | 2.21% | 2.76% | 2.30% |
| **1.8** | 0.00% | -1.29% | -0.66% | 0.71% | 1.57% | 1.97% | 3.14% | 4.51% | 5.39% | 3.96% |
| **2.0** | 0.00% | -1.24% | -0.72% | 1.02% | 2.18% | 2.73% | 4.39% | 6.31% | 7.33% | 5.08% |

### B.2.2  $\tau_m$ = 60%

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.25% | 11.74% | 1.74% | 0.61% | 0.53% | 0.73% | 2.29% | 6.53% | 20.43% | 15.02% |
| **0.2** | 11.52% | 10.28% | 1.48% | 0.45% | 0.31% | 0.45% | 1.61% | 4.79% | 14.57% | 9.52% |
| **0.5** | 6.63% | 6.15% | 0.81% | 0.12% | -0.08% | -0.08% | 0.26% | 1.32% | 4.03% | 1.38% |
| **0.8** | 2.16% | 2.36% | 0.28% | -0.02% | -0.13% | -0.16% | -0.16% | -0.03% | 0.29% | -0.32% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.44% | -0.23% | 0.09% | 0.26% | 0.32% | 0.47% | 0.63% | 0.82% | 0.87% |
| **1.5** | 0.00% | -1.36% | -0.48% | 0.35% | 0.85% | 1.07% | 1.69% | 2.48% | 3.35% | 2.71% |
| **1.8** | 0.00% | -1.29% | -0.63% | 0.76% | 1.67% | 2.11% | 3.44% | 5.16% | 6.80% | 4.82% |
| **2.0** | 0.00% | -1.24% | -0.68% | 1.10% | 2.34% | 2.94% | 4.85% | 7.30% | 9.39% | 6.28% |

### B.2.3  $\tau_m$ = 70%  *(canonical)*

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.25% | 11.75% | 1.76% | 0.66% | 0.62% | 0.86% | 2.65% | 7.83% | 30.53% | 25.40% |
| **0.2** | 11.52% | 10.29% | 1.50% | 0.49% | 0.38% | 0.55% | 1.89% | 5.78% | 21.56% | 16.41% |
| **0.5** | 6.64% | 6.15% | 0.81% | 0.13% | -0.06% | -0.04% | 0.36% | 1.67% | 6.08% | 3.18% |
| **0.8** | 2.16% | 2.36% | 0.28% | -0.01% | -0.13% | -0.16% | -0.15% | 0.03% | 0.61% | -0.07% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.44% | -0.23% | 0.09% | 0.26% | 0.33% | 0.49% | 0.66% | 0.87% | 0.93% |
| **1.5** | 0.00% | -1.36% | -0.47% | 0.37% | 0.88% | 1.11% | 1.79% | 2.70% | 3.92% | 3.16% |
| **1.8** | 0.00% | -1.29% | -0.61% | 0.80% | 1.75% | 2.21% | 3.67% | 5.71% | 8.22% | 5.86% |
| **2.0** | 0.00% | -1.24% | -0.66% | 1.16% | 2.45% | 3.10% | 5.21% | 8.13% | 11.49% | 7.76% |

### B.2.4  $\tau_m$ = 80%

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.25% | 11.76% | 1.78% | 0.69% | 0.69% | 0.96% | 2.94% | 8.98% | 43.53% | 53.29% |
| **0.2** | 11.52% | 10.29% | 1.51% | 0.51% | 0.44% | 0.62% | 2.11% | 6.65% | 30.20% | 32.55% |
| **0.5** | 6.64% | 6.16% | 0.82% | 0.14% | -0.04% | -0.01% | 0.45% | 1.99% | 8.43% | 6.69% |
| **0.8** | 2.16% | 2.36% | 0.28% | -0.01% | -0.13% | -0.15% | -0.13% | 0.08% | 0.97% | 0.42% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.44% | -0.22% | 0.10% | 0.27% | 0.33% | 0.50% | 0.69% | 0.92% | 0.96% |
| **1.5** | 0.00% | -1.36% | -0.46% | 0.38% | 0.91% | 1.14% | 1.86% | 2.88% | 4.48% | 3.74% |
| **1.8** | 0.00% | -1.29% | -0.60% | 0.83% | 1.81% | 2.29% | 3.87% | 6.17% | 9.63% | 7.31% |
| **2.0** | 0.00% | -1.24% | -0.64% | 1.20% | 2.54% | 3.22% | 5.51% | 8.84% | 13.60% | 9.89% |

## B.3  $k$ Sweep — C.1 metric across $\alpha$ and $g$

**Metric:** (Net($\alpha$) − Net(1) / TW($\alpha$)  ·  $\tau_0$ = 15%, $\tau_m$ = 70%, N = 30, $V_0$ = £20m.

### B.3.1  $k$ = 0.0001

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.22% | 11.58% | 1.37% | -0.08% | -0.68% | -0.85% | -1.05% | -0.96% | -0.08% | 4.85% |
| **0.2** | 11.50% | 10.14% | 1.20% | -0.08% | -0.61% | -0.76% | -0.95% | -0.90% | -0.22% | 3.60% |
| **0.5** | 6.62% | 6.07% | 0.71% | -0.06% | -0.39% | -0.49% | -0.63% | -0.65% | -0.41% | 1.04% |
| **0.8** | 2.16% | 2.33% | 0.27% | -0.03% | -0.16% | -0.20% | -0.27% | -0.29% | -0.27% | -0.01% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.42% | -0.25% | 0.04% | 0.17% | 0.21% | 0.28% | 0.33% | 0.39% | 0.49% |
| **1.5** | 0.00% | -1.35% | -0.60% | 0.10% | 0.42% | 0.53% | 0.73% | 0.89% | 1.20% | 2.01% |
| **1.8** | 0.00% | -1.28% | -0.92% | 0.17% | 0.69% | 0.86% | 1.21% | 1.53% | 2.23% | 4.31% |
| **2.0** | 0.00% | -1.24% | -1.12% | 0.23% | 0.87% | 1.09% | 1.55% | 1.99% | 3.05% | 6.20% |

### B.3.2  $k$ = 0.0002

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.23% | 11.60% | 1.41% | -0.00% | -0.56% | -0.69% | -0.74% | -0.34% | 2.00% | 16.26% |
| **0.2** | 11.50% | 10.16% | 1.23% | -0.02% | -0.52% | -0.64% | -0.72% | -0.42% | 1.39% | 12.06% |
| **0.5** | 6.62% | 6.08% | 0.72% | -0.04% | -0.36% | -0.45% | -0.55% | -0.48% | 0.18% | 3.87% |
| **0.8** | 2.16% | 2.34% | 0.27% | -0.03% | -0.16% | -0.20% | -0.26% | -0.27% | -0.18% | 0.45% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.43% | -0.25% | 0.04% | 0.18% | 0.22% | 0.30% | 0.37% | 0.47% | 0.62% |
| **1.5** | 0.00% | -1.35% | -0.59% | 0.13% | 0.47% | 0.59% | 0.84% | 1.09% | 1.67% | 3.00% |
| **1.8** | 0.00% | -1.29% | -0.89% | 0.24% | 0.80% | 1.00% | 1.46% | 1.99% | 3.40% | 6.60% |
| **2.0** | 0.00% | -1.24% | -1.07% | 0.33% | 1.03% | 1.30% | 1.92% | 2.68% | 4.80% | 9.46% |

### B.3.3  $k$ = 0.0005

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.24% | 11.66% | 1.54% | 0.24% | -0.15% | -0.16% | 0.34% | 2.05% | 11.62% | 37.87% |
| **0.2** | 11.51% | 10.21% | 1.33% | 0.16% | -0.20% | -0.24% | 0.11% | 1.42% | 8.61% | 26.02% |
| **0.5** | 6.63% | 6.11% | 0.75% | 0.02% | -0.26% | -0.31% | -0.26% | 0.18% | 2.65% | 6.86% |
| **0.8** | 2.16% | 2.34% | 0.27% | -0.02% | -0.15% | -0.19% | -0.22% | -0.18% | 0.20% | 0.68% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.43% | -0.24% | 0.06% | 0.21% | 0.26% | 0.37% | 0.48% | 0.67% | 0.81% |
| **1.5** | 0.00% | -1.36% | -0.55% | 0.22% | 0.62% | 0.78% | 1.18% | 1.71% | 2.95% | 3.63% |
| **1.8** | 0.00% | -1.29% | -0.79% | 0.44% | 1.14% | 1.43% | 2.27% | 3.46% | 6.34% | 7.52% |
| **2.0** | 0.00% | -1.24% | -0.92% | 0.63% | 1.55% | 1.94% | 3.13% | 4.88% | 9.05% | 10.42% |

### B.3.4  $k$ = 0.001  *(canonical)*

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.25% | 11.75% | 1.76% | 0.66% | 0.62% | 0.86% | 2.65% | 7.83% | 30.53% | 25.40% |
| **0.2** | 11.52% | 10.29% | 1.50% | 0.49% | 0.38% | 0.55% | 1.89% | 5.78% | 21.56% | 16.41% |
| **0.5** | 6.64% | 6.15% | 0.81% | 0.13% | -0.06% | -0.04% | 0.36% | 1.67% | 6.08% | 3.18% |
| **0.8** | 2.16% | 2.36% | 0.28% | -0.01% | -0.13% | -0.16% | -0.15% | 0.03% | 0.61% | -0.07% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.44% | -0.23% | 0.09% | 0.26% | 0.33% | 0.49% | 0.66% | 0.87% | 0.93% |
| **1.5** | 0.00% | -1.36% | -0.47% | 0.37% | 0.88% | 1.11% | 1.79% | 2.70% | 3.92% | 3.16% |
| **1.8** | 0.00% | -1.29% | -0.61% | 0.80% | 1.75% | 2.21% | 3.67% | 5.71% | 8.22% | 5.86% |
| **2.0** | 0.00% | -1.24% | -0.66% | 1.16% | 2.45% | 3.10% | 5.21% | 8.13% | 11.49% | 7.76% |

### B.3.5  $k$ = 0.002

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.28% | 11.94% | 2.23% | 1.63% | 2.50% | 3.48% | 9.25% | 23.40% | 34.93% | 18.84% |
| **0.2** | 11.54% | 10.45% | 1.86% | 1.23% | 1.82% | 2.54% | 6.81% | 16.75% | 23.10% | 10.91% |
| **0.5** | 6.65% | 6.24% | 0.94% | 0.38% | 0.43% | 0.64% | 1.99% | 4.79% | 5.26% | 1.19% |
| **0.8** | 2.17% | 2.39% | 0.29% | 0.01% | -0.08% | -0.08% | 0.06% | 0.40% | 0.25% | -0.44% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.45% | -0.19% | 0.16% | 0.38% | 0.47% | 0.71% | 0.91% | 1.01% | 0.99% |
| **1.5** | 0.00% | -1.37% | -0.31% | 0.70% | 1.44% | 1.81% | 2.91% | 3.93% | 3.80% | 2.96% |
| **1.8** | 0.00% | -1.30% | -0.25% | 1.55% | 3.03% | 3.81% | 6.15% | 8.20% | 7.38% | 5.16% |
| **2.0** | 0.00% | -1.24% | -0.11% | 2.28% | 4.34% | 5.44% | 8.73% | 11.48% | 9.98% | 6.65% |

### B.3.6  $k$ = 0.005

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.37% | 12.53% | 3.90% | 5.54% | 11.00% | 15.59% | 32.40% | 34.75% | 18.84% | 19.29% |
| **0.2** | 11.62% | 10.95% | 3.14% | 4.19% | 8.11% | 11.36% | 22.41% | 22.73% | 11.06% | 10.21% |
| **0.5** | 6.69% | 6.51% | 1.38% | 1.36% | 2.43% | 3.32% | 5.84% | 4.92% | 1.11% | 0.85% |
| **0.8** | 2.18% | 2.48% | 0.34% | 0.11% | 0.14% | 0.22% | 0.41% | 0.12% | -0.52% | -0.53% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.49% | -0.09% | 0.39% | 0.71% | 0.84% | 1.08% | 1.12% | 1.09% | 1.04% |
| **1.5** | 0.00% | -1.40% | 0.21% | 1.75% | 3.01% | 3.55% | 4.41% | 4.07% | 3.23% | 3.06% |
| **1.8** | 0.00% | -1.31% | 0.95% | 3.91% | 6.40% | 7.44% | 8.93% | 7.77% | 5.60% | 5.29% |
| **2.0** | 0.00% | -1.25% | 1.68% | 5.70% | 9.10% | 10.49% | 12.32% | 10.42% | 7.21% | 6.79% |

### B.3.7  $k$ = 0.01

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.51% | 13.57% | 7.63% | 15.24% | 28.72% | 34.46% | 32.71% | 20.14% | 18.35% | 19.23% |
| **0.2** | 11.74% | 11.83% | 5.94% | 11.21% | 20.08% | 23.52% | 21.02% | 12.09% | 9.66% | 9.92% |
| **0.5** | 6.76% | 6.98% | 2.31% | 3.43% | 5.36% | 5.87% | 4.16% | 1.32% | 0.48% | 0.64% |
| **0.8** | 2.20% | 2.64% | 0.44% | 0.31% | 0.37% | 0.35% | -0.07% | -0.55% | -0.67% | -0.62% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.56% | 0.11% | 0.72% | 1.06% | 1.15% | 1.21% | 1.19% | 1.18% | 1.14% |
| **1.5** | 0.00% | -1.45% | 1.13% | 3.22% | 4.36% | 4.55% | 4.13% | 3.54% | 3.38% | 3.29% |
| **1.8** | 0.00% | -1.34% | 3.00% | 6.90% | 8.86% | 9.07% | 7.68% | 6.15% | 5.76% | 5.65% |
| **2.0** | 0.00% | -1.25% | 4.63% | 9.80% | 12.25% | 12.42% | 10.19% | 7.92% | 7.35% | 7.24% |

### B.3.8  $k$ = 0.05

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 14.73% | 24.43% | 39.42% | 25.67% | 17.18% | 16.23% | 16.30% | 16.60% | 16.70% | 16.89% |
| **0.2** | 12.78% | 20.78% | 26.31% | 15.52% | 9.26% | 8.21% | 7.35% | 7.15% | 7.09% | 7.25% |
| **0.5** | 7.31% | 11.43% | 6.36% | 1.97% | -0.25% | -0.71% | -1.22% | -1.42% | -1.53% | -1.48% |
| **0.8** | 2.37% | 4.06% | 0.51% | -0.56% | -1.05% | -1.18% | -1.36% | -1.46% | -1.52% | -1.52% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -2.02% | 0.81% | 1.29% | 1.55% | 1.64% | 1.83% | 1.94% | 2.03% | 2.06% |
| **1.5** | 0.00% | -1.66% | 3.23% | 3.77% | 4.20% | 4.42% | 4.91% | 5.22% | 5.47% | 5.56% |
| **1.8** | 0.00% | -1.25% | 6.15% | 6.33% | 6.88% | 7.23% | 8.03% | 8.56% | 8.99% | 9.18% |
| **2.0** | 0.00% | -0.97% | 8.10% | 7.95% | 8.58% | 9.03% | 10.04% | 10.72% | 11.28% | 11.55% |

### B.3.9  $k$ = 0.1

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 16.38% | 43.79% | 25.12% | 15.15% | 14.23% | 14.14% | 13.84% | 13.51% | 13.24% | 13.26% |
| **0.2** | 14.17% | 35.72% | 15.10% | 7.14% | 5.33% | 4.86% | 4.02% | 3.53% | 3.19% | 3.15% |
| **0.5** | 8.06% | 17.69% | 2.11% | -1.41% | -2.67% | -3.06% | -3.79% | -4.24% | -4.59% | -4.72% |
| **0.8** | 2.59% | 5.80% | -0.26% | -1.36% | -1.88% | -2.05% | -2.39% | -2.61% | -2.79% | -2.87% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -2.32% | 0.70% | 1.66% | 2.19% | 2.38% | 2.75% | 2.99% | 3.19% | 3.30% |
| **1.5** | 0.00% | -1.68% | 1.85% | 4.16% | 5.50% | 5.98% | 6.91% | 7.51% | 8.04% | 8.33% |
| **1.8** | 0.00% | -1.05% | 2.84% | 6.42% | 8.53% | 9.27% | 10.74% | 11.69% | 12.54% | 13.01% |
| **2.0** | 0.00% | -0.65% | 3.37% | 7.76% | 10.33% | 11.25% | 13.04% | 14.21% | 15.26% | 15.85% |

## B.4  N Sweep — C.1 metric at four holding periods

**Metric:** (Net($\alpha$,N) − Net(1,N) / TW($\alpha$,N)  ·  $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, $V_0$ = £20m, $g$ = 10.45% throughout.  $\alpha$ = 1.0 row is zero by construction.

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

### B.4.3  N = 30  *(canonical)*

| $\alpha$ | C.1 at $g$ = 10.45% | TW (£m) | Net (£m) | Eff rate |
|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 0.62% | 254.82 | 46.87 | 18.39% |
| **0.2** | 0.38% | 258.51 | 46.28 | 17.90% |
| **0.5** | -0.06% | 269.39 | 45.14 | 16.76% |
| **0.8** | -0.13% | 279.99 | 44.93 | 16.05% |
| **1.0** | 0.00% | 286.91 | 45.29 | 15.79% |
| **1.2** | 0.26% | 293.71 | 46.07 | 15.68% |
| **1.5** | 0.88% | 303.68 | 47.98 | 15.80% |
| **1.8** | 1.75% | 313.40 | 50.77 | 16.20% |
| **2.0** | 2.45% | 319.74 | 53.13 | 16.62% |

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

**Metric:** (Net($\alpha$) − Net(1) / TW($\alpha$) at $g$ = 10.45%.  $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, N = 30.

### B.5.1  $V_0$ = £5m

| $\alpha$ | C.1 | TW (£m) | Net (£m) | Eff rate |
|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 1.84% | 76.78 | 11.98 | 15.60% |
| **0.2** | 0.59% | 71.35 | 10.99 | 15.40% |
| **0.5** | -0.34% | 68.89 | 10.33 | 14.99% |
| **0.8** | -0.16% | 71.55 | 10.45 | 14.61% |
| **1.0** | 0.00% | 73.32 | 10.57 | 14.41% |
| **1.2** | 0.18% | 75.08 | 10.70 | 14.25% |
| **1.5** | 0.49% | 77.72 | 10.95 | 14.09% |
| **1.8** | 0.85% | 80.34 | 11.25 | 14.00% |
| **2.0** | 1.12% | 82.08 | 11.48 | 13.99% |

### B.5.2  $V_0$ = £20m  *(canonical)*

| $\alpha$ | C.1 | TW (£m) | Net (£m) | Eff rate |
|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 0.62% | 254.82 | 46.87 | 18.39% |
| **0.2** | 0.38% | 258.51 | 46.28 | 17.90% |
| **0.5** | -0.06% | 269.39 | 45.14 | 16.76% |
| **0.8** | -0.13% | 279.99 | 44.93 | 16.05% |
| **1.0** | 0.00% | 286.91 | 45.29 | 15.79% |
| **1.2** | 0.26% | 293.71 | 46.07 | 15.68% |
| **1.5** | 0.88% | 303.68 | 47.98 | 15.80% |
| **1.8** | 1.75% | 313.40 | 50.77 | 16.20% |
| **2.0** | 2.45% | 319.74 | 53.13 | 16.62% |

### B.5.3  $V_0$ = £100m

| $\alpha$ | C.1 | TW (£m) | Net (£m) | Eff rate |
|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 10.97% | 1077.07 | 415.99 | 38.62% |
| **0.2** | 8.09% | 1107.26 | 387.39 | 34.99% |
| **0.5** | 2.42% | 1184.11 | 326.46 | 27.57% |
| **0.8** | 0.14% | 1243.72 | 299.52 | 24.08% |
| **1.0** | 0.00% | 1275.94 | 297.82 | 23.34% |
| **1.2** | 0.71% | 1303.45 | 307.13 | 23.56% |
| **1.5** | 3.01% | 1337.88 | 338.16 | 25.28% |
| **1.8** | 6.40% | 1366.29 | 385.32 | 28.20% |
| **2.0** | 9.10% | 1382.79 | 423.70 | 30.64% |

### B.5.4  $V_0$ = £500m

| $\alpha$ | C.1 | TW (£m) | Net (£m) | Eff rate |
|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 29.95% | 3913.50 | 3170.99 | 81.03% |
| **0.2** | 18.74% | 4022.65 | 2752.50 | 68.42% |
| **0.5** | 3.13% | 4192.12 | 2130.18 | 50.81% |
| **0.8** | -0.34% | 4336.01 | 1984.02 | 45.76% |
| **1.0** | 0.00% | 4440.80 | 1998.83 | 45.01% |
| **1.2** | 1.33% | 4553.12 | 2059.27 | 45.23% |
| **1.5** | 4.20% | 4734.28 | 2197.78 | 46.42% |
| **1.8** | 7.48% | 4928.84 | 2367.46 | 48.03% |
| **2.0** | 9.70% | 5065.23 | 2490.15 | 49.16% |

### B.5.5  $V_0$ = £1000m

| $\alpha$ | C.1 | TW (£m) | Net (£m) | Eff rate |
|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 16.38% | 8029.66 | 5247.23 | 65.35% |
| **0.2** | 8.59% | 7571.00 | 4582.84 | 60.53% |
| **0.5** | -0.57% | 7095.22 | 3891.98 | 54.85% |
| **0.8** | -1.15% | 7215.01 | 3849.20 | 53.35% |
| **1.0** | 0.00% | 7424.86 | 3932.20 | 52.96% |
| **1.2** | 1.62% | 7693.30 | 4056.51 | 52.73% |
| **1.5** | 4.33% | 8169.71 | 4286.21 | 52.46% |
| **1.8** | 7.05% | 8708.58 | 4545.76 | 52.20% |
| **2.0** | 8.76% | 9093.91 | 4728.97 | 52.00% |

### B.5.6  $V_0$ = £5000m

| $\alpha$ | C.1 | TW (£m) | Net (£m) | Eff rate |
|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 2.60% | 28514.33 | 18853.47 | 66.12% |
| **0.2** | -6.54% | 25315.03 | 16455.49 | 65.00% |
| **0.5** | -8.66% | 25460.95 | 15906.90 | 62.48% |
| **0.8** | -3.43% | 28529.72 | 17132.60 | 60.05% |
| **1.0** | 0.00% | 30892.14 | 18110.84 | 58.63% |
| **1.2** | 3.02% | 33316.52 | 19116.75 | 57.38% |
| **1.5** | 6.83% | 36985.25 | 20638.68 | 55.80% |
| **1.8** | 9.97% | 40663.12 | 22163.98 | 54.51% |
| **2.0** | 11.76% | 43116.10 | 23181.20 | 53.76% |

### B.5.7  $V_0$ = £10000m

| $\alpha$ | C.1 | TW (£m) | Net (£m) | Eff rate |
|:---:|:---:|:---:|:---:|:---:|
| **0.1** | -8.56% | 47677.88 | 32109.47 | 67.35% |
| **0.2** | -15.18% | 44432.42 | 29443.76 | 66.27% |
| **0.5** | -10.21% | 49500.69 | 31136.82 | 62.90% |
| **0.8** | -3.58% | 56794.30 | 34155.42 | 60.14% |
| **1.0** | 0.00% | 61698.94 | 36189.19 | 58.65% |
| **1.2** | 3.05% | 66605.36 | 38223.74 | 57.39% |
| **1.5** | 6.88% | 73965.29 | 41275.70 | 55.80% |
| **1.8** | 10.01% | 81325.23 | 44327.66 | 54.51% |
| **2.0** | 11.80% | 86231.87 | 46362.31 | 53.76% |

### B.5.8  $V_0$ = £50000m

| $\alpha$ | C.1 | TW (£m) | Net (£m) | Eff rate |
|:---:|:---:|:---:|:---:|:---:|
| **0.1** | -22.99% | 198369.05 | 135344.68 | 68.23% |
| **0.2** | -19.34% | 210361.67 | 140253.10 | 66.67% |
| **0.5** | -10.29% | 247160.60 | 155512.42 | 62.92% |
| **0.8** | -3.58% | 283960.35 | 170772.24 | 60.14% |
| **1.0** | 0.00% | 308493.51 | 180945.46 | 58.65% |
| **1.2** | 3.05% | 333026.68 | 191118.67 | 57.39% |
| **1.5** | 6.88% | 369826.42 | 206378.49 | 55.80% |
| **1.8** | 10.01% | 406626.17 | 221638.32 | 54.51% |
| **2.0** | 11.80% | 431159.33 | 231811.53 | 53.76% |

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

*Canonical cell: $\tau_0$ = 15%, N ceiling = 30.*

## B.7  $k$ × $V_0$ Joint Surface — C.1 Bracket Penalty for $\alpha$ = 1.8

**Metric:** (Net(1.8) − Net(1.0) / TW(1.8) at $g$ = 10.4%, N = 30.  $\tau_0$ = 15%, $\tau_m$ = 70%.  Negative = overstater pays less than honest.

| $k$ \ $V_0$ | £5m | £10m | £20m | £50m | £100m | £200m | £500m |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.0001 | 0.61% | 0.63% | 0.69% | 0.85% | 1.14% | 1.75% | 3.68% |
| 0.0002 | 0.63% | 0.69% | 0.80% | 1.14% | 1.75% | 3.04% | 6.41% |
| 0.0005 | 0.72% | 0.85% | 1.14% | 2.07% | 3.68% | 6.41% | 9.06% |
| 0.001 | 0.85% | 1.14% | 1.75% | 3.68% | 6.40% | 8.86% | 7.48% |
| 0.002 | 1.14% | 1.75% | 3.03% | 6.40% | 8.86% | 8.17% | 7.04% |
| 0.005 | 2.05% | 3.66% | 6.40% | 9.06% | 7.47% | 7.03% | 9.26% |
| 0.01 | 3.65% | 6.39% | 8.86% | 7.46% | 7.01% | 8.72% | 9.97% |
| 0.05 | 9.07% | 7.39% | 6.88% | 9.20% | 9.96% | 10.01% | 10.01% |
| 0.1 | 7.29% | 6.70% | 8.53% | 9.96% | 10.01% | 10.01% | 10.01% |

*Canonical cell: $k$ = 0.001, $V_0$ = £20m.*

## B.8  $W_{min}$ Sweep — C.1 metric across $\alpha$ and $g$

**Metric:** (Net($\alpha$) − Net(1) / TW($\alpha$))  ·  $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, N = 30, $V_0$ = £20m, $g$ = 10.45% throughout.  $W_{min}$ is the entry threshold; $\alpha$ = 1.0 row is zero by construction.

### B.8.1  $W_{min}$ = £0m

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.26% | 11.76% | 1.76% | 0.66% | 0.61% | 0.86% | 2.65% | 7.82% | 30.49% | 25.40% |
| **0.2** | 11.53% | 10.30% | 1.50% | 0.49% | 0.38% | 0.55% | 1.88% | 5.77% | 21.53% | 16.41% |
| **0.5** | 6.64% | 6.16% | 0.81% | 0.13% | -0.06% | -0.04% | 0.36% | 1.67% | 6.07% | 3.18% |
| **0.8** | 2.16% | 2.36% | 0.28% | -0.01% | -0.13% | -0.16% | -0.15% | 0.03% | 0.60% | -0.07% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.44% | -0.23% | 0.09% | 0.26% | 0.33% | 0.49% | 0.66% | 0.87% | 0.93% |
| **1.5** | 0.00% | -1.36% | -0.47% | 0.37% | 0.88% | 1.11% | 1.79% | 2.70% | 3.92% | 3.16% |
| **1.8** | 0.00% | -1.29% | -0.61% | 0.80% | 1.75% | 2.21% | 3.68% | 5.71% | 8.22% | 5.86% |
| **2.0** | 0.00% | -1.24% | -0.66% | 1.16% | 2.45% | 3.10% | 5.22% | 8.13% | 11.49% | 7.76% |

### B.8.2  $W_{min}$ = £1m

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.26% | 11.76% | 1.76% | 0.66% | 0.62% | 0.86% | 2.65% | 7.82% | 30.50% | 25.40% |
| **0.2** | 11.53% | 10.30% | 1.50% | 0.49% | 0.38% | 0.55% | 1.88% | 5.78% | 21.54% | 16.41% |
| **0.5** | 6.64% | 6.16% | 0.81% | 0.13% | -0.06% | -0.04% | 0.36% | 1.67% | 6.07% | 3.18% |
| **0.8** | 2.16% | 2.36% | 0.28% | -0.01% | -0.13% | -0.16% | -0.15% | 0.03% | 0.60% | -0.07% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.44% | -0.23% | 0.09% | 0.26% | 0.33% | 0.49% | 0.66% | 0.87% | 0.93% |
| **1.5** | 0.00% | -1.36% | -0.47% | 0.37% | 0.88% | 1.11% | 1.79% | 2.70% | 3.92% | 3.16% |
| **1.8** | 0.00% | -1.29% | -0.61% | 0.80% | 1.75% | 2.21% | 3.68% | 5.71% | 8.22% | 5.86% |
| **2.0** | 0.00% | -1.24% | -0.66% | 1.16% | 2.45% | 3.10% | 5.22% | 8.13% | 11.49% | 7.76% |

### B.8.3  $W_{min}$ = £2m  *(canonical)*

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 13.25% | 11.75% | 1.76% | 0.66% | 0.62% | 0.86% | 2.65% | 7.83% | 30.53% | 25.40% |
| **0.2** | 11.52% | 10.29% | 1.50% | 0.49% | 0.38% | 0.55% | 1.89% | 5.78% | 21.56% | 16.41% |
| **0.5** | 6.64% | 6.15% | 0.81% | 0.13% | -0.06% | -0.04% | 0.36% | 1.67% | 6.08% | 3.18% |
| **0.8** | 2.16% | 2.36% | 0.28% | -0.01% | -0.13% | -0.16% | -0.15% | 0.03% | 0.61% | -0.07% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.44% | -0.23% | 0.09% | 0.26% | 0.33% | 0.49% | 0.66% | 0.87% | 0.93% |
| **1.5** | 0.00% | -1.36% | -0.47% | 0.37% | 0.88% | 1.11% | 1.79% | 2.70% | 3.92% | 3.16% |
| **1.8** | 0.00% | -1.29% | -0.61% | 0.80% | 1.75% | 2.21% | 3.67% | 5.71% | 8.22% | 5.86% |
| **2.0** | 0.00% | -1.24% | -0.66% | 1.16% | 2.45% | 3.10% | 5.21% | 8.13% | 11.49% | 7.76% |

### B.8.4  $W_{min}$ = £5m

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 0.00% | 11.58% | 2.91% | 2.38% | 2.77% | 3.17% | 6.01% | 13.13% | 37.57% | 27.85% |
| **0.2** | 0.00% | 9.93% | 1.69% | 0.79% | 0.85% | 1.11% | 2.34% | 6.58% | 23.11% | 16.42% |
| **0.5** | 0.00% | 6.14% | 0.81% | 0.13% | -0.05% | -0.04% | 0.37% | 1.68% | 6.10% | 3.19% |
| **0.8** | 0.00% | 2.35% | 0.28% | -0.01% | -0.13% | -0.16% | -0.14% | 0.03% | 0.61% | -0.07% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.43% | -0.23% | 0.09% | 0.26% | 0.33% | 0.49% | 0.66% | 0.87% | 0.93% |
| **1.5** | 0.00% | -1.36% | -0.47% | 0.37% | 0.88% | 1.11% | 1.78% | 2.69% | 3.92% | 3.16% |
| **1.8** | 0.00% | -1.29% | -0.61% | 0.79% | 1.74% | 2.20% | 3.67% | 5.71% | 8.21% | 5.85% |
| **2.0** | 0.00% | -1.24% | -0.66% | 1.15% | 2.44% | 3.09% | 5.21% | 8.13% | 11.49% | 7.75% |

### B.8.5  $W_{min}$ = £10m

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 0.00% | 11.53% | 3.43% | 3.36% | 4.23% | 4.74% | 8.34% | 16.75% | 44.01% | 29.57% |
| **0.2** | 0.00% | 9.90% | 2.21% | 1.93% | 2.32% | 2.66% | 4.98% | 10.52% | 27.50% | 19.58% |
| **0.5** | 0.00% | 6.12% | 0.81% | 0.13% | -0.05% | -0.03% | 0.37% | 1.69% | 6.13% | 3.20% |
| **0.8** | 0.00% | 2.35% | 0.28% | -0.01% | -0.13% | -0.15% | -0.14% | 0.04% | 0.62% | -0.07% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | -1.43% | -0.23% | 0.09% | 0.26% | 0.32% | 0.48% | 0.66% | 0.87% | 0.93% |
| **1.5** | 0.00% | -1.36% | -0.47% | 0.37% | 0.88% | 1.10% | 1.78% | 2.69% | 3.91% | 3.15% |
| **1.8** | 0.00% | -1.29% | -0.61% | 0.79% | 1.74% | 2.19% | 3.66% | 5.70% | 8.21% | 5.83% |
| **2.0** | 0.00% | -1.24% | -0.66% | 1.15% | 2.44% | 3.08% | 5.20% | 8.13% | 11.49% | 7.73% |

### B.8.6  $W_{min}$ = £50m

| $\alpha$ \ $g$ | -4.5% | 0.4% | 5.9% | 8.4% | 10.4% | 11.4% | 13.9% | 16.4% | 20.4% | 25.4% |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **0.1** | 0.00% | 0.00% | 5.61% | 4.42% | 5.58% | 6.72% | 11.73% | 24.36% | 52.03% | 29.91% |
| **0.2** | 0.00% | 0.00% | 4.07% | 2.78% | 3.70% | 4.45% | 7.83% | 15.61% | 35.20% | 20.54% |
| **0.5** | 0.00% | 0.00% | 0.31% | 0.85% | 1.14% | 1.34% | 2.44% | 4.69% | 10.62% | 6.05% |
| **0.8** | 0.00% | 0.00% | 0.05% | 0.09% | 0.19% | 0.23% | 0.27% | 0.67% | 2.50% | 1.09% |
| **1.0** | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| **1.2** | 0.00% | 0.00% | -0.01% | 0.01% | 0.05% | 0.03% | -0.08% | -0.31% | -0.03% | -0.34% |
| **1.5** | 0.00% | 0.00% | 0.23% | 0.34% | 0.48% | 0.54% | 0.69% | 1.31% | 2.15% | 0.59% |
| **1.8** | 0.00% | 0.00% | 0.53% | 0.82% | 1.23% | 1.51% | 2.34% | 3.93% | 5.60% | 2.05% |
| **2.0** | 0.00% | 0.00% | 0.86% | 1.33% | 1.88% | 2.30% | 3.62% | 5.88% | 8.91% | 2.81% |

### B.8.5  N-crossing thresholds by $W_{min}$

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

All figures are generated by the VAL.S output scripts and share `wdt_core.py` as the simulation engine with no modifications.  VAL.A cross-references indicate which (SWEEPS.A §A) or (SWEEPS.A §B) subsection covers the same metric at canonical parameters.

| Fig | File | Title | Axes | Parameters | VAL.A ref |
|:---:|:---:|:---:|:---:|:---:|:---:|
| SS2.1a | val_s_fig_s2_1a_tau0_heatmaps.png | C.1 advantage landscape across $\tau_0$ values — 4-panel heatmap grid | Rows = $\alpha$; cols = $g$; colour = C.1 (pp) | $\tau_m$=70%, k=0.001, N=30, $V_0$=£20m | C.1 |
| SS2.1b | val_s_fig_s2_1b_tau0_n_crossings.png | N-crossing thresholds for $\alpha$ ∈ {1.5,1.8,2.0} as a function of $\tau_0$ | x=$\tau_0$ (%); y=N at crossing; line per $\alpha$ | $\tau_m$=70%, k=0.001, g=10.4% | C.7, B.5.6 |
| SS2.1c | val_s_fig_s2_1c_tau0_tolerant_zone.png | Tolerant-zone $\alpha$ boundaries as a function of $\tau_0$ | x=$\tau_0$ (%); y=$\alpha$; filled band=tolerant zone | k=0.001, N=30, g=10.4% | B.6 |
| SS2.2a | val_s_fig_s2_2a_taum_heatmaps.png | C.1 advantage landscape across $\tau_m$ values — 4-panel heatmap grid | As S2.1a; $\tau_m$ swept across panels | $\tau_0$=15%, k=0.001, N=30 | C.1 |
| SS2.2b | val_s_fig_s2_2b_taum_penalty_plateaus.png | Understater penalty plateau ceiling by $\alpha$ and $\tau_m$ | x=$\alpha$ (understater range); y=plateau ceiling (pp); line per $\tau_m$ | $\tau_0$=15%, k=0.001, N=30 | C.9, B.5.4 |
| SS2.2c | val_s_fig_s2_2c_taum_n_crossings.png | N-crossing thresholds for aggressive overstaters as a function of $\tau_m$ | x=$\tau_m$ (%); y=N at crossing; line per $\alpha$ | $\tau_0$=15%, k=0.001, g=10.4% | C.7, B.5.4 |
| SS2.3a | val_s_fig_s2_3a_k_rate_curves.png | Rate curve $\tau(W)$ overlaid for four $k$ values | x=W (£m, log); y=$\tau(W)$ (%); line per k | $\tau_0$=15%, $\tau_m$=70%, $W_{min}$=£2m | B.3.1 |
| SS2.3b | val_s_fig_s2_3b_k_heatmaps.png | C.1 advantage landscape across $k$ values — 4-panel heatmap grid | As S2.1a; $k$ swept across panels | $\tau_0$=15%, $\tau_m$=70%, N=30 | C.1, C.5 |
| SS2.3c | val_s_fig_s2_3c_k_bracket_penalty.png | Bracket penalty for $\alpha$=1.8 by k and V₀ | x=k; y=C.1 (pp) at $\alpha$=1.8; line per $V_0$ | $\tau_0$=15%, $\tau_m$=70%, N=30 | C.1, B.5.2 |
| SS2.4a | val_s_fig_s2_4a_wmin_rate_curves.png | Rate curve $\tau(W)$ overlaid for four $W_{min}$ values | x=W (£m, log); y=$\tau(W)$ (%); line per $W_{min}$ | $\tau_0$=15%, $\tau_m$=70%, k=0.001 | B.3.1 |
| SS2.4b | val_s_fig_s2_4b_wmin_heatmaps.png | C.1 advantage landscape across $W_{min}$ values — 4-panel heatmap grid | As S2.1a; $W_{min}$ swept across panels | $\tau_0$=15%, k=0.001, N=30 | C.1 |
| SS2.4c | val_s_fig_s2_4c_wmin_n_crossings.png | N-crossing thresholds as a function of $W_{min}$ | x=$W_{min}$ (£m); y=N at crossing; line per $\alpha$ | $\tau_0$=15%, k=0.001, g=10.4% | C.7, B.5.4 |
| SS3.1a | val_s_fig_s3_1a_n_crossing_annotated.png | Overstater advantage erosion and N-crossing thresholds (two-panel) | Left: x=N, y=Net diff £m. Right: bar chart of crossing N. | $\tau_0$=15%, k=0.001, g=10.4% | C.7, B.6 |
| SS3.1b | val_s_fig_s3_1b_n_understater_panels.png | Understater C.1 penalty profile by $g$ at four N values — 4-panel | x=$g$ (%); y=C.1 (pp); line per understater $\alpha$; panel per N | $\tau_0$=15%, k=0.001 | C.9, B.5.3 |
| SS3.1c | val_s_fig_s3_1c_n_tolerant_zone.png | Tolerant-zone $\alpha$ boundaries across N values | x=N (years); y=$\alpha$; filled band=tolerant zone | $\tau_0$=15%, k=0.001, g=10.4% | B.6 |
| SS3.2a | val_s_fig_s3_2a_v0_c1_curves.png | C.1 incentive structure by $V_0$ entry wealth — overlaid curves | x=$\alpha$ (%); y=C.1 (pp); line per $V_0$ | $\tau_0$=15%, k=0.001, N=30 | C.1 |
| SS3.2b | val_s_fig_s3_2b_v0_entry_rate.png | Entry rate $\tau(V_0)$ at four wealth levels on the rate curve | x=W (£m, log); y=$\tau(W)$ (%); markers at $V_0$ levels | $\tau_0$=15%, k=0.001 | B.3.1 |
| SS3.2c | val_s_fig_s3_2c_v0_heatmaps.png | C.1 advantage landscape across $V_0$ wealth levels — 4-panel heatmap grid | As S2.1a; $V_0$ swept across panels | $\tau_0$=15%, k=0.001, N=30 | C.1 |
| SS4.1 | val_s_fig_s4_1_tau0_n_surface.png | Joint surface: N-crossing for $\alpha$=2.0 across ($\tau_0$, N ceiling) | x=$\tau_0$ (%); y=N sweep ceiling; colour=N-crossing; grey=no crossing | $\tau_m$=70%, k=0.001, g=10.4% | C.7, B.6 |
| SS4.2 | val_s_fig_s4_2_k_v0_surface.png | Joint surface: C.1 bracket penalty for $\alpha$=1.8 across (k, $V_0$) | x=$V_0$ (£m); y=k; colour=C.1 (pp); bold border=canonical | $\tau_0$=15%, $\tau_m$=70%, N=30 | C.1, C.5 |
| SS4.3 | val_s_fig_s4_3_calibration_summary.png | Calibration summary — three mechanism properties by parameter variant | Three bar-chart panels: tolerant-zone width, N-crossing (α=1.8), plateau (α=0.1) | N=30, $V_0$=£20m, g=10.4% | B.6, C.9 |

# C. WDT Rate Parameter Sensitivity Sweep

**Run date:** 2026-09-09  
**Model version:** v8 (rates_model.py / wdt_core.py)  
**Headline coverage window:** 10 years (SSMcov10/TCMcov10 columns; change HEADLINE_WINDOW in wdt_analytics.py)  
**Parameters file:** `WDT_Params.toml`  

## ## C.1. Purpose

This document sweeps each of the four WDT rate-function parameters independently, holding the other three at Balanced baseline values, and reports how key transition metrics vary across the full 73-year historical start-year sweep (1947–2019 UK equity return series). It is intended as orientation material for future Governing Council calibration work, not as a scenario recommendation. Parameter interactions are not modelled here; joint sweeps are a natural second-order extension.

### ### C.1.1 The Rate Function

$$\tau(W) = \frac{\tau_m}{1 + \left(\frac{\tau_m - \tau_0}{\tau_0}\right)e^{-k(W - W_{\min})}}, \quad \tau(W) = 0 \text{ if } W < W_{\min}$$

Note: the docstring in `rates_model.py` contains a typographical error writing $(1-\tau_0)/\tau_0$ as the denominator coefficient. The implementation in `wdt_core.tau()` correctly uses $(\tau_m - \tau_0)/\tau_0$.

### ### C.1.2 Balanced Baseline Parameters

| Parameter | Baseline value | Role |
|---|---|---|
| $\tau_0$ (floor rate) | 15% | Marginal rate at W = W_min |
| $\tau_m$ (ceiling rate) | 70% | Asymptotic ceiling |
| k (steepness, per £m) | 0.001 | Controls rate climb speed |
| W_min (£m) | £2.0m | Entry point; below this rate = 0 |

**SWF sizing parameters (Balanced baseline; swept in §§5–6):**

| Parameter | Baseline value | Role |
|---|---|---|
| SRR capitalisation ratio | 3.0× | SRR target sizing |
| LRR floor | 3.0 years of expenditure | Phase Two viability threshold |

**Non-SWF parameters (held constant throughout):**

| Parameter | Value |
|---|---|
| Budget base (£b) | £1,157.4b |
| Budget growth (p.a.) | 4.51% |
| Historical mean return | 10.45% |
| Wealth brackets | 10 |
| Growth tiers | 4 |

### ### C.1.3 Metrics

**Success (v8):** LRR fills within the 71-year modelling window AND the LRR buffer never hits zero (lrr_failure_year is None).

**SSMcov10 / TCMcov10 (headline window):** Average Step-5 coverage fraction over the first 10 post-fill years. SSM applies uniform historical returns (worst-case floor); TCM applies heterogeneous tier differentials (ceiling). The headline window is 10 years; change HEADLINE_WINDOW in wdt_analytics.py to switch all tables and charts simultaneously.

**SSMcov50:** Same metric averaged over 50 post-fill years. Rising values indicate WDT revenue compounds faster than expenditure.

**LRR fail n:** Count of the 73 historical start years where the LRR balance reaches zero within the 71-year modelling window. At Balanced parameters this is 0.

*All distributions are across the 73 historical start years 1947–2019. The 2006 start year is extracted separately as the worst-case historical scenario.*

## ## C.2. Floor Rate (τ_0)

τ_0 sets the marginal rate at W = W_min. A higher floor raises effective rates across the entire taxable population; a lower floor concentrates the rate gradient in the upper distribution.

### ### τ_0 sweep

Other parameters held at Balanced baseline: τ_m = 70%,  k = 0.001,  W_min = £2.0m.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSMcov10 (min/med/mean/max) | TCMcov10 (min/med/mean/max) | SSMcov50 (min/med) | LRR fail n | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 5% | 100% | 1.4% / 111.0% / 97.1% / 160.8% | 9.5% / 122.2% / 110.2% / 198.1% | 0.8% / 4.1% | 0 | 10 / 22 / 24 / 42 | 3 | 10 / 911 |
| 10% | 100% | 9.1% / 105.1% / 115.2% / 261.5% | 15.1% / 121.7% / 120.7% / 291.9% | 0.9% / 4.2% | 0 | 8 / 16 / 18 / 34 | 3 | 27 / 886 |
| 15% ◄ | 100% | 6.4% / 122.1% / 126.0% / 287.9% | 14.6% / 125.5% / 138.8% / 321.4% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| 20% | 100% | 13.1% / 130.4% / 136.9% / 302.3% | 19.6% / 140.1% / 151.8% / 335.6% | 1.0% / 4.4% | 0 | 6 / 12 / 14 / 27 | 3 | 13 / 908 |
| 25% | 100% | 11.0% / 138.5% / 146.8% / 348.3% | 24.6% / 121.6% / 161.8% / 375.9% | 1.2% / 4.6% | 0 | 6 / 11 / 13 / 26 | 3 | 77 / 692 |
| 30% | 100% | 20.8% / 116.9% / 155.5% / 386.4% | 21.6% / 137.6% / 173.9% / 417.3% | 1.1% / 4.4% | 0 | 5 / 10 / 12 / 25 | 3 | 4 / 822 |
| 35% | 100% | 12.5% / 130.2% / 169.5% / 382.6% | 28.2% / 146.9% / 188.4% / 450.3% | 1.2% / 4.2% | 0 | 5 / 10 / 11 / 24 | 3 | 37 / 1095 |
| 40% | 100% | 17.9% / 132.6% / 177.4% / 408.4% | 34.2% / 146.8% / 195.1% / 476.0% | 1.2% / 4.0% | 0 | 5 / 10 / 11 / 24 | 3 | 30 / 1124 |
| 45% | 100% | 15.6% / 139.8% / 184.0% / 431.7% | 28.8% / 158.4% / 201.7% / 497.2% | 1.3% / 3.9% | 0 | 5 / 9 / 10 / 21 | 3 | 8 / 849 |
| 50% | 100% | 20.6% / 135.9% / 187.0% / 451.5% | 33.9% / 167.0% / 208.6% / 474.6% | 1.3% / 3.8% | 0 | 5 / 9 / 10 / 20 | 3 | 24 / 688 |

*◄ = Balanced baseline value. SSMcov10/TCMcov10: Step-5 coverage fraction averaged over 10 post-fill years. SSMcov50: 50yr window showing long-run trajectory. LRR fail n: start years where LRR buffer hits zero within 71-year window. Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSMcov10 | TCMcov10 | LRR fill yr | LRR surplus £b | LRR failure yr |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 5% | 109.1% | 104.6% | 39 | 1595 | — (no failure) |
| 10% | 94.7% | 65.2% | 34 | 1229 | — (no failure) |
| 15% ◄ | 58.0% | 54.7% | 29 | 523 | — (no failure) |
| 20% | 42.8% | 75.0% | 26 | 1999 | — (no failure) |
| 25% | 58.0% | 46.1% | 25 | 973 | — (no failure) |
| 30% | 70.6% | 56.0% | 25 | 2606 | — (no failure) |
| 35% | 41.9% | 66.2% | 21 | 411 | — (no failure) |
| 40% | 49.4% | 74.5% | 21 | 1277 | — (no failure) |
| 45% | 56.4% | 81.6% | 21 | 2075 | — (no failure) |
| 50% | 64.5% | 59.8% | 20 | 434 | — (no failure) |

## ## C.3. Ceiling Rate (τ_m)

τ_m is the asymptotic ceiling the marginal rate approaches but never reaches. Its primary effect is on the top brackets where W >> W_min.

### ### τ_m sweep

Other parameters held at Balanced baseline: τ_0 = 15%,  k = 0.001,  W_min = £2.0m.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSMcov10 (min/med/mean/max) | TCMcov10 (min/med/mean/max) | SSMcov50 (min/med) | LRR fail n | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 50% | 100% | 6.3% / 121.8% / 125.8% / 287.3% | 14.6% / 125.1% / 138.5% / 320.5% | 0.9% / 4.3% | 0 | 7 / 13 / 15 / 29 | 3 | 3 / 911 |
| 55% | 100% | 6.4% / 121.9% / 125.8% / 287.5% | 14.6% / 125.2% / 138.6% / 320.8% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 4 / 914 |
| 60% | 100% | 6.4% / 122.0% / 125.9% / 287.7% | 14.6% / 125.3% / 138.7% / 321.0% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 4 / 916 |
| 65% | 100% | 6.4% / 122.1% / 126.0% / 287.8% | 14.6% / 125.4% / 138.8% / 321.2% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 5 / 918 |
| 70% ◄ | 100% | 6.4% / 122.1% / 126.0% / 287.9% | 14.6% / 125.5% / 138.8% / 321.4% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| 75% | 100% | 6.4% / 122.2% / 126.1% / 288.0% | 14.7% / 125.6% / 138.9% / 321.5% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 6 / 920 |
| 80% | 100% | 6.4% / 122.2% / 126.1% / 288.1% | 14.7% / 125.6% / 138.9% / 321.7% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 7 / 921 |
| 85% | 100% | 6.4% / 122.3% / 126.1% / 288.2% | 14.7% / 125.7% / 139.0% / 321.8% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 7 / 922 |
| 90% | 100% | 6.4% / 122.3% / 126.2% / 288.3% | 14.7% / 125.7% / 139.0% / 321.9% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 7 / 923 |
| 95% | 100% | 6.4% / 122.3% / 126.2% / 288.4% | 14.7% / 125.7% / 139.1% / 322.0% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 8 / 924 |
| 100% | 100% | 6.4% / 122.4% / 126.2% / 288.4% | 14.7% / 125.8% / 139.1% / 322.0% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 8 / 925 |

*◄ = Balanced baseline value. SSMcov10/TCMcov10: Step-5 coverage fraction averaged over 10 post-fill years. SSMcov50: 50yr window showing long-run trajectory. LRR fail n: start years where LRR buffer hits zero within 71-year window. Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSMcov10 | TCMcov10 | LRR fill yr | LRR surplus £b | LRR failure yr |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 50% | 57.8% | 54.5% | 29 | 514 | — (no failure) |
| 55% | 57.9% | 54.6% | 29 | 517 | — (no failure) |
| 60% | 57.9% | 54.6% | 29 | 519 | — (no failure) |
| 65% | 57.9% | 54.7% | 29 | 521 | — (no failure) |
| 70% ◄ | 58.0% | 54.7% | 29 | 523 | — (no failure) |
| 75% | 58.0% | 54.7% | 29 | 524 | — (no failure) |
| 80% | 58.0% | 54.7% | 29 | 525 | — (no failure) |
| 85% | 58.0% | 54.8% | 29 | 526 | — (no failure) |
| 90% | 58.0% | 54.8% | 29 | 527 | — (no failure) |
| 95% | 58.0% | 54.8% | 29 | 528 | — (no failure) |
| 100% | 58.1% | 54.8% | 29 | 529 | — (no failure) |

## ## C.4. Steepness (k)

k (per £m) controls how rapidly the marginal rate climbs from τ_0 toward τ_m. Low k produces a shallow gradient; high k produces a steep step.

### ### k sweep (log-spaced)

Other parameters held at Balanced baseline: τ_0 = 15%,  τ_m = 70%,  W_min = £2.0m.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSMcov10 (min/med/mean/max) | TCMcov10 (min/med/mean/max) | SSMcov50 (min/med) | LRR fail n | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.0001 | 100% | 6.2% / 119.9% / 124.1% / 283.1% | 16.6% / 122.8% / 136.8% / 315.3% | 0.9% / 3.7% | 0 | 7 / 13 / 15 / 29 | 3 | 14 / 859 |
| 0.0002 | 100% | 6.2% / 120.2% / 124.3% / 283.7% | 16.6% / 123.1% / 137.1% / 316.0% | 0.9% / 3.8% | 0 | 7 / 13 / 15 / 29 | 3 | 17 / 866 |
| 0.0005 | 100% | 6.3% / 120.9% / 125.0% / 285.3% | 14.4% / 124.0% / 137.5% / 318.1% | 0.9% / 4.1% | 0 | 7 / 13 / 15 / 29 | 3 | 29 / 886 |
| 0.0010 ◄ | 100% | 6.4% / 122.1% / 126.0% / 287.9% | 14.6% / 125.5% / 138.8% / 321.4% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| 0.0020 | 100% | 6.6% / 124.5% / 127.9% / 292.9% | 15.1% / 127.9% / 139.9% / 322.7% | 1.0% / 4.8% | 0 | 7 / 13 / 15 / 29 | 3 | 0 / 939 |
| 0.0050 | 100% | 7.3% / 129.9% / 131.3% / 306.1% | 16.2% / 130.9% / 143.8% / 338.9% | 1.1% / 5.6% | 0 | 6 / 13 / 15 / 29 | 3 | 22 / 727 |
| 0.0100 | 100% | 8.4% / 131.1% / 135.7% / 324.9% | 17.9% / 139.9% / 151.6% / 361.6% | 1.2% / 6.2% | 0 | 6 / 13 / 15 / 29 | 3 | 4 / 718 |
| 0.0500 | 100% | 11.2% / 152.4% / 155.9% / 342.1% | 24.7% / 155.5% / 179.1% / 468.9% | 1.7% / 6.6% | 0 | 6 / 12 / 14 / 27 | 3 | 3 / 845 |
| 0.1000 | 100% | 13.8% / 170.8% / 174.9% / 396.1% | 21.9% / 164.9% / 196.9% / 446.6% | 1.7% / 6.1% | 0 | 6 / 12 / 14 / 27 | 3 | 70 / 1067 |

*◄ = Balanced baseline value. SSMcov10/TCMcov10: Step-5 coverage fraction averaged over 10 post-fill years. SSMcov50: 50yr window showing long-run trajectory. LRR fail n: start years where LRR buffer hits zero within 71-year window. Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSMcov10 | TCMcov10 | LRR fill yr | LRR surplus £b | LRR failure yr |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.0001 | 56.9% | 52.4% | 29 | 457 | — (no failure) |
| 0.0002 | 57.0% | 52.5% | 29 | 464 | — (no failure) |
| 0.0005 | 57.4% | 54.0% | 29 | 486 | — (no failure) |
| 0.0010 ◄ | 58.0% | 54.7% | 29 | 523 | — (no failure) |
| 0.0020 | 59.1% | 56.0% | 29 | 596 | — (no failure) |
| 0.0050 | 62.2% | 59.4% | 29 | 809 | — (no failure) |
| 0.0100 | 66.7% | 64.2% | 29 | 1136 | — (no failure) |
| 0.0500 | 44.4% | 88.4% | 26 | 1442 | — (no failure) |
| 0.1000 | 55.2% | 105.0% | 26 | 2820 | — (no failure) |

## ## C.5. Entry Point (W_min)

W_min (£m) is the wealth level below which the rate function produces zero liability. It is a rate design parameter, not a population boundary.

### ### W_min sweep

Other parameters held at Balanced baseline: τ_0 = 15%,  τ_m = 70%,  k = 0.001.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSMcov10 (min/med/mean/max) | TCMcov10 (min/med/mean/max) | SSMcov50 (min/med) | LRR fail n | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| £0.1m | 100% | 8.4% / 85.0% / 96.7% / 242.4% | 13.5% / 81.0% / 112.6% / 263.9% | 0.7% / 3.6% | 0 | 6 / 10 / 12 / 26 | 3 | 1 / 557 |
| £0.25m | 100% | 8.4% / 85.0% / 96.7% / 242.3% | 13.5% / 81.0% / 112.6% / 263.9% | 0.7% / 3.6% | 0 | 6 / 10 / 12 / 26 | 3 | 1 / 557 |
| £0.5m | 100% | 6.7% / 86.6% / 97.7% / 242.4% | 13.6% / 81.0% / 113.1% / 264.2% | 0.7% / 3.6% | 0 | 6 / 11 / 12 / 26 | 3 | 49 / 545 |
| £1.0m | 100% | 10.0% / 95.1% / 104.8% / 247.5% | 12.0% / 106.0% / 119.8% / 267.3% | 0.8% / 3.9% | 0 | 6 / 11 / 13 / 27 | 3 | 2 / 895 |
| £2.0m ◄ | 100% | 6.4% / 122.1% / 126.0% / 287.9% | 14.6% / 125.5% / 138.8% / 321.4% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| £3.0m | 100% | 10.9% / 133.4% / 142.8% / 290.2% | 15.5% / 148.5% / 152.0% / 318.3% | 1.1% / 4.8% | 0 | 8 / 15 / 17 / 33 | 3 | 52 / 976 |
| £5.0m | 100% | 11.7% / 157.2% / 173.0% / 348.2% | 23.7% / 176.4% / 188.4% / 395.6% | 1.3% / 5.2% | 0 | 9 / 18 / 20 / 35 | 3 | 72 / 1210 |
| £7.5m | 100% | 11.7% / 225.9% / 194.9% / 392.8% | 24.8% / 206.3% / 210.5% / 453.0% | 1.5% / 5.7% | 0 | 10 / 21 / 22 / 37 | 3 | 12 / 1001 |
| £10.0m | 100% | 11.1% / 249.0% / 217.6% / 431.2% | 25.4% / 229.1% / 231.1% / 506.6% | 1.9% / 6.4% | 0 | 11 / 22 / 24 / 39 | 3 | 79 / 1250 |

*◄ = Balanced baseline value. SSMcov10/TCMcov10: Step-5 coverage fraction averaged over 10 post-fill years. SSMcov50: 50yr window showing long-run trajectory. LRR fail n: start years where LRR buffer hits zero within 71-year window. Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSMcov10 | TCMcov10 | LRR fill yr | LRR surplus £b | LRR failure yr |
|:---:|:---:|:---:|:---:|:---:|:---:|
| £0.1m | 34.1% | 58.6% | 25 | 267 | — (no failure) |
| £0.25m | 34.1% | 58.5% | 25 | 266 | — (no failure) |
| £0.5m | 34.0% | 58.6% | 25 | 207 | — (no failure) |
| £1.0m | 32.2% | 58.1% | 26 | 1779 | — (no failure) |
| £2.0m ◄ | 58.0% | 54.7% | 29 | 523 | — (no failure) |
| £3.0m | 103.0% | 49.1% | 32 | 961 | — (no failure) |
| £5.0m | 149.4% | 90.1% | 35 | 4518 | — (no failure) |
| £7.5m | 142.3% | 166.1% | 35 | 115 | — (no failure) |
| £10.0m | 241.3% | 228.4% | 38 | 2710 | — (no failure) |

## ## C.6. SRR Capitalisation Ratio (srr_ratio)

srr_ratio sets the SRR capitalisation target as a multiple of average annual net WDT income. Affects milestone timing only; does not alter individual taxpayer burden.

### ### srr_ratio sweep

Other parameters held at Balanced baseline: τ_0=15%, τ_m=70%, k=0.001, W_min=£2.0m, lrr_years=3.0.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSMcov10 (min/med/mean/max) | TCMcov10 (min/med/mean/max) | SSMcov50 (min/med) | LRR fail n | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1.0× | 100% | 7.5% / 124.4% / 120.2% / 279.2% | 18.3% / 125.5% / 132.5% / 307.1% | 0.9% / 4.3% | 0 | 5 / 12 / 14 / 28 | 1 | 10 / 641 |
| 1.5× | 100% | 6.9% / 121.8% / 120.0% / 269.4% | 16.8% / 124.1% / 134.6% / 299.6% | 0.9% / 4.2% | 0 | 6 / 12 / 14 / 28 | 2 | 0 / 580 |
| 2.0× | 100% | 9.6% / 119.2% / 121.6% / 263.1% | 16.2% / 126.6% / 134.8% / 289.6% | 1.0% / 4.4% | 0 | 6 / 13 / 15 / 29 | 2 | 17 / 654 |
| 2.5× | 100% | 7.2% / 116.6% / 122.1% / 261.5% | 16.0% / 126.8% / 138.6% / 329.0% | 1.0% / 4.5% | 0 | 6 / 13 / 15 / 29 | 3 | 17 / 657 |
| 3.0× ◄ | 100% | 6.4% / 122.1% / 126.0% / 287.9% | 14.6% / 125.5% / 138.8% / 321.4% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| 4.0× | 100% | 6.8% / 125.2% / 125.4% / 270.5% | 15.3% / 130.8% / 140.2% / 368.7% | 1.1% / 4.4% | 0 | 8 / 14 / 16 / 29 | 4 | 28 / 956 |
| 5.0× | 100% | 9.0% / 119.8% / 125.4% / 311.8% | 16.1% / 141.4% / 142.5% / 352.2% | 1.1% / 4.4% | 0 | 8 / 15 / 17 / 30 | 5 | 2 / 831 |
| 6.0× | 100% | 12.6% / 114.4% / 126.2% / 293.3% | 17.9% / 139.5% / 143.1% / 324.1% | 1.1% / 4.4% | 0 | 9 / 16 / 18 / 31 | 6 | 31 / 840 |
| 8.0× | 100% | 15.1% / 119.1% / 134.8% / 297.6% | 21.7% / 139.7% / 151.4% / 382.6% | 1.3% / 4.3% | 0 | 11 / 17 / 19 / 33 | 8 | 4 / 1026 |
| 10.0× | 100% | 16.7% / 125.2% / 135.0% / 297.0% | 24.1% / 143.5% / 158.1% / 370.4% | 1.4% / 4.3% | 0 | 13 / 19 / 21 / 34 | 10 | 2 / 1073 |

*◄ = Balanced baseline value. SSMcov10/TCMcov10: Step-5 coverage fraction averaged over 10 post-fill years. SSMcov50: 50yr window showing long-run trajectory. LRR fail n: start years where LRR buffer hits zero within 71-year window. Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSMcov10 | TCMcov10 | LRR fill yr | LRR surplus £b | LRR failure yr |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 1.0× | 31.3% | 61.1% | 26 | 282 | — (no failure) |
| 1.5× | 30.2% | 59.5% | 26 | 67 | — (no failure) |
| 2.0× | 60.7% | 57.9% | 29 | 1002 | — (no failure) |
| 2.5× | 59.3% | 56.3% | 29 | 762 | — (no failure) |
| 3.0× ◄ | 58.0% | 54.7% | 29 | 523 | — (no failure) |
| 4.0× | 55.1% | 50.7% | 29 | 43 | — (no failure) |
| 5.0× | 62.5% | 47.8% | 30 | 1146 | — (no failure) |
| 6.0× | 59.5% | 44.8% | 30 | 601 | — (no failure) |
| 8.0× | 86.8% | 62.6% | 32 | 768 | — (no failure) |
| 10.0× | 108.9% | 71.6% | 34 | 2489 | — (no failure) |

## ## C.7. LRR Floor (lrr_years)

lrr_years sets the LRR floor as a multiple of prevailing government expenditure (growing at 4.51% p.a.). Affects LRR milestone timing only.

### ### lrr_years sweep

Other parameters held at Balanced baseline: τ_0=15%, τ_m=70%, k=0.001, W_min=£2.0m, srr_ratio=3.0×.

**Sweep summary — distributions across 73 historical start years**

| Value | Success% | SSMcov10 (min/med/mean/max) | TCMcov10 (min/med/mean/max) | SSMcov50 (min/med) | LRR fail n | LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.5 yrs | 100% | 7.5% / 48.9% / 70.3% / 196.6% | 12.5% / 63.8% / 83.7% / 250.1% | 0.7% / 2.4% | 0 | 4 / 6 / 7 / 12 | 3 | 3 / 192 |
| 1.0 yrs | 100% | 7.2% / 55.4% / 79.7% / 232.6% | 11.8% / 64.8% / 94.8% / 251.4% | 0.7% / 3.2% | 0 | 5 / 8 / 9 / 19 | 3 | 4 / 311 |
| 1.5 yrs | 100% | 7.2% / 72.5% / 95.9% / 228.6% | 15.9% / 80.0% / 107.2% / 276.4% | 0.8% / 3.8% | 0 | 5 / 10 / 11 / 24 | 3 | 6 / 582 |
| 2.0 yrs | 100% | 7.7% / 94.4% / 102.7% / 250.9% | 16.6% / 85.4% / 115.6% / 276.0% | 0.9% / 3.8% | 0 | 6 / 11 / 13 / 26 | 3 | 16 / 421 |
| 2.5 yrs | 100% | 8.9% / 115.7% / 113.8% / 248.7% | 15.9% / 117.2% / 126.6% / 321.9% | 1.0% / 4.1% | 0 | 6 / 12 / 14 / 27 | 3 | 4 / 685 |
| 3.0 yrs ◄ | 100% | 6.4% / 122.1% / 126.0% / 287.9% | 14.6% / 125.5% / 138.8% / 321.4% | 1.0% / 4.4% | 0 | 7 / 13 / 15 / 29 | 3 | 6 / 919 |
| 4.0 yrs | 100% | 8.9% / 133.1% / 144.6% / 280.8% | 15.1% / 157.8% / 157.1% / 387.3% | 1.0% / 4.6% | 0 | 8 / 15 / 18 / 34 | 3 | 6 / 895 |
| 5.0 yrs | 100% | 12.2% / 141.4% / 159.1% / 341.5% | 19.6% / 180.7% / 190.1% / 385.5% | 1.1% / 4.8% | 0 | 8 / 17 / 20 / 36 | 3 | 39 / 1220 |
| 6.0 yrs | 100% | 8.0% / 207.1% / 179.9% / 329.5% | 19.6% / 203.4% / 201.4% / 373.3% | 1.2% / 4.9% | 0 | 9 / 20 / 22 / 39 | 3 | 62 / 1383 |
| 8.0 yrs | 100% | 4.2% / 234.8% / 216.4% / 407.0% | 13.4% / 292.6% / 244.0% / 476.8% | 1.3% / 5.3% | 0 | 10 / 24 / 25 / 42 | 3 | 20 / 2037 |

*◄ = Balanced baseline value. SSMcov10/TCMcov10: Step-5 coverage fraction averaged over 10 post-fill years. SSMcov50: 50yr window showing long-run trajectory. LRR fail n: start years where LRR buffer hits zero within 71-year window. Distributions across all 73 historical start years 1947–2019.*

**2006 start year (worst-case historical scenario)**

| Value | SSMcov10 | TCMcov10 | LRR fill yr | LRR surplus £b | LRR failure yr |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.5 yrs | 7.5% | 14.4% | 9 | 13 | — (no failure) |
| 1.0 yrs | 7.2% | 14.0% | 13 | 108 | — (no failure) |
| 1.5 yrs | 23.2% | 40.2% | 21 | 309 | — (no failure) |
| 2.0 yrs | 40.7% | 34.1% | 25 | 583 | — (no failure) |
| 2.5 yrs | 33.5% | 61.3% | 26 | 1166 | — (no failure) |
| 3.0 yrs ◄ | 58.0% | 54.7% | 29 | 523 | — (no failure) |
| 4.0 yrs | 126.8% | 86.9% | 34 | 2595 | — (no failure) |
| 5.0 yrs | 126.9% | 148.6% | 35 | 2708 | — (no failure) |
| 6.0 yrs | 202.0% | 193.2% | 38 | 5138 | — (no failure) |
| 8.0 yrs | 210.7% | 349.1% | 39 | 150 | — (no failure) |

## ## C.8. Mean Growth Rate (g)

Each row is a single deterministic run with a constant growth rate replacing the historical return series. There is no start-year distribution; the columns show point values from one SSM pass. The hist_mean value (10.45%) appears in the table as the canonical historical baseline.

**g sweep — deterministic constant-g scenarios**

*◄ = hist_mean (canonical). No start-year distribution; one SSM/TCM run per value.*

| Value | LRR fill yr | LRR surplus £b | SSMcov10 | TCMcov10 | SSMcov50 | LRR failure yr |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 3.00% | — | 0 | — | — | — | — (none) |
| 5.00% | 35 | 24 | 8.7% | 21.4% | 8.6% | — (none) |
| 7.00% | 20 | 487 | 33.0% | 45.0% | 53.2% | — (none) |
| 8.45% | 16 | 684 | 53.2% | 65.8% | 117.2% | — (none) |
| 10.45% ◄ | 12 | 103 | 77.4% | 95.5% | 290.2% | — (none) |
| 12.00% | 11 | 663 | 110.8% | 131.1% | 609.4% | — (none) |
| 15.00% | 9 | 1007 | 177.7% | 199.3% | 2371.0% | — (none) |
| 20.00% | 7 | 751 | 322.7% | 349.4% | 17959.0% | — (none) |
| 25.00% | 6 | 979 | 547.5% | 715.4% | 83131.7% | — (none) |

## ## C.9. Synthetic Growth Scenario

Growth path: $g(t) = \mu + \lambda t + A \sin(2\pi t / T)$  ·  Canonical: μ=7.00%, λ=0.0000/yr, A=8.00%, T=10 yr.

### ### C.9.1  Amplitude sweep (μ, λ, T fixed at canonical)
λ=0.0000, μ=7.00%, T=10 yr.

**Amplitude sweep**

*A=0 degenerates to a linear-trend-only scenario.*

| Value | LRR fill yr | LRR surplus £b | SSMcov10 | TCMcov10 | SSMcov50 | LRR failure yr |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0.00% | 20 | 487 | 33.0% | 45.0% | 53.2% | — (none) |
| 1.00% | 20 | 466 | 33.1% | 45.7% | 53.7% | — (none) |
| 2.00% | 20 | 399 | 33.1% | 42.7% | 54.1% | — (none) |
| 3.00% | 20 | 451 | 33.8% | 43.7% | 54.3% | — (none) |
| 4.00% | 20 | 378 | 33.7% | 42.5% | 54.4% | — (none) |
| 5.00% | 20 | 356 | 33.7% | 44.2% | 54.2% | — (none) |
| 6.00% | 20 | 271 | 33.4% | 43.4% | 54.0% | — (none) |
| 8.00% ◄ | 20 | 74 | 33.5% | 42.7% | 54.8% | — (none) |

### ### C.9.2  Period sweep (μ, λ, A fixed at canonical)
λ=0.0000, μ=7.00%, A=8.00%.

**Period sweep**

*Shorter periods produce more volatile annual revenue; longer periods approach the linear-trend limit.*

| Value | LRR fill yr | LRR surplus £b | SSMcov10 | TCMcov10 | SSMcov50 | LRR failure yr |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 5 yr | 20 | 47 | 31.8% | 47.1% | 52.2% | — (none) |
| 7 yr | 17 | 398 | 23.9% | 38.5% | 52.0% | — (none) |
| 10 yr ◄ | 20 | 74 | 33.5% | 42.7% | 54.8% | — (none) |
| 15 yr | 18 | 1154 | 35.5% | 50.8% | 64.8% | — (none) |
| 20 yr | 11 | 54 | 4.3% | 11.7% | 45.5% | — (none) |
| 30 yr | 10 | 585 | 46.2% | 56.6% | 49.9% | — (none) |

# C. Reading Notes

**Coverage window direction.** SSMcov and TCMcov move together when a parameter raises or lowers revenue. The SSM–TCM gap measures sensitivity to persistent growth heterogeneity. The 50yr window is typically larger than the headline window because WDT revenue compounds on a growing wealth base.

**LRR failure vs. non-fill.** Two distinct failure modes: (1) LRR never fills — the mechanism does not reach Phase Two; (2) LRR fails post-fill — the buffer is later exhausted. Both are solvency constraints.

**Success rate at 100%.** The Balanced baseline achieves 100% success across all 73 start years. Parameters that reduce revenue may bring the success rate below 100%.

**Pre-behavioural baseline.** All figures are pre-behavioural. Behavioural responses — migration, restructuring, avoidance — are not modelled. See RATES §9.1 and BEHAV.

**Joint calibration.** These sweeps vary one parameter at a time. In practice, τ_0 and τ_m jointly determine revenue level and shape; W_min and k jointly determine the gradient location.

---

*Generated by `16_6_RATES_S_tables.py` from `sweep_cache.json`. Source: `rates_model.py` / `wdt_core.py` / `WDT_Params.toml`. No existing project files were modified.*