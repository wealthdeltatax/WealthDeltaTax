# WDT Rates and Revenue — Model Output

**Run date:** 2026-08-31  
**Scenario:** 2007 Balanced  
**Model version:** v7  
**Parameters file:** `260812_WDT_Params.toml`  

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
| LRR breakeven year | 29 |
| Annual expenditure at LRR breakeven (£b) | £3,980b |
| SRR balance at LRR breakeven (£b) | £1,498b |
| LRR surplus at breakeven (£b) | £1,041b |
| LRR first breach year | 35 |
| LRR breach lag (years) | 6 |
| Minimum LRR balance in window (£b) | £-6,333b |
| Capitalisation window (years) | 25 |
| Avg expenditure — capitalisation window (£b/yr) | £2,336.9b |
| **SSM coverage ratio** | **21.3%** |

*SSM coverage ratio: average annual SSM net income over the capitalisation window (SRR fill to LRR breakeven) divided by average annual expenditure over the same window. The SSM applies uniform historical returns across the population (correlated-shock assumption); TCM coverage appears in (RATES.A §B.3).*

## B.3 TCM Results — N=29 periods

### B.3.1 Net worth — start ($V_0$) and year N (£m)

*$V_0$ is the bracket mean wealth (£m) at entry, identical across tiers within a bracket. V_N is the true wealth (before tax settlement) at the end of period N for a representative taxpayer, varying by tier due to persistent return differentials. Figures are for a single representative taxpayer; they do not reflect aggregate portfolio wealth.*

| Net worth (£m) | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ |
|---|---|---|---|---|---|---|---|---|---|---|
| **$V_0$ (start, all tiers)** | £0.402m | £0.570m | £0.782m | £1.109m | £1.629m | £2.858m | £7.135m | £19.854m | £53.385m | £139.607m |
| **V_N -4.55% (Poor)** | £0.54m | £0.77m | £1.05m | £1.49m | £2.19m | £3.85m | £9.60m | £26.71m | £71.82m | £187.83m |
| **V_N -2.05% (Ok)** | £1.10m | £1.56m | £2.14m | £3.03m | £4.46m | £7.82m | £19.52m | £54.33m | £146.08m | £382.01m |
| **V_N +0.95% (Good)** | £2.52m | £3.57m | £4.91m | £6.95m | £10.22m | £17.93m | £44.75m | £124.53m | £334.84m | £875.65m |
| **V_N +3.45% (Great)** | £4.94m | £7.01m | £9.62m | £13.64m | £20.04m | £35.16m | £87.77m | £244.22m | £656.69m | £1,717.31m |

### B.3.2 Net per taxpayer per year — capitalisation window average (£/yr)

*Average annual net tax per representative taxpayer over the capitalisation window (SRR fill year to LRR breakeven year). Zeros suppressed.*

| Tier \ Bracket | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ |
|---|---|---|---|---|---|---|---|---|---|---|
| -4.55% (Poor) | £— | £— | £— | £— | £2,045 | £5,636 | £14,115 | £39,665 | £109,451 | £305,443 |
| -2.05% (Ok) | £— | £— | £— | £4,744 | £10,360 | £21,446 | £53,787 | £151,765 | £423,099 | £1,209,253 |
| +0.95% (Good) | £1,672 | £6,754 | £12,453 | £20,368 | £32,694 | £58,587 | £147,405 | £419,808 | £1,197,675 | £3,595,026 |
| +3.45% (Great) | £11,919 | £19,840 | £29,992 | £44,565 | £66,777 | £116,605 | £294,830 | £851,591 | £2,511,228 | £7,979,372 |

### B.3.3 Annual wealth burden (tax as % of net worth)

| Tier \ Bracket | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ |
|---|---|---|---|---|---|---|---|---|---|---|
| -4.55% (Poor) | 0.00% | 0.00% | 0.00% | 0.00% | 0.10% | 0.15% | 0.15% | 0.15% | 0.16% | 0.17% |
| -2.05% (Ok) | 0.00% | 0.00% | 0.04% | 0.18% | 0.26% | 0.31% | 0.31% | 0.31% | 0.33% | 0.36% |
| +0.95% (Good) | 0.12% | 0.23% | 0.30% | 0.35% | 0.39% | 0.42% | 0.42% | 0.43% | 0.47% | 0.56% |
| +3.45% (Great) | 0.31% | 0.36% | 0.40% | 0.43% | 0.46% | 0.47% | 0.48% | 0.50% | 0.57% | 0.75% |

### B.3.4 Effective rate on gains (tax as % of annual gain)

| Tier \ Bracket | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ |
|---|---|---|---|---|---|---|---|---|---|---|
| -4.55% (Poor) | 0.0% | 0.0% | 0.0% | 0.0% | 2.9% | 4.5% | 4.5% | 4.5% | 4.7% | 5.0% |
| -2.05% (Ok) | 0.0% | 0.0% | 1.1% | 5.3% | 7.7% | 9.2% | 9.3% | 9.4% | 9.8% | 10.9% |
| +0.95% (Good) | 3.5% | 7.0% | 9.1% | 10.6% | 11.8% | 12.5% | 12.6% | 13.0% | 14.0% | 16.7% |
| +3.45% (Great) | 9.2% | 10.8% | 12.1% | 13.0% | 13.8% | 14.1% | 14.4% | 15.1% | 17.1% | 22.4% |

### B.3.5 Average annual net tax per taxpayer — lifetime average (£/yr)

| Tier \ Bracket | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ |
|---|---|---|---|---|---|---|---|---|---|---|
| -4.55% (Poor) | £— | £— | £— | £— | £2,024 | £5,319 | £13,319 | £37,416 | £103,146 | £287,076 |
| -2.05% (Ok) | £— | £— | £773 | £5,041 | £10,292 | £21,000 | £52,670 | £148,629 | £414,423 | £1,184,033 |
| +0.95% (Good) | £2,841 | £7,731 | £13,266 | £21,025 | £33,082 | £59,493 | £149,755 | £427,038 | £1,221,581 | £3,676,976 |
| +3.45% (Great) | £13,714 | £21,809 | £32,057 | £46,864 | £69,476 | £122,020 | £308,933 | £895,554 | £2,659,203 | £8,471,582 |

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
| 10% (Poor) | £— | £— | £— | £— | £707 | £1,560 | £879 | £247 | £68 | £21 | **£3,482.7m** |
| 30% (Ok) | £— | £— | £— | £9,849 | £10,754 | £17,809 | £10,050 | £2,836 | £791 | £251 | **£52,338.1m** |
| 40% (Good) | £4,629 | £18,694 | £34,469 | £56,379 | £45,249 | £64,867 | £36,722 | £10,458 | £2,984 | £995 | **£275,445.4m** |
| 20% (Great) | £16,496 | £27,458 | £41,509 | £61,679 | £46,210 | £64,553 | £36,724 | £10,607 | £3,128 | £1,104 | **£309,468.7m** |
| **Column total** | **£21,125.0m** | **£46,152.1m** | **£75,978.2m** | **£127,906.3m** | **£102,920.3m** | **£148,788.6m** | **£84,374.2m** | **£24,148.3m** | **£6,970.3m** | **£2,371.6m** | **£640,735.0m** |

*Row totals in £b/yr:*

| Tier (weight) | £b/yr |
|---|---|
| 10% (Poor) | £3.48b |
| 30% (Ok) | £52.34b |
| 40% (Good) | £275.45b |
| 20% (Great) | £309.47b |
| **Grand total** | **£640.73b** |

### B.3.8 Cohort proportion of total tax paid (%)

*Each cell's capitalisation-window revenue as a percentage of the grand total. Row total is the tier's share; column total is the bracket's share across all tiers.*

| Tier (weight) \ Bracket | 50% | 60% | 70% | 80% | 90% | 95% | 99% | 99.9% | 99.99% | 99.99%+ | **Row total** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 10% (Poor) | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.2% | 0.1% | 0.0% | 0.0% | 0.0% | **0.5%** |
| 30% (Ok) | 0.0% | 0.0% | 0.0% | 1.5% | 1.7% | 2.8% | 1.6% | 0.4% | 0.1% | 0.0% | **8.2%** |
| 40% (Good) | 0.7% | 2.9% | 5.4% | 8.8% | 7.1% | 10.1% | 5.7% | 1.6% | 0.5% | 0.2% | **43.0%** |
| 20% (Great) | 2.6% | 4.3% | 6.5% | 9.6% | 7.2% | 10.1% | 5.7% | 1.7% | 0.5% | 0.2% | **48.3%** |
| **Column total** | **3.3%** | **7.2%** | **11.9%** | **20.0%** | **16.1%** | **23.2%** | **13.2%** | **3.8%** | **1.1%** | **0.4%** | **100.0%** |

### B.3.9 Revenue by tier (£b/yr)

| Tier | Lifetime avg (£b/yr) | Capitalisation window avg (£b/yr) |
|---|---|---|
| -4.55% (Poor) | £3.3b | £3.5b |
| -2.05% (Ok) | £53.8b | £52.3b |
| +0.95% (Good) | £287.8b | £275.4b |
| +3.45% (Great) | £328.1b | £309.5b |
| **Total** | **£673.1b** | **£640.7b** |

*TCM horizon N is derived from the SSM LRR breakeven year, not the TOML snapshot_N.*

**TCM coverage ratio:**

| Metric | Value |
|---|---|
| Avg revenue — capitalisation window (£b/yr) | £640.7b |
| Avg expenditure — capitalisation window (£b/yr) | £2,336.9b |
| Capitalisation window (years) | 25 |
| **TCM coverage ratio** | **27.4%** |

*TCM coverage ratio: average annual TCM revenue over the capitalisation window divided by average annual expenditure over the same window. The TCM applies heterogeneous tier differentials to the actual historical return series, producing higher revenue than the SSM's uniform-return assumption. The SSM coverage ratio (solvency/stress-test perspective) appears in (RATES.A §B.2).*


## B.4 Start-Year Sweep

All figures at $\tau_0$=15%, $\tau_m$=70%, k=0.001, $W_{min}$=£2.0m.

### B.4.1 Extremals — three dimensions

| Dimension | Start year | LRR breakeven | LRR surplus (£b) | LRR breach lag | Peak LRR deficit (£b) |
|---|---|---|---|---|---|
| Speed — slowest LRR breakeven | 2006 | 29 | £523b | 5 years | £-9,139b |
| Speed — fastest LRR breakeven | 1970 | 7 | £402b | no breach | £0b |
| Safety — thinnest surplus | 1996 | 11 | £6b | 4 years | £-64,851b |
| Safety — largest surplus | 1963 | 12 | £4,336b | no breach | £0b |
| Durability — shortest breach lag | 2000 | 19 | £104b | 3 years | £-52,429b |
| Durability — longest breach lag | 1970 | 7 | £402b | no breach | £0b |

*41 start years produce no LRR breach within the 71-year modelling window.*

### B.4.2 Full sweep table (all 73 calendar years)

| Start | SRR fill | LRR breakeven | LRR surplus (£b) | SRR at breakeven (£b) | LRR breach | Breach lag | Peak LRR deficit (£b) | SRR breach | SRR deficit (£b) | LRR at SRR breach (£b) | SRR breach covered | SSM coverage | TCM coverage |
|:---:|:---:|:---:|---:|---:|:---:|:---:|---:|:---:|---:|---:|:---:|---:|---:|
| 1947 | 3 | 21 | 1,934 | 1,721 | — | — | 0 | 61 | 77,564 | 1,734,108 | YES | 25.5% | 31.3% |
| 1948 | 3 | 20 | 2,454 | 1,850 | — | — | 0 | 60 | 76,197 | 1,753,102 | YES | 28.4% | 33.3% |
| 1949 | 3 | 18 | 152 | 1,500 | — | — | 0 | 59 | 74,492 | 1,764,594 | YES | 25.0% | 29.6% |
| 1950 | 3 | 18 | 2,153 | 1,901 | — | — | 0 | 58 | 68,594 | 1,692,959 | YES | 30.8% | 35.7% |
| 1951 | 3 | 17 | 2,126 | 1,963 | — | — | 0 | 57 | 64,885 | 1,662,643 | YES | 32.2% | 36.8% |
| 1952 | 3 | 16 | 2,274 | 2,078 | — | — | 0 | 56 | 62,629 | 1,664,778 | YES | 33.5% | 38.2% |
| 1953 | 3 | 15 | 1,115 | 1,889 | — | — | 0 | 55 | 53,880 | 1,515,837 | YES | 31.6% | 36.3% |
| 1954 | 3 | 17 | 3,266 | 2,207 | — | — | 0 | 54 | 43,723 | 1,322,578 | YES | 37.1% | 38.0% |
| 1955 | 3 | 16 | 3,113 | 2,271 | — | — | 0 | 53 | 40,260 | 1,283,865 | YES | 39.9% | 38.8% |
| 1956 | 3 | 15 | 2,704 | 2,286 | — | — | 0 | 52 | 37,213 | 1,256,768 | YES | 39.3% | 38.4% |
| 1957 | 3 | 14 | 2,681 | 2,411 | — | — | 0 | 51 | 34,694 | 1,242,379 | YES | 39.7% | 38.2% |
| 1958 | 3 | 13 | 360 | 1,877 | — | — | 0 | 50 | 25,959 | 1,032,518 | YES | 28.8% | 33.2% |
| 1959 | 3 | 13 | 586 | 1,944 | — | — | 0 | 49 | 18,878 | 845,983 | YES | 38.7% | 41.5% |
| 1960 | 3 | 12 | 482 | 2,041 | — | — | 0 | 48 | 16,739 | 823,703 | YES | 41.5% | 43.8% |
| 1961 | 3 | 11 | 227 | 2,109 | — | — | 0 | 47 | 14,432 | 792,626 | YES | 43.6% | 44.4% |
| 1962 | 3 | 11 | 662 | 2,272 | — | — | 0 | 46 | 11,358 | 722,735 | YES | 53.7% | 55.8% |
| 1963 | 3 | 12 | 4,336 | 3,326 | — | — | 0 | 45 | 8,444 | 649,330 | YES | 48.8% | 51.8% |
| 1964 | 3 | 11 | 4,047 | 3,541 | — | — | 0 | 44 | 6,831 | 636,275 | YES | 54.6% | 56.5% |
| 1965 | 3 | 10 | 2,813 | 3,419 | — | — | 0 | 43 | 4,586 | 575,700 | YES | 51.6% | 51.9% |
| 1966 | 3 | 9 | 2,328 | 3,635 | — | — | 0 | 42 | 2,971 | 552,108 | YES | 51.5% | 51.3% |
| 1967 | 3 | 8 | 320 | 3,029 | — | — | 0 | 41 | 1,020 | 474,542 | YES | 48.2% | 49.6% |
| 1968 | 3 | 9 | 1,906 | 3,424 | — | — | 0 | — | 0 | — | — | 80.4% | 80.2% |
| 1969 | 3 | 8 | 1,623 | 3,811 | — | — | 0 | — | 0 | — | — | 85.9% | 84.5% |
| 1970 | 3 | 7 | 402 | 3,694 | — | — | 0 | — | 0 | — | — | 80.4% | 89.3% |
| 1971 | 3 | 8 | 1,978 | 4,024 | — | — | 0 | — | 0 | — | — | 92.8% | 93.3% |
| 1972 | 3 | 8 | 2,189 | 4,150 | — | — | 0 | — | 0 | — | — | 103.4% | 105.2% |
| 1973 | 3 | 7 | 445 | 3,727 | — | — | 0 | — | 0 | — | — | 86.9% | 86.0% |
| 1974 | 3 | 7 | 1,138 | 4,247 | — | — | 0 | — | 0 | — | — | 130.5% | 134.5% |
| 1975 | 3 | 8 | 1,284 | 3,607 | — | — | 0 | — | 0 | — | — | 90.2% | 91.4% |
| 1976 | 3 | 8 | 1,663 | 3,835 | — | — | 0 | — | 0 | — | — | 97.5% | 100.4% |
| 1977 | 3 | 8 | 1,057 | 3,471 | — | — | 0 | — | 0 | — | — | 87.9% | 90.2% |
| 1978 | 3 | 8 | 1,669 | 3,839 | — | — | 0 | — | 0 | — | — | 85.4% | 87.8% |
| 1979 | 3 | 8 | 1,141 | 3,521 | — | — | 0 | — | 0 | — | — | 90.1% | 91.0% |
| 1980 | 3 | 8 | 498 | 3,136 | — | — | 0 | — | 0 | — | — | 74.8% | 79.6% |
| 1981 | 3 | 8 | 2,172 | 4,140 | — | — | 0 | — | 0 | — | — | 92.8% | 94.0% |
| 1982 | 3 | 7 | 243 | 3,575 | 42 | 35 | -13,035 | — | 0 | — | — | 85.9% | 82.8% |
| 1983 | 3 | 9 | 363 | 2,652 | 39 | 30 | -24,319 | — | 0 | — | — | 73.4% | 75.5% |
| 1984 | 3 | 9 | 77 | 2,509 | 36 | 27 | -35,169 | — | 0 | — | — | 59.4% | 61.5% |
| 1985 | 3 | 11 | 586 | 2,244 | 33 | 22 | -39,333 | — | 0 | — | — | 53.7% | 57.8% |
| 1986 | 3 | 11 | 453 | 2,194 | 25 | 14 | -48,594 | — | 0 | — | — | 42.4% | 46.0% |
| 1987 | 3 | 11 | 63 | 2,048 | 22 | 11 | -53,007 | — | 0 | — | — | 40.4% | 43.8% |
| 1988 | 3 | 12 | 318 | 1,986 | 21 | 9 | -64,382 | — | 0 | — | — | 49.1% | 52.7% |
| 1989 | 3 | 14 | 509 | 1,819 | 20 | 6 | -76,943 | — | 0 | — | — | 33.5% | 37.1% |
| 1990 | 3 | 13 | 645 | 1,962 | 19 | 6 | -68,921 | — | 0 | — | — | 36.9% | 40.3% |
| 1991 | 3 | 13 | 1,302 | 2,159 | 19 | 6 | -67,786 | — | 0 | — | — | 44.1% | 48.8% |
| 1992 | 3 | 12 | 522 | 2,054 | 17 | 5 | -67,930 | 71 | 75,261 | 2,838,385 | YES | 46.1% | 49.0% |
| 1993 | 3 | 12 | 588 | 2,076 | 17 | 5 | -69,711 | 70 | 57,259 | 2,464,401 | YES | 48.1% | 49.6% |
| 1994 | 3 | 11 | 539 | 2,226 | 16 | 5 | -64,044 | 69 | 54,367 | 2,461,654 | YES | 53.1% | 53.7% |
| 1995 | 3 | 11 | 133 | 2,074 | 15 | 4 | -65,815 | 68 | 40,020 | 2,139,957 | YES | 49.0% | 51.7% |
| 1996 | 3 | 11 | 6 | 2,026 | 15 | 4 | -64,851 | 67 | 31,602 | 1,963,419 | YES | 48.1% | 52.6% |
| 1997 | 3 | 16 | 191 | 1,597 | 21 | 5 | -59,722 | 66 | 19,932 | 1,643,781 | YES | 37.6% | 34.1% |
| 1998 | 3 | 18 | 1,141 | 1,698 | 23 | 5 | -56,299 | 65 | 12,583 | 1,437,646 | YES | 35.1% | 35.7% |
| 1999 | 3 | 18 | 48 | 1,480 | 22 | 4 | -58,810 | 64 | 5,905 | 1,205,031 | YES | 32.9% | 34.2% |
| 2000 | 3 | 19 | 104 | 1,460 | 22 | 3 | -52,429 | 63 | 3,103 | 1,135,687 | YES | 33.8% | 31.4% |
| 2001 | 3 | 18 | 242 | 1,518 | 21 | 3 | -49,123 | 62 | 1,347 | 1,110,214 | YES | 33.6% | 30.3% |
| 2002 | 3 | 25 | 1,395 | 1,555 | 31 | 6 | -25,262 | — | 0 | — | — | 24.5% | 27.5% |
| 2003 | 3 | 28 | 1,456 | 1,546 | 34 | 6 | -17,020 | — | 0 | — | — | 19.9% | 24.5% |
| 2004 | 3 | 28 | 2,287 | 1,645 | 33 | 5 | -16,933 | — | 0 | — | — | 20.6% | 26.9% |
| 2005 | 3 | 27 | 605 | 1,442 | 32 | 5 | -19,286 | — | 0 | — | — | 19.0% | 24.0% |
| 2006 | 3 | 29 | 523 | 1,438 | 34 | 5 | -9,139 | — | 0 | — | — | 20.8% | 27.1% |
| **2007** | **3** | **29** | **1,041** | **1,498** | **35** | **6** | **-6,333** | **—** | **0** | **—** | **—** | **21.3%** | **27.7%** |
| 2008 | 3 | 27 | 998 | 1,491 | 34 | 7 | -6,736 | — | 0 | — | — | 22.4% | 28.1% |
| 2009 | 3 | 26 | 815 | 1,471 | 33 | 7 | -6,539 | — | 0 | — | — | 21.9% | 28.4% |
| 2010 | 3 | 26 | 919 | 1,484 | 32 | 6 | -4,589 | 71 | 185,031 | 3,067,036 | YES | 21.8% | 29.0% |
| 2011 | 3 | 25 | 1,152 | 1,522 | 31 | 6 | -3,730 | 70 | 179,559 | 3,035,855 | YES | 22.8% | 29.6% |
| 2012 | 3 | 24 | 747 | 1,475 | 30 | 6 | -4,165 | 69 | 166,111 | 2,878,532 | YES | 22.4% | 28.5% |
| 2013 | 3 | 25 | 877 | 1,484 | — | — | 0 | 68 | 147,433 | 2,636,197 | YES | 22.3% | 28.7% |
| 2014 | 3 | 24 | 120 | 1,385 | 29 | 5 | -17 | 67 | 130,254 | 2,399,534 | YES | 21.1% | 26.7% |
| 2015 | 3 | 25 | 1,774 | 1,607 | — | — | 0 | 66 | 120,197 | 2,284,071 | YES | 22.0% | 28.3% |
| 2016 | 3 | 24 | 419 | 1,428 | — | — | 0 | 65 | 104,456 | 2,053,723 | YES | 20.2% | 26.5% |
| 2017 | 3 | 24 | 2,653 | 1,747 | — | — | 0 | 64 | 92,489 | 1,883,467 | YES | 23.8% | 29.5% |
| 2018 | 3 | 22 | 289 | 1,430 | — | — | 0 | 63 | 92,106 | 1,919,817 | YES | 21.2% | 26.3% |
| 2019 | 3 | 22 | 2,017 | 1,703 | — | — | 0 | 62 | 81,057 | 1,756,079 | YES | 24.7% | 30.2% |

*Active scenario shown in bold. SRR breach covered: LRR balance at SRR breach year ≥ SRR deficit. Peak LRR deficit: worst LRR balance in the 71-year window under the zero-governance assumption. Coverage ratios: capitalisation window averages (SRR fill to LRR breakeven).*

## B.5 Statistical Pass — P(success) Across Economic Cycles

**Success definition:** LRR fills within the 71-year window AND (SRR never breaches OR SRR breach is fully covered by LRR balance at time of breach).

### B.5.2 Overall (all 73 start years)

| Metric | Value |
|---|---|
| Success rate | 100.0% (73/73) |
| LRR fills | 100.0% (73/73) |
| SRR breaches | 56.2% (41/73) |
| — of which covered | 41 |
| — of which uncovered | 0 |
| No SRR breach | 32 |

### B.5.3 By economic cycle

| Period | N | Success% | LRR fill% |
|---|:---:|:---:|:---:|
| Post-war growth  1947–59 | 13 | 100.0% | 100.0% |
| Long boom        1960–79 | 20 | 100.0% | 100.0% |
| Liberalisation   1980–99 | 20 | 100.0% | 100.0% |
| Crisis decade    2000–19 | 20 | 100.0% | 100.0% |

### B.5.4 Key metric distributions

| Metric | N | Min | Median | Mean | Max |
|---|:---:|---:|---:|---:|---:|
| LRR breakeven year | 73 | 7 | 13 | 15 | 29 |
| SRR fill year | 73 | 3 | 3 | 3 | 3 |
| LRR surplus at breakeven (£b) | 73 | 6 | 919 | 1,198 | 4,336 |
| LRR breach lag (yrs) | 32 | 3 | 6 | 9 | 35 |
| Peak LRR deficit (£b) | 73 | -76,943 | 0 | -16,712 | 0 |
| SRR deficit at breach (£b) | 73 | 0 | 4,586 | 32,129 | 185,031 |
| SSM coverage ratio | 73 | 19.0% | 39.7% | 47.0% | 130.5% |
| TCM coverage ratio | 73 | 24.0% | 40.3% | 50.0% | 134.5% |
