"""W2-06  Presentation follows W2-02 (HLC calibration in the TOML) and the real RATES JSON contract.

 5_6_VALGEN_tables.py   HLP: caption says the burdens are the [val_gen.hlc] calibration (payers / top 0.1%, scenario and stamp);
                        the "not built" note points at print_hlc_calibration.py
 5_7_VALGEN_charts.py   HLP footnote likewise
 8_2_RATES_tables.py    docstring: the stale data['archetype_sweep'] / income_paid_cum_gdp contract replaced by what rates_core writes
                        (gl_arch_* scenario blocks; income_cum_gdp, income_cum_gdp_band{i}, income_short_share_band{i},
                        overall.rel_cov_never_share)
 Reading code is unchanged: T27 / T30 already read the keys W2-01 now writes.

Numbers: neutral (text only).  Not touched: 8_3_RATES_charts.py (not provided; it duplicates _hl, _med, _need, _route_b_names,
_default_of_mode, _rb_label with 8_2 -- move them to one module when 8_3 is next opened).
"""
from patchlib import Patch
P = Patch('W2-06', __doc__)

P.replace('5_6_VALGEN_tables.py',
"""        return _not_built('HLP', (why or 'the RATES JSON was not available when valgen_core ran') + '. Run rates_core.py, then valgen_core.py.')""",
"""        return _not_built('HLP', (why or '[val_gen.hlc] is not calibrated') + '. Then re-run valgen_core.py.')""")
P.replace('5_6_VALGEN_tables.py',
"""f"burden the WDT puts on the average payer ({fmt_pct(avg['rate'], 3)}) and on the top payer ({fmt_pct(top['rate'], 3)}), against the "
           f"WDT best response under {cand}. Burdens are the wealth-weighted stock rates of RATES scenario {src['scenario']}, read from "
           f"the RATES JSON. Conventional: no audits modelled.""",
"""f"burden the WDT puts on the average net payer ({fmt_pct(avg['rate'], 3)}, wealth-weighted) and on the top 0.1% ({fmt_pct(top['rate'], 3)}), against the "
           f"WDT best response under {cand}. Burdens are the stock rates held in [val_gen.hlc], calibrated from RATES scenario {src['scenario']} "
           f"({src.get('stamp') or 'no stamp'}). Conventional: no audits modelled.""")
P.replace('5_7_VALGEN_charts.py',
"'Burden = wealth-weighted stock rate from the RATES JSON. Conventional tax",
"'Burden = stock rate held in [val_gen.hlc] (RATES: net payers, top 0.1%). Conventional tax")
P.regex('8_2_RATES_tables.py',
r"  data\['archetype_sweep'\] = \{.*?  headline\.overall\['rel_cov_never_share'\][^\n]*\n",
"""  Table 31 reads the gl_arch_* scenario blocks rates_core writes (one block per route-mix scenario; there is no data['archetype_sweep']):
      block['routes']                     A/B/C/D shares by launch-wealth band, mix, Route B mode (_route_plan diag)
      headline[mode].overall.medians_all  cov_ref, er_stock_*, er_gain_*, fill_year, income_cum_gdp, dsettle_gdp_mean, ...
      headline[mode].overall.censored_share  share of windows whose fund never fills
      income_cum_gdp: cumulative external income paid to WDT over the window, in years of GDP.
  Route B scenarios, per launch-wealth band i (all-window medians, as the other *_band{i} columns):
      income_cum_gdp_band{i}        cumulative income paid over the window, in years of GDP
      income_short_share_band{i}    share of the assessment met by SALE: sold / (sold + gross income paid)      (W2-01)
  headline[mode].overall['rel_cov_never_share']   share of uncensored (filling) windows in which relief never reaches expenditure (W2-01)
""", count=1, flags=__import__('re').S)
P.run()
