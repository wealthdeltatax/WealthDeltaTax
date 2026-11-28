"""run.py -- the run script (V3-12; architecture.md 6.5, acceptance.md 2).  python -I -c "import sys; sys.path.insert(0, 'model'); from model_v3 import run; run.main(['--out', DIR])"
--size smoke|quick|final (explicit --paths, --o1e-draws, --workers, --point override), --seed S, --arm legacy, --parts level1,map,tornado,o1e (default all; map required; a subset writes `run.parts` and is never final); --final is refused; --unit plan|point:P|o1e-point|o1e:S:A:B [--plan-file F] writes one partial file of a split run, --merge DIR merges them (183c; design in results/split-run/design.md), and no flag runs all of them in one process: the unsplit run is plan, units, merge.  Named schedules by the manifest's rule; `scenario_range`: lowest p10 to highest p90, centre `no_central`.
Author rulings 2026-11-23: household arm first; O1e at the first point only, fund_return=market (the safe fund ignores the mean), range over draws `not_run_this_run` at 0 draws; markers `no_payer_at_launch`; OF1, CK1 pending. Sets NPY_DISABLE_CPU_FEATURES (numerics.py, imported first: one numerics path on every machine, 169c)."""
from __future__ import annotations
import argparse, copy, datetime, hashlib, json, os, subprocess, sys, time, types
from model_v3 import numerics  # noqa: F401  first, before numpy: one numerics path (169c)
from dataclasses import replace; from pathlib import Path
import numpy as np
import yaml
from model_v3.core import pack as pk, returns as rt, support as U
from model_v3.out import assemble as asm, split as sp, writer as wr
from model_v3.runner import out_sweeps as osw, runner as R, sweeps as S
ROOT = Path(__file__).resolve().parents[2]
MANIFEST, INPUTS, LEVERS = ROOT / 'model-specs/outputs.yml', ROOT / 'data/input-register/inputs.json', ROOT / 'model/model_v3/levers.json'
HH_INPUTS, PACKS = ROOT / 'results/cell-baseline/inputs_used.json', ROOT / 'data/country-packs'   # the pack folder is found, never named (R11)
SEED, TNM = 20261118, 'reform_not_defined'   # TNM: O8 cell marker only (author, 2026-11-26): the reform-in-place comparator has no value here (no base share, or its target is not met); run.arm.targets keeps status target_not_met
SIZES = dict(smoke=(50, 20, 3, 1.0, 1), quick=(1000, 50, 0, 1e-2, 5), final=(R.N1, R.N2P, R.N2, 1e-2, 5))   # paths, tornado paths, O1e draws, break-even tolerance, grid points
POINTS = {'median_mid': ('median', 'mid'), 'max_mid': ('max', 'mid'), 'median_low': ('median', 'low'), 'min_mid': ('min', 'mid'), 'median_high': ('median', 'high')}   # saving, regime; the arm's grid points
NO_SIGN, NO_PAYER, NO_CENTRAL, NOT_RUN_RUN, NO_PAYER_IDS = 'no_sign_change_0_15',  'no_payer_at_launch', 'no_central', 'not_run_this_run', ('O2', 'O2b', 'O2c', 'O2d', 'OH1b', 'OH1c', 'OW3', 'O8')
PARTS, PART_OF = ('level1', 'map', 'tornado', 'o1e'), {'OT1': 'tornado', 'O1e': 'o1e'}   # 178c: map = OF1, CK1 (pending) and the named schedules every part reads; level1 = every other id
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
        at = [{ckey(c): c for c in d[oid]['cells']} for d in docs if oid in d]
        for c in o['cells']:
            cs = [a[ckey(c)] for a in at if ckey(c) in a]   # an output not computed at a point (O1e) is not in its doc
            if any(x[f] is None for x in cs for f in (lo_f, c_f, hi_f)):
                c.update({lo_f: None, c_f: None, hi_f: None})
            elif len({(x[lo_f], x[c_f], x[hi_f]) for x in cs}) > 1:
                c.update({lo_f: min(x[lo_f] for x in cs), hi_f: max(x[hi_f] for x in cs), c_f: NO_CENTRAL})
    return out

def mark_no_payer(outs):
    for oid in NO_PAYER_IDS:
        for c in outs.get(oid, {}).get('cells', []):
            if (oid == 'O8' or c['by'].get('wealth_band') not in (None, 'overall')) and any(c[f] is None for f in FORMS['p10_mean_p90']):   # a band with no payer under the schedule and what derives from it; O8: the target was not met
                m = TNM if oid == 'O8' else NO_PAYER; c.update(p10=m, mean=m, p90=m)
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

def run_point(ctx, inp, pt, named, man, n1, n2p, seed, w=1, parts=PARTS):
    """(output docs, level 1 info, cap) of one grid point: level 1 and the tornado (OT1), assembled provisionally. O1e is its own unit (o1e_unit), merged by `merge`."""
    cp = ctx if pt is None else replace(ctx, arm=dict(arm='household', inputs=inp, saving=POINTS[pt][0], regime=POINTS[pt][1]))
    st, cap = rt.streams(seed), {}
    with U.capping(cap):   # a comparator that cannot raise its target stays at the cap and is recorded (the first record, level 1's, stands): the point is labelled, never repaired
        smp, info = R.level1(cp, named, st['level1_paths'], n=n1, workers=w, cap=cap) if 'level1' in parts else ({}, dict(unfilled_paths=dict(S_central=0)))
        eps = st['tornado_crn'].standard_normal((R.T, n2p)); ev = R.make_ev(cp, eps, heads=True)   # the tornado reads headlines only (151c)
        smp.update(osw.ot1(S.tornado(ev, named, {i: cp.reg[i] for i in cp.tier1}, R.reads(cp), workers=w)) if 'tornado' in parts else {})
    ents = asm.entries(man)
    smp.update({o: {k: reduce(o, ents[o]['summary'], k[3], v) for k, v in smp[o].items()} for o in smp if ents[o]['summary'] == 'point' or o in ('OR1', 'OT1')})
    hold = HELD if pt else {}; [smp.pop(o, None) for o in hold]   # household arm: nothing is computed for a held id
    return asm.assemble(man, smp, None, 'provisional', hold)[0], info, cap

def parts_of(a):
    return tuple(x for x in PARTS if x in a.parts.split(','))

def setup(a):
    """What every unit shares: the sizes, the manifest, the context and the grid points."""
    n1, n2p, n2, tol, npts = SIZES[a.size]
    man, lv = yaml.safe_load(MANIFEST.read_text(encoding='utf-8')), json.loads(LEVERS.read_text(encoding='utf-8'))
    tier1 = next(o for o in man['outputs'] if o['id'] == 'OT1')['by']['input']
    once = [e['id'] for e in asm.entries(man).values() if e.get('once_not_per_schedule')]
    ctx = R.context(pk.load_pack(next(d for d in sorted(PACKS.iterdir()) if (d / 'manifest.json').is_file())), pk.load_register(INPUTS), lv, tier1, list(asm.entries(man)), once)
    pts = [None] if a.arm == 'legacy' else (a.point or list(POINTS)[:npts])   # the range merge has its own test
    return types.SimpleNamespace(man=man, lv=lv, ctx=ctx, inp=json.loads(HH_INPUTS.read_text(encoding='utf-8')), pts=pts, n1=a.paths or n1, n2p=n2p, n2=n2 if a.o1e_draws is None else a.o1e_draws, tol=tol)

def arm_ctx(g, pt, market=False):
    return g.ctx if pt is None else replace(g.ctx, arm=dict(arm='household', inputs=g.inp, saving=POINTS[pt][0], regime=POINTS[pt][1], **({'fund_return': 'market'} if market else {})))

def probe():
    """A fingerprint of the numpy exp, log and pow paths: equal in every shard of a run, or the partials were made on different numerics (169c)."""
    x = np.abs(np.random.default_rng(7).standard_normal(100000)) + 0.5
    return hashlib.sha256(b''.join(np.asarray(f(x), float).tobytes() for f in (np.exp, np.log, lambda v: v ** 1.7))).hexdigest()[:16]

def git_sha():
    try: return subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError): return 'unknown'

def common(g, a, named):
    """The header fields every partial of one run must carry equal (split.COMMON)."""
    return dict(size=a.size, seed=a.seed, arm=a.arm, n1=g.n1, n2p=g.n2p, n2=g.n2, tol=g.tol, points=[p or 'legacy' for p in g.pts], schedules=list(named), batch=a.batch, git_sha=git_sha(),
                inputs={**{k: wr.sha256_file(f) for k, f in dict(manifest=MANIFEST, inputs=INPUTS, levers=LEVERS, hh_inputs=HH_INPUTS).items()}, 'pack': g.ctx.pack.sha256},
                numerics=dict(variable=os.environ.get('NPY_DISABLE_CPU_FEATURES'), numpy=np.__version__, python=sys.version.split()[0], probe=probe()), parts=list(parts_of(a)))

def parse_unit(t):
    k, *r = t.split(':')
    if k == 'point' and len(r) == 1 or k == 'plan' and not r or k == 'o1e-point' and not r: return sp.unit(k, point=r[0] if r else None)
    if k == 'o1e' and len(r) == 3 and r[1].isdigit() and r[2].isdigit(): return sp.unit(k, schedule=r[0], a=int(r[1]), b=int(r[2]))
    raise ValueError(f'--unit: plan, point:P, o1e-point or o1e:SCHEDULE:A:B, found {t!r}')

def plan_unit(g, a):
    """The feasibility map and the named schedules, once: every other unit reads `named` from this partial."""
    c0, st = arm_ctx(g, g.pts[0]), rt.streams(a.seed)
    fmap, _ = S.feasibility(R.make_ev(c0, st['tornado_crn'].standard_normal((R.T, g.n2p)), only=('sweeps',)), S.grid(g.lv), workers=a.workers)
    named = S.choose(fmap, g.man['feasibility'])
    if named is None: sys.exit('no feasible schedule point under the manifest rule: nothing is chosen in its place')
    return sp.dumps(dict(header=sp.header('plan', sp.unit('plan'), common(g, a, named), a.workers), body=dict(named=sp.enc([[s, list(spec.items())] for s, spec in named.items()]))))

def named_of(plan):
    """The named schedules of a decoded plan partial, in the order and with the keys in the order the plan chose them (JSON sorts the keys of a dict, not the items of a list)."""
    return {s: dict(kv) for s, kv in sp.dec(plan['body']['named'])}

def unit_head(g, a, plan_raw, u, draws=None):
    named = named_of(sp.loads(plan_raw))
    return named, sp.header(u['kind'], u, common(g, a, named), a.workers, sp.sha256(plan_raw), None if draws is None else sp.draws_sha(draws))

def point_unit(g, a, plan_raw, u):
    """Level 1 and the tornado of one grid point; a `ValueError` is recorded as the point's failure, as the unsplit run reports it."""
    named, h = unit_head(g, a, plan_raw, u)
    try: d, info, cap = run_point(g.ctx, g.inp, None if u['point'] == 'legacy' else u['point'], named, g.man, g.n1, g.n2p, a.seed, a.workers, parts_of(a))
    except ValueError as exc: return sp.dumps(dict(header=h, body=dict(failed=str(exc)[:80], doc=None, info=None, cap={})))
    return sp.dumps(dict(header=h, body=dict(failed=None, doc=d, info=sp.enc(info), cap=sp.enc(cap))))

def o1e_unit(g, a, plan_raw, u):
    """O1e at the first point under the market fund: the point roots and end values (`o1e-point`) or a batch of draws of one schedule (`o1e`)."""
    draws = R.draw_theta(rt.streams(a.seed)['level2_draws'], g.ctx, g.ctx.tier1, g.n2) if g.n2 else {}   # all draws, then the slice: the Latin hypercube depends on n
    named, h = unit_head(g, a, plan_raw, u, draws)
    eps, cap, body = rt.streams(a.seed)['tornado_crn'].standard_normal((R.T, g.n2p)), {}, {}
    evm = R.make_ev(arm_ctx(g, g.pts[0], market=True), eps, heads=True)
    try:
        with U.capping(cap):
            if u['kind'] == 'o1e-point':
                roots = S.breakeven_return(evm, named, R.RET['mean'], tol=g.tol, workers=a.workers)
                body = dict(roots={s: sp.enc(r) for s, (r, _) in roots.items()}, ends={s: sp.enc([S._mean(evm(named[s], {R.RET['mean']: m})['M1']['short']) for m in (0.0, 15.0)]) for s, (r, _) in roots.items() if not np.isfinite(r)})   # no root: the end values show the sign
            else:
                body = dict(roots=sp.enc(S.breakeven_return(evm, {u['schedule']: named[u['schedule']]}, R.RET['mean'], draws=sp.slice_draws(draws, u['a'], u['b']), tol=g.tol, workers=a.workers, point=False)[u['schedule']][1]))
    except ValueError as exc: body = dict(error=str(exc)[:80])
    return sp.dumps(dict(header=h, body=dict(roots=None, error=None) | body | dict(cap=sp.enc(cap))))

def merge(files, g, a):
    """The merged output document from the partials `files` [(name, bytes)]: the unsplit run's last lines, over the partials. `check` and the header of this run must agree first."""
    got = sp.check(files); named = named_of(got['plan'])
    for f, v in common(g, a, named).items():
        if got['plan']['header'][f] != v: raise sp.SplitError(f"header field {f}: {got['plan']['header'][f]!r} in the partials, {v!r} in this invocation")
    parts, o1e = parts_of(a), [v for k, v in got.items() if k.startswith('o1e')]
    docs, failed, info, tg, ends = [], [], None, [], {}
    for pt in g.pts:
        b, cap = got['point:' + (pt or 'legacy')]['body'], sp.dec(got['point:' + (pt or 'legacy')]['body']['cap'])
        err = b['failed'] or (next((x['body']['error'] for x in o1e if x['body']['error']), None) if pt == g.pts[0] else None)   # a failure of O1e fails the first point, as in the unsplit run
        if err: failed.append(f'{pt}: {err[:80]}'); continue
        d = b['doc']
        if pt == g.pts[0] and 'o1e' in parts:
            r0 = sp.dec(got['o1e-point']['body']['roots']); ends = sp.dec(got['o1e-point']['body']['ends'])
            for x in o1e: [cap.setdefault(k, v) for k, v in sp.dec(x['body']['cap']).items()]   # the first record stands, in the order the unsplit run evaluates
            roots = {s: (r0[s], [r for k, x in got.items() if k.startswith(f'o1e:{s}:') for r in sp.dec(x['body']['roots'])]) for s in named}
            d = {**d, **asm.assemble(g.man, osw.o1e(roots) if g.n2 else {'O1e': {(s, 'single', (), None): np.full(3, r) for s, (r, _) in roots.items()}}, None, 'provisional', {})[0]}
        docs.append(d); info = info or sp.dec(b['info']); tg.append(dict(point=pt, status='target_not_met' if cap else 'met', shortfalls={k: dict(reached=v[0], target=v[1]) for k, v in cap.items()}))
        print(f'{pt or "legacy"}: {len(d)} outputs', flush=True)
    if not docs: sys.exit('every grid point failed: ' + '; '.join(failed))
    outs = scenario_range(docs) if len(docs) > 1 else docs[0]; mark_no_payer(outs); n2, pts = g.n2, g.pts
    for c in outs.get('O1e', {}).get('cells', []): c.update(point=NO_SIGN if c['point'] is None else c['point'], **({} if n2 else dict(lo=NOT_RUN_RUN, hi=NOT_RUN_RUN)))   # no root in 0 to 15; no range over draws at 0 draws
    outs.update({o: {'summary': e['summary'], 'cells': [], 'not_run': NOT_RUN_RUN} for o, e in asm.entries(g.man).items() if ('map' if o in PENDING else PART_OF.get(o, 'level1')) not in parts})   # a part not run: its ids carry the marker, never a value (178c)
    outs.update({oid: {'summary': asm.entries(g.man)[oid]['summary'], 'cells': [], 'pending': lab} for oid, lab in PENDING.items()})
    label = dict(arm='legacy', legacy_consumption=g.ctx.centre['I-D14c'], central=False, note='legacy result, not a calibrated forecast') if a.arm == 'legacy' else \
        dict(arm='household', central=False, points=[x for x in pts if not any(f.startswith(f'{x}:') for f in failed)], failed=failed, targets=tg, met=f"{sum(t['status'] == 'met' for t in tg)} of {len(tg)} points met their target", note='range across all labelled scenario-grid points; no central value',
             o1e=dict(point=pts[0], fund_return='market', draws=n2, ends_0_15=ends, note='O1e at the first point only, fund_return=market (the safe fund ignores the generator mean)'), size=a.size)   # `workers` is no longer written: it is not a result (183c)
    run = wr.run_block(g.man, MANIFEST, INPUTS, LEVERS, dict(status='provisional', run_date=a.run_date or datetime.date.today().isoformat(), model_version='model_v3', paths=g.n1, base_year=int(str(g.ctx.pack.base_year)[:4]),
                       pack_country=g.ctx.pack.country, pack_sha256=g.ctx.pack.sha256, seed=a.seed, level2_draws=n2, level2_paths=g.n2p, unfilled_paths=info['unfilled_paths']['S_central'], arm=label))
    run |= {} if parts == PARTS else dict(parts=list(parts))   # a default run writes no `parts`: its file is unchanged
    path = wr.write_outputs(a.out, wr.document(outs, {}, run), MANIFEST, INPUTS)
    print(f'wrote {path}: {json.dumps({k: run[k] for k in ("status", "paths", "seed", "level2_draws", "unfilled_paths")})}; arm {label["arm"]}, points {label.get("points", "legacy")}, failed {len(failed)}')

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--size', choices=SIZES, default='final'); p.add_argument('--paths', type=int); p.add_argument('--o1e-draws', type=int); p.add_argument('--workers', type=int, default=1)
    p.add_argument('--point', action='append', choices=list(POINTS)); p.add_argument('--seed', type=int, default=SEED); p.add_argument('--out', required=True); p.add_argument('--final', action='store_true')
    p.add_argument('--arm', choices=('household', 'legacy'), default='household'); p.add_argument('--parts', default=','.join(PARTS))
    p.add_argument('--unit'); p.add_argument('--plan-file'); p.add_argument('--merge', metavar='DIR'); p.add_argument('--batch', type=int, default=25); p.add_argument('--run-date')
    a = p.parse_args(argv); ps = a.parts.split(',')
    if set(ps) - set(PARTS) or 'map' not in ps: p.error(f'--parts: a comma list from {",".join(PARTS)} that includes map (every part reads its schedules), found {a.parts!r}')
    if a.final: sys.exit('--final is refused: it waits for the every-test rule (brief 057 block 3)')
    if a.unit and a.merge: p.error('--unit and --merge are different runs')
    g = setup(a)
    if a.unit:
        try: u = parse_unit(a.unit)
        except ValueError as exc: p.error(str(exc))
        if (u['kind'] == 'plan') == bool(a.plan_file): p.error('--plan-file is the partial of the plan, and every unit but the plan needs it')
        t0 = time.time(); plan_raw = Path(a.plan_file).read_bytes() if a.plan_file else None
        raw = plan_unit(g, a) if u['kind'] == 'plan' else (point_unit if u['kind'] == 'point' else o1e_unit)(g, a, plan_raw, u)
        name = sp.uid(sp.loads(raw)['header']).replace(':', '_'); Path(a.out).mkdir(parents=True, exist_ok=True); (Path(a.out) / f'{name}.json').write_bytes(raw)
        cpu = next((l.split(':', 1)[1].strip() for l in open('/proc/cpuinfo') if l.startswith('model name')), 'unknown') if os.path.exists('/proc/cpuinfo') else 'unknown'
        (Path(a.out) / f'{name}.meta.json').write_text(json.dumps(dict(unit=name, seconds=round(time.time() - t0, 1), workers=a.workers, cpu=cpu, cores=os.cpu_count()), sort_keys=True) + '\n'); print(f'wrote {name}.json')
        return
    if a.merge:
        try: return merge([(f.name, f.read_bytes()) for f in sorted(Path(a.merge).glob('*.json')) if not f.name.endswith('.meta.json')], g, a)
        except sp.SplitError as exc: sys.exit(f'merge refused: {exc}')   # nothing is written, nothing repaired
    files = [('plan', plan_unit(g, a))]   # the unsplit run is the split run in one process: plan, the units in the canonical order, merge
    for k in sp.expected(sp.loads(files[0][1])['header'])[1:]:
        u = parse_unit(k); files.append((k, (point_unit if u['kind'] == 'point' else o1e_unit)(g, a, files[0][1], u)))
    merge(files, g, a)

if __name__ == '__main__':
    main()
