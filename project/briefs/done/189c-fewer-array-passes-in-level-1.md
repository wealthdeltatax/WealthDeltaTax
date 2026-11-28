# 189: Fewer array passes in the household year loop (level 1)

- **Status:** done, no model change (stop note), merged 2026-11-28
- **Agent:** 3
- **Needs:** none
- **Length:** 2
- **Author/date:** K. Ogata with the guru, 2026-11-28
- **Depends on:** none (171c, 178c, 179c, 186c merged)
- **Read:** `results/speedup/profile-after-154c.md` (sections 2 to 5) and `profile-after-154c/prof1000.json`; `project/brief-suggestions.md` entry "179c: level 1 is array-bound"; `model/model_v3/core/kernel.py`, `core/household.py` (`apply_payment`, `household_step`), `core/burden.py` (`m2`, `_cash`); `project/agents/reference/code/speedup.md`

## Goal
Level 1 is 75% of a `quick` run and runs at 1,000-path chunks, where the 179c profile shows it array-bound (9% fixed time, 1.4 times the floor of its numpy calls): a compiled loop (180c) cannot help, fewer and cheaper passes over the data can. Take the first targets the profile names, in this order, one commit each, and stop when the next costs more than it saves:
1. `builtins.sum` (536,000 calls per evaluation, 13.8 s of 117 s own time at 1,000 paths): find its callers and replace it where the result is the same.
2. `where` chains (1.44 million calls) and repeated `asarray` of the same values (1.03 million): fuse or hoist, where the results are the same.
3. `burden.m2` (5.7 s) and `burden._cash` (5.1 s), which are per-year loops of their own at 1,000 paths.

## Method (pre-registered)
- Measure first at 1,000 paths: `core_run` and one full evaluation, best of 2 on the same machine with `NPY_DISABLE_CPU_FEATURES=X86_V4`; the profile of the same case before and after each commit. No other timing counts.
- **Byte-identity is the test**: the smoke and `quick` outputs equal a before-file made with the same setting (as 186c did, `run_date` excluded). Python's `sum` over a list of arrays adds left to right; `np.sum` over a stacked array with `axis=0` also adds row by row, so identity is expected for that form; prove it on the real arrays. A form that changes the summation order (pairwise, float32) is not byte-identical: do not apply it, list it with its measured gain and its difference, and stop for the author (the `Asks` line).
- Report per change: lines touched, gain at 1,000 paths and at 20 paths (the 24% of `quick` that runs small), identity result.

## Touches
`model/model_v3/core/` (`kernel.py`, `household.py`, `burden.py`, within the 360-line and file budgets in `architecture.md`; if a file is at its budget say so before growing it), `results/speedup/` (ledger rows, a short note), tests only if a tripwire needs a new case.

## Acceptance criteria
- Every applied change: byte-identical `quick` and smoke outputs against a same-setting before-file, and the 171c pins unchanged; `fast` green on Actions.
- Level 1 time at 1,000 paths before and after each commit, in the ledger, with the speed-up of `quick` projected from the 179c part shares.
- A stop note: what was tried and left (with gain and difference) and what the next target would be.

## Out of scope
A compiled kernel (180c, stopped), float32 or layout changes that alter results without the author's tolerance, the O1e root count (153c), the shared year loop (152c; it may need measuring first: 179c says it helps only the 24% that runs at 20 to 50 paths, 180c says each `core_run` walks the year loop twice; if the first step of 152c shows which, say so here).

## Implementation notes
<!-- progress:start -->
- **Done:** baseline at 1,000 paths; step 1 (`asum`) tried and reverted; steps 2 and 3 measured in micro-tests; stop note in `results/speedup/array-passes-189c.md`.
- **Next:** author reads the change report; 152c is the next lever.
- **Resume:** nothing to resume.
- **State:** done, no model change
<!-- progress:end -->

## Change report
- **What changed:** no model code. `model/studies/run-cost/array_pass_micro.py` (new), `results/speedup/array-passes-189c.md` (new), two ledger rows, one suggestion entry.
- **Result:** no change meets the bar. Step 1 (`builtins.sum` at 12 sites): byte-identical, but no gain seen at 1,000 paths (`core_run` 14.9 to 17.0 s, full evaluation 91.4 to 96.2 s, inside this machine's 5 to 10% spread); the 12% own time of `sum` is the numpy adds inside it. Step 2: `_div` by `divide(where=)` is byte-identical, 22% faster at 280 elements and 11% slower at 14,000. Step 3: `m2` with fewer masks is 6% faster and not byte-identical, so it would need your tolerance; not worth it (about 0.7% of `quick`).
- **Projection:** none applied, so `quick` stays at 1,942 s serial and 1,210 s on 2 cores.
- **Next target:** 152c (the shared year loop).
- **Caveat:** timings are best of 2 on a 2-core machine with a 5 to 10% spread; a gain under about 7% could not be seen. No `quick` or smoke before-file was needed (no model file changed), and the 171c pins are untouched.
- **Author questions:** none.
