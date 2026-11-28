# 153: Fewer evaluations per O1e root

- **Status:** done, closed unmerged 2026-11-28 (bar not met: 1.44x against 2x; the opt-in code stays on branch `brief/153c-o1e-root-evals`)
- **Agent:** 2
- **Needs:** 179c
- **Length:** 1
- **Author/date:** K. Ogata with the guru, 2026-11-26
- **Depends on:** 180c (the kernel spike report: if a compiled kernel makes an evaluation several times cheaper, fewer evaluations per root matter less and the brief may shrink or drop; moved behind the spike by the author, 2026-11-27), 171c (zero tolerance, so a real change is told from rounding), 151c (headline-only evaluation), 179c (profile), 176c (bench)
- **Read:** `model/model_v3/runner/sweeps.py` (`breakeven_return`, `breakeven`); `results/run-cost/run-cost.md` ("Level 1 and O1e roots"); `model-specs/metrics.md` (O1e); `model/model_v3/run.py` (the O1e lines and the `no_sign_change_0_15` marker)

## Goal
An O1e root is a bisection of [0, 15] to a tolerance of 1e-2: two end evaluations plus about 10 more, 12 in all. Cut that to about 4 to 6 evaluations (2 to 3 times on the roots) without changing what a root means.

## Decisions (author, 2026-11-26)
Lever 4 is accepted on condition that the author signs off a tolerance rule. The rule is the guru's proposal, below.

## Proposed tolerance rule (for sign-off)
Bisection to 1e-2 guarantees each root is within 1e-2 of the true root, so any two valid roots differ by at most 2e-2. Hence: **each new root lands within 2 x 1e-2 of the bisection root, the `no_sign_change_0_15` flag is identical cell by cell, and the p10 to p90 range over draws moves by no more than 2e-2 at either end.** The new method must itself stop with a bracket of width at most 1e-2 around a sign change, so the guarantee holds. Where M1 is not monotone in the return (death-phase lumps) and the new method lands on a different sign change, the cell is reported, not accepted.

## Design
1. Candidates, each measured on the same `quick` and 20-path draws: (a) start the bracket around the previous draw's root and widen only if the sign test fails; (b) Illinois or Brent steps inside a bracket that still straddles the sign change; (c) a cheaper no-sign-change check (reuse an end evaluation across draws that share the end).
2. Every candidate keeps a bracket with a sign change and stops at width 1e-2, falling back to plain bisection on any doubt.
3. Compare against the bisection roots from the same run: evaluations per root, per-root difference, flag agreement, range movement. Adoption bar: the rule above holds on every cell at `quick`, and the evaluation count drops at least 2x on the roots.
4. The pins move in their own commit after the author reads the report, as 171c does.

## Touches
`model/model_v3/runner/sweeps.py`, `model/model_v3/run.py` (method name option, default the adopted one), `tests/model/model_v3/` (a root test on a noisy evaluator, as `test_pool.py` does), `results/speedup/` (report), `results/speedup/ledger.md`, pins. Not the evaluator or the kernel.

## Acceptance criteria
- The rule holds on every O1e cell at `quick` and at the 20-path smoke size; a table of the per-cell differences is in the report.
- Evaluations per root before and after, and the `quick` and 20-path root wall times, from `bench.py`.
- Bisection stays available (`--root-method bisect`) so any run can be redone the old way.

## Out of scope
The evaluator (151c), parallelism, the kernel, the O1e scope (central root at `median_mid`; draws via `--o1e-draws`).

## Open questions
For the author: sign off the rule (2 x 1e-2, flags identical, range moves at most 2e-2), or set another.

## Implementation notes
<!-- progress:start -->
- **Done:** Illinois root method built behind `--root-method`; measured on the real roots at `quick`, a 20-path probe with draws and smoke; rule holds on every cell; report `results/speedup/root-methods.md`. model_v3 suite 443 passed.
- **Next:** author: the 2x bar is not met (1.44x at `quick`, 1.05x with draws), so the default stays bisection; decide: close 153c without merging, or merge the opt-in method. And the finding below (two named schedules are the same schedule) needs its own brief.
- **Resume:** nothing pending in the code; no pins moved (the default is unchanged).
- **State:** done, bar not met, not adopted, not merged
<!-- progress:end -->


```
Change report
- Task: 153c fewer evaluations per O1e root
- Files changed: model/model_v3/runner/sweeps.py (`_illinois`, `method=` on `breakeven` and `breakeven_return`; default bisect); model/model_v3/run.py (`--root-method`, recorded in the run block only when not bisect; still 120 lines); tests/model/model_v3/test_pool.py (two tests); model-specs/architecture.md (budget: test_pool.py 103 to 150 and the sums, as 154c did); model/studies/run-cost/root_methods.py (the study); results/speedup/root-methods.md (report); results/153c-evidence/ (study data)
- What is different now: `--root-method illinois` gives O1e roots in fewer evaluations; the default is bisection, so every output is unchanged. Not adopted.
- New or changed interfaces: `run.py --root-method {bisect,illinois}` (default bisect); `sweeps.breakeven(..., method=)`, `breakeven_return(..., method=)`; run block `o1e.root_method` when not bisect.
- Acceptance criteria: (1) the rule holds on every O1e cell at `quick` and at the 20-path size, with the per-cell table: met (max root difference 0.0028, flags identical, range moves at most 0.0012; the smoke size has tol 1.0, so a 20-path run at tol 1e-2 with 6 draws was added). (2) evaluations per root before and after, and root wall times from `bench.py`: partly met: evaluations per root measured (13 to 9 at `quick`; 13.0 to 12.4 with draws); `bench.py`'s `root_1_20` is a 2-evaluation bracket check and cannot show the lever, so wall times come from the study (124 s to 109 s for map plus roots). (3) bisection stays available: met (default). Adoption bar (rule holds and at least 2x fewer evaluations): NOT met, 1.44x at best.
- Deviations from the brief: not adopted, so no default change, no ledger row and no pin move; `architecture.md` budget raised for `test_pool.py` (outside Touches, needed by `test_budget`); a 20-path tol 1e-2 probe added to the smoke size for the rule.
- Risks / follow-ups: (1) the root is a jump (plateau, then one path flipping), so no secant or hint method can reach 2x; bisection is near the floor for a jump. (2) New lever for the guru: S_low and S_central are the same spec in the `quick` run (466 of 466 level 1 cells identical); level 1, tornado and roots compute it twice; computing each distinct spec once is byte-identical and would save about 600 s of 1,942 s. Unmeasured at `final`. (3) `bench.py` case `quick_headlines` still passes `--parts headlines`, which 178c replaced with `level1,map`: it will fail until bench is updated (176c's file; not touched).
- Instruction friction: none
- Verification: tests/model/model_v3 not converge: 443 passed; the study on the real model at quick, probe20 and smoke; toy functions in the tests. Not run: the gate suite (unaffected), Actions, `--final`.
- Overview sections likely needing an update: none unless the author adopts the method
- Commit / branch: see below, brief/153c-o1e-root-evals (not merged)
```
