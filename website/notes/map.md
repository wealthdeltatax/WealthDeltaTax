# Restructure, stage A: hub outline and spoke map (author decisions applied 2026-11-16)

> **Ids (author, 2026-11-17).** Spoke shortcodes (`website/notes/shortcodes.md`) are the page ids, URLs, front-matter `spoke:` values and figure and table ids. Where this file still writes `S1` to `S12`, read it through `website/notes/ids-map.md`; the S numbers are planning labels only.

Brief 013g. Planning only. No spoke prose is written until the data gate (013g) opens. Spoke names, order and the list of standalone papers are proposals: the content ledger (stage B) tests them against what the 33 old papers actually say.

## 1. Shape
- **Hub:** one whitepaper for a general reader. Problem first. Target 5,000 to 7,000 words (old whitepaper: 15,306).
- **Spokes:** about 12 short pages, one per reader question, same shape each (short answer, evidence, strongest objection, Data block). Target 2,000 to 4,000 words each.
- **Data layer:** model v3 outputs (`model-specs/outputs.yml`), the input register (`inputs.md`) and the UK data pack. Spokes cite output IDs (data hooks); numbers are filled at build and never typed.
- **Standalone:** papers that do not need the wheel. They link in, nothing links out to them for the argument.
- **Old papers:** retired once the new set is accepted. Their content and findings feed the ledger, nothing more. Zenodo copies are replaced later.

## 2. Hub outline (proposed)
| # | Section | Job | Data hooks |
|---|---|---|---|
| H0 | One-page summary | Problem, the tax, the three results, where to go next | O1, O2, O4a |
| H1 | The problem | What is wrong now and who bears it; why existing taxes do not fix it | TBD in ledger (see section 5) |
| H2 | The tax in one page | The mechanism, plain words, one worked example | none |
| H3 | What it does | Three headline results as P10, mean, P90 for the named schedules | O1, O2, O3, O4a, O4b |
| H4 | Why it is fair | Short moral case, links to FAIR | none |
| H5 | How it could be wrong | The strongest objections and what would falsify the tax | O7, OS1, O8 |
| H6 | Where to go next | Reader routing block (section 3) | none |
| H7 | Data and method | Links to the data layer and the model | all |

## 3. Reader routing block (in H6)
| Reader | Start at |
|---|---|
| Economist | MECH, VAL, FISC, then the data layer |
| Tax lawyer or administrator | MECH, VAL, GOV |
| Policymaker or adviser | FISC, FUND, POL, FIRST, WIDER |
| Business owner or accountant | CORP, ATTR, VAL |
| Philosopher or sceptic | FAIR, LIT, FALS |
| Researcher wanting the numbers | the data layer, then FISC |

## 4. Spoke map (ledger confirms; shortcodes per `shortcodes.md`)
Source = old paper, by number. "Fed by" follows `ledger.md` section 7 and `ledger-sections.md` (brief 025w); v3 outputs follow the `element:` lists in `outputs.yml`.
| Page | Question it answers | Fed by (old papers) | v3 outputs | Depends on model numbers? |
|---|---|---|---|---|
| FAIR | Is it fair? | 2 | none | no |
| LIT | What exists, what is missing? | 3a, 3b | none | no |
| MECH | What exactly is taxed and when? | 1 (mechanism), 4, 13 | none | no |
| VAL | How is wealth measured? | 5, 5a, 5b | M-valuation hooks, TBD | partly |
| DECL | What do declarations do to incentives? | 5, 5a, 5b (VAL 7, VAL.A, VAL.B) | O7, OD1 | partly |
| FISC | What rate, what threshold, how much? | 8, 8a, 9, 9a, 11 | O1, O1a to O1d, OP1, OP4, OP5, OP3 | yes |
| PAY | Who pays? | 10 (RATES 2), 11 (WP 8.2), 21 (payslip), 14 | O2, O2b, O2c, O3 | yes |
| BEHAV | What do they do? | 10, 10a, 11 (WP 7.3, 8.3, 8.7), CLOSE objections | O5, O6, O8 | yes |
| WELF | How does it compare on welfare? | 19, 19a | OW1, OW3 | yes |
| FUND | Where does the money go? | 21, 11, parts of 8 | O1c, O1d, O4a, O4b | yes |
| CORP | How are firms treated? | 6, 6a | O1b | partly |
| ATTR | Who holds wealth held through entities? | 6a (ENT, section E) | none | no |
| GOV | Who runs it, on what law? | 7, 7a, 7b, 4 | none | no |
| POL | Can it pass, how is it staged? | 12, 12a, 15, 16, 13 | OP3, OP5 | partly |
| FIRST | What are the direct effects? | 21 (LDW 3.1, 3.2, 5) | O4a, O4b | partly |
| WIDER | What are the wider effects? | 14 (ENV), 21 | OS1 | partly |
| UNCER | What is not yet known? | 1, 5, 6, 7, 8, 9, 10, 11, 12, 14, 19, 21 (open questions, gaps, epistemic status) | OB1, O1b, O1d | yes |
| LIMIT | What can the design not do? | 1, 2, 5, 6, 7, 7a, 8, 10, 10a, 12, 12a, 14 (structural limits, named compromises) | none | no |
| FALS | What would show it wrong? | 22, 9 (SWEEPS 7.5), 12 (falsifiability objections) | CK1; O1, O2, O4a, O5, O6, OP6, OW1 if the element amendment in `ledger.md` section 9.3 is accepted | yes |
Standalone (decided): ADD (18 Addendums), INST (20 Institutional Selection), SCOPE (17 Scope Boundary, a meta paper outside the wheel). FAL folds into FALS (decided). WFR (19, 19a) and LDW (21) concern people, so they feed pages (WELF, PAY, FIRST, WIDER, FUND), not standalone papers. Pages over 6,000 kept words and their proposed splits: `ledger.md` section 9.2.

## 5. Decisions (author, 2026-11-16)
1. Spoke list and question-per-spoke shape: accepted. The ledger may still propose merges or splits.
2. FAL folds into S12 (now FALS).
3. The hub's problem section needs outputs. Add them: stage B also checks every spoke for outputs it needs that `outputs.yml` lacks, and lists them as proposed additions (with the problem section H1 first).
4. SCOPE stays outside the wheel. WFR and LDW go into spokes.
5. Spoke length 2,000 to 4,000 words: accepted provisionally. The author's experience is that it feels alarmingly short, so the ledger reports, per spoke, the words of material it keeps; if a spoke exceeds budget the budget is revisited then (split the spoke or raise the cap), not squeezed.

## 6. Not decided here
Site IDs and URLs (stage D), spoke template wording (stage C), the order of rewriting (stage E).

## 7. Changes after stage B (author, 2026-11-17; rewritten to shortcodes, brief 025w)
- Cap raised to 6,000 words per page (author confirmed 6,000, 2026-11-17). Overflow rule: a page that holds more than the cap gets its own shortcode, reached from its parent page. The `-A` suffix retires.
- **VAL** routes (VAL 1 to 6, 9 to 12) with **DECL** declaration incentives (VAL 7, VAL.A findings, VAL.B examples).
- **PAY** who pays (RATES 2, WP 8.2, payslip), **BEHAV** what they do (BEHAV, BEHAV.A, CLOSE objections) and **WELF** welfare comparison (WFR, with the new welfare outputs).
- **ATTR** entity attribution (ENT, CORP.A section E): its own page.
- S11 becomes FIRST and WIDER; S12 becomes UNCER, LIMIT and FALS (`shortcodes.md`). The 12 planning spokes plus 4 appendices are now 19 pages.
- Corrections to the "fed by" column are in `ledger.md` section 7 and apply; the row reassignment is in `ledger.md` section 9.
- H1 problem outputs OH1a to OH1c and data facts D-H1a to D-H1c accepted for now (OH1a later dropped; see `ledger.md` section 6.1).
