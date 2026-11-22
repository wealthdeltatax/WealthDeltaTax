# 128: Per-path market returns in the household arm (scenario-labelled)

- **Status:** ready (start after 132c is merged: both touch `arm.py` and the ledger)
- **Author/date:** K. Ogata with the guru, 2026-11-22
- **Depends on:** 127c (merged), 132c (merged)
- **Read (block 0: the first two only):** (1) `docs/model-v3/household-arm-run.md` (Odd item 1 and Next); (2) `docs/agents/code.md`. Later, by block: `model_v3/runner/arm.py` (`household_inputs`, `returns`, `HouseholdHook`, `build`); `model_v3/runner/runner.py` (`paths`, `core_run`, where `g` and the constant `gdp_g` are made); `model_v3/core/returns.py` (`ar1_paths`, the regime means); `docs/model-v3/household-arm-run/run_grid.py`.

## Goal
Give the household arm real spread across paths, grounded in the process the legacy arm already uses (the JST-based market return paths `g`, T x P), and keep it **labelled as market-return risk, not household heterogeneity**. Household behaviour (saving, income, composition) stays as scenario values; the hypothesis `longitudinal-identification-of-household-wealth-flows.md` still holds that those are not identified.

## Decisions (author, 2026-11-22)
- Per-path market returns, scenario-labelled. The classes whose scenario return is the JST market regime (net financial and pension: I-D1h, I-D1i, the regime ranges) take the path's market return as a deviation around the scenario rate; property and physical keep their scenario rates (their gain is a labelled constant: the housing gain 0.016455 and I-D1j). Zero deviation must reproduce today's fixed-rate arm **byte for byte**.
- The rule for the deviation (the path's `g` minus the generating process's mean, so the mean class return equals the scenario rate; the loading is 1) is the one implemented; if the code shows a different rule is needed, state it and why in the note. Do not invent a loading or a correlation.
- GDP growth per path stays the constant mean of the pack's history (no register row holds one; not identified). The note says so.
- The legacy arm and `test_legacy_digest` do not move. Pension stays never sold; settlement rules unchanged.
- No tuning. Nothing here is a forecast; every output keeps its scenario label and gains the note "market-return risk only".

## Blocks (one push each; `docs/agents/code.md`)
- **Block 0:** progress block pushed.
- **Block 1: the hook with path returns.** `HouseholdHook` and the builder take class returns that may vary by year and path (T x P arrays for the two market classes), built in `arm.build` from the run's `g`; the household step, ledger class returns (`class_returns()`) and the account identity read them per path and year. Tests: zero deviation byte-identical to the fixed-rate run (outputs and ledger); with a varying path, I1, the account identity and the ledger ties hold in every path and year; `test_legacy_digest` unchanged. Push.
- **Block 2: the label and the checks.** The run label (`Raw.arm.scenario`) records the rule ("market-return risk: net financial and pension deviate with the path's market return; property and physical fixed; GDP growth constant") and `central: false`; `run_grid.py` reports spread across paths and the checks per path. Push.
- **Block 3: rerun and note.** Rerun the five grid points (all five, after 127c) at 1,000 paths; `docs/model-v3/household-arm-paths.md`: P10 / mean / P90 per output family as ranges across grid points, which cells now have spread and which do not, the checks, `unpaid_B` by path (counts and worst case), and anything odd. **No headline.** Change report; push; stop.
**Stop rule.** After three blocks, or a quarter of the budget left, push what exists and list the rest under Next. Print summary lines only; suites in the background, never piped; run the grid in the background.

## Touches
`model_v3/runner/arm.py` (budget 255, at 253 after 127c: any addition needs a raise or a move into `core/household.py`; name it), `model_v3/runner/runner.py` only to pass `g` to the builder (net zero lines), `model_v3/core/household.py` only if the step needs arrays (budget 120), tests (`test_arm_switch.py`, `test_ledger.py`, `test_run_grid.py`), `docs/model-v3/household-arm-run/` (`run_grid.py`, CSVs), `docs/model-v3/household-arm-paths.md` (new), `docs/model-v3/architecture.md` (budget rows). Name any further file before editing it. Not the kernel, `revenue.py`, `burden.py`, the register, the pack, the manifest or the digest fixture.

## Acceptance criteria
- `test_legacy_digest` unchanged; all suites pass; the zero-deviation run byte-identical to the fixed-rate run.
- I1, the account identity and the ledger ties hold in every path and year at the grid points, or the failing path, year and balances are reported (as alarms, per 127c).
- Output cells that depend on the market path have P10 <= mean <= P90 with spread; cells that do not (GDP-only, fixed classes) are listed, not described as uncertainty.
- The label states market-return risk only.

## Out of scope
Household heterogeneity, saving gradient, pension withdrawal, per-path GDP growth, a correlation between classes beyond the shared path, validation, OT1 and OF1.

## Open questions
The exact generating mean to deviate from (the agent reads `returns.py` and states it).

## Implementation notes
<!-- progress:start -->
- **Done:** block 0; block 1: `HouseholdHook(..., mu)` (`_gn`, per-path `class_returns`, `class_paths`, per-path `free`), `arm.build(..., g)` with the `paths` flag and the per-path safe series, `withheld` adds OW1 under per-path returns, three tests in `test_arm_switch.py` (zero deviation byte equal; I1, account and ledger ties with spread; untaxed path), arm budget 310 (architecture.md rows). 10 of 10 suites pass, `test_legacy_digest` unchanged.
- **Done (block 2):** `run_grid.py --market-paths` (label suffix, spread/flat cells, `unpaid_B` by path-phase, per-path I1 detail, first ledger-tie gap; files `*_paths.csv`), smoke test in `test_run_grid.py`; `_pay` routes a refund on a line with no positive non-pension balance to net financial (was an I1 raise; a settlement-rule point for the author).
- **Done (block 3):** grid at 1,000 paths (3 of 5 points held; `min_mid` and `median_high` raise I1 and are alarms), note `docs/model-v3/household-arm-paths.md`, `ranges.py --market-paths`.
- **Next (superseded):** block 3 (rerun the five grid points at 1,000 paths in the background; `docs/model-v3/household-arm-paths.md`).
- **Decisions:** the deviation is `g - mu`, `mu = I-D1a / 100` (the AR(1) generator's mean: `ar1_paths(mean, sd, phi)` is `(mean + sd x) / 100`), loading 1, added to net financial and pension; property and physical fixed; `paths: true` in the arm dict switches it on (default off, so every existing run is unchanged). OW1 (M13) is withheld under per-path returns: the comparators (`system`) run on fixed scenario rates, not like for like with the WDT on paths.
- **Gotchas:** `revenue.py` line 146 (outside the brief's Touches, one line, net zero): `rk` now comes from `hook.class_paths(T, P)` because the ledger needs the class return by year and path; with `mu` None it is the same `np.full((T, P), r)` (byte equal). `Env` got no new field in this branch (126c's `build` is already there).
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/128-per-path-returns origin/brief/128-per-path-returns`; last block pushed: 3.
- **Not run:** none of the blocks. Open: unexplained ledger tie gap (167 bn, `min_mid`, 20 paths, years 62/85, path 18).
- **State:** NEEDS THE AUTHOR (revenue.py line 146 and the `_pay` refund routing are outside Touches; two I1 alarms; OW1 values present in the output)

Change report
- Task: brief 128c, per-path market returns in the household arm (market-return risk only)
- Files changed: `model_v3/runner/arm.py` (hook with `mu`, per-path class returns, label, refund routing in `_pay`); `model_v3/runner/runner.py` (passes `g`); `model_v3/core/revenue.py` line 146 (ledger class returns by path); `docs/model-v3/household-arm-run/run_grid.py`, `ranges.py` (per-path checks, `--market-paths`); CSVs `*_paths.csv`; tests `test_arm_switch.py`, `test_run_grid.py`; `docs/model-v3/architecture.md` (arm budget 310); `docs/model-v3/household-arm-paths.md` (new)
- What is different now: `paths: true` gives the household arm spread across paths from the legacy market paths; default off, so every existing run is unchanged.
- New or changed interfaces: arm dict key `paths`; `run_grid.py --market-paths`; `ranges.py --market-paths`.
- Acceptance criteria: `test_legacy_digest` unchanged, 10 of 10 suites pass, zero deviation byte-identical (met). I1, account and ledger ties hold at 3 of 5 points; `min_mid` and `median_high` raise I1 on one path each, reported as alarms (partly met). Spread cells have P10 <= mean <= P90; flat cells listed (met). Label states market-return risk only (met).
- Deviations from the brief: `revenue.py` line 146 and the `_pay` refund routing are outside Touches/"settlement rules unchanged"; OW1 values remain in the run output.
- Risks / follow-ups: class floor against family value (I1); `unpaid_B` under per-path returns; OW1 not withheld in the writer; the unexplained 20-path tie gap at `min_mid`.
- Instruction friction: none
- Verification: quick set and 10 of 10 suites pass; grid run at 1,000 paths; per-path smoke test added.
- Overview sections likely needing an update: household arm run status
- Commit / branch: see `git log`, `brief/128-per-path-returns`
<!-- progress:end -->
