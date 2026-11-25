# 145r: Pension withdrawal by age, evidence for a labelled scenario axis

Accessed 2026-11-23. Brief `docs/briefs/145r-withdrawal-and-saving-evidence.md`. Evidence and confidence only; no code, register, pack or manifest change. Scenario values are labelled as such, never a forecast, no central value.

Status: done (block 1 of brief 145r).

## 1. Summary

- The held sources contain **no pension withdrawal rate**. The nearest statement is IFS BN236 (Crawford 2018): real **net financial wealth** of people aged about 70 to 90 falls 1.8% a year on average (95% CI -3.7 to +0.1), 0.7% a year in the bottom half of the wealth distribution (CI -2.9 to +1.6) and 2.4% a year in the top half (CI -4.1 to -0.8) (pp. 11 and 13, text). It excludes pensions and ends in 2014-15, before pension freedoms; the source says pension behaviour "may be very different" (p. 20).
- Proposed, as a labelled scenario for the **retired stage only**, by wealth half, in % of the opening pension balance per year: bottom half (D1-3, D4-5) low 0.0, mid 0.7, high 2.9; top half (D6-7, D8-9, D10) low 0.8, mid 2.4, high 4.1. Evidence class `proxy`, except the zero floor (`scenario`). "Mid" is a labelled point estimate of a different asset, not a central estimate.
- `unset`: the not retired stage, the tail, gross withdrawal by pension type, behaviour after 2015, any age profile inside the retired stage.
- The draw moves value from the pension to non-pension wealth; the pension stays in the assessed base while held. A draw changes the liquid share of net worth, not net worth.


## 2. Sources read and not read

Read (opened through `website/build/to_markdown.py` or `pdftotext`; every BN236 figure is asserted on its PDF page by `withdrawal_range.py`):
- IFS BN236, *The use of financial wealth in retirement* (Crawford, June 2018), `literature/BN236.pdf`. Printed page = PDF page - 1 (checked on three pages). Pages cited are printed pages.
- ONS WAS Round 8 (April 2020 to March 2022), Table_1 of `meanmedianaggregateandpercentageofwealthbywealthcomponentandageofhouseholdreferenceperson.xlsx`: mean private pension wealth by age of the household reference person.
- Keyword search (drawdown, withdraw, decumulation) of the converted IFS "How is wealth distributed across British households" report and Resolution Foundation "Before the Fall": no withdrawal rate. The seven hits in the IFS report concern valuation and tax treatment of pensions in payment, not behaviour.

Not read, not held, listed as data requests (not fetched, not guessed): ELSA waves after 2014-15 and the ELSA pension variables (UKDS end-user licence); any DC drawdown rate after 2015 (for example FCA retirement income data, not held); WAS longitudinal microdata (UKDS 7215, safeguarded). The 129r audit's candidate "IFS/ELSA drawdown as the range for a labelled withdrawal scenario" is therefore used here with its limits stated.


## 3. Published drawdown figures (page, flag)

All rows are in `research/tables/145r-saving-shapes-and-withdrawal-range/withdrawal_range.csv` (rows W-P01 to W-P12, W-C01). ELSA, England, net financial wealth (savings and investments less financial debt, p. 6; pensions excluded), household level, 2002-03 to 2014-15.

| Figure | Value | Page | Flag |
|---|---|---|---|
| Median real net financial wealth, 12 years: cohorts 1930-34, 1925-29, 1920-24 | -14%, -13%, -1% | 2 | text |
| Age effect, all, per year | -1.8% (CI -3.7 to +0.1) | 11 | text |
| Cumulated from age 70, to 75 / 80 / 85 / 90 | 9 / 17 / 24 / 31% | 12 | text |
| Bottom half, per year (cumulated to 90) | -0.7% (CI -2.9 to +1.6); 13% | 13 | text |
| Top half, per year (cumulated to 90) | -2.4% (CI -4.1 to -0.8); 39% | 13 | text |
| Age has little systematic association with the drawdown rate once other characteristics are held | qualitative | 15 | text |
| Pension freedoms: pension behaviour may be very different | qualitative | 20 | text |
| WAS R8 mean private pension wealth by HRP age 55-64 / 65-74 / 75+ | £302,800 / £250,900 / £113,900 | Table_1 | table |

The WAS rows give ratios of 0.829 (65-74 to 55-64) and 0.454 (75+ to 65-74). They are a cross-section, not a rate: they mix cohorts, survivor selection, defined-benefit values that fall mechanically with age, and the SCAPE basis. Context only; not used as a rate.


## 4. Proposed low / mid / high by age stage

The model's stages are economic status (retired, not retired), not age (102r, 104r section 2), so a rate by age band inside a stage cannot be set; the source finds little age gradient (p. 15) and assumes a constant rate across ages (p. 11). One rate per stage and wealth half is the finest the evidence supports.

Annual draw from the pension into non-pension wealth, % of the opening pension balance, real. Scenario values, not forecasts; no central value.

| Stage | Bands | Low | Mid | High | Class |
|---|---|---|---|---|---|
| Retired | D1-3, D4-5 (bottom half) | 0.0 | 0.7 | 2.9 | mid and high `proxy`; low `scenario` (floor, the CI reaches an increase) |
| Retired | D6-7, D8-9, D10 (top half) | 0.8 | 2.4 | 4.1 | `proxy` (CI edges and point estimate of W-P07) |
| Not retired | all | unset | unset | unset | `unset` |

Wealthier faster, as the source says (p. 13). The mapping of ELSA halves (by six-year average financial wealth within a birth cohort) to pack wealth bands is an assumption: D1-5 against D6-10 is by total household wealth.

Expected consequence for the model, stated and not computed: the draw leaves net worth unchanged (a transfer between classes inside the base), raises the liquid share and so the capacity to settle from net financial wealth in retired cells, and shortens the time the pension stays illiquid.


## 5. Unset, and challenge note

**Unset** (rows W-U01 to W-U05): the not retired stage; the top 1% and tail; gross withdrawal by pension type (defined benefit in payment, defined contribution drawdown, annuity); behaviour after pension freedoms (2015); any rate by age inside the retired stage.

**Challenge.**
1. **Different asset.** The figure is the net change in financial wealth, not a withdrawal from a pension. Applied as a pension draw it conflates consumption out of wealth, bequests, and any draws from pensions into financial wealth (which would push financial wealth up). The source itself limits the transfer (p. 20).
2. **Historical cohorts.** Born 1920-34, mostly defined-benefit pensions, observed before 2015; current savers hold more defined-contribution pots with flexible access.
3. **Survivor bias.** The cumulated 31% likely overstates drawdown for those who survive to old ages (p. 12).
4. **Wide intervals.** The bottom-half CI includes a rise; the zero floor is a scenario choice, not evidence. The top-half CI (0.8 to 4.1) is the whole proposed spread.
5. **Halves.** Halves are within a birth cohort by six-year average financial wealth; pack bands rank households by total wealth.
6. **Stage.** ELSA covers ages about 69 to 91; the retired stage in WAS is economic status and includes younger retirees.
7. **Direction of a bias in net worth.** None: the draw is inside the base. A higher draw would raise liquid wealth and the capacity to settle, so the range matters for settlement, and it is not chosen for its effect on revenue or closure.


## 6. Reproduction

`python -I research/scripts/withdrawal_range.py` from the repo root (needs `pdftotext` and `openpyxl`). It asserts each BN236 figure on its PDF page and the three WAS cells, writes `withdrawal_range.csv` (24 rows) and prints one `ok:` line; it exits 1 on any failed check. Check: `python -I pipeline/check_agent_docs.py`.

