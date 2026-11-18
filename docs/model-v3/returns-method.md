# Model v3: how the return range is built (brief 036r)

Status: research result for stage C; nothing chosen for the author and no register, tornado or metrics file edited. Date 2026-11-18. Scripts and tables: `docs/model-v3/returns/` (`common.py`, `generators.py`, `run_generators.py`, `run_level2.py`, `run_composition.py`, `run_convergence.py`, `tables.py`, `check.py`; run each with `python3 -I`, in that order). Units: real annual returns in % a year; the series is the UK real total return on wealth (JST `capital_tr` deflated by CPI), 117 years, 1896 to 2019, with 1940 to 1946 absent.

## 1. What it says
1. **Recommended generator: an AR(1) with normal innovations, parameterised by the arithmetic mean, the marginal standard deviation and the lag-1 autocorrelation** (4.74%, 8.22%, 0.30 at the sample). Lag-1 autocorrelation is significant (t = 3.3); fat tails (Student t fits at 30 degrees of freedom, so it is normal) and regimes (the two-state model is not preferred by BIC and gives implausible loss runs) are not supported. A stationary block bootstrap with mean block 3 is the robustness check. This is a recommendation, the author chooses.
2. **The mean is 4.742%, the SD 8.219%, the geometric mean 4.420%.** The 4.76 in `drivers.md` is the geometric mean plus half the variance (4.420 + 0.338 = 4.758), an approximation; the observed arithmetic mean is 4.74. The generator takes the **arithmetic** mean; wealth paths then compound at about the arithmetic mean minus half the variance.
3. **The tornado double counts.** Its 2.18% to 7.47% is the spread of 30-year paths (level 1 return risk): the fitted generator with the mean known gives 2.17% to 7.32% for the 30-year mean. The true mean's own uncertainty (level 2) is **3.41% to 6.07%** (80% band, central 4.74), about a third as wide. On the tornado's own arithmetic the M1 swing from the return falls from 8.8 to about 4.1 to 4.4 points of GDP. The sign of M1 is still not safe: it is negative at a true arithmetic mean below 3.5% to 3.8%, a probability of about 12% to 18% from level 2 alone.
4. **The history supports about 63 effective annual observations,** so 0.6 of an independent 100-year path (1.17 on the raw count). Any 100-year path is a resampling of that information, not new information.
5. **No evidence of a structural break** (p = 0.38 for the largest shift). Pool; run 1950 to 2019 (arithmetic 5.82%) as a named scenario only if the author wants one.
6. **One return series is enough for level 2 now** (a payer mix moves the mean by -0.8 to +0.3 points, inside the level 2 standard error of 1.04), but the mix lowers the volatility (6.0% to 7.8% against 8.2%) and orders it by band; stage C needs asset-class rows by band before the level 1 range is split by band.
7. **10,000 paths** settle the toy statistics to 0.1 point across five seeds. The full test is stage C's.

## 2. Q1 Generator
Observed record against the candidates (20,000 simulated paths of 100 years each unless stated; seed 36; "88-window style" applies the observed procedure to 117-year simulated paths):

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

Normal: log-likelihood 126.8, BIC -244.2. Student t: df 30, BIC -239.6 (skew 0.00, kurtosis 3.26). AR(1): phi 0.298 (SE 0.089, t 3.3), 115 pairs. 2-state HMM: log-likelihood 134.8, BIC -241.0. Autocorrelation lags 1 to 5: 0.30, 0.08, 0.06, 0.19, -0.04 (about 2 standard errors at 0.18). Politis-White block length: 2.55.

- **Replay of historical windows (a)** reproduces the record by construction but is not a distribution: all 117 windows of 100 years contain the stitched 6-year loss run, so 100% show a run of 4 or more and 81% of 6 or more. The 117 start years are heavily overlapping and cross the missing 1940 to 1946 years (29 of the 88 thirty-year windows do).
- **Independent draws (c1, c2)** match the mean, SD and loss frequency but lose the serial correlation (-0.01 against 0.30) and understate the spread of 30-year means (2.5% to 6.4% against the observed 2.2% to 7.5%) and the long loss runs (3% against 17% to 18% at 6 or more).
- **AR(1) (c3)** matches lag-1 correlation (0.28), the loss frequency and the 88-window spread best (1.8% to 7.0% against 2.2% to 7.5%). Student t innovations (c4) change nothing.
- **Block bootstrap (b)** with mean block 3 (the Politis-White length is 2.55) reproduces 2.1% to 6.8% but only 0.18 of the serial correlation; longer blocks recover more correlation (0.24 at 10) and keep the mean exact.
- **Regimes (d2)** raise the mean (5.03%) and give a persistent bad state (mean -5.6%) with 46% of 100-year paths running 6 or more loss years; its BIC is worse than the plain normal. **Dropping the war years (d)** raises the mean to 5.26% (sample 5.25%).
- **Effective independent sample for 100-year paths.** Raw: 117 / 100 = 1.17. Corrected for lag-1 correlation of 0.30: n_eff = 117 x (1 - 0.30) / (1 + 0.30) = 63 observations, so 0.63 independent 100-year paths (the variance of a mean is inflated by (1 + rho) / (1 - rho) = 1.87).
- **Limits.** One realisation of one country; the 1939/1947 seam is stitched in the series and handled by wrapping within each contiguous segment in the bootstrap; lag 4 autocorrelation is 0.19, about two standard errors, not modelled; the normal has no lower bound at -100% (the fitted SD makes that irrelevant). Not tested: a longer history (the Bank of England series), asset-class generators, state-dependent volatility (GARCH).

## 3. Q2 Mean, its two readings, standard deviation
Same sample, exactly (n = 117, 1896 to 2019):

| Statistic | Value |
|---|---|
| Arithmetic mean | 4.742% (the register's 4.74; the second method on the original xlsx gives 4.742) |
| Geometric mean | 4.420% |
| Standard deviation (n - 1) | 8.219% (8.18% with n; the register's 8.2) |
| Half the variance | 0.338 |
| Arithmetic minus half the variance | 4.404 (the geometric is 4.420; the 0.016 gap is higher-order terms) |
| Geometric plus half the variance | 4.758 (the 4.76 in `drivers.md`) |

The 4.76 is derived (geometric plus half the variance), not observed; use 4.74. **The generator takes the arithmetic mean** (the tax falls on the expected annual gain), with the marginal SD and phi; geometric means follow as output and are not a parameter.

## 4. Q3 Level 2: the true mean, SD and autocorrelation
Naive SE 0.76; AR(1) corrected 1.04 (x1.37); Newey-West (2 lags) 0.91; block bootstrap 0.91; AR(1) parametric bootstrap 1.05. Effective independent annual observations 63. Block-bootstrap interval for the mean, 2.5/10/50/90/97.5%: 2.90, 3.55, 4.74, 5.90, 6.46.

| Parameter | Low (10th) | Central | High (90th) | 95% interval |
|---|---|---|---|---|
| Arithmetic mean, % a year | 3.41 | 4.74 | 6.07 | 2.71 to 6.78 |
| Standard deviation, % a year | 7.47 | 8.22 | 8.96 | |
| Lag-1 autocorrelation | 0.19 | 0.30 | 0.42 | |

Recommended band: the central plus or minus 1.2816 standard errors (10th to 90th percentile of a normal), using the AR(1)-corrected standard error for the mean (the widest, 1.04; Newey-West and the block bootstrap give 0.91 and a band of 3.6 to 5.9) and an AR(1) parametric bootstrap for the SD and phi. (J) The 80% band keeps the 10th/90th convention of the register.

Sub-samples:

| Sample | Years | Arithmetic | Geometric | SD | Loss years |
|---|---|---|---|---|---|
| 1896-1949 | 47 | 3.13 | 2.74 | 9.17 | 36.2% |
| 1950-2019 | 70 | 5.82 | 5.56 | 7.38 | 22.9% |
| 1980-2019 | 40 | 6.96 | 6.76 | 6.58 | 15.0% |
| 1896-1979 | 77 | 3.59 | 3.22 | 8.77 | 35.1% |
| all | 117 | 4.74 | 4.42 | 8.22 | 28.2% |
| excluding 1914-18 and 1939 | 111 | 5.25 | 4.94 | 8.03 | 25.2% |

The register's 5.56% and 6.76% are the geometric means; the arithmetic means are 5.82% and 6.96%.

**Break test.** Largest mean-shift statistic over candidate break years (15% trimmed): 2.41 at 1921; null 95th percentile 3.84; p = 0.38 (AR(1) parametric bootstrap, 2,000 series). Fixed-date contrasts (the date picked after seeing the data): 1950 on versus before 2.69 points, t = 1.38; 1980 on versus before 3.38 points, t = 1.99. The sample is short, so the test has low power; the fixed-date contrasts are the author's own post-hoc dates and are not evidence.

**One-paragraph choice for the author.** Pool: with 63 effective observations and p = 0.38 for the largest shift, the 1950 and 1980 sub-sample means (5.82% and 6.96%) sit within about one and two standard errors of the pooled 4.74% and a wider level 2 band (3.41% to 6.07%) already covers the 1950 value. Run the break as a named level 2 scenario only if the author thinks the post-1950 economy is structurally different for a reason the data do not test (not a statistical finding): then use arithmetic 5.82%, SD 7.38% and label it a scenario.

### Double count to remove from the tornado
The tornado row for I-D1a ranks the 2.18% to 7.47% spread (level 1) as parameter ignorance. Replace its swing with the level 2 band: at the tornado's own identity, M1a = epsilon x g x omega, the swing falls from 8.78 to 4.42 points of GDP (epsilon held at 29.97%) or 4.12 (epsilon recalibrated so M1a is 7.34 at 4.74%); arithmetic: 0.2997 x (6.07 - 3.41)% x 5.54 = 4.42. M1 reaches zero at an arithmetic mean of 3.55% (epsilon held) or 3.80% (recalibrated); with a standard error of 1.04 the probability that the true mean is below that is 12% (z = -1.15) or 18% (z = -0.90). Indicative: all other inputs are at their centres.

## 5. Replacement register rows (not applied)
Row format as in 012r; JST source S10; licence unconfirmed (section 7).

| ID | Input (feeds) | Unit | Low | Central | High | How the range was set | Source | Licence and access | Coverage | In repo | Confidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| I-D1a | Mean real total return on wealth, **arithmetic**, level 2 (g; M1a identity, P3) | % per year | 3.41 | 4.74 | 6.07 | Central: sample arithmetic mean. Low and high: central -/+ 1.2816 x 1.04 (AR(1)-corrected standard error), the 10th and 90th percentile of the true mean. (J) | S10; this note | Licence unconfirmed; cite only | UK 1896-2019, 117 years, 1940-46 absent | `Rates Data/JSTdatasetR6.xlsx`, `model_v2/jst_r6.json` | medium: 63 effective observations |
| I-D1a2 | Mean real total return, **geometric** (wealth path compounding; M3) | % per year | 3.07 | 4.42 | 5.73 | Central: sample geometric mean. Low and high: I-D1a low and high less half the variance (0.34), an approximation. Derived, not sampled separately | S10; this note | as above | as above | as above | medium |
| I-D1b | Standard deviation of annual real total return, marginal, level 2 | % per year | 7.47 | 8.22 | 8.96 | Central: sample SD. Low and high: central -/+ 1.2816 x 0.58 (AR(1) parametric bootstrap SE). (J) | S10; this note | as above | as above | as above | medium |
| I-D1b2 | Lag-1 autocorrelation of the annual real return, level 2 | correlation | 0.19 | 0.30 | 0.42 | Central: sample. Low and high: central -/+ 1.2816 x 0.088 (analytic SE sqrt((1 - rho^2)/n), confirmed by the parametric bootstrap). Lag 4 is 0.19 and is not modelled. (J) | S10; this note | as above | as above | as above | medium |
| I-D1c | Loss-year frequency: **output of the generator, not an input** | % of years | n/a | 28.2 (observed; generator 28.2) | n/a | Demoted: with mean, SD and phi sampled, the frequency follows (28.3% for the AR(1)). Keep as a reported check | S10 | as above | as above | as above | high |
| I-D1d | Longest loss run: **output of the generator, not an input** | years | n/a | 5 within contiguous data; 6 across the 1940-46 gap (register high of 6 crosses the gap) | n/a | Demoted: at 100 years, 71% of AR(1) paths show a run of 4 or more, 18% of 6 or more (observed one path of 117 years). Correct the register's 6 to 5 or footnote the gap | S10 | as above | as above | as above | high |
| I-D1a0 | Spread of 30-year geometric means (level 1 display, **not a level 2 range**) | % per year | 2.18 | 3.73 | 7.47 | P10, median, P90 of 88 rolling 30-year windows, 29 of which cross the 1940-46 gap. Contiguous windows only (59): 2.56, 6.51, 7.67. Generator at central parameters, independent 30-year paths: 2.17 / 4.75 / 7.32 (arithmetic) | S10; this note | as above | as above | as above | medium |
| I-D1f | Named scenario: UK 1950-2019 arithmetic mean and SD (only if the author runs the break) | % per year | n/a | 5.82 (SD 7.38) | n/a | Sample 1950-2019, 70 years; geometric 5.56. Not sampled | S10 | as above | UK 1950-2019 | as above | low: one sub-sample |
| I-D1g | Effective independent annual observations | count | n/a | 63 | n/a | 117 x (1 - 0.30)/(1 + 0.30) | this note | n/a | n/a | no | medium |

`I-D1e` (gap to 2025) stays; see section 7.

## 6. Q4 Wealth composition
**How JST builds the series** (NBER w24112, pp. 8 to 12; first 100,000 characters of the paper read, appendices not read): the return on wealth is a weighted average of a risky composite (equity and housing, weighted by stock market capitalisation and housing wealth) and a safe composite (bonds and bills, equal weights because the split of public debt is unknown), with country-year weights from outstanding asset stocks. Real returns are deflated with realised CPI inflation, (1 + R)/(1 + pi) - 1. Housing is rental yield plus capital gain, including imputed rents for owner-occupiers. Annual, with housing timed t to t+1 in the paper. A country-year needs all four asset returns. JST's wealth excludes pensions, private business and household cash, which Round 8 counts (pension alone is 36% of every upper band).

Backing the weights out of the held series (risky weight = (wealth - safe)/(risky - safe), only in years where risky and safe differ by 3 points or more; my calculation):

| Period | Risky weight (equity plus housing), median | Equity within risky, median |
|---|---|---|
| 1896-1913 | 0.86 (n=13) | 0.37 (n=12) |
| 1919-1939 | 0.50 (n=17) | 0.61 (n=17) |
| 1947-1969 | 0.47 (n=19) | 0.49 (n=19) |
| 1970-1989 | 0.76 (n=15) | 0.30 (n=20) |
| 1990-2019 | 0.85 (n=21) | 0.35 (n=28) |

So the JST return is 50% to 86% equity and housing, depending on the era, which is more risky exposure than a typical payer's mix.

| Real return series (JST UK) | Mean 1896-2019 | Geo | SD | Mean 1950-2019 | SD |
|---|---|---|---|---|---|
| capital_tr (JST wealth) | 4.74 | 4.42 | 8.22 | 5.82 | 7.38 |
| risky_tr | 6.35 | 5.90 | 9.84 | 7.77 | 9.17 |
| safe_tr | 1.31 | 1.04 | 7.48 | 1.82 | 6.17 |
| equity | 6.77 | 5.07 | 19.10 | 9.01 | 22.26 |
| housing | 5.40 | 5.02 | 9.01 | 6.44 | 8.36 |
| bonds | 1.91 | 1.24 | 11.86 | 2.64 | 11.14 |
| bills | 0.71 | 0.58 | 5.07 | 1.00 | 3.59 |

Payer mix, using Round 8 band shares and JST asset-class returns (assumptions, all (J): property earns the JST housing return with no mortgage gearing; financial wealth is 30%, 60% or 90% equity and the rest bonds and bills; pension earns the JST wealth return; physical wealth earns 0% real; same years, 117):

| Band (Round 8, Table 2.2) | Property | Financial | Pension | Physical | Mix mean (financial 30/60/90% equity) | Mix SD (same) |
|---|---|---|---|---|---|---|
| D4-5 | 37% | 7% | 36% | 20% | 3.95 / 4.06 / 4.16 | 5.95 / 6.06 / 6.20 |
| D6-7 | 46% | 9% | 32% | 13% | 4.29 / 4.44 / 4.59 | 6.44 / 6.60 / 6.79 |
| D8-9 | 43% | 13% | 35% | 9% | 4.38 / 4.59 / 4.79 | 6.62 / 6.87 / 7.17 |
| D10 | 38% | 19% | 36% | 6% | 4.39 / 4.70 / 5.01 | 6.77 / 7.22 / 7.78 |
| JST wealth return, same years | | | | | 4.74 | 8.22 |

Reading. The payer mix (D10) has a mean 0.7 below to 0.3 above the JST wealth return and an SD of 6.8% to 7.8% against 8.2%; lower bands have lower means (3.9% to 4.8%) and SDs (6.0% to 6.9%). The differences in mean are inside the level 2 standard error (1.04 points), so **one series is enough for level 2**. They are not inside the level 1 picture: the mix has more diversification and a different volatility by band. **Recommendation:** keep one series for the first stage C build; carry asset-class rows (mean, SD, correlation already in I-H6a to I-H6i) and band weights (Round 8; I-T6a to I-T6i in `inputs-added/tax.md`, 023r) so a mix can be added. **Register needs (not in it):** equity share of financial wealth by band (the held `financialwealthtables.xlsx` is the likely source), home mortgage gearing by band (property is net of debt in Round 8), the asset mix inside pensions, and private business wealth, which JST excludes. Limits: the mapping is mine; equity and housing correlation in the JST data is 0.03 over 117 years.

## 7. Q5 The gap to 2025 and the options
- **Missing:** `capital_tr` and `risky_tr` end in 2019 (117 years); equity, housing, bond, bill and CPI series run to 2020 (2020: equity -10.2%, housing +4.2%, bonds +4.8% real, from the held file). Missing for 2020 to 2025, six years: the 2020 crash and rebound, the 2022 inflation and gilt shock (a high-inflation year with large real losses on bonds), the 2022 to 2024 house price fall and recovery, and equity moves since. I-D1e holds the gap (5, 6, 6 years).
- **No later JST release** was seen. The NBER page states no release number; a direct fetch of macrohistory.net failed this session. Whether Release 7 exists is open.

| Option | Covers | Licence, as far as read | Status |
|---|---|---|---|
| JST later release | wealth return to a later year | NBER page: free open access under JST terms (macrohistory.net/data/#UseTerms); commercial data providers barred from integrating or selling it; citation rule not stated on that page; full text not read | Unconfirmed |
| Bank of England, A millennium of macroeconomic data v3.1 | long UK series to 2016 | Page states no licence, only a Bank copyright notice; contact address given on the page | Ends 2016; not a bridge; series list not confirmed |
| ONS UK House Price Index | house prices, monthly, UK | Open Government Licence v3.0 (page read) | Start year not confirmed; no rents |
| ONS consumer price index | deflator | Not checked this session | Needed for any splice |
| Land Registry house price data | house prices | Not checked this session | Same series as the ONS index |
| Nationwide house price index | house prices | Not checked this session | Licence unchecked |
| FTSE All-Share total return (FTSE Russell) | equity total return | Not checked this session; index data is normally licensed | Licence unchecked |

No splice is made. Rents and bond total returns (gilts) have no option above beyond a licence-unchecked FTSE or Bank of England gilt series.

## 8. Q6 Sample size and seed
Generator: the recommended AR(1) (mean 4.742%, phi 0.2975, marginal SD 8.219%). Statistic: the mean annual gain over 100 years and the P10, mean and P90 of its 30-year mean. Seeds 1 to 5.

| Paths N | Mean 100y gain | range over 5 seeds | 30y mean P10 | range | 30y mean | range | 30y mean P90 | range | Within 0.1? |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 4.820 | 0.346 | 2.128 | 1.001 | 4.740 | 0.564 | 7.200 | 0.894 | no |
| 300 | 4.783 | 0.198 | 2.245 | 0.914 | 4.876 | 0.360 | 7.590 | 0.614 | no |
| 1,000 | 4.742 | 0.087 | 2.173 | 0.193 | 4.777 | 0.203 | 7.320 | 0.463 | no |
| 3,000 | 4.747 | 0.064 | 2.161 | 0.133 | 4.734 | 0.075 | 7.338 | 0.168 | no |
| 10,000 | 4.749 | 0.018 | 2.167 | 0.071 | 4.748 | 0.057 | 7.315 | 0.080 | yes |
| 30,000 | 4.744 | 0.027 | 2.174 | 0.041 | 4.749 | 0.022 | 7.337 | 0.052 | yes |
| 100,000 | 4.743 | 0.015 | 2.161 | 0.022 | 4.743 | 0.026 | 7.327 | 0.048 | yes |

**10,000 paths** is the first size from which all four statistics sit within 0.1 point across five seeds, and they stay so at 30,000 and 100,000. Limit: this is a toy test of means and percentiles of a stationary generator; tails (loss runs), the transition horizon and the interaction with policy levers need more.

## 9. Open questions answered
- **Later JST release.** None seen and none read; the licence is unconfirmed (above).
- **War years.** Kept in the central sample (as the register). Dropping 1914 to 1918 and 1939 (6 years) raises the arithmetic mean from 4.74% to 5.25% (geometric 4.42% to 4.94%), lowers the SD from 8.22% to 8.03% and the loss frequency from 28.2% to 25.2%. The 1940 to 1946 years are not in the data at all. Treat the war years as a named sensitivity of +0.5 points on the mean, which is inside the level 2 band.

## 10. Checks
- Second method (`check.py`, pure Python on the original `JSTdatasetR6.xlsx`): n = 117, mean 4.742%, geometric 4.420%, SD 8.219%, rho 0.303; the generator simulated without numpy gives mean 4.72% and SD 8.21%; both within 0.05 point of the sample.
- Hand recomputation of one table. Standard error: 8.219 / sqrt(117) = 0.7598; inflation sqrt((1 + 0.3030)/(1 - 0.3030)) = sqrt(1.8696) = 1.3674; 0.7598 x 1.3674 = 1.039; 4.742 -/+ 1.2816 x 1.039 = 3.41 and 6.07. n_eff = 117 x 0.697/1.303 = 62.6. Geometric check: 4.742 - 0.5 x (0.08219)^2 x 100 = 4.742 - 0.338 = 4.404.
- Register row ids cited (I-D1a to I-D1e, I-H6a, I-H6i) exist in `inputs.md`; I-T6a to I-T6i are rows of `inputs-added/tax.md` (023r), not yet merged into `inputs.md`.
- Every number above is printed by a script; `tables.py` writes `tables.md` from their JSON outputs.

## 11. Not tested
Longer UK history; asset-class generators; GARCH or other state-dependent volatility; the interaction of return paths with policy levers and the transition horizon; any non-UK evidence; the effect of mortgage gearing and business wealth on payers' returns; a break test with a known date and a non-stationary alternative; rerunning the tornado.
