"""
runner.py -- the two-level run (model v3, stage V3-10)
=====================================================
Layer L4 (architecture.md 5.1). Imports numpy, the core modules and `groups` (the output groups, brief 084c); no file is read and nothing runs at import (R8). No country or tax is named
here (R11): the pack, the register, the lever file, the tier 1 list and the manifest's output ids arrive as arguments (the payer-side taxes are in the lever file).

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
from model_v3.core import support as U
from model_v3.runner import arm as ab, flow_switches as fsw, switches as sw
from model_v3.runner.groups import GROUPS
from model_v3.runner.pool import pmap

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
    ids: frozenset         # the manifest's output ids: what `samples` accepts
    once: frozenset        # the ids the manifest marks `once_not_per_schedule`: the only ids a group's `static` may return
    centre: dict           # id -> central value, for every id the run reads or draws
    rec: dict              # retired taxes' receipts, ascending (revenue.taxes)
    bill: np.ndarray
    income: np.ndarray
    gdp0: float
    exp: float
    gdp_g: float
    cache: dict
    arm: object = 'legacy'  # 'legacy' or 'household' (arm.build: a dict names the scenario): read by core_run


@dataclass(frozen=True)
class Level2:
    inputs: dict           # id -> (N2,) the draws
    samples: dict          # output id -> {key: (N2,)}, the mean over each draw's paths
    specs: tuple           # schedule names in the order run


class RunnerError(ValueError):
    """An input the run needs is missing or a draw left its admissible region."""


def context(pack, reg, levers, tier1, manifest_ids, once=()):
    mp = levers['pack_mappings']
    ids = dict.fromkeys([*tier1, *RET.values(), *SHAPE, *RUN])
    miss = [i for i in ids if i not in reg or reg[i].central is None]
    if miss:
        raise RunnerError(f'register rows missing or without a central value: {miss}')
    one = lambda ds, **w: pk.lookup(pack, ds, **w)[0]
    bill, income = bd.pack_deciles(pack)
    gdp_g = float(np.mean(rv.gdp_growth(pack, rt.real_series(pack)[0])))
    return Ctx(pack, reg, mp, tuple(tier1), frozenset(manifest_ids), frozenset(once), {i: float(reg[i].central) for i in ids}, rv.taxes(pack, mp['x2']['lines'], mp['parts']), bill, income,
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


@dataclass(frozen=True)
class Env:
    """What a group reads besides `Raw`: `ctx`, `theta` (a draw's inputs), the `pack`, the lambdas `lam`, `arm(base)` (the run's arm for a base) and `rng(name)`: a Generator from the run stream's SeedSequence plus `key` and a hash of the name; it draws nothing."""
    ctx: object
    theta: dict
    pack: object
    lam: dict
    seq: object
    key: tuple
    arm: object = None                                                                      # base -> the run's `arm.Arm` (the layer-3.5 groups cannot import arm.py), 126c

    def rng(self, name):
        h = int.from_bytes(hashlib.sha256(name.encode()).digest()[:4], 'big')
        return np.random.default_rng(np.random.SeedSequence(entropy=self.seq.entropy, spawn_key=(*self.seq.spawn_key, *self.key, h)))


def env_of(ctx, theta, seq=None, key=()):
    return Env(ctx, theta, ctx.pack, dict(lam_C=theta['I-D14a'] / 100, lam_D=theta['I-D14b'] / 100, **sw.lien_kw(ctx)), np.random.SeedSequence(0) if seq is None else seq, tuple(key), lambda b: ab.build(ctx.arm, ctx, theta, b))


@dataclass(frozen=True)
class Raw:
    """The core results of one schedule on one block of paths, as the output groups read them: the shaped base and rate, the burden run's line flows, the receipts (`run`), revenue.py's result `r`, the
    per-horizon window bounds `lo` and `hi` (1-based years), `ok` (the reserve fills), the retired taxes' incidence `inc`, the paths, the consumption share, the horizon and the arm's run record `arm`."""
    spec: dict
    base: object
    rate: object
    fl: dict
    run: dict
    r: dict
    lo: dict
    hi: dict
    ok: np.ndarray
    inc: np.ndarray
    g: np.ndarray
    gdp_g: np.ndarray
    c: float
    h: int
    arm: dict = None


def core_run(ctx, theta, spec, g, gdp_g, full=False, tweak=None):
    """One schedule (`spec`) on the paths g (T, P): the core modules run once, kept raw, under the arm `ctx.arm`. `full` takes the receipts from revenue.run_lines (the same numbers, a test); `tweak` maps the base."""
    g, gdp_g = np.asarray(g, float), np.asarray(gdp_g, float)
    P = g.shape[1]
    b = (tweak or (lambda x: x))(shaped(ctx, theta, spec['ratio']))
    rate = sc.rate_function(spec['k_ln'], spec['tau_0'], spec['tau_m'], b.w_min, 'logistic_ln')
    lam, ar = {**env_of(ctx, theta).lam, **sw.phase_kw(ctx.arm)}, ab.build(ctx.arm, ctx, theta, b, g, gdp_g)
    fl = bd.line_flows(b, rate, g, gdp_g, c := ar.c, hook=ar.make(), **lam)
    if full or ar.name != 'legacy':                                   # the household arm needs the ledger: revenue.run_lines
        run = rv.run_lines(b, rate, g, gdp_g, c, hook=ar.make(), **lam)
    else:
        net, z = np.einsum('tnp,n->tp', fl['net'], fl['wt']) * fl['adults_k'], np.zeros((T, P))
        run = dict(tax=net, refund=z, death_tax=z, heir=z, death_B=z, death_D=z, payers=z, entries=z, exits=z, fall_through=z, gdp_index=np.cumprod(1.0 + gdp_g, axis=0),
                   adults_k=fl['adults_k'])
    h, ms = int(theta['I-D14e']), theta['I-D8a']
    r = rv.revenue(run, ctx.gdp0, theta['I-D7a'], ctx.rec, g, ctx.exp, c, int(theta['I-D14d']), ms, ms, h, ar.safe(T, P), theta['I-D14f'] / 100)
    fill, ok, one = r['fill'], ~r['unfilled'], np.ones(P, int)
    lo = {'transition': one, 'short': fill + 1, 'long': 51 * one}
    hi = {'transition': np.where(ok, fill, T), 'short': fill + h, 'long': T * one}
    inc = bd.incidence(patched(ctx, theta), list(ctx.rec), ctx.mp['parts'], ctx.mp['payer_taxes'])
    return Raw(spec, b, rate, fl, run, r, lo, hi, ok, inc, g, gdp_g, c, h, ar.label)


def headlines(raw, ctx, theta):
    """Per-path results of the headline ids: M1 to M1d, M2 (by band), M4a (by decile), neg and P3h (each by horizon), M3, P1, P7b, fill, unfilled, long_T."""
    r, lo, hi, ok, fl = raw.r, raw.lo, raw.hi, raw.ok, raw.fl
    gate = lambda k, v: np.where(ok, v, np.nan) if k == 'short' else v
    win = lambda x, k: gate(k, rv.window_mean(x, r['gdp'], lo[k], hi[k]))
    ex, t = np.maximum(0.0, r['M1d'] - r['relief']), np.arange(1, T + 1)[:, None]
    out = {x: {k: win(r[x], k) for k in HORIZONS} for x in ('M1', 'M1a', 'M1b', 'M1c', 'M1d')}
    out['M2'] = {k: {b_: gate(k, v) for b_, v in bd.m2(fl, lo[k], hi[k]).items()} for k in HORIZONS}
    out['M4a'] = {k: {d: gate(k, v) for d, v in bd.m4(r['P5'], hi[k], raw.inc, ctx.bill, ctx.income)['M4a'].items()} for k in HORIZONS}
    out['M3'] = bd.m3(fl, (theta['I-D11a'], theta['I-D11b'], theta['I-D11c']))
    out['neg'] = {k: np.where(np.isfinite(out['M1'][k]), out['M1'][k] < 0, False) for k in HORIZONS}
    out['P3h'] = {k: (ex * (t <= hi[k][None, :])).sum(axis=0) for k in HORIZONS}
    return {**out, 'P1': r['P1'], 'P7b': r['P7b'], 'fill': r['fill'], 'unfilled': r['unfilled'], 'long_T': r['long_year_T']}


def evaluate(ctx, theta, spec, g, gdp_g, full=False, seq=None, key=(), heads=False, only=None):
    """core_run, the headline results, then `{group.NAME: group.per_path(raw, env, again)}`; `heads` (151c) stops after the headlines; `only` (186c) names the groups to run (the rest are left out; each group draws from its own `env.rng(name)`, so a group's result does not depend on which others ran). `seq` and `key` (run stream, chunk or draw) only feed `env.rng`.
    `again(override=None, full=False, tweak=None)` is the core run with the spec changed, run once per (spec, full, tweak)."""
    env = env_of(ctx, theta, seq, key)
    raw = core_run(ctx, theta, spec, g, gdp_g := fsw.gdp(ctx.arm, theta, g, gdp_g, env.rng), full)           # 148c: the per-path GDP growth when `gdp_paths` is on; else the array as given
    if heads: return headlines(raw, ctx, theta)
    seen = {(tuple(sorted(spec.items())), full, None): raw}

    def again(over=None, full=False, tweak=None):
        sp = {**spec, **(over or {})}
        k = (tuple(sorted(sp.items())), full, tweak)
        if k not in seen: seen[k] = core_run(ctx, theta, sp, g, gdp_g, full, tweak)
        return seen[k]

    return {**headlines(raw, ctx, theta), **{m.NAME: m.per_path(raw, env, again) for m in GROUPS if only is None or m.NAME in only}}


def statics(ctx, theta, seq=None, key=()):
    """{group NAME: m.static(env)} for the groups that define it."""
    return {m.NAME: m.static(env_of(ctx, theta, seq, key)) for m in GROUPS if hasattr(m, 'static')}


def make_ev(ctx, eps, seq=None, heads=False, only=None):
    """ev(spec, over=None, g=None, key=()): `evaluate` on the common innovations eps (T, P) with the central inputs updated by `over`, or on the paths g given; `heads`: the headline keys only (151c); `only`: the named groups only (186c)."""
    def ev(spec, over=None, g=None, key=()):
        th = {**ctx.centre, **(over or {})}
        gg = paths(eps, th[RET['mean']], th[RET['sd']], th[RET['phi']]) if g is None else np.asarray(g, float)
        return evaluate(ctx, th, spec, gg, np.full(gg.shape, ctx.gdp_g), seq=seq, key=key, heads=heads, only=only)
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


def samples(by_schedule, ids, once=frozenset(), static=None):
    """Output id -> {(schedule, horizon, by, line): array} from {schedule: evaluation}. `by` is a sorted tuple of (name, value); a missing dimension is
    () and `None` stands for no line (architecture.md 2.9). Ids: O1 (five lines), O1a to O1c, O2, O3, O4a, O1f, then each group's `cells(e[NAME])`,
    {output id: {(horizon, by, line): array}}, which gets the schedule put in front. Raises when an id is not in `ids` (the manifest), not declared in the
    group's IDS, or returned by two producers. `static` (from `statics`) is {group NAME: {id: cells}}: stored with schedule None, only for ids in `once`."""
    out = {k: {} for k in ('O1', 'O1a', 'O1b', 'O1c', 'O2', 'O3', 'O4a', 'O1f')}
    owner = dict.fromkeys(out, 'runner')
    if not set(out) <= set(ids):
        raise RunnerError(f'runner ids {sorted(set(out) - set(ids))} are not in the manifest')
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
        if 'M3' in e: out['O3'][s, 'single', (), None] = e['M3']
        for m in GROUPS:
            for oid, cells in m.cells(e[m.NAME]).items():
                if oid not in ids or oid not in m.IDS:
                    raise RunnerError(f'{m.NAME}: output id {oid} is not in the manifest and in the group\'s IDS')
                if owner.setdefault(oid, m.NAME) != m.NAME:
                    raise RunnerError(f'output id {oid} is returned by {owner[oid]} and by {m.NAME}')
                out.setdefault(oid, {}).update({(s, *k): v for k, v in cells.items()})
    for name, cells in (static or {}).items():
        for oid, cs in cells.items():
            m = next((g for g in GROUPS if g.NAME == name), None)
            if oid not in ids or m is None or oid not in m.IDS or oid not in once:
                raise RunnerError(f'{name}: static output id {oid} is not in the manifest, in the group\'s IDS and once_not_per_schedule')
            if owner.setdefault(oid, name) != name:
                raise RunnerError(f'output id {oid} is returned by {owner[oid]} and by {name}')
            out.setdefault(oid, {}).update({(None, *k): v for k, v in cs.items()})
    return out


def level1(ctx, specs, rng, n=N1, chunk=CHUNK, theta=None, workers=1, cap=None):
    """Level 1: n paths per schedule in chunks, the same paths for every schedule. Returns (Samples, {'paths', 'unfilled_paths': {schedule: count}}). The chunks' paths are drawn here in order (the
    serial stream) and the evaluations of (chunk, schedule) go through `pmap` (154c): the result does not depend on `workers`. `cap` is the caller's `support.capping` store: a shortfall met in a unit comes back with
    it and is merged in chunk order, the first record standing as in the serial run."""
    th, seq = theta or ctx.centre, rng.bit_generator.seed_seq
    gs = [rt.ar1_paths(rng, th[RET['mean']], th[RET['sd']], th[RET['phi']], T, min(chunk, n - a)) for a in range(0, n, chunk)]
    jobs = [(i, s) for i in range(len(gs)) for s in specs]   # one unit per (chunk, schedule), in the serial order: 3 per chunk, 30 per grid point at final size
    def unit(j):
        rec = {} if cap is not None else None
        with U.capping(rec):
            return evaluate(ctx, th, specs[j[1]], gs[j[0]], np.full(gs[j[0]].shape, ctx.gdp_g), seq=seq, key=(j[0],)), rec
    outs = pmap(unit, jobs, workers)
    for _, rec in outs:
        for k, v in (rec or {}).items(): cap.setdefault(k, v)
    ev = {s: cat([o for j, (o, _) in zip(jobs, outs) if j[1] == s]) for s in specs}
    return samples(ev, ctx.ids, ctx.once, statics(ctx, th, seq)), {'paths': n, 'unfilled_paths': {s: int(e['unfilled'].sum()) for s, e in ev.items()}}


def level2(ctx, specs, rng, n=N2, n_paths=N2P):
    """Level 2: n Latin hypercube draws of every tier 1 input, each run on n_paths common random paths for every schedule."""
    draws = draw_theta(rng, ctx, ctx.tier1, n)
    eps = rng.standard_normal((T, n_paths))
    seq = rng.bit_generator.seed_seq
    acc, ev, st = {s: [] for s in specs}, make_ev(ctx, eps, seq), []
    for i in range(n):
        over = {k: float(v[i]) for k, v in draws.items()}
        for s, spec in specs.items():
            acc[s].append(mean_of(ev(spec, over, key=(i,))))
        st.append(mean_of(statics(ctx, {**ctx.centre, **over}, seq, (i,))))
    return Level2(draws, samples({s: cat(a) for s, a in acc.items()}, ctx.ids, ctx.once, cat(st)), tuple(specs))


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
