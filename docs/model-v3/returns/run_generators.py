"""Q1, Q2: generator comparison against the observed UK record. python3 -I run_generators.py > generators_out.txt"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, json
from common import *
from generators import *
D = load(); ys, r = real(D, "capital_tr"); ends = segments(ys); n = len(r)
rng = np.random.default_rng(36); N = 20000; T = 100
res = {}
# observed
lg = np.log1p(r); cs = np.concatenate([[0], np.cumsum(lg)]); w88 = np.exp((cs[30:] - cs[:-30]) / 30) - 1
obs = dict(mean=r.mean(), sd=r.std(ddof=1), geo=gm(r), loss=(r < 0).mean(), ac1=acf(r, 1), ac2=acf(r, 2),
           run_contig=5, run_stitched=longest_run(r < 0), g30_p10=np.percentile(w88, 10), g30_p50=np.percentile(w88, 50), g30_p90=np.percentile(w88, 90), n_win=len(w88))
res["observed (117 years)"] = obs
# window replay of 100 years on the 117-year ring (v2 rule, wrap, repeats none)
Xw = np.array([[r[(i + k) % n] for k in range(100)] for i in range(n)]); st = path_stats(Xw); st["n_paths"] = n; res["a. window replay, 100y, 117 paths"] = st
# bootstrap family
for L in (1, 2, 3, 5, 10):
    X = sim_stationary_bootstrap(r, ends, L, N, T, rng); st = path_stats(X)
    st["w117"] = window_dispersion(sim_stationary_bootstrap(r, ends, L, 4000, 117, rng)).tolist(); res[f"b. stationary bootstrap, mean block {L}"] = st
# war years dropped (1914-18, 1939)
keep = ~(((ys >= 1914) & (ys <= 1918)) | (ys == 1939)); r2 = r[keep]; e2 = segments(ys[keep])
st = path_stats(sim_stationary_bootstrap(r2, e2, 3, N, T, rng)); st["sample_mean"] = r2.mean(); st["sample_sd"] = r2.std(ddof=1); res["d. bootstrap, 1914-18 and 1939 dropped, block 3"] = st
# parametric
mu, sd = r.mean(), r.std(ddof=1)
res["c1. iid normal"] = {**path_stats(sim_normal(mu, sd, N, T, rng)), "w117": window_dispersion(sim_normal(mu, sd, 4000, 117, rng)).tolist()}
llt, dft, mut, st_ = fit_t(r); Xt = sim_t(dft, mut, st_, N, T, rng)
res["c2. iid Student t"] = {**path_stats(Xt), "df": dft, "w117": window_dispersion(sim_t(dft, mut, st_, 4000, 117, rng)).tolist()}
m_, phi, se = fit_ar1(r, ends)
res["c3. AR(1) normal"] = {**path_stats(sim_ar1(m_, phi, se, N, T, rng)), "phi": phi, "w117": window_dispersion(sim_ar1(m_, phi, se, 4000, 117, rng)).tolist()}
res["c4. AR(1) t"] = {**path_stats(sim_ar1(m_, phi, se, N, T, rng, "t", max(dft, 4))), "w117": window_dispersion(sim_ar1(m_, phi, se, 4000, 117, rng, "t", max(dft, 4))).tolist()}
hm = fit_hmm(r, ends); Xh = sim_hmm(hm, N, T, rng)
res["d2. 2-state Gaussian HMM"] = {**path_stats(Xh), "mu": hm[1].tolist(), "sd": hm[2].tolist(), "A": hm[3].tolist(), "w117": window_dispersion(sim_hmm(hm, 4000, 117, rng)).tolist()}
# automatic block length, Politis and White (2004) flat-top window, lag 2 (rho_3 and beyond not distinguishable from zero)
g0 = r.var(); g1 = acf(r, 1) * g0; G_ = 2 * 1.0 * 1 * g1; gg0 = g0 + 2 * g1; Dsb = 2 * gg0 ** 2
res["pw_block"] = float((2 * G_ ** 2 / Dsb) ** (1 / 3) * n ** (1 / 3)); res["acf"] = [acf(r, k) for k in range(1, 6)]
# fit statistics (log likelihood, BIC), same 117 observations
def ll_norm(x, m, s): return float((-0.5 * np.log(2 * np.pi * s * s) - 0.5 * ((x - m) / s) ** 2).sum())
bic = lambda ll, k: -2 * ll + k * np.log(n)
llN = ll_norm(r, mu, r.std(ddof=0))
x0 = np.array([r[i - 1] for i in range(1, n) if not ends[i - 1]]); x1 = np.array([r[i] for i in range(1, n) if not ends[i - 1]])
llA = ll_norm(x1 - m_ - phi * (x0 - m_), 0, (x1 - m_ - phi * (x0 - m_)).std())
res["fit"] = dict(normal=dict(ll=llN, bic=bic(llN, 2)), t=dict(ll=llt, bic=bic(llt, 3), df=dft), ar1=dict(ll=llA, n=len(x1), phi=phi, se_phi=float(np.sqrt((1 - phi ** 2) / len(x1)))), hmm=dict(ll=hm[0], bic=bic(hm[0], 6)))
res["fit"]["moments"] = dict(skew=float(((r - mu) ** 3).mean() / r.std() ** 3), kurt=float(((r - mu) ** 4).mean() / r.std() ** 4))
json.dump(res, open("generators_out.json", "w"), indent=1, default=float)
fmt = lambda v: f"{100*v:.2f}"
for k, v in res.items():
    if k in ("fit", "pw_block", "acf"): print(k, json.dumps(v, default=float)); continue
    print(k)
    print("  ", {a: (round(b, 4) if isinstance(b, float) else b) for a, b in v.items() if a not in ("w117",)})
    if "w117" in v: print("   88-window-style P10/P50/P90:", [round(x, 4) for x in v["w117"]])
