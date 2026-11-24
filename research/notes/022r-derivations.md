# 022r: derivations

Method for the computed rows in `docs/model-v3/inputs-added/wealth.md`. Data held in the repo (`Rates Data/totalwealthtables.xlsx`, `model_v2/wid_out/wid_long.csv`). Run with `python3 -I`. Accessed 2026-11-17.

## 1. Shares of households and wealth up to £1m (I-W6a1 to I-W6d2)
- Household shares: Table 2.5, April 2020 to March 2022, weighted frequencies over 26.991m households: at least £85k 72.7%, £200k 59.2%, £300k 49.3%, £500k 34.2%, £1m 14.1%. Log-linear interpolation between these points for £150k, £250k and £500k.
- Alternative: decile bounds from `docs/model-v3/inputs.md` (D4 to 5 about £104k to £293k, D6 to 7 to £567k, D8 to 9 to £1.208m, D10 above): 70%, 50%, 30%, 10% of households above £104k, £293k, £567k, £1.208m. Used as the low or high bound.
- Wealth shares: Table 2.2 decile aggregates: £392,482m + £651,950m (D4 to 5), £955,204m + £1,322,966m (D6 to 7), £1,805,596m + £2,628,545m (D8 to 9), £5,523,204m (D10), total £13,568bn. Cumulative from the top: 40.7% above £1.208m, 73.4% above £567k, 90.2% above £293k, 97.9% above £104k. Log-linear interpolation in the threshold.

## 2. Pareto tail above £1.208m (I-W5b, I-W6e to I-W6g2)
- Top decile = 2.699m households, aggregate £5,523bn plus a share e of total wealth added for the missing top wealth (e = 0, 5.0%, 5.6%, from I-D4e). Mean above the bound m = D10' / 2.699m; Pareto alpha = (m/1.208m) / (m/1.208m - 1): 2.441, 2.109, 2.079.
- Households share above x = 10% x (x / £1.208m)^-alpha; wealth share = share x 26.991m x alpha x / (alpha - 1) divided by total wealth (1 + e).
- Results: at £2m, 2.9% to 3.5% of households and 19.7% to 25.5% of wealth; at £5m, 0.3% to 0.5% and 5.3% to 9.5%; at £10m, 0.06% to 0.12% and 1.9% to 4.5%. Top 1% of households: threshold £3.10m to £3.66m, share 10.5% to 13.3%.
- A Pareto fitted to one aggregate is a convenience, not a finding. The survey-only case sits below published adjusted top-1% shares (14.4% to 23%, per adult, 2016-18), which use tax data and the Rich List.

## 3. Other computed rows
- I-W5a: decile 10 share of total 40.71%; excluding private pension wealth 40.10%; pension share of total 35.4% (£4,806bn).
- I-W7a, I-W7b: WID series `shweal_p99p100_992_j` and `shweal_p90p100_992_j`, GB, minimum and maximum over 1990 to 2024.
- I-W8a, I-W8b: annual rate = 1 - sqrt(two-year persistence); constant hazard assumed.
- I-W1b: (2.4)^(1/11) - 1 = 8.3%, (1.5)^(1/11) - 1 = 3.8%, gap 4.5 points.
- I-W9e: 100 - 24 - 21 = 55.
