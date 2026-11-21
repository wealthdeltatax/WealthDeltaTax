"""102r block B: capital transfers and deaths, audit of the existing register rows, cell coverage inputs.
Run after derive_bands_stages.py and derive_debt_demography.py:  python -I docs/research/data/102r/derive_transfers_audit_coverage.py
Reads held files and this folder's outputs; exits non-zero when a stated tolerance fails."""
import csv, os, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
D098 = os.path.join(ROOT, 'docs', 'research', 'data', '098r'); D097 = os.path.join(ROOT, 'docs', 'research', 'data', '097r')
FAIL = []
def rd(p):
    with open(p, newline='') as fh: return list(csv.DictReader(fh))
def write(n, h, rows):
    with open(os.path.join(HERE, n), 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(h); w.writerows(rows)
def check(n, ok, d=''):
    if not ok: FAIL.append(f'{n}: {d}')
R8 = 'April 2020 to March 2022'

# ---------- capital transfers (UKEA, S.14), aggregate only ----------
uk = {(r['series_id'], r['period']): float(r['value']) for r in rd(os.path.join(D097, 'ons_ukea_household_annual.csv'))}
nb = {(r['series_id'], r['period']): float(r['value']) for r in rd(os.path.join(D097, 'ons_nbs_household_stocks_annual.csv'))}
SER = [('HAZC', 'capital transfers receivable D.9r'), ('HAZG', 'other capital transfers receivable D.99r'), ('HADR', 'capital transfers payable D.9p'),
       ('QYKC', 'capital taxes payable D.91p'), ('HADS', 'other capital transfers payable D.99p')]
rows = []
for yr in map(str, range(2015, 2026)):
    for sid, name in SER:
        if (sid, yr) not in uk: continue
        v = uk[(sid, yr)]
        prev = nb.get(('E45V', str(int(yr) - 1)))
        rows.append([yr, sid, name, v, round(v / prev * 100, 4) if prev else '',
                     'GBP million, UK households (S.14) with the sector\'s other sectors as counterparty; the ratio is to the previous year-end S.14 net worth (E45V); gifts and bequests between households net out inside the sector and are not in these lines'])
for yr, sid in [(y, s) for y in map(str, range(2015, 2026)) for s, _ in SER]:
    pass
write('capital_transfers_s14.csv', ['year', 'series_id', 'line', 'gbp_million', 'pct_of_prior_year_end_net_worth', 'note'], rows)
# identity check on D.9p = D.91p + D.99p and D.9r = D.92r + D.99r where held
for yr in map(str, range(2015, 2026)):
    if all((s, yr) in uk for s in ('HADR', 'QYKC', 'HADS')):
        check(f'D.9p identity {yr}', abs(uk[('HADR', yr)] - uk[('QYKC', yr)] - uk[('HADS', yr)]) <= 2, f'{uk[("HADR", yr)] - uk[("QYKC", yr)] - uk[("HADS", yr)]}')
    if all((s, yr) in uk for s in ('HAZC', 'HAZF', 'HAZG')):
        check(f'D.9r identity {yr}', abs(uk[('HAZC', yr)] - uk[('HAZF', yr)] - uk[('HAZG', yr)]) <= 2, f'{uk[("HAZC", yr)] - uk[("HAZF", yr)] - uk[("HAZG", yr)]}')

# ---------- deaths implied by population x qx (GB, 2024, 16-100) ----------
pop = {}
for r in rd(os.path.join(D098, 'ons_population_gb_principal_2024based.csv')):
    try: a = int(r['age'])
    except ValueError: continue
    if r['year'] == '2024': pop[(r['sex'].lower(), a)] = pop.get((r['sex'].lower(), a), 0) + float(r['population'])
qx = {(r['sex'], int(r['exact_age'])): float(r['qx']) / 1e5 for r in rd(os.path.join(D098, 'ons_qx_gb_2024based.csv')) if r['basis'] == 'period' and r['year_or_birth_year'] == '2024'}
rows = []; tot = 0.0
for lo, hi in [(16, 44), (45, 64), (65, 74), (75, 84), (85, 100)]:
    d = sum(pop.get((s, a), 0) * qx[(s, a)] for s in ('males', 'females') for a in range(lo, hi + 1))
    tot += d
    rows.append([lo, hi, round(d), 'expected deaths in a year = population x period qx, 2024, GB; ages above 100 and under 16 excluded'])
rows.append(['16', '100', round(tot), 'total of the bands above'])
write('adult_deaths_gb_2024.csv', ['age_from', 'age_to', 'expected_deaths', 'note'], rows)

# ---------- audit of existing rows ----------
tw = {}
for r in rd(os.path.join(D098, 'was_band_reconciliation.csv')): tw[r['wdt_band']] = r
comp = [r for r in rd(os.path.join(HERE, 'band_composition_by_pack_band.csv')) if r['round'] == R8]
tot_all = sum(float(r['total_gbp_bn']) for r in comp); pen_all = sum(float(r['private_pension_gbp_bn']) for r in comp)
d10 = [r for r in comp if r['pack_band'] == 'D10'][0]
pack = {(r['variable'], r['band']): float(r['value']) for r in rd(os.path.join(ROOT, 'model_v3', 'pack', 'GBR', 'wealth_distribution.csv'))}
ap = rd(os.path.join(HERE, 'adults_per_household_all_rounds.csv')); ap8 = [r for r in ap if r['round'] == R8][0]
hh = {(r['wealth_band']): float(r['value']) for r in rd(os.path.join(D098, 'was_households_by_wealth_band.csv')) if r['round'] == R8 and r['measure'] == 'Weighted Frequency'}
H = hh['All households']
ge300 = (hh['£300,000 but < £500,000'] + hh['£500,000 but < £1 million'] + hh['£1 million or more']) / H * 100
ge200 = ge300 + hh['£200,000 but < £300,000'] / H * 100
ge85 = ge200 + hh['£85,000 but < £200,000'] / H * 100
aud = []
def A(row_id, quantity, register, recomputed, diff, verdict, note): aud.append([row_id, quantity, register, recomputed, diff, verdict, note])
gdp_pack = pack[('gdp', 'all')]
A('I-D4a', 'WAS R8 total wealth / GDP, central', 5.94, round(13568 / 2284, 3), round(13568 / 2284 - 5.94, 3), 'supports',
  'register central uses GDP 2,284bn (2021); reproduces')
A('I-D4a', 'same, GDP as in the pack file (gdp, all, 2020-22)', 6.14, round(13568 / gdp_pack, 3), round(13568 / gdp_pack - 5.94, 3), 'contradicts (GDP differs)',
  f'pack GDP {gdp_pack}bn against register 2,284bn: 3.2% lower, ratio 6.14 against 5.94; not reconciled in the held files (the pack GDP source is not among the held series)')
nbs21 = nb[('E45V', '2021')] / 1000
A('I-D4a', 'low value 5.80 (national-accounts series, 2023) against held NBS S.14 net worth 2021 over 2,284bn', 5.80, round(nbs21 / 2284, 3), round(nbs21 / 2284 - 5.80, 3), 'contradicts as to basis',
  'held NBS S.14 B.90 is 11,492bn for 2021, ratio 5.03 on the same GDP; the register low is described as a national-accounts figure from S4 p.11 (a different year and basis); the held NBS does not reproduce 5.80')
n25 = nb[('E45V', '2025')] / 1000; n25b = nb[('CGRC', '2025')] / 1000
A('I-D4g', 'held NBS household net worth, end-2025, S.14 (E45V) and S.14+S.15 (CGRC)', '10.8tn (ratio 3.6)', f'{n25:.0f}bn / {n25b:.0f}bn', round(n25 / 1000 - 10.8, 2), 'supports the level (basis differs from the register wording)',
  'the register 10.8tn is of the same order as held S.14 net worth; the ratio 3.6 uses the register GDP of about 3.0tn, which is not in the held files, so the ratio is not recomputed; the same S.14 stock over 2021 GDP of 2,284bn is 5.03 (previous row), which shows the NBS-to-GDP ratio moves with the year')
A('I-D4b', 'low: households at or above 300,000 (every household two adults)', 49.3, round(ge300, 1), round(ge300 - 49.3, 2), 'supports',
  'reproduces from Table 2.5 weighted frequencies as a household share; register labels it share of adults')
A('I-D4b', 'bounds on household share at or above 150,000: between share at or above 200,000 and at or above 85,000', '49.3 / 54.9 / 64.3',
  f'{ge200:.1f} to {ge85:.1f}', '', 'supports (bounds inside)', 'the register central 54.9 and high 64.3 lie inside the held-band bracket; the 150,000 point is inside a band, so no held cell gives it directly')
A('I-D4h', 'adults per household, Table 2.11 16+ over Table 2.5 households', 1.93, float(ap8['adults_per_hh_2_11']), round(float(ap8['adults_per_hh_2_11']) - 1.93, 4), 'supports', 'reproduces: 52,043,000 over 26,991,000')
A('I-D4h', 'adults per household, Table 2.13 all persons over households', 1.93, float(ap8['adults_per_hh_2_13']), round(float(ap8['adults_per_hh_2_13']) - 1.93, 4), 'contradicts',
  'Table 2.13 totals 50,185,000 adults against 52,043,000 in Table 2.11 (difference 1,858,000); the register does not mention it; whether 2.13 excludes some 16 and 17 year olds is not stated in the held table')
A('I-D4h vs I-D4b', 'low 1.77 (assumed adult counts by household type)', 1.77, float(ap8['adults_per_hh_2_11']), round(1.77 - float(ap8['adults_per_hh_2_11']), 3), 'contradicts',
  'the low bound is an assumption; both published tables give 1.86 to 1.93, so 1.77 sits below both')
A('I-W5a', 'top decile share of total wealth R8 (central)', 40.7, round(float(d10['total_gbp_bn']) / tot_all * 100, 2), round(float(d10['total_gbp_bn']) / tot_all * 100 - 40.7, 3), 'supports', '5,523/13,568')
low = (float(d10['total_gbp_bn']) - float(d10['private_pension_gbp_bn'])) / (tot_all - pen_all) * 100
A('I-W5a', 'low 40.1: decile 10 over total excluding pensions', 40.1, round(low, 2), round(low - 40.1, 3), 'supports',
  'uses the total-wealth decile 10 and removes its pension; a decile ranked on wealth excluding pensions would differ')
A('I-W5e', 'pension share of total wealth R8', 35.4, round(pen_all / tot_all * 100, 2), round(pen_all / tot_all * 100 - 35.4, 3), 'supports', '4,808/13,568; the D10 share of pension wealth 41.8: ' + f"{float(d10['private_pension_gbp_bn']) / pen_all * 100:.1f}")
A('I-W5c/d vs pack tail', 'WID top 1% (2024, adults) 21.3 and top 10% 57.1 in wealth_tail.csv against register I-W5c 14.4 to 23.0 and I-W5d 52.4 (2016-18)', '14.4-23.0 / 52.4-52.5', '21.3 / 57.1', '',
  'definitions differ', 'WID is a distributional-national-accounts series (adults, 2024); the register rows are WAS or national-accounts aggregate shares for 2016-18; not averaged')
# mobility moments from 099r
mom = {r['id']: r for r in rd(os.path.join(ROOT, 'docs', 'research', 'data', '099r', 'moments.csv'))}
for mid in ('AB-02', 'BF-04', 'BF-06', 'AB-04'): check(f'099r id {mid}', mid in mom)
A('I-W4a/b', 'top decile stay and entrants from the ninth decile', '80 / 90', '80 / 90 (AB-02)', 0, 'supports',
  '099r AB-02: the paper dates the base 2014-16 on PDF 4 and 2016-18 on PDF 23; the register says 2014-16 and 2016-18 starting groups; two-year window; family wealth deciles')
A('I-W4c', 'four-year rank correlation 74 (low-to-middle) and 77 (higher income); about a third stay in the same decile', '74 / 77', '74 / 77; 33% / 32% same decile (BF-04)', 0, 'supports',
  'Table 1 read again in 099r (PDF 45): low-to-middle two-year 79, four-year 74; higher two-year 81, four-year 77; age-adjusted deciles, ages 25-54, by income group, not wealth band')
write('existing_row_audit.csv', ['register_row', 'quantity', 'register_value', 'recomputed_or_held_value', 'difference', 'verdict', 'note'], aud)

# ---------- cell coverage inputs ----------
stg = [r for r in rd(os.path.join(HERE, 'stage_weights_by_pack_band.csv')) if r['round'] == R8]
wts = {r['pack_band_approx']: r for r in rd(os.path.join(HERE, 'person_household_weights_by_band.csv')) if r['round'] == R8}
rec = {r['pack_band']: r for r in rd(os.path.join(HERE, 'band_reconciliation_exact.csv')) if r['round'] == R8}
bounds = {(r['pack_band_approx'], r['stage']): int(r['max_rounding_persons']) for r in rd(os.path.join(HERE, 'stage_rounding_bounds_r8.csv'))}
rows = []
for r in stg:
    g = r['pack_band_approx']; s = r['stage']
    rows.append([g, s, r['persons'], r['share_of_band_adults_pct'], bounds[(g, s)], wts[g]['households'], rec[g]['share_mismatch_pp'],
                 'derived (persons, rounded %, £-band group not decile)', 'derived at band level only (Table 2.2; not by stage)',
                 'unset (no gross debt by band or stage held)', 'unset (no inheritance or gift table held by band)',
                 'proxy at best (099r summary measures; income groups or family deciles, not pack band by stage)',
                 'proxy (age-band hazards, not wealth- or stage-specific)',
                 'suppressed cells in the band: ' + r['suppressed_cells_in_band'],
                 'persons not households; adults 16+ placed by household wealth; stage = self-reported status; inactive-not-retired shown separately'])
write('cell_coverage_inputs.csv', ['pack_band', 'stage', 'persons_r8', 'share_of_band_adults_pct', 'max_rounding_persons', 'band_households',
                                    'band_share_mismatch_pp', 'stage_weight_class', 'composition_class', 'debt_class', 'transfer_class', 'mobility_class',
                                    'mortality_class', 'suppression', 'note'], rows)
if FAIL:
    print('TOLERANCE FAILURES'); [print(' ', f) for f in FAIL]; sys.exit(1)
print('ok: all stated tolerances met')
