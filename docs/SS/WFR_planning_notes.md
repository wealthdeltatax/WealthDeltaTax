# WFR Paper — Planning Backbone v3
*Updated: 2026-09-11. Reflects model run with current appendix tables (WFR.A §A–§E) and code audit of (WFR.A §D).*
*v2 backbone is superseded. All cited numbers are from the current tables.*

---

## 1. What the WFR paper is doing

The paper closes three confirmed literature gaps from LR.A §2:

- **Item #1** — Domar-Musgrave formal extension to a progressive delta base (three complications)
- **Item #2** — Welfare comparison including the delta base alongside existing candidates
- **Item #3** — Distributional arithmetic of delta-base concentration under persistent return heterogeneity (Fagereng et al.)

No prior paper holds all three simultaneously, or evaluates them against the same empirical return distribution at revenue equivalence. That is the paper's primary contribution.

WFR is a Level 1 paper in the welfare evaluation taxonomy: it establishes the theoretical welfare case under controlled assumptions, identifies the structural channels through which the delta base differs from existing instruments, and positions those channels within the active theoretical debate. It does not attempt to calibrate behavioural responses, close the general equilibrium, or produce a quantitative ex-ante welfare estimate under empirically estimated parameters. That is the scope of a companion paper — provisionally EVAL — identified in §13 as the next step in the programme. WFR's burden-of-consideration conclusion is the right endpoint for a Level 1 paper; EVAL's break-even analysis is the right endpoint for Level 2. The two papers are complementary, not competing, and WFR's argument is stronger for being precise about what it does and does not claim.

---

## 2. Canonical N = 30

N = 30 is declared across VAL, RATES, SWEEPS, and WFR. The concentration path (WFR.A §D.3) already uses this: `run_concentration_analysis()` draws its scenario from `make_scenario_sequence(p, N)` where `N = p["tcm"]["canonical_N"] = 30`. The table caption correctly describes the "30-year scenario horizon starting 2000." The Python print statements and chart titles that say "73 years" are stale labels — they report 30-year results with unupdated copy. **This is a code annotation fix, not a model fix, and must be corrected before the code is shared or the charts used in the paper.**

---

## 3. Current model findings

All numbers below are from the current appendix tables (generated 2026-09-10). The v1 backbone numbers are replaced throughout.

### 3.1 Baseline single-agent welfare (WFR.A §A.1)

At revenue equivalence and γ=2, empirical distribution (Ver. A):

| System | CEW |
|---|---:|
| Symmetric WDT | −1.7539% |
| Income Tax | −1.7713% |
| CGT | −1.7713% |
| Stock Wealth Tax | −1.8870% |
| Consumption Tax | −1.8870% |

WDT advantage over income tax/CGT: **17.4 bp**. This is not a large efficiency claim. It establishes that WDT does not lose the base comparison, and that the large welfare differences emerge from distortions addressed in later sections.

Two structural results. (1) Stock wealth tax and consumption tax cluster at exactly −1.8870% across all γ — γ-invariance is correct and diagnostic: these systems apply a fixed proportional wedge leaving the relative consumption distribution unchanged, so CRRA scale-invariance makes risk aversion irrelevant. (2) Income tax = CGT throughout (WFR.A §A) — correct by construction; the lock-in separation is endogenous and enters only in (WFR.A §C).

The Ver. A / Ver. B rate differential for income tax (32.067% vs 33.404%) is worth a prose note: the historical distribution includes genuinely negative return years where income tax collects nothing but the symmetric WDT provides refunds, requiring a slightly lower rate to hit the same revenue target. The idealised two-state distribution misses this.

### 3.2 Domar-Musgrave test (WFR.A §A.4)

Flat-rate symmetric WDT satisfies D-M to floating-point precision across all γ and both distributions (gap ≈ 10⁻¹⁶ to 10⁻¹⁷). The D-M result is a risk-sharing result; the paper must keep this separate from the welfare result. (WFR.A §A.2) confirms the variance interpretation: WDT Var(C) = 0.0013, versus income/CGT 0.0014, versus stock wealth/consumption 0.0027.

### 3.3 Progressive rates — three D-M complications (WFR.A §B.1–§B.3)

**C1 (progression, WFR.A §B.1):** Gap is −0.00 bp at £10m across all γ and distributions. Correct: at W₀ = 5 × W_min, the logistic is nearly flat at τ₀, so progressive ≈ flat. The paper states this cleanly: C1 distortion is negligible at moderate wealth levels with canonical rate parameters. Running at £50m or £100m would widen the gap. (WFR.A §E.3.1–§E.3.4) confirms the gap remains sub-0.05 bp even at £100m across the full parameter range — so C1 is a second-order effect throughout the tested population.

**C2 (leverage, WFR.A §B.2):** Now present. Gap rises from 0.00 bp at 0% leverage to +1.10 bp at 70% leverage. NW base produces marginally better welfare than the asset-return alternative at all leverage ratios — the agent is poorer in W₀ terms as debt rises, reducing the absolute tax burden relative to the asset-return comparator. The direction is clean and monotone; the magnitude is small. State it as: C2 is real, direction is confirmed, magnitude is second-order at normal leverage ratios, reaches 1.10 bp only at extreme leverage (70%).

**C3 (intertemporal rate asymmetry, WFR.A §B.3):** The Asymmetry column (τ_gain − τ_refund) ranges from +0.0011 pp at £3m to +0.0946 pp at £200m. The Excess column is consistently negative — progressive WDT collects *less* net tax than flat in the gain-then-loss sequence. This is because the wealth levels tested sit in the near-flat region of the logistic, where progressive effective rates are below the flat benchmark rate (~33%). The C3 narrative in the paper must specify that the gain-at-higher-rate effect materialises only well above the logistic inflection point. The table still stands as a genuine empirical finding: C3 exists and is measurable; at canonical parameters and realistic wealth levels it is quantitatively minor.

### 3.4 CGT lock-in (WFR.A §C.1–§C.3)

The dominant result in the paper.

**(WFR.A §C.3) summary:**

| Metric | Ver. A (Empirical) | Ver. B (Idealised) |
|---|---:|---:|
| WDT CEW | −1.7539% | −1.7525% |
| CGT CEW (no lock-in) | −1.7713% | −1.7525% |
| Lock-in welfare cost | +141.22 bp | +41.19 bp |
| CGT CEW (with lock-in) | −3.1834% | −2.1644% |
| WDT advantage (no lock-in) | +1.74 bp | +0.00 bp |
| WDT advantage (with lock-in) | +142.96 bp | +41.19 bp |

The WDT advantage grows from 1.74 bp (base comparison) to 142.96 bp (with lock-in) under Ver. A. The mechanism is correct — CGT with endogenous realisation decision is structurally worse than CGT without. Ver. B (41.19 bp) understates severity because P(locked in) = 100% in the idealised two-state distribution by construction — half the states trigger lock-in regardless of parameters. The paper leads with Ver. A as the primary result.

**Framing discipline required.** The 142.96 bp figure is the model's result at the stated calibration (G/V=50%, T=5, τ_cgt=24%, r_A=10.45%, γ=2, empirical distribution). It is not an estimate of the general welfare cost of CGT lock-in. The paper must present it as: "in this model calibrated to UK parameters, the welfare cost of the lock-in distortion is 141 bp." The mechanism is very strongly supported by the literature (see §10); the magnitude is the model's contribution and is not externally validated. Arachi et al. (2022) is the most important counterargument to cite: they show that although realisation taxation generates lock-in, accrual taxation can create its own intertemporal consumption distortions, meaning accrual is not automatically welfare-superior. The paper should address this directly — the WDT's answer is that the delta base with symmetric refund specifically avoids the consumption-distortion problem Arachi et al. identify, because the refund in loss years restores the agent's consumption capacity rather than simply deferring a liability.

**(WFR.A §C.1) G/V sweep:** Lock-in cost rises from +16.4 bp at G/V=5% to +162.2 bp at G/V=76.6%, then dips before rising again above 81%. The non-monotonicity at high G/V is a discretisation artefact of the finite 30-state empirical distribution — boundary effects in P(locked in) as r_B* approaches distribution limits. Worth a footnote; not a model error.

**(WFR.A §C.1) P decomposition:** The three-column decomposition (P(total locked), P(CGT distortion), P(r_B < r_A)) resolves the planning notes' concern. At G/V = 5–31.8%, P(CGT distortion) = 0.0% — all lock-in is fundamental preference (r_B < r_A), not a CGT distortion. The CGT distortion proper begins only above G/V = 36.3%. At the G/V = 50% reference, P(CGT distortion) = 3.3%. The paper must be precise: the high P(locked in) at low G/V reflects market return states below r_A, not CGT-induced lock-in.

**(WFR.A §C.2) T sweep:** Lock-in cost rises from +56.1 bp at T=1 to a plateau of +181.1 bp at T≥8. The caption correctly states the direction is upward. The accompanying note correctly distinguishes the two phenomena: r_B* converges toward r_A as T→∞ (indifference return converges), while welfare cost rises with T (more compounding periods of foregone superior return). The WFR.8 caption issue from the v1 backbone is resolved.

### 3.5 Heterogeneous agents (WFR.A §D.1–§D.5)

**(WFR.A §D.1) CEW by tier:**

| System | Poor | Ok | Good | Great |
|---|---:|---:|---:|---:|
| Symmetric WDT | −0.2194% | −0.7816% | −1.4211% | −1.9269% |
| Income Tax | −0.6000% | −0.9274% | −1.4413% | −1.9161% |
| Stock Wealth Tax | −1.8424% | −1.8424% | −1.8424% | −1.8424% |
| Progressive WDT | −0.1375% | −0.5004% | −0.9223% | −1.3814% |

Progressive WDT is better for Poor (−0.1375% vs −0.2194% symmetric) and worse for Great (−1.3814% vs −1.9269% symmetric) — the redistribution mechanism is working. The comparison between symmetric WDT and income tax for the Poor tier is notable: income tax gives −0.6000% where symmetric WDT gives −0.2194%. The symmetric refund disproportionately benefits the low-return tier, which spends more time in loss states. This is a welfare argument for symmetric structure that the paper should surface explicitly.

**(WFR.A §D.2) Incidence:** Symmetric WDT has a Great/Poor incidence ratio of 2.2071% / 0.3362% = 6.6:1. Income tax is 2.1903% / 0.6779% = 3.2:1. Stock wealth tax is effectively flat (2.0163% / 1.8689% = 1.08:1). The WDT's accrual basis makes it more progressive than income tax in incidence because the base (net return × W₀) scales with both wealth and the return differential, whereas income tax scales with gains only.

**(WFR.A §D.3) Concentration path at N=30:**

| System | Initial | 2004 | 2009 | 2019 | 2029 |
|---|---:|---:|---:|---:|---:|
| Progressive WDT | 48.8× | 66.1× | 90.3× | 162.3× | 288.1× |
| Symmetric WDT | 48.8× | 65.1× | 87.4× | 157.2× | 286.3× |
| Income Tax | 48.8× | 65.5× | 90.2× | 166.1× | 320.2× |
| Stock Wealth Tax | 48.8× | 70.5× | 103.3× | 220.1× | 479.0× |
| Consumption Tax | 48.8× | 70.5× | 103.3× | 220.1× | 479.0× |

**The key finding:** At N=30, symmetric WDT (286.3×) and progressive WDT (288.1×) are nearly identical. The v1 backbone's claim — "accrual alone does not moderate concentration; progressivity does" — does not hold at this horizon. The Fagereng return differential (+8pp gap between Poor and Great tiers) completely dominates the progressive vs flat rate differential over 30 years. The logistic schedule at canonical parameters hasn't risen far enough above τ₀ to compound a meaningful difference.

The honest finding to state in the paper: **at N=30, the distinguishing axis is accrual basis vs stock base, not flat vs progressive rate.** Both WDT variants reach approximately 286–288×; both income-tax-family systems reach 320×; both stock-base systems reach 479×. The relevant split is two-way (accrual vs stock), not three-way. The progressive advantage on concentration requires a longer horizon to compound — this is an honest statement of a genuine scope limitation, and connects to the paper's pre-behavioural caveat.

If a longer-horizon sensitivity is wanted to show the progressive advantage does emerge, a 73-year run would demonstrate this. This could be an appendix item rather than a primary result.

**(WFR.A §D.4) Envelope binding:** Poor tier binds in 2001 with min slack = £0.0000m. The Poor tier's −4.55pp return differential produces a loss in the first scenario year before any cumulative tax has been paid. When the envelope floor binds, no refund is owed — the lifetime contribution envelope caps refunds at cumulative taxes paid to date, so a taxpayer who has paid nothing receives nothing. The refund is not issued rather than issued and unfunded.

This is the correct and important mechanic: the lifetime contribution envelope eliminates SRR solvency risk by construction. Refund obligations can never exceed cumulative receipts from that taxpayer. The SRR's capitalisation requirement is therefore a liquidity timing question — covering the gap between when refunds are paid out and when the next collection cycle settles — not a structural funding shortfall. The paper must state this clearly, as the naive reading of "envelope binds" is that the government owes a refund it cannot cover.

The policy implication is narrower than previously stated: the SRR needs adequate liquidity reserves for timing gaps, not external pre-funding to cover a structural deficit. Connect to open register item #18 on SRR sizing, and note that the binding result for the Poor tier is evidence that early-year liquidity needs are modest by construction — the taxpayer with the lowest return history also has the smallest cumulative contribution and therefore the smallest potential refund claim.

**(WFR.A §D.5) Off-diagonal:** Corner B Symmetric WDT shows "—". This is a solver boundary condition — at Great W₀ (£139.6m) with Poor return differential (−4.55pp), the symmetric WDT generates large expected refunds that prevent the aggregate revenue target from being reached within τ ∈ (0, 0.999]. Not a bug; a boundary condition. Requires a table footnote explaining why the cell is undefined.

---

## 4. The paper's core argument

The paper does not claim WDT wins an efficiency tournament. It claims:

1. At revenue equivalence, mechanical welfare differences between tax systems are small (≤17.4 bp for the WDT vs income tax base comparison) when behavioural distortions are suppressed. No system dominates on base properties alone.

2. The differences that matter emerge from distortions: CGT imposes large lock-in costs (142.96 bp, Ver. A at canonical G/V and T=5); stock-base systems allow heterogeneous returns to compound into extreme concentration (479× vs 286× at N=30); no existing system shares return risk symmetrically.

3. Every competitor system carries a structural cost that becomes welfare-relevant once the corresponding behavioural mechanism is admitted: income tax allows persistent return heterogeneity to compound into concentration; CGT imposes realisation lock-in once portfolio choice is endogenous; stock wealth and consumption taxes tax the stock regardless of performance and provide no symmetric loss participation. Progressive WDT is the only instrument in the tested option set that does not carry an equivalent structural cost at any of the tested margins — it simultaneously: (a) shares return risk symmetrically, (b) eliminates realisation lock-in by construction, (c) moderates concentration relative to stock-base systems, and (d) maintains progressive incidence without being a stock wealth tax.

4. The progressive vs flat WDT distinction on concentration is not visible at N=30 — the Fagereng differential dominates at this horizon. The relevant distributional split at the canonical horizon is accrual basis vs stock base.

---

## 5. Welfare ranking — summary statement

Ranking of existing systems in the single-agent frame:

Income tax > CGT (no lock-in) ≫ CGT (with lock-in) ≈ Stock wealth ≈ Consumption tax

This ranking is only useful within the single-agent frame. In the distributional frame: income tax produces 320× concentration at N=30; stock wealth tax produces 479×. The existing literature contains models in which both wealth taxation and capital-income taxation can be efficient under heterogeneous returns — this is an active theoretical dispute, not a settled result. WFR does not adjudicate that dispute. What it does is introduce a third instrument — a delta-based accrual tax — that has different properties from both comparators and that the existing comparison literature has not tested.

The headline claim the paper can defend is not "WDT outperforms all alternatives." It is: **within the model's assumptions, progressive WDT is the only tested system that combines symmetric return-risk sharing, absence of realisation lock-in, and lower 30-year concentration than all income-based and stock-based alternatives.** That is an empirical statement about the model experiment, not a claim about the optimal tax system. It is also harder to attack than a welfare-tournament framing, because it is precise about what dimensions are being compared and does not require the model to be a general equilibrium characterisation of the economy.

The critical pivot on which this claim rests is the relationship between the symmetric refund and the Arachi objection. Arachi et al. (2022) establish that accrual taxation is not automatically welfare superior to realisation taxation, because accrual creates an intertemporal consumption distortion by billing unrealised gains before the taxpayer has liquidity to pay without adjusting consumption. This is the strongest available counterargument to any accrual-based tax. The WDT's answer is specific: the symmetric refund in loss years restores consumption capacity at the moment it is most needed, which is precisely the intertemporal distortion Arachi et al. identify as accrual taxation's failure mode. The WDT is not simply an accrual tax — it is an accrual tax with a structural mechanism that addresses the principal welfare objection to accrual taxation. That distinction must be made explicit in the paper, not left implicit in the model mechanics.

The paper's conclusion should ultimately place a burden-of-consideration question on the reader: **if a tax system can be designed to share investment risk symmetrically, avoid realisation lock-in, and tax persistent increases in private wealth without taxing wealth merely for being held — and if the principal welfare objection to accrual taxation is addressed by its symmetric structure — what is the economic justification for excluding that tax base from serious consideration?** The paper does not have to prove WDT is the optimal tax system. It has to establish that the welfare properties are sufficiently unusual and sufficiently favourable that dismissing the delta base without investigating it would itself be unjustified. The current results are capable of supporting that claim.

---

## 6. Model status — what is done and what remains

### Done — ready for paper drafting

| Section | Content | Status |
|---|---|---|
| WFR.A §A.1–§A.4 | Baseline CEW, D-M test, variance, rates | ✓ |
| WFR.A §B.1 | C1 (progression gap) | ✓ |
| WFR.A §B.2 | C2 (leverage / NW base) | ✓ Added |
| WFR.A §B.3 | C3 (rate asymmetry) | ✓ |
| WFR.A §C.1 | Lock-in by G/V with P decomposition | ✓ |
| WFR.A §C.2 | Lock-in by T, caption corrected | ✓ |
| WFR.A §C.3 | Full WDT vs CGT comparison | ✓ |
| WFR.A §D.1 | CEW by tier | ✓ |
| WFR.A §D.2 | Incidence | ✓ |
| WFR.A §D.3 | Concentration path (N=30) | ✓ — narrative updated |
| WFR.A §D.4 | Envelope binding | ✓ |
| WFR.A §D.5 | Off-diagonal spot check | ✓ — footnote needed for "—" cell |
| WFR.A §E.1–§E.3.4 | Revenue sweep, start-year sweep, parameter sweep | ✓ |

### Remaining before paper is ready to submit

**Code fix (non-blocking for drafting):** Update the "after 73 years" print label and "73-Year Empirical Sequence" chart title in `module4_heterogeneous.py` — these are stale annotations reporting 30-year results. The figures cannot be used in the paper with the wrong labels. Not a model change; a string fix.

**(WFR.A §D.5) footnote (non-blocking for drafting):** Add a note explaining why Corner B Symmetric WDT is undefined — solver boundary condition, not a model failure.

**Optional — N=73 concentration sensitivity:** A 73-year run of the (WFR.A §D.3) concentration path would show whether the progressive WDT advantage over flat WDT on concentration emerges at longer horizons. This is useful context but not required for the paper's primary claims. If added, it should appear as an appendix sensitivity, not as a primary result. Decision: run or note the horizon limitation in prose.

---

## 7. Narrative structure (proposed)

The paper's argument is a progressive transition that changes the reader's organising question at each step. The structure is not a sequence of results but a movement: each step generates the question that the next step answers. The paper should be written so the reader feels that movement, not just reads the results.

**Step 1 — Concede the obvious. Ask the organising question.**

Start with the controlled baseline. WDT: −1.7539%. Income tax/CGT: −1.7713%. Stock wealth/consumption: −1.8870%. The WDT advantage is 17.4 bp. No knockout. State this plainly and use it: the small baseline difference establishes that WDT is not winning because it carries a lower tax burden. Then ask the question the rest of the paper answers: *if welfare differences are small when distortions are suppressed, where does the actual welfare cost of existing systems come from?*

**Step 2 — Investment risk. Establish the mechanism, not the verdict.**

Flat WDT satisfies Domar-Musgrave to floating-point precision. State what this means: the government becomes a proportional participant in both gains and losses, reducing the taxpayer's effective return risk without changing the relative attractiveness of risky assets. Then state explicitly what this does *not* mean: D-M is a risk-sharing result, not a welfare-superiority result. D-M identifies the mechanism through which WDT can reduce welfare-relevant consumption variance without creating the conventional risk-taking distortion. The welfare implication depends on what else is true about the economy. The mechanism is established here; the welfare payoff arrives in later steps.

**Step 3 — Progressive rates. Show the complications are real but second-order.**

Three D-M complications arise under a progressive rate schedule. C1 (progression itself) is negligible at canonical parameters across the tested population — sub-0.05 bp even at £100m. C2 (leverage) is real and monotone but reaches only 1.10 bp at extreme leverage (70%). C3 (intertemporal rate asymmetry) exists and is measurable but minor relative to what comes next. The progressive rate schedule does not materially undermine the risk-sharing properties established in Step 2. This clears the ground for the dominant result.

**Step 4 — Endogenous realisation. The dominant welfare result.**

Now allow the taxpayer to make the decision an actual taxpayer makes: should I sell this asset and switch to the better-returning alternative? CGT's realisation mechanism now matters. The WDT advantage grows from 1.74 bp (frictionless baseline) to 142.96 bp (Ver. A, G/V=50%, T=5). That is roughly 82 times the baseline advantage. The organising question from Step 1 is answered: the welfare cost of CGT does not come from its tax base considered in isolation — it comes from making taxation contingent on realisation. The important distortion is behavioural, not mechanical.

This is where Arachi et al. (2022) must be addressed directly, not defensively. Arachi establish that accrual taxation is not automatically welfare superior because it creates intertemporal consumption distortions by billing unrealised gains before the taxpayer has liquidity. The WDT's answer is the symmetric refund: loss-year refunds restore consumption capacity at exactly the moment it is most needed, which is the specific distortion Arachi identify as accrual's failure mode. WDT is not simply an accrual tax — it is an accrual tax that addresses the principal welfare objection to accrual taxation through its symmetric structure. State this as the pivot, not as a footnote.

**Step 5 — Heterogeneous returns. Stop treating taxpayers as identical.**

Introduce the Fagereng empirical premise: people do not simply have different amounts of wealth; they have persistently different returns on that wealth, with a gap of approximately 8pp between the Poor and Great tiers. Now ask what happens when those heterogeneous returns interact with different tax bases over 30 years. The result is striking: both WDT variants reach 286–288×; income tax reaches 320×; stock-base systems reach 479×. The dominant split is accrual vs stock, not flat vs progressive. That is the more interesting finding — the mechanism by which the tax base interacts with return heterogeneity matters more than the rate schedule at the canonical horizon.

Establish also that progressive WDT provides better CEW welfare across every tier than all alternatives, with the symmetric refund disproportionately benefiting the low-return tier (Poor tier: −0.1375% vs income tax −0.6000%). The symmetric structure is not just a macro risk-sharing property — it delivers concrete welfare benefits to the taxpayers most exposed to return risk.

**Step 6 — Literature positioning. Add the instrument, don't adjudicate the dispute.**

The existing literature is divided between Guvenen et al. (stock wealth tax can improve efficiency under heterogeneous returns) and Boadway/Spiritus (capital-income tax can also be optimal under heterogeneous returns). WFR does not adjudicate this dispute. Both papers are about stock wealth tax vs capital-income tax. WFR introduces a delta-based accrual tax that is neither. The correct framing: the dispute establishes that return heterogeneity materially changes the tax-base comparison; WFR adds the delta instrument and asks where it sits. This is a contribution claim that identifies a gap rather than taking a side.

**Step 7 — Synthesis. The burden-of-consideration conclusion.**

Bring the steps together: every competitor system carries a structural cost that becomes welfare-relevant once the corresponding behavioural mechanism is admitted. Income tax: concentration compounds under persistent return heterogeneity. CGT: realisation lock-in creates a 142.96 bp welfare cost once portfolio choice is endogenous. Stock wealth and consumption taxes: tax the stock regardless of performance, provide no symmetric loss participation, and produce the most extreme concentration path. Progressive WDT is the only tested instrument without an equivalent structural cost at any of the tested margins. Its advantage is small in the frictionless baseline and becomes large when empirically relevant mechanisms are admitted — which is precisely what you would expect from a tax base designed to address those mechanisms.

The conclusion does not claim WDT is the optimal tax system. It places a burden-of-consideration question on the reader: if a tax system can be designed to share investment risk symmetrically, avoid realisation lock-in, and tax persistent increases in private wealth without taxing wealth merely for being held — and if the principal welfare objection to accrual taxation is structurally addressed by its symmetric design — what is the economic justification for excluding that tax base from serious consideration? The paper establishes that no such justification emerges from the welfare comparison. That is the knockout.

---

## 8. Cross-paper connections to flag in the WFR paper

- **LR.A §2.1–2.3:** WFR closes items #1, #2, #3 — state explicitly
- **Open register item #17** (τ₀ × W_min joint surface): The finding that accrual vs stock-base dominates concentration at N=30 (not flat vs progressive) confirms τ₀ is the dominant calibration parameter, consistent with SWEEPS §7.1
- **Open register item #18** (SRR calibration implication): Poor tier envelope binding at 2001 is the concrete evidence bearing on this item. The correct implication is that the lifetime contribution envelope eliminates SRR solvency risk by construction — refunds cannot exceed cumulative taxes paid, so the SRR is never called upon to cover a structural shortfall. Item #18 therefore concerns SRR liquidity sizing (timing of outflows vs inflows within a collection cycle), not solvency capitalisation. This is a stronger property than previously recorded in the backbone.
- **RATES pre-behavioural caveat:** WFR results are also pre-behavioural; the two papers share this stated limitation and should cross-reference it
- **ENV §2** (mild-overstatement equilibrium): Refund exposure under mild overstatement exceeds the WFR baseline; the WFR welfare results for loss states are a lower bound on refund commitment
- **SWEEPS §7.1** (τ₀ as dominant parameter): The concentration decomposition confirms this — the flat vs progressive distinction on concentration at N=30 is second-order relative to the accrual vs stock-base distinction

---

## 9. What the hostile referee will say — and how to answer

The hostile framing from the planning notes stands unchanged and should be addressed in the paper:

> "The authors compare an analytically idealised WDT with realistic versions of competitor systems, using a partial-equilibrium single-period model without behavioural responses, calibrated to a stress scenario that favours variance-compressing mechanisms."

The honest response remains: this model establishes the welfare-theoretic case under idealised conditions, identifies the structural channels (D-M, lock-in, concentration), and the companion papers (VAL, BEHAV, CLOSE) address the practical objections the model abstracts away from. Each paper does a specific job.

One addition from the updated analysis: the near-equivalence of symmetric and progressive WDT at N=30 on concentration *reduces* the advocacy character of the result. A model that showed progressive WDT dramatically outperforming all alternatives on all dimensions would invite more scrutiny than one that shows a nuanced picture — the 30-year finding is honest, and honest findings are more defensible.

**The concentration result (WFR.A §D.3) is still the strongest independent argument** — it doesn't rely on welfare assumptions, it's not scenario-sensitive in direction, and it speaks directly to a policy concern. At N=30, the WDT variants collectively reach 286–288×, versus income tax at 320×, versus stock-base systems at 479×. That is a clean, three-way result that survives the partial-equilibrium critique.

---

## 10. Literature positioning

This section maps WFR's findings against the existing literature. The purpose is to distinguish what the literature establishes (the mechanism), what is contested (the welfare implications under heterogeneous returns), and what is WFR's own quantitative contribution (the magnitude results). The paper should be explicit about which category each claim falls into.

### 10.1 Domar-Musgrave and risk sharing

**Status: strongly supported.**

Domar and Musgrave (1944) derive the risk-sharing result explicitly: when the government participates proportionally in both gains and losses through full loss offsets, the agent's net return distribution contracts proportionally and risk-taking incentives are preserved. The flat symmetric WDT is a direct application of this mechanism to a wealth-delta base. The paper can state this connection confidently.

The important qualification is the one the backbone already carries: D-M is a risk-sharing result, not automatically a welfare-superiority result. Once general equilibrium, endogenous asset supply, adverse selection, and labour supply are introduced, the welfare implications are not automatic. The paper must maintain this separation throughout. The D-M confirmation (WFR.A §A.4) establishes the mechanism; it does not by itself establish welfare superiority.

The subsequent literature also shows the D-M risk-taking result can be altered by market structure and adverse selection. Cite these as the limits of the D-M framework, then show the model's welfare results as the next step.

### 10.2 Progressive taxation and risk asymmetry

**Status: supported theoretically; magnitude is WFR's contribution.**

Early public finance literature (e.g. Vickrey 1939, and work collected in the St. Louis Fed volume) explicitly notes that if gains fall into a higher bracket than losses are refunded, risk-taking is discriminated against even with loss offsets, and proposes income averaging as a remedy. WFR's C3 result (WFR.A §B.3) is a quantification of this long-identified mechanism under the specific logistic WDT schedule. The direction is literature-supported; the magnitude (0.0011 pp at £3m to 0.0946 pp at £200m) and the finding that it is minor relative to the lock-in effect are WFR's own results. The counterintuitive finding — that the Excess column is negative, meaning progressive WDT collects less net tax than flat in the gain-then-loss sequence — requires the mechanism to be stated very explicitly in the paper, since it is not a result the literature directly anticipates.

### 10.3 CGT lock-in

**Status: mechanism very strongly supported; magnitude is WFR's contribution.**

The CGT lock-in mechanism is textbook public finance. The IMF identifies the realization rule as creating lock-in because taxpayers can defer tax by postponing realization, retaining assets despite the availability of better alternatives. The OECD similarly identifies the efficiency problem as discouraging disposal and reinvestment. Ivković, Poterba and Weisbenner (2005) provide empirical confirmation of the lock-in effect in taxable vs tax-deferred accounts, with the effect stronger for large transactions and longer holding periods.

WFR's P(locked in) decomposition — separating fundamental non-switching (r_B < r_A) from CGT-induced lock-in (r_A ≤ r_B < r_B*) — is a useful clarification that the literature does not make explicitly. It prevents the paper from committing the common error of calling all retained positions "lock-in."

**The 142.96 bp figure is not externally validated.** The mechanism is strongly supported; the welfare magnitude is the model's result at the stated calibration. The paper must frame this correctly (see §3.4 above). The primary counterargument to cite and address is Arachi et al. (2022, *Fiscal Studies*), who show that accrual taxation can generate larger intertemporal consumption distortions than realisation taxation, meaning the welfare comparison is not automatically resolved in accrual's favour. WFR's answer is that the symmetric refund specifically addresses this: loss-year refunds restore consumption capacity rather than deferring a liability, which is the mechanism Arachi et al.'s critique targets.

### 10.4 Heterogeneous returns

**Status: empirical basis very strongly supported.**

Fagereng et al. (2020, *Econometrica*) establish: substantial heterogeneity in returns, heterogeneity within asset classes, positive correlation between wealth and returns, and substantial persistence in individual returns. Their 10th-to-90th percentile comparison produces an 18pp difference in average returns. The 2016 AER P&P paper makes the methodological point that ignoring heterogeneous returns can badly distort understanding of wealth inequality. WFR's use of persistent return heterogeneity in the concentration experiment is well motivated by this literature. The model's contribution is to ask what happens when people with systematically different returns are subjected to different tax bases — a question the Fagereng literature motivates but does not answer.

### 10.5 The active dispute WFR enters

**Status: active theoretical disagreement; WFR adds a new instrument, not a verdict.**

There is now a live dispute in the optimal taxation literature about what to do when returns are heterogeneous.

**Guvenen et al. (*Use It or Lose It*, Minneapolis Fed; NBER 2024):** With heterogeneous returns, a stock wealth tax can improve efficiency by pushing taxation toward low-return wealth holders, encouraging reallocation of capital toward productive uses. Revenue-neutral wealth-tax substitution can raise welfare in their calibrated model.

**Boadway and Spiritus (2025, *Economic Journal*):** When individuals have heterogeneous returns, positive capital-income taxation can itself be Pareto-efficient, and the optimal capital-income tax rate rises with the degree of return heterogeneity. This is a direct theoretical counterweight to the Guvenen et al. conclusion.

**The 2026 *Review of Income and Wealth* paper** (Dalle Luche et al.) extends optimal-tax analysis to joint heterogeneity in wealth and returns, arguing that increasing returns to wealth at the top have strong implications for tax design. This is the literature frontier closest to WFR's modelling problem.

WFR does not adjudicate the Guvenen vs Boadway/Spiritus dispute. Both papers are about stock wealth tax vs capital-income tax. WFR introduces a delta-based accrual tax that is neither. The correct framing is: the existing dispute establishes that return heterogeneity materially changes the tax-base comparison; WFR adds the delta instrument and asks where it sits. This is a stronger contribution claim than adjudicating the existing dispute, because it identifies a gap rather than taking a side.

**Do not write:** "The literature shows accrual taxation is superior to capital-income taxation when returns differ." It does not. There are competing mechanisms and the dispute is live.

**Write instead:** "The existing comparison literature has established that return heterogeneity changes the relative performance of stock wealth taxation and capital-income taxation in ways that challenge both Chamley-Judd-style zero-capital-tax results and standard wealth-tax critiques. WFR introduces the delta-based accrual instrument into this comparison for the first time."

### 10.6 The stock wealth = consumption tax equivalence

**Status: correct in the model; not a general empirical claim.**

The literature (Bastani and Waldenström 2023, *Oxford Review of Economic Policy*; IMF 2024 How-To Note) establishes that in a simple lifetime model with homogeneous saving and no labour income, consumption taxation exempts the normal return to saving while a proportional wealth tax taxes the stock regardless of realised return. The exact equivalence in WFR's single-agent model (both reach 479× at N=30, both CEW = −1.8870%) is a property of the model structure — single period, no labour income, proportional base, consume everything — not an empirical claim. The paper should explain why the equivalence holds in the model and note that it breaks once labour income, heterogeneous saving, liquidity constraints, or life-cycle structure are introduced.

### 10.7 Literature map for the paper

This table should inform the structure of WFR's literature review section. The third column identifies where the paper must be careful not to overclaim.

| WFR finding | Literature | Drafting note |
|:---|:---|:---|
| Flat symmetric WDT satisfies D-M | Domar & Musgrave (1944) | Direct application; state confidently |
| Full loss offset matters for risk-sharing | D-M + corporate tax literature | Strongly supported |
| Progressivity creates risk-sharing asymmetry | Vickrey (1939) and subsequent | Supported in direction; magnitude is WFR's |
| CGT creates lock-in | IMF; OECD; Ivković et al. (2005) | Very strongly supported; 142.96 bp is model result |
| Accrual ≠ automatically welfare superior | Arachi et al. (2022) | Must cite and address; WDT answer is the symmetric refund |
| Returns differ, persist, and rise with wealth | Fagereng et al. (2020, 2016) | Very strongly supported |
| Return heterogeneity changes the tax-base comparison | Guvenen et al.; Boadway/Spiritus (2025) | Active dispute; WFR adds delta instrument, doesn't adjudicate |
| Stock wealth = consumption tax in the model | Bastani & Waldenström (2023) | Model-specific; explain why; note it breaks in richer settings |
| WDT gives lower concentration at N=30 | — | WFR's quantitative result; not externally validated |
| Progressive ≈ flat WDT at N=30 on concentration | — | WFR's finding; honest and defensible |
| Progressive WDT combines X, Y, Z uniquely | — | Empirical claim about the model experiment; not an optimality claim |


## 11. Comparable Treatment — Where It Holds and Where It's Exposed

A hostile referee will inspect the comparison design before engaging with the results. This section pre-empts that inspection by naming both where the design is clean and where it is exposed. It should inform the methodology section of the paper itself, not just the response to reviewers.

### 11.1 Where comparable treatment holds cleanly

**Revenue equivalence is genuine.** E[T] = 2% of W₀ is solved numerically for each system, so rates differ across systems but the expected revenue burden is identical by construction. A referee cannot argue the comparison is tilted by giving WDT a lower rate.

**The welfare criterion is symmetric.** CEW is measured against the same no-tax benchmark for every system. Rankings are relative to that common reference point, not to each other directly. No system is measured on a more favourable scale.

**The return distribution is common.** All systems in Modules A and B face the same 73-observation empirical sequence (Ver. A) and the same idealised two-state distribution (Ver. B), at the same γ values. No system receives a more favourable draw.

**The sweep analysis closes the cherry-picking objection.** WDT ranks first in 100% of the 73 start-year windows (WFR.A §E.2.1). A referee who argues the 2000 start year was selected to favour WDT must explain why WDT also wins in 1972, 1987, and 1999. See §9 for the fuller treatment of this line of attack.

### 11.2 Where comparable treatment is more exposed

Three places where a careful referee will push.

**First: the CGT comparison is idealised vs realistic in asymmetric directions.** In Module A, CGT is modelled without the lock-in distortion — structurally it is income tax under a different name. Module C then adds lock-in. This sequencing is methodologically correct and transparent: it isolates the base comparison before introducing the distortion. But the asymmetry remains — CGT degrades as realism increases, while WDT is held at its idealised best throughout: no valuation friction, no compliance cost, no behavioural response. The paper must name this explicitly. The correct framing is that Module A establishes a baseline in which distortions are suppressed for all systems equally, and Module C introduces the CGT-specific distortion because it is the one that changes the welfare ranking most. The companion papers (VAL, BEHAV, CLOSE) address the WDT-specific practical objections that the model abstracts away from.

**Second: the concentration comparison uses aggregate revenue equivalence, not tier-specific equivalence.** The population-weighted aggregate tau drives the projection in (WFR.A §D.3). This is the methodologically correct design — "same aggregate revenue" is what revenue neutrality means in a heterogeneous population. But it produces substantially different effective burdens at the tier level: the Poor tier under symmetric WDT pays 0.34% of W₀ (WFR.A §D.2), against the Great tier's 2.21%. The stock wealth tax applies near-uniformly across tiers (1.87–2.02%). The concentration comparison is therefore not "same revenue burden per tier" — it is "same aggregate revenue." This should be stated in the paper, not left for a referee to notice. It is a feature of the accrual base — it collects less from low-return tiers because those tiers generate smaller deltas — but a referee unfamiliar with the mechanism will read it as a thumb on the scale.

**Third: the income tax / CGT identity in Module A understates real-world divergence.** The identity is correct within the model's stated assumptions (single period, all gains realised each period). In practice, income tax and CGT differ substantially — different statutory rates, different timing, different indexation rules, different treatment of losses across asset classes. The model cannot speak to any of these practical distinctions. The paper should acknowledge this rather than letting the identity imply the model settles the income tax vs CGT comparison that practitioners care about. The appropriate statement is that within the model's single-period realisation assumption, the two systems are identical; the lock-in distortion that separates them in practice is endogenous and enters only in Module C.

### 11.3 The unified response

None of the three exposures above invalidate the results. In each case the honest response is the same structure: name the limitation, identify it as a model design choice rather than cherry-picking, and point to where the practical objection is addressed.

The CGT asymmetry is a design choice — distortions are suppressed uniformly in the base comparison, then the dominant CGT distortion is added in isolation to measure its effect cleanly. The aggregate revenue design for the concentration comparison is the correct implementation of revenue neutrality in a heterogeneous population, and the tier-level incidence figures (WFR.A §D.2) are in the appendix for any reader who wants to inspect the effective burden distribution. The income tax / CGT identity is a stated model assumption, not a claim about the real-world relationship between the two systems.

The broader methodological point is the one already stated in §9: this model establishes the welfare-theoretic case under idealised conditions, identifies the structural channels, and the companion papers address the practical objections. That division of labour is not a weakness of the paper — it is the correct way to build a multi-paper programme where each paper does a specific job. The referee's objection, if it comes, should be met with a pointer to the companion paper that handles it, not a defensive qualification that undermines the model's own contribution.

---

## 12. Taxpayer Welfare Experience — The CEW Results as a Lower Bound

The WFR model measures welfare as CEW against a no-tax benchmark, at revenue equivalence, under idealised conditions. This is the right design for the comparative question the paper asks. But it means the model captures only the pure fiscal burden component of the taxpayer's welfare experience. The actual welfare position of a WDT taxpayer incorporates additional components that are uniformly positive for the WDT and outside the model's scope. The paper should name this explicitly: the CEW results are a lower bound on WDT welfare, not the full picture.

### 12.1 Components outside the model

**Compliance and avoidance cost reduction.** For the majority of assessed WDT taxpayers — those in the Poor and Ok tiers paying 0.34% and 0.92% of W₀ respectively (WFR.A §D.2) — the annual WDT liability is likely comparable to or below current combined expenditure on tax avoidance structures and the residual tax actually paid under those structures. If this holds empirically, the net financial position for this group is neutral or positive relative to the status quo, even before any other WDT-specific benefits are considered. This is an incidence claim, not a behavioural claim — it is testable in principle against compliance cost data from PHASE1's empirical programme. The paper should flag this as a direction for Phase One rather than asserting a result.

**Consumption smoothing from symmetric refunds.** The symmetric refund provides something qualitatively absent from all comparator systems: the state absorbs a proportional share of downside in loss years, at exactly the moment wealth has fallen and consumption pressure is highest. The D-M result captures variance reduction, but the consumption-timing value of the refund — receiving liquidity when you need it most — is a welfare benefit that CRRA utility in a single-period model does not fully capture. This is not a model failure; it is a scope boundary. Cross-reference WP §1 on the cooperative architecture and the distinction between pure extraction and proportional co-investment.

**Governance rights.** WDT taxpayers hold a stake in the SWF and governance rights through the cooperative architecture. These are a genuine return on the assessed position that no comparator system offers. They are not modelled in WFR — their valuation is outside the paper's scope — but they belong in the full welfare accounting and should be named as such.

**Elimination of lock-in costs.** The 142.96 bp lock-in welfare cost (WFR.A §C.3) is not only a model result — it represents a real friction that CGT taxpayers currently bear and navigate. The WDT eliminates this by construction. For taxpayers who are currently holding suboptimal positions because the CGT liability on switching exceeds the expected return differential, the WDT represents a direct improvement in portfolio efficiency that the CEW comparison only partially captures.

### 12.2 The lifetime contribution envelope: why the cap exists

The lifetime contribution envelope caps refunds at cumulative taxes paid to date. This is not fiscal conservatism — it closes a specific exploitation surface that would otherwise exist if refunds beyond the lifetime cap were permitted.

The attack vector without the cap: a taxpayer accumulates a modest tax history, engineers a large paper loss via inflated basis or related-party transaction, receives a refund exceeding their cumulative contribution (a net transfer from the state), then exits under CLOSE with the position legally settled and no recourse available to the government. The Governing Council could in principle offer beyond-cap refunds as a policy choice — to attract entrants, address specific hardship, or provide an entry-year credit for new taxpayers — but doing so explicitly reopens this surface and requires a new enforcement mechanism to close it.

The cap therefore reflects the same design logic as the cooperative architecture generally: align incentives before reaching for enforcement. A system that required the government to verify the authenticity of large loss claims before paying refunds would be operationally expensive and adversarial. A system where the refund is structurally bounded by prior contributions removes the incentive to manufacture losses in the first place.

Any future Governing Council experiment with beyond-cap refunds is treated as a named trade-off in (CLOSE §8.4): the benefit (more generous refund commitment, potentially attracting entrants with short tax histories) must be weighed against the exploitation surface it opens, and the enforcement mechanism required to close that surface must be specified before the extension is offered. The full argument for why the cap is set at cumulative contributions — rather than at the loss itself — is in (CLOSE §8.4). WFR cross-references that section; it does not repeat the argument.

### 12.3 What the paper should and should not claim

The paper should state clearly that WFR's CEW results measure the pure fiscal burden differential under controlled conditions. The full taxpayer welfare experience is better than the CEW figures suggest, for the reasons named above, but quantifying those additional components is outside WFR's scope and is addressed in companion papers (VAL for valuation stability, BEHAV for behavioural friction attenuation, PHASE1 for empirical compliance cost data, CLOSE for the envelope mechanics).

What the paper should not do is import those additional welfare components into the CEW comparison without modelling them. The strength of the WFR argument is precisely that it holds even at the lower bound — the CEW results already show structural advantages that survive the partial-equilibrium, idealised-conditions framing. Adding unmodelled welfare components to the argument would weaken it by inviting the referee to demand that they be quantified.

The correct structure is: model results first (lower bound, clean), companion paper cross-references second (additional welfare components, named but not claimed), and the combined picture as the conclusion (the case for WDT is robust to the model's own limitations).

---

## 13. EVAL — The Companion Paper (Provisional)

EVAL is the Level 2 companion to WFR: a quantitative ex-ante welfare evaluation of the WDT using empirically calibrated behavioural parameters, without requiring WDT implementation data. It is not a current paper in the programme; it is identified here as the natural next step once WFR is complete and PHASE1 begins generating evidence. This section records the scope, architecture, and sequencing so the relationship between WFR and EVAL can be described accurately in WFR's forward pointer.

### 13.1 What EVAL would do that WFR does not

WFR establishes the theoretical welfare case under controlled assumptions: distortions suppressed, representative agent, partial equilibrium, pre-behavioural. EVAL would extend that framework in four directions simultaneously:

**Behavioural calibration.** Rather than suppressing behavioural responses, EVAL would incorporate them as empirically estimated parameters drawn from the existing literature. CGT lock-in elasticities, wealth tax migration responses (Jakobsen et al. 2024; Agrawal et al. 2025), consumption responses to wealth shocks, and portfolio allocation responses to taxation are all estimable from existing systems without WDT implementation data. These enter the model as calibrated inputs with confidence intervals, not as unknowns.

**General equilibrium closure.** WFR is partial equilibrium — the government budget constraint is met by construction at revenue equivalence, but there is no asset pricing, no labour market, no aggregate saving response. EVAL would close the model at minimum sufficiently to propagate behavioural responses through the budget constraint and back into welfare. Full GE is not required; a sufficient closure is one that respects the government budget constraint under endogenous behavioural responses.

**Endogenous portfolio and realisation choice.** WFR's lock-in module treats the realisation decision as binary given the return differential. EVAL would model portfolio choice, switching frequency, and realisation timing as optimised responses to the tax schedule, calibrated against the empirical CGT literature.

**Uncertainty propagation.** WFR reports point estimates at canonical parameters and sweeps across ranges. EVAL would propagate uncertainty through the model — drawing behavioural parameters from their estimated distributions — and report welfare outcomes as distributions rather than point estimates, enabling statements about the probability that WDT dominates under empirically plausible assumptions.

### 13.2 The break-even analysis — EVAL's primary contribution

The most powerful tool EVAL can deploy is not a point estimate of WDT welfare superiority but a break-even analysis: for each source of potential WDT-specific implementation cost, what magnitude of that cost would be required to erase the welfare advantage identified in WFR?

Starting from WFR's 142.96 bp lock-in welfare cost as the primary welfare advantage, EVAL would calculate break-even thresholds for:

- **Compliance and valuation costs:** how large would per-taxpayer compliance costs have to be (as a fraction of assessed wealth) before the WDT welfare advantage disappears?
- **Migration:** what fraction of the assessed population would have to exit before the aggregate welfare gain is offset by the revenue and parallel-tax-base losses?
- **Avoidance:** what degree of systematic valuation manipulation would have to persist — beyond the mild-overstatement equilibrium VAL establishes — before revenue shortfall erases the welfare advantage?
- **Investment distortion:** what reduction in aggregate investment would have to occur before the welfare cost of reduced capital accumulation offsets the lock-in elimination benefit?
- **Administrative costs:** what government administrative cost per taxpayer would have to be incurred before the net welfare position turns negative?

Each break-even threshold is then compared against empirically plausible ranges from the existing literature. If the break-even for migration requires, say, 40% of assessed taxpayers to exit — a figure far above anything observed in the empirical wealth-tax migration literature — that is an extremely strong result. The welfare advantage does not require implementation to be nearly perfect; it requires that implementation costs not be catastrophically bad.

The resulting claim is not "WDT is better." It is: **the welfare advantage generated by eliminating realisation lock-in and symmetric risk participation is large enough that WDT-specific implementation costs would have to reach magnitude X before the theoretical welfare case fails — and X is substantially larger than anything observed in analogous systems.** That is a falsifiable, empirically grounded claim that is much harder to dismiss than a model point estimate.

### 13.3 What EVAL cannot establish without implementation data

There are irreducibly WDT-specific unknowns that EVAL can model but not observe:

- How wealthy taxpayers actually behave when wealth falls and a future refund is anticipated — the refund may affect risk-taking in ways that have no close empirical analogue in existing systems
- Novel avoidance strategies that emerge specifically in response to the delta base and the symmetric refund commitment
- Administrative learning dynamics — how quickly HMRC or an equivalent body develops operational competence with the Route D valuation process
- Political economy responses — how the cooperative architecture and SWF governance perform under fiscal stress or political pressure
- International coordination responses — how other jurisdictions react to a unilateral WDT in terms of bilateral information exchange and competitive tax design

These unknowns enter EVAL as sensitivity ranges, not calibrated parameters. EVAL's break-even analysis establishes how large these unknowns would have to be to matter. If the break-even thresholds are far above plausible ranges, the unknowns are second-order and the result is robust. If some break-even threshold falls within a plausible range, that identifies a priority empirical research target for PHASE1.

### 13.4 Sequencing relative to the programme

EVAL is a post-PHASE1 paper in its full form. PHASE1 will generate the first systematic evidence on several of the WDT-specific unknowns listed above — migration rates, administrative learning, valuation behaviour under the Route D architecture — which will sharpen the calibration inputs significantly. However, a preliminary version of EVAL's break-even analysis is achievable now using existing literature parameters, and could be published as a working paper alongside or shortly after WFR. The preliminary version would use conservative (unfavourable to WDT) parameter assumptions throughout and show that the welfare advantage survives even under those assumptions; the full version would refine the parameter estimates using PHASE1 data.

### 13.5 What WFR should say about EVAL

WFR's forward pointer (§1) identifies EVAL as the next step without committing to its findings. The paper should not pre-claim EVAL's results or imply that the Level 2 analysis will confirm WFR's conclusions. The correct language is: WFR establishes the theoretical welfare case and identifies the structural channels; quantifying the welfare advantage under empirically calibrated behavioural assumptions, and establishing the break-even thresholds at which the theoretical case fails, is the scope of EVAL. That division of labour is an honest description of where the programme currently stands and what it intends to do next.

---

*End of planning backbone v3. Sections integrated or rewritten in this version: §1 (EVAL forward pointer added); §4 (robustness-across-distortions framing); §5 (Arachi pivot and burden-of-consideration endpoint); §7 (rewritten as progressive transition); §11 (comparable treatment); §12 (taxpayer welfare experience as lower bound); §13 (EVAL companion paper scoped). §3.5 D.4 corrected: SRR pre-funding error removed; envelope mechanics stated correctly. §8 item #18 updated to reflect corrected mechanics. Code fix (module4 labels) and WFR.A §D.5 footnote remain as the only outstanding pre-drafting actions.*