# 012r stage B1: derivations

Method and code behind the computed rows in `docs/model-v3/inputs.md` (I-D4b, I-D4c, I-D9a to I-D9h, I-D1a to I-D1e). Inputs come from the held ONS Round 8 tables (`Rates Data/totalwealthtables.xlsx`, `financialwealthtables.xlsx`) and `model_v2/jst_r6.json`. Run each with `python3 -I`; `income_by_wealth.py` imports `wmin_share.py`, so keep them in one folder under the names given. Accessed 2026-11-16.

## 1. Share of adults and of wealth at or above W_min (`wmin_share.py`)
- W_min is half the median house price: £300,000 (England, year to September 2025, ONS) gives £150,000; v2's £112,500 is shown for comparison.
- Household basis: piecewise-linear CDF through the band quartiles of Table 2.5; wealth below a threshold assumes wealth is uniform between quartiles. Total wealth £13,568bn, 26.99m households.
- Adult basis: Table 2.9 household types with an assumed adult count (1, 2 or 3), a lognormal fitted to each type's quartiles, and a household counted as at or above W_min when its wealth is at least W_min times its adults.
- The wealth share for the adult basis uses the household threshold that reproduces the adult share (1.48 times W_min at £112,500, 1.61 times at £150,000).
- Results at £150,000: households 64.3% (wealth 96.4%); adults 54.9% (wealth 92.7%); every household treated as two adults, households at £300,000: 49.3% (wealth 89.7%). At £112,500: households 68.9% (97.6%); adults 62.5% (95.8%).
- Check: deciles 1 to 3 aggregate £288bn in Table 2.2; the interpolated CDF gives £298bn below the 30th percentile (3% off).

```python
# Share of households / adults / wealth at or above W_min, WAS Round 8 (Apr 2020-Mar 2022), GB.
# Inputs copied from Rates Data/totalwealthtables.xlsx Tables 2.2, 2.5, 2.9 (R8 column).
import math, bisect
from statistics import NormalDist
N = NormalDist()

# Table 2.5: bands (lo, hi), households, p25, p50, p75
bands = [
 (-1e9,   20000, 3132000, 3500,    8300,    14800),
 (20000,  85000, 4237000, 29300,   42900,   63700),
 (85000, 200000, 3650000, 109200,  135900,  165500),
 (200000,300000, 2655000, 224400,  247800,  274000),
 (300000,500000, 4084000, 344200,  396200,  447000),
 (500000,1e6,    5416000, 579700,  681100,  823200),
 (1e6,   1e9,    3816000, 1161200, 1437600, 1938500),
]
TOTAL_H = sum(b[2] for b in bands)
TOTAL_W = 13568e9  # Table 2.1, total wealth incl. private pensions

def cdf_points():
    # piecewise-linear CDF through band quartiles; lowest band lower edge 0
    pts=[]; cum=0
    for lo,hi,h,p25,p50,p75 in bands:
        lo = max(lo,0)
        seg=[(lo,0.0),(p25,0.25),(p50,0.5),(p75,0.75),(hi,1.0)]
        for w,f in seg:
            pts.append((w, (cum + f*h)/TOTAL_H))
        cum += h
    return pts
PTS = cdf_points()
def F(w):
    # share of households with wealth below w
    prev=None
    for x,y in PTS:
        if prev and w<=x:
            x0,y0=prev
            if x==x0: return y
            return y0+(y-y0)*(w-x0)/(x-x0)
        prev=(x,y)
    return 1.0
def wealth_below(w):
    # wealth held by households below w; piecewise-uniform within each quartile segment
    tot=0.0; prev=None; cum_h=0
    for lo,hi,h,p25,p50,p75 in bands:
        lo=max(lo,0)
        edges=[lo,p25,p50,p75,hi]; fr=[.25,.25,.25,.25]
        for i in range(4):
            a,b=edges[i],edges[i+1]
            if w<=a: break
            top=min(b,w)
            frac=(top-a)/(b-a) if b>a else 1
            hh=h*fr[i]*frac
            tot+=hh*(a+top)/2
        else:
            continue
        break
    return tot
# Table 2.9 household types: (households, adults assumed, p25, p50, p75)
types = {
 'Single over SPA':      (3724000,1,  76000, 291800, 591300),
 'Single under SPA':     (4506000,1,  20500, 117300, 365800),
 'Couple both over SPA': (2408000,2, 360400, 661600,1125400),
 'Couple both under SPA':(3471000,2, 148000, 398100, 835800),
 'Couple 1 over/1 under':( 706000,2, 368400, 711300,1150800),
 'Couple dep children':  (5646000,2,  93800, 291500, 600900),
 'Couple non-dep child': (2044000,3, 301400, 647900,1116900),
 'Lone parent dep':      (1562000,1,  14900,  35200, 155700),
 'Lone parent non-dep':  (1516000,2,  29700, 145100, 466700),
 '2+ / other':           (1408000,3,  68700, 235200, 581200),
}
def p_above_type(p25,p50,p75,thr):
    mu=math.log(p50); sig=(math.log(p75)-math.log(p25))/(2*0.6744897501960817)
    return 1-N.cdf((math.log(thr)-mu)/sig)
def adults_share(wmin, adult_shift=0):
    num=den=0
    for h,a,p25,p50,p75 in types.values():
        a2=a+adult_shift if a>=2 else a
        num+=h*a2*p_above_type(p25,p50,p75,wmin*a2)
        den+=h*a2
    return num/den, den
if __name__=="__main__":
    print("households (m):",TOTAL_H/1e6, " adults implied (m):",adults_share(1)[1]/1e6)
    # check F on decile aggregates: wealth below the 30th percentile threshold
    print("deciles 1-3 aggregate (Table 2.2, £bn):", (13897+78424+195622)/1e3)
    p30=None
    for w in range(0,400000,500):
        if F(w)>=0.30: p30=w;break
    print("household p30 (interp):",p30," wealth below, interp £bn:",round(wealth_below(p30)/1e9,1))
    for wmin in (112500,150000):
        print("\nW_min =",wmin)
        hh=1-F(wmin)
        print(" household basis: share of households >= W_min: %.1f%%; wealth share: %.1f%%"%(100*hh,100*(1-wealth_below(wmin)/TOTAL_W)))
        sa,_=adults_share(wmin)
        print(" per-adult (type-weighted lognormal): share of adults >= W_min: %.1f%%"%(100*sa))
        # equivalent household threshold k_eff such that household-basis share equals the adult share
        lo,hi=wmin,wmin*3
        for _ in range(60):
            mid=(lo+hi)/2
            if 1-F(mid)>sa: lo=mid
            else: hi=mid
        k=lo/wmin
        print("   equivalent household threshold = %.2f x W_min (£%d)"%(k,lo))
        print("   wealth share at that threshold: %.1f%%"%(100*(1-wealth_below(lo)/TOTAL_W)))
        for k2 in (2.0,):
            print("   k=2 bound: households >= %d: %.1f%%; wealth %.1f%%"%(k2*wmin,100*(1-F(k2*wmin)),100*(1-wealth_below(k2*wmin)/TOTAL_W)))
        # adult-count sensitivity: multi-adult types +/-1 adult... (non-dep and 2+ types only)
```

## 2. Income by wealth band (`income_by_wealth.py`)
- Table 2.6 gives wealth quartiles for each net equivalised income decile. For each income decile I fitted a lognormal to the quartiles and computed the share of each wealth decile's households in each income decile, then weighted decile mean gross incomes.
- Income decile means are an interpolation (judgement) anchored to ONS FYE 2024 means: all households £55,200, poorest fifth £18,100, richest fifth £120,000. The central set (£16,000 to £155,000) averages £55,000, £18,000 and £120,000 on those cuts. Two alternative shapes (steep and flat in deciles 9 and 10) moved results by under 2%.
- Output (central, £ per year): wealth D4 46,255; D5 54,256; D6 60,568; D7 65,508; D8 69,652; D9 73,345; D10 71,413. Bands in the register average the pairs.
- Limits: the mapping is from net equivalised to gross household income; wealth deciles are household-based; income independence within wealth deciles is assumed through the lognormal fit.

```python
import math, sys
from statistics import NormalDist
N=NormalDist()
sys.path.insert(0,".")
import wmin_share as W   # national CDF PTS, F()
# Table 2.6 (R8): wealth quartiles by net equivalised income decile
t26=[(17200,132000,376600),(21000,109800,332500),(31500,122800,361700),(41800,155600,402500),(51000,236500,522800),
     (72200,257200,552700),(130900,379400,676400),(213500,491600,869900),(291500,615100,1092200),(459900,932200,1645400)]
def cdf_d(d,w):
    p25,p50,p75=t26[d]; mu=math.log(p50); s=(math.log(p75)-math.log(p25))/(2*0.6744897501960817)
    return N.cdf((math.log(max(w,1.0))-mu)/s)
# wealth decile bounds from the national CDF (household basis)
def inv_F(q):
    lo,hi=0.0,5e6
    for _ in range(80):
        m=(lo+hi)/2
        if W.F(m)<q: lo=m
        else: hi=m
    return lo
bounds=[0.0]+[inv_F(q/10) for q in range(1,10)]+[1e9]
incomes={ # mean gross household income by income decile, £; judgement (see note)
 'central':[16000,20000,26000,32000,41000,49000,57000,69000,85000,155000],
 'steep':  [16000,20000,26000,32000,41000,49000,57000,69000,70000,170000],
 'flat':   [16000,20000,26000,32000,41000,49000,57000,69000,95000,145000]}
print("wealth decile bounds (£):",[round(b/1000) for b in bounds[1:-1]])
for name,inc in incomes.items():
    print("\n",name)
    for k in range(3,10):
        a,b=bounds[k],bounds[k+1]
        pd=[(cdf_d(d,b)-cdf_d(d,a))*0.1 for d in range(10)]
        tot=sum(pd); pd=[x/tot for x in pd]
        e=sum(p*i for p,i in zip(pd,inc))
        print("  wealth decile %d: £%.0fk-%.0fk  E[income] £%.0f   P(top2 income deciles)=%.2f"%(k+1,a/1e3,min(b,9e6)/1e3,e,pd[8]+pd[9]))
```

## 3. Net financial wealth share by band (`liquid_proxy.py`)
Net financial wealth over total wealth for decile pairs, Table 2.2, Rounds 6, 7, 8. Results: D4 to 5 5.6, 6.5, 6.6%; D6 to 7 8.5, 8.4, 9.3%; D8 to 9 10.4, 10.8, 12.8%; D10 21.5, 17.1, 19.3%. Round 8 top-10% share of total wealth from the same table: £5,523bn of £13,568bn, 40.7% (Round 7: 43.5%).

```python
# Net financial wealth / total wealth by total-wealth decile band, WAS Rounds 6 (2016-18), 7 (2018-20), 8 (2020-22).
# Source: Rates Data/totalwealthtables.xlsx Table 2.2 (total wealth block and net financial wealth block).
import openpyxl
wb=openpyxl.load_workbook("/home/claude/wealthdeltatax/Rates Data/totalwealthtables.xlsx",read_only=True,data_only=True)
rows=[[c for c in r if c is not None] for r in wb['Table 2.2'].iter_rows(values_only=True)]
blocks={}; cur=None
for r in rows:
    if not r: continue
    s0=str(r[0])
    if s0.startswith('Aggregate total wealth'): cur='tot'
    elif s0.startswith('Aggregate financial wealth'): cur='fin'
    elif s0.startswith(('Aggregate property','Aggregate physical','Aggregate private','Unweighted','Weighted')): cur=None
    if not cur: continue
    # first decile row: r[0] is the block header, r[1] is the decile label; later rows: r[0] is the label
    if s0.startswith('Aggregate'):
        if len(r)>1 and 'Decile' in str(r[1]): blocks.setdefault(cur,[]).append([float(x) for x in r[2:]])
    elif 'Decile' in s0:
        blocks.setdefault(cur,[]).append([float(x) for x in r[1:]])
print({k:len(v) for k,v in blocks.items()})
bands={'D4-5':[3,4],'D6-7':[5,6],'D8-9':[7,8],'D10':[9]}
waves={'R6 2016-18':6,'R7 2018-20':7,'R8 2020-22':8}
for b,idx in bands.items():
    out=[]
    for w,j in waves.items():
        f=sum(blocks['fin'][i][j] for i in idx); t=sum(blocks['tot'][i][j] for i in idx)
        out.append((w,100*f/t))
    print(b,[ "%s %.1f%%"%o for o in out], "mean fin/hh £k (R8):", round(sum(blocks['fin'][i][8] for i in idx)/(2.7*len(idx))/1e3,1))
```

## 4. UK real returns (`uk_returns.py`)
Real return = (1 + nominal total return) divided by CPI growth, minus 1, from JST R6. Loss year: real return below zero. Rolling windows: 30 years. Results for "capital_tr" (117 years, 1896 to 2019):
- 1871-2020: arithmetic mean 4.74%, geometric 4.42%, SD 8.2%, loss years 28.2% (33), longest run 6 (to 1949), 30-year geometric P10 2.18%, P90 7.47%.
- 1950-2019: 5.82%, 5.56%, SD 7.3%, loss 22.9% (16), run 3 (to 1957).
- 1980-2019: 6.96%, 6.76%, SD 6.5%, loss 15.0% (6), run 1 (to 1981).
- Equities (1871-2020): geometric 5.32%, SD 17.6%, loss 28.0%. Housing (1871-2020): 5.01%, SD 8.9%, loss 26.3%. Bonds 1.75%; safe assets 1.46%. Risky series SD 9.8%.
- Excluding the war years (1914-19, 1939-45) the capital_tr arithmetic mean is 5.37%, loss frequency 24.5%.

```python
import json, math, statistics as st
d=json.load(open("/home/claude/wealthdeltatax/model_v2/jst_r6.json"))
u=d['countries']['GBR']; yrs=u['years']; S=u['series']
cpi=S['cpi']
def real(name):
    out={}
    for i,y in enumerate(yrs):
        if i==0: continue
        r=S[name][i]; c0=cpi[i-1]; c1=cpi[i]
        if r is None or c0 is None or c1 is None: continue
        out[y]=(1+r)/(c1/c0)-1
    return out
def pct(xs,p):
    xs=sorted(xs); k=(len(xs)-1)*p; f=math.floor(k); c=min(f+1,len(xs)-1)
    return xs[f]+(xs[c]-xs[f])*(k-f)
def longest_run(vals_by_year):
    best=cur=0; best_end=None
    for y in sorted(vals_by_year):
        if vals_by_year[y]<0:
            cur+=1
            if cur>best: best=cur; best_end=y
        else: cur=0
    return best,best_end
def geo(xs): return math.exp(sum(math.log(1+x) for x in xs)/len(xs))-1
def stats(name,lo=None,hi=None):
    r=real(name)
    r={y:v for y,v in r.items() if (lo is None or y>=lo) and (hi is None or y<=hi)}
    ys=sorted(r); xs=[r[y] for y in ys]
    loss=sum(1 for x in xs if x<0)
    run,end=longest_run(r)
    # rolling 30y geometric mean
    roll=[geo(xs[i:i+30]) for i in range(len(xs)-29)]
    return dict(n=len(xs),first=ys[0],last=ys[-1],mean=st.mean(xs),geo=geo(xs),sd=st.pstdev(xs),
        loss_freq=loss/len(xs),loss_n=loss,run=run,run_end=end,worst=min(xs),worst_y=ys[xs.index(min(xs))],
        best=max(xs),roll_n=len(roll),roll_p10=pct(roll,.10) if roll else None,roll_p90=pct(roll,.90) if roll else None,
        roll_min=min(roll) if roll else None,roll_max=max(roll) if roll else None)
def fmt(s):
    return ("n=%d %d-%d mean %.2f%% geo %.2f%% sd %.1f%% loss %.1f%% (%d yrs) longest run %d (to %s) worst %.1f%% (%d) best %.1f%% | 30y roll P10 %.2f%% P90 %.2f%% min %.2f%% max %.2f%% (n=%d)"%(
        s['n'],s['first'],s['last'],100*s['mean'],100*s['geo'],100*s['sd'],100*s['loss_freq'],s['loss_n'],s['run'],s['run_end'],100*s['worst'],s['worst_y'],100*s['best'],
        100*(s['roll_p10'] or float('nan')),100*(s['roll_p90'] or float('nan')),100*(s['roll_min'] or float('nan')),100*(s['roll_max'] or float('nan')),s['roll_n']))
print("UK series span", yrs[0], yrs[-1])
for nm in ['capital_tr','risky_tr','safe_tr','eq_tr','housing_tr','bond_tr']:
    present=sum(1 for v in S[nm] if v is not None)
    print("\n",nm,"non-null",present)
    for lab,lo,hi in [("1871-2020",None,None),("1950-2020",1950,None),("1980-2020",1980,None),("ex-wars 1871-1913,1920-38,1946-2020",None,None)]:
        if lab.startswith("ex-wars"):
            r=real(nm); r={y:v for y,v in r.items() if not (1914<=y<=1919 or 1939<=y<=1945)}
            ys=sorted(r); xs=[r[y] for y in ys]
            print(" ",lab,"mean %.2f%% sd %.1f%% loss %.1f%% n=%d"%(100*st.mean(xs),100*st.pstdev(xs),100*sum(x<0 for x in xs)/len(xs),len(xs)))
            continue
        print(" ",lab, fmt(stats(nm,lo,hi)))
# last year with data
for nm in ['capital_tr','eq_tr','housing_tr','cpi']:
    ys=[y for y,v in zip(yrs,S[nm]) if v is not None]; print(nm,"last non-null year",ys[-1])
```

## Addendum 2026-11-21 (brief 106c): I-D4b refitted with the I-D4h adult count
- The script in section 1 reproduces the old central exactly (54.9% of adults, wealth 92.7%, at £150,000; 62.5% and 95.8% at £112,500). Its assumed counts (1, 2, 3 per household type) imply 47.642m adults over 26.991m households, 1.765 per household; I-D4h (Tables 2.9 and 2.11, persons 16 and over) gives 1.93.
- Refit: every assumed count is multiplied by one factor, 1.93 / 1.7651 = 1.0934 (counts 1.093, 2.187, 3.280; no household type added), so the household-weighted mean is 1.93. In `adults_share`, `a2 = a * 1.0934` for every type (the old function shifted only the 2 and 3 types, with `adult_shift`, and left 1 alone). Everything else is as in section 1.
- Results: £150,000: adults 52.4% (was 54.9%), equivalent household threshold 1.78 times W_min (£267,412; was 1.61), wealth share at that threshold 91.5% (was 92.7%). £112,500: adults 60.2% (was 62.5%), 1.68 times (was 1.48), wealth 95.0% (was 95.8%).
- Sensitivity of the target: 52,043,000 / 26,991,000 = 1.9282 gives 52.4% (52.44); the low 1.86 gives 53.5%.
- I-D4c was not changed by 106c. Its method (wealth above the household threshold that reproduces the adult share) gives the wealth shares above, 91.5% (was 92.7%), inside its bounds 89.7 to 96.4.

## Addendum 2026-11-21 (brief 107c): I-D4c and the rows that quote its threshold
- I-D4c refitted by the 106c result: 91.5% of wealth (was 92.7%) at £150,000, equivalent household threshold 1.78 times W_min (£267,412; was 1.61, £241,721). Bounds 89.7 and 96.4 kept. At £112,500: 95.0% (was 95.8%).
- I-H2a1 to I-H2a10 central threshold £241,721 to £267,412. The old centrals reproduce with the row text's method (linear between the 25th, 50th and 75th percentile points; a two-piece lognormal outside them) except decile 5, which computes 50.5 against the 50.4 printed. New centrals: 63.8, 67.7, 65.1, 61.3, 52.7, 50.9, 38.7, 29.8, 22.6, 11.7. Low (£150,000) and high (£300,000) unchanged.
- I-M6a and I-M6h divide a liability by the I-D4c wealth: central £13,568bn x 91.5% = £12,415bn (was £12,578bn). I-M6a central 7.03 / 12,415 = 0.0566, printed 0.057 (was 0.056); I-M6h 18.15 / 12,415 = 0.1462, printed 0.146 (was 0.144). Their low and high use the I-D4c bounds and the other year's liability, so they are unchanged.
- The I-W6 coverage notes and the 016g line now say about 1.78. Left alone: I-W6 values (household shares, no adult conversion), `tornado.md` lines 54 and 72 (a dated design note quoting 92.7), and the 102r and 103r audit files (history).

