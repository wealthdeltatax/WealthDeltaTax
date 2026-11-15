"""print_hlc_calibration.py -- print (or --write) the [val_gen.hlc] block from a finished RATES run.

    python test/print_hlc_calibration.py            # print the block
    python test/print_hlc_calibration.py --write    # replace the block in WDT_Params.toml (CRLF kept)

Reads rates_data.json (found under the Model root) and [rates.figures] scenario/mode from the TOML.
Values: medians over ALL windows of er_stock_payers and er_stock_top0.1 of that scenario (D1d).
This is a calibration TOOL, not part of the model: valgen/rates cores never import it.
"""
import argparse, glob, json, os, re, sys
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def find(name):
    h = [p for p in glob.glob(os.path.join(ROOT, '**', name), recursive=True) if '.bak' not in p and '/test/' not in p.replace('\\', '/')]
    if len(h) != 1:
        raise SystemExit(f'expected one {name} under {ROOT}, found {h}')
    return h[0]

def calibration(toml_path, json_path):
    t = tomllib.load(open(toml_path, 'rb'))
    fg = t['rates']['figures']
    name, mode = fg['scenario'], fg['mode']
    d = json.load(open(json_path))
    sc = (d.get('scenarios') or d)[name]
    hl = sc['headline']
    h = hl.get(mode) or next(iter(hl.values()))
    med = h['overall'].get('medians_all') or h['overall']['medians']
    avg, top = med.get('er_stock_payers'), med.get('er_stock_top0.1')
    if avg is None or top is None:
        raise SystemExit(f"medians lack er_stock_payers / er_stock_top0.1 for scenario {name!r} (have: {sorted(k for k in med if k.startswith('er_stock'))})")
    stamp = (d.get('meta') or {}).get('generated', '') + '/' + (d.get('meta') or {}).get('params_hash', '')
    return {'average': float(avg), 'top': float(top), 'scenario': name, 'mode': mode, 'stamp': stamp}

def block(c):
    return ('[val_gen.hlc]\n'
            'placeholder         = false\n'
            f"average_stock_rate  = {c['average']:.6f}     # net payers, wealth-weighted (er_stock_payers, all windows)\n"
            f"top_stock_rate      = {c['top']:.6f}     # top 0.1% (er_stock_top0.1, all windows)\n"
            f"source_scenario     = \"{c['scenario']}\"\n"
            f"stamp               = \"{c['stamp']}\"\n")

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--write', action='store_true')
    a = ap.parse_args()
    tp, jp = find('WDT_Params.toml'), find('rates_data.json')
    b = block(calibration(tp, jp))
    print(b)
    if a.write:
        raw = open(tp, 'rb').read().decode('utf-8'); crlf = '\r\n' in raw; t = raw.replace('\r\n', '\n')
        pat = re.compile(r'^\[val_gen\.hlc\]\n(?:(?!\[).*\n)*', re.M)
        if len(pat.findall(t)) != 1:
            raise SystemExit('[val_gen.hlc] block not found exactly once; apply patch W2-02 first')
        t = pat.sub(lambda m: b + '\n', t, count=1)
        open(tp, 'wb').write((t.replace('\n', '\r\n') if crlf else t).encode('utf-8'))
        print('written', tp)
