"""102r block A2: debt by age (ONS 3222), wealth composition by age of reference person (ONS 2813), national balance sheet
comparison with WAS Round 8, and demographic hazards (ONS 2024-based GB projections, mortality).
Run: python -I research/scripts/derive_debt_demography.py   (reads held files only; exits non-zero on a failed tolerance)"""
import csv, os, sys, collections
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))   # the repository root (this script is in research/scripts/)
HERE = os.path.join(ROOT, 'research', 'tables', '102r-parameter-map-stocks-and-cells')   # the 102r tables (was the folder of this script)
D098 = os.path.join(ROOT, 'data', 'uk-wealth-tables', '098r'); D097 = os.path.join(ROOT, 'data', 'uk-wealth-tables', '097r')
FAIL = []
def rd(p):
    with open(p, newline='') as fh: return list(csv.DictReader(fh))
def write(n, h, rows):
    with open(os.path.join(HERE, n), 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(h); w.writerows(rows)
def check(n, ok, d=''):
    if not ok: FAIL.append(f'{n}: {d}')

# ---------- debt by age (sum of eleven regions = Great Britain) ----------
debt = rd(os.path.join(D098, 'ons_was_debt_by_age_region.csv'))
cells = collections.defaultdict(dict)
for r in debt:
    if r['value'] == '' or r['measure'] == 'Notes': continue
    cells[(r['debt_type'], r['age_band'], r['region'])][r['measure']] = float(r['value'])
AGES = ['16 to 34', '35 to 44', '45 to 54', '55 to 64', '65 and over']
rows = []
for t in ('personal financial debt', 'personal property debt'):
    for a in AGES:
        regs = [c for (tt, aa, rg), c in cells.items() if tt == t and aa == a]
        tot = sum(c['Total'] for c in regs if 'Total' in c); n = sum(c['Weighted frequency'] for c in regs if 'Weighted frequency' in c)
        nreg = len(regs)
        # tolerance: published mean x frequency against published total, per region cell, where frequency >= 100k (mean rounded to 100, frequency to 1000)
        worst = 0.0
        for c in regs:
            if all(k in c for k in ('Total', 'Mean', 'Weighted frequency')) and c['Weighted frequency'] >= 100000:
                worst = max(worst, abs(c['Mean'] * c['Weighted frequency'] / c['Total'] - 1))
        check(f'debt mean x n vs total {t} {a}', worst <= 0.05, f'{worst:.3f}')
        rows.append([t, a, nreg, round(tot / 1e9, 3), round(n), round(tot / n) if n else '', round(worst * 100, 2),
                     'GB = sum of 11 regional cells (Total and Weighted frequency); persons or households as ONS labels; debtors only (the frequency is holders of that debt); tolerance 5% on mean x n vs total for cells over 100k'])
write('debt_by_age_gb.csv', ['debt_type', 'age_band', 'regions_summed', 'total_gbp_bn', 'weighted_frequency_holders', 'mean_gbp_per_holder_derived',
                              'max_pct_gap_mean_times_n_vs_total', 'note'], rows)
tot_fin = sum(r[3] for r in rows if r[0] == 'personal financial debt'); tot_prop = sum(r[3] for r in rows if r[0] == 'personal property debt')
summ = [['personal financial debt', round(tot_fin, 3)], ['personal property debt', round(tot_prop, 3)]]
write('debt_gb_totals.csv', ['debt_type', 'gb_total_gbp_bn'], summ)

# ---------- composition by age of household reference person ----------
w = rd(os.path.join(D098, 'ons_was_wealth_by_age_of_hrp.csv'))
agg = collections.defaultdict(dict); mean = collections.defaultdict(dict); pct = collections.defaultdict(dict); freq = {}
for r in w:
    if r['wealth_component'] == 'Weighted Frequency': freq[r['hrp_age']] = float(r['value']); continue
    if r['wealth_component'] == 'Unweighted Frequency': continue
    key = {'Aggregate': agg, 'Mean': mean, 'Percent': pct}.get(r['statistic'])
    if key is not None: key[r['hrp_age']][r['wealth_component']] = float(r['value'])
AGE_H = ['16 to 24', '25 to 34', '35 to 44', '45 to 54', '55 to 64', '65 to 74', '75+']
comp = ['Property wealth (net)', 'Financial wealth (net)', 'Physical wealth', 'Private pension wealth']
rows = []
for a in AGE_H + ['All households']:
    tot = agg[a]['Total wealth']
    s = sum(agg[a][c] for c in comp)
    check(f'2813 components {a}', abs(s - tot) <= 0.002 * tot + 5, f'{s - tot}')
    rows.append([a, round(freq[a]), round(tot / 1000, 1), *[round(agg[a][c] / 1000, 1) for c in comp],
                 *[round(agg[a][c] / tot * 100, 1) for c in comp], round(pct[a]['Total wealth'], 1),
                 round(mean[a]['Total wealth']), round(tot * 1e6 / freq[a]) if freq[a] else '',
                 'aggregates in £ million in the ONS file, shown in £bn; shares are of the age group total; pension basis is the ONS Round 8 SCAPE-based valuation'])
s_age = sum(agg[a]['Total wealth'] for a in AGE_H)
check('2813 ages sum to total', abs(s_age - agg['All households']['Total wealth']) <= 1000, f'{s_age}')
write('composition_by_age_of_hrp.csv', ['hrp_age', 'households', 'total_gbp_bn', 'net_property_gbp_bn', 'net_financial_gbp_bn', 'physical_gbp_bn',
                                         'private_pension_gbp_bn', 'share_property_pct', 'share_financial_pct', 'share_physical_pct',
                                         'share_pension_pct', 'published_share_of_all_wealth_pct', 'published_mean_total_gbp',
                                         'derived_mean_total_gbp', 'note'], rows)

# ---------- national balance sheet against WAS Round 8 ----------
nb = {}
for f in ('ons_nbs_household_stocks_annual.csv', 'ons_nbs_financial_annual.csv'):
    for r in rd(os.path.join(D097, f)):
        nb[(r['series_id'], r['period'])] = float(r['value'])
was = {'property_net': 5461, 'financial_net': 1915, 'physical': 1385, 'pension': 4808, 'total': 13568}  # Table 2.1 April 2020 to March 2022 (£bn)
rows = []
for yr in ('2020', '2021'):
    netw = nb[('E45V', yr)] / 1000; nfa = nb[('NYOH', yr)] / 1000; fa = nb[('NITF', yr)] / 1000; fl = nb[('NIWJ', yr)] / 1000
    land = nb[('E44N', yr)] / 1000; dwell = nb[('E46V', yr)] / 1000; prod = nb[('E462', yr)] / 1000; nonprod = nb[('E3VW', yr)] / 1000
    nonfin = prod + nonprod
    check(f'NBS identity {yr}', abs(nonfin + nfa - netw) <= 0.003 * netw, f'{nonfin + nfa - netw}')
    rows += [[yr, 'S.14 net worth B.90', round(netw, 1), 'WAS total incl pensions', was['total'], round(netw - was['total'], 1), 'NBS end-year stock, UK households (S.14); WAS April 2020 to March 2022, GB, SCAPE-based DB valuation'],
             [yr, 'S.14 net financial assets BF.90 (incl pension entitlements)', round(nfa, 1), 'WAS net financial + private pension', was['financial_net'] + was['pension'], round(nfa - (was['financial_net'] + was['pension']), 1), 'NBS financial assets include pension and insurance entitlements (AF.6) and are net of all liabilities including mortgages; WAS net financial excludes property debt'],
             [yr, 'S.14 non-financial assets (produced AN.1 + non-produced AN.2)', round(nonfin, 1), 'WAS net property + physical', was['property_net'] + was['physical'], round(nonfin - (was['property_net'] + was['physical']), 1), 'NBS gross of mortgage debt; WAS property is net of mortgage debt; WAS physical includes contents and vehicles, not in the NBS household non-financial line the same way'],
             [yr, 'S.14 non-financial assets (produced AN.1 + non-produced AN.2), again', round(nonfin, 1), 'WAS net property + ONS 3222 personal property debt + physical', round(was['property_net'] + tot_prop + was['physical'], 1), round(nonfin - (was['property_net'] + tot_prop + was['physical']), 1), 'tests the gross reading: 3222 property debt (individuals, GB, summed over regions) added back to WAS net property; the 3222 population (persons) and what it counts as property debt may differ from the WAS household net property definition'],
             [yr, 'S.14 total financial liabilities AF.L', round(fl, 1), 'WAS financial liabilities (Table 5.9)', '', '', 'WAS Table 5.9 gives shares and percentiles, not an aggregate; no WAS aggregate gross debt is held. NBS AF.L includes mortgages and other loans']]
write('nbs_vs_was_r8.csv', ['nbs_year_end', 'nbs_line', 'nbs_gbp_bn', 'was_line', 'was_r8_gbp_bn', 'difference_gbp_bn', 'definitions'], rows)

# ---------- demography ----------
pop = rd(os.path.join(D098, 'ons_population_gb_principal_2024based.csv'))
qx = rd(os.path.join(D098, 'ons_qx_gb_2024based.csv'))
def age_int(a):
    try: return int(a)
    except ValueError: return None
P = collections.defaultdict(float)
for r in pop:
    a = age_int(r['age'])
    if a is not None and r['year'] in ('2024', '2030', '2040'): P[(r['sex'], a, int(r['year']))] += float(r['population'])
Q = {}
for r in qx:
    if r['basis'] == 'period': Q[(r['sex'], int(r['exact_age']), int(r['year_or_birth_year']))] = float(r['qx']) / 1e5
rows = []
for yr in (2024, 2030, 2040):
    for lo, hi in [(16, 24), (25, 34), (35, 44), (45, 54), (55, 64), (65, 74), (75, 84), (85, 100)]:
        num = 0.0; den = 0.0
        for sx in ('Males', 'Females'):
            for a in range(lo, hi + 1):
                pp = P.get((sx, a, yr), 0.0); qq = Q.get((sx.lower(), a, yr))
                if qq is None: continue
                num += pp * qq; den += pp
        popn = sum(P.get((sx, a, yr), 0.0) for sx in ('Males', 'Females') for a in range(lo, hi + 1))
        rows.append([yr, f'{lo}-{hi}', round(popn), round(num / den * 1e5, 1) if den else '', 'population-weighted period qx, both sexes (per 100,000); mortality not wealth-specific; ages above 100 not in the held qx file so 85-100 excludes 101+ population'])
write('demography_age_bands.csv', ['year', 'age_band', 'population_gb', 'mean_qx_per_100000', 'note'], rows)
# survival from 65 to 75 and 85 (period 2024 qx held fixed: a period life-table survival, not a cohort one)
rows = []
for sx in ('males', 'females'):
    s = 1.0; out = {}
    for a in range(65, 101):
        if a in (75, 85, 95): out[a] = s
        s *= 1 - Q[(sx, a, 2024)]
    rows.append([sx, round(out[75], 4), round(out[85], 4), round(out[95], 4), 'period qx 2024 applied from age 65 (a period life-table survival; the cohort qx file starts at births 1981 so it cannot be used for people now of retirement age)'])
write('survival_from_65_period2024.csv', ['sex', 'survive_65_to_75', 'survive_65_to_85', 'survive_65_to_95', 'note'], rows)
# tolerance: spot checks recorded by 098r
check('qx males 65 2024', abs(Q[('males', 65, 2024)] * 1e5 - 1164.76) < 0.01)
check('pop males 65 2030', abs(P[('Males', 65, 2030)] - 415319) < 1)
if FAIL:
    print('TOLERANCE FAILURES'); [print(' ', f) for f in FAIL]; sys.exit(1)
print('ok: all stated tolerances met')
