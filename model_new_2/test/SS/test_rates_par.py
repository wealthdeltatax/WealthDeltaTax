"""
test_rates_par.py -- the parallel sweep must give the serial numbers, exactly
===========================================================================
Run from anywhere:   python test/test_rates_par.py [--workers 4] [--stride 40]

Checks (all exact, no tolerance: the patch moves no number):
  1. HOIST     run_window with the per-sweep constants (pre=...) equals run_window without them (the old per-window path).
  2. PARITY    sweep(...) serial equals sweep(..., pool=WorkerPool(N)): same rows, same order, bit-identical, on scenarios
               that exercise the stationary-c rebuild, the Route B lien plan and the CORP levy.
  3. ERRORS    an exception in a worker reaches the parent; a pool started with other inputs is refused; the pool survives.
  4. END2END   rates_core.main() with --workers 1 and --workers N writes the same JSON (meta.generated / meta.elapsed_s aside).
               The JSON goes to a temp file; OUTPUTS/RATES/rates_data.json is not touched.

Uses the real WDT_Params.toml and JST file, a few countries and a coarse stride, so it takes a minute or two.
The `if __name__ == '__main__'` guard is required: worker processes re-import this module (Windows 'spawn').
"""

import argparse
import sys
import tempfile
import time
from pathlib import Path

import pandas as pd

MODEL = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(MODEL), str(MODEL / 'RATES')]

import wdt_core as wc                                   # noqa: E402
import wdt_par as wpar                                  # noqa: E402
import rates_core as rc                                 # noqa: E402
from wdt_jst import load_jst                            # noqa: E402

SCENARIOS = ['gain_ladder', 'gl_stationary', 'gl_arch_wealth_lien']
COUNTRIES = ['GBR', 'USA', 'JPN']


def scenario_cfg(p, J, name, stride, isos):
    ov = dict(p['rates']['scenarios'][name]['overrides'])
    ov.update(start_stride=stride, countries=isos)
    cfg = rc.make_cfg(p, **ov)
    if cfg['levy'] and cfg['levy_calibrate']:
        cfg['levy'], _ = rc.calibrate_levy(J, cfg, p)
    return cfg


def same_frame(a, b, what):
    pd.testing.assert_frame_equal(a, b, check_exact=True, obj=what)


def test_hoist(p, J, stride):
    for name in SCENARIOS:
        cfg = scenario_cfg(p, J, name, stride, COUNTRIES)
        cal = rc.calibration(J, cfg, p)
        pre = rc._sweep_ctx(cfg, cal, p)
        n = 0
        for iso in COUNTRIES:
            d = rc.panel(J, iso)
            fl = rc.flag_years(d, p['rates']['flags'])['any']
            wins = rc.loop_windows(rc.usable_years(d, rc.MODEL_COLS + ['eq_capgain', 'gdpg']), cfg['T'], wrap=True)
            for w in wins[::max(1, len(wins) // 2)][:2]:
                for mode in cfg['index_modes']:
                    old = rc.run_window(J, iso, w, mode, cfg, cal, p, flags=fl)
                    new = rc.run_window(J, iso, w, mode, cfg, cal, p, pre=pre)
                    same_frame(pd.DataFrame([old]), pd.DataFrame([new]), f'{name} {iso} {w["start"]}')
                    n += 1
        print(f'  1 HOIST   {name:22s} {n} windows identical')


def test_parity(p, J, stride, workers):
    with wpar.WorkerPool(workers, initializer=rc._w_init, initargs=(J, p), tag=rc._pool_tag(J, p)) as pool:
        assert pool.parallel, 'need --workers >= 2 to test the pool'
        for name in SCENARIOS:
            cfg = scenario_cfg(p, J, name, stride, COUNTRIES)
            t0 = time.time()
            ser, cal = rc.sweep(J, cfg, p)
            t1 = time.time()
            par, _ = rc.sweep(J, cfg, p, cal=cal, pool=pool)
            t2 = time.time()
            same_frame(ser, par, name)
            print(f'  2 PARITY  {name:22s} {len(ser):4d} rows identical   serial {t1 - t0:6.1f}s   {workers} workers {t2 - t1:6.1f}s')


def test_errors(p, J, workers):
    cfg = scenario_cfg(p, J, 'gain_ladder', 60, COUNTRIES)
    with wpar.WorkerPool(workers, initializer=rc._w_init, initargs=(J, p), tag=rc._pool_tag(J, p)) as pool:
        try:
            rc.sweep(J, {**cfg, 'index_modes': ('bogus',)}, p, pool=pool)
            raise AssertionError('a worker error must reach the parent')
        except ValueError as e:
            assert 'index_mode' in str(e), e
        other = {**p, 'rules': {**p['rules'], 'base': 'units_and_value/reset/on'}}
        try:
            rc.sweep(J, cfg, other, pool=pool)
            raise AssertionError('a pool started with other params must be refused')
        except ValueError as e:
            assert 'different J / p' in str(e), e
        df, _ = rc.sweep(J, cfg, p, pool=pool)
        assert len(df) > 0
    print('  3 ERRORS  worker error reaches the parent; mismatched pool refused; pool reusable')


def _strip(data):
    data = dict(data)
    data['meta'] = {k: v for k, v in data['meta'].items() if k not in ('generated', 'elapsed_s')}
    return data


def test_end_to_end(stride, workers):
    keep = rc.json_path
    try:
        with tempfile.TemporaryDirectory() as tmp:
            outs = {}
            for w in (1, workers):
                path = Path(tmp) / f'rates_{w}.json'
                rc.json_path = lambda path=path: path
                rc.main(['--scenario', 'gain_ladder', '--stride', str(stride), '--countries', *COUNTRIES,
                         '--fresh', '--workers', str(w)])
                outs[w] = _strip(wc.load_json(path))
            assert outs[1] == outs[workers], 'JSON differs between --workers 1 and --workers N'
    finally:
        rc.json_path = keep
    print(f'  4 END2END rates_data.json identical for --workers 1 and --workers {workers}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=max(2, min(4, wpar.available_cpus())))
    ap.add_argument('--stride', type=int, default=40)
    a = ap.parse_args()
    p = wc.load_rates_params()
    J = load_jst(p['rates']['jst_path'])
    print(f'rates parallel parity: {a.workers} workers, stride {a.stride}, countries {COUNTRIES}')
    test_hoist(p, J, a.stride)
    test_parity(p, J, a.stride, a.workers)
    test_errors(p, J, a.workers)
    test_end_to_end(a.stride, a.workers)
    print('ALL OK')


if __name__ == '__main__':
    main()
