# 097: Collect the open UK series (national accounts, Bank of England, HMRC)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-21
- **Depends on:** none
- **Read:** `docs/model-v3/household-flow-plan.md`; `docs/research/095r-source-acquisition-and-verification.md` (sections 2, 3, 5 and 9, which give the links); `docs/research/095r-uk-household-flow-evidence-map.md` (the per-flow table); `docs/agents/reference/research/reference-workflow.md`.

## Goal
Collect, or confirm unreachable, the open numeric series the household-flow model needs, so that phase 2 has data in hand. Do not analyse beyond checking identities and units.

## Decisions (author, 2026-11-21)
- Scenario B: cells by wealth band and life stage; saving on the income side; no universal depletion rate; no value chosen for fiscal effect (see the plan).
- A source the tools cannot read is **logged with its exact file name and link** for the author to upload to `Research/`; it is not guessed or replaced by a summary.

## Design
For each item: try to fetch; record the outcome as **extracted**, **reachable but not parseable**, or **unreachable**; for extracted series write a CSV to `docs/research/data/097r/` with columns series id or table, period, value, unit, price basis, seasonal adjustment, sector, sign convention, source link and retrieval date, and a one-line definition.
1. **ONS sector accounts and UK Economic Accounts, households (S.14, and S.14+S.15 where only that is given):** D41, D42, D44, D45 received and paid; D8; gross disposable income; saving and the saving ratio; household final consumption expenditure; other changes in volume and revaluation; net worth and the financial and non-financial asset and liability stocks. Annual 1997 to the latest year, and quarterly if parseable.
2. **ONS national balance sheet:** household net worth and its components by year, with the revaluation split by asset class.
3. **Bank of England NMG survey (2011 to 2026 and 2004 to 2011 files, and the Stata do-file):** if the file cannot be read, log it. If readable, record the variable list (saving, income, debt, repayments, interest, financial wealth, age) and the years each is present; extract nothing at household level.
4. **HMRC:** Personal Incomes Statistics Table 3.7 (property, interest, dividends by income range), capital gains tax statistics, inheritance tax liabilities (estates by size, reliefs), property rental income.
5. **Reconciliation checks that need no judgement:** the national-accounts identity for households (saving equals disposable income plus pension adjustment less consumption), and units and vintage of net worth.
6. **Per-source register** (what was fetched, what is missing, what the author must upload) in the note's table.

## Touches
`docs/research/097r-open-series-collection.md` (new, the register and checks), `docs/research/data/097r/*.csv` (new), this brief's progress block, `docs/agents/friction-log.md`. No code, pack, register or manifest edits.

## Acceptance criteria
- Each of items 1 to 4 has a status per series or file; each extracted CSV has the columns above and values that match the source on at least three spot-checked rows (stated in the note).
- Unreachable items list the exact link and file name.
- No figure is described as a saving, depletion or consumption rate for a wealth band.

## Checks to run
`python -I pipeline/check_agent_docs.py`.

## Out of scope
Microdata (WAS, ELSA, matched LCF-WAS); any parameter or register row; interpretation for the model.

## Open questions
None.

## Implementation notes
<!-- progress:start -->
- **Done:** Read the required agent/workflow/decision documents; created the research note and per-source status register; extracted ONS annual S.14 flow and financial-stock series where HTML time-series tables were readable; extracted HMRC HTML summary metrics; created source-linked CSVs; checked the household saving identity and the NBS financial-stock identity.
- **Next:** Parse the uploaded ONS XLSX, BoE NMG workbooks and HMRC ODS files in a local/runtime environment that supports these formats; then extend the source register and CSVs. The author upload step is complete.
- **Decisions:** Scenario B preserved. No wealth-band consumption/depletion rate or fiscal parameter introduced. ONS D.45 is treated as rent on land, not gross landlord rental income.
- **Gotchas:** The author has now uploaded the ONS QSA/NBS workbooks, both BoE NMG workbooks, the Stata example and HMRC ODS tables under `docs/research/data/097r/`. The Stata example is readable and documents income construction for 2024 and March 2025 only; it does not identify saving, consumption, debt, repayments, interest, financial wealth or age variables. Binary workbook/table contents remain unread in the available connector runtime. HAXW and M8MD are Blue Book 2025 vintage (latest annual value 2024); the other newer UKEA series run to 2025.
- **Resume:** Continue from section 8 of `docs/research/097r-open-series-collection.md`; parse the already-uploaded files and update the same register and CSV set.
- **Not run:** `python -I pipeline/check_agent_docs.py` (the GitHub connector provides repository API access, not a local checkout/runtime for executing the project script).
- **State:** source uploads received; accessible HTML extraction and Stata example review complete; full XLSX/ODS extraction and NMG variable inventory remain outstanding because the available repository connector/runtime cannot decode the binary files.
<!-- progress:end -->

## Change report

- **Task:** Brief 097r — Collect the open UK series (national accounts, Bank of England, HMRC).
- **Files changed:**
  - `docs/research/097r-open-series-collection.md` — source register, extraction outcomes, limitations, upload list and mechanical checks.
  - `docs/research/data/097r/ons_household_flows_annual.csv` — annual ONS S.14 flow series.
  - `docs/research/data/097r/ons_household_consumption_annual.csv` — annual ONS S.14 P.31 consumption.
  - `docs/research/data/097r/ons_household_saving_identity_check.csv` — source series and derived identity checks.
  - `docs/research/data/097r/ons_nbs_financial_annual.csv` — annual ONS S.14 financial stocks.
  - `docs/research/data/097r/hmrc_html_summary_extracts.csv` — HMRC numeric summary extracts from readable HTML commentary.
  - `docs/briefs/097r-open-series-collection.md` — progress block and this report.
  - `docs/agents/friction-log.md` — binary download/content-type limitation.
- **What is different now:** Accessible ONS and HMRC HTML series/summary data are in source-linked CSVs; the report records all remaining unreadable files with exact filenames and URLs. The household saving identity and NBS financial-stock identity reconcile.
- **New or changed interfaces:** None.
- **Acceptance criteria:**
  - Item 1 (ONS): **met as an acquisition register**; readable annual series extracted, unavailable series/workbooks explicitly marked reachable but not parseable.
  - Item 2 (NBS): **partly met**; financial stocks extracted and checked; non-financial components and revaluation split await readable NBS file.
  - Item 3 (BoE NMG): **status recorded, extraction not met**; workbooks and Stata do-file are published but not parseable here; variable inventory awaits author upload.
  - Item 4 (HMRC): **partly met**; HTML summaries extracted; underlying banded ODS tables are reachable but not parseable.
  - CSV schema and source spot checks: **met** for all five CSVs; checks are documented in the research note.
  - Exact links for inaccessible files: **met**.
  - No wealth-band saving, consumption or depletion rate introduced: **met**.
- **Deviations from the brief:** Full spreadsheet extraction could not be completed because the retrieval tool rejected CSV/XLSX/ODS/Stata file content-types. No substitute values were invented.
- **Risks / follow-ups:** Author upload is required to complete NMG variable inventory, full D.42/D.44 and NBS non-financial/revaluation series, and full HMRC band tables. The local agent-doc check remains unrun.
- **Instruction friction:** Added 2026-11-21 entry to `docs/agents/friction-log.md`.
- **Verification:** Three-year saving identity check (2023–2025) and three-year financial-stock identity check (2023–2025) passed; source-value spot checks are recorded. `python -I pipeline/check_agent_docs.py` **not run**: repository connector has no local checkout/runtime. No CI status checks are attached to the branch.
- **Overview sections likely needing an update:** None; this brief adds acquisition evidence and no model conclusion.
- **Commit / branch:** `0294bc1b18f29d7545f96372e56aa13d5d70db7a` / `brief/097r-open-series-collection`. Branch is 18 commits ahead of main and 0 behind. **NEEDS THE AUTHOR**; not merged because the named check was not run and unreadable source files remain.


## Follow-up change report (2026-11-21)

- **Author action received:** ONS QSA Q2 2026, ONS NBS, both BoE NMG workbooks, the BoE Stata example, HMRC Personal Incomes collated tables, CGT Tables 1–3, IHT Tables 12.1–12.3 and property-rental tables are now committed under `docs/research/data/097r/`.
- **Files changed by this follow-up:** `docs/research/097r-open-series-collection.md` (new upload inventory, binary-inspection status and Stata findings); this brief's progress block and follow-up report.
- **New finding:** The Stata file constructs household annual income for 2024 and March 2025 by combining respondent/partner/other-earner income, midpoint-imputing bands and calculating within-wave income deciles. It is not a general codebook; it does not establish availability of saving, consumption, debt, repayments, interest, financial wealth or age. The income deciles are not wealth deciles. The >=£100,000 open-ended band is assigned £125,000, requiring sensitivity treatment if used for aggregate income analysis.
- **Acceptance update:** Author upload requirement **met**. Stata example inspection **met**. ONS workbook extraction, BoE variable inventory and detailed HMRC table extraction remain **not met** because XLSX/ODS contents could not be decoded through the available repository connector/runtime. No values have been guessed.
- **Verification:** Existing saving and financial-stock identities remain as previously recorded. The local `python -I pipeline/check_agent_docs.py` check remains unrun because no local repository checkout/runtime is available here.
- **Branch:** `brief/097r-open-series-collection`. The follow-up commits are on this branch only; not merged.
- **State:** **NEEDS THE AUTHOR / local parsing environment** for the remaining binary extraction and required local check. No model changes or parameter choices.
