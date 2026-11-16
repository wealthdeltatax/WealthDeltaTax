# Audit synthesis and v3 requirements (brief 001c, stage E)

Guru and author, 2026-11-16. Inputs: `v1-inventory.md`, `v1-errors.md`, `v2-inventory.md`, `v2-complication.md`, `lessons-so-far.md`. Neither model is fixed; v3 is a clean slate and a piece of v1 or v2 is ported only when a named whitepaper element needs it and a test exists.

## 1. What the audit found, in four lines
1. v1 is narrow and has drifted: two C.1 denominators, a stale canonical marker, 8 of 16 run entries that cannot start, 42 register items (all with a status) plus 3 new.
2. v2 tried to cover everything: 17,729 Python lines (v1: 18,136), a 1,839-line parameter file with 101 scenarios (27 unused), 55 figures and 56 tables, and an orphaned `eval_core` (2,718 lines) that cannot import.
3. Neither produces what the papers embed: 0 of 19 embedded VAL and RATES names match v2; v1 leaves 6 embeds with no file.
4. The failures were process failures (no metric register, no output-to-paper link, no tests that travel), not arithmetic ones. The lessons are in `lessons-so-far.md` and stand unchanged.

## 2. The author's reframe (2026-11-16)
The model cannot cover the whole economic parameter space. v3 therefore **estimates ranges** and the papers are rewritten to follow its results, not the other way round. The paper series becomes one whitepaper with supporting appendices, not a sequence read in order. This replaces the earlier question "which existing outputs do the papers need": the output list below is the model's, and the whitepaper cites it.

## 3. Decisions (author, 2026-11-16)
| Topic | Decision |
|---|---|
| Headline outputs | Three: government revenue; proportional tax burden on taxpayers; proportional tax savings on non-WDT taxpayers |
| Supporting output | The tolerant zone, with C.1 defined over TW(1) |
| Burden metric | Both: the annual burden as a share of wealth, and the gain-weighted effective lifetime rate. Each is compared with two baselines: the suggested wealth taxes (for example a flat stock rate and a Wealth Tax Commission style schedule) and what the same people pay today in income tax and CGT. The data is for current wealthy potential WDT payers |
| Savings metric | Two named metrics, each defined once: share of current tax bill, and share of income. The whitepaper picks one as headline |
| Range method | Sampled. Each ranged input has one stated range and a source; the model samples them and reports P10, mean and P90 per output. No hand-picked scenarios |
| Ranged inputs | Wealth distribution and threshold; asset returns and loss years; behavioural response (avoidance, migration, valuation understatement); rate schedule and design |
| Rate function | Arbitrary provided it is progressive: the incentive mathematics holds for any progressive schedule, so the rate is a revenue and burden question. v3 samples over a stated family of progressive schedules and the model enforces progressivity. The family is v2's highest-revenue thresholded shape, the logistic in ln W (see section 8); its three parameters are the sampled inputs |
| Time | Year-by-year path over N years with a steady-state summary; headline numbers reported at steady state and at a stated year |
| Allocation | One fixed order: refunds first, then reserve top-up to the targets the papers already set (short and long reserves, each 3 times the trailing mean annual refund), then relief for non-payers from the remainder. This replaces the "stated SWF share" of the first draft: the share is a result of the reserve rules, not an input |
| Corporate levy | Part of government revenue, reported as its own line, never merged into the individual WDT line |
| Retired taxes | The taxes WDT replaces are removed at the same moment WDT starts, so that revenue is not double counted. Retired together: capital gains tax, inheritance tax, stamp duties (property and shares), council tax, business rates and corporation tax. Everything else stays. The headline revenue is the net fiscal effect: WDT plus levy minus the receipts of every retired tax, with each as its own visible line (the author, 2026-11-16) |
| Threshold | Set by policy intent, not by the papers: only people with a secure living situation pay. W_min = half the median house price, per adult, read as the share a couple holds in a median home owned outright (net of mortgage). v2's value (0.5 times the median price, about £113k, about half of adults and 93% of wealth) is the starting point. The papers' canonical figures are ignored: they will all change |
| Countries | UK only in v3. Country data enters through one data pack (distribution, returns, tax baselines, units) and the core contains no UK constant, so adding a country is adding a pack, not editing code |
| Wealth data | Official survey for the bulk plus a rich-list tail; the tail's uncertainty is a stated input range |
| Build approach | Clean slate, port by exception |
| Legacy design choices | The gain ladder, the fresh-entrant heir rule and the strategy verdicts BRG, HSC, SPT and SST appear in 0 papers and are not carried over unless the whitepaper needs them |

## 4. Requirements for v3
**R1 Output manifest.** One file lists every output: ID, whitepaper element it feeds, metric, formula, unit. The whitepaper and appendices cite IDs. An output with no element does not exist (lessons 6, 6a, 7).
**R2 Metric register.** One definition per metric, in one place that code and papers cite: numerator, denominator, unit, horizon. C.1 uses TW(1) (lesson 1; v1-errors B1).
**R3 Parameter file.** Every ranged input has a low, central and high value (or a distribution), a unit and a source. No duplicated or stale values, no unused entries, no numbers typed into presentation text (lesson 3; v1-errors B7, B8; v2's 27 unused scenarios).
**R4 Layering.** Core computation, then range runner, then output writer. The core imports no presentation code and nothing imports across cores (lesson 2; v1-errors C3).
**R5 Reproducibility.** A fixed seed and stated sample size; the same inputs give the same P10, mean and P90. A run script and a smoke test that fail loudly when a file is renamed or an import breaks (lesson 4; v1 `run_all`).
**R6 Convention log.** Any change of convention (basis, denominator, rate form) is written down next to the code and in `docs/decisions.md` the day it changes (lesson 5; `BASIS_CHANGE.md` was cited and untracked).
**R7 Tests travel.** Each core has tests before anything else is built on it; nothing is retired before its tests are ported or rewritten (lessons 6b, 6c).
**R8 No side effects on import, no orphan code.** Nothing rewrites data on import; nothing unused or unported stays in the tree (lessons 6b, 8).
**R9 Size.** A stated line budget for the core and for the output layer, set in 011g stage C and checked in each build brief. As a starting proposal: the output layer is smaller than the core (v2's was 5,150 lines, the largest single source of complexity).
**R10 Progressive schedules.** The sampled rate family is monotone in marginal rate, and the model rejects a non-progressive draw instead of running it.
**R11 Country data pack.** Everything country-specific (wealth distribution, returns, baseline taxes, expenditure, currency) lives in one data pack with a documented format. The core and the output layer contain no UK name, rate or amount. v3 ships with the UK pack only; a second country is a test of this requirement, not a v3 feature (v2 ran 14 countries at once and that was a source of its bulk).

## 5. What carries over, and what does not
Candidates to port by exception (each needs a named element and a test): v2's layering and `wdt_kernel` (564 lines), the JST return series `jst_r6.json`, the loss-refund and delta-tax mechanics as stated in the papers, and the decomposition identity (residual 1.6e-13 in stage A).
Not carried over: the gain ladder, the fresh-entrant heir rule, strategy verdicts, `eval_core`, the 101 scenarios, the 55 figures and 56 tables, the v1 and v2 output scripts, and any item in `drift-register.md` (the register stays as history; v3 inherits the lessons, not the items).

## 6. Consequences for the other lanes
- **Writing:** the whitepaper outline follows the output manifest, so v3 stage A comes before the outline. The 33-entry paper series is rewritten; the old figure names disappear.
- **Research:** a brief to source the wealth survey and rich-list tail, the return series, and the behavioural ranges (including the Norway leakage figure already cited in the Project Map).
- **Web:** nothing now. The revenue calculator is replaced after v3 (author, 2026-11-16).
- **Crosslinks (007w) and retiring the legacy folders (009c):** both wait for the rewrite and v3.

## 7. Open questions
Closed on 2026-11-16: burden denominator, rate family, UK-only, corporate levy (own line), threshold approach, the list of retired taxes, the headline revenue definition (net fiscal effect, every line shown), the unit of assessment (per adult).
1. **Does the arithmetic close?** See section 10: on v2's own rough numbers the retired taxes exceed what WDT and the levy raise. Stage A of 011g tests this first.
2. **Seed and sample size.** Fixed seed recorded in every output; sample size set by a convergence test across seeds in stage C.
3. **Horizon, start years and returns.** Chosen, not calculated. Replay of historical windows (v1 and v2) or a sampled return distribution fitted to history: stage C.
4. **Data gaps** (section 9), for brief 012r.

## 8. Evidence for the rate family: v2 schedules run on UK windows
A scratch run of v2's `rates_core` on a copy outside the repo (nothing committed): UK only, `start_stride` 5, 24 windows each, `gdp_pc` indexation, scenarios as defined in `model_v2/WDT_Params.toml`. v2 is incomplete and incorrect (author, 2026-11-16), so this ranks schedules; it is not a result.

| v2 scenario | Schedule | Adults in scope | Net revenue, mean % of GDP (P10 to P90) |
|---|---|---:|---:|
| `logistic_ref` | logistic in W, 30% to 90%, every adult in scope | 100% | 7.16 (5.79 to 9.05) |
| `logistic_ln_ref` | logistic in ln W, 4% to 90%, k_ln 1 | 50% | 5.73 (4.51 to 7.18) |
| `gain_ladder` (= `baseline`) | gain ladder, top 45% | 50% | 5.43 (4.37 to 6.86) |
| `stock_ladder` | stock ladder, 2% at £1bn | 50% | 5.21 (4.24 to 6.61) |
| `logistic_ln_gain` | logistic in ln W through the gain-ladder top point | 50% | 4.79 (4.02 to 5.91) |
| `logistic_ln_stock` | logistic in ln W through the stock-ladder top point | 50% | 4.40 (3.79 to 5.20) |
| `logistic_gain` | logistic in W through the gain-ladder top point | 50% | 3.91 (3.59 to 4.27) |
| `logistic_stock` | logistic in W through the stock-ladder top point | 50% | 3.75 (3.46 to 4.13) |
- The highest figure, `logistic_ref`, taxes every adult at a 30% floor (the "former baseline" of v2); it is not a wealth tax on the wealthy, so the thresholded winner, `logistic_ln_ref`, is the family for v3.
- Of the 5.43% for the baseline, the corporate levy is 2.88 and the individual WDT 2.55 (the `levy_off` ablation gives 2.55). See open question 1.
- The papers' own rate is a logistic in W with canonical 15% to 70% and W_min £2m (`source/8_Rates_and_Revenue.md`); v2's baseline moved to the gain ladder and a W_min near £113k.

## 9. Data held and data to get (for brief 012r)
**Held:** JST R6 (`Rates Data/JSTdatasetR6.xlsx`, `jst_r6.json`: returns, prices, GDP, 18 countries); ONS Wealth and Assets Survey tables for Great Britain (`totalwealthtables.xlsx`, `financialwealthtables.xlsx`; the v2 parameters use the 2016-18 wave); Advani, Bangham and Leslie (2021) top shares and the Sunday Times Rich List (2017/18 top 1,000 and 2025 top 350) as encoded in the v2 `[rates.dist]` sections; WID extract for 14 countries (`model_v2/wid_out/`, 81 MB, the long file is not tracked); IFS composition of UK revenue (`Revenue composition spreadsheet.xlsx`); headline UK tax rates and thresholds 2000-01 to 2023 (`maintax_2023.xlsx`); public sector expenditure tables (`PSS_May_2024_TES_UPDATED.xlsx`); the 1975 and 1988 rate-table parameter sets (`7.1_260716_Rates_Data_Tables.xlsx`); the Wealth Tax Commission background paper (`Research/`).
**Useful to get (suggested, none yet checked):**
1. The latest WAS wave (the v2 distribution is 2016-18 wealth with a 2025 Rich List mixed in).
2. What the people above the threshold pay today. That is about half of all adults, not only the very rich, so the data must cover the broad middle as well as the top: income tax by income band, capital gains tax (liabilities, gains realised, by gain size), inheritance tax, dividend and savings income. Needed for the comparison with today's income tax and CGT, and for the ratio of realised to accrued gains.
2a. Receipts and payers of every retired tax: CGT, IHT, stamp duty (SDLT; LBTT and LTT outside England), council tax, and business rates and corporation tax if retired. Receipts are in `Revenue composition spreadsheet.xlsx`; who pays them, by wealth, is not.
2b. A joint distribution of income by wealth (ONS WAS or HMRC). The v2 `[rates.replacement.income_by_wealth]` table is judgement placeholders, flagged as such in the parameter file, and decides who receives the savings.
3. A reference set of suggested wealth taxes to compare against: Wealth Tax Commission proposals, the Zucman 2% above £1bn floor (already a v2 check), and any rate the author names.
4. Behavioural ranges: avoidance, migration (the Norway leakage figure already in the Project Map) and valuation understatement, each with a low, central and high value.
5. Pension, housing and business-asset treatment in the distribution (what counts as wealth for the threshold).
6. For R11: a note of what each data source covers outside the UK, so the pack format does not assume UK-only fields.

## 10. Scale check: retired taxes against what v2 raises (rough, for stage A to test)
Retired taxes, receipts as a share of GDP, `Revenue composition spreadsheet.xlsx` (IFS, "% GDP (cash)", the 2025-26 column; the later columns are forecasts):
| Tax | % of GDP |
|---|---:|
| Corporation tax | 3.37 |
| Council tax | 1.75 |
| Business rates | 1.29 |
| Capital gains tax | 0.77 |
| Stamp duties (property) | 0.66 |
| Stamp taxes on shares | 0.16 |
| Inheritance tax | 0.27 |
| **Total retired** | **8.27** |
Against that, the v2 scratch run (section 8, `gain_ladder`, UK, mean over 24 windows) shows net revenue of 5.43% of GDP, of which the corporate levy is 2.88 and the individual WDT 2.55. On these numbers the net fiscal effect would be about -2.8% of GDP (-5.7% if the individual WDT alone is counted), before any reserve top-up or relief for non-payers.
**Caveats.** The v2 figures are unfixed and average the early fill years, the periods differ (UK 2025-26 receipts against replayed windows), and the v2 distribution and rates are not v3's. This is an order-of-magnitude warning, not a result. It does say the closure question comes before the sampled ranges: if the retired list stays this long, the schedule or threshold must raise far more than v2's, or the net headline will be negative, and v3 should report that honestly. The three headline outputs may then include a break-even rate.
