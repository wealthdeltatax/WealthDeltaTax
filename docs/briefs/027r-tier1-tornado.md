# 027: Research: tier 1 tornado on the revenue identity

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** 012r and 022r to 024r (merged into `docs/model-v3/inputs.md`, 260 rows)
- **Read:** `docs/agents/research.md`; `docs/model-v3/drivers.md` sections 1, 2 and 4; `docs/model-v3/metrics.md` (M1, M1a to M1e, M2, M3, M4a definitions); `docs/model-v3/inputs.md` rows named below. Nothing else need be opened.

## Goal
Show which inputs move the headline results most, before model stage C is designed, so stage C spends its effort where the uncertainty is. The result is `docs/model-v3/tornado.md`.

## Decisions (author, 2026-11-16)
- The tornado runs the identity `M1a ≈ ε · g · ω − refunds`, one input at a time over its low and high (`drivers.md` section 1), on paper or in a small script. It is not a model run.
- A tier 2 input that moves M1 by less than 0.5 points of GDP stays at its single range (cut-off confirmed).
- It also backs out `ε · g · ω` against v2's post-fill WDT of 7.34% of GDP (`logistic_ln_ref`, `docs/model-audit/synthesis.md`), as the first number to reconcile.

## Design
1. **Inputs, all rows with a low and a high.** Tier 1: D4 (I-D4a to I-D4e; the wealth base ω), D5 (I-D5a to I-D5d; behavioural response and valuation), D6 (I-D6*; incidence of retired taxes), D9 (I-D9*; non-payers and thresholds), D10 (I-D10a to I-D10c; capitalisation), D1 (I-D1a to I-D1e; return, volatility, loss years). Tier 2: D7 (I-D7*), D8 (I-D8*), D11 (I-D11*), the corporate levy base.
2. **Outputs.** M1 (revenue, % of GDP), M2 (burden, % of wealth, overall), M4a (non-payer savings, % of tax bill, overall), M3 (gains, real change in net wealth). Where the identity cannot reach an output (M4a, M3 for some inputs), say so and report the direction only.
3. **One input at a time**, others at central. Report for each input and output: low result, central, high result, swing, rank. Draw one tornado per output (a table sorted by swing is enough; a chart in a Data-style reference table is welcome, no prose claims beyond ranking).
4. **Apply the cut-off.** List each tier 2 input and whether it moves M1 by 0.5 points of GDP or more. Those below stay at one range.
5. **Back out ε · g · ω** at central inputs and set it beside v2's 7.34%; state the gap and its likely sources from the register, without fitting parameters to close it.
6. **State what the identity cannot do:** interactions between inputs (for example g and the loss-year share), the refund term, and the retirement order. Note which input pairs are likely to interact, for stage C.
7. **Stock-wealth floor:** no work in this brief. Do not add the stock tax.

## Touches
`docs/model-v3/tornado.md` (new), `docs/model-v3/tornado/` (new; optional script and CSV), this brief's progress block. Nothing in `inputs.md`, `drivers.md`, `metrics.md`, `outputs.yml`, `source/`, `pipeline/`, `model_v1/`, `model_v2/`.

## Acceptance criteria
- Every tier 1 and tier 2 input with a range appears with low, central, high and swing on at least M1.
- Tornado ordering for M1, M2, M4a and M3 is shown, or the output is marked not reachable with the reason.
- The 0.5-point cut-off is applied and listed.
- The ε · g · ω back-out against 7.34% is shown with its arithmetic.
- Every number traces to a register row id; a number that does not is labelled assumption.
- `git diff --stat` shows only the Touches list.

## Checks to run
Recompute the central M1 and two swings by hand or a second method. Script (if any) runs with `python -I`.

## Out of scope
Choosing values, editing the register, running model v1 or v2, the stock-wealth floor, behavioural modelling.

## Open questions
Ask rather than guess, for example if a register row's unit does not map to a term of the identity.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:**
<!-- progress:end -->
