# Decisions digest

One entry per finished brief or settled question, at most 8 lines each. Newest first. Maintained by the guru.

## 2026-11-22: tail pension ceiling (119c), a labelled scenario
- Author: the tail lines (D10a, D10b, RL3, RL2, RL1) hold pension of at most the D10 mean pension per adult, an absolute amount, real: 0.386 £m (WAS Round 8, D10 pension share 36.4% of D10 wealth times D10 mean wealth per adult 1.06 £m). Register row I-D1l, one value, mid-point label, no low or high.
- Why: no held distribution of pension wealth and no unit-record licence; with D10's class shares RL1 held 37% pension that is never sold, so the richest lines could not pay by year 69.
- Wealth the ceiling displaces goes to property, net financial and physical pro rata to D10's mix. D10a (0.24) is below the ceiling and unchanged; D10b to RL1 are capped.
- It is a scenario, not a measurement: replace the one value with the p90 or p99 of private pension wealth, or a lifetime-allowance-based figure, from an ONS pension-wealth-by-percentile table when one is held. The settlement rule (pension never sold) is unchanged.

## 2026-11-21: 100r JST cash yield and holding-gain split (data design)
- The JST file carries the split: equity and housing identities hold to 5e-6 percentage points; bonds use `bond_rate` as a yield proxy with `bond_tr - bond_rate` as the gain (not an observed coupon split); bills have zero nominal gain by convention.
- Portfolio weights are recovered from `capital_tr`, `risky_tr`, `safe_tr`: equity 28.6%, housing 41.2%, bonds 15.1%, bills 15.1% on average over 117 years. They are market-stock weights, not household weights.
- Real conversion: `y/(1+pi)` and `(g-pi)/(1+pi)`, matching `core/returns.py`; arithmetic and additive, not for compounded paths. Mean real yield 4.03% plus real gain 0.71% equals I-D1a (4.74%).
- Spec only: `returns_decomposition.csv` schema in `docs/research/100r-jst-cash-yield-and-gain-split.md`. It is the market return, not household saving or retained income. No pack, builder or I-D1a change.

## 2026-11-21: parameter-map phase approved; pension wealth is in the WDT base
- Author: the empirical household-flow parameter-map hypothesis (`docs/hypotheses/empirical-household-flow-parameter-map.md`) is approved as phase 2, briefed as 101r (flows and returns), 102r (stocks, stage weights, transitions), 103r (assembly: one register, cross-side checks, unresolved data, proposed rulings) and 104r (design side: coverage matrix, accounting conventions, public-side representation), with the accounting rulings left to the author. The evidence side was split after a single-agent brief ran out of tokens without pushing.
- Author: **pension wealth is inside the WDT base.** Pension accrual is household saving in the account; the pension valuation basis (ONS SCAPE-based, as the pack) matters for the base; pension wealth is not liquid cash for consumption or tax payment until drawn, a consequence 104r states for settlement.
- Phase 1 is complete (097r to 100r; the 099r moments contain no UK saving or return rate by band or stage).

## 2026-11-21: Scenario B and the household-flow plan
- Author: scenario B. Cells by wealth band and life stage, saving on the income side, parameters with no UK range left unset or run as labelled judgement scenarios, no universal scalar. The closure baseline (a scalar from the untaxed steady state) may be kept as a labelled comparison arm.
- Diagnosis recorded: the kernel has no household flow, so wealth is never replenished (wealth/GDP 47% of start by year 100, 62% with the tax off); 3.5% began as a v2 steady-state device and became a "consumption share" without its steady state being tested; the repeated `(1+g)(1-c)` is a cost, not a cause.
- Plan: `docs/model-v3/household-flow-plan.md`. Phase 1 is four collection briefs (097r, 098r, 099r, 100r); no code or register change until phase 2 (parameter map and rulings). Bozio and others (2013) read: `docs/research/095r-bozio-2013-reading.md`.

## 2026-11-20: I-D14c (3.5%) abandoned as the central assumption
- Author: the 3.5% is a v2 judgement device (decision D16), not a UK measurement (093r). It is abandoned as the central consumption or depletion assumption; no replacement scalar (no 0%, 1.5%, 2.5% or other universal rate). It stays as a labelled legacy comparator to reproduce historical outputs. Results that rest on it (083c, 090c, the first provisional run) are legacy results, not calibrated forecasts.
- Replacement: an accounting-consistent household flow model, by cells (hypothesis `household-consumption-and-wealth-replenishment.md`, sections 10 to 14). Briefs 094r (kernel map and accounts), 095r (UK evidence map), 096r (cohort cell design, with plans for backcast and comparison). Backcast and WDT comparison runs and the implementation are later code briefs, after the author reviews 096r. No change to kernel, register or manifest until then.
- Feasibility rule (089c) stays parked: it was measured against 3.5%. 057c still runs on 3.5% and labels the run legacy.
- Origin of the brief: an external agent drafted a combined 094 on a branch; the guru rewrote it as 094r to 096r (tests A and B; C; D with plans for E and F).

## 2026-11-20: after the output-group briefs (085c to 088c, 090c; 093r)
- 085c, 086c, 088c and 090c merged and retired; 087c (six of seven ids) resumes with a narrow `runner.py` edit for OS1. `o1e` and `ot1` are formatters, not runners (R4): the run script (057c) calls the sweeps.
- Author: hold the feasibility rule (089c) until the consumption evidence is in; no change to the margin, tolerance, closure share or CK1 window now. 093r gathers evidence for I-D14c (audit and net depletion by band); no value is chosen for its fiscal effect.
- Author: M5 and M8 compare against M2 in life only for the first run (stated limit; the O8 gap is +24.6 points at the median under tau_m 0.9 against M2 in life and about +5 against M2d). A with-death line (M5d row, O5 and O8 second line) is considered after the first provisional run.
- Author: M2 denominator is start-of-year wealth (already closed 2026-11-16; reconfirmed). RATES's 0.35% (terminal wealth) is restated when the papers are rewritten.

## 2026-11-20: 055c range runner merged; no schedule closes (briefs 055c, 083c to 089c)
- 055c merged as built (`e4993a4`): two-level runner and sweeps, N1 to N7, R3, R10 met, 201 model tests and all 10 suites pass. The branch stopped for the author because the feasible region is empty: short-window F1 4.0 to 11.2% at all 27 grid points against the A5 closure share of 75%, with a tolerance of 1e-9. On a constant 4.74% return path relief after the fill falls from 5.7% to 2.9% of GDP over 100 years against 4.74% retired, so CK1's P3 is 100.9 at amplitude 0 over 100 years.
- Author (2026-11-20): measure first (083c: tolerance, retirement margin, constant path, CK1 window), then rule on the feasibility rule; no constant (A5) or definition changes before then. 089c (OF1, CK1) is parked on that ruling.
- 055c built only O1, O1a to O1c, O2, O3, O4a, O1f into Samples; the other 32 manifest ids go to four group files filled in parallel (084c fixes the group interface and moves `payer_taxes` into `levers.json`; 085c revenue, 086c burden, 087c support, 088c sweeps and pack; 089c feasibility).
- CK1's mu is I-D1a central 4.74 (arithmetic), not 4.42 (the geometric I-D1a2): the `metrics.md` row carried the pre-036r figure and is corrected. 055c used 4.42 as the caller's argument; 057c's `run.py` reads it from the register.

## 2026-11-17: research inputs merged, ONS decile data read (briefs 022r to 024r)
- `docs/model-v3/inputs-added/` (wealth I-W 45 rows, tax I-T 58, households I-H 65) merged into `inputs.md` as a part of its own; the register now has 260 rows. A duplicate id in the tax file (two rows called I-T6j) was fixed by renumbering the ISA row I-T6m.
- The ONS FYE 2024 reference tables are read: decile total tax and gross income per household (I-H1k to I-H1t, I-H3k to I-H3t), with Table 2b central and Tables 2c and 13 as the range for the choice of ranking. Published council tax shares replace the derived I-D6a and I-D6h; the published bottom-five share (45.8%) is above the old derived high (43.5%).
- Flagged conflicts for the model stage: published stamp duty (top original-income decile 55.9%, I-D6q) against the derived 21.8% (I-D6f); the ONS allocates business rates wholly to consumers (I-D6o, I-D6p), against the derived owners, workers and consumers split.
- Not met: the non-payer share by income decile (I-H2a). If it means below W_min, it needs WAS Table 2.6, not the ETB. 024r retired.

## 2026-11-16: model v3 design review and stage A2 (brief 011)
- The author accepted the guru's review: policy levers (rate schedule, threshold, retirement order) are swept as named schedules S_low, S_central, S_high plus a feasibility map, not sampled; exogenous inputs are sampled at two levels reported apart (return risk; parameter ignorance, as a tornado).
- The long window (years 51 to 100) is read as a steady-state property, not a forecast; headline claims rest on the transition and short windows and the path to year 50. P4 is read with P6 (fund assets as a share of GDP).
- Added outputs: cash-flow burden by income and by liquid assets (M2b, M2c), a reform-in-place benchmark (M8), capitalisation of retired property taxes as a sensitivity (S1), public wealth path (P6). Manifest: 21 entries.
- New stage A2 sits before the input register; 012r is tiered by `docs/model-v3/drivers.md` and a tornado runs on tier 1 before stage C. Confirmed the same day: retirement trigger, named-schedule choice rule, 0.5-point tornado cut-off. Stage B is brief 012r (four sessions B1 to B4).
- `synthesis.md` section 3 amended (range method, rate function).

## 2026-11-16: model v3 stage A passed (brief 011, stage A)
- Author confirmed all four open items: windows (transition to the long-reserve fill; short = 10 years after it; long = mean of years 51 to 100 and year 100), default retirement order ascending by receipts, M2 revenue-weighted, M3 life length 30 years.
- Six taxes retire; stamp duties carry two receipt lines, so the retired-receipts metric has seven lines. The retirement trigger (first year after the fill in which net relief covers the tax's receipts) is a stated default that follows from P3, not yet confirmed.
- Open checks, not blocking: M2 against the RATES paper's 0.35%; the Green Book discount schedule text. Files: `docs/model-v3/metrics.md`, `docs/model-v3/outputs.yml` (16 entries).

## 2026-11-16: site architecture doc refreshed (brief 004)
- `docs/wdt-site-architecture.md` corrected against the files (root path, tree, preprocess steps, tracked `OUTPUTS`, workflow, issue statuses) and later updated for the `model_v1/model_v2` rename. A path check over its 359 backticked names finds 23 with no file, all generated outputs, externals, things the doc says are gone, or the old root `wdt-site/`.
- Not split: the doc is 32 KB (target about 15 KB). `docs/agents/web.md` names this single file and splitting was outside the brief's `Touches`. Open for the web role if wanted.
- Not checked against the live site; issues were re-checked in code only. Issue 7 (sandbox token) left as is; Issue 16 (revenue calculator) parked until after model v3 (author, 2026-11-16).

## 2026-11-16: audit stage D merged (brief 001c)
- Stage D (v2 complication and tests) reviewed by spot-check and merged: v2 model Python 17,729 lines against v1's 18,136; the growth is the parameter file (1,839 against 554 lines) and unused parts. Three largest sources: output layer 5,150 lines, `valgen_core` 3,353, `eval_core` 2,718 (orphaned).
- The branch lacked stage B (it was built on the stage C commit), so the two stage D files were applied to `main` instead of merging the branch. The audit stages A to D are now complete; stage E (synthesis and v3 requirements) is the guru's and is next.

## 2026-11-16: audit stages B and C merged (brief 001c)
- Stage B (v1 errors against the drift register: 36 confirmed, 4 partly, 1 not reproduced, 1 not checked, 3 new) and stage C (v2 inventory) reviewed by spot-check against the code and merged. Stage D and the synthesis remain.
- Rule from the author: model v1 and v2 are incomplete and incorrect and are not fixed, only learned from. So the B1 question (which C.1 denominator is canonical) is not decided now; it goes to the v3 design (011g). Running list of lessons: `docs/model-audit/lessons-so-far.md`.
- `registry/references.json` and `site/pages/glossary.md` untracked and ignored (the build regenerates both; checked). `registry/contents.yml` stays tracked: the build only syncs it and keeps hand-written titles for headings with maths.
- Author answers: the Zenodo sandbox token is non-critical; the revenue calculator will be replaced after model v3; letter `s` stays; old uploaded skills removed from the account.

## 2026-11-16: model audit and the v3 reframe (brief 001)
- Stages A to D audited v1 (42 register items, 3 new) and v2 (complication, tests). Neither model is fixed; lessons are in `docs/model-audit/lessons-so-far.md`, requirements in `docs/model-audit/synthesis.md`.
- v3 is a range model: three headline outputs (government revenue, taxpayer burden, non-payer savings) as sampled P10, mean and P90, a year-by-year path with a steady-state summary, and the tolerant zone (C.1 over TW(1)) as a supporting output. Papers become one whitepaper plus appendices, rewritten to follow the results.
- Fixed allocation order (refunds, SWF share, relief). Rate schedule sampled over a progressive family. Wealth data: survey plus a rich-list tail. Clean slate, port by exception. Gain ladder, heir rule and strategy verdicts dropped.
- Retired together: CGT, IHT, stamp duties, council tax, business rates, corporation tax, in steps as relief arrives. Headline revenue is the net fiscal effect with every line shown; the corporate levy is its own line. Threshold: half the median house price per adult.
- Closure check on v2 (UK, 117 windows): post-fill relief of about 3% to 15% of GDP against 8.27% of GDP retired; the retired taxes are covered in 42% to 55% of windows. Details: `docs/model-audit/synthesis.md` section 10.
- Next: brief 011g stage A (draft written), then a research brief for the input register.

## 2026-11-15: model folders renamed (brief 010)
- `model/` is now `model_v1/` and `model_new_2/` is `model_v2/`. The build reads `model_v1/` and still writes `_build/model/`, so published URLs (`/model/wdt_core.py`, `/model/WDT_Params.toml`) are unchanged (author's default).
- Site output identical before and after: 157 files, 95 figures. The Action on `main` is green on the tip that contains the rename.
- Open, not fixed here: `site/_quarto.yml` lists `model/rates_model.py` (gone) and `site/tools/revenue_calc.html` fetches it, so the revenue calculator probably fails (architecture doc Issue 16).

## 2026-11-15: output and CI hygiene (brief 003)
- Deleted `check.txt` and `pipeline/check2.txt`; untracked `source/.obsidian/` (files stay on disk); `.gitignore` covers them and future `check*.txt`; removed the "Inspect build output" step from `deploy.yml`.
- Merged with a local Linux build passing (53 pages, 28 `wfr_*` figures) and the Action green on later tips. The build is not `git status` clean: it rewrites `registry/contents.yml`, `site/pages/glossary.md`, `registry/references.json` while the papers are mid-rewrite.
- Open for the author: do those three generated files stay tracked? (Answered 2026-11-16: two untracked, `contents.yml` stays.)

## 2026-11-15: model folder cleanup (brief 006)
- Deleted the four `SS` folders under `model_new_2/`, `model_new_2/test/_backups/` and `model/test/welfare_core.py`, `welfare_tables.py`: 226 tracked files (709 to 483), `model_new_2` 192 to 154 MB. The pack stays 105.83 MiB (history kept).
- The brief's import check was reworded: `python -I` drops the current directory, so it needs `sys.path.insert(0, '.')`. Same intent, not weaker; the author approved the wording fix and the merge. Pattern recorded in `docs/agents/code.md`.
- Core imports resolve in both folders. Not caused by this brief: `wdt_analytics` imports `rates_core` (now `rates_core1.py`), so it fails to import (see `docs/brief-suggestions.md`).

## 2026-11-15: docs and naming housekeeping (brief 008)
- Renamed `docs/WDT JEL Codes.md` to `docs/wdt-jel-codes.md` and the two `Rates Data` xlsx files without `(1)`; they were not duplicates.
- Nothing archived or deleted. Every file directly under `docs/` has an owner in `OVERVIEW.md`.
- One `(1)` name remains (`model_new_2/SS/...`); brief 006c deletes it.

## 2026-11-15: repo triage (brief 002)
- Final cleanup order: 003s, 004s, 005g, 006c, 008g, 010s; then audit 001c; then model v3 design 011g. 007w (crosslinks) waits for the paper rewrite; 009c (retire legacy) waits for v3.
- Kept: data dumps (`wid_out/`, `audit_d0/`) and shared copies. Untrack `source/.obsidian/`. Model folders become `model_v1`, `model_v2` (010s).
- Brief letters: g guru, w writing, c code, r research, s site/web.

## 2026-11-15: tools and skills cleanup (brief 005)
- Deleted `Tools/SS/` (old doc-coauthoring, formatter, laconic, model and reference skills, `web_search.json`); the author had moved them there.
- `Tools/` holds the five role `.skill` files and `repo-scaffold.skill`. Each role file matches `.claude/skills/<role>/SKILL.md` (checked); both locations stay, `.claude/skills/` is the source.
- Still the author's: remove the old uploaded `wdt-*` skills from the claude.ai account.

## 2026-11-15: agent scaffold
- Roles are guru, code, writing, research, web. Skills are repo stubs in `.claude/skills/` that point at `docs/agents/`.
- Formatter and laconic skills folded into the writing role; the co-authoring skill became `wdt-write`.
- The librarian skill was a failed project and is kept only as an archive.
- `SS` ("superseded") folders deleted; history is in git and the author's separate backup.
- Model v1/v2 is legacy; a third refactor starts from a clean slate (brief 001).
- `model/OUTPUTS/` stays tracked; old paper-number references are not being fixed because the papers are being rewritten.

## 2026-11-16: restructure of the series (013g)
The 33 papers are replaced by a hub (general-reader whitepaper, problem first), about 12 spokes and standalone papers (ADD, INST candidates), resting on the v3 data layer. Old papers only guide the new ones. Gate: no spoke prose until the data is finalised. Plan first in five stages (map, ledger, template, site needs, order). Brief 007w becomes obsolete.

## 2026-11-17: briefs are split for parallel work
The guru splits parallel parts into separate small briefs (own number, one lane, one session, disjoint Touches, shared inputs fixed first). Stages are for sequential steps only. Rule is in `docs/agents/brief-template.md` (Splitting) and `guru.md`.

## 2026-11-17: 012r and 013g stage B merged
012r: `docs/model-v3/inputs.md`, 89 rows, 40 judgement; incidence (D6) and the D7 and D8 ranges are derived or from v2 output, not independent evidence. Finding: the RATES 0.35% burden divides by terminal wealth; M2 on start-of-year wealth is about 1.2% on a crude path average, so RATES' claim of staying below 1 to 2% is not shown. M2's denominator is the author's call.
013g stage B: ledger of 980 sections; every spoke exceeds 4,000 kept words (2.6 times overall); outputs.yml `element:` filled with hub and spoke IDs (proposed). Decisions in `ledger.md` section 8 are open.

## 2026-11-17: author decisions on 012r and 013g stage B
M2 uses same-year (start-of-year) wealth; RATES 0.35% is a different quantity. References are to be reworked to only those actually used. Spoke cap 6,000 words; overflow goes to an appendix spoke (suffix -A); S4 and S6 split, ENT becomes S8-A; welfare outputs are added and produced by the v3 run; H1 problem outputs accepted for now; manifest additions accepted; synthetic stress test kept; v1 headline figures not carried. Briefs 014g to 016g define the added outputs in parallel (files under docs/model-v3/added/); the guru merges them into metrics.md and outputs.yml.

## 2026-11-17: 012r retired
Merged and reviewed; the brief moved to `docs/archive/briefs/`. Open items moved: tornado to 011g, references rework to the author's later decision.

## 2026-11-17: spoke template approved; figures framework
The author approved the spoke template (one objection block, 60-word reading note, long value never alone in a short answer, strict lint on typed figures). Figures: every figure has a reference table in the Data block, drawn from the same data; a caption describes and never states a result or a number; no tables in the prose, each table is referenced from its figure's caption. Template section 6a. Stage D builds the lint and renderer.

## 2026-11-17: output definitions merged; stage D and research follow-ups split
014g to 016g merged as files under `docs/model-v3/added/` (21 new or changed outputs, one stress-test check); integration into metrics.md and outputs.yml waits on the author's 12 answers. 013g stage D split into 017s to 021s, each writing one file under `docs/restructure/site/`. 12 research requests across 014g to 016g go to 022r to 024r, each writing one file under `docs/model-v3/inputs-added/`.

## 2026-11-17: author answers on the added outputs
Defaults accepted for: heterogeneous returns by wealth rank as a stated premise (drop OH1a if too costly), OW2 as a post-processing module, gamma sampled at level 2, M3 gains as the real change in net wealth, M4a deciles of all adults with non-payers inside, OW3 as envelope only (concentration is OH1a), the stress test as a check with mean return from I-D1a and amplitude to about 12%, tornado headlines M1, M2, M4a and M3, the hub's wealth-to-GDP basis, 022r to 024r as written, no extra table type. Not default: the consumption tax stays as a comparator in OW1, because it is the WDT's main intellectual competitor; 024r must source consumption to wealth ratios. Agents are kept to one skill: site 2 and 3, research 4 and 5, writing 6.

## 2026-11-17: added outputs integrated
Metrics renumbered into one sequence (M10 to M15b, B1, P7, M7c to M7e, M9, M4c, F1, T1); manifest now 38 outputs and one check (CK1, a test not an output) with data facts DH1a to DH1c; all elements validated against the hub and spoke ids, appendix spokes included. Applied the author's answers (M3 gains, M4a deciles, consumption tax kept in M13, OW3 envelope only, tornado on four headlines). Briefs 014g to 016g retired. Open inputs remain 022r to 024r.

## 2026-11-17 (afternoon): shortcodes, concentration output dropped, stage D accepted
Shortcodes of `shortcodes.md` are the page ids, URLs, front-matter values and figure ids; the S numbers are planning labels read through `docs/restructure/ids-map.md`; the `-A` suffix retires; S11 splits into FIRST and WIDER and S12 into UNCER, LIMIT and FALS. OH1a and M10 are dropped: the concentration path needs returns that rise with wealth rank and 022r found no UK evidence; OW3 is by wealth band, not return tier. All proposed answers in 017s, 018s and 020w are accepted; nothing outside the repo reads `site-index.json`. `outputs.yml` gained unit tags, decimals, per-output horizons, `by` value maps and series flags. 022r and 023r retired.

## 2026-11-17: four calls
S11 and S12 output assignments kept (FIRST, WIDER, UNCER, FALS; none to LIMIT). Brief 007w dropped as obsolete. Retired-tax receipts take the primary source as central with the IFS sheet as cross-check (CGT 24.2bn HMRC against 19.5bn IFS), written into M1e. Brief 025w (ledger and map to shortcodes) written for the writing lane.

## 2026-11-17: spoke checker questions (020w)
Q1 question is the title; Q2 H3 allowed inside Evidence sections only (PT7 amended; H3 is not a section address); Q4 draft downgrade accepted; Q18 waivers of warnings accepted. The remaining 020w questions were accepted under the author's blanket approval and stay open to review.

## 2026-11-17 (evening): ledger in shortcodes (025w), navigation (021s)
025w accepted: POL splits into POL, ADOPT and PILOT and FALS into FALS and HYPO (working names); UNCER and LIMIT M rows count as kept at stage E; payslip stays in PAY. `outputs.yml` `element:` amended so the FAL claims sit in FALS (O1, O2, O4a, O5, O6, OP6, OW1) and OW3 lists WELF only. 021s merged with the author's 12 answers (`docs/restructure/site/nav.md` section 10): flat navbar, 15 menu spokes and 4 parent-reached, old calculators and pending pages stay live labelled as the old model. The stock-wealth floor hypothesis (`docs/model-v3/stock-floor-hypothesis.md`) is exploratory and not adopted; discussion with the author first.

## 2026-11-17 (night): tornado, 028r, site.md approved
**Tier 1 tornado** (`docs/model-v3/tornado.md`): the mean return dominates (swing 8.8 points of GDP on M1), central M1 is +1.45% of GDP and turns negative below a return of 3.55%. **Retired total corrected to 8.11% of GDP** (the stamp-duty row contains the shares line; 8.27 double counted); corrected in `drivers.md` and `metrics.md`, and a correction note added to `synthesis.md` section 10 (its v2 closure results are at the old total and are not recomputed). **Revenue identity uses the arithmetic mean return** (about 4.76%) for g; paths compound at the geometric rate (author); stage C writes it in. **028r accepted**: non-payer share by income decile merged into `inputs.md` as I-H2a1 to I-H2a10 (269 rows), labelled as household deciles. **`site.md` approved** with all eight proposed answers: drafts under `/draft/`, hub Data block, ADOPT, PILOT, HYPO reached from their parents, `source/hub.md`, pending-page links rewritten to `retired.html`, glossary seeding allowed before the gate, standalones move after the gate. Build briefs B1 to B16 wait for `order.md`.

## 2026-11-17 (night): order.md approved, restructure plan complete
All ten proposed answers accepted (`docs/restructure/order.md` section 9): the order of 26 pages in six waves; the whole gate G1 to G5 for every page, no early start; no optional split now (trigger: compressed Evidence over 5,400 words in a first draft); WELF concentration claim to UNCER, comparison-tables page and avoidance guide folded; 21 grouped writing briefs plus a cross-link pass; hub cap 6,000; `source/data/` for DL4 and DL6; HYPO lists O1, O4a, OP6, OW1 and FALS keeps O2, O5, O6, CK1 (applied to `outputs.yml`); the gate uses the `(J)` flag. Judgement rows reconciled to 87 (the register's prose said 84 and 70 were flagged: 17 prose-listed rows were unflagged and are now flagged, three bracketed rows of 028r added). Brief 013g (restructure, stages A to E) and 026g are retired. First parallel build briefs written: 029s, 030c, 031s, 032r, 033c, 034c.

## 2026-11-18: model v3 stage C1 decisions (brief 035g; `docs/model-v3/stage-c-decisions.md`)
One mean return throughout: the geometric mean (supersedes the 2026-11-17 note that the identity takes the arithmetic mean; the author wants the fewest assumptions). The model never clips M1, uses one sign convention (receipt positive), reports the share of paths with M1 below zero per horizon, and the break-even return becomes an output (proposed ids `M1f`, `O1e`, `O1f`; awaiting approval). Epsilon is computed by the model from the named schedule; the revenue identity is a check, run by reproducing v2's 7.34% at v2-like inputs within a tolerance (039g). Payer-level state per path carries the refund cap. D5 behavioural response is a level 2 draw; D10 capitalisation is a switch, off in the headline. Seed fixed and recorded; 2025-26 prices; sample size from a convergence test. Item 4 (replay or sampled paths) waits for 036r.


## 2026-11-18: return model, refund rule, merges
Author, on 036r: generator is an AR(1) with normal innovations (arithmetic mean 4.742%, SD 8.219%, lag-1 0.30) with a block bootstrap as cross-check; pool all years; war years a named sensitivity (+0.5 points). **Mean basis (revised):** arithmetic in the generator and the identity check, geometric (4.42%) quoted as the holder's return; supersedes the geometric-throughout answer of 2026-11-17. Refund rule tau x loss (the papers'); envelope resets at death (v2); `logistic_ln_ref` not run. 029s accepted (ids `old-<stem>`, 15 menu labels); 031s merged with the revenue calculator left broken (Issue 16). Merged 029s, 030c, 031s, 037c. Register 274 rows (036r rows applied); manifest units fixed (`stage-A7-units-2026-11-18`). Briefs 041r and 042r written. Items recorded in `docs/model-v3/stage-c-decisions.md`.

## 2026-11-18: architecture approved, return sample ends 2019
Author approved `docs/model-v3/architecture.md` (039g): section 9 defaults 1 to 9 as written and section 8.1 amendments A1 to A7 (stage V3-0 applies them). On 042r: the v3 return sample ends in 2019 (JST R6 wealth return); no splice; the missing 2020 to 2025 is stated in UNCER with 042r's bracket (mean 4.37 to 4.70) as the sensitivity; a later licensed series is a future update. JST R6 is CC BY-NC-SA 4.0 (042r), a licence notice is a writing item. 041r: both epsilon treatments carried in the tornado; the model computes epsilon (C1 item 3), so held or recalibrated is moot.

## 2026-11-18: file layout
Author: a vertical tree with four areas plus root files (`model/` with v1, v2, v3 and the model data; `research/` with sources and notes; `web/` with site, pipeline, registry and page tests; `docs/` with the status files, briefs, agents, archive and skills). Old papers (`source/`) go to `docs/archive/papers/` once the hub and spokes replace them. The move runs after the v3 build (brief 044c, parked); until then all briefs use today's paths. Design: `docs/restructure/file-layout.md`.

## 2026-11-18: acceptance plan approved
Author approved `docs/model-v3/acceptance.md` (040g D1) with Q1 to Q6 as proposed: `accept.sh` and `test_converge.py` join V3-12 (test budget 3,020); convergence thresholds 0.10 and 0.15 on spreads, 0.05 on doubling, 0.10 at level 2; unfilled-path ceiling 5%; no time cap on `accept.sh`; acceptance includes a full provisional run; P9 reads the register count from `inputs.md`. D2 follows.

## 2026-11-18: model v3 build briefs approved
Author approved the 13 build briefs 045g to 057c (040g D2) with two fixes for Agent 4 before merge: `docs/decisions.md` added to 057c Touches; the empty `__init__.py` files for `core/`, `runner/`, `out/` and `pack/` created by 046c. First wave 045g, 046c, 049c on Agents 2, 3 and 6. 050c re-derives its pinned return statistics on the 2019 sample and reports; a difference from the register (4.742, 8.219) stops for the author.

## 2026-11-18: feasibility constants (A5)
Author: a schedule is feasible when retired receipts never exceed revenue in at least 75% of level 1 return paths, mean payer burden M2 is at most 2.0% of wealth a year, and non-payers' overall saving M4a is at least 0%. S_central is the feasible point with the highest closure share under the cap; S_low and S_high are the edges of the feasible region. If no schedule is feasible the map reports the best achievable closure share and the run says so. Set in `outputs.yml` by 045g.

## 2026-11-18: pack hash error message (P2) and pack mappings
Author accepted the weaker reading of P2: a changed pack byte fails on the file sha256 and names the file; row and column are added only when the file also breaks its schema. A per-row hash was not adopted. `architecture.md` P2 and P9 and the 047c brief now say so; P9 compares the register row count with `inputs.md` at test time (274 today). The part-of, group and X1 pointer mappings that `core/pack.py` takes from its caller are written by brief 048c into `model_v3/levers.json` (`pack_mappings`).

## 2026-11-18: register corrections from the source check
Author: the central workers' share of corporation tax is 51% (held ifo WP 241, pp. 5, 6, 19), not 40% (that was the capital share); I-D6c and I-D6j change by the row's own rule. I-M6l's figures are replaced by those in the held OxREP article (Advani, Hughson, Summers). Applied by 059r; dependants (tornado, drivers) are listed in its report for the guru. Site tooling briefs B3, B7, B8, B10, B14 written as 060c, 061s, 062s, 063s, 064s.

## 2026-11-19: review of the first site tooling and the UK pack
Author: the five receipts rows I-T3d, e, g, m, p keep low and high as the OBR sheet's neighbouring-year columns (not bounds); the pack stores them as given. Glossary owner of "retired taxes" is FISC. The Short answer limit stays 150 words although it does not fit a 360 by 640 phone fold with the current header. Guru: the break-even return is the arithmetic mean (M1f); the tornado is not rerun after the 51% workers' share because the v3 tornado (055c) supersedes it; CK1 gets `lines` (065g).

## 2026-11-19: base inputs
Author: the pack is extended before the base is built (wealth in pounds, adult and household counts, median house price from the ONS file the author uploads, GDP): brief 067c. The route mix is adopted from the v2 baseline D13 (A 50, B 25, C 8, D 17 of initial value; Route C range 5 to 10 with A absorbing; Route B paid by sale) as new judgement rows pending in G3: brief 068g. Both were gaps in architecture.md (2.3 said "register values" and no rows existed); 051c waits on both.

## 2026-11-19: revenue stage inputs
Author: verification hazards lambda_C and lambda_D 5% central, range 0 to 10% (v2 headline framing value; judgement rows). Guru: the corporate levy M1b reads the register's I-D7a (2.82% of GDP) as a constant share; consumption 3.5% and the fund settings (a_window 5, horizon 10, safe_share 0, reference year 2019) are v2 defaults entered as judgement rows (071g); real GDP per head and the reference expenditure over GDP come from JST into the pack (070c). The base uses deciles, so within-decile spread is not seen by the kernel: a limit for the papers and a reason the identity I1 may miss.

## 2026-11-19: base tail and identity I3
Author: the v3 base adopts v2's top-tail construction (survey shares, Rich List tiers, Pareto split) because an 11-line base reproduces 3.5% of GDP against v2's 7.34% (effective rate 10.2% against 24.5%). Identity I1 passes v2's own tail constants as test constants; the model uses register rows (072g adds Pareto alpha and tier cuts, framing values from v2; 073c builds the tail). I3 is the exact decomposition: assessed tax equals eps g omega; M1a equals in-life tax minus refunds plus death-time and heirs' assessments. Paper sentence "M1a is about eps g omega minus refunds" holds for in-life assessment only.

## 2026-11-19: I1 and I2 gap
Author: with v2's own tail the port check still gives 5.02% of GDP against 7.34 (I2 4.97, floor 6.34). Diagnose first (074c: one v2 input at a time, no fix) and hold 052c until I1 and I2 pass; 053c and 054c wait. Loosening the limits was offered and not chosen.

## 2026-11-19: closing I1
Author: after 074c the identity tests take v2's inputs as test constants (W_min, GDP, adults, the 41-cell table, GDP-per-head growth); the model keeps the pack. v2 is run once and its per-window output and cell table recorded as a fixture (078c) to locate the last 0.68 points; I1 stays strict. A band for I1 and a hunt from the spec were offered and not chosen. 052c merges only when I1 passes.

## 2026-11-19: the statistic behind 7.34
The v2 reference run (078c) shows the recorded 7.34 is the mean over the 117 windows of the net post-fill take (ratio of sums, fill to fill+9, no levy); the median is 6.59. The v3 identity tests compare the mean (guru correction; architecture.md and acceptance.md updated). The I1 limit stays 0.02 and I2's band 6.34 to 7.36, both on the mean. Earlier median-based gaps (5.02, 6.66) are superseded.

## 2026-11-19: I1 and I2 restated
Author: v3 learns from v2, it does not replicate it. I1 is the exact-take port check at v2's fill year (passes: 1e-5 in all 117 windows); I2 is the refund-rule difference at v2's fill year, in 6.34 to 7.36; the fill-year difference (39 of 117 windows, +0.17 on the mean) comes from v3's constant levy against v2's per-year path and is reported as a finding, not a failure. 052c merges when its tests pass on this basis. Paper question: does a constant levy understate how much the fund's timing varies.

## 2026-11-20: burden metrics (053c)
Author: M2 is reported in life as the headline and including death flows as M2d (labelled; death flows are 87% of M2); M5 compares in life. M3 gains are the positive real changes in net wealth. M4a incidence is a stated limit of the pack. OH1b all-tax line, M8 non-payer saving and M2b/M2c below W_min are not built and listed as limits of the first run. Manifest entry for M2d: brief 079g.

## 2026-11-20: M7e
Author: the first provisional run goes without M7e (modal declaration): no distribution of declared alpha is held (M-3). OD1 reports M7c and M7d; O7 uses the curve only. Brief 080r looks for the evidence for a later run. Process note: a data gap marked MISSING in a design file must be turned into a brief before the stage that needs it is assigned.

## 2026-11-20: check of MISSING flags in the design files
The MISSING flags in `added/supporting.md`, `h1.md` and `welfare.md` (written 2026-11-17) were answered by the 022r to 024r research: every request has register rows (coverage tables in `inputs.md`). Open after that, all stated in the register: M-3 declared alpha (I-W9a to I-W9e foreign, no distribution; first run goes without M7e, 080r); null rows I-H4b (employee NICs of likely leavers), I-H7c and I-H7d (spending to wealth in the middle bands), I-T6k and I-T6l (business relief share): none is read by the runner; they are needed only by the consumption-tax comparator and finer M9 and M14 forms. Partly-met rows (return by rank, saving by band, mobility, investment income, accrued gains, realisation, exempt shares) rest on foreign or judgement figures and are (J) rows in the tornado.

## 2026-11-20: M7e dropped; the alpha 1.1 claim retracted
Author, after 080r: M7e (modal declaration) is dropped from the metrics and the manifest (it reads 1.00 on the OD1 grid for any centre between 0.875 and 1.125); OD1 keeps M7c and M7d, O7 keeps the tolerant zone; no register rows for a declared-alpha distribution. The old papers' behavioural centre near alpha 1.1 and the "mild-overstatement equilibrium" are retracted as findings (model-implied from the refund asymmetry, unsourced, untested; a centre above 1 also follows from owners overestimating their homes). Brief 081g (manifest). The old papers and site pages are not edited (author: they are rewritten from the ground up); the guru ledger and `framework.md` carry the retraction so the rewrite does not repeat the claim. Brief 082w was written and removed.

## 2026-11-21: stage, physical wealth and register fixes after 101r and 102r
Author: (1) stage is the person's economic status (the held WAS table) as a proxy; the household reference person's status is requested from the WAS household file. (2) Physical wealth (contents and vehicles) is inside the WDT base as a separate asset class, not merged into the other classes. (3) I-D4a, I-D4b and I-D4h are corrected to the numbers with a citation: I-D4h low becomes 1.86 (Table 2.13), I-D4a and I-D4b values stay with corrected caveats (brief 105c); the I-D4b central is not recomputed and stays an open question.

## 2026-11-21: rulings after 103r (accounting)
Author: (1) Pension accrual runs as one labelled aggregate scenario on the ONS basis; no rate is formed on the WAS SCAPE stock until the ONS reconciliation (SUP-3) arrives. (2) Classes with no held return (pension, physical, net financial) are credited a labelled scenario range per class, never an estimate. (3) The wealth roll-forward residual O is a reported residual, not forced to zero; the survey (WAS) stays the stock base and national accounts are validation only. (4) Two deflators are kept and labelled: CPI for real returns, the ONS household consumption deflator for liability erosion; 104r lists where each is used. Housekeeping by the guru: F-03 is labelled `T_C` not `TR`, F-21 is a `CG` term not `O`, and I-W3b is context only (applied in 104r's conventions; no registry edit yet).

## 2026-11-21: I-D4b refit, adult age, I-W3 citations
Author: (1) The I-D4b central is refitted with I-D4h's 1.93 adults per household (brief 106c). (2) Adult means 16 and over, as held; the 18-plus split is a request to the WAS microdata. (3) I-W3c and I-W3d stay validation moments marked unverified until the source PDFs are uploaded (SUP-7).

## 2026-11-21: I-D4b refitted; I-D4c to follow
Brief 106c refitted the I-D4b central to 52.4% (adults per household 1.93, one scale factor 1.0934 on the assumed counts). Author: refit I-D4c the same way as its own brief (107c), stopping for review if any model digest moves.

## 2026-11-21: 104r rulings; build starts
Author, on 104r: (1) Convention A (credit the holding gain; saving carries the retained yield once), B as an equivalence check; double counting is a failing test. (2) Settlement: the first implementation settles from net financial wealth only and reports the shortfall by cell; the order of other sources stays unset. (3) Public side: one public ledger by class at market value; the fund balance and its return are read from it. (4) Stage within band: the labelled person-based proxy; no microdata is commissioned (no UKDS licence). 104r questions 4 to 8 taken at their recommendations: add register rows for the scenario ranges (unset until the author sets a range), no cross-cell transfers (TR = 0), the deflator wedge reported inside CG, gross saving reported only as an upper bound while CFC is unset, the pension basis reconciliation stays open. Research is closed for now; build order: 108c household step, then pack additions, the public ledger (kernel and revenue), cell wiring, validation, comparison. 089c and 057c stay held.

## 2026-11-21: settlement ruling replaced
Author, after discussing the liquidity gap: the earlier ruling (settle from net financial wealth only, report the shortfall) is withdrawn. It left tax unpaid in most cells and is not the tax's mechanism. Settlement uses the existing kernel routes (I-D13a to I-D13e): the payment is taken pro rata across the non-pension classes (property, net financial, physical); pension stays in the base but is not sold (illiquid until drawn); Route D keeps its lien. Liquidity pressure is a reported diagnostic per cell (payment as a share of net financial and of non-pension wealth, and cells where it exceeds net financial wealth).

## 2026-11-21: scenario return ranges
Author: the pension and net financial real return ranges are the JST market-portfolio real total return across the two held regimes (low 1947-79, high 1980-2019; 1896-2019 mean as reference only); physical wealth is held at 0% real, labelled an assumption; pension accrual is one aggregate range from the 1998-2025 min and max of D.8 over opening net worth. All are judgement rows, never estimates (brief 109c). 107c and 108c merged the same day (I-D4c 91.5%; `household_step` exists, not wired).

## 2026-11-21: first cell run inputs
Author: saving by cell is one uniform ratio (the ONS non-pension saving ratio, min, median and max of 1998-2025), no wealth gradient; income by band from I-D9a to I-D9d for all stages, with D1-3 at the D4-5 low bound and retired cells at a labelled retired fraction (held source if any, else 0.6, range 0.4 to 0.8). First run is untaxed and standalone (brief 110c); validation against the 099r moments follows. 109c merged (I-D1h to I-D1k, pack v2).

## 2026-11-21: 110c income gap
Block 1 found cell income (I-D9 band means times households) 19.5% below ONS B.6g, while the saving ratio is a national-accounts ratio of B.6g. Author: scale every cell's income by one factor to the B.6g total, keeping band proportions and the retired split; label the run aggregate-constrained; keep the unscaled run as a sensitivity.

## 2026-11-22: pension accrual on income
110c (untaxed cell baseline, merged) found wealth over GDP at year 100 of 0.85, 2.04 and 9.9 across the three return regimes (median saving), and that the path is set by the pension accrual label (I-D1k, a share of opening net worth: 1.12% mid-point, 2.7 times today's ONS D.8). Legacy untaxed is 0.61 at year 100. Author: base the accrual on income (D.8 over B.6g), central the observed 2024 value, range the 1998-2025 min and max, no mid-point label; scale cell income to B.6g and rerun (brief 111c, merged: I-D1k 3.01 / 4.83 / 9.74, income factor 1.3733, wealth over GDP at year 100 0.75 / 1.29 / 4.42 across return regimes, legacy 0.61, no cell goes negative). The 1.12% net-worth basis and the 2.04 and 9.9 figures of 110c are withdrawn. The branch `brief/110-cell-baseline-run` (a parallel earlier attempt, blocks 0 to 2) is superseded by the merged run and is not to be merged.

## 2026-11-22: D.8 base accepted; wiring design next
Author: D.8 over B.6g is accepted as the net national pension flow, applied by income to every cell for now; a labelled withdrawal scenario comes later with the aggregate held to D.8. Next step is a wiring design brief (112r) before the code, because taxed runs need the household step inside the kernel's payer lines, not a band mean.

## 2026-11-22: kernel wiring design rulings (112r)
Author: Q4 payment above non-pension wealth is capped and the excess reported (`unpaid_B`), counted as a model alarm: WDT is a tax on the change in net worth at a marginal rate below 1, so the payment cannot exceed the change in net worth; it can only exceed non-pension wealth if the gain sits in pension (illiquid, not sold) or a position is inconsistent, and a non-zero count in a standard run means the model is wrong, not that the schedule is extreme. Q5: M3, M12 and M13 are withheld and labelled `legacy_only` under the household arm until a comparator brief. Q7: a new `runner/arm.py` module (about 140 lines, tests 210), `kernel.py` budget raised to 660, `runner.py` stays at 360. Q3: tail lines carry the D10 mean income at multiple 1; scaling to B.6g is a separate switch, off by default. Q1, Q2, Q6, Q8, Q9, Q10 taken at 112r's recommendations (stage as a label, decile class shares, a hook object built by the runner, three saving values as a scenario axis, legacy the default arm, the corporate levy as cash under the fund rule). Build order W1 to W7 in `docs/model-v3/kernel-wiring-design.md` section 4; W1 is brief 113c.

## 2026-11-22: decile mix and the debt return
Author: the decile class mix is confirmed as held (WAS Table 2.2 shares of net wealth, net of debt, negative shares included; D1 net financial -104.92%). Negative net positions earn 0% real in the household step (a labelled assumption: debt interest roughly equal to inflation); the debt-rate range stays unset. D10b and the tiers carry the D10 mix, labelled. W1 (113c) and W2 (114c) merged; W3 is 115c.

## 2026-11-22: W4 merged; W5 split
W4 (116c) found the design note wrong on one point: the sale routes did not cap payments at holdings (`_div` only guards a zero divisor); W4 added the cap and `unpaid_B` reporting (no legacy run triggers it: max 0.0 over 90 books). W5 is split into W5a (117c, the household hook with T = 0, equivalence with the cell baseline) and W5b (the taxed hook, the `out_*` call sites and the per-line account table for the author's review).


2026-11-22 Author: tail-line pension. The 118c account table showed RL1 to RL3 unable to pay in year 69 because they held D10's pension share (37%) of very large wealth. Ruling: tail lines hold pension as an absolute amount per adult, capped at the D10 mean pension (WAS Round 8). Labelled scenario, to be challenged with better data (p90/p99 of private pension wealth or a lifetime-allowance figure); displaced wealth goes to the other three classes pro rata. Brief 119c. Settlement rule unchanged.

2026-11-22 Author: review of 119c. I-D1l stays an opening-stock allocation assumption (starting stock only; accrual and gains continue above it); no running cap, because a cap needs a rule for contributions above it and there is no data. A better tail pension distribution (p90/p99 or a lifetime-allowance figure) is on the data wishlist, not a research phase. Pension withdrawal stays zero for the first integrated run and is a mandatory labelled sensitivity before any long-run claim. Death and terminal payments are reconciled in the year they occur (W6 acceptance). The 118c/119c account is a diagnostic of 14 lines alone, not an aggregate revenue run. W6 proceeds as brief 120c.
