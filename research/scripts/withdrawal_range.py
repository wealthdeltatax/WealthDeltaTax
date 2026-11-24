"""145r block 1: pension withdrawal evidence and the proposed labelled range, from held sources only.
Reads literature/BN236.pdf (IFS BN236, Crawford 2018; checked by pdftotext, every figure asserted on its page) and the ONS WAS R8 xlsx (Table_1).
Writes withdrawal_range.csv. Prints one line; exits 1 on any failed check. Run from the repo root: python -I research/scripts/withdrawal_range.py
Printed page = PDF page - 1 (asserted on the pages used). Rates are scenario inputs for the author, not forecasts; there is no central value."""
import csv, re, subprocess, sys
import openpyxl
OUT = 'research/tables/145r-saving-shapes-and-withdrawal-range/'
PDF = 'literature/BN236.pdf'
XL = 'data/uk-wealth-tables/098r/meanmedianaggregateandpercentageofwealthbywealthcomponentandageofhouseholdreferenceperson.xlsx'   # was the 129r copy, byte-identical, removed (044c R4)
def page(p):
    t = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), '-layout', PDF, '-'], capture_output=True, text=True).stdout
    return re.sub(r'\s+', '', t)          # the extraction splits words ("surv ey"); numbers are matched with spaces removed
fails = []
def need(pdfp, *strs):
    t = page(pdfp)
    for s in strs:
        if re.sub(r'\s+', '', s) not in t: fails.append(f'pdf p{pdfp}: {s!r} not found')
for p in (12, 13, 14):                    # printed page numbers are PDF - 1
    m = re.search(r'(\d+)©InstituteforFiscalStudies|©InstituteforFiscalStudies(\d+)', page(p))
    if not m or int(m.group(1) or m.group(2)) != p - 1: fails.append(f'printed page offset not confirmed on pdf p{p}')
need(3, 'declined by 14%', 'declined by just 1%', 'it declined by 13%', '17% between ages 70 and 80', '31%', '39% on average', '13%')
need(12, 'wealth declines by 1.8%', 'decline in wealth of 3.7% and an increase in wealth of 0.1%', 'the rate at which wealth changes is the same at all ages')
need(13, '9% between ages 70 and 75', '17% between ages 70 and 80', '24% between ages 70 and 85', '31% between ages 70 and 90')
need(14, '0.7% per year', '2.9% to an increase of 1.6%', '2.4% per', '4.1% to a decline of 0.8%', '39% between ages 70 and 90', '13%')
need(16, 'Age has little systematic association')
need(7, 'Net financial wealth is defined as total savings')
need(21, 'pension freedoms', 'may be very different')
wb = openpyxl.load_workbook(XL, data_only=True); ws = wb['Table_1']
hdr = None; pen = {}
for row in ws.iter_rows():
    v = [c.value for c in row]
    if isinstance(v[0], str) and v[0].strip() in ('55 to 64', '65 to 74', '75+'):
        pen[v[0].strip()] = (row[0].row, v[8], v[10])   # mean (GBP) and aggregate (GBP m) of private pension wealth
hdr = [c.value for c in ws[ws.min_row]]  # header rows are located by label below
labels = {}
for row in ws.iter_rows():
    for c in row:
        if isinstance(c.value, str) and c.value.strip() == 'Private pension wealth': labels['pension_col_start'] = c.column_letter
col_mean = openpyxl.utils.get_column_letter(9); col_agg = openpyxl.utils.get_column_letter(11)
if labels.get('pension_col_start') not in ('H', 'I', 'J'): fails.append('pension column block not where expected')
exp = {'55 to 64': 302800, '65 to 74': 250900, '75+': 113900}
for k, v in exp.items():
    if pen.get(k, (0, 0))[1] != v: fails.append(f'xlsx {k}: {pen.get(k)} != {v}')
r64, r74, r75 = (pen[k][1] for k in ('55 to 64', '65 to 74', '75+'))
ratio1, ratio2 = r74 / r64, r75 / r74
HDR = ['row_id', 'kind', 'item', 'value', 'unit', 'source', 'page_printed', 'flag', 'evidence_class', 'note_or_challenge']
rows = []
def add(*a): rows.append(list(a))
B = 'IFS BN236 (Crawford 2018), ELSA 2002-03 to 2014-15, England, net financial wealth'
add('W-P01', 'published', 'median real net financial wealth change over 12 years, born 1930-34 (aged 69 to 81)', -14, '%', B, '2', 'text', 'derived', 'a decline of a stock, not a withdrawal rate; financial wealth excludes pensions (p.6)')
add('W-P02', 'published', 'same, born 1925-29 (aged 74 to 86)', -13, '%', B, '2', 'text', 'derived', '')
add('W-P03', 'published', 'same, born 1920-24 (aged 79 to 91)', -1, '%', B, '2', 'text', 'derived', 'samples 537, 320, 133 (p.8, Figure 3 note)')
add('W-P04', 'published', 'estimated change in real net financial wealth per year of age, all', -1.8, '% per year', B, '11', 'text', 'derived', '95% CI -3.7 to +0.1; assumes the rate is the same at all ages and for all generations (p.11)')
add('W-P05', 'published', 'cumulated from age 70: to 75, 80, 85, 90', '9; 17; 24; 31', '% of age-70 wealth', B, '12', 'text', 'derived', 'the note says this likely overstates drawdown for those who survive to old age (p.12)')
add('W-P06', 'published', 'bottom half of wealth distribution (within cohort): change per year', -0.7, '% per year', B, '13', 'text', 'derived', '95% CI -2.9 to +1.6; cumulated 13% by 90')
add('W-P07', 'published', 'top half: change per year', -2.4, '% per year', B, '13', 'text', 'derived', '95% CI -4.1 to -0.8; cumulated 39% by 90; halves by six-year average wealth')
add('W-P08', 'published', 'age has little systematic association with the rate of drawdown once other characteristics are held constant', 'qualitative', '', B, '15', 'text', 'derived', 'supports one rate per stage, no age profile inside it')
add('W-P09', 'published', 'pension freedoms: results do not imply pension savings are held as financial wealth is; behaviour for pension wealth may be very different', 'qualitative', '', B, '20', 'text', 'derived', 'the source itself limits the transfer to pension wealth')
X = 'ONS WAS Round 8 (Apr 2020 to Mar 2022), Table_1, mean private pension wealth by age of household reference person'
add('W-P10', 'published', 'mean private pension wealth, HRP 55 to 64', r64, 'GBP', X, 'Table_1', 'table', 'derived', f'cell row {pen["55 to 64"][0]}, column {col_mean}; SCAPE basis (R8 method, not comparable with earlier rounds)')
add('W-P11', 'published', 'mean private pension wealth, HRP 65 to 74', r74, 'GBP', X, 'Table_1', 'table', 'derived', f'row {pen["65 to 74"][0]}')
add('W-P12', 'published', 'mean private pension wealth, HRP 75+', r75, 'GBP', X, 'Table_1', 'table', 'derived', f'row {pen["75+"][0]}')
add('W-C01', 'context', 'ratio of mean pension wealth 65-74 to 55-64, and 75+ to 65-74', f'{ratio1:.3f}; {ratio2:.3f}', 'ratio', X, 'Table_1', 'table', 'unset', 'a cross-section, not a rate: mixes cohorts, mortality selection, DB annuity values that fall mechanically with age, and SCAPE discounting; not used as a withdrawal rate')
# proposed range, retired stage, by wealth half; the pack bands D1-3 and D4-5 are the bottom half, D6-7, D8-9 and D10 the top half
P = 'proposed (scenario; not a forecast; no central value)'
RB = 'D1-3, D4-5 (bottom half)'; RT = 'D6-7, D8-9, D10 (top half)'
add('W-S01', 'proposed', f'retired stage, {RB}: low', 0.0, '% of opening pension balance per year, real', P, '', 'derived from W-P06', 'scenario', 'floor at zero, not evidence: the CI of W-P06 reaches an increase of 1.6, and the model draw cannot be negative')
add('W-S02', 'proposed', f'retired stage, {RB}: mid', 0.7, '% per year', P, '13', 'text', 'proxy', 'a point estimate for a different asset (financial wealth), a labelled mid, not a central estimate')
add('W-S03', 'proposed', f'retired stage, {RB}: high', 2.9, '% per year', P, '13', 'text', 'proxy', 'edge of the 95% CI of W-P06')
add('W-S04', 'proposed', f'retired stage, {RT}: low', 0.8, '% per year', P, '13', 'text', 'proxy', 'edge of the 95% CI of W-P07')
add('W-S05', 'proposed', f'retired stage, {RT}: mid', 2.4, '% per year', P, '13', 'text', 'proxy', 'wealthier faster, as the source says; point estimate for financial wealth; D10 has no separate figure, the top-half rate is a proxy for lack of one')
add('W-S06', 'proposed', f'retired stage, {RT}: high', 4.1, '% per year', P, '13', 'text', 'proxy', 'edge of the 95% CI of W-P07')
add('W-U01', 'unset', 'not retired stage, every band', '', '', '', '', '', 'unset', 'no held rate for draws before retirement (pension freedoms allow access from 55; no figure held); a model default of zero is a modelling choice, not evidence')
add('W-U02', 'unset', 'top 1% and the tail', '', '', '', '', '', 'unset', 'no rate by tail line in any held source')
add('W-U03', 'unset', 'gross withdrawal from a pension, by type (DB in payment, DC drawdown, annuity)', '', '', '', '', '', 'unset', 'ELSA here is the net change in financial wealth; no split by pension type is held (129r)')
add('W-U04', 'unset', 'behaviour after pension freedoms (2015)', '', '', '', '', '', 'unset', 'the ELSA window ends 2014-15; later waves are not held (data request, UKDS end-user licence)')
add('W-U05', 'unset', 'a rate by age inside the retired stage', '', '', '', '', '', 'unset', 'the model stage is economic status, not age; the source finds little age gradient (W-P08)')
with open(OUT + 'withdrawal_range.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(HDR); w.writerows(rows)
if fails:
    print('FAILED:', *fails, sep='\n'); sys.exit(1)
print(f'ok: {len(rows)} rows; every BN236 figure found on its page; pension ratios {ratio1:.3f}, {ratio2:.3f}')
