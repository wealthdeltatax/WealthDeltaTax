# 103: Parameter map, assembly: one register, the pension-basis check, unresolved data and proposed rulings

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-21
- **Read (all three evidence briefs):** `docs/hypotheses/empirical-household-flow-parameter-map.md` (sections 3 to 8, the classification and deliverables A, B, E); `docs/model-v3/household-flow-plan.md`; `docs/research/094r-kernel-map-and-household-accounts.md` (B1 and B2, the identity and the variable dictionary); `docs/research/096r-cohort-cell-design.md`; the phase 1 notes `095r-*`, `097r-*`, `098r-*`, `099r-*`, `100r-*` in `docs/research/` and the data under `docs/research/data/`; `docs/model-v3/inputs.md` (the rows named in each brief); `docs/agents/research.md` (runtime check first).
- **Depends on:** 101r and 102r (both reported and reviewed)

## Goal
Merge the two evidence-side registers into one, check consistency across them, and produce the unresolved-data list and the proposed rulings that 104r and the author use. This is the short closing step of deliverables A, B and E.

## Decisions (author, 2026-11-21)
- Stage is the person's economic status (held WAS table) as a proxy; the household reference person's status is a data request, not a blocker.
- Physical wealth (contents and vehicles) is inside the WDT base as a separate asset class.
- Scenario B: cells of wealth band by life stage; saving on the income side; a parameter with no UK evidence is **unset** or a labelled **scenario**; no universal scalar; nothing is chosen for its effect on WDT revenue, fund fill or closure.
- **Pension wealth is inside the WDT base** (DC and DB, on the ONS SCAPE-based basis the pack uses): pension accrual counts as saving; every pension row names its valuation basis; the Resolution Foundation basis is validation context only and is never mixed with it.
- 3.5% (I-D14c) is a legacy comparator only, never evidence.
- Do not average or splice sources whose definitions differ; report the difference.

## Design
1. **Merge** `flows_register.csv` and `stocks_register.csv` into one `parameter_register.csv`, and the two crosswalks into one `source_crosswalk.csv`, under `docs/research/data/103r/`, with a script that does it and checks the merged files (unique variable names, no row without a classification, no unset row with a value).
2. **Consistency checks across the two sides**, each reported with the numbers: every pension row on one stated basis; the cash-yield and holding-gain convention consistent with 100r and unable to double-count (a worked case for one cell); household flows against stocks (opening stock plus flows less revaluations against the closing stock where both exist, to a stated tolerance, differences classed as definitional, coverage, timing or measurement); survey totals against national-account totals; units and price basis (nominal against real, CPI).
3. **Unresolved-data list.** Merge the data requests of 101r and 102r and cut to the smallest set the author could supply: exact table, file or series, the parameter it informs, whether the model can proceed without it (unset or labelled scenario), access route and licence.
4. **Rulings summary.** Count and list the rows by proposed ruling (ready, scenario range, unset, further data) and the consequence of each unset row for the first implementation.
5. **Differences from the existing register.** A single table of the register rows this map supports, contradicts or reclassifies, taken from the 101r and 102r audits; no edits to the register.

## Touches
`docs/research/103r-parameter-map-assembly.md` (new), `docs/research/data/103r/` (new: merged register and crosswalk, the merge and check script), this brief's progress block, `docs/agents/friction-log.md`. No register, code, pack or manifest edits.

## Acceptance criteria
- The merged register has a row for every variable of the 094r dictionary and every existing register row named in 101r and 102r; every row classified; no unset row carries a value.
- Items 2 to 5 are present, with the cross-side checks reported with numbers and tolerances.
- No row is adjusted or chosen with regard to WDT revenue.
- `git diff --stat` limited to Touches.

## Checks to run
`python -I pipeline/check_agent_docs.py`; the merge and check script from a clean checkout.

## Out of scope
New collection or derivation beyond what 101r and 102r delivered (log gaps instead); the coverage matrix and accounting conventions (104r); register, pack or code edits.

## Open questions
None.

**Session limits.** This brief is sized for one session but may not fit. Work in blocks (one source group or one variable group at a time); after each block run its script, append its rows to the register CSV, commit and push the branch, and update the progress block. If you run out, the next agent resumes from the branch. Never hold finished work unpushed.

## Implementation notes
<!-- progress:start -->
- **Done:** block 0 note skeleton; branch cut from origin/main 152d700. Block 1: `merge_and_check.py`, merged register (73 rows), crosswalk (25), dictionary map; note section 2; structural checks pass. Block 2: `cross_side_checks.py`, `cross_side_checks.csv` (14 checks, 4 hard pass), `worked_cell_d45.csv`; `cross_side_flag` column in the register; note section 3. Block 3: supply list (16 requests into 7; `unresolved_data.csv`), rulings summary with the consequence of each unset row, `register_differences.csv` (26 rows), reproduction list; note sections 4 to 7.
- **Next:** block 4: summary (note section 1), friction log, final check, merge decision.
- **Decisions:** none yet.
- **Gotchas:** the clone tracks main only; fetch other branches by name.
- **Resume:** branch `brief/103`; read this block and the note skeleton.
- **Not run:** nothing yet.
- **State:** in progress
<!-- progress:end -->
