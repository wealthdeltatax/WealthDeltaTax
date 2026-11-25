# WDT framework and consistency checks

Interpretive lens for the guru. Use it when a question has no direct answer in `site/pages/Project-Map.md`, when papers pull in different directions, or when a new idea needs checking. It is the author's own synthesis, not quoted from a paper.

## The author's framework

This is the interpretive lens behind the WDT project. Pieces surface in MF and WP §1.1 but it isn't stated as a unified framework in any single paper. Use it when a question doesn't have a direct answer in the Project Map, when papers pull in different directions, or when the user proposes something new and wants to know whether it fits.

### The governing sentence

> "The legitimacy of concentrated private power depends on its continued compatibility with broad democratic human flourishing."

Everything else is downstream of this. The WDT is not justified by revenue, efficiency, or fairness in the abstract — it's justified by what happens to democratic flourishing if extreme concentration goes unmanaged.

### Three tiers

**1. Descriptive** (empirical claims, not value judgments)
- Wealth concentration compounds into institutional power, which eventually rewrites the rules of the systems it operates within. This is ordinary mechanics of influence and compounding advantage, not conspiracy.
- Democratic governments are structurally mismatched against long-duration concentrated capital. Electoral mandates are short; patient capital is not.
- Purely adversarial taxation fails operationally. Capital is mobile. A system that only extracts gives its targets every incentive to exit, restructure, or politically dismantle it before it can extract enough to matter.

**2. Normative** (the axioms — not derived from anything further back)
- Individual humans are the only legitimate moral subjects of a tax system. Corporations, trusts, and funds are instruments through which human wealth is organised; they have no welfare of their own. *This is* the axiom the whole project claims to derive from.
- The goal is broad democratic flourishing, not mechanical tax efficiency. A WDT that works perfectly as engineering but leaves ordinary people structurally subjugated has failed on its own terms.

**3. Strategic** (how to design, given the above two tiers)
- Cooperative mechanisms outlast coercive ones. Align incentives before reaching for enforcement.
- The system must tolerate imperfect compliance without collapsing. A design that only works under near-universal honesty has assumed away the avoidance problem, not solved it.

### Priority order when tiers conflict

The normative axioms (individual-as-subject, democratic flourishing) are load-bearing and shouldn't be traded away. The strategic principles are instrumental — how you *get* to the normative goals given the descriptive constraints. If a strategic choice stopped serving the normative goal, the framework says: change the strategy, not the goal.

**Diagnostic**: if a proposed design choice only works by treating a corporation as the morally relevant subject, by leaning on pure coercion, or by assuming the system needn't survive anyone's incentive to defect — it's drifting from the framework, even if it's individually well-argued.

The named compromises in MF §9 (per Project Map §2) are the project's own model for how new trade-offs should be framed: name the trade explicitly rather than disguising it as a natural extension of the theory.

---

## Checking consistency of new ideas

When the user proposes a new mechanism, a tweak, or asks "would this fit," check in order:

1. Does it contradict a settled design position (per Project Map)? Or does it touch something genuinely still open (§27)? If open, say so — there's no settled position to contradict.
2. Does it sit with the named compromises in MF §9, or does it quietly re-open one of those trades without acknowledging it?
3. Does it serve the normative tier, or does it only work by treating a corporation as the relevant subject, leaning on pure coercion, or assuming away imperfect compliance?

Say plainly where an idea fits, where it's genuinely new territory, and which of the three checks it conflicts with, if any. The point is to be a useful check, not a rubber stamp or a wall of objections.

---

## Things to get right that are easy to get wrong

- **"Open question" and "named compromise" are different categories.** A named compromise (MF §9) is a trade-off the project has already accepted and stated explicitly. An open question (§27) is something nobody has answered yet. They can overlap — the exemption threshold is both — but they're separate facts.


- **The mild-overstatement equilibrium is NOT a finding (retracted 2026-11-20, author).** The old papers' behavioural centre near alpha 1.1 is a model-implied prediction from the refund asymmetry, not an estimate; no source measures it and none tests it (`research/notes/080r-declared-alpha-evidence.md`). The evidence that exists (Sweden, Colombia) shows understatement where no third party reports value, with a truthful minority. Do not repeat the claim; the tolerant zone and the declaration curve (M7c, M7d, O7) stand as model results.

- **The ten enumerated structural clauses in GOV §5.2 are load-bearing** — they define the properties the system must preserve to remain the same kind of tax. Any question about whether a design change is compatible with the WDT must be checked against these ten, not just against individual paper positions.

- **τ_prov and τ_h are distinct optimisation problems** (CORP.A §B.1 and §B.2 respectively) — not the same parameter. τ_m is a ceiling for τ_h calibration, not its anchor. τ_0 is the dominant fiscal parameter at canonical k=0.001.

- **RATES's revenue figures are pre-behavioural.** The modelled coverage ratios are a starting point, not the answer. The absence of behavioural modelling is the paper's own stated principal source of overstatement.

- **The SRR and LRR are separate reserves on different timescales** within the SWF. SRR fill (3 years, invariant across all 73 start years) makes the refund guarantee credible; LRR fill (up to 29 years at the worst-case 2007 start) makes full Phase Two viable. These are distinct milestones gating distinct Governing Council decisions.

- **The Open Questions Register (§27) has four sub-categories.** Items not listed there are settled. Before calling something unresolved, check §27. The register currently covers items grouped as: confirmed literature gaps (#1–3, #7–9); Phase One empirical questions (#4–6, #13–16, #18, #29–30); MACRO tasks (#11–12); and Governing Council calibration parameters (#10, #17, #19–21, #24) — plus jurisdiction-specific items (#22–23, #25–28 in SCOPE).

- **The SWEEPS cross-dataset tension is the most consequential calibration decision.** Higher τ_0 accelerates LRR capitalisation and raises coverage ratios; it simultaneously weakens and eventually eliminates the self-limiting correction for aggressive overstaters (disappears above τ_0 ≈ 29–32%). No setting simultaneously optimises both. This is item #17 in the open register (resolvable without Phase One data, via the τ_0 × W_min joint surface not yet generated).


- **CLOSE unified the position-closure theory.** Death, exit, threshold fall-through, and bankruptcy are treated as structurally the same event. The bridging facility (CLOSE §5) decouples physical departure from settlement completion. The re-entry rule carries the lifetime contribution envelope forward across all closures.

- **FM states a binary.** Any jurisdiction that has concluded the WDT's properties are likely true faces commit-or-suppress, with no stable middle option. Partial adoption is not available because removing the symmetric refund collapses the valuation architecture and breaks the Domar-Musgrave logic.

- **MOD distinguishes Category 1 (infrastructure with independent justification) from Category 2 (constitutively WDT-specific mechanisms).** Accretion reaches the Category 1 boundary and stops. Category 2 mechanisms require deliberate political commitment.
