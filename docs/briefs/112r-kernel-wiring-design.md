# 112: Design: wiring the household step into the kernel's payer lines

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 108c, 110c, 111c (merged)
- **Read (block 0: the first two only):** (1) `docs/research/104r-parameter-map-design.md` sections 3, 4 and 5 (conventions, public side, interface gaps); (2) `docs/model-v3/architecture.md` sections 2 and 5.1 (modules, layers, the payer-line book). Later, by block: `model_v3/core/kernel.py` (`grow_and_consume`, the book, routes, lien, `_move`); `model_v3/core/household.py`, `cells.py`; `model_v3/runner/runner.py` and `revenue.py`, `burden.py`, `support.py` (the five sites of `(1+g)(1-c)`); `docs/model-v3/cell-baseline.md` (the "Rerun" section only); `docs/decisions.md` (settlement, convention, public ledger rulings).

## Goal
A design note, no code, that says exactly how `household_step` replaces the kernel's `W(1+g)(1-c)` growth-and-consumption inside the payer-line book, so that the next code briefs are small, ordered and testable, and the legacy arm still reproduces every existing digest.

## Decisions (author, 2026-11-21 and 2026-11-22)
Convention A. Settlement by the existing routes: the payment is taken pro rata across the non-pension classes; pension is never sold; Route D keeps its lien. One public ledger by class at market value, with the fund return read from it. Stage within band is the person-based proxy. Pension accrual is D.8 over B.6g applied to income (I-D1k), accepted as the net national flow for now; withdrawal is a later labelled scenario. Pension, net financial and physical returns are the scenario ranges I-D1h to I-D1j. The legacy 3.5% arm stays as a switch.

## Blocks (one push each; `docs/agents/research.md`, Long data briefs)
- **Block 0:** skeleton of `docs/model-v3/kernel-wiring-design.md` (every section pending) and the progress block; push before reading anything but the first two Read items.
- **Block 1: the book as it is.** What a payer line carries today (wealth by route, weight, cohort, income ratios); where growth, consumption, death, revenue and the lien act on it; the five sites of `(1+g)(1-c)` with file and line; which outputs and digests depend on each. A table. No proposals yet.
- **Block 2: the mapping.** How a payer line maps to a cell (band, stage) and carries a class mix, an income and a saving share, given that a line is a point in the wealth distribution inside a band, not a band mean. Offer options with consequences and one recommendation for: income and class mix of a line within its band (for example proportional to the band mean, to wealth, or a labelled scenario), the saving share, and the pension class for a line (units versus a class balance). State what evidence exists for each and what is a scenario.
- **Block 3: the replacement.** Where `household_step` is called, how routes and classes reconcile (the book's units `f`, `s`, `V` against class positions: is a route a class, or does a route hold a class mix), how the lien and `_move` take payment pro rata from non-pension classes, how the public ledger is read, and the legacy switch with the test that proves the digests do not move.
- **Block 4: the build order.** The code briefs that follow, each with deliverables (three or fewer), Touches, size against the budget, tests and the point where the author reviews numbers; plus the author's rulings table (each question with a recommendation first). Summary at the top; set State; change report; push; stop.
**Stop rule.** After three blocks, or when a quarter of the budget is left, write the remaining sections as "partial" from what exists, push, list the rest under Next and stop. Print only summary lines from scripts; read files by slice.

## Design (what the note must answer)
1. What breaks, and what does not, when growth plus consumption becomes an account with income, saving and class returns?
2. Is the payer line the right unit for cells, and what must be added to it (names, not code)?
3. Which existing tests, digests and pins move under the new arm, and which must stay fixed under legacy?
4. What the public ledger replaces in `revenue.py`, `support.py` and the fund recursion, and the tying test.
5. What is still unset and blocks a taxed run, with the scenario that stands in for it.

## Touches
New: `docs/model-v3/kernel-wiring-design.md`, optional small scripts and CSVs under `docs/model-v3/kernel-wiring/`. No change to any model, test, register or pack file.

## Acceptance criteria
- Every section above answered with file and line references; options have consequences and one recommendation.
- The build order lists briefs with three or fewer deliverables each and a named review point.
- A rulings table for the author, recommendation first.
- Diff limited to Touches.

## Checks to run
`python -I pipeline/check_agent_docs.py`. No suites needed (docs only).

## Out of scope
Any code, register or pack change; validation against moments; withdrawal or a saving gradient (list them as later scenario briefs).

## Open questions
Left to the note.

## Implementation notes
<!-- progress:start -->
- **Done:** blocks 0 to 2 (sections 1 and 2 of `docs/model-v3/kernel-wiring-design.md`; `kernel-wiring/decile_composition.py` and CSV)
- **Next:** block 3 (the replacement: routes against classes, lien and `_move`, public ledger, legacy switch and test), block 4 (build order, rulings, summary, change report)
- **Decisions:**
- **Gotchas:**
- **Resume:** branch `brief/112-kernel-wiring-design`; `git fetch origin brief/112-kernel-wiring-design`; last block pushed: 2; first action: block 3
- **Not run:**
- **State:** in progress, block 2 pushed
<!-- progress:end -->
