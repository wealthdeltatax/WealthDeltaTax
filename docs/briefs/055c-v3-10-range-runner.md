# 055: Model v3 V3-10: range runner

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** 053, 054
- **Read:** `docs/model-v3/architecture.md` 2.8, 3.1 to 3.3, 6.2 (N1 to N7) and 6.5; `docs/model-v3/drivers.md`; `docs/model-v3/tornado.md`; `docs/model-v3/stage-c-decisions.md` items 2, 6, 7; `docs/model-v3/acceptance.md` V3-10 row and section 4 (R3, R10).

## Goal
The two-level run, the schedule sweep, the tornado and the stress test, producing Samples.

## Decisions (author, 2026-11-18)
`architecture.md` approved (sections 8.1 and 9 as written); `acceptance.md` approved with Q1 to Q6 as proposed. v3 imports nothing from `model_v1/` or `model_v2/`. No file outside this brief's Touches is changed.

## Design
`runner/runner.py` (360 lines): level 1 at `N1` = 10,000 per schedule, level 2 at `N2` = 200 Latin hypercube draws of `N2P` = 1,000 paths on common random numbers, folded into the kernel's line axis in chunks of 1,000 paths; seed streams. `runner/sweeps.py` (300 lines): the feasibility map over the lever grid, the three named schedules by the confirmed rule, the tornado, break-even and negative-M1 share (`O1e`, `O1f`), CK1 and the bootstrap run. `runner/pool.py` (70 lines) only if the full run would exceed 60 minutes or K6 failed. Add the set-equality test between the drawn level 2 ids and the tier 1 list of `drivers.md` (R3), and the monotone check over every cell of the lever grid (R10).

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1.

This is build stage V3-10 of `architecture.md` section 7. One session, one lane; the stage ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. The stage's files are budgeted in `architecture.md` 6.1; a stage more than 15% over its budget reports it before the next starts.

## Touches
`model_v3/runner/runner.py`, `model_v3/runner/sweeps.py`, `model_v3/runner/pool.py`, `tests/model_v3/test_runner.py`, this brief's progress block.

## Acceptance criteria
- N1 to N7 pass; the same seed gives byte-identical `Samples`.
- The R3 set-equality and R10 grid tests pass.
- N7: the time of one 10,000-path schedule is measured and written to the change report; `pool.py` exists only if its trigger fired.
- `runner.py` at most 360 lines and `sweeps.py` at most 300.
- `git diff --stat` is limited to the Touches list.

## Checks to run
`pytest tests/model_v3 -q`.

## Out of scope
The writer (V3-11); the convergence test (V3-12); a final run.

## Open questions
Ask if N7 shows the full run would take over 60 minutes and K6 passed: the pool rule is the answer, but confirm the reference machine.

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
