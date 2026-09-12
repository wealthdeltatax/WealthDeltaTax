# WFR Paper — Planning Backbone
*Derived from model review session, September 2026*
*Status: pre-refinement. Model outputs reviewed; significant model work required before paper drafting begins.*

---

## 1. What the WFR paper is doing

The paper closes three confirmed literature gaps from LR.A §2:

- **Item #1** — Domar-Musgrave formal extension to a progressive delta base (three complications)
- **Item #2** — Welfare comparison including the delta base alongside existing candidates
- **Item #3** — Distributional arithmetic of delta-base concentration under persistent return heterogeneity (Fagereng et al.)

No prior paper in the existing literature holds all three simultaneously, or evaluates them against the same empirical return distribution at revenue equivalence. That is the paper's primary contribution.

---

## 2. Canonical N = 30

**Decision:** A single static N = 30 is declared across VAL, RATES, SWEEPS, and WFR.

**Dual justification:**

- *Demographic:* median UK inheritance receipt age ≈ 57, life expectancy ≈ 85 → expected years above W_min ≈ 28. N = 30 is a round central estimate.
- *Fiscal:* LRR breakeven year at the 2007 worst-case start = 29. N = 30 is adjacent and consistent.

**Why one value rather than paper-specific N:** Individual N is largely uncontrollable (mortality, threshold fall-through) and unpredictable (migration timing is the only controllable variable, excluded from this calculation). The variance in individual outcomes swamps any precision gained from separate derivations. One canonical value with two corroborating justifications is cleaner and more honest.

**Implication for WFR concentration results:** The 73-year concentration figures (e.g. 4,033× for symmetric WDT, 10,483× for stock wealth tax) should be reframed or rerun at N = 30. The directional result is expected to hold; the magnitudes will be less extreme and more defensible to readers.

---

## 3. Current model findings — what the evidence shows

### 3.1 Baseline single-agent welfare (Module 1)

At revenue equivalence, mechanical welfare differences between systems are small:

| System | CEW, γ=2, empirical |
|---|---:|
| Symmetric WDT | −1.6408% |
| Income tax | −1.6474% |
| CGT | −1.6474% |
| Stock wealth tax | −1.8107% |
| Consumption tax | −1.8107% |

WDT advantage over income tax/CGT: **0.65 basis points**. This is not noise — it is the correct answer to the baseline question. It establishes that WDT is not claiming mechanical efficiency superiority. The large welfare differences emerge from distortions, not from the base comparison.

**Important finding:** Stock wealth tax and consumption tax are welfare-equivalent in the single-period model. This is an artefact of the model's assumption that W₁ = C (consume everything), not a general result. The equivalence dissolves over multiple periods because a consumption tax only bites when wealth is actually spent — high-wealth agents who defer consumption indefinitely face a near-zero effective burden. The political advocacy pattern (wealthy agents opposing stock wealth tax while endorsing consumption tax) reflects this multi-period reality, not fiscal efficiency arguments.

### 3.2 Domar-Musgrave test (Module 1)

Flat-rate symmetric WDT satisfies D-M to floating-point precision across all tested γ and both distributions. Gap ≈ 10⁻¹⁶. This is the textbook confirmation the mechanism is correctly implemented.

Variance of consumption confirms the risk-sharing interpretation:
- WDT: 0.0045
- Income/CGT: 0.0046
- Stock wealth/consumption: 0.0067

The D-M result is a risk-sharing result, not yet a welfare result. These should be kept conceptually separate in the paper.

### 3.3 Progressive rates — three D-M complications (Module 2)

**C1 (progression):** Real and substantial. Progressive WDT shows better welfare than flat WDT in the CEW comparison (e.g. −1.2926% vs −1.6408% at γ=2). This is counterintuitive and needs careful framing.

The reason: CEW mixes two effects — the D-M deviation cost (bad) and redistribution (good for this agent at this wealth level). The redistribution effect dominates in this calibration. The paper must not write "progression breaks D-M → welfare falls." The model shows the opposite, and the explanation is the decomposition of these two effects.

**C2 (net-worth base vs asset return):** Present in the model architecture but does not surface cleanly as a standalone test in the current appendix tables. This is a gap that needs either a dedicated table or explicit acknowledgment.

**C3 (intertemporal rate asymmetry):** Exists mathematically but is quantitatively small:
- At £10m: 0.0037 pp rate asymmetry
- At £200m: 0.0946 pp rate asymmetry

This is a genuine empirical finding, not a null result to suppress. The multi-period rate asymmetry that LR.A §2.1 flags as unresolved turns out to be minor at these parameters. State it clearly.

### 3.4 CGT lock-in (Module 3)

The dominant result in the paper.

| Metric | Version A (empirical) | Version B (idealised) |
|---|---:|---:|
| WDT CEW | −1.6408% | −1.6308% |
| CGT CEW (no lock-in) | −1.6474% | −1.6308% |
| CGT CEW (with lock-in) | −6.1724% | −8.0564% |
| WDT advantage (with lock-in) | **+453 bp** | **+643 bp** |

The welfare case for WDT over CGT rests almost entirely here, not in the base comparison. The 0.65 bp base advantage becomes 453 bp once the realisation decision is endogenised. This is an order-of-magnitude shift.

**Flagged issue — Table WFR.8:** The caption states "lock-in cost declines as T increases" but the numbers increase monotonically (T=1: 265 bp → T=20: 529 bp). The numbers are likely correct. Economically, more remaining years above threshold means more periods of foregone superior return, so welfare cost of lock-in should rise with T. The caption conflates two quantities: the indifference return r_B* (which correctly converges toward r_A as T→∞) and the welfare cost of lock-in (a different quantity). Both can be right simultaneously — they are measuring different things. **Requires investigation and correction before paper finalisation.**

### 3.5 Heterogeneous agents (Module 4)

**CEW by tier (progressive WDT):**

| Tier | CEW |
|---|---:|
| Poor | −0.6832% |
| OK | −1.0246% |
| Good | −1.4369% |
| Great | −1.9344% |

Progressive WDT is a deliberate welfare transfer from Great to Poor. On any social welfare function weighting lower-wealth agents at least equally, progressive WDT dominates all alternatives.

**Concentration path (Great/Poor ratio at N=73 — to be rerun at N=30):**

| System | Final ratio |
|---|---:|
| Progressive WDT | 174× |
| Symmetric WDT | 4,033× |
| Income tax | 4,644× |
| Stock wealth tax | 10,483× |
| Consumption tax | 10,483× |

Critical decomposition: **the flat WDT produces 4,033× concentration. The progressive WDT produces 174×. Accrual basis alone does not moderate concentration. Progressivity does.** This distinction must be explicit in the paper. It has direct implications for Governing Council calibration (open register item #17).

**Envelope binding:** The lifetime contribution envelope binds for Poor and OK tiers in early years (1947–1952 and 1947–1949 respectively). This means their symmetric treatment of gains and losses is constrained during adverse sequences. The paper cannot describe progressive WDT welfare for these tiers as if the mechanism were unconstrained. This finding also bears on open register item #18 (SRR floor calibration implication of mild-overstatement equilibrium) — under the mild-overstatement equilibrium, refund exposure is larger than the honest-declaration baseline, so binding may be more frequent or severe.

---

## 4. The paper's core argument

The WFR paper is not claiming WDT wins an efficiency tournament. It is claiming:

1. At revenue equivalence, mechanical welfare differences between tax systems are small (≤20 bp) when behavioural distortions are suppressed. No existing system dominates on base properties alone.

2. The differences that matter emerge from distortions: realisation-based systems impose large lock-in costs (453 bp for CGT); flat-rate systems allow heterogeneous returns to compound into extreme concentration; no existing system shares return risk symmetrically.

3. Progressive WDT is the only instrument in the tested option set that simultaneously: (a) shares return risk symmetrically, (b) eliminates realisation lock-in by construction, (c) is progressive without being a stock wealth tax, and (d) moderates concentration compounding under heterogeneous returns.

4. This is why the existing fiscal literature's compromise framing persists: every instrument under comparison makes at least one of the four choices that forecloses at least one welfare dimension. The WDT escapes that constraint set.

**The paper's contribution to Items #1, #2, #3:** The first formal evidence that a progressive accrual-basis tax with symmetric loss treatment dominates the existing option set across all measurable welfare dimensions, subject to the stated model limitations.

---

## 5. Welfare ranking — summary statement

**Progressive WDT dominates all alternatives on all dimensions the model measures.**

The ranking of existing systems the model produces:

$$\text{Income tax} > \text{CGT (no lock-in)} > \text{CGT (with lock-in)} \approx \text{Stock wealth} \approx \text{Consumption tax}$$

But this ranking collapses under distributional scrutiny: income tax "wins" the single-agent comparison and produces 4,644× concentration over 73 years. The existing literature's impasse is confirmed — systems that perform best on efficiency tend to perform worst on distribution, and the literature has had no instrument that holds both.

---

## 6. Theoretical alternatives not modelled

The following were reviewed and none is expected to outperform progressive WDT on all four dimensions simultaneously.

**Retrospective CGT (Vickrey 1939):** Eliminates lock-in by charging interest on deferred liability. Probably sits between income tax and WDT. Fails on risk-sharing (no symmetric refund).

**Mark-to-market accrual tax:** Structurally close to WDT but without the symmetric refund — losses reduce future bills but the state does not refund. Worse than WDT in loss states.

**Risk-free return method / RFRM (Norway):** Taxes deemed risk-free return on asset value regardless of actual return. Zero risk-sharing. Welfare similar to stock wealth tax or worse.

**Lifetime capital receipts tax (Mirrlees):** Aggregates inheritance, gifts, and capital gains over a lifetime. Retains lock-in during holding period. Requires significant model restructuring to test.

**Land value tax:** Performs well on efficiency (inelastic supply) but narrow base, no risk-sharing, doesn't reach financial wealth.

**Progressive expenditure tax (Kaldor/Andrews):** Fixes the regressivity of flat consumption tax. Still doesn't reach accumulated wealth that is never spent — the core failure at WDT-relevant wealth levels.

**Strengthened IHT (no reliefs, full aggregation):** Captures some of what WDT reaches but timing is radically different. Lock-in persists during holding period. No risk-sharing.

**Structural conclusion:** All alternatives make at least one of: (1) realisation trigger → lock-in, (2) no symmetric refund → fails D-M, (3) flat rate → fails on concentration, (4) narrow base → misses key wealth categories. The WDT's combination of accrual basis, symmetric refund, and progressive rates occupies a position no single alternative reaches.

---

## 7. Model refinement required before paper drafting

The following are identified as requiring attention before results can be treated as paper-ready.

**Priority 1 — Reframe concentration results at N=30.** The 73-year figures are technically correct but will be questioned on horizon grounds. Rerun or reframe at N=30 canonical. Confirm the directional result holds (expected); report N=30 as the primary result with N=73 as a sensitivity or appendix item.

**Priority 2 — Audit WFR.8 (lock-in cost vs holding period).** Caption and numbers are inconsistent. Distinguish clearly between (a) indifference return r_B* as a function of T, and (b) welfare cost of lock-in as a function of T. Correct the caption. Confirm which quantity the model is computing.

**Priority 3 — C2 standalone test.** The net-worth base vs asset-return base test (leverage extension) is in the Module 2 code but does not surface as a clean standalone result in the appendix tables. Either add a dedicated table or explicitly state C2 is not separately quantified at the tested parameters.

**Priority 4 — Envelope binding implications.** Clarify in the paper that the progressive WDT welfare result for Poor and OK tiers is produced under an envelope constraint, not an unconstrained symmetric mechanism. Connect to open register item #18.

**Priority 5 — WFR.9 audit.** The lock-in result is large enough (453 bp) that the construction of the full welfare comparison table needs to be verified independently before it is cited as the paper's primary result.

**Lower priority — C3 framing.** The intertemporal rate asymmetry result is correct and should be reported as a quantitatively minor finding, not suppressed. The paper should say: "C3 exists and is measurable; at canonical parameters it is small relative to C1 and the lock-in effect."

---

## 8. Paper narrative structure (proposed)

The results support a sequential argument that gets progressively richer:

1. **Baseline** — mechanical welfare differences are small; no existing system dominates on base properties
2. **Risk sharing** — flat WDT satisfies D-M exactly; this is a risk-sharing result, not yet a welfare result
3. **Progression** — progressive rates introduce redistribution that dominates the D-M deviation cost; welfare improves for the representative agent
4. **Lock-in** — endogenising the realisation decision produces the dominant welfare result; WDT advantage grows from 0.65 bp to 453 bp
5. **Heterogeneous returns** — progressive WDT dramatically moderates concentration compounding; accrual alone is insufficient; progressivity is the instrument
6. **Synthesis** — progressive WDT is the only system in the tested option set that escapes the efficiency-distribution trade-off that makes the existing literature's compromise framing unavoidable

---

## 9. Cross-paper connections to flag in the WFR paper

- **LR.A §2.1–2.3:** WFR closes items #1, #2, #3 — state explicitly
- **Open register item #17** (τ₀ × W_min joint surface): The concentration decomposition (flat vs progressive WDT) is direct empirical input to this calibration decision
- **Open register item #18** (SRR calibration implication): Envelope binding for Poor/OK tiers is evidence bearing on this item
- **RATES pre-behavioural caveat:** WFR results are also pre-behavioural; the two papers share this stated limitation and should cross-reference it
- **ENV §2** (mild-overstatement equilibrium): Refund exposure under mild overstatement exceeds the WFR baseline; the WFR welfare results for loss states should be read as a lower bound on refund commitment
- **SWEEPS §7.1** (cross-dataset tension): The WFR concentration decomposition shows why τ₀ is the dominant parameter for distributional outcomes, reinforcing SWEEPS's identification of τ₀ as the primary calibration decision

---

*End of planning backbone. Next step: model refinement (N=30 reframe, WFR.8 audit, C2 table, envelope clarification, WFR.9 verification) before paper drafting begins.*
