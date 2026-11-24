"""
lien_rerun.py -- brief 132c, block 3: the two 127c points (`min_mid`, `median_high`) rerun with the pension-secured lien, 20 paths (the arm has no spread; paths move only the fund).
Per point: the run_grid checks (account residual, unpaid, unpaid_B, shortfall lines, ledger ties) plus the lien: where it arises (line, first year, amount), its size against that line's pension and
non-pension wealth, how many years it is carried, what settles from the classes and what from the pension, and what stays unpaid. Units: millions of pounds per adult (real), the lien balance
`bal` unweighted per line; the receivable of the public ledger is in billions (`ledger['rec']`). No headline number is read or written. Run from the repository root:
python -I docs/model-v3/household-arm-run/lien_rerun.py [--paths N] [--out DIR]
Writes lien_alarms.csv (the floor and unpaid alarms, first year by line), lien_checks.csv (one row a point) and lien_lines.csv (one row a point and line that ever carried a lien, the instance of the largest balance over the phases and paths); prints only summary lines.
"""
import argparse
import csv
import sys
from pathlib import Path

import numpy as np
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT), str(HERE)]

import run_grid as G                                                           # noqa: E402  (the same builder, points and checks)
from model_v3.runner import arm as ab                                          # noqa: E402

L = 14
LINES = ('point', 'line', 'instances', 'first_year', 'lien_new_first', 'bal_max', 'year_of_max', 'pension_at_max', 'nonpension_at_max', 'years_carried', 'settled_from_classes', 'settled_from_pension')   # the instance with the largest balance


class Log(ab.HouseholdHook):
    """Logs the lien of every line instance (phase, path, line) at each year's close; `Log.rec[(phase, i)]` holds the instance's history."""
    rec, ph, alarm = {}, 0, {}

    def _start(self, book):
        Log.ph += 1
        super()._start(book)

    def pre(self, book, t, g):
        self.t = t
        out = super().pre(book, t, g)
        for i in np.flatnonzero(np.abs(self.fl) > 0):
            k = ('floor', int(i % L))
            Log.alarm[k] = min(Log.alarm.get(k, (t, float(self.fl[i]))), (t, float(self.fl[i])))              # the first year over the phases and paths
        return out

    def lien(self):
        out, npw = super().lien(), sum(self.q[k] for k in ab.CLASSES[:3])
        new, bal, sc, wo = (np.zeros(len(self.PL)) + np.asarray(out[k]) for k in ('new', 'bal', 'settled', 'wo'))
        for i in np.flatnonzero((bal > 0) | (new > 0) | (sc > 0) | (wo > 0)):
            r = Log.rec.setdefault((Log.ph, int(i)), dict(first=self.t, new=float(new[i]), years=0, bal=0.0, pen=0.0, npw=0.0, c=0.0, p=0.0, wo=0.0))
            r['wo'] += float(wo[i])                                                                                    # 148c: the year's write-off (what the heir floor leaves, the limited recourse of 138c, a dead line's lien)
            r['years'] += int(bal[i] > 0)
            r['c'] += float(self.set_c[i]) if np.ndim(self.set_c) else 0.0
            r['p'] += float(self.set_p[i]) if np.ndim(self.set_p) else 0.0
            if bal[i] > r['bal']:
                r.update(bal=float(bal[i]), pen=float(self.q['pension'][i]), npw=float(npw[i]), at=self.t)
        for i in np.flatnonzero(np.asarray(self.unpaid) > 0):
            k = ('unpaid', int(i % L))
            Log.alarm[k] = min(Log.alarm.get(k, (self.t, float(self.unpaid[i]))), (self.t, float(self.unpaid[i])))          # what the lien could not settle (expected none)
        return out


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--paths', type=int, default=20)
    p.add_argument('--out', default=str(HERE))
    p.add_argument('--points', default='min_mid,median_high')
    p.add_argument('--pension-withdrawal', choices=('low', 'mid', 'high'), help='148c: files get the suffix _wd_<setting>')
    p.add_argument('--heir-floor', type=int, choices=(0, 25, 50), help='148c: files get the suffix _floor<N>; 0 is today\'s settlement (the same run, with the write-off columns)')
    a = p.parse_args(argv)
    flow = {k: v for k, v in (('pension_withdrawal', a.pension_withdrawal), ('heir_floor', a.heir_floor)) if v is not None}
    sfx = (f'_wd_{a.pension_withdrawal}' if a.pension_withdrawal else '') + (f'_floor{a.heir_floor}' if a.heir_floor is not None else '')
    ctx, inp = G.A.setup()
    manifest = yaml.safe_load((ROOT / 'docs' / 'model-v3' / 'outputs.yml').read_text())
    chk, lines, alarms, orig = [], [], [], ab.HouseholdHook
    for name in a.points.split(','):
        Log.rec, Log.ph, Log.alarm = {}, 0, {}
        ab.HouseholdHook = Log
        try:
            rows, c = G.run_point(G.point_ctx(ctx, inp, name, flow=flow), inp, name, manifest, a.paths, a.paths)
        finally:
            ab.HouseholdHook = orig
        base = G.R.shaped(ctx, ctx.centre, G.A.SPEC['ratio'])
        by = {}
        for (ph, i), r in Log.rec.items():
            by.setdefault(i % L, []).append(r)
        for i, rs in sorted(by.items()):
            r = max(rs, key=lambda x: (x['bal'], x['new']))
            lines.append(dict(point=name, line=base.labels[i], instances=len(rs), first_year=min(x['first'] for x in rs), lien_new_first=r['new'], bal_max=r['bal'], year_of_max=r.get('at', ''), pension_at_max=r['pen'],
                              nonpension_at_max=r['npw'], years_carried=r['years'], settled_from_classes=r['c'], settled_from_pension=r['p'], written_off=r['wo'], written_off_all_instances=sum(x['wo'] for x in rs)))
        alarms += [dict(point=name, alarm=k, line=base.labels[i], first_year=t, amount_millions_pounds_per_adult=x) for (k, i), (t, x) in sorted(Log.alarm.items(), key=lambda kv: (kv[0][0], kv[1][0]))]
        c = dict(c, **({} if not flow else dict(written_off_total=sum(r['wo'] for r in Log.rec.values()), written_off_instances=sum(r['wo'] > 0 for r in Log.rec.values()))), paths=a.paths, lien_lines=len({i % L for _, i in Log.rec}), lien_instances=len(Log.rec), i1='held, no raise' if not c.get('error') else 'FAILED')
        chk.append(c)
        print(f"{name}: lien on {c['lien_lines']} line(s), {c.get('error') or 'no error'}, shortfall lines {c.get('shortfall_lines')}, unpaid_B max {c.get('unpaid_B_max')}", flush=True)
    for f, cols, data in ((f'lien_checks{sfx}.csv', None, chk), (f'lien_lines{sfx}.csv', LINES + (('written_off', 'written_off_all_instances') if flow else ()), lines), (f'lien_alarms{sfx}.csv', ('point', 'alarm', 'line', 'first_year', 'amount_millions_pounds_per_adult'), alarms)):
        cols = cols or sorted({k for d in data for k in d})
        with open(Path(a.out) / f, 'w', newline='') as fh:
            w = csv.DictWriter(fh, cols, extrasaction='ignore')
            w.writeheader()
            w.writerows(data)


if __name__ == '__main__':
    main()
