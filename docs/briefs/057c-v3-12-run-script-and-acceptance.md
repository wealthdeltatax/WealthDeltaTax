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
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** draft; not started
<!-- progress:end -->
