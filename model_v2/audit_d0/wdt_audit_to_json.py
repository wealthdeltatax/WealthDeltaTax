"""wdt_audit_to_json.py - collect the WDT data-audit CSV files into one JSON file.

Usage:
  python wdt_audit_to_json.py [--dir DIR] [--out FILE] [--no-coerce]
                              [--usable-years FILE] [--strict] [--selftest]

Reads (all optional; whatever is found in DIR is used):
  coverage_matrix_d*.csv   one row per candidate source per dataset (D0..D9)
  d1_overlap_runs.csv      D1 run-level overlap with candidate wealth series
  uk_holder_shares_ons.csv UK ONS holder shares (D4 series values)
  --usable-years FILE      JST usable_years.csv from d0_jst_audit.py (compacted to runs)
  any other *.csv in DIR is added under "tables" using its file stem.

Output JSON layout:
  {"meta": {...},
   "coverage": {"D1": {"columns": [...], "rows": [...]}, ...},
   "tables":   {"<stem>": {"columns": [...], "rows": [...]}},
   "usable_years": {"<set>": {"<ISO>": {"n": int, "runs": [{"run_id","first","last","n"}]}}},
   "warnings": [...]}

Values: empty string -> null; integers and decimals -> numbers (unless --no-coerce);
everything else stays a string. Year-like strings with notes (e.g. "2022 (2024 edition
exists)") stay strings. Ragged rows (too few or too many fields) are reported in
"warnings"; with --strict they abort the run. Standard library only.
"""
import argparse, csv, glob, json, os, re, sys, tempfile
from datetime import datetime, timezone

NUM = re.compile(r'^-?(0|[1-9]\d*)(\.\d+)?$')

def coerce(v, on=True):
    if v is None:
        return None
    v = v.strip()
    if v == '':
        return None
    if on and NUM.match(v):
        return float(v) if '.' in v else int(v)
    if on and v in ('True', 'False'):
        return v == 'True'
    return v

def read_csv(path, coerce_on, warnings):
    rows, cols = [], []
    with open(path, newline='', encoding='utf-8-sig') as f:
        rd = csv.reader(f)
        try:
            cols = [c.strip() for c in next(rd)]
        except StopIteration:
            warnings.append(f'{os.path.basename(path)}: empty file')
            return cols, rows
        for i, rec in enumerate(rd, start=2):
            if not rec or all(c.strip() == '' for c in rec):
                continue
            if len(rec) != len(cols):
                warnings.append(f'{os.path.basename(path)} line {i}: {len(rec)} fields, expected {len(cols)}')
                rec = (rec + [''] * len(cols))[:len(cols)] if len(rec) < len(cols) else rec[:len(cols)]
            rows.append({c: coerce(v, coerce_on) for c, v in zip(cols, rec)})
    return cols, rows

def compact_usable(path, warnings):
    out = {}
    with open(path, newline='', encoding='utf-8-sig') as f:
        runs = {}
        for r in csv.DictReader(f):
            try:
                k = (r['set'], r['country'], int(r['run_id']))
                y = int(r['year'])
            except (KeyError, ValueError) as e:
                warnings.append(f'{os.path.basename(path)}: bad row {r} ({e})')
                continue
            a = runs.setdefault(k, [y, y, 0, int(r.get('run_len') or 0)])
            a[0] = min(a[0], y); a[1] = max(a[1], y); a[2] += 1
    for (s, c, rid), (a, b, n, ln) in sorted(runs.items()):
        d = out.setdefault(s, {}).setdefault(c, {'n': 0, 'runs': []})
        d['n'] += n
        d['runs'].append({'run_id': rid, 'first': a, 'last': b, 'n': n})
        if ln and ln != n:
            warnings.append(f'usable_years {s} {c} run {rid}: run_len {ln} != rows {n}')
    return out

def build(dir_, coerce_on=True, usable=None, strict=False):
    warnings, coverage, tables = [], {}, {}
    files = sorted(glob.glob(os.path.join(dir_, '*.csv')))
    used = []
    for p in files:
        name = os.path.basename(p)
        stem = name[:-4]
        if name == 'usable_years.csv':
            continue  # handled via --usable-years (large)
        m = re.fullmatch(r'coverage_matrix_(d\d+)', stem, re.I)
        cols, rows = read_csv(p, coerce_on, warnings)
        used.append(name)
        if m:
            coverage[m.group(1).upper()] = {'columns': cols, 'rows': rows}
        else:
            tables[stem] = {'columns': cols, 'rows': rows}
    if strict and warnings:
        raise SystemExit('strict: ' + '; '.join(warnings))
    doc = {
        'meta': {
            'generated_utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'source_dir': os.path.abspath(dir_),
            'files': used,
            'row_counts': {**{k: len(v['rows']) for k, v in coverage.items()},
                           **{k: len(v['rows']) for k, v in tables.items()}},
            'coerce_numbers': coerce_on,
            'note': 'Provenance, grades and verification status are in the provenance registers (.md); this file holds the CSV content only.',
        },
        'coverage': dict(sorted(coverage.items(), key=lambda kv: int(kv[0][1:]))),
        'tables': tables,
    }
    if usable:
        doc['usable_years'] = compact_usable(usable, warnings)
        doc['meta']['files'].append(os.path.basename(usable))
    doc['warnings'] = warnings
    return doc

def selftest():
    with tempfile.TemporaryDirectory() as d:
        open(os.path.join(d, 'coverage_matrix_d1.csv'), 'w').write(
            'country,first,last,note\nAUS,1960,2019,"a, b"\nBEL,,,none\nGBR,1855,2018 (x),ok\nBAD,1\n')
        open(os.path.join(d, 'other.csv'), 'w').write('year,v\n1963,54.0\n1969,47.4\n')
        open(os.path.join(d, 'usable_years.csv'), 'w').write(
            'country,set,year,run_id,run_len,flagged\nAUS,BASE,1902,1,2,False\nAUS,BASE,1903,1,2,False\nAUS,BASE,1948,2,1,False\n')
        doc = build(d, usable=os.path.join(d, 'usable_years.csv'))
        r = doc['coverage']['D1']['rows']
        assert r[0] == {'country': 'AUS', 'first': 1960, 'last': 2019, 'note': 'a, b'}
        assert r[1]['first'] is None and r[2]['last'] == '2018 (x)'
        assert any('line 5' in w for w in doc['warnings'])
        assert doc['tables']['other']['rows'][0] == {'year': 1963, 'v': 54.0}
        assert doc['usable_years']['BASE']['AUS'] == {'n': 3, 'runs': [
            {'run_id': 1, 'first': 1902, 'last': 1903, 'n': 2}, {'run_id': 2, 'first': 1948, 'last': 1948, 'n': 1}]}
        assert 'usable_years.csv' in doc['meta']['files'] and 'other.csv' in doc['meta']['files']
        d2 = build(d, coerce_on=False)
        assert d2['coverage']['D1']['rows'][0]['first'] == '1960'
        try:
            build(d, strict=True); raise AssertionError('strict should fail')
        except SystemExit:
            pass
    print('wdt_audit_to_json self-test ok')

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dir', default='.')
    ap.add_argument('--out', default='wdt_audit.json')
    ap.add_argument('--no-coerce', action='store_true')
    ap.add_argument('--usable-years')
    ap.add_argument('--strict', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    doc = build(a.dir, not a.no_coerce, a.usable_years, a.strict)
    with open(a.out, 'w', encoding='utf-8') as f:
        json.dump(doc, f, indent=1, ensure_ascii=False)
    m = doc['meta']
    print(f"wrote {a.out}: {len(m['files'])} files, rows {m['row_counts']}")
    for w in doc['warnings']:
        print('warning:', w, file=sys.stderr)

if __name__ == '__main__':
    main()
