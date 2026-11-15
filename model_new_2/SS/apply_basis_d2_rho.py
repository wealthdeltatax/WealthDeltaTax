"""
apply_basis_d2_rho.py  --  D2 gain ladder as the baseline, D1/D1a real basis for VAL with JST replay, D1c rho block.
Refactor plan decisions D2, D1, D1a, D1b, D1c.

    python apply_basis_d2_rho.py "C:\Users\kyleo\OneDrive\My Documents\Hobbies\Wealth Delta Tax\Model" --check     (reports anchors, writes nothing)
    python apply_basis_d2_rho.py MODEL_DIR             (backups *.pre_d2.bak, then writes)

MODEL_DIR holds WDT_Params.toml, wdt_core.py, wdt_jst.py; valgen_core.py is looked up in MODEL_DIR/VAL then MODEL_DIR.
Prerequisites: apply_rates_t100.py (not required by any anchor here, but run it first). Every edit needs its anchor
found EXACTLY once or nothing is written. CRLF files are handled. A second run is refused (marker in the TOML).

D2  TOML   [rates.defaults]: schedule = "gain_ladder", wmin_house_ratio = 1.0, dist_kw = body split. Every ablation scenario
           inherits it, so all of them re-derive on the ladder. Scenarios that are logistic by design get schedule = "logistic"
           (and, where they are the OLD logistic grid, wmin_house_ratio = 0.0 and dist_kw = {} so their numbers do not move):
           tau0_*, k_*, taum_*, wmin_1m/5m/top5/top2 (parked), logistic_gain, logistic_stock, wmin_house.
           wealth_x13 keeps the body split. New: logistic_ref (the former baseline, as a comparison schedule) and wmin_all
           (ladder, every adult in scope). [rates.figures] rate_grid starts at logistic_ref; scope = wmin_all, baseline, wmin_house_hp.
           RETIRED: [rate]; [sweep] tau_0_canon, tau_m_canon, k_canon, W_min_canon (N_canon, V0_canon, g_canon stay).
           There is no legacy_logistic scenario in the file (nothing to remove); logistic_ref is its replacement as a comparison.
   wdt_core load_params: [rate] optional; absent, p['tau_0'], p['tau_m'], p['k'], p['W_min'] come from the RATES defaults
           (so the legacy SSM that sets N_fill now sees W_min = £0.225m, tau_0 30%, k 0.005). '' as a rate scenario = the defaults.
D1  TOML   [val_gen] basis = "jst" | "manual" | "legacy". "jst": g_real and index_rate derived at run time from JST
           (wdt_jst.real_basis_inputs on [rates].uk_iso, optional basis_years) and stamped into the JSON meta.
   wdt_jst load_jst(), real_return_series().   wdt_core with_val_basis() / jst_basis().
D1a valgen _p7_replay: the headline rule sets x lambda {0, lambda_base} re-run on the real JST return paths of loop windows
           (wrap = True, repeats flagged, contiguous reported separately). TOML replay_stride (0 = off), replay_countries.
D1c TOML   [rho] base, sweep (0, 2.5, 3.5, 5%). wdt_core p['rho'] = [rho].base, p['rho_sens'] = the sweep.
   valgen  family3_pair adds pv_rel_by_rho; _p5_search: SST is the primary state test (n_conflict = SST conflicts;
           n_conflict_spt / _sst / _any kept), SPT is reported at every rho (spt_by_rho); verdict SPT_by_rho; JSON key 'rho'.
Also    valgen check reset_rule_removes_overstatement_gain relaxed from "allow > +3%" to "reset <= allow and reset < 0.5%":
        the 3% was tuned to nominal 10.45% growth and would abort the run on a real 4.4% basis.
        TOML [val_gen] growth_vals re-centred on real growth.

NOT DONE: [sweep] g_vals (the LIFE / CDS grid) is still the nominal 10.45% grid; rebuild with the VAL tables. hist_mean,
[budget], [tcm], [[tiers]], [[brackets]], N_fill still exist (D11). The first real run is the first test of these anchors.
"""
import re
import sys
from pathlib import Path

MARK = '# D2 patch (apply_basis_d2_rho.py)'


def rd(path):
    raw = Path(path).read_bytes().decode('utf-8')
    crlf = '\r\n' in raw
    return raw.replace('\r\n', '\n'), crlf


def wr(path, text, crlf):
    Path(path).write_bytes((text.replace('\n', '\r\n') if crlf else text).encode('utf-8'))


def plain(text, old, new, label, problems):
    n = text.count(old)
    if n != 1:
        problems.append(f'{label}: anchor found {n} times')
        return text
    return text.replace(old, new)


def rx(text, pattern, repl, label, problems, flags=re.M):
    new, n = re.subn(pattern, repl if callable(repl) else (lambda m, r=repl: r), text, flags=flags)
    if n != 1:
        problems.append(f'{label}: pattern matched {n} times')
        return text
    return new


# ───────────────────────── TOML ─────────────────────────
OLD_LOGISTIC = ['tau0_015_k_002', 'tau0_010_k_003', 'tau0_010_k_005', 'tau0_010', 'tau0_020', 'taum_050', 'taum_090',
                'k_0005', 'k_002', 'wmin_1m', 'wmin_5m', 'wmin_top5', 'wmin_top2']
LOGISTIC_ONLY = ['logistic_gain', 'logistic_stock', 'wmin_house']

RHO_BLOCK = '''# ─────────────────────────────────────────────────────────────
# [rho] — the real discount rate, state side only (D1c)
# rho is REAL and enters only the state's present value of receipts (SPT, breakeven spread). The family objective stays undiscounted
# terminal true net worth. SST (the state's terminal stake) is discount-free and is the PRIMARY state test; SPT is reported at every
# rho in the sweep. base = 3.5%: HMT Green Book STPR, years 0 to 30. Read by wdt_core.load_params into p['rho'] and p['rho_sens'].
# [val] rho_sweep (the fine grid for the legacy C.12 / Fig 7.4-7.6 tables) is unchanged.
# ─────────────────────────────────────────────────────────────
[rho]
base  = 0.035
sweep = [0.0, 0.025, 0.035, 0.05]

'''

BASIS_BLOCK = '''# basis : the economy VAL runs on (D1, D1a).
#   "jst"    g_real and index_rate are DERIVED at run time from the JST history RATES uses: the geometric-mean REAL capital return and
#            REAL GDP/head growth of [rates].uk_iso, over basis_years if given (else every usable year). Stamped into the JSON
#            (meta.params.val_basis_info). Hand values from print_val_real_inputs.py, for comparison: g_real 0.0442, index_rate 0.01872.
#   "manual" g_real and index_rate below, as numbers (a REAL return and REAL GDP/head growth).
#   "legacy" nominal hist_mean and [budget] budget_growth. Kept only until D11 retires them.
basis = "jst"
# basis_years = [1950, 2017]
# g_real     = 0.0442
# index_rate = 0.0187
# JST replay (D1a, D1b): the headline rule sets x lambda {0, lambda_base} re-run on the real return path of each JST loop window
# (wrap = True; windows that repeat years are flagged, not dropped; `contiguous` windows reported separately). The strategy library
# runs once per window, so cost = windows x 4 searches. 0 = no replay. index_rate stays the constant above.
replay_stride    = 10
replay_countries = ["GBR"]
'''

RETIRED_RATE = '''# [rate] RETIRED (D2, apply_basis_d2_rho.py). The rate design is [rates.defaults] (the gain ladder, W_min = 1 x median house price);
# a named variant is a [rates.scenarios.*]. wdt_core.load_params fills p['tau_0'], p['tau_m'], p['k'], p['W_min'] from those defaults
# for the legacy SSM only. The former baseline (logistic 30% / 90% / k 0.005, every adult in scope) is [rates.scenarios.logistic_ref].
'''

RETIRED_CANON = '''# tau_0_canon, tau_m_canon, k_canon, W_min_canon RETIRED (D2): they described the old logistic (15% / 70% / 0.001 / £2m).
# load_params falls back to p['tau_0'] ... p['W_min'] (the RATES defaults) for any legacy reader. N_canon, V0_canon, g_canon stay.
'''


def scen_block(name, label, lines):
    return f'[rates.scenarios.{name}]\nlabel = "{label}"\n' + '\n'.join(lines) + '\n\n'


def patch_toml(t, problems):
    if MARK in t:
        problems.append('TOML: already patched (marker found)')
        return t
    # ---- [rates.defaults]
    t = rx(t, r'^schedule\s+= "logistic"[^\n]*$',
           MARK + ': the gain ladder is the baseline everywhere (D2). Logistics are comparison schedules only.\n'
           'schedule         = "gain_ladder"   # "logistic" | "logistic_ln" | a name in [rates.schedules.*]\n'
           'wmin_house_ratio = 1.0             # W_min = ratio x median house price at launch (0.0 = off: every adult in scope, or wmin_gbp_m / wmin_pct)',
           'toml defaults schedule', problems)
    t = rx(t, r'^dist_kw\s+= \{\}[^\n]*$',
           'dist_kw          = { body_split = 5, body_split_from = 0.5 }   # overrides for the distribution builder (a scenario that sets dist_kw REPLACES this); '
           'body split lets W_min fall inside a decile',
           'toml defaults dist_kw', problems)
    # ---- scenarios that must stay logistic
    for name in OLD_LOGISTIC:
        t = rx(t, rf'^(\[rates\.scenarios\.{name}\]\nlabel = [^\n]*\n)',
               lambda m: m.group(1) + 'schedule = "logistic"\nwmin_house_ratio = 0.0\ndist_kw = {}\n',
               f'toml scenario {name}', problems)
    for name in LOGISTIC_ONLY:
        t = rx(t, rf'^(\[rates\.scenarios\.{name}\]\nlabel = [^\n]*\n)',
               lambda m: m.group(1) + 'schedule = "logistic"\n', f'toml scenario {name}', problems)
    t = plain(t, 'dist_kw = { wealth_scale = 1.3 }', 'dist_kw = { body_split = 5, body_split_from = 0.5, wealth_scale = 1.3 }',
              'toml wealth_x13 dist_kw', problems)
    # ---- new comparison scenarios
    t = t.rstrip('\n') + '\n\n' + '# ═══ D2 patch: comparison schedules (the logistic survives only here) ═══\n' + \
        scen_block('logistic_ref', 'Logistic 30% / 90% / k 0.005, every adult in scope (the former baseline, comparison only)',
                   ['schedule = "logistic"', 'wmin_house_ratio = 0.0', 'dist_kw = {}']) + \
        scen_block('wmin_all', 'Gain ladder, every adult in scope (W_min = 0)', ['wmin_house_ratio = 0.0'])
    t = rx(t, r'^  "tau0_015_k_002", "tau0_010_k_003", "tau0_010_k_005",$',
           lambda m: m.group(0) + '\n  "logistic_ref", "wmin_all",', 'toml run.scenarios', problems)
    t = plain(t, 'rate_grid    = ["baseline", "tau0_015_k_002"', 'rate_grid    = ["logistic_ref", "tau0_015_k_002"', 'toml figures rate_grid', problems)
    t = plain(t, 'scope        = ["baseline", "wmin_house", "wmin_house_hp"]', 'scope        = ["wmin_all", "baseline", "wmin_house_hp"]',
              'toml figures scope', problems)
    # ---- retire [rate] and the [sweep] rate canon
    t = rx(t, r'^\[rate\]\ntau_0 = 0\.3[^\n]*\ntau_m = 0\.90[^\n]*\nk     = 0\.005[^\n]*\nW_min = 1\.0[^\n]*\n', RETIRED_RATE,
           'toml [rate]', problems)
    t = rx(t, r'^tau_0_canon = 0\.15[^\n]*\ntau_m_canon[^\n]*\nk_canon[^\n]*\nW_min_canon[^\n]*\n', RETIRED_CANON,
           'toml [sweep] canon', problems)
    # ---- rho
    t = rx(t, r'^rho    = 0\.035  # 3\.5% real discount rate[^\n]*$',
           '# rho moved to [rho] base / sweep (D1c).', 'toml [val] rho', problems)
    t = rx(t, r'(^# ─+\n)(# \[val_gen\] — VAL generational model)', lambda m: RHO_BLOCK + m.group(1) + m.group(2),
           'toml insert [rho]', problems)
    # ---- val_gen basis
    t = rx(t, r'^# g_real / index_rate : VAL on the REAL basis.*?^# index_rate = [0-9.]+\n', BASIS_BLOCK,
           'toml val_gen basis', problems, flags=re.M | re.S)
    t = plain(t, '"" = the legacy logistic in [rate].', '"" = the [rates.defaults] design (the gain ladder, D2).', 'toml rate_scenario comment', problems)
    t = plain(t, 'growth_vals   = [0.03, 0.05, 0.07, 0.1045, 0.15]',
              'growth_vals   = [0.01, 0.03, 0.05, 0.07, 0.10]   # REAL growth (D1); the JST UK mean is about 4.4%', 'toml growth_vals', problems)
    t = plain(t, '# state_tol     : SPT and SST tolerance, two-sided: state PV and stake within this share of honest.',
              '# state_tol     : SPT and SST tolerance, two-sided: state PV and stake within this share of honest. SST (stake, discount-free) is the\n'
              '#                 PRIMARY state test; SPT is a sensitivity reported at each rho in [rho] sweep (D1c).', 'toml state_tol comment', problems)
    t = plain(t, 'note = "Among gaining strategies, state PV within state_tol"',
              'note = "Among gaining strategies, state PV within state_tol; a sensitivity across the [rho] sweep"', 'toml SPT note', problems)
    t = plain(t, 'note = "Among gaining strategies, state terminal stake within state_tol"',
              'note = "Among gaining strategies, state terminal stake within state_tol; the primary state test (discount-free)"',
              'toml SST note', problems)
    return t


# ───────────────────────── wdt_core ─────────────────────────
WITH_VAL_BASIS = '''_JST_BASIS_CACHE = {}


def jst_basis(p, J=None):
    """
    REAL basis inputs of VAL from the JST history ([val_gen] basis = "jst"): geometric-mean real capital return (g_real) and real
    GDP/head growth (index_rate) of [rates].uk_iso, over [val_gen] basis_years (default: every usable year). One source with RATES.
    Returns wdt_jst.real_basis_inputs plus 'source', 'iso', 'jst_path'. Cached per (file, country, years).
    """
    import wdt_jst
    rp, vg = p['rates'], p['val_gen']
    yrs = tuple(range(vg['basis_years'][0], vg['basis_years'][1] + 1)) if vg.get('basis_years') else None
    key = (rp['jst_path'], rp['uk_iso'], yrs)
    if key not in _JST_BASIS_CACHE:
        if J is None:
            here = Path(__file__).resolve().parent
            J = wdt_jst.load_jst(rp['jst_path'], [here, here / 'RATES', here.parent])
        out = wdt_jst.real_basis_inputs(J, rp['uk_iso'], years=yrs)
        out.update({'source': 'jst', 'iso': rp['uk_iso'], 'jst_path': rp['jst_path']})
        _JST_BASIS_CACHE[key] = out
    return dict(_JST_BASIS_CACHE[key])


def with_val_basis(p, J=None):
    """
    Copy of p on the basis VAL runs in, per [val_gen] basis:
      'jst'     g_real and index_rate derived from JST (jst_basis); p['g'] becomes the real return
      'manual'  [val_gen] g_real (REAL return) replaces p['g']; index_rate (REAL GDP/head growth) is the W_min / k index,
                else [budget] budget_growth (legacy)
      'legacy'  the legacy numbers: nominal hist_mean, budget_growth
    Sets p['val_basis'] ('real' | 'legacy_nominal'), p['index_rate'] and p['val_basis_info'].
    """
    vg = p['val_gen']
    q = dict(p)
    basis = vg.get('basis') or ('manual' if vg.get('g_real') is not None else 'legacy')
    info = {'source': basis}
    g_real = None
    if basis == 'jst':
        info = jst_basis(p, J)
        g_real, idx = info['g_real'], info['index_rate']
    elif basis == 'manual':
        g_real = float(vg['g_real'])
        idx = float(vg['index_rate']) if vg.get('index_rate') is not None else p['budget_growth']
    else:
        idx = p['budget_growth']
    if g_real is not None:
        q['g'] = g_real
    q['index_rate'] = idx
    q['val_basis'] = 'real' if g_real is not None else 'legacy_nominal'
    q['val_basis_info'] = info
    return q
'''


def patch_core(t, problems):
    if "def jst_basis(" in t:
        problems.append('wdt_core: already patched')
        return t
    t = plain(t, "    if name not in rp['scenarios']:\n        raise ValueError(f'rate scenario {name!r} is not defined in [rates.scenarios]')\n"
                 "    cfg = {**rp['defaults'], **rp['scenarios'][name]['overrides']}\n",
              "    if name in (None, ''):                      # '' = the [rates.defaults] design (D2: the gain ladder is the baseline)\n"
              "        cfg = dict(rp['defaults'])\n"
              "    elif name not in rp['scenarios']:\n"
              "        raise ValueError(f'rate scenario {name!r} is not defined in [rates.scenarios]')\n"
              "    else:\n"
              "        cfg = {**rp['defaults'], **rp['scenarios'][name]['overrides']}\n", 'core rate_spec_from_scenario', problems)
    t = plain(t, "    '' keeps the legacy logistic in [rate]. Sets p['rate_scenario'] so the choice is stamped into outputs.",
              "    '' = the [rates.defaults] design (D2). Sets p['rate_scenario'] so the choice is stamped into outputs.", 'core with_rate_scenario doc', problems)
    t = plain(t, "    q = dict(p)\n    if name:\n        q.update(rate_spec_from_scenario(p, name))\n    else:\n        q['schedule'] = 'logistic'\n    q['rate_scenario'] = name\n",
              "    q = dict(p)\n    q.update(rate_spec_from_scenario(p, name))\n    q['rate_scenario'] = name or 'defaults'\n", 'core with_rate_scenario body', problems)
    t = rx(t, r'^def with_val_basis\(p\):.*?\n    return q\n', WITH_VAL_BASIS, 'core with_val_basis', problems, flags=re.M | re.S)
    t = plain(t, "    for n, s in scenarios.items():\n        sc_ = s['overrides'].get('schedule')\n",
              "    _ds = defaults.get('schedule')\n"
              "    if _ds not in (None, 'logistic', 'logistic_ln') and _ds not in schedules:\n"
              "        raise ValueError(f\"[rates.defaults] schedule={_ds!r} is not defined in [rates.schedules]\")\n"
              "    for n, s in scenarios.items():\n        sc_ = s['overrides'].get('schedule')\n", 'core _parse_rates defaults schedule', problems)
    t = plain(t, "    p['tau_0'] = float(raw['rate']['tau_0'])\n    p['tau_m'] = float(raw['rate']['tau_m'])\n"
                 "    p['k']     = float(raw['rate']['k'])\n    p['W_min'] = float(raw['rate']['W_min'])\n",
              "    p['rates'] = _parse_rates(raw.get('rates'))\n"
              "    if 'rate' in raw:                           # a file that still has the legacy [rate] table\n"
              "        p['tau_0'] = float(raw['rate']['tau_0'])\n        p['tau_m'] = float(raw['rate']['tau_m'])\n"
              "        p['k']     = float(raw['rate']['k'])\n        p['W_min'] = float(raw['rate']['W_min'])\n"
              "    else:                                       # D2: [rate] retired; the RATES defaults (gain ladder) feed the legacy SSM only\n"
              "        _spec = rate_spec_from_scenario(p, '')\n"
              "        p['tau_0'], p['tau_m'], p['k'], p['W_min'] = _spec['tau_0'], _spec['tau_m'], _spec['k'], _spec['W_min']\n",
              'core load_params [rate]', problems)
    t = plain(t, "    p['rho']   = float(raw['val']['rho'])\n",
              "    _rh = raw.get('rho', {})                     # D1c: [rho] base and sweep (real, state side only)\n"
              "    p['rho']   = float(_rh.get('base', raw['val'].get('rho', 0.035)))\n"
              "    p['rho_sens'] = sorted({float(x) for x in _rh.get('sweep', [p['rho']])} | {p['rho']})\n"
              "    if min(p['rho_sens']) < 0.0:\n        raise ValueError('[rho] values must be >= 0')\n", 'core load_params rho', problems)
    t = plain(t, "        'g_real': (float(vg['g_real']) if 'g_real' in vg else None),\n"
                 "        'index_rate': (float(vg['index_rate']) if 'index_rate' in vg else None),\n",
              "        'g_real': (float(vg['g_real']) if 'g_real' in vg else None),\n"
              "        'index_rate': (float(vg['index_rate']) if 'index_rate' in vg else None),\n"
              "        'basis': str(vg.get('basis', 'manual' if 'g_real' in vg else 'legacy')),\n"
              "        'basis_years': ([int(x) for x in vg['basis_years']] if 'basis_years' in vg else None),\n"
              "        'replay_stride': int(vg.get('replay_stride', 0)),\n"
              "        'replay_countries': [str(x) for x in vg.get('replay_countries', [])],\n", 'core load_params val_gen keys', problems)
    t = plain(t, "    p['names_val'] = {",
              "    _b = p['val_gen']['basis']\n"
              "    if _b not in ('jst', 'manual', 'legacy'):\n"
              "        raise ValueError(f\"[val_gen] basis must be jst | manual | legacy, got {_b!r}\")\n"
              "    if _b == 'manual' and p['val_gen']['g_real'] is None:\n"
              "        raise ValueError('[val_gen] basis = \"manual\" needs g_real (and index_rate)')\n"
              "    if p['val_gen']['basis_years'] is not None and len(p['val_gen']['basis_years']) != 2:\n"
              "        raise ValueError('[val_gen] basis_years must be [first, last]')\n"
              "    p['names_val'] = {", 'core load_params basis validation', problems)
    return t


# ───────────────────────── wdt_jst ─────────────────────────
JST_FUNCS = '''def load_jst(name, dirs):
    """Parse the JST JSON `name`, looked up in each directory of `dirs` in order. Raises FileNotFoundError listing what was tried."""
    tried = []
    for d in dirs:
        path = Path(d) / name
        tried.append(str(path))
        if path.exists():
            with open(path, 'r', encoding='utf-8') as fh:
                return json.load(fh)
    raise FileNotFoundError(f'JST file not found; tried {tried}')


def real_return_series(J, iso):
    """
    {year: REAL capital return} for one JST country: (1 + capital_tr) / (1 + CPI inflation) - 1, for every year in which the return
    and this year's and the prior year's CPI are present. The series VAL replays (D1a); window rules are loop_windows on its sorted years.
    """
    ret = _jst_series(J, iso, 'capital_tr')
    cpi = _jst_series(J, iso, 'cpi')
    return {y: (1.0 + r) / (cpi[y] / cpi[y - 1]) - 1.0 for y, r in sorted(ret.items()) if y in cpi and (y - 1) in cpi}


'''


def patch_jst(t, problems):
    if 'def real_return_series(' in t:
        problems.append('wdt_jst: already patched')
        return t
    t = plain(t, 'import math\n\n\ndef usable_years', 'import json\nimport math\nfrom pathlib import Path\n\n\ndef usable_years', 'jst imports', problems)
    t = plain(t, "if __name__ == '__main__':", JST_FUNCS + "if __name__ == '__main__':", 'jst funcs', problems)
    t = plain(t, "    print('wdt_jst self-tests ok:', window_summary(w_loop))",
              "    rs = real_return_series(J, 'XXX')\n"
              "    assert sorted(rs) == [2001, 2002, 2003, 2004, 2005] and abs(rs[2003] - (1.10 / 1.02 - 1.0)) < 1e-12, rs\n"
              "    print('wdt_jst self-tests ok:', window_summary(w_loop))", 'jst selftest', problems)
    return t


# ───────────────────────── valgen_core ─────────────────────────
PV_HELPER = '''def _pv_rel_at(p: dict, h: dict, a: dict, rho: float):
    """(PV(a) - PV(h)) / PV(h) of the state's receipts at discount rate rho; None where the honest PV is too small (as family3_pair)."""
    pv_h, pv_a = pv_true(h, rho), pv_true(a, rho)
    return ((pv_a - pv_h) / pv_h if pv_h >= p['val_gen']['pv_rel_min_frac'] * abs(h['family_true_T']) else None)


'''

REPLAY = '''def _geo_mean(xs: list) -> float:
    return math.exp(sum(math.log1p(x) for x in xs) / len(xs)) - 1.0


def _p7_summary(rows: list, key: str) -> dict:
    """Share of windows passing BRG / SST and the spread of the best-response gain, full loop and contiguous-only."""
    out = {}
    for name, keep in (('full_loop', lambda r: True), ('contiguous', lambda r: r['contiguous'])):
        cells = [r['cells'][key] for r in rows if keep(r)]
        if not cells:
            out[name] = None
            continue
        gains = sorted(c['gain'] for c in cells)
        out[name] = {'windows': len(cells),
                     'BRG_pass_share': sum(1 for c in cells if c['BRG']) / len(cells),
                     'SST_pass_share': sum(1 for c in cells if c['SST']) / len(cells),
                     'gain_max': gains[-1], 'gain_median': gains[len(gains) // 2], 'gain_min': gains[0]}
    return out


def _p7_replay(p: dict, strategies: list) -> dict:
    """
    D1a / D1b. The headline rule sets x lambda {0, lambda_base} on the REAL JST capital-return path of each loop window of
    [val_gen] replay_countries (wdt_jst.loop_windows, wrap = True; every start_stride-th start). T = [val_gen] T. The strategy
    library runs once per window. Windows that repeat years are flagged (`repeat`), not dropped; `contiguous` marks windows that
    cross no seam, summarised separately. index_rate stays the constant of the basis. Returns {} content 'skipped' when replay_stride = 0.
    """
    vg = p['val_gen']
    stride = int(vg.get('replay_stride', 0))
    if stride <= 0 or not vg.get('replay_countries'):
        print('  (JST replay skipped: replay_stride = 0 or no replay_countries)')
        return {'skipped': True}
    rp = p['rates']
    here = Path(__file__).resolve().parent
    J = load_jst(rp['jst_path'], [here, here / 'RATES', here.parent, here.parent / 'RATES'])
    T = vg['T']
    rules = vg['headline_rules']
    lams = [0.0, vg['lambda_base']]
    out = {'T': T, 'stride': stride, 'rules': rules, 'lambda_vals': lams,
           'note': 'real JST capital return path (CPI-deflated) per loop window; constant index_rate; wrap = True, repeats flagged',
           'countries': {}}
    for iso in vg['replay_countries']:
        r = real_return_series(J, iso)
        years = sorted(r)
        wins = loop_windows(years, T, wrap=True)[::stride]
        rows = []
        for w in wins:
            ser = [r[y] for y in w['years']]
            cells = {}
            for rule in rules:
                for lam in lams:
                    s = _p5_search(p, rule, lam, strategies, ser=ser)
                    cells[f'{rule}|{lam}'] = {'gain': s['best']['gain'], 'label': s['best']['label'], 'BRG': s['BRG_pass'],
                                              'SST': s['SST_pass'], 'SPT': s['SPT_pass'], 'n_conflict': s['n_conflict']}
            rows.append({'start': w['start'], 'wraps': w['wraps'], 'repeat': w['repeat'], 'contiguous': w['contiguous'],
                         'g_geo': _geo_mean(ser), 'cells': cells})
        summ = {k: _p7_summary(rows, k) for k in rows[0]['cells']} if rows else {}
        out['countries'][iso] = {'usable_years': len(years), 'windows': len(rows),
                                 'repeat_windows': sum(1 for x in rows if x['repeat']), 'rows': rows, 'summary': summ}
        print(f"  replay {iso}: {len(years)} usable years, {len(rows)} windows (stride {stride}), "
              f"{sum(1 for x in rows if x['contiguous'])} contiguous, {sum(1 for x in rows if x['repeat'])} with repeats")
        for k, sm in summ.items():
            for nm in ('full_loop', 'contiguous'):
                c = sm[nm]
                if c:
                    print(f"    {k:<34} {nm:<9} n={c['windows']:>3} BRG pass {c['BRG_pass_share']:.0%} SST pass {c['SST_pass_share']:.0%} "
                          f"best gain median {c['gain_median']:+.2%} max {c['gain_max']:+.2%}")
    return out


'''

MAIN_ADD = '''    print('[9c] JST replay (D1a) and the rho sensitivity (D1c)...')
    data['replay'] = _p7_replay(p, strategies)
    data['rho'] = {'base': p['rho'], 'sweep': p['rho_sens'],
                   'note': 'SST (state terminal stake) is the primary state test and does not depend on rho; SPT is the sensitivity',
                   'spt_by_rho': {k_: v_['spt_by_rho'] for k_, v_ in search.items()},
                   'verdict_spt_by_rho': {rule: verdict[rule]['SPT_by_rho'] for rule in rules}}
    for rule in vg['headline_rules']:
        if rule in verdict:
            print(f"  state tests, {rule}: SST (primary) {'pass' if verdict[rule]['SST'] else 'FAIL'}; SPT by rho " +
                  ', '.join(f"{k_}: {'pass' if v_ else 'FAIL'}" for k_, v_ in verdict[rule]['SPT_by_rho'].items()))
'''


def patch_valgen(t, problems):
    if '_p7_replay' in t:
        problems.append('valgen: already patched')
        return t
    t = plain(t, 'from wdt_fmt import out_dir, ensure_dir\n',
              'from wdt_fmt import out_dir, ensure_dir\nfrom wdt_jst import loop_windows, load_jst, real_return_series   # D1a / D1b\n', 'valgen import', problems)
    t = plain(t, 'def family3_pair(p: dict, alpha_C: float, alpha_D: float, g_series: list, G: int | None,',
              PV_HELPER + 'def family3_pair(p: dict, alpha_C: float, alpha_D: float, g_series: list, G: int | None,', 'valgen pv helper', problems)
    t = plain(t, "        'TW': a['family_true_T'], 'TW_honest': h['family_true_T'],\n",
              "        'pv_rel_by_rho': {str(r_): _pv_rel_at(p, h, a, r_) for r_ in (p.get('rho_sens') or [])},   # SPT sensitivity (D1c)\n"
              "        'TW': a['family_true_T'], 'TW_honest': h['family_true_T'],\n", 'valgen family3_pair rho', problems)
    t = plain(t, 'def _p5_search(p: dict, rule: str, lam: float, strategies: list) -> dict:',
              'def _p5_search(p: dict, rule: str, lam: float, strategies: list, ser: list | None = None) -> dict:', 'valgen _p5_search sig', problems)
    t = plain(t, "    vg  = p['val_gen']\n    ser = [p['g']] * vg['T']\n    tol = vg['state_tol']\n    o   = _p5_opts(p, rule, lam)\n",
              "    vg  = p['val_gen']\n    ser = list(ser) if ser is not None else [p['g']] * vg['T']     # a JST replay path, else constant real g\n"
              "    tol = vg['state_tol']\n    o   = _p5_opts(p, rule, lam)\n", 'valgen _p5_search ser', problems)
    t = plain(t, "                     'gain': m['gain'], 'pv_rel': m['pv_rel'], 'state_rel': m['state_rel']})",
              "                     'gain': m['gain'], 'pv_rel': m['pv_rel'], 'state_rel': m['state_rel'],\n"
              "                     'pv_rel_by_rho': m['pv_rel_by_rho']})", 'valgen recs', problems)
    t = plain(t, "    conf = [r_ for r_ in gaining if bad_pv(r_) or bad_st(r_)]\n",
              "    conf_any = [r_ for r_ in gaining if bad_pv(r_) or bad_st(r_)]\n"
              "    conf = list(conf_st)       # D1c: SST (discount-free) is the primary state test; n_conflict counts SST conflicts\n", 'valgen conf', problems)
    t = plain(t, "    conf.sort(key=lambda r_: -r_['gain'])\n",
              "    conf.sort(key=lambda r_: -r_['gain'])\n"
              "    spt_by_rho = {}\n"
              "    for rk_ in (p.get('rho_sens') or []):\n"
              "        bad_ = [x_ for x_ in gaining if x_['pv_rel_by_rho'].get(str(rk_)) is None or abs(x_['pv_rel_by_rho'][str(rk_)]) > tol]\n"
              "        spt_by_rho[str(rk_)] = {'n_conflict': len(bad_), 'pass': len(bad_) == 0}\n", 'valgen spt_by_rho', problems)
    t = plain(t, "'n_gaining': len(gaining), 'n_conflict': len(conf),",
              "'n_gaining': len(gaining), 'n_conflict': len(conf), 'n_conflict_any': len(conf_any),", 'valgen n_conflict', problems)
    t = plain(t, "'worst_conflicts': conf[:5], 'SPT_pass': len(conf_pv) == 0, 'SST_pass': len(conf_st) == 0,",
              "'worst_conflicts': conf[:5], 'SPT_pass': len(conf_pv) == 0, 'SST_pass': len(conf_st) == 0,\n"
              "            'spt_by_rho': spt_by_rho, 'state_test': 'SST',", 'valgen return', problems)
    t = plain(t, "'SPT': all(r_['SPT_pass'] for r_ in rs), 'SST': all(r_['SST_pass'] for r_ in rs),",
              "'SPT': all(r_['SPT_pass'] for r_ in rs), 'SST': all(r_['SST_pass'] for r_ in rs),\n"
              "                         'SPT_by_rho': {k_: all(r_['spt_by_rho'][k_]['pass'] for r_ in rs) for k_ in rs[0]['spt_by_rho']},",
              'valgen verdict', problems)
    t = plain(t, "    check('reset_rule_removes_overstatement_gain', g_allow > 0.03 and g_reset < 0.005,\n",
              "    check('reset_rule_removes_overstatement_gain', g_reset < 0.005 and g_reset <= g_allow + 1e-12,   # was g_allow > 3% (tuned to nominal growth)\n",
              'valgen relaxed check', problems)
    t = plain(t, "'val_basis': p.get('val_basis', 'legacy_nominal'),",
              "'val_basis': p.get('val_basis', 'legacy_nominal'), 'val_basis_info': p.get('val_basis_info'), 'rho_sens': p.get('rho_sens'),",
              'valgen meta', problems)
    t = plain(t, 'def _clean(obj):', REPLAY + 'def _clean(obj):', 'valgen replay def', problems)
    t = plain(t, "    data['p6'] = p6_out\n", "    data['p6'] = p6_out\n" + MAIN_ADD, 'valgen main', problems)
    return t


def main(argv):
    if not argv or argv[0].startswith('-'):
        raise SystemExit(__doc__)
    root = Path(argv[0])
    check = '--check' in argv
    vg = next((c for c in (root / 'VAL' / 'valgen_core.py', root / 'valgen_core.py') if c.exists()), None)
    paths = {'toml': root / 'WDT_Params.toml', 'core': root / 'wdt_core.py', 'jst': root / 'wdt_jst.py'}
    if vg is None:
        raise SystemExit(f'valgen_core.py not found under {root}')
    paths['valgen'] = vg
    for v in paths.values():
        if not v.exists():
            raise SystemExit(f'missing {v}')
    fns = {'toml': patch_toml, 'core': patch_core, 'jst': patch_jst, 'valgen': patch_valgen}
    new, problems = {}, []
    for k, path in paths.items():
        text, crlf = rd(path)
        new[k] = (fns[k](text, problems), crlf)
    if problems:
        print('NOTHING WRITTEN. Problems:')
        for pr in problems:
            print('  -', pr)
        raise SystemExit(1)
    print('All anchors found exactly once.')
    if check:
        print('--check: no files written.')
        return
    for k, path in paths.items():
        bak = path.with_name(path.name + '.pre_d2.bak')
        if not bak.exists():
            bak.write_bytes(path.read_bytes())
        wr(path, *new[k])
        print(f'patched {path}  (backup {bak.name})')
    print('Next: python wdt_jst.py   then   python -c "import wdt_core as w; p=w.load_params(); print(p[\'rho\'], p[\'rho_sens\'], w.with_val_basis(w.with_rate_scenario(p))[\'val_basis_info\'])"')
    print('      then rates_core.py --quick --stride 5 --countries GBR USA JPN   and   valgen_core.py --dry-run')


if __name__ == '__main__':
    main(sys.argv[1:])
