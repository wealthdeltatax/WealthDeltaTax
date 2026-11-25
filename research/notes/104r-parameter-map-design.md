# 104r: parameter map, design side: cell coverage, accounting conventions, public side

Accessed 2026-11-21. Brief `docs/briefs/104r-parameter-map-design.md`. Closes deliverables C and D of the parameter map from the 103r register (`research/tables/103r-parameter-map-assembly/parameter_register.csv`). Proposals with a recommendation each; the author rules. No code, register, pack or manifest edit; no model run; no replacement for 3.5%.

Status: done.

## 1. Summary

- **Coverage (section 2).** Ten cells (five pack bands by retired or not). Only 2 of 73 register rows exist at band by stage resolution; 25 are observed, derived or proxy at the aggregate. Every flow is aggregate-only and allocated by a labelled scenario.
- **Conventions (section 3).** Recommend A: credit the holding gain only; saving carries the retained yield once (`dNW/NW = s + g_h`). B is the equivalent check; counting the yield twice is wrong (worked household: 54 against 90). Pension sits in the base on the WAS SCAPE stock basis, illiquid until drawn; two deflators (CPI for returns, expenditure deflator for liability erosion), the wedge reported as its own line; `O` reported, not forced; no cross-cell `TR`.
- **Public side (section 4).** Recommend one public ledger by class at market value; the payment is `T_WDT` in the household account and a receipt in the ledger; the household-plus-public identity sums to zero in the illustrative case (labelled as such).
- **Interface (section 5).** Gap list: a new `household.py`, pack inputs that do not exist, manifest outputs, kernel and revenue changes, tests that move, LAYER, budget and `test_groups.py` rows. The 3.5% stays a switchable comparator.
- **Rulings (section 6).** 73 rows: ready 22, scenario range 14, unset 8, further data 15, other 14. Nine questions for the author, recommendation first.
- **Validation (section 7).** Aggregate and class-level moments only (BF-01, BF-02, AB-01, BF-14, GB-01); band persistence moments need a transition rule that does not exist yet.


## 2. Cell coverage matrix (item 1)
Script `research/scripts/coverage_matrix.py` reads the 103r register and the 102r cell inputs and writes `104r-parameter-map-design-cell-weights.csv`, `coverage_matrix.csv` (15 variable groups x 5 pack bands x 2 stages = 150 entries), `resolution_by_row.csv` (every 103r row with the finest resolution it supports) and `resolution_pivot.csv`. It fails if a cell or a register row is missing. The matrix classifies evidence; it holds no value for any cell.

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
Script `research/scripts/conventions_worked.py` (committed, reads the 103r worked cell and the 102r composition) writes the four tables used here and fails if an identity does not close. The author's rulings of 2026-11-21 are applied as ruled: pension accrual is one labelled aggregate scenario on the ONS basis; classes with no held return get a labelled scenario range per class; `O` is a reported residual; WAS is the stock base and national accounts are validation only; two deflators are kept; F-03 is labelled `T_C`; F-21 is a `CG` term; I-W3b is context only; physical wealth is a separate asset class inside the base. Nothing below is chosen for its effect on WDT revenue or closure.

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
**Problem (094r A3).** The kernel moves units from the family to the state (`_move`: `f -= units; s += units`) and grows the state's units at `g`; `state_true` is read by no module outside the kernel. The revenue code reads the same payment as a cash flow `wdt = tax + refund + death_tax + heir + death_B + death_D` into a fund recursion `fund(wdt + lev, E, g, ...)` that earns `r = g` (a share `safe_share`, I-D14f, in the safe asset), pays out `R` against expenditure and reports M1c. These are two recursions of one asset with no test that ties them, and no consolidated household-plus-public account is checked anywhere.

**Options.**
| Option | What the payment becomes | Consequence |
|---|---|---|
| A. Cash only | a cash transfer into the fund; the household sells units to the market | drops the state's units; the fund recursion is the public asset; consistent with the revenue code but not with the kernel's refund cap on the state's stake |
| B. In kind only | units moved to the state; the fund is the value of the stake | needs the stake valued each year and cash flows (refunds, payout, the corporate levy) written as unit sales |
| **C. One public ledger** | a transfer to the public sector, entered once as `Rec`; the public sector holds one ledger of positions by asset class, in units, at market value; the fund balance is read from the ledger, not run as a second recursion | cash and in-kind receipts reach the same positions; the same price index values household and public units |

*Recommendation: C.*
- **What the household payment becomes.** In the household account it is `T_WDT` (net of any refund), one negative line in `dNW`; in the public account the same amount is a receipt `Rec` and an addition to the ledger. A cash settlement (the household sells units to the rest of the market, outside the modelled sectors, and pays cash) and an in-kind transfer give the same ledger; the market counterparty's change is zero because units and cash swap at one price (composition only).
- **How the stake is valued.** At market value, units times the true price index of the asset class (the kernel's `state_true` basis), the same index that values household units; the declared value is used for assessment only (the kernel's declared against true distinction is unchanged). Cash receipts are held under the fund rule (`safe_share`, I-D14f, unchanged); an in-kind receipt keeps its class. The fund's return `r_f` (D03) is then the ledger's own realised return and is endogenous, not a second input.
- **Other flows through the ledger.** Refunds are a ledger-to-household transfer (the kernel caps them at the state's stake: that cap is the ledger balance of that class). The corporate levy `lev` is an external receipt (firms), not a household flow; the fund payout `R` leaves the ledger, and is either government expenditure (public out) or a transfer to households (household income, so in `T_C` net or `S`), never both. Death taxes and the heir receipt are household-to-public payments of the same form as the annual payment.

**Reconciliation identity (no wealth or income created).** For each year, with `L` the ledger value:
`dNW_HH + dL = [S + CG + TR + O]_HH + r_pub L + Lev - R_out`
where `R_out` is the part of `R` not paid to households (a transfer to households is income inside `S` and cancels against the ledger fall), `Lev` is the external receipt and `r_pub L` the ledger's own return. The payment `T_WDT` appears as `-T` in `dNW_HH` and `+T` in `dL` and cancels. The conservation test in units is `f + s = F` per class (household units plus the ledger's units equal the starting units less units sold to or bought from the market), which the kernel already holds.

**Illustrative case (not data, not a band, no rate of tax; `public_side_identity.py`, `public_side_identity.csv`).** A WDT of 5 (thousand pounds) in one equity-like class with a gain of 2% and a cash yield of 3% in year 2:
| Case | Year | Household dNW against the no-WDT counterfactual | Ledger dL | Sum |
|---|---|---|---|---|
| cash settlement | 1 | -5.00 | +5.00 | 0 |
| cash settlement | 2 | -0.25 | +0.25 | 0 |
| in kind | 1 | -5.00 | +5.00 | 0 |
| in kind | 2 | -0.25 | +0.25 | 0 |
| cash settlement, payout R = 0.10 to households | 2 | -0.15 | +0.15 | 0 |

In year 2 the household forgoes the gain (0.10) and the yield (0.15) on the 5 units, and the ledger earns them; with a payout of 0.10 to households the household's shortfall falls to 0.15 and the ledger's change to 0.15. The legacy two recursions agree here (the stake and the fund both reach 5.25) only because one return is used and there is no payout; nothing in the code makes them agree.

**Limits.** The model stays partial equilibrium (094r B5): the market counterparty to a sale is outside the modelled sectors, prices do not respond to the sale, and nothing here is a macroeconomic closure. The ledger's holding by class needs the same class returns as the household side, including the classes with no held return (pension, physical, net financial), which are scenario ranges; the public stake is therefore a scenario for those classes, labelled in the same way.

## 5. Interface to v3 (item 4)
Gap list only. Nothing here is code; each line names what would have to exist or move, so the implementation brief can be sized. The legacy 3.5% stays a switchable comparator that reproduces today's digests (F-25, S19).

**5.1 Function signature (proposed).** A new module `model/model_v3/core/household.py` holding one household step per cell and year:

`household_step(cell, pos, flows, rets, defl, convention) -> (pos1, acct)`

- `cell`: band and stage (ten cells, section 2); `pos`: real positions by class (H, E, B/M, K, PA, D) at opening market value; `flows`: `Y_L`, `Y_P`, `I_D`, `T_C` (net of benefits, F-03), `C`, and the pension flows (contributions, accrual, decumulation) as aggregate-allocated scenario inputs; `rets`: per-class yield and holding gain from the JST split (F-20), plus the scenario ranges for pension, physical and net financial (F-12); `defl`: CPI for returns and numeraire, expenditure deflator for liability erosion (F-21); `convention`: `'A'` (recommended), `'B'` (check) or `'legacy'` (3.5% comparator).
- `acct` is the identity `dNW = S + CG + TR + O - T_WDT`, each term and the erosion wedge as its own line (section 3.4).
- `TR` is an argument fixed at zero in the first implementation (3.5).

**5.2 Pack inputs that do not exist.**
| Input | Source | Status |
|---|---|---|
| Cell weights (five bands by two stages) | `104r-parameter-map-design-cell-weights.csv` | built (102r and block 1); stage weights are a proxy (S06) |
| Composition by class including physical | `band_composition_by_pack_band.csv` | held at band; joint band by stage needs microdata |
| Yield and holding gain by class | JST split (F-20) | held for property class; others scenario |
| Scenario ranges: pension, physical, net financial return | register rows to add (F-12) | for the author to set; never a central value |
| Pension aggregate accrual, ONS basis | F-10 | one labelled scenario; DR-01 open |
| Aggregate flow constraints (`Y_L`, `Y_P`, `I_D`, `T_C`, `C`) | national accounts | aggregate only; allocation by cell is a labelled scenario |
| Expenditure deflator | national accounts | held (C10) |
| Consumption and saving by band | none | unset (F-24, F-29) |

`model/model_v3/pack/build_gbr.py` and `levers.json` have no mapping for I-D14c today; the cell inputs need a mapping and a version bump of the pack, and the legacy digests must not move when the comparator arm is selected.

**5.3 Manifest outputs that would be added.** Per cell and year: `dNW`, `S`, `CG` (with the erosion wedge line), `TR`, `O`, `T_WDT`; the consolidated household-plus-public identity of section 4 and its residual (must be zero to rounding); the `O` reported residual against the national-accounts gap (C06, C08); liquidity by class (section 3.8).

**5.4 Kernel and revenue changes.**
- `kernel.py`: `grow_and_consume` (line 324) holds the single `c = I-D14c / 100` consumption rule read by `runner/runner.py`; it becomes the legacy arm and the household step the other. `assess` (275), `declare` (343) and `step_death` (478) read `state_true` (167); the state needs the class positions, not one wealth number, before the cell account can feed them. `_move` and the revenue `fund(wdt + lev, E, g, ...)` recursion are replaced by reads from one public ledger (section 4, option C), so `core/revenue.py` and `core/burden.py` (`free_path`) change from running their own recursion to reading it.
- No kernel rule decides the settlement source; the author does (section 6, question 2).

**5.5 Tests that would move or be added.**
- Moving: `test_burden.py`, `test_revenue.py`, `test_out_burden.py`, `test_kernel.py`, `test_support.py` (they reference I-D14c, `state_true` or `state_cash`, or consumption). Under the comparator arm none should change; under the new arm the digests change and that is stated, not hidden.
- New: identity holds per cell and year (no residual); no-double-counting worked case (section 3, the household example gives `dNW` = 54 on both sides); consolidated household-plus-public sum is zero (the seven rows of `public_side_identity.csv`); the legacy comparator reproduces the stored digests; `O` is reported, not forced.
- Registration (docs/agents/code.md): a LAYER row for `household` in `tests/model/model_v3/conftest.py`; a budget row in the budgets block of `model-specs/architecture.md`; rows in `tests/model/model_v3/test_groups.py` for the new test file.


## 6. Rulings table (item 5)

Generated by `rulings_table.py` from the 103r register (73 rows), with the author's 2026-11-21 rulings applied.

| Row | Variable | Class | Finest resolution | 103r | 104r ruling | Consequence for the first implementation |
|---|---|---|---|---|---|---|
| F-01 | Labour income: compensation of employees (D.1), share of gross primary | observed | aggregate | further data | further data required | absent in the first implementation; data needed: By wealth band and stage: needs a household survey link (WAS/FRS/LCF), not held; an aggregate or a labelled scenario range stands in |
| F-02 | Self-employment and housing services: gross operating surplus plus mix | observed | aggregate | further data | further data required | absent in the first implementation; data needed: ONS split of B.2g by dwelling services versus other; not held; an aggregate or a labelled scenario range stands in |
| F-03 | Transfer income: social benefits in cash (D.62) share of disposable in | observed | aggregate | scenario range | implement with a scenario range | label fixed to T_C (taxes net of benefits); aggregate only; band means are scenario or unset |
| F-04 | Taxes on income and wealth (D.5), share of gross primary income | observed | aggregate | scenario range | implement with a scenario range | used only as a labelled range, direction from the evidence; the range is for the author to set |
| F-05 | Gross disposable income B.6g | observed | aggregate | ready | ready for implementation | used as stated in the pack, a pack addition or a reported check; value from the cited source |
| F-06 | Household final consumption (P.31) as a share of B.6g | observed | aggregate | further data | further data required | absent in the first implementation; data needed: Consumption by wealth band: LCF/WAS link; not held; an aggregate or a labelled scenario range stands in |
| F-07 | Saving ratio, published | observed | aggregate | ready | ready for implementation | used as stated in the pack, a pack addition or a reported check; value from the cited source |
| F-08 | Non-pension saving: B.8g - D.8 (the part of the ratio not pension accr | derived | aggregate | scenario range | implement with a scenario range | used only as a labelled range, direction from the evidence; the range is for the author to set |
| F-09 | Cash-basis saving ratio (CSJ8) | observed | aggregate | ready | ready for implementation | used as stated in the pack, a pack addition or a reported check; value from the cited source |
| F-10 | Pension accrual: adjustment for change in pension entitlements D.8 | observed | aggregate | scenario range | implement with a scenario range | one labelled aggregate scenario on the ONS basis; no rate on the SCAPE stock until DR-01 (author) |
| F-11 | Pension contributions (employee and employer) | proxy | aggregate | further data | further data required | absent in the first implementation; data needed: DR-02: split D.611/D.613 into pension and NIC; an aggregate or a labelled scenario range stands in |
| F-12 | Pension investment return | unset | none | unset | implement with a scenario range | author ruling: a labelled scenario range per class (pension, physical, net financial), never an estimate; evidence class stays unset; the range is for the author to set; pension, physical and net financial classes are 62.6% of a D4-5 cell and have no held return: each runs a labelled range and a cell is not run end to end without it |
| F-13 | Pension withdrawal and decumulation | proxy | other axis (age, income, estate size, stage only) | further data | further data required | absent in the first implementation; data needed: DR-03: D.622 split by scheme type and age group; an aggregate or a labelled scenario range stands in |
| F-35 | Pension valuation basis register | observed | aggregate | unset | remain unset | no conversion between pension bases; flows (ONS) and the stock (WAS SCAPE) stay on their own bases |
| F-14 | Retained cash property income (D.4 received excluding D.441 and D.442) | derived | aggregate | scenario range | implement with a scenario range | used only as a labelled range, direction from the evidence; the range is for the author to set |
| F-15 | HMRC taxable interest and dividends against ONS D.41 and D.42 | observed | other axis (age, income, estate size, stage only) | ready | ready for implementation | used as stated in the pack, a pack addition or a reported check; value from the cited source |
| F-16 | Housing services yield cross-check | proxy | aggregate | unset | remain unset | housing yield stays a reported cross-check; the JST split (F-20) is the only source |
| F-17 | Cash yield, portfolio, real (JST market portfolio, arithmetic mean of  | derived | market path, not household | scenario range | implement with a scenario range | used only as a labelled range, direction from the evidence; the range is for the author to set |
| F-18 | Holding gain, portfolio, real (JST market portfolio, arithmetic mean o | derived | market path, not household | scenario range | implement with a scenario range | used only as a labelled range, direction from the evidence; the range is for the author to set |
| F-19 | Total return, real, arithmetic (JST) | derived | market path, not household | ready | ready for implementation | used as stated in the pack, a pack addition or a reported check; value from the cited source |
| F-20 | Cash yield and gain by asset class (real) | derived | market path, not household | scenario range | implement with a scenario range | used only as a labelled range, direction from the evidence; the range is for the author to set |
| F-21 | Revaluation of nominal liabilities (real erosion) | derived | aggregate | scenario range | implement with a scenario range | label fixed to CG (real erosion of liabilities); deflator is the expenditure deflator; wedge to CPI reported as its own line |
| F-22 | Holding gains on financial assets (B.103) and other volume changes (B. | observed | aggregate | ready | ready for implementation | used as stated in the pack, a pack addition or a reported check; value from the cited source |
| F-23 | Net-worth residual O | derived | aggregate | ready | ready for implementation | O is a reported residual, not forced to zero; WAS is the stock base and national accounts are validation only (author) |
| F-24 | Aggregate saving over opening net worth (gross of CFC) | derived | aggregate | unset | remain unset | no saving rate on wealth; saving enters through each cell income side (scenario or unset), never as a share of net worth |
| F-25 | Legacy I-D14c: 3.5% consumption share of net worth | scenario | none | unset | legacy comparator only | reproduces today digests as a switchable comparator; no replacement value; only the legacy comparator run uses 3.5% |
| F-26 | Existing row I-D1a (arithmetic mean real total return 4.74) | observed | market path, not household | ready | ready for implementation | used as stated in the pack, a pack addition or a reported check; value from the cited source |
| F-27 | Existing row I-D1a2 (geometric 4.42) | derived | market path, not household | ready | ready for implementation | used as stated in the pack, a pack addition or a reported check; value from the cited source |
| F-28 | Audit I-W1c: UK financial return gap, top decile minus bottom deciles  | proxy | top tail or distribution moment | unset | remain unset | validation context only; no return difference by band is set |
| F-29 | Audit I-W3a: net active saving rate by wealth, 6 to 8% of disposable i | proxy | none | unset | remain unset | no UK saving by wealth band; direction only; the Norwegian figure is not used |
| F-30 | Audit I-W3b: gross saving rate top 1% (about 35%) | proxy | top tail or distribution moment | unset | context only | author ruling: I-W3b is context only (gross saving rate of a foreign top 1%); not a saving parameter; not used as a saving parameter |
| F-31 | Audit I-W3c: net saving share of the change in family financial wealth | proxy | aggregate | scenario range | validation moment only (unverified until SUP-7) | I-W3c stays a validation moment marked unverified until the source PDF is uploaded (author) |
| F-32 | Audit I-W3d: active saving about 40% of total wealth gain, 2018-20 to  | proxy | other axis (age, income, estate size, stage only) | scenario range | validation moment only (unverified until SUP-7) | I-W3d stays a validation moment marked unverified until the source PDF is uploaded (author) |
| F-33 | Saving by lifetime income and education (direction) | scenario | other axis (age, income, estate size, stage only) | scenario range | implement with a scenario range | used only as a labelled range, direction from the evidence; the range is for the author to set |
| F-34 | Passive and active share of wealth change (validation moments) | observed | aggregate | ready | ready for implementation | used as stated in the pack, a pack addition or a reported check; value from the cited source |
| F-36 | NMG survey saving and debt-service variables | unset | other axis (age, income, estate size, stage only) | further data | further data required | absent in the first implementation; data needed: DR-06: NMG 2011-2026 workbook contents (values), exact wave coverage per variable; an aggregate or a labelled scenario range stands in |
| S01 | Pack wealth bands (deciles of total wealth) | observed | band | ready | ready for implementation | used as stated in the pack, a pack addition or a reported check; value from the cited source |
| S02 | Band-edge mapping, GBP bands against pack deciles | derived | band | ready | ready for implementation | used as stated in the pack, a pack addition or a reported check; value from the cited source |
| S03 | Stage weights by pack band (persons 16+) | proxy | band x stage | scenario range | implement with a scenario range | used only as a labelled range, direction from the evidence; the range is for the author to set |
| S04 | Cell sizes by pack band and stage | derived | band x stage | ready | ready for implementation | used as stated in the pack, a pack addition or a reported check; value from the cited source |
| S05 | Asset composition by pack band (R8) | observed | band | ready | ready for implementation | used as stated in the pack, a pack addition or a reported check; value from the cited source |
| S06 | Asset composition by age of household reference person (proxy for stag | proxy | other axis (age, income, estate size, stage only) | validation or proxy only | validation or proxy only | age of the reference person is a proxy for stage in the composition; the joint band by stage composition needs the microdata |
| S07 | DB against DC pension split and pensions in payment | unset | band x stage | further data | further data required | absent in the first implementation; data needed: WAS pension tables (DB, DC, in payment) by decile; study 7215; an aggregate or a labelled scenario range stands in |
| S08 | Pension valuation basis for stock rows (WAS R8 SCAPE-based) | observed | aggregate | ready | ready for implementation | used as stated in the pack, a pack addition or a reported check; value from the cited source |
| S09 | Physical (contents and vehicles) wealth share by band | observed | band | ready | ready for implementation | physical wealth (contents and vehicles) is a separate asset class inside the WDT base (author); its return is a scenario range with F-12 |
| S10 | Secured debt (personal property debt), GB total and by age | observed | other axis (age, income, estate size, stage only) | further data | further data required | absent in the first implementation; data needed: WAS study 7215 gross debt by band and stage; an aggregate or a labelled scenario range stands in |
| S11 | Unsecured debt (personal financial debt), GB total and by age | observed | other axis (age, income, estate size, stage only) | further data | further data required | absent in the first implementation; data needed: As S10; an aggregate or a labelled scenario range stands in |
| S12 | Aggregate liabilities cross-check, ONS 3222 against NBS AF.L | proxy | aggregate | unset | remain unset | the 3222 against AF.L gap is reported; no debt aggregate constrains the cells |
| S13 | Debt service by band and stage | unset | band x stage | further data | further data required | absent in the first implementation; data needed: NMG household survey tables; WAS 7215 debt service variables; an aggregate or a labelled scenario range stands in |
| S14 | Top-tail share series (WID) | observed | top tail or distribution moment | ready | ready for implementation | used as stated in the pack, a pack addition or a reported check; value from the cited source |
| S15 | Top-tail adjustment for wealth missing from the WAS top | scenario | top tail or distribution moment | scenario range | implement with a scenario range | used only as a labelled range, direction from the evidence; the range is for the author to set |
| S16 | Capital transfers of households with other sectors (S.14) | observed | aggregate | ready | ready for implementation | used as stated in the pack, a pack addition or a reported check; value from the cited source |
| S17 | Gifts and inheritances by band and stage | unset | band x stage | unset | remain unset | TR is zero by cell (no inter-cell transfer); the legacy heir rule is the only transfer in the legacy arm |
| S18 | Estates passing at death by size and composition | unset | other axis (age, income, estate size, stage only) | further data | further data required | absent in the first implementation; data needed: HMRC IHT statistics (tables 12.1 to 12.3 are held as ods in 097r but not parsed for estate; an aggregate or a labelled scenario range stands in |
| S19 | Legacy heir rule (one heir, G = 30 years) | legacy | none | legacy comparator | legacy comparator only | one-heir rule kept as the labelled legacy arm; the account carries no cross-cell transfer (3.5) |
| S20 | Two-year top-decile persistence and entry | proxy | top tail or distribution moment | ready | ready for implementation | used as stated in the pack, a pack addition or a reported check; value from the cited source |
| S21 | Four-year rank correlation and same-decile share | proxy | other axis (age, income, estate size, stage only) | ready | ready for implementation | used as stated in the pack, a pack addition or a reported check; value from the cited source |
| S22 | Band-to-band and stage transition matrix | unset | band x stage | further data | further data required | absent in the first implementation; data needed: WAS 7215 longitudinal file; an aggregate or a labelled scenario range stands in |
| S23 | Age structure of the adult population | observed | other axis (age, income, estate size, stage only) | ready | ready for implementation | used as stated in the pack, a pack addition or a reported check; value from the cited source |
| S24 | Mortality, period qx and survival from 65 | derived | other axis (age, income, estate size, stage only) | ready | ready for implementation | used as stated in the pack, a pack addition or a reported check; value from the cited source |
| S25 | Working-to-retired transition hazard by band | unset | band x stage | further data | further data required | absent in the first implementation; data needed: WAS 7215 longitudinal status changes; DWP State Pension age schedule; an aggregate or a labelled scenario range stands in |
| S26 | Household formation and dissolution | unset | band x stage | unset | remain unset | cell membership fixed within a generation step; no household formation |
| S27 | Adults per household by pack band | derived | band | scenario range | implement with a scenario range | used only as a labelled range, direction from the evidence; the range is for the author to set |
| S28 | Person weights by stage within band | unset | band x stage | further data | further data required | absent in the first implementation; data needed: WAS 7215 household file; an aggregate or a labelled scenario range stands in |
| S29 | Audit I-D4a wealth to GDP | observed | aggregate | audit (no ruling) | report only (audit, no register edit) | no model use; differences reported for the guru |
| S30 | Audit I-D4b, I-D4g, I-D4h adult base and adults per household | derived | aggregate | audit (no ruling) | report only (audit, no register edit) | no model use; differences reported for the guru |
| S31 | Audit I-W5a and I-W5e top-decile and pension shares | observed | top tail or distribution moment | audit (no ruling) | report only (audit, no register edit) | no model use; differences reported for the guru |
| S32 | Audit I-W5b to I-W5d tail shares against the pack tail | proxy | top tail or distribution moment | audit (no ruling) | report only (audit, no register edit) | no model use; differences reported for the guru |
| S33 | Audit I-W4a to I-W4f mobility rows | proxy | top tail or distribution moment | audit (no ruling) | report only (audit, no register edit) | no model use; differences reported for the guru |
| D01 | T_WDT: WDT paid by the household, net of refund | endogenous | none | not applicable (endogenous) | not applicable (model output) | output of the account, not an input |
| D02 | dNW: change in net worth (the identity left-hand side) | endogenous | none | not applicable (endogenous) | not applicable (model output) | output of the account, not an input |
| D03 | r_f: fund return | endogenous | none | not applicable (endogenous) | not applicable (model output) | output of the account, not an input |
| D04 | I_D: interest paid on household debt, and principal repayment R | unset | none | further data | further data required | absent in the first implementation; an aggregate or a labelled scenario range stands in |

Counts: ready 22, scenario range 14, unset 8, further data 15, other 14 (legacy comparator 2, validation moment only 2, context only 1, validation or proxy only 1, report only 5, not applicable 3). The "ready" rows carry a source value; no row is given a value the evidence does not support, and no ruling is chosen for its effect on WDT revenue or closure.

**Questions the author must rule on (recommendation first).**
1. **Convention.** Recommend A (credit the holding gain only; saving carries the retained yield once) with B as an identity check; C is wrong. Alternative: B as the primary convention.
2. **Settlement source.** Recommend that the first implementation settles from net financial wealth only (the one liquid class) and reports the shortfall by cell, leaving the order of sources (a to f in section 4) unset. Alternative: set a legacy-style order now.
3. **Public side.** Recommend one public ledger by class at market value (option C of section 4), with `r_f` endogenous. Alternative: keep two recursions and add a tying test (option A).
4. **New register rows.** Recommend adding rows for the physical, pension and net financial scenario ranges (F-12) and the pension aggregate scenario (F-10), each marked unset until the author sets a range.
5. **Cross-cell transfers.** Recommend none in the first implementation (`TR` = 0); the legacy one-heir rule stays the comparator.
6. **Deflator wedge.** Recommend reporting the CPI to expenditure-deflator wedge as its own line inside `CG` (about £6.9bn a year at the mean, up to £32bn).
7. **Gross saving.** Recommend reporting it only as an upper bound while CFC is unset.
8. **Pension basis.** Recommend that DR-01 (SCAPE stock against ONS flows) stays open and nothing converts between bases.
9. **Joint band by stage.** Recommend commissioning the microdata cross-tab (S06) before any cell is run end to end; until then stage weights are a labelled proxy.


## 7. Validation moments (item 6)
Plans only; no moment is computed here and no tolerance is a result. The untaxed baseline is the account with `T_WDT = 0`, run with scenario ranges for the unset classes. Tolerances are proposals for the author; where a moment's resolution is coarser than the model's, only the coarse comparison is planned.

| Moment (099r) | What it is | Resolution to compare at | Use | Proposed tolerance |
|---|---|---|---|---|
| BF-01, BF-02 | share of wealth growth that is passive, excluding DB and pensions in payment (53% since 2010-12; 60% latest period) | aggregate, by period | validates the holding-gain share of `dNW`, `CG` over `S + CG` in the households with property and financial positions | baseline passive share inside 53 to 60% across the scenario range, or the range reported as not matching |
| AB-01 | passive share of financial wealth (93, 93, 82, 76, 79%) | financial classes only, by period | checks the class split of `CG` for E and B/M | within 5pp of each published period; direction (fall then rise) must match |
| BF-06 | same-decile share at ages 25-34 and 35-54 (27%, 34%) | stage (not retired) crossed with age proxy | plausibility of band persistence for the non-retired cells | only if band transitions exist (see below); otherwise not run |
| AB-02 | top decile: 80% stay, 90% of entrants from the ninth decile | D10 against D8-9 | persistence at the top | same caveat; D10 stay rate within 5pp |
| BF-04, BF-05 | mobility and mean changes, age-adjusted, by income group | income groups, not wealth bands | context only; not a pack-resolution test | none |
| BF-14 | retired shape (qualitative) | retired against not retired cells | sign check: retired cells draw down liquid wealth, pension decumulates | sign only |
| GB-01 | saving rate 10.8% (Q2 2025) against 4.0% (2022) | aggregate | reported against aggregate `S`; gross saving is an upper bound (CFC unset) | report, no tolerance |
| F-31, F-32 | I-W3c, I-W3d | aggregate | unverified until SUP-7; not used as targets | none |

Two limits. First, the cells have fixed membership within a generation step (S26) and no inter-cell transfer (3.5), so band persistence (BF-04, BF-06, AB-02) is mechanically 100% within a step; those moments need a transition rule the first implementation does not have and are listed as a gap, not as tests. Second, the baseline cannot validate a flow by band, because every flow is aggregate-only (section 2): the validation is of aggregates and of class-level direction, which is what the evidence supports.


## 8. Reproduction

From the repo root, with `python -I`: `research/scripts/coverage_matrix.py` (section 2), `conventions_worked.py` (section 3; writes four CSVs), `public_side_identity.py` (section 4), `rulings_table.py` (section 6; writes `rulings_table.csv` and `.md`). Each prints one `ok:` line and exits 1 on failure. Inputs: `research/tables/103r-parameter-map-assembly/parameter_register.csv`, `worked_cell_d45.csv`, `cross_side_checks.csv`; `102r/band_composition_by_pack_band.csv`, `cell_coverage_inputs.csv`; `099r/moments.csv`. Check: `python -I pipeline/check_agent_docs.py`.
