# External observation: judgement-marked model inputs

**Date:** 18 November 2026  
**Scope:** Review of the V3 input register, principally `model-specs/inputs.md`  
**Status:** External analytical observation; not a formal audit or a change to model assumptions

## Executive observation

The current V3 input register identifies **90 judgement-marked rows out of 260 registered inputs**. The register explicitly records these as judgement rows using the `(J)` marker. This is approximately 34.6% of the register.

That is a substantial share, but it should not be read as meaning that 90 independent numbers have simply been guessed. The marked rows cover several different kinds of uncertainty: assumptions, derived allocations, interpolations, fitted estimates, proxy measures, transferred evidence and choices made where the available data do not identify a unique value. Some are downstream of other inputs and some share the same underlying evidence.

The important question is therefore not simply how many judgement rows exist. It is **which judgements materially determine the model's conclusions, how well they are supported, and how their uncertainty and dependencies are represented**.

This is an opportunity to make the model more transparent and more useful. The judgement markers provide a starting point for a structured uncertainty and sensitivity programme.

## 1. What the register currently says

The register's latest summary records the 90 judgement-marked rows as follows:

| Input area | Judgement-marked rows | Broad subject |
|---|---:|---|
| Core B1-B4 inputs (I-D / I-M) | 41 | Core economic, distributional, tax-baseline and model-comparison inputs |
| Wealth inputs (I-W) | 29 | Wealth distribution, asset holdings and wealth dynamics |
| Tax-base inputs (I-T) | 8 | Taxable investment income, gains and related estimates |
| Household inputs (I-H) | 12 | Household distribution, income/wealth relationships and incidence |
| **Total** | **90** | |

The register reports 260 inputs in total: 92 in the core B1-B4 sections and 168 in the added I-W, I-T and I-H sections. The 90 judgement-marked rows are therefore about 34.6% of the current register.

These figures describe the register as it stood on 18 November 2026. They should be recalculated if the register changes. They are not a permanent property of the model.

### An important distinction

The `(J)` marker is a useful disclosure convention, but it does not by itself tell the reader what kind of judgement is involved or how much uncertainty it introduces.

For example:

- A midpoint selected between two evidence-based bounds is not the same thing as an unsupported point estimate.
- An allocation derived from a published aggregate is not the same thing as a directly observed statistic.
- An interpolation between published percentiles is not equivalent to a measurement at the interpolated point.
- A proxy transferred from another country or tax regime may be empirically grounded, but its applicability to the UK remains uncertain.
- A genuine policy or behavioural assumption may be unavoidable, but should be identified as such.

The count is consequently a useful warning light, not a quality score.

## 2. Where the judgement burden matters most

The register points to several areas where uncertainty could have a material effect on the model's outputs.

### 2.1 The upper tail of the wealth distribution

Household wealth surveys are weakest where the model most needs precise information: at the very top of the distribution. Very wealthy households are relatively few, difficult to sample and may hold assets that are difficult to value consistently. Survey estimates can therefore understate or mischaracterise the upper tail.

The model necessarily uses estimates and fitted distributions to extend beyond the directly observed data. This is a material issue for any proposal with a wealth threshold, and particularly for a stock wealth tax: the amount of wealth above a threshold depends directly on the shape and scale of the upper tail.

A single fitted tail should not be treated as established fact. The model should test alternative plausible specifications, such as:

- Pareto and generalised Pareto tails;
- lognormal or other alternative distributional fits;
- fits constrained by observed survey percentiles;
- alternative treatments of very wealthy households and external rich-list evidence.

The objective is not to select whichever distribution produces the most favourable revenue result. It is to establish how much the result changes when reasonable tail assumptions change.

### 2.2 Behavioural responses and avoidance

Behavioural responses are especially difficult to estimate because the evidence comes from different countries, institutional settings and tax designs. A conventional annual tax on accumulated wealth is not equivalent to a tax on annual changes in wealth. Rates, thresholds, valuation rules, liquidity provisions, enforcement, residence rules and the treatment of losses all affect incentives.

A single behavioural-loss percentage is unlikely to capture these differences adequately. Nor should a headline behavioural adjustment be added to component adjustments if the headline already includes those components. That would double-count the response.

A stronger approach would model behavioural responses as functions of relevant characteristics, including:

- the effective marginal tax rate;
- wealth level and asset composition;
- liquidity and the ease of moving or restructuring assets;
- the availability and credibility of valuation and enforcement;
- residence and migration incentives;
- the particular tax design being simulated.

Where the evidence cannot support a detailed response function, the model should retain explicit scenario ranges and make the limits of the evidence clear.

### 2.3 Incidence of existing taxes

The WDT comparison depends not only on who legally pays existing taxes, but on who ultimately bears their economic cost. This is particularly important when estimating the distributional effect of replacing taxes such as corporation tax and business rates.

The UK does not provide a single comprehensive dataset that directly identifies the final incidence of every relevant tax across the full household wealth and income distribution. Some allocations must therefore be inferred from research, transferred from other jurisdictions or approximated using available household data.

These choices can materially change the apparent winners and losers from tax replacement. Incidence assumptions should be varied explicitly, especially where a tax is divided between owners, workers and consumers.

The model should report whether its conclusions about the distribution of gains from reform survive reasonable alternative incidence assumptions.

### 2.4 The joint distribution of income and wealth

Income and wealth are related, but they are not interchangeable. A household's position in the income distribution does not reliably identify its position in the wealth distribution. Retirees, asset-rich low-income households, business owners and high-income renters are obvious examples of why the distinction matters.

Where the available data do not provide the joint distribution required by the model, interpolation or proxy relationships are necessary. These should be treated as estimates with their own uncertainty, not as if they were directly observed household records.

This matters for both tax incidence and the identification of non-payers or net beneficiaries. A model that gets the marginal income and wealth distributions approximately right can still get their joint distribution wrong.

The preferred long-term solution is a better joint income-wealth dataset or a defensible synthetic population calibrated to the available UK evidence. Until then, the model should test alternative plausible relationships between income and wealth.

### 2.5 Unrealised gains and the annual change in the tax base

An accrual-basis wealth tax needs to represent changes in asset values whether or not those changes have been realised through a sale. This creates a data problem: published tax statistics are often organised around realised transactions, while household wealth data provide snapshots of asset values rather than a complete account of accrued gains.

Estimates of unrealised gains therefore require assumptions about asset composition, acquisition values, holding periods and the distribution of gains across households. These estimates can materially affect the modelled tax base.

The model should distinguish, as far as the data permit:

- observed changes in asset values;
- estimated accrued gains on assets without a current market transaction;
- realised gains;
- changes caused by saving, consumption, inheritance or transfers;
- valuation changes that do not represent an economically available cash flow.

This is also an area where liquidity and tax design interact. A tax liability arising from an unrealised gain is not necessarily a liability that can be paid from cash income in the same year.

## 3. The 90 rows are not 90 independent uncertainties

This is the most important modelling implication.

Many of the judgement-marked rows are related to one another. They may be derived from the same source data, depend on a common fitted distribution, or describe different parts of the same underlying economic process.

For example, an individual or household's:

- wealth level;
- asset composition;
- investment return;
- realised and unrealised gains;
- tax liability;
- liquidity position;
- avoidance response;
- likelihood of changing tax residence

are not independent characteristics.

Likewise, errors in the upper-tail wealth distribution can affect several inputs at once. A change in the assumed distribution may alter the number of taxpayers, the wealth held above a threshold, the composition of the tax base and the estimated revenue.

If every judgement-marked row is sampled independently in a Monte Carlo simulation, the model may generate combinations that are internally inconsistent or economically implausible. It may also exaggerate or understate the resulting uncertainty. The direction of the error is not guaranteed.

The model should therefore distinguish between:

1. **Independent or plausibly independent uncertainty:** where separate variation is defensible.
2. **Shared-source uncertainty:** where several inputs inherit error from the same dataset or study.
3. **Derived uncertainty:** where an input is calculated from other uncertain inputs.
4. **Structural uncertainty:** where alternative model forms or economic relationships are plausible.
5. **Behavioural uncertainty:** where responses depend on incentives and institutional conditions.

A dependency map should be built before introducing elaborate correlation machinery. The initial aim is to document which inputs move together and why. Conditional distributions, common factors or copulas may be useful later, but should be introduced only where they improve the representation of the evidence.

## 4. Epistemic and aleatory uncertainty should be separated

Two different forms of uncertainty are relevant:

- **Epistemic uncertainty** is uncertainty caused by limited knowledge or imperfect data. Examples include the true upper-tail wealth distribution, the incidence of existing taxes and the distribution of unrealised gains. Better evidence or research may reduce it.
- **Aleatory uncertainty** is variation inherent in the process being modelled. Future investment returns are an obvious example. Better data may improve the distributional estimate, but cannot eliminate future randomness.

This distinction matters for interpretation. A wide range caused by future market returns is not the same as a wide range caused by not knowing how much wealth the richest households hold. The former is a feature of the world; the latter is a research limitation.

The model should avoid presenting both as one undifferentiated confidence interval.

## 5. Recommended treatment in the V3 model

The 90 judgement-marked rows should not all receive equal research effort. The practical priority is to identify which uncertainties drive the outputs that matter.

A proportionate sequence would be:

### Step 1: Classify the judgement rows by type

Add a structured classification for each `(J)` row:

| Type | Meaning |
|---|---|
| Direct assumption | A value selected because the model requires a parameter and evidence does not identify it |
| Derived allocation | Calculated from other inputs or published aggregates |
| Interpolation / extrapolation | Estimated between or beyond observed data points |
| Fitted estimate | Produced by fitting a statistical distribution or model |
| Proxy / transferred evidence | Based on a related measure, population, country or tax regime |
| Structural choice | One of several plausible ways to represent the underlying process |

A row may need more than one tag. The aim is to describe the method, not force every input into an artificial single category.

### Step 2: Record dependencies

For each material input, record:

- which other inputs it depends on;
- whether it shares a source with other inputs;
- whether its low, central and high values are conditional on other assumptions;
- whether changing it requires other inputs to change as well.

This can begin as a simple dependency table or graph. It does not need to become a complex probabilistic model immediately.

### Step 3: Run the baseline model

The current central estimates and ranges should first be run through the V3 model as documented. This establishes a baseline against which sensitivity can be measured.

The existence of judgement-marked inputs is not a reason to postpone modelling indefinitely. A transparent baseline is more informative than an indefinitely expanding list of unresolved research questions.

### Step 4: Conduct sensitivity analysis

Test how changes in each material input, and in coherent groups of related inputs, affect:

- net government revenue;
- the distribution of tax burdens;
- the number and characteristics of taxpayers;
- the number and characteristics of non-payers;
- the distribution of gains and losses from replacing existing taxes;
- the long-run fiscal position of the Sovereign Wealth Fund.

Where feasible, use global sensitivity analysis rather than relying only on one-at-a-time changes. One-at-a-time tests are useful for explanation but can miss interactions.

### Step 5: Prioritise research by influence

Research effort should be concentrated on inputs that are both uncertain and influential. A weakly evidenced input that barely changes the outputs is a lower priority than a moderately uncertain input that determines whether the proposal raises or loses several percentage points of GDP.

The sensitivity results should therefore guide the next research programme. This avoids spending equal effort on all 90 rows simply because they carry the same marker.

### Step 6: Report uncertainty in the outputs

The eventual model outputs should show ranges and explain their main drivers. If the model reports P10, mean and P90 results, it should also identify which assumptions account for most of the spread.

A P10/P90 range is only as meaningful as the distributions and dependencies used to generate it. The model should not imply a level of statistical precision that the evidence does not support.

## 6. Implications for interpreting WDT and stock-wealth-tax comparisons

These observations are relevant to the WDT proposal itself and to any comparison with a conventional stock wealth tax.

The two systems do not necessarily share the same behavioural responses or revenue sensitivities:

- A stock wealth tax applies to the value of the wealth stock above a threshold.
- The WDT applies to changes in wealth under its accrual-basis design.
- The same asset valuation problem can affect both, but the way it enters the tax base differs.
- A stock tax creates a recurring liability related to the level of wealth, while an accrual tax creates a liability related to changes in wealth.
- Liquidity, loss treatment, migration, avoidance and asset allocation may therefore respond differently.

In particular, evidence from countries that operated conventional net wealth taxes should not automatically be transferred to the WDT as if the incentives were identical. It can inform plausible scenarios, but the transfer itself is a judgement that should be visible.

The same applies in reverse: a behavioural assumption that is reasonable for the WDT should not be applied uncritically to a stock wealth tax.

This is important if the project explores a hybrid system combining a low-rate stock tax with the WDT. The two tax bases and their behavioural interactions would need to be modelled separately before their combined effect could be assessed.

## 7. What this observation does not establish

This review does **not** establish that:

- the WDT revenue estimate is wrong;
- the judgement-marked inputs are necessarily biased;
- every judgement-marked input is poorly supported;
- the 90 rows are 90 independent parameters;
- replacing judgement with more data will always narrow the model's uncertainty;
- the WDT is either viable or unviable.

It identifies where the model relies on estimates, proxies, derived quantities or assumptions, and why those areas deserve explicit treatment.

The count is not evidence for or against the proposal. It is a measure of where the model's evidential structure needs to be understood.

## 8. Overall assessment

The 90 judgement-marked rows are not, by themselves, a reason to reject the model. They are also not something to hide behind a general statement that all economic models require assumptions.

They provide a practical map of the model's evidential limits. Properly classified and tested, they can help answer three more useful questions:

1. Which assumptions are genuinely uncertain?
2. Which uncertainties materially affect the conclusions?
3. What additional evidence would most improve the model?

The next milestone should not be to eliminate all judgement. That is impossible. It should be to make judgement explicit, trace its dependencies, test its consequences and direct research towards the assumptions that matter.

**The central recommendation is to treat the 90 judgement-marked rows as a structured uncertainty programme, not as 90 independent guesses and not as 90 equal research priorities.**

---

## Register reference

Primary source: `model-specs/inputs.md`, including its dated summary of input and judgement-row counts. The register is the authority for the current count and row-level classifications. This note is an analytical interpretation of that register, not a replacement for it.

Related model documentation: `docs/model-v3/`, particularly the input register and V3 implementation plan.
