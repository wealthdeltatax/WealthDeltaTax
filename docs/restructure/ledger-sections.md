# Content ledger: section dispositions (brief 013g, stage B)

One row per section (or run of sections with one disposition) of the old papers. Generated from the dispositions the guru recorded; edit this file by hand from now on. Summary, totals and coverage: `ledger.md`.

Columns: **Sec** old section number; **Words** old words in the row; **Disp**: K keep to the target, M merge into the target (overlaps another kept section), D drop as redundant, SA standalone paper, AR archive, DL move to the data layer; **Target**: hub section H0 to H7, spoke S1 to S12, standalone paper, or data layer; **Model**: Y the claims need model numbers, P partly, N no; **Demands**: output IDs from `outputs.yml` the claims need, or `NEW:` tags for outputs it lacks (defined in `ledger.md`).


## 1_Wealth_Delta_Tax_Whitepaper (15078 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 119 | AR | - | N | - | front matter; the hub writes its own summary (H0) |
| rev | Revision History | 477 | AR | - | N | - | front matter; the hub writes its own summary (H0) |
| abs | Abstract | 221 | AR | - | N | - | front matter; the hub writes its own summary (H0) |
| gloss | Glossary | 276 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. Introduction | 300 | M | H1 | N | NEW:H1 | opening statement of the problem (unrealised gains treated as a non-event); H1 needs data hooks |
| 1.1 | 1.1 The Cooperative Basis of the Design | 363 | M | S1 | N | - | cooperative basis; duplicates MF 7 |
| 2.1 | 2.1 The Haig-Simons Definition and the Comprehensive Income  | 279 | K | S2 | N | - | literature context; overlaps 3a and 3b, ledger keeps one copy per idea |
| 2.2 | 2.2 The Empirical Literature on Wealth Taxation | 228 | K | S2 | N | - | literature context; overlaps 3a and 3b, ledger keeps one copy per idea |
| 2.3 | 2.3 The Income versus Consumption Debate | 385 | K | S2 | N | - | literature context; overlaps 3a and 3b, ledger keeps one copy per idea |
| 2.4 | 2.4 The Wealth Concentration Literature | 141 | K | H1 | P | NEW:H1-wealth | wealth concentration (top 1% share about 38%, US); needs UK concentration facts for H1 |
| 2.5 | 2.5 The Domar-Musgrave Principle | 238 | K | S2 | N | - | literature context; overlaps 3a and 3b, ledger keeps one copy per idea |
| 2.6 | 2.6 Harberger Self-Assessment and the Purchase Option Tradit | 218 | K | S2 | N | - | literature context; overlaps 3a and 3b, ledger keeps one copy per idea |
| 2.7 | 2.7 Five Design Problems Unresolved in Prior Literature | 274 | K | S2 | N | - | literature context; overlaps 3a and 3b, ledger keeps one copy per idea |
| 3 | 3. The Wealth Delta Tax: Mechanism Design | 152 | K | H2 | N | - | plain-words mechanism opener |
| 3.1 | 3.1 The Tax Base | 239 | K | S3 | N | - | tax base, unit, voluntary participation, symmetric refund, windows |
| 3.2 | 3.2 The Individual as the Unit of Taxation | 525 | K | S3 | N | - | tax base, unit, voluntary participation, symmetric refund, windows |
| 3.3 | 3.3 The Progressive Rate Structure | 129 | K | S5 | N | - | rate structure in words; numbers belong to the named schedules |
| 3.4 | 3.4 The Exemption Threshold | 86 | K | S5 | P | N-PAYERS | threshold is the political parameter; payer count by threshold is not an output yet |
| 3.4.1 | 3.4.1 Voluntary Participation Below the Threshold | 373 | K | S3 | N | - | tax base, unit, voluntary participation, symmetric refund, windows |
| 3.5 | 3.5 The Symmetric Loss-Refund Mechanism | 690 | K | S3 | N | - | tax base, unit, voluntary participation, symmetric refund, windows |
| 3.6 | 3.6 Assessment Windows | 319 | K | S3 | N | - | tax base, unit, voluntary participation, symmetric refund, windows |
| 3.7 | 3.7 Valuation Architecture | 357 | M | S4 | N | - | valuation architecture; duplicates VAL |
| 3.8 | 3.8 Valuation Incentives and the Structure of the Problem | 496 | M | S4 | Y | O7,NEW:alpha | model-implied behavioural centre alpha about 1.1; C.1 covers tolerance, not the centre |
| 4 | 4. The Sovereign Wealth Fund | 155 | K | S7 | N | - | fund purpose and why it is structurally necessary |
| 4.1 | 4.1 Why the Fund Is Structurally Necessary | 225 | K | S7 | N | - | fund purpose and why it is structurally necessary |
| 4.2 | 4.2 Governance and Shared Interests | 407 | K | S9 | N | - | three-constituency governance |
| 4.3 | 4.3 Route D Auction Mechanism | 702 | K | S4 | N | - | Route D auction (entry basis problem) |
| 5 | 5. Revenue Properties | 627 | K | S5 | Y | O1,O1a,O1b,OP1,NEW:reserve-solvency,NEW:coverage | v1 claims: 73 start years, reserve never reaches zero, fill 7 to 29 years, 125.5% coverage, 874bn and 172bn; v2 closure is 42 to 55% of windows, so these cannot be carried over |
| 5.1 | 5.1 Parameter Selection and the N = 30 Working Assumption | 732 | K | S5 | Y | O2,O3,O5,O6 | 0.35% revenue-weighted burden, 13.0% lifetime rate, against 1 to 2% stock taxes and CGT 18 to 24%; M2 formula still to be checked against 0.35% |
| 6 | 6. Replacing Existing Taxes: Scope and Sequencing | 550 | K | S7 | Y | O1d,OP5,OP3 | replacing existing taxes, scope and sequencing |
| 7 | 7. Implementation Pathway | 172 | K | S10 | P | OP1 | implementation pathway and Phase One; thresholds are council parameters |
| 7.1 | 7.1 Phase One: Infrastructure and Proof of Mechanism | 340 | K | S10 | P | OP1 | implementation pathway and Phase One; thresholds are council parameters |
| 7.2 | 7.2 Phase Two: Expansion and Labour Tax Relief | 134 | K | S10 | P | OP1 | implementation pathway and Phase One; thresholds are council parameters |
| 7.3 | 7.3 International Coordination and Capital Mobility | 173 | K | S6 | P | - | migration and capital mobility; Norway evidence, no v3 range yet (driver D5) |
| 8 | 8. Principal Objections | 0 | M | S4 | N | - | valuation objection; duplicates VAL |
| 8.1 | 8.1 The Valuation Problem | 474 | M | S4 | N | - | valuation objection; duplicates VAL |
| 8.2 | 8.2 The Liquidity Problem | 669 | K | S6 | Y | O2b,O2c | liquidity objection; cash-flow burden outputs answer it |
| 8.3 | 8.3 Behavioural Responses | 243 | K | S6 | P | - | behavioural responses and the complexity (attribution) objection |
| 8.4 | 8.4 The Consumption Tax Alternative | 52 | M | S2 | N | - | consumption tax alternative |
| 8.5 | 8.5 Constitutional Entrenchment | 250 | K | S9 | N | - | entrenchment and state-finance entanglement |
| 8.6 | 8.6 State-Finance Entanglement | 61 | K | S9 | N | - | entrenchment and state-finance entanglement |
| 8.7 | 8.7 The Complexity Objection | 541 | K | S6 | P | - | behavioural responses and the complexity (attribution) objection |
| 9 | 9. Limitations and Required Further Work | 0 | D | - | N | - | status text (gaps closed by WFR; data-access precondition covered by S9) |
| 9.1 | 9.1 Formal modelling gaps | 267 | D | - | N | - | status text (gaps closed by WFR; data-access precondition covered by S9) |
| 9.2 | 9.2 Phase One Empirical Unknowns | 221 | M | S12 | N | - | empirical unknowns and irreducible limits |
| 9.3 | 9.3 Fiscal Concentration Risk | 299 | M | S12 | Y | N-PAYERS | fiscal concentration risk, 32,000 payers at W_min 10m |
| 9.4 | 9.4 Jurisdiction-Specific Legal and Implementation Work | 99 | D | - | N | - | status text (gaps closed by WFR; data-access precondition covered by S9) |
| 9.5 | 9.5 Structural and Irreducible Limits of the Design | 284 | M | S12 | N | - | empirical unknowns and irreducible limits |
| 10 | 10. Conclusion | 516 | D | - | N | - | conclusion restates RATES; the hub writes its own |

## 2_Moral_and_Philosophical_Foundations (7642 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 102 | AR | - | N | - | front matter |
| rev | Revision History | 256 | AR | - | N | - | front matter |
| abs | Abstract | 198 | AR | - | N | - | front matter |
| gloss | Glossary | 577 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. Introduction | 546 | D | - | N | - | introduction and conclusion; S1 opens and closes itself |
| 2 | 2. The Individual as the Only Legitimate Moral Subject | 906 | K | S1 | N | - | the individual as the only legitimate moral subject |
| 3 | 3. Where Wealth Comes From | 0 | K | S1 | N | - | where wealth comes from, collective production, why the delta |
| 3.1 | 3.1 Wealth as Constituted by Collective Frameworks | 346 | K | S1 | N | - | where wealth comes from, collective production, why the delta |
| 3.2 | 3.2 Collective Inputs to Accumulation | 351 | K | S1 | N | - | where wealth comes from, collective production, why the delta |
| 3.3 | 3.3 Why the Delta | 549 | K | S1 | N | - | where wealth comes from, collective production, why the delta |
| 4 | 4. Wealth as Power, Not Deferred Consumption | 455 | K | S1 | N | - | wealth as power; fiscal opacity |
| 5 | 5. Fiscal Opacity and the Conditions for Democratic Delibera | 296 | K | S1 | N | - | wealth as power; fiscal opacity |
| 6 | 6. Democratic Flourishing as the Terminal Goal | 714 | K | S1 | P | O4a | democratic flourishing; points to LDW for payslip numbers |
| 7 | 7. The Cooperative Architecture | 637 | K | S1 | N | - | cooperative architecture; the hub H4 draws one paragraph |
| 8 | 8. Tolerance for Imperfect Compliance | 295 | M | S12 | N | - | tolerance for imperfect compliance; links to O7 |
| 9 | 9. Limitations and Required Further Work | 37 | D | - | N | - | limitations register; items are carried by S12 |
| 9.1 | 9.1 Formal modelling gaps | 100 | D | - | N | - | limitations register; items are carried by S12 |
| 9.2 | 9.2 Phase One empirical unknowns | 65 | D | - | N | - | limitations register; items are carried by S12 |
| 9.3 | 9.3 Jurisdiction-specific legal and implementation work | 42 | D | - | N | - | limitations register; items are carried by S12 |
| 9.4 | 9.4 Structural and irreducible limits of the design | 0 | M | S12 | N | - | structural limits, short items |
| 9.4.1 | 9.4.1 The corporate instrument | 46 | M | S12 | N | - | structural limits, short items |
| 9.4.2 | 9.4.2 The asymmetric treatment of corporate loss years | 40 | M | S12 | N | - | structural limits, short items |
| 9.4.3 | 9.4.3 The exemption threshold | 48 | M | S12 | N | - | structural limits, short items |
| 9.4.4 | 9.4.4 International mobility and exit | 57 | M | S12 | N | - | structural limits, short items |
| 9.4.5 | 9.4.5 The assumption of functional democratic institutions | 66 | M | S12 | N | - | structural limits, short items |
| 9.4.6 | 9.4.6 The transition period | 54 | M | S12 | N | - | structural limits, short items |
| 9.4.7 | 9.4.7 The institutional tiers the mechanism produces | 56 | M | S12 | N | - | structural limits, short items |
| 9.4.8 | 9.4.8 The Route D extreme residual | 266 | M | S4 | N | - | Route D extreme residual; duplicates WP 4.3 |
| 9.4.9 | 9.4.9 The governance compromises | 193 | M | S12 | N | - | structural limits, short items |
| 9.5 | 9.5 Governing Council calibration parameters | 6 | D | - | N | - | limitations register; items are carried by S12 |
| 10 | 10. Conclusion | 338 | D | - | N | - | introduction and conclusion; S1 opens and closes itself |

## 3a_Research_Gaps (4561 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 108 | AR | - | N | - | front matter |
| rev | Revision History | 91 | AR | - | N | - | front matter |
| abs | Abstract | 204 | AR | - | N | - | front matter |
| gloss | Glossary | 191 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. Introduction | 210 | D | - | N | - | introduction; conclusion list of nine gaps is superseded by the new set |
| 2 | 2. Formal Modelling Gaps | 0 | K | S2 | N | - | formal modelling gaps |
| 2.1 | 2.1 The Domar-Musgrave Extension | 480 | K | S2 | N | - | formal modelling gaps |
| 2.2 | 2.2 The Welfare Comparison | 345 | K | S2 | N | - | formal modelling gaps |
| 2.3 | 2.3 Heterogeneous Returns and the Delta Base | 368 | K | S2 | N | - | formal modelling gaps |
| 3 | 3. Compliance and Behavioural Gaps | 0 | K | S2 | N | - | compliance and behavioural gaps; migration externality also informs S6 |
| 3.1 | 3.1 Cooperative Compliance at the Ultra-High-Net-Worth Level | 654 | K | S2 | N | - | compliance and behavioural gaps; migration externality also informs S6 |
| 3.2 | 3.2 The Cross-Base Migration Externality | 283 | K | S2 | N | - | compliance and behavioural gaps; migration externality also informs S6 |
| 3.3 | 3.3 Administrative-Layer Intervention Effects | 324 | K | S2 | N | - | compliance and behavioural gaps; migration externality also informs S6 |
| 4 | 4. Political and International Gaps | 0 | K | S2 | N | - | political and international gaps; Zucman 2% minimum tax is a comparator (O5) |
| 4.1 | 4.1 The Political Durability Causal Framework | 261 | K | S2 | N | - | political and international gaps; Zucman 2% minimum tax is a comparator (O5) |
| 4.2 | 4.2 The International Competitive Dynamic at the Political L | 283 | K | S2 | N | - | political and international gaps; Zucman 2% minimum tax is a comparator (O5) |
| 4.3 | 4.3 The Minimum-Tax Interaction | 304 | K | S2 | N | - | political and international gaps; Zucman 2% minimum tax is a comparator (O5) |
| 5 | 5. Conclusion | 455 | D | - | N | - | introduction; conclusion list of nine gaps is superseded by the new set |

## 3b_Intellectual_Background (9707 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 111 | AR | - | N | - | front matter |
| rev | Revision History | 99 | AR | - | N | - | front matter |
| abs | Abstract | 192 | AR | - | N | - | front matter |
| gloss | Glossary | 526 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. Introduction and How to Use This Document | 405 | D | - | N | - | how to use this document |
| 2 | 2. The Tax Base Question | 431 | K | S2 | N | - | tax base, unrealised gains, loss treatment, heterogeneous returns, welfare comparison |
| 3 | 3. Unrealised Gains and Prior Accrual Proposals | 1264 | K | S2 | N | - | tax base, unrealised gains, loss treatment, heterogeneous returns, welfare comparison |
| 4 | 4. Symmetric Loss Treatment and Risk-Sharing | 448 | K | S2 | N | - | tax base, unrealised gains, loss treatment, heterogeneous returns, welfare comparison |
| 5 | 5. Heterogeneous Returns and Efficiency Under a Wealth Tax | 610 | K | S2 | N | - | tax base, unrealised gains, loss treatment, heterogeneous returns, welfare comparison |
| 6 | 6. Welfare Comparisons | 409 | K | S2 | N | - | tax base, unrealised gains, loss treatment, heterogeneous returns, welfare comparison |
| 7 | 7. The Empirical Wealth Tax Record | 494 | K | S2 | N | - | empirical wealth tax record; migration qualification also informs S6 |
| 8 | 8. The Valuation Problem | 430 | M | S4 | N | - | valuation problem and self-assessment literature |
| 9 | 9. Self-Assessment and Deterrence | 415 | M | S4 | N | - | valuation problem and self-assessment literature |
| 10 | 10. Cooperative Compliance and Procedural Justice | 391 | M | S6 | N | - | cooperative compliance and professionally mediated systems |
| 11 | 11. Compliance in Professionally Mediated Systems | 421 | M | S6 | N | - | cooperative compliance and professionally mediated systems |
| 12 | 12. Collective Action and Governance of Multi-Constituency I | 404 | M | S9 | N | - | collective action, pension governance, SWF reference cases, precommitment |
| 13 | 13. Mutual and Pension Governance | 402 | M | S9 | N | - | collective action, pension governance, SWF reference cases, precommitment |
| 14 | 14. Sovereign Wealth Fund Reference Cases | 329 | M | S9 | N | - | collective action, pension governance, SWF reference cases, precommitment |
| 15 | 15. Precommitment and Fiscal Rules | 317 | M | S9 | N | - | collective action, pension governance, SWF reference cases, precommitment |
| 16 | 16. Moral Philosophy and the Normative Case | 475 | M | S1 | N | - | moral philosophy and democratic legitimacy |
| 17 | 17. Democratic Legitimacy and Wealth Concentration | 587 | M | S1 | N | - | moral philosophy and democratic legitimacy |
| 18 | 18. Exit Taxation and International Coordination | 547 | M | S11 | N | - | exit taxation and international coordination |

## 4_UK_Jurisdiction_and_Data_Reference_Paper (6320 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 117 | AR | - | N | - | front matter |
| rev | Revision History | 59 | AR | - | N | - | front matter |
| abs | Abstract | 193 | AR | - | N | - | front matter |
| gloss | Glossary | 616 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. The UK as Reference Jurisdiction | 0 | K | S9 | N | - | why the UK as reference jurisdiction |
| 1.1 | 1.1 Why a Reference Jurisdiction at All | 86 | K | S9 | N | - | why the UK as reference jurisdiction |
| 1.2 | 1.2 Why the UK | 17 | K | S9 | N | - | why the UK as reference jurisdiction |
| 1.2.1 | 1.2.1 Wealth Data | 124 | K | S9 | N | - | why the UK as reference jurisdiction |
| 1.2.2 | 1.2.2 Administrative Capacity | 68 | K | S9 | N | - | why the UK as reference jurisdiction |
| 1.2.3 | 1.2.3 Constitutional Flexibility | 48 | K | S9 | N | - | why the UK as reference jurisdiction |
| 1.2.4 | 1.2.4 Political Salience | 61 | K | S9 | N | - | why the UK as reference jurisdiction |
| 1.2.5 | 1.2.5 Researcher Familiarity | 52 | K | S9 | N | - | why the UK as reference jurisdiction |
| 1.3 | 1.3 What Is and Is Not Being Modelled | 205 | K | S9 | N | - | what is and is not modelled |
| 1.4 | 1.4 The Wealth Tax Commission Comparison | 202 | M | S2 | N | - | Wealth Tax Commission comparison (WTC 500,000 threshold, 260bn) |
| 1.5 | 1.5 UK Institutional Architecture and WDT Requirements | 33 | K | S9 | N | - | UK institutions against WDT requirements: HMRC, VOA, OBR, tribunals |
| 1.5.1 | 1.5.1 HMRC | 196 | K | S9 | N | - | UK institutions against WDT requirements: HMRC, VOA, OBR, tribunals |
| 1.5.2 | 1.5.2 The Valuation Office Agency | 310 | K | S9 | N | - | UK institutions against WDT requirements: HMRC, VOA, OBR, tribunals |
| 1.5.3 | 1.5.3 The Office for Budget Responsibility | 580 | K | S9 | N | - | UK institutions against WDT requirements: HMRC, VOA, OBR, tribunals |
| 1.5.4 | 1.5.4 The Tax Tribunal System | 216 | K | S9 | N | - | UK institutions against WDT requirements: HMRC, VOA, OBR, tribunals |
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
| 4.3 | 4.3 Jurisdiction-specific legal and implementation work | 266 | M | S9 | N | - | jurisdiction-specific legal work (HMRC data access, Custodian form) |
| 4.4 | 4.4 Structural and irreducible limits of the design | 17 | D | - | N | - | limitations register |
| 4.5 | 4.5 Governing Council calibration parameters | 6 | D | - | N | - | limitations register |
