# Hypothesis: an empirical household-flow parameter map should replace the universal 3.5% drawdown

**Status:** Hypothesis and proposed research design; subject to author review  
**Origin:** 090c–100r diagnostics and the agreed household-flow refactor plan  
**Scope:** Research and parameter classification only. No model code, input values, tax schedules, fund rules or fiscal assumptions are changed by this document.

## 1. Hypothesis

WDT should move from a universal annual consumption/drawdown parameter to an empirically constrained household-flow model, built from a transparent parameter map across wealth band and life stage.

The central proposition is that the current 3.5% parameter is not an empirically established measure of household consumption, saving or net dissaving. In the v3 kernel it is a uniform proportional liquidation of existing household asset units. It is applied to all households, routes and asset classes, without representing the income and balance-sheet flows that determine whether a household accumulates wealth, maintains it or draws it down.

The next research step should therefore not estimate a replacement scalar. It should determine, flow by flow and household cell by household cell, which quantities can be measured from the completed research collection, which can be derived consistently, which require proxies or explicit scenario assumptions, and which must remain unset.

**Working hypothesis:** a parameter map that separates observed data, derived quantities, proxies, judgement scenarios and unresolved parameters will provide a defensible specification for a new untaxed household baseline. That baseline can then be compared with the legacy kernel and have WDT applied on top.

This does not presume that the new model will produce higher wealth, higher receipts or better fiscal closure. The direction and size of those effects are empirical results to be tested, not design objectives.

## 2. Why this is the next step

The current kernel effectively applies:

```
W[t+1] = W[t] * (1 + r[t]) * (1 - c)
```

where c is the same proportional drawdown across the model. The operation has no corresponding household wage, self-employment, pension-income, cash-income, saving, borrowing, debt repayment or transfer flows. The recorded consumed amount is not received by another modelled sector.

The research to date establishes the need for a different specification:

- **090c:** long-run wealth/GDP and fiscal outputs are highly sensitive to c. The current setting is consequential, not innocuous.
- **093r–096r:** the consumption treatment is a stock drawdown rather than a household budget model; the accounting identities and missing flows have been mapped.
- **097r:** open UK macroeconomic and national-account series provide aggregate constraints and time series.
- **098r:** Wealth and Assets Survey material provides household wealth distributions and population information, with limits on which flows can be cross-tabulated.
- **099r:** on the assumption that the held PDFs are successfully extracted and reconciled, the research collection adds published empirical moments and estimates. These must be classified by population, period, definition and evidential strength rather than treated as interchangeable observations.
- **100r:** JST historical returns can be decomposed into cash-yield and holding-gain components. The result is an aggregate market-portfolio decomposition, not a household saving or retained-income estimate.

Together these sources are sufficient to begin a parameter map. They are not assumed to identify every household flow directly.

## 3. What the parameter map must answer

For each required variable, the map must answer:

1. What is the economic definition?
2. Is it a household flow, a stock, a revaluation, a transfer, a tax or a model identity?
3. Which population and unit does the source cover?
4. What period, frequency and price basis does it use?
5. Which wealth-band and life-stage cells can actually be observed?
6. Is the value observed, derived, proxied, scenario-based or unset?
7. What transformation or reconciliation is required?
8. What uncertainty, coverage gap or double-counting risk remains?
9. Is the parameter suitable for calibration, validation only, or neither?

The map must distinguish a variable being available somewhere in the source collection from it being available at the required cell resolution. An aggregate national-account series does not become a wealth-band parameter merely because a household survey also contains wealth bands.

## 4. Required household-flow account

The proposed account is a net-worth reconciliation, not a list of independent additions to wealth.

At household or cell level, use a clearly defined identity of the form:

```
Change in net worth
  = net saving from current income
  + holding gains and losses
  + net capital transfers and other volume changes
  - net taxes and other relevant charges
```

The exact signs and classifications must follow the chosen accounting framework. In particular:

- **Income and consumption:** disposable income is allocated between consumption and saving. Consumption is not automatically a percentage of existing wealth.
- **Saving:** saving is the part of disposable income not consumed, with pension saving and imputed items treated consistently with the selected data definition.
- **Cash yield:** dividends, rent, interest and other property income must be treated consistently with whether they are included in disposable income, retained, distributed or consumed.
- **Holding gains:** asset-price revaluation is separate from current income and saving. It must not be counted as cash income.
- **Transfers:** gifts, inheritances and other capital transfers redistribute net worth between households. They should not be treated as newly created aggregate private wealth unless the counterparty lies outside the modelled household sector.
- **Debt:** borrowing creates a liability as well as an asset or expenditure; debt repayment reduces liabilities and/or liquid assets. Inflation revaluation of nominal liabilities must have the correct sign.
- **Taxes:** WDT and other taxes must be placed once, at the correct point in the flow and stock reconciliation.
- **Pensions:** contributions, employer contributions, investment returns, accruals and decumulation need a consistent treatment. Pension wealth cannot simply be treated as liquid cash available for consumption.

The account must reconcile both household assets and liabilities to net worth. It must also identify counterparties where needed to prevent the model from creating income or wealth without a corresponding sectoral flow.

### Critical no-double-counting rule

The JST total return is already the sum of yield and holding gain. If the model credits total return to assets, it must not also add retained yield as saving. A valid design can either:

- credit holding gains separately and add retained cash income through saving; or
- credit total return and define saving to exclude the yield already credited.

The parameter map must select and document one convention before implementation. The same principle applies to pension income, employer contributions, imputed rent and transfers.

## 5. Proposed classification

Every parameter or moment must receive one of five classifications:

| Classification | Meaning | Permitted use |
|---|---|---|
| **Observed** | Directly reported by a source with a matching definition and population | Calibration or validation, subject to quality checks |
| **Derived** | Calculated from observed quantities using a documented identity or transformation | Calibration, with formula and source lineage |
| **Proxy** | Related empirical measure used because the exact variable is unavailable | Calibration only with explicit caveat and sensitivity |
| **Scenario** | Deliberate judgement value used to explore an unresolved mechanism | Labelled scenario runs only |
| **Unset** | Evidence does not justify a value or range | Must not silently receive a central estimate |

A source moment can be observed while the model parameter inferred from it remains a proxy or unset. For example, aggregate household saving is observable, but a saving rate for the top wealth decile at a particular life stage may not be.

Do not infer a cell-specific value by distributing an aggregate in proportion to wealth unless a separate empirical or explicitly labelled scenario basis supports that allocation.

## 6. Required dimensions and cells

The agreed Scenario B design is a matrix of **wealth band × life stage**. The parameter map should use those dimensions as its target structure, but must not pretend the source data support every cross-tabulation.

At minimum, test the availability of:

- wealth band, using definitions compatible with the WDT tax base;
- age or life-stage group;
- employment and retirement status;
- household disposable income;
- consumption expenditure;
- saving and dissaving;
- liquid and illiquid asset composition;
- private pension wealth and pension flows;
- secured and unsecured liabilities;
- gifts, inheritances and other transfers;
- asset cash yields and holding gains.

Where a cell is too sparse, suppressed, unavailable or definitionally incompatible, record the gap. Possible responses are to merge cells, use a documented proxy, run a labelled scenario, or leave the parameter unset. The choice must be explicit and must not be driven by the resulting WDT revenue.

## 7. Research tasks for the parameter-map phase

The next research brief should produce the following deliverables.

### A. Source-to-variable crosswalk

List every relevant source from 097r–100r and the completed 099r collection. For each source, record:

- exact file, table, page or series identifier;
- publisher and source URL;
- reference period and publication date;
- population, unit, frequency and price basis;
- definitions and coverage;
- available dimensions and cross-tabulations;
- known revisions, sampling limitations and missing observations;
- whether the held repository file was checked against the published source.

### B. Parameter register

Create one row for every required flow, stock, rate, weight or transition. Include:

- variable name and definition;
- accounting location;
- target cell dimension;
- classification (observed / derived / proxy / scenario / unset; plus endogenous for model outputs that are not parameters, such as T_WDT, dNW and r_f, added after 103r);
- source and exact reference;
- calculation or transformation;
- value or range, only where supported;
- uncertainty and caveats;
- intended model use;
- outstanding question or data request.

Do not force a numeric value into rows classified unset.

### C. Cell coverage matrix

Show which variables are genuinely available for each wealth-band/life-stage cell. Distinguish direct observations from modelled allocations and aggregate constraints. Identify the minimum cell structure supportable by the data, rather than starting with a preferred number of cells and filling them artificially.

### D. Accounting and reconciliation decisions

Resolve the conventions needed to combine sources:

- disposable income versus primary income;
- consumption and saving definitions;
- pension contributions, accrual and withdrawals;
- property income and imputed rent;
- nominal cash yield versus holding gains;
- nominal versus real returns and CPI deflation;
- household debt and liability revaluation;
- gifts, inheritances and inter-household transfers;
- household survey totals versus national-account totals;
- WDT tax timing and settlement.

Where two sources disagree, report the difference and explain whether it is a definitional, coverage, timing or measurement discrepancy. Do not average incompatible measures.

### E. Unresolved-data list

List the smallest set of additional data required from the author. For every request, give the exact table/file/series, why it matters, which parameter it informs, and whether the model can proceed without it using an unset parameter or labelled scenario.

## 8. Tests and acceptance criteria

The parameter-map phase is complete only when:

1. Every flow required by the proposed household account has a row in the parameter register.
2. Every row has a definition, accounting location and evidence classification.
3. Every observed or derived value has traceable source lineage and a reproducible calculation.
4. Every proxy has a stated reason and a sensitivity requirement.
5. Every scenario is visibly labelled as judgement, not empirical evidence.
6. Every unset parameter is listed with its consequence for implementation.
7. The cell coverage matrix shows which wealth-band/life-stage distinctions are supported and which are not.
8. Aggregate household totals are compared with appropriate national-account constraints where definitions permit.
9. The cash-yield/holding-gain convention is consistent with 100r and cannot double-count income.
10. No parameter is selected or adjusted to improve WDT revenue, fund fill, fiscal closure or political attractiveness.

The output should end with explicit rulings:

- **Ready for implementation:** sufficiently evidenced and defined.
- **Implement with scenario range:** mechanism is required but its value is uncertain.
- **Remain unset:** no defensible parameter or range is available.
- **Further data required:** a specific missing source materially blocks the design.

## 9. What happens after the map

The parameter map is a design gate, not a reason to delay all engineering work indefinitely.

Once the map is reviewed:

1. Implement a household-flow function behind the existing consumption operation, with a legacy mode that reproduces existing results exactly.
2. Add only the pack data justified by the map, including the 100r return decomposition where it is useful.
3. Build the wealth-band/life-stage baseline and transitions, keeping unsupported values unset or in labelled scenarios.
4. Reconcile household and public-sector accounts so WDT receipts, the state's asset stake and fund balances are not separate, inconsistent representations.
5. Validate the untaxed baseline against independent historical household wealth, income, consumption and saving moments.
6. Compare the new and legacy arms using common assumptions where possible, with an attribution of differences to specific mechanisms.

The old 3.5% path remains available as a comparator. It is not the default calibration target and should not be silently carried into the new baseline.

## 10. Falsification and risks

This hypothesis would be weakened if the completed data collection shows that the required household-flow parameters cannot be identified at a useful level of aggregation, or if a coherent flow model cannot improve historical accounting consistency and fit relative to the simpler drawdown representation.

Other risks include:

- survey wealth changes mixing saving, revaluation, transfers and measurement error;
- incompatible household definitions across WAS, expenditure, income and national accounts;
- insufficient sample sizes at the top of the wealth distribution;
- pension wealth being measured on a different basis from liquid household assets;
- using aggregate asset returns as if they were household portfolio returns;
- allocating aggregate saving or income to wealth cells without evidence;
- treating transfers as new aggregate wealth;
- modelling household flows without consistent business, government and external-sector counterparts.

If these limitations prevent a fully identified cell model, the correct result is a smaller empirically supported model plus explicit scenario and unset parameters. It is not a return to an undocumented universal scalar.

## 11. Decision requested

Approve the parameter-map phase as the next WDT research task, assuming 099r completes successfully and its extracted moments are available.

The immediate deliverable is the source-to-variable crosswalk, parameter register, cell coverage matrix, accounting rulings and unresolved-data list. No new central consumption rate is to be proposed.

**The decision being tested is not which percentage replaces 3.5%. It is which household flows can be represented from evidence, at what level of disaggregation, and with what remaining uncertainty.**
