# 129r: Longitudinal household wealth data without a licence (access and feasibility audit)

**Status.** Done outside the repo by an external agent (chat transcript supplied by the author, 2026-11-22); recorded here by the guru after spot-checking the figures that matter. No licensed microdata was extracted, no register row or parameter changed. Evidence and confidence only; the values and rulings are the author's.

**Verification.** Checked against the source pages on 2026-11-22: **confirmed** (RF mobility and passive share; IFS pension valuation figures; IFS/ELSA drawdown; ONS blog on the Round 7 data), **corrected** (below), **not checked** (everything else; the external transcript's own scope note says it did not download or recalculate workbooks).

## Findings

| Proposition | Result | Evidence class |
|---|---|---|
| P1 active accumulation varies with starting wealth | Heterogeneity is supported broadly; the gradient by starting wealth is not published | general: identified; by income group: derived; by wealth decile and by decile x age x employment: **unset** |
| P2 wealth mobility is material | Matched WAS analysis exists (RF, 2016-18 to 2020-22, age-adjusted, deciles of wealth, split by **income** group): 76% (low-to-middle income) and 73% (higher income) moved no more than one wealth decile; 45% (higher) and 40% (low-to-middle) moved up at least one. The full transition matrix is not published | broad: identified; matrix by band, age, employment: **unset** |
| P3 retirement changes flows | IFS/ELSA (Crawford 2018; ELSA 2002-03 to 2014-15, ages 70 to 90): real net financial wealth falls about 31% overall, about 39% in the wealthier half, about 13% in the less wealthy half. Historical cohorts, financial wealth only | historical: identified; current UK: **proxy**; by pension type: **unset** |
| P4 asset composition matters | Composition by age and wealth group is published (ONS); the flow decomposition by class is not | stock shares: identified; class-level active accumulation: proxy / unset |
| P5 top tail under-coverage | Advani, Summers and Tarrant (2025): top 1% share 2016-18 ranges 14.4% to 16.5% across aggregates and sources; this is a stock sensitivity, not behaviour | stock: derived; top-tail saving and returns: **unset** |

Passive gains were **60%** of the rise in average family wealth between 2018-20 and 2020-22 (RF). The active share is not stated in the text; the residual includes saving, debt change and transfers, so it is not a saving rate.

## Pension valuation (the finding that touches our pack)

IFS: Round 8 changed Round 7 (2018-20) private pension wealth by -£2.3tn (annuity conversion, **36%**), about -£300bn (normal retirement age, about 5%) and about +£500bn (real SCAPE discounting, about 8%); total fell from £6.4tn to £4.2tn. IFS's alternative (gilt-rate discounting, directly computed annuity factors; code at `github.com/laurenceob/was-pension-wealth`) gives a mean household pension wealth of about **£450,000** for 2020-22 against about £230,000 under the ONS method. Our pack is on the ONS SCAPE basis, so the gap to RF's £17tn (BF-11, 125c) is a **valuation-basis** difference, now with a second source for the size. ONS (blog, 7 July 2026): the GAD-reviewed method was applied to 2020-22 last year; the updated **2018-20** data were published 7 July 2026; the full back series "by the end of this year".

## Corrections to the external transcript

- It says Round 7 tables were published in July 2026 and "microdata planned for Autumn 2026". The ONS blog confirms July 2026 for the 2018-20 data and "by the end of this year" for the full back series, and **says nothing about microdata or autumn**. Treat the microdata date as unverified.
- Round 9 (11,708 households interviewed; Round 8 response 41%) is taken from an ONS guide the guru did not open: **not checked**.
- The "IFS 2026" label is right: the report in `data/129r` is dated April 2026 (Delestre and O'Brien) and its replication package 9 April 2026. The March 2025 IFS file found in search is an earlier report ("£2 trillion poorer").
- Mobility is by wealth decile but the **groups are income groups**, and it is a four-year interval across the pandemic period.

Note: the RF mobility figures were already in the 099r held moments (BF-04 and AB-02 hold two-year and four-year mobility, partly as text); the audit adds the source assessment, not new data. The transcript's claim that P2 is 'much better supported than the previous research inventory suggested' overstates it.

## What can be used now (candidates, no register rows proposed)

1. RF mobility as a constraint on the model's implied transitions (a test, not a transition probability).
2. RF/IFS passive-active decomposition as a benchmark for the account.
3. IFS/ELSA drawdown as the range for a **labelled withdrawal scenario** (financial wealth; wealthier faster).
4. ONS component shares by age and band as initial-condition checks (BF-12, BF-14).
5. IFS pension valuation as a sensitivity on the pension base (the author's convention choice).
6. Advani et al. as a top-tail stock sensitivity only.

## Not established

Whether public microdata could support the desired band x life-stage matrix at adequate sample size; whether active accumulation can be separated from debt and transfers; whether WAS Round 7 and Round 8 pension variables harmonise; whether ELSA separates DB, DC and other retirement flows; whether any dataset identifies top-tail flows.

## Data-access request list (ranked, from the transcript)

1. WAS Study 7215 longitudinal microdata with linkage and longitudinal weights (safeguarded UKDS; not available to the author now).
2. WAS Round 7 revised-pension back-series (check the ONS release and what is open).
3. WAS asset-class and income variables across matched waves.
4. ELSA waves 1 to 11 financial and pension derived variables (UKDS end-user licence).
5. WAS top-tail records or an authorised supplement (separate ONS discussion).
6. ONS bespoke transition or wealth-by-stage tables (the cheapest route to BF-14 and wealth by stage).

## The IFS replication package (`github.com/laurenceob/was-pension-wealth`)

Stata code (needs Stata 17+, `ssc` packages `missings`, `fastgini`) that revalues WAS private pensions in waves 1 to 8 under four discount rates (real gilt, real AA corporate, real SCAPE, constant real). It **needs the WAS microdata** (UKDS 7215, safeguarded), which the raw data are not included for, and the repo carries **no licence file**, so reuse terms are unstated. Not runnable here. Reusable without microdata: its `rawdata/` inputs (gilt and corporate yields, CPI/CPIH/RPI series, ONS mortality `qx` tables 2008 to 2022) and the method (annuity factor from survival probabilities and forward rates), which a Python aggregate sensitivity could reimplement. Published results usable now: mean household pension wealth about £450,000 (IFS) against £230,000 (ONS) in 2020-22; at the 90th percentile of total wealth the IFS basis is about £490,000 higher and at the median about £130,000 higher; the percentage uplift is about 49% at the 30th and 34% at the 90th percentile; the top 10% share of household wealth falls from 45% (2006-08) to 42% (2018-20) on the IFS basis against 46% to 45% officially.

## Guru notes

- The licence is **not** the next step; the open sources above give validation constraints now. A bespoke ONS table request (6) is cheap and fits the validation gaps of 125c.
- Recommendation 5 of the transcript (do not add arbitrary stochastic paths) is consistent with brief 128c: that brief uses the identified JST market-return process only, labelled market-return risk, and leaves household behaviour as scenario values.
- Nothing here changes a parameter. Any use of 1 to 6 is a later brief, and register rows follow the register's rules.
