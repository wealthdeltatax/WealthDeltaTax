# 104r: parameter map, design side: cell coverage, accounting conventions, public side

Accessed 2026-11-21. Brief `docs/briefs/104r-parameter-map-design.md`. Closes deliverables C and D of the parameter map from the 103r register (`docs/research/data/103r/parameter_register.csv`). Proposals with a recommendation each; the author rules. No code, register, pack or manifest edit; no model run; no replacement for 3.5%.

Status: in progress; sections marked pending are not yet written.

## 1. Summary
(pending)

## 2. Cell coverage matrix (item 1)
Script `docs/research/data/104r/coverage_matrix.py` reads the 103r register and the 102r cell inputs and writes `cell_weights.csv`, `coverage_matrix.csv` (15 variable groups x 5 pack bands x 2 stages = 150 entries), `resolution_by_row.csv` (every 103r row with the finest resolution it supports) and `resolution_pivot.csv`. It fails if a cell or a register row is missing. The matrix classifies evidence; it holds no value for any cell.

**Definitions.** Pack bands are the five used by 102r and the schedule: D1-3 (below the assessed threshold, one remainder line), D4-5, D6-7, D8-9, D10. Stage is the author's proxy, the person's economic status in the held WAS table (four groups: working, unemployed, inactive not retired, retired); two stages are used here, **retired** and **not retired** (the other three together), and the three non-retired groups are shown separately in the weight table. The household reference person's status is a data request (SUP-1), not a blocker.

### 2.1 What is held by cell: weights only
| Pack band | Stage | Persons 16+ (WAS R8) | Rounding bound | Share of band adults | Band-edge mismatch |
|---|---|---|---|---|---|
| D1-3 | not retired | 10,662,020 | +-385,450 | 86.7% | -2.7pp of households |
| D1-3 | retired | 1,629,600 | +-116,400 | 13.3% | -2.7pp of households |
| D4-5 | not retired | 9,198,350 | +-385,450 | 82.3% | +3.4pp of households |
| D4-5 | retired | 1,978,800 | +-116,400 | 17.7% | +3.4pp of households |
| D6-7 | not retired | 5,565,890 | +-192,725 | 73.8% | -4.9pp of households |
| D6-7 | retired | 1,978,800 | +-58,200 | 26.2% | -4.9pp of households |
| D8-9 | not retired | 7,663,730 | +-192,725 | 70.2% | +0.1pp of households |
| D8-9 | retired | 3,259,200 | +-58,200 | 29.8% | +0.1pp of households |
| D10 | not retired | 5,357,350 | +-192,725 | 64.8% | +4.1pp of households |
| D10 | retired | 2,910,000 | +-58,200 | 35.2% | +4.1pp of households |

The ten cells hold 50.20 million persons (37.91 million above D1-3); this is the 102r Round 8 table, not the 52.04 million of Table 2.11 used for I-D4h (103r audit, not reconciled). Cell sizes are weighted counts, derived from whole-number percentages of band adults, grouped by GBP band edges that differ from the pack deciles by up to 4.9pp of households. Sample sizes are not published, and two source cells in the D4-5 band are suppressed in the held table (`stage_weights_by_pack_band.csv`, column `suppressed_cells_in_band`), so the D4-5 weights carry that uncertainty on top of the rounding bound.

### 2.2 Evidence class by variable group and cell
Within a group the class is the same for the four D4-5 to D10 bands except where noted: D1-3 differs for composition (shares unstable at small or negative net totals) and for income (not held below D4); the tail group applies to D10 only.

| Group | Not retired, D1-3 | Not retired, D4-5 to D10 | Retired, D1-3 | Retired, D4-5 to D10 | Evidence form | Register rows |
|---|---|---|---|---|---|---|
| G01 Cell weights (persons by band and stage) | derived | derived | derived | derived | derived from direct observation | S02, S03, S04 |
| G02 Opening band wealth (mean and total) | observed | observed | unset | unset | direct observation | S01, S29 |
| G03 Asset composition: property, net financial, physical, pension | observed (unstable shares) | observed | proxy | proxy | direct observation at band; age of reference person as a proxy for stage | S05, S06, S07, S08, S09 |
| G04 Gross debt, interest and repayment | unset | unset | unset | unset | none by band (age totals observed, aggregate cross-check only) | S10, S11, S12, S13, D04 |
| G05 Labour income and benefits (Y_L; transfer income) | unset | proxy | unset | unset | aggregate constraint; band means are register judgement rows | F-01, F-02, F-03, F-05 |
| G06 Ordinary taxes net of benefits (T_C) | proxy | proxy | proxy | proxy | modelled allocation (income decile mapped to wealth band by judgement) | F-04 |
| G07 Consumption (C), and the legacy comparator | unset | unset | unset | unset | aggregate constraint | F-06, F-25 |
| G08 Net saving (S) and saving over wealth | unset | unset | unset | unset | aggregate constraint; average-family and foreign proxies are validation moments only | F-07, F-08, F-09, F-24, F-29, F-30, F-31, F-32, F-33, F-34, F-36 |
| G09 Pension flows: contributions, accrual, withdrawal | scenario | scenario | scenario | scenario | aggregate constraint on the ONS basis; one labelled aggregate scenario (author ruling 2026-11-21) | F-10, F-11, F-13, F-35 |
| G10 Retained cash yield and the yield and gain by asset class | externally specified | externally specified | externally specified | externally specified | externally specified path (JST market portfolio); retained fraction by band unset | F-14, F-15, F-16, F-17, F-18, F-19, F-20, F-26, F-27 |
| G11 Return on classes with no held return: pension, physical, net financial | scenario | scenario | scenario | scenario | labelled scenario range per class (author ruling 2026-11-21) | F-12 |
| G12 Liability revaluation and residual O | unset | unset | unset | unset | aggregate constraint | F-21, F-22, F-23 |
| G13 Gifts, inheritances, inter-household transfers (TR) | unset | unset | unset | unset | aggregate (sector with other sectors only); legacy heir rule is the comparator | S16, S17, S18, S19 |
| G14 Transitions: band mobility, retirement entry, mortality, household formation | proxy | proxy | unset | unset | proxy: whole-distribution and income-group mobility moments; mortality age-sex only | S20, S21, S22, S23, S24, S25, S26, S27, S28, S33 |
| G15 Top tail within D10 | n/a | scenario (D10 only) | n/a | scenario (D10 only) | observed tail shares (WID, WAS) with a labelled adjustment range | S14, S15, S31, S32, F-28 |

Forms, as the brief asks, are kept apart: **direct observation** (band wealth, band composition), **derived from observation** (cell weights), **modelled allocation** (only the income-decile mapping of ordinary taxes; no other allocation is made, and none by wealth share, per the hypothesis rule), **aggregate constraint** (consumption, saving, pension flows, liability revaluation, the residual `O`), **externally specified path** (the JST market return and its split) and **scenario** (author rulings: one aggregate pension scenario; a range per class for pension, physical and net financial returns).

### 2.3 What resolution each register row supports
| Finest resolution the row supports | observed | derived | proxy | scenario | unset | endogenous | legacy | total |
|---|---|---|---|---|---|---|---|---|
| aggregate | 15 | 6 | 4 | 0 | 0 | 0 | 0 | 25 |
| market path, not household | 1 | 5 | 0 | 0 | 0 | 0 | 0 | 6 |
| band | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 5 |
| other axis (age, income, estate size, stage only) | 4 | 1 | 4 | 1 | 2 | 0 | 0 | 12 |
| top tail or distribution moment | 2 | 0 | 5 | 1 | 0 | 0 | 0 | 8 |
| band x stage | 0 | 1 | 1 | 0 | 7 | 0 | 0 | 9 |
| none | 0 | 0 | 1 | 1 | 2 | 3 | 1 | 8 |

Reading the pivot: **25 of the 73 rows are observed, derived or proxy at the aggregate**, 6 more at market-path level, 5 at band level, and only **2 at band x stage** (S03 weights as a proxy, S04 sizes derived) against **7 unset** at that resolution (S07, S13, S17, S22, S25, S26, S28). The data hold state variables at band, weights at band x stage, and every flow at aggregate only.

### 2.4 The smallest cell structure the data support
- **State and weights: five bands by two stages (ten cells).** Weights are derived per cell, opening wealth and composition are observed per band; the stage split of composition has only the age-of-reference-person proxy (S06). This is where the evidence ends; it is not a preferred number of cells.
- **Flows: one aggregate each.** Consumption, saving, pension contributions and accrual, retained cash income, liability revaluation and `O` are observed only for the household sector. A cell flow is an **allocation of that aggregate by a labelled scenario**, never an observation and never an allocation in proportion to wealth.
- **Splits that are scenarios only:** the retired cell's flows (income, drawdown, pension withdrawal); a separate high-wealth cell inside D10 (the tail is a range, G15); the inactive-not-retired and unemployed stages as cells of their own (they are weights only: unemployed 1.1% to 5.5% and inactive not retired 7.7% to 29.9% of band adults, the highest shares in D1-3); within-band distribution.
- **Not supported at any resolution:** debt and debt service, gifts and inheritances, saving by band, consumption by band, mortality by wealth, household formation.
- **Consequence for the model.** A cell model can be specified now as a **weighting and balance-sheet structure** with an aggregate flow account allocated by scenario. Treating its band by stage cells as separate behavioural units would give them flow parameters the data do not hold. The four illustrative cells of 096r (a working saver, a low-saving working cell, a retired cell, a high-wealth cell) remain illustrations.

## 3. Accounting conventions (item 2)
Script `docs/research/data/104r/conventions_worked.py` (committed, reads the 103r worked cell and the 102r composition) writes the four tables used here and fails if an identity does not close. The author's rulings of 2026-11-21 are applied as ruled: pension accrual is one labelled aggregate scenario on the ONS basis; classes with no held return get a labelled scenario range per class; `O` is a reported residual; WAS is the stock base and national accounts are validation only; two deflators are kept; F-03 is labelled `T_C`; F-21 is a `CG` term; I-W3b is context only; physical wealth is a separate asset class inside the base. Nothing below is chosen for its effect on WDT revenue or closure.

**The account (094r B1, with the label fixes).** `dNW = S + CG + TR + O - T_WDT` in real pounds of the pack's CPI basis. Assets: housing `H`, equities `E`, bonds and cash `B`/`M`, **physical wealth `K` (contents and vehicles)**, pension asset `PA`. Liabilities `D`. `S = Y_L + Y_P - I_D - T_C - C` with `T_C` taxes net of benefits (so F-03 benefits sit in `T_C`, not `TR`) and `Y_P` including retained cash income and imputed rent. `CG` is holding gain on every asset and the real revaluation of nominal positions (so F-21, the real erosion of liabilities, is `CG`, not `O`), excluding cash income already in `S`.

### 3.1 Total return against yield plus gain (the no-double-counting rule)
| Option | What it does | Identity (094r B4) and growth step |
|---|---|---|
| **A. Credit holding gain only; saving carries the retained yield once** | assets grow by `g_h`; `S` includes the retained cash income `y` | `dNW/NW = s + g_h`. The kernel growth step `W(1+r)(1-c)` is replaced by `W(1+g_h)` plus the explicit flow `S`. |
| **B. Credit total return `r = y + g_h`; saving defined net of the yield already credited** | assets grow by `r`; the saving added is `S - yW` | Same `dNW`. The kernel growth step is unchanged; `c` is replaced by `(y - s)/(1 + r)`, which is not consumption (094r B4). |
| C. Credit `r` and count `y` in `S` | yield counted twice | breaks the identity (the wrong case in the tables below) |

*Recommendation: A.* The held data support it: the yield and gain split of the JST market portfolio reproduces the register total return to 0.0024pp (C04, F-17, F-18, F-20), retained cash income is a national-account constraint (F-14), and A keeps consumption, saving and yield visible as separate lines, which B hides inside one rate. B stays as the algebraically equivalent check and as the way the legacy 3.5% comparator is reproduced. Either is correct; C is excluded.

**Worked case, D4-5, property class, per 100 of cell wealth** (`worked_d45_conventions.csv`; yield 1.409 and gain 0.617 from 103r F-20): under A the account gives 0.617 (the gain, with the yield in `S` and consumed); under B the credit is 2.026 and the saving line is -1.409, the same 0.617. Crediting 2.026 without consuming the imputed rent gives 2.026 (excess 1.409); also counting the yield as saving gives 3.435 (excess 2.818; 103r shows 3.436 and 2.819 from unrounded inputs). The other three classes of the cell (pension 36.3, physical 19.7, net financial 6.6; 62.6% of the wealth) have no held return, so each is credited a labelled scenario range per class, and the cell is not run end to end.

**Worked household, one year, recommended conventions** (`worked_household_year.csv`; illustrative, thousand pounds, not data and not a band): opening `H 600, E 200, M 100, PA 400, D 200`, net worth 1,100. `S = 60 + 18 + 6 + 2 + 12 - 8 - 12 - 58 = 20` (imputed rent 18 is income and consumption; consumption 58 is cash 40 plus that rent). `CG = 4 + 12 + 20 - 2.0 + 5.0 = 39.0`. WDT 5 paid by selling equities. Flow side `20 + 39 + 0 + 0 - 5 = 54`; stock side `612 + 199 + 98 + 440 - 195 = 1,154`, change 54: they agree. Cash closes at zero. The wrong treatment (total return credited and the yields also left in `S`) gives 90, an overstatement of exactly the 36 of yields.

### 3.2 Disposable against primary income; consumption, saving, imputed rent
| Option | Consequence |
|---|---|
| A. `S` from disposable income as the ONS ratio is built: `B.8g = B.6g + D.8 - P.31` | the published ratio (F-07) and the cash-basis ratio (F-09) are directly comparable; ordinary taxes and benefits enter as one net line `T_C` |
| B. `S` from primary income with taxes, benefits and transfers as separate flows | needs each by cell (F-01 to F-05 are aggregate or unset by band) |

*Recommendation: A for the aggregate constraint, with the account carrying `T_C` net of benefits as one line.* The ratio includes the pension adjustment `D.8`, so the ratio and `S` both state whether `D.8` is inside (it is inside the published ratio; the non-pension part is F-08). The held saving is gross of consumption of fixed capital (F-24), so it is an upper bound for the net saving the account needs; the held files give no household CFC series.
**Imputed rent.** ONS counts it in income (F-02) and in household consumption (F-06). *Recommendation:* carry it as income and as consumption, credit only the holding gain to housing, and state the consequence: model consumption `C` includes imputed rent, so cash consumption is `C` less that rent (58 against 40 in the worked household). The two other routes (drop it from both sides; or credit the total return unconsumed) give the same `dNW` for the first and an overstatement for the second.

### 3.3 Pension: contributions, accrual, withdrawals, valuation basis
| Option | Consequence |
|---|---|
| A. `PA` is an asset with explicit flows: contributions (employee in `S` out of income, employer inside `Y_L`), retained fund income in `S`, gains in `CG`, withdrawals as composition changes (`PA` down, cash up), and **accrual as one labelled aggregate scenario on the ONS basis** | consistent with the ruling; keeps pension inside net worth and the assessed base; cell allocation is a scenario key, not proportional to wealth |
| B. `PA` grows at a rate on the stock, like other assets | needs a pension return (F-12 unset) and a rate on the SCAPE stock (C02: 1.15% is not an accrual rate); mixes the ONS flow basis with the SCAPE stock |
| C. Exclude `PA` from the account | contradicts the decision that pension is inside the base |

*Recommendation: A.* **Valuation basis:** the stock is the pack's ONS Round 8 SCAPE-based valuation (35.4% of total wealth; 36.3% in D4-5); the Resolution Foundation basis (£17tn total) is validation context only and is never mixed in a row (C01); no conversion factor between bases is held (F-35 stays unset). **Flows** (F-10, F-11, F-13, F-35) are on the ONS basis, so until DR-01 reconciles them pension accrual is one aggregate scenario, not a rate on the stock. Withdrawals and decumulation (F-13) are a proxy at best and unset by cell. **Liquidity:** pension wealth is net worth and in the assessed base, but it is not cash available to consume or to pay tax before it is drawn; the consequence for settlement is in 3.8.

### 3.4 Nominal yield, holding gain, real conversion, liability sign, deflators
The account is in real pounds on the pack's CPI basis; the JST yield and gain are real by CPI (F-17 to F-20). Two deflators are kept (author ruling) and used in these places only:

| Deflator | Used for | Not used for |
|---|---|---|
| Pack CPI | the real conversion of every asset return and yield (JST), the real numeraire of the account, the real loss on nominal assets (cash) | liabilities |
| ONS household consumption (expenditure) deflator | the real erosion of nominal liabilities (F-21, a `CG` term) | asset returns |

**Wedge.** Over 1999 to 2019 the two differ by 0.49pp a year on average and up to 2.29pp (C10). With the 103r debt aggregate (£1,412bn, C09) that is about £6.9bn a year at the mean difference and £32bn at the maximum; these are the order of the term, not a calibrated value. *Recommendation:* where the account is in CPI pounds and liabilities are eroded at the expenditure deflator, report the difference as its own labelled line inside `CG` (1.0 in the worked household: 5.0 at 2.5% against 4.0 at 2.0%) rather than let it fall into `O`. **Sign:** inflation lowers the real value of a nominal liability, so erosion is a gain to the borrower (`CG` up); nominal interest paid is a negative item in `S`; principal repayment moves cash and `D` together and is in neither `S` nor `CG` (094r B3 case 4b). The corresponding real loss on nominal assets is in the cash return, not in F-21.

### 3.5 Gifts, inheritances and inter-household transfers
| Option | Consequence |
|---|---|
| A. Transfers between households cancel; no cell-to-cell `TR` in the first implementation; only the counterparty outside the sector (S16) is a flow | consistent with the evidence: nothing held by band or stage (S17, S18 unset) |
| B. A modelled bequest and gift flow between cells by a scenario key | needs an allocation the data do not support |
| C. The legacy one-heir rule (S19) | one heir per generation, no splitting; the WDT death step reads the heir's receipt as a rise from zero |

*Recommendation: A for the household account, C kept as the labelled legacy arm.* In the account a death moves the decedent's net worth to the heir within the same cell (`TR` nets to zero); a cross-cell transfer is a scenario only. The net capital transfers of the household sector with other sectors are an observed aggregate that agrees between two series (C07: -£1,043m in 2024), and capital taxes (D.91p, £8.16bn in 2024, held in `ons_ukea_household_annual.csv`) are an outflow to the public sector. **Worked:** `worked_transfer_and_fund.csv`: a gift of 30 gives `TR -30` and `+30` and a cell total of 0.

### 3.6 Survey totals against national-account totals
| Option | Consequence |
|---|---|
| A. WAS is the stock base; national accounts constrain flows and validate totals (author ruling) | the 18% to 23% gap (C08: +£2,496bn and +£2,076bn, end-2020 and end-2021) is reported, not removed |
| B. Scale WAS to the national balance sheet | removes the gap by a factor no held file separates (SCAPE against entitlements, contents and vehicles, GB against UK) |

*Recommendation: A as ruled.* Concretely: the pack's band wealth is the opening stock; national-account aggregates are checks on the sum of cell flows, expressed as ratios (saving to disposable income, retained property income to income), never as a scale on stocks; the roll-forward residual `O` is reported (2.95% and 2.36% of opening net worth in 2020 and 2021, and outside 1% in 21 of 28 years, C06), because the dwelling and land revaluation is not held. Nothing is forced to zero.

### 3.7 `O` and what is reported
`O` is the stock-minus-flow residual of the account and is a reported output, not forced to zero. It absorbs the unrecorded dwelling revaluation, survey and national-account differences and the deflator wedge unless the wedge is its own line (3.4).

### 3.8 WDT timing, settlement, and the payment source (pension and housing)
**Timing.** The account's pre-tax change `dNW = S + CG + TR + O` is the assessed delta (094r B4); the WDT `T_WDT` is deducted once at the year's end after consumption, in the kernel's order (growth, consumption, declaration, assessment, settlement); no in-year instalments. The base includes pension wealth, so the assessed delta carries pension contributions, employer contributions, fund income, pension gains and decumulation as they change `PA`: it is not the cash the household received.
**Payment source.** Whatever the source, the payment reduces net worth once and is a transfer to the public sector (4). The sources the account must allow, without assuming a rule: (a) liquid financial assets; (b) borrowing (`D` up, case 3 of 094r B3); (c) sale of housing or physical assets; (d) deferral as a liability to the state (the kernel's lien, Routes B and D); (e) pension drawdown, whose tax treatment is not held; (f) income. A, B, C, E move composition or add a liability; D moves a liability to the state.
**Liquidity facts from the base** (`liquidity_by_band.csv`, WAS Round 8 composition, observed):

| Band | Net financial % | Net property % | Physical % | Pension % | Net financial per 100 of pension plus property |
|---|---|---|---|---|---|
| D1-3 | 0.0 | 8.1 | 53.6 | 38.3 | 0.0 |
| D4-5 | 6.6 | 37.5 | 19.7 | 36.3 | 8.9 |
| D6-7 | 9.3 | 45.6 | 12.6 | 32.5 | 12.0 |
| D8-9 | 12.8 | 42.7 | 9.1 | 35.4 | 16.4 |
| D10 | 19.3 | 38.3 | 6.0 | 36.4 | 25.9 |

Net financial wealth is the only held liquid class (no instrument split); pension plus property is 74% to 78% of net worth in D4-5 to D10. A household whose wealth is mostly pension and housing cannot pay from cash on hand without a sale, a loan, deferral or a drawdown: which of these the design allows is an author ruling (section 6), not an assumption here. No payment rate is computed.

## 4. Public-side representation and settlement (item 3)
(pending)

## 5. Interface to v3 (item 4)
(pending)

## 6. Rulings table (item 5)
(pending)

## 7. Validation moments (item 6)
(pending)

## 8. Reproduction
(pending)
