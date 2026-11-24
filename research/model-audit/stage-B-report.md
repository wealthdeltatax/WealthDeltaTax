# Change report: 001c stage B (v1 errors)

The brief's `Touches` is `research/model-audit/` only, so this report and the progress block live here, as for stage A.

```
Change report
- Task: 001c stage B, audit of model v1 errors against research/model-lessons/drift-register.md. No code changed.
- Files changed: research/model-audit/v1-errors.md (new, the checkpoint note); research/model-audit/stage-B-report.md (new, this report)
- What is different now: every one of the 42 register items has a status with file, line and, where possible, a number; 3 new findings recorded
- New or changed interfaces: none
- Acceptance criteria:
  - Stage B checkpoint file exists and meets its check ("every drift-register item has a status"): met. A script found all 42 IDs (A1-A7, B1-B13, C1-C13, D1-D5, E1-E4), 0 missing
  - git diff --stat only under research/model-audit/: met (2 new files; git status shows nothing else)
  - Each claim about the code cites a file and function name: met, with line numbers
  - Every error carries a number or a reproducible check: met for B1, B4, B5, B6, B8, B9, B13, C5, C6 and A6 corner labels (numbers or in-memory snippets). Items confirmed by reading code only (A1-A5, A7, B7, B11, B12, C1-C4, C7-C13, D1-D5, E1-E3) cite file and line, which is a reproducible grep, not a measured effect. B10 not checked. Not fully met for effects on paper outputs: those need running the cores (out of scope)
- Deviations from the brief: (1) report and progress block in research/model-audit/, not in the brief, because of Touches. (2) Read research/model-lessons/drift-register.md although AGENTS.md says not to open research/model-lessons/: the brief's Read line names it and the brief decides
- Risks / follow-ups:
  - NEEDS THE AUTHOR: B1. C.1 uses TW(α) in wdt_analytics.c1 (paper 9 figures, paper 5a definition) and TW(1) in wdt_core.run_pair (paper 5 tables). Tolerant zone upper bound 1.85 vs 1.80 at canonical parameters. The brief says to stop and ask if published figures depend on a v1 error. Stage C is not started
  - B8: the synthetic scenario in the TOML (mu 0.07, amplitude 0.08, cached range -0.61% to +14.61%) disagrees with its own comments (2%, 4%, -2% to +6%). Which one the paper states was not checked
  - B5: burden sweep runs at N = 19, titled N = 30
  - Register items fixed since it was written: B2 (5_4 reads the new keys), most of B3 (5_3 prose, footer); C6 (load_params) not reproduced as slow (0.097 s)
  - The register file itself is not edited (outside Touches); the guru strikes items in stage E
- Verification: in-memory snippets (alias rates_core -> rates_core1, PYTHONDONTWRITEBYTECODE=1, python -I) for B1, B5, B6, B8, B9, C5, C6, the tolerant zone and B4; greps for the rest; git status clean outside research/model-audit/ after every run. Not run: run_all, any core main, val_core, wfr_core, table and chart scripts, any test
- Overview sections likely needing an update: section 6 (add the C.1 denominator split and the 1.85 vs 1.80 tolerant zone once the author decides)
- Commit / branch: brief/001-model-audit-b; merged to main by the guru on 2026-11-16 after review (see Guru review below)
```

## Progress block (handover)

- **Done:** stage A (v1 inventory, on main); stage B (`v1-errors.md`, branch `brief/001-model-audit-b`).
- **Next:** author decides B1 (which C.1 denominator), then stage C: audit v2 inventory and mechanism into `research/model-audit/v2-inventory.md`. One stage per session.
- **Decisions:** the in-memory alias `sys.modules['rates_core'] = importlib.import_module('rates_core1')` is how import-broken v1 is exercised; no file is edited. Do not redo the register pass.
- **Gotchas:** `load_params()['N']` is 19 (`N_fill`), `N_val` is 30; `wdt_analytics.make_p()` gives N = 30. `python -I` needs `sys.path.insert(0, '.')`.
- **Resume:** `git fetch origin && git checkout brief/001-model-audit-b`; read `research/model-audit/v1-errors.md` section 2 (B1).
- **Not run:** val_core, wfr_core, rates_core1 main, run_all, tables, charts, tests; B10 and the effects on `OUTPUTS/`.
- **State:** merged to main on 2026-11-16.

## Guru review (2026-11-16)
- Spot-checked against the code: B1 (`run_pair` divides by `TW_settled(1)`; its own docstring says "the pre-refactor C.1 divided by TW_settled(alpha)"), B4 (line 109), B5 (line 960), B7 (line 272 vs TOML 0.15), B8 (TOML lines 543 to 546), B9 (`_to_json_safe`), D2 (`run_all.bat` lines 14, 15). All hold.
- NEEDS THE AUTHOR on B1 is closed as a finding, not a decision: the author's rule for the audit (2026-11-16) is that model v1 and v2 are not fixed, only learned from. The denominator question moves to the v3 design (brief 011g) as an open design question.
- Evidence strength: A1 to A5, B7, B11, B12, C1 to C4, C7 to C13, D1 to D5, E1 to E3 rest on file and line reading, not on a measured effect; the note says so. Effects on `OUTPUTS/` were not measured and are not needed for the lessons.
