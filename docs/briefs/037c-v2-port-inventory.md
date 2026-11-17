# 037: Code: inventory of v2 for the port by exception (model v3 stage C input)

- **Status:** ready
- **Author/date:** K. Ogata with the guru, 2026-11-17
- **Depends on:** none
- **Read:** `docs/briefs/011g-model-v3-design.md` (stage C text); `docs/model-audit/synthesis.md` sections 4, 5 and 10; `model_v2/README.md`, `model_v2/WDT_Code_Reference.md`; `model_v2/wdt_kernel.py`, `wdt_core.py`, `wdt_jst.py`, `wdt_par.py`; `model_v2/test/`; `docs/model-v3/outputs.yml` and `metrics.md` (ids and formulas); `docs/agents/code.md`. Nothing else need be opened.

## Goal
List exactly what of model v2 v3 may port, what it must rewrite and what it drops, with the output element that needs each ported item and the tests that travel with it, so the architecture (039g) names the port by exception from facts, not memory.

## Decisions (author, 2026-11-16, `synthesis.md` section 5)
Clean slate with port by exception. Candidates: v2's layering and `wdt_kernel` (564 lines), the JST return series `jst_r6.json`, the loss-refund and delta-tax mechanics as the papers state them, the decomposition identity. Not carried over: the gain ladder, the fresh-entrant heir rule, strategy verdicts, `eval_core`, the 101 scenarios, the figure and table scripts, everything in the drift register. Each ported item needs a named element and a test (R7); nothing unused or unported stays in the tree (R8).

## Design
Read-only. Write `docs/model-v3/port-inventory.md` with:
1. A table, one row per function or class of 30 lines or more in `wdt_kernel.py`, `wdt_core.py`, `wdt_jst.py` and `wdt_par.py`: file and lines, what it computes in one line, imports (to show the layering), tests that cover it, the `outputs.yml` id or metric that needs it (or "none"), and a verdict: **port** (as is), **port with change** (say what), **rewrite** (v3 needs it, v2's form does not fit) or **drop**; one-line reason.
2. Line totals by verdict, for the kernel and for the core separately.
3. The four candidate items named in the decision, each located by file and lines, with its tests (existing, missing) and what the papers require of it (cite the paper section).
4. Where v2 computes: the wealth-weighted effective rate ε, the refund cap, the reserve fill, the closure test and the decomposition identity; for each, file, lines, and the inputs it reads. This is what C1 item 3 needs to reproduce v2's 7.34% of GDP at v2-like inputs.
5. The existing tests: run them, read-only, and record pass or fail and run time. Say which would still make sense in v3.
6. Layering violations and import side effects found (R4, R8), with file and line.

## Touches
`docs/model-v3/port-inventory.md` (new), this brief's progress block. Nothing else; no file in `model_v2/` is edited, moved or formatted.

## Acceptance criteria
- Every function or class of 30 lines or more in the four files has a row and a verdict; the row count is checked by script against the source.
- Items 3 and 4 above are answered with file and line numbers that exist.
- Line totals add up to the file lengths (`wc -l`) within the lines not in a function.
- Test results recorded; no file changed in `model_v2/`.
- `git diff --stat` shows only the Touches list.

## Checks to run
A script that lists functions of 30 lines or more (`ast`) and compares with the table; `git status` clean in `model_v2/`; `pytest model_v2/test` or the folder's own runner, with the exact command in the note.

## Out of scope
Porting any code, running scenario scripts or sweeps, fixing v2, deciding the verdicts for the author (verdicts are recommendations), v1.

## Open questions
Whether to run v2's `logistic_ln_ref` scenario once to record its realised ε (it would give C1 item 3 an exact number). Default: no; list how it could be run and what it costs, and ask.

## Implementation notes
<!-- progress:start -->
- **Done:**
- **Next:**
- **Decisions:**
- **Gotchas:**
- **Resume:**
- **Not run:**
- **State:** ready; not started
<!-- progress:end -->
