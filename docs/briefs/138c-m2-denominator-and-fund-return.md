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
- **Done:** none
- **Next:** block 0
- **Resume:** `git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git checkout -B brief/138-m2-fund-return origin/brief/138-m2-fund-return`
- **State:** ready; not started (after 137c and 135c)
<!-- progress:end -->
