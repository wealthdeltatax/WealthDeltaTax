# C1 seed noise and limits (brief 187c)

Machine and run: Intel(R) Xeon(R) Processor @ 2.10GHz, 2 cores, numpy 2.5.3, NPY_DISABLE_CPU_FEATURES=X86_V4, workers 1, N1 10,000, commit 515c74c491ba

Rule (fixed in the brief before measuring): limit = q x sd(N1), q = 4.613 (99th percentile of the range of 5 standard normal draws, 10^6 draws, seed 20261127; the brief recalled about 4.6), sd the standard deviation across 10 seeds at N1 = 10,000 paths; no absolute ceiling; a floor of 1e-09 (the 171c zero tolerance, author 2026-11-28).

## 1. Monte Carlo law: sd(N) x sqrt(N) against its value at N1 (ratio; ok = within 20%)

| output | statistic | N=1,250 | N=2,500 | N=5,000 | N=10,000 | N=20,000 |
|---|---|---|---|---|---|---|
| O1 | mean | 0.99 ok | 1.48 OUT | 1.47 OUT | 1.00 ok | 0.84 ok |
| O1 | p10 | 0.84 ok | 0.82 ok | 0.80 OUT | 1.00 ok | 1.23 OUT |
| O1 | p90 | 2.17 OUT | 2.24 OUT | 1.42 OUT | 1.00 ok | 1.06 ok |
| O2 | mean | 1.48 OUT | 1.67 OUT | 1.86 OUT | 1.00 ok | 1.00 ok |
| O2 | p10 | 1.17 ok | 0.96 ok | 1.06 ok | 1.00 ok | 0.64 OUT |
| O2 | p90 | 0.77 OUT | 1.21 OUT | 1.11 ok | 1.00 ok | 1.31 OUT |
| O3 | mean | 1.61 OUT | 1.87 OUT | 1.88 OUT | 1.00 ok | 1.21 OUT |
| O3 | p10 | 0.87 ok | 1.45 OUT | 1.26 OUT | 1.00 ok | 1.31 OUT |
| O3 | p90 | 1.24 OUT | 1.26 OUT | 1.29 OUT | 1.00 ok | 1.34 OUT |
| O4a | mean | 0.83 ok | 1.12 ok | 1.10 ok | 1.00 ok | 1.20 ok |
| O4a | p10 | 0.35 OUT | 0.50 OUT | 0.71 OUT | 1.00 ok | 0.00 OUT |
| O4a | p90 | 0.35 OUT | 0.50 OUT | 0.71 OUT | 1.00 ok | 0.00 OUT |

sd from 10 seeds is itself uncertain by about 22% (35% for the five pairs at 2 x N1), so single `OUT` cells at the extremes are not evidence against the law; a row that is OUT at every N is.

The ratio is to a single reference (sd at N1, from 10 seeds), and the nested subsamples of one seed share their paths, so a low or high reference moves a whole row together (O2 and O3 means: 1.5 to 1.9 below N1). A reference-free check, added to the brief's method: the slope of log sd on log N over N1/8 to N1 (the law says -0.5):

| output | mean | p10 | p90 |
|---|---|---|---|
| O1 | -0.50 | -0.43 | -0.90 |
| O2 | -0.65 | -0.55 | -0.40 |
| O3 | -0.71 | -0.46 | -0.59 |
| O4a | -0.42 | 0.00 | 0.00 |

## 2. Limits and the measured spread

| output | statistic | sd(N1) | limit | spread of the 5 C1 seeds | range of all 10 seeds | limit / path sd | limit / abs mean | N for O3 limit 0.15 |
|---|---|---|---|---|---|---|---|---|
| O1 | mean | 0.0355 | 0.1636 | 0.1019 | 0.1120 | 0.030 | 0.044 |  |
| O1 | p10 | 0.0597 | 0.2751 | 0.1312 | 0.1684 | 0.051 | 0.073 |  |
| O1 | p90 | 0.0697 | 0.3214 | 0.1120 | 0.2233 | 0.059 | 0.086 |  |
| O2 | mean | 0.0072 | 0.0330 | 0.0186 | 0.0223 | 0.024 | 0.009 |  |
| O2 | p10 | 0.0151 | 0.0697 | 0.0118 | 0.0526 | 0.052 | 0.019 |  |
| O2 | p90 | 0.0253 | 0.1167 | 0.0671 | 0.0737 | 0.087 | 0.032 |  |
| O3 | mean | 0.0666 | 0.3073 | 0.1907 | 0.2164 | 0.037 | 0.006 | 41,961 |
| O3 | p10 | 0.0988 | 0.4559 | 0.2615 | 0.2920 | 0.054 | 0.009 | 92,372 |
| O3 | p90 | 0.0738 | 0.3404 | 0.1918 | 0.2850 | 0.040 | 0.006 | 51,495 |
| O4a | mean | 0.0218 | 0.1007 | 0.0457 | 0.0685 | 0.039 | 0.004 |  |
| O4a | p10 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.000 | 0.000 |  |
| O4a | p90 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.000 | 0.000 |  |

Rows where the five C1 seeds spread more than the limit: none.
Rows where the range of all ten seeds exceeds the limit: none. (The limit is built for the range of 5 draws, which is the one the test uses; the range of 10 draws is larger on average, about 3.08 sd against 2.33, so the ten-seed list is the stricter check and a row on it is a warning, not a failure of the rule.)

"Limit / path sd" is the limit in units of the output's own cross-path standard deviation (mean over seeds at N1); "limit / abs mean" in units of the mean over seeds. The last column is information, not a proposal: it assumes sd falls as 1/sqrt(N).
