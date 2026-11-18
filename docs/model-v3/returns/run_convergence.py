"""Q6: toy convergence test for the recommended generator (AR(1), normal innovations, fitted on the UK record). python3 -I run_convergence.py"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, json
from common import *
from generators import *
D = load(); ys, r = real(D, "capital_tr"); ends = segments(ys)
m_, phi, se = fit_ar1(r, ends)
Ns = [100, 300, 1000, 3000, 10000, 30000, 100000]; seeds = [1, 2, 3, 4, 5]
stats = ["mean100", "p10_30", "mean_30", "p90_30"]
res = {N: {s: [] for s in stats} for N in Ns}
for N in Ns:
    for sd_ in seeds:
        X = sim_ar1(m_, phi, se, N, 100, np.random.default_rng(sd_))
        a30 = X[:, :30].mean(1)
        res[N]["mean100"].append(100 * X.mean()); res[N]["p10_30"].append(100 * np.percentile(a30, 10)); res[N]["mean_30"].append(100 * a30.mean()); res[N]["p90_30"].append(100 * np.percentile(a30, 90))
table = []
for N in Ns:
    row = dict(N=N)
    for s in stats: v = np.array(res[N][s]); row[s + "_mid"] = float(v.mean()); row[s + "_range"] = float(v.max() - v.min())
    row["settled"] = bool(max(row[s + "_range"] for s in stats) <= 0.1); table.append(row)
settle = next((t["N"] for t in table if t["settled"] and all(u["settled"] for u in table if u["N"] >= t["N"])), None)
json.dump(dict(params=dict(mean=m_, phi=phi, se=se), table=table, settle=settle), open("convergence_out.json", "w"), indent=1)
print("params", m_, phi, se)
for t in table: print(t["N"], {k: round(v, 3) if isinstance(v, float) else v for k, v in t.items() if k != "N"})
print("first N from which all four statistics sit within 0.1 point across five seeds:", settle)
