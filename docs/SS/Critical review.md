# Referee Report: The Wealth Delta Tax Paper Series

**Reviewer role:** Senior examiner, public finance and institutional design
**Scope:** Full series (WP, MF, LR.A/B, JUR, VAL/A/B, CORP/A, GOV/A/B, RATES/A, SWEEPS/A, WFR/A, BEHAV/A, CLOSE, POL, PHASE1, ENV, FM, MOD, SCOPE, ADD, LDW, INST, FAL)

---

## Layer 1 — Logical Validity

### 1.1 The tolerant zone does not entail what the enforcement argument needs (VAL §7.1, WP §8.1, BEHAV §8.1) — **unacknowledged gap**

The argument runs: declaration ratios α ∈ [0.8, 1.5] produce lifetime tax outcomes close to honest declaration; therefore the state does not need declaration precision; therefore enforcement can be passive.

The conclusion outruns the premise in a specific way. The C.1 tables in VAL.A show that the *taxpayer's* lifetime outcome is similar across the zone. They do not show that *aggregate revenue* is similar across the zone. These are different quantities and the series conflates them. C.1 is normalised as (Net(α) − Net(1)) / TW(α) — a per-taxpayer ratio at a single reference wealth. Aggregate revenue under a population distributed across [0.8, 1.5] with a behavioural centre at α ≈ 1.1 is not derivable from a table of per-taxpayer deviations at V₀ = £20m without a population weighting, and SWEEPS §11 explicitly concedes that mechanism intensity varies materially with V₀ (correction magnitudes of 1–2pp at £20m versus 8–10pp at £500m). The revenue-relevant population is concentrated where the reference taxpayer is *least* representative.

What the series has: per-taxpayer indifference at one wealth point. What the enforcement claim requires: aggregate revenue invariance across the plausible population distribution of α, weighted by wealth. The second does not follow from the first. This is not the same as the acknowledged "population-level extrapolation" limitation in SWEEPS §11, which concerns whether the *incentive structure* generalises; the revenue-invariance step is a separate inference and is nowhere stated as an assumption.

**What is needed:** A population-weighted revenue calculation across the α distribution, using the RATES bracket populations, showing aggregate collection under (i) universal honest declaration, (ii) the predicted α ≈ 1.1 centre with a realistic dispersion, and (iii) a pessimistic left-skewed distribution. The series' own model (wdt_core, rates_model) can in principle produce this. It has not.

### 1.2 The α ≈ 1.1 behavioural centre is asserted, not derived (VAL.A §A.6, ENV §2) — **partially acknowledged**

VAL.A §A.6 Concept 3 argues: taxpayers face a ±10–20% error band; understatement loses refund protection; therefore a risk-averse taxpayer centres at α ≈ 1.1 so that the lower tail of their band stays in overstatement territory.

The inference requires an unstated premise: that the taxpayer's loss function is *sufficiently* asymmetric that the expected cost of the periodic overpayment from centring at 1.1 is exceeded by the expected value of preserved refund protection. No such comparison is performed. C.6 shows the refund-protection differential at g = −4.5% only, and only as a terminal-wealth ratio. The periodic cost of running at α = 1.1 across N = 30 is not netted against it. Given that C.12 establishes that the nominal advantage of mild overstatement *reverses* under a 5% discount rate, the discounted expected value of the refund-protection motive is precisely the quantity that has not been computed — and it is the only remaining support for the 1.1 prediction after C.12 removed the TW-advantage rationale.

The series labels this "a conditional prediction contingent on the assumed uncertainty and risk preferences." That labelling is honest about *empirical* status but not about *derivational* status: the paper presents 1.1 as following from a stated argument, and it does not. A specific ±band and a specific γ would yield a specific α*; none is computed.

**Load-bearing consequences:** ENV §9.2.1 and SCOPE #18 make the SRR floor calibration depend on this centre. If the centre is at 1.0 or below, the SRR adjustment direction reverses.

### 1.3 The "both offers are self-defeating" argument in INST is not exhaustive (INST Abstract, §6.2) — **unacknowledged**

INST claims the two constituencies cannot be separated because any executive offer must either weaken refund protection (collapsing declaration behaviour and hence the revenue base) or reduce the dividend (removing its fiscal source). The disjunction is presented as exhaustive.

It is not. A third option is available: maintain both the refund guarantee and the dividend at current levels, and capture the *growth* in WDT revenue for state priorities. Because the dividend is a level of labour tax relief already delivered, and WDT revenue grows with the wealth base, an executive can hold the dividend nominally constant while directing all incremental revenue elsewhere. Neither constituency experiences a withdrawal. The wealthy taxpayer's refund is untouched; the majority's payslip does not fall. INST's own clause-6 protection is directional ("net revenue above pre-existing obligations committed to reducing taxes on labour and consumption") and does not obviously bind against a freeze — GOV §5.2 clause 6 is a commitment to direction, not to pace, and RATES §6.3 treats pace as a Governing Council decision.

This is the classic hollowing mechanism POL §3.5 identifies as institutional brittleness, applied to the dividend rather than to the base. The series has an extensive account of how thresholds and exemptions drift, and no account of how dividend *pace* drifts. INST's central novelty — that the two constituencies are structurally inseparable — depends on the disjunction being exhaustive, and it is not.

### 1.4 The corporate instrument's asymmetry argument is invalid as stated (CORP §3, §5.5, MF §9.4.2) — **acknowledged as a compromise, but the argument given for it is unsound**

The claim: corporations do not experience losses in a humanly meaningful sense; shareholders' losses are captured through individual assessment; therefore no corporate-level refund is required.

The premise "shareholders' losses are captured through individual assessment" is false for exactly the population the corporate instrument exists to reach. Tranche-two holders failing the attribution test and tranche-three holders pay τ₀ or τ_h in gain years and receive nothing in loss years — and by construction they have no individual assessment through which the loss is captured. The set of positions the corporate levy collects from as a *final* charge is precisely the set for which the "shareholders are covered individually" defence does not hold.

CORP.A §B.2.2 treats this asymmetry as a deterrence *feature* (refund forfeiture substitutes for rate-based deterrence). That is a coherent position. But it is incompatible with the position in CORP §3 and MF §9.4.2, which presents the asymmetry as *principled* — as following from the individual-centred axiom rather than as a chosen deterrent. Only one of these can be the argument. The principled version is invalid; the deterrence version is valid but is a departure from the moral architecture, not a consequence of it, and MF §9 does not list it as a named compromise in that form.

### 1.5 CLOSE §4.3 threshold fall-through generates a refund on a non-loss (CLOSE §4.3) — **unacknowledged**

CLOSE specifies that on fall-through, "the final delta for a fall-through closure is the distance from the last declared basis to the threshold value: a negative delta in all cases."

Consider a taxpayer with declared basis £3m who falls to £2.5m against a £2m threshold. Their actual loss is £0.5m. CLOSE's rule computes the delta to the *threshold* — £1m — and refunds on that. The taxpayer receives a refund on £0.5m of wealth they still hold. The rule as written is not "refund the loss"; it is "refund down to the threshold." Repeated entry and exit across the threshold would extract refunds without corresponding losses, bounded only by the lifetime envelope.

The envelope caps the exploit but does not eliminate it: a taxpayer with a large accumulated envelope from prior contribution years can cycle across the threshold and convert envelope headroom into cash at a rate faster than their actual losses justify. CLOSE §6 addresses *re-entry* basis and envelope carry-forward but does not address the over-refund in the closing calculation itself. Either the delta should be computed to actual net worth at closure (not to the threshold), or the rule needs an explicit defence it does not currently have.

**Uncertain element:** it is possible the authors intend "threshold value" to mean the taxpayer's net worth at the assessment at which they are confirmed below threshold, in which case the text is simply ambiguous rather than wrong. If so, the wording needs correcting; if not, the mechanism needs correcting.

### 1.6 The FM non-decomposability argument proves less than claimed (FM §2)

FM argues that removing the symmetric refund destroys the valuation architecture, because "the penalty for lying is automatic and runs in both directions" and removing the refund removes the bad-year penalty.

VAL's own account contradicts the strength of this. VAL §5.2 and §7.2 establish that the dominant deterrent against understatement on Route C is the must-transfer dilution mechanism, which operates entirely in gain years and does not depend on the refund. On Route D, the deterrent is the basis-gap recovery at realisation plus the auction — again refund-independent. The refund-protection asymmetry is presented in VAL §7.3 as the source of the *mild upward bias*, not as the primary deterrent against understatement.

So a refund-less WDT loses the mild upward bias and the risk-sharing property, but retains the two mechanisms VAL identifies as doing the deterrence work. FM's claim that "understatement becomes straightforwardly attractive" without the refund does not follow from VAL. The non-decomposability claim is still defensible on Domar-Musgrave and cooperative-architecture grounds, but the *valuation-architecture* leg of it is overstated, and FM §2 and MOD §1 both rest on it.

---

## Layer 2 — Internal Consistency

### 2.1 LDW's headline purchasing-power figures are mutually inconsistent within the paper, and inconsistent with the Project Map

LDW §2.2 table: median earner current take-home £29,300 → post-WDT £39,039 → purchasing power equivalent "~£49,700," described as a "70% increase."

LDW §4.4 table: total annual gain £10,688, giving "equivalent purchasing power £49,727."

£29,300 + £10,688 = £39,988, not £49,727. The §4.4 table's own components (NICs £2,117 + income tax £5,294 + VAT £2,750 + energy £527 = £10,688) sum to a purchasing-power equivalent of approximately £40,000, not £49,700. The £49,700 figure appears to double-count the tax displacement: once in the move from £29,300 to £39,039, and again in the £10,688 total.

Separately, the Project Map states the same result as "£31,628 to approximately £43,144, a 36% increase." Neither of these pairs matches the other, and neither matches LDW §7.2's "£29,300 to approximately £49,200 — a 68% increase" (excluding energy).

**Which is better supported:** the arithmetic in LDW §2.1 (NICs £2,117, income tax £5,294 on the stated 2025/26 schedules at £39,039) is checkable and appears correct. The derived purchasing-power headline is not. The 70% claim is the single most-quoted figure from LDW and it does not survive its own table. This must be recomputed and reconciled across LDW, ENV §4.6, MF §6, POL §5.3, and WP §6.

### 2.2 RATES coverage claims are stated in at least three incompatible forms

- RATES Abstract and §3: "post-fill surplus equivalent to 6–15% of government expenditure at the hardest historical start and 125% at the median," where 6.4% is SSM 10yr and 14.6% is TCM 10yr for the 2000 start.
- RATES.A §A.6: "The SSM coverage ratio is average annual net SSM income over the capitalisation window divided by average annual government expenditure: 21.3% for the 2007 Balanced scenario... The TCM coverage ratio... 27.4%."
- FM §3.1: "coverage ratios of between twenty and forty percent of government expenditure during the capitalisation window at the worst-case reference scenario... median TCM coverage ratio of approximately sixty percent."

These are three different metrics (post-fill 10-year window; capitalisation-window average; and whatever FM is using) presented without discriminating language, and FM's "median approximately sixty percent" does not correspond to any figure in RATES or RATES.A, where the median 10-year TCM post-fill coverage is 125.5% and the median capitalisation-window figure is not reported as 60% anywhere. RATES.A §A.6 also flags a known boundary-alignment bug making the SSM and TCM ratios non-comparable, which is not carried forward into any paper that cites them.

**Which is better supported:** the RATES §7.1 post-fill window figures, which are generated directly from the sweep table. FM §3.1 should be corrected or its source identified. RATES.A's 2007-scenario figures are stale relative to the 2000 reference and are cited as if current.

### 2.3 Route D share of WDT-taxable wealth versus Route D share of revenue

BEHAV §8.2 puts Route D at 10–20% of WDT-taxable wealth, and uses this to bound the enforcement residual. BEHAV §8.2 then concedes Route D may cover "40–50% of the liability attributable to the top 500 taxpayers." RATES §7.1 establishes that revenue is concentrated in the Good and Great tiers (91% of aggregate) and heavily in upper brackets.

The enforcement-residual claim is stated in wealth-share terms and the fiscal exposure is in revenue terms. Since the entire enforcement argument is about whether the residual is fiscally material, the wealth-share framing is the wrong denominator and the paper knows it ("volume share and revenue share are not the same number") but proceeds to state the conclusion in volume terms anyway. BEHAV's conclusion — "the enforcement residual applies to a minority of WDT-taxable wealth, not the majority" — is true and irrelevant to the claim it is used to support. This is not merely imprecision: WP §8.1, the Project Map's core feasibility case, and FAL H4's cost accounting all inherit the volume-share framing.

### 2.4 WFR's Poor-tier envelope binding versus RATES's SRR sizing

WFR §4.3.5 and WFR.A §D.4 establish that the Poor tier's envelope binds in the *first* assessment year, and WFR §4.2.3 concludes that at the entry margin "the Arachi distortion applies in full" and that "the SRR requires capitalisation from non-WDT sources to honour early-year refunds for low-return entrants."

RATES §4 draws the opposite operational conclusion from the same mechanism: "The lifetime contribution envelope performs a structural role... refund exposure is automatically bounded by that history. The mechanism is self-limiting without any active Governing Council intervention." RATES §6.1 sizes the SRR against net annual income with no non-WDT capitalisation requirement, and RATES §7.2 reports SRR fill at year 3 invariantly.

Both cannot be right about the same early-year period. If the envelope binds and refunds are capped at zero, RATES is correct that SRR exposure is bounded and WFR is wrong to say non-WDT capitalisation is required. If WFR is correct that refunds must be honoured for early entrants (via an entry credit or pre-funding), then RATES's SRR sizing understates the requirement and the year-3 fill result is not robust to that design change.

**Which is better supported:** RATES is internally consistent with the envelope as specified in WP §3.5 and modelled in RATES.A §A.5. WFR §4.2.3's "policy implication" is a normative recommendation presented as a finding, and it is not reconciled with the envelope constraint it identifies. But WFR has correctly identified that the mechanism delivers *nothing* to a first-year loss entrant — which is a real design consequence the rest of the series does not carry. This needs resolving in one direction and propagating.

### 2.5 Full symmetry is "settled" but the corporate and closure cases are asymmetric, and GOV clause 2 does not distinguish

RATES §4 and WP §3.5 state full symmetry as a settled design position; GOV §5.2 clause 2 protects "refund symmetry" as an enumerated structural clause. But:

- CORP §5.5: no corporate refund in loss years.
- VAL §11.3: corrective over-declaration generates no refund.
- CORP.A §B.2.2: tranche-three positions forfeit refund access entirely.
- WFR §4.3.5: envelope binding produces zero refund for first-year loss entrants.

None of these is inconsistent with a *carefully stated* symmetry clause, but clause 2 as written ("the system recognises losses at a rate mirroring gain-year treatment") does not state its exceptions, and MF §7, POL §5.1, and INST §5.3 all rely on unqualified symmetry as the foundation of the cooperative architecture's moral claim. The exceptions are individually defensible; collectively they mean the symmetric refund is a property of the individual delta on attributed positions, not of the mechanism. A wealthy taxpayer evaluating INST's Condition 3 is entitled to know which of their positions carry the guarantee.

### 2.6 GOV.A §B.2 describes VAL's Route D self-correction in terms VAL contradicts

GOV.A §B.2: "An understated entry basis permanently reduces the delta base from which all future assessments proceed, compounding the advantage of understatement through the entire holding period."

VAL §1, §5.3, §7.2 and VAL.A §A.4.4: understatement on Route D *defers* liability; the basis gap is recovered in full at realisation, taxed at the full marginal rate with no smoothing, and the cost compounds *against* the understater.

These are opposite characterisations of the same mechanism. GOV.A's version supports a stronger case for the auction; VAL's version is the one supported by the simulation tables. GOV.A §B.2 should be corrected to VAL's account, which weakens (but does not eliminate) the auction's necessity argument.

---

## Layer 3 — Gap Coverage

### Type (c) gaps — unacknowledged, load-bearing

**3.1 No aggregate revenue model under the predicted declaration distribution.** Every revenue figure in RATES assumes α = 1 (RATES.A §A.5: "Declared wealth W_t is a fraction f_t of V_t, where f_t begins at 1.0" — f is the retained equity fraction, not a declaration ratio; α does not appear in the TCM at all). ENV §2 and VAL.A §A.6 predict a population centre above 1. SWEEPS §11 establishes mechanism intensity varies with V₀. No paper computes revenue under the predicted distribution. The Project Map's headline revenue claims, WP §5, and INST §7.1's resource-pool advantage all inherit an α = 1 assumption that the series' own behavioural work says will not hold.

*Closable internally:* yes. The existing model takes α as a parameter; running the TCM across a distribution of α by bracket is a straightforward extension.

**3.2 No model of revenue under route distribution.** BEHAV §8.2 establishes Route D at 10–20% of wealth and PHASE1 §4.4 notes "Phase One revenue from Route D taxpayers will be lower than the cohort model suggests until the first realisation events occur." RATES models all taxpayers as Route C (RATES.A §A.5). Route D taxpayers generate *zero* annual revenue during the holding period. If 10–20% of WDT-taxable wealth — concentrated at the top, where revenue concentrates — produces no annual delta revenue for decades, the SRR and LRR fill timelines are materially wrong and the year-3 SRR invariance result is not established.

This is the single largest unacknowledged quantitative gap in the series. PHASE1 §4.4 states the problem in one sentence and does not propagate it. RATES §9.1–§9.5 does not list it.

*Closable internally:* yes, and it should be, before any further reliance on the fill timelines. The required change is to the TCM: partition each bracket by route with Route D contributing only at a modelled realisation event.

**3.3 The corporate levy's interaction with the individual base is not modelled for double-provisioning.** CORP §5 provisions at the company level against the full market-cap delta including the native-shareholder tranche; those shareholders separately declare net worth including the listed holding, and settle individually. RATES §8.1 adds the corporate levy estimate (£172b) to the individual estimate (£874b) as "additive pre-behaviour." CORP.A §B.1 states explicitly that the provisional levy is escrow and that the tranche-one amount is *released* on settlement — i.e. it is not incremental revenue. The £172b figure is constructed from unattributable and unidentified tranches only (RATES §8.1's table shows £0 from the identifiable-and-attributable tranche), which is internally consistent — but the individual WDT figure of £874b is computed on total net worth including listed equity, and no check confirms the two bases do not overlap at the intermediary tranche. The "additive" claim is asserted, not demonstrated.

*Closable internally:* yes, by a reconciliation showing the corporate estimate's base is disjoint from the TCM's.

**3.4 No account of dividend pace drift as a hollowing channel.** See §1.3. POL §3.5 identifies institutional brittleness as operating through exemption creep and threshold drift; the dividend is the WDT's novel political asset and no paper models how it erodes. GOV clause 6 protects direction; nothing protects pace. INST's two-constituency argument, POL §5.3's organised-constituency argument, and FM §3.2's electoral-weight argument all depend on the dividend being *felt*, which depends on pace.

*Closable internally:* partly. A pace-protection mechanism could be specified within GOV's existing architecture. Whether it would hold is a Phase One question.

**3.5 No account of what the Taxpayer Chamber does to rate-setting.** GOV §1.1 argues TP's inclusion converts private lobbying into public argument. SWEEPS §7.2 derives TP's rational preference as "lower τ₀" with intensity scaling with wealth. GOV.B §A.1.3 gives each TP member an equal share. ADD §3.1 identifies that threshold drift produces mass enrolment of near-threshold members who would numerically dominate. No paper models the resulting rate trajectory. If TP's 25% plus any FS fraction plus any DR fraction sympathetic to lower entry burden produces persistent downward rate pressure, the RATES fill timelines — which assume canonical parameters held constant for 19–29 years — are not the right object. This is the "self-shaping problem" POL §7 names at the level of political interests but does not apply to the parameter trajectory.

*Closable internally:* only partially. A rate-trajectory model under the chamber structure is constructible but requires behavioural assumptions the series does not have.

### Type (b) gaps — acknowledged literature gaps, correctly identified

LR.A §3.1 (cooperative compliance under professional mediation), §3.2 (cross-base externality modelling), §4.1–§4.3. These are honestly stated. See Layer 4 for whether the series' reliance on them is proportionate.

### Type (a) gaps — Phase One, correctly assigned

PHASE1 §4's seven clusters and the register items #4–#6, #13–#16, #18, #29–#32. No objection to the assignment; objection in Layer 4 to the *weight* placed on items that are simultaneously assigned to Phase One and treated as established elsewhere.

---

## Layer 4 — Structural Soundness

### 4.1 Does RATES deliver what WP claims?

**Partially, and less than WP states.** WP §5 claims four properties "simultaneously... calibrated to represent the hardest historical starting conditions." RATES does establish, within its own model: SRR fill at year 3 across all 73 start years; LRR fill in all 73; burden figures at N = 30.

What it does not deliver, and what WP claims:

- **"The mechanism never fails."** This is a claim about a model in which every taxpayer is Route C, declares honestly, never migrates, and never dies. The 100% success rate is a property of the model's closure, not a stress result. RATES §9.2 concedes pre-behavioural status; WP §5 and the Project Map's "the arithmetic works, without exception" do not carry that qualification with equal force.
- **The Route D zero-revenue problem (§3.2 above)** is not in the model at all and is not in RATES's limitations register.
- **Fiscal replacement "viable at scale"** rests on the £1,073b combined estimate whose additivity is asserted (§3.3).

WP's §9.2 caveat is correct but is not proportionate to what §5 asserts. The gap between "the arithmetic works" and "a model with these five exclusions produces these numbers" is where the series is most exposed to a hostile reading.

### 4.2 Does VAL's tolerant zone bear the weight BEHAV and POL place on it?

**No.** BEHAV §8.1 uses the tolerant zone to convert the enforcement problem from "imprecision in general" to "the egregious tail." This is a legitimate use. But BEHAV then treats that conversion as establishing the enforcement paradigm shift, and the paradigm shift claim requires the aggregate-revenue step identified in §1.1, which VAL has not supplied.

Worse: SWEEPS §2.2 Figure 2.2b establishes that the tolerant zone *narrows with N*, reaching approximately α = 0.5–1.2 by N ≈ 55 and crossing below the VAL.A upper bound of 1.5 at N ≈ 40–45. VAL states the zone as α ∈ [0.8, 1.5] without an N qualifier; SWEEPS establishes it is an N = 30 property. The zone's lower boundary is *below* 0.8 at all tested N per SWEEPS §2.2b — meaning VAL's stated lower bound is conservative — but the upper boundary claim is horizon-specific and the papers that cite it (WP §3.8, §8.1, BEHAV §1.1 and §8.1, Project Map) do not carry the qualifier.

Additionally, VAL §14.2 and SWEEPS §11 both concede the zone is a single-reference-taxpayer result at V₀ = £20m, and SWEEPS §11 states plainly that "the canonical reference understates mechanism intensity for precisely the taxpayers who generate most WDT revenue." SWEEPS frames this as conservative for robustness claims; it is *not* conservative for the tolerant-zone claim, which is a claim that the zone is *wide*. A narrower zone at high V₀ means the forgiveness property that BEHAV relies on is weakest where it matters most. Neither VAL nor BEHAV states this.

**Verdict:** the tolerant zone is a real and interesting result about the mechanism's local incentive geometry. It cannot currently support (i) the aggregate-revenue-invariance claim, (ii) an unqualified statement of the zone's width across N, or (iii) the claim that the zone applies at the wealth levels where revenue concentrates.

### 4.3 Does the cooperative compliance architecture deliver what MF and POL claim, given LR.A §3.1?

**No, and the series is inconsistent about whether it knows this.**

LR.A §3.1 states the gap precisely: the cooperative compliance literature models individual decision-makers; the WDT's population decides through professional intermediaries; whether cooperative design features alter adviser compliance posture "the existing literature does not address." BEHAV §11.1 repeats this. PHASE1 §4.1 assigns it to cluster 1. MF §9.1 names it as a formal modelling gap. This is all correct and honest.

But MF §7 states three convergent arguments for the cooperative architecture and characterises the incentive-based one as "directionally well-grounded." POL §5.1 treats the symmetric refund's political reciprocity as resting on "three independent reasons," of which the incentive argument is one, and §5.7 uses the redundancy to argue for a lower failure rate. INST §5.2 states as a *condition* that "cooperation must be the path of least resistance" and asserts the WDT satisfies it. INST §6.2's entire two-constituency mechanism requires that wealthy taxpayers *actually* demand refund protection strongly enough to generate institutional pressure.

The chain is: cooperative design → adviser-mediated compliance posture → declaration behaviour in the tolerant zone → revenue → dividend → second constituency → accountability pressure. The first link is the acknowledged literature gap. INST treats the whole chain as Tier B ("derived implications") when its first link is Tier C at best.

The redundancy argument in POL §5.7 is the strongest available defence: the refund survives on D-M and moral grounds even if the incentive argument fails. That defence works for the refund's *existence*. It does not work for INST's argument, which needs the incentive channel to be live, nor for BEHAV's enforcement-paradigm claim, which needs advisers to transmit cooperative norms rather than optimise against them — and Klepper's finding, cited in LR.A §3.1, is that advisers *increase* strategic optimisation on ambiguous items. The tolerant zone is precisely a zone of ambiguity.

**This is the most serious structural weakness in the series.** A mechanism whose deterrence architecture deliberately creates a broad zone of tolerated ambiguity, administered to a population whose compliance decisions are made by professionals whose documented behaviour is to optimise within ambiguity, is not obviously stable at α ≈ 1.1. The plausible adviser-optimal position is the bottom of the zone, not above centre. Nothing in the series rules this out, and VAL.A §C.1 shows α = 0.8 produces a C.1 of only 0.19% at the historical mean — i.e. the zone's lower edge is close to costless at the reference taxpayer.

### 4.4 Does the revenue case establish what POL §5.3 needs?

**Not yet.** POL §5.3 needs the dividend to be (i) delivered, (ii) attributable, and (iii) large enough to generate an organised constituency. RATES establishes post-fill surplus of 6–15% of expenditure at the reference case, reaching the LRR floor at year 19. LDW's quantification of what that means at the household level is (a) arithmetically broken at the headline (§2.1) and (b) computed for the *mature, full-displacement* state, which LDW §1.1 explicitly says is not a projection of when it arrives.

The political argument requires the constituency to form during the vulnerability window POL §6 identifies. The revenue case delivers material displacement at year 19 in the reference scenario, year 13 at the median. POL §6.1 states the mitigations must accumulate "before a hostile government arrives." A 13–19 year gap between implementation and the constituency-forming benefit is three to five electoral cycles. No paper reconciles the displacement timeline with the vulnerability-window timeline. POL §6.7 concedes the vulnerability is irreducible; it does not concede that the *principal* mitigation it relies on (the organised majority constituency) is not available until the vulnerability window has already closed or the mechanism has already failed.

There is also a scale problem POL does not address. ENV §4.1 puts incremental disposable income during the capitalisation window at £300–500 per worker per year. That is a real but small benefit, and POL §3.3's own analysis of France establishes that diffuse benefits do not generate organised political defence. Whether £300–500/year is above the threshold at which a benefit becomes politically defended is exactly the question, and it is neither asked nor assigned.

### 4.5 A structural dependency the series does not state

RATES's SRR year-3 fill result is the foundation of: FM §3.1's first-mover timeline, POL §6.5's political threshold, INST §7.3's pre-built capacity advantage, and FAL H3's Path A. It is derived from a model with no Route D, no behavioural response, no migration, α = 1, and a fixed taxpayer cohort with no entry or exit. Each of those five exclusions pushes in the direction of faster fill. The invariance across 73 start years is a property of the return series, not of the exclusion set, and invariance under one dimension of variation is being read as robustness generally. This should be stated in RATES §9 and in every paper that inherits the result.

---

## Overall Verdict

The central mechanism is logically coherent. The delta base, the recognised-basis rule, and the symmetric refund fit together, and the claim that the state need not certify values in order to tax is a genuine and correctly argued reframing. Nothing in this report disturbs that core. The most serious problems are not fatal to the central claim but three of them are fatal to specific headline claims as currently stated: the revenue model excludes Route D and assumes α = 1 while the series' own behavioural work predicts neither holds (so "the arithmetic works without exception" is not established at the stated confidence); the LDW purchasing-power headline does not reconcile with its own table and is quoted downstream in four papers; and the enforcement-paradigm claim rests on a per-taxpayer indifference result being read as an aggregate-revenue-invariance result, which does not follow. All three are addressable within the series' own modelling framework and should be addressed before external circulation, because each is checkable by a hostile reader in under an hour.

The single most important unresolved issue is the one identified at 4.3: the entire cooperative equilibrium — and therefore the revenue base, the dividend, the second constituency, and INST's competitive argument — depends on professionally-mediated taxpayers settling at or above honest declaration within a zone the mechanism has deliberately made forgiving, while the only literature the series cites on professional mediation (Klepper 1989, via LR.A §3.1) predicts that advisers optimise strategically precisely where judgment is ambiguous. The series names this as a literature gap and then builds on the favourable side of it in MF, BEHAV, POL, INST, and FAL H3 without flagging that the adverse resolution — a population centre at the bottom of the tolerant zone rather than above its centre — is at least as consistent with the evidence cited. Until either the α distribution is modelled under an adviser-optimising assumption, or the revenue consequences of a left-skewed distribution are shown to be tolerable, the project's central empirical bet is undefended against the one piece of literature it has itself identified as most relevant.