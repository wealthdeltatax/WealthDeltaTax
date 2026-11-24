# Hypothesis: the household-flow model needs a longitudinal empirical identification phase

**Status:** New hypothesis and proposed research direction; subject to author review  
**Date:** 2026-11-22  
**Depends on:** `research/hypotheses/empirical-household-flow-parameter-map.md`; 124c household-arm first run; 125c validation against 099r moments  
**Scope:** Empirical source identification and measurement design. No model parameters, tax schedules, fiscal assumptions or code are changed by this document.

## 1. Hypothesis

The household arm cannot yet support credible wealth-specific saving, accumulation or transition parameters. The next research phase should use longitudinal household data, principally the Wealth and Assets Survey (WAS), to identify which components of household wealth change can be measured by starting wealth, age and life stage.

The central hypothesis is that the present household-arm results are materially shaped by an absence of empirically identified heterogeneity. In particular, a common saving ratio across wealth groups, fixed asset-class returns and no observed wealth transitions cannot establish how wealth concentration, taxpayer composition or WDT receipts evolve. The observed decline in modelled wealth concentration is therefore a mechanical consequence of the current assumptions, not empirical evidence that wealth naturally becomes more equal.

The research should not attempt to produce a single replacement saving rate. It should first determine which dimensions of household accumulation and decumulation can be identified from available longitudinal data, and distinguish direct observations from residuals, proxies and scenario assumptions.

**Working hypothesis:** a longitudinal WAS analysis, supplemented by retirement-focused ELSA evidence and independent top-tail wealth measurement, can materially improve the empirical identification of household wealth transitions and active accumulation. It may not identify every desired wealth-band × life-stage parameter. Unsupported cells should remain unset or be represented by labelled scenarios.

## 2. Evidence motivating the hypothesis

### 2.1 The household arm is structurally under-identified

The first household-arm run (124c) established that the accounting implementation can complete for three of five initial scenario points, with account identity and public-ledger checks tying closely. However:

- Two scenario points fail I1 when non-pension asset classes are exhausted while pension wealth continues to grow. This is an accounting/floor interaction requiring diagnosis, not evidence that the household economics are correct or incorrect.
- The household arm has no meaningful path dispersion: asset-class returns and GDP growth are fixed by scenario, so P10, mean and P90 coincide. The 1,000 paths do not currently represent 1,000 distinct household or market histories.
- The resulting M1, M2 and debt paths differ substantially from the legacy arm. These are model outputs under the present assumptions, not forecasts or evidence of fiscal sustainability.
- The household model has not yet established wealth-specific saving behaviour, realistic portfolio heterogeneity or transitions between wealth groups.

The absence of path variation should be treated separately from empirical parameter uncertainty. Adding random noise to fixed assumptions would not solve the identification problem.

### 2.2 Existing validation does not identify a saving gradient

The 125c comparison against 099r moments shows that the current evidence collection is useful for broad checks but does not identify the key household-flow parameters:

- Of 33 empirical moments mapped, five were held as data, four partly held and 24 were not held. Of ten useful validation moments, only one was also held as data, and that comparison was only partly like-for-like.
- The observed top-decile wealth share is around one half, while the model starting pack is materially lower and the model's year-100 concentration falls further. The model currently applies the same saving ratio across wealth groups and has no empirical wealth transitions. The long-run concentration result is therefore not a validation result.
- The retired-wealth comparison is not valid as currently constructed: the model's retired-person share is being compared with an observed retired-wealth share.
- The saving-ratio comparison partly reuses the ONS series from which the model input was constructed. It confirms that the source series was represented, but is not independent validation.
- The current evidence does not empirically identify saving by wealth group.

The immediate gap is not a shortage of aggregate wealth totals. It is the absence of independently identified household-level changes and their decomposition.

### 2.3 The best candidate sources answer different questions

The source review identifies a hierarchy rather than one universal dataset:

1. **WAS longitudinal microdata** is the strongest candidate for household wealth transitions, asset and debt changes, demographic and employment changes, and active/passive accumulation analysis. The UK Data Service catalogue identifies the combined Waves 1–5 and Rounds 5–8 longitudinal study (Study 7215). Access is safeguarded, and the public microdata have disclosure and top-tail limitations. ONS also warns that published and public-microdata aggregates need not match exactly.
2. **Resolution Foundation, _Before the Fall_ (2025)** provides a useful existing analysis of active and passive accumulation using WAS and external asset returns. Its active-accumulation residual is not pure saving: it can include net saving, debt changes and wealth transfers. Reuse its method and results with that interpretation, rather than relabelling the residual as a saving rate.
3. **ELSA and IFS retirement research** provide a complementary longitudinal view of financial wealth decumulation among older households. ELSA is particularly relevant to retirement transitions and financial-wealth use, but does not replace WAS for the full wealth distribution.
4. **IFS 2026 work on DB pension valuation** is important for harmonising pension wealth across WAS rounds. Pension valuation-method changes can create artificial breaks in measured wealth changes.
5. **Advani, Summers and Tarrant (2025)** provide a top-tail measurement cross-check using survey and income-capitalisation approaches. This is needed because WAS under-represents very high wealth, even with oversampling.
6. **ONS published wealth tables** provide immediate aggregate and distributional cross-checks by wealth component, age and decile. They are not a substitute for longitudinal microdata.
7. **HMRC Distribution of Personal Wealth** is based on estates and is old (2014–16). It can be used as a historical cross-check on estate composition and mortality-related measurement, not as a current household wealth or saving dataset.

Source links and retrieval details should be recorded in the research output, including access restrictions and exact versions used.

## 3. Specific empirical propositions to test

The research should test the following propositions independently. They are not assumed to be true.

### P1. Active accumulation varies with starting wealth

Households in different starting wealth groups may have different active accumulation after accounting for the passive return on their initial asset holdings. The direction and shape of this gradient are unknown.

Test whether the gradient persists after conditioning or stratifying by age, employment, household income, asset mix and starting debt.

### P2. Wealth mobility is material and heterogeneous

Households move between wealth groups over time. Transition probabilities may vary by age, starting wealth, employment, household composition and asset mix.

Estimate observed transitions across matched WAS waves. Do not infer mobility from changes in cross-sectional decile shares.

### P3. Retirement changes the composition and direction of wealth flows

Retirement may reduce labour income and contributions while changing pension income, financial-asset withdrawals, debt repayment and consumption. These changes may differ by initial wealth and pension type.

Use WAS where possible and ELSA as a targeted supplementary source. Do not treat retirement status as equivalent to age 65+, or a retired-person share as a retired-wealth share.

### P4. Asset composition changes the relationship between income, saving and net-worth change

Property, private pensions, financial assets and physical wealth have different cash-flow, valuation and liquidity characteristics. A single household saving ratio cannot represent all of them.

Estimate asset-class-specific changes and distinguish cash flows from revaluation wherever the data permit.

### P5. Top-tail under-coverage materially affects aggregate and distributional estimates

WAS survey weights and oversampling improve coverage but do not fully resolve the under-representation of very high wealth. Compare survey-based estimates with independent top-tail methods and report sensitivity rather than forcing a single correction.

## 4. Recommended research design

### Workstream A: WAS longitudinal extraction (first priority)

Use the UK Data Service longitudinal WAS study, subject to access and permitted-use conditions. Start with a feasibility audit of the actual available files, wave identifiers, longitudinal weights, household/person linkage, variable definitions and disclosure rules.

Produce five core outputs:

1. **Wealth transition matrices:** starting wealth decile or defensible band against ending wealth decile/band for each available interval. Report transition probabilities, upward/downward mobility, immobility, sample sizes and uncertainty. Use consistent wealth definitions and longitudinal weights.
2. **Active/passive accumulation:** calculate passive changes from starting asset holdings and external asset-class return series. Compare with observed wealth changes. Label the residual *active accumulation*, not pure saving. Show results by starting wealth, asset class, age and life stage where sample sizes permit.
3. **Income, saving and debt profiles:** examine household income, reported saving, consumption where available, debt changes and wealth changes by starting wealth and life stage. Make clear which quantities are direct survey responses and which are balance-sheet residuals.
4. **Pension lifecycle:** track private pension wealth and financial wealth around retirement, separating DB and DC where the data permit. Harmonise DB valuation methodology across rounds and test alternative pension bases.
5. **Asset allocation:** measure property, private pension, financial and physical wealth shares by starting wealth group, with a separate top-tail view only where data support it.

For every output retain the survey weight used, unweighted and weighted sample counts, standard errors or confidence intervals, missing-data treatment, wave coverage and exact wealth definition. Test robustness excluding Round 8 (2020–22), given pandemic-period fieldwork and the quality caveats around the series.

Do not assume that the public-use microdata can reproduce published ONS totals exactly. Record the discrepancy and investigate its source.

### Workstream B: ELSA retirement supplement

Use ELSA/IFS research to answer a narrow set of questions not adequately resolved by WAS:

- how financial wealth changes through retirement;
- how outcomes differ by initial financial wealth and pension arrangements;
- the relative roles of withdrawals, annuitisation and drawdown;
- whether financial wealth is run down, preserved or replenished after retirement.

Keep the ELSA population boundary explicit: it follows older people in England and is not a representative panel of all UK households or all wealth groups. Do not splice ELSA estimates directly into WAS cells without a documented population and definition bridge.

### Workstream C: top-tail triangulation

Use Advani, Summers and Tarrant (2025) and related top-wealth work to assess the likely gap between survey estimates and top-tail adjusted estimates.

The objective is not to manufacture missing household transitions for the top 1%. It is to establish:
- which top-tail wealth shares and asset compositions are robust across methods;
- which survey-based estimates are likely understated;
- whether a defensible sensitivity range can be specified;
- which top-tail flow parameters remain unidentified.

Keep top-tail stock corrections separate from behavioural assumptions about saving or returns.

### Workstream D: pension valuation harmonisation

Document the DB pension valuation basis used in every WAS round and in each comparator. Reconstruct a consistent series where possible, and show alternative valuation bases as sensitivities.

Do not interpret a change caused by a valuation-method break as household saving, pension accrual or a real wealth transition.

### Workstream E: independent aggregate checks

Cross-check the microdata outputs against ONS published wealth distributions, component totals and national-account aggregates where definitions permit.

The checks must be genuinely independent of the input series used to construct the model parameter. In particular, a model saving ratio derived from an ONS series cannot then be presented as independently validated by that same series.

## 5. Measurement rules

These rules are mandatory for the research.

1. **Wealth change is not saving.** It combines active saving, holding gains/losses, debt changes, transfers, household composition changes, valuation changes and survey/reporting error.
2. **Active accumulation is a residual.** Unless the components are independently observed, do not call it pure saving or assign the whole residual to household behaviour.
3. **Use starting wealth for gradients.** Grouping by end-period wealth risks conditioning on the outcome being explained. Report starting-group results as the primary analysis and ending-group results only as a secondary description.
4. **Do not infer decile transitions from repeated cross-sections.** Transitions require matched longitudinal observations and appropriate longitudinal weights.
5. **Keep household and person units distinct.** Wealth is generally measured at household level, while age, retirement and employment may be person-level. State how person characteristics are assigned to households.
6. **Keep pension definitions consistent.** DB accrued rights, DC pots and pension income are not interchangeable. State whether pension wealth is included and on what valuation basis.
7. **Treat transfers as redistribution unless the counterparty is outside the modelled sector.** Inheritances and gifts can change household wealth without creating aggregate private wealth.
8. **Do not fill unsupported cells by proportional allocation.** Merge cells, use a labelled proxy/scenario or leave them unset.
9. **Separate sampling uncertainty from model uncertainty.** Survey confidence intervals do not capture uncertainty from return assumptions, residual decomposition or model structure.
10. **No calibration to desired fiscal outcomes.** Source choice, grouping and transformations must not be selected to improve WDT receipts, fund fill, debt or fiscal closure.

## 6. Expected deliverables

The research phase should produce:

- **Source register:** exact dataset/table/report, URL, version, access conditions, reference periods, population, unit, weights and limitations.
- **WAS feasibility and variable map:** wave availability, longitudinal linkage, variable names, definitions, weights, suppression and missingness.
- **Transition tables:** weighted wealth transition matrices with uncertainty and sample diagnostics.
- **Active/passive accumulation tables:** by starting wealth group and relevant asset classes, with the residual correctly labelled.
- **Income/debt/pension tables:** only for cells supported by the source.
- **Top-tail comparison:** survey versus adjusted wealth shares and the implications for model starting distributions.
- **Cell coverage matrix:** direct observation, derived measure, proxy, scenario or unset for every proposed wealth × life-stage cell.
- **Parameter recommendations:** values or ranges only where identified; explicit unset rulings elsewhere.
- **Data-access request list:** exact additional data required, the parameter it would inform, why public data are insufficient and whether the model can proceed without it.

Every table must include its definition, period, unit, population, weighting, sample size and uncertainty. Reproducible scripts and source lineage should be retained.

## 7. Implications for the model

Until this research is complete:

- Do not describe the current wealth-concentration trajectory as an empirical projection.
- Do not treat P10, mean and P90 as a meaningful distribution when the underlying paths are identical.
- Do not interpret the 1,000 identical paths as uncertainty analysis.
- Keep fixed return regimes explicitly labelled as scenarios. A separate market/household path model may be considered later, but stochastic variation must be grounded in an identified process.
- Keep the two I1 floor failures open as a distinct accounting issue. Do not alter household behaviour or asset economics merely to make the checks pass.
- Do not promote the current household-arm revenue or debt results to headline forecasts.
- Retain the legacy arm and existing digest unchanged as a comparator while the empirical baseline is developed.

The existing hypothesis, `empirical-household-flow-parameter-map.md`, remains the overarching accounting and classification framework. This document narrows the next research step to empirical identification of heterogeneity, transitions and lifecycle flows.

## 8. Acceptance criteria and decision gates

The phase is successful if it establishes, with reproducible evidence:

1. Whether WAS longitudinal data can support matched household wealth transitions across the relevant rounds.
2. Which wealth-group differences in active accumulation are estimable, and with what uncertainty.
3. Which components of the active-accumulation residual can be separated from returns, debt changes and transfers.
4. Whether retirement-related wealth decumulation can be estimated by initial wealth and pension type, or only more broadly.
5. The minimum defensible wealth-band × life-stage cell structure.
6. The size and direction of top-tail measurement sensitivity.
7. A harmonised pension valuation basis or a clearly specified set of sensitivities.
8. Independent validation moments that do not reuse the model's calibration inputs.
9. A complete list of parameters that must remain unset or scenario-based.

At the end, classify each proposed model input as:
- **Empirically identified:** direct evidence supports the measure at the required resolution.
- **Derived with defensible assumptions:** reproducible calculation, with uncertainty stated.
- **Proxy:** useful but not equivalent to the target parameter; sensitivity required.
- **Scenario only:** no empirical central value is justified.
- **Unset:** evidence is insufficient even for a defensible scenario range.

A failure to identify a parameter is a valid research result. It must not be hidden by a convenient point estimate.

## 9. Recommended order of work

1. **WAS access and feasibility audit.** Confirm whether the required longitudinal microdata and weights are actually accessible. Do this before commissioning a large extraction.
2. **WAS transition and active-accumulation pilot.** Start with a small number of waves and a compact set of wealth groups. Establish whether the core decomposition is feasible and interpretable.
3. **Full WAS extraction.** Expand only after the pilot resolves linkage, weights, definitions and sample-size issues.
4. **Pension and retirement supplement using ELSA.** Target the gaps identified by the WAS pilot.
5. **Top-tail triangulation.** Reconcile starting wealth distributions and specify sensitivity bounds.
6. **Parameter-map update.** Feed results into the existing parameter-map hypothesis and decide which model cells can be populated.
7. **Only then revise the household baseline.** Do not change the kernel to fit results before the evidence and accounting conventions are settled.

## 10. Falsification and limitations

This hypothesis would be weakened if:
- WAS longitudinal data cannot provide sufficiently reliable matched wealth observations or weights;
- active accumulation residuals are too contaminated by transfers, debt and measurement error to identify useful behavioural differences;
- wealth-group and life-stage cells are too sparse for stable estimates;
- retirement evidence cannot be reconciled across WAS and ELSA;
- top-tail adjustments are too method-dependent to constrain the model usefully.

If so, the appropriate response is a simpler model with fewer empirically supported groups and explicit scenario ranges. It is not to manufacture a detailed gradient from aggregate averages.

## 11. Decision requested

Approve a focused longitudinal empirical-identification phase, beginning with a WAS access and feasibility audit followed by a small transition/active-accumulation pilot.

The key question is not whether the household arm can be made to produce a plausible concentration curve. It is whether observed UK household data can identify the wealth mobility, active accumulation and lifecycle behaviour needed to make that curve meaningful.

No model parameter or fiscal conclusion should be revised solely on the basis of this hypothesis.
