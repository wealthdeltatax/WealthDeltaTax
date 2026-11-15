"""
d1_identity.py: D1 gate rerun and identity-route c per country (job J2).

Inputs (all in the repo):
  audit_d0/usable_years.csv         JST usable years per country and set (LEVY used)
  audit_d0/Research/1a WID_...csv   WID headline series (apweal = net private wealth, anninc = national income)
  jst_r6.json                       JST file, read through wdt_jst.load_jst
Rules, from decision_log.md (14, 16 and 17 Oct):
  * WID is primary everywhere. A country's usable years are JST LEVY usable years from the first
    year all of pwfin, pwnfa, pwdeb exist (WID_Data_Guide section 4; the larger of the starts).
  * Runs are contiguous calendar years. DEU and NLD runs are split at 1979/80.
  * Per-run minimum 20 retained years; pooling weight = retained overlap years (no cap).
  * Gate: at least 50 retained years in at least 8 of the 16 countries.
  * Identity route: c = 1 - (1 + g_WY)(1 + g_pc) / (1 + r) per run, where g_WY is the geometric growth of
    WID W/Y between the run's first and last year, g_pc the geometric real GDP-per-head growth and r the
    geometric real capital return (both from wdt_jst.real_basis_inputs over the run's growth years).
  * Sensitivity (--debt): drop DEU 1980-95 and GBR 1980-87 (WID debt data quality 1) before building runs.
Not applied: half-year alignment of WID mid-year averages (D1 decision log 4); the denominator is WID net
national income, JST growth is GDP per head (D1 decision log 5). Both are flagged in the output.
Run:  python audit_d0/d1_identity.py [--debt]
"""

import argparse
import collections
import csv
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from wdt_jst import load_jst, real_basis_inputs  # noqa: E402

MIN_RUN = 20
GATE_YEARS = 50
GATE_COUNTRIES = 8

ISO = {'Australia': 'AUS', 'Switzerland': 'CHE', 'Germany': 'DEU', 'Denmark': 'DNK', 'Spain': 'ESP',
       'Finland': 'FIN', 'France': 'FRA', 'United Kingdom': 'GBR', 'Italy': 'ITA', 'Japan': 'JPN',
       'Netherlands': 'NLD', 'Norway': 'NOR', 'Sweden': 'SWE', 'USA': 'USA'}
# First year of the private balance-sheet components, the larger of pwfin/pwdeb and pwnfa (WID_Data_Guide section 4).
COMP_START = {'AUS': 1977, 'CHE': 1980, 'DEU': 1954, 'DNK': 1973, 'ESP': 1901, 'FIN': 1980, 'FRA': 1970,
              'GBR': 1920, 'ITA': 1966, 'JPN': 1970, 'NLD': 1880, 'NOR': 1979, 'SWE': 1811, 'USA': 1913}
SPLIT_1980 = {'DEU', 'NLD'}
DEBT_DROP = {'DEU': range(1980, 1996), 'GBR': range(1980, 1988)}
ALL16 = ['AUS', 'BEL', 'CAN', 'CHE', 'DEU', 'DNK', 'ESP', 'FIN', 'FRA', 'GBR', 'IRL', 'ITA', 'JPN', 'NLD', 'NOR',
         'PRT', 'SWE', 'USA']


def load_wid():
    path = HERE / 'Research' / '1a WID_Data_16102026-111858.csv'
    rows = list(csv.reader(open(path, encoding='utf-8-sig'), delimiter=';'))[2:]
    d = collections.defaultdict(dict)
    for r in rows:
        if len(r) < 6 or not r[4].strip():
            continue
        code = r[1].split('\n')[0]
        if code.startswith(('apweal_pall_999_i', 'anninc_pall_999_i')):
            d[(ISO[r[0].strip()], code[:6])][int(r[3])] = float(r[4])
    return d


def load_usable(set_name='LEVY'):
    out = collections.defaultdict(list)
    for r in csv.DictReader(open(HERE / 'usable_years.csv')):
        if r['set'] == set_name:
            out[r['country']].append(int(r['year']))
    return {k: sorted(v) for k, v in out.items()}


def runs_of(years):
    runs, cur = [], []
    for y in sorted(years):
        if cur and y != cur[-1] + 1:
            runs.append(cur)
            cur = []
        cur.append(y)
    if cur:
        runs.append(cur)
    return runs


def build_runs(iso, years, debt):
    ys = [y for y in years if y >= COMP_START[iso]]
    if debt and iso in DEBT_DROP:
        ys = [y for y in ys if y not in DEBT_DROP[iso]]
    if iso in SPLIT_1980:
        out = []
        for part in ([y for y in ys if y < 1980], [y for y in ys if y >= 1980]):
            out += runs_of(part)
    else:
        out = runs_of(ys)
    return [r for r in out if len(r) >= MIN_RUN]


def solve_c(J, wid, iso, run):
    w, y = wid[(iso, 'apweal')], wid[(iso, 'anninc')]
    y0, y1 = run[0], run[-1]
    n = y1 - y0
    wy0, wy1 = w[y0] / y[y0], w[y1] / y[y1]
    g_wy = (wy1 / wy0) ** (1.0 / n) - 1.0
    b = real_basis_inputs(J, iso, years=run[1:])
    c = 1.0 - (1.0 + g_wy) * (1.0 + b['index_rate']) / (1.0 + b['g_real'])
    return {'n_steps': n, 'wy_start': wy0, 'wy_end': wy1, 'g_wy': g_wy, 'g_pc': b['index_rate'],
            'r': b['g_real'], 'c': c, 'steps_used': b['n']}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--debt', action='store_true', help='drop DEU 1980-95 and GBR 1980-87')
    ap.add_argument('--out', default=str(HERE))
    a = ap.parse_args()
    J = load_jst('jst_r6.json')
    wid = load_wid()
    usable = load_usable('LEVY')
    tag = '_debt' if a.debt else ''

    run_rows, country = [], {}
    for iso in sorted(COMP_START):
        retained = 0
        for i, run in enumerate(build_runs(iso, usable.get(iso, []), a.debt), 1):
            s = solve_c(J, wid, iso, run)
            retained += len(run)
            run_rows.append({'country': iso, 'run': i, 'first': run[0], 'last': run[-1], 'retained': len(run), **s})
        country[iso] = retained

    passing = [c for c in ALL16 if country.get(c, 0) >= GATE_YEARS]

    def pool(rows):
        wt = sum(r['retained'] for r in rows)
        return sum(r['c'] * r['retained'] for r in rows) / wt if wt else float('nan')

    pooled_all = pool(run_rows)
    pooled_ex_nor = pool([r for r in run_rows if r['country'] != 'NOR'])
    pooled_pass = pool([r for r in run_rows if r['country'] in passing])

    with open(Path(a.out) / f'd1_identity_runs{tag}.csv', 'w', newline='') as fh:
        wr = csv.DictWriter(fh, fieldnames=list(run_rows[0]))
        wr.writeheader()
        for r in run_rows:
            wr.writerow({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()})

    cc = Path(a.out) / f'c_country{tag}.csv'
    with open(cc, 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(['country', 'c', 'span', 'route', 'grade', 'retained_years', 'passes_gate', 'flags'])
        for iso in ALL16:
            rows = [r for r in run_rows if r['country'] == iso]
            ok = country.get(iso, 0) >= GATE_YEARS
            if ok:
                c, span, route, grade = pool(rows), f"{min(r['first'] for r in rows)}-{max(r['last'] for r in rows)}", 'identity', 'B'
                flags = 'strict grade; WID headline back-cast excluded; no half-year alignment'
            else:
                c, span, route, grade = pooled_all, '', 'pooled', 'C'
                flags = 'pooled c; fails 50-year test or no WID series'
                if iso == 'NOR':
                    flags += '; Norway wealth definition unconfirmed'
            wr.writerow([iso, round(c, 5), span, route, grade, country.get(iso, 0), ok, flags])

    print(f"Set LEVY, {'debt-year sensitivity' if a.debt else 'base'}; run minimum {MIN_RUN}")
    print(f"{'country':8}{'retained':>9}{'gate':>6}{'c (own)':>10}")
    for iso in ALL16:
        rows = [r for r in run_rows if r['country'] == iso]
        own = pool(rows) if rows else float('nan')
        print(f"{iso:8}{country.get(iso, 0):9d}{'pass' if iso in passing else 'fail':>6}{own:10.4f}")
    print(f"Gate: {len(passing)} of 16 (threshold {GATE_COUNTRIES}); passing {passing}")
    print(f"Pooled c: all retained runs {pooled_all:.4f}; excluding NOR {pooled_ex_nor:.4f}; passing countries only {pooled_pass:.4f}")


if __name__ == '__main__':
    main()
