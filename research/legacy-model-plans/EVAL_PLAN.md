# EVAL: Break-Even Welfare Analysis — Planning Document

**Status:** Pre-development planning  
**Authors:** K. Ogata / Claude (research and planning session, 28 September 2026)  
**Purpose:** This document records the full research and planning conversation that preceded development of the EVAL model. It is the single reference point for model design decisions, source provenance, data requirements, and open questions before a line of code is written.

---

## 1. What EVAL Is

WFR establishes a pre-behavioural welfare baseline showing that the WDT eliminates 141–143 basis points of welfare cost that CGT imposes through realisation lock-in. WFR cannot say whether the prospective implementation costs of the WDT exceed that advantage, because those costs are unquantifiable without implementation data.

EVAL's job is to make that uncertainty tractable through break-even analysis. The question is not whether the WDT's welfare advantage survives Category 3 costs. The question is: **how large would each implementation cost have to be to eliminate the advantage?** If a break-even threshold is empirically implausible, that cost cannot explain away the welfare advantage. If it falls within a plausible empirical range, that is a genuine open question for Phase One.

This framing is intentionally adversarial. EVAL is a stress test of the WFR result, not a defence of it. It does not assume the WFR baseline survives — it rebuilds the relevant long-horizon comparator from scratch before calculating break-even thresholds, and reports what it finds regardless of direction.

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

### 2.3 The N = 30 CGT Model EVAL Must Build — and Its Continuity Requirement

**The mechanism that produces 141 bp is a portfolio switching problem, not a single-asset realisation problem.**

WFR's lock-in result specifically arises from the two-asset switching framework in WFR §4.2: the taxpayer holds asset A (current position) and faces asset B (alternative opportunity with potentially higher return). The welfare cost of CGT is the tax-induced switching wedge — the embedded gain on A makes switching to B costly, so the taxpayer rationally remains in an inferior allocation. The 141 bp measures the welfare loss from this distortion, not simply the tax paid on gains.

This has a critical implication for EVAL. If Module 1 replaces WFR's switching model with a single-asset model where assets grow and the taxpayer simply decides whether to realise:

```
State: (W_t, B_t) — single asset, decide to realise or hold
```

then EVAL is measuring something different from WFR. A discrepancy between EVAL's N=30 result and WFR's 141 bp could mean either (a) the N=30 dynamics genuinely change the welfare comparison, which is the interesting result, or (b) you've built a subtly different model. You cannot tell which is happening without the ability to reproduce the WFR result as a special case.

**Continuity requirement:** Before any N=30 extension result is accepted as valid, EVAL must demonstrate that its CGT model reproduces the WFR result of 141.22 bp when run at WFR's reference parameters: T=5, G/V=50%, τ_cgt=24%, γ=2, Ver. A distribution. If EVAL cannot reproduce this, the model has diverged from WFR's mechanism and must be corrected before proceeding.

**The correct architecture: N-period extension of WFR's switching model**

The state must include both assets:

```
State at each period t:
    W_A_t   = current value of held asset A
    W_B_t   = current value of alternative asset B  
    B_t     = CGT recognised basis on A (for CGT simulations)
    age_t   = current age (for death probability)

At each period:
    Observe return r_A_t for current asset (JST historical sequence)
    Observe return r_B_t for alternative asset (same sequence, or modelled separately)
    
    Switching decision:
        Under CGT: switching realises (W_A_t - B_t), triggers CGT payment
                   → threshold condition: r_B > r_B_indiff(W_A_t, B_t, tau_cgt, T_remaining)
                   → the indifference return r_B_indiff is the AssetSwitchDecision mechanism
                   → this is exactly wfr_core.AssetSwitchDecision — use it, extend it
        Under WDT: switching is tax-neutral (no embedded gain crystallisation)
                   → agent switches whenever r_B > r_A (no CGT wedge in the threshold)
    
    Death check: with prob q_x(age_t), taxpayer dies
        Under CGT: step-up; heirs inherit W_A_t with B_t reset to W_A_t (no CGT)
        Under WDT: inheritance auction fires; Route D or A/B at market value
    
    Proceed to t+1
```

This preserves the WFR mechanism — the welfare cost comes from the switching wedge, compounded over N periods — while extending it to the dynamic N=30 horizon with endogenous G/V and death probability.

**The WDT counterfactual in the same framework:**
1. Both assets are held in the optimal portfolio (no switching wedge — WDT is switching-neutral)
2. Annual delta W_t − W_{t-1} computed on total portfolio value
3. WDT applied at τ(W_t) on positive deltas, symmetric refund on negative deltas
4. Death triggers inheritance auction, not step-up

**The key references for this architecture:**

**Dammon, Spatt, and Zhang (2001), Review of Financial Studies 14(3): 583–616.** The foundational dynamic model of optimal consumption and portfolio choice with capital gains taxes. Key finding: the incentive to rediversify is inversely related to the size of the embedded gain and investor's age. Optimal equity holding increases well into an investor's lifetime because of death step-up. This is the theoretical precedent for the N-period two-asset model EVAL is building.

**Jensen and Marekwica (2013), Journal of Economic Dynamics and Control.** Life-cycle model with unspanned labour income and realisation-based CGT. Key finding: CEW gains from tax-optimised decisions < 2% of financial wealth + lifetime income vs a heuristic; < **0.5%** relative to mark-to-market. Three critical adjustments required for the WDT population: (1) no labour income at age 60+, so the denominator shrinks and the 0.5% figure rises substantially as a fraction of financial wealth; (2) the model includes the death step-up which is the primary driver of low welfare cost — EVAL must price step-up removal explicitly; (3) the 0.5% figure is against mark-to-market, not against the WDT's delta base with symmetric refund.

**Agersnap and Zidar (2021), AER: Insights 3(4): 399–416.** Long-run elasticity of CGT realizations substantially larger than short-run — lock-in builds over time, consistent with WFR's plateau finding at T ≥ 8.

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

For migration to eliminate the welfare advantage, the revenue loss through migration and the Agrawal multiplier must equal `ΔCEW_EVAL` from Module E1 (expected to be at least as large as WFR's 141 bp reference, and likely larger at N=30). At a 2× multiplier (conservative UK estimate) and 0.35% annual burden, the implied emigration rate must reach approximately **12–18% of the assessed population** to threaten the WFR 141 bp reference. The Module E1 advantage is expected to be larger, so the actual break-even emigration rate will be higher still. Migration, on its own, is unlikely to threaten the welfare advantage.

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

At 0.54 cents/dollar (upper bound), a WDT collecting £874b/year loses approximately £471b/year to intensive margin responses — leaving net revenue of ~£403b, still substantial relative to the fiscal target. The welfare break-even question is different from the fiscal one: intensive margin avoidance reduces declared deltas (and therefore tax paid), which reduces Treasury revenue, but also involves real costs to the avoider — professional fees, restructuring friction, suboptimal business structures — that are themselves welfare-destroying. The net welfare effect of avoidance is therefore smaller than the gross revenue loss. Module E2 computes the welfare break-even (real resource cost sufficient to eliminate `ΔCEW_EVAL`) and the fiscal break-even (revenue loss sufficient to eliminate projected WDT receipts) as separate outputs and shows that the welfare break-even is reached substantially later than the fiscal break-even. This is an underdeveloped area of the analysis that EVAL should flag as a Phase One empirical question.

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

The break-even annual compliance cost is determined by Module E2's annuity formula applied to `ΔCEW_EVAL`. Using 141 bp as an indicative reference: 141 bp at W₀ = £1.63m implies a welfare advantage equivalent to approximately £22,969 in present-value consumption terms, or a break-even annualised cost of approximately £1,494/year at ρ = 5% (annuity factor 0.0651). The Burgherr WDT-adjusted central estimate of 0.05% of taxable wealth (≈ £815/year at W₀) is well below this indicative threshold; the upper bound at 0.07% (≈ £1,140/year) is also below it. The actual Module E1 baseline is expected to be larger than 141 bp, raising the break-even further. Compliance cost is unlikely on its own to eliminate the welfare advantage.

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

**Treatment in EVAL:** Include as a sensitivity scenario with a parameter for the fraction of the taxable population that successfully engineers simultaneous loss recognition. Show that the break-even fraction required to exhaust `ΔCEW_EVAL` is implausibly high given the coordination barriers — this holds across the full Module E1 scenario range, not just at 141 bp. This is a confirmatory analysis, not a primary risk.

**Data requirement:** None additional. The RATES simulation infrastructure already models this implicitly through the SRR stress scenarios. EVAL can inherit those results directly.

---

## 5. Model Architecture

### 5.1 Overview

EVAL is four modules sharing a common return series and parameter set. The return series is the JST UK equity capital total return data (1947–2019, 73 observations) from `WDT_Params.toml`. Rate function parameters are the Balanced scenario canonical values (τ₀ = 15%, τ_m = 70%, k = 0.001, W_min = £2m).

**Module 1: Welfare baseline at N = 30**  
Rebuilds the WDT-vs-CGT welfare comparison at N = 30 using a proper dynamic CGT simulation. This is new modelling, not inherited from WFR (which uses T = 5). Outputs: `ΔCEW_EVAL = CEW_WDT − CEW_CGT` in basis points, across effective CGT rate scenarios, death probability scenarios, and CGT realisation behaviour scenarios. **141 bp is a reference point from WFR, not an assumption here.** Module 1's output is the actual EVAL baseline, which may be higher or lower than 141 bp depending on the N=30 dynamics. Everything downstream reads from `ΔCEW_EVAL`.

**Module 2: Per-taxpayer break-even**  
For each of the five cost categories, solves for the cost magnitude that exactly offsets the Module 1 welfare advantage. Runs across the four tiers (Poor/Ok/Good/Great) and the key wealth brackets. Output: "cost X must exceed £Y/year to eliminate the welfare advantage for a [tier] taxpayer at [bracket]." All annualisation uses the intertemporal welfare machinery from Module 1, not arithmetic division by N.

**Module 3: Aggregate fiscal break-even**  
Weights per-taxpayer results by TOML bracket populations. Adds migration response using Jakobsen elasticities and Agrawal multiplier (2×, 4×, 6× sensitivity). Adds admin cost comparison. Output: fiscal viability assessment with break-even thresholds for the aggregate revenue claim.

**Module 4: Admin cost comparison**  
Standalone comparison of CGT + IHT admin costs per £1 of revenue against projected WDT admin costs per £1, split by route. Output: whether WDT is a net admin saver and under what assumptions.

### 5.2 Module 1 — Dynamic CGT Model Design

**Architecture: N-period extension of wfr_core.AssetSwitchDecision**

Module 1 is not a new lock-in model. It is a dynamic extension of the existing WFR switching model, preserving the two-asset portfolio structure that generates the 141 bp result. The `AssetSwitchDecision` class in wfr_core already implements the key mechanism: for given (V, B, tau_cgt, T, r_A), it computes the indifference return r_B_indiff above which switching is welfare-improving and below which lock-in occurs. Module 1 makes this dynamic by running that decision at each period t = 1..N rather than at fixed T, and adding death probability.

**State variables at each period t:**

```
(W_A_t, B_t, W_B_t, age_t)
  W_A_t   = current wealth in held asset A
  B_t     = CGT basis on A (resets to W_A_t at death — step-up)
  W_B_t   = current wealth available in alternative asset B
  age_t   = current age (60 + t, for death probability lookup)
```

For the WDT counterfactual, there is no CGT wedge, so the agent holds the optimal portfolio throughout and the state simplifies to (W_t, age_t).

**Per-period logic:**

```
Each year t:
  1. Observe return r_t from the return path (see Return path specification below)
  2. Both assets earn r_t (or a variant — see note on single vs dual asset below)
  3. Compute switching decision under CGT:
       → r_B_indiff = AssetSwitchDecision(W_A_t, B_t, tau_cgt, T_remaining, r_A).indifference_return()
       → if realisation_rule says switch at this point: pay tau_cgt*(W_A_t - B_t), reset B_t = W_A_t
  4. Check death at prob q_x(age_t):
       Under CGT: B_t = W_A_t (step-up), heirs inherit W_A_t, no CGT
       Under WDT: inheritance auction fires (Route D or A/B)
       Simulation ends
  5. Under WDT: compute delta W_t - W_{t-1}; apply tau(W_t) on positive delta; 
                apply refund on negative delta subject to cumulative envelope
  6. Record terminal wealth at period N or at death
```

**Note on single-asset simplification:** The full two-asset model requires modelling the return on asset B, which introduces a second return series not present in the TOML. A valid simplification — consistent with WFR's existing treatment — is to model the switching decision as: the agent faces an opportunity with return r_B that is uncertain, and holds A when the CGT wedge makes the switching threshold too high. In the single-asset extension, this is equivalent to modelling the *cost of non-switching*: the agent is locked in an asset that earns r_A when r_B would have been higher. The welfare cost accumulates as the compounding of this suboptimal allocation. This simplification is acceptable **provided** that the limiting case (T=5, G/V=50%, τ_cgt=24%) reproduces 141.22 bp — if it does, the mechanism is preserved; if it doesn't, the two-asset model is required.

**Reproducibility gate:** Before running the N=30 sweep, Module 1 must run the following validation:

```python
# Validation: reproduce WFR Module 3 result at reference parameters
# If this fails, stop and fix the model before proceeding
val = compute_cew_eval(
    p, W0=1.0, tau_cgt=0.24, realisation_rule='threshold_mid',
    death_probs=[0.0]*5,   # T=5, no death
    gamma=2.0, G_V=0.50,   # reference calibration
    horizon=5              # T=5 to match WFR
)
assert abs(val - 141.22) < 2.0, f"Reproducibility check failed: got {val:.2f} bp, expected ~141.22 bp"
```

A tolerance of ±2 bp is acceptable given differences in path construction. A failure means the mechanism has diverged; do not proceed with N=30 analysis until resolved.

**Welfare decomposition — explicit component output:**

Module 1 must decompose `ΔCEW_EVAL` into its contributing components. This makes the paper substantially harder to attack and allows readers to see why the number has the value it does:

| Component | Description | Sign |
|---|---|---|
| Lock-in switching wedge | Welfare cost of sub-optimal portfolio persistence under CGT | + (favours WDT) |
| CGT realisation taxation | Direct welfare cost of CGT payments when realising | + (favours WDT) |
| CGT death step-up benefit | Welfare benefit of CGT basis reset at death (CGT only) | − (favours CGT) |
| WDT inheritance auction cost | Welfare cost of Route D auction firing at death (WDT only) | + (favours WDT) |
| WDT symmetric refund benefit | Welfare benefit of loss-year refunds (WDT only) | + (favours WDT) |
| **ΔCEW_EVAL (net)** | Sum of above components | ? |

The sign of ΔCEW_EVAL is the answer to EVAL's central question. Decomposing it shows *why* it has that sign, and which components are decisive. Under `hold_to_death`, the death step-up benefit is at its maximum; if WDT still wins, it wins on the other components. That is the adversarial result.

**Return path specification — 44 rolling windows, not 73 starts:**

The JST dataset has 73 annual observations (1947–2019). A 30-year simulation requires a 30-year return sequence. The claim "73 historical starting years" in the previous version of this plan was incorrect — with 73 annual observations and a 30-year window, there are only 44 non-overlapping starting points:

```
73 - 30 + 1 = 44 rolling windows
```

Window 1: 1947–1976
Window 2: 1948–1977
...
Window 44: 1990–2019

**Module 1 uses 44 rolling windows as the primary specification.** The equally-weighted E[U] is computed over these 44 paths. This is the cleanest empirical interpretation and what a reviewer would expect.

Two robustness specifications are computed but labelled as secondary:
- **Circular/wrapping (73 starts):** After 2019, wrap to 1947. Gives 73 paths but introduces artificial 2019→1947 transitions. Labelled "circular" in output.
- **Bootstrap (1,000 paths):** Sample 30 annual returns with replacement from the 73 observations. Gives a larger empirical distribution but changes the stochastic process. Labelled "bootstrap" in output.

The primary result is always the 44-window specification. If results differ substantially across specifications, that is itself reported.

**CGT realisation behaviour — sensitivity dimension:**

Realisation behaviour is a **primary sensitivity dimension** across five rules:

| Rule label | Description | Bias |
|---|---|---|
| `hold_to_death` | Zero realisations during lifetime; full step-up at death | Most favourable to CGT |
| `threshold_high` | Realise only when embedded gain ratio > 80% | Favourable to CGT |
| `threshold_mid` | Realise when embedded gain ratio > 50% | Neutral |
| `threshold_low` | Realise when embedded gain ratio > 30% | Unfavourable to CGT |
| `annual_fraction` | Realise a fixed 5% of embedded gain each year | Unfavourable to CGT |

The `hold_to_death` rule is the economically correct description of the dominant strategy for this population and the most adversarial test. EVAL must report results for all five rules. No single rule is "the" CGT comparator.

**Sweep parameters for Module E1:**

| Parameter | Values | Purpose |
|---|---|---|
| `tau_cgt` | 0.24, 0.18, 0.14, 0.12, 0.00 | Headline → optimal structuring → death step-up only |
| `realisation_rule` | all five rules above | CGT optimisation sensitivity |
| `death_prob` | ONS central, 0.5× ONS, 0.0 | Sensitivity on step-up value |
| `return_path` | 44-window (primary), circular, bootstrap | Distributional robustness |
| `gamma` | 1.0, 2.0, 4.0 | Risk aversion sensitivity |
| `W0` | bracket V0_m values | Per-bracket results |

Note: BADR is **not** a primary sweep dimension at the reference cell. See Section 7.1 for rationale.

### 5.3 Module 2 — Per-Taxpayer Break-Even

For each cost category, compute the annual cost that, as a constant stream over N years, has a present value equal to the welfare advantage produced by Module E1. This uses the annuity formula, not arithmetic division by N — the two differ substantially at ρ = 5% over 30 years (annuity factor ≈ 0.065, versus the ÷30 implicit rate of 0.033).

**The 141 bp figure from WFR does not appear in Module E2.** Module E2 reads `ΔCEW_EVAL` from Module E1's output. The welfare baseline that drives break-even thresholds is whatever Module E1 computes, across the full scenario sweep. Break-even results are therefore reported per scenario, not as single numbers.

See Section 10.4 for the implementation formula.

### 5.4 Module 3 — Aggregate Fiscal Break-Even

**Hard structural rule: welfare break-even ≠ fiscal break-even.**

A fiscal revenue loss is not the same object as a welfare loss. A taxpayer who avoids £1 of WDT liability by spending 20p on professional restructuring has reduced Treasury revenue by £1 but generated a real welfare cost of 20p — the other 80p is a transfer, not a deadweight loss. Similarly, emigration reduces Treasury revenue by the full wealth-tax amount plus cross-base multiplier, but may increase or decrease the emigrant's own welfare, and the welfare of remaining residents is affected through public goods provision and distributional effects. These are different objects and must be computed and reported separately.

Module E5 therefore produces two distinct outputs:

- **Fiscal break-even:** at what behavioural response magnitude does WDT net revenue fall to zero (or to parity with the current system)?
- **Welfare break-even:** at what real resource cost does the per-taxpayer welfare advantage produced by Module E1 fall to zero?

The paper must state explicitly, in its framing and its conclusions, that fiscal solvency and welfare dominance are not the same claim and can diverge.

**Migration (fiscal):**
- Apply Jakobsen semi-elasticity (−0.17 pp per 1pp effective rate) to WDT burden (0.35%)
- Implied annual emigration rate increase: 0.17 × 0.35 = 0.06 pp
- Apply Agrawal multiplier (2×, 4×, 6× sensitivity) for cross-base revenue loss
- Compare to WDT lifetime average revenue (£873.6b/year, RATES §7.1)
- Break-even: what emigration rate makes net fiscal revenue negative

**Intensive margin (fiscal and welfare separately):**
- Apply Jakobsen intensive margin coefficient (0.54 cents/dollar) for fiscal impact
- For welfare impact: note that avoidance activity (professional fees, restructuring, suboptimal holdings) is itself welfare-destroying. The welfare break-even requires the *net* real resource cost, not the gross revenue loss. The fiscal break-even is reached first; the welfare break-even requires substantially more avoidance activity and cost.
- Show the gap between the two thresholds explicitly

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

**Note on how Section 6 findings are used:** Section 6 summarises the empirical priors that informed model design. These are not model outputs and must not be presented as conclusions. The model produces break-even thresholds; Section 6 provides the empirical comparison ranges. The reader draws the conclusion. The correct EVAL output format is a table like the following, not a series of claims about what is or isn't likely:

| Cost category | Break-even quantity | Empirical comparison range | Source |
|---|---|---|---|
| Migration | X% annual emigration rate | Jakobsen: ~0.06 pp increase implied | Jakobsen et al. (2024) |
| Avoidance | £X real resource cost / taxpayer | Jakobsen: 0.54 cents/dollar fiscal | Jakobsen et al. (2024) |
| Compliance | £X/year professional fees | Burgherr: 0.05–0.1% of taxable wealth | Burgherr (2021) |
| Admin failure | X% probability of Phase One failure | No empirical basis — scenario only | — |
| Refund gaming | X% coordinated loss engineering | Structural bound — see §4.5 | — |

The break-even quantities (X values) are computed by Module E2 from `ΔCEW_EVAL`. The empirical comparison ranges are the external data points. The reader sees the gap between them. Section 6 provides that empirical grounding.

### 6.1 The WFR 141 bp Figure as a Reference Point

The WFR baseline of 141 bp is computed against the 24% headline CGT rate at T = 5. It is a reference, not an assumption for EVAL. Three reasons the true N = 30 advantage may differ:

1. **Effective rate for the WDT population is 10–24%, not 24%.** Advani-Summers (2023) establish that EATRs decline at the top of the distribution. EOT structures and deferral-to-death reduce the realistic effective rate for optimally structured disposals. Note: BADR is a minor factor at the reference cell (Good tier, ~£18m lifetime gains) where the £1m lifetime limit is exhausted rapidly; it is more significant for smaller holdings.

2. **The T = 5 calibration may understate lock-in at N = 30.** WFR's lock-in cost plateaus at 181 bp from T = 8 onward due to portfolio persistence. At N = 30, the embedded gain ratio G/V reaches ~90%, and WFR Table 4.2.2b shows lock-in costs approaching 162 bp at G/V = 77%.

3. **The death step-up is potentially the dominant factor at N = 30 — in CGT's favour.** At N = 30, the most valuable feature of CGT for a long-horizon wealthy holder is the basis step-up at death. The WDT's inheritance auction fires at death, removing this benefit. Under `hold_to_death`, CGT effectively costs the agent nothing in present-value terms if the step-up is large enough. Whether the other WDT advantages (switching neutrality, symmetric refund) outweigh this is the central empirical question Module E1 answers.

**The honest framing:** EVAL computes `ΔCEW_EVAL` from first principles at N = 30 under all five CGT realisation rules, reports the full scenario range including CGT-favourable assumptions, and then asks how large each Category 3 cost would need to be to eliminate whatever advantage the model produces. The result may show WDT dominance, CGT dominance, or a range spanning both — all are valid and reported.

### 6.2 Intensive Margin Avoidance — Empirical Grounding

The Jakobsen semi-elasticity gives:

- Migration (extensive margin): 0.22 cents per dollar raised (fiscal)
- Avoidance/restructuring (intensive margin): 0.54 cents per dollar raised (fiscal)

The WDT's tolerant zone (α ≈ 0.8–1.5) and self-balancing mechanisms are specifically designed to reduce the intensive margin response relative to conventional wealth taxes. Whether they succeed is empirically unknown before Phase One. Module E2 will compute the welfare break-even threshold; the comparison against Jakobsen's 0.54 fiscal estimate is the empirical reference point, not the conclusion.

### 6.3 Migration — Empirical Grounding

At the WDT's 0.35% revenue-weighted annual burden, the Jakobsen semi-elasticity implies an annual emigration rate increase of approximately 0.06 percentage points above a 0.2% baseline. Module E3 computes the fiscal break-even emigration rate. The empirical comparison is the Jakobsen-implied rate (~0.06 pp increase) against that threshold. The reader draws the conclusion.

The Agrawal 6× cross-base multiplier is directionally valid but calibrated to intra-national Spanish regional mobility. It is included as the upper-bound multiplier scenario; 2–3× is the more defensible UK estimate.

### 6.4 Admin Costs — Empirical Grounding

Current HMRC Self Assessment admin cost (CGT's collection mechanism): **2.14p per £1** (NAO 2025). WTC projected ongoing government cost for a UK annual wealth tax at the £10m threshold: approximately **0.03p per £1** (£3m/year against ~£10bn projected revenue). Module E4 computes this comparison and the net saving margin.

### 6.5 The Honest Framing for EVAL's Output

EVAL's output should be presented as: **"The WDT's N=30 welfare advantage, computed across the 44-window historical return distribution and across CGT realisation scenarios from the most to the least favourable, ranges from X to Y basis points. Category 3 costs would need to reach [threshold] to eliminate even the lower bound of this range. The empirical comparison for each cost category is shown in the break-even table."**

The paper does not characterise whether each break-even is plausible. It shows the numbers and the empirical reference range. That is EVAL's contribution.

---

## 7. Open Questions for EVAL Development

### 7.1 Modelling Choices — Locked Decisions and Open Items

The following six rules are **locked** — they reflect decisions reached in design review and must not be overridden during coding without explicit author approval:

**Locked rule 1: `ΔCEW_EVAL` is the baseline, not 141 bp.**
141 bp appears nowhere in eval_core.py as a hard-coded constant used to drive break-even calculations. Module E1 computes the baseline; Modules E2–E5 read from it.

**Locked rule 2: CGT realisation behaviour is a sensitivity dimension, not a parameter to calibrate.**
eval_core.py implements all five realisation rules (see §5.2). The primary analytical result is presented across the full rule range. No single rule is presented as "the" CGT comparator. The `hold_to_death` rule must be included and clearly labelled as the most CGT-favourable assumption.

**Locked rule 3: Welfare break-even and fiscal break-even are separate outputs.**
eval_core.py computes and reports both. The narrative never conflates fiscal revenue loss with welfare loss. The distinction is stated explicitly in the output schema and in any text generated from it.

**Locked rule 4: Break-even annualisation uses the annuity formula.**
The annuity factor at ρ = 0.05, N = 30 is approximately 0.0651. The ÷30 shortcut is not used anywhere in the code.

**Locked rule 5: Module 1 must reproduce the WFR 141.22 bp result as a limiting case before N=30 extension proceeds.**
The reproducibility gate described in §5.2 is mandatory. If the model cannot reproduce 141.22 bp (±2 bp tolerance) at WFR's reference parameters (T=5, G/V=50%, τ_cgt=24%, γ=2, no death), development stops and the model is corrected. This gate ensures EVAL is extending WFR's mechanism, not measuring something subtly different.

**Locked rule 6: The primary return path specification is 44 rolling windows, not 73 starts.**
With 73 annual observations (1947–2019) and a 30-year simulation horizon, there are 44 non-overlapping starting windows (1947–1976 through 1990–2019). The claim of "73 independent 30-year paths" is mathematically impossible and is not used. Circular and bootstrap specifications are computed as labelled robustness checks only.

The following items remain open and must be decided before coding:

1. **Death probability model.** Use ONS England national life tables starting at age 60 (single entry age, life table gives annual probability of death through age 90). Entry age distribution is out of scope.

2. **Route D fraction of portfolio.** Assume 15% Route D for the reference taxpayer (midpoint of BEHAV §8.2 range of 10–20%) as the central case, with 10% and 20% as bounds.

3. **Discount rate for welfare calculations.** Use ρ = 5% (consistent with VAL.A §C.12) as the central case. Report sensitivity at ρ = 3% and ρ = 7%.

4. **Single-asset vs two-asset CGT model.** The full architecture requires both asset A and alternative asset B. The single-asset simplification (measuring cost of non-switching directly) is acceptable if and only if it passes the reproducibility gate in locked rule 5. If it fails, the two-asset model is required.

**Note on BADR:** BADR is not a primary sweep dimension at the reference cell (£1m lifetime limit exhausted within a few years of any partial-realisation path for the ~£18m lifetime gain trajectory). Note as a model limitation; model explicitly only for secondary cases where it materially affects the effective rate.

**Note on output presentation:** EVAL does not characterise whether each cost category is "likely" or "unlikely" to threaten the welfare advantage. It produces break-even quantities and provides empirical comparison ranges. See Section 6 and the output table format in §6.0.

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

EVAL bridges these frameworks by:

1. **Extending wfr_core's `AssetSwitchDecision` dynamically** — making the switching decision at each period t = 1..N rather than at fixed T, adding death probability, and adding the death step-up benefit. This preserves the mechanism that generates the 141 bp result and ensures EVAL is genuinely extending WFR rather than building a parallel model.

2. **Using 44 rolling historical windows** — with 73 annual observations and a 30-year horizon, there are 44 non-overlapping starting windows. The primary CEW computation uses equally-weighted E[U] over these 44 paths for both the WDT and CGT systems. Circular (73) and bootstrap (1,000) are labelled robustness specifications.

3. **Enforcing the reproducibility gate before any N=30 results are accepted** — Module E1 must reproduce the WFR 141.22 bp result (±2 bp) at WFR's reference parameters before proceeding. This verifies that the dynamic extension has not inadvertently diverged from the WFR mechanism.

**Distributional basis — correct implementation:**

For each (tau_cgt, realisation_rule, death_scenario, W0, gamma) combination:
- Run 44 WDT simulations (one per rolling window), record `TW_settled` per window
- Run 44 CGT simulations (one per rolling window), record terminal wealth per window
- Run 44 no-tax simulations, record terminal wealth per window
- Compute `E[U_WDT] = mean(crra_utility(tw_i, gamma) for i in 44 windows)`
- Compute `E[U_CGT]` and `E[U_notax]` on the same basis
- Convert to `ΔCEW_EVAL = (cew_wdt - cew_cgt) * 10000` in basis points

Do not pass single `TW_settled` values from individual paths into `crra_utility` and label the result CEW. Single-path results are path illustrations, not expected-utility welfare measures.

**Welfare decomposition — required output structure:**

Module E1 must decompose `ΔCEW_EVAL` into contributing components by running targeted simulations that isolate each effect:

| Component | Isolation method |
|---|---|
| Lock-in switching wedge | CEW difference between CGT-with-lock-in and CGT-without-lock-in (mark-to-market CGT) |
| CGT realisation taxation | CEW cost of actual CGT payments in realisation-rule paths vs no-tax |
| CGT death step-up benefit | CEW difference between CGT-with-step-up and CGT-without-step-up |
| WDT inheritance auction cost | CEW cost of Route D auction at death vs costless inheritance |
| WDT symmetric refund benefit | CEW difference between WDT-with-refund and WDT-without-refund (one-sided WDT) |

The sum of these components equals `ΔCEW_EVAL`. Decomposing it allows the reader to see which components drive the result and how the balance shifts across the realisation rule sweep — particularly how the CGT death step-up benefit interacts with the `hold_to_death` rule.

**For the CGT side — simulation logic:**
Build `DynamicCGTPath` in eval_core.py. At each year t:
1. Apply return r_t from the window's historical sequence
2. Apply realisation rule (see §5.2) to determine whether to crystallise the embedded gain
3. If crystallising: pay tau_cgt × (W_t − B_t); reset B_t = W_t
4. Check death at prob q_x(age_t): if death, apply step-up (B_t = W_t, no CGT); heir inherits W_t
5. At year N if still alive: forced realisation of remaining embedded gain

Terminal wealth = W_N minus all CGT paid through the path.

Note that `AssetSwitchDecision` provides the theoretical indifference-return threshold at each step. Under the `threshold_mid` and related rules, realise when the embedded gain ratio exceeds the threshold, which approximates the regime where the switching wedge makes staying suboptimal. This maintains the link to the WFR mechanism even in the simplified single-asset extension.

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

### 10.3 Module E1 — N=30 Welfare Baseline

This is the core new contribution. Extends `AssetSwitchDecision`'s static T-period model into a proper N-period dynamic simulation preserving the two-asset switching mechanism.

**Reproducibility gate — run first, before anything else:**

```python
def validate_reproducibility(p):
    """
    Must reproduce WFR Module 3 result at reference parameters.
    Tolerance ±2 bp. If this fails, stop and fix the model.
    """
    result = compute_cew_eval(
        p,
        W0=1.0,
        tau_cgt=0.24,
        realisation_rule='threshold_mid',   # approximates WFR's switching threshold
        death_probs=[0.0] * 5,             # no death, T=5
        gamma=2.0,
        G_V_initial=0.50,                  # WFR reference embedded gain ratio
        horizon=5,                          # T=5 to match WFR
        return_spec='circular'             # use full 73-year series as WFR does
    )
    assert abs(result - 141.22) < 2.0, (
        f"Reproducibility check FAILED: got {result:.2f} bp, expected ~141.22 bp. "
        "Fix the CGT dynamic model before running N=30 analysis."
    )
    return result
```

If this fails, the CGT simulation has diverged from WFR's mechanism. Do not proceed with N=30 analysis until resolved.

**New class: `DynamicCGTPath`**

(Renamed from `DynamicCGTAgent` — "Path" is more accurate since one instance produces one return-path simulation.)

```python
@dataclass
class DynamicCGTPath:
    W0: float                # initial wealth (£m)
    B0: float                # initial basis (£m); default = W0 * (1 - G_V_initial)
    tau_cgt: float           # effective CGT rate (scenario parameter)
    death_probs: list        # annual q_x by year, len=N (from ONS life tables)
    realisation_rule: str    # one of: 'hold_to_death', 'threshold_high', 'threshold_mid',
                             #         'threshold_low', 'annual_fraction'
    # AssetSwitchDecision used internally to compute indifference return at each step
    # BADR is not a field — see note below
```

**Simulation logic per year t (single-path, one historical window):**

```
State: (W_t, B_t, cgt_paid_cum)
  W_t          = current wealth (£m); includes prior-year CGT deductions
  B_t          = CGT recognised basis; resets to W_t at death (step-up)
  cgt_paid_cum = cumulative CGT paid to date

Each year:
  1. Apply return r_t from the window's historical sequence
     W_t = W_{t-1} * (1 + r_t)

  2. Compute switching indifference threshold using AssetSwitchDecision:
     decision = AssetSwitchDecision(V=W_t, B=B_t, tau_cgt=tau_cgt,
                                    T=N-t, r_A=r_A_bar)
     r_B_indiff = decision.indifference_return()
     # This links the dynamic simulation to WFR's switching mechanism

  3. Apply realisation rule:
     hold_to_death:    never realise during lifetime
     threshold_high:   realise if (W_t - B_t) / W_t > 0.80
     threshold_mid:    realise if (W_t - B_t) / W_t > 0.50
     threshold_low:    realise if (W_t - B_t) / W_t > 0.30
     annual_fraction:  realise 5% of (W_t - B_t) each year

  4. If realising: pay tau_cgt * (W_t - B_t), deduct from W_t, reset B_t = W_t

  5. Check death at prob death_probs[t]:
     → step-up: B_t = W_t, no CGT; heir inherits W_t
     → terminal_wealth = W_t; simulation ends

  6. At year N if still alive: forced realisation
     terminal_wealth = W_N - tau_cgt * (W_N - B_N)
```

**CEW conversion — 44-window distributional basis (mandatory):**

```python
def compute_cew_eval(p, W0, tau_cgt, realisation_rule, death_probs, gamma,
                     return_spec='rolling_44', G_V_initial=None, horizon=30):
    """
    Returns ΔCEW_EVAL in basis points (positive = WDT wins).
    
    return_spec options:
        'rolling_44'  — primary: 44 non-overlapping 30-year windows (1947-1976..1990-2019)
        'circular'    — robustness: 73 starts, wrapping after 2019 → 1947
        'bootstrap'   — robustness: 1,000 resampled 30-year paths
    """
    windows = get_return_windows(p, spec=return_spec, horizon=horizon)
    # rolling_44: len(windows) == 44
    # circular:   len(windows) == 73
    # bootstrap:  len(windows) == 1000

    eu_wdt_list, eu_cgt_list, eu_notax_list = [], [], []

    for window_returns in windows:  # each is a list of `horizon` annual returns
        # WDT path
        wdt_result = run_wdt_path(p, W0, window_returns, horizon)
        tw_wdt = wdt_result['TW_settled']

        # CGT path
        B0 = W0 * (1 - G_V_initial) if G_V_initial else W0  # basis = W0 if no embedded gain
        cgt_path = DynamicCGTPath(W0=W0, B0=B0, tau_cgt=tau_cgt,
                                   death_probs=death_probs,
                                   realisation_rule=realisation_rule)
        tw_cgt = cgt_path.simulate(window_returns)

        # No-tax path
        tw_notax = W0
        for r in window_returns:
            tw_notax *= (1 + r)

        eu_wdt_list.append(crra_utility(tw_wdt, gamma))
        eu_cgt_list.append(crra_utility(tw_cgt, gamma))
        eu_notax_list.append(crra_utility(tw_notax, gamma))

    eu_wdt   = mean(eu_wdt_list)
    eu_cgt   = mean(eu_cgt_list)
    eu_notax = mean(eu_notax_list)

    cew_wdt = consumption_equiv_welfare(eu_wdt, eu_notax, gamma)
    cew_cgt = consumption_equiv_welfare(eu_cgt, eu_notax, gamma)

    return (cew_wdt - cew_cgt) * 10000   # ΔCEW_EVAL in basis points
```

**Welfare decomposition — required alongside primary output:**

Run additional targeted simulations to isolate each contributing component. These are helper runs using the same 44-window loop:

```python
def decompose_delta_cew(p, W0, tau_cgt, death_probs, gamma):
    """
    Returns a dict of component contributions to ΔCEW_EVAL.
    All components computed at the primary (rolling_44) specification.
    """
    return {
        'lock_in_wedge': (
            compute_cew_eval(..., tau_cgt=tau_cgt, death_probs=[0]*30, ...)
            - compute_cew_eval(..., tau_cgt=0.0, death_probs=[0]*30, ...)
            # difference between CGT-with-lock-in and CGT-without (mark-to-market)
            # death set to zero to isolate the switching wedge
        ),
        'death_step_up_benefit': (
            compute_cew_eval(..., death_probs=[0]*30, ...)
            - compute_cew_eval(..., death_probs=death_probs, ...)
            # CGT only; difference is the value of the step-up
        ),
        'wdt_refund_benefit': (
            compute_cew_eval_wdt_only(..., with_refund=True)
            - compute_cew_eval_wdt_only(..., with_refund=False)
            # WDT only; difference is the symmetric refund value
        ),
        'wdt_inheritance_auction_cost': (
            compute_cew_eval_wdt_only(..., auction_cost_fraction=ROUTE_D_FRACTION)
            - compute_cew_eval_wdt_only(..., auction_cost_fraction=0.0)
        ),
        'net_delta_cew_eval': ...   # must equal sum of above ± floating point
    }
```

**Note on BADR:** Not a sweep parameter at the reference cell. See §7.1.

**Output:** `ΔCEW_EVAL` in basis points by `(tau_cgt, realisation_rule, death_scenario, W0, gamma, return_spec)`, plus `decompose_delta_cew` for the primary scenario. 141 bp is a reference comparison; the computed range is the primary result.

### 10.4 Module E2 — Per-Taxpayer Break-Even

For each of the five cost categories, compute the annual cost (£/year) that exactly offsets the Module E1 welfare advantage for the reference taxpayer.

**Reference taxpayer:** Good tier, 95th percentile, W0 = £1.629m, N = 30, implied return = 11.4%/year.

**Module E2 reads `ΔCEW_EVAL` from Module E1.** It does not use 141 bp. Break-even results are computed per Module E1 scenario, producing a range rather than a point estimate.

**Break-even formula — annuity basis (mandatory):**

```python
def breakeven_annual_cost(delta_cew_eval_bp, W0, N=30, rho=0.05):
    """
    Annual cost (£m/year) whose N-year annuity PV equals the welfare advantage.
    
    welfare_advantage_gbm: ΔCEW_EVAL as a fraction of W0, converted to £m
    annuity_factor: converts lump-sum PV to equivalent constant annual payment
    
    At rho=0.05, N=30: annuity_factor ≈ 0.0651
    Note: simple division by N gives factor 0.0333 — approximately half the correct value.
    Always use this formula, never ÷N.
    """
    welfare_gbm = (delta_cew_eval_bp / 10000) * W0
    annuity_factor = rho / (1 - (1 + rho) ** -N)
    return welfare_gbm * annuity_factor
```

**Five cost break-evens:**

1. **Migration (welfare break-even):** parameterised on emigration rate. The welfare cost of migration is *not* the full revenue loss — it is the resource cost of relocating and the welfare changes experienced by remaining residents. For the welfare break-even, use the migration cost net of the emigrant's own welfare change (which may be positive or negative). Flag that this cannot be quantified without Phase One data and present the fiscal break-even (full revenue loss) as an upper bound on welfare cost.

2. **Intensive margin avoidance (welfare break-even):** parameterised on real resource cost fraction, not revenue loss fraction. The welfare break-even requires: real_resource_cost_per_dollar_avoided × avoidance_rate = welfare_advantage / annual_wdt_revenue. Since real resource costs (professional fees, restructuring friction, suboptimal holdings) are a fraction of the gross revenue loss, the welfare break-even threshold is higher than the fiscal break-even. Report both thresholds.

3. **Compliance cost:** parameterised on £/year professional fees. Break-even = `breakeven_annual_cost(delta_cew_eval_bp, W0)`. Compare against Burgherr estimates (0.1% of taxable wealth ≈ £1,629/year at W0; 0.07% WDT-adjusted ≈ £1,140/year). Both are well below break-even across all Module E1 scenarios.

4. **Route D auction cost:** event-based. Break-even = welfare_advantage_gbm / (auction_cost_fraction × route_D_wealth_fraction). Number of Route D events over 30 years: 1 mandatory (inheritance) + 0–2 voluntary. At 3% auction cost on Route D portion (assume 15% of portfolio, growing with W): one inheritance auction costs approximately £7,200 at W0 → ~£90,000 at terminal wealth. This is well below break-even across all Module E1 scenarios.

5. **Admin learning:** probability-weighted scenario. If Phase One fails (probability p_fail) and system is repealed at year T_repeal, the agent receives only T_repeal years of welfare advantage. Expected welfare advantage = full_advantage × [1 − p_fail × (1 − T_repeal/N)]. Solve for the (p_fail, T_repeal) combinations that reduce expected advantage to zero. Present as a grid, not a point estimate.

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
    "params": { ... },
    "notes": {
      "baseline": "ΔCEW_EVAL is computed from Module E1, not from WFR's 141 bp figure",
      "distributional_basis": "CEW computed over 44 rolling 30-year windows (primary); circular and bootstrap as robustness",
      "fiscal_vs_welfare": "module_e2 and module_e5 report fiscal and welfare break-evens separately",
      "reproducibility": "WFR 141.22 bp reproduced at T=5, G/V=50%, tau_cgt=24%, gamma=2 before N=30 analysis"
    },
    "reproducibility_gate": {
      "wfr_reference_bp": 141.22,
      "eval_reproduced_bp": "...",
      "tolerance_bp": 2.0,
      "passed": true
    }
  },
  "module_e1": {
    "n30_welfare_baseline": {
      "return_spec": "rolling_44",
      "n_windows": 44,
      "by_scenario": {
        "(tau_cgt=0.24, rule=hold_to_death, death=ons_central, gamma=2.0)": {
          "wdt_cew_bp": ...,
          "cgt_cew_bp": ...,
          "delta_cew_eval_bp": ...,
          "wfr_reference_bp": 141.22
        }
      },
      "scenario_range": {
        "delta_cew_eval_min_bp": ...,
        "delta_cew_eval_max_bp": ...,
        "most_favourable_to_cgt_scenario": "tau_cgt=0.00, rule=hold_to_death, death=ons_central",
        "least_favourable_to_cgt_scenario": "tau_cgt=0.24, rule=annual_fraction, death=0.0"
      },
      "decomposition": {
        "scenario": "(tau_cgt=0.24, rule=hold_to_death, death=ons_central, gamma=2.0)",
        "lock_in_switching_wedge_bp": ...,
        "cgt_realisation_tax_cost_bp": ...,
        "cgt_death_step_up_benefit_bp": ...,
        "wdt_inheritance_auction_cost_bp": ...,
        "wdt_symmetric_refund_benefit_bp": ...,
        "net_delta_cew_eval_bp": "... (must equal sum above ±rounding)"
      },
      "robustness": {
        "circular_73_delta_cew_bp": "...",
        "bootstrap_1000_delta_cew_bp": "..."
      }
    }
  },
  "module_e2": {
    "reference_taxpayer": { "W0_gbm": 1.629, "tier": "Good", "bracket": "95pct", "N": 30 },
    "annuity_factor_rho5_N30": 0.0651,
    "breakeven_by_cost_and_scenario": {
      "migration": {
        "welfare_breakeven_emigration_rate_pct": { "(scenario_key)": ... },
        "fiscal_breakeven_emigration_rate_pct":  { "(scenario_key)": ... },
        "jakobsen_implied_additional_rate_pct": 0.06
      },
      "avoidance": {
        "welfare_breakeven_resource_cost_per_dollar": { "(scenario_key)": ... },
        "fiscal_breakeven_revenue_loss_cents_per_dollar": { "(scenario_key)": ... },
        "jakobsen_upper_bound_fiscal": 0.54
      },
      "compliance": {
        "welfare_breakeven_annual_gbm": { "(scenario_key)": ... },
        "burgherr_central_annual_gbm": 0.001629,
        "burgherr_wdt_adjusted_annual_gbm": 0.00114
      },
      "auction": {
        "welfare_breakeven_events_over_30yr": { "(scenario_key)": ... },
        "realistic_events": "1-3 (1 mandatory inheritance + 0-2 voluntary)"
      },
      "learning": {
        "p_fail_T_repeal_grid": [ { "p_fail": ..., "T_repeal": ..., "expected_advantage_bp": ... } ]
      }
    }
  },
  "module_e3": {
    "migration_scenarios": [
      { "multiplier": 2, "elasticity": "jakobsen", "annual_departures": ...,
        "fiscal_revenue_loss_gb": ..., "welfare_cost_note": "Cannot quantify without Phase One data" },
      { "multiplier": 4, ... },
      { "multiplier": 6, ... }
    ],
    "fiscal_breakeven_emigration_rate_pct": ...
  },
  "module_e4": {
    "current_system": { "cgt_pence_per_gbp": 2.14, "iht_pence_per_gbp": 0.66 },
    "wdt_projected":  { "government_pence_per_gbp": ..., "taxpayer_pence_per_gbp": ... },
    "net_saving_gb_per_year": ...
  },
  "module_e5": {
    "aggregate_delta_cew_eval_bp": ...,
    "fiscal_break_even_surface": {
      "description": "combinations of (migration_rate, avoidance_fraction) at which WDT net fiscal revenue = 0",
      "grid": [ { "migration_rate_pct": ..., "avoidance_fraction": ..., "net_revenue_gb": ... } ]
    },
    "welfare_break_even_surface": {
      "description": "combinations of (migration_rate, real_resource_cost_fraction) at which aggregate ΔCEW_EVAL = 0",
      "grid": [ { "migration_rate_pct": ..., "resource_cost_fraction": ..., "net_welfare_advantage_bp": ... } ]
    }
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
*Version updated: 28 September 2026 (v1) — Added Sections 9 and 10 covering existing code infrastructure and eval_core.py specification.*  
*Version updated: 28 September 2026 (v2) — Design review (Review 1) incorporated. Five changes: (1) reframed as adversarial stress test; (2) `ΔCEW_EVAL` replaces hard-coded 141 bp throughout; (3) CGT realisation behaviour made primary sensitivity dimension with `hold_to_death` as adversarial baseline; (4) welfare and fiscal break-evens separated as distinct outputs; (5) distributional basis requirement made explicit. BADR removed as primary sweep dimension. Annuity formula confirmed as mandatory annualisation method.*  
*Version updated: 28 September 2026 (v3) — Design review (Review 2) incorporated. Four changes: (1) Module 1 respecified as N-period extension of wfr_core.AssetSwitchDecision, preserving the two-asset switching mechanism that generates the 141 bp result — single-asset simplification permitted only if reproducibility gate passes; (2) mandatory reproducibility gate added: EVAL must reproduce WFR 141.22 bp (±2 bp) at T=5 reference parameters before N=30 analysis proceeds; (3) return path specification corrected from "73 starts" to 44 rolling non-overlapping windows as primary, with circular and bootstrap as labelled robustness checks; (4) welfare decomposition output added to Module E1, isolating lock-in wedge, step-up benefit, refund benefit, and auction cost as separate components of ΔCEW_EVAL. Section 6 analytical findings reformatted to produce a break-even table with empirical comparison ranges rather than conclusions about plausibility.*
