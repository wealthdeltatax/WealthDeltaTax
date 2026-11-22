# The household arm with per-path market returns (brief 128c)

Status: run, three of five grid points complete; two raise I1 on a single path and are reported as alarms. **Market-return risk only.** Household behaviour is the scenario constants; only the market return varies by path. Every number is a scenario value at a labelled grid point, not a forecast, not a central case, no headline. Written for the author.

## Rule and label

Net financial and pension add `g - mu` (loading 1; `mu = I-D1a / 100`, the generating mean of the market path `g`). Property (0.016455) and physical (I-D1j) stay fixed. GDP growth stays a constant. Pension is never sold. Zero deviation is byte-identical to the fixed-rate arm (test). The legacy arm and `test_legacy_digest` do not move. Switch: `paths: true` in the arm dict (`run_grid.py --market-paths`). Each row's label ends "market-return risk only (128c)"; `label['scenario']` carries `market_paths` and `central: false`.

Setup is as in `household-arm-run.md` (five points, 1,000 paths, chunk 100, seed 1). Files: `household-arm-run/grid_results_paths.csv`, `checks_paths.csv`, `ranges_paths.csv` (`ranges.py --market-paths`).

## Checks

| Point | Account residual | `unpaid` | `unpaid_B` worst | `unpaid_B` path-phases | Shortfall lines | Ledger tie | Spread / flat cells | I1 |
|---|---:|---:|---:|---:|---:|---:|---|---|
| `min_mid` | | | | | | | | **ALARM** |
| `median_mid` | 2.8e-11 | 0 | 2.36 | 2,776 | 13,152 | 5.9e-12 | 291 / 132 | holds |
| `max_mid` | 3.0e-11 | 0 | 2.46 | 446 | 953 | 2.9e-11 | 258 / 165 | holds |
| `median_low` | 2.5e-11 | 0 | 14.4 | 6 | 6 | 4.3e-12 | 289 / 134 | holds |
| `median_high` | | | | | | | | **ALARM** |

`ledger_dL` (the fund tie to the book change) is at most 1.5e-11 at the three held points. The held points keep I1, the account identity and the ledger ties on every path and year.

**I1 alarms (reported, nothing changed):**

- `min_mid`: chunk path 9, line 3, year 96. Family value -0.077135, class total -0.0723546; balances property 0.112454, net financial -0.201371, physical 0.0165618, pension 1.15916. The family value and the class total differ by 0.0048.
- `median_high`: chunk path 34, line 8, year 81. Family value 0, class total 1.28519e-09; balances property 0, net financial 1.28519e-09, physical 0, pension 11.5916. A rounding-size residual on a line whose non-pension classes are exhausted.

Both are the same family as the 124c failures (a line whose non-pension classes are drained, against the kernel's family value). Per-path returns reach them on a path at both points that held under fixed rates only at some of them. Not diagnosed. The grid at these two points has no rows, so the range in saving is known only from median and max (and the low regime).

**`unpaid_B` by path.** `unpaid_B` is nonzero on 2,776 path-phases at `median_mid` (worst 2.36), 446 at `max_mid` (2.46) and 6 at `median_low` (14.4). Under fixed rates it was 0 at the same points. `unpaid` is 0 everywhere. The shortfall lines follow the same pattern (13,152; 953; 6). The pension-secured lien exists (132c); these are the cases it does not cover.

## P10 / mean / P90 across paths, ranges across the three held points

Selected cells (`grid_results_paths.csv` has all 486; the three held points are the range; units as the manifest states). Format: P10, mean, P90 per point.

| Cell (O1 schedule S, % of GDP) | `median_mid` | `max_mid` | `median_low` |
|---|---|---|---|
| M1 net, short | -1.99, -0.145, 1.15 | -1.80, 0.163, 1.90 | -2.89, -0.516, 0.873 |
| M1 net, long | -4.54, -2.77, -0.517 | -2.82, 1.77, 8.10 | -5.09, -3.13, -1.18 |
| M1a gross receipts, long | 0.912, 2.14, 4.12 | 3.17, 8.28, 15.5 | 0.676, 0.937, 1.25 |
| M1 net, transition | about 0 (1e-15) | about 0 | about 0 |

In every cell with spread, P10 <= mean <= P90 (checked in `run_grid.py`). Across the three points the mean of M1 net is -0.52 to 0.16 (short) and -3.13 to 1.77 (long); M1a long 0.94 to 8.28; M1d (by tax) long 6.49 to 8.10, short 5.36 to 6.52 (legacy 7.29, 5.89, context). The long horizon at `max_mid` is far wider than at the other points. The distribution is wide relative to the fixed-rate 124c ranges (M1 long -1.43 to 0.49), and the mean at `median_mid` long (-2.77) differs from the fixed-rate figure at the same point: the mean over paths is not the fixed-rate value, because the system is non-linear in the return.

By family, cells with spread at any held point: O1 25 of 45, O2 115 of 120, O4 44 of 66, O5 15 of 30, OB 27 of 36, OL 8 of 12, OP 13 of 13, OW 36 of 42, O8 4 of 4. Distribution output O2 (burden in life by wealth band) has spread in 115 of its 120 cells.

## Cells without spread (listed, not uncertainty)

- GDP-only or fixed-class cells: M1b (2.82 at every point), the transition line M1d (0), O6, O7, OD1, OH1b2, OR1, OS1: no spread at any point, because they depend on the constant GDP growth and the fixed classes (property, physical), not on the return path.
- Flat cells by point: 132 (`median_mid`), 165 (`max_mid`), 134 (`median_low`) of the `p10_mean_p90` cells; 134 have no spread at any held point (`ranges_paths.csv`, `path_spread`).
- Empty at every household point: OW3 and (by `ranges_paths.csv`) 7 all-nan cells. The 124c reserve-not-filling cells (O2, D4-5 short/transition) are still `nan` at some points.

## Odd, listed without a verdict

1. **OW1 is not withheld in the run output.** `arm.withheld()` lists OW1 as `legacy_only` under per-path returns (the comparators run on fixed scenario rates, not like for like), and a test checks it, but `grid_results_paths.csv` holds OW1 values at the household points (for example -540 at `median_mid`, mean). Nothing in `run_grid.py` applies `withheld()`. Read OW1 under per-path returns as **not valid**. The 124c note said OW1 was withheld by design; that mechanism is not visible in this path.
2. **I1 raised under per-path returns**, once at each of two points, and a pre-fix raise at `median_mid` (a refund on a line with no positive non-pension balance). The latter is fixed in `_pay` (a refund on a line whose non-pension classes are non-positive goes to net financial). That is a settlement-rule change; the brief says "settlement rules unchanged". Flagged for the author.
3. **Unexplained ledger tie gap** in a 20-path smoke run at `min_mid` (167 bn, years 62 and 85, path 18). At 1,000 paths `min_mid` fails I1 before any tie is reported, so this is not reproduced at the grid. Not diagnosed.
4. **`unpaid_B` appears under per-path returns** (2,776 path-phases at `median_mid`); under fixed rates it was 0. This is the first sign of the lien not covering a bad path.
5. **M1 transition** is zero (1e-15) at every point, as in 124c.
6. **The mean over paths is not the fixed-rate value** (M1 net long at `median_mid`: -2.77 here). The fixed-rate arm is the zero-deviation case, not the mean case.

## Needs the author

- Two things outside the brief's Touches: `model_v3/core/revenue.py` line 146 (one line, byte equal when `mu` is None) and the refund routing in `_pay`. By the auto-merge rule this branch is **not merged: NEEDS THE AUTHOR**.
- Two I1 alarms (above), `unpaid_B` counts, and the OW1 finding.
- Per-path GDP growth stays out by decision, so GDP-only cells stay flat.

## Next

- A brief to reconcile the class floor with the family value (the I1 alarms at both points, 124c and 128c).
- Apply `withheld()` in the grid writer, or confirm OW1 is read as invalid.
- Out of scope here: heterogeneity, a saving gradient, pension withdrawal, per-path GDP, validation, OT1 and OF1.
