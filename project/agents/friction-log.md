# Friction log

Any agent appends here when the **instructions, workflow or tooling** failed it: a rule that was missing, stale or contradictory, a command that does not work as written, an ambiguity that forced a guess. Log only what cost time or caused a wrong action. Not here: a flaw in the brief (change report), work for a new brief (`project/brief-suggestions.md`), preferences.

Append at the bottom, at most four lines per entry, when it happens (commit it with your next checkpoint). Never edit or delete another entry; only the guru sets `Status`. The file merges with git's union driver (`.gitattributes`), so concurrent appends do not conflict.

Entry format:
```
### <date> · <brief or task> · <role>
- Instruction: <file and section, or "none: missing">
- Happened: <what went wrong, with the first error line>
- Cost: <time lost, rework, wrong action, blocked>
- Suggest: <optional one line>
```
The guru adds `- Status: open | fixed <commit> | dropped (reason)` when triaging. One entry is noted; two on the same instruction mean the guide is edited. Fixed and dropped entries move to `project/agents/friction-log-archive.md`; keep this file under about 100 lines.

## Entries

### 2026-11-21 · 104r · research
- Instruction: brief 104r `Resume` text and wdt-research skill (branch naming).
- Happened: the branch is `brief/104`, not `104r`; the clone tracks main only; main moved during the brief, so the rebase needed `git push --force-with-lease` after a non-fast-forward rejection.
- Cost: one failed push and a lookup. A parallel 102r run was superseded mid-brief.

### 2026-11-23 · 131r · research
- **Instruction:** 131r Decisions and Block 1: flag each published figure `table` or `read from chart`.
- **Happened:** the IFS report has no data table of uplifts; its figures are in running text and charts, so a third value `text` was needed (acceptance criterion 1 names only the two).
- **Cost:** a wording guess; none otherwise.
- **Suggest:** research briefs that extract from a report name the flags `table`, `text` and `read from chart`.

### 2026-11-23 · 145r · research
- Instruction: brief 145r `Resume` line (branch name).
- Happened: it names `brief/145-withdrawal-saving-evidence`, which does not exist; the pushed branch is `brief/145-withdrawal-and-saving-evidence`.
- Cost: a lookup; corrected in the brief.
### 2026-11-23 · 140c · code
- **Instruction:** 140c Block 1 (run F1 at five scenario points on 128c paths); `model-specs/household-arm-paths.md` (two of five points raise I1).
- **Happened:** the brief does not say what to do when the arm raises I1 on a path; the first run stopped at `min_mid`, schedule point 7 (`ValueError: I1 fails: the book's family value is not the class total...`).
- **Cost:** about 6 minutes and a rerun; the script now records each failed cell (12 of 135) and carries on, as the stop rule (no model change) implies.
- **Suggest:** briefs that run the household arm on per-path returns say "record an I1 alarm per cell, do not work around it".

- 149c: the brief did not say what to do when the arm raises its I1 alarm in a cell (1, 3 and 5 cells at 6, 15, 30 phases) or when a 140c cell stops running (`tm90_k2_r025`). I recorded the cells per cell, left them out of the tables and merged nothing. A rebase onto main also needed an explicit `--force-with-lease=<branch>:<sha>` because the shallow clone has no remote ref.
### 2026-11-23 · 057c · code
- **Instruction:** `acceptance.md` section 1 and `architecture.md` 6.4 give `python -I -m model_v3.run ...` as the run and smoke command.
- **Happened:** `-I` ignores the current directory, so `No module named 'model_v3'`; the command cannot work as written (the code guide's import-check rule says the same for imports).
- **Cost:** about 10 minutes (a smoke run started and failed unseen); fixed by `python -I -c "import sys; sys.path.insert(0, '.'); from model_v3 import run; run.main([...])"` in `accept.sh` and `test_smoke.py`.
- **Suggest:** the guru amends the two command lines in `acceptance.md` and `architecture.md` 6.4 to the `-I -c` form.

### 2026-11-23 · 057c · code
- **Instruction:** brief 057c Touches lists `run.py`, the two test files, `accept.sh`, `decisions.md` and the brief; block 1 also names "validator change", and the null marker needs `assemble` handling.
- **Happened:** `model/tools/validate_outputs.py` (markers, `pending` entry field) is outside Touches, so the merge rule fails; `model/model_v3/out/assemble.py` was left untouched by marking in `run.py` instead.
- **Cost:** merge blocked (`NEEDS THE AUTHOR`) until Touches names the validator.
- **Suggest:** add `model/tools/validate_outputs.py` to 057c's Touches (and `tests/data` if its pins move).

### 2026-11-23 · 057c · code
- **Instruction:** `AGENTS.md` Auto-merge: "`git fetch`, rebase the branch on `origin/main`".
- **Happened:** the session clone is shallow (depth 1) and `origin/main` was force-updated, so branch and main shared no history; `git rebase` and `git cherry-pick` replayed or conflicted on the whole tree (about 20 add/add conflicts in files I never touched).
- **Cost:** about 15 minutes; fixed by `git fetch --depth=50 origin main`, then rebasing (which then worked), or applying only my own diff with `git diff A B | git apply --3way`.
- **Suggest:** the guide says to `git fetch --depth=50 origin main` before a rebase in a shallow session clone.

- 057c round 3: the ruling "OW1 under the household arm is withheld" suggests a manifest `arms: [legacy]` entry, but 126c pins that no id is restricted to the legacy arm (8 tests fail). Done in the validator (`MAY_WITHHOLD`) instead; the brief should say which of the two is meant.

- 140c (market): the `check` command compares to stored 128c rows that 135c/138c regenerated, so it reports DIFFERENT at the short horizon on an unchanged model; the brief's acceptance names only the 124c reproduction, so I used that and noted the rest.

### 2026-11-24 · 057c · code
- Instruction: `project/agents/agent-code.md` (running tests): none says that `pytest tests/data tests/hooks tests/model_v3` in one call fails (`ImportError: cannot import name 'INPUTS_JSON' from 'conftest'`).
- Happened: one call over several test directories clashes on the three `conftest.py` files; also `git fetch -q origin main <branch>` in a shallow clone leaves no `origin/<branch>` ref (use `git ls-remote`).
- Cost: about 10 minutes; fixed by one pytest call per directory.
### 2026-11-24 · 148c block 3 · code
- Instruction: `project/briefs/open/148c-...md` Block 3 ("five grid points ... ledger tie") and `run_grid.py` checks.
- Happened: the brief names no grid points for the floor and withdrawal runs, and `run_grid.py`'s ledger check reads only the first chunk's main-spec run, which carries no lien at `min_mid`: the first floor 50 rerun printed write-off 0 and a tie identical to floor 0.
- Cost: about 40 minutes and two reruns; I chose `min_mid` and `median_high` (the 127c lien points) and added `flow_ties.py`, which checks the tie on every `core_run`.
- Suggest: briefs that rerun lien switches name the points and say the tie is checked on every core run, not only the main one.


### 2026-11-24 · 009c · code
- Instruction: 009c Design 1 ("push the tag"); `project/agents/agent-code.md` does not say tag pushes are blocked.
- Happened: `git push origin legacy-models-2026-11` fails with `RPC failed; HTTP 403` from the session proxy (branch pushes work).
- Cost: the tag acceptance criterion cannot be met from the session; the author pushes it.

### 2026-11-24 · 044c R1 round 2 · code
- Instruction: `project/restructure/move_tripwire.py` docstring and 044c "How each stage proves it broke nothing"; the shallow-clone warning is only in `project/agents/agent-code.md` for "pack work".
- Happened: in a depth-50 clone the tripwire reports `FAIL: ['pack']` (`rebuild_is_byte_identical: false`, tree hash equal) because `build_gbr.py` reads `retrieved` dates from `git log --follow`.
- Cost: one failed run and a history fetch (`git fetch --depth=5000 origin main brief/044-inventory` gave the full 809 commits); the rerun passed.
- Suggest: say in the tripwire docstring and the stage briefs that it needs a full-history clone.

### 2026-11-24 · 160c · code
- Instruction: 044c "How each stage proves it broke nothing" and the map's pinned list; `python project/tools/path_refs.py --check` after a stage.
- Happened: (1) `--check` builds its map from the current tree, so once files have moved every old path is "not a tracked file" and nothing is reported; the stage had to use its own scan from the committed map. (2) The pinned list names four lines, but `data/country-packs/GBR/NOTICE.md` (hashed in the tripwire's pack tree) and the NOTICE text inside `build_gbr.py` also quote moved paths; only the path constants that open files could change. (3) `project/tools/to_markdown.py`, `project/tools/check_agent_docs.py` and their two tests assume sources and reading copies share one root (`docs/research`); after the split that is a logic change, so they were left. (4) A Python `read_text`/`write_text` path rewrite turns CRLF into LF; six CRLF tables showed as changed in the proof until redone on bytes. (5) The proof run on a subset map lists every other file as "added" (795 lines).
- Cost: extra analysis and one extra commit.
- Suggest: add NOTICE.md and the build_gbr.py text to the pinned list or re-baseline the tripwire; a brief to re-root the converter and the reading-copy warning; make `--check` read old paths from the committed map; give the proof a `--stage` filter and a bytes warning.
### 2026-11-24 · 161c · code
- Instruction: 161c Design ("web tests ... gate") against `file-layout-map.md` case 7 and 10 (`check_gate.py`, `tests/model/gate` belong to the model move (162c)); and `path_rewrite_proof.py`, which applies the map to generic words.
- Happened: the brief and the map disagree on the gate (followed the map, stage 162c owns it); the proof reports `source:`, `site` and the nav label `Tools` as "changed" (map applied to plain words), so 46 files show red although only intended edits remain.
- Cost: a manual review of the diff to tell intended depth and path edits from proof noise.
- Suggest: make the proof apply the map to path-like tokens only (a slash or an extension), and say in each stage brief where the gate lives.
### 2026-11-25 · 165c · code
- Instruction: 165c "Fix in the scratch copy what can be fixed" and "do not change a check to make it pass"; 044c says the proof and the apply step share one rule, but they were two implementations.
- Happened: the proof reported 198 changed files on a correct apply (its regular expression rewrote prose words and ignored folders holding a renamed file); and after `git mv` the used tree keeps empty old folders that make `exists()` checks pass.
- Cost: about two hours chasing differences that were the proof's, and one project test that passed in the used copy and failed in a clean one.
- Suggest: the stage briefs say "run the stage's final checks in a fresh checkout (`git clean -fdx`)"; the proof uses `path_refs.Rewriter`.

- 2026-11-25, 162c: `path_refs.py --check` prints only the first 50 findings (`left[:50]`), so pinned lines past 50 stay invisible; the proof's before and after counts need a stage map (rows of other stages held to identity), which the brief does not name.

### 2026-11-25 · 163c · code
- Instruction: 163c "tripwire clean"; `project/agents/agent-code.md` warns about shallow clones only for "pack work".
- Happened: the session's clone of the repository was shallow (16 commits), so the scratch copy's tripwire reported `FAIL pack` (`model_v2/jst_r6.json is not in git history`); same cause as the 044c entry. A second slip: switching the scratch copy to another commit while a suite ran in it made that run void (rerun, 10 minutes).
- Cost: one extra tripwire run and one extra `model_v3` run.
- Suggest: `code.md` says "run `git fetch --unshallow` first in every session that runs the tripwire"; run a stage in a scratch clone and bring it back with `git merge --squash`, never touch the clone while suites run.

- 2026-11-26, 168c: the brief says `gh workflow run --ref <branch>` starts a new workflow once pushed; GitHub returns 404 for a workflow file that is not on the default branch, so the agent cannot start the first run without a merge of the skeleton to main. Also `accept.sh` step 1 (`python -I -m pytest`) fails at collection, and the digest fixtures depend on the CPU (AVX512 path of numpy).

### 2026-11-27 · 176c · code
- Instruction: 176c "Checks to run: `python model/tools/run_suites.py tools` and `project` suites".
- Happened: `run_suites.py` knows only suites that hold a `conftest.py`; `tests/model/tools` and `tests/project` have none, so both names are refused (`unknown suite(s)`). Also the acceptance line "the small cases total under 3 minutes on this 2-core machine" was set from the 150c figures (about 176 s); this session's machine runs the same cases about 1.5 to 2 times slower (see the change report).
- Cost: a few minutes; ran `python -m pytest tests/model/tools` and `tests/project` directly (12 and 22 passed).
- Suggest: briefs name the pytest path for suites that `run_suites.py` does not list, or `run_suites.py` lists every `tests/` folder with tests; a time criterion names the machine's measured speed (bench header) or is stated as a ratio to a bench baseline.

## 180c (compiled kernel spike)
- Instruction: 180c acceptance "all suites pass with `WDT_KERNEL` unset".
- Happened: the `model_v3` suite has no stated run time; `test_converge.py` and `test_heads_only.py` run full evaluations (minutes per test), so one process was still under 20% after 15 minutes on 2 cores, and the CPU contention spoiled a timing run I had started alongside.
- Cost: about 40 minutes of waiting; one timing run repeated.
- Suggest: the check lists name a fast subset (and the expected total time) for a change that touches no file the numpy path imports, and say never to time while a suite runs.
- Instruction: 180c Touches (`kernel.py`, `kernel_jit.py`) with the goal "hot year-loop body only".
- Happened: the year loop's cost is mostly the household hook in `runner/arm.py` (37% of `eval_hh_20`), which is not in Touches, so the switch could not be put in the loop as designed; I installed the compiled functions into `core.household` instead.
