# 053: Model v3 V3-8: burden and savings

- **Status:** draft (ready when the author approves 040g D2)
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** 052
- **Read:** `docs/model-v3/architecture.md` 2.6 and 6.2 (D1 to D6); `docs/model-v3/metrics.md` (M2, M2b, M2c, M3, M4a to M4c, M5, M6, M8, M11, M12); `docs/model-v3/added/` (welfare and problem outputs); `docs/model-v3/acceptance.md` V3-8 row.

## Goal
Burden, non-payer savings and the comparators as per-path arrays.

## Decisions (author, 2026-11-18)
`architecture.md` approved (sections 8.1 and 9 as written); `acceptance.md` approved with Q1 to Q6 as proposed. v3 imports nothing from `model_v1/` or `model_v2/`. No file outside this brief's Touches is changed.

## Design
`core/burden.py` (430 lines) for the ids `O2, O3, O2b, O2c, O4a, O4b, O5, O6, O8, OL1, OH1b, OH1b2, OH1c, DH1c` of `architecture.md` 2.10. Comparators read only the pack and register. Imports `pack`, `base`, `schedule`, `kernel`, `revenue`.

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1.

This is build stage V3-8 of `architecture.md` section 7. One session, one lane; the stage ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. The stage's files are budgeted in `architecture.md` 6.1; a stage more than 15% over its budget reports it before the next starts.

## Touches
`model_v3/core/burden.py`, `tests/model_v3/test_burden.py`, this brief's progress block.

## Acceptance criteria
- D1 to D6 pass; hand cases exact to 1e-12.
- DH1c equals the pack decile table.
- `burden.py` at most 430 lines.
- `git diff --stat` is limited to the Touches list.

## Checks to run
`pytest tests/model_v3 -q`.

## Out of scope
Supporting metrics (V3-9); the runner.

## Open questions
Ask if a metric formula in `metrics.md` is ambiguous.

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
