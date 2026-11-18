# 047: Model v3 V3-2: country pack and register loader

- **Status:** draft (ready when the author approves 040g D2)
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** 046 (the tests scaffold)
- **Read:** `docs/model-v3/architecture.md` 2.1 and 6.2 (`pack` tests P1 to P7, P10); `docs/model-v3/country-pack.md` in full; `registry/inputs.json` and `docs/model-v3/inputs.md` (headers only); `docs/model-v3/acceptance.md` V3-2 row.

## Goal
`core/pack.py` reads and validates any country pack and the register, so the UK data and a test pack load through the same code.

## Decisions (author, 2026-11-18)
`architecture.md` approved (sections 8.1 and 9 as written); `acceptance.md` approved with Q1 to Q6 as proposed. v3 imports nothing from `model_v1/` or `model_v2/`. No file outside this brief's Touches is changed.

## Design
Implement `core/pack.py` (340 lines) as `architecture.md` 2.1 says: manifest first, folder name equals `country`, per-file sha256, header equals schema, first violation raises with file, row and column, no fill or interpolation or clipping; `pack_sha256`; the register as low, central and high per id with `(J)` flags and unit; the consistency checks X1 and X2 (they run only when the UK pack is present, so this stage tests them on the fixture only); accessors; the data facts DH1a and DH1b. Build the ZZZ fixture pack under `tests/model_v3/fixtures/pack_ZZZ/` (small, invented numbers, flagged in its NOTICE).

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1.

This is build stage V3-2 of `architecture.md` section 7. One session, one lane; the stage ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. The stage's files are budgeted in `architecture.md` 6.1; a stage more than 15% over its budget reports it before the next starts.

## Touches
`model_v3/core/pack.py`, `tests/model_v3/test_pack.py`, `tests/model_v3/fixtures/pack_ZZZ/`, this brief's progress block.

## Acceptance criteria
- P1 to P7 and P10 pass; the ZZZ pack loads with no code change (R11).
- A changed byte in a fixture file fails on the sha256 and names file, row and column.
- `core/pack.py` is at most 340 lines (`test_budget.py`) and imports only numpy and the standard library.
- `git diff --stat` is limited to the Touches list.

## Checks to run
`pytest tests/model_v3 -q`.

## Out of scope
The UK pack (V3-3); P8 and P9 (V3-3, they need it).

## Open questions
Ask where the country pack format is ambiguous; do not extend the format.

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
