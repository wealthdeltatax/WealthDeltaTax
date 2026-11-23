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

### 2026-11-23 · 140c · code
- **Instruction:** 140c Block 1 (run F1 at five scenario points on 128c paths); `docs/model-v3/household-arm-paths.md` (two of five points raise I1).
- **Happened:** the brief does not say what to do when the arm raises I1 on a path; the first run stopped at `min_mid`, schedule point 7 (`ValueError: I1 fails: the book's family value is not the class total...`).
- **Cost:** about 6 minutes and a rerun; the script now records each failed cell (12 of 135) and carries on, as the stop rule (no model change) implies.
- **Suggest:** briefs that run the household arm on per-path returns say "record an I1 alarm per cell, do not work around it".
