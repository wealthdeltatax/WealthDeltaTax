# 054: Model v3 V3-9: supporting metrics

- **Status:** draft (ready when the author approves 040g D2)
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** 052
- **Read:** `docs/model-v3/architecture.md` 2.7 and 6.2 (U1 to U6); `docs/model-v3/metrics.md` (M7, M7c to M7e, M9, M13, M14, M15a, M15b, S1); `docs/model-v3/added/`; `docs/model-v3/acceptance.md` V3-9 row.

## Goal
Declaration, welfare, lock-in, envelope, migration and capitalisation metrics.

## Decisions (author, 2026-11-18)
`architecture.md` approved (sections 8.1 and 9 as written); `acceptance.md` approved with Q1 to Q6 as proposed. v3 imports nothing from `model_v1/` or `model_v2/`. No file outside this brief's Touches is changed.

## Design
`core/support.py` (520 lines) for `O7, OD1, OW1, OW2, OW3, OM1, OS1`. S1 is a switch, off in every headline cell, with one extra variant run. It does not import `burden`.

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1.

This is build stage V3-9 of `architecture.md` section 7. One session, one lane; the stage ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. The stage's files are budgeted in `architecture.md` 6.1; a stage more than 15% over its budget reports it before the next starts.

## Touches
`model_v3/core/support.py`, `tests/model_v3/test_support.py`, this brief's progress block.

## Acceptance criteria
- U1 to U6 pass; hand cases exact.
- S1 off equals S1 absent.
- `support.py` at most 520 lines; no import of `burden`.
- `git diff --stat` is limited to the Touches list.

## Checks to run
`pytest tests/model_v3 -q`.

## Out of scope
Burden metrics (V3-8); the runner.

## Open questions
Ask if a welfare formula needs a risk-aversion value the register does not hold.

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
