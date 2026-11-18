# 049: Model v3 V3-4: rate schedule and kernel (port)

- **Status:** ready
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
- **Done:** `core/schedule.py` (77 lines), `core/kernel.py` (567 lines, 480 code), `test_schedule.py` S1 to S5, `test_kernel.py` K1 to K10; 24 tests pass.
- **Next:** none for this brief; V3-5 onward import `rate_function` and `run_lines`.
- **Decisions:** refund rate read at new declared wealth (as v2); cumulative paid/refunded are lifetime records, not reset at death; K8 settle_delta case uses a stale post-sale basis set by the test (v1 convention); no `__init__.py` added (outside Touches).
- **Gotchas:** `schedule.py` needs no levers or pack reading, so the named schedules and schedule grid are not built here.
- **Resume:** n/a
- **Not run:** `tests/model_v3/test_budget.py` and import-graph tests of V3-1 (rebased onto them, see report).
- **State:** done; merged by the auto-merge rule if the report below says so
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 049c, model v3 V3-4: rate schedule and kernel (port)
- Files changed: model_v3/core/schedule.py (new: tau, rate_function with R10 check); model_v3/core/kernel.py (new: port of model_v2/wdt_kernel.py with five changes); tests/model_v3/test_schedule.py (S1-S5); tests/model_v3/test_kernel.py (K1-K10); this brief's progress block
- What is different now: v3 has the rate function and the refund kernel, tested, importing numpy only
- New or changed interfaces: schedule.tau(W,k,tau_0,tau_m,W_min,form), schedule.rate_function(...)->callable (raises ValueError on a non-progressive draw); kernel.run_lines(rate_fn, g_mat (T,n), V0, ...); Book.paid / Book.refunded cumulative per line; step_death has no heir_influx argument
- Acceptance criteria:
  - S1-S5, K1-K10 pass: met (24 passed)
  - K8 to 1e-12: met. 70 points (alpha 0.5,0.75,1,1.5,2,3,5 x g -3%,0,7.45%,10.45%,20% x N 10,30): worst |error| 2.3e-13. Non-zero settle_delta case (alpha 1.5, g 10.45%, N 30, stale post-sale basis): settle_delta 4.19, error 1.1e-14
  - K6 (1000 lines vs alone, three B modes) and K9 to 1e-12: met
  - K3 exact to the pound: met (refund = paid to 1e-6; one pound over is held back, lost_refund 1e-6)
  - schedule.py <= 170 lines: 77. kernel.py <= 620: 567 (480 code). No project import: met (ast test)
  - git diff --stat limited to Touches: met
- Deviations from the brief: none. K8 does not reuse the v2 `settle_tw` pound cap: on the kernel path the refund cap is in units (as in v2's kernel), so the terms are read off kernel flows and TW off the book.
- Risks / follow-ups: (1) the refund rate is read at new declared wealth W_new (v2 behaviour); the papers' "rate on an equivalent gain" could mean the old wealth. Author may confirm. (2) For Route C the cap is units paid, so credited pounds refunded can exceed credited pounds paid if the declared price rose; K3 tests the cash routes. (3) named schedules and the schedule grid from levers.json are not built here (architecture 2.4 lists them; the brief's Out of scope reads no pack).
- Verification: pytest tests/model_v3 -q; line counts; ast import check
- Overview sections likely needing an update: model v3 build status
- Commit / branch: brief/049-schedule-kernel
```

