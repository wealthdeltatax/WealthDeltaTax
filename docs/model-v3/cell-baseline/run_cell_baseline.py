"""Brief 110c: untaxed cell baseline. Block 1: python -I docs/model-v3/cell-baseline/run_cell_baseline.py units  (summary lines on screen, table to CSV)."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from model_v3.core import pack as pk                       # noqa: E402
from model_v3.runner import cell_baseline as cb            # noqa: E402

FLOWS = ROOT / 'docs' / 'research' / 'data' / '101r' / 'derived_ons_flows.csv'
OUT = Path(__file__).resolve().parent


def ons(item, year):
    with open(FLOWS, encoding='utf-8') as fh:
        (v,) = [float(r['value']) for r in csv.DictReader(fh) if r['item'] == item and r['year'] == str(year)]
    return v


def units():
    pack, reg = pk.load_pack(ROOT / 'model_v3' / 'pack' / 'GBR'), pk.load_register(ROOT / 'registry' / 'inputs.json')
    b6g, d8 = ons('B6g_gdhi', 2025) / 1e3, ons('D8_pension_adj', 2025) / 1e3
    rows = []
    for f in (0.4, 0.6, 0.8):
        cells = cb.build_cells(pack, reg, retired_fraction=f)
        r = cb.reconcile(cells, pack, b6g, d8)
        rows.append(dict(retired_fraction=f, **{k: round(v, 4) for k, v in r.items()}))
        print(f"f={f}: wealth {r['wealth_cells']:.1f} vs pack {r['wealth_pack_all']:.1f} ({r['wealth_gap_pct']:+.2f}%); wealth/GDP {r['wealth_over_gdp']:.3f} "
              f"vs {r['pack_wealth_over_gdp']:.3f}; income {r['income_cells']:.1f} vs B6g {b6g:.1f} ({r['income_gap_pct']:+.1f}%), vs B6g+D8 {b6g + d8:.1f} ({r['income_gap_incl_d8_pct']:+.1f}%)")
    with open(OUT / 'units.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, list(rows[0])); w.writeheader(); w.writerows(rows)
    cells = cb.build_cells(pack, reg)
    with open(OUT / 'cells.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh); w.writerow(['cell', 'persons', 'households_k', 'wealth_bn', *cb.CLASSES, 'income_bn', 'income_per_hh', 'wealth_per_hh', 'wealth_per_person'])
        for c in cells:
            w.writerow([c['cell'], c['persons'], round(c['households_k'], 3), round(c['wealth'], 3), *[round(c['pos'][k], 3) for k in cb.CLASSES],
                        round(c['income'], 3), round(c['income_per_hh']), round(c['wealth_per_hh']), round(c['wealth_per_person'])])
    print('saving ratio 1998-2025: see block 2; per-household income and wealth in cells.csv')


if __name__ == '__main__':
    units() if sys.argv[1:] == ['units'] else sys.exit('usage: run_cell_baseline.py units')
