# 104: Parameter map, design side (cell coverage, accounting conventions, public side)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-21
- **Depends on:** 103r (merged)
- **Read:** `docs/hypotheses/empirical-household-flow-parameter-map.md` (sections 4 to 9: the account, the no-double-counting rule, deliverables C and D); `docs/research/103r-parameter-map-assembly.md` and its register; `docs/research/096r-cohort-cell-design.md` (cells, interface gap list, open questions); `docs/research/094r-kernel-map-and-household-accounts.md` (A3 the public side; B3 the worked cases); `docs/research/100r-jst-cash-yield-and-gain-split.md`; `docs/model-v3/architecture.md`.

## Goal
From the 103r register, decide **which cells the evidence supports** and **how the household account is to be built**: the coverage matrix (deliverable C), the accounting conventions (D), and how the state's asset stake, the fund and WDT receipts are made one representation. These are proposals with a recommendation each; the author rules.

## Decisions (author, 2026-11-21)
- Pension accrual: one labelled aggregate scenario on the ONS basis; no rate on the SCAPE stock (SUP-3 pending).
- Classes with no held return (pension, physical, net financial): a labelled scenario range per class, not an estimate.
- Residual O is reported, not forced to zero; survey (WAS) is the stock base, national accounts validation only.
- Two deflators kept and labelled (CPI for real returns; ONS household consumption deflator for liability erosion); list where each is used.
- Apply the label fixes: F-03 is `T_C` not `TR`; F-21 is a `CG` term not `O`; I-W3b is context only. Add physical wealth to the asset list.
- Stage is the person's economic status (held WAS table) as a proxy; the household reference person's status is a data request, not a blocker.
- Physical wealth (contents and vehicles) is inside the WDT base as a separate asset class.
- Scenario B; no universal scalar; nothing chosen for revenue (see 101r).
- **Pension wealth is inside the WDT base.** The account therefore carries pension contributions, employer contributions, accrual, investment return and decumulation; pension wealth is part of net worth and of the assessed base but not liquid cash available to consume or to pay tax before it is drawn. State the consequence for payment and settlement (liquidity), without assuming a rule.

## Design
1. **Cell coverage matrix (C).** For each wealth band of the pack by stage (working, retired; and any further split the data allow), which register rows are observed, derived, proxy, scenario or unset. Mark direct observations, modelled allocations and aggregate constraints separately. Name the **smallest cell structure the data support**, and which splits (for example, a retired cell, a high-wealth cell) are scenarios only. Do not start from a preferred number of cells.
2. **Accounting conventions (D), each as options, consequences and a recommendation:**
   - total return credited to assets with saving defined to exclude the yield already credited, against yield retained as saving with holding gain credited separately (100r and the hypothesis section 4); say what each does to the identity of 094r B4 and to the kernel's growth step;
   - disposable against primary income; consumption and saving definitions; imputed rent;
   - pension contributions, accrual, withdrawals and the valuation basis (ONS SCAPE basis, as the pack; the Resolution Foundation basis is validation context only);
   - nominal cash yield, holding gain and real conversion with the pack's CPI; liability revaluation sign;
   - gifts, inheritances and inter-household transfers (cancel in aggregate; what happens at death, and the legacy heir rule);
   - survey totals against national-account totals (which constrain which);
   - WDT tax timing and settlement, and the payment source for a household whose wealth is mostly pension and housing.
3. **Public-side representation.** 094r found the state's units and the fund's cash flow are two unlinked representations. Propose one: what the household payment becomes (a transfer to the public sector, a fund asset), how the state's stake is valued, and how it reconciles to the household account so that no wealth or income is created.
4. **Interface to v3.** For each convention chosen as the recommendation: the household-step function signature, the pack inputs, the manifest outputs and the tests that would move. Gap list only; no edits. The legacy 3.5% remains a switchable comparator reproducing today's digests.
5. **Rulings table.** For each parameter row: ready for implementation, implement with a scenario range, remain unset, or further data required, with the consequence of the unset rows for the first implementation.
6. **Validation moments.** Which 099r moments validate the untaxed baseline, at which resolution, and the tolerance a pass would need before the comparison is run (plans only).

## Resume (a first agent pushed blocks 0 and 1, then ran out of tokens)
Branch `brief/104` (not `104r`). Fetch and check it out:
`git fetch origin brief/104:refs/remotes/origin/brief/104 && git checkout -b brief/104 origin/brief/104 && git pull --rebase origin main`
(the clone tracks main only; main has since moved: 105c and 106c briefs, rulings in `docs/decisions.md`). On the branch the brief's progress block is accurate: read it, the note `docs/research/104r-parameter-map-design.md` (section 2 is written, 3 to 8 pending) and `docs/research/data/104r/`. Do not redo block 1 (`coverage_matrix.py` and its CSVs); if the brief file conflicts on rebase, keep the branch version and add the Decisions section from main.

Remaining blocks, one push each, filling the note section and the progress block in the same commit (`docs/agents/research.md`, Long data briefs). Print only summary lines from scripts; read CSVs by slice.
- **Block 2: accounting conventions (note section 3, design item 2).** Each convention as options, consequences and one recommendation. Apply the author's rulings above (pension aggregate scenario; scenario range per no-return class; O reported; two deflators, say where each is used; label fixes F-03 and F-21; I-W3b context only; physical wealth added to the asset list). Include the worked D4-5 case from 103r (`worked_cell_d45.csv`) rewritten under the recommended conventions, with the imputed-rent consumption point.
- **Block 3: public side (section 4, item 3).** One representation of the household payment, the state's stake and settlement; 094r's two unlinked representations are the problem statement.
- **Block 4: interface, rulings table, validation moments (sections 5 to 7, items 4 to 6).** Interface is a gap list only (signature, pack inputs, manifest outputs, tests that would move; the LAYER and `test_groups.py` rows for any new module per `docs/agents/code.md`). The rulings table is built from `docs/research/data/103r/parameter_register.csv` (73 rows) plus the author's rulings; it ends with the questions the author must rule on, each with a recommendation first. Validation moments use the 099r set at stated resolution with tolerances, plans only.
- **Block 5: summary (section 1), reproduction (section 8), change report, friction entry; set State to done; push; stop.**

**Stop rule.** After three of these blocks, or when a quarter of the budget is left, write the unfinished sections from what exists (marked "partial" with what is missing), push, list the rest under Next and stop. The author wants the build to start after this brief: prefer a complete short section to a long unfinished one. No more research is wanted: where a number is not held, say unset or scenario, as the register classes do.

## Touches
`docs/research/104r-parameter-map-design.md` (new), this brief's progress block, `docs/agents/friction-log.md`. No code, register, pack or manifest edits.

## Acceptance criteria
- A coverage matrix covering every pack band and both stages, with each cell's evidence class stated.
- Each convention in item 2 has options, consequences for the identity and a recommendation; the no-double-counting rule is shown to hold with a worked case.
- The public-side proposal shows that household payments, the state's stake and the fund reconcile with no created wealth (an identity, with numbers for an illustrative case labelled as such).
- Pension liquidity and valuation basis are stated for the base and for settlement.
- The rulings table covers every register row of 103r; no row is given a value the evidence does not support.
- No parameter or option is chosen for its effect on WDT revenue or closure.

## Checks to run
`python -I pipeline/check_agent_docs.py`.

## Out of scope
Any code, pack, register or manifest edit; running the model; calibration; a replacement for 3.5%.

## Open questions
None.

## Implementation notes

Change report
- Task: brief 104r, parameter map, design side
- Files changed: `docs/research/104r-parameter-map-design.md` (note, sections 1 to 8); `docs/research/data/104r/` (scripts and CSVs for coverage, conventions, public side, rulings); this brief; `docs/agents/friction-log.md`.
- What is different now: a design note with a cell coverage matrix, accounting conventions with a worked case, a public-ledger proposal with an illustrative identity, an interface gap list, a 73-row rulings table and a validation plan. Proposals only.
- New or changed interfaces: none.
- Acceptance criteria: coverage matrix covers every band and both stages (met); each convention has options, consequences and a recommendation, with a worked no-double-counting case (met); public-side identity with illustrative numbers, labelled (met); pension liquidity and valuation basis stated for base and settlement (met); rulings table covers all 73 rows with no unsupported values (met); nothing chosen for WDT revenue or closure (met).
- Deviations from the brief: none. The 102r branch was superseded and not merged.
- Risks / follow-ups: nine author questions in section 6; DR-01 (pension bases) open; joint band-by-stage cross-tab needed (S06); band persistence moments cannot be tested without a transition rule.
- Instruction friction: one entry added to the friction log.
- Verification: `check_agent_docs.py` and the four scripts run clean (`ok:` lines); no model run.
- Overview sections likely needing an update: none until the author rules.
- Commit / branch: brief/104
<!-- progress:start -->
- **Done:** block 4 (note sections 5 to 7, `rulings_table.py`). Blocks 0 and 1 (note skeleton; coverage matrix, section 2). Block 3: section 4 public ledger with `public_side_identity.py`. Block 2: note section 3 (accounting conventions 3.1 to 3.8) with `conventions_worked.py` and four CSVs in `docs/research/data/104r/`.
- **Next:** author rules on the nine questions in note section 6.
- **Decisions:** recommended A (credit holding gain, saving carries retained yield once) with B as equivalent check; disposable-income basis; no cross-cell transfers in the first implementation; settlement source left to the author.
- **Gotchas:** branch is `brief/104`; the clone tracks main only. Do not pipe `git push`.
- **Resume:** branch `brief/104`; read this block and the note; section 4 onward pending.
- **Not run:** nothing; checks pass.
- **State:** done
<!-- progress:end -->
