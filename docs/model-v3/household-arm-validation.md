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

## Suggestions (not applied)

None of these changes a parameter here: a held-moments table for the model could carry a `pack basis` column so definitional gaps are visible at source; the saving axis could be compared with a total-ratio series, not the non-pension part, if a validation of the saving level is wanted.

## Limits and Next

- Only untaxed runs are compared; the taxed account at the same three saving values is not compared (no held moment concerns a taxed outcome).
- Next: block of wealth-by-stage and a top-tail row in the pack (a research brief); a table of the model's class shares by band against `ons_was_wealth_by_age_of_hrp.csv` for BF-12 and BF-14.
