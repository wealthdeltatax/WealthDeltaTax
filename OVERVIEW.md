# Wealth Delta Tax: overview

A map of what exists now, not a history. Read by section. Kept under about 15 KB by the guru (`docs/agents/overview-maintenance.md`). Last synced against the repo files on 2026-11-15; the live site was not fetched.

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
model/       v1/v2 Python model (legacy, see section 6): *_core.py, *_tables.py, *_charts.py,
             WDT_Params.toml, jst_r6.json, OUTPUTS/ (tracked, generated), test/
docs/        todo.md, EVAL_PLAN.md, plans; agents/ (role guides + reference/); briefs/;
             decisions.md; model-lessons/ (legacy model notes); audit/; wdt-site-architecture.md
model_new_2/ second model (v2, legacy): wdt_core/kernel/jst/par, EVAL/, RATES/, VAL/, WID data and guide,
             README.md, WDT_Code_Reference.md; replaced by model v3 (brief 001)
Rates Data/  source spreadsheets (JST, tax tables)      Research/  background PDF
Tools/       flat .skill files: five current role stubs (wdt-guru, -code, -write, -research, -web)
             plus old archives to remove (brief 005)
.github/workflows/deploy.yml   Quarto build and GitHub Pages deploy on push to main
```

## 3. Key concepts
- Paper shortcodes (WP, MF, VAL, GOV, RATES ...) are defined in `registry/papers.yml` and `site/pages/Project-Map.md`.
- Cross-references use `(X §N)`; resolution is checked by `pipeline/wdt_crosslinks.py`, syntax by `pipeline/check_wdt_format.py`.
- Positions per paper and the open-questions register: `site/pages/Project-Map.md`.
- Interpretive framework for consistency checks: `docs/agents/reference/framework.md`.

## 4. How to run, build and check
- Site: `pipeline/build.bat` (no render) or `pipeline/build_and_render.bat`; CI runs the same steps on Linux. Details: `docs/wdt-site-architecture.md` (stale in places, see section 6).
- Model: `model/run_all.bat` (cores first, then tables and charts).
- Format check: `python pipeline/check_wdt_format.py source/<paper>.md`.
- Crosslink check: `python pipeline/wdt_crosslinks.py check` (workflow in `docs/agents/reference/writing/style-guide.md`).

## 5. Status of work
See `STATUS.md`. Finished work and decisions: `docs/decisions.md`.

## 6. Findings and open issues
- `docs/wdt-site-architecture.md` still says the root is `wdt-site/` and was last synced 5 Oct 2026.
- `model/WDT_Model_Reference.md` names `rates_model.py` (now `rates_core1.py`) and old script numbers.
- The v1 (`model/`) and v2 (`model_new_2/`) models are being replaced by a third refactor (brief 001). Do not extend either.
- `model_new_2/` is large (WID data dumps, raw JSON) and contains an `SS` folder of superseded material.
- `check.txt` and `pipeline/check2.txt` are old crosslink-check output kept at their old paths.
- `model/test/` holds `welfare_core.py` and `welfare_tables.py`, which are not tests.
- Crosslink errors in the papers (duplicate ADD section numbers, missing SCOPE/RATES/WFR/SWEEPS targets): see `check.txt`; the author is rewriting the papers.
- Audit: `docs/audit/scaffold-2026-11-15.md`.
