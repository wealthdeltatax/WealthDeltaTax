"""
flows.py -- brief 136c, block 1: the flow comparison of the household arm and the legacy arm, every line, on common ground. Diagnosis only: no model file is changed; both arms are run through the repository's own `core_run`.

Common ground: one constant market path, the register's mean market return (I-D1 mean, percent) for the legacy arm's `g`, no spread (one path), the same GDP growth; the three held grid points (`median_mid`, `max_mid`, `median_low`; their
class returns and saving differ, the legacy arm does not depend on the point, so its rows are written once with point `all`). The household arm reads fixed scenario class returns, not `g` (its market-return deviation is 128c, off here).
Per line (14), per year (1, 10, 30, 100), per arm; units millions of pounds per adult, real; the line values are the mean over the six death phases (equal weights, as the model weights them).
weight: the line's share of adults (the weights of the model); W_start / W_end: the line's total wealth (pension included) at the start of the year and after the year's in-life tax (before a death settlement); growth = W_end / W_start - 1; c_eq = 1 - (W_end / W_start) / (1 + g) the implied
consumption-equivalent after tax, c_eq_pre_tax with the in-life tax added back (the legacy arm's own c, 3.5%, by construction); the household account terms are shares of W_start: S saving, CG holding gain, T in-life tax, death the
settlement a death triggers, resid the account residual. Every table is scenario-labelled; no figure is a central value or a headline.   Run from the repository root:  python -I docs/model-v3/household-vs-legacy/flows.py [--out DIR]
"""
import argparse
import csv
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / 'docs' / 'model-v3' / 'household-arm-account'), str(ROOT / 'docs' / 'model-v3' / 'household-arm-run')]

import account_table as A                                                      # noqa: E402
import run_grid as G                                                           # noqa: E402
from model_v3.runner import arm as ab, runner as R                             # noqa: E402

L, PH, YEARS = 14, 6, (1, 10, 30, 100)
LABELS = ('D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10a', 'D10b', 'RL3', 'RL2', 'RL1')
COLS = ('point', 'arm', 'line', 'year', 'weight', 'W_start', 'W_end', 'growth', 'c_eq', 'c_eq_pre_tax', 'S_share', 'CG_share', 'T_share', 'death_share', 'resid_share', 'label')
POINTS = ('median_mid', 'max_mid', 'median_low')


def phases(x, n=PH):
    """(n * T, L) records of one hook (phase-major) to (T, L): the mean over the phases."""
    x = np.asarray(x, float)
    return x.reshape(n, -1, L).mean(0)


def tap(cls, total):
    """A subclass of the arm's hook that records each year's start and end total wealth by line, and the household account; `total(hook, book)` gives the (n,) total wealth. Records of the first instance only (line_flows)."""
    rec = {}

    class Tap(cls):
        def pre(self, book, t, g):
            out = super().pre(book, t, g)
            rec.setdefault(id(self), dict(start=[], end=[], acc=[]))['start'].append(total(self, book).copy())
            return out

        def post(self, book, fl):
            super().post(book, fl)
            r = rec[id(self)]
            r['end'].append(total(self, book).copy())
            if hasattr(self, 'account'):
                a = self.account()
                r['acc'].append({k: np.asarray(a[k], float).copy() for k in ('S', 'CG', 'T_WDT', 'residual')})
    return Tap, rec


def run_arm(ctx, theta, g, gg, household):
    """(records, raw) of one arm: the first hook's per-year records (the `line_flows` hook) and the `Raw` core result."""
    cls = ab.HouseholdHook if household else ab.LegacyHook
    Tap, rec = tap(cls, (lambda h, b: sum(h.q[k] for k in ab.CLASSES) - h.PL) if household else (lambda h, b: b.family_true()))
    orig = getattr(ab, cls.__name__)
    setattr(ab, cls.__name__, Tap)
    try:
        raw = R.core_run(ctx, theta, A.SPEC, g, gg)
    finally:
        setattr(ab, cls.__name__, orig)
    return next(iter(rec.values())), raw


def table(point, arm, rec, fl, g, label):
    """Rows (one per line and year in YEARS) of one arm."""
    T = R.T
    ws, we = phases(rec['start']), phases(rec['end'])
    net, dth = (np.asarray(fl[k], float)[:, :L * PH, 0] for k in ('net', 'death'))
    net, dth = (x.reshape(T, PH, L).mean(1) for x in (net, dth))
    tax, wl = net - dth, np.asarray(fl['wt'], float)[:L] * PH                      # wl: the line's weight (the share of adults it stands for)
    acc = {k: phases([a[k] for a in rec['acc']]) for k in ('S', 'CG', 'residual')} if rec['acc'] else {}
    for t in YEARS:
        for i, name in enumerate(LABELS):
            w0, w1, tx = ws[t - 1, i], we[t - 1, i], tax[t - 1, i]
            gr = w1 / w0 - 1.0
            r = dict(point=point, arm=arm, line=name, year=t, weight=wl[i], W_start=w0, W_end=w1, growth=gr, c_eq=1 - (w1 / w0) / (1 + g), c_eq_pre_tax=1 - ((w1 + tx) / w0) / (1 + g), T_share=tx / w0, death_share=dth[t - 1, i] / w0, label=label)
            for k, o in (('S', 'S_share'), ('CG', 'CG_share'), ('residual', 'resid_share')):
                r[o] = acc[k][t - 1, i] / w0 if acc else np.nan
            yield r


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--out', default=str(HERE))
    out = Path(p.parse_args(argv).out)
    ctx, inp = A.setup()
    mu = ctx.centre[R.RET['mean']] / 100.0
    g, gg = np.full((R.T, 1), mu), np.full((R.T, 1), ctx.gdp_g)
    rows = []
    rec, raw = run_arm(ctx, ctx.centre, g, gg, False)
    rows += list(table('all', 'legacy', rec, raw.fl, mu, f'legacy (context, c = I-D14c), constant market return {mu:.4f}'))
    for name in POINTS:
        c = G.point_ctx(ctx, inp, name)
        rec, raw = run_arm(c, ctx.centre, g, gg, True)
        rows += list(table(name, 'household', rec, raw.fl, mu, G.label(c)))
    with open(out / 'flows.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, COLS)
        w.writeheader()
        w.writerows(rows)
    print(f'flows.csv: {len(rows)} rows, g = {mu:.4f}, gdp growth {ctx.gdp_g:.4f}')


if __name__ == '__main__':
    main()
