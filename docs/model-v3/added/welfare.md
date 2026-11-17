# Welfare outputs OW1 to OW3 (brief 015g)

> Integrated into `metrics.md` and `outputs.yml` on 2026-11-17 (ids renumbered there). Those two files are the definition; this file keeps the working, flags and research requests.

Status: proposed, for the guru merge into `metrics.md`, `outputs.yml` and `inputs.md` after briefs 014g, 015g and 016g are done. Nothing here edits those files. No values are chosen: every number below is cited as a v1 finding to check, not a fact. Old figures (WFR, paper 19 and 19a) come from a single-agent model and are not carried as targets.

Source claims: ledger section 4, claim 10 (CGT lock-in; concentration and contribution envelope) and claim 19 (welfare of six tax systems at revenue equivalence, FAL H4). Ledger section 6.2, S6 and S12.

Design rule (brief goal): all three are read off the same v3 run as the headlines, on the same return paths, schedules (S_low, S_central, S_high) and windows. Where that is not possible without a second model, section 5 says so.

Conventions as in `metrics.md`: payer = adult at or above W_min; t = years since launch; real money; P10, mean, P90 over return paths (level 1), tornado and P10 to P90 over parameter draws (level 2), reported apart.

## 1. OW1: certainty-equivalent welfare of the tax systems at revenue equivalence

- **Proposed id:** OW1 (metric MW1). Claim a spoke may make: "At the same revenue, the WDT costs payers X basis points of certainty-equivalent welfare, against Y for income tax and CGT and Z for a stock wealth tax" (S6-B; FAL H4 in S12). Whether it is "less" is read from the range, not asserted.
- **Metric row:**

| ID | Name | Definition | Denominator | Unit | Horizon |
|---|---|---|---|---|---|
| MW1 | Certainty-equivalent welfare cost, by tax system | For payer i, CEW_i(s) = (E[U^-1(W_N,i(s))] / E[U^-1(W_N,i(none))]) - 1, with U the CRRA utility of terminal wealth W_N under system s, and the no-tax run on the same return paths as benchmark. Systems s: v3 WDT (the named schedule), income tax and CGT on the realised-gain base, stock wealth tax, consumption tax. Each comparator rate is solved so that its expected revenue equals the WDT's (revenue equivalence, same payers, same paths). Reported overall (payer-weighted) and by wealth band; the difference to the WDT is the headline | no-tax certainty equivalent | basis points of benchmark; difference in basis points | one life, N = G = 30 years (M3 life length); the steady-state horizon is not used |
| Summary form | p10_mean_p90 over return paths per schedule; tornado over gamma and the comparator rate solver | | | |

- **Inputs needed:**
  - Return paths and loss years: I-D1a, I-D1b, I-D1c (v3 level 1 draws).
  - Wealth by band and payer count: I-D4a, I-D4b, I-D4c.
  - Comparator revenue targets and rates: I-M5a to I-M5q for the wealth-tax comparators; I-M6h, I-M6k (CGT), I-M6a, I-M6k (IHT) and I-M6l (income tax) for today's systems.
  - Behavioural response applied equally to all systems: I-D5a, I-D5b.
  - Risk aversion gamma (CRRA): **MISSING.** Research request: the range of relative risk aversion used in published welfare work on UK or comparable household portfolio choice, with a defensible low, central and high. The old papers used 2 as a single value, which is a choice, not an input.
  - Consumption tax base (share of wealth change consumed by band): **MISSING.** Research request: UK consumption to wealth ratios by wealth band, needed only if the consumption tax stays in the comparison. The author may drop this comparator; the old model found it welfare-identical to the stock wealth tax.
- **`outputs.yml` line to add:**
  `  - {id: OW1,  metric: MW1, title: "Certainty-equivalent welfare of the tax systems at equal revenue", summary: p10_mean_p90, by: [overall, wealth_band, tax_system], element: [S6, S12], kind: comparison}`

## 2. OW2: CGT lock-in welfare cost

- **Proposed id:** OW2 (metric MW2). Claim a spoke may make: "Where today's CGT makes holders delay switching to a better asset, the delay costs X basis points of certainty-equivalent welfare for payers with embedded gains Y; the WDT has no such cost by construction" (S6-B).
- **Metric row:**

| ID | Name | Definition | Denominator | Unit | Horizon |
|---|---|---|---|---|---|
| MW2 | CGT lock-in cost | The CEW (as MW1) of a payer holding asset A with embedded gain ratio g = G/V, who can switch to asset B, under CGT with realisation on switching, minus the CEW of the same payer in the same state with the switching decision tax-neutral. The payer switches when the return of B on the path exceeds the indifference return r_B*(g, T, tax rate), which rises with g and falls with remaining holding period T. Also reported: P(locked in), the share of paths where the CGT, not asset preference, blocks the switch | no-tax, tax-neutral switching certainty equivalent | basis points; share of paths | remaining holding period T, one life |
| Summary form | p10_mean_p90 over return paths, by embedded-gain band | | | |

- **Inputs needed:**
  - Returns of the two assets: I-D1a to I-D1d give one aggregate series and the component returns (equity, housing, bonds) in the D1 note; the spread between A and B is **MISSING.** Research request: a dated pair of UK real return series for the asset a payer holds and the asset they would switch to, with the cross-correlation.
  - CGT rate and base: I-M6h, I-M6k, I-M6j (CGT paid, concentration of gains). The statutory rates are not an inputs row: **MISSING.** Research request: current CGT rates by asset class and band, annual exempt amount, and the no-uplift-at-death rule.
  - Embedded gain ratio g by wealth band: **MISSING.** Research request: unrealised gains as a share of asset value by wealth band (HMRC, Bank of England or ONS wealth by asset class). The old papers held g at 50% for the reference case.
  - Holding period T and realisation rates by band: **MISSING.** Research request: HMRC realisation and holding-period data for gains by asset class.
  - Risk aversion gamma: **MISSING** (as OW1).
- **`outputs.yml` line to add:**
  `  - {id: OW2,  metric: MW2, title: "CGT lock-in welfare cost", summary: p10_mean_p90, by: [embedded_gain_band, holding_period], element: [S6], kind: comparison}`

## 3. OW3: contribution envelope binding (concentration shared with OH1a)

- **Proposed id:** OW3 (metric MW3), with concentration as the alias OW3b = OH1a. One definition per metric: concentration (top 1% share, with and without the WDT) is defined once under OH1a in the H1 brief; OW3 does not define a second. Claim a spoke may make: "In X% of paths and for Y% of payers the lifetime contribution envelope binds, and it binds first for entrants whose first year is a loss year" (S6-B; the entry-margin point of WFR 4.2.3 for S12).
- **Metric row:**

| ID | Name | Definition | Denominator | Unit | Horizon |
|---|---|---|---|---|---|
| MW3a | Envelope binding | Slack_i,t = cumulative net tax paid by payer i to year t minus cumulative refunds received. The envelope binds in year t when a refund due exceeds slack (refund capped at slack). Reported: (1) share of payers for whom it binds at least once; (2) the first year it binds; (3) refunds foregone because of the cap as a share of refunds due; (4) the same by entry year and by return tier of the payer | payers; refunds due | % of payers; year; % of refunds due | transition, short and long |
| MW3b | Aggregate liquidity timing of the cap | The initial-cohort refund exposure at the short reserve: refunds the SRR would owe in the first N years if the cap did not exist, minus refunds with it, as a share of GDP | GDP_t | % of GDP | transition |
| Summary form | p10_mean_p90 over return paths | | | | |

- **Inputs needed:**
  - Loss-year frequency and runs (opening-year loss is the binding case): I-D1c, I-D1d.
  - Wealth distribution and payer count: I-D4a to I-D4c.
  - Persistent return heterogeneity by wealth tier (the Fagereng premise, used for the "tier" split): **MISSING.** Research request: the UK or Norwegian estimate of return differentials by wealth percentile and their persistence (rank autocorrelation over 10 years), with a low, central and high. The old papers took 8 percentage points between the outer tiers, against Fagereng's published 18 point P10 to P90 gap.
  - Reserve targets for MW3b: I-D8 rows (D8 reserve rule).
  - No other new input: the cap is a rule in the tax, not a parameter.
- **`outputs.yml` line to add:**
  `  - {id: OW3,  metric: MW3, title: "Contribution envelope binding", summary: p10_mean_p90, by: [return_tier, entry_year], lines: [MW3a, MW3b], element: [S6, S12], kind: path}`
  Concentration needs no separate line: it is OH1a (`element` on that line gains S6).

## 4. What each needs from the v3 state

| Output | Needs from the v3 run | Available from payer paths? |
|---|---|---|
| OW1 | Per-payer return path for N = 30 years; per-payer wealth and tax paid under each comparator system on the same path | Yes, if the run keeps payer-level paths and the comparators of M5 and M6 are run on those paths. The CEW is a transform of terminal wealth, done after the run. Needs gamma and a revenue-equivalence solver per comparator |
| OW2 | The above, plus a second asset return, an embedded-gain state per payer and a switching decision | **No.** Payer wealth paths carry one aggregate return. See section 5 |
| OW3a | Per-payer cumulative tax and cumulative refund ledger; the refund cap already in M1a | Yes: the cap is part of M1a, so the ledger exists. Needs entry-year tracking |
| OW3a by tier | A persistent idiosyncratic return component per payer | Only if the v3 payer paths carry one. Not in D1, which is one aggregate series |
| OW3b | Reserve rule and refund path | Yes, from P1 and M1c machinery |

## 5. What cannot be produced without a second model

1. **OW2 needs an agent-level decision module.** The lock-in cost compares two assets and a realisation choice. v3 payer paths have one return series, no asset choice and no embedded-gain state. Either (a) v3 carries two asset classes per payer (equity and housing, say, from the D1 component series) and an embedded-gain state, which is an extension of the run, or (b) OW2 is a post-processing module over the v3 paths that adds the two-asset choice. Neither is a separate paper model: both use v3's draws and are written into the same run. The guru or code lane must pick (a) or (b); option (b) is cheaper and is the one this brief assumes.
2. **OW1 by return tier and OW3a by tier** need persistent return heterogeneity per payer, which D1 does not provide. Without the MISSING input above, these two splits cannot be produced and the by-tier cuts fall away; the overall and by-wealth-band cuts remain.
3. **Out of scope of OW1 (FAL H4):** valuation friction, avoidance cost, administrative cost and migration are not welfare terms in OW1. The behavioural response (I-D5a to I-D5d) shrinks the base for all systems alike. H4 as FAL states it (falsified if the WDT's distortion is higher once those costs are restored) needs a cost-side output the v3 manifest does not have. The nearest are OS1 and O7. Flagged for the author: OW1 supports H4 only on the controlled part, as the old paper did.
4. **Concentration:** defined once as OH1a; it needs the heterogeneous-returns state of item 2 as well.

## 6. Questions for the author (not guessed)
1. Is the consumption tax staying as a comparator? It drives one MISSING input and the old model found it equal to the stock wealth tax.
2. Option (a) or (b) for OW2 (section 5, item 1)?
3. Confirm that OW3 holds the envelope only and concentration stays as OH1a, as the ledger says, instead of the brief's wording "OW3 contribution envelope binding and concentration".
4. Gamma: one value with a tornado, or a range sampled at level 2?
