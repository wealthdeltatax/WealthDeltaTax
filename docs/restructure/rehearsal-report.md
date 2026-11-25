# Rehearsal of the whole move (165c)

Scratch copy: full-history clone of `3efb03b`, `path_refs.py --apply` (map csv of 044c, no map change), then fixes. Tags in the scratch copy: `applied` (apply only) and `fixed` (apply + fixes). `rehearsal-fixes.patch` is `applied..fixed` (138 files), hunks grouped by stage and labelled `# ===== stage NNNc`; it applies cleanly to `applied`. The scratch copy is deleted at the end; to redo, run `python pipeline/path_refs.py --apply <clone at 3efb03b>` and the patch.

## Result

| Check, on `fixed` | Result |
|---|---|
| `move_tripwire.py` against the baseline | PASS (inputs, legacy digest, pack rebuild byte-identical, 4 evaluation cases) |
| `tests/model/data` | 103 passed |
| `tests/model/gate` | 17 passed |
| `tests/model/tools` | 5 passed (1 failure on first run, fixed, see 162c) |
| `tests/model/model_v3` | 408 passed (10 min) |
| `tests/project` | 15 passed, 1 failed in a clean tree: `test_check_agent_docs.py::test_cli_exit_status_and_real_repo_is_clean`, because of the 37 findings of the prose sweep (164c below); it passed in the used copy only because of leftover empty folders |
| `tests/website` | 201 passed, 41 skipped (40 of them `layout`, skipped in the baseline too) |
| `path_rewrite_proof.py`, `--head applied` | 328 path-only, 769 moved, 7 removed, 0 changed, 1 added (the 165c brief, not in the csv) |
| `path_refs.py --check` equivalent on `fixed` | 94 old-path tokens left, all explained below |

Every suite fails at collection on `applied` (depth shifts, constructed paths), as expected; every model and website suite passes on `fixed`.

**Trap for the stage agents.** The tree after `git mv` keeps empty old folders (`model_v3/`, `pipeline/`, `site/`, `source/`, `docs/research/`, with only `__pycache__` in them) when tests have run. They make `check_agent_docs.py` and any `exists()` test pass although the path is gone. Run `git clean -fdx` (or use a fresh checkout) before the final run of a stage. I found this because the project test passed in the used copy and failed in a clean one.

## Fixes by stage

Each fix is mechanical enough to script; the scripts used are described, not shipped. Counts are from the run.

### 160c: data, literature, research (35 files)
- **Pack folder name.** The pack loader (and `country-pack.md`) require folder name == manifest country. The map sends `data/country-packs/GBR/` to `data/country-pack-GBR/`: loading fails. Rehearsed as `data/country-packs/GBR`. **Map error, for the guru**: either `data/country-packs/GBR` or loader change (not a path rewrite).
- **Pinned bytes the pinned list does not cover** (the tripwire hashes the pack tree, so the rewrite breaks it): `NOTICE.md` and three strings written by `build_gbr.py` (the builder regenerates NOTICE.md and manifest.json: its output text must equal the committed bytes); the pack `manifest.json` has more than the pinned line 104. Fix: keep the old citations in those strings and files. **Map gap**: the pinned list needs these.
- `tests/model/data` conftest: pipeline folder constant.
- `to_markdown.py` and `check_agent_docs.py` mirror `docs/research` (split by the move): pointed at `literature/` for readable copies and the `--all` scan. Design decision for 160c: the readable-copies folder now lives with the literature, so the 8 PDFs of `literature/` that have no reading copy only warn, as before.
- `config.py` filter on `papers/legacy/` (prefix of the old `source/`).
- `readable-copies-index.md`: the map renames `readable/INDEX.md`; the tool writes the name from a constant.
- Research scripts: depth shifts (`parents[k]`).

### 161c: website (25 files)
- Conftests of `tests/website/{nav,pages,retired,hooks,cards,glossary}`: `pipeline/` and `site/` directories in `sys.path` and root derivation (depth +1).
- Hook modules: `validate_outputs.py` lives in `model/tools`, the other hook modules in `website/build`: the loader needs both.
- Glossary: the repository root is three folders above `website/registry/glossary.yml`, no longer two.
- Legacy pages: prefix filter on the old `source/` folder.

### 162c: model code and inputs (60 files)
- **Two import roots.** `model_v3` now sits under `model/`, so every `sys.path` insertion of the repository root becomes `ROOT / 'model'` (20 lines); tests import both.
- **Depth.** `Path(__file__).parents[k]` 50 lines, `.parent` chains 13, `HERE`/`DIR` chains 5; `os.path.dirname` nests as needed. Rule: a file whose depth changes by d moves every root-reaching count by d.
- **Constructed paths** the finder cannot see (`ROOT / 'docs' / 'model-v3' / 'outputs.yml'`): 161 chains rewritten from the map. 50 chains name paths the map does not list (generated outputs and folders): not individually triaged, no suite fails on them.
- **Split study folders.** `docs/model-v3/<study>` splits into code (`model/studies/<study>`) and data (`results/<study>`); a variable or a `sys.path` line naming such a folder cannot be rewritten as one path. Rule used: `sys.path` means the code folder; `VAR / 'file'` becomes the file's own new path (6 variable uses, 12 inline, 1 relative chain).
- `run_suites.py` discovered `tests/<name>`; after the move suites sit in `tests/model`, `tests/website`, `tests/project`. Fix: discover both layouts, run each by its real path.
  - The test of `run_suites` builds a throwaway flat tree (`tests/model/gate/...`) and asserts on its paths: the automatic rewrite had changed the expected strings to `tests/model/...` (the one failure of `tests/model/tools`). Fixed by restoring the expectation. **General lesson**: a test that builds its own tree and asserts on paths inside it must keep those paths; the rewrite cannot know. Same with the gate conftest's f-string tree.
- `G5_TEST_DIRS` of `check_gate`: `tests/hooks` split into `tests/website/hooks` and `tests/project/tools`.
- `inputs.json` is generated from `inputs.md` and pinned (`inputs_sha256`): its stale citation on line 568 comes from `inputs.md` line 145, which must keep the old text. **Map gap**: the pinned list names the json line, not its source line.
- `outputs.yml` is hashed (`manifest_sha256` in the fixture and in every stored run): its comment line naming `docs/restructure/shortcodes.md` must keep its old text. **Map gap**: a sixth pinned file.

### 163c: specs and results (3 files)
Only the three pinned lines above reach this stage (`inputs.md` line 145, `outputs.yml`, `inputs.md` readers). Nothing else in `model-specs/` or `results/` is read by code beyond what the depth and constructed-path passes cover.

### 164c: project, skills, final sweep (15 files)
- Project tools and their throwaway trees (`tests/project/tools`): same rule as the `run_suites` test.
- The five `.skill` archives are generated from the stubs whose text the rewrite changed: regenerate (`project/skills/*.skill`). Committed archives become stale otherwise.
- **The prose sweep.** 94 old-path tokens remain after the apply, and `check_agent_docs.py` reports 37 findings in a clean tree: all name an old folder whose files went to several new places, so no single path replaces it. `source/` 9, `pipeline/` 7, `model_v3/` 5, `docs/research/` 5, `docs/archive/` 4, `site/` 3, `docs/` 3, `registry/` 1, in `AGENTS.md` (14), `project/START_HERE.md`, `project/agents/*.md`. They need a rewrite by hand (name each target folder); that is the 164c final sweep. The rest: `path_refs.py`'s own map text (11, deliberate: it describes the old layout), the briefs 044c/057c/160c to 165c (they describe the move), pinned strings (above), `model-specs/` prose citing old code paths in 7 places, and one `lane-plan.html`.

## The proof and the apply disagreed

Before this work, `path_rewrite_proof.py` and the apply step had two different ideas of the rewrite. On `applied` the proof reported 198 changed files; the proof's rewriter used one regular expression over every key, which rewrote prose words (`site`, `source`) and ignored folders whose files include a renamed file, so it called correct edits wrong and, in a few files, missed wrong ones. I made `path_refs.py` expose one `Rewriter` class that `--apply` uses, and ran the proof with it: 0 changed on `applied` (table above). The change to the proof is **not in the repository**: the brief forbids changing a check, so it is for the guru to accept. It is small (the `rewriter()` function becomes a call to `path_refs.Rewriter(...).text`, looked up in `pipeline/` or `project/tools/`); the diff is in the session scratchpad and I can attach it to the change report on request.
With `--allow` (the 138 files of the patch) the proof on `fixed` shows only the declared differences, plus the 13 files of the pack rename (the folder-name decision).

## Depth-based lines (`file-layout-depth.csv`, 498 lines)
Pass 1 changed 94 files: 50 + 13 + 1 + 4 root-reaching counts; none of the others fails a suite. Lines that do need the change are exactly those: `parents[k]` with k reaching the root, `.parent` chains of length >= depth, `HERE`/`DIR` variants. Files whose depth is unchanged need nothing.

## Not run
Quarto build; `tests/website/layout` (40 skipped, same as the baseline); the full `quick` comparison; the research and write scripts that only run on demand (no suite calls them).

## Decisions needed (map is not changed here)
1. Pack folder: `data/country-packs/GBR` (loader needs folder == country) instead of `data/country-pack-GBR`.
2. Pinned list: add `NOTICE.md` and the `build_gbr.py` strings, the whole pack `manifest.json` strings, `outputs.yml` line (shortcodes citation), `inputs.md` line 145.
3. Take the shared `Rewriter` into the proof (above).
4. Readable copies live under `literature/readable/`: confirm.
5. Add the 165c brief to the map csv (or let each stage's `--apply` report it).
