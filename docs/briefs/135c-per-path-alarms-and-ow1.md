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
`model_v3/runner/arm.py` (budget 310; name any raise), `model_v3/core/revenue.py` only for a bookkeeping fix, `docs/model-v3/household-arm-run/` (`run_grid.py`, `ranges.py`, rerun CSVs), `docs/model-v3/household-arm-paths.md`, `docs/model-v3/architecture.md`, `docs/decisions.md`, tests. Name any further file before editing it. Not the register, the pack, the manifest or the digest fixture.

## Acceptance criteria
- `test_legacy_digest` unchanged; all suites pass; held points and the fixed-rate account CSVs byte-identical.
- OW1 is a marker, not a value, under per-path returns (test on the written CSV).
- Each of the two I1 alarms has a diagnosis; a bookkeeping cause is fixed, an economic one is reported with balances.
- The tie gap is explained or marked not reproducible with the run that was tried.

## Out of scope
The deferral rate (134r), per-path GDP, heterogeneity, saving gradient, withdrawal, validation, any headline number.

## Implementation notes
<!-- progress:start -->
- **Done:** none
- **Next:** block 0
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/135-per-path-alarms origin/brief/135-per-path-alarms`
- **State:** ready; not started (after 133c)
<!-- progress:end -->
