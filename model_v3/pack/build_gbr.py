"""Builds model_v3/pack/GBR from the held files (brief 048c). A data tool, not core: run once from the repo root and commit the output.

    python3 -B -I model_v3/pack/build_gbr.py

Writes the seven CSV files, manifest.json and NOTICE.md, copies model_v2/jst_r6.json unchanged to GBR/source/, and rewrites the x1_pointers and
x1_skipped parts of levers.json's pack_mappings. Numbers are computed from the held sheets and rounded to the precision the register prints them at
(percent shares one decimal, receipts two, pounds whole) so X1 can compare them exactly; a value no sheet gives is left out, never filled. A re-run gives
byte-identical files. No test beyond the hash check of test_pack.py.
"""
import csv
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'model_v3' / 'pack' / 'GBR'
WEALTH, REVENUE, ETB = 'Rates Data/totalwealthtables.xlsx', 'Rates Data/Revenue composition spreadsheet.xlsx', 'Research/etbreferencetablesfye202324final.xlsx'
HOUSING = 'Research/Housing affordability in England and Wales 2025.pdf'
SCHEMA = {'returns': 'year eq_tr housing_tr bond_tr capital_tr cpi', 'wealth_distribution': 'variable band value unit basis year',
          'wealth_tail': 'series year value unit low high basis', 'receipts': 'line fiscal_year pct_gdp gbp_bn basis',
          'household_incidence': 'variable group tax value unit fiscal_year basis', 'tax_rules': 'rule tax_year subject lower upper rate amount flag',
          'public_expenditure': 'function fiscal_year pct_gdp gbp_bn basis'}
KEY = {'wealth_distribution': 'variable band', 'wealth_tail': 'series year', 'receipts': 'line', 'household_incidence': 'variable group tax'}
SKIP = {'derived from the return series, checked by the model not stored': ['I-D1c', 'I-D1d', 'I-D1e'] + [f'I-H6{c}' for c in 'abcdefghi'],
        'needs W_min, a register input, so no pack row': [f'I-H2a{i}' for i in range(1, 8)],
        'no held sheet gives the HMRC series': ['I-D7d'],
        'data not in the repo (register In repo cell says no)': ['I-D4d', 'I-D4f', 'I-W5c', 'I-W5d', 'I-T1a', 'I-T1b', 'I-T1e'] + [f'I-H1{c}' for c in 'abcdefghij'] + [f'I-T7{c}' for c in 'abcdef']}
ROWS, POINTERS, BOOKS = {d: [] for d in SCHEMA}, {}, {}


def sheet(path, name):
    BOOKS[path] = BOOKS.get(path) or openpyxl.load_workbook(ROOT / path, read_only=True, data_only=True)
    return [list(r) for r in BOOKS[path][name].iter_rows(values_only=True)]


def txt(x):
    return '' if x is None else f'{x:.6f}'.rstrip('0').rstrip('.') if isinstance(x, float) else str(x)


def add(ds, ids, **cells):
    """One pack row; `ids` are the register rows that point at it (X1)."""
    ROWS[ds].append([cells.get(c, '') for c in SCHEMA[ds].split()])
    col = 'pct_gdp' if ds == 'receipts' else 'value'
    for i in ids:
        POINTERS[i] = [ds, {k: int(cells[k]) if str(cells.get(k)).isdigit() else (cells.get(k) or None) for k in KEY.get(ds, '').split()}, col]


def returns():
    j = json.loads((OUT / 'source' / 'jst_r6.json').read_text(encoding='utf-8'))['countries']['GBR']
    for k, y in enumerate(j['years']):
        if y <= 2019:    # the return sample ends in 2019 (author, 2026-11-18)
            v = {s: j['series'][s][k] for s in ('eq_tr', 'housing_tr', 'bond_tr', 'capital_tr', 'cpi')}
            ROWS['returns'].append([y] + [txt(None if v[s] is None else v[s] * (1 if s == 'cpi' else 100)) for s in v])


def wealth():
    t = sheet(WEALTH, 'Table 2.2')
    at = lambda b, ds: sum(t[2 + 10 * b + d][10] for d in ds)   # block 0 total, 1 property, 2 financial, 4 pension; rows are deciles 1 to 10
    bands = {'D4-5': [4, 5], 'D6-7': [6, 7], 'D8-9': [8, 9], 'D10': [10]}
    row = lambda var, band, v, unit, ids: add('wealth_distribution', ids, variable=var, band=band, value=txt(v), unit=unit, basis='household', year='2020-22')
    for band, ds, ids in zip(bands, bands.values(), [('I-D9e',), ('I-D9f', 'I-T6h'), ('I-D9g', 'I-T6i'), ('I-D9h', 'I-T6j')]):
        row('net_financial_share', band, round(100 * at(2, ds) / at(0, ds), 1), 'pct_of_band', ids)
    row('pension_share', 'all', round(100 * at(4, range(1, 11)) / at(0, range(1, 11)), 1), 'pct_of_band', ('I-W5e',))
    for band, ids in zip(list(bands)[1:], ['I-T6b', 'I-T6c', 'I-T6d']):
        row('pension_share', band, round(100 * at(4, bands[band]) / at(0, bands[band]), 1), 'pct_of_band', (ids,))
    for band, ids in zip(list(bands)[1:], ['I-T6e', 'I-T6f', 'I-T6g']):
        row('property_share', band, round(100 * at(1, bands[band]) / at(0, bands[band]), 1), 'pct_of_band', (ids,))
    for band, ids in zip(bands, ['I-T4a', 'I-T4b', 'I-T4c', 'I-T4d']):
        row('gain_bearing_wealth', band, round((at(1, bands[band]) + at(2, bands[band])) / 1000), 'gbp_bn', (ids,))
    # 067c, the base's inputs. wealth_total: Table 2.2 block 0 (GBP million, April 2020 to March 2022) over the deciles, 'all' is Table 2.1 row 8 (GBP bn, as printed).
    t1 = sheet(WEALTH, 'Table 2.1')
    assert t1[7][1].startswith('Total Wealth (including Pr') and t1[28][1].startswith('Total Wealth (including Pr') and 'Aggregate' in t1[3][0] and 'Weighted' in t1[24][0]
    for d in range(1, 11):
        row('wealth_total', f'D{d}', round(at(0, [d]) / 1000, 3), 'gbp_bn', ())
    row('wealth_total', 'all', t1[7][-1], 'gbp_bn', ())
    # households: Table 2.1 row 29 (weighted frequency, total wealth including pensions); a decile holds a tenth of the households by definition, so D1 to D10 are
    # the printed total over ten (the tables print no count per decile). Adults are not in any held table by decile, so no adults rows (the guru's 067c question, answered).
    for b in [f'D{d}' for d in range(1, 11)] + ['all']:
        row('households', b, round(t1[28][-1] / 1000 / (1 if b == 'all' else 10), 1), 'thousand', ())
    # median house price: the ONS bulletin 'Housing affordability in England and Wales: 2025', England, year ending Sept 2025, all dwellings (GBP 300,000); checked against the PDF text.
    pdf = subprocess.run(['pdftotext', '-layout', str(ROOT / HOUSING), '-'], capture_output=True, text=True, check=True).stdout
    assert 'the median average home in England, at \u00a3300,000' in pdf
    add('wealth_distribution', (), variable='median_house_price', band='all', value='300000', unit='gbp', basis='adult', year='YE Sep 2025')
    # gdp: 'Total revenues' sheet, GDP column, GBP bn nominal, mean of financial years 2020-21 and 2021-22 (the survey's April 2020 to March 2022); income-year basis as the wealth rows.
    rv = sheet(REVENUE, 'Total revenues')
    g = {r[0]: r[6] for r in rv if r and r[0] in ('2020-21', '2021-22')}
    assert len(g) == 2 and all(isinstance(v, float) for v in g.values())
    row('gdp', 'all', round(sum(g.values()) / 2, 2), 'gbp_bn', ())


def tail():
    want = {'shweal_p99p100_992_j': ('wid_top1', 'I-W7a'), 'shweal_p90p100_992_j': ('wid_top10', 'I-W7b')}
    with open(ROOT / 'model_v2/wid_out/wid_long.csv', newline='', encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            if r['country'] == 'GB' and r['series_key'] in want and r['year'] in ('2000', '2010', '2024'):
                name, rid = want[r['series_key']]
                add('wealth_tail', (rid,) if r['year'] == '2024' else (), series=name, year=r['year'], value=txt(round(100 * float(r['value']), 1)), unit='pct_wealth', basis='adult')
    ROWS['wealth_tail'].sort(key=lambda r: (r[0], int(r[1])))


def receipts():
    t = sheet(REVENUE, '% GDP (cash)')
    c = t[2].index('2025-26')
    lines = zip('income_tax paye self_assessment nics vat corporation_tax fuel_duty cgt iht stamp_duties stamp_property stamp_shares business_rates council_tax total_hmrc total_current'.split(),
                [4, 6, 7, 8, 9, 10, 19, 20, 21, 22, 24, 25, 52, 53, 50, 57], 'abcdefghijklmnop')
    for line, r, k in lines:
        add('receipts', ('I-T3' + k,) + (('I-D7b',) if line == 'corporation_tax' else ()), line=line, fiscal_year='2025-26', pct_gdp=txt(round(100 * t[r - 1][c], 2)), basis='forecast')


def incidence():
    t = sheet(ETB, 'Table 2b')
    find = lambda lab, tb=t: next(r for r in tb if str(r[1]).startswith(lab) or str(r[0]).startswith(lab))[2:12]
    hh, gross, direct, indirect = (find(x) for x in ('Number of households', 'Gross income', 'Total direct', 'Total indirect'))
    row = lambda var, grp, tax, v, unit, ids, basis='equivalised_disposable': add('household_incidence', ids, variable=var, group=grp, tax=tax, value=txt(v), unit=unit, fiscal_year='2023-24', basis=basis)
    for d, c in enumerate('klmnopqrst'):
        row('total_tax', f'D{d + 1}', '', direct[d] + indirect[d], 'gbp_per_household_year', (f'I-H1{c}',))
        row('gross_income', f'D{d + 1}', '', gross[d], 'gbp_per_household_year', (f'I-H3{c}',))
    for tax, lab, ids in (('council_tax', 'Council Tax an', ('I-D6a', 'I-D6h')), ('business_rates', 'Commercial and', ('I-D6o', 'I-D6p'))):
        paid = [a * b for a, b in zip(find(lab), hh)]
        row('tax_share_top_decile', 'D10', tax, round(100 * paid[9] / sum(paid), 1), 'pct_of_tax', ids[:1])
        row('tax_share_bottom_five', 'D1-5', tax, round(100 * sum(paid[:5]) / sum(paid), 1), 'pct_of_tax', ids[1:])
    c = sheet(ETB, 'Table 2c')
    stamp = next(r for r in c if str(r[1]).startswith('Stamp Duty'))
    nh = next(r for r in c if str(r[1]).startswith('Number of households'))
    row('tax_share_top_decile', 'D10', 'stamp_property', round(100 * stamp[11] * nh[11] / (stamp[12] * nh[12]), 1), 'pct_of_tax', ('I-D6q',), 'original')
    t16 = next(r for r in sheet(ETB, 'Table 16') if str(r[0]).strip() == '2023/24')
    row('share_receiving_net_benefit', 'all', '', t16[1], 'pct_individuals', ('I-H2b',))


def write(name, rows):
    with open(OUT / name, 'w', newline='', encoding='utf-8') as fh:
        csv.writer(fh, lineterminator='\n').writerows([SCHEMA[name[:-4]].split()] + rows)


BUILT = '2026-11-18'
NOTES = 'Pack values are as published; the model expresses them in 2025-26 prices (base_year, stage C1).'
FROM = {'returns': ['model_v2/jst_r6.json'], 'wealth_distribution': [WEALTH, REVENUE, HOUSING], 'wealth_tail': ['model_v2/wid_out/wid_long.csv'], 'receipts': [REVENUE],
        'household_incidence': [ETB]}   # dataset -> the repo file it is read from; a dataset with no source file carries the build date


def added(path):
    """The day a source file entered the repository, following renames (the oldest add commit)."""
    out = subprocess.run(['git', 'log', '--follow', '--diff-filter=A', '--format=%as', '--', path], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    assert out, f'{path} is not in git history'
    return out[-1]


def retrieved(ds):
    return min(added(p) for p in FROM[ds]) if ds in FROM else BUILT


def main():
    (OUT / 'source').mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / 'model_v2' / 'jst_r6.json', OUT / 'source' / 'jst_r6.json')
    for f in (returns, wealth, tail, receipts, incidence):
        f()
    src = {'returns': ('JST Macrohistory R6, model_v2/jst_r6.json', 'cite-only', 'JST R6'), 'wealth_distribution': ('ONS WAS Round 8, totalwealthtables.xlsx Tables 2.1, 2.2; ONS Housing affordability 2025 (median price); IFS Revenue composition, Total revenues (GDP)', 'cite-only', 'WAS Round 8'),
           'wealth_tail': ('WID.world, model_v2/wid_out/wid_long.csv', 'cite-only', 'WID 2026-10-16'), 'receipts': ('IFS Revenue composition spreadsheet, % GDP (cash)', 'cite-only', 'EFO March 2023'),
           'household_incidence': ('ONS effects of taxes and benefits FYE 2024, Tables 2b, 2c, 16', 'ogl-v3', 'ETB FYE 2024'), 'tax_rules': ('none held', 'unverified', 'none'),
           'public_expenditure': ('none cited by the register', 'unverified', 'none')}
    files = []
    for ds in SCHEMA:
        write(ds + '.csv', ROWS[ds])
        files.append({'name': ds + '.csv', 'dataset': ds, 'sha256': hashlib.sha256((OUT / (ds + '.csv')).read_bytes()).hexdigest(), 'rows': len(ROWS[ds]),
                      'source': src[ds][0], 'licence': src[ds][1], 'retrieved': retrieved(ds), 'vintage': src[ds][2]})
    (OUT / 'manifest.json').write_text(json.dumps({'country': 'GBR', 'currency': 'GBP', 'base_year': '2025-26', 'pack_version': 1, 'built': BUILT,
                                                                       'notes': NOTES, 'files': files}, indent=1) + '\n', encoding='utf-8')
    (OUT / 'NOTICE.md').write_text('# GBR pack notice\n\nContains public sector information licensed under the Open Government Licence v3.0 (ONS). JST Macrohistory R6 is CC BY-NC-SA 4.0 '
                                   '(Jorda, Schularick and Taylor): cite only, non-commercial. IFS and WID rows are cite only. The pack stays a private input of the repo.\n\n'
                                   'Each file\'s `retrieved` date is the day its source file entered this repository (git history, renames followed); a file with no source file carries the build date.\n\n'
                                   'wealth_distribution.csv base rows (brief 067c): wealth_total D1 to D10 from totalwealthtables.xlsx Table 2.2 (block 1, last column, GBP million, over 1000) and all from Table 2.1 row 8; '
                                   'households from Table 2.1 row 29 (weighted frequency, 26,991,000), each decile the total divided by ten (a decile holds a tenth of households by definition; no table prints a count per decile); '
                                   'no adults rows (no held table gives adults by decile); median_house_price GBP 300,000 is England, year ending Sept 2025, all dwellings, from `Research/Housing affordability in England and Wales 2025.pdf` '
                                   '(the existing-dwelling median in `medianpricepaidforadministrativegeographiesexisting.xlsx` table 1a is GBP 297,000); gdp is the mean of financial years 2020-21 (2,085.204) and 2021-22 (2,337.757) '
                                   'GBP bn in `Revenue composition spreadsheet.xlsx` sheet Total revenues, column G, nominal as published. The file is cite only because the GDP series comes from the IFS spreadsheet.\n', encoding='utf-8')
    p = ROOT / 'model_v3' / 'levers.json'
    text, lev = p.read_text(encoding='utf-8'), json.loads(p.read_text(encoding='utf-8'))
    lev['pack_mappings'].update(x1_pointers=dict(sorted(POINTERS.items())), x1_skipped={i: why for why, ids in SKIP.items() for i in ids})
    cut = text.index(',\n  "pack_mappings"')
    p.write_text(text[:cut] + ',\n  "pack_mappings": ' + json.dumps(lev['pack_mappings'], indent=2).replace('\n', '\n  ') + '\n}\n', encoding='utf-8')


if __name__ == '__main__':
    main()
