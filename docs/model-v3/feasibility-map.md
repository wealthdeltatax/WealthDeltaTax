# OF1 and CK1 at 10 death phases (brief 089c)

Status: run on `main` after 139c and 150c (10 death phases is the runner's default, ruled in 149c). Diagnostic output shaped for the Samples file; no schedule is renamed or re-chosen, no rule is picked, and no relaxed rule is offered as the strict result. Every number is a scenario value at a labelled grid point and fund setting (five points, none central; `safe` = net financial class return stand-in, `market` = the path's market return, 138c), never a forecast. 200 paths of the 128c market returns, seed 20261118; the sampling error of a share near 75% is 3.1 points.

## Reproduce

From the repository root, `python -I docs/model-v3/of1-ck1/of1_ck1.py` (about 25 minutes with `--workers 2`; `--points`, `--funds`, `--n`, `--out` select a part). It writes `of1_grid.csv` (fund, point, schedule-grid point, w_min, tolerance, margin, horizon, F1, M2, M4a), `of1_summary.csv` (per rule: best F1 anywhere and inside the M2 cap and M4a floor, feasible points or the marker `none_passes_75`, the named schedules `choose` finds under that rule), `ck1.csv` and `failed.csv`. The cells are produced by the model's functions: `sweeps.feasibility` (per-path shortfalls from `out_sweeps.per_path`), `out_sweeps.of1` and `ck1` (Samples form), `sweeps.map_summary`, `sweeps.stress`. The driver evaluates with `runner.core_run`, `headlines` and `out_sweeps.per_path` only (not the other output groups); a check on one point gave per-path arrays identical to the full `runner.evaluate`. The strict rule (tolerance 0, margin 0) equals the old F1, M2 and M4a (`tests/model_v3/test_of1.py`); `phase10_median_mid/` holds the earlier block 1 run, whose `median_mid` best F1 at tol 0, m 0 (21.5 and 31.5%) equals the numbers here. A second full run printed byte-identical CSVs (checked with `cmp`).

## The rule axes

Tolerance: the largest total shortfall P3 (summed over years 1 to the end of the window, percent of GDP; 0 is the strict closure) a path may have and still count as closed: 0, 0.05, 0.25, 1 (083c's). Margin: a tax is retired when relief divided by (1 + margin) covers its receipts, 0, 10, 25%; the shortfall is measured against the true relief. Both are labelled scenario constants (`out_sweeps.TOLS`, `MARGINS`), not register rows. Feasible: F1 at least 75%, M2 short at most 2.0 and M4a short at least 0.

## Strict rule first

At the strict rule (tolerance 0, margin 0) no schedule point is feasible at any of the five scenario points at either fund: best F1 15.5 to 36.5% at `safe` and 31.5 to 45.5% at `market`, against 75% required; every strict cell carries `none_passes_75`. Everything below is a relaxation, labelled with its rule.

## OF1: best F1 at the short window (percent of paths; * marks a rule with at least one feasible point)


**Fund `safe`**

| tolerance | margin | min_mid | median_mid | max_mid | median_low | median_high |
|---|---|---|---|---|---|---|
| tol_0 | m0 | 26.5 | 21.5 | 36.5 | 15.5 | 30.5 |
| tol_0 | m10 | 39.5 | 36.5 | 37.5 | 29.0 | 41.5 |
| tol_0 | m25 | 60.0 | 55.5 | 47.5 | 44.5 | 63.0 |
| tol_0p05 | m0 | 28.5 | 23.0 | 38.0 | 19.0 | 30.5 |
| tol_0p05 | m10 | 42.5 | 38.5 | 39.0 | 31.0 | 43.0 |
| tol_0p05 | m25 | 63.5 | 57.0 | 49.0 | 46.0 | 64.5 |
| tol_0p25 | m0 | 33.0 | 29.5 | 39.5 | 23.0 | 33.0 |
| tol_0p25 | m10 | 47.5 | 46.5 | 41.0 | 35.5 | 49.5 |
| tol_0p25 | m25 | 68.5 | 65.5 | 56.5 | 50.5 | 70.0 |
| tol_1 | m0 | 47.5 | 43.5 | 43.5 | 33.5 | 47.5 |
| tol_1 | m10 | 62.0 | 61.0 | 50.5 | 46.0 | 61.0 |
| tol_1 | m25 | 81.0* | 78.5* | 69.5 | 62.0 | 80.0* |

**Fund `market`**

| tolerance | margin | min_mid | median_mid | max_mid | median_low | median_high |
|---|---|---|---|---|---|---|
| tol_0 | m0 | 37.0 | 31.5 | 45.5 | 45.5 | 32.0 |
| tol_0 | m10 | 54.0 | 51.5 | 47.0 | 62.0 | 43.5 |
| tol_0 | m25 | 72.0 | 69.5 | 64.5 | 73.5 | 65.5 |
| tol_0p05 | m0 | 40.0 | 33.0 | 47.5 | 47.5 | 32.5 |
| tol_0p05 | m10 | 56.5 | 53.0 | 49.0 | 64.5 | 45.5 |
| tol_0p05 | m25 | 73.5 | 70.0 | 65.0 | 76.0* | 67.0 |
| tol_0p25 | m0 | 44.5 | 40.5 | 50.0 | 54.5 | 35.0 |
| tol_0p25 | m10 | 61.0 | 61.5 | 52.0 | 70.5 | 50.0 |
| tol_0p25 | m25 | 79.0* | 77.5* | 69.5 | 81.5* | 72.5 |
| tol_1 | m0 | 57.0 | 50.0 | 55.5 | 64.5 | 46.0 |
| tol_1 | m10 | 75.0* | 70.0 | 59.5 | 79.5* | 60.5 |
| tol_1 | m25 | 87.5* | 85.0* | 78.0* | 88.0* | 80.0* |

## Feasible rules and where (F1 at least 75%, M2 and M4a inside)

| fund | point | tolerance | margin | best F1 inside | at | feasible points | named schedules under this rule (`choose`) |
|---|---|---|---|---|---|---|---|
| safe | min_mid | tol_1 | m25 | 81.0 | tm50_k05_r100 | 2 | S_low=tm50_k05_r100;S_central=tm50_k05_r100;S_high=tm70_k05_r100 |
| safe | median_mid | tol_1 | m25 | 78.5 | tm50_k05_r100 | 1 | S_low=tm50_k05_r100;S_central=tm50_k05_r100;S_high=tm50_k05_r100 |
| safe | median_high | tol_1 | m25 | 80.0 | tm50_k05_r100 | 3 | S_low=tm50_k05_r100;S_central=tm50_k05_r100;S_high=tm90_k05_r100 |
| market | min_mid | tol_0p25 | m25 | 79.0 | tm70_k05_r100 | 2 | S_low=tm50_k05_r100;S_central=tm70_k05_r100;S_high=tm70_k05_r100 |
| market | min_mid | tol_1 | m10 | 75.0 | tm50_k05_r100 | 1 | S_low=tm50_k05_r100;S_central=tm50_k05_r100;S_high=tm50_k05_r100 |
| market | min_mid | tol_1 | m25 | 87.5 | tm50_k05_r100 | 3 | S_low=tm50_k05_r100;S_central=tm50_k05_r100;S_high=tm90_k05_r100 |
| market | median_mid | tol_0p25 | m25 | 77.5 | tm50_k05_r100 | 1 | S_low=tm50_k05_r100;S_central=tm50_k05_r100;S_high=tm50_k05_r100 |
| market | median_mid | tol_1 | m25 | 85.0 | tm50_k05_r100 | 3 | S_low=tm50_k05_r100;S_central=tm50_k05_r100;S_high=tm90_k05_r100 |
| market | max_mid | tol_1 | m25 | 78.0 | tm50_k05_r100 | 1 | S_low=tm50_k05_r100;S_central=tm50_k05_r100;S_high=tm50_k05_r100 |
| market | median_low | tol_0p05 | m25 | 76.0 | tm90_k05_r100 | 1 | S_low=tm90_k05_r100;S_central=tm90_k05_r100;S_high=tm90_k05_r100 |
| market | median_low | tol_0p25 | m25 | 81.5 | tm50_k05_r100 | 3 | S_low=tm50_k05_r100;S_central=tm50_k05_r100;S_high=tm90_k05_r100 |
| market | median_low | tol_1 | m10 | 79.5 | tm50_k05_r100 | 1 | S_low=tm50_k05_r100;S_central=tm50_k05_r100;S_high=tm50_k05_r100 |
| market | median_low | tol_1 | m25 | 88.0 | tm50_k05_r100 | 5 | S_low=tm50_k05_r050;S_central=tm50_k05_r100;S_high=tm90_k05_r100 |
| market | median_high | tol_1 | m25 | 80.0 | tm50_k05_r100 | 2 | S_low=tm50_k05_r100;S_central=tm50_k05_r100;S_high=tm70_k05_r100 |

14 of 120 (fund, point, rule) cells have a feasible point; all others carry the marker `none_passes_75` in `of1_summary.csv`. At the strict rule (tolerance 0, margin 0) none does at either fund (best F1 15.5 to 36.5% at `safe`, 31.5 to 45.5% at `market`). At `safe`, a feasible point needs tolerance 1 with margin 25% (3 of 5 points); at `market` a margin 25% (or 10% at tolerance 1) and tolerance 0.05 to 1. Every feasible best point has w_min `r100` and k_ln 0.5, mostly tm50; I did not test why. The F1 is not monotone in the margin everywhere (149c's lumpy relief); it is monotone in the tolerance (a test).

Cells that raised the arm's I1 alarm and were left out (not worked around; `failed.csv`): safe max_mid tm90_k2_r050; safe median_high tm90_k2_r025; market max_mid tm50_k2_r025; market max_mid tm70_k2_r025; market median_high tm90_k2_r025. A map point is missing there, so that row's best F1 is over the points that ran.

## CK1: fixed path g(t) = 4.74 + A sin(2 pi t / 10), amplitudes 0, 1, 3, 5, 8, 12; P3 from year 1 to the end of the short window

The largest amplitude up to which P3 is zero on every smaller amplitude too (`none`: P3 is positive even at A 0), per fund, point and schedule (the 140c schedules; `ck1.csv` has P1, P3 over transition plus short, P3 over all 100 years and P7b per amplitude):

| fund | point | tm50_k1_r050 | tm70_k1_r050 | tm90_k1_r050 | tm70_k05_r050 |
|---|---|---|---|---|---|
| safe | min_mid | 3 | 5 | 5 | none |
| safe | median_mid | 5 | 5 | 5 | none |
| safe | max_mid | 3 | none | none | 5 |
| safe | median_low | none | none | none | none |
| safe | median_high | 3 | none | none | 8 |
| market | min_mid | 8 | 8 | 8 | 1 |
| market | median_mid | 8 | 5 | 5 | none |
| market | max_mid | 3 | 1 | 1 | 8 |
| market | median_low | 8 | 8 | 8 | 3 |
| market | median_high | 3 | 1 | 1 | 8 |

P3 at A 0 is zero in 29 of 40 rows and positive in the others (up to 28.34); a row's `none` is a finding, kept. P1 (fill year) is 5 to 8; P7b is 0.89 to 1.44.

## What this does not do, and where it needs the author

- It picks no tolerance, margin or schedule. Which rule (if any) is the feasibility rule is the author's ruling; the named schedules shown under a relaxed rule are `choose`'s output under that rule, labelled with it, not the strict result (none exists at the strict rule).
- The tolerance is a total shortfall in GDP-points over the window (as 083c); if the author wants a per-year or share-of-relief tolerance, the axis changes.
- CK1's schedules are 140c's four stand-ins; the manifest's CK1 has no schedule axis, so the file's schedule key is None until the author names the schedule the check runs on.
- The marker `none_passes_75` is accepted by the validator for OF1 (and `not_run_this_point` for OF1 and CK1); `of1_summary.csv` carries it, the OF1 cells themselves are numeric. How 057c's run places the summary in the file is for 057c.
- Not run: 1,000 paths, level 2, schedule points beyond the 27.
