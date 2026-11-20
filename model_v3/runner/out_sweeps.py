"""
out_sweeps.py -- output group: the sweep-owned ids O1e and OT1 and the pack's data facts DH1a and DH1b (brief 088c)
====================================================================================================================
Interface: see groups.py. `per_path` and `cells` stay empty: O1e and OT1 are sweep results, not per-path cells, so the run script (057c) runs `sweeps.breakeven_return` and
`sweeps.tornado`, formats them with `o1e` and `ot1` and puts their cells into Samples next to `samples(...)`; they come back keyed as Samples are, (schedule, horizon, by, line), the schedule already in
front. DH1a and DH1b read the pack only, through `static(env)` (schedule None, `once_not_per_schedule`). Imports core/pack only (the sweeps are in the runner layer: the run script passes their results in).
"""

import numpy as np

from model_v3.core import pack as pk

NAME = 'sweeps'
IDS = ('DH1a', 'DH1b', 'O1e', 'OT1')
HORIZON = {'M1': 'short', 'M2': 'short', 'M4a': 'short', 'M3': 'single'}     # OT1 is single horizon: M3 has one, the others are read at the short window


def per_path(raw, env, again):
    """Nothing per path (see the module note)."""
    return {}


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
