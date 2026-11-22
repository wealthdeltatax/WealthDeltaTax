"""
sweeps.py -- the schedule sweep, the tornado, the break-even return and the stress test (model v3, stage V3-10)
==============================================================================================================
Layer L4 (architecture.md 5.1). Imports numpy and the return generator; it does not import runner.py (same layer): every function takes the evaluator
`ev(spec, over=None, g=None)` that runner.make_ev builds, and returns per-path evaluations (runner.evaluate). Nothing is read and nothing runs at import
(R8). No country or tax is named here (R11): the lever grid, the feasibility constants, the register rows and the tier 1 list arrive as arguments.

A `spec` is a dict tau_0, tau_m, k_ln, ratio (the threshold as a multiple of the median house price per adult).

THE NAMED SCHEDULES (architecture.md 2.8, 8.1; author 2026-11-18)
-----------------------------------------------------------------
The feasibility map runs every point of the lever grid at central inputs. A point is feasible when, over the short window, the closure share F1 (the
share of paths in which retired receipts never outrun relief, P3 zero up to the end of the window) is at least `closure_share_pct`, M2 is at most
`m2_cap_pct_per_year` and M4a at least `m4a_floor_pct`. S_central is the feasible point with the highest closure share (the lower M2 on a tie); S_low and
S_high are the feasible points with the lowest and the highest M2, the two edges of the region along the burden axis. No feasible point: `choose` returns
None and the run reports it (nothing is chosen in its place).

THE TORNADO (T1)
----------------
One input at a time at its register low and high, every other input central, on the same common random numbers: the swing is the headline at that value
minus the headline at central, as a mean over the paths. Inputs the evaluator does not read (runner.reads) are not run and their swing is exactly 0.
Rows are sorted within each (schedule, headline, horizon) by the larger absolute swing, descending (N3). M3 has one horizon, `single`.
"""

from __future__ import annotations

import numpy as np

from model_v3.core import returns as rt

HEADS = ('M1', 'M2', 'M4a', 'M3')
CLOSED = 1e-9


def labels(spec):
    """The manifest's vocabulary for one grid point: (schedule_grid, w_min), e.g. ('tm70_k05', 'r050')."""
    k = f"{spec['k_ln']:g}".replace('.', '')
    return f"tm{round(100 * spec['tau_m'])}_k{k}", f"r{round(100 * spec['ratio']):03d}"


def grid(levers):
    """Every point of the lever grid as specs, in the file's axis order."""
    ax = levers['axes']
    return [dict(tau_0=t0, tau_m=tm, k_ln=k, ratio=r) for tm in ax['tau_m'] for k in ax['k_ln'] for t0 in ax['tau_0'] for r in ax['threshold_ratio']]


def _mean(x):
    x = np.asarray(x, float)
    return float(np.nanmean(x)) if np.isfinite(x).any() else float('nan')


def feasibility(ev, specs):
    """The feasibility map: for each spec, per horizon (transition, short) F1 (percent of paths), M2 and M4a (means over paths). Returns the points
    (dicts with the spec, its labels and those numbers) and OF1 as {key: array} with one entry per path (F1 is the 0 or 1 of each path)."""
    pts, of1 = [], {}
    for sp in specs:
        e, (sg, wm) = ev(sp), labels(sp)
        pt = dict(spec=sp, schedule_grid=sg, w_min=wm, F1={}, M2={}, M4a={})
        for hz in ('transition', 'short'):
            closed = (e['P3h'][hz] <= CLOSED).astype(float)
            pt['F1'][hz], pt['M2'][hz], pt['M4a'][hz] = 100 * closed.mean(), _mean(e['M2'][hz]['overall']), _mean(e['M4a'][hz]['overall'])
            by = (('schedule_grid', sg), ('w_min', wm))
            of1[None, hz, by, 'F1'], of1[None, hz, by, 'M2'], of1[None, hz, by, 'M4a'] = closed * 100, e['M2'][hz]['overall'], e['M4a'][hz]['overall']
        pts.append(pt)
    return pts, of1


def choose(points, rule):
    """The named schedules by the rule above: {'S_low', 'S_central', 'S_high'} -> spec, or None when no point is feasible."""
    ok = [p for p in points if p['F1']['short'] >= rule['closure_share_pct'] and p['M2']['short'] <= rule['m2_cap_pct_per_year'] and p['M4a']['short'] >= rule['m4a_floor_pct']]
    if not ok:
        return None
    pick = lambda f: f['spec']
    return {'S_low': pick(min(ok, key=lambda p: p['M2']['short'])), 'S_central': pick(max(ok, key=lambda p: (p['F1']['short'], -p['M2']['short']))),
            'S_high': pick(max(ok, key=lambda p: p['M2']['short']))}


def headline(e, name, hz):
    """The mean over paths of one headline at one horizon of an evaluation."""
    if name == 'M3':
        return _mean(e['M3'])
    return _mean(e[name][hz] if name == 'M1' else e[name][hz]['overall'])


def tornado(ev, specs, rows, read):
    """OT1 rows: dicts schedule, input, headline, horizon, low, high (swings against central), sorted within each (schedule, headline, horizon) by the larger
    absolute swing, descending. `rows` maps each input id to its register Row, `read` is the set of ids the evaluator reads; the others get 0.0 without a run."""
    out = []
    for s, spec in specs.items():
        cen = ev(spec)
        run = {i: {side: ev(spec, {i: getattr(r, side)}) for side in ('low', 'high')} for i, r in rows.items() if i in read}
        for name in (h for h in HEADS if h in cen or h != 'M3'):          # the household arm holds no M3 (withheld, arm.WITHHELD_BY): the head is left out
            for hz in (('single',) if name == 'M3' else ('transition', 'short', 'long')):
                grp = []
                for i in rows:
                    sw = {side: headline(run[i][side], name, hz) - headline(cen, name, hz) if i in run else 0.0 for side in ('low', 'high')}
                    grp.append(dict(schedule=s, input=i, headline=name, horizon=hz, **sw))
                out += sorted(grp, key=lambda r: -max(abs(r['low']), abs(r['high'])) if np.isfinite([r['low'], r['high']]).all() else 0.0)
    return out


def breakeven(f, lo, hi, tol=1e-3, maxit=60):
    """The root of f on [lo, hi] by bisection, nan when f does not change sign there (never clipped)."""
    a, b = f(lo), f(hi)
    if not np.isfinite([a, b]).all() or a * b > 0:
        return float('nan')
    for _ in range(maxit):
        m = 0.5 * (lo + hi)
        v = f(m)
        lo, hi = (m, hi) if a * v > 0 else (lo, m)
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


def breakeven_return(ev, specs, mean_id, lo=0.0, hi=15.0, draws=None, tol=1e-2):
    """O1e: for each schedule the generator mean (percent a year) at which the short-window M1 is zero, other inputs central; with `draws` ({id: array}) one more
    root per draw, in the same order, for the range. Returns {schedule: (point, [roots over draws])}."""
    out = {}
    for s, spec in specs.items():
        root = lambda over, spec=spec: breakeven(lambda m: _mean(ev(spec, {**over, mean_id: m})['M1']['short']), lo, hi, tol)
        n = len(next(iter(draws.values()))) if draws else 0
        out[s] = (root({}), [root({i: float(v[j]) for i, v in draws.items() if i != mean_id}) for j in range(n)])
    return out


def stress(ev, spec, mu, amps, T, period=10):
    """CK1: the fixed path g(t) = mu + A sin(2 pi t / period) (percent), one path per amplitude A: {A: {'P1', 'P3', 'P7b'}} and the largest A on the grid up to
    which P3 is zero on every smaller amplitude too (None if even the first is not zero)."""
    t, out, top = np.arange(1, T + 1), {}, None
    for a in amps:
        e = ev(spec, g=((mu + a * np.sin(2 * np.pi * t / period)) / 100.0)[:, None])
        out[a] = {'P1': float(e['P1'][0]), 'P3': float(e['P3h']['long'][0]), 'P7b': float(e['P7b'][0])}
    for a in amps:
        if out[a]['P3'] > CLOSED:
            break
        top = a
    return out, top


def robustness(ev, spec, rng, years, r, T, n):
    """The block bootstrap check: the same schedule on n stationary block bootstrap paths of the sample r (percent), M1 by horizon per path and the unfilled count."""
    e = ev(spec, g=rt.block_bootstrap(rng, years, r, T, n))
    return {'M1': e['M1'], 'unfilled_paths': int(e['unfilled'].sum())}


def spread30(g, q=(10, 50, 90)):
    """The 30-year spread display (C1 item 4a): percentiles of the geometric mean real return over the first 30 years of each path, percent a year."""
    return np.percentile(100 * (np.prod(1.0 + np.asarray(g)[:30], axis=0) ** (1 / 30) - 1), q)
