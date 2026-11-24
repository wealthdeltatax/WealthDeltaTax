# The household arm with per-path market returns (brief 128c)

Status: run, three of five grid points complete; two raise I1 on a single path and are reported as alarms. **Market-return risk only.** Household behaviour is the scenario constants; only the market return varies by path. Every number is a scenario value at a labelled grid point, not a forecast, not a central case, no headline. Written for the author.

## Rule and label

Net financial and pension add `g - mu` (loading 1; `mu = I-D1a / 100`, the generating mean of the market path `g`). Property (0.016455) and physical (I-D1j) stay fixed. GDP growth stays a constant. Pension is never sold. Zero deviation is byte-identical to the fixed-rate arm (test). The legacy arm and `test_legacy_digest` do not move. Switch: `paths: true` in the arm dict (`run_grid.py --market-paths`). Each row's label ends "market-return risk only (128c)"; `label['scenario']` carries `market_paths` and `central: false`.

Setup is as in `household-arm-run.md` (five points, 1,000 paths, chunk 100, seed 1). Files: `household-arm-run/grid_results_paths.csv`, `checks_paths.csv`, `ranges_paths.csv` (`ranges.py --market-paths`).

## Checks (128c, 1,000 paths, before the lien; superseded above)

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

## I1 tolerance and the lien's limited recourse (brief 138c, block 1a)

**I1 tolerance.** The hook's check (`HouseholdHook._check`, also run at `post`) now allows an absolute 1e-7 (never tighter than the earlier 1e-9 relative), the kernel cap's own tolerance on the lien's unit part (the 135c residuals of 1.0e-9 to 5.0e-8 on lines the floor holds at 0). No change in `core/`. A test: a gap of 5e-8 passes, 1e-6 raises. `median_high` now runs at 200 paths (checks below, its account residual is 1.6e-9, the residuals' size).

**Limited recourse.** `settle` collects up to the pension; the remainder `rest` is no longer kept in the lien and in `unpaid_B` but written off in the public ledger's write-off column (`wo`, as the floor's does): the lien never exceeds the pension after a settlement, `PL` and `PK` are 0 and the ledger balance ties (opening - settled - written off = closing; tests). Where it does not fire, nothing moves. At `min_mid` (200 paths, first chunk of 100 paths for the ledger): one path-phase writes off 357.7 bn (after weighting) in total; `median_mid` and `median_high` none.

| Point (200 paths) | `unpaid_B` worst | `unpaid_B` path-phases | Shortfall lines | Account residual | Ledger tie | `ledger_dL` | Spread / flat | I1 |
|---|---:|---:|---:|---:|---:|---:|---|---|
| `min_mid` | 0.253 | 2,634 | 7,315 | 2.5e-11 | 3.6e-10 | 2.6e-12 | 278 / 129 | holds |
| `median_high` | 0 | 0 | 0 | 1.6e-9 | 1.6e-10 | 2.9e-11 | 251 / 156 | holds |

`min_mid` `unpaid_B` fell from 3.02 to 0.253; the rest is another cause, the class floor's alarm (`fl`, added to `unpaid_B` in `pre`), not the lien. Not changed here. The other three points are unchanged by it (`median_mid`, `max_mid` and `median_low` write nothing off). The heir floor (148c) is a separate later switch.

## Rerun at 200 paths with the lien in place (brief 135c)

`run_grid.py --market-paths --paths 200` (chunk 100, seed 1), 133c lien and 137c floor and the restart fix in place; files `grid_results_paths.csv`, `checks_paths.csv`, `ranges_paths.csv` replaced. This replaces the 1,000-path tables below (128c, before the lien). Held-point checks:

| Point | Account residual | `unpaid` | `unpaid_B` worst | `unpaid_B` path-phases | Shortfall lines | Ledger tie | `ledger_dL` | Spread / flat cells | I1 |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `min_mid` | 2.5e-11 | 0 | 3.02 | 2,638 | 7,321 | 3.6e-10 | 2.6e-11 | 278 / 129 | holds at 200 paths (raises at 1,000, see Diagnosis) |
| `median_mid` | 2.6e-11 | 0 | 0 | 0 | 0 | 5.9e-12 | 5.5e-12 | 274 / 133 | holds |
| `max_mid` | 2.5e-11 | 0 | 0 | 0 | 0 | 2.5e-11 | 2.9e-11 | 245 / 162 | holds |
| `median_low` | 2.5e-11 | 0 | 0 | 0 | 0 | 4.3e-12 | 1.3e-12 | 273 / 134 | holds |
| `median_high` | | | | | | | | **ALARM** (I1 fails within 200 paths; 1.0e-9 to 5.0e-8 residuals, Diagnosis) |

With the lien carrying the tax the cap could not collect, `unpaid_B` is gone at `median_mid`, `max_mid` and `median_low` (it was 2,776, 446 and 6 path-phases); it remains at `min_mid` (worst 3.02 billions after weighting, on 2,638 path-phases): the pension cannot cover the lien there (133c's draw limit, the author's question). Alarms that remain: `median_high` I1 (tolerance-size), `min_mid` I1 at 1,000 paths (tolerance-size) and `min_mid` `unpaid_B`. No headline number. OW1 is the marker `withheld (legacy_only)` in every household row and `ranges_paths.csv` (test on the written CSV); the fixed-rate CSVs are not rewritten: a fresh run of `median_mid`, `max_mid` and `median_low` equals every cell they hold (1,308 cells, 0 differ; 150 later ids are new to a fresh run).

## Diagnosis of the loose ends (brief 135c)

Run on main with the 133c lien and 137c floor: `run_grid.py --market-paths`, point at 1,000 paths, chunk 100, seed 1, every failing check logged (not raised). Balances in millions of pounds per adult; PL and PK the lien and its part netted from the pension.

**The two alarms.** Both still raise, at other lines than 128c reported (the lien and the floor moved them). Each is a residual of 1e-9 or more against the check's 1e-9 tolerance, on a line whose non-pension balances are zero or near zero and whose pension is 8 to 57.

| Point | Path, line, year | Family value | Class total | Diff | PL - PK | Pension | Rule | Cause |
|---|---|---|---|---|---|---|---|---|
| `min_mid` | 66, 10, 96 | -0.005821972896 | -0.005821971311 | 1.6e-9 | 1.07e-10 | 19.06 | `_check` (post), kernel cap (`Lp > hold + 1e-9`) | tolerance |
| `median_high` | 34, 9, 81 | 0 | -1.02e-9 | 1.0e-9 | 1.02e-9 | 13.74 | same | tolerance |

Not a bookkeeping error and not economics: relative to the balances the gap is 1e-10 to 1e-9, the size of the kernel cap's own 1e-9 tolerance (what the cap leaves unpaid is the lien's unit part, PL - PK, which sits in the class total and not in the family value of a line the floor holds at 0). A further 10 events at `median_high` (1,000 paths) are the same kind: 1.0e-9 to 7.1e-9, and one of 5.0e-8 (path 60, line 10, year 96, PL - PK 5.03e-8, pension 57.5). Reported, not tuned. The cap is 133c's; a kernel change is stop-and-report. **Needs the author:** to loosen the check to the cap's tolerance (absolute 1e-7) or to have the cap hand over the whole excess.

**A third case found and fixed (bookkeeping).** `median_high`, path 69, line 7, year 96 (1,000-path run): family 0.000917 against class total 0.00204 (diff 1.1e-3, PL 0, pension 0.589). The line's lien (2.86) was settled at year 95, which rescaled the route units by N/family with N = 0, leaving prices at 0 and unit fractions at about 1e18 (A: -2.5e18). The 137c restart then added the target to that f (f + u) and lost it in rounding: family 0.5 for 1. Fix in `HouseholdHook._restart`: for a wiped line (`bad`) f is the target and `sold` is the identity's remainder (`tot - s - f`); other lines keep their arithmetic. Test: `test_a_dead_line_with_huge_units_restarts_exactly_and_i1_holds` (fails without the fix).

**The ledger tie gap (167 bn, 20 paths, `min_mid`, years 62 and 85, path 18): not reproducible.** Tried: `run_grid.py --market-paths --paths 20 --points min_mid --no-legacy` (chunk 20, seed 1) on main with the lien as a ledger receivable (132c, 133c): ledger tie max 1.8e-12, dL max 1.0e-12, I1 held, no tie gap. The 128c gap predates the lien receivable. Not diagnosed beyond that.

## Odd, listed without a verdict

1. **(Fixed in 135c: marker, test on the CSV.) OW1 is not withheld in the run output.** `arm.withheld()` lists OW1 as `legacy_only` under per-path returns (the comparators run on fixed scenario rates, not like for like), and a test checks it, but `grid_results_paths.csv` holds OW1 values at the household points (for example -540 at `median_mid`, mean). Nothing in `run_grid.py` applies `withheld()`. Read OW1 under per-path returns as **not valid**. The 124c note said OW1 was withheld by design; that mechanism is not visible in this path.
2. **I1 raised under per-path returns**, once at each of two points, and a pre-fix raise at `median_mid` (a refund on a line with no positive non-pension balance). The latter is fixed in `_pay` (a refund on a line whose non-pension classes are non-positive goes to net financial). That is a settlement-rule change; the brief says "settlement rules unchanged". Flagged for the author.
3. **(135c: not reproducible, see Diagnosis.) Unexplained ledger tie gap** in a 20-path smoke run at `min_mid` (167 bn, years 62 and 85, path 18). At 1,000 paths `min_mid` fails I1 before any tie is reported, so this is not reproduced at the grid. Not diagnosed.
4. **`unpaid_B` appears under per-path returns** (2,776 path-phases at `median_mid`); under fixed rates it was 0. This is the first sign of the lien not covering a bad path.
5. **M1 transition** is zero (1e-15) at every point, as in 124c.
6. **The mean over paths is not the fixed-rate value** (M1 net long at `median_mid`: -2.77 here). The fixed-rate arm is the zero-deviation case, not the mean case.

## Per-path GDP growth, `gdp_paths` (brief 148c)

A scenario switch, off by default (off is byte-identical). **A scenario, not a forecast; no central value; no headline number.** Code: `model_v3/runner/flow_switches.py`; evidence 146r (one country's history, derived). Run: `household-arm-run/run_grid.py --paths 200 --no-legacy [--market-paths] --gdp-paths indep|hist --out household-arm-run/gdp_paths`; summary: `gdp_spread.py` (writes `gdp_spread.csv`); files in `household-arm-run/gdp_paths/`. Five grid points, 200 paths (two chunks of 100).

**Rule.** Real GDP growth per head is the pack constant plus a zero-mean AR(1) deviation (marginal SD 2.68 points, lag-1 0.28; the mean is not moved). Its innovation is correlated with the market return's by 0 (`indep`, "growth risk only") or 0.37 (`hist`, "growth and market risk, correlated"). With no market paths (`alone`) the market return is still drawn, so `hist` correlates GDP with it but the household's classes stay at their fixed returns.

**What scales with the GDP path.** The GDP index (so M1 and P6, which are shares of GDP), the contribution threshold W_min (indexed to GDP per head), and the household's income (so its saving and the accrual in pounds). **What does not:** property, physical and the fund's safe stand-in (as in 128c), and the quantities that read fixed scenario rates per line and not per path, which `arm.withheld` withholds (as under market paths).

**P6 (fund as % of GDP), schedule S, year 50: P10 / mean / P90 across 200 paths.** The point value with the switch off is in the first column (no spread without paths).

| Point | alone, off | alone, `indep` | alone, `hist` | market paths, off | market paths, `indep` | market paths, `hist` |
|---|---|---|---|---|---|---|
| `min_mid` | 34.3 | 25.4 / 36.4 / 47.3 | 25.3 / 36.3 / 46.9 | 24.1 / 42.3 / 66.9 | 22.4 / 44.9 / 74.5 | 24.2 / 42.9 / 67.2 |
| `median_low` | 24.8 | 21.0 / 25.9 / 30.8 | 21.2 / 25.8 / 30.5 | 21.4 / 28.0 / 37.1 | 20.0 / 29.6 / 41.3 | 20.9 / 28.5 / 38.0 |
| `median_mid` | 35.7 | 26.9 / 37.9 / 49.2 | 26.4 / 37.9 / 48.8 | 26.0 / 44.9 / 70.7 | 24.1 / 47.6 / 78.0 | 25.8 / 45.4 / 71.3 |
| `max_mid` | 51.8 | 41.8 / 54.4 / 66.8 | 41.5 / 54.3 / 67.8 | 35.5 / 69.4 / 111.7 | 33.1 / 73.3 / 120.6 | 34.7 / 69.3 / 110.3 |
| `median_high` | 78.3 | 58.5 / 82.8 / 107.1 | 57.5 / 82.7 / 106.8 | 42.6 / 91.6 / 154.7 | **I1 failed** (below) | 41.5 / 91.9 / 154.8 |

**M1 (net fiscal effect, % of GDP), long horizon, schedule S: P10 / mean / P90.**

| Point | alone, off | alone, `indep` | alone, `hist` | market paths, off | market paths, `indep` | market paths, `hist` |
|---|---|---|---|---|---|---|
| `min_mid` | -0.97 | -1.52 / -1.08 / -0.26 | -1.61 / -1.09 / -0.31 | -4.89 / -3.16 / -1.07 | -4.84 / -3.13 / -0.89 | -4.78 / -3.12 / -1.04 |
| `median_low` | -1.44 | -4.89 / -2.11 / -0.86 | -4.79 / -2.06 / -0.88 | -5.18 / -2.82 / -0.98 | -5.13 / -2.92 / -0.92 | -5.08 / -2.79 / -0.83 |
| `median_mid` | -0.28 | -3.07 / -0.69 / 0.52 | -3.15 / -0.67 / 0.46 | -4.59 / -2.61 / -0.32 | -4.62 / -2.36 / -0.02 | -4.47 / -2.50 / -0.33 |
| `max_mid` | 0.50 | -0.85 / 1.10 / 2.80 | -0.60 / 1.11 / 2.59 | -2.89 / 2.06 / 8.44 | -3.06 / 2.57 / 11.77 | -2.78 / 1.94 / 9.33 |
| `median_high` | 1.91 | 0.25 / 2.38 / 4.46 | 0.64 / 2.43 / 4.30 | -2.96 / 0.90 / 4.77 | **I1 failed** | -2.87 / 1.04 / 5.79 |

Reading, without a verdict:
- A GDP path alone puts P10 and P90 of P6 at year 50 about 20 to 30% below and above the mean (for example `median_mid` 26.9 to 49.2 around 37.9), and the means sit within 1 to 5 points of the fixed-growth values (the fund is nonlinear in GDP, so a mean need not equal the point value). The spread grows with the horizon (`median_high` `indep`, year 100: 122.0 to 251.5). The 0 and 0.37 correlations give nearly the same spread when the household's classes do not take the market return.
- With market paths the spread is already wide, and GDP risk widens it a little under `indep` (`max_mid` year 50: 33.1 to 120.6, against 35.5 to 111.7 with no GDP path); `hist` gives a narrower spread than `indep` at the top points (34.7 to 110.3).
- **M15a/b.** With no market paths and no GDP path the envelope never binds (0 nonzero cells). A GDP path alone makes it bind in a small corner: 2 of the 20 cells at `min_mid` only (long horizon; mean 0.25% and 0.10% under `indep`, 0.75% and 0.30% under `hist`; P10 and P90 are 0, so a minority of paths), none at the other four points. Market paths make it bind widely whether or not the GDP path is on (80 of 100 cells nonzero with no GDP path, 66 of 80 under `indep`, whose fifth point failed; at `min_mid`, long horizon, mean about 10 to 31%, P90 90 to 100%), so GDP risk adds little to it.

**Checks (account residual max / ledger tie, per point; shortfall lines are the 127c floor alarm, unchanged).** Alone (off, `indep`, `hist`; 15 runs): all hold I1 and the account identity (1.5e-11 to 1.2e-8), with a worst tie of 1.3e-8 at `median_high` `indep` (1.4e-12 off the GDP path; 4.7e-10 under `hist`). Market paths (15 runs): all but one hold I1; the residuals and ties are in `checks_paths*.csv`.

**Where the criteria are not met (reported, not tuned away).**
1. **`median_high`, market paths, `indep`: I1 fails** ("a book's family value is not the class total"): path 89 of the first chunk, line 7, year 95, family value 0.0016 against class total 0.0017, on a line whose non-pension wealth is nearly drained (net financial 0.0017 against a pension of 5.6). It is the family of the 124c and 128c alarms (a line with its non-pension classes exhausted) that those notes left undiagnosed; with the GDP path off and the same market paths the run holds I1 (account residual 2.9e-9, already loose), so the GDP path moves a path onto it. The run has no grid rows.
2. **`min_mid`, market paths, `indep`: account residual 3.5e-4** (0.00035; most other runs are at 2.6e-11 or below) and ledger tie 8.4e-9 on the first chunk. It arises in one core run only, the `ratio 0.25` sensitivity rerun (full receipts), at year 99 on one line that carries a lien (PL 0.0024) with negative net financial wealth. It is a real residual that scales with the GDP deviation: with the same core run and market paths, the worst residual over all lines and years is 2.1e-11 with no GDP path, 2.4e-11 with the deviation at 1% of its SD, and 3.5e-4 at full SD. The main run and the other four reruns hold (2e-11). Not root-caused here; no rule or tolerance was changed.
3. The alone `median_high` ties (1.3e-8 `indep`, 4.7e-10 `hist`) and account residuals (1.1e-8, 1.2e-8) are about 1e-11 of the receipts, above the 1e-9 flag the grid prints; reported as printed.

## Needs the author

- Two things outside the brief's Touches: `model_v3/core/revenue.py` line 146 (one line, byte equal when `mu` is None) and the refund routing in `_pay`. By the auto-merge rule this branch is **not merged: NEEDS THE AUTHOR**.
- Two I1 alarms (above), `unpaid_B` counts, and the OW1 finding.
- Per-path GDP growth stays out by decision, so GDP-only cells stay flat.

## Next

- A brief to reconcile the class floor with the family value (the I1 alarms at both points, 124c and 128c).
- Apply `withheld()` in the grid writer, or confirm OW1 is read as invalid.
- Out of scope here: heterogeneity, a saving gradient, pension withdrawal, per-path GDP, validation, OT1 and OF1.
