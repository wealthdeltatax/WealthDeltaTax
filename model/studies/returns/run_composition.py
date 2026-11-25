"""Q4: JST wealth-return construction as seen in the data, and a payer mix. python3 -I run_composition.py"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, json, openpyxl
from common import *
D = load(); out = {}
ys, cap = real(D, "capital_tr"); cap = dict(zip(ys, cap))
yk, rk = real(D, "risky_tr"); yk = dict(zip(yk, rk)); ysf, sf = real(D, "safe_tr"); sf = dict(zip(ysf, sf))
ye, eq = real(D, "eq_tr"); eq = dict(zip(ye, eq)); yh, hs = real(D, "housing_tr"); hs = dict(zip(yh, hs))
yb, bd = real(D, "bond_tr"); bd = dict(zip(yb, bd)); ybl, bl = real(D, "bill_rate"); bl = dict(zip(ybl, bl))
# implied weights
def implied(lo, hi):
    w = [(cap[y] - sf[y]) / (yk[y] - sf[y]) for y in range(lo, hi + 1) if y in cap and y in yk and y in sf and abs(yk[y] - sf[y]) > 0.03]
    v = [(yk[y] - hs[y]) / (eq[y] - hs[y]) for y in range(lo, hi + 1) if y in yk and y in eq and y in hs and abs(eq[y] - hs[y]) > 0.03]
    return dict(risky_w_median=float(np.median(w)), risky_n=len(w), equity_in_risky_median=float(np.median(v)), eq_n=len(v))
out["implied_weights"] = {f"{a}-{b}": implied(a, b) for a, b in [(1896, 1913), (1919, 1939), (1947, 1969), (1970, 1989), (1990, 2019)]}
# series stats on a common sample 1896-2019 and 1950-2019
def st(d, lo, hi):
    x = np.array([d[y] for y in sorted(d) if lo <= y <= hi]); return dict(n=len(x), mean=float(x.mean()), geo=float(gm(x)), sd=float(x.std(ddof=1)))
out["series"] = {}
for lab, d in [("capital_tr (JST wealth)", cap), ("risky_tr", yk), ("safe_tr", sf), ("equity", eq), ("housing", hs), ("bonds", bd), ("bills", bl)]:
    out["series"][lab] = {"1896-2019": st(d, 1896, 2019), "1950-2019": st(d, 1950, 2019)}
common = [y for y in sorted(cap) if y in eq and y in hs and y in bd and y in bl]
mat = np.array([[eq[y], hs[y], bd[y], bl[y]] for y in common]); out["corr_common"] = np.corrcoef(mat.T).round(3).tolist(); out["corr_labels"] = ["equity", "housing", "bonds", "bills"]; out["corr_n"] = len(common)
# Round 8 composition by decile group (Table 2.2, column K), the shares used for the payer mix
wb = openpyxl.load_workbook(os.path.join(ROOT, "data/rates", "totalwealthtables.xlsx"), data_only=True); ws = wb["Table 2.2"]
col = lambda base: [ws.cell(base + k, 11).value for k in range(10)]
TOT, PROP, FIN, PHY, PEN = col(4), col(14), col(24), col(34), col(44)
G = {"D4-5": [3, 4], "D6-7": [5, 6], "D8-9": [7, 8], "D10": [9]}
sh = {}
for g, ix in G.items():
    t = sum(TOT[i] for i in ix); sh[g] = dict(property=sum(PROP[i] for i in ix) / t, financial=sum(FIN[i] for i in ix) / t, physical=sum(PHY[i] for i in ix) / t, pension=sum(PEN[i] for i in ix) / t)
out["round8_shares"] = sh
# mixes (J): property -> JST housing; financial -> 60% equity 40% bonds-and-bills average; pension -> JST wealth return; physical -> 0% real
def mix(g, fin_eq=0.6, phys=0.0):
    w = sh[g]; yrs = [y for y in common]
    ret = []
    for y in yrs:
        safe = 0.5 * bd[y] + 0.5 * bl[y]
        ret.append(w["property"] * hs[y] + w["financial"] * (fin_eq * eq[y] + (1 - fin_eq) * safe) + w["pension"] * cap[y] + w["physical"] * phys)
    ret = np.array(ret); tot = w["property"] + w["financial"] + w["pension"] + w["physical"]
    return ret / tot   # renormalise (shares of the four classes sum to 1 in Table 2.2)
out["mixes"] = {}
for g in G:
    for lab, fe in [("financial 60% equity", 0.6), ("financial 30% equity", 0.3), ("financial 90% equity", 0.9)]:
        x = mix(g, fe); out["mixes"][f"{g}, {lab}"] = dict(mean=float(x.mean()), geo=float(gm(x)), sd=float(x.std(ddof=1)), n=len(x))
x = np.array([cap[y] for y in common]); out["mixes"]["JST wealth return, same years"] = dict(mean=float(x.mean()), geo=float(gm(x)), sd=float(x.std(ddof=1)), n=len(x))
json.dump(out, open("composition_out.json", "w"), indent=1)
print(json.dumps({k: out[k] for k in ("implied_weights", "round8_shares", "mixes", "corr_n", "corr_common")}, indent=1)); print(json.dumps(out["series"], indent=0)[:1500])
