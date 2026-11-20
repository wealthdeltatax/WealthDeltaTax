# F1 closure diagnostic (brief 083c)

No (tol, m) cell in the brief's grid reaches the 75% closure share: the best is 50.6% (tol 1.0, m 25%), at tm50_k05_r100. Not every cell is under 25%, so the early-check condition (a different mechanism, not a different tolerance) is not triggered by the brief's own test. Only a retirement margin of 100% with tol 1.0, outside the grid, reaches 75% (79.3%); see "Which single change".

Reproduce: `python -I docs/model-v3/f1-diagnostic/f1_gap.py` from the repository root (about 1.5 minutes; seed 20261118). A second run prints identical text. Seed 20261118; 1000 level 1 paths of the AR(1) generator at central inputs (mean 4.74, SD 8.22, lag-1 0.3); the same paths for all 27 grid points; short window = the 10 years after the fill; margins (0.0, 0.1, 0.25) (and (0.5, 1.0) in the last table only); tolerances (0.0, 0.05, 0.25, 1.0) GDP-points.

### Summary: (tol, m) against best F1 and the feasible-point count

F1 is the percent of paths with short-window P3 at most `tol`. "Best F1 passing M2 and M4a" is the highest F1 among grid points with M2 short at most 2.0 and M4a short at least 0.0; "feasible points" also needs F1 at least 75.

| tol | m | best F1 (any point) | at | best F1 passing M2, M4a | at | feasible points of 27 |
|---|---|---|---|---|---|---|
| 0 | 0% | 11.5 | tm90_k2_r025 | 5.7 | tm50_k05_r025 | 0 |
| 0 | 10% | 11.9 | tm90_k2_r025 | 11.4 | tm50_k05_r100 | 0 |
| 0 | 25% | 24.6 | tm50_k05_r100 | 24.6 | tm50_k05_r100 | 0 |
| 0.05 | 0% | 11.5 | tm90_k2_r025 | 7.0 | tm50_k05_r100 | 0 |
| 0.05 | 10% | 13.1 | tm50_k05_r100 | 13.1 | tm50_k05_r100 | 0 |
| 0.05 | 25% | 26.3 | tm50_k05_r100 | 26.3 | tm50_k05_r100 | 0 |
| 0.25 | 0% | 12.4 | tm90_k2_r025 | 11.3 | tm50_k05_r100 | 0 |
| 0.25 | 10% | 17.8 | tm50_k05_r100 | 17.8 | tm50_k05_r100 | 0 |
| 0.25 | 25% | 32.4 | tm50_k05_r100 | 32.4 | tm50_k05_r100 | 0 |
| 1 | 0% | 27.6 | tm50_k05_r100 | 27.6 | tm50_k05_r100 | 0 |
| 1 | 10% | 37.0 | tm50_k05_r100 | 37.0 | tm50_k05_r100 | 0 |
| 1 | 25% | 50.6 | tm50_k05_r100 | 50.6 | tm50_k05_r100 | 0 |

## Reading

The failure is structural, not noise. On a constant path at the central return (item 4) the fund fills in year 6, five taxes (six at tau_m 0.9) are retired by year 100, each when relief just covers it, and then relief decays: the wealth tax receipts M1a fall from 11.3% of GDP in year 10 to 0.09% in year 100 (tau_m 0.5), the corporate levy M1b stays at 2.82, and relief ends at 2.85 to 2.86, almost all of it the levy, against retired receipts of 4.74 (five taxes) or 8.11 (six, at tau_m 0.9). Relief first falls below M1d in year 13 (tau_m 0.5 and 0.7) or year 11 (tau_m 0.9), inside the 10-year short window that ends in year 16, so a path with no volatility at all already fails the short-window test. Why M1a decays is not tested here; the inputs that move it on this path are the consumption share (I-D14c, 3.5%), the return (4.74%) and a threshold and GDP that grow with GDP per head (1.57%).

On the 1,000 random paths this shows as P3 that is large rather than marginal (item 1): the median short-window P3 is 3.4 to 11.6 GDP-points summed over years, the 90th percentile 15.6 to 29.7 and the maximum 45.7 to 55.3, and 69 to 87% of the failing paths first fall short within 3 years of a retirement. Between 5.0 and 6.0 of the 6 taxes are retired by the end of the window, and no path is unfilled, so F1 is not helped by unfilled paths. Because P3 is large, a tolerance only forgives dips that are small against it: tol 1.0 raises the best F1 from 11.5 to 27.6, and with the retirement rule as it is, tol 0.05 and 0.25 leave the best F1 at 11.5 and 12.4 (item 2). A margin acts on the cause, since it delays each retirement until relief exceeds the receipts by m, but it costs retired taxes and M4a and is still short of 75 at 25% (item 3).

## Which single change reaches 75%

Within the brief's grid (tol up to 1.0, m up to 25%): none. The highest F1 is 50.6% at tol 1.0 and m 25% (tm50_k05_r100, M4a short 10.8 against 14.1 at m 0, 4.51 taxes retired against 4.96); no point passes all three conditions in any of the 12 cells. A tolerance alone tops out at 27.6% (tol 1.0, m 0).

Beyond the grid (last table, run only to show where it would close): a margin of 100% with tol 1.0 gives F1 79.3% at tm50_k05_r100 and 76.4% at tm70_k05_r100, the only two feasible points; at the first M4a short is 5.6 (14.1 with no margin) and 3.61 taxes are retired on average (4.96). At tol 0 the same margin gives 66.8%, and a margin of 50% gives 43.7% (tol 0) and 62.9% (tol 1.0). No tolerance and margin combination other than that corner reaches 75%.

The report recommends nothing about the rule; the guru and the author rule.

## Notes on method

- `core` calls `runner.core_run` (brief 084c: the first half of `evaluate`, kept raw) at central inputs; `runner/` and `core/` are unedited. On grid points 1, 14 and 27 the script's short-window P3, M2, M4a and fill years equal `runner.headlines` (asserted). The first runs, before 084c landed, used a copy of that half and printed the same tables.
- The margin is applied as the brief says: `relief / (1 + m)` goes to `revenue.retire`, so a tax is retired when relief is at least (1 + m) times the receipts of that tax plus those already retired; the excess is measured against the true relief. At m 0 it reproduces `revenue.retire` exactly (asserted).
- F1 is the share of paths with short-window P3 at most `tol` (1e-9 for tol 0, as `sweeps.CLOSED`); P3 is summed from year 1 to the end of the short window, as `evaluate`'s `P3h['short']`.
- Item 1 at (tol 0, m 0) gives F1 4.3 to 11.5% over the 27 points; 055c reported 4.0 to 11.2%. The difference is the path sample: 055c's progress block does not record its stream, and three other draws of 1,000 paths give lows of 3.6 to 4.7% and highs of 11.3 to 13.4% (checked outside the script), which is the sampling error of a 1,000-path share (about 0.7 points at 5%, 1.0 at 11%).
- Taxes retired is the mean over filled paths of the taxes with a retirement year at or before the end of the short window. The pack has 6 retired taxes.
- Item 5 uses the schedules of item 4 and the tm70_k05_r050 schedule that 055c used for CK1, and both mu values (4.42, which 055c used, and 4.74, which metrics.md now names). Over transition plus short, P3 is positive at A 0 in all eight rows and zero at A 12 in six of eight; no row is zero up to a stated amplitude, so CK1 does not pass in either window.
- Level 1 at central inputs only, 1,000 paths; no level 2, no change to A5.

## Tables (script output)

### Item 1: size of the failure (tol 0, m 0)

| point | F1 % (P3<=1e-9) | P3 exactly 0 % | P3 P10 | median | P90 | max | failing paths, first shortfall within 3 y of a retirement % | taxes retired (mean, filled paths) | unfilled paths % | M2 short | M4a short |
|---|---|---|---|---|---|---|---|---|---|---|---|
| tm50_k05_r025 | 5.7 | 0.4 | 0.48 | 6.81 | 23.55 | 51.65 | 86.4 | 5.42 | 0.0 | 1.38 | 18.5 |
| tm50_k05_r050 | 5.2 | 0.2 | 0.38 | 5.49 | 18.70 | 50.30 | 87.0 | 5.20 | 0.0 | 1.36 | 16.4 |
| tm50_k05_r100 | 5.6 | 0.2 | 0.18 | 3.36 | 15.63 | 46.19 | 84.9 | 4.96 | 0.0 | 1.47 | 14.1 |
| tm50_k1_r025 | 5.0 | 0.1 | 0.88 | 8.98 | 28.77 | 52.66 | 82.9 | 5.75 | 0.0 | 2.04 | 22.2 |
| tm50_k1_r050 | 4.9 | 0.1 | 0.72 | 7.68 | 25.78 | 51.98 | 85.3 | 5.55 | 0.0 | 1.89 | 20.0 |
| tm50_k1_r100 | 5.6 | 0.0 | 0.29 | 5.34 | 20.21 | 50.63 | 86.3 | 5.24 | 0.0 | 1.89 | 16.9 |
| tm50_k2_r025 | 9.2 | 0.4 | 0.26 | 11.24 | 29.65 | 55.28 | 76.1 | 5.91 | 0.0 | 2.82 | 24.0 |
| tm50_k2_r050 | 6.3 | 0.2 | 0.61 | 9.06 | 28.98 | 52.34 | 81.1 | 5.78 | 0.0 | 2.51 | 22.5 |
| tm50_k2_r100 | 5.4 | 0.2 | 0.56 | 7.41 | 25.67 | 51.79 | 84.4 | 5.53 | 0.0 | 2.54 | 19.8 |
| tm70_k05_r025 | 4.8 | 0.1 | 0.78 | 7.36 | 24.93 | 51.67 | 87.1 | 5.51 | 0.0 | 1.77 | 19.5 |
| tm70_k05_r050 | 5.7 | 0.4 | 0.39 | 5.96 | 20.81 | 50.70 | 87.6 | 5.28 | 0.0 | 1.79 | 17.2 |
| tm70_k05_r100 | 5.2 | 0.2 | 0.25 | 4.23 | 16.62 | 45.75 | 85.2 | 5.04 | 0.0 | 1.97 | 14.9 |
| tm70_k1_r025 | 6.5 | 0.5 | 0.81 | 9.44 | 28.91 | 52.32 | 81.2 | 5.82 | 0.0 | 2.60 | 22.9 |
| tm70_k1_r050 | 4.9 | 0.2 | 0.96 | 8.15 | 26.63 | 49.95 | 84.0 | 5.65 | 0.0 | 2.44 | 21.0 |
| tm70_k1_r100 | 6.5 | 0.2 | 0.31 | 6.20 | 22.28 | 50.92 | 85.9 | 5.35 | 0.0 | 2.50 | 17.9 |
| tm70_k2_r025 | 10.3 | 0.9 | 0.00 | 11.39 | 28.79 | 52.72 | 70.7 | 5.96 | 0.0 | 3.69 | 24.6 |
| tm70_k2_r050 | 8.0 | 0.3 | 0.53 | 9.60 | 28.71 | 51.96 | 79.1 | 5.85 | 0.0 | 3.33 | 23.3 |
| tm70_k2_r100 | 4.8 | 0.0 | 0.99 | 8.07 | 25.98 | 48.64 | 84.2 | 5.67 | 0.0 | 3.44 | 21.3 |
| tm90_k05_r025 | 4.3 | 0.2 | 0.93 | 7.64 | 25.38 | 51.59 | 86.3 | 5.55 | 0.0 | 2.13 | 20.0 |
| tm90_k05_r050 | 5.5 | 0.3 | 0.44 | 6.50 | 22.74 | 50.63 | 86.9 | 5.35 | 0.0 | 2.19 | 17.9 |
| tm90_k05_r100 | 5.5 | 0.4 | 0.29 | 4.64 | 17.56 | 45.67 | 86.3 | 5.10 | 0.0 | 2.44 | 15.4 |
| tm90_k1_r025 | 7.1 | 0.4 | 0.74 | 10.00 | 29.34 | 52.00 | 79.8 | 5.86 | 0.0 | 3.12 | 23.4 |
| tm90_k1_r050 | 4.3 | 0.0 | 1.00 | 8.66 | 27.64 | 49.17 | 83.9 | 5.71 | 0.0 | 2.96 | 21.7 |
| tm90_k1_r100 | 5.8 | 0.4 | 0.42 | 6.53 | 23.69 | 50.88 | 87.0 | 5.44 | 0.0 | 3.08 | 18.8 |
| tm90_k2_r025 | 11.5 | 0.2 | 0.00 | 11.60 | 27.59 | 51.09 | 68.8 | 5.97 | 0.0 | 4.51 | 24.8 |
| tm90_k2_r050 | 8.8 | 0.5 | 0.36 | 10.34 | 27.92 | 51.36 | 76.6 | 5.89 | 0.0 | 4.14 | 23.8 |
| tm90_k2_r100 | 4.6 | 0.1 | 0.95 | 8.51 | 26.62 | 51.55 | 83.5 | 5.75 | 0.0 | 4.31 | 22.2 |

F1 over the 27 points at (tol 0, m 0): 4.3 to 11.5 percent (055c: 4.0 to 11.2).

### Item 2 and 3: F1 by tolerance and margin (percent of paths)

| point | tol 0, m 0% | tol 0.05, m 0% | tol 0.25, m 0% | tol 1, m 0% | tol 0, m 10% | tol 0.05, m 10% | tol 0.25, m 10% | tol 1, m 10% | tol 0, m 25% | tol 0.05, m 25% | tol 0.25, m 25% | tol 1, m 25% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| tm50_k05_r025 | 5.7 | 6.2 | 8.0 | 14.2 | 8.4 | 9.2 | 11.5 | 21.2 | 13.2 | 13.9 | 17.1 | 29.0 |
| tm50_k05_r050 | 5.2 | 5.5 | 8.7 | 19.7 | 8.3 | 8.6 | 12.9 | 27.2 | 17.8 | 18.3 | 22.5 | 36.8 |
| tm50_k05_r100 | 5.6 | 7.0 | 11.3 | 27.6 | 11.4 | 13.1 | 17.8 | 37.0 | 24.6 | 26.3 | 32.4 | 50.6 |
| tm50_k1_r025 | 5.0 | 5.2 | 6.2 | 10.7 | 6.5 | 6.9 | 7.9 | 13.5 | 9.8 | 10.3 | 11.8 | 18.8 |
| tm50_k1_r050 | 4.9 | 4.9 | 6.2 | 12.0 | 8.2 | 8.3 | 10.0 | 17.9 | 12.4 | 12.8 | 15.0 | 25.5 |
| tm50_k1_r100 | 5.6 | 6.1 | 8.9 | 21.6 | 8.9 | 9.6 | 13.1 | 27.9 | 17.4 | 18.4 | 21.7 | 37.7 |
| tm50_k2_r025 | 9.2 | 9.4 | 10.0 | 12.5 | 10.2 | 10.4 | 11.0 | 14.0 | 11.5 | 11.7 | 12.6 | 16.4 |
| tm50_k2_r050 | 6.3 | 6.6 | 7.9 | 12.1 | 7.2 | 7.6 | 9.3 | 14.1 | 10.5 | 10.9 | 13.1 | 20.1 |
| tm50_k2_r100 | 5.4 | 5.4 | 7.3 | 13.1 | 8.1 | 8.2 | 10.9 | 19.5 | 12.6 | 13.0 | 15.7 | 26.9 |
| tm70_k05_r025 | 4.8 | 5.0 | 6.5 | 12.2 | 8.2 | 8.7 | 10.9 | 18.5 | 12.2 | 12.9 | 15.0 | 25.9 |
| tm70_k05_r050 | 5.7 | 6.0 | 8.3 | 18.2 | 8.1 | 8.7 | 11.2 | 23.8 | 14.8 | 15.6 | 18.7 | 33.5 |
| tm70_k05_r100 | 5.2 | 6.0 | 9.9 | 25.5 | 10.4 | 11.4 | 16.4 | 32.7 | 22.2 | 23.3 | 28.6 | 46.1 |
| tm70_k1_r025 | 6.5 | 6.8 | 7.4 | 11.3 | 7.4 | 7.7 | 8.3 | 13.3 | 10.0 | 10.4 | 11.3 | 18.0 |
| tm70_k1_r050 | 4.9 | 5.1 | 5.8 | 10.4 | 6.8 | 7.3 | 8.4 | 14.3 | 11.0 | 11.7 | 13.4 | 22.5 |
| tm70_k1_r100 | 6.5 | 6.7 | 9.2 | 18.1 | 9.6 | 10.1 | 12.5 | 24.0 | 14.7 | 15.3 | 18.7 | 32.7 |
| tm70_k2_r025 | 10.3 | 10.4 | 11.0 | 14.5 | 10.5 | 10.6 | 11.3 | 15.1 | 11.1 | 11.2 | 11.9 | 16.5 |
| tm70_k2_r050 | 8.0 | 8.2 | 9.0 | 11.9 | 9.0 | 9.2 | 10.0 | 14.5 | 10.5 | 10.7 | 11.7 | 18.1 |
| tm70_k2_r100 | 4.8 | 5.0 | 5.7 | 10.2 | 6.6 | 7.3 | 8.5 | 15.2 | 10.5 | 11.4 | 14.0 | 23.1 |
| tm90_k05_r025 | 4.3 | 4.4 | 5.4 | 10.3 | 7.2 | 7.4 | 9.0 | 16.4 | 11.4 | 11.8 | 13.8 | 23.8 |
| tm90_k05_r050 | 5.5 | 5.8 | 7.8 | 16.8 | 8.2 | 8.7 | 10.9 | 23.2 | 13.3 | 14.1 | 17.1 | 31.7 |
| tm90_k05_r100 | 5.5 | 6.0 | 9.2 | 23.4 | 9.4 | 10.4 | 14.2 | 30.8 | 20.3 | 21.6 | 25.5 | 43.2 |
| tm90_k1_r025 | 7.1 | 7.6 | 8.5 | 11.1 | 7.9 | 8.4 | 9.2 | 13.3 | 9.5 | 9.9 | 11.0 | 16.7 |
| tm90_k1_r050 | 4.3 | 4.8 | 5.9 | 10.0 | 5.8 | 6.5 | 7.9 | 13.8 | 9.6 | 10.5 | 12.6 | 20.3 |
| tm90_k1_r100 | 5.8 | 6.0 | 8.3 | 15.5 | 8.7 | 9.0 | 11.3 | 22.7 | 12.9 | 13.6 | 16.5 | 30.2 |
| tm90_k2_r025 | 11.5 | 11.5 | 12.4 | 15.6 | 11.9 | 11.9 | 12.8 | 16.1 | 12.2 | 12.2 | 13.2 | 17.0 |
| tm90_k2_r050 | 8.8 | 9.2 | 9.6 | 12.1 | 9.7 | 10.1 | 10.5 | 13.7 | 11.3 | 11.7 | 12.1 | 16.5 |
| tm90_k2_r100 | 4.6 | 4.7 | 5.8 | 10.3 | 6.0 | 6.1 | 7.3 | 13.2 | 9.0 | 9.6 | 12.0 | 19.6 |

### Item 3: margin effect on M4a (short), taxes retired and F1 at tol 0

| point | F1 m 0% | M4a m 0% | taxes m 0% | F1 m 10% | M4a m 10% | taxes m 10% | F1 m 25% | M4a m 25% | taxes m 25% |
|---|---|---|---|---|---|---|---|---|---|
| tm50_k05_r025 | 5.7 | 18.5 | 5.42 | 8.4 | 17.1 | 5.26 | 13.2 | 15.3 | 5.07 |
| tm50_k05_r050 | 5.2 | 16.4 | 5.20 | 8.3 | 15.2 | 5.06 | 17.8 | 13.4 | 4.85 |
| tm50_k05_r100 | 5.6 | 14.1 | 4.96 | 11.4 | 12.9 | 4.80 | 24.6 | 10.8 | 4.51 |
| tm50_k1_r025 | 5.0 | 22.2 | 5.75 | 6.5 | 21.4 | 5.68 | 9.8 | 19.9 | 5.53 |
| tm50_k1_r050 | 4.9 | 20.0 | 5.55 | 8.2 | 18.8 | 5.43 | 12.4 | 17.1 | 5.24 |
| tm50_k1_r100 | 5.6 | 16.9 | 5.24 | 8.9 | 15.7 | 5.11 | 17.4 | 13.9 | 4.89 |
| tm50_k2_r025 | 9.2 | 24.0 | 5.91 | 10.2 | 23.5 | 5.87 | 11.5 | 22.9 | 5.81 |
| tm50_k2_r050 | 6.3 | 22.5 | 5.78 | 7.2 | 21.9 | 5.72 | 10.5 | 20.5 | 5.58 |
| tm50_k2_r100 | 5.4 | 19.8 | 5.53 | 8.1 | 18.6 | 5.41 | 12.6 | 16.9 | 5.23 |
| tm70_k05_r025 | 4.8 | 19.5 | 5.51 | 8.2 | 18.1 | 5.36 | 12.2 | 16.2 | 5.16 |
| tm70_k05_r050 | 5.7 | 17.2 | 5.28 | 8.1 | 15.9 | 5.14 | 14.8 | 14.1 | 4.94 |
| tm70_k05_r100 | 5.2 | 14.9 | 5.04 | 10.4 | 13.6 | 4.88 | 22.2 | 11.6 | 4.62 |
| tm70_k1_r025 | 6.5 | 22.9 | 5.82 | 7.4 | 22.3 | 5.76 | 10.0 | 21.1 | 5.64 |
| tm70_k1_r050 | 4.9 | 21.0 | 5.65 | 6.8 | 19.9 | 5.54 | 11.0 | 18.3 | 5.37 |
| tm70_k1_r100 | 6.5 | 17.9 | 5.35 | 9.6 | 16.7 | 5.21 | 14.7 | 14.9 | 5.02 |
| tm70_k2_r025 | 10.3 | 24.6 | 5.96 | 10.5 | 24.2 | 5.93 | 11.1 | 23.5 | 5.87 |
| tm70_k2_r050 | 8.0 | 23.3 | 5.85 | 9.0 | 22.8 | 5.81 | 10.5 | 22.0 | 5.73 |
| tm70_k2_r100 | 4.8 | 21.3 | 5.67 | 6.6 | 20.2 | 5.57 | 10.5 | 18.5 | 5.39 |
| tm90_k05_r025 | 4.3 | 20.0 | 5.55 | 7.2 | 18.6 | 5.42 | 11.4 | 16.7 | 5.22 |
| tm90_k05_r050 | 5.5 | 17.9 | 5.35 | 8.2 | 16.4 | 5.19 | 13.3 | 14.6 | 5.00 |
| tm90_k05_r100 | 5.5 | 15.4 | 5.10 | 9.4 | 14.1 | 4.95 | 20.3 | 12.2 | 4.70 |
| tm90_k1_r025 | 7.1 | 23.4 | 5.86 | 7.9 | 22.8 | 5.81 | 9.5 | 21.9 | 5.73 |
| tm90_k1_r050 | 4.3 | 21.7 | 5.71 | 5.8 | 20.6 | 5.61 | 9.6 | 19.1 | 5.45 |
| tm90_k1_r100 | 5.8 | 18.8 | 5.44 | 8.7 | 17.4 | 5.29 | 12.9 | 15.8 | 5.12 |
| tm90_k2_r025 | 11.5 | 24.8 | 5.97 | 11.9 | 24.5 | 5.95 | 12.2 | 24.1 | 5.92 |
| tm90_k2_r050 | 8.8 | 23.8 | 5.89 | 9.7 | 23.3 | 5.85 | 11.3 | 22.7 | 5.79 |
| tm90_k2_r100 | 4.6 | 22.2 | 5.75 | 6.0 | 21.3 | 5.67 | 9.0 | 19.7 | 5.52 |

### Item 4: constant return path

g = 4.74% every year (I-D1a central), GDP-per-head growth 1.57% a year, one path. Relief and M1d in percent of GDP; diff = relief - M1d (negative: retired receipts outrun relief).

**tm50_k1_r050** (tau_m 0.5): fill year 6; taxes retired by year 100: 5 of 6; first year relief < M1d: 13; P3 81.45.

| year | relief | of which M1a | M1b | M1c | M1d | diff |
|---|---|---|---|---|---|---|
| 5 | -0.000 | 11.844 | 2.820 | -14.664 | 0.000 | -0.000 |
| 10 | 6.960 | 11.296 | 2.820 | -7.157 | 4.740 | 2.220 |
| 20 | 6.464 | 10.080 | 2.820 | -6.437 | 4.740 | 1.724 |
| 30 | 6.088 | 9.165 | 2.820 | -5.897 | 4.740 | 1.348 |
| 50 | 5.042 | 6.296 | 2.820 | -4.074 | 4.740 | 0.302 |
| 100 | 2.864 | 0.087 | 2.820 | -0.042 | 4.740 | -1.876 |

**tm70_k1_r050** (tau_m 0.7): fill year 6; taxes retired by year 100: 5 of 6; first year relief < M1d: 13; P3 83.74.

| year | relief | of which M1a | M1b | M1c | M1d | diff |
|---|---|---|---|---|---|---|
| 5 | -0.000 | 13.910 | 2.820 | -16.730 | 0.000 | -0.000 |
| 10 | 7.645 | 13.165 | 2.820 | -8.340 | 4.740 | 2.905 |
| 20 | 7.001 | 11.607 | 2.820 | -7.426 | 4.740 | 2.261 |
| 30 | 6.506 | 10.408 | 2.820 | -6.723 | 4.740 | 1.766 |
| 50 | 5.027 | 6.280 | 2.820 | -4.074 | 4.740 | 0.287 |
| 100 | 2.854 | 0.076 | 2.820 | -0.041 | 4.740 | -1.886 |

**tm90_k1_r050** (tau_m 0.9): fill year 6; taxes retired by year 100: 6 of 6; first year relief < M1d: 11; P3 348.94.

| year | relief | of which M1a | M1b | M1c | M1d | diff |
|---|---|---|---|---|---|---|
| 5 | -0.000 | 15.648 | 2.820 | -18.468 | 0.000 | -0.000 |
| 10 | 8.206 | 14.703 | 2.820 | -9.317 | 8.110 | 0.096 |
| 20 | 7.414 | 12.806 | 2.820 | -8.211 | 8.110 | -0.696 |
| 30 | 6.806 | 11.338 | 2.820 | -7.352 | 8.110 | -1.304 |
| 50 | 4.930 | 6.027 | 2.820 | -3.917 | 8.110 | -3.180 |
| 100 | 2.849 | 0.069 | 2.820 | -0.040 | 8.110 | -5.261 |

### Item 5: CK1 window

P3 on g(t) = mu + A sin(2 pi t / 10), GDP-points summed over years: whole 100 years (as 055c reports it) and years 1 to fill + short horizon only.

**tm50_k1_r050**, mu 4.42:

| A | fill year | P3 whole 100 y | P3 to end of short window |
|---|---|---|---|
| 0 | 6 | 96.29 | 3.16 |
| 2 | 6 | 94.57 | 1.44 |
| 4 | 6 | 94.45 | 0.00 |
| 8 | 6 | 366.67 | 3.12 |
| 12 | 6 | 364.62 | 0.00 |

**tm50_k1_r050**, mu 4.74:

| A | fill year | P3 whole 100 y | P3 to end of short window |
|---|---|---|---|
| 0 | 6 | 81.45 | 2.79 |
| 2 | 6 | 79.87 | 0.99 |
| 4 | 6 | 338.46 | 0.81 |
| 8 | 6 | 342.08 | 1.94 |
| 12 | 6 | 343.89 | 0.00 |

**tm70_k1_r050**, mu 4.42:

| A | fill year | P3 whole 100 y | P3 to end of short window |
|---|---|---|---|
| 0 | 6 | 98.31 | 3.07 |
| 2 | 6 | 96.32 | 1.14 |
| 4 | 6 | 366.79 | 6.48 |
| 8 | 6 | 363.39 | 1.54 |
| 12 | 6 | 363.35 | 0.00 |

**tm70_k1_r050**, mu 4.74:

| A | fill year | P3 whole 100 y | P3 to end of short window |
|---|---|---|---|
| 0 | 6 | 83.74 | 2.66 |
| 2 | 6 | 338.05 | 1.15 |
| 4 | 6 | 341.56 | 5.44 |
| 8 | 6 | 340.19 | 0.77 |
| 12 | 6 | 343.59 | 0.00 |

**tm90_k1_r050**, mu 4.42:

| A | fill year | P3 whole 100 y | P3 to end of short window |
|---|---|---|---|
| 0 | 7 | 100.87 | 3.00 |
| 2 | 6 | 368.37 | 8.15 |
| 4 | 6 | 366.04 | 5.65 |
| 8 | 6 | 363.52 | 0.91 |
| 12 | 6 | 364.82 | 0.00 |

**tm90_k1_r050**, mu 4.74:

| A | fill year | P3 whole 100 y | P3 to end of short window |
|---|---|---|---|
| 0 | 6 | 348.94 | 10.23 |
| 2 | 6 | 344.64 | 7.18 |
| 4 | 6 | 342.15 | 4.90 |
| 8 | 6 | 341.60 | 0.15 |
| 12 | 6 | 345.76 | 0.00 |

**tm70_k05_r050**, mu 4.42:

| A | fill year | P3 whole 100 y | P3 to end of short window |
|---|---|---|---|
| 0 | 6 | 105.51 | 3.38 |
| 2 | 6 | 103.47 | 2.15 |
| 4 | 6 | 103.11 | 0.86 |
| 8 | 6 | 107.55 | 0.00 |
| 12 | 6 | 386.73 | 1.65 |

**tm70_k05_r050**, mu 4.74:

| A | fill year | P3 whole 100 y | P3 to end of short window |
|---|---|---|---|
| 0 | 6 | 89.48 | 3.12 |
| 2 | 6 | 87.82 | 1.83 |
| 4 | 6 | 87.72 | 0.49 |
| 8 | 6 | 364.88 | 1.74 |
| 12 | 6 | 368.80 | 1.23 |

### Item 6: chosen point for each (tol, m)

| tol | m | points passing all three | which | highest F1 among points passing M2 and M4a |
|---|---|---|---|---|
| 0 | 0% | 0 | none | 5.7 (tm50_k05_r025) |
| 0 | 10% | 0 | none | 11.4 (tm50_k05_r100) |
| 0 | 25% | 0 | none | 24.6 (tm50_k05_r100) |
| 0.05 | 0% | 0 | none | 7.0 (tm50_k05_r100) |
| 0.05 | 10% | 0 | none | 13.1 (tm50_k05_r100) |
| 0.05 | 25% | 0 | none | 26.3 (tm50_k05_r100) |
| 0.25 | 0% | 0 | none | 11.3 (tm50_k05_r100) |
| 0.25 | 10% | 0 | none | 17.8 (tm50_k05_r100) |
| 0.25 | 25% | 0 | none | 32.4 (tm50_k05_r100) |
| 1 | 0% | 0 | none | 27.6 (tm50_k05_r100) |
| 1 | 10% | 0 | none | 37.0 (tm50_k05_r100) |
| 1 | 25% | 0 | none | 50.6 (tm50_k05_r100) |

### Beyond the brief: larger margins (not part of the specified grid)

Same definitions as the summary table, margins of 50% and 100%, tolerance 0 and 1. "taxes" is the mean number retired by the end of the short window at the best point passing M2 and M4a.

| m | tol | best F1 passing M2, M4a | at | its M4a short | taxes retired | feasible points of 27 | which |
|---|---|---|---|---|---|---|---|
| 50% | 0 | 43.7 | tm50_k05_r100 | 8.5 | 4.16 | 0 | none |
| 50% | 1 | 62.9 | tm50_k05_r100 | 8.5 | 4.16 | 0 | none |
| 100% | 0 | 66.8 | tm50_k05_r100 | 5.6 | 3.61 | 0 | none |
| 100% | 1 | 79.3 | tm50_k05_r100 | 5.6 | 3.61 | 2 | tm50_k05_r100 (F1 79.3, M4a 5.6, taxes 3.61); tm70_k05_r100 (F1 76.4, M4a 6.0, taxes 3.71) |

EARLY CHECK: best F1 anywhere in the (tol, m) table is 50.6 percent.
