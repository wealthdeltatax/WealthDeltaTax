# Wealth Delta Tax: overview

A map of what exists now, not a history. Read by section. Kept under about 15 KB by the guru (`docs/agents/overview-maintenance.md`). Last synced against the repo files on 2026-11-15 (after briefs 003s to 010s); the live site was not fetched.

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
model_v1/    first Python model (legacy, see section 6): *_core.py, *_tables.py, *_charts.py,
             WDT_Params.toml, jst_r6.json, OUTPUTS/ (tracked, generated), test/
docs/        agents/ (role guides + reference/); briefs/ (NNNx-slug, x = role letter); lane-plan.html (plan view);
             decisions.md; model-lessons/ (legacy model notes); audit/; model-audit/ (v1 and v2 audit, synthesis); archive/. Owners of the loose files:
             wdt-site-architecture.md and navigation_suggestions.md (web); wdt-jel-codes.md (writing);
             EVAL_PLAN.md, VAL_generational_model_plan.md, VAL_refactor_report.md (code, v2 legacy plans);
             todo.md and brief-suggestions.md (guru; todo list is also in STATUS.md)
model_v2/    second model (legacy): wdt_core/kernel/jst/par, EVAL/, RATES/, VAL/, WID data and guide,
             README.md, WDT_Code_Reference.md; replaced by model v3 (design brief 011g; requirements in `docs/model-audit/synthesis.md`)
Rates Data/  source spreadsheets (JST, tax tables)      Research/  background PDF
Tools/       flat .skill files: five role stubs (wdt-guru, -code, -write, -research, -web), copies of
             .claude/skills/<role>/SKILL.md, plus repo-scaffold.skill
.github/workflows/deploy.yml   Quarto build and GitHub Pages deploy on push to main
```

## 3. Key concepts
- Paper shortcodes (WP, MF, VAL, GOV, RATES ...) are defined in `registry/papers.yml` and `site/pages/Project-Map.md`.
- Cross-references use `(X §N)`; resolution is checked by `pipeline/wdt_crosslinks.py`, syntax by `pipeline/check_wdt_format.py`.
- Positions per paper and the open-questions register: `site/pages/Project-Map.md`.
- Interpretive framework for consistency checks: `docs/agents/reference/framework.md`.

## 4. How to run, build and check
- Site: `pipeline/build.bat` (no render) or `pipeline/build_and_render.bat`; CI runs the same steps on Linux. Details: `docs/wdt-site-architecture.md` (synced 15 Nov 2026). The build reads `model_v1/` and publishes it as `/model/`.
- Model: `model_v1/run_all.bat` (cores first, then tables and charts).
- Format check: `python pipeline/check_wdt_format.py source/<paper>.md`.
- Crosslink check: `python pipeline/wdt_crosslinks.py check` (workflow in `docs/agents/reference/writing/style-guide.md`).

## 5. Status of work
See `STATUS.md`. Finished work and decisions: `docs/decisions.md`.

## 6. Findings and open issues
- `docs/wdt-site-architecture.md` is 32 KB (target 15 KB); not split. It lists Issue 7 (a Zenodo sandbox token is hardcoded in `pipeline/zenodo_upload.py`) and Issue 16 (the revenue calculator fetches `rates_model.py`, which is gone).
- `model_v1/WDT_Model_Reference.md` names `rates_model.py` (now `rates_core1.py`) and old script numbers.
- The v1 (`model_v1/`) and v2 (`model_v2/`) models are being replaced by a range model, v3 (audit done; design brief 011g is a draft). Do not extend either.
- `model_v2/` is large (WID data dumps, raw JSON).
- The site build is not `git status` clean: it rewrites `registry/contents.yml`, `site/pages/glossary.md` and `registry/references.json` (author to decide if they stay tracked).
- Crosslink errors in the papers (duplicate ADD section numbers, missing SCOPE/RATES/WFR/SWEEPS targets): run `python pipeline/wdt_crosslinks.py check`; the author is rewriting the papers.
- Audit: `docs/audit/scaffold-2026-11-15.md`.
