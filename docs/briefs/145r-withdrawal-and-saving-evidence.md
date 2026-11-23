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
<!-- progress:start -->
- **Done:** block 0 (note skeletons); block 1 withdrawal (`145r-pension-withdrawal-range.md`, `withdrawal_range.py`); block 2 saving (`145r-saving-gradient-shapes.md`, `saving_shapes.py`)
- **Next:** block 3 change report
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/145-withdrawal-and-saving-evidence origin/brief/145-withdrawal-and-saving-evidence`
- **State:** in progress
<!-- progress:end -->
