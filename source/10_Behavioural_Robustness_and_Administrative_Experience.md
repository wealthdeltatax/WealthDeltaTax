---
title: "The Wealth Delta Tax: Behavioural Robustness and Administrative Experience"
shortcode: "BEHAV"
status: "active"
keywords:
    - Wealth Delta Tax
    - wealth taxation
    - behavioural robustness
    - tax compliance
    - tax avoidance
    - cooperative compliance
    - taxpayer behaviour
    - administrative burden
    - institutional legitimacy
    - membrane theory
    - behavioural responses
    - migration
    - enforcement
    - phase sequencing
---

### Revision History {.unnumbered .unlisted}

| Revision | Date            | Details                  |
|:--------:|:---------------:|--------------------------|
| 0.01      | 24 July 2026     | First Draft          |
| 1.00      | 15 August 2026  | Published to website |
| 1.01      | 14 September 2026 | Abstract updated to reference tolerant zone as bounding the enforcement claim; §8.11 reframed: Route D enforcement residual characterised as the egregious-understatement tail rather than a general valuation problem, referencing VAL §7.1 tolerant zone (α ≈ 0.8–1.5) and updated equilibrium framing (α ≈ 1.1 as conditional prediction, not dominant strategy); §8.12 closing paragraph extended to note tolerant zone substantially reduces the enforcement problem for the non-egregious declaration range; §9.2 new opening sub-section added noting the WDT is not a stock wealth tax and that Agrawal's ratio was calibrated to structurally different systems (directional risk retained, magnitude uncertain); §6.3 new paragraph added after interaction matrix on SWEEPS parameter separability as a structural contribution to Clarity and Fairness membrane dimensions |
| 1.02      | 18 September 2026 | §2.1 citation corrected: Londoño-Vélez & Avila-Mahecha prose reference converted to @LondonoVelezAvilaMahecha2025 cite key (journal version: *Review of Economic Studies* 92(4), 2624–2655) |
| 1.03      | 19 September 2026 | Restructured: supporting material (route distribution detail, membrane calcification monitoring, Agrawal seven-part response, secondary objections, membrane examples) moved to BEHAV.A companion paper; main paper compressed to core argument |

\newpage

# Abstract {.unnumbered .unlisted}

This paper addresses behavioural failure in wealth taxation: the tendency of tax systems to function only under the behavioural assumptions built into their design, and to become fragile or ineffective when taxpayers respond differently. It argues that behavioural robustness — the degree to which a mechanism's effectiveness is independent of any particular assumption about how taxpayers will behave — is a design property derivable from first principles, without requiring behavioural predictions the empirical record cannot supply.

Five friction types drive the most damaging behavioural responses to taxation regardless of headline rate: information friction, visibility friction, legitimacy friction, feedback friction, and compliance friction. Five design principles follow from this taxonomy. The paper introduces The Membrane — the layer of procedures, communications, defaults, and feedback loops through which taxpayers experience the institution — and analyses the interaction structure between its five health dimensions, showing how failures in some generate downstream degradation in others. Nine behavioural shapes from full cooperative compliance to active resistance define the range against which robustness is evaluated. The WDT's enforcement paradigm shifts from active detection to passive collection: unattributed ownership faces the highest rate by default; the tolerant zone (VAL §7.1, α ≈ 0.8–1.5) absorbs legitimate valuation imprecision; and the Route D residual applies to a minority of WDT-taxable wealth. The cross-base fiscal externality (@AgrawalEtAl2025) is the dominant empirical qualification and is addressed structurally rather than dismissed. Supporting material — the full route distribution analysis, the seven-part Agrawal response, the membrane calcification monitoring architecture, and worked membrane examples — appears in (BEHAV.A).

\newpage

# Glossary {.unnumbered .unlisted}

**Behavioural friction:** Any cognitive or administrative variable that makes honest compliance more costly, more uncertain, or less legible than avoidance or exit.

**Behavioural robustness:** The degree to which a tax system's effectiveness is independent of any particular assumption about how taxpayers will behave. A behaviourally robust system functions across the distribution of responses rather than only under the assumptions its designers found convenient to make.

**Behavioural shape:** One of nine identified categories of taxpayer response, ranging from full cooperative compliance (Shape 1) to active resistance and non-compliance (Shape 9). The shapes are not predictions about frequency; they are a complete map of the range against which robustness is evaluated.

**Compliance friction (Type V):** The direct cost of complying honestly with a tax system — professional advice, record-keeping, time spent navigating rules — which functions as a tax on honest engagement and can make avoidance or restructuring economically preferable to remaining within the base.

**Cross-base revenue loss:** The fiscal loss associated with wealth-tax-driven emigration that extends beyond the wealth tax itself to include income tax and VAT revenues attributable to the departing taxpayer, as documented in @AgrawalEtAl2025.

**Exit closure:** The event by which a taxpayer's WDT assessment position ends on jurisdictional departure. The mechanism settles the accrued running account without treating departure as an act requiring a fiscal penalty. The full position closure framework is in (CLOSE).

**Feedback friction (Type IV):** The experience of delay and unpredictability in the system's response to taxpayer action, which causes the institution to be experienced as unresponsive regardless of whether the substantive outcome is correct.

**Information friction (Type I):** Uncertainty about liability arising from complexity or ambiguity in the rules, which drives route-shopping and professional avoidance activity independently of the headline rate.

**Legitimacy friction (Type III):** Perceived procedural unfairness in the operation of the tax system, which erodes compliance outcomes even among taxpayers who would benefit financially from the system's continuation.

**Membrane calcification:** The tendency of a mature institution to preserve Membrane processes that made sense at implementation even when the taxpayer population and behavioural distribution have changed. Addressed in (BEHAV.A §B).

**Membrane health:** The aggregate condition of The Membrane across the five friction dimensions.

**Membrane-first sequencing:** The implementation principle that the administrative layer governing taxpayer experience must be operational before or simultaneous with the first assessment cycle, not developed in parallel with it.

**Phase One:** The implementation phase in which the mechanism is untested, the Membrane is unproven, and behavioural uncertainty is at its highest.

**The Membrane:** The permeable boundary between a tax system and the taxpayers it governs — the layer of procedures, communications, defaults, and feedback loops through which the taxpayer experiences the institution and through which the institution receives information from the taxpayer.

**Visibility friction (Type II):** The opacity of the relationship between what a taxpayer pays and what they receive in return, which causes the tax to be experienced as confiscation rather than participation.

\newpage


\newpage
# 1. Introduction

If you tax wealthy people heavily enough to matter, they will leave. This is not a fringe view. It is the default assumption of most people who have thought about wealth taxation for more than a few minutes, and it is durable because it is grounded in something real: wealthy people have exit options most people do not, and every wealth tax attempted so far has given them good reason to use them.

The WDT cannot prevent wealthy people from leaving. The question this paper addresses is whether a tax system can be designed to remain functional across the full range of behavioural responses it will encounter — including exit — rather than only under the behavioural assumptions its designers found convenient to make.

The emigration objection is structurally correct about existing systems. Under a realisation-based capital gains regime, a taxpayer who defers realisation, departs the jurisdiction, and crystallises their gain elsewhere has done exactly what a rational actor does when a system offers them no reason to stay. Most exit tax regimes are either absent, easily structured around, or set at rates that a sufficiently wealthy taxpayer finds net-positive to trigger. And international mobility compounds both problems: the taxpayer is not choosing between paying and not paying, but between jurisdictions competing for their presence on adversarial terms.

The WDT does not claim to win that game. It claims to change the game.

The symmetric loss refund is the mechanism by which it does so. For the first time in the history of wealth taxation, a taxpayer within scope has a financial partner in both directions: a system that shares in their losses at the same rate at which it participates in their gains. That is not an enforcement mechanism. It is a structural reason to remain engaged with the institution.

Behavioural robustness is a design property, not a prediction. It can be built in or left out. The sections that follow establish the friction taxonomy that drives damaging behavioural responses, the principles that follow from it, the concept of The Membrane and the interaction structure of its health dimensions, the nine behavioural shapes the mechanism must remain functional across, and the empirical basis for the enforcement paradigm shift claim.

\newpage

# 2. Why Behaviour Cannot Be Predicted

## 2.1 What the Evidence Shows

The cross-country literature on wealth taxation is more developed than it was a decade ago, and its primary lesson is not the one most people expect. The headline finding is not that wealthy people leave en masse, nor that they stay put and pay without complaint.

Norway is the most carefully studied case. Following an increase in the wealth tax, migration among affected taxpayers did increase — the effect was real and measurable. Revenues from the wealth tax also continued to grow. Both are simultaneously true.

Colombia tells a different story. @LondonoVelezAvilaMahecha2025 document responses substantially larger than those observed in Norway. Their analysis points toward something specific: the scale of the response tracks closely with the weakness of third-party reporting infrastructure. Where that infrastructure is thin, responses are large; where it is strong, responses are smaller. The rate appears in both cases but does not explain the difference.

@AgrawalEtAl2025 add a further layer. When wealth-tax-driven migration occurs, the associated income tax and VAT losses can be approximately six times the direct wealth-tax revenue loss. This finding belongs in any honest account of what the literature contains and is returned to in (BEHAV §9.2).

## 2.2 Why the Numbers Don't Travel

Those three findings describe three specific situations, each shaped by factors that do not transfer automatically. The norms that shape whether a wealthy person in a given country regards tax as an obligation or an imposition are not captured in any dataset. The degree to which taxpayers feel the system is operating in good faith shapes their responses in ways no study has reliably measured.

The literature is not uninformative. Strong third-party reporting tends to reduce avoidance responses; symmetric loss participation is more consistent with the Domar-Musgrave tradition than asymmetric treatment. What the literature cannot do is supply the magnitudes a designer would need to calibrate a mechanism against a specific predicted response in a specific future jurisdiction.

## 2.3 The Design Implication

Designing around specific predicted responses is an unstable foundation. A mechanism that only functions if migration stays below a certain threshold has absorbed a prediction as a design assumption. When the prediction is wrong, the mechanism inherits the error.

The alternative is to ask what properties the institution should have so that it remains functional across the range of things taxpayers might do. That shifts the design objective from prediction to robustness.

\newpage

# 3. Behavioural Robustness as a Design Objective

## 3.1 The Concept Defined

Behavioural robustness is the degree to which a tax system's effectiveness is independent of any particular assumption about how taxpayers will behave. A system calibrated to a specific migration rate is less robust than one that remains functional whether migration is higher or lower than anticipated. The question to ask of any design feature is not whether it produces the desired behaviour, but whether the mechanism continues to work if the behaviour turns out differently.

## 3.2 What Robustness Is Not

Robustness is not the same as behavioural prediction. Prediction asks what taxpayers will do. Robustness asks whether the mechanism remains functional across the range of plausible responses, including responses the designer did not anticipate. It is not a weaker form of prediction but a different objective.

Robustness is also not behavioural engineering. The WDT does shape incentives deliberately — the symmetric loss refund, the self-balancing valuation mechanism, and the lifetime contribution envelope all alter the rational calculus facing taxpayers. But the mechanism is not designed around the assumption that any particular incentive will produce any particular response reliably. It is designed so that the institution remains functional across the range of responses those incentives might actually produce.

## 3.3 The Same Logic Applied Twice

(GOV) confronts a structurally identical problem at the institutional level: it does not assume that appointed governors will behave well, but designs constraints that function under either assumption. This paper applies the same logic to citizens rather than governors. Where (VAL) addressed informational failure and (GOV) addressed institutional failure, this paper addresses behavioural failure — the tendency of tax systems to function only under the behavioural assumptions built into their design.

\newpage

# 4. Sources of Behavioural Friction

Robustness requires knowing what to be robust against. The magnitude of damaging behavioural responses is driven not primarily by headline rates but by a small number of friction types that operate largely independently of the rate. Five can be identified.

## 4.1 Type I — Information Friction

When the rules governing a tax are difficult to understand, taxpayers face uncertainty about their liability. That uncertainty is resolved in one of two ways: some taxpayers engage professional advice, which creates and sustains an avoidance industry whose commercial incentive is to find the boundary of the rules rather than stay within them; others avoid the taxed activity altogether. Both responses are reactions to uncertainty, not to the underlying rate. Information friction is the primary driver of route-shopping risk.

## 4.2 Type II — Visibility Friction

When the relationship between what a taxpayer pays and what they receive in return is invisible, the tax is experienced as confiscation. A tax whose reciprocal structure is opaque cannot generate the public legitimacy that sustains it through hostile political periods. Visibility friction is distinct from the size of the reciprocal benefit: a symmetric refund the taxpayer does not know about in advance produces a different behavioural relationship with the institution than one they were informed of before they needed it.

## 4.3 Type III — Legitimacy Friction

Perceived procedural fairness materially affects compliance outcomes — a finding robust across the cooperative compliance literature (Tyler, 1990; Kirchler, 2007; Gangl et al., 2015) and one that applies even among populations that would benefit financially from non-compliance. A tax experienced as structurally rigged faces legitimacy erosion no enforcement architecture can fully offset. Legitimacy friction is not the same as visibility friction: a perfectly transparent system can still be experienced as unfair.

## 4.4 Type IV — Feedback Friction

When the feedback loop between a taxpayer's action and the system's response is long and uncertain, the system is experienced as unresponsive. Unresponsive systems are worked around rather than engaged with. This is specifically relevant to the loss-refund mechanism: a refund that arrives slowly and unpredictably does not feel like partnership. It feels like a bureaucratic concession.

## 4.5 Type V — Compliance Friction

The direct cost of complying honestly — professional advice, record-keeping, time spent navigating rules — functions as a tax on honest engagement. Where that cost is high relative to the underlying liability, the rational response is to restructure away from the tax base, eliminating both the liability and the compliance burden in one move. Compliance friction falls disproportionately on the honest taxpayer, who bears the full cost, relative to one who has already paid for professional restructuring and no longer faces the system at all.

## 4.6 The Design Implication

The objective that follows is precise: the honest strategy should be the lowest-friction equilibrium. When honest compliance requires more effort, more uncertainty, and more cost than restructuring or exit, the institution has built its own fragility into its design.

\newpage

# 5. Design Principles for Behavioural Robustness

Each principle is stated as a requirement derived from the friction type it addresses.

## 5.1 The Clarity Principle

**Requirement:** The determination of liability must be clear enough that honest self-assessment is the path of least effort.

The test is not whether a lawyer can interpret the rule, but whether a taxpayer can apply it without one. A rule can be clearly drafted and still be ambiguous in application to a specific asset type or ownership structure; the relevant question is whether classification is a bounded problem rather than an open one.

## 5.2 The Reciprocity Principle

**Requirement:** The benefit structure of the tax must be as visible to the taxpayer as the liability structure, and that visibility must be active rather than passive.

A loss refund entitlement buried in legislation satisfies no version of this principle. Confirmation of that entitlement, delivered before the loss is realised, does. The Sovereign Wealth Fund contributes to Reciprocity at a population level by demonstrating that accumulated wealth is being deployed for broad public benefit.

## 5.3 The Fairness Principle

**Requirement:** The administrative exercise of the system must be consistent, transparent, and accountable to the same standards it applies to taxpayers.

Fairness here is procedural, not distributive. It is not a claim about whether the tax produces a fair outcome but about whether the process by which it is administered applies the same rules to everyone subject to it.

## 5.4 The Responsiveness Principle

**Requirement:** The system must respond to taxpayer action within a timeframe and with a predictability that makes honest engagement feel like engagement with something that is paying attention.

Responsiveness is not a customer service requirement. It is a structural property of cooperative institutions. An institution that responds slowly loses the informational and relational advantage that makes cooperative compliance possible.

## 5.5 The Accessibility Principle

**Requirement:** The direct cost of honest compliance must not exceed the cost of the avoidance strategies it competes with.

This is not a requirement that compliance be costless. It is a requirement that honest engagement not be systematically more expensive than dishonest disengagement. Where that condition fails, the institution is selecting against the taxpayers it most needs to retain.

## 5.6 The Personal Adviser Corps

The five principles above are systemic — they improve the average experience across the taxpayer population. The personal adviser is the individual-level complement.

At thirty-two thousand initial TP members the population is small enough to support high-touch professional delivery. Each adviser works with a specific taxpayer through their first assessment cycle, covering route classification, delta calculation, window election, and privacy election. The adviser's function is navigation and comprehension, not optimisation: they work for the state, explain the mechanism honestly, and have no mandate to minimise the taxpayer's liability. The comprehension gap that makes tax systems more navigable for the very wealthy is partially closed by design.

Advisers should be drawn from the professional compliance industry the WDT displaces. That workforce carries relevant skills — asset classification, valuation methodology, complex ownership structure analysis — currently oriented toward avoidance. The adviser role reorients those skills toward comprehension, converts a source of organised Phase One opposition into a constituency with positive interest in the mechanism's success, and builds institutional knowledge across a wide range of asset compositions. In Phase Two, Phase One advisers become the training pool.

\newpage

# 6. The Membrane

## 6.1 Definition

The Membrane is the permeable boundary between a tax system and the taxpayers it governs. It is not the mechanism and it is not the legislation. It is the layer of procedures, communications, defaults, and feedback loops through which the taxpayer experiences the institution and through which the institution receives information from the taxpayer. A mechanism can be sound while The Membrane is degraded. The two are distinct, and conflating them is one of the more common errors in tax system evaluation.

The five principles in (BEHAV §5) are properties of The Membrane: a tax system satisfies them to the degree that its Membrane transmits the right signals clearly in both directions. Where a principle is violated, it is almost always The Membrane that has failed, not the underlying mechanism.

## 6.2 Membrane Health

Membrane health is the aggregate condition of The Membrane across the five friction dimensions. What can be assessed is whether The Membrane has been designed with each friction type in mind, and whether observable outputs — communication clarity, refund processing times, dispute resolution processes, self-assessment completion rates — are consistent with a membrane that is functioning.

A degraded membrane is self-reinforcing. When taxpayers experience friction in honest engagement, they disengage. When they disengage, the institution loses the informational signal that would allow it to identify where The Membrane is failing.

## 6.3 The Interaction Structure of Membrane Health Dimensions

The five membrane health dimensions are not independent. Failures in some generate downstream consequences in others regardless of whether those others were independently healthy, and some degradation paths resist correction even when the underlying cause is removed.

**Clarity and Reciprocity — complementary.** The same rule clarity that removes uncertainty about what is owed removes uncertainty about what is owed back. In the WDT context, clear route classification removes route-shopping incentives on the liability side and simultaneously removes uncertainty about refund entitlement on the loss side. Observable signature: self-assessment completion rates and unprompted refund claim rates should move together; if they diverge — high completion, low claim rates — Reciprocity is failing independently of Clarity.

**Clarity and Fairness — complementary.** Ambiguous rules are experienced as selectively applied even when they are not. Where classification boundaries are clear, inconsistent administrative outcomes are legible as inconsistency rather than attributable to deliberate arbitrariness. Clarity is a precondition for Fairness being observable at all. Observable signature: dispute rates that remain elevated after rules are clarified signal a Fairness problem; rates that fall with clarification confirm Clarity was the binding constraint.

**Clarity and Accessibility — complementary (strongest relationship in the framework).** A simpler rule reduces both information friction and compliance cost simultaneously. The WDT's four-route architecture does its most important membrane work here: collapsing the valuation question from an open problem to a bounded classification problem reduces Compliance friction and Information friction in the same move. Observable signature: professional adviser engagement rates for routine cases; if these fall as route guidance improves, both dimensions are responding.

**Clarity and Responsiveness — tension.** More precise rules generate more edge-case queries. Efforts to improve Clarity through elaboration increase the volume of cases that fall into gaps between new categories. Responsiveness therefore requires its own resourcing rather than being assumed as a byproduct of clearer rules. Observable signature: query volumes per taxpayer after rule clarification exercises; if these rise rather than fall, Clarity investment has been elaborative rather than simplifying.

**Reciprocity and Fairness — asymmetric (most important relationship in the framework).** A system can deliver symmetric economics while being perceived as administered inconsistently — different processing times for different taxpayers, opaque valuation decisions, discretion exercised without explanation. The WDT's most acute Phase One vulnerability is here: the refund mechanism is symmetric by construction from the first assessment cycle, but the administrative exercise of that mechanism may not feel consistent for years. Reciprocity and Fairness therefore require independent maintenance. Observable signature: taxpayer satisfaction surveys and formal dispute rates disaggregated by wealth band and asset type; systematic variation across groups confirms a Fairness failure independent of Reciprocity delivery.

**Reciprocity and Responsiveness — complementary.** The refund mechanism's cooperative character is felt through timing, not just through entitlement. A refund confirmation that arrives promptly before a loss year converts the mechanism's symmetric commitment into a present-tense experience of partnership. Observable signature: refund processing time against subsequent declaration accuracy; if taxpayers who received prompt refund confirmation in loss years show higher subsequent declaration accuracy, the Responsiveness–Reciprocity channel is functioning.

**Reciprocity and Accessibility — neutral.** These two dimensions operate through largely independent mechanisms. Investment in one does not propagate to the other, making Accessibility the one dimension that must be resourced on its own terms.

**Fairness and Responsiveness — downstream.** Slow responses are eventually experienced as arbitrary, regardless of whether the underlying process is principled. A taxpayer waiting without status updates for a four-month refund decision does not experience that wait as a neutral delay. Responsiveness failures generate Fairness degradation over time even when no actual inconsistency exists.

**Fairness and Accessibility — downstream.** A system expensive to engage honestly is experienced as rigged toward those who can afford to disengage. Accessibility failures generate Fairness degradation through the perceived asymmetry they create, independently of whether the rules are in fact applied consistently.

**Responsiveness and Accessibility — resource tension.** These two dimensions compete directly for administrative resource. A membrane attempting to maximise both simultaneously faces a cost constraint that must be acknowledged. The appropriate sequencing follows from Phase One data: which dimension's degradation generates faster legitimacy erosion determines which receives first claim on administrative investment.

**The special status of Fairness.** Fairness is downstream of all four other dimensions and degrades independently through arbitrary administrative discretion that none of them can address. A membrane whose Fairness dimension has degraded cannot be restored simply by improving Clarity or Responsiveness; the legitimacy damage requires direct administrative accountability intervention. For practical monitoring purposes, Fairness degradation should be treated as a leading indicator of membrane failure rather than a lagging consequence.

| | Clarity | Reciprocity | Fairness | Responsiveness | Accessibility |
|---|---|---|---|---|---|
| **Clarity** | — | complementary | complementary | tension | complementary |
| **Reciprocity** | complementary | — | asymmetric | complementary | neutral |
| **Fairness** | complementary | asymmetric | — | downstream | downstream |
| **Responsiveness** | tension | complementary | downstream | — | resource tension |
| **Accessibility** | complementary | neutral | downstream | resource tension | — |

**Parameter separability and membrane visibility.** SWEEPS establishes that the WDT's four rate-function parameters are doing largely separable jobs, and that each parameter's consequences can be characterised in advance and stated publicly. A governing body whose calibration decisions are legible — where a vote on $\tau_0$ has publicly characterised consequences on fiscal speed, overstater correction timing, and entry burden simultaneously — satisfies a dimension of the Fairness and Clarity principles that opaque multi-parameter systems cannot. This is a structural contribution of the small lever set to membrane health: parameter separability reduces information friction (Type I) at the system design level, before the Membrane delivers any individual communication.

## 6.4 How the WDT Satisfies the Five Principles

The WDT mechanism satisfies most principles structurally; the remainder require Membrane-level administrative specification.

**Clarity** is addressed most directly by the four-route valuation architecture (VAL §4). The four-route architecture relocates complexity from an open valuation question to a bounded classification problem, which is a materially different experience for the taxpayer. The self-balancing mechanism (VAL §6) provides a defined process for challenge with known consequences. What the Membrane must supply is communications that allow a taxpayer to identify their applicable route without professional assistance in routine cases.

**Reciprocity** is addressed most directly and distinctively by the symmetric loss refund. The condition is visibility: the Reciprocity Principle requires, at the Membrane level, that every taxpayer within scope receive confirmation of their refund entitlement before they need to exercise it. The Membrane must also confirm promptly when a loss year triggers an entitlement, treating the confirmation as a present-tense demonstration of partnership rather than an administrative formality.

**Fairness** is most thoroughly addressed by (GOV): the three-chamber Governing Council, the dual-threshold voting rule, and the ten enumerated structural clauses collectively address the institutional conditions for procedural fairness. GOV's architecture constrains but does not eliminate Membrane-level failures — inconsistent administrative interactions, opaque dispute resolution. The Membrane must specify that decisions affecting individual taxpayers are accompanied by a statement of basis and a clear route to challenge.

**Responsiveness** is the principle least addressed by the WDT's existing mechanism design and the one that most directly requires Membrane-level specification. The mechanism sets no response-time standards, because response times are operational rather than structural. Any taxpayer action generating a system obligation should produce a confirmed acknowledgement within a defined period, followed by a substantive response within a further defined period.

**Accessibility** faces the most structurally embedded obstacle. The professional compliance industry currently profits from complexity; a system simple enough for honest self-assessment in routine cases removes a significant revenue source from that industry. Naming this clearly is a precondition for designing around it rather than assuming it away. The four-route architecture reduces compliance costs in routine cases by eliminating the open valuation question. The administrator's verification task is arithmetic confirmation — checking that the delta between two declared values is correctly calculated — not truth-discovery. The minimum-necessary-information principle follows from the mechanism's design: the administrator holding extra data does not improve compliance because the mechanism's own structure catches most errors regardless.

**Privacy compatibility** follows from the same architecture. Full privacy for any individual taxpayer is compatible with the WDT functioning identically in every dimension that matters for revenue, compliance, and cooperative architecture. Full privacy does not affect revenue, refund symmetry, the Route D auction deterrent, or the lifetime contribution envelope. The democratic-visibility goal and price discovery function for Route D assets are both served by aggregate statistical outputs. A privacy election is therefore a choice between two equivalent ways of participating in a mechanism that works identically either way. This reframing addresses legitimacy friction (Type III) among the specific taxpayer population where that friction is highest.

\newpage

# 7. The Nine Behavioural Shapes

The nine shapes below are not predictions about which responses will be most common. They are a complete account of the range — from full cooperation to active resistance — against which the mechanism and The Membrane must both be evaluated.

## 7.1 Shape 1 — Full Cooperative Compliance

The taxpayer understands their liability, values the reciprocal structure, files accurate declarations, and pays without seeking to minimise. The WDT mechanism handles this shape without difficulty. The Membrane requirement is low but not zero: a cooperatively compliant taxpayer who receives poor communication or inconsistent treatment will not necessarily remain cooperative.

## 7.2 Shape 2 — Passive Non-Optimisation

The taxpayer is compliant but disengaged. They pay what is asked, do not seek professional advice, and do not exercise entitlements they are not prompted to claim. The mechanism handles this shape adequately on the liability side; the problem is on the entitlement side. The Membrane must proactively surface entitlements — notifying the taxpayer of their refund entitlement before it is needed, prompting a challenge where one appears warranted.

## 7.3 Shape 3 — Active Optimisation Within the Rules

The taxpayer engages professional advice to minimise their liability within the rules as written. Rule-compliant optimisation is the expected response of a rational actor to a well-designed tax. The self-balancing valuation mechanism (VAL §6) handles this shape: an undervalued asset can be acquired by the state at the declared value, bounding optimisation without eliminating it. The Membrane requirement is primarily Clarity: the taxpayer optimising within the rules must be able to identify which optimisations are permissible without excessive professional assistance.

## 7.4 Shape 4 — Avoidance Through Restructuring

The taxpayer restructures their asset holdings to reduce exposure to the tax base. The WDT mechanism addresses this through the attribution test in (CORP), the lifetime contribution envelope (WP §3.5), and threshold design that limits disaggregation benefits. The Membrane requirement is primarily Fairness and Clarity: where restructuring is legal the system must not treat it as evasion; where it crosses into avoidance the rules are designed to prevent, that boundary must be communicated clearly enough that the taxpayer and their adviser understand it before the structure is implemented.

## 7.5 Shape 5 — Deferral and Timing Manipulation

The taxpayer manages the timing of realisations and declarations to shift liability between periods. The WDT mechanism is more resistant to timing manipulation than a conventional realisation-based tax because the delta base accrues annually. A taxpayer cannot defer the accrual of wealth by deferring a sale. The Membrane requirement is modest: multi-year patterns in declarations must be visible to the administering authority in a way that allows anomalous timing patterns to be identified without the taxpayer being presumed dishonest.

## 7.6 Shape 6 — Migration of Assets Without Personal Exit

The taxpayer retains personal residence but transfers assets to offshore structures outside the reach of the tax. The WDT mechanism addresses this primarily through the individual-as-subject principle (MF §3) and through the reporting requirements that flow from it. The Membrane requirement is significant and partially unresolved: guidance accessible without specialist international tax advice for the most common structures; acknowledgement that the most complex offshore arrangements remain outside practical self-assessment reach.

## 7.7 Shape 7 — Personal Exit

The taxpayer emigrates. The WDT mechanism addresses jurisdictional exit through position closure: the assessment position ends, the final delta is calculated, and any symmetric refund entitlement is honoured and settled. The mechanism does not impose punitive exit taxation; departure is treated as a legitimate termination event. The full exit closure framework is in (CLOSE §3) through (CLOSE §5). Beyond exit closure mechanics, the mechanism's response is structural: a tax system that loses taxpayers through departure at a rate that materially affects its revenue base has a problem that enforcement cannot solve. The Membrane requirement is to ensure that the departure process itself is clear and complete — a taxpayer who is leaving should be able to understand their final liability and close their account without professional assistance in routine cases.

## 7.8 Shape 8 — Partial Exit

The taxpayer maintains a formal presence in the jurisdiction while substantially offshoring their assets and economic life. This is harder to address than full emigration because the taxpayer's formal status remains within the system while their substantive engagement has largely left it. The WDT mechanism addresses this through the individual-as-subject principle combined with the residency determination rules developed in (JUR). The Membrane requirement is primarily Fairness: distinguishing continued residence from nominal presence without treating every taxpayer with offshore assets as a nominal resident.

## 7.9 Shape 9 — Active Resistance and Non-Compliance

The taxpayer does not comply, files inaccurately, or files in ways designed to misrepresent their position. The WDT mechanism addresses individual non-compliance through the standard enforcement architecture available to any tax authority. The self-balancing valuation feature reduces one dimension of non-compliance risk: the incentive to declare undervalued assets is bounded by the purchase option. The Membrane requirement is limited but important: where non-compliance results from confusion rather than intent, the membrane interventions for Shapes 1–6 reduce this population by making honest compliance easier. Where non-compliance is intentional, The Membrane cannot substitute for enforcement, but it can ensure that the experience of honest taxpayers is not degraded by the enforcement responses directed at non-compliant ones.

## 7.10 The Distribution as a Whole

The nine shapes are not equally populated and not equally important for revenue. Shapes 1 and 2 account for most taxpayers within scope. Shapes 3–6 account for most of the value at risk from avoidance. Shapes 7 and 8 account for most of the political visibility of behavioural response. Shape 9 accounts for the most direct enforcement cost.

A behaviourally robust mechanism does not need to eliminate any of these shapes. It needs to remain functional across all of them simultaneously.

\newpage

# 8. The Enforcement Paradigm Shift

## 8.1 Passive Collection Rather Than Active Detection

The enforcement paradigm of most wealth tax analysis assumes a detection contest in which the state tries to find hidden assets and sophisticated actors with large resources routinely win. That premise does not hold for the WDT's specific architecture.

Consider each hiding strategy in turn. Assets hidden through unattributed corporate structures: the attribution test means unattributed ownership faces $\tau_h$ by default. The state does not need to pierce the structure — it taxes it at the highest rate and places the burden of attribution on whoever wants to claim a lower one. Assets hidden illegally: every year an appreciating asset remains hidden off the books generates a compounding concealment cost, because surfacing it in the formal economy at any future point crystallises a larger liability than honest declaration would have. Realisation to cash: any realisation through the formal financial system creates a recorded delta; the lifetime contribution envelope means prior hiding does not reset the clock.

The genuine residual is the Route D entry basis. An asset that enters Route D at a dramatically understated basis is formally in the system but with every subsequent delta calculation wrong relative to true value. The Route D auction mechanism is the deterrent response. Two findings from VAL further bound this residual. First, the tolerant zone (VAL §7.1): at the canonical N = 30 horizon, declaration ratios from approximately α = 0.8 to α = 1.5 produce lifetime tax outcomes close to honest declaration — the basis update rule carries any gap forward and closes it at realisation. Second, the model-implied behavioural centre sits near α ≈ 1.1: a conditional prediction driven by refund-protection asymmetry under valuation uncertainty, not a wealth-maximising equilibrium. Route D's enforcement problem is the extreme tail of the declaration distribution — egregious understatement — rather than the whole of it.

## 8.2 The Route Distribution

The severity of the enforcement residual scales with the share of WDT-taxable wealth that classifies as Route D. The full asset-class walkthrough appears in (BEHAV.A §A). The directional conclusion is summarised here.

| Route | Asset classes | Estimated share of WDT-taxable wealth |
|---|---|---|
| A | Listed equities, bonds, pensions, cash | 40–55% |
| B | Property, agricultural land, illiquid alternatives with professional valuation | 20–30% |
| C | Self-declared fungibles | 5–10% |
| D | Private company equity, illiquid non-fungibles, collectibles | 10–20% |

Route D at 10–20% — with the upper bound applying only at the very top of the distribution where private company equity concentration is highest — means the enforcement residual applies to a minority of WDT-taxable wealth, not the majority. Three caveats follow.

First, Route D concentration is heavily skewed toward the very top. A route that covers 10–20% of aggregate WDT-taxable wealth might cover 40–50% of the liability attributable to the top 500 taxpayers. Volume share and revenue share are not the same number. The enforcement residual is bounded in wealth-share terms, but the fiscally relevant measure is revenue share, which is not the same quantity. Route D is concentrated at the upper tail of the wealth distribution — the brackets where revenue concentrates — and PHASE1 §5.4's measurement agenda should therefore track Route D's share of aggregate assessed liability, not only its share of taxable wealth by volume. The wealth-share figure establishes that the residual is a minority of the base; the revenue-share figure, once Phase One data exists, will establish whether it is a minority of the fiscal exposure.

Second, the estimates rely on wealth survey data that systematically undersample the top of the distribution. (JUR §2.4) flags that the WAS lost Official Statistics accreditation in June 2025 and undersamples above £3m. The true Route D share could be higher than these estimates suggest.

Third, the boundary between Route B and Route D is partly a taxpayer election. The equilibrium distribution across routes will depend on Phase One adoption behaviour — whether the compounding cost of understatement and the audit deterrent are sufficient to push Route D-eligible assets toward Route B in practice.

The conclusion is calibrated: the enforcement paradigm shift claim is defensible as a statement about the mechanism's architecture, but its practical significance scales with Route D's actual share of WDT-taxable wealth, which is a Phase One observable. VAL's tolerant zone strengthens that claim considerably: the enforcement problem on Route D is not imprecision in general, but egregious understatement specifically. The residual is real but substantially more bounded than a pure detection-contest framing would suggest.

\newpage

# 9. Principal Objections

## 9.1 The Wealthy Will Leave

The emigration objection holds that a wealth tax of sufficient magnitude triggers departure at a scale that renders the system unviable: the population most able to pay is also the population most able to exit.

The objection is correct that wealthy people have exit options ordinary people do not, and that some will use them. It is not, however, an argument against the WDT specifically — it is an argument against any wealth tax not designed to be robust against exit. The WDT's exit closure framework (CLOSE §3) through (CLOSE §5) settles the accrued running account at departure without treating exit as an act requiring a punitive fiscal response.

The objection also implicitly assumes that exit is the dominant response. Jurisdictional exit is Shape 7 in a nine-shape distribution. The population that departs is a subset of a population that predominantly stays, optimises within the rules, restructures, or defers. Designing around the assumption that Shape 7 is the modal response is a category error.

Membrane quality matters here too. A taxpayer who experiences the system as fair, reciprocal, and accessible has a weaker incentive to leave than one who experiences it as arbitrary and burdensome. The objection treats membrane quality as a fixed property of wealth taxation; this paper has established that it is a design variable.

The re-entry rule (CLOSE §6) provides a structural reason to return that no adversarial system can offer. A taxpayer's lifetime contribution envelope travels with them on exit and is restored on re-entry. The mechanism incentivises re-entry for the population whose continued participation generates the most revenue.

## 9.2 The Cross-Base Fiscal Externality

@AgrawalEtAl2025 find that wealth-tax-driven migration generates income tax and VAT losses approximately six times the direct wealth-tax revenue loss. This is the most serious empirical challenge the paper faces and is stated without softening. A wealth tax that triggers sufficient departure to generate cross-base losses at that ratio could be net-fiscally negative even while continuing to raise direct revenue.

The WDT is not a stock wealth tax. Every system in the Agrawal empirical record levies a charge on the accumulated stock of wealth regardless of whether it grew in that year. The WDT's tax base is the annual delta — the change in net worth above a cost-of-capital allowance. The revenue-weighted annual burden at RATES-canonical parameters is 0.35% of net worth, structurally below the 1–2% stock levy in every empirical study Agrawal draws on. Whether the structural differences reduce the migration ratio materially is a Phase One question, not an answerable prior. But applying the Agrawal ratio wholesale imports a behavioural prediction calibrated to systems with structurally different incentive properties. The honest framing: the Agrawal direction of effect is likely to apply; the magnitude is unknown and the structural differences give Phase One reason to expect a smaller ratio.

The six-to-one finding transforms the economics of membrane investment. Each departure event prevented by better membrane quality saves not only the direct WDT revenue attributable to that taxpayer but approximately six times that amount in preserved income tax and VAT base. An administration that treats the membrane as a secondary implementation concern is implicitly accepting avoidable cross-base losses at a six-to-one ratio. The Agrawal finding is therefore not only a warning about emigration — it is the strongest available argument for front-loading membrane investment, and it produces that argument from fiscal arithmetic rather than institutional preference.

The Governing Council can reduce rates in response to observed departure: a rate reduction that prevents enough departures to preserve more cross-base revenue than it sacrifices in direct WDT revenue is a net-positive fiscal move. No prior wealth tax design held this capacity. The Governing Council also has a timeline extension buffer: accepting a longer path to Phase Two in exchange for operating at lower rates that reduce the departure incentive. This trades time for retention, at the cost of delaying the labour tax relief dividend and extending the bootstrapping vulnerability window (POL §6).

A fuller treatment — the jurisdictional transfer caveat, the re-entry rule's temporal structure, and the formal possibility of net inward migration — appears in (BEHAV.A §D).

## 9.3 The Complexity Objection

The objection holds that any system sophisticated enough to be robust across nine behavioural shapes is too complex to be accessible, and therefore fails the Clarity and Accessibility Principles it claims to satisfy.

The complexity required for behavioural robustness lives in the mechanism and administrative architecture, not in the taxpayer's experience. A taxpayer does not need to understand the full four-route valuation architecture to file an accurate declaration; they need to understand which route applies to their assets and what value that route requires them to declare. The claim is not that the WDT's mechanism must be simple. The claim is that The Membrane must be clear.

## 9.4 The Membrane Is Undeliverable

The objection holds that the administrative layer described in this paper requires a quality of public administration no tax authority has demonstrated it can sustain at scale. This is an honest objection without a complete answer. It applies to implementation, not to design. The relevant comparison is not absolute: the WDT's administrative requirements should be measured against those of the alternatives, including the alternative of doing nothing, which carries its own administrative and fiscal costs.

## 9.5 Robustness Is Rebranding Failure

The objection holds that describing a tax system as robust across the distribution of behavioural responses is a sophisticated way of saying it will not work as intended. This is a rhetorical position rather than an analytical one. Every institution operates across a distribution of responses from the people it governs. The question is whether the institution is designed with that distribution in mind or assumes it away. Assuming it away does not produce a more effective institution — it produces a less honest account of what is being built.

\newpage

# 10. Phase Sequencing

## 10.1 Phase One — Implementation

The implementation phase is the period of highest behavioural uncertainty and highest institutional vulnerability. The mechanism is untested, The Membrane unproven, and taxpayers have not yet formed settled views about the system's fairness, responsiveness, or reciprocal character.

The Agrawal risk is most acute here. Phase One emigration is the worst-case scenario precisely because it happens before the institution has had the opportunity to demonstrate what it is.

Membrane investment is front-loaded and cannot be deferred. A membrane not functioning at design quality from the point of first taxpayer contact generates legitimacy friction that compounds into subsequent phases. The administrative architecture — notification systems, response-time standards, accessible self-assessment guidance, dispute resolution processes — must be operational before the first assessment cycle, not developed in parallel with it.

## 10.2 Phase Two — Stabilisation

The stabilisation phase begins when the first full assessment cycle has completed and the first observable behavioural data is available. Avoidance structures that did not materialise can be deprioritised; those that emerged can be addressed. Membrane failures that generated friction in Phase One can be identified and corrected with evidence rather than inference.

If Phase One membrane investment was effective, the distribution will be weighted toward Shapes 1–3. If it was insufficient, the distribution will be shifted toward avoidance and exit. Recovery is possible but costly: a taxpayer who restructured in response to membrane failure has already incurred that cost and has no automatic incentive to reverse it when the membrane improves.

## 10.3 Phase Three and Membrane Calcification

The mature institution has an empirical record calibrated against evidence rather than inference. Phase Three is also when membrane calcification risk — the tendency of a mature institution to preserve processes suited to an earlier taxpayer population — becomes most acute. The monitoring architecture that addresses this risk, including the mandatory publication of membrane health observables and the role of the Taxpayer Chamber as institutional monitor, is developed in (BEHAV.A §B).

## 10.4 Sequencing as a Design Variable

Behavioural robustness is not a property the institution either has or does not have at implementation — it must be built and maintained across time. The single most important sequencing decision is membrane-first: a mechanism operational before its membrane is ready generates Phase One friction that compounds. A membrane ready before its mechanism is fully tested can absorb early behavioural responses while the mechanism is refined.

\newpage

# 11. Limitations

## 11.1 Formal Modelling Gaps

The existing compliance literature does not address whether specific institutional communication choices alter adviser compliance norms in predictable ways. The OECD Cooperative Compliance programme found that certainty, predictability, and early disclosure arrangements improve compliance among sophisticated actors, but did not isolate the effect of any particular administrative feature. This is a gap in the literature's agenda, not merely a data availability problem.

The same structural point applies to the adviser-mediation concern identified in (LR.A §3.1). The compliance literature's finding that professional advisers increase strategic optimisation on ambiguous items is calibrated to extractive systems where the optimisation direction is clear. The WDT's tolerant zone is not a zone of legal ambiguity in the Klepper sense; it is a zone of valuation uncertainty within which both understatement and overstatement carry quantifiable costs. An adviser recommending systematic understatement within the zone is not optimising against the state; they are reducing their client's refund protection in the states where that protection is most valuable. The professionally rational advice and the cooperative outcome are aligned by the mechanism's cost structure, not by any appeal to cooperative norms.

Phase One cluster 1 (the distribution of declared α across the taxpayer population and the unprompted refund claim rate) is the first empirical test of whether this alignment holds in practice. Until that data exists, the adverse resolution cannot be ruled out, but it requires a specific form of adviser behaviour (systematic action against clients' measurable bad-year interests) that the existing literature does not predict and that the mechanism's structure actively works against.

## 11.2 Phase One Empirical Unknowns

The most acute unresolved exposure is the Agrawal net-effect question. The cross-base fiscal loss ratio cannot be quantified against membrane investment at the margin before Phase One data exists. Six responses to this risk are set out in (BEHAV §9.2) and (BEHAV.A §D); none resolves the underlying empirical uncertainty.

The route distribution estimates in (BEHAV §8.2) are the section most exposed to revision by Phase One data. The Route D estimate of 10–20% is the most uncertain and the most consequential for the enforcement paradigm shift claim: if Phase One route adoption shows Route D concentration significantly above the upper bound, the residual is larger than (BEHAV §8.2) suggests.

## 11.3 Structural Limits of the Design

BEHAV does not model behavioural outcomes, does not predict elasticities, and does not resolve the principal empirical unknowns. It sets out the design framework within which Phase One can generate evidence on those questions. What the paper establishes is that the mechanism's behavioural robustness derives from design properties — not from optimistic assumptions about taxpayer psychology — and that this robustness can be argued from first principles without requiring behavioural predictions the empirical record cannot currently support.

Membrane calcification (BEHAV.A §B) is the one form of institutional drift the design addresses least directly. The monitoring architecture described there is the best available response within the existing institutional design — a named architecture with specified instruments and actors, not a prevention mechanism.

## 11.4 Governing Council Calibration Parameters

No items in this paper.

\newpage

# 12. Conclusion

The folk knowledge is correct. Wealthy people do leave in response to taxation. They do restructure, defer, offshore, and depart. The frustration behind the emigration objection is not a misreading of reality — it is an accurate description of how every wealth tax designed so far has performed against a mobile, well-advised population with access to a global market in lower-tax jurisdictions.

The why is not mysterious. A realisation-based capital gains regime defers liability until the taxpayer chooses to trigger it, so departure before realisation exports the gain tax-free. Exit tax regimes are routinely structured around, or set at rates that make departure net-positive. And every jurisdiction is playing the same adversarial game — extracting as much as possible while offering as little as necessary. On that model, mobile capital will always find a way out, because the system offers nothing worth staying for that cannot be replicated elsewhere at lower cost.

The folk knowledge is therefore not a statement about the character of wealthy people. It is a statement about the character of the systems built so far. Every wealth tax attempted has been built on an adversarial model: the state extracts, the taxpayer minimises, and the outcome depends on whose advisers are better. The WDT does not improve that model. It replaces it.

The symmetric loss refund is the mechanism by which that replacement occurs. It is not a compliance incentive or a behavioural nudge — it is a structural commitment: the state participates in the taxpayer's losses at the same rate at which it participates in their gains. No existing tax system makes that commitment. No existing wealth tax offers a rational actor a financial reason to remain engaged with the institution that goes beyond the cost of exit.

The Membrane is the concept this paper introduces to make that change operational. The mechanism can be well-designed and still be experienced as adversarial if the administrative layer between the taxpayer and the system is opaque, unresponsive, or inaccessible. Clarity, Reciprocity, Fairness, Responsiveness, and Accessibility are not peripheral features. They are the properties through which the institution's reciprocal character is either demonstrated or undermined at every point of contact. The interaction structure of the membrane's health dimensions — established in (BEHAV §6.3) — shows that investment in some dimensions propagates to others, while failures in Fairness compound independently and resist correction. This structure matters for implementation sequencing.

The route distribution analysis establishes the empirical basis for the enforcement paradigm shift claim. Route D — the mechanism's most vulnerable point — likely covers a minority of WDT-taxable wealth by volume. The mechanisms whose self-correction is most active cover the majority. The cross-base fiscal externality is the most serious empirical challenge; the WDT has more structural responses available than any prior wealth tax design, including the rate calibration lever, the timeline extension buffer, and the re-entry rule's deepening incentive. Whether those responses are sufficient is a Phase One observable, not a prior.

The paper does not claim the WDT will end exit. It claims that a system designed for behavioural robustness — one that functions across the full distribution of responses including exit, that offers a rational actor something no adversarial system can offer, and that is administered through a membrane designed to demonstrate rather than undermine its reciprocal character — deserves a different answer to the emigration objection than the systems that have generated the folk knowledge so far.

The folk knowledge was earned. It does not have to be permanent.
