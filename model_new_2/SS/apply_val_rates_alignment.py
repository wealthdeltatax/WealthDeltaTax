"""
apply_val_rates_alignment.py: STEP 1 of bringing valgen in line with RATES.

What it does (and nothing else):
  wdt_core.py     tau() becomes schedule-aware (logistic | logistic_ln | ladder), same maths as rate_vec.
                  New: rate_params(p), rate_spec_from_scenario(p, name), with_rate_scenario(p, name=None).
                  The six hard-wired 4-key rate dicts become rate_params(p). The two honest-run caches key on the
                  schedule too (otherwise a ladder run could be served a logistic result).
                  load_params() passes [val_gen] rate_scenario through.
  valgen_core.py  uses rate_params(p) wherever it built the 4-key dict; main() applies the rate scenario;
                  _flat() / the no-tax ceiling force the logistic (their maths needs a flat or zero rate);
                  the plan-S1 fixtures are skipped under any non-logistic schedule; meta.params records the schedule.
  WDT_Params.toml [val_gen] rate_scenario = "gain_ladder"  ("" = the legacy logistic in [rate]).

Numerics: for a p with no 'schedule' key (everything that exists today) results are bit-identical.
Under rate_scenario = "gain_ladder" VAL numbers MOVE (rate at GBP 20m: about 32% -> about 53%). Re-run
valgen_core.py and then every VAL presentation script.

Usage (from the folder that holds wdt_core.py; valgen_core.py and the TOML are looked up there, one level up and below):
    python apply_val_rates_alignment.py            # dry run: checks every anchor, writes nothing
    python apply_val_rates_alignment.py --write    # applies, keeps <file>.bak next to each file
    python apply_val_rates_alignment.py --dir PATH
Every edit must match the expected number of times, or the script stops and writes NOTHING.
"""

import argparse
import re
import sys
import tomllib
from pathlib import Path

# ───────────────────────────── the new wdt_core block (replaces def tau) ─────────────────────────────
CORE_BLOCK = r'''import bisect as _bisect

_RATE_KEYS = ('k', 'tau_0', 'tau_m', 'W_min')


def tau(W_m, p):
    """
    Marginal WDT rate on declared wealth W_m (pounds m). Schedule-aware scalar twin of rate_vec.

    p['schedule'] (absent = 'logistic'):
      'logistic'     tau(W) = tau_m / (1 + ((tau_m - tau_0) / tau_0) * exp(-k * (W - W_min)))
      'logistic_ln'  the same in ln(W / W_min); k is dimensionless; needs W_min > 0
      'ladder'       p['ladder'] = [(W, tau)] statutory anchors in pounds m, linear in ln W, flat beyond the ends
    tau(W) = 0 if W < W_min in every case. Key names are those of load_params (W_min, not wmin).
    The logistic branch is the original code, unchanged.
    """
    s = p.get('schedule', 'logistic')
    if s == 'logistic':
        if W_m < p['W_min']:
            return 0.0
        return p['tau_m'] / (
            1.0 + ((p['tau_m'] - p['tau_0']) / p['tau_0'])
            * math.exp(-p['k'] * (W_m - p['W_min']))
        )
    if W_m < p['W_min']:
        return 0.0
    if s == 'ladder':
        return _ladder_tau(W_m, p['ladder'], p.get('_lw'))
    if s == 'logistic_ln':
        if p['W_min'] <= 0.0:
            raise ValueError("schedule 'logistic_ln' needs W_min > 0")
        return p['tau_m'] / (
            1.0 + ((p['tau_m'] - p['tau_0']) / p['tau_0'])
            * math.exp(-p['k'] * math.log(W_m / p['W_min']))
        )
    raise ValueError(f'unknown schedule {s!r}')


def _ladder_tau(W, lad, lw=None):
    """Linear in ln W through the anchors lad = [(W, tau)], flat beyond the ends (same as np.interp on ln W)."""
    if W <= lad[0][0]:
        return lad[0][1]
    if W >= lad[-1][0]:
        return lad[-1][1]
    if lw is None:
        lw = [math.log(w) for w, _ in lad]
    x = math.log(W)
    i = _bisect.bisect_right(lw, x) - 1
    t0, t1 = lad[i][1], lad[i + 1][1]
    return t0 + (t1 - t0) * (x - lw[i]) / (lw[i + 1] - lw[i])


def rate_params(p):
    """
    The rate-function inputs of p: exactly the four logistic keys when p has no schedule (so legacy callers are unchanged),
    plus schedule / ladder / _lw for a non-logistic schedule. Use this wherever a function builds the dict tau() reads.
    """
    out = {k: p[k] for k in _RATE_KEYS}
    s = p.get('schedule', 'logistic')
    if s != 'logistic':
        out['schedule'] = s
        if s == 'ladder':
            out['ladder'] = p['ladder']
            out['_lw'] = p.get('_lw')
    return out


def _rate_key(p):
    """Hashable identity of the rate function of p (cache keys)."""
    r = rate_params(p)
    return (r['k'], r['tau_0'], r['tau_m'], r['W_min'], r.get('schedule', 'logistic'),
            tuple(tuple(a) for a in r.get('ladder', ())))


def rate_spec_from_scenario(p, name):
    """
    The rate design of a [rates.scenarios.NAME] as tau() inputs in pounds m (one source: RATES decides, VAL follows).
    Reads schedule, tau_0, tau_m, k_per_gbp_m / k_ln, wmin_house_ratio / wmin_gbp_m and anchor_from from the scenario merged over
    [rates.defaults], and builds a ladder with ladder_to_tau exactly as rates_core.calibration does. W_min comes out in pounds m
    (wmin_pct needs the wealth distribution and is not supported here). Returns the keys to merge into p.
    """
    rp = p['rates']
    if name not in rp['scenarios']:
        raise ValueError(f'rate scenario {name!r} is not defined in [rates.scenarios]')
    cfg = {**rp['defaults'], **rp['scenarios'][name]['overrides']}
    if cfg.get('wmin_pct'):
        raise ValueError(f"rate scenario {name!r} sets wmin_pct; VAL needs W_min in pounds m")
    wmin = cfg['wmin_gbp_m']
    if cfg.get('wmin_house_ratio'):
        wmin = cfg['wmin_house_ratio'] * rp['dist']['house_median_gbp_m']
    sched = cfg['schedule']
    spec = {'tau_0': cfg['tau_0'], 'tau_m': cfg['tau_m'], 'k': cfg['k_per_gbp_m'], 'W_min': wmin, 'schedule': 'logistic'}
    if sched not in ('logistic', 'logistic_ln'):
        sp = rp['schedules'][sched]
        lad, _ = ladder_to_tau(sp['anchors'], sp['basis'], sp['r_ref'], sp['c_ref'], cfg['tau_m'])
        spec.update({'schedule': 'ladder', 'ladder': lad, '_lw': [math.log(w) for w, _ in lad]})
    elif sched == 'logistic_ln':
        spec.update({'schedule': 'logistic_ln', 'k': cfg['k_ln']})
    if cfg.get('anchor_from'):
        sp = rp['schedules'][cfg['anchor_from']]
        lad, _ = ladder_to_tau(sp['anchors'], sp['basis'], sp['r_ref'], sp['c_ref'], cfg['tau_m'])
        W_ref, tau_ref = lad[-1]
        spec['k'] = fit_k(sched, cfg['tau_0'], cfg['tau_m'], wmin, W_ref, tau_ref)
    return spec


def with_rate_scenario(p, name=None):
    """
    Copy of p with the rate design of a RATES scenario merged in. name defaults to p['val_gen']['rate_scenario'];
    '' keeps the legacy logistic in [rate]. Sets p['rate_scenario'] so the choice is stamped into outputs.
    """
    if name is None:
        name = p['val_gen'].get('rate_scenario', '')
    q = dict(p)
    if name:
        q.update(rate_spec_from_scenario(p, name))
    else:
        q['schedule'] = 'logistic'
    q['rate_scenario'] = name
    return q
'''

CORE_FUNC_RE = re.compile(r"def tau\(W_m, p\):.*?\n    \)\n", re.S)   # def tau ... through its closing ')' line
RATE4_RE = re.compile(r"\{k: (p|p_in)\[k\] for k in \('k', 'tau_0', 'tau_m', 'W_min'\)\}")


def lit(s):
    return re.compile(re.escape(s))


# (file, [(compiled pattern, replacement string or callable, expected matches)])
PLAN = [
    ('wdt_core.py', [
        (CORE_FUNC_RE, lambda m: CORE_BLOCK, 1),
        (RATE4_RE, lambda m: f'rate_params({m.group(1)})', 6),
        (lit("p['k'], p['tau_0'], p['tau_m'], p['W_min']"), lambda m: '_rate_key(p)', 2),
        (lit("'example_alphas': _FL('example_alphas'),"),
         lambda m: m.group(0) + "\n        'rate_scenario': str(vg.get('rate_scenario', '')),", 1),
    ]),
    ('valgen_core.py', [
        (lit('from wdt_core import load_params, tau, simulate, run_pair, run_sim_hist, settle_tw_flows'),
         lambda m: m.group(0) + ', rate_params, with_rate_scenario', 1),
        (RATE4_RE, lambda m: f'rate_params({m.group(1)})', 6),
        (lit("return dict(p, tau_m=p['tau_0'], W_min=0.0)"),
         lambda m: "return dict(p, tau_m=p['tau_0'], W_min=0.0, schedule='logistic')", 1),
        (lit("p0 = dict(p, tau_0=1e-12, tau_m=1e-12)"),
         lambda m: "p0 = dict(p, tau_0=1e-12, tau_m=1e-12, schedule='logistic')", 1),
        (lit("    return all(abs(p[k] - PLAN_S1_BASELINE[k]) < 1e-12 for k in (keys or PLAN_S1_BASELINE))"),
         lambda m: ("    if keys is None and p.get('schedule', 'logistic') != 'logistic':\n"
                    "        return False                      # the fixtures are for the baseline logistic only\n" + m.group(0)), 1),
        (lit("    p = load_params()\n    N, g = p['N_val'], p['g']"),
         lambda m: "    p = with_rate_scenario(load_params())      # rate design from [val_gen] rate_scenario\n    N, g = p['N_val'], p['g']", 1),
        (lit("'index_rate': ir, **{k: v for k, v in vg.items()}},"),
         lambda m: ("'index_rate': ir, 'rate_scenario': p.get('rate_scenario'),\n"
                    "                       'schedule': p.get('schedule', 'logistic'), 'ladder': p.get('ladder'),\n"
                    "                       **{k: v for k, v in vg.items()}},"), 1),
    ]),
    ('WDT_Params.toml', [
        (lit('envelope_unit = "real"\n'),
         lambda m: (m.group(0) +
                    "# rate_scenario : the rate design VAL runs under = a name in [rates.scenarios.*]. Its schedule (ladder / logistic),\n"
                    "#                 tau_m, W_min (e.g. the median house price) are read from there by wdt_core.with_rate_scenario, so RATES\n"
                    "#                 and VAL share one source. \"\" = the legacy logistic in [rate].\n"
                    'rate_scenario = "gain_ladder"\n'), 1),
    ]),
]


def find(name, base):
    for cand in (base / name, base.parent / name):
        if cand.exists():
            return cand
    hits = sorted(base.rglob(name)) or sorted(base.parent.rglob(name))
    return hits[0] if hits else None


def apply(text, edits, label):
    errors = []
    for i, (pat, rep, want) in enumerate(edits, 1):
        n = len(pat.findall(text))
        if n != want:
            errors.append(f'{label} edit {i}: matched {n} times, expected {want}: {pat.pattern[:70]!r}')
            continue
        text = pat.sub(rep, text)
    return text, errors


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dir', default='.')
    ap.add_argument('--write', action='store_true')
    a = ap.parse_args()
    base = Path(a.dir).resolve()
    results, errors = {}, []
    for name, edits in PLAN:
        path = find(name, base)
        if path is None:
            errors.append(f'{name}: not found under {base} or its parent')
            continue
        text, errs = apply(path.read_text(encoding='utf-8'), edits, name)
        errors += errs
        if not errs:
            try:
                if name.endswith('.py'):
                    compile(text, name, 'exec')
                else:
                    tomllib.loads(text)
            except (SyntaxError, tomllib.TOMLDecodeError) as exc:
                errors.append(f'{name}: patched text does not parse: {exc}')
        results[name] = (path, text, len(edits))
    if errors:
        print('NOTHING WRITTEN. Problems:')
        for e in errors:
            print('  -', e)
        sys.exit(1)
    for name, (path, text, n) in results.items():
        print(f'{"WRITE" if a.write else "ok   "} {path}  ({n} edits)')
        if a.write:
            path.with_suffix(path.suffix + '.bak').write_text(path.read_text(encoding='utf-8'), encoding='utf-8')
            path.write_text(text, encoding='utf-8')
    print('\nNow: python test_rate_schedules.py, then python valgen_core.py and every VAL presentation script.'
          if a.write else '\nDry run only. Re-run with --write to apply.')


if __name__ == '__main__':
    main()
