# Content ledger: summary (brief 013g, stage B)

> **Ids (author, 2026-11-17).** Spoke shortcodes (`docs/restructure/shortcodes.md`) are the page ids, URLs, front-matter `spoke:` values and figure and table ids. Where this file still writes `S1` to `S12`, read it through `docs/restructure/ids-map.md`; the S numbers are planning labels only.

Status: stage B drafted, waiting for the author; reassigned to the shortcodes by brief 025w (2026-11-17), see section 9. One row per section of all 33 old papers is in `ledger-sections.md` (980 rows, no section without a disposition; the four reader-facing site pages have their own rows at the end of that file). This file holds the totals, the budget finding, the demanded outputs checked against `outputs.yml`, the proposed additions and the decisions for the author. Words are body words counted per section, about 2% under `wc`.

## 1. What the 33 papers hold
| Disposition | Rows | Words | Share |
|---|---:|---:|---:|
| K keep to a page or hub section | 398 | 133,808 | 39% |
| M merge (overlaps a kept section) | 207 | 59,712 | 17% |
| SA standalone paper | 32 | 23,590 | 7% |
| DL move to the data layer | 69 | 24,253 | 7% |
| AR archive (design history, v1 results, statute detail) | 199 | 86,031 | 25% |
| D drop as redundant | 75 | 15,101 | 4% |
| Total | 980 | 342,495 | |

Read this as: a quarter of the old words (AR 86,031) is v1 result tables, operational statute detail and design history that no reader needs; 133,808 words are kept for the 19 pages and the hub; 59,712 overlap them and are the pool for compression. Brief 025w moved ENT (6,498 words) from SA to K, because the author made it the page ATTR (decision 2, section 8), so K rose from 127,310 and SA fell from 30,088.

## 2. Words kept per page against the 6,000 cap
"Kept" is the old words of K rows. "Merged" is the old words of M rows, which overlap kept sections and are not additional. "Model words" is kept and merged words whose claims need model numbers (Y) or partly (P); those get replaced by data hooks, so they shrink most. Pages are the shortcodes of `shortcodes.md`; the planning ids S1 to S12 are retired (`ids-map.md`). Words from the four reader-facing site pages are counted apart, in section 9.4.

| Page | Question | Kept | Merged | Kept ÷ 6,000 | Model words Y / P |
|---|---|---:|---:|---:|---:|
| FAIR | Is it fair? | 5,947 | 1,876 | 0.99 | 0 / 714 |
| LIT | What exists, what is missing? | 8,580 | 3,869 | 1.43 | 380 / 0 |
| MECH | What exactly is taxed and when? | 6,972 | 1,587 | 1.16 | 0 / 425 |
| VAL | How is wealth measured? | 6,784 | 3,719 | 1.13 | 0 / 1,210 |
| DECL | What do declarations do to incentives? | 10,700 | 2,884 | 1.78 | 7,414 / 5,057 |
| FISC | What rate, what threshold, how much? | 8,164 | 8,445 | 1.36 | 14,488 / 1,478 |
| PAY | Who pays? | 4,212 | 1,108 | 0.70 | 4,212 / 1,108 |
| BEHAV | What do taxpayers do? | 6,797 | 2,175 | 1.13 | 863 / 3,305 |
| WELF | How does it compare on welfare? | 9,671 | 3,003 | 1.61 | 8,409 / 2,524 |
| FUND | Where does the money go? | 6,210 | 3,021 | 1.03 | 3,110 / 1,331 |
| CORP | How are firms treated? | 9,671 | 3,942 | 1.61 | 2,555 / 0 |
| ATTR | Who owns what, through which entities? | 6,498 | 0 | 1.08 | 0 / 1,233 |
| GOV | Who runs it, on what law? | 10,668 | 4,387 | 1.78 | 0 / 970 |
| POL | Can it pass, how is it staged? | 13,238 | 3,755 | 2.21 | 546 / 3,731 |
| FIRST | What are the direct effects? | 1,010 | 0 | 0.17 | 0 / 1,010 |
| WIDER | What are the wider effects? | 6,054 | 1,932 | 1.01 | 374 / 3,699 |
| UNCER | What do we not know? | 0 | 6,827 | 0.00 | 547 / 1,368 |
| LIMIT | What can the design not do? | 204 | 6,233 | 0.03 | 0 / 0 |
| FALS | What would show it wrong? | 12,135 | 649 | 2.02 | 1,018 / 3,789 |
| H1 The problem (hub) | | 141 | 300 | | 0 / 141 |
| H2 The tax in one page (hub) | | 152 | 0 | | 0 / 0 |

**Finding.** 133,515 kept words sit on 19 pages whose caps add to 114,000, a ratio of 1.17. Five pages are within the cap (FAIR, PAY, FIRST, UNCER, LIMIT); fourteen are over it on kept words alone, six of them by less than 20% (WIDER 1.01, FUND 1.04, ATTR 1.08, BEHAV 1.13, VAL 1.13, MECH 1.16). The template's first compression measurement is a ratio of 1.9 (template section 3), so a page whose kept words are at or below 1.9 times the cap should fit after a laconic rewrite. Two pages are above that line: **POL 2.21** and **FALS 2.02**. The author expected overshoot ("alarmingly short"); the budget is revisited here, not squeezed. The splits that stage B decided (S4 into VAL and DECL, S6 into PAY, BEHAV and WELF, S8-A as ATTR) and the S11 and S12 divisions are in these figures; sections 9.1 and 9.2 say how the rows were placed and what would move if a page is split again.

**Two pages have no kept rows of their own.** UNCER has 0 kept words and LIMIT 204, because every old limitations and unknowns section was dispositioned M (it overlaps a kept section) when its only kept partner was FAL (now FALS). Their merged pools are 6,827 and 6,233 words and are in practice the whole source. Section 9.1 asks the author to treat those M rows as K for these two pages.

**FIRST is thin.** 1,010 kept words against the headline outputs O4a and O4b. The LDW payslip rows (1,618 words) are in PAY by the author's decision (`map.md` section 7). If the author wants FIRST to carry the non-payer saving, they move to FIRST and PAY falls to 2,594 (section 9.1).

## 3. Hub and standalone
- **H1 (the problem)** has 441 old words (WP §1 and §2.4, about concentration). The rest of H1 is new writing and needs outputs the manifest lacks: section 6.1 (OH1a was dropped on 2026-11-17; the manifest note gives the reason).
- **H2** has 152 old words (WP §3 opener). H0 and H3 to H7 draw on spokes and the data layer; no old words are assigned to them.
- **Standalone, as decided:** ADD 6,789 words, INST 14,264, SCOPE 2,537. INST §7 (the three competitive advantages) rests on O1, O4a and OP1, so it is not free of the model.
- **Decided (author, 2026-11-17):** ENT, the attribution test for charities, trusts, SPVs, partnerships, insurance wrappers, carried interest, manipulation and public entities (CORP.A §E, 6,498 words), is the page **ATTR**, reached from CORP; its four rows are K.

## 4. Claims that need model numbers, checked against `outputs.yml`
Each is a claim the old papers make from v1 or v2 runs. The hub and spokes may not carry the figure; they cite the output. Coverage: **yes** the manifest has the output; **partly** it has part; **no** it has nothing.

| # | Old claim (v1 figure) | Where | Output | Coverage |
|---|---|---|---|---|
| 1 | Revenue-weighted burden 0.35% of net worth, below 1 to 2% for stock wealth taxes | WP §5.1; RATES §2; BEHAV §9.2 | O2, O5 | yes; M2 formula still to be checked against 0.35% |
| 2 | Gain-weighted lifetime rate 13.0%, below CGT 18 to 24% and income tax up to 45% | WP §5.1; RATES §2 | O3, O6 | yes |
| 3 | Long reserve fills in every one of 73 start years and never reaches zero; breakeven 7 to 29 years, median 13 | WP §5, §10; RATES.A §B.5; FM §3.1 | OP1, reserve solvency | partly: fill years yes, "never reaches zero" no. v2 closes 42 to 55% of windows (`drivers.md` D1), so the v1 claim is not carried |
| 4 | Short reserve fills within 3 years under every sequence | WP §10; FM §3.1; RATES.A §B.2 | OP1 | yes |
| 5 | 10-year post-fill coverage: median 125.5%, worst case 6 to 15% of spending | WP §5; FM §3.1 | O1 over spending | partly: O1 is in % of GDP; spending share is a derived denominator |
| 6 | Individual WDT 874bn a year at the 30-year average, corporate levy 172bn at 30% unattributable | WP §5; RATES §8.3 | O1a, O1b | yes |
| 7 | Tolerant zone alpha 0.8 to 1.5; behavioural centre near 1.1; understater penalty plateaus; overstatement self-limiting | WP §3.8; VAL §7; VAL.A §A.2, §C; SWEEPS §2 | O7 | partly: O7 gives the zone, not the curve or the centre |
| 8 | Parameter hierarchy: entry rate dominates revenue, ceiling rate inert, steepness sets zone width, threshold sets scope | SWEEPS §3 to §7 | tornado, feasibility map | no entry in the manifest (both are in `metrics.md`) |
| 9 | Payslip: care worker on 25,000 gains 3,480 a year; 618 a month at median earnings; purchasing power up 36% and 29% | LDW §2, §4.4; POL §5.3 | O4a, O4b | partly: shares yes; pounds per month and price pass-through are a view on O4b plus the incidence input |
| 10 | CGT lock-in costs 141 to 143 basis points, the dominant welfare result; concentration and contribution envelope under heterogeneous returns | WFR §4.2, §4.3; WFR.A | welfare layer | no |
| 11 | Route D holds 10 to 20% of taxable wealth | BEHAV §8.2, §11.2 | input (012r) | no: an input, not an output |
| 12 | Cross-base externality: income tax and VAT lost per unit of wealth tax lost to emigration | BEHAV §9.2, BEHAV.A §D; WP §7.3 | net fiscal effect after migration | no (driver D5 has no output) |
| 13 | About 32,000 payers at a 10m threshold; fall-through refund volume as the threshold drops | WP §9.3; CLOSE §4.3, §7.2 | payer count and flows | no |
| 14 | Six taxes retired in steps; corporate levy may displace corporation tax | WP §6; CORP §9.2 | O1d, OP5, OP3, O1b | yes |
| 15 | Housing price response when stamp duty and council tax go | ENV §8; LDW §4.2 | OS1 | yes |
| 16 | Three competitive advantages: resource pool, welfare floor, crisis capacity | INST §7 | O1, O4a, OP1 | yes |
| 17 | Break-even burden at which a taxpayer prefers the existing system (H1) | FAL §3.3 | O2 against O6 | yes, derived |
| 18 | Automatic stabilisation: refunds dampen the fiscal swing by return state (H2c) | FAL §4.4 | O1 by return path, OP6 | yes, derived |
| 19 | Welfare of six tax systems at revenue equivalence (H4) | FAL §6; WFR §3 | welfare layer | no |
| 20 | Automation resilience of the base (H5); feedback loop integrity (H2d); cooperative equilibrium (H3) | FAL §5, §7; ENV §5 | none | not modelled; stays a stated hypothesis |
| 21 | UK wealth shares (top 1% 18 to 23%, top 10% about half), wealth to GDP, tax mix | WP §2.4; JUR §2.4, §3.1 | data layer | data facts, not model outputs |

Outputs in the manifest that no old section demands: **O1c** (fund income net of retention), **OP4** (sustainability) and **O8** (reform-in-place benchmark). They come from the v3 design, so their claims are new writing, not rewrites.

## 5. `element:` filled in `outputs.yml`
Every entry names the hub sections and the page shortcodes that use it (R1: an output with no element does not exist). The assignment follows the author's decision of 2026-11-17: O4a and O4b to FIRST (and PAY, FUND, H0, H3), OS1 to WIDER, CK1 to FALS, the other former S12 outputs to UNCER, none to LIMIT. The values are proposals until the author approves the stage. Section 9.3 shows where that assignment disagrees with the rows now placed in FALS.

## 6. Proposed additions (not added to `outputs.yml`)
### 6.1 The problem section, H1 first
The old papers state the problem in 441 words and give it no numbers. Three outputs and three data facts would let H1 stand on evidence. They are proposals; the claims H1 makes are fixed when it is drafted.

| Id (proposed) | Claim H1 can make | What it needs | Kind |
|---|---|---|---|
| OH1a (dropped by the author, 2026-11-17: it rested on returns rising with wealth rank, which has no UK evidence; `outputs.yml`) | Without a change, wealth concentration rises: top 1% share at years 10, 25 and 50, with and without the WDT | heterogeneous returns (Fagereng premise); the same run as the concentration output in 6.2 | model output |
| OH1b | Large holders pay a lower rate on gains than workers pay on earnings: gain-weighted lifetime rate under today's taxes for the payers (M3 on today's system) beside a median worker's income tax and NICs rate | extends M6, which gives the burden as a share of wealth but not the rate on gains | model output |
| OH1c | Most gains on large wealth are never taxed today: share of lifetime gains that escape tax through deferral and uplift at death, by wealth band | a holding-period and realisation input by band (012r) | model output |
| D-H1a | Wealth is concentrated: top 1% and top 10% shares, wealth to GDP, over time | WAS, IFS, Rich List (UK data pack) | data fact |
| D-H1b | The tax mix leans on labour: receipts by head, labour taxes against wealth-linked taxes | JUR §3.1 tables, current year | data fact |
| D-H1c | Who bears the tax today: non-payers' tax bill by income decile, the M4a denominator | incidence by decile (012r input D6) | data fact |

### 6.2 Other pages
| Page | Outputs it needs that the manifest lacks | Source of the need |
|---|---|---|
| MECH | payer count, entries, exits and fall-through refund volume (**OB1**) | CLOSE §4.3 |
| VAL and DECL | declaration curve across alpha with the modal declaration, understater plateau, lost refund protection (**OD1**, extends O7); asset share by route (input) | VAL §7, VAL.A §C, BEHAV §8.2 |
| FISC | payer count and base by threshold (OB1); reserve solvency, share of paths where the long reserve ever reaches zero and the minimum cover (**OR1**); feasibility map over the schedule family (**OF1**); tornado (**OT1**); spending share of M1 (derived) | WP §5, §9.3; RATES; SWEEPS |
| PAY, BEHAV and WELF | net fiscal effect after migration (**OM1**); worker view of the non-payer saving in pounds per month (**OL1**, a derived view of O4b); welfare layer: certainty-equivalent welfare (**OW1**), CGT lock-in cost (**OW2**), concentration (the same as OH1a), contribution envelope binding (**OW3**) | BEHAV §9.2; LDW §2, §4.4; WFR §3, §4 |
| FUND | OL1 | LDW §4.3; POL §5.3 |
| UNCER and FALS | OB1; OW1; synthetic cyclical stress test (question: drop it, or confirm level 1 sampling covers cycles) | SWEEPS §7.5; FAL §6 |
| FAIR, LIT, CORP, GOV, POL, FIRST, WIDER | none beyond the manifest | |

### 6.3 Not outputs
- **Inputs for 012r:** share of taxable wealth by valuation route and asset class (BEHAV §8.2, BEHAV.A §A); holding-period and realisation by band (OH1c).
- **Fixtures for the code lane:** the five VAL.B worked examples take their figures from the v1 simulation or closed-form arithmetic; regenerate or recompute them once, and keep them as test fixtures.
- **Not modelled in v3:** automation resilience (H5), feedback loop integrity (H2d), cooperative equilibrium (H3). They stay stated hypotheses in FALS with their falsification conditions.

## 7. Corrections to `map.md` section 4 ("fed by")
Applied to `map.md` by brief 025w, in the shortcodes.
- **MECH** is fed by WP §3, VAL §3 and CLOSE (closure events, re-entry); not JUR (4) or PHASE1 (13).
- **FISC** is fed by RATES, SWEEPS and WP §5; CLOSE (11) feeds MECH, BEHAV (its objections) and FUND, not FISC.
- **FUND** also takes VAL §13 (liquidity facility), CLOSE §5 (closure bonds), GOV §6.3 (Custodian), LDW §4.3 and POL §5.3.
- **GOV** takes GOV, GOV.B, JUR §1 and §1.5, and VAL §10.6 and §12.
- **POL** takes POL, FM, MOD and PHASE1.
- **FIRST and WIDER** take ENV and LDW: LDW §3 and §5 go to FIRST; ENV §3 to §8 and LDW §4.2, §4.5 and §6 go to WIDER; the LDW payslip rows stay in PAY. LR.B §18 goes to BEHAV. WFR goes to WELF (and LIT for the literature), not to FIRST or WIDER.
- **FALS** is FAL (with SWEEPS §7.5 and the check CK1). **UNCER** takes the unknowns and modelling gaps, and **LIMIT** the structural limits and named compromises, of every paper; the per-paper "Limitations" registers are otherwise dropped.
- JUR (4): institutions to GOV; the data tables, gaps and input provenance to the data layer.

## 8. Decisions (author, 2026-11-17)
1. **Budget:** split S4 and S6 (option 3) into VAL and DECL, and PAY, BEHAV and WELF and raise the cap to 6,000 words (author confirmed 6,000). A spoke that holds more than its cap moves its less important material into a secondary spoke, an appendix to that spoke (the `-A` suffix retired on 2026-11-17; the page gets its own shortcode, `ids-map.md`).
2. **ENT:** a separate page, **ATTR**, reached from CORP.
3. **Welfare layer:** add OW1 to OW3, designed together with model v3 (page WELF).
4. **H1:** accept OH1a to OH1c (OH1a was later dropped, section 6.1) and D-H1a to D-H1c for now; refine later.
5. **Manifest:** add OF1, OT1, OB1, OR1, OD1, OM1 and OL1.
6. **Synthetic stress test (SWEEPS 7.5):** keep (confirmed: kept as a stated output or check).
7. **v1 headline figures:** not carried; v3 will contradict them again. Confirmed.

## 9. Reassignment to the shortcodes (brief 025w, 2026-11-17)

Every row of `ledger-sections.md` now has a shortcode, a standalone code, the data layer or a drop reason as its target; none has an S id. Rows the brief moved carry a `[025w: ...]` note in the Note column.

### 9.1 How the rows were placed, and what is in doubt
- **Converted by `ids-map.md`:** S1 to FAIR, S2 to LIT, S3 to MECH, S5 to FISC, S7 to FUND, S8 to CORP, S9 to GOV, S10 to POL.
- **S4 and S6, split as `map.md` section 7 decided:** VAL 7, VAL.A findings (A.2) and VAL.B go to DECL, with four merge rows on the same subject; the rest of S4 is VAL. RATES 2, WP 8.2 and the LDW payslip go to PAY; WFR (19) goes to WELF; BEHAV, BEHAV.A, CLOSE 8 and WP 7.3, 8.3 and 8.7 go to BEHAV. The four ENT rows are K on ATTR (they were SA).
- **S11 (29 rows, 10,855 words):** FIRST 4 rows, 1,010 words, WIDER 21 rows, 7,986 words, PAY 2 rows, 1,108 words, BEHAV 1 rows, 547 words, LIMIT 1 rows, 204 words. FIRST takes the direct effects of removing NICs on the employment relationship and household capacity (LDW 3.1, 3.2, 5). WIDER takes the longer chains: capital allocation, automation and the tax base, the consumption multiplier, financial stability, inflation response, housing, demand reallocation, welfare demand. A merge row follows the page of the kept section it overlaps.
- **S12 (104 rows, 25,844 words):** FALS 52 rows, 12,784 words, UNCER 25 rows, 6,827 words, LIMIT 27 rows, 6,233 words. FALS takes FAL (all of paper 22), the synthetic stress test (SWEEPS 7.5, CK1) and the objections about falsifiability and circularity (POL 8.1, 8.2, 8.6). UNCER takes what is not yet known: Phase One empirical unknowns, formal modelling gaps, open questions, the epistemic status of a paper. LIMIT takes what the design cannot do: the structural-limit registers (§9.4 and §9.5), the named compromises, governance decay, the membrane limit. The test is the one in `shortcodes.md` section 4.

Rows where the placement is a judgement (the page chosen, and the alternative):

| Row | Words | Placed | Alternative | Reason |
|---|---:|---|---|---|
| 3b §18 Exit taxation and international coordination (M) | 547 | BEHAV | WIDER | overlaps the kept migration rows (WP 7.3, BEHAV.A D) |
| ENV §4.2 NICs case (M) and §4.6 displacement effects on households (M) | 1,108 | PAY | FIRST | duplicate the kept LDW payslip rows, which the author placed in PAY |
| ENV §4.7 Extreme automation as a stress test (K) | 224 | WIDER | FALS | a scenario in the transmission chain; the H5 falsification conditions are in FALS (FAL 7) |
| ENV §4.8 What the WDT does not solve (K) | 204 | LIMIT | WIDER | a structural limit, not a transmission effect |
| WP 9.3 Fiscal concentration risk (M) | 299 | UNCER | FISC | an unknown about payers at the threshold; its figure needs OB1, which the manifest gives to UNCER |
| RATES.A 11 Limitations of the sweeps (M) | 1,211 | UNCER | LIMIT | method gaps (single reference taxpayer, extrapolation), not limits of the design |
| VAL 14.3 and 14.4 (M) | 994 | UNCER (14.3), LIMIT (14.4) | - | legal work still to do against a structural boundary, split by subsection |
| MF 8 Tolerance for imperfect compliance (M) | 295 | LIMIT | DECL | a boundary the design accepts; it links to O7, which the manifest gives to DECL, so LIMIT can only point there |
| POL 7 Self-shaping problem (M) | 251 | LIMIT | UNCER | a problem the design cannot remove |
| POL 8.6 Democratic flourishing as the terminal good (M) | 237 | FALS | LIMIT | the objection that the terminal goal is not falsifiable |
| LDW 7.1 and 7.4 (M) | 522 | UNCER | LIMIT | what the paper can and cannot establish, and claims that survive conservative assumptions |

**Two overlaps to know about.** ENV 3 (capital allocation, hypothesis H2a) is kept in WIDER and FAL 4.2 (the same hypothesis, with its falsification condition) is kept in FALS. WFR 4.3 (concentration and the envelope, in WELF) and FAL 6 (accumulation-point efficiency, in FALS) share the welfare comparison. The ledger keeps both copies, as it did before the split; the writing lane states each claim once and cross-references.

**For the author.**
1. UNCER and LIMIT have no kept rows of their own (section 2). *Proposed:* treat their M rows (6,827 and 6,233 words) as K, since no kept section overlaps them. I have not changed the disposition.
2. FIRST has 1,010 kept words. *Proposed:* leave the payslip in PAY as decided, and revisit when FIRST's short answer is drafted; if the author moves it, FIRST gets LDW 2 and 4 (1,618 words) and PAY falls to 2,594.

### 9.2 Pages over 6,000 kept words: proposed splits
A page whose kept words are at or below 1.9 times its cap should fit after compression (template section 3), so a split is **default** only above 1.9 and **optional** below it. New shortcodes are working names for the author to confirm or change; a split moves rows, it does not add words. The words moved are kept words of the rows named.

| Page | Kept | Ratio | Verdict | Proposed split: new page, what moves, words | Page left with | Affects |
|---|---:|---:|---|---|---:|---|
| POL | 13,238 | 2.21 | default | **ADOPT and PILOT**: first mover and modular adoption (FM, MOD, 4286); Phase One (PHASE1, 2817), 7,103 words | 6,135 | OP3, OP5 and OR1 stay in POL (check) |
| FALS | 12,135 | 2.02 | default | **HYPO**: hypotheses H2 to H5 (FAL 4 to 7), 6,096 words | 6,039 | CK1 stays in FALS |
| DECL | 10,700 | 1.78 | optional | **EXMP**: worked examples (VAL.B), 4,798 words | 5,902 | O7 and OD1 stay in DECL |
| GOV | 10,668 | 1.78 | optional | **SAFE**: safeguards and executive bodies (GOV 3 to 6), 5,653 words | 5,015 |  |
| WELF | 9,671 | 1.61 | optional | **CONC**: heterogeneous returns, incidence and the envelope (WFR 4.3) and progressive WDT advantage (WFR 7.4), 3,639 words | 6,032 | OW3 would move to CONC |
| CORP | 9,671 | 1.61 | optional | **OWNR**: ownership, institutions, administration and foreign attribution (CORP 7, 8; CORP.A C, D, F), 4,490 words | 5,181 | O1b stays in CORP |
| LIT | 8,580 | 1.43 | optional | **GAPS**: research gaps (3a, 3302), 3,302 words | 5,278 |  |
| FISC | 8,164 | 1.36 | optional | **SENS**: parameter hierarchy and the small lever set (SWEEPS 7.1 and 9), 1,860 words | 6,304 | OT1 would move to SENS |
| BEHAV | 6,797 | 1.13 | optional | **MIGR**: migration and the cross-base externality (WP 7.3, BEHAV 9.1 and 9.2, BEHAV.A D, CLOSE 8), 2,381 words | 4,416 | OM1 would move to MIGR |
| MECH | 6,972 | 1.16 | optional | **TERM**: closure events and re-entry (CLOSE 4 and 6), 3,413 words | 3,559 |  |
| VAL | 6,784 | 1.13 | optional | **AUCT**: Route D auction (VAL 6.5 and 11), 1,719 words | 5,065 |  |
| ATTR | 6,498 | 1.08 | optional | **MANIP**: market manipulation (ENT E.9), 1,233 words | 5,265 |  |
| FUND | 6,210 | 1.03 | optional, marginal | **LIQ**: liquidity facilities (VAL 13, CLOSE 5), 1,299 words | 4,911 |  |
| WIDER | 6,054 | 1.01 | no split | not needed: over by 54 words | 6,054 | |

FAIR (5,947), PAY, FIRST, UNCER and LIMIT are within the cap. After the two default splits there are 22 pages (ADOPT, PILOT and HYPO are new); all the proposals would make 32. The kept words are before compression, so a page the table calls optional may need no split; stage E measures it. An output listed in a moved row's page changes `element:` if its claims move (last column); the guru edits the manifest.

### 9.3 Model-number claims in FIRST, WIDER, UNCER, LIMIT and FALS
Rows with model Y or P in these pages (and merge rows), checked against `outputs.yml` as of this brief. **Covered** means the manifest has an output and the page's `element:` lists it.

| Page | Rows | Demand | Manifest | Result |
|---|---|---|---|---|
| FIRST | LDW 3.1, 3.2, 5 (P, 1,010 words) | none stated | O4a, O4b in FIRST | covered; household capacity in pounds a month would need OL1, which lists PAY and FUND, so add FIRST to OL1 if the draft cites it |
| WIDER | ENV 8, LDW 4.2, 4.5 (housing, Y/P, 1,946 words) | OS1 | OS1 in WIDER | covered |
| WIDER | ENV 5 consumption multiplier (P, 795 words) | none | none | no output; v3 is partial equilibrium, so the claim stays structural |
| UNCER | CORP 9.2 (Y, 248) | O1b, O1d | listed in UNCER | covered |
| UNCER | WP 9.3, CLOSE 9.2 (Y and P, 456) | payer count, entries, exits (old tag NEW:payers) | OB1 lists UNCER | covered |
| LIMIT | all rows (N) | none | none | nothing to cover |
| FALS | FAL 3 (H1, P/Y, 1,302) | O2, O5, O6 | O2, O5, O6 list UNCER, not FALS | **not covered by element** |
| FALS | FAL 4.1 to 4.3 (H2a, H2b; P, 1,195 with 4.1) | O4a | O4a lists UNCER, not FALS | **not covered by element** |
| FALS | FAL 4.4 (H2c, P, 541) | O1, OP6 | both list UNCER, not FALS | **not covered by element** |
| FALS | FAL 6 (H4, P, 994) | certainty-equivalent welfare (old tag NEW:cew) | OW1 lists WELF and UNCER, not FALS | **not covered by element** |
| FALS | SWEEPS 7.5 (Y, 775) | stress test (old tag NEW:stress) | CK1 lists FALS | covered |
| FALS | FAL 4.5, 5, 7 (H2d, H3, H5; N) | none (old tag NEW:automation on H5) | none | not modelled in v3; stay stated hypotheses with falsification conditions (section 6.3) |

**New outputs proposed: none.** Every demanded quantity has an output. What fails is the assignment: the author gave the former S12 outputs to UNCER, but the rows that use them are FAL's and sit in FALS. R1 would reject FALS hooks to O1, O2, O4a, O5, O6, OP6 and OW1, and would reject UNCER for listing outputs none of its rows cites. *Proposed amendments to `element:` (not applied; the guru edits the manifest):*

| Output | Now | Proposed |
|---|---|---|
| O1 | H0, H3, FISC, POL, UNCER | H0, H3, FISC, POL, FALS |
| O2 | H0, H3, FISC, PAY, UNCER | H0, H3, FISC, PAY, FALS |
| O4a | H0, H3, PAY, FUND, FIRST, UNCER | H0, H3, PAY, FUND, FIRST, FALS |
| O5 | FISC, PAY, UNCER | FISC, PAY, FALS |
| O6 | FISC, PAY, UNCER | FISC, PAY, FALS |
| OP6 | FUND, UNCER | FUND, FALS |
| OW1 | WELF, UNCER | WELF, FALS |
| OW3 | WELF, UNCER | WELF |

OW3 (contribution envelope) is cited by WELF only; no UNCER or FALS row demands it. OB1, O1b and O1d keep UNCER. Outside this brief's five pages: WELF 4.3 (2,697 words, concentration and the envelope) still demands a concentration output and OH1a was dropped on 2026-11-17, so the concentration result has no output; OW3 covers the envelope. The guru decides.

### 9.4 The four reader-facing pages
Named in `site/ids.md` Q7 (they carry reader-facing material and v1 numbers that are not in the 33 papers' rows). Section rows are at the end of `ledger-sections.md`. Words are body words without heading lines.

| Page | Words | Folds into (words, disposition M) | D | AR | Note |
|---|---:|---|---:|---:|---|
| `faq.md` | 2,088 | FISC 605, FUND 552, BEHAV 213, FAIR 179, MECH 169, PAY 161, VAL 135 | 74 | 0 | the twelve questions become the entry list of H5; each answer is already a spoke's objection or short answer |
| `comparison-tables.md` | 1,242 | WELF 456, FUND 193, MECH 179, BEHAV 156, POL 91, VAL 76 | 91 | 0 | the table form conflicts with template 6a rule 3 (question 3 below) |
| `avoidance.md` | 3,040 | DECL 841, MECH 694, BEHAV 560, VAL 519 | 316 | 110 | a second-person guide to the same routes; the calculator embed stays until a v3 calculator replaces it |
| `corporate-levy-taxpayer.md` | 2,031 | CORP 1,358, ATTR 220 | 184 | 269 | the worked example (v1 figures) is archived; a VAL.B-style fixture can replace it |
| Total | 8,401 | M 7,357 | 665 | 379 | |

**Words kept: none.** Each section restates a kept or merged section of the papers, so the four pages add 7,357 merged words to the pool and no kept words; the per-page budget in section 2 is unchanged. Their reader-facing wording (questions as headings, a second-person voice) is a style input for the writing lane.

**For the author.**
3. The comparison page is a table of three systems on eleven criteria. Template section 6a, rule 3 allows tables only in the Data block, and template section 10(b) leaves open a table type for tables that are not data. *Proposed:* fold the content into WELF and H5 as prose, and decide a table type only if the author wants the page kept as a table.
4. The avoidance guide is all M. *Proposed:* fold it into BEHAV, DECL, VAL and MECH, and keep none of its form; if the author wants a reader page in the guide's voice, it is built from the objection blocks later.

## 10. Checks run
- Every section of all 33 papers resolves to a disposition: the generator reported no unresolved section across 980 rows (stage B). Brief 025w: all 980 rows have a shortcode, a standalone code, a data-layer or register target or a drop reason; no row has an S id as its target (grep of `ledger-sections.md`).
- Words kept per page are recomputed from the rows (sum of K rows by target): 133,808 in total, equal to the stage B total plus the 6,498 words of ENT.
- `git diff --stat origin/main` touches only the Touches list of brief 025w.
- Not run: a read of every paper in full. Dispositions rest on the section headings, openings and number-bearing sentences of each section; the rows marked K with `Y` should be read in full when the page is drafted. The four site pages were read by section opening only.
