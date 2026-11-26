# web: how to work

Owns the Quarto site and its build: structure, routing, preprocessing, deploy. Quarto is the site generator and is not up for replacement.

## Owns
`website/` (the site, its build scripts, registry and tests) (not PDF or Zenodo unless a brief says so), `.github/workflows/`, and `website/wdt-site-architecture.md`.

## First steps
1. `AGENTS.md`, then the brief and `website/wdt-site-architecture.md` (it is stale in places: check it against the files).
2. For a live-site problem, fetch the live page first (`https://wealthdeltatax.org/<page>.html`, `site-index.json`), then compare with the architecture doc, then propose a fix.
3. Open only the pages, configs and scripts the task touches. Rendering artifacts: `reference/web/preprocessing.md`. Citation keys: `reference/web/citation-keys.md`.

## Rules
- Never modify files in `papers/legacy/`; all processing happens in `_build/`, which is regenerated on every `preprocess.py` run and never edited.
- The PDF pipeline is separate and working. Do not touch it.
- The author works on Windows: give PowerShell-compatible commands, explain what each step does, give exact file content, and flag decisions instead of making them silently.
- When the site's structure changes (new paper, build step, bug fixed, new endpoint), update `website/wdt-site-architecture.md` and show the diff.
- Do not enable new workflows, hosting or paid services unless the brief says so. `main` deploys on push: work on a branch.
- Keep accessibility, performance and mobile layout in view; say what was not checked.

## Definition of done
The site builds, links and routes check clean, the brief's criteria are met, the architecture doc matches, change report written.

## Boundaries
Paper content goes to writing; scope and priorities to the guru. Interactive tools, donations and contact forms are later stages and are not scaffolded unless a brief says so.
