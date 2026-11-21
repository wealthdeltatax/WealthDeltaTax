# 102: Parameter map, evidence side B: stocks, stage weights, debt, transfers and mobility

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-21
- **Read (all three evidence briefs):** `docs/hypotheses/empirical-household-flow-parameter-map.md` (sections 3 to 8, the classification and deliverables A, B, E); `docs/model-v3/household-flow-plan.md`; `docs/research/094r-kernel-map-and-household-accounts.md` (B1 and B2, the identity and the variable dictionary); `docs/research/096r-cohort-cell-design.md`; the phase 1 notes `095r-*`, `097r-*`, `098r-*`, `099r-*`, `100r-*` in `docs/research/` and the data under `docs/research/data/`; `docs/model-v3/inputs.md` (the rows named in each brief); `docs/agents/research.md` (runtime check first).
- **Depends on:** 097r, 098r, 099r, 100r (merged); runs in parallel with 101r

## Goal
Crosswalk the sources and register the parameters for the **stocks and structure** of the household account: wealth bands, stage weights, asset and liability composition, debt, transfers and the transitions between bands and stages. Companion briefs: 101r (flows and returns), then 103r (assembly).

## Decisions (author, 2026-11-21)
- Scenario B: cells of wealth band by life stage; saving on the income side; a parameter with no UK evidence is **unset** or a labelled **scenario**; no universal scalar; nothing is chosen for its effect on WDT revenue, fund fill or closure.
- **Pension wealth is inside the WDT base** (DC and DB, on the ONS SCAPE-based basis the pack uses): pension accrual counts as saving; every pension row names its valuation basis; the Resolution Foundation basis is validation context only and is never mixed with it.
- 3.5% (I-D14c) is a legacy comparator only, never evidence.
- Do not average or splice sources whose definitions differ; report the difference.

## Design
1. **Runtime check first.** The brief names held workbooks and CSVs and committed scripts; it needs a local checkout and a shell. If the session has neither, stop and ask.
2. **Source crosswalk (stocks and structure).** One row per source used: the WAS published tables and the 098r derived files (households by wealth band, persons by age and by activity by band, composition by age, debt by age and region, the band-edge mapping and reconciliation, the stage by WDT band derived table), the pack's `wealth_distribution.csv`, the ONS population and mortality files (098r), the ETB income by decile for retired and non-retired households, the ONS national balance sheet household stocks (097r), the 099r moments for mobility, composition and top-tail (BF, AB, TZ, EER, TD rows), and the pension valuation breaks (Round 7 against Round 8; Resolution Foundation against ONS). Columns as in 101r.
3. **Parameter register rows for:** wealth-band definitions and edges against the pack's bands; the stage weights by band (working, retired, the economically inactive not retired; the definition used and what the tables can and cannot support); asset composition by band and stage (property, financial, DB and DC pension, other); liabilities (secured, unsecured) and debt service; the top-tail adjustments; transfers (gifts, inheritances, estates at death, the legacy heir rule); mobility between bands and stages (the 099r summary measures only; no full matrix exists); demographic transitions (working to retired, death, household formation; ONS hazards from 098r); household to person weights; and the existing rows I-D4a to I-D4h, I-W4a to I-W4f and I-W5a to I-W5e. Columns: variable and definition; accounting location; target cell dimension; classification (observed, derived, proxy, scenario, unset); source and exact reference (file, table or sheet, series id or page); calculation, with the formula and the script that runs it; value or range **only where supported**; uncertainty and caveats; intended model use (calibration, validation only, or neither); proposed ruling (ready for implementation, implement with a scenario range, remain unset, further data required); open question or data request. An unset row has no number. Where a register row exists, say whether the new row supports, contradicts or reclassifies it.
4. **Existing-row audit.** For I-D4a (wealth to GDP, 5.94 against the pack's 6.14), I-D4b (adults per household, 1.77 against I-D4h 1.93), and I-W4 and I-W5: what the evidence supports, with the numbers and the classification; report disagreements, do not edit the register.
5. **Cell coverage inputs.** For each pack band by stage, list which structure rows are observed, derived, proxy or unset, and the cell size (households, persons) the held tables allow, so 104r can build the coverage matrix. Do not build the matrix itself.
6. **Reproducible calculations.** Every derived value (band reconciliation, stage weights by band, composition shares, a person to household weight, transition hazards) is computed by a script under `docs/research/data/102r/` that reads the held files, with its output CSV and the tolerance against the source.
7. Append **data requests** for this side to the unresolved list in the note (exact table, file or series, the parameter it informs, whether the model can proceed unset or on a labelled scenario, the access route: UK Data Service WAS study 7215, ELSA, ONS request).

## Touches
`docs/research/102r-parameter-map-stocks-and-cells.md` (new: crosswalk and register for the stocks and structure), `docs/research/data/102r/` (new: `stocks_register.csv`, `stocks_crosswalk.csv`, derivation scripts and outputs), this brief's progress block, `docs/agents/friction-log.md`. No register, code, pack or manifest edits.

## Acceptance criteria
- Every variable group of item 3 has rows with definition, accounting location, classification, exact source reference and intended use.
- Every observed or derived value reproduces from a committed script, tolerance stated and met.
- Every proxy states why and its sensitivity need; every unset row states the consequence for implementation.
- Pension stock rows state their valuation basis; none mixes the two pension bases.
- The band reconciliation to the pack shows its mismatch where bands do not align; no cell value is built by spreading an aggregate in proportion to wealth.
- No value is chosen with regard to WDT revenue.
- `git diff --stat` limited to Touches.

## Checks to run
`python -I pipeline/check_agent_docs.py`; each derivation script run once from a clean checkout.

## Out of scope
Flows, returns and saving (101r); assembly and rulings (103r); the coverage matrix itself (104r); register, pack or code edits; any model run.

## Open questions
None.

**Session limits.** This brief is sized for one session but may not fit. Work in blocks (one source group or one variable group at a time); after each block run its script, append its rows to the register CSV, commit and push the branch, and update the progress block. If you run out, the next agent resumes from the branch. Never hold finished work unpushed.

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
