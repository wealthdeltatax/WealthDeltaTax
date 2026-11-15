"""test_dist.py — validation of rates_dist against the published anchors it is built on."""
import numpy as np
import rates_data as rd, rates_dist as dd

J = rd.load_jst(); u = rd.panel(J, 'GBR').loc[2017]
adults = float(u['pop']) * 1e3 / 1.27
res = []
def chk(n, ok, det=''):
    print(('PASS ' if ok else 'FAIL ') + n + '  ' + det); res.append(bool(ok))

for scen, mode in (('survey', 'add'), ('adjusted', 'add'), ('adjusted', 'reallocate')):
    d = dd.build(scen, adults, mode); ts = dd.top_shares(d); tag = f'[{scen}/{mode}]'
    chk(f'{tag} adult shares sum to 1', abs(d['share'].sum() - 1) < 1e-12)
    chk(f'{tag} wealth sums to total', abs(d['wealth_bn'].sum() - d['total_bn']) < 1e-6)
    chk(f'{tag} cell means non-decreasing', np.all(np.diff(d['mean_gbp_m']) >= 0),
        f"repaired cells {d['repaired_cells']}")
    if scen == 'survey':
        chk(f'{tag} total = ONS £14.6tn', abs(d['total_bn'] - dd.ONS_TOTAL_BN) < 1e-6)
        chk(f'{tag} top 1% = table 14.2%', abs(ts[.01] - 0.1423) < 2e-3)
    else:
        chk(f'{tag} top 1% = 22.5%', abs(ts[.01] - 0.225) < 2e-3, f'{ts[.01]:.4f}')
        chk(f'{tag} top 0.1% = 9%', abs(ts[1e-3] - 0.09) < 2e-3, f'{ts[1e-3]:.4f}')
        rl = sum(w for l, w in zip(d['labels'], d['wealth_bn']) if l.startswith('RichList'))
        n = sum(a for l, a in zip(d['labels'], d['share']) if l.startswith('RichList')) * adults
        chk(f'{tag} Rich List = £772.8bn, 350 people', abs(rl - 772.8) < 1e-6 and abs(n - 350) < 1e-6)
    if mode == 'reallocate':
        chk(f'{tag} total held at ONS', abs(d['total_bn'] - dd.ONS_TOTAL_BN) < 1e-6)

# --- advani scenario: reproduces the published anchors ---
for v, (s10, s1, tot) in (('central', (0.5333, 0.2190, 15120.0)), ('upper', (0.5399, 0.2300, 15335.0))):
    d = dd.build('advani', adults, v); ts = dd.top_shares(d); tag = f'[advani/{v}]'
    chk(f'{tag} cell means strictly increasing, shares sum to 1',
        np.all(np.diff(d['mean_gbp_m']) > 0) and abs(d['share'].sum() - 1) < 1e-12)
    chk(f'{tag} total = £{tot:,.0f}bn', abs(d['total_bn'] - tot) < 1.0, f"{d['total_bn']:,.1f}")
    chk(f'{tag} top 10% = {s10:.1%} (paper: 51% survey -> 55% adjusted; upper variant is ~1pp short of the 55% in the paper)', abs(ts[.10] - s10) < 2e-3, f'{ts[.10]:.4f}')
    chk(f'{tag} top 1% = {s1:.1%} (paper: 18% survey -> 23% adjusted)', abs(ts[.01] - s1) < 2e-3, f'{ts[.01]:.4f}')
    rl = sum(w for l, w in zip(d['labels'], d['wealth_bn']) if l.startswith('RichList'))
    n = sum(a for l, a in zip(d['labels'], d['share']) if l.startswith('RichList')) * adults
    chk(f'{tag} Rich List tier = £700bn, 1000 families', abs(rl - 700) < 1e-6 and abs(n - 1000) < 1e-6)
    chk(f'{tag} tail index alpha in [1.5, 1.8] and top 0.1% in [8%, 11%]',
        1.5 < d['params']['alpha_tail'] < 1.8 and 0.08 < ts[1e-3] < 0.11,
        f"alpha {d['params']['alpha_tail']:.2f}, top0.1% {ts[1e-3]:.3f}")
d0 = dd.build('advani', adults, 'central'); d1 = dd.build('advani', adults, 'central', wealth_scale=0.5)
chk('[advani] wealth_scale rescales £ and leaves shares unchanged',
    abs(d1['total_bn'] / d0['total_bn'] - 0.5) < 1e-9 and abs(dd.top_shares(d1)[.01] - dd.top_shares(d0)[.01]) < 1e-12)

a, s = dd.build('adjusted', adults, 'add'), dd.build('survey', adults, 'add')
chk('add mode leaves the body (below top 1%) at survey levels',
    abs(a['wealth_bn'][:14].sum() - s['wealth_bn'][:14].sum()) < 1e-6)
chk('threshold by percentile is decreasing in the fraction',
    dd.wealth_at_top_fraction(a, .05) < dd.wealth_at_top_fraction(a, .02) < dd.wealth_at_top_fraction(a, .01))
print('\nALL PASS' if all(res) else '\nSOME FAILED')
raise SystemExit(0 if all(res) else 1)
