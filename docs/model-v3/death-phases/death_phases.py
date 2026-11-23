"""
death_phases.py -- brief 149c: does the death-phase count cause the five-year cycle in M1a, and with it the F1 failure of 140c? Diagnosis only: no rule and no count is recommended, nothing in model_v3 changes.
=======================================================================================================================================================================================================
A one-off measurement, not part of model_v3. It imports the runner and the core read-only and imports 140c's script (`docs/model-v3/f1-household/f1_household.py`) for its setup, its scenario points and its `core`.
`runner.core_run` does not pass `n_phase` to `burden.line_flows` and `revenue.run_lines`, so `phases(n)` wraps those two module functions for the length of a run (a runtime wrapper; no file is edited) and sets `n_phase`.
The phase count is a numerical approximation of the age-at-death distribution (first deaths at ceil(i G / n_phase), then every G = 30 years), so its effect is read as a convergence study: does the answer settle as the count grows.

Run from the repository root (python -I):
    python -I docs/model-v3/death-phases/death_phases.py check                   the 6-phase rows reproduce 140c's constant-path numbers (about 10 s)
    python -I docs/model-v3/death-phases/death_phases.py years [--phases 6,10,15,30]    block 1: year-by-year tables on a constant path, CSV next to the script
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
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'docs' / 'model-v3' / 'f1-household'))

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
    print('\nAll equal.' if ok else '\nA CHECK FAILED.')
    return 0 if ok else 1


def run_years(a):
    lv, ctx, inp = F.setup()
    ns = [int(x) for x in a.phases.split(',')]
    mu = ctx.centre['I-D1a']
    print(f'Household arm, `safe` fund, constant {mu}% path, GDP-per-head growth {100 * ctx.gdp_g:.2f}% a year; phase counts {ns}; percent of GDP; relief = M1a + M1b + M1c; diff = relief - M1d. Amplitude: max minus min over years '
          f'{CYCLE[0]} to {CYCLE[1]}. Every number is a scenario value at a labelled grid point, not a forecast. Death years for n phases: ceil(i * 30 / n), i = 1..n, then every 30 years: '
          + '; '.join(f'{n}: {sorted(set(int(np.ceil((i + 1) * 30 / n)) for i in range(n)))[:8]}...' for n in ns) + '.\n')
    res, rows, stats = {}, [], []
    for pn in PTS:
        for sp in SPECS:
            for n in ns:
                F.log(f'{pn} {F.lab(sp)} phases {n}')
                line, s = const_run(ctx, inp, pn, sp, n)
                res[pn, F.lab(sp), n] = line
                stats.append((pn, F.lab(sp), n, s))
                for y in range(YEARS):
                    rows.append((pn, F.lab(sp), n, y + 1, *[round(float(line[x][y]), 4) for x in ('M1a', 'M1b', 'M1c', 'relief', 'M1d')], round(float(line['relief'][y] - line['M1d'][y]), 4)))
    F.write_csv(OUT / 'years_safe.csv', ('point', 'schedule', 'phases', 'year', 'M1a', 'M1b', 'M1c', 'relief', 'M1d', 'diff'), rows)
    srows = [(pn, sc, n, s['fill_year'], s['first_below'], s['years_below_10_40'], f'{s["M1a_amp"]:.2f}', f'{s["relief_amp"]:.2f}', f'{s["M1a_mean"]:.2f}', f'{s["relief_mean"]:.2f}', f'{s["M1d_end"]:.2f}',
              f'{s["P3_short"]:.2f}', f'{s["P3_100"]:.1f}') for pn, sc, n, s in stats]
    shead = ('point', 'schedule', 'phases', 'fill year', 'first year relief < M1d', f'years relief < M1d in {CYCLE[0]}-{CYCLE[1]}', f'M1a amplitude {CYCLE[0]}-{CYCLE[1]}', 'relief amplitude', 'M1a mean', 'relief mean', 'M1d year 40',
             'P3 to end of short window', 'P3 100 y')
    F.write_csv(OUT / 'years_safe_summary.csv', shead, srows)
    print('### Summary by phase count\n')
    print(F.tab(shead, srows))
    for pn in PTS:
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


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('block', choices=('check', 'years'))
    ap.add_argument('--phases', default=','.join(str(n) for n in PHASES))
    a = ap.parse_args()
    sys.exit({'check': run_check, 'years': run_years}[a.block](a))
