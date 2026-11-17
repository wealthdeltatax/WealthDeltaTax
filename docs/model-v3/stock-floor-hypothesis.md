# Hypothesis: a low-rate stock-wealth floor alongside WDT

**Status:** exploratory hypothesis; not an adopted design decision  
**Date:** 2026-11-17  
**Owner:** author  
**Purpose:** record a possible extension to WDT for discussion and later testing. This document does not change the settled WDT mechanism, model-v3 specification, metric register or output manifest.

## 1. The problem this hypothesis addresses

The WDT's central ambition is to replace the existing tax system, rather than become one more tax layered onto it. Its principal instrument is a progressive annual tax on changes in an individual's net wealth, with symmetric loss refunds and a lifetime contribution envelope.

A concern has emerged that a tax on wealth changes alone may not provide a sufficiently broad or stable fiscal base to replace the taxes it is intended to retire. Wealth can remain substantial while its measured annual change is small or negative. Revenue from a delta base may therefore be volatile, sensitive to return paths and constrained by the refund commitment.

A separate political and administrative concern is that conventional annual stock-wealth-tax proposals often use rates that create substantial liabilities relative to the cash income or liquidity of some asset-rich taxpayers. This is particularly acute for owners of private businesses and other illiquid assets. Such liabilities can create opposition, forced sales, avoidance and pressure for exemptions that undermine the tax base.

The hypothesis is that these weaknesses may be addressed by combining the two bases rather than choosing between them.

## 2. The proposed combination

The combined system would have two components:

1. **Progressive wealth-delta component (WDT):** retain the existing progressive tax on annual changes in net wealth, together with its symmetric loss-refund mechanism and Sovereign Wealth Fund architecture.
2. **Low-rate stock-wealth component:** add a flat annual rate on the portion of an individual's net wealth above a separate, high exemption threshold.

The stock component would tax the stock above its threshold, not the taxpayer's entire wealth. The threshold would be distinct from the existing WDT entry threshold unless later analysis supports combining them.

The stock rate would be deliberately low. The proposition is not that a low rate is painless for every taxpayer, but that above a sufficiently high threshold it may be modest relative to the wealth being taxed, while the aggregate base could still produce material revenue.

The combined system is intended to remain one coherent WDT fiscal architecture, not a return to a collection of unrelated taxes. The stock component would be a supplementary base within the proposed replacement system.

## 3. Core hypothesis

> There may be a high level of wealth above which a low, flat annual charge on the stock of net wealth is a relatively small burden for most affected taxpayers. Applied above a high threshold and combined with progressive rates on annual wealth changes, this charge could generate substantial and more stable revenue without requiring the higher stock-tax rates that create strong resistance among asset-rich but illiquid taxpayers.
>
> If stock-tax payments also count towards the taxpayer's lifetime contribution envelope, they would contribute to the taxpayer's cumulative entitlement to qualifying WDT loss refunds. This could make the stock component more acceptable by giving the payment a second function: it helps finance the state while also increasing the taxpayer's protection against future losses.

This is a proposition to test, not a conclusion. In particular, the claim that the charge is incidental above a given threshold must be tested against asset composition, income and liquidity, not inferred from net worth alone.

## 4. Interaction with the lifetime contribution envelope

The existing WDT design caps cumulative refunds by the taxpayer's cumulative tax contributions. The proposal is to count qualifying stock-wealth-tax payments as contributions to that same lifetime envelope.

In simplified terms:

`Lifetime contribution envelope = cumulative WDT paid + cumulative qualifying stock tax paid`

The envelope would continue to limit total refunds. Stock-tax payments would not automatically be refunded, would not generate a refund in isolation, and would not turn the stock tax into a personal savings account. They would increase the amount of cumulative contributions against which a future qualifying WDT loss refund could be paid.

This is the least disruptive initial interpretation of the proposal because it extends the existing contribution principle rather than inventing a separate insurance product.

However, the accounting and fiscal consequences need careful examination:

- If stock-tax payments increase the refund ceiling pound-for-pound, the state receives durable revenue only to the extent that the additional refund capacity is not subsequently used.
- If the stock tax is paid in years when WDT losses arise, the taxpayer may still face a stock-tax cash liability while being eligible for a WDT refund. The timing and net cash-flow treatment matter.
- Counting stock-tax payments in the envelope may create refund liabilities that would not exist under WDT alone. The model must recognise these liabilities when assessing reserve requirements and solvency.
- The rule must be consistent across entry, exit, death, bankruptcy and re-entry, including the existing rule that the lifetime contribution envelope follows the taxpayer across closure events.
- The treatment of interest, inflation, prior-year contributions and any interaction with corporate levies must be specified.

A key design choice remains open: whether all stock-tax paid counts towards the envelope, or whether only a defined fraction does. Full inclusion is the clean baseline for testing; partial inclusion is a sensitivity, not an assumed improvement.

## 5. Why the combination might work

### 5.1 A broader and more stable revenue base

The WDT component taxes changes in wealth. The stock component taxes accumulated wealth above a high threshold, including in years when that wealth does not grow.

The two bases therefore respond differently to economic conditions. A stock charge could provide revenue in low-growth or stagnant-wealth years, while the delta component captures a larger share of the fiscal upside in strong-growth years.

This does not guarantee stability. A falling stock market, valuation changes, migration or avoidance could affect both bases. The degree of diversification between the revenue streams must be measured rather than assumed.

### 5.2 Lower stock rates may reduce the liquidity and political objection

A low rate applied only to a high-value excess stock could produce a materially smaller annual liability than a high-rate wealth tax with a lower threshold.

The relevant comparison is not simply the tax as a percentage of net worth. It is also the liability as a percentage of income, liquid assets, business cash flow and the value of the illiquid asset itself.

The proposal therefore does not assume that every taxpayer above the threshold can pay easily. It asks whether the combination of a high threshold and low rate makes severe liquidity problems sufficiently uncommon or manageable without broad exemptions.

### 5.3 A cooperative rather than purely extractive relationship

Including stock-tax payments in the lifetime contribution envelope gives the taxpayer a defined benefit in return for contributing during periods when their wealth may not be increasing.

This is consistent in principle with the WDT's cooperative architecture: the state collects contributions while accepting a bounded share of downside risk. It may strengthen the perceived reciprocity of the system.

The benefit must be described accurately. It is additional refund capacity, not a guaranteed repayment of stock tax and not an investment return.

## 6. Illustrative arithmetic, not proposed parameters

For a flat rate applied only to net wealth above a threshold:

`Annual stock charge = rate × max(0, net wealth − threshold)`

The following examples illustrate the scale of the liability at a hypothetical 0.1% rate. They do not imply that 0.1%, or any listed threshold, is an appropriate setting.

| Net wealth | Threshold | Taxable excess | Annual charge at 0.1% |
|---:|---:|---:|---:|
| £10m | £10m | £0 | £0 |
| £15m | £10m | £5m | £5,000 |
| £25m | £10m | £15m | £15,000 |
| £50m | £10m | £40m | £40,000 |
| £100m | £10m | £90m | £90,000 |
| £500m | £10m | £490m | £490,000 |

This table shows why the threshold and rate must be considered jointly. It does not establish that the charge is incidental: a £40,000 liability may be small relative to £50m of wealth, but could still be difficult to pay from the cash flow of a private business owner.

## 7. Fit with the WDT's existing principles and design

The proposal appears broadly compatible with the WDT's stated strategic and normative framework, but it is a substantive extension and must be assessed against the existing mechanism.

- **Individual as the tax subject:** the stock liability should attach to the individual beneficial owner, not treat a company or trust as a moral subject. Existing attribution and corporate-collection rules would need to be reconciled.
- **Cooperative architecture:** counting stock-tax contributions towards the lifetime envelope extends the existing reciprocal contribution principle. It should not create an unconditional or uncapped public insurance promise.
- **Tolerance of imperfect compliance:** a high-threshold stock base may be particularly exposed to valuation, entity-attribution, residency and wealth-fragmentation strategies. The proposal cannot assume that a low rate removes the incentive to avoid.
- **Symmetric downside protection:** the stock component must not silently weaken the existing symmetry between gains and qualifying losses. Its contribution to the lifetime envelope changes the scale of possible refunds and therefore the reserve requirement.
- **Tax replacement ambition:** the stock component is proposed as part of the replacement architecture, not as a permanent additional tax on top of all existing taxes. Its revenue must be evaluated net of the taxes WDT is intended to retire.

No settled WDT design position is amended by this hypothesis. In particular, the progressive delta schedule, the symmetric refund principle, the contribution-envelope cap and the Sovereign Wealth Fund architecture remain the baseline pending an explicit author decision.

## 8. Main risks and possible failure modes

1. **Revenue is smaller than expected.** A high threshold and low rate may leave too little taxable wealth to make a meaningful contribution to the fiscal requirement.
2. **The rate is not incidental for illiquid taxpayers.** A small percentage of wealth can still exceed available cash flow, especially where wealth is concentrated in a private company, land or other hard-to-sell assets.
3. **Avoidance shifts to the stock base.** Taxpayers may split ownership, use trusts or entities, alter residency, borrow against assets, or manipulate valuation and liabilities. The combined system could create more avoidance surfaces rather than fewer.
4. **The two components compound the burden.** A taxpayer may owe stock tax in addition to progressive WDT on annual gains. The combined effective burden, not either component in isolation, determines behavioural response.
5. **The refund envelope creates contingent liabilities.** Counting stock-tax payments as contributions can increase future refund capacity, potentially weakening the revenue advantage or increasing reserve needs.
6. **Revenue streams are not sufficiently independent.** A downturn can reduce WDT receipts, increase refunds and coincide with falling valuations or liquidity stress under the stock component.
7. **The threshold creates avoidance and boundary effects.** A separate high threshold may encourage wealth fragmentation or strategic valuation around the threshold. The threshold's unit (individual, household, beneficial ownership group) is a major design choice.
8. **Administrative cost outweighs yield.** Annual valuation and attribution of the top-tail base may consume a material share of receipts.
9. **Political acceptance is assumed rather than demonstrated.** Wealthy taxpayers may object to the principle, the interaction with WDT, or the perceived risk of future rate increases even where the initial liability is low.

## 9. Questions the hypothesis must answer

### Revenue and distribution
- What share of total household net wealth lies above candidate thresholds?
- How many taxpayers and how much wealth are covered at £5m, £10m, £20m and £50m (illustrative thresholds)?
- What is the gross and net revenue yield at 0.05%, 0.1%, 0.2% and 0.25% (illustrative rates)?
- How much does the stock component reduce the probability or severity of WDT fiscal shortfalls?
- Does it materially improve the ability to retire the taxes in the replacement package?

### Liquidity and incidence
- What is the annual charge as a share of income and liquid assets, by wealth band and asset composition?
- How many taxpayers would need to sell assets or borrow to pay?
- Are private-business owners, farmers, landowners and other illiquid-wealth groups disproportionately affected?
- Would deferral secured against the asset solve a genuine timing problem, or simply postpone and compound liabilities?

### Behaviour and administration
- How sensitive is the base to migration, entity restructuring, valuation understatement and debt allocation?
- Can existing WDT valuation routes and attribution rules administer the stock base without creating a second valuation system?
- What is the likely administrative cost per pound collected?
- How does the design treat couples, trusts, foundations, pensions, private companies, debt and non-resident beneficial owners?

### Refund-envelope interaction
- How much additional refund capacity is created by including stock-tax payments?
- How often would the expanded envelope bind, and how much additional refund would be paid?
- What happens to short- and long-reserve fill times and solvency?
- Should the envelope credit be full, fractional, or subject to a separate ceiling?
- Does the additional protection materially change taxpayer behaviour or political acceptance?

### Political economy
- Is a low-rate, high-threshold stock component more acceptable to wealthy taxpayers than a higher-rate stock tax?
- Does the refund-envelope link create a credible reciprocal bargain, or is it too remote and contingent to affect acceptance?
- Would the general public regard the combined system as a fairer and more reliable replacement tax?
- Can the government credibly commit not to increase the stock rate or lower the threshold opportunistically?

## 10. Suggested test design

The first test should be a transparent static revenue-and-incidence exercise, not an immediate change to the model-v3 architecture.

1. **Establish the stock base.** Estimate individual net wealth above several high thresholds, with a separately identified rich-list tail and clear treatment of debt and beneficial ownership.
2. **Calculate gross yield.** Sweep a small set of illustrative flat rates and thresholds. Report taxpayer count, taxable excess, gross receipts and concentration of receipts.
3. **Measure cash-flow burden.** Report the liability against income and liquid assets, split by wealth band and asset composition where evidence permits. Identify the illiquid tail rather than hiding it in an average.
4. **Overlay the WDT.** Add the stock liability to the existing WDT taxpayer paths and report combined annual and lifetime burdens, including loss years.
5. **Recalculate the contribution envelope.** Compare WDT-only contributions with WDT-plus-stock contributions. Measure the change in binding frequency, refund amounts and reserve requirements.
6. **Stress behaviour and fiscal conditions.** Test migration, valuation and avoidance responses, as well as poor-return sequences. Do not treat the static yield as a behavioural revenue forecast.
7. **Compare against alternatives.** Retain the existing equal-revenue stock-tax comparator, but add the combined system as a distinct candidate. Compare systems on equal-revenue welfare and liquidity measures as well as revenue stability.

Only after these tests should the author decide whether the stock component belongs in the canonical WDT design, whether it should be included in model v3, and whether it changes the replacement-tax schedule.

## 11. Relationship to current model-v3 work

The current model-v3 specification already includes a **stock wealth tax as a comparator** in the equal-revenue welfare comparison (M13 / OW1). That comparator answers a different question: how a stock wealth tax performs against WDT when each raises the same expected revenue.

It does not test a combined system in which a low-rate stock charge sits alongside progressive WDT, nor does it test stock-tax payments being counted towards the lifetime contribution envelope.

This hypothesis therefore must not be treated as already covered by OW1. It is a possible new policy schedule and a new interaction with the refund mechanism.

The current model-v3 work should not be silently expanded on the strength of this note. The first step is to establish whether the data can support a credible top-tail stock base and liquidity analysis, then decide whether the combined system merits a separate design and modelling brief.

## 12. Provisional conclusion

The combined design could address a real weakness in a pure wealth-delta tax: the absence of a direct charge on accumulated wealth in years when that wealth does not grow. A low-rate stock component above a high threshold may broaden and stabilise the revenue base while avoiding the most politically and economically difficult features of high-rate stock wealth taxes.

Its strongest distinctive feature is the proposed link to the lifetime contribution envelope. This could make the stock component part of the WDT's reciprocal risk-sharing architecture rather than a disconnected additional levy.

But the key claims remain unproven. The decisive tests are the revenue yield after behavioural response, the cash-flow burden on illiquid taxpayers, the additional contingent refund liability, and whether the combined system remains simpler and more robust than the alternatives.

**Working label:** stock-wealth floor hypothesis. This is a discussion label, not an approved paper title or shortcode.
