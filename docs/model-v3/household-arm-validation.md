# The household arm against the held 099r moments (brief 125c)

Status: first comparison. A comparison, not a calibration: no parameter, register row, label or file of the model was changed. The model side is the **untaxed** cell baseline (`model_v3/core/cells.py`, convention A, 100 years) at the three saving values (min, median, max of the ONS non-pension ratio) and the mid regime; every model number is a scenario value, not a forecast, and none is called central. The author reads this and decides what is next.

## What the held data allow

Of the 33 moments in `moments.csv` (`household-arm-validation/moments_map.csv` has one row each), 5 are held as data, 4 partly, 24 not. Ten are validation moments of 096r. **Only one validation moment is also held (BF-14, partly, and only qualitatively).** The transition matrix, the share with falling wealth, and the passive and active shares (BF-01 to BF-07, AB-01, AB-02) all need linked WAS microdata or a source not held, so they are `not held`; `moments_map.csv` states what each would need. The comparison below therefore uses the moments that are held and have a model analogue, and says plainly that these are mostly consistency checks, not tests.

| Status | Count | Moments |
|---|---:|---|
| computable | 5 | BF-11, BF-13, BF-14, BF-15, GB-01 |
| definition differs, no analogue | 3 | BF-12 (per-adult deciles), EER-01 (top 1%), TZ-01 (above 50m) |
| not held | 25 | the rest; AB-04 is here because its observed 1.4tn to 2.3tn is the paper's, and only 2020-22 financial wealth is held |

## Comparison (`comparison.csv`)

Gap: 0 inside the model range, else observed minus the nearest end.

| Moment | Observed | Model min to max (saving axis) | Gap | Label |
|---|---:|---:|---:|---|
| BF-11 wealth over GDP, year 0 | 7.5 | 6.14 (no axis: year 0 is the pack) | +1.36 | definition differs |
| BF-13 top-band wealth share, year 0 (top 10% about half) | 0.50 | 0.407 | +0.09 | definition differs |
| BF-13 top-band share, year 100 untaxed | 0.50 | 0.201 to 0.341 | +0.16 | definition differs |
| BF-14 retired cells' share of wealth, year 0 (age 60 and over held 49%) | 0.49 | 0.301 | +0.19 | definition differs |
| GB-01 total saving ratio, year 1, against 2019 / 2022 / 2024 / 2025 | 5.7 / 5.0 / 9.5 / 9.6% | 2.2 to 18.4% | 0 | inside |
| BF-15 total saving ratio, year 1, against 2020 | 16.5% | 2.2 to 18.4% | 0 | inside |

## Which axes drive each gap, and which gaps are definitional

- **BF-11 (wealth over GDP).** Year 0 is the pack total (13,568bn, the WAS Table 2.1 basis), so it matches by construction and the saving axis does not enter. The gap to 7.5 is the pension valuation: Resolution Foundation values pensions at market annuity rates (17tn), the pack at ONS SCAPE. Definitional; nothing in the model run explains it.
- **BF-13 (top-band share).** Year 0 is again the pack (D10 holds 0.407 of household wealth) against "about half" for the top 10% of per-adult families on a different valuation: a definitional gap. The year-100 untaxed share falls to 0.20 to 0.34 across the saving axis because saving is a uniform ratio of income, not a gradient in wealth, and cells do not mix; that is a **scenario consequence of the known gaps (no saving gradient, no transitions)**, not evidence on the observed share. The top-1% share (18% to 23%, EER-01 14.4 to 16.5%) is not computable: the pack has no split inside D10.
- **BF-14 (retired share).** The model splits band wealth between stages by person share, so its 0.30 is the retired person share, not a wealth measure; the observed 49% is people aged 60 and over, an age proxy for stage (retired is not identified). Definitional on both sides; the number cannot test the model until wealth by stage exists.
- **GB-01 and BF-15 (saving ratio).** The axis is built from the same ONS series as the observed ratio (the non-pension part, 1998 to 2025), with the pension accrual added, so the observed values lying `inside` the 2.2 to 18.4% range is by construction and says nothing about the model. The comparison does show the axis is wide: the observed total ratio moved between 5.0% and 16.5% over 2019 to 2022. The report's own 4.0% (2022) and 10.8% (Q2 2025) do not match the held annual values (vintage, quarter), and the RF 25% quarterly peak is not held.

## What better data would resolve

- A top-1% (or Pareto tail) row in the pack would let EER-01, TZ-01 and the top-share part of BF-13 be compared.
- Wealth by stage, and by age, would turn BF-14 from a person-share check into a wealth check.
- Linked WAS microdata (UKDS, out of scope here) are the only source for the transition matrix, the share with falling wealth and the passive share by band, which are the moments that bear on a saving-by-wealth gradient and per-path regimes.
- The pension valuation basis of the pack against Resolution Foundation (BF-11) is a research question, not a model one.

## Concentration under the stock and saving switches (147c)

Two labelled scenario switches (147c, `switches.py`): `top_tail` scales D10b's opening stock to a published top-1% share (14.4% `ast_low`, 16.5% `ast_high`; the `_e0` settings first take the missing wealth I-D4e off the top) and `saving_shape` gives the saving ratio by line a step (`mild`, 7 points: D1 and D2 save less) or a step plus a rise (`steep`, 7 more points up the percentiles). Each is a scenario with no fitted value; nothing here is calibrated, and no headline number is read. Shares are of the arm's own household wealth, pension included, untaxed (the `none` run through the arm's step), of the arm's opening stock after the launch loss, so year 0 is 0.430 for the top decile and 0.216 for the top 1% with both switches off. The top-decile share is unchanged by `top_tail` (D10a takes what D10b gives); `_e0` lowers it to 0.402. 20 paths, the five grid points (`scenario_grid.py`, `scenario_grid.csv`).

**Against 0.50 (BF-13, top 10%), range over saving min, median, max at the mid regime.** The observed 0.50 is on a different definition (per-adult families), so the label stays `definition differs`; the gap is shown, not claimed. Year 0 is the stock: top-1% rows at year 0 equal the setting by construction, not a test.

| top-1% setting | saving shape | top 10%, year 0 | top 10%, year 100 | gap to 0.50, year 100 | top 1%, year 0 | top 1%, year 100 |
|---|---|---|---|---|---|---|
| off | flat | 0.430 | 0.207 to 0.339 | +0.161 | 0.216 | 0.069 to 0.166 |
| off | mild | 0.430 | 0.212 to 0.351 | +0.149 | 0.216 | 0.069 to 0.166 |
| off | steep | 0.430 | 0.230 to 0.388 | +0.112 | 0.216 | 0.071 to 0.167 |
| ast_low | flat | 0.430 | 0.207 to 0.338 | +0.162 | 0.144 | 0.048 to 0.110 |
| ast_low | mild | 0.430 | 0.212 to 0.351 | +0.149 | 0.144 | 0.049 to 0.111 |
| ast_low | steep | 0.430 | 0.230 to 0.388 | +0.112 | 0.144 | 0.051 to 0.113 |
| ast_high | flat | 0.430 | 0.207 to 0.338 | +0.162 | 0.165 | 0.054 to 0.126 |
| ast_high | mild | 0.430 | 0.212 to 0.351 | +0.149 | 0.165 | 0.055 to 0.127 |
| ast_high | steep | 0.430 | 0.230 to 0.388 | +0.112 | 0.165 | 0.057 to 0.129 |
| ast_low_e0 | flat | 0.402 | 0.196 to 0.314 | +0.186 | 0.144 | 0.047 to 0.109 |
| ast_low_e0 | mild | 0.402 | 0.202 to 0.326 | +0.174 | 0.144 | 0.048 to 0.110 |
| ast_low_e0 | steep | 0.402 | 0.220 to 0.366 | +0.134 | 0.144 | 0.050 to 0.112 |
| ast_high_e0 | flat | 0.402 | 0.196 to 0.314 | +0.186 | 0.165 | 0.053 to 0.125 |
| ast_high_e0 | mild | 0.402 | 0.202 to 0.326 | +0.174 | 0.165 | 0.053 to 0.126 |
| ast_high_e0 | steep | 0.402 | 0.220 to 0.366 | +0.134 | 0.165 | 0.055 to 0.128 |

Reading: with both switches off the year-100 untaxed top-decile share is 0.207 to 0.339 (gap +0.161). `mild` raises it to 0.212 to 0.351 and `steep` to 0.230 to 0.388 (gap +0.112), still short of 0.50 at the range's top; `top_tail` moves the top-1% share (year 100: 0.048 to 0.129 against 0.069 to 0.166 off) and moves the top-decile share not at all, the `_e0` settings aside (0.196 to 0.314 flat). Saving by wealth closes 0.05 of the 0.16 gap at the top end of the range; no setting reaches 0.50.

**By year, at `median_mid`.**

| top-1% setting | saving shape | top 10%: yr 1 | 10 | 30 | 100 | top 1%: yr 1 | 10 | 30 | 100 |
|---|---|---|---|---|---|---|---|---|---|
| off | flat | 0.427 | 0.406 | 0.367 | 0.291 | 0.215 | 0.201 | 0.176 | 0.128 |
| off | mild | 0.427 | 0.407 | 0.370 | 0.296 | 0.215 | 0.201 | 0.176 | 0.126 |
| off | steep | 0.428 | 0.414 | 0.386 | 0.327 | 0.215 | 0.201 | 0.177 | 0.129 |
| ast_low | flat | 0.427 | 0.406 | 0.367 | 0.291 | 0.143 | 0.134 | 0.117 | 0.086 |
| ast_low | mild | 0.427 | 0.407 | 0.370 | 0.296 | 0.143 | 0.134 | 0.118 | 0.085 |
| ast_low | steep | 0.428 | 0.414 | 0.386 | 0.327 | 0.143 | 0.135 | 0.119 | 0.088 |
| ast_high | flat | 0.427 | 0.406 | 0.367 | 0.291 | 0.164 | 0.153 | 0.134 | 0.098 |
| ast_high | mild | 0.427 | 0.407 | 0.370 | 0.296 | 0.164 | 0.153 | 0.134 | 0.097 |
| ast_high | steep | 0.428 | 0.414 | 0.386 | 0.327 | 0.164 | 0.154 | 0.136 | 0.100 |
| ast_low_e0 | flat | 0.399 | 0.379 | 0.342 | 0.271 | 0.143 | 0.133 | 0.116 | 0.084 |
| ast_low_e0 | mild | 0.399 | 0.380 | 0.346 | 0.276 | 0.143 | 0.133 | 0.117 | 0.084 |
| ast_low_e0 | steep | 0.400 | 0.387 | 0.362 | 0.309 | 0.143 | 0.134 | 0.118 | 0.087 |
| ast_high_e0 | flat | 0.399 | 0.379 | 0.342 | 0.271 | 0.164 | 0.153 | 0.133 | 0.096 |
| ast_high_e0 | mild | 0.399 | 0.380 | 0.346 | 0.276 | 0.164 | 0.153 | 0.133 | 0.095 |
| ast_high_e0 | steep | 0.400 | 0.387 | 0.362 | 0.309 | 0.164 | 0.153 | 0.135 | 0.098 |

**What the run reports** (20 paths, schedule S; ranges over the cells that ran at the five points; M2 is the long horizon):

| top-1% setting | saving shape | cells run of 5 | M1a long | M2 long, overall | M2 long, D10 | shortfall line-phases (max) | largest lien balance | I1 and ties |
|---|---|---|---|---|---|---|---|---|
| off | flat | 5 | 0.94 to 7.95 | 0.11 to 0.40 | 0.16 to 0.53 | 160 | 0.6 | held; tie max 5e-12 |
| off | mild | 3 | 2.11 to 9.18 | 0.16 to 0.43 | 0.20 to 0.53 | 0 | 0.3 | held; tie max 6e-12 |
| off | steep | 1 | 7.47 to 7.47 | 0.27 to 0.27 | 0.33 to 0.33 | 0 | 0.0 | held; tie max 8e-12 |
| ast_low | flat | 5 | 0.95 to 8.37 | 0.10 to 0.41 | 0.14 to 0.53 | 160 | 0.6 | held; tie max 5e-12 |
| ast_low | mild | 3 | 2.14 to 9.55 | 0.16 to 0.44 | 0.20 to 0.54 | 0 | 0.2 | held; tie max 6e-12 |
| ast_low | steep | 1 | 7.54 to 7.54 | 0.27 to 0.27 | 0.33 to 0.33 | 0 | 0.0 | held; tie max 7e-12 |
| ast_high | flat | 5 | 0.95 to 8.29 | 0.10 to 0.41 | 0.14 to 0.53 | 160 | 0.6 | held; tie max 4e-12 |
| ast_high | mild | 3 | 2.14 to 9.48 | 0.16 to 0.44 | 0.20 to 0.54 | 0 | 0.2 | held; tie max 4e-12 |
| ast_high | steep | 1 | 7.52 to 7.52 | 0.27 to 0.27 | 0.33 to 0.33 | 0 | 0.0 | held; tie max 9e-12 |
| ast_low_e0 | flat | 5 | 0.86 to 7.94 | 0.10 to 0.40 | 0.13 to 0.51 | 160 | 0.6 | held; tie max 4e-12 |
| ast_low_e0 | mild | 3 | 2.03 to 9.16 | 0.15 to 0.43 | 0.19 to 0.52 | 0 | 0.2 | held; tie max 6e-12 |
| ast_low_e0 | steep | 1 | 7.40 to 7.40 | 0.27 to 0.27 | 0.32 to 0.32 | 0 | 0.0 | held; tie max 8e-12 |
| ast_high_e0 | flat | 5 | 0.86 to 7.83 | 0.10 to 0.40 | 0.14 to 0.51 | 160 | 0.6 | held; tie max 4e-12 |
| ast_high_e0 | mild | 3 | 2.02 to 9.06 | 0.15 to 0.43 | 0.19 to 0.52 | 0 | 0.2 | held; tie max 4e-12 |
| ast_high_e0 | steep | 1 | 7.39 to 7.39 | 0.27 to 0.27 | 0.32 to 0.32 | 0 | 0.0 | held; tie max 7e-12 |

**Thirty of the 50 non-flat cells stop** in the M13 welfare output (`crra_ce`: CRRA utility needs positive terminal wealth), none in the flat cells: `mild` at `min_mid` and `median_low`, `steep` at all but `max_mid` (both, five `top_tail` settings each). D1 and D2 start near £3,000 a person and dissave 5 to 12 points of income, so they end negative. No rule was changed; the cells are reported as stops, and their concentration (which does not need M13) is in the tables above. Where the runs complete, I1, the account identity (max 5e-11) and the ledger ties (max 9e-12) hold at every one of the 45 cells and `unpaid` is 0. The 160 shortfall line-phases at `min_mid` are the 137c floor alarm (unchanged by either switch); `unpaid_B` there is 0.13, also unchanged.

## Suggestions (not applied)

None of these changes a parameter here: a held-moments table for the model could carry a `pack basis` column so definitional gaps are visible at source; the saving axis could be compared with a total-ratio series, not the non-pension part, if a validation of the saving level is wanted.

## Limits and Next

- Only untaxed runs are compared; the taxed account at the same three saving values is not compared (no held moment concerns a taxed outcome).
- Next: block of wealth-by-stage and a top-tail row in the pack (a research brief); a table of the model's class shares by band against `ons_was_wealth_by_age_of_hrp.csv` for BF-12 and BF-14.
