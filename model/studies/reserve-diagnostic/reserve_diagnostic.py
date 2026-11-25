"""
reserve_diagnostic.py -- brief 166c: can the fund's reserves cover the gap years? Diagnosis only: no rule is recommended, nothing in model_v3 changes.
==========================================================================================================================================================
A one-off measurement, not part of model_v3 (its layer and budget rules do not apply). It imports the runner and the core read-only, and imports 140c's script (`model/studies/f1-household/f1_household.py`)
for its setup, scenario points and `closed`. The household arm runs 10 death phases by default now (149c's ruling, `switches.N_PHASE`); the one 6-phase check wraps `burden.line_flows` and `revenue.run_lines`
for the length of a run (`phases(n)`, a runtime wrapper: no file is edited; 149c's own wrapper adds `n_phase` and now clashes with the runner's).

The kernel (`runner.core_run`) runs ONCE per (fund, scenario point, schedule, paths). Everything that follows the fund (relief, M1d, the windows) is recomputed by `revenue.revenue` on the same receipts with
`revenue.fund` replaced for the length of the call by a labelled copy (`fund_copy`) that separates the payout window `w_pay` from the reserve multiple `ml` (the core uses one number for both) and can top up a gap year.
Variants (all labelled scenarios, none a rule of the model):
    core      the core's own fund (`w_pay` = ml = 3, a_window 5): the reference.
    copy_w3   the copy at w_pay 3: must equal `core` to 1e-9 on every output (block `check`, and asserted on every cell of `d`).
    w5, w10, w15   the copy with the payout averaged over the last 5, 10, 15 post-fill years (reserve multiples stay 3, I-D8a).
    a10       a_window 10 (I-D14d's high) with w_pay 3.
    topup     relief R = min(max(R*, M1d of the taxes already retired, in billions), S_pre minus the short reserve): a gap year is topped up from what the fund holds above the short reserve target.
Household arm, 10 death phases (149c), schedules tau_m 0.5, 0.7, 0.9 (k_ln 1, ratio 0.5), the five scenario points, funds `safe` and `market`.

Run from the repository root (python -I):
    python -I model/studies/reserve-diagnostic/reserve_diagnostic.py check                 the 6-phase check against 140c, and the fund-copy check on one cell (about 1 minute)
    python -I model/studies/reserve-diagnostic/reserve_diagnostic.py a [--phases 10]        part A: the accounting on the constant path, CSVs next to the script (a_accounting_*_10ph.csv; run again with --phases 6 for the 140c count)
    python -I model/studies/reserve-diagnostic/reserve_diagnostic.py d [--n 200] [--seed 20261118] [--points a,b] [--funds safe,market] [--time]
                                                                                           parts B, C, D: every variant on the constant path and on n level 1 paths, CSVs next to the script
Progress goes to stderr; two runs with the same arguments print identical text.
"""
from __future__ import annotations

import argparse
import csv
import sys
import time
from contextlib import contextmanager
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'docs' / 'model-v3' / 'f1-household'))

import f1_household as F  # noqa: E402  (140c: setup, point_ctx, closed, lab, tab, write_csv, paths_of)

R, rv, T, CLOSED = F.R, F.rv, F.T, F.CLOSED
SPECS = F.CONST_SPECS                                   # tm50, tm70, tm90 at k_ln 1, ratio 0.5
POINTS = tuple(F.POINTS)                                # min_mid, median_mid, max_mid, median_low, median_high
FUNDS = F.FUNDS
VARIANTS = ('core', 'copy_w3', 'w5', 'w10', 'w15', 'a10', 'topup')
YEARS = (10, 25, 50, 100)
TOL_RELAXED, MARGIN_RELAXED = 1.0, 0.25                 # the 140c grid cell "tolerance 1, margin 25%" (tolerance in GDP-points summed over years)


def log(*a):
    print(*a, file=sys.stderr, flush=True)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def fund_copy(net, E, r, ms=3.0, ml=3.0, a_window=5, safe=None, safe_share=0.0, unfilled_after=90, led=None, w_pay=None, topup=None):
    """A copy of `revenue.fund` (model/model_v3/core/revenue.py) with two labelled additions, nothing else changed. `w_pay`: the years of the payout average R* (default `ml`, as the core). `topup`
    {'gdp': (T, P) billions, 'rec': receipts of the retired taxes in ascending order, percent of GDP}: the relief of a year is max(R*, M1d of the taxes already retired at the start of the year) before the
    cap by what is available above the short reserve. The taxes retire by the existing trigger (`revenue.retire`'s rule, replayed here per year on the relief paid)."""
    net = np.asarray(net, float)
    T, P = net.shape
    if led is None:
        r = np.asarray(r, float)
    if led is None and safe_share > 0.0:
        if safe is None:
            raise ValueError('safe returns are needed when safe_share > 0')
        r = (1.0 - safe_share) * r + safe_share * np.asarray(safe, float)
    w = max(1, int(round(ml if w_pay is None else w_pay)))
    c = np.vstack([np.zeros((1, P)), np.cumsum(np.maximum(net, 0.0), axis=0)])
    i = np.arange(1, T + 1)[:, None]
    lo = np.maximum(0, i - max(1, int(a_window)))
    A = (c[i, np.arange(P)] - c[lo, np.arange(P)]) / (i - lo)
    S, Sp = np.zeros((T, P)), np.zeros(P)
    R, Z = np.zeros((T, P)), np.zeros((T, P))
    fill, srr_fill = np.zeros(P, int), np.zeros(P, int)
    ev = {k: np.zeros(P, int) for k in ('unmet', 'ring', 'insolvent')}
    if led is not None:
        Lk, cl, ret, pay, r = {k: np.zeros(P) for k in led['rc']}, {}, {}, {}, np.zeros((T, P))
        for d in (cl, ret, pay):
            d.update({k: np.zeros((T, P)) for k in Lk})
    if topup is not None:
        rec = np.asarray(topup['rec'], float)
        done_tax = np.zeros((P, len(rec)), bool)
    for t in range(T):
        tsrr, ttot = ms * A[t], (ms + ml) * A[t]
        gro = Sp * (1.0 + r[t]) if led is None else sum(Lk[k] * (1.0 + led['rk'][k][t]) for k in Lk)
        pre = gro + net[t]
        srr_fill = np.where((srr_fill == 0) & (A[t] > 0) & (pre >= tsrr), t + 1, srr_fill)
        done = fill > 0
        newly = ~done & (A[t] > 0) & (pre >= ttot)
        Z[t] = np.where(done, net[t] - np.maximum(0.0, ttot - gro), 0.0)
        lo_t = np.maximum(fill, t - w + 1)
        cz = np.cumsum(np.vstack([np.zeros((1, P)), Z[:t + 1]]), axis=0)
        k = np.maximum(t + 1 - lo_t, 1)
        rstar = np.where(done, np.maximum(0.0, (cz[t + 1, np.arange(P)] - cz[lo_t, np.arange(P)]) / k), 0.0)
        avail = np.maximum(0.0, pre - tsrr)
        for name, m in (('unmet', rstar > avail + 1e-12), ('ring', pre < tsrr - 1e-12), ('insolvent', pre < -1e-12)):
            ev[name] = np.where(done & (ev[name] == 0) & m, t + 1, ev[name])
        want = rstar
        if topup is not None:
            want = np.maximum(rstar, (done_tax * rec).sum(axis=1) / 100.0 * topup['gdp'][t])
        R[t] = np.where(done, np.minimum(want, avail), 0.0)
        if topup is not None:                                                    # replay revenue.retire for this year on the relief paid (percent of GDP)
            rel = 100.0 * R[t] / topup['gdp'][t]
            live = (fill > 0) & (t + 1 > fill)
            for j in range(len(rec)):
                cover = rel - (done_tax * rec).sum(axis=1) >= rec[j]
                go = live & ~done_tax[:, j] & cover & (done_tax[:, :j].all(axis=1) if j else True)
                done_tax[:, j] |= go
        if led is None:
            Sp = pre - R[t]
        else:
            r[t] = np.where(Sp > 0, sum(Lk[k] * led['rk'][k][t] for k in Lk) / np.where(Sp > 0, Sp, 1.0), 0.0)
            for k in Lk:
                ret[k][t], lp = Lk[k] * led['rk'][k][t], Lk[k] * (1.0 + led['rk'][k][t]) + led['rc'][k][t]
                pay[k][t] = np.where(pre > 0, R[t] * lp / np.where(pre > 0, pre, 1.0), 0.0)
                Lk[k], cl[k][t] = lp - pay[k][t], lp - pay[k][t]
            Sp = sum(Lk.values())
        S[t] = Sp
        fill = np.where(newly, t + 1, fill)
    unfilled = (fill == 0) | (fill > unfilled_after)
    return {'S': S, 'R': R, 'A': A, 'rr': r, 'srr': ms * A, 'fill': fill, 'srr_fill': srr_fill, 'unfilled': unfilled, **{k + '_year': v for k, v in ev.items()}, **({} if led is None else {'L': cl, 'ret': ret, 'pay': pay, 'rc': led['rc'], **({'rec': led['rec']} if 'rec' in led else {})})}


@contextmanager
def fund_as(**kw):
    """`revenue.fund` is the copy with `kw` for the length of the `with` (a runtime wrapper, as 149c's `phases`); restored after."""
    orig = rv.fund
    rv.fund = lambda net, E, r, ms=3.0, ml=3.0, a_window=5, safe=None, safe_share=0.0, unfilled_after=90, led=None: fund_copy(net, E, r, ms, ml, a_window, safe, safe_share, unfilled_after, led, **kw)
    try:
        yield
    finally:
        rv.fund = orig


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@contextmanager
def phases(n):
    """Run the kernel with n death phases: `burden.line_flows` and `revenue.run_lines` get n_phase = n (the runner already passes the household arm's 10, so the wrapper overrides it); restored after."""
    bd = F.bd
    lf, rl = bd.line_flows, rv.run_lines
    bd.line_flows = lambda *a, **k: lf(*a, **{**k, 'n_phase': n})
    rv.run_lines = lambda *a, **k: rl(*a, **{**k, 'n_phase': n})
    try:
        yield
    finally:
        bd.line_flows, rv.run_lines = lf, rl


def run_kernel(cp, spec, g, n_phase):
    """The kernel once: `runner.core_run` at central inputs, with n_phase death phases. Returns Raw (its `run` holds the receipts every variant reuses)."""
    g = np.asarray(g, float)
    with phases(n_phase):
        raw = R.core_run(cp, cp.centre, spec, g, np.full(g.shape, cp.gdp_g))
    assert raw.fl['net'].shape[1] == len(raw.base.labels) * n_phase, 'the phase count did not reach the kernel'
    return raw


def variant_run(cp, raw, name):
    """revenue.revenue on the kernel's receipts with the fund of variant `name`. `core` is revenue.revenue untouched."""
    th = cp.centre
    ms, h, aw = th['I-D8a'], int(th['I-D14e']), int(th['I-D14d'])
    safe = R.ab.build(cp.arm, cp, th, raw.base, raw.g, raw.gdp_g).safe(T, raw.g.shape[1])
    kw = {'core': None, 'copy_w3': dict(w_pay=ms), 'w5': dict(w_pay=5), 'w10': dict(w_pay=10), 'w15': dict(w_pay=15), 'a10': dict(w_pay=ms), 'topup': dict(w_pay=ms, topup=dict(gdp=raw.r['gdp'], rec=list(cp.rec.values())))}[name]
    aw = 10 if name == 'a10' else aw
    args = (raw.run, cp.gdp0, th['I-D7a'], cp.rec, raw.g, cp.exp, raw.c, aw, ms, ms, h, safe, th['I-D14f'] / 100)
    if kw is None:
        return rv.revenue(*args)
    with fund_as(**kw):
        return rv.revenue(*args)


def flat(x, pre=''):
    """Every numeric array of a nested result, by key."""
    if isinstance(x, dict):
        for k, v in x.items():
            yield from flat(v, f'{pre}{k}.')
    elif isinstance(x, (np.ndarray, float, int, bool, np.floating, np.integer, np.bool_)):
        yield pre[:-1], np.asarray(x)


def max_diff(a, b):
    """The largest absolute difference over every numeric output of two revenue results (nan equal to nan, inf to inf); also the count of outputs compared."""
    worst, n = 0.0, 0
    fb = dict(flat(b))
    for k, v in flat(a):
        w = fb[k]
        assert v.shape == w.shape, k
        v, w = v.astype(float), w.astype(float)
        same = (v == w) | (np.isnan(v) & np.isnan(w))
        if not same.all():
            worst = max(worst, float(np.max(np.abs(np.where(same, 0.0, v - w)))))
        n += 1
    return worst, n


def window(r, fl, h, x):
    ok = ~r['unfilled']
    return np.where(ok, rv.window_mean(r[x], r['gdp'], fl + 1, fl + h), np.nan)


def p3_margin(cp, r, h, m):
    """P3 from year 1 to the end of the short window (140c's `with_margin`): retirement on relief / (1 + m), the excess measured against the true relief. Returns (p3, m1d)."""
    fl = r['fill']
    m1d, _ = rv.retire(r['relief'] / (1.0 + m), fl, cp.rec)
    t = np.arange(1, T + 1)[:, None]
    return (np.maximum(0.0, m1d - r['relief']) * (t <= (fl + h)[None, :])).sum(axis=0), m1d


def se_mean(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    return float(x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 1 else float('nan')


def mean(x):
    x = np.asarray(x, float)
    return float(np.nanmean(x)) if np.isfinite(x).any() else float('nan')


def summarise(cp, r):
    """The columns of part D for one variant's revenue result over P paths."""
    h, fl, P = int(cp.centre['I-D14e']), r['fill'], r['fill'].shape[0]
    ok = ~r['unfilled']
    p3a, _ = p3_margin(cp, r, h, 0.0)
    p3b, _ = p3_margin(cp, r, h, MARGIN_RELAXED)
    f1a, f1b = F.closed(p3a, 0), F.closed(p3b, TOL_RELAXED)
    se = lambda f: 100.0 * float(np.sqrt(f / 100.0 * (1 - f / 100.0) / P))
    p7b = np.where(np.isfinite(r['P7b']) & ok, r['P7b'], np.nan)
    row = dict(F1_strict=f1a, F1_strict_se=se(f1a), F1_relaxed=f1b, F1_relaxed_se=se(f1b), P3_strict_mean=mean(p3a), P1=mean(np.where(ok, r['P1'], np.nan)), unfilled_pct=100 * float(np.mean(~ok)),
               P7a_pct=100 * float(np.mean(r['P7a'])), P7a_se=se(100 * float(np.mean(r['P7a']))), P7b_mean=mean(p7b), P7b_se=se_mean(p7b), P7b_min=float(np.nanmin(p7b)) if np.isfinite(p7b).any() else float('nan'))
    for x in ('M1a', 'M1b', 'M1c', 'M1d', 'M1'):
        w = window(r, fl, h, x)
        row[x + '_short'], row[x + '_short_se'] = mean(w), se_mean(w)
    for y in YEARS:
        row[f'P6_y{y}'], row[f'P6_y{y}_se'] = mean(np.where(ok, r['P6'][y], np.nan)), se_mean(np.where(ok, r['P6'][y], np.nan))
    return row


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def const_path(ctx):
    return np.full((T, 1), ctx.centre['I-D1a'] / 100.0)


def accounting(cp, r, point, fund, spec, n_phase):
    """Part A for one constant-path run: the year rows and the summary row. Units: percent of GDP unless named; `idle` = fund S minus the short reserve (`srr`), `idle_total` = S minus both targets."""
    rel, m1d, gdp = r['relief'][:, 0], r['M1d'][:, 0], r['gdp'][:, 0]
    f = r['fund']
    S, srr, A = f['S'][:, 0], f['srr'][:, 0], f['A'][:, 0]
    ms = cp.centre['I-D8a']
    sf = np.maximum(0.0, m1d - rel)
    idle, idle_tot = 100 * (S - srr) / gdp, 100 * (S - 2 * ms * A) / gdp
    fy, hi = int(r['fill'][0]), int(r['fill'][0]) + int(cp.centre['I-D14e'])
    below = np.where((m1d > CLOSED) & (rel < m1d - CLOSED))[0]
    rows = [(fund, point, F.lab(spec), n_phase, y + 1, f'{rel[y]:.4f}', f'{m1d[y]:.4f}', f'{sf[y]:.4f}', f'{r["S_gdp"][y, 0]:.4f}', f'{idle[y]:.4f}', f'{idle_tot[y]:.4f}') for y in range(fy, T)]
    p3 = float(sf[:hi].sum())
    summ = dict(fund=fund, point=point, schedule=F.lab(spec), phases=n_phase, fill_year=fy, end_short_window=hi, first_shortfall_year=int(below[0]) + 1 if below.size else 0,
                years_with_shortfall=int((sf > CLOSED).sum()), P3_short=p3, P3_100=float(sf.sum()))
    if below.size:
        j, jm = int(below[0]), int(sf.argmax())
        summ.update(shortfall_first=float(sf[j]), idle_first=float(idle[j]), idle_to_shortfall_first=float(idle[j] / sf[j]), idle_total_first=float(idle_tot[j]),
                    largest_shortfall=float(sf[jm]), largest_year=jm + 1, idle_at_largest=float(idle[jm]), idle_to_shortfall_largest=float(idle[jm] / sf[jm]))
    else:
        summ.update(shortfall_first=0.0, idle_first=float('nan'), idle_to_shortfall_first=float('nan'), idle_total_first=float('nan'), largest_shortfall=0.0, largest_year=0, idle_at_largest=float('nan'),
                    idle_to_shortfall_largest=float('nan'))
    summ['idle_at_window_start'] = float(idle[fy - 1]) if fy > 0 else float('nan')           # S minus srr at the end of the fill year = the start of the short window
    summ['P3_short_to_idle_at_start'] = p3 / summ['idle_at_window_start'] if fy > 0 and summ['idle_at_window_start'] > 0 else float('nan')
    return rows, summ


SUMM_HEAD = ('fund', 'point', 'schedule', 'phases', 'fill_year', 'end_short_window', 'first_shortfall_year', 'years_with_shortfall', 'P3_short', 'P3_100', 'shortfall_first', 'idle_first', 'idle_to_shortfall_first',
             'idle_total_first', 'largest_shortfall', 'largest_year', 'idle_at_largest', 'idle_to_shortfall_largest', 'idle_at_window_start', 'P3_short_to_idle_at_start')


def fmt(v):
    return f'{v:.3f}' if isinstance(v, float) else str(v)


def run_check(a):
    """(1) 6 phases, constant path, `safe` fund: the first shortfall year and P3 to the end of the short window equal 140c's `f1_safe_constant_path.csv` for every row. (2) The fund copy at w_pay 3 equals the
    core to 1e-9 on every output, on one cell (median_mid, tm70) at 6 phases, constant path and 20 paths."""
    lv, ctx, inp = F.setup()
    stored = {(r['point'], r['schedule']): r for r in csv.DictReader(open(ROOT / 'docs' / 'model-v3' / 'f1-household' / 'f1_safe_constant_path.csv'))}
    ok, rows = True, []
    for pn in POINTS:
        cp = F.point_ctx(ctx, inp, pn, 'safe')
        for sp in SPECS:
            raw = run_kernel(cp, sp, const_path(ctx), 6)
            _, s = accounting(cp, raw.r, pn, 'safe', sp, 6)
            st = stored[pn, F.lab(sp)]
            for name, got, want in (('first year relief < M1d', s['first_shortfall_year'], int(st['first_year_relief_below_M1d'])), ('P3 to end of short window', f'{s["P3_short"]:.2f}', st['P3_to_end_short_window'])):
                good = str(got) == str(want)
                ok &= good
                rows.append((pn, F.lab(sp), name, got, want, 'equal' if good else 'DIFFERENT'))
    print('### Check 1: 6 phases, constant path, safe fund, against 140c (`f1_safe_constant_path.csv`)\n')
    print(F.tab(['point', 'schedule', 'quantity', 'this script', '140c stored', ''], rows))
    cp = F.point_ctx(ctx, inp, 'median_mid', 'safe')
    g = np.hstack([const_path(ctx), F.paths_of(ctx, 20261118, 19)])
    raw = run_kernel(cp, SPECS[1], g, 6)
    d, n = max_diff(variant_run(cp, raw, 'core'), variant_run(cp, raw, 'copy_w3'))
    d0, _ = max_diff(raw.r, variant_run(cp, raw, 'core'))
    print(f'\n### Check 2: fund copy at w_pay 3 against the core, median_mid tm70_k1_r050, 6 phases, the constant path and 19 level 1 paths\n\n{n} numeric outputs compared; largest absolute difference {d:.3g} '
          f'({"equal to 1e-9" if d <= 1e-9 else "NOT EQUAL"}). The core called again on the same receipts differs from the runner\'s own result by {d0:.3g}.')
    ok &= d <= 1e-9 and d0 <= 1e-9
    print('\nAll checks hold.' if ok else '\nA CHECK FAILED.')
    return 0 if ok else 1


def run_a(a):
    lv, ctx, inp = F.setup()
    rows, summ = [], []
    for fund in a.funds.split(','):
        for pn in a.points.split(','):
            cp = F.point_ctx(ctx, inp, pn, fund)
            for sp in SPECS:
                log(f'A {fund} {pn} {F.lab(sp)}')
                raw = run_kernel(cp, sp, const_path(ctx), a.phases)
                yr, s = accounting(cp, raw.r, pn, fund, sp, a.phases)
                rows += yr
                summ.append(s)
    F.write_csv(OUT / f'a_accounting_years_{a.phases}ph.csv', ('fund', 'point', 'schedule', 'phases', 'year', 'relief', 'M1d', 'shortfall', 'S_pct_gdp', 'idle_S_minus_srr', 'idle_S_minus_total_target'), rows)
    F.write_csv(OUT / f'a_accounting_summary_{a.phases}ph.csv', SUMM_HEAD, [[s[k] if not isinstance(s[k], float) else round(s[k], 4) for k in SUMM_HEAD] for s in summ])
    print(f'### A. Accounting on the constant path ({a.phases} death phases, household arm; percent of GDP; `idle` = fund S minus the short reserve at the end of the year)\n')
    for fund in a.funds.split(','):
        print(f'**Fund `{fund}`**\n')
        print(F.tab(['point', 'schedule', 'fill', 'first shortfall', 'largest shortfall (year)', 'idle in first shortfall year', 'idle / shortfall', 'P3 to end of short window', 'idle at window start', 'P3 / idle at start'],
                    [(s['point'], s['schedule'], s['fill_year'], s['first_shortfall_year'] or 'never', f'{s["largest_shortfall"]:.2f} ({s["largest_year"]})', fmt(s['idle_first']), fmt(s['idle_to_shortfall_first']),
                      f'{s["P3_short"]:.2f}', fmt(s['idle_at_window_start']), fmt(s['P3_short_to_idle_at_start'])) for s in summ if s['fund'] == fund]))
        print()
    return 0


def run_d(a):
    lv, ctx, inp = F.setup()
    g = F.paths_of(ctx, a.seed, a.n)
    rows_c, rows_p, copy_diffs = [], [], []
    t_start = time.time()
    for fund in a.funds.split(','):
        for pn in a.points.split(','):
            cp = F.point_ctx(ctx, inp, pn, fund)
            for sp in SPECS:
                log(f'D {fund} {pn} {F.lab(sp)}  (elapsed {time.time() - t_start:.0f} s)')
                for kind, gg in (('constant', const_path(ctx)), ('paths', g)):
                    t0 = time.time()
                    try:
                        raw = run_kernel(cp, sp, gg, a.phases)
                    except ValueError as exc:                                  # the arm's own alarm (128c): reported with its cell, not worked around
                        log(f'  FAILED: {exc}')
                        (rows_c if kind == 'constant' else rows_p).append(dict(fund=fund, point=pn, schedule=F.lab(sp), variant='FAILED: ' + str(exc).split(':')[0]))
                        continue
                    t_kernel = time.time() - t0
                    base_r = variant_run(cp, raw, 'core')
                    assert max_diff(raw.r, base_r)[0] <= 1e-9, 'revenue.revenue on the stored receipts must reproduce the runner'
                    res = {v: (base_r if v == 'core' else variant_run(cp, raw, v)) for v in VARIANTS}
                    d, nout = max_diff(res['core'], res['copy_w3'])
                    copy_diffs.append((fund, pn, F.lab(sp), kind, nout, d))
                    assert d <= 1e-9, f'the fund copy at w_pay 3 differs from the core by {d}'
                    for v in VARIANTS:
                        s = summarise(cp, res[v])
                        s.update(fund=fund, point=pn, schedule=F.lab(sp), variant=v)
                        if kind == 'constant':
                            r = res[v]
                            rel, m1d = r['relief'][:, 0], r['M1d'][:, 0]
                            below = np.where((m1d > CLOSED) & (rel < m1d - CLOSED))[0]
                            s['first_shortfall_year'] = int(below[0]) + 1 if below.size else 0
                            s['P3_100'] = float(np.maximum(0.0, m1d - rel).sum())
                        (rows_c if kind == 'constant' else rows_p).append(s)
                    if a.time:
                        log(f'  {kind}: kernel {t_kernel:.1f} s, variants {time.time() - t0 - t_kernel:.1f} s')
                    del raw, res
    cols = ['fund', 'point', 'schedule', 'variant', 'F1_strict', 'F1_strict_se', 'F1_relaxed', 'F1_relaxed_se', 'P3_strict_mean', 'P1', 'unfilled_pct', 'M1a_short', 'M1b_short', 'M1c_short', 'M1d_short', 'M1_short'] \
           + [f'P6_y{y}' for y in YEARS] + ['P7a_pct', 'P7a_se', 'P7b_mean', 'P7b_se', 'P7b_min'] + [k + '_se' for k in ('M1a_short', 'M1d_short', 'M1_short')] + [f'P6_y{y}_se' for y in YEARS]
    ccols = cols + ['first_shortfall_year', 'P3_100']
    rnd = lambda v: round(v, 4) if isinstance(v, float) else v
    F.write_csv(OUT / 'd_paths.csv', cols, [[rnd(s.get(k, '')) for k in cols] for s in rows_p])
    F.write_csv(OUT / 'd_constant_path.csv', ccols, [[rnd(s.get(k, '')) for k in ccols] for s in rows_c])
    F.write_csv(OUT / 'b_fund_copy_check.csv', ('fund', 'point', 'schedule', 'run', 'outputs_compared', 'largest_abs_difference'), [(*r[:5], f'{r[5]:.3g}') for r in copy_diffs])
    print(f'Fund-copy check (w_pay 3 against the core): {len(copy_diffs)} runs, every numeric output of `revenue.revenue`; largest absolute difference {max(r[5] for r in copy_diffs):.3g}.\n')
    for kind, rows in (('paths', rows_p), ('constant path', rows_c)):
        print(f'### D. Variants side by side, {kind} ({a.n} level 1 paths, seed {a.seed}; F1 in percent of paths, ± the binomial standard error)\n' if kind == 'paths' else '### D. Variants on the constant path (one path)\n')
        for fund in a.funds.split(','):
            for pn in a.points.split(','):
                sub = [s for s in rows if s['fund'] == fund and s['point'] == pn and 'F1_strict' in s]
                if not sub:
                    continue
                print(f'**Fund `{fund}`, `{pn}`**\n')
                head = ['schedule', 'variant', 'F1 strict', f'F1 tol {TOL_RELAXED:g}, m {int(100 * MARGIN_RELAXED)}%', 'M1a', 'M1b', 'M1c', 'M1d', 'P1', 'P6 y10', 'y25', 'y50', 'y100', 'P7a %', 'P7b mean', 'P7b min'] + (['first shortfall', 'P3 100 y'] if kind != 'paths' else [])
                body = [(s['schedule'], s['variant'], f'{s["F1_strict"]:.1f} ± {s["F1_strict_se"]:.1f}', f'{s["F1_relaxed"]:.1f} ± {s["F1_relaxed_se"]:.1f}', *[f'{s[x + "_short"]:.2f}' for x in ('M1a', 'M1b', 'M1c', 'M1d')],
                         f'{s["P1"]:.1f}', *[f'{s[f"P6_y{y}"]:.1f}' for y in YEARS], f'{s["P7a_pct"]:.1f}', f'{s["P7b_mean"]:.2f}', f'{s["P7b_min"]:.2f}') + ((s['first_shortfall_year'] or 'never', f'{s["P3_100"]:.2f}') if kind != 'paths' else ())
                        for s in sub]
                print(F.tab(head, body))
                print()
    print(f'Total {time.time() - t_start:.0f} s.')
    return 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('block', choices=('check', 'a', 'd'))
    ap.add_argument('--seed', type=int, default=20261118)
    ap.add_argument('--n', type=int, default=200)
    ap.add_argument('--phases', type=int, default=10)
    ap.add_argument('--points', default=','.join(POINTS))
    ap.add_argument('--funds', default=','.join(FUNDS))
    ap.add_argument('--out', default=None)
    ap.add_argument('--time', action='store_true', help='log the kernel and variant time of each run (the size stop)')
    a = ap.parse_args()
    if a.out:
        OUT = Path(a.out)
        OUT.mkdir(parents=True, exist_ok=True)
    sys.exit({'check': run_check, 'a': run_a, 'd': run_d}[a.block](a))
