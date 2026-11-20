"""
runner.py -- the two-level run (model v3, stage V3-10)
=====================================================
Layer L4 (architecture.md 5.1). Imports numpy and the core modules; no file is read and nothing runs at import (R8). No country or tax is named
here (R11): the pack, the register, the lever file, the tier 1 list and the payer-side taxes arrive as arguments.

TWO LEVELS (architecture.md 2.8, 3.1; stage-c-decisions items 4, 6, 7)
----------------------------------------------------------------------
Level 1: for fixed inputs (every register row at its central value), N1 paths of the AR(1) generator, in chunks of CHUNK paths folded into the kernel's
line axis, each named schedule on the same paths. Level 2: N2 Latin hypercube draws of every tier 1 input, each with N2P paths on common random numbers
(the same standard normal innovations for every draw and schedule); each result is the mean over the draw's paths, so the P10 to P90 of a Level2 array is
the range of the level 1 mean. `Samples` (level 1) and `Level2` are separate objects: the first holds one entry per path, the second one per draw.

WHAT A HEADLINE READS
---------------------
Paths are real arithmetic returns (returns.py) with a constant real GDP-per-head growth, the mean of the pack's own history (no register row holds one).
Horizons are per path: transition = years 1 to the fill year (to the last year if the reserve never fills); short = the `horizon` years after it (nan
for a path that never fills); long = years 51 to 100. M1 is a ratio of sums over the window; M2 (in life) and M4a are read over the same window; M3
is over the first generation. Everything else (taxes retired, fund) is revenue.py's. The kernel is run once through burden.line_flows; the wealth
tax receipts it gives equal revenue.run_lines' (a test), so M1 is built from them and the second run is left for `full=True`.

INPUTS THE RUN READS (everything else stays central; see READ and `reads`)
---------------------------------------------------------------------------
Return mean, SD and lag-1 (I-D1a, I-D1b, I-D1b2): the generator. Wealth over GDP (I-D4a): every line's wealth scaled by the draw over the central.
Loss of base to behaviour (I-D5a): the wealth of the lines at or above the threshold at launch is scaled by one minus it. The incidence shares that
have a pack row (the lever file's pointers into the household incidence table): the by-decile M4a at level 2. A tier 1 input with none of these is drawn
and reaches no headline of this stage; its tornado swing is exactly zero and it is not run. That includes the incidence shares, which move a tax's pounds
between deciles and leave the overall M4a unchanged.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, replace

import numpy as np

from model_v3.core import base as bs
from model_v3.core import burden as bd
from model_v3.core import pack as pk
from model_v3.core import returns as rt
from model_v3.core import revenue as rv
from model_v3.core import schedule as sc

T = 100
N1, N2, N2P, CHUNK = 10_000, 200, 1_000, 1_000
HORIZONS = ('transition', 'short', 'long')
RET = {'mean': 'I-D1a', 'sd': 'I-D1b', 'phi': 'I-D1b2'}
SHAPE = ('I-D4a', 'I-D5a')
RUN = ('I-D14a', 'I-D14b', 'I-D14c', 'I-D14d', 'I-D14e', 'I-D14f', 'I-D7a', 'I-D8a', 'I-D11a', 'I-D11b', 'I-D11c')
Z90 = 1.2815515655446004
TAIL = 0.0013498980316301     # the normal probability beyond three standard deviations: the quantile map of draw_theta stops at plus and minus three


@dataclass(frozen=True)
class Ctx:
    pack: object
    reg: dict
    mp: dict               # the lever file's pack_mappings
    tier1: tuple           # ids drawn at level 2 and swung by the tornado
    payer_taxes: tuple     # retired taxes that fall on payers, not on the non-payers (given by the caller)
    centre: dict           # id -> central value, for every id the run reads or draws
    rec: dict              # retired taxes' receipts, ascending (revenue.taxes)
    bill: np.ndarray
    income: np.ndarray
    gdp0: float
    exp: float
    gdp_g: float
    cache: dict


@dataclass(frozen=True)
class Level2:
    inputs: dict           # id -> (N2,) the draws
    samples: dict          # output id -> {key: (N2,)}, the mean over each draw's paths
    specs: tuple           # schedule names in the order run


class RunnerError(ValueError):
    """An input the run needs is missing or a draw left its admissible region."""


def context(pack, reg, levers, tier1, payer_taxes):
    mp = levers['pack_mappings']
    ids = dict.fromkeys([*tier1, *RET.values(), *SHAPE, *RUN])
    miss = [i for i in ids if i not in reg or reg[i].central is None]
    if miss:
        raise RunnerError(f'register rows missing or without a central value: {miss}')
    one = lambda ds, **w: pk.lookup(pack, ds, **w)[0]
    bill, income = bd.pack_deciles(pack)
    gdp_g = float(np.mean(rv.gdp_growth(pack, rt.real_series(pack)[0])))
    return Ctx(pack, reg, mp, tuple(tier1), tuple(payer_taxes), {i: float(reg[i].central) for i in ids}, rv.taxes(pack, mp['x2']['lines'], mp['parts']), bill, income,
               one('wealth_distribution', variable='gdp', band='all')['value'], one('public_expenditure', function='total')['pct_gdp'], gdp_g, {})


def reads(ctx):
    """Ids the tornado must run: the generator's three and the two that shape the base. The incidence shares only move a retired tax's pounds between
    income deciles, so the overall M4a does not change with them (the by-decile O4a does, at level 2); they are patched into the pack, not run."""
    return (set(RET.values()) | set(SHAPE)) & set(ctx.tier1)


def draw_theta(rng, ctx, ids, n):
    """n Latin hypercube draws of each id, {id: (n,)}: the register's low, central and high are the 10th, 50th and 90th percentiles. The three return
    rows go through returns.level2_draw; the others map a normal quantile with the spread of the side the draw falls on, within three standard deviations (the Latin hypercube is
    laid over that range, so no tier 1 row leaves its physical range). A row whose low is zero has a
    floor there: its 10th percentile can only be met by a tenth of the draws at the floor, so those draws are zero. Any other negative draw of a row
    whose low is not negative raises (not clipped)."""
    ids = list(ids)
    out = rt.level2_draw(rng, {k: ctx.reg[i] for k, i in RET.items()}, n)
    out = {RET[k]: v for k, v in out.items()}
    for i in ids:
        if i in out:
            continue
        r = ctx.reg[i]
        z = rt._ppf(TAIL + (1 - 2 * TAIL) * (rng.permutation(n) + rng.random(n)) / n)
        out[i] = r.central + z * np.where(z > 0, r.high - r.central, r.central - r.low) / Z90
        if r.low == 0:
            out[i] = np.maximum(out[i], 0.0)
        if r.low >= 0 and (out[i] < 0).any():
            raise RunnerError(f'{i}: a draw below zero for a row whose low is {r.low}: not clipped')
    return {i: out[i] for i in ids}


def paths(eps, mean, sd, phi):
    """(T, P) real arithmetic returns from fixed standard normal innovations: the recursion of returns.ar1_paths, so the same eps gives common random numbers."""
    x = np.empty_like(eps)
    x[0] = eps[0]
    for t in range(1, len(eps)):
        x[t] = phi * x[t - 1] + np.sqrt(1 - phi * phi) * eps[t]
    return rt._checked((mean + sd * x) / 100)


def shaped(ctx, theta, ratio):
    """The base for one threshold ratio with the wealth scale (I-D4a over its central) and the behavioural loss (I-D5a, payer lines at launch) applied."""
    if ratio not in ctx.cache:
        ctx.cache[ratio] = bs.build_base(ctx.pack, ctx.reg, ratio)
    b = ctx.cache[ratio]
    k = theta['I-D4a'] / ctx.centre['I-D4a'] * np.where(b.wealth >= b.w_min, 1.0 - theta['I-D5a'] / 100.0, 1.0)
    return replace(b, wealth=b.wealth * k, wealth_bn=b.wealth_bn * k, V0={r: v * k for r, v in b.V0.items()})


def patched(ctx, theta):
    """The pack with the household incidence rows named by the lever file's pointers set to this draw's values (only where they differ from central)."""
    tabs = dict(ctx.pack.tables)
    for i, (ds, where, col) in ctx.mp['x1_pointers'].items():
        if ds == 'household_incidence' and i in theta and theta[i] != ctx.centre.get(i, theta[i]):
            tabs[ds] = [dict(r, **{col: theta[i]}) if all(r.get(k) == v for k, v in where.items()) else r for r in tabs[ds]]
    return replace(ctx.pack, tables=tabs)


def evaluate(ctx, theta, spec, g, gdp_g, full=False):
    """One schedule (`spec`: tau_0, tau_m, k_ln, ratio) on the paths g (T, P), per-path results: {'M1', 'M1a'..'M1d': {horizon: (P,)}, 'M2': {horizon: {band}},
    'M4a': {horizon: {decile}}, 'M3': (P,), 'neg': {horizon: bool}, 'P3h': {horizon: (P,)}, 'P1', 'P7b', 'fill', 'unfilled', 'long_T'}. `full` takes the
    receipts from revenue.run_lines instead of the burden run (the same numbers, a test)."""
    g, gdp_g = np.asarray(g, float), np.asarray(gdp_g, float)
    P = g.shape[1]
    b = shaped(ctx, theta, spec['ratio'])
    rate = sc.rate_function(spec['k_ln'], spec['tau_0'], spec['tau_m'], b.w_min, 'logistic_ln')
    c, lam = theta['I-D14c'] / 100, dict(lam_C=theta['I-D14a'] / 100, lam_D=theta['I-D14b'] / 100)
    fl = bd.line_flows(b, rate, g, gdp_g, c, **lam)
    if full:
        run = rv.run_lines(b, rate, g, gdp_g, c, **lam)
    else:
        net, z = np.einsum('tnp,n->tp', fl['net'], fl['wt']) * fl['adults_k'], np.zeros((T, P))
        run = dict(tax=net, refund=z, death_tax=z, heir=z, death_B=z, death_D=z, payers=z, entries=z, exits=z, fall_through=z, gdp_index=np.cumprod(1.0 + gdp_g, axis=0),
                   adults_k=fl['adults_k'])
    h, ms = int(theta['I-D14e']), theta['I-D8a']
    r = rv.revenue(run, ctx.gdp0, theta['I-D7a'], ctx.rec, g, ctx.exp, c, int(theta['I-D14d']), ms, ms, h, None, theta['I-D14f'] / 100)
    fill, ok, one = r['fill'], ~r['unfilled'], np.ones(P, int)
    lo = {'transition': one, 'short': fill + 1, 'long': 51 * one}
    hi = {'transition': np.where(ok, fill, T), 'short': fill + h, 'long': T * one}
    gate = lambda k, v: np.where(ok, v, np.nan) if k == 'short' else v
    win = lambda x, k: gate(k, rv.window_mean(x, r['gdp'], lo[k], hi[k]))
    inc = bd.incidence(patched(ctx, theta), list(ctx.rec), ctx.mp['parts'], ctx.payer_taxes)
    ex, t = np.maximum(0.0, r['M1d'] - r['relief']), np.arange(1, T + 1)[:, None]
    out = {x: {k: win(r[x], k) for k in HORIZONS} for x in ('M1', 'M1a', 'M1b', 'M1c', 'M1d')}
    out['M2'] = {k: {b_: gate(k, v) for b_, v in bd.m2(fl, lo[k], hi[k]).items()} for k in HORIZONS}
    out['M4a'] = {k: {d: gate(k, v) for d, v in bd.m4(r['P5'], hi[k], inc, ctx.bill, ctx.income)['M4a'].items()} for k in HORIZONS}
    out['M3'] = bd.m3(fl, (theta['I-D11a'], theta['I-D11b'], theta['I-D11c']))
    out['neg'] = {k: np.where(np.isfinite(out['M1'][k]), out['M1'][k] < 0, False) for k in HORIZONS}
    out['P3h'] = {k: (ex * (t <= hi[k][None, :])).sum(axis=0) for k in HORIZONS}
    return {**out, 'P1': r['P1'], 'P7b': r['P7b'], 'fill': fill, 'unfilled': r['unfilled'], 'long_T': r['long_year_T']}


def make_ev(ctx, eps):
    """ev(spec, over=None, g=None): `evaluate` on the common innovations eps (T, P) with the central inputs updated by `over`, or on the paths g given."""
    def ev(spec, over=None, g=None):
        th = {**ctx.centre, **(over or {})}
        gg = paths(eps, th[RET['mean']], th[RET['sd']], th[RET['phi']]) if g is None else np.asarray(g, float)
        return evaluate(ctx, th, spec, gg, np.full(gg.shape, ctx.gdp_g))
    return ev


def cat(parts):
    """Concatenate nested dicts of per-path arrays along the path axis."""
    if isinstance(parts[0], dict):
        return {k: cat([p[k] for p in parts]) for k in parts[0]}
    return np.concatenate(parts)


def mean_of(ev):
    """Reduce a nested evaluation to the mean over paths (nan ignored), as the level 2 draws do; boolean leaves become shares."""
    if isinstance(ev, dict):
        return {k: mean_of(v) for k, v in ev.items()}
    with np.errstate(all='ignore'):
        return np.array([np.nanmean(np.asarray(ev, float)) if np.isfinite(np.asarray(ev, float)).any() else np.nan])


def samples(by_schedule):
    """Output id -> {(schedule, horizon, by, line): array} from {schedule: evaluation}. `by` is a sorted tuple of (name, value); a missing dimension is
    () and `None` stands for no line (architecture.md 2.9). Ids: O1 (five lines), O1a to O1c, O2, O3, O4a, O1f."""
    out = {k: {} for k in ('O1', 'O1a', 'O1b', 'O1c', 'O2', 'O3', 'O4a', 'O1f')}
    for s, e in by_schedule.items():
        for hz in HORIZONS:
            for x in ('M1', 'M1a', 'M1b', 'M1c', 'M1d'):
                out['O1'][s, hz, (), x] = e[x][hz]
            for oid, x in (('O1a', 'M1a'), ('O1b', 'M1b'), ('O1c', 'M1c')):
                out[oid][s, hz, (), None] = e[x][hz]
            for band, v in e['M2'][hz].items():
                out['O2'][s, hz, (('wealth_band', band),), None] = v
            for d, v in e['M4a'][hz].items():
                out['O4a'][s, hz, (('income_decile', d),), None] = v
            out['O1f'][s, hz, (), None] = np.asarray(e['neg'][hz], float)
        out['O3'][s, 'single', (), None] = e['M3']
    return out


def level1(ctx, specs, rng, n=N1, chunk=CHUNK, theta=None):
    """Level 1: n paths per schedule in chunks, the same paths for every schedule. Returns (Samples, {'paths', 'unfilled_paths': {schedule: count}})."""
    th = theta or ctx.centre
    parts = {s: [] for s in specs}
    for a in range(0, n, chunk):
        g = rt.ar1_paths(rng, th[RET['mean']], th[RET['sd']], th[RET['phi']], T, min(chunk, n - a))
        for s, spec in specs.items():
            parts[s].append(evaluate(ctx, th, spec, g, np.full(g.shape, ctx.gdp_g)))
    ev = {s: cat(p) for s, p in parts.items()}
    return samples(ev), {'paths': n, 'unfilled_paths': {s: int(e['unfilled'].sum()) for s, e in ev.items()}}


def level2(ctx, specs, rng, n=N2, n_paths=N2P):
    """Level 2: n Latin hypercube draws of every tier 1 input, each run on n_paths common random paths for every schedule."""
    draws = draw_theta(rng, ctx, ctx.tier1, n)
    eps = rng.standard_normal((T, n_paths))
    acc, ev = {s: [] for s in specs}, make_ev(ctx, eps)
    for i in range(n):
        for s, spec in specs.items():
            acc[s].append(mean_of(ev(spec, {k: float(v[i]) for k, v in draws.items()})))
    return Level2(draws, samples({s: cat(a) for s, a in acc.items()}), tuple(specs))


def digest(s):
    """SHA-256 of a Samples (or Level2.samples) mapping, over sorted keys and the array bytes: equal for equal runs."""
    h = hashlib.sha256()
    for oid in sorted(s):
        for k in sorted(s[oid], key=repr):
            h.update(repr((oid, k)).encode())
            h.update(np.ascontiguousarray(s[oid][k], dtype=float).tobytes())
    return h.hexdigest()


def timed(f, *a, **kw):
    """(result, seconds) of one call; the run record's timing (N7)."""
    t0 = time.perf_counter()
    out = f(*a, **kw)
    return out, time.perf_counter() - t0
