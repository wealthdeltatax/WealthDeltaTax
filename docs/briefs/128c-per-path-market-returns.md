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
- **Done:** none
- **Next:** block 0
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/128-per-path-returns origin/brief/128-per-path-returns`
- **State:** ready; not started (after 127c)
<!-- progress:end -->
