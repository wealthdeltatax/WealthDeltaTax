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
- **Done:** blocks 0 to 4 (all sections of `docs/model-v3/kernel-wiring-design.md`; `kernel-wiring/decile_composition.py` and CSV)
- **Next:** the author rules on section 4.1 (Q1 to Q10); the guru writes W1 to W7 as briefs
- **Decisions:** routes are settlement channels crossed with classes (every route's units carry the line's non-pension mix); pension a balance beside the units; household step through a hook built by the runner (kernel stays numpy-only); one public ledger by class; legacy default and bit-equal to a digest captured first
- **Gotchas:** no stored digest exists in tests or docs, so W1 must capture one before any change; `runner.py` is at its 360-line budget; assessment loses tax if every route delta is non-positive while the pension delta is positive (fallback in W4); M3, M12, M13 are not like for like under the household arm
- **Resume:** branch `brief/112-kernel-wiring-design`; `git fetch origin brief/112-kernel-wiring-design`; last block pushed: 3; first action: block 4
- **Not run:** no code, suites or model runs (docs only); line numbers are those of `origin/main` 16c4493 and were spot-checked, not machine-verified
- **State:** complete; design only
<!-- progress:end -->

```
Change report
- Task: 112r design: wiring the household step into the kernel's payer lines
- Files changed: docs/model-v3/kernel-wiring-design.md (the design note); docs/model-v3/kernel-wiring/decile_composition.py and .csv (decile composition from WAS R8 Table 2.2, sizes the within-band gradient); this brief's progress block
- What is different now: the author has a sectioned design (book as it is, mapping, replacement, build order W1 to W7, ten rulings) for wiring household_step into the kernel; no code, test, register or pack changed
- New or changed interfaces: none (proposed: hook object, signed flow share, apply_payment, arm switch)
- Acceptance criteria: every section answered with file and line references: met (line numbers spot-checked against origin/main 16c4493); build order with three or fewer deliverables per brief and a named review point: met; rulings table recommendation first: met (Q1 to Q10); diff limited to Touches: met
- Deviations from the brief: none
- Risks / follow-ups: no stored legacy digest exists (W1 captures it); runner.py has no line headroom (Q7); M3, M12, M13 withheld under the household arm (Q5); the return ranges for pension, net financial and physical stay author-set
- Instruction friction: none
- Verification: python -I pipeline/check_agent_docs.py passes; decile_composition.py runs (10 deciles; largest within-band gap 7.07 pp). Not run: any suite or model
- Overview sections likely needing an update: model-v3 household-flow plan (phase 3 now has a build order W1 to W7)
- Commit / branch: brief/112-kernel-wiring-design
```
