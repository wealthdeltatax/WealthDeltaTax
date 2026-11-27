# File layout: a vertical tree (design record; the move is applied)

> **Applied** (stages L1 to L7, merged by 2026-11-26): the repository now has the tree in `README.md` and `project/OVERVIEW.md` section 2; the old-to-new path of every file is `project/restructure/file-layout-map.csv`. Everything below is the original design and is kept as a record; its target tree and open points are not the layout in use.
>
> Superseded on 2026-11-24 by `project/briefs/open/044c-file-layout-move.md`: the tree is now by type of thing (data, literature, research, model, model-specs, results, papers, website, tests, project), file names are unique and descriptive, and the stages are L1 to L7. Where this note differs, the brief wins.

Status: design approved in part by the author, 2026-11-18; **the move runs after the model v3 build** (author's answer on timing). Nothing in this document is applied. Until then every brief uses today's paths.

## 1. The rule
Each folder holds only what it needs at its own level, and the rule repeats inside every folder: a folder's top level is a short list of subfolders and at most a README; files live at the deepest folder that owns them. Target: root has 4 folders and a handful of files that tools require there; no folder has more than about 8 entries at its top level.

## 2. Target tree (the author's answers to the shape: five areas, papers into docs/archive, status files into docs/)

```
README.md  AGENTS.md  CNAME  robots.txt  .gitignore        root files tools require
.github/  .claude/                                         tool folders, stay
model/
  v1/   v2/   v3/                                          model_v1, model_v2, model_v3 (v3: core, runner, out, pack, levers, OUTPUTS, tests)
  data/                                                    'Rates Data' (model inputs)
research/
  sources/                                                 Research/ (PDFs, ETB xlsx) and the model's literature
  notes/                                                   docs/research/ (derivations)
web/
  site/   pipeline/   registry/   tests/                    site, pipeline, registry, tests (page, gate, cards, data)
docs/
  project/STATUS.md  project/OVERVIEW.md  project/START_HERE.md                    moved from root
  briefs/  agents/  archive/  decisions.md  todo.md        as now
  restructure/  model-v3/  model-audit/  model-lessons/    as now (model-v3 may move to model/v3/docs/, see 4)
  archive/papers/                                          source/ (old papers), see 3
  skills/                                                  Tools/ (the .skill files)
```

## 3. Open points (decide when the move brief starts, not now)
1. **Papers.** The author put `source/` (33 files, the old papers) under `docs/archive/papers/`. The site build reads `source/` today and the restructure writes the hub at `source/hub.md` with drafts under `/draft/`. Archiving the old papers is only safe once the hub and spokes replace them; the new live content needs a home (proposal: `web/content/`). The move brief must not archive `source/` before that.
2. **`docs/model-v3/`.** It is the design record of the model and the input register. Proposal: it moves to `model/v3/docs/`; the author has not said.
3. **Tests.** Proposal: model tests with the model (`model/v3/tests/`), page, gate, cards and data tests with `web/tests/`.
4. **Build and deploy.** `.github/workflows/deploy.yml` builds from `site/`, `source/`, `pipeline/` and `_build/`; the live URL `/model/` is kept (`site/_quarto.yml`). CNAME and robots.txt must reach the published site root.

## 4. Size of the job (references to the old paths in tracked files outside the archive)
`pipeline/` 74 files, `docs/` 85, `source/` 48, `registry/` 44, `site/` 42, `model_v1` 24, `model_v2` 23, `Rates Data` 20, `Research/` 12, `tests/` 12, `Tools/` 7, `model_v3` 7; `project/STATUS.md` and `project/OVERVIEW.md` 13 each, `project/START_HERE.md` 6. A move is `git mv` plus a rewrite of every reference (code, YAML, workflow, briefs, the skills under `Tools/`, `.claude/`), so a script that lists every reference and a check that the site still builds and all tests pass bound the job.

## 5. Order
1. Model v3 build (040g, then the build briefs) and the restructure gates run on today's paths.
2. Brief 044c does the move in stages: inventory, then folder moves with the reference rewrite per area (research, model, web, docs), the deploy last.
3. Briefs still open at that time are rewritten by the guru.
