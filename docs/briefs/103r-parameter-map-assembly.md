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
- **Done:** all blocks. Block 1 merged register and crosswalk with structural checks; block 2 cross-side checks and worked cell; block 3 supply list, rulings and register differences; block 4 summary, friction log, change report. Note: `docs/research/103r-parameter-map-assembly.md`; data and scripts: `docs/research/data/103r/`.
- **Next:** guru review and retire; 104r takes the decisions listed in the note summary.
- **Decisions:** none taken beyond the author's 2026-11-21 decisions.
- **Gotchas:** the clone tracks main only; fetch other branches by name. Flows are on the ONS national-accounts pension basis, the stock on the WAS SCAPE basis.
- **Resume:** nothing to resume.
- **Not run:** nothing skipped. No source re-collected; the 101r and 102r scripts were not re-run (their CSVs are read).
- **State:** done
<!-- progress:end -->

**Change report**
- Task: 103r, parameter map assembly (deliverables A, B, E closing step).
- Files changed: `docs/research/103r-parameter-map-assembly.md` (new note); `docs/research/data/103r/` (new: `merge_and_check.py`, `cross_side_checks.py`, `parameter_register.csv`, `source_crosswalk.csv`, `dictionary_map.csv`, `unresolved_data.csv`, `register_differences.csv`, `cross_side_checks.csv`, `worked_cell_d45.csv`); this brief's progress block; `docs/agents/friction-log.md` (one entry).
- What is different now: one 73-row parameter register and a 25-source crosswalk replace the two; the cross-side consistency checks, a worked cell, a 7-item data-supply list, the rulings with the consequence of each unset row, and a table of differences from the existing register exist for 104r and the author.
- New or changed interfaces: two scripts run with `python -I` from the repository root; no model, register, pack or manifest interface.
- Acceptance criteria: (1) merged register has a row for every one of the 18 094r dictionary terms and every one of the 26 existing register rows named in 101r and 102r, every row classified, no unset row with a value: met, checked by `merge_and_check.py` (0 failures). (2) Items 2 to 5 present with numbers and tolerances: met (14 cross-side checks, section 3; supply list section 4; rulings section 5; differences section 6). (3) No row adjusted or chosen with regard to WDT revenue: met. (4) `git diff --stat` limited to Touches: met (see Verification).
- Deviations from the brief: a sixth classification, "endogenous", for three dictionary rows that are model outputs (friction-log entry); a second script for the numeric checks.
- Risks / follow-ups: the pension flows and stock are on different bases (DR-01); the wealth roll-forward does not close without the non-financial revaluation (DR-05); one imputed-rent claim rests on an ONS methodology page read on the web, not on a held file.
- Instruction friction: one entry added (classification vocabulary for non-parameter dictionary terms).
- Verification: `python -I pipeline/check_agent_docs.py` passes; both scripts re-run from a clean checkout of the branch tip with identical outputs (below).
- Overview sections likely needing an update: none; the guru records the decisions in the note summary (a) to (e).
- Commit / branch: see the final commit on `brief/103`.

