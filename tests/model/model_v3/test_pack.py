"""Tests P1 to P10 of architecture.md 6.2 for core/pack.py: P1 to P7 and P10 on the invented ZZZ pack (047c), P8 and P9 on the UK pack (048c)."""
import ast, hashlib, json, re, shutil, sys
from pathlib import Path

import numpy as np, pytest

from model_v3.core import pack as pk

FIX = Path(__file__).parent / 'fixtures' / 'pack_ZZZ'
PINNED = 'f7cbb8948ca28eaede41e157c8c3af4f1b049be2c5288ef310bceab25c24d54d'   # P7: the fixture's pack_sha256
ROOT = Path(__file__).parents[3]
GBR = ROOT / 'data' / 'country-packs' / 'GBR'
GBR_SHA = '5ac89a2db2dacb60d75d4cb37974fd481aaaf23cf59ad2aa8aa881f46ee3d72c'   # the UK pack_sha256, pinned: a rebuilt pack that changes a byte fails here
KNOWN_UNORDERED = {'I-T3d', 'I-T3e', 'I-T3g', 'I-T3m', 'I-T3p'}   # register rows with low > central or central > high (finding of 048c, for the author)
PARTS = {'stamp_all': ['stamp_a', 'stamp_b'], 'income_tax': ['pay_a', 'pay_b']}


@pytest.fixture
def zzz(tmp_path):   # the loader wants the folder named by the country, so the fixture is copied to .../ZZZ
    shutil.copytree(FIX, tmp_path / 'ZZZ')
    return tmp_path / 'ZZZ'


def edit(z, name, old, new, rehash=True):
    """Replace the first `old` by `new` in a pack file; with rehash the manifest follows, so only the schema can object."""
    p = z / name
    p.write_text(p.read_text().replace(old, new, 1), newline='')
    if rehash:
        m = json.loads((z / 'manifest.json').read_text())
        for f in m['files']:
            if f['name'] == name:
                f['sha256'] = hashlib.sha256(p.read_bytes()).hexdigest()
        (z / 'manifest.json').write_text(json.dumps(m))


def fails(z, match, *edits, **kw):
    for e in edits:
        edit(z, *e, **kw)
    with pytest.raises(pk.PackError, match=match):
        pk.load_pack(z)


def test_p1_fixture_loads_every_dataset(zzz):
    p = pk.load_pack(zzz)
    assert (p.country, p.currency, p.base_year, p.version) == ('ZZZ', 'ZZD', 2020, 1)
    assert set(p.tables) == set(pk.SCHEMA) and all(len(p.tables[d]) == p.files[f'{d}.csv']['rows'] for d in p.tables)
    assert p.tables['returns'][0]['capital_tr'] is None and p.tables['returns'][2]['capital_tr'] == 4.4   # no fill
    years, v = pk.series(p, 'capital_tr')
    assert list(years[:3]) == [2000, 2001, 2002] and np.isnan(v[:2]).all() and v[2] == 4.4


def test_p2_changed_byte_fails_on_sha256_and_names_file_row_column(zzz):
    fails(zzz, r'returns\.csv: sha256 mismatch.*returns\.csv:3:eq_tr', ('returns.csv', '2001,6,', '2001,x,'), rehash=False)


def test_p2_a_changed_byte_that_stays_valid_names_its_file(zzz):
    fails(zzz, r'receipts\.csv: sha256', ('receipts.csv', 'income_tax,2025-26,10', 'income_tax,2025-26,11'), rehash=False)


@pytest.mark.parametrize('file,old,new,match', [
    ('receipts.csv', 'line,fiscal_year', 'fiscal_year,line', r'receipts\.csv:1:header'),
    ('returns.csv', '2000,5,3.0,2.0,,100.0,', '2000,5,3.0,2.0,100.0,', r'returns\.csv:2:-: 6 cells')])
def test_p3_wrong_header_order_and_cell_count_fail(zzz, file, old, new, match):
    fails(zzz, match, (file, old, new))


@pytest.mark.parametrize('bad', ['"1,234.5"', 'nan', '"4,5"', '1e999'])
def test_p3_number_formats_the_pack_forbids(zzz, bad):
    fails(zzz, r'returns\.csv:3:cpi', ('returns.csv', '102.0', bad))


@pytest.mark.parametrize('file,old,new,match', [
    ('returns.csv', '104.04', '', r'returns\.csv:4:cpi: empty cell'),   # P4
    ('wealth_distribution.csv', 'ge_100,40', 'ge_100,140', r'wealth_distribution\.csv:12:value'),   # P5
    ('receipts.csv', 'income_tax,2025-26,10', 'income_tax,2025-26,100', r'receipts\.csv:2:pct_gdp'),
    ('tax_rules.csv', ',20,,', ',120,,', r'tax_rules\.csv:2:rate'),
    ('returns.csv', '2000,5,', '2000,-100,', r'returns\.csv:2:eq_tr'),
    ('returns.csv', '2.0,,100.0', '2.0,,-5', r'returns\.csv:2:cpi')])
def test_p5_other_ranges(zzz, file, old, new, match):
    fails(zzz, match, (file, old, new))


def test_p6_partition_must_sum_to_100_within_half_a_point(zzz):
    edit(zzz, 'wealth_distribution.csv', 'D1,0.5', 'D1,0.9')
    assert pk.load_pack(zzz)
    edit(zzz, 'wealth_distribution.csv', 'D1,0.9', 'D1,2.5')
    fails(zzz, r'wealth_distribution\.csv:2:value: bands of wealth_share partition.*sum to', ('wealth_distribution.csv', 'D1,0.5', 'D1,2.5'))


def test_p7_fixture_pack_hash_is_pinned(zzz):
    assert pk.load_pack(zzz).sha256 == PINNED


def test_p7_hash_moves_with_data_currency_and_base_year(zzz):
    edit(zzz, 'tax_rules.csv', ',20,,', ',21,,')
    assert pk.load_pack(zzz).sha256 != PINNED
    for k, v in (('currency', 'ZZE'), ('base_year', 2021), ('pack_version', 2)):
        m = json.loads((FIX / 'manifest.json').read_text())
        m[k] = v
        (zzz / 'manifest.json').write_text(json.dumps(m))
        shutil.copy(FIX / 'tax_rules.csv', zzz / 'tax_rules.csv')
        assert pk.load_pack(zzz).sha256 not in (PINNED, None)
    shutil.copy(FIX / 'tax_rules.csv', zzz / 'tax_rules.csv')
    (zzz / 'manifest.json').write_text(json.dumps(dict(json.loads((FIX / 'manifest.json').read_text()), built='2030-01-01')))
    assert pk.load_pack(zzz).sha256 == PINNED   # the built date is not hashed


def test_p10_stamp_sub_rows_are_never_summed_with_their_parent(zzz):
    p = pk.load_pack(zzz)
    assert pk.receipts_sum(p, ['stamp_a', 'stamp_b'], PARTS) == pytest.approx(0.9)
    assert pk.receipts_sum(p, ['stamp_all', 'sales_tax'], PARTS) == pytest.approx(7.0)
    with pytest.raises(pk.PackError, match='summed with its own parts'):
        pk.receipts_sum(p, ['stamp_all', 'stamp_a'], PARTS)
    pk.check_parts(p, PARTS)
    with pytest.raises(pk.PackError, match='sum to more'):
        pk.check_parts(p, {'stamp_all': ['stamp_a', 'stamp_b', 'property_tax']})


def test_manifest_rules(zzz):
    m = json.loads((zzz / 'manifest.json').read_text())
    for k in ('currency', 'built', 'files'):
        bad = {a: b for a, b in m.items() if a != k}
        (zzz / 'manifest.json').write_text(json.dumps(bad))
        with pytest.raises(pk.PackError, match=f'manifest.json:{k}'):
            pk.load_pack(zzz)
    (zzz / 'manifest.json').write_text(json.dumps(dict(m, country='QQQ')))
    with pytest.raises(pk.PackError, match='differs from the folder name'):
        pk.load_pack(zzz)
    (zzz / 'manifest.json').write_text(json.dumps(dict(m, base_year=None)))
    assert pk.load_pack(zzz).base_year is None


def test_manifest_file_entries(zzz):
    m = json.loads((zzz / 'manifest.json').read_text())
    for field, val in (('licence', 'free'), ('vintage', ''), ('dataset', 'nope')):
        m2 = json.loads(json.dumps(m))
        m2['files'][0][field] = val
        (zzz / 'manifest.json').write_text(json.dumps(m2))
        with pytest.raises(pk.PackError, match='bad entry'):
            pk.load_pack(zzz)
    m['files'][0]['rows'] = 99
    (zzz / 'manifest.json').write_text(json.dumps(m))
    with pytest.raises(pk.PackError, match='manifest says 99 rows'):
        pk.load_pack(zzz)
    (zzz / 'manifest.json').unlink()
    with pytest.raises(pk.PackError, match='manifest.json is missing'):
        pk.load_pack(zzz)


@pytest.mark.parametrize('file,old,new,match', [
    ('returns.csv', '2003,', '2004,', r'returns\.csv:5:year'),
    ('wealth_distribution.csv', 'households_above,ge_100,40,pct_households', 'wealth_share,D1,40,pct_households', r'wealth_distribution\.csv:12:variable: duplicate of row 2'),
    ('wealth_tail.csv', '2010,18.0,', '2010,15.0,', r'wealth_tail\.csv:2:low'),
    ('receipts.csv', 'pay_a,', 'pay_b,', r'receipts\.csv:4:line: duplicate'),
    ('household_incidence.csv', ',D10,,25,', ',D10,,30,', r'household_incidence\.csv:7:value: decile mean'),
    ('household_incidence.csv', 'top_decile,all,income_tax,40', 'top_decile,all,,40', r'household_incidence\.csv:17:tax: empty'),
    ('tax_rules.csv', ',20,,', ',20,5,', r'tax_rules\.csv:2:rate: exactly one'),
    ('tax_rules.csv', 'higher,50,150', 'higher,40,150', r'tax_rules\.csv:3:lower: bands'),
    ('tax_rules.csv', 'higher,50,150', 'higher,50,', r'tax_rules\.csv:4:lower: bands')])
def test_cross_checks(zzz, file, old, new, match):
    fails(zzz, match, (file, old, new))


def test_an_interior_gap_in_a_return_column_loads_and_stays_missing(zzz):   # JST has no housing or capital return for 1940-46
    edit(zzz, 'returns.csv', '2003,8,4.5,2.3,4.6,', '2003,8,4.5,2.3,,')
    assert pk.load_pack(zzz).tables['returns'][3]['capital_tr'] is None


def test_register_loader(tmp_path):
    f = tmp_path / 'r.json'
    f.write_text(json.dumps({'inputs': [{'id': 'I-A', 'low': 1, 'central': 2, 'high': 3, 'unit': '%', 'judgement': True},
                                        {'id': 'I-B', 'low': None, 'central': 5, 'high': None, 'unit': '', 'judgement': False}]}))
    r = pk.load_register(f)
    assert r['I-A'] == pk.Row('I-A', 1.0, 2.0, 3.0, '%', True) and r['I-B'].low is None and not r['I-B'].judgement
    for bad in ({'id': 'I-A', 'low': 1, 'central': 2, 'high': 3, 'judgement': 0}, {'id': 'I-C', 'low': 'x', 'central': 1, 'high': 2, 'judgement': 0}):
        f.write_text(json.dumps({'inputs': [{'id': 'I-A', 'low': 1, 'central': 2, 'high': 3, 'judgement': 0}, bad]}))
        with pytest.raises(pk.PackError, match='register'):
            pk.load_register(f)


def test_real_register_loads_with_flags():
    r = pk.load_register(Path(__file__).parents[3] / 'data' / 'input-register' / 'inputs.json')
    assert r['I-D4a'].central == 5.94 and r['I-D4a'].low <= r['I-D4a'].high and any(x.judgement for x in r.values())


def test_x1_and_x2_on_the_fixture(zzz):
    p = pk.load_pack(zzz)
    reg = {'I-X': pk.Row('I-X', 1.0, 10.0, 11.0, '%', False)}
    ptr = {'I-X': ('receipts', {'line': 'income_tax'}, 'pct_gdp')}
    assert pk.check_x1(p, reg, ptr) == 1
    with pytest.raises(pk.PackError, match='X1 I-X'):
        pk.check_x1(p, {'I-X': pk.Row('I-X', 1.0, 10.000001, 11.0, '%', False)}, ptr)
    assert pk.check_x2(p, ['sales_tax', 'stamp_all', 'property_tax'], 8.5, parts=PARTS) == pytest.approx(8.5)
    with pytest.raises(pk.PackError, match='X2'):
        pk.check_x2(p, ['sales_tax'], 8.5)
    with pytest.raises(pk.PackError, match='no such line'):
        pk.check_x2(p, ['nope'], 1)


def test_data_facts_dh1a_and_dh1b(zzz):
    p = pk.load_pack(zzz)
    a = pk.dh1a(p)
    assert a['adult_top1'] == {'point': 20.0, 'lo': 18.0, 'hi': 22.0, 'year': 2020, 'basis': 'adult', 'history': [(2010, 18.0), (2020, 20.0)]}
    assert set(a) == {'adult_top1', 'adult_top10'} and a['adult_top10']['lo'] is None
    b = pk.dh1b(p, {'labour': ['pay_a', 'pay_b'], 'wealth': ['property_tax']})
    assert b['lines']['income_tax'] == 10 and b['groups'] == {'labour': 7, 'wealth': 1.5}
    with pytest.raises(pk.PackError):
        pk.dh1b(p, {'g1': ['pay_a'], 'g2': ['pay_a']})
    assert len(pk.lookup(p, 'receipts', line='income_tax')) == 1


def test_only_numpy_and_the_standard_library_are_imported():
    t = ast.parse((Path(__file__).parents[3] / 'model' / 'model_v3' / 'core' / 'pack.py').read_text())
    roots = {n.module.split('.')[0] if isinstance(n, ast.ImportFrom) else a.name.split('.')[0]
             for n in ast.walk(t) if isinstance(n, (ast.Import, ast.ImportFrom)) for a in getattr(n, 'names', [])}
    assert roots <= set(sys.stdlib_module_names) | {'numpy'}


def test_p8_the_uk_pack_agrees_with_the_register_and_the_retirement_target():
    mp = json.loads((ROOT / 'model' / 'model_v3' / 'levers.json').read_text())['pack_mappings']
    p, reg = pk.load_pack(GBR), pk.load_register(ROOT / 'data' / 'input-register' / 'inputs.json')
    assert pk.check_x1(p, reg, mp['x1_pointers']) == len(mp['x1_pointers']) > 0
    assert set(mp['x1_skipped']) <= set(reg) and not set(mp['x1_skipped']) & set(mp['x1_pointers'])
    pk.check_parts(p, mp['parts'])
    x = mp['x2']
    assert abs(pk.check_x2(p, x['lines'], x['target'], x['tolerance'], mp['parts']) - x['target']) <= x['tolerance']


def test_p9_the_register_agrees_with_inputs_md():
    text = (ROOT / 'docs' / 'model-v3' / 'inputs.md').read_text(encoding='utf-8')
    md = {m[1]: '(J)' in line for line in text.splitlines() if (m := re.match(r'\| (I-\w+) \|', line))}
    reg = pk.load_register(ROOT / 'data' / 'input-register' / 'inputs.json')
    assert len(reg) == len(md) == int(re.search(r'register has (\d+) rows', text)[1]) == json.loads((ROOT / 'data' / 'input-register' / 'inputs.json').read_text())['count']
    assert {i: r.judgement for i, r in reg.items()} == md
    bad = {i for i, r in reg.items() if r.low is not None and r.high is not None and not r.low <= r.central <= r.high}
    assert bad == KNOWN_UNORDERED


def test_p7_the_uk_pack_hash_is_pinned():
    assert pk.load_pack(GBR).sha256 == GBR_SHA


@pytest.mark.parametrize('file,old,new,match', [
    ('band_composition.csv', 'B1,pension,35,', 'B1,pension,30,', r'band_composition\.csv:2:value: classes of B1 sum to 95'),
    ('band_composition.csv', 'B2,physical,5.2,', 'B2,property,5.2,', r'band_composition\.csv:8:band: duplicate of row 6'),
    ('cell_weights.csv', 'B1,retired,', 'B1,not retired,', r'cell_weights\.csv:3:band: duplicate'),
    ('cell_weights.csv', 'B2,retired,', 'B2,old,', r'cell_weights\.csv:5:stage'),
    ('cell_weights.csv', ',700,', ',-7,', r'cell_weights\.csv:4:persons'),
    ('decile_composition.csv', 'D2,B1,pension,40,', 'D2,B1,pension,30,', r'decile_composition\.csv:6:value: classes of D2 sum to 90'),                  # 115c
    ('decile_composition.csv', 'D3,B2,physical,5.2,', 'D3,B2,property,5.2,', r'decile_composition\.csv:12:decile: duplicate of row 10')])
def test_cell_inputs_of_the_fixture_are_checked(zzz, file, old, new, match):   # 109c
    fails(zzz, match, (file, old, new))


def test_the_uk_pack_carries_the_cell_inputs_and_they_close():   # 109c
    p = pk.load_pack(GBR)
    w, c = p.tables['cell_weights'], p.tables['band_composition']
    bands = ['D1-3', 'D4-5', 'D6-7', 'D8-9', 'D10']
    assert [(x['band'], x['stage']) for x in w] == [(b, s) for b in bands for s in ('not retired', 'retired')] and p.version == 3
    assert abs(sum(x['persons'] for x in w) - 50_200_000) <= sum(x['max_rounding'] for x in w) and round(sum(x['persons'] for x in w) / 1e6, 2) == 50.20
    assert {x['class'] for x in c} == {'property', 'net_financial', 'physical', 'pension'} and len(c) == 20
    assert all(abs(sum(x['value'] for x in c if x['band'] == b) - 100) <= 0.5 for b in bands)


def test_the_uk_pack_carries_the_decile_mixes_and_they_reproduce_the_band_rows():   # 115c
    p = pk.load_pack(GBR)
    d, c = p.tables['decile_composition'], p.tables['band_composition']
    w = {x['band']: x['value'] for x in p.tables['wealth_distribution'] if x['variable'] == 'wealth_total'}   # a decile's net wealth: the weights of the band's value-weighted shares (persons or households do not give them)
    ids = {x['decile'] for x in d}
    assert len(d) == 40 and ids == {f'D{i}' for i in range(1, 11)} and all(abs(sum(x['value'] for x in d if x['decile'] == k) - 100) <= 0.05 for k in ids)
    assert [x['value'] for x in d if x['decile'] == 'D1'] == [-4.72, -104.92, 169.46, 40.18] and 'assumption' in next(x['basis'] for x in d if x['decile'] == 'D10')
    for x in c:
        ds = {y['decile'] for y in d if y['band'] == x['band']}
        assert abs(sum(w[k] * y['value'] for k in ds for y in d if y['decile'] == k and y['class'] == x['class']) / sum(w[k] for k in ds) - x['value']) < 0.06, x
