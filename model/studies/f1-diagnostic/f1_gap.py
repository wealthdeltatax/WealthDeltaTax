"""
f1_gap.py -- brief 083c: why no schedule closes (F1), and which single change would move it
=========================================================================================
A one-off measurement, not part of model_v3 (its layer and budget rules do not apply). It imports the runner and the core and edits neither.
`runner.core_run` (brief 084c: the first half of `evaluate`, up to the revenue call, kept raw) gives relief, M1d and the retirement years per path.
Before 084c this script carried its own copy of that half; the numbers did not change.

Run from the repository root:   python -I model/studies/f1-diagnostic/f1_gap.py [--seed 20261118] [--n 1000]
It prints the report's tables as Markdown on stdout (progress on stderr). Two runs with the same seed print identical text.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'model'))

import json  # noqa: E402

from model_v3.core import burden as bd, pack as pk, returns as rt, revenue as rv, schedule as sc  # noqa: E402
from model_v3.runner import runner as R, sweeps as S  # noqa: E402

T = R.T
CLOSED = S.CLOSED                              # 1e-9, as runner and sweeps use it
TOLS = (0.0, 0.05, 0.25, 1.0)                  # GDP-points summed over years; 0 means the 055c rule (P3 <= CLOSED)
MARGINS = (0.0, 0.10, 0.25)
EXTRA = (0.50, 1.00)                           # beyond the brief's grid: printed in their own table, to show where F1 would reach 75%
F1_MIN, M2_CAP, M4A_FLOOR = 75.0, 2.0, 0.0     # the A5 constants (levers/manifest); read, not changed
CHECK = (1, 14, 27)                            # grid points (1-based) on which the numbers are compared with runner.headlines
YEARS = (5, 10, 20, 30, 50, 100)
AMPS = (0, 2, 4, 8, 12)
CONST_SPECS = [dict(tau_0=0.04, tau_m=tm, k_ln=1.0, ratio=0.5) for tm in (0.5, 0.7, 0.9)]
CK1_SPECS = CONST_SPECS + [dict(tau_0=0.04, tau_m=0.7, k_ln=0.5, ratio=0.5)]     # the last is the schedule 055c used for CK1 and its tornado
CK1_MU = (4.42, 4.74)                          # 055c used 4.42 (I-D1a2); metrics.md now says I-D1a, 4.74


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def tab(head, rows):
    out = ['| ' + ' | '.join(head) + ' |', '|' + '|'.join('---' for _ in head) + '|']
    return '\n'.join(out + ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows])


def build_ctx():
    lv = json.loads((ROOT / 'model' / 'model_v3' / 'levers.json').read_text())
    out = yaml.safe_load((ROOT / 'model-specs' / 'outputs.yml').read_text())
    tier1 = next(o for o in out['outputs'] if o['id'] == 'OT1')['by']['input']
    ctx = R.context(pk.load_pack(ROOT / 'data' / 'country-packs' / 'GBR'), pk.load_register(ROOT / 'data' / 'input-register' / 'inputs.json'), lv, tier1, [o['id'] for o in out['outputs']])
    return lv, ctx


def core(ctx, spec, g):
    """`runner.core_run` at central inputs, plus the short-window M2 per path. Returns what the diagnostic reads."""
    g = np.asarray(g, float)
    raw = R.core_run(ctx, ctx.centre, spec, g, np.full(g.shape, ctx.gdp_g))
    m2 = np.where(raw.ok, bd.m2(raw.fl, raw.lo['short'], raw.hi['short'])['overall'], np.nan)
    return dict(r=raw.r, fl=raw.fl, lo=raw.lo, hi=raw.hi, ok=raw.ok, fill=raw.r['fill'], h=raw.h, inc=raw.inc, m2=m2, P=g.shape[1], raw=raw)


def with_margin(ctx, k, m):
    """Retirement with margin m: relief / (1 + m) goes to rv.retire (so a tax is retired when relief / (1 + m), net of what is already retired, covers its
    receipts); the excess is measured against the TRUE relief. Returns per-path P3 to the end of the short window, M1d, retirement years, M4a (short), taxes retired."""
    r, hi = k['r'], k['hi']['short']
    m1d, yr = rv.retire(r['relief'] / (1.0 + m), k['fill'], ctx.rec)
    t = np.arange(1, T + 1)[:, None]
    ex = np.maximum(0.0, m1d - r['relief'])
    p3 = (ex * (t <= hi[None, :])).sum(axis=0)
    bad = (ex > CLOSED) & (t <= hi[None, :])
    anybad = bad.any(axis=0)
    first = bad.argmax(axis=0) + 1
    near = ((yr > 0) & (first[:, None] - yr >= 0) & (first[:, None] - yr <= 3)).any(axis=1)
    m4a = np.where(k['ok'], bd.m4(yr, hi, k['inc'], ctx.bill, ctx.income)['M4a']['overall'], np.nan)
    ntax = ((yr > 0) & (yr <= hi[:, None])).sum(axis=1)
    return dict(p3=p3, m1d=m1d, yr=yr, m4a=S._mean(m4a), ntax=float(ntax[k['ok']].mean()) if k['ok'].any() else float('nan'),
                near=100 * near[anybad].mean() if anybad.any() else float('nan'))


def closed(p3, tol):
    return 100.0 * float(np.mean(p3 <= (CLOSED if tol == 0 else tol)))


def pct(x):
    return f'{x:.1f}'


def lab(sp):
    sg, wm = S.labels(sp)
    return f'{sg}_{wm}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=int, default=20261118)
    ap.add_argument('--n', type=int, default=1000)
    a = ap.parse_args()
    lv, ctx = build_ctx()
    specs = S.grid(lv)
    g = rt.streams(a.seed)['level1_paths']
    g = rt.ar1_paths(g, ctx.centre[R.RET['mean']], ctx.centre[R.RET['sd']], ctx.centre[R.RET['phi']], T, a.n)
    print(f'Seed {a.seed}; {a.n} level 1 paths of the AR(1) generator at central inputs (mean {ctx.centre["I-D1a"]}, SD {ctx.centre["I-D1b"]}, lag-1 {ctx.centre["I-D1b2"]}); '
          f'the same paths for all {len(specs)} grid points; short window = the {int(ctx.centre["I-D14e"])} years after the fill; margins {MARGINS} (and {EXTRA} in the last table only); tolerances {TOLS} GDP-points.\n')

    res = {}
    for n, sp in enumerate(specs, 1):
        log(f'grid point {n}/{len(specs)} {lab(sp)}')
        k = core(ctx, sp, g)
        by = {m: with_margin(ctx, k, m) for m in MARGINS + EXTRA}
        if n in CHECK:                         # the diagnostic's own P3, M2, M4a and fill years equal the runner's headlines
            e = R.headlines(k['raw'], ctx, ctx.centre)
            assert np.allclose(e['P3h']['short'], by[0.0]['p3']) and abs(S._mean(e['M4a']['short']['overall']) - by[0.0]['m4a']) < 1e-9
            assert np.allclose(e['M2']['short']['overall'], k['m2'], equal_nan=True) and np.array_equal(e['fill'], k['fill'])
            log('  diagnostic equals runner.headlines on this point')
        assert np.allclose(by[0.0]['m1d'], k['r']['M1d']), 'margin 0 must reproduce revenue.retire'
        for x in by.values():
            del x['m1d']                       # keep memory small: the line flows and the (T, P) arrays are dropped with k
        res[lab(sp)] = dict(spec=sp, m2=S._mean(k['m2']), ok=k['ok'], by=by)
        del k

    # ---------- summary table (item 6 headline) ----------
    cells = {}
    for tol in TOLS:
        for m in MARGINS:
            n_ok, best_pass, best_all = 0, None, None
            for name, v in res.items():
                f1, m2, m4 = closed(v['by'][m]['p3'], tol), v['m2'], v['by'][m]['m4a']
                if best_all is None or f1 > best_all[0]:
                    best_all = (f1, name)
                if m2 <= M2_CAP and m4 >= M4A_FLOOR and (best_pass is None or f1 > best_pass[0]):
                    best_pass = (f1, name)
                n_ok += f1 >= F1_MIN and m2 <= M2_CAP and m4 >= M4A_FLOOR
            cells[tol, m] = (n_ok, best_pass, best_all)
    print('### Summary: (tol, m) against best F1 and the feasible-point count\n')
    print('F1 is the percent of paths with short-window P3 at most `tol`. "Best F1 passing M2 and M4a" is the highest F1 among grid points with M2 short at most '
          f'{M2_CAP} and M4a short at least {M4A_FLOOR}; "feasible points" also needs F1 at least {F1_MIN:g}.\n')
    rows = []
    for tol in TOLS:
        for m in MARGINS:
            n_ok, bp, ba = cells[tol, m]
            rows.append((f'{tol:g}', f'{int(100 * m)}%', pct(ba[0]), ba[1], pct(bp[0]) if bp else 'none', bp[1] if bp else '', n_ok))
    print(tab(['tol', 'm', 'best F1 (any point)', 'at', 'best F1 passing M2, M4a', 'at', 'feasible points of 27'], rows))
    print()

    # ---------- item 1 ----------
    print('### Item 1: size of the failure (tol 0, m 0)\n')
    rows = []
    for name, v in res.items():
        p3, b0 = v['by'][0.0]['p3'], v['by'][0.0]
        rows.append((name, pct(closed(p3, 0)), pct(100 * float(np.mean(p3 == 0.0))), f'{np.percentile(p3, 10):.2f}', f'{np.median(p3):.2f}', f'{np.percentile(p3, 90):.2f}',
                     f'{p3.max():.2f}', pct(b0['near']), f'{b0["ntax"]:.2f}', pct(100 * float(np.mean(~v['ok']))), f'{v["m2"]:.2f}', f'{b0["m4a"]:.1f}'))
    print(tab(['point', 'F1 % (P3<=1e-9)', 'P3 exactly 0 %', 'P3 P10', 'median', 'P90', 'max', 'failing paths, first shortfall within 3 y of a retirement %',
               'taxes retired (mean, filled paths)', 'unfilled paths %', 'M2 short', 'M4a short'], rows))
    f1s = [closed(v['by'][0.0]['p3'], 0) for v in res.values()]
    print(f'\nF1 over the {len(res)} points at (tol 0, m 0): {min(f1s):.1f} to {max(f1s):.1f} percent (055c: 4.0 to 11.2).\n')

    # ---------- item 2 and 3 ----------
    print('### Item 2 and 3: F1 by tolerance and margin (percent of paths)\n')
    head = ['point'] + [f'tol {t:g}, m {int(100 * m)}%' for m in MARGINS for t in TOLS]
    print(tab(head, [(name, *[pct(closed(v['by'][m]['p3'], t)) for m in MARGINS for t in TOLS]) for name, v in res.items()]))
    print('\n### Item 3: margin effect on M4a (short), taxes retired and F1 at tol 0\n')
    head = ['point'] + [f'{c} m {int(100 * m)}%' for m in MARGINS for c in ('F1', 'M4a', 'taxes')]
    print(tab(head, [(name, *[x for m in MARGINS for x in (pct(closed(v['by'][m]['p3'], 0)), f'{v["by"][m]["m4a"]:.1f}', f'{v["by"][m]["ntax"]:.2f}')]) for name, v in res.items()]))
    print()

    # ---------- item 4 ----------
    print('### Item 4: constant return path\n')
    mu = ctx.centre['I-D1a']
    print(f'g = {mu}% every year (I-D1a central), GDP-per-head growth {100 * ctx.gdp_g:.2f}% a year, one path. Relief and M1d in percent of GDP; diff = relief - M1d '
          '(negative: retired receipts outrun relief).\n')
    for sp in CONST_SPECS:
        k = core(ctx, sp, np.full((T, 1), mu / 100.0))
        r = k['r']
        rel, m1d = r['relief'][:, 0], r['M1d'][:, 0]
        below = np.where((m1d > CLOSED) & (rel < m1d - CLOSED))[0]
        print(f'**{lab(sp)}** (tau_m {sp["tau_m"]}): fill year {int(k["fill"][0])}; taxes retired by year 100: {int((r["P5"][0] > 0).sum())} of {len(ctx.rec)}; '
              f'first year relief < M1d: {int(below[0]) + 1 if below.size else "never"}; P3 {float(r["P3"][0]):.2f}.\n')
        print(tab(['year', 'relief', 'of which M1a', 'M1b', 'M1c', 'M1d', 'diff'], [(y, *[f'{x[y - 1]:.3f}' for x in (rel, r['M1a'][:, 0], r['M1b'][:, 0], r['M1c'][:, 0], m1d)], f'{rel[y - 1] - m1d[y - 1]:.3f}') for y in YEARS]))
        print()

    # ---------- item 5 ----------
    print('### Item 5: CK1 window\n')
    print('P3 on g(t) = mu + A sin(2 pi t / 10), GDP-points summed over years: whole 100 years (as 055c reports it) and years 1 to fill + short horizon only.\n')
    t = np.arange(1, T + 1)
    for sp in CK1_SPECS:
        for m_ in CK1_MU:
            rows = []
            for A in AMPS:
                k = core(ctx, sp, ((m_ + A * np.sin(2 * np.pi * t / 10)) / 100.0)[:, None])
                ex = np.maximum(0.0, k['r']['M1d'] - k['r']['relief'])[:, 0]
                rows.append((A, int(k['fill'][0]), f'{ex.sum():.2f}', f'{ex[t <= k["hi"]["short"][0]].sum():.2f}'))
            print(f'**{lab(sp)}**, mu {m_}:\n')
            print(tab(['A', 'fill year', 'P3 whole 100 y', 'P3 to end of short window'], rows))
            print()

    # ---------- item 6 ----------
    print('### Item 6: chosen point for each (tol, m)\n')
    rows = []
    for tol in TOLS:
        for m in MARGINS:
            n_ok, bp, _ = cells[tol, m]
            ok_pts = [name for name, v in res.items() if closed(v['by'][m]['p3'], tol) >= F1_MIN and v['m2'] <= M2_CAP and v['by'][m]['m4a'] >= M4A_FLOOR]
            rows.append((f'{tol:g}', f'{int(100 * m)}%', n_ok, ', '.join(ok_pts) or 'none', f'{pct(bp[0])} ({bp[1]})' if bp else 'none'))
    print(tab(['tol', 'm', 'points passing all three', 'which', 'highest F1 among points passing M2 and M4a'], rows))
    print()
    print('### Beyond the brief: larger margins (not part of the specified grid)\n')
    print('Same definitions as the summary table, margins of 50% and 100%, tolerance 0 and 1. "taxes" is the mean number retired by the end of the short window '
          'at the best point passing M2 and M4a.\n')
    rows = []
    for m in EXTRA:
        for tol in (0.0, 1.0):
            best, n_ok, who = None, 0, []
            for name, v in res.items():
                f1, m4 = closed(v['by'][m]['p3'], tol), v['by'][m]['m4a']
                if v['m2'] <= M2_CAP and m4 >= M4A_FLOOR and (best is None or f1 > best[0]):
                    best = (f1, name, m4, v['by'][m]['ntax'])
                if f1 >= F1_MIN and v['m2'] <= M2_CAP and m4 >= M4A_FLOOR:
                    n_ok += 1
                    who.append(f'{name} (F1 {f1:.1f}, M4a {m4:.1f}, taxes {v["by"][m]["ntax"]:.2f})')
            rows.append((f'{int(100 * m)}%', f'{tol:g}', pct(best[0]) if best else 'none', best[1] if best else '', f'{best[2]:.1f}' if best else '', f'{best[3]:.2f}' if best else '', n_ok, '; '.join(who) or 'none'))
    print(tab(['m', 'tol', 'best F1 passing M2, M4a', 'at', 'its M4a short', 'taxes retired', 'feasible points of 27', 'which'], rows))
    print()
    top = max(c[2][0] for c in cells.values())
    print(f'EARLY CHECK: best F1 anywhere in the (tol, m) table is {top:.1f} percent' + ('; every cell is under 25%.' if top < 25 else '.'))


if __name__ == '__main__':
    main()
