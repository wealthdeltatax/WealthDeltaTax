# Content ledger: section dispositions (brief 013g, stage B)

One row per section (or run of sections with one disposition) of the old papers. Generated from the dispositions the guru recorded; edit this file by hand from now on. Summary, totals and coverage: `ledger.md`. Brief 025w (2026-11-17) reassigned every target to the shortcodes and split S4, S6, S11 and S12; a row it moved carries a `[025w: ...]` note.

Columns: **Sec** old section number; **Words** old words in the row; **Disp**: K keep to the target, M merge into the target (overlaps another kept section), D drop as redundant, SA standalone paper, AR archive, DL move to the data layer; **Target**: hub section H0 to H7, a spoke shortcode (`shortcodes.md`; the planning ids S1 to S12 retired, `ids-map.md`), a standalone paper, or the data layer; **Model**: Y the claims need model numbers, P partly, N no; **Demands**: output IDs from `outputs.yml` the claims need, or `NEW:` tags for outputs it lacks (defined in `ledger.md`).


## 1_Wealth_Delta_Tax_Whitepaper (15078 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 119 | AR | - | N | - | front matter; the hub writes its own summary (H0) |
| rev | Revision History | 477 | AR | - | N | - | front matter; the hub writes its own summary (H0) |
| abs | Abstract | 221 | AR | - | N | - | front matter; the hub writes its own summary (H0) |
| gloss | Glossary | 276 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. Introduction | 300 | M | H1 | N | NEW:H1 | opening statement of the problem (unrealised gains treated as a non-event); H1 needs data hooks |
| 1.1 | 1.1 The Cooperative Basis of the Design | 363 | M | FAIR | N | - | cooperative basis; duplicates MF 7 |
| 2.1 | 2.1 The Haig-Simons Definition and the Comprehensive Income | 279 | K | LIT | N | - | literature context; overlaps 3a and 3b, ledger keeps one copy per idea |
| 2.2 | 2.2 The Empirical Literature on Wealth Taxation | 228 | K | LIT | N | - | literature context; overlaps 3a and 3b, ledger keeps one copy per idea |
| 2.3 | 2.3 The Income versus Consumption Debate | 385 | K | LIT | N | - | literature context; overlaps 3a and 3b, ledger keeps one copy per idea |
| 2.4 | 2.4 The Wealth Concentration Literature | 141 | K | H1 | P | NEW:H1 | wealth concentration (top 1% share about 38%, US); needs UK concentration facts for H1 |
| 2.5 | 2.5 The Domar-Musgrave Principle | 238 | K | LIT | N | - | literature context; overlaps 3a and 3b, ledger keeps one copy per idea |
| 2.6 | 2.6 Harberger Self-Assessment and the Purchase Option Tradit | 218 | K | LIT | N | - | literature context; overlaps 3a and 3b, ledger keeps one copy per idea |
| 2.7 | 2.7 Five Design Problems Unresolved in Prior Literature | 274 | K | LIT | N | - | literature context; overlaps 3a and 3b, ledger keeps one copy per idea |
| 3 | 3. The Wealth Delta Tax: Mechanism Design | 152 | K | H2 | N | - | plain-words mechanism opener |
| 3.1 | 3.1 The Tax Base | 239 | K | MECH | N | - | tax base, unit, voluntary participation, symmetric refund, windows |
| 3.2 | 3.2 The Individual as the Unit of Taxation | 525 | K | MECH | N | - | tax base, unit, voluntary participation, symmetric refund, windows |
| 3.3 | 3.3 The Progressive Rate Structure | 129 | K | FISC | N | - | rate structure in words; numbers belong to the named schedules |
| 3.4 | 3.4 The Exemption Threshold | 86 | K | FISC | P | NEW:payers | threshold is the political parameter; payer count by threshold is not an output yet |
| 3.4.1 | 3.4.1 Voluntary Participation Below the Threshold | 373 | K | MECH | N | - | tax base, unit, voluntary participation, symmetric refund, windows |
| 3.5 | 3.5 The Symmetric Loss-Refund Mechanism | 690 | K | MECH | N | - | tax base, unit, voluntary participation, symmetric refund, windows |
| 3.6 | 3.6 Assessment Windows | 319 | K | MECH | N | - | tax base, unit, voluntary participation, symmetric refund, windows |
| 3.7 | 3.7 Valuation Architecture | 357 | M | VAL | N | - | valuation architecture; duplicates VAL [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 3.8 | 3.8 Valuation Incentives and the Structure of the Problem | 496 | M | DECL | Y | O7,NEW:alpha-curve | model-implied behavioural centre alpha about 1.1; C.1 covers tolerance, not the centre [025w: S4 split: declaration incentives (VAL 7, VAL.A findings, VAL.B examples; map section 7)] |
| 4 | 4. The Sovereign Wealth Fund | 155 | K | FUND | N | - | fund purpose and why it is structurally necessary |
| 4.1 | 4.1 Why the Fund Is Structurally Necessary | 225 | K | FUND | N | - | fund purpose and why it is structurally necessary |
| 4.2 | 4.2 Governance and Shared Interests | 407 | K | GOV | N | - | three-constituency governance |
| 4.3 | 4.3 Route D Auction Mechanism | 702 | M | VAL | N | - | Route D auction; duplicates VAL 6.5 and 11 [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 5 | 5. Revenue Properties | 627 | K | FISC | Y | O1,O1a,O1b,OP1,NEW:reserve-solvency,NEW:coverage | v1 claims: 73 start years, reserve never reaches zero, fill 7 to 29 years, 125.5% coverage, 874bn and 172bn; v2 closure is 42 to 55% of windows, so these cannot be carried over |
| 5.1 | 5.1 Parameter Selection and the N = 30 Working Assumption | 732 | K | FISC | Y | O2,O3,O5,O6 | 0.35% revenue-weighted burden, 13.0% lifetime rate, against 1 to 2% stock taxes and CGT 18 to 24%; M2 formula still to be checked against 0.35% |
| 6 | 6. Replacing Existing Taxes: Scope and Sequencing | 550 | K | FUND | Y | O1d,OP5,OP3 | replacing existing taxes, scope and sequencing |
| 7 | 7. Implementation Pathway | 172 | K | POL | P | OP1 | implementation pathway and Phase One; thresholds are council parameters |
| 7.1 | 7.1 Phase One: Infrastructure and Proof of Mechanism | 340 | K | POL | P | OP1 | implementation pathway and Phase One; thresholds are council parameters |
| 7.2 | 7.2 Phase Two: Expansion and Labour Tax Relief | 134 | K | POL | P | OP1 | implementation pathway and Phase One; thresholds are council parameters |
| 7.3 | 7.3 International Coordination and Capital Mobility | 173 | K | BEHAV | P | - | migration and capital mobility; Norway evidence, no v3 range yet (driver D5) [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 8 | 8. Principal Objections | 0 | M | VAL | N | - | valuation objection; duplicates VAL [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 8.1 | 8.1 The Valuation Problem | 474 | M | VAL | N | - | valuation objection; duplicates VAL [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 8.2 | 8.2 The Liquidity Problem | 669 | K | PAY | Y | O2b,O2c | liquidity objection; cash-flow burden outputs answer it [025w: S6 split: who pays (RATES 2, WP 8.2, payslip; map section 7)] |
| 8.3 | 8.3 Behavioural Responses | 243 | K | BEHAV | P | - | behavioural responses and the complexity (attribution) objection [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 8.4 | 8.4 The Consumption Tax Alternative | 52 | M | LIT | N | - | consumption tax alternative |
| 8.5 | 8.5 Constitutional Entrenchment | 250 | K | GOV | N | - | entrenchment and state-finance entanglement |
| 8.6 | 8.6 State-Finance Entanglement | 61 | K | GOV | N | - | entrenchment and state-finance entanglement |
| 8.7 | 8.7 The Complexity Objection | 541 | K | BEHAV | P | - | behavioural responses and the complexity (attribution) objection [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 9 | 9. Limitations and Required Further Work | 0 | D | - | N | - | status text (gaps closed by WFR; data-access precondition covered by GOV) |
| 9.1 | 9.1 Formal modelling gaps | 267 | D | - | N | - | status text (gaps closed by WFR; data-access precondition covered by GOV) |
| 9.2 | 9.2 Phase One Empirical Unknowns | 221 | M | UNCER | N | - | empirical unknowns and irreducible limits [025w: was S12; what is not yet known empirically (unknowns, gaps, open questions)] |
| 9.3 | 9.3 Fiscal Concentration Risk | 299 | M | UNCER | Y | NEW:payers | fiscal concentration risk, 32,000 payers at W_min 10m [025w: was S12; payer concentration at W_min; the figure needs OB1, which the manifest gives to UNCER] |
| 9.4 | 9.4 Jurisdiction-Specific Legal and Implementation Work | 99 | D | - | N | - | status text (gaps closed by WFR; data-access precondition covered by GOV) |
| 9.5 | 9.5 Structural and Irreducible Limits of the Design | 284 | M | LIMIT | N | - | empirical unknowns and irreducible limits [025w: was S12; structural limit of the design] |
| 10 | 10. Conclusion | 516 | D | - | N | - | conclusion restates RATES; the hub writes its own |

## 2_Moral_and_Philosophical_Foundations (7642 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 102 | AR | - | N | - | front matter |
| rev | Revision History | 256 | AR | - | N | - | front matter |
| abs | Abstract | 198 | AR | - | N | - | front matter |
| gloss | Glossary | 577 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. Introduction | 546 | D | - | N | - | introduction and conclusion; FAIR opens and closes itself |
| 2 | 2. The Individual as the Only Legitimate Moral Subject | 906 | K | FAIR | N | - | the individual as the only legitimate moral subject |
| 3 | 3. Where Wealth Comes From | 0 | K | FAIR | N | - | where wealth comes from, collective production, why the delta |
| 3.1 | 3.1 Wealth as Constituted by Collective Frameworks | 346 | K | FAIR | N | - | where wealth comes from, collective production, why the delta |
| 3.2 | 3.2 Collective Inputs to Accumulation | 351 | K | FAIR | N | - | where wealth comes from, collective production, why the delta |
| 3.3 | 3.3 Why the Delta | 549 | K | FAIR | N | - | where wealth comes from, collective production, why the delta |
| 4 | 4. Wealth as Power, Not Deferred Consumption | 455 | K | FAIR | N | - | wealth as power; fiscal opacity |
| 5 | 5. Fiscal Opacity and the Conditions for Democratic Delibera | 296 | K | FAIR | N | - | wealth as power; fiscal opacity |
| 6 | 6. Democratic Flourishing as the Terminal Goal | 714 | K | FAIR | P | O4a | democratic flourishing; points to LDW for payslip numbers |
| 7 | 7. The Cooperative Architecture | 637 | K | FAIR | N | - | cooperative architecture; the hub H4 draws one paragraph |
| 8 | 8. Tolerance for Imperfect Compliance | 295 | M | LIMIT | N | - | tolerance for imperfect compliance; links to O7 [025w: was S12; tolerance for imperfect compliance is a boundary the design accepts; it links to O7, which the manifest gives to DECL, so LIMIT can only point to DECL] |
| 9 | 9. Limitations and Required Further Work | 37 | D | - | N | - | limitations register; items are carried by UNCER and LIMIT |
| 9.1 | 9.1 Formal modelling gaps | 100 | D | - | N | - | limitations register; items are carried by UNCER and LIMIT |
| 9.2 | 9.2 Phase One empirical unknowns | 65 | D | - | N | - | limitations register; items are carried by UNCER and LIMIT |
| 9.3 | 9.3 Jurisdiction-specific legal and implementation work | 42 | D | - | N | - | limitations register; items are carried by UNCER and LIMIT |
| 9.4 | 9.4 Structural and irreducible limits of the design | 0 | M | LIMIT | N | - | structural limits, short items [025w: was S12; structural limit of the design] |
| 9.4.1 | 9.4.1 The corporate instrument | 46 | M | LIMIT | N | - | structural limits, short items [025w: was S12; structural limit of the design] |
| 9.4.2 | 9.4.2 The asymmetric treatment of corporate loss years | 40 | M | LIMIT | N | - | structural limits, short items [025w: was S12; structural limit of the design] |
| 9.4.3 | 9.4.3 The exemption threshold | 48 | M | LIMIT | N | - | structural limits, short items [025w: was S12; structural limit of the design] |
| 9.4.4 | 9.4.4 International mobility and exit | 57 | M | LIMIT | N | - | structural limits, short items [025w: was S12; structural limit of the design] |
| 9.4.5 | 9.4.5 The assumption of functional democratic institutions | 66 | M | LIMIT | N | - | structural limits, short items [025w: was S12; structural limit of the design] |
| 9.4.6 | 9.4.6 The transition period | 54 | M | LIMIT | N | - | structural limits, short items [025w: was S12; structural limit of the design] |
| 9.4.7 | 9.4.7 The institutional tiers the mechanism produces | 56 | M | LIMIT | N | - | structural limits, short items [025w: was S12; structural limit of the design] |
| 9.4.8 | 9.4.8 The Route D extreme residual | 266 | M | VAL | N | - | Route D extreme residual; duplicates WP 4.3 [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 9.4.9 | 9.4.9 The governance compromises | 193 | M | LIMIT | N | - | structural limits, short items [025w: was S12; structural limit of the design] |
| 9.5 | 9.5 Governing Council calibration parameters | 6 | D | - | N | - | limitations register; items are carried by UNCER and LIMIT |
| 10 | 10. Conclusion | 338 | D | - | N | - | introduction and conclusion; FAIR opens and closes itself |

## 3a_Research_Gaps (4561 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 108 | AR | - | N | - | front matter |
| rev | Revision History | 91 | AR | - | N | - | front matter |
| abs | Abstract | 204 | AR | - | N | - | front matter |
| gloss | Glossary | 191 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. Introduction | 210 | D | - | N | - | introduction; conclusion list of nine gaps is superseded by the new set |
| 2 | 2. Formal Modelling Gaps | 0 | K | LIT | N | - | formal modelling gaps |
| 2.1 | 2.1 The Domar-Musgrave Extension | 480 | K | LIT | N | - | formal modelling gaps |
| 2.2 | 2.2 The Welfare Comparison | 345 | K | LIT | N | - | formal modelling gaps |
| 2.3 | 2.3 Heterogeneous Returns and the Delta Base | 368 | K | LIT | N | - | formal modelling gaps |
| 3 | 3. Compliance and Behavioural Gaps | 0 | K | LIT | N | - | compliance and behavioural gaps; migration externality also informs BEHAV |
| 3.1 | 3.1 Cooperative Compliance at the Ultra-High-Net-Worth Level | 654 | K | LIT | N | - | compliance and behavioural gaps; migration externality also informs BEHAV |
| 3.2 | 3.2 The Cross-Base Migration Externality | 283 | K | LIT | N | - | compliance and behavioural gaps; migration externality also informs BEHAV |
| 3.3 | 3.3 Administrative-Layer Intervention Effects | 324 | K | LIT | N | - | compliance and behavioural gaps; migration externality also informs BEHAV |
| 4 | 4. Political and International Gaps | 0 | K | LIT | N | - | political and international gaps; Zucman 2% minimum tax is a comparator (O5) |
| 4.1 | 4.1 The Political Durability Causal Framework | 261 | K | LIT | N | - | political and international gaps; Zucman 2% minimum tax is a comparator (O5) |
| 4.2 | 4.2 The International Competitive Dynamic at the Political L | 283 | K | LIT | N | - | political and international gaps; Zucman 2% minimum tax is a comparator (O5) |
| 4.3 | 4.3 The Minimum-Tax Interaction | 304 | K | LIT | N | - | political and international gaps; Zucman 2% minimum tax is a comparator (O5) |
| 5 | 5. Conclusion | 455 | D | - | N | - | introduction; conclusion list of nine gaps is superseded by the new set |

## 3b_Intellectual_Background (9707 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 111 | AR | - | N | - | front matter |
| rev | Revision History | 99 | AR | - | N | - | front matter |
| abs | Abstract | 192 | AR | - | N | - | front matter |
| gloss | Glossary | 526 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. Introduction and How to Use This Document | 405 | D | - | N | - | how to use this document |
| 2 | 2. The Tax Base Question | 431 | K | LIT | N | - | tax base, unrealised gains, loss treatment, heterogeneous returns, welfare comparison |
| 3 | 3. Unrealised Gains and Prior Accrual Proposals | 1264 | K | LIT | N | - | tax base, unrealised gains, loss treatment, heterogeneous returns, welfare comparison |
| 4 | 4. Symmetric Loss Treatment and Risk-Sharing | 448 | K | LIT | N | - | tax base, unrealised gains, loss treatment, heterogeneous returns, welfare comparison |
| 5 | 5. Heterogeneous Returns and Efficiency Under a Wealth Tax | 610 | K | LIT | N | - | tax base, unrealised gains, loss treatment, heterogeneous returns, welfare comparison |
| 6 | 6. Welfare Comparisons | 409 | K | LIT | N | - | tax base, unrealised gains, loss treatment, heterogeneous returns, welfare comparison |
| 7 | 7. The Empirical Wealth Tax Record | 494 | K | LIT | N | - | empirical wealth tax record; migration qualification also informs BEHAV |
| 8 | 8. The Valuation Problem | 430 | M | VAL | N | - | valuation problem and self-assessment literature [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 9 | 9. Self-Assessment and Deterrence | 415 | M | DECL | N | - | valuation problem and self-assessment literature [025w: S4 split: declaration incentives (VAL 7, VAL.A findings, VAL.B examples; map section 7)] |
| 10 | 10. Cooperative Compliance and Procedural Justice | 391 | M | BEHAV | N | - | cooperative compliance and professionally mediated systems [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 11 | 11. Compliance in Professionally Mediated Systems | 421 | M | BEHAV | N | - | cooperative compliance and professionally mediated systems [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 12 | 12. Collective Action and Governance of Multi-Constituency I | 404 | M | GOV | N | - | collective action, pension governance, SWF reference cases, precommitment |
| 13 | 13. Mutual and Pension Governance | 402 | M | GOV | N | - | collective action, pension governance, SWF reference cases, precommitment |
| 14 | 14. Sovereign Wealth Fund Reference Cases | 329 | M | GOV | N | - | collective action, pension governance, SWF reference cases, precommitment |
| 15 | 15. Precommitment and Fiscal Rules | 317 | M | GOV | N | - | collective action, pension governance, SWF reference cases, precommitment |
| 16 | 16. Moral Philosophy and the Normative Case | 475 | M | FAIR | N | - | moral philosophy and democratic legitimacy |
| 17 | 17. Democratic Legitimacy and Wealth Concentration | 587 | M | FAIR | N | - | moral philosophy and democratic legitimacy |
| 18 | 18. Exit Taxation and International Coordination | 547 | M | BEHAV | N | - | exit taxation and international coordination [025w: was S11; overlaps the kept migration rows in BEHAV (WP 7.3, BEHAV.A D); WIDER also fits] |

## 4_UK_Jurisdiction_and_Data_Reference_Paper (6320 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 117 | AR | - | N | - | front matter |
| rev | Revision History | 59 | AR | - | N | - | front matter |
| abs | Abstract | 193 | AR | - | N | - | front matter |
| gloss | Glossary | 616 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. The UK as Reference Jurisdiction | 0 | K | GOV | N | - | why the UK as reference jurisdiction |
| 1.1 | 1.1 Why a Reference Jurisdiction at All | 86 | K | GOV | N | - | why the UK as reference jurisdiction |
| 1.2 | 1.2 Why the UK | 17 | K | GOV | N | - | why the UK as reference jurisdiction |
| 1.2.1 | 1.2.1 Wealth Data | 124 | K | GOV | N | - | why the UK as reference jurisdiction |
| 1.2.2 | 1.2.2 Administrative Capacity | 68 | K | GOV | N | - | why the UK as reference jurisdiction |
| 1.2.3 | 1.2.3 Constitutional Flexibility | 48 | K | GOV | N | - | why the UK as reference jurisdiction |
| 1.2.4 | 1.2.4 Political Salience | 61 | K | GOV | N | - | why the UK as reference jurisdiction |
| 1.2.5 | 1.2.5 Researcher Familiarity | 52 | K | GOV | N | - | why the UK as reference jurisdiction |
| 1.3 | 1.3 What Is and Is Not Being Modelled | 205 | K | GOV | N | - | what is and is not modelled |
| 1.4 | 1.4 The Wealth Tax Commission Comparison | 202 | M | LIT | N | - | Wealth Tax Commission comparison (WTC 500,000 threshold, 260bn) |
| 1.5 | 1.5 UK Institutional Architecture and WDT Requirements | 33 | K | GOV | N | - | UK institutions against WDT requirements: HMRC, VOA, OBR, tribunals |
| 1.5.1 | 1.5.1 HMRC | 196 | K | GOV | N | - | UK institutions against WDT requirements: HMRC, VOA, OBR, tribunals |
| 1.5.2 | 1.5.2 The Valuation Office Agency | 310 | K | GOV | N | - | UK institutions against WDT requirements: HMRC, VOA, OBR, tribunals |
| 1.5.3 | 1.5.3 The Office for Budget Responsibility | 580 | K | GOV | N | - | UK institutions against WDT requirements: HMRC, VOA, OBR, tribunals |
| 1.5.4 | 1.5.4 The Tax Tribunal System | 216 | K | GOV | N | - | UK institutions against WDT requirements: HMRC, VOA, OBR, tribunals |
| 2 | 2. Data Reference | 28 | DL | UK data pack | N | - | data tables move to the data layer, cited by source |
| 2.1 | 2.1 Population and Economy | 120 | DL | UK data pack | N | - | data tables move to the data layer, cited by source |
| 2.2 | 2.2 Tax Revenues | 177 | DL | UK data pack | N | - | data tables move to the data layer, cited by source |
| 2.3 | 2.3 Government Expenditure Breakdown | 159 | DL | UK data pack | N | - | data tables move to the data layer, cited by source |
| 2.4 | 2.4 Wealth Distribution | 248 | DL | UK data pack | N | - | data tables move to the data layer, cited by source |
| 2.5 | 2.5 HMRC Institutional Data | 149 | DL | UK data pack | N | - | data tables move to the data layer, cited by source |
| 2.6 | 2.6 Valuation Office Agency Institutional Data | 155 | DL | UK data pack | N | - | data tables move to the data layer, cited by source |
| 2.7 | 2.7 OBR Institutional Data | 88 | DL | UK data pack | N | - | data tables move to the data layer, cited by source |
| 2.8 | 2.8 Tax Tribunal System Data | 138 | DL | UK data pack | N | - | data tables move to the data layer, cited by source |
| 2.9 | 2.9 Capital Gains Tax and Inheritance Tax: Baseline Data | 139 | DL | UK data pack | N | - | data tables move to the data layer, cited by source |
| 2.10 | 2.10 Data Gaps and Limitations | 253 | DL | UK data pack | N | - | data gaps (WAS undersamples above 3m); belongs to input register |
| 2.11 | 2.11 Model Input Data Provenance | 685 | DL | UK data pack | N | - | model input provenance; superseded by the v3 input register (012r) |
| 3 | 3. Data Summary | 0 | DL | UK data pack | N | - | data summary tables |
| 3.1 | 3.1 UK Government Income 2024-25 | 202 | DL | UK data pack | N | - | data summary tables |
| 3.2 | 3.2 UK Government Expenditure 2024-25 | 192 | DL | UK data pack | N | - | data summary tables |
| 3.3 | 3.3 Fiscal Summary | 42 | DL | UK data pack | N | - | data summary tables |
| 4 | 4. Limitations and Further Work | 0 | D | - | N | - | limitations register |
| 4.1 | 4.1 Formal modelling gaps | 5 | D | - | N | - | limitations register |
| 4.2 | 4.2 Phase One empirical unknowns | 68 | D | - | N | - | limitations register |
| 4.3 | 4.3 Jurisdiction-specific legal and implementation work | 266 | M | GOV | N | - | jurisdiction-specific legal work (HMRC data access, Custodian form) |
| 4.4 | 4.4 Structural and irreducible limits of the design | 17 | D | - | N | - | limitations register |
| 4.5 | 4.5 Governing Council calibration parameters | 6 | D | - | N | - | limitations register |

## 5_Valuing_Wealth (17034 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 107 | AR | - | N | - | front matter |
| rev | Revision History | 887 | AR | - | N | - | front matter |
| abs | Abstract | 340 | AR | - | N | - | front matter |
| gloss | Glossary | 698 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. The Valuation Problem | 629 | K | VAL | N | - | the valuation problem and the asset classification [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 2 | 2. Asset Classification | 28 | K | VAL | N | - | the valuation problem and the asset classification [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 2.1 | 2.1 Automatically Priced Assets | 41 | K | VAL | N | - | the valuation problem and the asset classification [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 2.2 | 2.2 Fungible Assets | 91 | K | VAL | N | - | the valuation problem and the asset classification [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 2.3 | 2.3 Non-Fungible Assets | 34 | K | VAL | N | - | the valuation problem and the asset classification [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 2.4 | 2.4 Why Periodic Valuation and Audit Are Insufficient | 66 | K | VAL | N | - | the valuation problem and the asset classification [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 3 | 3. Assessment Windows | 0 | M | MECH | N | - | assessment windows and borrowing; duplicates WP 3.6 |
| 3.1 | 3.1 Annual Reporting and Formal Assessment | 132 | M | MECH | N | - | assessment windows and borrowing; duplicates WP 3.6 |
| 3.2 | 3.2 Available Assessment Windows | 160 | M | MECH | N | - | assessment windows and borrowing; duplicates WP 3.6 |
| 3.3 | 3.3 Borrowing and Net Worth | 42 | M | MECH | N | - | assessment windows and borrowing; duplicates WP 3.6 |
| 4 | 4. The Four Valuation Routes | 178 | K | VAL | N | - | the four valuation routes [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 4.1 | 4.1 Route A: Professional Valuation of Fungible Assets | 65 | K | VAL | N | - | the four valuation routes [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 4.2 | 4.2 Route B: Professional Valuation of Non-Fungible Assets | 85 | K | VAL | N | - | the four valuation routes [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 4.3 | 4.3 Route C: Self-Declaration of Fungible Assets | 133 | K | VAL | N | - | the four valuation routes [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 4.4 | 4.4 Route D: Self-Declaration of Non-Fungible Assets | 163 | K | VAL | N | - | the four valuation routes [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 5 | 5. The Self-Balancing Mechanism: Fungible Assets | 307 | K | VAL | P | - | self-balancing mechanism for fungible assets; figures are closed-form arithmetic [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 5.1 | 5.1 The Grandfathering Baseline | 64 | K | VAL | P | - | self-balancing mechanism for fungible assets; figures are closed-form arithmetic [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 5.2 | 5.2 The Must-Transfer Rule | 765 | K | VAL | P | - | self-balancing mechanism for fungible assets; figures are closed-form arithmetic [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 5.3 | 5.3 Delta Continuity at Realisation | 74 | K | VAL | P | - | self-balancing mechanism for fungible assets; figures are closed-form arithmetic [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 6 | 6. Non-Fungible Assets and Realisation | 0 | K | VAL | N | - | non-fungible assets and realisation (Route D) [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 6.1 | 6.1 Why Periodic Accrual Is Not Workable for Non-Fungible As | 126 | K | VAL | N | - | non-fungible assets and realisation (Route D) [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 6.2 | 6.2 Assessment During the Holding Period | 88 | K | VAL | N | - | non-fungible assets and realisation (Route D) [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 6.3 | 6.3 The Realisation Calculation | 112 | K | VAL | N | - | non-fungible assets and realisation (Route D) [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 6.4 | 6.4 Voluntary Settlement | 529 | K | VAL | N | - | non-fungible assets and realisation (Route D) [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 6.5 | 6.5 Inheritance and the Auction Mechanism | 497 | K | VAL | N | - | non-fungible assets and realisation (Route D) [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 6.6 | 6.6 Destruction, Theft, and Forced Removal | 40 | K | VAL | N | - | non-fungible assets and realisation (Route D) [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 7.1 | 7.1 Declaration Strategy and the Rational Equilibrium | 2037 | K | DECL | Y | O7,NEW:alpha-curve | declaration strategy, understatement, overstatement; results from the v1 simulation [025w: S4 split: declaration incentives (VAL 7, VAL.A findings, VAL.B examples; map section 7)] |
| 7.2 | 7.2 Understatement: Deferred Liability and Dilution | 625 | K | DECL | Y | O7,NEW:alpha-curve | declaration strategy, understatement, overstatement; results from the v1 simulation [025w: S4 split: declaration incentives (VAL 7, VAL.A findings, VAL.B examples; map section 7)] |
| 7.3 | 7.3 Overstatement: Signalling and Confidence Effects | 883 | K | DECL | Y | O7,NEW:alpha-curve | declaration strategy, understatement, overstatement; results from the v1 simulation [025w: S4 split: declaration incentives (VAL 7, VAL.A findings, VAL.B examples; map section 7)] |
| 7.4 | 7.4 Boundary Conditions and Limitations | 259 | K | DECL | P | O7 | boundary conditions [025w: S4 split: declaration incentives (VAL 7, VAL.A findings, VAL.B examples; map section 7)] |
| 7.5 | 7.5 Portfolio Composition as a Structural Constraint on Decl | 724 | K | DECL | Y | O7,NEW:composition | portfolio composition limits deviation; needs share of wealth in observable assets by band (input) [025w: S4 split: declaration incentives (VAL 7, VAL.A findings, VAL.B examples; map section 7)] |
| 8 | 8. The Assessment Window Premium | 143 | M | MECH | N | - | assessment window premium; excluded from the reference model |
| 9 | 9. The Public Valuation Register | 725 | K | VAL | N | - | public valuation register [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 10 | 10. Professional Valuation | 0 | K | VAL | N | - | professional valuation route [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 10.1 | 10.1 Purpose | 43 | K | VAL | N | - | professional valuation route [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 10.2 | 10.2 Competitive Tender Model | 143 | K | VAL | N | - | professional valuation route [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 10.3 | 10.3 Cost Sharing with a Fee Cap | 84 | K | VAL | N | - | professional valuation route [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 10.4 | 10.4 The Two-Stage Review Process | 130 | K | VAL | N | - | professional valuation route [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 10.5 | 10.5 The Valuation Code | 186 | K | VAL | N | - | professional valuation route [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 10.6 | 10.6 Valuation Governance | 217 | K | GOV | N | - | Valuation Code Board governance |
| 11 | 11. The Route D Auction Mechanism — Three Uses of One Proces | 175 | K | VAL | N | - | Route D auction, three uses [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 11.1 | 11.1 Deterrent Logic | 130 | K | VAL | N | - | Route D auction, three uses [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 11.2 | 11.2 Voluntary Hard-Reset Auction | 140 | K | VAL | N | - | Route D auction, three uses [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 11.3 | 11.3 Corrective Auction: Trigger and Process | 446 | K | VAL | N | - | Route D auction, three uses [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 11.4 | 11.4 Inheritance Auction | 189 | K | VAL | N | - | Route D auction, three uses [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 11.5 | 11.5 Scope | 142 | K | VAL | N | - | Route D auction, three uses [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 12 | 12. Administration and Fraud Detection | 75 | K | GOV | N | - | administration, reporting, statistical review, penalties |
| 12.1 | 12.1 Annual Reporting Requirements | 66 | K | GOV | N | - | administration, reporting, statistical review, penalties |
| 12.2 | 12.2 The Purpose of Audit: Fraud, Not Valuation | 136 | K | VAL | N | - | audit is for fraud, not valuation [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| 12.3 | 12.3 Statistical Review | 110 | K | GOV | N | - | administration, reporting, statistical review, penalties |
| 12.4 | 12.4 Penalties | 81 | K | GOV | N | - | administration, reporting, statistical review, penalties |
| 13 | 13. The Sovereign Liquidity Facility | 340 | K | FUND | N | - | Sovereign Liquidity Facility |
| 14 | 14. Limitations and Further Work | 0 | D | - | N | - | limitations register, v1 validation note, premium calibration, conclusion |
| 14.1 | 14.1 Formal Modelling Gaps | 93 | D | - | N | - | limitations register, v1 validation note, premium calibration, conclusion |
| 14.2 | 14.2 Phase One Empirical Unknowns | 389 | D | - | N | - | limitations register, v1 validation note, premium calibration, conclusion |
| 14.3 | 14.3 Jurisdiction-Specific Legal and Implementation Work | 481 | M | UNCER | N | - | Route D entry-basis boundary and the other two boundaries [025w: was S12; legal and implementation work still to do; the matching limit is the next row (LIMIT)] |
| 14.4 | 14.4 Structural and Irreducible Limits of the Design | 513 | M | LIMIT | N | - | Route D entry-basis boundary and the other two boundaries [025w: was S12; structural limit (LIMIT); the open legal work is the row above (UNCER)] |
| 14.5 | 14.5 Governing Council Calibration Parameters | 91 | D | - | N | - | limitations register, v1 validation note, premium calibration, conclusion |
| 15 | 15. Conclusion | 757 | D | - | N | - | limitations register, v1 validation note, premium calibration, conclusion |

## 5a_Valuing_Wealth_Mathematical_and_Simulation_Appendix (17111 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 108 | AR | - | N | - | front matter |
| rev | Revision History | 690 | AR | - | N | - | front matter |
| ~A. | A. Mathematical Model and Incentive Analysis | 0 | DL | method note for O7 | N | - | formal model of declaration incentives (notation, recursion, propositions); the specification M7 needs |
| A.1 | A.1 Purpose | 298 | DL | method note for O7 | N | - | formal model of declaration incentives (notation, recursion, propositions); the specification M7 needs |
| A.2 | A.2 Main Findings (+5) | 1374 | K | DECL | Y | O7,NEW:alpha-curve | five findings in short form [025w: S4 split: declaration incentives (VAL 7, VAL.A findings, VAL.B examples; map section 7)] |
| A.3 | A.3 Model Assumptions and Notation (+4) | 955 | DL | method note for O7 | N | - | formal model of declaration incentives (notation, recursion, propositions); the specification M7 needs |
| A.4 | A.4 Multi-Period Incentive Model (+7) | 972 | DL | method note for O7 | N | - | formal model of declaration incentives (notation, recursion, propositions); the specification M7 needs |
| A.5 | A.5 Scope of the Arguments (+6) | 1625 | DL | method note for O7 | N | - | formal model of declaration incentives (notation, recursion, propositions); the specification M7 needs |
| A.6 | A.6 The Declaration Equilibrium: A Broad Tolerant Zone with | 1275 | M | DECL | Y | O7,NEW:alpha-curve | declaration equilibrium; duplicates VAL 7.1 [025w: S4 split: declaration incentives (VAL 7, VAL.A findings, VAL.B examples; map section 7)] |
| ~B. | B. Simulation Methodology | 0 | DL | method note for O7 | N | - | simulation algorithm, parameter table, metrics |
| B | B.1 Purpose (+6) | 1198 | DL | method note for O7 | N | - | simulation algorithm, parameter table, metrics |
| ~C. | C. WDT Valuation Analysis: Summary Tables | 102 | AR | - | Y | O7,NEW:alpha-curve | v1 result tables C.1 to C.12 (0 FAILs, v1 only); v3 regenerates them |
| C | C.1 Total Tax Paid (TTP) Difference Relative to Honest Decla | 6568 | AR | - | Y | O7,NEW:alpha-curve | v1 result tables C.1 to C.12 (0 FAILs, v1 only); v3 regenerates them |
| C.6 | C.6 Terminal Net Worth After Refunds: Refund Protection Rati | 199 | AR | - | Y | NEW:alpha-curve | refund protection ratio in loss years: understaters lose refund protection |
| ~D. | D. Mechanism Cases | 27 | D | - | N | - | five abstract cases; covered by VAL.B and A.5 |
| D | D.1 Case 1: Persistent Understatement, Asset Never Realises | 564 | D | - | N | - | five abstract cases; covered by VAL.B and A.5 |
| ~E. | E. Route Specification Tables | 24 | M | VAL | N | - | route specification tables; duplicate VAL 4 [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| E | E.1 Route A: Professional Valuation of Fungible Assets (+4) | 873 | M | VAL | N | - | route specification tables; duplicate VAL 4 [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| ~F. | F. Annual Reporting Requirements | 10 | M | GOV | N | - | annual reporting requirements |
| F | F.1 Taxpayer Annual Return (+3) | 249 | M | GOV | N | - | annual reporting requirements |

## 5b_Valuing_Wealth_Worked_Examples_Appendix (5592 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 92 | AR | - | N | - | front matter |
| rev | Revision History | 204 | AR | - | N | - | front matter |
| ~Reader | Reader's Guide | 309 | D | - | N | - | reader's guide and summary table |
| ~J. | J. The Deferred Delta | 37 | K | DECL | P | NEW:example-figures | five worked examples tethered to the five VAL claims; figures from the v1 simulation or closed-form arithmetic, to be regenerated as fixtures [025w: S4 split: declaration incentives (VAL 7, VAL.A findings, VAL.B examples; map section 7)] |
| J | J.1 Setup (+5) | 687 | K | DECL | P | NEW:example-figures | five worked examples tethered to the five VAL claims; figures from the v1 simulation or closed-form arithmetic, to be regenerated as fixtures [025w: S4 split: declaration incentives (VAL 7, VAL.A findings, VAL.B examples; map section 7)] |
| ~K. | K. Dilution Compounds with Growth | 46 | K | DECL | P | NEW:example-figures | five worked examples tethered to the five VAL claims; figures from the v1 simulation or closed-form arithmetic, to be regenerated as fixtures [025w: S4 split: declaration incentives (VAL 7, VAL.A findings, VAL.B examples; map section 7)] |
| K | K.1 Setup (+6) | 719 | K | DECL | P | NEW:example-figures | five worked examples tethered to the five VAL claims; figures from the v1 simulation or closed-form arithmetic, to be regenerated as fixtures [025w: S4 split: declaration incentives (VAL 7, VAL.A findings, VAL.B examples; map section 7)] |
| ~L. | L. Why Route D Defers to Realisation | 45 | K | DECL | P | NEW:example-figures | five worked examples tethered to the five VAL claims; figures from the v1 simulation or closed-form arithmetic, to be regenerated as fixtures [025w: S4 split: declaration incentives (VAL 7, VAL.A findings, VAL.B examples; map section 7)] |
| L | L.1 Setup (+6) | 812 | K | DECL | P | NEW:example-figures | five worked examples tethered to the five VAL claims; figures from the v1 simulation or closed-form arithmetic, to be regenerated as fixtures [025w: S4 split: declaration incentives (VAL 7, VAL.A findings, VAL.B examples; map section 7)] |
| ~M. | M. Voluntary Settlement — Certainty, Not Avoidance | 69 | K | DECL | P | NEW:example-figures | five worked examples tethered to the five VAL claims; figures from the v1 simulation or closed-form arithmetic, to be regenerated as fixtures [025w: S4 split: declaration incentives (VAL 7, VAL.A findings, VAL.B examples; map section 7)] |
| M | M.1 Setup (+5) | 964 | K | DECL | P | NEW:example-figures | five worked examples tethered to the five VAL claims; figures from the v1 simulation or closed-form arithmetic, to be regenerated as fixtures [025w: S4 split: declaration incentives (VAL 7, VAL.A findings, VAL.B examples; map section 7)] |
| ~N. | N. Forecast Exposure | 46 | K | DECL | P | NEW:example-figures | five worked examples tethered to the five VAL claims; figures from the v1 simulation or closed-form arithmetic, to be regenerated as fixtures [025w: S4 split: declaration incentives (VAL 7, VAL.A findings, VAL.B examples; map section 7)] |
| N | N.1 Setup (+6) | 1373 | K | DECL | P | NEW:example-figures | five worked examples tethered to the five VAL claims; figures from the v1 simulation or closed-form arithmetic, to be regenerated as fixtures [025w: S4 split: declaration incentives (VAL 7, VAL.A findings, VAL.B examples; map section 7)] |
| ~O. | O. Summary of Design Properties Illustrated | 189 | D | - | N | - | reader's guide and summary table |

## 6_Corporate_Architecture (8681 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 112 | AR | - | N | - | front matter |
| rev | Revision History | 116 | AR | - | N | - | front matter |
| abs | Abstract | 286 | AR | - | N | - | front matter |
| gloss | Glossary | 462 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. Introduction | 286 | M | CORP | N | - | introduction; the individual-centred logic duplicates WP 3.2 |
| 2 | 2. Why Existing Corporate Tax Systems Are Insufficient | 430 | K | CORP | N | - | why existing corporate taxes fall short; listed against private; lifecycle events |
| 2.1 | 2.1 Existing Administrative Analogues | 183 | K | CORP | N | - | why existing corporate taxes fall short; listed against private; lifecycle events |
| 3 | 3. The Individual-Centred Logic and Its Limits | 113 | M | CORP | N | - | introduction; the individual-centred logic duplicates WP 3.2 |
| 4 | 4. The Listed/Private Distinction | 110 | K | CORP | N | - | why existing corporate taxes fall short; listed against private; lifecycle events |
| 4.1 | 4.1 Corporate Lifecycle Events | 589 | K | CORP | N | - | why existing corporate taxes fall short; listed against private; lifecycle events |
| 5 | 5. The Listed Company Corporate Delta Levy | 0 | K | CORP | Y | O1b | the corporate delta levy as escrow, annual cycle, tranches, year end, loss years |
| 5.1 | 5.1 The Mechanism in One Place | 701 | K | CORP | Y | O1b | the corporate delta levy as escrow, annual cycle, tranches, year end, loss years |
| 5.2 | 5.2 Annual Cycle: Measurement and Reporting | 383 | K | CORP | Y | O1b | the corporate delta levy as escrow, annual cycle, tranches, year end, loss years |
| 5.3 | 5.3 Tranche Outcomes During the Year | 548 | K | CORP | Y | O1b | the corporate delta levy as escrow, annual cycle, tranches, year end, loss years |
| 5.4 | 5.4 Year-End Settlement | 350 | K | CORP | Y | O1b | the corporate delta levy as escrow, annual cycle, tranches, year end, loss years |
| 5.5 | 5.5 Loss Years | 112 | K | CORP | Y | O1b | the corporate delta levy as escrow, annual cycle, tranches, year end, loss years |
| 5.6 | 5.6 Residual Imperfections | 188 | M | LIMIT | N | - | residual imperfections (assessment-date gaming) [025w: was S12; structural limit of the design] |
| 6 | 6. The Corporate Equity Settlement Facility | 0 | K | CORP | N | - | Corporate Equity Settlement Facility |
| 6.1 | 6.1 Purpose and Scope | 252 | K | CORP | N | - | Corporate Equity Settlement Facility |
| 6.2 | 6.2 Mechanism | 384 | K | CORP | N | - | Corporate Equity Settlement Facility |
| 6.3 | 6.3 Relationship to the SWF | 334 | K | CORP | N | - | Corporate Equity Settlement Facility |
| 6.4 | 6.4 Governing Council Calibration Parameters | 149 | DL | parameter register | N | - | Governing Council calibration parameters |
| 7 | 7. Institutional Ownership | 592 | K | CORP | N | - | institutional ownership; synthetic exposure and derivatives |
| 8 | 8. Synthetic Exposure and Derivatives | 496 | K | CORP | N | - | institutional ownership; synthetic exposure and derivatives |
| 9 | 9. Limitations and Required Further Work | 0 | D | - | N | - | limitations register and conclusion |
| 9.1 | 9.1 Formal modelling gaps | 47 | D | - | N | - | limitations register and conclusion |
| 9.2 | 9.2 Phase One empirical unknowns | 248 | M | UNCER | Y | O1b,O1d | whether the levy displaces corporation tax outright [025w: was S12; what is not yet known empirically (unknowns, gaps, open questions)] |
| 9.3 | 9.3 Jurisdiction-specific legal and implementation work | 58 | D | - | N | - | limitations register and conclusion |
| 9.4 | 9.4 Structural and irreducible limits of the design | 506 | M | LIMIT | N | - | structural limits of the corporate instrument [025w: was S12; structural limit of the design] |
| 9.5 | 9.5 Governing Council calibration parameters | 371 | DL | parameter register | N | - | Governing Council calibration parameters |
| 10 | 10. Conclusion | 275 | D | - | N | - | limitations register and conclusion |

## 6a_Corporate_Architecture_Appendix (15089 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 97 | AR | - | N | - | front matter |
| rev | Revision History | 45 | AR | - | N | - | front matter |
| ~A. | A. Collection Mechanics and Worked Illustrations | 0 | AR | - | N | - | collection mechanics detail; kept for the statute-drafting phase |
| A.1 | A.1 The Two-Deadline Structure | 322 | M | CORP | N | - | two-deadline structure, sequencing, broker and nominee case; duplicate CORP 5 |
| A.2 | A.2 Shareholders Who Sell Before the Assessment Date** | 129 | AR | - | N | - | collection mechanics detail; kept for the statute-drafting phase |
| A.3 | A.3 Partial-Year Attribution | 92 | AR | - | N | - | collection mechanics detail; kept for the statute-drafting phase |
| A.4 | A.4 Sequencing | 201 | M | CORP | N | - | two-deadline structure, sequencing, broker and nominee case; duplicate CORP 5 |
| A.5 | A.5 Loss Years and Private Arrangements | 54 | AR | - | N | - | collection mechanics detail; kept for the statute-drafting phase |
| A.6 | A.6 Worked Illustration: Standard Shareholders | 344 | K | CORP | N | - | worked illustration with three shareholders |
| A.7 | A.7 Corporate Entities as Shareholders | 167 | AR | - | N | - | collection mechanics detail; kept for the statute-drafting phase |
| A.8 | A.8 No Minimum Threshold | 36 | AR | - | N | - | collection mechanics detail; kept for the statute-drafting phase |
| A.9 | A.9 Intermediary Chain Illustrations | 0 | M | CORP | N | - | two-deadline structure, sequencing, broker and nominee case; duplicate CORP 5 |
| A.9.1 | A.9.1 Broker/Nominee Case | 500 | M | CORP | N | - | two-deadline structure, sequencing, broker and nominee case; duplicate CORP 5 |
| A.9.2 | A.9.2 Pooled Fund Case | 198 | AR | - | N | - | collection mechanics detail; kept for the statute-drafting phase |
| ~B. | B. Corporate Rate Calibration | 83 | M | CORP | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.1 | B.1 The Floor Rate ($\tau_0$): Collection Security | 475 | M | CORP | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.1.1 | B.1.1 Phase One data requirement | 112 | DL | parameter register | N | - | Phase One data requirements for calibration |
| B.2 | B.2 The Final Charge on Permanently Unattributable Ownership | 68 | M | CORP | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.2.1 | B.2.1 The deterrence condition | 93 | M | CORP | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.2.2 | B.2.2 The refund-forfeiture effect | 123 | M | CORP | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.2.3 | B.2.3 The revenue-recovery ceiling | 83 | M | CORP | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.2.4 | B.2.4 The legal proportionality constraint, and why it is we | 228 | M | CORP | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.2.5 | B.2.5 One carve-out applies | 81 | M | CORP | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.2.6 | B.2.6 The resulting calibration range | 107 | M | CORP | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.2.7 | B.2.7 Phase One data requirement | 134 | DL | parameter register | N | - | Phase One data requirements for calibration |
| B.2.8 | B.2.8 The ramp structure | 341 | M | CORP | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.2.9 | B.2.9 The joint-calibration constraint | 402 | M | CORP | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.3 | B.3 Intermediary-Level Provisioning Floor | 354 | M | CORP | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.4 | B.4 The Rejected Pool-Average Alternative | 82 | M | CORP | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| ~C. | C. Ownership Structure Classification Under the Attribution | 935 | K | CORP | N | - | ownership structure classification under the attribution test |
| ~D. | D. Administrative Burden | 0 | K | CORP | N | - | administrative burden of the corporate mechanism |
| D | D.1 Purpose (+4) | 1078 | K | CORP | N | - | administrative burden of the corporate mechanism |
| D.6 | D.6 Transitional Considerations and the Parallel-Running Ris | 220 | K | CORP | N | - | administrative burden of the corporate mechanism |
| D.7 | D.7 Summary | 208 | K | CORP | N | - | administrative burden of the corporate mechanism |
| ~E. | E. Non-Corporate Instruments and the Attribution Test | 0 | K | ATTR | N | - | non-corporate instruments and the attribution test; proposed standalone paper, author to decide [025w: S8-A decision, 2026-11-17: was a proposed standalone paper (SA, ENT), now the page ATTR] |
| E.1 | E.1 Purpose | 204 | K | ATTR | N | - | non-corporate instruments and the attribution test; proposed standalone paper, author to decide [025w: S8-A decision, 2026-11-17: was a proposed standalone paper (SA, ENT), now the page ATTR] |
| E | E.2 Charitable Vehicles (+17) | 5061 | K | ATTR | N | - | non-corporate instruments and the attribution test; proposed standalone paper, author to decide [025w: S8-A decision, 2026-11-17: was a proposed standalone paper (SA, ENT), now the page ATTR] |
| E.9 | E.9 Market Manipulation and the Bilateral-Claim Structure of | 1233 | K | ATTR | P | - | market manipulation and short positions (v3 does not model manipulation) [025w: S8-A decision, 2026-11-17: was a proposed standalone paper (SA, ENT), now the page ATTR] |
| ~F. | F. $\tau_f$: Foreign Attribution and Diplomatic Rate-Setting | 560 | K | CORP | N | - | foreign attribution and diplomatic rate-setting |
| F.1 | F.1 $\tau_c$ as an Ownership-Composition Lever | 401 | K | CORP | N | - | foreign attribution and diplomatic rate-setting |
| ~G. | G. Existing $\tau$ parameters | 238 | DL | parameter register | N | - | existing tau parameters |

## 7_Constitutional_Governance (13117 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 105 | AR | - | N | - | front matter |
| rev | Revision History | 297 | AR | - | N | - | front matter |
| abs | Abstract | 403 | AR | - | N | - | front matter |
| gloss | Glossary | 2553 | DL | glossary | N | - | 2,553 words of role and term definitions; merge into the build glossary |
| 1 | 1. Introduction | 457 | K | GOV | N | - | the governance problem the paper addresses |
| 1.1 | 1.1 The Governance Problem This Paper Addresses | 527 | K | GOV | N | - | the governance problem the paper addresses |
| 2 | 2. The Standard This Design Is Held To | 320 | K | GOV | N | - | the standard the design is held to; mechanism-shaped test |
| 2.1 | 2.1 The Mechanism-Shaped Test | 448 | K | GOV | N | - | the standard the design is held to; mechanism-shaped test |
| 3 | 3. Deriving the Architecture | 152 | K | GOV | N | - | deriving the architecture; dividend recipients' standing |
| 3.1 | 3.1 The Corrected Derivation | 407 | K | GOV | N | - | deriving the architecture; dividend recipients' standing |
| 3.2 | 3.2 Closing the Dividend Recipients' Standing | 851 | K | GOV | N | - | deriving the architecture; dividend recipients' standing |
| 4 | 4. Designing Against Capture | 379 | K | GOV | N | - | designing against capture; structural safeguards, anti-collusion, enumerated clauses, tiered review |
| 5 | 5. The Structural Safeguards | 43 | K | GOV | N | - | designing against capture; structural safeguards, anti-collusion, enumerated clauses, tiered review |
| 5.1 | 5.1 The Anti-Collusion Guarantee | 303 | K | GOV | N | - | designing against capture; structural safeguards, anti-collusion, enumerated clauses, tiered review |
| 5.2 | 5.2 The Enumerated Structural Clauses | 1395 | K | GOV | N | - | designing against capture; structural safeguards, anti-collusion, enumerated clauses, tiered review |
| 5.3 | 5.3 Tiered Review, Rebalancing, and Transparency | 832 | K | GOV | N | - | designing against capture; structural safeguards, anti-collusion, enumerated clauses, tiered review |
| 6 | 6. The Executive Bodies | 28 | K | GOV | N | - | executive bodies: Valuation Bodies, Allocator, Administrator |
| 6.1 | 6.1 The Valuation Bodies | 357 | K | GOV | N | - | executive bodies: Valuation Bodies, Allocator, Administrator |
| 6.2 | 6.2 The Allocator | 444 | K | GOV | N | - | executive bodies: Valuation Bodies, Allocator, Administrator |
| 6.3 | 6.3 The SWF Custodian | 656 | K | FUND | N | - | SWF Custodian |
| 6.4 | 6.4 The Administrator | 462 | K | GOV | N | - | executive bodies: Valuation Bodies, Allocator, Administrator |
| 7 | 7. Limitations and Further Work | 11 | D | - | N | - | limitations register, calibration list and conclusion |
| 7.1 | 7.1 Formal modelling gaps | 93 | D | - | N | - | limitations register, calibration list and conclusion |
| 7.2 | 7.2 Phase One empirical unknowns | 401 | M | UNCER | N | - | empirical unknowns (volunteer rate under lottery, constituency dissolution) [025w: was S12; what is not yet known empirically (unknowns, gaps, open questions)] |
| 7.3 | 7.3 Jurisdiction-specific legal and implementation work | 164 | D | - | N | - | limitations register, calibration list and conclusion |
| 7.4 | 7.4 Structural and irreducible limits of the design | 344 | M | LIMIT | N | - | governance entropy and its four sub-forms [025w: was S12; structural limit of the design] |
| 7.5 | 7.5 Governing Council calibration parameters | 305 | D | - | N | - | limitations register, calibration list and conclusion |
| 8 | 8. Conclusion | 380 | D | - | N | - | limitations register, calibration list and conclusion |

## 7a_WDT_Constitutional_Governance_Intellectual_Appendix (7740 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 92 | AR | - | N | - | front matter |
| rev | Revision History | 110 | AR | - | N | - | front matter |
| ~A. | A. Failure-Mode Taxonomy | 45 | AR | - | N | - | failure-mode taxonomy, instrument audit, rejected first derivation, explored and dropped mechanisms; design history, kept so dropped ideas are not re-proposed |
| A | A.1 Oracle Failure (+2) | 892 | AR | - | N | - | failure-mode taxonomy, instrument audit, rejected first derivation, explored and dropped mechanisms; design history, kept so dropped ideas are not re-proposed |
| ~B. | B. WDT Instrument Audit | 37 | AR | - | N | - | failure-mode taxonomy, instrument audit, rejected first derivation, explored and dropped mechanisms; design history, kept so dropped ideas are not re-proposed |
| B | B.1 Instruments That Pass Cleanly (+1) | 1101 | AR | - | N | - | failure-mode taxonomy, instrument audit, rejected first derivation, explored and dropped mechanisms; design history, kept so dropped ideas are not re-proposed |
| ~C. | C. The Rejected First Derivation | 64 | AR | - | N | - | failure-mode taxonomy, instrument audit, rejected first derivation, explored and dropped mechanisms; design history, kept so dropped ideas are not re-proposed |
| C | C.1 The First Transaction: Delta Measurement and Tax Flow (+ | 1316 | AR | - | N | - | failure-mode taxonomy, instrument audit, rejected first derivation, explored and dropped mechanisms; design history, kept so dropped ideas are not re-proposed |
| ~D. | D. Explored and Dropped Mechanisms | 80 | AR | - | N | - | failure-mode taxonomy, instrument audit, rejected first derivation, explored and dropped mechanisms; design history, kept so dropped ideas are not re-proposed |
| D | D.1 Mechanisms That Reproduce the Resource-Defines-Truth Fai | 2315 | AR | - | N | - | failure-mode taxonomy, instrument audit, rejected first derivation, explored and dropped mechanisms; design history, kept so dropped ideas are not re-proposed |
| ~E. | E. Governance Decay: Four Sub-Forms | 78 | M | LIMIT | N | - | governance decay in four sub-forms; limits feed the failure section [025w: was S12; structural limit of the design] |
| E | E.1 Definitional Drift (+4) | 1610 | M | LIMIT | N | - | governance decay in four sub-forms; limits feed the failure section [025w: was S12; structural limit of the design] |

## 7b_Constitutional_Governance_Operational_Appendix (22067 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 95 | AR | - | N | - | front matter |
| rev | Revision History | 453 | AR | - | N | - | front matter |
| ~A. | A. The Chambers in Full | 0 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |
| A | A.1 The Taxpayer Chamber (TP) (+18) | 3097 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |
| ~B. | B. The Executive Bodies in Full | 69 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |
| B | B.1 The Valuation Bodies (VB-1, VB-2, VB-3) (+18) | 3085 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |
| B.3 | B.3 The SWF Custodian | 528 | M | FUND | N | - | SWF Custodian, institutional form, stress function |
| B.4.7 | B.4.7 The Privacy Election: Binary Disclosure and the Rate D | 692 | M | GOV | N | - | privacy election and rate differential |
| ~C. | C. Voting Mechanics in Full | 0 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |
| C | C.1 The Dual-Threshold Calculation: Worked Arithmetic (+7) | 3490 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |
| ~D. | D. The Rebalancing Mechanism in Full | 0 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |
| D | D.1 Conservation Arithmetic: How Vote Share Moves (+3) | 1179 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |
| ~E. | E. The SWF: Operational Detail | 0 | AR | - | N | - | SWF operational detail; solvency floor, drawdown, closure bonds, unit-holder rights |
| E.1 | E.1 The Solvency Floor: Definition and the Automatic-Consequ | 270 | AR | - | N | - | SWF operational detail; solvency floor, drawdown, closure bonds, unit-holder rights |
| E.2 | E.2 Drawdown Conditions: Pre-Crisis Commitment and the Annua | 233 | AR | - | N | - | SWF operational detail; solvency floor, drawdown, closure bonds, unit-holder rights |
| E.3 | E.3 The Closure Bond Facility: Bond Posting Sequence and Set | 643 | AR | - | N | - | SWF operational detail; solvency floor, drawdown, closure bonds, unit-holder rights |
| E.4 | E.4 Unit-Holder Rights: Financial Rights, Investment Input, | 501 | AR | - | N | - | SWF operational detail; solvency floor, drawdown, closure bonds, unit-holder rights |
| E.5 | E.5 Stewardship Statements: Annual Cycle, Mandatory Content, | 315 | AR | - | N | - | SWF operational detail; solvency floor, drawdown, closure bonds, unit-holder rights |
| E.6 | E.6 Institutional Form: Candidate Mapping (UK Reference) | 198 | M | FUND | N | - | SWF Custodian, institutional form, stress function |
| E.7 | E.7 Custodian Investment Mandate: Inflationary Conditions | 641 | AR | - | N | - | SWF operational detail; solvency floor, drawdown, closure bonds, unit-holder rights |
| E.8 | E.8 Custodian Alignment Mechanisms | 419 | AR | - | N | - | SWF operational detail; solvency floor, drawdown, closure bonds, unit-holder rights |
| E.9 | E.9 The Stress Function | 300 | M | FUND | N | - | SWF Custodian, institutional form, stress function |
| ~F. | F. Per-Actor Cost Mechanisms | 0 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |
| F | F.1 Patient Wealth (TP and FS): Vote-Share Rebalancing (+4) | 1532 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |
| ~G. | G. The Route D Auction Process in Full | 145 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |
| G | G.1 Sealed-Estimate Protocol: Sequencing and the Non-Anchori | 2878 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |
| ~H. | H. The Corporate Equity Settlement Facility: Mandate Extensi | 0 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |
| H | H.1 Purpose and Relationship to CORP (+4) | 1304 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |

## 8_Rates_and_Revenue (14419 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 114 | AR | - | N | - | front matter |
| rev | Revision History | 225 | AR | - | N | - | front matter |
| abs | Abstract | 344 | AR | - | N | - | front matter |
| gloss | Glossary | 1359 | DL | glossary | N | - | 1,359 words with model figures; merge into the build glossary |
| 1 | 1. The Question This Paper Answers | 441 | D | - | N | - | the question the paper answers |
| 2 | 2. What Taxpayers Actually Pay | 1925 | K | PAY | Y | O2,O3,O2b,O5,O6 | what taxpayers actually pay: revenue-weighted burden and the lifetime effective rate on gains; 204 figures, all v1 [025w: S6 split: who pays (RATES 2, WP 8.2, payslip; map section 7)] |
| 3 | 3. The Revenue Claim | 465 | K | FISC | Y | O1 | the revenue claim and the direction of conservatism; v3 must test whether every assumption still errs low |
| 3.1 | 3.1 Direction of Conservatism | 469 | K | FISC | Y | O1 | the revenue claim and the direction of conservatism; v3 must test whether every assumption still errs low |
| 4 | 4. The Rate Function | 883 | K | FISC | P | - | the logistic rate function; named schedules S_low, S_central, S_high replace the single canonical set |
| 5.1 | 5.1 The Wealth Distribution | 541 | DL | input register | Y | - | wealth distribution (WAS deciles, Pareto tail) and growth model; inputs D4 and D1 |
| 5.2 | 5.2 The Growth Model | 343 | DL | input register | Y | - | wealth distribution (WAS deciles, Pareto tail) and growth model; inputs D4 and D1 |
| 6 | 6. The Two Models and How They Connect | 285 | K | FUND | Y | OP1 | the two models, sizing the short and long reserves |
| 6.1 | 6.1 Sizing the SRR | 428 | K | FUND | Y | OP1 | the two models, sizing the short and long reserves |
| 6.2 | 6.2 Sizing the LRR | 272 | K | FUND | Y | OP1 | the two models, sizing the short and long reserves |
| 6.3 | 6.3 The Two Internal Milestones and What They Gate | 769 | K | FUND | Y | OP1 | the two internal milestones and what they gate |
| 7.1 | 7.1 Revenue Results and Coverage | 623 | K | FISC | Y | O1,O1a | revenue results and coverage at 2000 Balanced parameters (v1) |
| 7.2 | 7.2 Historical Starting-Year Sensitivity | 920 | K | FISC | Y | O1,OP1 | historical start-year sensitivity; v3 level 1 return paths replace it |
| 7.3 | 7.3 SRR and LRR Milestones | 460 | K | FUND | Y | OP1 | SRR and LRR milestones |
| 7.4 | 7.4 Route D Deferred Revenue and Capitalisation Window Timin | 509 | K | FISC | P | NEW:composition | Route D deferred revenue and window timing; needs the share of base on Route D |
| 7.5 | 7.5 Revenue Under the Predicted Declaration Distribution** | 617 | K | FISC | Y | O7,NEW:alpha-curve | revenue under the predicted declaration distribution |
| 8.1 | 8.1 The Corporate Levy | 461 | K | CORP | Y | O1b | corporate levy, v1 figure |
| 8.2 | 8.2 The Ultra-High-Net-Worth Tail | 145 | M | FISC | Y | NEW:payers | UHNW tail beyond the Pareto bound; input D4 |
| 8.3 | 8.3 Combined Pre-Behavioural Estimate | 244 | K | FISC | Y | O1,O1a,O1b | combined pre-behavioural estimate |
| 9 | 9. Limitations and Further Work | 0 | D | - | N | - | empty heading, inherited items, conclusion |
| 9.1 | 9.1 Formal modelling gaps | 171 | M | UNCER | N | - | modelling gaps, pre-behavioural caveat, heterogeneous tier stylisation [025w: was S12; what is not yet known empirically (unknowns, gaps, open questions)] |
| 9.2 | 9.2 Phase One empirical unknowns | 185 | M | UNCER | N | - | modelling gaps, pre-behavioural caveat, heterogeneous tier stylisation [025w: was S12; what is not yet known empirically (unknowns, gaps, open questions)] |
| 9.3 | 9.3 Jurisdiction-specific legal and implementation work | 30 | D | - | N | - | empty heading, inherited items, conclusion |
| 9.4 | 9.4 Structural and irreducible limits of the design | 221 | M | LIMIT | N | - | modelling gaps, pre-behavioural caveat, heterogeneous tier stylisation [025w: was S12; structural limit of the design] |
| 9.5 | 9.5 Governing Council calibration parameters | 114 | DL | parameter register | N | - | criteria for declaring SRR fill |
| 10 | 10. Conclusion | 856 | D | - | N | - | empty heading, inherited items, conclusion |

## 8a_Rates_and_Revenue_Appendix (7969 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 99 | AR | - | N | - | front matter |
| rev | Revision History | 62 | AR | - | N | - | front matter |
| ~A. | A. Model Specification | 0 | AR | - | N | - | specification of the v1 model; v1 is legacy and v3 replaces it |
| A.1 | A.1 Purpose | 206 | AR | - | N | - | specification of the v1 model; v1 is legacy and v3 replaces it |
| A.2 | A.2 Architecture | 398 | AR | - | N | - | specification of the v1 model; v1 is legacy and v3 replaces it |
| A.3 | A.3 Inputs | 478 | AR | - | N | - | specification of the v1 model; v1 is legacy and v3 replaces it |
| A.4 | A.4 SSM Mechanics | 601 | AR | - | N | - | specification of the v1 model; v1 is legacy and v3 replaces it |
| A.5 | A.5 TCM Mechanics | 291 | AR | - | N | - | specification of the v1 model; v1 is legacy and v3 replaces it |
| A.6 | A.6 Coverage Metrics | 781 | AR | - | N | - | specification of the v1 model; v1 is legacy and v3 replaces it |
| A.7 | A.7 Reproducibility | 165 | AR | - | N | - | specification of the v1 model; v1 is legacy and v3 replaces it |
| ~B. | B. Model Output | 12 | AR | - | Y | O1,OP1,O2,O3,NEW:reserve-solvency | v1 run output (2000 Balanced), start-year sweep of 73 years, 100% success; superseded, v3 regenerates |
| B.1 | B.1 Active Parameters | 121 | AR | - | Y | O1,OP1,O2,O3,NEW:reserve-solvency | v1 run output (2000 Balanced), start-year sweep of 73 years, 100% success; superseded, v3 regenerates |
| B.2 | B.2 SSM Results — Active Scenario | 202 | AR | - | Y | O1,OP1,O2,O3,NEW:reserve-solvency | v1 run output (2000 Balanced), start-year sweep of 73 years, 100% success; superseded, v3 regenerates |
| B.3 | B.3 TCM Results — snapshot N=19 (cap. window) / N=30 (lifeti | 1930 | AR | - | Y | O1,OP1,O2,O3,NEW:reserve-solvency | v1 run output (2000 Balanced), start-year sweep of 73 years, 100% success; superseded, v3 regenerates |
| B.4 | B.4 Start-Year Sweep (+2) | 2258 | AR | - | Y | O1,OP1,O2,O3,NEW:reserve-solvency | v1 run output (2000 Balanced), start-year sweep of 73 years, 100% success; superseded, v3 regenerates |
| B.5 | B.5 Statistical Pass — P(success) Across Economic Cycles (+3 | 365 | AR | - | Y | O1,OP1,O2,O3,NEW:reserve-solvency | v1 run output (2000 Balanced), start-year sweep of 73 years, 100% success; superseded, v3 regenerates |

## 9_Parameter_Sweeps (17730 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 108 | AR | - | N | - | front matter |
| rev | Revision History | 186 | AR | - | N | - | front matter |
| abs | Abstract | 216 | AR | - | N | - | front matter |
| gloss | Glossary | 481 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. Introduction | 383 | D | - | N | - | introduction, conclusion, open questions covered by the feasibility map |
| 2 | 2. What the Sweeps Are Measuring | 51 | M | FISC | Y | NEW:feasibility-map | what the sweeps measure; v3 replaces the properties with the feasibility map |
| 2.1 | 2.1 The Tolerant Zone and Fiscal Coverage | 166 | M | FISC | Y | NEW:feasibility-map | what the sweeps measure; v3 replaces the properties with the feasibility map |
| 2.2 | 2.2 The N-Crossing Threshold and LRR Fill Year | 783 | M | FISC | Y | NEW:feasibility-map | what the sweeps measure; v3 replaces the properties with the feasibility map |
| 2.3 | 2.3 The Understater Penalty Plateau and What It Indicates | 562 | M | FISC | Y | NEW:feasibility-map | what the sweeps measure; v3 replaces the properties with the feasibility map |
| 2.4 | 2.4 Reading the Two Datasets in Parallel | 347 | M | FISC | Y | NEW:feasibility-map | what the sweeps measure; v3 replaces the properties with the feasibility map |
| 3 | 3. $\tau_0$ — The Entry Rate | 26 | M | FISC | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 3.1 | 3.1 What $\tau_0$ Controls on the Declaration Mechanism (SWE | 889 | M | FISC | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 3.2 | 3.2 What $\tau_0$ Controls on Fiscal Outcomes (SWEEPS.R) | 446 | M | FISC | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 3.3 | 3.3 What the Council Is Calibrating When It Sets $\tau_0$ | 266 | M | FISC | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 4 | 4. $\tau_m$ — The Ceiling Rate | 35 | M | FISC | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 4.1 | 4.1 What $\tau_m$ Controls on the Declaration Mechanism (SWE | 560 | M | FISC | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 4.2 | 4.2 What $\tau_m$ Controls on Fiscal Outcomes (SWEEPS.R) | 323 | M | FISC | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 4.3 | 4.3 What the Council Is Calibrating When It Sets $\tau_m$ | 294 | M | FISC | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 5 | 5. $k$ — The Steepness Parameter | 173 | M | FISC | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 5.1 | 5.1 What $k$ Controls on the Declaration Mechanism (SWEEPS.V | 770 | M | FISC | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 5.2 | 5.2 What $k$ Controls on Fiscal Outcomes (SWEEPS.R) | 407 | M | FISC | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 5.3 | 5.3 What the Council Is Calibrating When It Sets k | 303 | M | FISC | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 6 | 6. $W_{min}$ — The Exemption Threshold | 215 | M | FISC | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 6.1 | 6.1 What $W_{min}$ Controls on the Declaration Mechanism (SW | 500 | M | FISC | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 6.2 | 6.2 What $W_{min}$ Controls on Fiscal Outcomes (SWEEPS.R) | 377 | M | FISC | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 6.3 | 6.3 What the Council Is Calibrating When It Sets $W_{min}$ | 369 | M | FISC | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 7 | 7. The Parameter Hierarchy and Its Two Faces | 0 | DL | parameter register | N | - | operational parameters (premium, final-charge ramp, rotation pace, privacy differential, facility) |
| 7.1 | 7.1 The Two Hierarchies | 738 | K | FISC | Y | NEW:tornado | the two parameter hierarchies (fiscal and mechanism) |
| 7.2 | 7.2 Chamber Positions and the Stabilising Effect of Disagree | 970 | M | GOV | P | - | chamber positions on parameters and the stabilising effect of disagreement |
| 7.3 | 7.3 Growth Rate Sensitivity | 608 | K | FISC | Y | O1 | growth-rate sensitivity; covered by level 1 return paths |
| 7.4 | 7.4 Cross-Parameter Coverage Fan | 438 | M | FISC | Y | NEW:feasibility-map | cross-parameter coverage fan |
| 7.5 | 7.5 Synthetic Stress-Test: Cyclical Growth Scenarios | 775 | K | FALS | Y | NEW:stress | synthetic cyclical growth stress test; covered only if level 1 sampling includes synthetic cycles [025w: was S12; the stress test is CK1, which the manifest gives to FALS] |
| 8 | 8. The Operational Parameters | 46 | DL | parameter register | N | - | operational parameters (premium, final-charge ramp, rotation pace, privacy differential, facility) |
| 8.1 | 8.1 The Assessment Window Premium | 90 | DL | parameter register | N | - | operational parameters (premium, final-charge ramp, rotation pace, privacy differential, facility) |
| 8.2 | 8.2 The $\tau_{h}$ Ramp | 123 | DL | parameter register | N | - | operational parameters (premium, final-charge ramp, rotation pace, privacy differential, facility) |
| 8.3 | 8.3 The LRR Drawdown Pace | 1331 | M | FUND | P | - | LRR drawdown pace and chamber positions |
| 8.4 | 8.4 Route C Rotation Pace | 109 | DL | parameter register | N | - | operational parameters (premium, final-charge ramp, rotation pace, privacy differential, facility) |
| 8.5 | 8.5 The Privacy Rate Differential | 114 | DL | parameter register | N | - | operational parameters (premium, final-charge ramp, rotation pace, privacy differential, facility) |
| 8.6 | 8.6 Corporate Facility Parameters | 96 | DL | parameter register | N | - | operational parameters (premium, final-charge ramp, rotation pace, privacy differential, facility) |
| 9 | 9. The Small Lever Set as a Design Feature | 514 | K | FISC | N | - | the small lever set as a design feature |
| 10 | 10. What Phase One Needs to Measure for Calibration | 466 | M | POL | N | - | what Phase One needs to measure |
| 11 | 11. Limitations | 1211 | M | UNCER | P | - | limitations of the sweeps (single reference taxpayer, population extrapolation) [025w: was S12; limits of the sweeps are method gaps, not design limits; LIMIT also fits] |
| 12 | 12. Conclusion | 627 | D | - | N | - | introduction, conclusion, open questions covered by the feasibility map |
| 13 | 13. Open Questions | 0 | D | - | N | - | introduction, conclusion, open questions covered by the feasibility map |
| 13.1 | 13.1 The Revenue Frontier | 68 | D | - | N | - | introduction, conclusion, open questions covered by the feasibility map |
| 13.2 | 13.2 Custodian Mandate: SRR Buffer Condition for Drawdown Ac | 170 | D | - | N | - | introduction, conclusion, open questions covered by the feasibility map |

## 9a_Parameter_Sweeps_Appendix (17954 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 97 | AR | - | N | - | front matter |
| rev | Revision History | 60 | AR | - | N | - | front matter |
| ~A. | A. Appendix Tables | 359 | AR | - | Y | NEW:feasibility-map | v1 heatmaps and figure index for the four parameters (C.1 metric across alpha and g) |
| A.1 | A.1 SWEEPS.R — $\tau_0$ Sweep | 446 | AR | - | Y | NEW:feasibility-map | v1 heatmaps and figure index for the four parameters (C.1 metric across alpha and g) |
| A.2 | A.2 SWEEPS.R — $\tau_m$ Sweep | 393 | AR | - | Y | NEW:feasibility-map | v1 heatmaps and figure index for the four parameters (C.1 metric across alpha and g) |
| A.3 | A.3 SWEEPS.R — $k$ Sweep | 444 | AR | - | Y | NEW:feasibility-map | v1 heatmaps and figure index for the four parameters (C.1 metric across alpha and g) |
| A.4 | A.4 SWEEPS.R — $W_{min}$ Sweep | 500 | AR | - | Y | NEW:feasibility-map | v1 heatmaps and figure index for the four parameters (C.1 metric across alpha and g) |
| A.5 | A.5 SWEEPS.V — N Sweep | 246 | AR | - | Y | NEW:feasibility-map | v1 heatmaps and figure index for the four parameters (C.1 metric across alpha and g) |
| A.6 | A.6 SWEEPS.V — $V_0$ Sweep | 245 | AR | - | Y | NEW:feasibility-map | v1 heatmaps and figure index for the four parameters (C.1 metric across alpha and g) |
| A.7 | A.7 SWEEPS.V — $\tau_0$ × N Joint Surface | 213 | AR | - | Y | NEW:feasibility-map | v1 heatmaps and figure index for the four parameters (C.1 metric across alpha and g) |
| A.8 | A.8 SWEEPS.V — $k$ × $V_0$ Joint Surface | 219 | AR | - | Y | NEW:feasibility-map | v1 heatmaps and figure index for the four parameters (C.1 metric across alpha and g) |
| ~B. | B. SWEEPS.V Figure Index | 314 | AR | - | Y | NEW:feasibility-map | v1 heatmaps and figure index for the four parameters (C.1 metric across alpha and g) |
| B.1 | B.1  $\tau_0$ Sweep — C.1 metric across $\alpha$ and $g$ (+6 | 1425 | AR | - | Y | NEW:feasibility-map | v1 heatmaps and figure index for the four parameters (C.1 metric across alpha and g) |
| B.2 | B.2  $\tau_m$ Sweep — C.1 metric across $\alpha$ and $g$ (+4 | 951 | AR | - | Y | NEW:feasibility-map | v1 heatmaps and figure index for the four parameters (C.1 metric across alpha and g) |
| B.3 | B.3  $k$ Sweep — C.1 metric across $\alpha$ and $g$ (+9) | 2116 | AR | - | Y | NEW:feasibility-map | v1 heatmaps and figure index for the four parameters (C.1 metric across alpha and g) |
| B.4 | B.4  N Sweep — C.1 metric at four holding periods (+5) | 550 | AR | - | Y | NEW:feasibility-map | v1 heatmaps and figure index for the four parameters (C.1 metric across alpha and g) |
| B.5 | B.5  $V_0$ Sweep — C.1 metric at four wealth levels (+8) | 934 | AR | - | Y | NEW:feasibility-map | v1 heatmaps and figure index for the four parameters (C.1 metric across alpha and g) |
| B.6 | B.6  $\tau_0$ × N Joint Surface — N-crossing for $\alpha$ = | 475 | AR | - | Y | NEW:feasibility-map | v1 heatmaps and figure index for the four parameters (C.1 metric across alpha and g) |
| B.7 | B.7  $k$ × $V_0$ Joint Surface — C.1 Bracket Penalty for $\a | 207 | AR | - | Y | NEW:feasibility-map | v1 heatmaps and figure index for the four parameters (C.1 metric across alpha and g) |
| B.8 | B.8  $W_{min}$ Sweep — C.1 metric across $\alpha$ and $g$ (+ | 1534 | AR | - | Y | NEW:feasibility-map | v1 heatmaps and figure index for the four parameters (C.1 metric across alpha and g) |
| B.9 | B.9  Figure Index | 739 | AR | - | Y | NEW:feasibility-map | v1 heatmaps and figure index for the four parameters (C.1 metric across alpha and g) |
| ~C. | C. WDT Rate Parameter Sensitivity Sweep | 23 | AR | - | Y | NEW:feasibility-map,NEW:tornado | v1 rate-parameter sensitivity sweep (v8 model) |
| C.1 | C.1 Purpose (+3) | 367 | AR | - | Y | NEW:feasibility-map,NEW:tornado | v1 rate-parameter sensitivity sweep (v8 model) |
| C.2 | C.2 Floor Rate ($\tau_0$) (+1) | 740 | AR | - | Y | NEW:feasibility-map,NEW:tornado | v1 rate-parameter sensitivity sweep (v8 model) |
| C.3 | C.3 Ceiling Rate ($\tau_m$) (+1) | 789 | AR | - | Y | NEW:feasibility-map,NEW:tornado | v1 rate-parameter sensitivity sweep (v8 model) |
| C.4 | C.4 Steepness ($k$) (+1) | 679 | AR | - | Y | NEW:feasibility-map,NEW:tornado | v1 rate-parameter sensitivity sweep (v8 model) |
| C.5 | C.5 Entry Point ($W_{min}$) (+1) | 677 | AR | - | Y | NEW:feasibility-map,NEW:tornado | v1 rate-parameter sensitivity sweep (v8 model) |
| C.6 | C.6 SRR Capitalisation Ratio (srr_ratio) (+1) | 734 | AR | - | Y | NEW:feasibility-map,NEW:tornado | v1 rate-parameter sensitivity sweep (v8 model) |
| C.7 | C.7 LRR Floor (lrr_years) (+1) | 750 | AR | - | Y | NEW:feasibility-map,NEW:tornado | v1 rate-parameter sensitivity sweep (v8 model) |
| C.8 | C.8 Mean Growth Rate (g) | 229 | AR | - | Y | NEW:feasibility-map,NEW:tornado | v1 rate-parameter sensitivity sweep (v8 model) |
| C.9 | C.9 Synthetic Growth Scenario (+2) | 327 | AR | - | Y | NEW:feasibility-map,NEW:tornado | v1 rate-parameter sensitivity sweep (v8 model) |
| ~D. | D. Reading Notes | 172 | D | - | N | - | reading notes |

## 10_Behavioural_Robustness_and_Administrative_Experience (8803 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 119 | AR | - | N | - | front matter |
| rev | Revision History | 219 | AR | - | N | - | front matter |
| abs | Abstract | 255 | AR | - | N | - | front matter |
| gloss | Glossary | 487 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. Introduction | 371 | M | BEHAV | N | - | introduction; complexity objection [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 2 | 2. Why Behaviour Cannot Be Predicted | 0 | K | BEHAV | N | - | why behaviour cannot be predicted; robustness as a design objective [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 2.1 | 2.1 What the Evidence Shows | 193 | K | BEHAV | N | - | why behaviour cannot be predicted; robustness as a design objective [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 2.2 | 2.2 Why the Numbers Don't Travel | 118 | K | BEHAV | N | - | why behaviour cannot be predicted; robustness as a design objective [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 2.3 | 2.3 The Design Implication | 73 | K | BEHAV | N | - | why behaviour cannot be predicted; robustness as a design objective [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 3 | 3. Behavioural Robustness as a Design Objective | 0 | K | BEHAV | N | - | why behaviour cannot be predicted; robustness as a design objective [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 3.1 | 3.1 The Concept Defined | 75 | K | BEHAV | N | - | why behaviour cannot be predicted; robustness as a design objective [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 3.2 | 3.2 What Robustness Is Not | 117 | K | BEHAV | N | - | why behaviour cannot be predicted; robustness as a design objective [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 3.3 | 3.3 The Same Logic Applied Twice | 72 | K | BEHAV | N | - | why behaviour cannot be predicted; robustness as a design objective [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 4 | 4. Sources of Behavioural Friction | 40 | K | BEHAV | N | - | five types of behavioural friction [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 4.1 | 4.1 Type I — Information Friction | 79 | K | BEHAV | N | - | five types of behavioural friction [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 4.2 | 4.2 Type II — Visibility Friction | 81 | K | BEHAV | N | - | five types of behavioural friction [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 4.3 | 4.3 Type III — Legitimacy Friction | 71 | K | BEHAV | N | - | five types of behavioural friction [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 4.4 | 4.4 Type IV — Feedback Friction | 57 | K | BEHAV | N | - | five types of behavioural friction [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 4.5 | 4.5 Type V — Compliance Friction | 85 | K | BEHAV | N | - | five types of behavioural friction [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 4.6 | 4.6 The Design Implication | 40 | K | BEHAV | N | - | five types of behavioural friction [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 5 | 5. Design Principles for Behavioural Robustness | 14 | M | BEHAV | N | - | five design principles [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 5.1 | 5.1 The Clarity Principle | 73 | M | BEHAV | N | - | five design principles [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 5.2 | 5.2 The Reciprocity Principle | 74 | M | BEHAV | N | - | five design principles [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 5.3 | 5.3 The Fairness Principle | 59 | M | BEHAV | N | - | five design principles [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 5.4 | 5.4 The Responsiveness Principle | 59 | M | BEHAV | N | - | five design principles [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 5.5 | 5.5 The Accessibility Principle | 59 | M | BEHAV | N | - | five design principles [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 5.6 | 5.6 The Personal Adviser Corps | 185 | K | BEHAV | N | - | Personal Adviser Corps [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 6 | 6. The Membrane | 0 | K | BEHAV | N | - | the Membrane: definition, health, how the WDT satisfies the principles [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 6.1 | 6.1 Definition | 130 | K | BEHAV | N | - | the Membrane: definition, health, how the WDT satisfies the principles [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 6.2 | 6.2 Membrane Health | 90 | K | BEHAV | N | - | the Membrane: definition, health, how the WDT satisfies the principles [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 6.3 | 6.3 The Interaction Structure of Membrane Health Dimensions | 944 | AR | - | N | - | interaction structure of membrane health dimensions (944 words, table) |
| 6.4 | 6.4 How the WDT Satisfies the Five Principles | 498 | K | BEHAV | N | - | the Membrane: definition, health, how the WDT satisfies the principles [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 7 | 7. The Nine Behavioural Shapes | 41 | K | BEHAV | P | - | nine behavioural shapes; no v3 output models shapes, only the driver D5 range [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 7.1 | 7.1 Shape 1 — Full Cooperative Compliance | 50 | K | BEHAV | P | - | nine behavioural shapes; no v3 output models shapes, only the driver D5 range [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 7.2 | 7.2 Shape 2 — Passive Non-Optimisation | 69 | K | BEHAV | P | - | nine behavioural shapes; no v3 output models shapes, only the driver D5 range [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 7.3 | 7.3 Shape 3 — Active Optimisation Within the Rules | 80 | K | BEHAV | P | - | nine behavioural shapes; no v3 output models shapes, only the driver D5 range [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 7.4 | 7.4 Shape 4 — Avoidance Through Restructuring | 88 | K | BEHAV | P | - | nine behavioural shapes; no v3 output models shapes, only the driver D5 range [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 7.5 | 7.5 Shape 5 — Deferral and Timing Manipulation | 79 | K | BEHAV | P | - | nine behavioural shapes; no v3 output models shapes, only the driver D5 range [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 7.6 | 7.6 Shape 6 — Migration of Assets Without Personal Exit | 70 | K | BEHAV | P | - | nine behavioural shapes; no v3 output models shapes, only the driver D5 range [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 7.7 | 7.7 Shape 7 — Personal Exit | 130 | K | BEHAV | P | - | nine behavioural shapes; no v3 output models shapes, only the driver D5 range [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 7.8 | 7.8 Shape 8 — Partial Exit | 83 | K | BEHAV | P | - | nine behavioural shapes; no v3 output models shapes, only the driver D5 range [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 7.9 | 7.9 Shape 9 — Active Resistance and Non-Compliance | 114 | K | BEHAV | P | - | nine behavioural shapes; no v3 output models shapes, only the driver D5 range [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 7.10 | 7.10 The Distribution as a Whole | 82 | K | BEHAV | P | - | nine behavioural shapes; no v3 output models shapes, only the driver D5 range [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 8 | 8. The Enforcement Paradigm Shift | 0 | K | BEHAV | N | - | passive collection rather than active detection [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 8.1 | 8.1 Passive Collection Rather Than Active Detection | 301 | K | BEHAV | N | - | passive collection rather than active detection [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 8.2 | 8.2 The Route Distribution | 441 | K | BEHAV | Y | NEW:composition | route distribution: Route D 10 to 20% of taxable wealth; share of base by route is an input [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 9 | 9. Principal Objections | 0 | K | BEHAV | P | - | the wealthy will leave [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 9.1 | 9.1 The Wealthy Will Leave | 263 | K | BEHAV | P | - | the wealthy will leave [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 9.2 | 9.2 The Cross-Base Fiscal Externality | 422 | K | BEHAV | Y | NEW:cross-base | cross-base fiscal externality (Agrawal); net fiscal effect after migration is not an output [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 9.3 | 9.3 The Complexity Objection | 107 | M | BEHAV | N | - | introduction; complexity objection [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 9.4 | 9.4 The Membrane Is Undeliverable | 75 | M | LIMIT | N | - | undeliverable membrane, rebranding failure, modelling gaps, Agrawal net-effect question [025w: was S12; structural limit of the design] |
| 9.5 | 9.5 Robustness Is Rebranding Failure | 91 | M | LIMIT | N | - | undeliverable membrane, rebranding failure, modelling gaps, Agrawal net-effect question [025w: was S12; structural limit of the design] |
| 10 | 10. Phase Sequencing | 0 | M | POL | N | - | phase sequencing; duplicates WP 7 and PHASE1 |
| 10.1 | 10.1 Phase One — Implementation | 126 | M | POL | N | - | phase sequencing; duplicates WP 7 and PHASE1 |
| 10.2 | 10.2 Phase Two — Stabilisation | 112 | M | POL | N | - | phase sequencing; duplicates WP 7 and PHASE1 |
| 10.3 | 10.3 Phase Three and Membrane Calcification | 71 | M | POL | N | - | phase sequencing; duplicates WP 7 and PHASE1 |
| 10.4 | 10.4 Sequencing as a Design Variable | 67 | M | POL | N | - | phase sequencing; duplicates WP 7 and PHASE1 |
| 11 | 11. Limitations | 0 | D | - | N | - | limitations register and conclusion |
| 11.1 | 11.1 Formal Modelling Gaps | 264 | M | UNCER | N | - | undeliverable membrane, rebranding failure, modelling gaps, Agrawal net-effect question [025w: was S12; what is not yet known empirically (unknowns, gaps, open questions)] |
| 11.2 | 11.2 Phase One Empirical Unknowns | 130 | M | UNCER | N | - | undeliverable membrane, rebranding failure, modelling gaps, Agrawal net-effect question [025w: was S12; what is not yet known empirically (unknowns, gaps, open questions)] |
| 11.3 | 11.3 Structural Limits of the Design | 121 | D | - | N | - | limitations register and conclusion |
| 11.4 | 11.4 Governing Council Calibration Parameters | 6 | D | - | N | - | limitations register and conclusion |
| 12 | 12. Conclusion | 583 | D | - | N | - | limitations register and conclusion |

## 10a_Behavioural_Robustness_and_Administrative_Experience_Appendix (4643 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 85 | AR | - | N | - | front matter |
| rev | Revision History | 57 | AR | - | N | - | front matter |
| ~A. | A. Route Distribution and Enforcement Residual | 52 | DL | input register | Y | NEW:composition | asset-class walkthrough by route; feeds the share of base by route |
| A.1 | A.1 Classification Logic | 186 | DL | input register | Y | NEW:composition | asset-class walkthrough by route; feeds the share of base by route |
| A.2 | A.2 Route A — Professional Valuation, Fungible | 191 | DL | input register | Y | NEW:composition | asset-class walkthrough by route; feeds the share of base by route |
| A.3 | A.3 Route C — Self-Declaration, Fungible | 150 | DL | input register | Y | NEW:composition | asset-class walkthrough by route; feeds the share of base by route |
| A.4 | A.4 Route B — Professional Valuation, Non-Fungible | 189 | DL | input register | Y | NEW:composition | asset-class walkthrough by route; feeds the share of base by route |
| A.5 | A.5 Route D — Self-Declaration, Non-Fungible | 233 | DL | input register | Y | NEW:composition | asset-class walkthrough by route; feeds the share of base by route |
| A.6 | A.6 Edge Cases and Classification Ambiguities | 320 | M | VAL | N | - | classification edge cases; why the bias toward Routes A and B is structurally positive [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| A.7 | A.7 Why the Bias Toward Routes A and B Is Structurally Posit | 273 | M | VAL | N | - | classification edge cases; why the bias toward Routes A and B is structurally positive [025w: S4 split: valuation routes (VAL 1 to 6 and 9 to 12; map section 7)] |
| ~B. | B. Membrane Calcification and the Monitoring Architecture | 28 | M | LIMIT | N | - | membrane calcification, the honest limit [025w: was S12; structural limit of the design] |
| B.1 | B.1 The Nature of the Problem | 217 | M | LIMIT | N | - | membrane calcification, the honest limit [025w: was S12; structural limit of the design] |
| B.2 | B.2 The Monitoring Instrument | 135 | AR | - | N | - | monitoring architecture detail |
| B.3 | B.3 The Taxpayer Chamber as Monitor | 120 | AR | - | N | - | monitoring architecture detail |
| B.4 | B.4 The Internal TP Voting Structure | 222 | AR | - | N | - | monitoring architecture detail |
| B.5 | B.5 The Allocator as Fairness Signal | 143 | AR | - | N | - | monitoring architecture detail |
| B.6 | B.6 The TP/DR Coalition and the FS Constraint | 130 | AR | - | N | - | monitoring architecture detail |
| B.7 | B.7 The Honest Limit | 138 | M | LIMIT | N | - | membrane calcification, the honest limit [025w: was S12; structural limit of the design] |
| ~C. | C. The Membrane in Practice — Institutional Examples | 25 | AR | - | N | - | membrane examples from banking, water and insurance |
| C.1 | C.1 A Healthy Membrane — Retail Banking | 145 | AR | - | N | - | membrane examples from banking, water and insurance |
| C.2 | C.2 Monopoly-Induced Degradation — Water Utilities | 191 | AR | - | N | - | membrane examples from banking, water and insurance |
| C.3 | C.3 Interest-Aligned Degradation — Mandatory Insurance Marke | 214 | AR | - | N | - | membrane examples from banking, water and insurance |
| ~D. | D. The Cross-Base Fiscal Externality — Full Response | 64 | K | BEHAV | P | NEW:cross-base | seven-part response to the Agrawal finding [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| D.1 | D.1 The Jurisdictional Transfer Caveat | 167 | K | BEHAV | P | NEW:cross-base | seven-part response to the Agrawal finding [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| D.2 | D.2 The Rate Calibration Lever | 142 | K | BEHAV | P | NEW:cross-base | seven-part response to the Agrawal finding [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| D.3 | D.3 The Timeline Extension Buffer | 147 | K | BEHAV | P | NEW:cross-base | seven-part response to the Agrawal finding [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| D.4 | D.4 The Re-Entry Rule and the Externality's Temporal Shape | 187 | K | BEHAV | P | NEW:cross-base | seven-part response to the Agrawal finding [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| D.5 | D.5 The Immigration Possibility | 492 | K | BEHAV | P | NEW:cross-base | seven-part response to the Agrawal finding [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |

## 11_Position_Closure (11415 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 106 | AR | - | N | - | front matter |
| rev | Revision History | 219 | AR | - | N | - | front matter |
| abs | Abstract | 196 | AR | - | N | - | front matter |
| gloss | Glossary | 761 | DL | glossary | N | - | 761 words; merge into the build glossary |
| 1 | 1. Intellectual Context and Prior Literature | 43 | M | LIT | N | - | exit tax, migration and insolvency literature |
| 1.1 | 1.1 Conventional Exit Tax Design | 142 | M | LIT | N | - | exit tax, migration and insolvency literature |
| 1.2 | 1.2 The Wealth Tax Migration Literature | 285 | M | LIT | N | - | exit tax, migration and insolvency literature |
| 1.3 | 1.3 Insolvency and Taxation | 96 | M | LIT | N | - | exit tax, migration and insolvency literature |
| 1.4 | 1.4 What the Literature Leaves Unresolved | 121 | M | LIT | N | - | exit tax, migration and insolvency literature |
| 2 | 2. The General Theory of Position Closure | 826 | K | MECH | N | - | general theory of position closure; what the mechanism owes at closure |
| 3 | 3. What the Mechanism Owes at Closure | 587 | K | MECH | N | - | general theory of position closure; what the mechanism owes at closure |
| 4 | 4. The Four Closure Event Types | 0 | K | MECH | N | - | death, death auction waiver, exit, bankruptcy |
| 4.1 | 4.1 Death | 1198 | K | MECH | N | - | death, death auction waiver, exit, bankruptcy |
| 4.1.1 | 4.1.1 The Death Auction Waiver | 431 | K | MECH | N | - | death, death auction waiver, exit, bankruptcy |
| 4.2 | 4.2 Jurisdictional Exit | 413 | K | MECH | N | - | death, death auction waiver, exit, bankruptcy |
| 4.3 | 4.3 Threshold Fall-Through | 425 | K | MECH | P | NEW:payers | threshold fall-through; refund volume at fall-through grows as the threshold drops |
| 4.4 | 4.4 Bankruptcy | 460 | K | MECH | N | - | death, death auction waiver, exit, bankruptcy |
| 4.5 | 4.5 Incarceration and Criminal Forfeiture (+4) | 1226 | AR | - | N | - | incarceration and criminal forfeiture; edge-case rules for statute drafting |
| 5 | 5. The Closure Bond Facility | 109 | K | FUND | N | - | closure bond facility (SWF) |
| 5.1 | 5.1 Bond Mechanics | 321 | K | FUND | N | - | closure bond facility (SWF) |
| 5.2 | 5.2 Death Variant | 130 | K | FUND | N | - | closure bond facility (SWF) |
| 5.3 | 5.3 Exit Variant | 182 | K | FUND | N | - | closure bond facility (SWF) |
| 5.4 | 5.4 Bankruptcy Variant | 217 | K | FUND | N | - | closure bond facility (SWF) |
| 6 | 6. The Re-entry Rule | 486 | K | MECH | N | - | the re-entry rule |
| 7 | 7. Phase Sequencing | 0 | M | POL | N | - | phase sequencing |
| 7.1 | 7.1 Phase One | 236 | M | POL | N | - | phase sequencing |
| 7.2 | 7.2 Phase Two | 168 | M | POL | N | - | phase sequencing |
| 8 | 8. Principal Objections | 0 | K | BEHAV | N | - | compulsion and double taxation objections to exit closure [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 8.1 | 8.1 The Compulsion Objection | 202 | K | BEHAV | N | - | compulsion and double taxation objections to exit closure [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 8.2 | 8.2 The Double Taxation Objection | 122 | K | BEHAV | N | - | compulsion and double taxation objections to exit closure [025w: S6 split: what they do (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3, 8.7; map section 7)] |
| 8.3 | 8.3 The Re-entry Asymmetry Objection | 190 | M | MECH | N | - | re-entry asymmetry and beyond-lifetime-cap objections |
| 8.4 | 8.4 The Beyond-Lifetime-Cap Objection | 504 | M | MECH | N | - | re-entry asymmetry and beyond-lifetime-cap objections |
| 9 | 9. Limitations and Required Further Work | 0 | D | - | N | - | limitations register and conclusion |
| 9.1 | 9.1 Formal modelling gaps | 5 | D | - | N | - | limitations register and conclusion |
| 9.2 | 9.2 Phase One empirical unknowns | 157 | M | UNCER | P | - | number of exits and fall-through rates unknown [025w: was S12; what is not yet known empirically (unknowns, gaps, open questions)] |
| 9.3 | 9.3 Jurisdiction-specific legal and implementation work | 206 | D | - | N | - | limitations register and conclusion |
| 9.4 | 9.4 Structural and irreducible limits of the design | 60 | D | - | N | - | limitations register and conclusion |
| 9.5 | 9.5 Governing Council calibration parameters | 223 | DL | parameter register | N | - | closure bond sizing ratios |
| 10 | 10. Conclusion | 362 | D | - | N | - | limitations register and conclusion |

## 12_Political_Architecture (11664 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 110 | AR | - | N | - | front matter |
| rev | Revision History | 110 | AR | - | N | - | front matter |
| abs | Abstract | 390 | AR | - | N | - | front matter |
| gloss | Glossary | 554 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. Introduction | 305 | D | - | N | - | introduction and conclusion |
| 2 | 2. Intellectual Context and Prior Literature | 395 | M | LIT | N | - | political economy literature |
| 3 | 3. Why Wealth Taxes Fail Politically | 52 | K | POL | N | - | why wealth taxes fail politically: legitimacy, organised opposition, brittleness, the spiral |
| 3.1 | 3.1 The Empirical Pattern | 238 | K | POL | N | - | why wealth taxes fail politically: legitimacy, organised opposition, brittleness, the spiral |
| 3.2 | 3.2 Three Structural Mechanisms | 124 | K | POL | N | - | why wealth taxes fail politically: legitimacy, organised opposition, brittleness, the spiral |
| 3.3 | 3.3 Mechanism One: Legitimacy Collapse | 406 | K | POL | N | - | why wealth taxes fail politically: legitimacy, organised opposition, brittleness, the spiral |
| 3.4 | 3.4 Mechanism Two: Organised Opposition Advantage | 324 | K | POL | N | - | why wealth taxes fail politically: legitimacy, organised opposition, brittleness, the spiral |
| 3.5 | 3.5 Mechanism Three: Institutional Brittleness | 477 | K | POL | N | - | why wealth taxes fail politically: legitimacy, organised opposition, brittleness, the spiral |
| 3.6 | 3.6 The Spiral | 160 | K | POL | N | - | why wealth taxes fail politically: legitimacy, organised opposition, brittleness, the spiral |
| 3.7 | 3.7 Why Revenue Is Not the Failure Mode | 164 | K | POL | N | - | why wealth taxes fail politically: legitimacy, organised opposition, brittleness, the spiral |
| 4 | 4. Political Durability as a Design Property | 665 | K | POL | N | - | political durability as a design property; redundancy; offer to professional services |
| 5 | 5. The WDT's Political Architecture | 175 | K | POL | N | - | political durability as a design property; redundancy; offer to professional services |
| 5.1 | 5.1 The Symmetric Loss-Refund Mechanism | 416 | M | MECH | N | - | symmetric refund; duplicates WP 3.5 |
| 5.2 | 5.2 The Sovereign Wealth Fund | 228 | M | FUND | N | - | the SWF |
| 5.3 | 5.3 The Labour Relief Dividend | 346 | K | FUND | Y | O4a,O4b,NEW:labour-dividend | labour relief dividend; 618 pounds a month at median earnings |
| 5.4 | 5.4 The Taxpayer Chamber | 278 | M | GOV | N | - | Taxpayer Chamber, Dividend Recipient Chamber, enumerated clauses |
| 5.5 | 5.5 The Dividend Recipient Chamber | 262 | M | GOV | N | - | Taxpayer Chamber, Dividend Recipient Chamber, enumerated clauses |
| 5.6 | 5.6 The Enumerated Structural Clauses | 208 | M | GOV | N | - | Taxpayer Chamber, Dividend Recipient Chamber, enumerated clauses |
| 5.7 | 5.7 Redundancy and the Failure Rate | 256 | K | POL | N | - | political durability as a design property; redundancy; offer to professional services |
| 5.8 | 5.8 The Cooperative Offer to the Displaced Professional Serv | 238 | K | POL | N | - | political durability as a design property; redundancy; offer to professional services |
| 6 | 6. The Credibility Bootstrapping Problem | 73 | K | POL | N | - | credibility bootstrapping, vulnerability window, Phase One as a political term |
| 6.1 | 6.1 The Vulnerability Window | 144 | K | POL | N | - | credibility bootstrapping, vulnerability window, Phase One as a political term |
| 6.2 | 6.2 The Accidental Hostage and the Deliberate Stake | 261 | K | POL | N | - | credibility bootstrapping, vulnerability window, Phase One as a political term |
| 6.3 | 6.3 The Thought Experiment | 145 | K | POL | N | - | credibility bootstrapping, vulnerability window, Phase One as a political term |
| 6.4 | 6.4 Phase One Parameters as Politically Determined | 289 | K | POL | N | - | credibility bootstrapping, vulnerability window, Phase One as a political term |
| 6.5 | 6.5 The SRR Milestone as Political Threshold | 268 | K | POL | P | OP1 | SRR milestone as political threshold |
| 6.6 | 6.6 Phase One as a Political Term | 195 | K | POL | N | - | credibility bootstrapping, vulnerability window, Phase One as a political term |
| 6.7 | 6.7 The Calcification Ceiling and the Honest Limitation | 418 | K | POL | N | - | credibility bootstrapping, vulnerability window, Phase One as a political term |
| 7 | 7. The Self-Shaping Problem | 251 | M | LIMIT | N | - | self-shaping problem; objections about falsifiability and circularity; limitations [025w: was S12; structural limit of the design] |
| 8 | 8. Principal Objections | 0 | K | POL | N | - | bootstrapping and too-radical objections |
| 8.1 | 8.1 The Political Durability Claim Is Unfalsifiable | 188 | M | FALS | N | - | self-shaping problem; objections about falsifiability and circularity; limitations [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 8.2 | 8.2 The Redundancy Argument Proves Too Much | 224 | M | FALS | N | - | self-shaping problem; objections about falsifiability and circularity; limitations [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 8.3 | 8.3 The Bootstrapping Problem Is Fatal | 186 | K | POL | N | - | bootstrapping and too-radical objections |
| 8.4 | 8.4 The Tiered Citizenship Risk Is the Point | 259 | M | FAIR | N | - | tiered citizenship objections; duplicate POL.A |
| 8.5 | 8.5 The Existing-Tiers Argument Is a Deflection | 192 | M | FAIR | N | - | tiered citizenship objections; duplicate POL.A |
| 8.6 | 8.6 Democratic Flourishing as the Terminal Goal Is Circular | 237 | M | FALS | N | - | self-shaping problem; objections about falsifiability and circularity; limitations [025w: was S12; objection that the terminal goal is not falsifiable; LIMIT also fits] |
| 8.7 | 8.7 The Governance Structure Is Too Radical to Be Adopted | 231 | K | POL | N | - | bootstrapping and too-radical objections |
| 8.8 | 8.8 The Cross-Base Externality Makes the Emigration Risk Unm | 69 | D | - | N | - | cross-base externality; covered in BEHAV 9.2 |
| 9 | 9. Limitations and Further Work | 0 | D | - | N | - | limitations register |
| 9.1 | 9.1 Formal modelling gaps | 117 | M | UNCER | N | - | self-shaping problem; objections about falsifiability and circularity; limitations [025w: was S12; what is not yet known empirically (unknowns, gaps, open questions)] |
| 9.2 | 9.2 Phase One empirical unknowns | 162 | M | UNCER | N | - | self-shaping problem; objections about falsifiability and circularity; limitations [025w: was S12; what is not yet known empirically (unknowns, gaps, open questions)] |
| 9.3 | 9.3 Jurisdiction-specific legal and implementation work | 26 | D | - | N | - | limitations register |
| 9.4 | 9.4 Structural and irreducible limits of the design | 260 | M | LIMIT | N | - | self-shaping problem; objections about falsifiability and circularity; limitations [025w: was S12; structural limit of the design] |
| 9.5 | 9.5 Governing Council calibration parameters | 6 | D | - | N | - | limitations register |
| 10 | 10. Conclusion | 582 | D | - | N | - | introduction and conclusion |

## 12a_Political_Architecture_Appendix (2046 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 111 | AR | - | N | - | front matter |
| rev | Revision History | 26 | AR | - | N | - | front matter |
| ~A. | A. The Tiered Citizenship Problem | 23 | K | FAIR | N | - | the tiered citizenship problem |
| A.1 | A.1 We Already Live in a Tiered Society | 388 | K | FAIR | N | - | the tiered citizenship problem |
| A.2 | A.2 The Tiered Citizenship Risk | 250 | K | FAIR | N | - | the tiered citizenship problem |
| A.3 | A.3 Why the WDT Is Not Feudalism | 353 | K | FAIR | N | - | the tiered citizenship problem |
| A.4 | A.4 Equality of Outcome Is the Wrong Goal | 223 | K | FAIR | N | - | the tiered citizenship problem |
| A.5 | A.5 The Small Community Illustration | 287 | K | FAIR | N | - | the tiered citizenship problem |
| A.6 | A.6 The Limits of Mechanism | 169 | K | FAIR | N | - | the tiered citizenship problem |
| A.7 | A.7 A Remarkable Problem | 216 | M | LIMIT | N | - | a remarkable problem: success raises the stakes [025w: was S12; structural limit of the design] |

## 13_Phase_One (6635 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 116 | AR | - | N | - | front matter |
| rev | Revision History | 99 | AR | - | N | - | front matter |
| abs | Abstract | 305 | AR | - | N | - | front matter |
| gloss | Glossary | 225 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. Introduction | 244 | D | - | N | - | introduction, conclusion, limitations register |
| 2 | 2. The Boundary of Desk Research | 283 | K | POL | P | - | boundary of desk research; working assumptions in force; v3 ranges replace point assumptions |
| 3 | 3. The Working Assumptions Currently in Force | 690 | K | POL | P | - | boundary of desk research; working assumptions in force; v3 ranges replace point assumptions |
| 4 | 4. The Empirical Clusters | 0 | K | POL | P | - | the seven empirical clusters Phase One must answer |
| 4.1 | 4.1 Behavioural Response to Cooperative Architecture | 228 | K | POL | P | - | the seven empirical clusters Phase One must answer |
| 4.2 | 4.2 Avoidance Under Imperfect Compliance | 244 | K | POL | P | - | the seven empirical clusters Phase One must answer |
| 4.3 | 4.3 Migration and the Cross-Base Externality | 299 | K | POL | P | - | the seven empirical clusters Phase One must answer |
| 4.4 | 4.4 Valuation Route and Assessment Window Adoption | 257 | K | POL | P | - | the seven empirical clusters Phase One must answer |
| 4.5 | 4.5 Administrative Intervention Effects | 332 | K | POL | P | - | the seven empirical clusters Phase One must answer |
| 4.6 | 4.6 OBR Independence — Empirical Assessment | 272 | K | POL | P | - | the seven empirical clusters Phase One must answer |
| 4.7 | 4.7 Corporate Instrument Transition | 212 | K | POL | P | - | the seven empirical clusters Phase One must answer |
| 5 | 5. What Phase One Would Need to Measure | 39 | M | POL | N | - | prospective measurement designs |
| 5.1 | 5.1 Measuring Behavioural Response to the Cooperative Archit | 261 | M | POL | N | - | prospective measurement designs |
| 5.2 | 5.2 Measuring Avoidance Under Imperfect Compliance | 247 | M | POL | N | - | prospective measurement designs |
| 5.3 | 5.3 Measuring the Cross-Base Externality | 281 | M | POL | N | - | prospective measurement designs |
| 5.4 | 5.4 Measuring Valuation Route and Assessment Window Adoption | 204 | M | POL | N | - | prospective measurement designs |
| 5.5 | 5.5 Measuring Administrative Intervention Effects | 340 | M | POL | N | - | prospective measurement designs |
| 5.6 | 5.6 Measuring OBR Independence | 255 | M | POL | N | - | prospective measurement designs |
| 5.7 | 5.7 Measuring the Corporate Instrument Transition | 262 | M | POL | N | - | prospective measurement designs |
| 6 | 6. Limitations and Further Work | 0 | D | - | N | - | introduction, conclusion, limitations register |
| 6.1 | 6.1 Formal modelling gaps | 17 | D | - | N | - | introduction, conclusion, limitations register |
| 6.2 | 6.2 Phase One empirical unknowns | 81 | D | - | N | - | introduction, conclusion, limitations register |
| 6.3 | 6.3 Jurisdiction-specific legal and implementation work | 230 | D | - | N | - | introduction, conclusion, limitations register |
| 6.4 | 6.4 Structural and irreducible limits of the design | 44 | D | - | N | - | introduction, conclusion, limitations register |
| 6.5 | 6.5 Governing Council calibration parameters | 192 | DL | parameter register | N | - | calibration parameters |
| 7 | 7. Conclusion | 376 | D | - | N | - | introduction, conclusion, limitations register |

## 14_Environmental_Effects_and_Transmission_Channels (10385 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 125 | AR | - | N | - | front matter |
| rev | Revision History | 101 | AR | - | N | - | front matter |
| abs | Abstract | 338 | AR | - | N | - | front matter |
| gloss | Glossary | 308 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. The Paper's Place in the Series | 405 | D | - | N | - | place in the series, limitations register, conclusion |
| 2 | 2. The Predicted Rational Equilibrium | 698 | M | DECL | N | - | predicted rational equilibrium; duplicates VAL 7 [025w: S4 split: declaration incentives (VAL 7, VAL.A findings, VAL.B examples; map section 7)] |
| 3 | 3. Capital Allocation and Velocity | 890 | K | WIDER | N | - | capital allocation and velocity (hypothesis H2a) [025w: was S11; longer causal chain, institutional or second-order effect] |
| 4 | 4. The Displacement Channel and Labour Markets | 0 | M | FUND | N | - | staged displacement of labour taxes |
| 4.1 | 4.1 Staged Displacement | 280 | M | FUND | N | - | staged displacement of labour taxes |
| 4.2 | 4.2 The NICs Case | 457 | M | PAY | P | O4a,O4b | NICs case and household effects; duplicate LDW 2 [025w: was S11; duplicates the kept payslip rows of LDW 2 in PAY; FIRST also fits] |
| 4.3 | 4.3 Automation and the Labour Tax Base | 433 | K | WIDER | N | - | automation and the labour tax base, existing responses, tax-base migration, stress test, what the WDT does not solve [025w: was S11; longer causal chain, institutional or second-order effect] |
| 4.4 | 4.4 What Existing Responses Address | 361 | K | WIDER | N | - | automation and the labour tax base, existing responses, tax-base migration, stress test, what the WDT does not solve [025w: was S11; longer causal chain, institutional or second-order effect] |
| 4.5 | 4.5 Tax-Base Migration | 355 | K | WIDER | N | - | automation and the labour tax base, existing responses, tax-base migration, stress test, what the WDT does not solve [025w: was S11; longer causal chain, institutional or second-order effect] |
| 4.6 | 4.6 Displacement Effects on Households | 651 | M | PAY | P | O4a,O4b | NICs case and household effects; duplicate LDW 2 [025w: was S11; duplicates the kept payslip rows of LDW 2 in PAY; FIRST also fits] |
| 4.7 | 4.7 Extreme Automation as a Stress Test | 224 | K | WIDER | N | - | automation and the labour tax base, existing responses, tax-base migration, stress test, what the WDT does not solve [025w: was S11; stress scenario; the H5 falsification conditions sit in FALS] |
| 4.8 | 4.8 What the WDT Does Not Solve | 204 | K | LIMIT | N | - | automation and the labour tax base, existing responses, tax-base migration, stress test, what the WDT does not solve [025w: was S11; what the design does not solve is a structural limit (LIMIT)] |
| 5 | 5. The Consumption Multiplier and Growth Feedback | 795 | K | WIDER | P | - | consumption multiplier and growth feedback; v3 is partial equilibrium, so the claim stays structural [025w: was S11; longer causal chain, institutional or second-order effect] |
| 6 | 6. Financial System Stability | 936 | K | WIDER | N | - | financial system stability; inflation response and countercyclical architecture [025w: was S11; longer causal chain, institutional or second-order effect] |
| 7 | 7. Inflation Response and Countercyclical Architecture | 714 | K | WIDER | N | - | financial system stability; inflation response and countercyclical architecture [025w: was S11; longer causal chain, institutional or second-order effect] |
| 8 | 8. Housing and Distributional Consequences | 374 | K | WIDER | Y | OS1 | housing and distributional consequences; capitalisation of retired property taxes [025w: was S11; longer causal chain, institutional or second-order effect] |
| 9.1 | 9.1 Formal modelling gaps | 88 | D | - | N | - | place in the series, limitations register, conclusion |
| 9.2 | 9.2 Phase One empirical unknowns (+4) | 604 | M | UNCER | N | - | empirical unknowns (multiplier, housing, bias direction, automation) and structural limits [025w: was S12; what is not yet known empirically (unknowns, gaps, open questions)] |
| 9.3 | 9.3 Jurisdiction-specific legal and implementation work | 24 | D | - | N | - | place in the series, limitations register, conclusion |
| 9.4 | 9.4 Structural and irreducible limits of the design | 358 | M | LIMIT | N | - | empirical unknowns (multiplier, housing, bias direction, automation) and structural limits [025w: was S12; structural limit of the design] |
| 9.5 | 9.5 Governing Council calibration parameters | 31 | DL | parameter register | N | - | inflationary rotation trigger |
| 10 | 10. Conclusion | 631 | D | - | N | - | place in the series, limitations register, conclusion |

## 15_First_Mover (4143 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 92 | AR | - | N | - | front matter |
| rev | Revision History | 131 | AR | - | N | - | front matter |
| abs | Abstract | 96 | AR | - | N | - | front matter |
| gloss | Glossary | 346 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. The Binary | 653 | K | POL | N | - | the binary; why the middle option does not exist |
| 2 | 2. Why The Middle Option Doesn't Exist | 945 | K | POL | N | - | the binary; why the middle option does not exist |
| 3 | 3. What Each Strategy Delivers | 0 | K | POL | Y | OP1,O1 | commit and compound; cites the 73-window reserve fill and 125.5% coverage, v1 only |
| 3.1 | 3.1 The First Strategy: Commit and Compound | 546 | K | POL | Y | OP1,O1 | commit and compound; cites the 73-window reserve fill and 125.5% coverage, v1 only |
| 3.2 | 3.2 The Second Strategy: Suppress Before Demonstration | 841 | K | POL | N | - | suppress before demonstration |
| 4 | 4. The Record | 493 | AR | - | N | - | the record as of August 2026; dated |

## 16_Modular_Adoption (2163 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 100 | AR | - | N | - | front matter |
| rev | Revision History | 30 | AR | - | N | - | front matter |
| abs | Abstract | 165 | AR | - | N | - | front matter |
| gloss | Glossary | 213 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. The Two Categories | 366 | K | POL | N | - | the two categories, why infrastructure accrues, what accretion delivers |
| 2 | 2. Why Infrastructure Accrues | 527 | K | POL | N | - | the two categories, why infrastructure accrues, what accretion delivers |
| 3 | 3. What Accretion Delivers | 408 | K | POL | N | - | the two categories, why infrastructure accrues, what accretion delivers |
| 4 | 4. The Relationship to the Binary | 354 | M | POL | N | - | relationship to the binary |

## 17_Scope_Boundary (2811 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 68 | AR | - | N | - | front matter |
| rev | Revision History | 206 | AR | - | N | - | front matter |
| 1 | 1. Purpose | 125 | SA | SCOPE | N | - | the canonical record of questions outside the project; stays outside the wheel (author, 2026-11-16) |
| 2 | 2. Comparative Political Economy and International Coordinat | 552 | SA | SCOPE | N | - | the canonical record of questions outside the project; stays outside the wheel (author, 2026-11-16) |
| 3 | 3. Phase One Empirical Questions (+4) | 903 | SA | SCOPE | N | - | the canonical record of questions outside the project; stays outside the wheel (author, 2026-11-16) |
| 4 | 4. Phase One Successor Tasks | 142 | SA | SCOPE | N | - | the canonical record of questions outside the project; stays outside the wheel (author, 2026-11-16) |
| 5 | 5. Governing Council Calibration Parameters | 273 | SA | SCOPE | N | - | the canonical record of questions outside the project; stays outside the wheel (author, 2026-11-16) |
| 6 | 6. Jurisdiction-Specific and Institutional Preconditions | 407 | SA | SCOPE | N | - | the canonical record of questions outside the project; stays outside the wheel (author, 2026-11-16) |
| 7 | 7. What This Document Is Not Doing | 135 | SA | SCOPE | N | - | the canonical record of questions outside the project; stays outside the wheel (author, 2026-11-16) |

## 18_Addendums (7476 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 105 | AR | - | N | - | front matter |
| rev | Revision History | 130 | AR | - | N | - | front matter |
| abs | Abstract | 172 | AR | - | N | - | front matter |
| gloss | Glossary | 280 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. Introduction | 342 | SA | ADD | N | - | eight implementation calibration questions and open questions; standalone (author, 2026-11-16) |
| 2 | 2. The Nature of Implementation Calibration | 318 | SA | ADD | N | - | eight implementation calibration questions and open questions; standalone (author, 2026-11-16) |
| 3 | 3. Calibration Question One: Exemption Threshold Indexation | 779 | SA | ADD | N | - | eight implementation calibration questions and open questions; standalone (author, 2026-11-16) |
| 4 | 4. Calibration Question Two: TP Chamber Conflict of Interest | 524 | SA | ADD | N | - | eight implementation calibration questions and open questions; standalone (author, 2026-11-16) |
| 5 | 5. Calibration Question Three: External Chamber Communicatio | 480 | SA | ADD | N | - | eight implementation calibration questions and open questions; standalone (author, 2026-11-16) |
| 6 | 6. Calibration Question Four: DR Chamber Eligible Pool Monit | 429 | SA | ADD | N | - | eight implementation calibration questions and open questions; standalone (author, 2026-11-16) |
| 7 | 7. Calibration Question Five: The Consumption Delta (+4) | 643 | SA | ADD | N | - | eight implementation calibration questions and open questions; standalone (author, 2026-11-16) |
| 8 | 8. Calibration Question Six: SWF Asset Composition Monitorin | 441 | SA | ADD | N | - | eight implementation calibration questions and open questions; standalone (author, 2026-11-16) |
| 9 | 9. Calibration Question Seven: Phase One Measurement Framewo | 491 | SA | ADD | N | - | eight implementation calibration questions and open questions; standalone (author, 2026-11-16) |
| 10 | 10. Calibration Question Eight: The Bootstrapping Facility ( | 751 | SA | ADD | N | - | eight implementation calibration questions and open questions; standalone (author, 2026-11-16) |
| 11 | 11. The Relationship Between These Questions | 325 | SA | ADD | N | - | eight implementation calibration questions and open questions; standalone (author, 2026-11-16) |
| 12 | 12. Limitations and Further Work | 342 | SA | ADD | N | - | eight implementation calibration questions and open questions; standalone (author, 2026-11-16) |
| 13 | 13. Conclusion | 462 | SA | ADD | N | - | eight implementation calibration questions and open questions; standalone (author, 2026-11-16) |
| 14 | 14. Open Questions (+5) | 462 | SA | ADD | N | - | eight implementation calibration questions and open questions; standalone (author, 2026-11-16) |

## 19_Taxpayer_Welfare (19641 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 104 | AR | - | N | - | front matter |
| rev | Revision History | 130 | AR | - | N | - | front matter |
| abs | Abstract | 337 | AR | - | N | - | front matter |
| gloss | Glossary | 319 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. Introduction | 781 | M | WELF | N | - | introduction and method of the welfare comparison [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 2 | 2. Methodology | 0 | M | WELF | N | - | introduction and method of the welfare comparison [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 2.1 | 2.1 The Comparison Design | 388 | K | WELF | N | - | six tax systems at revenue equivalence [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 2.2 | 2.2 What the Baseline Suppresses — and Why | 246 | M | WELF | N | - | introduction and method of the welfare comparison [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 2.3 | 2.3 The Three-Category Epistemic Framework | 224 | M | UNCER | N | - | three-category epistemic framework; what is not known; open questions [025w: was S12; what is not yet known empirically (unknowns, gaps, open questions)] |
| 2.4 | 2.4 Comparable-Treatment Exposures | 326 | M | WELF | N | - | introduction and method of the welfare comparison [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 3 | 3. Part I: The Controlled Baseline | 0 | K | WELF | Y | NEW:cew | controlled baseline and the Domar-Musgrave risk-sharing property [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 3.1 | 3.1 Revenue Equivalence and the Single-Agent Baseline | 854 | K | WELF | Y | NEW:cew | controlled baseline and the Domar-Musgrave risk-sharing property [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 3.2 | 3.2 The D-M Risk-Sharing Property: Mechanism Established, Ve | 641 | K | WELF | Y | NEW:cew | controlled baseline and the Domar-Musgrave risk-sharing property [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 4 | 4. Part II: The Mechanisms | 0 | M | WELF | Y | NEW:cew | progressive rates: three complications, all second order [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 4.1 | 4.1 Progressive Rates: Three Complications, All Second-Order | 1650 | M | WELF | Y | NEW:cew | progressive rates: three complications, all second order [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 4.2 | 4.2 CGT Lock-In: The Dominant Welfare Result | 0 | K | WELF | Y | NEW:lockin | CGT lock-in, the dominant welfare result (141 to 143 basis points) [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 4.2.1 | 4.2.1 The Endogenous Realisation Decision | 407 | K | WELF | Y | NEW:lockin | CGT lock-in, the dominant welfare result (141 to 143 basis points) [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 4.2.2 | 4.2.2 The Welfare Cost of Lock-In | 1415 | K | WELF | Y | NEW:lockin | CGT lock-in, the dominant welfare result (141 to 143 basis points) [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 4.2.3 | 4.2.3 The Arachi Pivot | 498 | K | WELF | Y | NEW:lockin | CGT lock-in, the dominant welfare result (141 to 143 basis points) [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 4.2.4 | 4.2.4 Category Classification | 247 | K | WELF | Y | NEW:lockin | CGT lock-in, the dominant welfare result (141 to 143 basis points) [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 4.3 | 4.3 Heterogeneous Returns: Concentration Under the Fagereng | 0 | K | WELF | Y | NEW:concentration,NEW:envelope | heterogeneous returns, concentration, incidence, lifetime contribution envelope [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 4.3.1 | 4.3.1 The Fagereng Premise and the Four-Tier Calibration | 224 | K | WELF | Y | NEW:concentration,NEW:envelope | heterogeneous returns, concentration, incidence, lifetime contribution envelope [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 4.3.2 | 4.3.2 The Concentration Result | 587 | K | WELF | Y | NEW:concentration,NEW:envelope | heterogeneous returns, concentration, incidence, lifetime contribution envelope [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 4.3.3 | 4.3.3 Within-Tier Welfare | 452 | K | WELF | Y | NEW:concentration,NEW:envelope | heterogeneous returns, concentration, incidence, lifetime contribution envelope [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 4.3.4 | 4.3.4 Distributional Incidence | 650 | K | WELF | Y | NEW:concentration,NEW:envelope | heterogeneous returns, concentration, incidence, lifetime contribution envelope [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 4.3.5 | 4.3.5 The Lifetime Contribution Envelope — Binding Result | 537 | K | WELF | Y | NEW:concentration,NEW:envelope | heterogeneous returns, concentration, incidence, lifetime contribution envelope [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 4.3.6 | 4.3.6 The Off-Diagonal Cell | 247 | K | WELF | Y | NEW:concentration,NEW:envelope | heterogeneous returns, concentration, incidence, lifetime contribution envelope [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 4.4 | 4.4 Stock Wealth and Consumption Taxes: Equivalence and Conc | 380 | M | LIT | Y | NEW:cew | stock wealth and consumption tax equivalence |
| 4.5 | 4.5 Robustness: Revenue Target, Historical Windows, and Rate | 150 | AR | - | Y | NEW:cew | v1 robustness checks (revenue target, 73 windows, rate parameters) |
| 4.5.1 | 4.5.1 Revenue Target Sensitivity | 513 | AR | - | Y | NEW:cew | v1 robustness checks (revenue target, 73 windows, rate parameters) |
| 4.5.2 | 4.5.2 Historical Window Robustness | 634 | AR | - | Y | NEW:cew | v1 robustness checks (revenue target, 73 windows, rate parameters) |
| 4.5.3 | 4.5.3 Progressive Rate Parameter Sensitivity | 897 | AR | - | Y | NEW:cew | v1 robustness checks (revenue target, 73 windows, rate parameters) |
| 5 | 5. Part III: Literature Positioning | 0 | M | LIT | N | - | literature positioning |
| 5.1 | 5.1 Domar-Musgrave and Risk-Sharing | 236 | M | LIT | N | - | literature positioning |
| 5.2 | 5.2 Progressive Taxation and Risk Asymmetry | 143 | M | LIT | N | - | literature positioning |
| 5.3 | 5.3 CGT Lock-In: Literature and Model Contribution | 427 | M | LIT | N | - | literature positioning |
| 5.4 | 5.4 Heterogeneous Returns and Concentration | 191 | M | LIT | N | - | literature positioning |
| 5.5 | 5.5 The Active Dispute WFR Enters — and Does Not Adjudicate | 506 | M | LIT | N | - | literature positioning |
| 5.6 | 5.6 Stock Wealth and Consumption Tax Equivalence | 217 | M | LIT | N | - | literature positioning |
| 5.7 | 5.7 Literature Summary | 433 | M | LIT | N | - | literature positioning |
| 6 | 6. Part IV: Synthesis and Conclusion | 0 | K | WELF | P | - | synthesis: what the model establishes about incumbent systems and about the WDT [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 6.1 | 6.1 What the Model Establishes and What It Does Not | 132 | M | UNCER | N | - | three-category epistemic framework; what is not known; open questions [025w: was S12; what is not yet known empirically (unknowns, gaps, open questions)] |
| 6.1.1 | 6.1.1 Category 1: Modelled Properties of Incumbent Systems | 390 | K | WELF | P | - | synthesis: what the model establishes about incumbent systems and about the WDT [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 6.1.2 | 6.1.2 Category 2: Structural Properties of the WDT Independe | 340 | K | WELF | P | - | synthesis: what the model establishes about incumbent systems and about the WDT [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 6.1.3 | 6.1.3 Category 3: What We Do Not Know | 360 | M | UNCER | N | - | three-category epistemic framework; what is not known; open questions [025w: was S12; what is not yet known empirically (unknowns, gaps, open questions)] |
| 6.2 | 6.2 The Comparative Question | 241 | K | WELF | P | - | synthesis: what the model establishes about incumbent systems and about the WDT [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 6.3 | 6.3 The Burden-of-Consideration Conclusion | 611 | K | WELF | P | - | synthesis: what the model establishes about incumbent systems and about the WDT [025w: S6 split: welfare comparison (WFR; map section 7)] |
| 7 | 7. Open Questions | 0 | M | UNCER | N | - | three-category epistemic framework; what is not known; open questions [025w: was S12; what is not yet known empirically (unknowns, gaps, open questions)] |
| 7.1 | 7.1 Behavioural Calibration | 189 | M | UNCER | N | - | three-category epistemic framework; what is not known; open questions [025w: was S12; what is not yet known empirically (unknowns, gaps, open questions)] |
| 7.2 | 7.2 General Equilibrium | 218 | M | UNCER | N | - | three-category epistemic framework; what is not known; open questions [025w: was S12; what is not yet known empirically (unknowns, gaps, open questions)] |
| 7.3 | 7.3 Implementation Cost Quantification | 227 | M | UNCER | N | - | three-category epistemic framework; what is not known; open questions [025w: was S12; what is not yet known empirically (unknowns, gaps, open questions)] |
| 7.4 | 7.4 Progressive WDT Advantage at Longer Horizons | 942 | K | WELF | P | - | synthesis: what the model establishes about incumbent systems and about the WDT [025w: S6 split: welfare comparison (WFR; map section 7)] |

## 19a_Taxpayer_Welfare_Appendix (5551 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 100 | AR | - | N | - | front matter |
| rev | Revision History | 54 | AR | - | N | - | front matter |
| ~A. | A. Baseline Single-Agent Comparison | 41 | AR | - | Y | NEW:cew,NEW:lockin,NEW:concentration,NEW:envelope | v1 appendix tables for the welfare comparison; v3 regenerates any that survive |
| A | A.1 Consumption-Equivalent Welfare (CEW) by System, γ, and D | 592 | AR | - | Y | NEW:cew,NEW:lockin,NEW:concentration,NEW:envelope | v1 appendix tables for the welfare comparison; v3 regenerates any that survive |
| ~B. | B. Progressive Rates and the Three D-M Complications | 53 | AR | - | Y | NEW:cew,NEW:lockin,NEW:concentration,NEW:envelope | v1 appendix tables for the welfare comparison; v3 regenerates any that survive |
| B | B.1 Flat WDT vs Progressive WDT CEW (+2) | 839 | AR | - | Y | NEW:cew,NEW:lockin,NEW:concentration,NEW:envelope | v1 appendix tables for the welfare comparison; v3 regenerates any that survive |
| ~C. | C. CGT Lock-In Distortion | 32 | AR | - | Y | NEW:cew,NEW:lockin,NEW:concentration,NEW:envelope | v1 appendix tables for the welfare comparison; v3 regenerates any that survive |
| C | C.1 Lock-In Welfare Cost by Embedded Gain Ratio (+2) | 1055 | AR | - | Y | NEW:cew,NEW:lockin,NEW:concentration,NEW:envelope | v1 appendix tables for the welfare comparison; v3 regenerates any that survive |
| ~D. | D. Heterogeneous Agents — Incidence and Concentration | 87 | AR | - | Y | NEW:cew,NEW:lockin,NEW:concentration,NEW:envelope | v1 appendix tables for the welfare comparison; v3 regenerates any that survive |
| D | D.1 CEW by Tier and Tax System (+4) | 1077 | AR | - | Y | NEW:cew,NEW:lockin,NEW:concentration,NEW:envelope | v1 appendix tables for the welfare comparison; v3 regenerates any that survive |
| ~E. | E. Welfare Sweep Analysis | 68 | AR | - | Y | NEW:cew,NEW:lockin,NEW:concentration,NEW:envelope | v1 appendix tables for the welfare comparison; v3 regenerates any that survive |
| E | E.1 Sweep A: CEW by System and Revenue Target (γ=2) (+9) | 986 | AR | - | Y | NEW:cew,NEW:lockin,NEW:concentration,NEW:envelope | v1 appendix tables for the welfare comparison; v3 regenerates any that survive |
| ~F. | F. Extended Concentration Horizon (N=73) | 0 | AR | - | Y | NEW:cew,NEW:lockin,NEW:concentration,NEW:envelope | v1 appendix tables for the welfare comparison; v3 regenerates any that survive |
| F | F.1 — Setup and Scope (+3) | 462 | AR | - | Y | NEW:cew,NEW:lockin,NEW:concentration,NEW:envelope | v1 appendix tables for the welfare comparison; v3 regenerates any that survive |
| ~G. | G. Parameter Reference | 105 | DL | input register | N | - | parameter reference |

## 20_Institutional_Selection (16215 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 117 | AR | - | N | - | front matter |
| rev | Revision History | 558 | AR | - | N | - | front matter |
| abs | Abstract | 398 | AR | - | N | - | front matter |
| gloss | Glossary | 878 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. Introduction | 664 | SA | INST | N | - | fiscal architecture and institutional selection; standalone (author, 2026-11-16) |
| 2 | 2. The Persistent Dominance of Authoritarian Governance (+3) | 1178 | SA | INST | N | - | fiscal architecture and institutional selection; standalone (author, 2026-11-16) |
| 3 | 3. The Untaxed Pool (+2) | 889 | SA | INST | N | - | fiscal architecture and institutional selection; standalone (author, 2026-11-16) |
| 4 | 4. Why Prior Mechanisms Failed (+1) | 1033 | SA | INST | N | - | fiscal architecture and institutional selection; standalone (author, 2026-11-16) |
| 5 | 5. Four Conditions for a Stable Large-Scale Wealth Tax (+4) | 2299 | SA | INST | N | - | fiscal architecture and institutional selection; standalone (author, 2026-11-16) |
| 6 | 6. The Authoritarian Exclusion: Structural, Dynamic, and Emp | 3393 | SA | INST | N | - | fiscal architecture and institutional selection; standalone (author, 2026-11-16) |
| 7 | 7. Three Competitive Advantages for Democratic WDT Adopters | 1441 | SA | INST | Y | O1,O4a,OP1 | three competitive advantages for democratic adopters; each is conditional on a model number |
| 8 | 8. Memetic Diffusion and the Race Condition | 773 | SA | INST | N | - | fiscal architecture and institutional selection; standalone (author, 2026-11-16) |
| 9 | 9. Failure Conditions (+3) | 1282 | SA | INST | N | - | fiscal architecture and institutional selection; standalone (author, 2026-11-16) |
| 10 | 10. The Research Programme (+5) | 750 | SA | INST | N | - | fiscal architecture and institutional selection; standalone (author, 2026-11-16) |
| 11 | 11. Conclusion | 562 | SA | INST | N | - | fiscal architecture and institutional selection; standalone (author, 2026-11-16) |

## 21_Labour_Dividend_Welfare (9068 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 117 | AR | - | N | - | front matter |
| rev | Revision History | 202 | AR | - | N | - | front matter |
| abs | Abstract | 255 | AR | - | N | - | front matter |
| 1 | 1. The Paper's Place in the Series and Its Character | 94 | D | - | N | - | place in the series, conclusion |
| 1.1 | 1.1 The Mature WDT as Analytical Baseline | 117 | M | UNCER | N | - | analytical baseline, speculative character, what the paper can and cannot show, conservative core [025w: was S12; what is not yet known empirically (unknowns, gaps, open questions)] |
| 1.2 | 1.2 Speculative Character and What That Means Here | 187 | M | UNCER | N | - | analytical baseline, speculative character, what the paper can and cannot show, conservative core [025w: was S12; what is not yet known empirically (unknowns, gaps, open questions)] |
| 2 | 2. What Appears on the Payslip | 101 | K | PAY | Y | O4a,O4b,NEW:labour-dividend | what appears on the payslip [025w: S6 split: who pays (RATES 2, WP 8.2, payslip; map section 7)] |
| 2.1 | 2.1 The Bilateral NICs Case | 488 | K | PAY | Y | O4a,O4b,O1,NEW:labour-dividend | NICs and income tax displacement; a care worker on 25,000 gains 3,480 pounds a year [025w: S6 split: who pays (RATES 2, WP 8.2, payslip; map section 7)] |
| 2.2 | 2.2 Income Tax Displacement | 463 | K | PAY | Y | O4a,O4b,O1,NEW:labour-dividend | NICs and income tax displacement; a care worker on 25,000 gains 3,480 pounds a year [025w: S6 split: who pays (RATES 2, WP 8.2, payslip; map section 7)] |
| 3 | 3. Employment Structure and the Occupational Constraint | 0 | K | FIRST | P | - | employment structure, household capacity, welfare demand and its upstream conditions [025w: was S11; direct effect, short causal chain] |
| 3.1 | 3.1 What NICs Removal Does to the Employment Relationship | 271 | K | FIRST | P | - | employment structure, household capacity, welfare demand and its upstream conditions [025w: was S11; direct effect, short causal chain] |
| 3.2 | 3.2 The Occupational Constraint and What Relaxes It | 287 | K | FIRST | P | - | employment structure, household capacity, welfare demand and its upstream conditions [025w: was S11; direct effect, short causal chain] |
| 4 | 4. The Cost of Living Under a Mature WDT | 43 | K | PAY | Y | NEW:labour-dividend | cost of living under a mature WDT; the full purchasing power calculation [025w: S6 split: who pays (RATES 2, WP 8.2, payslip; map section 7)] |
| 4.1 | 4.1 VAT and Consumption Taxes | 182 | K | PAY | Y | NEW:labour-dividend | cost of living under a mature WDT; the full purchasing power calculation [025w: S6 split: who pays (RATES 2, WP 8.2, payslip; map section 7)] |
| 4.2 | 4.2 Housing: Renters and Owners | 495 | M | WIDER | P | OS1 | housing; demand expansion and reallocation (second-order effects) [025w: was S11; longer causal chain, institutional or second-order effect] |
| 4.3 | 4.3 Public Infrastructure and the SWF as Patient Investor | 765 | K | FUND | N | - | SWF as patient investor; the author's normative case |
| 4.4 | 4.4 The Full Purchasing Power Calculation | 341 | K | PAY | Y | NEW:labour-dividend | cost of living under a mature WDT; the full purchasing power calculation [025w: S6 split: who pays (RATES 2, WP 8.2, payslip; map section 7)] |
| 4.5 | 4.5 Demand Expansion and Economic Reallocation | 165 | M | WIDER | P | OS1 | housing; demand expansion and reallocation (second-order effects) [025w: was S11; longer causal chain, institutional or second-order effect] |
| 4.5.1 | 4.5.1 Increased Household Consumption | 244 | M | WIDER | P | OS1 | housing; demand expansion and reallocation (second-order effects) [025w: was S11; longer causal chain, institutional or second-order effect] |
| 4.5.2 | 4.5.2 Labour Reallocation and Occupational Choice | 340 | M | WIDER | P | OS1 | housing; demand expansion and reallocation (second-order effects) [025w: was S11; longer causal chain, institutional or second-order effect] |
| 4.5.3 | 4.5.3 Entry into Marginal and Previously Unprofitable Sector | 243 | M | WIDER | P | OS1 | housing; demand expansion and reallocation (second-order effects) [025w: was S11; longer causal chain, institutional or second-order effect] |
| 4.5.4 | 4.5.4 Returns to Private Capital | 229 | M | WIDER | P | OS1 | housing; demand expansion and reallocation (second-order effects) [025w: was S11; longer causal chain, institutional or second-order effect] |
| 4.5.5 | 4.5.5 Distributional Ambiguity | 216 | M | WIDER | P | OS1 | housing; demand expansion and reallocation (second-order effects) [025w: was S11; longer causal chain, institutional or second-order effect] |
| 5 | 5. Household Capacity | 452 | K | FIRST | P | - | employment structure, household capacity, welfare demand and its upstream conditions [025w: was S11; direct effect, short causal chain] |
| 6 | 6. Welfare Demand and Its Upstream Conditions | 75 | K | WIDER | P | - | employment structure, household capacity, welfare demand and its upstream conditions [025w: was S11; longer causal chain, institutional or second-order effect] |
| 6.1 | 6.1 The Cascade Threshold | 285 | K | WIDER | P | - | employment structure, household capacity, welfare demand and its upstream conditions [025w: was S11; longer causal chain, institutional or second-order effect] |
| 6.2 | 6.2 Healthcare Demand | 246 | K | WIDER | P | - | employment structure, household capacity, welfare demand and its upstream conditions [025w: was S11; longer causal chain, institutional or second-order effect] |
| 6.3 | 6.3 Pensions and Long-Run Security | 184 | K | WIDER | P | - | employment structure, household capacity, welfare demand and its upstream conditions [025w: was S11; longer causal chain, institutional or second-order effect] |
| 6.4 | 6.4 A Different Relationship Between State and Citizen | 182 | K | WIDER | P | - | employment structure, household capacity, welfare demand and its upstream conditions [025w: was S11; longer causal chain, institutional or second-order effect] |
| 7.1 | 7.1 What This Paper Can and Cannot Establish | 373 | M | UNCER | N | - | analytical baseline, speculative character, what the paper can and cannot show, conservative core [025w: was S12; epistemic status of the paper; UNCER] |
| 7.2 | 7.2 The Infrastructure Mandate | 156 | M | FUND | N | - | infrastructure mandate |
| 7.3 | 7.3 Phase One Measurement Agenda | 266 | M | POL | N | - | Phase One measurement agenda |
| 7.4 | 7.4 The Conservative Core | 149 | M | UNCER | N | - | analytical baseline, speculative character, what the paper can and cannot show, conservative core [025w: was S12; claims that survive the speculative assumptions; UNCER] |
| 8 | 8. Conclusion | 855 | D | - | N | - | place in the series, conclusion |

## 22_Falsification_Hypotheses (12025 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 92 | AR | - | N | - | front matter |
| rev | Revision History | 70 | AR | - | N | - | front matter |
| abs | Abstract | 315 | AR | - | N | - | front matter |
| gloss | Glossary | 188 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. Purpose and Methodological Commitment | 0 | K | FALS | N | - | purpose, research question, what counts as a serious result, research challenge [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 1.1 | 1.1 What This Paper Is | 173 | K | FALS | N | - | purpose, research question, what counts as a serious result, research challenge [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 1.2 | 1.2 What This Paper Does Not Claim | 77 | K | FALS | N | - | purpose, research question, what counts as a serious result, research challenge [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 1.3 | 1.3 Relation to the Existing Project | 175 | K | FALS | N | - | purpose, research question, what counts as a serious result, research challenge [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 2 | 2. The Research Question | 333 | K | FALS | N | - | purpose, research question, what counts as a serious result, research challenge [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 3 | 3. H1: Wealthy Taxpayer Preference | 0 | K | FALS | P | O2,O5,O6 | H1 wealthy taxpayer preference [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 3.1 | 3.1 Statement | 28 | K | FALS | P | O2,O5,O6 | H1 wealthy taxpayer preference [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 3.2 | 3.2 The Comparison That Matters | 338 | K | FALS | P | O2,O5,O6 | H1 wealthy taxpayer preference [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 3.3 | 3.3 The Break-Even Burden | 243 | K | FALS | Y | O2,O6 | break-even burden; derived by comparing the burden with today's taxes [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 3.4 | 3.4 The Institutional Participation Component | 249 | K | FALS | P | O2,O5,O6 | H1 wealthy taxpayer preference [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 3.5 | 3.5 The Migration Evidence | 283 | K | FALS | P | O2,O5,O6 | H1 wealthy taxpayer preference [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 3.6 | 3.6 Falsification Conditions | 161 | K | FALS | P | O2,O5,O6 | H1 wealthy taxpayer preference [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 4 | 4. H2: Macroeconomic Effects | 0 | K | FALS | P | O4a | H2a capital allocation efficiency and H2b labour tax displacement [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 4.1 | 4.1 Structure of the Decomposition | 143 | K | FALS | P | O4a | H2a capital allocation efficiency and H2b labour tax displacement [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 4.2 | 4.2 H2a: Capital Allocation Efficiency | 544 | K | FALS | P | O4a | H2a capital allocation efficiency and H2b labour tax displacement [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 4.3 | 4.3 H2b: Labour Tax Displacement Welfare Effect | 508 | K | FALS | P | O4a | H2a capital allocation efficiency and H2b labour tax displacement [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 4.4 | 4.4 H2c: Automatic Stabilisation | 541 | K | FALS | P | OP6,O1 | H2c automatic stabilisation; counter-cyclical position by return state [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 4.5 | 4.5 H2d: Positive Feedback Loop Integrity | 743 | K | FALS | N | - | H2d positive feedback loop integrity; not modelled in v3 (partial equilibrium) [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 5 | 5. H3: Cooperative Institutional Equilibrium | 0 | K | FALS | N | - | H3 cooperative institutional equilibrium; needs a repeated-game model, not part of v3 [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 5.1 | 5.1 Statement | 39 | K | FALS | N | - | H3 cooperative institutional equilibrium; needs a repeated-game model, not part of v3 [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 5.2 | 5.2 What the Hypothesis Is Not | 203 | K | FALS | N | - | H3 cooperative institutional equilibrium; needs a repeated-game model, not part of v3 [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 5.3 | 5.3 The Repeated-Game Structure | 403 | K | FALS | N | - | H3 cooperative institutional equilibrium; needs a repeated-game model, not part of v3 [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 5.4 | 5.4 The Governance Architecture as Anti-Capture Design | 319 | K | FALS | N | - | H3 cooperative institutional equilibrium; needs a repeated-game model, not part of v3 [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 5.5 | 5.5 The Bootstrapping Phase | 413 | K | FALS | N | - | H3 cooperative institutional equilibrium; needs a repeated-game model, not part of v3 [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 5.6 | 5.6 Required Model | 277 | K | FALS | N | - | H3 cooperative institutional equilibrium; needs a repeated-game model, not part of v3 [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 5.7 | 5.7 Falsification Conditions | 195 | K | FALS | N | - | H3 cooperative institutional equilibrium; needs a repeated-game model, not part of v3 [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 6 | 6. H4: Accumulation-Point Efficiency | 0 | K | FALS | P | NEW:cew | H4 accumulation-point efficiency; needs a welfare comparison [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 6.1 | 6.1 Statement | 38 | K | FALS | P | NEW:cew | H4 accumulation-point efficiency; needs a welfare comparison [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 6.2 | 6.2 The Mechanism | 427 | K | FALS | P | NEW:cew | H4 accumulation-point efficiency; needs a welfare comparison [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 6.3 | 6.3 The Costs WDT Introduces | 274 | K | FALS | P | NEW:cew | H4 accumulation-point efficiency; needs a welfare comparison [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 6.4 | 6.4 What a Hostile Model Should Measure | 124 | K | FALS | P | NEW:cew | H4 accumulation-point efficiency; needs a welfare comparison [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 6.5 | 6.5 Falsification Conditions | 131 | K | FALS | P | NEW:cew | H4 accumulation-point efficiency; needs a welfare comparison [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 7 | 7. H5: Automation Base Robustness | 0 | K | FALS | N | NEW:automation | H5 automation base robustness; not modelled in v3 [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 7.1 | 7.1 Statement | 44 | K | FALS | N | NEW:automation | H5 automation base robustness; not modelled in v3 [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 7.2 | 7.2 The Mechanism | 261 | K | FALS | N | NEW:automation | H5 automation base robustness; not modelled in v3 [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 7.3 | 7.3 The Dependency on H2d | 173 | K | FALS | N | NEW:automation | H5 automation base robustness; not modelled in v3 [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 7.4 | 7.4 Required Model | 146 | K | FALS | N | NEW:automation | H5 automation base robustness; not modelled in v3 [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 7.5 | 7.5 Falsification Conditions | 150 | K | FALS | N | NEW:automation | H5 automation base robustness; not modelled in v3 [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 8 | 8. Interactions Between the Five Hypotheses | 534 | K | FALS | N | - | interactions among the hypotheses; minimum requirements for hostile modelling; what would count against the WDT [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 9 | 9. What Counts as a Serious Result | 77 | K | FALS | N | - | purpose, research question, what counts as a serious result, research challenge [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 9.1 | 9.1 Support | 52 | K | FALS | N | - | purpose, research question, what counts as a serious result, research challenge [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 9.2 | 9.2 Conditional Support | 151 | K | FALS | N | - | purpose, research question, what counts as a serious result, research challenge [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 9.3 | 9.3 Falsification | 93 | K | FALS | N | - | purpose, research question, what counts as a serious result, research challenge [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 10 | 10. Minimum Requirements for Hostile Modelling | 442 | K | FALS | N | - | interactions among the hypotheses; minimum requirements for hostile modelling; what would count against the WDT [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 11 | 11. What Would Constitute Evidence Against WDT | 344 | K | FALS | N | - | interactions among the hypotheses; minimum requirements for hostile modelling; what would count against the WDT [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 12 | 12. Research Challenge | 306 | K | FALS | N | - | purpose, research question, what counts as a serious result, research challenge [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| 13 | 13. Conclusion | 712 | K | FALS | N | - | purpose, research question, what counts as a serious result, research challenge [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |
| ~A. | A. Hypothesis Summary Table | 493 | K | FALS | N | - | hypothesis summary table [025w: was S12; a test of a central claim (FAL hypothesis, condition or evidence rule)] |

## Site pages: four reader-facing pages (brief 025w; not in the 980 rows above)

These four pages (`site/pages/`, named in `site/ids.md` Q7) restate material of the papers for readers. They are source material for the new pages, like an old paper, and are counted apart from the 980 rows and 342,495 words. **Words** are body words without the heading line. None is K: each section either repeats a kept or merged section of the papers (M, folded into the page named) or has no content to keep (D) or is a v1 figure set or an embed (AR). The reader-facing form (the FAQ question wording, the second-person guide voice) is a style input to the writing lane, not content.

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| faq-0 | (opening) | 74 | D | - | N | - | page introduction; the hub (H5) frames the objections, and the three-way distinction becomes the Status label of each objection block |
| faq-1 | "If gains and losses are symmetrical, won't it raise no money?" | 115 | M | FISC | P | - | revenue under symmetry; restates the revenue claim and the long-run drift argument |
| faq-2 | "How can the government afford refunds in a crash?" | 136 | M | FISC | Y | OP1,OR1 | refund funding in a crash; the figure for fill years is v1 and is not carried (OP1, OR1) |
| faq-3 | "Annual valuation is impossible." | 135 | M | VAL | N | - | annual valuation objection; restates VAL 1 and the declaration logic |
| faq-4 | "Won't people just hide or move their wealth?" | 213 | M | BEHAV | P | - | concealment, restructuring and migration; also touches CORP and ATTR |
| faq-5 | "Isn't this just another wealth tax?" | 169 | M | MECH | N | - | definition: charge on the increase, refund on a fall |
| faq-6 | "Will people have to sell assets just to pay the tax?" | 161 | M | PAY | N | - | forced sale objection; listed assets settle through the corporate levy, others by deferred settlement |
| faq-7 | "Why tax unrealised gains?" | 179 | M | FAIR | N | - | why tax unrealised gains; the normative case |
| faq-8 | "Why should government invest alongside private wealth?" | 202 | M | FUND | N | - | public investment alongside private wealth; reciprocity argument |
| faq-9 | "What if the economy stops growing?" | 166 | M | FISC | P | - | economy stops growing; tested against UK return sequences (v1 figure not carried) |
| faq-10 | "Why have a Sovereign Wealth Fund instead of spending the money?" | 162 | M | FUND | N | - | why a fund and not spending; the refund obligation is contractual |
| faq-11 | "Why use the money to cut labour taxes?" | 188 | M | FUND | N | - | why the money cuts labour taxes; the objective of the design |
| faq-12 | "Does everyone have to pay this?" | 188 | M | FISC | N | - | threshold: administrative and political arguments |
| comp-0 | (opening) | 91 | D | - | N | - | page introduction; replaced by the comparison page |
| comp-1 | Tax base | 67 | M | MECH | N | - | tax base |
| comp-2 | Lock-in and neutrality | 115 | M | WELF | Y | OW2 | lock-in and neutrality; the 141 bp figure is v1 (OW2 replaces it) |
| comp-3 | Treatment of losses | 112 | M | MECH | N | - | treatment of losses; symmetric refund |
| comp-4 | Wealth concentration over time | 118 | M | WELF | Y | - | wealth concentration over time; the 320x figure is v1 and has no v3 output (OH1a was dropped 2026-11-17, see `outputs.yml`) |
| comp-5 | Valuation and administration | 76 | M | VAL | N | - | valuation and administration |
| comp-6 | Avoidance and concealment | 81 | M | BEHAV | N | - | avoidance and concealment |
| comp-7 | Migration incentive | 75 | M | BEHAV | N | - | migration incentive |
| comp-8 | Political durability | 91 | M | POL | N | - | political durability |
| comp-9 | Countercyclical behaviour | 89 | M | FUND | N | - | countercyclical behaviour; the SWF buffer |
| comp-10 | Revenue use and distributional objective | 104 | M | FUND | N | - | revenue use and distributional objective |
| comp-11 | Empirical standing | 223 | M | WELF | Y | OW1,OW2 | empirical standing; v1 results throughout, restated from OW1 to OW3 when they exist |
| avoi-1 | This is the cheat sheet. | 197 | D | - | N | - | "This is the cheat sheet": a summary of the six decisions, restated by the sections below |
| avoi-2 | How your liability is calculated | 251 | M | MECH | P | - | how liability is calculated; restates the delta, the rate schedule and the window |
| avoi-4 | Decision 1 — Choose Route D if your assets permit it | 239 | M | VAL | N | - | decision 1, choose Route D if the assets permit |
| avoi-5 | Decision 2 — Declare at or slightly above your genuine central estimat | 447 | M | DECL | P | - | decision 2, declare near the central estimate; restates VAL 7 |
| avoi-6 | Decision 3 — Elect the longest assessment window if you hold volatile  | 272 | M | MECH | N | - | decision 3, elect the longest window |
| avoi-7 | Decision 4 — Understand what your Route C declaration commits you to | 394 | M | DECL | P | - | decision 4, what a Route C declaration commits to |
| avoi-8 | Decision 5 — Emigration, divestment, and the corporate levy | 560 | M | BEHAV | N | - | decision 5, emigration, divestment and the corporate levy; the levy part also overlaps CORP |
| avoi-9 | Decision 6 — Trigger a voluntary hard-reset auction before death on Ro | 280 | M | VAL | N | - | decision 6, a voluntary hard-reset auction on Route D assets |
| avoi-10 | What you cannot change | 171 | M | MECH | N | - | what you cannot change: the rate schedule, the threshold, the refund cap |
| avoi-11 | What this tells you | 119 | D | - | N | - | "what this tells you": a closing restatement |
| avoi-12 | The calculator | 110 | AR | - | N | - | calculator embed; stays until a v3 calculator replaces it (ids.md Q8) |
| corp-1 | The levy does the work. Your job is to claim it. | 180 | M | CORP | N | - | the levy collects before you file |
| corp-2 | How the corporate delta levy is calculated | 151 | M | CORP | N | - | how the corporate delta levy is calculated |
| corp-3 | Who gets the credit and who doesn't | 316 | M | CORP | N | - | the three tranches of shareholders; the attribution test overlaps ATTR |
| corp-4 | What your broker does on your behalf | 194 | M | CORP | N | - | the broker statement and reconciliation |
| corp-5 | The credit timeline: one deadline the rolling window doesn't move | 206 | M | CORP | N | - | the credit deadline the rolling window does not move |
| corp-6 | A worked example: equity portfolio at the 95th percentile | 269 | AR | - | Y | - | worked example at the 95th wealth percentile; v1 figures (38), not carried; a fixture of the VAL.B kind can replace it |
| corp-7 | What happens to corporate credits in a loss year | 181 | M | CORP | N | - | corporate credits in a loss year |
| corp-8 | Derivatives and synthetic exposure: what the levy doesn't reach | 130 | M | CORP | N | - | derivatives and synthetic exposure; overlaps CORP 8 |
| corp-9 | The case for full attribution | 220 | M | ATTR | N | - | the case for full attribution; overlaps the attribution test in ATTR |
| corp-10 | Summary: what you need to do | 184 | D | - | N | - | summary of what to do; restates the sections above |
