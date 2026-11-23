# 144: Top-tail stock sensitivity: scale the top lines' opening wealth to the published range

- **Status:** ready (after 142c; independent of 143c, but both touch `arm.py` so they run in sequence)
- **Author/date:** K. Ogata with the guru, 2026-11-23
- **Depends on:** 119c (merged), 129r (merged), 142c
- **Read (block 0: the first two only):** (1) `docs/research/129r-was-access-audit.md` (the P5 top tail row: Advani, Summers and Tarrant 2025, top 1% share 14.4% to 16.5% across aggregates and sources) and `docs/model-v3/household-arm-validation.md` (BF-13 top-decile share 0.41 against 0.50); (2) `docs/agents/code.md`. Later: `docs/model-v3/inputs.md` rows I-D1l and the tail lines (D10a, D10b, RL3, RL2, RL1); `docs/model-v3/household-arm-account.md` (tail pension shares); `model_v3/runner/arm.py` (opening stock, `pension_cap`); the Rich List input in the pack.

## Goal
The pack has no top-1% row: the tail lines D10a, D10b and the Rich List tiers carry D10's mix with a capped pension, and the top-decile share starts at 0.41 against 0.50 observed. Published top-1% shares differ across sources (Advani, Summers and Tarrant 2025: 14.4% to 16.5% across aggregates and sources). Add a labelled **top-tail sensitivity**: scale the opening stock of the top lines so the top-1% share sits at the low and the high of that published range, measure what it does, and say how far it closes the BF-13 gap. Stock only; off by default.

## Decisions (author, 2026-11-23)
- A stock sensitivity, not behaviour: saving, returns and pension accrual of the tail lines stay `unset` and unchanged (the household arm's existing scenario values); no tail-specific behaviour is invented. Say so in every table.
- Two labelled settings besides the default: `ast_low` (top-1% share 14.4%) and `ast_high` (16.5%); the mapping from the published share to the opening stock of D10a, D10b, RL3 to RL1 (which lines are scaled, and how the extra wealth is offset in the rest of the distribution so total wealth is unchanged, or not) is stated and chosen in block 1 with the alternatives; if two readings are plausible, stop and report for the author's ruling. Nothing is tuned to hit 0.50.
- The tail pension ceiling (I-D1l) is held as is; any wealth added to a tail line is non-pension (stated, labelled); the pension basis scenario (131r) is not combined here.
- Default off: every existing output byte-identical; `test_legacy_digest` unchanged.

## Blocks (one push each; `docs/agents/code.md`)
- **Block 0:** progress block pushed.
- **Block 1: the mapping.** `docs/research/144c-top-tail-mapping.md` and a small CSV: the pack's current top-1% share (from its own lines), the AST range with page and flag, the proposed scaling of the tail lines for `ast_low` and `ast_high`, the offset rule, and the alternatives. Convert the PDF on the fly with `to_markdown.py`; no new sources. Push.
- **Block 2: the switch.** `top_tail` in the household arm (`off`, `ast_low`, `ast_high`); tests (off: byte-identical; on: total wealth as stated, I1 and the account identity hold, the top-1% share at year 0 equals the published value within tolerance). Push.
- **Block 3: rerun and note.** Five grid points, 20 paths, three settings: top-decile and top-1% share by year (1, 10, 30, 100), BF-13 and its gap, M1a and the tail lines' payments and any lien, shortfall lines. `household-arm-validation.md` updated: the range against 0.50, **not fitted, no headline number**. Change report; push; stop.
**Stop rule.** A kernel change is stop-and-report. After three blocks or a quarter of the budget left, push and list the rest. Suites in the background, never piped.

## Touches
`model_v3/runner/arm.py` (budget 310; name any raise), `docs/research/144c-top-tail-mapping.md` and data, `docs/model-v3/household-arm-validation.md` and its CSVs, `docs/model-v3/household-arm-run/` (`run_grid.py`), tests. Not the kernel, the register, the pack, the manifest or the digest fixture.

## Acceptance criteria
- The AST figures carry a page and flag; the mapping and offset rule are stated with alternatives.
- `off` byte-identical; all suites pass; `test_legacy_digest` unchanged.
- The note reports the top-decile and top-1% shares under each setting against 0.50 and says it is a stock sensitivity with tail behaviour `unset`.

## Out of scope
Tail behaviour (saving, returns, pension accrual), the pension basis scenario, withdrawal, per-path GDP, the register rows, any headline number.

## Implementation notes
<!-- progress:start -->
- **Done:** none
- **Next:** block 0
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/144-top-tail origin/brief/144-top-tail`
- **State:** ready; not started (after 142c)
<!-- progress:end -->
