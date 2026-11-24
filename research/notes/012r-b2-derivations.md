# 012r stage B2: derivations for D6 and D10

Accessed 2026-11-16. Method notes for the derived rows in `docs/model-v3/inputs.md` (I-D5b, I-D6a to n, I-D10b). Nothing here is a published incidence.

## D6 allocation method (`d6_incidence.py`)
- Households per income decile are equal. Wealth by income decile comes from WAS Round 8 Table 2.6 quartiles (`Rates Data/totalwealthtables.xlsx`). Within each income decile the wealth distribution is a two-piece lognormal: lower half scaled by the 25th to 50th percentile gap, upper half by the 50th to 75th gap. A single lognormal over-stated the tail (bottom-decile upper quartile is £376,600, so the single fit put 22% of inheritance tax in decile 1).
- Income deciles are the B1 judgement set (£16,000 to £155,000, anchored to S9).
- Council tax: bill proportional to income to the power b; b = 1 + ln(4.8/1.5) / ln(18,000/120,000) = 0.39 from the Resolution Foundation shares (S19). Variants b minus and plus 0.15.
- Business rates and corporation tax: split between owners (wealth above £100,000), workers (income) and consumers (income to the power 0.7). Workers' share 40% from S22 (Germany).
- Capital gains tax: HMRC bands (S20), not wealth, because the wealth proxy contradicted HMRC (it gave the bottom three deciles over 20%; HMRC says income under £37,700 with gains under £50,000 is 3% of gains).
- Inheritance tax, stamp taxes: wealth above a threshold by income decile (thresholds in the rows).
- Check: every vector sums to 100.00 before rounding; the rounded central vectors sum to 99.9 to 100.1.
- Limits: income decile is net equivalised in Table 2.6 but gross household in the incomes; no published decile incidence reached (S23 workbook not retrievable).

## D10 arithmetic
- I-D10a low: 1 / 0.041 = 24.4 (highest implied discount rate in S16).
- I-D10b: 0.0175 x 3,000 x multiple / 6,600: 19.4, 24.2, 26.7 per cent (GDP £3.0tn is an approximation; £6.6tn from S12 produced £2.1tn plus non-produced £4.5tn).
- I-D10c central: 1 - 0.6 = 40 per cent (S17: about £900 of a £1,500 cut reached the buyer).

## Script
```python
import math
from statistics import NormalDist
N=NormalDist()
t26=[(17200,132000,376600),(21000,109800,332500),(31500,122800,361700),(41800,155600,402500),(51000,236500,522800),
     (72200,257200,552700),(130900,379400,676400),(213500,491600,869900),(291500,615100,1092200),(459900,932200,1645400)]
inc=[16000,20000,26000,32000,41000,49000,57000,69000,85000,155000]   # judgement set from B1
z=0.6744897501960817
def fit(d):
    p25,p50,p75=t26[d]; return math.log(p50),(math.log(p75)-math.log(p25))/(2*z)

G=[(i+0.5)/20000 for i in range(20000)]
Q=[N.inv_cdf(u) for u in G]
def wq(d):
    p25,p50,p75=t26[d]; mu=math.log(p50)
    slo=(mu-math.log(p25))/z; sup=(math.log(p75)-mu)/z
    return [math.exp(mu+(slo if q<0 else sup)*q) for q in Q]
WQ=[wq(d) for d in range(10)]
def wealth_above(d,T): return sum(w for w in WQ[d] if w>T)/len(G)
def mean_w(d): return sum(WQ[d])/len(G)
def norm(v): t=sum(v); return [100*x/t for x in v]
out={}
# council tax: bill per household ~ income^b, b calibrated to RF quintile ratio (4.8% vs 1.5% of gross income)
q1=(inc[0]+inc[1])/2; q5=(inc[8]+inc[9])/2   # 18000, 120000 (matches S9 quintile means)
b=1+math.log(4.8/1.5)/math.log(q1/q5)
out['council tax']={'b_central':b}
for name,bb in [('low_top',b-0.15),('central',b),('high_top',b+0.15)]:
    out['council tax '+name]=norm([x**bb for x in inc])
# stamp duty on property: wealth-linked, allocate by total wealth (mean) by income decile; low/high: income-proportional / wealth^1.0
out['SDLT property central']=norm([mean_w(d) for d in range(10)])
out['SDLT property low_top']=norm([x for x in inc])            # proportional to income
out['SDLT property high_top']=norm([wealth_above(d,500000) for d in range(10)])
# stamp tax on shares: wealth above 500k as proxy for large share holders
out['stamp shares central']=norm([wealth_above(d,500000) for d in range(10)])
out['stamp shares low_top']=norm([mean_w(d) for d in range(10)])
out['stamp shares high_top']=norm([wealth_above(d,1000000) for d in range(10)])
# CGT: wealth above 1m central; 500k low-top, 2m high-top
for n,T in [('low_top',500000),('central',1000000),('high_top',2000000)]:
    out['CGT '+n]=norm([wealth_above(d,T) for d in range(10)])
# IHT: wealth above 1m central (couple's nil-rate); 500k low; 2m high
for n,T in [('low_top',500000),('central',1000000),('high_top',2000000)]:
    out['IHT '+n]=norm([wealth_above(d,T) for d in range(10)])
# corporation tax: shareholders s_cap (wealth above 100k proxy? use mean wealth), workers s_lab (gross income), consumers rest (income^0.7 spending proxy)
cap=norm([wealth_above(d,100000) for d in range(10)]); lab=norm(inc); con=norm([x**0.7 for x in inc])
for n,(sc,sl) in [('low_top',(0.3,0.6)),('central',(0.5,0.4)),('high_top',(0.8,0.1))]:
    sh=1-sc-sl
    out['corp tax '+n]=[sc*c+sl*l+sh*k for c,l,k in zip(cap,lab,con)]
# business rates: proxy = same split, central only, labour 40 consumers 40 shareholders 20? -> use mix of income, spending, capital
for n,(sc,sl) in [('low_top',(0.1,0.3)),('central',(0.3,0.3)),('high_top',(0.6,0.2))]:
    sh=1-sc-sl
    out['business rates '+n]=[sc*c+sl*l+sh*k for c,l,k in zip(cap,lab,con)]
for k,v in out.items():
    if k=='council tax': print(k,v); continue
    print("%-28s sum=%.2f  "%(k,sum(v))+" ".join("%5.1f"%x for x in v))

print("\n--- CGT from HMRC bands ---")
def cgt(A,C):
    B=100-A-C
    wc=[wealth_above(d,500000) for d in range(6)]; wc=[100*x/sum(wc) for x in wc]
    bi=[57000,69000,85000]; bi=[100*x/sum(bi) for x in bi]
    return [C*x/100 for x in wc]+[B*x/100 for x in bi]+[A]
for n,(A,C) in [('low_top',(52,6)),('central',(55,4)),('high_top',(55,3))]:
    v=cgt(A,C); out['CGT '+n]=v
    print("CGT",n,"sum=%.2f "%sum(v)," ".join("%5.1f"%x for x in v))
print("\n--- summary: D10 share, deciles 1-5 share, deciles 1-3 share ---")
for t in ['council tax','SDLT property','stamp shares','CGT','IHT','corp tax','business rates']:
    for n in ['low_top','central','high_top']:
        v=out[t+' '+n]; print("%-14s %-9s D10 %5.1f  D1-5 %5.1f  D1-3 %5.1f  sum %.2f"%(t,n,v[9],sum(v[:5]),sum(v[:3]),sum(v)))

print("\n--- ranges: (min, central, max) ---")
for t in ['council tax','business rates','corp tax','CGT','IHT','SDLT property','stamp shares']:
    vs=[out[t+' '+n] for n in ['low_top','central','high_top']]
    d10=[v[9] for v in vs]; b5=[sum(v[:5]) for v in vs]
    print("%-14s D10 %.1f / %.1f / %.1f   D1-5 %.1f / %.1f / %.1f"%(t,min(d10),vs[1][9],max(d10),min(b5),sum(vs[1][:5]),max(b5)))
print("\n--- central vectors rounded 1dp ---")
for t in ['council tax','business rates','corp tax','CGT','IHT','SDLT property','stamp shares']:
    v=[round(x,1) for x in out[t+' central']]; print("%-14s"%t,v,"sum=%.1f"%sum(v))
```
