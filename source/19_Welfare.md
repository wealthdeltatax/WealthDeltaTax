---
title: "The Wealth Delta Tax: Welfare Comparison Across Tax Systems at Revenue Equivalence"
shortcode: "WFR"
status: "draft"
keywords:
    - Wealth Delta Tax
    - welfare comparison
    - Domar-Musgrave
    - capital gains tax lock-in
    - return heterogeneity
    - revenue equivalence
---

### Revision History {.unnumbered .unlisted}

| Revision | Date          | Details                                      |
|:--------:|:-------------:|----------------------------------------------|
| 0.01     | 13 September 2026 | Initial scaffold. |

\newpage

# Abstract {.unnumbered .unlisted}

[To be written last.]

\newpage

# Glossary {.unnumbered .unlisted}

**Certainty-equivalent welfare (CEW):** The proportional change in consumption under a no-tax counterfactual that would make an agent indifferent to the taxed system. Negative values indicate a welfare cost relative to the no-tax benchmark.

**Delta base:** The annual change in an individual's net worth, net of a cost-of-capital allowance, used as the tax base under the Wealth Delta Tax.

**Domar-Musgrave (D-M) property:** The result that a proportional tax with full symmetric loss offsets contracts the agent's net return distribution without altering relative risk rankings, leaving the risk-taking incentive intact.

**Lifetime contribution envelope:** The mechanism bounding cumulative refunds at cumulative taxes paid by each taxpayer to date, preventing the symmetric refund from operating as open-ended public insurance.

**Lock-in distortion:** The welfare cost arising when a capital gains tax creates a switching wedge between the gross return differential and the after-tax return from realising a position, causing the taxpayer to remain in an inferior asset.

**Long-run reserve (LRR):** The WDT's accumulation vehicle for Phase Two fiscal replacement, funded from post-SRR surplus.

**Revenue equivalence:** The condition under which all systems are calibrated such that the expected tax collected equals the same target as a proportion of initial wealth — here, E[T] = 2% of W₀.

**Short-run reserve (SRR):** The ring-fenced reserve capitalised in the early years of the WDT, which makes the refund guarantee mechanically credible within a single political cycle.

**Symmetric WDT:** A flat-rate variant of the WDT in which the tax rate on gains equals the refund rate on losses.

**Ver. A / Ver. B:** The two return distributions used throughout. Ver. A is the 73-observation UK historical equity return sequence (1950–2022). Ver. B is an idealised two-state distribution with the same mean and standard deviation.

References throughout this paper to (WFR.A §A) through (WFR.A §E) refer to sections of the companion appendix paper, which contains the full simulation tables and model specification underlying the results presented here.

\newpage
\newpage

# 1. Introduction

Most comparisons of tax systems carry a hidden asymmetry: they do not hold revenue constant across systems, do not model the mechanisms through which each system generates welfare costs, and do not test all candidate instruments against the same empirical return distribution. The consequence is that welfare comparisons in this literature tend to conflate the revenue level with the welfare outcome, suppress the structural distortions that generate the largest real-world welfare costs, and omit instruments that do not yet have a large implementation literature. This paper does none of these things.

The comparison is conducted across six systems — flat-rate symmetric WDT, progressive symmetric WDT, income tax, capital gains tax, stock wealth tax, and consumption tax — at genuine revenue equivalence: a numerical solve for E[T] = 2% of W₀ across all systems. The welfare criterion is certainty-equivalent welfare against a common no-tax benchmark, so rankings are directly comparable. Distortions are not suppressed throughout; they are admitted one at a time in a controlled sequence, so that welfare differences can be attributed to specific mechanisms rather than to a bundle of confounded effects. The result is a comparison that is both fair — same revenue burden — and informative — structural welfare costs visible.

The paper closes three confirmed gaps in the existing literature. No prior paper formally extends the Domar-Musgrave risk-sharing framework to a progressive delta base and quantifies the three complications this introduces under a logistic rate schedule. No prior welfare comparison includes the delta base alongside the standard candidates, tested against the same empirical return distribution at revenue equivalence. No prior paper works through the distributional arithmetic of delta-base concentration under persistent return heterogeneity of the type Fagereng et al. (2020) establish — where returns differ persistently across the wealth distribution and these differences compound into concentration over a multi-decade horizon. These gaps are identified as confirmed literature gaps in (LR.A §2.1–2.3). No prior paper closes all three simultaneously, and that simultaneous closure matters: the Domar-Musgrave extension establishes the risk-sharing mechanism; the welfare comparison establishes that the mechanism translates into welfare advantage once distortions are admitted; the concentration result establishes that the same mechanism has distributional implications extending beyond the single-agent frame.

The paper's argument rests on a three-category epistemic taxonomy that must be in place before the results are presented, because it determines what the paper can and cannot claim.

Category 1 findings are welfare costs of existing tax systems established by this model. They do not require the WDT to exist. A reader who rejects the WDT entirely must still account for them.

Category 2 findings are properties of the WDT that follow from the design of the delta base and the symmetric refund, independently of implementation outcomes. They are theoretical results but are not contingent on calibration choices.

Category 3 findings are prospective costs of WDT implementation that are genuine but not currently quantifiable without implementation data.

The taxonomy matters because the standard objection to any welfare case for an unimplemented instrument — "you haven't shown it has no costs" — conflates Category 2 and Category 3. It is correct that Category 3 costs exist and are unknown. It does not follow that they are large, or that they plausibly exceed the Category 1 welfare costs of existing systems that this paper has measured. The paper is precise about this distinction from the outset so that the conclusion follows from the argument rather than from an assertion.

The main results are three. First, a controlled baseline in which all distortions are suppressed shows the flat WDT leading by 17.4 basis points over income tax and CGT — a small advantage establishing fair ground, not a knockout. Second, as mechanisms are admitted, the welfare differences become large: CGT's realisation lock-in imposes a 141–143 basis-point welfare cost once portfolio choice is endogenous, approximately 82 times the baseline difference between systems. Third, stock wealth and consumption taxes allow the Fagereng return differential to compound into 479-fold Great/Poor wealth concentration at the 30-year horizon, versus 286–288-fold for WDT variants and 320-fold for income tax; the relevant axis is accrual basis versus stock base, not flat versus progressive rate.

The paper is a Level 1 contribution. It establishes the theoretical welfare case under controlled conditions and positions the delta instrument in the active theoretical debate. It does not calibrate behavioural responses to the WDT, close the general equilibrium, or produce a quantitative ex-ante welfare estimate under empirically estimated parameters. Each of those tasks is handled by a companion paper. The companion paper EVAL uses empirically calibrated behavioural parameters to produce break-even thresholds for each Category 3 cost, using the welfare advantage this paper establishes as the starting point. (BEHAV) characterises the behavioural shapes and the mild-overstatement equilibrium; (VAL) characterises the valuation architecture and the tolerant zone; (CLOSE) designs the departure settlement mechanism. The argument is stronger for being precise about this boundary, not weaker.

The paper proceeds as follows. Section 2 establishes the comparison design, the three-category taxonomy, and the three comparable-treatment exposures the reader should know about before the results. Section 3 presents the controlled baseline: the single-agent CEW comparison and the Domar-Musgrave risk-sharing result, with the welfare verdict on the latter explicitly deferred. Section 4 admits mechanisms one at a time: progressive rate complications (§4.1), CGT lock-in (§4.2), heterogeneous returns and concentration (§4.3), and stock wealth and consumption tax equivalence (§4.4). Section 5 positions WFR in the existing literature, including the active dispute between Guvenen et al. and Boadway and Spiritus on heterogeneous-return taxation, which WFR enters as a gap-filling rather than side-taking contribution. Section 6 applies the three-category taxonomy to the paper's findings and reaches the burden-of-consideration conclusion. Section 7 identifies the open questions this paper does not resolve. The appendix contains the model specification; the companion appendix paper (WFR.A) contains the full simulation tables.

\newpage

# 2. Methodology

## 2.1 The Comparison Design

Six tax systems are compared throughout: flat-rate symmetric WDT, progressive symmetric WDT, income tax, capital gains tax, stock wealth tax, and consumption tax. Both WDT variants apply symmetric loss refunds — the refund rate in a loss year equals the marginal rate that would have applied to an equivalent gain. The flat variant applies this rate proportionally across all wealth levels; the progressive variant applies it through the logistic schedule described in (RATES §3). All references to "the WDT" without qualification apply to both variants; where the two differ, they are identified explicitly.

The comparison is conducted at revenue equivalence. For each system and each return distribution, the tax rate is solved numerically such that the expected tax collected equals 2% of initial wealth W₀. This condition — E[T] = 2% of W₀ — is held across all six systems simultaneously. Rates therefore differ across systems, because different tax bases collect differently against the same return distribution. The resulting revenue-equivalent rates are reported in (WFR.A §A.3). The income tax rate differential between the two distributions — 32.067% against the empirical distribution versus 33.404% against the idealised distribution — reflects a feature of the comparison that becomes relevant in §3.1 and is explained there.

The welfare criterion is certainty-equivalent welfare (CEW): the proportional change in consumption under a no-tax counterfactual that would make the agent indifferent to the taxed system. Negative values indicate a welfare cost relative to the no-tax benchmark. All six systems are evaluated against the same no-tax benchmark, so rankings are directly comparable. The underlying utility function is CRRA with risk-aversion parameter γ. The central case throughout is γ=2, following (@FlavinYamashita2002) as a commonly used benchmark calibration. A sensitivity sweep across γ=1, 2, and 4 is reported in (WFR.A §A.1); the qualitative rankings are stable across this range.

Two return distributions are used. Ver. A is the 73-observation UK historical equity return sequence covering 1950–2022, with a mean annual return of 10.45% and standard deviation of 8.31% (JST dataset, capital gains only). Ver. B is an idealised two-state distribution constructed to match the same mean and standard deviation. Ver. A is the primary distribution for all results reported in the main text; Ver. B serves as a robustness check and is noted where it diverges meaningfully from Ver. A. The canonical scenario horizon is N=30 years, consistent with the treatment in (VAL), (RATES), and (SWEEPS). This horizon reflects the expected duration of WDT system membership following inheritance-triggered crossing of W_min as the dominant entry mechanism, as established in (RATES §4).

## 2.2 What the Baseline Suppresses — and Why

The comparison proceeds in two stages. The first stage — Part I of the paper — suppresses all behavioural mechanisms and examines what the tax base itself contributes to welfare before distortions are introduced. Specifically, the baseline suppresses portfolio choice, realisation decisions, return heterogeneity across agents, agent heterogeneity in wealth, and all behavioural responses to taxation. This is not a limitation of the model that the analysis works around; it is the design. A comparison that admits all mechanisms simultaneously cannot attribute welfare differences to any of them. The baseline's job is to isolate what the structure of each tax base contributes before the mechanisms that generate the real welfare differences are examined.

The second stage — Part II — admits mechanisms one at a time, in a controlled sequence. Each section in Part II names a mechanism, explains why it is structural to the relevant tax base rather than an artefact of this model, quantifies its welfare consequence, and shows how the WDT responds to it by design. The sequence is: progressive rate complications (§4.1), CGT lock-in (§4.2), heterogeneous agent returns and concentration (§4.3), and the stock wealth and consumption tax equivalence result (§4.4). This ordering is not arbitrary. The progressive rate complications are introduced first because they qualify the D-M result established in §3.2 before that result is used in the lock-in section. The lock-in section comes before the heterogeneous agent section because the envelope-binding result in §4.3 cross-references the Category 2 properties established in §4.2.

The attribution logic of the design is this: when welfare differences are large in Part II and small in Part I, the difference is attributable to the mechanism admitted in that Part II section, not to the tax base considered in isolation, and not to a rigged comparison. Part I's small baseline advantage for the WDT (17.4 basis points over income tax and CGT at canonical parameters) establishes that the WDT does not win through a mechanical rate advantage. Everything that follows in Part II is therefore the consequence of structural mechanisms, not of a comparison designed to favour one system.

## 2.3 The Three-Category Epistemic Framework

The paper makes three epistemically distinct kinds of claims, and it is worth being explicit about the distinction from the outset rather than leaving it to the conclusion.

Category 1 claims are findings about existing tax systems established by this model. They do not require the WDT to exist, let alone to be implemented. A reader who rejects the WDT entirely must still account for Category 1 findings, because they describe systems that currently operate.

Category 2 claims are properties of the WDT that follow from the design of the delta base and the symmetric refund, independently of implementation outcomes. They are theoretical results, not observations of a running system, but they are not contingent on implementation choices. The Domar-Musgrave property of the flat symmetric WDT, the structural absence of realisation lock-in, and the lifetime contribution envelope's bound on refund exposure are all Category 2. They hold wherever the relevant design features hold.

Category 3 claims are prospective costs of WDT implementation that are genuine but not currently quantifiable. Valuation friction under Route D, compliance costs at scale, administrative learning dynamics, migration response, and novel avoidance strategies specific to the symmetric refund are all Category 3. This paper names them explicitly (§6.1.3). It does not pretend they are zero. What it does not do is treat their unknown magnitude as grounds for dismissal — the correct tool for evaluating their magnitude against the Category 1 costs the paper has measured is the break-even analysis of the companion paper EVAL, which is noted at the appropriate point in §6.2.

This taxonomy matters because the standard objection to any welfare case for an unimplemented tax system — "you haven't shown it has no costs" — conflates Category 2 and Category 3. It is correct that Category 3 costs exist and are unknown. It does not follow that they are large, or that they plausibly exceed the Category 1 costs the paper has established for the systems the WDT would replace. The taxonomy structures what the paper can and cannot claim, and that structure should be visible to the reader before the results are presented.

## 2.4 Comparable-Treatment Exposures

Three asymmetries in the comparison design require explicit statement before the results, not in response to a referee.

The first concerns CGT. In the controlled baseline (§3.1), CGT is modelled without a realisation decision — the agent is assumed to realise all gains each period, making CGT structurally identical to income tax. In §4.2, the realisation decision is made endogenous: the agent can choose whether to switch between assets, triggering a CGT liability if they do. This sequencing is methodologically correct — it isolates the tax-base comparison before introducing the dominant CGT distortion, so that the distortion's welfare cost is attributable to the mechanism rather than to initial conditions. The asymmetry is real nonetheless: CGT is examined at its idealised best in the baseline and at a realistic calibration in §4.2, while the WDT is held at its idealised best throughout the main paper. The companion papers (VAL), (BEHAV), and (CLOSE) address the WDT-specific practical costs that this model abstracts away from; the appropriate response to demands that those costs be quantified here is a cross-reference to those papers.

The second concerns the heterogeneous-agent comparison in §4.3. Revenue equivalence is implemented at the aggregate population level, not tier by tier. This is the correct implementation of revenue neutrality in a heterogeneous population — requiring tier-level equivalence would amount to setting a different revenue target for each system based on where the tax falls, not how much it raises. The consequence is that effective burdens differ substantially across tiers under different systems. The tier-level incidence figures are reported in (WFR.A §D.2) for any reader who wants to examine the effective burden distribution directly.

The third concerns income tax and CGT in the baseline. The two systems are welfare-equivalent by construction in the single-period baseline where all gains are realised each period. This does not settle the real-world income tax versus CGT comparison that practitioners care about. It establishes a baseline in which the lock-in distortion is suppressed, so that when it is admitted in §4.2, its isolated welfare cost is visible. The large welfare difference between the two systems in Part II operates entirely through the realisation mechanism — which is itself the result that determines what the policy-relevant choice actually is.

\newpage

# 3. Part I: The Controlled Baseline

## 3.1 Revenue Equivalence and the Single-Agent Baseline

With distortions suppressed, all six systems are compared at γ=2 against the Ver. A distribution. Table 1 reports the results.

**Table 1: Certainty-Equivalent Welfare by System, γ=2, Ver. A**

| System | CEW |
|:---|---:|
| Flat WDT | −1.7539% |
| Income Tax | −1.7713% |
| CGT | −1.7713% |
| Progressive WDT | −1.8288% |
| Stock Wealth Tax | −1.8870% |
| Consumption Tax | −1.8870% |

*CEW relative to no-tax benchmark. Negative values indicate welfare cost. Revenue-equivalent rates in (WFR.A §A.3). Full results across γ=1, 2, 4 and both distributions in (WFR.A §A.1).*

The flat WDT leads by 17.4 basis points over income tax and CGT, and by 133.1 basis points over stock wealth and consumption tax. Neither advantage constitutes a knockout result, and neither is the paper's primary conclusion. The baseline's job is to establish fair ground — to confirm that the WDT does not win through a mechanical rate advantage before any distortions are admitted. The small baseline lead accomplishes this. Everything that follows in Part II is therefore attributable to mechanisms, not to a tilted starting point.

Two structural features of Table 1 require explanation because they recur throughout Part II.

The first is the exact clustering of stock wealth tax and consumption tax at −1.8870% across all values of γ and across both distributions — a result visible in full in (WFR.A §A.1). Both systems apply a fixed proportional wedge to a base that does not condition on return performance. Under CRRA preferences, a fixed proportional wedge leaves the relative consumption distribution unchanged — the ratio of consumption across states is the same with or without the tax — and CRRA scale-invariance then makes the risk-aversion parameter irrelevant. The welfare cost is determined entirely by the revenue extracted, not by how the extraction interacts with return risk. This γ-invariance is a structural property of these two bases, not a coincidence of calibration. It is also the first indication of what the concentration result in §4.3 will show: a tax base that does not condition on return performance does not attenuate the compounding of return differences across taxpayers.

The second is the exact equality of income tax and CGT at −1.7713%. This is correct by construction. In a single-period model where all gains are realised each period, CGT is structurally identical to a gains-only income tax — the two systems apply the same rate to the same base with the same collection timing. The realisation decision that separates CGT from income tax in practice is endogenous, and it is suppressed here. When it is admitted in §4.2, the welfare difference between the two systems becomes the largest in the paper. The baseline equality is therefore not a limitation to be apologised for; it is the controlled condition that makes the lock-in cost in §4.2 attributable to the realisation mechanism alone.

Progressive WDT sits between the two clusters at −1.8288%, 74.9 basis points worse than flat WDT and 58.2 basis points better than the stock-base systems. This intermediate position reflects the logistic rate schedule: at the canonical wealth levels tested here, the logistic is operating near its entry rate τ₀ rather than its ceiling τ_m, so the progressive schedule diverges only modestly from the flat rate. The three complications this introduces to the Domar-Musgrave result are the subject of §4.1.

The organising question these results leave open is this: if structural welfare differences are small when distortions are suppressed, where does the actual welfare cost of existing systems come from? Part II answers this question for each system in turn. The answer, in each case, is a mechanism that the delta base either eliminates by construction or substantially attenuates.

## 3.2 The D-M Risk-Sharing Property: Mechanism Established, Verdict Deferred

@DomarMusgrave1944 establish that a proportional tax with full symmetric loss offsets leaves the agent's optimal risky portfolio share unchanged. The mechanism is this: when the government taxes gains at rate τ and refunds losses at the same rate, it participates proportionally in both the upside and the downside of every risky position. From the agent's perspective, the gross return distribution is contracted by the factor (1−τ) in every state — gains and losses alike. The relative ranking of return states is unchanged, the indifference condition for portfolio allocation is unchanged, and therefore the optimal portfolio is unchanged. Risk-taking is undistorted because the government co-invests proportionally rather than taxing only one side of the distribution.

The flat symmetric WDT is a direct application of this mechanism to a wealth-delta base. The model confirms it holds to floating-point precision. Table 2 reports the Domar-Musgrave test across risk-aversion parameters and both distributions.

**Table 2: Domar-Musgrave Test — Flat Symmetric WDT**

| Distribution | γ | τ | (1−τ)² | Actual ratio | Gap |
|:---|---:|---:|---:|---:|---:|
| Ver. A | 1 | 33.404% | 0.443505 | 0.443505 | −5.55×10⁻¹⁷ |
| Ver. A | 2 | 33.404% | 0.443505 | 0.443505 | −5.55×10⁻¹⁷ |
| Ver. A | 4 | 33.404% | 0.443505 | 0.443505 | −5.55×10⁻¹⁷ |
| Ver. B | 1 | 33.404% | 0.443505 | 0.443505 | 9.44×10⁻¹⁶ |
| Ver. B | 2 | 33.404% | 0.443505 | 0.443505 | 9.44×10⁻¹⁶ |
| Ver. B | 4 | 33.404% | 0.443505 | 0.443505 | 9.44×10⁻¹⁶ |

*Ratio = Var(C_tax) / Var(C_notax). D-M predicts this equals (1−τ)². Gap = actual ratio minus predicted. Gaps are at floating-point precision (10⁻¹⁶ to 10⁻¹⁷). Full specification in (WFR.A §A.4).*

The consumption variance result in (WFR.A §A.2) confirms the mechanism from a different angle. At γ=2, the flat WDT produces Var(C) = 0.0013 — identical across both distributions. Income tax and CGT produce Var(C) = 0.0014 under Ver. A, approximately 8% higher. Stock wealth and consumption tax produce Var(C) = 0.0027, more than double the WDT figure. The WDT contracts the consumption distribution more tightly than any other system at revenue equivalence, and it does so without distorting the relative ranking of return states.

What the D-M result does not say is equally important to state, because the paper's subsequent argument depends on the distinction. D-M is a risk-sharing result. It identifies the channel through which the flat symmetric WDT contracts consumption variance without creating the conventional risk-taking distortion. It does not establish that the WDT produces superior welfare outcomes. Whether the variance reduction translates into a welfare advantage depends on what else is true about the economy — specifically, on what distortions the competing systems impose and whether the WDT introduces distortions of its own that offset the variance benefit. The welfare translation is the subject of Part II. The mechanism is established here; the verdict is deferred.

This sequencing is not merely organisational. @ArachiDAntoni2022 establish that accrual taxation is not automatically welfare superior to realisation taxation, because accrual taxes bill unrealised gains before the taxpayer has liquidity to pay without adjusting consumption. That argument is the primary theoretical objection to any accrual-based tax, and engaging with it requires first establishing what the WDT's risk-sharing mechanism is before showing how the symmetric refund answers the Arachi objection. If the D-M result were presented as a welfare argument rather than a mechanism, the paper would appear to be making exactly the claim Arachi et al. rebut. Section 4.2 shows why the WDT is not subject to that rebuttal — but that argument requires the mechanism established here as its foundation.

\newpage

# 4. Part II: The Mechanisms

## 4.1 Progressive Rates: Three Complications, All Second-Order

A progressive rate schedule breaks the Domar-Musgrave result established in §3.2. The D-M derivation requires a flat proportional rate: the government's co-investment share must be constant across all wealth levels for the contracted return distribution to leave risk rankings unchanged. Under a logistic progressive schedule, the effective rate varies with wealth, so the co-investment share varies too — gains in higher-wealth states are taxed more heavily than equivalent losses at lower post-loss wealth. This introduces three distinct complications to the D-M architecture. All three are real. All three are second-order at canonical parameters across the tested population.

**C1: Progression itself.** The most direct complication is that the progressive schedule applies different effective rates at different wealth levels, breaking the flat co-investment property. The welfare gap between flat and progressive WDT — measured as (CEW_flat − CEW_progressive) × 10,000 — is the quantification of this effect in isolation. At the canonical test wealth of W₀ = £10m (five times the entry threshold), the gap is −0.00 basis points across all γ and both distributions (WFR.A §B.1). The sweep across τ₀, τ_m, k, and W_min in (WFR.A §E.3.1–§E.3.4) confirms the gap remains below 0.05 basis points even at W₀ = £100m under all canonical parameter combinations. The reason is the position of the logistic: at W₀ = £10m with W_min = £2m and k = 0.001, the logistic is operating on the near-flat lower limb well below its inflection point, where effective rates barely differ from τ₀. C1 is a genuine feature of the progressive schedule that would widen at wealth levels far above the inflection point — but across the population this model tests, it is empirically negligible.

**C2: The leverage and net-worth base interaction.** The WDT applies to net worth W = A − D, where A is gross assets and D is outstanding debt. An agent with leverage ratio D/A holds less net worth for a given gross asset position, so the WDT's absolute tax burden is smaller than it would be on the underlying asset return alone. Table 3 reports the welfare gap between the WDT's actual net-worth base and a hypothetical asset-return base across leverage ratios from 0% to 70%.

**Table 3: Leverage Effect on WDT Tax Base and Welfare (Selected Rows)**

| Leverage (%) | W₀ net (£m) | CEW: NW base | CEW: asset-return base | Gap (bp) |
|---:|---:|---:|---:|---:|
| 0.0 | £10.00m | −0.7865% | −0.7865% | +0.00 |
| 20.0 | £8.00m | −0.9501% | −0.9516% | +0.15 |
| 40.0 | £6.00m | −1.1995% | −1.2033% | +0.38 |
| 60.0 | £4.00m | −1.6228% | −1.6306% | +0.78 |
| 70.0 | £3.00m | −1.9602% | −1.9712% | +1.10 |

*Full table in (WFR.A §B.2). Progressive rate function. γ=2. Ver. A distribution. Gross assets = £10m throughout.*

The gap is monotone in leverage, rising from zero at no debt to +1.10 basis points at 70% leverage — the highest ratio tested. Direction is unambiguous and the mechanism is straightforward: as debt rises, net worth falls, reducing the absolute tax liability relative to the asset-return comparator, so welfare under the NW base is marginally higher. This is a genuine complication that would be relevant to a policymaker deciding whether to apply the WDT to gross or net positions. At 1.10 basis points even at extreme leverage, it is second-order relative to the mechanisms in §§4.2–4.3.

**C3: Intertemporal rate asymmetry.** Under a progressive schedule, a gain in period 1 increases wealth and therefore attracts a higher effective rate than the refund received in period 2 on an equivalent loss — because the loss is assessed at the lower post-gain wealth level. This asymmetry is a property of any progressive tax with non-linear rates and gain-loss sequences. Table 4 reports the gain-refund rate differential and the net tax difference relative to the flat WDT benchmark across initial wealth levels.

**Table 4: Two-Period Rate Asymmetry by Initial Wealth**

| W₀ (£m) | τ gain (%) | τ refund (%) | Asymmetry (pp) | Excess vs flat (£m) |
|---:|---:|---:|---:|---:|
| 3.0 | 15.015 | 15.014 | +0.0011 | −0.0532 |
| 10.0 | 15.106 | 15.102 | +0.0037 | −0.1765 |
| 40.0 | 15.498 | 15.483 | +0.0153 | −0.6908 |
| 100.0 | 16.305 | 16.263 | +0.0415 | −1.6488 |
| 200.0 | 17.713 | 17.619 | +0.0946 | −3.0220 |

*Full table in (WFR.A §B.3). Sequence: +18.8% gain period 1, −8.3% loss period 2. Excess = net tax progressive − net tax flat; negative means progressive WDT collects less than flat.*

The asymmetry column confirms the rate differential exists and grows with wealth — from +0.0011 percentage points at £3m to +0.0946 percentage points at £200m. Both magnitudes are small relative to the canonical τ₀ of 15%. The Excess column requires explanation because its sign is counterintuitive. Progression collects *less* net tax than flat across the full wealth range tested — the Excess is uniformly negative. This is not a model error. The wealth levels tested sit in the near-flat region of the logistic, where effective rates are at or just above τ₀, well below the flat revenue-equivalent rate of 33.4%. A progressive schedule that concentrates its higher rates far above the current wealth level — at the logistic ceiling rather than the near-flat entry region — collects less net tax than the flat rate calibrated to the same revenue target, because the progressive schedule barely reaches above τ₀ across the tested distribution. The gain-at-higher-rate asymmetry that textbook treatment of progressive brackets would predict requires wealth to sit at or above the logistic inflection point, which the canonical population does not reach. C3 is a genuine and measurable complication; its direction in the current calibration is not the direction a reader familiar with progressive bracket asymmetry would expect.

All three complications are real features of the logistic progressive schedule, not artefacts of the model. None is large enough to alter the comparative welfare picture. The progressive rate schedule introduces second-order complications that do not materially undermine the D-M risk-sharing architecture — and the mechanisms that do generate large welfare differences are in the sections that follow.

## 4.2 CGT Lock-In: The Dominant Welfare Result

### 4.2.1 The Endogenous Realisation Decision

The baseline comparison in §3.1 showed income tax and CGT at identical welfare levels. That equality holds when the realisation decision is suppressed — when the agent is assumed to sell every period regardless of the tax consequence. In practice, a CGT taxpayer who holds asset A and observes that asset B offers a higher expected return faces a decision the baseline did not model: switching from A to B triggers a CGT liability on the embedded gain, creating a wedge between the gross return advantage of switching (r_B − r_A) and the net return from switching after tax. If the gain-to-value ratio G/V is large enough, or the remaining holding period T is short enough, the tax cost of switching exceeds the benefit of the superior return — and the rational response is to remain in the inferior asset.

This is lock-in. It is not a decision error; it is the rational response to the tax schedule. The CGT creates a wedge between what the asset is worth in the market and what it costs the taxpayer to access a better alternative. The wedge is larger when embedded gains are larger relative to asset value, when the remaining investment horizon is shorter, and when the CGT rate is higher. Each of these dimensions is tested in the sweep results below.

The indifference return r_B* is the minimum return on asset B at which the agent is willing to switch given the CGT liability on the existing position. It is determined by the condition that the net present value of remaining in A equals the net present value of switching to B and paying the CGT on exit. Above r_B*, the agent switches; below it, the agent stays locked in. At the reference calibration (G/V = 50%, T = 5, τ_cgt = 24%, r_A = 10.45%), r_B* = 13.31% — almost three percentage points above r_A. Any asset B offering a return between 10.45% and 13.31% would be preferred to asset A in the absence of CGT but is not worth the switching cost given the embedded liability.

### 4.2.2 The Welfare Cost of Lock-In

Table 5 reports the full welfare comparison between the WDT and CGT once the realisation decision is endogenous.

**Table 5: WDT vs CGT — With and Without Lock-In**

| Metric | Ver. A (Empirical) | Ver. B (Idealised) |
|:---|---:|---:|
| Flat WDT CEW | −1.7539% | −1.7525% |
| CGT CEW (no lock-in) | −1.7713% | −1.7525% |
| Lock-in welfare cost | +141.22 bp | +41.19 bp |
| CGT CEW (with lock-in) | −3.1834% | −2.1644% |
| WDT advantage (no lock-in) | +1.74 bp | +0.00 bp |
| WDT advantage (with lock-in) | +142.96 bp | +41.19 bp |
| P(agent locked in) | 90.0% | 100.0% |
| CGT indifference return r_B* | 13.31% | 13.31% |

*Reference calibration: G/V = 50%, T = 5 years, τ_cgt = 24%, r_A = 10.45%, γ = 2. Full table in (WFR.A §C.3).*

The WDT advantage grows from 1.74 basis points without lock-in to 142.96 basis points with lock-in — approximately 82 times the baseline difference. The mechanism is not a rate advantage: the revenue-equivalent CGT rate is 32.07% against Ver. A versus the WDT's 33.40%. CGT is cheaper at revenue equivalence. The welfare cost arises entirely from the lock-in distortion — the portfolio misallocation the realisation contingency enforces.

The Ver. A and Ver. B results diverge considerably: 142.96 basis points versus 41.19 basis points. This reflects the composition of the empirical return distribution. Ver. A includes genuinely negative return years in which the CGT collects nothing but the WDT provides refunds. These years require a lower revenue-equivalent CGT rate (32.07% versus 33.40%), which reduces the switching wedge slightly — but more importantly, the empirical distribution's fat left tail generates more states in which the agent is locked in to a loss-making position without tax relief, which the WDT's symmetric refund addresses directly. The Ver. B idealised distribution, by smoothing over these states, understates both the lock-in cost and the WDT's revenue-equivalence rate advantage.

**The G/V sweep.** The lock-in cost varies substantially with the embedded gain ratio. Table 6 reports selected rows from the full sweep in (WFR.A §C.1).

**Table 6: Lock-In Welfare Cost by Embedded Gain Ratio (Selected Rows)**

| G/V (%) | Lock-in cost (bp) | P(total locked) | P(CGT distortion) | P(r_B < r_A) |
|---:|---:|---:|---:|---:|
| 5.0 | +16.4 | 86.7% | 0.0% | 86.7% |
| 31.8 | +110.7 | 86.7% | 0.0% | 86.7% |
| 49.7 | +140.4 | 90.0% | 3.3% | 86.7% |
| 67.6 | +142.0 | 93.3% | 6.7% | 86.7% |
| 76.6 | +162.2 | 93.3% | 6.7% | 86.7% |
| 81.1 | +106.9 | 96.7% | 10.0% | 86.7% |

*Full table in (WFR.A §C.1). Ver. A distribution, γ=2, T=5.*

The lock-in cost rises from +16.4 basis points at G/V = 5% to a peak of +162.2 basis points at G/V = 76.6%, then falls non-monotonically above G/V = 81%. The non-monotonicity at high G/V ratios is a discretisation artefact: as r_B* rises with the embedded gain, it approaches the upper boundary of the empirical return distribution, and the probability of any return state exceeding r_B* shrinks rapidly. States that were generating lock-in costs are absorbed into the P(r_B < r_A) category as r_B* crosses above r_A for an increasing share of the distribution. This is a boundary effect of the finite empirical distribution, not a meaningful economic result, and should not be interpreted as evidence that lock-in costs fall at very high embedded gain ratios.

The P-decomposition columns in Table 6 carry a distinction the paper must be precise about. P(total locked) at G/V = 5% is 86.7%, with P(CGT distortion) = 0.0%. That 86.7% reflects states where r_B < r_A — the agent stays in asset A regardless of the CGT because asset B is simply inferior. This is fundamental preference, not a tax distortion. The CGT distortion proper — states where r_A ≤ r_B < r_B* — only begins above G/V = 36.3%, where P(CGT distortion) first registers at 3.3%. At the reference calibration of G/V = 50%, P(CGT distortion) = 3.3% and P(r_B < r_A) = 86.7%. The welfare cost of lock-in at this calibration is attributable to the distortion component — but 86.7% of the total locked-in probability reflects market return states, not the CGT. Conflating the two components would overstate the CGT's role in driving lock-in probability and understate the role of asset return dynamics.

**The T sweep.** Table 7 reports the lock-in cost across holding periods at G/V = 50%.

**Table 7: Lock-In Welfare Cost by Remaining Holding Period (Selected Rows)**

| T (years) | r_B* (%) | Lock-in cost (bp) | P(CGT distortion) |
|---:|---:|---:|---:|
| 1 | 25.51% | +56.1 | 13.3% |
| 2 | 17.74% | +73.3 | 10.0% |
| 5 | 13.31% | +141.2 | 3.3% |
| 8 | 12.23% | +181.1 | 0.0% |
| 20 | 11.16% | +181.1 | 0.0% |

*Full table in (WFR.A §C.2). G/V = 50%, Ver. A distribution, γ=2.*

The lock-in cost rises from +56.1 basis points at T = 1 to a plateau of +181.1 basis points from T = 8 onward. The direction is unambiguously upward across all empirically relevant holding periods. The mechanism: at T = 1, the agent has only one period in which to benefit from switching to asset B, so the opportunity cost of lock-in is relatively low. Each additional year compounds the return advantage of asset B over asset A — the foregone return accumulates. Meanwhile, r_B* converges toward r_A as T grows, because at longer horizons the annualised CGT liability cost per period shrinks and the switching threshold falls toward the gross return indifference level. The plateau from T = 8 reflects the point at which r_B* has fallen below the distribution's resolution: P(CGT distortion) reaches 0.0% because no empirical return state falls in the increasingly narrow wedge between r_A and r_B* — and yet the welfare cost is at its maximum, because the agent has been locked in across many compounding periods at a disadvantage the CGT never fully releases.

### 4.2.3 The Arachi Pivot

@ArachiDAntoni2022, writing in *Fiscal Studies*, establish that accrual taxation is not automatically welfare superior to realisation-based taxation. Their argument: an accrual tax bills unrealised gains before the taxpayer has received the cash to pay without altering consumption. In years when asset values have risen but no sale has occurred, the taxpayer either draws down liquid reserves to meet the liability, adjusts consumption downward, or borrows — all of which create intertemporal consumption distortions that realisation-based taxation avoids. The Arachi objection is the most technically serious theoretical counterargument available to any accrual-based tax proposal, and it must be addressed directly rather than cited in passing.

The WDT is an accrual-based tax. It bills annually on the change in net worth, not on realised gains. The Arachi objection applies — unless the design specifically addresses the mechanism through which accrual creates intertemporal distortions.

The WDT's symmetric refund is that specific address. In any year in which net worth falls, the WDT does not levy a tax; it pays a refund proportional to the loss. The refund is delivered at exactly the moment when the taxpayer's wealth has declined — when liquid reserves are most strained, when consumption pressure is highest, and when the Arachi distortion would otherwise be most acute. The government does not merely collect less in a bad year; it actively transfers purchasing power to the taxpayer when the taxpayer's position has deteriorated. The symmetric refund operates as a direct injection of liquidity at the moment the Arachi mechanism would otherwise force a consumption adjustment.

The WDT is therefore not subject to the Arachi objection as stated. The Arachi critique targets accrual taxes that create consumption distortions in loss years — income tax on unrealised gains, or an accrual wealth tax that levies on appreciation without providing loss relief. Under those systems, a taxpayer who has seen wealth fall still faces a positive tax assessment, which forces a consumption or liquidity decision the tax has imposed. Under the WDT, that taxpayer receives a refund. The distortion runs in the opposite direction to what Arachi describes.

This distinction is not a technicality. It is the structural difference between the WDT and every prior accrual tax proposal. All earlier accrual proposals — the Vickrey averaging system, the Bradford X-tax accrual variant, prior rate-of-return allowance designs — either did not include full symmetric loss refunds or imposed conditions that limited refund access in precisely the years when loss relief is most valuable. The WDT's unconditional symmetric refund, bounded only by the lifetime contribution envelope, is the design feature that makes the Arachi objection inapplicable to the general case.

One qualification is required. The lifetime contribution envelope caps cumulative refunds at cumulative taxes paid by each taxpayer to date (WP §3.5). A taxpayer who enters the WDT in a loss year — before any cumulative tax has been paid — cannot receive a refund, because the envelope floor binds at zero. This is the situation of the Poor tier in the concentration analysis of §4.3, where the envelope binds in the scenario's first year. In that case, the Arachi distortion does apply: the taxpayer faces wealth deterioration without compensating transfer. This is a genuine boundary condition of the design, not a model error. Its policy implication — that the SRR requires capitalisation from non-WDT sources to honour early-year refunds for low-return entrants — is addressed in §4.3. The Arachi objection applies in full to taxpayers for whom the envelope is binding; it does not apply to the general case where a history of positive contributions has accumulated a refund balance.

### 4.2.4 Category Classification

The lock-in welfare cost — 141–143 basis points at the reference calibration under Ver. A — is a Category 1 finding. It is a welfare cost of an existing, operating system: CGT with endogenous portfolio choice. It requires no WDT implementation data. A government that chose to maintain CGT as the default capital taxation instrument after reviewing this analysis would be choosing to accept a welfare cost of this magnitude at plausible UK parameters, relative to any system that does not make the switching decision tax-relevant.

The magnitude is the model's contribution at this calibration and is not claimed to be an externally validated general estimate of CGT lock-in costs. The mechanism is very strongly supported in the existing literature (§5.3). The magnitude depends on G/V, T, τ_cgt, r_A, γ, and the return distribution in ways the sweep results document. What the model establishes is that across plausible UK parameter ranges, the lock-in cost is large — substantially larger than the baseline welfare differences across systems in Part I.

The WDT's structural elimination of lock-in is a Category 2 property. The delta base does not make the switching decision between assets tax-relevant: switching from asset A to asset B changes the future return stream to which the delta base is applied, but does not trigger a realisation event and does not create a switching wedge. Lock-in cannot arise under the WDT by construction, not by calibration. Whether the WDT introduces its own intertemporal distortions through implementation friction, valuation error under Route D, or compliance complexity is a Category 3 question — named in §6.1.3 and not dismissed here.

## 4.3 Heterogeneous Returns: Concentration Under the Fagereng Premise

### 4.3.1 The Fagereng Premise and the Four-Tier Calibration

@FagerengEtAl2020, using Norwegian administrative data covering virtually the entire wealth distribution, establish three properties of individual investment returns that are directly relevant to tax-base design. First, there is substantial within-asset-class return heterogeneity: the gap between the 10th and 90th percentile of individual returns on broadly similar assets is approximately 18 percentage points. Second, returns are positively correlated with wealth level — wealthier individuals systematically earn higher returns than less wealthy individuals holding comparable asset classes. Third, this heterogeneity is highly persistent: an individual's return rank is a strong predictor of their return rank a decade later.

These three properties together — large, wealth-correlated, persistent return differences — have direct implications for how different tax bases interact with wealth concentration over time. A tax base that conditions on return performance will collect more from high-return taxpayers in proportion to their gains; a tax base that conditions on the stock of wealth will collect the same proportion from high- and low-return taxpayers regardless of how differently their wealth is growing. When returns differ persistently and are wealth-correlated, the choice of tax base determines whether the tax system attenuates or compounds the concentration process.

The model uses a four-tier calibration drawn from @FagerengEtAl2020. Tiers are defined by their return differential relative to the UK historical equity mean of 10.45%: Poor (−4.55pp, approximate 95th wealth percentile), Ok (−2.05pp, 99th), Good (+0.95pp, 99.9th), and Great (+3.45pp, 99.99th+). Initial wealth levels are £2.9m, £7.1m, £19.9m, and £139.6m respectively. The 8pp gap between the outer tiers is conservative relative to Fagereng's full 18pp distribution; the concentration results reported here are therefore a lower bound on the effect the Fagereng mechanism would produce at the full empirical return spread.

### 4.3.2 The Concentration Result

Table 8 reports the Great/Poor wealth ratio at five points across the 30-year scenario horizon starting in 2000.

**Table 8: Wealth Concentration Path — Great/Poor Ratio at Key Years**

| System | Initial | 2004 | 2009 | 2019 | 2029 (N=30) |
|:---|---:|---:|---:|---:|---:|
| Flat WDT | 48.8× | 65.1× | 87.4× | 157.2× | 286.3× |
| Progressive WDT | 48.8× | 66.1× | 90.3× | 162.3× | 288.1× |
| Income Tax | 48.8× | 65.5× | 90.2× | 166.1× | 320.2× |
| Stock Wealth Tax | 48.8× | 70.5× | 103.3× | 220.1× | 479.0× |
| Consumption Tax | 48.8× | 70.5× | 103.3× | 220.1× | 479.0× |

*Initial ratio reflects W₀ difference only. All systems calibrated at population-weighted aggregate revenue equivalence. Full series in (WFR.A §D.3).*

The dominant finding is the two-way split at N=30: the relevant axis is accrual basis versus stock base, not flat versus progressive rate. Both WDT variants reach approximately 286–288×; income tax reaches 320×; both stock-base systems reach 479×. The gap between the WDT variants at N=30 is 1.8× — smaller than the gap between either WDT variant and income tax (33–34×), which is itself smaller than the gap between income tax and the stock-base systems (159×).

This is an honest finding and should be stated as such. The progressive rate schedule does not produce meaningfully lower concentration than the flat rate at the canonical 30-year horizon. The Fagereng return differential of +8pp between the Poor and Great tiers dominates the progressive versus flat rate differential at canonical logistic parameters over this horizon: the logistic has not risen far enough above τ₀ to compound a material difference in the effective rate burden between tiers. A longer horizon would eventually reveal the progressive advantage as the logistic rate rises with wealth accumulation, but that horizon is outside the 30-year canonical window. The paper acknowledges this scope limitation rather than suppressing it.

The mechanism driving the 479× outcome for stock-base systems is structural. A stock wealth tax and a consumption tax both levy proportionally on wealth regardless of whether that wealth is generating high or low returns. The Great-tier taxpayer — earning 3.45pp above the mean — and the Poor-tier taxpayer — earning 4.55pp below the mean — pay the same proportional charge on the same stock of wealth each period. Nothing in the tax system attenuates the differential compounding of their returns. The gap therefore compounds at the full Fagereng rate across all 30 years, producing the 479× outcome. The delta base changes this by construction: a poor-return year generates a lower WDT charge or a refund, which reduces the net wealth drain on the low-return taxpayer relative to the high-return taxpayer. The compounding differential is attenuated, not eliminated, which is why the WDT reaches 286× rather than holding concentration constant.

### 4.3.3 Within-Tier Welfare

Table 9 reports CEW by tier and system.

**Table 9: Certainty-Equivalent Welfare by Tier and Tax System**

| System | Poor | Ok | Good | Great |
|:---|---:|---:|---:|---:|
| Progressive WDT | −0.1375% | −0.5004% | −0.9223% | −1.3814% |
| Flat WDT | −0.2194% | −0.7816% | −1.4211% | −1.9269% |
| Income Tax | −0.6000% | −0.9274% | −1.4413% | −1.9161% |
| CGT | −0.6000% | −0.9274% | −1.4413% | −1.9161% |
| Stock Wealth Tax | −1.8424% | −1.8424% | −1.8424% | −1.8424% |
| Consumption Tax | −1.8424% | −1.8424% | −1.8424% | −1.8424% |

*Tier wealth levels: Poor £2.9m, Ok £7.1m, Good £19.9m, Great £139.6m. γ=2, Ver. A. Full table in (WFR.A §D.1).*

The sharpest within-tier result is at the Poor tier. Flat WDT delivers −0.2194% versus income tax's −0.6000% — a gap of 38.1 basis points in the Poor tier's favour under WDT. Progressive WDT widens this to 46.3 basis points. The mechanism is the symmetric refund: the Poor tier's −4.55pp return differential means this tier spends more scenario years in negative-return states than any other. In those years, the WDT pays a refund proportional to the loss; income tax collects nothing but also provides nothing. The asymmetry is income tax's structural property — it participates in gains through collection but does not participate in losses through relief — and it falls hardest on the taxpayer most frequently in loss states.

Progressive WDT provides better welfare than flat WDT at every tier. At the Poor tier, the improvement is 8.2 basis points; at the Great tier it is 54.6 basis points — the redistribution mechanism is working as designed, with the higher logistic rates at the Great tier transferring burden upward and reducing the effective welfare cost for lower tiers. Stock wealth and consumption tax are welfare-equivalent across all tiers at −1.8424%, reflecting the γ-invariance result from §3.1 operating uniformly across the wealth distribution.

### 4.3.4 Distributional Incidence

Table 10 reports expected tax as a percentage of W₀ by tier.

**Table 10: Distributional Incidence — Expected Tax as % of W₀**

| System | Poor | Ok | Good | Great | Great/Poor ratio |
|:---|---:|---:|---:|---:|---:|
| Flat WDT | 0.34% | 0.92% | 1.62% | 2.21% | 6.6:1 |
| Income Tax | 0.68% | 1.05% | 1.63% | 2.19% | 3.2:1 |
| CGT | 0.68% | 1.05% | 1.63% | 2.19% | 3.2:1 |
| Stock Wealth Tax | 1.87% | 1.92% | 1.97% | 2.02% | 1.1:1 |
| Consumption Tax | 1.87% | 1.92% | 1.97% | 2.02% | 1.1:1 |

*E[T]/W₀ × 100. Full table in (WFR.A §D.2).*

The WDT's Great/Poor incidence ratio of 6.6:1 is substantially higher than income tax's 3.2:1, despite both systems being calibrated to the same aggregate revenue target. The mechanism: the WDT's delta base scales with both wealth and the return differential, because the tax applies to net-return × W₀. The Great tier earns 3.45pp above the mean on £139.6m of initial wealth; the Poor tier earns 4.55pp below the mean on £2.9m. The product of wealth and outperformance is highly concentrated at the Great tier, so the delta base collects disproportionately from the highest-return taxpayers. Income tax also collects more from high-return taxpayers, but because it applies to gross gains rather than net returns above a cost-of-capital allowance, the scaling is less pronounced. Stock and consumption tax incidence is near-flat at approximately 1.1:1 — the stock base collects proportionally to wealth regardless of returns, so the wealthier tier pays only slightly more in absolute terms.

A note on the comparison design: aggregate revenue equivalence produces these tier-level differences by construction. The comparison is calibrated so that the same total revenue is raised across the population, not so that each tier pays the same rate. A referee who observes that the WDT's Poor-tier burden is 0.34% against income tax's 0.68% should read this as the consequence of the accrual base: a taxpayer earning 4.55pp below the mean on a modest wealth base generates a small positive or negative delta each year, and the WDT accordingly collects little from them. The tier-level figures are in (WFR.A §D.2) for any reader who wishes to inspect the full effective burden distribution.

### 4.3.5 The Lifetime Contribution Envelope — Binding Result

Table 11 reports the envelope binding status across tiers under flat WDT over the 30-year scenario.

**Table 11: Lifetime Contribution Envelope — Binding Summary**

| Tier | W₀ (£m) | Cumulative tax | Cumulative refund | Min slack | Ever binds? |
|:---|---:|---:|---:|---:|:---:|
| Poor | £2.9m | £0.473m | £0.270m | £0.000m | ⚠ Yes (2001) |
| Ok | £7.1m | £2.440m | £0.398m | £0.042m | No |
| Good | £19.9m | £16.503m | £0.310m | £0.210m | No |
| Great | £139.6m | £330.303m | £1.423m | £2.210m | No |

*Min slack = minimum of (cumulative tax − cumulative refund) over the 30-year window. Zero = envelope exactly reached. Full table in (WFR.A §D.4).*

The Poor tier's envelope binds in 2001 — the first assessment year of the scenario. The Poor tier's −4.55pp return differential produces a loss in the opening scenario year before any cumulative tax has been paid. The refund that would be owed exceeds the cumulative contribution to date, which is zero; the envelope floor binds and the refund is capped at zero. For all other tiers the envelope does not bind across the full 30-year window: the Ok tier's minimum slack is £0.042m, the Good tier's £0.210m, and the Great tier's £2.210m.

The policy implication is specific. The lifetime contribution envelope eliminates SRR solvency risk by construction across the full distribution — refund obligations can never exceed cumulative receipts from any taxpayer whose envelope is not binding. For the small number of taxpayers who enter the system in a loss year with no prior contribution history, the government must either pre-fund the SRR from non-WDT sources or provide an initial credit against future taxes to honour the refund commitment in full. This is a liquidity timing question for the SRR, not a structural funding shortfall: the Poor-tier taxpayer who receives no refund in 2001 will generate positive contributions in subsequent gain years, and the envelope will accumulate slack over time. The result here holds for the 2000-start scenario; the full start-year distribution is in (WFR.A §E.2).

As noted in §4.2.3, this is also the boundary condition under which the Arachi objection applies in full: the Poor-tier entrant in a loss year does not receive the symmetric refund that makes the WDT's accrual structure welfare-superior to realisation-based taxation. This is a genuine scope limitation of the design at the entry margin, not a failure of the mechanism in the general case.

### 4.3.6 The Off-Diagonal Cell

Table D.5 in (WFR.A) reports a spot check that decouples initial wealth from return differential — examining what happens when a Poor-level return differential is applied to Great-level wealth, and vice versa. The "—" entry for Corner B Symmetric WDT (Poor return differential at Great W₀) requires explanation.

TODO: add table footnote to WFR.A §D.5 confirming the following.

At Great-tier initial wealth of £139.6m with the Poor-tier return differential of −4.55pp, the flat symmetric WDT generates expected refunds large enough that the aggregate revenue target cannot be reached within the feasible rate space τ ∈ (0, 0.999]. The revenue-equivalence solver fails to converge: no flat rate applied to this combination of large wealth and persistently negative returns can collect E[T] = 2% of W₀ in expectation, because the refund commitment at any positive rate exceeds the collection in gain states by too wide a margin. This is a solver boundary condition — the parameter combination lies outside the feasible calibration space — not a model failure. The cell is undefined for the flat symmetric WDT; it is not undefined for income tax, CGT, stock wealth tax, consumption tax, or progressive WDT, all of which have solutions in this corner because they either do not pay refunds (income tax, CGT, stock wealth tax, consumption tax) or apply a low enough effective rate at this wealth level (progressive WDT's logistic entry rate) that the revenue target remains reachable.

## 4.4 Stock Wealth and Consumption Taxes: Equivalence and Concentration

The controlled baseline in §3.1 showed stock wealth tax and consumption tax clustered at exactly −1.8870% CEW. Table 8 showed them reaching the same 479× concentration at N=30. Both results have the same explanation, and that explanation is the key to understanding what makes the stock base structurally different from the delta base.

**The welfare equivalence.** Both systems apply a fixed proportional wedge to a base that does not condition on return performance. The stock wealth tax applies a rate to the end-of-period stock of wealth; the consumption tax applies a rate to the flow of consumption, which in this model equals wealth growth net of the tax. In a single-period model with no labour income, no heterogeneous saving, and no liquidity constraints, these two bases produce the same proportional compression of the consumption distribution across all return states. CRRA scale-invariance then makes the risk-aversion parameter irrelevant: if the relative distribution of consumption across states is unchanged by the tax, the welfare cost is determined entirely by the revenue extracted and not by how that extraction interacts with return risk. The γ-invariance identified in §3.1 is the signature of this property — it holds across γ=1, 2, and 4 without exception, and it holds across both return distributions, because neither the flat proportional wedge nor the return distribution changes with γ.

This equivalence is a model-structural property, not a general claim about the two systems in practice. It breaks as soon as the model's simplifying assumptions are relaxed. Labour income changes the consumption-expenditure identity and separates consumption tax from wealth tax incidence. Heterogeneous saving rates mean that a stock wealth tax and a consumption tax fall on different bases for the same taxpayer. Liquidity constraints create a wedge between the two systems in years when the consumption tax would require drawing down non-liquid wealth. Life-cycle structure introduces age-specific consumption patterns that interact differently with the two bases. The equivalence is presented as what it is: a clean theoretical result under specific conditions, not a policy finding about the two systems' real-world comparability.

**The concentration equivalence and its mechanism.** The 479× result for both systems at N=30 is a Category 1 finding. Both stock-base systems reach exactly this ratio under the four-tier Fagereng calibration because the mechanism is the same for both: a tax that levies proportionally on wealth regardless of return performance provides no attenuation of the compounding of return differences across taxpayers. The Great-tier taxpayer earns 3.45pp above the mean every period; the Poor-tier taxpayer earns 4.55pp below the mean every period. The stock wealth tax and the consumption tax both apply the same proportional charge to the same stock of wealth each period — neither conditions on the difference between the taxpayer's return and any cost-of-capital benchmark. The full 8pp return differential therefore compounds unattenuated across all 30 years, producing 479× from an initial 48.8×.

This is the structural property the delta base eliminates by construction. The WDT's tax base is the change in net worth net of a cost-of-capital allowance — it taxes the return in excess of the benchmark, not the stock. A Poor-tier year in which net worth falls generates a refund, reducing the wealth drain on the low-return taxpayer. A Great-tier year in which net worth rises substantially generates a large positive tax. The differential between the two compounds more slowly under the delta base than under the stock base because the tax system is participating asymmetrically: taking more from the high-return taxpayer and giving back to the low-return taxpayer in proportion to the return differential, rather than treating both identically on the stock they hold.

The 479× versus 286–288× contrast between stock-base and delta-base systems is the concentration mechanism stated in numbers. It is a Category 1 finding for the stock-base systems — a welfare cost of existing systems established without requiring WDT implementation data — and a Category 2 property of the delta base: the attenuation follows from the structure of the tax base, not from any implementation choice.

\newpage

# 5. Part III: Literature Positioning

## 5.1 Domar-Musgrave and Risk-Sharing

@DomarMusgrave1944 establish the risk-sharing result for proportional taxation with symmetric loss offsets in the *Quarterly Journal of Economics*. Their mechanism is simple: when the government taxes gains and refunds losses at the same rate, the investor's after-tax return distribution is contracted proportionally — upside and downside alike — without altering relative risk rankings. A risk-averse investor who was willing to hold a volatile asset before the tax remains willing to hold it after, because the reduction in expected return is matched by an equivalent reduction in variance. @Sandmo1977 confirms the same mechanism from a portfolio equilibrium starting point, finding that asymmetric tax treatment penalises variance directly: where losses receive no equivalent relief, investors face rising effective costs of volatile positions and underinvest in risky assets relative to what their risk-adjusted returns justify. @Stiglitz1969 formalises the conditions under which proportional taxation with full loss offset can leave the optimal risky portfolio share unchanged, and @King1977 extends the analysis to show that asymmetric loss treatment raises the cost of capital for risky projects across the investment universe.

The flat symmetric WDT is a direct application of the Domar-Musgrave mechanism to a net wealth delta base. The mechanism holds wherever the rate is proportional and refunds are symmetric, so the floating-point confirmation in §3.2 is not a calibration result but a verification that the design satisfies the mathematical conditions the D-M tradition identifies. This can be stated with confidence.

The settled question is the risk-sharing mechanism; the open question is the welfare translation. Domar and Musgrave do not show that symmetric taxation produces superior welfare outcomes — they show that it avoids a specific distortion. Whether avoiding that distortion translates into welfare advantage depends on what else is true about the economy and what distortions the competing systems introduce. That translation is the subject of Part II.

## 5.2 Progressive Taxation and Risk Asymmetry

@Vickrey1939 identifies the rate asymmetry problem for progressive income averaging: if gains fall into a higher bracket than the one at which equivalent losses are refunded, a nominally symmetric system discriminates against risk-taking even with full loss offsets. The mechanism operates wherever a progressive schedule interacts with gain-loss sequences, and it applies to the WDT's logistic rate function. Section 4.1 reports the quantification of this effect under the specific WDT schedule: rate differentials ranging from +0.0011 percentage points at £3m to +0.0946 percentage points at £200m, with Excess uniformly negative across the tested range because the canonical population sits in the near-flat entry region of the logistic well below the inflection point. The direction of the effect is literature-supported; the magnitude and the counterintuitive negative Excess result — progressive WDT collecting less net tax than flat across the tested sequence — are this paper's contributions at these parameters. Vickrey's diagnosis applies; his predicted direction requires the population to be operating on the steeply progressive limb of the rate schedule, which the canonical calibration does not reach.

## 5.3 CGT Lock-In: Literature and Model Contribution

The welfare cost of realisation-based capital gains taxation has a long analytical record. The mechanism is standard: by making realisation the taxable event, CGT allows unrealised appreciation to accumulate without tax but imposes a switching cost on any taxpayer who holds an embedded gain and wants to move to a superior asset. The International Monetary Fund and the OECD have documented the resulting portfolio rigidity across multiple country studies; the OECD's 2025 analysis of capital gains tax design explicitly identifies lock-in as the primary efficiency cost of realisation-contingent systems (@OECD2025).

The empirical literature confirms the mechanism is real and economically significant at the magnitudes the model implies. Studies of portfolio reallocation behaviour consistently find that taxpayers with large embedded gains in appreciated assets hold them longer and switch less frequently than portfolio theory would predict in the absence of tax — and that this divergence from unconstrained behaviour is correlated with the size of the embedded gain and the prevailing CGT rate in ways that are not explained by information or transactions costs alone. This body of evidence supports the causal interpretation that the realisation rule is generating the observed rigidity.

WFR's specific modelling contribution is the P(locked in) decomposition in (WFR.A §C.1): separating states where the agent does not switch because asset B is simply inferior to asset A from states where the agent does not switch despite asset B being superior because the embedded CGT liability makes switching irrational. At the reference calibration (G/V = 50%), 86.7% of locked-in probability reflects market return states where r_B < r_A — the agent stays because the alternative is worse, not because the tax has distorted the decision. The CGT distortion proper, P(CGT distortion), first appears above G/V = 36.3%. A paper that read the headline P(total locked) as a measure of tax distortion would overstate the CGT's contribution to lock-in and understate the role of asset return dynamics. This distinction is not made in the empirical portfolio literature, which has not decomposed lock-in probability in this way.

The 141–143 basis-point welfare cost at the reference calibration is the model's result at the stated parameters. It is not an estimate of the general welfare cost of CGT lock-in in the UK economy, and the paper does not present it as such. The mechanism producing the estimate is very strongly supported in the existing literature. What the model establishes is that across plausible UK parameter ranges — the G/V and T sweeps in (WFR.A §C.1–§C.2) — the welfare cost is large relative to the baseline differences between systems in Part I.

The Arachi objection requires direct treatment here because it is the strongest available counterargument to any accrual-based taxation proposal, and WFR's case for the WDT is a case for accrual taxation. @ArachiDAntoni2022, in *Fiscal Studies*, establish that accrual taxation is not automatically welfare superior to realisation-based taxation. Their argument is that an accrual tax bills unrealised gains before the taxpayer has received cash from those gains, creating an intertemporal consumption distortion in years when wealth has appreciated but nothing has been sold: the taxpayer must either draw down liquid reserves, borrow, or reduce consumption to meet the assessment. This objection applies to any accrual proposal that does not specifically address the intertemporal distortion mechanism — income tax on unrealised gains, or an annual net wealth tax with no loss relief. Section 4.2.3 establishes that the WDT is not subject to the Arachi critique as stated, because the symmetric refund restores consumption capacity in exactly the years when the Arachi distortion would otherwise be most acute. The point is made there and need not be repeated at length here; it is placed in the literature positioning section to confirm that the paper has engaged with the methodological caution Arachi et al. raise, and that the engagement is structural rather than rhetorical.

## 5.4 Heterogeneous Returns and Concentration

@FagerengEtAl2020, in *Econometrica*, provide the empirical foundation for the heterogeneous-returns analysis in §4.3. Their Norwegian administrative dataset establishes three properties: persistent individual-level return heterogeneity with a cross-sectional standard deviation of approximately 8 percentage points; substantial year-to-year autocorrelation within individuals that survives controls for portfolio composition, confirming that the dispersion reflects individual characteristics rather than transient luck; and a positive correlation between wealth level and financial asset returns of approximately 3 percentage points between the 10th and 90th percentile of the wealth distribution, even within asset classes. A companion paper in the American Economic Review (Papers and Proceedings, 2016) establishes the same persistence properties using a slightly different sample definition.

WFR's four-tier calibration draws conservative parameters from this evidence — an outer-tier return differential of approximately 8 percentage points against Fagereng's observed 18-percentage-point 10th-to-90th percentile gap. The 479-fold concentration result for stock-base systems at N = 30 is therefore a lower bound on what the full Fagereng heterogeneity would produce. WFR's specific modelling contribution is the multi-decade concentration path: asking not what return heterogeneity implies at a point in time but what it implies when different tax bases either attenuate or fail to attenuate the differential compounding of persistent return differences across taxpayers. This question has not been formally examined in the existing concentration literature, which has focused on cross-sectional incidence and short-run distributional effects rather than on the dynamic interaction between persistent return heterogeneity and tax base design over investment horizons.

## 5.5 The Active Dispute WFR Enters — and Does Not Adjudicate

A live dispute in the academic literature directly frames the comparison WFR conducts, and WFR's relationship to that dispute requires precise statement.

@GuvenonEtAl2023, in the *Quarterly Journal of Economics*, formalise the efficiency case for a stock wealth tax over capital income taxation when returns are persistently heterogeneous. Their use-it-or-lose-it mechanism: capital income taxation concentrates the burden on productive investors who earn high returns, penalising efficient capital deployment, while a stock wealth tax falls equally on all holders of equivalent wealth regardless of return, shifting the burden toward unproductive holders and encouraging capital to concentrate with investors who earn more from it. Their model, calibrated to US data, finds a welfare gain of approximately 8% in consumption-equivalent terms from replacing capital income tax with a revenue-neutral stock wealth tax.

Boadway and Spiritus (2025, *Economic Journal*) reach the opposite conclusion from the same premise. When individuals earn persistently heterogeneous returns, they argue, positive capital income taxation can be Pareto-efficient and the optimal rate rises with the degree of return heterogeneity — the case for taxing capital income strengthens, rather than weakens, as return dispersion increases. Their mechanism: heterogeneous returns imply that the planner can use capital income taxes to redistribute toward low-return individuals without distorting the margin that matters, because the productive investor's return advantage is in part a rent that taxation can extract. The Guvenen and Boadway-Spiritus papers reach directly opposing welfare conclusions from the same empirical premise and represent an unresolved dispute at the frontier of optimal taxation under return heterogeneity.

WFR does not adjudicate this dispute. Neither paper includes a delta-based accrual tax as one of the instruments under comparison: both Guvenen et al. and Boadway and Spiritus confine their comparison to stock wealth tax and capital income tax. WFR introduces the delta instrument into a comparison that has been conducted across only two alternatives, which is a gap-filling contribution rather than a side-taking one. The delta base is neither a stock wealth tax nor a capital income tax: it taxes the annual change in net worth above a cost-of-capital allowance, which means a productive entrepreneur whose wealth is stable pays nothing under the delta base even if their return is high and their stock is large. Whether this property strengthens or weakens the Guvenen use-it-or-lose-it mechanism, or changes the conditions under which the Boadway-Spiritus optimality result holds, cannot be determined within the partial equilibrium framework of this paper. That analysis is the substance of a Level 2 general equilibrium extension, noted as an open question in §7.2.

Dalle Luche, Garbinti, and Goupille-Lebret (2026, *Review of Income and Wealth*) extend the analysis to joint heterogeneity in wealth and returns at the top of the distribution, finding that increasing returns to wealth at the upper tail have implications for optimal tax design that the Guvenen and Boadway-Spiritus frameworks do not fully capture. Their paper is the most recent statement of the frontier question WFR sits adjacent to. WFR's contribution is to position the delta instrument in this frontier debate, not to resolve a dispute the frontier has not resolved.

The text the paper should not contain follows from this framing. WFR cannot claim that the literature establishes accrual taxation as superior to capital income taxation when returns differ: the dispute is live and the paper has no basis for adjudicating it within its partial equilibrium scope. What the paper can claim — and does — is that the existing dispute has been conducted without the delta instrument and that WFR introduces it.

## 5.6 Stock Wealth and Consumption Tax Equivalence

The welfare equivalence of stock wealth taxes and consumption taxes in simple lifecycle models is a well-established theoretical result. @BastaniWaldenstrom2020, in the *Journal of Economic Surveys*, survey the terrain of capital taxation design and confirm the conditions under which stock wealth tax and consumption tax produce equivalent welfare implications: no labour income, proportional bases, a uniform saving rate, no liquidity constraints, and CRRA preferences that make the relative consumption distribution invariant to the level of proportional taxation. The IMF's (2024) analysis of wealth tax design provides further institutional confirmation of the equivalence and the conditions under which it breaks.

WFR's contribution on this point is the exact numerical confirmation at both welfare (−1.8870% for both systems across all γ values) and concentration (479× for both at N = 30). The exact equivalence is a model-structural property, not a coincidence of calibration. It holds because both systems apply a fixed proportional wedge to a base that does not condition on return performance, and CRRA scale-invariance makes the welfare result independent of risk aversion. The same independence from γ that produces the welfare equivalence also explains the concentration equivalence: neither system attenuates the Fagereng return differential between taxpayers, so both allow the full 8-percentage-point differential to compound unattenuated across the 30-year horizon.

The paper is precise about where the equivalence breaks. It is a model-structural property under specific simplifying assumptions — single period, no labour income, no heterogeneous saving, no liquidity constraints, no life-cycle structure. Each of these assumptions, when relaxed, creates a wedge between the two systems. A consumption tax and a stock wealth tax produce different effective burdens as soon as households earn labour income (which enters the consumption base but not the wealth base), save at different rates (which changes the stock base faster for high savers), or face liquidity constraints (which the stock wealth tax can trigger in a way a consumption tax assessed on expenditure does not). The equivalence result is presented as what it is — a clean finding under controlled conditions — and not as a claim about the two systems' real-world comparability.

## 5.7 Literature Summary

Table 11 maps WFR's main findings against the literature on which they rest and states the drafting basis for each claim — what can be asserted confidently because the literature establishes it versus what is the model's contribution at this calibration.

**Table 11: Literature Map**

| WFR finding | Literature basis | Drafting note |
|:---|:---|:---|
| Flat symmetric WDT satisfies Domar-Musgrave | @DomarMusgrave1944; @Sandmo1977; @Stiglitz1969; @King1977 | Confident assertion — WFR verifies that the delta base satisfies the mathematical conditions the D-M tradition identifies |
| D-M is a risk-sharing result, not a welfare-superiority result | @DomarMusgrave1944 (scope of original result) | Confident assertion — the limitation is explicit in D-M; WFR restates it as framing discipline |
| Progressive schedule breaks D-M; three complications all second-order at canonical parameters | @Vickrey1939 for the underlying rate-asymmetry problem; magnitude is WFR's own | Model contribution — direction literature-supported; magnitude and the negative Excess result are this model's findings at this calibration |
| CGT lock-in is real and large at plausible parameters | @OECD2025 and empirical portfolio literature for the mechanism; magnitude is WFR's own | Model contribution — the 141–143 bp figure is WFR's at stated parameters; the mechanism and its empirical relevance are strongly literature-supported |
| P(locked in) decomposition distinguishing CGT distortion from market preference | Not previously made in this form | WFR contribution |
| Arachi objection does not apply to WDT | @ArachiDAntoni2022 for the objection; WFR's structural response is its own | WFR contribution — the paper is the first to engage with this objection at the design level for a symmetric-refund accrual tax |
| Fagereng return heterogeneity is persistent, large, and wealth-correlated | @FagerengEtAl2020 | Confident assertion — WFR uses their parameter estimates directly |
| 479× Great/Poor concentration for stock-base systems at N = 30 | Mechanism follows from @FagerengEtAl2020 applied to stock base; the multi-decade simulation is WFR's | Model contribution — the concentration path is WFR's simulation at Fagereng parameters |
| Delta base attenuates concentration; accrual vs stock is the relevant axis at N = 30 | Mechanism is WFR's; the Fagereng foundation is established | Model contribution |
| Stock wealth tax and consumption tax are welfare-equivalent in the model | @BastaniWaldenstrom2020 and IMF (2024) for the general conditions; numerical confirmation is WFR's | Confident assertion for the equivalence conditions; model contribution for the exact numerical confirmation |
| WFR does not adjudicate Guvenen vs Boadway-Spiritus | @GuvenonEtAl2023; Boadway and Spiritus (2025) | Framing statement — the paper's gap-filling position relative to a live dispute |

# 6. Part IV: Synthesis and Conclusion

## 6.1 What the Model Establishes and What It Does Not

### 6.1.1 Category 1: What We Know About Existing Systems

The model has established four findings about existing tax systems under controlled conditions at revenue equivalence. None of these findings requires the WDT to exist. A reader who rejects the WDT entirely must still account for them, because they describe systems that currently operate.

*CGT lock-in imposes a welfare cost of 141–143 basis points at the reference calibration.* Once portfolio choice is endogenous and the realisation decision is modelled, CGT produces a switching wedge that costs the agent 141.22 basis points of CEW at the reference calibration (G/V = 50%, T = 5, τ_cgt = 24%, Ver. A, γ=2) — growing to 162.2 basis points at G/V = 76.6% and reaching a plateau of 181.1 basis points from T = 8 years onward. The mechanism — the realisation contingency creating a wedge between the gross and net return from switching — is textbook and very strongly supported in the empirical literature. The magnitude is this model's contribution at this calibration.

*Stock wealth and consumption taxes produce 479-fold Great/Poor concentration at the 30-year horizon under Fagereng-calibrated return heterogeneity.* Both stock-base systems levy proportionally on wealth regardless of return performance, leaving the full 8pp Fagereng differential to compound unattenuated across 30 years. This is a structural property of the stock base, not a calibration artefact: any system that conditions the tax on the stock rather than the return performance will produce the same mechanism, and the 479× outcome is its consequence at the Fagereng parameterisation.

*Income tax produces 320-fold concentration at the same horizon.* Income tax conditions on gains but not on a net-return benchmark, so the gross Fagereng differential compounds without attenuation below the cost of capital. The result is worse than both WDT variants (286–288×) but substantially better than the stock-base systems (479×). The relevant comparison axis at N=30 is accrual basis versus stock base, not flat versus progressive rate.

*Income tax and CGT are welfare-equivalent when the realisation rule is suppressed.* The large real-world divergence between income tax and CGT operates entirely through the lock-in mechanism. This means the realisation rule — not the rate, not the base considered in isolation — is the welfare-relevant policy choice when comparing the two systems. A reform that moved from CGT to income tax without eliminating the realisation rule would not capture the welfare gain the model attributes to eliminating the lock-in distortion.

### 6.1.2 Category 2: What We Know About the WDT Without Implementation Data

The model has established five properties of the WDT that follow from the design of the delta base and the symmetric refund, independently of any implementation outcome. These are theoretical results, but they are not contingent on calibration choices.

*Flat-rate symmetric WDT satisfies Domar-Musgrave to floating-point precision.* The government participates proportionally in both gains and losses across all return states, contracting the net return distribution by the factor (1−τ) without altering relative risk rankings. This holds at γ=1, 2, and 4 and across both return distributions. It is a structural consequence of the flat rate combined with full symmetric refunds, not a feature of this particular calibration.

*The WDT eliminates realisation lock-in by construction.* The switching decision between assets is not tax-relevant under the delta base: changing from asset A to asset B changes the future return stream the delta base is applied to, but does not trigger a realisation event and does not create a switching wedge. Lock-in cannot arise under the WDT by construction. This is a Category 2 property — it follows from the tax base design, not from any implementation choice.

*The lifetime contribution envelope eliminates SRR solvency risk by construction.* Refund obligations are bounded at cumulative receipts from each taxpayer. The envelope is not a limitation on the symmetric refund's welfare properties for taxpayers with positive contribution histories; it is the mechanism that makes the refund commitment financially sustainable without pre-funding the full potential refund exposure. The boundary condition — where the envelope binds for early entrants in loss years — is a liquidity timing question for SRR capitalisation, not a structural funding shortfall.

*The WDT is more progressive in incidence than income tax under heterogeneous returns.* The delta base scales with both wealth and return differential, while income tax scales with gains only. The Great/Poor incidence ratio is 6.6:1 for the flat WDT versus 3.2:1 for income tax, despite identical aggregate revenue targets. This is a structural consequence of the accrual base under Fagereng-style return heterogeneity.

*The symmetric refund delivers disproportionate welfare benefit to low-return taxpayers.* The Poor tier — most frequently in loss states — receives the symmetric refund in the years when it is most needed. The WDT advantage at the Poor tier is 38.1 basis points over income tax under the flat rate and 46.3 basis points under the progressive rate. Income tax's structural asymmetry — participating in gains through collection but not in losses through relief — falls hardest on the taxpayer who spends the most time in loss states.

### 6.1.3 Category 3: What We Do Not Know

The following are genuine prospective costs of WDT implementation. They are real, not hypothetical. This paper does not claim they are zero or small. It claims that their magnitude is not currently determinable and that a break-even analysis — the contribution of the companion paper EVAL — is the correct tool for evaluating whether any of them plausibly exceeds the Category 1 welfare costs the paper has established.

*Valuation friction under Route D.* The four-route valuation architecture (VAL) is designed to minimise friction by making declared values the legally operative basis rather than requiring state-certified assessments. The empirical friction cost under real-world implementation — administrative load, professional fees, contested declarations, auction proceedings — is not quantifiable without implementation data.

*Compliance and avoidance costs at scale.* (BEHAV) establishes theoretical stability of the mild-overstatement equilibrium (α ≈ 1.1–1.5) and characterises the nine behavioural shapes from full compliance to active resistance. It does not establish the empirical compliance cost that HMRC-level implementation would generate, nor the avoidance cost at the population level once Shapes 4–6 (restructuring, timing manipulation, cross-border asset migration) are active.

*Administrative learning dynamics.* The speed at which an administering body develops operational competence with the Route D auction process, the declaration review system, and the settlement architecture has no direct empirical analogue. The cost of the learning period — in errors, delays, and contested assessments — is a real implementation cost that Phase One is designed to generate data on (PHASE1 §2).

*Migration response.* @JakobsenEtAl2020 and @AgrawalEtAl2025 provide calibration ranges from existing wealth taxes, but WDT-specific migration dynamics are untested. The cross-base externality identified by @AgrawalEtAl2025 — income and VAT losses approximately six times the direct wealth-tax revenue loss — is the dominant empirical qualification on all pre-behavioural revenue figures in this paper and in (RATES). Its magnitude under WDT-specific conditions is a Phase One measurement priority (PHASE1 §3).

*Novel avoidance strategies specific to the symmetric refund.* The mild-overstatement equilibrium (ENV §2) is the settled equilibrium for the declaration game under canonical parameters. Avoidance strategies specific to the symmetric refund — engineered losses to maximise refund exposure, basis manipulation to time loss recognition, cross-asset structuring to shift returns into refund-eligible periods — are prospective. Their magnitude depends on the legal architecture, enforcement capability, and the Rule D auction's deterrent effectiveness, all of which are Phase One questions.

## 6.2 The Comparative Question

The welfare comparison between existing systems and the WDT cannot be resolved by observing that the WDT has not been implemented. That observation establishes that Category 3 costs are unknown — it does not establish that they are large, or that they exceed the Category 1 costs the paper has measured for the systems the WDT would replace.

The correct question is this: *are the Category 3 prospective costs of WDT implementation plausibly larger than the Category 1 welfare costs of the systems WDT would replace?*

Administrative familiarity does not answer this question. Administrative familiarity establishes that existing systems are known quantities and the WDT is not — it says nothing about the relative magnitude of their welfare costs. The CGT's 141–143 basis point lock-in cost and the stock wealth tax's 479× concentration path are not reduced by the fact that those systems are familiar. They are properties of the systems themselves that this model has made visible.

The break-even framing translates the question into tractable form. Starting from the 141–143 basis point lock-in welfare advantage of the WDT over CGT, the question becomes: how large would each Category 3 cost have to be, individually, to offset that advantage? If the break-even for migration requires, for example, 40% of assessed taxpayers to exit the jurisdiction — far outside the range of any empirical wealth-tax response in the existing literature — then migration cannot plausibly explain away the welfare advantage, regardless of the uncertainty about its precise magnitude. If a break-even threshold falls within a plausible empirical range, that identifies a genuine uncertainty that requires resolution before the comparison can be settled.

This is EVAL's primary contribution. WFR establishes the welfare advantage that question must contend with. The language appropriate to this paper's scope is: whether any Category 3 implementation cost plausibly exceeds the 141–143 basis point welfare advantage is the question EVAL is designed to answer. WFR provides the welfare baseline EVAL's break-even analysis will use as its starting point.

## 6.3 The Burden-of-Consideration Conclusion

Once tax systems are compared on their welfare consequences rather than on their administrative familiarity, the WDT cannot reasonably be dismissed without addressing the mechanisms this paper has identified and quantified.

The mechanisms are four, and each is actionable.

*Symmetric risk participation.* The delta base with symmetric refund satisfies the Domar-Musgrave risk-sharing condition by construction, contracting the agent's consumption variance below the level of every alternative system at revenue equivalence. No existing system in the tested set shares this property. The mechanism is structural — it follows from the proportional co-investment design — and is not a calibration-dependent result.

*Structural elimination of realisation lock-in.* CGT with endogenous portfolio choice imposes a welfare cost of 141–143 basis points at the reference calibration, approximately 82 times the baseline welfare difference between systems. This cost is eliminated by construction under the WDT because the tax base does not make the switching decision tax-relevant. The primary theoretical objection to accrual taxation — the Arachi intertemporal consumption distortion in loss years — is specifically addressed by the symmetric refund, which restores consumption capacity at the moment it is most needed. The WDT is not a conventional accrual tax; it is an accrual tax that structurally answers the principal welfare objection to accrual taxation.

*Concentration moderation under persistent return heterogeneity.* At the 30-year canonical horizon, WDT variants reach 286–288× Great/Poor concentration versus 320× for income tax and 479× for stock wealth and consumption tax. The split is accrual versus stock base, not flat versus progressive. The delta base's conditioning on net return above a cost-of-capital benchmark attenuates the compounding of the Fagereng return differential that produces the 479× outcome under stock-base systems.

*Progressive incidence from the accrual base.* The WDT is more progressive in incidence than income tax — a 6.6:1 Great/Poor ratio versus 3.2:1 — because the delta base scales with both wealth and return differential. The symmetric refund delivers disproportionate welfare benefit to the low-return tier, which spends the most time in loss states.

A dismissal of the WDT on welfare grounds would have to establish one or more of the following. First, that the CGT lock-in mechanism does not operate as the model and the empirical literature describe — a position that runs against a large body of evidence on portfolio reallocation and realisation behaviour. Second, that persistent return heterogeneity does not interact with the stock base to produce concentration paths of the magnitude the model shows — a position that requires rejecting the Fagereng findings or their implication for multi-decade compounding. Third, that the Category 3 prospective costs of WDT implementation plausibly exceed 141–143 basis points — the current Category 1 welfare cost of CGT lock-in that the WDT eliminates by construction — without identifying which cost would produce a break-even at a plausible empirical magnitude. Fourth, that some welfare cost of the WDT not identified or measured in this paper is large enough to reverse the comparison.

Each of the first two runs against the empirical literature. Neither the third nor the fourth can currently be established, because WDT has not been implemented — but the absence of an empirical estimate of WDT-specific costs is not evidence that those costs are large. It is evidence that EVAL's break-even analysis is the right next step, and that the burden of justification has shifted.

This paper does not claim the WDT is the optimal tax system. It establishes that the welfare case is coherent, that it rests on mechanisms independently well-evidenced, and that the principal welfare objection to accrual taxation is structurally answered by the WDT's symmetric design. A decision to maintain CGT or a stock wealth tax as the default is, after this analysis, a decision to accept known welfare costs. That decision may ultimately be defensible — on grounds that EVAL and PHASE1 will investigate. It cannot be defended on welfare grounds without engaging with the mechanisms this paper has measured.

\newpage

# 7. Open Questions {.unnumbered}

## 7.1 Behavioural Calibration

This paper is pre-behavioural throughout. All results assume agents respond to tax incentives only through the mechanism being tested in each section — the realisation decision in §4.2, the portfolio allocation in §3.2, the concentration dynamics in §4.3 — without modelling second-order responses such as risk-taking adjustment, labour supply, consumption timing, or strategic asset structuring in response to the tax system. This limitation is shared with (RATES), which uses the same pre-behavioural assumption for all revenue and burden figures, and is noted explicitly there.

The pre-behavioural assumption means the results in this paper are bounds rather than point estimates. Where WDT's structural properties generate positive behavioural effects — the symmetric refund encouraging risk-taking by reducing the asymmetry of outcomes, the elimination of lock-in enabling portfolio reallocation toward higher-return assets — the welfare advantage over CGT and stock-base systems would widen under a behavioural model. Where WDT's implementation generates negative behavioural effects — migration, avoidance, restructuring — the advantage would narrow. WFR establishes the pre-behavioural welfare baseline; whether positive or negative behavioural effects dominate at calibrated parameters is the question EVAL is designed to answer by testing each Category 3 cost against the Category 1 welfare advantage at empirically plausible behavioural magnitudes.

## 7.2 General Equilibrium

The analysis is partial equilibrium throughout. Prices, wages, interest rates, and the aggregate capital stock are held fixed; the comparison is conducted at the individual taxpayer level with no feedback from the tax system to the macroeconomic environment. This is the correct scope for a Level 1 paper establishing theoretical welfare properties under controlled conditions, but it leaves several general equilibrium channels unexamined.

The most consequential omission is the capital allocation effect. Under Fagereng-style persistent return heterogeneity, the choice of tax base determines not just who bears the welfare cost but whether the tax system creates incentives for capital to move toward higher-return uses. A stock wealth tax that levies equally on high- and low-return wealth creates no reallocation incentive; a delta-base tax that takes more from high-return wealth and refunds low-return wealth attenuates the reallocation signal in one direction and strengthens it in another. The general equilibrium welfare effect of this channel — which is the substance of the Guvenen et al. dispute with Boadway and Spiritus discussed in §5.5 (@BoadwaySpiritusEtAl2025, @GerritsenEtAl2025) — cannot be evaluated within the partial equilibrium framework of this paper. A Level 2 treatment would require closing the model with an aggregate production function, a capital market clearing condition, and a calibrated relationship between the return distribution and the marginal product of capital.

## 7.3 Implementation Cost Quantification

The five Category 3 costs identified in §6.1.3 — valuation friction, compliance and avoidance costs, administrative learning, migration response, and novel avoidance strategies — are open questions that cannot be resolved within this paper's scope. They are addressed by different parts of the companion paper series at different levels of specificity: (VAL) characterises the valuation architecture and the tolerant zone but does not quantify friction at scale; (BEHAV) characterises the behavioural shapes and the mild-overstatement equilibrium but does not produce empirical avoidance cost estimates; (CLOSE) designs the departure settlement mechanism but does not estimate migration response; (PHASE1) specifies the measurement framework through which Phase One implementation would generate the first empirical data on all five costs simultaneously.

The relationship between this paper and EVAL is worth stating precisely. WFR establishes the welfare advantage at the pre-behavioural level. EVAL's contribution is to test each Category 3 cost against that advantage using a break-even framework: for each cost, what magnitude would be required to offset the 141–143 basis point lock-in welfare advantage? If a break-even threshold is empirically implausible given the existing literature on analogous wealth tax systems, that cost cannot explain away the welfare advantage. If a threshold falls within an empirically plausible range, that is a genuine open question that Phase One is designed to resolve. WFR does not pre-empt EVAL's findings; it provides the welfare baseline EVAL requires.

## 7.4 Progressive WDT Advantage at Longer Horizons

The N=30 concentration result in §4.3 shows a near-equivalence between flat and progressive WDT at the canonical horizon: 286.3× versus 288.1×. The plan's finding — that the relevant axis at N=30 is accrual versus stock base, not flat versus progressive rate — follows from the logistic schedule operating in the near-flat entry region across the tested wealth levels for 30 years. The progressive advantage would emerge at longer horizons as accumulated wealth pushes the logistic higher up its curve, increasing the differential between the Great and Poor tier effective rates and compounding a widening concentration gap.

Whether this longer-horizon result is worth establishing as a formal model output is an open question for WFR.A. A 73-year run using the full historical return sequence would show whether the progressive WDT advantage on concentration becomes visible at horizons consistent with the full empirical dataset. TODO: decide whether to include the N=73 concentration sensitivity in WFR.A as an appendix result, and update the cross-reference here when the decision is made. If the N=73 run is not included, the paper should acknowledge explicitly that the progressive concentration advantage requires a longer horizon to compound than the canonical 30-year window permits — this is a genuine scope limitation, not a suppressed finding.

\newpage

# References {.unnumbered .unlisted}
