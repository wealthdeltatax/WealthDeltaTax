"""P11 and P12 of architecture.md 6.2 for the UK pack's macro fields (brief 070c). Kept apart from test_pack.py, which is at its line budget."""
import hashlib, json, shutil
from pathlib import Path

import openpyxl, pytest

from model_v3.core import pack as pk

ROOT = Path(__file__).parents[2]
GBR = ROOT / 'model_v3' / 'pack' / 'GBR'


def jst():
    rows = list(openpyxl.load_workbook(ROOT / 'data/rates' / 'JSTdatasetR6.xlsx', read_only=True, data_only=True)['Sheet1'].iter_rows(values_only=True))
    return {r[0]: dict(zip(rows[0], r)) for r in rows[1:] if r[2] == 'GBR'}


def edit(z, name, old, new):
    p = z / name
    p.write_text(p.read_text().replace(old, new, 1), newline='')
    m = json.loads((z / 'manifest.json').read_text())
    for f in m['files']:
        if f['name'] == name:
            f['sha256'] = hashlib.sha256(p.read_bytes()).hexdigest()
    (z / 'manifest.json').write_text(json.dumps(m))


def test_p11_gdp_pc_has_the_jst_span_is_positive_and_matches_the_sheet():
    rows, sheet = pk.load_pack(GBR).tables['returns'], jst()
    assert [r['year'] for r in rows] == list(range(1870, 2020)) and all(r['gdp_pc'] > 0 for r in rows)
    assert all(abs(r['gdp_pc'] - sheet[r['year']]['rgdpmad']) < 1e-6 for r in rows)      # the file prints six decimals
    assert next(r for r in rows if r['year'] == 2019)['gdp_pc'] == pytest.approx(26341.025966169807, abs=1e-6)
    assert next(r for r in rows if r['year'] == 2019)['cpi'] == 193.109993               # cpi is as it was


def test_p12_the_total_row_equals_the_sheet():
    rows, sheet = pk.load_pack(GBR).tables['public_expenditure'], jst()[2019]
    (r,) = rows
    assert (r['function'], r['fiscal_year'], r['basis'], r['gbp_bn']) == ('total', '2019', 'outturn', None)
    assert r['pct_gdp'] == round(100 * sheet['expenditure'] / sheet['gdp'], 2) == 36.82


@pytest.mark.parametrize('file,old,new,match', [
    ('returns.csv', '2019,18.38,3.27202,5.720197,8.84315,193.109993,26341.025966', '2019,18.38,3.27202,5.720197,8.84315,193.109993,0', r'returns\.csv:151:gdp_pc'),
    ('public_expenditure.csv', '36.82', '0', r'public_expenditure\.csv:2:pct_gdp'),
    ('public_expenditure.csv', '36.82', '100', r'public_expenditure\.csv:2:pct_gdp'),
    ('public_expenditure.csv', 'total,2019', 'health,2019', r'public_expenditure\.csv:-:function: a non-empty file needs a total row')])
def test_p12_the_loader_rejects_a_broken_macro_field(tmp_path, file, old, new, match):
    shutil.copytree(GBR, tmp_path / 'GBR')
    edit(tmp_path / 'GBR', file, old, new)
    with pytest.raises(pk.PackError, match=match):
        pk.load_pack(tmp_path / 'GBR')
