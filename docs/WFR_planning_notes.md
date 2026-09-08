Here's a systematic read, module by module, with interpretive commentary on what's interesting, what's clean, and what needs attention before the paper can rely on these numbers.

---

## Module 1 (WFR.1–4)

**The system clustering is the headline finding.** Two distinct welfare groups emerge clearly:

- **Risk-sharing group** (Symmetric WDT, Income Tax, CGT): CEW around −1.64% to −1.73% at γ=2. These systems all share gains and losses in some form.
- **Proportional-base group** (Stock Wealth Tax, Consumption Tax): CEW locked at exactly −1.8107% across all γ values.

The proportional group's γ-invariance is correct and diagnostic — these systems apply a fixed proportional wedge to end-period wealth, so the relative consumption distribution is unchanged by the tax, and CRRA utility's scale-invariance means risk aversion makes no difference. This is a clean theoretical prediction and the data confirms it perfectly.

**The WDT's advantage narrows with γ, not widens.** At γ=1, WDT beats Stock Wealth Tax by 8.6 bp. At γ=4 it beats by 36 bp (−1.4813% vs −1.8107%). So the advantage actually grows with risk aversion — which is correct: more risk-averse agents value variance compression more, and the symmetric WDT is the only system providing full symmetric variance compression.

**Income Tax = CGT in Module 1 throughout.** Both show identical CEW and identical rates (18.944% Ver. A, 19.134% Ver. B). This is correct by construction — Module 1 treats CGT as a gains-only tax identical to income tax. The lock-in separation happens in Module 3. Worth a brief footnote in the table so readers don't think it's a bug.

**The rate asymmetry between Ver. A and Ver. B for Income/CGT is interesting.** Income tax requires 18.944% in Ver. A but 19.134% in Ver. B — the same rate as WDT. This happens because in the idealised two-state distribution, both states have positive gross returns (R_bad = 1 + μ − σ = 1 + 0.1045 − 0.0831 = 1.0214 > 1), so income tax collects on every state and its effective base is close to the symmetric WDT base. In Ver. A the historical sequence includes genuinely negative return years where income tax collects nothing but WDT receives refunds — so income tax needs a slightly lower rate to hit the same revenue target. This is a subtle but real insight about the two-state approximation's limitations.

**D-M holds to machine precision** (gaps of order 10⁻¹⁶). The rate is identical across all γ — 19.1337% in every row. That's expected because the D-M result and the revenue-equivalent rate don't depend on γ for the symmetric flat case.

---

## Module 2 (WFR.5, 6b, 6)

**WFR.5 — C1 gap is essentially zero.** After the revenue-matching fix, the gap across all (distribution, γ) combinations is −0.00 to −0.01 bp. This is the correct result for £10m: that wealth level sits in the entry-rate region of the logistic where the schedule is nearly flat at τ₀ = 15%, so the progressive system behaves almost identically to a flat 15.1% rate. The finding is that C1 distortion is negligible at moderate wealth levels with this rate schedule. The paper can state this cleanly: "at W₀ = 5 × W_min, progression contributes negligible additional welfare cost relative to a revenue-equivalent flat rate."

One thing to flag: the "vs 2% target" column shows −£0.0421m uniformly across all rows. That's right — E[T]_progressive is a function of the rate schedule and W₀ only, not γ, so the deviation from the 2% target is constant. But it does mean the C1 analysis is being run at a much lower revenue level (£0.158m vs £0.200m target). If you want to stress-test C1 at higher wealth — where the logistic has climbed — you'd run the analysis at W₀ = £50m or £100m and the gap would widen.

**WFR.6b — C2 leverage table.** The direction is clear and monotone: as leverage rises, the NW-base CEW is consistently *better* (less negative) than the AR-base CEW, and the gap grows from 0 bp at 0% leverage to +1.70 bp at 70%. The E[T] excess is small and negative throughout (NW base collects slightly *less* than AR base), meaning the actual WDT is marginally more favourable to leveraged agents in this scenario. The welfare advantage of the NW base comes from the smaller effective tax base at lower net worth — the agent is poorer in W₀ terms, which reduces the absolute tax burden relative to the asset-return comparator. At 70% leverage, W₀ has fallen to £3m and the welfare difference is 1.70 bp — small but no longer negligible for highly leveraged positions. This is a clean, honest finding: C2 is a second-order effect at normal leverage ratios, becomes meaningful at very high leverage.

**WFR.6 — C3 rate asymmetry.** The "Excess" column is consistently *negative* throughout. This means progressive WDT actually collects *less* net tax than the flat benchmark in the gain-then-loss sequence, not more. That's the opposite of the C3 description in the paper. The explanation is that the rate schedule at these wealth levels (£3m–£200m) is still mostly in the τ₀ region — the logistic hasn't risen far enough above 15% for the asymmetry to dominate. The gain-year rate (15.015% at £3m, up to 17.713% at £200m) is barely above the refund-year rate (15.014% / 17.619%), but the gain is taxed on a larger absolute delta than the loss is refunded, so the net tax is actually *lower* for progressive than flat because the flat rate (calibrated to the 2% global target at ~19%) is higher than the effective progressive rates in this wealth range.

This means two things. First, the C3 narrative in the paper ("gain taxed at higher rate, refund at lower rate, net excess cost") needs to specify that this materialises only well above the logistic inflection point — not at the wealth levels modelled here. Second, the table is still useful: it shows the rate asymmetry is real but quantitatively tiny at these levels (0.001–0.095 pp), and the net tax comparison is dominated by the rate-level difference between the flat benchmark and the progressive schedule.

---

## Module 3 (WFR.7–9)

**WFR.7 — Lock-in cost is large and non-monotone at high G/V.** Lock-in cost rises from 51 bp at G/V = 5% to a peak around 626 bp at G/V = 72%, then dips slightly (to 655 bp at 81.1%) before rising again. The non-monotonicity at the top end deserves scrutiny — it likely reflects a boundary effect where the indifference return r_B* exceeds the maximum return in the empirical distribution, so all states look like "always switch" and P(locked in) ticks up from 68.5% to 71–75%. The slight dip in lock-in cost at G/V ~80% is probably a discretisation artefact in P(locked in) from the finite 30-state distribution. Worth a footnote.

The P(locked in) numbers are striking: even at G/V = 5%, 57.5% of return states result in lock-in. That seems high and is worth checking. At G/V = 5% with r_A = 10.45% and τ_cgt = 24%, the indifference return is r_B* = r_B × 0.24 × 0.05 ≈ very small, so almost any r_B > r_A should break lock-in. The high P(locked in) at low G/V suggests the model is measuring something slightly different from what the label implies — possibly that many return states simply have r_B < r_A (the market return is below Asset A's expected return), not that the CGT creates the lock-in. This is a modelling clarity issue rather than an error, but the paper should be precise: P(locked in) here includes both the CGT lock-in proper and the case where the market return is simply below r_A.

**WFR.8 — Lock-in cost rises, not falls, with T.** The note says "cost declines as T increases" but the data shows the opposite: 265 bp at T=1, rising to a plateau around 512 bp by T=8 and staying there. This contradicts the stated direction. The theoretical intuition is wrong here — or the model is doing something different from the description. At T=1, the agent has only one period to benefit from switching, so the lock-in cost is lower. As T increases, the compounding benefit of being in the better asset for longer makes the lock-in cost *larger*. The plateau from T=8 onwards makes sense: beyond a certain horizon the indifference return r_B* converges to r_A and the locked/not-locked distinction becomes about the level of r_B* vs the distribution, not T. The note in the table and in `module3_lockin.py` needs correcting.

**WFR.9 — The lock-in numbers are very large.** The WDT advantage with lock-in is 453 bp (Ver. A) and 643 bp (Ver. B). These are substantial. The mechanism is correct — CGT with lock-in is much worse than CGT without — but the magnitude warrants a sense-check on the baseline: CGT CEW (with lock-in) = −6.17%. That means lock-in is costing the agent the equivalent of roughly 4.5% of initial wealth in perpetuity. At G/V = 50% and τ_cgt = 24%, that's plausible as an order of magnitude but sits at the high end. The Ver. B number (642 bp, CEW = −8.06%) is even larger because the idealised two-state distribution gives a P(locked in) = 50% by construction — exactly half the states trigger lock-in regardless of parameters. Worth flagging in the paper that Ver. B overstates lock-in severity for this reason.

---

## Module 4 (WFR.10–13)

**WFR.10 — Progressive WDT does more for the Poor tier and costs more for the Great tier, as intended.** Poor tier: Progressive WDT CEW = −0.683% vs Symmetric WDT −0.707% — so progressive is welfare-*better* for the poor agent. Great tier: Progressive WDT = −1.934% vs Symmetric WDT −1.767% — progressive is welfare-*worse* for the rich agent. The redistribution mechanism is working correctly.

The Income Tax and CGT numbers showing near-zero difference between tiers (−0.868% Poor, −1.764% Great) versus the Symmetric WDT (−0.707% Poor, −1.767% Great) reveals something interesting: income tax is harder on the Poor tier than the symmetric WDT. That's because the Poor tier has a negative return differential (−4.55 pp), meaning it experiences more loss states where income tax collects nothing but the symmetric WDT provides a refund. The refund mechanism disproportionately benefits the low-return tier. This is a strong welfare argument for the symmetric structure that the paper should surface explicitly.

**WFR.11 — Symmetric WDT incidence is the most progressive of all flat-rate systems.** At the Great tier it collects 2.16% of W₀; at the Poor tier only 0.92% — a ratio of 2.4:1. Income tax is similar (2.15% / 1.06% = 2.0:1). Stock wealth and consumption taxes are nearly flat across tiers (2.02% / 1.88% = 1.07:1). This is because the WDT base (net return × W₀) scales with both wealth and the return differential, whereas a wealth tax base scales with wealth alone.

**WFR.12 — Concentration is the dominant story here.** Starting at 50× Great/Poor ratio, the 30-year endpoint ranges from 291× (Progressive WDT) to 490× (Stock Wealth Tax, Consumption Tax). That's a near-10× spread in the final concentration ratio across tax systems — much larger than the welfare cost differences in basis points. The progression effect matters: Progressive WDT reaches 291× vs Symmetric WDT's 349× — a 58× difference attributable to the progressive rate schedule alone. This deserves prominence in the paper as the concentration result is arguably more striking than the welfare result.

**WFR.13 — The envelope binding for the Poor tier is important and needs attention.** The Poor tier binds in 2001 — the first year of the scenario sequence — with min slack = £0.0000m. This is the 2008 financial crisis year in the rotated sequence? No — 2001 is the dot-com crash, which hits the Poor tier particularly hard given its −4.55 pp return differential. The envelope binds because the Poor tier enters a severe loss state before accumulating enough cumulative tax to cover the refund. Min slack = 0.0000 means it hit exactly zero — the refund was capped. This isn't a calibration failure; it's the model correctly enforcing the envelope. But the paper should note it: under the 2000-start scenario, the poorest tier's first-year refund exceeds its cumulative tax contributions, and the envelope floor binds. That has a real-world policy implication — the SRR needs to be funded from other sources to honour the refund in the early years, or the entry-year assessment should provide some initial credit. This is the ENV paper issue in concrete numerical form.

---

## Summary of items requiring action before publication

Three issues need fixing or flagging:

1. **WFR.8 note direction is wrong** — lock-in cost rises with T, doesn't fall. Fix the note in `module3_lockin.py` and the `build_appendix` text.

2. **WFR.7 P(locked in) at low G/V needs clarification** — the 57.5% figure at G/V=5% conflates CGT lock-in with the base case of r_B < r_A. The paper should separate these explicitly.

3. **WFR.13 Poor tier envelope binding** — flag as the concrete numerical realisation of the ENV paper's SRR early-year funding gap. Currently the finding is silently present in the data; the paper needs to name it.

Yes, but be careful about how you frame that.

The results *are* favourable to the WDT, but the model is set up in a way that structurally advantages it, and a referee will notice. Before you lean on these numbers in the paper, you need to be honest with yourself about what the model can and can't establish.

---

**What the results genuinely establish**

The D-M result holds exactly. That's not an advocacy finding — it's a mathematical confirmation that the implementation is correct. The symmetric WDT compresses variance by exactly (1−τ)², which is what it's supposed to do.

The lock-in advantage over CGT is real and large (453 bp). This is probably the most defensible welfare argument in the paper because it doesn't depend on the WDT being intrinsically superior — it depends on CGT having a structural distortion that the WDT avoids by construction. That's a clean comparative claim.

The concentration path showing Progressive WDT reaching 291× vs Stock Wealth Tax at 490× is a genuine distributional result. It doesn't rely on welfare assumptions; it's just arithmetic on the return paths.

---

**What the model is doing that inflates the WDT's apparent performance**

Several structural choices tilt the comparison:

The **no-tax benchmark** is the welfare reference point. Every system looks bad relative to no-tax, but the WDT looks least bad because its D-M risk-sharing property genuinely reduces welfare cost. However, no-tax is not a policy counterfactual — the real comparison is WDT vs the existing CGT/income tax regime. The Module 3 comparison does this, but Modules 1–2 don't.

The **symmetric WDT proxy** in Module 1 has no progressive rate, no valuation friction, no lock-in analogue, and no envelope constraint. You're comparing the idealised version of the WDT against the realistic versions of competing systems. The progressive WDT in Modules 2 and 4 is closer to the real thing, but it still has no valuation uncertainty (the hardest practical objection) and no behavioural response.

The **revenue target of 2% of W₀** is arbitrary and chosen symmetrically across systems. In practice, the WDT's logistic schedule at £10m only collects £0.158m — 79% of the target. So the flat-rate systems are being taxed harder in absolute terms to hit the benchmark. This is partly what drove the spurious C1 result you spotted, and it may be subtly affecting the Module 1 rankings too for agents at moderate wealth levels.

The **single-period, no-saving model** removes the main behavioural distortions that generate welfare costs in reality — labour supply responses, investment distortions, portfolio reallocation. Income tax and CGT look worse than they would in a general equilibrium model because their lock-in and income effects are suppressed.

The **2000-start scenario** is one of the designated stress scenarios (worst 10-year coverage post-fill). It includes the dot-com crash and the 2008 crisis within the 30-year window. Systems that do better under volatile sequences — i.e., the WDT, which provides refunds — will mechanically look better in this scenario than they would under a benign growth sequence. Running the full 73-year series would give a fairer average, and running the 1960–1979 scenario (strong, steady growth) would probably compress the WDT advantage considerably.

---

**What a hostile referee will say**

"The authors compare an analytically idealised WDT with realistic versions of competitor systems, using a partial-equilibrium single-period model without behavioural responses, calibrated to a stress scenario that favours variance-compressing mechanisms. The welfare differences measured are small in absolute terms (sub-2% CEW) while the model omits the largest practical costs of WDT implementation — valuation uncertainty on illiquid assets, compliance costs, and the political economy of symmetric refunds."

That's not a fatal objection, but you need to have an answer for it in the paper. The honest version of that answer is: this model establishes the welfare-theoretic case under idealized conditions, identifies the structural channels (D-M, lock-in, concentration), and the companion papers (VAL, BEHAV, CLOSE) address the practical objections the model abstracts away from. Each paper does a specific job; none of them alone establishes the full case.

---

**What this means for how you write it up**

Lead with the channel identification, not the magnitudes. "The WDT has a structural advantage over CGT through the absence of lock-in distortion" is a strong, defensible claim. "The WDT has 453 bp lower welfare cost than CGT" is true in this model but will invite the objection above.

Be explicit about the scenario dependence. The 2000-start results are a stress test, not the central estimate. Either run the full 73-year series as the headline and show 2000-start as robustness, or be very clear in the text that these numbers are scenario-specific.

The concentration result (WFR.12) is actually your strongest independent argument — it doesn't rely on welfare assumptions, it's not scenario-sensitive in direction (just magnitude), and it speaks directly to a policy concern that resonates outside academic economics. That result probably deserves more prominence than the CEW tables.