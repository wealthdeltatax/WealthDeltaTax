"""
validate.py -- brief 125c block 2: what the untaxed household cells imply, against the held 099r moments. A comparison, not a calibration: no parameter is changed.
The model side is the untaxed cell baseline (`model/model_v3/core/cells.py`, convention A, 100 years, no tax) at the three saving values (min, median, max of the ONS non-pension ratio; none central),
mid regime, the stored inputs of `docs/model-v3/cell-baseline/inputs_used.json`, income scaled to B.6g, accrual as observed. Writes comparison.csv next to itself; prints summary lines only.
Result per moment: observed, model min and max over the saving axis, the gap (0 inside the range, else the signed distance to the nearest end), a label (inside, outside, definition differs).
Run from the repository root:   python -I model/studies/household-arm-validation/validate.py
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
DATA = ROOT / 'docs' / 'model-v3' / 'household-arm-validation'   # outputs and stored tables stay here until 163c
sys.path.insert(0, str(ROOT / 'model'))

from model_v3.core import cells as ce, pack as pk  # noqa: E402

YEARS = 100
OBS_RATIO = ROOT / 'data' / 'uk-wealth-tables' / '097r' / 'qsa_household_annual_2026q2.csv'
COLS = ('id', 'measure', 'population_and_definition_of_observed', 'observed', 'observed_source', 'model_min', 'model_max', 'axis', 'gap', 'label', 'definitions_that_differ')


def share(part, whole):
    return part / whole


def growth(a0, a1):
    return a1 / a0 - 1.0


def gap(observed, lo, hi):
    """0 when the observed value is inside [lo, hi], else the signed distance to the nearest end (observed minus that end)."""
    lo, hi = min(lo, hi), max(lo, hi)
    return 0.0 if lo <= observed <= hi else (observed - lo if observed < lo else observed - hi)


def label(observed, lo, hi, differs):
    """`definition differs` wins: the numbers are shown, but no inside or outside is claimed."""
    if differs:
        return 'definition differs'
    return 'inside' if gap(observed, lo, hi) == 0.0 else 'outside'


def observed_ratio(year):
    with open(OBS_RATIO, newline='', encoding='utf-8') as fh:
        (v,) = [float(r['value']) for r in csv.DictReader(fh) if r['sheet'] == 'HH_3' and r['series_id'] == 'DGD8' and r['period'] == str(year)]
    return v / 100


def setup():
    inp = json.loads((ROOT / 'docs' / 'model-v3' / 'cell-baseline' / 'inputs_used.json').read_text())
    pack, reg = pk.load_pack(ROOT / 'data' / 'country-packs' / 'GBR'), pk.load_register(ROOT / 'data' / 'input-register' / 'inputs.json')
    cells, _ = ce.scaled(ce.cell_table(pack, reg, inp['etb']), inp['b6g_2024'] / 1.0)
    r, y = inp['regimes']['mid'], inp['yreg']['mid']
    rets = dict(g=dict(property=0.016455, net_financial=r - y, physical=reg['I-D1j'].central / 100, pension=r - y), y=dict(property=0.03758, net_financial=y, pension=y))
    gdp = pk.lookup(pack, 'wealth_distribution', variable='gdp', band='all')[0]['value'] * 1e9
    return inp, cells, rets, gdp


def run(cells, inp, rets, sav):
    """Aggregate untaxed run: per year, wealth by class and by band (pounds), and the saving ratio (S over income). Households times per-household positions."""
    paths = {c['cell']: ce.run_cell(c, YEARS, sav, inp['acc']['obs'], inp['g'], rets) for c in cells}
    unit = ce.UNIT
    out = {}
    for t in range(YEARS + 1):
        w = {k: 0.0 for k in ce.CLASSES}; band = {}; ret = 0.0; S = 0.0; Y = 0.0
        for c in cells:
            pos = c['pos'] if t == 0 else paths[c['cell']][t - 1][1]
            n = c['households']
            for k in ce.CLASSES:
                w[k] += n * float(pos[k]) * unit
            band[c['band']] = band.get(c['band'], 0.0) + n * sum(float(pos[k]) for k in ce.CLASSES) * unit
            ret += n * sum(float(pos[k]) for k in ce.CLASSES) * unit if c['stage'] == 'retired' else 0.0
            if t >= 1:
                a = paths[c['cell']][t - 1][2]
                S += n * float(a['S']) * unit; Y += n * float(a['income']) * unit
        out[t] = dict(classes=w, total=sum(w.values()), band=band, retired=ret, ratio=(S / Y if t >= 1 else float('nan')))
    return out


def main():
    inp, cells, rets, gdp = setup()
    runs = {k: run(cells, inp, rets, v) for k, v in inp['sav'].items()}
    rng = lambda f: (min(f(r) for r in runs.values()), max(f(r) for r in runs.values()))
    rows = []
    add = lambda *a: rows.append(dict(zip(COLS, a)))
    lo, hi = rng(lambda r: r[0]['total'] / gdp)
    add('BF-11', 'Aggregate net wealth over GDP, year 0', 'GB households, 2020-22, RF pension valuation', 7.5, 'Before the fall, p15 (about 7.5 times GDP; 17tn)', lo, hi, 'none (year 0 is the pack)', gap(7.5, lo, hi), label(7.5, lo, hi, True),
        'RF values pensions at market annuity rates, the pack at ONS SCAPE; the model total is the pack total by construction')
    lo, hi = rng(lambda r: share(r[0]['band']['D10'], r[0]['total']))
    add('BF-13', 'Wealth share of the top band, year 0 (top 10% held about half)', 'GB, per-adult families, RF basis', 0.5, 'Before the fall (top 10% about half since 1980)', lo, hi, 'none (year 0 is the pack)', gap(0.5, lo, hi), label(0.5, lo, hi, True),
        'households (the pack D10) against families; the top-1% share (18% to 23%) is not computable: no split inside D10')
    lo, hi = rng(lambda r: share(r[YEARS]['band']['D10'], r[YEARS]['total']))
    add('BF-13', 'Wealth share of the top band, year 100 untaxed', 'as above', 0.5, 'as above', lo, hi, 'saving min to max', gap(0.5, lo, hi), label(0.5, lo, hi, True), 'as above; a scenario value, not a forecast')
    lo, hi = rng(lambda r: share(r[0]['retired'], r[0]['total']))
    add('BF-14', 'Share of wealth held by the retired cells, year 0', 'GB adults aged 60 and over, 2020-22', 0.49, 'Before the fall, Fig (people aged 60 and over held 49%)', lo, hi, 'none (year 0)', gap(0.49, lo, hi), label(0.49, lo, hi, True),
        'an age proxy for stage; the model stage split of wealth is by person share, so its number is the retired person share')
    lo, hi = rng(lambda r: r[1]['ratio'])
    for yr, src in ((2019, 'ONS QSA HH_3 DGD8 2019'), (2022, 'ONS QSA HH_3 DGD8 2022'), (2024, 'ONS QSA HH_3 DGD8 2024'), (2025, 'ONS QSA HH_3 DGD8 2025')):
        o = observed_ratio(yr)
        add('GB-01', f'Household saving ratio, total, year 1 against {yr}', 'UK households and NPISH, annual, incl. the pension adjustment', o, src, lo, hi, 'saving min to max', gap(o, lo, hi), label(o, lo, hi, False),
            'the non-pension ratio is an input drawn from the same ONS series, so the axis spans the observed values by construction; the accrual is added on top')
    o = observed_ratio(2020)
    add('BF-15', 'Household saving ratio, total, year 1 against 2020', 'UK households and NPISH, annual (the RF 25% quarterly peak is not held)', o, 'ONS QSA HH_3 DGD8 2020', lo, hi, 'saving min to max', gap(o, lo, hi), label(o, lo, hi, False),
        'the held value is annual; the RF figure is a seasonally adjusted quarter, not held')
    with open(DATA / 'comparison.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, COLS); w.writeheader(); w.writerows([{k: (round(v, 5) if isinstance(v, float) else v) for k, v in r.items()} for r in rows])
    for r in rows:
        print(f"{r['id']:6} {r['measure'][:62]:62} observed {r['observed']:.3f}  model {r['model_min']:.3f} to {r['model_max']:.3f}  gap {r['gap']:+.3f}  {r['label']}")


if __name__ == '__main__':
    main()
