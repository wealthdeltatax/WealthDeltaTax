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
| 4.3 | 4.3 Route D Auction Mechanism | 702 | M | S4 | N | - | Route D auction; duplicates VAL 6.5 and 11 |
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

## 5_Valuing_Wealth (17034 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 107 | AR | - | N | - | front matter |
| rev | Revision History | 887 | AR | - | N | - | front matter |
| abs | Abstract | 340 | AR | - | N | - | front matter |
| gloss | Glossary | 698 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. The Valuation Problem | 629 | K | S4 | N | - | the valuation problem and the asset classification |
| 2 | 2. Asset Classification | 28 | K | S4 | N | - | the valuation problem and the asset classification |
| 2.1 | 2.1 Automatically Priced Assets | 41 | K | S4 | N | - | the valuation problem and the asset classification |
| 2.2 | 2.2 Fungible Assets | 91 | K | S4 | N | - | the valuation problem and the asset classification |
| 2.3 | 2.3 Non-Fungible Assets | 34 | K | S4 | N | - | the valuation problem and the asset classification |
| 2.4 | 2.4 Why Periodic Valuation and Audit Are Insufficient | 66 | K | S4 | N | - | the valuation problem and the asset classification |
| 3 | 3. Assessment Windows | 0 | M | S3 | N | - | assessment windows and borrowing; duplicates WP 3.6 |
| 3.1 | 3.1 Annual Reporting and Formal Assessment | 132 | M | S3 | N | - | assessment windows and borrowing; duplicates WP 3.6 |
| 3.2 | 3.2 Available Assessment Windows | 160 | M | S3 | N | - | assessment windows and borrowing; duplicates WP 3.6 |
| 3.3 | 3.3 Borrowing and Net Worth | 42 | M | S3 | N | - | assessment windows and borrowing; duplicates WP 3.6 |
| 4 | 4. The Four Valuation Routes | 178 | K | S4 | N | - | the four valuation routes |
| 4.1 | 4.1 Route A: Professional Valuation of Fungible Assets | 65 | K | S4 | N | - | the four valuation routes |
| 4.2 | 4.2 Route B: Professional Valuation of Non-Fungible Assets | 85 | K | S4 | N | - | the four valuation routes |
| 4.3 | 4.3 Route C: Self-Declaration of Fungible Assets | 133 | K | S4 | N | - | the four valuation routes |
| 4.4 | 4.4 Route D: Self-Declaration of Non-Fungible Assets | 163 | K | S4 | N | - | the four valuation routes |
| 5 | 5. The Self-Balancing Mechanism: Fungible Assets | 307 | K | S4 | P | - | self-balancing mechanism for fungible assets; figures are closed-form arithmetic |
| 5.1 | 5.1 The Grandfathering Baseline | 64 | K | S4 | P | - | self-balancing mechanism for fungible assets; figures are closed-form arithmetic |
| 5.2 | 5.2 The Must-Transfer Rule | 765 | K | S4 | P | - | self-balancing mechanism for fungible assets; figures are closed-form arithmetic |
| 5.3 | 5.3 Delta Continuity at Realisation | 74 | K | S4 | P | - | self-balancing mechanism for fungible assets; figures are closed-form arithmetic |
| 6 | 6. Non-Fungible Assets and Realisation | 0 | K | S4 | N | - | non-fungible assets and realisation (Route D) |
| 6.1 | 6.1 Why Periodic Accrual Is Not Workable for Non-Fungible As | 126 | K | S4 | N | - | non-fungible assets and realisation (Route D) |
| 6.2 | 6.2 Assessment During the Holding Period | 88 | K | S4 | N | - | non-fungible assets and realisation (Route D) |
| 6.3 | 6.3 The Realisation Calculation | 112 | K | S4 | N | - | non-fungible assets and realisation (Route D) |
| 6.4 | 6.4 Voluntary Settlement | 529 | K | S4 | N | - | non-fungible assets and realisation (Route D) |
| 6.5 | 6.5 Inheritance and the Auction Mechanism | 497 | K | S4 | N | - | non-fungible assets and realisation (Route D) |
| 6.6 | 6.6 Destruction, Theft, and Forced Removal | 40 | K | S4 | N | - | non-fungible assets and realisation (Route D) |
| 7.1 | 7.1 Declaration Strategy and the Rational Equilibrium | 2037 | K | S4 | Y | O7,NEW:alpha-curve | declaration strategy, understatement, overstatement; results from the v1 simulation |
| 7.2 | 7.2 Understatement: Deferred Liability and Dilution | 625 | K | S4 | Y | O7,NEW:alpha-curve | declaration strategy, understatement, overstatement; results from the v1 simulation |
| 7.3 | 7.3 Overstatement: Signalling and Confidence Effects | 883 | K | S4 | Y | O7,NEW:alpha-curve | declaration strategy, understatement, overstatement; results from the v1 simulation |
| 7.4 | 7.4 Boundary Conditions and Limitations | 259 | K | S4 | P | O7 | boundary conditions |
| 7.5 | 7.5 Portfolio Composition as a Structural Constraint on Decl | 724 | K | S4 | Y | O7,NEW:composition | portfolio composition limits deviation; needs share of wealth in observable assets by band (input) |
| 8 | 8. The Assessment Window Premium | 143 | M | S3 | N | - | assessment window premium; excluded from the reference model |
| 9 | 9. The Public Valuation Register | 725 | K | S4 | N | - | public valuation register |
| 10 | 10. Professional Valuation | 0 | K | S4 | N | - | professional valuation route |
| 10.1 | 10.1 Purpose | 43 | K | S4 | N | - | professional valuation route |
| 10.2 | 10.2 Competitive Tender Model | 143 | K | S4 | N | - | professional valuation route |
| 10.3 | 10.3 Cost Sharing with a Fee Cap | 84 | K | S4 | N | - | professional valuation route |
| 10.4 | 10.4 The Two-Stage Review Process | 130 | K | S4 | N | - | professional valuation route |
| 10.5 | 10.5 The Valuation Code | 186 | K | S4 | N | - | professional valuation route |
| 10.6 | 10.6 Valuation Governance | 217 | K | S9 | N | - | Valuation Code Board governance |
| 11 | 11. The Route D Auction Mechanism — Three Uses of One Proces | 175 | K | S4 | N | - | Route D auction, three uses |
| 11.1 | 11.1 Deterrent Logic | 130 | K | S4 | N | - | Route D auction, three uses |
| 11.2 | 11.2 Voluntary Hard-Reset Auction | 140 | K | S4 | N | - | Route D auction, three uses |
| 11.3 | 11.3 Corrective Auction: Trigger and Process | 446 | K | S4 | N | - | Route D auction, three uses |
| 11.4 | 11.4 Inheritance Auction | 189 | K | S4 | N | - | Route D auction, three uses |
| 11.5 | 11.5 Scope | 142 | K | S4 | N | - | Route D auction, three uses |
| 12 | 12. Administration and Fraud Detection | 75 | K | S9 | N | - | administration, reporting, statistical review, penalties |
| 12.1 | 12.1 Annual Reporting Requirements | 66 | K | S9 | N | - | administration, reporting, statistical review, penalties |
| 12.2 | 12.2 The Purpose of Audit: Fraud, Not Valuation | 136 | K | S4 | N | - | audit is for fraud, not valuation |
| 12.3 | 12.3 Statistical Review | 110 | K | S9 | N | - | administration, reporting, statistical review, penalties |
| 12.4 | 12.4 Penalties | 81 | K | S9 | N | - | administration, reporting, statistical review, penalties |
| 13 | 13. The Sovereign Liquidity Facility | 340 | K | S7 | N | - | Sovereign Liquidity Facility |
| 14 | 14. Limitations and Further Work | 0 | D | - | N | - | limitations register, v1 validation note, premium calibration, conclusion |
| 14.1 | 14.1 Formal Modelling Gaps | 93 | D | - | N | - | limitations register, v1 validation note, premium calibration, conclusion |
| 14.2 | 14.2 Phase One Empirical Unknowns | 389 | D | - | N | - | limitations register, v1 validation note, premium calibration, conclusion |
| 14.3 | 14.3 Jurisdiction-Specific Legal and Implementation Work | 481 | M | S12 | N | - | Route D entry-basis boundary and the other two boundaries |
| 14.4 | 14.4 Structural and Irreducible Limits of the Design | 513 | M | S12 | N | - | Route D entry-basis boundary and the other two boundaries |
| 14.5 | 14.5 Governing Council Calibration Parameters | 91 | D | - | N | - | limitations register, v1 validation note, premium calibration, conclusion |
| 15 | 15. Conclusion | 757 | D | - | N | - | limitations register, v1 validation note, premium calibration, conclusion |

## 5a_Valuing_Wealth_Mathematical_and_Simulation_Appendix (17111 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 108 | AR | - | N | - | front matter |
| rev | Revision History | 690 | AR | - | N | - | front matter |
| ~A. | A. Mathematical Model and Incentive Analysis | 0 | DL | method note for O7 | N | - | formal model of declaration incentives (notation, recursion, propositions); the specification M7 needs |
| A.1 | A.1 Purpose | 298 | DL | method note for O7 | N | - | formal model of declaration incentives (notation, recursion, propositions); the specification M7 needs |
| A.2 | A.2 Main Findings (+5) | 1374 | K | S4 | Y | O7,NEW:alpha-curve | five findings in short form |
| A.3 | A.3 Model Assumptions and Notation (+4) | 955 | DL | method note for O7 | N | - | formal model of declaration incentives (notation, recursion, propositions); the specification M7 needs |
| A.4 | A.4 Multi-Period Incentive Model (+7) | 972 | DL | method note for O7 | N | - | formal model of declaration incentives (notation, recursion, propositions); the specification M7 needs |
| A.5 | A.5 Scope of the Arguments (+6) | 1625 | DL | method note for O7 | N | - | formal model of declaration incentives (notation, recursion, propositions); the specification M7 needs |
| A.6 | A.6 The Declaration Equilibrium: A Broad Tolerant Zone with  | 1275 | M | S4 | Y | O7,NEW:alpha-curve | declaration equilibrium; duplicates VAL 7.1 |
| ~B. | B. Simulation Methodology | 0 | DL | method note for O7 | N | - | simulation algorithm, parameter table, metrics |
| B | B.1 Purpose (+6) | 1198 | DL | method note for O7 | N | - | simulation algorithm, parameter table, metrics |
| ~C. | C. WDT Valuation Analysis: Summary Tables | 102 | AR | - | Y | O7,NEW:alpha-curve | v1 result tables C.1 to C.12 (0 FAILs, v1 only); v3 regenerates them |
| C | C.1 Total Tax Paid (TTP) Difference Relative to Honest Decla | 6568 | AR | - | Y | O7,NEW:alpha-curve | v1 result tables C.1 to C.12 (0 FAILs, v1 only); v3 regenerates them |
| C.6 | C.6 Terminal Net Worth After Refunds: Refund Protection Rati | 199 | AR | - | Y | NEW:refund-protection | refund protection ratio in loss years: understaters lose refund protection |
| ~D. | D. Mechanism Cases | 27 | D | - | N | - | five abstract cases; covered by VAL.B and A.5 |
| D | D.1 Case 1: Persistent Understatement, Asset Never Realises  | 564 | D | - | N | - | five abstract cases; covered by VAL.B and A.5 |
| ~E. | E. Route Specification Tables | 24 | M | S4 | N | - | route specification tables; duplicate VAL 4 |
| E | E.1 Route A: Professional Valuation of Fungible Assets (+4) | 873 | M | S4 | N | - | route specification tables; duplicate VAL 4 |
| ~F. | F. Annual Reporting Requirements | 10 | M | S9 | N | - | annual reporting requirements |
| F | F.1 Taxpayer Annual Return (+3) | 249 | M | S9 | N | - | annual reporting requirements |

## 5b_Valuing_Wealth_Worked_Examples_Appendix (5592 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 92 | AR | - | N | - | front matter |
| rev | Revision History | 204 | AR | - | N | - | front matter |
| ~Reader | Reader's Guide | 309 | D | - | N | - | reader's guide and summary table |
| ~J. | J. The Deferred Delta | 37 | K | S4 | P | NEW:example-figures | five worked examples tethered to the five VAL claims; figures from the v1 simulation or closed-form arithmetic, to be regenerated as fixtures |
| J | J.1 Setup (+5) | 687 | K | S4 | P | NEW:example-figures | five worked examples tethered to the five VAL claims; figures from the v1 simulation or closed-form arithmetic, to be regenerated as fixtures |
| ~K. | K. Dilution Compounds with Growth | 46 | K | S4 | P | NEW:example-figures | five worked examples tethered to the five VAL claims; figures from the v1 simulation or closed-form arithmetic, to be regenerated as fixtures |
| K | K.1 Setup (+6) | 719 | K | S4 | P | NEW:example-figures | five worked examples tethered to the five VAL claims; figures from the v1 simulation or closed-form arithmetic, to be regenerated as fixtures |
| ~L. | L. Why Route D Defers to Realisation | 45 | K | S4 | P | NEW:example-figures | five worked examples tethered to the five VAL claims; figures from the v1 simulation or closed-form arithmetic, to be regenerated as fixtures |
| L | L.1 Setup (+6) | 812 | K | S4 | P | NEW:example-figures | five worked examples tethered to the five VAL claims; figures from the v1 simulation or closed-form arithmetic, to be regenerated as fixtures |
| ~M. | M. Voluntary Settlement — Certainty, Not Avoidance | 69 | K | S4 | P | NEW:example-figures | five worked examples tethered to the five VAL claims; figures from the v1 simulation or closed-form arithmetic, to be regenerated as fixtures |
| M | M.1 Setup (+5) | 964 | K | S4 | P | NEW:example-figures | five worked examples tethered to the five VAL claims; figures from the v1 simulation or closed-form arithmetic, to be regenerated as fixtures |
| ~N. | N. Forecast Exposure | 46 | K | S4 | P | NEW:example-figures | five worked examples tethered to the five VAL claims; figures from the v1 simulation or closed-form arithmetic, to be regenerated as fixtures |
| N | N.1 Setup (+6) | 1373 | K | S4 | P | NEW:example-figures | five worked examples tethered to the five VAL claims; figures from the v1 simulation or closed-form arithmetic, to be regenerated as fixtures |
| ~O. | O. Summary of Design Properties Illustrated | 189 | D | - | N | - | reader's guide and summary table |

## 6_Corporate_Architecture (8681 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 112 | AR | - | N | - | front matter |
| rev | Revision History | 116 | AR | - | N | - | front matter |
| abs | Abstract | 286 | AR | - | N | - | front matter |
| gloss | Glossary | 462 | DL | glossary | N | - | merge into the build glossary |
| 1 | 1. Introduction | 286 | M | S8 | N | - | introduction; the individual-centred logic duplicates WP 3.2 |
| 2 | 2. Why Existing Corporate Tax Systems Are Insufficient | 430 | K | S8 | N | - | why existing corporate taxes fall short; listed against private; lifecycle events |
| 2.1 | 2.1 Existing Administrative Analogues | 183 | K | S8 | N | - | why existing corporate taxes fall short; listed against private; lifecycle events |
| 3 | 3. The Individual-Centred Logic and Its Limits | 113 | M | S8 | N | - | introduction; the individual-centred logic duplicates WP 3.2 |
| 4 | 4. The Listed/Private Distinction | 110 | K | S8 | N | - | why existing corporate taxes fall short; listed against private; lifecycle events |
| 4.1 | 4.1 Corporate Lifecycle Events | 589 | K | S8 | N | - | why existing corporate taxes fall short; listed against private; lifecycle events |
| 5 | 5. The Listed Company Corporate Delta Levy | 0 | K | S8 | Y | O1b | the corporate delta levy as escrow, annual cycle, tranches, year end, loss years |
| 5.1 | 5.1 The Mechanism in One Place | 701 | K | S8 | Y | O1b | the corporate delta levy as escrow, annual cycle, tranches, year end, loss years |
| 5.2 | 5.2 Annual Cycle: Measurement and Reporting | 383 | K | S8 | Y | O1b | the corporate delta levy as escrow, annual cycle, tranches, year end, loss years |
| 5.3 | 5.3 Tranche Outcomes During the Year | 548 | K | S8 | Y | O1b | the corporate delta levy as escrow, annual cycle, tranches, year end, loss years |
| 5.4 | 5.4 Year-End Settlement | 350 | K | S8 | Y | O1b | the corporate delta levy as escrow, annual cycle, tranches, year end, loss years |
| 5.5 | 5.5 Loss Years | 112 | K | S8 | Y | O1b | the corporate delta levy as escrow, annual cycle, tranches, year end, loss years |
| 5.6 | 5.6 Residual Imperfections | 188 | M | S12 | N | - | residual imperfections (assessment-date gaming) |
| 6 | 6. The Corporate Equity Settlement Facility | 0 | K | S8 | N | - | Corporate Equity Settlement Facility |
| 6.1 | 6.1 Purpose and Scope | 252 | K | S8 | N | - | Corporate Equity Settlement Facility |
| 6.2 | 6.2 Mechanism | 384 | K | S8 | N | - | Corporate Equity Settlement Facility |
| 6.3 | 6.3 Relationship to the SWF | 334 | K | S8 | N | - | Corporate Equity Settlement Facility |
| 6.4 | 6.4 Governing Council Calibration Parameters | 149 | DL | parameter register | N | - | Governing Council calibration parameters |
| 7 | 7. Institutional Ownership | 592 | K | S8 | N | - | institutional ownership; synthetic exposure and derivatives |
| 8 | 8. Synthetic Exposure and Derivatives | 496 | K | S8 | N | - | institutional ownership; synthetic exposure and derivatives |
| 9 | 9. Limitations and Required Further Work | 0 | D | - | N | - | limitations register and conclusion |
| 9.1 | 9.1 Formal modelling gaps | 47 | D | - | N | - | limitations register and conclusion |
| 9.2 | 9.2 Phase One empirical unknowns | 248 | M | S12 | Y | O1b,O1d | whether the levy displaces corporation tax outright |
| 9.3 | 9.3 Jurisdiction-specific legal and implementation work | 58 | D | - | N | - | limitations register and conclusion |
| 9.4 | 9.4 Structural and irreducible limits of the design | 506 | M | S12 | N | - | structural limits of the corporate instrument |
| 9.5 | 9.5 Governing Council calibration parameters | 371 | DL | parameter register | N | - | Governing Council calibration parameters |
| 10 | 10. Conclusion | 275 | D | - | N | - | limitations register and conclusion |

## 6a_Corporate_Architecture_Appendix (15089 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 97 | AR | - | N | - | front matter |
| rev | Revision History | 45 | AR | - | N | - | front matter |
| ~A. | A. Collection Mechanics and Worked Illustrations | 0 | AR | - | N | - | collection mechanics detail; kept for the statute-drafting phase |
| A.1 | A.1 The Two-Deadline Structure | 322 | M | S8 | N | - | two-deadline structure, sequencing, broker and nominee case; duplicate CORP 5 |
| A.2 | A.2 Shareholders Who Sell Before the Assessment Date** | 129 | AR | - | N | - | collection mechanics detail; kept for the statute-drafting phase |
| A.3 | A.3 Partial-Year Attribution | 92 | AR | - | N | - | collection mechanics detail; kept for the statute-drafting phase |
| A.4 | A.4 Sequencing | 201 | M | S8 | N | - | two-deadline structure, sequencing, broker and nominee case; duplicate CORP 5 |
| A.5 | A.5 Loss Years and Private Arrangements | 54 | AR | - | N | - | collection mechanics detail; kept for the statute-drafting phase |
| A.6 | A.6 Worked Illustration: Standard Shareholders | 344 | K | S8 | N | - | worked illustration with three shareholders |
| A.7 | A.7 Corporate Entities as Shareholders | 167 | AR | - | N | - | collection mechanics detail; kept for the statute-drafting phase |
| A.8 | A.8 No Minimum Threshold | 36 | AR | - | N | - | collection mechanics detail; kept for the statute-drafting phase |
| A.9 | A.9 Intermediary Chain Illustrations | 0 | M | S8 | N | - | two-deadline structure, sequencing, broker and nominee case; duplicate CORP 5 |
| A.9.1 | A.9.1 Broker/Nominee Case | 500 | M | S8 | N | - | two-deadline structure, sequencing, broker and nominee case; duplicate CORP 5 |
| A.9.2 | A.9.2 Pooled Fund Case | 198 | AR | - | N | - | collection mechanics detail; kept for the statute-drafting phase |
| ~B. | B. Corporate Rate Calibration | 83 | M | S8 | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.1 | B.1 The Floor Rate ($\tau_0$): Collection Security | 475 | M | S8 | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.1.1 | B.1.1 Phase One data requirement | 112 | DL | parameter register | N | - | Phase One data requirements for calibration |
| B.2 | B.2 The Final Charge on Permanently Unattributable Ownership | 68 | M | S8 | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.2.1 | B.2.1 The deterrence condition | 93 | M | S8 | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.2.2 | B.2.2 The refund-forfeiture effect | 123 | M | S8 | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.2.3 | B.2.3 The revenue-recovery ceiling | 83 | M | S8 | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.2.4 | B.2.4 The legal proportionality constraint, and why it is we | 228 | M | S8 | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.2.5 | B.2.5 One carve-out applies | 81 | M | S8 | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.2.6 | B.2.6 The resulting calibration range | 107 | M | S8 | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.2.7 | B.2.7 Phase One data requirement | 134 | DL | parameter register | N | - | Phase One data requirements for calibration |
| B.2.8 | B.2.8 The ramp structure | 341 | M | S8 | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.2.9 | B.2.9 The joint-calibration constraint | 402 | M | S8 | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.3 | B.3 Intermediary-Level Provisioning Floor | 354 | M | S8 | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| B.4 | B.4 The Rejected Pool-Average Alternative | 82 | M | S8 | N | - | calibration reasoning for the floor rate and the final charge; the values live in the parameter register |
| ~C. | C. Ownership Structure Classification Under the Attribution  | 935 | K | S8 | N | - | ownership structure classification under the attribution test |
| ~D. | D. Administrative Burden | 0 | K | S8 | N | - | administrative burden of the corporate mechanism |
| D | D.1 Purpose (+4) | 1078 | K | S8 | N | - | administrative burden of the corporate mechanism |
| D.6 | D.6 Transitional Considerations and the Parallel-Running Ris | 220 | K | S8 | N | - | administrative burden of the corporate mechanism |
| D.7 | D.7 Summary | 208 | K | S8 | N | - | administrative burden of the corporate mechanism |
| ~E. | E. Non-Corporate Instruments and the Attribution Test | 0 | SA | ENT (proposed) | N | - | non-corporate instruments and the attribution test; proposed standalone paper, author to decide |
| E.1 | E.1 Purpose | 204 | SA | ENT (proposed) | N | - | non-corporate instruments and the attribution test; proposed standalone paper, author to decide |
| E | E.2 Charitable Vehicles (+17) | 5061 | SA | ENT (proposed) | N | - | non-corporate instruments and the attribution test; proposed standalone paper, author to decide |
| E.9 | E.9 Market Manipulation and the Bilateral-Claim Structure of | 1233 | SA | ENT (proposed) | P | - | market manipulation and short positions (v3 does not model manipulation) |
| ~F. | F. $\tau_f$: Foreign Attribution and Diplomatic Rate-Setting | 560 | K | S8 | N | - | foreign attribution and diplomatic rate-setting |
| F.1 | F.1 $\tau_c$ as an Ownership-Composition Lever | 401 | K | S8 | N | - | foreign attribution and diplomatic rate-setting |
| ~G. | G. Existing $\tau$ parameters | 238 | DL | parameter register | N | - | existing tau parameters |

## 7_Constitutional_Governance (13117 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 105 | AR | - | N | - | front matter |
| rev | Revision History | 297 | AR | - | N | - | front matter |
| abs | Abstract | 403 | AR | - | N | - | front matter |
| gloss | Glossary | 2553 | DL | glossary | N | - | 2,553 words of role and term definitions; merge into the build glossary |
| 1 | 1. Introduction | 457 | K | S9 | N | - | the governance problem the paper addresses |
| 1.1 | 1.1 The Governance Problem This Paper Addresses | 527 | K | S9 | N | - | the governance problem the paper addresses |
| 2 | 2. The Standard This Design Is Held To | 320 | K | S9 | N | - | the standard the design is held to; mechanism-shaped test |
| 2.1 | 2.1 The Mechanism-Shaped Test | 448 | K | S9 | N | - | the standard the design is held to; mechanism-shaped test |
| 3 | 3. Deriving the Architecture | 152 | K | S9 | N | - | deriving the architecture; dividend recipients' standing |
| 3.1 | 3.1 The Corrected Derivation | 407 | K | S9 | N | - | deriving the architecture; dividend recipients' standing |
| 3.2 | 3.2 Closing the Dividend Recipients' Standing | 851 | K | S9 | N | - | deriving the architecture; dividend recipients' standing |
| 4 | 4. Designing Against Capture | 379 | K | S9 | N | - | designing against capture; structural safeguards, anti-collusion, enumerated clauses, tiered review |
| 5 | 5. The Structural Safeguards | 43 | K | S9 | N | - | designing against capture; structural safeguards, anti-collusion, enumerated clauses, tiered review |
| 5.1 | 5.1 The Anti-Collusion Guarantee | 303 | K | S9 | N | - | designing against capture; structural safeguards, anti-collusion, enumerated clauses, tiered review |
| 5.2 | 5.2 The Enumerated Structural Clauses | 1395 | K | S9 | N | - | designing against capture; structural safeguards, anti-collusion, enumerated clauses, tiered review |
| 5.3 | 5.3 Tiered Review, Rebalancing, and Transparency | 832 | K | S9 | N | - | designing against capture; structural safeguards, anti-collusion, enumerated clauses, tiered review |
| 6 | 6. The Executive Bodies | 28 | K | S9 | N | - | executive bodies: Valuation Bodies, Allocator, Administrator |
| 6.1 | 6.1 The Valuation Bodies | 357 | K | S9 | N | - | executive bodies: Valuation Bodies, Allocator, Administrator |
| 6.2 | 6.2 The Allocator | 444 | K | S9 | N | - | executive bodies: Valuation Bodies, Allocator, Administrator |
| 6.3 | 6.3 The SWF Custodian | 656 | K | S7 | N | - | SWF Custodian |
| 6.4 | 6.4 The Administrator | 462 | K | S9 | N | - | executive bodies: Valuation Bodies, Allocator, Administrator |
| 7 | 7. Limitations and Further Work | 11 | D | - | N | - | limitations register, calibration list and conclusion |
| 7.1 | 7.1 Formal modelling gaps | 93 | D | - | N | - | limitations register, calibration list and conclusion |
| 7.2 | 7.2 Phase One empirical unknowns | 401 | M | S12 | N | - | empirical unknowns (volunteer rate under lottery, constituency dissolution) |
| 7.3 | 7.3 Jurisdiction-specific legal and implementation work | 164 | D | - | N | - | limitations register, calibration list and conclusion |
| 7.4 | 7.4 Structural and irreducible limits of the design | 344 | M | S12 | N | - | governance entropy and its four sub-forms |
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
| ~E. | E. Governance Decay: Four Sub-Forms | 78 | M | S12 | N | - | governance decay in four sub-forms; limits feed the failure section |
| E | E.1 Definitional Drift (+4) | 1610 | M | S12 | N | - | governance decay in four sub-forms; limits feed the failure section |

## 7b_Constitutional_Governance_Operational_Appendix (22067 words)

| Sec | Section | Words | Disp | Target | Model | Demands | Note |
|---|---|---:|---|---|---|---|---|
| pre | (preamble) | 95 | AR | - | N | - | front matter |
| rev | Revision History | 453 | AR | - | N | - | front matter |
| ~A. | A. The Chambers in Full | 0 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |
| A | A.1 The Taxpayer Chamber (TP) (+18) | 3097 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |
| ~B. | B. The Executive Bodies in Full | 69 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |
| B | B.1 The Valuation Bodies (VB-1, VB-2, VB-3) (+18) | 3085 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |
| B.3 | B.3 The SWF Custodian | 528 | M | S7 | N | - | SWF Custodian, institutional form, stress function |
| B.4.7 | B.4.7 The Privacy Election: Binary Disclosure and the Rate D | 692 | M | S9 | N | - | privacy election and rate differential |
| ~C. | C. Voting Mechanics in Full | 0 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |
| C | C.1 The Dual-Threshold Calculation: Worked Arithmetic (+7) | 3490 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |
| ~D. | D. The Rebalancing Mechanism in Full | 0 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |
| D | D.1 Conservation Arithmetic: How Vote Share Moves (+3) | 1179 | AR | - | N | - | operational specification of chambers, bodies, voting, rebalancing, auctions and the corporate facility mandate; kept for statute drafting, not for readers |
| ~E. | E. The SWF: Operational Detail | 0 | AR | - | N | - | SWF operational detail; solvency floor, drawdown, closure bonds, unit-holder rights |
| E.1 | E.1 The Solvency Floor: Definition and the Automatic-Consequ | 270 | AR | - | N | - | SWF operational detail; solvency floor, drawdown, closure bonds, unit-holder rights |
| E.2 | E.2 Drawdown Conditions: Pre-Crisis Commitment and the Annua | 233 | AR | - | N | - | SWF operational detail; solvency floor, drawdown, closure bonds, unit-holder rights |
| E.3 | E.3 The Closure Bond Facility: Bond Posting Sequence and Set | 643 | AR | - | N | - | SWF operational detail; solvency floor, drawdown, closure bonds, unit-holder rights |
| E.4 | E.4 Unit-Holder Rights: Financial Rights, Investment Input,  | 501 | AR | - | N | - | SWF operational detail; solvency floor, drawdown, closure bonds, unit-holder rights |
| E.5 | E.5 Stewardship Statements: Annual Cycle, Mandatory Content, | 315 | AR | - | N | - | SWF operational detail; solvency floor, drawdown, closure bonds, unit-holder rights |
| E.6 | E.6 Institutional Form: Candidate Mapping (UK Reference) | 198 | M | S7 | N | - | SWF Custodian, institutional form, stress function |
| E.7 | E.7 Custodian Investment Mandate: Inflationary Conditions | 641 | AR | - | N | - | SWF operational detail; solvency floor, drawdown, closure bonds, unit-holder rights |
| E.8 | E.8 Custodian Alignment Mechanisms | 419 | AR | - | N | - | SWF operational detail; solvency floor, drawdown, closure bonds, unit-holder rights |
| E.9 | E.9 The Stress Function | 300 | M | S7 | N | - | SWF Custodian, institutional form, stress function |
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
| 2 | 2. What Taxpayers Actually Pay | 1925 | K | S6 | Y | O2,O3,O2b,O5,O6 | what taxpayers actually pay: revenue-weighted burden and the lifetime effective rate on gains; 204 figures, all v1 |
| 3 | 3. The Revenue Claim | 465 | K | S5 | Y | O1 | the revenue claim and the direction of conservatism; v3 must test whether every assumption still errs low |
| 3.1 | 3.1 Direction of Conservatism | 469 | K | S5 | Y | O1 | the revenue claim and the direction of conservatism; v3 must test whether every assumption still errs low |
| 4 | 4. The Rate Function | 883 | K | S5 | P | - | the logistic rate function; named schedules S_low, S_central, S_high replace the single canonical set |
| 5.1 | 5.1 The Wealth Distribution | 541 | DL | input register | Y | - | wealth distribution (WAS deciles, Pareto tail) and growth model; inputs D4 and D1 |
| 5.2 | 5.2 The Growth Model | 343 | DL | input register | Y | - | wealth distribution (WAS deciles, Pareto tail) and growth model; inputs D4 and D1 |
| 6 | 6. The Two Models and How They Connect | 285 | K | S7 | Y | OP1 | the two models, sizing the short and long reserves |
| 6.1 | 6.1 Sizing the SRR | 428 | K | S7 | Y | OP1 | the two models, sizing the short and long reserves |
| 6.2 | 6.2 Sizing the LRR | 272 | K | S7 | Y | OP1 | the two models, sizing the short and long reserves |
| 6.3 | 6.3 The Two Internal Milestones and What They Gate | 769 | K | S7 | Y | OP1 | the two internal milestones and what they gate |
| 7.1 | 7.1 Revenue Results and Coverage | 623 | K | S5 | Y | O1,O1a | revenue results and coverage at 2000 Balanced parameters (v1) |
| 7.2 | 7.2 Historical Starting-Year Sensitivity | 920 | K | S5 | Y | O1,OP1 | historical start-year sensitivity; v3 level 1 return paths replace it |
| 7.3 | 7.3 SRR and LRR Milestones | 460 | K | S7 | Y | OP1 | SRR and LRR milestones |
| 7.4 | 7.4 Route D Deferred Revenue and Capitalisation Window Timin | 509 | K | S5 | P | NEW:composition | Route D deferred revenue and window timing; needs the share of base on Route D |
| 7.5 | 7.5 Revenue Under the Predicted Declaration Distribution** | 617 | K | S5 | Y | O7,NEW:alpha-curve | revenue under the predicted declaration distribution |
| 8.1 | 8.1 The Corporate Levy | 461 | K | S8 | Y | O1b | corporate levy, v1 figure |
| 8.2 | 8.2 The Ultra-High-Net-Worth Tail | 145 | M | S5 | Y | NEW:payers | UHNW tail beyond the Pareto bound; input D4 |
| 8.3 | 8.3 Combined Pre-Behavioural Estimate | 244 | K | S5 | Y | O1,O1a,O1b | combined pre-behavioural estimate |
| 9 | 9. Limitations and Further Work | 0 | D | - | N | - | empty heading, inherited items, conclusion |
| 9.1 | 9.1 Formal modelling gaps | 171 | M | S12 | N | - | modelling gaps, pre-behavioural caveat, heterogeneous tier stylisation |
| 9.2 | 9.2 Phase One empirical unknowns | 185 | M | S12 | N | - | modelling gaps, pre-behavioural caveat, heterogeneous tier stylisation |
| 9.3 | 9.3 Jurisdiction-specific legal and implementation work | 30 | D | - | N | - | empty heading, inherited items, conclusion |
| 9.4 | 9.4 Structural and irreducible limits of the design | 221 | M | S12 | N | - | modelling gaps, pre-behavioural caveat, heterogeneous tier stylisation |
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
| 2 | 2. What the Sweeps Are Measuring | 51 | M | S5 | Y | NEW:feasibility-map | what the sweeps measure; v3 replaces the properties with the feasibility map |
| 2.1 | 2.1 The Tolerant Zone and Fiscal Coverage | 166 | M | S5 | Y | NEW:feasibility-map | what the sweeps measure; v3 replaces the properties with the feasibility map |
| 2.2 | 2.2 The N-Crossing Threshold and LRR Fill Year | 783 | M | S5 | Y | NEW:feasibility-map | what the sweeps measure; v3 replaces the properties with the feasibility map |
| 2.3 | 2.3 The Understater Penalty Plateau and What It Indicates | 562 | M | S5 | Y | NEW:feasibility-map | what the sweeps measure; v3 replaces the properties with the feasibility map |
| 2.4 | 2.4 Reading the Two Datasets in Parallel | 347 | M | S5 | Y | NEW:feasibility-map | what the sweeps measure; v3 replaces the properties with the feasibility map |
| 3 | 3. $\tau_0$ — The Entry Rate | 26 | M | S5 | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 3.1 | 3.1 What $\tau_0$ Controls on the Declaration Mechanism (SWE | 889 | M | S5 | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 3.2 | 3.2 What $\tau_0$ Controls on Fiscal Outcomes (SWEEPS.R) | 446 | M | S5 | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 3.3 | 3.3 What the Council Is Calibrating When It Sets $\tau_0$ | 266 | M | S5 | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 4 | 4. $\tau_m$ — The Ceiling Rate | 35 | M | S5 | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 4.1 | 4.1 What $\tau_m$ Controls on the Declaration Mechanism (SWE | 560 | M | S5 | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 4.2 | 4.2 What $\tau_m$ Controls on Fiscal Outcomes (SWEEPS.R) | 323 | M | S5 | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 4.3 | 4.3 What the Council Is Calibrating When It Sets $\tau_m$ | 294 | M | S5 | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 5 | 5. $k$ — The Steepness Parameter | 173 | M | S5 | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 5.1 | 5.1 What $k$ Controls on the Declaration Mechanism (SWEEPS.V | 770 | M | S5 | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 5.2 | 5.2 What $k$ Controls on Fiscal Outcomes (SWEEPS.R) | 407 | M | S5 | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 5.3 | 5.3 What the Council Is Calibrating When It Sets k | 303 | M | S5 | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 6 | 6. $W_{min}$ — The Exemption Threshold | 215 | M | S5 | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 6.1 | 6.1 What $W_{min}$ Controls on the Declaration Mechanism (SW | 500 | M | S5 | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 6.2 | 6.2 What $W_{min}$ Controls on Fiscal Outcomes (SWEEPS.R) | 377 | M | S5 | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 6.3 | 6.3 What the Council Is Calibrating When It Sets $W_{min}$ | 369 | M | S5 | Y | NEW:feasibility-map,NEW:tornado | one passage per lever: entry rate, ceiling rate, steepness, threshold; v3 sweeps the schedule and the threshold as levers |
| 7 | 7. The Parameter Hierarchy and Its Two Faces | 0 | DL | parameter register | N | - | operational parameters (premium, final-charge ramp, rotation pace, privacy differential, facility) |
| 7.1 | 7.1 The Two Hierarchies | 738 | K | S5 | Y | NEW:tornado | the two parameter hierarchies (fiscal and mechanism) |
| 7.2 | 7.2 Chamber Positions and the Stabilising Effect of Disagree | 970 | M | S9 | P | - | chamber positions on parameters and the stabilising effect of disagreement |
| 7.3 | 7.3 Growth Rate Sensitivity | 608 | K | S5 | Y | O1 | growth-rate sensitivity; covered by level 1 return paths |
| 7.4 | 7.4 Cross-Parameter Coverage Fan | 438 | M | S5 | Y | NEW:feasibility-map | cross-parameter coverage fan |
| 7.5 | 7.5 Synthetic Stress-Test: Cyclical Growth Scenarios | 775 | K | S12 | Y | NEW:stress | synthetic cyclical growth stress test; covered only if level 1 sampling includes synthetic cycles |
| 8 | 8. The Operational Parameters | 46 | DL | parameter register | N | - | operational parameters (premium, final-charge ramp, rotation pace, privacy differential, facility) |
| 8.1 | 8.1 The Assessment Window Premium | 90 | DL | parameter register | N | - | operational parameters (premium, final-charge ramp, rotation pace, privacy differential, facility) |
| 8.2 | 8.2 The $\tau_{h}$ Ramp | 123 | DL | parameter register | N | - | operational parameters (premium, final-charge ramp, rotation pace, privacy differential, facility) |
| 8.3 | 8.3 The LRR Drawdown Pace | 1331 | M | S7 | P | - | LRR drawdown pace and chamber positions |
| 8.4 | 8.4 Route C Rotation Pace | 109 | DL | parameter register | N | - | operational parameters (premium, final-charge ramp, rotation pace, privacy differential, facility) |
| 8.5 | 8.5 The Privacy Rate Differential | 114 | DL | parameter register | N | - | operational parameters (premium, final-charge ramp, rotation pace, privacy differential, facility) |
| 8.6 | 8.6 Corporate Facility Parameters | 96 | DL | parameter register | N | - | operational parameters (premium, final-charge ramp, rotation pace, privacy differential, facility) |
| 9 | 9. The Small Lever Set as a Design Feature | 514 | K | S5 | N | - | the small lever set as a design feature |
| 10 | 10. What Phase One Needs to Measure for Calibration | 466 | M | S10 | N | - | what Phase One needs to measure |
| 11 | 11. Limitations | 1211 | M | S12 | P | - | limitations of the sweeps (single reference taxpayer, population extrapolation) |
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
| B.6 | B.6  $\tau_0$ × N Joint Surface — N-crossing for $\alpha$ =  | 475 | AR | - | Y | NEW:feasibility-map | v1 heatmaps and figure index for the four parameters (C.1 metric across alpha and g) |
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
