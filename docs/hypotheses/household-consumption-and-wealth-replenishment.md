# Hypothesis: household consumption, income and the replenishment of private wealth

**Status:** Hypothesis for investigation; not an established model finding  
**Origin:** 090c wealth-ratio diagnostic and review of the WDT v3 household wealth kernel  
**Decision status:** No change to model inputs, core mechanics, tax schedules or fund rules is proposed.

## 1. Hypothesis

The current WDT v3 model may materially understate the long-run growth of private wealth relative to GDP because its household wealth dynamics represent consumption primarily as a fixed annual proportional depletion of existing asset holdings, without a corresponding, empirically calibrated representation of household disposable income, saving and wealth replenishment.

If this representation is materially incomplete, the model may overstate the long-run erosion of the WDT tax base and understate the sustainable revenue capacity of WDT. The size and even the direction of the correction are unknown until alternative representations are calibrated and tested against household data.

This is a hypothesis about model specification. It is not a claim that consumption is unimportant, that household spending automatically becomes private wealth, or that a more complete model must improve WDT's fiscal results.

## 2. Evidence prompting the hypothesis

The 090c wealth-ratio diagnostic tested the sensitivity of aggregate wealth relative to GDP to the annual consumption parameter and to WDT taxation.

In its constant-return illustration (4.74% real arithmetic return), the reported year-100 aggregate wealth/GDP index at the current 3.5% consumption setting was approximately:

- 0.47 with WDT switched on;
- 0.62 with WDT switched off.

The same diagnostic reported approximately 1.16 at 2.5% consumption and 2.77 at 1.5% consumption, with WDT on. The reported break-even consumption rate for keeping aggregate wealth/GDP broadly stable under the tested constant-path assumptions was approximately 2.65%.

These are model outputs under specified assumptions, not estimates of actual future UK wealth. A constant 4.74% arithmetic-return path is not equivalent to a stochastic path compounding at the 4.42% geometric-return estimate. The results should not be interpreted as a forecast.

The diagnostic nevertheless establishes a useful sensitivity result: the 3.5% setting has a very large effect on the model's long-run wealth/GDP trajectory. Switching off WDT reduces the decline but does not remove it at the current consumption setting. This points to consumption treatment as a major driver within the model, with WDT taxation adding a further drag.

## 3. The modelling issue

The WDT kernel's yearly growth-and-consumption operation applies asset growth and then reduces the household's asset units by a consumption share. In simplified form, before tax:

```
W[t+1] = W[t] * (1 + r[t]) * (1 - c)
```

Here, c is applied to the value of asset holdings after growth. It therefore behaves as a proportional drawdown of existing wealth.

That is one possible household behaviour: a household can fund spending by selling assets or drawing down savings. But it is not a complete representation of household consumption in general.

A more complete household budget relationship distinguishes income, consumption and saving:

```
Disposable income = consumption + saving
Change in assets = saving + capital gains/losses + transfers and other changes
```

A household that spends part of its current disposable income does not necessarily reduce its pre-existing asset stock by the same amount. If income exceeds consumption, the residual may add to wealth. If consumption exceeds income, the household may draw down assets or borrow. Capital gains, losses, gifts, inheritances and other balance-sheet changes also affect wealth.

At the whole-economy level, expenditure is income to other economic actors, but that accounting identity does not mean all expenditure is converted into household wealth. It may pay wages, taxes, profits, imports, depreciation, intermediate inputs or consumption of current output. The relevant question for WDT is how these flows affect the distribution and aggregate stock of household-owned assets after sectoral transactions and revaluations.

The current 3.5% parameter is recorded as a retained v2 setting, not as a measured UK-wide rate of household wealth depletion. Treating it as a universal annual drawdown rate therefore requires empirical justification that has not yet been established.

## 4. What the hypothesis does and does not claim

### It claims

1. The current consumption parameter is highly consequential for long-run WDT outcomes.
2. A fixed proportional drawdown of asset holdings is not interchangeable with a model in which households consume from disposable income and save the residual.
3. Household income, saving and asset drawdown should be represented distinctly if the model is intended to make long-run claims about household wealth.
4. The effects are likely to differ across households by wealth, income, age, liquidity, asset composition and lifecycle position.
5. WDT's long-run tax base and fiscal closure results should be re-evaluated under empirically grounded alternatives before conclusions are drawn from the current 3.5% setting.

### It does not claim

1. That household consumption is not a genuine use of economic resources.
2. That aggregate expenditure automatically replenishes the wealth of the households making the expenditure.
3. That the 3.5% setting is necessarily too high or that 2.65% is the correct replacement.
4. That introducing wages and saving will necessarily increase the WDT tax base or revenue.
5. That the current WDT fiscal closure failure disappears under a more complete household model.
6. That aggregate wealth/GDP alone captures distributional effects or the number of taxpayers.

## 5. Competing explanations

The observed decline in wealth/GDP and fiscal relief may be explained by several interacting mechanisms:

- **Consumption drawdown:** the current proportional deduction removes asset units each year.
- **WDT tax drag:** tax settlement transfers assets or value away from private households and can reduce subsequent compounding.
- **Threshold indexation:** a GDP-per-head-indexed exemption can change the taxable population and taxable increments over time.
- **Returns and compounding:** arithmetic and geometric returns differ; volatility and sequence effects can materially change long-run outcomes.
- **Distribution and lifecycle:** households with different income, wealth, ages and saving behaviour do not follow one representative path.
- **Transfers and ownership changes:** inheritance, gifts, household formation and dissolution redistribute wealth without necessarily changing aggregate private wealth by the same amount.
- **Macroeconomic consistency:** wages, profits, investment, government, foreign balances and asset valuations interact. A household-only income addition could double-count income or asset formation if not reconciled with the rest of the model.

The hypothesis is strengthened only if a better-supported household-flow representation materially changes the results and the change can be attributed to missing mechanisms rather than unrelated calibration or accounting inconsistencies.

## 6. Proposed empirical and modelling tests

No core changes should be made as part of this hypothesis record. A separate diagnostic should compare alternative representations using common assumptions wherever possible.

### Test A: Audit the existing parameter

Establish exactly what the 3.5% parameter is intended to represent:

- annual consumption expenditure as a share of wealth;
- net asset liquidation to fund consumption;
- a proxy for net dissaving;
- or a deliberately simplified depletion hazard.

Document its original source, rationale, population coverage, and whether it is intended to apply uniformly to every household and every asset class.

If no empirical source exists, retain its classification as a judgement assumption.

### Test B: Compare three household-flow specifications

**A. Current proportional drawdown**

Retain the existing treatment as the baseline. Consumption reduces asset units by a fixed proportion.

**B. Income-funded consumption and saving**

Give households a disposable-income flow. Consumption is funded from that flow first; income left after consumption and taxes is saved and added to household assets. Where consumption exceeds available income, the model must explicitly represent asset drawdown or borrowing. Avoid counting investment returns, income and asset appreciation twice.

**C. Heterogeneous household behaviour**

Represent household groups with different combinations of income, consumption propensity, saving, asset drawdown and lifecycle characteristics. At minimum, distinguish groups by wealth and income; where data allow, also distinguish age, employment/retirement status, liquidity and asset composition.

The specifications should be compared on an accounting-consistent basis. If the model does not include the other sectors needed to close the income and saving flows, clearly label the exercise as a partial-equilibrium household model rather than a complete macroeconomic model.

### Test C: Calibrate against historical UK evidence

Use available UK household data to estimate or bound:

- disposable income and consumption by household group;
- saving rates and dissaving;
- wealth levels and changes;
- asset composition and liquidity;
- age/lifecycle patterns;
- capital gains and losses separately from saving;
- inheritance, gifts and other transfers where measurable.

Potential sources include ONS household income, consumption and wealth statistics; the Wealth and Assets Survey; national accounts and sectoral balance sheets; and relevant academic work. Reconcile definitions, population coverage, survey limitations and national-account aggregates rather than combining incompatible series without adjustment.

Do not calibrate the consumption parameter to produce a desired WDT revenue or fiscal closure result.

### Test D: Separate wealth accumulation from revaluation

For each specification, report the change in household wealth attributable to:

1. saving from disposable income;
2. asset purchases and sales;
3. capital gains and losses;
4. WDT and other taxes;
5. transfers, gifts and inheritances;
6. consumption-funded asset drawdown;
7. other changes and reconciliation residuals.

This decomposition is essential. A rise in asset values is not household saving, and expenditure is not necessarily a reduction in existing wealth.

### Test E: Re-run WDT outcomes

For each specification, report at least:

- aggregate real private wealth;
- aggregate wealth/GDP;
- wealth above the WDT threshold;
- number and share of taxpayers;
- positive taxable increments;
- WDT receipts (M1a);
- other relief components (M1b and M1c);
- total fiscal relief and the gap against retired receipts (M1d);
- first year of fiscal shortfall;
- taxpayer burden and non-payer outcomes;
- distributions and relevant percentiles, not only aggregate means.

Use common return paths, seeds, tax schedules and starting distributions so differences can be attributed to the household-flow specification.

Include both deterministic illustrations and stochastic paths. Report arithmetic and geometric return conventions explicitly. Do not treat the constant-return path as a substitute for stochastic results.

### Test F: Sensitivity and falsification

Vary empirically uncertain inputs over defensible ranges. Include low- and high-saving groups and alternative lifecycle assumptions where evidence supports them.

The hypothesis is weakened if:
- income-funded saving makes little difference to wealth/GDP or WDT outcomes;
- empirically plausible household-flow parameters reproduce the current drawdown trajectory;
- the apparent effect disappears when accounting inconsistencies are corrected;
- or alternative specifications make fiscal sustainability worse.

It is supported if:
- the current fixed drawdown is inconsistent with observed household wealth and saving dynamics;
- a calibrated flow-based model better reproduces historical wealth accumulation and distribution;
- and the resulting WDT outcomes materially differ from the current baseline for identifiable reasons.

A mixed result is entirely possible.

## 7. Reporting requirements

The diagnostic report should begin with a short answer to four questions:

1. Is the current 3.5% setting an empirically defensible estimate of annual net wealth depletion, or merely a judgement proxy?
2. Which household-flow specification best fits the available UK evidence?
3. How much of the difference in long-run wealth/GDP and WDT receipts is attributable to income-funded saving, asset drawdown and heterogeneity?
4. Does the revised representation materially alter the fiscal closure conclusion?

The report must distinguish measured data, calibrated parameters, judgement assumptions and illustrative scenarios. It must not present an improved fiscal result as evidence that a specification is more realistic.

## 8. Implications for WDT

If the hypothesis is supported, the current model's long-run revenue and fiscal sustainability conclusions will need to be qualified and potentially re-estimated. The appropriate response would be to improve the household wealth dynamics and then rerun the existing tax and fund tests, not to select a consumption rate that makes WDT appear feasible.

If the hypothesis is not supported, the current consumption treatment may remain a useful reduced-form approximation, but its interpretation and empirical basis should be made explicit.

Either way, this work should precede changes to the tax schedule, retirement rule, exemption indexation or fund policy. Those are policy decisions that should be assessed against a credible economic model, not used to compensate for uncertainty in the model's household accounting.

## 9. Current conclusion

090c provides strong evidence that WDT results are highly sensitive to the consumption assumption. It does not establish that the assumption is wrong.

The underlying kernel confirms that consumption is currently implemented as a proportional reduction in asset units. This is a model of wealth-funded consumption, not a complete model of household consumption and saving.

The central unresolved question is therefore:

**Does the current WDT model confuse consumption expenditure with net depletion of existing household wealth, and if so, how much does that distort the projected wealth base and fiscal capacity of WDT?**

That is the hypothesis to test.
