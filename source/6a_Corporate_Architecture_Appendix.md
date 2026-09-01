---
title: "The Wealth Delta Tax: Corporate Architecture Appendix"
shortcode: "CORP.A"
status: "active"
keywords:
    - Wealth Delta Tax
    - wealth taxation
    - corporate tax administration
    - shareholder reporting
    - beneficial ownership
    - corporate compliance
    - tax automation
    - administrative burden
    - listed-company taxation
    - foreign attribution
    - transitional taxation
    - corporate tax transition
    - tax intermediaries
---

### Revision History {.unnumbered .unlisted}

| Revision | Date            | Details                  |
|:--------:|:---------------:|--------------------------|
| 0.01      | 03 July 2026     | First Draft          |
| 1.00      | 15 August 2026  | Published to website |
| 1.01      | 20 August 2026  | Update Section E for clarity |

\newpage

# A. Collection Mechanics and Worked Illustrations {.appendix}

## A.1 The Two-Deadline Structure

The mechanism runs two separate deadlines from the same assessment date. The annual reporting cycle runs every year: the corporation measures the corporate delta, pays the provisional levy into the settlement account, and issues delta statements to all registered shareholders within sixty days. Native shareholders include their allocation in their annual WDT report. The credit-claiming deadline runs one year from the assessment date: the native shareholder settles individual WDT for that year and registers their credit claim; the tax authority confirms settlement; the credit is released against the shareholder's WDT liability for that assessment year; and the provisioned amount exits the settlement account. At the one-year close, unclaimed credits lapse and the provisioned amounts are refunded to the corporation; known non-attributable holders are assessed at $\tau_0$ (final); unidentified beneficial owners are assessed at $\tau_h$ (final); and the corporation pays any top-up shortfall or receives any overprovision refund.

The rolling settlement cycle is separate: when a taxpayer's rolling average window closes, the taxpayer settles their total accumulated WDT across all assessment years in that window at their progressive marginal rate. Corporate credits already claimed annually are applied at that point; credits that lapsed do not reduce this liability.

The key distinction is that claiming each year's corporate credit and settling total individual WDT are separate events on separate deadlines. A shareholder with a five-year rolling window must register and claim each year's credit within one year of that year's assessment date. The rolling window governs when total WDT is paid, not when credits are claimed.

Credits are released against the shareholder's WDT liability for that assessment year, not paid back to the corporation directly. The settlement account is the vehicle through which the provisional levy is held and distributed. What the corporation recovers at the one-year close is the release of its provisional obligation on the native-shareholder tranche through claimed credits, plus a refund of any excess where credits lapse or are waived.

## A.2 Shareholders Who Sell Before the Assessment Date

When a native shareholder sells before the assessment date, the gain enters their individual WDT delta through the transaction. They do not appear on the register at assessment date and receive no delta statement for that year. The corporation still pays its provisional levy on the full corporate delta, including the tranche attributable to the departed seller.

The seller settles their individual WDT for the year that includes the sale and registers their credit claim within the standard reconciliation window from that year's assessment date, the same deadline that applies to all native shareholders. The tax authority attributes the corporate component of their gain to the relevant company and releases the corresponding credit at that point.

The buyer pays a price reflecting post-appreciation value. Their delta statements cover appreciation since purchase, and their credit claim covers their holding period only.

## A.3 Partial-Year Attribution

A buyer who purchases shares after a sale and holds through the assessment date receives a delta statement based on their proportional share of the company's full-year delta, not just appreciation during their ownership period, overstating their actual gain for that year.

The overpayment is bounded by trade size and the length of the mismatched period. Correcting it would require transaction-level tracking of every registered position against specific holding dates. This is an accepted approximation: the administrative cost of full transaction tracking is disproportionate to the revenue at stake in most cases.

## A.4 Sequencing

The one-year credit-claiming deadline resolves most sequencing ambiguity: all corporate credits for a given assessment year are claimed, lapsed, or waived within twelve months of the assessment date, regardless of where individual shareholders sit in their rolling windows.

One narrow question remains. Where a shareholder's annual WDT settlement and credit claim for a given year both fall in the same filing cycle as the corporate assessment date, a true-up in the following year may be required rather than same-cycle reconciliation. The mechanics of that true-up are a filing infrastructure question, not specified here.

## A.5 Loss Years and Private Arrangements

In a loss year the corporation pays no levy. Native shareholders whose net worth delta is negative receive individual WDT refunds through personal assessment. Corporations may make private arrangements with shareholders about contributions and credits across good and bad years. These arrangements do not affect tax liability, refund entitlement, or the corporate levy calculation.

## A.6 Worked Illustration: Standard Shareholders

This illustration traces three shareholders through a single assessment cycle.

Shareholder A holds throughout the year, is on the register at the assessment date, and receives a delta statement. Within the reconciliation window, A settles individual WDT for that year at their marginal rate on their total net worth delta including the corporate allocation. The tax authority confirms settlement and releases the credit against A's liability. The provisioned amount attributable to A's tranche exits the settlement account. A's rolling window may extend further; when it closes, A settles their accumulated total WDT for the full window, but the corporate credit for this assessment year has already been applied.

Shareholder B sells in month four, before the assessment date. The gain enters B's individual WDT delta. B does not appear on the register at the assessment date. The corporation pays provisional levy on the full delta including B's tranche. B settles their individual WDT for this year and registers their credit claim within the standard reconciliation window. The tax authority matches B's corporate gain component to the company and releases the credit against B's liability. Shareholder C, who bought B's shares, is on the register at the assessment date, receives a delta statement for the full remaining year, and claims their credit within their own reconciliation window. The partial-year gap for C, described in (CORP.A §A.3), is visible here: C's delta statement covers the company's full-year appreciation, not just the period from when C held the shares.

Shareholder D holds throughout the year, receives a delta statement, but voluntarily elects not to claim the credit within the reconciliation window. D's WDT liability is unaffected; D pays their full individual assessment without the offset. At the one-year close, the provisioned amount attributable to D's tranche is refunded to the corporation as an overprovision release.

## A.7 Corporate Entities as Shareholders

A holding company that owns shares in a listed subsidiary reconciles against the subsidiary's levy proportional to its own registered stake. An individual shareholder further up the chain reconciles against the holding company's net position. Each entity in the chain needs only its own immediate stake and the figure from one level below.

The chain works only where every entity in it is eligible for reconciliation: a native individual, a domestic listed company, or a domestic private company reached through individual assessment. A foreign entity anywhere in the chain breaks eligibility at that point. Where the chain breaks at a foreign entity, $\tau_f$ applies to the unattributed portion of that entity's holding. Any portion the foreign entity can attribute to named beneficial owners passes through at $\tau_0$; the remainder bears $\tau_f$. Where no diplomatic agreement exists between the WDT jurisdiction and the foreign entity's home jurisdiction, $\tau_f$ defaults to $\tau_h$. Domestic shareholders above the break point reconcile against the holding company's net position after that settlement has been applied.

## A.8 No Minimum Threshold

Credits have no minimum. There is no separate claims process a shareholder must initiate. A shareholder's proportional share, however small, is calculated from registry data and recorded against their individual WDT settlement in the normal way.

## A.9 Intermediary Chain Illustrations

### A.9.1 Broker/Nominee Case

Setup. Company X has a corporate delta of £100m in the assessment year. The share register shows 60% held by direct shareholders (native WDT taxpayers and institutional holders) and 40% held by Nominee Broker Ltd. Company X provisions at $\tau_{prov}$ = 2% against the full £100m delta, paying £2m into its settlement account. Broker Ltd's registered tranche represents £40m of the delta; the corporation has provisioned £0.8m against it at $\tau_0$ = 2%.

Broker Ltd's client book. Broker Ltd's book for Company X shares breaks down as follows: 85% of its registered tranche (£34m of delta) is held by retail clients confirmed as below-threshold through WDT voluntary registration; 10% (£4m) is held by above-threshold native WDT shareholders; and 5% (£2m) is unattributable, positions held through sub-nominee structures Broker Ltd cannot look through.

Company-level settlement. At the one-year close, Company X's settlement account closes for Broker Ltd's tranche. Company X has paid $\tau_0$ = 2% on £40m = £0.8m against Broker Ltd's registered position. That £0.8m is Broker Ltd's provisional charge at the company level. Company X's obligation is discharged, but the amount is recoverable by Broker Ltd through its own reconciliation with the tax authority.

Broker-level reconciliation. Broker Ltd submits its reconciliation return within the reconciliation window. Against the 85% below-threshold registered proportion (£34m delta): Broker Ltd claims back the $\tau_0$ paid on those clients' shares, 2% × £34m = £0.68m. Those clients owe no WDT and the levy on their shares is not final. Against the 10% native WDT shareholder proportion (£4m delta): those shareholders settle their individual WDT with the tax authority, which matches their corporate allocation to Company X and releases the corresponding credit. Broker Ltd's $\tau_0$ payment on that proportion (2% × £4m = £0.08m) is recovered through the credit-release process. Against the 5% unattributable proportion (£2m delta): $\tau_h$ applies as a final charge at the broker level. If $\tau_h$ = 10%, Broker Ltd pays 10% × £2m = £0.2m as a final settlement on that tranche. Broker Ltd provisioned only at $\tau_0$ = 2% against this tranche at the company level (£0.04m), so it pays a shortfall of £0.16m from its own resources.

Net position. Company X paid £0.8m. Of this, £0.68m + £0.08m = £0.76m is recovered by Broker Ltd through claim-back and credit releases. The £0.04m provisioned against the unattributable tranche stays with the tax authority as part of the final $\tau_h$ settlement. Broker Ltd contributes an additional £0.16m top-up. Total collected on Broker Ltd's tranche: £0.2m (= $\tau_h$ × £2m unattributable).

The incentive structure. Every retail client Broker Ltd can confirm as below-threshold registered reduces its net levy cost by the difference between $\tau_0$ provisioned and the claim-back. The 5% unattributable position costs Broker Ltd $\tau_h$ on its full value, a substantially higher rate, because those positions were not structured for attribution. Shareholders using opaque sub-nominee structures to avoid attribution have caused their broker a real financial cost, which the broker is likely to pass through in pricing or decline to facilitate.

### A.9.2 Pooled Fund Case

The same logic applies where the intermediary is an ETF or mutual fund, with one structural difference: a fund does not hold individually identified client accounts in the way a broker does. It allocates proportionally by unit holding.

Suppose Fund Y holds a further 10% of Company X's shares (£10m of the delta). Fund Y maintains a unit register sufficient to identify each unit holder's proportional interest and, through ordinary investor onboarding, their WDT status. Fund Y's £10m tranche is provisioned at $\tau_0$ = 2% (£0.2m) at the company level.

Within the reconciliation window, Fund Y allocates the £10m delta proportionally across its unit holders by holding size, rather than by named client account, since units rather than specific shares are what each investor holds, and submits a reconciliation return on the same basis as Broker Ltd's: below-threshold unit holders generate a claim-back, above-threshold native shareholders settle individually and trigger ordinary credit release, and any units held through structures Fund Y cannot look through remain unattributable and bear $\tau_h$ at the fund level.

The mechanism is identical in structure to the broker case. Only the allocation method differs: proportional by unit rather than direct by named holding.

\newpage

# B. Corporate Rate Calibration {.appendix}

$\tau_0$ and $\tau_h$ are calibrated against structurally distinct failure modes of the corporate instrument. $\tau_0$ addresses the case where attribution succeeds but settlement does not: the identified person who fails to reconcile within the window. $\tau_h$ addresses the case where attribution itself fails: the position that cannot be resolved to an identified individual at any level of the chain. Because the failure modes are different, the calibration logic is different in kind, and the two parameters cannot be derived from a single optimisation.

## B.1 The Floor Rate ($\tau_0$): Collection Security

$\tau_{prov}$ is an administrative withholding parameter, not a tax rate in the sense the WDT uses that term. The corporation is acting as a collection agent for individual WDT liabilities that will be assessed elsewhere. A consequence follows: changing $\tau_{prov}$ never changes the eventual WDT liability of any shareholder who reconciles successfully. A corporation provisioning at 15% and one provisioning at 50% produce identical final shareholder liabilities. The only difference is the timing of payment and the size of the reconciliation flows needed to correct the gap. $\tau_{prov}$ is therefore a cash-flow and administration parameter. The optimisation objective is to minimise the total expected cost of collection, balancing corporate financing costs, administrative reconciliation costs, shareholder cash-flow distortion, and collection-risk exposure, rather than to set a revenue rate.

The $\tau_0$ floor is grounded in collection security against reconciliation failure. Where a shareholder dies, emigrates, becomes insolvent, fails to file, or is otherwise unreachable within the reconciliation window, the provisional amount already held by the state is the only revenue available. $\tau_0$ is therefore the minimum secured collection requirement the state requires as a condition of the corporate instrument operating at all.

The calibration problem is an expected-value one. The state's expected revenue loss per assessment cycle from non-reconciliation across the native-shareholder tranche is approximately $p × (\tau_{actual} − \tau_0) × W_{tranche-1}$, where p is the non-reconciliation rate, $\tau_{actual}$ is the marginal WDT rate that successful reconciliation would have produced, and $W_{tranche-1}$ is the delta allocated to tranche one. Setting $\tau_0$ so that this expected loss is acceptably bounded is the calibration objective.

Two structural properties of the failure population bear on this bound. First, the failure population clusters at lower wealth levels within the taxable tranche. Large WDT taxpayers have strong financial incentive to reconcile: the credit they are claiming offsets a large individual liability, and the opportunity cost of letting it lapse is high. The non-reconciling population therefore skews toward holders with more modest holdings, whose per-failure shortfall is correspondingly lower. Second, the position closure framework in (CLOSE) substantially reduces the emigration component of non-reconciliation: the bridging facility requires departing taxpayers to post a bond or receive one before leaving, so departure does not generate an unrecovered liability in the way a conventional exit does. The residual failure population after these structural filters consists primarily of death events not yet processed through the estate, insolvency proceedings, and administrative inaction by smaller holders.

The consequence is that $\tau_0$ anchored at or near the individual WDT entry-level effective rate is likely to provide adequate collection security. The failure population's average effective rate approaches $\tau_0$ (they are near-threshold holders), so the per-failure shortfall is small; the non-reconciliation rate, bounded by the structural filters above, is expected to be low; and the product of the two is therefore modest relative to the $\tau_0$ level that collection-security reasoning independently motivates.

### B.1.1 Phase One data requirement 

The Governing Council should review $\tau_0$ against the following observables, available within the first one to two assessment cycles: the non-reconciliation rate across the native-shareholder tranche, broken down by wealth band; the distribution of non-reconciliation by reason (death, emigration, insolvency, administrative inaction); and the average revenue shortfall per non-reconciliation event by wealth band. A standing rule linking $\tau_0$ to these observables (for example, maintaining $\tau_0$ at a level that covers the expected shortfall at the 95th percentile of the non-reconciliation rate distribution) would convert an initial calibration judgment into a data-driven parameter updated at each LRR milestone. Exact initial calibration remains a Governing Council parameter under the Tier 1 process (GOV §6).

## B.2 The Final Charge on Permanently Unattributable Ownership ($\tau_h$): Deterrence and Revenue Recovery

$\tau_h$ is not an administrative parameter of the same kind as $\tau_{prov}$. Where $\tau_{prov}$ is a withholding estimate corrected through downstream reconciliation, $\tau_h$ is a final liability with no downstream reconciliation path. The calibration problem is correspondingly different: the Governing Council must set a rate that makes permanent opacity economically irrational and approximates the WDT revenue that opacity forecloses, within a ceiling set by the revenue-recovery rationale itself.

### B.2.1 The deterrence condition 

For opacity to be irrational, the expected cost of $\tau_h$ must exceed the expected cost of individual WDT assessment across the relevant holding period. Under individual assessment at the top bracket, the effective rate on gains approaches $\tau_m$. For a position held at high growth rates, $\tau_h$ applied to the full delta without rolling-average smoothing or progressive relief must therefore approach $\tau_m$ to close the deterrence gap. A rate substantially below $\tau_m$ can create a structurally cheaper route through opacity for high-growth concentrated positions, undermining the attribution incentive the tranche architecture depends on.

### B.2.2 The refund-forfeiture effect 

Permanently unattributed ownership forfeits access to the symmetric loss-refund mechanism. This is an economically significant additional cost of opacity, independent of the $\tau_h$ rate itself. Attributed shareholders receive proportional refunds in loss years; permanently unattributed positions receive nothing. The expected value of forfeited refund entitlement is a function of asset return volatility and holding period: for high-volatility positions at the top bracket, forfeited refunds over a multi-decade holding period can be worth multiple percentage points of average annual return. This effect partially substitutes for rate-based deterrence: the deterrence condition can be satisfied at a $\tau_h$ somewhat below $\tau_m$ once forfeited refund rights are included in the comparison. The precise magnitude is a (RATES) and (VAL.A) modelling question; the directional claim is structurally robust.

### B.2.3 The revenue-recovery ceiling 

The corporate instrument exists to collect what the individual mechanism cannot reach. A $\tau_h$ that substantially exceeds what the individual mechanism would have collected from the same holders is a punitive surcharge rather than a collection mechanism. The individual mechanism's asymptotic maximum rate is $\tau_m$, making $\tau_m$ the natural ceiling on $\tau_h$: above it, the corporate instrument is collecting more from the opaque position than it would have collected from a fully attributed one, which is indefensible on revenue-recovery grounds regardless of deterrence.

### B.2.4 The legal proportionality constraint, and why it is weaker than it appears 

$\tau_h$ applies without progressive assessment, individual valuation, rolling-average smoothing, or a formal right of appeal against the quantum of the liability. This might suggest that applying a high flat rate exposes $\tau_h$ to constitutional challenge on proportionality grounds. The constraint is substantially weaker than it appears, for a structural reason: any beneficial owner who mounts a legal challenge to $\tau_h$ must first establish standing by identifying themselves as the affected party. Establishing standing is itself an attribution event. The moment a claimant demonstrates that they are the beneficial owner of a position bearing $\tau_h$, they have satisfied the attribution test, and the position reclassifies automatically to the appropriate tranche: either tranche one (native shareholder) or tranche two (identified intermediary). $\tau_h$ ceases to apply from that point forward.

This creates a self-defeating structure for litigation. The legal remedy available to a beneficial owner dissatisfied with $\tau_h$ is to identify themselves, which is also the attribution act the mechanism is designed to incentivise. A court assessing proportionality will ask whether the affected party has a reasonable route to better treatment; here the route is immediate, automatic, and within the claimant's own control. $\tau_h$ is a default charge that dissolves on voluntary identification, not a penalty with no exit. That legal character is materially different from a punitive flat rate with no procedural remedy, and it substantially weakens the proportionality objection.

### B.2.5 One carve-out applies 

Some tranche-three positions involve structural opacity with no identifiable beneficial owner at all: genuinely fragmented offshore structures, bearer arrangements, or multi-layer vehicles where no single human holds a challengeable legal interest. These positions face no litigation risk because no claimant exists to bring a challenge. The calibration rationale for these positions shifts from deterrence (there is no decision-maker to deter) toward pure revenue recovery. $\tau_m$ remains the appropriate ceiling for the same revenue-recovery reasons, but the deterrence framing does not apply.

### B.2.6 The resulting calibration range 

The constraints above produce a range. The floor is set by the deterrence condition net of the refund-forfeiture effect: high enough that opacity is economically irrational even for a rational actor who has correctly priced the expected value of forfeited refunds. The ceiling is $\tau_m$, on revenue-recovery grounds. The legal proportionality constraint does not compress this range materially from above: the self-defeating nature of litigation means the practical proportionality ceiling sits at or close to $\tau_m$. The refund-forfeiture effect means the deterrence floor sits somewhat below $\tau_m$, creating meaningful Governing Council discretion within the range. The exact calibration within [deterrence floor, $\tau_m$] is a Phase One decision.

### B.2.7 Phase One data requirement 

The deterrence question cannot be directly observed, because the counterfactual population that chose attribution because $\tau_h$ was high enough is by definition invisible. The best available proxy signals are: attribution test pass and fail rates by entity type, available from the first assessment cycle; the tranche-three share of listed corporate ownership over time, which should decline if deterrence is working; and the composition of tranche-three positions (structural impossibility versus apparent deliberate choice), which indicates whether the opacity is sensitive to rate-based deterrence at all. These signals are slower-moving than the $\tau_0$ data and require three to five assessment cycles before meaningful trends emerge. The Governing Council should set an initial $\tau_h$ on the basis of the analytical range above and treat the Phase One trend data as the primary input to any subsequent revision.

### B.2.8 The ramp structure 

Rather than fixing $\tau_h$ at a single value from Phase One, the Governing Council publishes in advance a schedule under which $\tau_h$ rises from its initial level toward the ceiling of [deterrence floor, $\tau_m$] over a defined transition window, paced by observed aggregate attribution trends. This is not a departure from the calibration framework above; it is the Governing Council's parameterisation of that framework across time rather than at a single point. A pre-announced trajectory has a distinct property that a sequence of undeclared point-in-time revisions does not: it converts $\tau_h$ into a pre-committed cost that companies and ownership structures can plan against, which is itself a deterrence input. An opacity structure calibrated against a known rising schedule is harder to sustain as a stable strategy than one calibrated against a static rate that may or may not be revised.

The observable pacing the ramp is the aggregate tranche-three share of listed corporate ownership across the full assessment universe, computed across all listed companies rather than company by company. A company-specific observable would give companies an incentive to shift large attributable holders in and out of their registers around the measurement point to affect the threshold. An aggregate observable eliminates that incentive: no single company's register movements can materially affect the system-wide tranche-three share, so gaming the observable requires coordinated action across the assessment universe, which is both visible and expensive.

The transitional deterrence gap is accepted. During the ramp period, opacity may remain cheaper than individual WDT assessment for some high-growth concentrated positions at the lower initial $\tau_h$ level. This is tolerable provided the ramp window is short enough that the gap cannot be exploited with confidence across a multi-year holding period. A ramp window of three to five years, matched to the Phase One SRR fill window, limits the exploitable period to a range within which the expected value of sustained opacity does not dominate the expected value of attribution, given the ramp's pre-committed trajectory. A longer ramp requires explicit Governing Council justification against this cost at each review.

### B.2.9 The joint-calibration constraint 

The $\tau_h$ ramp cannot be calibrated in isolation from the displacement of CIT and dividend taxation. As $\tau_h$ rises, companies with significant unattributable ownership tranches face a rising aggregate fiscal burden unless parallel reductions in CIT and dividend tax proceed at a matching pace. Where those reductions do not keep pace with the ramp, the combined burden on attribution-hard companies rises faster than on transparent-ownership companies, creating a wedge that works against the ramp's own goal: a company that finds the combined burden sufficiently punitive has an incentive to maintain opacity as a hedge, since its total tax position is worsening regardless of attribution outcome. The ramp must therefore be co-designed with the CIT and dividend displacement schedule as a single joint trajectory rather than as two independently calibrated parameters (WP §6). Both sit within the Governing Council's authority; the joint-calibration requirement is a constraint on how that authority is exercised. Uniform rollout across industries is the target, not because all industries have identical attribution feasibility — they do not — but because industry-specific rollout rates create arbitrage opportunities: capital structures and holding arrangements migrate toward the industry category facing the slower pace, and the competitive distortion compounds as the divergence widens. Where attribution feasibility genuinely differs across industries, that difference belongs in the ramp's pace parameter, not in differentiated CIT offset schedules that create the arbitrage the ramp is designed to close.

The Governing Council's factional structure is what makes a ramp schedule epistemically superior to technocratic calibration at a single point. TP members from industries with transparent ownership structures have a direct financial interest in fast ramp progression: a lower $\tau_h$ for longer disadvantages them relative to opaque competitors whose effective rate is below theirs. TP members from industries with structurally harder attribution — cross-border financial firms, complex group structures, multi-jurisdiction holding arrangements — have a direct financial interest in slower progression and will argue for it with specificity, because their financial credibility with DR depends on making the attribution-feasibility case accurately. The ramp schedule therefore emerges from a negotiation in which the parties with the best private information about attribution feasibility are also those with the strongest incentive to reveal it accurately. FS counterbalances with fiscal concerns about revenue timing; DR evaluates the competing claims without a stake in the outcome. Phase One attribution data is the audit against which both sets of claims are tested after the fact.

## B.3 Intermediary-Level Provisioning Floor

A pass-through intermediary with comprehensive KYC and confirmed below-threshold registrations for the bulk of its book has substantially lower residual uncertainty than the company. The collection-security rationale for the $\tau_0$ floor applies at the intermediary level too, but the risk profile differs: an intermediary with near-complete attribution has a much smaller unreconciled population than the company does, so the expected shortfall per failure event is lower and the floor can rationally be set below $\tau_0$.

The same self-defeating litigation property that applies to $\tau_h$ at the company level also applies to $\tau_h$ within an intermediary's unattributable remainder. Any beneficial owner within that remainder who contests the charge reveals their identity, triggering reclassification at the intermediary level just as it would at the company level. What this establishes for (CORP.A §B.3) purposes is not that the intermediary-level floor should be higher, but that it need not carry independent deterrence weight against legal challenge: $\tau_h$'s self-defeating character means the proportionality objection does not bind at the intermediary level any more than it binds at the company level. This reinforces the case for maintaining $\tau_0$ as the intermediary-level floor: the $\tau_h$ deterrence effect within the intermediary's book is already secured by the attribution architecture, and the floor's calibration objective remains collection security rather than deterrence.

In practice, if $\tau_0$ turns out to be a small absolute figure and the aggregate sum across intermediary-held retail positions is modest, the simplest answer may be to keep $\tau_0$ as the intermediary floor, accepting a small amount of over-collection against retail positions as an administrative simplification. Whether the efficiency gain from a lower intermediary floor justifies the additional calibration complexity, and at what level to formalise it, remains a Governing Council parameter. A lower floor than $\tau_0$ is available in principle to intermediaries that can demonstrate their book composition and bear the shortfall risk of their own judgment.

For modelling purposes, (RATES) used $\tau_{c}$ = $\tau_{m}$ = 70% as its corporate levy reference calibration. That figure represents the ceiling of the [deterrence floor, $\tau_{m}$] range derived here and remains a reasonable working assumption for revenue estimation pending Phase One attribution data.

## B.4 The Rejected Pool-Average Alternative

An alternative approach, anchoring the corporate rate to the average effective WDT rate across a company's actual shareholder pool rather than to the individual entry-level rate, has been considered and rejected. A pool-average rate would be company-specific, giving companies an incentive to shape ownership composition to minimise it. It also requires estimating an average effective rate for a dispersed, partly anonymous shareholder base, which approaches the attribution problem the corporate mechanism exists to avoid. This paper does not adopt that alternative.

\newpage

# C. Ownership Structure Classification Under the Attribution Test {.appendix}

(CORP §6) establishes a single operative test for every tranche-two holder: can the intermediary identify and attribute its underlying beneficiaries to a degree that supports individual WDT reconciliation? This appendix applies that test to the specific entity types most likely to arise in practice. The classification, not the entity's label, determines treatment.

| Entity | Can identify beneficiaries? | Treatment | Note |
|---|---|---|---|
| Direct individual shareholder | Yes | Pass-through, tranche 1 | Not a tranche-two case; included for contrast |
| Broker/custodian nominee | Usually yes | Pass-through to identified clients; $\tau_h$ on unattributable remainder | Standard case; see (CORP §5.3) and (CORP.A §A.9) |
| ETF/mutual fund | Yes, via unit register | Pass-through; proportional allocation by unit | See (CORP.A §A.9) |
| DC pension fund | Yes in principle; prohibitive at scale | $\tau_0$ final, as a policy boundary | See discussion below |
| DB pension fund | No — defined benefit, not a proportional accumulation claim | $\tau_0$ final | Beneficiary's claim is to a promised benefit, not a share of fund NAV |
| Insurance company | No — contingent claim | $\tau_0$ final | Policyholder claim is contingent on an insured event |
| Endowment/charity | No — no human claimant | $\tau_0$ final | Serves an institutional mission rather than a population with a quantifiable individual stake |
| Foreign sovereign wealth fund | No — outside the WDT system | $\tau_0$ final | No individual liability exists to reconcile against |
| State holding entity | No — no individual claimant | $\tau_0$ final | See circularity note below |
| WDT Sovereign Wealth Fund | No — public institution | $\tau_0$ final | See circularity note below |
| Employee share trust | Yes for vested allocations; no for unvested | Pass-through for vested portion; $\tau_0$ final on unvested tranche | Vested shares are attributable to a named employee; unvested shares have no individual claimant yet |
| ADR depositary | Yes, if the depositary holds KYC on underlying holders | Pass-through to identified holders | Requires foreign information-exchange coordination; treated as a cross-border instance of the standard intermediary case |
| Securities lending borrower | Registered holder of record on assessment date | Normal tranche assessment under whichever category the borrower itself falls into | The assessment-date rule in (CORP §5) applies without modification: whoever is on the register at the assessment date is assessed in that capacity; the lender's claim against the borrower is handled through individual WDT assessment of the lender |

Defined contribution pension schemes. A DC member's account balance tracks fund NAV closely enough that the fund could, in principle, calculate each member's proportional share of the corporate delta and pass the attribution test. The exclusion of DC schemes is a policy boundary rather than a principled failure of that test: extending reconciliation to scheme memberships numbering in the tens of millions, the overwhelming majority of whom are below the WDT threshold and whose credits would lapse unclaimed, creates administrative infrastructure disproportionate to the revenue at stake. This position should be revisited if Phase Two materially lowers the WDT threshold and brings a non-trivial share of DC membership above it. Defined benefit schemes are excluded for the separate, principled reason given in the table: a DB member's claim is to a promised benefit rather than a proportional share of fund performance, and so does not pass the attribution test regardless of administrative capacity.

The attribution test applies in binary form in its settled steady-state design. A phased on-ramp during Phase One, partial pass-through treatment proportional to attributed book share for intermediaries demonstrating improving capability, is available as a Governing Council calibration parameter if Phase One uptake data supports it. By Phase Two the binary test applies without graduation.

State holding entities and the WDT Sovereign Wealth Fund. Where the state itself (through a state holding company, a strategic stake, or the WDT's own Sovereign Wealth Fund) holds shares in a listed company, no individual claimant exists behind that holding. The treatment is $\tau_0$ final at the company level. A circularity worth naming: the state, acting through the SWF, would in this scenario be both the entity levying the corporate charge and a holder being charged it. This is not a design flaw. The final charge on the SWF's own holdings becomes a transfer within the state's own accounts; revenue that the corporate mechanism would otherwise have collected from a private holder is instead retained by the SWF as the holder of record, and it is recorded as such rather than netted out silently, so that the SWF's investment performance and the corporate mechanism's collection figures both remain legible on their own terms.

\newpage

# D. Administrative Burden

## D.1 Purpose

This appendix examines the administrative requirements the WDT corporate mechanism creates and compares them with the systems it replaces, assuming a mature WDT framework in which corporate income taxation, dividend taxation, and capital gains taxation have been retired. Transitional overlap is addressed in §E.6. The central question is whether the new requirements are greater than those of the systems they replace. The short answer is no: for listed companies and retail shareholders, mature WDT compliance is substantially lighter than the systems it displaces. The burden shifts rather than grows, and it shifts selectively — falling most heavily on the one population for whom the current system's tolerance of opacity has been most valuable.

## D.2 Shareholder Compliance

**Retail shareholders.** Under existing systems, shareholders manage dividend taxation, capital gains reporting, acquisition cost records, holding periods, and transaction-level calculations including same-day matching rules, bed-and-breakfast provisions, and Section 104 pooling. Under a mature WDT system this entire transaction-tracking obligation disappears. Shareholder compliance shifts from event-driven reporting to annual wealth reporting: year-end holdings, market value, and corporate WDT credits. All three are already held by brokers and custodial systems and can be reported automatically. Below-threshold retail shareholders who register once have no further compliance obligation in relation to listed holdings at all. The compliance reduction for this population is categorical, not marginal.

**Above-threshold native shareholders.** The corporate credit appears as a single line in the annual WDT return, populated automatically from the delta statement issued by the company or broker. No transaction-level matching is required. Capital gains and dividend tax reporting obligations are retired. Net annual burden is lower than under current systems.

**Large shareholders and institutional investors.** Large shareholders require reconciliation capability because corporate WDT credits depend on ownership classification. The relevant information — beneficial ownership, ownership percentage, credit eligibility, and reconciliation between corporate payments and individual liabilities — overlaps substantially with existing obligations under PSC register requirements, FATCA, DOTAS, and securities reporting. The WDT changes the purpose of this data rather than requiring new data infrastructure. The incremental burden is real but modest for institutions already maintaining compliant KYC and ownership disclosure systems.

## D.3 Automatability and Corporate Compliance

The corporate levy mechanism is primarily automatable at the company level. The inputs it requires are: market capitalisation on a fixed annual date, which is public and machine-readable; the shareholder register at that date, already maintained electronically under company law; and the tranche classification of each registered holder, largely derivable from KYC and beneficial ownership data already held under AML and securities regulation. The delta calculation is arithmetic. The provisional levy payment is a single annual transaction. Delta statement issuance is a batch process against the existing register. Credit release is triggered by settlement confirmation from the tax authority — a data-matching exercise. None of these require new data collection. They require repurposing data that already exists.

The tranche-two classification is factual and self-declaring, not a judgment exercise. An intermediary either produces a consenting, identifiable next-level holder — at which point the chain extends and attribution continues — or it does not, at which point the chain terminates and $\tau_h$ attaches to the unresolved remainder. There is no evaluation of sufficiency and no discretion at the point of application. The only human judgment involved is in the legislative definition of the attribution test itself; applying that definition to any specific holding is mechanical.

Three recurring administrative functions follow from this.

**Corporate delta calculation.** The delta is the change in market capitalisation between assessment dates — public data, requiring methodology alignment rather than new measurement. Listed companies already perform related exercises for financial reporting, impairment testing, and investor disclosures. The additional work is producing a tax-relevant figure on a defined annual date, not developing new valuation capability.

**Shareholder reconciliation.** Companies classify their register into three tranches at assessment date. For most registers this is a standing classification requiring update only on ownership changes. Intermediaries that pass the attribution test carry their own downstream reconciliation obligation — classifying their client books and submitting reconciliation returns — built on existing KYC infrastructure. This is the primary area where the WDT creates new incentive rather than new burden: improved ownership transparency at each tier of the chain reduces $\tau_h$ exposure, so the financial cost of not maintaining attribution capability is larger than the cost of maintaining it.

**Corporate provisioning.** Setting $\tau_{prov}$ and paying the provisional levy is comparable to existing corporate tax provisioning and regulatory capital calculations. For most companies this is a simpler annual calculation than the deferred tax accounting, uncertain tax position reserves, and transfer pricing documentation that CIT compliance currently requires.

## D.4 Comparative Burden: Companies

The burden comparison with current CIT compliance is directionally clear and worth stating plainly. Large listed company CIT compliance currently involves transfer pricing documentation across jurisdictions, intercompany loan analysis, thin capitalisation calculations, deferred tax accounting across multiple bases, R&D credit claims, loss carry-forward management, country-by-country reporting, and annual negotiation of uncertain tax positions with HMRC. Each element requires specialist input and generates significant advisory cost.

The corporate delta levy in a mature WDT replaces this with: one delta calculation, one provisional payment, one batch of delta statements, and one settlement account reconciliation at the year close. The tranche classification exercise is added, but it sits on existing infrastructure and is largely standing rather than annual. For a large listed company with a predominantly identifiable shareholder base, total compliance cost in a mature WDT is substantially lower than current CIT compliance. §E.4's prior framing — that the WDT "changes the composition rather than the total number of compliance functions" — understates this: for large listed companies, the total burden falls.

The population for whom burden increases is narrow and specific: intermediaries and holding structures that currently operate with deliberate opacity and have relied on the current system's tolerance of nominee arrangements. For them, the choice is invest in attribution infrastructure or pay $\tau_h$. That is a designed incentive, not an inadvertent compliance cost, and it is the mechanism through which the corporate instrument achieves its coverage objective.

## D.5 Valuation Requirements

The largest technical change is the shift from transaction-based to annual wealth measurement. For listed companies, valuation is straightforward: market capitalisation on a fixed date is public, unambiguous, and requires no professional judgment. This is a material simplification relative to current systems, where declared profit — the CIT base — is a construct involving discretionary judgments across transfer pricing, impairment, depreciation, and provisions.

For companies with significant private assets or subsidiaries, requirements increase. But corporations already perform valuation exercises for acquisitions, financial reporting, impairment testing, and regulatory disclosures. The WDT expands the use of these processes; it does not create new valuation capability from scratch.

## D.6 Transitional Considerations and the Parallel-Running Risk

The transition period — during which WDT reporting runs alongside unreformed CIT, dividend tax, and capital gains tax — is the period of maximum administrative burden and the principal implementation risk on the compliance dimension. Companies and intermediaries must simultaneously maintain two full compliance regimes. Transitional compliance cost will exceed both the current steady state and the mature WDT steady state. This is not a feature of the WDT's design; it is an argument for minimising the parallel-running period as an explicit implementation objective rather than treating it as an unavoidable phase of indeterminate length.

The transition design question — how quickly existing corporate tax systems are retired relative to WDT introduction — is therefore not merely political but has direct compliance cost consequences. A longer parallel-running period imposes higher aggregate compliance cost on companies and intermediaries with no offsetting revenue or design benefit. Implementation sequencing should treat parallel-running duration as a cost to be minimised, not a transition management tool to be extended for comfort.

International ownership introduces additional requirements: beneficial ownership identification across jurisdictions, information exchange, and cross-border credit recognition. These are primarily coordination questions rather than domestic design problems, but they bear on the transition timeline: jurisdictions with strong existing information-exchange infrastructure (FATCA, CRS) face a shorter path to functional international tranche classification than those without it.

## D.7 Summary

The corporate WDT mechanism is primarily automatable for listed companies. Its inputs — market cap, shareholder register, tranche classification — are either already public or already held by the relevant parties under existing regulatory obligations. The principal new compliance requirement is ownership transparency, and the mechanism is designed so that the financial cost of not maintaining that transparency ($\tau_h$ exposure) exceeds the cost of maintaining it.

The net burden comparison against current systems runs as follows. Retail shareholders: categorically lower — transaction tracking eliminated, annual filing reduced to year-end wealth data already held by brokers. Above-threshold native shareholders: lower — credit claim is a single automated line; CGT and dividend reporting retired. Listed companies: substantially lower in a mature implementation — delta calculation and tranche classification replace a substantially more complex CIT compliance regime. Intermediaries with maintained attribution infrastructure: modest increase on existing KYC obligations, largely automatable. Intermediaries and structures dependent on opacity: material increase, by design.

The one period of elevated burden is the transition, during which parallel running of old and new systems creates overhead that exceeds both the prior and successor steady states. Minimising parallel-running duration is therefore an explicit implementation design objective with direct compliance cost consequences, not merely a political timing preference.

\newpage

# E. Non-Corporate Instruments and the Attribution Test {.appendix}

## E.1 Purpose

This appendix applies the attribution test established in (CORP §6) to entity types that are not listed companies and not private companies held under individual assessment. The test is the same in every case: can the instrument identify and attribute its underlying beneficiaries to a degree sufficient to support individual WDT reconciliation? What differs across instruments is how that question resolves, and what follows when it does not.

The WDT requires no special regime for any of these instruments. Neutral application of the attribution test, the delta mechanic, and the existing tranche structure produces the correct outcome in each case. Where the current tax system grants special treatment to particular legal forms (charitable status, partnership structures, insurance wrappers), the WDT is indifferent to those labels. Behaviour determines treatment, not legal form.

Where attribution fails entirely and no individual marginal rate can be applied, the entity pays at $\tau_m$ by default. This is not a separately designed entity rate. It is the ceiling rate of the individual progressive schedule (CORP.A §B.2.3), and an entity that cannot or will not identify attributable beneficiaries receives no benefit of the lower brackets that transparency would have unlocked. This principle applies wherever $\tau_m$ is invoked in the sections below.

## E.2 Charitable Vehicles

### E.2.1 The Attribution Question

A charitable entity is an instrument. It holds no welfare of its own. The attribution test therefore asks, as with any intermediary, whether a continuous chain exists from the entity to identifiable humans whose individual WDT assessment can absorb the relevant delta. For most charitable vehicles the answer is no, and the reason is structural rather than administrative. Donors have relinquished legal title to their contributions. The charitable recipients who benefit from the entity's activities hold no proprietary claim on its asset base. There are no humans with legal beneficial interests in the corpus to pass through to by default.

Two routes create attribution where it would otherwise be absent. The first applies where a founding donor or their family retains effective control of an endowment's investment and grant-making decisions through board dominance or reserved powers. Something economically analogous to a beneficial interest exists in those cases and the attribution test is live on the facts. Loss of effective control (independent governance, arm's-length board, no family representation) dissolves the attribution concern, because at that point the wealth has separated from any identifiable human.

The second route is voluntary registration. Any individual may register as a beneficiary of any entity, including a charitable entity, with that entity's agreement. Registration creates an attribution relationship for WDT purposes only. It confers no legal or equitable interest in the entity's assets, no governance rights, and no claim on distributions. What it does is make the registrant's WDT position available to the entity's attribution chain in both directions: the entity's positive deltas flow through the registrant's individual assessment at their own marginal rates, reducing the entity's $\tau_m$ exposure on the registered tranche; and the entity's negative deltas can draw on the registrant's lifetime contribution envelope to support refund entitlement, up to the registrant's cumulative contribution history.

The individual cost in gain years is real. A voluntary beneficiary pays WDT on their allocated share of the entity's delta as if that appreciation had accrued in their own portfolio. This makes voluntary registration a form of financial support: the individual deploys their tax envelope on behalf of the entity rather than making a cash donation. The support scales with the entity's actual financial experience: in good years the registrant bears a tax cost; in bad years their contribution history backstops a refund the entity could not otherwise access. For charitable entities that would otherwise face $\tau_m$ on any net accumulation and have no refund access at all, a community of voluntary registrants materially changes the economics of the institution.

The lifetime contribution envelope constraint governs refund access. Cumulative refunds flowing through a voluntary registrant's envelope cannot exceed their cumulative WDT contributions. A registrant with a long contribution history can meaningfully support an entity's bad years; one with no contribution history offers nothing on this dimension. No special rule is required to enforce this: the envelope constraint operates automatically and symmetrically for voluntary beneficiaries as for any other taxpayer.

The mechanism is available to any entity type, not only charitable ones. Its practical importance is greatest where the attribution chain would otherwise fail entirely, which is the charitable and mission-driven space, where conventional ownership structures are absent by design.

The same logic runs in reverse. A charitable entity whose activities generate genuine net losses — deploying more than it receives, or holding assets that fall in value — produces a negative delta. Where beneficiaries have accepted attribution, that negative delta flows through their individual assessments as refund entitlement against their contribution history. The mechanism therefore rewards genuine charitable deployment twice: it removes the tax cost of accumulation and it allows loss years to benefit the humans who have committed their tax envelopes to the entity.

### E.2.2 Operating Charities

A genuine operating charity takes in donations and deploys them. Its net assets do not accumulate year on year because it spends what it raises. No positive delta arises. No WDT liability arises. This outcome requires no special provision.

On the donor side, the gift reduces the donor's net worth. That reduction is a negative delta under ordinary WDT mechanics, reducing the donor's liability in a gain year or generating a refund entitlement in a loss year. The current tax system's charitable giving relief is replicated automatically by the delta mechanic without any charitable exemption regime being required. The WDT is indifferent to whether the wealth reduction flows to a charity, another person, or any other destination.

Where a charity receives a large donation and holds it as reserves before deployment, its net worth increases in the year of receipt. That increase is a positive delta. The same $\tau_m$ treatment that applies to accumulating endowments applies here: the incentive is toward rapid deployment rather than accumulation. A charity that deploys promptly generates no taxable delta; one that holds reserves accumulates a growing tax cost. No special rule is required to produce this outcome; it follows from the delta mechanic applied neutrally.

### E.2.3 Accumulating Endowments

An endowment that invests its corpus and distributes less than its investment return accumulates net assets year on year. This is a positive delta. Attribution typically fails by design, for the reasons given in (CORP.A §E.2.1). The default treatment applies: $\tau_m$ on the net asset growth, with no refund symmetry.

The asymmetric loss treatment follows from the same principled grounds as the corporate instrument's treatment of loss years established in (CORP §3). The entity does not experience losses in any humanly meaningful sense. Its balance sheet movements are not events in anyone's welfare. The refund mechanism exists because the same human who paid tax in good years deserves protection in bad years; that logic has no application to an endowment's investment portfolio.

The practical consequence is that the $\tau_m$ charge on net accumulation creates a strong incentive to deploy capital rather than compound it inside a charitable wrapper. This is what charity law already requires as a matter of principle but frequently fails to enforce in practice. The WDT enforces it through the cost structure rather than through regulatory oversight.

### E.2.4 Refund Direction

A person with WDT contribution history may nominate any entity — charitable or otherwise — as the recipient of their refund payment in a loss year. The refund belongs to the human. They may direct it to any recipient, including a charitable entity. The SWF pays whoever the person nominates; the person's lifetime contribution envelope reduces accordingly. No special mechanism is required and no special charitable status is conferred. This is ordinary freedom to direct one's own money, applied to a payment the symmetric refund mechanism generates. The charitable context is an example, not a limit: the same freedom applies to any nominated recipient. The calculation of the refund is unaffected by the nominated recipient: the amount is determined by the person's own contribution history and delta, not by the identity of the payee.

## E.3 Special Purpose Vehicles and Holding Companies

Special purpose vehicles and holding companies are currently used to defer realisation events, shift profits between tax jurisdictions, and interpose a lower-rate entity between income and the individual taxpayer. Each of these functions depends on the existence of multiple tax bases with different rates and different triggering events. The gap between income tax rates and capital gains rates creates income-to-capital conversion incentives. The gap between realisation and accrual creates deferral incentives. The gap between corporate and individual rates creates interposition incentives.

The WDT eliminates these gaps rather than targeting the vehicles that exploit them. A holding company's value is an asset in the individual owner's net worth. If the holding company appreciates, the individual's declared net worth appreciates by the same amount. The interposition achieves nothing because the delta flows through to the individual regardless of how many corporate layers sit between the individual and the underlying assets. The valuation route question is live (a holding company full of listed assets sits naturally on Route A; a complex private portfolio may require Routes C or D), but the route governs how the value is established, not whether it is. The delta accrues to the individual owner in every case.

Where an SPV or holding company itself holds shares in a listed company, it appears on that company's register as a tranche-two identified intermediary. The listed company pays $\tau_0$ on its registered tranche. The SPV then runs its own assessment against its own book: $\tau_0$ on each level it can attribute, $\tau_h$ on whatever it cannot. The individual WDT treatment and the corporate levy chain are separate tracks operating simultaneously; this section addresses the former and the corporate levy chain resolves through the intermediary mechanism in CORP §5 without requiring any additional rule.

## E.4 Trusts

Family trusts and discretionary trusts are currently used to fragment wealth across beneficiaries to reduce marginal rates, defer estate taxation, and obscure beneficial ownership. Under the attribution test (CORP §7), the operative question is whether the trust can identify and attribute its underlying beneficiaries to a degree sufficient to support individual WDT reconciliation.

Where the trust holds listed equity, it appears on the relevant company's register as a tranche-two intermediary and the corporate levy chain applies on those terms. Where the trust holds other assets, each attributable beneficiary's allocated delta flows into their individual WDT assessment directly. In both cases the operative question is the same: is there a consenting, identifiable human at the end of the chain?

This inverts the incentive structure of the current system. Under current law, deliberate opacity through discretionary trust structures is either free or actively rewarded by rate differentials. Under the WDT, deliberate opacity is costly: $\tau_m$ at entity level is more expensive than the marginal rates the identifiable beneficiaries would face individually. The trust therefore has a strong financial incentive to identify its beneficiaries and pass through. Systematic misdirection of beneficial ownership becomes a tax strategy that costs more than the transparency it avoids.

## E.5 Family Limited Partnerships and Similar Structures

Family limited partnerships and analogous vehicles are used to apply valuation discounts (minority interest discounts, lack-of-marketability discounts) to transfer wealth at reduced values for gift and estate tax purposes, and to shift income flows to lower-bracket family members.

The valuation discount problem is real but partially self-correcting through the delta mechanism. A taxpayer who declares a limited partnership interest at a substantial discount today establishes that declared value as the recognised basis. When the interest is later sold or attributed at a higher value, the accumulated gap enters the tax base at that point through the ordinary delta calculation. The discount defers tax rather than eliminating it, and the cost of that deferral compounds with the asset's growth rate. (VAL.A §C) establishes the magnitude of this effect at RATES-aligned parameters; the self-correcting property is structural rather than calibration-dependent.

The income-shifting function collapses more completely. The WDT taxes net worth change, not income flows. Redirecting dividend or profit distributions between family members through a partnership structure does not change the aggregate delta of the family's holdings. A pound shifted from a high-bracket family member to a lower-bracket one through a partnership structure reduces one member's income tax exposure under the current system; under the WDT it has no effect on the aggregate wealth delta that the mechanism is tracking.

## E.6 Life Insurance Wrappers

Life insurance wrappers are used to shelter investment returns inside a policy, access accumulated value through policy loans without realisation, and achieve tax-free transfer of the death benefit. Each function depends on the insurance wrapper being treated as a different instrument from the underlying investment portfolio for tax purposes.

The WDT is indifferent to this categorisation. The policy's cash value is an asset in the policyholder's net worth. Its appreciation from one assessment date to the next is a positive delta. The insurance wrapper does not change what is happening economically: wealth is accumulating inside the policy, and that accumulation enters the delta calculation in the same way any other asset appreciation does. Policy loans do not reduce net worth because they add both an asset (the loan proceeds) and a liability (the repayment obligation) simultaneously. On death, the policyholder's WDT position terminates. The policy's cash value at the date of death is settled as a final delta through the position closure mechanics in (CLOSE §4.1). The death benefit paid to named beneficiaries is distinct: it is new wealth entering those individuals' net worth at the date of payout, not a transfer of a previously declared asset. It generates a positive delta for each recipient in the year of receipt, assessed through their own individual WDT at their own marginal rates. Where the death benefit exceeds the policy's declared cash value — as it typically will, since life policies pay out more than cash value on death by design — that excess enters the recipient's delta in full. No inheritance mechanics are involved; the inheritance mechanics govern transfer of existing declared assets, and the death benefit excess was not previously sitting in anyone's WDT position.

## E.7 Carried Interest and Performance Fee Structures

Carried interest and similar performance fee structures are currently treated as capital gains rather than income in most jurisdictions, achieving a lower rate on what is economically a fee for asset management services. The debate about whether this characterisation is correct has been live in tax policy for decades without resolution, because the current system's answer depends on which of two differently-rated tax bases the receipt falls into.

The WDT makes this debate irrelevant. The mechanism asks only whether net worth increased, not what caused the increase or what legal character the receipt carries. Carried interest crystallises into wealth when it vests or is realised; at that point it enters the recipient's net worth and generates a positive delta. The rate applicable to that delta is determined by the recipient's total net worth at assessment, not by the income or capital characterisation of the underlying transaction. The recharacterisation strategy produces no tax saving because the characterisation has no bearing on the applicable rate.

## E.8 The General Principle and Its Limits

The sections above share a common structure: each begins with a legal vehicle currently used to achieve a tax advantage, identifies which gap in the existing system the vehicle exploits, and shows that the WDT closes the gap at the base rather than by targeting the vehicle. The general principle is that conventional tax avoidance is a legal-category game — its profitability depends on gaps between differently-rated or differently-timed tax bases — and the WDT removes most of those gaps by asking a simpler question: where did the wealth go?

The conditions required to defeat the WDT through structural means are mutually incompatible. A taxpayer seeking to retain genuine durable economic benefit while avoiding attribution must simultaneously hold that benefit as a durable entitlement, maintain effective control, and possess no legally or economically attributable asset or claim. Durable benefit under effective control produces an economic claim. An economic claim held through another entity resolves through attribution or bears $\tau_m$. An undervalued asset creates a valuation problem rather than an ownership escape; the recognised-basis mechanism defers rather than eliminates liability. Genuinely transferred wealth leaves the taxpayer poorer. No construction threads this needle.

This is not a claim that the WDT defeats all avoidance. Valuation accuracy at the very top of the distribution, where the hardest-to-value assets are concentrated and professional judgment is most consequential, remains a permanent challenge addressed in VAL and VAL.A. The Route D entry basis is the genuine residual gap — the one point at which the passive architecture cannot self-correct without the auction mechanism's intervention. But the structural conditions under which conventional avoidance works, primarily the legal-category gaps that make changing the form of a transaction change its tax treatment, are removed rather than merely targeted. What remains is narrower and more tractable than the avoidance surface facing most existing systems.

## E.9 Market Manipulation and the Bilateral-Claim Structure of Short Positions

Market manipulation raises a different question from ownership restructuring: not whether a taxpayer can re-engineer their own position to avoid attribution, but whether third-party price manipulation can produce durable WDT consequences — for the manipulator, for a target, or for the reference company.

The analysis turns on a structural property of short positions. A short position is a bilateral claim between counterparties. The short seller's gain, if the reference asset falls, runs against the party on the other side of the trade, not against the reference company itself. The reference company is the measurement point for the contract, not a party to it. Therefore the fate of the reference company — whether it survives, is wound up, is restructured, or is reconstituted under a new vehicle — does not alter the bilateral claim. A short seller who profits as a company's value falls and then collapses has gained through the counterparty relationship; the wealth created by that gain has entered the short seller's net worth through the position's delta across assessment dates. Subsequent changes to the corporate structure create no further tax event and provide no mechanism for eliminating the recognised gain. The "short → destroy company → resurrect elsewhere" strategy that can defer or extinguish realisation events under realisation-based systems achieves nothing here: the short seller's wealth moved when the position was marked, not when the company's legal structure changed.

The treatment of the short seller's position under individual WDT is through ordinary assessment. The gain on the position, whether a listed equity short, an OTC derivative, or a structured note referencing the company's price, enters the short seller's net worth as the position moves. At assessment, the delta is included in the individual's total net worth change and taxed at the applicable marginal rate. Closing the reference company does not reopen a prior assessment period or create a new basis event for the short. Reconstituting the position in a new vehicle simply opens a new asset with its own delta history from inception.

The corporate levy is uninvolved. (CORP §8) establishes that derivative holders have no position in the corporate levy's reconciliation ledger because their claim runs against a counterparty, not the company. A short seller does not appear on the company's share register, receives no delta statement, and has no credit to claim or tranche to occupy. The analysis here concerns the individual WDT treatment of the position's economic gain, not the corporate mechanism.

The reverse attack — deliberately inflating a target's asset value before their assessment date to force their WDT liability higher — is self-correcting through the delta mechanism. Suppose a manipulator drives an asset held by a third party from its true value of £100m to £150m at assessment. The target recognises a +£50m delta and pays WDT at their marginal rate. When the artificial inflation reverses, the target recognises a −£50m delta and receives a proportional refund. The attack does not produce a permanent tax wedge; it produces a timing cost at most. The manipulator's own gain from the price movement — through a long position unwound at the inflated price, for instance — enters the manipulator's net worth as a positive delta and is taxed through the manipulator's own assessment in the ordinary way.

Two properties follow. First, market manipulation can still cause real harm to targets through mechanisms unrelated to the WDT — reputation, forced selling, legal exposure — but it does not produce a clean, privately bounded WDT payoff for the manipulator. The manipulator's gain is taxed; the target's artificial liability self-corrects. Second, the WDT does not need to detect or characterise manipulation to handle it correctly. The mechanism follows economic positions and their changes rather than depending on the legal sequence by which those changes occurred. The state does not need to win an evidentiary contest about whether a given price movement was genuine. It taxes what happened to net worth between assessment dates, whoever caused it and for whatever reason. The self-correcting property operates without any finding of manipulation, which is consistent with the WDT's broader posture of passive collection rather than active detection.

The one residual is assessment-date gaming through coordinated price movement — a manipulator briefly pushing an asset's price down just before the target's assessment date and up just after, creating an artificially low delta in the target's favour rather than an artificially high one (CORP §5.10). This is structurally analogous to the sell-and-repurchase gaming already noted in (CORP §5.6), and is bounded by the same constraints: trade scale, gap length, and the carrying cost of the manipulation over the window. It is an accepted imperfection present in any annual measurement system rather than a structural vulnerability of the WDT specifically.

A further manipulation vector: deliberate weaponisation of the attribution test against a target company. A hostile actor acquires a stake through an opaque intermediary structure and deliberately refuses attribution — not to reduce their own WDT liability but to impose $\tau_h$ on the target's unattributed tranche, suppressing growth, reducing the share price, and making the target more vulnerable to subsequent acquisition at a depressed valuation.

The attack is real but structurally self-limiting. Strategic opacity and effective shareholder activism are mutually exclusive under the WDT. Exercising any shareholder right — voting, requisitioning a general meeting, blocking a resolution, signalling a bid — requires identifying the beneficial owner, which is itself an attribution event that dissolves $\tau_h$'s application to that position. The attacker must choose between the $\tau_h$ weapon and the shareholder activism weapon; the mechanism does not permit both simultaneously.

The $\tau_h$ ramp adds a time dimension. A pre-announced rising trajectory means sustained multi-year pressure campaigns become progressively more expensive for the attacker, while the attacker's own position generates no loss-year refund protection due to refund forfeiture on unattributed positions.

For large-stake attacks, existing Takeover Panel disclosure thresholds require beneficial owner identification at levels likely sufficient to impose meaningful $\tau_h$ burden on a significant company. The WDT amplifies an existing regulatory problem rather than creating a new one.

The residual is a short-horizon sub-disclosure-threshold purely financial attack: building a stake below mandatory disclosure levels, imposing $\tau_h$ pressure for one or two assessment cycles, and exiting into a depressed price. This requires no shareholder activism tools and evades the Takeover Panel threshold. The appropriate response is a flag-event publication mechanism analogous to the Route D audit flag: where the Administrator's mandatory data shows an unusual concentration of unattributed ownership at a specific company against the population baseline, the Administrator publishes a flag noting the anomalous pattern without making a judgment about intent. The flag is a transparency mechanism, not an enforcement one, consistent with the Administrator's transmission-only function.

As noted in (CORP.A §E.8), the conditions required to sustain a meaningful attack through structural means are progressively harder to satisfy as the mechanism matures. The WDT substantially closed this attack vector through its attribution architecture before the attack was identified as a problem.

# F. $\tau_f$: Foreign Attribution and Diplomatic Rate-Setting

Where the attribution chain breaks at a foreign entity, the unattributed portion bears $\tau_f$ rather than $\tau_0$. $\tau_f$ is not a WDT parameter; it is set by bilateral or multilateral diplomatic agreement between the WDT jurisdiction and the foreign entity's home jurisdiction. Where no agreement exists, $\tau_f$ defaults to $\tau_h$ — the implicit cost that gives foreign jurisdictions an incentive to negotiate. The FS chamber is the natural advocate for pursuing such agreements; TP and DR may hold different interests on pace and terms. The outcome is democratic, not a technocratic calibration.

The mechanism recommends that $\tau_f$ vary on two factors jointly: the home jurisdiction's overall attribution cooperation, and the individual company's own attribution percentage. A company in a cooperative jurisdiction with thorough attribution pays near $\tau_0$ on its residual. A company in a non-cooperative jurisdiction with no attribution effort pays the maximum $\tau_f$ for that jurisdiction. The rate moves with attribution quality rather than switching between fixed tiers.

The compliance burden of operating under $\tau_f$ falls entirely on structures that resist attribution. A company with complete attribution has no $\tau_f$ exposure. This is deliberate: complexity and burden scale with opacity, extending domestically the principle that the economically rational strategy is the one that produces the information the mechanism needs.

Attribution is self-declared initially. The legal claim that declaration establishes is the near-term output: a traceable human-to-asset relationship in the WDT's records, regardless of whether it can be independently verified. As Valuation Body capacity develops, overseas verification becomes progressively available. Even where $\tau_f$ is negotiated low, the attribution process forces a legal claim to exist — a form of visibility the pre-WDT architecture did not produce.

The refund-forfeiture effect applies to unattributed foreign holdings as to domestic tranche-three positions. Portions bearing $\tau_f$ as a final charge forfeit access to the symmetric loss-refund mechanism, independently of the $\tau_f$ rate, partially substituting for rate-based deterrence where $\tau_f$ has been negotiated low.

A low $\tau_f$ is a genuine coverage gap: a foreign company with no attribution incentive can declare its entire holding unattributable, pay $\tau_f$ on that portion, and the WDT mechanism has no domestic lever to compel more. No paper trail beyond the payment itself is created. This is accepted as a structural limit of what a unilateral domestic mechanism can achieve internationally.

The gap is nonetheless visible, costly, and recoverable — not through the mechanism, but through the political process the mechanism makes legible. The decision to negotiate a low $\tau_f$ is a public act: it appears in the diplomatic record, in Governing Council deliberations, and in the Administrator's published attribution data by jurisdiction. A government that accepts too low a rate with a publicly unfavoured jurisdiction faces domestic political pressure. Within the Governing Council, DR can push TP and FS to act; some TP members will be independently displeased, since a low $\tau_f$ for foreign-held positions undercuts domestic competitors and encourages tax-driven restructuring whose benefits fall unevenly across the TP population. FS positions will vary with the political situation and cannot be predicted in advance. The record of which $\tau_f$ rates were set, with whom, and what attribution flows resulted is permanent — available to future Governing Councils and future governments as evidence for renegotiation. The gap is not closed by the mechanism. It is made structurally legible and politically accountable in a way that pre-WDT offshore sheltering was not.

---

# G. Existing $\tau$ parameters

| Symbol | What it is | Calibration home |
|---|---|---|
| $\tau_0$ | Individual WDT entry-level effective rate; floor for corporate provisional levy; provisional final charge on identified intermediaries at company level | Governing Council Tier 1; CORP.A §B.1 |
| $\tau_{prov}$ | Provisional levy rate set by the corporation; must be ≥ $\tau_0$; corporation bears shortfall risk of its own choice | Corporation's own governance decision; no GC calibration required |
| $\tau_h$ | Final charge on permanently unattributable ownership; calibration range [deterrence floor, $\tau_m$]; ramp structure in CORP.A §B.2 | Governing Council Tier 1; CORP.A §B.2 |
| $\tau_m$ | Individual WDT top marginal rate; ceiling for $\tau_h$ | Set by RATES; not a CORP parameter |
| $\tau_c$ | Corporate levy reference calibration used in RATES modelling; currently set at $\tau_m$ = 70% pending Phase One data | Working assumption in RATES.A; not independently calibrated |
| $\tau_f$ | τ_f diplomatic rate-setting (bilateral/multilateral agreement; not a WDT parameter). Ceiling on unattributable ownership by foreign companies of WDT jusrisdiciton assets |

