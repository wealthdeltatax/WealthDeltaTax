# Restructure, stage A: hub outline and spoke map (DRAFT for the author to mark up)

Brief 013g. Planning only. No spoke prose is written until the data gate (013g) opens. Spoke names, order and the list of standalone papers are proposals: the content ledger (stage B) tests them against what the 33 old papers actually say.

## 1. Shape
- **Hub:** one whitepaper for a general reader. Problem first. Target 5,000 to 7,000 words (old whitepaper: 15,306).
- **Spokes:** about 12 short pages, one per reader question, same shape each (short answer, evidence, strongest objection, Data block). Target 2,000 to 4,000 words each.
- **Data layer:** model v3 outputs (`docs/model-v3/outputs.yml`), the input register (`inputs.md`) and the UK data pack. Spokes cite output IDs (data hooks); numbers are filled at build and never typed.
- **Standalone:** papers that do not need the wheel. They link in, nothing links out to them for the argument.
- **Old papers:** retired once the new set is accepted. Their content and findings feed the ledger, nothing more. Zenodo copies are replaced later.

## 2. Hub outline (proposed)
| # | Section | Job | Data hooks |
|---|---|---|---|
| H0 | One-page summary | Problem, the tax, the three results, where to go next | O1, O2, O4a |
| H1 | The problem | What is wrong now and who bears it; why existing taxes do not fix it | TBD in ledger (see section 5) |
| H2 | The tax in one page | The mechanism, plain words, one worked example | none |
| H3 | What it does | Three headline results as P10, mean, P90 for the named schedules | O1, O2, O3, O4a, O4b |
| H4 | Why it is fair | Short moral case, links to S1 | none |
| H5 | How it could be wrong | The strongest objections and what would falsify the tax | O7, OS1, O8 |
| H6 | Where to go next | Reader routing block (section 3) | none |
| H7 | Data and method | Links to the data layer and the model | all |

## 3. Reader routing block (in H6)
| Reader | Start at |
|---|---|
| Economist | S4, S5, S6, then the data layer |
| Tax lawyer or administrator | S3, S4, S9 |
| Policymaker or adviser | S5, S7, S10, S11 |
| Business owner or accountant | S8, S4 |
| Philosopher or sceptic | S1, S2, S12 |
| Researcher wanting the numbers | the data layer, then S5 |

## 4. Spoke map (tentative; ledger confirms)
Source = old paper, by number.
| Spoke | Question it answers | Fed by (old papers) | v3 outputs | Depends on model numbers? |
|---|---|---|---|---|
| S1 Why | Is it fair? | 2 | none | no |
| S2 Prior work | What exists, what is missing? | 3a, 3b | none | no |
| S3 How it works | What exactly is taxed and when? | 1 (mechanism), 4, 13 | none | no |
| S4 Valuation | How is wealth measured? | 5, 5a, 5b | M-valuation hooks, TBD | partly |
| S5 Rates and revenue | What rate, what threshold, how much? | 8, 8a, 9, 9a, 11 | O1, O1a to O1d, OP1, OP4, OP5, OP3 | yes |
| S6 Who pays | Who pays, what do they do? | 10, 10a, 19, 19a | O2, O2b, O2c, O3, O5, O6, O8 | yes |
| S7 The fund and replaced taxes | Where does the money go? | 21, 11, parts of 8 | O1c, O1d, O4a, O4b | yes |
| S8 Companies | How are firms treated? | 6, 6a | O1b | partly |
| S9 Law and governance | Who runs it, on what law? | 7, 7a, 7b, 4 | none | no |
| S10 Politics and adoption | Can it pass, how is it staged? | 12, 12a, 15, 16, 13 | OP3, OP5 | partly |
| S11 Wider effects | Environment, welfare, scope | 14, 17, 19, 21 | O4a, O4b | partly |
| S12 How it could be wrong | What would falsify it? | 22, 10 (limits), 9 (sensitivity) | O7, OS1, tornado | yes |
Standalone candidates: 18 Addendums (ADD) and 20 Institutional Selection (INST), as the author said. 22 Falsification (FAL) is folded into S12 above; the author may prefer it standalone. 17 Scope Boundary and 19 Taxpayer Welfare overlap S11 and S6 and are the likeliest merges.

## 5. Decisions for the author
1. Is the spoke list right (merge, split, rename, drop)? Is the question-per-spoke shape right?
2. FAL: fold into S12 (proposed) or stand alone?
3. H1 needs data on the problem itself (what is wrong now). No v3 output covers it. Add outputs for the problem (current distribution, current burden), or does the hub cite existing public data only?
4. Which of SCOPE, WFR and LDW survive as spokes, merge, or go?
5. Spoke length target: 2,000 to 4,000 words OK?

## 6. Not decided here
Site IDs and URLs (stage D), spoke template wording (stage C), the order of rewriting (stage E).
