# O1e roots: Illinois steps against bisection (brief 153c)

**Verdict: not adopted. The rule holds on every cell, but the evaluation count drops 1.44x on the `quick` roots (13 to 9 per root) and 1.05x on 20-path draws (13 to 12.4), against the bar of 2x. The default stays bisection; `--root-method illinois` is available and off.**

Machine: 2 cores, 8 GB, `NPY_DISABLE_CPU_FEATURES=X86_V4`, workers 1. Branch started from main `b71eacd`. Study: `model/studies/run-cost/root_methods.py` (runs `run.py --parts map,o1e` once per method, counts the evaluations of every root); data in `results/153c-evidence/root-methods-*.json`. `bench.py`'s `root_1_20` is a bracket check only (the root has no sign change there: 2 evaluations), so it cannot show this lever; the study counts evaluations on the real roots instead.

## The method
`sweeps.breakeven(..., method='illinois')` / `breakeven_return(..., method=)`: the two end evaluations as before (so the `no_sign_change_0_15` flag is decided by the same two values and is identical by construction), then Illinois secant steps inside a bracket that keeps its sign change; when the estimate settles it probes tol/2 beyond the last point, which closes the bracket if the sign changes there. It stops, as bisection does, with a bracket narrower than tol and returns its midpoint. Doubt (non-finite value, estimate outside the bracket, a bracket not halved in two steps, more than 6 secant steps) is a bisection step.

## The rule (author, 2026-11-28): each root within 2 x tol, flags identical, range moves at most 2e-2
| run | roots | with a sign change | flags identical | max difference of a root | range (p10, p90) movement |
|---|---|---|---|---|---|
| `quick` (50 paths, tol 1e-2, no draws) | 3 | 2 | yes | 0.0023 | not run at 0 draws |
| `probe20` (20 paths, tol 1e-2, 6 draws) | 21 | 10 | yes | 0.0028 | 0.0012 (p10) and 0.0006 (p90) |
| `smoke` (20 paths, tol 1.0, 3 draws) | 12 | 8 | yes | 0.27 against the rule's 2.0 at tol 1 | n/a |

Per root, `quick`: bisection 11.2170 and 11.2170 (S_low, S_central), no sign change (S_high); Illinois 11.2193, 11.2193, no sign change. `probe20` differences per root: -0.0026, -0.0025, -0.0015, 0.0014, 0.0028 for each of the two schedules. No cell is reported for a different sign change.

## Evaluations
| case | bisection | Illinois | ratio |
|---|---|---|---|
| `quick` roots with a sign change (per root) | 13 | 9 | 1.44x |
| `quick` roots, all three (the third has no sign change: 2 each) | 28 | 20 | 1.40x |
| `probe20` roots with a sign change | 13.0 | 12.4 | 1.05x |
| wall, `quick` (map plus roots, one run each) | 124 s | 109 s | 0.88; the saving is the 8 evaluations at about 1.9 s |

## Why it cannot reach 2x
The function is not smooth where the root is. The trace of one `quick` root (bisection, S_central) is f(0) = 0.27, f(7.5) = 0.49, f(11.25) = -0.066, f(11.13) = 0.001, f(11.19) = 0.002, f(11.21) = 0.003, f(11.22) = -0.032: a hump, then a plateau about 0.002 above zero, then a jump of 0.035 (one path of 50 flipping) at 11.217. The root is a jump, not a crossing, so a secant step cannot place the bracket closer than the plateau, and the last bracket of width 1e-2 costs log2 steps whatever the method. A narrow starting bracket from a hint (candidate a, the central root of the schedule) needs the draws' roots within about 0.1 of it for 2x; in `probe20` the draw roots are 11.64, 11.97, 11.78, 11.25 against the central 11.63, so a bracket of about 0.8 is needed: 2 ends plus 7 halvings is 9 evaluations, 1.4x, and a miss costs the full bracket on top. Candidate (c), reusing an end evaluation, does not apply: the ends differ by schedule and by draw.

## What the study found instead: two of the three named schedules are the same schedule
In the `quick` run S_low and S_central are the same spec: all 466 cells of the level 1 file are identical for the two, and the two roots above are the same root, computed twice. Level 1, the tornado and the roots each run all three named schedules, so one third of level 1 (about 480 s of 1,465), one third of the tornado and half of the roots (13 of 28 evaluations) repeat a result. Computing each distinct spec once and copying the result to its aliases is byte-identical by construction and would save about 600 s of the 1,942 s `quick` here (about 30%), more than anything in 153c. It holds where the map picks the same grid point for S_low and S_central, which it does in this run; at `final` size the map is the same rule on 50 paths, so likely, not measured. This is a different lever from 153c and needs its own brief (guru).
