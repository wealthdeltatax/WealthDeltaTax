"""112r: composition of net wealth by WAS Round 8 decile (Table 2.2), to size the within-band gradient a payer line would ignore under band shares.
Run: python -I model/studies/kernel-wiring/decile_composition.py   (reads data/rates/totalwealthtables.xlsx; writes decile_composition.csv beside this file)
Pension is private pension wealth on the ONS SCAPE-based WAS basis. Prints one summary line."""
import csv, os
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
DATA = os.path.join(ROOT, 'results', 'kernel-wiring')   # outputs stay here until 163c
ws = list(openpyxl.load_workbook(os.path.join(ROOT, 'data/rates', 'totalwealthtables.xlsx'), data_only=True, read_only=True)['Table 2.2'].iter_rows(values_only=True))
col = lambda r0: [float(ws[r0 - 1 + k][10]) for k in range(10)]          # R8 is the last column; rows 4, 14, 24, 34, 44 start each block of ten deciles
tot, prop, fin, phys, pen = col(4), col(14), col(24), col(34), col(44)
BAND = {1: 'D1-3', 2: 'D1-3', 3: 'D1-3', 4: 'D4-5', 5: 'D4-5', 6: 'D6-7', 7: 'D6-7', 8: 'D8-9', 9: 'D8-9', 10: 'D10'}
rows = []
for k in range(10):
    assert abs(prop[k] + fin[k] + phys[k] + pen[k] - tot[k]) <= 5, k            # identity to rounding (GBP m)
    rows.append(dict(decile=f'D{k+1}', band=BAND[k + 1], property_pct=round(100 * prop[k] / tot[k], 2), net_financial_pct=round(100 * fin[k] / tot[k], 2),
                     physical_pct=round(100 * phys[k] / tot[k], 2), pension_pct=round(100 * pen[k] / tot[k], 2)))
with open(os.path.join(DATA, 'decile_composition.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
gap = max(abs(a[c] - b[c]) for a, b in zip(rows[3::2], rows[4::2]) for c in ('property_pct', 'net_financial_pct', 'physical_pct', 'pension_pct'))
print(f'10 deciles written; largest class-share gap between the two deciles of one band (D4/D5, D6/D7, D8/D9): {gap:.2f} pp')
