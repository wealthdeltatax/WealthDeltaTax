# 090: Wealth-to-GDP and revenue decomposition (tests of the private-wealth hypothesis)

- **Status:** retired 2026-11-20 (merged `4958609`)
- **Author/date:** K. Ogata with the guru, 2026-11-20
- **Depends on:** none (084c merged)
- **Read:** `docs/hypotheses/private-wealth-growth-relative-to-gdp-and-declining-wdt-revenue.md` (sections 3 and 6); `docs/model-v3/f1-diagnostic/report.md` (Reading, item 4) and `f1_gap.py` (how it builds the context and calls `runner.core_run`); `model_v3/runner/runner.py` (`context`, `core_run`, `Raw`); `model_v3/core/burden.py` (module note, `line_flows`: `w0`, `delta`) and `core/revenue.py` (module note: relief, fund, retirement, `gdp_growth`); `docs/model-v3/inputs.md` rows I-D14c, I-D1a, I-D1a2, I-D7a.

## Goal
Say, with numbers, why post-fill relief falls relative to GDP in the 083c runs, by running tests A to F of the hypothesis. Report only: no model, register or metric change.

## Decisions (author, 2026-11-20)
The hypothesis file is the test plan; decompose, do not tune until F1 improves. The author rules on I-D14c (consumption, a retained v2 setting), the feasibility rule and CK1 only after this report and the 083c report.

## Design
Write `docs/model-v3/wealth-ratio-diagnostic/wealth_ratio.py` and `report.md` (outside `model_v3/`, as 083c did). Central inputs, the 27-point grid reduced to three schedules (tau_m 0.5, 0.7, 0.9 at k 0.5, ratio 0.5), seed 20261118.

Guru preliminary look (one schedule, tau_m 0.5, k 0.5, ratio 0.5, constant 4.74% return, `core_run`, not a result; reproduce or refute it): aggregate wealth W (sum of weight times `w0`) divided by the GDP index, in years 1, 5, 10, 20, 30, 50, 75, 100, was 1.00 to 0.47 at consumption 3.5%, to 1.16 at 2.5%, to 2.77 at 1.5%, to 9.5 at 0, and to 0.62 at 3.5% with the tax switched off (rates 1e-9; `tau_0` must be above zero). So consumption looks decisive and the tax's own drag takes 0.62 to 0.47. Two cautions: (a) M1a read in a single year is spiky: years 90 and 95 gave 2.67 and 2.15 against about 0.10 in the years between (death settlements every five years), so single-year M1a comparisons mislead; use five-year block means; (b) the constant path compounds at the arithmetic mean 4.74%, which flatters: paths compound geometrically (about 4.42% less the path's own variance), so random paths are worse than the constant path.

Items (all per schedule; per-year values as five-year block means of GDP-points):
1. **A, consumption sweep.** I-D14c in {0, 1.5, 2.5, 3.5 and the register's low and high}: W, W/GDP index, wealth above W_min, annual positive taxable increments, M1a, M1b, M1c, relief, relief minus M1d, and the first year relief falls below M1d.
2. **B, tax drag.** returns only (rates 1e-9, consumption 0); returns plus consumption (rates 1e-9); returns, consumption and the tax. W/GDP index at years 10, 30, 50, 100.
3. **C, levels and ratios.** For every scenario above, the real level (pounds, index to year 1) beside the share of GDP, so growth in pounds is not read as growth of the base.
4. **D, threshold indexation.** The threshold follows GDP per head (`gdp_growth`). If the core has no switch for a fixed real threshold, report that and do not edit core; otherwise compare the two on taxpayer count, taxable wealth and M1a.
5. **E, relief components.** M1a, M1b (the constant levy, I-D7a), M1c (fund income) and the reserve, per block, so a fall in relief is attributed.
6. **F, conventions.** (i) the constant path at the arithmetic mean 4.74 against the geometric 4.42; (ii) 1,000 random paths at central inputs (the generator of `returns.py`), reporting the median and P10 of W/GDP at years 30, 50, 100 and the share of paths whose relief falls below M1d inside the short window; (iii) constant GDP growth: `runner.context` takes the arithmetic mean of annual growth, 1.57%, as the constant; the geometric mean of the same years is 1.49%: run both and report the difference in W/GDP at year 100 and in the first year relief falls below M1d.

The report opens with three sentences: what share of the fall in relief over years 10 to 100 each of consumption, tax drag, threshold drift and the levy accounts for, whether the hypothesis is supported, weakened or mixed (section 7 of the hypothesis), and the consumption rate at which W/GDP stays flat with the tax on. It recommends nothing about the rule or I-D14c.

**Early check.** At consumption 3.5% and the tax off, W/GDP at year 100 must be close to the hypothesis's own illustration (about two-thirds); report the number. If it is not, stop and report: the kernel's compounding is not what the hypothesis assumes.

## Touches
`docs/model-v3/wealth-ratio-diagnostic/wealth_ratio.py`, `docs/model-v3/wealth-ratio-diagnostic/report.md`, this brief's progress block, `docs/agents/friction-log.md`.

## Acceptance criteria
- The report holds items 1 to 6 with numbers and the three opening sentences; the script reruns to identical text with the seed in the report.
- On the central, consumption-3.5% schedule the script reproduces 083c's first year of relief below M1d (year 13 at tau_m 0.5 and 0.7, year 11 at 0.9) or says why not.
- `python -I -m pytest tests/model_v3 -q` passes with no file under `model_v3/` or `tests/` changed.
- `git diff --stat` limited to Touches.

## Checks to run
The script; `pytest tests/model_v3 -q`.

## Out of scope
Any change to the kernel, `revenue.py`, `runner.py`, I-D14c, A5, CK1 or the manifest; level 2; a fix.

## Open questions
None.

## Implementation notes
<!-- progress:start -->
- **Done:** wealth_ratio.py and report.md (items 1 to 6, three opening sentences); early check 0.62; script reruns to identical text (seed 20261118); pytest tests/model_v3 208 passed.
- **Next:** author rules on I-D14c, the feasibility rule and CK1 after this report and the 083c report.
- **Decisions:** relief rises to year 20 then falls, so the attribution runs from the block ending year 20 (not 10) to year 100; 083c's year-11 at tau_m 0.9 is reproduced on its own k 1.0 schedules.
- **Gotchas:** the runner has no fixed-real-threshold switch; the script repeats core_run with burden.line_flows' index argument and asserts equality with core_run on the GDP-indexed case.
- **Resume:** none.
- **Not run:** none.
- **State:** done; merged
<!-- progress:end -->

### Change report
```
Change report
- Task: brief 090c, wealth-to-GDP and revenue decomposition
- Files changed: docs/model-v3/wealth-ratio-diagnostic/wealth_ratio.py (the diagnostic); report.md (its output); this brief's notes
- What is different now: the report says, with numbers, why relief falls relative to GDP: consumption (I-D14c 3.5) accounts for all of the fall from the year-20 peak (with c 0 relief rises 36.6 to 36.9 GDP-points instead of falling 1.22 to 1.53); the tax's own drag is 35 to 36% of the log fall in W/GDP (0.62 tax off, 0.47 on at year 100); a fixed real threshold removes 8 to 11% of the fall; the levy 0%. W/GDP stays flat at c about 2.65 to 2.67 with the tax on. Hypothesis: supported.
- New or changed interfaces: none
- Acceptance criteria: report holds items 1 to 6 and the three opening sentences, script reruns identical (met); 083c first year below M1d reproduced: year 13 at tau_m 0.5 and 0.7, year 11 at 0.9 on 083c's k 1.0 schedules (met; at this brief's k 0.5 tm90 gives 13, six taxes retire only at k 1.0); pytest tests/model_v3 passes, no file under model_v3/ or tests/ changed (met, 208 passed); diff limited to Touches (met)
- Deviations from the brief: attribution measured from the block ending year 20 because relief does not fall from year 10 (3.02 to 3.14); shares are removal counterfactuals, consumption's is above 100% (it reverses the fall) so no remainder is reported; geometric GDP growth on the same 117 years is 1.534%, not the brief's 1.49% (full 1870-2019 history 1.43%)
- Risks / follow-ups: constant path compounds at the arithmetic mean; the 1,000 random paths give W/GDP y100 median 0.34, P10 0.09, and every path has relief below M1d (median first year 11)
- Instruction friction: none
- Verification: script run twice, cmp identical; early check 0.616; pytest tests/model_v3 -q 208 passed; not run: nothing
- Overview sections likely needing an update: none
- Commit / branch: see git log, brief/090-wealth-ratio, merged to main
```
