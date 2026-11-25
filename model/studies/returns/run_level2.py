"""Q3: level 2 uncertainty of the true mean, sd and lag-1 autocorrelation; break test. python3 -I run_level2.py"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, json
from common import *
from generators import *
D = load(); ys, r = real(D, "capital_tr"); ends = segments(ys); n = len(r)
rng = np.random.default_rng(37); out = {}
mu, sd = r.mean(), r.std(ddof=1); rho = acf(r, 1)
out["n"] = n; out["mean"] = mu; out["sd"] = sd; out["rho1"] = rho
out["se_naive"] = sd / np.sqrt(n)
out["inflation_ar1"] = float(np.sqrt((1 + rho) / (1 - rho))); out["se_ar1"] = out["se_naive"] * out["inflation_ar1"]
out["n_eff"] = n * (1 - rho) / (1 + rho)
def hac_se(x, lag=2):
    x = x - x.mean(); g0 = (x * x).mean(); s = g0
    for k in range(1, lag + 1): s += 2 * (1 - k / (lag + 1)) * (x[:-k] * x[k:]).mean()
    return float(np.sqrt(s / len(x)))
out["se_hac_nw2"] = hac_se(r)
# stationary bootstrap of the sample mean, sd and rho (block 3), seam-respecting
B = 20000; X = sim_stationary_bootstrap(r, ends, 3, B, n, rng)
bm = X.mean(1); bs = X.std(ddof=1, axis=1)
bphi = np.array([np.corrcoef(x[:-1], x[1:])[0, 1] for x in X[:4000]])
q = lambda a, p: [float(v) for v in np.percentile(a, p)]
out["boot_mean_p"] = dict(zip(["2.5", "10", "50", "90", "97.5"], q(bm, [2.5, 10, 50, 90, 97.5])))
out["boot_sd_p"] = dict(zip(["2.5", "10", "50", "90", "97.5"], q(bs, [2.5, 10, 50, 90, 97.5])))
out["boot_rho_p"] = dict(zip(["2.5", "10", "50", "90", "97.5"], q(bphi, [2.5, 10, 50, 90, 97.5])))
out["boot_se_mean"] = float(bm.std())
# sample cases
def cut(lab, m): sub = r[m]; return dict(n=int(m.sum()), mean=float(sub.mean()), geo=float(gm(sub)), sd=float(sub.std(ddof=1)), loss=float((sub < 0).mean()))
out["subs"] = {"1896-1949": cut("a", ys <= 1949), "1950-2019": cut("b", ys >= 1950), "1980-2019": cut("c", ys >= 1980), "1896-1979": cut("d", ys < 1980),
               "all": cut("e", ys > 0), "excluding 1914-18 and 1939": cut("f", ~(((ys >= 1914) & (ys <= 1918)) | (ys == 1939)))}
# break tests: HAC t for mean shift at each candidate year (15% trim); null by AR(1) parametric bootstrap
def sup_t(x, yrs):
    best = 0; arg = None; m = len(x)
    for i in range(int(0.15 * m), int(0.85 * m)):
        a, b = x[:i], x[i:]
        se = np.sqrt(hac_se(a) ** 2 + hac_se(b) ** 2)
        t = abs(a.mean() - b.mean()) / se
        if t > best: best, arg = t, int(yrs[i])
    return best, arg
obs_t, obs_year = sup_t(r, ys)
m_, phi, se = fit_ar1(r, ends)
Xn = sim_ar1(m_, phi, se, 2000, n, rng); nulls = np.array([sup_t(x, ys)[0] for x in Xn])
out["sup_t"] = dict(stat=float(obs_t), year=obs_year, p_value=float((nulls >= obs_t).mean()), null_p95=float(np.percentile(nulls, 95)))
# fixed-date contrasts with HAC se (post-1950 vs pre-1950, post-1980 vs rest)
def contrast(mask):
    a, b = r[mask], r[~mask]; d = a.mean() - b.mean(); se_ = np.sqrt(hac_se(a) ** 2 + hac_se(b) ** 2); return dict(diff=float(d), se=float(se_), t=float(d / se_))
out["contrast_1950"] = contrast(ys >= 1950); out["contrast_1980"] = contrast(ys >= 1980)
# rolling 30-year means (stitched) summary
w = [r[i:i + 30].mean() for i in range(n - 29)]
out["roll30_arith"] = dict(min=float(min(w)), p10=float(np.percentile(w, 10)), median=float(np.median(w)), p90=float(np.percentile(w, 90)), max=float(max(w)))
# parametric (AR(1) normal) bootstrap of the estimators: block bootstrap breaks the autocorrelation, so rho is taken from this
m_, phi, se = fit_ar1(r, ends); Xp = sim_ar1(m_, phi, se, 4000, n, rng)
pm = Xp.mean(1); ps = Xp.std(ddof=1, axis=1); pr = np.array([acf(x, 1) for x in Xp])
out["par_boot"] = dict(se_mean=float(pm.std()), se_sd=float(ps.std()), se_rho=float(pr.std()), mean_rho_hat=float(pr.mean()), analytic_se_rho=float(np.sqrt((1 - rho ** 2) / n)), analytic_se_sd_normal=float(sd / np.sqrt(2 * n)))
z = 1.2816
out["lvl2"] = dict(z=z, mean=[float(mu - z * out["se_ar1"]), float(mu), float(mu + z * out["se_ar1"])],
                   sd=[float(sd - z * out["par_boot"]["se_sd"]), float(sd), float(sd + z * out["par_boot"]["se_sd"])],
                   rho=[float(rho - z * out["par_boot"]["se_rho"]), float(rho), float(rho + z * out["par_boot"]["se_rho"])],
                   mean95=[float(mu - 1.96 * out["se_ar1"]), float(mu + 1.96 * out["se_ar1"])])
json.dump(out, open("level2_out.json", "w"), indent=1)
print(json.dumps({k: out[k] for k in ("par_boot", "lvl2", "sup_t")}, indent=1))
