---
title: "WDT Project Map"
description: "**Last updated:** 13 September 2026  
**Papers covered:** (WP), (MF), (LR.A), (LR.B), (JUR), (VAL), (VAL.A), (VAL.B), (CORP), (CORP.A), (GOV), (GOV.A), (GOV.B), (RATES), (RATES.A), (SWEEPS), (SWEEPS.A), (WFR), (WFR.A), (BEHAV), (CLOSE), (POL), (PHASE1), (ENV), (FM), (MOD), (SCOPE), (ADD)  
**Papers not yet in project:** *None*"
author: "K. Ogata"
---
```
<script>
  document.addEventListener("DOMContentLoaded", function () {
    WDTGeocities.inject(["banner"]);
  });
</script>
```

## The Core Feasibility Case

Five objections recur against any mark-to-market wealth tax. The WDT's answers, drawing across papers:

**"You can't value illiquid assets accurately every year."** The mechanism does not require accurate valuations. A declared value establishes the recognised basis from which all future deltas are measured; tax liability flows from the change between declared values, not from whether any declaration was correct. The state enforces the consequences of whatever was declared, not whether it was correct. Understatement defers rather than eliminates tax; overstatement inflates a refund entitlement that will overshoot in a loss year. At canonical parameters, declaration ratios spanning α = 0.8 to α = 1.5 produce lifetime outcomes close to honest declaration — the tolerant zone — a wide forgiving centre with penalties concentrated only at the tails. The valuation objection is dissolved at the design level, not managed. (WP §3.7; VAL §1, §7.1; RATES §10)

**"Taxpayers will understate."** Within the tolerant zone, understatement is largely self-defeating: the basis gap compounds with asset growth and recovers at realisation. The refund in a loss year is proportional to the declared basis, so a systematic understater forfeits downside protection precisely when they need it most. For fungible assets, Route C's must-transfer rule creates a direct compounding equity dilution cost without requiring any audit. The state does not need to win a technical competition over what an asset is worth; it needs only to enforce the consequences of what the taxpayer said it was worth. (VAL §5, §7.2; WP §8.1)

**"The arithmetic doesn't work."** RATES establishes four properties simultaneously at the 2000 reference scenario — chosen because it produces the lowest post-fill coverage of all 73 tested start years. The SRR fills within 3 years invariantly across all 73 historical start years: the refund guarantee becomes mechanically credible within a single political cycle. The LRR fills in every tested start year with a breakeven range of 7–29 years and a median of 13. Post-fill fiscal surplus reaches 6–15% of government expenditure at the 2000 worst-case and 125.5% at the median start year. Individual burdens are proportionate throughout: the revenue-weighted annual wealth burden is 0.35% of net worth, below the 1–2% stock levy of conventional wealth tax proposals; the gain-weighted effective lifetime rate is 13.0%, comparable to CGT on a materially larger base. (RATES §10)

**"The rich will just leave."** Norway's 2022 wealth tax increase produced migration responses that were real but fiscally modest — roughly 22 cents of revenue lost per unit raised, with overall revenues continuing to grow. The cross-base externality (Agrawal et al. 2025: income and VAT losses approximately six times the direct wealth-tax loss) is the dominant empirical qualification and Phase One's first measurement priority. The WDT's design responses are structural: Route C and D hold taxpayers' entire accumulated basis gap as a departure cost; the lifetime contribution envelope persists across closures and re-entries; the bridging facility (CLOSE §5) decouples physical departure from settlement completion. The Governing Council can reduce rates in response to observed departure — a capacity no prior wealth tax mechanism held. (WP §7.3; BEHAV §9.2; CLOSE §4.2)

**"Governments will eventually scrap the refund."** The refund commitment is designed for legal durability from the outset, not as a political aspiration. Ten enumerated structural clauses (GOV §5.2) protect the mechanism's core commitments against erosion within the governance architecture itself. The SRR is ring-fenced and pre-funded; the refund drawdown is mechanical and constitutionally guaranteed, not subject to governance discretion. The SWF's accumulated reserves mean the government cannot suspend the refund without breaching a funded obligation rather than merely breaking a promise. Constitutional entrenchment is the long-run goal, built on the track record Phase One creates. (WP §4, §8.5; GOV §4.2)

---

## 1 WP: The White Paper

The spine of the project. Establishes the mechanism, derives each component from the others, frames the cooperative logic, and identifies what companion papers must establish.

**Mechanism.** The WDT levies a progressive annual charge on the change in an individual's net worth above an exemption threshold. Three interdependent components — accrual-basis delta tax, symmetric loss-refund, Sovereign Wealth Fund — plus taxpayer governance participation in the SWF are designed as a system: each exists because the others require it. The delta base removes the lock-in distortion and debt-preference incentive that realisation-based systems create. (WP §3.1)

**Valuation architecture.** The state does not need to determine correct asset values, only enforce the consequences of declared values. A declared value becomes the legally operative basis; future deltas are calculated mechanically from it. Professional routes (A/B) place valuation risk with the valuator. Self-declaration routes (C/D) place it with the taxpayer. The tolerant zone (α ≈ 0.8–1.5) is a design feature: penalties concentrate at the tails, leaving the centre deliberately forgiving to absorb legitimate valuation uncertainty. (WP §3.7, §3.8)

**Symmetric refund.** The refund rate in loss years equals the marginal rate that would have applied to an equivalent gain. Full symmetry is a settled design position. The lifetime contribution envelope bounds total refunds at total taxes paid — preventing the mechanism functioning as public insurance — while creating a deepening cooperative stake that compounds across time. (WP §3.5)

**Revenue.** RATES demonstrates four properties simultaneously at the 2000 worst-case reference: refund credibility within 3 years; 100% success across 73 historical start years; post-fill surplus of 6–15% of government expenditure; revenue-weighted annual wealth burden of 0.35% and gain-weighted effective lifetime rate of 13.0%. The pre-behavioural combined estimate (individual WDT ~£874b, corporate levy ~£172b, UHNW tail ~£27b) approaches near-parity with UK total managed expenditure, inverting the conventional burden of proof. (WP §5)

**Liquidity.** The delta base significantly reduces the liquidity problem versus a stock wealth tax because tax is proportional to the gain rather than the total stock. Route C settles in equity; Route D defers all settlement to realisation. Conservative self-declaration within the reporting relationship is an intended feature, not a loophole. Route C and D liquidity management is resolved by design; Routes A and B remain the design challenge. (WP §8.2)

**Implementation.** Phase One: high threshold, small population, primary objectives are infrastructure and institutional legitimacy. Phase Two: lower threshold, labour tax relief dividend. Transition is condition-based, not calendar-based. Constitutional entrenchment starts with strong ordinary legislation and deepens as Phase One builds a track record. (WP §7, §8.5)

---

## 2 MF: Moral and Philosophical Foundations

Establishes the foundational axiom and terminal goal from which the design is derived, and records eight named compromises where theory and practice part company.

**Foundational axiom.** Individual human beings are the only legitimate moral subjects of a tax system. Everything in the design derives from this axiom applied consistently. Corporations, trusts, and funds are instruments; they have no welfare of their own. (MF §2)

**Collective production argument.** Extraordinary private wealth is partly a collective product — it depends on workers, households, and the public infrastructure those households fund. At extreme concentration, the connection between individual effort and financial return weakens; large fortunes emerge substantially from inheritance, structural positioning, and compounding of advantages already held. (MF §3)

**Wealth as power.** Above sufficiency, wealth provides present-tense advantages that do not depend on spending: credit access, geographic optionality, political influence, legal leverage, intergenerational transmission. The consumption-tax tradition treats wealth as fiscally irrelevant until spent; the WDT rejects this at extreme concentration. (MF §4)

**Terminal goal.** Democratic flourishing — maintaining conditions under which democratic institutions remain functional and ordinary people retain meaningful participation. The labour tax relief dividend is the mechanism through which this goal is actually pursued; an implementation that taxed wealth but directed revenue elsewhere would fail on its own terms. (MF §6)

**Named compromises.** Eight points where foundational theory and practical design part company, to be consulted whenever a new design decision introduces a similar trade-off. Key items: the corporate instrument is a pragmatic departure from the individual-centred axiom; the exemption threshold is an administrative necessity; international mobility is managed, not closed; the Route D extreme residual is an accepted boundary condition. (MF §9)

---

## 3 LR.A / LR.B: Literature

Two companion papers covering confirmed gaps in existing literature and the project's intellectual ancestry.

**LR.A: confirmed gaps.** Identifies nine gaps in existing academic literature bearing directly on WDT design. Three are now closed by WFR (gaps #1–3: the Domar-Musgrave extension to a progressive delta base; a welfare comparison including the delta base; distributional arithmetic of delta-base concentration under persistent return heterogeneity). Six remain open: cooperative compliance at professional-intermediary-mediated wealth levels; the cross-base migration externality; administrative-layer intervention effects; the causal framework for wealth tax abolition; the international competitive dynamic; and the minimum-tax floor interaction with refund-based systems. These are literature gaps, not Phase One questions: they require formal modelling or comparative case-study work. (LR.A §2)

**LR.B: intellectual ancestry.** Reference guide across nineteen sections: Haig-Simons and the comprehensive income tradition; prior accrual proposals and where they stopped (all reached the delta concept and stopped at valuation difficulty); Domar-Musgrave symmetric loss treatment; heterogeneous returns and welfare; the empirical wealth tax record; Harberger self-assessment; cooperative compliance; SWF reference cases; exit taxation and international coordination. The cross-base externality finding (Agrawal et al. 2025) is the dominant qualification on the Norwegian 22-cent migration estimate. (LR.B §1–§19)

---

## 4 JUR: UK Jurisdiction and Data Reference

Justifies the UK as reference jurisdiction and compiles empirical data the companion papers require. Models an idealised country inheriting specific UK features, not the UK in its full constitutional complexity.

**Key data.** UK GDP ~£2.65 trillion; total managed expenditure 2022–23 ~£1,157b; equity return series 1947–2019 (JST dataset, capital gains only, 10.45% p.a. mean); WDT bracket populations via Pareto extrapolation above ~£3m, lighter than the true distribution and consistently conservative for revenue claims. (JUR §3–§5)

**Institutional preconditions.** The HMRC data access agreement required for microsimulation is an institutional precondition, not a Phase One output. Resolution requires negotiation independent of the design papers. (JUR §6)

---

## 5 VAL: Valuing Wealth

Establishes the four-route valuation architecture, the self-balancing mechanism, the tolerant zone, and the Route D auction as the deterrent of last resort.

**Core reframe.** The question is not how the state determines the correct value of an asset the taxpayer prefers to undervalue, but whether the state needs to determine that value at all. A declared value becomes the legally operative basis and tax liability flows mechanically from subsequent deltas. The state enforces the consequences of the declaration, not whether it was correct. (VAL §1)

**Four-route architecture.** Assets classified by fungible/non-fungible and professionally valued/self-declared produce four routes. Routes A/B: professional valuation with the valuator bearing risk of overturned assessment. Route C: self-declared fungible assets, settlement in kind only (must-transfer of proportional equity interest at declared value — the self-balancing mechanism). Route D: self-declared non-fungible assets, no periodic formal assessment, settlement deferred to realisation only. Settlement must match the valuation route that produced the liability. (VAL §4)

**Declaration strategy and the tolerant zone.** Strategic stability rests on three layers. First, a broad tolerant zone: at canonical parameters, declaration ratios spanning α = 0.8 to α = 1.5 produce lifetime outcomes close to honest declaration, absorbing legitimate valuation uncertainty by design. Second, tail penalties: severe understatement at moderate-to-high growth and aggressive overstatement at moderate growth carry real accumulating costs. Third, asymmetry within the zone: understatement reduces refund protection in loss years while overstatement preserves it, giving risk-averse taxpayers a modest incentive to bias slightly upward. The model-implied behavioural centre is near α ≈ 1.1 — a conditional prediction, not a dominant strategy. (VAL §7.1, §7.3)

**Route D auction.** The deterrent of last resort for egregious misdeclaration of self-declared non-fungible assets. A taxpayer declaring below true value risks losing the asset at their own declared price through competitive bidding, drawing on the Harberger self-assessment tradition. Fires only on three-body Valuation Body unanimous agreement (sealed estimates, non-anchored, simultaneous opening). Narrow and infrequent by design; deterrent effect depends on credibility, not frequency. Three pathways: enforced (Valuation Body triggered), voluntary hard-reset (taxpayer-initiated for basis certainty), and inheritance (automatic on transfer). Full architecture in GOV.B §G. (VAL §11)

**Boundary conditions.** Three named residual limits: the inception basis vulnerability (Route D basis is weakest at first declaration, with no prior committed value to self-correct against); the reclassification boundary (assets moving from A/B to D carry a correct prior basis but lose ongoing self-correction); the auction market maturation boundary (competitive bidding may eventually reflect market dynamics rather than underlying value). Phase One declaration data versus subsequent realisation prices is the primary detection instrument. (VAL §14.4)

---

## 6 CORP: Corporate Architecture

Establishes the corporate delta levy as a collection mechanism that closes the attribution gap for large listed companies with dispersed ownership that individual WDT assessment cannot reach.

**Three ownership tranches.** (1) Native WDT shareholders: provisional levy held in settlement account, released as credit on confirmed individual settlement within one-year window. (2) Identified intermediaries: provisional levy at entity level with downstream pass-through where the attribution test is met. (3) Unidentified beneficial owners: final charge at τ_h. The attribution test is binary — can the intermediary identify and attribute underlying beneficiaries to support individual WDT reconciliation? Attributability, not entity type, is the operative category. (CORP §3)

**Loss years.** No levy, no refund at the corporate level. Shareholders experiencing losses receive individual WDT refunds through personal assessment. (CORP §5)

**Rate parameters.** τ_prov and τ_h are distinct optimisation problems (CORP.A §B.1, §B.2). τ_m is a ceiling for τ_h calibration, not its anchor. τ_0 is the dominant fiscal parameter at canonical k = 0.001. (CORP §4; CORP.A §B)

---

## 7 GOV: Constitutional Governance

Establishes the three-chamber Governing Council, ten enumerated structural clauses, and the constitutional architecture protecting the mechanism against erosion.

**The governance problem.** Setting WDT parameters requires operational knowledge held almost entirely by the taxable population itself. Conventional democratic governance excludes that population from the formal process. The Governing Council resolves this by giving formal standing to those with the best operational knowledge while structurally preventing that advantage from becoming a decision advantage. (GOV §2)

**Three-chamber structure.** Taxpayer Chamber (TP, 25%), Fiscal Sovereign Chamber (FS, 25%), Dividend Recipient Chamber (DR, 50%). DR's 50% share is derived — not chosen for symmetry — from the anti-collusion guarantee: DR's unanimous opposition must independently be sufficient to defeat any joint TP/FS proposal. DR is filled by monthly lottery from the general population with staggered one-year terms. A proposal passes only if nays stay below DR's share and yays exceed 50% of votes actually cast. (GOV §3)

**Ten enumerated structural clauses.** Define the properties the system must preserve to remain the same kind of tax. Any compatibility question about a design change must be checked against these ten. Seven follow directly from foundational axioms; three rest partly on judgment — the Route D auction mechanism, DR's lottery constitution, and mandatory permanent public transparency are the judgment-dependent three. (GOV §5.2)

**Refund guarantee.** The refund drawdown is mechanical and constitutionally guaranteed, not subject to governance discretion. This separation — automatic refund trigger versus discretionary governance — is necessary for the credibility of both. (GOV §4.2)

---

## 8 RATES: Rates and Revenue

Establishes that the mechanism's arithmetic works at proportionate individual burdens across the full range of historical starting conditions.

**The question.** Does the arithmetic work, without exception, on four properties simultaneously? The answer is yes at the 2000 reference scenario — chosen because it produces the lowest 10-year post-fill coverage of all 73 tested start years, making every claim a floor.

**The four properties.**

1. *Refund credibility within a single political cycle.* The SRR fills at year 3 invariantly across all 73 start years in the 1947–2019 UK equity return data, regardless of whether the mechanism inherits a boom or a crash.

2. *The mechanism never fails.* 100% success rate across all 73 start years and all four economic cycles. LRR breakeven ranges from 7 to 29 years, median 13. Reference scenario (2000) breakeven: year 19.

3. *Fiscal replacement is viable at scale.* Post-fill surplus equivalent to 6–15% of government expenditure at the 2000 worst-case; 125.5% TCM median across the 73-start-year sweep. Pre-behavioural combined estimate (individual WDT ~£874b, corporate levy ~£172b, UHNW tail ~£27b) approaches near-parity with UK total managed expenditure of ~£1,157b.

4. *Individual burdens are proportionate throughout.* Revenue-weighted annual wealth burden: 0.35% of net worth, below the 1–2% stock levy of conventional proposals. Gain-weighted effective lifetime rate: 13.0%, comparable to CGT on a materially larger base. Maximum annual wealth burden: 0.79%; maximum effective rate on gains: 27.2% — both requiring simultaneous membership of the top 0.01% wealth bracket and highest persistent-outperformance growth tier across the full 30-year horizon.

**Conservatism direction.** All modelling assumptions are chosen to understate revenue except one: behavioural responses are not modelled. Migration, restructuring, and avoidance will reduce actual revenue by an amount only Phase One can establish. Revenue is heavily concentrated at the upper tail — the population most capable of responding. BEHAV addresses this; these figures are the pre-response baseline. (RATES §10)

**Rate function.** A logistic S-curve: τ(W) = τ_m / (1 + A·exp(−k·(W − W_min))). Canonical parameters: τ_0 = 15%, τ_m = 70%, k = 0.001/£m, W_min = £2m. Full symmetry of the loss-refund is a settled design position: partial symmetry breaks the Domar-Musgrave risk-sharing logic. (RATES §4)

**N = 30 as upper-bound horizon.** N measures years in the WDT system, not the holding period of any asset. The 30-year working assumption is grounded in inheritance-triggered crossing of W_min using ONS demographic data. Burden figures at N = 30 are ceiling estimates: both burden measures are increasing and convex in N, so taxpayers with shorter histories or loss years face lower burdens. (RATES §5)

---

## 9 SWEEPS: Parameter Sweeps and Governing Council Calibration

Characterises the parameter space available to the Governing Council through two complementary simulation datasets, VAL.S and RATES.S.

**Purpose.** The architecture is fixed; the parameters are the Governing Council's to move. VAL.S examines declaration incentive properties: tolerant zone width, self-limiting correction timing, understater deterrence strength. RATES.S examines fiscal outcomes: LRR fill year and TCM coverage ratio. (SWEEPS §1)

**Parameter hierarchy (fiscal).** τ_0 dominates: at canonical k = 0.001, the logistic midpoint sits far above top-bracket entry wealth, so τ_0 is approximately the whole rate every bracket pays. W_min is second on LRR fill timing. k matters conditionally above realistic values. τ_m is fiscally inert for the modelled population across the full sweep. (SWEEPS §3)

**Parameter hierarchy (mechanism integrity).** τ_0 controls N-crossing timing — how quickly the self-limiting correction activates for aggressive overstaters. τ_m controls the understater penalty plateau ceiling — the egregious-understater deterrence lever, separable and concentrated at the far tail. k controls tolerant zone width and progressivity. W_min has near-zero leverage on declaration incentives for taxpayers above threshold. (SWEEPS §3)

**The primary calibration tension.** τ_0 is the one parameter where fiscal speed and declaration incentive correction move in the same direction, but both move together with entry burden. Higher τ_0 accelerates LRR fill and brings the overstater correction earlier; it also raises effective rates across the full distribution. The policy question is not which dimension to sacrifice but how fast to proceed and at what entry burden Phase One is most likely to establish the cooperative norm the mechanism depends on. (SWEEPS §4)

**Self-correction robustness.** At canonical parameters, all three tracked overstater levels (α = 1.5, 1.8, 2.0) cross into nominal net-cost territory before N = 22. The mild-overstater nominal advantage does not survive NPV adjustment even before the nominal crossing: periodic outflows are real early money while the sell-year refund is inflated late money. The declaration equilibrium is near α ≈ 1.1 — driven by refund-protection asymmetry under valuation uncertainty, not a genuine economic return to overstatement. (SWEEPS §5)

**Small lever set as design feature.** Four rate-function parameters doing largely separable jobs is preferable to a larger entangled set on accountability and democratic legibility grounds: calibration decisions have characterised consequences that any motivated observer can track and evaluate against outcomes. (SWEEPS §6)

---

## 10 WFR: Welfare Comparison Across Tax Systems

A Level 1 theoretical paper comparing six tax systems on welfare grounds at genuine revenue equivalence, closing three confirmed literature gaps simultaneously.

**Scope.** WFR compares flat symmetric WDT, progressive symmetric WDT, income tax, CGT, stock wealth tax, and consumption tax, using a common empirical return distribution and admitting welfare mechanisms one at a time in a controlled sequence. It closes gaps #1–3 from LR.A and positions the delta instrument in the active Guvenen / Gerritsen-Jacobs-Spiritus dispute without adjudicating it. WFR.A contains the full simulation tables underlying all results. (WFR §1)

**The three-category framework.** Category 1 findings are welfare costs of existing systems established by the model — they do not require the WDT to exist. Category 2 findings are properties of the WDT following from the delta base and symmetric refund, independently of implementation outcomes. Category 3 findings are prospective implementation costs that are real but not currently quantifiable. The standard objection to any unimplemented instrument — "you haven't shown it has no costs" — conflates Category 2 and Category 3. (WFR §2)

**Controlled baseline.** With distortions suppressed and all systems at revenue equivalence, flat WDT leads by 17.4 basis points over income tax and CGT, and by 133.1 basis points over stock wealth and consumption tax. The baseline confirms the WDT does not win through a mechanical rate advantage. The flat WDT satisfies Domar-Musgrave to floating-point precision across all tested γ — a mechanism result, not a welfare verdict. (WFR §3)

**Progressive rate complications.** A progressive rate schedule introduces three complications to the D-M architecture: the progression effect (C1), the leverage and net-worth base interaction (C2), and the intertemporal rate asymmetry from gain-loss sequences (C3). All three are second-order at canonical parameters — the welfare gap between flat and progressive WDT stays below 0.05 basis points up to £100m initial wealth. This is an honest constraint on the progressive rate claim, not a suppressed finding. (WFR §4.1; WFR.A §B)

**CGT lock-in.** When portfolio choice is endogenous, CGT imposes a switching wedge between the gross return differential and the after-tax cost of moving to a superior asset. At the reference calibration, the lock-in welfare cost is 141–143 basis points — approximately 82 times the baseline welfare difference between systems. This is a Category 1 finding: a cost of an existing, operating system established without requiring WDT implementation data. The WDT eliminates lock-in by construction (Category 2). The Arachi et al. (2022) objection that accrual taxation creates intertemporal consumption distortions in loss years is addressed directly: the symmetric refund restores consumption capacity at exactly the moment the Arachi mechanism would otherwise be most acute. The objection applies at the envelope binding boundary — Poor-tier entrants in the first loss year — but not in the general case. (WFR §4.2; WFR.A §C)

**Heterogeneous returns and concentration.** Using the four-tier Fagereng calibration (outer-tier return differential ≈ 8pp, conservative against Fagereng's observed 18pp), WFR tracks wealth concentration over 30 years. At N = 30 both WDT variants reach approximately 286–288× Great/Poor concentration; income tax reaches 320×; both stock-base systems reach 479×. The dominant axis is accrual basis versus stock base, not flat versus progressive rate. The progressive WDT advantage on concentration is not visible at N = 30 at canonical parameters, though it would emerge at longer horizons. The 479× result for stock-base systems is a Category 1 finding. (WFR §4.3; WFR.A §D)

**Literature positioning.** WFR closes gaps #1–3 from LR.A simultaneously. It enters but does not adjudicate the active dispute between Guvenen et al. (2023) and Gerritsen, Jacobs, Spiritus & Rusu (2025) — both comparing stock wealth tax and capital income tax — by adding the delta instrument to a comparison that has not previously included it. The 141–143 bp lock-in cost and the 479× concentration path are Category 1 findings referenced in this dispute. (WFR §5)

**Conclusion.** A decision to maintain CGT or a stock wealth tax after this analysis is a decision to accept known welfare costs. Whether any Category 3 prospective implementation cost plausibly exceeds 141–143 basis points is the question EVAL (forthcoming) is designed to answer using WFR's welfare baseline. (WFR §6, §7)

---

## 11 BEHAV: Behavioural Robustness

Establishes behavioural robustness as a design property derivable from first principles, characterises nine behavioural shapes, and identifies the enforcement paradigm shift and the Membrane as its institutional expression.

**First principles.** Behavioural robustness is a design property, not a behavioural prediction. The existing architecture actively engineers stagnation through lock-in distortions, basis step-up, and debt preferences; the WDT removes those frictions before claiming any compliance improvement. (BEHAV §3)

**The Membrane.** Five friction types (information, visibility, legitimacy, feedback, compliance) produce five design principles. The Membrane — the layer through which taxpayers experience the institution — has five health dimensions. Clarity and Accessibility share the strongest complementarity; Reciprocity and Responsiveness are also complementary; Fairness is downstream of all four other dimensions and the leading indicator of membrane failure. SWEEPS's parameter separability result contributes structurally to both the Clarity and Fairness dimensions. (BEHAV §4–§6)

**Nine behavioural shapes.** From full cooperative compliance to active resistance, these provide the range against which robustness is evaluated. Shapes 4–6 (restructuring, timing manipulation, cross-border asset migration without personal exit) generate most value at risk from avoidance. (BEHAV §8.1–§8.10)

**Enforcement paradigm shift.** Unattributed ownership faces τ_h by default; surfacing hidden assets compounds the concealment cost progressively; the Route D entry basis is substantially more bounded than a pure detection-contest framing suggests. The route distribution analysis establishes the empirical basis: Routes A and B likely account for ~60–85% of WDT-taxable wealth by volume, with Route D at ~10–20%, concentrated at the very top. VAL's tolerant zone (α ≈ 0.8–1.5) further bounds the residual: Route D's enforcement problem is the egregious-understatement tail, not imprecision in general. (BEHAV §8.11, §8.12)

**Cross-base externality.** The Agrawal et al. (2025) six-to-one multiplier is a directional warning calibrated to conventional stock wealth taxes — structurally different from the WDT's delta base at a revenue-weighted annual burden of 0.35% of net worth. The directional risk is retained; the magnitude is uncertain and a Phase One observable. Six design responses are available: the multiplier is a point estimate from subnational Spanish data; membrane investment is fiscally urgent at a six-to-one ratio; the Governing Council can reduce rates in response to observed departure; the LRR timeline extension buffer allows lower-rate operation; the re-entry rule and envelope carry-forward strengthen with system age; net inward migration remains a formal possibility. (BEHAV §9.2)

**Membrane calcification.** The tendency of a mature institution to preserve processes suited to an earlier taxpayer population is the one form of institutional drift the WDT addresses least directly. The response is a named monitoring architecture: mandatory publication of membrane health observables; the Taxpayer Chamber as institutional monitor; the Allocator as the Fairness-dimension signal; the TP/DR coalition as the lever against FS resistance on funding. (BEHAV §10)

**Phase sequencing.** Membrane investment is front-loaded and cannot be deferred. A membrane not functioning at design quality from first taxpayer contact generates legitimacy friction that compounds into subsequent phases. The personal adviser corps — state-funded advisers drawn from the displaced professional compliance industry — operationalises the Accessibility principle at the individual level for each Phase One taxpayer's first assessment cycle. (BEHAV §11.1, §5.5–§5.6)

---

## 12 CLOSE: Position Closure

Establishes death, jurisdictional exit, threshold fall-through, and bankruptcy as a unified class of event, and derives the bridging facility and re-entry rule from that unification.

**Unified closure theory.** All four closure types are the same kind of event: the WDT assessment position closes. The mechanism owes a correct final delta calculation and honours the symmetric refund on any negative final delta; the individual owes a correct final accounting regardless of why the position closes. (CLOSE §2)

**Bridging facility.** Decouples physical departure from settlement completion. Where the expected exit delta is positive the taxpayer posts a bond; where negative the SWF posts a bond to the taxpayer; where uncertain both sides post proportional bonds that net on settlement. Friction concentrates on non-cooperation, not on the act of departure. (CLOSE §5)

**Re-entry rule.** The lifetime contribution envelope persists across all closures and re-entries; the re-entry basis is fresh but the envelope carries the prior history forward, closing strategic cycling. (CLOSE §4.2)

---

## 13 POL: Political Architecture

Identifies the three structural failure mechanisms behind OECD wealth tax abolition and establishes political durability as a design property of the WDT.

**Why wealth taxes fail.** Twelve OECD countries levied individual net wealth taxes by 1990; most abolished them by 2020. Three structural failure mechanisms: legitimacy collapse (invisible reciprocity — taxpayers experience the tax as confiscation with no visible benefit to defend); organised opposition advantage (small concentrated taxed population versus large diffuse beneficiaries); and institutional brittleness (individually defensible exemptions accumulating invisibly into structural hollowing). (POL §3)

**Durability as design property.** The WDT addresses all three failure mechanisms as a consequence of correct derivation rather than political afterthought. Each WDT institution serves multiple independent functions simultaneously: the symmetric refund addresses Domar-Musgrave risk-sharing, cooperative moral commitment, and taxpayer incentives before it addresses political reciprocity. Because each feature exists for three independent reasons, an opponent must pay three separate costs to remove it. (POL §5)

**Bootstrapping problem.** Phase One is the vulnerability window — the mechanism is untested, the membrane unproven, and mutual stake not yet accumulated. The mitigations (SRR partially capitalised, refund demonstrated, envelope deepening) must replace the accidental hostage equilibrium before a hostile government arrives. There is no mechanism-shaped resolution to this; the mitigation is sequencing. (POL §6)

---

## 14 PHASE1: Phase One

Draws the line between what the design establishes and what only implementation can answer, and identifies seven empirical clusters unanswerable at the design stage.

**Seven empirical clusters.**

1. Cooperative architecture effects at professional-intermediary-mediated wealth levels
2. Avoidance shapes (Shapes 4, 5, 6 from BEHAV's nine-shape taxonomy)
3. Migration and the cross-base externality magnitude (the Agrawal six-to-one multiplier)
4. Valuation route and assessment window adoption (load-bearing for flexibility levy calibration)
5. Administrative-layer intervention effects (taxpayer history record highest-priority sub-item)
6. OBR independence as mandate-guardian adequacy
7. Corporate instrument transition conditions for the CIT displacement question

**Evaluation design.** Phase One that confirms working assumptions and Phase One that requires design revision are equally valid outcomes; the evaluation designs in PHASE1 §5 exist to distinguish the two. (PHASE1 §5)

---

## 15 ENV: Environmental Effects and Transmission Channels

Establishes that the standard efficiency critique fails for the WDT and identifies four positive transmission channels.

**The efficiency critique.** The standard framing — wealth taxation as a friction on a capital stock — fails for a tax on the annual change in net worth with a symmetric loss refund. The WDT removes capital allocation frictions (lock-in distortion, debt preference, basis step-up) rather than adding new ones. (ENV §2)

**Displacement.** Staged replacement of labour taxation through constitutionally committed LRR accumulation delivers demand stimulus at a pace that reduces transition-shock risk. Bilateral NICs removal is the cleanest case: both sides see the benefit directly; labour becomes cheaper to supply and hire simultaneously. (ENV §3)

**Automation.** The WDT tax base tracks wealth delta regardless of whether appreciation was generated by human labour or capital deployment. As automation increases the productive value of capital, WDT revenue increases automatically without legislative change — categorically different from robot taxes, capital income taxes, or stock wealth taxes. (ENV §4)

**Financial stability.** The symmetric refund reaches the population whose portfolio decisions move asset markets precisely when liquidation pressure is highest, dampening the forced-selling mechanism that turns valuation problems into systemic crises. The SWF's countercyclical deployment capacity and the DR chamber's pre-commitment capacity are two independent countercyclical instruments requiring no discretionary intervention to activate. (ENV §5)

---

## 16 FM / MOD / SCOPE / ADD

**FM (First Mover).** Any jurisdiction that has concluded the WDT's properties are likely true faces commit-or-suppress, with no stable middle option. Partial adoption is not available: removing the symmetric refund collapses the valuation architecture and breaks the Domar-Musgrave logic; removing the constitutional governance makes the mechanism vulnerable to the same incremental erosion that ended every prior OECD wealth tax.

**MOD (Modular Adoption).** Category 1 institutions (professional valuation systems, beneficial ownership attribution law, sovereign wealth funds, independent fiscal governance) have independent justification outside the WDT and accrue through locally rational policy decisions. Category 2 mechanisms (symmetric refund, Route D auction, lifetime contribution envelope, three-chamber Governing Council) do not accrue and require deliberate political commitment. Accretion lowers the remaining commitment cost when a jurisdiction eventually evaluates the WDT; it does not make the decision.

**SCOPE.** Records which open question register items fall outside the project's scope and why — distinguishing formal modelling gaps requiring peer-review infrastructure, comparative political economy requiring case-study depth, and jurisdiction-specific legal analysis. Prevents re-opening settled questions without addressing the objections already recorded.

**ADD.** Eight implementation questions the design papers leave open — exemption threshold indexation, TP chamber conflict-of-interest visibility, external chamber communication rules, DR-eligible pool monitoring, the consumption delta, SWF asset composition monitoring, Phase One measurement framework as binding standard, and the bootstrapping bridge facility — each with an approach sketch showing the shape of what a genuine answer requires.

---

## 17 Open Questions Register

Items not listed here are settled. Items listed under **Closed** have been resolved by a completed paper and are retained for audit trail only.

### Closed Literature Gaps (resolved by completed papers)

| # | Question | Closed by |
|---|---|---|
| 1 | Domar-Musgrave formal extension to a progressive delta base (three complications: net worth base, progressive rates, multi-period rate asymmetry) | WFR §3.2, §4.1; WFR.A §A.4, §B |
| 2 | Welfare comparison including delta base alongside existing candidates | WFR §3, §4; WFR.A §A–§D |
| 3 | Distributional arithmetic of delta-base concentration under persistent return heterogeneity | WFR §4.3; WFR.A §D |

### Confirmed Literature Gaps (formal modelling required; separable from Phase One)

| # | Question |
|---|---|
| 7 | Causal framework for wealth tax abolition (three-mechanism framework not yet independently validated as political economy model) |
| 8 | International competitive dynamic at the political level |
| 9 | Minimum-tax floor interaction with refund-based systems in treaty law |

### Phase One Empirical Questions (unanswerable before a live system)

| # | Question |
|---|---|
| 4 | Cooperative compliance at ultra-high-net-worth level (professional intermediary mediation of compliance decisions) |
| 5 | Cross-base migration externality magnitude (Agrawal et al. 2025 six-to-one ratio applied to WDT population) |
| 6 | Administrative-layer intervention effects on compliance psychology |
| 13 | Valuation route and assessment window adoption distribution; flexibility levy calibration |
| 14 | OBR independence adequacy as WDT mandate-guardian |
| 15 | Corporate instrument transition: conditions for CIT displacement question to become a policy decision |
| 16 | Housing price net effect (demand composition shift; net price level ambiguous) |
| 18 | SRR floor calibration implication of mild-overstatement equilibrium (α ≈ 1.1 population centre) |
| 29 | Monitoring instrument for population distribution of α (mild-overstatement drift detection) |
| 30 | Bootstrapping problem: Phase One vulnerability window mitigation sufficiency |

### Assigned to MACRO (Phase One successor; requires live data)

| # | Question |
|---|---|
| 11 | Consumption multiplier magnitude and net bias direction of RATES estimates |
| 12 | Automation and tax-base migration under different automation trajectories |

### Governing Council Calibration Parameters (settled in kind, open in value)

| # | Question |
|---|---|
| 10 | SWF governance Phase One parameters (DR floor size, constituency dissolution triggers) |
| 17 | τ_0 × W_min joint surface — the only item in this group resolvable without Phase One data |
| 19 | Liquidity threshold for thinly traded company reclassification |
| 20 | τ_0 exact calibration (collection-security floor; 1–2 assessment cycles) |
| 21 | τ_h exact calibration within [deterrence floor, τ_m]; ramp pace; joint calibration with CIT/dividend displacement |
| 24 | Assessment window premium exact calibration (deferral charge + flexibility levy coefficients) |

### Jurisdiction-Specific and Institutional Preconditions (not design gaps)

| # | Question |
|---|---|
| 22 | τ_f diplomatic rate-setting (bilateral/multilateral agreement) |
| 23 | Route D auction implementation details (conduct rules, no-bid fallback, timeline, international assets) |
| 25 | Derivatives valuation methodology for illiquid positions |
| 26 | HMRC data access agreement for microsimulation |
| 27 | Post-Brexit information exchange gaps (DAC loss, EU-domiciled structures) |
| 28 | Constitutional/legal analysis of Route D auction trigger in specific jurisdictions |

### Summary observations

- **3 confirmed literature gaps** remain open, requiring formal modelling or comparative case study work. Gaps #1–3 (D-M extension, welfare comparison, concentration arithmetic) are closed by WFR.
- **10 Phase One empirical questions** cannot be resolved without live system data. Items 4–6 and 30 are the most consequential. The Agrawal cross-base externality (#5) is the dominant empirical qualification on all pre-behavioural revenue figures.
- **2 MACRO items** require Phase One data before modelling can be calibrated.
- **6 Governing Council calibration parameters** are settled in kind, open in value. Item #17 (the τ_0 × W_min joint surface) is the only one resolvable without Phase One data.
- **6 jurisdiction-specific items** are not design gaps; resolution requires legal analysis, diplomatic process, or institutional negotiation.
- **The most consequential calibration problem** is the τ_0 cross-dataset tension: higher τ_0 accelerates LRR fill and brings the overstater correction earlier, but also raises entry burden. No setting simultaneously optimises all three. The τ_0 × W_min joint surface (item #17) is the next analytical deliverable that does not require Phase One data.
- **The most consequential outstanding deliverable** is Phase One implementation itself: items 4–6, 29, and 30 cannot be resolved by any further desk research.

```{=html}
<!-- All four elements, canonical order -->
<script>
  document.addEventListener("DOMContentLoaded", function () {
    WDTGeocities.injectAll();
  });
</script>
```