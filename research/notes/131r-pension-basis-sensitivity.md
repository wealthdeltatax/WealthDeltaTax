# 131r: pension valuation basis (IFS against ONS SCAPE) as a labelled scenario on the starting stock

Brief `docs/briefs/131r-pension-basis-sensitivity.md`. A side computation from published figures only: no pack, register, model or microdata change, no recommendation of a convention. The pack stays on the ONS SCAPE basis; the IFS basis is a scenario for the author to choose.

**Status: complete (blocks 0 to 3).** Data: `research/tables/131r-pension-basis-sensitivity/` (`ifs_published.csv`, `basis_sensitivity.csv`, `basis_checks.csv`, `basis_headline.csv`, and the two scripts that make them).

## Answer in brief
- **Level: the basis explains all of the wealth-over-GDP gap and more.** On the IFS basis the pack's pension stock roughly doubles (4,810 to 9,422 £bn, a multiplier of 1.96, range 1.94 to 1.98 on chart and rounding error), and wealth over GDP goes from 6.14 to **8.22** (8.18 to 8.26) on the pack's own definition. BF-11 observed 7.5: the basis adds 2.09 against a gap of 1.36, so it overshoots by 0.72. On the IFS definition (home contents cut by 75%) the figures are 5.67 and 7.75, 0.25 above 7.5.
- **Distribution: the basis explains almost none of the top-decile gap.** The top-decile share goes from 0.407 to **0.412** (0.401 to 0.423) against 0.50 observed: it explains 0.005 of the 0.093 gap (about 6%, at most 17%). The IFS report itself finds the top-10% share the same under both bases, 42% (published). The remaining 0.09 is not a pension valuation matter: it is the unit (per-adult families, not households), business wealth and the thin top tail, none of which the report adjusts.
- **Age: it does not help BF-14.** The IFS basis shifts wealth to the young: the 65 and over share falls from 36% to 29% (published), further from the 0.49 observed for people aged 60 and over. The pack's 0.30 is a retired person share, not a wealth share, so BF-14 is still untestable.
- **The band uplift is about 1.9 to 2.0 in every band above D1-3** (D4-5 2.02, D6-7 2.01, D8-9 1.91, D10 1.98), because the published uplift in percent of wealth is nearly flat across the distribution (49% at p30 to 34% at p90) while the pension share is about a third in each band. D1-3 is lower (1.64) and weakly identified.
- **It is a 2020-22 artefact of low gilt yields.** The two measures differ only in the discount rate (real gilt yield -1.9% against SCAPE 2.4%); the report expects the gap to narrow in 2022-24 as yields rose. A start year of 2020-22 is the year the bases diverge most.
- **Unset parts.** Decile 1, the tail above p90 and any split by stage or age inside a band have no published uplift and stay `unset`. One check missed its rounding tolerance (C6, section 3).

## 1. Published figures (block 1)
Source: Delestre and O'Brien (IFS, April 2026), *How is wealth distributed across British households? Reassessing the valuation of pensions*, the PDF held in `literature/`. Table: `research/tables/131r-pension-basis-sensitivity/ifs_published.csv` (56 rows: 38 `text`, 18 `read from chart`), made by `extract_ifs_published.py`, which stops unless each quoted phrase is found on its stated PDF page. Printed page is the PDF index minus 1. Money is in 2026 prices; 2020-22 is April 2020 to March 2022 (WAS Round 8). The report has no data table of uplifts: numbers are in running text or in charts, so the brief's `table` flag does not occur; they are `text` or `read from chart` (Figure 4 by percentile, Figure B3 by age).

| Figure (2020-22) | ONS | IFS | Page |
|---|---:|---:|---|
| Mean household pension wealth | £230,000 | £450,000 | p2 |
| Mean total household wealth (no business wealth) | £600,000 | £830,000 (+37%) | p16 |
| Aggregate household wealth | £16.3tn | £22.3tn | p16 |
| Pension share of household wealth | 38% | 54% | p2 |
| Top 10% share of household wealth | 42% | 42% | p21 |
| Total wealth, IFS over ONS, 30th / 90th percentile | | +49% / +34% (+£490,000 at p90, about +£130,000 at the median) | p20 to p21 |
| Real discount rate | 2.4% fixed (SCAPE) | -1.9% (15-year index-linked gilt) | p16 to p17 |

Cross-checks of the published numbers against each other (rounding stated in the CSV): 54% of £830,000 is £448,000 (published £450,000); 38% of £600,000 is £228,000 (published £230,000); £22.3tn over £16.3tn is 1.368 (published +37%); the Figure 4 bars give +£130,000 at the median and +£490,000 over about £1.45m at p90 (33.8%, published 34%). Both measures exclude business wealth and cut home contents by 75% (footnote 20); neither adjusts for the thin top tail.

## 2. Mapping the published percentiles to the pack bands
**Rule.** (1) In 2020-22 the two measures differ only in the pension discount rate (report, printed page 17), so the uplift in pounds is a pension revaluation: IFS pension stock = ONS pension stock + uplift. (2) Percent uplifts in the report are on total wealth after home contents are cut by 75% in both measures (its footnote 20, printed page 16; business wealth excluded in both), so they are applied to the pack's decile wealth less 0.75 of its physical wealth. (3) Deciles 2 to 9: Figure 4 gives the uplift at the percentiles 10, 20, ... 90, which are the decile edges; a decile takes the mean of its two edges (trapezoid). (4) Decile 10 has no published value and is closed by the published aggregate: uplift in pounds = (22.3 over 16.3 trillion, 36.8%) of contents-adjusted wealth, less deciles 1 to 9. (5) Bands are sums of deciles; the pack's pension stock is its own: band wealth times the one-decimal pension share, as `model/model_v3/core/cells.py` builds it.

**Error.** Figure 4 readings are by eye, +-2 points each (p30 and p90 agree with the text, 49% and 34%); the range in the table shifts every reading together, and takes the aggregate at its rounding (36.1% to 37.5%), so it is a conservative envelope. The comparison is **quantile-matched, not household-matched**: Figure 4 compares the p-th percentile under each measure, so a band is the band of that rank under each basis, and re-ranking of households between measures is not measured. Decile 10's closure has the widest range (33.0% to 41.9% of its adjusted wealth) and contains the published p90 value (34%).

**Cannot cover.** Decile 1 (below p10, no published value; bounded by the p10 reading of 4% on a base near zero, counted 0, so D1-3 is a lower bound); the tail within D10 and above (no published uplift; the report makes no top-tail adjustment); band by stage or age (section 5).

## 3. Side table: ONS stock, IFS-basis stock, uplift, class
Pack basis in £bn, 2020-22 nominal pounds (no price index enters: the report's 2026 prices appear only as ratios). Table: `basis_sensitivity.csv` (deciles, bands, all).

| Band | ONS pension stock | Uplift (range) | IFS-basis pension stock | Multiplier | Pension share of band wealth, ONS to IFS | Class |
|---|---:|---:|---:|---:|---:|---|
| D1-3 | 110.3 | +70.5 (67.0 to 74.0) | 180.8 | 1.64 | 38.3% to 50.4% | proxy; decile 1 `unset`, counted 0, so a lower bound |
| D4-5 | 379.1 | +387.2 (369.4 to 405.0) | 766.4 | 2.02 | 36.3% to 53.5% | proxy |
| D6-7 | 740.4 | +746.8 (705.5 to 788.0) | 1,487.2 | 2.01 | 32.5% to 49.2% | proxy |
| D8-9 | 1,569.7 | +1,433.4 (1,350.8 to 1,516.0) | 3,003.0 | 1.91 | 35.4% to 51.2% | proxy |
| D10 | 2,010.4 | +1,974.2 (1,738.3 to 2,210.7) | 3,984.6 | 1.98 | 36.4% to 53.2% | proxy (closed by the published aggregate) |
| All | 4,809.9 | +4,612.0 (4,521.3 to 4,703.3) | 9,422.0 | 1.96 (1.94 to 1.98) | 35.4% to 51.8% | |

No band is `observed` or `derived`: every uplift is a `proxy` (published percentile points, partly read from a chart, mapped to bands by the rule above). A `scenario` label belongs to the use, not the table (section 7).

**Checks** (`basis_checks.csv`; 15, 14 pass):
- The ONS column equals the pension stock the model's own cell table starts from (`cell_table`, read-only import): largest band difference 0.0 £bn, total 4,809.948. It is within 0.05% of the exact held 2020-22 sums (4,807.7), the rounding of the one-decimal shares.
- The pack, put on the IFS "ONS" basis, reproduces the published ONS-basis figures: mean pension wealth £231,800 against £230,000 (tolerance £5,000, the rounding), pension share of contents-adjusted wealth 38.4% against 38%, top-10% share 42.1% against 42%, using a price factor of 1.301 (2026 prices over 2020-22 pounds) implied by the stated £16.3 trillion; I have not checked that factor against a CPI series (the pack's CPI ends in 2020).
- The IFS-basis side table reproduces the published means: mean pension wealth £454,100 against £450,000 (tolerance £5,000), mean total wealth £826,200 against £830,000, top-10% share 42.3% against 42%. These are mostly consistency with the stated aggregate, since the uplift total is fixed by it; the independent parts are the multiplier (1.96 against 450/230 = 1.957), the top-10% share (a test of the closure), and the closure sitting inside the p90 range.
- **Miss (C6).** The IFS-basis pension share of contents-adjusted wealth is 54.97% against a published 54%: outside the rounding of a whole percent (tolerance 0.5) by 0.47 points. Not loosened. It is the rounding of the report's own figures taken together: the pension difference from the published shares (54% of 22.3 less 38% of 16.3 = 5.85 trillion) and the published total difference (6.0 trillion) differ by 0.15 against a combined rounding of 0.34 (C12 passes), and the side table sits at the high end of both.
- The Figure 4 bar differences (about £130,000 at the median and £490,000 at p90) agree with the text by construction of my reading, to chart precision; they are not an independent test.

## 4. How much of the 125c gaps the basis explains
Source: `basis_headline.csv`; the observed rows are BF-11, BF-13, BF-14 (`results/household-arm-validation/household-arm-validation.md`).

| Moment | Observed | Pack (ONS SCAPE) | IFS basis (range) | Basis moves it by | Gap left |
|---|---:|---:|---:|---:|---|
| BF-11 wealth over GDP, year 0 | 7.5 | 6.14 | 8.22 (8.18 to 8.26) | +2.09 against a gap of 1.36 (153%) | overshoots by 0.72 (0.68 to 0.76) |
| BF-11 on the IFS definition (contents cut 75%) | 7.5 | 5.67 | 7.75 | +2.09 | overshoots by 0.25 |
| BF-13 top-decile share, year 0 | 0.50 | 0.407 | 0.412 (0.401 to 0.423) | +0.005 of a gap of 0.093 (about 6%; at most 17%) | 0.088 (0.077 to 0.099) |
| BF-13 on the IFS definition | 0.50 | 0.421 | 0.423 | +0.002 | 0.077 |
| BF-14 retired cells' share of wealth | 0.49 | 0.301 | not computable | published 65+ share of wealth 36% to 29% | untestable; the pack figure is a person share |

- **BF-11 is mostly valuation.** The basis is more than enough: it takes the pack past the observed 7.5. What this does not show is that the Resolution Foundation figure is on the IFS basis: BF-11 gives only "about 7.5, 17tn", and its price year, denominator and exact definition are not held here. As an observation, the IFS-basis contents-adjusted total in 2020-22 pounds is 17.1 trillion (22.3 over the implied 1.301), close to 17tn; that proves nothing without the same price base. Residual in BF-11: definitional or unexplained (0.72 on the pack definition).
- **BF-13 is not a valuation gap.** The basis leaves the top-decile share almost unchanged (and the report says so: 42% under both). The 0.09 gap is definitional (families against households, the per-adult unit) or about business wealth and the top tail, which the IFS report excludes or leaves unadjusted. The side table cannot say which.
- **BF-14 is not helped.** The IFS basis moves the 65+ share of individual wealth from 36% to 29%, away from 0.49 (age 60 and over, a different age cut and unit). Wealth by stage in the pack does not exist; the person share is unchanged by the basis.

## 5. Household-arm inputs that would need a basis review under the IFS basis
None is changed here.
1. **Opening stock.** Every cell's pension class is multiplied by its band multiplier (1.64 to 2.02); total pension 4.8 to 9.4 £tn; pension share of wealth 35% to 52%; net financial, property and physical are unchanged. Retired and non-retired cells share a band mean in the pack; the IFS uplift is much larger for the young (section 6), so a band multiplier overstates the retired cells and understates the working ones.
2. **I-D1k, the pension accrual (4.83% of B.6g).** It is the ONS D.8 flow, in pounds unchanged here; on a pension stock twice as large it halves as a share of the stock. The report revalues stocks of accrued rights; a new-accrual flow under gilt discounting is a different calculation, not published. The basis of D.8 needs a review.
3. **I-D1l, the tail pension cap (£0.386m per adult).** It is the D10 mean pension per adult on the ONS basis. On the IFS basis the same construction gives about **£0.765m** (£0.720m to £0.810m on the range), using the 5.21 million D10 adults the register row states (not recomputed). The cap is a scenario constant and would move with the basis.
4. **Tail lines (D10a, D10b, the Rich List tiers).** They take D10's pension mix (36.4% on the ONS basis, 53.2% on the IFS basis before the cap). No uplift is published for the top 1% or above; the report makes no top-tail adjustment. Left `unset`.
5. **Pension return paths (I-D1h).** A gilt-discounted stock moves with gilt yields: it would fall as real yields rose from 2022 (the report expects the IFS measure to fall and the ONS one to rise in 2022-24), while the SCAPE stock moves in steps (2.4% to 1.7% real in 2023). The arm's pension holding gain would need a rate-sensitive path under the IFS basis.
6. **Stage weights and the retired cells.** By-age pension uplifts are very unequal (section 6): a band-by-stage multiplier is not identifiable from the published figures.

## 6. What stays unset
- **Decile 1** (below the 10th percentile): no published value; counted 0; D1-3 is a lower bound (multiplier 1.64).
- **Above p90 within D10**, the top 1% and the Rich List: no published uplift. The report states no adjustment for the thin top tail, so the side table does not extend to it.
- **Band by stage or age.** The open question was whether the report allows a by-age uplift as well as one by percentile: **partly, not jointly.** Figure B3 (chart only, by eye, +-10 points) gives the ratio of individual pension wealth, IFS over ONS, for April 2020 to March 2022 by age: about 470% up to 34, 265% at 35 to 49, 182% at 50 to 59, 147% at 60 to 69, 131% at 70 and over; the text gives the pension share of wealth by age (65+: 31% to 38%; 40 to 64: about 40% to 59%; 20 to 39: about 40% to 73%) and shares of aggregate wealth (20 to 39: 11% to 18%; 65+: 36% to 29%). There is no band-by-age table, so no stage multiplier is computed. Direction: retired cells gain least.
- **Years other than 2020-22.** Before 2020-22 the two measures are close in aggregate (mean total £530,000 to £720,000 on ONS against £550,000 to £750,000 on IFS, 2006-08 to 2018-20); the side table says nothing about the path.
- **Price factor (1.301).** Implied, not verified against CPI.

## 7. Proposed register row (not added)
Proposed id `I-D1m` (the next free `I-D1` letter in `model-specs/inputs.md`; not added, nothing in `registry/` or `inputs.md` is touched).

| Field | Proposal |
|---|---|
| Row | Scenario switch, pension valuation basis: multiplier on the opening pension stock, IFS gilt-discounted against ONS SCAPE (the pack), by pack band, 2020-22 |
| Unit | ratio of the IFS-basis pension stock to the ONS-basis stock |
| Low / Central / High | 1.00 (the pack, ONS SCAPE) / 1.96 (all bands; band values 1.64, 2.02, 2.01, 1.91, 1.98 from `basis_sensitivity.csv`) / 2.02 (upper rounding of 450,000 over 230,000; the side table's own range is 1.94 to 1.98) |
| Evidence class | `scenario` (the uplift is a `proxy`; the choice of basis is the author's) |
| Label | A labelled scenario of the valuation convention, not a measurement of any household's pension. The multiplier applies to the 2020-22 starting stock only; the IFS gap narrows as gilt yields rise. |
| Challenge note | One research report (IFS, April 2026), not official statistics. Band multipliers are quantile-matched proxies read partly from a chart (+-2 points) and closed for D10 from a rounded aggregate. Decile 1, the top tail and any stage or age split are unset. The side table overshoots the Resolution Foundation level (8.22 against 7.5 on the pack definition) and leaves the top-decile gap (0.09) untouched. The report's discount-rate choice (real gilt yields, -1.9% in 2020-22) is itself a convention the ONS and GAD method does not share. |
| Dependants to review if adopted | I-D1k, I-D1l, I-D1h, the tail lines, the stage weights (section 5) |

## Sources read, and not read
**Read, by `pdftotext` from the PDF itself, by page:** Delestre and O'Brien (IFS, April 2026), *How is wealth distributed across British households? Reassessing the valuation of pensions*, `literature/IFS Report - How is wealth distributed across British households.pdf`: PDF pages 3 to 4, 17 to 23 and 25 to 28 (executive summary; section 3; Figures 1 to 9), 41 and 42 (Figures B1 to B3); Figures 4 and B3 also rendered and read by eye. **Not read:** PDF pages 5 to 16 (the methodology section and Table 1), 24, 29 to 40 (including Appendix A, the outstanding issues), the replication package (it needs microdata and Stata and is out of scope), the ONS and GAD method notes, and the Resolution Foundation report (BF-11, BF-13 and BF-14 values are taken from `results/household-arm-validation/comparison.csv`, as held by 099r). Pack inputs: `data/country-packs/GBR/` (read-only); exact sums: `research/tables/102r-parameter-map-stocks-and-cells/band_composition_by_pack_band.csv`.
