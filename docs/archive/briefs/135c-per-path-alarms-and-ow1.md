# 135: Close the per-path loose ends: OW1 under per-path returns, the two I1 alarms, the ledger tie gap

- **Status:** ready (after 133c merges: both touch the hook and the kernel cap)
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 128c (merged), 133c (merged)
- **Read (block 0: the first two only):** (1) `docs/model-v3/household-arm-paths.md` ("Odd" items 1 to 4 and the I1 alarms); (2) `docs/agents/code.md`. Later: `docs/model-v3/household-arm-run/run_grid.py`; `model_v3/runner/arm.py` (`withheld`, `_pay`, the I1 check); `model_v3/core/revenue.py` (the ledger tie).

## Goal
128c left four things unexplained or unapplied. Close them without changing economics: (1) OW1 is listed as `legacy_only` under per-path returns but the grid writer still writes its values; (2) `min_mid` (path 9, line 3, year 96: family value -0.077135, class total -0.0723546, a gap of 0.0048) and `median_high` (path 34, line 8, year 81: family 0, class total 1.285e-09, balances exhausted) raise I1 on one path each; (3) a ledger tie gap of 167 bn in a 20-path smoke run at `min_mid` (years 62 and 85, path 18), not reproduced at 1,000 paths because I1 fails first; (4) the refund routing in `_pay` the author accepted (2026-11-22): document it as a settlement rule in the architecture note and `decisions.md`.

## Decisions (author, 2026-11-22)
- 128c is merged with `revenue.py` line 146 and the refund routing accepted. No other rule changes here.
- The two I1 alarms are diagnosed before anything is changed: say for each whether it is a **tolerance** (the `median_high` residual is 1.3e-9 against the check's tolerance), a **bookkeeping** disagreement (the 0.0048 gap) or **economics**. Fix only bookkeeping; report the rest. No result is forced to pass.
- Under per-path returns OW1 is **withheld** like any `legacy_only` output (a labelled marker, never the value).
- Passing grid points and the fixed-rate arm stay byte-identical; `test_legacy_digest` unchanged.

## Blocks (one push each; `docs/agents/code.md`)
- **Block 0:** progress block pushed.
- **Block 1: diagnose.** A two-case table (and the tie gap) in `docs/model-v3/household-arm-paths.md`: point, path, line, year, balances, kernel value, which rule, tolerance, bookkeeping or economics. Reproduce the 20-path tie gap at `min_mid` and name its cause or say it is not reproducible. Push.
- **Block 2: fixes.** OW1 withheld in the grid writer and `ranges.py` under `--market-paths` (test); any bookkeeping fix the diagnosis supports, with a test that the failing path now closes and the held points are byte-identical; the refund-routing rule written in `docs/model-v3/architecture.md` and `decisions.md`. Push.
- **Block 3: rerun and note.** Rerun the five points at 200 paths with the 133c lien in place; update the note: checks per point, which alarms remain with their balances. **No headline number.** Change report; push; stop.
**Stop rule.** A kernel change is stop-and-report (133c owns the kernel cap). After three blocks or a quarter of the budget left, push and list the rest. Suites in the background, never piped.

## Touches
`model_v3/runner/arm.py` is at 329 of its 330 lines (137c; the old 'budget 310' is stale): new scenario-switch code goes in the new `model_v3/runner/switches.py` (budget 200, a new file; `arm.py` gains call sites only, or shrinks); any growth of `arm.py` past 330 is stop-and-report, `model_v3/core/revenue.py` only for a bookkeeping fix, `docs/model-v3/household-arm-run/` (`run_grid.py`, `ranges.py`, rerun CSVs), `docs/model-v3/household-arm-paths.md`, `docs/model-v3/architecture.md`, `docs/decisions.md`, tests. Name any further file before editing it. Not the register, the pack, the manifest or the digest fixture.

## Acceptance criteria
- `test_legacy_digest` unchanged; all suites pass; held points and the fixed-rate account CSVs byte-identical.
- OW1 is a marker, not a value, under per-path returns (test on the written CSV).
- Each of the two I1 alarms has a diagnosis; a bookkeeping cause is fixed, an economic one is reported with balances.
- The tie gap is explained or marked not reproducible with the run that was tried.

## Out of scope
The deferral rate (134r), per-path GDP, heterogeneity, saving gradient, withdrawal, validation, any headline number.

## Implementation notes
<!-- progress:start -->
- **Done:** blocks 0 to 3 (branch from main f706c83); all pushed
- **Next:** author decision on the 1e-9 to 5e-8 I1 residuals (kernel cap tolerance, 133c)
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/135-per-path-alarms origin/brief/135-per-path-alarms`
- **State:** complete, not merged: NEEDS THE AUTHOR
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 135c, close the per-path loose ends (OW1, the two I1 alarms, the ledger tie gap)
- Files changed: model_v3/runner/arm.py (330 lines, the architecture.md budget; `_restart` sets a wiped line's units exactly); docs/model-v3/household-arm-run/run_grid.py and ranges.py (OW1 marker under --market-paths); the three *_paths.csv (200-path rerun); docs/model-v3/household-arm-paths.md (diagnosis, rerun); architecture.md (refund routing rule); decisions.md; tests (test_household_tax.py, test_run_grid.py)
- What is different now: OW1 is the marker `withheld (legacy_only)` under per-path returns, never a value. A third I1 case (median_high path 69, line 7, year 96, diff 1.1e-3) was bookkeeping (units near 1e18 after a settlement rescale lost the 137c restart in rounding) and is fixed. The refund routing is written as a settlement rule.
- New or changed interfaces: none (the written rows of a per-path run carry the marker in a, b, c and summary `withheld`)
- Acceptance criteria: test_legacy_digest unchanged and all 10 suites pass (met); fixed-rate held points equal in every shared cell (1,308 cells, 0 differ) and their CSVs not rewritten (met); OW1 marker with a test on the written CSV (met); each alarm diagnosed (met: both named alarms and 10 more are 1.0e-9 to 5.0e-8 residuals at the kernel cap's 1e-9 tolerance, family 0 against class total -(PL-PK), pension 8 to 57: tolerance, not fixed; one bookkeeping case fixed with a failing-then-passing test); tie gap (met: not reproducible, 20 paths min_mid seed 1, tie 1.8e-12)
- Deviations from the brief: held points compared by cell against a fresh run, since the committed fixed-rate CSV predates 150 later ids. The tolerance residuals are left, not tuned. median_high still raises I1 at 200 paths and min_mid at 1,000, so median_high has no rows in the rerun.
- Risks / follow-ups: the cap (133c, kernel) leaves up to 5e-8 of unit part on a line the floor holds at 0; the author decides between loosening the check to the cap's tolerance and a cap that hands over the whole excess. min_mid unpaid_B 3.02 on 2,638 path-phases (pension cannot cover the lien).
- Instruction friction: none
- Verification: python pipeline/run_suites.py 10 of 10 passed; new tests fail without the fix; run_grid --market-paths --paths 200; 20-path min_mid tie check
- Overview sections likely needing an update: household arm per-path note; decisions
- Commit / branch: brief/135-per-path-alarms; NEEDS THE AUTHOR, not merged
```
