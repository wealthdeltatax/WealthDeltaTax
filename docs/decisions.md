# Decisions digest

One entry per finished brief or settled question, at most 8 lines each. Newest first. Maintained by the guru.

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
