# 095r: UK evidence and calibration map for household wealth flows (test C)

**Corrections and source locations: see `research/notes/095r-source-acquisition-and-verification.md` (2026-11-21), which resolves the "recheck" items: state pension treatment corrected, the 92% gains share is ranked by remuneration (Advani, Bangham and Summers 2020), the OBR 7% and Resolution Foundation 34% pension figures are not a common range, and NMG microdata are public.**

Accessed 2026-11-20. Brief `docs/briefs/095r-uk-household-flow-evidence-map.md`; hypothesis `research/hypotheses/household-consumption-and-wealth-replenishment.md` (sections 10 to 14); predecessor `research/notes/093r-consumption-depletion-evidence.md`. Nothing here edits the register, the model or the manifest, and no value is chosen for its effect on WDT revenue. Proposed register rows are in section 7 only.

**Question.** For each household wealth flow in ΔNW = S + CG + TR + O − T_WDT, does UK evidence give a measured **level**, **rate**, **transition**, a **bound**, or is the flow a **gap**? The map feeds the cohort design (096r). It does not map the kernel (094r), choose a parameter or backcast anything.

## Answer in brief
- **No UK source identifies any flow by wealth band as a rate on wealth.** Every figure is aggregate, by income, by age, or for the whole distribution. Following the author's decision, this note gives **no replacement for the legacy 3.5% (I-D14c) and no band-level depletion rate**.
- **Best-measured flows (aggregate levels):** household saving (ONS saving ratio and sector accounts), pension contributions and accrual (ONS Table 29 / D8 and the ONS pension wealth bulletin), capital gains in aggregate (national balance sheet revaluations).
- **Partly identified:** the passive/active split of wealth change (Resolution Foundation, WAS panel, about 53 to 60% passive, 40 to 47% active). It separates returns on opening holdings from a residual that **mixes** saving, debt change and transfers, so it identifies none of those three alone.
- **Bound only:** drawdown (ELSA, ages 50 plus, financial wealth only, -1.8% a year, total change including returns), transfers (levels by income and wealth group, not as a share of the giver's wealth), debt service (no band split found).
- **Gaps:** (i) saving as a share of wealth by band; (ii) the share of top-decile wealth change from income-funded saving against returns (brief item 6); (iii) transfers given as a share of giver's wealth; (iv) retained property income by band; (v) capital gains by wealth band as a share of opening wealth. Each is named below with the data that would close it.
- **The aggregate saving ratio is not converted into a depletion rate here**, per the author's decision. Where 093r's identity is mentioned it is cited as a mapping, not an estimate.

## 1. Entries by flow

Status key: **L** level (a stock or flow amount), **R** rate (a share of opening wealth or income), **T** transition (a change between waves or bands), **B** bound, **G** gap. "How read": WebSearch/WebFetch summaries unless stated; page numbers are not checked. Figures reused from 093r are cited to it and not re-fetched. Items marked **recheck** were carried from earlier reading in this session and not re-verified at the end.

### 1.1 Net saving from current income (S, labour-funded part)

| Item | Detail |
|---|---|
| Quantity | Household saving out of current income |
| Aggregate | ONS saving ratio 9.5% of gross disposable income in 2024, 9.6% in 2025 (via 093r, rows 1 and 4). Gross of consumption of fixed capital, **includes pension accumulations (D8) and imputed rent** |
| Population, years | UK household sector (including non-profit bodies), annual and quarterly, 1990s to 2025 |
| Definition issue | The ONS cash-basis measure differs sharply from the national-accounts basis: 2017 was −0.8% on a cash basis against 4.1% on the accounts basis (**recheck**, ONS household saving article read earlier). The saving ratio therefore mixes labour-funded saving, retained property income and pension accrual |
| Distribution | Bank of England/NMG survey gives household saving and buffer distributions by income and age (survey, self-reported; the 2017 to 2019 bulletins appeared in search, **not fetched**). Bozio, Emmerson, O'Dea and Tetlow (2013) find saving rises with permanent income (abstract only; **no numbers read**; the PDFs at IFS and HAL were not retrievable, see friction log) |
| Share of wealth change from saving | Resolution Foundation: "active" accumulation about 40% (2018-20 to 2020-22) and 47% (from 2010-12) of the rise in mean family wealth per adult. This is a **residual** (saving, debt change, transfers). Bangham and Leslie (I-W3c): net saving 7 to 24% of the change in family financial wealth, not by band |
| Status | **L** and **R** (aggregate, income-based); **B** for the active share of wealth change; **G** for saving as a share of wealth by band |
| Foreign | Fagereng and others (I-W3a/b, Norway): net active saving about 6 to 8% of disposable income, roughly flat above the 20th percentile. Foreign; not substituted |

### 1.2 Retained property income (interest, dividends, rent not consumed)

| Item | Detail |
|---|---|
| Quantity | Household property income received (D4: interest, distributed income of corporations, rent), and the part retained |
| UK data | ONS quarterly sector accounts S.14 carry D41 (interest), D42 (dividends) and D44 (investment income attributable to policyholders and pension funds) as time series (series pages surfaced in search; **values not read**). Mortgage and consumer interest paid is on the payments side |
| Distribution | HMRC self-assessment data show dividend and interest income concentrated among high-income filers (HMRC statistics surfaced; **numbers not read**). No source found that gives retained property income by **wealth** band |
| Definition issue | In the accounts, property income is income, so it is **inside saving** (section 1.1). The RF "passive" definition uses returns on opening assets, which includes income yield (Annex 2 matches interest rates and equity returns to asset classes); whether yield is wholly within passive for equities is not stated, only that returns are applied by class. Retained income is therefore on the passive side of the RF split and on the saving side of the ONS accounts. These cannot be added |
| Status | **L** (aggregate series exists, not read); **G** for retained share by band. Retained share (income not consumed) is not separately observed anywhere found |

### 1.3 Capital gains (CG, holding gains)

| Item | Detail |
|---|---|
| Aggregate | ONS national balance sheet: between 2023 and 2024 land revaluation rose £177.0bn and dwellings (in produced assets) £55.0bn (**recheck**); 2023 household net worth fell 2.4% on land (093r row 3). Revaluations are shown in the sector accounts' other changes in volume and revaluation account, not split from other volume changes in the bulletin text |
| Distribution | Resolution Foundation passive gain (asset-price) by wealth quintile: median two-year passive gain 8% in the middle quintile, zero in the bottom (2018-20 to 2020-22; 093r row 7). Not by decile. Method (Annex 2): opening holdings by class matched to ONS regional HPI (owner-occupied main homes), UK HPI (other property), interest rates and equity returns by class, DC pensions on a 70:30 equity-bond mix rolling down to 70% bonds and cash from ten years before retirement age; DB pensions and pensions in payment **not modelled**; all assets in a class assumed to change at the same rate |
| Concentration of realised gains | HMRC capital gains tax statistics: realised gains are highly concentrated (the figure read was 92% to the top 1% by remuneration, **recheck** the ranking basis). Realised gains are a fraction of accrued ones and have no relation to a holding-period model |
| Saving by holding | Advani, Bangham and Leslie (2021, S5) and Summers (2023), held in `literature/`: the share of top-tail wealth that comes from held asset appreciation is large at the very top, but their samples are tax records of top income or foreign wealth, not a UK wealth-band decomposition (read earlier in this session; **recheck** before use) |
| Status | **L** (aggregate revaluation by asset class); **T** (RF passive by quintile, whole-distribution); **G** for gains by decile or by band as a share of opening wealth |

### 1.4 Transfers given and received (TR)

| Item | Detail |
|---|---|
| UK data | IFS (Boileau and Sturrock 2023, WAS): transfers received over eight years are worth 0.5% of income in the bottom income fifth and 2.6% in the top fifth; more than half the value of gifts given comes from the wealthiest (93r 2.4, snippet only). Nolan, Palomino, Van Kerm and Morelli (2020, WAS): top wealth quarter received two thirds of transferred wealth, bottom quarter 15%. Resolution Foundation, Inheritance reports (2017, Audit 2024): inheritances and gifts are large and rising relative to income, and concentrated in older and wealthier families (summaries only; **numbers not read in this pass**). HMRC inheritance tax statistics give estates and tax paid for the taxed minority |
| Identification | Transfers **received** have a level by income and by wealth quartile. Transfers **given** as a share of the giver's wealth by band: **no UK figure found**. Lifetime gifts versus bequests, and gifts made within seven years of death, are separate lines in HMRC data |
| Definition issue | RF "active" contains transfers. In WAS, gifts are recorded only above a threshold and bequests are recorded when received, so "net capital transfers" at the household-sector level (D9 in the accounts) is a small residual of large gross flows |
| Status | **L** and **T** for receipts by quartile; **B** for the top group's share of givers; **G** for the rate that matters to a depletion-by-band model (given as a share of giver wealth) |

### 1.5 Liabilities and debt service

| Item | Detail |
|---|---|
| UK data | ONS sector accounts: household interest paid (D41 paid), financial liabilities stock; ONS and BoE household debt-to-income and debt service ratios (aggregate). WAS gives debt by wealth decile in the datasets, but the bulletin text read gives no decile debt shares (**not read**). OBR's household balance sheet pages describe mortgage debt mechanics (capital repayment versus interest) at the aggregate level. The RF family debt repayment gradient (pandemic period) is by family income and age |
| Definition issue | Capital repayment of a mortgage is **saving** in the accounts (it reduces liabilities) and **active** in the RF split. Interest is an expense inside disposable income. Gross and net debt service differ |
| Status | **L** (aggregate debt, interest); **G** for capital repayment against interest by wealth band (the BoE debt service series by band surfaced in search, **not fetched**; the NMG bulletins are the likeliest route) |

### 1.6 Pension contributions and accrual

| Item | Detail |
|---|---|
| UK data | ONS Table 29 and D8 (adjustment for the change in pension entitlements) give aggregate contributions and accruals in the sector accounts; ONS wealth bulletins give pension wealth by decile (top tenth hold 64% of private pension wealth, **recheck**). WAS DB valuation moved to a SCAPE-based method from Round 8, creating a **series break** (093r bridge). IFS valuation work shows mean pension wealth depends heavily on the discount basis (the figures read were £450k against £230k, **recheck** which two methods) |
| Active saving share | OBR decomposition: about 7% of pension contributions were additional saving rather than substitution in 2009 (**recheck** exact basis). Resolution Foundation auto-enrolment work: about 66p of each £1 of employee contribution offset elsewhere (**recheck**) |
| Definition issue | The ONS saving ratio includes pension accumulations; WAS pension wealth is a stock valued by the survey method, and the RF passive/active leaves DB pensions out of passive. A DB accrual is a change in the PV of entitlement, which mixes contribution, accrued service and discount-rate revaluation |
| Status | **L** (aggregate contributions, accrual); **T** (pension wealth by decile at WAS rounds, with the series break); **B** (offset share); **G** for gross new saving, net of offset, by band |

### 1.7 Drawdown

| Item | Detail |
|---|---|
| UK data | Crawford (2018), IFS BN236, ELSA: net financial wealth of the 50 plus fell on average 1.8% a year (95% CI −3.7 to +0.1); wealthier half −2.4% (CI −4.1 to −0.8), poorer half −0.7% (CI −2.9 to +1.6); cumulative 31% over ages 70 to 90 (093r row 6). Financial wealth only. Housing wealth is rarely drawn on (IFS, same note family). IFS "Savings after retirement" (2022) and "Managing retirement incomes" (2022) surfaced; **not read** |
| Definition issue | These are total changes in net financial wealth **including** returns, for people with positive net financial wealth at both ends, and they exclude housing, other property and pensions. They cannot be read as c without a return assumption (093r 3.1) |
| Status | **R** (total change, age group, financial wealth); **B** for the kernel's c on older financial holdings; **G** for drawdown of pension and property wealth, and for any band at working age |

## 2. Bridge: national accounts against survey definitions

| Concept | National accounts (ONS sector accounts, S.14 plus S.15) | Survey (WAS, ELSA) | What breaks a direct bridge |
|---|---|---|---|
| **Saving** | Disposable income − consumption + **change in pension entitlements (D8)**; gross of consumption of fixed capital; includes retained property income and imputed rent; ratio about 9.5% (2024) | No saving variable in WAS; saving is inferred as the change in wealth net of estimated revaluation (RF "active"), or taken from other surveys (NMG, LCF-based) | Inclusion of pension accruals and imputed rent; gross against net of depreciation; **cash basis against accounts basis** (2017: −0.8% against 4.1%, recheck); active residual also holds transfers and debt repayment |
| **Income** | Gross disposable household income (nearly £1.8tn, 2024), including imputed rent, employers' pension contributions, FISIM adjustments and non-profit bodies | Household survey income (FRS/WAS), gross or net of tax, excluding imputed rent unless stated, no employer pension contributions | Imputed rent and FISIM only in the accounts; non-profit institutions serving households sit in S.14 plus S.15 in the accounts; survey income under-captures property income at the top |
| **Net wealth** | National balance sheet: household and non-profit sector net worth about £10.7tn to £10.8tn (2024 to 2025); **market values**; covers communal establishments and people in institutions; state pension treatment differs from WAS (earlier reading: NA includes it, WAS does not; **recheck**, not confirmed in a page read this pass) | WAS: private households only, communal establishments excluded; **self-reported** house values; DB pension valued by the survey method (SCAPE from Round 8, a break); top-tail under-coverage (S5) | Coverage, valuation basis, treatment of DB and top tail; NA net worth vintages revised (£10.7tn to £11.1tn for 2024) |
| **Consumption** | Household final consumption expenditure including imputed rent for owner-occupiers and FISIM; resident households plus non-profit | LCF/WAS-matched spending: total consumption excluding rent and mortgage interest (93r row 5) | Imputed rent; FISIM; mortgage interest and rent excluded in the survey measure; durables treated as consumption in both |

Note: the state pension line and the WAS SCAPE change are from earlier reading and are marked recheck.

## 3. Per-flow table for 096r

"Data or J" is judgement (J) or data (D). A range is shown only where the evidence supports one; none is a band rate.

| Flow | Best UK evidence | What it identifies | Range if supportable | Data or J | Gap |
|---|---|---|---|---|---|
| Net saving from current income | ONS saving ratio and sector accounts; RF active share; NMG | Aggregate level and rate on income (gross, pension and imputed rent inside). Active share of wealth change (mixed) | Aggregate ratio about 9.5% (2024) of GDHI, D; active share 40 to 47% of mean wealth gain, D, mixed | D (aggregate), none by band | Saving by wealth band; the labour-funded part alone |
| Retained property income | ONS S.14 D4 series; HMRC SA data | Level of property income received; not the retained share | No range | D for level (not read), none for retained | Retained income by band; WAS income detail by band |
| Capital gains | National balance sheet revaluations; RF passive by quintile; HMRC CGT | Aggregate revaluation by asset class; passive gain by quintile (2 yrs); realised gains concentration | Median passive 8% over two years in the middle quintile, zero in the bottom (2018-20 to 2020-22) | D, one period, whole distribution | Gains by decile as a share of opening wealth; accrual against realisation |
| Transfers received | IFS, Nolan et al., RF Inheritance, HMRC IHT | Level by income and wealth quartile | Receipts 0.5% to 2.6% of income by income fifth (8 yrs, IFS) | D | Transfers given as a share of giver's wealth, by band |
| Transfers given | HMRC IHT, IFS (givers are the wealthiest) | Direction and concentration only | No range | none | The rate (96r would need it) |
| Liabilities and debt service | ONS and BoE aggregate debt, interest; OBR mortgage mechanics | Aggregate stock, interest, DSR | No range | D aggregate | Capital repayment against interest by band |
| Pension contributions and accrual | ONS Table 29/D8; ONS pension wealth by decile; OBR offset; RF auto-enrolment | Aggregate contributions and accrual; stock by decile; offset share | Offset 7% additional (2009, OBR) to 34% (RF, 100−66p), basis differs, recheck | D with definitions mixed | Net new pension saving by band; DB accrual net of revaluation |
| Drawdown | IFS BN236 (ELSA) | Total change in net financial wealth, 50 plus | 0.7 to 2.4% a year decline (poorer half to wealthier half), total change including returns | D for the total change; any kernel equivalent needs a return (J) | Housing, pensions, working-age drawdown; band |

## 4. Top tail: income-funded saving against returns (brief item 6)

**No UK source gives the share of top-decile wealth change that comes from income-funded saving against returns.** The nearest bounds:
- **Whole distribution, UK:** RF passive 53 to 60%, active 40 to 47% of the rise in mean family wealth per adult (WAS, families, 2006-08 to 2020-22). Not top decile; "active" includes debt repayment and transfers.
- **Financial wealth, UK:** Bangham and Leslie, net saving 7 to 24% of the change in family financial wealth, rest asset prices and yields (I-W3c). Not by band.
- **Top group, UK matched data:** income less spending about 1.3% of wealth in the top fifth on all three measures (093r 3.2, indicative, group averages).
- **Top 1%, Norway:** gross saving rate about 35% including held gains (I-W3b). Foreign and not comparable.
- **Possible UK identification:** the ONS and WAS microdata (top decile by wealth, two or three waves) with the RF passive method, or HMRC tax records linked to wealth. A Bach, Calvet and Sodini style Swedish decomposition was found but the saving against return split was not confirmed from the part read (**not used**).

The nearest **bound** is that active accumulation (which contains income-funded saving) accounts for at most 40 to 47% of wealth gains for the average family. It is an upper bound on saving for the mean only, and says nothing about the top decile.

## 5. Data requests

| # | Request | Purpose | Access route |
|---|---|---|---|
| 1 | WAS decile or band table of net wealth by component (property, financial, pension DB, DC, debt) for Rounds 7 and 8 | Composition by band; debt share; pension break | ONS adhoc request (the ONS "decile composition" release is an xlsx link not reachable here); or UK Data Service special licence microdata |
| 2 | WAS longitudinal panel microdata with RF-style passive/active by decile | Active and passive share for the top decile (item 6) | UK Data Service under licence or ONS Secure Research Service; the author or a collaborator with access; RF authors may share the code |
| 3 | ONS quarterly sector accounts D41, D42, D44, D45 received and paid for S.14 | Retained property income level | ONS time series download (open licence); the shell cannot reach the site, so the author or a later session with fetch access |
| 4 | BoE NMG survey household debt service and saving by income and age | Debt service split and saving distribution | BoE publication (public bulletins); tables need manual download |
| 5 | Bozio, Emmerson, O'Dea, Tetlow (2013) IFS WP 13/30 full text | UK saving rate by permanent income | Author attaches the PDF, or IFS; not retrievable here |
| 6 | HMRC IHT, CGT and SA tables | Estates, realised gains and property income concentration | HMRC statistics (open licence) manual download |
| 7 | ELSA wave data, housing and pension wealth drawdown | Drawdown beyond financial wealth | UK Data Service (registration) |
| 8 | ONS matched LCF–WAS (experimental) microdata | Income, spending and wealth together by band | ONS request or Secure Research Service |

## 6. Cautions for 096r
- Keep S, retained income, CG, TR and dissaving apart. Where a source figure mixes them, the entry says which. The RF active share mixes saving, debt change and transfers; the ONS saving ratio mixes labour-funded saving, retained property income and pension accrual.
- The legacy 3.5% remains a labelled legacy comparator (J). No evidence here replaces it, and no band-level rate is offered.
- The ONS saving ratio is not converted into a wealth-depletion rate in this note.
- Revisions: net worth and saving figures differ by vintage.

## 7. Proposed register rows (not entered; 080r form)

| Proposed row | Low / central / high | D or J | Note |
|---|---|---|---|
| Active share of mean family wealth gain, GB, WAS | 40% / 47% / 47% (2018-20 to 2020-22 and 2010-12 onward) | D | Mixes saving, debt change and transfers; not top decile |
| Median passive gain over two years, middle wealth quintile, GB | 8% (single value) | D | Passive from average class returns; zero in the bottom quintile |
| Net financial wealth change, 50 plus, ELSA | −0.7 / −1.8 / −2.4% a year | D | Total change, financial wealth only |
| Pension contribution additionality | 7% (OBR 2009) to 34% (RF) | D with different bases (recheck) | Offset share, not a flow rate |
| Everything else | no row | – | No band rate, no top-decile saving share, no transfers-given rate |

## 8. Open questions for the author
1. **Top-decile saving against returns has no UK evidence in reach.** Proposed resolution: record as a gap; the author decides whether to request WAS panel access (data request 2) or accept the 40 to 47% mean-family bound for 096r.
2. **Bozio and others (2013) could not be fetched.** Proposed resolution: the author attaches the PDF; a follow-up reads it for the saving-by-permanent-income numbers.
3. **Items marked "recheck"** were carried from earlier reading in the session and not re-verified. Proposed resolution: a short follow-up pass against the sources before any row is entered.

## Sources
- ONS, Quarterly sector accounts, UK: [October to December 2025](https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/bulletins/quarterlysectoraccounts/octobertodecember2025); [October to December 2024](https://ons.gov.uk/economy/nationalaccounts/uksectoraccounts/bulletins/quarterlysectoraccounts/octobertodecember2024)
- ONS, [National balance sheet 2025](https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/bulletins/nationalbalancesheet/2025/pdf)
- ONS, [Households' finances and saving, UK: 2020 to 2024](https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/articles/householdsfinancesandsavinguk/2020to2024)
- ONS, [Understanding real household disposable income per head](https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/articles/understandingrealhouseholddisposableincomeperhead/2025-11-07)
- ONS, [Household income, spending and wealth in Great Britain](https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth/articles/householdincomespendingandwealthgreatbritain/latest)
- Broome and Kanabar (2025), Resolution Foundation, [Before the fall](https://www.resolutionfoundation.org/app/uploads/2025/10/Before-the-fall.pdf) (held copy, Annex 2 read)
- Crawford (2018), IFS BN236, [The use of financial wealth in retirement](https://www.ifs.org.uk/sites/default/files/output_url_files/BN236.pdf)
- IFS, [Savings after retirement (WP 2022/53)](https://ifs.org.uk/sites/default/files/2022-12/WP202253-Savings-after-retirement.pdf) (surfaced, not read)
- Bozio, Emmerson, O'Dea, Tetlow (2013), [IFS WP 13/30](https://ideas.repec.org/p/ifs/ifsewp/13-30.html) (abstract only)
- Boileau and Sturrock (2023), [IFS WP 2023/08](https://ifs.org.uk/sites/default/files/2023-02/WP202308-Who-gives-and-receives-substantial-financial-transfers.pdf)
- Nolan and others (2020), [The wealth of families](https://stonecenter.gc.cuny.edu/files/2020/08/Intergenerational-Wealth-Transfers-Report-Aug-2020.pdf)
- Bank of England, [Financial position of British households, NMG 2018](https://www.bankofengland.co.uk/quarterly-bulletin/2018/2018-q4/the-financial-position-of-british-households-evidence-from-the-2018-nmg-consulting-survey) (surfaced, not read)
- OBR, [Household balance sheet box sets](https://obr.uk/economy_categories/household-balance-sheet/) (surfaced)
- HMRC, [Property rental income statistics 2026](https://www.gov.uk/government/statistics/property-rental-income-statistics/property-rental-income-statistics-2026) (surfaced)
- Repository: `research/notes/093r-consumption-depletion-evidence.md`; `research/hypotheses/household-consumption-and-wealth-replenishment.md`; `model-specs/inputs.md` (I-W3a to I-W3d, I-D14c, I-D1a); held `literature/` PDFs (Before the fall; Advani, Bangham and Leslie 2021; Summers 2023)
