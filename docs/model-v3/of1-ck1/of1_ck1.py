"""OF1 and CK1 at the household arm's 10 death phases, shaped by the model's own functions (brief 089c): `sweeps.feasibility`, `out_sweeps.of1`, `sweeps.map_summary`, `sweeps.stress`.

Five scenario grid points x two fund settings; 27 schedule-grid points; tolerance x margin rules (`out_sweeps.TOLS`, `MARGINS`); 200 paths of the 128c per-path market returns (seed 20261118).
Every number is a scenario value at a labelled grid point and fund setting, not a forecast. Reuses 140c's helpers (`docs/model-v3/f1-household/f1_household.py`) for the points and the paths.

    python -I docs/model-v3/of1-ck1/of1_ck1.py [--points a,b] [--funds safe,market] [--n 200] [--seed 20261118] [--workers 2] [--out DIR]     writes of1_*.csv, ck1.csv, failed.csv
"""
import argparse, csv, importlib.util, sys, time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('f1h', HERE.parent / 'f1-household' / 'f1_household.py')
F = importlib.util.module_from_spec(spec); sys.modules['f1h'] = F; spec.loader.exec_module(F)
from model_v3.runner import out_sweeps as O, runner as R, sweeps as S

AMPS = (0, 1, 3, 5, 8, 12)            # the manifest's CK1 amplitudes (A1, A3, A5, A8, A12) and 0, whose positive P3 is carried as a finding (089c)
RULE = dict(closure_share_pct=75, m2_cap_pct_per_year=2.0, m4a_floor_pct=0)       # 083c's feasibility constants (the 75% threshold is the author's)
lab = lambda sp: '%s_k%s_r%03d' % (f"tm{round(100 * sp['tau_m'])}", f"{sp['k_ln']:g}".replace('.', ''), round(100 * sp['ratio']))


def light(cp, g0):
    """The evaluator `sweeps` reads, without the output groups the map does not need: `runner.core_run`, `headlines`, then only `out_sweeps.per_path` (the same numbers as `runner.evaluate`; the full
    evaluation runs every group's per_path, about ten times the cost). `g0` the paths (T, P), or None where `sweeps.stress` passes its own path."""
    def ev(sp, over=None, g=None, key=()):
        th, gg = {**cp.centre, **(over or {})}, np.asarray(g0 if g is None else g, float)
        raw = R.core_run(cp, th, sp, gg, np.full(gg.shape, cp.gdp_g))
        return {**R.headlines(raw, cp, th), 'sweeps': O.per_path(raw, R.env_of(cp, th, None, key), None)}
    return ev


def csv_out(path, head, rows):
    with open(path, 'w', newline='') as f:
        w = csv.writer(f, lineterminator='\n'); w.writerow(head); w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--points', default=','.join(F.POINTS)); ap.add_argument('--funds', default='safe,market'); ap.add_argument('--n', type=int, default=200)
    ap.add_argument('--seed', type=int, default=20261118); ap.add_argument('--workers', type=int, default=2); ap.add_argument('--out', default=str(HERE))
    a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    lv, ctx, inp = F.setup(); specs = S.grid(lv); g = F.paths_of(ctx, a.seed, a.n); mu = ctx.centre['I-D1a']
    grid, summ, ck, failed = [], [], [], []
    for fund in a.funds.split(','):
        for pn in a.points.split(','):
            t0 = time.time(); cp = F.point_ctx(ctx, inp, pn, fund)
            ev = light(cp, g)
            try:
                pts, _ = S.feasibility(ev, specs, a.workers)
            except ValueError:
                pts = []
                for sp in specs:
                    try:
                        pts += S.feasibility(ev, [sp])[0]
                    except ValueError as e:
                        failed.append((fund, pn, 'OF1', lab(sp), str(e).split(':')[0]))
            print(f'{fund} {pn}: OF1 {len(pts)} of {len(specs)} points, {time.time() - t0:.0f} s', file=sys.stderr, flush=True)
            for p in pts:
                for (tol, m), v in p['map'].items():
                    for hz, (f1, m2, m4) in v.items():
                        grid.append((fund, pn, p['schedule_grid'], p['w_min'], *O.tolabel(tol, m), hz, round(f1, 2), round(m2, 4), round(m4, 4)))
            for (tol, m), s in S.map_summary(pts, RULE).items():
                nm = s['named']
                summ.append((fund, pn, *O.tolabel(tol, m), round(s['best_any'][0], 2), '%s_%s' % s['best_any'][1:], '' if s['best_inside'] is None else round(s['best_inside'][0], 2),
                             '' if s['best_inside'] is None else '%s_%s' % s['best_inside'][1:], s['feasible'], 'none_passes_75' if nm is None else ';'.join(f'{k}={lab(v)}' for k, v in nm.items())))
            for sp in [dict(tau_0=0.04, tau_m=tm, k_ln=1.0, ratio=0.5) for tm in (0.5, 0.7, 0.9)] + [dict(tau_0=0.04, tau_m=0.7, k_ln=0.5, ratio=0.5)]:
                try:
                    res, top = S.stress(light(cp, None), sp, mu, AMPS, 100)
                except ValueError as e:
                    failed.append((fund, pn, 'CK1', lab(sp), str(e).split(':')[0])); continue
                for A, v in res.items():
                    ck.append((fund, pn, lab(sp), A, int(v['P1']), round(v['P3'], 2), round(v['P3_long'], 2), round(v['P7b'], 2), 'none' if top is None else top))
    csv_out(out / 'of1_grid.csv', ('fund', 'point', 'schedule_grid', 'w_min', 'tolerance', 'margin', 'horizon', 'F1_pct', 'M2', 'M4a'), grid)
    csv_out(out / 'of1_summary.csv', ('fund', 'point', 'tolerance', 'margin', 'best_F1_any', 'at', 'best_F1_inside_M2_M4a', 'at_inside', 'feasible_points', 'named_schedules_under_the_rule'), summ)
    csv_out(out / 'ck1.csv', ('fund', 'point', 'schedule', 'A', 'P1', 'P3_transition_plus_short', 'P3_all_years', 'P7b', 'zero_P3_up_to_A'), ck)
    csv_out(out / 'failed.csv', ('fund', 'point', 'output', 'schedule', 'alarm'), failed)


if __name__ == '__main__':
    main()
