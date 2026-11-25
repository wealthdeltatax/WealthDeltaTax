# File layout map (044c R1: inventory, nothing moved)

Written by `pipeline/path_refs.py --map` from the tracked files at `1af9e73` (009c merged). The rule table is `RULES` in that script; 
the per-file table is `file-layout-map.csv` (old, new, flag, rule, rename, duplicate_of); the references and the depth-based paths are `file-layout-references.csv` and `file-layout-depth.csv`. 
Flag **S** = settled: by the author's rules, or by the R1 checkpoint rulings (2026-11-24, brief 044c) that closed the 13 review cases and changed some defaults. This map is the authority for 160c to 164c. After each stage `python pipeline/path_refs.py --check` must report no old path of the moved areas (the four pinned lines excepted).

**1104 tracked files**: 1104 settled, 0 still open, 0 without a rule; 77 renamed under R3; 7 byte-identical copies removed under R4; 2599 lines name an old path, in 333 files; 498 lines build a path from their own location.

## Review table (all 13 cases settled at the R1 checkpoint, author, 2026-11-24; R1 round 2 regenerated this map)

| # | Case | Placement in this map | Ruling |
|---|---|---|---|
| 1 | Loose plans and notes | `docs/navigation_suggestions.md` to `website/notes/`; `docs/EVAL_PLAN.md`, `VAL_*.md` to `research/legacy-model-plans/`; `docs/wdt-jel-codes.md` to `research/`; `docs/wdt-site-architecture.md` to `website/` | **Settled** as the guru defaults of 044c (checkpoint, 2026-11-24: the map's defaults stand). |
| 2 | Site design notes in `docs/restructure/` | every file except the layout design, the map files, the proof and the tripwire (`file-layout*.md/csv`, `path_rewrite_proof.py`, `move_tripwire.py`, `move-tripwire-baseline.json`, which go to `project/restructure/`) to `website/notes/` | **Settled** as the map default: they describe the site build, so they follow the site. |
| 3 | Research study outputs in `docs/research/data/` | folders 097r, 098r, 129r (source tables) to `data/uk-wealth-tables/`; the derived tables of 099r to 104r, 131r, 145r, 146r to `research/tables/<NNNr-slug>/`; every script of these folders (the 097r, 098r extractors included) to `research/scripts/` | **Settled, changed from the default** (ruling 1): research outputs are research; `results/` holds model run outputs only and `model/` model code only. The 097r and 098r extractor scripts follow the same rule (not named in the ruling). |
| 4 | Readable copies | `docs/research/readable/` (incl. the `data/097r`, `098r`, `129r` copies of workbooks) to `literature/readable/`; `INDEX.md` becomes `readable-copies-index.md` | **Settled** as the map default; the index is renamed (ruling 4d: it differs from Quarto's `index.md` only by case). |
| 5 | Workbooks in `Research/` | `etbreferencetablesfye202324final.xlsx`, `medianpricepaidforadministrativegeographiesexisting.xlsx` to `data/uk-source-workbooks/` | **Settled** as the map default (datasets, not PDFs). |
| 6 | Split of `docs/model-v3/` | 24 spec files to `model-specs/`; 11 reports with their folders to `results/<study>/`; 12 study folders as listed in the CSV; scripts to `model/studies/<study>/`; `added/` and `inputs-added/` to `model-specs/` | **Settled** as the map default, including the borderline specs (`i1-gap.md`, `kernel-wiring-design.md`, `returns-gap.md`, `returns-method.md`) and `cell-baseline/inputs_used.json` staying in `results/cell-baseline/`. |
| 7 | Split of `pipeline/` | web and build scripts to `website/build/`; `build_inputs`, `build_metrics`, `validate_outputs`, `run_suites`, `check_gate` to `model/tools/`; `check_agent_docs`, `build_skills`, `path_refs` to `project/tools/` | **Settled, changed from the default** (ruling 4a): the project tools go to `project/tools/`, not `project/housekeeping/`. `bib_to_json.py` goes with the website build scripts and reads the bibliography from `literature/` (ruling 2). |
| 8 | Split of `registry/` | `inputs.json`, `inputs-display.yml`, `metrics.json` to `data/input-register/`; `references.bib`, `internal.json` and the generated `references.json` to `literature/` (flat, unique names); everything else (pages, glossary, crosslinks, ...) to `website/registry/` | **Settled, changed from the default** (ruling 2): the bibliography is literature. |
| 9 | Country pack | `model_v3/pack/GBR/*` to `data/country-packs/GBR/`; `build_gbr.py` stays in `model/model_v3/pack/`; the pack's own `source/jst_r6.json` stays beside the manifest that names it | **Settled** (ruling 4d): the pack copy of `jst_r6.json` is an exempt loader file, not removed as a duplicate of `data/jst/jst_r6.json`; the loader path is rewritten in 162c. |
| 10 | Test suites | `data`, `gate`, `model_v3` to `tests/model/`; `cards`, `glossary`, `layout`, `nav`, `pages`, `retired` to `tests/website/`; the `hooks` suite split by what each test file tests: `test_build_skills.py`, `test_check_agent_docs.py` to `tests/project/tools/`; `test_run_suites.py` to `tests/model/tools/`; the other five test files, `conftest.py` and the fixtures to `tests/website/hooks/` | **Settled, changed from the default** (ruling 4c): tests follow the code they test (`tests/model`, `tests/website`, `tests/project`). `pipeline/run_suites.py` and the hooks `conftest.py` find suites and fixtures by path: 162c and 164c rewrite them (see the depth list). |
| 11 | Agent guide names | `docs/agents/code.md`, `guru.md`, `research.md`, `web.md`, `writing.md` become `project/agents/agent-code.md`, `agent-guru.md`, `agent-research.md`, `agent-web.md`, `agent-writing.md` | **Settled, changed from the default** (ruling 4b): all five are renamed; R6 (164c) rewrites the skills and every active reader. |
| 12 | Generic names that are unique | listed in the section "Generic names that remain" below | **Settled** as the map default: the stage that owns the file may rename it, with every reader rewritten. `index.md` and `index.qmd` (Quarto) are exempt names. |
| 13 | Pinned files that name an old path | the four stale citations of the section "Files whose bytes are pinned" below keep their bytes: `registry/inputs.json` line 568, `legacy_digest.json` line 3, the pack `manifest.json` line 104, `internal.json` line 2 (then under `literature/`) | **Settled** (ruling 3): `path_refs.py --check` allow-lists exactly these four lines; they are refreshed at the next real re-pin of the register. Rewriting any other line of a pinned file is stop-and-report. |

## Old area to new area

| old area | files | | new area | files |
|---|---|---|---|---|
| `docs` | 747 | | `project` | 205 |
| `tests` | 126 | | `results` | 155 |
| `site` | 53 | | `research` | 135 |
| `model_v3` | 45 | | `data` | 133 |
| `pipeline` | 35 | | `website` | 129 |
| `source` | 33 | | `tests` | 126 |
| `Research` | 20 | | `model` | 74 |
| `registry` | 13 | | `literature` | 64 |
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
| `^Research/(.*\.pdf)$` | 18 | S | `Research/1-s2.0-S0014292125001266-main.pdf` | `literature/1-s2.0-S0014292125001266-main.pdf` |
| `^Research/(.*\.xlsx)$` | 2 | S | `Research/etbreferencetablesfye202324final.xlsx` | `data/uk-source-workbooks/etbreferencetablesfye202324final.xlsx` |
| `^Tools/(.*\.skill)$` | 6 | S | `Tools/repo-scaffold.skill` | `project/skills/repo-scaffold.skill` |
| `^data/(jst/.*/wid/.*)$` | 4 | S | `data/jst/jst_r6.json` | `data/jst/jst_r6.json` |
| `^docs/(EVAL_PLAN\.md/VAL_[^/]*\.md)$` | 3 | S | `docs/EVAL_PLAN.md` | `research/legacy-model-plans/EVAL_PLAN.md` |
| `^docs/agents/(.*)$` | 21 | S | `docs/agents/README.md` | `project/agents/README.md` |
| `^docs/agents/(code/guru/research/web/writing)\.md$` | 5 | S | `docs/agents/code.md` | `project/agents/agent-code.md` |
| `^docs/archive/briefs/(.*)$` | 143 | S | `docs/archive/briefs/001c-model-audit.md` | `project/briefs/done/001c-model-audit.md` |
| `^docs/archive/friction-log-archive\.md$` | 1 | S | `docs/archive/friction-log-archive.md` | `project/agents/friction-log-archive.md` |
| `^docs/archive/wdt-librarian\.skill$` | 1 | S | `docs/archive/wdt-librarian.skill` | `project/skills/wdt-librarian.skill` |
| `^docs/audit/(.*)$` | 1 | S | `docs/audit/scaffold-2026-11-15.md` | `research/scaffold-audit/scaffold-2026-11-15.md` |
| `^docs/(decisions\.md/todo\.md/lane-plan\.html/brief-suggesti` | 4 | S | `docs/brief-suggestions.md` | `project/brief-suggestions.md` |
| `^docs/briefs/(.*)$` | 8 | S | `docs/briefs/044c-file-layout-move.md` | `project/briefs/open/044c-file-layout-move.md` |
| `^docs/housekeeping/(.*)$` | 2 | S | `docs/housekeeping/README.md` | `project/housekeeping/README.md` |
| `^docs/hypotheses/(.*)$` | 4 | S | `docs/hypotheses/empirical-household-flow-parameter-map.md` | `research/hypotheses/empirical-household-flow-parameter-map.md` |
| `^docs/model-audit/(.*)$` | 13 | S | `docs/model-audit/change-report-household-resilience.md` | `research/model-audit/change-report-household-resilience.md` |
| `^docs/model-lessons/(.*)$` | 3 | S | `docs/model-lessons/drift-register.md` | `research/model-lessons/drift-register.md` |
| `^docs/model-v3/([^/]+)$` | 35 | S | `docs/model-v3/acceptance.md` | `model-specs/acceptance.md` |
| `^docs/model-v3/([^/]+)/(.*)$` | 192 | S | `docs/model-v3/added/h1.md` | `model-specs/added/h1.md` |
| `^docs/navigation_suggestions\.md$` | 1 | S | `docs/navigation_suggestions.md` | `website/notes/navigation_suggestions.md` |
| `^docs/research/([0-9]{3}r-[^/]*\.md)$` | 29 | S | `docs/research/012r-b1-derivations.md` | `research/notes/012r-b1-derivations.md` |
| `^docs/research/data/([0-9]{3}r)/(.*)$` | 192 | S | `docs/research/data/097r/Collated_Tables_3_1_to_3_11_2324.ods` | `data/uk-wealth-tables/097r/Collated_Tables_3_1_to_3_11_2324.ods` |
| `^docs/research/readable/INDEX\.md$` | 1 | S | `docs/research/readable/INDEX.md` | `literature/readable/readable-copies-index.md` |
| `^docs/research/readable/(.*)$` | 39 | S | `docs/research/readable/data/097r/Collated_Tables_3_1_to_3_11_2324.ods.md` | `literature/readable/data/097r/Collated_Tables_3_1_to_3_11_2324.ods.md` |
| `^docs/restructure/(file-layout\.md/file-layout-map\.md/file-` | 8 | S | `docs/restructure/file-layout-depth.csv` | `project/restructure/file-layout-depth.csv` |
| `^docs/restructure/(.*)$` | 39 | S | `docs/restructure/ids-map.md` | `website/notes/ids-map.md` |
| `^docs/wdt-jel-codes\.md$` | 1 | S | `docs/wdt-jel-codes.md` | `research/wdt-jel-codes.md` |
| `^docs/wdt-site-architecture\.md$` | 1 | S | `docs/wdt-site-architecture.md` | `website/wdt-site-architecture.md` |
| `^model_v3/(.*)$` | 32 | S | `model_v3/__init__.py` | `model/model_v3/__init__.py` |
| `^model_v3/pack/GBR/(.*)$` | 13 | S | `model_v3/pack/GBR/NOTICE.md` | `data/country-packs/GBR/NOTICE.md` |
| `^pipeline/(.*)$` | 35 | S | `pipeline/bib_to_json.py` | `website/build/bib_to_json.py` |
| `^registry/([^/]+)$` | 13 | S | `registry/contents.yml` | `website/registry/contents.yml` |
| `^site/(.*)$` | 53 | S | `site/_quarto.yml` | `website/site/_quarto.yml` |
| `^source/(.*)$` | 33 | S | `source/10_Behavioural_Robustness_and_Administrative_Experience.md` | `papers/legacy/10_Behavioural_Robustness_and_Administrative_Experience.md` |
| `^tests/([^/]+)/(.*)$` | 126 | S | `tests/cards/test_cards.py` | `tests/website/cards/test_cards.py` |

## Duplicates (R4)

Byte-identical, checked by SHA-256; the copy in the type's own branch stays, the other is removed by the stage that owns it. The pack's own `source/jst_r6.json` is an exempt loader file (case 9) and is not listed.

| removed copy | kept copy |
|---|---|
| `docs/model-v3/household-arm-run/cap_lien/lien_alarms.csv` | `docs/model-v3/household-arm-run/lien_alarms.csv` -> `results/household-arm-run/household-arm-run-lien-alarms.csv` |
| `docs/model-v3/household-arm-run/flow_switches/lien_alarms_floor25.csv` | `docs/model-v3/household-arm-run/flow_switches/lien_alarms_floor0.csv` -> `results/household-arm-run/flow_switches/lien_alarms_floor0.csv` |
| `docs/model-v3/household-arm-run/flow_switches/lien_alarms_floor50.csv` | `docs/model-v3/household-arm-run/flow_switches/lien_alarms_floor0.csv` -> `results/household-arm-run/flow_switches/lien_alarms_floor0.csv` |
| `docs/model-v3/household-arm-run/flow_switches/lien_alarms_wd_low.csv` | `docs/model-v3/household-arm-run/floor_restart/lien_alarms.csv` -> `results/household-arm-run/floor_restart/floor-restart-lien-alarms.csv` |
| `docs/research/data/129r/Before-the-fall.pdf` | `Research/Before-the-fall.pdf` -> `literature/Before-the-fall.pdf` |
| `docs/research/data/129r/meanmedianaggregateandpercentageofwealthbywealthcomponentandageofhouseholdreferenceperson.xlsx` | `docs/research/data/098r/meanmedianaggregateandpercentageofwealthbywealthcomponentandageofhouseholdreferenceperson.xlsx` -> `data/uk-wealth-tables/098r/meanmedianaggregateandpercentageofwealthbywealthcomponentandageofhouseholdreferenceperson.xlsx` |
| `docs/research/data/129r/totalwealthtables.xlsx` | `Rates Data/totalwealthtables.xlsx` -> `data/rates/totalwealthtables.xlsx` |

## Same-name files that differ, renamed (R3)

77 files, all in the CSV (column `rename`). The rule: the copy that is a brief, a study output, a study script or an agent guide gives way; a study output gets its folder as a prefix (`f1_phases_6/f1_safe_grid.csv` becomes `f1-phases-6-f1-safe-grid.csv`), an archived brief the suffix `-brief`. The names are mechanical: the stage that moves them may choose better ones, and rewrites every reader (code, manifest, test, doc) in the same commit.

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

`build.bat`, `common.py`, `config.py`, `gap.py`, `hooks.md`, `hooks.py`, `pdf.py`, `ranges.csv`, `ranges.py`, `tables.py`, `tools.css`, `tools.py`, `transforms.py`, `validate.py`

## Files whose bytes are pinned and that name an old path (hazard 2)

Moves keep bytes. A path rewritten inside one of these changes its hash or digest. Ruling 3: the four lines marked **allowed** keep their stale citation until the next real re-pin; rewriting any other line of a pinned file is stop-and-report.

- `registry/inputs.json` (new home `data/input-register/inputs.json`): line 568: `model_v3/runner/switches.py` **allowed**
- `tests/model_v3/fixtures/legacy_digest.json` (new home `tests/model/model_v3/fixtures/legacy_digest.json`): line 3: `tests/model_v3/test_legacy_digest.py` **allowed**
- `model_v3/pack/GBR/manifest.json` (new home `data/country-packs/GBR/manifest.json`): line 104: `docs/model-v3/kernel-wiring/decile_composition.csv` **allowed**
- `registry/internal.json` (new home `literature/internal.json`): line 2: `pipeline/bib_to_json.py` **allowed**
- `registry/metrics.json` (new home `data/input-register/metrics.json`): no old path named

## Depth-based paths (hazard 1)

498 lines in `file-layout-depth.csv` (`__file__`, `parents[`, `.parent`, `os.path`, `..`, includes, `.bat`, YAML), each with the shift its file's move needs (`depth +1` means one folder deeper). Scripts that write their output beside themselves (`HERE / name`) change too: their output folder moves from the script's folder to `results/<study>/`, which no shift expresses; the 162c and 163c briefs list them from this file.

| area | lines |
|---|---|
| `docs` | 207 |
| `tests` | 177 |
| `pipeline` | 102 |
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
- registry/references.json  ->  literature/references.json (generated by website/build/bib_to_json.py; ruling 2)
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
| `docs` | 1039 |
| `pipeline` | 276 |
| `Rates Data` | 248 |
| `registry` | 236 |
| `tests` | 168 |
| `Research` | 167 |
| `site` | 131 |
| `model_v3` | 131 |
| `source` | 121 |
| `STATUS.md` | 26 |
| `OVERVIEW.md` | 23 |
| `START_HERE.md` | 17 |
| `Tools` | 16 |

Per file: `python pipeline/path_refs.py --refs`; per line: `file-layout-references.csv`. Kinds: `file` (an exact tracked path), `folder`, `other` (a glob, a placeholder or a path that no longer exists: not rewritten, listed).
