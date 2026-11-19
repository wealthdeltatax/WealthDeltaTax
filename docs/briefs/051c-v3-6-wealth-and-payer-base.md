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
- **Done:** `model_v3/core/base.py` (122 lines, budget 380; numpy and `core/pack.py` only) and `tests/model_v3/test_base.py` (101 lines). `build_base(pack, register, ratio)` gives `Base`: 11 lines (D1 to D9, D10a the 90th to 99th percentile, D10b the top 1%), households and adults, weights, wealth by line summing to the pack total, `V0` by route A to D, income and liquid assets per adult, `w_min`, wealth over GDP, the ten income deciles of gross income and total tax, G = 30. `w_min(pack, ratio)`. B1 to B5 pass. `pytest tests/model_v3 -q`: 128 passed.
- **Next:** V3-7 (052c) once this is merged.
- **Decisions:** (1) Lines are the WAS wealth deciles, D10 split by the pack's top 1% over top 10% WID share (latest year both are given): a ratio of two adult-basis shares applied to the household-basis D10, the one cross-basis step. (2) Adults per household is the register's I-D4h central (1.93), the same for every line; W_min is compared with wealth per adult. (3) Route mix is the register's I-D13a to d central, the same for every line (no source varies it by band); low and high are for the level 2 draw. (4) Lines are scaled so wealth sums to the printed total (the deciles sum to it within 0.11bn). (5) Income per line is the register's I-D9a to d (D4 to D5, D6 to D7, D8 to D9, D10) over adults per household; liquid assets are the pack's net financial share of wealth by the same bands (the register calls it an upper-side proxy). Lines D1 to D3 have no source and stay nan: the build raises if a line at or above W_min has nan, which no lever ratio on the grid triggers (the lowest, 0.25, gives W_min below the D4 mean).
- **Gotchas:** (1) Income by line is not ordered: I-D9c (D8 to D9) is 71,500 and I-D9d (D10) 71,400, so D10 sits 0.1% below; B4 tests order for the income deciles and liquid assets, and non-negativity for the line income. D10a and D10b share one income figure (no source for the top 1%). (2) wealth over GDP is 6.14 on the pack's GDP, the register's I-D4a central is 5.94 (067c noted this). (3) The Route B payment mode (I-D13e, text) is not read: `load_register` drops text rows to None; it is a kernel argument. (4) Not in `Base`, by the brief: the cohort return tiers and the behaviour shrink factor (V3-10), non-payer income-decile shares (M4a, V3-8: I-H2a depends on W_min). (5) Decile means: a decile that straddles W_min (D4 at the lowest ratio, D5 and D6 at the central) is treated as all payers or none by its mean; the kernel sees the line mean, not the spread inside a decile.
- **Resume:** none needed.
- **Not run:** nothing in the brief.
- **State:** done; merged to main by the auto-merge rule
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 051c, model v3 stage V3-6: wealth and payer base
- Files changed: model_v3/core/base.py (new, 122 lines); tests/model_v3/test_base.py (new, 101); this brief
- What is different now: v3 builds the payer lines the kernel runs from the UK pack and the register: values by route, weights, income and liquid assets, W_min.
- New or changed interfaces: build_base, w_min, Base, BaseError, IDS, BANDS, LABELS, G in model_v3.core.base
- Acceptance criteria: B1 to B5 pass (met); base.py 122 of 380 lines, imports numpy and core/pack.py only (met); git diff --stat limited to Touches (met)
- Deviations from the brief: none
- Risks / follow-ups: (1) income and liquid assets exist only for wealth bands D4 and above; (2) the top 1% split mixes adult and household bases; (3) one adults-per-household figure for all lines; (4) route mix identical across lines; (5) wealth over GDP 6.14 against the register's 5.94 (guru)
- Verification: pytest tests/model_v3 -q: 128 passed
- Overview sections likely needing an update: model v3 build status (V3-6)
- Commit / branch: brief/051-base, merged to main
```
