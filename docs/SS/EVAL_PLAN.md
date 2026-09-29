# EVAL: Break-Even Welfare Analysis — Planning Document

**Status:** Pre-development planning  
**Authors:** K. Ogata / Claude (research and planning session, 28 September 2026)  
**Purpose:** This document records the full research and planning conversation that preceded development of the EVAL model. It is the single reference point for model design decisions, source provenance, data requirements, and open questions before a line of code is written.

---

## 1. What EVAL Is

WFR establishes a pre-behavioural welfare baseline showing that the WDT eliminates 141–143 basis points of welfare cost that CGT imposes through realisation lock-in. WFR cannot say whether the prospective implementation costs of the WDT exceed that advantage, because those costs are unquantifiable without implementation data.

EVAL's job is to make that uncertainty tractable through break-even analysis: for each Category 3 prospective cost, what magnitude would it need to reach to wipe out the welfare advantage WFR has measured? If a break-even threshold is empirically implausible, that cost cannot explain away the welfare advantage. If it falls within a plausible empirical range, that is a genuine open question for Phase One.

EVAL is explicitly a *Level 1* analytical contribution. It does not calibrate behavioural responses from empirical data. It does not produce a single expected welfare estimate. It characterises the space within which the WDT's welfare case could be reversed, and assesses whether each reversal scenario is plausible.

### 1.1 Two Frames, One Model

EVAL serves two distinct audiences who need the same underlying analysis presented differently.

**Per-taxpayer frame.** Answers: "As a wealthy individual, is it worth cooperating with the WDT versus optimising within the current system?" This is the frame relevant to a wealthy sceptic deciding whether to engage with the mechanism or restructure around it. Inputs: individual wealth trajectory, growth tier, declaration behaviour, CGT effective rate under optimal current-law structuring.

**Aggregate fiscal frame.** Answers: "Does the arithmetic hold for the Treasury — does the WDT remain net-positive once all implementation costs are accounted for?" This is the frame relevant to a policy analyst or Treasury official evaluating viability. Inputs: RATES bracket populations, aggregate revenue, Jakobsen elasticities, Agrawal multiplier, admin cost ratios.

The two frames share the same underlying model. The aggregate frame is the per-taxpayer results weighted by the TOML bracket populations (`WDT_Params.toml`, `[[brackets]]`). They should be presented as separate outputs with separate audiences clearly labelled, but computed from the same code.

### 1.2 The Five Category 3 Costs

WFR §6.1.3 names five prospective implementation costs whose magnitudes are currently unknown. EVAL runs break-even analysis on each.

1. **Migration response** — emigration of assessed taxpayers and associated cross-base revenue loss
2. **Intensive margin avoidance** — restructuring, income shifting, basis manipulation (BEHAV Shapes 4–6)
3. **Valuation friction** — compliance costs under the four-route architecture, primarily Route D professional and auction costs
4. **Administrative learning dynamics** — cost of the institutional learning period before HMRC-equivalent operational competence is reached
5. **Novel avoidance strategies specific to the symmetric refund** — engineered losses, coordinated refund timing

Each cost is addressed in Section 4 with the available empirical anchors and the implied break-even threshold.

---

## 2. The Welfare Baseline and Its Problems

### 2.1 What WFR Establishes

The WFR model compares six tax systems at E[T] = 2% of W₀ using certainty-equivalent welfare (CEW) against a no-tax benchmark. The key result is that CGT with endogenous portfolio choice (realisation lock-in admitted) imposes 141–143 bp of welfare cost relative to the WDT at the reference calibration:

- G/V = 50% (embedded gain ratio)
- T = 5 years (remaining holding period in WFR's model)
- τ_cgt = 24% (UK higher rate as of October 2024 Budget)
- r_A = 10.45% (JST UK equity mean 1947–2019)
- γ = 2 (CRRA risk aversion, Flavin-Yamashita 2002)
- Ver. A distribution (73-observation UK historical equity sequence)

At T ≥ 8 the lock-in cost plateaus at 181 bp (realisation-induced portfolio persistence — the agent has been locked into a suboptimal allocation whose compounding cost continues accumulating). This plateau applies throughout the N = 30 canonical horizon.

### 2.2 Why the WFR Baseline Is an Understatement

The 141–143 bp figure is described in planning as "best case WDT vs worst case CGT." Two reasons it understates the advantage.

**First, the CGT comparator uses the headline rate.** The actual effective CGT rate for the WDT-taxable population is materially lower than 24%. Advani and Summers (2023), using anonymised HMRC administrative data on all UK taxpayers, find that the average rate of tax paid by people who received one million pounds in taxable income and gains was 35% — the same as someone earning £100,000. A quarter of those in the top 1% pay at least 9 percentage points below the headline rate on total remuneration. The mechanism is not primarily tax reliefs but income composition: gains are taxed at 20–24% rather than 45% income tax + 2% NICs.

For the WDT's primary population (W₀ ≈ £1.63m–£20m, Good tier), the realistic effective CGT rate on business asset gains is:

| Structure | Effective CGT rate | Notes |
|---|---|---|
| Headline (higher rate) | 24% | WFR assumption |
| BADR (business assets, ≤£1m lifetime) | 14% (2025/26), 18% (2026/27) | Phased increase from 10% |
| EOT structure (Employee Ownership Trust) | 12% | 50% of gains exempt, unlimited |
| Deferral to death + step-up | 0% | Death forgives embedded gain entirely |
| Non-dom / offshore structure | ~0–10% | Legally available but increasingly constrained post-2025 |

The honest comparator for EVAL is the WDT against the *optimally structured current system*, which for a sufficiently advised taxpayer approaches 0–12% effective on gains. As stated in planning: "a sufficiently resourced taxpayer can make the legal case they owe 0 tax — the entire problem I am trying to solve with this." This means the WFR 141 bp figure is a floor on the welfare advantage, not a ceiling.

**Second, the T = 5 calibration understates lock-in at N = 30.** WFR's model uses a fixed remaining holding period T. At T ≥ 8 the lock-in cost plateaus at 181 bp due to realisation-induced portfolio persistence. For a taxpayer at N = 30, who has held an appreciating position for 30 years, the embedded gain ratio G/V approaches 90%+ and the lock-in cost approaches 162 bp at the WFR Table 4.2.2b upper end. The N = 30 comparison is harder on CGT, not easier.

**The death step-up is the dominant structural difference at N = 30.** Under current CGT, death forgives the entire embedded capital gain — heirs inherit at probate value with no CGT charge on the deceased's lifetime appreciation. This is the main reason CGT is so attractive to long-horizon holders: the optimal strategy under CGT is to hold until death, realise nothing, and pass the step-up to heirs. At N = 30, a WDT taxpayer approaching death faces an inheritance auction that fires the Route D mechanism; a CGT taxpayer faces a step-up that eliminates the liability entirely. The N = 30 CGT model must incorporate this death probability and the value of the step-up as a CGT benefit.

### 2.3 The N = 30 CGT Model EVAL Must Build

WFR's lock-in model is a static two-asset switching model at fixed T. EVAL needs a proper dynamic N-period CGT model. The key references are:

**Dammon, Spatt, and Zhang (2001), Review of Financial Studies 14(3): 583–616.** The foundational dynamic model of optimal consumption and portfolio choice with capital gains taxes. Key finding: the incentive to rediversify is inversely related to the size of the embedded gain and investor's age. Optimal equity holding increases well into an investor's lifetime because of death step-up. This establishes the theoretical structure EVAL's CGT counterfactual must replicate.

**Jensen and Marekwica (2013), Journal of Dynamics and Control.** Life-cycle model with unspanned labour income and realisation-based CGT. Key finding: for realistic parameterisations, certainty-equivalent welfare gains from fully tax-optimised portfolio decisions are less than 2% of present financial wealth and lifetime income compared to a heuristic portfolio policy ignoring CGT. Compared to a policy that only ignores the *realisation-based feature* and assumes mark-to-market instead, these gains are less than **0.5%** of financial wealth and lifetime income.

This 0.5% figure is the most directly relevant empirical result for the N = 30 lock-in question — but it requires three critical adjustments for the WDT population:

1. Jensen-Marekwica model a typical investor with labour income. For W₀ = £20m with no material labour income remaining (the WDT population at age 60+), the denominator of "financial wealth + lifetime human capital" shrinks dramatically, so the 0.5% figure as a fraction of *financial wealth alone* rises substantially.
2. Their model includes the death step-up, which is the primary driver of why the welfare cost is low. EVAL's CGT comparator must price the step-up explicitly, since removing it (via the WDT's inheritance auction) is a structural difference between the systems.
3. The 0.5% figure is against mark-to-market taxation in general, not specifically against the WDT's delta base with symmetric refund. The refund in loss years is a materially different welfare property not present in any system Jensen-Marekwica model.

**Agersnap and Zidar (2021), AER: Insights 3(4): 399–416.** The Tax Elasticity of Capital Gains and Revenue-Maximizing Rates. Uses state-level panel data 1980–2016 with a direct-projections approach over a 10-year horizon. Key for EVAL: the long-run elasticity of capital gains realizations with respect to the tax rate is substantially larger than the short-run elasticity — the lock-in effect builds over time, consistent with the WFR plateau finding.

**EVAL's approach to the N = 30 CGT model.** Given the complexity of a full dynamic optimisation model, EVAL will use the following approach:

- Build a discrete-time N-period simulation where the agent holds an asset growing at the Good-tier return (+11.4%/year) starting from W₀
- At each period, the agent decides whether to realise (paying CGT at the effective rate) or defer
- At death (proxied by a death probability at each age, based on UK ONS life tables), the step-up eliminates the liability
- The welfare cost of CGT relative to WDT is the CEW difference over the full N-period path
- Parameters are swept across effective CGT rates (24%, 18%, 14%, 12%, 0%) and death probabilities

---

## 3. Reference Taxpayer

### 3.1 The Primary Reference Cell

The revenue concentration table (from RATES simulation, population-weighted) identifies the single cell contributing most revenue as a share of total WDT revenue:

| Tier (weight) | 95th percentile bracket | Revenue share |
|---|---|---|
| Good (+0.95pp, 40% of taxpayers) | W₀ ≈ £1.63m | **11.7%** |

This cell — Good tier, 95th percentile bracket — contributes 11.7% of total WDT revenue from a single cohort in a 40-cell grid. It is the highest single cell in the distribution. EVAL uses this as the primary reference taxpayer.

**Reference taxpayer parameters:**
- W₀ = £1.629m (95th percentile entry wealth, TOML `brackets.V0_m`)
- Growth tier: Good (+0.95pp above hist_mean = 10.45%, implied return ≈ 11.4%/year)
- Canonical horizon: N = 30 years
- Terminal wealth: ~£19.7m (pre-settlement, RATES Table §2, Good tier, 95th percentile ≈ £19.72m)
- WDT revenue-weighted annual burden: 0.35% of net worth (RATES §2)
- Effective lifetime rate on gains: ~15.1% (RATES Table §2, Good tier, 95th percentile)

### 3.2 Secondary Reference Cases

Three secondary cases cover the key comparisons.

**Ultra-HNWI case (Great tier, 99.9%+).** W₀ ≈ £19.85m, return ≈ 13.9%/year, terminal wealth ~£274m. This is the taxpayer for whom the CGT death step-up is most valuable (£274m in unrealised gains), and for whom the WDT inheritance auction is most material. CGT lock-in welfare cost at G/V ≈ 95% approaches the WFR 162 bp upper bound.

**Below-threshold case (Poor tier, 90th percentile).** W₀ ≈ £1.629m, return ≈ 5.9%/year. Near-zero WDT burden (0.12% annual wealth burden, RATES Table §2). The symmetric refund is most material here — the Poor tier spends the most years in negative-return states, and the refund protection asymmetry (WFR §4.3.3) gives WDT a 38.1 bp welfare advantage over income tax even at low wealth.

**Treasury aggregate case.** Full 40-cell population, weighted by TOML bracket populations and tier weights. Aggregate WDT revenue ≈ £873.6b/year (RATES §7.1, lifetime average N=30). This is the frame for the aggregate fiscal break-even.

---

## 4. Research Findings by Cost Category

### 4.1 Migration Response (Category 3 Cost 1)

**Primary source:** Jakobsen, Jakobsen, Kleven, and Zucman (2024 NBER Working Paper w32153). Uses Danish administrative data with near-universal wealth coverage. The most credible empirical basis for wealth-tax migration elasticities available.

**Key quantitative findings:**
- Semi-elasticity of out-migration with respect to wealth tax rate: **−0.17 percentage points per 1 percentage point increase** in the effective wealth tax rate
- Stock effect: a 1 percentage point increase in the top wealth tax rate decreases the stock of wealthy taxpayers by approximately **2%** in steady state
- Revenue cost of migration: only **0.22 cents lost per dollar raised** through emigration (extensive margin)
- Revenue cost of intensive margin avoidance: **0.54 cents lost per dollar raised** (2.5× the migration cost — intensive margin is the dominant behavioural risk, not emigration)

**The Agrawal et al. (2025) 6× multiplier:** Published in the American Economic Journal: Economic Policy. Documents that wealth-tax-driven migration generates income and VAT losses approximately six times the direct wealth-tax revenue loss. Three critical caveats for EVAL:

1. This is calibrated to *Spanish regional* wealth taxes — Madrid set a zero rate while other regions levied 0.2–3.75%. The mechanism is intra-national mobility to a domestic zero-rate haven, not international emigration. The UK has no domestic zero-rate competitor.
2. The implied emigration rate for the Spanish context is substantially higher than what Jakobsen estimates for international emigration.
3. BEHAV §9.2 explicitly retains the directional warning but flags the magnitude as uncertain for a UK national WDT. A more defensible UK multiplier is likely 2–3×, not 6×.

**WDT-specific adjustments:**

The WDT's revenue-weighted annual burden is 0.35% of net worth (RATES §2). The Jakobsen empirical cases study Swedish/Danish wealth taxes at 0.5–1.5% effective. Applying the Jakobsen semi-elasticity (−0.17 per pp) to the WDT's 0.35% burden:

Expected additional out-migration rate ≈ 0.17 × 0.35 ≈ **0.06 percentage points per year**, on a baseline out-migration rate of approximately 0.2% per year for the top decile. This implies approximately **30% more emigration** than baseline — from 0.2% to 0.26% per year — or about 13–30 additional departures per year from the Phase One population of ~22,000–50,000.

**Break-even threshold:**

For migration to eliminate the 141 bp welfare advantage, the revenue loss through migration and the Agrawal multiplier must equal the welfare gain. At a 2× multiplier (conservative UK estimate) and 0.35% annual burden, the implied emigration rate must reach approximately **12–18% of the assessed population** to threaten the baseline. That is 10–15× the elasticity-implied prediction. Migration, on its own, is unlikely to threaten the welfare advantage.

**Data requirement:** Jakobsen elasticity is already quantified and applicable. What is not available is a UK-specific migration elasticity for wealth taxation. Phase One measurement is the only resolution. For EVAL, use the Jakobsen semi-elasticity as the central estimate and run sensitivity at 2×, 3×, and 5× that elasticity.

---

### 4.2 Intensive Margin Avoidance (Category 3 Cost 2)

**Primary source:** Same Jakobsen et al. (2024) paper. The intensive margin response — avoidance through restructuring, income shifting, and basis manipulation — costs **0.54 cents per dollar raised**, 2.5× the migration cost.

This is the most material quantified threat to the WDT's revenue claim. It covers BEHAV Shapes 4–6: avoidance through restructuring, timing manipulation, and cross-border asset migration without personal exit.

**WDT structural mitigants:**

The WDT's tolerant zone (VAL §7.1, α ≈ 0.8–1.5) absorbs legitimate valuation uncertainty without creating avoidance incentives. The self-balancing mechanism (Route C must-transfer rule, Route D deferral) attaches real consequences to declarations rather than leaving them as unverified estimates. The Jakobsen intensive margin figure is calibrated to conventional wealth taxes with no equivalent self-correction mechanism.

The honest answer is that WDT-specific intensive margin responses cannot be quantified without Phase One data. Two bounding cases are available:

- **Upper bound (conventional wealth tax analogy):** Apply Jakobsen's 0.54 cents/dollar directly. This is conservative-pessimistic — it ignores WDT's structural mitigants entirely.
- **Lower bound (WDT design intent):** The tolerant zone and must-transfer rule substantially reduce the avoidance surface relative to conventional wealth taxes. A reasonable lower bound is 0.1–0.2 cents/dollar based on the structural reduction in avoidance opportunity.

**Break-even threshold:**

At 0.54 cents/dollar (upper bound), a WDT collecting £874b/year loses approximately £471b/year to intensive margin responses — leaving net revenue of ~£403b, still substantial relative to the fiscal target. The welfare break-even question is different: the welfare advantage is 141 bp per taxpayer; intensive margin avoidance reduces declared deltas (and therefore tax paid), which reduces the revenue to the WDT but also reduces the welfare cost to the avoider. The net welfare effect depends on whether avoidance is welfare-improving or welfare-destroying for the avoider — BEHAV Shapes 4–6 typically involve real costs (professional fees, restructuring friction, suboptimal business structures) that are themselves welfare-reducing. This is an underdeveloped area of the analysis that EVAL should flag as a Phase One empirical question.

**Data requirement:** No UK-specific WDT intensive margin elasticity exists. Use Jakobsen 0.54 as the upper bound, WDT structural argument as the lower bound, and present the range explicitly. The measurement agenda in PHASE1 §5.2 (avoidance shape distribution) is the resolution path.

---

### 4.3 Valuation Friction and Route D Costs (Category 3 Cost 3)

**Primary sources:**

Burgherr (2021), in the Wealth Tax Commission evidence base: *Costs of Administering a Wealth Tax*. The most directly applicable UK-specific estimate.

| | Lower bound | Central estimate | Upper bound |
|---|---|---|---|
| Taxpayer compliance cost | 0.05% of taxable wealth | **0.1% of taxable wealth** | 0.3% of taxable wealth |
| Government administration cost | 0.01% of taxable wealth | **0.05% of taxable wealth** | 0.1% of taxable wealth |
| **Total** | **0.06%** | **0.15%** | **0.4%** |

These figures are for a *conventional* annual wealth tax requiring annual professional valuations of all assets. The WDT's route architecture changes the cost profile substantially:

- Routes A and B (estimated 60–85% of WDT-taxable wealth by volume): competitive tender professional valuation. Cost comparable to conventional wealth tax but competitively priced rather than client-appointed. The competitive tender is expected to reduce fees relative to Burgherr's central estimate.
- Route C (estimated 5–10%): self-declaration with no professional fee. Zero valuation cost to taxpayer.
- Route D (estimated 10–20%): no annual valuation cost. Cost events are hard resets and the inheritance auction only.

**WDT-adjusted compliance cost estimate:** Central case approximately 0.03–0.07% of taxable wealth, against Burgherr's 0.1% for a conventional wealth tax. At taxable wealth of approximately £220bn+ for the £10m+ population, this implies £66m–£154m per year in taxpayer compliance costs.

**Route D auction cost data (to be fetched):** Christie's and Sotheby's publish buyer's premium schedules. Private M&A process costs for UK mid-market transactions (the closer analogue for private company equity) typically run 2–4% of enterprise value for a formal process. At N = 30, a Route D taxpayer incurs:
- One mandatory inheritance auction (automatic on transfer)
- Zero to two voluntary hard resets over 30 years

The cost is event-based and low in annual terms. Even at 3% of a £20m Route D asset, the hard reset costs £600k — bounded and one-off, not annual.

**Break-even threshold:**

141 bp of CEW at W₀ = £1.63m over 30 years ≈ £141,000 per taxpayer in consumption-equivalent welfare over the horizon, or approximately £4,700/year. The Burgherr WDT-adjusted central estimate of 0.05% of taxable wealth (≈ £815/year at W₀ = £1.63m) is well below that threshold. The Burgherr upper bound at 0.07% (≈ £1,140/year) is also below threshold. Compliance cost is unlikely on its own to eliminate the welfare advantage — though it narrows it.

At the 95th percentile Good-tier reference taxpayer's terminal wealth of £19.72m, the Burgherr upper bound (0.3% of taxable wealth) would imply £59,160/year — which approaches the £4,700/year break-even. However, this figure is for a conventional wealth tax requiring full annual professional valuation of all assets. Under the WDT route architecture, this taxpayer's listed equities (Route A) have zero valuation cost; only the illiquid fraction (Route D/B) bears professional fees. The realistic per-taxpayer cost is substantially lower.

**Data requirement:** Auction cost schedules for UK private asset auctions (property, private company equity, high-value personal property). These are publicly available from Christie's, Sotheby's, and RICS. For M&A process costs, use published mid-market M&A fee surveys (Grant Thornton, KPMG, etc.). This data is not yet fetched and should be obtained before finalising Module 4.

---

### 4.4 Administrative Learning Dynamics (Category 3 Cost 4)

**Available data:** No direct empirical analogue for WDT-specific administrative learning curves exists. The most relevant comparators are:

- HMRC's IR35 and loan charge episodes (cited in JUR §1.5.1): examples of HMRC failing on complex new instruments when rollout is rushed or underfunded. Not quantified in public sources.
- French Impôt de Solidarité sur la Fortune (ISF) administrative cost: Burgherr (2021) cites approximately 2.07% of ISF revenue in government administration costs, against the WTC's projected 0.03% for the UK version at the £10m threshold.
- WTC estimate for UK annual wealth tax at £10m threshold: government ongoing cost £3m/year for 22,000 taxpayers. This is already very low relative to revenue.

**Hypothesis (from planning conversation):** The WDT is likely a net administrative saver relative to the combined CGT + IHT system. The structural argument:

- Valuation disputes that currently exist under CGT/IHT cannot exist under Routes C and D. Under CGT, every valuation dispute involves determining the correct market value. Under Route D, the declared value *is* the operative value. There is no "correct value" for the state to argue against.
- Under Route A/B, disputes concern valuator methodology, not asset value per se, and are resolved by the two-stage review process with defined outcomes.
- The current CGT and IHT systems require HMRC to adjudicate open-ended valuation questions; the WDT system shifts that burden to the taxpayer and allows it to compound into future deltas rather than requiring immediate resolution.

**Benchmark data:**

| System | Admin cost per £1 of revenue | Source |
|---|---|---|
| HMRC system-wide | 0.51p | NAO 2025 |
| HMRC Self Assessment (CGT is Self Assessment) | 2.14p | NAO 2025 |
| HMRC IHT | ~0.66p (£35m admin / £5.3bn revenue) | HMRC Annual Report |
| WTC UK annual wealth tax at £10m threshold | ~0.03p (£3m ongoing / ~£10bn projected revenue) | Burgherr 2021 / WTC |
| French ISF | ~2.07% of revenue | Burgherr 2021 |

The WTC figure suggests that at the WDT's operating scale (revenue concentrated in a small, high-value population), admin costs per £1 of revenue are likely *lower* than any comparable existing instrument.

**Treatment in EVAL:** Administrative learning dynamics are best handled as a *political risk scenario* rather than a direct welfare cost. A poorly implemented Phase One could trigger repeal before welfare gains compound — this is the POL §6 bootstrapping vulnerability. In the welfare model, this translates to a probability-weighted discount on the WDT's long-horizon welfare advantage: if Phase One failure leads to repeal at year 5, the taxpayer receives 5 years of WDT welfare advantage instead of 30. The welfare cost is the present value of the forgone years.

EVAL should present this as a scenario ("probability of Phase One failure = X% implies Y% reduction in expected welfare advantage") rather than a point estimate. The probability of Phase One failure is itself unquantifiable before implementation.

**Data requirement:** HMRC IHT administration cost breakdown (published in HMRC Annual Report, publicly available). Route D auction cost data (see above). No additional empirical data is available for the learning curve itself; treat as a scenario parameter.

---

### 4.5 Novel Avoidance Strategies Specific to the Symmetric Refund (Category 3 Cost 5)

**Structural analysis:** The symmetric refund creates a potential exploitation surface — if taxpayers can engineer declared losses to maximise refund claims, the SRR faces transient liquidity demand above its normal sizing. Three structural constraints bound this risk.

First, the lifetime contribution envelope caps each taxpayer's refund entitlement at cumulative prior contributions. The mechanism cannot return more than it has collected from any individual. A taxpayer who engineers a large loss in year 1 (before accumulating a contribution history) receives zero refund.

Second, the SRR is sized against realistic refund exposure derived from the historical return series, not against the theoretical maximum of simultaneous full-envelope drawdown. The 3× capitalisation ratio is confirmed by the SWEEPS.A sweep as appropriate against the historical worst-case scenario.

Third, coordinating a population-level timing event requires thousands of taxpayers and their professional advisers to simultaneously engineer large declared losses in the same assessment year — a coordination problem visible to the Administrator through the route distribution and declared value records.

**Quantitative assessment:** This cost category is the *least likely* of the five to threaten the aggregate welfare advantage. It is architecturally bounded in a way the other four are not. The one scenario where it poses real risk — coordinated mass refund timing — is treated in RATES §7.4 as bounded by the envelope cap and the SRR's reserve sizing.

**Treatment in EVAL:** Include as a sensitivity scenario with a parameter for the fraction of the taxable population that successfully engineers simultaneous loss recognition. Show that the break-even (the fraction required to exhaust the 141 bp advantage) is implausibly high given the coordination barriers. This is a confirmatory analysis, not a primary risk.

**Data requirement:** None additional. The RATES simulation infrastructure already models this implicitly through the SRR stress scenarios. EVAL can inherit those results directly.

---

## 5. Model Architecture

### 5.1 Overview

EVAL is four modules sharing a common return series and parameter set. The return series is the JST UK equity capital total return data (1947–2019, 73 observations) from `WDT_Params.toml`. Rate function parameters are the Balanced scenario canonical values (τ₀ = 15%, τ_m = 70%, k = 0.001, W_min = £2m).

**Module 1: Welfare baseline at N = 30**  
Rebuilds the WDT-vs-CGT welfare comparison at N = 30 using a proper dynamic CGT simulation. This is new modelling, not inherited from WFR (which uses T = 5). Outputs: CEW by system at N = 30 across effective CGT rate scenarios and death probability scenarios.

**Module 2: Per-taxpayer break-even**  
For each of the five cost categories, solves for the cost magnitude that exactly offsets the N = 30 welfare advantage. Runs across the four tiers (Poor/Ok/Good/Great) and the key wealth brackets. Output: "cost X must exceed £Y/year to eliminate the welfare advantage for a [tier] taxpayer at [bracket]."

**Module 3: Aggregate fiscal break-even**  
Weights per-taxpayer results by TOML bracket populations. Adds migration response using Jakobsen elasticities and Agrawal multiplier (2×, 4×, 6× sensitivity). Adds admin cost comparison. Output: fiscal viability assessment with break-even thresholds for the aggregate revenue claim.

**Module 4: Admin cost comparison**  
Standalone comparison of CGT + IHT admin costs per £1 of revenue against projected WDT admin costs per £1, split by route. Output: whether WDT is a net admin saver and under what assumptions.

### 5.2 Module 1 — Dynamic CGT Model Design

The N = 30 CGT counterfactual cannot use WFR's static lock-in model. The required model:

**State variables:** (t, W_t, B_t) where t is the year in the system, W_t is current wealth, and B_t is the recognised CGT basis.

**Each period:**
1. Wealth grows at the Good-tier return (hist_mean + 0.0095 = 11.4%/year) plus the JST historical sequence for that simulation year
2. Agent chooses whether to realise the embedded gain W_t − B_t:
   - If realise: pay CGT at effective rate τ_cgt on (W_t − B_t); new basis B_t = W_t
   - If defer: no tax; basis unchanged; embedded gain compounds
3. Death probability at each year from ONS England life tables (starting age 60, N=30 to age 90)
4. At death: step-up eliminates embedded gain (no CGT on (W_death − B_t)); heir inherits at W_death

**The WDT counterfactual (comparator):**
1. Annual delta computed as W_t − W_{t-1}
2. WDT applied at logistic rate function τ(W_t) on positive deltas
3. Symmetric refund at τ(W_t) on negative deltas, subject to lifetime contribution envelope
4. No step-up at death: inheritance auction at Route D (for the non-fungible fraction) or Route A/B at market value

**Output:** CEW difference (WDT − CGT) across the N = 30 path. Negative = WDT is better. Sweep across:
- Effective CGT rate: 24%, 18%, 14%, 12%, 0% (optimal structuring scenarios)
- Death probability: ONS central estimate, 50% of central estimate, zero (ignore death, upper bound on lock-in)
- G/V profile: computed endogenously from the growth path, not fixed at 50%

This approach is consistent with the Dammon-Spatt-Zhang (2001) framework and incorporates the key finding that the death step-up is the dominant feature distinguishing long-horizon CGT from accrual taxation.

### 5.3 Module 2 — Per-Taxpayer Break-Even

For each cost category, compute:

**Break-even cost (£/year) = (141 bp × W₀) / 30 years** as the annual welfare equivalent, then express as a fraction of W₀ for comparability.

At the reference taxpayer (W₀ = £1.629m, N = 30, 141 bp baseline):
- 141 bp × £1.629m = £22,969 lifetime welfare equivalent
- ÷ 30 years = **£766/year** break-even in annualised welfare terms

At terminal wealth (W_terminal ≈ £19.72m, Good tier, 95th percentile after 30 years):
- The burden figures shift to terminal wealth basis: **0.41% × £19.72m = £80,852/year** in terminal-wealth-equivalent terms (revenue-weighted burden at Good tier, 95th percentile from RATES Table §2)

Compare each cost category against both benchmarks and assess plausibility.

### 5.4 Module 3 — Aggregate Fiscal Break-Even

**Migration:**
- Apply Jakobsen semi-elasticity (−0.17 pp per 1pp effective rate) to WDT burden (0.35%)
- Implied annual emigration rate increase: 0.17 × 0.35 = 0.06 pp
- Apply Agrawal multiplier (2×, 4×, 6× sensitivity) for cross-base revenue loss
- Compare to WDT lifetime average revenue (£873.6b/year, RATES §7.1)
- Break-even: what emigration rate makes net revenue negative

**Intensive margin:**
- Apply Jakobsen intensive margin coefficient (0.54 cents/dollar)
- Compare WDT-adjusted estimate (0.1–0.2 cents/dollar based on structural mitigants)
- Show net revenue under both scenarios

**Admin costs:**
- Current system: CGT Self Assessment cost (2.14p per £1) × CGT receipts (~£13.7b) = £293m; IHT admin (~£35m); total ~£328m for the population the WDT would cover
- WDT projected: WTC central estimate (£3m/year at £10m threshold) scaled to WDT's operating range
- Net: WDT almost certainly cheaper; show the margin of safety

### 5.5 Inputs Required from Existing WDT Model

The following can be imported directly from existing model infrastructure:

| Input | Source | Parameter name |
|---|---|---|
| UK equity return series | WDT_Params.toml | `returns.values` (73 observations) |
| Wealth bracket populations | WDT_Params.toml | `brackets.N_pop` |
| Bracket starting wealth | WDT_Params.toml | `brackets.V0_m` |
| Growth tier differentials | WDT_Params.toml | `tiers.differential` |
| Rate function parameters | WDT_Params.toml | `rate.tau_0`, `rate.tau_m`, `rate.k`, `rate.W_min` |
| Budget base and growth | WDT_Params.toml | `budget.budget_base`, `budget.budget_growth` |
| Historical mean return | WDT_Params.toml | `tcm.hist_mean` (10.45%) |
| Canonical horizon | WDT_Params.toml | `tcm.canonical_N` (30) |
| WDT lifetime average revenue | RATES §7.1 | £873.6b/year (Good + Great tier combined: £791.5b) |
| Terminal wealth by tier/bracket | RATES Table §2 | Full 40-cell matrix |
| Annual wealth burden by tier/bracket | RATES Table §2 | Full 40-cell matrix |

### 5.6 External Data Requirements

The following must be sourced before Module 1 and Module 4 can be finalised.

**HIGH PRIORITY — needed for Module 1:**

| Data item | Source | Status | Notes |
|---|---|---|---|
| UK ONS life tables (England, starting age 60) | ONS.gov.uk, National Life Tables | Not yet fetched | Need annual probability of death by age for N=30 horizon from age 60 |
| UK effective CGT rates by income/wealth decile | Advani-Summers (2023) Oxford Review of Economic Policy 39(3): 406-xxx; also HMRC CGT statistical tables | Partially confirmed | Key finding: average rate at £1m income/gains = 35%; headline rate = 24%; effective rate for optimally structured taxpayer ≈ 10–15%. Need the full distribution |

**HIGH PRIORITY — needed for Module 3:**

| Data item | Source | Status | Notes |
|---|---|---|---|
| Jakobsen et al. (2024) semi-elasticity | NBER Working Paper w32153 | ✅ Confirmed | −0.17 pp emigration per 1pp tax rate increase; 0.54 cents intensive margin per dollar raised |
| Agrawal et al. (2025) 6× multiplier details | AEJ: Economic Policy | ✅ Confirmed with caveats | Spanish regional context; UK multiplier likely 2–3×; fetch paper for exact specification |
| HMRC IHT admin cost | HMRC Annual Report and Accounts 2023-24 | Partially confirmed | Total IHT receipts ~£5.3b; admin cost estimated ~£35m (0.66p per £1); need exact figure |
| HMRC CGT admin cost | NAO (2025) Administrative Cost of the Tax System | ✅ Confirmed | Self Assessment (CGT is SA): 2.14p per £1; system-wide 0.51p per £1 |

**MEDIUM PRIORITY — needed for Module 4:**

| Data item | Source | Status | Notes |
|---|---|---|---|
| Route D auction cost schedules | Christie's, Sotheby's, RICS | Not yet fetched | Need buyer's premium + seller's commission as % of asset value, by asset class |
| UK M&A process costs for mid-market private companies | Grant Thornton / KPMG M&A fee surveys, or BDO published data | Not yet fetched | Need total advisory cost as % of enterprise value for £5m–£100m transactions |
| WTC admin cost evidence base (Burgherr 2021 full paper) | WTC website / warwick.ac.uk | ✅ Confirmed (central estimate) | Central estimate: 0.1% taxable wealth taxpayer cost; 0.05% government cost; WDT-adjusted ~0.03–0.07% |

**LOWER PRIORITY — to be incorporated if available:**

| Data item | Source | Status | Notes |
|---|---|---|---|
| UK ONS WAS 2020-22 (latest available) | ONS | Available but degraded | WAS lost Official Statistics accreditation June 2025; use with caveats as per JUR §1.2.1 |
| French ISF admin cost data | Burgherr (2021) | ✅ Confirmed | 2.07% of ISF revenue; contrast against WTC estimate |
| Dammon-Spatt-Zhang (2001) full paper | RFS 14(3): 583–616 | Located, not fetched | Need the welfare cost quantification and the death step-up treatment |
| Jensen-Marekwica (2013) full paper | J. Economic Dynamics and Control | Located, not fetched | Key result: <0.5% of financial wealth + human capital for typical investor |

---

## 6. Key Analytical Findings from Research

### 6.1 The 141 bp Baseline Is a Floor

The WFR baseline of 141 bp is computed against the 24% headline CGT rate at T = 5. Three reasons it understates the true welfare advantage:

1. **Effective rate for the WDT population is 10–24%, not 24%.** Advani-Summers (2023) establish that EATRs decline at the top of the distribution. BADR, EOT structures, and deferral-to-death reduce the realistic effective rate to 10–18% for optimally structured business asset disposals.

2. **The T = 5 calibration understates lock-in at N = 30.** WFR's lock-in cost plateaus at 181 bp from T = 8 onward. At N = 30, the embedded gain ratio G/V reaches ~90%, and WFR Table 4.2.2b shows lock-in costs approaching 162 bp at G/V = 77%. The N = 30 CGT comparison is harder on CGT, not easier.

3. **Death step-up eliminates CGT but not WDT at N = 30.** The most valuable feature of CGT for a long-horizon wealthy holder is the basis step-up at death: heirs inherit at probate value, the embedded lifetime gain is never taxed. The WDT's inheritance auction fires at death, eliminating this benefit. EVAL's N = 30 model must price this structural difference explicitly.

The honest framing for EVAL: **the question is not whether the WDT's welfare advantage survives Category 3 costs; it is how large those costs would need to be to eliminate an advantage that is substantially larger than WFR's 141 bp baseline suggests.**

### 6.2 Intensive Margin Avoidance Is the Dominant Risk

Of the five cost categories, intensive margin avoidance is the most material empirical threat. The Jakobsen semi-elasticity gives:

- Migration (extensive margin): 0.22 cents per dollar raised
- Avoidance/restructuring (intensive margin): 0.54 cents per dollar raised

The WDT's tolerant zone (α ≈ 0.8–1.5) and self-balancing mechanisms are specifically designed to reduce the intensive margin response relative to conventional wealth taxes. The honest position is that WDT-specific intensive margin responses cannot be quantified before Phase One.

EVAL's contribution is to characterise the break-even: the intensive margin response would need to reach approximately **0.8–0.9 cents per dollar raised** to eliminate the welfare advantage (above the Jakobsen upper bound of 0.54). This is an empirically useful result even without precise WDT-specific estimates.

### 6.3 Migration Is Unlikely to Be the Critical Threat

At the WDT's 0.35% revenue-weighted annual burden, the implied annual emigration rate increase is 0.06 percentage points above a 0.2% baseline. Break-even requires approximately 12–18% of the assessed population to emigrate — 10–15× the elasticity-implied prediction. Migration, on its own, cannot plausibly eliminate the welfare advantage at the WDT's calibrated burden level.

The Agrawal 6× cross-base multiplier is directionally valid but calibrated to intra-national Spanish regional mobility. A UK-specific multiplier of 2–3× is more defensible. Even at 6×, the migration break-even remains implausibly high.

### 6.4 The WDT Is Likely a Net Administrative Saver

Current HMRC Self Assessment admin cost (CGT's collection mechanism): **2.14p per £1**. WTC projected ongoing government cost for a UK annual wealth tax at the £10m threshold: approximately **0.03p per £1** (£3m/year against ~£10bn projected revenue). The WDT's admin cost per £1 of revenue is likely lower than any comparable incumbent instrument, not higher.

This is the one cost category where EVAL's conclusion is almost certainly not "possible threat to welfare advantage" but "net benefit." The structural argument (no open-ended valuation disputes under Routes C/D, bounded two-stage process under Routes A/B) is well-supported by the WTC evidence base.

### 6.5 The Honest Framing for EVAL's Output

EVAL's output should be presented as: **"The WDT's welfare advantage survives Category 3 costs unless [condition]. That condition requires [implausible empirical magnitude] in the case of [migration/admin] and [plausible but uncertain magnitude] in the case of [intensive margin avoidance]. Phase One is the resolution path for the latter."**

This framing is more honest and more useful than a single welfare number, because it makes the uncertainty explicit and identifies the empirical questions that actually matter.

---

## 7. Open Questions for EVAL Development

### 7.1 Modelling Choices to Resolve Before Coding

1. **Death probability model.** Use ONS England national life tables starting at age 60 (the assumed WDT entry age based on inheritance-triggered W_min crossing)? Or a distribution of entry ages? The simpler approach (single entry age 60, life table gives annual probability of death through age 90) is sufficient for EVAL's Level 1 contribution.

2. **CGT realisation decision rule.** Dammon-Spatt-Zhang show optimal rebalancing is complex. For EVAL, use a simpler rule: realise when embedded gain ratio exceeds a threshold (calibrated to be roughly welfare-neutral), or realise at a fixed fraction of gains each year. The full dynamic optimisation is the correct answer but is substantially harder to implement. Decide whether Option A (threshold rule) or Option B (full dynamic optimisation) is within scope for this model.

3. **Treatment of BADR lifetime limit.** BADR applies at 18% to the first £1m of lifetime qualifying business asset gains. For the reference taxpayer (terminal wealth ~£20m), the BADR limit is reached early in the holding period. Model BADR as: 18% on first £1m of gains, then 24% thereafter. This is more realistic than a flat 24% for the entire path.

4. **Route D fraction of portfolio.** BEHAV §8.2 estimates Route D at 10–20% of WDT-taxable wealth. For the 95th percentile Good-tier reference taxpayer with W₀ ≈ £1.63m, a large fraction may be in listed equities (Route A) or property (Route B). The Route D inheritance auction cost is therefore a fraction of total portfolio value, not the whole thing. Need an assumed Route D fraction for the reference taxpayer.

5. **Discount rate for welfare calculations.** WFR uses γ = 2 (CRRA) with no explicit discount rate for welfare comparisons. EVAL's N = 30 model needs a discount rate ρ for present-value comparisons. Use ρ = 5% (consistent with VAL.A §C.12 NPV adjustment) as the central case.

### 7.2 Data Still to Fetch

- ONS England life tables (starting age 60, annual death probabilities to age 90)
- Christie's/Sotheby's buyer's premium schedules by asset type
- UK M&A process cost data for private company transactions £5m–£100m
- Dammon-Spatt-Zhang (2001) full text for welfare cost quantification
- Jensen-Marekwica (2013) full text for the <0.5% figure and its assumptions

### 7.3 Scope Boundaries

EVAL is not:
- A general equilibrium model (no labour market, no asset price effects)
- A behavioural calibration model (no empirical WDT-specific migration or avoidance estimates)
- A revenue forecast (that is RATES's job)
- A political economy model (Phase One failure scenarios are scenarios, not probabilities)

EVAL is a break-even characterisation. Its primary output is threshold values: "Cost X must exceed Y to eliminate the welfare advantage." The interpretation of whether Y is plausible is documented with reference to the empirical literature and left to the reader.

---

## 8. Source Reference List

All sources cited or consulted in the planning session, with provenance.

### 8.1 Migration and Behavioural Response

**Jakobsen, K., Jakobsen, K., Kleven, H., & Zucman, G. (2024).** *A Dozen Facts about Wealth Taxation and Portfolio Choice.* NBER Working Paper 32153. [Key finding: semi-elasticity −0.17 pp; migration 0.22 cents/dollar; intensive margin 0.54 cents/dollar]

**Agrawal, D., Foremny, D., & Martínez-Toledano, C. (2025).** *Wealth Taxes and Mobility.* American Economic Journal: Economic Policy. [Key finding: 6× cross-base externality multiplier; calibrated to Spanish intra-regional competition; likely overstates UK national WDT magnitude]

**Agersnap, O., & Zidar, O. (2021).** The Tax Elasticity of Capital Gains and Revenue-Maximizing Rates. *AER: Insights, 3*(4): 399–416. [Key finding: long-run elasticity of CGT realizations substantially larger than short-run; lock-in effect builds over time]

**Londoño-Vélez, J., & Avila-Mahecha, J. (2025).** [Wealth tax administrative capacity and compliance.] *Review of Economic Studies, 92*(4): 2624–2655. [Colombia wealth tax; key finding: magnitude of response tracks with weakness of third-party reporting infrastructure]

### 8.2 CGT Lock-In and Dynamic Portfolio Choice

**Auerbach, A. J. (1991).** Retrospective Capital Gains Taxation. *American Economic Review, 81*(1): 167–178. [Foundational: retrospective CGT eliminates lock-in by charging interest on deferred gains; equivalent to accrual on ex-ante basis]

**Dammon, R. M., Spatt, C. S., & Zhang, H. H. (2001).** Optimal Consumption and Investment with Capital Gains Taxes. *Review of Financial Studies, 14*(3): 583–616. [Key finding: optimal equity holding increases with age due to death step-up; incentive to rebalance inversely related to embedded gain size; death step-up is the dominant feature for long-horizon holders]

**Jensen, B. A., & Marekwica, M. (2013).** Asset allocation over the life cycle: How much do taxes matter? *Journal of Economic Dynamics and Control.* [Key finding: CEW gains from tax-optimised portfolio decisions < 2% of financial wealth + lifetime income; < 0.5% relative to mark-to-market; calibrated to typical investor with labour income — adjustments required for WDT population]

### 8.3 UK Effective Tax Rates and CGT Structure

**Advani, A., & Summers, A. (2023).** How much tax do the rich really pay? Evidence from the UK. *Oxford Review of Economic Policy, 39*(3): 406–xxx. [Key finding: average EATR for £1m income/gains = 35%; EATRs decline at the top; a quarter of top 1% pay ≥9pp below headline rate; capital gains are primary driver of low effective rates]

**Advani, A., Lonsdale, H., & Summers, A. (2024).** Reforming Capital Gains Tax: Revenue and Distributional Implications. CenTax Policy Briefing. [Key finding: more than 90% of all taxable gains go to individuals with total remuneration above £100,000; CGT reform must include base-broadening to be effective]

**HMRC (2025).** Capital Gains Tax statistical tables. [Key finding: in 2022/23, 41% of CGT receipts came from individuals with gains of £5m+; this group is <1% of CGT taxpayers]

**MHA / Deloitte / GoFile (2026).** CGT rate history and current rates. [Key finding: headline rates from October 2024 Budget: 18% basic, 24% higher rate; BADR 14% (2025/26) rising to 18% (2026/27); EOT effective rate 12% for higher-rate taxpayers on unlimited gains]

### 8.4 Administrative Costs

**National Audit Office (2025).** The Administrative Cost of the Tax System. [Key finding: HMRC system-wide cost of collection 0.51p per £1; Self Assessment 2.14p per £1; taxpayer compliance burden estimated at £15.4b/year for businesses — individuals not separately estimated]

**Burgherr, D. (2021).** Costs of Administering a Wealth Tax. In Advani, Chamberlain, & Summers, *A Wealth Tax for the UK: Evidence and Design,* Wealth Tax Commission. [Key finding: central estimate 0.1% of taxable wealth in taxpayer compliance costs, 0.05% in government costs; French ISF: 2.07% of revenue in admin costs; WTC projected UK annual wealth tax at £10m threshold: £3m/year ongoing government cost for 22,000 taxpayers]

**Wealth Tax Commission (2020).** *A Wealth Tax for the UK.* [Key institutional reference; £10m threshold corresponds closest to WDT operating range; admin cost estimates most directly applicable]

### 8.5 WDT Project Documents

**WFR (2026).** Taxpayer Welfare Comparison Across Tax Systems at Revenue Equivalence. Shortcode: WFR. [Primary welfare baseline: 141 bp CGT lock-in cost at T=5, G/V=50%, τ_cgt=24%; 181 bp at T≥8 plateau; concentration results by tier]

**WFR.A (2026).** Taxpayer Welfare Comparison Appendix Tables. Shortcode: WFR.A. [Simulation tables: CEW by system/γ/distribution; lock-in cost by G/V and T; heterogeneous agent results by tier]

**RATES (2026).** Rates and Revenue. Shortcode: RATES. [Revenue baseline: £873.6b/year lifetime average N=30; burden matrices; bracket populations; 0.35% revenue-weighted annual wealth burden; 13.0% gain-weighted effective lifetime rate]

**BEHAV (2026).** Behavioural Robustness and Administrative Experience. Shortcode: BEHAV. [Nine behavioural shapes; route distribution estimates (Route D: 10–20% of WDT-taxable wealth); Agrawal 6× multiplier discussion and structural responses]

**JUR (2026).** UK Jurisdiction and Data Reference Paper. Shortcode: JUR. [HMRC FTE and budget data; VOA institutional data; VTS operating cost £5.2m/year; WAS degradation note; institutional capacity assessment]

**VAL (2026).** Valuing Wealth. Shortcode: VAL. [Four-route architecture; tolerant zone α≈0.8–1.5; Route D auction mechanism; death auction waiver; inheritance auction as mandatory hard reset]

**WDT_Params.toml.** Single source of truth for all model parameters. [Return series 1947–2019; bracket populations; tier differentials; rate function parameters; budget base and growth]

---

## 9. Existing Code Infrastructure

### 9.1 What Lives in wdt_core.py

`wdt_core.py` is the simulation engine for the WDT mechanism itself. `eval_core.py` should import from it directly — do not duplicate these.

**Rate function:**
```python
tau(W_m, p)  # logistic marginal rate — the canonical implementation
```
Parameters come from `p['tau_0']`, `p['tau_m']`, `p['k']`, `p['W_min']`. Returns 0 for W < W_min. This is the single source of truth for the rate function; EVAL must use it, not reimplement it.

**Single-taxpayer simulation (Route C, N-period):**
```python
simulate(V0_m, g_series, alpha, p)   # → list of N+1 record dicts
simulate_sell(sim, g_next, p)         # → sell-year event dict
settle_tw(sell_result, p)             # → (TW_settled, net_settle_tax, n_iter)
```
Each record contains: `{t, V, W, f, cum, L, rate, delta, q}`. The `f` field is the equity retention fraction (only relevant for Route C — alpha drops out at liquidation, so `W_sell = f_N * V_sell` not `f_N * alpha * V_sell`). `cum` is the lifetime contribution envelope balance. `L` is the tax/refund in that period (negative = refund). The envelope floor is enforced: `L = max(-cum, rate * delta)`.

**Primary output metrics from a simulation:**
- `TW_settled` — settled terminal net worth after post-sale oscillation converges. **This is the primary metric, not TW.**
- `Net_settled` — net lifetime tax including post-sale settlement. Use this, not `Net`.

**Convenience runners:**
```python
run_sim(p_in, alpha, N, g)        # constant-g simulation
run_sim_hist(p_in, alpha, N)      # uses p['returns'] historical series
```
Both return the same dict: `{TW, TW_settled, TTP, Refunds, Net, Net_settled, records, sell, g_use, settle_iters}`.

**NPV calculation (C.12):**
```python
npv_tax(records, sell, rho)              # PV of all tax cash flows
npv_tax_advantage(p, alpha, g, rho)     # C.12 metric: NPV diff vs honest
```
Discounts at rate `rho` (from `p['rho']` = 0.05). This is exactly what EVAL needs for the per-taxpayer welfare present-value calculation.

**SSM marginal revenue:**
```python
_ssm_marginals(p, max_N=71)  # → list of {N, ttp, ref, net, g} per year
```
This is the expensive loop that populates the SSM. EVAL's aggregate fiscal module needs this for the revenue baseline. The marginals are in £b, scaled by `b['N'] / 1000.0` per bracket.

**Parameter loading:**
```python
load_params(toml_path)  # → unified p dict with all TOML values
```
This is the entry point for all parameters. EVAL should call this once and pass `p` everywhere. Key fields EVAL needs:
- `p['returns']` — rotated 73-element list starting at scenario_start_year (2000)
- `p['returns_meta']` — numpy array, offset, year list (unrotated)
- `p['brackets']` — list of `{label, N, V0_m}` (N in individuals, V0_m in £m)
- `p['tiers']` — list of `{label, weight, differential}`
- `p['rate']` — sub-dict with `tau_0`, `tau_m`, `k`, `W_min`
- `p['tcm']` — sub-dict with `canonical_N` (30), `hist_mean` (0.1045)
- `p['rho']` — discount rate (0.05)
- `p['N_demo']` — 30 (demographic reference horizon)
- `p['V0_m']` — 20.0 (VAL reference entry wealth, not the bracket entry wealths)
- `p['sweep']` — all sweep grids including `wfr_*` keys

**What wdt_core does NOT do:**
- No CEW calculation
- No welfare comparison across systems
- No CGT model of any kind
- No migration or admin cost modelling
- No death probability or step-up

---

### 9.2 What Lives in wfr_core.py

`wfr_core.py` is the welfare comparison engine. `eval_core.py` should import the primitives; it does not need to run the WFR modules themselves.

**Importable primitives — use these directly:**

```python
# Core types
ReturnDistribution(returns, probs, label)   # dataclass; validates sum(probs)==1

# Welfare arithmetic
crra_utility(c, gamma)                      # CRRA utility, handles gamma=1 (log)
expected_utility(W0, dist, tax_fn, tau, gamma)
expected_tax(W0, dist, tax_fn, tau)
consumption_equiv_welfare(eu_tax, eu_notax, gamma)  # → CEW (λ)
variance_of_consumption(W0, dist, tax_fn, tau)

# Revenue equivalence
solve_revenue_equivalent_rate(W0, dist, tax_fn, target_et)  # Brent solver

# Tax system functions (all take W0, R, tau → TaxResult)
tax_symmetric_flat    # flat-rate WDT
tax_income            # income tax, gains only, no refund
tax_cgt               # = tax_income in Module 1 (lock-in enters Module 3)
tax_stock_wealth      # stock wealth tax on W1
tax_consumption       # consumption tax
get_tax_fn(name)      # registry lookup

# Progressive rate function
ProgressiveRateFunction(tau0, taum, k, W_min)
  .rate(W)                    # point rate at W
  .effective_rate(W0, W1)     # midpoint approx for delta
build_rate_fn(p)              # convenience constructor from p['rate']
ScaledRateFn(base_fn, scale)  # uniform scale factor on effective_rate

# Progressive welfare helpers
tax_progressive_wdt(W0, R, rate_fn)          # → (tax, W1_post, consumption)
expected_utility_progressive(W0, dist, rate_fn, gamma)
expected_tax_progressive(W0, dist, rate_fn)

# Full comparison runner
run_welfare_comparison(W0, dist, gamma, target_et)  # → {system: SystemResult}

# Distribution constructors
make_empirical_distribution_scenario(p, N)      # Ver. A, N-year from scenario start
make_idealised_distribution_scenario(p, N)      # Ver. B, calibrated to same N-year
make_empirical_distribution_for_start(p, start_year, N)  # for Sweep B
make_empirical_distribution(p)                  # full 73-year, used internally

# CGT lock-in (Module 3 primitives — static model to be extended)
AssetSwitchDecision(V, B, tau_cgt, T, r_A)
  .indifference_return()      # r_B* at which switching is welfare-neutral
  .switch_cost_pv()           # CGT cost of realising today
  .value_of_stay(r_B_grid)    # NPV comparison array

# Heterogeneous agent tier
AgentTier(name, differential, pop_share, W0, bracket_label)
  .shifted_distribution(base_dist)  # applies tier differential to return series

# Diagnostics
dm_test(W0, dist, tau)        # D-M property check

# Module constants (module-level, available after import)
W0_NORM   = 1.0               # normalised reference wealth
TARGET_ET = 0.02              # 2% of W0 revenue target
GAMMA_VALS = [1.0, 2.0, 4.0]
GAMMA_CEN  = 2.0
SYSTEMS    = ["symmetric_wdt", "stock_wealth", "income", "cgt", "consumption"]
```

**Known bugs from refactor (do not import these until fixed):**
The file has at least one reference to `OUTPUT_DIR` in `run_module5()` (line 1569) that references the module-level variable `OUTPUT_DIR` but should be using `module_output_dir("wfr")` — the refactor likely introduced a scoping issue here. Do not call the `main()` function until this is resolved. The importable primitives listed above are unaffected.

**What wfr_core does NOT do:**
- No N-period dynamic simulation — all welfare comparisons are single-period (one-shot expected utility over a distribution)
- No death probability or step-up — CGT Module 3 is static
- No lifetime contribution envelope tracking — the WDT is modelled as single-period `tau * delta`, not as a multi-year path with cumulative `cum`
- No migration, admin cost, or break-even analysis
- No bracket-population weighting — tier comparison uses one representative agent per tier, not the full population grid

---

### 9.3 The Structural Gap EVAL Must Bridge

The central architectural problem for EVAL is that **wdt_core and wfr_core model different things and have never been connected**:

| Dimension | wdt_core | wfr_core |
|---|---|---|
| Time horizon | N periods (30 years) | Single period (one-shot EU) |
| WDT tax | Full delta simulation with f-erosion, cumulative envelope, settle_tw | `tau * (W1 - W0)` flat |
| CGT | Not present | Static switching decision at fixed T |
| Return path | Actual year-by-year series with compounding | Distribution over states, equal weight |
| Output | TW_settled, Net_settled (£m) | CEW (proportional welfare change) |
| Death | Not modelled | Not modelled |
| Population | All 40 bracket×tier cells via SSM marginals | One representative agent per tier |

EVAL needs to bridge these two frameworks to produce comparable N=30 welfare numbers for both WDT and CGT. The approach:

**For the WDT side:** Use `wdt_core.run_sim_hist()` to simulate the N=30 path for a representative taxpayer. Convert `TW_settled` into a consumption-equivalent by treating it as the terminal consumption available to the agent. For CEW comparison, compute EU over the historical return sequence using the wdt_core path outputs rather than wfr_core's single-period expected utility.

**For the CGT side:** Build a new N-period dynamic CGT simulation in `eval_core.py`. At each year t, given current wealth W_t and embedded gain (W_t - B_t), decide whether to realise based on the death probability and remaining horizon. At death: step-up (basis resets to W_t, no CGT). At year N (if not dead): forced realisation. Convert the N-period consumption path to EU and CEW using the same wfr_core primitives.

This means EVAL's Module 1 (the N=30 welfare baseline) produces results that are **not directly comparable to WFR's Module 1** — they are computed on a different basis (multi-period path vs single-period distribution). EVAL should make this explicit in its output, noting that the N=30 results are a separate computation from the WFR baseline and are expected to show a larger WDT advantage for the reasons documented in Section 2.2.

---

## 10. eval_core.py — Specification

### 10.1 File Structure

```
eval_core.py
│
├── 0.  Imports and paths
├── 1.  Parameter loading (delegates to wdt_core.load_params)
├── 2.  N-period WDT simulation wrapper
├── 3.  N-period CGT dynamic model (new — the core contribution)
├── 4.  N=30 welfare baseline (Module E1)
├── 5.  Per-taxpayer break-even analysis (Module E2)
├── 6.  Migration response model (Module E3)
├── 7.  Admin cost comparison (Module E4)
├── 8.  Aggregate fiscal break-even (Module E5)
├── 9.  Module constants and serialisation
├── 10. CLI entry point
```

### 10.2 Imports

```python
# From wdt_core — use directly, do not reimplement
from wdt_core import (
    tau,                  # rate function
    simulate,             # N-period Route C simulation
    simulate_sell,        # terminal sell event
    settle_tw,            # post-sale oscillation
    run_sim,              # constant-g convenience runner
    run_sim_hist,         # historical-series runner
    npv_tax,              # PV of tax cash flows
    npv_tax_advantage,    # C.12 metric
    load_params,          # parameter loading
    _ssm_marginals,       # aggregate revenue marginals
)

# From wfr_core — primitives only
from wfr_core import (
    ReturnDistribution,
    crra_utility,
    consumption_equiv_welfare,
    ProgressiveRateFunction,
    build_rate_fn,
    tax_progressive_wdt,
    make_empirical_distribution_scenario,
    make_empirical_distribution_for_start,
    AgentTier,
    GAMMA_CEN, GAMMA_VALS, W0_NORM,
)
```

### 10.3 Module E1 — N=30 Welfare Baseline (New CGT Dynamic Model)

This is the core new contribution. Replace `AssetSwitchDecision`'s static T-period model with a proper N-period dynamic simulation.

**New class: `DynamicCGTAgent`**

```python
@dataclass
class DynamicCGTAgent:
    W0: float           # initial wealth (£m)
    tau_cgt: float      # effective CGT rate (scenario parameter)
    r_A: float          # baseline return (hist_mean = 10.45%)
    death_probs: list   # annual death probability by year, len=N (from ONS life tables)
    badr_limit: float   # £m of gains eligible for BADR rate (default 1.0)
    tau_badr: float     # BADR rate (default 0.18)
```

**Simulation logic per year t:**

```
State: (W_t, B_t, cum_t, alive)
  W_t    = current wealth
  B_t    = CGT recognised basis (resets at death to W_t — step-up)
  cum_t  = cumulative CGT paid (for comparison with WDT envelope)

Each year:
  1. Draw return r_t from historical sequence
  2. W_t = W_{t-1} * (1 + r_t)
  3. Check death: with prob death_probs[t], taxpayer dies
     → step-up: B_t = W_t (embedded gain forgiven), no CGT, heir inherits W_t
     → simulation ends; record W_death as terminal consumption
  4. If alive: realisation decision
     → compute r_B_indiff at current (W_t, B_t, tau_cgt, T_remaining)
     → if r_t > r_B_indiff: switch (realise), pay CGT on (W_t - B_t), B_t = W_t
     → else: hold, no tax
  5. Repeat to year N
  6. If still alive at year N: forced realisation, pay CGT on (W_N - B_N)
```

**CEW conversion:**
The N-period path produces a terminal consumption value C_terminal = W_terminal after all CGT is paid. Convert to CEW using the wfr_core utility:
```python
eu_wdt = crra_utility(wdt_sim['TW_settled'], gamma)
eu_cgt = crra_utility(cgt_sim.C_terminal, gamma)
eu_notax = crra_utility(W0 * product(1 + r_t for t in range(N)), gamma)
cew_wdt = consumption_equiv_welfare(eu_wdt, eu_notax, gamma)
cew_cgt = consumption_equiv_welfare(eu_cgt, eu_notax, gamma)
wdt_advantage_bp = (cew_wdt - cew_cgt) * 10000
```

**Sweep parameters for Module E1:**

| Parameter | Values | Purpose |
|---|---|---|
| `tau_cgt` | 0.24, 0.18, 0.14, 0.12, 0.00 | Headline → optimal structuring → death step-up only |
| `death_prob` | ONS central, 0.5× ONS, 0.0 | Sensitivity on step-up value |
| `badr_limit` | 1.0, 0.0 | BADR applies / does not apply |
| `gamma` | 1.0, 2.0, 4.0 | Risk aversion sensitivity |
| `W0` | bracket V0_m values | Per-bracket results |

**Output:** `wdt_advantage_bp` by `(tau_cgt, death_scenario, W0, gamma)`. This is the welfare baseline from which Module E2's break-even analysis proceeds.

### 10.4 Module E2 — Per-Taxpayer Break-Even

For each of the five cost categories, compute the annual cost (£/year) that exactly offsets the Module E1 welfare advantage for the reference taxpayer.

**Reference taxpayer:** Good tier, 95th percentile, W0 = £1.629m, N = 30, implied return = 11.4%/year.

**Break-even formula:**

```python
def breakeven_annual_cost(wdt_advantage_bp, W0, N, rho=0.05):
    """
    Annual cost (£m/year) that PV-offsets the welfare advantage.
    welfare_advantage_gbp = wdt_advantage_bp / 10000 * W0
    annualised = welfare_advantage_gbp * rho / (1 - (1+rho)^-N)
    (annuity formula — constant annual cost with PV = welfare advantage)
    """
    welfare_gbp = (wdt_advantage_bp / 10000) * W0
    annuity_factor = rho / (1 - (1 + rho) ** -N)
    return welfare_gbp * annuity_factor
```

**Five cost break-evens:**

1. **Migration:** parameterised on emigration rate. Revenue lost per departure = WDT annual liability × Agrawal multiplier (2×, 4×, 6× scenarios). Break-even emigration rate = welfare_advantage / (revenue_per_departure × multiplier).

2. **Intensive margin avoidance:** parameterised on fraction of annual revenue lost. Break-even fraction = welfare_advantage / annual_wdt_revenue_per_taxpayer.

3. **Compliance cost:** parameterised on £/year professional fees. Break-even = `breakeven_annual_cost(...)` directly. Compare against Burgherr estimates (0.1% of taxable wealth = ~£1,629/year at W0, scaling to ~£19,720/year at terminal wealth).

4. **Route D auction cost:** event-based. Break-even = welfare_advantage / (auction_cost_fraction × route_D_wealth_fraction). Number of Route D events over 30 years: 1 mandatory (inheritance) + 0–2 voluntary. At 3% auction cost on Route D portion (assume 15% of portfolio = £0.24m at W0 growing to ~£3m at terminal wealth): one event costs ~£7,200 at W0 → ~£90,000 at terminal. Bounded, well below break-even.

5. **Admin learning:** framed as a probability-weighted scenario. If Phase One fails (probability p_fail) and system is repealed at year T_repeal, the agent receives only T_repeal years of welfare advantage instead of 30. Expected welfare advantage = (1 - p_fail) × full_advantage + p_fail × (T_repeal/30) × full_advantage. Show the (p_fail, T_repeal) combinations that reduce expected advantage to zero.

### 10.5 Module E3 — Migration Response Model

**Inputs:**
- Jakobsen semi-elasticity: −0.17 pp emigration per 1pp effective WDT rate
- WDT effective burden: 0.35% revenue-weighted (from RATES §2)
- Phase One population: 22,000–50,000 assessed taxpayers
- Agrawal multiplier scenarios: 2×, 4×, 6×
- Baseline out-migration rate: 0.2%/year for top decile

**Computation:**

```python
def migration_revenue_loss(
    effective_burden,      # 0.0035 = 0.35%
    jakobsen_elasticity,   # 0.17 (pp emigration per pp tax rate)
    agrawal_multiplier,    # 2, 4, or 6
    assessed_population,   # 22000
    annual_revenue_per_taxpayer,  # £b aggregate / population
):
    delta_emigration_rate = jakobsen_elasticity * effective_burden  # pp
    annual_departures = assessed_population * delta_emigration_rate / 100
    direct_revenue_loss = annual_departures * annual_revenue_per_taxpayer
    total_revenue_loss = direct_revenue_loss * agrawal_multiplier
    return {
        'delta_emigration_rate_pp': delta_emigration_rate,
        'annual_departures': annual_departures,
        'direct_revenue_loss_gb': direct_revenue_loss,
        'total_revenue_loss_gb': total_revenue_loss,
        'as_pct_of_wdt_revenue': total_revenue_loss / aggregate_wdt_revenue,
    }
```

**Break-even:** Solve for the emigration rate at which total revenue loss (including Agrawal multiplier) equals the aggregate WDT welfare advantage (Module E1 results × population weights).

**Sweep over:** Agrawal multiplier (2×, 4×, 6×), Jakobsen elasticity (baseline, 2×, 5× — upper pessimism scenarios), Phase One population (22k, 50k).

### 10.6 Module E4 — Admin Cost Comparison

Static lookup table, no simulation required.

**Current system admin costs (from research):**

```python
ADMIN_COSTS_CURRENT = {
    'cgt_self_assessment_pence_per_gbp': 2.14,    # NAO 2025
    'iht_pence_per_gbp': 0.66,                     # HMRC Annual Report
    'system_wide_pence_per_gbp': 0.51,             # NAO 2025
    'cgt_annual_receipts_gb': 13.7,                # HMRC 2023-24
    'iht_annual_receipts_gb': 7.5,                 # HMRC 2023-24
}
```

**WDT projected admin costs (from Burgherr / WTC):**

```python
ADMIN_COSTS_WDT = {
    'government_ongoing_gb_at_10m_threshold': 0.003,   # £3m/year, 22k taxpayers
    'taxpayer_central_pct_of_taxable_wealth': 0.001,   # 0.1% Burgherr central
    'taxpayer_wdt_adjusted_pct': 0.0005,               # 0.05% adjusted for route architecture
    'route_c_d_taxpayer_cost': 0.0,                    # zero professional fee
    'route_a_b_taxpayer_cost_pct': 0.001,              # competitive tender, comparable to Burgherr
}
```

**Output:** Admin cost per £1 of revenue, current system vs WDT, with net saving/cost.

### 10.7 Module E5 — Aggregate Fiscal Break-Even

Combine Module E3 (migration) and Module E4 (admin) against the RATES revenue baseline.

**Revenue baseline from wdt_core:**
Use `_ssm_marginals(p)` to get year-by-year net revenue, weighted by bracket populations. Do not re-run the full SSM — inherit the £873.6b/year lifetime average from RATES §7.1 and weight by tier × bracket grid from TOML.

**Aggregate welfare advantage:**
Sum per-taxpayer Module E1 advantages across the 40-cell grid, weighted by `b['N'] * t['weight']`. This gives the total population-level welfare gain from switching to the WDT.

**Break-even conditions:**
Express as: "migration rate must exceed X% AND/OR intensive margin losses must exceed Y cents/dollar to eliminate the aggregate welfare advantage." Run on a grid so the (migration, avoidance) combinations that threaten the baseline are visible as a contour plot.

### 10.8 Output Schema

```json
{
  "meta": {
    "version": "eval_core_v1",
    "date": "...",
    "params": { ... }
  },
  "module_e1": {
    "n30_welfare_baseline": {
      "by_scenario": {
        "(tau_cgt=0.24, death=ons_central)": {
          "wdt_cew": ...,
          "cgt_cew": ...,
          "wdt_advantage_bp": ...,
          "breakeven_annual_cost_gbm": ...
        }
      }
    }
  },
  "module_e2": {
    "reference_taxpayer": { "W0": 1.629, "tier": "Good", "bracket": "95%", "N": 30 },
    "breakeven_by_cost": {
      "migration": { "required_emigration_rate_pct": ..., "jakobsen_implied_pct": ... },
      "avoidance": { "required_cents_per_dollar": ..., "jakobsen_upper_bound": 0.54 },
      "compliance": { "required_annual_gbm": ..., "burgherr_estimate_gbm": ... },
      "auction":   { "required_events": ..., "realistic_events": "1-2" },
      "learning":  { "p_fail_T_repeal_combinations": [...] }
    }
  },
  "module_e3": {
    "migration_scenarios": [
      { "multiplier": 2, "elasticity": "jakobsen", "annual_departures": ..., "revenue_loss_gb": ... },
      { "multiplier": 4, ... },
      { "multiplier": 6, ... }
    ],
    "breakeven_emigration_rate_pct": ...
  },
  "module_e4": {
    "current_system": { "cgt_pence_per_gbp": 2.14, "iht_pence_per_gbp": 0.66 },
    "wdt_projected":  { "government_pence_per_gbp": ..., "taxpayer_pence_per_gbp": ... },
    "net_saving_gb_per_year": ...
  },
  "module_e5": {
    "aggregate_welfare_advantage_bp": ...,
    "break_even_surface": { "(migration_rate, avoidance_fraction)": "threatens_baseline" }
  }
}
```

### 10.9 What eval_core.py Must NOT Do

- Do not reimplement `tau()`, `simulate()`, or `settle_tw()` — import from wdt_core
- Do not reimplement `crra_utility()` or `consumption_equiv_welfare()` — import from wfr_core
- Do not run wfr_core's `main()` or call `run_module1()` through `run_module5()` — EVAL is a separate pipeline
- Do not re-derive the RATES revenue figures — use `_ssm_marginals()` and the documented RATES §7.1 outputs as inputs
- Do not produce figures — output JSON only; figures are a separate output script's job (consistent with the rest of the pipeline)
- Do not run the full SSM with post-fill mechanics — only the capitalisation marginals are needed for EVAL's aggregate fiscal frame

### 10.10 ONS Life Table Data Requirement

Module E1's `DynamicCGTAgent` requires annual death probabilities for a UK adult entering the WDT system at age 60, for years t = 1 to 30 (ages 61–90).

Source: ONS National Life Tables, England, latest available (2020–2022 edition as of September 2026). The relevant column is q_x — probability of dying between age x and age x+1 for males or females separately, or for persons combined.

These values must be hardcoded into `eval_core.py` as a lookup table or read from a small CSV. They are not in the TOML and are not available from wdt_core or wfr_core.

**Confirmed values — ONS England and Wales 2018–2020 (males), from lifetable.de citing ONS:**

Source: ONS National Life Tables, England and Wales, 2018–2020. Males column. These are period q_x values (probability of death between age x and x+1). The WDT population is predominantly male (wealth concentration is strongly male-skewed in UK data); the males column is the appropriate central case. Persons-combined values are approximately 10–15% lower at each age.

```python
# ONS England and Wales 2018-2020, males
# Source: lifetable.de citing ONS; confirmed from search result index 14
ONS_QX_MALES_2018_2020 = {
    60: 0.007758,   # from England and Wales 2018-2020 males
    61: 0.008398,
    62: 0.009380,
    63: 0.010286,
    64: 0.011167,
    # 65-89: need full table — approximate from lx survivors column
    # England and Wales males 2018-2020: lx at 60 = 90921, at 89 ≈ (from dx pattern)
}
```

**Full q_x table (ages 60–90) to be hardcoded in eval_core.py:**

The values below are derived from the England and Wales 2018–2020 males series (confirmed from ONS via lifetable.de, result index 14). The 2020–2022 England series (result index 25) is confirmed to exist at lifetable.de but the ages 60–90 are not in the search snippets. Before coding, fetch the full 2020–2022 England series from:

`https://www.lifetable.de/File/GetDocument/data/GBR/GBRENG020202022CU1.pdf`

and replace the 2018–2020 values below. The 2020–2022 values will be slightly higher at ages 70–85 due to COVID-period mortality effects.

**Working values (England and Wales 2018–2020 males) confirmed from ONS:**

| Age | q_x (males) | Source |
|---|---|---|
| 60 | 0.007758 | England and Wales 2018-2020, ONS via lifetable.de |
| 61 | 0.008398 | confirmed |
| 62 | 0.009380 | confirmed |
| 63 | 0.010286 | confirmed |
| 64 | 0.011167 | confirmed |
| 65 | ~0.012200 | interpolated from lx series |
| 66 | ~0.013400 | interpolated |
| 67 | ~0.014700 | interpolated |
| 68 | ~0.016200 | interpolated |
| 69 | ~0.017900 | interpolated |
| 70 | ~0.019800 | interpolated |
| 71 | ~0.021900 | interpolated |
| 72 | ~0.024200 | interpolated |
| 73 | ~0.026800 | interpolated |
| 74 | ~0.029700 | interpolated |
| 75 | ~0.033000 | interpolated |
| 76 | ~0.036700 | interpolated |
| 77 | ~0.040900 | interpolated |
| 78 | ~0.045600 | interpolated |
| 79 | ~0.050900 | interpolated |
| 80 | ~0.057000 | interpolated |
| 81 | ~0.064000 | interpolated |
| 82 | ~0.071800 | interpolated |
| 83 | ~0.080700 | interpolated |
| 84 | ~0.090800 | interpolated |
| 85 | ~0.102200 | interpolated |
| 86 | ~0.115100 | interpolated |
| 87 | ~0.129500 | interpolated |
| 88 | ~0.145700 | interpolated |
| 89 | ~0.163800 | interpolated |
| 90 | ~0.183800 | interpolated |

**Pre-coding action required:** Fetch the full 2020–2022 England table from the ONS or lifetable.de PDF to replace interpolated values with confirmed figures at each single year of age from 60–90. The confirmed values for ages 60–64 above should be verified against that table as a consistency check.

**Note on persons vs males:** The WDT population at W₀ ≈ £1.63m–£140m is male-dominated in UK wealth survey data (men hold approximately 60–65% of net wealth in the top quintile). Using males q_x is the appropriate central case. For sensitivity, run Module E1 also with females q_x (approximately 25–30% lower mortality at each age, which reduces the CGT step-up benefit and makes the WDT relatively more attractive).

---

*End of EVAL_PLAN.md*  
*Version updated: 28 September 2026 — Added Sections 9 and 10 covering existing code infrastructure and eval_core.py specification.*
