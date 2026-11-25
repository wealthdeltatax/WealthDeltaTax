"""Return generators for brief 036r. All take the observed real annual returns r (117 values, two contiguous segments)."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from common import *

def sim_stationary_bootstrap(r, ends, L, n_paths, T, rng, demean_to=None):
    """Stationary block bootstrap (Politis and Romano 1994), mean block length L. Blocks wrap inside their own
    contiguous calendar segment (never across a gap), so every observation keeps the same weight and the mean is unbiased."""
    n = len(r); x = r.copy()
    if demean_to is not None: x = x - x.mean() + demean_to
    start = np.zeros(n, int); s0 = 0
    for i in range(n):
        start[i] = s0
        if ends[i]: s0 = i + 1
    pos = rng.integers(0, n, n_paths); out = np.empty((n_paths, T))
    for t in range(T):
        out[:, t] = x[pos]
        nxt = np.where(ends[pos], start[pos], pos + 1)
        pos = np.where(rng.random(n_paths) < 1.0 / L, rng.integers(0, n, n_paths), nxt)
    return out

def sim_normal(mu, sd, n_paths, T, rng): return mu + sd * rng.standard_normal((n_paths, T))

def fit_t(r):
    """Student t by maximum likelihood over df on a grid (location and scale by EM-free grid refinement)."""
    from math import lgamma, pi, log
    best = None
    for df in [3, 4, 5, 6, 8, 10, 15, 20, 30, 60]:
        mu = r.mean(); s = r.std(ddof=1) * np.sqrt((df - 2) / df)
        for _ in range(60):   # EM for location/scale given df
            z = (r - mu) / s; w = (df + 1) / (df + z * z)
            mu = (w * r).sum() / w.sum(); s = np.sqrt((w * (r - mu) ** 2).mean())
        z = (r - mu) / s
        ll = (len(r) * (lgamma((df + 1) / 2) - lgamma(df / 2) - 0.5 * log(df * pi) - log(s)) - (df + 1) / 2 * np.log1p(z * z / df).sum())
        if best is None or ll > best[0]: best = (ll, df, mu, s)
    return best  # ll, df, mu, scale

def sim_t(df, mu, s, n_paths, T, rng): return mu + s * rng.standard_t(df, (n_paths, T))

def fit_ar1(r, ends):
    """AR(1) by least squares within segments: r_t - m = phi (r_t-1 - m) + e; returns (mean, phi, innovation sd)."""
    m = r.mean(); x0 = []; x1 = []
    for i in range(1, len(r)):
        if not ends[i - 1]: x0.append(r[i - 1] - m); x1.append(r[i] - m)
    x0 = np.array(x0); x1 = np.array(x1); phi = (x0 * x1).sum() / (x0 * x0).sum()
    # parameterised by the marginal sd, so the simulated sd equals the sample sd: innovation sd = sd * sqrt(1 - phi^2)
    return m, phi, r.std(ddof=1) * np.sqrt(1 - phi ** 2)

def sim_ar1(m, phi, se, n_paths, T, rng, dist="normal", df=None):
    out = np.empty((n_paths, T)); sd0 = se / np.sqrt(1 - phi ** 2)
    x = sd0 * rng.standard_normal(n_paths)
    for t in range(T):
        e = se * (rng.standard_normal(n_paths) if dist == "normal" else rng.standard_t(df, n_paths) * np.sqrt((df - 2) / df))
        x = phi * x + e if t else x; out[:, t] = m + x
    return out

def fit_hmm(r, ends, K=2, iters=300, seed=0):
    """Gaussian K-state hidden Markov model by EM. Observations in two segments; state chain restarts at each segment (stationary start)."""
    rng = np.random.default_rng(seed); n = len(r)
    best = None
    for rep in range(8):
        mu = np.sort(r.mean() + r.std() * rng.standard_normal(K)); sd = np.full(K, r.std()); A = np.full((K, K), 1.0 / K) * 0.5 + 0.5 * np.eye(K); pi = np.full(K, 1.0 / K)
        segs = []; s0 = 0
        for i in range(n):
            if ends[i]: segs.append((s0, i + 1)); s0 = i + 1
        ll_old = -1e18
        for it in range(iters):
            g_tot = np.zeros(K); xi_tot = np.zeros((K, K)); m1 = np.zeros(K); m2 = np.zeros(K); pi_new = np.zeros(K); ll = 0.0
            for a, b in segs:
                x = r[a:b]; T = len(x)
                B = np.exp(-0.5 * ((x[:, None] - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi)) + 1e-300
                al = np.zeros((T, K)); c = np.zeros(T)
                al[0] = pi * B[0]; c[0] = al[0].sum(); al[0] /= c[0]
                for t in range(1, T):
                    al[t] = (al[t - 1] @ A) * B[t]; c[t] = al[t].sum(); al[t] /= c[t]
                be = np.ones((T, K))
                for t in range(T - 2, -1, -1): be[t] = (A @ (B[t + 1] * be[t + 1])) / c[t + 1]
                g = al * be; g /= g.sum(1, keepdims=True)
                for t in range(T - 1):
                    xi = al[t][:, None] * A * (B[t + 1] * be[t + 1])[None, :]; xi_tot += xi / xi.sum()
                g_tot += g.sum(0); m1 += (g * x[:, None]).sum(0); m2 += (g * x[:, None] ** 2).sum(0); pi_new += g[0]; ll += np.log(c).sum()
            mu = m1 / g_tot; sd = np.sqrt(np.maximum(m2 / g_tot - mu ** 2, 1e-6)); A = xi_tot / xi_tot.sum(1, keepdims=True); pi = pi_new / pi_new.sum()
            if abs(ll - ll_old) < 1e-9: break
            ll_old = ll
        if best is None or ll > best[0]: best = (ll, mu.copy(), sd.copy(), A.copy(), pi.copy())
    return best

def sim_hmm(par, n_paths, T, rng):
    ll, mu, sd, A, pi = par; K = len(mu); out = np.empty((n_paths, T))
    # stationary distribution of A
    w, v = np.linalg.eig(A.T); st = np.real(v[:, np.argmax(np.real(w))]); st = st / st.sum()
    cum = np.cumsum(A, 1); s = rng.choice(K, n_paths, p=st)
    for t in range(T):
        out[:, t] = mu[s] + sd[s] * rng.standard_normal(n_paths)
        u = rng.random(n_paths); s = (u[:, None] > cum[s]).sum(1).clip(max=K - 1)
    return out

def path_stats(X, win=30):
    """Statistics over simulated paths X (n_paths x T), real annual returns."""
    n, T = X.shape; neg = X < 0
    # longest run per path
    run = np.zeros(n, int); cur = np.zeros(n, int)
    for t in range(T):
        cur = np.where(neg[:, t], cur + 1, 0); run = np.maximum(run, cur)
    lg = np.log1p(X)
    g30 = np.exp(lg[:, :win].mean(1)) - 1
    ac1 = np.array([np.corrcoef(X[i, :-1], X[i, 1:])[0, 1] for i in range(min(n, 2000))]).mean()
    return dict(mean=X.mean(), sd=X.std(ddof=1, axis=1).mean(), geo=(np.exp(lg.mean(1)) - 1).mean(), loss=neg.mean(), ac1=ac1,
                run_mean=run.mean(), run_p90=np.percentile(run, 90), run4=(run >= 4).mean(), run6=(run >= 6).mean(),
                g30_p10=np.percentile(g30, 10), g30_p50=np.percentile(g30, 50), g30_p90=np.percentile(g30, 90))

def window_dispersion(X, T=117, win=30):
    """Same procedure as the 88 observed windows: all overlapping 30-year geometric means within each 117-year path, pooled."""
    lg = np.log1p(X[:, :T]); cs = np.cumsum(np.concatenate([np.zeros((len(X), 1)), lg], 1), 1)
    w = np.exp((cs[:, win:] - cs[:, :-win]) / win) - 1
    return np.percentile(w, [10, 50, 90])
