# D6 provenance and status (baseline burden allocation)

Date: 15 October 2026. Status: coverage census only; no values extracted. Companion: `coverage_matrix_d6.csv`.
Hook: `band_net_position`, extended with before-and-after taxes by band. Sweep: CIT owner share 100%, 50%, 25%.

## What was opened

| Source | Status | Opened |
|:---|:---|:---|
| HMRC Capital Gains Tax statistical tables (2026 release) | partly | Table list and notes. ODS data not opened. |
| HMRC IHT liabilities commentary (2026) | verified | Headline 2023-24 figures, bands, allowances and reliefs. |
| HMRC IHT Table 12.4 (assets by net estate range) | partly | Landing page only; last data year 2019-20. |
| CEPR VoxEU column on corporate tax incidence (Fuest, Peichl, Siegloch) | partly | Column text, not the paper. |
| ONS wealth-by-decile ad hoc | not read | Search hit only. |

## Findings

1. **CGT.** HMRC publishes gains and liabilities by size of gain, and by size of gain against taxable income, by tax year. Neither is a wealth band. Mapping gains bands to wealth bands needs an assumption or a link to the WAS or a wealth-ranked cut, so the baseline CGT by wealth band is not directly observed.
2. **IHT.** 2023-24: 30,400 taxpaying estates (4.72% of deaths), 7.03bn pounds, average effective rate 13% against 40% marginal. Estate bands are available, including a 2m-7.5m, 7.5m-10m and above-10m split. The asset split by estate size is 2019-20 and older than the headline. Reliefs matter: agricultural and business property relief claimed 5.96bn pounds. Death-time liabilities need an annualisation to compare with a yearly wealth tax.
3. **Income tax and employee NI by wealth.** No linked income-by-wealth cut found. The spec's D6 gate applies: the net-change display must say the income profile is a placeholder.
4. **CIT incidence.** The one estimate opened is German local business tax: 51% borne by workers, about 49% implied for owners (about 65 cents of wages lost per euro including excess burden). Pass-through is near zero for large, foreign-owned and multi-jurisdiction firms. Not UK, and the authors do not extend it to national taxes. The 100%, 50%, 25% owner-share sweep brackets it, with 50% near the German point estimate.
5. **Employer NI.** Not searched.

## Definition fidelity

- **Band mismatch.** CGT bands are by gain and income, IHT bands by estate size at death, the model's bands by wealth. Each needs a mapping, which is an assumption to state.
- **Flow versus stock.** CGT and IHT are annual flows, so band shares need an annualisation against wealth.

## Gate

CGT and IHT aggregates by band exist, but not by wealth band. No joint income-by-wealth cut found, so the income profile stays a placeholder and the display must say so.

## Open

1. Open the HMRC CGT and IHT ODS tables and extract the bands.
2. Locate a UK joint income-by-wealth source (WAS microdata via the UK Data Service, or published tabulations).
3. Employer NI aggregates.
4. Read the UK incidence papers.
5. Decide the CIT owner-share sweep values (spec open item 2). Evidence so far supports keeping 100%, 50%, 25%.

## UK joint income-by-wealth search (15 Oct, second pass)

Result: no published tabulation of income tax or employee NI by wealth band found. What exists:

| Source | What it gives | Limit |
|:---|:---|:---|
| ONS ad hoc 008029 (1 Feb 2018) | Median household total net wealth and median net equivalised income, by net equivalised income decile, GB, July 2012-June 2016 (xls) | Medians by income decile, not wealth band; no tax or NI; one period; file not opened |
| ONS dataset "Household income, spending and wealth, Great Britain" (released 9 Mar 2022, April 2018-March 2020 only) | Decile boundaries for equivalised spending, financial wealth and property wealth | No income tax, NI or income variables on the page; single edition |
| WAS microdata, UK Data Service (EUL SN 7215; Secure Access SN 6709), waves 1-5 (2006-2016), rounds 6-8 (to 2022) | Household and individual schedules | Whether tax and NI variables are included is not stated on the page; needs the data dictionary and a user licence; microdata work, not a lookup |
| ONS quality and methods guide | Not read (session limit hit before the fetch returned) | Top-of-distribution treatment and income variables unconfirmed |

Conclusion: a joint cut would have to be built from WAS microdata (income variables unconfirmed) or from the ONS Effects of Taxes and Benefits person-level historical datasets (located, not opened), which hold tax and NI by income but not wealth. The D6 gate stands: the net-change display says the income profile is a placeholder.

## WAS data dictionary check (15 Oct, third pass)

The full variable-level dictionary was not retrievable (UK Data Service and Secure Research Service documentation not opened). What the pages opened establish:

- **Income is measured.** The WAS validation note (Wave 5) names gross regular household income as the main measure (includes equity release) and gives gross personal measures for employment, self-employment, pensions and investment income. Net measures are used where gross are unavailable.
- **Income tax and National Insurance: no derived variable confirmed.** The validation note does not address them; the ADR UK catalogue entry and the quality and methods guide do not mention them. So a tax-by-wealth cut cannot be built from the documented WAS variables alone. A gross-income-by-wealth cut can. Tax and NI would then be imputed with a tax calculator from gross income, a stated assumption and not an observed figure.
- **Income quality.** WAS gross household income was 1,132bn pounds against HMRC 977bn (FYE 2016); median gross household income 32,800 against 22,400 pounds (different units: household versus taxpayer). Employment income 721bn against 672bn; private pension income 99bn against 140bn. Round 8 removed some income questions during the telephone move and does not reflect COVID support schemes.
- **Top of the distribution.** Differential non-response is evident among very high wealth households; offshore assets, informal debts and complex trusts are not captured. This weakens any tax-by-wealth profile exactly where the levy bites.
- **Access.** End User Licence SN 7215 (waves 1-5, rounds 5-8 files listed), Secure Access SN 6709, and the ONS Secure Research Service (access level 3, SPSS). Round 8 is April 2020 to March 2022.

Conclusion: the D6 gate stands. Best available route for the net-change display is gross income by wealth band from WAS microdata with tax and NI imputed, labelled as such; the placeholder statement stays until that is built.

## Unit (added 15 Oct)

UK income tax, NI, CGT and IHT are individual, so the tax side already matches the per-adult WDT. The wealth side is household-based. A joint cut (income by wealth, by sex) therefore depends on the sharing rule decided in D3: equal split baseline, as-owned sensitivity. WAS individual files allow cuts by sex; carer and disability variables not checked.

Follow-up (15 Oct): the WBG report on the WAS says WAS splits main residence and physical wealth equally between adults (over 16) and keeps pensions individual, so joint property shares are not observed (as-owned for property cannot be built). Sex cuts exist at personal level (single women hold less than single men and than people in couples in every group; Table 4). Carer and disability variables not seen.
