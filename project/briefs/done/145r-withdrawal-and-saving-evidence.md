# 145: Evidence for two scenario axes: pension withdrawal by age, and saving by wealth

- **Status:** ready (research only; can start now; feeds 147c and 148c)
- **Author/date:** K. Ogata with the guru, 2026-11-23
- **Depends on:** 129r (merged), 131r (merged)
- **Read (block 0: the first two only):** (1) `docs/research/129r-was-access-audit.md` and `docs/research/data/129r/feasibility_map.csv` (the drawdown and saving rows); (2) `docs/agents/research.md`. Later: the specific PDFs in `docs/research/data/129r/` the audit names (IFS/ELSA drawdown; Resolution Foundation "Before the Fall"; ONS tables), opened through `pipeline/to_markdown.py`, only the pages you cite; `docs/model-v3/household-arm-validation.md` (BF-13, the concentration gap); `docs/model-v3/inputs.md` (I-D1j, the saving inputs).

## Goal
Two labelled scenario axes need evidence before any code: (1) **pension withdrawal** (the pension is never drawn in life today; a ruling made it a mandatory labelled sensitivity before long-run claims), and (2) a **saving gradient** (one saving ratio for every line collapses concentration: top-decile share 0.41 to 0.20 to 0.34 against 0.50 observed). Read the held sources and say what they support, in a form the code briefs can take over. No new data collection, no UKDS licence.

## Decisions (author, 2026-11-23)
- Every figure has a page or figure reference and a flag (`text`, `table`, `read from chart`); every proposed rate has an evidence class (`derived`, `proxy`, `scenario`, `unset`) and a challenge note. Scenario values are labelled as such, never a forecast, no central value.
- Withdrawal: low / mid / high rates by age band, wealthier faster where the source says so; the draw is from the pension into non-pension wealth, the pension staying in the assessed base while held. Where the held sources give no rate by age band, say so and propose the nearest labelled statement or mark `unset`.
- Saving gradient: three shapes, `flat` (today, default), `mild` and `steep`: the saving ratio by decile and by tail line, scaled so aggregate saving equals `flat`'s (state the scaling). Not tuned to reach 0.50; the note may say how each shape would be expected to move concentration but computes nothing in the model.
- Sources not held are listed, not fetched and not guessed.

## Blocks (one push each; `docs/agents/research.md`)
- **Block 0:** progress block pushed.
- **Block 1: withdrawal.** `docs/research/145r-pension-withdrawal-range.md` and `docs/research/data/145r/withdrawal_range.csv`: published drawdown figures (page, flag), the proposed low / mid / high by age band (the model's stages), what stays `unset`, and the challenge note. Push.
- **Block 2: saving.** `docs/research/145r-saving-gradient-shapes.md` and `docs/research/data/145r/saving_shapes.csv`: what the held sources say about saving by wealth band (page, flag), the `mild` and `steep` ratio by decile and tail line, the aggregate-saving scaling, what is `unset`. Push.
- **Block 3:** change report; push; stop.
**Stop rule.** No model, register or manifest change. After three blocks or a quarter of the budget left, push and list the rest.

## Touches
New: `docs/research/145r-*.md`, `docs/research/data/145r/`. Not `model_v3/`, the register, the pack or the manifest.

## Acceptance criteria
- Every figure has a page and flag; each proposed rate or ratio has an evidence class and challenge note; `unset` parts are listed.
- Withdrawal rates exist by the model's age stages, or the gap is stated; saving shapes exist for the 14 lines (decile lines and the tail), scaled to the `flat` aggregate.
- Nothing outside `docs/research/` changes; `python -I pipeline/check_agent_docs.py` exits 0.

## Out of scope
Any code, any register row, per-path GDP and the top tail (146r), any headline number.

## Implementation notes
Change report
- Task: brief 145r, evidence for two scenario axes (pension withdrawal by stage; saving gradient shapes)
- Files changed: `docs/research/145r-pension-withdrawal-range.md`, `docs/research/145r-saving-gradient-shapes.md` (notes); `docs/research/data/145r/` (`withdrawal_range.py` and `.csv`, `saving_shapes.py`, `saving_shapes.csv`, `saving_evidence.csv`); this brief's progress block; `docs/agents/friction-log.md`.
- What is different now: the held sources contain no pension withdrawal rate and no UK saving rate by wealth band. The nearest statements are proposed as labelled scenarios: a withdrawal range for the retired stage by wealth half (bottom half low 0.0 / mid 0.7 / high 2.9, top half 0.8 / 2.4 / 4.1 % of the pension balance a year; class `proxy`, floor `scenario`) from IFS BN236 on financial wealth; and three saving shapes over the 14 lines (flat, mild, steep) with additive offsets that keep aggregate saving equal to flat's at each flat value.
- New or changed interfaces: none.
- Acceptance criteria: every figure has a page and flag, each rate or ratio an evidence class and a challenge note, unset parts listed (met; BN236 and RF figures asserted on their PDF pages by the scripts); withdrawal by the model's stages (met for the retired stage; the not retired stage and any age profile are stated `unset`); saving shapes for the 14 lines scaled to flat (met, aggregate equality checked to 1e-12 at min, median and max); nothing outside docs changes and `check_agent_docs.py` exits 0 (met).
- Deviations from the brief: none. The saving scaling is additive, not multiplicative, because the flat value can be negative; stated in the note as an author choice.
- Risks / follow-ups: the withdrawal range is a proxy from a different asset and period (financial wealth, ELSA 2002-2015); the saving magnitudes have no UK by-wealth evidence; the Norwegian rows are read from the register, source not held. Data requests: ELSA waves after 2014-15 and pension variables (UKDS), any post-2015 drawdown series, WAS longitudinal microdata. For 147c and 148c: map ELSA halves to D1-5 and D6-10 and the retired stage as the note states.
- Instruction friction: one entry added to the friction log.
- Verification: `withdrawal_range.py` ok (24 rows), `saving_shapes.py` ok (42 and 9 rows; a deliberately wrong RF figure was rejected), `check_agent_docs.py` rc 0. No model run.
- Overview sections likely needing an update: none.
- Commit / branch: brief/145-withdrawal-and-saving-evidence; brief 145 merged, ready to retire (if merged below).
<!-- progress:start -->
- **Done:** block 0 (note skeletons); block 1 withdrawal (`145r-pension-withdrawal-range.md`, `withdrawal_range.py`); block 2 saving (`145r-saving-gradient-shapes.md`, `saving_shapes.py`)
- **Next:** none; guru reviews
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/145-withdrawal-and-saving-evidence origin/brief/145-withdrawal-and-saving-evidence`
- **State:** done
<!-- progress:end -->
