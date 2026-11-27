# Wealth Delta Tax: overview

A map of what exists now, not a history. Read by section. Kept under about 15 KB by the guru (`project/agents/overview-maintenance.md`). Directory map synced to the moved layout on 2026-11-26; the other sections were last synced on 2026-11-15; the live site was not fetched.

## 1. What this is
An accrual-basis wealth tax with symmetric loss refunds and a sovereign wealth fund, set out in a paper series (main papers plus appendix companions), with a Python model that produces the papers' figures and tables and a Quarto site at https://wealthdeltatax.org.

## 2. Directory map
```
papers/legacy/     the papers as Markdown, one file per paper or appendix (canonical)
website/           build/ (scrape_contents, build_glossary, build_anchors, preprocess; pdf.py; zenodo_upload.py;
                   wdt_crosslinks.py; check_wdt_format.py; build.bat), site/ (_quarto.yml, pages/, style/, includes/,
                   diagrams/, tools/), registry/ (papers.yml, contents.yml, glossary.yml, routing.yml; crosslinks.json
                   and anchors.yml are generated), notes/ (site design notes), wdt-site-architecture.md
model/             model_v3/ (core, runner, out, pack builder, run.py, levers.json, numerics.py), studies/ (one folder of
                   scripts per diagnostic), tools/ (build_inputs, build_metrics, validate_outputs, run_suites, check_gate)
model-specs/       the model's design record: inputs.md, metrics.md, outputs.yml, architecture.md, acceptance.md, country-pack.md ...
data/              input-register/ (inputs.json, metrics.json), country-packs/GBR/, rates/ (source spreadsheets), jst/, wid/,
                   uk-wealth-tables/, uk-source-workbooks/
literature/        PDFs, references.bib, internal.json, references.json (generated); readable/ = a Markdown copy of every binary
research/          notes/ (NNNr derivations), scripts/, tables/, hypotheses/, model-audit/, model-lessons/ (do not open),
                   legacy-model-plans/, scaffold-audit/, wdt-jel-codes.md
results/           committed run and study outputs, one folder per study
tests/             model/ (data, gate, model_v3, tools), website/ (cards, glossary, hooks, layout, nav, pages, retired), project/
project/           agents/ (role guides + reference/), briefs/ (open/, done/; NNNx-slug, x = role letter), skills/ (.skill files
                   for claude.ai), tools/ (check_agent_docs, to_markdown, path_refs, build_skills), restructure/ (the file move:
                   map, proof, tripwire), housekeeping/; OVERVIEW.md, STATUS.md, START_HERE.md, decisions.md, todo.md,
                   brief-suggestions.md, lane-plan.html
.github/workflows/ deploy.yml: Quarto build and GitHub Pages deploy on push to main
.claude/skills/    the five role skill stubs (source of the .skill files)
```
The v1 and v2 models are removed (tag `legacy-models-2026-11`; restore with `git checkout legacy-models-2026-11 -- model_v2`). Old path to new path for every moved file: `project/restructure/file-layout-map.csv`.

## 3. Key concepts
- Paper shortcodes (WP, MF, VAL, GOV, RATES ...) are defined in `website/registry/papers.yml` and `website/site/pages/Project-Map.md`.
- Cross-references use `(X §N)`; resolution is checked by `website/build/wdt_crosslinks.py`, syntax by `website/build/check_wdt_format.py`.
- Positions per paper and the open-questions register: `website/site/pages/Project-Map.md`.
- Interpretive framework for consistency checks: `project/agents/reference/framework.md`.

## 4. How to run, build and check
- Site: `website/build/build.bat` (no render) or `website/build/build_and_render.bat`; CI runs the same steps on Linux. Details: `website/wdt-site-architecture.md` (synced 15 Nov 2026). The build no longer reads or publishes a model folder (`model_v1/` removed, tag `legacy-models-2026-11`).
- Model: model v3 (`model/model_v3/`, run script `model/model_v3/run.py`); the legacy v1 and v2 models are removed, see tag `legacy-models-2026-11`.
- Format check: `python website/build/check_wdt_format.py papers/legacy/<paper>.md`.
- Crosslink check: `python website/build/wdt_crosslinks.py check` (workflow in `project/agents/reference/writing/style-guide.md`).

## 5. Status of work
See `project/STATUS.md`. Finished work and decisions: `project/decisions.md`.

## 6. Findings and open issues
- `website/wdt-site-architecture.md` is 32 KB (target 15 KB); not split. It lists Issue 7 (a Zenodo sandbox token is hardcoded in `website/build/zenodo_upload.py`) and Issue 16 (the revenue calculator fetches `rates_model.py`, which is gone).
- The v1 and v2 models are removed from the tree (tag `legacy-models-2026-11`); the range model v3 replaces them. The site's old calculators and the old papers' figures lost their model assets (brief 009c, rule R5).
- The site build is not `git status` clean: it rewrites `website/registry/contents.yml`, `website/site/pages/glossary.md` and `literature/references.json` (author to decide if they stay tracked).
- Crosslink errors in the papers (duplicate ADD section numbers, missing SCOPE/RATES/WFR/SWEEPS targets): run `python website/build/wdt_crosslinks.py check`; the author is rewriting the papers.
- Audit: `research/scaffold-audit/scaffold-2026-11-15.md`.
