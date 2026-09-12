# WFR — Comprehensive Paper Plan v1
*Prepared: 2026-09-11. Supersedes the narrative structure in planning backbone v3 §7.*
*Integrates: backbone v3 model findings; structural replanning from session; three-category epistemic framework.*

---

## 0. What this document is

This is the full planning architecture for the WFR paper — not a draft, but a complete specification of what every section argues, what numbers it uses, what the referee risks are, and how the paper's conclusion follows from its structure. It is the document from which drafting begins.

The paper plan has two layers. The **argument layer** describes what the paper is trying to establish and why the sections are ordered as they are. The **content layer** describes what each section actually contains — specific numbers, specific literature, specific framing choices. Both layers are needed before drafting starts.

---

## 1. The paper's governing question and conclusion

### 1.1 The governing question

Most comparisons of tax systems do not hold revenue constant across systems, do not model the mechanisms through which each system generates welfare costs, and do not test all candidate instruments against the same empirical return distribution. This paper does all three. The question it answers is:

**When tax systems are compared on welfare grounds, at revenue equivalence, with their structural welfare mechanisms admitted, what do we find?**

### 1.2 The conclusion the paper must reach

> Once tax systems are compared on their welfare consequences rather than merely their administrative familiarity, WDT cannot reasonably be dismissed without addressing the welfare mechanisms identified here.

This conclusion does not assert that WDT is the optimal tax system. It does not assert that WDT has no costs. It asserts that the welfare mechanisms this paper identifies — and which no prior paper has tested simultaneously — shift the burden of justification. A decision to maintain CGT or a stock wealth tax as the default, after this analysis, is a decision to accept known welfare costs without demonstrating that the prospective costs of an alternative exceed them. The paper establishes that this comparison has not previously been made, and that making it produces results that cannot be set aside by appeal to administrative familiarity alone.

### 1.3 The epistemic architecture

The paper's argument rests on a three-category taxonomy that must be stated clearly in the methodology section and carried through to the conclusion. This taxonomy is what makes the conclusion defensible against the hostile referee's standard line ("you haven't shown WDT has no costs"):

**Category 1 — Known costs of existing systems, established by this paper**
These are welfare costs of CGT, income tax, stock wealth tax, and consumption tax that the model demonstrates under controlled conditions. They do not require WDT to exist. A referee cannot object that they await implementation data, because they are findings about systems that already operate.

**Category 2 — WDT welfare properties established without implementation data**
These are positive properties of the WDT that follow from the design of the delta base and the symmetric refund. They are theoretical results, not empirical observations of a running system, but they are not contingent on implementation choices. The D-M property, the structural absence of realisation lock-in, and the lifetime contribution envelope's solvency guarantee are all Category 2.

**Category 3 — WDT prospective costs, real but not currently quantifiable**
These are genuine costs that WDT may introduce, which cannot be measured without implementation data. Valuation friction under Route D, compliance cost at scale, administrative learning dynamics, novel avoidance strategies specific to the symmetric refund. The paper names them. It does not pretend they are zero. It notes that EVAL's break-even analysis is the tool for determining whether any of them plausibly exceed the Category 1 welfare costs the paper has measured.

The conclusion then follows from these three categories together: the Category 1 costs of existing systems are large and structural; the Category 2 properties of WDT eliminate or substantially alter several of those costs; the Category 3 costs of WDT are real but their magnitude is unknown and is the subject of EVAL. The question is not "is WDT costless?" — it is not. The question is "are the Category 3 costs plausibly larger than the Category 1 costs WDT removes?" That is what cannot be answered by appeal to administrative familiarity.

---

## 2. What the paper is not doing

State this near the front and do not retreat from it.

WFR is a Level 1 paper. It establishes the theoretical welfare case under controlled conditions, identifies the structural channels through which the delta base differs from existing instruments, and positions those channels in the active theoretical debate. It does not:

- Calibrate behavioural responses to the WDT
- Close the general equilibrium
- Produce a quantitative ex-ante welfare estimate under empirically estimated parameters
- Claim that WDT implementation costs are small
- Adjudicate the Guvenen vs Boadway/Spiritus dispute about stock wealth tax vs capital-income tax

Each of these is handled by a companion paper. The paper's argument is stronger for being precise about this boundary, not weaker. A Level 1 paper that stays within its level and reaches a defensible Level 1 conclusion is more valuable than one that overreaches and invites a referee to dismiss the whole contribution.

The companion paper EVAL (provisionally scoped, not yet written) is the Level 2 analysis. It will use empirically calibrated behavioural parameters, without requiring WDT implementation data, to produce break-even thresholds for each Category 3 cost. WFR identifies the welfare advantage EVAL will use as its starting point. The two papers are complementary, not competing.

---

## 3. Literature gaps this paper closes

WFR closes three confirmed gaps from LR.A §2:

**Gap #1** — No prior paper formally extends the Domar-Musgrave framework to a progressive delta base and quantifies the three complications this introduces (progression itself, leverage effects on the net wealth base, and intertemporal rate asymmetry under a logistic rate schedule).

**Gap #2** — No prior welfare comparison includes the delta base alongside the standard candidates (income tax, CGT, stock wealth tax, consumption tax) tested against the same empirical return distribution at revenue equivalence.

**Gap #3** — No prior paper works through the distributional arithmetic of delta-base concentration under persistent return heterogeneity in the Fagereng sense — where returns differ persistently across the wealth distribution and these differences compound into concentration over a multi-decade horizon.

No prior paper closes all three simultaneously. This matters not because simultaneous closure is impressive, but because the three gaps interact: the D-M extension (Gap #1) establishes the risk-sharing mechanism; the welfare comparison (Gap #2) establishes that the mechanism translates into welfare advantage once distortions are admitted; the concentration result (Gap #3) establishes that the same mechanism has distributional implications that extend beyond the single-agent frame. A paper that closed only one or two gaps would miss the interaction.

---

## 4. Paper structure — overview

The paper has four parts plus front and back matter. The parts are not just organisational divisions; each part has a distinct argumentative job that the next part depends on.

| Part | Title | Job |
|---|---|---|
| — | Front matter and methodology | Establish the comparison design; introduce the three-category framework; name what is suppressed in the baseline and why |
| I | The controlled baseline | Show that no system dominates when distortions are suppressed — the fair starting point |
| II | The mechanisms | Show that each competitor system carries a structural welfare cost that only emerges once the corresponding mechanism is admitted — the core of the paper |
| III | Literature positioning | Show that the delta instrument has not previously been tested in this comparison, and that adding it does not adjudicate an existing dispute but fills a gap |
| IV | Synthesis and conclusion | Bring the three-category framework to bear; state what the paper has established and what it has not; reach the burden-of-consideration conclusion |

---

## 5. Front matter and methodology

### 5.1 Abstract

The abstract must do four things: state the comparison design, state the three main findings (D-M result, lock-in cost, concentration result), identify the three literature gaps the paper closes, and state the conclusion. It should not assert WDT optimality.

Draft structure (not final language):

> We compare five tax systems — symmetric WDT, progressive WDT, income tax, CGT, stock wealth tax, and consumption tax — at revenue equivalence, against a common empirical return distribution, using certainty-equivalent welfare as the criterion. The comparison proceeds in controlled stages, admitting one welfare mechanism at a time. In the controlled baseline, WDT leads by 17.4 basis points — a small advantage that establishes fair ground, not a knockout. As mechanisms are admitted, the welfare differences become large: CGT's realisation lock-in imposes a 142.96 basis-point welfare cost once portfolio choice is endogenous; stock-wealth-tax and consumption-tax systems allow persistent return heterogeneity to compound into 479-fold concentration at the 30-year horizon versus 286–288-fold for WDT variants. The paper closes three confirmed literature gaps and introduces the delta instrument into a comparison that existing literature has conducted only across income and stock wealth tax bases. The conclusion is not that WDT is the optimal tax system. It is that WDT cannot be dismissed on welfare grounds without addressing the mechanisms this paper has measured.

### 5.2 Introduction

The introduction has three jobs: establish the comparison problem, state the paper's contribution relative to the existing literature, and introduce the three-category epistemic framework.

**The comparison problem (first two paragraphs).**
Most tax system comparisons do one of two things: compare systems at different revenue levels, which confounds the welfare comparison with the revenue level; or suppress all behavioural mechanisms to produce a clean base comparison that says nothing about real-world welfare. This paper does neither. Revenue equivalence is genuine — numerical solve for E[T] = 2% of W₀ across all systems. Mechanisms are admitted one at a time, not suppressed throughout. The result is a comparison that is both fair (same revenue burden) and informative (mechanisms visible).

**Contribution statement.**
Three literature gaps are closed simultaneously. State the gaps from §3 above. Note that the key differentiating feature is the simultaneous closure — the interaction between D-M (risk mechanism), welfare comparison (welfare translation), and concentration (distributional consequence) is only visible when all three are in the same model.

**Three-category framework.**
Introduce the taxonomy here, not in the conclusion. The reader needs to know from the start that the paper is making three epistemically distinct kinds of claims. Category 1 claims are about existing systems. Category 2 claims are theoretical properties of the WDT. Category 3 claims are prospective costs that the paper names but does not quantify — and explains why. This framing pre-empts the hostile referee's standard objection before the results section.

**Forward pointers.**
LR.A §2.1–2.3 for the three gaps. EVAL as the Level 2 companion for the break-even analysis. BEHAV, VAL, and CLOSE for the companion papers that address the Category 3 costs.

### 5.3 Methodology

This section is short but load-bearing. Its job is to explain the comparison design and to name the comparable-treatment exposures before a referee discovers them.

**Revenue equivalence.** E[T] = 2% of W₀, solved numerically for each system. Rates differ across systems; the revenue burden does not. A table of the resulting rate parameters across systems and distributions (Ver. A and Ver. B) belongs here.

**Welfare criterion.** Certainty-equivalent welfare (CEW) against a common no-tax benchmark for all systems. Rankings are relative to the same reference point, not to each other directly.

**Return distributions.** Ver. A: 73-observation empirical sequence (1950–2022 UK data). Ver. B: idealised two-state distribution. Both used throughout. Results are reported for Ver. A as primary, Ver. B as robustness check. Note the rate differential implication for income tax (32.067% Ver. A vs 33.404% Ver. B) and explain it: the empirical distribution includes genuinely negative return years where income tax collects nothing but WDT provides refunds, requiring a lower rate to hit the same revenue target. The idealised distribution misses this, which means Ver. B understates the WDT's revenue-equivalence rate advantage.

**What the baseline suppresses — and why.** The baseline suppresses behavioural responses, lock-in, portfolio choice, return heterogeneity, and agent heterogeneity. These suppressions are intentional. They are there to isolate what the tax base itself contributes to welfare before the mechanisms that make the real comparison interesting. Each mechanism is admitted in Part II in a controlled sequence. This design — suppress first, admit one at a time — is what allows the paper to attribute welfare differences to specific mechanisms rather than to a bundle.

**Comparable-treatment exposures.** Name all three before the results, not in a response to the referee. (i) CGT is modelled without lock-in in the baseline, then with lock-in in Part II §3. The sequencing is methodologically correct — it isolates the base comparison before introducing the dominant CGT distortion — but the asymmetry is real: CGT degrades as realism increases while WDT is held at its idealised best throughout. The companion papers (VAL, BEHAV, CLOSE) address the WDT-specific practical objections the model abstracts away from. (ii) The concentration comparison uses aggregate revenue equivalence, not tier-specific equivalence. This is the correct implementation of revenue neutrality in a heterogeneous population, but it produces substantially different effective burdens at the tier level: the Poor tier under symmetric WDT pays 0.34% of W₀ against the Great tier's 2.21%. The tier-level incidence figures are in WFR.A §D.2 for any reader who wants to inspect the effective burden distribution. (iii) Income tax and CGT are identical in the baseline by construction — single period, all gains realised each period. This does not settle the real-world income tax vs CGT comparison that practitioners care about; it establishes a baseline in which the lock-in distortion is suppressed, so that when it is admitted in Part II §3 its isolated welfare cost is visible.

**N = 30.** The canonical horizon is 30 years, consistent with VAL, RATES, and SWEEPS. Chart titles and print labels in module4 that say "73 years" are stale annotation errors that must be corrected before the charts are used in the paper or the code is shared.

---

## 6. Part I — The Controlled Baseline

### Argumentative job of Part I

Part I makes a single argument across two sections: when distortions are suppressed, no tax system produces dramatically different welfare outcomes. The WDT has a small advantage (17.4 bp) but nothing that constitutes a knockout. This concession is the paper's most important strategic move. It establishes that WDT is not winning because it imposes a lighter revenue burden or because the baseline is tilted. Everything that follows in Part II is therefore attributable to mechanisms, not to a rigged comparison.

The end of Part I leaves the reader with a specific question: if mechanical welfare differences are small when distortions are suppressed, where does the actual welfare cost of existing systems come from?

### §1 — Revenue equivalence and the single-agent baseline

**Content.**

Present the five-system CEW comparison at γ=2, Ver. A:

| System | CEW |
|---|---:|
| Symmetric WDT | −1.7539% |
| Income Tax | −1.7713% |
| CGT | −1.7713% |
| Stock Wealth Tax | −1.8870% |
| Consumption Tax | −1.8870% |

State the WDT advantage plainly: 17.4 bp over income tax/CGT; 133.1 bp over stock wealth/consumption. Neither is a large efficiency claim.

Two structural observations require explanation because they will appear again in Part II. (a) Stock wealth tax and consumption tax cluster at exactly −1.8870% across all γ values — γ-invariance. Explain why: both systems apply a fixed proportional wedge leaving the relative consumption distribution unchanged, so CRRA scale-invariance makes risk aversion irrelevant. This is correct and diagnostic. (b) Income tax = CGT throughout the baseline — correct by construction. The lock-in separation is endogenous and enters only in Part II §3.

**What this section must not do.** Do not claim the 17.4 bp advantage is the paper's conclusion. Do not suggest the baseline comparison resolves anything. The baseline's job is to establish fair ground. State this explicitly: the small baseline advantage establishes that the WDT does not win through a mechanical rate advantage. The mechanisms examined in Part II are therefore the source of the real welfare differences.

### §2 — The D-M risk-sharing property: mechanism established, verdict deferred

**Content.**

Flat-rate symmetric WDT satisfies Domar-Musgrave to floating-point precision across all γ and both distributions (gap ≈ 10⁻¹⁶ to 10⁻¹⁷). State what D-M means precisely in this context: the government participates proportionally in both gains and losses, contracting the agent's net return distribution without altering relative risk rankings. The consumption variance result (WFR.A §A.2) confirms the mechanism: WDT Var(C) = 0.0013, versus income/CGT 0.0014, versus stock wealth/consumption 0.0027.

Then state clearly what D-M does *not* mean — this is the single most important discipline point in the paper. D-M is a risk-sharing result, not a welfare-superiority result. It identifies the channel through which WDT can reduce welfare-relevant consumption variance without creating the conventional risk-taking distortion. Whether that channel translates into welfare superiority depends on what else is true about the economy and about the taxpayer's situation. The welfare translation is the subject of Part II. The mechanism is established here; the verdict is deferred.

**Why this section must hold the welfare verdict back.**
If the D-M result is presented as a welfare argument rather than a mechanism, the paper commits the error Arachi et al. (2022) expose: treating accrual taxation as automatically welfare superior to realisation taxation because of its variance properties, without accounting for the intertemporal consumption distortion that accrual creates. The WDT's answer to Arachi is the symmetric refund, but that answer belongs in Part II §3, not here. Sequencing matters.

---

## 7. Part II — The Mechanisms

### Argumentative job of Part II

Part II is the core of the paper. It has four sections, each following the same pattern: (1) name the mechanism and explain why it is structural to the relevant tax base, not an artefact of this model; (2) quantify its welfare consequence; (3) show that WDT avoids it — or substantially attenuates it — by design. The four mechanisms together build a cumulative picture: every competitor system carries a structural cost that only emerges once the corresponding mechanism is admitted. Not all of these are Category 1 findings (costs of existing systems); some are Category 2 (WDT properties). The distinction should be maintained explicitly.

### §3 — Progressive rates: three complications, all second-order

**Content.**

Introduce the three D-M complications under a progressive rate schedule. State at the outset that all three are real — they are genuine features of the progressive logistic schedule, not model artefacts — and that all three are second-order at canonical parameters across the tested population.

**C1 (progression itself, WFR.A §B.1).** Gap is −0.00 bp at £10m. Correct: at W₀ = 5 × W_min, the logistic is nearly flat at τ₀, so progressive ≈ flat. The WFR.A §E.3.1–§E.3.4 sweep confirms the gap remains sub-0.05 bp even at £100m. State cleanly: C1 is a second-order effect throughout the tested population with canonical rate parameters. Running the logistic at much higher wealth levels would widen the gap — note this as a sensitivity that would matter at the far right tail of the wealth distribution, outside the canonical population.

**C2 (leverage / NW base, WFR.A §B.2).** Gap rises from 0.00 bp at 0% leverage to +1.10 bp at 70% leverage — real, monotone, direction confirmed. The mechanism: as debt rises, W₀ falls in NW terms, reducing the absolute tax burden relative to the asset-return comparator. The NW base produces marginally better welfare at all leverage ratios. State the magnitude honestly: 1.10 bp at extreme leverage (70%) is second-order relative to the mechanisms in §4–§6. C2 is a genuine complication that deserves acknowledgment; it is not a dominant result.

**C3 (intertemporal rate asymmetry, WFR.A §B.3).** The asymmetry column (τ_gain − τ_refund) ranges from +0.0011 pp at £3m to +0.0946 pp at £200m. The Excess column is consistently negative — progressive WDT collects less net tax than flat in the gain-then-loss sequence. Explain the mechanism precisely: the wealth levels tested sit in the near-flat region of the logistic, where progressive effective rates are below the flat benchmark rate (~33%). The gain-at-higher-rate effect materialises only well above the logistic inflection point. C3 exists, is measurable, and is minor relative to what follows. The counterintuitive negative Excess result requires explicit prose explanation because it is not what a reader familiar with progressive tax bracket asymmetry would expect.

**Section close.** The progressive rate schedule introduces three real but second-order complications that do not materially undermine the D-M risk-sharing architecture established in §2. The paper can proceed to the mechanisms that do matter.

### §4 — CGT lock-in: the dominant welfare result

**Content.**

This is the paper's central finding and must be its longest mechanism section. The structure is: (a) introduce the endogenous realisation decision; (b) quantify the welfare cost of CGT lock-in; (c) address the Arachi objection as the structural pivot; (d) state the Category 1 finding clearly.

**(a) The endogenous realisation decision.**
CGT without endogenous portfolio choice is structurally identical to income tax in the model — the baseline confirms this. Now allow the taxpayer to make the decision an actual taxpayer makes: given that asset B has a higher expected return than asset A, and given that switching from A to B triggers a CGT liability, should I switch? The CGT creates a wedge between the gross return differential (r_B − r_A) and the after-tax return from switching (r_B − τ_cgt × G − r_A). Where G/V is large enough or T short enough, the taxpayer stays in A despite its inferior return. This is lock-in. It is not a decision error; it is the rational response to the tax schedule.

**(b) The lock-in welfare cost (WFR.A §C.1–§C.3).**

Full comparison table (WFR.A §C.3):

| Metric | Ver. A (Empirical) | Ver. B (Idealised) |
|---|---:|---:|
| WDT CEW | −1.7539% | −1.7525% |
| CGT CEW (no lock-in) | −1.7713% | −1.7525% |
| Lock-in welfare cost | +141.22 bp | +41.19 bp |
| CGT CEW (with lock-in) | −3.1834% | −2.1644% |
| WDT advantage (no lock-in) | +1.74 bp | +0.00 bp |
| WDT advantage (with lock-in) | +142.96 bp | +41.19 bp |

The WDT advantage grows from 1.74 bp to 142.96 bp once lock-in is admitted at G/V=50%, T=5, Ver. A, γ=2. That is approximately 82 times the baseline advantage.

Present the sweep results to show robustness:
- G/V sweep (WFR.A §C.1): lock-in cost rises from +16.4 bp at G/V=5% to +162.2 bp at G/V=76.6%, then non-monotone above 81%. The non-monotonicity is a discretisation artefact of boundary effects in P(locked in) as r_B* approaches distribution limits — worth a footnote, not a model error.
- P decomposition (WFR.A §C.1): At G/V = 5–31.8%, P(CGT distortion) = 0.0% — all lock-in is fundamental preference (r_B < r_A), not CGT-induced. The CGT distortion proper begins only above G/V = 36.3%. At the G/V = 50% reference, P(CGT distortion) = 3.3%. The paper must be precise: the high P(locked in) at low G/V reflects market return states below r_A, not CGT-induced lock-in. Failing to make this distinction would invite the referee to argue the paper conflates market risk with tax distortion.
- T sweep (WFR.A §C.2): Lock-in cost rises from +56.1 bp at T=1 to a plateau of +181.1 bp at T≥8. Direction upward, mechanism: r_B* converges toward r_A as T→∞ (indifference return converges) while welfare cost rises (more compounding periods of foregone superior return).

**Calibration note.** The 142.96 bp figure is the model's result at the stated calibration (G/V=50%, T=5, τ_cgt=24%, r_A=10.45%, γ=2, empirical distribution). It is not an estimate of the general welfare cost of CGT lock-in. The paper presents it as: "in this model calibrated to UK parameters, the welfare cost of the lock-in distortion is 141 bp." The mechanism is very strongly supported by the literature; the magnitude is the model's contribution and is not externally validated. Framing discipline is required throughout this section.

**(c) The Arachi pivot — the paper's structural hinge.**

Arachi et al. (2022, *Fiscal Studies*) establish that accrual taxation is not automatically welfare superior to realisation taxation. Their argument: accrual taxes bill unrealised gains before the taxpayer has liquidity to pay without adjusting consumption. This creates an intertemporal consumption distortion in loss years — the taxpayer who has seen wealth fall still faces a tax assessment, cannot pay without consuming, and therefore makes an intertemporal consumption decision the tax has forced. This is the strongest available theoretical counterargument to any accrual-based tax, and it must be addressed directly, not cited in passing.

The WDT's answer is the symmetric refund. In loss years, the WDT provides a refund proportional to the loss. The refund restores consumption capacity at exactly the moment wealth has fallen and consumption pressure is highest. This is not a side property of the design — it is the mechanism the cooperative architecture calls "proportional co-investment" (WP §1). The government does not merely levy less tax in a bad year; it actively transfers purchasing power back to the taxpayer at the moment the Arachi distortion would otherwise be most severe.

The WDT is therefore not simply an accrual tax. It is an accrual tax that structurally addresses the principal welfare objection to accrual taxation. Arachi et al.'s critique applies to accrual taxes without symmetric refunds — income tax on unrealised gains, for instance, or an accrual wealth tax that does not offset losses. It does not apply to the WDT's specific architecture. This distinction must be stated explicitly, not left implicit in the model mechanics.

**(d) Category classification.**
The lock-in welfare cost (141–143 bp at canonical calibration) is a Category 1 finding: a welfare cost of an existing system (CGT with endogenous realisation), established without requiring WDT implementation data. The WDT's structural elimination of lock-in is a Category 2 property: it follows from the tax base not making the switching decision tax-relevant. Whether WDT introduces its own intertemporal distortions through implementation friction, valuation error, or compliance complexity is a Category 3 question — named here, not dismissed, addressed in EVAL and the companion papers.

### §5 — Heterogeneous returns: what the Fagereng premise does to concentration

**Content.**

This section introduces agent heterogeneity and asks what happens to concentration when persistently different returns interact with different tax bases over 30 years.

**(a) The Fagereng premise.**
Fagereng et al. (2020, *Econometrica*) establish substantial, persistent return heterogeneity that is positively correlated with wealth level. The 10th-to-90th percentile gap in average returns is approximately 18pp. WFR uses a four-tier calibration (Poor, Ok, Good, Great) with a return differential of approximately 8pp between the outer tiers. This is conservative relative to Fagereng's full distribution — the paper should note this as a lower bound on the concentration effects.

**(b) The concentration result (WFR.A §D.3).**

N=30 concentration paths:

| System | Initial | 2004 | 2009 | 2019 | 2029 |
|---|---:|---:|---:|---:|---:|
| Progressive WDT | 48.8× | 66.1× | 90.3× | 162.3× | 288.1× |
| Symmetric WDT | 48.8× | 65.1× | 87.4× | 157.2× | 286.3× |
| Income Tax | 48.8× | 65.5× | 90.2× | 166.1× | 320.2× |
| Stock Wealth Tax | 48.8× | 70.5× | 103.3× | 220.1× | 479.0× |
| Consumption Tax | 48.8× | 70.5× | 103.3× | 220.1× | 479.0× |

The key finding must be stated precisely: at N=30, the distinguishing axis is accrual basis vs stock base, not flat vs progressive rate. Both WDT variants reach approximately 286–288×; both income-tax-family systems reach 320×; both stock-base systems reach 479×. The relevant split is two-way (accrual vs stock), not three-way.

State the honest implication: the progressive vs flat WDT distinction on concentration is not visible at the canonical 30-year horizon. The Fagereng return differential (+8pp between Poor and Great) dominates the progressive vs flat rate differential over 30 years. The logistic schedule at canonical parameters has not risen far enough above τ₀ to compound a meaningful difference. This is an honest finding — it reduces the paper's advocacy character and makes the result more defensible.

The 479× figure for stock wealth and consumption tax is the most policy-relevant number in the section. It is the consequence of taxing the stock regardless of performance: a low-return taxpayer pays the same proportional tax as a high-return taxpayer on the same wealth, so no mechanism dampens the differential compounding of returns. This should be stated not just as a number but as a mechanism.

**Optional N=73 sensitivity.** A 73-year run would show whether the progressive WDT advantage over flat WDT on concentration emerges at longer horizons. This is useful context if the stale "73 years" print labels are being corrected anyway. If included, it goes in WFR.A as an appendix sensitivity, not in the main paper as a primary result. Decision: run or note the horizon limitation in prose. The paper should acknowledge explicitly that the progressive advantage on concentration requires a longer horizon to compound — this is a genuine scope limitation, not a suppressed finding.

**(c) Within-tier welfare (WFR.A §D.1).**

CEW by tier:

| System | Poor | Ok | Good | Great |
|---|---:|---:|---:|---:|
| Symmetric WDT | −0.2194% | −0.7816% | −1.4211% | −1.9269% |
| Income Tax | −0.6000% | −0.9274% | −1.4413% | −1.9161% |
| Stock Wealth Tax | −1.8424% | −1.8424% | −1.8424% | −1.8424% |
| Progressive WDT | −0.1375% | −0.5004% | −0.9223% | −1.3814% |

The Poor-tier finding is the sharpest within-tier result: symmetric WDT gives −0.2194% versus income tax's −0.6000%. The mechanism is the symmetric refund: the Poor tier spends more time in loss states (the −4.55pp return differential means frequent negative-return years), so the WDT's proportional refund in loss years delivers a disproportionate welfare benefit to this tier. Income tax collects nothing in loss years but also provides nothing; the asymmetry is income tax's structural property, not a failure of calibration.

Progressive WDT provides better CEW than symmetric WDT for every tier below Great. For the Great tier, progressive WDT (−1.3814%) is better than symmetric WDT (−1.9269%) — the redistribution mechanism is working. Both WDT variants dominate income tax at the Poor tier by a substantial margin.

**(d) Incidence (WFR.A §D.2).**
Symmetric WDT has a Great/Poor incidence ratio of 2.2071% / 0.3362% = 6.6:1. Income tax is 2.1903% / 0.6779% = 3.2:1. Stock wealth tax is effectively flat (2.0163% / 1.8689% = 1.08:1). The WDT's accrual basis makes it more progressive in incidence than income tax because the base (net return × W₀) scales with both wealth and the return differential, whereas income tax scales with gains only.

Note on the concentration comparison design: aggregate revenue equivalence is the correct implementation of revenue neutrality in a heterogeneous population, but it produces substantially different effective burdens at the tier level. This must be stated in the text, not left for a referee to discover.

**(e) The envelope binding result (WFR.A §D.4).**
The Poor tier's lifetime contribution envelope binds in 2001 with min slack = £0.0000m. This is the correct mechanic: the Poor tier's −4.55pp return differential produces a loss in the first scenario year before any cumulative tax has been paid. When the envelope floor binds, no refund is issued — the lifetime contribution envelope caps refunds at cumulative taxes paid to date. A taxpayer who has paid nothing receives nothing.

State the policy implication clearly: the lifetime contribution envelope eliminates SRR solvency risk by construction. Refund obligations can never exceed cumulative receipts from that taxpayer. The SRR's capitalisation requirement is a liquidity timing question — covering the gap between when refunds are paid out and when the next collection cycle settles — not a structural funding shortfall. This is a Category 2 property. Connect to the Arachi objection: the envelope is not a limitation on the symmetric refund's welfare properties, it is the mechanism that prevents the refund commitment from becoming an open-ended state liability.

**(f) The off-diagonal cell (WFR.A §D.5).**
Corner B Symmetric WDT shows "—" in the spot-check table. Add a table footnote: at Great W₀ (£139.6m) with Poor return differential (−4.55pp), the symmetric WDT generates large expected refunds that prevent the aggregate revenue target from being reached within τ ∈ (0, 0.999]. This is a solver boundary condition, not a model failure. The cell is undefined because the parameter combination is outside the feasible rate space.

### §6 — Stock wealth and consumption taxes: equivalence and concentration

**Content.**

This section is shorter than §4 and §5 because both main findings — welfare equivalence with each other, and concentration path — are already introduced in §§1 and 5. The section's job is to explain the equivalence, note where it breaks, and draw the concentration consequence explicitly as a Category 1 finding.

**The equivalence.** Both systems hit exactly −1.8870% CEW at γ=2, and both reach 479× at N=30. The γ-invariance explains the welfare result: a fixed proportional wedge on stock or consumption leaves the relative consumption distribution unchanged, so CRRA scale-invariance makes γ irrelevant. The N=30 equivalence reflects the same mechanism: both systems tax the stock without conditioning on return performance, so the Fagereng differential compounds at the same rate under both.

**Where it breaks.** The equivalence holds within the model's assumptions: single period, no labour income, proportional base, consume everything. It breaks once labour income, heterogeneous saving, liquidity constraints, or life-cycle structure are introduced. The paper should explain the equivalence as a model-structural property, not as a claim that the two systems are equivalent in practice.

**The concentration consequence.** 479× at N=30 is a Category 1 finding. It is the consequence of taxing the stock regardless of return performance, combined with persistent Fagereng-style return heterogeneity. The mechanism: a low-return taxpayer and a high-return taxpayer with the same initial wealth pay the same proportional tax on that wealth each period, so nothing in the tax system dampens the differential compounding of returns. This is the structural property that the delta base eliminates by construction — the WDT taxes the delta (return net of cost of capital), so a low-return year generates a lower tax burden or a refund, attenuating the compounding differential.

---

## 8. Part III — Literature Positioning

### Argumentative job of Part III

Part III does not defend the results of Part II. They have been presented with their calibration notes and comparable-treatment exposures. Part III explains where WFR sits in the existing literature — specifically, it identifies the active dispute the paper enters (Guvenen vs Boadway/Spiritus), explains that WFR does not adjudicate it, and argues that WFR's contribution is to add the delta instrument to a comparison that has been conducted across only two instruments.

### §7 — The existing literature and the gap WFR fills

**7.1 D-M and risk-sharing.**
Domar and Musgrave (1944) derive the risk-sharing result for proportional taxation with full loss offsets. The flat symmetric WDT is a direct application of this mechanism to a wealth-delta base. State confidently. The qualification — D-M is a risk-sharing result, not a welfare-superiority result — was established in §2 and need not be repeated at length here; a cross-reference suffices.

**7.2 Progressive taxation and risk asymmetry.**
Vickrey (1939) and subsequent work identify that if gains fall into a higher bracket than losses are refunded, risk-taking is discriminated against even with loss offsets. WFR's C3 result (WFR.A §B.3) is a quantification of this long-identified mechanism under the specific logistic WDT schedule. Direction is literature-supported; the magnitude and the counterintuitive negative Excess column are WFR's contributions.

**7.3 CGT lock-in.**
The mechanism is textbook. IMF and OECD identify the realisation rule as creating lock-in by allowing indefinite deferral. Ivković, Poterba, and Weisbenner (2005) provide empirical confirmation of the lock-in effect, stronger for large transactions and longer holding periods. WFR's P(locked in) decomposition — separating fundamental non-switching (r_B < r_A) from CGT-induced lock-in (r_A ≤ r_B < r_B*) — clarifies a distinction the literature does not always maintain.

The 142.96 bp figure is not externally validated. Arachi et al. (2022, *Fiscal Studies*) is the primary counterargument. The paper has already addressed Arachi in §4 at the structural level. Here, cite Arachi as the appropriate methodological caution, note that the paper has engaged with their mechanism directly, and confirm the framing: the 142.96 bp is the model's result at stated calibration.

**7.4 Heterogeneous returns.**
Fagereng et al. (2020, *Econometrica*) and the 2016 AER P&P companion establish: substantial within-asset-class return heterogeneity, positive correlation between wealth and returns, substantial persistence. The 10th-to-90th percentile gap is approximately 18pp. WFR's use of persistent return heterogeneity is well-motivated by this literature; the model's contribution is to ask what happens when persistent return differences interact with specific tax bases over a multi-decade horizon.

**7.5 The active dispute WFR enters — and why it does not adjudicate it.**

There is a live dispute about what tax base to favour when returns are heterogeneous:

*Guvenen et al. (Minneapolis Fed; NBER 2024):* With heterogeneous returns, a stock wealth tax improves efficiency by pushing taxation toward low-return wealth holders and encouraging capital reallocation toward productive uses. Revenue-neutral wealth-tax substitution can raise welfare in their calibrated model.

*Boadway and Spiritus (2025, Economic Journal):* When individuals have heterogeneous returns, positive capital-income taxation can be Pareto-efficient, and the optimal rate rises with the degree of return heterogeneity. A direct counterweight to Guvenen.

*Dalle Luche et al. (2026, Review of Income and Wealth):* Extends optimal-tax analysis to joint heterogeneity in wealth and returns, arguing that increasing returns to wealth at the top have strong implications for tax design. This is the frontier closest to WFR's modelling problem.

WFR does not adjudicate this dispute. Both Guvenen and Boadway/Spiritus compare stock wealth tax and capital-income tax. WFR introduces a delta-based accrual tax that is neither. The correct framing: the existing dispute establishes that return heterogeneity materially changes the tax-base comparison; WFR adds the delta instrument and asks where it sits. This is a gap-filling contribution, not a side-taking contribution.

The text must not say: "The literature shows accrual taxation is superior to capital-income taxation when returns differ." It does not. The dispute is live and the paper has no business claiming to resolve it.

The text should say: "The existing comparison literature has established that return heterogeneity changes the relative performance of stock wealth taxation and capital-income taxation in ways that challenge both Chamley-Judd-style zero-capital-tax results and standard wealth-tax critiques. WFR introduces the delta-based accrual instrument into this comparison for the first time."

**7.6 Stock wealth = consumption tax in the model.**
Bastani and Waldenström (2023, Oxford Review of Economic Policy) and IMF (2024) establish the equivalence in a simple lifetime model. WFR's exact equivalence (both reach −1.8870% and 479×) is a model-structural property. The paper should explain the mechanism and note where it breaks in richer settings.

**Literature map table.** A summary table of the form in backbone v3 §10.7 should appear here. Column headers: WFR finding / Literature / Drafting note (what can be stated confidently vs what is the model's own contribution).

---

## 9. Part IV — Synthesis and the Burden-of-Consideration Conclusion

### Argumentative job of Part IV

Part IV applies the three-category epistemic framework to the paper's findings, names the Category 3 prospective costs that the paper has not quantified, draws the budget comparison between Category 1 and Category 3 explicitly, and reaches the burden-of-consideration conclusion. The conclusion must follow from the argument, not from an assertion.

### §8 — What the model establishes and what it does not

**8.1 Category 1: what we know about existing systems.**

The model has established, under controlled conditions and at revenue equivalence, four Category 1 findings about existing tax systems. These findings do not require WDT to exist. They are not contingent on WDT implementation choices. A reader who rejects the WDT entirely must still account for these findings about systems that currently operate:

1. CGT imposes a lock-in welfare cost of 141–143 bp (Ver. A, canonical calibration) once portfolio choice is endogenous. The mechanism — realisation contingency creating a switching wedge — is textbook and very strongly supported in the empirical literature. The magnitude is the model's contribution.

2. Stock wealth and consumption taxes produce 479-fold Great/Poor concentration at the 30-year horizon under Fagereng-calibrated return heterogeneity. The mechanism is the absence of return-conditioning: taxing the stock regardless of performance does not attenuate the compounding of persistent return differentials.

3. Income tax produces 320-fold concentration at the same horizon — better than stock wealth/consumption but substantially worse than both WDT variants (286–288×). The mechanism is the same: income tax does not condition on the net return relative to a cost of capital, so the gross Fagereng differential compounds without attenuation.

4. Income tax and CGT (without lock-in) are welfare-equivalent in the baseline by construction. The large real-world divergence between income tax and CGT welfare outcomes operates through the lock-in mechanism — which means the realisation rule is the welfare-relevant policy choice, not the rate or the base considered in isolation.

**8.2 Category 2: what we know about the WDT without implementation data.**

The model has also established several properties of the WDT that follow from the design of the delta base and the symmetric refund, independently of implementation outcomes:

1. Flat-rate symmetric WDT satisfies Domar-Musgrave to floating-point precision. The government participates proportionally in both gains and losses, contracting the net return distribution without altering risk rankings. This is a structural property of the delta base — it holds wherever the rate is proportional and refunds are symmetric.

2. The WDT eliminates realisation lock-in by construction. The switching decision is not tax-relevant under the delta base: switching from asset A to asset B changes the future return stream the delta base is applied to, but does not trigger a realisation event. The lock-in mechanism simply does not arise.

3. The lifetime contribution envelope eliminates SRR solvency risk by construction. Refund obligations are bounded by cumulative receipts from each taxpayer. The envelope is not a limitation on the welfare properties of the symmetric refund — it is the mechanism that makes the refund commitment sustainable without pre-funding.

4. The WDT's accrual basis makes it more progressive in incidence than income tax when returns are heterogeneous: the base scales with both wealth and return differential, while income tax scales with gains only. The Poor/Great incidence ratio is 6.6:1 for WDT versus 3.2:1 for income tax.

5. Progressive WDT provides better CEW than all alternatives at the Poor tier and better CEW than income tax and stock wealth tax at all tiers. The symmetric refund disproportionately benefits the low-return tier, which spends more time in loss states.

**8.3 Category 3: what we do not know.**

The following are genuine prospective costs of WDT implementation that the model cannot quantify and that require either empirical estimation from analogous systems (EVAL) or WDT implementation data (PHASE1):

- **Valuation friction under Route D.** The four-route valuation architecture (VAL) determines how assets without liquid prices are assessed. The architecture is designed to minimise friction; the empirical friction cost under real-world implementation is unknown.
- **Compliance and avoidance costs at scale.** BEHAV establishes theoretical stability of the mild-overstatement equilibrium (α ≈ 1.2–1.5); it does not establish the empirical compliance cost that HMRC-level implementation would generate.
- **Administrative learning dynamics.** The speed at which an administering body develops operational competence with the Route D auction process has no empirical analogue.
- **Migration response.** Jakobsen et al. (2024) and Agrawal et al. (2025) provide calibration ranges from existing wealth taxes; WDT-specific migration dynamics are untested.
- **Novel avoidance strategies.** The mild-overstatement equilibrium (ENV) is the settled equilibrium for the declaration game; avoidance strategies specific to the symmetric refund — loss engineering, basis manipulation — are prospective.

These are not hypothetical objections. They are real costs that any serious implementation of the WDT would generate. The paper does not claim they are zero. It claims that EVAL's break-even analysis is the correct tool for determining whether any of them plausibly exceeds the Category 1 welfare costs the paper has established.

**8.4 The comparative question.**

Given the three categories, the welfare comparison between existing systems and WDT cannot be resolved by noting that WDT has not been implemented. That observation establishes that Category 3 costs are unknown — it does not establish that they are large. The question is:

*Are the Category 3 prospective costs of WDT implementation plausibly larger than the Category 1 welfare costs of the systems WDT would replace?*

This is not the question that administrative familiarity answers. Administrative familiarity establishes that existing systems are known and WDT is not — it says nothing about the relative magnitude of welfare costs. The CGT's 142.96 bp lock-in cost and the stock wealth tax's 479× concentration path are not reduced by familiarity. They are properties of the existing systems that this analysis has made visible.

The break-even framing (EVAL) translates this into a quantitative question: starting from the 142.96 bp lock-in welfare advantage, how large would each Category 3 cost have to be to offset that advantage? If the break-even for migration requires, say, 40% of assessed taxpayers to exit — far above anything in the empirical wealth-tax literature — then migration cannot plausibly explain away the welfare advantage. If a break-even threshold falls within a plausible empirical range, that identifies a genuine uncertainty that EVAL must resolve. WFR establishes the welfare advantage EVAL will use as its starting point.

### §9 — The burden-of-consideration conclusion

**The conclusion the evidence supports:**

Once tax systems are compared on their welfare consequences rather than merely their administrative familiarity, WDT cannot reasonably be dismissed without addressing the welfare mechanisms identified here.

The mechanisms are four, and each is actionable:

**Symmetric risk participation.** The delta base with symmetric refund satisfies the Domar-Musgrave risk-sharing condition by construction, attenuating consumption variance while preserving risk-taking incentives. No existing system in the tested set has this property. This is a structural design difference, not a calibration choice.

**Structural elimination of realisation lock-in.** CGT with endogenous portfolio choice imposes a 142.96 bp welfare cost at canonical calibration — approximately 82 times the baseline welfare difference between systems. This cost is eliminated by construction under the WDT because the tax base does not make the switching decision tax-relevant. The Arachi objection to accrual taxation — that it creates intertemporal consumption distortions in loss years — is specifically addressed by the symmetric refund, which restores consumption capacity at the moment it is most needed.

**Concentration moderation under persistent return heterogeneity.** At the 30-year canonical horizon, WDT variants reach 286–288× Great/Poor concentration versus income tax at 320× and stock wealth/consumption at 479×. The split is accrual vs stock, not flat vs progressive. The delta base's conditioning on net return relative to a cost of capital attenuates the compounding of persistent return differentials that produce the 479× outcome under stock-base systems.

**Progressive incidence from the accrual base.** The WDT is more progressive in incidence than income tax — 6.6:1 ratio versus 3.2:1 — because the delta base scales with both wealth and return differential. The symmetric refund delivers disproportionate welfare benefit to the low-return tier, which is also the tier that spends the most time in loss states.

**What a dismissal would have to establish:**

A dismissal of the WDT on welfare grounds would have to establish one or more of the following: (a) the CGT lock-in mechanism does not operate as the model and the empirical literature describe; (b) persistent return heterogeneity does not interact with the stock base to produce the concentration path the model shows; (c) the Category 3 prospective costs of WDT implementation plausibly exceed 142.96 bp — the current Category 1 welfare cost of CGT lock-in that WDT eliminates by construction; or (d) some welfare cost of WDT that this paper has not identified or has mismeasured is large enough to reverse the comparison.

Each of (a) and (b) runs against a large body of empirical evidence. Neither (c) nor (d) can currently be established because WDT has not been implemented — but the absence of an empirical estimate of WDT-specific costs is not evidence that those costs are large. It is evidence that EVAL's break-even analysis is the right next step.

The paper does not claim WDT is the optimal tax system. It establishes that the welfare case is coherent, that it rests on mechanisms that are independently well-evidenced, and that the principal welfare objection to accrual taxation is addressed by the WDT's symmetric structure. A decision to maintain CGT or a stock wealth tax as the default is, after this analysis, a decision to accept known welfare costs. That decision may be defensible on grounds that EVAL and PHASE1 will investigate. It cannot be defended on welfare grounds without engaging with the mechanisms this paper has measured.

---

## 10. Back matter

### 10.1 Cross-paper connections (to appear as footnotes or in the introduction, not as a separate section)

- **LR.A §2.1–2.3:** Gaps #1, #2, #3 — state that all three are closed simultaneously and that the simultaneous closure is the contribution
- **Open register item #17** (τ₀ × W_min joint surface): The N=30 finding — accrual vs stock dominates flat vs progressive on concentration — confirms τ₀ is the dominant calibration parameter at canonical parameters, consistent with SWEEPS §7.1
- **Open register item #18** (SRR calibration): Poor tier envelope binding at 2001 establishes the correct SRR implication — liquidity timing question, not solvency capitalisation. Connect here.
- **RATES pre-behavioural caveat:** WFR results are also pre-behavioural; cross-reference the shared limitation
- **ENV §2 (mild-overstatement equilibrium):** Refund exposure under mild overstatement exceeds the WFR baseline; WFR welfare results for loss states are a lower bound on refund commitment
- **SWEEPS §7.1 (τ₀ as dominant parameter):** The concentration decomposition confirms this

### 10.2 WFR.A appendix (already complete)

The appendix tables are complete as of 2026-09-10. The paper's primary job is to make them legible, not to reproduce them. Each appendix table should be referenced from the section that uses it, with a sentence explaining what the table shows and where to look for detail.

Outstanding before paper is ready to submit:
1. **Code annotation fix (non-blocking for drafting):** Update "after 73 years" print label and "73-Year Empirical Sequence" chart title in `module4_heterogeneous.py` to reflect the correct 30-year horizon. Not a model change; a string fix. Charts cannot be used in the paper with wrong labels.
2. **WFR.A §D.5 table footnote:** Add explanation for the "—" cell in the off-diagonal spot check — solver boundary condition, not model failure.
3. **Optional WFR.A sensitivity:** N=73 concentration run if the progressive advantage at longer horizons is wanted as appendix evidence.

### 10.3 EVAL forward pointer (to appear in the introduction and in §8.4)

WFR identifies the welfare mechanisms and quantifies them under controlled conditions. The break-even analysis — for each Category 3 cost, what magnitude would erase the Category 1 welfare advantage? — is EVAL's primary contribution. WFR should point to EVAL at the end of §8.4 without pre-claiming EVAL's findings. The language: "Whether any of the Category 3 implementation costs plausibly exceeds the 142.96 bp welfare advantage is the question EVAL is designed to answer. WFR establishes the welfare advantage that question must contend with."

---

## 11. Referee risks and how to manage them

### 11.1 "You haven't shown WDT has no welfare costs."

*Correct response:* The paper does not claim WDT has no costs. It identifies and names the Category 3 prospective costs explicitly (§8.3). The paper's claim is that the Category 1 welfare costs of existing systems are large and structural, that several Category 2 properties of WDT eliminate or substantially alter those costs, and that the Category 3 costs require a break-even analysis (EVAL) to evaluate. This is a more defensible position than a welfare-tournament framing — it is precise about the epistemic situation.

### 11.2 "The CGT comparison is idealised vs realistic in asymmetric directions."

*Correct response:* The asymmetry is stated in the methodology section (§5.3) before the results, not in response to the referee. The design choice — suppress distortions uniformly in the baseline, then admit the dominant CGT distortion in isolation to measure its effect cleanly — is methodologically transparent. The companion papers (VAL, BEHAV, CLOSE) address the WDT-specific practical objections the model abstracts away from. A pointer to those papers is the correct response to demands that WDT-specific costs be quantified in this paper.

### 11.3 "The concentration comparison uses aggregate revenue equivalence, which favours WDT."

*Correct response:* Aggregate revenue equivalence is the correct implementation of revenue neutrality in a heterogeneous population. The tier-level incidence figures (WFR.A §D.2) are in the appendix. The paper states in the methodology section that aggregate equivalence produces different effective burdens at the tier level; the magnitude is visible in WFR.A §D.2. This is not a concealed thumb on the scale — it is a stated design feature of the comparison.

### 11.4 "The 142.96 bp lock-in cost is a model artefact, not a real-world welfare estimate."

*Correct response:* The framing discipline is already built in. The paper presents 142.96 bp as the model's result at the stated calibration. It does not assert this as an estimate of the general welfare cost of CGT lock-in. The mechanism is very strongly supported in the empirical literature; the magnitude is the model's contribution and is not claimed to be externally validated. The P(locked in) decomposition (WFR.A §C.1) separates the CGT distortion component from fundamental non-switching, which defends the model against the conflation objection.

### 11.5 "The start year selection (2000) was chosen to favour WDT."

*Correct response:* WFR.A §E.2.1 shows WDT ranks first in 100% of the 73 start-year windows. A referee who argues the 2000 start year was selected to favour WDT must explain why WDT also wins in 1972, 1987, and 1999. The sweep closes this objection.

### 11.6 "The near-equivalence of symmetric and progressive WDT at N=30 undermines the paper's argument for progressive WDT."

*Correct response:* The near-equivalence is an honest finding that reduces the advocacy character of the result. It is stated as such in §5(b). A model that showed progressive WDT dramatically outperforming all alternatives on all dimensions would invite more scrutiny than one that shows a nuanced picture. The N=30 finding is: the relevant split is accrual vs stock, not flat vs progressive. That is an informative result, not a gap in the argument. If the referee wants evidence of the progressive advantage at longer horizons, WFR.A provides the N=73 sensitivity (if run) or acknowledges the horizon limitation in prose.

### 11.7 "You have not addressed behavioural responses."

*Correct response:* This paper is explicitly Level 1: theoretical welfare case under controlled conditions, distortions admitted one at a time. Behavioural calibration is the scope of EVAL. The pre-behavioural caveat is shared with RATES and should be cross-referenced. The paper's results are a lower bound on the welfare advantage in the presence of positive behavioural effects from WDT (symmetric refund encouraging risk-taking, lock-in elimination allowing portfolio reallocation) and an upper bound in the presence of negative behavioural effects (migration, avoidance). EVAL's break-even analysis determines which bound is binding.

---

## 12. Drafting sequence

The following sequence minimises rework. Later sections depend on framing decisions made earlier.

1. **Methodology section (§5.3 of this plan)** — write first. Every subsequent framing decision about what the baseline suppresses, what the three-category taxonomy means, and what the comparable-treatment exposures are needs to be settled before the results sections are drafted.

2. **Part I §1 (baseline CEW table and structural observations)** — write second. The table is fixed; the prose needs to set up the organising question that Part II answers.

3. **Part I §2 (D-M mechanism, verdict deferred)** — write third. The discipline about what D-M does and does not establish must be in place before the lock-in section, because the lock-in section's Arachi pivot relies on the reader understanding that D-M is a mechanism result, not a welfare result.

4. **Part II §4 (CGT lock-in)** — the paper's most important section. Write before §3, §5, and §6. The Arachi pivot in §4(c) is the structural hinge of the whole paper; it needs to be in its final form before the surrounding sections are drafted so their framing is consistent.

5. **Part II §3 (progressive rates)** — write after §4. The section's close ("all three are second-order relative to what follows") only makes sense once §4 exists.

6. **Part II §5 (heterogeneous returns)** — write after §4. The envelope binding result (§5(e)) cross-references the Category 2 properties established in §4.

7. **Part II §6 (stock wealth and consumption taxes)** — write after §5. Most of the content has been introduced earlier; this section connects the dots.

8. **Part III §7 (literature positioning)** — write after Part II. The literature section's Arachi treatment, Guvenen/Boadway framing, and gap statement all depend on Parts I and II being drafted.

9. **Part IV §§8–9 (synthesis and conclusion)** — write last. The three-category framework is applied to findings that are now drafted; the conclusion follows from what the paper has established, not from what the plan intended.

10. **Introduction** — write after everything else. The introduction can then point forward accurately to what the paper actually argues, not to what the plan intended.

---

*End of WFR paper plan v1.*
*Outstanding pre-drafting actions: module4 label fix; WFR.A §D.5 table footnote. Both non-blocking for drafting; blocking for figure use and code sharing.*
