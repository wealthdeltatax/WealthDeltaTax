### generators

| Generator | Mean | Geo | SD | Loss yrs | Lag-1 | Longest run (mean) | 100y paths with run >= 4 | with run >= 6 | 30y geo mean P10 / P50 / P90 (independent paths) | Same, 88-window style on 117y paths |
|---|---|---|---|---|---|---|---|---|---|---|
| **Observed, 117 years** | 4.74 | 4.42 | 8.22 | 28.2 | 0.30 | 5 (6 across the gap) | n/a (one path) | n/a | 2.18 / 3.73 / 7.47 (88 windows) | same |
| a. window replay, 100y, 117 paths | 4.74 | 4.42 | 8.20 | 28.2 | 0.30 | 5.8 | 100% | 81% | 2.13 / 3.87 / 7.25 | n/a |
| b. stationary bootstrap, mean block 1 | 4.75 | 4.43 | 8.16 | 28.2 | -0.01 | 3.3 | 36% | 3% | 2.50 / 4.43 / 6.37 | 2.52 / 4.44 / 6.35 |
| b. stationary bootstrap, mean block 2 | 4.75 | 4.43 | 8.13 | 28.2 | 0.13 | 3.9 | 55% | 9% | 2.25 / 4.48 / 6.62 | 2.21 / 4.46 / 6.64 |
| b. stationary bootstrap, mean block 3 | 4.73 | 4.41 | 8.12 | 28.3 | 0.18 | 4.0 | 60% | 9% | 2.07 / 4.50 / 6.77 | 2.11 / 4.50 / 6.72 |
| b. stationary bootstrap, mean block 5 | 4.74 | 4.42 | 8.12 | 28.2 | 0.21 | 4.1 | 60% | 9% | 1.91 / 4.50 / 6.83 | 1.97 / 4.51 / 6.85 |
| b. stationary bootstrap, mean block 10 | 4.75 | 4.43 | 8.11 | 28.1 | 0.24 | 4.2 | 61% | 6% | 1.93 / 4.47 / 6.97 | 1.93 / 4.49 / 6.97 |
| d. bootstrap, 1914-18 and 1939 dropped, block 3 | 5.26 | 4.96 | 7.96 | 25.2 | 0.14 | 3.5 | 46% | 4% | 2.87 / 4.98 / 7.10 | n/a |
| c1. iid normal | 4.74 | 4.42 | 8.20 | 28.2 | -0.01 | 3.3 | 36% | 3% | 2.53 / 4.42 / 6.36 | 2.47 / 4.42 / 6.36 |
| c2. iid Student t | 4.76 | 4.44 | 8.16 | 27.6 | -0.01 | 3.3 | 35% | 3% | 2.53 / 4.44 / 6.35 | 2.50 / 4.42 / 6.35 |
| c3. AR(1) normal | 4.73 | 4.41 | 8.16 | 28.2 | 0.28 | 4.4 | 71% | 18% | 1.81 / 4.45 / 7.04 | 1.84 / 4.44 / 7.01 |
| c4. AR(1) t | 4.75 | 4.43 | 8.16 | 27.8 | 0.28 | 4.3 | 69% | 17% | 1.86 / 4.45 / 7.04 | 1.84 / 4.43 / 7.02 |
| d2. 2-state Gaussian HMM | 5.03 | 4.73 | mixture | 26.6 | 0.16 | 6.0 | 71% | 46% | 1.31 / 5.21 / 7.45 | 1.29 / 5.21 / 7.45 |

### fit

Normal: log-likelihood 126.8, BIC -244.2. Student t: df 30, BIC -239.6 (skew 0.00, kurtosis 3.26). AR(1): phi 0.298 (SE 0.089, t 3.3), 115 pairs. 2-state HMM: log-likelihood 134.8, BIC -241.0. Autocorrelation lags 1 to 5: 0.30, 0.08, 0.06, 0.19, -0.04 (about 2 standard errors at 0.18). Politis-White block length: 2.55.

### subs

| Sample | Years | Arithmetic | Geometric | SD | Loss years |
|---|---|---|---|---|---|
| 1896-1949 | 47 | 3.13 | 2.74 | 9.17 | 36.2% |
| 1950-2019 | 70 | 5.82 | 5.56 | 7.38 | 22.9% |
| 1980-2019 | 40 | 6.96 | 6.76 | 6.58 | 15.0% |
| 1896-1979 | 77 | 3.59 | 3.22 | 8.77 | 35.1% |
| all | 117 | 4.74 | 4.42 | 8.22 | 28.2% |
| excluding 1914-18 and 1939 | 111 | 5.25 | 4.94 | 8.03 | 25.2% |

### se

Naive SE 0.76; AR(1) corrected 1.04 (x1.37); Newey-West (2 lags) 0.91; block bootstrap 0.91; AR(1) parametric bootstrap 1.05. Effective independent annual observations 63. Block-bootstrap interval for the mean, 2.5/10/50/90/97.5%: 2.90, 3.55, 4.74, 5.90, 6.46.

### lvl2

| Parameter | Low (10th) | Central | High (90th) | 95% interval |
|---|---|---|---|---|
| Arithmetic mean, % a year | 3.41 | 4.74 | 6.07 | 2.71 to 6.78 |
| Standard deviation, % a year | 7.47 | 8.22 | 8.96 | |
| Lag-1 autocorrelation | 0.19 | 0.30 | 0.42 | |

### break

Largest mean-shift statistic over candidate break years (15% trimmed): 2.41 at 1921; null 95th percentile 3.84; p = 0.38 (AR(1) parametric bootstrap, 2,000 series). Fixed-date contrasts (the date picked after seeing the data): 1950 on versus before 2.69 points, t = 1.38; 1980 on versus before 3.38 points, t = 1.99.

### weights

| Period | Risky weight (equity plus housing), median | Equity within risky, median |
|---|---|---|
| 1896-1913 | 0.86 (n=13) | 0.37 (n=12) |
| 1919-1939 | 0.50 (n=17) | 0.61 (n=17) |
| 1947-1969 | 0.47 (n=19) | 0.49 (n=19) |
| 1970-1989 | 0.76 (n=15) | 0.30 (n=20) |
| 1990-2019 | 0.85 (n=21) | 0.35 (n=28) |

### series

| Real return series (JST UK) | Mean 1896-2019 | Geo | SD | Mean 1950-2019 | SD |
|---|---|---|---|---|---|
| capital_tr (JST wealth) | 4.74 | 4.42 | 8.22 | 5.82 | 7.38 |
| risky_tr | 6.35 | 5.90 | 9.84 | 7.77 | 9.17 |
| safe_tr | 1.31 | 1.04 | 7.48 | 1.82 | 6.17 |
| equity | 6.77 | 5.07 | 19.10 | 9.01 | 22.26 |
| housing | 5.40 | 5.02 | 9.01 | 6.44 | 8.36 |
| bonds | 1.91 | 1.24 | 11.86 | 2.64 | 11.14 |
| bills | 0.71 | 0.58 | 5.07 | 1.00 | 3.59 |

### mix

| Band (Round 8, Table 2.2) | Property | Financial | Pension | Physical | Mix mean (financial 30/60/90% equity) | Mix SD (same) |
|---|---|---|---|---|---|---|
| D4-5 | 37% | 7% | 36% | 20% | 3.95 / 4.06 / 4.16 | 5.95 / 6.06 / 6.20 |
| D6-7 | 46% | 9% | 32% | 13% | 4.29 / 4.44 / 4.59 | 6.44 / 6.60 / 6.79 |
| D8-9 | 43% | 13% | 35% | 9% | 4.38 / 4.59 / 4.79 | 6.62 / 6.87 / 7.17 |
| D10 | 38% | 19% | 36% | 6% | 4.39 / 4.70 / 5.01 | 6.77 / 7.22 / 7.78 |
| JST wealth return, same years | | | | | 4.74 | 8.22 |

### conv

| Paths N | Mean 100y gain | range over 5 seeds | 30y mean P10 | range | 30y mean | range | 30y mean P90 | range | Within 0.1? |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 4.820 | 0.346 | 2.128 | 1.001 | 4.740 | 0.564 | 7.200 | 0.894 | no |
| 300 | 4.783 | 0.198 | 2.245 | 0.914 | 4.876 | 0.360 | 7.590 | 0.614 | no |
| 1,000 | 4.742 | 0.087 | 2.173 | 0.193 | 4.777 | 0.203 | 7.320 | 0.463 | no |
| 3,000 | 4.747 | 0.064 | 2.161 | 0.133 | 4.734 | 0.075 | 7.338 | 0.168 | no |
| 10,000 | 4.749 | 0.018 | 2.167 | 0.071 | 4.748 | 0.057 | 7.315 | 0.080 | yes |
| 30,000 | 4.744 | 0.027 | 2.174 | 0.041 | 4.749 | 0.022 | 7.337 | 0.052 | yes |
| 100,000 | 4.743 | 0.015 | 2.161 | 0.022 | 4.743 | 0.026 | 7.327 | 0.048 | yes |

