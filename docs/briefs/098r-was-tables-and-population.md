# 098: WAS published tables, ages and the working-to-retired transition

- **Status:** ready
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
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
