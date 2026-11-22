# The household arm: first run (brief 124c)

Status: first run, three of five grid points complete; two fail I1 and are reported with their inputs. Every number is a **scenario value at a labelled grid point, not a forecast and not a central case**. Class returns are fixed scenario rates: the market path is not read by the household arm. Written for the author. No parameter, rule or model file was changed to produce it, apart from one defect fix named under "Needs the author".

## Grid and setup

Five labelled points, none central. Setup common to all: schedule tau_0 0.04, tau_m 0.7, k_ln 1, ratio 0.5; B.6g income scale 1.3733; tail pension cap I-D1l; stand-in safe return (the net financial class return); withheld ids stay withheld (O3, OH1b, OH1c, OW1, OW3, OM1).

| Point | Saving ratio | Regime | Result |
|---|---|---|---|
| `min_mid` | min of the series | mid | **fails I1** |
| `median_mid` | median | mid | run, all checks hold |
| `max_mid` | max | mid | run, all checks hold |
| `median_low` | median | low (JST 1947-79) | run, all checks hold |
| `median_high` | median | high (JST 1980-2019) | **fails I1** |

Paths: 1,000 per point (chunk 100, seed 1). The brief caps it at 2,000; P10 and P90 need hundreds of paths, and 1,000 costs about two minutes a point. See the first finding under "Odd": the household arm turned out to be identical on every path, so the number was not needed. The legacy arm (`I-D14c`, 3.5%) is run on the same paths as **labelled context only**. Script `household-arm-run/run_grid.py`; `ranges.py` writes `ranges.csv` (min to max across the three complete points). Files: `grid_results.csv` (one row per cell and point: a mean, b P10, c P90, or the stored values), `checks.csv`, `ranges.csv`.

## Checks

| Point | Account residual (max) | `unpaid` | `unpaid_B` | Shortfall lines | Ledger tie (max) | I1 |
|---|---:|---:|---:|---:|---:|---|
| `min_mid` | | | | | | **FAILED** |
| `median_mid` | 1.5e-11 | 0 | 0 | 0 | 1.6e-12 | holds |
| `max_mid` | 1.3e-11 | 0 | 0 | 0 | 1.3e-11 | holds |
| `median_low` | 1.4e-11 | 0 | 0 | 0 | 1.7e-12 | holds |
| `median_high` | | | | | | **FAILED** |

The three complete points hold every check. The two failures raise before any output exists, so those points have no rows.

- `min_mid`: I1 fails at threshold ratio 0.25 (the B1 rerun), line D5, year 78. The non-pension class total is -0.0012 (net financial -0.1329) against the kernel's family value floored at 0.
- `median_high`: I1 fails at ratio 0.25 (year 70) and at the schedule's own ratio 0.5 (year 97), line D10a. The non-pension classes are drained to 0.0015 while the pension holds 6.45.

Common reading, not a diagnosis: a line whose non-pension classes are exhausted is floored at zero in the kernel's family value but the class book goes slightly negative, so the two disagree by a small amount. The rule is not changed here; the inputs are above (point, ratio, line, year).

## Ranges across the three complete points (min to max; no central)

Unit as the manifest states. Where fewer than three points have a value (a `nan` at a point, e.g. the reserve not filling), the range is over the points that have one; `ranges.csv` holds `n_points`. The legacy column is context from the same paths, not a comparison target.

**Headline, schedule S (O1, % of GDP)**

| Line | Horizon | Household, min to max | Legacy (context) |
|---|---|---:|---:|
| M1 net effect | short | 0.05 to 1.56 | 0.28 |
| | long | -1.43 to 0.49 | -3.26 |
| | transition | 0 (to 1e-15) | 0 |
| M1a gross receipts | short | 2.43 to 4.48 | 3.66 |
| | long | 0.88 to 6.66 | 1.18 |
| M1b | short, long | 2.82 | 2.82 |
| M1c | short | -0.39 to -0.04 | -0.31 |
| | long | -0.88 to -0.11 | 0.04 |
| M1d | short | 4.41 to 7.15 | 5.89 |
| | long | 4.74 to 8.11 | 7.29 |

M1d by tax (O1d) is equal across points except corporation tax (long 0 to 3.37; legacy 2.58); the other lines do not move with the grid. The break-even `O1f` is 0 or 1 (a flag).

**Burden in life, M2 by wealth band (O2, % per year, long)**

| Band | Household | Legacy (context) |
|---|---:|---:|
| D4-5 | 0.27 to 0.30 | 0.48 |
| D6-7 | 0.11 to 0.37 | 0.52 |
| D8-9 | 0.12 to 0.43 | 0.63 |
| D10 | 0.20 to 0.46 | 1.50 |
| overall | 0.15 to 0.38 | 1.27 |

Short horizon, overall: household 0.22 to 0.47, legacy 2.44. M2b and M2c (cash-flow cutoffs) range from 0 to 96.4 and 0 to 5.6 across cells (see `ranges.csv`); M2d, the lifetime figure, is 8.7 to 12.2 overall at the long horizon (legacy 13.8), D10 14.7 to 19.0 (legacy 17.2).

**Distribution and support (long)**: M4a (income deciles) overall 13.1 to 25.1 (legacy 22.2), D10 7.1 to 17.6 (15.1), D1 27.7 to 36.2 (34.1); M4b overall 4.4 to 8.4 (7.45). OL1 monthly cost for a p50 worker: 219 to 397 (legacy 354). O5 differences against the comparators are about 0.6 to 1.4 pp (green 1.21 to 1.43 against legacy 0.32; once 0.62 to 0.85 against legacy -0.27). O6, OW2, OD1, OH1b2 and O7 do not move across points.

**Public ledger (single)**: P1 7 years at all three points (legacy 6.6). P3 debt 43 to 107% of GDP (legacy 277). P4 ratio -3.14 to 10.2 (legacy -0.41). P5 by tax is 0 to 10 years for corporation tax and the same elsewhere. P6 debt path: year 10 38 to 52% of GDP, year 50 28 to 59, year 100 22 to 78 (legacy 64, 230, 1,170). P7a 0; P7b 0.94 to 1.15 (legacy 1.25). B1 (OB1): B1a 70 to 100, B1b 0 to 0.20, B1c 0, B1d 0 at the `r025` threshold (legacy 40.5, 2.61, 4.24, 0). S1: M1 -2.31 to 0.32 (legacy 0.27).

## Odd, listed without a verdict

1. **No spread across paths.** Every household cell has P10 = mean = P90 (371 of 371 `p10_mean_p90` cells). The brief expected GDP growth to move with the path; `run_grid.py` and `core_run` pass `np.full(g.shape, ctx.gdp_g)`, a constant, so the household arm is deterministic and one path would have given the same numbers. The legacy arm does spread (it reads `g`). A range across paths therefore does not exist for the household arm; the ranges above are across grid points only. This needs a decision (per-path GDP growth, or accept a deterministic arm).
2. **Two of five grid points fail I1** (checks above), including the min-saving point, so the range in saving is known only from median and max.
3. **Empty cells.** 50 of 486 cells hold no value at any point: they are the withheld ids (OW1, OW3, OM1, O3), by design. A further 24 cells (the O2 family) are `nan` at one or two points, mainly D4-5 at the short and transition horizons, where the reserve does not fill (the existing gate, also seen under the legacy arm); a cell that never fills at any point is not seen.
4. **The household M2 is an order below the legacy M2 in the top bands** (D10 long 0.20 to 0.46 against 1.50; short 0.28 to 0.55 against 3.01) and the household debt path ends far below the legacy one (P6 year 100: 22 to 78% against 1,170%).
5. **P4 is negative at `median_low`** (-3.14) and 10.2 at `max_mid`: a ratio with a denominator near zero or a sign change; not investigated.
6. **M1 transition is zero** (1e-15) at every point and arm; M1b is the same 2.82 everywhere.
7. **Debt floor.** The class rule floors a negative property or net financial balance at 0% real, a labelled assumption of the arm; it is the likeliest place for the I1 failures to come from, but this is a guess.

## Needs the author

- **A defect fixed outside Touches.** Level 1 under the household arm raised because `out_support.per_path` returned `None` for the withheld groups and `runner.cat` cannot concatenate `None`; it now returns `{}` (8 lines in `model_v3/runner/out_support.py`, a 121c defect). The brief names the runner as not touched, so by the auto-merge rule **this branch is not merged: NEEDS THE AUTHOR** (accept the fix, or have it made in its own brief).
- The I1 failures at `min_mid` and `median_high`, and the no-spread finding, are for the author and guru to read.

## Next

- The tornado (OT1) and the feasibility map (OF1) on the full model under the household arm: not run. Both are sweeps, neither has been exercised under the household arm (121c), and the session stopped after three blocks.
- Decide whether the household arm should take a per-path GDP growth (finding 1) before more paths are run.
- I1 at `min_mid` and `median_high`: a brief for the class-floor reconciliation.
