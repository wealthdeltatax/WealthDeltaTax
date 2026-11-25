"""
f1_household.py -- brief 140c: F1 (the closure share) and CK1 (the stress check) under the household arm. Diagnosis only: no rule is recommended, nothing in the model changes.
=======================================================================================================================================================================
A one-off measurement, not part of model_v3 (its layer and budget rules do not apply). It imports the runner and the core and edits neither. The method is 083c's (`model/studies/f1-diagnostic/f1_gap.py`):
`runner.core_run` gives relief, M1d and the retirement years per path; a retirement margin m is applied as relief / (1 + m) going to `revenue.retire`; F1 is the share of paths whose short-window P3
(summed from year 1 to the end of the short window, as `evaluate`'s `P3h['short']`) is at most a tolerance. What differs from 083c is the arm: the household arm (W5b, taxed) on per-path market returns (128c).

The household arm runs at five labelled scenario points (none central): saving min, median and max at the `mid` regime, and the `low` and `high` regimes at median saving (the 124c grid). Each point runs the 27 schedule
points of the lever grid, on the same paths. Every number is a scenario value at a labelled grid point and fund setting, never a forecast.

Fund settings: `safe` (the fund earns the net financial class return, a stand-in with no register row, deviating with the path's market return; the current arm). `market` (138c: the fund earns the path's market return, like the legacy arm; a labelled axis, no central value).

Run from the repository root (python -I):
    python -I model/studies/f1-household/f1_household.py check [--fund safe]            the reproduction checks against 124c and 128c (about 30 s)
    python -I model/studies/f1-household/f1_household.py f1    [--fund safe] [--seed 20261118] [--n 200] [--points a,b] [--out DIR]    block 1: tables on stdout, CSVs next to the script (about 11 minutes)
    python -I model/studies/f1-household/f1_household.py ck1   [--fund safe]            block 2: the stress check
Progress goes to stderr; two runs with the same arguments print identical text.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = ROOT / 'docs' / 'model-v3' / 'f1-household'   # outputs and stored tables stay here until 163c
OUT = DATA                                     # where the CSVs go (--out)
sys.path.insert(0, str(ROOT / 'model'))

from model_v3.core import burden as bd, pack as pk, returns as rt, revenue as rv  # noqa: E402
from model_v3.runner import runner as R, sweeps as S  # noqa: E402

T = R.T
CLOSED = S.CLOSED                              # 1e-9, as runner and sweeps use it
TOLS = (0.0, 0.05, 0.25, 1.0)                  # GDP-points summed over years; 0 means the 055c rule (P3 <= CLOSED)
MARGINS = (0.0, 0.10, 0.25)                    # retirement margins, as 083c
F1_MIN, M2_CAP, M4A_FLOOR = 75.0, 2.0, 0.0     # the A5 constants (levers/manifest); read, not changed
CHECK = (1, 14, 27)                            # schedule points (1-based) on which the numbers are compared with runner.headlines
YEARS = (5, 10, 20, 30, 50, 100)
POINTS = {'min_mid': ('min', 'mid'), 'median_mid': ('median', 'mid'), 'max_mid': ('max', 'mid'), 'median_low': ('median', 'low'), 'median_high': ('median', 'high')}   # the 124c grid
MAIN = 'median_mid'                            # the point whose long tables are printed in full
SPEC124 = dict(tau_0=0.04, tau_m=0.7, k_ln=1, ratio=0.5)                              # the 124c schedule (account_table.SPEC)
CONST_SPECS = [dict(tau_0=0.04, tau_m=tm, k_ln=1.0, ratio=0.5) for tm in (0.5, 0.7, 0.9)]
FUNDS = ('safe', 'market')


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def tab(head, rows):
    out = ['| ' + ' | '.join(head) + ' |', '|' + '|'.join('---' for _ in head) + '|']
    return '\n'.join(out + ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows])


def pct(x):
    return f'{x:.1f}'


def lab(sp):
    sg, wm = S.labels(sp)
    return f'{sg}_{wm}'


def setup():
    lv = json.loads((ROOT / 'model' / 'model_v3' / 'levers.json').read_text())
    out = yaml.safe_load((ROOT / 'docs' / 'model-v3' / 'outputs.yml').read_text())
    tier1 = next(o for o in out['outputs'] if o['id'] == 'OT1')['by']['input']
    ctx = R.context(pk.load_pack(ROOT / 'data' / 'country-packs' / 'GBR'), pk.load_register(ROOT / 'data' / 'input-register' / 'inputs.json'), lv, tier1, [o['id'] for o in out['outputs']])
    inp = json.loads((ROOT / 'docs' / 'model-v3' / 'cell-baseline' / 'inputs_used.json').read_text())
    return lv, ctx, inp


def point_ctx(ctx, inp, point, fund='safe', paths=True):
    """The context at one scenario grid point of the household arm. `paths` True: per-path market returns (128c); False: the fixed scenario rates of 124c (used by the reproduction check)."""
    sav, regime = POINTS[point]
    arm = dict(arm='household', inputs=inp, saving=sav, regime=regime, paths=paths)
    if fund != 'safe':
        arm['fund_return'] = fund      # 138c: the fund earns the path's market return (needs per-path returns)
    return replace(ctx, arm=arm)


def core(ctx, spec, g):
    """`runner.core_run` at central inputs, plus the short-window M2 per path. Returns what the diagnostic reads."""
    g = np.asarray(g, float)
    raw = R.core_run(ctx, ctx.centre, spec, g, np.full(g.shape, ctx.gdp_g))
    m2 = np.where(raw.ok, bd.m2(raw.fl, raw.lo['short'], raw.hi['short'])['overall'], np.nan)
    return dict(r=raw.r, fl=raw.fl, lo=raw.lo, hi=raw.hi, ok=raw.ok, fill=raw.r['fill'], h=raw.h, inc=raw.inc, m2=m2, P=g.shape[1], raw=raw)


def with_margin(ctx, k, m):
    """Retirement with margin m: relief / (1 + m) goes to rv.retire (so a tax is retired when relief / (1 + m), net of what is already retired, covers its receipts); the excess is measured
    against the TRUE relief. Returns per-path P3 to the end of the short window, M1d, retirement years, M4a (short), taxes retired. As 083c's `with_margin`."""
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


def paths_of(ctx, seed, n):
    return rt.ar1_paths(rt.streams(seed)['level1_paths'], ctx.centre[R.RET['mean']], ctx.centre[R.RET['sd']], ctx.centre[R.RET['phi']], T, n)


def write_csv(path, head, rows):
    with open(path, 'w', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(head)
        w.writerows(rows)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def run_check(a):
    """The reproduction checks. (1) The household arm at its fixed 124c rates on one constant path at the register mean (the common point of household-vs-legacy) reproduces the 124c M1 and M1d at the
    124c schedule and point `median_mid` (grid_results.csv). (2) The 128c paths (seed 1, 1000 paths in chunks of 100, as run_grid.py) reproduce the 128c means (grid_results_paths.csv)."""
    lv, ctx, inp = setup()
    ok = True

    def stored(fname, oid, hz, line):
        for r in csv.DictReader(open(ROOT / 'docs' / 'model-v3' / 'household-arm-run' / fname)):
            if r['grid'] == 'median_mid' and r['id'] == oid and r['horizon'] == hz and r['line'] == line:
                return float(r['a'])
        raise KeyError((fname, oid, hz, line))

    def cmp(tag, got, want, lien=False):
        """`lien`: a long-horizon 128c row. The stored 128c file was written before the pension-secured lien (132c) and the kernel-cap lien (133c); the lien starts in year 61, so it can move only the long horizon."""
        nonlocal ok
        good = abs(got - want) <= 1e-9 * max(1.0, abs(want))
        ok &= good or lien
        print(f'| {tag} | {got:.12g} | {want:.12g} | {"equal" if good else ("differs: the lien of 132c/133c, which came after the 128c file (long horizon only)" if lien else "DIFFERENT")} |')

    print('### Reproduction checks (household arm, `median_mid`, 124c schedule tau_0 0.04, tau_m 0.7, k_ln 1, ratio 0.5)\n')
    print('| quantity | this script | stored | |\n|---|---|---|---|')
    c0 = point_ctx(ctx, inp, MAIN, a.fund, paths=False)
    mu = ctx.centre['I-D1a']
    k = core(c0, SPEC124, np.full((T, 1), mu / 100.0))
    e = R.headlines(k['raw'], c0, c0.centre)
    for hz in ('short', 'long'):
        for x in ('M1', 'M1d'):
            cmp(f'124c fixed rates, constant path {mu}%: {x} {hz}', S._mean(e[x][hz]), stored('grid_results.csv', 'O1', hz, x))
    c1 = point_ctx(ctx, inp, MAIN, a.fund, paths=True)
    rng, parts = rt.streams(1)['level1_paths'], []
    for _ in range(10):
        g = rt.ar1_paths(rng, ctx.centre[R.RET['mean']], ctx.centre[R.RET['sd']], ctx.centre[R.RET['phi']], T, 100)
        parts.append(R.headlines(core(c1, SPEC124, g)['raw'], c1, c1.centre))
    for hz in ('short', 'long'):
        for x in ('M1', 'M1d'):
            cmp(f'128c market paths, seed 1, 1000 paths: {x} {hz}', S._mean(np.concatenate([p[x][hz] for p in parts])), stored('grid_results_paths.csv', 'O1', hz, x), lien=hz == 'long')
    print('\nEvery check holds (the short horizon, which F1 and CK1 read, is equal everywhere).' if ok else '\nA CHECK FAILED.')
    return 0 if ok else 1


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def run_f1(a):
    lv, ctx, inp = setup()
    specs = S.grid(lv)
    pts = list(POINTS) if a.points == 'all' else a.points.split(',')
    g = paths_of(ctx, a.seed, a.n)
    print(f'Fund `{a.fund}`; household arm, per-path market returns (128c); seed {a.seed}; {a.n} level 1 paths of the AR(1) generator at central inputs (mean {ctx.centre["I-D1a"]}, SD {ctx.centre["I-D1b"]}, '
          f'lag-1 {ctx.centre["I-D1b2"]}); the same paths for all {len(specs)} schedule points and all {len(pts)} scenario points; short window = the {int(ctx.centre["I-D14e"])} years after the fill; '
          f'margins {MARGINS}; tolerances {TOLS} GDP-points. Every number is a scenario value at a labelled grid point, not a forecast.\n')
    res, grid_rows, summ_rows, failed = {}, [], [], []
    for pn in pts:
        cp = point_ctx(ctx, inp, pn, a.fund)
        res[pn] = {}
        for n, sp in enumerate(specs, 1):
            log(f'{pn} schedule point {n}/{len(specs)} {lab(sp)}')
            try:
                k = core(cp, sp, g)
            except ValueError as exc:                                # the arm's own alarm (I1, 128c): reported with its point, not worked around; nothing in the model changes
                failed.append((pn, lab(sp), str(exc).split(':')[0]))
                log(f'  FAILED: {exc}')
                continue
            by = {m: with_margin(cp, k, m) for m in MARGINS}
            if n in CHECK:                                           # this script's P3, M2, M4a and fill years equal the runner's headlines
                e = R.headlines(k['raw'], cp, cp.centre)
                assert np.allclose(e['P3h']['short'], by[0.0]['p3']) and abs(S._mean(e['M4a']['short']['overall']) - by[0.0]['m4a']) < 1e-9
                assert np.allclose(e['M2']['short']['overall'], k['m2'], equal_nan=True) and np.array_equal(e['fill'], k['fill'])
            assert np.allclose(by[0.0]['m1d'], k['r']['M1d']), 'margin 0 must reproduce revenue.retire'
            for x in by.values():
                del x['m1d']
            sg = k['r']['S_gdp']
            res[pn][lab(sp)] = dict(spec=sp, m2=S._mean(k['m2']), ok=k['ok'], by=by, fill=S._mean(np.where(k['ok'], k['fill'], np.nan)),
                                    fund={y: S._mean(sg[y - 1]) for y in (10, 25, 50, 100)})
            del k

    pts = [pn for pn in pts if res[pn]]
    nrun = {pn: len(res[pn]) for pn in pts}
    cells = {}
    for pn in pts:
        for tol in TOLS:
            for m in MARGINS:
                n_ok, best_pass, best_all = 0, None, None
                for name, v in res[pn].items():
                    f1, m2, m4 = closed(v['by'][m]['p3'], tol), v['m2'], v['by'][m]['m4a']
                    grid_rows.append((a.fund, pn, name, tol, m, round(f1, 2), round(m2, 4), round(m4, 4), round(v['by'][m]['ntax'], 3)))
                    if best_all is None or f1 > best_all[0]:
                        best_all = (f1, name)
                    if m2 <= M2_CAP and m4 >= M4A_FLOOR and (best_pass is None or f1 > best_pass[0]):
                        best_pass = (f1, name)
                    n_ok += f1 >= F1_MIN and m2 <= M2_CAP and m4 >= M4A_FLOOR
                cells[pn, tol, m] = (n_ok, best_pass, best_all)
                summ_rows.append((a.fund, pn, tol, m, round(best_all[0], 2), best_all[1], round(best_pass[0], 2) if best_pass else '', best_pass[1] if best_pass else '', n_ok, nrun[pn]))
    write_csv(OUT / f'f1_{a.fund}_grid.csv', ('fund', 'point', 'schedule', 'tol', 'margin', 'F1_pct', 'M2_short', 'M4a_short', 'taxes_retired'), grid_rows)
    write_csv(OUT / f'f1_{a.fund}_summary.csv', ('fund', 'point', 'tol', 'margin', 'best_F1_any', 'at', 'best_F1_pass_M2_M4a', 'at', 'feasible_points', 'schedule_points_run'), summ_rows)

    print('### Summary: (tol, m) against best F1 and the feasible-point count, by scenario point\n')
    print('F1 is the percent of paths with short-window P3 at most `tol`. "Best F1 passing M2 and M4a" is the highest F1 among schedule points with M2 short at most '
          f'{M2_CAP} and M4a short at least {M4A_FLOOR}; "feasible points" also needs F1 at least {F1_MIN:g}.\n')
    for pn in pts:
        print(f'**Scenario point `{pn}`** (saving {POINTS[pn][0]}, regime {POINTS[pn][1]}; {nrun[pn]} of {len(specs)} schedule points ran)\n')
        rows = []
        for tol in TOLS:
            for m in MARGINS:
                n_ok, bp, ba = cells[pn, tol, m]
                rows.append((f'{tol:g}', f'{int(100 * m)}%', pct(ba[0]), ba[1], pct(bp[0]) if bp else 'none', bp[1] if bp else '', n_ok))
        print(tab(['tol', 'm', 'best F1 (any point)', 'at', 'best F1 passing M2, M4a', 'at', 'feasible points'], rows))
        print()
    if failed:
        write_csv(OUT / f'f1_{a.fund}_failed.csv', ('point', 'schedule', 'alarm'), failed)
        print('**Schedule points that did not run** (the arm raised its own alarm on a path under per-path market returns, 128c; nothing was changed, the cell is left out of every table above and below):\n')
        print(tab(['scenario point', 'schedule point', 'alarm'], failed))
        print()
    top = max(c[2][0] for c in cells.values())
    nfe = sum(c[0] for c in cells.values())
    print(f'Best F1 anywhere in the (scenario point, tol, m) tables: {top:.1f} percent; feasible (point, tol, m) cells: {nfe} of {len(cells)}.\n')

    if MAIN in res:
        pn = MAIN
        print(f'### Size of the failure at `{pn}` (tol 0, m 0)\n')
        rows = []
        for name, v in res[pn].items():
            b0 = v['by'][0.0]
            p3 = b0['p3']
            rows.append((name, pct(closed(p3, 0)), pct(100 * float(np.mean(p3 == 0.0))), f'{np.percentile(p3, 10):.2f}', f'{np.median(p3):.2f}', f'{np.percentile(p3, 90):.2f}', f'{p3.max():.2f}',
                         pct(b0['near']), f'{b0["ntax"]:.2f}', pct(100 * float(np.mean(~v['ok']))), f'{v["fill"]:.1f}', f'{v["m2"]:.2f}', f'{b0["m4a"]:.1f}'))
        print(tab(['schedule', 'F1 % (P3<=1e-9)', 'P3 exactly 0 %', 'P3 P10', 'median', 'P90', 'max', 'failing paths, first shortfall within 3 y of a retirement %',
                   'taxes retired (mean, filled paths)', 'unfilled paths %', 'fill year (mean)', 'M2 short', 'M4a short'], rows))
        f1s = [closed(v['by'][0.0]['p3'], 0) for v in res[pn].values()]
        print(f'\nF1 over the {len(f1s)} schedule points at (tol 0, m 0): {min(f1s):.1f} to {max(f1s):.1f} percent.\n')
        print(f'### F1 by tolerance and margin at `{pn}` (percent of paths)\n')
        head = ['schedule'] + [f'tol {t:g}, m {int(100 * m)}%' for m in MARGINS for t in TOLS]
        print(tab(head, [(name, *[pct(closed(v['by'][m]['p3'], t)) for m in MARGINS for t in TOLS]) for name, v in res[pn].items()]))
        print(f'\n### Fund size at `{pn}` (percent of GDP, mean over filled paths, tol-free)\n')
        print(tab(['schedule', 'year 10', 'year 25', 'year 50', 'year 100'], [(name, *[f'{v["fund"][y]:.1f}' for y in (10, 25, 50, 100)]) for name, v in res[pn].items()]))
        print()

    # ---- a constant return path (the structural test: no volatility at all) ----
    print('### Constant return path (the structural test)\n')
    mu = ctx.centre['I-D1a']
    print(f'g = {mu}% every year (I-D1a central), one path, GDP-per-head growth {100 * ctx.gdp_g:.2f}% a year; household arm at each scenario point, schedules tau_m 0.5, 0.7, 0.9 (k_ln 1, ratio 0.5). '
          'Relief and M1d in percent of GDP; diff = relief - M1d (negative: retired receipts outrun relief). "short window" is the 10 years after the fill.\n')
    crow, const_rows = [], []
    for pn in list(POINTS) if a.points == 'all' else a.points.split(','):
        cp = point_ctx(ctx, inp, pn, a.fund)
        for sp in CONST_SPECS:
            try:
                k = core(cp, sp, np.full((T, 1), mu / 100.0))
            except ValueError as exc:
                crow.append((pn, lab(sp), 'FAILED: ' + str(exc).split(':')[0], '', '', '', '', '', ''))
                continue
            r = k['r']
            rel, m1d = r['relief'][:, 0], r['M1d'][:, 0]
            below = np.where((m1d > CLOSED) & (rel < m1d - CLOSED))[0]
            fy, hi = int(k['fill'][0]), int(k['hi']['short'][0])
            inw = bool(below.size and below[0] + 1 <= hi)
            crow.append((pn, lab(sp), fy, hi, int((r['P5'][0] > 0).sum()), int(below[0]) + 1 if below.size else 'never', 'yes' if inw else 'no', f'{float(r["P3"][0]):.2f}',
                         f'{float(np.maximum(0.0, m1d - rel)[:hi].sum()):.2f}'))
            if pn == MAIN:
                const_rows.append((sp, rel, r['M1a'][:, 0], r['M1b'][:, 0], r['M1c'][:, 0], m1d, r['S_gdp'][:, 0]))
    print(tab(['scenario point', 'schedule', 'fill year', 'end of short window', 'taxes retired by year 100 (of 6)', 'first year relief < M1d', 'inside short window', 'P3 whole 100 y', 'P3 to end of short window'], crow))
    write_csv(OUT / f'f1_{a.fund}_constant_path.csv', ('point', 'schedule', 'fill_year', 'end_short_window', 'taxes_retired_100', 'first_year_relief_below_M1d', 'inside_short_window', 'P3_100y', 'P3_to_end_short_window'), crow)
    for sp, rel, m1a, m1b, m1c, m1d, sgdp in const_rows:
        print(f'\n**{lab(sp)}** (tau_m {sp["tau_m"]}), `{MAIN}`:\n')
        print(tab(['year', 'relief', 'of which M1a', 'M1b', 'M1c', 'M1d', 'diff', 'fund S % GDP'], [(y, *[f'{x[y - 1]:.3f}' for x in (rel, m1a, m1b, m1c, m1d)], f'{rel[y - 1] - m1d[y - 1]:.3f}', f'{sgdp[y - 1]:.1f}') for y in YEARS]))
    print()
    return 0


AMPS = (0, 1, 2, 3, 4, 5, 6, 8, 10, 12)        # the stress amplitudes in GDP-return points: the manifest's A1, A3, A5, A8, A12 (CK1 by-vocabulary) and 083c's 0, 2, 4, 8, 12, with the gaps filled
CK1_SPECS = [dict(tau_0=0.04, tau_m=tm, k_ln=1.0, ratio=0.5) for tm in (0.5, 0.7, 0.9)] + [dict(tau_0=0.04, tau_m=0.7, k_ln=0.5, ratio=0.5)]   # 083c's four; tm70_k1_r050 is the 124c schedule


def run_ck1(a):
    """CK1: the fixed path g(t) = mu + A sin(2 pi t / 10) (mu the register's I-D1a, 4.74), one path per amplitude, under the household arm at each scenario point. Per amplitude: P1 (the fill year, T if unfilled),
    P3 over the short window proper (years fill+1 to fill+h), over transition plus short (years 1 to fill+h: the F1 definition) and over all 100 years (what `sweeps.stress` reports), and P7b (the minimum
    cover) over the years after the fill up to the end of the short window and over all the years after the fill (the metric's definition). Transition adds no years after the fill, so P7b has the two windows."""
    lv, ctx, inp = setup()
    mu, t, h, ml = ctx.centre['I-D1a'], np.arange(1, T + 1), int(ctx.centre['I-D14e']), ctx.centre['I-D8a']
    print(f'Fund `{a.fund}`; household arm; g(t) = {mu} + A sin(2 pi t / 10) percent a year, one path per amplitude; short window = the {h} years after the fill. Every number is a scenario value at a labelled grid point, not a forecast.\n')
    rows, tops, failed = [], [], []
    for pn in list(POINTS) if a.points == 'all' else a.points.split(','):
        cp = point_ctx(ctx, inp, pn, a.fund)
        for sp in CK1_SPECS:
            top, prev = {'short window': None, 'transition + short': None, 'all 100 years': None}, {'short window': True, 'transition + short': True, 'all 100 years': True}
            for A in AMPS:
                log(f'{pn} {lab(sp)} A {A}')
                g = ((mu + A * np.sin(2 * np.pi * t / 10)) / 100.0)[:, None]
                try:
                    k = core(cp, sp, g)
                except ValueError as exc:
                    failed.append((pn, lab(sp), A, str(exc).split(':')[0]))
                    prev = dict.fromkeys(prev, False)
                    continue
                r, fl = k['r'], int(k['fill'][0])
                ex = np.maximum(0.0, r['M1d'] - r['relief'])[:, 0]
                f = r['fund']
                lres = ((f['S'] - f['srr']) / (ml * np.where(f['A'] > 0, f['A'], np.nan)))[:, 0]
                after = (t > fl) & (fl > 0)
                assert abs(np.where(after, lres, np.inf).min() - float(r['P7b'][0])) < 1e-9 and abs(ex.sum() - float(r['P3'][0])) < 1e-9      # this script's windows equal the core's whole-run values
                p3 = {'short window': ex[(t > fl) & (t <= fl + h)].sum(), 'transition + short': ex[t <= fl + h].sum(), 'all 100 years': ex.sum()}
                ok = fl <= T and not bool(r['unfilled'][0])
                p7w, p7 = (np.where(after & (t <= fl + h), lres, np.inf).min() if ok else np.nan), (np.where(after, lres, np.inf).min() if ok else np.nan)
                for w in prev:
                    prev[w] = prev[w] and p3[w] <= CLOSED
                    if prev[w]:
                        top[w] = A
                rows.append((pn, lab(sp), A, int(r['P1'][0]), 'yes' if ok else 'no', *[f'{p3[w]:.2f}' for w in p3], f'{p7w:.2f}', f'{p7:.2f}'))
            tops.append((pn, lab(sp), *[('none' if v is None else v) for v in top.values()]))
    head = ['scenario point', 'schedule', 'A', 'P1 (fill year)', 'filled', 'P3 short window', 'P3 transition + short', 'P3 all 100 y', 'P7b short window', 'P7b all years after fill']
    write_csv(OUT / f'ck1_{a.fund}.csv', head, rows)
    print('### CK1: the largest amplitude up to which P3 is zero on every smaller amplitude too (none: even A 0 is not zero)\n')
    print(tab(['scenario point', 'schedule', 'short window', 'transition + short', 'all 100 years'], tops))
    for pn in dict.fromkeys(r[0] for r in rows):
        print(f'\n### CK1 at `{pn}`\n')
        print(tab(head[1:], [r[1:] for r in rows if r[0] == pn]))
    if failed:
        write_csv(OUT / f'ck1_{a.fund}_failed.csv', ('point', 'schedule', 'A', 'alarm'), failed)
        print('\n**Cells that did not run** (the arm raised its own alarm; nothing was changed):\n')
        print(tab(['scenario point', 'schedule', 'A', 'alarm'], failed))
    print()
    return 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('block', choices=('check', 'f1', 'ck1'))
    ap.add_argument('--fund', default='safe', choices=FUNDS)
    ap.add_argument('--seed', type=int, default=20261118)
    ap.add_argument('--n', type=int, default=200)
    ap.add_argument('--points', default='all', help='comma-separated scenario points (default all five)')
    ap.add_argument('--out', default=None, help='folder for the CSVs (default: next to the script)')
    a = ap.parse_args()
    if a.out:
        OUT = Path(a.out)
        OUT.mkdir(parents=True, exist_ok=True)
    sys.exit({'check': run_check, 'f1': run_f1, 'ck1': run_ck1}[a.block](a))
