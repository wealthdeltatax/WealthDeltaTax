# 110: Untaxed cell baseline run (standalone, not wired into the kernel)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-21
- **Depends on:** 108c, 109c (merged)
- **Read (first block only the first two; read the rest when the block needs it):** (1) `model_v3/core/household.py` and `tests/model_v3/test_household.py`; (2) `docs/research/104r-parameter-map-design.md` section 3 only. Later, by block: pack `model_v3/pack/GBR/` (`cell_weights.csv`, `band_composition.csv`); register rows I-D1a, I-D1h to I-D1k, I-D9a to I-D9d, I-D4h and the growth and GDP rows `runner.py` reads for the legacy run; `docs/research/data/101r/` (JST split by class; the ONS non-pension saving ratio series).

## Goal
Run the ten cells (five pack bands by retired or not) forward for 100 years with **no WDT**, using `household_step` under convention A, and report how aggregate wealth, wealth over GDP and the saving ratio behave against the legacy 3.5% rule. The point is a first look at the baseline the new arm produces. Nothing is tuned to hit a target.

## Decisions (author, 2026-11-21)
- **Saving by cell:** one uniform ratio, no wealth gradient: the ONS non-pension saving ratio out of the cell's income, run at the min, median and max of the observed 1998 to 2025 series. A gradient is a later sensitivity, not part of this run.
- **Income:** band means from I-D9a to I-D9d (D4-5 to D10, all households, per household) for every stage; D1-3 takes the D4-5 low bound; retired cells take a labelled retired fraction of the band income. Use the held ETB or other held table if it gives retired households' income; otherwise 0.6 with range 0.4 to 0.8 as a labelled assumption. Say which, and show the sensitivity to it.
- **Returns:** property from the JST housing split (yield and gain, F-20); pension and net financial from I-D1h and I-D1i (low, mid-point label, high: three runs); physical from I-D1j (0); pension accrual from I-D1k, as an aggregate scenario applied to the pension class. Pension is not sold or drawn in this run (no withdrawal flow yet: state this as a limit).
- Settlement does not arise (T_WDT = 0). Convention A; B as a check on one run.
- The legacy arm comparison uses `household_step(..., convention='legacy')` with c = I-D14c over the same cells.

## Blocks (one push each; `docs/agents/code.md`, Long builds)
- **Block 0:** push the progress block and the skeleton of `docs/model-v3/cell-baseline.md` (sections: units and reconciliation, inputs, runs, findings, limits; all pending). Read nothing else first.
- **Block 1: inputs and units.** The loader that builds the ten cells' inputs from the pack and register, and the units reconciliation (cell income against B.6g, cell wealth against the pack total, per-household or per-person conversion with I-D4h). Test it; fill the note's units section; push. If the gaps are large, report and stop for review before block 2.
- **Block 2: one run.** Mid-point regime, median saving ratio, convention A, 100 years, identity residual test, the legacy arm on the same inputs matching the kernel's legacy path. Fill the runs section for this run; push.
- **Block 3: the grid.** Low, mid, high regimes times min, median, max saving ratios; one B check; the CSVs; summary lines only on screen; push.
- **Block 4: findings.** Write the findings and limits from the CSVs, set State, change report, push; stop.
**Stop rule.** After three blocks, or when a quarter of the budget is left, write the findings from what exists, push, list the rest under Next and stop.

## Resume (blocks 0 and 1 are pushed; block 1 stopped for the author's ruling)
`git fetch origin brief/110-cell-baseline-run:refs/remotes/origin/brief/110-cell-baseline-run && git checkout -b brief/110-cell-baseline-run origin/brief/110-cell-baseline-run && git pull --rebase origin main`. The branch's progress block is accurate; do not redo blocks 0 and 1. If the brief file conflicts on rebase, keep the branch version and add this section.
**Author's ruling on the income gap (2026-11-21):** scale every cell's income by one factor so the total equals ONS B.6g (state the year you match to; the wealth base is 2020 to 2022, I-D9 is at the FYE 2024 level, B.6g is quoted for 2025, so say which year and why, and whether prices need adjusting), keeping the band proportions and the retired split. Label the run aggregate-constrained. Keep the unscaled run as a sensitivity (one extra run, mid regime and median saving). Then blocks 2 to 4 as written.

## Design
1. A standalone module (choose the layer from architecture.md 5.1 and report; it imports `household` and the pack/register readers, and the kernel imports nothing from it) and a script that writes a table per run: cell, year, positions by class, `dNW`, `S`, `CG` (with the erosion wedge line), `O`, and the aggregate (sum over cells weighted by persons or households: state which and the conversion with I-D4h).
2. **Units first.** State the units of income, wealth and weights and reconcile: the sum of cell income against ONS B.6g and of cell wealth against the pack total wealth (report the gap; do not rescale to force a match).
3. Runs: three return regimes (low, mid-point label, high) times three saving ratios (min, median, max) under A; one B check; the legacy arm. Report for year 0, 10, 50 and 100: aggregate wealth over GDP (index to start), the saving ratio realised, the share of wealth by band, the identity residual.
4. Report plainly what comes out: where the wealth/GDP path flattens, rises or falls and why in the account terms (saving plus gain against growth), against the legacy path (wealth/GDP 47% of start at year 100). Do not adjust any input to make a run look reasonable; if a result looks wrong (negative wealth, explosion), report it with the inputs.
5. Output: `docs/model-v3/cell-baseline.md` (the findings, with the tables and the units reconciliation), the CSVs under `docs/model-v3/cell-baseline/`, the script. Tests: the identity holds in every year of every run; the legacy arm reproduces the kernel's legacy wealth path on the same inputs; the run is deterministic.

## Touches
New: the module, its test file, `docs/model-v3/cell-baseline.md`, `docs/model-v3/cell-baseline/`, the run script. Registration per `docs/agents/code.md` (LAYER row, budget row, `test_groups.py` only if a runner group is filled). Nothing in `kernel.py`, `runner.py`, `revenue.py`, `burden.py`, the register or the pack. Name any further file before editing it.

## Acceptance criteria
- Ten cells run 100 years under the stated inputs; identity residual below 1e-9 in every year; the legacy arm matches the kernel's legacy path.
- Units reconciliation with the gaps reported, not forced.
- The findings note states results for all runs and what drives the paths; no input is tuned.
- Existing digests and suites unchanged (237+ model tests pass; pre-existing data and hooks failures reported as on main).
- Diff limited to Touches.

## Checks to run
v3 suites in the background (never piped); `python -I pipeline/check_agent_docs.py`. Print only summary lines from the run script; write tables to CSV.

## Out of scope
Any WDT, the public ledger, kernel wiring, pension withdrawal, transitions between cells, mortality and inheritance, validation against the 099r moments (the next brief), any register or paper edit.

## Open questions
Retired fraction source; whether the per-household and per-person conversions make the aggregate wealth/GDP comparable with the pack's.

## Implementation notes
<!-- progress:start -->
- **Done:** `model_v3/core/cells.py` (layer 2), `tests/model_v3/test_cells.py`, run script and CSVs in `docs/model-v3/cell-baseline/`, findings in `docs/model-v3/cell-baseline.md`; 15 runs (9 regime by saving, 2 accrual and 2 retired-fraction sensitivities, B, legacy); v3 250 passed; check_agent_docs exit 0; script reruns byte-identical.
- **Next:** the validation brief against the 099r moments; the author decides what to do about the accrual mid-point label (2.7 times ONS D.8 on today's wealth).
- **Decisions:** weights are households (pack counts split by the person shares of cell_weights); money carried in thousands of pounds inside the module; retired fraction 0.4386 from the held ETB Tables 3a and 4a; gain = total return minus the regime's JST portfolio yield for pension and net financial.
- **Gotchas:** `household_step` tripped on a cell with negative non-pension wealth even when nothing is paid (NaN shares, a payment-exceeds error); fixed in `household.py` with a test (named below). Its identity check is absolute 1e-9, so per-household pounds in the millions failed on rounding.
- **Resume:** none.
- **Not run:** none.
- **State:** done; merged
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 110c, untaxed cell baseline run
- Files changed: model_v3/core/cells.py (new); tests/model_v3/test_cells.py (new, 4 tests); docs/model-v3/cell-baseline.md; docs/model-v3/cell-baseline/ (cell_baseline.py, cell_paths.csv, aggregates.csv, tables.md, inputs_used.json); tests/model_v3/conftest.py (LAYER row core/cells: 2); docs/model-v3/architecture.md (budget row 80/60, totals, 2.12); NAMED, outside Touches: model_v3/core/household.py (no-payment case: shares no longer NaN and the payment check applies only when T > 0) and tests/model_v3/test_household.py (one test)
- What is different now: ten cells run 100 years untaxed under convention A, B and legacy; the findings note reports wealth over GDP, saving, shares, account terms and negative positions for 15 runs.
- New or changed interfaces: cells.cell_table(pack, reg, retired), cells.run_cell(cell, years, sav, accrual, growth, rets, convention, c); household_step accepts a cell with negative non-pension wealth when T_WDT is 0
- Acceptance criteria: ten cells, 100 years, identity residual below 3e-11 in every year of every run (met, tested); legacy arm equals grow_and_consume (met, rtol 1e-12, tested); units reconciliation with gaps reported not forced: households 0.00%, wealth 0.01%, persons -3.6% against I-D4h central (0.0% at low), income -11% against B.6g 2021, accrual 2.7 times D.8 2021 (met); findings state all runs, nothing tuned (met); existing digests and suites unchanged: v3 250 passed, data 5 failed and hooks 1 failed as on main (met); diff limited to Touches plus the two named files (partly met)
- Deviations from the brief: retired fraction from the held ETB (0.4386), not the 0.6 fallback, with 0.6 and 0.8 as sensitivity; gain on pension and net financial is the register's total return minus the JST regime yield (so the yield is not counted twice); sensitivities on accrual added because it drives the result
- Risks / follow-ups: the mid-point label of I-D1k gives 2.7 times today's ONS D.8, and with the median saving ratio the accrual is 1.12 of the 1.22 points of saving, so the baseline path is mostly a statement about that label and about the return regime (0.85 low, 2.04 mid, 9.9 high at year 100); minimum saving ratio makes net financial wealth negative in every band eventually (no borrowing constraint); B and A paths differ in composition after year 1; household_step's identity check is absolute, so callers must keep money near unit scale
- Instruction friction: none
- Verification: pytest tests/model_v3: 250 passed in the background; run_suites data hooks: 5 and 1 failures, the pre-existing ones; check_agent_docs exit 0; script rerun byte-identical (md5)
- Overview sections likely needing an update: none
- Commit / branch: brief/110-cell-baseline, merged to main
```
