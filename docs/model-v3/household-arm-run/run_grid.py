"""
run_grid.py -- brief 124c: the first household-arm run, one level 1 evaluation per scenario grid point.
Five labelled grid points, none called central: saving min, median and max at the `mid` regime, and the `low` and `high` regimes at median saving. Everything else as the account's centre
(schedule tau_0 0.04, tau_m 0.7, k_ln 1, ratio 0.5; register central inputs; B.6g income scale; tail pension cap I-D1l; the safe asset earns the net financial class return, a stand-in).
The class returns are fixed scenario rates unless --market-paths (128c: net financial and pension deviate with the path's market return, scenario-labelled); only GDP growth and the fund's returns see the path. The legacy arm (c = I-D14c) runs on the
same paths as labelled context. Each point goes through `runner.level1` (the core, the output groups, `samples`) and writes one row per cell: mean, P10 and P90 over the paths for the
p10_mean_p90 ids, the stored values for the others. Checks per point: I1 (raises inside the hook), the account identity and unpaid_B (every year of every phase), the shortfall lines, and the
ledger ties of 120c on the first chunk. No number is tuned. Run from the repository root:   python -I docs/model-v3/household-arm-run/run_grid.py [--paths N] [--out DIR] [--points a,b]
Writes grid_results.csv and checks.csv; prints only summary lines.
"""
import argparse
import csv
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / 'docs' / 'model-v3' / 'household-arm-account')]

import account_table as A                                                      # noqa: E402  (setup and SPEC: the same builder and grid point)
from model_v3.core import kernel as K, returns as rt                           # noqa: E402
from model_v3.runner import arm as ab, runner as R                             # noqa: E402

POINTS = {'min_mid': ('min', 'mid'), 'median_mid': ('median', 'mid'), 'max_mid': ('max', 'mid'), 'median_low': ('median', 'low'), 'median_high': ('median', 'high')}
SEED, PATHS, CHUNK = 1, 1000, 100
CHECKS = ('point', 'account_residual_max', 'unpaid_max', 'unpaid_B_max', 'unpaid_B_path_phases', 'shortfall_lines', 'spread_cells', 'flat_cells', 'ledger_tie_max', 'ledger_tie_first', 'ledger_dL_max', 'i1', 'error')
COLS = ('grid', 'label', 'id', 'schedule', 'horizon', 'by', 'line', 'unit', 'summary', 'a', 'b', 'c', 'n_nan')


def label(arm_ctx):
    a = arm_ctx.arm
    return 'legacy (context, c = I-D14c)' if a == 'legacy' else f"household, saving {a['saving']}, regime {a['regime']} (a scenario, not central)" + (', market-return risk only (128c)' if a.get('paths') else '')


def point_ctx(ctx, inp, name, paths=False):
    sav, regime = POINTS[name]
    return replace(ctx, arm=dict(arm='household', inputs=inp, saving=sav, regime=regime, paths=paths))


def rows(name, ctx, samples, manifest):
    """One row per cell of every produced id: mean, P10, P90 over the paths (p10_mean_p90), else the stored values."""
    ent = {e['id']: e for k in ('outputs', 'checks') for e in manifest.get(k) or []}
    for oid in sorted(samples):
        for key, v in sorted(samples[oid].items(), key=lambda kv: repr(kv[0])):
            s, h, by, ln = key
            x, e = np.asarray(v, float), ent[oid]
            if e['summary'] == 'p10_mean_p90' and np.isfinite(x).any():
                a, b, c = np.nanmean(x), *np.nanpercentile(x, [10, 90])
            elif e['summary'] == 'p10_mean_p90':
                a = b = c = np.nan
            else:
                a, b, c = (list(x.ravel()) + [np.nan] * 3)[:3]
            yield dict(grid=name, label=label(ctx), id=oid, schedule=s, horizon=h, by=';'.join(f'{k}={w}' for k, w in by), line=ln, unit=e.get('unit', ''), summary=e['summary'],
                       a=a, b=b, c=c, n_nan=int((~np.isfinite(x)).sum()))


def spread(rows):
    """(cells with spread, flat cells) among the p10_mean_p90 cells: spread is P90 above P10."""
    c = [r for r in rows if r['summary'] == 'p10_mean_p90' and np.isfinite(r['a'])]
    s = sum(1 for r in c if r['c'] - r['b'] > 1e-12)
    return s, len(c) - s


def run_point(ctx, inp, name, manifest, n=PATHS, chunk=CHUNK, seed=SEED):
    """(rows, checks) of one grid point; the legacy arm (name 'legacy') has no checks."""
    hh = ctx.arm != 'legacy'
    seen, books, orig, hook = [], [], K.Book, ab.HouseholdHook

    class Spy(hook):
        def post(self, book, fl):
            super().post(book, fl)
            a = self.account()
            seen.append((np.abs(a['residual']).max(), np.abs(a['unpaid']).max()))

        def _check(self, book):
            try:
                super()._check(book)
            except ValueError as exc:                                                 # report the failing path, line, year and balances (128c); no rule is changed
                N, L = self._n(self.q), len(self.st['income'])
                j = int(np.argmax(np.abs(book.family_true() - N)))
                raise ValueError(f"{exc} First: path {j // L} (of the chunk), line {j % L}, year {len(self.gh)}, family value {book.family_true()[j]:.6g}, class total {N[j]:.6g}, balances "
                                 + ', '.join(f'{k} {self.q[k][j]:.6g}' for k in ab.CLASSES)) from None

    if hh:
        ab.HouseholdHook, K.Book = Spy, (lambda *a, **k: books.append(orig(*a, **k)) or books[-1])
    try:
        try:
            samples, _ = R.level1(ctx, {'S': A.SPEC}, rt.streams(seed)['level1_paths'], n=n, chunk=chunk)
        except ValueError as exc:                                                    # a failed run is reported with its point and error; no rule is changed (124c)
            return [], dict(point=name, i1='FAILED', error=str(exc))
        chk = None
        if hh:
            g = rt.ar1_paths(rt.streams(seed)['level1_paths'], ctx.centre[R.RET['mean']], ctx.centre[R.RET['sd']], ctx.centre[R.RET['phi']], R.T, min(chunk, n))
            raw = R.core_run(ctx, ctx.centre, A.SPEC, g, np.full(g.shape, ctx.gdp_g))
            wdt = sum(raw.run[k] for k in ('tax', 'refund', 'death_tax', 'heir', 'death_B', 'death_D'))
            f, dl = raw.r['fund'], 0.0
            for k in f['L']:
                d = np.diff(np.vstack([np.zeros((1, g.shape[1])), f['L'][k]]), axis=0)
                dl = max(dl, float(np.abs(d - (f['rc'][k] + f['ret'][k] - f['pay'][k])).max()))
            pp = [np.abs(b.unpaid_B).reshape(-1, 14).max(1) for b in books if b.n % 14 == 0]            # per path (and phase): the worst unpaid_B over its lines
            tie = np.abs(sum(raw.run['ledger']['rc'].values()) - wdt)
            first = '' if tie.max() < 1e-9 else (lambda i: f"first chunk: year {i[0] + 1}, path {i[1]}, gap {tie[tuple(i)]:.4g}, tax {raw.run['tax'][tuple(i)]:.4g}, refund {raw.run['refund'][tuple(i)]:.4g}, receipts " + ', '.join(f"{k} {v[tuple(i)]:.4g}" for k, v in raw.run['ledger']['rc'].items()))(np.argwhere(tie > 1e-9)[0])
            chk = dict(point=name, account_residual_max=max(r for r, _ in seen), unpaid_max=max(u for _, u in seen), unpaid_B_max=max(float(x.max()) for x in pp), unpaid_B_path_phases=int(sum((x > 0).sum() for x in pp)),
                       spread_cells=None, flat_cells=None, shortfall_lines=int(sum(K.shortfall_lines(b) for b in books)), ledger_tie_max=float(np.abs(sum(raw.run['ledger']['rc'].values()) - wdt).max()), ledger_dL_max=dl, i1='held (raises in the hook otherwise)', error='', ledger_tie_first=first)
    finally:
        ab.HouseholdHook, K.Book = hook, orig
    out = list(rows(name, ctx, samples, manifest))
    if chk:
        chk['spread_cells'], chk['flat_cells'] = spread(out)
    return out, chk


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--paths', type=int, default=PATHS)
    p.add_argument('--out', default=str(HERE))
    p.add_argument('--points', default=','.join(POINTS))
    p.add_argument('--no-legacy', action='store_true')
    p.add_argument('--market-paths', action='store_true', help='per-path market returns (128c): files get the suffix _paths')
    a = p.parse_args(argv)
    if not 1 <= a.paths <= 2000:
        sys.exit('paths must be 1 to 2000 (brief 124c)')
    ctx, inp = A.setup()
    manifest = yaml.safe_load((ROOT / 'docs' / 'model-v3' / 'outputs.yml').read_text())
    out, allrows, checks = Path(a.out), [], []
    for name in [x for x in a.points.split(',') if x] + ([] if a.no_legacy else ['legacy']):
        c = ctx if name == 'legacy' else point_ctx(ctx, inp, name, a.market_paths)
        r, chk = run_point(c, inp, name, manifest, a.paths, min(CHUNK, a.paths))
        allrows += r
        checks += [chk] if chk else []
        print(f"{name}: {len(r)} cells" + (f", FAILED: {chk['error'][:90]}" if chk and chk.get('error') else '') + (f", ledger tie gap: {chk['ledger_tie_first'][:70]}" if chk and chk.get('ledger_tie_first') else '') + (f", account residual {chk['account_residual_max']:.1e}, unpaid {chk['unpaid_max']:.1e}, unpaid_B {chk['unpaid_B_max']:.1e}, shortfall lines {chk['shortfall_lines']}, ledger tie {chk['ledger_tie_max']:.1e}" if chk and not chk.get('error') else ''), flush=True)
    sfx = '_paths' if a.market_paths else ''
    for f, cols, data in ((f'grid_results{sfx}.csv', COLS, allrows), (f'checks{sfx}.csv', CHECKS, checks)):
        with open(out / f, 'w', newline='') as fh:
            w = csv.DictWriter(fh, cols)
            w.writeheader()
            w.writerows(data)


if __name__ == '__main__':
    main()
