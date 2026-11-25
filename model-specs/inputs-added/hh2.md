# Model v3 added inputs: non-payer share by income decile (brief 028r)

Research file for brief 028r; the guru merges it into `inputs.md`. Row format as in 012r. UK only. No value is chosen for the model. Everything is derived from one held table (WAS Round 8, Table 2.6); the method and script are at the end.

## Where the request is answered
| Request | Rows | Status |
|---|---|---|
| Share of adults below W_min = £150,000 by income decile (014g 12, wealth-based reading; O4a) | I-H2a1 to I-H2a10 (income deciles of households, lowest to highest) | Met with limits: the joint distribution of income decile and wealth exists in WAS Table 2.6 as three percentile points per decile; deciles are of households, not adults; three rows are only bracketed |
| W_min at £100,000 and £200,000 | Sensitivity table below | Met, same limits |

## Joint-distribution route
Route stated: ONS Wealth and Assets Survey Round 8 (April 2020 to March 2022), Table 2.6, "Distribution of household total wealth, by total household net equivalised income deciles", gives the 25th, 50th and 75th percentile of household total wealth in each income decile (about 2.7 million households per decile, 1,350 to 2,050 sample households). That is the joint distribution. No other source was found: ONS ad hoc 12451 (FYE 2019, `householdsnotax.xlsx`) could not be fetched (URL not on the allowlist) and in any case measures households paying no income tax, not wealth below W_min; no IFS or Resolution Foundation table of wealth by income decile was found in one search.

## Gaps and conflicts
- **Households, not adults.** Table 2.6 deciles are of households by net equivalised income. The brief asks for deciles of all adults. The shares are therefore shares of households. Adults per household by income decile is not in any held file (the ETB workbook has none), so the W_min test is applied to household wealth with three thresholds: £150,000 (every household one adult), £241,721 (central, 1.61 times W_min, the GB average that gives the adult share in I-D4c), £300,000 (every household two adults). The central threshold is one number for all deciles; low-income deciles probably have more single-adult households and high-income deciles more couples, so the central understates the spread. I did not interpolate to adult deciles.
- **Three percentile points only.** Where a threshold falls inside the 25th to 75th percentile range the share is interpolated in a straight line, as in B1. Where it falls outside, the data say only "below 25%" or "above 75%": the low or high is then the bracket end (0 or 25, 75 or 100), and the central a two-piece lognormal fit. Those cells are marked **(J)** and rated low.
- **Cross-check.** The mean of the ten central shares at £150,000 is 43.9% of households; I-D4b gives 45.1% non-payers (54.9% at or above W_min) by adult. The 1.2 point difference is the household against adult weighting, and the bracketed deciles.
- **Price base.** Wealth is 2020-22 pounds against a W_min set at the 2025 median house price (I-D4b made the same choice). Deflating W_min to 2020-22 prices would lower it and so lower every share; the £100,000 column is of that order but is a W_min sensitivity, not a deflation.
- **Round 8 breaks.** Income questions were cut when interviewing moved to telephone (table note 5) and note 6 marks a break in the series at April 2020; pension valuation also changed between Rounds 7 and 8 (012r gotcha, not in this table's notes). Income deciles are net equivalised, not the gross income of I-D9a to I-D9d.
- **Lowest income deciles are asset-rich.** Decile 1 has a median wealth of £132,000 and a 75th percentile of £376,600 (retirees, the self-employed with low reported income), so about 52 to 67% of the lowest income decile is below W_min, not nearly all of it. This is the data, not an error.

## Rows
| ID | Input (feeds) | Unit | Low | Central | High | How the range was set | Source | Licence and access | Coverage | In repo | Confidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| I-H2a1 | Share of households in income decile 1 (lowest) with total wealth below W_min = £150,000, the non-payers (O4a, M4a, M4b; 028r) | % of households in the decile | 51.8 | 61.2 | 67.2 | Published quartiles: wealth 25th, 50th, 75th percentile points £17,200, £132,000, £376,600 (decile 1, 2020-22); share found by straight-line interpolation between them. Low: threshold £150,000 (every household counted as one adult). Central: £241,721 (1.61 times W_min, the GB average of I-D4c; decile mix of single and couple households not known). High: £300,000 (every household two adults). | SN1 Table 2.6; SN3 | OGL v3.0 | GB, April 2020 to March 2022; households by net equivalised income decile, not adults. Outside UK: none | `data/rates/totalwealthtables.xlsx` Table 2.6 | medium: published quartiles, interpolated within range; household not adult weights |
| I-H2a2 | Share of households in income decile 2 with total wealth below W_min = £150,000, the non-payers (O4a, M4a, M4b; 028r) | % of households in the decile | 54.5 | 64.8 | 71.4 | Published quartiles: wealth 25th, 50th, 75th percentile points £21,000, £109,800, £332,500 (decile 2, 2020-22); share found by straight-line interpolation between them. Low: threshold £150,000 (every household counted as one adult). Central: £241,721 (1.61 times W_min, the GB average of I-D4c; decile mix of single and couple households not known). High: £300,000 (every household two adults). | SN1 Table 2.6; SN3 | OGL v3.0 | GB, April 2020 to March 2022; households by net equivalised income decile, not adults. Outside UK: none | `data/rates/totalwealthtables.xlsx` Table 2.6 | medium: published quartiles, interpolated within range; household not adult weights |
| I-H2a3 | Share of households in income decile 3 with total wealth below W_min = £150,000, the non-payers (O4a, M4a, M4b; 028r) | % of households in the decile | 52.8 | 62.4 | 68.5 | Published quartiles: wealth 25th, 50th, 75th percentile points £31,500, £122,800, £361,700 (decile 3, 2020-22); share found by straight-line interpolation between them. Low: threshold £150,000 (every household counted as one adult). Central: £241,721 (1.61 times W_min, the GB average of I-D4c; decile mix of single and couple households not known). High: £300,000 (every household two adults). | SN1 Table 2.6; SN3 | OGL v3.0 | GB, April 2020 to March 2022; households by net equivalised income decile, not adults. Outside UK: none | `data/rates/totalwealthtables.xlsx` Table 2.6 | medium: published quartiles, interpolated within range; household not adult weights |
| I-H2a4 | Share of households in income decile 4 with total wealth below W_min = £150,000, the non-payers (O4a, M4a, M4b; 028r) | % of households in the decile | 48.8 | 58.7 | 64.6 | Published quartiles: wealth 25th, 50th, 75th percentile points £41,800, £155,600, £402,500 (decile 4, 2020-22); share found by straight-line interpolation between them. Low: threshold £150,000 (every household counted as one adult). Central: £241,721 (1.61 times W_min, the GB average of I-D4c; decile mix of single and couple households not known). High: £300,000 (every household two adults). | SN1 Table 2.6; SN3 | OGL v3.0 | GB, April 2020 to March 2022; households by net equivalised income decile, not adults. Outside UK: none | `data/rates/totalwealthtables.xlsx` Table 2.6 | medium: published quartiles, interpolated within range; household not adult weights |
| I-H2a5 | Share of households in income decile 5 with total wealth below W_min = £150,000, the non-payers (O4a, M4a, M4b; 028r) | % of households in the decile | 38.3 | 50.4 | 55.5 | Published quartiles: wealth 25th, 50th, 75th percentile points £51,000, £236,500, £522,800 (decile 5, 2020-22); share found by straight-line interpolation between them. Low: threshold £150,000 (every household counted as one adult). Central: £241,721 (1.61 times W_min, the GB average of I-D4c; decile mix of single and couple households not known). High: £300,000 (every household two adults). | SN1 Table 2.6; SN3 | OGL v3.0 | GB, April 2020 to March 2022; households by net equivalised income decile, not adults. Outside UK: none | `data/rates/totalwealthtables.xlsx` Table 2.6 | medium: published quartiles, interpolated within range; household not adult weights |
| I-H2a6 | Share of households in income decile 6 with total wealth below W_min = £150,000, the non-payers (O4a, M4a, M4b; 028r) | % of households in the decile | 35.5 | 47.9 | 53.6 | Published quartiles: wealth 25th, 50th, 75th percentile points £72,200, £257,200, £552,700 (decile 6, 2020-22); share found by straight-line interpolation between them. Low: threshold £150,000 (every household counted as one adult). Central: £241,721 (1.61 times W_min, the GB average of I-D4c; decile mix of single and couple households not known). High: £300,000 (every household two adults). | SN1 Table 2.6; SN3 | OGL v3.0 | GB, April 2020 to March 2022; households by net equivalised income decile, not adults. Outside UK: none | `data/rates/totalwealthtables.xlsx` Table 2.6 | medium: published quartiles, interpolated within range; household not adult weights |
| I-H2a7 | Share of households in income decile 7 with total wealth below W_min = £150,000, the non-payers (O4a, M4a, M4b; 028r) | % of households in the decile | 26.9 | 36.1 | 42.0 | Published quartiles: wealth 25th, 50th, 75th percentile points £130,900, £379,400, £676,400 (decile 7, 2020-22); share found by straight-line interpolation between them. Low: threshold £150,000 (every household counted as one adult). Central: £241,721 (1.61 times W_min, the GB average of I-D4c; decile mix of single and couple households not known). High: £300,000 (every household two adults). | SN1 Table 2.6; SN3 | OGL v3.0 | GB, April 2020 to March 2022; households by net equivalised income decile, not adults. Outside UK: none | `data/rates/totalwealthtables.xlsx` Table 2.6 | medium: published quartiles, interpolated within range; household not adult weights |
| I-H2a8 | Share of households in income decile 8 with total wealth below W_min = £150,000, the non-payers (O4a, M4a, M4b; 028r) | % of households in the decile | 0.0 | 27.5 | 32.8 | Published quartiles: wealth 25th, 50th, 75th percentile points £213,500, £491,600, £869,900 (decile 8, 2020-22); share found by straight-line interpolation between them. Low: threshold £150,000 (every household counted as one adult). Central: £241,721 (1.61 times W_min, the GB average of I-D4c; decile mix of single and couple households not known). High: £300,000 (every household two adults). **(J)** low: £150,000 is below the 25th percentile point (£213,500), so the share is only known to lie between 0 and 25, and the lower end is used. | SN1 Table 2.6; SN3 | OGL v3.0 | GB, April 2020 to March 2022; households by net equivalised income decile, not adults. Outside UK: none | `data/rates/totalwealthtables.xlsx` Table 2.6 | low: bracket, not interpolated |
| I-H2a9 | Share of households in income decile 9 with total wealth below W_min = £150,000, the non-payers (O4a, M4a, M4b; 028r) | % of households in the decile | 0.0 | 19.9 | 25.7 | Published quartiles: wealth 25th, 50th, 75th percentile points £291,500, £615,100, £1,092,200 (decile 9, 2020-22); share found by straight-line interpolation between them. Low: threshold £150,000 (every household counted as one adult). Central: £241,721 (1.61 times W_min, the GB average of I-D4c; decile mix of single and couple households not known). High: £300,000 (every household two adults). **(J)** low: £150,000 is below the 25th percentile point (£291,500), so the share is only known to lie between 0 and 25, and the lower end is used; central: £241,721 is outside the quartile range (25th percentile £291,500), so the central is a two-piece lognormal fit through the three points. | SN1 Table 2.6; SN3 | OGL v3.0 | GB, April 2020 to March 2022; households by net equivalised income decile, not adults. Outside UK: none | `data/rates/totalwealthtables.xlsx` Table 2.6 | low: bracket, not interpolated |
| I-H2a10 | Share of households in income decile 10 (highest) with total wealth below W_min = £150,000, the non-payers (O4a, M4a, M4b; 028r) | % of households in the decile | 0.0 | 9.9 | 25.0 | Published quartiles: wealth 25th, 50th, 75th percentile points £459,900, £932,200, £1,645,400 (decile 10, 2020-22); share found by straight-line interpolation between them. Low: threshold £150,000 (every household counted as one adult). Central: £241,721 (1.61 times W_min, the GB average of I-D4c; decile mix of single and couple households not known). High: £300,000 (every household two adults). **(J)** low: £150,000 is below the 25th percentile point (£459,900), so the share is only known to lie between 0 and 25, and the lower end is used; central: £241,721 is outside the quartile range (25th percentile £459,900), so the central is a two-piece lognormal fit through the three points; high: £300,000 is below the quartile range, so the share is only bracketed (0 to 25) and the upper end is used. | SN1 Table 2.6; SN3 | OGL v3.0 | GB, April 2020 to March 2022; households by net equivalised income decile, not adults. Outside UK: none | `data/rates/totalwealthtables.xlsx` Table 2.6 | low: bracket, not interpolated |

## Sensitivity to W_min
Share of households below W_min (low / central / high), same method; "(bracket)" means at least one of the three cells is a quartile bracket, not an interpolation. At £200,000 the high threshold of £400,000 lies above the 75th percentile in the three lowest deciles, so the high is 100 there (no information). Moving W_min from £150,000 to £100,000 lowers the equal-weight mean central share from 43.9% to 35.2%; to £200,000 raises it to 51.6%. Deciles 1 to 6 are the most sensitive.

| Income decile | W_min £100,000 (low / central / high) | W_min £150,000 | W_min £200,000 |
|---|---|---|---|
| 1 | 43.0 / 53.0 / 57.0 | 51.8 / 61.2 / 67.2 | 57.0 / 69.4 / 100.0 (bracket) |
| 2 | 47.2 / 55.7 / 60.1 | 54.5 / 64.8 / 71.4 | 60.1 / 73.8 / 100.0 (bracket) |
| 3 | 43.8 / 54.0 / 58.1 | 52.8 / 62.4 / 68.5 | 58.1 / 70.8 / 100.0 (bracket) |
| 4 | 37.8 / 50.5 / 54.5 | 48.8 / 58.7 / 64.6 | 54.5 / 66.8 / 74.7 |
| 5 | 31.6 / 39.8 / 45.1 | 38.3 / 50.4 / 55.5 | 45.1 / 57.5 / 64.3 |
| 6 | 28.8 / 37.0 / 42.3 | 35.5 / 47.9 / 53.6 | 42.3 / 55.5 / 62.1 |
| 7 | 0.0 / 28.0 / 32.0 (bracket) | 26.9 / 36.1 / 42.0 | 32.0 / 44.2 / 51.7 |
| 8 | 0.0 / 18.3 / 25.0 (bracket) | 0.0 / 27.5 / 32.8 (bracket) | 0.0 / 34.8 / 41.8 (bracket) |
| 9 | 0.0 / 11.3 / 25.0 (bracket) | 0.0 / 19.9 / 25.7 (bracket) | 0.0 / 27.4 / 33.4 (bracket) |
| 10 | 0.0 / 4.7 / 25.0 (bracket) | 0.0 / 9.9 / 25.0 (bracket) | 0.0 / 15.5 / 25.0 (bracket) |
| Mean of deciles (equal weight) | 23.2 / 35.2 / 42.4 | 30.9 / 43.9 / 50.6 | 34.9 / 51.6 / 65.3 |

## Judgement rows
I-H2a8, I-H2a9, I-H2a10 (three rows with bracket cells). The other seven are published percentile points interpolated; the household-for-adult substitution and the central threshold multiplier are judgement in all ten rows, and are stated in each row.

## Sources (accessed 2026-11-17)
| ID | Source | Accessed | Licence and access |
|---|---|---|---|
| SN1 | ONS, Household total wealth in Great Britain: April 2020 to March 2022, Table 2.6 (published 24 Jan 2025), held as `data/rates/totalwealthtables.xlsx` | 2026-11-17 | Open Government Licence v3.0 |
| SN2 | ONS ad hoc 12451, Proportion of UK households paying no income tax and direct taxes, FYE 2019 (4 Nov 2020); not read, fetch refused (URL not on the allowlist) | 2026-11-17 | Open Government Licence v3.0 |
| SN3 | `model-specs/inputs.md` rows I-D4b (W_min £150,000; adult share 54.9%) and I-D4c (household threshold 1.61 times W_min) | 2026-11-17 | repository |

## Method and script
Run with `python -I script.py "data/rates/totalwealthtables.xlsx"`. It reads the last column (April 2020 to March 2022) of Table 2.6, prints the shares for W_min 100,000, 150,000 and 200,000, and a re-read of the decile 1 median.

```python
import openpyxl, math, sys
from statistics import NormalDist
N=NormalDist(); z=0.6744897501960817
ws=openpyxl.load_workbook(sys.argv[1],data_only=True)['Table 2.6']
rows=[[c for c in r if c is not None] for r in ws.iter_rows(values_only=True)]
q={}
for blk,p in ((3,25),(14,50),(25,75)):            # first data rows (0-based index of header row +1)
    pass
vals=[r[-1] for r in rows]  # last column = Apr 2020 to Mar 2022
P25=[rows[i][-1] for i in range(3,13)]; P50=[rows[i][-1] for i in range(14,24)]; P75=[rows[i][-1] for i in range(25,35)]
W=[rows[i][-1] for i in range(47,57)]
def F(d,T):
    a,b,c=P25[d],P50[d],P75[d]
    if a<=T<=b: return (.25+.25*(T-a)/(b-a),)*2
    if b<T<=c: return (.5+.25*(T-b)/(c-b),)*2
    if T<a: return (0.0,.25)
    return (.75,1.0)
def ln(d,T):   # two-piece lognormal, central only
    mu=math.log(P50[d]); s=((mu-math.log(P25[d]))/z if T<P50[d] else (math.log(P75[d])-mu)/z)
    return N.cdf((math.log(T)-mu)/s)
M=1.61  # I-D4c: household threshold = 1.61 x W_min
def row(d,Wmin):
    lo=F(d,Wmin)[0]; hi=F(d,2*Wmin)[1]
    Tc=M*Wmin; f=F(d,Tc); ce=f[0] if f[0]==f[1] else ln(d,Tc)
    return 100*lo,100*ce,100*hi,(F(d,Wmin)[0]!=F(d,Wmin)[1] or f[0]!=f[1] or F(d,2*Wmin)[0]!=F(d,2*Wmin)[1])
for Wm in (100000,150000,200000):
    print("Wmin",Wm)
    tot=[0,0,0]
    for d in range(10):
        l,c,h,br=row(d,Wm); print(" D%-2d %5.1f %5.1f %5.1f %s"%(d+1,l,c,h,"bracket" if br else ""))
        for k,v in enumerate((l,c,h)): tot[k]+=v/10
    print(" mean %.1f %.1f %.1f"%tuple(tot))
print("check P50 D1",P50[0],"weights",set(W))
```
