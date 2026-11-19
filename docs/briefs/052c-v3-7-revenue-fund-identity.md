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

## Guru rulings, 2026-11-19 (after the first build)
Reviewed: revenue.py and the tests are as the brief wants; your diagnosis of I1 and I2 is right (11 lines, the top line is the whole top 1%) and the author chose the fix.
- **I1, I2:** briefs 072g (register rows for the Pareto alpha and tier cuts) and 073c (base tail from the Rich List, builder taking its constants as arguments) first. Then rebase this branch on main and rerun. I1 and I2 pass v2's own tail constants (2017/18 Rich List 1,000 entries and £700bn, `s1_survey` 0.18, `s10_survey` 0.51, 5% extra, alpha 1.5, cuts 1%, 10%, 100%) as constants in the test; the model passes the register's. A remaining miss stops with NEEDS THE AUTHOR and the numbers; do not tune.
- **I3 (author: exact decomposition):** assert (a) the tax assessed on gains equals eps x g x omega to 1e-12 (it holds to 1e-15 now) and (b) M1a = in-life tax minus refunds plus the death-time assessments and the heirs' assessments, each to 1e-12. The sentence "M1a is about eps x g x omega minus refunds" holds for in-life assessment only: report it as a writing item, with the median gap you measured.
- **B1d:** keep B1d valid and zero as a finding (a line that falls below W_min gets no refund because the kernel refunds at the rate of the new wealth, which is 0 below W_min); record it in the report as a finding for the papers.
- **Long-term M1 negative in every window:** expected with the coarse base; report the figure again after the tail, do not treat it as a defect first.
- Remove the two xfail marks when I1 and I2 pass; keep the stage's other tests as they are.

## Guru rulings, 2026-11-19 (after the rework)
Reviewed `brief/052c-rework` (4b76e03): the tests and the I3 decomposition are as ruled. I1 5.02 and I2 4.97 still miss; the author decided: diagnose first (brief 074c, one v2 input at a time, no fix), and **do not merge 052c until I1 and I2 pass**. Keep the two strict xfails. Do not tune. Continue on this branch with 074c.

## Guru rulings, 2026-11-19 (after 074c)
Reviewed `docs/model-v3/i1-gap.md`: good work; your withdrawal of the finer-cells proposal is accepted. Author decisions:
- **Test constants approved.** The I1 and I2 tests take v2's inputs as constants in the test file (W_min 0.1125, GDP 2,097bn, 51.0m adults, v2's 41-cell table, JST `gpc_real` growth); the model, register and pack keep their own values. Same principle as the tail: the identity checks the port, not the data. Expected I1 about 6.66, I2 about 6.61.
- **I1 stays strict (within 0.02).** The last 0.68 is not to be hunted from the spec. Brief 078c (another agent) runs v2 once and records its per-window output and cell table as `tests/model_v3/fixtures/v2_logistic_ln_ref.json`. When it lands, rebase, compare window by window, and report where the 0.68 sits; do not tune.
- Until then keep I1 as a strict xfail with the new constants and the numbers in the reason; I2 passes and loses its xfail. Do not merge 052c until I1 passes. The W_min (0.1125 against 0.150) and wealth over GDP (7.21 against 6.44) differences are recorded as writing items, not changed.

## Guru ruling, 2026-11-19 (after 078c): the statistic is the mean
The v2 reference run found that v2's 7.34 is the **mean over the 117 windows** of the net post-fill take (7.3416); the median is 6.594. Your I1 and I2 compared a v3 median with it. Corrected in `architecture.md` and `acceptance.md` (merged to main). This replaces the earlier ruling's expectation of I1 about 6.66:
- Rerun I1 and I2 with the **mean over windows**, v2 constants in the test as already approved, per-window take defined as v2 does (net: tax + death tax + heirs - refunds, no levy, years fill to fill+9, ratio of sums over GDP). Use `tests/model_v3/fixtures/v2_logistic_ln_ref.json` for the cells, GDP, W_min, `gpc_real` and the per-window arrays.
- I1: v3 mean within 0.02 of 7.34. I2: mean with the model's refund within 6.34 to 7.36.
- Compare window by window with the fixture (fill year, net take) and report the largest differences. Do not tune. A remaining miss stops with NEEDS THE AUTHOR and the table.
- Remove the xfail marks that now pass; keep a strict xfail only on a check that still misses.
- Merge main into this branch first (it has the fixture).

## Implementation notes
<!-- progress:start -->
- **Done:** branch `brief/052c-rework` = main 737ee3a + the first build (cherry-picked; `revenue.py` unchanged, 246 of 520 lines) + this rerun. Tests only: I1 and I2 run on v2's tail constants (`V2_TAIL`, `V2_S10`, fixture `v2env`), I3 rewritten as 3a (assessed tax = eps x g x omega, 1e-12), 3b (M1a = in-life tax - refunds + death-time + heirs, 1e-12), 3c (median gap recorded). `pytest tests/model_v3 -q`: 153 passed, 2 xfailed (I1, I2, strict).
- **Next:** the author rules on I1 and I2 (numbers in the change report). Not merged. Do not tune.
- **Decisions:** (1) v2's top-10% share 0.51 is applied by rescaling the pack deciles inside the test (the pack gives 0.407); the model keeps the pack's. (2) `death_tax`, `death_B`, `death_D` are the "death-time assessments" of I3b; `heir` the heirs'. (3) The old branch `brief/052-revenue` is not rewritten; this branch carries its two commits.
- **Gotchas:** (1) **I1 and I2 still miss** with v2's own tail: I1 5.02 (limit 7.34 +- 0.02), I2 4.97 (lower bound 6.34); register tail 4.62 and 4.59. (2) Realised eps 12.3% (v2 tail) against v2's implied 24.5% (`tornado.md` 4; definitions differ: g there is gross). Start-state wealth-weighted rate is 22.9%. (3) Long-term M1 negative in 117 of 117 windows (median -4.69).
- **Resume:** `git checkout brief/052c-rework`; after the ruling: edit `test_revenue.py` (xfail marks, constants) only; `pytest tests/model_v3 -q`.
- **Not run:** v2 (7.34 is a constant); nothing else in the brief.
- **State:** pushed on `brief/052c-rework`; NEEDS THE AUTHOR (I1, I2). Gap diagnosis (074c): `docs/model-v3/i1-gap.md`, 71% of the gap recovered from v2 inputs.
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 052c rework, model v3 stage V3-7: rerun I1 to I3 after briefs 072g and 073c
- Files changed: tests/model_v3/test_revenue.py (213 lines, budget 350); this brief. model_v3/core/revenue.py is unchanged from the first build (246 of 520 lines)
- What is different now: I1 and I2 run on the 14-line base with v2's own tail constants (2017/18 Rich List 1,000 entries, GBP 700bn; s1 18%, s10 51%, 5% extra, alpha 1.5, cuts 1% and 10%) as test constants; I3 is the exact decomposition
- New or changed interfaces: none
- Acceptance criteria:
  - M1 to M7 pass; M1 equals its parts to 1e-12; a negative-M1 path passes unclipped: met
  - I1 (7.34 within 0.02): NOT met. v2 tail 5.016 with the levy fund, 4.884 without; miss 2.32. Register tail 4.623 and 4.564 (old 11-line base 3.58 and 3.50)
  - I2 (6.34 to 7.36): NOT met. v2 tail 4.974 with the levy, 4.924 without; 1.37 below the lower bound. Register tail 4.585 and 4.582 (old 3.45 and 3.46). Model refund (tau x loss) against ratio mirror: -0.04 to +0.04 (levy and no levy; was 0.13 on the old base)
  - I3: met as the author's exact decomposition. (a) tax assessed on gains = eps x g x omega, max relative gap 1.1e-15 (limit 1e-12); (b) M1a = in-life tax - refunds + death-time + heirs' assessments, max gap 0 (limit 1e-12); in the register mix death_tax and death_B are 0, death_D (Route D settled at death) and heirs are not
  - revenue.py at most 520 lines: met (246). git diff --stat limited to Touches: met (revenue.py, test_revenue.py, this brief)
- Deviations from the brief: v2's 0.51 top-10% share is imposed in the test by rescaling the pack deciles (the model's base takes it from the pack, 0.407); the old branch brief/052-revenue was not rewritten (new branch, two commits cherry-picked)
- Risks / follow-ups (NEEDS THE AUTHOR, I1 and I2):
  - Measured on 117 UK windows, post-fill 10-year individual WDT take, median, percent of GDP. v2-like inputs (all Route C, v2 rule set, no verification hazard, c 3.5%). Model settings (register route mix, lambda 5%): 4.21 on v2's tail, 3.92 on the register tail (old 3.09)
  - Where the gap sits: realised eps 12.3% against v2's implied 24.5% (tornado.md 4; g there is gross, here net of consumption, so not like for like). The start-state wealth-weighted rate is 22.9%. Each line is one representative adult: D10a holds 31.4% of wealth at a mean of GBP 0.96m (rate 20.6%), D10b 17.0% at GBP 4.7m (53.2%); a spread inside a line would lift the rate, v2's cells carry one. Hypothesis, not tested
  - Options: (1) accept the 14-line base and restate I1 and I2 on it; (2) a base brief that splits D10a and D10b finer, then rerun; (3) give v2's cell table as a test constant. Proposal: (2), testable and in the model's own terms
  - Findings for the papers: B1d is identically zero (the kernel refunds at the rate of the new wealth, 0 below W_min, and rebases); the sentence "M1a is about eps x g x omega minus refunds" holds for in-life assessment only, median gap of M1a to that sum 55% (range 37 to 87%, 30 random paths, register mix); long-term M1 is negative in 117 of 117 windows (median -4.69% of GDP, P3 median 364 percentage-point years, P7a 0), as before the tail, not treated as a defect
- Verification: pytest tests/model_v3 -q: 153 passed, 2 xfailed (I1, I2, strict: a pass would error and prompt removing the marks). Fill year median 7, no unfilled window
- Overview sections likely needing an update: model v3 build status (V3-7 built, I1 and I2 open)
- Commit / branch: brief/052c-rework (pushed, NOT merged: NEEDS THE AUTHOR)
```
