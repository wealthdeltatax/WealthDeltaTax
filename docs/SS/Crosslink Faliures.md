I ran a full mechanical pass over all 32 papers in `/mnt/project/` — 1,527 section-level cross-references, 891 unique source→target pairs — then hand-checked the ones where the target exists but the claim didn't look right. Findings below in seven groups.

---

## 1. Dead targets (link resolves to nothing)

27 instances, 22 distinct.

| Source | Ref | Problem |
|---|---|---|
| CLOSE §3 | `BEHAV §8.7` | BEHAV §8 now has only §8.1–§8.2 after the v1.03 restructure. Emigration objection is **BEHAV §9.1** |
| CLOSE §3 | `CLOSE §9` | CLOSE has no `# 9` heading (see §3 below) |
| LR.B §18 | `CLOSE §9` | same |
| MF §8 | `BEHAV §8.11` | doesn't exist post-restructure; content is **BEHAV §8.1** |
| INST §5.4 footnote | `BEHAV §8.11` | same |
| PHASE1 §6.3 | `BEHAV §12.3` | BEHAV §12 is the conclusion, no subsections |
| PHASE1 §6.3 | `BEHAV §12.1` | same |
| BEHAV.A rev. history | `BEHAV §8.12–§8.13` | historical note, but now unresolvable |
| CORP.A §E.9 | `CORP §5.10` | CORP §5 ends at §5.6; intended **§5.6** |
| FAL §4.4 | `GOV §4.2` | GOV §4 has no subsections |
| INST §4.2 | `GOV §4.2` | same |
| INST §5.3 | `GOV §4.2` | same (3 occurrences across INST) |
| INST §7.2 | `ENV §3.1` | ENV §3 has no subsections; intended **ENV §4.1** |
| INST §9.3 | `JUR §5` | JUR ends at §4 |
| POL §1 | `POL §9.7` | POL §9 ends at §9.5; content is in **§9.4** |
| VAL glossary, §4, §12.1 | `VAL.A §D`, `§E`, `§F` | **VAL.A contains only §A–§C.** See §3 |
| VAL.A §B.5 | `VAL.A §D` | same |
| VAL.B Reader's Guide | `VAL.A §F` | same |
| WFR §4.3.5 | `WFR.A §E.2` | WFR.A has §E.2.1/§E.2.2 but no §E.2 heading |

---

## 2. Links that resolve but point at the wrong content

These are the more damaging category — they look fine to a checker and mislead a reader.

**Systematic: the "reciprocal partnership" attribution.** Five papers attribute the working characterisation of the state/taxpayer relationship to GOV.A §E. GOV.A §E is *Governance Decay: Four Sub-Forms* (§E.1 definitional drift, §E.2 procedural calcification, §E.5 the correct partition). Nothing in GOV.A §E discusses reciprocal partnership.
- MF glossary → `GOV.A §E`
- MF §7 → `GOV.A §E.5`
- WP §3.5 → `GOV.A §E.5`
- LR.B §4 → `GOV.A §E.5`
- POL §5.4 → `GOV.A §E.2`
- CLOSE §3 → `GOV.A §E.2`

Either the characterisation needs a real home (GOV.A §B.2 on the Allocator redesign is closest, or it belongs in GOV §2/§3) or all six need repointing to MF §7, which is where it is actually argued.

**Individual misfires:**

| Source | Ref as written | Should be |
|---|---|---|
| POL §5.3 | MF's terminal goal `(MF §9.4.1)` | MF §6 (§9.4.1 is "the corporate instrument") |
| POL §5.6 | ten enumerated clauses `(GOV §6.3)` | GOV §5.2 |
| POL §5.2 | raiding the fund "triggers the enumerated clause 6 rebalancing" | clause 4 (SWF sole capitalisation purpose) |
| POL §A.6 | `(MF §9.5)` names the democratic boundary condition | MF §9.4.5 (§9.5 is "no items") |
| LR.B §16 | foundational axiom `(WP §2)`, collective production `(WP §3)`, wealth as power `(WP §4)`, opacity `(WP §5)`, terminal goal `(WP §6)` | **MF** §2/§3/§4/§5/§6 — wrong paper code throughout |
| JUR §1.5.2 | "As `(JUR §4.2)` establishes, the VOA's capacity is adequate" | §4.2 is the OBR Phase One item; VOA adequacy is asserted in §1.5.2 itself |
| JUR §1.5.3 | OBR "assigned to Phase One at `(JUR §4.4)`" | JUR §4.2 (§4.4 says "no items") |
| LR.B §15 | `(JUR §4.4)` | JUR §4.2 |
| CORP.A §C, §E.1 | attribution test established in `(CORP §6)` | CORP §7 (§6 is the equity settlement facility) |
| VAL §14.3 | double-counting "resolved by `(CORP §7)`" | CORP §8 |
| CORP.A §D.1 | transitional overlap "addressed in §E.6" | §D.6 (§E.6 is life insurance wrappers) |
| CORP.A §D.4 | "§E.4's prior framing" on compliance functions | §D.3/§D.4 (§E.4 is trusts) |
| VAL §7.1 | worked examples `(VAL.A §C.1)` | VAL.B §N |
| VAL §7.4 | "(VAL.B §J), (VAL.B §L), and (VAL.B §M) … respectively" | three refs, two antecedents — the Route D entry-basis case is §M |
| VAL §3.1 | annual returns submitted "to the **Allocator**" | Allocator is the SWF surplus body (GOV §6.2); VAL §12.1 says reports go to the Valuation Bodies |
| ENV §6 | provisional refund notification `(BEHAV §5.6)` | BEHAV §5.6 is the adviser corps; the intervention set is BEHAV §5.2 / PHASE1 §4.5 |
| ENV §7 | "the appropriate home is GOV.B's SWF operational section `(GOV §6.3)`" | GOV.B §E.7 |
| PHASE1 §4.2 | "measurement design in `(PHASE1 §4.3)`" | §5.2 |
| PHASE1 §4.4 | "the `(PHASE1 §4.5)` measurement design tracks" | §5.4 |
| PHASE1 §5 preamble | `(BEHAV §11.1)` specifies phase-appropriate interventions | BEHAV §10 (§11.1 is formal modelling gaps) |
| FAL §9.1 | membrane investment `(BEHAV §10.1, §11.1)` | §11.1 wrong; §10.1/§10.4 |
| INST §8 | `(BEHAV §11.1)` | same |
| SCOPE §3.1 #4 | `(BEHAV §4.1)` assigns to cluster 1 | PHASE1 §4.1 |
| SCOPE §3.1 #6 | `(BEHAV §7)` assigns to cluster 5 | PHASE1 §4.5 |
| SCOPE §3.1 #29 | `(BEHAV §10.2)` | BEHAV.A §B |
| RATES §3, §8.3 | £1,157b expenditure base `(JUR §2.2)` | JUR §2.3 / §3.2 (§2.2 is tax revenues) |
| WFR §2.1, Fig 4.1a | logistic schedule `(RATES §3)` | RATES §4 |
| WFR §2.1 | N=30 inheritance-crossing rationale `(RATES §4)` | WP §5.1 |
| WFR §7.4 | N=73 concentration run "committed to `(WFR.A §F)`" | WFR.A §F is the parameter reference table — the run is not there |
| ADD §9.2 | consumption multiplier cluster `(PHASE1 §4.1)`, `(§5.1)` | §4.1/§5.1 are the cooperative-architecture cluster; the multiplier is ENV §9.2.1 |
| ADD glossary | tolerant zone "defined formally in `(VAL.A §A.5)`" | VAL.A §A.2.5 / §A.6 |
| FAL §1.3, §2 | "the open questions register in `(WP §9)`" | WP §9 is Limitations; the register is the external 0.0 doc |

**SWEEPS ↔ SWEEPS.A table keying is broken end to end.** SWEEPS.A Part 1 (§A.1–§A.8) describes its own tables as "A.1.1–A.1.6", "A.4.1–A.4.4", "A.8.1–A.8.6" — every one of those tables actually sits at §B.1–§B.8. §A.4 (W_min) opens "A.8 contains six C.1 heatmaps"; §A.8 (k×V₀) opens "A.7 is a two-dimensional grid". Headings §A.1–§A.4 are labelled "SWEEPS.R" while describing SWEEPS.V heatmaps. Inbound from SWEEPS inherits the damage:

| SWEEPS ref | Actual location |
|---|---|
| "Table B.3.3" for τ₀ N-crossings (§3.1) | B.6 |
| "Table B.4.3" for plateau ceilings (Fig 4.1b) | B.2.1–B.2.4 |
| "Table B.2.4" for tolerant zone across N (Fig 2.2b) | B.2.4 is the τ_m = 80% heatmap |
| "Table B.2.6" (Fig 2.3) | does not exist |
| "SWEEPS.A §§B.6–B.7" for srr_ratio / lrr_years (§8.3, §11) | §C.6 / §C.7 — Figures 8.3a/8.3b get this right, the prose doesn't |
| "Fig S3.1a/b/c", "Fig S4.2", "Fig S4.3" (SWEEPS ×3, VAL.A ×5) | SWEEPS.A §B.9 indexes these as **SS**3.1a, SS4.2, SS4.3 |

---

## 3. Structural problems that break or will break inbound links

- **VAL.A is missing §D, §E and §F.** The file contains §A (model), §B (simulation), §C (tables) and stops. VAL.A's own revision history edits "§D.6", "§E.4", "§E.4.1". Eight inbound references assume §D (mechanism cases), §E (route specification tables) and §F (annual reporting requirements), including VAL §4 ("full route specifications… are in VAL.A §E") and VAL §12.1 ("full specification of reporting requirements is in VAL.A §F"). This is the largest single gap in the link graph.
- **CLOSE has no `# 9` heading.** §9.1–§9.5 sit visually under §8 Principal Objections. LR.B §18 and CLOSE §3 both link to `CLOSE §9`.
- **POL has two §8.7s** — "The Governance Structure Is Too Radical" and "The Cross-Base Externality Makes the Emigration Risk Unmanageable".
- **SWEEPS.A has two §B.8.5s** — "W_min = £10m" and "N-crossing thresholds by W_min".
- **INST §4 has no §4.1** (jumps from §4 body text to §4.2).
- **WFR.A §E has no §E.2 / §E.3 parents** (only §E.2.1, §E.2.2, §E.3.1–§E.3.4).
- **CORP carries stray drafting text** before §5: *"Before drafting I want to make sure I have the full text of every subsection I'm collapsing… Good. I have everything. Drafting now."*
- **CORP.A §G**: the τ_f row is missing its "Calibration home" cell.
- **Sentence corruption where refs were spliced in** — four places where a cross-reference has eaten the end of a sentence:
  - GOV Abstract: "…argument quality is directly (GOV §1.1) develops this argument…"
  - GOV §4: "They cannot close the drift (GOV §7) returns to this honestly…"
  - GOV §5: "…fixed its vote share at 50% on structural (GOV §4) established that…"
  - POL §4: "…wealth taxes have historically been (POL §5) evaluates the WDT's institutions…"
- POL §5.7 opens "The institutions in (POL §5.1) through (POL §5.7)" — self-inclusive; should be §5.1–§5.6.
- JUR §2.11: "The caveat at (JUR §2.4) and (JUR §2.4) applies in full" — duplicated ref.
- LR.A §2.1 contains "The gap in (LR.A §2.1) is therefore…" — self-reference inside its own section.

---

## 4. Stale links — target moved on since the link was written

- **LR.A is the biggest stale node.** §2.1, §2.2, §2.3 and the §5 gap register still mark gaps 1–3 "Confirmed". WP §9.1 and SCOPE §2 both record them as closed by WFR. Every inbound link to LR.A §2.x now sends the reader to a superseded verdict.
- **LR.B §4, §5, §6** forward notes still say the D-M extension / welfare comparison "has not been accomplished" and point to LR.A.
- **ENV §3** cites "(WP §2.5), with the qualification noted there that formal extension… has not been completed" — WP §2.5 now says the opposite. ENV §9.1 still assigns the D-M and welfare gaps to LR.A.
- **Mild-overstatement drift.** VAL v1.07 and VAL.A v1.07 recharacterised this as a tolerant zone (α ≈ 0.8–1.5) with a *conditional* behavioural centre near α ≈ 1.1, explicitly not a population equilibrium. Still describing it as a settled equilibrium at α ≈ 1.2–1.5: MF §3.3, ENV §2 ("systematic mild overstatement as the equilibrium declaration pattern"), SWEEPS glossary, VAL.A §A.3.2's own design note, SCOPE #18, ADD. All of these cite VAL.A §A.6, which no longer says it.
- **RATES.A §A.6** is still written against the 2007 Balanced scenario (window year 3→29, SSM 21.3% / TCM 27.4%) while RATES's active scenario is 2000 (window year 3→19). RATES §7.1 and §3 both send readers to §A.6 for "the full specification".
- **N = 29 vs N = 30.** VAL.A §B.3's parameter table still reads 29 with prose "the 29-year reference holding period is the canonical horizon", despite revision 1.06 correcting it; SWEEPS.A §A preamble also says N = 29; everything else (VAL.A §C, SWEEPS, WFR, RATES) uses 30.
- **N-crossing figures conflict three ways across cross-cited papers:**
  - VAL.A §A.2.4/§A.5.4/§A.6: α=2.0 at N ≈ 30, α=1.8 at N ≈ 32, crossing disappears above τ₀ ≈ 29–32%
  - SWEEPS.A §B.4.5 / §B.6: 19.5 / 20.0 / 20.8, and crossings present at every τ₀ up to 41%
  - VAL Figure 7.1a: 20 / 21 / 22
  Each cites the others as its source.
- **SWEEPS §1** cites "VAL (v2.7), VAL.A (v3.0), VAL.B (v1.5), RATES (v2.3)". No paper carries those revision numbers.
- **Paper counts:** FM §4 "twenty-one papers"; FAL §1.3, §2, §12 "26 papers"; INST abstract "26 papers". The series is now 32.
- **WFR §2.1 / glossary** date Ver. A as "1950–2022" while WFR.A and every other paper use 1947–2019.

---

## 5. References to papers that do not exist

| Code | Cited by | Status |
|---|---|---|
| **EVAL** | WFR abstract, §1, §2.3, §6.1.3, §6.2, §7.3 | Load-bearing — WFR's entire Category 3 break-even argument is deferred to it |
| **MACRO** | ENV §9.2.3, §9.2.4, §10; SCOPE §4; INST §10.2; FAL; LDW §1.1 | Explicitly framed as a Phase One successor, so forward-referencing is defensible, but no paper says it's unwritten |
| **FAL.A** | FAL §3.2 ("FAL.A is intended to sketch the methodology") | — |
| **ENV.A** | SCOPE §4 ("(ENV.A) sets out what MACRO requires") | — |
| **0.0 / 0.4** | LR.B §1, LR.B §18, CLOSE §9.3, SCOPE §1, plus all `#n` open-question numbers | Unpublished internal registers; readers of the public series can't resolve `#8`, `#16`, `#30`, `#31`, `#32` |

Also: SCOPE uses a hybrid format `(FAL H3 §5.5)` / `(FAL H2d and H5)` mixing hypothesis IDs with section refs — resolvable but inconsistent with the rest of the series.

---

## 6. New crosslinks that should exist

Ordered roughly by how much the absence costs.

1. **LR.A → WFR.** §2.1, §2.2, §2.3 and the §5 register need "closed by WFR §3.2/§4.1, §3–§4, §4.3". Right now the gap register contradicts WP §9.1 and SCOPE §2.
2. **LR.B → WFR.** §4 (Domar-Musgrave), §5 (heterogeneous returns), §6 (welfare comparisons) forward notes; and §3 should point to WFR §4.2.3 for the Arachi engagement.
3. **LR.B → INST, FAL, LDW.** LR.B's forward-note apparatus stops at the original 26. No section routes a reader to the four newest papers.
4. **BEHAV §9.2 content moved to BEHAV.A §D** in v1.03. CLOSE §1.2, PHASE1 §4.3, INST §9.2 and WFR §6.1.3 all still point only at BEHAV §9.2 for the full Agrawal response.
5. **LDW is cited by nothing except SCOPE.** MF §6 (terminal goal), POL §5.3 (labour dividend constituency), ENV §4.6 (household effects), RATES §6.3 and WP §6 all now have a fuller treatment downstream and should say so.
6. **INST is cited by nothing except SCOPE.** POL §3 (three failure mechanisms) and FM §3.2 (suppression) are the two sections INST extends directly; neither points forward.
7. **FAL is cited by nothing except SCOPE.** WP §9 and PHASE1 §7 are the natural inbound points.
8. **VAL / VAL.A → WFR.** WFR builds its Category 3 cost list from VAL's tolerant zone and route architecture; VAL §14 and VAL.A §B.5 have no reciprocal pointer.
9. **RATES → WFR.** RATES §2's burden figures are WFR's revenue-equivalence baseline, and RATES §9.1's formal-modelling-gap note predates WFR.
10. **CORP §6 / §9.5 → GOV.B §H.** GOV.B §H cites CORP §6; the reverse link is missing, so a reader of CORP §6.4's calibration list never reaches the Custodian mandate extension.
11. **VAL §13 ↔ GOV.B §E.3 ↔ CORP §6.** Three distinct SWF-side credit instruments (sovereign liquidity facility, bridging facility, corporate equity settlement facility) with no cross-reference between them. CORP §6.3 distinguishes two of the three; VAL §13 mentions neither.
12. **ADD §10 → GOV.B §E.1/§E.2 and GOV §5.2 clause 4.** The bootstrapping facility's subordination and publication conditions are tested against exactly those provisions but cite neither.
13. **SWEEPS §13.2 → GOV.B §E.2/§E.7.** SWEEPS flags the Custodian mandate amendment as belonging in GOV.B; GOV.B has no inbound note.
14. **GOV §7.5 and RATES §9.5 calibration registers** omit the τ_h ramp parameters (CORP.A §B.2.8) and the five corporate facility parameters (GOV.B §H.5), both of which are Tier 1 Governing Council items.
15. **JUR §2 → LDW §2.** LDW's arithmetic rests on 2025/26 rate schedules, ONS ASHE April 2025 median earnings (£39,039) and the Ofgem October 2025 cap (£1,755) — none of which JUR carries. Either JUR gains the rows or LDW should state that its inputs sit outside the JUR data reference.
16. **MF §4 → LR.B §16.** LR.B identifies Hasen (2017) as independent prior art for the specific wealth-as-power claim MF §4 makes; MF doesn't acknowledge it.
17. **LR.A §2.2 → WFR §5.5.** WFR positions itself in the live Guvenen / Boadway-Spiritus dispute that LR.A §2.2 frames as the gap.
18. **VAL.A §A.6 → BEHAV.A §B.** VAL.A names the absence of a monitoring instrument for the population distribution of α (item #29); BEHAV.A §B specifies the membrane-observable publication architecture that is the closest existing answer.
19. **FM §2 → INST §6.3.** INST adds a second, independent reason the labour dividend can't be stripped out; FM's non-decomposability section only carries the first.
20. **CLOSE §4.4 → GOV.B §E.** Bankruptcy closure puts a refund obligation into an insolvency estate; nothing in the Custodian's mandate addresses it.

---

## 7. Two things worth deciding before you fix any of it

**Numbering convention for appendix parents.** VAL.A, WFR.A and SWEEPS.A each have sub-subsections without a parent heading, which is what produces the dead `§E.2` and `§A.5` style refs. A rule that every cited level gets a heading would remove a whole class of these.

**Whether `(PAPER §n)` refs should ever point at a *paper's* discussion of another paper's content.** Most of the §2 misfires above are this pattern — SCOPE citing BEHAV for a PHASE1 cluster assignment, ENV citing BEHAV §5.6 for an intervention listed in PHASE1, POL citing GOV §6.3 for clauses in GOV §5.2. The convention that a cross-reference points at where something is *established*, not where it is *mentioned*, would catch the rest.

---

Two numbers for scale: 22 of 891 unique links are dead (2.5%), but roughly 40 more resolve to the wrong content — so the real error rate is closer to 7%, and it's concentrated in the SWEEPS/SWEEPS.A table layer, the VAL.A missing sections, and the GOV.A §E attribution.

Want this as a markdown file you can work through paper by paper?