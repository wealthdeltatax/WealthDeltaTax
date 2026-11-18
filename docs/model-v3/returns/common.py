"""Shared loader for brief 036r. Reads model_v2/jst_r6.json (UK). Run scripts with python3 -I."""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
def load():
    d = json.load(open(os.path.join(ROOT, "model_v2", "jst_r6.json")))["countries"]["GBR"]
    yrs = d["years"]; S = d["series"]
    ser = lambda v: {y: x for y, x in zip(yrs, S[v]) if x is not None}
    return {v: ser(v) for v in ("capital_tr", "risky_tr", "safe_tr", "eq_tr", "housing_tr", "bond_tr", "bill_rate", "cpi")}
def real(D, var, y0=1871, y1=2020):
    """Real return (1+r)/(cpi_t/cpi_t-1)-1 for years where var and both CPIs exist. Returns (years, array)."""
    c = D["cpi"]; v = D[var]
    ys = [y for y in sorted(v) if y0 <= y <= y1 and y in c and y - 1 in c]
    return np.array(ys), np.array([(1 + v[y]) / (c[y] / c[y - 1]) - 1 for y in ys])
def gm(x): return np.exp(np.log1p(x).mean()) - 1
def segments(ys):
    """Index of the last observation of each contiguous calendar segment (seams: gap years)."""
    ends = np.zeros(len(ys), bool); ends[-1] = True
    ends[:-1] = np.diff(ys) != 1
    return ends
def acf(x, k):
    x = x - x.mean(); return float((x[:-k] * x[k:]).sum() / (x * x).sum())
def longest_run(neg):
    best = cur = 0
    for b in neg:
        cur = cur + 1 if b else 0; best = max(best, cur)
    return best
