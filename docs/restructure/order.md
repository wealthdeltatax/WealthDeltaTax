# Rewrite order and the data gate (013g stage E, brief 026g stage B)

Status: draft for the author. Design only: no spoke or hub prose is written (the two test paragraphs of the appendix are tests, as `template.md` section 8 is). Stage A, `site.md`, is approved with its eight answers; this file places the build items of its section 8 on the gate, then orders the writing. The build briefs B1 to B16 and the writing briefs of section 6 are written only after the author approves this file.

Sources: [map](map.md), [ledger](ledger.md) and [ledger-sections](ledger-sections.md), [shortcodes](shortcodes.md), [ids-map](ids-map.md), [template](template.md), [site](site.md) with its five siblings, `docs/model-v3/outputs.yml` (version `stage-A5-falsifiability-elements-2026-11-17`), `inputs.md` (269 rows), `metrics.md`, `drivers.md`, `docs/model-v3/stock-floor-hypothesis.md`.

## 1. The units

26 units are written, plus two hand-written data pages that travel with the hub.

| Group | Units | Count |
|---|---|---:|
| Hub | `source/hub.md`, sections H0 to H7 | 1 |
| Spokes in the menu | FAIR, LIT, MECH, VAL, FISC, PAY, FUND, CORP, GOV, POL, FIRST, WIDER, UNCER, LIMIT, FALS | 15 |
| Parent-reached spokes | DECL, BEHAV, WELF, ATTR | 4 |
| Parent-reached from the splits (site Q4) | ADOPT, PILOT (from POL), HYPO (from FALS) | 3 |
| Standalone papers | ADD, INST, SCOPE | 3 |
| Total | | 26 |
| Data pages written by hand (with the hub) | DL4 method (`/data/method.html`), DL6 UK data pack (`/data/uk-pack.html`) | 2 |

## 2. Order

**How the positions were fixed.** In turn: (1) a claim is owned by one page and stated once there (ledger 9.1 names two overlaps); an owning page is written before the pages that cite it. (2) A page needs the outputs it lists in `element:`; the data gate (section 4) is one gate for all of them. (3) A page cited by many comes early. (4) The critical pages (UNCER, LIMIT, FALS, HYPO) come after the claims they criticise exist. (5) The hub comes last because it summarises and routes; a hub outline (not prose) is allowed before the gate. (6) Reader value breaks ties: the first stop of each of the six reader routes (`map.md` section 3) goes early.

A wave is a set of pages that can be written at the same time. A later wave starts when the pages it cites are at `author-review`, so their Short answers are fixed; cross-references to a page not yet written are allowed (checker XR7 reports them as unverified) and are resolved in the final cross-link pass (section 6).

| Pos | Wave | Page | Why here | Cites (for substance) | Cited by |
|---:|---|---|---|---|---|
| 1 | W1 | MECH | The canonical mechanism; `shortcodes.md` section 4 says every other page refers back to it. Needs one output (OB1). First stop for the economist and tax-lawyer routes | none | all |
| 2 | W1 | VAL | How wealth is measured; owns the routes and the valuation understatement. Cited for the measurement base. First stop on three routes | MECH | DECL, CORP, ATTR, GOV, BEHAV |
| 3 | W1 | FISC | Carries the headline results (17 of 37 outputs list it) and the sweeps; H3 mirrors it. Fixing its wording first stops ripples | MECH, VAL | PAY, FUND, CORP, BEHAV, POL, WELF, FALS |
| 4 | W1 | GOV | The legal and institutional base; no outputs; the lawyer and policymaker routes start here | MECH, VAL | FUND, CORP, POL, ADOPT, PILOT |
| 5 | W2 | PAY | The reader's first question ("who pays"); 10 outputs, the burden and the non-payer saving. Owns the payslip (author, 2026-11-17) | MECH, FISC | WELF, FIRST, FALS |
| 6 | W2 | FUND | Where the money goes; the reserve and retirement paths | MECH, FISC, GOV | WIDER, POL |
| 7 | W2 | CORP | Firms and the levy; owns O1b with FISC | MECH, VAL, FISC | ATTR |
| 8 | W2 | DECL | Declaration incentives; reached from VAL; owns O7 and OD1 | MECH, VAL | none |
| 9 | W2 | BEHAV | Responses (avoidance, migration); reached from PAY; owns OM1 | MECH, VAL, FISC | WELF, WIDER |
| 10 | W2 | FAIR | The normative case; no outputs; H4 links to it; philosopher route entry | MECH | LIMIT, hub |
| 11 | W2 | LIT | Prior work; no outputs; philosopher and economist routes | MECH | none |
| 12 | W3 | ATTR | Entity attribution; reached from CORP; after CORP fixes the levy treatment | CORP, VAL | none |
| 13 | W3 | WELF | Welfare comparison; reached from PAY; OW1 to OW3 | PAY, FISC, BEHAV | FALS, HYPO |
| 14 | W3 | FIRST | Direct effects; short (1,010 kept words); after PAY owns the payslip | PAY, FUND | WIDER, HYPO |
| 15 | W3 | WIDER | Longer transmission chains; OS1 | FUND, FIRST, BEHAV | HYPO |
| 16 | W3 | POL | Can it pass and how it is staged; OP1, OP3, OP5, OR1 | GOV, FISC, FUND | ADOPT, PILOT, FALS |
| 17 | W3 | ADOPT | First mover and modular adoption; reached from POL | POL, GOV | none |
| 18 | W3 | PILOT | Phase One; reached from POL | POL, GOV, FISC | none |
| 19 | W4 | UNCER | What is not known; cites every other page's gaps; O1b, O1d, OB1 | all spokes | FALS, hub |
| 20 | W4 | LIMIT | What the design cannot do; no outputs; after the pages that state what it does | GOV, FAIR, MECH | hub |
| 21 | W4 | FALS | What would show it wrong; owns CK1 and, until the split is taken, the FAL claims | FISC, PAY, WELF, UNCER, LIMIT | hub, HYPO |
| 22 | W4 | HYPO | Hypotheses H2 to H5; reached from FALS | FALS, WIDER, FIRST | none |
| 23 | W5 | Hub (H0 to H7), DL4, DL6 | Summarises and routes: H0 and H3 hook the results, H5 points at UNCER, LIMIT, FALS, H6 routes to all 22 spokes, H1 takes the problem outputs (OH1b, OH1b2, OH1c, DH1a to DH1c), DL4 is the target of H7 | all | none |
| 24 | W6 | ADD | Supplementary; links in, nothing links out to it for the argument | the settled spokes | none |
| 25 | W6 | INST | Institutional selection (14,264 words kept as standalone); largest; own session | GOV, POL | none |
| 26 | W6 | SCOPE | The meta-paper on scope; written last so it describes the series as accepted | all | none |

The "Cites" and "Cited by" columns are my reading of the "fed by" columns (`map.md` section 4, `ledger.md` section 7) and the output `element:` lists; the author may reorder. W1 and W2 together are 11 pages: with fewer agents than pages the waves run in the order of the position column.

## 3. What each page needs

Outputs are the `element:` lists of `outputs.yml`. Input families are the register groups the page's hooks will draw on (D1 returns, D4 wealth, D5 behaviour, D6 retired-tax incidence, D7 to D11 the tier 2 inputs and capitalisation, M5, M6, M8 comparators, W wealth tail and dynamics, T tax data, H household deciles). The page's front matter `inputs:` is the exact list, fixed at drafting. "Frozen" means the part of `outputs.json` the page reads. Old papers are those whose kept rows make up the page (`ledger-sections.md`; words in brackets are kept words; UNCER and LIMIT count the merged pool by the author's decision 8(b)). The old numbering is `ledger-sections.md`'s.

| Pos | Page | Outputs (element) | Input families | Data to freeze | Old papers to read |
|---:|---|---|---|---|---|
| 1 | MECH | OB1 | W6 (payer counts) | OB1 by threshold | 11 Position Closure (4,826); 1 Whitepaper (2,146) |
| 2 | VAL | none | D5 (valuation understatement, routes) | no outputs | 5 Valuing wealth (6,784) |
| 3 | FISC | O1, O1a, O1b, O1c, O1d, O2, O3, O5, O6, O7, O8, OP1, OP4, OB1, OR1, OF1, OT1 | D1, D4, D5, D7, D8, D11, M5, M6, M8, T3, W6 | all 17, three schedules, three horizons | 8 Rates and Revenue (4,730); 9 Parameter Sweeps (1,860); 1 Whitepaper (1,574) |
| 4 | GOV | none | none | no outputs | 7 Constitutional governance (7,405); 4 UK jurisdiction (1,996); 1 Whitepaper (718) |
| 5 | PAY | O2, O3, O4a, O4b, O5, O6, O2b, O2c, DH1c, OL1 | D4, D6, D9, D11, M5, M6, H1 to H3, T3 | the by-decile and by-band cells of O2, O2b, O2c, O4a, O4b | 8 Rates and Revenue (1,925); 21 Labour dividend welfare (1,618); 1 Whitepaper (669) |
| 6 | FUND | O1c, O1d, O4a, O4b, OP1, OP3, OP4, OP5, OP6, OL1 | D1, D6, D8, T3 | the path outputs and the P6 series | 8 Rates and Revenue (2,214); 11 Position Closure (959); 1 Whitepaper (930); 21 (765) |
| 7 | CORP | O1b | D7 | O1b | 6 Corporate architecture (5,464); 6a (3,746) |
| 8 | DECL | O7, OD1 | D5, W9 | the alpha grid | 5b Worked examples (4,798); 5 Valuing wealth (4,528); 5a (1,374) |
| 9 | BEHAV | OM1 | D5, D4 | OM1 lines | 10 Behavioural robustness (4,317); 10a (1,199); 1 Whitepaper (957) |
| 10 | FAIR | none | none | no outputs | 2 Moral foundations (4,254); 12a Political architecture appendix (1,693) |
| 11 | LIT | none | none | no outputs | 3b Intellectual background (3,656); 3a Research gaps (3,302); 1 Whitepaper (1,622) |
| 12 | ATTR | none | none | no outputs | 6a Corporate architecture appendix (6,498) |
| 13 | WELF | OW1, OW2, OW3 | H5 to H7 (risk aversion, returns, spending), W3 | OW1 by system and band; OW2; OW3 | 19 Taxpayer welfare (9,671) |
| 14 | FIRST | O4a, O4b | H1 to H3 | the O4a and O4b decile cells | 21 Labour dividend welfare (1,010: sections 3.1, 3.2, 5) |
| 15 | WIDER | OS1 | D10 | OS1 | 14 Environmental effects (5,082); 21 (972) |
| 16 | POL | O1, OP1, OP3, OP5, OR1 | D1, D8 | path outputs | 12 Political architecture (5,489); 15 First mover (2,985); 13 Phase One (2,817); 16 Modular adoption (1,301) |
| 17 | ADOPT | none yet (OP3, OP5, OR1 stay in POL; assign at the split) | none yet | to be set at the split | 15 First mover (2,985); 16 Modular adoption (1,301) |
| 18 | PILOT | none yet | none yet | to be set at the split | 13 Phase One (2,817) |
| 19 | UNCER | O1b, O1d, OB1 | D5, D7, T3, W6 | the three outputs | 19 (1,350); 9 Parameter sweeps (1,211); 21 (826); 14 (604); 1 Whitepaper (520); and others, all merged rows |
| 20 | LIMIT | none | none | no outputs | 7a Governance intellectual appendix (1,688); 2 Moral foundations (855); 6 (694); 5 (513); 12 (511); and others, mostly merged rows |
| 21 | FALS | O1, O2, O4a, O5, O6, OP6, OW1, CK1 (after the HYPO split: O2, O5, O6, CK1) | D1, D4, M5, M6, W3 | the listed outputs and the CK1 check | 22 Falsification hypotheses (11,360); 9 Parameter sweeps (775) |
| 22 | HYPO | O1, O4a, OP6, OW1 (moved from FALS with FAL 4 to 7, see the finding below) | D1, H1 to H3 | the four outputs | 22 Falsification hypotheses, sections 4 to 7 (6,096) |
| 23 | Hub | H0: O1, O2, O4a; H1: OH1b, OH1b2, OH1c, DH1a, DH1b, DH1c; H3: O1, O1a, O1b, O2, O3, O4a, O4b; H5: O7, O8, OS1, OD1; H2, H4, H6, H7: none | all headline families, T1 to T7, W5, W7 | 14 outputs and 3 data facts | 1 Whitepaper (141 kept for H1, 152 for H2); the rest is new writing |
| 24 | ADD | none | none | no outputs | 18 Addendums (6,789 standalone words) |
| 25 | INST | none | none | no outputs | 20 Institutional selection (14,264 standalone words) |
| 26 | SCOPE | none | none | no outputs | 17 Scope boundary (2,537 standalone words) |

**Finding: the HYPO split moves four element entries.** `ledger.md` 9.2 says CK1 stays in FALS and does not mention the others. The author gave O1, O4a, OP6 and OW1 to FALS because FAL 4.1 to 4.4 and FAL 6 use them (ledger 9.3). Those sections are in the rows the split moves to HYPO. If the split stands, the guru changes the `element:` lists of O1, O4a, OP6 and OW1 to name HYPO (and FALS only where FAL 3 or the sweeps still cite them: O2, O5, O6 stay in FALS). The same applies to POL: if the Phase One rows cite OP5 or OP1, the split puts PILOT in their `element:`. R1 forbids a hook to an output the page does not list, so this is a gate item (G4).

**Also found.** Old paper 4 (UK jurisdiction) feeds GOV (1,996) and the data layer (DL6, 2,775 words), not only GOV. `site.md` section 8.3 leaves DL4 and DL6 prose to this file: they are written with the hub (position 23), by the same brief group (section 6).

## 4. The gate

**Rule (author, 2026-11-17).** No spoke prose until the data is finalised. Spoke prose is any spoke or hub text, drafts included. Planning, outlines, page cards and tests of one paragraph are allowed. Glossary seeding by copying existing definitions is allowed (site Q7).

The gate is five checks. Each can be run by a command; section 4.3 names the tool that runs them all. A page opens when the checks it needs are true.

### 4.1 The checks

| # | Check | How it is tested |
|---|---|---|
| G1 | **Model v3 complete and accepted.** The design stages are closed, the model is built and its acceptance run passes | `docs/model-v3/architecture.md` and `acceptance.md` exist; `docs/archive/briefs/011g-model-v3-design.md` exists (the brief is retired only when its stages are done); the command that `acceptance.md` names as the acceptance run exits 0. If `acceptance.md` names no single command, 011g stage D is incomplete: return it |
| G2 | **Data final.** One run, marked final by the author | `model_v3/OUTPUTS/outputs.json` exists; `run.status == "final"`; `run.fixture` is false; `run.manifest_version` equals `version` in `outputs.yml`; `run.manifest_sha256` equals the hash of `outputs.yml`; `run.inputs_sha256` equals the hash of `registry/inputs.json`; `python pipeline/validate_outputs.py` exits 0 with zero errors in final mode (V1 to V12, with V7, V9 and V11 as errors; the flag names are fixed by B2). A change to the manifest or the register after the run makes G2 false again |
| G3 | **Input judgement rows decided.** Every register row flagged `(J)` has a recorded decision | the set of rows whose text contains `(J)` in `inputs.md` (70 of 269 today) equals the set of ids in `docs/model-v3/judgement-decisions.md`; each line there reads `accepted`, `fixed at <value>` or `replaced by <row id>` with a date. The guru writes the file from the author's answers |
| G4 | **The page's own data is complete.** Per page | for the page P: every output id O whose `element:` lists P is in `outputs.json` with every cell, none `null`; every `{{i:}}` id in P's front matter is in `registry/inputs.json`; P's `element:` entries and its front matter `outputs:` agree (R1 both ways) |
| G5 | **Tooling works.** The resolver, Data block, figures and checker | B2, B3, B4, B5, B6 and B15 of `site.md` are merged; `pytest tests/data tests/hooks tests/data_block tests/figures tests/spokes` passes; a fixture spoke builds under `WDT_MODE=release` with zero errors and `_build/hooks-report.json` shows zero unresolved hooks |

### 4.2 What each page needs

The default is the author's rule: **every page waits for G1 to G5.** The table gives the minimum each page needs, so the author can release pages early if they choose (Q3).

| Pages | Cites outputs? | Needs |
|---|---|---|
| MECH, FISC, PAY, FUND, CORP, DECL, BEHAV, WELF, FIRST, WIDER, POL, UNCER, FALS, HYPO, the hub | yes | G1, G2, G3, G4, G5 |
| VAL | no; cites register rows (D5) | G3, G5 |
| FAIR, LIT, GOV, ATTR, LIMIT, ADOPT and PILOT (until the split gives them outputs), ADD, INST, SCOPE | no | G5; G3 if the front matter lists `inputs:` |

A page whose front matter later lists an output falls under the first row. If G2 turns false after a page is accepted (the register or manifest changes), the checker's release build fails for every page that cites a changed value and those pages return to `author-review`.

**Early start is one decision, not a loophole.** A page in the last two rows can begin at a **design freeze** (G1 design part: `architecture.md`, `acceptance.md` and 011g retired) plus G5, before the model is built. The risk is rework: the mechanism of these pages could still change. The stock-wealth floor hypothesis (section 7) would touch VAL, GOV, FAIR, ATTR and LIMIT among these pages, so the author decides it first (Q3).

### 4.3 The gate tool

The checks are one script, so "the gate is open" is a command and not an opinion: `python pipeline/check_gate.py --page <ID>` prints G1 to G5 for a page with pass or fail and a reason and exits 0 only if the page's needs are met; `--all` prints the table of section 4.2 for the 26 units. It is a new build item that `site.md` does not list (B17, section 6). Until B17 exists, the checks are run by hand from the table above; the change report of a writing brief records which were run.

## 5. The optional splits against the cap

Counted prose is the Short answer (80 to 150 words), the Objection block (150 to 400) and the Evidence; the cap is 6,000 for the whole. A page's Evidence therefore has between 5,450 and 5,770 words, and the Objection block is mostly new writing. I use 5,500 as the Evidence ceiling.

**What was measured.** The only measurement is the compression ratio of test paragraphs (old words over new words). Three exist: the whitepaper §3.5 test of `template.md` section 8 (238 to 125, ratio 1.90), and two made for this file, GOV 6.4 (462 to 222, ratio 2.08) and CORP 6.2 (384 to 220, ratio 1.75). Word-weighted over the three: 1,084 to 567, ratio 1.91. All three are prose with no model numbers, from papers with typical padding. This is a measurement of three paragraphs and not of any page: no page may be drafted before the gate.

**Estimate.** Compressed Evidence = kept words over the ratio. Pages with model words Y or P will shrink more, because hooks replace typed numbers and their narration; that is not quantified. Kept words from `ledger.md` section 2; UNCER and LIMIT use the merged pool (decision 8(b)).

| Page | Kept words | Kept ÷ 6,000 | At 2.08 | At 1.91 | At 1.75 | Model words Y / P | Reading |
|---|---:|---:|---:|---:|---:|---:|---|
| DECL | 10,700 | 1.78 | 5,144 | 5,602 | 6,114 | 7,414 / 5,057 | over the 5,500 ceiling at 1.91; model-heavy, so likely to shrink. **Watch** |
| GOV | 10,668 | 1.78 | 5,129 | 5,585 | 6,096 | 0 / 970 | over at 1.91; almost no model words to shrink. **Watch; the most likely split** |
| CORP | 9,671 | 1.61 | 4,650 | 5,063 | 5,526 | 2,555 / 0 | fits at 1.91, edge at 1.75 |
| WELF | 9,671 | 1.61 | 4,650 | 5,063 | 5,526 | 8,409 / 2,524 | fits; model-heavy |
| LIT | 8,580 | 1.43 | 4,125 | 4,492 | 4,903 | 380 / 0 | fits |
| FISC | 8,164 | 1.36 | 3,925 | 4,274 | 4,665 | 14,488 / 1,478 | fits; model-heavy |
| UNCER | 6,827 | 1.14 | 3,282 | 3,574 | 3,901 | 547 / 1,368 | fits |
| MECH | 6,972 | 1.16 | 3,352 | 3,650 | 3,984 | 0 / 425 | fits |
| BEHAV | 6,797 | 1.13 | 3,268 | 3,559 | 3,884 | 863 / 3,305 | fits |
| VAL | 6,784 | 1.13 | 3,262 | 3,552 | 3,877 | 0 / 1,210 | fits |
| ATTR | 6,498 | 1.08 | 3,124 | 3,402 | 3,713 | 0 / 1,233 | fits |
| LIMIT | 6,233 | 1.04 | 2,997 | 3,263 | 3,562 | 0 / 0 | fits |
| FUND | 6,210 | 1.03 | 2,986 | 3,251 | 3,549 | 3,110 / 1,331 | fits |
| WIDER | 6,054 | 1.01 | 2,911 | 3,170 | 3,459 | 374 / 3,699 | fits |
| FAIR, PAY, FIRST | 5,947; 4,212; 1,010 | 0.99; 0.70; 0.17 | | | | | within cap before compression |

After the two default splits (taken, author 2026-11-17): POL 6,135 (3,212 at 1.91), ADOPT 4,286 and PILOT 2,817 (4,286 is first mover and modular adoption together), FALS 6,039, HYPO 6,096; all fit at every ratio above.

**Verdict.** Take no optional split now. On three paragraphs, no page exceeds the ceiling at the pooled ratio except DECL (5,602) and GOV (5,585) by about 100 words, within what the Objection block's new writing and one more test could swing. The splits stay pre-agreed so that taking one costs a registry row and no redesign: **GOV to SAFE** (GOV sections 3 to 6, 5,653 words) and **DECL to EXMP** (VAL.B worked examples, 4,798 words) first; **CORP to OWNR** and **WELF to CONC** only if their first drafts miss. The rule is a trigger, not a judgement: if the compressed Evidence of a first draft exceeds 5,400 words, the writer stops, files the split with the ledger 9.2 rows, and the guru writes the extra brief. The `element:` change that follows a split is the guru's (WELF to CONC moves OW3; FISC to SENS moves OT1; BEHAV to MIGR moves OM1). Q4 asks the author to confirm.

## 6. Writing briefs

### 6.1 How many

One brief per page, except where two pages share one source set and fit one session together. **21 writing briefs** (numbers are assigned when each is written, lane letter `w`):

| Brief | Pages | Wave | Why grouped |
|---|---|---|---|
| W1 | MECH | 1 | canonical, own session |
| W2 | VAL | 1 | |
| W3 | FISC | 1 | most outputs; the heaviest review |
| W4 | GOV | 1 | |
| W5 | PAY | 2 | |
| W6 | FUND | 2 | |
| W7 | CORP and ATTR | 2 and 3 | ATTR is 6a section E; one source paper, one session |
| W8 | DECL | 2 | |
| W9 | BEHAV | 2 | |
| W10 | FAIR | 2 | |
| W11 | LIT | 2 | |
| W12 | WELF | 3 | |
| W13 | FIRST and WIDER | 3 | FIRST is 1,010 kept words and shares the household inputs with WIDER's drivers |
| W14 | POL | 3 | |
| W15 | ADOPT and PILOT | 3 | both from the small old papers 13, 15, 16; after POL |
| W16 | UNCER and LIMIT | 4 | one source pool (the limitations and unknowns of every paper); one agent keeps the two boundaries apart |
| W17 | FALS and HYPO | 4 | one source paper (22) |
| W18 | Hub, DL4, DL6 | 5 | one agent; the author's closest review |
| W19 | ADD | 6 | |
| W20 | INST | 6 | |
| W21 | SCOPE | 6 | |

If a grouped brief does not fit one session the guru splits it at its page boundary; the page files are disjoint (`source/spokes/<ID>.md`), so a split needs no replanning.

A last brief, **W22**, the cross-link pass, runs after every page is `accepted`: it resolves XR7 across pages, checks every reader route of H6, and writes the Read-next lists. It touches `source/` pages for cross-references only.

### 6.2 What each needs as a shared input (fixed before the brief starts; no writer edits these)

- `docs/restructure/template.md`, the style guide and prose rules named there, and the spoke checker (B6) in source mode.
- A **page card** per page: the ledger rows whose target is the page (K and M, with disposition, model flag and note), its `element:` outputs, its input families, its neighbours from section 2, and the front matter skeleton (`spoke`, `question`, `depends`, `outputs`, `inputs`, `budget` 6,000, `status: draft`). Generated by a script from `ledger-sections.md`, `outputs.yml`, `inputs.md` and `shortcodes.md`, so the card cannot drift from them (B18).
- `outputs.json` (final), `inputs.json`, `registry/pages.yml`, `registry/glossary.yml`, `registry/lit-figures.yml` and `registry/figure-style.yml`, all from the B briefs.
- The text of the old papers named on the card, read by section only. The old papers retire and only guide the rewrite (author): a writer never copies a paragraph; a section kept in the ledger is restated in the page's own words and numbers become hooks.
- Accepted pages of the earlier wave, read for their Short answers, so no claim is stated twice (ledger 9.1: ENV 3 against FAL 4.2; WFR 4.3 against FAL 6).

### 6.3 What can run in parallel after the gate

All pages of a wave, and pages of the next wave once the pages they cite are at `author-review`. Briefs write only their own page file and their own progress block, so there is no shared file between writing briefs; the only shared files are `registry/pages.yml` (read-only for writers) and the data files. The author's review capacity, not the files, sets the pace: four pages in the first wave.

### 6.4 The review loop (checker, then guru, then author)

1. **Writer.** Drafts the page; runs the checker in source mode (zero E); builds under `WDT_MODE=draft`; fixes every E and either fixes or waives every W with a reason on its line; does the manual prose pass for the rules the checker leaves manual and records it in the change report; records the compressed word count against the cap (feeds section 5). When the gate is open for the page, runs the release build and `check_spokes.py --release` (zero E). Sets `status: author-review` only when both pass.
2. **Guru.** Checks, from the page card and the change report: every K row of the card is restated, moved (with the page named) or dropped with a reason; every number on the page is a hook; every claim the page owns is stated once and every claim it cites is a cross-reference; the Objection block states the strongest objection, not a weak one; the output cited supports the claim in the Short answer (read the hook's value against the sentence). The guru returns the page or passes it to the author.
3. **Author.** Reads the Short answer and the Objection block first, then the Evidence, in the rendered draft build. Sets `accepted` or returns with notes. The author reads the hub's Short answer, H0, H3 and H5 in full.
4. A page stays `author-review` until its cited pages are accepted or the author says otherwise.

### 6.5 Build items this file adds to `site.md` section 8

| Brief | Lane | Goal | Touches | Depends on |
|---|---|---|---|---|
| B17 | c | Gate checker: G1 to G5 per page and for all 26 units, with pass or fail and a reason; reads `outputs.json`, `inputs.json`, `inputs.md`, `outputs.yml`, `pages.yml`, front matter | `pipeline/check_gate.py`, `tests/gate/` | B1, B2, B3 |
| B18 | c | Page cards: one generated file per page from the ledger rows, the manifest, the register and the shortcode list | `pipeline/page_cards.py`, `docs/restructure/pages/` (generated), `tests/cards/` | A (needs no other brief; reads `pages.yml` if B1 has landed) |

Both touch files no sibling in section 8 of `site.md` touches. B17 and B18 can run now, in parallel with B1, B2, B11 and B12, because neither writes spoke prose.

## 7. The stock-wealth floor, if it were adopted

`stock-floor-hypothesis.md` is exploratory. Nothing here is designed around it. If the author later adopts it, these units and outputs would change (it would add a second base, a stock-rate and threshold lever, a contribution-envelope switch and a combined candidate in the welfare comparison). Sources: that file's sections 2, 4, 9, 11 and 13.4.

| Unit | Outputs it would touch | What changes |
|---|---|---|
| MECH, VAL, GOV, ATTR, CORP | OB1, O1b | the stock base needs the valuation routes and entity attribution; a second base is in the canonical mechanism and the legal text |
| FISC | O1, O1a (and a new stock-receipts line), O2, O3, O5, O6, OF1, OT1, OP1, OP4, OR1, OB1 | revenue and burden; the feasibility map gains a stock-rate and threshold axis; the tornado gains the new levers |
| PAY | O2, O2b, O2c, O3, O4a, O4b, OL1, DH1c | the stock charge against income and liquid assets by band; needs a liquidity-by-asset source for the top tail the register lacks |
| FUND | O1c, O1d, OP1, OP3, OP4, OP5, OP6 | reserve fill and retirement paths with the extra receipts and refund capacity |
| POL | OP3, OP5, OR1 | acceptability to asset-rich taxpayers; opportunistic change of the rate |
| BEHAV, DECL | OM1, O7, OD1 | migration and declaration response to a stock base |
| WELF | OW1, OW3 | the combined system as a new candidate in OW1; the envelope inclusion changes OW3 |
| UNCER, LIMIT, FALS, HYPO | CK1, O5 | new unknowns, limits and tests; the combined system is a new hypothesis, not covered by OW1 |
| FAIR, LIT | none | the fairness of a stock charge on illiquid wealth; the literature on stock wealth taxes |
| Hub | H0, H3, H5 | results and objections |
| Register | D4e, D4f, new rows | top-tail data above WAS and liquidity by asset |

Because 19 of the 26 units would change, the decision on whether to test it first (`stock-floor-hypothesis.md` section 10) comes before any early start of the pages named in section 4.2 (Q3).

## 8. Open items from `ledger.md` 8(e)

| Item | Finding | Proposed answer |
|---|---|---|
| WELF 4.3 has no concentration output | OH1a is dropped (no UK evidence for rank-dependent returns, `022r`). The claim in WFR 4.3 (2,697 words) is that concentration rises under heterogeneous returns, which is the dropped premise. OW3 covers the envelope only | WELF keeps the envelope part (OW3) and drops the concentration claim. The unknown (does the return rise with wealth rank, and what follows) goes to UNCER as a named gap with its evidence status; no hook, no figure |
| Comparison-tables page | A table of three systems on eleven criteria; template 6a rule 3 allows tables only in the Data block | Fold the content into WELF and H5 as prose; keep no table page. The reader-facing question headings carry over as a style input |
| Avoidance guide | All M rows; a second-person guide to the same routes | Fold into BEHAV, DECL, VAL and MECH; keep none of its form. If the author wants a reader page in that voice, build it from the objection blocks after the pages are accepted |

All three need the author's yes (Q5).

## 9. Questions for the author

Each has a proposed answer; the writing briefs assume the proposals until the author decides.

**Q1. The order.** *Proposed:* the 26 positions of section 2: W1 MECH, VAL, FISC, GOV; W2 PAY, FUND, CORP, DECL, BEHAV, FAIR, LIT; W3 ATTR, WELF, FIRST, WIDER, POL, ADOPT, PILOT; W4 UNCER, LIMIT, FALS, HYPO; W5 the hub, DL4, DL6; W6 ADD, INST, SCOPE. Say if you want the hub earlier (for example the hub outline reviewed before W2) or a page moved.

**Q2. The gate.** *Proposed:* G1 to G5 of section 4.1 as written, with `judgement-decisions.md` as the record for G3 and `check_gate.py` (B17) as the command. Confirm, or name a check to add or drop.

**Q3. Early start.** Section 4.2 shows six pages cite no output (VAL needs the register only; FAIR, LIT, GOV, ATTR, LIMIT need nothing). *Proposed:* no early start; the gate stays whole for every page, because your rule says so, the stock-floor decision could still change five of those six pages (all but LIT), and the gain is small while G5 is not met. If the model build is long and you want writers busy, release LIT at G5 alone (the page the stock floor touches least), and the rest at a design freeze plus your decision on the stock floor.

**Q4. The optional splits.** *Proposed:* take none now; keep the trigger of section 5 (compressed Evidence over 5,400 words in a first draft) and the order GOV to SAFE, DECL to EXMP, then CORP to OWNR, WELF to CONC. Say if you want GOV to SAFE taken now: it is the likeliest and needs only a registry row and a routing entry (parent-reached from GOV, site Q4).

**Q5. The three items of section 8** (WELF concentration to UNCER, comparison-tables page folded into prose, avoidance guide folded). *Proposed:* all three as stated.

**Q6. Writing briefs.** *Proposed:* the 21 of section 6.1 plus the cross-link pass W22 and the build items B17 and B18. Say if you want one brief per page everywhere (26) or fewer groups.

**Q7. Hub cap.** The hub target is 5,000 to 7,000 words (`map.md` section 1) and its cap is 6,000 (`site.md` Q5, template section 3). *Proposed:* cap 6,000, target 5,000 to 6,000; the hub stays under the cap by routing, not by length.

**Q8. Where the hand-written data pages live.** DL4 (method) and DL6 (UK data pack) are hand-written and nothing fixes their source. *Proposed:* `source/data/method.md` and `source/data/uk-pack.md`, with `type: data` rows in `pages.yml`, checked by the spoke checker's hub mode (no four-part shape).

**Q9. The HYPO and PILOT elements.** The HYPO split moves O1, O4a, OP6 and OW1 (section 3); PILOT and ADOPT have no outputs assigned. *Proposed:* the guru edits `outputs.yml` `element:` when the splits are filed (they are already taken), as follows: HYPO lists O1, O4a, OP6, OW1; FALS keeps O2, O5, O6, CK1; PILOT and ADOPT stay at none until their first draft shows a need, and then the guru adds them.

**Q10. Judgement rows.** The register's own prose counts 84 judgement rows (38 in B1 to B4 plus 46 in the added parts) and 70 rows carry the `(J)` flag. *Proposed:* the gate uses the flag, and the guru reconciles the two counts before G3 is run. The decision for each row is yours; `judgement-decisions.md` lists them.

## 10. Guru follow-through (after the author approves; not done here)

- Write B17 and B18 and the 22 writing briefs (numbers from the next unused); assign `element:` for HYPO, PILOT and ADOPT (Q9); apply the stock-floor decision if any.
- Write `docs/model-v3/judgement-decisions.md` from the author's answers; reconcile the 84 and 70 counts (Q10).
- `site.md` section 8: add B17 and B18 to the table and a pointer to this file; `site.md` and the siblings are not rewritten.
- STATUS.md, `docs/lane-plan.html`, `docs/decisions.md` and the 013g status line: at the end of 026g only.

## 11. Checks run

Run for stage B, results in the brief's progress block.
- Coverage: a script (kept in the brief's change report) confirmed that all 19 shortcodes of `shortcodes.md`, the three splits (ADOPT, PILOT, HYPO), the hub and ADD, INST and SCOPE each have a row in sections 2 and 3, and that every `element:` value of `outputs.yml` (17 distinct, including H0, H1, H3, H5) resolves to a page or hub section of this file.
- The gate checks G1 to G5 are written as commands or file tests (section 4.1); G1's acceptance command depends on 011g stage D naming it, which is stated as a defect to return if it does not.
- Measured: three test paragraphs of one paper each (ratios 1.90, 2.08, 1.75). Not measured: any whole page (the gate forbids drafting) and the shrinkage of model words.
- Not run: any build, any model, any edit of `outputs.yml`, `metrics.md`, `inputs.md`, `template.md` or a sibling file. `git diff --stat` shows only this file and the brief.

## Appendix A. Test paragraphs for section 5

Test only. Not spoke text and not to be reused as written. No model numbers, so no hooks. Each draft keeps the mechanism and drops the second-order narration; each cross-reference and defined term of the original was kept or left for another paragraph.

**GOV, 6.4 The Administrator.** Source: `source/7_Constitutional_Governance.md`, section 6.4 (462 words). Draft: 222 words, ratio 2.08.

> The Administrator transmits and decides nothing. It holds no vote, no seat and no discretion, because whoever controls what is sent, how it is framed or when it appears has acquired a power the design never assigned. It publishes exactly what the system generates, on a fixed cycle, in an externally set format, and it publishes a contested result immediately. It cannot embargo an output or put one chamber's ahead of another's. Any change to the format is logged as a dated event.
>
> Its data role follows from the same rule. It issues credentials and confirms consistency; it does not hold truth. A conventional tax authority treats declarations as adversarial claims and holds everything it can. The delta base needs less: the Administrator confirms that the change between two declared values is arithmetically correct, not that either value is right. A wrong basis today produces a wrong delta next year, and the cost falls on the taxpayer. The Valuation Bodies catch extreme Route D outliers and the auction handles the rest. Holding the minimum necessary information is therefore a compliance argument. The privacy benefit is real and follows from it, not the reverse.
>
> The risk is incompetent or captured transmission. Either shows in the permanent log as something missing, so nobody has to detect intent. The full specification sits outside this page.

**CORP, 6.2 Mechanism.** Source: `source/6_Corporate_Architecture.md`, section 6.2 (384 words). Draft: 220 words, ratio 1.75.

> The facility turns the levy into a collateralised loan. On the assessment date a company that elects it notifies the Administrator and the SWF Custodian together and transfers shares to the SWF at the volume-weighted average price over a pre-assessment window. The Custodian lends the provisional levy against those shares.
>
> The company repays at its own pace above a minimum annual schedule. The Governing Council sets the interest rate and publishes it in advance, and it applies to every user in the cycle. Partial repayment releases shares pro rata. The company can repurchase shares at market price at any time without penalty; if the price has fallen, it pays the lower value and the SWF absorbs the difference against the collateral.
>
> A margin call applies if collateral falls below a set share of the loan. The company then adds shares, repays in cash or lets the Custodian sell enough to restore the margin. If the loan is unpaid at the maximum holding period, the SWF sells the remaining shares, settles the loan first and returns any surplus. The period must cover the realistic cash generation of the companies the facility serves and stay short enough that the SWF holds no permanent stake in a listed company. The Governing Council also sets the window, the repayment minimum and the margin threshold.

What the tests show: the GOV test drops the privacy-versus-compliance restatement and the self-correction chain to one sentence each; the CORP test is a mechanism and compresses less because every clause is a rule. A rule-dense page will compress near 1.75, a rationale-dense page near 2.1.
