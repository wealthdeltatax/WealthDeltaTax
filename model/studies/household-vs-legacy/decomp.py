"""
decomp.py -- brief 136c, block 2: the revenue and burden outputs of the household and legacy arms written as base x rate, and the fund path split into its flows. Diagnosis only: nothing in the model is changed; both arms run through
`core_run`, the outputs are rebuilt from the kernel flows (`fl`) and revenue's result (`r`) and checked against the outputs `headlines` gives (and, for the household arm, against the 124c grid).
Cases (every row carries its case; none is a central value or a headline):
  `common:legacy`            the legacy arm on one constant market path (the register mean market return), no spread;
  `common:household:<point>` the household arm at a held grid point (median_mid, max_mid, median_low) on the same constant path (its class returns are fixed scenario rates; the path reaches only the fund's safe stand-in);
  `stoch:legacy`             the legacy arm on its own stochastic paths (1,000, chunks of 100, seed 1, as 124c): each term is the mean over the paths.
Terms (percent unless named; the windows are the model's: short = the 10 years after the reserve fills, long = years 51 to 100):
  M1a   = 100 x Base x Rate, window sums: Base = sum of the aggregate taxed wealth (billions) over the window / sum of GDP, Rate = sum of WDT cash / sum of taxed wealth (exact, no interaction);
  M2    = R_pay x K: R_pay = 100 x sum(w net) / sum(w w0) over the payers (net > 0 and w0 > 0), K = M2 / R_pay the tax-weighting of the rate (K = 1 if every payer pays one rate); `w0` is the kernel's start-of-year family value (the
          denominator M2 divides by); M2d the same with the settlement at death. For the household arm `R_pay_total` divides the same tax by the line's total wealth, pension included (what `w0` leaves out from year 2);
  M1c   = (return on the fund - the fund's growth) as % of GDP: window sums of S(-1) x rr and of the change in S, over GDP; M1 net and M1d as the model's windows;
  P6    = S / GDP at years 10, 25, 50, 100, with the cumulative inflow (WDT cash + levy), return and payout, each as % of that year's GDP (S = inflow + return - payout).
Run from the repository root:  python -I model/studies/household-vs-legacy/decomp.py [--paths N] [--out DIR]
"""
import argparse
import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT / 'model'), str(HERE), str(ROOT / 'model' / 'studies' / 'household-arm-account'), str(ROOT / 'model' / 'studies' / 'household-arm-run')]

import account_table as A                                                      # noqa: E402
import flows as F                                                              # noqa: E402
import run_grid as G                                                           # noqa: E402
from model_v3.core import burden as bd, returns as rt                          # noqa: E402
from model_v3.runner import arm as ab, runner as R                             # noqa: E402

COLS = ('case', 'output', 'horizon', 'band', 'term', 'value')
HOR = ('short', 'long')
BANDS = ('overall', 'D4_5', 'D6_7', 'D8_9', 'D10')
YEARS = (10, 25, 50, 100)
POINTS = ('median_mid', 'max_mid', 'median_low')


def total_wealth(rec, T=R.T):
    """(T, 6 * 14, 1) start-of-year total wealth (pension included) of the household hook's records, phase-major as `line_flows` orders its lines."""
    s = np.asarray(rec['start'], float)
    return s.reshape(F.PH, T, F.L).transpose(1, 0, 2).reshape(T, F.PH * F.L)[:, :, None]


def terms(raw, wtot=None):
    """{(output, horizon, band, term): per-path array} of one core run (paths P)."""
    r, fl, out = raw.r, raw.fl, {}
    T, P = r['M1a'].shape
    gdp, wt, w0 = r['gdp'], fl['wt'][None, :, None], fl['w0']
    for h in HOR:
        lo, hi = raw.lo[h], raw.hi[h]
        gate = (lambda v: np.where(raw.ok, v, np.nan)) if h == 'short' else (lambda v: v)
        m = (np.arange(1, T + 1)[:, None] >= lo[None, :]) & (np.arange(1, T + 1)[:, None] <= hi[None, :]) & (hi[None, :] <= T)
        base = fl['adults_k'] * (wt * w0).sum(1)                                    # (T, P) the aggregate taxed wealth, billions (the kernel's family value)
        if wtot is not None:
            base_all = fl['adults_k'] * (wt * wtot).sum(1)
        den = (gdp * m).sum(0)
        wdt = r['wdt_bn']
        out[('M1a', h, 'all', 'value')] = gate(100 * (wdt * m).sum(0) / den)
        out[('M1a', h, 'all', 'base_pct_gdp')] = gate(100 * (base * m).sum(0) / den)
        out[('M1a', h, 'all', 'rate_pct')] = gate(100 * (wdt * m).sum(0) / (base * m).sum(0))
        if wtot is not None:
            out[('M1a', h, 'all', 'base_total_pct_gdp')] = gate(100 * (base_all * m).sum(0) / den)
        ret, S = r['fund']['rr'] * np.vstack([np.zeros((1, P)), r['fund']['S'][:-1]]), r['fund']['S']
        Sp = np.vstack([np.zeros((1, P)), S[:-1]])
        out[('M1c', h, 'all', 'value')] = gate(100 * ((Sp * r['fund']['rr'] - (S - Sp)) * m).sum(0) / den)
        out[('M1c', h, 'all', 'return_on_fund_pct_gdp')] = gate(100 * ((Sp * r['fund']['rr']) * m).sum(0) / den)
        out[('M1c', h, 'all', 'fund_growth_pct_gdp')] = gate(100 * (((S - Sp)) * m).sum(0) / den)
        out[('M1c', h, 'all', 'fund_level_pct_gdp')] = gate(100 * (Sp * m).sum(0) / den)
        out[('M1c', h, 'all', 'return_rate_pct')] = gate(100 * (r['fund']['rr'] * m).sum(0) / m.sum(0))
        for k in ('M1', 'M1b', 'M1d'):
            out[(k, h, 'all', 'value')] = gate((r[k] * gdp * m).sum(0) / den)
        for inlife, oid in ((True, 'M2'), (False, 'M2d')):
            net = fl['net'] - fl['death'] if inlife else fl['net']
            mk = m[:, None, :] & (net > 0) & (w0 > 0) if False else bd._window(T, lo, hi, P)[:, None, :] & (net > 0) & (w0 > 0)
            for b, gm in bd._groups(fl['band']).items():
                if b not in BANDS:
                    continue
                k = mk[:, gm]
                tax = (wt[:, gm] * np.where(k, net[:, gm], 0.0)).sum((0, 1))
                w2 = (wt[:, gm] * np.where(k, net[:, gm] ** 2 / np.where(w0[:, gm] > 0, w0[:, gm], 1.0), 0.0)).sum((0, 1))
                wea = (wt[:, gm] * np.where(k, w0[:, gm], 0.0)).sum((0, 1))
                m2, rp = 100 * w2 / np.where(tax > 0, tax, np.nan), 100 * tax / np.where(wea > 0, wea, np.nan)
                out[(oid, h, b, 'value')], out[(oid, h, b, 'R_pay_pct')], out[(oid, h, b, 'K')] = gate(m2), gate(rp), gate(m2 / rp)
                out[(oid, h, b, 'payer_wealth_share_of_group')] = gate(wea / (wt[:, gm] * np.where(bd._window(T, lo, hi, P)[:, None, :], w0[:, gm], 0.0)).sum((0, 1)))
                if wtot is not None:
                    wt_all = (wt[:, gm] * np.where(k, wtot[:, gm], 0.0)).sum((0, 1))
                    out[(oid, h, b, 'R_pay_total_pct')] = gate(100 * tax / np.where(wt_all > 0, wt_all, np.nan))
    inflow = r['wdt_bn'] + r['M1b'] * gdp / 100
    S = r['fund']['S']
    Sp = np.vstack([np.zeros((1, P)), S[:-1]])
    ret, pay = Sp * r['fund']['rr'], r['fund']['R']
    for y in YEARS:
        i = y - 1
        out[('P6', f'year {y}', 'all', 'value')] = 100 * S[i] / gdp[i]
        for k, v in (('cum_inflow_pct_gdp', inflow), ('cum_return_pct_gdp', ret), ('cum_payout_pct_gdp', pay)):
            out[('P6', f'year {y}', 'all', k)] = 100 * v[:y].sum(0) / gdp[i]
    return out


def mean_terms(parts):
    """Mean over the paths of each term (nan-aware), parts a list of `terms` dicts (chunks)."""
    return {k: float(np.nanmean(np.concatenate([np.asarray(p[k], float).ravel() for p in parts]))) if np.isfinite(np.concatenate([np.asarray(p[k], float).ravel() for p in parts])).any() else float('nan') for k in parts[0]}


def reported(grid):
    """The 124c values (grid_results.csv, schedule S) of one grid point or `legacy`, keyed as the terms' (output, horizon, band, 'value') where a 124c row exists."""
    path = ROOT / 'docs' / 'model-v3' / 'household-arm-run' / 'grid_results.csv'
    ids = {'O1': 'line', 'O2': 'by', 'O2d': 'by', 'OP6': 'by'}
    res = {}
    for r in csv.DictReader(open(path)):
        if r['grid'] != grid or r['schedule'] != 'S' or r['id'] not in ids:
            continue
        a = float(r['a'])
        if r['id'] == 'O1' and r['line'] in ('M1', 'M1a', 'M1b', 'M1c', 'M1d') and r['horizon'] in HOR:
            res[(r['line'], r['horizon'], 'all', 'value')] = a
        elif r['id'] in ('O2', 'O2d') and r['horizon'] in HOR and r['by'].startswith('wealth_band='):
            res[({'O2': 'M2', 'O2d': 'M2d'}[r['id']], r['horizon'], r['by'].split('=')[1], 'value')] = a
        elif r['id'] == 'OP6':
            res[('P6', 'year ' + r['by'].split('=')[1], 'all', 'value')] = a
    return res


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--paths', type=int, default=G.PATHS)
    p.add_argument('--out', default=str(HERE))
    a = p.parse_args(argv)
    ctx, inp = A.setup()
    mu = ctx.centre[R.RET['mean']] / 100.0
    g, gg = np.full((R.T, 1), mu), np.full((R.T, 1), ctx.gdp_g)
    cases = {}
    rec, raw = F.run_arm(ctx, ctx.centre, g, gg, False)
    cases['common:legacy'] = {k: float(v[0]) for k, v in terms(raw).items()}
    for name in POINTS:
        rec, raw = F.run_arm(G.point_ctx(ctx, inp, name), ctx.centre, g, gg, True)
        cases[f'common:household:{name}'] = {k: float(v[0]) for k, v in terms(raw, total_wealth(rec)).items()}
    rng, parts = rt.streams(G.SEED)['level1_paths'], []
    for s in range(0, a.paths, G.CHUNK):
        gs = rt.ar1_paths(rng, ctx.centre[R.RET['mean']], ctx.centre[R.RET['sd']], ctx.centre[R.RET['phi']], R.T, min(G.CHUNK, a.paths - s))
        parts.append(terms(R.core_run(ctx, ctx.centre, A.SPEC, gs, np.full(gs.shape, ctx.gdp_g))))
    cases['stoch:legacy'] = mean_terms(parts)
    rows, worst = [], {}
    for case, tm in cases.items():
        rep = reported({'stoch:legacy': 'legacy'}.get(case, case.split(':')[-1])) if not case.startswith('common:legacy') else {}
        for (o, h, b, t), v in tm.items():
            rows.append(dict(case=case, output=o, horizon=h, band=b, term=t, value=v))
            if t == 'value' and (o, h, b, t) in rep:
                rows.append(dict(case=case, output=o, horizon=h, band=b, term='reported_124c', value=rep[(o, h, b, t)]))
                worst[case] = max(worst.get(case, 0.0), abs(v - rep[(o, h, b, t)]) / max(abs(rep[(o, h, b, t)]), 1e-9) if np.isfinite(v) else 0.0)
    for case in [c for c in cases if c.startswith('common:household')]:                                          # the ratio household / legacy as base x rate (exact), on the common ground and against the legacy arm's own paths
        for ref in ('common:legacy', 'stoch:legacy'):
            for (o, h, bd_, t), v in cases[case].items():
                pair = {'M1a': ('base_pct_gdp', 'rate_pct'), 'M2': ('R_pay_pct', 'K'), 'M2d': ('R_pay_pct', 'K')}.get(o)
                if t != 'value' or pair is None:
                    continue
                num = [cases[case][(o, h, bd_, x)] for x in ('value',) + pair]
                den = [cases[ref][(o, h, bd_, x)] for x in ('value',) + pair]
                for nm, x, y in zip(('ratio_value', 'ratio_' + pair[0], 'ratio_' + pair[1]), num, den):
                    rows.append(dict(case=f'{case} / {ref}', output=o, horizon=h, band=bd_, term=nm, value=x / y if y else float('nan')))
                q = [x / y if y else float('nan') for x, y in zip(num, den)]
                rows.append(dict(case=f'{case} / {ref}', output=o, horizon=h, band=bd_, term='ratio_interaction', value=q[0] / (q[1] * q[2]) if q[1] * q[2] else float('nan')))   # 1 on the common ground; on the legacy arm's own paths it is the error of using means of terms
    with open(Path(a.out) / 'decomp.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, COLS)
        w.writeheader()
        w.writerows(rows)
    print(f'decomp.csv: {len(rows)} rows, {len(cases)} cases; worst relative gap to the 124c value by case: ' + ', '.join(f'{k} {v:.2e}' for k, v in worst.items()))


if __name__ == '__main__':
    main()
