"""Second method for brief 036r: pure Python (no numpy) on the original JSTdatasetR6.xlsx, then the recommended generator against it.
Run: python3 -I check.py"""
import os, math, random, json, openpyxl
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DATA = os.path.join(ROOT, 'docs', 'model-v3', 'returns')   # outputs stay here until 163c
ws = openpyxl.load_workbook(os.path.join(ROOT, "data/rates", "JSTdatasetR6.xlsx"), read_only=True, data_only=True)["Sheet1"]
it = ws.iter_rows(values_only=True); h = list(next(it)); ix = {k: i for i, k in enumerate(h)}
cap, cpi = {}, {}
for row in it:
    if row[ix["iso"]] == "GBR":
        y = row[ix["year"]]
        if row[ix["capital_tr"]] is not None: cap[y] = row[ix["capital_tr"]]
        if row[ix["cpi"]] is not None: cpi[y] = row[ix["cpi"]]
ys = [y for y in sorted(cap) if y in cpi and y - 1 in cpi]
r = [(1 + cap[y]) / (cpi[y] / cpi[y - 1]) - 1 for y in ys]
n = len(r); mean = sum(r) / n; sd = math.sqrt(sum((x - mean) ** 2 for x in r) / (n - 1))
geo = math.exp(sum(math.log1p(x) for x in r) / n) - 1
rho = sum((r[i] - mean) * (r[i + 1] - mean) for i in range(n - 1)) / sum((x - mean) ** 2 for x in r)
main = json.load(open(os.path.join(DATA, "level2_out.json")))
assert n == 117 and (ys[0], ys[-1]) == (1896, 2019)
assert abs(mean - main["mean"]) < 5e-4 and abs(sd - main["sd"]) < 5e-4 and abs(rho - main["rho1"]) < 5e-3   # within 0.05 point
print(f"xlsx, pure Python: n={n} mean={100*mean:.3f}% geo={100*geo:.3f}% sd={100*sd:.3f}% rho1={rho:.3f}")
# the recommended generator, simulated without numpy: AR(1), normal innovations, marginal sd = sample sd
phi = json.load(open(os.path.join(DATA, "convergence_out.json")))["params"]["phi"]; se = sd * math.sqrt(1 - phi * phi)
random.seed(36); P = 4000; tot = 0.0; tot2 = 0.0; cnt = 0
for _ in range(P):
    x = random.gauss(0, sd)
    for t in range(100):
        x = phi * x + random.gauss(0, se); tot += mean + x; tot2 += x * x; cnt += 1
sim_mean = tot / cnt; sim_sd = math.sqrt(tot2 / cnt)
print(f"simulated AR(1): mean={100*sim_mean:.3f}% sd={100*sim_sd:.3f}%")
assert abs(sim_mean - mean) < 5e-4 and abs(sim_sd - sd) < 5e-4
print("both within 0.05 point of the sample: ok")
