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
- **Done:** Read the household-flow plan, 096r and 095r source register. Reviewed Round 8 ONS bulletin/methodology; located age-component (2813), debt-by-age (3222), GB population projection and qx files; reviewed HBAI, FRS and UKDS 7215/6709 access. Added research note and three CSVs, including pack band aggregation.
- **Next:** Parse the held WAS and ETB workbooks plus ONS binary files; record sheet/range/weights and three cell spot-checks; extract numeric population and qx series; resolve inactive-not-retired treatment before phase 2.
- **Decisions:** Scenario B unchanged. No rate or parameter selected. Use self-reported retired status rather than treating State Pension age as retirement; leave economically inactive but not retired unallocated pending author ruling.
- **Gotchas:** No published wealth-band × age/status joint weights. Round 8 accreditation suspended; DB pension valuation break. Study 7215 Round 8 person-file dictionary missing. Study 6709 is Secure Access and UK-based.
- **Resume:** Checkout `brief/098r-was-tables-population`; parse `Rates Data/totalwealthtables.xlsx`, `Rates Data/financialwealthtables.xlsx`, `Research/etbreferencetablesfye202324final.xlsx`, ONS 2813/3222, `gb1.zip` and `periodcohortqx2024basedgb.xlsx`.
- **Not run:** `python -I pipeline/check_agent_docs.py` (no local checkout); no XLSX/ZIP cell extraction or microdata analysis.
- **State:** partial; branch pushed; acceptance criterion 1 unmet; no merge.
<!-- progress:end -->


### Implementation notes — 2026-11-21

**Change report**
- **Task:** 098r — WAS published tables, ages and the working-to-retired transition.
- **Files changed:**
  - `docs/research/098r-was-tables-and-population.md` — source findings, definitions, data limitations, access plan and exact remaining downloads.
  - `docs/research/data/098r/was_published_evidence.csv` — numeric ONS Round 8 age/status and composition figures stated in the bulletin.
  - `docs/research/data/098r/was_band_reconciliation.csv` — aggregation of existing pack deciles into WDT bands; derived means labelled as such.
  - `docs/research/data/098r/098r_source_inventory.csv` — source periods, geography, access status and exact links.
  - `docs/agents/friction-log.md` — binary parsing limitation.
  - This brief — progress and change report.
- **What is different now:** the public evidence and source routes are documented. The report distinguishes age/status marginals from the missing joint wealth-band × stage weights. It identifies the preferred microdata route and the ONS tabulation request.
- **New or changed interfaces:** none.
- **Acceptance criteria:**
  1. **Not met.** The held WAS/ETB workbooks and ONS binary files could not be parsed. No sheet/range metadata or three-cell workbook spot-checks are claimed. Public HTML figures were extracted and source-linked.
  2. **Partly met.** Decile-to-WDT-band mapping and pack arithmetic are shown. The held workbook band edges could not be independently rechecked.
  3. **Met.** HBAI/FRS/ETB ranking limitations, ONS population and mortality definitions, retirement-transition limitations, and the UKDS 7215/6709 access route are documented.
- **Deviations from the brief:** no scope change. Binary extraction is incomplete because the available connector/runtime cannot decode XLSX/ZIP files.
- **Risks / follow-ups:** full workbook extraction and numeric age/mortality series remain outstanding. Phase 2 also needs an author ruling on the economically inactive, not-retired residual; it is not silently assigned to either of the two stages.
- **Instruction friction:** added 098r entry to `docs/agents/friction-log.md`.
- **Verification:** official ONS, DWP and UKDS source pages and download links checked; pack band arithmetic calculated from the existing CSV. No local script/check was run because there is no local repository checkout.
- **Overview sections likely needing an update:** none until the brief is completed.
- **Commit / branch:** see branch head; `brief/098r-was-tables-population`.
