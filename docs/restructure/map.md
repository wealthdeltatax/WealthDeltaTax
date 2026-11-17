# Restructure, stage A: hub outline and spoke map (author decisions applied 2026-11-16)

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
Standalone (decided): 18 Addendums (ADD), 20 Institutional Selection (INST), 17 Scope Boundary (SCOPE, a meta paper outside the wheel). FAL is folded into S12 (decided). WFR (19, 19a) and LDW (21) concern people, so they feed spokes (S6, S7, S11), not standalone papers. S11 no longer draws on 17.

## 5. Decisions (author, 2026-11-16)
1. Spoke list and question-per-spoke shape: accepted. The ledger may still propose merges or splits.
2. FAL folds into S12.
3. The hub's problem section needs outputs. Add them: stage B also checks every spoke for outputs it needs that `outputs.yml` lacks, and lists them as proposed additions (with the problem section H1 first).
4. SCOPE stays outside the wheel. WFR and LDW go into spokes.
5. Spoke length 2,000 to 4,000 words: accepted provisionally. The author's experience is that it feels alarmingly short, so the ledger reports, per spoke, the words of material it keeps; if a spoke exceeds budget the budget is revisited then (split the spoke or raise the cap), not squeezed.

## 6. Not decided here
Site IDs and URLs (stage D), spoke template wording (stage C), the order of rewriting (stage E).

## 7. Changes after stage B (author, 2026-11-17)
- Cap raised to 6,000 words per spoke (author confirmed 6,000, 2026-11-17). Overflow rule: a spoke that holds more than the cap moves its less important material into an appendix spoke, id suffix `-A`, reached from the main spoke.
- **S4 Valuation routes** (VAL 1 to 6, 9 to 12) with **S4-A Declaration incentives** (VAL 7, VAL.A findings, VAL.B examples).
- **S6 Who pays** (RATES 2, WP 8.2, payslip) with **S6-A What they do** (BEHAV, BEHAV.A, CLOSE objections) and **S6-B Welfare comparison** (WFR, with the new welfare outputs).
- **S8-A Entity attribution** (ENT, CORP.A section E): a separate spoke, appendix to S8.
- 12 spokes become 12 main spokes plus 4 appendix spokes (S4-A, S6-A, S6-B, S8-A). Corrections to the "fed by" column are in `ledger.md` section 7 and apply.
- H1 problem outputs OH1a to OH1c and data facts D-H1a to D-H1c accepted for now.
