# 083: F1 closure diagnostic (why no schedule closes, and what would)

- **Status:** retired 2026-11-20 (report `docs/model-v3/f1-diagnostic/report.md`)
- **Author/date:** K. Ogata with the guru, 2026-11-20
- **Depends on:** 055c (merged to `main`, `e4993a4`).
- **Read:** `docs/archive/briefs/055c-v3-10-range-runner.md` (progress block, gotchas 1 and 2); `docs/model-v3/metrics.md` rows P3, F1, CK1 and the range-design paragraph; `model_v3/core/revenue.py` `retire` and `revenue` (lines 20 to 30 and 174 to 215); `model_v3/runner/runner.py` `evaluate`; `model_v3/runner/sweeps.py` `feasibility`, `choose`, `CLOSED`.

## Goal
Say where the closure share F1 comes from and which single change would move it, with numbers, so the author can rule on the feasibility rule. This is a measurement, not a model change.

## Decisions (author, 2026-11-20)
- Option 1 of the 055c review: measure first. No change to the metric definitions, the retirement rule or the A5 constants (closure share 75% of paths, M2 cap 2.0% a year, M4a floor 0%) in this brief. The author rules after reading the report.

## Design
The 055c finding: at central inputs and 1,000 common paths, short-window F1 is 4.0 to 11.2% at all 27 grid points (needed 75%). On a constant 4.74% return path at tau_m 0.7, k 0.5, ratio 0.5, relief after the fill is 5.7% of GDP and falls to 2.9% by year 100, while the retired receipts stay at 4.74% (the first five taxes by ascending receipts), so P3 is 100.9 at CK1 amplitude 0. `CLOSED` is 1e-9, so any dip counts as not closed.

Write `docs/model-v3/f1-diagnostic/f1_gap.py` (not under `model_v3/`: its layer and budget rules do not apply to a one-off script) and its report `docs/model-v3/f1-diagnostic/report.md`. The script imports the runner and core; it does not edit them. To read relief, M1d and the retirement years per path, copy the first half of `runner.evaluate` (up to the `rv.revenue` call) into the script; do not change `evaluate`.

Measure on the 27 grid points at central inputs, 1,000 level 1 paths from `rt.streams(seed)['level1_paths']`, seed 20261118, short window as in 055c:

1. **Size of the failure.** Per point: share of paths with P3 exactly zero; P10, median, P90 and maximum of short-window P3 (GDP-points summed over years); share of failing paths whose first shortfall year is within 3 years of a retirement; the number of taxes retired by the end of the window (mean).
2. **Tolerance.** F1 recomputed with "closed" meaning short-window P3 at most `tol` for `tol` in {0, 0.05, 0.25, 1.0} GDP-points summed over years.
3. **Retirement margin.** A tax is retired when relief, net of retired receipts, covers its receipts times (1 + m), for m in {0, 10%, 25%}. Without editing `revenue.retire`: pass `relief / (1 + m)` to `retire` to get the retirement years and `M1d`, then compute the excess against the true relief. Report F1, M4a (short, overall) and the mean number of taxes retired by the end of the window for each m, and F1 for the tolerance grid at each m.
4. **Constant path.** For the three schedules (tau_m 0.5, 0.7, 0.9, k 1, ratio 0.5) on the constant central-return path: relief, M1d and their difference at years 5, 10, 20, 30, 50, 100, and the year relief first falls below M1d.
5. **CK1 window.** CK1's P3 for A in the grid, as 055c reports it (whole 100 years) and over transition plus short only.
6. **Chosen point.** For each (tol, m) pair, the number of grid points that pass all three feasibility conditions (F1 at least 75, M2 at most 2.0, M4a at least 0), and the highest F1 among those that pass the M2 cap and M4a floor.

The report starts with a table of (tol, m) against best F1 and feasible-point count, then one paragraph of reading, and states plainly which single change, if any, reaches 75% and what it costs in M4a and the number of taxes retired. It recommends nothing about the rule: the guru and the author do.

**Early check.** If an item cannot be computed from what `evaluate` leaves available, stop and report the missing quantity; do not edit `core/` or `runner/`. If every cell of the (tol, m) table is under 25% F1, say so in the first line of the report: that means the 75% target needs a different mechanism, not a different tolerance.

## Touches
`docs/model-v3/f1-diagnostic/f1_gap.py`, `docs/model-v3/f1-diagnostic/report.md`, this brief's progress block, `docs/agents/friction-log.md`.

## Acceptance criteria
- The report holds the six items above with numbers; every number reruns from the script with the seed in the report (a second run prints identical figures).
- Item 1 at (tol 0, m 0) reproduces 055c's F1 of 4.0 to 11.2% over the 27 points, or the report says by how much it differs and why.
- `python -I -m pytest tests/model_v3 -q` still passes (no file under `model_v3/` or `tests/` changed).
- `git diff --stat` is limited to Touches.

## Checks to run
The script run; `pytest tests/model_v3 -q` to show nothing moved.

## Out of scope
Any change to `retire`, `evaluate`, `choose`, `CLOSED`, the manifest, A5 or CK1; the full N1 and N2 sizes; level 2.

## Open questions
None. None.

## Implementation notes
<!-- progress:start -->
- **Done:** `docs/model-v3/f1-diagnostic/f1_gap.py` (items 1 to 6, plus a labelled scan of margins 50% and 100% beyond the grid) and `report.md`. Two runs of the script (seed 20261118, 1,000 paths, about 1.5 minutes) print identical text. `pytest tests/model_v3 -q`: 208 passed on the tree rebased on 084c (201 before the rebase); no file under `model_v3/` or `tests/` changed.
- **Next:** the guru and the author read `report.md` and rule on the feasibility rule.
- **Decisions:** (1) The context is built as `tests/model_v3/test_runner.py` does (tier 1 list from `outputs.yml` OT1, the manifest ids). After 084c merged during the work (`runner.core_run`, `payer_taxes` in `levers.json`), the script calls `core_run` instead of its own copy of evaluate's first half; the tables did not change (cmp on the output). (2) The margin follows the brief (`relief / (1 + m)` to `retire`), so it applies to the cumulative retired receipts; the excess is against true relief. (3) CK1 is shown for the three item-4 schedules and tm70_k05_r050 (055c's), with mu 4.42 and 4.74. (4) Margins 50% and 100% added in their own table, outside the grid, because no cell of the brief's grid reaches 75%.
- **Gotchas:** (1) Keeping every point's line flows in memory gets the run killed at about point 21 of 27; the script keeps only small arrays per point. (2) Item 1 gives F1 4.3 to 11.5% against 055c's 4.0 to 11.2%: a different 1,000-path sample (other draws give lows 3.6 to 4.7, highs 11.3 to 13.4), not a model difference; the script's P3, M2, M4a and fill years equal `runner.headlines` on points 1, 14 and 27 (asserted).
- **Resume:** none; finished.
- **Not run:** level 2, the full N1 size, any change to `retire`, `evaluate`, `choose`, `CLOSED`, A5 or CK1 (out of scope).
- **State:** done; result: no cell of the brief's grid reaches 75% (best 50.6% at tol 1.0, m 25%); a margin of 100% with tol 1.0 reaches 79.3% (M4a short 5.6, 3.61 taxes retired)
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 083c, F1 closure diagnostic
- Files changed: docs/model-v3/f1-diagnostic/f1_gap.py (new, one-off measurement script); docs/model-v3/f1-diagnostic/report.md (new, the report); this brief's progress block; docs/agents/friction-log.md (one entry)
- What is different now: the author has the numbers behind the empty feasible region: F1 by tolerance and retirement margin on the 27 grid points, the constant-path decay of relief, CK1 in two windows, and the chosen point for each (tol, m).
- New or changed interfaces: none (the script is run by hand; nothing under model_v3/ or tests/ changed)
- Acceptance criteria: report holds the six items with numbers (met); a second run prints identical text (met, cmp on two runs); item 1 at (tol 0, m 0) gives F1 4.3 to 11.5% against 055c's 4.0 to 11.2% (differs by 0.3 points at both ends: another 1,000-path sample, see gotcha 2); pytest tests/model_v3 -q 208 passed after rebasing on 084c (met); git diff --stat limited to Touches (met).
- Deviations from the brief: margins 50% and 100% added in a separate, labelled table (the brief's grid does not reach 75%); CK1 also shown for mu 4.74 and for the 055c schedule.
- Risks / follow-ups: the author rules on the feasibility rule after reading report.md. Only a 100% margin with tol 1.0 reaches 75% in this measurement; nothing is recommended.
- Instruction friction: one entry added to docs/agents/friction-log.md (how to build the runner context).
- Verification: the script run twice (identical output); script's numbers asserted equal to runner.headlines on grid points 1, 14 and 27; script rerun after rebasing on 084c with identical output; pytest tests/model_v3 -q: 208 passed (rebased on 084c).
- Overview sections likely needing an update: model v3 status (feasible region: no point at 75%, see f1-diagnostic/report.md)
- Commit / branch: brief/083-f1-diagnostic (see below)
```
