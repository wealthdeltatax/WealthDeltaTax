"""
out_sweeps.py -- output group: the sweep-owned ids O1e, OF1 and OT1 and the pack's data facts DH1a and DH1b (briefs 088c, 089c)
====================================================================================================================
Interface: see groups.py. `cells` stays empty: O1e, OF1 and OT1 are sweep results, not per-schedule cells, so the run script (057c) runs `sweeps.breakeven_return`, `sweeps.feasibility` and
`sweeps.tornado`, formats them with `o1e`, `of1` and `ot1` and puts their cells into Samples next to `samples(...)` (CK1, a check, from `sweeps.stress` with `ck1`; `per_path` carries only OF1's private per-path shortfalls); they come back keyed as Samples are, (schedule, horizon, by, line), the schedule already in
front. DH1a and DH1b read the pack only, through `static(env)` (schedule None, `once_not_per_schedule`). Imports core/pack only (the sweeps are in the runner layer: the run script passes their results in).
"""

import numpy as np

from model_v3.core import burden as bd, pack as pk, revenue as rv

NAME = 'sweeps'
IDS = ('DH1a', 'DH1b', 'O1e', 'OF1', 'OT1')
CLOSED = 1e-9                                                   # the strict closure tolerance (055c): P3 at most this is closed
TOLS = (0.0, 0.05, 0.25, 1.0)                                   # OF1 rule axes (089c, 140c): labelled scenario constants, not register rows. A tolerance is a total shortfall P3 (GDP-points); 0 is `CLOSED`
MARGINS = (0.0, 0.10, 0.25)                                     # retirement margin: a tax is retired when relief / (1 + margin) covers its receipts; the shortfall is measured against the true relief
HORIZON = {'M1': 'short', 'M2': 'short', 'M4a': 'short', 'M3': 'single'}     # OT1 is single horizon: M3 has one, the others are read at the short window


def per_path(raw, env, again):
    """Per path, for OF1 only (`sweeps.feasibility` reads it; the group's `cells` stays empty): {'of1': {(margin, horizon): {'p3', 'M2', 'M4a'}}} for the transition and the short window,
    p3 the shortfall summed from year 1 to the window's end against a retirement with that margin (`revenue.retire` on relief / (1 + margin)); M2 and M4a as the headlines (nan on an unfilled path at `short`)."""
    r, t = raw.r, np.arange(1, raw.r['relief'].shape[0] + 1)[:, None]
    out = {}
    for m in MARGINS:
        m1d, yr = rv.retire(r['relief'] / (1.0 + m), r['fill'], env.ctx.rec)
        ex = np.maximum(0.0, m1d - r['relief'])
        for hz in ('transition', 'short'):
            hi, gate = raw.hi[hz], (lambda v: np.where(raw.ok, v, np.nan)) if hz == 'short' else (lambda v: v)
            out[m, hz] = dict(p3=(ex * (t <= hi[None, :])).sum(axis=0), M2=gate(bd.m2(raw.fl, raw.lo[hz], hi)['overall']),
                              M4a=gate(bd.m4(yr, hi, raw.inc, env.ctx.bill, env.ctx.income)['M4a']['overall']))
    return {'of1': out}


def cells(e):
    """Nothing per schedule (see the module note)."""
    return {}


def static(env):
    """DH1a (top wealth shares: [point, lo, hi], the point itself for a side the source gives no range for) and DH1b (receipts by line, percent of GDP),
    only the ids the context marks once_not_per_schedule (`Ctx.once`: the only ids a `static` may return)."""
    a, b = pk.dh1a(env.pack), pk.dh1b(env.pack)['lines']
    cells = {'DH1a': {('single', (('series', s),), None): np.array([v['point'], *(v['point'] if v[x] is None else v[x] for x in ('lo', 'hi'))], float) for s, v in a.items()},
            'DH1b': {('single', (('line', ln),), None): np.array([v], float) for ln, v in b.items()}}
    return {i: c for i, c in cells.items() if i in env.ctx.once}


def o1e(roots):
    """O1e: {'O1e': {(schedule, 'single', (), None): [point, p10, p90]}} from `sweeps.breakeven_return`, {schedule: (point, roots over draws)}: the range is the
    10th and 90th percentiles of the roots (never clipped; a draw with no root is left out)."""
    cell = {}
    for s, (pt, r) in roots.items():
        r = np.asarray(r, float)
        cell[s, 'single', (), None] = np.array([pt, *(np.nanpercentile(r, [10, 90]) if np.isfinite(r).any() else (np.nan, np.nan))], float)
    return {'O1e': cell}


def ot1(rows):
    """OT1: {'OT1': {(schedule, 'single', (('headline', h), ('input', i)), None): [0, low, high]}} from the rows of `sweeps.tornado` (the inputs not read are in as
    exact zeros); M3 at `single`, M1, M2 and M4a at the short window."""
    return {'OT1': {(r['schedule'], 'single', (('headline', r['headline']), ('input', r['input'])), None): np.array([0.0, r['low'], r['high']])
                    for r in rows if r['horizon'] == HORIZON[r['headline']]}}


def tolabel(tol, margin):
    """The `by` values of OF1's two rule axes, e.g. ('tol_0p05', 'm10')."""
    return 'tol_' + f'{tol:g}'.replace('.', 'p'), f'm{round(100 * margin)}'


def of1(pts):
    """OF1: {'OF1': {(None, horizon, by, line): [F1, M2, M4a per path]}} from `sweeps.feasibility`'s points, one cell per schedule-grid point, rule (tolerance, margin) and line;
    `by` is schedule_grid, w_min, tolerance and margin. F1 is 0 or 100 per path, so its mean is the share closed."""
    cell = {}
    for p in pts:
        for (tol, m, hz), v in p['paths'].items():
            by = (('margin', tolabel(tol, m)[1]), ('schedule_grid', p['schedule_grid']), ('tolerance', tolabel(tol, m)[0]), ('w_min', p['w_min']))
            for ln in ('F1', 'M2', 'M4a'):
                cell[None, hz, by, ln] = v[ln]
    return {'OF1': cell}


def ck1(res):
    """CK1: {'CK1': {(schedule, 'short', (('amplitude', 'A<a>'),), line): [value]}} from `sweeps.stress` (the schedule key is None: the check is not per named schedule); P3 is
    the shortfall from year 1 to the end of the short window (transition plus short), amplitude 0 included, whatever its value."""
    return {'CK1': {(None, 'short', (('amplitude', f'A{a:g}'),), ln): np.array([v[ln]], float) for a, v in res.items() for ln in ('P1', 'P3', 'P7b')}}
