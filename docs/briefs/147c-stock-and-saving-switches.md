# 147: Two household-arm scenario switches on the starting position: the top-tail stock and the saving gradient

- **Status:** ready (code; after 139c and the evidence in 145r and 146r; touches `arm.py`)
- **Author/date:** K. Ogata with the guru, 2026-11-23
- **Depends on:** 119c, 124c, 125c (merged), 139c, 145r (merged, accepted), 146r (top-tail mapping)
- **Read (block 0: the first two only):** (1) `docs/research/146r-top-tail-mapping.md` and `docs/research/145r-saving-gradient-shapes.md`; (2) `docs/agents/code.md`. Later: `docs/model-v3/household-arm-validation.md` (BF-13); `docs/model-v3/household-arm-account.md`; `model_v3/runner/arm.py` (opening stock, `pension_cap`, `sav`); `docs/model-v3/household-arm-run/run_grid.py`.

## Goal
Two labelled switches, both off by default, so every existing output is byte-identical until they are used. (1) `top_tail` (`off`, `ast_low`, `ast_high`): scale the opening stock of the top-1% line D10b to the published top-1% share (14.4% and 16.5%, Advani, Summers and Tarrant). **The pack's own top 1% is 21.9%, so these settings LOWER the top stock** (by 1,069bn and 770bn); the Rich List tiers stay at 784bn and the removed wealth goes to D10a, so total wealth and the top-decile share (43.5%) are unchanged (146r recommended mapping, accepted). A second pair of settings, `ast_low_e0` and `ast_high_e0`, repeats this with I-D4e at 0% (pack top 1% 18.0%). (2) `saving_shape` (`flat`, `mild`, `steep`): the saving ratio by line from the 145r shapes, scaled to the same aggregate saving as `flat`. Then report what each does to concentration and to the outputs.

## Decisions (author, 2026-11-23)
- 146r rulings: downward stock sensitivity accepted; D10b only (list fixed), offset to D10a; also with I-D4e at 0%. Where D10a receives wealth it is non-pension only; the reduced line keeps its capped pension; `line_state` builds class balances from wealth times D10's class shares, so the adjustment applies after the composition step (146r section 4).
- Scenarios, not measurements and not fitted: nothing is tuned to reach the observed 0.50 top-decile share; report what each setting gives and say it is a range. Tail behaviour (saving, returns, pension accrual) stays `unset` and unchanged under `top_tail`.
- The mapping and the shapes are those the research notes propose; where a note lists an open ruling, stop and report for the author before building that part.
- Added tail wealth is non-pension; the I-D1l ceiling holds; total wealth and offsets as the note states.
- Default off: `test_legacy_digest`, the legacy arm and all household outputs byte-identical; no register row (the later register brief).

## Blocks (one push each; `docs/agents/code.md`)
- **Block 0:** progress block pushed.
- **Block 1: `top_tail`.** The switch, tests (off: byte-identical; on: total wealth as stated, I1 and the account identity hold, the year-0 top-1% share equals the published value within tolerance). Push.
- **Block 2: `saving_shape`.** The switch, tests (`flat` byte-identical; aggregate saving equal across shapes within tolerance; I1 and the account identity hold). Push.
- **Block 3: rerun and note.** Five grid points, 20 paths, every top_tail setting crossed with the three saving shapes: top-decile and top-1% share by year (1, 10, 30, 100), BF-13 and its gap, M1a and M2 as ranges, shortfall lines, lien balances. `household-arm-validation.md` updated: the range against 0.50, **no fitting, no headline number**. Change report; push; stop.
**Stop rule.** A kernel change is stop-and-report. After three blocks or a quarter of the budget left, push and list the rest. Suites in the background, never piped.

## Touches
`model_v3/runner/arm.py` is at 329 of its 330 lines (137c; the old 'budget 310' is stale): new scenario-switch code goes in the new `model_v3/runner/switches.py` (budget 200, a new file; `arm.py` gains call sites only, or shrinks); any growth of `arm.py` past 330 is stop-and-report, `docs/model-v3/household-arm-validation.md` and its CSVs, `docs/model-v3/household-arm-run/` (`run_grid.py`), tests. Not the kernel, the register, the pack, the manifest or the digest fixture.

## Acceptance criteria
- Both switches off: all suites pass, all outputs byte-identical; `test_legacy_digest` unchanged.
- With them on, I1, the account identity and the ledger ties hold at all five points.
- The note reports concentration under each setting against 0.50 and says each is a labelled scenario with no fitted value.

## Out of scope
Tail behaviour, withdrawal, GDP paths (148c), the register rows, any headline number.

## Implementation notes
<!-- progress:start -->
- **Done:** none
- **Next:** block 0
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/147-stock-saving-switches origin/brief/147-stock-saving-switches`
- **State:** ready; not started (after 139c, 145r, 146r)
<!-- progress:end -->
