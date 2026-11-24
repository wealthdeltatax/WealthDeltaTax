# File layout map (044c R1: inventory, nothing moved)

Written by `pipeline/path_refs.py --map` from the tracked files at `817dccc` (the merged state of 009c). The rule table is `RULES` in that script; 
the per-file table is `file-layout-map.csv` (old, new, flag, rule, rename, duplicate_of); the references and the depth-based paths are `file-layout-references.csv` and `file-layout-depth.csv`. 
Flag **S** = settled by the author's rules, **D** = a default that stays open at the L1 checkpoint (the review table below). After each stage `python pipeline/path_refs.py --check` must report no old path of the moved areas.

**1096 tracked files**: 384 settled, 712 default, 0 without a rule; 78 renamed under R3; 8 byte-identical copies removed under R4; 2471 lines name an old path, in 330 files; 472 lines build a path from their own location.

## Review table (the checkpoint: the guru and the author decide before 160c and 161c start)

| # | Case | Default in this map | Why / what is open |
|---|---|---|---|
| 1 | Loose plans and notes | `docs/navigation_suggestions.md` to `website/notes/`; `docs/EVAL_PLAN.md`, `VAL_*.md` to `research/legacy-model-plans/`; `docs/wdt-jel-codes.md` to `research/`; `docs/wdt-site-architecture.md` to `website/` | the guru defaults of 044c; `project/notes/` was named for "the loose plans" and is the alternative for the first and fourth |
| 2 | Site design notes in `docs/restructure/` | every file except `file-layout.md` (and the new map files) to `website/notes/` (ids-map, ledger, ledger-sections, map, order, shortcodes, site, template, pages/, site/) | they describe the site build, so they follow the site; `project/restructure/` is the alternative |
| 3 | Research study outputs in `docs/research/data/` | folders 097r, 098r, 129r (source tables) to `data/uk-wealth-tables/`; the others (099r to 104r, 131r, 145r, 146r): csv to `results/<NNNr>-<slug>/`, scripts to `model/studies/` | R2 makes datasets one branch and model outputs another; the derived tables of the parameter map are outputs, not source datasets. Open: whether they belong in `data/` (they feed the input register) |
| 4 | Readable copies | `docs/research/readable/` (40 files incl. `data/097r`, `098r`, `129r` copies of workbooks) to `literature/readable/` | the target tree puts `readable/` in `literature/`; the workbook copies are of datasets, not papers |
| 5 | Workbooks in `Research/` | `etbreferencetablesfye202324final.xlsx`, `medianpricepaidforadministrativegeographiesexisting.xlsx` to `data/uk-source-workbooks/` | they are datasets, not PDFs (R2) |
| 6 | Split of `docs/model-v3/` | 24 spec files to `model-specs/`; 11 reports with their folders to `results/<study>/`; 12 study folders as listed in the CSV; scripts to `model/studies/<study>/`; `added/` and `inputs-added/` to `model-specs/` | borderline: `i1-gap.md`, `kernel-wiring-design.md`, `returns-gap.md`, `returns-method.md` (kept as specs); `cell-baseline/inputs_used.json` is read by `run.py` as an input (kept in `results/cell-baseline/`) |
| 7 | Split of `pipeline/` | web and build scripts to `website/build/`; `build_inputs`, `build_metrics`, `validate_outputs`, `run_suites`, `check_gate` to `model/tools/`; `check_agent_docs`, `build_skills`, `path_refs` to `project/housekeeping/` | the target tree has no folder for project tools; `run_suites.py` and `check_gate.py` serve both sides |
| 8 | Split of `registry/` | `inputs.json`, `inputs-display.yml`, `metrics.json` to `data/input-register/`; everything else (pages, glossary, crosslinks, references.bib, internal.json, ...) to `website/registry/` | `references.bib` and `internal.json` are the research database; `literature/` is "the PDFs only", so they stay with the registry unless the author says otherwise |
| 9 | Country pack | `model_v3/pack/GBR/*` to `data/country-pack-GBR/` (target tree); `build_gbr.py` stays in `model/model_v3/pack/` | the loader reads the pack by fixed file names under a path the code passes: 162c rewrites the path; the pack's `source/jst_r6.json` is byte-identical to `data/jst/jst_r6.json` (R4) but the manifest names it |
| 10 | Test suites | `data`, `gate`, `model_v3` to `tests/model/`; `cards`, `glossary`, `layout`, `nav`, `pages`, `retired`, `hooks` to `tests/website/` | the target tree has two folders; `hooks` tests the agent-doc and format hooks and could be `tests/project/` |
| 11 | Agent guide names | `docs/agents/research.md` is renamed `agents-research.md` (it collides with the site page `research.md`); `code.md`, `guru.md`, `web.md`, `writing.md` keep their names | R3 would also call `code.md` generic; renaming all five (`agent-code.md`, ...) touches the skills and every brief that names them |
| 12 | Generic names that are unique | listed in the section "Generic names that remain" below | R3 names `check.py`, `tables.md`, `report.md`; a module renamed changes every import (`config`, `tools`, `hooks`, `pdf`, `transforms`, `common`): the stage that owns the file decides |
| 13 | Pinned files that name an old path | see the section "Files whose bytes are pinned" below | moves keep bytes; rewriting a path inside them changes a hash or a digest. Needs the author: keep the stale citation, or re-pin on the author's word |

## Old area to new area

| old area | files | | new area | files |
|---|---|---|---|---|
| `docs` | 740 | | `results` | 213 |
| `tests` | 126 | | `project` | 197 |
| `site` | 53 | | `data` | 132 |
| `model_v3` | 45 | | `website` | 131 |
| `pipeline` | 34 | | `tests` | 126 |
| `source` | 33 | | `model` | 97 |
| `Research` | 20 | | `literature` | 62 |
| `registry` | 13 | | `research` | 54 |
| `Rates Data` | 7 | | `papers` | 33 |
| `Tools` | 6 | | `model-specs` | 31 |
| `.claude` | 5 | | `.claude` | 5 |
| `data` | 4 | | `.gitattributes` | 1 |
| `.gitattributes` | 1 | | `.github` | 1 |
| `.github` | 1 | | `.gitignore` | 1 |
| `.gitignore` | 1 | | `AGENTS.md` | 1 |
| `AGENTS.md` | 1 | | `CNAME` | 1 |
| `CNAME` | 1 | | `README.md` | 1 |
| `OVERVIEW.md` | 1 | | `robots.txt` | 1 |
| `README.md` | 1 | | `` |  |
| `START_HERE.md` | 1 | | `` |  |
| `STATUS.md` | 1 | | `` |  |
| `robots.txt` | 1 | | `` |  |

## The rules, with one example each

| rule (regex on the old path) | files | flag | example old | example new |
|---|---|---|---|---|
| `^(\.github/.*/\.claude/.*)$` | 6 | S | `.claude/skills/wdt-code/SKILL.md` | `.claude/skills/wdt-code/SKILL.md` |
| `^(README\.md/AGENTS\.md/CNAME/robots\.txt/\.gitignore/\.gita` | 6 | S | `.gitattributes` | `.gitattributes` |
| `^(STATUS/OVERVIEW/START_HERE)\.md$` | 3 | S | `OVERVIEW.md` | `project/OVERVIEW.md` |
| `^Rates Data/(.*)$` | 7 | S | `Rates Data/7.1_260716_Rates_Data_Tables.xlsx` | `data/rates/7.1_260716_Rates_Data_Tables.xlsx` |
| `^Research/(.*\.pdf)$` | 18 | D | `Research/1-s2.0-S0014292125001266-main.pdf` | `literature/1-s2.0-S0014292125001266-main.pdf` |
| `^Research/(.*\.xlsx)$` | 2 | D | `Research/etbreferencetablesfye202324final.xlsx` | `data/uk-source-workbooks/etbreferencetablesfye202324final.xlsx` |
| `^Tools/(.*\.skill)$` | 6 | S | `Tools/repo-scaffold.skill` | `project/skills/repo-scaffold.skill` |
| `^data/(jst/.*/wid/.*)$` | 4 | S | `data/jst/jst_r6.json` | `data/jst/jst_r6.json` |
| `^docs/(EVAL_PLAN\.md/VAL_[^/]*\.md)$` | 3 | D | `docs/EVAL_PLAN.md` | `research/legacy-model-plans/EVAL_PLAN.md` |
| `^docs/agents/(.*)$` | 26 | S | `docs/agents/README.md` | `project/agents/README.md` |
| `^docs/archive/briefs/(.*)$` | 143 | S | `docs/archive/briefs/001c-model-audit.md` | `project/briefs/done/001c-model-audit.md` |
| `^docs/archive/friction-log-archive\.md$` | 1 | D | `docs/archive/friction-log-archive.md` | `project/agents/friction-log-archive.md` |
| `^docs/archive/wdt-librarian\.skill$` | 1 | D | `docs/archive/wdt-librarian.skill` | `project/skills/wdt-librarian.skill` |
| `^docs/audit/(.*)$` | 1 | S | `docs/audit/scaffold-2026-11-15.md` | `research/scaffold-audit/scaffold-2026-11-15.md` |
| `^docs/(decisions\.md/todo\.md/lane-plan\.html/brief-suggesti` | 4 | S | `docs/brief-suggestions.md` | `project/brief-suggestions.md` |
| `^docs/briefs/(.*)$` | 8 | S | `docs/briefs/044c-file-layout-move.md` | `project/briefs/open/044c-file-layout-move.md` |
| `^docs/housekeeping/(.*)$` | 2 | S | `docs/housekeeping/README.md` | `project/housekeeping/README.md` |
| `^docs/hypotheses/(.*)$` | 4 | S | `docs/hypotheses/empirical-household-flow-parameter-map.md` | `research/hypotheses/empirical-household-flow-parameter-map.md` |
| `^docs/model-audit/(.*)$` | 13 | S | `docs/model-audit/change-report-household-resilience.md` | `research/model-audit/change-report-household-resilience.md` |
| `^docs/model-lessons/(.*)$` | 3 | S | `docs/model-lessons/drift-register.md` | `research/model-lessons/drift-register.md` |
| `^docs/model-v3/([^/]+)$` | 35 | D | `docs/model-v3/acceptance.md` | `model-specs/acceptance.md` |
| `^docs/model-v3/([^/]+)/(.*)$` | 192 | D | `docs/model-v3/added/h1.md` | `model-specs/added/h1.md` |
| `^docs/navigation_suggestions\.md$` | 1 | D | `docs/navigation_suggestions.md` | `website/notes/navigation_suggestions.md` |
| `^docs/research/([0-9]{3}r-[^/]*\.md)$` | 29 | S | `docs/research/012r-b1-derivations.md` | `research/notes/012r-b1-derivations.md` |
| `^docs/research/data/([0-9]{3}r)/(.*)$` | 192 | D | `docs/research/data/097r/Collated_Tables_3_1_to_3_11_2324.ods` | `data/uk-wealth-tables/097r/Collated_Tables_3_1_to_3_11_2324.ods` |
| `^docs/research/readable/(.*)$` | 40 | D | `docs/research/readable/INDEX.md` | `literature/readable/INDEX.md` |
| `^docs/restructure/(file-layout\.md/file-layout-map\.md/file-` | 1 | S | `docs/restructure/file-layout.md` | `project/restructure/file-layout.md` |
| `^docs/restructure/(.*)$` | 39 | D | `docs/restructure/ids-map.md` | `website/notes/ids-map.md` |
| `^docs/wdt-jel-codes\.md$` | 1 | D | `docs/wdt-jel-codes.md` | `research/wdt-jel-codes.md` |
| `^docs/wdt-site-architecture\.md$` | 1 | D | `docs/wdt-site-architecture.md` | `website/wdt-site-architecture.md` |
| `^model_v3/(.*)$` | 32 | S | `model_v3/__init__.py` | `model/model_v3/__init__.py` |
| `^model_v3/pack/GBR/(.*)$` | 13 | D | `model_v3/pack/GBR/NOTICE.md` | `data/country-pack-GBR/NOTICE.md` |
| `^pipeline/(.*)$` | 34 | D | `pipeline/bib_to_json.py` | `website/build/bib_to_json.py` |
| `^registry/([^/]+)$` | 13 | D | `registry/contents.yml` | `website/registry/contents.yml` |
| `^site/(.*)$` | 53 | S | `site/_quarto.yml` | `website/site/_quarto.yml` |
| `^source/(.*)$` | 33 | S | `source/10_Behavioural_Robustness_and_Administrative_Experience.md` | `papers/legacy/10_Behavioural_Robustness_and_Administrative_Experience.md` |
| `^tests/([^/]+)/(.*)$` | 126 | D | `tests/cards/test_cards.py` | `tests/website/cards/test_cards.py` |

## Duplicates (R4)

Byte-identical, checked by SHA-256; the copy in the type's own branch stays, the other is removed by the stage that owns it (a pack copy that a manifest names is open: review case 9).

| removed copy | kept copy |
|---|---|
| `docs/model-v3/household-arm-run/cap_lien/lien_alarms.csv` | `docs/model-v3/household-arm-run/lien_alarms.csv` -> `results/household-arm-run/household-arm-run-lien-alarms.csv` |
| `docs/model-v3/household-arm-run/flow_switches/lien_alarms_floor25.csv` | `docs/model-v3/household-arm-run/flow_switches/lien_alarms_floor0.csv` -> `results/household-arm-run/flow_switches/lien_alarms_floor0.csv` |
| `docs/model-v3/household-arm-run/flow_switches/lien_alarms_floor50.csv` | `docs/model-v3/household-arm-run/flow_switches/lien_alarms_floor0.csv` -> `results/household-arm-run/flow_switches/lien_alarms_floor0.csv` |
| `docs/model-v3/household-arm-run/flow_switches/lien_alarms_wd_low.csv` | `docs/model-v3/household-arm-run/floor_restart/lien_alarms.csv` -> `results/household-arm-run/floor_restart/floor-restart-lien-alarms.csv` |
| `docs/research/data/129r/Before-the-fall.pdf` | `Research/Before-the-fall.pdf` -> `literature/Before-the-fall.pdf` |
| `docs/research/data/129r/meanmedianaggregateandpercentageofwealthbywealthcomponentandageofhouseholdreferenceperson.xlsx` | `docs/research/data/098r/meanmedianaggregateandpercentageofwealthbywealthcomponentandageofhouseholdreferenceperson.xlsx` -> `data/uk-wealth-tables/098r/meanmedianaggregateandpercentageofwealthbywealthcomponentandageofhouseholdreferenceperson.xlsx` |
| `docs/research/data/129r/totalwealthtables.xlsx` | `Rates Data/totalwealthtables.xlsx` -> `data/rates/totalwealthtables.xlsx` |
| `model_v3/pack/GBR/source/jst_r6.json` | `data/jst/jst_r6.json` -> `data/jst/jst_r6.json` |

## Same-name files that differ, renamed (R3)

78 files, all in the CSV (column `rename`). The rule: the copy that is a brief, a study output, a study script or an agent guide gives way; a study output gets its folder as a prefix (`f1_phases_6/f1_safe_grid.csv` becomes `f1-phases-6-f1-safe-grid.csv`), an archived brief the suffix `-brief`. The names are mechanical: the stage that moves them may choose better ones, and rewrites every reader (code, manifest, test, doc) in the same commit.

| old folder | files renamed |
|---|---|
| `docs/archive/briefs` | 15 |
| `docs/model-v3/f1-household` | 10 |
| `docs/model-v3/of1-ck1/phase10_median_mid` | 8 |
| `docs/model-v3/household-arm-run` | 7 |
| `docs/model-v3/death-phases/f1_phases_15` | 5 |
| `docs/model-v3/death-phases/f1_phases_30` | 5 |
| `docs/model-v3/death-phases/f1_phases_6` | 5 |
| `docs/model-v3/household-arm-run/floor_restart` | 4 |
| `docs/model-v3/household-arm-run/gdp_paths` | 4 |
| `docs/model-v3/household-arm-run/cap_lien` | 2 |
| `docs/model-v3/returns` | 2 |
| `docs/agents` | 1 |
| `docs/model-v3/cell-baseline` | 1 |
| `docs/model-v3/death-phases` | 1 |
| `docs/model-v3/f1-diagnostic` | 1 |
| `docs/model-v3/kernel-wiring` | 1 |
| `docs/model-v3/tornado` | 1 |
| `docs/model-v3/wealth-ratio-diagnostic` | 1 |
| `docs/research/data/104r` | 1 |
| `docs/research/data/129r` | 1 |
| `docs/research/readable/data/098r` | 1 |
| `docs/research/readable/data/129r` | 1 |

## Generic names that remain (R3, unique but generic)

`INDEX.md`, `build.bat`, `common.py`, `config.py`, `gap.py`, `hooks.md`, `hooks.py`, `index.md`, `index.qmd`, `pdf.py`, `ranges.csv`, `ranges.py`, `tables.py`, `tools.css`, `tools.py`, `transforms.py`, `validate.py`

## Files whose bytes are pinned and that name an old path (hazard 2)

Moves keep bytes. A path rewritten inside one of these changes its hash or digest; none is rewritten by this map.

- `registry/inputs.json`: line 568: `model_v3/runner/switches.py`
- `tests/model_v3/fixtures/legacy_digest.json`: line 3: `tests/model_v3/test_legacy_digest.py`
- `model_v3/pack/GBR/manifest.json`: line 104: `docs/model-v3/kernel-wiring/decile_composition.csv`
- `registry/internal.json`: line 2: `pipeline/bib_to_json.py`
- `registry/metrics.json`: no old path named

## Depth-based paths (hazard 1)

472 lines in `file-layout-depth.csv` (`__file__`, `parents[`, `.parent`, `os.path`, `..`, includes, `.bat`, YAML), each with the shift its file's move needs (`depth +1` means one folder deeper). Scripts that write their output beside themselves (`HERE / name`) change too: their output folder moves from the script's folder to `results/<study>/`, which no shift expresses; the 162c and 163c briefs list them from this file.

| area | lines |
|---|---|
| `docs` | 201 |
| `tests` | 177 |
| `pipeline` | 82 |
| `model_v3` | 12 |

## Local-only files (hazard 5)

Git does not move these; the change report of the stage lists each with its old and new path for the author to move by hand.

- docs/research/data/097r/boe-nmg-*.xlsx  ->  data/uk-wealth-tables/097r/boe-nmg-*.xlsx
- docs/research/data/097r/nbs.xlsx  ->  data/uk-wealth-tables/097r/nbs.xlsx
- docs/research/data/097r/ukea2026q2.xlsx  ->  data/uk-wealth-tables/097r/ukea2026q2.xlsx
- .quarto/  ->  website/.quarto/ (rebuilt by quarto; the build is run from website/ or the root, see 161c)
- _build/ and _site/  ->  rebuilt by the build; not moved
- scratch/  ->  wherever the converter writes (pipeline/to_markdown.py); decided in 160c
- pdfs/  ->  literature/ (the build copies PDFs from it; 161c)
- print/  ->  website/print/ (generated PDFs; 161c)
- anchors.yml  ->  generated next to the page registry: website/registry/anchors.yml (161c)
- registry/references.json  ->  website/registry/references.json (generated)
- site/pages/glossary.md  ->  website/site/pages/glossary.md (generated)
- source/.obsidian/  ->  papers/legacy/.obsidian/ (editor state; move by hand or ignore)
- check*.txt, pipeline/check*.txt  ->  generated reports; ignore patterns rewritten

## Windows path length (hazard 4)

Longest new relative paths (the checkout adds about 60 characters; the limit is 260):

- 132: `literature/readable/data/098r/098r-meanmedianaggregateandpercentageofwealthbywealthcomponentandageofhouseholdreferenceperson-xlsx.md`
- 132: `literature/readable/data/129r/129r-meanmedianaggregateandpercentageofwealthbywealthcomponentandageofhouseholdreferenceperson-xlsx.md`
- 121: `data/uk-wealth-tables/098r/meanmedianaggregateandpercentageofwealthbywealthcomponentandageofhouseholdreferenceperson.xlsx`
- 119: `literature/readable/data/129r/ukda_data_dictionaries/was_round_8_person_eul_may_2025_230525_ukda_data_dictionary.rtf.md`
- 118: `literature/readable/data/129r/ukda_data_dictionaries/was_round_8_hhold_eul_may_2025_230525_ukda_data_dictionary.rtf.md`

`Rates Data/` (a space) becomes `data/rates/`; `Research/` and `docs/research/` differ in case and in place, so Windows and Linux agree after the move.

## References by old area

| old area named | lines |
|---|---|
| `docs` | 981 |
| `pipeline` | 256 |
| `Rates Data` | 248 |
| `registry` | 225 |
| `Research` | 167 |
| `tests` | 145 |
| `site` | 130 |
| `model_v3` | 123 |
| `source` | 117 |
| `STATUS.md` | 25 |
| `OVERVIEW.md` | 22 |
| `START_HERE.md` | 16 |
| `Tools` | 16 |

Per file: `python pipeline/path_refs.py --refs`; per line: `file-layout-references.csv`. Kinds: `file` (an exact tracked path), `folder`, `other` (a glob, a placeholder or a path that no longer exists: not rewritten, listed).
