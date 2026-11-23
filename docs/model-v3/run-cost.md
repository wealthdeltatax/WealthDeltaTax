# Run cost of model_v3 (brief 150c)

Timings: `docs/model-v3/run-cost/timing.py` (wall seconds, best of 2, spec tau_m 0.5, k_ln 0.5, ratio 1.0, grid point median_mid, 2 cores, 7 GB, one process). Raw JSON: `run-cost/timing.json`. Block 1 only measures; nothing in the model changed.

## One evaluation

`ev(spec)` is `evaluate`: one `core_run` plus the `again` runs the groups ask for. It makes 5 `core_run` calls on both arms.

| paths | household | legacy | household/legacy |
|---:|---:|---:|---:|
| 20 | 8.9 s | 2.9 s | 3.0 |
| 200 | 18.5 s | 8.2 s | 2.3 |
| 1,000 | 76 s (RSS 2.0 GB) | 36 s (RSS 2.2 GB) | 2.1 |

The brief quoted 4.9 s (household) and 1.8 s (legacy) at 20 paths. This machine gives 8.9 s and 2.9 s; the brief's figures were probably taken on a faster machine or before 132c/133c. All projections below use this machine's numbers.

Cost is not linear in paths: at 20 paths it is already 8.9 s. About 8 s of it is fixed per evaluation (the year loop), about 0.07 s per path after that. Evaluations at few paths are the worst value.

## Cost by part (one evaluation, seconds)

`core_run` is the sum of its 5 calls. The groups' own `per_path` times include the `again` core runs they trigger, so the group rows overlap `core_run`; they are not additive.

| part | hh 20 | hh 200 | leg 20 | leg 200 |
|---|---:|---:|---:|---:|
| total | 8.5 | 19.2 | 3.3 | 8.5 |
| `core_run` (5 calls) | 6.6 | 16.5 | 3.0 | 7.4 |
| headlines | 0.01 | 0.09 | 0.01 | 0.10 |
| group revenue (incl. its core runs) | 3.8 | 10.3 | 2.4 | 5.7 |
| group burden | 0.07 | 0.58 | 0.07 | 0.61 |
| group support (welfare solves, M13) | 3.3 | 5.1 | 0.5 | 1.3 |
| group sweeps | 0.00 | 0.00 | 0.00 | 0.00 |
| not in `core_run` or headlines | 1.9 | 2.6 | 0.3 | 1.1 |

Reading: `core_run` is 78 to 86 % of an evaluation. The household arm's extra cost over legacy is in `core_run` (hook, lien, floor) and in the support group's welfare solves (3.3 s against 0.5 s at 20 paths). Groups burden and sweeps are negligible. `statics`: 0.02 s.

## Level 1 and O1e roots

| item | household | legacy |
|---|---:|---:|
| level 1, one schedule, 1,000 paths | 74 s | 36 s |
| O1e root, bracket check only (2 evals, no sign change) at 20 / 200 paths | 16.4 / 36.8 s | 5.4 / 14.6 s |
| O1e root with a sign change, about 12 evals | 12 x one evaluation | same |

`breakeven` evaluates both ends of [0, 15] first and returns nan when M1 does not change sign, so a root costs 2 evaluations or about 12 (2 plus the bisection to tol 1e-2: log2(15/0.01) is 10.5). Which roots bracket is not known before the run.

Legacy finding (not repaired, outside this brief): at 20 and 200 paths the O1e root on the legacy arm raises `ValueError: income_tax_gains: a rate of 1.0 raises 0.46, less than the target 0.53` from `solve_rate` in `core/support.py` at an end of the bracket. `run.py --arm legacy` would die in O1e the same way. Household does not.

## The smoke run

`python -m model_v3.run --smoke` (057c branch, 56a0a14): n1 = 50, n2 = 3 draws, n2p = 20, one point (median_mid), household. 783 s wall, 13 minutes, in which the run computed everything and then stopped at assembly: `every grid point failed: median_mid: DH1c ('S_low', 'transition', ...): point_and_r...` (the validator on 057c's branch; the message is cut by the script at 80 characters). The compute time is complete; the output file was not written. That failure is 057c's, not this brief's.

Split of the 783 s, by evaluation counts (a tornado is 1 + 2 x 5 read inputs = 11 evaluations per schedule, 3 schedules; level 1 at 50 paths is small):

| part | evaluations | seconds |
|---|---:|---:|
| tornado (n2p 20) | 33 | about 295 |
| level 1 (3 schedules, 50 paths) | n/a | about 10 (at 74 ms per path) |
| O1e (3 schedules x 4 roots) | remainder | about 480, about 54 evaluations, 4.5 per root |

The O1e share is inferred as the remainder, not timed separately. It implies most smoke roots had no sign change.

## Projection, full run, serial, this machine

Evaluations in the run are at n2p = 1,000 paths: 76 s each (household). N1 = 10,000, N2 = 200. Author decision 2026-11-23: O1e at `median_mid` only; the other four points carry level 1 and the tornado.

| part, per grid point | evaluations or paths | time |
|---|---:|---:|
| level 1, 3 schedules x 10,000 paths | 30,000 paths | 2,220 s (37 min) |
| tornado, 3 schedules x 11 | 33 evaluations | 2,510 s (42 min) |
| one point without O1e | | 4,730 s (79 min) |
| O1e, 3 x (1 + 200) = 603 roots | | |
| - every root has no sign change (2 evals) | 1,206 | 91,600 s (25 h) |
| - smoke-like mix (4.5 evals per root, inferred) | 2,700 | 206,000 s (57 h) |
| - every root brackets (12 evals) | 7,236 | 550,000 s (153 h) |

Full run, one-point O1e, one process: 4 x 79 min + 79 min + O1e = 6.6 h + 25 to 153 h, central 64 h, about 2.7 days. `accept.sh` runs it twice. Without one-point O1e the same five points would take 5 times the O1e figure.

Memory: 2 GB per process at 1,000 paths. Two workers on this machine fit (4 GB of 7).

## What parallelism can and cannot do (for blocks 2 and 3)

Independent units: the 3 schedules, the 603 roots, the tornado's 33 evaluations, level 1's chunks, and the five grid points. The roots are the bulk (over 90 % of the run in the central case), and each is a serial bisection, so the unit is a root.

On this machine the best case is 2 workers, 2x: the central full run about 32 h. A 16-core machine with 32 GB (2 GB each) is memory-bound at about 14 workers: the central full run about 4.6 h (64 h / 14), and 32 to 160 h becomes 2.3 to 11 h. Block 3 replaces these with measured speed-ups.

The fixed cost per evaluation (5 `core_run` calls, a year loop) bounds everything and is a kernel matter: outside this brief.
