"""103r block 1: merge the 101r (flows) and 102r (stocks) registers and crosswalks.

Reads the committed CSVs only. Writes parameter_register.csv, source_crosswalk.csv,
dictionary_map.csv (094r B2 terms -> register rows). Fails (exit 1) on:
 - a repeated variable name; a row without a classification; an unset row with a value;
 - a 094r dictionary term with no register row; a named existing register row with no row;
 - a pension row without exactly one stated basis.
Prints one summary line. Run from the repository root with python -I.
"""
import csv, re, sys, os
R = 'docs/research/data/'
OUT = R + '103r/'
fl = list(csv.DictReader(open(R + '101r/flows_register.csv')))
st = list(csv.DictReader(open(R + '102r/stocks_register.csv')))
fx = list(csv.DictReader(open(R + '101r/flows_crosswalk.csv')))
sx = list(csv.DictReader(open(R + '102r/stocks_crosswalk.csv')))
aud = list(csv.DictReader(open(R + '102r/existing_row_audit.csv')))

# Short unique names for the 102r rows (their register holds a long definition, not a name).
S_NAME = {
 'S01': 'Pack wealth bands (deciles of total wealth)', 'S02': 'Band-edge mapping, GBP bands against pack deciles',
 'S03': 'Stage weights by pack band (persons 16+)', 'S04': 'Cell sizes by pack band and stage',
 'S05': 'Asset composition by pack band (R8)', 'S06': 'Asset composition by age of household reference person (proxy for stage)',
 'S07': 'DB against DC pension split and pensions in payment', 'S08': 'Pension valuation basis for stock rows (WAS R8 SCAPE-based)',
 'S09': 'Physical (contents and vehicles) wealth share by band', 'S10': 'Secured debt (personal property debt), GB total and by age',
 'S11': 'Unsecured debt (personal financial debt), GB total and by age', 'S12': 'Aggregate liabilities cross-check, ONS 3222 against NBS AF.L',
 'S13': 'Debt service by band and stage', 'S14': 'Top-tail share series (WID)', 'S15': 'Top-tail adjustment for wealth missing from the WAS top',
 'S16': 'Capital transfers of households with other sectors (S.14)', 'S17': 'Gifts and inheritances by band and stage',
 'S18': 'Estates passing at death by size and composition', 'S19': 'Legacy heir rule (one heir, G = 30 years)',
 'S20': 'Two-year top-decile persistence and entry', 'S21': 'Four-year rank correlation and same-decile share',
 'S22': 'Band-to-band and stage transition matrix', 'S23': 'Age structure of the adult population', 'S24': 'Mortality, period qx and survival from 65',
 'S25': 'Working-to-retired transition hazard by band', 'S26': 'Household formation and dissolution', 'S27': 'Adults per household by pack band',
 'S28': 'Person weights by stage within band', 'S29': 'Audit I-D4a wealth to GDP', 'S30': 'Audit I-D4b, I-D4g, I-D4h adult base and adults per household',
 'S31': 'Audit I-W5a and I-W5e top-decile and pension shares', 'S32': 'Audit I-W5b to I-W5d tail shares against the pack tail',
 'S33': 'Audit I-W4a to I-W4f mobility rows'}

# Pension basis per row. ONS-NA = ONS national-accounts flow or stock series; WAS-R8 = WAS Round 8 SCAPE-based DB valuation (pack base);
# RF = Resolution Foundation basis (excludes DB; validation context only); '' = not a pension row.
BASIS = {'F-10': 'ONS-NA', 'F-11': 'ONS-NA', 'F-12': 'ONS-NA', 'F-13': 'ONS-NA', 'F-35': 'register of the three bases',
         'F-32': 'RF', 'F-34': 'RF', 'S05': 'WAS-R8', 'S06': 'WAS-R8', 'S07': 'WAS-R8', 'S08': 'WAS-R8', 'S29': 'WAS-R8', 'S31': 'WAS-R8',
         'S01': 'WAS-R8', 'F-03': 'ONS-NA', 'F-08': 'ONS-NA', 'F-09': 'ONS-NA', 'F-14': 'ONS-NA', 'F-24': 'ONS-NA', 'F-36': 'excludes pensions'}
ALLOWED = {'ONS-NA', 'WAS-R8', 'RF', 'excludes pensions', 'register of the three bases', ''}

# 094r B2 variable dictionary terms -> register rows. D-rows are added below for terms with no parameter row.
DICT = {
 'NW': ['S01', 'S05', 'S29'], 'A (H, E, B, M, PA)': ['S05', 'S06', 'S08', 'S09', 'F-20'], 'L = D': ['S10', 'S11', 'S12', 'S13'],
 'dNW': ['D02', 'F-23'], 'S': ['F-07', 'F-08', 'F-09', 'F-10', 'F-24'], 'Y_L': ['F-01', 'F-02'], 'Y_P': ['F-14', 'F-15', 'F-16'],
 'I_D': ['D04', 'S13'], 'T_C': ['F-03', 'F-04'], 'C': ['F-06', 'F-25'], 'K': ['F-11'], 'CG': ['F-18', 'F-20', 'F-22'],
 'TR': ['S16', 'S17', 'S18', 'S19'], 'O': ['F-21', 'F-23'], 'T_WDT': ['D01'], 'B, R': ['S13', 'D04'], 'y, g_h, r': ['F-17', 'F-18', 'F-19', 'F-26', 'F-27'],
 'r_f': ['D03'], 'Physical wealth (author decision 2026-11-21; not in the 094r dictionary)': ['S09']}
D_ROWS = [
 ('D01', 'T_WDT: WDT paid by the household, net of refund', 'T_WDT, uses', 'Endogenous', 'model output (kernel tax, refund and death flows); no parameter',
  'ruling not applicable: determined by the model, never a calibration target'),
 ('D02', 'dNW: change in net worth (the identity left-hand side)', 'dNW', 'Endogenous', 'model state change; reported residuals O and constraints F-23, F-24',
  'ruling not applicable: identity output'),
 ('D03', 'r_f: fund return', 'fund, public side', 'Endogenous', 'kernel and revenue code set r_f = g (same return path), optionally mixed with a safe return (register I-D14f); no pack row',
  'ruling not applicable here; a fund-rule matter outside the flow map'),
 ('D04', 'I_D: interest paid on household debt, and principal repayment R', 'I_D, uses; B and R swap M and D', 'Unset', 'no household interest series by band or stage; aggregate D.4 paid is in derived_ons_flows.csv (101r) and is not split into debt interest',
  'further data required (DR-06, DR-10 debt service)')]

def cls(c):
    c = c.strip()
    return c.split(' (')[0].split(',')[0].strip().lower()
def ruling_class(t):
    t = t.lower()
    for k, v in (('ready for implementation', 'ready'), ('implement with', 'scenario range'), ('further data required', 'further data'),
                 ('remain unset', 'unset'), ('remain as the legacy', 'legacy comparator'), ('report', 'audit (no ruling)'),
                 ('supports', 'audit (no ruling)'), ('remain a proxy', 'validation or proxy only'), ('ruling not applicable', 'not applicable (endogenous)')):
        if t.startswith(k): return v
    return 'UNMATCHED: ' + t[:40]

rows = []
for r in fl:
    rows.append(dict(row_id=r['id'], side='101r flows', group='', variable=r['variable'], definition=r['definition'], accounting_location=r['accounting_location'],
        target_cell_dimension=r['target_cell_dimension'], classification=r['classification'], source_reference=r['source_reference'],
        calculation_and_script=r['calculation_and_script'], value_or_range=r['value_or_range'], caveats=r['uncertainty_caveats'], intended_use=r['intended_use'],
        proposed_ruling=r['proposed_ruling'], relation_to_existing_row=r['relation_to_existing_row'], open_question_or_data_request=r['open_question_or_data_request']))
for r in st:
    rows.append(dict(row_id=r['id'], side='102r stocks', group=r['group'], variable=S_NAME[r['id']], definition=r['variable_and_definition'],
        accounting_location=r['accounting_location'], target_cell_dimension=r['target_cell_dimension'], classification=r['classification'],
        source_reference=r['source_and_exact_reference'], calculation_and_script=r['calculation_and_script'], value_or_range=r['value_or_range'],
        caveats=r['uncertainty_and_caveats'], intended_use=r['intended_model_use'], proposed_ruling=r['proposed_ruling'],
        relation_to_existing_row=r['relation_to_existing_row'], open_question_or_data_request=r['open_question_or_data_request']))
for rid, var, loc, c, why, rl in D_ROWS:
    rows.append(dict(row_id=rid, side='103r dictionary row', group='dictionary', variable=var, definition=var, accounting_location=loc, target_cell_dimension='none',
        classification=c, source_reference='docs/research/094r-kernel-map-and-household-accounts.md B2', calculation_and_script='none', value_or_range='',
        caveats=why, intended_use='none', proposed_ruling=rl, relation_to_existing_row='none', open_question_or_data_request=''))
for r in rows:
    r['class_norm'] = cls(r['classification'])
    r['ruling_class'] = ruling_class(r['proposed_ruling'])
    r['pension_basis'] = BASIS.get(r['row_id'], '')
    r['dictionary_terms'] = '; '.join(k for k, v in DICT.items() if r['row_id'] in v)

errs = []
names = [r['variable'].strip().lower() for r in rows]
for n in {n for n in names if names.count(n) > 1}: errs.append('repeated variable name: ' + n)
ids = [r['row_id'] for r in rows]
for i in {i for i in ids if ids.count(i) > 1}: errs.append('repeated id: ' + i)
for r in rows:
    if not r['classification'].strip(): errs.append('no classification: ' + r['row_id'])
    if r['class_norm'] == 'unset' and r['value_or_range'].strip(): errs.append('unset row carries a value: ' + r['row_id'])
    if r['ruling_class'].startswith('UNMATCHED'): errs.append('ruling not classed: %s %s' % (r['row_id'], r['ruling_class']))
# pension rows: any row whose text names pension must carry a basis (one stated)
for r in rows:
    txt = ' '.join([r['variable'], r['definition'], r['accounting_location']]).lower()
    if 'pension' in txt and not r['pension_basis'] and r['row_id'] not in ('S03', 'S04'):
        errs.append('pension row without a basis tag: ' + r['row_id'])
    if r['pension_basis'] not in ALLOWED: errs.append('basis not in the allowed set: ' + r['row_id'])
# dictionary coverage
idset = set(ids)
for t, v in DICT.items():
    miss = [i for i in v if i not in idset]
    if miss: errs.append('dictionary term %s names missing rows %s' % (t, miss))
    if not v: errs.append('dictionary term with no row: ' + t)
# every existing register row named in 101r and 102r has a merged row that names it
named = set()
for r in aud:
    named |= set(re.findall(r'I-[A-Z]\d+[a-z]?\d?', r['register_row']))
for r in fl + st:
    named |= set(re.findall(r'I-[A-Z]\d+[a-z]?\d?', r.get('variable', '') + ' ' + r.get('variable_and_definition', '') + ' ' + r.get('relation_to_existing_row', '')))
# ranges such as I-D4a to I-D4h, I-W3a to I-W3d expand over the letters
def expand(text):
    out = set(re.findall(r'I-[A-Z]\d+[a-z]?\d?', text))
    for m in re.finditer(r'(I-[A-Z]\d+)([a-z]) to (?:I-[A-Z]\d+)?([a-z])', text):
        for ch in range(ord(m.group(2)), ord(m.group(3)) + 1): out.add(m.group(1) + chr(ch))
    return out
alltext = ' '.join(' '.join(str(v) for v in r.values()) for r in rows)
have = expand(alltext)
missing_named = sorted(n for n in named if n not in have)
for n in missing_named: errs.append('existing register row named but absent from the merged register: ' + n)

# source crosswalk merge
xcols = ['source_id', 'side', 'source', 'exact_reference', 'publisher_and_link', 'reference_period', 'population_unit_frequency_price_basis',
         'definitions_and_coverage', 'dimensions_available', 'revisions_and_sampling_limits', 'held_file_checked_against_published_source', 'used_for_register_rows']
xrows = []
for r in fx:
    xrows.append(dict(source_id='A-' + r['source_id'], side='101r', source=r['file_or_table'], exact_reference=r['file_or_table'], publisher_and_link=r['publisher_and_link'],
        reference_period=r['reference_period'], population_unit_frequency_price_basis=r['population_unit_frequency_price_basis'],
        definitions_and_coverage=r['definitions_and_coverage'], dimensions_available=r['available_dimensions'], revisions_and_sampling_limits=r['revisions_and_limits'],
        held_file_checked_against_published_source=r['held_file_checked_against_published'], used_for_register_rows=r['used_for_register_rows']))
for r in sx:
    xrows.append(dict(source_id='B-' + r['id'], side='102r', source=r['source'], exact_reference=r['exact_reference'], publisher_and_link=r['publisher_and_link'],
        reference_period=r['reference_period'], population_unit_frequency_price_basis=r['population_unit_frequency_price_basis'],
        definitions_and_coverage=r['definitions_and_coverage'], dimensions_available=r['dimensions_available'], revisions_and_sampling_limits=r['revisions_and_sampling_limits'],
        held_file_checked_against_published_source=r['held_file_checked_against_published_source'], used_for_register_rows=''))
for r in xrows:
    for k in xcols:
        r.setdefault(k, '')

pcols = ['row_id', 'side', 'group', 'variable', 'definition', 'accounting_location', 'target_cell_dimension', 'classification', 'class_norm', 'source_reference',
         'calculation_and_script', 'value_or_range', 'caveats', 'intended_use', 'proposed_ruling', 'ruling_class', 'pension_basis', 'dictionary_terms',
         'relation_to_existing_row', 'open_question_or_data_request']
os.makedirs(OUT, exist_ok=True)
with open(OUT + 'parameter_register.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, pcols); w.writeheader(); w.writerows(rows)
with open(OUT + 'source_crosswalk.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, xcols); w.writeheader(); w.writerows(xrows)
with open(OUT + 'dictionary_map.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['094r_term', 'register_rows'])
    for t, v in DICT.items(): w.writerow([t, '; '.join(v)])
print('rows=%d (flows %d, stocks %d, dictionary %d) crosswalk=%d terms=%d named_existing_rows=%d failures=%d' %
      (len(rows), len(fl), len(st), len(D_ROWS), len(xrows), len(DICT), len(named), len(errs)))
for e in errs: print('FAIL', e)
sys.exit(1 if errs else 0)
