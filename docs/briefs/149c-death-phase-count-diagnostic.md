# 149: Death-phase count: does the five-year cycle in M1a cause the F1 failure? Diagnostic only

- **Status:** ready (read-only diagnostic; can start now)
- **Author/date:** K. Ogata with the guru, 2026-11-23
- **Depends on:** 140c (the `safe` case merged: `docs/model-v3/f1-household/f1_household.py`), 083c (archived)
- **Read (block 0: the first two only):** (1) `docs/model-v3/f1-household.md` (the section "Is the failure structural?" and its year table); (2) `docs/agents/code.md`. Later: `model_v3/core/revenue.py` (`run_lines`, the module docstring on `n_phase`) and `model_v3/core/burden.py` (`line_flows`, the `n_phase` argument and `ceil(i G / n_phase)`); `docs/model-v3/f1-household/f1_household.py`; `docs/model-v3/f1-diagnostic/report.md` (the legacy 083c).

## Goal
140c found that no schedule is feasible even on a constant 4.74% path, and traced it to timing, not volatility: with six death phases and a 30-year generation (`G`), one sixth of the base settles at death every fifth year, so M1a is about 1% of GDP in four years and 11 to 12% in the fifth, the fund pays the lump out over about two years and then has nothing, and relief falls below the retired taxes (M1d) in two years of five. The six phases are an approximation of a smooth age-at-death distribution. Test whether the phase count causes the failure, before the author rules on the feasibility rule. Diagnosis only.

## Decisions (author, 2026-11-23)
- Diagnose first; the author rules on the feasibility rule afterwards, and on whether the phase count changes. No model change, no register row, no recommendation in this brief.
- The `n_phase` argument is already a parameter of `line_flows` and `run_lines`: use it. If a run cannot pass it without editing `model_v3/`, copy the call in the diagnostic script; do not edit the model (stop-and-report).
- The phase count is a numerical approximation, not a scenario: report its effect as a convergence study (does the answer settle as the count grows), not as a range across scenarios.

## Blocks (one push each; `docs/agents/code.md`)
- **Block 0:** progress block pushed.
- **Block 1: year-by-year on a constant path.** At `median_mid` and `median_low` (household arm, `safe` fund, constant 4.74% path), schedule tm70_k1_r050 (and tm50_k1_r050): M1a, M1b, M1c, relief and M1d in years 1 to 40 with 6, 10, 15 and 30 phases. Table and CSV; say where the five-year cycle appears and disappears, and how the amplitude (max minus min of M1a over years 10 to 40) changes with the count. Push.
- **Block 2: F1 and the first shortfall.** Rerun `f1_household.py f1` at `median_mid` only (27 schedule points, 200 paths, seed 20261118) with 6, 15 and 30 phases (the cost scales with the count; state the run times first and cut to 6 and 15 if 30 is not feasible, saying so): best F1 by (tolerance, margin), number of feasible cells, first shortfall year on the constant path, the constant-path P3. Push.
- **Block 3: legacy and note.** The same block 1 table for the legacy arm (does 083c's year-13 first shortfall have the same cause?) and a note `docs/model-v3/death-phases.md`: what changes with the count, what does not, what it costs in run time. **No recommendation.** Change report; push; stop.
**Stop rule.** No model, register or manifest change. After three blocks or a quarter of the budget left, push and list the rest. Suites in the background, never piped.

## Touches
New: `docs/model-v3/death-phases/` (script and CSVs), `docs/model-v3/death-phases.md`. Read-only imports of `model_v3`. Not `runner/`, `core/`, the register, the pack or the manifest.

## Acceptance criteria
- Reproducible from commands in the note; a second run is identical; the 6-phase rows reproduce the 140c numbers at the common point (state the check).
- The note states whether the cycle depends on the phase count, with the table, and says what it does to F1 and the first shortfall year; it does not recommend a rule or a count.

## Out of scope
Choosing the feasibility rule, changing `n_phase`, the `market` fund case (140c after 138c), OF1 and CK1 (089c), any headline number.

## Implementation notes
<!-- progress:start -->
- **Done:** block 0 (branch and progress block pushed)
- **Next:** block 1 (year-by-year, constant path, 6/10/15/30 phases)
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/149-death-phases origin/brief/149-death-phases`
- **State:** in progress, block 0 done
<!-- progress:end -->
