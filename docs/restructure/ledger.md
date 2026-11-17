# Content ledger: summary (brief 013g, stage B)

Status: stage B drafted, waiting for the author. One row per section of all 33 old papers is in `ledger-sections.md` (980 rows, no section without a disposition). This file holds the totals, the budget finding, the demanded outputs checked against `outputs.yml`, the proposed additions and the decisions for the author. Words are body words counted per section, about 2% under `wc`.

## 1. What the 33 papers hold
| Disposition | Rows | Words | Share |
|---|---:|---:|---:|
| K keep to a spoke or hub section | 394 | 127,310 | 37% |
| M merge (overlaps a kept section) | 207 | 59,712 | 17% |
| SA standalone paper | 36 | 30,088 | 9% |
| DL move to the data layer | 69 | 24,253 | 7% |
| AR archive (design history, v1 results, statute detail) | 199 | 86,031 | 25% |
| D drop as redundant | 75 | 15,101 | 4% |
| Total | 980 | 342,495 | |

Read this as: a quarter of the old words (AR 86,031) is v1 result tables, operational statute detail and design history that no reader needs; 127,310 words are kept for 12 spokes and the hub; 59,712 overlap them and are the pool for compression.

## 2. Words kept per spoke against the 2,000 to 4,000 budget
"Kept" is the old words of K rows. "Merged" is the old words of M rows, which overlap kept sections and are not additional. "Model words" is kept and merged words whose claims need model numbers (Y) or partly (P); those get replaced by data hooks, so they shrink most.

| Spoke | Question | Kept | Merged | Kept ÷ 4,000 | Model words Y / P |
|---|---|---:|---:|---:|---:|
| S1 | Is it fair? | 5,947 | 1,876 | 1.5 | 0 / 714 |
| S2 | What exists, what is missing? | 8,580 | 3,869 | 2.1 | 380 / 0 |
| S3 | What exactly is taxed and when? | 6,972 | 1,587 | 1.7 | 0 / 425 |
| S4 | How is wealth measured? | 17,484 | 6,603 | 4.4 | 7,414 / 6,267 |
| S5 | What rate, what threshold, how much? | 8,164 | 8,445 | 2.0 | 14,488 / 1,478 |
| S6 | Who pays, what do they do? | 20,680 | 4,631 | 5.2 | 13,484 / 5,829 |
| S7 | Where does the money go? | 6,210 | 3,021 | 1.6 | 3,110 / 1,331 |
| S8 | How are firms treated? | 9,671 | 3,942 | 2.4 | 2,555 / 0 |
| S9 | Who runs it, on what law? | 10,668 | 4,387 | 2.7 | 0 / 970 |
| S10 | Can it pass, how is it staged? | 13,238 | 3,755 | 3.3 | 546 / 3,731 |
| S11 | What are the wider effects? | 7,268 | 3,587 | 1.8 | 374 / 5,817 |
| S12 | What would falsify it? | 12,135 | 13,709 | 3.0 | 1,565 / 5,157 |
| H1 | The problem (hub) | 141 | 300 | | 0 / 141 |
| H2 | The tax in one page (hub) | 152 | 0 | | |

**Finding.** Every spoke is over budget on kept words alone: 127,017 kept words against 48,000 for twelve spokes at the cap, a ratio of 2.6. The author expected this ("alarmingly short"). Under the brief the budget is revisited here, not squeezed.

Where the weight sits (kept words by source paper): S6 is WFR 9,671, BEHAV 4,317, RATES 1,925, WP 1,626, LDW 1,618, BEHAV.A 1,199. S4 is VAL 11,312, VAL.B 4,798, VAL.A 1,374. S10 is POL 5,489, FM 2,985, PHASE1 2,817, MOD 1,301. S12 is FAL 11,360. S9 is GOV 7,405 and JUR 1,996. S8 is CORP 5,464 and CORP.A 3,746.

**Options.**
1. Keep 4,000 and compress. Needed ratios of old to new: S6 5.2, S4 4.4, S10 3.3, S12 3.0, S9 2.7, S8 2.4, S2 2.1, S5 2.0, S11 1.8, S3 1.7, S7 1.6, S1 1.5. A laconic rewrite of verbose prose can reach about 2.5 to 3; beyond that it is a cut, not a compression.
2. Raise the cap to 6,000. Ratios fall to 3.4 for S6 and 2.9 for S4; the rest are 2.2 or less. Simple, but the spokes stop being short.
3. Split the two that need more than 4. S6 becomes **who pays** (RATES 2, WP 8.2, LDW payslip, about 4,200 words kept), **what they do** (BEHAV, BEHAV.A, CLOSE objections, WP 7.3, 8.3 and 8.7, about 6,800) and **the welfare comparison** (WFR, 9,671, which waits on the welfare outputs in section 6.2). S4 becomes **valuation routes** (VAL 1 to 6 and 9 to 12, about 6,800) and **declaration incentives** (VAL 7, VAL.A findings, VAL.B examples, about 10,700, which depends on O7 and the declaration curve). That gives 15 spokes, with S10 and S12 left at 3.3 and 3.0 to be tested on one paragraph at stage C.

Recommendation: option 3, with the 4,000 cap kept for the other ten and revisited at stage C once the test paragraph shows the real compression ratio. The author decides.

## 3. Hub and standalone
- **H1 (the problem)** has 441 old words (WP §1 and §2.4, about concentration). The rest of H1 is new writing and needs outputs the manifest lacks: section 6.1.
- **H2** has 152 old words (WP §3 opener). H0 and H3 to H7 draw on spokes and the data layer; no old words are assigned to them.
- **Standalone, as decided:** ADD 6,789 words, INST 14,264, SCOPE 2,537. INST §7 (the three competitive advantages) rests on O1, O4a and OP1, so it is not free of the model.
- **Proposed standalone, not decided:** ENT, the attribution test for charities, trusts, SPVs, partnerships, insurance wrappers, carried interest, manipulation and public entities (CORP.A §E, 6,498 words). It does not fit a 4,000-word S8. The author decides; otherwise it is archived.

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
All 21 entries now name the hub sections and spokes that use them (R1: an output with no element does not exist). The mapping follows `map.md` sections 2 and 4, plus the extra consumers the ledger found: O4a and O4b in S6 (the payslip), S11 and S12; O5, O6 and O2 in S12 (FAL H1); OP6 in S7 and S12; OP3 and OP5 in S10. The values are proposals until the author approves the stage.

## 6. Proposed additions (not added to `outputs.yml`)
### 6.1 The problem section, H1 first
The old papers state the problem in 441 words and give it no numbers. Three outputs and three data facts would let H1 stand on evidence. They are proposals; the claims H1 makes are fixed when it is drafted.

| Id (proposed) | Claim H1 can make | What it needs | Kind |
|---|---|---|---|
| OH1a | Without a change, wealth concentration rises: top 1% share at years 10, 25 and 50, with and without the WDT | heterogeneous returns (Fagereng premise); the same run as the concentration output in 6.2 | model output |
| OH1b | Large holders pay a lower rate on gains than workers pay on earnings: gain-weighted lifetime rate under today's taxes for the payers (M3 on today's system) beside a median worker's income tax and NICs rate | extends M6, which gives the burden as a share of wealth but not the rate on gains | model output |
| OH1c | Most gains on large wealth are never taxed today: share of lifetime gains that escape tax through deferral and uplift at death, by wealth band | a holding-period and realisation input by band (012r) | model output |
| D-H1a | Wealth is concentrated: top 1% and top 10% shares, wealth to GDP, over time | WAS, IFS, Rich List (UK data pack) | data fact |
| D-H1b | The tax mix leans on labour: receipts by head, labour taxes against wealth-linked taxes | JUR §3.1 tables, current year | data fact |
| D-H1c | Who bears the tax today: non-payers' tax bill by income decile, the M4a denominator | incidence by decile (012r input D6) | data fact |

### 6.2 Other spokes
| Spoke | Outputs it needs that the manifest lacks | Source of the need |
|---|---|---|
| S3 | payer count, entries, exits and fall-through refund volume (**OB1**) | CLOSE §4.3 |
| S4 | declaration curve across alpha with the modal declaration, understater plateau, lost refund protection (**OD1**, extends O7); asset share by route (input) | VAL §7, VAL.A §C, BEHAV §8.2 |
| S5 | payer count and base by threshold (OB1); reserve solvency, share of paths where the long reserve ever reaches zero and the minimum cover (**OR1**); feasibility map over the schedule family (**OF1**); tornado (**OT1**); spending share of M1 (derived) | WP §5, §9.3; RATES; SWEEPS |
| S6 | net fiscal effect after migration (**OM1**); worker view of the non-payer saving in pounds per month (**OL1**, a derived view of O4b); welfare layer: certainty-equivalent welfare (**OW1**), CGT lock-in cost (**OW2**), concentration (the same as OH1a), contribution envelope binding (**OW3**) | BEHAV §9.2; LDW §2, §4.4; WFR §3, §4 |
| S7 | OL1 | LDW §4.3; POL §5.3 |
| S12 | OB1; OW1; synthetic cyclical stress test (question: drop it, or confirm level 1 sampling covers cycles) | SWEEPS §7.5; FAL §6 |
| S1, S2, S8, S9, S10, S11 | none beyond the manifest | |

### 6.3 Not outputs
- **Inputs for 012r:** share of taxable wealth by valuation route and asset class (BEHAV §8.2, BEHAV.A §A); holding-period and realisation by band (OH1c).
- **Fixtures for the code lane:** the five VAL.B worked examples take their figures from the v1 simulation or closed-form arithmetic; regenerate or recompute them once, and keep them as test fixtures.
- **Not modelled in v3:** automation resilience (H5), feedback loop integrity (H2d), cooperative equilibrium (H3). They stay stated hypotheses in S12 with their falsification conditions.

## 7. Corrections to `map.md` section 4 ("fed by")
- **S3** is fed by WP §3, VAL §3 and CLOSE (closure events, re-entry); not JUR (4) or PHASE1 (13).
- **S5** is fed by RATES, SWEEPS and WP §5; CLOSE (11) feeds S3, S6 and S7, not S5.
- **S7** also takes VAL §13 (liquidity facility), CLOSE §5 (closure bonds), GOV §6.3 (Custodian), LDW §4.3 and POL §5.3.
- **S9** takes GOV, GOV.B, JUR §1 and §1.5, and VAL §10.6 and §12.
- **S10** takes POL, FM, MOD and PHASE1.
- **S11** takes ENV, LDW and LR.B §18; WFR goes to S6 (and S2 for the literature), not S11.
- **S12** is FAL plus the unknowns and limits of every paper; the per-paper "Limitations" registers are otherwise dropped.
- JUR (4): institutions to S9; the data tables, gaps and input provenance to the data layer.

## 8. Decisions for the author
1. **Budget:** option 1, 2 or 3 in section 2 (recommended: 3).
2. **ENT** (CORP.A §E, 6,498 words): standalone paper, or archive.
3. **Welfare layer** (WFR, 9,671 kept words in S6): add OW1 to OW3 to the manifest, or keep WFR as labelled v1 results with no hub claim.
4. **H1:** accept OH1a to OH1c and D-H1a to D-H1c, or name the claims you want.
5. **Manifest:** add OF1 (feasibility map) and OT1 (tornado) as entries, since `metrics.md` already defines both; add OB1, OR1, OD1, OM1, OL1 on the same footing.
6. **Synthetic stress test** (SWEEPS §7.5): drop, or confirm level 1 sampling includes cycles.
7. **The v1 headline figures** in WP §5, FM §3.1 and INST are contradicted by v2 (100% success against 42 to 55% of windows). The ledger carries none of them. Confirm.

## 9. Checks run
- Every section of all 33 papers resolves to a disposition: the generator reported no unresolved section across 980 rows.
- `git diff --stat origin/main` touches only `docs/restructure/`, `docs/model-v3/outputs.yml` and the brief files.
- Not run: a read of every paper in full. Dispositions rest on the section headings, openings and number-bearing sentences of each section; the rows marked K with `Y` should be read in full when the spoke is drafted.
