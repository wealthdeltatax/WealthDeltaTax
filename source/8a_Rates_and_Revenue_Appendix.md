---
title: "The Wealth Delta Tax: Rates and Revenue Appendix"
shortcode: "RATES.A"
status: "active"
keywords:
    - Wealth Delta Tax
    - wealth taxation
    - revenue modelling
    - accrual taxation
    - fiscal simulation
    - Sovereign Wealth Fund solvency
    - reserve capitalisation
    - historical return simulation
    - correlated shocks
    - heterogeneous returns
    - taxpayer cohort model
    - reproducible modelling
    - Python simulation
---

### Revision History {.unnumbered .unlisted}

| Revision | Date            | Details                  |
|:--------:|:---------------:|--------------------------|
| 0.01      | 31 July 2026     | First Draft          |
| 1.00      | 15 August 2026  | Published to website |
| 1.01      | 31 August 2026  | Corrected TCM coverage ratio prose (27.7% → 27.4%) and minimum-coverage start-year attribution (2003 → 2005) in §A.6 to match §B.3.9 model output |

\newpage

# A. Model Specification

## A.1 Purpose

RATES rests on four computational components, each answering a distinct question about the WDT mechanism.

The SWF Solvency Model (SSM) is a transition-planning instrument. Under the correlated-shock assumption (every taxpayer experiencing the same return simultaneously, maximising refund pressure and minimising net income), it tracks year-by-year capitalisation of the two internal reserves and establishes how long the mechanism takes to reach self-sufficiency. It asks whether the mechanism survives; it does not forecast expected revenue.

The Taxpayer Cohort Model (TCM) evaluates individual taxpayer experience in cumulative tax and refund flows given persistent heterogeneous return differentials, and derives aggregate revenue from those flows. It is calibrated to the LRR breakeven year produced by the SSM, so the two models share the same horizon.

The Historical Start-Year Sweep tests whether the SSM's transition properties depend on which portion of the historical return sequence the WDT inherits at launch. It runs a stripped SSM from every viable start year in the 1947–2019 data, generating a 73-row dataset covering SRR capitalisation speed, LRR breakeven year, reserve surplus, and post-fill coverage.

The Statistical Pass converts that 73-row dataset into summary statistics: success rate across start years, variation by economic cycle, and distribution of key transition metrics. The success definition is in (RATES.A §A.4).

## A.2 Architecture

The model is a single Python script; all inputs are read from a TOML parameter file at runtime. Every rate parameter, reserve sizing target, budget assumption, return series value, tier definition, and wealth bracket figure is specified in the TOML. No input is hardcoded. Replication requires only modifying the TOML and rerunning; the Python file does not change between scenarios.

Execution sequence: the TOML is loaded and validated against structural constraints (73 return values, tier weights summing to unity, population-weighted differentials summing to zero, rate parameter bounds). The SSM then runs on the active scenario (the canonical return series rotated so the configured start year is at index zero), producing year-by-year SRR and LRR trajectories and the LRR breakeven year N. N is passed to the TCM, which runs across all ten wealth brackets and four growth tiers, computing cumulative tax and refund flows over N periods plus a terminal sell year. The sweep follows, rotating the return series independently for each of the 73 calendar years and running both a stripped SSM and a full TCM for each. The statistical pass then processes the sweep output. Each run produces a dated Markdown report containing all active parameters, SSM and TCM results, sweep tables, and statistical summaries.

To reproduce any result: `python3 model.py params.toml`. Both arguments are optional and default to files in the script's directory.

One architectural feature of the SSM is not obvious from the above description and affects how the model should be read. The SSM computes year-by-year income using a marginal cohort approach: for each year N, it runs the full cumulative simulation for all ten wealth brackets from t = 0 through t = N (plus a terminal sell year at t = N+1), then subtracts the prior year's cumulative totals to extract the marginal flow for year N. This is equivalent to simulating a fresh cohort entering in year N, but implemented as a difference of cumulative simulations. Two consequences follow. First, the sell year at position N+1 appears in every year's marginal calculation, because each cumulative total includes the terminal sell event at the then-current horizon. Second, the computational cost of the SSM grows with N, since each year requires re-running the full history from t = 0. The stripped SSM used in the sweep applies the same architecture across all 73 start years, rotating the return series independently for each.

## A.3 Inputs

**Rate parameters.** The WDT applies a logistic marginal rate function $\tau$(W) to the annual wealth delta, parameterised by $\tau_0$ (floor rate at W = $W_{min}$), $\tau_m$ (asymptotic ceiling rate), $k$ (steepness per £m), and $W_{min}$ (entry point in £m). At the Balanced calibration: $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001 per £m, $W_{min}$ = £2.0m. $W_{min}$ is a rate design parameter, not a population boundary; the taxable population is fixed at 35,222,800 across all calibrations.

**Reserve sizing parameters.** The SRR target is a multiple of average net annual WDT income; the recommended Governing Council floor is 3×. The LRR floor is a number of years of prevailing government expenditure; the recommended minimum is 3 years. Both are TOML parameters and can be varied independently.

**Budget constants.** The expenditure model uses OBR total managed expenditure for 2022–23 as its base (£1,157.4b), grown at 4.51% per annum derived from the compound annual growth rate of nominal Total Managed Expenditure from 1999–00 to 2019–20 (HM Treasury, 2024, Table 10; see (JUR §2.11) for the corrected derivation and audit trail). A higher growth rate raises the fiscal hurdle while leaving the revenue trajectory unchanged, so any coverage result above 100% is a stronger demonstration under this rate than under a lower one.

**Return series.** The model uses 73 annual UK equity total-return figures for 1947–2019 (Jordà et al., 2019), stored in canonical order in the TOML. At runtime, the series is rotated so the configured start year sits at index zero; the canonical series is preserved separately for the sweep, which rotates independently for each start year. The series proxies broad wealth growth across the taxable population. A return sequence worse than any in the 1947–2019 data would extend transition timescales beyond those reported; the paper makes no claim of robustness beyond the historical range.

**Growth tier definitions.** The TCM applies four persistent return differentials relative to the historical mean of 10.45% per annum, derived from @FagerengEtAl2020: −4.55pp (Poor, 10% of active taxpayers), −2.05pp (Ok, 30%), +0.95pp (Good, 40%), and +3.45pp (Great, 20%). Population weights sum to unity; the population-weighted mean of differentials is zero, recovering the historical mean. Assigning 40% of taxpayers to below-average tiers is conservative given Fagereng et al.'s finding of a positive wealth-return correlation, since the WDT population is concentrated in the upper deciles.

**Wealth brackets.** Ten brackets cover the full taxable population, combining ONS Wealth and Assets Survey 2018–20 data for the bottom 99% with a Pareto extrapolation ($\alpha$ = 2.25) above the top-1% threshold of £3.6m. Each bracket is characterised by a population count and a mean wealth figure ($V_0$ in £m) used as TCM starting wealth. Above the top-1% threshold all figures are Pareto-implied. The WAS undersamples above £3m, so the modelled tail is lighter than the true distribution; both the revenue estimate and the refund exposure are conservative by the same degree.

## A.4 SSM Mechanics

The SSM models the WDT's transition from launch through LRR capitalisation as year-by-year accounting of two separate reserve processes, applying the historical return series uniformly to the entire taxable population. This is the correlated-shock assumption: every taxpayer experiences the same return in a given year, maximising simultaneous refund pressure and minimising net tax income. It is a deliberate worst-case, designed to stress the reserve structure against the kind of shock (a 2008-analogue crash) most damaging to the refund guarantee.

$\tau$(W) is applied to positive annual deltas to compute gross tax; in loss years the symmetric refund mechanism produces a refund at the same marginal rate, subject to the lifetime contribution envelope (cumulative refunds cannot exceed cumulative taxes paid). Net annual WDT income is gross taxes less gross refunds across the full population in a given year.

The SRR is a ring-fenced reserve whose sole purpose is to guarantee the refund obligation. Its target in any year N is 3× the running average of net annual income over years 1 through N. The SRR has first claim on net annual income: income flows to the SRR until its target is met; any surplus is available to the LRR. The SRR may draw on accumulated LRR surplus to restore itself when net income alone is insufficient. The SRR fill year is the first year the SRR balance reaches or exceeds its running-average target.

The LRR receives only the surplus remaining after the SRR target is satisfied. During the accumulation phase it bears no expenditure obligation; it simply accumulates SRR surplus each year, building toward its floor target. The LRR breakeven year (the primary SSM output, and the horizon to which the TCM is calibrated) is the first year the LRR balance reaches the recommended floor of 3 years of prevailing government expenditure.

Once the LRR floor is reached, the model applies a zero-governance assumption: the full burden of government expenditure falls on the LRR each year with no Governing Council rate adjustment. The LRR balance increases by the SRR surplus and decreases by full annual expenditure. The LRR breach year is the first year this cumulative outflow exhausts the reserve. Breach year and breach lag are reported in the sweep table as indicators of available intervention time, not predictions of system behaviour under active governance.

**Success definition.** A start year is a success if two conditions hold simultaneously: the LRR fills within the 71-year modelling window, and either the SRR never breaches zero or, if it does, the LRR balance at the moment of first SRR breach covers that deficit in full. Transition length and solvency are treated as separate questions; a long breakeven is not itself a failure.

The SRR breach check is a static coverage assessment, not a modelled active transfer. The model records the LRR balance at first SRR breach and checks whether it exceeds the SRR deficit at that moment. It does not simulate a transfer. First breach is used rather than worst deficit because a real SRR solvency event would not arise suddenly: the SRR draws down gradually over multiple years as net income falls short of the running-average target, giving the Governing Council time to observe deterioration before the balance turns negative. No additional governance response is assumed. In practice the mandatory rate review (GOV §5.3) and (GOV §6) would intervene before breach; the model takes no credit for this. The LRR balance at first SRR breach is therefore the relevant buffer under the most conservative assumption: whatever the LRR holds at that moment, without any subsequent intervention, stands between the mechanism and a genuine solvency failure.

## A.5 TCM Mechanics

The TCM models a representative taxpayer in each of forty wealth-bracket-by-growth-tier cells (ten brackets × four tiers), simulating cumulative tax and refund flows over N regular periods plus a terminal sell year, where N is the LRR breakeven year produced by the SSM. N is always passed from the SSM output; the two models share the same horizon by construction.

In each period t, true wealth V_t grows at the actual historical return for that period (from the return series rotated to the active scenario's start year) plus the tier's persistent differential. Declared wealth W_t is a fraction f_t of V_t, where f_t begins at 1.0 and evolves through the Route C equity-transfer mechanism: in each period the WDT settlement transfers a proportional equity interest at the declared value, gradually reducing the retained equity fraction. The annual delta is W_t − W_{t−1}; $\tau$(W_t) is applied to positive deltas to compute gross tax. In loss years the symmetric refund applies at the same marginal rate, subject to the lifetime contribution envelope: annual liability L_t is bounded below by the larger of zero and the negative of cumulative net tax paid to date, ensuring refunds never exceed taxes paid over the lifetime horizon.

Net annual tax per taxpayer in bracket b and tier d is the mean of L_t over all N+1 periods. The annual revenue contribution of each cell is this figure multiplied by bracket population and tier population weight. Total annual TCM revenue is the sum across all forty cells. All figures are population-weighted averages over the full N+1-period horizon, not single-year snapshots.

The terminal sell year uses the return at position N+1 of the rotated series and settles the full remaining declared position. It is included in all per-taxpayer averages.

## A.6 Coverage Metrics

The coverage metrics in (RATES.A §B.2) and (RATES.A §B.3) (and the sweep table's SSM and TCM coverage columns) answer a specific question: what fraction of government expenditure could have been replaced by WDT revenue during the capitalisation period? This is narrower than the headline revenue figures in (RATES §7).

The capitalisation window runs from SRR fill to LRR fill: the years the WDT is operational, the refund guarantee is credible, and the LRR is accumulating toward its floor target. For the 2007 Balanced scenario this is year 3 to year 29, a span of 25 years. Coverage ratios are averages over this window, not point-in-time figures at LRR fill.

The SSM coverage ratio is average annual net SSM income over the capitalisation window divided by average annual government expenditure over the same window: 21.3% for the 2007 Balanced scenario. In years where the return series is negative or very low, net income falls sharply as refund outflows approach or exceed gross tax receipts, pulling the window average well below long-run revenue potential. The SSM coverage ratio is a floor under the most conservative assumptions about return correlation.

The TCM coverage ratio is average annual TCM revenue over the capitalisation window divided by average annual government expenditure: 27.4% for the 2007 Balanced scenario. Higher-tier taxpayers compound at persistent above-average rates throughout the window, producing higher average revenue than the SSM's uniform series. The gap between 21.3% and 27.4% is narrower than at prior calibrations, reflecting that a lower floor rate reduces the premium that persistent tier-differential compounding produces over the correlated-shock baseline: at $\tau_0$ = 15% the floor-rate contribution to gross tax in lower-wealth brackets is smaller, so the tier differentials produce less relative uplift over the SSM's uniform-return assumption. Neither figure is more correct; they stress different aspects of the same mechanism and together bracket the plausible range.

There is a known boundary-alignment bug. The SSM window runs from the SRR fill year through to (but excluding) the LRR fill year; the TCM budget denominator in the sweep runs from the year after SRR fill through to (and including) the LRR fill year — the mirror image, shifted by one year at each end. The TCM post-fill revenue numerator was partially corrected to align with the SSM window but the budget denominator was not correspondingly corrected, leaving the two sides of the TCM coverage ratio computed over slightly different year sets. The effect is small (on the order of one year's revenue and expenditure at each boundary), but the inconsistency means the two ratios are not as cleanly comparable as they appear. The fix requires aligning both the numerator window in `run_tcm` and the budget denominator range in `run_start_year_sweep` to the same boundary convention. Until then, both ratios should be read as order-of-magnitude indicators.

The TCM coverage figure does not mean 27.4% of expenditure is replaced during the capitalisation window. The LRR is still being filled during this period; existing taxes have not yet been displaced. The interpretation is directional: at the moment of LRR fill, the mechanism has delivered average revenue equal to roughly a quarter of contemporaneous government expenditure across the prior 25 years. This supports a magnitude claim (appreciable tens of percent, not single digits and not hundreds of percent) without asserting precision a forward-looking model cannot provide. Across all 73 start years, TCM coverage ranges from 24.0% (2005 start) to 134.5% (1974 start); several starts from the 1960s and early 1970s exceed 100%, meaning the mechanism would have been capable of full fiscal replacement immediately upon LRR fill under those historical conditions.

The approximately 4:3 ratio of TCM to SSM coverage (27.4% vs. 21.3% in the 2007 case) has a directional implication for transition length. If actual conditions are closer to the TCM's persistent-heterogeneity model than the SSM's correlated-shock assumption, revenue accumulates somewhat faster on average, suggesting LRR fill could plausibly arrive somewhat earlier than the SSM projects. The relationship between average revenue and LRR fill year is not linear, but the direction holds even at the worst-case start year. The ratio is narrower at $\tau_0$= 15% than at prior calibrations; this is expected: the lower floor rate compresses both the SSM income (less gross tax at the floor) and the TCM income (same compression, partially offset by tier differentials), but the TCM's tier-differential advantage diminishes at lower floor rates because the gain-year marginal rates at lower wealth brackets converge more closely to the SSM's uniform-return calculation.

These metrics are statistical summaries derived from historical return data. They establish that the mechanism produces revenue of a substantial order of magnitude during the capitalisation period and show how that order of magnitude varies with historical starting conditions.

## A.7 Reproducibility

All inputs are in the TOML parameter file (`7_4_260729_WDT_Rates_and_Revenue_Params.toml`). The Python file contains no hardcoded inputs. Replication requires only the TOML, the script, and a standard Python 3 environment with `tomllib` (or `tomli`). No proprietary data, external API calls, or Excel workbook are required.

To run: `python3 model.py [params.toml]`. The TOML path defaults to the script directory if omitted. Each run produces a dated Markdown output file (`7_5_YYMMDD_WDT_Rates_Revenue_Output.md`) containing the full parameter set, all SSM and TCM results, the complete 73-row sweep table, and the statistical pass. §B.1–§B.5 reproduce the output from the 2007 Balanced run.

To vary a scenario, modify the TOML and rerun. Only the `scenario_start_year` field in the `[tcm]` section changes between start-year scenarios; rate parameters, reserve ratios, budget constants, and return series values are shared and need not be touched. The sweep tests all 73 start years regardless of the active scenario, so a single run produces both the active-scenario results and the full historical comparison.

\newpage

# B. Model Output

**Run date:** 2026-09-12  
**Scenario:** 2000 Balanced  
**Model version:** v7  
**Parameters file:** `WDT_Params.toml`  

## B.1 Active Parameters

| Parameter | Value |
|:---|:---|
| $\tau_0$ (floor rate) | 15% |
| $\tau_m$ (ceiling rate) | 70% |
| $k$ (steepness, per £m) | 0.001 |
| $W_{\min}$ (£m) | £2.0m |
| SRR capitalisation ratio | 3.0× |
| LRR floor (years of expenditure) | 3.0 years |
| Budget base (£b) | £1,157.4b |
| Budget growth (p.a.) | 4.51% |
| Historical mean return | 10.45% |

**Growth tiers:**

| Tier | Weight | Differential | Implied return |
|:---|---:|---:|---:|
| Poor | 10% | -4.55% | 5.90% |
| Ok | 30% | -2.05% | 8.40% |
| Good | 40% | +0.95% | 11.40% |
| Great | 20% | +3.45% | 13.90% |

## B.2 SSM Results — Active Scenario

| Metric | Value |
|:---|:---|
| SRR fill year | 3 |
| LRR breakeven year | 19 |
| Annual expenditure at LRR breakeven (£b) | £2,560b |
| SRR balance at LRR breakeven (£b) | £1,460b |
| LRR surplus at breakeven (£b) | £104b |
| LRR failure year | no failure within 71-year window |
| SRR failure year | no failure within 71-year window |
| LRR→SRR failure gap (years) | — |

**SSM Step-5 coverage fraction by window (average % of annual expenditure available for labour tax relief):**

| Window | SSM coverage | Zero-coverage years | Min LRR balance (£b) | Years LRR below floor |
|:---|---:|---:|---:|---:|
| 5 years | 0.0% | 5 | £7,858b | 5 |
| 10 years | 6.4% | 7 | £7,858b | 7 |
| 20 years | 21.3% | 10 | £7,858b | 10 |
| 50 years | 307.1% | 14 | £7,858b | 14 |

*SSM applies uniform historical returns across the population (correlated-shock assumption — worst-case floor). Coverage fraction = Step-5 remainder / annual expenditure; zero in any year where LRR or SRR balance hits zero. TCM coverage (heterogeneous-tier ceiling) appears in §B.3.*

## B.3 TCM Results — snapshot N=19 (cap. window) / N=30 (lifetime)

*Two TCM horizons are used in this section. Capitalisation-window tables (§B.3.1, §B.3.2, §B.3.6–§B.3.9 cap-window column) use N=19 — the SSM LRR breakeven year. Lifetime and burden tables (§B.3.3, §B.3.4, §B.3.5, §B.3.9 lifetime column) use N=30 — the canonical taxpayer horizon declared across VAL, RATES, SWEEPS, and WFR. Using N=19 for those tables would understate the burden by averaging tax over too few years and anchoring terminal wealth too early.*


### B.3.1 Net worth — start ($V_0$) and year N (£m)

*$V_0$ is the bracket mean wealth (£m) at entry, identical across tiers within a bracket. V_N is the true wealth (before tax settlement) at the end of period N for a representative taxpayer, varying by tier due to persistent return differentials. Figures are for a single representative taxpayer; they do not reflect aggregate portfolio wealth.*

| Net worth (£m) | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ |
|---|---|---|---|---|---|---|---|---|---|---|
| **$V_0$ (start, all tiers)** | £0.402m | £0.570m | £0.782m | £1.109m | £1.629m | £2.858m | £7.135m | £19.854m | £53.385m | £139.607m |
| **V_N -4.55% (Poor)** | £0.64m | £0.91m | £1.25m | £1.77m | £2.61m | £4.57m | £11.41m | £31.75m | £85.36m | £223.23m |
| **V_N -2.05% (Ok)** | £1.02m | £1.44m | £1.98m | £2.80m | £4.12m | £7.23m | £18.05m | £50.21m | £135.02m | £353.10m |
| **V_N +0.95% (Good)** | £1.74m | £2.46m | £3.38m | £4.79m | £7.04m | £12.36m | £30.84m | £85.82m | £230.76m | £603.47m |
| **V_N +3.45% (Great)** | £2.68m | £3.80m | £5.23m | £7.41m | £10.88m | £19.10m | £47.67m | £132.63m | £356.64m | £932.65m |

### B.3.2 Net per taxpayer per year — capitalisation window average (£/yr)

*Average annual net tax per representative taxpayer over the capitalisation window (SRR fill year to LRR breakeven year). Zeros suppressed.*

| Tier \ Bracket | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| -4.55% (Poor) | £— | £— | £— | £— | £4,897 | £11,854 | £29,698 | £83,531 | £230,983 | £647,561 |
| -2.05% (Ok) | £— | £— | £— | £5,341 | £16,508 | £28,670 | £71,890 | £202,722 | £564,248 | £1,605,704 |
| +0.95% (Good) | £— | £3,143 | £8,653 | £18,646 | £34,334 | £59,282 | £148,894 | £421,881 | £1,188,304 | £3,470,065 |
| +3.45% (Great) | £4,468 | £11,740 | £21,216 | £35,314 | £56,583 | £97,252 | £244,752 | £697,543 | £1,992,762 | £5,985,093 |

### B.3.3 Annual wealth burden (tax as % of net worth) — N=30

*Average annual net tax as a percentage of terminal settlement wealth. Computed at N=30 (canonical 30-year horizon): avg_net = total_net / (N+1); wealth_burden = avg_net / TW_settled. TW_settled is the post-settlement terminal wealth at year N=30.*

| Tier \ Bracket | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| -4.55% (Poor) | 0.00% | 0.00% | 0.00% | 0.00% | 0.12% | 0.17% | 0.17% | 0.17% | 0.18% | 0.20% |
| -2.05% (Ok) | 0.00% | 0.00% | 0.13% | 0.21% | 0.31% | 0.32% | 0.32% | 0.33% | 0.34% | 0.39% |
| +0.95% (Good) | 0.18% | 0.27% | 0.31% | 0.36% | 0.40% | 0.41% | 0.42% | 0.43% | 0.47% | 0.59% |
| +3.45% (Great) | 0.33% | 0.37% | 0.40% | 0.42% | 0.44% | 0.45% | 0.46% | 0.49% | 0.57% | 0.79% |

| Aggregation | Value | Interpretation |
|:---|---:|:---|
| Population-weighted avg burden | 0.24% | Σ(burden × headcount) / Σ headcount — each taxpayer counts once; lower-wealth brackets dominate numerically |
| Revenue-weighted (wealth-weighted) burden | 0.35% | Σ(avg_net_m × headcount) / Σ(TW × headcount) — burden as fraction of aggregate terminal wealth; higher-wealth brackets dominate |

*Both figures computed at N=30. The gap between them reflects wealth concentration: if returns were homogeneous the two would be equal; the higher-wealth tiers' larger TW pulls the revenue-weighted figure relative to the headcount figure.*

### B.3.4 Effective rate on lifetime gains (income-tax analogue) — N=30

*income_tax_rate = total_net_settled / (TW_settled − V₀). Numerator: total lifetime net WDT (including post-sale settlement oscillations). Denominator: net lifetime wealth gain — what the taxpayer ended up with above what they started with, after all tax cash flows have resolved. Directly comparable to an income or CGT rate. Cells showing "—" have TW_settled ≤ V₀ (net loss over the horizon; WDT issued net refunds, so no positive effective rate is defined). Computed at N=30.*

| Tier \ Bracket | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| -4.55% (Poor) | 0.0% | 0.0% | 0.0% | 0.0% | 10.9% | 15.6% | 15.7% | 15.9% | 16.5% | 18.2% |
| -2.05% (Ok) | 0.0% | 0.0% | 5.7% | 9.7% | 14.7% | 15.0% | 15.2% | 15.5% | 16.3% | 18.6% |
| +0.95% (Good) | 6.3% | 9.7% | 11.2% | 13.1% | 14.7% | 15.1% | 15.3% | 15.9% | 17.5% | 21.9% |
| +3.45% (Great) | 11.0% | 12.3% | 13.3% | 14.2% | 14.9% | 15.2% | 15.6% | 16.6% | 19.5% | 27.2% |

| Aggregation | Value | Interpretation |
|:---|---:|:---|
| Population-weighted avg effective rate | 9.1% | Σ(income_tax_rate × headcount) / Σ headcount — cells with net loss excluded; lower-wealth brackets dominate numerically |
| Gain-weighted effective rate | 13.0% | Σ(total_net_settled × headcount) / Σ(lifetime_gain × headcount) — tax as fraction of aggregate lifetime wealth created; higher-wealth brackets dominate |

*Both figures computed at N=30, excluding cells where TW_settled ≤ V₀. The gain-weighted figure is the closer analogue to a statutory income tax rate applied to aggregate gains.*

### B.3.5 Average annual net tax per taxpayer — lifetime average (£/yr) — N=30

*Average annual net tax (total_net / (N+1)) per representative taxpayer over the full N=30-year horizon. Distinct from §B.3.2 (capitalisation-window average at N=19): this figure reflects the long-run per-taxpayer cost across all years including pre-SRR-fill periods where rates are lower.*

| Tier \ Bracket | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| -4.55% (Poor) | £— | £— | £— | £— | £3,121 | £7,393 | £18,530 | £52,181 | £144,753 | £409,119 |
| -2.05% (Ok) | £— | £— | £3,243 | £7,445 | £14,989 | £26,752 | £67,160 | £190,045 | £533,644 | £1,549,590 |
| +0.95% (Good) | £5,462 | £11,288 | £17,341 | £27,067 | £41,975 | £74,185 | £187,066 | £536,151 | £1,552,524 | £4,782,591 |
| +3.45% (Great) | £19,018 | £28,851 | £41,045 | £59,090 | £86,700 | £151,887 | £385,789 | £1,128,445 | £3,416,036 | £11,137,038 |

### B.3.6 Population distribution (taxpayers per bracket per tier)

*Cell population = bracket population × tier weight. Bracket population is constant within a bracket across tiers.*

| Tier \ Bracket | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10% (Poor) | 692,000 | 692,000 | 692,000 | 692,000 | 346,000 | 276,800 | 62,280 | 6,228 | 623 | 69 |
| 30% (Ok) | 2,076,000 | 2,076,000 | 2,076,000 | 2,076,000 | 1,038,000 | 830,400 | 186,840 | 18,684 | 1,868 | 208 |
| 40% (Good) | 2,768,000 | 2,768,000 | 2,768,000 | 2,768,000 | 1,384,000 | 1,107,200 | 249,120 | 24,912 | 2,491 | 277 |
| 20% (Great) | 1,384,000 | 1,384,000 | 1,384,000 | 1,384,000 | 692,000 | 553,600 | 124,560 | 12,456 | 1,246 | 138 |

### B.3.7 Tax collected per year — capitalisation window average (£m/yr)

*Average annual revenue per bracket-tier cell over the capitalisation window. Row total is the sum across all brackets for that tier. Column total is the sum across all tiers for that bracket. Grand total is in the bottom-right cell.*

| Tier (weight) \ Bracket | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ | **Row total** |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10% (Poor) | £— | £— | £— | £— | £1,694 | £3,281 | £1,850 | £520 | £144 | £45 | **£7,534.3m** |
| 30% (Ok) | £— | £— | £— | £11,089 | £17,135 | £23,808 | £13,432 | £3,788 | £1,054 | £333 | **£70,638.5m** |
| 40% (Good) | £— | £8,699 | £23,950 | £51,613 | £47,518 | £65,637 | £37,093 | £10,510 | £2,960 | £961 | **£248,940.9m** |
| 20% (Great) | £6,184 | £16,249 | £29,362 | £48,874 | £39,155 | £53,839 | £30,486 | £8,689 | £2,482 | £828 | **£236,148.9m** |
| **Column total** | **£6,184.2m** | **£24,947.8m** | **£53,312.7m** | **£111,576.1m** | **£105,502.7m** | **£146,564.9m** | **£82,860.3m** | **£23,506.4m** | **£6,640.6m** | **£2,167.0m** | **£563,262.6m** |

*Row totals in £b/yr:*

| Tier (weight) | £b/yr |
|:---|---:|
| 10% (Poor) | £7.53b |
| 30% (Ok) | £70.64b |
| 40% (Good) | £248.94b |
| 20% (Great) | £236.15b |
| **Grand total** | **£563.26b** |

### B.3.8 Cohort proportion of total tax paid (%)

*Each cell's capitalisation-window revenue as a percentage of the grand total. Row total is the tier's share; column total is the bracket's share across all tiers.*

| Tier (weight) \ Bracket | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ | **Row total** |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10% (Poor) | 0.0% | 0.0% | 0.0% | 0.0% | 0.3% | 0.6% | 0.3% | 0.1% | 0.0% | 0.0% | **1.3%** |
| 30% (Ok) | 0.0% | 0.0% | 0.0% | 2.0% | 3.0% | 4.2% | 2.4% | 0.7% | 0.2% | 0.1% | **12.5%** |
| 40% (Good) | 0.0% | 1.5% | 4.3% | 9.2% | 8.4% | 11.7% | 6.6% | 1.9% | 0.5% | 0.2% | **44.2%** |
| 20% (Great) | 1.1% | 2.9% | 5.2% | 8.7% | 7.0% | 9.6% | 5.4% | 1.5% | 0.4% | 0.1% | **41.9%** |
| **Column total** | **1.1%** | **4.4%** | **9.5%** | **19.8%** | **18.7%** | **26.0%** | **14.7%** | **4.2%** | **1.2%** | **0.4%** | **100.0%** |

### B.3.9 Revenue by tier (£b/yr)

*Lifetime avg column: revenue_m = (total_net / (N+1)) × bracket_pop × tier_weight, computed at N=30 (canonical 30-year horizon). Capitalisation window avg column: post_fill_revenue_m averaged over the SRR→LRR window, computed at N=19 (SSM LRR breakeven year).*

| Tier | Lifetime avg N=30 (£b/yr) | Cap. window N=19 (£b/yr) |
|:---|---:|---:|
| -4.55% (Poor) | £4.7b | £7.5b |
| -2.05% (Ok) | £77.4b | £70.6b |
| +0.95% (Good) | £374.7b | £248.9b |
| +3.45% (Great) | £416.8b | £236.1b |
| **Total** | **£873.6b** | **£563.26b** |

*TCM horizon N is derived from the SSM LRR breakeven year, not the TOML snapshot_N.*

**TCM Step-5 coverage fraction by window:**

| Window | TCM coverage | TCM failure year (LRR) | TCM failure year (SRR) |
|:---|---:|---:|---:|
| 5 years | 15.9% | None | None |
| 10 years | 14.6% | None | None |
| 20 years | 35.8% | None | None |
| 50 years | 655.6% | None | None |

*TCM applies heterogeneous tier differentials to the actual historical return series, producing higher revenue than the SSM uniform-return assumption. The SSM forms the solvency/stress-test floor; the TCM ceiling bounds the plausible range. TCM and SSM run independent SRR/LRR balance trackers.*

## B.4 Start-Year Sweep

All figures at $\tau_0$=15%, $\tau_m$=70%, k=0.001, $W_{\min}$=£2.0m.

### B.4.1 Extremals — four dimensions

| Dimension | Start year | LRR breakeven | LRR surplus (£b) | LRR failure year | SRR failure year | SSM cov 50yr |
|:---|:---:|:---:|---:|:---:|:---:|---:|
| Speed — slowest LRR fill | 2006 | 29 | £523b | none | none | 593.9% |
| Speed — fastest LRR fill | 1970 | 7 | £402b | none | none | 397.5% |
| Margin — thinnest surplus | 1996 | 11 | £6b | none | none | 156.0% |
| Margin — largest surplus | 1963 | 12 | £4,336b | none | none | 459.1% |
| Durability — lowest 50yr SSMcov | 1984 | 9 | £77b | none | none | 95.6% |
| Durability — highest 50yr SSMcov | 1952 | 16 | £2,274b | none | none | 656.3% |
| Resilience — earliest LRR failure | — | — | — | — | — | — |
| Resilience — latest/no LRR failure | 1970 | 7 | £402b | none | none | 397.5% |

*73 start years produce no LRR failure within the 71-year modelling window.*

### B.4.2 Full sweep table (all 73 calendar years)

| Start | SRR fill | LRR fill | LRR surplus (£b) | LRR failure | SRR failure | gap | SSMcov5 | SSMcov10 | SSMcov20 | SSMcov50 | TCMcov10 | TCMcov50 |
|:---:|:---:|:---:|---:|:---:|:---:|:---:|---:|---:|---:|---:|---:|---:|
| 1947 | 3 | 21 | 1,934 | — | — | — | 92.0% | 131.8% | 286.2% | 559.7% | 158.1% | 1321.8% |
| 1948 | 3 | 20 | 2,454 | — | — | — | 97.1% | 139.8% | 300.9% | 587.6% | 164.4% | 1355.1% |
| 1949 | 3 | 18 | 152 | — | — | — | 86.5% | 132.9% | 271.6% | 615.8% | 170.2% | 1385.3% |
| 1950 | 3 | 18 | 2,153 | — | — | — | 101.5% | 146.3% | 315.7% | 615.8% | 166.2% | 1355.4% |
| 1951 | 3 | 17 | 2,126 | — | — | — | 103.7% | 149.9% | 323.2% | 630.2% | 167.7% | 1358.0% |
| 1952 | 3 | 16 | 2,274 | — | — | — | 107.7% | 156.7% | 336.7% | 656.3% | 171.9% | 1381.8% |
| 1953 | 3 | 15 | 1,115 | — | — | — | 97.2% | 145.4% | 321.1% | 627.0% | 176.9% | 1288.5% |
| 1954 | 3 | 17 | 3,266 | — | — | — | 151.2% | 218.8% | 379.3% | 605.3% | 156.6% | 1160.7% |
| 1955 | 3 | 16 | 3,113 | — | — | — | 152.9% | 221.5% | 384.3% | 612.8% | 154.7% | 1153.4% |
| 1956 | 3 | 15 | 2,704 | — | — | — | 153.3% | 223.7% | 391.3% | 624.9% | 248.8% | 1246.8% |
| 1957 | 3 | 14 | 2,681 | — | — | — | 157.3% | 230.1% | 402.6% | 643.2% | 271.6% | 1279.4% |
| 1958 | 3 | 13 | 360 | — | — | — | 128.9% | 195.5% | 353.5% | 565.7% | 229.7% | 1093.3% |
| 1959 | 3 | 13 | 586 | — | — | — | 142.4% | 194.1% | 321.8% | 491.2% | 228.6% | 943.0% |
| 1960 | 3 | 12 | 482 | — | — | — | 143.3% | 196.4% | 326.4% | 498.5% | 228.2% | 937.3% |
| 1961 | 3 | 11 | 227 | — | — | — | 141.1% | 195.9% | 327.5% | 500.5% | 224.2% | 920.2% |
| 1962 | 3 | 11 | 662 | — | — | — | 144.0% | 212.1% | 340.6% | 487.6% | 244.6% | 897.1% |
| 1963 | 3 | 12 | 4,336 | — | — | — | 207.9% | 250.9% | 349.4% | 459.1% | 288.1% | 844.5% |
| 1964 | 3 | 11 | 4,047 | — | — | — | 211.4% | 255.6% | 356.3% | 468.5% | 291.1% | 845.6% |
| 1965 | 3 | 10 | 2,813 | — | — | — | 201.6% | 244.2% | 338.9% | 446.0% | 275.6% | 789.1% |
| 1966 | 3 | 9 | 2,328 | — | — | — | 201.5% | 243.2% | 339.1% | 446.6% | 270.4% | 775.3% |
| 1967 | 3 | 8 | 320 | — | — | — | 172.2% | 212.3% | 306.0% | 406.4% | 282.7% | 732.3% |
| 1968 | 3 | 9 | 1,906 | — | — | — | 183.9% | 241.1% | 305.2% | 380.3% | 269.0% | 664.1% |
| 1969 | 3 | 8 | 1,623 | — | — | — | 189.5% | 247.9% | 315.1% | 393.3% | 273.4% | 673.6% |
| 1970 | 3 | 7 | 402 | — | — | — | 179.3% | 242.5% | 315.5% | 397.5% | 321.4% | 666.0% |
| 1971 | 3 | 8 | 1,978 | — | — | — | 191.8% | 287.9% | 307.2% | 327.9% | 316.5% | 551.4% |
| 1972 | 3 | 8 | 2,189 | — | — | — | 173.5% | 235.4% | 268.6% | 282.5% | 257.1% | 472.7% |
| 1973 | 3 | 7 | 445 | — | — | — | 148.3% | 204.7% | 239.8% | 254.4% | 223.3% | 418.1% |
| 1974 | 3 | 7 | 1,138 | — | — | — | 197.1% | 229.7% | 248.3% | 281.8% | 244.8% | 469.6% |
| 1975 | 3 | 8 | 1,284 | — | — | — | 187.4% | 187.6% | 213.1% | 221.7% | 207.1% | 376.9% |
| 1976 | 3 | 8 | 1,663 | — | — | — | 223.9% | 167.7% | 216.9% | 211.0% | 181.7% | 358.5% |
| 1977 | 3 | 8 | 1,057 | — | — | — | 164.6% | 151.5% | 194.9% | 184.6% | 166.6% | 315.6% |
| 1978 | 3 | 8 | 1,669 | — | — | — | 154.2% | 141.6% | 187.8% | 176.1% | 154.0% | 302.8% |
| 1979 | 3 | 8 | 1,141 | — | — | — | 126.6% | 130.7% | 163.8% | 147.5% | 141.4% | 253.1% |
| 1980 | 3 | 8 | 498 | — | — | — | 99.9% | 107.1% | 129.6% | 126.5% | 121.1% | 220.4% |
| 1981 | 3 | 8 | 2,172 | — | — | — | 66.0% | 113.8% | 122.4% | 118.9% | 126.2% | 207.0% |
| 1982 | 3 | 7 | 243 | — | — | — | 50.2% | 92.1% | 104.7% | 104.3% | 108.9% | 223.5% |
| 1983 | 3 | 9 | 363 | — | — | — | 80.9% | 82.5% | 97.8% | 106.7% | 95.1% | 192.9% |
| 1984 | 3 | 9 | 77 | — | — | — | 71.9% | 84.8% | 88.6% | 95.6% | 116.9% | 208.4% |
| 1985 | 3 | 11 | 586 | — | — | — | 80.2% | 105.4% | 89.8% | 114.9% | 124.0% | 226.2% |
| 1986 | 3 | 11 | 453 | — | — | — | 58.6% | 89.7% | 77.0% | 98.0% | 107.3% | 192.3% |
| 1987 | 3 | 11 | 63 | — | — | — | 65.6% | 72.0% | 65.0% | 110.2% | 85.1% | 228.4% |
| 1988 | 3 | 12 | 318 | — | — | — | 73.2% | 62.4% | 54.4% | 111.0% | 74.7% | 239.1% |
| 1989 | 3 | 14 | 509 | — | — | — | 56.2% | 45.9% | 37.4% | 129.9% | 62.8% | 299.4% |
| 1990 | 3 | 13 | 645 | — | — | — | 60.3% | 49.3% | 39.9% | 136.6% | 64.9% | 306.4% |
| 1991 | 3 | 13 | 1,302 | — | — | — | 50.4% | 47.6% | 35.6% | 137.8% | 57.0% | 286.9% |
| 1992 | 3 | 12 | 522 | — | — | — | 42.8% | 42.6% | 32.7% | 132.9% | 55.8% | 289.9% |
| 1993 | 3 | 12 | 588 | — | — | — | 39.7% | 35.6% | 26.9% | 137.2% | 48.0% | 304.4% |
| 1994 | 3 | 11 | 539 | — | — | — | 41.3% | 37.0% | 28.1% | 142.7% | 47.6% | 307.7% |
| 1995 | 3 | 11 | 133 | — | — | — | 23.5% | 32.8% | 24.0% | 145.7% | 44.4% | 314.8% |
| 1996 | 3 | 11 | 6 | — | — | — | 14.4% | 30.3% | 24.1% | 156.0% | 42.2% | 337.2% |
| 1997 | 3 | 16 | 191 | — | — | — | 30.6% | 20.2% | 26.7% | 267.4% | 30.5% | 646.9% |
| 1998 | 3 | 18 | 1,141 | — | — | — | 22.2% | 13.5% | 27.3% | 305.2% | 23.0% | 659.7% |
| 1999 | 3 | 18 | 48 | — | — | — | 7.1% | 10.2% | 20.4% | 272.1% | 17.9% | 681.6% |
| **2000** | **3** | **19** | **104** | **—** | **—** | **—** | **0.0%** | **6.4%** | **21.3%** | **307.1%** | **14.6%** | **655.6%** |
| 2001 | 3 | 18 | 242 | — | — | — | 0.0% | 7.1% | 22.2% | 312.4% | 20.5% | 650.8% |
| 2002 | 3 | 25 | 1,395 | — | — | — | 44.4% | 34.0% | 62.3% | 442.9% | 17.0% | 745.8% |
| 2003 | 3 | 28 | 1,456 | — | — | — | 43.9% | 49.4% | 105.0% | 407.7% | 45.6% | 1140.6% |
| 2004 | 3 | 28 | 2,287 | — | — | — | 27.8% | 38.8% | 112.4% | 448.0% | 44.1% | 1557.9% |
| 2005 | 3 | 27 | 605 | — | — | — | 18.5% | 32.1% | 102.8% | 634.1% | 62.3% | 1366.8% |
| 2006 | 3 | 29 | 523 | — | — | — | 32.8% | 58.0% | 145.0% | 593.9% | 54.7% | 1383.7% |
| 2007 | 3 | 29 | 1,041 | — | — | — | 46.3% | 63.5% | 157.5% | 607.7% | 48.3% | 1284.6% |
| 2008 | 3 | 27 | 998 | — | — | — | 38.3% | 64.0% | 156.5% | 597.9% | 56.8% | 1342.8% |
| 2009 | 3 | 26 | 815 | — | — | — | 37.3% | 64.2% | 158.2% | 602.0% | 54.3% | 1241.3% |
| 2010 | 3 | 26 | 919 | — | — | — | 50.5% | 69.1% | 170.6% | 461.3% | 48.1% | 1256.7% |
| 2011 | 3 | 25 | 1,152 | — | — | — | 53.7% | 72.3% | 176.5% | 576.1% | 48.5% | 1263.8% |
| 2012 | 3 | 24 | 747 | — | — | — | 50.3% | 70.4% | 174.9% | 591.1% | 45.0% | 1227.8% |
| 2013 | 3 | 25 | 877 | — | — | — | 44.5% | 104.2% | 211.9% | 495.2% | 82.8% | 1299.6% |
| 2014 | 3 | 24 | 120 | — | — | — | 37.2% | 97.5% | 202.5% | 539.2% | 89.8% | 1291.0% |
| 2015 | 3 | 25 | 1,774 | — | — | — | 92.3% | 130.5% | 258.6% | 591.7% | 85.4% | 1251.7% |
| 2016 | 3 | 24 | 419 | — | — | — | 81.1% | 120.8% | 244.7% | 561.0% | 123.8% | 1271.7% |
| 2017 | 3 | 24 | 2,653 | — | — | — | 88.8% | 126.6% | 273.5% | 521.9% | 125.5% | 1302.8% |
| 2018 | 3 | 22 | 289 | — | — | — | 79.9% | 122.1% | 249.5% | 579.6% | 131.0% | 1344.4% |
| 2019 | 3 | 22 | 2,017 | — | — | — | 89.6% | 128.1% | 278.3% | 562.3% | 156.2% | 1317.2% |

*Active scenario shown in bold. Coverage fractions = Step-5 remainder / annual expenditure, averaged over each window. Zero in failure years drags the average. LRR failure: buffer exhausted (lrr_bal = 0). SRR failure: refund guarantee broken (srr_bal = 0). Gap: years between LRR and SRR failure. SSM = correlated-shock floor; TCM = heterogeneous-tier ceiling.*

## B.5 Statistical Pass — P(success) Across Economic Cycles

**Success definition (v8):** LRR fills within the 71-year window AND LRR never fails (lrr_failure_year is None).

### B.5.1 Overall (all 73 start years)

| Metric | Value |
|:---|:---|
| Success rate | 100.0% (73/73) |
| LRR fills | 100.0% (73/73) |
| LRR failures | 0.0% (0/73) |
| SRR failures | 0.0% (0/73) |

### B.5.2 By economic cycle

| Period | N | Success% | LRR fill% |
|:---|:---:|:---:|:---:|
| Post-war growth  1947–59 | 13 | 100.0% | 100.0% |
| Long boom        1960–79 | 20 | 100.0% | 100.0% |
| Liberalisation   1980–99 | 20 | 100.0% | 100.0% |
| Crisis decade    2000–19 | 20 | 100.0% | 100.0% |

### B.5.3 Key metric distributions

| Metric | N | Min | Median | Mean | Max |
|:---|:---:|---:|---:|---:|---:|
| LRR breakeven year | 73 | 7 | 13 | 15 | 29 |
| SRR fill year | 73 | 3 | 3 | 3 | 3 |
| LRR failure year | 0 | — | — | — | — |
| SRR failure year | 0 | — | — | — | — |
| LRR→SRR failure gap (yrs) | 0 | — | — | — | — |
| LRR surplus at breakeven (£b) | 73 | 6 | 919 | 1,198 | 4,336 |
| SSM coverage 5yr avg | 73 | 0.0% | 86.5% | 97.4% | 223.9% |
| TCM coverage 5yr avg | 73 | 5.5% | 93.5% | 106.8% | 239.0% |
| SSM coverage 10yr avg | 73 | 6.4% | 122.1% | 126.0% | 287.9% |
| TCM coverage 10yr avg | 73 | 14.6% | 125.5% | 138.8% | 321.4% |
| SSM coverage 20yr avg | 73 | 20.4% | 202.5% | 198.4% | 402.6% |
| TCM coverage 20yr avg | 73 | 35.7% | 233.7% | 234.9% | 515.7% |
| SSM coverage 50yr avg | 73 | 95.6% | 442.9% | 386.2% | 656.3% |
| TCM coverage 50yr avg | 73 | 192.3% | 775.3% | 810.4% | 1557.9% |

*Coverage fractions: Step-5 remainder / annual expenditure, averaged over each window length. Zero in any failure year. SSM = correlated-shock floor; TCM = heterogeneous-tier ceiling.*
