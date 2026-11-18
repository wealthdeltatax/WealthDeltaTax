# 049: Model v3 V3-4: rate schedule and kernel (port)

- **Status:** draft (ready when the author approves 040g D2)
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** none (can start at once)
- **Read:** `docs/model-v3/architecture.md` 2.4, 3.2, 4 and 6.2 (S1 to S5, K1 to K10); `docs/model-v3/port-inventory.md` in full; `docs/model-v3/stage-c-decisions.md` items 3, 5, 9, 10; `model_v2/wdt_kernel.py` and `model_v2/wdt_core.py` (the lines the inventory names); `docs/model-v3/acceptance.md` V3-4 row.

## Goal
The rate function and the refund mechanics, ported with five changes and tested, with no dependence on any other v3 module.

## Decisions (author, 2026-11-18)
`architecture.md` approved (sections 8.1 and 9 as written); `acceptance.md` approved with Q1 to Q6 as proposed. v3 imports nothing from `model_v1/` or `model_v2/`. No file outside this brief's Touches is changed.

## Design
`core/schedule.py` (170 lines): `tau` logistic in W and in ln W with `(tau_m - tau_0) / tau_0`, ladder dropped, a monotone-marginal-rate check that raises on a non-progressive draw (R10). `core/kernel.py` (620 lines): the ported kernel vectorised over a line axis, all routes (A, B, C, D, Cv) and the three Route B modes; changes: refund is tau times loss, the envelope resets at death, each line carries cumulative paid and refunded, the `fresh_entrant` heir rule is dropped, the growth input is a `(T, n)` matrix. Both files import numpy only. Write kernel hand cases K1 to K5, K7, K10 and the equivalence tests K6 and K9, and the decomposition K8 on the 70-point grid of the inventory plus one case with `settle_delta` not zero.

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1.

This is build stage V3-4 of `architecture.md` section 7. One session, one lane; the stage ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. The stage's files are budgeted in `architecture.md` 6.1; a stage more than 15% over its budget reports it before the next starts.

## Touches
`model_v3/core/schedule.py`, `model_v3/core/kernel.py`, `tests/model_v3/test_schedule.py`, `tests/model_v3/test_kernel.py`, this brief's progress block.

## Acceptance criteria
- S1 to S5 and K1 to K10 pass.
- K8 holds to 1e-12; K6 and K9 hold to 1e-12; K3 is exact to the pound.
- `schedule.py` at most 170 lines and `kernel.py` at most 620; neither imports a project module.
- `git diff --stat` is limited to the Touches list.

## Checks to run
`pytest tests/model_v3 -q`. The `tests/model_v3/conftest.py` of V3-1 may not exist yet: if so, the tests are self-contained and V3-1 adopts them.

## Out of scope
Anything that reads the pack, register or paths; the ladder branch.

## Open questions
Stop and ask if K8 fails: it means the port or the decomposition is wrong, not the tolerance.

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
