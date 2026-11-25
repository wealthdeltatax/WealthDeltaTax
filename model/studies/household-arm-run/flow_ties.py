"""
flow_ties.py -- brief 148c, block 3: the public ledger's tie on EVERY household-arm `core_run` of a level 1 evaluation, with the flow switches on.
`run_grid.py` checks the tie on the first chunk's main run only; a run with a lien in another spec (or with the per-path GDP array of `gdp_paths`) is not covered there. This wraps `runner.core_run`
(the call `evaluate` and its reruns make, with the array they actually use), and per call computes the tie of 120c: receipts by route against the WDT cash (tax, refunds, death taxes, heir, death B and D;
a lien is no receipt of its year, its settlement is). Per point it writes one row: the number of calls, how many carry a lien, the worst tie, the receivable's write-offs and largest balance (billions, weighted).
No number is tuned. Run from the repository root:
python -I model/studies/household-arm-run/flow_ties.py [--paths N] [--out DIR] [--points a,b] [--market-paths] [--pension-withdrawal S] [--heir-floor N] [--gdp-paths S]
Writes ties<suffix>.csv (the suffix as run_grid's: _paths, _wd_<s>, _floor<N>, _gdp_<s>).
"""
import argparse
import csv
import sys
from pathlib import Path

import numpy as np
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = ROOT / 'results' / 'household-arm-run'   # outputs and stored tables stay here until 163c
sys.path[:0] = [str(HERE)]

import run_grid as G                                                           # noqa: E402  (the same builder, points and chunking)
from model_v3.core import returns as rt                                        # noqa: E402
from model_v3.runner import runner as R                                        # noqa: E402

COLS = ('point', 'paths', 'core_runs', 'runs_with_lien', 'tie_max', 'wo_sum', 'lien_bal_max', 'new_sum', 'settled_sum', 'error')


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--paths', type=int, default=20)
    p.add_argument('--out', default=str(DATA))
    p.add_argument('--points', default='min_mid,median_high')
    p.add_argument('--market-paths', action='store_true')
    p.add_argument('--pension-withdrawal', choices=('low', 'mid', 'high'))
    p.add_argument('--heir-floor', type=int, choices=(0, 25, 50))
    p.add_argument('--gdp-paths', choices=('indep', 'hist'))
    a = p.parse_args(argv)
    flow = {k: v for k, v in (('pension_withdrawal', a.pension_withdrawal), ('heir_floor', a.heir_floor), ('gdp_paths', a.gdp_paths)) if v is not None}
    sfx = ('_paths' if a.market_paths else '') + (f'_wd_{a.pension_withdrawal}' if a.pension_withdrawal else '') + (f'_floor{a.heir_floor}' if a.heir_floor is not None else '') + (f'_gdp_{a.gdp_paths}' if a.gdp_paths else '')
    ctx, inp = G.A.setup()
    manifest = yaml.safe_load((G.ROOT / 'model-specs' / 'outputs.yml').read_text())
    orig, out = R.core_run, []
    for name in [x for x in a.points.split(',') if x]:
        st = dict(n=0, lien=0, tie=0.0, wo=0.0, bal=0.0, new=0.0, settled=0.0)

        def spy(*args, _st=st, **kw):
            raw = orig(*args, **kw)
            led = raw.run.get('ledger')
            if led is not None:                                                  # the legacy arm's runs keep no ledger
                run, rec = raw.run, led['rec']
                wdt = sum(run[k] for k in ('tax', 'refund', 'death_tax', 'heir', 'death_B', 'death_D')) - (rec['new'] - rec['xnew']) + rec['settled']
                _st['n'] += 1
                _st['lien'] += int(bool(np.any(rec['bal']) or np.any(rec['new']) or np.any(rec['settled']) or np.any(rec['wo'])))
                _st['tie'] = max(_st['tie'], float(np.abs(sum(led['rc'].values()) - wdt).max()))
                _st['wo'] += float(np.sum(rec['wo']))
                _st['bal'] = max(_st['bal'], float(np.max(rec['bal'])))
                _st['new'] += float(np.sum(rec['new']))
                _st['settled'] += float(np.sum(rec['settled']))
            return raw

        R.core_run, err = spy, ''
        try:
            G.R.level1(G.point_ctx(ctx, inp, name, a.market_paths, 'safe', flow), {'S': G.A.SPEC}, rt.streams(G.SEED)['level1_paths'], n=a.paths, chunk=min(G.CHUNK, a.paths))
        except ValueError as exc:                                                # a failed run is reported with its point and error; no rule is changed
            err = str(exc)[:200]
        finally:
            R.core_run = orig
        out.append(dict(point=name, paths=a.paths, core_runs=st['n'], runs_with_lien=st['lien'], tie_max=st['tie'], wo_sum=st['wo'], lien_bal_max=st['bal'], new_sum=st['new'], settled_sum=st['settled'], error=err))
        print(f"{name}: {st['n']} core runs, {st['lien']} with a lien, worst tie {st['tie']:.2e}, write-offs {st['wo']:.4g}, largest balance {st['bal']:.4g}" + (f', FAILED: {err[:90]}' if err else ''), flush=True)
    with open(Path(a.out) / f'ties{sfx}.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, COLS)
        w.writeheader()
        w.writerows(out)


if __name__ == '__main__':
    main()
