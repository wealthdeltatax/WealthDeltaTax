# 104: Parameter map, design side (cell coverage, accounting conventions, public side)

- **Status:** hold
- **Author/date:** K. Ogata with the guru, 2026-11-21
- **Depends on:** 103r (reported and reviewed)
- **Read:** `docs/hypotheses/empirical-household-flow-parameter-map.md` (sections 4 to 9: the account, the no-double-counting rule, deliverables C and D); `docs/research/103r-parameter-map-assembly.md` and its register; `docs/research/096r-cohort-cell-design.md` (cells, interface gap list, open questions); `docs/research/094r-kernel-map-and-household-accounts.md` (A3 the public side; B3 the worked cases); `docs/research/100r-jst-cash-yield-and-gain-split.md`; `docs/model-v3/architecture.md`.

## Goal
From the 103r register, decide **which cells the evidence supports** and **how the household account is to be built**: the coverage matrix (deliverable C), the accounting conventions (D), and how the state's asset stake, the fund and WDT receipts are made one representation. These are proposals with a recommendation each; the author rules.

## Decisions (author, 2026-11-21)
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
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** hold; waits for 103r
<!-- progress:end -->
