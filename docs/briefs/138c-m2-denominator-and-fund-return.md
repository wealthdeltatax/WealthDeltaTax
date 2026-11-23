# 138: M2 on total wealth, and the fund's return as a labelled scenario axis

- **Status:** ready (after 137c and 135c: all three touch `arm.py`)
- **Author/date:** K. Ogata with the guru, 2026-11-23
- **Depends on:** 136c (merged), 137c, 135c
- **Read (block 0: the first two only):** (1) `docs/model-v3/household-vs-legacy.md` (Defects list 1; the P6 and M1c sections); (2) `docs/agents/code.md`. Later: `model_v3/core/revenue.py` (`line_flows`, `w0`, the fund's return); `model_v3/runner/arm.py` (the fund's safe stand-in); `docs/model-v3/household-arm-run/run_grid.py`.

## Goal
Two things 136c found. (1) M2 and M2d divide by `w0`, the kernel's family value, which under the household arm is total wealth in year 1 and non-pension wealth from year 2, so household M2 is overstated 1.5 to 2.5 times against the legacy arm, which divides by total. (2) The household fund earns the safe stand-in (net financial return, about -0.5 to 1.1%) where the legacy fund earns the market mean (4.74%); that one choice makes up all of the P6 gap, and drives M1c and the long M1 net.

## Decisions (author, 2026-11-23)
- M2 and M2d divide by total wealth including the pension (the base the tax is assessed on). A bookkeeping fix in the household arm only; the legacy arm is unchanged and byte-identical.
- The fund's return is a labelled **scenario axis**: `safe` (today's stand-in, the low case) and `market` (the fund earns the market mean, like the legacy arm). P6, M1c and the M1 net are reported as a range across both, never one value and never a central case. Default stays `safe` so every existing output is unchanged; `market` is an explicit switch. No register row now (the named constant goes in the later register brief with `I-D15a` and `I-D1m`).
- No change to household economics beyond these two items; no headline number.

## Added by author ruling, 2026-11-23 (after 135c): two small items, do them first as block 1a
- **I1 tolerance.** The I1 residuals of 1e-9 to 5e-8 (millions of pounds per adult) on lines the floor holds at zero are the kernel cap's own tolerance (the lien's unit part). Loosen the check to **1e-7 absolute** (the hook's post check and any test that mirrors it), say so in `household-arm-paths.md`, and rerun `median_high` at 200 paths so that point has rows. No kernel change; if the check cannot be loosened without touching `core/`, stop and report.
- **Lien remainder the pension cannot cover.** At `min_mid` with per-path returns `unpaid_B` is 3.02bn (after weighting) on 2,638 path-phases: the lien exceeds the pension. Rule: limited recourse. The state collects up to the pension; the remainder is a **labelled write-off in the public ledger** (the ledger's write-off column, as the floor already does), so `unpaid_B` from this cause is zero and the cost to government is visible. Bookkeeping only, in the hook and `pension_lien.py`; tests (the lien never exceeds the pension; the write-off ties to the ledger; held points byte-identical where it does not fire); rerun `min_mid` at 200 paths and report the write-off total and path-phases. Heir floor (148c) is a separate later switch.

## Blocks (one push each; `docs/agents/code.md`)
- **Block 0:** progress block pushed.
- **Block 1: M2 denominator.** Total wealth (class total incl. pension) stored for the household arm, used by M2 and M2d; any other reader of `fl['w0']` named in the note and either fixed or listed. Test: D5 `median_mid` year 2 uses 0.1286, not 0.0808; legacy outputs byte-identical. Push.
- **Block 2: fund-return axis.** The `fund_return` switch (`safe` or `market`) in the household arm, off by default; a test that `safe` is byte-identical to today and `market` credits the fund at the path's market return. Push.
- **Block 3: rerun and note.** Rerun `median_mid`, `max_mid`, `median_low` for both fund settings; in `household-vs-legacy.md` update M2, M2d, M1c, M1 net and P6 as ranges across the two fund settings, each labelled a scenario value. Change report; push; stop.
**Stop rule.** A kernel change is stop-and-report. After three blocks or a quarter of the budget left, push and list the rest. Suites in the background, never piped.

## Touches
`model_v3/runner/arm.py` is at 329 of its 330 lines (137c; the old 'budget 310' is stale): new scenario-switch code goes in the new `model_v3/runner/switches.py` (budget 200, a new file; `arm.py` gains call sites only, or shrinks); any growth of `arm.py` past 330 is stop-and-report, `model_v3/core/revenue.py` only for the denominator, `docs/model-v3/household-arm-run/` (`run_grid.py`, rerun CSVs), `docs/model-v3/household-vs-legacy.md`, `docs/model-v3/household-vs-legacy/`, tests. Not the register, the pack, the manifest, the digest fixture or the kernel.

## Acceptance criteria
- `test_legacy_digest` unchanged; all suites pass; the legacy arm and `fund_return = safe` outputs byte-identical apart from M2 and M2d.
- Household M2 and M2d use total wealth; the 136c like-for-like figures (M2 long 0.14 / 0.25 / 0.10) are reproduced by the model's own M2.
- P6, M1c and M1 net carry both fund settings, labelled scenario values with no central value.

## Out of scope
The deferral rate, pension withdrawal, per-path return regimes beyond 128c, the saving split of the base, any headline number.

## Implementation notes
<!-- progress:start -->
- **Done:** blocks 0, 1a, 1, 2, 3 (branch from main f917908); all pushed
- **Next:** author review
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/138-m2-fund-return origin/brief/138-m2-fund-return`
- **State:** complete
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 138c, M2 denominator, the fund's return axis, I1 tolerance and the lien's limited recourse
- Files changed: model_v3/runner/arm.py (330 lines, the budget: HouseholdHook.total, tolerance 1e-7, settle writes off the lien remainder, calls to switches); model_v3/runner/switches.py (new, fund_return); model_v3/core/burden.py (outside Touches, named: one line, line_flows w0 = hook.total(book) for the household arm; legacy unchanged); docs/model-v3/architecture.md (outside Touches, named: stated total 6,060 -> 6,260 which was failing on main, switches test budget, layer L3.55); tests/model_v3 (conftest layer, test_switches, test_m2_total, test_pension_lien, test_household_tax); run_grid.py (--fund-return); household-vs-legacy/fund_axis.py and .csv; the grid CSVs; household-arm-paths.md; household-vs-legacy.md
- What is different now: M2, M2d (and M2c, O5, O8, OS1 computed from them) divide by total wealth in the household arm: D5 median_mid phase 0 w0 is 0.1286 in year 2 (was 0.0808). fund_return axis: safe (default, byte-identical) or market (every class of the fund and the levy's safe share earn the path's market return; labelled). A lien the pension cannot cover is written off in the ledger at settlement, not left in unpaid_B. The I1 check allows 1e-7.
- New or changed interfaces: arm dict key fund_return; run_grid --fund-return; label scenario.fund_return when market
- Acceptance criteria: test_legacy_digest unchanged, 10 of 10 suites pass (met, last full run before the final note edits); safe equal to the run without the key (test); market ledger rate equals the path return (test); grid checks hold at the held points in both settings (met); median_high runs at 200 paths with I1 holding (met); min_mid unpaid_B 3.02 -> 0.25 (the rest is the class floor's alarm, not the lien: reported)
- Deviations from the brief: burden.py and architecture.md edited (named above). The write-off at min_mid is 357.7 bn on one path-phase in the first 100 paths. fixed-rate CSVs changed in the M2-derived ids only (192 cells), as the brief requires for M2.
- Risks / follow-ups: M1c and M1 net do not depend on the fund setting at median_mid (payout - inflow while the fund covers its payout); the author may want the register to say which setting a figure uses. M2c now multiplies the liquid share by total wealth. The floor's unpaid_B at min_mid remains.
- Instruction friction: the brief's arm.py budget (310) is stale; the budget table says 330.
- Verification: python pipeline/run_suites.py 10 of 10; run_grid 1,000 paths both settings; fund_axis.py
- Overview sections likely needing an update: household arm, fund return axis; decisions
- Commit / branch: brief/138-m2-fund-return; not merged (the arm.py and burden.py changes and the write-off are for the author)
```
