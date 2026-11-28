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
from model_v3.runner.out_sweeps import CLOSED, MARGINS, TOLS, of1
from model_v3.runner.pool import pmap

HEADS = ('M1', 'M2', 'M4a', 'M3')


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


def feasibility(ev, specs, workers=1):
    """The feasibility map: for each spec and each rule (tolerance, margin) of out_sweeps (TOLS x MARGINS), per horizon (transition, short) F1 (percent of paths), M2 and M4a (means
    over paths). Returns the points (dicts with the spec, its labels, `F1`, `M2` and `M4a` by horizon under the strict rule (tolerance 0, margin 0, `CLOSED`), `map` = {(tol, margin): {horizon:
    (F1, M2, M4a)}} for every rule and `paths` = {(tol, margin, horizon): {line: per-path array}}), and OF1 as {key: per-path array} (`out_sweeps.of1`)."""
    pts = []
    for sp, e in zip(specs, pmap(ev, specs, workers)):   # `workers` > 1 evaluates the points in processes (pool.py); the same results
        (sg, wm), raw = labels(sp), e['sweeps']['of1']
        pt = dict(spec=sp, schedule_grid=sg, w_min=wm, F1={}, M2={}, M4a={}, map={}, paths={})
        for tol in TOLS:
            for m in MARGINS:
                for hz in ('transition', 'short'):
                    k = raw[m, hz]
                    closed = (k['p3'] <= (CLOSED if tol == 0 else tol)).astype(float) * 100
                    pt['paths'][tol, m, hz] = dict(F1=closed, M2=k['M2'], M4a=k['M4a'])
                    pt['map'].setdefault((tol, m), {})[hz] = (closed.mean(), _mean(k['M2']), _mean(k['M4a']))
        for hz in ('transition', 'short'):
            pt['F1'][hz], pt['M2'][hz], pt['M4a'][hz] = pt['map'][0.0, 0.0][hz]
        pts.append(pt)
    return pts, of1(pts)['OF1']


def under(pts, tol, margin):
    """The points as `choose` reads them, with F1, M2 and M4a of the rule (tol, margin)."""
    v = lambda p, i: {hz: p['map'][tol, margin][hz][i] for hz in ('transition', 'short')}
    return [dict(p, F1=v(p, 0), M2=v(p, 1), M4a=v(p, 2)) for p in pts]


NONE_PASSES = 'none_passes_75'


def map_summary(pts, rule):
    """OF1's summary per rule (tol, margin): the best F1 at the short window (any point, and among the points inside the M2 cap and the M4a floor) and where, the number of feasible
    points (F1 at least `closure_share_pct`, M2 and M4a inside) and the named schedules `choose` finds under that rule. `feasible` is the marker `none_passes_75` when there is none:
    nothing is relaxed silently, a relaxed rule's result is labelled with its rule (tolerance, margin), never offered as the strict result."""
    out = {}
    for tol in TOLS:
        for m in MARGINS:
            q = under(pts, tol, m)
            ok = [p for p in q if p['M2']['short'] <= rule['m2_cap_pct_per_year'] and p['M4a']['short'] >= rule['m4a_floor_pct']]
            best = lambda ps: (max(ps, key=lambda p: (p['F1']['short'], -p['M2']['short'])) if ps else None)
            feas = [p for p in ok if p['F1']['short'] >= rule['closure_share_pct']]
            b, bo = best(q), best(ok)
            out[tol, m] = dict(best_any=(b['F1']['short'], b['schedule_grid'], b['w_min']), best_inside=bo and (bo['F1']['short'], bo['schedule_grid'], bo['w_min']),
                               feasible=len(feas) or NONE_PASSES, named=choose(q, rule))
    return out


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


def tornado(ev, specs, rows, read, workers=1):
    """OT1 rows: dicts schedule, input, headline, horizon, low, high (swings against central), sorted within each (schedule, headline, horizon) by the larger
    absolute swing, descending. `rows` maps each input id to its register Row, `read` is the set of ids the evaluator reads; the others get 0.0 without a run."""
    out, ins = [], [i for i in rows if i in read]
    units = [(s, i, side) for s in specs for i, side in [(None, None)] + [(i, k) for i in ins for k in ('low', 'high')]]   # each is one evaluation, independent of the rest
    done = dict(zip(units, pmap(lambda u: ev(specs[u[0]]) if u[1] is None else ev(specs[u[0]], {u[1]: getattr(rows[u[1]], u[2])}), units, workers)))
    for s, spec in specs.items():
        cen = done[s, None, None]
        run = {i: {side: done[s, i, side] for side in ('low', 'high')} for i in ins}
        for name in (h for h in HEADS if h in cen or h != 'M3'):          # the household arm holds no M3 (withheld, arm.WITHHELD_BY): the head is left out
            for hz in (('single',) if name == 'M3' else ('transition', 'short', 'long')):
                grp = []
                for i in rows:
                    sw = {side: headline(run[i][side], name, hz) - headline(cen, name, hz) if i in run else 0.0 for side in ('low', 'high')}
                    grp.append(dict(schedule=s, input=i, headline=name, horizon=hz, **sw))
                out += sorted(grp, key=lambda r: -max(abs(r['low']), abs(r['high'])) if np.isfinite([r['low'], r['high']]).all() else 0.0)
    return out


def _illinois(f, lo, hi, a, b, tol, steps=6, maxit=60):
    """153c: the root of f on [lo, hi] (f(lo) = a and f(hi) = b of opposite sign) by Illinois secant steps, every one inside a bracket that keeps a sign change. It stops, as
    bisection does, with a bracket narrower than tol and returns its midpoint. When the secant estimate settles (within tol/2 of the point just evaluated) it probes tol/2 beyond
    that point, which closes the bracket if the sign changes there. Any doubt (a non-finite value, an estimate outside the bracket, a bracket not halved in two steps, `steps` secant steps
    used) is a bisection step."""
    last, side, n, sa, wid = None, 0, 0, np.sign(a), [hi - lo]
    while hi - lo >= tol and n < maxit:
        n += 1
        x = 0.5 * (lo + hi)
        if n <= steps and np.isfinite([a, b]).all() and a != b and not (n > 2 and hi - lo > 0.5 * wid[-2]):
            x = hi - b * (hi - lo) / (b - a)
            if last is not None and abs(x - last) < tol / 2:
                x = last + (tol / 2 if x >= last else -tol / 2)
            if not lo < x < hi:
                x = 0.5 * (lo + hi)
        v = f(x)
        if sa * v > 0:
            lo, a, b = x, v, (b / 2 if side == 1 else b); side = 1
        else:
            hi, b, a = x, v, (a / 2 if side == -1 else a); side = -1
        last = x; wid.append(hi - lo)
    return 0.5 * (lo + hi)


def breakeven(f, lo, hi, tol=1e-3, maxit=60, method='bisect'):
    """The root of f on [lo, hi] by bisection (`method='illinois'`: 153c, fewer evaluations, the same bracket guarantee), nan when f does not change sign there (never clipped)."""
    a, b = f(lo), f(hi)
    if not np.isfinite([a, b]).all() or a * b > 0:
        return float('nan')
    if method == 'illinois':
        return _illinois(f, lo, hi, a, b, tol, maxit=maxit)
    for _ in range(maxit):
        m = 0.5 * (lo + hi)
        v = f(m)
        lo, hi = (m, hi) if a * v > 0 else (lo, m)
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


def breakeven_return(ev, specs, mean_id, lo=0.0, hi=15.0, draws=None, tol=1e-2, workers=1, method='bisect'):
    """O1e: for each schedule the generator mean (percent a year) at which the short-window M1 is zero, other inputs central; with `draws` ({id: array}) one more
    root per draw, in the same order, for the range. Returns {schedule: (point, [roots over draws])}."""
    n = len(next(iter(draws.values()))) if draws else 0
    units = [(s, j) for s in specs for j in [None] + list(range(n))]   # one root each (a serial bisection); the roots are independent
    over = lambda j: {} if j is None else {i: float(v[j]) for i, v in draws.items() if i != mean_id}
    roots = dict(zip(units, pmap(lambda u: breakeven(lambda m: _mean(ev(specs[u[0]], {**over(u[1]), mean_id: m})['M1']['short']), lo, hi, tol, method=method), units, workers)))
    return {s: (roots[s, None], [roots[s, j] for j in range(n)]) for s in specs}


def stress(ev, spec, mu, amps, T, period=10):
    """CK1: the fixed path g(t) = mu + A sin(2 pi t / period) (percent), one path per amplitude A: {A: {'P1', 'P3', 'P3_long', 'P7b'}} (P3 from year 1 to the end of the short window,
    transition plus short, as 089c rules; P3_long over all years) and the largest A on the grid up to which P3 is zero on every smaller amplitude too (None if even the first is not
    zero: a finding, carried as it is, never dropped)."""
    t, out, top = np.arange(1, T + 1), {}, None
    for a in amps:
        e = ev(spec, g=((mu + a * np.sin(2 * np.pi * t / period)) / 100.0)[:, None])
        out[a] = {'P1': float(e['P1'][0]), 'P3': float(e['P3h']['short'][0]), 'P3_long': float(e['P3h']['long'][0]), 'P7b': float(e['P7b'][0])}
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
