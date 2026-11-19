# 051: Model v3 V3-6: wealth and payer base

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** 048, 049, 067, 068, 069 (all merged)
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

## Guru rulings, 2026-11-19
Blocked on the first run (Agent 3's note on `brief/051-base`): the merged UK pack had shares only, and no register row held the route mix. Both were my gaps in the architecture, not yours. They are now resolved and merged (067c, 068g, 069r). The branch `brief/051-base` carries only the blocker note: start again from main, keep the progress block. Depends on 048, 049, 067, 068, 069 (all merged).

**Where each input is (read it from here; type none of it).**
- **Pack, `wealth_distribution.csv`** (field list: the 067c progress block, `docs/archive/briefs/067c-pack-base-fields.md`):
  - `wealth_total`: D1 to D10 and `all`, `gbp_bn`, household basis, 2020-22. The deciles sum to 13,567.89 and `all` is the printed 13,568.
  - `households`: D1 to D10 and `all`, `thousand`; each decile is 2,699.1 (a tenth of 26,991 by definition; no held table prints a count per decile).
  - `median_house_price`: band `all`, `gbp`, 300,000, England, year to Sep 2025.
  - `gdp`: `all`, `gbp_bn`, 2,211.48 (mean of FY 2020-21 and FY 2021-22, nominal as published).
  - **`adults` is not in the pack** (no held table gives adults by decile); it is a register row, below.
- **Register, `registry/inputs.json`:**
  - Route mix, family D13: I-D13a Route A 48/50/53, I-D13b Route B 25/25/25, I-D13c Route C 5/8/10, I-D13d Route D 17/17/17 (% of initial value; A absorbs the C change; the four sum to 100 at central and at each end of the C range). I-D13e is the Route B payment mode: **text, so `low`, `central`, `high` are null and the word `sale` is in `nulls.central.raw`.** Read it from there.
  - Adults per household: I-D4h, 1.77 / 1.93 / 1.93 (central: persons aged 16 and over, Table 2.11, over households, Table 2.9). The central counts people **16 and over**, not 18 and over.
- All the D13 rows and I-D4h are `(J)` rows still pending the author's decision at gate G3. That is expected; build to the central and carry low and high.

**Known mismatches; do not fix them, report them in the change report if they bite.**
- Register I-D4a (wealth to GDP, central 5.94) uses calendar-2021 GDP of 2,284bn; the pack ratio is 13,568 / 2,211.48 = 6.14. The base reads the pack. The register row is a guru and author question (`docs/brief-suggestions.md`).
- Register I-D4b's central implies 1.77 adults per household; I-D4h's is 1.93. If your `base.py` needs an adult count in a test that touches I-D4b, say which row you used. Open question for the author (`docs/brief-suggestions.md`).
- `wealth_distribution.csv` is now `cite-only` in the manifest (the IFS GDP series), so any later page that republishes pack numbers needs that noted.
- In a shallow git clone the pack builder writes different `retrieved` dates, so do not run `build_gbr.py` to rebuild the pack in a shallow clone; you should not need to rebuild it for this brief.

**Budgets.** `core/pack.py` is exactly at its 340-line budget, so `base.py` may not add to it; accessors you need come from `lookup` and the existing functions or you stop and report. `base.py` is budgeted 380 lines, its test file 220.

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
