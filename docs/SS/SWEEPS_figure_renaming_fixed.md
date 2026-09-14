# SWEEPS Figure Renaming — Working Document

For each figure: current name → suggested new name, section, appendix ref, filename (for code),
and the full caption text to edit. Fill in your new name and appendix refs, then return for
the paper update pass.

Format: `Figure §N.n (caption) (SWEEPS.A §X.X)`

---

## Figure 1

**Current name:** S3.1a
**Section:** §2.2
**Suggested new name:** Figure §2.2a
**Appendix ref:** SWEEPS.A Table B.4.5
**Filename:** `sweeps_v_fig_s2_2a_n_crossing_annotated.png`

**Caption:**
Overstater advantage erosion and N-crossing thresholds at canonical parameters — two-panel. Left panel: Net($\alpha$) − Net(honest) in £m plotted against holding period N at $g$ = 10.4%; negative values indicate the overstater pays less net tax than honest declaration. All three overstater lines ($\alpha$ = 1.5, 1.8, 2.0) begin negative — the advantage is active from early periods — and then cross zero as the self-limiting mechanism accumulates: $\alpha$ = 1.5 at approximately N = 21, $\alpha$ = 1.8 at approximately N = 20, $\alpha$ = 2.0 at approximately N = 20 (Table B.4.5). Beyond the crossing, the lines turn sharply positive: the mechanism is not merely self-limiting but imposes a growing cost on aggressive overstatement at long holding horizons. The N = 30 reference line (RATES ref) marks the outer edge of the capitalisation period. Right panel: bar chart of the first N-crossing for each $\alpha$. $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, $V_0$ = £20m (SWEEPS.A Table B.4.5).

---

## Figure 2

**Current name:** S3.1c
**Section:** §2.2
**Suggested new name:** Figure §2.2b
**Appendix ref:** SWEEPS.A Table B.2.4
**Filename:** `sweeps_v_fig_s2_2b_n_tolerant_zone.png`

**Caption:**
Tolerant-zone (|C.1| < 2pp) $\alpha$ boundaries across holding period N at canonical growth $g$ = 10.4%. The shaded band is the $\alpha$ range within which all declaration strategies produce approximately the same lifetime tax outcome as honest declaration. The lower boundary (blue line) starts near $\tau_0$ at short horizons, falls to a minimum near N = 10, remains near that floor through mid-range N, then partially recovers at long horizons — the recovery does not reach the VAL.A lower bound ($\alpha$ = 0.8, dotted). The upper boundary (red line) expands steeply to a peak near N = 13, then contracts continuously through the N = 30 canonical reference and on toward long horizons — there is no post-contraction recovery in the tested range (Table B.2.4). The VAL.A canonical tolerant-zone bounds ($\alpha$ = 0.8 lower, $\alpha$ = 1.5 upper, dotted horizontals) are reproduced for reference; they correspond to the N = 30 canonical panel. $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001.

---

## Figure 3

**Current name:** S3.1b
**Section:** §2.3
**Suggested new name:** Figure §2.3
**Appendix ref:** SWEEPS.A Table B.2.6
**Filename:** `sweeps_v_fig_s2_3_n_understater_panels.png`

**Caption:**
Understater penalty profile across holding periods — four-panel. Each panel plots C.1 (pp) against growth rate $g$ for four understater $\alpha$ values at a given N. At N = 10 (upper left), penalties are moderate and monotonically declining in $g$ across the plotted range: the mechanism has not yet had enough periods to compound the deferred liability into a large C.1 value, and at high growth rates the rapid expansion of the denominator (terminal wealth) partially offsets the growing absolute penalty. At N = 20 (upper right) the plateau structure begins to emerge for the most egregious understater. At N = 30 (lower left, canonical, bold), a pronounced peak is visible for $\alpha$ = 0.1 — the line rises from low values at $g$ = 0%, peaks at a high-growth $g$ in the low-to-mid twenties, then descends at $g$ = 35%, reflecting the interaction between the rate ceiling and the growing terminal-wealth denominator (Table B.2.6). At N = 50 (lower right) the peak shape is essentially identical: adding twenty years beyond the canonical horizon does not materially change the peak height or its location. $\alpha$ = 0.8 (mild understatement) remains near zero throughout all four panels, confirming that the plateau structure is specific to egregious understatement. $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, $V_0$ = £20m.

---

## Figure 4

**Current name:** RATES.S-5
**Section:** §2.4
**Suggested new name:** Figure §2.4
**Appendix ref:** —
**Filename:** `sweeps_r_fig_s2_4_rate_function_shapes.png`

**Caption:**
Rate function shape $\tau(W)$ across the wealth range — four-panel, one per parameter. Each line shows the marginal rate curve at one parameter value, with all other parameters held at the Balanced baseline; the baseline curve is shown as a red dashed line in each panel. Top left ($\tau_0$): raising $\tau_0$ lifts the entire curve in parallel — the family of curves fans out from the y-intercept while all converging toward $\tau_m$ = 70% at extreme wealth. Top right ($\tau_m$): raising $\tau_m$ pulls the ceiling upward — curves fan out at high wealth while sharing the same floor $\tau_0$ = 15%. The separation between lines is entirely in the upper wealth range, making visible why $\tau_m$ is fiscally inert at canonical k: no bracket approaches the range where the curves diverge. Bottom left (k, log-spaced): at low $k$ the curve is nearly flat across the full range; at high $k$ it rises steeply near $W_{min}$ and approaches $\tau_m$ quickly. The baseline $k$ = 0.001 (bold) sits in the moderate-slope region. Bottom right ($W_{min}$): all lines are nearly identical once above the onset point — the curves differ only in where they start, and above the highest tested $W_{min}$ the family converges completely. This confirms graphically that $W_{min}$ shifts the scope of the mechanism without changing what it does to in-scope taxpayers. $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, $W_{min}$ = £2m (baseline in each panel).

---

## Figure 5

**Current name:** S2.1a
**Section:** §3.1
**Suggested new name:** Figure §3.1a
**Appendix ref:** —
**Filename:** `sweeps_v_fig_s3_1a_tau0_heatmaps.png`

**Caption:**
C.1 advantage landscape across $\tau_0$ values — four-panel heatmap. Each cell reports $(Net(\alpha) - Net(1) / TW(\alpha)$ in percentage points. Red cells indicate the declaration strategy costs more than honest declaration; blue cells indicate it costs less. The canonical panel ($\tau_0$ = 15%, bold border) is reproduced from (VAL.A §C.1). Understater rows ($\alpha$ < 1.0) intensify monotonically with $\tau_0$ across all growth rates. Overstater rows ($\alpha$ > 1.0) show positive C.1 values at canonical growth and above — the correction is active at N = 30 — and intensify as $\tau_0$ rises, consistent with the crossing arriving earlier at higher floor rates. $\tau_m$ = 70%, $k$ = 0.001, N = 30, $V_0$ = £20m; $\alpha$ = 1.0 row is zero by construction.

---

## Figure 6

**Current name:** S2.1b
**Section:** §3.1
**Suggested new name:** Figure §3.1b
**Appendix ref:** SWEEPS.A Table B.3.3
**Filename:** `sweeps_v_fig_s3_1b_tau0_n_crossings.png`

**Caption:**
N-crossing thresholds by $\tau_0$ for $\alpha$ ∈ {1.5, 1.8, 2.0} at $g$ = 10.4%. The y-axis is the first holding period N at which the overstater's lifetime net tax first exceeds honest declaration. The N = 30 reference line (dotted horizontal) is the RATES reference horizon, not a pass/fail threshold. All three $\alpha$ lines cross well before N = 30 at canonical $\tau_0$ (dotted vertical) and shift to earlier crossings as $\tau_0$ rises — the decision to raise $\tau_0$ is simultaneously a decision to accelerate the self-correction for aggressive overstaters (Table B.3.3). Crossings are present across the full tested $\tau_0$ range. $\tau_m$ = 70%, $k$ = 0.001, $V_0$ = £20m.

---

## Figure 7

**Current name:** S2.1c
**Section:** §3.1
**Suggested new name:** Figure §3.1c
**Appendix ref:** —
**Filename:** `sweeps_v_fig_s3_1c_tau0_tolerant_zone.png`

**Caption:**
Tolerant-zone (|C.1| < 2pp) $\alpha$ boundaries as a function of $\tau_0$. The shaded band is the $\alpha$ range within which all declaration strategies produce approximately the same lifetime tax outcome as honest declaration at canonical growth $g$ = 10.4%. The lower boundary (blue line) is flat near the test floor through approximately mid-range $\tau_0$, then rises sharply as $\tau_0$ continues to increase — approaching the VAL.A lower bound at the upper end of the sweep. The upper boundary (red line) declines continuously from the low-$\tau_0$ end through canonical $\tau_0$ and on to the high end — there is no stable plateau; the zone narrows from the top throughout the full sweep. Canonical $\tau_0$ is marked by the dotted vertical; $\alpha$ = 1.0 (honest declaration) by the dotted horizontal. $\tau_m$ = 70%, $k$ = 0.001, N = 30.

---

## Figure 8

**Current name:** S4.1
**Section:** §3.1
**Suggested new name:** Figure §3.1d
**Appendix ref:** SWEEPS.A Table B.3.5
**Filename:** `sweeps_v_fig_s3_1d_tau0_n_surface.png`

**Caption:**
Joint surface — N-crossing threshold for $\alpha$ = 2.0 across ($\tau_0$, N sweep ceiling). The x-axis is the entry rate $\tau_0$ (%); the y-axis is the maximum holding period N tested. Each cell shows the first N at which the aggressive overstater's ($\alpha$ = 2.0) lifetime net tax exceeds honest declaration at $g$ = 10.4% (Table B.3.5). The canonical $\tau_0$ (vertical dashed line) and the canonical N = 30 reference (horizontal dotted line) are marked. As $\tau_0$ rises across the sweep, crossing thresholds fall monotonically — at the low end crossings arrive near the canonical reference; at the high end they are pulled substantially earlier. A grey no-crossing region exists in the upper-left corner at low $\tau_0$ and low N sweep ceilings. The surface shows the decision to raise $\tau_0$ is simultaneously a decision to bring the self-correction forward: higher floor rates accelerate the arrival of the correction for aggressive overstaters. $\tau_m$ = 70%, $k$ = 0.001, $V_0$ = £20m.

---

## Figure 9

**Current name:** RATES.S-1
**Section:** §3.2
**Suggested new name:** Figure §3.2
**Appendix ref:** —
**Filename:** `sweeps_r_fig_s3_2_tau0_sensitivity.png`

**Caption:**
Parameter sensitivity — $\tau_0$ (floor rate). Four-panel RATES.S output across the full $\tau_0$ sweep. Shaded bands show min–max across 73 historical start years; lines show medians; canonical $\tau_0$ is marked by the red dotted vertical. Top left: SSM coverage ratio (blue, correlated-shock floor) and TCM coverage ratio (orange, heterogeneity ceiling) both rise with $\tau_0$ — median coverage is above 100% expenditure coverage at canonical parameters and continues rising across the sweep; the SSM and TCM medians track closely together. Top right: median LRR fill year falls steeply from the high end of the sweep to the low end; the shaded band narrows as $\tau_0$ rises, indicating that higher floor rates reduce start-year sensitivity. Bottom left: LRR surplus at fill is broadly stable with high variance — the surplus is not a simple monotone function of $\tau_0$, reflecting interaction between fill timing and the position of the capitalisation window in the return sequence. Bottom right: taxpayer burden rises monotonically across the sweep; the effective rate on gains rises proportionally. $\tau_m$ = 70%, $k$ = 0.001, $W_{min}$ = £2m.

---

## Figure 10

**Current name:** S2.2a
**Section:** §4.1
**Suggested new name:** Figure §4.1a
**Appendix ref:** —
**Filename:** `sweeps_v_fig_s4_1a_taum_heatmaps.png`

**Caption:**
C.1 advantage landscape across $\tau_m$ values — four-panel heatmap. Each cell reports $(Net(\alpha) - Net(1) / TW(\alpha)$ in percentage points. The canonical panel ($\tau_m$ = 70%, bold border) is reproduced from (VAL.A §C.1). The interior of all four panels — moderate $\alpha$, moderate $g$ — is nearly identical: the tolerant zone is stable across the full sweep and overstater rows show almost no response to $\tau_m$ changes. The strong effect is concentrated in the extreme understater rows ($\alpha$ = 0.1, 0.2) at high growth rates (g ≥ 16.4%), where penalty magnitudes intensify dramatically from $\tau_m$ = 50% to $\tau_m$ = 80%. $\tau_0$ = 15%, $k$ = 0.001, N = 30, $V_0$ = £20m; $\alpha$ = 1.0 row is zero by construction.

---

## Figure 11

**Current name:** S2.2b
**Section:** §4.1
**Suggested new name:** Figure §4.1b
**Appendix ref:** SWEEPS.A Table B.4.3
**Filename:** `sweeps_v_fig_s4_1b_taum_penalty_plateaus.png`

**Caption:**
Understater penalty plateau ceiling by $\alpha$ and $\tau_m$. The y-axis is the maximum C.1 value reached at the high end of the growth sweep — the plateau that the rate function's ceiling imposes on egregious understaters. All four lines converge near zero at $\alpha$ = 0.8 (mild understatement), confirming $\tau_m$ has near-zero leverage on the compliant middle. The separation is largest at $\alpha$ = 0.1 (most egregious), rising monotonically from the $\tau_m$ = 50% line through canonical $\tau_m$ to $\tau_m$ = 80% (Table B.4.3). The x-axis represents $\alpha$ as a percentage (10 = $\alpha$ = 0.1; 80 = $\alpha$ = 0.8); all lines converge near zero by $\alpha$ = 80%. The plateau ceiling is a monotone function of both $\tau_m$ and the degree of understatement. $\tau_0$ = 15%, $k$ = 0.001, N = 30.

---

## Figure 12

**Current name:** S2.2c
**Section:** §4.1
**Suggested new name:** Figure §4.1c
**Appendix ref:** —
**Filename:** `sweeps_v_fig_s4_1c_taum_n_crossings.png`

**Caption:**
N-crossing thresholds by $\tau_m$ for $\alpha$ ∈ {1.5, 1.8, 2.0} at $g$ = 10.4%. The y-axis is the first holding period N at which the overstater's lifetime net tax first exceeds honest declaration. All three lines are nearly flat as $\tau_m$ varies — the total movement across the full sweep is small relative to the movement produced by a comparable $\tau_0$ sweep (compare Fig §3.1b). All three $\alpha$ values cross within the tested range. Canonical $\tau_m$ is marked by the dotted vertical. $\tau_0$ = 15%, $k$ = 0.001, $V_0$ = £20m.

---

## Figure 13

**Current name:** RATES.S-2
**Section:** §4.2
**Suggested new name:** Figure §4.2
**Appendix ref:** —
**Filename:** `sweeps_r_fig_s4_2_taum_sensitivity.png`

**Caption:**
Parameter sensitivity — $\tau_m$ (ceiling rate). Four-panel RATES.S output across the full $\tau_m$ sweep from 50% to 100%. All four panels are essentially flat across the entire sweep range; canonical $\tau_m$ is marked by the red dotted vertical. Top left: SSM coverage (blue) and TCM coverage (orange) lines are horizontal — the shaded min–max bands are wide due to start-year variation but the medians do not move with $\tau_m$. Top right: median LRR fill year holds at a stable level throughout. Bottom left: LRR surplus at fill is flat. Bottom right: taxpayer burden (annual wealth burden and effective rate on gains) is flat — the $\tau_m$ sweep does not alter what any bracket actually pays during the capitalisation window. The four flat panels are the visual confirmation of the fiscal inertness claim: $\tau_m$ is a declaration-side lever with no fiscal consequence for the modelled population. $\tau_0$ = 15%, $k$ = 0.001, $W_{min}$ = £2m.

---

## Figure 14

**Current name:** S2.3a
**Section:** §5 (section intro, before §5.1)
**Suggested new name:** Figure §5a
**Appendix ref:** —
**Filename:** `sweeps_v_fig_s5a_k_rate_curves.png`

**Caption:**
Rate curve $\tau(W)$ across four $k$ values on a log wealth axis. All four curves share $\tau_0$ = 15% at $W_{min}$ = £2m and approach $\tau_m$ = 70% asymptotically. The $V_0$ = £20m reference point (dotted vertical) sits on the flat lower portion of all four curves: at canonical $k$ = 0.001 (solid purple) the marginal rate at £20m is barely above $\tau_0$. The three lower-k curves (dashed) remain near $\tau_0$ across the entire plotted range — reaching only approximately 21%, 29%, and 54% at £5bn for $k$ = 0.0001, 0.0002, and 0.0005 respectively. The canonical curve rises steeply through £500m–£2bn, demonstrating that at canonical $k$ the mechanism becomes genuinely progressive only at extreme wealth. $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

---

## Figure 15

**Current name:** S2.3b
**Section:** §5.1
**Suggested new name:** Figure §5.1a
**Appendix ref:** —
**Filename:** `sweeps_v_fig_s5_1a_k_heatmaps.png`

**Caption:**
C.1 advantage landscape across $k$ values — four-panel heatmap. Each cell reports $(Net(\alpha) - Net(1) / TW(\alpha)$ in percentage points. The canonical panel (k = 0.001, bold border) is reproduced from (VAL.A §C.1). At $k$ = 0.0001 the landscape is nearly flat: the $\alpha$ = 0.1, $g$ = 25.4% understater cell reaches approximately 4.9pp; at high $g$ overstater cells show small negative C.1 values — a mild advantage that disappears as $k$ rises. As $k$ rises, the tails intensify in both directions while the interior remains moderate. Understater rows remain red throughout; overstater rows at canonical growth show positive C.1 values (correction active at N = 30) that intensify with $k$, confirming that $k$ changes magnitude without altering the direction of the self-correction. $\tau_0$ = 15%, $\tau_m$ = 70%, N = 30, $V_0$ = £20m; $\alpha$ = 1.0 row is zero by construction.

---

## Figure 16

**Current name:** S4.2
**Section:** §5.1
**Suggested new name:** Figure §5.1b
**Appendix ref:** —
**Filename:** `sweeps_v_fig_s5_1b_k_v0_surface.png`

**Caption:**
Joint surface — bracket penalty (C.1) for $\alpha$ = 1.8 across (k, $V_0$). The x-axis is entry wealth $V_0$; the y-axis is steepness parameter $k$ (log-spaced). Each cell shows C.1 at $\alpha$ = 1.8 and $g$ = 10.4%, N = 30; positive values (red) indicate the overstater pays more than honest declaration (correction active), near-zero values indicate the correction has not yet materially activated. The canonical cell (k = 0.001, $V_0$ = £20m, bold border) reads +1.7pp — the correction is already active at this $\alpha$, k, and $V_0$ combination at N = 30. The surface is positive throughout: the self-limiting mechanism has activated for $\alpha$ = 1.8 overstaters at all tested (k, $V_0$) combinations at this holding horizon. Values are smallest in the upper-left (low k, low $V_0$) and rise steeply toward the lower-right (high k, high $V_0$), where steepness concentrates bracket effects on wealthier positions. The non-monotonicity visible at intermediate $k$ for some $V_0$ levels reflects the sensitivity of the correction to where on the logistic curve the taxpayer sits. $\tau_0$ = 15%, $\tau_m$ = 70%, N = 30.

---

## Figure 17

**Current name:** S2.3c
**Section:** §5.1
**Suggested new name:** Figure §5.1c
**Appendix ref:** —
**Filename:** `sweeps_v_fig_s5_1c_k_bracket_penalty.png`

**Caption:**
Bracket penalty for $\alpha$ = 1.8 by $k$ and $V_0$. The y-axis is C.1 at $\alpha$ = 1.8 and $g$ = 10.4%; positive values indicate the overstater pays more than honest declaration (correction active). The three wealth levels show qualitatively different k-dependence. $V_0$ = £20m (blue) sits near the lower end throughout — near-threshold taxpayers show modest correction magnitudes, confirming that the reference taxpayer's position on the rate curve barely shifts as steepness changes. $V_0$ = £100m (red) and $V_0$ = £500m (purple) show larger corrections that intensify with $k$. All wealth levels show non-zero correction at N = 30. The $V_0$ = £100m (red) and $V_0$ = £500m (purple) lines show non-monotone k-dependence, peaking near $k$ ≈ 0.0004 and dipping to a local minimum near canonical $k$ = 0.001 before rising again. $\tau_0$ = 15%, $\tau_m$ = 70%, N = 30.

---

## Figure 18

**Current name:** RATES.S-3
**Section:** §5.2
**Suggested new name:** Figure §5.2
**Appendix ref:** —
**Filename:** `sweeps_r_fig_s5_2_k_sensitivity.png`

**Caption:**
Parameter sensitivity — $k$ (steepness, per £m, log x-axis). Four-panel RATES.S output across nine log-spaced $k$ values from 0.0001 to 0.1. The canonical $k$ = 0.001 is marked by the red dotted vertical. Top left: SSM and TCM coverage medians are broadly stable through the lower portion of the sweep before rising at high $k$; the shaded bands widen at high $k$, reflecting increasing start-year sensitivity as steep curves concentrate revenue on high-growth assets with volatile return sequences. Top right: median LRR fill year is flat through the lower portion of the sweep, then falls modestly at high $k$ values. Bottom left: LRR surplus at fill is broadly stable with slightly elevated variance at high $k$. Bottom right: taxpayer burden diverges dramatically at high $k$ — the max band (highest burden taxpayer in the distribution) rises steeply above the mid-sweep range, reflecting the concentration of progressive rate structure on wealthier positions; the median and 25th percentile are largely unchanged, confirming that $k$ redistributes burden within the taxable population rather than lifting all burdens uniformly. $\tau_0$ = 15%, $\tau_m$ = 70%, $W_{min}$ = £2m.

---

## Figure 19

**Current name:** S2.4a
**Section:** §6 (section intro, before §6.1)
**Suggested new name:** Figure §6a
**Appendix ref:** —
**Filename:** `sweeps_v_fig_s6a_wmin_rate_curves.png`

**Caption:**
Rate curve $\tau(W)$ across four $W_{min}$ values on a log wealth axis. All four curves share $\tau_0$ = 15%, $\tau_m$ = 70%, and $k$ = 0.001; they differ only in the onset point at which the logistic function activates. Below $W_{min}$ the rate is zero. The $V_0$ = £20m reference point (dotted vertical) sits well above every tested $W_{min}$ value: shifting $W_{min}$ between £0m and £5m moves the onset but does not change the curve's shape above it, and the reference taxpayer's position on the rate curve is essentially unchanged. At $W_{min}$ = £2m (canonical, solid purple), $V_0$ = £20m sits on the flat lower portion of the logistic at approximately $\tau_0$. The onset-shift comparison makes visible why $W_{min}$ has near-zero leverage on declaration incentives for taxpayers well above the threshold: once a taxpayer is in scope, the rate they face is determined by the curve's shape above $W_{min}$, not by where the onset is. $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001.

---

## Figure 20

**Current name:** S2.4b
**Section:** §6.1
**Suggested new name:** Figure §6.1a
**Appendix ref:** —
**Filename:** `sweeps_v_fig_s6_1a_wmin_heatmaps.png`

**Caption:**
C.1 advantage landscape across $W_{min}$ values — four-panel heatmap. Each cell reports $(Net(\alpha) - Net(1) / TW(\alpha)$ in percentage points. The canonical panel ($W_{min}$ = £2m, bold border) is reproduced from (VAL.A §C.1). The $W_{min}$ = £0m and $W_{min}$ = £1m panels are visually identical to the canonical panel: the landscape is unchanged because $V_0$ = £20m sits above all three thresholds and the rate curve's shape above each $W_{min}$ is the same. The $W_{min}$ = £5m panel introduces one structural difference: at negative growth rates, $V_0$ = £20m can fall below $W_{min}$ in early periods, producing zero liability in the leftmost $g$ column for the most egregious understater rows ($\alpha$ = 0.1 and $\alpha$ = 0.2) — the white cells in the upper-left corner. Interior cells at moderate $\alpha$ and moderate $g$ remain stable across all four panels, confirming that $W_{min}$'s effect on declaration incentives for in-scope taxpayers is negligible. $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, N = 30, $V_0$ = £20m; $\alpha$ = 1.0 row is zero by construction.

---

## Figure 21

**Current name:** S2.4c
**Section:** §6.1
**Suggested new name:** Figure §6.1b
**Appendix ref:** SWEEPS.A Table B.8.5
**Filename:** `sweeps_v_fig_s6_1b_wmin_n_crossings.png`

**Caption:**
N-crossing thresholds by $W_{min}$ for $\alpha$ ∈ {1.5, 1.8, 2.0} at $g$ = 10.4%. The y-axis is the first holding period N at which the overstater's lifetime net tax first exceeds honest declaration. All three lines are essentially flat across the full $W_{min}$ sweep from £0m to £10m: the crossing threshold for $\alpha$ = 1.5 holds at approximately 20.8, $\alpha$ = 1.8 at approximately 20.0, and $\alpha$ = 2.0 at approximately 19.5 regardless of where the entry threshold sits (Table B.8.5). All three cross well before N = 30. The N = 30 reference line (dotted horizontal) and the $W_{min}$ = £2m canonical value (dotted vertical) are marked. The flat trajectories confirm the key finding from the C.1 heatmaps: $W_{min}$ does not affect the timing of the self-limiting correction for overstaters, because the mechanism's temporal dynamics are driven by the rate curve's shape above $W_{min}$, which is invariant to $W_{min}$'s position. $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, $V_0$ = £20m.

---

## Figure 22

**Current name:** RATES.S-4
**Section:** §6.2
**Suggested new name:** Figure §6.2
**Appendix ref:** —
**Filename:** `sweeps_r_fig_s6_2_wmin_sensitivity.png`

**Caption:**
Parameter sensitivity — $W_{min}$ (entry point, £m). Four-panel RATES.S output across $W_{min}$ values from £0m to £10m. The canonical $W_{min}$ = £2m is marked by the red dotted vertical. Top left: SSM and TCM coverage both rise as $W_{min}$ rises — at very low $W_{min}$ median coverage sits below 100% expenditure coverage, but as $W_{min}$ rises and fewer lower-wealth taxpayers enter scope, coverage climbs steeply to high multiples at $W_{min}$ = £10m; the effect reflects the denominator shift: when only upper-bracket taxpayers remain in scope, the capitalisation window opens later in the budget growth trajectory. Top right: median LRR fill year rises monotonically from the low end to the high end of the sweep — the largest LRR fill year range of any single-parameter sweep. The shaded band widens at high $W_{min}$, reflecting greater start-year sensitivity when the taxable population is small. Bottom left: LRR surplus at fill rises at high $W_{min}$ values — a consequence of the late fill timing coinciding with a later, higher-revenue portion of the return sequence. Bottom right: taxpayer burden falls monotonically as $W_{min}$ rises — as fewer taxpayers enter scope the median and lower percentile burden approach zero; at very high $W_{min}$ essentially the entire lower distribution drops out of liability. $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001.

---

## Figure 23

**Current name:** S4.3
**Section:** §7.1
**Suggested new name:** Figure §7.1
**Appendix ref:** —
**Filename:** `sweeps_v_fig_s7_1_calibration_summary.png`

**Caption:**
Governing Council calibration summary — three mechanism-integrity properties across all rate-function parameter variants. Three bar-chart panels share a common x-axis grouping by parameter ($\tau_0$ group blue; $\tau_m$ group red; $k$ group purple; $W_{min}$ group green); bold borders mark canonical values. Top panel: tolerant-zone width (% of $\alpha$ range where |C.1| < 2pp). $\tau_0$ narrows the zone progressively across the tested range. $\tau_m$ variants are essentially flat. $k$ produces the largest variation: width is elevated at low $k$ and falls sharply at high $k$. $W_{min}$ variants are broadly flat. Middle panel: N-crossing threshold for $\alpha$ = 1.8 (years; lower = correction activates earlier). $\tau_0$ brings the crossing earlier across its tested range; $\tau_m$ variants shift the crossing by a small amount; $k$ shows the widest range across its sweep; $W_{min}$ variants are flat. Bottom panel: understater penalty plateau ceiling at $\alpha$ = 0.1 at high growth ($g$ > 17%, pp). $\tau_m$ dominates: the ceiling rises monotonically from the low-$\tau_m$ to high-$\tau_m$ end of the sweep. $\tau_0$ shows a substantial secondary effect. $k$ variants are broadly flat near the canonical value. $W_{min}$ is broadly flat with the high-$W_{min}$ variant somewhat elevated. The three panels together confirm parameter separability with one revision: $k$ is the primary lever for tolerant-zone width; $\tau_0$ for N-crossing timing; $\tau_m$ for plateau ceiling; but $\tau_0$ also shows substantial secondary leverage on the plateau ceiling. N = 30, $V_0$ = £20m, $g$ = 10.4%.

---

## Figure 24

**Current name:** RATES.S-6
**Section:** §7.2
**Suggested new name:** Figure §7.2
**Appendix ref:** —
**Filename:** `sweeps_r_fig_s7_2_relative_sensitivity.png`

**Caption:**
Relative parameter sensitivity — normalised parameter value (0–1) vs key fiscal metrics. Each line represents one parameter swept from its minimum to maximum tested value, with the x-axis normalised so 0 = minimum and 1 = maximum, making all four parameters directly comparable on a single chart. The baseline position is marked by a vertical dotted line at the same normalised position for each. Left panel (TCM coverage ratio, median): $\tau_0$ (blue) shows the steepest positive slope — the strongest fiscal lever among the four parameters. $\tau_m$ (orange) is flat throughout, confirming fiscal inertness. $k$ (green) rises modestly. $W_{min}$ (purple) shows the largest absolute swing, rising steeply from its low end to high end. Right panel (LRR fill year, median): $\tau_0$ (blue) falls steeply across its normalised range. $W_{min}$ (purple) rises — the largest upward movement of any parameter. $\tau_m$ (orange) is flat throughout. $k$ (green) falls slightly. Together the two panels confirm the fiscal hierarchy established in (SWEEPS §7.1): $\tau_0$ dominates both coverage and fill timing; $W_{min}$ is second on fill timing but inverse on coverage; $k$ matters conditionally at the upper end; $\tau_m$ is inert on both dimensions.

---

## Figure 25

**Current name:** RATES.S-7
**Section:** §8.3
**Suggested new name:** Figure §8.3a
**Appendix ref:** —
**Filename:** `sweeps_r_fig_s8_3a_srr_ratio_sensitivity.png`

**Caption:**
SWF sizing sensitivity — srr_ratio (SRR capitalisation ratio). Four-panel RATES.S output across srr_ratio from 1× to 10×; canonical srr_ratio marked by the red dotted vertical. Individual taxpayer burden is invariant across this sweep — the bottom-right panel is omitted and replaced by a dual-axis SRR/LRR fill year chart. Top left: SSM and TCM coverage ratios both rise as srr_ratio increases — higher srr_ratio diverts more early revenue into SRR accumulation, which extends the capitalisation window and raises the within-window coverage ratio. Top right: median LRR fill year rises monotonically across the 1×–10× sweep, with each unit increase adding roughly one year to fill timing. Bottom left: LRR surplus at fill is broadly stable with high variance; the surplus is not a simple function of srr_ratio because fill timing shifts the position of the capitalisation window within the return sequence. Bottom right: dual-axis chart showing SRR fill year (blue, left axis) and LRR fill year (green, right axis) against srr_ratio; the gap between the two lines is the capitalisation window — the period during which the refund guarantee is mechanically credible but Phase Two has not yet become viable. Both lines rise as srr_ratio increases; the gap widens as srr_ratio increases — the SRR fill year rises faster proportionally than the LRR fill year — meaning that a higher srr_ratio lengthens the credibility-only period before Phase Two becomes viable.

---

## Figure 26

**Current name:** RATES.S-8
**Section:** §8.3
**Suggested new name:** Figure §8.3b
**Appendix ref:** —
**Filename:** `sweeps_r_fig_s8_3b_lrr_years_sensitivity.png`

**Caption:**
SWF sizing sensitivity — lrr_years (LRR floor, years of expenditure). Four-panel RATES.S output across lrr_years from 0.5 to 8 years; canonical lrr_years marked by the red dotted vertical. Individual taxpayer burden is invariant across this sweep. Top left: SSM and TCM coverage ratios rise as lrr_years increases — a higher floor target means the capitalisation window opens later in the budget growth trajectory, shifting the denominator and raising coverage ratios. Top right: median LRR fill year scales directly with lrr_years, with a roughly linear relationship across the sweep; the shaded band widens at high lrr_years, reflecting greater start-year sensitivity when the fill target is distant. Bottom left: LRR surplus at fill rises steeply at high lrr_years values — reflecting the compounding of returns over extended capitalisation windows. Bottom right: dual-axis SRR/LRR fill year chart; the SRR fill year (blue) is flat across the full lrr_years sweep — confirming that the two reserves capitalise on independent timescales and lrr_years does not affect refund-guarantee credibility. The gap between the flat SRR line and the rising LRR line is the capitalisation window, which widens monotonically as lrr_years increases.

---

## Figure 27

**Current name:** S3.2b
**Section:** §11
**Suggested new name:** Figure §11a
**Appendix ref:** —
**Filename:** `sweeps_v_fig_s11a_v0_entry_rate.png`

**Caption:**
Entry rate $\tau(V_0)$ at four wealth levels annotated on the canonical rate curve. The rate curve at canonical parameters is shown on a log wealth axis; coloured markers indicate where each reference taxpayer sits at entry. $V_0$ = £5m (blue) and $V_0$ = £20m (red) are both on the flat lower portion of the logistic, barely above $\tau_0$. $V_0$ = £100m (purple) has begun to climb the curve's slope. $V_0$ = £500m (green) sits meaningfully above $\tau_0$ and is approaching the curve's steepest region. The spread in entry rates understates the difference in mechanism exposure: the gap widens further as wealth grows over the holding period, since the £500m taxpayer ascends the logistic while the £20m taxpayer remains near the floor. $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, $W_{min}$ = £2m.

---

## Figure 28

**Current name:** S3.2a
**Section:** §11
**Suggested new name:** Figure §11b
**Appendix ref:** —
**Filename:** `sweeps_v_fig_s11b_v0_c1_curves.png`

**Caption:**
C.1 incentive structure by $V_0$ entry wealth — overlaid curves at canonical growth $g$ = 10.4%. The x-axis is declaration ratio $\alpha$; the y-axis is C.1 in percentage points. Positive values (left of $\alpha$ = 1.0) indicate understaters pay more than honest; negative values (right of $\alpha$ = 1.0) indicate overstaters pay less. The four lines cross at $\alpha$ = 1.0 by construction. $V_0$ = £5m (blue dotted) and $V_0$ = £20m (red solid, canonical) cluster near zero across the full $\alpha$ range — understater penalties are modest and the overstater advantage is small, reflecting that both taxpayers sit on the near-flat portion of the rate curve. $V_0$ = £100m (purple dashed) shows substantially larger penalties in both directions. $V_0$ = £500m (green dash-dot) shows the sharpest structure: material understater penalties at extreme understatement and positive overstater C.1 values at aggressive overstatement — the self-limiting correction is active and the overstater pays more than honest at this horizon. The intensification with wealth is the primary limitation of the canonical $V_0$ = £20m reference: mechanism properties are qualitatively correct but quantitatively compressed relative to the population of taxpayers where WDT revenue actually concentrates. $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, N = 30.

---

## Figure 29

**Current name:** S3.2c
**Section:** §11
**Suggested new name:** Figure §11c
**Appendix ref:** —
**Filename:** `sweeps_v_fig_s11c_v0_heatmaps.png`

**Caption:**
C.1 advantage landscape across $V_0$ entry wealth levels — four-panel heatmap. Each cell reports $(Net(\alpha) - Net(1) / TW(\alpha)$ in percentage points. The canonical panel ($V_0$ = £20m, bold border) is reproduced from (VAL.A §C.1). The $V_0$ = £5m panel is noticeably flatter: at strongly negative growth rates, $V_0$ falls below $W_{min}$ early in the holding period and the taxpayer exits scope, producing zero entries in the leftmost column. At $V_0$ = £100m the landscape sharpens substantially — understater penalties at extreme understatement and high growth, and positive overstater C.1 values in the mid-growth range, are both materially larger than the canonical panel. At $V_0$ = £500m the structure intensifies further across both the understater and overstater cells. The four-panel comparison makes the population-level extrapolation limitation concrete: the canonical reference understates mechanism intensity for the wealthier taxpayers who generate most WDT revenue. $\tau_0$ = 15%, $\tau_m$ = 70%, $k$ = 0.001, N = 30; $\alpha$ = 1.0 row is zero by construction.
