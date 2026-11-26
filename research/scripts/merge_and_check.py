"""103r block 1: merge the 101r (flows) and 102r (stocks) registers and crosswalks.

Reads the committed CSVs only. Writes parameter_register.csv, source_crosswalk.csv,
dictionary_map.csv (094r B2 terms -> register rows). Fails (exit 1) on:
 - a repeated variable name; a row without a classification; an unset row with a value;
 - a 094r dictionary term with no register row; a named existing register row with no row;
 - a pension row without exactly one stated basis.
Prints one summary line. Run from the repository root with python -I.
"""
import csv, re, sys, os
DIRS = {'101r': 'research/tables/101r-parameter-map-flows-and-returns/', '102r': 'research/tables/102r-parameter-map-stocks-and-cells/', '103r': 'research/tables/103r-parameter-map-assembly/'}   # 160c: the tables moved here (project/restructure map)
OUT = DIRS['103r']
fl = list(csv.DictReader(open(DIRS['101r'] + 'flows_register.csv')))
st = list(csv.DictReader(open(DIRS['102r'] + 'stocks_register.csv')))
fx = list(csv.DictReader(open(DIRS['101r'] + 'flows_crosswalk.csv')))
sx = list(csv.DictReader(open(DIRS['102r'] + 'stocks_crosswalk.csv')))
aud = list(csv.DictReader(open(DIRS['102r'] + 'existing_row_audit.csv')))

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

# Cross-side flags found by cross_side_checks.py (labels only; no value or row text is edited here).
FLAGS = {
 'F-03': 'C03: labelled TR; in 094r B2 benefits sit in T_C net of benefits and TR is net capital transfers',
 'F-21': 'C03: labelled O; in 094r B2 the real revaluation of nominal positions is a CG term',
 'F-06': 'C05: P.31 includes owners imputed rent (ONS), so imputed rent nets out of S',
 'F-10': 'C01/C02: ONS national-accounts basis; the stock rows are on the WAS R8 SCAPE basis; not convertible (DR-01)',
 'F-12': 'C01/C02: as F-10', 'F-13': 'C01/C02: as F-10', 'F-23': 'C06: O outside 1% of opening NW in 2020 and 2021 (non-financial revaluation not held, DR-05)',
 'S08': 'C01/C02: stock basis differs from the flow rows F-10 to F-13',
 'S09': 'not in the 094r asset list A (H, E, B, M, PA); author ruling 2026-11-21 puts it in the base',
 'S12': 'C09: ONS 3222 total is 0.69 of NBS AF.L (2021); coverage',
 'S05': 'C05: property class returns exist (F-20); financial, pension and physical classes cannot be run'}
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
        classification=c, source_reference='research/notes/094r-kernel-map-and-household-accounts.md B2', calculation_and_script='none', value_or_range='',
        caveats=why, intended_use='none', proposed_ruling=rl, relation_to_existing_row='none', open_question_or_data_request=''))
for r in rows:
    r['class_norm'] = cls(r['classification'])
    r['ruling_class'] = ruling_class(r['proposed_ruling'])
    r['pension_basis'] = BASIS.get(r['row_id'], '')
    r['dictionary_terms'] = '; '.join(k for k, v in DICT.items() if r['row_id'] in v)
    r['cross_side_flag'] = FLAGS.get(r['row_id'], '')

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
         'cross_side_flag', 'relation_to_existing_row', 'open_question_or_data_request']
os.makedirs(OUT, exist_ok=True)
with open(OUT + 'parameter_register.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, pcols); w.writeheader(); w.writerows(rows)
with open(OUT + 'source_crosswalk.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, xcols); w.writeheader(); w.writerows(xrows)
with open(OUT + 'dictionary_map.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['094r_term', 'register_rows'])
    for t, v in DICT.items(): w.writerow([t, '; '.join(v)])

# ---- unresolved-data list: 16 requests (101r DR-01 to DR-09, 102r R1 to R7) merged into supplies -------------------------------
SUP = [
 ('SUP-1', 'WAS study 7215 (UKDS), Round 8 and panel, person and household files: household wealth with components, age and economic status of the reference person, gross secured and unsecured debt, DB/DC and in-payment pensions, gifts and inheritances received, income, and the longitudinal status and decile changes',
  '101r:DR-07; 101r:DR-08 (partly); 102r:R1', 'F-01,F-06,F-13,F-29,S07,S10,S11,S13,S17,S22,S25,S28,D04',
  'cells keep stage on the pack proxy (S06), stage and band transitions stay unset, debt and debt service stay unset, income and consumption by cell stay on scenario ranges',
  'UK Data Service registration and the End User Licence for safeguarded study 7215 (098r section 6; 095r); commercial use may need data-owner approval; Secure Access study 6709 is the fallback (3 to 4 months, non-commercial, UK-based)',
  'UKDS End User Licence (safeguarded); not unrestricted'),
 ('SUP-2', 'ONS national accounts, household sector S.14: pension entitlements AF.6 stock by year; non-financial revaluation (dwellings and land); consumption of fixed capital on dwellings; B.2g split into dwelling services and other surplus; D.611/D.613 split into pension and NIC contributions; D.622 benefits by scheme type and age group (ONS or DWP)',
  '101r:DR-01 (stock); 101r:DR-02; 101r:DR-03; 101r:DR-04; 101r:DR-05', 'F-02,F-11,F-12,F-13,F-16,F-23,F-24,F-35',
  'pension accrual only as an aggregate scenario on the ONS basis, no pension return, saving stays gross of consumption of fixed capital, O stays a reported residual',
  'ONS UK Economic Accounts and National Balance Sheet downloads; the ONS spreadsheet link was not parseable by the research interface (095r), so the author or code role downloads; series ids to be identified',
  'ONS statistics are published under the Open Government Licence v3.0 (093r reading; licence page not re-checked here)'),
 ('SUP-3', 'ONS enquiry: reconciliation of household pension entitlements (AF.6) to WAS Round 8 SCAPE-based pension wealth; note on WAS Table 2.13 against Table 2.11 adult counts; ONS 3222 against NBS financial liabilities',
  '101r:DR-01 (reconciliation); 102r:R2; 102r:R6 (part)', 'F-12,F-35,S08,S12,S27',
  'the three pension bases stay unconverted, adults per household stays on the I-D4h register value, S12 stays a reported mismatch',
  'ONS enquiry (not a download); no response time known', 'not applicable (correspondence)'),
 ('SUP-4', 'Bank of England NMG 2011 to 2026 survey (workbook or microdata): values and wave coverage of saving, debt service and income-band variables (be2afree_c, soa1, qbe02, be08free_c, be07free_c, qincomev2)',
  '101r:DR-06; 102r:R5', 'F-36,S13,D04',
  'no NMG value is used; saving and debt service by income band stay scenario or unset',
  'Bank of England publishes downloadable NMG microdata and example Stata code (095r); the raw files were not downloaded', 'licence not checked in the repository'),
 ('SUP-5', 'HMRC inheritance tax statistics: estates by size band and composition, current years (tables held as ODS in 097r but not parsed)',
  '102r:R3', 'S17,S18',
  'gifts and inheritances stay unset; the one-heir rule S19 stays the legacy modelling choice',
  'HMRC statistics download', 'licence not checked in the repository'),
 ('SUP-6', 'Mortality by wealth or a linked wealth-mortality estimate for the UK (no source identified in 098r)',
  '102r:R4', 'S24',
  'mortality stays age and sex only (S24, ready); no wealth gradient',
  'ONS enquiry; no direct published table identified', 'not applicable'),
 ('SUP-7', 'Author or analyst items: the source PDFs for I-W1c and the I-W3 rows (Fagereng and others; Bangham and Leslie 2020; Advani, Bangham and Leslie 2021) and the page references; the GDP series behind the register ratio against the pack; the Round 8 top-wealth reconciliation',
  '101r:DR-09; 102r:R6 (part); 102r:R7', 'F-28,F-30,S15,S29,S31',
  'the four I-W3 rows and I-W1c stay validation context only and unverified; I-D4a and the pack GDP stay as audited in 102r',
  'supplied by the author', 'as the publishers state; not checked'),
]
NO_SOURCE = {'F-25': 'legacy comparator; no data wanted (author ruling)', 'F-29': 'no UK source known for saving by wealth band (101r DR-08); SUP-1 could give wealth change by band, not saving',
             'F-30': 'foreign figure, gross of gains; no UK counterpart wanted', 'S26': 'no source identified for household formation and dissolution by band',
             'F-28': 'UK return by rank is not published (101r); SUP-7 only verifies the registered figures'}
orig = ['101r:DR-0%d' % i for i in range(1, 10)] + ['102r:R%d' % i for i in range(1, 8)]
mapped = set()
for _, _, m, _, _, _, _ in SUP:
    mapped |= {x.split(' ')[0] for x in re.split(r';\s*', m)}
mapped = {x for x in mapped}
for o in orig:
    if not any(o == x or x.startswith(o) for x in mapped): errs.append('original request not mapped to a supply: ' + o)
need = {r['row_id'] for r in rows if r['ruling_class'] in ('unset', 'further data')}
covered = set()
for _, _, _, ids_, _, _, _ in SUP:
    covered |= set(ids_.split(','))
for i in sorted(need - covered - set(NO_SOURCE)): errs.append('unset or further-data row not covered by a supply or a no-source reason: ' + i)
for i in covered:
    if i not in idset: errs.append('supply names an unknown row: ' + i)
with open(OUT + 'unresolved_data.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['supply_id', 'what_to_supply', 'merges_requests', 'register_rows_informed', 'n_rows', 'model_can_proceed_without', 'access_route', 'licence_or_terms'])
    for sid, what, m, ids_, proc, acc, lic in sorted(SUP, key=lambda x: -len(x[3].split(','))):
        w.writerow([sid, what, m, ids_, len(ids_.split(',')), proc, acc, lic])
    for k, v in sorted(NO_SOURCE.items()): w.writerow(['no source', v, '', k, 1, 'row stays as classified', '', ''])
print('supplies=%d original_requests=%d rows_needing_data=%d covered=%d no_source=%d' % (len(SUP), len(orig), len(need), len(need & covered), len(need & set(NO_SOURCE))))

# ---- differences from the existing register (read-only; 105c edits to I-D4a, I-D4b, I-D4h are on main) -----------------------
DIFF = [
 ('I-D1a', 'supports', 'F-26', 'JST arithmetic real mean 4.742% against 4.74', 'none', 'no change'),
 ('I-D1a2', 'no disagreement; no additive split', 'F-27', 'geometric mean has no additive yield and gain split', 'none', 'keep as the geometric comparator; the split rows are arithmetic'),
 ('I-D14c', 'legacy comparator, not evidence', 'F-25', '3.5% (0.5 to 5) has no UK source (093r); author decision 2026-11-21', 'run labelling in 057c', 'keep only as a labelled legacy run; no replacement scalar'),
 ('I-W1c', 'unverified; proxy for validation', 'F-28', 'composition-implied financial return gap; figures not in a held file; direction agrees with AB-05', 'none', 'validation context only; verify with DR-09 (SUP-7)'),
 ('I-W3a', 'foreign; proxy (J central)', 'F-29', 'Norway, % of disposable income; no UK saving by wealth band held', 'none', 'not a UK value; do not use as a band saving rate'),
 ('I-W3b', 'reclassify: saving plus gains, not saving', 'F-30', 'gross of unrealised gains (S + CG), so it must not feed a saving term (094r B3 case 6c)', 'none', 'author or guru to reclassify as context only'),
 ('I-W3c', 'validation moment; citation unreconciled', 'F-31', 'share of the change in financial wealth that is saving; register cites Bangham and Leslie 2020 Fig 6, 099r read the 2021 paper', 'none', 'resolve the citation with DR-09; midpoint 15 is not an estimate'),
 ('I-W3d', 'validation moment; RF basis; page unreconciled', 'F-32', 'active saving about 40% of the total wealth gain; Resolution Foundation basis excludes DB pensions; page 22 against 099r pages 21, 13, 5', 'none', 'resolve the page with DR-09; not on the WDT pension basis'),
 ('I-D4a', 'central supports; low and high unverified; GDP differs from the pack', 'S29', '5.94 reproduces; pack GDP 2,211.48bn gives 6.14 (3.2%); held NBS S.14 over the same GDP gives 5.03', '105c annotated the row (unverified low and high, GDP mismatch); not reconciled', 'open: reconcile the pack GDP with the register GDP; verify low and high (SUP-7)'),
 ('I-D4b', 'low supports; high inside the held bracket; central below it and untestable', 'S30', 'low 49.3 reproduces as a household share; bracket 59.2 to 72.7; central 54.9 implies 1.77 adults per household', '105c relabelled the bounds as household shares and flagged the central', 'open for the author: the central (lognormal fit) cannot be tested by a held table'),
 ('I-D4c', 'not tested; depends on the I-D4b central', 'S30', 'share of wealth held by the adults above W_min; derived from I-D4b', 'none', 'moves with I-D4b; no separate evidence'),
 ('I-D4d', 'supports as a range', 'S15', 'top 1% share 14.4 to 23.0 published', 'none', 'keep as a range; WID 21.3 (2024) is on a different basis (S32)'),
 ('I-D4e', 'supports as a range', 'S15', 'wealth missing from the WAS top, 0 to 5.6% of total', 'none', 'keep as a range; no single value'),
 ('I-D4g', 'supports the level; ratio not reproducible', 'S29', 'held NBS S.14 net worth end-2025 GBP 10,829bn; ratio 3.6 uses a GDP not held', 'none', 'cross-check only; do not mix with the I-D4a survey basis (C08)'),
 ('I-D4h', 'central supports; Table 2.13 differs; old low contradicted', 'S30', '1.93 reproduces (1.9282); Table 2.13 gives 1.8593; the earlier low 1.77 was an assumption', '105c set the low to 1.86', 'closed; the 16+ against 18+ definition stays an author decision'),
 ('I-W4a', 'supports', 'S33', '80% top-decile stay (AB-02)', 'none', 'no change'),
 ('I-W4b', 'supports', 'S33', '90% of entrants from the ninth decile (AB-02)', 'none', 'no change'),
 ('I-W4c', 'supports; central is a midpoint', 'S33', '74 and 77 reproduce (Table 1); 75.5 is the register midpoint (J)', 'none', 'age-adjusted income groups, not wealth bands'),
 ('I-W4d', 'not audited against a held file', 'S33', 'Norway 11-year move to the top 1%', 'none', 'foreign; context only'),
 ('I-W4e', 'not audited against a held file', 'S33', 'Norway bottom decile to the top decile', 'none', 'foreign; context only'),
 ('I-W4f', 'not audited against a held file', 'S33', 'UK rank-rank slope 0.27 to 0.37', 'none', 'not audited; no held table'),
 ('I-W5a', 'supports', 'S31', '40.71 reproduces from Table 2.2; low 40.1 reproduces', 'none', 'high 43.9 depends on the I-D4e add-on'),
 ('I-W5b', 'derived (J); not tested', 'S32', 'Pareto-implied household top 1%; not tested against a held file', 'none', 'not tested here'),
 ('I-W5c', 'definitions differ from the pack tail', 'S32', 'WID top 1% 21.3 (2024 adults) against 14.4 to 23.0 (2016-18)', 'none', 'not averaged; different years and definitions'),
 ('I-W5d', 'definitions differ from the pack tail', 'S32', 'WID top 10% 57.1 (2024) against 52.4 to 52.5 (2016-18)', 'none', 'not averaged'),
 ('I-W5e', 'supports', 'S31', 'pension share 35.43 against 35.4', 'none', 'no change'),
]
dids = {d[0] for d in DIFF}
for n in sorted(named - dids): errs.append('named existing row without a differences entry: ' + n)
for d in DIFF:
    if d[2] not in idset: errs.append('differences entry names an unknown row: ' + d[2])
with open(OUT + 'register_differences.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['existing_row', 'verdict', 'merged_register_row', 'finding', 'edit_already_on_main', 'recommended_action_not_made_here'])
    w.writerows(DIFF)
print('rows=%d (flows %d, stocks %d, dictionary %d) crosswalk=%d terms=%d named_existing_rows=%d failures=%d' %
      (len(rows), len(fl), len(st), len(D_ROWS), len(xrows), len(DICT), len(named), len(errs)))
for e in errs: print('FAIL', e)
sys.exit(1 if errs else 0)
