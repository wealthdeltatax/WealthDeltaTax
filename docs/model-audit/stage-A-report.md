# Change report: 001c stage A (v1 inventory and mechanism)

The brief's `Touches` is `docs/model-audit/` only, so this report lives here instead of in the brief's Implementation notes.

```
Change report
- Task: 001c stage A, audit of model v1 (inventory and mechanism). No code changed.
- Files changed: docs/model-audit/v1-inventory.md (new, the checkpoint note); docs/model-audit/stage-A-report.md (new, this report)
- What is different now: the repo has a verified account of what model_v1 contains, how it depends on itself, what it outputs and which paper uses which output
- New or changed interfaces: none
- Acceptance criteria:
  - Stage A checkpoint file exists and meets its check: met. All 21 `model_v1/*.py` names appear in v1-inventory.md (grep loop, 0 missing)
  - `git diff --stat` only under docs/model-audit/: met (2 new files, see Verification)
  - Each claim about the code cites a file and function name: met for code claims; two statements rest on docs/model-lessons/mechanics.md and are marked as such in the note (SSM uniform-return floor, section 5.3)
  - Every error carries a number or reproducible check: not applicable at stage A (errors are stage B). Facts that look like errors carry numbers (8 of 16 run_all entries cannot start; 6 import failures with file and line)
- Deviations from the brief: (1) change report is in docs/model-audit/, not the brief, because of the Touches limit. (2) The brief's "Read" line says `registry/contents.yml` lists figures and tables; it lists sections only. Outputs were mapped to papers by matching image embeds in source/*.md instead
- Risks / follow-ups:
  - model_v1 does not import as shipped (`rates_core` vs `rates_core1.py`); 8 of 16 run_all entries fail. Not fixed (audit only). Logged in docs/brief-suggestions.md already for wdt_analytics; the guru should widen that entry
  - Tracked OUTPUTS are dated 2026-09-28 to 2026-09-30, before the rename; not regenerated
  - Paper 19 embeds 3 figures (4.1e/f/g) that no code produces, and 3 with a doubled `fig_` prefix
  - My question text said "about 14,000 lines"; the correct total is 18,136
- Verification: import tests of all 10 core/base modules and all 11 numbered scripts; numeric snippets for tau, run_pair, decompose_tw_advantage (identity residual 1.6e-13), SSM fill years and the 73-year sweep (9.5 s); 4 test scripts (320 assertions pass, 1 file cannot import). `git status` showed no change outside docs/model-audit/ after every run. Not run: run_all, any core main, any table or chart script, regeneration of OUTPUTS
- Overview sections likely needing an update: section 6 (add: v1 import break; OUTPUTS dated September; paper 19 figure gaps). Section 2 `model/` line should read `model_v1/`
- Commit / branch: brief/001-model-audit
```
