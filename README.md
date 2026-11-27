# Wealth Delta Tax

A series of papers (main papers plus appendix companions) proposing an accrual-basis wealth tax with symmetric loss refunds and a sovereign wealth fund. Live site: https://wealthdeltatax.org

## Layout
- `papers/legacy/` the papers (Markdown, canonical)
- `website/` the Quarto site: `build/` (scripts that build the site, PDFs and Zenodo uploads), `site/` (hand-written pages, styles, `_quarto.yml`), `registry/` (paper list, contents, glossary, generated anchors and crosslinks), `notes/` (design notes)
- `model/` the range model: `model_v3/` (code; run script `run.py`), `studies/` (one folder of scripts per diagnostic), `tools/` (build, validate, gate and suite runners). The legacy models are removed (tag `legacy-models-2026-11`)
- `model-specs/` the model's design record: inputs, metrics, outputs (`outputs.yml`), architecture, acceptance
- `data/` model inputs: `input-register/`, `country-packs/`, `rates/`, `jst/`, `wid/`, `uk-wealth-tables/`, `uk-source-workbooks/`
- `literature/` the PDFs, `references.bib`, `internal.json`; `readable/` holds a Markdown reading copy of every binary
- `research/` notes, scripts and derived tables, model audits and lessons, legacy model plans
- `results/` committed outputs of model runs and studies, one folder per study
- `tests/` `model/` (data, gate, model_v3, tools), `website/` (cards, glossary, hooks, layout, nav, pages, retired), `project/` (tools)
- `project/` agents, briefs, status, overview, decisions, tools (`check_agent_docs.py`, `to_markdown.py`, `path_refs.py`, `build_skills.py`), skills, and the file-move record in `restructure/`
- `.github/workflows/` the Quarto build and the GitHub Pages deploy on push to `main`; `.claude/skills/` the five role skill stubs

Working with an agent in this repo: start at `project/START_HERE.md`. The full old-to-new path map of the move: `project/restructure/file-layout-map.md`.
