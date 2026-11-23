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
- **Done:** block 0; block 1 (`docs/model-v3/death-phases/death_phases.py years`, `years_safe_tables.md`, CSVs; 6-phase rows equal 140c on 20 values; 36 s for four counts x four rows). M1a amplitude over years 10-40 at `median_mid` tm70: 11.10 (6), 6.69 (10), 4.61 (15), 1.02 (30) phases; first shortfall year 13, 63, 9, 61; at `median_low` the shortfall stays at 30 phases (first year 22), so the cycle is not the only cause there
- **Done (cont.):** block 2 (`death_phases.py f1`: `f1_tables.md`, `f1_phases_N/`; run times 81 s, 179 s, 339 s for 6, 15, 30 phases; rebased onto main f917908 first). Best F1 at (tol 0, m 0): 9.0, 12.5, 25.5; at (1, 25%): 65.5, 63.5, 75.0 (one feasible cell at 30 phases); constant-path first shortfall (tm50, tm70, tm90): 13/13/13, 33/9/9, 61/61/61; I1 alarm cells 1, 3, 5 of 27. 6-phase cells equal 140c's (312 of 312) except that tm90_k2_r025 no longer runs. Block 3 legacy table also generated (`years_legacy_*`).
- **Done (cont.):** block 3: note `docs/model-v3/death-phases.md`; second runs of `years`, `legacy`, `f1` identical (only wall-clock times differ).
- **Next:** none; stop.
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/149-death-phases origin/brief/149-death-phases`
- **State:** done, branch pushed, not merged (see change report)
<!-- progress:end -->

## Change report
- **Files:** new `docs/model-v3/death-phases.md` (note), `docs/model-v3/death-phases/` (`death_phases.py`, checks, tables, CSVs, `f1_phases_6/15/30/`). No model, register or manifest file changed; the phase count is overridden at run time only.
- **Answer:** the five-year cycle in M1a depends on the count (period 30/n years, amplitude roughly 1/n up to 15 phases; 11.10, 6.69, 4.61, 1.02 at 6, 10, 15, 30 at `median_mid` tm70). At 30 phases the short-window failure on a constant path disappears at `median_mid`, but F1 stays low (best 25.5% at tol 0, m 0; one feasible cell at the threshold, tol 1, m 25%), relief still decays below M1d later, and `median_low` still fails in year 22. The 15-phase case over-retires on the lump. Legacy arm: year-13 first shortfall moves to 32 or 33 at 30 phases. No rule or count recommended.
- **Checks:** 6-phase rows equal 140c (20 constant-path values; 312 of 312 shared F1 cells) and legacy equals 083c. Second runs identical.
- **Deviation:** `tm90_k2_r025` ran in 140c and now raises I1 at 6 phases (arm changed since 140c's base; not traced). The brief did not say what to do with I1 cells; recorded per cell, left out.
- **Merge:** all acceptance criteria met. Left for the author: whether to auto-merge was not tested against 140c's unmerged branch; the diff stays in `Touches`.
