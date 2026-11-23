"""run.py -- the run script (V3-12; architecture.md 6.5, acceptance.md 2).  python -I -c "import sys; sys.path.insert(0, '.'); from model_v3 import run; run.main(['--out', DIR])"  (--paths N, --seed S, --smoke, --arm legacy, --final refused)
Named schedules by the manifest's rule on the first household point; every scenario-grid point (level 1, tornado; O1e at the first point only); `scenario_range`: lowest p10 to highest p90, centre `no_central` where points differ.
Author rulings 2026-11-23: household arm first, legacy a labelled comparator; markers `no_payer_at_launch` (O2, O2d, OW3 at D4_5), `not_run_this_point` (O1e); OF1 and CK1 pending until 140c, 089c. Sets no environment variable.
"""
from __future__ import annotations

import argparse, copy, datetime, json, sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import yaml

from model_v3.core import pack as pk, returns as rt
from model_v3.out import assemble as asm, writer as wr
from model_v3.runner import out_sweeps as osw, runner as R, sweeps as S

ROOT = Path(__file__).resolve().parents[1]
MANIFEST, INPUTS, LEVERS = ROOT / 'docs/model-v3/outputs.yml', ROOT / 'registry/inputs.json', ROOT / 'model_v3/levers.json'
HH_INPUTS, PACKS = ROOT / 'docs/model-v3/cell-baseline/inputs_used.json', ROOT / 'model_v3/pack'   # the pack folder is found, never named (R11)
SEED, SMOKE = 20261118, (50, 3, 20)
POINTS = {'median_mid': ('median', 'mid'), 'max_mid': ('max', 'mid'), 'median_low': ('median', 'low'), 'min_mid': ('min', 'mid'), 'median_high': ('median', 'high')}   # saving, regime; the arm's grid points
NO_PAYER, NO_CENTRAL, NOT_RUN, NO_PAYER_IDS = 'no_payer_at_launch', 'no_central', 'not_run_this_point', ('O2', 'O2b', 'O2c', 'O2d', 'OH1b', 'OH1c', 'OW3')
HELD = {'OW1': 'legacy_only'}   # household arm: a labelled marker, never a number (author, 2026-11-23; 121c, 135c)
PENDING = {'OF1': 'feasibility_rule_pending_140c_089c', 'CK1': 'feasibility_rule_pending_140c_089c'}
FORMS = {'p10_mean_p90': ('p10', 'mean', 'p90'), 'point_and_range': ('lo', 'point', 'hi')}

def ckey(c):
    return (c.get('schedule'), c['horizon'], c.get('line'), tuple(sorted(c['by'].items())))

def scenario_range(docs):
    """The range rule, in one place: per cell the lowest low and highest high over the points; the centre slot is NO_CENTRAL where the points differ. A null at any point stays null."""
    out = copy.deepcopy(docs[0])
    for oid, o in out.items():
        if o['summary'] not in FORMS:
            continue
        lo_f, c_f, hi_f = FORMS[o['summary']]
        at = [{ckey(c): c for c in d[oid]['cells']} for d in docs]
        for c in o['cells']:
            cs = [a[ckey(c)] for a in at if ckey(c) in a]
            if any(x[f] is None for x in cs for f in (lo_f, c_f, hi_f)):
                c.update({lo_f: None, c_f: None, hi_f: None})
            elif len({(x[lo_f], x[c_f], x[hi_f]) for x in cs}) > 1:
                c.update({lo_f: min(x[lo_f] for x in cs), hi_f: max(x[hi_f] for x in cs), c_f: NO_CENTRAL})
    return out

def mark_no_payer(outs):
    for oid in NO_PAYER_IDS:
        for c in outs.get(oid, {}).get('cells', []):
            if c['by'].get('wealth_band') not in (None, 'overall') and any(c[f] is None for f in FORMS['p10_mean_p90']):   # a band with no payer under the schedule, and what derives from it
                c.update(p10=NO_PAYER, mean=NO_PAYER, p90=NO_PAYER)

def reduce(oid, form, line, v):   # per-path arrays -> what assemble expects (author, 2026-11-23): one value for `point`; for OR1 the share over paths, P10 and P90 across paths (P7a in pct)
    v = np.asarray(v, float) * (100 if line == 'P7a' else 1)
    if form == 'point':
        u = np.unique(v)
        if u.size != 1: raise ValueError(f'{oid}: a value-only output must be one value on every path, found {u.size}')
        return u
    if oid == 'OT1': return np.array([v[0], v[1:].min(), v[1:].max()])   # a tornado swing is written lo to hi (V6); the signed effects are in the tornado itself
    v = v[np.isfinite(v)]
    if not v.size: raise ValueError(f'{oid} {line}: no path has a value')
    return np.array([v.mean(), *np.percentile(v, (10, 90))])

def run_point(ctx, inp, pt, named, man, n1, n2p, draws, seed, tol, be):
    """(output docs, level 1 info) of one grid point: level 1 at the named schedules, the tornado (OT1) and the break-even return (O1e), assembled provisionally."""
    cp = ctx if pt is None else replace(ctx, arm=dict(arm='household', inputs=inp, saving=POINTS[pt][0], regime=POINTS[pt][1]))
    st = rt.streams(seed); smp, info = R.level1(cp, named, st['level1_paths'], n=n1)
    ev = R.make_ev(cp, st['tornado_crn'].standard_normal((R.T, n2p)))
    smp.update(osw.ot1(S.tornado(ev, named, {i: cp.reg[i] for i in cp.tier1}, R.reads(cp))))
    if be: smp.update(osw.o1e(S.breakeven_return(ev, named, R.RET['mean'], draws=draws, tol=tol)))   # break-even only at the first point (author, 2026-11-23; 150c does the speed)
    ents = asm.entries(man)
    smp.update({o: {k: reduce(o, ents[o]['summary'], k[3], v) for k, v in smp[o].items()} for o in smp if ents[o]['summary'] == 'point' or o in ('OR1', 'OT1')})
    hold = HELD if pt else {}; [smp.pop(o, None) for o in hold]   # household arm: nothing is computed for a held id
    return asm.assemble(man, smp, None, 'provisional', hold)[0], info

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--paths', type=int); p.add_argument('--seed', type=int, default=SEED); p.add_argument('--out', required=True)
    p.add_argument('--smoke', action='store_true'); p.add_argument('--final', action='store_true'); p.add_argument('--arm', choices=('household', 'legacy'), default='household')
    a = p.parse_args(argv)
    n1, n2, n2p = (SMOKE if a.smoke else (R.N1, R.N2, R.N2P))
    n1 = a.paths or n1
    if a.final: sys.exit('--final is refused: it waits for 137c, 135c, 138c and 139c and the every-test rule (brief 057 block 3)')
    man, lv = yaml.safe_load(MANIFEST.read_text(encoding='utf-8')), json.loads(LEVERS.read_text(encoding='utf-8'))
    tier1 = next(o for o in man['outputs'] if o['id'] == 'OT1')['by']['input']
    once = [e['id'] for e in asm.entries(man).values() if e.get('once_not_per_schedule')]
    ctx = R.context(pk.load_pack(next(d for d in sorted(PACKS.iterdir()) if (d / 'manifest.json').is_file())), pk.load_register(INPUTS), lv, tier1, list(asm.entries(man)), once)
    inp = json.loads(HH_INPUTS.read_text(encoding='utf-8'))
    pts = [None] if a.arm == 'legacy' else list(POINTS)[:1 if a.smoke else None]   # smoke tests the structure on the first grid point; the range merge has its own test
    c0 = ctx if pts[0] is None else replace(ctx, arm=dict(arm='household', inputs=inp, saving=POINTS[pts[0]][0], regime=POINTS[pts[0]][1]))
    st = rt.streams(a.seed)
    fmap, _ = S.feasibility(R.make_ev(c0, st['tornado_crn'].standard_normal((R.T, n2p))), S.grid(lv))
    named = S.choose(fmap, man['feasibility'])
    if named is None: sys.exit('no feasible schedule point under the manifest rule: nothing is chosen in its place')
    draws = R.draw_theta(st['level2_draws'], ctx, ctx.tier1, n2)
    docs, failed, info = [], [], None
    for pt in pts:
        try:
            d, i = run_point(ctx, inp, pt, named, man, n1, n2p, draws, a.seed, 1.0 if a.smoke else 1e-2, pt in (None, pts[0]))
        except ValueError as exc:   # a point that fails its own checks (I1) is reported and left out, never repaired
            failed.append(f'{pt}: {str(exc)[:80]}'); continue
        docs.append(d); info = info or i; print(f'{pt or "legacy"}: {len(d)} outputs', flush=True)
    if not docs: sys.exit('every grid point failed: ' + '; '.join(failed))
    outs = scenario_range(docs) if len(docs) > 1 else docs[0]
    mark_no_payer(outs)
    for c in outs['O1e']['cells'] if len(pts) > 1 else []: c['point'] = NOT_RUN   # O1e ran at the first point only: no centre across the points
    outs.update({oid: {'summary': asm.entries(man)[oid]['summary'], 'cells': [], 'pending': lab} for oid, lab in PENDING.items()})
    label = dict(arm='legacy', legacy_consumption=ctx.centre['I-D14c'], central=False, note='legacy result, not a calibrated forecast') if a.arm == 'legacy' else \
        dict(arm='household', central=False, points=[x for x in pts if not any(f.startswith(f'{x}:') for f in failed)], failed=failed, note='range across labelled scenario-grid points; no central value')
    run = wr.run_block(man, MANIFEST, INPUTS, LEVERS, dict(status='provisional', run_date=datetime.date.today().isoformat(), model_version='model_v3', paths=n1, base_year=int(str(ctx.pack.base_year)[:4]),
                       pack_country=ctx.pack.country, pack_sha256=ctx.pack.sha256, seed=a.seed, level2_draws=n2, level2_paths=n2p, unfilled_paths=info['unfilled_paths']['S_central'], arm=label))
    path = wr.write_outputs(a.out, wr.document(outs, {}, run), MANIFEST, INPUTS)
    print(f'wrote {path}: {json.dumps({k: run[k] for k in ("status", "paths", "seed", "level2_draws", "unfilled_paths")})}; arm {label["arm"]}, points {label.get("points", "legacy")}, failed {len(failed)}')

if __name__ == '__main__':
    main()
