---
title: "WFR Figure Captions — Complete Register"
note: >
  Naming convention: Figure N.X where N.X is the section the figure appears in.
  Multiple figures in a section use suffixes a, b, c, etc. in insertion order.
  WFR.A figure numbers follow the same logic against WFR.A section headings.
  All figures in Module 5 (Sweep analysis) belong in WFR.A; cross-reference
  hooks in WFR.md are noted separately.
---

# Module 1 — Baseline Single-Agent Comparison (§3)

## Figure 3.1a
*File:* `wfr_fig_a1_cew_by_gamma.png`
*Insertion:* §3.1, after Table 1 italic note, before "The flat WDT leads by 17.4 basis points…"

![Figure 3.1a: Certainty-equivalent welfare (CEW) by tax system across risk-aversion parameters $\gamma \in \{1, 2, 4\}$, at $E[T] = 2\%$ of $W_0$. Left panel: Ver. A (UK historical equity, 30-year scenario from 2000). Right panel: Ver. B (idealised two-state distribution, same mean and standard deviation). The flat symmetric WDT (blue) sits above income tax and CGT (gold/orange, overlapping) across all $\gamma$ values in Ver. A; the two distributions converge to near-identical rankings in Ver. B. Stock wealth tax and consumption tax (red/grey) are flat across $\gamma$ and sit below all other systems — the welfare cost is invariant to risk aversion because a fixed proportional wedge on a non-return-conditioned base leaves the relative consumption distribution unchanged under CRRA preferences. Source: WFR simulation model; underlying data from JST dataset (UK equity returns 1947–2019). **(WFR.A §A.1)**](../figures/wfr_fig_a1_cew_by_gamma.png){width=100%}

---

## Figure 3.1b
*File:* `wfr_fig_a4_wdt_advantage.png`
*Insertion:* §3.1, after the first structural-feature paragraph (ending "…does not attenuate the compounding of return differences across taxpayers."), before the second structural-feature paragraph (income tax = CGT equality).

![Figure 3.1b: WDT welfare advantage over competing systems ($\text{CEW}_{\text{WDT}} - \text{CEW}_{\text{competitor}}$, basis points; positive = WDT better), by $\gamma$. Left panel: Ver. A; right panel: Ver. B. The advantage over stock wealth tax and consumption tax (red/grey) rises approximately linearly with $\gamma$ — from roughly 7 basis points at $\gamma = 1$ to 26–27 basis points at $\gamma = 4$ — because those systems' CEW is $\gamma$-invariant while the WDT's improves with risk aversion. The advantage over income tax and CGT (gold/orange) is small and near-zero in Ver. B, confirming that the baseline result is not a rate artefact. Source: WFR simulation model; underlying data from JST dataset. **(WFR.A §A.1)**](../figures/wfr_fig_a4_wdt_advantage.png){width=100%}

---

## Figure 3.1c
*File:* `wfr_fig_a3_annual_tax.png`
*Insertion:* §3.1, after the second structural-feature paragraph (ending "…the lock-in cost in §4.2 attributable to the realisation mechanism alone."), before "Progressive WDT sits between the two clusters…"

![Figure 3.1c: Annual tax paid (positive bars) and refund received (negative bars) per £1 of $W_0$, Ver. A — UK historical equity returns, 30-year scenario 2000–2029. Top panel: flat symmetric WDT; middle panel: stock wealth tax; bottom panel: income tax (no refund). Dotted vertical lines mark years of negative returns (2008, 2018, 2021, 2022). The WDT top panel is the only system with below-zero bars: in loss years the government pays a refund proportional to the wealth decline. The stock wealth tax middle panel is near-flat across all years, insensitive to return performance. The income tax bottom panel tracks gain years only, collecting nothing in loss years and providing no relief. Source: WFR simulation model; underlying data from JST dataset. **(WFR.A §A.2)**](../figures/wfr_fig_a3_annual_tax.png){width=100%}

---

## Figure 3.2
*File:* `wfr_fig_a2_variance.png`
*Insertion:* §3.2, after the paragraph beginning "The consumption variance result in (WFR.A §A.2) confirms…" (ending "…without distorting the relative ranking of return states."), before "What the D-M result does not say…"

![Figure 3.2: Variance of consumption by tax system at $\gamma = 2$, $E[T] = 2\%$ of $W_0$. Left panel: Ver. A; right panel: Ver. B. Dashed horizontal line marks the no-tax variance (0.0028). The flat symmetric WDT (blue) achieves the lowest consumption variance (0.0013) of any taxed system — half the stock wealth tax and consumption tax figure (0.0027) and below income tax and CGT (0.0014 under Ver. A). Under Ver. B, income tax, CGT, and the WDT converge to 0.0013, confirming that the Ver. A gap reflects the empirical distribution's loss years rather than a structural rate advantage. The stock wealth and consumption tax bars reach 0.0027 in both distributions, consistent with the $\gamma$-invariance established in §3.1. Source: WFR simulation model; underlying data from JST dataset. **(WFR.A §A.2)**](../figures/wfr_fig_a2_variance.png){width=100%}

---

# Module 2 — Progressive Rates: Three Complications (§4.1)

## Figure 4.1a
*File:* `wfr_fig_b0_rate_function.png`
*Insertion:* §4.1, before "A progressive rate schedule breaks the Domar-Musgrave result…" (section opener).

![Figure 4.1a: Progressive WDT marginal rate function $\tau(W)$ at canonical parameters ($\tau_0 = 15\%$, $\tau_m = 70\%$, $k = 0.001$, $W_{min} = £2\text{m}$), plotted against wealth as a multiple of $W_{min}$. The near-flat lower limb — where the logistic barely rises above $\tau_0$ from entry up to roughly $50 \times W_{min}$ (£100m) — is the geometric reason all three D-M complications in this section are second-order at canonical parameters. The $\tau_m = 70\%$ ceiling (red dashed) is approached only at billion-pound wealth levels, far above the tested population. The vertical drop to zero at $W_{min}$ marks the entry threshold below which the WDT does not apply. Source: WFR simulation model; rate parameters from TOML \texttt{[rate]} block. **(RATES §3)**](../figures/wfr_fig_b0_rate_function.png){width=100%}

---

## Figure 4.1b
*File:* `wfr_fig_b1_flat_vs_progressive.png`
*Insertion:* §4.1, after the C1 paragraph (ending "…empirically negligible."), before the C2 paragraph.

![Figure 4.1b: CEW under flat WDT and progressive WDT across $\gamma \in \{1, 2, 4\}$, $W_0 = £10\text{m}$, $E[T] = 2\%$ of $W_0$. Left panel: Ver. A; right panel: Ver. B. The two series are visually coincident in both panels — the gap (C1 complication) is $-0.00$ basis points at $\gamma = 2$ and remains below $0.05$ basis points across all tested parameters. Both lines rise toward zero welfare cost as $\gamma$ increases because higher risk aversion amplifies the value of variance reduction: the D-M risk-sharing mechanism delivers greater benefit to more risk-averse agents, irrespective of whether the rate is flat or progressive, at these wealth levels. Source: WFR simulation model; underlying data from JST dataset. **(WFR.A §B.1)**](../figures/wfr_fig_b1_flat_vs_progressive.png){width=100%}

---

## Figure 4.1c
*File:* `wfr_fig_b2_leverage.png`
*Insertion:* §4.1, after the C2 interpretation paragraph (ending "…second-order relative to the mechanisms in §§4.2–4.3."), before the C3 paragraph.

![Figure 4.1c: C2 complication — leverage effect on the WDT tax base. Left panel: CEW gap between the net-worth (NW) delta base and a hypothetical asset-return base, in basis points, across leverage ratios 0–70% ($\gamma = 2$, Ver. A, gross assets = £10m throughout). The gap is monotone and convex in leverage, reaching +1.10 basis points at 70% — the direction confirms that taxing net worth rather than gross asset return marginally favours leveraged taxpayers, but the magnitude is small at all empirically relevant leverage ratios. Right panel: expected tax $E[T]$ under each base across the same leverage range. The NW base $E[T]$ (blue) falls with leverage as net worth shrinks; the asset-return base $E[T]$ (red) is flat, because the gross asset position is held constant at £10m regardless of debt. Source: WFR simulation model; underlying data from JST dataset. **(WFR.A §B.2)**](../figures/wfr_fig_b2_leverage.png){width=100%}

---

## Figure 4.1d
*File:* `wfr_fig_b3_asymmetry.png`
*Insertion:* §4.1, after the C3 interpretation paragraph (ending "…the direction a reader familiar with progressive bracket asymmetry would expect."), before "All three complications are real features…"

![Figure 4.1d: C3 complication — two-period rate asymmetry under a progressive WDT schedule. Sequence: gain of +18.8% in period 1, loss of $-8.3\%$ in period 2. Left panel (red): net tax excess relative to the flat revenue-equivalent rate (£m), plotted against initial wealth $W_0$. The Excess is uniformly negative — progression collects less net tax than flat across the full tested range — because the canonical population sits in the near-flat entry region of the logistic, well below the inflection point where the gain-at-higher-rate asymmetry would favour the government. Right panel (purple): rate asymmetry $\tau_{\text{gain}} - \tau_{\text{refund}}$ (percentage points), rising from +0.001 pp at £3m to +0.095 pp at £200m. The asymmetry is real and grows with wealth but remains small in absolute magnitude throughout. Source: WFR simulation model; rate parameters from TOML \texttt{[rate]} block. **(WFR.A §B.3)**](../figures/wfr_fig_b3_asymmetry.png){width=100%}

---

## Figure 4.1e
*File:* `wfr_fig_b4_combined_gamma1.png`
*Insertion:* §4.1, after the closing paragraph (ending "…the mechanisms that do generate large welfare differences are in the sections that follow."), before §4.2. Three-panel synthesis; each panel has its own caption.

![Figure 4.1e ($\gamma = 1.0$): Progressive WDT CEW with all three D-M complications, compared against the flat WDT and stock wealth tax benchmarks from §3.1. Ver. A — UK historical equity, 30-year scenario from 2000. At $\gamma = 1$, the progressive WDT sits at $-0.820\%$, between the flat WDT ($-1.820\%$) and the stock wealth tax ($-1.887\%$). The large separation between the flat WDT and progressive WDT bars reflects the single-agent test point at $W_0 = £10\text{m}$, where the progressive schedule applies lower effective rates than the flat revenue-equivalent rate. The stock wealth tax bar is constant across all three panels, confirming $\gamma$-invariance. Source: WFR simulation model; underlying data from JST dataset. **(WFR.A §B.1)**](../figures/wfr_fig_b4_combined_gamma1.png){width=100%}

---

## Figure 4.1f
*File:* `wfr_fig_b4_combined_gamma2.png`
*Insertion:* §4.1, immediately after Figure 4.1e.

![Figure 4.1f ($\gamma = 2.0$): Same comparison as Figure 4.1e at $\gamma = 2$. Progressive WDT CEW narrows to $-0.787\%$; the flat WDT moves to $-1.754\%$ and the stock wealth tax remains at $-1.887\%$, confirming $\gamma$-invariance for the stock base. The gap between flat and progressive WDT narrows slightly relative to $\gamma = 1$, consistent with the D-M variance-reduction benefit growing with risk aversion for the flat rate but not the progressive at this wealth level. Source: WFR simulation model; underlying data from JST dataset. **(WFR.A §B.1)**](../figures/wfr_fig_b4_combined_gamma2.png){width=100%}

---

## Figure 4.1g
*File:* `wfr_fig_b4_combined_gamma4.png`
*Insertion:* §4.1, immediately after Figure 4.1f.

![Figure 4.1g ($\gamma = 4.0$): Same comparison at $\gamma = 4$. Progressive WDT CEW reaches $-0.720\%$; the flat WDT reaches $-1.622\%$; the stock wealth tax holds at $-1.887\%$. The ordering — progressive WDT lowest welfare cost, then flat WDT, then stock wealth tax — is stable across all three $\gamma$ values, confirming that the C1–C3 complications do not alter the ranking relative to the stock-base benchmark at canonical parameters. Source: WFR simulation model; underlying data from JST dataset. **(WFR.A §B.1)**](../figures/wfr_fig_b4_combined_gamma4.png){width=100%}

---

# Module 3 — CGT Lock-In (§4.2)

## Figure 4.2.1
*File:* `wfr_fig_c1_lock_in_threshold.png`
*Insertion:* §4.2.1, after the paragraph defining $r_B^*$ (ending "…not worth the switching cost given the embedded liability."), before §4.2.2.

![Figure 4.2.1: CGT lock-in threshold at the reference calibration ($V = £10\text{m}$, $G/V = 50\%$, $\tau_{cgt} = 24\%$, $T = 5\text{ yr}$). The yellow curve plots NPV(stay in A) $-$ NPV(switch to B) as a function of asset B's expected return $r_B$. Where the curve is positive, the agent prefers to remain in asset A; where negative, the agent would switch in the absence of CGT. The indifference return $r_B^* = 13.31\%$ (red dashed) is the threshold where the CGT switching cost exactly offsets the return advantage of asset B — the zero crossing of the NPV curve. The shaded lock-in region (pink) spans $r_A = 10.45\%$ (grey dotted) to $r_B^* = 13.31\%$: returns in this band are superior to asset A but not superior enough to justify realising the embedded CGT liability. Source: WFR simulation model; $r_A$ from JST dataset (UK equity mean 1947–2019). **(WFR.A §C.1)**](../figures/wfr_fig_c1_lock_in_threshold.png){width=100%}

---

## Figure 4.2.2a
*File:* `wfr_fig_c4_full_comparison.png`
*Insertion:* §4.2.2, after Table 5 italic note, before "The WDT advantage grows from 1.74 basis points…"

![Figure 4.2.2a: Full welfare comparison — WDT vs CGT with and without lock-in. $\gamma = 2$, Ver. A (UK historical equity, 30-year scenario from 2000), $P(\text{locked in}) = 90.0\%$. Left bar (blue): flat WDT CEW ($-1.754\%$). Centre bar (gold): CGT CEW with no lock-in ($-1.771\%$), matching the §3.1 baseline. Right bar (orange): CGT CEW with endogenous realisation decision ($-3.183\%$); the annotated arrow marks the 141.22 basis-point lock-in cost attributable entirely to the realisation contingency. The WDT advantage of 142.96 basis points with lock-in is the distance from the left bar to the right bar. Source: WFR simulation model; underlying data from JST dataset. **(WFR.A §C.3)**](../figures/wfr_fig_c4_full_comparison.png){width=100%}

---

## Figure 4.2.2b
*File:* `wfr_fig_c2_sensitivity_gain.png`
*Insertion:* §4.2.2, after the P-decomposition paragraph (ending "…understate the role of asset return dynamics."), before "**The T sweep.**"

![Figure 4.2.2b: Sensitivity of CGT lock-in welfare cost and lock-in probability to the embedded gain ratio $G/V$. Left panel (purple): lock-in welfare cost in basis points across $G/V \in [5\%, 90\%]$, Ver. A, $\gamma = 2$, $T = 5$. The cost rises from +16.4 basis points at $G/V = 5\%$ to a peak of +162.2 basis points at $G/V = 76.6\%$, then falls non-monotonically — a discretisation artefact of the finite empirical distribution as $r_B^*$ approaches the upper boundary of the return distribution. Right panel (red): P(agent locked in) as a percentage of return states, showing three step-change levels as additional return states cross into the CGT distortion zone. The baseline 86.7\% locked-in probability below $G/V \approx 36\%$ reflects states where $r_B < r_A$ — market preference, not a tax distortion. Only the incremental probability above that baseline represents the CGT distortion proper. Source: WFR simulation model; underlying data from JST dataset. **(WFR.A §C.1)**](../figures/wfr_fig_c2_sensitivity_gain.png){width=100%}

---

## Figure 4.2.2c
*File:* `wfr_fig_c3_sensitivity_T.png`
*Insertion:* §4.2.2, after the T sweep prose paragraph (ending "…a disadvantage the CGT never fully releases."), before §4.2.3.

![Figure 4.2.2c: Sensitivity of CGT lock-in welfare cost and the indifference return $r_B^*$ to the remaining holding period $T$, at $G/V = 50\%$, Ver. A, $\gamma = 2$. Left panel (purple): lock-in welfare cost in basis points, rising from +56.1 basis points at $T = 1$ to a plateau of +181.1 basis points from $T = 8$ onward. The two intermediate plateaus at $T = 2$–$3$ and $T = 4$–$7$ reflect discrete jumps as $r_B^*$ descends through the empirical return distribution. Right panel (red): $r_B^*$ converges toward $r_A = 10.45\%$ as $T \to \infty$, confirming that the trapped zone collapses asymptotically. The welfare cost is at its maximum precisely when $r_B^*$ has converged close enough to $r_A$ that no additional return state triggers lock-in, because the agent has been trapped across many compounding periods. Source: WFR simulation model; underlying data from JST dataset. **(WFR.A §C.2)**](../figures/wfr_fig_c3_sensitivity_T.png){width=100%}

---

# Module 4 — Heterogeneous Returns (§4.3)

## Figure 4.3.2
*File:* `wfr_fig_d3_concentration_path.png`
*Insertion:* §4.3.2, after the two prose paragraphs discussing Table 8 (ending "…which is why the WDT reaches 286× rather than holding concentration constant."), before §4.3.3.

![Figure 4.3.2: Wealth concentration path — Great-tier / Poor-tier wealth ratio over the 30-year scenario from 2000. Left panel: ratio trajectories by system. The stock wealth tax (red) diverges sharply after 2010, reaching approximately 479× by 2029; income tax (orange) reaches approximately 320×; both WDT variants (blue, dark blue) track close together and reach approximately 286–288×. The two-way split between accrual-base and stock-base systems is visible as early as 2005 and widens monotonically thereafter. Right panel: per-tier wealth growth (normalised to $W_0 = 1$) for WDT (solid lines) vs stock wealth tax (dashed lines). Under WDT the Poor tier (red solid) remains near 1× — the symmetric refund in loss years partially offsets the $-4.55$pp return drag. Under the stock wealth tax (red dashed) the Poor tier dips below 1×: the stock charge is collected regardless of return performance, compounding the loss. Source: WFR simulation model; return differentials from Fagereng et al. (2020); underlying return data from JST dataset. **(WFR.A §D.3)**](../figures/wfr_fig_d3_concentration_path.png){width=100%}

---

## Figure 4.3.3
*File:* `wfr_fig_d1_tier_cew.png`
*Insertion:* §4.3.3, after the two prose paragraphs discussing Table 9 (ending "…γ-invariance result from §3.1 operating uniformly across the wealth distribution."), before §4.3.4.

![Figure 4.3.3: CEW by tier and tax system, $\gamma = 2$, Ver. A (UK historical equity, 30-year scenario from 2000). Left panel (heatmap): each cell reports CEW as a percentage of the no-tax benchmark; redder cells indicate higher welfare cost. The stock wealth and consumption tax rows are uniformly deep red across all tiers, confirming $\gamma$-invariance and the absence of return-conditioned relief. The progressive WDT row is the lightest across all tiers, particularly at the Poor tier ($-0.137\%$), reflecting both the lower effective entry rate and the symmetric refund acting in loss years. Right panel (grouped bars): the same data in bar form, grouped by tier. At the Poor tier, the gap between the symmetric WDT bar (light blue, $-0.219\%$) and the income/CGT bars (gold/orange, $-0.600\%$) is the 38.1-basis-point differential attributable to the symmetric refund. Source: WFR simulation model; tier wealth levels from ONS/WAS brackets; return differentials from Fagereng et al. (2020). **(WFR.A §D.1)**](../figures/wfr_fig_d1_tier_cew.png){width=100%}

---

## Figure 4.3.4
*File:* `wfr_fig_d2_incidence.png`
*Insertion:* §4.3.4, after the prose paragraph discussing Table 10 (ending "…so the wealthier tier pays only slightly more in absolute terms."), before §4.3.5.

![Figure 4.3.4: Distributional incidence — expected tax as a percentage of $W_0$ by tier, all systems revenue-equivalent at $2\%$ of Good-tier $W_0$. The symmetric WDT (blue) has the steepest incidence slope: from $0.34\%$ at the Poor tier to $2.21\%$ at the Great tier (a 6.6:1 ratio), reflecting the delta base scaling with both wealth and the return differential simultaneously. Income tax and CGT (orange/gold) overlap and rise from $0.68\%$ to $2.19\%$ (3.2:1). Stock wealth and consumption tax (red/grey, overlapping) are nearly flat near $1.9\%$–$2.0\%$ across all tiers — the 1.1:1 ratio is the signature of a stock base that conditions on wealth level rather than return performance. The crossover of WDT below income tax at the Poor tier, and above income tax at the Great tier, is the structural consequence of the delta base. Source: WFR simulation model; tier wealth levels from ONS/WAS brackets; return differentials from Fagereng et al. (2020). **(WFR.A §D.2)**](../figures/wfr_fig_d2_incidence.png){width=100%}

---

## Figure 4.3.5
*File:* `wfr_fig_d4_envelope_binding.png`
*Insertion:* §4.3.5, after the paragraph describing the Poor-tier binding result (ending "…the Ok tier's minimum slack is £0.042m, the Good tier's £0.210m, and the Great tier's £2.210m."), before "The policy implication is specific."

![Figure 4.3.5: Lifetime contribution envelope — slack over time by tier (slack = cumulative tax paid $-$ cumulative refunds received; zero = envelope binds). 30-year scenario from 2000, flat symmetric WDT. Top-left (red): Poor tier ($W_0 = £3\text{m}$). The dotted vertical line at 2001 marks the single binding year: the opening-year loss produces a refund obligation before any cumulative tax has been paid, so the floor binds and the refund is capped at zero. Slack becomes strictly positive from 2002 onward. Top-right (orange): Ok tier ($W_0 = £7\text{m}$); minimum slack £0.042m — never binds. Bottom-left (green): Good tier ($W_0 = £21\text{m}$); minimum slack £0.210m — accumulates to approximately £16m by 2029. Bottom-right (blue): Great tier ($W_0 = £151\text{m}$); minimum slack £2.210m — accumulates to over £320m by 2029. Source: WFR simulation model; return differentials from Fagereng et al. (2020); underlying return data from JST dataset. **(WFR.A §D.4)**](../figures/wfr_fig_d4_envelope_binding.png){width=100%}

---

## Figure 4.3.6
*File:* `wfr_fig_d5_corner_check.png`
*Insertion:* §4.3.6, after the paragraph explaining the Corner B "—" entry (ending "…the revenue target remains reachable."), as the section's closing figure before §4.4.

![Figure 4.3.6: Off-diagonal spot check — decoupling $W_0$ from return differential. $\gamma = 2$; revenue target = $2\%$ of each corner's own $W_0$. Each system shows three bars: dark = corner cell (decoupled $W_0$ and return differential); mid-grey = diagonal sharing the corner's $W_0$; light-grey = diagonal sharing the corner's return differential. Left panel (Corner A): Great-tier return differential (+3.45pp) at Poor-tier $W_0$ (£2.86m). All systems show the corner cell below the diagonal sharing the same $W_0$ — applying a high-return differential at low wealth worsens CEW because more revenue is collected against a small base. The Symmetric WDT corner bar is absent: no flat rate achieves the revenue target at this parameter combination. Right panel (Corner B): Poor-tier return differential ($-4.55$pp) at Great-tier $W_0$ (£139.6m). The progressive WDT corner cell (far right) is nearly flat near zero CEW — the logistic entry rate at £139.6m is low enough that the persistent loss generates minimal collection and substantial refund. Source: WFR simulation model; return differentials from Fagereng et al. (2020). **(WFR.A §D.5)**](../figures/wfr_fig_d5_corner_check.png){width=100%}

---

# Module 5 — Sweep Analysis (WFR.A §E)

*Note: All Module 5 figures belong in WFR.A, not in WFR. Figure numbers reference WFR.A section headings. Two cross-reference hooks in WFR.md are noted below each relevant caption.*

## Figure E.1a  *(WFR.A §E.1)*
*File:* `wfr_fig_e1_revenue_target.png`
*Insertion:* WFR.A §E.1, after Table E.1.

![Figure E.1a: CEW by tax system and revenue target $E[T]$ as a percentage of $W_0$, $\gamma = 2$. Left panel: Ver. A (empirical); right panel: Ver. B (idealised). All rankings are stable across the full 1%–5% revenue range: the flat WDT (blue) sits above income tax and CGT (gold/orange, overlapping) in Ver. A at every target; stock wealth and consumption tax (red/grey) sit below all accrual-base systems and are visually coincident, confirming $\gamma$-invariance at every revenue level. The parallel downward slopes confirm that welfare costs scale approximately linearly with revenue extracted and that no ranking reversal occurs as the revenue burden rises. Source: WFR simulation model; underlying data from JST dataset. **(WFR.A §E.1)**](../figures/wfr_fig_e1_revenue_target.png){width=100%}

---

## Figure E.1b  *(WFR.A §E.1)*
*File:* `wfr_fig_e1b_w0_sensitivity.png`
*Insertion:* WFR.A §E.1, immediately after Figure E.1a.

![Figure E.1b: CEW vs initial wealth $W_0$ across systems, $E[T] = 2\%$ of $W_0$, $\gamma = 2$, Ver. A. All series are flat across the full $W_0$ range from £3m to £140m — CEW is invariant to initial wealth under the flat-rate revenue-equivalence design. The two-cluster structure from (WFR.A §A.1) is reproduced: WDT, income tax, and CGT cluster near $-1.75\%$; stock wealth and consumption tax sit at approximately $-1.885\%$. The scale invariance follows from normalising revenue to $2\%$ of $W_0$ at each wealth level: the tax burden is held proportionally constant, and CRRA preferences make the welfare outcome depend only on the relative burden. Source: WFR simulation model; underlying data from JST dataset. **(WFR.A §E.1)**](../figures/wfr_fig_e1b_w0_sensitivity.png){width=100%}

---

## Figure E.2.1  *(WFR.A §E.2.1)*
*File:* `wfr_fig_e2a_start_year_distribution.png`
*Insertion:* WFR.A §E.2.1, after Table E.2.1.
*WFR cross-reference hook:* none (summary statistics only cross-referenced to WFR.A).

![Figure E.2.1: Distribution of CEW across all 73 start-year windows (1947–2019), 30-year windows with wrap-around, $E[T] = 2\%$ of $W_0$, $\gamma = 2$. Box shows interquartile range; white line = median; whiskers extend to min and max. The flat WDT (blue) has the highest median CEW ($-1.672\%$) and the highest minimum CEW ($-1.765\%$) of any system, leading in 100\% of historical windows. The WDT median advantage over the stock wealth tax is +14.2 basis points (annotated). Stock wealth and consumption tax boxes (red/grey) sit entirely below the other systems with tight spreads — their near-flat revenue profile generates low variance in CEW across start years but consistently worse outcomes. Income tax and CGT boxes (orange/gold) are similar in spread to the WDT but shifted downward, confirming the 17-basis-point advantage from §3.1 holds across all historical windows. Source: WFR simulation model; underlying data from JST dataset (UK equity returns 1947–2019). **(WFR.A §E.2.1)**](../figures/wfr_fig_e2a_start_year_distribution.png){width=100%}

---

## Figure E.2.2  *(WFR.A §E.2.2)*
*File:* `wfr_fig_e2b_timeseries.png`
*Insertion:* WFR.A §E.2.2, after Table E.2.2.
*WFR cross-reference hook:* §4.3.5, at "the full start-year distribution is in (WFR.A §E.2)" → append "(Figure E.2.2)".

![Figure E.2.2: CEW by scenario start year — all 73 historical 30-year windows, $E[T] = 2\%$ of $W_0$, $\gamma = 2$. The vertical dashed line marks the canonical 2000 start year. The flat WDT (blue) and income/CGT (gold/orange, overlapping) track closely throughout, with the WDT holding a consistent narrow lead visible from approximately 1975 onward. Consumption tax (grey) declines monotonically from left to right, reaching its worst outcome near the 2000 start year before partially recovering — the decline reflects the increasing weight of post-2000 loss years in windows starting later. Stock wealth tax coincides with consumption tax at this scale and is not separately visible. The WDT's resilience across adverse windows — 1972 (oil shock), 1987, 2000 — reflects the symmetric refund acting in the loss years that characterise each adverse period. Source: WFR simulation model; underlying data from JST dataset (UK equity returns 1947–2019). **(WFR.A §E.2.2)**](../figures/wfr_fig_e2b_timeseries.png){width=100%}

---

## Figure E.3.1  *(WFR.A §E.3.1)*
*File:* `wfr_fig_e3a_tau0.png`
*Insertion:* WFR.A §E.3.1, after Table E.3.1.
*WFR cross-reference hook:* §4.1 C1, at "(WFR.A §E.3.1–§E.3.4)" → append "(Figures E.3.1–E.3.4)".

![Figure E.3.1: Progressive vs flat WDT CEW gap (flat $-$ progressive, basis points) as a function of the entry rate $\tau_0$, at three wealth levels ($W_0 = £10\text{m}$, £30m, £100m). All values are negative throughout — progressive WDT is marginally better than flat at all $\tau_0$ levels tested. The gap rises toward zero as $\tau_0$ increases because a higher entry rate means the progressive schedule begins closer to the flat revenue-equivalent rate. The $W_0 = £100\text{m}$ series (blue) shows the largest gap at low $\tau_0$: at higher wealth the logistic is marginally further up its curve, so the progressive advantage is marginally more visible, but the maximum gap of approximately $-0.0075$ basis points confirms the C1 complication remains second-order throughout. Source: WFR simulation model; $\tau_m = 70\%$, $k = 0.001$, $W_{min} = £2\text{m}$ held at canonical values. **(WFR.A §E.3.1)**](../figures/wfr_fig_e3a_tau0.png){width=100%}

---

## Figure E.3.2  *(WFR.A §E.3.2)*
*File:* `wfr_fig_e3b_taum.png`
*Insertion:* WFR.A §E.3.2, after Table E.3.2.

![Figure E.3.2: Progressive vs flat WDT CEW gap as a function of the ceiling rate $\tau_m$, at three wealth levels. All gaps remain negative throughout. The $W_0 = £10\text{m}$ (orange) and $W_0 = £30\text{m}$ (green) series are nearly flat and close to zero across the full $\tau_m$ range: raising the ceiling has almost no effect at these wealth levels because they sit far below the inflection point regardless of the ceiling value. The $W_0 = £100\text{m}$ series (blue) shows a monotone decline as $\tau_m$ rises — a higher ceiling steepens the logistic curve and makes the progressive schedule collect slightly more in gain years while refunding at the lower post-loss effective rate, marginally widening the C1 complication. Even at $\tau_m = 90\%$ and $W_0 = £100\text{m}$, the gap remains below $-0.007$ basis points. Source: WFR simulation model; $\tau_0 = 15\%$, $k = 0.001$, $W_{min} = £2\text{m}$ held at canonical values. **(WFR.A §E.3.2)**](../figures/wfr_fig_e3b_taum.png){width=100%}

---

## Figure E.3.3  *(WFR.A §E.3.3)*
*File:* `wfr_fig_e3c_k.png`
*Insertion:* WFR.A §E.3.3, after Table E.3.3.

![Figure E.3.3: Progressive vs flat WDT CEW gap as a function of the logistic steepness parameter $k$ (per £m), at three wealth levels. At very low $k$ (near-flat schedule), the gap is small and negative at all wealth levels. As $k$ increases, paths diverge sharply: the $W_0 = £100\text{m}$ series (blue) reaches a minimum around $k = 0.01$ before recovering toward zero at $k = 0.05$; the $W_0 = £30\text{m}$ series (green) continues declining throughout; the $W_0 = £10\text{m}$ series (orange) remains relatively flat. The crossing of the blue and green/orange series at high $k$ occurs because at very steep logistic curves, a £100m agent sits above the inflection point where gain and refund rates reconverge near the ceiling. Within the canonical range ($k = 0.001$), all gaps are negligible. Source: WFR simulation model; $\tau_0 = 15\%$, $\tau_m = 70\%$, $W_{min} = £2\text{m}$ held at canonical values. **(WFR.A §E.3.3)**](../figures/wfr_fig_e3c_k.png){width=100%}

---

## Figure E.3.4  *(WFR.A §E.3.4)*
*File:* `wfr_fig_e3d_wmin.png`
*Insertion:* WFR.A §E.3.4, after Table E.3.4.

![Figure E.3.4: Progressive vs flat WDT CEW gap as a function of the entry threshold $W_{min}$ (£m), at three wealth levels. The $W_0 = £30\text{m}$ (green) and $W_0 = £100\text{m}$ (blue) series are flat at zero throughout — raising $W_{min}$ has no effect when $W_0$ is well above the threshold. The $W_0 = £10\text{m}$ series (orange) is zero at $W_{min} \leq £5\text{m}$ but rises sharply once $W_{min}$ approaches $W_0$: when $W_{min} = £10\text{m}$, the agent sits exactly at the entry threshold and the progressive schedule applies only the entry rate $\tau_0$, while the flat revenue-equivalent rate calibrated to the full population is higher — at this point the flat WDT has higher welfare cost than the progressive (+1.74 basis points). This is the only parameter combination in Sweep C where the gap turns positive, and it requires $W_{min} \approx W_0$. Source: WFR simulation model; $\tau_0 = 15\%$, $\tau_m = 70\%$, $k = 0.001$ held at canonical values. **(WFR.A §E.3.4)**](../figures/wfr_fig_e3d_wmin.png){width=100%}