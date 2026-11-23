`median_mid`, household arm, `safe` fund, seed 20261118, 200 paths, 27 schedule points per phase count; the phase count is the only change. Run time is wall clock of one `f1` run (all of 27 schedule points, margins and the constant-path section).

### Best F1 by (tolerance, margin) and feasible cells

| tol | m | 6 phases: best F1 / passing M2, M4a / feasible | 15 phases: best F1 / passing M2, M4a / feasible | 30 phases: best F1 / passing M2, M4a / feasible |
|---|---|---|---|---|
| 0 | 0% | 9.0 / 9.0 / 0 of 26 | 12.5 / 12.5 / 0 of 24 | 25.5 / 25.5 / 0 of 22 |
| 0 | 10% | 21.0 / 21.0 / 0 of 26 | 28.0 / 28.0 / 0 of 24 | 41.0 / 41.0 / 0 of 22 |
| 0 | 25% | 35.5 / 35.5 / 0 of 26 | 42.0 / 42.0 / 0 of 24 | 56.5 / 56.5 / 0 of 22 |
| 0.05 | 0% | 9.0 / 9.0 / 0 of 26 | 14.0 / 14.0 / 0 of 24 | 26.5 / 26.5 / 0 of 22 |
| 0.05 | 10% | 23.0 / 23.0 / 0 of 26 | 30.0 / 30.0 / 0 of 24 | 42.5 / 42.5 / 0 of 22 |
| 0.05 | 25% | 38.5 / 38.5 / 0 of 26 | 43.5 / 43.5 / 0 of 24 | 57.5 / 57.5 / 0 of 22 |
| 0.25 | 0% | 12.0 / 12.0 / 0 of 26 | 17.5 / 17.5 / 0 of 24 | 30.5 / 30.5 / 0 of 22 |
| 0.25 | 10% | 30.5 / 30.5 / 0 of 26 | 35.0 / 35.0 / 0 of 24 | 48.0 / 48.0 / 0 of 22 |
| 0.25 | 25% | 46.5 / 46.5 / 0 of 26 | 50.0 / 50.0 / 0 of 24 | 62.0 / 62.0 / 0 of 22 |
| 1 | 0% | 25.0 / 25.0 / 0 of 26 | 32.0 / 32.0 / 0 of 24 | 45.0 / 45.0 / 0 of 22 |
| 1 | 10% | 45.0 / 45.0 / 0 of 26 | 51.5 / 51.5 / 0 of 24 | 61.5 / 61.5 / 0 of 22 |
| 1 | 25% | 65.5 / 65.5 / 0 of 26 | 63.5 / 63.5 / 0 of 24 | 75.0 / 75.0 / 1 of 22 |

### F1 at the 055c rule (tol 0, m 0) over the schedule points that ran, and cells that did not run

| phases | schedule points run | F1 range (tol 0, m 0) | median over points | M2 short range | cells that raised I1 | run time |
|---|---|---|---|---|---|---|
| 6 | 26 | 1.5 to 9.0 | 3.8 | 0.60 to 3.60 | 1 | 81 s |
| 15 | 24 | 3.0 to 12.5 | 5.5 | 0.59 to 2.75 | 3 | 179 s |
| 30 | 22 | 11.0 to 25.5 | 15.8 | 0.59 to 2.65 | 5 | 339 s |

### Constant path: first shortfall year and P3 (`median_mid`; schedules tm50, tm70, tm90, k_ln 1, ratio 0.5)

| phases | schedule | fill year | end of short window | first year relief < M1d | inside short window | P3 to end of short window | P3 100 y |
|---|---|---|---|---|---|---|---|
| 6 | tm50_k1_r050 | 7 | 17 | 13 | yes | 2.03 | 43.08 |
| 6 | tm70_k1_r050 | 7 | 17 | 13 | yes | 1.84 | 43.04 |
| 6 | tm90_k1_r050 | 7 | 17 | 13 | yes | 1.71 | 43.30 |
| 15 | tm50_k1_r050 | 7 | 17 | 33 | no | 0.00 | 17.96 |
| 15 | tm70_k1_r050 | 7 | 17 | 9 | yes | 19.72 | 295.02 |
| 15 | tm90_k1_r050 | 7 | 17 | 9 | yes | 16.87 | 292.81 |
| 30 | tm50_k1_r050 | 6 | 16 | 61 | no | 0.00 | 13.42 |
| 30 | tm70_k1_r050 | 6 | 16 | 61 | no | 0.00 | 15.51 |
| 30 | tm90_k1_r050 | 6 | 16 | 61 | no | 0.00 | 17.51 |

