"""
out_support.py -- output group: support, declaration and welfare (model v3, brief 087c)
======================================================================================
Interface: groups.py. Layer L3.5: reads core only; the runner's `Raw`, `Env` and `again` arrive as arguments. Ids and the core function behind each (core/support.py):
  O7   M7   declaration_runs, declaration_curve, tolerant_zone: a Route C line of I-D14h pounds m at each alpha, G holding years and a sale year, the schedule's rate
  OD1  M7c, M7d   the same curve at the manifest's eight alphas, by path
  OW1  M13  welfare (I-H5a, I-D14c, the base's lines and weights), per band: payer-weighted mean over the band's lines; one value per chunk, repeated over its paths
  OW2  M14  lockin (I-T7a); whole years drawn jointly from the pack's housing_tr and bond_tr (real, same year for both) with env.rng('support'); one value per chunk
  OW3  M15a, M15b  envelope, liquidity_timing on a kernel rerun with per-year capture (one death phase, deaths every G years); M15b first I-D14e years
  OM1  M1, X, M9  migration_effect (I-D5c, I-D9d, I-M6l, I-T3q, I-D14c); the payer count is the full receipts run's (`again({}, True)`)
Cells follow outputs.yml: p10_mean_p90 ids keep the per-path (level 1) or per-draw (level 2) array; point_and_range ids hold [point, lo, hi] = [mean, P10, P90] over it;
O7 holds [1.0, mean lower edge, mean upper edge] of the tolerant zone. A band with no payer at launch is nan, as in O2. 
  OS1  S1  s1_effect on again({}, tweak=...) with capitalise (pack property_share by band, I-D10b); m1, m2 (overall) and payer_count at the short horizon; [mean, P10, P90]
"""
from __future__ import annotations

from dataclasses import replace

import numpy as np

from model_v3.core import burden as bd
from model_v3.core import kernel as K
from model_v3.core import revenue as rv
from model_v3.core import support as U

NAME, IDS = 'support', ('O7', 'OD1', 'OW1', 'OW2', 'OW3', 'OM1', 'OS1')
HZ = ('transition', 'short', 'long')
ALPHA = (('a050', .5), ('a075', .75), ('a100', 1.0), ('a125', 1.25), ('a150', 1.5), ('a200', 2.0), ('a300', 3.0), ('a500', 5.0))
GAIN, HOLD = (('pct25', .25), ('pct50', .5), ('pct75', .75)), (('y5', 5), ('y10', 10), ('y20', 20))
SYS = (('wdt', 'wdt'), ('income_tax_cgt', 'income_tax_gains'), ('stock_wealth_tax', 'stock_wealth_tax'), ('consumption_tax', 'consumption_tax'))
TOL = 1e-12


def _row(env, i):
    """A register row: this evaluation's value when the run draws it, else its central."""
    return env.theta[i] if i in env.theta else float(env.ctx.reg[i].central)


def _assets(env, n, P):
    """(housing, bond) real arithmetic returns (n, P): whole years drawn jointly from the pack's returns table."""
    t = env.pack.tables['returns']
    col = lambda c: np.array([np.nan if r[c] is None else r[c] for r in t])
    h, b, cpi, yr = col('housing_tr'), col('bond_tr'), col('cpi'), col('year')
    ok = np.isfinite(h[1:]) & np.isfinite(b[1:]) & np.isfinite(cpi[1:]) & np.isfinite(cpi[:-1]) & (np.diff(yr) == 1)
    i = env.rng('support').integers(0, int(ok.sum()), (n, P))
    real = lambda x: ((1 + x[1:][ok] / 100) / (cpi[1:][ok] / cpi[:-1][ok]) - 1)[i]
    return real(h), real(b)


def _record(raw, env):
    """The kernel over every line and path with per-year capture: (T, P, L) assessed tax and cumulative lost refund (line_flows' fold, one death phase)."""
    b, (T, P), L, lam = raw.base, raw.g.shape, len(raw.base.labels), env.lam
    old = raw.arm['arm'] == 'legacy'
    hook = None if old else env.arm(b).make()                                                    # the household arm reruns the kernel on its account (126c): the hook sets growth and consumption, g is ignored
    book = K.Book(L * P, {r: np.tile(v, P) for r, v in b.V0.items()}, alpha0={'C': 1.0, 'D': 1.0}, has_cv=lam['lam_C'] > 0 and bool(np.any(b.V0['C'] > 0)))
    ix, Ls, lost = np.cumprod(1.0 + raw.gdp_g, axis=0), [], []
    for t in range(1, T + 1):
        il, gt = np.repeat(ix[t - 1], L), np.repeat(raw.g[t - 1], L)
        Ls.append(dict(K.step_year(book, raw.rate, il, gt, raw.c if old else 0.0, 1.0, 1.0, lam['lam_C'], lam['lam_D'], hook=hook, t=t))['tax'].L)
        lost.append(book.lost_refund.copy())
        if t < T and t % b.G == 0:
            K.step_death(book, raw.rate, il)
    return U.envelope(np.array(Ls), np.array(lost))['forgone_t'].reshape(T, P, L)


def _envelope(raw, env):
    """{'M15a': {horizon: {band: (P,)}}, 'M15b': {band: (P,)}}: share of payers whose cap binds in the window (percent), and the refunds held back as percent of GDP."""
    b, x = raw.base, _record(raw, env)
    pw, t = b.weights * (b.wealth >= b.w_min), np.arange(1, x.shape[0] + 1)[:, None]
    a, m15a = {}, {}
    for h in HZ:
        hit = ((x > TOL) & ((t >= raw.lo[h]) & (t <= raw.hi[h]))[:, :, None]).any(0)
        m15a[h] = {k: np.where(raw.ok | (h != 'short'), 100 * (hit[:, m] * pw[m]).sum(1) / pw[m].sum() if pw[m].any() else np.nan, np.nan) for k, m in bd._groups(b.band).items()}
    for k, m in bd._groups(b.band).items():
        a[k] = U.liquidity_timing(b.adults_k.sum() * (b.weights[m] * x[:, :, m]).sum(2), raw.r['gdp'], int(raw.h))
    return {'M15a': m15a, 'M15b': a}


def _migration(raw, env, again):
    """{line: {horizon: (P,)}} for M1, X and M9, windowed like M1 (ratio of sums over the horizon's years)."""
    b, run, r = raw.base, again({}, True).run, raw.r
    pw = b.weights * (b.wealth >= b.w_min)
    spend = raw.c * (pw * b.wealth).sum() / pw.sum() if raw.arm['arm'] == 'legacy' else (pw * env.arm(b).make().consumption()).sum() / pw.sum()    # a leaver's spend: the legacy share of wealth, or the account's consumption C (126c)
    m = U.migration_effect(r['M1'], run['payers'], r['gdp'], run['gdp_index'], _row(env, 'I-D5c') / 100, _row(env, 'I-D9d'), _row(env, 'I-M6l') / 100,
                           spend=spend * 1e6, rate_spend=_row(env, 'I-T3q') / 100)
    return {k: {h: np.where(raw.ok | (h != 'short'), rv.window_mean(v, r['gdp'], raw.lo[h], raw.hi[h]), np.nan) for h in HZ} for k, v in m.items()}


def grow(b, f):
    """The base with every line's wealth and routes times f (the routes sum to the wealth; burden.line_flows starts from the routes)."""
    return replace(b, wealth=b.wealth * f, V0={r: v * f for r, v in b.V0.items()})


def _s1(raw, env, again):
    """{'m1', 'm2', 'payer_count': (P,)}: the capitalisation switch on minus off at the short horizon (property share by band from the pack, uplift I-D10b, threshold untouched)."""
    t = {r['band']: r['value'] / 100 for r in env.pack.tables['wealth_distribution'] if r['variable'] == 'property_share'}
    sh, up = np.array([t.get(x, 0.0) for x in raw.base.band]), _row(env, 'I-D10b') / 100
    q = lambda x: {'m1': rv.window_mean(x.r['M1'], x.r['gdp'], x.lo['short'], x.hi['short']), 'm2': bd.m2(x.fl, x.lo['short'], x.hi['short'])['overall'],
                   'payer_count': np.full(x.g.shape[1], U.payer_count(x.base.wealth, x.base.adults_k, x.base.w_min))}
    return U.s1_effect(q(again({}, tweak=lambda b: grow(b, U.capitalise(b.wealth, sh, up, on=True) / b.wealth))), q(raw))


def per_path(raw, env, again):
    """Per-path arrays for one chunk of paths; the certainty-equivalent leaves hold the chunk's one value repeated over its paths."""
    b, P, al = raw.base, raw.g.shape[1], [a for _, a in ALPHA]
    c1, lost = U.declaration_curve(U.declaration_runs(raw.rate, raw.g[:b.G + 1], _row(env, 'I-D14h'), al), al)
    zlo, zhi = U.tolerant_zone(al, c1)
    old = raw.arm['arm'] == 'legacy'
    cew = U.welfare(raw.rate, raw.g[:b.G], b.V0, b.weights, _row(env, 'I-H5a'), b.w_min, raw.c if old else 0.0, hook=None if old else env.arm(b).make(), **env.lam)[0]   # M13: the household arm's comparators sit on its account (126c)
    pw, hA, hB = b.weights * (b.wealth >= b.w_min), *_assets(env, max(n for _, n in HOLD), P)
    one = lambda v: np.full(P, v)
    return {'decl': {'M7c': {k: c1[i] for i, (k, _) in enumerate(ALPHA)}, 'M7d': {k: lost[i] for i, (k, _) in enumerate(ALPHA)}, 'zone': {'lo': zlo, 'hi': zhi}},
            'welfare': {k: {s: one(U.wmean(cew[u][m], pw[m]) if pw[m].any() else np.nan) for s, u in SYS} for k, m in bd._groups(b.band).items()},
            'lock': {g: {h: one(U.lockin(hA, hB, _row(env, 'I-T7a') / 100, e, n, _row(env, 'I-H5a'))[0]) for h, n in HOLD} for g, e in GAIN},
            'env': _envelope(raw, env), 'mig': _migration(raw, env, again), 's1': _s1(raw, env, again)}


def _tri(x):
    """[point, lo, hi] of a per-path (level 1) or per-draw (level 2) array: mean, P10, P90."""
    return np.array([np.nanmean(x), *np.nanpercentile(x, [10, 90])])


def cells(e):
    """{output id: {(horizon, by, line): array}} from this group's per-path results of one schedule."""
    if not e:
        return {}
    d, w, k, v, m, s1 = (e[x] for x in ('decl', 'welfare', 'lock', 'env', 'mig', 's1'))
    ev = lambda b: (('entry_year', 'value_per_cohort'), ('wealth_band', b))
    out = {'O7': {('single', (), None): np.array([1.0, np.nanmean(d['zone']['lo']), np.nanmean(d['zone']['hi'])])},
            'OD1': {('single', (('alpha_grid', a),), l): _tri(d[l][a]) for l in ('M7c', 'M7d') for a, _ in ALPHA},
            'OW2': {('single', (('embedded_gain_band', g), ('holding_period', h)), None): k[g][h] for g, _ in GAIN for h, _ in HOLD},
            'OS1': {('single', (('quantity', q),), None): _tri(x) for q, x in s1.items()}}
    out['OW1'] = {('single', (('tax_system', s), ('wealth_band', b)), None): w[b][s] for b in w for s, _ in SYS}
    if v:
        out['OW3'] = {**{(h, ev(b), 'M15a'): v['M15a'][h][b] for h in HZ for b in v['M15a'][h]}, **{('transition', ev(b), 'M15b'): x for b, x in v['M15b'].items()}}
        out['OM1'] = {(h, (), l): m[l][h] for l in m for h in HZ}
    return out
