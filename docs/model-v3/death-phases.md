# Death-phase count and the F1 failure (brief 149c)

Diagnosis only. No model, register or manifest file changed, and this note recommends neither a feasibility rule nor a phase count; the author rules on both. Every number is a scenario value at a labelled grid point (household arm, `safe` fund: the net financial class return, a stand-in with no register row), or the legacy arm at central inputs, never a forecast. Run on `main` at `f917908` (135c merged).

## What the phase count is

`revenue.run_lines` and `burden.line_flows` run each line in `n_phase` death phases: phase i has its first death at year ceil(i G / n_phase), G = 30, then every G years, each with weight 1/n_phase. It is a numerical approximation of a smooth age-at-death distribution, so the cycle in M1a has period G / n_phase: every 5 years at 6 phases, 3 at 10, 2 at 15, none at 30 (one phase in each year, the finest the integer years allow; a count above 30 would repeat years, which I did not test). `runner.core_run` does not pass `n_phase`, so `death_phases.py` wraps the two module functions for the length of a run (`phases(n)`); no model file is edited.

## Reproduce

From the repository root, `python -I`:
- `death_phases.py check`: the 6-phase and legacy rows against 140c and 083c (`checks.md`, 10 s).
- `death_phases.py years` (block 1, `years_safe*.csv`, `years_safe_tables.md`, 36 s) and `legacy` (`years_legacy*.csv`, 20 s).
- `death_phases.py f1` (block 2, `f1_tables.md`, `f1_phases_N/`, about 10 min), then `death_phases.py checkf1` (`checks_f1.md`).

All under `docs/model-v3/death-phases/`. Seed 20261118, 200 paths, `median_mid`. A second run of each printed byte-identical text and CSVs (checked with `cmp`), except the wall-clock run times in `f1_tables.md` (second run 77, 185 and 345 s against 81, 179 and 339 s).

**Reproduction.** At 6 phases the constant-path rows equal 140c's (`f1_safe_constant_path.csv`): fill year, end of short window, first shortfall year, P3 to the end of the short window and P3 over 100 years, 20 values at two points and two schedules. The legacy 6-phase rows equal 083c's report (fill year 6, first shortfall 13, P3 81.45 and 83.74, P3 short 2.79 and 2.66). The 6-phase F1 grid equals 140c's in all 312 shared cells (F1, M2, M4a, taxes retired). One schedule point, `tm90_k2_r025`, ran in 140c and now raises the arm's I1 alarm; `arm.py` changed after 140c's base (137c, 135c), and I did not trace it.

## Block 1: the cycle depends on the count

Constant 4.74% path, `median_mid`, tm70_k1_r050 (percent of GDP; amplitude is max minus min over years 10 to 40; full year-by-year tables for both points and both schedules in `years_safe_tables.md`):

| phases | cycle period | M1a amplitude | relief amplitude | M1a mean | relief mean | first year relief < M1d | years below M1d in 10 to 40 |
|---|---|---|---|---|---|---|---|
| 6 | 5 years | 11.10 | 3.92 | 3.06 | 5.65 | 13 | 12 |
| 10 | 3 | 6.69 | 1.03 | 2.73 | 5.57 | 63 | 0 |
| 15 | 2 | 4.61 | 2.20 | 2.85 | 5.57 | 9 | 31 |
| 30 | none | 1.02 | 1.02 | 2.78 | 5.54 | 61 | 0 |

- M1a's amplitude falls roughly as 1 / n up to 15 phases; at 30 phases the lumps are gone (M1a runs 3.23 to 2.21 over years 10 to 40, decaying).
- The means barely move (M1a mean 2.73 to 3.06, relief mean 5.54 to 5.65): the total received is stable, the timing is what the count sets.
- The first shortfall year is not monotone in the count: 13, 63, 9, 61 for tm70 and 13, 63, 33, 61 for tm50. At 15 phases and tm70 (and tm90) six taxes are retired by year 100 instead of five and M1d at year 40 is 8.11 against 4.74 (P3 to the end of the short window 19.72, over 100 years 295). My reading, from the series and not tested: the lumpy relief makes the retirement rule retire one tax too many at the lump; I did not vary the rule.
- `median_low` (the same table is in the summary CSV) shows the cycle is not the only cause. At 30 phases the cycle is gone (M1a amplitude 1.06), yet relief runs 3.79 to 5.26 over years 10 to 40 (decaying) and first falls below M1d in year 22 (tm70) and 18 (tm50); at 6 phases it is year 13 at both points.

## Block 2: F1 by phase count (`median_mid`, 27 schedule points, 200 paths)

Best F1 over the schedule points that ran at each count (26 at 6 phases, 24 at 15, 22 at 30; percent of paths; the full tables with M2 and M4a are in `f1_tables.md`):

| tol | m | 6 phases | 15 phases | 30 phases |
|---|---|---|---|---|
| 0 | 0% | 9.0 | 12.5 | 25.5 |
| 0 | 25% | 35.5 | 42.0 | 56.5 |
| 0.25 | 25% | 46.5 | 50.0 | 62.0 |
| 1 | 0% | 25.0 | 32.0 | 45.0 |
| 1 | 10% | 45.0 | 51.5 | 61.5 |
| 1 | 25% | 65.5 | 63.5 | 75.0 |

- Feasible cells (F1 at least 75%, M2 short at most 2.0, M4a short at least 0): 0 of 26 at 6 phases, 0 of 24 at 15; 1 of 22 at 30 (tm50_k05_r100, tol 1, m 25%, F1 exactly 75.0). On 200 paths the standard error of a share near 75% is 3.1 points, so that cell is not distinguishable from 72 to 78%.
- F1 at the 055c rule (tol 0, m 0) over all schedule points that ran: 1.5 to 9.0 (6 phases), 3.0 to 12.5 (15), 11.0 to 25.5 (30).
- Constant path, first shortfall (tm50, tm70, tm90): 13, 13, 13 at 6 phases; 33, 9, 9 at 15; 61, 61, 61 at 30. P3 to the end of the short window is positive at 6 phases (1.71 to 2.03 over the three schedules), at 15 phases for tm70 and tm90 (19.72, 16.87), and zero at 30 phases.
- Cells that raised I1 (not worked around, left out): 1 at 6 phases, 3 at 15, 5 at 30 (`f1_phases_N/f1_safe_failed.csv`). The sets of points that ran differ by count; restricted to the 22 schedule points that ran at all three counts, the best F1 values in the table above are the same.
- Cost: one 27-point `f1` run takes 81 s at 6 phases, 179 s at 15 and 339 s at 30 (about 2.2 and 4.2 times); memory was not measured.

## Block 3: the legacy arm

Same table for the legacy arm (083c: consumption share I-D14c, the fund earns the market return), central inputs, constant path (`years_legacy_tables.md`):

| phases | schedule | M1a amplitude | relief amplitude | first year relief < M1d | P3 to end of short window | P3 100 y |
|---|---|---|---|---|---|---|
| 6 | tm70 | 12.87 | 4.57 | 13 | 2.66 | 83.7 |
| 10 | tm70 | 7.70 | 1.54 | 33 | 0.00 | 64.7 |
| 15 | tm70 | 5.38 | 2.79 | 21 | 0.00 | 67.3 |
| 30 | tm70 | 1.53 | 1.53 | 33 | 0.00 | 65.6 |
| 6 | tm50 | 10.98 | 3.87 | 13 | 2.79 | 81.4 |
| 30 | tm50 | 1.09 | 1.09 | 32 | 0.00 | 62.7 |

083c's year-13 first shortfall shares the cause: it is year 13 only at 6 phases (tm50 also 13 at 15), and moves to year 32 or 33 at 30 phases. What remains at 30 phases is the slow decay 083c described: relief 5.93 in year 10 to 4.40 in year 40 against M1d 4.74 (M1a 3.16 to 1.63).

## What changes and what does not

Changes with the count: the period and amplitude of the lumps in M1a and in relief; the first shortfall year on a constant path (13 to 33 or later at 10 and 30 phases, but 9 at 15 for two schedules); P3 in the short window (positive at 6, zero at 30); F1 (best 9 to 25% at the 055c rule) and the feasible-cell count (0, 0, 1); run time (about 4 times at 30 phases).

Does not change: the totals (means of M1a and relief over years 10 to 40, within about 10%); a slow decay of relief below M1d later (year 61 at `median_mid`, 22 and 18 at `median_low`, 32 and 33 in the legacy arm); the failure of F1 at most cells even at 30 phases (best 25.5% at tol 0, m 0; none above 75% except one cell at the threshold); the I1 alarm cells, which grow with the count.

Convergence: 10 and 30 phases agree on the constant-path result at `median_mid` (no shortfall in the short window, first shortfall year 61 to 63); 15 phases does not, because of the retirement on the lump; 6 phases is far from both. The count is therefore not settled by the count itself in this study; 30 is the finest resolution the annual model has. F1 was run at 6, 15 and 30 only, not at 10.

## Not done

No rule or count is recommended; the `market` fund case waits on 138c (140c); 1,000-path and level 2 versions, OF1 and CK1 (089c), and any other scenario point than `median_mid` (F1) and `median_mid` and `median_low` (years) were not run; the retirement rule and the fund's payout window were not varied.
