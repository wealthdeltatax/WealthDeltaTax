"""104r block 1: cell coverage matrix (deliverable C), from the 103r register and the 102r cell inputs.

Reads committed CSVs only. Writes, next to this script:
  104r-parameter-map-design-cell-weights.csv   persons by pack band and stage (102r, WAS Round 8) with the stated rounding bound
  resolution_by_row.csv   each 103r register row: variable group, finest resolution supported, evidence class, evidence form
  coverage_matrix.csv     variable group x cell (5 pack bands x {not retired, retired}): evidence class and form per cell
  resolution_pivot.csv    103r rows counted by resolution and evidence class
Fails (exit 1) if a cell or a register row is missing from the matrix, or a cell in the matrix names an evidence class outside the
103r vocabulary. 'Evidence form' separates direct observation, derived from observation, modelled allocation, aggregate constraint,
externally specified path, scenario and none. Nothing here is a value for any cell. Run from the repository root with python -I.
"""
import csv, sys, collections
DIRS = {'102r': 'research/tables/102r-parameter-map-stocks-and-cells/', '103r': 'research/tables/103r-parameter-map-assembly/', '104r': 'research/tables/104r-parameter-map-design/'}   # 160c: the tables moved here (project/restructure map)
O = DIRS['104r']
reg = list(csv.DictReader(open(DIRS['103r'] + 'parameter_register.csv')))
cells_in = list(csv.DictReader(open(DIRS['102r'] + 'cell_coverage_inputs.csv')))
BANDS = ['D1-3', 'D4-5', 'D6-7', 'D8-9', 'D10']
STAGES = ['not retired', 'retired']
errs = []

# ---- cell weights: persons by band and the four WAS status groups; 'not retired' = working + unemployed + inactive not retired
w = collections.defaultdict(dict)
for r in cells_in:
    w[r['pack_band']][r['stage']] = (int(r['persons_r8']), int(r['max_rounding_persons']), float(r['share_of_band_adults_pct']), float(r['band_share_mismatch_pp']))
wr = []
for b in BANDS:
    tot = sum(v[0] for v in w[b].values())
    nr = sum(v[0] for k, v in w[b].items() if k != 'retired'); nr_r = sum(v[1] for k, v in w[b].items() if k != 'retired')
    rt, rt_r = w[b]['retired'][0], w[b]['retired'][1]
    wr.append(dict(pack_band=b, stage='not retired', persons=nr, max_rounding=nr_r, share_of_band_adults_pct=round(100 * nr / tot, 1),
                   of_which='working %d; unemployed %d; inactive not retired %d' % (w[b]['working'][0], w[b]['unemployed'][0], w[b]['inactive_not_retired'][0]),
                   band_share_mismatch_pp=w[b]['retired'][3]))
    wr.append(dict(pack_band=b, stage='retired', persons=rt, max_rounding=rt_r, share_of_band_adults_pct=round(100 * rt / tot, 1), of_which='', band_share_mismatch_pp=w[b]['retired'][3]))
with open(O + '104r-parameter-map-design-cell-weights.csv', 'w', newline='') as f:
    x = csv.DictWriter(f, list(wr[0])); x.writeheader(); x.writerows(wr)

# ---- variable groups: which 103r rows carry each, and the evidence class and form at each resolution
GROUPS = [
 # id, group, register rows, class at band level (per band overrides), class by stage, form, note
 ('G01', 'Cell weights (persons by band and stage)', 'S02,S03,S04', 'derived', 'derived', 'derived from direct observation', 'stage is the person status in the WAS table; band edges differ from the deciles by up to 4.9pp of households (S02); whole-number percentages'),
 ('G02', 'Opening band wealth (mean and total)', 'S01,S29', 'observed', 'unset', 'direct observation', 'band totals from WAS Round 8; no joint wealth by stage table is held'),
 ('G03', 'Asset composition: property, net financial, physical, pension', 'S05,S06,S07,S08,S09', 'observed', 'proxy', 'direct observation at band; age of reference person as a proxy for stage', 'D1-3 shares are unstable (small or negative net totals); the pension share is on the WAS SCAPE basis'),
 ('G04', 'Gross debt, interest and repayment', 'S10,S11,S12,S13,D04', 'unset', 'unset', 'none by band (age totals observed, aggregate cross-check only)', 'DR in SUP-1 and SUP-4'),
 ('G05', 'Labour income and benefits (Y_L; transfer income)', 'F-01,F-02,F-03,F-05', 'proxy', 'unset', 'aggregate constraint; band means are register judgement rows', 'register I-D9a to I-D9d are all-household means for D4-5 to D10 and are not held below D4; retired income unset'),
 ('G06', 'Ordinary taxes net of benefits (T_C)', 'F-04', 'proxy', 'proxy', 'modelled allocation (income decile mapped to wealth band by judgement)', 'ETB by income decile; no wealth-band split'),
 ('G07', 'Consumption (C), and the legacy comparator', 'F-06,F-25', 'unset', 'unset', 'aggregate constraint', 'P.31 aggregate only; no spending by wealth band or stage held'),
 ('G08', 'Net saving (S) and saving over wealth', 'F-07,F-08,F-09,F-24,F-29,F-30,F-31,F-32,F-33,F-34,F-36', 'unset', 'unset', 'aggregate constraint; average-family and foreign proxies are validation moments only', 'no UK saving by wealth band (103r SUP-1 note)'),
 ('G09', 'Pension flows: contributions, accrual, withdrawal', 'F-10,F-11,F-13,F-35', 'scenario', 'scenario', 'aggregate constraint on the ONS basis; one labelled aggregate scenario (author ruling 2026-11-21)', 'no rate on the SCAPE stock; allocation to cells is a scenario, not an estimate'),
 ('G10', 'Retained cash yield and the yield and gain by asset class', 'F-14,F-15,F-16,F-17,F-18,F-19,F-20,F-26,F-27', 'externally specified', 'externally specified', 'externally specified path (JST market portfolio); retained fraction by band unset', 'same path for every cell; weights differ by cell composition'),
 ('G11', 'Return on classes with no held return: pension, physical, net financial', 'F-12', 'scenario', 'scenario', 'labelled scenario range per class (author ruling 2026-11-21)', 'a range, not an estimate; no instrument split of net financial wealth is held'),
 ('G12', 'Liability revaluation and residual O', 'F-21,F-22,F-23', 'unset', 'unset', 'aggregate constraint', 'O reported, not forced to zero (author ruling); by band needs G04'),
 ('G13', 'Gifts, inheritances, inter-household transfers (TR)', 'S16,S17,S18,S19', 'unset', 'unset', 'aggregate (sector with other sectors only); legacy heir rule is the comparator', 'zero in aggregate within the household sector by construction'),
 ('G14', 'Transitions: band mobility, retirement entry, mortality, household formation', 'S20,S21,S22,S23,S24,S25,S26,S27,S28,S33', 'proxy', 'unset', 'proxy: whole-distribution and income-group mobility moments; mortality age-sex only', 'entry hazard and band-by-stage matrix unset (SUP-1)'),
 ('G15', 'Top tail within D10', 'S14,S15,S31,S32,F-28', 'scenario', 'scenario', 'observed tail shares (WID, WAS) with a labelled adjustment range', 'the tail is a split of D10 supported as a range, not a cell'),
]
VOCAB = {'observed', 'derived', 'proxy', 'scenario', 'unset', 'externally specified', 'endogenous', 'legacy'}
regid = {r['row_id']: r for r in reg}
mat = []
for gid, name, rowids, cband, cstage, form, note in GROUPS:
    for rid in rowids.split(','):
        if rid not in regid: errs.append('group %s names an unknown row %s' % (gid, rid))
    for b in BANDS:
        for s in STAGES:
            cls = cband if s == 'not retired' else cstage
            if gid in ('G03',) and b == 'D1-3': cls = 'observed (unstable shares)' if s == 'not retired' else 'proxy'
            if gid == 'G05' and b == 'D1-3' and s == 'not retired': cls = 'unset'
            if gid == 'G15' and b != 'D10': cls = 'not applicable'
            mat.append(dict(group_id=gid, variable_group=name, pack_band=b, stage=s, evidence_class=cls, evidence_form=form, register_rows=rowids, note=note))
            base = cls.split(' (')[0]
            if base not in VOCAB and base != 'not applicable': errs.append('class outside the vocabulary: %s %s' % (gid, cls))
with open(O + 'coverage_matrix.csv', 'w', newline='') as f:
    x = csv.DictWriter(f, list(mat[0])); x.writeheader(); x.writerows(mat)
if len(mat) != len(GROUPS) * len(BANDS) * len(STAGES): errs.append('matrix size')
for b in BANDS:
    for s in STAGES:
        if not any(m['pack_band'] == b and m['stage'] == s for m in mat): errs.append('cell missing: %s %s' % (b, s))

# ---- every register row: group (if any), resolution, class and form
def level(r):
    t = r['target_cell_dimension'].lower()
    if t.startswith('band x stage'): return 'band x stage'
    if t.startswith('stage (retired)'): return 'other axis (age, income, estate size, stage only)'
    if t.startswith('band') and 'band x' not in t: return 'band'
    if t.startswith('d10') or 'tail' in t or 'top' in t or 'decile, financial' in t: return 'top tail or distribution moment'
    if t.startswith('age') or 'age and income' in t or 'income' in t or 'estate' in t or 'household, income' in t: return 'other axis (age, income, estate size, stage only)'
    if t.startswith('market') or t.startswith('asset class'): return 'market path, not household'
    if t.startswith('aggregate') or t in ('all',) or t.startswith('average family') or 'average family' in t: return 'aggregate'
    return 'none'
grp = {}
for gid, name, rowids, *_ in GROUPS:
    for rid in rowids.split(','): grp.setdefault(rid, gid)
rr = []
for r in reg:
    rr.append(dict(row_id=r['row_id'], variable=r['variable'], group_id=grp.get(r['row_id'], ''), finest_resolution_supported=level(r), evidence_class=r['class_norm'], ruling_class=r['ruling_class'],
                   target_cell_dimension=r['target_cell_dimension']))
with open(O + 'resolution_by_row.csv', 'w', newline='') as f:
    x = csv.DictWriter(f, list(rr[0])); x.writeheader(); x.writerows(rr)
piv = collections.Counter((x['finest_resolution_supported'], x['evidence_class']) for x in rr)
levels = ['aggregate', 'market path, not household', 'band', 'other axis (age, income, estate size, stage only)', 'top tail or distribution moment', 'band x stage', 'none']
classes = ['observed', 'derived', 'proxy', 'scenario', 'unset', 'endogenous', 'legacy']
with open(O + 'resolution_pivot.csv', 'w', newline='') as f:
    x = csv.writer(f); x.writerow(['resolution'] + classes + ['total'])
    for l in levels: x.writerow([l] + [piv[(l, c)] for c in classes] + [sum(piv[(l, c)] for c in classes)])
ungrouped = [x['row_id'] for x in rr if not x['group_id'] and x['ruling_class'] not in ('audit (no ruling)', 'not applicable (endogenous)', 'legacy comparator')]
print('cells=%d groups=%d matrix_rows=%d register_rows=%d grouped=%d ungrouped_parameter_rows=%s failures=%d' % (len(wr), len(GROUPS), len(mat), len(rr), sum(1 for x in rr if x['group_id']), ','.join(ungrouped), len(errs)))
for l in levels: print(l, [piv[(l, c)] for c in classes])
for e in errs: print('FAIL', e)
sys.exit(1 if errs else 0)
