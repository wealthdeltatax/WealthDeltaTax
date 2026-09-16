Yes. I’ve read the current page rather than relying on our earlier discussion. My overall reaction is that **the paper has a genuinely interesting core, but it currently overstates what the model establishes in several places**. The strongest results are actually narrower than the rhetoric, and tightening that rhetoric would make the paper considerably harder to attack.

[WFR — Welfare Comparison Across Tax Systems at Revenue Equivalence](https://wealthdeltatax.org/wfr.html?utm_source=chatgpt.com)

## 1. The biggest issue: the paper sometimes turns a partial-equilibrium result into a welfare conclusion

The paper is commendably explicit that it does **not** model general equilibrium, behavioural responses to WDT, implementation costs, migration, etc. ([Wealth Delta Tax (WDT)][1])

But then the conclusion says:

> "the WDT cannot reasonably be dismissed without addressing the mechanisms this paper has identified and quantified."

and frames the comparison around whether Category 3 costs exceed the **141–143 bp** CGT lock-in result. ([Wealth Delta Tax (WDT)][1])

That's rhetorically stronger than the model warrants.

The 141 bp number isn't really "the welfare advantage of WDT" in a general sense. It is:

**the difference between two particular partial-equilibrium models under a particular portfolio-switching experiment, with a particular embedded gain, horizon, return distribution, tax rate, and utility function.**

That's still interesting. But the distinction matters enormously.

I'd change the conceptual framing from:

> WDT has established a ~143 bp welfare advantage over CGT

to something closer to:

> **Under the model's reference calibration, endogenous realisation behaviour introduces a 141–143 bp CEW cost relative to the accrual benchmark.**

Then separately:

> **The WDT eliminates this particular realisation-contingent wedge by construction.**

That is rock solid.

The reader can do the subtraction themselves.

---

# 2. The CGT lock-in result is probably the most vulnerable major section

This is where I'd expect a hostile public-finance referee to attack first.

The model takes:

* \(G/V=50\%\)
* \(T=5\) years
* \(r_A=10.45\%\)
* CGT = 24%
* \(\gamma=2\)

and gets 141 bp. ([Wealth Delta Tax (WDT)][1])

But the result is **extremely sensitive to the construction of the portfolio-choice experiment**.

The paper itself shows this:

| Assumption | Lock-in CEW cost |
| ---------- | ---------------: |
| T = 1      |            56 bp |
| T = 2      |            73 bp |
| T = 5      |           141 bp |
| T ≥ 8      |           181 bp |

([Wealth Delta Tax (WDT)][1])

That isn't a minor calibration sensitivity.

It tells the reader that the headline number is substantially determined by the artificial horizon structure.

And there's an even more important point.

### The model doesn't appear to have a realistic cross-sectional asset-choice distribution.

The paper compares one existing asset A against an alternative asset B and then evaluates whether the agent switches.

That's a useful mechanism demonstration.

But it isn't obviously equivalent to modelling an investor choosing an optimal portfolio from a realistic investment opportunity set.

The 90% "locked in" number looks particularly dangerous until you read the decomposition. The paper correctly admits that **86.7% of states aren't tax lock-in at all** because \(r_B<r_A\). ([Wealth Delta Tax (WDT)][1])

So:

> **90% locked in**

is potentially a very misleading headline.

Only **3.3 percentage points** of states at the reference calibration are actually in the CGT-induced distortion region.

You explain this later, but I'd go further and **stop calling 90% "P(agent locked in)" in the main narrative**.

Call it something like:

> \(P(\text{remain in A})\)

and separately:

> \(P(\text{CGT-induced non-switching})\)

That would prevent someone accusing the paper of inflating the lock-in result.

---

# 3. There is an odd contradiction in the long-horizon lock-in result

This is actually fascinating.

At \(T=8+\), the model says:

* \(r_B^*\) has fallen almost to \(r_A\)
* \(P(\text{CGT distortion})=0\%\)
* yet the welfare cost reaches **181.1 bp** and stays there. ([Wealth Delta Tax (WDT)][1])

You explain this as compounding of the foregone return advantage.

Mathematically, that may be fine.

But economically, it needs much more explanation.

A referee is going to ask:

**If there are no return states in which the agent is currently prevented from switching, what exactly is causing the 181 bp welfare loss?**

The answer seems to be that the *initial* switching decision creates a long-lived allocation error which compounds.

That's a perfectly interesting result.

But it means this isn't really a conventional "annual lock-in probability" result. It's an **initial portfolio misallocation propagated over a long horizon**.

I'd explicitly rename/reframe this:

> **Realisation-induced portfolio persistence**

rather than allowing the reader to interpret 181 bp as "CGT causes a huge annual lock-in distortion."

---

# 4. The WDT is getting a much easier behavioural treatment than CGT

You actually admit this in §2.4, which is good:

> CGT is examined at its idealised best in the baseline and realistic calibration later, while WDT remains idealised throughout. ([Wealth Delta Tax (WDT)][1])

But I think this needs to be **much more prominent**.

Because otherwise a reader gets:

**CGT**
→ endogenous realisation
→ portfolio misallocation
→ 143 bp cost

versus

**WDT**
→ symmetric refunds
→ no lock-in
→ perfect accrual implementation.

The comparison is therefore not:

> real-world CGT vs real-world WDT

It is:

> **CGT with one important behavioural distortion vs WDT with its implementation distortions deliberately excluded.**

The paper knows this. The reader needs to feel it.

Your Category 3 framework helps enormously, but the paper currently sometimes treats Category 3 as though it were merely an appendix qualification.

It isn't.

For WDT, these could be central welfare terms:

* valuation cost
* compliance cost
* avoidance
* migration
* liquidity constraints
* strategic loss generation
* administrative costs
* legal disputes
* asset restructuring

You acknowledge all of these. ([Wealth Delta Tax (WDT)][1])

I'd therefore describe WFR as:

> **a comparison of the identifiable tax-base and behavioural mechanisms, not a complete welfare comparison of implemented tax systems.**

That is less sexy, but academically much stronger.

---

# 5. The stock-wealth-tax / consumption-tax result is useful, but currently too easy to overread

The paper does a good job saying the equivalence depends on:

* no labour income
* proportional bases
* uniform saving
* no liquidity constraints
* CRRA preferences
* etc. ([Wealth Delta Tax (WDT)][1])

But then you present:

> 479× concentration

as a Category 1 finding about existing systems. ([Wealth Delta Tax (WDT)][1])

That's potentially misleading.

The **479× isn't an empirical prediction of actual wealth concentration under a consumption tax**.

It is:

> Fagereng's return heterogeneity + your assumed persistent 8pp return differential + your model's compounding mechanism + a 30-year horizon.

That's a legitimate simulation.

But the prose should repeatedly call it something like:

> **Fagereng-calibrated simulated concentration**

rather than simply:

> **stock wealth and consumption taxes produce 479-fold concentration**

because the latter sounds like an empirical claim.

---

# 6. The 30-year horizon is doing a *lot* of work

This is probably the biggest conceptual issue outside CGT.

The paper says:

> "the relevant axis at N=30 is accrual basis versus stock base."

([Wealth Delta Tax (WDT)][1])

That's fine.

But why **30 years**?

You explain that it corresponds to expected WDT membership after crossing \(W_{min}\). ([Wealth Delta Tax (WDT)][1])

That is a WDT-specific reason for choosing the horizon.

But then you use that horizon to make claims about the relative welfare properties of **other tax systems**.

That's potentially circular.

The stronger design would be:

**N = 1, 5, 10, 20, 30, 50, 73**

and show when the results diverge.

You've already discovered in our previous work that **the 30-year compounding horizon may be one of the main reasons the welfare differences become large**.

I think that should become a central figure.

Something like:

> **CEW difference vs horizon**

and separately:

> **Great/Poor wealth ratio vs horizon**

That would tell us whether WFR's conclusion is:

**"WDT is structurally better"**

or:

**"The difference becomes economically interesting once persistent return heterogeneity has had sufficient time to compound."**

The latter is a much more interesting finding.

---

# 7. Your "progressive WDT" result is actually weaker than the paper makes it sound

This is an important one.

The canonical progressive schedule is:

$$
\tau_0=15\%,\quad \tau_m=70\%,\quad k=.001,\quad W_{min}=£2m
$$

Yet at £10m the schedule is barely above the entry rate. ([Wealth Delta Tax (WDT)][1])

So the finding that:

> progressive WDT ≈ flat WDT

isn't really telling us much about progressive taxation.

You're effectively testing:

> **a nearly-flat WDT versus a flat WDT.**

And you explicitly show that the gap is almost zero at £10m. ([Wealth Delta Tax (WDT)][1])

This is actually an opportunity.

I'd separate:

### Result A

**Progression itself has little effect under the canonical calibration.**

### Result B

**This is because the canonical population lies below the inflection point of the logistic schedule.**

Then show a deliberate high-wealth sweep.

Otherwise someone can reasonably say:

> "You haven't demonstrated that progressive WDT has little welfare effect. You've demonstrated that your particular progressive schedule is almost flat over the wealth range being evaluated."

Which is true.

---

# 8. The distributional section contains an interesting tension that should be highlighted

This is one of the strongest parts of the paper.

You find:

* WDT Great/Poor tax incidence = **6.6×**
* income tax = **3.2×**
* stock wealth/consumption = **1.1×**. ([Wealth Delta Tax (WDT)][1])

And yet the WDT gives **lower welfare cost to the Poor tier** because of symmetric loss refunds. ([Wealth Delta Tax (WDT)][1])

That is genuinely interesting.

It gives you a potentially important distinction:

> **Progressivity of expected tax incidence ≠ progressivity of welfare incidence.**

The WDT can collect disproportionately from high-return/high-wealth people while simultaneously providing disproportionately valuable insurance to low-return people.

I think this deserves much more prominence.

It is arguably more interesting than some of the "WDT wins" language.

---

# 9. The lifetime refund envelope exposes a serious qualification to the symmetric-refund argument

This is probably the most important thing I found on the page.

You show:

> Poor entrant in the first year of a loss → no refund.

Because cumulative contribution = zero. ([Wealth Delta Tax (WDT)][1])

And you explicitly acknowledge:

> "the Arachi objection applies in full"

at this entry boundary. ([Wealth Delta Tax (WDT)][1])

That undermines the categorical wording earlier:

> "The WDT is therefore not subject to the Arachi objection as stated."

([Wealth Delta Tax (WDT)][1])

No.

The more accurate statement is:

> **The symmetric refund substantially changes the Arachi mechanism for established taxpayers, but the lifetime contribution envelope creates an entry-margin case in which the objection remains applicable.**

You actually demonstrate this yourself later.

I'd change this. A referee spotting the contradiction will trust the paper less even though the underlying model is fine.

---

# 10. "Lifetime contribution envelope eliminates SRR solvency risk by construction" is too strong

This:

> "eliminates SRR solvency risk by construction"

is followed two lines later by:

> "government must either pre-fund the SRR from non-WDT sources or provide an initial credit..."

([Wealth Delta Tax (WDT)][1])

That's not really "eliminates solvency risk."

It eliminates **long-run taxpayer-level actuarial exposure beyond cumulative contributions**.

But it does **not** eliminate:

* aggregate liquidity risk
* cohort-entry risk
* correlated loss-year risk
* political commitment risk
* initial capitalisation risk

You even say the latter yourself.

I'd replace "eliminates SRR solvency risk" with something like:

> **bounds taxpayer-level lifetime refund exposure, leaving an initial-cohort liquidity requirement.**

Much harder to attack.

---

# 11. The phrase "the WDT contracts consumption variance below every alternative system" should go

This is at §6.2/6.3. ([Wealth Delta Tax (WDT)][1])

That is much too broad.

Your model shows it relative to **the systems actually specified under the model's assumptions**.

It does not establish:

> WDT consumption variance < every possible alternative system.

That sentence is exactly the kind of thing a hostile referee circles in red.

Make it:

> **"contracts consumption variance relative to the alternative tax systems modelled here at revenue equivalence."**

Same argument. Much safer.

---

# 12. "The primary theoretical objection to accrual taxation ... is specifically addressed" is also too categorical

The paper itself recognises liquidity and entry issues.

Also, Arachi's objection isn't merely:

> "taxpayer has a loss and doesn't get a refund."

The deeper issue concerns **timing of taxation relative to consumption and liquidity**.

Symmetric refunds clearly address a major component of that problem.

But "specifically addressed" sounds like you've disproved the objection.

I'd say:

> **"the symmetric refund directly addresses the loss-year component of the Arachi objection."**

That's much more defensible.

---

# 13. The "burden of consideration" conclusion is clever but slightly advocacy-shaped

This sentence:

> "A dismissal of the WDT on welfare grounds would have to establish..."

followed by four things a critic would need to show... ([Wealth Delta Tax (WDT)][1])

is rhetorically effective, but academically it feels like you're prosecuting the opposing case.

You don't actually need it.

The stronger scientific conclusion is:

> **The model identifies several welfare mechanisms that favour accrual taxation under the stated assumptions, while leaving implementation costs and general-equilibrium effects unresolved. The quantitative importance of those unresolved effects determines whether the partial-equilibrium results survive in a full welfare comparison.**

That's much harder to accuse of motivated reasoning.

Ironically, it makes the actual findings look **more credible**, because you're not demanding that critics prove the WDT wrong.

---

# 14. One thing I really like: the paper is increasingly honest about what it doesn't know

This is probably the strongest improvement compared with the earlier versions we've discussed.

The Category 1 / 2 / 3 taxonomy is genuinely useful.

In particular:

> Category 1 = costs/mechanisms of existing systems
> Category 2 = structural properties of WDT
> Category 3 = unknown WDT implementation costs

is a good organisational device. ([Wealth Delta Tax (WDT)][1])

I'd keep that.

But I'd rename it slightly.

**Category 1: Modelled properties of incumbent systems**

rather than:

> "What We Know About Existing Systems"

because you don't actually know that CGT costs 141 bp in the real world.

You know your model produces 141 bp.

That's a small wording change with a large epistemological benefit.

---

# 15. The paper's actual strongest claims, in my view

If I strip away the rhetoric, I think the genuinely defensible contribution is roughly this:

### Finding 1 — Risk sharing

A flat WDT with fully symmetric refunds has the Domar-Musgrave risk-sharing property.

That is mathematically strong and doesn't depend much on calibration. ([Wealth Delta Tax (WDT)][1])

### Finding 2 — Realisation lock-in

An accrual tax does not create the same realisation-induced switching wedge as CGT.

That's basically structural.

### Finding 3 — Persistent heterogeneous returns

If Fagereng-style return heterogeneity persists, taxing **return/delta rather than wealth stock** attenuates the compounding of return differences.

That's interesting and potentially quite important.

### Finding 4 — Distributional mechanism

The delta base produces substantially more progressive **tax incidence** than income tax in your heterogeneous-return experiment, while symmetric refunds provide insurance to low-return taxpayers. ([Wealth Delta Tax (WDT)][1])

### Finding 5 — Stock-base equivalence

Under your stripped-down model, stock wealth taxation and consumption taxation become mathematically equivalent.

That is a useful replication/extension result, though not a general real-world equivalence.

### Finding 6 — The big one

The welfare differences between systems are **not primarily coming from the headline tax rate**.

They emerge from:

> **what the tax base makes the taxpayer do.**

That's arguably the central intellectual contribution of WFR.

---

# 16. What I would change before doing anything else

I wouldn't add more literature yet.

I'd do a **claim-strength audit**.

I'd go through every sentence containing:

* "establishes"
* "shows"
* "proves"
* "eliminates"
* "superior"
* "advantage"
* "welfare cost"
* "structural"
* "by construction"
* "cannot"
* "every"
* "large"
* "real-world"
* "empirical"
* "plausible"

and classify it:

**A. Mathematical result of the model**

**B. Result conditional on calibration**

**C. Empirical fact imported from literature**

**D. Interpretation of the model**

**E. Claim about the real world**

I suspect we'll find that quite a few currently labelled A/D are actually B/E.

That is the biggest weakness I see.

---

## And there is one deeper issue I'd investigate next

The paper currently has **three different things mixed together**:

1. **tax-system efficiency**
2. **distributional consequences**
3. **long-run wealth concentration**

Those aren't the same welfare object.

The 479× → 286× result is interesting, but it isn't automatically a welfare gain. Likewise, a 6.6:1 incidence ratio isn't automatically better or worse than 3.2:1.

The paper occasionally slides between:

> lower concentration

and

> higher welfare

without explicitly making the social-welfare bridge.

That's where I'd be particularly careful, especially given that the paper's stated welfare metric is individual CEW rather than a social welfare function.

And this matters because the public-finance literature explicitly treats **efficiency and distribution as separate components of normative analysis**; the literature around Kaplow, Boadway, etc. is much more careful about that distinction. ([Annual Reviews][2])

---

### My assessment at this stage

**The underlying paper is stronger than the current prose makes it.**

The simulations contain several genuinely interesting results. But the prose periodically turns:

> "Under this model, this mechanism produces X"

into:

> "therefore WDT has established a welfare advantage."

I'd pull those back.

In particular, I'd attack **§4.2 (CGT lock-in), §4.3 (Fagereng concentration), §6.1–6.3 (the conclusions)** first. Those are where the strongest claims are and where a skeptical economist is most likely to push.

And I would **not** weaken the actual numerical results merely because they're favourable to WDT. The better move is to make absolutely explicit **what each number is a number of**. The 141 bp, 479×, 286×, 6.6:1 etc. can stay if the paper stops letting the reader mistake them for empirical welfare estimates.

[1]: https://wealthdeltatax.org/wfr.html "The Wealth Delta Tax: Welfare Comparison Across Tax Systems at Revenue Equivalence – Wealth Delta Tax (WDT)"
[2]: https://www.annualreviews.org/content/journals/10.1146/annurev-lawsocsci-101518-043037?utm_source=chatgpt.com "The Law and Economics of Redistribution | Annual Reviews"
