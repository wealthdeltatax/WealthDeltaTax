# Decisions digest

One entry per finished brief or settled question, at most 8 lines each. Newest first. Maintained by the guru.

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
