# 074: Diagnose the remaining I1 and I2 gap (one v2 input at a time)

- **Status:** done, awaiting the author
- **Author/date:** K. Ogata with the guru, 2026-11-19
- **Depends on:** 052c on branch `brief/052c-rework` (this brief continues on that branch), 073c (merged)
- **Read:** the 052c progress block on `brief/052c-rework` (I1 5.02, I2 4.97, register tail 4.62, realised eps 12.3% against 24.5%, start-state wealth-weighted rate 22.9%); `docs/model-v3/architecture.md` section 230 to 232 (I1, I2); `docs/model-v3/tornado.md` section 4 (how 24.5% was backed out); `model_v2/WDT_Params.toml` lines 700 to 760 (`logistic_ln_ref`, `body_split = 5`, `body_split_from = 0.5`, `wmin_house_ratio`) and the v2 scenario's other settings; `model_v2/RATES/rates_core.py` `_build_advani` and the body-split builder (specification only; v2 is not run or imported); `synthesis.md` section 10 (where 7.34 is recorded).

## Goal
A table that says, for each difference between the v3 test environment and v2's `logistic_ln_ref` run, how many points of GDP it moves the I1 number, so the author can decide the fix on evidence. No fix is made in this brief.

## Candidate differences (check each; add any you find)
1. **Body split:** v2 splits the body into finer cells (`body_split = 5` from 0.5) so W_min falls inside a decile; v3 lines are decile means, so a decile with a mean below W_min pays nothing though part of it is above.
2. **Wealth over GDP:** v2's calibrated total against v3's pack-based 6.44 (and the 1.05 add-on).
3. **W_min:** half the median house price per adult: v2's value and basis against the pack's.
4. **Returns:** v2's JST sample and window rule against the pack's `returns.csv` (same 117 windows? same mean?).
5. **GDP growth and indexation** of the threshold (`gdp_pc`), the death phases, G, and the fund settings (v2's levy fund against none: 3.58 against 3.50 already seen).
6. **Definition of the take:** "post-fill 10-year individual WDT take" in v2 against what the test measures (units received or cash, gross of refunds, the levy and fund share), and the 24.5% eps definition (gross g) against the realised 12.3%.

## Design
1. On the rework branch, in the agent's scratchpad (not committed), run the I1 environment from the test, then change one thing at a time toward v2's value where v2's value can be written from its toml or from `tornado.md`; where v2's value cannot be recovered without running v2, say so and give the v3 sensitivity instead (do not run v2).
2. Record each swap's I1 result and the change from 5.02. Then swap all that were recoverable together.
3. Write `docs/model-v3/i1-gap.md`: the table, the combined result, the factors not recovered, and a recommended fix for the author with its size (for example: lines to add to the base, a test constant to correct). No change to `revenue.py`, `base.py`, the pack or the register.

## Touches
`docs/model-v3/i1-gap.md` (new), this brief's progress block, the 052c brief's progress block (one line pointing here). Nothing else.

## Acceptance criteria
- `i1-gap.md` has one row per candidate with a number or "not recoverable without running v2" and the reason.
- The sum of the recovered effects is compared with the 2.3-point gap and the remainder stated.
- `git diff --stat` limited to the Touches list; `pytest tests/model_v3 -q` unchanged (153 passed, 2 xfailed).

## Checks to run
`pytest tests/model_v3 -q`.

## Out of scope
Any model change, the xfail marks, merging 052c, tuning.

## Open questions
If a swap needs a v2 number that is in neither the toml nor `tornado.md`, say so; do not run v2.

## Implementation notes
<!-- progress:start -->
- **Done:** `docs/model-v3/i1-gap.md` written: one row per candidate, combined swap, remainder, recommended fix. Scratch scripts only (not committed). No model, pack, register or test change.
- **Next:** the author rules on the recommended fix (test constants from v2; v2 per-window output for the last 0.68).
- **Decisions:** v2 cell grid rewritten from the spec with toml constants (not checked against a v2 printout); take read net of refunds as in the test.
- **Gotchas:** recovered 1.64 of the 2.32 gap (71%): v2 distribution, GDP, W_min and `gpc_real` growth give 6.659; remainder 0.68. Returns identical (0.000). Finer cells alone +0.22, so the 052c proposal to split D10a/D10b finer is withdrawn. I2 on the combined base 6.61 passes.
- **Resume:** `git checkout brief/052c-rework`; nothing to rebuild.
- **Not run:** v2 (by rule); the rewritten grid was not compared with a v2 output.
- **State:** done; pushed on `brief/052c-rework`; decision with the author.
<!-- progress:end -->
