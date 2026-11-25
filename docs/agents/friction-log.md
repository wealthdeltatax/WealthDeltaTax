# Friction log

Any agent appends here when the **instructions, workflow or tooling** failed it: a rule that was missing, stale or contradictory, a command that does not work as written, an ambiguity that forced a guess. Log only what cost time or caused a wrong action. Not here: a flaw in the brief (change report), work for a new brief (`docs/brief-suggestions.md`), preferences.

Append at the bottom, at most four lines per entry, when it happens (commit it with your next checkpoint). Never edit or delete another entry; only the guru sets `Status`. The file merges with git's union driver (`.gitattributes`), so concurrent appends do not conflict.

Entry format:
```
### <date> · <brief or task> · <role>
- Instruction: <file and section, or "none: missing">
- Happened: <what went wrong, with the first error line>
- Cost: <time lost, rework, wrong action, blocked>
- Suggest: <optional one line>
```
The guru adds `- Status: open | fixed <commit> | dropped (reason)` when triaging. One entry is noted; two on the same instruction mean the guide is edited. Fixed and dropped entries move to `docs/archive/friction-log-archive.md`; keep this file under about 100 lines.

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
- **Instruction:** 140c Block 1 (run F1 at five scenario points on 128c paths); `docs/model-v3/household-arm-paths.md` (two of five points raise I1).
- **Happened:** the brief does not say what to do when the arm raises I1 on a path; the first run stopped at `min_mid`, schedule point 7 (`ValueError: I1 fails: the book's family value is not the class total...`).
- **Cost:** about 6 minutes and a rerun; the script now records each failed cell (12 of 135) and carries on, as the stop rule (no model change) implies.
- **Suggest:** briefs that run the household arm on per-path returns say "record an I1 alarm per cell, do not work around it".

- 149c: the brief did not say what to do when the arm raises its I1 alarm in a cell (1, 3 and 5 cells at 6, 15, 30 phases) or when a 140c cell stops running (`tm90_k2_r025`). I recorded the cells per cell, left them out of the tables and merged nothing. A rebase onto main also needed an explicit `--force-with-lease=<branch>:<sha>` because the shallow clone has no remote ref.

- 140c (market): the `check` command compares to stored 128c rows that 135c/138c regenerated, so it reports DIFFERENT at the short horizon on an unchanged model; the brief's acceptance names only the 124c reproduction, so I used that and noted the rest.

### 2026-11-24 · 148c block 3 · code
- Instruction: `docs/briefs/148c-...md` Block 3 ("five grid points ... ledger tie") and `run_grid.py` checks.
- Happened: the brief names no grid points for the floor and withdrawal runs, and `run_grid.py`'s ledger check reads only the first chunk's main-spec run, which carries no lien at `min_mid`: the first floor 50 rerun printed write-off 0 and a tie identical to floor 0.
- Cost: about 40 minutes and two reruns; I chose `min_mid` and `median_high` (the 127c lien points) and added `flow_ties.py`, which checks the tie on every `core_run`.
- Suggest: briefs that rerun lien switches name the points and say the tie is checked on every core run, not only the main one.


### 2026-11-24 · 009c · code
- Instruction: 009c Design 1 ("push the tag"); `docs/agents/code.md` does not say tag pushes are blocked.
- Happened: `git push origin legacy-models-2026-11` fails with `RPC failed; HTTP 403` from the session proxy (branch pushes work).
- Cost: the tag acceptance criterion cannot be met from the session; the author pushes it.

### 2026-11-24 · 044c R1 round 2 · code
- Instruction: `docs/restructure/move_tripwire.py` docstring and 044c "How each stage proves it broke nothing"; the shallow-clone warning is only in `docs/agents/code.md` for "pack work".
- Happened: in a depth-50 clone the tripwire reports `FAIL: ['pack']` (`rebuild_is_byte_identical: false`, tree hash equal) because `build_gbr.py` reads `retrieved` dates from `git log --follow`.
- Cost: one failed run and a history fetch (`git fetch --depth=5000 origin main brief/044-inventory` gave the full 809 commits); the rerun passed.
- Suggest: say in the tripwire docstring and the stage briefs that it needs a full-history clone.

### 2026-11-24 · 160c · code
- Instruction: 044c "How each stage proves it broke nothing" and the map's pinned list; `python pipeline/path_refs.py --check` after a stage.
- Happened: (1) `--check` builds its map from the current tree, so once files have moved every old path is "not a tracked file" and nothing is reported; the stage had to use its own scan from the committed map. (2) The pinned list names four lines, but `model_v3/pack/GBR/NOTICE.md` (hashed in the tripwire's pack tree) and the NOTICE text inside `build_gbr.py` also quote moved paths; only the path constants that open files could change. (3) `pipeline/to_markdown.py`, `pipeline/check_agent_docs.py` and their two tests assume sources and reading copies share one root (`docs/research`); after the split that is a logic change, so they were left. (4) A Python `read_text`/`write_text` path rewrite turns CRLF into LF; six CRLF tables showed as changed in the proof until redone on bytes. (5) The proof run on a subset map lists every other file as "added" (795 lines).
- Cost: extra analysis and one extra commit.
- Suggest: add NOTICE.md and the build_gbr.py text to the pinned list or re-baseline the tripwire; a brief to re-root the converter and the reading-copy warning; make `--check` read old paths from the committed map; give the proof a `--stage` filter and a bytes warning.
