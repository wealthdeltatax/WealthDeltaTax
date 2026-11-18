# 051: Model v3 V3-6: wealth and payer base

- **Status:** draft (ready when the author approves 040g D2)
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** 048, 049
- **Read:** `docs/model-v3/architecture.md` 2.3 and 6.2 (B1 to B5); `docs/model-v3/country-pack.md` (`wealth_distribution`, `wealth_tail`, `household_incidence`); `docs/model-v3/drivers.md`; `model_v2/rates_core.py` lines 408 to 599 as specification only; `docs/model-v3/acceptance.md` V3-6 row.

## Goal
The payer lines the kernel runs, calibrated to the pack, with income and liquid assets by band.

## Decisions (author, 2026-11-18)
`architecture.md` approved (sections 8.1 and 9 as written); `acceptance.md` approved with Q1 to Q6 as proposed. v3 imports nothing from `model_v1/` or `model_v2/`. No file outside this brief's Touches is changed.

## Design
`core/base.py` (380 lines): build `Base` (arrays `V0` by route, weights, band and decile labels, W_min as the lever ratio times median house price per adult, income and liquid assets per line, death-age structure G = 30) from the pack and register; calibrate weights to the pack totals; fail if a band does not partition. Rewritten from the specification, not ported.

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1.

This is build stage V3-6 of `architecture.md` section 7. One session, one lane; the stage ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. The stage's files are budgeted in `architecture.md` 6.1; a stage more than 15% over its budget reports it before the next starts.

## Touches
`model_v3/core/base.py`, `tests/model_v3/test_base.py`, this brief's progress block.

## Acceptance criteria
- B1 to B5 pass: band shares partition and equal the pack totals; W_min equals the lever ratio times the pack median; income and liquid assets are non-negative and ordered; two runs give the same base.
- `base.py` at most 380 lines; it imports numpy and `core/pack.py` only.
- `git diff --stat` is limited to the Touches list.

## Checks to run
`pytest tests/model_v3 -q`.

## Out of scope
Kernel changes; behaviour (a level 2 draw in V3-10).

## Open questions
Ask if the pack tables do not support a route mix; do not invent one.

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
