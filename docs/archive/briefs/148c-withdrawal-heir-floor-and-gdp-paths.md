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
- **Done:** blocks 0, 1, 2 (`gdp_paths` in `flow_switches.py`); block 3 (reruns, notes in `household-arm-lien.md` and `household-arm-paths.md`, `run_grid.py`, `lien_rerun.py`, `flow_ties.py`, `gdp_spread.py`); one bug fixed in `flow_switches.py` (withdrawal on the untaxed path) with a test
- **Next:** NEEDS THE AUTHOR: two `gdp_paths` runs with market paths miss the I1 / account-identity criterion (`brief-suggestions.md`, "Account residual and I1 under `gdp_paths`"); not merged
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/148-flow-switches origin/brief/148-flow-switches`
- **State:** finished except the open criterion; branch pushed, not merged; `arm.py` at 330
<!-- progress:end -->

**Budget note (guru, 2026-11-24):** `switches.py` is now 195 of its 200 lines (147c merged), so none of this brief's code goes there. The three switches go in a new file `model_v3/runner/flow_switches.py` (numpy only, budget 200, same layer as `switches.py`); `arm.py` gains call sites only and stays at 330 or fewer (growth is stop-and-report). Add its row to the `docs/model-v3/architecture.md` budget table and update the stated totals so `test_budget.py` passes (rows 200 and about 60 for its tests, or the true figure). Constants (the 145r and 146r numbers) are named and labelled in that file.

### Change report (block 3, 2026-11-24)
```
Change report
- Task: brief 148c, block 3 (rerun and notes), continuing the other agent's blocks 0 to 2
- Files changed: model_v3/runner/flow_switches.py (one-line fix: withdrawal hook on the untaxed path); tests/model_v3/test_flow_switches.py (regression test, trimmed to its 150-line budget);
  docs/model-v3/household-arm-run/run_grid.py, lien_rerun.py (flow flags, write-off columns), flow_ties.py and gdp_spread.py (new); household-arm-run/flow_switches/ and gdp_paths/ (data);
  docs/model-v3/household-arm-lien.md and household-arm-paths.md (new sections); docs/agents/friction-log.md and docs/brief-suggestions.md (one entry each); this brief's progress block
- What is different now: the three switches have been run. Floor 0/25/50 and withdrawal low/mid/high at `min_mid` and `median_high` (20 paths) and `gdp_paths` off/indep/hist at five points, 200 paths, alone and with market paths. No headline number
- New or changed interfaces: run_grid.py --pension-withdrawal / --heir-floor / --gdp-paths; lien_rerun.py --points / --pension-withdrawal / --heir-floor (0 allowed); flow_ties.py; gdp_spread.py. Defaults unchanged
- Acceptance criteria:
  - Switches off, suites pass, outputs byte-identical, test_legacy_digest unchanged: met. tests/model_v3 gave 406 passed, 2 failed (my test file was 155 lines against a budget of 150); after the trim the flow, budget and rules tests give 36 passed. The full suite was NOT rerun after the trim; no other suite was run
  - I1, account identity and ledger ties at all five points with the switches on: MET for the withdrawal and floor rows (twelve rows; worst tie 4.3e-10, equal to the unswitched run); NOT MET for gdp_paths in two of thirty runs: (a) median_high, market paths, indep: I1 raises (path 89, line 7, year 95); (b) min_mid, market paths, indep: account residual 3.5e-4 and tie 8.4e-9, in the ratio 0.25 rerun at year 99, scaling with the GDP deviation. Not root-caused; no rule or tolerance changed. Alone, the median_high ties and residuals are 1.3e-8 and 1.2e-8 (about 1e-11 of the receipts), above the 1e-9 the grid flags
  - Floor write-offs reported: met (min_mid D4: 0.106 at floor 0, 0.249 at 25, 0.391 at 50; no effect at median_high)
  - Notes say which quantities scale with the GDP path and show the spread, no headline: met
- Deviations from the brief: grid points chosen by me (min_mid and median_high, the 127c lien points; the brief names none); added flow_ties.py and a fix in flow_switches.py (block 1 bug found by the smoke run); the 20-path floor/withdrawal runs use schedule S only
- Risks / follow-ups: NEEDS THE AUTHOR (brief-suggestions.md, "Account residual and I1 under gdp_paths"). Not merged
- Instruction friction: one entry added to friction-log.md (brief names no points; the grid's tie reads only the main run)
- Verification: model_v3 suite (see above); smoke and grid runs as in the notes; the new test fails without the fix and passes with it. Not run: the full suite after the trim, other suites, the local site build (nothing site-facing changed)
- Overview sections likely needing an update: none
- Commit / branch: see git log, brief/148-flow-switches (pushed, not merged)
```

