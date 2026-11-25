"""102r block A1: band reconciliation, composition by pack band, stage weights and person/household weights.
Reads only held files (data/rates/totalwealthtables.xlsx, data/uk-wealth-tables/098r/*.csv, the pack wealth_distribution.csv).
Run from anywhere: python -I research/scripts/derive_bands_stages.py
Writes CSVs next to this script. Every output has a `tolerance_note` or check column; the script exits non-zero if a stated tolerance fails."""
import csv, os, sys
import openpyxl

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))   # the repository root (this script is in research/scripts/)
HERE = os.path.join(ROOT, 'research', 'tables', '102r-parameter-map-stocks-and-cells')   # the 102r tables (was the folder of this script)
D098 = os.path.join(ROOT, 'data', 'uk-wealth-tables', '098r')
XL = os.path.join(ROOT, 'data/rates', 'totalwealthtables.xlsx')
PACK = os.path.join(ROOT, 'model_v3', 'pack', 'GBR', 'wealth_distribution.csv')
FAIL = []

def check(name, ok, detail=''):
    if not ok:
        FAIL.append(f'{name}: {detail}')

def write(name, header, rows):
    with open(os.path.join(HERE, name), 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(header); w.writerows(rows)

def rd(path):
    with open(path, newline='') as fh:
        return list(csv.DictReader(fh))

ROUNDS = ['July 2006 to June 2008', 'July 2008 to June 2010', 'July 2010 to June 2012', 'July 2012 to June 2014',
          'July 2014 to June 2016', 'April 2014 to March 2016', 'April 2016 to March 2018',
          'April 2018 to March 2020', 'April 2020 to March 2022']
BANDS = ['Less than £20,000', '£20,000 but < £85,000', '£85,000 but < £200,000', '£200,000 but < £300,000',
         '£300,000 but < £500,000', '£500,000 but < £1 million', '£1 million or more']
GROUPS = [('D1-3', [0, 1], 30), ('D4-5', [2, 3], 50), ('D6-7', [4], 70), ('D8-9', [5], 90), ('D10', [6], 100)]
PACK_DEC = {'D1-3': (1, 3), 'D4-5': (4, 5), 'D6-7': (6, 7), 'D8-9': (8, 9), 'D10': (10, 10)}

# ---------- Workbook Table 2.1 and 2.2 (aggregate components, by decile) ----------
wb = openpyxl.load_workbook(XL, read_only=True, data_only=True)
def block(ws_name, first_row, n, col):
    ws = wb[ws_name]
    rows = list(ws.iter_rows(min_row=first_row, max_row=first_row + n - 1, values_only=True))
    return [r[col] for r in rows]
# columns: B=1 label, C..K = rounds 0..8 -> index 2..10
t21 = {}
for key, row in [('property', 4), ('financial', 5), ('physical', 6), ('pension', 7), ('total', 8)]:
    ws = wb['Table 2.1']
    r = list(ws.iter_rows(min_row=row, max_row=row, values_only=True))[0]
    t21[key] = [r[2 + i] for i in range(9)]
t22 = {}
for key, first in [('total', 4), ('property', 14), ('financial', 24), ('physical', 34), ('pension', 44),
                   ('unweighted', 54), ('households', 64)]:
    t22[key] = [block('Table 2.2', first, 10, 2 + i) for i in range(9)]  # per round: list of 10 deciles

# ---------- A. composition by pack band ----------
comp_rows = []
for ri, rd_name in enumerate(ROUNDS):
    for g, _, _ in GROUPS:
        lo, hi = PACK_DEC[g]
        idx = range(lo - 1, hi)
        agg = {k: sum(t22[k][ri][i] for i in idx) / 1000.0 for k in ('total', 'property', 'financial', 'physical', 'pension')}
        hh = sum(t22['households'][ri][i] for i in idx) / 1000.0
        comp_sum = agg['property'] + agg['financial'] + agg['physical'] + agg['pension']
        # tolerance: Table 2.2 rows in £ million, components may not sum to total because of rounding of the published cells
        resid = agg['total'] - comp_sum
        check(f'comp_sum {rd_name} {g}', abs(resid) < 0.01 * max(1.0, abs(agg['total'])) + 1.0, f'{resid:.3f}bn')
        sh = {k: (agg[k] / agg['total'] * 100 if agg['total'] else '') for k in ('property', 'financial', 'physical', 'pension')}
        comp_rows.append([rd_name, g, f'{lo}-{hi}', round(agg['total'], 3), round(agg['property'], 3), round(agg['financial'], 3),
                          round(agg['physical'], 3), round(agg['pension'], 3), round(resid, 3), round(hh, 1),
                          round(agg['total'] * 1e6 / (hh * 1e3), 0) if hh else '',
                          *[round(sh[k], 1) if sh[k] != '' else '' for k in ('property', 'financial', 'physical', 'pension')],
                          'sum of Table 2.2 decile rows; households = weighted frequency of the deciles; shares of band net total; band with small or negative net total gives unstable shares (D1-3)'])
write('band_composition_by_pack_band.csv',
      ['round', 'pack_band', 'wealth_deciles', 'total_gbp_bn', 'net_property_gbp_bn', 'net_financial_gbp_bn', 'physical_gbp_bn',
       'private_pension_gbp_bn', 'components_minus_total_gbp_bn', 'households_thousand', 'mean_total_gbp_per_household',
       'share_property_pct', 'share_financial_pct', 'share_physical_pct', 'share_pension_pct', 'note'], comp_rows)

# decile-sum vs Table 2.1, in £bn (Table 2.1 is rounded to £1bn)
t_rows = []
for ri, rd_name in enumerate(ROUNDS):
    for k in ('property', 'financial', 'physical', 'pension', 'total'):
        s = sum(t22[k][ri]) / 1000.0
        diff = s - t21[k][ri]
        tol = 1.0 if ri > 0 else 0.02 * t21[k][ri]
        check(f'T2.1 vs T2.2 {rd_name} {k}', abs(diff) <= tol, f'{diff:.3f}')
        t_rows.append([rd_name, k, round(s, 3), t21[k][ri], round(diff, 3),
                       f'tolerance {tol:.1f} bn: 1.0 for rounds 2 to 9 (Table 2.1 is rounded to 1bn); 2% of the component for July 2006 to June 2008 (the footnote names a half sample for total and physical wealth only; the 1.8% financial gap is unexplained and recorded as found)'])
write('check_table21_vs_table22.csv', ['round', 'component', 'sum_of_deciles_gbp_bn', 'table_2_1_gbp_bn', 'difference', 'tolerance_note'], t_rows)

# R8 against the pack file
pack = rd(PACK)
pk = {(r['variable'], r['band']): float(r['value']) for r in pack}
for d in range(1, 11):
    check(f'pack wealth_total D{d}', abs(t22['total'][8][d - 1] / 1000.0 - pk[('wealth_total', f'D{d}')]) < 0.0005)
for g in ('D4-5', 'D6-7', 'D8-9', 'D10'):
    row = [r for r in comp_rows if r[0] == ROUNDS[8] and r[1] == g][0]
    chk = [('net_financial_share', row[12]), ('property_share', row[11]), ('pension_share', row[14])]
    for var, val in chk:
        if (var, g) in pk:
            check(f'pack {var} {g}', abs(val - pk[(var, g)]) <= 0.1, f'{val} vs {pk[(var, g)]}')

# ---------- B. band reconciliation (exact weighted frequencies) ----------
hh = rd(os.path.join(D098, 'was_households_by_wealth_band.csv'))
old_map = rd(os.path.join(D098, 'was_band_edge_mapping.csv'))
rec_rows = []; hh_by_round = {}
for rd_name in ROUNDS:
    wf = {r['wealth_band']: float(r['value']) for r in hh if r['round'] == rd_name and r['measure'] == 'Weighted Frequency'}
    tot = wf['All households']
    band_n = [wf[b] for b in BANDS]
    check(f'band sum {rd_name}', abs(sum(band_n) - tot) <= 7000, f'{sum(band_n) - tot}')  # rounding of each cell to thousands
    hh_by_round[rd_name] = (band_n, tot)
    cum = 0
    for g, idxs, tgt_hi in GROUPS:
        n = sum(band_n[i] for i in idxs)
        lo_cum = cum / tot * 100; cum += n; hi_cum = cum / tot * 100
        tgt_lo = tgt_hi - {'D1-3': 30, 'D4-5': 20, 'D6-7': 20, 'D8-9': 20, 'D10': 10}[g]
        old = [r for r in old_map if r['round'] == rd_name and r['wdt_band'] == g]
        old_share = float(old[0]['was_household_share_pct']) if old else ''
        d_old = (hi_cum - lo_cum - old_share) if old else ''
        if old:
            check(f'098r share {rd_name} {g}', abs(d_old) <= 1.0, f'{d_old}')
        rec_rows.append([rd_name, g, '+'.join(BANDS[i] for i in idxs), tgt_lo, tgt_hi, round(lo_cum, 1), round(hi_cum, 1),
                         round(hi_cum - lo_cum, 1), tgt_hi - tgt_lo, round((hi_cum - lo_cum) - (tgt_hi - tgt_lo), 1),
                         round(hi_cum - tgt_hi, 1), old_share, round(d_old, 1) if old else '',
                         'exact weighted frequencies (Table 2.5, thousands); 098r used rounded percentages; tolerance 1.0pp vs 098r'])
write('band_reconciliation_exact.csv',
      ['round', 'pack_band', 'was_bands_grouped', 'target_cum_lo_pct', 'target_cum_hi_pct', 'was_cum_lo_pct', 'was_cum_hi_pct',
       'was_household_share_pct', 'target_share_pct', 'share_mismatch_pp', 'upper_edge_mismatch_pp', 'share_098r_rounded_pct',
       'exact_minus_098r_pp', 'note'], rec_rows)

# ---------- C. stage weights and person/household weights ----------
act = rd(os.path.join(D098, 'was_persons_activity_by_wealth_band.csv'))
age = rd(os.path.join(D098, 'was_persons_age_by_wealth_band.csv'))
old_stage = rd(os.path.join(D098, 'was_stage_by_wdt_band_derived.csv'))
STAGE_OF = {'In employment': 'working', 'Unemployed': 'unemployed', 'Student': 'inactive_not_retired',
            'Looking after family/home': 'inactive_not_retired', 'Sick/disabled (2)': 'inactive_not_retired',
            'Other inactive': 'inactive_not_retired', 'Retired': 'retired'}
st_rows = []; adults_by = {}
for rd_name in ROUNDS:
    rr = [r for r in act if r['round'] == rd_name]
    groups = {}
    for r in rr:
        g = r['group']
        if g.startswith('All Persons'):
            groups['ALL'] = float(r['weighted_n']); continue
        if g in STAGE_OF and r['level'] == 'main' and r['group_kind'] == 'activity':
            groups.setdefault(g, {'n': float(r['weighted_n']) if r['weighted_n'] else 0.0, 'pct': {}, 'flag': {}})
            if r['percent'] != '':
                groups[g]['pct'][r['wealth_band']] = float(r['percent'])
            groups[g]['flag'][r['wealth_band']] = r['flag']
    all_adults = groups['ALL']
    stage_tot = sum(groups[g]['n'] for g in STAGE_OF if g in groups)
    check(f'stage totals vs all adults {rd_name}', abs(stage_tot - all_adults) <= 0.001 * all_adults, f'{stage_tot} vs {all_adults}')
    res = {}
    for g, idxs, _ in GROUPS:
        res[g] = {s: 0.0 for s in ('working', 'unemployed', 'inactive_not_retired', 'retired')}
        res[g + '_flagged_missing_rows'] = 0
        for grp, s in STAGE_OF.items():
            if grp not in groups: continue
            for i in idxs:
                b = BANDS[i]
                if b in groups[grp]['pct']:
                    res[g][s] += groups[grp]['n'] * groups[grp]['pct'][b] / 100.0
                else:
                    res[g + '_flagged_missing_rows'] += 1
    for g, idxs, _ in GROUPS:
        tot_g = sum(res[g].values())
        adults_by[(rd_name, g)] = tot_g
        for s, v in res[g].items():
            old = [r for r in old_stage if r['round'] == rd_name and r['wdt_band'] == g and r['stage'] == s]
            d = (v - float(old[0]['derived_persons'])) if old else ''
            if old: check(f'098r stage {rd_name} {g} {s}', abs(d) < 1.0, f'{d}')
            st_rows.append([rd_name, g, s, round(v), round(v / tot_g * 100, 1) if tot_g else '', round(tot_g),
                            res[g + '_flagged_missing_rows'], d if d == '' else round(d, 3),
                            'persons aged 16+ placed by household wealth; weighted total of the status group x whole-number % of that row; each cell +-0.5pp of its row total'])
write('stage_weights_by_pack_band.csv',
      ['round', 'pack_band_approx', 'stage', 'persons', 'share_of_band_adults_pct', 'band_adults_total', 'suppressed_cells_in_band',
       'difference_from_098r_persons', 'note'], st_rows)

# rounding half-width: each row group's weighted n x 0.5pp, by stage and band group (R8)
R8 = ROUNDS[8]
half = []
rr = [r for r in act if r['round'] == R8]
for s in ('working', 'unemployed', 'inactive_not_retired', 'retired'):
    ng = [float(r['weighted_n']) for r in rr if r['group'] in STAGE_OF and STAGE_OF[r['group']] == s and r['level'] == 'main' and r['group_kind'] == 'activity' and r['wealth_band'] == BANDS[0]]
    for g, idxs, _ in GROUPS:
        half.append([R8, g, s, round(sum(ng) * 0.005 * len(idxs)), 'max rounding error in persons: row-group total x 0.5pp x bands grouped (upper bound, assumes errors all one sign)'])
write('stage_rounding_bounds_r8.csv', ['round', 'pack_band_approx', 'stage', 'max_rounding_persons', 'note'], half)

# Persons by age by band (Table 2.11) -> persons per household and adults per household by band group
agerows = {}
for r in age:
    if r['group_kind'] != 'age': continue
    agerows.setdefault((r['round'], r['group']), {})[r['wealth_band']] = (r['percent'], float(r['weighted_n']) if r['weighted_n'] else None)
AGES = ['Under 16', '16-24', '25-34', '35-44', '45-54', '55-64', '65+']
w_rows = []
for rd_name in ROUNDS:
    band_n, tot = hh_by_round[rd_name]
    for g, idxs, _ in GROUPS:
        persons = 0.0; adults = 0.0; missing = 0
        for a in AGES:
            ent = agerows.get((rd_name, a))
            if not ent: missing += 1; continue
            for i in idxs:
                p, n = ent.get(BANDS[i], ('', None))
                if p == '' or n is None: missing += 1; continue
                v = n * float(p) / 100.0
                persons += v
                if a != 'Under 16': adults += v
        h = sum(band_n[i] for i in idxs)
        a13 = adults_by[(rd_name, g)]
        w_rows.append([rd_name, g, round(h), round(persons), round(adults), round(persons / h, 3) if h else '',
                       round(adults / h, 3) if h else '', round(a13), round(a13 / h, 3) if h else '', missing,
                       'persons and adults from Table 2.11 age rows x % (16+ = 16-24 to 65+, so includes 16 and 17 year olds); adults_2_13 from Table 2.13; households from Table 2.5 weighted frequency'])
write('person_household_weights_by_band.csv',
      ['round', 'pack_band_approx', 'households', 'persons_all_ages_2_11', 'adults_16plus_2_11', 'persons_per_household',
       'adults_per_household_2_11', 'adults_2_13', 'adults_per_household_2_13', 'suppressed_cells', 'note'], w_rows)

# all-round adult totals (I-D4h comparison)
allrows = []
for rd_name in ROUNDS:
    adults11 = 0.0
    for a in AGES[1:]:
        ent = agerows.get((rd_name, a))
        if ent and 'All households' in ent: pass
    # age 'All' column not carried: use the all-persons rows from Table 2.11 weighted_n (one per age group)
    n11 = {}
    for r in age:
        if r['round'] == rd_name and r['group'] in AGES and r['wealth_band'] == BANDS[0]:
            n11[r['group']] = float(r['weighted_n'])
    a11 = sum(n11[a] for a in AGES[1:]); all11 = sum(n11[a] for a in AGES)
    h = hh_by_round[rd_name][1]
    a13 = [float(r['weighted_n']) for r in act if r['round'] == rd_name and r['group'].startswith('All Persons')][0]
    allrows.append([rd_name, round(h), round(all11), round(a11), round(a11 / h, 4), round(a13), round(a13 / h, 4),
                    round((a11 - a13)), 'Table 2.11 16+ rows against Table 2.13 all persons (16+); both over Table 2.5 households'])
write('adults_per_household_all_rounds.csv',
      ['round', 'households', 'persons_all_ages_2_11', 'adults_16plus_2_11', 'adults_per_hh_2_11', 'adults_2_13', 'adults_per_hh_2_13',
       'adults_2_11_minus_2_13', 'note'], allrows)

if FAIL:
    print('TOLERANCE FAILURES'); [print(' ', f) for f in FAIL]; sys.exit(1)
print('ok: all stated tolerances met')
