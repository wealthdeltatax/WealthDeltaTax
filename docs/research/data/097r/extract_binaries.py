"""097r: extract what the author-uploaded binaries contain, as text. Run: python -I extract_binaries.py [NMG_DIR]
Reads quarterlysectoraccounts2026q2.xlsx and the HMRC .ods files from this folder; the two Bank of England NMG
workbooks (80 MB and 7 MB, kept out of git) from NMG_DIR (default /home/claude/held-097r). Needs openpyxl, pandas, odfpy."""
import csv, re, sys, warnings
from pathlib import Path
import openpyxl, pandas as pd
warnings.filterwarnings('ignore')
HERE = Path(__file__).resolve().parent
NMG = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/home/claude/held-097r')
RETR = '2026-11-21'

def qsa():
    wb = openpyxl.load_workbook(HERE / 'quarterlysectoraccounts2026q2.xlsx', read_only=True)
    out = []
    for sh in ('HH_1', 'HH_2', 'HH_3', 'HH_Alt'):
        rows = list(wb[sh].iter_rows(values_only=True))
        hi = next(i for i, r in enumerate(rows) if r and r[0] and str(r[0]).startswith('Time period column'))
        idj = next(j for j in range(hi + 1, hi + 6) if rows[j][0] and 'Dataset identifier' in str(rows[j][0]))
        titles, esa, ids = rows[hi], rows[hi + 1], rows[idj]
        for r in rows[idj + 1:]:
            if not isinstance(r[0], int): break           # annual table 1 only
            for c in range(1, len(titles)):
                if r[c] in ('', None): continue
                t = ' '.join(str(titles[c]).split())
                pct = 'ratio' in t.lower() or 'percentage' in t.lower()
                out.append([sh, ids[c], t, esa[c] or '', r[0], r[c], 'percent' if pct else 'GBP million (see title)',
                            'chained volume' if 'chained' in t.lower() else 'current prices',
                            'NSA' if sh == 'HH_Alt' else 'as published on sheet', 'S.14 households',
                            'quarterlysectoraccounts2026q2.xlsx (ONS QSA, release 30 Sep 2026)', RETR])
    with open(HERE / 'qsa_household_annual_2026q2.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['sheet', 'series_id', 'series_title', 'esa_code', 'period', 'value', 'unit', 'price_basis',
                    'seasonal_adjustment', 'sector', 'source_file', 'retrieval_date'])
        w.writerows(out)
    print('qsa rows', len(out))

def hmrc():
    d = HERE / 'hmrc_csv'; d.mkdir(exist_ok=True)
    for f in sorted(HERE.glob('*.ods')):
        x = pd.ExcelFile(f, engine='odf')
        for s in x.sheet_names:
            if s.startswith(('Notes', 'Guidance', 'Contents', 'Cover', 'Footnotes')) and 'Table' not in s: continue
            df = x.parse(s, header=None)
            safe = re.sub(r'[^A-Za-z0-9_.-]+', '_', s)[:60]
            df.to_csv(d / f'{f.stem}__{safe}.csv', index=False, header=False)
    print('hmrc csv', len(list(d.glob('*.csv'))))

def nmg():
    p = NMG / 'boe-nmg-household-survey-data.xlsx'                     # 2011-2026 (the 2004-11 file lists variables by number: read its 'Data descriptions' sheet by hand)
    if not p.exists(): print('missing', p); return
    wb = openpyxl.load_workbook(p, read_only=True)
    sheets = [ws.title for ws in wb.worksheets]
    n = 0
    with open(HERE / 'nmg_variable_inventory_2011_2026.csv', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['variable', 'label'])
        for r in wb['Data description'].iter_rows(values_only=True):
            c = next((str(x) for x in r if x is not None), '')
            m = re.match(r'^([A-Za-z0-9_]+) - (.*)$', c, re.S)
            if m: w.writerow([m.group(1), ' '.join(m.group(2).split())[:300]]); n += 1
    print('sheets', len(sheets), 'variables', n)

if __name__ == '__main__':
    qsa(); hmrc(); nmg()
