# I1 gap: one v2 input at a time (brief 074c)

Measured on branch `brief/052c-rework` (the 052c build, `revenue.py` and the pack unchanged). v2 was not run or imported; every v2 value comes from `model_v2/WDT_Params.toml` or `jst_r6.json`. Scripts are throwaway (scratchpad, not committed).

**Measure.** The I1 test environment: post-fill 10-year individual WDT take, % of GDP, median over the 117 UK loop windows, `logistic_ln_ref` (k_ln 1, tau0 4%, tau_m 90%), all Route C, v2 rule set (`c_cap` units_and_value, `verify_down` reset), no verification hazard, c 3.5%, levy fund 2.82% of GDP, ratio-mirror refund, v2's tail constants. Baseline 5.016 against v2's recorded 7.34: gap **2.324**.

## The table

Each row changes one thing from the baseline (v3 14 lines, v2 tail constants) toward v2.

| # | Candidate | v2 value / v3 value | I1 | Change from 5.016 |
|---|---|---|---|---|
| 1 | Body split and finer cells | v2: 41 cells (body split 5 from 0.5, 90-99% in 5 cells, top 1% in 8, RL in 3); v3: 14 lines. Cells put at v3's total, adults and W_min | 5.234 | **+0.219** |
| 1a | of which body split alone | v3's D6 mean is 0.152, just above W_min 0.15, so no decile straddles it. Splitting the body: 5.239 (top cells only) against 5.234 (all cells) | | -0.005 |
| 1b | of which the finer top (90-99%, top 1%, RL) | | 5.239 | +0.223 |
| 2a | Wealth over GDP | v2 7.21 (total 15,120bn, GDP 2,097bn, 2017); v3 6.44 (14,246bn over 2,211bn). GDP scaled, wealth unchanged | 5.680 | **+0.664** |
| 2c | v2's whole distribution (41 cells, total, 51.0m adults, v2 GDP), v3 W_min | | 6.002 | **+0.986** |
| 3 | W_min | v2 0.1125 (0.5 x 0.225 `house_median_gbp_m`); v3 0.150 (0.5 x 0.300 pack). 14 lines | 5.769 | **+0.753** |
| 3b | W_min on v2's distribution and GDP | | 6.862 | +0.860 over 2c |
| 4 | Returns | v2 JST `capital_tr` real: 117 usable years 1896 to 2019, mean 4.742%; pack `returns.csv`: the same 117, max difference 3e-5 points | | **0.000** |
| 5a | GDP-per-head growth for the threshold index | v2 `gpc_real` (nominal GDP per head, CPI-deflated, mean 1.65%); v3 pack real GDP per head (mean 1.47%) | 4.939 | -0.077 |
| 5b | Threshold not indexed (sensitivity, v2 uses `gdp_pc`) | | 5.630 | +0.614 |
| 5c | Levy fund removed (sensitivity) | v2 calibrates a levy to 2.77% of GDP, v3 uses 2.82 | 4.884 | -0.131 |
| 5d | Levy 2.77 against 2.82 | | 5.016 | 0.000 |
| 5e | G, death phases, fund | v2 and v3 the same: G 30, n_phase 6, a_window 5, horizon 10, safe_share 0, lambda_C 0, death_verifies false | | 0.000 |
| 5f | Sensitivities, not v2 differences | G 25: 6.218 (+1.202); n_phase 12: 5.161 (+0.145); c 2.5%: 6.945 (+1.929) | | |
| 6a | Take: gross of refunds against net | the test measures net (tax + death + heirs - refunds); gross 6.893 | 6.893 | +1.877 |
| 6b | Take: mean against median over windows | mean 6.023 (p25 3.707, p75 8.408) | 6.023 | +1.007 |
| 6c | eps | realised 12.1% against v2's implied 24.5% (`tornado.md` 4, gross g there, g net of consumption here: not like for like) | | not a swap |

Rows 6a and 6b change what is read, not an input. v2's definition of the recorded 7.34 is not in the toml or `tornado.md`, so I could not tell which of the two it uses; 6a would overshoot once rows 1 to 3 are in (9.03 gross on the combined base), so net looks the better reading.

## Combined

| Swap set | I1 | Change from 5.016 | Share of the 2.324 gap |
|---|---|---|---|
| A: rows 1, 2 and 3 together (v2's 41 cells, total, adults, GDP, W_min) | 6.862 | +1.846 | 79% |
| B: A plus v2's GDP-per-head growth (row 5a) | **6.659** | +1.643 | 71% |
| B without the levy fund | 6.517 | +1.501 | |
| B with the model refund (the I2 rule) | 6.607 | +1.591 | |

On B the realised eps is 13.4% (baseline 12.1%), omega over GDP 5.58 (5.10), fund fill year median 7, no unfilled window.

**Remainder: 0.681 points (29% of the gap)** at 7.34 against 6.659. I2 on B is 6.607, inside 6.34 to 7.36, so I2 would pass on v2's inputs while I1 still misses by 0.66 against a 0.02 limit.

## Not recovered

- **The last 0.68.** Candidates left, none testable without running v2: v2's fund and fill-year rule (`run_fund`; v3 rewrote it, fill median 7 here), the exact refund rule of v2's `assess` (the ratio mirror is the test's stand-in; it differs from the model's own by 0.05 here), the median taken over the windows v2 keeps, and rounding in the recorded 7.34.
- **The 41-cell grid is my rewrite from the spec** (`_body_cells`, `_build_advani`, `_fit_tail`, tiers, PAV repair; total 15,120bn, 7.21 of GDP, no PAV repairs, no failed fit). It was not checked against a v2 printout of its cells. The v2 distribution table is the one thing that would confirm it.
- v2's per-window output (fill year, take gross and net, eps) is not in the repo as data I could read; one such array would settle the remainder.

## Recommended fix (author's decision)

My 052c proposal, a base brief that splits D10a and D10b finer, is withdrawn: all finer cells together move I1 by 0.22. The gap is in input values, not line count.

1. **Put v2's inputs into the I1 and I2 tests as constants** (not into the model or the register): W_min 0.1125, GDP 2,097bn, 51.0m adults, v2's cell table (41 rows: share and wealth), JST `gpc_real`. This is a test-file change (size estimated, not built) and reaches I1 6.66 and I2 6.61. I2 then passes.
2. **I1 stays open by 0.68** until one of: (a) the author supplies v2's per-window outputs or runs v2 once and gives the cell table and the median, or (b) I1 is restated to a band (I2's) on v3's own pack values: W_min and omega from the pack (the two prices may differ in data year; not checked).
3. The two input differences worth a decision for the papers, since they are 1.6 of the 2.3 points: **W_min** (0.1125 against 0.150: v2's toml gives 0.225m, the pack 0.300m per adult; the years and bases behind the two were not checked; at the same 0.5 ratio this alone moves the take 0.75 to 0.86) and **wealth over GDP** (7.21 against 6.44).
