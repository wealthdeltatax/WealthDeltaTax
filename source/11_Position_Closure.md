---
title: "The Wealth Delta Tax: Position Closure"
shortcode: "CLOSE"
status: "active"
zenodo_doi: "10.5281/zenodo.XXXXXXX"
keywords:
    - Wealth Delta Tax
    - wealth taxation
    - position closure
    - tax assessment closure
    - death taxation
    - exit taxation
    - bankruptcy taxation
    - threshold exit
    - jurisdictional exit
    - re-entry
    - bridging facility
    - lifetime tax account
    - lifetime contribution envelope
    - tax settlement
---

### Revision History {.unnumbered .unlisted}

| Revision | Date            | Details                  |
|:--------:|:---------------:|--------------------------|
| 0.01      | 24 July 2026     | First Draft          |
| 1.00      | 15 August 2026  | Published to website |
| 1.01      | 11 September 2026 | Added §8.4: beyond-lifetime-cap exploitation surface and rationale for the cap |
| 1.02      | 20 September 2026 | Crosslinks to BEHAV.A §D added: §1.2 and §3 Agrawal cross-base externality passages now point to full seven-part response in (BEHAV.A §D); §4.4 bankruptcy section extended with GOV.B §E mandate gap note for bankruptcy refund procedure |
| 1.03 | 25 September 2026 | §4.1 substantially expanded: full death settlement sequence, marginal rate dependency problem, provisional $\tau_{W_death}$ mechanism, hard reset waiver, soft reset effects, heir basis mechanics, estate administration mandate gap; §5 renamed and generalised to closure bond facility covering death, exit and bankruptcy as procedural variants of one instrument; Glossary updated throughout; §9.5 extended; §10 conclusion updated. Added §4.5: incarceration and criminal forfeiture as a unified treatment; glossary entries for custodial suspension, forfeiture closure, and forfeiture resolution award; §9.3 and §9.5 updated |

\newpage

# Abstract {.unnumbered .unlisted}

This paper establishes the general theory of WDT position closure: the set of events by which an individual's WDT assessment position ends, and the mechanisms the WDT uses to settle each one. Its central claim is that death, jurisdictional exit, threshold fall-through, and bankruptcy are structurally the same kind of event (the assessment position closes), and that the WDT already possesses, or can straightforwardly derive from existing machinery, a principled settlement procedure for each. The paper's conceptual contribution is the abstraction itself: shifting from a conventional exit-tax framing to a general account of how a delta-based assessment position closes, what the mechanism owes the individual at closure, and what the individual owes the mechanism. It further establishes the re-entry rule governing individuals who re-enter the WDT's scope after a prior closure, and confirms that the lifetime contribution envelope is a property of the individual rather than of the assessment position, persisting across closures and re-entries. This paper does not model the revenue or behavioural consequences of any closure event type, resolve the constitutional and legal design of exit taxation provisions in any jurisdiction, or address the international coordination arrangements Phase Two re-entry rules will require.

\newpage

# Glossary {.unnumbered .unlisted}

**Closure bond facility:** The SWF-provided settlement instrument that decouples interim activity from final WDT settlement across all closure event types where a Route D auction is required and non-Route-D assets or distributions need to proceed before that auction completes. Operates through a bond structure under which the estate, executor, practitioner, or departing taxpayer posts security for an expected positive delta, and the SWF posts security for an expected negative delta. The facility has three procedural variants — exit, death, and bankruptcy — differing in who initiates and what interim activity is decoupled, but sharing identical bond mechanics and netting-on-settlement logic.

**Custodial route reclassification:** The automatic reclassification of all assets held within a WDT assessment position to Route D upon legal freezing by a competent authority. Reclassification follows from the assets' loss of the properties that define their normal routes: a frozen asset cannot be transferred in Route C settlement, cannot be professionally valued at a price reflecting free transferability, and cannot be liquidated to settle a cash obligation. The reclassification is temporary; assets revert to their normal route classification when the freeze lifts or, where forfeiture follows, the position closes under (CLOSE §4.5).

**Closure event:** Any event by which an individual's WDT assessment position ends. The closure event types recognised by this paper are death, jurisdictional exit, threshold fall-through, bankruptcy, and criminal forfeiture. Each triggers the same general settlement sequence, with event-specific procedural differences.

**Death auction waiver:** A Governing Council calibration parameter specifying the maximum period since a qualifying hard basis reset within which the inheritance auction may be waived at death. Where a hard reset occurred within that period, the reset price serves as the Route D input to W_death without a further auction, and the heir enters at the reset price as their opening basis. The appreciation from last reset to death is deferred into the heir's future delta rather than taxed in the deceased's estate. The waiver period is a named trade-off between administrative simplification and the deferral it creates.

**Exit valuation service:** The taxpayer-initiated process that opens formal valuation on Route D assets at the declared exit date, using the inheritance-auction machinery described in (VAL §6.5), with the taxpayer's own declared annual values serving as the opening bid floor.

**Forfeiture closure:** A closure event triggered by criminal forfeiture of assets from an individual's WDT assessment position. The position closes at the point legal ownership transfers to the enforcement authority. The final delta is calculated from the last declared Route D basis to the forfeiture value; any negative delta generates a refund entitlement bounded by the lifetime contribution envelope in the normal way. Forfeited assets pass to the enforcement authority as an unattributed tranche-three position under the corporate levy, bearing $\tau_h$ until attribution to a human beneficial owner is established.

**Forfeiture resolution award:** A share of the value of forfeited assets, paid to named enforcement personnel involved in the seizure on confirmation that those assets have been attributed to a human beneficial owner. The award converts an unattributed tranche-three position to an attributed one, ending $\tau_h$ accrual. Its size is a Governing Council calibration parameter; it is calculated on the asset's value at forfeiture, not on $\tau_h$ accrued during the unresolved period, to avoid creating an incentive to delay attribution.

**Hard basis reset:** Voluntary settlement of a Route D liability using an auction to establish market value, rather than self-declaration. The auction price becomes the new recognised basis. Performing a hard reset before death establishes a market-verified basis that may waive the inheritance auction requirement and simplifies estate administration.

**Position closure:** The general condition in which an individual's WDT assessment position ends and a final settlement is calculated. Distinct from position suspension, which does not occur under the design proposed here: all events that might have been treated as suspension are instead treated as closure events, with re-entry above the threshold treated as a new first entry.

**Provisional $\tau_{W_death}$:** The marginal rate calculated from a provisional W_death — the deceased's total declared net worth established from all non-Route-D assets at their determined values plus the Route D component at the last declared or reset basis — used to settle non-Route-D liabilities before the inheritance auction completes. Final settlement adjusts for any difference between provisional and final $\tau_{W_death}$ once the auction establishes the true Route D value.

**Re-entrant:** An individual who previously held a WDT assessment position, experienced a closure event, and subsequently re-enters the WDT's scope, either by returning to the jurisdiction after exit or by rising back above the exemption threshold after threshold fall-through.

\newpage
\tableofcontents
\newpage

# 1. Intellectual Context and Prior Literature

Existing tax systems handle the events this paper groups under position closure through separate, largely unconnected legal regimes, each with its own design logic, its own literature, and its own characteristic failure mode. None treats them as instances of a single underlying problem.

## 1.1 Conventional Exit Tax Design

Exit tax regimes in most developed jurisdictions take the form of deemed-disposal provisions: the taxpayer is treated as having sold all assets at market value on departure, generating a taxable gain settled before or at exit. The design logic is deterrence. The structural failure is well-documented: deemed-disposal creates compelled liquidation pressure on illiquid assets, generates constitutional challenge on proportionality grounds, and concentrates friction on taxpayers with the longest tenure and most illiquid holdings. The deterrence effect is also weak relative to that friction, since a taxpayer who has decided to leave permanently will accept a one-time cost that a continuing participant would not.

The academic literature has largely accepted the deterrence framing, debating rates, unrealised gains, and constitutional limits. The WDT's position closure framework rejects it, treating exit as a legitimate termination event rather than an avoidance act requiring a fiscal penalty.

## 1.2 The Wealth Tax Migration Literature

The empirical literature on wealth tax migration provides the most relevant evidence base for assessing exit responses to a wealth tax. Its principal finding, surveyed in (LR.B §7), is that behavioural response magnitude is driven primarily by the quality of third-party reporting and the degree of jurisdictional arbitrage available, not by headline rates or exit penalty provisions. @JakobsenEtAl2024 find that Norwegian wealth tax increases generated approximately 22 cents of revenue loss per unit raised from migration, with overall revenues continuing to grow (a modest real migration effect in the absence of punitive exit provisions). Why behavioural response magnitudes vary so substantially across jurisdictions and what that implies for the WDT's administrative design is developed in (BEHAV §2).

The more structurally significant finding is that of @AgrawalEtAl2025, who establish that wealth-tax-driven emigration generates income tax and VAT losses approximately six times larger than the direct wealth-tax revenue loss. This cross-base externality is the fiscal argument most commonly advanced for punitive exit taxation: if losing a high-wealth resident costs six times as much in parallel tax bases, the case for deterrence through exit penalties seems strong. The WDT's response is structural: in a mature Phase Two context where those parallel taxes have been displaced by WDT revenue, the externality disappears. The Agrawal et al. case for punitive exit taxation applies only in Phase One, and only transitionally. The full treatment, including the argument that the externality strengthens the case for membrane investment in administrative experience, is in (LR.A §3.2) and (BEHAV §9.2). The seven-part structural response — the jurisdictional transfer caveat, the rate calibration lever, the timeline extension buffer, the re-entry rule's temporal shape, the immigration possibility, and the formal break-even framing — is in (BEHAV.A §D).

## 1.3 Insolvency and Taxation

The interaction between insolvency proceedings and tax obligations is extensively treated in jurisdiction-specific legal literature but has received little systematic treatment in tax design literature. Across most developed jurisdictions, tax debts occupy a defined priority position within the creditor waterfall, subordinate to secured creditors and sometimes senior to unsecured creditors, varying substantially by jurisdiction. Wealth taxes are rare enough that their specific treatment in insolvency is not well-established in most places. The WDT's position (creditors first, WDT claim subordinate) is a deliberate design choice, not an inheritance from existing practice; its rationale is in (CLOSE §4.4).

## 1.4 What the Literature Leaves Unresolved

The unifying gap across these three bodies of work is the absence of a general theory of account closure for an ongoing wealth assessment relationship. Conventional exit tax design treats exit as a special case requiring a special deterrent. The migration literature treats emigration as a behavioural response to be modelled and mitigated. The insolvency literature treats tax obligations as one creditor claim among many. None asks the prior question: what does a mechanism built on an ongoing assessment relationship owe the individual when that relationship ends, and what does the individual owe the mechanism? CLOSE proposes that answering it produces a general framework within which exit, death, threshold fall-through, and bankruptcy are all instances of the same underlying event.

\newpage

# 2. The General Theory of Position Closure

A WDT assessment position is the running relationship between a taxpayer and the mechanism: a declared basis, an accumulating delta record, a lifetime contribution envelope, and a set of entitlements and obligations that evolve across assessment periods. This paper is about how that relationship ends.

The design literature on wealth taxation handles endings badly. Inheritance receives specialised treatment through a separate estate tax regime with its own base, rate structure, and administration. Exit receives adversarial treatment as a form of avoidance that exit tax provisions are designed to deter (MF §9.4.4). Bankruptcy is handled through insolvency law that interacts with the tax system in ways that are largely jurisdiction-specific and not designed with a wealth tax in mind. Threshold fall-through (the event where a taxpayer's wealth drops below the exemption threshold) is rarely treated as an event at all; it is simply the absence of further assessment.

If the individual is the only legitimate subject of the tax (MF §2), and if the mechanism's obligations to the individual (above all the symmetric loss refund) are real commitments rather than administrative parameters, then how the position ends is a substantive design question. The mechanism owes the individual a correct final settlement regardless of why the position is closing. The individual owes the mechanism a correct accounting of the position's state at closure, regardless of whether they are dying, departing, falling below threshold, or entering insolvency.

Death, jurisdictional exit, threshold fall-through, and bankruptcy are structurally the same kind of event: in each case, the assessment position closes. The assets that constitute the position are valued, the outstanding delta is calculated, the mechanism's obligations to the individual (or their estate, or their creditors) are honoured, and the position is settled. The destination of the assets after closure (to heirs, to a foreign jurisdiction, to creditors, or simply to a smaller portfolio below the threshold) is irrelevant to the settlement logic. It is relevant to the procedural mechanics, which differ across closure event types and are addressed in (CLOSE §4). The underlying logic is the same in each case, and the WDT's existing machinery handles all four.

The abstraction is not merely conceptual tidiness. It closes a design gap that would otherwise require a patchwork of event-specific provisions, each with its own loopholes. A conventional exit tax that treats departure as a special case invites comparison to inheritance treatment, creating pressure for parity and administrative complexity. The WDT's position closure framework applies the same settlement logic regardless of the triggering event, with procedural adjustments only where the event-specific circumstances require them.

Two further concepts are established here before the taxonomy develops.

Position closure is not the same as position suspension. Treating threshold fall-through as suspension (the position going dormant until the taxpayer re-enters the threshold) would require maintaining a live position record for an individual who is not being assessed, creates ambiguity about the lifetime envelope's status during the dormant period, and introduces a re-entry mechanics problem that does not arise if fall-through is treated as a clean closure. The simpler and more consistent treatment: fall-through is a closure event, re-entry above the threshold is a new first entry. This is developed in (CLOSE §4.3).

The lifetime contribution envelope is a property of the individual, not of the assessment position. When a position closes, the envelope does not close with it. The individual carries their accumulated envelope balance (the record of contributions made and refunds received across all prior positions) into any future position they open. A re-entrant inherits their prior envelope balance; they do not start fresh. The state's commitment to the individual persists across the administrative fact of position closure (MF §2).

The auction infrastructure that operates at death closure (VAL §6.5) and at exit closure (CLOSE §4.2) also operates in a non-closure context: the (GOV §6.1) / (GOV.B §G) compelled mid-position revaluation for confirmed Route D outliers. All three use the same mechanics (open bidding at the declared value as floor, only third parties may bid, the taxpayer holds a right of first refusal at the highest third-party bid, and the winning price establishes a new recognised basis). The closure auctions and the mid-position auction are triggered by different events and serve different purposes, but share a common institutional form. The auction infrastructure is a standing feature of the Route D architecture, not an instrument improvised for each context separately.

The closure bond facility described in (CLOSE §5) operates across all three closure event types in which Route D assets require auction — death, exit, and bankruptcy. It is a single instrument with three procedural variants, not three separate mechanisms. What varies is who initiates the bond process and what interim activity is decoupled; the bond mechanics are identical across all three. This unification follows directly from the general theory: if death, exit, and bankruptcy are structurally the same kind of event, the instrument that manages the timing gap they create should be the same instrument.

\newpage

# 3. What the Mechanism Owes at Closure

The mechanism's obligations at the point of closure are the same regardless of which closure event has triggered settlement.

The mechanism owes the individual a correct calculation of the final delta. Whether the final period ends at death, at a declared exit date, at the threshold, or at the point of insolvency, the delta is calculated in the standard way: current net worth (or the threshold, in the case of fall-through) minus the prior declared basis, adjusted for the assessment window and rate function. No haircut or penalty is applied to the final delta calculation by reason of the closure event type.

The mechanism owes the individual (or their estate) the symmetric refund on any negative final delta. If the terminal net worth is below the prior declared basis, the refund obligation fires at the applicable marginal rate. The state's commitment to accept downside exposure alongside the taxpayer (MF §7) does not diminish because the individual is dying, departing, or insolvent. The refund flows to whoever has the legal claim on the individual's assets at closure: their estate in the case of death, their creditor pool in the case of bankruptcy, the individual themselves in the other cases.

The mechanism is owed a correct accounting of the position's state at closure: declared values for all assets across all routes, a complete lifetime envelope record, and cooperation with the valuation process where Route D assets require auction. The annual reporting trail is the mechanism's principal verification tool. An individual who has reported honestly across the life of the position faces a straightforward closure process. An individual who has systematically understated finds that the floor established by their own prior declarations is the starting point for final valuation.

The WDT does not impose punitive exit taxation. It does not penalise departure, deter it through border charges, or treat the act of leaving as something requiring a coercive fiscal response. If the mechanism is a reciprocal relationship (the state accepting downside exposure through the symmetric refund, the taxpayer participating in a governance structure that gives them a stake in the institution), treating exit as an act requiring punishment contradicts the foundational claim. A punitive exit provision signals that the mechanism does not trust its own design to retain participants. The full response to the emigration objection (including the argument that jurisdictional exit is one behavioural shape among nine, that membrane quality determines exit rates, and that the re-entry rule provides a structural reason to return) is in (BEHAV §9.1) and (CLOSE §9.3).

The enforcement work at exit is done by the annual reporting trail and the correct closure settlement, not by a border penalty. Adding a coercive layer is both unnecessary and inconsistent with the mechanism's posture toward every other closure event type.

The cross-base fiscal externality identified by @AgrawalEtAl2025 (income tax and VAT losses approximately six times larger than the direct wealth-tax revenue loss from emigration) is sometimes cited as the fiscal justification for punitive exit taxation. Punitive exit provisions do not recover income tax and VAT base; they operate on the WDT's own base only. The externality is also a Phase One transitional exposure that resolves structurally in Phase Two when those parallel taxes are displaced by WDT revenue. The fuller treatment is in (CLOSE §9.2). The seven-part structural response — including the rate calibration lever, the re-entry rule's temporal structure, and the formal possibility of net inward migration — is in (BEHAV §9.2) and (BEHAV.A §D). The response to the compulsion objection is in (CLOSE §8.1).

\newpage

# 4. The Four Closure Event Types

## 4.1 Death

Death most fully exercises the WDT's settlement machinery and raises the greatest number of procedural questions. (VAL §6.5) specifies the Route D inheritance auction mechanism; (GOV.B §G.8) specifies the auction's operational conduct. This section establishes the full settlement sequence across all routes and addresses the procedural and timing consequences that follow.

**The marginal rate dependency problem.** The WDT taxes each route's final delta at $\tau_{W_death}$ — the marginal rate applicable to the deceased's total declared net worth at death. That aggregate cannot be established until all assets across all routes have been valued. Routes A and B require professional valuations triggered at the date of death. Route C settles at the last declared value through the must-transfer mechanism. Route D requires the inheritance auction to complete. Only once all route values are in hand can W_death be computed, and only then can the final tax liability on any individual route be calculated — the rate that applies to the Route A asset depends on what the Route D auction established.

Nothing can be finally settled and released from the estate until the slowest-resolving asset class closes. For an estate with significant Route D holdings alongside Routes A, B, and C assets, all distributions are blocked pending the auction's completion. This is the correct application of the marginal rate logic, not a design flaw, but it is a real administrative burden that the provisional $\tau$ mechanism and the closure bond facility exist to manage.

**Provisional $\tau_{W_death}$ and the closure bond facility.** Where Routes A, B, and C are valued and the Route D auction is still running, the estate executor may establish a provisional W_death from all determined asset values plus the Route D component at the last declared or reset basis. A provisional $\tau_{W_death}$ is calculated from that figure, and tax on Routes A, B, and C is provisionally settled at that rate. The closure bond facility (CLOSE §5) then operates: the estate posts a bond covering the potential upside if the auction establishes a Route D value above the provisional basis, pushing W_death into a higher bracket; the SWF posts a bond to the estate covering the potential downside if the auction comes in below, reducing W_death and meaning the estate overpaid provisionally. Both bonds net on final settlement once the auction completes and the true $\tau_{W_death}$ is established. This allows the estate to begin partial distribution to heirs while the Route D auction runs, rather than freezing all assets until it completes.

**The settlement sequence in full.** Once $\tau_{W_death}$ is established — provisionally under the closure bond facility or finally after all routes complete — the sequence is:

For Routes A and B: the professional valuation at death date is the realisation value. The final delta is that value minus the last declared basis. Tax is calculated at $\tau_{W_death}$ and settled from estate liquid assets.

For Route C: the must-transfer mechanism settles at the last declared value. The delta is calculated in the standard way and the equity interest transfers to the estate at that value. The heir receives the interest at the declared value as their opening WDT basis if their resulting net worth exceeds W_min.

For Route D: the inheritance auction triggers automatically at the transfer event. The last declared basis is the opening floor. Third-party competitive bidding establishes a market price. The estate holds the right of first refusal at the highest third-party bid. If the estate exercises retention, it pays WDT on the upward delta (auction price minus last declared basis) at $\tau_{W_death}$. If it allows the sale, the proceeds are cash; the delta calculation is identical and the tax is settled from proceeds. The heir's WDT entry basis is the auction price in either case.

All WDT liabilities across all routes are a first charge on the estate, settled before any distribution to heirs.

**The symmetric refund at death.** If any route produces a negative final delta — the asset is worth less at death than the last declared basis — the symmetric refund applies in full. The refund flows to the estate and distributes to heirs through estate administration, increasing the estate's liquid assets and the heir's opening inherited net worth. The mechanism does not withdraw the symmetric protection because the taxpayer has died.

**Heir basis and basis compression.** After all WDT liabilities are settled, the remaining assets distribute to heirs through ordinary succession. The heir enters the WDT — if their resulting net worth exceeds W_min — as a fresh first-time entrant. Their opening basis is what they actually receive after WDT settlement, not the gross asset value before settlement. A Route D asset that auctioned at £30m with £3m WDT liability settled from the estate leaves the heir with £27m from that asset; their opening basis is £27m. This compression is a consequence of taxes being settled first, not a designed feature, but it is the correct treatment: the heir begins from their actual inherited position. The deceased's lifetime contribution envelope does not transfer to the heir; the heir starts with a clean envelope, consistent with the individual-as-subject axiom (MF §2).

**Hard resets before death.** A taxpayer who performs a voluntary hard basis reset on Route D assets before death achieves several advantages for their estate. The reset establishes a market-verified price through competitive bidding at the taxpayer's own declared value as floor. This market-verified basis may, depending on how recently it occurred, waive the inheritance auction requirement at death under the death auction waiver mechanism (see §4.1.1 below). Even where the waiver does not apply, a recent hard reset brings the declared basis close to the likely auction price, reducing the final delta, compressing upward pressure on W_death, and minimising the difference between provisional and final $\tau_{W_death}$ — which reduces the bond posting required under the closure bond facility and accelerates final settlement.

A soft reset in the years before death achieves less. It brings the declared basis closer to the likely auction price, reducing the final delta and simplifying provisional rate calculations, but it does not establish a market-verified price. The inheritance auction is still required and the heir receives an unverified self-declared basis rather than an auction-confirmed one. Soft resets are useful preparation but not a substitute for a hard reset where the death auction waiver is sought.

**Estate administration mandate gap.** (GOV.B §E) specifies the Custodian's mandate for the standard refund cycle, the closure bond facility for exit, and the corporate equity settlement facility. The operational mechanics of the bond facility applied to death closure — who initiates the provisional $\tau$ calculation with the Custodian, what documentation the estate executor must provide, how the provisional settlement transmits to the tax authority, and how the final bond netting occurs after the auction completes — are not currently specified for the death case. This is the same category of gap noted in (CLOSE §4.4) for the bankruptcy refund procedure. Both should be resolved in a future GOV.B revision before Phase One: the first death closure within a WDT system will otherwise face a procedural gap at exactly the moment when the mechanism most needs to demonstrate its orderly operation.

### 4.1.1 The Death Auction Waiver

A hard basis reset establishes a market-verified price through open competitive bidding. If a qualifying hard reset occurred sufficiently recently before death, the inheritance auction may be waived: the reset price serves as the Route D component of W_death without a further auction, the reset price is the heir's opening basis, and the estate proceeds to final settlement without waiting for an auction to complete.

The waiver rests on the following logic. A recent hard reset already produced the best available market price through the same competitive bidding mechanism the inheritance auction would use. Running the inheritance auction again a short time later produces marginal improvement in price accuracy at significant administrative cost and delay. The appreciation between the reset date and death is not lost to the Exchequer: it falls into the heir's future delta, taxed at the heir's own marginal rate when they eventually realise the asset. This is a deferral, not a tax gap, consistent with Route D's general design principle of deferring settlement to the point of realisation.

The **waiver threshold period** — the maximum time since a qualifying hard reset within which the waiver applies — is a Governing Council calibration parameter. A shorter threshold captures more post-reset appreciation in the deceased's estate (at the cost of the administrative burden the waiver is designed to avoid); a longer threshold provides greater estate planning certainty and stronger incentives for pre-death hard resets (at the cost of more deferral into the heir's position). The Governing Council sets this parameter under the Tier 1 process, informed by Phase One estate data and actuarial evidence on typical appreciation rates in the Route D asset population.

A qualifying hard reset is one conducted through the full voluntary hard-reset auction process specified in (GOV.B §G.7): open competitive bidding at the declared value as floor, third-party bids only, right of first refusal at the highest bid. A soft reset does not qualify regardless of recency. A corrective auction triggered by Valuation Body consensus qualifies if it established a final price through the same bidding mechanics, but the specific tax treatment of any corrective over-declaration at that auction (no refund on downward correction) carries forward — the reset price is the qualifying basis regardless of direction.

Where the waiver applies, W_death is established immediately from all determined route values plus the hard reset price as the Route D component, with no auction delay. The closure bond facility is not needed for the Route D component, though it may still be used if Route A or B valuations produce uncertainty about the provisional marginal rate.

## 4.2 Jurisdictional Exit

Jurisdictional exit (the taxpayer departing the jurisdiction and ceasing to be within the WDT's scope) is the closure event requiring the most structural addition: the bridging facility described in (CLOSE §5). The settlement logic is identical to death (the position closes, the final delta is calculated, the mechanism's obligations are honoured). The procedural challenge is that the taxpayer is alive and mobile, so the timing of closure cannot be fixed by an external event the way death fixes it.

For Routes A and B, exit triggers professional valuation at the declared exit date, following the competitive-tender model in (VAL §10). For Route C, exit triggers the must-transfer settlement: the equity interest transfers at the declared value and the delta is calculated in the standard way. Route D is the substantively novel case, since Route D was designed precisely for assets where periodic cash settlement is impractical. The inheritance-auction mechanism (VAL §11) applies directly: the exit valuation service opens on the declared exit date, the declared annual values serve as the opening bid floor, and the auction runs to establish the final price.

The same auction infrastructure (open bidding at the declared value as floor, only third parties may bid, the taxpayer holds a right of first refusal at the highest third-party bid, and the winning price becomes the new recognised basis) also operates in a third context: the (GOV §6.1) / (GOV.B §G) compelled mid-position revaluation, triggered when the three-body Valuation Body system confirms a Route D declaration as a significant outlier. That mechanism is not a closure event; the position continues after the auction. But it uses identical mechanics and the same Custodian administration, and its existence reinforces the exit auction's credibility: the infrastructure is a standing feature of the Route D architecture, not purpose-built for departure alone.

The bridging facility (CLOSE §5) addresses the timing problem Route D creates. Without it, a taxpayer with significant Route D holdings cannot depart until the auction completes (the detention problem conventional exit tax regimes produce).

The declared annual values do their most important work at exit closure. A taxpayer who has reported honest annual values throughout the holding period has a well-established floor that the auction process is likely to confirm with minimal deviation. A taxpayer who has systematically understated finds that the floor is low, not because the mechanism has set it punitively, but because they established it themselves across the annual reporting cycle. The mechanism takes them at their word.

## 4.3 Threshold Fall-Through

Threshold fall-through is a closure event, not a suspension. The position closes at the assessment at which fall-through is confirmed.

The final delta is the distance from the last declared basis to the exemption threshold W_min (a negative delta in all cases). The threshold is both the trigger for the closure event and the terminal value in the delta calculation, because the WDT's interest runs only to the threshold in either direction: gains below W_min are not taxed, and losses below W_min are not refunded. This is not special treatment for fall-through; it is the consistent application of the threshold's meaning. A taxpayer whose declared basis was £3m and whose net worth at fall-through is £1m, against a threshold of £2m, receives a refund on a £1m negative delta (the distance from £3m to £2m). The £1m of net worth below the threshold is outside the mechanism's scope entirely, as it would have been throughout the assessment period had wealth never exceeded W_min. The symmetric refund fires on the £1m delta at the applicable marginal rate. The position closes. The lifetime envelope is updated to reflect the refund received, carried by the individual for application to any future position they open.

Fall-through receives no special treatment under the symmetric refund logic: the same mechanism that refunds losses in any assessment year refunds the final negative delta at closure. This eliminates the position-suspension problem: no dormant position record to maintain, no ambiguity about the envelope's status during a period of sub-threshold wealth, no re-entry mechanics problem.

Re-entry above the threshold is treated as a new first entry. The individual declares their net worth at re-entry; that declaration is the new basis; a new position opens from there. The basis is fresh; the lifetime envelope is not. The individual carries their prior envelope balance into the new position. If wealth has grown between closure and re-entry, that appreciation is captured in the first delta of the new position. Threshold fall-through is not a basis-reset mechanism, and re-entry above threshold is not a grandfathered fresh start in the same sense that a first entry is.

A first-time entrant is grandfathered because the mechanism has no prior basis to anchor to. A re-entrant enters above a threshold they previously fell below; the mechanism has a declared basis on record from the prior closure. The new position's basis is fixed at re-entry net worth because that is the correct fresh-start basis for a new position, not because the mechanism has forgotten the prior history. The envelope carries that history forward.

## 4.4 Bankruptcy

Bankruptcy triggers the same terminal settlement machinery as the other closure event types. The position closes. Route D assets are auctioned. Routes A, B, and C settle through their standard mechanisms. The final delta is calculated. The mechanism's refund obligation is honoured if the final delta is negative.

Two features distinguish the bankruptcy case procedurally. First, the taxpayer no longer controls their assets: once insolvency proceedings open, an insolvency practitioner administers the estate. The position closure machinery runs under the practitioner's direction; the practitioner provides asset declarations, cooperates with the Route D auction process, and settles outstanding WDT obligations from estate proceeds. The taxpayer's own elections and voluntary revaluations are no longer available. Second, the priority order of claims places creditors ahead of the WDT's tax claim. The WDT follows jurisdiction-specific insolvency priority rules rather than asserting super-priority.

The rationale for creditor priority: an individual entering bankruptcy has characteristically experienced sustained losses. In many bankruptcy cases the lifetime envelope will have been substantially drawn down by prior-period refunds. The WDT's interest in the estate (tax owed on any positive delta remaining) is likely modest relative to creditor claims, and the mechanism's purpose is taxing gains, not competing with creditors for the residue of a failed estate. Asserting super-priority would be small in revenue terms and inconsistent with the cooperative architecture.

The refund obligation is not subject to creditor priority in the same way. If the final delta is negative (which is likely in a bankruptcy closure), the SWF owes the estate a refund as a guaranteed commitment regardless of the creditor pool's claims. The refund flows to the estate and is distributed through the insolvency process alongside other estate assets. The state's downside commitment extends, through the estate, to the creditors; the mechanism does not withdraw the symmetric protection because the individual is insolvent.

A gap in the current Custodian mandate specification should be noted. (GOV.B §E) specifies the Custodian's mandate for the standard refund cycle, the bridging facility, the solvency floor, and the corporate equity settlement facility. None of these provisions addresses the procedural mechanics of a refund obligation that has entered an insolvency estate: who initiates the refund calculation with the Custodian when the taxpayer is under insolvency administration, what documentation the insolvency practitioner must provide, and how the Custodian transmits the refund to the estate for distribution through the creditor waterfall. These are operational details the mandate will need to carry before Phase One, because the first bankruptcy closure within a WDT system will otherwise face a procedural gap at exactly the moment when the symmetric commitment most needs to be seen to operate. This gap should be resolved in a future GOV.B revision.

## 4.5 Incarceration and Criminal Forfeiture

Incarceration and criminal forfeiture present two distinct problems that share a common starting point and diverge at the point legal ownership transfers.

### 4.5.1 The Position During Incarceration

An incarcerated individual remains the beneficial owner of their assets throughout custody. Under (MF §2), beneficial ownership attaches to the person, not to their physical freedom or legal status. The WDT assessment position stays open; delta accrues normally. Incarceration does not trigger any of the standard closure events.

The practical difficulty is that an incarcerated taxpayer may be unable to execute the obligations their route classification requires. A Route C position requires transfer capability; Routes A and B require engagement with professional valuation. A legally frozen asset has lost these properties regardless of its normal type: frozen cash cannot be transferred in Route C settlement; an asset over which no party may transact cannot be professionally valued at a price reflecting free transferability. The correct treatment follows from the route classification logic in (VAL §4), which classifies assets by their current properties, not by a fixed typology. An asset that cannot be transferred, liquidated, or professionally valued without legal impediment fails the tests for Routes A, B, and C and falls to Route D by elimination: self-declared basis, no annual cash settlement, deferred to realisation.

Custodial route reclassification applies at the assessment date following the imposition of a legal freeze. All frozen assets are reclassified to Route D. The self-declared basis for each is its last declared or reset value at the point of reclassification, carried forward without adjustment until the freeze lifts or the position closes. No annual cash obligation arises during the reclassified period. When the freeze lifts — through charge dropping, acquittal, or completion of sentence without forfeiture — assets revert to their normal route classification and the assessment continues from the carried basis. The delta since reclassification is calculated at the next assessment date from the carried Route D basis to the then-current value under the reverted route's normal rules.

Who files the annual Route D self-declaration during incarceration follows from existing legal authority over the taxpayer's financial affairs. The WDT does not create a new representative institution for this purpose. Whoever holds legal authority to act on the taxpayer's behalf — a lasting power of attorney, a court of protection appointee, or a court-appointed financial administrator under jurisdiction-specific criminal procedure — files as the taxpayer's authorised representative on the same terms as any other authorised filer. Where no such authority exists at incarceration, the Administrator records the position as reclassified to Route D at the last declared basis and the position accrues without annual declaration until a representative is established. The absence of a representative does not pause delta accrual.

### 4.5.2 Criminal Forfeiture as a Closure Event

Where criminal forfeiture transfers legal ownership of assets out of the individual's name, those assets exit the individual's WDT assessment position. Where forfeiture encompasses the entire above-threshold position, it is a full position closure event.

The settlement sequence follows (CLOSE §3) without modification. The final delta for each forfeited asset is calculated from the last declared Route D basis — established at custodial reclassification — to the forfeiture value. Where forfeiture produces a negative delta (assets forfeited below declared basis, as is common where criminal activity inflated declared values or where assets declined during the restrained period), the symmetric refund fires at the applicable marginal rate bounded by the lifetime contribution envelope. The mechanism does not condition the refund on the nature of the loss. What bounds it is the envelope: a taxpayer who accumulated little WDT history on assets that were undeclared or under-declared will have a correspondingly small envelope balance and a correspondingly small refund entitlement. For legitimately declared assets that are forfeited, the envelope balance reflects taxes paid on prior gains and the refund is proportionate. The self-correction is structural rather than discretionary.

All WDT liabilities on any positive final delta are settled before the enforcement authority receives net proceeds, on the same priority terms as other closure types.

### 4.5.3 Post-Forfeiture Attribution

Once forfeiture is complete, the assets pass to the enforcement authority. The individual's position has closed. The assets have no human beneficial owner: prior ownership has been legally extinguished and no new ownership conferred on an identified person. Under the corporate levy framework in (CORP §5), assets with no identifiable beneficial owner are unattributed tranche-three positions bearing $\tau_h$.

Applying $\tau_h$ to enforcement-authority-held assets requires no exception. The enforcement authority is an identified holder; what it has not done is establish attribution to a human beneficial owner. $\tau_h$ accrues from the date of forfeiture in the same way it accrues on any other tranche-three position. This creates the same incentive that $\tau_h$ creates throughout the corporate levy structure: surface the human beneficial owner and the charge ends. The enforcement authority has a direct financial interest in swift attribution.

Attribution is achieved by any transfer that places the asset in the hands of an identifiable human or an intermediary that passes the attribution test. Three pathways are available without requiring any change to existing asset recovery law.

First, sale into the market. The enforcement authority's standard practice of selling forfeited assets into the open market transfers legal ownership to a new human buyer. Attribution is established at the point of sale; $\tau_h$ stops accruing; the new owner enters the corporate levy's normal tranche-one or tranche-two structure from the sale price as their opening basis.

Second, assignment to a charity or public redistribution scheme. A transfer to a registered charity with named trustees confers a tranche-two attributed position on the charity; its underlying beneficiaries are identifiable through the charity's governance. A direct cash distribution to named individuals creates immediate individual attribution.

Third, the forfeiture resolution award. Named enforcement personnel involved in the seizure receive a defined share of the asset's value at forfeiture on confirmed attribution to a human beneficial owner. The award is calculated on the forfeiture value, not on $\tau_h$ accrued during the unresolved period, so the financial incentive points entirely toward speed of resolution. The percentage and eligibility definition are Governing Council calibration parameters under the Tier 1 process. The award requires no new legal institution: it is a statutory payment from the enforcement authority's recovered proceeds, the terms of which are set in the WDT's enabling legislation.

The forfeiture resolution award aligns enforcement incentives with attribution incentives at the same moment. An officer who recovers assets and resolves attribution quickly receives more, net, than one who allows $\tau_h$ to erode them during a prolonged unresolved period. The effect on asset recovery timelines is a Phase One empirical question; the directional incentive is unambiguous.

### 4.5.4 The position of the individual after forfeiture

Where forfeiture closes only part of the position — some assets forfeited, others retained — the retained assets continue under normal assessment. Custodial route reclassification lifts for retained assets when the legal freeze lifts. The lifetime contribution envelope carries the forfeiture closure's settlement forward: taxes paid on forfeited assets and refunds received on their negative deltas update the envelope balance, which the individual carries into any continuing or future position.

Where forfeiture closes the entire position, the individual exits the WDT system. Re-entry above threshold follows (CLOSE §6) on the usual terms: fresh basis at re-entry net worth, lifetime envelope carried forward. An individual who re-enters following full forfeiture closure typically does so with a materially smaller envelope balance than a first-time entrant of equivalent wealth, reflecting the prior position's settlement history.

\newpage

# 5. The Closure Bond Facility

The closure bond facility decouples interim activity from final WDT settlement across all closure event types where Route D assets require auction and other assets or distributions need to proceed before that auction completes. It is a single instrument with three procedural variants — death, exit, and bankruptcy — sharing identical bond mechanics and differing only in who initiates the process and what interim activity is decoupled.

The facility is not needed where no Route D assets are held. Where all assets settle through Routes A, B, and C, valuations are triggered immediately at the closure event, marginal rate can be established quickly, and settlement completes without significant delay.

## 5.1 Bond Mechanics

The bond structure is identical across all three variants. Once a provisional W is established from all determined route values plus the Route D component at the last declared or reset basis, a provisional  $\tau(W)$  is calculated and non-Route-D settlement proceeds provisionally. Two bonds may then be posted:

Where the expected Route D contribution to W is above the provisional basis — meaning the auction is expected to come in above the last declared value and push W into a higher bracket — the initiating party (taxpayer, estate executor, or insolvency practitioner) posts a bond to the Custodian covering the estimated additional tax liability. This protects the Exchequer against underpayment if the auction produces a higher-than-expected price.

Where the expected Route D contribution is below the provisional basis — meaning the auction may come in below the last declared value, reducing W and lowering the applicable marginal rate — the SWF posts a bond to the initiating party covering the estimated overpayment. This protects the estate, creditor pool, or departing taxpayer against having overpaid against an excess they cannot then recover.

Where direction is uncertain, both parties post proportional bonds reflecting their respective exposure; the bonds net against each other on final settlement.

All bonds are sized to the estimated difference between provisional and expected final settlement, not to the full tax liability. Sizing ratios are Governing Council calibration parameters under the Tier 1 process, informed by Phase One closure data. (GOV.B §E.3) specifies the sizing principles; the values await implementation experience.

Final settlement occurs when the Route D auction completes and the true W is established. All provisional settlements are adjusted, bonds are released, and the net amount owed transfers in the appropriate direction. Where the death auction waiver applies (CLOSE §4.1.1), no Route D auction runs and bonds are not required for the Route D component; the waiver collapses the timing problem by making the provisional W immediately final.

## 5.2 Death Variant

**Initiating party:** Estate executor.

**Interim activity decoupled:** Provisional distribution to heirs while the Route D inheritance auction runs.

**Initiation:** After death, the executor establishes provisional W_death and initiates the bond process with the Custodian. Documentation requirements are assigned to a future GOV.B revision (see CLOSE §4.1 mandate gap).

**Symmetric character:** The SWF posting a bond to the estate on a negative expected delta ensures the estate has security for the expected refund. The state's downside commitment extends to the estate before final settlement is established.

**Hard reset waiver interaction:** Where the death auction waiver applies, the executor does not initiate the bond process for the Route D component — the reset price is treated as final immediately. The bond may still apply if Route A or B valuations produce rate uncertainty.

## 5.3 Exit Variant

**Initiating party:** Taxpayer.

**Interim activity decoupled:** Physical departure from the jurisdiction before Route D auction completes.

**Initiation:** The taxpayer declares an intended exit date through the Administrator's system. The Custodian calculates the expected delta direction and magnitude. Bonds are posted before departure; physical departure and settlement are then independent events.

**Cooperative character:** The SWF posting a bond to the departing taxpayer on a negative expected delta demonstrates that the state will honour the refund commitment even after the person has left the jurisdiction. This is the trust-building dimension of the exit variant that the death and bankruptcy variants do not carry in the same way: the departing taxpayer is making a judgment about whether to remain in the system, and the SWF's posted bond is evidence that the mechanism will meet its obligations.

**Friction concentration:** A taxpayer who initiates the exit valuation service early, provides complete documentation, and cooperates with the pre-departure process faces minimal uncertainty at departure. A taxpayer who initiates late or with incomplete documentation faces a longer open-liability period. Friction concentrates on non-cooperation, not on the act of departure.

## 5.4 Bankruptcy Variant

**Initiating party:** Insolvency practitioner.

**Interim activity decoupled:** Provisional creditor distributions while Route D assets are auctioned.

**Initiation:** Once insolvency proceedings open, the practitioner initiates the bond process with the Custodian, provides asset declarations, and cooperates with the Route D auction process. Documentation requirements are assigned to the same GOV.B revision noted in (CLOSE §4.4).

**Priority ordering:** The bond posted by the insolvency estate is a claim by the WDT mechanism on that estate, ranked according to jurisdiction-specific insolvency priority rules as specified in (CLOSE §4.4) — creditors first, WDT claim subordinate. The bond does not assert super-priority. In bankruptcy, the more likely scenario is that the final delta is negative (assets have declined), the SWF owes a refund, and the estate bond is not needed; the SWF's bond to the estate is what matters for creditor recovery.

**Hard reset waiver:** The death auction waiver does not apply to bankruptcy. A hard reset performed before insolvency is useful — it reduces the Route D delta and simplifies the practitioner's auction process — but the waiver is specific to death closure because the deferral logic (heir pays later) has no equivalent in bankruptcy, where the creditor pool receives the estate as a one-time settlement and there is no continuing position into which deferred tax could fall.

\newpage

# 6. The Re-entry Rule

A re-entrant is an individual who has previously experienced a WDT position closure and subsequently re-enters the WDT's scope. The re-entry rule has two components that work differently and must be stated separately.

The basis on re-entry is the individual's net worth at the point of re-entry, declared in the standard way. This applies regardless of which closure event type preceded the re-entry: a taxpayer returning after exit closure, a taxpayer whose wealth has risen back above the threshold after fall-through closure, and a taxpayer who re-enters the jurisdiction after bankruptcy closure all declare their current net worth as their opening basis. The new position starts from where they are, not from where they were before closure.

The lifetime envelope on re-entry is the individual's accumulated prior balance, carried forward from all previous positions. A re-entrant whose prior position closed with a partial envelope balance carries that balance into the new position; the new position may generate further contributions or refunds, subject to the envelope ceiling, from the point of re-entry onward.

The interaction between these two components closes a potential loophole that either component alone would leave open. Consider a taxpayer who exits, holds assets through an appreciation period outside the jurisdiction, and returns. Their re-entry basis is their current net worth, which reflects appreciation that occurred outside the system. Their first delta is therefore zero: a new position starting at current values has no first-period delta unless net worth changes during the first assessment period. The appreciation that occurred during the absence is not directly taxed.

But the envelope carries forward. A taxpayer cycling strategically (exiting before an expected loss period, claiming a refund on exit closure, returning with a fresh basis after the loss has passed) finds that the refund claimed at exit closure has reduced the envelope balance available for the new position. The envelope is not a mechanism for unlimited loss recovery through cycling. Each closure and re-entry settles the running account, and the settled account follows the individual into every subsequent position.

The carry-through also operates in the other direction. A re-entrant who has been a net contributor across prior positions carries a larger envelope balance into the new position, and therefore has more refund headroom in loss years than a first-time entrant of equivalent wealth. Making re-entry attractive to long-term participants is a design objective.

The re-entry rule treats re-entrants differently from first-time entrants. A first-time entrant is grandfathered because the mechanism has no prior basis for them and no claim on their pre-WDT wealth (a consequence of the mechanism's inability to retroactively assess wealth accumulated before the system existed). A re-entrant is in a different position: the mechanism has a complete record of their prior position (declared values, delta history, lifetime envelope balance), and uses that record to carry forward what belongs to the individual (the envelope) while starting the new position from current values (the basis).

\newpage

# 7. Phase Sequencing

## 7.1 Phase One

Phase One applies the full position closure framework to the small identified population that Phase One's high threshold and limited reach actually affect. Death closures will be rare but will exercise the inheritance auction machinery from (VAL §6.5). Exit closures will test the bridging facility and the exit valuation service. Threshold fall-through closures are likely the most common, particularly in years where market conditions produce negative deltas across the top of the wealth distribution; these are also the cleanest test of the symmetric refund at closure because the negative-delta-to-threshold calculation is straightforward.

Bankruptcy closures at Phase One are likely to be uncommon and, as argued in (CLOSE §4.4), likely to produce minimal WDT tax claims. Their principal value in Phase One is testing the interaction between position closure mechanics and insolvency procedures in the reference jurisdiction, a prerequisite for the jurisdiction-specific legal work assigned to JUR.

Phase One will generate the first systematic evidence on closure behaviour: how many taxpayers exit, at what wealth levels, whether exit rates are sensitive to the cooperative features of the mechanism. RATES's revenue estimates are explicitly pre-behavioural (RATES §9.1), and exit behaviour is among the principal sources of overstatement in those figures. Phase One evidence will begin to correct this, though the correction is a Phase One paper item. The design framework within which Phase One generates that evidence is in (BEHAV §4) and (BEHAV §7) and (CLOSE §10).

## 7.2 Phase Two

Phase Two introduces additional complexity in two respects. First, the lower Phase Two threshold means a larger population, with threshold fall-through closures becoming more frequent as a proportion of the total (lower-wealth taxpayers experience more volatility relative to threshold). The symmetric refund at fall-through closure becomes a more significant aggregate fiscal commitment as the threshold drops; this interaction between threshold level and fall-through refund volume should be modelled as part of the Phase Two design process, and is flagged as CLOSE OQ 2.

Second, the re-entry rule's Phase Two extension to foreign nationals with prior WDT-equivalent positions requires bilateral information exchange arrangements. A foreign national immigrating for the first time retains full first-entry grandfathering regardless of Phase. A foreign national who previously held a WDT-equivalent position in another jurisdiction is a re-entrant for envelope purposes (their prior contributions elsewhere carry forward to the extent the bilateral arrangement can establish them). The specific design of these arrangements cannot be done unilaterally and is flagged as CLOSE OQ 3.

\newpage

# 8. Principal Objections

## 8.1 The Compulsion Objection

The most intuitive objection to exit closure, and to position closure in general, is that it amounts to compelled membership: a taxpayer should be free to leave, fail, or fall below the threshold without the state extracting a settlement as the price of doing so. The WDT's response operates at two levels.

The first is conceptual. Position closure settlement is not a charge for the act of closing; it is the settlement of an accrued running account. A taxpayer who has held a WDT position for twenty years has twenty years of delta calculations, offset by refund entitlements in loss periods. The closure event settles the running account, as the termination of any ongoing credit or debit relationship settles the account. The accrued amount does not disappear because the individual is leaving, failing, or falling below threshold.

The second is structural, and applies specifically to exit closure. The bridging facility means that physical departure is not conditional on settlement being complete. The compulsion objection in its most serious form (that the taxpayer is detained pending settlement) does not arise. What remains is that the individual has an accrued liability that will be collected after they depart, which is a different claim.

## 8.2 The Double Taxation Objection

A taxpayer exiting to a jurisdiction that also operates a wealth or capital gains tax may face assessment in both jurisdictions on appreciation that occurred while they were a WDT participant. The WDT's exit closure establishes a definitive, auditable final basis: the exit settlement value is a clean record of the mechanism's last assessment. If the receiving jurisdiction treats that as the new entry basis, no double taxation arises. If it does not, a coordination gap exists that the WDT cannot resolve unilaterally.

What the WDT can offer is the documentation: the exit settlement value, the declared value trail, the delta record. Whether a receiving jurisdiction uses that documentation to avoid double-counting is a bilateral coordination question assigned to CLOSE OQ 3.

## 8.3 The Re-entry Asymmetry Objection

The re-entry rule treats re-entrants differently from first-time entrants: the re-entrant's envelope carries forward while a first-time entrant starts with a clean envelope. The objection is that this creates an asymmetry that disadvantages returning taxpayers relative to immigrants of equivalent wealth.

The asymmetry is real and is a named feature, not an oversight. A first-time entrant starts with a clean envelope because the mechanism has never assessed them and has no claim on their pre-WDT history. A re-entrant carries their prior envelope balance because the mechanism has assessed them, settled the running account at closure, and has a complete record. The envelope that follows them into the new position reflects contributions they actually made and refunds they actually received. It is a record, not a penalty.

The practical consequence is that a re-entrant who has exhausted their envelope through prior refunds enters the new position with less refund headroom than a first-time entrant of identical wealth. This is correct: they have already received refunds up to their prior contribution level. Treating them identically would allow a re-entrant to claim refunds on losses that duplicate refunds already received on prior closures.

## 8.4 The Beyond-Lifetime-Cap Objection

An objection sometimes raised against the lifetime contribution envelope is that it is overly restrictive: a taxpayer who has paid little tax to date — because they are new to the system, because prior years were predominantly gain years with small assessed amounts, or because the mechanism was recently introduced — may face a large refund entitlement in a bad loss year that the envelope cap prevents them from receiving in full. The objection asks why the refund should be bounded by prior contributions rather than by the loss itself.

The answer is that the cap closes a specific exploitation surface that would otherwise exist. If refunds could exceed the cumulative lifetime contribution — that is, if the state could pay out more in refunds than it had collected from a given taxpayer — the following attack becomes viable: a taxpayer accumulates a modest tax history, engineers a large paper loss through inflated basis, related-party transactions, or other valuation manipulation, receives a refund that exceeds their cumulative contribution (a net transfer from state to taxpayer), and then exits under the position closure framework with the position legally settled and no recourse available to the mechanism. The net result is that the taxpayer has extracted money from the SWF using a manufactured loss, departed, and left the state holding no claim.

The lifetime cap makes this impossible by construction. A refund can never exceed cumulative taxes paid by that taxpayer. The mechanism can only return what it has received. A taxpayer who has paid nothing into the system has no refund entitlement regardless of how large a loss their position records.

This is not a restriction on the symmetric refund commitment. The commitment is honoured in full for every taxpayer within the envelope. What the cap does is remove the incentive to manufacture losses beyond that amount. A taxpayer whose genuine loss is smaller than their cumulative contribution receives the full symmetric refund. A taxpayer whose genuine loss exceeds their cumulative contribution receives refunds up to the cap, which represents the full amount the mechanism has collected from them — the state is returning everything it has taken, which is a complete settlement of its downside commitment given the history of the position.

The Governing Council may in future consider extending refund availability beyond the lifetime cap — for example, to attract entrants with short tax histories, to provide relief in exceptional circumstances, or to offer an entry-year credit to new taxpayers who experience early losses. Any such extension is a named trade-off under the (MF §9) framework: the benefit (more generous refund commitment, lower barrier to entry) must be weighed against the fact that it reopens the exploitation surface described above, and the enforcement mechanism required to close that surface must be specified before the extension is offered. The cap in its current form reflects the cooperative architecture's preference for incentive alignment over enforcement: it removes the motivation to manufacture losses rather than requiring the mechanism to detect and challenge them after the fact.

# 9. Limitations and Required Further Work

## 9.1 Formal modelling gaps

No items in this paper.

## 9.2 Phase One empirical unknowns

How many taxpayers will exit following WDT assessment, how threshold fall-through rates vary across market conditions, and whether closure mechanics affect taxpayer behaviour in unanticipated ways are all Phase One empirical questions. RATES's revenue estimates assume no behavioural exit response; this paper establishes the closure mechanics but does not correct that assumption.

The cross-base fiscal externality [@AgrawalEtAl2025] applies specifically during Phase One and is not addressed by the position closure framework. The CLOSE framework settles the WDT's internal account correctly at exit; it does not recover the income tax and VAT base that leaves with the individual. In Phase Two, where those parallel taxes are displaced, the externality disappears structurally.

At Phase Two's lower threshold, threshold fall-through closures and the symmetric refunds they generate become more frequent. The aggregate fiscal commitment at Phase Two scale should be modelled as part of Phase Two transition design. This is assigned to a Phase Two design paper or RATES revision.

## 9.3 Jurisdiction-specific legal and implementation work

The constitutional and legal analysis of exit closure and bankruptcy closure in the reference jurisdiction is absent from this paper. The interaction of the WDT's position closure framework with domestic insolvency priority rules, deemed-disposal provisions, and freedom-of-movement considerations are jurisdiction-specific questions assigned to JUR and to the dedicated legal paper.

The Route D closure mechanics (exit valuation service, inheritance auction in its exit application, conduct rules, no-bid fallback procedures, timelines, and treatment of internationally-sited assets at closure) are complete at the design level but leave implementation questions open requiring legal specification before Phase One.

The re-entry rule's extension to foreign nationals with prior WDT-equivalent positions in other jurisdictions depends on bilateral information exchange arrangements that cannot be designed unilaterally. This is assigned to a future international coordination paper (#16 in the consolidated register).

The interaction of custodial route reclassification and criminal forfeiture closure with existing asset-freezing and proceeds-of-crime legislation requires jurisdiction-specific legal analysis. The WDT's route classification logic follows from the assets' properties at the relevant date; whether domestic courts will accept reclassification from Route C to Route D on this basis, and how the forfeiture settlement sequence interacts with creditor priority rules under criminal confiscation orders, are questions for the dedicated legal paper and JUR.

## 9.4 Structural and irreducible limits of the design

The paper does not quantify the revenue or behavioural consequences of any closure event type. How those quantities turn out depends on conditions the mechanism cannot determine in advance. The design framework within which Phase One generates evidence on these questions is in BEHAV. CLOSE establishes the closure mechanics and their principled basis; predicting the consequences is outside its scope.

## 9.5 Governing Council calibration parameters

Bond sizing ratios for the closure bond facility — the proportionality of bonds posted by the taxpayer, executor, or practitioner (positive expected delta) and by the SWF (negative expected delta) relative to estimated liability — are Governing Council calibration parameters under the Tier 1 process, informed by Phase One closure data across all three variants. (GOV.B §E.3) specifies the principles; the values await implementation experience.

The death auction waiver threshold period — the maximum time since a qualifying hard basis reset within which the inheritance auction may be waived at death — is a Governing Council calibration parameter. The relevant trade-off (administrative simplification against deferral of post-reset appreciation into the heir's position) and the qualifying conditions for a hard reset are specified in (CLOSE §4.1.1). The value awaits Phase One estate data and actuarial evidence on typical Route D appreciation rates.

The forfeiture resolution award — the share of forfeiture value payable to named enforcement personnel on confirmed attribution — is a Governing Council calibration parameter under the Tier 1 process. The relevant trade-off is between an award size sufficient to materially accelerate attribution and one that does not crowd out other enforcement incentives or create distortions in investigative prioritisation toward high-value WDT targets. Phase One data on forfeiture timelines and attribution rates will inform the calibration. The value awaits implementation experience.

\newpage

# 10. Conclusion

Death, jurisdictional exit, threshold fall-through, and bankruptcy are structurally the same kind of event: the WDT assessment position closes. The mechanism's response to each is the same in structure — calculate the final delta, honour the symmetric refund if it is negative, settle the running account — with procedural differences that follow from the specific circumstances of each closure type.

Death most fully exercises the machinery. The marginal rate dependency problem — $\tau_{W_death}$ cannot be established until all route valuations are complete, meaning Route D's inheritance auction blocks final settlement of everything else — is managed through the provisional $\tau$ mechanism and the closure bond facility. The death auction waiver, where a qualifying hard reset occurred within the Governing Council's threshold period, collapses this timing problem by treating the reset price as the final Route D component of W_death without a further auction, deferring the post-reset appreciation into the heir's future delta.

The closure bond facility unifies what would otherwise be three separate instruments. Death, exit, and bankruptcy all face the same underlying problem: Route D assets require an auction that takes time, while other assets or distributions need to proceed. The bond structure — provisional settlement, bonds posted by both sides proportional to expected delta direction, netting on final settlement — is identical across all three variants. What differs is who initiates, what is being decoupled, and the specific procedural context. Exit carries an additional cooperative dimension: the SWF posting a bond to a departing taxpayer demonstrates that the mechanism will honour its refund commitment across jurisdictional boundaries.

The lifetime contribution envelope persists across all closure types and re-entries because it is a property of the individual, not of the assessment position. Re-entrants carry their prior envelope balance into any new position. The basis of the new position is fresh; the envelope history is not. This is the closure framework's principal safeguard against strategic cycling through the mechanism.

The paper's contribution is the abstraction itself: position closure as a general theory, with the closure bond facility as its operational expression, rather than exit taxation and inheritance treatment as separate specialised regimes with their own logic and their own failure modes.

\newpage