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
- **Done:** `model_v3/core/revenue.py` (246 lines, budget 520) and `tests/model_v3/test_revenue.py` (168 lines, budget 350). `run_lines` (kernel over paths x 6 death phases, one call), `fund` (rewritten from `run_fund`, vectorised), `taxes`, `retire` (staged retirement), `revenue` (M1a to M1e, M1, B1a to B1d, P1, P3 to P7b, short and long windows, negative-M1 share), `identity` (I3), `gdp_growth`, `window_mean`. M1 to M7 pass (M1 equals its parts to 1e-12, a negative-M1 path passes unclipped, fund hand cases, retirement order, P3 zero at each retirement, B1d a split of M1a). `pytest tests/model_v3 -q`: 143 passed, 2 xfailed (I1 and I2, strict). A smoke run of 117 windows takes under 1 second.
- **Next:** the author rules on I1, I2 and I3 (numbers below). Not merged.
- **Decisions:** (1) Run settings are read from the register (I-D14a to g, I-D7a 2.82 as a constant share of GDP, I-D8a 3 and 3 as `ms`, `ml`); the I1 and I2 runs use v2-like settings: all value on Route C, v2's candidate rule set (`units_and_value`, `reset`), no verification hazard, GDP-indexed threshold, c 3.5%, 6 phases, G 30. (2) GDP in year t is the pack's 2,211.48 bn times cumulated real GDP per head growth (population fixed). (3) The kernel's deaths are staggered as in v2 (first deaths at 5, 10, ... 30). (4) `tax` and `refund` are the in-life assessments split by sign; the death-time assessments (`death_tax`), heirs, `death_B` and `death_D` are their own arrays; M1a is their sum, as v2's `net`. (5) M1c = S(-1) r - (S - S(-1)), so relief = M1a + M1b + M1c exactly.
- **Gotchas:** (1) **I1 and I2 miss.** v2-like inputs over the 117 UK windows, post-fill 10-year individual WDT take, median, percent of GDP: with the ratio-mirror refund 3.58 with the levy fund, 3.50 with no levy; with the model's refund (tau x loss) 3.45 and 3.46. v2: 7.34. I1 misses by 3.76 (limit 0.02), I2 is 2.89 below its lower bound 6.34. The refund rule moves the number by 0.13 (3.58 to 3.45); the gap is not the refund. Fill year median 7 (v2: 7), no unfilled window. The cause is in the base: the realised effective rate eps is 10.2% (omega 5.71), against 24.5% for v2-like inputs (`tornado.md` section 4); 7.34 x 10.2 / 24.5 is 3.0, the right order. Eleven lines, the top one the whole top 1% at a mean of about 4m per adult, cannot carry the tail where the schedule reaches 90%; v2's cells go to the Rich List. With the register route mix and lambda 5% the number is 3.09. (2) **I3 misses on M1a.** The tax assessed on gains equals eps x g x omega to 1e-15 (an exact accounting identity). M1a does not: its median gap to eps x g x omega - refunds is 70% (60% with the register mix), because M1a is cash and units received, and it includes Route D tax that accrues and is settled at death, the death assessments and the heirs' assessments (the heir is taxed on the whole receipt as a delta from zero, as the kernel does, which is about as large as the in-life tax). No gain rate explains those. (3) **B1d is identically zero**: the kernel refunds at the rate of the new wealth, which is 0 below W_min, and rebases, so a line that falls out of the base is never refunded; B1d stays a valid split (0 <= B1d <= refunds) and the test records the finding. (4) **Long-term M1 is negative in all 117 windows** (median -4.57% of GDP) and P3 is large (median 364 percentage-point years): taxes are retired as relief covers them, then relief (about 3.5 WDT + 2.8 levy) falls below the 8.11 retired. With a base that carries 7.34 this would be much smaller. (5) The corporate levy is the register constant, so the levy bases of v2 ("both levy bases") are not both available; I ran with and without it (above).
- **Resume:** after the author's ruling: finer top lines (from the tail table or a Rich List input) are the probable fix for I1, and a decision on whether I3 should compare against the in-life assessment; then rerun `pytest tests/model_v3 -q` and remove the two xfail marks.
- **Not run:** nothing in the brief; v2 not run (its 7.34 is a constant).
- **State:** built; I1, I2 and I3 miss; branch pushed, NEEDS THE AUTHOR
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 052c, model v3 stage V3-7: revenue, fund and identity check
- Files changed: model_v3/core/revenue.py (new, 246 lines); tests/model_v3/test_revenue.py (new, 168); this brief
- What is different now: v3 computes per-path revenue lines M1a to M1e and M1, the fund, the fill year and horizon windows, P1 and P3 to P7b, and the epsilon identity.
- New or changed interfaces: run_lines, fund, taxes, retire, window_mean, revenue, identity, gdp_growth in model_v3.core.revenue
- Acceptance criteria: M1 to M7 pass (met); M1 equals its parts to 1e-12 and a negative-M1 path passes unclipped (met); I1 7.34 within 0.02: NOT met (3.58); I2 between 6.34 and 7.36: NOT met (3.45, refund-rule effect 0.13); I3 within 5% of M1a: NOT met (70%; exact for the assessed tax, 1e-15); revenue.py 246 of 520 lines (met); git diff --stat limited to Touches (met)
- Deviations from the brief: none; I1 and I2 are strict xfail tests, so the suite is green and the miss cannot pass silently
- Risks / follow-ups: (1) the base's 11 lines understate the effective rate (10.2% against 24.5%): needs finer top lines; (2) I3 as worded compares M1a, which includes deferred and death flows; (3) B1d identically zero by the kernel's refund-at-new-wealth rule and rebase; (4) long-term M1 negative in every window at this base; (5) levy is a constant share
- Verification: pytest tests/model_v3 -q: 143 passed, 2 xfailed
- Overview sections likely needing an update: model v3 build status (V3-7 built, acceptance open)
- Commit / branch: brief/052-revenue (pushed, not merged)
```
