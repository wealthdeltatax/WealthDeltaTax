# Change report: 001c stage D (v2 complication and tests)

The brief's `Touches` is `docs/model-audit/` only, so this report lives here, as for stages A and C.

```
Change report
- Task: 001c stage D, audit of model v2 complication and tests. No model code changed.
- Files changed: docs/model-audit/v2-complication.md (new, the checkpoint note); docs/model-audit/stage-D-report.md (new, this report)
- What is different now: the repo has a measured account of what v2 added over v1, which additions the papers name, the three largest sources of complexity with line counts, and what is and is not tested
- New or changed interfaces: none
- Acceptance criteria:
  - Stage D checkpoint exists with three named sources of complexity, each with a line count: met (output layer 5,150; valgen_core 3,353; eval_core 2,718)
  - git diff --stat only under docs/model-audit/: met (4 new files on the branch vs main)
  - Each claim cites a file and function: met; estimates and unchecked items are marked and listed in section 6 of the note
  - Every error carries a number or reproducible check: not applicable (errors are not in stage D); size and test facts carry numbers
- Deviations from the brief:
  (1) I ran test/test_hlc_drift.py (the only v2 test, 0.2 s, read-only, no --write). The brief names no test commands, so this is within "run them if under 5 minutes". Result: exit 0 with one WARN (placeholder HLC).
  (2) My first draft of the note had wrong figures (an output-layer difference, an arithmetic claim, three estimated valgen rows, a "cannot skip validators" claim). I re-measured and corrected them before committing; remaining estimates are listed in section 6.
  (3) Change report is in docs/model-audit/ because of the Touches limit.
- Risks / follow-ups:
  - Stage B (v1 errors) is not on this branch: the branch has A, C, D only. Stage E needs B.
  - The papers' embedded model figure names match nothing v2 produces (stage C); stage D adds that the v2 design choices (gain ladder, fresh-entrant heir rule, strategy verdicts BRG/HSC/SPT/SST) appear in no paper.
  - eval_core.py is 15% of v2 Python and cannot import; paper 19 depends on welfare outputs that v2 cannot currently produce.
  - 4 test files named in WDT_Code_Reference.md do not exist; no check that valgen and rates agree on the same line.
- Verification: wc -l and ast line counts for modules, functions, TOML sections; TOML walk for scenario references; grep of source/ for concepts (second, corrected grep); import test result from stage C; test_hlc_drift.py run. Not run: any core main, table or chart script, print_hlc_calibration.py, v1 tests
- Overview sections likely needing an update: section 6 (add: eval_core orphaned in v2; HLC placeholder; 27 unreferenced scenarios)
- Merge: the two stage D files were applied onto main by the guru on 2026-11-16 (the branch was built on the stage C commit and lacked stage B, so it was not merged as a branch). Brief 001c has stage E open.
- Commit / branch: brief/001-model-audit (d8dfc44)
```

## Guru review (2026-11-16)
- Spot-checked: `val_core` 1,161, `wfr_core` 1,635, `rates_core1` 1,709, `eval_core` 2,718, `wdt_kernel` 564; v1 output layer 4,172 and v2 output layer 5,150 (re-counted); 27 of 101 scenarios unreferenced (TOML walk); `test_hlc_drift.py` exit 0 with the placeholder WARN; `valgen_core.main` at line 2919; seven `_validate` functions; "ladder" and "fresh entrant" appear in 0 papers. All hold.
- Fixed in the note: two off-by-one figures (v1 output layer 4,172 not 4,171; `rates_core` 2,127 not 2,128, so +418 over v1).
- Limits the note states stay: the 135-line scenario figure is an estimate; "paper names it" is a text match.
