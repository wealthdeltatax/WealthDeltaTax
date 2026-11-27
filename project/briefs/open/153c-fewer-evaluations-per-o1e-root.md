# 153: Fewer evaluations per O1e root

- **Status:** hold; draft, needs the author's sign-off on the tolerance rule below before it is released
- **Agent:** 5
- **Needs:** 171c, 151c, 179c, 180c
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
- **Done:**
- **Next:**
- **Resume:**
- **State:** draft
<!-- progress:end -->
