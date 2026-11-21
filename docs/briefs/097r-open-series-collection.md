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
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
