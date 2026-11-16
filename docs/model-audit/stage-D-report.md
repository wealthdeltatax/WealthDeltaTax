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
- Merge: not merged. Brief 001c has stages B and E open; the branch stays pushed.
- Commit / branch: brief/001-model-audit
```
