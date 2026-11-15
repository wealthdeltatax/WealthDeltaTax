"""W2-02  HLC burdens come from a TOML-held calibration, not from rates_data.json.

  WDT_Params.toml   new [val_gen.hlc]  (average_stock_rate, top_stock_rate, source_scenario, stamp, placeholder)
                    Shipped as a PLACEHOLDER (placeholder = true, rates 0.0): valgen SKIPS the HLC pair, loudly,
                    until you run  print_hlc_calibration.py --write  after a RATES run.
  wdt_core.py       load_params parses [val_gen.hlc] -> p['val_gen']['hlc'] (None when absent)
  valgen_core.py    _rates_burdens reads p['val_gen']['hlc']; valgen no longer touches rates_data.json.
                    Definition now matches D1d: average = wealth-weighted rate over all NET PAYERS (er_stock_payers),
                    top = top 0.1% (er_stock_top0.1)  [was: richest wealth BAND].

Numbers: HLC pair moves (new definition, and absent until calibrated).  Nothing else moves.
"""
from patchlib import Patch
P = Patch('W2-02', __doc__)

P.replace('WDT_Params.toml',
"[val_gen.route_shares]    # D13 baseline",
"""# HLC pair (D1d): the conventional self-declared tax at the burden RATES finds for (a) the average net payer and (b) the top 0.1%.
# One calibration, held HERE: valgen never reads rates_data.json. Regenerate with  python test/print_hlc_calibration.py --write
# after any RATES run (er_stock_payers / er_stock_top0.1 medians, all windows, of [rates.figures] scenario/mode).
# placeholder = true  =>  valgen skips the HLC pair and says why.  The 0.0 rates below are NOT calibrated values.
[val_gen.hlc]
placeholder         = true
average_stock_rate  = 0.0     # PLACEHOLDER  annual WDT / wealth, wealth-weighted over net payers
top_stock_rate      = 0.0     # PLACEHOLDER  annual WDT / wealth, top 0.1%
source_scenario     = ""
stamp               = ""

[val_gen.route_shares]    # D13 baseline""")

P.replace('wdt_core.py',
"""        'basis_years': ([int(x) for x in vg['basis_years']] if 'basis_years' in vg else None),""",
"""        'basis_years': ([int(x) for x in vg['basis_years']] if 'basis_years' in vg else None),
        'hlc': ({'average_stock_rate': float(vg['hlc']['average_stock_rate']), 'top_stock_rate': float(vg['hlc']['top_stock_rate']),
                 'source_scenario': str(vg['hlc'].get('source_scenario', '')), 'stamp': str(vg['hlc'].get('stamp', '')),
                 'placeholder': bool(vg['hlc'].get('placeholder', False))} if 'hlc' in vg else None),""")

NEW_BURDENS = '''def _rates_burdens(p: dict) -> dict:
    """
    HLC burdens (D1d) from the TOML-held calibration [val_gen.hlc]; valgen reads no RATES output.
    average = wealth-weighted annual WDT / wealth over net payers; top = top 0.1%.  Regenerate with test/print_hlc_calibration.py.
    Returns {'ok': False, 'reason': ...} when the block is absent or still a PLACEHOLDER.
    """
    h = p['val_gen'].get('hlc')
    if not h:
        return {'ok': False, 'reason': '[val_gen.hlc] absent from the TOML'}
    if h['placeholder']:
        return {'ok': False, 'reason': '[val_gen.hlc] is a PLACEHOLDER; run RATES, then test/print_hlc_calibration.py --write'}
    return {'ok': True, 'scenario': h['source_scenario'], 'stamp': h['stamp'], 'average': h['average_stock_rate'],
            'top': h['top_stock_rate'], 'by_band': None, 'wealth_share': None}


'''
P.regex('valgen_core.py', r'def _rates_burdens\(p: dict\) -> dict:\n.*?\n(?=def _hlc_pair)', NEW_BURDENS.replace('\\', '\\\\'),
        count=1, flags=__import__('re').S)
P.replace('valgen_core.py',
"""    out = {'skipped': False, 'source': {'scenario': b['scenario'], 'by_band': b['by_band'], 'wealth_share': b['wealth_share']},""",
"""    out = {'skipped': False, 'source': {'scenario': b['scenario'], 'stamp': b['stamp'], 'by_band': b['by_band'], 'wealth_share': b['wealth_share'],
                                        'definition': 'average = net payers, wealth-weighted; top = top 0.1% (D1d); from [val_gen.hlc]'},""")
P.replace('valgen_core.py',
"""    Skipped, with the reason, when the RATES JSON is not there. Burden = annual rate on declared value, equal to the stock rate.\"\"\"""",
"""    Skipped, with the reason, while [val_gen.hlc] is absent or a PLACEHOLDER. Burden = annual rate on declared value, equal to the stock rate.\"\"\"""")
P.replace('valgen_core.py',
"""HLC pair (RATES burdens read via
wdt_core.load_json; skipped, with the reason, if rates_data.json is absent).""",
"""HLC pair (burdens from the
TOML-held calibration [val_gen.hlc]; skipped, with the reason, while it is a PLACEHOLDER).""")
P.run()
