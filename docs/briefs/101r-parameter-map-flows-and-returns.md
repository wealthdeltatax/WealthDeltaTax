# 101: Parameter map, evidence side A: income, saving, consumption, returns and pension flows

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-21
- **Read (all three evidence briefs):** `docs/hypotheses/empirical-household-flow-parameter-map.md` (sections 3 to 8, the classification and deliverables A, B, E); `docs/model-v3/household-flow-plan.md`; `docs/research/094r-kernel-map-and-household-accounts.md` (B1 and B2, the identity and the variable dictionary); `docs/research/096r-cohort-cell-design.md`; the phase 1 notes `095r-*`, `097r-*`, `098r-*`, `099r-*`, `100r-*` in `docs/research/` and the data under `docs/research/data/`; `docs/model-v3/inputs.md` (the rows named in each brief); `docs/agents/research.md` (runtime check first).
- **Depends on:** 097r, 098r, 099r, 100r (merged)

## Goal
Crosswalk the sources and register the parameters for the **flows** of the household account: income, consumption, saving (non-pension and pension), cash yield, holding gains, pension contributions, accrual and decumulation, and the macro aggregates that constrain them. Companion briefs: 102r (stocks, cells and transitions), then 103r (assembly).

## Decisions (author, 2026-11-21)
- Scenario B: cells of wealth band by life stage; saving on the income side; a parameter with no UK evidence is **unset** or a labelled **scenario**; no universal scalar; nothing is chosen for its effect on WDT revenue, fund fill or closure.
- **Pension wealth is inside the WDT base** (DC and DB, on the ONS SCAPE-based basis the pack uses): pension accrual counts as saving; every pension row names its valuation basis; the Resolution Foundation basis is validation context only and is never mixed with it.
- 3.5% (I-D14c) is a legacy comparator only, never evidence.
- Do not average or splice sources whose definitions differ; report the difference.

## Design
1. **Runtime check first.** The brief names held workbooks and CSVs and committed scripts; it needs a local checkout and a shell. If the session has neither, stop and ask.
2. **Source crosswalk (flows).** One row per source used for these variables: ONS quarterly sector accounts and UK Economic Accounts (097r: S.14 allocation of primary income, secondary distribution, use of disposable income, the ONS non-pension and pension saving split, the cash-basis alternative), the ONS national balance sheet revaluations, ONS household final consumption, HMRC personal income tables for property income, interest and dividends by income range, the NMG saving and debt-service variables, the JST split (100r), Bozio and others 2013 (095r), the 099r moments for saving and returns (BF, AB, GB, ZM rows). Columns: exact file, table, sheet or page, series id; publisher and link; reference period; population, unit, frequency, price basis; definitions and coverage; available dimensions; revisions and sampling limits; whether the held file was checked against the published source.
3. **Parameter register rows for:** labour and transfer disposable income; consumption; non-pension saving; pension contributions (employee and employer), accrual, investment return, and withdrawal; retained cash property income; cash yield and holding gain by asset class (100r); nominal-liability revaluation; the national-account aggregates that constrain these (saving ratio, property income, revaluations); the legacy I-D14c row classed legacy; and the existing rows I-D1a, I-D1a2, I-W1c, I-W3a to I-W3d. Columns: variable and definition; accounting location; target cell dimension; classification (observed, derived, proxy, scenario, unset); source and exact reference (file, table or sheet, series id or page); calculation, with the formula and the script that runs it; value or range **only where supported**; uncertainty and caveats; intended model use (calibration, validation only, or neither); proposed ruling (ready for implementation, implement with a scenario range, remain unset, further data required); open question or data request. An unset row has no number. Where a register row exists, say whether the new row supports, contradicts or reclassifies it.
4. **Existing-row audit.** For I-W3a to I-W3d (saving by wealth, including the "gross saving rate of the top 1%" row) and I-W1c: what each is, whether its source supports the definition and population, and the classification the evidence gives. Report disagreements; do not edit the register.
5. **Reproducible calculations.** Every derived value (for example the pension and non-pension saving shares, a cash-yield share of total return, retained property income as a share of the aggregate) is computed by a script under `docs/research/data/101r/` that reads the held files, with its output CSV and the tolerance against the source figure.
6. **Flow-side constraints.** Compare aggregate household flows with the account constraints where definitions permit (for example the saving identity of 097r), and report any difference as definitional, coverage, timing or measurement; do not average incompatible measures.
7. Append **data requests** for this side to the unresolved list in the note (exact table, file or series, the parameter it informs, whether the model can proceed unset or on a labelled scenario).

## Touches
`docs/research/101r-parameter-map-flows-and-returns.md` (new: crosswalk and register for the flows), `docs/research/data/101r/` (new: `flows_register.csv`, `flows_crosswalk.csv`, derivation scripts and outputs), this brief's progress block, `docs/agents/friction-log.md`. No register, code, pack or manifest edits.

## Acceptance criteria
- Every variable group of item 3 has rows; every row has a definition, accounting location, classification, exact source reference and intended use.
- Every observed or derived value reproduces from a committed script, tolerance stated and met.
- Every proxy states why and its sensitivity need; every unset row states the consequence for implementation.
- Pension rows state their valuation basis; none mixes the two pension bases.
- No value is chosen with regard to WDT revenue; no new central rate for consumption, saving or depletion appears.
- `git diff --stat` limited to Touches.

## Checks to run
`python -I pipeline/check_agent_docs.py`; each derivation script run once from a clean checkout.

## Out of scope
Stocks, wealth bands, stage weights, transitions and debt (102r); assembly, pension-basis check across both sides, the full unresolved list and rulings (103r); register, pack or code edits; any model run.

## Open questions
None.

**Session limits.** This brief is sized for one session but may not fit. Work in blocks (one source group or one variable group at a time); after each block run its script, append its rows to the register CSV, commit and push the branch, and update the progress block. If you run out, the next agent resumes from the branch. Never hold finished work unpushed.

## Implementation notes
<!-- progress:start -->
- **Done:** blocks 1 and 2 by Agent 3 (ONS, JST, HMRC scripts; register and crosswalk CSVs). Blocks 3 to 6: note `docs/research/101r-parameter-map-flows-and-returns.md` (summary, basis, crosswalk, register view, existing-row audit, flow-side constraints, data requests DR-01 to DR-09, reproduction list); F-29 caveat wording and the pension-basis labels on F-11 to F-13 fixed in the build script; friction-log entry added.
- **Next:** guru review; then 102r (stocks, cells, debt) and 103r (assembly, which merges the data requests).
- **Decisions:** none beyond the author's 2026-11-21 decisions.
- **Gotchas:** the clone tracks main only; fetch the branch by name. The four I-W3 rows have four different denominators and are not comparable.
- **Resume:** branch `brief/101-parameter-map-flows`; nothing to resume.
- **Not run:** nothing skipped. Source PDFs for I-W1c and I-W3 are not held, so their figures are unverified (DR-09); no model run.
- **State:** done (on the branch, not merged to main)
<!-- progress:end -->
