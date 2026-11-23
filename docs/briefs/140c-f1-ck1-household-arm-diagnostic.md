# 140: Feasibility (F1) and the stress check (CK1) under the household arm: diagnostic only

- **Status:** ready (can start now on the current arm; rerun the fund `market` case after 138c)
- **Author/date:** K. Ogata with the guru, 2026-11-23
- **Depends on:** 083c (archived), 126c (merged); the `market` fund case needs 138c
- **Read (block 0: the first two only):** (1) `docs/model-v3/f1-diagnostic/report.md` (the legacy diagnostic; the summary and "Which single change"); (2) `docs/agents/code.md`. Later: `docs/model-v3/f1-diagnostic/f1_gap.py` (the method to copy); `model_v3/runner/sweeps.py` (`feasibility`, `choose`, `stress`, `CLOSED`); `docs/model-v3/household-arm-outputs.md` (OF1 "not run here"); `docs/model-v3/household-vs-legacy.md` (the fund's return).

## Goal
083c measured F1 (share of paths whose short-window P3 is at most a tolerance) under the legacy 3.5% rule: best 50.6% against 75%, structural. The household arm has a different fund (22 to 78% of GDP, safe stand-in; much larger if the fund earns the market return). Measure F1 and the CK1 stress check under the household arm so the author can rule on the feasibility rule with numbers from the arm the first run uses. Diagnosis only: no rule recommended, no model change.

## Decisions (author, 2026-11-23)
- Diagnose first, then the author rules; OF1 and CK1 stay pending (a labelled marker in the first run) until then.
- Every number is a scenario value at a labelled grid point and fund setting, never a forecast; no central value.

## Blocks (one push each; `docs/agents/code.md`)
- **Block 0:** progress block pushed.
- **Block 1: F1 under the household arm.** A script in `docs/model-v3/f1-household/` copying 083c's method: the 27 schedule points (or the 5 scenario points times the schedule grid, state which), tolerances and retirement margins as 083c, on per-path market returns (128c) at 200 paths; the fund `safe` now. Table as in 083c: F1 by (tol, m), best F1, feasible points, with M2 and M4a. Say whether the failure is structural (as in 083c) or not, and why. Push.
- **Block 2: CK1.** The fixed sinusoidal stress path (mu 4.74, the I-D1a central) at amplitudes A1 to A12 under the household arm: P1, P3, P7b over the short window and over transition plus short. Push.
- **Block 3: the market fund case and note.** Once 138c is merged, repeat blocks 1 and 2 with the fund at the market return (if 138c is not merged, say so and stop). `docs/model-v3/f1-household.md`: what each arm assumes, the tables, where the household arm differs from 083c and why. **No recommendation.** Change report; push; stop.
**Stop rule.** No model, register or manifest change. After three blocks or a quarter of the budget left, push and list the rest. Suites in the background, never piped.

## Touches
New: `docs/model-v3/f1-household/` (script and CSVs), `docs/model-v3/f1-household.md`. Read-only imports of `model_v3`. Not `runner/`, `core/`, the register, the pack or the manifest.

## Acceptance criteria
- Reproducible from a command in the note; a second run is identical; the household points reproduce the 124c fund path at the common point (state the check).
- Tables as in 083c for the household arm at the `safe` setting, and the `market` setting if 138c is merged.
- The note states the feasibility result without a recommendation.

## Out of scope
Choosing a rule, changing `CLOSED` or levers, the OF1 and CK1 outputs themselves (089c), any headline number.

## Implementation notes
<!-- progress:start -->
- **Done:** none
- **Next:** block 0
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/140-f1-household origin/brief/140-f1-household`
- **State:** ready; not started
<!-- progress:end -->
