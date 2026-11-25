"""
death_phases.py -- brief 149c: does the death-phase count cause the five-year cycle in M1a, and with it the F1 failure of 140c? Diagnosis only: no rule and no count is recommended, nothing in model_v3 changes.
=======================================================================================================================================================================================================
A one-off measurement, not part of model_v3. It imports the runner and the core read-only and imports 140c's script (`model/studies/f1-household/f1_household.py`) for its setup, its scenario points and its `core`.
`runner.core_run` does not pass `n_phase` to `burden.line_flows` and `revenue.run_lines`, so `phases(n)` wraps those two module functions for the length of a run (a runtime wrapper; no file is edited) and sets `n_phase`.
The phase count is a numerical approximation of the age-at-death distribution (first deaths at ceil(i G / n_phase), then every G = 30 years), so its effect is read as a convergence study: does the answer settle as the count grows.

Run from the repository root (python -I):
    python -I model/studies/death-phases/death_phases.py check                   the 6-phase rows reproduce 140c's constant-path numbers (about 10 s)
    python -I model/studies/death-phases/death_phases.py years [--phases 6,10,15,30]    block 1: year-by-year tables on a constant path, CSV next to the script
    python -I model/studies/death-phases/death_phases.py legacy [--phases 6,10,15,30]    block 3: block 1's table for the legacy arm (083c's), CSV next to the script
    python -I model/studies/death-phases/death_phases.py checkf1                  after `f1`: the 6-phase cells equal 140c's cell by cell
    python -I model/studies/death-phases/death_phases.py f1 [--phases 6,15,30] [--seed 20261118] [--n 200] [--out DIR]    block 2: 140c's `f1` at `median_mid` per phase count (about 10 minutes); per-count files in f1_phases_N/
Progress goes to stderr; two runs with the same arguments print identical text.
"""
from __future__ import annotations

import argparse
import csv
import sys
from contextlib import contextmanager
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'model'))
sys.path.insert(0, str(ROOT / 'model' / 'studies' / 'f1-household'))

import f1_household as F  # noqa: E402  (140c's script: setup, point_ctx, core, lab, tab, write_csv)

T, CLOSED = F.T, F.CLOSED
OUT = HERE
PHASES = (6, 10, 15, 30)
YEARS = 40                                            # block 1 prints years 1 to 40
CYCLE = (10, 40)                                      # the years over which the amplitude of M1a is read
SPECS = [dict(tau_0=0.04, tau_m=tm, k_ln=1.0, ratio=0.5) for tm in (0.7, 0.5)]   # tm70_k1_r050 (the 124c schedule) and tm50_k1_r050
PTS = ('median_mid', 'median_low')


@contextmanager
def phases(n):
    """Run the core with n death phases: wraps burden.line_flows and revenue.run_lines (the runner calls both without n_phase) for the length of the `with`; restores them after."""
    bd, rv = F.bd, F.rv
    lf, rl = bd.line_flows, rv.run_lines
    bd.line_flows = lambda *a, **k: lf(*a, n_phase=n, **k)
    rv.run_lines = lambda *a, **k: rl(*a, n_phase=n, **k)
    try:
        yield
    finally:
        bd.line_flows, rv.run_lines = lf, rl


def const_run(ctx, inp, point, spec, n, arm_ctx=None):
    """The constant 4.74% path (one path) at one scenario point and phase count; returns the year-by-year lines (percent of GDP) and the numbers read off them."""
    cp = arm_ctx or F.point_ctx(ctx, inp, point, 'safe')
    mu = ctx.centre['I-D1a']
    with phases(n):
        k = F.core(cp, spec, np.full((T, 1), mu / 100.0))
    assert k['raw'].fl['net'].shape[1] == len(k['raw'].base.labels) * n, 'the phase count did not reach the kernel'
    r = k['r']
    line = {x: np.asarray(r[x])[:, 0] for x in ('M1a', 'M1b', 'M1c', 'relief', 'M1d')}
    fy, hi = int(k['fill'][0]), int(k['hi']['short'][0])
    ex = np.maximum(0.0, line['M1d'] - line['relief'])
    below = np.where((line['M1d'] > CLOSED) & (line['relief'] < line['M1d'] - CLOSED))[0]
    c0, c1 = CYCLE[0] - 1, CYCLE[1]
    stat = dict(fill_year=fy, end_short=hi, first_below=int(below[0]) + 1 if below.size else 0, years_below_10_40=int(((line['M1d'][c0:c1] > CLOSED) & (line['relief'][c0:c1] < line['M1d'][c0:c1] - CLOSED)).sum()),
                P3_short=float(ex[:hi].sum()), P3_100=float(ex.sum()),
                M1a_amp=float(line['M1a'][c0:c1].max() - line['M1a'][c0:c1].min()), relief_amp=float(line['relief'][c0:c1].max() - line['relief'][c0:c1].min()),
                M1a_mean=float(line['M1a'][c0:c1].mean()), relief_mean=float(line['relief'][c0:c1].mean()), M1d_end=float(line['M1d'][c1 - 1]))
    return line, stat


def run_check(a):
    """The 6-phase rows reproduce 140c's constant-path table (`f1_safe_constant_path.csv`): first year relief < M1d, P3 to the end of the short window, P3 over 100 years, fill year, end of short window."""
    lv, ctx, inp = F.setup()
    stored = {(r['point'], r['schedule']): r for r in csv.DictReader(open(ROOT / 'docs' / 'model-v3' / 'f1-household' / 'f1_safe_constant_path.csv'))}
    ok = True
    print('### Reproduction check: 6 phases against 140c (`f1_safe_constant_path.csv`), constant path, safe fund\n')
    rows = []
    for pn in PTS:
        for sp in SPECS:
            _, s = const_run(ctx, inp, pn, sp, 6)
            st = stored[pn, F.lab(sp)]
            pairs = (('fill year', s['fill_year'], int(st['fill_year'])), ('end of short window', s['end_short'], int(st['end_short_window'])), ('first year relief < M1d', s['first_below'], int(st['first_year_relief_below_M1d'])),
                     ('P3 to end of short window', f'{s["P3_short"]:.2f}', st['P3_to_end_short_window']), ('P3 100 y', f'{s["P3_100"]:.2f}', st['P3_100y']))
            for name, got, want in pairs:
                good = str(got) == str(want)
                ok &= good
                rows.append((pn, F.lab(sp), name, got, want, 'equal' if good else 'DIFFERENT'))
    print(F.tab(['point', 'schedule', 'quantity', 'this script', '140c stored', ''], rows))
    print('\n### Reproduction check: legacy arm, 6 phases, against 083c (`docs/model-v3/f1-diagnostic/report.md`, item 4 and the F1 tables), constant path\n')
    old083 = {'tm50_k1_r050': dict(first=13, p3_100='81.45', p3_short='2.79'), 'tm70_k1_r050': dict(first=13, p3_100='83.74', p3_short='2.66')}   # report.md lines 154, 165, 205, 225
    rows = []
    for sp in SPECS:
        _, s = const_run(ctx, inp, 'legacy', sp, 6, arm_ctx=ctx)
        w = old083[F.lab(sp)]
        for name, got, want in (('fill year', s['fill_year'], 6), ('first year relief < M1d', s['first_below'], w['first']), ('P3 100 y', f'{s["P3_100"]:.2f}', w['p3_100']), ('P3 to end of short window', f'{s["P3_short"]:.2f}', w['p3_short'])):
            good = str(got) == str(want)
            ok &= good
            rows.append(('legacy', F.lab(sp), name, got, want, 'equal' if good else 'DIFFERENT'))
    print(F.tab(['arm', 'schedule', 'quantity', 'this script', '083c report', ''], rows))
    print('\nAll equal.' if ok else '\nA CHECK FAILED.')
    return 0 if ok else 1


def run_checkf1(a):
    """After `f1`: the 6-phase `median_mid` cells equal 140c's (`f1_safe_grid.csv`) cell by cell (F1, M2, M4a, taxes retired, for every tolerance and margin); cells present in only one file are listed."""
    key = lambda r: (r['schedule'], r['tol'], r['margin'])
    new = {key(r): r for r in csv.DictReader(open(OUT / 'f1_phases_6' / 'f1_safe_grid.csv'))}
    old = {key(r): r for r in csv.DictReader(open(ROOT / 'docs' / 'model-v3' / 'f1-household' / 'f1_safe_grid.csv')) if r['point'] == 'median_mid'}
    same = [k for k in new if k in old]
    bad = [k for k in same if any(new[k][f] != old[k][f] for f in ('F1_pct', 'M2_short', 'M4a_short', 'taxes_retired'))]
    only_old = sorted(set(k[0] for k in old if k not in new))
    print(f'### Reproduction check: 6 phases, `median_mid`, F1 grid against 140c (`f1_safe_grid.csv`)\n\n{len(same)} cells (schedule x tolerance x margin) in both files; {len(bad)} differ in F1, M2, M4a or taxes retired. '
          f'Schedule points in 140c and not here: {", ".join(only_old) if only_old else "none"}; here and not in 140c: {", ".join(sorted(set(k[0] for k in new if k not in old))) or "none"}.')
    return 0 if not bad else 1


def run_years(a, legacy=False):
    lv, ctx, inp = F.setup()
    ns = [int(x) for x in a.phases.split(',')]
    mu = ctx.centre['I-D1a']
    print(('Legacy arm (083c: consumption share I-D14c, the fund earns the market return), central inputs' if legacy else 'Household arm, `safe` fund') + f', constant {mu}% path, GDP-per-head growth {100 * ctx.gdp_g:.2f}% a year; phase counts {ns}; percent of GDP; relief = M1a + M1b + M1c; diff = relief - M1d. Amplitude: max minus min over years '
          f'{CYCLE[0]} to {CYCLE[1]}. Every number is a scenario value at a labelled grid point, not a forecast. Death years for n phases: ceil(i * 30 / n), i = 1..n, then every 30 years: '
          + '; '.join(f'{n}: {sorted(set(int(np.ceil((i + 1) * 30 / n)) for i in range(n)))[:8]}...' for n in ns) + '.\n')
    pts = ('legacy',) if legacy else PTS
    res, rows, stats = {}, [], []
    for pn in pts:
        for sp in SPECS:
            for n in ns:
                F.log(f'{pn} {F.lab(sp)} phases {n}')
                line, s = const_run(ctx, inp, pn, sp, n, arm_ctx=ctx if legacy else None)
                res[pn, F.lab(sp), n] = line
                stats.append((pn, F.lab(sp), n, s))
                for y in range(YEARS):
                    rows.append((pn, F.lab(sp), n, y + 1, *[round(float(line[x][y]), 4) for x in ('M1a', 'M1b', 'M1c', 'relief', 'M1d')], round(float(line['relief'][y] - line['M1d'][y]), 4)))
    tag = 'legacy' if legacy else 'safe'
    F.write_csv(OUT / f'years_{tag}.csv', ('point', 'schedule', 'phases', 'year', 'M1a', 'M1b', 'M1c', 'relief', 'M1d', 'diff'), rows)
    srows = [(pn, sc, n, s['fill_year'], s['first_below'], s['years_below_10_40'], f'{s["M1a_amp"]:.2f}', f'{s["relief_amp"]:.2f}', f'{s["M1a_mean"]:.2f}', f'{s["relief_mean"]:.2f}', f'{s["M1d_end"]:.2f}',
              f'{s["P3_short"]:.2f}', f'{s["P3_100"]:.1f}') for pn, sc, n, s in stats]
    shead = ('point', 'schedule', 'phases', 'fill year', 'first year relief < M1d', f'years relief < M1d in {CYCLE[0]}-{CYCLE[1]}', f'M1a amplitude {CYCLE[0]}-{CYCLE[1]}', 'relief amplitude', 'M1a mean', 'relief mean', 'M1d year 40',
             'P3 to end of short window', 'P3 100 y')
    F.write_csv(OUT / f'years_{tag}_summary.csv', shead, srows)
    print('### Summary by phase count\n')
    print(F.tab(shead, srows))
    for pn in pts:
        for sp in SPECS:
            sc = F.lab(sp)
            print(f'\n### Years 1 to {YEARS}: `{pn}`, {sc}. M1a, relief and diff (relief - M1d) by phase count\n')
            head = ['year'] + [f'M1a {n}' for n in ns] + [f'relief {n}' for n in ns] + [f'diff {n}' for n in ns]
            body = []
            for y in range(YEARS):
                row = [y + 1]
                for x in ('M1a', 'relief'):
                    row += [f'{res[pn, sc, n][x][y]:.2f}' for n in ns]
                row += [f'{res[pn, sc, n]["relief"][y] - res[pn, sc, n]["M1d"][y]:.2f}' for n in ns]
                body.append(row)
            print(F.tab(head, body))
    print()
    return 0


def run_f1(a):
    """140c's F1 at `median_mid` (27 schedule points, `n` paths, the seed) with each phase count: the same code (`f1_household.run_f1`) inside `phases(n)`. Its tables and CSVs go to f1_phases_N/; this prints the comparison."""
    import contextlib
    import time
    from types import SimpleNamespace
    ns = [int(x) for x in a.phases.split(',')]
    res = {}
    for n in ns:
        d = OUT / f'f1_phases_{n}'
        d.mkdir(exist_ok=True)
        F.OUT = d
        t0 = time.time()
        with open(d / 'f1_safe_tables.md', 'w') as fh, contextlib.redirect_stdout(fh), phases(n):
            F.run_f1(SimpleNamespace(fund='safe', seed=a.seed, n=a.n, points='median_mid'))
        res[n] = time.time() - t0
        F.log(f'phases {n}: {res[n]:.0f} s')
    print(f'`median_mid`, household arm, `safe` fund, seed {a.seed}, {a.n} paths, 27 schedule points per phase count; the phase count is the only change. Run time is wall clock of one `f1` run (all of 27 schedule points, margins and the constant-path section).\n')
    rd = lambda n, f: list(csv.DictReader(open(OUT / f'f1_phases_{n}' / f)))
    print('### Best F1 by (tolerance, margin) and feasible cells\n')
    head = ['tol', 'm'] + [f'{n} phases: best F1 / passing M2, M4a / feasible' for n in ns]
    body = []
    for t in F.TOLS:
        for m in F.MARGINS:
            row = [f'{t:g}', f'{int(100 * m)}%']
            for n in ns:
                r = next(x for x in rd(n, 'f1_safe_summary.csv') if float(x['tol']) == t and float(x['margin']) == m)
                row.append(f"{float(r['best_F1_any']):.1f} / {float(r['best_F1_pass_M2_M4a']) if r['best_F1_pass_M2_M4a'] else float('nan'):.1f} / {r['feasible_points']} of {r['schedule_points_run']}")
            body.append(row)
    print(F.tab(head, body))
    print('\n### F1 at the 055c rule (tol 0, m 0) over the schedule points that ran, and cells that did not run\n')
    rows = []
    for n in ns:
        v = [float(x['F1_pct']) for x in rd(n, 'f1_safe_grid.csv') if float(x['tol']) == 0 and float(x['margin']) == 0]
        m2 = [float(x['M2_short']) for x in rd(n, 'f1_safe_grid.csv') if float(x['tol']) == 0 and float(x['margin']) == 0]
        try:
            nf = len(rd(n, 'f1_safe_failed.csv'))
        except FileNotFoundError:
            nf = 0
        rows.append((n, len(v), f'{min(v):.1f} to {max(v):.1f}' if v else 'none ran', f'{np.median(v):.1f}' if v else '', f'{min(m2):.2f} to {max(m2):.2f}' if m2 else '', nf, f'{res[n]:.0f} s'))
    print(F.tab(['phases', 'schedule points run', 'F1 range (tol 0, m 0)', 'median over points', 'M2 short range', 'cells that raised I1', 'run time'], rows))
    print('\n### Constant path: first shortfall year and P3 (`median_mid`; schedules tm50, tm70, tm90, k_ln 1, ratio 0.5)\n')
    rows = []
    for n in ns:
        for x in rd(n, 'f1_safe_constant_path.csv'):
            if x['point'] == 'median_mid':
                rows.append((n, x['schedule'], x['fill_year'], x['end_short_window'], x['first_year_relief_below_M1d'], x['inside_short_window'], x['P3_to_end_short_window'], x['P3_100y']))
    print(F.tab(['phases', 'schedule', 'fill year', 'end of short window', 'first year relief < M1d', 'inside short window', 'P3 to end of short window', 'P3 100 y'], rows))
    print()
    return 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('block', choices=('check', 'years', 'f1', 'legacy', 'checkf1'))
    ap.add_argument('--phases', default=None)
    ap.add_argument('--seed', type=int, default=20261118)
    ap.add_argument('--n', type=int, default=200)
    ap.add_argument('--out', default=None, help='folder for the outputs of `f1` (default: next to the script)')
    a = ap.parse_args()
    if a.out:
        OUT = Path(a.out)
        OUT.mkdir(parents=True, exist_ok=True)
    a.phases = a.phases or ('6,15,30' if a.block == 'f1' else ','.join(str(n) for n in PHASES))
    sys.exit({'check': run_check, 'years': run_years, 'f1': run_f1, 'legacy': lambda x: run_years(x, True), 'checkf1': run_checkf1}[a.block](a))
