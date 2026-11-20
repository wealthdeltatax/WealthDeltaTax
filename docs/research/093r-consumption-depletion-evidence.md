# 093r: what I-D14c (3.5%) is, and what UK data bound for net depletion of existing wealth

Accessed 2026-11-20. Brief `docs/briefs/093r-consumption-depletion-evidence.md`; hypothesis `docs/hypotheses/household-consumption-and-wealth-replenishment.md` (tests A and C). Nothing here edits the register, the model or the manifest, and no value is chosen for its fiscal effect.

**Question, restated.** (A) What is I-D14c, where did it come from, and does any source support it? (C) What do UK data bound for net depletion of existing household wealth by band (D4-5, D6-7, D8-9, D10), keeping saving, revaluation and transfers apart?

## Answer in brief
- **I-D14c is a judgement setting with no empirical source.** It entered the v2 plan on 1 Oct as decision D16, "steady-state wealth": wealth per family "cannot compound unchecked for 100 years", so a consumption share of 2 to 5% of net worth (baseline 3.5%) was set by the user. It was a device to stop dynastic wealth running away, applied to every family alike. Nothing in the repository ties 3.5% to a measurement.
- **No UK source gives a net depletion rate by wealth band.** The register already says so for saving by band (I-W3, "no UK saving rate by wealth band"); this search found none either. The table in section 4 therefore gives no band rate, only weaker statements.
- **Aggregate evidence points below 3.5%.** UK household saving is positive (ratio 9.5% of disposable income in 2024, about 1.6% of net worth by my arithmetic), so aggregate non-valuation change is an accumulation, not a depletion. Mapped to the kernel's form, the aggregate-implied c is at most about 3.0% for any income yield up to the full 4.74% return, and about 0.4 to 1.3% at yields of 2 to 3% (section 3.2).
- **One strand points the other way.** For people aged 70 and over, net financial wealth fell on average 1.8% a year in ELSA (2.4% in the wealthier half, 0.7% in the poorer half). That is a total change including returns, for financial wealth only; it is compatible with a kernel-equivalent at or above 3.5% for that group's financial holdings.
- **Reading (item 5), for the bands that pay WDT:** net depletion of existing wealth is probably **below** 3.5% taken across the upper bands, **about equal or above** for retired holders of financial wealth, and unmeasured by band. Confidence: low to moderate on the direction for the aggregate, low for any single band. This is not a WDT result.

## 1. Test A: audit of I-D14c

| Question | Finding | Where |
|---|---|---|
| What was it meant to be? | A **steady-state device**: "Wealth per family cannot compound unchecked for 100 years." Consumption is "a fall in net worth" and enters the delta (D17). Not described as a measured consumption share, net liquidation, dissaving proxy or hazard. Closest of the four options in the hypothesis: a deliberately simplified depletion hazard | `docs/VAL_generational_model_plan.md` D16 (row 72), §9 item 9; status line says D16 "user (1 Oct), index proposed here" |
| Original rate | c swept over 2, 3, 4 and 5% of net worth per year, baseline 3.5%; one heir per generation | plan §9 item 9 |
| Units when set | The plan reads g as **nominal** (UK equity total return 10.45%, budget growth 4.51%; §9 item 7). The v2 RATES default is `basis = "real"` and v3 runs on a real return of 4.74% (I-D1a). I found no record that c was revisited when the basis changed. Whether 3.5% was chosen against a nominal or a real return is therefore unknown | plan §9 item 7; `model_v2/WDT_Params.toml` `[rates.defaults]`; `docs/model-v3/inputs.md` I-D1a |
| Uniform across households and assets? | Yes in the baseline: `c_mode = "fixed"` applies c "everywhere" to every route. v2 also had `payout_top` scenarios (for example "Top 6% consume 3.0%, rest absorb"), so heterogeneity was a scenario, not the default. The v3 kernel applies c per line but the register holds one scalar | `WDT_Params.toml` lines 711-712, `[rates.scenarios.top6_at_3]`; `model_v3/core/kernel.py` `grow_and_consume` |
| Sensitivity grid | The TOML scenarios are `c_0005` ("c = 0.5% for everyone"), `c_002` and `c_005`, plus `stationary_c`. The register's "0.5, 2 and 5" is those three; the plan's own grid was 2 to 5, so 0.5 is not in it, and when it was added is not recorded. The register's low and high are end values of the grid, not bounds | `WDT_Params.toml` lines 1133-1146; register I-D14c |
| The stationary mode | `c_mode = "stationary"` sets c so that `(1+r)(1-c) = 1+g` on the window's geometric means, keeping an untaxed holder's wealth/GDP flat (clipped to 0 to 10%). It is a closure, not an estimate. It is the mechanism behind the 090c break-even of about 2.65% | `model_v2/RATES/rates_core.py` (the `stationary` block); `docs/model-v3/wealth-ratio-diagnostic/report.md` |
| What the kernel does with it | `grow_and_consume` grows every route at g, then sells a share c of the family's units at the grown value: `W[t+1] = W[t](1+g)(1-c)`. c is a proportional drawdown of the whole stock after growth | `model_v3/core/kernel.py` lines 324-340 |
| Empirical source? | **None found** in the repository, the old papers or the v2 files. The register already says so ("Not a UK measurement: a run setting of the v2 model") and marks it (J). `docs/decisions.md` records consumption 3.5% as a "v2 default entered as a judgement row (071g)" | register I-D14c; `docs/decisions.md` |

Two small points for the guru. The register cites `WDT_Params.toml` "line 714" for `c`; the line is 711. And the 3.5% sits on the plan's nominal-return footing in the only place a rationale is written down; the register does not say so.

**Conclusion of the audit.** I-D14c stays a judgement assumption. Its stated purpose (keep wealth from compounding unchecked) is a model-closure purpose, which is a different thing from "net depletion of existing wealth", the quantity test C asks the data about.

## 2. Test C: sources

How read: every source below was read through WebSearch or WebFetch, which return summaries; figures are as the tool reported them and **page numbers are the tool's, not checked against the PDFs**. The shell cannot reach the sites. Licences: ONS statistics are Open Government Licence v3.0; Resolution Foundation reports are published under a Creative Commons non-commercial no-derivatives licence (as shown on the document); IFS licence not seen. Only figures and short paraphrase are used; nothing is reproduced. Sources already held in the register (Fagereng and others, Bangham and Leslie) are cited by row and were not re-read.

### 2.1 Saving, revaluation and transfers, aggregate

| # | Source | Quantity | Number | Sample, year, coverage | Definitions and what is mixed | Read |
|---|---|---|---|---|---|---|
| 1 | ONS, Blue Book 2026 national accounts at a glance; Quarterly sector accounts | Household saving ratio | 9.5% in 2024, 9.6% in 2025; quarterly 9.9% (Q4 2025), 8.9% (Q1 2026) | UK household sector, annual and quarterly | Saving as a share of gross disposable income **plus pension accumulations**; gross of consumption of fixed capital; property income counted as income (national-accounts convention; not stated in the pages read, imputed rent included), so **saving includes retained income and excludes holding gains**; includes pension saving shown separately | fetched |
| 2 | ONS, Regional GDHI 1997 to 2024 | Gross disposable household income | Nearly £1.8 trillion in 2024 (provisional) | UK | GDHI, current prices | fetched (search text) |
| 3 | ONS, National balance sheet (Dec 2025; preliminary June 2026) | Household net worth | £10.7tn (2024) and £10.8tn (2025) in the June 2026 bulletin; +£146.1bn in 2025. The Dec 2025 bulletin: +£217.7bn to £10.8tn between 2023 and 2024; 2023 fell 2.4% (£11.2tn to £10.9tn, driven by land). Estimates are revised between vintages | UK household sector, market values | Net worth **mixes** saving, revaluation, depreciation and transfers; the bulletins do not split the change | fetched (search text) |
| 4 | ONS, Households' finances and saving, UK: 2020 to 2024 | Saving ratio path; no wealth decomposition | Q4 2019 5.8%; Q2 2020 27.4% peak; Q2 2022 6.6%; Q1 2024 11.1%. No annual series, no net-worth split, no revaluation figures | UK | The article says non-labour income includes changes in the value of household-owned pension funds (I read this as pension accruals, not holding gains on direct assets; not confirmed) | fetched |

### 2.2 By household group

| # | Source | Quantity | Number | Sample, year, coverage | Definitions and what is mixed | Read |
|---|---|---|---|---|---|---|
| 5 | ONS, Household income, spending and wealth in Great Britain (experimental) | Spending, income and wealth for households in the top fifth on **all three** measures | Income £86,000, net wealth £2,135,600, spending £58,700; 8.6% of households. Bottom fifth on all three: income £10,500, wealth £14,700, spending £12,300; 7.0% of households | LCF (about 5,000 households a year) statistically matched onto WAS (about 10,000 per wave); LCF FYE 2017 and 2018 with WAS 2016-18 (the WAS period is taken from the page address); Great Britain; 15 matching variables, 100 imputations averaged | Spending is total consumption expenditure **excluding rent and mortgage interest**; wealth is net property, financial, pension and physical wealth; wealth is equivalised here (unlike the total-wealth bulletin); income definition and equivalisation of the income and spending figures not confirmed; the top group is selected on high income as well as wealth. Matched data are experimental; the link rests on the matching variables | fetched |
| 6 | Crawford (2018), IFS Briefing Note BN236, The use of financial wealth in retirement | Annual change in **net financial wealth** of older people | All: -1.8% a year (95% CI -3.7 to +0.1), cumulatively 31% from age 70 to 90. Wealthier half: -2.4% a year (CI -4.1 to -0.8), 39% cumulative. Less wealthy half: -0.7% a year (CI -2.9 to +1.6), 13% cumulative. Cohort medians 2002-03 to 2014-15: born 1930-34 down 14%, 1925-29 down 13%, 1920-24 down 1% | ELSA (England, aged 50 plus), seven biennial waves 2002-03 to 2014-15; regression samples 4,759 (full) and 2,351 (waves 4 to 7); six-year panels need positive net financial wealth at both ends | Net financial wealth is savings and investments less financial debt; **excludes** housing, other property and pensions; household level, CPI-deflated, 2015 prices. It is the **total** change, so it **mixes** saving, returns and revaluation, and the note does not say whether gifts are netted out. The author says the top-half figure probably overstates drawdown, and cumulating the rate overstates it for the long-lived. Halves of the age-relative wealth distribution, not UK-wide wealth bands | fetched |
| 7 | Broome and Kanabar (Oct 2025), Resolution Foundation, Before the fall | Split of the rise in mean family wealth per adult into **passive** (asset-price) and **active** accumulation | 2018-20 to 2020-22: about 60% passive, 40% active. From 2010-12: 53% passive, 47% active. Median two-year passive gain 8% in the middle wealth quintile, zero in the bottom quintile (2018-20 to 2020-22). No split by decile | WAS longitudinal, Great Britain, 2006-08 to 2020-22; families | **Passive** is the change implied by average returns on the opening portfolio by asset class; **active** is the residual: saving, debt repayment and transfers (gifts and inheritances), pension contributions presumably included but not stated. The pandemic window carries record saving. DB pensions and pensions in payment are excluded. Annex 2 gives no decile figures | fetched |
| 8 | Bozio, Emmerson, O'Dea, Tetlow (2013), IFS WP 13/30, Savings and wealth of the lifetime rich | Saving rate against permanent income, UK | Positive relationship between saving rates, wealth accumulation and permanent income; **no numbers seen** (abstract page only) | UK consumption data and a linked survey-wealth and earnings-records dataset | Income-based saving rates, not wealth-based | fetched (abstract) |

### 2.3 Already in the register (not re-read)
- **I-W3a, I-W3b** (Fagereng, Holm, Moll, Natvik 2019, Norway 2005-2015): net active saving about 6 to 8% of disposable income, roughly flat above the 20th percentile; gross saving rate of the top 1% about 35%, but that includes capital gains held, so it is not comparable with a saving ratio. Foreign.
- **I-W3c** (Bangham and Leslie 2020, GB financial wealth 2008-10 to 2016-18): net saving 7 to 24% of the change in family financial wealth, the rest asset prices and yields; not by band.
- **I-W3d** (Resolution Foundation, 2018-20 to 2020-22): active saving about 40% of total wealth gains; the same finding as row 7 above.

### 2.4 Transfers (kept apart)
- IFS (Boileau and Sturrock) on significant gifts and loans in Great Britain (WAS): over eight years, transfers received are worth 0.5% of income in the bottom income fifth and 2.6% in the top fifth, and more than half the value of gifts is given by the wealthiest (as the search text reads; fetched only as a snippet).
- Nolan, Palomino, Van Kerm, Morelli (2020), WAS: the top quarter of the wealth distribution had received two thirds of the wealth transferred, the bottom quarter 15%.
- The kernel keeps heirs and gifts outside c (v2 `heir_rule`, D6, D20), so these belong to a transfer line, not to the depletion rate. **No UK figure was found for gifts and bequests given as a share of the giver's wealth by band**, which is what "net of gifts given" would need.

## 3. Reconciliation

### 3.1 Definitions that do not match
- **Saving in the accounts includes retained income; the Resolution Foundation's "active" does not.** ONS saving counts property income (dividends, interest, imputed rent) as income, so it enters saving; the RF's "passive" is the return on opening assets, so income yield sits on the passive side. The two series cannot be added or compared as one number. The kernel's g is a **total** return (I-D1a), income and gains together.
- **ELSA's change is total; the kernel's c is not.** A total change of -2.4% includes returns. The non-valuation part is the total less the return on those holdings. The note gives no return, so a kernel equivalent needs one: at a zero return c is about 2.4% (wealthier half); at a real return of 2% it is about (0.02 + 0.024)/1.02 = 4.3% (my arithmetic, return **(J)**).
- **ONS spending excludes rent and mortgage interest; wealth is equivalised and includes pension wealth.** Row 5's ratios are not like-for-like with a consumption share of net worth.
- **Survey and accounts.** WAS and ELSA are household surveys with top-tail under-coverage (the register's S5); the sector accounts are aggregates for all UK households including non-profit bodies. I have not tried to reconcile them. Net worth differs by vintage (£10.7tn to £11.1tn for 2024).
- **Gross against net.** The saving ratio is gross of consumption of fixed capital (dwelling depreciation), so it overstates saving that adds to net worth.

### 3.2 My arithmetic (labelled, not source figures)
1. **Aggregate saving against net worth.** 9.5% of nearly £1.8tn is about £170bn (the ratio's denominator adds pension accumulations, so the pound figure is approximate). Over £10.7tn of household net worth that is about **1.6% a year**, gross and including pension saving and retained income.
2. **Mapping to the kernel.** With total return r = y + g_h (income yield y, holding gains g_h) and non-valuation change s (saving, as a share of opening wealth), the kernel's `W[t+1] = W[t](1+r)(1-c)` gives `c = (y - s)/(1 + r)`. This is an identity under the kernel's form, not a behavioural estimate. With s = +1.6% and r = 4.74%: y = 2% gives c = 0.4%; y = 3% gives 1.3%; y = 4% gives 2.3%; the ceiling y = r gives 3.0%. So **for every feasible yield the aggregate-implied c is below 3.5%**, with a margin of only 0.5 points at the extreme. The yield is not sourced here (it needs household property income and holding gains from the financial accounts, not retrieved); y is **(J)**. If net saving were zero rather than +1.6%, c = y/(1+r), which reaches 3.5% only at y of about 3.7%.
3. **Top group in the ONS matched data.** Income less spending is £86,000 - £58,700 = £27,300, about **1.3% of £2,135,600** net wealth; spending is about 2.7% of net wealth. Group averages, income not confirmed as disposable, excludes housing costs: indicative only.
4. **Older financial wealth.** See 3.1: c from -1.8% to -2.4% total change is 1.8 to 2.4% at zero return, higher at positive returns.

## 4. What the evidence supports (the register is not edited)

Rate columns are net depletion of existing wealth in the sense of the kernel's c (consumption and net outflow withdrawn after growth, expressed as a share of the grown stock), **not** the share of wealth consumed. "J" means judgement.

| Band | Low | Central | High | Data or J | Gap to the kernel's 3.5% on every line | Weaker statement the evidence supports |
|---|---|---|---|---|---|---|
| D4-5 | no value | no value | no value | none | not measurable | Mid-wealth: median two-year passive gain 8% in the middle quintile (RF, 2018-20 to 2020-22). No saving or depletion rate by band. IFS reports that most older homeowners in ELSA do not access housing wealth (England, 50 plus) |
| D6-7 | no value | no value | no value | none | not measurable | As D4-5. Nothing UK-specific by band |
| D8-9 | no value | no value | no value | none | not measurable | As D4-5. Nothing UK-specific by band |
| D10 | no value | no value | no value | none | not measurable | Top-fifth-on-all-three households: income exceeds spending by about 1.3% of wealth (row 5, my arithmetic), spending about 2.7% of wealth. Foreign (Norway) top-1% saving is positive but includes held gains (I-W3b) |
| All households, aggregate | about 0.4 | about 1.3 | about 3.0 | **J** for y (2, 3 and the ceiling 4.74); the saving figure is data (ONS, gross, 1.6% of net worth) | **-3.1, -2.2 and -0.5 points** (aggregate-implied c below 3.5 at every yield) | Positive aggregate saving; net worth rose in each year reported except 2023, where revaluation (land) dominated |
| Retired holders of financial wealth (ages 70 plus, ELSA) | 0.7 (poorer half, total change) | 1.8 (all) | 2.4 (wealthier half) | **Data** for the total change; kernel equivalent needs a return **(J)** | At zero return -2.8, -1.7 and -1.1 points; at a 2% return about +0.8 for the wealthier half (4.3 against 3.5) | Financial wealth only, excludes housing, other property and pensions; includes returns; probably overstates drawdown for long-lived (the authors) |

**What the evidence cannot support.** A rate for any one band, a UK saving rate by wealth band, or the share of top-decile wealth change that comes from income-funded saving (item 6). **What it can support:** an aggregate direction (positive net saving, so an aggregate c at or below about 3%), a retired-financial-wealth figure (0.7 to 2.4% total change), and a top-group indicator (income above spending by about 1.3% of wealth).

## 5. Plain reading

For the bands that pay WDT, the evidence suggests net depletion of existing wealth is **below 3.5% on balance**: the household sector as a whole saves, and the one UK group matched on income, spending and wealth that sits at the top spends less than its income. It is **about equal or above 3.5% for one subgroup**: retired holders of financial wealth, where ELSA shows a decline of 1.8 to 2.4% a year before adding back the return those holdings earned. No source measures a band, so the reading is about direction.

**Confidence: low to moderate for the aggregate direction (the arithmetic is an identity, but y is a judgement and the saving ratio is gross); low for the bands that pay WDT.** The aggregate is dominated by the upper bands (ONS 2012 to 2014 put the top 10% at 45% of aggregate wealth), but the saving ratio is income-based and not allocated by wealth. The opposite direction cannot be ruled out for older payers whose wealth is mostly financial, or for working-age payers whose income funds saving (see section 6). This is not translated into a WDT result.

**Rows the guru might propose (placeholders, not entered):**
- **Reclassify the framing of I-D14c.** Its Notes say "framing value, not an estimate", which stays correct. The audit adds the original purpose (steady state, 1 Oct, set against nominal returns). The author may wish the register to say so.
- **A: aggregate non-valuation saving, % of opening household net worth, UK:** low, central, high not set. One data point, about 1.6% (my arithmetic from ONS, 2024); a series would need ONS annual household saving in pounds and net worth by year. Data, with the gross, pension-inclusive caveat.
- **B: financial wealth change, ages 70 plus, % a year, ELSA:** 0.7 / 1.8 / 2.4, **data** (total change, financial wealth only, 2002 to 2015).
- **No row for any band D4-5 to D10.** No data support one.

## 6. Income-funded saving at the top (pointer for specification B only)
- **No UK figure** on the share of top-decile wealth accumulation that comes from saving out of income against returns. The Resolution Foundation's split is by family mean and for the whole distribution (about 40 to 47% active), not top-decile, and its "active" includes debt repayment and transfers.
- **Norway** (I-W3a, I-W3b): net active saving 6 to 8% of disposable income flat above the 20th percentile; the 35% top-1% rate includes held gains.
- **UK** (Bozio and others 2013, row 8): saving rises with permanent income; the numbers were not read. The full paper (http://www.ifs.org.uk/wps/wp201330.pdf) is the first thing to read for specification B.
- **ONS matched data** (row 5): income less spending of about 1.3% of wealth for the top-fifth-on-all-three group.
- Fiscal and income definitions differ across these four; none is a band-level wealth-based saving rate.

## 7. Open questions for the author
1. **Is the aggregate comparison enough to relabel?** The audit finds a model-closure origin, and the evidence points below 3.5% in aggregate. Proposed resolution: leave I-D14c as (J) and add the origin to its Notes at the next register edit; no value change.
2. **Retired-wealth subgroup.** It points the other way; the kernel treats all lines alike. Proposed resolution: let the later code brief (tests B, D to F) decide whether to give older holders their own c, only after the author rules on this note.
3. **Next evidence to fetch.** (a) Bozio and others full text; (b) ONS household property income and holding gains by year (needed for y); (c) a band-level source if one exists (WAS microdata, the Bank of England NMG survey), which the author could request or upload. Proposed resolution: fetch (a) and (b) in a follow-up, since they bound the aggregate row; (c) is a data request, not a search.

## Sources
- ONS, Blue Book 2026, national accounts at a glance: https://www.ons.gov.uk/economy/grossdomesticproductgdp/compendium/unitedkingdomnationalaccountsthebluebook/2026/nationalaccountsataglance
- ONS, Quarterly sector accounts, UK: October to December 2025: https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/bulletins/quarterlysectoraccounts/octobertodecember2025
- ONS, Regional GDHI 1997 to 2024: https://www.ons.gov.uk/economy/regionalaccounts/grossdisposablehouseholdincome/bulletins/regionalgrossdisposablehouseholdincomegdhi/1997to2024
- ONS, National balance sheet 2025 and preliminary 2026: https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/bulletins/nationalbalancesheet/2025 and https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/bulletins/thenationalbalancesheetandcapitalstockspreliminaryestimatesuk/2026
- ONS, Households' finances and saving, UK: 2020 to 2024: https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/articles/householdsfinancesandsavinguk/2020to2024
- ONS, Household income, spending and wealth in Great Britain: https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth/articles/householdincomespendingandwealthgreatbritain/latest
- ONS, Wealth in Great Britain 2012 to 2014 (top 10% share): https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth/compendium/wealthingreatbritainwave4/2012to2014/mainresultsfromthewealthandassetssurveyjuly2012tojune2014
- Crawford (2018), IFS BN236: https://www.ifs.org.uk/sites/default/files/output_url_files/BN236.pdf
- Broome and Kanabar (2025), Resolution Foundation, Before the fall: https://www.resolutionfoundation.org/app/uploads/2025/10/Before-the-fall.pdf
- Bozio, Emmerson, O'Dea, Tetlow (2013), IFS WP 13/30: https://ideas.repec.org/p/ifs/ifsewp/13-30.html
- Boileau and Sturrock (2023), IFS WP 2023/08: https://ifs.org.uk/sites/default/files/2023-02/WP202308-Who-gives-and-receives-substantial-financial-transfers.pdf
- Nolan and others (2020), The wealth of families: https://stonecenter.gc.cuny.edu/files/2020/08/Intergenerational-Wealth-Transfers-Report-Aug-2020.pdf
- Repository: `docs/VAL_generational_model_plan.md`; `model_v2/WDT_Params.toml`; `model_v2/RATES/rates_core.py`; `model_v3/core/kernel.py`; `docs/model-v3/inputs.md` (I-D14c, I-D1a, I-W3a to I-W3d); `docs/model-v3/wealth-ratio-diagnostic/report.md`; `docs/decisions.md`.
