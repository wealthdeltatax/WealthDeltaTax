"""W2-04  D11 code: the legacy SSM and the retired TOML readers leave wdt_core / valgen_core.

Apply AFTER W2-03.  Apply W2-05 (TOML) straight after, in the same sitting: this patch makes the retired blocks
OPTIONAL-by-absence (load_params no longer reads them), so the TOML still loads either way.

 wdt_core.py
   - delete _ssm_marginals and _ssm_lrr_fill_year (and their section banner); load_params no longer runs the SSM
   - load_params no longer reads [swf] [budget] [returns] [tcm] [[tiers]] [[brackets]] [rate]; drops p['N_fill'], p['N'],
     p['tcm'], p['returns'], p['returns_meta'], p['rate'], p['tiers'], p['brackets'], p['hist_mean'], p['budget_*'], p['srr_ratio'], ...
   - p['g_real'] is NOT set by load_params any more: only with_val_basis sets it (jst | manual), so a nominal g cannot return
   - with_val_basis: basis = jst | manual only; no budget_growth fallback; sets q['sweep']['g_vals'] = g_real + [sweep].g_offsets
   - [val_gen] basis and rate_scenario are REQUIRED; manual needs g_real AND index_rate
   - [sweep]: *_canon, rates_*_sweep and wfr_* no longer parsed; g_vals becomes g_offsets (pp around g_real)
   - [synthetic_scenario] kept (mu now required in the TOML; no hist_mean default)
   - docstrings: N CONVENTION, _require_N text
 valgen_core.py
   - _ir(): p['index_rate'] only
   - _RETIRED_KEYS removed (nothing parses those keys any more)
 Tests: test_valgen_pairs.py (g from the output meta), rates_test.py (stale checks removed, load_jst call fixed).

Kept on purpose (D9 not built): simulate, run_pair, run_sim_hist, settle_tw_flows and relatives, run_sim, g_eff, synthetic_returns.
Numbers: valgen outputs unchanged EXCEPT the g_vals grid (recentred on g_real: the C.1-style growth grids move) and
meta no longer carries nothing new.  RATES: unchanged (it never read these keys).
"""
import re
from patchlib import Patch
P = Patch('W2-04', __doc__)
S = re.S | re.M
C = 'wdt_core.py'

# ---- delete the SSM block --------------------------------------------------------------------------------------------
P.regex(C, r"^# ─+\n# SHARED SSM MARGINAL REVENUE PASS\n# ─+\n\n.*?(?=^# ─+\n# VECTORISED RATE FUNCTION)", "", count=1, flags=S)

# ---- load_params ----------------------------------------------------------------------------------------------------
P.regex(C, r"    N keys \(see module docstring\):\n.*?    All monetary values in pounds m\.",
        "    N: p['N_val'] = [val] N_demo (30), the canonical taxpayer holding period. There is no SSM fill year any more (D11):\n"
        "    the fund fills inside each RATES window (fill_year in the RATES JSON).\n"
        "    p['g_real'] / p['index_rate'] are set by with_val_basis, not here.\n\n"
        "    All monetary values in pounds m.", count=1, flags=S)
P.regex(C, r"    if 'rate' in raw:  .*?\n    else:  [^\n]*\n(        _spec = rate_spec_from_scenario\(p, ''\)\n        p\['tau_0'\][^\n]*\n)",
        "    # D2/D11: the rate design is [rates.defaults]; [val_gen] rate_scenario picks the variant (with_rate_scenario)\n"
        r"    _spec = rate_spec_from_scenario(p, '')" "\n"
        "    p['tau_0'], p['tau_m'], p['k'], p['W_min'] = _spec['tau_0'], _spec['tau_m'], _spec['k'], _spec['W_min']\n",
        count=1, flags=S)
P.regex(C, r"    p\['srr_ratio'\] = float\(raw\['swf'\]\['srr_ratio'\]\).*?        for b in raw\['brackets'\]\n    \]\n\n", "", count=1, flags=S)
P.regex(C, r"    p\['g_real'\] = p\['hist_mean'\][^\n]*\n(    p\['alpha'\] = 1\.0\n    p\['beta'\]  = 0\.0\n)\n    lrr_N = .*?p\['N'\]      = lrr_N[^\n]*\n",
        r"\1", count=1, flags=S)

# [sweep]
P.regex(C, r"        'tau_0_canon':.*?        'g_canon':[^\n]*\n", "", count=1, flags=S)
P.replace(C, "        'g_vals':            [float(v) for v in sw.get('g_vals',        [])],\n",
          "        'g_offsets':         [float(v) for v in sw.get('g_offsets',     [])],   # pp around g_real\n"
          "        'g_vals':            [],                                                # filled by with_val_basis: g_real + g_offsets\n")
P.regex(C, r"        'rates_tau_0_sweep':.*?        'rates_g_sweep':[^\n]*\n", "", count=1, flags=S)
P.regex(C, r"    if p\['sweep'\]\['N_canon'\] != p\['N_val'\]:\n.*?canonical N = 30\)\.\"\)\n\n", "", count=1, flags=S)
P.replace(C, "        'mu':              float(syn.get('mu',              p['hist_mean'])),\n",
          "        'mu':              float(syn['mu']),\n")
P.regex(C, r"    # ── WFR sweep keys \(welfare model\).*?    \}\)\n\n    # ── Structured sub-dicts.*?        'values':           canonical,     # raw list, unrotated\n    \}\n\n", "", count=1, flags=S)

# with_val_basis
P.regex(C, r"def with_val_basis\(p, J=None\):\n.*?    return q\n",
'''def with_val_basis(p, J=None):
    """
    Copy of p on the REAL basis VAL runs in, per [val_gen] basis (D11: the nominal 'legacy' basis is gone):
      'jst'     g_real and index_rate derived from JST (jst_basis)
      'manual'  [val_gen] g_real (REAL return) and index_rate (REAL GDP/head growth), both required
    Sets p['g_real'], p['index_rate'], p['val_basis'] = 'real', p['val_basis_info'], and p['sweep']['g_vals'] = g_real + [sweep].g_offsets.
    """
    vg = p['val_gen']
    q = dict(p)
    basis = vg.get('basis')
    if basis == 'jst':
        info = jst_basis(p, J)
        g_real, idx = info['g_real'], info['index_rate']
    elif basis == 'manual':
        info = {'source': 'manual'}
        g_real, idx = float(vg['g_real']), float(vg['index_rate'])
    else:
        raise ValueError(f"[val_gen] basis must be jst | manual, got {basis!r}")
    q['g_real'] = g_real
    q['index_rate'] = idx
    q['val_basis'] = 'real'
    q['val_basis_info'] = info
    q['sweep'] = dict(p['sweep'], g_vals=[g_real + o for o in p['sweep']['g_offsets']])
    return q
''', count=1, flags=S)

# [val_gen] validation
P.replace(C, "'basis': str(vg.get('basis', 'manual' if 'g_real' in vg else 'legacy')),", "'basis': str(vg.get('basis', '')),")
P.regex(C, r"    if _b not in \('jst', 'manual', 'legacy'\):\n.*?needs g_real \(and index_rate\)'\)\n",
'''    if _b not in ('jst', 'manual'):
        raise ValueError(f"[val_gen] basis must be jst | manual, got {_b!r}")
    if _b == 'manual' and (p['val_gen']['g_real'] is None or p['val_gen']['index_rate'] is None):
        raise ValueError('[val_gen] basis = "manual" needs g_real AND index_rate')
    if not p['val_gen']['rate_scenario']:
        raise ValueError('[val_gen] rate_scenario is required (a [rates.scenarios.*] name; baseline "gain_ladder")')
''', count=1, flags=S)

# docstrings
P.regex(C, r"N CONVENTION  \(refactor: N is never implicit\)\n-+\nThere are two different N's:\n.*?RAISE if N is not passed\. Before the refactor they defaulted to p\['N'\] \(=N_fill\),\nso any table that did not pass N explicitly silently ran at N = 19 while its\ncaption said N = 30\.",
        "N CONVENTION  (N is never implicit)\n-----------------------------------\n"
        "p['N_val'] = [val] N_demo = 30 is the canonical taxpayer holding period. The SSM fill year (N_fill) is retired with D11.\n"
        "run_sim, run_sim_hist, decompose_tw_advantage, run_pair and npv_tax_advantage RAISE if N is not passed.", count=1, flags=S)
P.regex(C, r"            \"Use p\['N_val'\] \(=30, canonical taxpayer holding period\) for VAL \"\n.*?not the canonical N = 30\.\"\n",
        "            \"Use p['N_val'] (=30, the canonical taxpayer holding period).\"\n", count=1, flags=S)

# ---- valgen_core ----------------------------------------------------------------------------------------------------
V = 'valgen_core.py'
P.replace(V, '''    """W_min / k index rate: p['index_rate'] (set by wdt_core.with_val_basis) else the legacy [budget] budget_growth."""
    return p.get('index_rate', p['budget_growth'])''',
'''    """W_min / k index rate: p['index_rate'], set by wdt_core.with_val_basis (required since D11)."""
    return p['index_rate']''')
P.regex(V, r"^_RETIRED_KEYS = [^\n]*\n\n\n", "", count=1)
P.replace(V, "**{k: v for k, v in vg.items() if k not in _RETIRED_KEYS}},", "**vg},")

# ---- tests ----------------------------------------------------------------------------------------------------------
P.replace('test_valgen_pairs.py', "DATA = TABLES.load_data()\n",
          "DATA = TABLES.load_data()\nP['g_real'] = DATA['meta']['params']['g']     # D11: load_params carries no g; the real return VAL ran on is in the output\n")
R = 'rates_test.py'
P.replace(R, "J = rc.load_jst(p['rates'])", "J = rc.load_jst(p['rates']['jst_path'])")
P.regex(R, r"^def test_valgen_equivalence\(p, J\):\n.*?(?=^# ═+\n# pipeline, registries)", "", count=1, flags=S)
P.replace(R, "    test_valgen_equivalence(p, J)\n", "    # valgen equivalence is now bridge_test.py (kernel vs run_family3 vs run_lines)\n")
P.regex(R, r"^def test_series\(J\):\n.*?(?=^def test_legacy_csv)", "", count=1, flags=S)
P.replace(R, "    if a.data:\n        if J is None:\n            skip('data checks', 'JST file not found')\n        else:\n            test_series(J)\n",
          "    if a.data and J is None:\n        skip('data checks', 'JST file not found')\n")
P.run()
