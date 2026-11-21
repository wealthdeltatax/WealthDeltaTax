# 101: Parameter map, evidence side (source crosswalk, parameter register, unresolved data)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-21
- **Depends on:** 097r, 098r, 099r, 100r (all merged)
- **Read:** `docs/hypotheses/empirical-household-flow-parameter-map.md` (sections 3 to 8: the classification and the deliverables A, B, E; this brief is its evidence side); `docs/model-v3/household-flow-plan.md`; `docs/research/094r-kernel-map-and-household-accounts.md` (B1, B2: the identity and the variable dictionary); `docs/research/096r-cohort-cell-design.md`; the phase 1 notes `docs/research/097r-*`, `098r-*`, `099r-*`, `100r-*`, `095r-*` and the data folders under `docs/research/data/`; `docs/model-v3/inputs.md` rows I-D1*, I-D4*, I-D14c, I-W1* to I-W5* and the section that maps 014g onto them; `docs/agents/research.md` (runtime check first).

## Goal
Turn everything collected in phase 1 into two tables that the design side (102r) and the later code briefs can use: a **source-to-variable crosswalk** and a **parameter register** with one row for every flow, stock, rate, weight or transition of the household account, each classified **observed, derived, proxy, scenario or unset**. Plus the smallest list of data the author still has to supply.

## Decisions (author, 2026-11-21)
- Scenario B: cells of wealth band by life stage; saving on the income side; a parameter with no UK evidence is **unset** or a labelled **scenario**; no universal scalar; nothing is chosen for its effect on WDT revenue, fund fill or closure.
- **Pension wealth is inside the WDT base.** Private pension wealth (DC and DB, on the WAS basis the pack uses) is in the net wealth that is assessed, so pension accrual counts as saving in the household account, and the valuation basis (ONS SCAPE-based, as the pack, against the Resolution Foundation market-annuity basis) matters for the base. Every row that touches pension says which basis it is on.
- 3.5% (I-D14c) is a legacy comparator only. It has a row in the register, classed as legacy, not as evidence.
- Do not average or splice sources whose definitions differ; report the difference (hypothesis section 7D).

## Design
1. **Runtime check first.** The brief names held workbooks and CSVs; it needs a local checkout and a shell. If the session has neither, stop at once and ask (`docs/agents/research.md`).
2. **A. Source-to-variable crosswalk.** One row per source used, from 095r to 100r and the files they hold: exact file, table, sheet or page and series id; publisher and link; reference period and publication date; population, unit, frequency and price basis; definitions and coverage; available dimensions and cross-tabulations; revisions and sampling limits; whether the held file was checked against the published source (and by which note).
3. **B. Parameter register.** One row for each variable of the 094r dictionary (the net-worth identity: net saving from labour and transfer income, retained property income, cash yield, holding gains, consumption, pension contributions, accrual and withdrawals, debt and debt service, transfers and inheritances, taxes, and the stage weights and transitions of 096r), and for every existing register row it replaces or constrains (I-D1a and I-D1a2, I-D4*, I-D14c, I-W1c, I-W3a to I-W3d, I-W4a to I-W4f, I-W5a to I-W5e). Columns: variable and definition; accounting location; target cell dimension; classification; source and exact reference; calculation, with the formula and the file it runs on; value or range **only where supported**; uncertainty and caveats; intended model use (calibration, validation only, or neither); open question or data request. Do not give a number to an unset row. Where a register row exists, say whether the new row supports, contradicts or reclassifies it.
4. **Existing-row audit.** For I-W3a to I-W3d in particular (saving by wealth, including the "gross saving rate of the top 1%" row), say what each is, whether the source supports the definition and population, and the classification the evidence gives. Report disagreements; do not edit the register.
5. **Reproducible calculations.** Every derived value (for example: a pension-excluded saving share from the ONS split, a household to person weight, a stage weight by pack band from 098r) is computed by a script committed under `docs/research/data/101r/` that reads the held files, with its output CSV. State the tolerance against the source figure.
6. **E. Unresolved-data list.** The smallest set of further data the author could supply: exact table, file or series, the parameter it informs, whether the model can proceed without it by leaving the parameter unset or running a labelled scenario, and the access route (097r and 098r section on microdata).
7. **Rulings column.** For each row, a proposed ruling: ready for implementation, implement with a scenario range, remain unset, or further data required. These are proposals; the author rules after 102r.

## Touches
`docs/research/101r-parameter-map-evidence.md` (new: crosswalk, register as a table), `docs/research/data/101r/` (new: `parameter_register.csv`, `source_crosswalk.csv`, derivation scripts and outputs), this brief's progress block, `docs/agents/friction-log.md`. No register, code, pack or manifest edits.

## Acceptance criteria
- Every variable of the 094r dictionary and every register row named in item 3 has a row; every row has a definition, accounting location, classification, source reference and intended use.
- Every observed or derived value reproduces from a committed script, with the tolerance stated and met.
- Every proxy states why and the sensitivity it needs; every unset row states the consequence for implementation.
- Pension rows state their valuation basis; no row mixes the Resolution Foundation and ONS pension bases.
- No row's value is adjusted or chosen with regard to WDT revenue; no new central rate for consumption, saving or depletion appears.
- `git diff --stat` limited to Touches.

## Checks to run
`python -I pipeline/check_agent_docs.py`; each derivation script run once from a clean checkout.

## Out of scope
The cell coverage matrix and the accounting conventions (102r); register, pack or code edits; any model run; new data collection beyond what is already held.

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
