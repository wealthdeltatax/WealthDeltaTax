"""W2-03  p['g'] -> p['g_real']  (the real capital return VAL runs on).

  wdt_core.py     with_val_basis: q['g_real'] = g_real ; run_sim default g ; load_params legacy default ; docstrings
  valgen_core.py  every parameter-dict read/write p['g'], pg['g'] (28) ; PLAN_S1_BASELINE key ; _plan_fixture_applies key
  tests           bridge_test, kernel_test, test_valgen_pairs

NOT renamed (deliberately): JSON OUTPUT keys 'g' (meta.params, pairs_at_N_val, p2b/p3 grids ...) that downstream tables read;
the example-spec keys spec['g'] / L['g'] / M['g']; the marginals record 'g': g_sell; the `g` argument names; [val_gen] g_real in the TOML.

Numbers: NEUTRAL (rename only).  Prove it with  python test/diff_json.py before.json after.json  on valgen_data.json.
"""
import re
from patchlib import Patch
P = Patch('W2-03', __doc__)

# wdt_core
P.replace('wdt_core.py', "        q['g'] = g_real\n", "        q['g_real'] = g_real\n")
P.replace('wdt_core.py', "else p_in['g']", "else p_in['g_real']")
P.replace('wdt_core.py', "    p['g']     = p['hist_mean']\n", "    p['g_real'] = p['hist_mean']     # legacy default; with_val_basis replaces it with the JST / manual real return\n")
P.replace('wdt_core.py', "p['g'] becomes the real return", "p['g_real'] becomes the real return")
P.replace('wdt_core.py', "replaces p['g']; index_rate", "replaces p['g_real']; index_rate")

# valgen_core
P.regex('valgen_core.py', r"(?<![\w])(p|pg)\['g'\]", r"\1['g_real']", count=28)
P.replace('valgen_core.py', "'V0_m': 20.0, 'g': 0.1045}", "'V0_m': 20.0, 'g_real': 0.1045}")
P.replace('valgen_core.py', "_plan_fixture_applies(p, ('tau_0', 'g'))", "_plan_fixture_applies(p, ('tau_0', 'g_real'))")

# tests
P.replace('bridge_test.py', "ser = [p['g']] * T", "ser = [p['g_real']] * T", count=2)
P.replace('bridge_test.py', "np.full(T, p['g'])", "np.full(T, p['g_real'])")
P.replace('kernel_test.py', "vg['G'], p['g']", "vg['G'], p['g_real']")
P.replace('test_valgen_pairs.py', "P['rho'], P['g'],", "P['rho'], P['g_real'],")
P.run()
