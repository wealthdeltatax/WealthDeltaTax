# 143: Per-path GDP growth in the household arm: a labelled scenario axis

- **Status:** ready (after 142c: touches `arm.py`, the grid and the paths note)
- **Author/date:** K. Ogata with the guru, 2026-11-23
- **Depends on:** 128c (merged), 135c, 138c, 142c
- **Read (block 0: the first two only):** (1) `docs/model-v3/household-arm-paths.md` (what varies per path and what is fixed; GDP growth fixed); (2) `docs/agents/code.md`. Later: `model_v3/core/revenue.py` (`gdp_growth`, where GDP enters the ratios and the fund); `model_v3/runner/arm.py` (the per-path switch `paths`, `dv`); `docs/model-v3/household-arm-comparators.md` (M15a/b "envelope never binds"); the pack's `gdp_pc` series and the return generator (register I-D1a to I-D1g).

## Goal
In the household arm every path has the same real GDP growth (0.0157 a year, the pack series), so the fund-to-GDP ratios, the burden shares and M15a/b (the envelope never binds in the 20 smoke cells) carry no growth risk. Add a labelled **per-path GDP growth** axis: growth varies around the scenario rate by path, with the same JST-based machinery as the market-return paths (128c), so the two can be run alone or together. Off by default.

## Decisions (author, 2026-11-23)
- A scenario axis, labelled "growth risk only"; no central case and no forecast. Default off (`gdp_paths` false): every existing output byte-identical.
- The growth shock follows 128c's pattern: scenario rate plus a per-path deviation, loading and any correlation with the market return stated, with the evidence class and challenge note. Use the held JST series and the register rows already there (the AR(1) parameters for returns); if the pack has no growth-spread or growth-return correlation row, say so, mark it `unset`, and offer the labelled options (independent / the historic correlation from the held JST data) rather than choose silently; the author rules.
- Property, physical and the fund's safe stand-in stay as 128c has them; only the GDP index (denominator) and the income and saving that scale with GDP per head move with the path. State exactly which quantities scale.
- The fixed-rate account and legacy arm stay byte-identical; `test_legacy_digest` unchanged.

## Blocks (one push each; `docs/agents/code.md`)
- **Block 0:** progress block pushed.
- **Block 1: design and evidence.** A short section in `household-arm-paths.md`: what GDP growth touches in the hook and ledger (income, saving, the denominators of M1, P6, M15), the proposed deviation process, its parameters from the held JST data (page or table, flag), the correlation options, and what is `unset`. Push; if a correlation choice is open, stop here and report so the author can rule.
- **Block 2: the switch.** `gdp_paths` in the household arm; the per-path growth into the GDP index and income scaling; tests (off: byte-identical; on: I1, the account identity and the ledger ties hold; the mean growth over paths equals the scenario rate within tolerance). Push.
- **Block 3: rerun and note.** Five grid points at 200 paths with `gdp_paths` on, and with market and GDP paths together: checks per point, spread of P6 and M1 across paths, whether M15a/b bind on any path. **No headline number.** Change report; push; stop.
**Stop rule.** A kernel change is stop-and-report. After three blocks or a quarter of the budget left, push and list the rest. Suites in the background, never piped.

## Touches
`model_v3/runner/arm.py` (budget 310; name any raise), `model_v3/core/revenue.py` only if the GDP index must take a path (name the lines), `docs/model-v3/household-arm-run/` (`run_grid.py`), `docs/model-v3/household-arm-paths.md`, tests. Not the kernel, the register, the pack, the manifest or the digest fixture.

## Acceptance criteria
- With `gdp_paths` off all suites pass and all outputs are byte-identical; `test_legacy_digest` unchanged.
- With it on, I1, the account identity and the ledger ties hold at all five points; the note says which quantities scale with the path and what spread results.
- The correlation choice is either ruled or marked open with the options stated.

## Out of scope
The register rows (a later register brief), pension withdrawal and the saving gradient, the top tail, any headline number.

## Implementation notes
<!-- progress:start -->
- **Done:** none
- **Next:** block 0
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/143-per-path-gdp origin/brief/143-per-path-gdp`
- **State:** ready; not started (after 142c)
<!-- progress:end -->
