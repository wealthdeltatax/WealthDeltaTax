"""W2-01  rates_core fixes: missing RATES columns, quick-run coverage, per-scenario plan cache, docstring.

 1. rel_cov_never_share  (T27)  share of uncensored windows in which relief never covers expenditure
                                (rel_cov_year is NaN).  Written as a direct key of every group block
                                and into overall['medians'] / ['medians_all'] (as a share, not a median).
 2. income_short_share_band{i} (T30)  Route B income mode: share of the band's assessment met by SALE
                                (the shortfall) = sold / (sold + gross income paid), over the window.
 3. figure_scenarios()  now includes [rates.figures].route_b and the gl_arch_* scenarios from [rates.run].scenarios.
 4. _route_plan / _verification are built once per scenario (cached in cal), not once per window.
 5. module docstring: kernel engine, Route B, loop windows.
 6. bridge_test.py: rates_line() builds a per-line `plan` and the signature guard expects (plan, ver); the old
    `rb=` call made the B-vs-valgen parity test SKIP.

Numbers: NO existing number moves.  New JSON keys only; --quick now runs more scenarios.
"""
from patchlib import Patch
P = Patch('W2-01', __doc__)
F = 'rates_core.py'

# 1a  group block: direct key
P.replace(F,
"""        'exp_gdp_mean': float(g['exp_gdp_mean'].mean()) if len(g) else None,
        'stable': {'windows': int(len(stable)),""",
"""        'exp_gdp_mean': float(g['exp_gdp_mean'].mean()) if len(g) else None,
        'rel_cov_never_share': (float(ok['rel_cov_year'].isna().mean())
                                if len(ok) and 'rel_cov_year' in ok else None),
        'stable': {'windows': int(len(stable)),""")

# 1b  medians dicts carry the share too (tables read overall['medians'][col])
P.replace(F,
"""    for q_, key_ in ((0.10, 'p10'), (0.90, 'p90')):
        overall[key_] = {c: (None if np.isnan(v) else float(v)) for c, v in num.quantile(q_).items()}
""",
"""    for q_, key_ in ((0.10, 'p10'), (0.90, 'p90')):
        overall[key_] = {c: (None if np.isnan(v) else float(v)) for c, v in num.quantile(q_).items()}
    if 'rel_cov_year' in g:                  # W2-01: a SHARE of windows (not a median), kept beside the medians the tables read
        overall['medians']['rel_cov_never_share'] = overall['rel_cov_never_share']
        overall['medians_all']['rel_cov_never_share'] = (float(g['rel_cov_year'].isna().mean()) if len(g) else None)
""")

# 2  income short share by launch-wealth band
P.replace(F,
"""    for i_, v_ in enumerate(np.bincount(cal['band_id'], weights=out['income_b_gdp'].sum(axis=0), minlength=nbd_)):
        rextra[f'income_cum_gdp_band{i_}'] = float(v_)
""",
"""    for i_, v_ in enumerate(np.bincount(cal['band_id'], weights=out['income_b_gdp'].sum(axis=0), minlength=nbd_)):
        rextra[f'income_cum_gdp_band{i_}'] = float(v_)
    # W2-01: Route B income mode, share of the assessment met by SALE (the shortfall) = sold / (sold + gross income paid)
    sold_ = np.bincount(cal['band_id'], weights=out['lvl']['b_sold_b'].sum(axis=0), minlength=nbd_)
    paid_ = np.bincount(cal['band_id'], weights=out['lvl']['income_gross_b'].sum(axis=0), minlength=nbd_)
    for i_ in range(nbd_):
        den_ = sold_[i_] + paid_[i_]
        rextra[f'income_short_share_band{i_}'] = float(sold_[i_] / den_) if den_ > 1e-15 else np.nan
""")

# 3  figure_scenarios
P.replace(F,
"""    for key in ('decomposition', 'rate_grid', 'schedules', 'cohorts', 'scope', 'stack', 'headline', 'consumption', 'levy'):
        names += fg[key]
    names += p['rates']['representativeness']['bootstrap_scenarios']
""",
"""    for key in ('decomposition', 'rate_grid', 'schedules', 'cohorts', 'scope', 'stack', 'headline', 'consumption', 'levy'):
        names += fg[key]
    names += fg.get('route_b', [])                                                    # W2-01: T22b / T30 inputs
    names += [n for n in p['rates']['run']['scenarios'] if n.startswith('gl_arch_')]    # W2-01: archetype sweep (T27, F27)
    names += p['rates']['representativeness']['bootstrap_scenarios']
""")

# 4  plan cache: helper + the call site in run_window
P.replace(F,
"""def run_cohorts(scn, cal, tiers=None, n_phase=6, G=30, deaths=True,""",
"""def _plan_ver(cfg, cal, p):
    \"\"\"(_route_plan(...)['cell'], _verification(...)) built once per scenario: cached in `cal` (one cal per scenario).\"\"\"
    pv = cal.get('_plan_ver')
    if pv is None:
        pv = cal['_plan_ver'] = (_route_plan(cfg, cal, p)['cell'], _verification(cfg, p))
    return pv


def run_cohorts(scn, cal, tiers=None, n_phase=6, G=30, deaths=True,""")
P.replace(F,
"""                      plan_cell=_route_plan(cfg, cal, p)['cell'], ver=_verification(cfg, p))""",
"""                      plan_cell=_plan_ver(cfg, cal, p)[0], ver=_plan_ver(cfg, cal, p)[1])""")

# 5  docstring
P.replace(F,
"""  L3  engine     honest-declaration WDT mechanics, vectorised across lines; aggregation""",
"""  L3  engine     honest-declaration WDT mechanics, vectorised across lines; aggregation.
                 Settlement runs through wdt_kernel (routes A/B/C/D; Route B sale | lien | income;
                 C caps; lambda_C / lambda_D; death verification), driven by _route_plan / _verification.
                 step_death has no line mask: run_lines cuts sub-books (_sub_book) and writes them back.
                 Windows are JST LOOP windows (wdt_jst.loop_windows, T = 100; `contiguous` marks the
                 second report).""")
# 6  bridge_test.py follows the S2 run_lines signature (plan / ver, not rb): without this the B-vs-valgen parity test SKIPS
P.replace('bridge_test.py',
"""    rb = None if mode == 'sale' else {'mode': mode, 'r_def': p['route_b']['r_def'], 'cap': inc['cap'],
                                      'bshare': np.array([bshare]), 'income': np.array([ratio])}""",
"""    plan = None if mode == 'sale' else {'shares': {'B': np.array([float(bshare)]), 'C': np.array([1.0 - float(bshare)])},
                                        'mode': mode, 'r_def': p['route_b']['r_def'], 'cap': inc['cap'],
                                        'income': np.array([ratio])}""")
P.replace('bridge_test.py', "heir_rule='delta', c_cap=rule_cap, rb=rb)", "heir_rule='delta', c_cap=rule_cap, plan=plan)")
P.replace('bridge_test.py',
"want = ['g', 'idx', 'V0', 'w', 'group', 'nb', 'ph', 'G', 'c', 'rp', 'heir_rule', 'c_cap', 'rb']",
"want = ['g', 'idx', 'V0', 'w', 'group', 'nb', 'ph', 'G', 'c', 'rp', 'heir_rule', 'c_cap', 'plan', 'ver']")
P.run()
