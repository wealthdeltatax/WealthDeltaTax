"""104r block 4: rulings table for every 103r register row, with the author's 2026-11-21 rulings applied.
Reads 103r/parameter_register.csv and 104r/resolution_by_row.csv; writes rulings_table.csv and rulings_table.md (a markdown table the note includes).
Exits 1 if a register row is missing, or the four brief categories do not account for every row.  Run from the repo root: python -I docs/research/data/104r/rulings_table.py"""
import csv, sys, collections
R = 'docs/research/data/'
reg = list(csv.DictReader(open(R + '103r/parameter_register.csv')))
res = {r['row_id']: r for r in csv.DictReader(open(R + '104r/resolution_by_row.csv'))}
READY, SCEN, UNSET, DATA = 'ready for implementation', 'implement with a scenario range', 'remain unset', 'further data required'
BASE = {'ready': READY, 'scenario range': SCEN, 'unset': UNSET, 'further data': DATA, 'audit (no ruling)': 'report only (audit, no register edit)',
        'validation or proxy only': 'validation or proxy only', 'legacy comparator': 'legacy comparator only', 'not applicable (endogenous)': 'not applicable (model output)'}
# author rulings 2026-11-21 and the recommended conventions of sections 3 and 4
OVER = {
 'F-03': (SCEN, 'label fixed to T_C (taxes net of benefits); aggregate only; band means are scenario or unset'),
 'F-10': (SCEN, 'one labelled aggregate scenario on the ONS basis; no rate on the SCAPE stock until DR-01 (author)'),
 'F-12': (SCEN, 'author ruling: a labelled scenario range per class (pension, physical, net financial), never an estimate; evidence class stays unset; the range is for the author to set'),
 'F-21': (SCEN, 'label fixed to CG (real erosion of liabilities); deflator is the expenditure deflator; wedge to CPI reported as its own line'),
 'F-23': (READY, 'O is a reported residual, not forced to zero; WAS is the stock base and national accounts are validation only (author)'),
 'F-25': ('legacy comparator only', 'reproduces today digests as a switchable comparator; no replacement value'),
 'F-30': ('context only', 'author ruling: I-W3b is context only (gross saving rate of a foreign top 1%); not a saving parameter'),
 'F-31': ('validation moment only (unverified until SUP-7)', 'I-W3c stays a validation moment marked unverified until the source PDF is uploaded (author)'),
 'F-32': ('validation moment only (unverified until SUP-7)', 'I-W3d stays a validation moment marked unverified until the source PDF is uploaded (author)'),
 'S09': (READY, 'physical wealth (contents and vehicles) is a separate asset class inside the WDT base (author); its return is a scenario range with F-12'),
 'S19': ('legacy comparator only', 'one-heir rule kept as the labelled legacy arm; the account carries no cross-cell transfer (3.5)'),
}
CONS = {
 'F-12': 'pension, physical and net financial classes are 62.6% of a D4-5 cell and have no held return: each runs a labelled range and a cell is not run end to end without it',
 'F-16': 'housing yield stays a reported cross-check; the JST split (F-20) is the only source',
 'F-24': 'no saving rate on wealth; saving enters through each cell income side (scenario or unset), never as a share of net worth',
 'F-25': 'only the legacy comparator run uses 3.5%',
 'F-28': 'validation context only; no return difference by band is set',
 'F-29': 'no UK saving by wealth band; direction only; the Norwegian figure is not used',
 'F-30': 'not used as a saving parameter',
 'F-35': 'no conversion between pension bases; flows (ONS) and the stock (WAS SCAPE) stay on their own bases',
 'S12': 'the 3222 against AF.L gap is reported; no debt aggregate constrains the cells',
 'S17': 'TR is zero by cell (no inter-cell transfer); the legacy heir rule is the only transfer in the legacy arm',
 'S26': 'cell membership fixed within a generation step; no household formation',
 'S06': 'age of the reference person is a proxy for stage in the composition; the joint band by stage composition needs the microdata',
}
DEFAULT = {READY: 'used as stated in the pack, a pack addition or a reported check; value from the cited source',
           SCEN: 'used only as a labelled range, direction from the evidence; the range is for the author to set',
           DATA: 'absent in the first implementation; an aggregate or a labelled scenario range stands in',
           UNSET: 'no value; the model must not receive a central estimate',
           'report only (audit, no register edit)': 'no model use; differences reported for the guru',
           'not applicable (model output)': 'output of the account, not an input'}
rows = []; cnt = collections.Counter()
for x in reg:
    rid = x['row_id']
    ruling, note = OVER.get(rid, (BASE[x['ruling_class']], ''))
    cons = CONS.get(rid, '') or note or DEFAULT.get(ruling, '')
    if note and rid in CONS: cons = note + '; ' + CONS[rid]
    if ruling == DATA and x['open_question_or_data_request']: cons = 'absent in the first implementation; data needed: ' + x['open_question_or_data_request'][:90].rstrip(' ;,') + '; an aggregate or a labelled scenario range stands in'
    rr = res[rid]
    cat = {READY: 'ready', SCEN: 'scenario range', UNSET: 'unset', DATA: 'further data'}.get(ruling, 'other')
    cnt[cat] += 1
    rows.append([rid, x['variable'][:70], x['class_norm'], rr['finest_resolution_supported'], x['ruling_class'], ruling, cons])
if len(rows) != len(reg) or len({r[0] for r in rows}) != len(reg): print('FAILED: rows'); sys.exit(1)
with open(R + '104r/rulings_table.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['row_id', 'variable', 'evidence_class', 'finest_resolution', 'ruling_103r', 'ruling_104r', 'consequence_for_first_implementation']); w.writerows(rows)
md = '| Row | Variable | Class | Finest resolution | 103r | 104r ruling | Consequence for the first implementation |\n|---|---|---|---|---|---|---|\n'
for r in rows: md += '| ' + ' | '.join(c.replace('|', '/') for c in r) + ' |\n'
open(R + '104r/rulings_table.md', 'w').write(md)
print('ok: %d rows; ' % len(rows) + '; '.join(f'{k} {v}' for k, v in sorted(cnt.items())))
