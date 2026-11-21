"""Brief 110c: untaxed cell baseline. Block 1: python -I docs/model-v3/cell-baseline/run_cell_baseline.py units | run  (summary lines on screen, tables to CSV)."""
from __future__ import annotations

import csv
import statistics
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from model_v3.core import pack as pk                       # noqa: E402
from model_v3.core import returns as rt, revenue as rv    # noqa: E402
from model_v3.runner import cell_baseline as cb            # noqa: E402

FLOWS = ROOT / 'docs' / 'research' / 'data' / '101r' / 'derived_ons_flows.csv'
OUT = Path(__file__).resolve().parent
JST = ROOT / 'docs' / 'research' / 'data' / '101r' / 'jst_split_stats.csv'
B6G_YEAR = 2024   # I-D9 is at the FYE 2024 level; B.6g 2024 is the nearest calendar year
YEARS = (0, 10, 50, 100)


def ons_value(item, year):
    with open(FLOWS, encoding='utf-8') as fh:
        (v,) = [float(r['value']) for r in csv.DictReader(fh) if r['item'] == item and r['year'] == str(year)]
    return v


def units():
    pack, reg = pk.load_pack(ROOT / 'model_v3' / 'pack' / 'GBR'), pk.load_register(ROOT / 'registry' / 'inputs.json')
    b6g, d8 = ons_value('B6g_gdhi', 2025) / 1e3, ons_value('D8_pension_adj', 2025) / 1e3
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



def jst(period, item):
    with open(JST, encoding='utf-8') as fh:
        (v,) = [float(r['mean_or_value']) for r in csv.DictReader(fh) if r['period_or_check'] == period and r['item'] == item]
    return v / 100


def scenario(pack, reg, regime='mid', saving='median'):
    """regime low = 1947-79, high = 1980-2019, mid = the mid-point label (mean of the two); saving min, median or max of the ONS series 1998-2025."""
    ser = [ons_value('saving_ratio_pct', y) / 100 for y in range(1998, 2026)]
    pick = lambda low, high: dict(low=low, high=high, mid=(low + high) / 2)[regime]
    pg = pick(jst('1947_1979', 'housing_g_real'), jst('1980_2019', 'housing_g_real'))
    py = pick(jst('1947_1979', 'housing_y_real'), jst('1980_2019', 'housing_y_real'))
    rp, rf = (dict(low=reg[i].low, mid=reg[i].central, high=reg[i].high)[regime] / 100 for i in ('I-D1h', 'I-D1i'))
    pen = dict(low=reg['I-D1k'].low, mid=reg['I-D1k'].central, high=reg['I-D1k'].high)[regime] / 100
    gdp_g = float(np.mean(rv.gdp_growth(pack, rt.real_series(pack)[0])))
    return dict(arm='new', s=dict(min=min(ser), median=statistics.median(ser), max=max(ser))[saving], gdp_g=gdp_g, pen=pen, r=reg['I-D1a'].central / 100,
                c=reg['I-D14c'].central / 100, g=dict(property=pg, financial=rf, physical=reg['I-D1j'].central / 100, pension=rp), y=dict(property=py))


def write(name, rows):
    with open(OUT / name, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, list(rows[0])); w.writeheader(); w.writerows([{k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()} for r in rows])


def one(label, cells, sc, gdp0):
    rows = cb.run_cells(cells, sc, 100)
    agg = cb.aggregate(rows, range(101), gdp0, sc['gdp_g'])
    write(f'run_{label}_cells.csv', rows); write(f'run_{label}_aggregate.csv', agg)
    for a in (x for x in agg if x['year'] in YEARS):
        print(f"{label} y{a['year']:>3}: wealth {a['wealth']:.0f}bn, W/GDP index {a['wealth_over_gdp_index']:.3f}, saving ratio {a['saving_ratio']:.4f}, "
              f"top-band share {a['share_D10']:.3f}, residual {a['resid']:.1e}")
    return rows, agg


def run():
    pack, reg = pk.load_pack(ROOT / 'model_v3' / 'pack' / 'GBR'), pk.load_register(ROOT / 'registry' / 'inputs.json')
    gdp0 = pk.lookup(pack, 'wealth_distribution', variable='gdp', band='all')[0]['value']
    raw = cb.build_cells(pack, reg)
    scaled = cb.scale_income(raw, ons_value('B6g_gdhi', B6G_YEAR) / 1e3)
    sc = scenario(pack, reg, 'mid', 'median')
    print(f"scenario mid/median: s {sc['s']:.4f}, g {sc['g']}, y {sc['y']}, pen {sc['pen']}, gdp_g {sc['gdp_g']:.4f}; income scale {scaled[0]['income_scale']:.4f} (B.6g {B6G_YEAR})")
    one('mid_median_A_scaled', scaled, sc, gdp0)
    one('mid_median_A_unscaled', raw, sc, gdp0)
    one('legacy', scaled, dict(sc, arm='legacy'), gdp0)


if __name__ == '__main__':
    {'units': units, 'run': run}.get(sys.argv[1] if sys.argv[1:] else '', lambda: sys.exit('usage: run_cell_baseline.py units|run'))()
