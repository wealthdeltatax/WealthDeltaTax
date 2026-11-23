# 057: Model v3 V3-12: run script, smoke test and acceptance wiring

- **Status:** ready (provisional scope, 2026-11-23: after 137c, 135c, 138c and 139c for a `--final` file; blocks 1 and 2 may start now)
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
- Register rows (139c) and the fund and floor fixes (137c, 138c) land before `--final`, because they change numbers and the gate hash.

## Blocks (added 2026-11-23; one push each)
- **Block 0:** progress block. **Block 1:** `run.py` (arm field, scenario-range assembly, null marker, pending marker for OF1 and CK1), validator change, tests. **Block 2:** `accept.sh`, `test_smoke.py` and the five seeded breakages. **Block 3:** `test_converge.py`, the `--final` refusal rules. Stop after block 2 if 137c, 135c, 138c or 139c are not merged; `--final` waits for them.

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
