# 052: Model v3 V3-7: revenue, fund and the identity check

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-18
- **Depends on:** 049, 050, 051
- **Read:** `docs/model-v3/architecture.md` 2.5, 3.4, 6.2 (M1 to M7) and 6.3 (I1 to I3); `docs/model-v3/metrics.md` (M1 family, B1, P1, P3 to P7); `docs/model-v3/stage-c-decisions.md` items 2 and 3; `model_v2/rates_core.py` lines 1109 to 1193 (`run_fund`) as specification; `docs/model-v3/acceptance.md` V3-7 row.

## Goal
Per-path revenue lines, the fund and the horizon windows, with the identity check against v2's recorded number.

## Decisions (author, 2026-11-18)
`architecture.md` approved (sections 8.1 and 9 as written); `acceptance.md` approved with Q1 to Q6 as proposed. v3 imports nothing from `model_v1/` or `model_v2/`. No file outside this brief's Touches is changed.

## Design
`core/revenue.py` (520 lines): M1a to M1e, M1 = M1a + M1b + M1c - M1d with no floor or clip, B1a to B1d, the fund (short and long reserve, fill rule, retention), the fill year, the horizon windows of 3.4 and the unfilled-path rule, P1, P3 to P7b, and the epsilon identity as a computed check. Staged retirement in ascending order of receipts. Tests I1 and I2 run at the `logistic_ln_ref` scenario over the 117 usable windows (the reference 7.34 is a constant in the test; v2 is not run or imported). I1 patches `assess` to the ratio-mirror refund inside the test.

**Shared interfaces, fixed before any stage starts** (a build brief never edits them; a mismatch is a question to the guru): the output file shape is `schema wdt-outputs/1` as `pipeline/validate_outputs.py` checks it and `docs/restructure/site/hooks.md` section 3 with the 030c rulings; the country pack format is `docs/model-v3/country-pack.md`; the id lists are `docs/model-v3/outputs.yml` and the module-to-id table of `architecture.md` 2.10; the Samples contract is `architecture.md` 2.9; the layers and import rules are `architecture.md` 5.1.

This is build stage V3-7 of `architecture.md` section 7. One session, one lane; the stage ends in a stop: tests pass, change report written, branch merged by the auto-merge rule. The stage's files are budgeted in `architecture.md` 6.1; a stage more than 15% over its budget reports it before the next starts.

## Touches
`model_v3/core/revenue.py`, `tests/model_v3/test_revenue.py`, this brief's progress block.

## Acceptance criteria
- M1 to M7 pass; M1 equals its parts to 1e-12; a negative-M1 path passes unclipped.
- I1: post-fill 10-year WDT take 7.34 within 0.02 points of GDP. I2: between 6.34 and 7.36 with the model's refund; the measured difference is in the change report. I3: identity within 5% of M1a.
- `revenue.py` at most 520 lines.
- `git diff --stat` is limited to the Touches list.

## Checks to run
`pytest tests/model_v3 -q`.

## Out of scope
Burden metrics; the range runner.

## Open questions
An I1 or I2 miss is not tuned away: stop with NEEDS THE AUTHOR and the numbers.

## Guru rulings, 2026-11-19
Blocked on the first run (your note on `brief/052-revenue`): correct, my gaps again. Do not start before 070c and 071g merge; start again from main and keep the progress block.
- **Macro inputs:** brief 070c adds real GDP per head (`returns.csv` `gdp_pc`, you derive growth) and the reference expenditure over GDP (`public_expenditure.csv`, function `total`).
- **Run settings:** brief 071g adds `lambda_C`, `lambda_D` (5 central, 0 to 10), consumption `c` (3.5), `a_window` 5, `horizon` 10, `safe_share` 0 and `exp_ref_year` 2019 as register rows. Read them from `registry/inputs.json`.
- **Levy base:** M1b reads the register's I-D7a (2.82% of GDP, constant share); v2's per-window derivation from the equity price return is not ported.
- **Not needed under Route B `sale`:** the deferral rate and the income cap.
- **I1 risk:** v3's base is the WAS deciles plus a tail ratio (11 lines), not v2's cell distribution, so I1 (7.34 within 0.02) may miss. A miss stops with NEEDS THE AUTHOR and the numbers, never a tune: report the v3 value, both levy bases, and the difference.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** draft; not started
<!-- progress:end -->
