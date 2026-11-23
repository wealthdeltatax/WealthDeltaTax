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
- **Done:** block 0; block 1 (F1 under the household arm: script `docs/model-v3/f1-household/f1_household.py`, tables `f1_safe_tables.md`, CSVs; 5 scenario points x 27 schedule points, 200 paths, seed 20261118; 12 of 135 cells did not run: the arm's own I1 alarm, 128c, recorded not worked around; no (point, tol, m) cell feasible, best F1 67.5%)
- **Done (cont.):** block 2 (CK1: `f1_household.py ck1`, `ck1_safe_tables.md`, `ck1_safe.csv`; 5 scenario points x 4 schedules x 10 amplitudes, none failed; P3 is positive at A 0 in all 20 rows, so P3 is zero up to no amplitude; zero P3 appears only at isolated larger amplitudes in 12 of 20 rows)
- **Done (cont.):** block 3 for the `safe` case: note `docs/model-v3/f1-household.md`, change report below. Second full runs of `f1` and `ck1` byte-identical.
- **Next:** rerun blocks 1 and 2 with `--fund market` once 138c is merged (the script stops with a message for it now; 138c waits on 137c and 135c), add the `market` tables to the note, then merge by the auto-merge rule
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/140-f1-household origin/brief/140-f1-household`
- **State:** `safe` case complete and pushed; `market` case waiting on 138c; not merged
<!-- progress:end -->

### Change report
- Task: 140c, F1 and CK1 under the household arm (diagnostic only), `safe` fund case.
- Files changed: `docs/model-v3/f1-household/` (`f1_household.py`; `checks.md`; `f1_safe_tables.md`, `f1_safe_grid.csv`, `f1_safe_summary.csv`, `f1_safe_failed.csv`, `f1_safe_constant_path.csv`; `ck1_safe_tables.md`, `ck1_safe.csv`); `docs/model-v3/f1-household.md` (the note); this brief's notes; `docs/brief-suggestions.md` and `docs/agents/friction-log.md` (one entry each).
- What is different now: the household arm's F1 and CK1 are measured at five labelled scenario points. No (point, tol, m) cell is feasible (0 of 60; best F1 67.5% against 75%); CK1 P3 is positive at A 0 in all 20 rows. The failure is structural in 083c's sense (a constant path fails, first shortfall year 13) but with a different mechanism: a five-year settlement cycle, not decay.
- New or changed interfaces: `python -I docs/model-v3/f1-household/f1_household.py check|f1|ck1 [--fund safe] [--seed] [--n] [--points] [--out]`. Nothing in `model_v3/` changed.
- Acceptance criteria: (1) reproducible from a command, second run identical (`cmp` on all `f1` and `ck1` outputs), 124c fund path reproduced at the common point to 12 digits: met. 128c paths: short horizon equal, M1 long differs 0.1% because 132c and 133c came after the stored file: stated, F1 and CK1 do not read it. (2) tables at `safe`: met; `market`: not run, 138c not merged (criterion is conditional on it). (3) result without a recommendation: met.
- Deviations from the brief: 12 of 135 cells (`min_mid` 2, `max_mid` 2, `median_high` 8) raised the arm's I1 alarm and are recorded, not worked around. 200 paths (as the brief says), five scenario points times 27 schedule points. CK1 uses four schedules and ten amplitudes (0 to 12).
- Risks / follow-ups: `market` rerun after 138c (needs 137c, 135c first). Brief suggestion logged: the five-year cycle. The feasibility rule needs the author's ruling.
- Instruction friction: one entry in `docs/agents/friction-log.md` (no rule for an I1 alarm in the cell loop).
- Verification: `check` run; `f1` and `ck1` each run twice, byte-identical; script asserts equal the runner's headlines at schedule points 1, 14, 27 and margin 0 equals `revenue.retire`. Not run: `--fund market`; the Action (docs only, no site files touched).
- Overview sections likely needing an update: none now; after the `market` rerun, section 6 (model v3 diagnostics).
- Commit / branch: `brief/140-f1-household`. Not merged: the `market` case is outstanding, so the brief is not finished.
