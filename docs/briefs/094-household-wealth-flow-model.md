# 094: Design an accounting-consistent household wealth-flow model

- **Status:** ready for investigation
- **Author/date:** K. Ogata with the guru, 2026-11-20
- **Depends on:** 093r consumption/depletion evidence review; household-consumption-and-wealth-replenishment hypothesis
- **Decision:** author has abandoned I-D14c's 3.5% as the preferred/central consumption or depletion assumption. Do not search for a replacement universal percentage.
- **Purpose:** specify and test a more economically coherent representation of household wealth accumulation and depletion before changing the v3 kernel.

## Goal

Replace the conceptual role currently played by the universal proportional wealth haircut with an accounting-consistent household-flow representation. The model should distinguish current income, consumption, saving, asset returns, capital gains, transfers, liabilities and WDT taxation.

This brief is a model-design and empirical-calibration task. It does not authorise selecting parameters to improve WDT fiscal closure, nor does it assume that the new model will increase private wealth, taxable wealth or revenue.

## Author decision on I-D14c

The 3.5% value is abandoned as the central model assumption. It was a judgement device, not a measured UK net-depletion rate. No replacement scalar is authorised.

- Do not continue to apply 3.5% as the preferred baseline.
- It may be retained as a labelled legacy comparator solely to reproduce and compare with historical outputs.
- Do not replace it with 0%, 1.5%, 2.5%, or another universal rate and call that empirically grounded.
- The input register and kernel must be changed only after the replacement design has been reviewed and the implementation implications are clear.
- Existing outputs relying on 3.5% must be identified as legacy results, not presented as a calibrated forecast.

## Core hypothesis

Household net worth changes through net saving from current income, revaluation, net transfers, other balance-sheet changes and taxes. Consumption reduces net worth to the extent that it causes net dissaving, asset drawdown or additional liabilities. A fixed percentage haircut to the entire existing asset stock is not a suitable general representation of household consumption.

A cohort-based model with distinct income and balance-sheet flows should better reproduce observed household wealth accumulation and decumulation than the current universal drawdown. Whether it materially changes WDT outcomes, and in which direction, is an empirical question.

## Required accounting framework

Use household net worth, not gross asset turnover:

`NW_{i,t}=Assets_{i,t}-Liabilities_{i,t}`

Candidate change identity:

`\Delta NW_{i,t}=S_{i,t}+CG_{i,t}+TR_{i,t}+O_{i,t}-T^{WDT}_{i,t}`

Definitions:

- `S`: net saving from current income after consumption and ordinary current taxes. Include retained cash property income once, and be explicit about pension saving/accrual.
- `CG`: capital gains and losses, excluding cash income already included in saving.
- `TR`: net capital transfers received, including gifts and inheritances received less those given.
- `O`: other volume changes and reconciliation items.
- `T^WDT`: WDT paid by the household, shown separately from consumption. Where within model scope, show the corresponding public/SWF receipt.

This is an accounting identity, not a behavioural equation. The model must specify the behavioural or empirical method used to estimate each flow.

Accounting rules:

1. Selling an asset and holding the proceeds as cash does not reduce net worth. Consumption of the proceeds does.
2. Consumption is funded from disposable resources first. Income left after consumption and current taxes is saving. If consumption exceeds resources, the household dissaves or borrows.
3. Borrowing increases liabilities; debt interest and repayment must be handled consistently.
4. Separate cash interest/dividends/rents from capital gains. If the return path already credits total returns to wealth, do not add cash returns again as saving.
5. Separate saving from revaluation and transfers. Do not infer saving from changes in wealth without decomposing valuation and transfer effects.
6. Household-to-household gifts and inheritances redistribute wealth. They should not create or destroy aggregate household-sector wealth except through taxes, costs, cross-border flows or sector-boundary changes.
7. Treat WDT as a transfer from private households to the state/SWF, not as consumption or destruction of aggregate wealth.
8. Define the treatment of owner-occupied housing, mortgages, private pensions and pension entitlements. Avoid double-counting pension contributions, accruals and pension assets.
9. Reconcile gross/net saving conventions and consumption of fixed capital. Do not mix incompatible national-account and survey definitions without an explicit bridge.

## Model architecture to investigate

Start with a modest cohort/cell model, not a full microsimulation:

- Minimum segmentation: wealth and income.
- Add working/retired status or age where data support it.
- Consider asset liquidity/composition only where data can identify or bound it.
- Each cell has an initial net-worth distribution or representative balance sheet, income flow, consumption flow, saving/dissaving flow, returns/revaluation, transfers and WDT payment.
- Demographic transitions, household formation/dissolution and inheritance should be included only to the extent required to preserve the relevant aggregate and distributional accounting.

The model may initially be partial-equilibrium, with GDP, labour income and return paths specified externally. If so, state that clearly. Do not claim a fully stock-flow-consistent macro model unless household flows are reconciled with firms, government, financial institutions and the rest of the world.

## Tests

### Test A: Map the existing kernel

Document precisely:
- where I-D14c enters the v3 kernel and what it does to units/wealth;
- how returns are currently credited (cash income, capital gains or total return);
- how WDT payments affect private wealth and whether the corresponding public/SWF asset is represented;
- whether pensions, liabilities, gifts and bequests are currently represented;
- which outputs and prior results depend on the 3.5% setting.

Do not change code in this audit step.

### Test B: Specify the household accounts

Produce a flow-of-funds diagram and a variable dictionary. For each term in the identity, state:
- economic meaning and sign convention;
- whether it is a flow or stock;
- source and data definition;
- whether it is endogenous, calibrated, externally specified or a judgement;
- which other term could overlap with it;
- treatment under nominal and real accounting.

Demonstrate that asset sales, borrowing, debt repayment, pension contributions, cash returns and capital gains are not double-counted.

### Test C: Build an evidence and calibration map

Use UK sources where possible:
- ONS Wealth and Assets Survey, including longitudinal evidence and asset/liability composition;
- ONS household income, spending and wealth statistics, with the matched/experimental nature made explicit;
- ONS sector accounts and household balance sheets for aggregate reconciliation;
- ELSA/IFS retirement drawdown evidence, with its England/financial-wealth coverage limits;
- relevant academic and Bank of England work on saving, dissaving and wealth accumulation.

For each parameter/flow, report measured quantities, population, dates, definitions, limitations and whether the data identify a level, rate, transition or only a bound. Keep labour-funded saving, retained property income, capital gains, transfers and dissaving distinct wherever possible.

Do not convert the aggregate household saving ratio directly into a wealth-depletion rate. Do not infer band-specific depletion rates where the data do not support them.

### Test D: Construct the simplest viable cohort model

Specify at least:
1. a working household cell with positive net saving;
2. a low-saving or zero-saving cell;
3. a retired/dissaving cell;
4. a high-wealth cell whose saving and wealth preservation may differ from the others.

These are test cells, not claims that every household in a group behaves identically. Show how the same accounting identity applies to each. Use ranges or calibrated distributions where evidence supports them; label judgement assumptions explicitly.

Do not force each cell to have a positive saving rate. Do not assume all retirees decumulate or all high-wealth households preserve wealth.

### Test E: Historical fit and validation

Where data permit, backcast the model over overlapping UK data periods. Compare predicted with observed:
- aggregate household net worth and its asset/liability composition;
- saving and dissaving by group;
- distribution of wealth and changes by age/wealth group;
- capital gains versus active accumulation;
- retirement drawdown;
- household-sector aggregates.

Use a holdout period or other out-of-sample check if the data permit. Report survey uncertainty, sample attrition, changing definitions and reconciliation residuals. A model that matches aggregate wealth while missing distributional dynamics is not sufficient.

### Test F: WDT consequences

Only after Tests A-E establish a coherent and empirically defensible model, compare:
- legacy 3.5% runs (reproduction only);
- the new cohort-flow baseline;
- defensible low/high parameter or behavioural scenarios.

Use common starting distributions, return paths, tax schedules, seeds and conventions. Report real private household net worth, wealth/GDP, taxable wealth, taxpayer counts, taxable increments, receipts, relief components, distributional outcomes and fiscal closure. Attribute differences to the flow mechanisms, not to unrelated calibration changes.

A more favourable fiscal result is not evidence of a more accurate economic model. A worse result is not evidence against it either.

## Acceptance criteria

- The 3.5% value is explicitly retired as the preferred/central assumption; no replacement scalar is invented.
- The existing kernel and all affected outputs are mapped.
- A coherent household balance-sheet identity and variable dictionary are provided.
- Cash returns, capital gains, saving, consumption, transfers, liabilities, pensions and WDT are accounted for without double counting.
- The proposed cohort structure is the simplest one that can represent accumulation and drawdown and can be calibrated from available data.
- UK evidence is mapped to each flow, with gaps and incompatible definitions clearly identified.
- The report distinguishes data, calibrated estimates, judgements and illustrative scenarios.
- No code/register/manifest change is made until the author reviews the design and authorises implementation.
- No result is selected or calibrated to achieve a desired fiscal closure outcome.

## Touches

Expected research/design outputs only:
- `docs/research/094-household-wealth-flow-model.md` (new)
- this brief's progress block
- `docs/hypotheses/household-consumption-and-wealth-replenishment.md` (updated with the 093r evidence and author decision)

Do not edit the kernel, input register, manifest, schedules, retirement rules or fund rules in this brief.

## Out of scope

- Selecting a new universal consumption/depletion percentage.
- Implementing the new kernel.
- Changing tax rates, thresholds, indexation or fund rules.
- Claiming macroeconomic closure from a household-only partial-equilibrium model.
- Choosing assumptions to make WDT fiscally close.

## Progress

- **Decision:** 3.5% abandoned as the preferred/central assumption; retain only as a labelled legacy comparator.
- **Next:** map the current kernel, specify household accounts, and assess which flows UK data can actually calibrate.
- **Not done:** no code or register changes; no new parameter values selected.
