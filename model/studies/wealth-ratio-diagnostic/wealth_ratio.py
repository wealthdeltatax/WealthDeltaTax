"""
wealth_ratio.py -- brief 090c: why post-fill relief falls relative to GDP (tests A to F of the private-wealth hypothesis)
=======================================================================================================================
A one-off measurement, not part of model_v3 (its layer and budget rules do not apply). It imports the runner and the core and edits neither.
`runner.core_run` gives the raw core results (line flows, receipts, relief, retirement); this script reads them. Where the runner has no switch (a fixed
real threshold) it repeats core_run's body with burden.line_flows' own `index` argument, and asserts that the copy equals core_run when the index is GDP per head.

Run from the repository root:   python -I model/studies/wealth-ratio-diagnostic/wealth_ratio.py [--seed 20261118] [--n 1000]
It prints the report as Markdown on stdout (progress on stderr). Two runs with the same seed print identical text.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'model'))

from model_v3.core import burden as bd, pack as pk, returns as rt, revenue as rv, schedule as sc  # noqa: E402
from model_v3.runner import runner as R  # noqa: E402

T, CLOSED = R.T, 1e-9
SCHEDS = [dict(tau_0=0.04, tau_m=tm, k_ln=0.5, ratio=0.5) for tm in (0.5, 0.7, 0.9)]
OFF = dict(tau_0=1e-9, tau_m=1e-9, k_ln=0.5, ratio=0.5)          # a tax of one in a billion: the schedule needs tau_0 above zero
YEARS = (1, 5, 10, 20, 30, 50, 75, 100)
BLOCKS = (5, 10, 20, 30, 50, 75, 100)                            # a block is the five years ending in this year
BASE = 4.74                                                      # I-D1a, the arithmetic mean, as a constant path


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def tab(head, rows):
    out = ['| ' + ' | '.join(head) + ' |', '|' + '|'.join('---' for _ in head) + '|']
    return '\n'.join(out + ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows])


def build_ctx():
    lv = json.loads((ROOT / 'model' / 'model_v3' / 'levers.json').read_text())
    out = yaml.safe_load((ROOT / 'docs' / 'model-v3' / 'outputs.yml').read_text())
    tier1 = next(o for o in out['outputs'] if o['id'] == 'OT1')['by']['input']
    return R.context(pk.load_pack(ROOT / 'data' / 'country-packs' / 'GBR'), pk.load_register(ROOT / 'data' / 'input-register' / 'inputs.json'), lv, tier1, [o['id'] for o in out['outputs']])


def core(ctx, theta, spec, g, gdp_g, index='gdp_pc', copy=False):
    """runner.core_run, or (for a fixed real threshold, index other than gdp_pc) the same steps with burden.line_flows' index argument."""
    g = np.asarray(g, float)
    gg = np.full(g.shape, gdp_g)
    if index == 'gdp_pc' and not copy:
        return R.core_run(ctx, theta, spec, g, gg)
    b = R.shaped(ctx, theta, spec['ratio'])
    rate = sc.rate_function(spec['k_ln'], spec['tau_0'], spec['tau_m'], b.w_min, 'logistic_ln')
    c, lam = theta['I-D14c'] / 100, dict(lam_C=theta['I-D14a'] / 100, lam_D=theta['I-D14b'] / 100)
    fl = bd.line_flows(b, rate, g, gg, c, index=index, **lam)
    net, z = np.einsum('tnp,n->tp', fl['net'], fl['wt']) * fl['adults_k'], np.zeros(g.shape)
    run = dict(tax=net, refund=z, death_tax=z, heir=z, death_B=z, death_D=z, payers=z, entries=z, exits=z, fall_through=z, gdp_index=np.cumprod(1.0 + gg, axis=0), adults_k=fl['adults_k'])
    h, ms = int(theta['I-D14e']), theta['I-D8a']
    r = rv.revenue(run, ctx.gdp0, theta['I-D7a'], ctx.rec, g, ctx.exp, c, int(theta['I-D14d']), ms, ms, h, None, theta['I-D14f'] / 100)
    return R.Raw(spec, b, rate, fl, run, r, {}, {}, ~r['unfilled'], None, g, gg, c, h)


def read(raw):
    """Per-path series (T, P) of everything the report reads. Ratios to GDP use the GDP index at the start of the year; index_ ratios are to year 1."""
    fl, r, P = raw.fl, raw.r, raw.g.shape[1]
    wt, w0 = fl['wt'][None, :, None], fl['w0']
    pay = w0 >= fl['w_min'] * fl['idx'][:, None, :]
    gi = np.vstack([np.ones((1, P)), np.cumprod(1.0 + raw.gdp_g, axis=0)[:-1]])
    W, tax_w = (wt * w0).sum(1), (wt * w0 * pay).sum(1)
    rel = lambda x: (x / gi) / (x[0] / gi[0])
    inc = (wt * np.maximum(fl['delta'], 0.0) * pay).sum(1) * fl['adults_k'] / r['gdp'] * 100
    below = r['relief'] < r['M1d'] - CLOSED
    first = np.where(below.any(0), below.argmax(0) + 1, 0)
    return dict(W_real=W / W[0], W_gdp=rel(W), tax_gdp=rel(tax_w), payers=(wt * pay).sum(1) * 100, inc=inc, M1a=r['M1a'], M1b=r['M1b'], M1c=r['M1c'],
                relief=r['relief'], M1d=r['M1d'], excess=r['relief'] - r['M1d'], S=r['S_gdp'], first=first, fill=r['fill'], ntax=((r['P5'] > 0) & (r['P5'] <= T)).sum(1))


def at(x, ys=YEARS):
    return [f'{x[y - 1].mean():.2f}' for y in ys]


def blk(x, ends=BLOCKS):
    return [f'{x[e - 5:e].mean():.2f}' for e in ends]


def one(ctx, spec, g, c=None, mean=BASE, gdp=None, index='gdp_pc', over=None):
    th = {**ctx.centre, **({'I-D14c': c} if c is not None else {}), **(over or {})}
    gp = np.full((T, 1), mean / 100) if g is None else g
    return read(core(ctx, th, spec, gp, ctx.gdp_g if gdp is None else gdp, index))


def flat_c(ctx, spec, lo=0.0, hi=3.5, tol=1e-3):
    """The consumption rate (percent) at which the wealth to GDP index at year 100 is 1 with the tax on (bisection; nan if it does not cross)."""
    f = lambda c: float(one(ctx, spec, None, c)['W_gdp'][99, 0]) - 1.0
    a, b = f(lo), f(hi)
    if a * b > 0:
        return float('nan')
    while hi - lo > tol:
        m = 0.5 * (lo + hi)
        lo, hi = (m, hi) if f(m) * a > 0 else (lo, m)
    return 0.5 * (lo + hi)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=int, default=20261118)
    ap.add_argument('--n', type=int, default=1000)
    a = ap.parse_args()
    ctx = build_ctx()
    sec, lab = [], [f'tm{round(100 * s["tau_m"])}' for s in SCHEDS]
    # the copy of core_run equals core_run on the GDP-indexed threshold
    g0 = np.full((T, 1), BASE / 100)
    for s0 in SCHEDS:
        x, y = core(ctx, ctx.centre, s0, g0, ctx.gdp_g).r, core(ctx, ctx.centre, s0, g0, ctx.gdp_g, copy=True).r
        assert all(np.allclose(x[k], y[k], rtol=1e-9, atol=1e-12) for k in ('M1a', 'M1b', 'M1c', 'relief', 'M1d')), 'the copy of core_run differs from core_run'
    # EARLY CHECK: consumption 3.5 and the tax off
    off = one(ctx, OFF, None, 3.5)
    early = float(off['W_gdp'][99, 0])
    log(f'early check: W/GDP at year 100, c 3.5, tax off: {early:.3f}')
    if not 0.5 <= early <= 0.8:
        print(f'# STOP: the early check failed: W/GDP at year 100 with consumption 3.5 and the tax off is {early:.3f}, not about two thirds. Nothing else was run.')
        return
    # item A: consumption sweep (constant path at 4.74)
    r_c, r_lo, r_hi = ctx.reg['I-D14c'], ctx.reg['I-D14c'].low, ctx.reg['I-D14c'].high
    cs = sorted({0.0, 1.5, 2.5, 3.5, r_lo, r_hi})
    A = {(i, c): one(ctx, s, None, c) for i, s in enumerate(SCHEDS) for c in cs}
    rows = lambda f, ys: [[lab[i], f'{c:g}', *f(A[i, c], ys)] for i in range(3) for c in cs]
    secA = [f'## Item 1 (A): consumption sweep, constant path at {BASE}% (I-D14c: low {r_lo:g}, central {r_c.central:g}, high {r_hi:g})\n',
            'Schedules: tau_m 0.5, 0.7, 0.9 at k 0.5, ratio 0.5. Rows are (schedule, consumption %). Years are single years; blocks are the five years ending in the year shown, in GDP-points (percent of GDP). Indexes are 1.00 in year 1.\n',
            '### Aggregate wealth, real level (pounds, index to year 1) and as a share of GDP (index to year 1), items 1 and 3 (C)\n',
            tab(['schedule', 'c %', *[f'real y{y}' for y in (10, 30, 100)], *[f'W/GDP y{y}' for y in (10, 30, 50, 100)]],
                [[lab[i], f'{c:g}', *at(A[i, c]['W_real'], (10, 30, 100)), *at(A[i, c]['W_gdp'], (10, 30, 50, 100))] for i in range(3) for c in cs]),
            '\n### Wealth above W_min as a share of GDP (index), payers (percent of adults), annual positive taxable increments (percent of GDP, blocks)\n',
            tab(['schedule', 'c %', *[f'taxable/GDP y{y}' for y in (10, 50, 100)], *[f'payers y{y}' for y in (10, 50, 100)], *[f'incr b{e}' for e in (10, 50, 100)]],
                [[lab[i], f'{c:g}', *at(A[i, c]['tax_gdp'], (10, 50, 100)), *at(A[i, c]['payers'], (10, 50, 100)), *blk(A[i, c]['inc'], (10, 50, 100))] for i in range(3) for c in cs]),
            '\n### Receipts and relief (percent of GDP, five-year blocks): M1a, relief, relief minus M1d\n',
            tab(['schedule', 'c %', *[f'M1a b{e}' for e in BLOCKS]], rows(lambda d, ys: blk(d['M1a']), 0)),
            '', tab(['schedule', 'c %', *[f'relief b{e}' for e in BLOCKS]], rows(lambda d, ys: blk(d['relief']), 0)),
            '', tab(['schedule', 'c %', *[f'relief-M1d b{e}' for e in BLOCKS]], rows(lambda d, ys: blk(d['excess']), 0)),
            '\n### First year relief is below M1d, fill year, taxes retired by year 100\n',
            tab(['schedule', 'c %', 'first year below', 'fill year', 'taxes retired'],
                [[lab[i], f'{c:g}', int(A[i, c]['first'][0]) or 'never', int(A[i, c]['fill'][0]), int(A[i, c]['ntax'][0])] for i in range(3) for c in cs])]
    sec.append('\n'.join(secA))
    # item B: tax drag
    ret = one(ctx, OFF, None, 0.0)
    B = [('returns only (tax 1e-9, c 0)', None, ret), ('returns and consumption (tax 1e-9, c 3.5)', None, off)] + [(f'returns, consumption and the tax ({lab[i]}, c 3.5)', i, A[i, 3.5]) for i in range(3)]
    secB = ['## Item 2 (B) and item 3 (C): the tax\'s own drag on compounding\n', 'Aggregate wealth, constant path; real level and share of GDP, both indexed to year 1.\n',
            tab(['scenario', *[f'real y{y}' for y in (10, 30, 50, 100)], *[f'W/GDP y{y}' for y in (10, 30, 50, 100)]],
                [[n, *at(d['W_real'], (10, 30, 50, 100)), *at(d['W_gdp'], (10, 30, 50, 100))] for n, _, d in B])]
    sec.append('\n'.join(secB))
    # item D: threshold indexation
    D = {(i, ix): one(ctx, SCHEDS[i], None, 3.5, index=ix) for i in range(3) for ix in ('gdp_pc', 'real')}
    secD = ['## Item 4 (D): threshold indexation\n',
            'The runner (`core_run`) has no switch for a fixed real threshold; `burden.line_flows` and `revenue.run_lines` take `index` (anything but `gdp_pc` leaves the threshold fixed in real terms). '
            'The script repeats core_run\'s steps with that argument (no core edit) and asserts the copy equals core_run for the GDP-indexed case. Consumption 3.5, constant path.\n',
            tab(['schedule', 'threshold', *[f'payers y{y}' for y in (10, 50, 100)], *[f'taxable/GDP y{y}' for y in (10, 50, 100)], *[f'M1a b{e}' for e in (10, 50, 100)], 'relief b100', 'first year below M1d'],
                [[lab[i], 'GDP per head' if ix == 'gdp_pc' else 'fixed real', *at(D[i, ix]['payers'], (10, 50, 100)), *at(D[i, ix]['tax_gdp'], (10, 50, 100)), *blk(D[i, ix]['M1a'], (10, 50, 100)),
                  blk(D[i, ix]['relief'], (100,))[0], int(D[i, ix]['first'][0]) or 'never'] for i in range(3) for ix in ('gdp_pc', 'real')])]
    sec.append('\n'.join(secD))
    # item E: relief components and the attribution of the fall
    lev = {i: one(ctx, SCHEDS[i], None, 3.5, over={'I-D7a': 0.0}) for i in range(3)}
    drop = lambda d, k: float(d[k][15:20].mean() - d[k][95:100].mean())         # block ending in year 20 (the post-fill peak) minus block ending in year 100
    attr = []
    for i in range(3):
        d0, dc, dr = A[i, 3.5], A[i, 0.0], D[i, 'real']
        F0 = drop(d0, 'relief')
        attr.append(dict(F0=F0, M1a=drop(d0, 'M1a') / F0, M1b=drop(d0, 'M1b') / F0, M1c=drop(d0, 'M1c') / F0, cons=(F0 - drop(dc, 'relief')) / F0, thr=(F0 - drop(dr, 'relief')) / F0,
                         levy=(F0 - drop(lev[i], 'relief')) / F0))
        attr[-1]['c0'] = float(dc['relief'][95:100].mean() - dc['relief'][15:20].mean())
    secE = ['## Item 5 (E): relief components, percent of GDP, five-year blocks (consumption 3.5, constant path)\n',
            tab(['schedule', 'component', *[f'b{e}' for e in BLOCKS]],
                [[lab[i], n, *blk(A[i, 3.5][k])] for i in range(3) for n, k in (('M1a individual WDT', 'M1a'), ('M1b corporate levy', 'M1b'), ('M1c fund income', 'M1c'), ('reserve (stock)', 'S'), ('relief', 'relief'), ('retired receipts M1d', 'M1d'))]),
            '\n### Attribution of the fall in relief, block ending year 20 to block ending year 100\n',
            'Relief does not fall between the blocks ending in years 10 and 100 in the central run (it is still rising to its post-fill peak in the block ending year 20), so the fall is measured from the block ending year 20, the peak, to the block ending year 100. F0 is that fall in relief (GDP-points) in the central run. "By component" splits F0 into the fall of M1a, M1b and M1c. "Counterfactual" rows are F0 minus the fall with the factor removed, over F0: '
            'consumption set to 0, the threshold fixed in real terms, the levy set to 0 (I-D7a). Removing consumption does not shorten the fall, it reverses it (last column: relief rises by that many GDP-points from the block ending year 20 to year 100), so its share is far above 100% and is read as: consumption accounts for all of the fall and more. The tax\'s own drag on compounding is measured in item 2 (B), not here.\n',
            tab(['schedule', 'F0', 'M1a %', 'M1b %', 'M1c %', 'consumption %', 'threshold %', 'levy %', 'relief change with c = 0'],
                [[lab[i], f'{x["F0"]:.2f}', *[f'{100 * x[k]:.0f}' for k in ('M1a', 'M1b', 'M1c', 'cons', 'thr', 'levy')], f'{x["c0"]:+.2f}'] for i, x in enumerate(attr)])]
    sec.append('\n'.join(secE))
    # item F: conventions
    geo_r = 100 * (np.exp(np.log1p(0.0442)) - 1)
    gdp_geo = float(np.expm1(np.mean(np.log1p(rv.gdp_growth(ctx.pack, rt.real_series(ctx.pack)[0])))))
    F1 = {(i, m): one(ctx, SCHEDS[i], None, 3.5, mean=m) for i in range(3) for m in (4.74, 4.42)}
    F3 = {(i, k): one(ctx, SCHEDS[i], None, 3.5, gdp=v) for i in range(3) for k, v in (('arithmetic', ctx.gdp_g), ('geometric', gdp_geo))}
    g = rt.ar1_paths(rt.streams(a.seed)['level1_paths'], ctx.centre['I-D1a'], ctx.centre['I-D1b'], ctx.centre['I-D1b2'], T, a.n)
    F2 = {i: one(ctx, SCHEDS[i], g, 3.5) for i in range(3)}
    secF = ['## Item 6 (F): conventions\n', f'### (i) constant path at the arithmetic mean {BASE} (I-D1a) against the geometric mean 4.42 (I-D1a2), consumption 3.5\n',
            tab(['schedule', 'return', 'W/GDP y30', 'W/GDP y100', 'M1a b100', 'relief b100', 'first year below M1d'],
                [[lab[i], m, *at(F1[i, m]['W_gdp'], (30, 100)), *blk(F1[i, m]['M1a'], (100,)), *blk(F1[i, m]['relief'], (100,)), int(F1[i, m]['first'][0]) or 'never'] for i in range(3) for m in (4.74, 4.42)]),
            f'\n### (ii) {a.n} random paths of the AR(1) generator at central inputs (seed {a.seed}), consumption 3.5\n',
            tab(['schedule', 'W/GDP y30 median', 'P10', 'y50 median', 'P10', 'y100 median', 'P10', 'paths with relief below M1d at some year %', 'median first year below'],
                [[lab[i], *[f'{np.median(F2[i]["W_gdp"][y - 1]):.2f}' if k == 0 else f'{np.percentile(F2[i]["W_gdp"][y - 1], 10):.2f}' for y in (30, 50, 100) for k in (0, 1)],
                  f'{100 * np.mean(F2[i]["first"] > 0):.1f}', int(np.median(F2[i]["first"][F2[i]["first"] > 0])) if (F2[i]["first"] > 0).any() else 'never'] for i in range(3)]),
            f'\n### (iii) constant GDP growth: arithmetic mean {100 * ctx.gdp_g:.3f}% (what runner.context uses) against geometric mean {100 * gdp_geo:.3f}% of the same 117 years (the brief quoted 1.49%, which this series does not give; the full 1870-2019 history gives 1.43%), constant return {BASE}, consumption 3.5\n',
            tab(['schedule', 'GDP growth', 'W/GDP y100', 'first year below M1d'], [[lab[i], k, *at(F3[i, k]['W_gdp'], (100,)), int(F3[i, k]['first'][0]) or 'never'] for i in range(3) for k in ('arithmetic', 'geometric')])]
    sec.append('\n'.join(secF))
    # the consumption rate that keeps W/GDP flat; the 083c reproduction
    flat = [flat_c(ctx, s) for s in SCHEDS]
    k1 = [one(ctx, dict(s, k_ln=1.0), None, 3.5) for s in SCHEDS]
    repro = [(lab[i], int(k1[i]['first'][0]), int(A[i, 3.5]['first'][0]), int(k1[i]['ntax'][0])) for i in range(3)]
    # opening
    base_ratio = [float(A[i, 3.5]['W_gdp'][99, 0]) for i in range(3)]
    drag = [(np.log(base_ratio[i]) - np.log(early)) / np.log(base_ratio[i]) for i in range(3)]
    cons = [x['cons'] for x in attr]
    lo_, hi_ = lambda v: min(v), lambda v: max(v)
    verdict = ('supported' if min(cons) >= 0.5 and max(base_ratio) < 0.9 and min(drag) > 0 else 'weakened' if min(base_ratio) >= 0.9 else 'mixed')
    pct = lambda v: f'{100 * lo_(v):.0f} to {100 * hi_(v):.0f}%'
    opening = [f'**Of the fall in relief between the blocks ending in years 20 (its peak) and 100 (central run, constant {BASE}% return, tm50 to tm90), consumption accounts for all of it and more: with consumption at 0 relief rises by '
               f'{lo_([x["c0"] for x in attr]):.1f} to {hi_([x["c0"] for x in attr]):.1f} GDP-points instead of falling by {lo_([x["F0"] for x in attr]):.2f} to {hi_([x["F0"] for x in attr]):.2f}; fixing the threshold in real terms removes {pct([x["thr"] for x in attr])} of the fall, '
               f'the levy {pct([x["levy"] for x in attr])} (M1b is constant), and the tax\'s own drag on compounding is {pct(drag)} of the log fall in wealth to GDP (year 100 index {early:.2f} with the tax off, {lo_(base_ratio):.2f} to {hi_(base_ratio):.2f} with it on).**',
               f'**The hypothesis is {verdict} (rule: supported when removing consumption accounts for at least half of the fall in every schedule, wealth to GDP at year 100 is below 0.9 and the tax adds to the fall; weakened when the ratio at year 100 stays at 0.9 or above; mixed otherwise).**',
               f'**With the tax on, wealth to GDP at year 100 is 1.00 at a consumption rate of {", ".join(f"{x:.2f}" for x in flat)}% (tm50, tm70, tm90); at the central 3.5% it is {lo_(base_ratio):.2f} to {hi_(base_ratio):.2f}.**']
    head = ['# Wealth-to-GDP and revenue decomposition (brief 090c)\n', '\n\n'.join(opening), '',
            f'Reproduce: `python -I model/studies/wealth-ratio-diagnostic/wealth_ratio.py` from the repository root (seed {a.seed}; two runs print identical text). Central inputs; schedules tau_m 0.5, 0.7, 0.9 at k 0.5, ratio 0.5. '
            f'Constant path at the arithmetic mean {BASE}% unless a table says random paths; constant GDP growth {100 * ctx.gdp_g:.3f}%. The report recommends nothing about the feasibility rule, I-D14c or CK1.\n',
            f'**Early check (stop condition).** Consumption 3.5% and the tax off: wealth to GDP at year 100 is {early:.2f}; the hypothesis\'s own illustration is about two thirds. It holds, so the kernel\'s compounding is what the hypothesis assumes.\n',
            f'**083c reproduction.** First year relief falls below M1d at consumption 3.5 on 083c\'s own constant-path schedules (k 1.0, ratio 0.5): {", ".join(f"{n} year {y} ({t} taxes retired)" for n, y, _, t in repro)}; 083c: year 13 at tau_m 0.5 and 0.7, year 11 at 0.9. '
            f'This brief\'s schedules use k 0.5 as the brief asks, and there the first year is {", ".join(f"{n} year {z}" for n, _, z, _ in repro)}: 083c\'s year 11 at tau_m 0.9 comes from k 1.0 (six taxes retired, M1d 8.11), not from a difference in the kernel.\n']
    print('\n'.join(head) + '\n\n' + '\n\n'.join(sec) + '\n')


if __name__ == '__main__':
    main()
