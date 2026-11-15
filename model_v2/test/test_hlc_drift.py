"""test_hlc_drift.py -- WARNS when [val_gen.hlc] has drifted from rates_data.json (or is still a PLACEHOLDER).
Exit 0 on warnings; --strict makes warnings fail."""
import glob, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import print_hlc_calibration as ph
strict = '--strict' in sys.argv
tp = ph.find('WDT_Params.toml')
h = ph.tomllib.load(open(tp, 'rb'))['val_gen'].get('hlc')
warn = []
if h is None: warn.append('[val_gen.hlc] absent (apply W2-02)')
elif h.get('placeholder'): warn.append('[val_gen.hlc] is a PLACEHOLDER: HLC pair is skipped by valgen')
else:
    jp = glob.glob(os.path.join(ph.ROOT, '**', 'rates_data.json'), recursive=True)
    if not jp: warn.append('no rates_data.json to compare against')
    else:
        c = ph.calibration(tp, jp[0])
        for k, kk in (('average', 'average_stock_rate'), ('top', 'top_stock_rate')):
            if abs(c[k] - h[kk]) > 5e-6:
                warn.append(f'{kk}: TOML {h[kk]:.6f} vs RATES {c[k]:.6f}  (run print_hlc_calibration.py --write)')
        if c['scenario'] != h['source_scenario']: warn.append(f"source_scenario {h['source_scenario']!r} vs [rates.figures] {c['scenario']!r}")
for w in warn: print('WARN', w)
if not warn: print('PASS [val_gen.hlc] matches rates_data.json')
sys.exit(1 if (warn and strict) else 0)
