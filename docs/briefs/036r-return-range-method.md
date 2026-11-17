# 036: Research: how the return range is built (model v3 stage C input)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** none. Feeds 035g (stage C), which waits for it on the return module only.
- **Read:** `docs/model-v3/metrics.md` (range design, reading rule A2); `docs/model-v3/drivers.md` sections 1, 2 and the note of 2026-11-17 on the mean return; `docs/model-v3/inputs.md` rows I-D1a to I-D1e and I-H6a to I-H6i; `docs/model-v3/tornado.md` sections 1 to 4 (and `tornado/tornado.py`, `check.py` for the working style); `docs/model-audit/synthesis.md` sections 3, 7 and 10; `docs/agents/research.md`. The data is `Rates Data/JSTdatasetR6.xlsx` and `jst_r6.json` (UK, annual real total return on wealth to 2019, equities, housing, bonds and CPI to 2020). Nothing else need be opened.

## Goal
Recommend, with evidence, how model v3 generates return paths for the level 1 range (P10, mean, P90 over return risk) and what range to give the return parameters at level 2, so stage C can fix the return module and the revenue sign without guessing.

## Decisions (author, 2026-11-17)
- The annual tax falls on the expected annual gain, so the revenue identity uses the **arithmetic** mean return; wealth paths compound at the geometric rate. The register carries both (`drivers.md` note, 2026-11-17).
- Policy levers are swept, not sampled. Exogenous inputs are sampled at two levels reported apart (`metrics.md`): level 1 return risk, level 2 parameter ignorance.
- Every headline is reported for three horizons (transition, short, long); long is a steady-state property, not a forecast.
- UK data only, through the country pack (R11). A fixed seed and a stated sample size (R5).

## Design
Why this is needed. The tier 1 tornado ranks the mean real return first (swing 8.8 points of GDP on M1; M1 is +1.45 at central and zero at g = 3.55% a year, `tornado.md` section 1). But its low and high (2.18% and 7.47%) are the 10th and 90th percentile of 88 rolling 30-year geometric means (I-D1a). That spread is sampling variation of a 30-year path, which is level 1 return risk, so the tornado may count return risk as parameter ignorance, and level 2 has no sourced range for the true mean at all. The design also has to produce paths up to 100 years from 117 years of history, which window replay cannot do without heavy overlap.

Questions, in order. Answer each with a number, a table or a plot in the note, and say what was not tested.

1. **Generator.** Compare at least: (a) replay of historical windows (v2's 117 start years); (b) stationary block bootstrap of annual real returns, with the block length justified by the autocorrelation of the series; (c) independent draws from a fitted distribution (normal and a fat-tailed form such as Student t); (d) any regime or war-years variant the data supports. Criteria, each against the observed UK record: dispersion of 30-year geometric means (the 88 windows), loss-year frequency (I-D1c), longest loss run (I-D1d), standard deviation (I-D1b), serial correlation, and the share of 100-year paths with a long loss run. State the effective number of independent 100-year paths the history can support.
2. **Mean and its two readings.** Pin the arithmetic mean, geometric mean and standard deviation of the annual real total return on wealth on the same sample, exactly. The register gives the arithmetic mean as 4.74% (I-D1a) and `drivers.md` as about 4.76%; settle which and show that geometric is approximately the arithmetic mean minus half the variance (4.76 less 0.34 gives 4.42). Say which of the two the generator takes as its parameter.
3. **Level 2 range for the mean and standard deviation.** Give the uncertainty of the true mean and standard deviation given 117 annual observations (standard error, a bootstrap interval, and the autocorrelation correction), apart from window variation. Say whether the sub-sample means (1950 to 2019 at 5.56%, 1980 to 2019 at 6.76%) are evidence of a structural break or ordinary sampling variation, and give the author a one-paragraph choice: pool, or run the break as a named level 2 scenario. Recommend the low, central and high the register should carry for level 2, and the double-count to remove from the tornado. Do not edit `inputs.md`; list the replacement rows.
4. **Wealth composition.** I-D1a is the return on total wealth in JST. State how JST builds it (asset weights, series, deflator, timing) and whether the return on the wealth of payers (more equity and business, less pension and cash) differs materially, using I-H6a to I-H6f. Recommend whether v3 needs one return series or an asset mix by band, and what the register needs for that. Do not build the mix.
5. **The gap to 2025.** The history ends in 2019 or 2020 (I-D1e). Name what is missing (the 2022 gilt and inflation shock included) and list the options to bridge it, with source and licence for each (a later JST release, the Bank of England long-run series, ONS, Nationwide or Land Registry house prices, FTSE). Do not splice anything in; the author chooses.
6. **Sample size and seed.** For a generator you recommend, run a toy convergence test on a simple statistic (mean annual gain over 100 years, and the P10 and P90 of its 30-year mean) and report the number of paths at which P10, mean and P90 settle to 0.1 point across five seeds. The full test is stage C's.

Method and style: follow `tornado.py` and `check.py` (a script reading the data file, a second method, both run with `python3 -I`); label every assumption; mark each judgement `(J)`; never invent a source or a licence; JST's licence is unverified (I-D1a), so confirm it or say it is unconfirmed.

## Touches
New files only: `docs/model-v3/returns-method.md` (the note), `docs/model-v3/returns/` (scripts, output tables). The progress block of this brief. No edit to `inputs.md`, `metrics.md`, `drivers.md`, `tornado.md`, `outputs.yml`, `jst_r6.json`, `model_v1/`, `model_v2/`, `source/` or `pipeline/`.

## Acceptance criteria
- `returns-method.md` answers questions 1 to 6, each with a table or number, a stated recommendation and a stated limit.
- The note names one recommended generator, the parameter it takes (arithmetic or geometric), and the level 2 low, central and high for the mean and standard deviation, with the replacement register rows listed.
- The effective independent sample for 100-year paths is stated with its method.
- Scripts rerun from a clean checkout and reproduce every table in the note; a second method agrees with the main one within 0.05 points on the mean and standard deviation.
- The arithmetic mean figure is settled to one value, with the source of the 4.74 against 4.76 difference.
- `git diff --stat` shows only the Touches list.

## Checks to run
`python3 -I docs/model-v3/returns/<script>` and its second-method check; a grep that every register row id cited exists in `inputs.md`; one table recomputed by hand.

## Out of scope
Building the sampler, choosing the generator for the author, editing the register or the tornado, rerunning the tornado, running or porting `model_v1/` and `model_v2/`, wealth distribution and behavioural inputs, anything beyond UK returns.

## Open questions
The implementer asks rather than guesses: whether a later JST release is available to you and under what licence; whether the 1914 to 1918 and 1939 to 1945 years are kept in the central sample (the register keeps them; record the effect of dropping them).

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
