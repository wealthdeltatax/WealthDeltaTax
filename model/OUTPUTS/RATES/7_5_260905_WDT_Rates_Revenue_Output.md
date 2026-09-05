# WDT Rates and Revenue — Model Output

**Run date:** 2026-09-05  
**Scenario:** 2007 Balanced  
**Model version:** v7  
**Parameters file:** `WDT_Params.toml`  

## B.1 Active Parameters

| Parameter | Value |
|---|---|
| $\tau_0$ (floor rate) | 15% |
| $\tau_m$ (ceiling rate) | 70% |
| $k$ (steepness, per £m) | 0.001 |
| $W_{min}$ (£m) | £2.0m |
| SRR capitalisation ratio | 3.0× |
| LRR floor (years of expenditure) | 3.0 years |
| Budget base (£b) | £1,157.4b |
| Budget growth (p.a). | 4.51% |
| Historical mean return | 10.45% |

**Growth tiers:**

| Tier | Weight | Differential | Implied return |
|---|---|---|---|
| Poor | 10% | -4.55% | 5.90% |
| Ok | 30% | -2.05% | 8.40% |
| Good | 40% | +0.95% | 11.40% |
| Great | 20% | +3.45% | 13.90% |

## B.2 SSM Results — Active Scenario

| Metric | Value |
|---|---|
| SRR fill year | 3 |
| LRR breakeven year | 19 |
| Annual expenditure at LRR breakeven (£b) | £2,560b |
| SRR balance at LRR breakeven (£b) | £1,460b |
| LRR surplus at breakeven (£b) | £104b |
| LRR failure year | no failure within 71-year window |
| SRR failure year | no failure within 71-year window |
| LRR→SRR failure gap (years) | — |

**SSM Step-5 coverage fraction by window (average % of annual expenditure available for labour tax relief):**

| Window | SSM coverage | Zero-coverage years | Min LRR balance (£b) | Years LRR below floor |
|---|---:|---:|---:|---:|
| 5 years | 0.0% | 5 | £7,858b | 5 |
| 10 years | 6.4% | 7 | £7,858b | 7 |
| 20 years | 21.3% | 10 | £7,858b | 10 |
| 50 years | 307.1% | 14 | £7,858b | 14 |

*SSM applies uniform historical returns across the population (correlated-shock assumption — worst-case floor). Coverage fraction = Step-5 remainder / annual expenditure; zero in any year where LRR or SRR balance hits zero. TCM coverage (heterogeneous-tier ceiling) appears in §B.3.*

## B.3 TCM Results — N=19 periods

### B.3.1 Net worth — start ($V_0$) and year N (£m)

*$V_0$ is the bracket mean wealth (£m) at entry, identical across tiers within a bracket. V_N is the true wealth (before tax settlement) at the end of period N for a representative taxpayer, varying by tier due to persistent return differentials. Figures are for a single representative taxpayer; they do not reflect aggregate portfolio wealth.*

| Net worth (£m) | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ |
|---|---|---|---|---|---|---|---|---|---|---|
| **$V_0$ (start, all tiers)** | £0.402m | £0.570m | £0.782m | £1.109m | £1.629m | £2.858m | £7.135m | £19.854m | £53.385m | £139.607m |
| **V_N -4.55% (Poor)** | £0.64m | £0.91m | £1.25m | £1.77m | £2.61m | £4.57m | £11.41m | £31.75m | £85.36m | £223.23m |
| **V_N -2.05% (Ok)** | £1.02m | £1.44m | £1.98m | £2.80m | £4.12m | £7.23m | £18.05m | £50.21m | £135.02m | £353.10m |
| **V_N +0.95% (Good)** | £1.74m | £2.46m | £3.38m | £4.79m | £7.04m | £12.36m | £30.84m | £85.82m | £230.76m | £603.47m |
| **V_N +3.45% (Great)** | £2.68m | £3.80m | £5.23m | £7.41m | £10.88m | £19.10m | £47.67m | £132.63m | £356.64m | £932.65m |

### B.3.2 Net per taxpayer per year — capitalisation window average (£/yr)

*Average annual net tax per representative taxpayer over the capitalisation window (SRR fill year to LRR breakeven year). Zeros suppressed.*

| Tier \ Bracket | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ |
|---|---|---|---|---|---|---|---|---|---|---|
| -4.55% (Poor) | £— | £— | £— | £— | £4,897 | £11,854 | £29,698 | £83,531 | £230,983 | £647,561 |
| -2.05% (Ok) | £— | £— | £— | £5,341 | £16,508 | £28,670 | £71,890 | £202,722 | £564,248 | £1,605,704 |
| +0.95% (Good) | £— | £3,143 | £8,653 | £18,646 | £34,334 | £59,282 | £148,894 | £421,881 | £1,188,304 | £3,470,065 |
| +3.45% (Great) | £4,468 | £11,740 | £21,216 | £35,314 | £56,583 | £97,252 | £244,752 | £697,543 | £1,992,762 | £5,985,093 |

### B.3.3 Annual wealth burden (tax as % of net worth)

| Tier \ Bracket | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ |
|---|---|---|---|---|---|---|---|---|---|---|
| -4.55% (Poor) | 0.00% | 0.00% | 0.00% | 0.00% | 0.17% | 0.25% | 0.25% | 0.25% | 0.26% | 0.28% |
| -2.05% (Ok) | 0.00% | 0.00% | 0.00% | 0.20% | 0.40% | 0.42% | 0.42% | 0.42% | 0.44% | 0.49% |
| +0.95% (Good) | 0.00% | 0.18% | 0.29% | 0.42% | 0.53% | 0.56% | 0.56% | 0.57% | 0.61% | 0.70% |
| +3.45% (Great) | 0.24% | 0.37% | 0.47% | 0.55% | 0.62% | 0.64% | 0.65% | 0.67% | 0.72% | 0.87% |

### B.3.4 Effective rate on gains (tax as % of annual gain)

| Tier \ Bracket | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ |
|---|---|---|---|---|---|---|---|---|---|---|
| -4.55% (Poor) | 0.0% | 0.0% | 0.0% | 0.0% | 3.4% | 5.0% | 5.0% | 5.0% | 5.2% | 5.6% |
| -2.05% (Ok) | 0.0% | 0.0% | 0.0% | 4.0% | 8.0% | 8.3% | 8.4% | 8.5% | 8.8% | 9.8% |
| +0.95% (Good) | 0.0% | 3.6% | 5.9% | 8.4% | 10.7% | 11.1% | 11.2% | 11.4% | 12.1% | 13.9% |
| +3.45% (Great) | 4.9% | 7.4% | 9.4% | 11.1% | 12.3% | 12.8% | 12.9% | 13.3% | 14.4% | 17.4% |

### B.3.5 Average annual net tax per taxpayer — lifetime average (£/yr)

| Tier \ Bracket | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ |
|---|---|---|---|---|---|---|---|---|---|---|
| -4.55% (Poor) | £— | £— | £— | £— | £4,186 | £10,338 | £25,901 | £72,866 | £201,606 | £566,034 |
| -2.05% (Ok) | £— | £— | £— | £5,389 | £14,746 | £26,634 | £66,794 | £188,436 | £525,086 | £1,498,335 |
| +0.95% (Good) | £— | £4,373 | £9,398 | £18,270 | £32,128 | £57,757 | £145,120 | £411,665 | £1,162,873 | £3,416,433 |
| +3.45% (Great) | £6,348 | £13,173 | £21,963 | £35,023 | £54,786 | £97,542 | £245,690 | £701,918 | £2,016,927 | £6,122,031 |

### B.3.6 Population distribution (taxpayers per bracket per tier)

*Cell population = bracket population × tier weight. Bracket population is constant within a bracket across tiers.*

| Tier (weight) \ Bracket | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ |
|---|---|---|---|---|---|---|---|---|---|---|
| 10% (Poor) | 692,000 | 692,000 | 692,000 | 692,000 | 346,000 | 276,800 | 62,280 | 6,228 | 623 | 69 |
| 30% (Ok) | 2,076,000 | 2,076,000 | 2,076,000 | 2,076,000 | 1,038,000 | 830,400 | 186,840 | 18,684 | 1,868 | 208 |
| 40% (Good) | 2,768,000 | 2,768,000 | 2,768,000 | 2,768,000 | 1,384,000 | 1,107,200 | 249,120 | 24,912 | 2,491 | 277 |
| 20% (Great) | 1,384,000 | 1,384,000 | 1,384,000 | 1,384,000 | 692,000 | 553,600 | 124,560 | 12,456 | 1,246 | 138 |

### B.3.7 Tax collected per year — capitalisation window average (£m/yr)

*Average annual revenue per bracket-tier cell over the capitalisation window. Row total is the sum across all brackets for that tier. Column total is the sum across all tiers for that bracket. Grand total is in the bottom-right cell.*

| Tier (weight) \ Bracket | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ | **Row total** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 10% (Poor) | £— | £— | £— | £— | £1,694 | £3,281 | £1,850 | £520 | £144 | £45 | **£7,534.3m** |
| 30% (Ok) | £— | £— | £— | £11,089 | £17,135 | £23,808 | £13,432 | £3,788 | £1,054 | £333 | **£70,638.5m** |
| 40% (Good) | £— | £8,699 | £23,950 | £51,613 | £47,518 | £65,637 | £37,093 | £10,510 | £2,960 | £961 | **£248,940.9m** |
| 20% (Great) | £6,184 | £16,249 | £29,362 | £48,874 | £39,155 | £53,839 | £30,486 | £8,689 | £2,482 | £828 | **£236,148.9m** |
| **Column total** | **£6,184.2m** | **£24,947.8m** | **£53,312.7m** | **£111,576.1m** | **£105,502.7m** | **£146,564.9m** | **£82,860.3m** | **£23,506.4m** | **£6,640.6m** | **£2,167.0m** | **£563,262.6m** |

*Row totals in £b/yr:*

| Tier (weight) | £b/yr |
|---|---|
| 10% (Poor) | £7.53b |
| 30% (Ok) | £70.64b |
| 40% (Good) | £248.94b |
| 20% (Great) | £236.15b |
| **Grand total** | **£563.26b** |

### B.3.8 Cohort proportion of total tax paid (%)

*Each cell's capitalisation-window revenue as a percentage of the grand total. Row total is the tier's share; column total is the bracket's share across all tiers.*

| Tier (weight) \ Bracket | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ | **Row total** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 10% (Poor) | 0.0% | 0.0% | 0.0% | 0.0% | 0.3% | 0.6% | 0.3% | 0.1% | 0.0% | 0.0% | **1.3%** |
| 30% (Ok) | 0.0% | 0.0% | 0.0% | 2.0% | 3.0% | 4.2% | 2.4% | 0.7% | 0.2% | 0.1% | **12.5%** |
| 40% (Good) | 0.0% | 1.5% | 4.3% | 9.2% | 8.4% | 11.7% | 6.6% | 1.9% | 0.5% | 0.2% | **44.2%** |
| 20% (Great) | 1.1% | 2.9% | 5.2% | 8.7% | 7.0% | 9.6% | 5.4% | 1.5% | 0.4% | 0.1% | **41.9%** |
| **Column total** | **1.1%** | **4.4%** | **9.5%** | **19.8%** | **18.7%** | **26.0%** | **14.7%** | **4.2%** | **1.2%** | **0.4%** | **100.0%** |

### B.3.9 Revenue by tier (£b/yr)

| Tier | Lifetime avg (£b/yr) | Capitalisation window avg (£b/yr) |
|---|---|---|
| -4.55% (Poor) | £6.5b | £7.5b |
| -2.05% (Ok) | £65.9b | £70.6b |
| +0.95% (Good) | £247.4b | £248.9b |
| +3.45% (Great) | £240.5b | £236.1b |
| **Total** | **£560.3b** | **£563.3b** |

*TCM horizon N is derived from the SSM LRR breakeven year, not the TOML snapshot_N.*

**TCM Step-5 coverage fraction by window:**

| Window | TCM coverage | TCM failure year (LRR) | TCM failure year (SRR) |
|---|---:|---:|---:|
| 5 years | 15.9% | None | None |
| 10 years | 14.6% | None | None |
| 20 years | 35.8% | None | None |
| 50 years | 655.6% | None | None |

*TCM applies heterogeneous tier differentials to the actual historical return series, producing higher revenue than the SSM uniform-return assumption. The SSM forms the solvency/stress-test floor; the TCM ceiling bounds the plausible range. TCM and SSM run independent SRR/LRR balance trackers.*

## B.4 Start-Year Sweep

All figures at $\tau_0$=15%, $\tau_m$=70%, k=0.001, $W_{min}$=£2.0m.

### B.4.1 Extremals — four dimensions

| Dimension | Start year | LRR breakeven | LRR surplus (£b) | LRR failure year | SRR failure year | SSM cov 50yr |
|---|:---:|:---:|---:|:---:|:---:|---:|
| Speed — slowest LRR fill | 2006 | 29 | £523b | none | none | 593.9% |
| Speed — fastest LRR fill | 1970 | 7 | £402b | none | none | 397.5% |
| Margin — thinnest surplus | 1996 | 11 | £6b | none | none | 156.0% |
| Margin — largest surplus | 1963 | 12 | £4,336b | none | none | 459.1% |
| Durability — lowest 50yr SSMcov | 1984 | 9 | £77b | none | none | 95.6% |
| Durability — highest 50yr SSMcov | 1952 | 16 | £2,274b | none | none | 656.3% |
| Resilience — earliest LRR failure | — | — | — | — | — | — |
| Resilience — latest/no LRR failure | 1970 | 7 | £402b | none | none | 397.5% |

*73 start years produce no LRR failure within the 71-year modelling window.*

### B.4.2 Full sweep table (all 73 calendar years)

| Start | SRR fill | LRR fill | LRR surplus (£b) | LRR failure | SRR failure | gap | SSMcov5 | SSMcov10 | SSMcov20 | SSMcov50 | TCMcov10 | TCMcov50 |
|:---:|:---:|:---:|---:|:---:|:---:|:---:|---:|---:|---:|---:|---:|---:|
| 1947 | 3 | 21 | 1,934 | — | — | — | 92.0% | 131.8% | 286.2% | 559.7% | 158.1% | 1321.8% |
| 1948 | 3 | 20 | 2,454 | — | — | — | 97.1% | 139.8% | 300.9% | 587.6% | 164.4% | 1355.1% |
| 1949 | 3 | 18 | 152 | — | — | — | 86.5% | 132.9% | 271.6% | 615.8% | 170.2% | 1385.3% |
| 1950 | 3 | 18 | 2,153 | — | — | — | 101.5% | 146.3% | 315.7% | 615.8% | 166.2% | 1355.4% |
| 1951 | 3 | 17 | 2,126 | — | — | — | 103.7% | 149.9% | 323.2% | 630.2% | 167.7% | 1358.0% |
| 1952 | 3 | 16 | 2,274 | — | — | — | 107.7% | 156.7% | 336.7% | 656.3% | 171.9% | 1381.8% |
| 1953 | 3 | 15 | 1,115 | — | — | — | 97.2% | 145.4% | 321.1% | 627.0% | 176.9% | 1288.5% |
| 1954 | 3 | 17 | 3,266 | — | — | — | 151.2% | 218.8% | 379.3% | 605.3% | 156.6% | 1160.7% |
| 1955 | 3 | 16 | 3,113 | — | — | — | 152.9% | 221.5% | 384.3% | 612.8% | 154.7% | 1153.4% |
| 1956 | 3 | 15 | 2,704 | — | — | — | 153.3% | 223.7% | 391.3% | 624.9% | 248.8% | 1246.8% |
| 1957 | 3 | 14 | 2,681 | — | — | — | 157.3% | 230.1% | 402.6% | 643.2% | 271.6% | 1279.4% |
| 1958 | 3 | 13 | 360 | — | — | — | 128.9% | 195.5% | 353.5% | 565.7% | 229.7% | 1093.3% |
| 1959 | 3 | 13 | 586 | — | — | — | 142.4% | 194.1% | 321.8% | 491.2% | 228.6% | 943.0% |
| 1960 | 3 | 12 | 482 | — | — | — | 143.3% | 196.4% | 326.4% | 498.5% | 228.2% | 937.3% |
| 1961 | 3 | 11 | 227 | — | — | — | 141.1% | 195.9% | 327.5% | 500.5% | 224.2% | 920.2% |
| 1962 | 3 | 11 | 662 | — | — | — | 144.0% | 212.1% | 340.6% | 487.6% | 244.6% | 897.1% |
| 1963 | 3 | 12 | 4,336 | — | — | — | 207.9% | 250.9% | 349.4% | 459.1% | 288.1% | 844.5% |
| 1964 | 3 | 11 | 4,047 | — | — | — | 211.4% | 255.6% | 356.3% | 468.5% | 291.1% | 845.6% |
| 1965 | 3 | 10 | 2,813 | — | — | — | 201.6% | 244.2% | 338.9% | 446.0% | 275.6% | 789.1% |
| 1966 | 3 | 9 | 2,328 | — | — | — | 201.5% | 243.2% | 339.1% | 446.6% | 270.4% | 775.3% |
| 1967 | 3 | 8 | 320 | — | — | — | 172.2% | 212.3% | 306.0% | 406.4% | 282.7% | 732.3% |
| 1968 | 3 | 9 | 1,906 | — | — | — | 183.9% | 241.1% | 305.2% | 380.3% | 269.0% | 664.1% |
| 1969 | 3 | 8 | 1,623 | — | — | — | 189.5% | 247.9% | 315.1% | 393.3% | 273.4% | 673.6% |
| 1970 | 3 | 7 | 402 | — | — | — | 179.3% | 242.5% | 315.5% | 397.5% | 321.4% | 666.0% |
| 1971 | 3 | 8 | 1,978 | — | — | — | 191.8% | 287.9% | 307.2% | 327.9% | 316.5% | 551.4% |
| 1972 | 3 | 8 | 2,189 | — | — | — | 173.5% | 235.4% | 268.6% | 282.5% | 257.1% | 472.7% |
| 1973 | 3 | 7 | 445 | — | — | — | 148.3% | 204.7% | 239.8% | 254.4% | 223.3% | 418.1% |
| 1974 | 3 | 7 | 1,138 | — | — | — | 197.1% | 229.7% | 248.3% | 281.8% | 244.8% | 469.6% |
| 1975 | 3 | 8 | 1,284 | — | — | — | 187.4% | 187.6% | 213.1% | 221.7% | 207.1% | 376.9% |
| 1976 | 3 | 8 | 1,663 | — | — | — | 223.9% | 167.7% | 216.9% | 211.0% | 181.7% | 358.5% |
| 1977 | 3 | 8 | 1,057 | — | — | — | 164.6% | 151.5% | 194.9% | 184.6% | 166.6% | 315.6% |
| 1978 | 3 | 8 | 1,669 | — | — | — | 154.2% | 141.6% | 187.8% | 176.1% | 154.0% | 302.8% |
| 1979 | 3 | 8 | 1,141 | — | — | — | 126.6% | 130.7% | 163.8% | 147.5% | 141.4% | 253.1% |
| 1980 | 3 | 8 | 498 | — | — | — | 99.9% | 107.1% | 129.6% | 126.5% | 121.1% | 220.4% |
| 1981 | 3 | 8 | 2,172 | — | — | — | 66.0% | 113.8% | 122.4% | 118.9% | 126.2% | 207.0% |
| 1982 | 3 | 7 | 243 | — | — | — | 50.2% | 92.1% | 104.7% | 104.3% | 108.9% | 223.5% |
| 1983 | 3 | 9 | 363 | — | — | — | 80.9% | 82.5% | 97.8% | 106.7% | 95.1% | 192.9% |
| 1984 | 3 | 9 | 77 | — | — | — | 71.9% | 84.8% | 88.6% | 95.6% | 116.9% | 208.4% |
| 1985 | 3 | 11 | 586 | — | — | — | 80.2% | 105.4% | 89.8% | 114.9% | 124.0% | 226.2% |
| 1986 | 3 | 11 | 453 | — | — | — | 58.6% | 89.7% | 77.0% | 98.0% | 107.3% | 192.3% |
| 1987 | 3 | 11 | 63 | — | — | — | 65.6% | 72.0% | 65.0% | 110.2% | 85.1% | 228.4% |
| 1988 | 3 | 12 | 318 | — | — | — | 73.2% | 62.4% | 54.4% | 111.0% | 74.7% | 239.1% |
| 1989 | 3 | 14 | 509 | — | — | — | 56.2% | 45.9% | 37.4% | 129.9% | 62.8% | 299.4% |
| 1990 | 3 | 13 | 645 | — | — | — | 60.3% | 49.3% | 39.9% | 136.6% | 64.9% | 306.4% |
| 1991 | 3 | 13 | 1,302 | — | — | — | 50.4% | 47.6% | 35.6% | 137.8% | 57.0% | 286.9% |
| 1992 | 3 | 12 | 522 | — | — | — | 42.8% | 42.6% | 32.7% | 132.9% | 55.8% | 289.9% |
| 1993 | 3 | 12 | 588 | — | — | — | 39.7% | 35.6% | 26.9% | 137.2% | 48.0% | 304.4% |
| 1994 | 3 | 11 | 539 | — | — | — | 41.3% | 37.0% | 28.1% | 142.7% | 47.6% | 307.7% |
| 1995 | 3 | 11 | 133 | — | — | — | 23.5% | 32.8% | 24.0% | 145.7% | 44.4% | 314.8% |
| 1996 | 3 | 11 | 6 | — | — | — | 14.4% | 30.3% | 24.1% | 156.0% | 42.2% | 337.2% |
| 1997 | 3 | 16 | 191 | — | — | — | 30.6% | 20.2% | 26.7% | 267.4% | 30.5% | 646.9% |
| 1998 | 3 | 18 | 1,141 | — | — | — | 22.2% | 13.5% | 27.3% | 305.2% | 23.0% | 659.7% |
| 1999 | 3 | 18 | 48 | — | — | — | 7.1% | 10.2% | 20.4% | 272.1% | 17.9% | 681.6% |
| **2000** | **3** | **19** | **104** | **—** | **—** | **—** | **0.0%** | **6.4%** | **21.3%** | **307.1%** | **14.6%** | **655.6%** |
| 2001 | 3 | 18 | 242 | — | — | — | 0.0% | 7.1% | 22.2% | 312.4% | 20.5% | 650.8% |
| 2002 | 3 | 25 | 1,395 | — | — | — | 44.4% | 34.0% | 62.3% | 442.9% | 17.0% | 745.8% |
| 2003 | 3 | 28 | 1,456 | — | — | — | 43.9% | 49.4% | 105.0% | 407.7% | 45.6% | 1140.6% |
| 2004 | 3 | 28 | 2,287 | — | — | — | 27.8% | 38.8% | 112.4% | 448.0% | 44.1% | 1557.9% |
| 2005 | 3 | 27 | 605 | — | — | — | 18.5% | 32.1% | 102.8% | 634.1% | 62.3% | 1366.8% |
| 2006 | 3 | 29 | 523 | — | — | — | 32.8% | 58.0% | 145.0% | 593.9% | 54.7% | 1383.7% |
| 2007 | 3 | 29 | 1,041 | — | — | — | 46.3% | 63.5% | 157.5% | 607.7% | 48.3% | 1284.6% |
| 2008 | 3 | 27 | 998 | — | — | — | 38.3% | 64.0% | 156.5% | 597.9% | 56.8% | 1342.8% |
| 2009 | 3 | 26 | 815 | — | — | — | 37.3% | 64.2% | 158.2% | 602.0% | 54.3% | 1241.3% |
| 2010 | 3 | 26 | 919 | — | — | — | 50.5% | 69.1% | 170.6% | 461.3% | 48.1% | 1256.7% |
| 2011 | 3 | 25 | 1,152 | — | — | — | 53.7% | 72.3% | 176.5% | 576.1% | 48.5% | 1263.8% |
| 2012 | 3 | 24 | 747 | — | — | — | 50.3% | 70.4% | 174.9% | 591.1% | 45.0% | 1227.8% |
| 2013 | 3 | 25 | 877 | — | — | — | 44.5% | 104.2% | 211.9% | 495.2% | 82.8% | 1299.6% |
| 2014 | 3 | 24 | 120 | — | — | — | 37.2% | 97.5% | 202.5% | 539.2% | 89.8% | 1291.0% |
| 2015 | 3 | 25 | 1,774 | — | — | — | 92.3% | 130.5% | 258.6% | 591.7% | 85.4% | 1251.7% |
| 2016 | 3 | 24 | 419 | — | — | — | 81.1% | 120.8% | 244.7% | 561.0% | 123.8% | 1271.7% |
| 2017 | 3 | 24 | 2,653 | — | — | — | 88.8% | 126.6% | 273.5% | 521.9% | 125.5% | 1302.8% |
| 2018 | 3 | 22 | 289 | — | — | — | 79.9% | 122.1% | 249.5% | 579.6% | 131.0% | 1344.4% |
| 2019 | 3 | 22 | 2,017 | — | — | — | 89.6% | 128.1% | 278.3% | 562.3% | 156.2% | 1317.2% |

*Active scenario shown in bold. Coverage fractions = Step-5 remainder / annual expenditure, averaged over each window. Zero in failure years drags the average. LRR failure: buffer exhausted (lrr_bal = 0). SRR failure: refund guarantee broken (srr_bal = 0). Gap: years between LRR and SRR failure. SSM = correlated-shock floor; TCM = heterogeneous-tier ceiling.*

## B.5 Statistical Pass — P(success) Across Economic Cycles

**Success definition (v8):** LRR fills within the 71-year window AND LRR never fails (lrr_failure_year is None).

### B.5.1 Overall (all 73 start years)

| Metric | Value |
|---|---|
| Success rate | 100.0% (73/73) |
| LRR fills | 100.0% (73/73) |
| LRR failures | 0.0% (0/73) |
| SRR failures | 0.0% (0/73) |

### B.5.2 By economic cycle

| Period | N | Success% | LRR fill% |
|---|:---:|:---:|:---:|
| Post-war growth  1947–59 | 13 | 100.0% | 100.0% |
| Long boom        1960–79 | 20 | 100.0% | 100.0% |
| Liberalisation   1980–99 | 20 | 100.0% | 100.0% |
| Crisis decade    2000–19 | 20 | 100.0% | 100.0% |

### B.5.3 Key metric distributions

| Metric | N | Min | Median | Mean | Max |
|---|:---:|---:|---:|---:|---:|
| LRR breakeven year | 73 | 7 | 13 | 15 | 29 |
| SRR fill year | 73 | 3 | 3 | 3 | 3 |
| LRR failure year | 0 | — | — | — | — |
| SRR failure year | 0 | — | — | — | — |
| LRR→SRR failure gap (yrs) | 0 | — | — | — | — |
| LRR surplus at breakeven (£b) | 73 | 6 | 919 | 1,198 | 4,336 |
| SSM coverage 5yr avg | 73 | 0.0% | 86.5% | 97.4% | 223.9% |
| TCM coverage 5yr avg | 73 | 5.5% | 93.5% | 106.8% | 239.0% |
| SSM coverage 10yr avg | 73 | 6.4% | 122.1% | 126.0% | 287.9% |
| TCM coverage 10yr avg | 73 | 14.6% | 125.5% | 138.8% | 321.4% |
| SSM coverage 20yr avg | 73 | 20.4% | 202.5% | 198.4% | 402.6% |
| TCM coverage 20yr avg | 73 | 35.7% | 233.7% | 234.9% | 515.7% |
| SSM coverage 50yr avg | 73 | 95.6% | 442.9% | 386.2% | 656.3% |
| TCM coverage 50yr avg | 73 | 192.3% | 775.3% | 810.4% | 1557.9% |

*Coverage fractions: Step-5 remainder / annual expenditure, averaged over each window length. Zero in any failure year. SSM = correlated-shock floor; TCM = heterogeneous-tier ceiling.*
