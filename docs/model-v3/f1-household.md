# F1 and CK1 under the household arm (brief 140c)

Status: the `safe` fund case is run (blocks 1 and 2). The `market` fund case is **not run**: brief 138c (the fund's return as a labelled axis) is not merged, and `f1_household.py --fund market` stops with that message. This note recommends nothing about the feasibility rule; the author rules. Every number is a scenario value at a labelled grid point and fund setting, never a forecast, with no central value.

## Reproduce

From the repository root, with `python -I`:

- `python -I docs/model-v3/f1-household/f1_household.py check`: the reproduction checks (`checks.md`, about 30 seconds).
- `python -I docs/model-v3/f1-household/f1_household.py f1`: block 1, writes `f1_safe_tables.md` (stdout) and `f1_safe_*.csv` (about 11 minutes).
- `python -I docs/model-v3/f1-household/f1_household.py ck1`: block 2, writes `ck1_safe_tables.md` (stdout) and `ck1_safe.csv` (about 5 minutes).

`f1` uses seed 20261118 and 200 paths (the same paths for every cell); `ck1` is one fixed path per amplitude. A second full run of `f1` and of `ck1` printed byte-identical text and CSVs (checked with `cmp`).

**Reproduction against 124c and 128c** (`checks.md`). At the 124c schedule (tau_0 0.04, tau_m 0.7, k_ln 1, ratio 0.5) and point `median_mid`: on one constant path at the register mean (4.74%) with the arm's fixed 124c rates, M1 and M1d at the short and long horizons equal the stored 124c values to 12 digits (M1 short 1.5628, long -0.3016; M1d short 4.4115, long 4.74). On the 128c market paths (seed 1, 1,000 paths in chunks of 100) M1 short (-0.1449) and M1d short (5.8659) and M1d long (7.5347) equal the stored 128c values. M1 long differs (-2.7674 against a stored -2.7702): the stored file was written before the pension-secured lien (132c) and the kernel-cap lien (133c), which are active in these runs (lien assessed and settled on the paths) and change cash receipts and the fund. The difference is in M1a long (2.1421 against 2.1359) and M1c long (-0.1948 against -0.1913); the short horizon, which F1 and CK1 read, is equal.

## What each arm assumes

| | 083c (legacy arm) | this note (household arm) |
|---|---|---|
| Consumption | share of wealth `I-D14c` (3.5%) | the household account: class balances, a saving ratio, an income path (121c to 133c) |
| Market return | one AR(1) path drives every class and the fund | fixed scenario class rates by regime; net financial and pension deviate with the path's market return (128c); property, physical, saving, income and GDP growth are scenario constants |
| Fund return | the market return on the path | `safe`: the net financial class return plus the path's deviation, a stand-in with no register row |
| Fund size | 396% (constant path) to 611% (its own paths) of GDP at the long horizon (`household-vs-legacy.md`) | at `median_mid`, 31 to 106% of GDP in year 10 and 41 to 92% in year 100 across the 27 schedule points (`f1_safe_tables.md`) |
| Scenario | one: central inputs | five labelled points (none central): saving min, median, max at regime `mid`; regimes `low` and `high` at median saving |
| Paths | 1,000 | 200 |
| Schedule points | the 27 of the lever grid | the same 27 at each of the five scenario points (135 cells) |

Tolerances (0, 0.05, 0.25, 1.0 GDP-points) and retirement margins (0, 10, 25%) are 083c's. F1 is the share of paths whose P3, summed from year 1 to the end of the short window (the 10 years after the fill), is at most the tolerance. Feasible means F1 at least 75%, M2 short at most 2.0 and M4a short at least 0.

Twelve of the 135 cells did not run: the arm raised its own I1 alarm on a path (the known 128c alarm; 135c and 137c are open). They are `min_mid` 2, `max_mid` 2 and `median_high` 8 schedule points, listed in `f1_safe_failed.csv`. They are left out of every table and nothing was worked around. `median_mid` and `median_low` ran all 27.

## F1 under the household arm

Best F1 anywhere in a cell (percent of paths; 083c's best-any column for comparison; the full tables with M2, M4a and the best point passing them are in `f1_safe_tables.md`):

| tol | m | 083c | min_mid | median_mid | max_mid | median_low | median_high |
|---|---|---|---|---|---|---|---|
| 0 | 0% | 11.5 | 9.5 | 9.0 | 19.0 | 5.5 | 22.0 |
| 0 | 10% | 11.9 | 22.5 | 21.0 | 19.0 | 14.0 | 22.5 |
| 0 | 25% | 24.6 | 37.0 | 35.5 | 30.0 | 26.0 | 40.0 |
| 0.05 | 0% | 11.5 | 10.5 | 9.0 | 19.5 | 8.0 | 22.0 |
| 0.05 | 10% | 13.1 | 26.5 | 23.0 | 19.5 | 17.5 | 22.5 |
| 0.05 | 25% | 26.3 | 41.0 | 38.5 | 32.0 | 29.5 | 41.5 |
| 0.25 | 0% | 12.4 | 14.5 | 12.0 | 20.0 | 14.0 | 23.0 |
| 0.25 | 10% | 17.8 | 34.0 | 30.5 | 21.0 | 25.0 | 29.5 |
| 0.25 | 25% | 32.4 | 47.0 | 46.5 | 39.5 | 35.5 | 47.5 |
| 1 | 0% | 27.6 | 27.5 | 25.0 | 24.5 | 28.5 | 30.0 |
| 1 | 10% | 37.0 | 52.5 | 45.0 | 37.0 | 40.5 | 44.0 |
| 1 | 25% | 50.6 | 67.5 | 65.5 | 60.0 | 52.5 | 65.5 |

- **No cell is feasible:** 0 of 60 (point, tol, m) cells. The best F1 is 67.5% (`min_mid`, tol 1, m 25%, `tm50_k05_r100`), against 75% required; 083c's best was 50.6%.
- **At the 055c rule (tol 0, m 0)** F1 over the schedule points runs 1.5 to 9.5% at `min_mid`, 1.5 to 9.0% at `median_mid`, 0.5 to 5.5% at `median_low`, 3.0 to 19.0% at `max_mid` and 5.5 to 22.0% at `median_high` (083c: 4.3 to 11.5%). At `max_mid` and `median_high` the best point is `tm90_k2_r025`, where M2 short is above the 2.0 cap; the best F1 passing M2 and M4a is lower there (9.5 and 11.0).
- **M2 and M4a:** at `median_mid` M2 short runs 0.60 to 4.33 and is at most 2.0 at 21 of 27 schedule points; M4a short runs 12.4 to 25.1 and the floor of 0 never binds. The binding condition is F1.
- **Fund filled:** no path is unfilled at `median_mid`; the mean fill year is 6.7 to 7.5; taxes retired by the end of the short window 4.83 to 6.00 on average (083c: 4.96 to 5.97).
- **Sampling:** the standard error of a share on 200 paths is 1.5 points at 5%, 2.1 at 10% and 3.5 at 50%; the same paths are used for every cell, so differences between cells are tighter than that.

## Is the failure structural? Yes in 083c's sense, with another mechanism

083c's test: a path with no volatility at all already fails. Here it does too. On the constant path at 4.74% (`f1_safe_constant_path.csv`, three schedules at each of five points, 15 rows) relief first falls below M1d in year 13 in every row, inside the short window (which ends in year 17), and P3 to the end of the short window is 0.29 to 6.90 GDP-points, never zero. Volatility is not needed to fail.

The mechanism is not 083c's. There the wealth-tax receipts M1a decayed (11.3% of GDP in year 10 to 0.09 in year 100 at tau_m 0.5) until relief sat at about 2.85, below the 4.74 of five retired taxes. Under the household arm M1a does not decay (at `median_mid`, tau_m 0.5: 10.1 in year 10, 7.06 in year 100) and relief stays above M1d on average (5.58 against 4.74 in year 100). The failure is timing. At `median_mid`, tm70_k1_r050, constant path, per cent of GDP:

| year | M1a | M1b | M1c | relief | M1d | fund S |
|---|---|---|---|---|---|---|
| 10 | 11.90 | 2.82 | -7.24 | 7.48 | 4.74 | 45.5 |
| 11 | 1.06 | 2.82 | 3.52 | 7.40 | 4.74 | 41.8 |
| 12 | 1.06 | 2.82 | 3.44 | 7.33 | 4.74 | 38.1 |
| 13 | 1.06 | 2.82 | -0.06 | 3.82 | 4.74 | 38.0 |
| 14 | 1.06 | 2.82 | -0.06 | 3.82 | 4.74 | 37.9 |
| 15 | 11.55 | 2.82 | -7.06 | 7.32 | 4.74 | 44.8 |

M1a is about 1.0 in four years of five and about 11 to 12 in the fifth (years 10, 15, 20 and on). The fund takes the lump in (M1c about -7), pays it out over the next two years (M1c about +3.5), and in the two years after that has nothing to pay, so relief is M1a plus M1b, about 3.8, below M1d. Summed over years 10 to 14 relief is 29.85 against 23.70 for M1d: the cycle covers M1d on average and fails in two years of five. The fund fills in year 7 in all 15 rows and the first retirement is year 8 at `median_mid`; the first shortfall is year 13 in every row.

The lump is the arm's death-phase structure: six phases with a 30-year generation, so one sixth of the base settles at death each fifth year (`revenue.run_lines`: first deaths at ceil(i G / n_phase), then every G years). I read this from the components; I did not test it by changing the phases or the fund's payout parameters, and I did not trace why the payout takes two years. Both are outside this brief. The legacy arm has the same six phases, so the year-13 first shortfall in 083c may share this cause; that is not established here.

## CK1 under the household arm

Fixed path g(t) = 4.74 + A sin(2 pi t / 10), one path per amplitude A in 0, 1, 2, 3, 4, 5, 6, 8, 10, 12 (the manifest's 1, 3, 5, 8, 12 and 083c's 0, 2, 4, 8, 12, with the gaps filled), schedules tm50, tm70, tm90 (k_ln 1, ratio 0.5) and tm70_k05_r050, at each of the five scenario points (`ck1_safe.csv`, `ck1_safe_tables.md`). No cell failed.

- **P3 is positive at A 0 in all 20 rows** (0.29 to 6.90 to the end of the short window), so there is no amplitude up to which P3 is zero on every smaller amplitude, in any of the three windows (short window proper, years 1 to the end of the short window, all 100 years). Under the strict reading of CK1 (P3 equal to zero up to a stated amplitude) it does not pass at any point. P3 before the first retirement is zero, so the short-window-proper and years-1-to-end-of-short-window values are equal in all 200 cells.
- P3 is zero only at isolated larger amplitudes, in 21 of 200 cells (for example `median_mid`, tm50_k1_r050 at A 5 and 6; `max_mid` and `median_high` tm70_k05_r050 at A 4 to 6), and it is not monotone in A.
- **P3 over all 100 years** is 34 to 118 at A 0 and in many rows jumps by a few hundred at one amplitude (`median_mid`, tm70_k1_r050: 44 at A 3, 280 at A 4; `median_mid`, tm70_k05_r050 has no jump up to A 12: 53 to 76). 083c's item 5 shows the same kind of step (tm70_k1_r050, mu 4.74: 84 at A 2, 338 at A 4). I did not trace the step.
- **P1** (fill year) is 6 or 7 and every row fills. **P7b** (minimum cover) is 0.93 to 1.43 over the years after the fill to the end of the short window and 0.81 to 1.43 over all years after the fill. Transition adds no years after the fill, so P7b has the two windows only.

## What this note does not do

It does not pick a tolerance, a margin or a different rule, and it does not name a feasible schedule: none is feasible on the numbers above. It does not run the `market` fund case (138c), the 1,000-path and level 2 versions, or OF1 and CK1 themselves (089c). The five scenario points are not a range around a central value; the grid has none.

## Where this needs the author's ruling

- The feasibility rule (the diagnosis above is the input): which of tolerance, margin or a different test, and whether F1 should see the six-phase cycle at all.
- Whether the `market` fund case should be run before the ruling (138c first).
