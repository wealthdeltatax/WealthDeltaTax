# 057: Model v3 V3-12: run script, smoke test and acceptance wiring

- **Status:** in progress on branch `brief/057-run-script-acceptance` (blocks 0 to 2 and three rounds of rulings done; block 3 and `--final` wait for 138c and 139c; rebase on main first)
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** 055 (merged), 056; for a complete `--final` file also 084c to 088c and the ruling in 089c (a provisional smoke run may start after 084c)
- **Read:** `docs/model-v3/architecture.md` 6.4, 6.5 and 3.1; `docs/model-v3/acceptance.md` in full (sections 1, 2, 5); `pipeline/check_gate.py`; `docs/restructure/order.md` G1.

## Goal
One command, `bash tests/model_v3/accept.sh`, that exits 0 only when the model is accepted.

## Guru note, 2026-11-20
CK1's mu is I-D1a central, 4.74 (arithmetic), not 4.42 (the geometric I-D1a2); `metrics.md` was corrected. `run.py` passes it to `sweeps.stress` from the register, not as a typed number.

Also (guru, 2026-11-20): `run.py` passes `once` (the manifest's `once_not_per_schedule` ids) to `runner.context`, or any group `static` id raises (086c, 088c).

Also (guru, 2026-11-20): a band with no payer at launch (D4_5, wealth under w_min) gives nan in O2, O2d and OW3; `assemble` treats non-finite as an error in a final run, so 057c decides how the final file marks those cells (a stated null, not a number) before `--final`.

Also (guru, updated 2026-11-21): the author abandoned I-D14c's 3.5% as the central assumption (094r). The household step now exists (108c, not wired) with a `legacy` mode that reproduces the 3.5% rule; the planned wiring brief makes it a switchable arm. Until the new arm is wired and validated, the run uses the legacy arm, so `run.py` writes a run field (for example `legacy_consumption: 3.5`) and every report or page that prints a result from this run labels it a **legacy result, not a calibrated forecast**. Choose the field name with the A6 run fields. When the arm selector exists, the run field records the arm; this brief stays held until the wiring, validation and comparison briefs have run, and then also reads the arm.

## Author rulings, 2026-11-23
- The first official run uses the **household arm**. The run field records `arm: household`; each output is a **range across the labelled scenario-grid points** (reuse `docs/model-v3/household-arm-run/ranges.py`; read it first), never a central value; legacy is a labelled comparator run only (`legacy result, not a calibrated forecast`).
- Cells with no payer at launch (D4_5 under w_min: O2, O2d, OW3) are written as a **stated null marker** (`no_payer_at_launch`), not a number and not zero; `pipeline/validate_outputs.py` accepts the marker only for these cells; `assemble` treats it as covered, other non-finite values stay errors.
- OF1 and CK1 are a **labelled pending marker** in the first run until the author rules on the feasibility rule after the diagnostic (140c), then 089c.
- M15a/b and M9 X are **printed with a labelled caveat** in the first run (M15a/b: not binding in this scenario set; M9 X: not comparable across arms), not withheld or dropped.
- Register rows (139c) and the fund and floor fixes (137c, 138c) land before `--final`, because they change numbers and the gate hash.

## Blocks (added 2026-11-23; one push each)
- **Block 0:** progress block. **Block 1:** `run.py` (arm field, scenario-range assembly, null marker, pending marker for OF1 and CK1), validator change, tests. **Block 2:** `accept.sh`, `test_smoke.py` and the five seeded breakages. **Block 3:** `test_converge.py`, the `--final` refusal rules. Stop after block 2 if 137c, 135c, 138c or 139c are not merged; `--final` waits for them.

## Author rulings, 2026-11-23 (second round, after the 057c review)
- **OR1 and DH1c:** DH1c is a pack fact (one value per path): report a single value. OR1 (P7a, P7b) is a share over paths: the point is the share, the range is P10 to P90 across paths. Record the reading in the manifest notes (stage-A17 amendment, part of this brief).
- **Pack label:** map the pack code GBR to the manifest label UK in validator V8 by a stated mapping table; the run records both the pack code and the label.
- **Run scope:** the break-even return (O1e) is run at `median_mid` only; the other four points carry the outputs that need no root search, and the file marks O1e at those points with a stated marker (`not_run_this_point`), accepted by the validator for O1e only. The parallel evaluation and timing work is brief 150c.
- **Null cells, general rule (third round, 2026-11-23):** any cell of a group with no payer at launch under the schedule, and any output derived from that group (O2, O2b, O2c, O2d, OH1b, OH1c, OW3), is written `no_payer_at_launch`; the validator accepts the marker for those ids only and any other non-finite cell stays an error. This covers D6_7 as well as D4_5. OW1 under the household arm gets the `withheld (legacy_only)` marker, as already ruled (121c, 135c). O1e at the one point it runs is not marked: if it is still non-finite at the real tolerance, diagnose and report (a coarse smoke tolerance may be the cause). **Fourth-round ruling (2026-11-23):** it is non-finite at the real tolerance because the `safe` fund ignores the generator mean (M1 identical at every mean). Run O1e at `median_mid` with `fund_return=market`, labelled in the file; if still flat, report and use a stated marker. Under `safe`, O1e is the marker `not_defined_under_safe_fund` (validator accepts it for O1e only). 057c does not wait for 147c or 148c; it waits for the 139c wiring. The four unknown run fields (`seed`, `level2_draws`, `level2_paths`, `unfilled_paths`) are added to the manifest's `run_fields_added` and the validator's list (part of this brief); the 12 OP6 cells without a series are reported, not changed.
- **Feasibility collapse** (one household point passes, S_low, S_central and S_high coincide): not ruled here. 149c (death-phase count) and 089c follow; the first official run keeps OF1 and CK1 pending.

## Independence from Agent 6's chain (guru check, 2026-11-23)
057c does not edit `model_v3/runner/arm.py`, `model_v3/core/`, `docs/model-v3/household-arm-run/` (`run_grid.py`, `ranges.py`), the register or the manifest; those belong to 137c, 135c, 138c and 139c. If a block needs a change there, stop and report; do not edit.
- **Safe to build now (structure):** `run.py` with the arm field and the stated null and pending markers; the `validate_outputs.py` change; `accept.sh`; `test_smoke.py`; the five seeded breakages.
- **Depends on the chain (content):** (a) the scenario-range assembly reads the five grid points; today `min_mid` and `median_high` have no rows (I1 floor, 137c and 135c fix that) and the grid logic lives in `docs/model-v3/household-arm-run/` scripts, which 135c and 138c edit: write `run.py` against `runner.arm` and `runner` (not by importing the docs scripts), and keep the range rule (min to max, no central) in one small function in `model_v3/`; (b) M2 and M2d change under 138c (total-wealth denominator) and the fund switch arrives there; (c) 139c edits `registry/inputs.json` and the gate hash, so `check_gate.py` and `accept.sh` step 6 may fail until it merges; (d) `test_converge.py` and any `--final` file are meaningful only after all four.
- **Merge order:** Agent 6's briefs merge first when they land; Agent 2 rebases and re-runs `accept.sh` before each push. A smoke test that pins a number from the household arm is a defect: pin shapes and identities, not values, until 139c has merged.

## Decisions (author, 2026-11-18)
`architecture.md` approved (sections 8.1 and 9 as written); `acceptance.md` approved with Q1 to Q6 as proposed. v3 imports nothing from `model_v1/` or `model_v2/`. No file outside this brief's Touches is changed.

## Design
`model_v3/run.py` (120 lines): `python -m model_v3.run [--paths N] [--seed S] [--out DIR] [--smoke] [--final]`; `--final` is refused below the starting sizes or with any failing test; no environment variable is set. `test_smoke.py` (three tests: smoke passes; a renamed module copy fails it; a broken import fails it). `accept.sh` (30 lines): the seven steps of `acceptance.md` section 1. `test_converge.py` (C1 to C4 of section 5, marked `converge`). Check that `python pipeline/check_gate.py --all` reads the acceptance line.

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1.

This is build stage V3-12 of `architecture.md` section 7. One session, one lane; the stage ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. The stage's files are budgeted in `architecture.md` 6.1; a stage more than 15% over its budget reports it before the next starts.

## Touches
`model_v3/run.py`, `tests/model_v3/test_smoke.py`, `tests/model_v3/accept.sh`, `tests/model_v3/test_converge.py`, `docs/decisions.md` (a raised sample size is entered there), this brief's progress block.

## Acceptance criteria
- `bash tests/model_v3/accept.sh` exits 0 on the whole tree.
- It exits non-zero under each of five seeded breakages (a failing unit test, a changed seed, a missing manifest id, a `null` cell, a non-identical rerun).
- The convergence test passes, or the size in `run.py` is raised and the change entered in `docs/decisions.md`; a failure that doubling does not fix goes to the author.
- `run.py` at most 120 lines; the new test files within the budget lines of `architecture.md` 6.1.
- `git diff --stat` is limited to the Touches list.

## Checks to run
`bash tests/model_v3/accept.sh`; `python pipeline/check_gate.py --all` (G1 reads the acceptance line).

## Out of scope
A final run (the author's act, G2); the first provisional commit of `outputs.json`.

## Open questions
None; thresholds are fixed in `acceptance.md`.

## Implementation notes
<!-- progress:start -->
- **Done:** blocks 0 to 2 and rulings one to five (2026-11-23). `run.py` (120 lines): `--size smoke|quick|final`, `--o1e-draws`, `--workers`, `--point`; O1e at the first point only, under `fund_return=market` (labelled in `run.arm.o1e`), range cells `not_run_this_run` at 0 draws; validator accepts `not_run_this_run` (O1e lo/hi) and `not_defined_under_safe_fund` (O1e); `accept.sh` runs a `quick` pair. `quick` reference file produced (see report).
- **Next:** the author's rulings on the three findings in the report (3 of 5 grid points fail at the schedule chosen at `median_mid`; O1e still has no root at `quick` size; C3 of the convergence test costs days). Block 3 is unblocked by the merges (135c, 138c, 139c) but not started.
- **Decisions:** O1e centre slot keeps the central root (not `not_run_this_point`) now that O1e is a real single-point result under the market fund; `level2_draws` in the run block is the O1e draws actually run (0 at `quick` and `final`); `accept.sh` step 5 checks paths >= 1000 and level2_paths >= 50 because acceptance runs `quick`; an output not computed at a point is skipped by the range merge; a point whose own checks fail is reported in `run.arm.failed`, never repaired.
- **Gotchas:** `quick` takes 44 minutes serial; smoke is now 17 minutes (O1e under the market fund does real root-finding); one process only measured; collecting tests/data, tests/hooks and tests/model_v3 in one pytest call clashes on `conftest`.
- **Resume:** `git status`; fast: `python -I -m pytest tests/model_v3 -q --ignore=tests/model_v3/test_smoke.py -m "not converge"` (4.5 min); `test_smoke.py` 17 min.
- **Not run:** `accept.sh` end to end (step 2 needs `test_converge.py`; step 5 would fail on the O1e nulls); any `--final`; a full-size run.
- **State:** NEEDS THE AUTHOR
<!-- progress:end -->

**150c merged (2026-11-23):** add a `--workers` switch to `run.py` (serial default, 0 one per core) passing `workers=` to `feasibility`, `tornado` and `breakeven_return`; the exact diff is in the last section of `docs/model-v3/run-cost.md`. Serial and parallel results must stay byte-identical.

**Run sizes and O1e scale (author, 2026-11-23, fifth round):** (1) O1e's range over input draws becomes a switch, `--o1e-draws N`: the first official run uses N = 0 (the central root per schedule only: 3 roots, not 603), the file marks the range cells with the stated marker `not_run_this_run`, and N = 200 stays available for a later, larger run; nothing else in the output changes with N. (2) Three named run sizes, one switch `--size smoke|quick|final`: `smoke` as it is; `quick` (new) a fast reproducible run for development and for timing the speed-up work, five grid points, N1 about 1,000, n2p about 50, `--o1e-draws 0`, tolerance 1e-2, target well under an hour on one process (say in the change report what it measures); `final` the official size. `--size` sets defaults that the explicit flags (`--workers`, `--o1e-draws`, `--point`) override. (3) The change report gives the measured wall time of `quick` and of one grid point at `final` without O1e, as the baseline for the speed-up work; the `quick` output file is the byte-for-byte reference that any speed-up must reproduce. This stays inside the brief's session budget by replacing the second `accept.sh` full run with a `quick` pair; the full-size run is not part of acceptance.

Change report
- Task: brief 057c, V3-12 run script and acceptance (blocks 0 to 2; rulings one to five)
- Files changed: `model_v3/run.py` (new, 120 lines); `pipeline/validate_outputs.py` (markers `no_payer_at_launch` for the ruled ids, `no_central`, `not_run_this_point`, `not_run_this_run` and `not_defined_under_safe_fund` for O1e only; `pending` for OF1 and CK1; GBR to UK in V8; a withheld OW1 accepted under the household arm; four run fields in its list); `docs/model-v3/outputs.yml` (DH1c `point`; stage-A17 comments; `run_fields_added` gains `seed`, `level2_draws`, `level2_paths`, `unfilled_paths`); `tests/data/fixtures/outputs.fixture.json` and `tests/data/make_fixture.py` (forced by the manifest); `tests/model_v3/test_arm_switch.py` (one line: its run block carries the four new fields); `tests/model_v3/accept.sh` (new, 30 lines); `tests/model_v3/test_smoke.py` (new, 79 lines); `docs/agents/friction-log.md`; `docs/brief-suggestions.md`; this brief.
- What is different now: `python -I -c "import sys; sys.path.insert(0, '.'); from model_v3 import run; run.main(['--size', 'quick', '--out', DIR])"`; sizes smoke (50 paths, 20 tornado paths, 3 O1e draws, tolerance 1.0, 1 point), quick (1,000, 50, 0, 1e-2, 5 points), final (10,000, 1,000, 0, 1e-2, 5 points); `--paths`, `--o1e-draws`, `--point` (repeatable) and `--workers` override. O1e runs at the first point only under `fund_return=market`, recorded in `run.arm.o1e`; at 0 draws its lo and hi are `not_run_this_run`. `accept.sh` steps 3 and 6 are `--size quick`.
- Measured: `quick` 2,665 s (44 minutes, serial, this machine, 2 cores). One final-size grid point without O1e (level 1 at 10,000 paths on 3 schedules, tornado at 1,000 paths): 5,655 s (94 minutes, serial; 150c projected 79 minutes). The `quick` file (seed 20261118) is the byte reference for the speed-up work; it is not committed (it is regenerated by the command above).
- Acceptance criteria: seeded breakages MET (changed seed, missing id, null cell, non-identical rerun each exit 1; failing unit test exits 1 through the full script); renamed-module and broken-import copies fail the smoke run: MET; smoke and quick runs complete and validate (0 errors) : MET; `tests/data` 102, `tests/hooks` 88, `tests/model_v3` 369 passed (excluding `test_smoke.py`), `test_smoke.py` 6 passed (17 min). NOT MET: `accept.sh` end to end (no `test_converge.py`; step 5 would fail on the O1e nulls), block 3.
- Findings for the author (none repaired): (1) at `quick` size three of the five grid points fail their own check at the schedule chosen at `median_mid` (tm50_k05 r100): `max_mid` and `median_low` cannot raise the income-tax-on-gains target at rate 1.0 (0.106 against 0.171; 0.021 against 0.040), `median_high` the consumption tax (0.151 against 0.165); the file's range covers `median_mid` and `min_mid` only (`run.arm.failed` lists the others). (2) O1e under the market fund is no longer flat (at 20 paths S_low goes 0.34, 0.59, 0.76, 0.40, -0.21 at generator means 0, 2, 5, 10, 15 and so has a root near 13; S_central and S_high stay positive to 15), but the `quick` file has no root for any of the three schedules, so the O1e centre is null; the ruling says report and use a stated marker, and none is named for "no sign change on 0 to 15 percent". (3) The convergence test as specified is days of compute on the household arm (C3 alone is 400 level 2 draws at 1,000 paths, 76 s each, per schedule).
- Deviations from the brief: Touches does not name the validator, manifest, fixture or `test_arm_switch.py`; `-I -c` instead of `-I -m`; the O1e centre keeps the central root instead of `not_run_this_point`; `level2_draws` is the O1e draws run; OW1's held state accepted, not required (a manifest `arms` entry would break the 126c pin).
- Instruction friction: four entries in `docs/agents/friction-log.md`.
- Verification: as above; not run: `accept.sh`, any full-size run, the 5-point range merge with all five points (three fail), `--workers` above 1 (150c tests it byte for byte).
- Overview sections likely needing an update: none yet.
- Commit / branch: `brief/057-run-script-acceptance` (not merged: criteria unmet, diff outside Touches).

**Sixth-round rulings (author, 2026-11-24), on the three findings of the round 4 and 5 report:** (1) *Failed points.* A grid point that cannot meet its own closure target at the schedule chosen at `median_mid` stays in the file, marked `target_not_met`, with its outputs at the capped rate and the figure reached beside the target (never repaired, never silently dropped); the range is stated over all five points with the failures labelled, and `run.arm.failed` keeps listing them. The validator accepts `target_not_met` only on those points' cells, and a summary line says how many of the five met their target. (2) *O1e with no root.* The stated marker is `no_sign_change_0_15` (M1 keeps one sign across generator means 0 to 15 percent, so no break-even in range), accepted for O1e only, with the sign and the end values recorded beside it; no wider bracket in this run. (3) *Convergence test.* Acceptance runs a reduced C3 whose sizes are stated in the test and in the file (fewer level 2 draws and paths, about an hour in all; say in the change report what it measures); the full-size C3 is a later manual run, not part of acceptance, not part of the first official run. The sixth-round changes, then block 3 (`test_converge.py` with the reduced C3, the final refusal rules) and `--final` after the first `accept.sh` end to end passes.
