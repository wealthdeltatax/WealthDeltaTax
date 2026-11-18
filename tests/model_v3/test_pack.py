"""Tests P1 to P7 and P10 of architecture.md 6.2 for core/pack.py, on the invented ZZZ pack (brief 047c). P8 and P9 need the UK pack (V3-3)."""
import ast, hashlib, json, shutil, sys
from pathlib import Path

import numpy as np
import pytest

from model_v3.core import pack as pk

FIX = Path(__file__).parent / 'fixtures' / 'pack_ZZZ'
PINNED = '90031fcd58434fe98b1329646ceb40320a229ecb36c430f1f99ede8b505d67c5'   # P7: the fixture's pack_sha256
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


def test_p1_missing_values_stay_missing(zzz):
    years, v = pk.series(pk.load_pack(zzz), 'capital_tr')
    assert list(years[:3]) == [2000, 2001, 2002] and np.isnan(v[:2]).all() and v[2] == 4.4


def test_p2_changed_byte_fails_on_sha256_and_names_file_row_column(zzz):
    fails(zzz, r'returns\.csv: sha256 mismatch.*returns\.csv:3:eq_tr', ('returns.csv', '2001,6,', '2001,x,'), rehash=False)


def test_p2_changed_byte_that_stays_valid_names_the_file(zzz):
    fails(zzz, r'returns\.csv: sha256 mismatch', ('returns.csv', '2001,6,', '2001,6.5,'), rehash=False)


def test_p2_the_manifest_may_not_hide_a_changed_byte_in_another_file(zzz):
    edit(zzz, 'receipts.csv', 'income_tax,2025-26,10', 'income_tax,2025-26,11', rehash=False)
    with pytest.raises(pk.PackError, match=r'receipts\.csv: sha256'):
        pk.load_pack(zzz)


def test_p3_wrong_header_order_fails(zzz):
    fails(zzz, r'receipts\.csv:1:header', ('receipts.csv', 'line,fiscal_year', 'fiscal_year,line'))


def test_p3_wrong_cell_count_and_junk_numbers_fail(zzz):
    fails(zzz, r'returns\.csv:2:-: 5 cells', ('returns.csv', '2000,5,3.0,2.0,,100.0', '2000,5,3.0,2.0,100.0'))


@pytest.mark.parametrize('bad', ['"1,234.5"', 'nan', '"4,5"', '1e999'])
def test_p3_number_formats_the_pack_forbids(zzz, bad):
    fails(zzz, r'returns\.csv:3:cpi', ('returns.csv', '102.0', bad))


def test_p4_empty_cell_where_not_allowed_fails(zzz):
    fails(zzz, r'returns\.csv:4:cpi: empty cell', ('returns.csv', '104.04', ''))


def test_p5_percent_outside_0_to_100_fails(zzz):
    fails(zzz, r'wealth_distribution\.csv:12:value', ('wealth_distribution.csv', 'ge_100,40', 'ge_100,140'))


@pytest.mark.parametrize('file,old,new,match', [
    ('receipts.csv', 'income_tax,2025-26,10', 'income_tax,2025-26,100', r'receipts\.csv:2:pct_gdp'),
    ('tax_rules.csv', ',20,,', ',120,,', r'tax_rules\.csv:2:rate'),
    ('returns.csv', '2000,5,', '2000,-100,', r'returns\.csv:2:eq_tr'),
    ('returns.csv', '2.0,,100.0', '2.0,,-5', r'returns\.csv:2:cpi')])
def test_p5_other_ranges(zzz, file, old, new, match):
    fails(zzz, match, (file, old, new))


def test_p6_partition_must_sum_to_100(zzz):
    fails(zzz, r'wealth_distribution\.csv:2:value: bands of wealth_share partition.*sum to', ('wealth_distribution.csv', 'D1,0.5', 'D1,2.5'))


def test_p6_partition_within_half_a_point_passes(zzz):
    edit(zzz, 'wealth_distribution.csv', 'D1,0.5', 'D1,0.9')
    assert pk.load_pack(zzz)


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


def test_p7_built_date_is_not_hashed(zzz):
    m = json.loads((zzz / 'manifest.json').read_text())
    m['built'] = '2030-01-01'
    (zzz / 'manifest.json').write_text(json.dumps(m))
    assert pk.load_pack(zzz).sha256 == PINNED


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
    ('returns.csv', '2003,8,4.5,2.3,4.6,', '2003,8,4.5,2.3,,', r'returns\.csv:5:capital_tr: missing inside'),
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
    r = pk.load_register(Path(__file__).parents[2] / 'registry' / 'inputs.json')
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
    t = ast.parse((Path(__file__).parents[2] / 'model_v3' / 'core' / 'pack.py').read_text())
    roots = {n.module.split('.')[0] if isinstance(n, ast.ImportFrom) else a.name.split('.')[0]
             for n in ast.walk(t) if isinstance(n, (ast.Import, ast.ImportFrom)) for a in getattr(n, 'names', [])}
    assert roots <= set(sys.stdlib_module_names) | {'numpy'}
