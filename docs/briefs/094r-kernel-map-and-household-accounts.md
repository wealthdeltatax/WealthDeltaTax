# 094: Map the v3 kernel and specify accounting-consistent household accounts (tests A and B)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-20
- **Depends on:** 093r (merged)
- **Read:** `docs/research/093r-consumption-depletion-evidence.md` (sections 1, 3, 4); `docs/hypotheses/household-consumption-and-wealth-replenishment.md` (sections 10 to 14); `model_v3/core/kernel.py` (`grow_and_consume`, the return paths, the WDT and fund steps); `model_v3/core/`, `model_v3/runner/`, `model_v3/pack/GBR/` as needed; `docs/model-v3/inputs.md` (I-D14c, I-D1a, I-D10b, I-W3a to I-W3d); `docs/model-v3/outputs.yml`; archived `docs/archive/briefs/080r-declared-alpha-evidence.md` (research-note form).

## Goal
Two pieces of design work before any model change. (A) State exactly what the kernel does today with I-D14c, returns, WDT payments, pensions, liabilities and transfers, and which outputs depend on 3.5%. (B) Specify the household accounts that would replace the universal proportional drawdown, with a variable dictionary and a demonstration that nothing is double-counted.

## Decisions (author, 2026-11-20)
- **3.5% is abandoned as the central consumption or depletion assumption.** It was a judgement device (v2 decision D16), not a UK measurement (093r). It stays only as a labelled **legacy comparator** to reproduce historical outputs.
- **No replacement scalar.** Do not propose 0%, 1.5%, 2.5% or any universal rate as the new value, and do not call any single rate empirically grounded.
- Nothing is chosen because it improves or worsens WDT's fiscal closure. A better fiscal result is not evidence of a better model, and a worse one is not evidence against it.
- No code, register, manifest, schedule, retirement-rule or fund-rule change comes from this brief. Implementation is a later brief, after the author reviews the design (096r) and authorises it.

## Design
### A. Map the existing kernel (read only)
1. Where I-D14c enters (`grow_and_consume`, lever, pack mapping), the form `W[t+1] = W[t](1+g)(1-c)`, and what it does to units, to the base and to each route.
2. How returns are credited: cash income, capital gains or one total return (I-D1a, 4.74 real arithmetic). State whether any term exists for cash income apart from gains, and whether the kernel has any income, saving or consumption flow.
3. How WDT payments leave private wealth, and whether the matching public or fund asset is represented (the fund, its return, the retirement rule). State where WDT sits relative to c in the order of steps.
4. Whether pensions, liabilities, gifts and bequests exist in the kernel or the pack, and in what form (v2's `heir_rule`, D6, D20).
5. A table of **outputs and prior results that depend on 3.5%**: every manifest id and every committed number or report (083c, 090c, 093r) that moves with c, and how (directly, through the base, through feasibility). This is the inventory that lets them be labelled "legacy".
6. Which inputs a flow model would need that the pack does not hold (income by band, consumption, liabilities, age, pension wealth), as a gap list with the pack file nearest each.

### B. Specify the household accounts
1. The identity: `NW = Assets - Liabilities` and `dNW = S + CG + TR + O - T_WDT` (hypothesis section 13), with the accounting rules of the hypothesis section 12 taken as given.
2. A flow-of-funds diagram (a Mermaid or table form that renders in the repo) and a **variable dictionary**. For each term: meaning, sign, stock or flow, source and data definition, status (endogenous, calibrated, externally specified or judgement), the term it could overlap with, and its treatment in nominal and in real terms.
3. A worked demonstration, with numbers for one illustrative household (labelled illustrative, not data), that these cases do not double-count: selling an asset and holding the cash; consuming the proceeds; borrowing to consume; debt interest and repayment; pension contribution, accrual and pension asset; cash income against capital gain when a total return is credited; a gift between two modelled households (cancels in aggregate); WDT paid (a transfer to the fund, not consumption).
4. How the kernel's total return maps in: say how `S` is defined so retained cash income enters once, and what `r = y + g_h` implies for the kernel's growth step.
5. Boundary statement: partial equilibrium, with GDP, labour income and returns specified outside; what is and is not closed against firms, government and the rest of the world.

## Touches
`docs/research/094r-kernel-map-and-household-accounts.md` (new), this brief's progress block, `docs/agents/friction-log.md`. No code, register or manifest edits.

## Acceptance criteria
- Every claim in part A cites a file and line or a committed result; each item 1 to 6 is answered or marked "not represented".
- The dependence table lists every output and prior result that moves with c, with the mechanism.
- The variable dictionary covers every term of the identity with the columns in B2, and the worked demonstration covers each case in B3 with the arithmetic shown.
- 3.5% is described as legacy comparator only; no scalar is proposed for any band or overall.
- `git diff --stat` limited to Touches.

## Checks to run
`python -I pipeline/check_agent_docs.py`. The guru checks part A against the code before review.

## Out of scope
Evidence on UK flows (095r); cohort cells and any calibration (096r); backcasting and WDT comparisons (later briefs); any model change.

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
