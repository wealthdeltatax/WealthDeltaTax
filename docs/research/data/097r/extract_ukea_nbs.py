"""097r follow-up: extract household (S.14) series from the ONS UK Economic Accounts workbook and the ONS
National Balance Sheet CSV, as tidy text. Run: python -I extract_ukea_nbs.py [UKEA_XLSX]
UKEA_XLSX defaults to /home/claude/held-097r/ukea2026q2.xlsx (11.7 MB, kept out of git); nbs.csv is read from this folder.
Needs openpyxl. Annual rows only (the first table on each UKEA sheet); 1997 onward. Nothing is derived or inferred."""
import csv, re, sys, warnings
from pathlib import Path
import openpyxl
warnings.filterwarnings('ignore')
HERE = Path(__file__).resolve().parent
UKEA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/home/claude/held-097r/ukea2026q2.xlsx')
RETR = '2026-11-21'
LINK_UKEA = 'https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/unitedkingdomeconomicaccounts'
LINK_NBS = 'https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/nationalbalancesheet'
HEAD = ['series_id', 'period', 'value', 'unit', 'price_basis', 'seasonal_adjustment', 'sector', 'sign_convention',
        'source_link', 'retrieval_date', 'definition', 'esa_code', 'side', 'table']
# sheet -> (sector, label). 6.1.x sheets are households and NPISH together (S.14+S.15).
SHEETS = {'6.2.3': 'S.14', '6.2.4': 'S.14', '6.2.5': 'S.14', '6.2.6_A': 'S.14', '6.2.6_B': 'S.14',
          '6.2.7': 'S.14', '6.1.9': 'S.14+S.15', '6.1.10': 'S.14+S.15'}
YEAR = re.compile(r'^(19|20)\d\d$')


def ukea():
    wb = openpyxl.load_workbook(UKEA, read_only=True)
    out = []
    for sh, sector in SHEETS.items():
        rows = list(wb[sh].iter_rows(values_only=True))
        hi = next(i for i, r in enumerate(rows) if r and r[0] and str(r[0]).startswith('Time period and dataset code'))
        ii = next(i for i in range(hi, hi + 8) if rows[i][0] and str(rows[i][0]).startswith('Dataset identifier'))
        names, ids = rows[hi], rows[ii]
        esa = next(r for r in rows[hi + 1:ii] if str(r[0]).startswith('ESA code'))
        side = next((r for r in rows[hi + 1:ii] if r[0] and not str(r[0]).startswith('ESA code')), None)
        got = False
        for r in rows[ii + 1:]:
            if not (r and r[0] is not None and YEAR.match(str(r[0]).strip())):
                if got:
                    break
                continue
            got = True
            yr = int(str(r[0]).strip())
            if yr < 1997:
                continue
            for j in range(1, len(r)):
                if r[j] in (None, '') or not ids[j]:
                    continue
                try:
                    v = float(r[j])
                except (TypeError, ValueError):
                    continue
                sd = str(side[j] or '').strip() if side else ''
                sign = {'resources': 'resource_positive', 'uses': 'use_positive'}.get(sd.lower(), 'as_published')
                nm = re.sub(r'\s*\[note \d+\]', '', str(names[j])).replace('\n', ' ').strip()
                out.append([ids[j], yr, int(v) if v == int(v) else v, '£m', 'current price', 'NSA', sector, sign,
                            LINK_UKEA, RETR, nm, esa[j] or '', sd.lower(), sh])
    return out


def write(path, rows):
    with open(HERE / path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(HEAD)
        w.writerows(rows)
    print(path, len(rows), 'rows,', len({r[0] for r in rows}), 'series')


def nbs():
    rows = list(csv.reader(open(HERE / 'nbs.csv', encoding='utf-8')))
    titles, cdid = rows[0], rows[1]
    data = [r for r in rows if r and YEAR.match(r[0])]
    out = []
    for j in range(1, len(titles)):
        m = re.match(r'Balance Sheet: (S\.14|S\.1HN): LE: ([A-Z]{1,2}\.[0-9A-Z.]+): (.+): (CP|CVM): (NSA|SA): £m$', titles[j])
        if not m:
            continue
        sector, code, name = m.group(1), m.group(2), m.group(3)
        for r in data:
            if int(r[0]) < 1997 or j >= len(r) or r[j].strip() in ('', '..'):
                continue
            v = float(r[j])
            out.append([cdid[j], int(r[0]), int(v) if v == int(v) else v, '£m', 'current price', 'NSA',
                        'S.14' if sector == 'S.14' else 'S.14+S.15', 'net_assets_positive', LINK_NBS, RETR,
                        f'{name} ({code}), end-year stock', code, 'stock', 'nbs.csv'])
    return out


if __name__ == '__main__':
    write('ons_ukea_household_annual.csv', ukea())
    write('ons_nbs_household_stocks_annual.csv', nbs())
