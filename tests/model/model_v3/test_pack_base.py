"""P10 of architecture.md 6.2 for the UK pack's base fields (brief 067c). Kept apart from test_pack.py, which is at its line budget."""
import hashlib, json, shutil
from pathlib import Path

import pytest

from model_v3.core import pack as pk

ROOT = Path(__file__).parents[3]
GBR = ROOT / 'data' / 'country-packs' / 'GBR'


def edit(z, name, old, new):
    """Replace `old` by `new` in a pack file and rehash it in the manifest, so only the loader's own checks can object."""
    p = z / name
    p.write_text(p.read_text().replace(old, new, 1), newline='')
    m = json.loads((z / 'manifest.json').read_text())
    for f in m['files']:
        if f['name'] == name:
            f['sha256'] = hashlib.sha256(p.read_bytes()).hexdigest()
    (z / 'manifest.json').write_text(json.dumps(m))


def uk_rows(p, var):
    return {r['band']: r for r in p.tables['wealth_distribution'] if r['variable'] == var}


def test_p10_the_uk_pack_carries_the_base_fields_and_they_match_the_sheets():
    import openpyxl
    p = pk.load_pack(GBR)
    t21 = [r for r in openpyxl.load_workbook(ROOT / 'data/rates' / 'totalwealthtables.xlsx', read_only=True, data_only=True)['Table 2.1'].iter_rows(values_only=True)]
    rev = [r for r in openpyxl.load_workbook(ROOT / 'data/rates' / 'Revenue composition spreadsheet.xlsx', read_only=True, data_only=True)['Total revenues'].iter_rows(values_only=True)]
    bands = [f'D{d}' for d in range(1, 11)]
    wt, hh = uk_rows(p, 'wealth_total'), uk_rows(p, 'households')
    assert set(wt) == set(hh) == set(bands) | {'all'} and not uk_rows(p, 'adults')       # no adults table is held
    assert wt['all']['value'] == t21[7][-1] == 13568 and hh['all']['value'] * 1000 == t21[28][-1] == 26991000
    assert abs(sum(wt[b]['value'] for b in bands) - wt['all']['value']) <= 0.5            # the bands partition the printed total
    assert abs(sum(hh[b]['value'] for b in bands) - hh['all']['value']) <= 0.1
    assert all((r['unit'], r['basis'], r['year']) == ('gbp_bn', 'household', '2020-22') for r in wt.values())
    assert all((r['unit'], r['basis']) == ('thousand', 'household') for r in hh.values())
    mh, = uk_rows(p, 'median_house_price').values()
    assert (mh['band'], mh['value'], mh['unit'], mh['basis'], mh['year']) == ('all', 300000, 'gbp', 'adult', 'YE Sep 2025')
    g = {r[0]: r[6] for r in rev if r and r[0] in ('2020-21', '2021-22')}
    gdp, = uk_rows(p, 'gdp').values()
    assert (gdp['unit'], gdp['value']) == ('gbp_bn', round(sum(g.values()) / 2, 2)) and gdp['value'] > 0


def test_p10_the_loader_rejects_a_broken_base_field(tmp_path):
    for name, old, new, match in [('wealth_total', 'wealth_total,D5,651.95', 'wealth_total,D5,700', r'wealth_distribution\.csv:\d+:value: bands D1 to D10 of wealth_total'),
                                  ('households', 'households,D3,2699.1', 'households,D3,2000', r'bands D1 to D10 of households'),
                                  ('house price', 'median_house_price,all,300000', 'median_house_price,all,0', r'median_house_price must be greater than 0'),
                                  ('gdp', 'gdp,all,2211.48', 'gdp,all,-1', r'gdp must be greater than 0'),
                                  ('unit', 'gdp,all,2211.48,gbp_bn', 'gdp,all,2211.48,gbp_billion', r'unit')]:
        z = tmp_path / name.replace(' ', '') / 'GBR'
        shutil.copytree(GBR, z)
        edit(z, 'wealth_distribution.csv', old, new)
        with pytest.raises(pk.PackError, match=match):
            pk.load_pack(z)
