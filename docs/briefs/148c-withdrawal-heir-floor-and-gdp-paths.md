# 148: Three household-arm scenario switches on the flows: pension withdrawal, the heir floor, per-path GDP growth

- **Status:** ready (code; after 147c and the evidence in 145r and 146r; touches `arm.py`, `pension_lien.py`)
- **Author/date:** K. Ogata with the guru, 2026-11-23
- **Depends on:** 132c, 133c, 128c (merged), 139c, 147c, 145r (merged, accepted), 146r (GDP process)
- **Read (block 0: the first two only):** (1) `docs/research/145r-pension-withdrawal-range.md` and `docs/research/146r-gdp-growth-process.md`; (2) `docs/agents/code.md`. Later: `docs/model-v3/household-arm-lien.md`; `docs/model-v3/household-arm-paths.md`; `model_v3/core/pension_lien.py`; `model_v3/runner/arm.py`; `model_v3/core/revenue.py` (`gdp_growth`).

## Goal
Three labelled switches, off by default, so every existing output is byte-identical until used. (1) `pension_withdrawal` (`off`, `low`, `mid`, `high`): a draw from the pension into non-pension wealth by age stage, from the 145r range; the pension stays in the assessed base while held. (2) `heir_floor` (0, 25, 50%): the share of the pension the lien's settlement draw at death cannot take (the base case is uncapped, author ruling 2026-11-23); the unpaid remainder is written off and reported in the ledger. (3) `gdp_paths` (`off`, `indep`, `hist`): per-path real GDP growth `0.0157039 + d`, `d` a zero-mean AR(1) with marginal SD 2.68 points (full sample) and lag-1 0.28, the correlation with the market return 0 (`indep`) or 0.37 (`hist`); household income follows the path (saving and accrual ratios fixed); labelled "growth risk only" (146r, accepted). The postwar SD 1.93 is a noted alternative, not built.

## Decisions (author, 2026-11-22 and 2026-11-23)
- All three are scenarios, never forecasts, with no central value. The pension stays in the base and is never sold in life except under the labelled withdrawal; the lien stays senior and uncapped unless the floor is set.
- GDP process: author rulings 2026-11-23 (146r): both correlations as labelled settings, full-sample SD, income follows the path; the constants are named and labelled in `switches.py` (register rows in a later brief). Anything else the 146r note leaves `unset`: stop and report; do not choose silently.
- Property, physical and the fund's safe stand-in stay as in 128c; only the GDP index and what scales with GDP per head move under `gdp_paths` (146r lists them).
- Default off: `test_legacy_digest`, the legacy arm and all household outputs byte-identical. No register row (the later register brief).

## Blocks (one push each; `docs/agents/code.md`)
- **Block 0:** progress block pushed.
- **Block 1: withdrawal and heir floor.** Both switches (hook and `pension_lien.py`), tests (off: byte-identical; withdrawal on: class total and I1 hold, total wealth unchanged by the draw; floor 0 is today's settlement, 50% leaves half the pension and reports the write-off). Push.
- **Block 2: `gdp_paths`.** The switch; tests (off: byte-identical; on: I1, the account identity and the ledger ties hold; mean growth over paths equals the scenario rate within tolerance). Push.
- **Block 3: rerun and note.** Five grid points: withdrawal low / mid / high and floor 0 / 50% at 20 paths (shortfall lines, lien balances, write-offs, ledger tie); `gdp_paths` at 200 paths alone and with market paths (spread of P6 and M1, whether M15a/b ever bind). Tables in `household-arm-lien.md` and `household-arm-paths.md`. **No headline number.** Change report; push; stop.
**Stop rule.** A kernel change is stop-and-report. After three blocks or a quarter of the budget left, push and list the rest. Suites in the background, never piped.

## Touches
`model_v3/runner/arm.py` is at 329 of its 330 lines (137c; the old 'budget 310' is stale): new scenario-switch code goes in the new `model_v3/runner/switches.py` (budget 200, a new file; `arm.py` gains call sites only, or shrinks); any growth of `arm.py` past 330 is stop-and-report, `model_v3/core/pension_lien.py`, `model_v3/core/revenue.py` only if the GDP index must take a path (name the lines), `docs/model-v3/household-arm-lien.md`, `docs/model-v3/household-arm-paths.md`, `docs/model-v3/household-arm-run/` (`run_grid.py`), tests. Not the kernel, the register, the pack, the manifest or the digest fixture.

## Acceptance criteria
- All three switches off: all suites pass, all outputs byte-identical; `test_legacy_digest` unchanged.
- With them on, I1, the account identity and the ledger ties hold at all five points; floor write-offs are reported.
- The notes say which quantities scale with the GDP path and show the spread, with no headline number.

## Out of scope
The deferral rate, the saving gradient and top tail (147c), the register rows, any headline number.

## Implementation notes
<!-- progress:start -->
- **Done:** none
- **Next:** block 0
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/148-flow-switches origin/brief/148-flow-switches`
- **State:** ready; not started (after 147c, 145r, 146r)
<!-- progress:end -->
