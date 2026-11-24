# 096r: the simplest viable household cohort model, on paper (test D)

Written 2026-11-21. Brief `docs/briefs/096r-cohort-cell-design.md`; builds on `research/notes/094r-kernel-map-and-household-accounts.md` (identity, variable dictionary, line numbers at `origin/main` 7e3379f) and `research/notes/095r-uk-household-flow-evidence-map.md` (what is identified). Design only: no code, register, manifest, schedule or fund-rule edit, no run, no value chosen for its effect on WDT revenue, and no scalar depletion rate proposed. 3.5% appears only as the labelled legacy comparator.

## Answer in brief
- **Cell structure.** Cells are **wealth band × life stage**, using the bands the WDT schedule already uses (D4-5, D6-7, D8-9, D10, below-threshold lines as one remainder) and two stages (working, retired). Four test cells illustrate the same identity (section 2): a working saver (D6-7), a low or zero saving working cell (D4-5), a retired cell (D8-9) and a high-wealth cell (D10). They are illustrations; any band-by-stage combination is a cell of the same form.
- **One identity in every cell:** `dNW = S + CG + TR + O − T_WDT` with `S = Y_L + Y_P − I_D − T_C − C` (094r B1). Cash yield sits in `S` once and holding gains in `CG` once. The consumption behaviour is **not** a share of wealth: saving is specified on the income side, where the data speak (095r), and is **unset** wherever 095r found no range.
- **What is data.** Opening balance-sheet shares by band (pack, WAS 2020-22), mean income by wealth band (register, but a judgement row), the return paths and the cash/gain split (the JST file holds the split; the pack builder drops it), ordinary taxes by income decile (not wealth band). Almost every flow parameter by cell is **unset**; the sections say which and why.
- **Public side (item 4).** One representation: the WDT payment is a household outflow and a fund inflow in one pound amount, and household plus fund net worth is conserved by the payment. The kernel's state-stake units are kept only as settlement bookkeeping for in-kind routes and reconciled to the fund. This is a design choice, listed as open question 1.
- **Code impact.** A single household-step function would be introduced first. Five places carry the `(1+g)(1−c)` form (section 4); about nine test files, two pinned digests and the line budget would move.
- **Plans, not runs.** Sections 5 and 6 give the validation and comparison plans. A model that matches aggregate wealth and misses the distribution fails.

## 0. Boundary and conventions
- **Partial equilibrium.** GDP, labour compensation by band, asset returns, prices and interest rates are specified outside the model. Firms, government, banks and the rest of the world are **not** closed: consumption is no firm's revenue and moves no return; ordinary taxes and expenditure are external; cross-border transfers do not cancel; household wealth does not feed back on returns or income (094r B5, hypothesis section 13). Nothing here claims stock-flow closure with those sectors.
- **Real terms**, as the kernel. Nominal positions (cash, bonds, debt) get a real revaluation in `CG` using the pack's CPI path.
- **Status labels** (brief): **data**, **calibrated** (a later brief must fit it to data), **externally specified**, **judgement**, **illustrative** (a value used only to show mechanics, never a proposal), plus **unset** (no supportable range; nothing is entered). 095r's ranges are used only where it gave one and the guru's note allows: the items it marks recheck, its section 7 rows and the pension additionality range are not used.

## 1. Segmentation: why each split earns its place

| Split | Why | What 095r identifies | Data cost | Decision |
|---|---|---|---|---|
| **Wealth band** (D4-5, D6-7, D8-9, D10; below-threshold remainder) | The WDT schedule and the register rows are by these bands; assessment, payer status and revenue are all computed on them. Composition (property, financial, pension) differs by band in the pack | Nothing identifies a flow rate by band; composition by band is data. So the split organises opening state, not behaviour | Held: shares by band (`wealth_distribution.csv`), income by band (I-D9a to I-D9d, J), tail (`wealth_tail.csv`). Missing: debt, age, consumption by band | **Keep.** Cheapest split already used by the model |
| **Life stage** (working, retired) | Dissaving and decumulation are the one place a UK source shows total financial wealth falling (ELSA, 50 plus: −0.7 to −2.4% a year, total change incl. returns, financial wealth only); the income side also changes (labour to pension income) | Drawdown is a bound for older financial wealth; no stage-by-band rate; housing and pensions not identified | A joint age-by-wealth-band table is **not in the pack**; WAS age bands exist in the held workbook (Table 2.11) and in WAS microdata. Moderate | **Keep, two stages only.** Finer age cells cost data 095r says nobody holds a rate for |
| **Income** within band | Saving is specified on the income side; low-income and high-income households at the same wealth differ in `Y_L` and `T_C` | Saving rises with permanent income (Bozio and others 2013), abstract only, no numbers read; the active share is a mean-family residual | Mean income by band is held (J); no joint income-wealth distribution in the pack | **Not a separate split.** Carried as a cell-level `Y_L`; a later brief may split if a joint table is obtained (data request 8 in 095r) |
| **Asset composition** (housing, equity, bond, cash, pension, debt) | Needed because cash yield, holding gain and the order of liquidation differ by class | Passive gains by class are matched to indices in the RF method; income/gain split for the UK is in the JST file; liquidity by band only the net-financial share | Shares by band held; debt and the liquid/illiquid split by band not held (only `net_financial_share` as an upper-side proxy) | **Keep as a state vector inside each cell**, not a split of cells |
| **Tenure or mortgage status** | Interest and capital repayment differ; owners with a mortgage differ in flow | Debt service by band: gap (095r 1.5) | Not in the pack | **Left out** until a WAS debt-by-band table exists |
| **Pension type** (DC, DB, in payment) | DC is market-valued, DB is an entitlement valued by a method with a series break | Contributions and accrual by band: gap | Not in the pack | **Left out**: `PA` is one asset at WAS value; accrual unset |
| **Household type, region, ownership of business** | Real heterogeneity | Nothing | High | **Left out** |

The brief allows asset composition and liquidity only where data identify or bound them. Composition by band is data; liquidity is bounded only by `net_financial_share`, so the liquidation order (section 2.3) is a judgement, labelled so.

## 2. The four test cells

### 2.1 Common structure
Each cell is a representative balance sheet `NW = H + E + B + M + PA − D` with weights `w` (adults or households, from WAS by band and stage; a gap for the stage split). The year's step, in order:

1. **Cash income.** `Y_P = Σ y_class · A_class` (dividends, rents, interest), `I_D = i · D`.
2. **Net saving** `S = Y_L + Y_P − I_D − T_C − C`, with `C` specified per cell (2.3). Retained cash yield is inside `S`.
3. **Holding gains** `CG = Σ g_h,class · A_class` plus the real revaluation of nominal positions. The kernel's total return `r = y + g_h` is **split**, not credited whole (094r B4); this removes the double count of case 6c.
4. **Financing** a negative `S` or a payment: cash `M` first, then sale of `B` and `E`, then borrowing within a limit; housing and the pension asset are not liquidated in-year (**judgement**, supported only by ELSA's finding that older owners rarely draw on housing wealth).
5. **Transfers** `TR` between cells (cancel in the sector); **other** `O` is the reconciliation residual.
6. **WDT.** Assessed on the cell's `dNW` before tax, the quantity the kernel already assesses (`delta`), so consumption explicitly lowers the taxable change (plan decision D17 retained). `T_WDT` leaves the household and enters the fund.

Behaviour is **not** a proportional sale of all units. A cell that saves more than it consumes of its income accumulates; one that consumes more than its income draws down by asset order. Whether a cell does either is an input, never a result of a universal rate.

### 2.2 Parameter matrix
Cells: **W** = working saver, D6-7; **L** = working, low or zero saving, D4-5; **R** = retired, D8-9; **H** = D10 (working or retired). "Unset" means no supportable range; the cell cannot be run on that parameter until data or an author decision supplies it, except as a labelled illustration.

| Parameter | W (D6-7, working) | L (D4-5, working) | R (D8-9, retired) | H (D10) |
|---|---|---|---|---|
| Opening wealth, band mean | **data** (pack, WAS 2020-22 band mean) | data | data | data; top-tail under-coverage (S5), `wealth_tail.csv` for the extreme |
| Composition: property, net financial, pension share of band wealth | **data**: 45.6 / 9.3 / 32.5% (D6-7, 2020-22) | data: net financial 6.6%; property and pension rows for D4-5 are blank in the file read, so **unset** until the pack row is checked | **data**: 42.7 / 12.8 / 35.4% | **data**: 38.3 / 19.3 / 36.4% |
| Debt `D` and its interest `I_D` | **unset** (no gross debt in pack; netted inside wealth) | unset | unset | unset |
| Labour/pension income `Y_L` | **externally specified** growth (GDP per head); level from I-D9b £63,000 mean gross, all households in band, **judgement** (±20%) | I-D9a £50,300, judgement | I-D9c £71,500 is an all-households mean, **not a retired-income figure**: retired income **unset** | I-D9d £71,400, the register's weakest; top incomes not captured: **unset** for the tail |
| Cash yield `y` by class | **externally specified** from the returns path (JST split, not yet in the pack) | same | same | same |
| Holding gain `g_h` by class | externally specified path | same | same | same |
| Ordinary taxes net of benefits `T_C` | **data by income decile** (ETB 2023-24, `household_incidence.csv`); mapping to wealth bands is **judgement** | same | same | same |
| Consumption `C` / saving as a share of income | **unset**. Illustrative values appear only in the worked example (2.4). The aggregate ONS saving ratio (9.5% in 2024, gross, pension and imputed rent inside) is a **check on the weighted sum**, not a cell input | **unset**; "low or zero saving" is the cell's defining state, not a number | **unset**; no rate for retired non-financial wealth. ELSA's total change in financial wealth (−0.7 to −2.4% a year, 50 plus) is a **validation moment**, not a parameter | **unset**; no UK top-decile saving share exists (095r section 4). H is run with `S ≥ 0` and `S < 0` as two **illustrative** states, never as a claim about top households |
| Pension contributions `K` and accrual | unset | unset | unset (decumulation unset) | unset |
| Net transfers `TR` | unset; aggregate zero by construction | unset | unset | unset; the heir rule (every 30 years) is the legacy comparator only |
| Other `O` | zero in design; residual in validation | zero | zero | zero |
| `T_WDT` | endogenous | endogenous | endogenous | endogenous |
| Liquidation order | **judgement**: cash, bonds, equities, then borrowing; housing and pension not sold in-year | same | same; the retired cell may differ (annuity, decumulation): **unset** | same |

Where 095r gave a range it is a **moment to compare against**, not a parameter: the RF active share of the rise in mean family wealth per adult (about 40 to 47%, whole distribution, includes debt repayment and transfers), the median two-year passive gain of 8% in the middle quintile, ELSA's drawdown band, receipts of transfers by income fifth (0.5 to 2.6% of income over eight years). None is turned into a cell input.

### 2.3 Why consumption is on the income side
The kernel's `c` is the retained cash yield less net saving as a share of the grown stock (094r B4); it compresses income, consumption and saving into one rate and applies it to every unit, including pensions and housing. The data that exist (the saving ratio, matched LCF-WAS spending, NMG, income-based saving by permanent income) speak in income terms. Specifying `S` or `C` against income per cell is the unit the evidence uses, and it does not turn a saving ratio into a depletion rate. The sum over cells is checked against the aggregate; it is never solved for.

### 2.4 Worked example (illustrative, not data)
Using 094r's B3 household (£ thousand, real; H 600, E 200, M 100, PA 400, D 200, `NW0 = 1,100`) in cell W: `Y_L` 60, `T_C` 12, dividends 6, interest received 2, interest paid 8, fund income 12, gains E 4, H 18, PA fund 20, and `C` **illustratively** 40. `S = 20`, `CG = 42`, `dNW = 62`. The same household with `C` raised to 60 has `S = 0`, `dNW = 42`; with `C = 80`, `S = −20`, financed by cash first and then equities, and `dNW = 22`. These show mechanics only. No cell's consumption is proposed, and the three values are not a range.

## 3. Aggregation and transitions

**Aggregation.** The sector is `Σ_cells w_c · (state_c)`, with weights by band and stage. To the WDT schedule's bands: each cell maps to one band, so band totals are sums over that band's stage cells; payer status uses the cell's wealth against the threshold exactly as `base` does, with the within-cell distribution handled as today (the pack's lines) unless a later brief carries a within-cell distribution. Checks on every run (not calibration): (a) `Σ w S` against the sector saving with the 095r bridge applied (gross, pension and imputed rent inside, cash against accounts basis), up to a stated reconciliation residual; (b) `Σ w NW` against the balance-sheet aggregate (£10.7tn to £11.1tn by vintage); (c) the identity, per cell and in total, to rounding.

**Transitions needed to keep the aggregates and the distribution.**

| Transition | Needed? | Treatment |
|---|---|---|
| Working to retired | **Yes.** Without it the retired cell empties or fills artificially and the age structure drifts | Flow of weight and balance sheet from W/L/H-working to R/H-retired by band at a demographic hazard taken from ONS population projections (**externally specified**); balance sheets carry over unchanged at transition |
| Death and inheritance | **Yes**, minimal | Keep the kernel's 30-year heir rule as the **legacy** mode. In the new mode a bequest is a `TR` from a retired cell to a working cell of the same or adjacent band; the size is **unset** (095r: no transfers-given-as-share-of-wealth figure). Until set, the baseline runs with `TR = 0` and says so |
| Household formation and dissolution | Left out | No UK flow data identified; changes weights, not the identity |
| Band mobility from the flows themselves | **Endogenous** | A household moves band when its wealth crosses a band boundary; this is how the distribution evolves and is the main thing validation tests |
| Migration, divorce, assortative mating, mortality by wealth | Left out | No identified parameter; named as limits |

Aggregates the transitions must preserve: the stage split of weights, wealth by band, and mean age of the retired cell at entry (to keep the ELSA moment meaningful).

## 4. Interface to v3 (gap list only; nothing edited)

**Where it replaces the kernel.** `grow_and_consume(book, g, consumption)` (`kernel.py:324-341`), called in the year loop (`kernel.py:450-475`) before `declare` and the single assessment. The replacement is one **household-step function** returning, per cell and year: balance sheet, `S`, `CG`, `TR`, `T_C`, and the pre-tax `dNW` the assessment reads. The order of steps downstream is unchanged: assessment on total declared wealth, settlement per route, rebase.

**Introduce the household step first?** Yes. Five places repeat the form and must read the same function, or the legacy and new modes diverge silently:
1. `kernel.grow_and_consume` (`kernel.py:324-341`): the growth and sale of units.
2. `revenue.run_lines` payer status: `W1 = W0 (1+g)(1−c)` (`revenue.py:83`), which feeds `pay1` and the rate at the new wealth.
3. `revenue.identity`, the M1a/I3 check: `gacc = (1+g)(1−c) − 1` (`revenue.py:241`); the accrued gain rate would be the account's `dNW` before tax over opening wealth.
4. `burden.free_path`: the no-tax wealth path `(1+g)(1−c)` cumulated (`burden.py:173-176`), which feeds `m3_today` and the incidence of retired taxes.
5. `support.system_run`: `grown·(1−c) − tax`, with the `consumption_tax` comparator taxing `rate·c·grown` (`support.py:120-136`); `wdt_run` and `welfare` pass `c` through. In the new design the consumption comparator needs the cell's `C`, not `c·grown`.
Pass-through callers: `burden.line_flows` (`burden.py:86`), `revenue.run_lines` (`revenue.py:53`), `support.wdt_run` (`support.py:150`), and the runner's `c = theta['I-D14c']/100` (`runner.py:202`).

**Public side.** The household step returns `T_WDT` in pounds; the fund inflow is that same amount (`wdt = tax + refund + death_tax + heir + death_B + death_D`, `revenue.py:207`). The state's units (`s`, `state_true`, `growth_state`), which nothing outside the kernel reads (094r A3), are demoted to **settlement bookkeeping** for the in-kind routes (C, D) and reconciled each year to the fund's holding; a conservation check "household NW + fund NW unchanged by the payment" replaces the unchecked pair. Unresolved: whether to drop the unit book altogether (open question 1).

**Missing pack inputs.** Income by wealth band for D1 to D3 and a labour/capital split; household consumption; gross debt, mortgage, interest and repayment by band; age and stage by band; pension contributions, accrual and state/DB split; the cash-yield and gain split by class (present in `source/jst_r6.json`, dropped by the builder); transfers; saving by band (none exists for the UK). Each is a new pack table or a register row; adding tables changes `pack_sha256`.

**Register and manifest.** New register rows only for parameters that gain a supportable range (none today); the cell definitions, liquidation order and weights are levers or pack data. I-D14c stays as the legacy comparator (`legacy` mode) and is not a model input in the new mode. New outputs: per-cell `S`, `CG`, `TR`, `T_WDT` decomposition and the identity residual; the manifest and `outputs.yml` would need ids for them. Outputs now carrying 3.5% in labels (094r A5) would need relabelling by the author.

**What stays as it is.** Assessment and rate function (`schedule`), settlement routes, the fund and retirement rules (`revenue.py:121-174`), the writer and output layer, the seed streams. The return generator is unchanged except that it must supply the split `y` and `g_h` (or a total plus a yield share).

**Tests and digests that would move.** `test_kernel`, `test_revenue` (payer status, identity), `test_burden` (`free_path`, `m3_today`), `test_support` (`system_run`, `welfare`), `test_groups` (the pinned Samples digest, `PIN`), `test_out` and `test_out_burden` (new outputs and labels), `test_pack` (`GBR_SHA`, and the fixture digest if the fixture gains tables), `test_budget` (the 4,770-line budget and the 3,020 test budget). A **legacy-mode regression** test is needed so the old results reproduce.

## 5. Validation plan (test E, a plan only)

**Overlap and holdout.** The UK wealth panel and the stock history overlap in WAS Rounds 1 to 8 (2006-08 to 2020-22, the span the RF decomposition uses) and the balance-sheet series. Holdout options, in order of strength: (1) **temporal**: fit or set cells on Rounds 1 to 6 and predict the 2018-20 to 2020-22 transition; (2) **cross-band**: leave one band's behaviour unset and test whether the others' flows reproduce it (weak, since behaviour is unset); (3) **cross-source**: ELSA drawdown for the retired cell and the NMG for debt and saving distributions, neither used in setting anything. The top decile cannot be held out: it is the least covered by the survey.

**Moments compared** (all must be matched in the same definition as the data, using the 095r bridge):
- Level: aggregate and band means of wealth; aggregate saving (gross, pension inclusive).
- **Distribution:** band shares, quantiles and the top-tail share; the **band transition matrix** between waves (rank mobility); the share of households with falling wealth over two years.
- **Decomposition:** the model's passive/active split computed with the **RF method** (opening holdings at class returns) against about 53 to 60% passive, 40 to 47% active; compared with the same method on the simulated panel, never with the model's own S and CG, so the definitions match.
- Cell moments: retired net financial wealth change against ELSA's −0.7 to −2.4% a year (financial wealth only, total change); composition shares by band.

**Pass rule.** Matching aggregate wealth and missing the distribution, the transition matrix or the decomposition is a **fail**. Tolerances are the author's to set before any run (open question 3).

**Named threats.** WAS attrition and top-tail under-coverage (S5); the Round 8 DB pension valuation break (SCAPE); survey against accounts coverage (communal establishments, non-profit institutions); self-reported house values against market values; the cash against accounts saving basis (095r bridge, one entry marked recheck); imputed rent and FISIM; net-worth vintage revisions (£10.7tn to £11.1tn for 2024); real against nominal treatment of debt; the reconciliation residual `O`, to be reported, never absorbed into `S`.

## 6. Comparison plan (test F, a plan only)

**Arms.** (i) **Legacy**: the current kernel with I-D14c at 3.5%, labelled legacy comparator, reproduced by the legacy mode. (ii) **New baseline**: the cell model with parameters at what the data support, unset parameters either supplied by an author ruling or run as stated scenarios. (iii) **Defensible low** and (iv) **defensible high**: variants that move flow mechanisms only inside identified ranges or named judgement bounds.

**Held common to all arms.** The starting distribution (pack 2020-22 bands and the tail table), the return paths (same seed stream, 20261118, same 10,000 level-1 paths and 200 level-2 draws), the schedule family and threshold grid in `levers.json`, the retirement order, the horizon windows, and the demographic weights.

**What defines low and high.** Only mechanisms with an identified or bounded range may vary: for instance, the active/passive bound (whole distribution), the ELSA band for the retired financial cell, the transfers-received range by income fifth. Where there is no range (saving by band, transfers given, debt service, pension flows), low and high **do not exist** and the arms say "unset"; the author may authorise judgement scenarios, labelled as such. No scenario is chosen for its effect on revenue.

**Outputs to report.** Wealth by band over time, payer counts, `T_WDT` by band, fund balance, the per-cell identity residual, the per-cell decomposition into `S`, `CG`, `TR`, `T_WDT` and the existing manifest outputs under each arm, with the legacy labels.

**Attribution.** Differences between arms are attributed **only to flow mechanisms**, by switching them one at a time from the legacy form to the cell form: (1) cash and gain split; (2) explicit income-side saving by cell; (3) the liquidation order (no in-year sale of housing or pensions); (4) transfers; (5) the public-side representation. Five switches have 120 orders; report two orders (the natural one and its reverse) and the largest order-dependence, so interaction is visible. Results are described as differences in mechanism, not as favourable or unfavourable to WDT.

## 7. Open questions for the author
1. **Public side.** Is the single fund representation (units kept only as settlement bookkeeping) acceptable, or should the unit book be removed? Proposed resolution: keep the units as bookkeeping with the conservation check in the first code brief, and drop them only if Route C and D settlement can be rewritten in cash.
2. **Low and high scenarios where no range exists.** Saving by band, transfers given, debt service and pension flows have no identified range. Proposed resolution: run those flows as unset (the arm cannot run on them) until the author rules which, if any, may be run as labelled judgement scenarios.
3. **Validation tolerances.** The pass rule needs numbers for the distribution and transition moments. Proposed resolution: the author sets them before any run; the guru records them in the implementation brief.
4. **Retired-cell income and stage weights.** The register's income rows are all-household means and the pack has no stage-by-band table. Proposed resolution: a data request for WAS age-by-wealth-band weights and retired income, as 095r data request 1, before the cell weights are set.
5. **Placing bequests.** In the new mode, bequests are `TR` between cells with no identified size. Proposed resolution: the baseline carries `TR = 0` and the legacy heir rule only in the legacy arm; the author may authorise a judgement scenario.

## Checked
- Line numbers and call sites were read in `origin/main` 7f292f8 (`revenue.py:83, 207, 241`; `burden.py:173`; `support.py:120, 150`; `kernel.py:324`). Pack rows quoted are those printed from `wealth_distribution.csv`; D4-5 property and pension rows were not in the printed lines and are marked unset.
- No code was run and nothing was edited outside Touches. Worked-example arithmetic: `S = 60 − 12 − 40 + 6 + 2 − 8 + 12 = 20`; `CG = 4 + 18 + 20 = 42`; `dNW = 62`; with `C = 60`, `S = 0` and `dNW = 42`; with `C = 80`, `S = −20` and `dNW = 22`.

## Sources
Repository: `research/notes/094r-kernel-map-and-household-accounts.md`; `research/notes/095r-uk-household-flow-evidence-map.md`; `research/notes/093r-consumption-depletion-evidence.md`; `research/hypotheses/household-consumption-and-wealth-replenishment.md` (sections 11 to 14); `docs/model-v3/architecture.md`; `docs/model-v3/inputs.md` (I-D9a to I-D9h, I-D14c, I-D1a); `model_v3/core/kernel.py`, `revenue.py`, `burden.py`, `support.py`; `model_v3/runner/runner.py`; `model_v3/pack/GBR/wealth_distribution.csv`, `household_incidence.csv`, `source/jst_r6.json`; `tests/model_v3/`.
External evidence is cited through 095r and 093r (ONS saving ratio and national balance sheet; Resolution Foundation, Before the fall, 2025; Crawford 2018, IFS BN236; Boileau and Sturrock 2023; Bozio and others 2013, abstract only); none was re-fetched for this note.
