# 098: WAS published tables, ages and the working-to-retired transition

- **Status:** done, merged 2026-11-21
- **Author/date:** K. Ogata with the guru, 2026-11-21
- **Depends on:** none
- **Read:** `docs/model-v3/household-flow-plan.md`; `docs/research/096r-cohort-cell-design.md` (sections 1 to 3 and open question 4); `docs/research/095r-source-acquisition-and-verification.md` (section 1); the held workbooks `Rates Data/totalwealthtables.xlsx` and `Rates Data/financialwealthtables.xlsx`; `model_v3/pack/GBR/wealth_distribution.csv` and `build_gbr.py`.

## Goal
Get what the published WAS tables, ONS population statistics and the held workbooks can give for the **stage** dimension of the cells (working or retired, by wealth band), the composition and debt by band, and the transition hazards. Confirm what only microdata can give, and what the author must apply for.

## Decisions (author, 2026-11-21)
Same as 097r. Scenario B.

## Design
1. **From the held workbooks:** extract, with table and sheet names, wealth by age band and by wealth decile or band (Table 2.11 and any equivalent), composition (property, financial, DB and DC pension, other), and debt where given, for the rounds present. Reconcile the band edges to the pack's bands (D4-5, D6-7, D8-9, D10).
2. **Stage weights:** the share of households or adults in each wealth band by age group, and a working/retired split (state the age or status definition used, and what the tables can and cannot support).
3. **Retired income:** what the published sources give for income of retired households by wealth band or decile (HBAI, FRS, ETB reference tables `Research/etbreferencetablesfye202324final.xlsx`); say which of these ranks by income only.
4. **Transitions:** ONS population projections by single year or age group and mortality by age (and by wealth or deprivation if published) to give hazards for working to retired and death; the ONS definitions used.
5. **Microdata route:** UKDS study 7215 (safeguarded) and 6709 (secure): the steps, licence, training and timescale, and the variables each would give that the tables do not. A list of exactly what to ask ONS for if tables are preferable.
6. Anything the held workbooks do not contain that the author must upload, with the exact file.

## Touches
`docs/research/098r-was-tables-and-population.md` (new), `docs/research/data/098r/*.csv` (new), this brief's progress block, `docs/agents/friction-log.md`. No code, pack, register or manifest edits.

## Acceptance criteria
- Every table extracted has its sheet, range, round, unit and weights stated, and matches the workbook on at least three spot-checked cells.
- The band-edge reconciliation to the pack is shown, or the mismatch is stated.
- Items 3 and 4 say what is and is not identified; item 5 is a concrete access plan.

## Checks to run
`python -I pipeline/check_agent_docs.py`.

## Out of scope
Parameter choice; microdata analysis; changes to the pack.

## Open questions
None.

## Implementation notes
<!-- progress:start -->
- **Done:** First pass (agent, no spreadsheet reader): public bulletin evidence, source inventory, access plan. Close-out (guru): extracted held WAS Tables 2.5, 2.11, 2.13, ONS 2813, 3222, population (principal), qx and ETB Tables 3b and 4b with `extract_098r.py`; band-edge reconciliation; derived stage shares by WDT band; note corrected (section 9 supersedes the first pass).
- **Next:** author rulings (inactive-not-retired; whether the £-band stage table suffices for phase 2); retire.
- **Decisions:** Scenario B unchanged. No rate or parameter chosen. Self-reported retired status, not State Pension age; inactive-not-retired left unallocated.
- **Gotchas:** The first pass claimed the joint stage-by-wealth distribution is not published; the held Tables 2.11 and 2.13 publish it by £ band for persons (rounded percentages, no deciles, age table has no weighted totals). Cohort qx exists only for births from 1981.
- **Resume:** n/a
- **Not run:** none.
- **State:** done; merged
<!-- progress:end -->

## Change report

- **Task:** 098r, WAS published tables, ages and the working-to-retired transition.
- **Files changed:** `docs/research/098r-was-tables-and-population.md` (first pass by the research agent; corrected and section 9 added by the guru); `docs/research/data/098r/` (14 new CSVs, `extract_098r.py`, the small ONS workbooks 2813, 3222 and qx, the principal population projection and its code list); `docs/agents/friction-log.md`; this brief.
- **What is different now:** stage-by-wealth-band weights, age and activity by band, population, mortality, debt by age and retired income are in the repo as text, with a script that rebuilds them.
- **New or changed interfaces:** none.
- **Acceptance criteria:** (1) met: sheet, block, round, unit and weights stated; three or more spot-checked cells per source family match. (2) met with the mismatch stated: WAS £ bands group to 28, 24, 15, 20 and 14 % of households against the pack's 30, 20, 20, 20 and 10 %. (3) met: items 3 and 4 say what is and is not identified; the access plan is narrowed to the household-based cross-tab and debt by band.
- **Deviations from the brief:** `extract_098r.py` and the ONS workbooks added to `docs/research/data/098r/` (Touches said CSVs); the 13 other projection variants (18 MB) stay on branch `brief/098r-was-tables-population` only.
- **Risks / follow-ups:** stage shares are person-based and carry whole-number rounding; the age-by-band table has no weights; the inactive-not-retired residual needs an author ruling; Round 8 accreditation is suspended and the DB pension valuation changed.
- **Instruction friction:** the first-pass agent ran without a spreadsheet reader and logged it (entry kept). Research briefs that name held workbooks should say the run needs a local checkout.
- **Verification:** `python -I pipeline/check_agent_docs.py` passes; extraction re-run clean; spot-checks above.
- **Overview sections likely needing an update:** none.
- **Commit / branch:** `brief/098r-close`, merged to `main` fast-forward.
