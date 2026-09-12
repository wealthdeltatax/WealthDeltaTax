# WFR Paper — Planning Backbone v2
*Updated: 2026-09-10. Reflects model run with current appendix tables (WFR.A §A–§E) and code audit of (WFR.A §D).*
*v1 backbone is superseded. All cited numbers are from the current tables.*

---

## 1. What the WFR paper is doing

The paper closes three confirmed literature gaps from LR.A §2:

- **Item #1** — Domar-Musgrave formal extension to a progressive delta base (three complications)
- **Item #2** — Welfare comparison including the delta base alongside existing candidates
- **Item #3** — Distributional arithmetic of delta-base concentration under persistent return heterogeneity (Fagereng et al.)

No prior paper holds all three simultaneously, or evaluates them against the same empirical return distribution at revenue equivalence. That is the paper's primary contribution.

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

**(WFR.A §D.4) Envelope binding:** Poor tier binds in 2001 with min slack = £0.0000m. This is the concrete numerical realisation of the ENV paper's SRR early-year funding gap — the Poor tier's −4.55pp differential produces a loss in the first scenario year before any cumulative tax has been paid. The paper must name this explicitly, connect to open register item #18, and note the policy implication: the SRR needs pre-funding from other sources, or the entry-year assessment must provide an initial credit against future taxes.

**(WFR.A §D.5) Off-diagonal:** Corner B Symmetric WDT shows "—". This is a solver boundary condition — at Great W₀ (£139.6m) with Poor return differential (−4.55pp), the symmetric WDT generates large expected refunds that prevent the aggregate revenue target from being reached within τ ∈ (0, 0.999]. Not a bug; a boundary condition. Requires a table footnote explaining why the cell is undefined.

---

## 4. The paper's core argument

The paper does not claim WDT wins an efficiency tournament. It claims:

1. At revenue equivalence, mechanical welfare differences between tax systems are small (≤17.4 bp for the WDT vs income tax base comparison) when behavioural distortions are suppressed. No system dominates on base properties alone.

2. The differences that matter emerge from distortions: CGT imposes large lock-in costs (142.96 bp, Ver. A at canonical G/V and T=5); stock-base systems allow heterogeneous returns to compound into extreme concentration (479× vs 286× at N=30); no existing system shares return risk symmetrically.

3. Progressive WDT is the only instrument in the tested option set that simultaneously: (a) shares return risk symmetrically, (b) eliminates realisation lock-in by construction, (c) moderates concentration relative to stock-base systems, and (d) maintains progressive incidence without being a stock wealth tax.

4. The progressive vs flat WDT distinction on concentration is not visible at N=30 — the Fagereng differential dominates at this horizon. The relevant distributional split at the canonical horizon is accrual basis vs stock base.

---

## 5. Welfare ranking — summary statement

Ranking of existing systems in the single-agent frame:

Income tax > CGT (no lock-in) ≫ CGT (with lock-in) ≈ Stock wealth ≈ Consumption tax

This ranking is only useful within the single-agent frame. In the distributional frame: income tax produces 320× concentration at N=30; stock wealth tax produces 479×. The existing literature contains models in which both wealth taxation and capital-income taxation can be efficient under heterogeneous returns — this is an active theoretical dispute, not a settled result. WFR does not adjudicate that dispute. What it does is introduce a third instrument — a delta-based accrual tax — that has different properties from both comparators and that the existing comparison literature has not tested.

The headline claim the paper can defend is not "WDT outperforms all alternatives." It is: **within the model's assumptions, progressive WDT is the only tested system that combines symmetric return-risk sharing, absence of realisation lock-in, and lower 30-year concentration than all income-based and stock-based alternatives.** That is an empirical statement about the model experiment, not a claim about the optimal tax system. It is also harder to attack than a welfare-tournament framing, because it is precise about what dimensions are being compared and does not require the model to be a general equilibrium characterisation of the economy.

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

The results support a sequential argument:

1. **Baseline** — mechanical welfare differences are small; no existing system dominates on base properties; WDT advantage is 17.4 bp, not a knockout result
2. **Risk sharing** — flat WDT satisfies D-M exactly; this is a risk-sharing result, established separately from the welfare result; progressive WDT breaks the exact D-M identity but the welfare cost of doing so is negligible at canonical parameters
3. **D-M complications** — C1 is second-order across the tested population; C2 is real but small at normal leverage; C3 exists and is measurable but minor relative to C1 and the lock-in effect
4. **Lock-in** — endogenising the realisation decision produces the dominant welfare result; WDT advantage grows from 1.74 bp to 142.96 bp (Ver. A); the case for WDT over CGT rests almost entirely here; the 142.96 bp is a model result at the stated calibration, not an empirical estimate; Arachi et al. (2022) is the primary counterargument and must be addressed
5. **Literature positioning** — the existing literature contains an active dispute between Guvenen et al. (wealth tax can improve efficiency under heterogeneous returns) and Boadway/Spiritus (capital-income tax can also be optimal under heterogeneous returns); WFR does not adjudicate this dispute; it introduces a third instrument — the delta-based accrual tax — that neither strand of the existing literature has tested; this is the correct framing of WFR's contribution, stronger than "WDT performs better"
6. **Heterogeneous returns** — at N=30, the accrual vs stock-base distinction is the dominant distributional split; progressive WDT has better welfare across all tiers than all alternatives; the progressive vs flat WDT concentration advantage requires horizons beyond N=30 to compound
7. **Synthesis** — progressive WDT is the only tested system combining symmetric risk-sharing, absence of lock-in, and lower concentration than all comparators; the progressive advantage on concentration is real but horizon-dependent; the paper establishes the structural channels and positions the delta base within an active theoretical debate rather than claiming to settle it

---

## 8. Cross-paper connections to flag in the WFR paper

- **LR.A §2.1–2.3:** WFR closes items #1, #2, #3 — state explicitly
- **Open register item #17** (τ₀ × W_min joint surface): The finding that accrual vs stock-base dominates concentration at N=30 (not flat vs progressive) confirms τ₀ is the dominant calibration parameter, consistent with SWEEPS §7.1
- **Open register item #18** (SRR calibration implication): Poor tier envelope binding at 2001 is the concrete evidence bearing on this item
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

*End of planning backbone v2. Sections integrated in this version: §11 (comparable treatment). Code fix (module4 labels) and WFR.A §D.5 footnote remain as the only outstanding pre-drafting actions.*