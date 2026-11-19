# 052: Model v3 V3-7: revenue, fund and the identity check

- **Status:** done
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

## Guru ruling, 2026-11-19 (after your I1 result): I1 and I2 restated; you may merge
Excellent diagnosis. The author decided v3 learns from v2 and does not replicate it, and approved restating the checks (see `architecture.md` "Restatement", merged to main; merge main first):
- **I1** = given v2's fill year the v3 take equals v2's per window to 1e-5 points in all 117 windows. Your exact-take test is I1: it is no longer an xfail target; remove the I1 xfail and make that test the I1 check (keep its name or rename to `test_i1`).
- **I2** = at v2's fill year, the mean over the 117 windows with the model's own refund (tau x loss) lies in 6.34 to 7.36; write the difference from I1 (the ratio-mirror) into the change report. If it falls outside, stop with NEEDS THE AUTHOR and the number.
- **The fill-year difference is a finding, not a failure.** Keep a test that records it (fill year equal in 78 of 117 windows; v3 earlier in 39; mean difference +0.17) as an assertion on the counts you measured or as a printed report, and do not tune the fund or the levy.
- Change report: say v3's constant levy (register I-D7a 2.82) against v2's per-window, per-year levy path is the cause, and add the paper question: does a constant levy understate how much the fund's timing varies.
- Then, when `tests/model_v3`, `tests/data`, `tests/gate` and `tests/cards` pass (one at a time or `python pipeline/run_suites.py`), **merge 052c to main**: merge origin/main into the branch, fast-forward push to main, no force. Update the progress block (State: merged) and tell the guru; 053c and 054c start after.

## Implementation notes
<!-- progress:start -->
- **Done:** `revenue.py` (246 of 520 lines), `test_revenue.py` (242 of 350). I1 and I2 restated per architecture.md 6.3 and the 2026-11-19 ruling; both xfails removed; a fill-year finding test added. `pytest tests/model_v3` 159 passed; `tests/data` 84; `tests/gate` 17; `tests/cards` 8. Tests only on this pass; `revenue.py`, `base.py`, pack and register unchanged.
- **Next:** 053c and 054c.
- **Results (percent of GDP, mean over the 117 windows):**
  - **I1 met.** At v2's fill year, with v2's inputs and the ratio-mirror refund, the v3 take equals v2's in all 117 windows to 1e-5 (the measured maximum is 6.5e-6); mean 7.3416.
  - **I2 met.** At v2's fill year with the model's own refund (tau x loss): mean **7.2253** (band 6.34 to 7.36); median 6.489. Difference from I1: **-0.1163** (mean), -0.1047 (median). The model's refund returns less than the ratio mirror.
  - **Fill-year finding (recorded as an assertion, not tuned):** v3's own fund with the ratio mirror gives 7.5137 against 7.3416, +0.1721. Fill year equal in 78 of 117 windows (take difference there at most 1e-5); different in 39: v3 earlier in 37 (by 1 year in 25, 2 in 6, 3 in 3, 4 in 3), later by 1 in 2. The 39 differ by +0.516 on average. The ruling says "earlier in 39": it is 37 earlier and 2 later.
  - **Cause:** v3's fund is fed a constant levy (register I-D7a, 2.82% of GDP); v2 charges a per-window, per-year path (calibrated entry rate on the equity price return, 2.77 post-fill mean). The fund's fill year depends on the net receipts including the levy. A constant levy did not close it in the earlier check: levy 0 matches 81 fill years, 2.2 matches 87, 2.77 matches 79, 3.08 matches 75, 4.0 matches 64 (so no constant reproduces v2's timing).
  - **Paper question:** does a constant levy understate how much the fund's timing varies? In v2 the levy follows the equity price return, so a bad-return window both thins the wealth-tax take and shrinks the levy, and the fill year spreads out; with a constant 2.82 v3 fills earlier in 37 of 39 differing windows, and the fund's timing is less variable. Worth a sentence in the revenue paper and a levy-path option for a later brief.
- **Earlier findings (unchanged):** (1) **B1d is identically zero**: the kernel refunds at the rate of the new wealth, which is 0 below W_min, and rebases, so a line that falls out is never refunded (test M7). (2) **Long-term M1 is negative in 117 of 117 windows** (median -4.69% of GDP on the 14-line base before the v2-input run), as before the tail; not a defect. (3) **"M1a is about eps x g x omega minus refunds" holds only for in-life assessment**: the median gap of M1a to that sum is 55% (range 37 to 87%, 30 random paths, register mix) because death-time and heirs' assessments are part of M1a (I3b is the exact decomposition, I3a holds to 1e-15). Writing items.
- **Decisions:** (1) The model's own base (14 lines, pack inputs, own refund) gives a full-chain mean of 5.52 (median 4.59); it is printed, not asserted against v2: its wealth over GDP is 6.44 against v2's 7.21 and W_min 0.15 against 0.1125. (2) The levy in I1 and I2 tests is the register's 2.82. (3) v2 is not run; the fixture (078c) is the reference.
- **Gotchas:** the local clone fetches only main, so `origin/brief/052c-rework` needs the explicit refspec (`git fetch origin '+refs/heads/brief/052c-rework:refs/remotes/origin/brief/052c-rework'`).
- **Resume:** nothing.
- **Not run:** v2 (read from the fixture).
- **State:** merged.
<!-- progress:end --><!-- progress:end -->

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
