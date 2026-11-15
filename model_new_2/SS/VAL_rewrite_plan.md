# VAL rewrite plan (P6)

Status: plan only, nothing drafted. Written 4 Oct against `5_Valuing_Wealth.md` (v1.09), `5a_Valuing_Wealth_Mathematical_and_Simulation_Appendix.md` (v1.08), the finished VALGEN set (G1–G13 pairs, build log of 3 Oct) and `VAL_tables_figures_plan.md`.

Your three instructions, taken as fixed:

1. The main paper keeps its structure. New subsections are allowed.
2. The appendices are open: full rewrite, new appendices allowed.
3. Drafting order is figures → captions → placement → prose built around the captions.

---

## 1. What the new evidence does to the paper's claim

The current paper argues one thing: the state need not know true value, because declared values carry consequences. Its evidence is single-life, constant α, Route C only (the "tolerant zone", α ≈ 0.8–1.5). The VALGEN work tests a different and harder claim: **no strategy has unbounded benefit, and the conventional self-declared tax does.** Results to carry honestly:

| Result | Where it sits against the current text |
|:--|:--|
| Conventional flat self-declared tax: gain rises without bound as α falls (+58.2% at α = 0.01). | New. This is the headline (G12). |
| Base rule (`units/allow/off`) at λ = 0 still reaches +45.8% at α = 0.01. | **Weakens** the current claim that Route C dilution alone deters understatement without audit. |
| Candidate rule (`units_and_value/reset/on`) at λ = 0 reaches +4.1%. | Supports "bounded", but needs verification (λ) and the corrective auction on C and D. |
| Candidate fails G1 (gain ≤ 1%) at λ ≤ 2%; passes at 5% and 10%. | New limit. λ_base = 5% is a placeholder. |
| G3 (state stake within ±2%) fails at every λ for every rule; nearest miss −2.1% (λ = 5%), −2.3% (10%). | New limit. Show it. |
| G2 (honest shock cost) is exactly 0.000% for all rules. | New, clean. |
| Search is a lower bound (428 strategies), one parameter point, failed assets not modelled. | Caveats the figures must carry. |

Three things follow before any prose is written:

- **The abstract and §15 overclaim against this evidence.** "Dissolved, not merely managed" and "no auction backstop needed on Route C" do not survive the base-rule result. The rewrite has to say what the candidate rule set adds and what it needs (verification at λ ≥ about 5%).
- **Spec conflict.** §4.3, §5 and Appendix E.3 say Route C has no auction backstop. The new model applies the corrective auction to Routes C and D (rule `dauc`). Either the specification changes (and §4.3, §11, E.3 change with it) or the model is re-run without it. This is a mechanism decision, not a drafting one.
- **Rule set.** The paper currently specifies the base rule only. The candidate adds a unit cap with a value cap, reset on downward verification, and the auction. The paper must say which rule set it is proposing (decision D1).

---

## 2. Main paper: keep §1–§15, add subsections

I propose **appending new subsections inside existing sections and not renumbering existing ones.** Other papers cite VAL by section (SWEEPS, SWEEPS.A, RATES, WFR §6.1.3, ENV §9.2, GOV.B §G, CLOSE §4.1, CORP, BEHAV.A, PHASE1 §5.4, JUR). Insert-and-renumber is possible but needs a full cross-reference audit (wdt-formatter against `contents.yml`). Decision D4.

| Section | Change | New figures (proposed) |
|:--|:--|:--|
| Abstract | Rewrite around the bounded-gain claim and its conditions. | none |
| §1 The Valuation Problem | Keep the framing. Add **§1.1 The claim and how it is tested**: conventional vs WDT contrast, then the caveats up front. | **G12** (headline) |
| §2 Asset Classification | Unchanged. | none |
| §3 Assessment Windows | Unchanged. | none |
| §4 Four Routes | Fix §4.3 per D2. Add one paragraph: routes are tested together as a family portfolio. | none |
| §5 Self-Balancing Mechanism | Keep §5.1–5.3. Rewrite §5.2 around units conserved and the in-kind cap. Add **§5.4 Where dilution alone is not enough** (base-rule weakness at λ = 0). | G1, G2, G5 (or appendix) |
| §6 Non-Fungible Assets | Keep. Add reset-interval sensitivity to §6.4. | G4 |
| §7 Declaration Strategy | Keep §7.1–7.5 as the **single-life** analysis, trimmed. Add **§7.6 Family-level search**, **§7.7 Rule-set ablation and verdicts**, **§7.8 Growth and loss-year robustness**, **§7.9 Where the design does not pass**. | G7, G8, G9, G11, G10, G13, G3 |
| §8–§10 | Unchanged apart from any D2 consequences in §9–§10. | none |
| §11 Auction | Add the verified-share-by-year result to §11.3. Corrective auction on C if D2 says so. | G6 |
| §12–§13 | Unchanged. | none |
| §14 Limitations | Rewrite §14.2 (the "empirical unknowns" now include λ). Add the G3 near-miss and the failed-asset gap to §14.4. | G10 cross-ref |
| §15 Conclusion | Rewrite to the new claim and its limits. | none |

Proposed main-text figure budget: **G12, G7, G8, G10, G13** (five), plus the old Fig 5 rate function. Everything else goes to the appendix. G1–G6 are mechanism evidence a reader can take on trust once the verdict figures are seen.

Single-life material (Figs 5.2a/b, 7.1a–d, 7.2a/b, 7.3) moves down to an appendix or is cut to one or two representative figures. That is a placement decision (step 2 of your drafting order), not made here.

---

## 3. Appendices: proposed set

Current VAL.A has A (maths), B (method), C (tables C.1–C.12), D (mechanism cases), E (route specs), F (reporting). Proposal:

| Appendix | Content | Basis |
|:--|:--|:--|
| **VAL.A** Model and rules | A: family model (generations, heir, routes, λ, rule-set key, verdicts G1–G3 defined). Single-life propositions kept in a short §A.x. B: methodology, strategy library, parameter table generated from the TOML. | rewrite |
| **VAL.A tables** (C) | New G-tables (`Table G1…G13`) plus the gap tables. Old C.1–C.12 frozen as a "single-life reference" block, numbering unchanged (cited elsewhere). | extend |
| **New: conventional baseline and leak checks** | Flat self-declared tax calibration, no-tax ceiling, why the ceiling is a check not a result, no audits modelled. | new |
| **New: strategy search and the G3 near-miss** | 428-strategy library, families, lower-bound caveat, worst conflicts, near-miss table. | new |
| **New (optional): heir view** | Residual gain at low λ (up to +4.4% at λ = 0): late understatement before death, heir inherits declared basis (D4/D6). Needs a core view first. | needs core work |
| D Mechanism cases | Keep; add cases for corrective auction on C and the reset rule if adopted. | extend |
| E Route specs | Update E.3 (D2) and add the rule-set fields. | edit |
| F Reporting | Unchanged. | keep |

Naming: VAL.B is the worked-examples companion (5_5 script, not in this Project). Whether the new appendices become VAL.C and VAL.D, or sections of VAL.A, is decision D3. It changes the glossary pointer paragraph and the site build.

Orphans to resolve at the same time: the old pipeline generates C.12b (state tolerance) and C.13 (uncertainty) tables and Figs 7.4–7.7, but neither VAL.A nor the paper body uses them. Retire or place.

---

## 4. Drafting order (your sequence, with mechanics)

**Phase 0. Freeze.** Re-run `valgen_core.py` once on final parameters. Tag the JSON. Open decisions D1–D3 settled first because they change numbers or specs.

**Phase 1. Figure captions.** One caption per figure, built from the JSON, not typed:

> Figure Gn: what is plotted. The reading in one sentence. Parameters (λ, T, G, N_val, α range). Caveat. Source: Table Gn.

I propose a `VAL/5_9_VALGEN_captions.py` that writes `OUTPUTS/VAL/captions.md` with every number pulled from the JSON and p. Reason: the current revision history is mostly hand-typed numbers going stale (v1.03 to v1.07). Same approach for a **numbers register** (`OUTPUTS/VAL/valgen_numbers.md`: key, value, source path) that prose cites by key. This is a proposal; say if you'd rather type them.

**Phase 2. Placement.** A placement matrix (figure → section → main or appendix → one-line job). The section 2 table above is the starting draft. You decide; I do not.

**Phase 3. Prose around captions.** For each section: caption order fixed → one claim sentence per figure → connecting prose → caveats. Section by section in this order: §1.1 and abstract last, §7.6–7.9, §5.4, §6.4, §11.3, §14, §15. Use `wdt-doc-coauthoring` per section, `wdt-laconic` after each.

**Phase 4. Appendices.** Methods and rules first (they define terms prose uses), then tables, then mechanism cases and route specs.

**Phase 5. Consistency.** `wdt-formatter` cross-reference audit against `contents.yml`; `wdt-guru` check on downstream papers; `wdt-reference` for new citations (corrective-auction and Harberger literature, the UK tax-gap figure).

**Phase 6. Release.** Revision history entry, version bump, site build (`wdt-web`).

---

## 5. Known inconsistencies in the current text (fix by regeneration, not by edit)

| Item | Where |
|:--|:--|
| Plateau inflection g ≈ 17.3% vs 19.1% | A.2.3, A.5.4, §7.2b, §14.2 |
| N-crossings ≈ 19.5–20.8 (text) vs α = 2.0 at N ≈ 30, α = 1.8 at N ≈ 32 | A.2.4 vs A.5.6 Proposition 4 row |
| 2000 series mean g 6.0% (main) vs 7.05% (C.10 preamble) vs 5.99% (C.10.2) | §7.1, C.10 |
| C.10.1 honest TW 65.05 / Net 6.99 vs C.10.2 N = 30 row TW 89.36 / Net 10.86 | C.10 |
| C.1 text says α = 0.1 exceeds 100% at g ≈ 23–24%; table shows 6.21% at g = 25.4% | C.1 |
| C.1 text says mild overstatement has no reversal; table shows positive values from g ≈ 13.9% | C.1 vs A.5.4 |
| Plateau ceilings 38/26/7/3% (§7.2b) vs 98/70/24/6% (C.9), unlabelled bases | §7.2b, C.9 |
| Refund protection 93.78% / 88.30% (main) vs 93.76% / 88.27% (C.6) | §7.4, C.6 |
| Figure numbering: revision notes cite Figure 5.3 and 7.4–7.6 renumbering; the body has neither; "Figure 10" for 7.1d | throughout |
| "±2%" means per-taxpayer outcome in §7.1 and state-stake tolerance in G3 | name collision to resolve in prose |

The UK tax-gap comparison (4–5%) in §7.1 is unsourced in the text; check or replace with the conventional-baseline comparison.

---

## 6. Claims inventory (keep / re-test / withdraw)

| Claim in current paper | Status against new work | Proposed action |
|:--|:--|:--|
| Valuation accuracy is not a precondition of administration (institutional argument) | Unaffected | Keep, §1 and §15 |
| Understatement is deterred by dilution on Route C without audit | Weakened (base rule +45.8% at λ = 0) | Reframe; §5.4 |
| Corrective auction is Route D only | Conflicts with model | D2 |
| Tolerant zone α ≈ 0.8–1.5 | Single-life, base rule; not retested at family level | Keep as single-life result; do not lead with it |
| Aggressive overstatement is self-limiting (N-crossing) | Not retested; G12 axis stops at α = 1 | Keep in appendix, flagged conditional on τ_0 |
| Mild upward bias α ≈ 1.1 | Not tested | Keep as conditional prediction or move to §14 |
| Portfolio composition anchors α (§7.5) | Consistent; G5 adds the C-share result | Keep, add G5 |
| Routes do not interact | Tested by G3 | Keep, cite G3 |
| Failed assets accepted as a boundary | Still not modelled | Keep, §14.4 |

---

## 7. Decisions needed from you

- **D1. Which rule set is the paper's mechanism?** Base, or the candidate `units_and_value/reset/on`. The candidate fails G1 at λ ≤ 2% and G3 at every λ. This decides how §5, §6.4 and §11 read.
- **D2. Corrective auction on Route C.** Change the specification (§4.3, §11, E.3) to match the model, or re-run without `dauc` on C.
- **D3. Appendix naming.** VAL.C / VAL.D, or sections of VAL.A. Whether VAL.B stays as is.
- **D4. Numbering.** Append new subsections (cross-references stable) or insert and renumber (full audit).
- **D5. Old figures.** Which of 5.2a/b, 7.1a–d, 7.2a/b, 7.3 stay in the main text; what happens to the unused 7.4–7.7 and C.12b/C.13 outputs.
- **D6. Thresholds.** Whether 1% / 1% / ±2% stay as the verdict thresholds; they decide the pass/fail picture.
- **D7. Heir view.** Whether to build the extra core view for the residual late-understatement gain.
- **D8. Captions and numbers generated or typed** (section 4, Phase 1).

Downstream papers to re-check after the rewrite: SWEEPS, SWEEPS.A (plateau, N-crossing), RATES, WFR §6.1.3, ENV §9.2 (SRR floor and α bias), GOV.B §G, CLOSE §4.1, CORP, BEHAV.A, PHASE1 §5.4.
