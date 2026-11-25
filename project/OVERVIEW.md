# Wealth Delta Tax: overview

A map of what exists now, not a history. Read by section. Kept under about 15 KB by the guru (`project/agents/overview-maintenance.md`). Last synced against the repo files on 2026-11-15 (after briefs 003s to 010s); the live site was not fetched.

## 1. What this is
An accrual-basis wealth tax with symmetric loss refunds and a sovereign wealth fund, set out in a paper series (main papers plus appendix companions), with a Python model that produces the papers' figures and tables and a Quarto site at https://wealthdeltatax.org.

## 2. Directory map
```
source/      papers as Markdown, one file per paper or appendix (canonical)
pipeline/    scrape_contents, build_glossary, build_anchors, preprocess (site build);
             pdf.py (PDF build); zenodo_upload.py; wdt_crosslinks.py; check_wdt_format.py
site/        _quarto.yml, pages/, style/, diagrams/, tools/   (hand-written site files)
registry/    papers.yml (33 entries), contents.yml, internal.json, references.bib/json,
             crosslinks.json (generated), anchors.yml (generated, gitignored)
data/        jst/jst_r6.json (JST R6, read by the model v3 pack builder), wid/ (wid_long.csv, wid_download.py, WID_Data_Guide.md)
docs/        agents/ (role guides + reference/); briefs/ (NNNx-slug, x = role letter); lane-plan.html (plan view);
             decisions.md; model-lessons/ (legacy model notes); audit/; model-audit/ (v1 and v2 audit, synthesis); archive/. Owners of the loose files:
             wdt-site-architecture.md and navigation_suggestions.md (web); wdt-jel-codes.md (writing);
             EVAL_PLAN.md, VAL_generational_model_plan.md, VAL_refactor_report.md (code, v2 legacy plans);
             todo.md and brief-suggestions.md (guru; todo list is also in project/STATUS.md)
(model_v1 and model_v2: removed from the tree, see tag `legacy-models-2026-11`; restore with `git checkout legacy-models-2026-11 -- model_v2`)
data/rates/  source spreadsheets (JST, tax tables)      Research/  background PDF
Tools/       flat .skill files: five role stubs (wdt-guru, -code, -write, -research, -web), copies of
             .claude/skills/<role>/SKILL.md, plus repo-scaffold.skill
.github/workflows/deploy.yml   Quarto build and GitHub Pages deploy on push to main
```

## 3. Key concepts
- Paper shortcodes (WP, MF, VAL, GOV, RATES ...) are defined in `website/registry/papers.yml` and `website/site/pages/Project-Map.md`.
- Cross-references use `(X §N)`; resolution is checked by `website/build/wdt_crosslinks.py`, syntax by `website/build/check_wdt_format.py`.
- Positions per paper and the open-questions register: `website/site/pages/Project-Map.md`.
- Interpretive framework for consistency checks: `project/agents/reference/framework.md`.

## 4. How to run, build and check
- Site: `website/build/build.bat` (no render) or `website/build/build_and_render.bat`; CI runs the same steps on Linux. Details: `website/wdt-site-architecture.md` (synced 15 Nov 2026). The build no longer reads or publishes a model folder (`model_v1/` removed, tag `legacy-models-2026-11`).
- Model: model v3 (`model_v3/`, run script `model_v3/run.py`); the legacy v1 and v2 models are removed, see tag `legacy-models-2026-11`.
- Format check: `python website/build/check_wdt_format.py source/<paper>.md`.
- Crosslink check: `python website/build/wdt_crosslinks.py check` (workflow in `project/agents/reference/writing/style-guide.md`).

## 5. Status of work
See `project/STATUS.md`. Finished work and decisions: `project/decisions.md`.

## 6. Findings and open issues
- `website/wdt-site-architecture.md` is 32 KB (target 15 KB); not split. It lists Issue 7 (a Zenodo sandbox token is hardcoded in `website/build/zenodo_upload.py`) and Issue 16 (the revenue calculator fetches `rates_model.py`, which is gone).
- The v1 and v2 models are removed from the tree (tag `legacy-models-2026-11`); the range model v3 replaces them. The site's old calculators and the old papers' figures lost their model assets (brief 009c, rule R5).
- The site build is not `git status` clean: it rewrites `website/registry/contents.yml`, `website/site/pages/glossary.md` and `literature/references.json` (author to decide if they stay tracked).
- Crosslink errors in the papers (duplicate ADD section numbers, missing SCOPE/RATES/WFR/SWEEPS targets): run `python website/build/wdt_crosslinks.py check`; the author is rewriting the papers.
- Audit: `research/scaffold-audit/scaffold-2026-11-15.md`.
