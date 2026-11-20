# 083: F1 closure diagnostic (why no schedule closes, and what would)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-20
- **Depends on:** 055c (built on branch `brief/055-runner`, tip `1a60781`, not merged). Branch from that tip if `main` does not yet hold `model_v3/runner/`.
- **Read:** `docs/briefs/055c-v3-10-range-runner.md` (progress block, gotchas 1 and 2); `docs/model-v3/metrics.md` rows P3, F1, CK1 and the range-design paragraph; `model_v3/core/revenue.py` `retire` and `revenue` (lines 20 to 30 and 174 to 215); `model_v3/runner/runner.py` `evaluate`; `model_v3/runner/sweeps.py` `feasibility`, `choose`, `CLOSED`.

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
None. Ask if the 055c branch cannot be fetched or its tip is no longer `1a60781`.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
