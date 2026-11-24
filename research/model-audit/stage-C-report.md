# Change report: 001c stage C (v2 inventory and mechanism)

The brief's `Touches` is `docs/model-audit/` only, so this report lives here, as for stage A.

```
Change report
- Task: 001c stage C, audit of model v2 (inventory and mechanism). No model code changed.
- Files changed: docs/model-audit/v2-inventory.md (new, the checkpoint note); docs/model-audit/stage-C-report.md (new, this report)
- What is different now: the repo has a verified account of what model_v2 contains, how it depends on itself, what it outputs, how it differs from v1 and from the papers
- New or changed interfaces: none
- Acceptance criteria:
  - Stage C checkpoint exists and meets its check: met. All 29 `*.py` files in model_v2 (excluding audit_d0/Research) appear in v2-inventory.md (grep loop, 0 missing)
  - `git diff --stat` only under docs/model-audit/: met (2 new files)
  - Each claim about the code cites a file and function: met; claims resting only on WDT_Code_Reference.md or docstrings are marked [doc]
  - Every error carries a number or reproducible check: not applicable at stage C (v2 errors are not in scope). Facts that look like faults carry numbers: eval_core import failure (line 62), v1/v2 run_pair table
- Deviations from the brief:
  (1) Import tests of `wid_checks.py` and `wid_summarise.py` executed their module-level code (no main guard) and rewrote CSV/JSON under model_v2/wid_out/summary and summary2, twice (my second run did not exclude them). `git status` was clean afterwards, so the files were byte-identical to the tracked ones; nothing changed in the repo. This breaks the brief's "model folders are read, never run" in letter. I did not import them again.
  (2) Change report is in docs/model-audit/, not the brief, because of the Touches limit.
- Risks / follow-ups:
  - v2 `simulate` uses a different basis convention from v1 (post-surrender basis); same inputs give different net_pct and tw_gap (+0.0132 vs +0.0093 at alpha 1.5). BASIS_CHANGE.md is cited in code but not tracked. Stage B/E should decide whether the v1 convention is a register item.
  - The papers' embedded figure names (19) match none of v2's output names. The papers' RATES numbers (73 UK start years, SRR year 3, logistic 15% to 70%) are not what v2's baseline (gain ladder, JST windows, T = 100) computes. This does not say a published figure depends on a v1 error, so I did not stop under the brief's open question; the author may want to read it as one.
  - eval_core.py cannot import in v2 (missing wfr_core, retired TOML sections).
  - WDT_Code_Reference.md names four test files that do not exist in the repo.
  - Suggest widening the existing brief-suggestions entry on import side effects in wid_checks.py / wid_summarise.py (not logged by me).
- Verification: AST inventory of all 29 files; import tests of 24 files (23 ok, eval_core fails); AST name-resolution check of all cross-module references (0 unresolved); numeric snippets: load_params time, tau on the gain ladder and on v1 logistic, run_pair at alpha 1.5, 1.0, 0.5 in v1 and v2; function-source diff v1 vs v2 wdt_core; figure-name regex match against source/*.md. Not run: any core main, table or chart script, jst_r6.json, test scripts (none exist for the cores)
- Overview sections likely needing an update: section 6 (add: v2 eval_core orphaned; basis-convention change; name mismatch with papers; import side effects in two WID scripts)
- Commit / branch: brief/001-model-audit; merged to main by the guru on 2026-11-16 after review (see Guru review below)
```

## Guru review (2026-11-16)
- Spot-checked: 29 `.py` files and 19,558 lines; `WDT_Params.toml` 1,839 lines; `eval_core.py` line 62 imports `wfr_core` (not in v2); `BASIS_CONVENTION = 'post'` at `wdt_core.py` line 121 and no `BASIS_CHANGE.md` in the folder; none of the four test files named by `WDT_Code_Reference.md` exists; `wid_checks.py` and `wid_summarise.py` have no `main` guard. All hold.
- Deviation 1 (importing the two WID scripts ran their module code and rewrote files under `wid_out/`): accepted. `git status` was clean after it, so the files were byte-identical; the import side effect is itself a finding (add to `docs/brief-suggestions.md` if v2 data tooling survives).
- The author's rule (2026-11-16): v1 and v2 are not fixed, only learned from. The v1/v2 basis-convention difference is therefore a lesson (same inputs, different answers, no tracked note of why), not a bug to resolve.
