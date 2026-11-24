"""103r block 2: numeric consistency checks across the flows side (101r) and the stocks side (102r).

Reads committed CSVs, the register text and the pack CPI only; derives nothing new beyond the arithmetic shown in each row.
Writes cross_side_checks.csv and worked_cell_d45.csv. Hard checks (HARD) must pass or the script exits 1; the others report
a difference and its class (definitional, coverage, timing, measurement). Tolerances are reporting thresholds stated per row;
none was chosen with regard to WDT revenue. Run from the repository root with python -I.
"""
import csv, re, sys
DIRS = {'101r': 'research/tables/101r-parameter-map-flows-and-returns/', '102r': 'research/tables/102r-parameter-map-stocks-and-cells/', '103r': 'research/tables/103r-parameter-map-assembly/'}   # 160c: the tables moved here (docs/restructure map)
O = DIRS['103r']
def rd(p): return list(csv.DictReader(open(p)))
reg = {r['row_id']: r for r in rd(O + 'parameter_register.csv')}
der = {}
for r in rd(DIRS['101r'] + 'derived_ons_flows.csv'): der[(r['item'], int(r['year']))] = float(r['value'])
jst = {(r['period_or_check'], r['item']): r for r in rd(DIRS['101r'] + 'jst_split_stats.csv')}
nbs = rd(DIRS['102r'] + 'nbs_vs_was_r8.csv')
ct = rd(DIRS['102r'] + 'capital_transfers_s14.csv')
debt = {r['debt_type']: float(r['gb_total_gbp_bn']) for r in rd(DIRS['102r'] + 'debt_gb_totals.csv')}
comp = {r['pack_band']: r for r in rd(DIRS['102r'] + 'band_composition_by_pack_band.csv') if r['round'].startswith('April 2020')}
cpi = {int(r['year']): float(r['cpi']) for r in rd('model_v3/pack/GBR/returns.csv') if r['cpi']}
inputs = open('docs/model-v3/inputs.md').read()
out, fails = [], []
def add(i, check, a, va, b, vb, diff, tol, res, cls, note, hard=False):
    out.append(dict(check_id=i, check=check, side_a=a, value_a=va, side_b=b, value_b=vb, difference=diff, tolerance=tol, result=res, difference_class=cls, note=note))
    if hard and res != 'PASS': fails.append(i)
f = lambda x, n=3: ('%.' + str(n) + 'f') % x

# C01 pension rows on one stated basis each
basis = {}
for r in reg.values():
    if r['pension_basis']: basis.setdefault(r['pension_basis'], []).append(r['row_id'])
ok = all(reg[i]['pension_basis'] == 'ONS-NA' for i in ('F-10', 'F-11', 'F-12', 'F-13')) and all(reg[i]['pension_basis'] == 'WAS-R8' for i in ('S05', 'S06', 'S07', 'S08')) \
     and all('validation' in reg[i]['intended_use'].lower() for i in basis.get('RF', []))
add('C01', 'Every pension row carries one stated basis; the Resolution Foundation basis only in validation rows', 'rows by basis',
    '; '.join('%s %d' % (k, len(v)) for k, v in sorted(basis.items())), 'RF rows', ','.join(basis.get('RF', [])), '', 'exact', 'PASS' if ok else 'FAIL', 'none',
    'flows rows F-10 to F-13 are ONS national-accounts series; stock rows S05 to S08 are WAS Round 8 SCAPE-based; F-35 is the register of bases', hard=True)
# C02 mixed-basis ratio, reported so that it is not used
d8_2021 = der[('D8_pension_adj', 2021)] / 1000.0
was_pen = float(re.search(r'GBP ([\d,\.]+)bn', reg['S08']['value_or_range']).group(1).replace(',', ''))
add('C02', 'Pension accrual (ONS national-accounts D.8, 2021) over WAS Round 8 pension wealth (SCAPE-based): a mixed-basis ratio, not a rate', 'D.8 2021 GBP bn', f(d8_2021, 1),
    'WAS R8 private pensions GBP bn', f(was_pen, 1), f(100 * d8_2021 / was_pen, 2) + '% (mixed basis)', 'none', 'INFO', 'definitional',
    'numerator and denominator are on different bases and different periods (one year, a two-year wave); the AF.6 stock that would give a same-basis rate is not held (DR-01). Do not use as a growth or accrual rate')
# C03 accounting-location labels against 094r B2
c03 = []
if 'TR' in reg['F-03']['accounting_location'] and 'D.62' in reg['F-03']['variable']: c03.append('F-03 (social benefits D.62) is labelled TR; in 094r B2 TR is net capital transfers and benefits sit in T_C net of benefits')
if reg['F-21']['accounting_location'].startswith('O') and 'real' in reg['F-21']['accounting_location'].lower(): c03.append('F-21 (real erosion of nominal liabilities) is labelled O; in 094r B2 and B1 the real revaluation of nominal positions is a CG term')
add('C03', 'Accounting-location labels of the flows rows against the 094r B2 terms', 'flows rows', '36', 'flagged', str(len(c03)), '; '.join(c03), 'exact', 'FLAG' if c03 else 'PASS', 'definitional (labelling)',
    'labels only; the values are unaffected. Not edited here; reported for 104r (accounting conventions)')
# C04 JST split additive and reproduces the register total return
yg = float(jst[('all_1896_2019', 'portfolio_y_real')]['mean_or_value']) + float(jst[('all_1896_2019', 'portfolio_g_real')]['mean_or_value'])
tr = float(jst[('all_1896_2019', 'capital_tr_real')]['mean_or_value'])
reg_c = [c.strip() for c in re.search(r'\| I-D1a \|[^\n]*', inputs).group(0).split('|')][5]
add('C04', 'Cash yield plus holding gain equals the register total return (arithmetic, real)', 'y + g_h (JST, 1896-2019, pct)', f(yg, 4), 'I-D1a central (register, pct)', reg_c,
    f(yg - float(reg_c), 4), '0.005 (register is to 2 dp)', 'PASS' if abs(yg - float(reg_c)) <= 0.005 else 'FAIL', 'measurement',
    'JST additivity check in jst_split_stats.csv: max |y+g-tr| = 1.2e-8; the geometric I-D1a2 has no additive split', hard=True)
# C05 worked cell, band D4-5: pounds per 100 of opening wealth
band = comp['D4-5']
w = {k: float(band['share_' + k + '_pct']) for k in ('property', 'financial', 'physical', 'pension')}
yh = float(jst[('all_1896_2019', 'housing_y_real')]['mean_or_value']); gh = float(jst[('all_1896_2019', 'housing_g_real')]['mean_or_value'])
y_p, g_p = w['property'] * yh / 100, w['property'] * gh / 100
wc = [dict(asset_class=k, weight_pct_of_cell_wealth=w[k], pounds_cash_yield_per_100=(f(y_p) if k == 'property' else ''), pounds_holding_gain_per_100=(f(g_p) if k == 'property' else ''),
           status=('JST housing split (F-20); imputed rent included in the yield' if k == 'property' else
                   'no instrument split of net financial wealth in the pack or WAS tables held (S05); yield and gain by instrument not applicable' if k == 'financial' else
                   'pension return unset (F-12; DR-01)' if k == 'pension' else 'no return series for contents and vehicles held')) for k in w]
with open(O + 'worked_cell_d45.csv', 'w', newline='') as fh:
    ww = csv.DictWriter(fh, list(wc[0])); ww.writeheader(); ww.writerows(wc)
A = g_p                      # account: imputed rent is income and consumption (HFCE includes imputed rent), so S = 0 and dNW = CG
B = (y_p + g_p) - y_p        # total return credited to wealth, with the imputed-rent yield consumed: equals the account
B0 = y_p + g_p               # total return credited and nothing consumed (kernel with no consumption on this class)
C = B0 + y_p                 # total return credited and the yield also counted as retained saving
add('C05', 'Worked cell D4-5, property class, per GBP 100 of cell wealth: the account against crediting the total return', 'account: CG only (imputed rent is income and consumption, S = 0)', f(A),
    'total return credited, yield consumed', f(B),
    'yield not consumed: %s (excess %s); yield also counted in S: %s (excess %s)' % (f(B0), f(B0 - A), f(C), f(C - A)), '0.001', 'PASS' if abs(A - B) < 1e-9 else 'FAIL', 'none',
    'property weight %.1f%% x JST housing yield %.3f%% and gain %.4f%%. ONS household final consumption includes imputed rental of owner-occupiers (ONS, "Differences between ONS household expenditure statistics") and ONS income includes it (F-02), so it nets out of S. Financial, pension and physical classes (%.1f%%, %.1f%%, %.1f%% of the cell) cannot be run: see worked_cell_d45.csv' %
    (w['property'], yh, gh, w['financial'], w['pension'], w['physical']), hard=True)
# C06 net-worth roll-forward on the national-accounts side at the WAS wave years
tol = 0.01
yrs = sorted(y for (i, y) in der if i == 'O_residual_over_open_NW')
inside = [y for y in yrs if abs(der[('O_residual_over_open_NW', y)]) <= tol]
for y in (2020, 2021, 2024):
    v = der[('O_residual_over_open_NW', y)]
    add('C06.%d' % y, 'Opening net worth plus saving, other volume and financial revaluation against closing net worth (S.14), year %d' % y, 'dNW GBP bn', f(der[('dNW_S14', y)] / 1000, 1),
        'B.101g + B.102 + B.103 GBP bn', f((der[('B101g_saving_plus_capital_transfers', y)] + der[('B102_other_volume_fin', y)] + der[('B103_holding_gain_fin', y)]) / 1000, 1),
        'O = %s bn = %s%% of opening NW' % (f(der[('O_residual_dNW_less_B101g_B102_B103', y)] / 1000, 1), f(100 * v, 2)), '1% of opening NW (reporting threshold)',
        'PASS' if abs(v) <= tol else 'OUTSIDE', 'coverage', 'B.102 and B.103 are held for financial assets only; the non-financial revaluation (dwellings and land) sits in O (DR-05). %d of %d years in %d-%d are within the threshold' % (len(inside), len(yrs), yrs[0], yrs[-1]))
# C07 capital transfers: 101r identity against the 102r S.14 lines
byy = {}
for r in ct: byy.setdefault(int(r['year']), {})[r['series_id']] = float(r['gbp_million'])
chk = []
for y, s in sorted(byy.items()):
    if all(k in s for k in ('HAZC', 'HADR')) and ('B101g_saving_plus_capital_transfers', y) in der:
        a = der[('B101g_saving_plus_capital_transfers', y)] - der[('B8g_saving', y)]; b = s['HAZC'] - s['HADR']; chk.append((y, a, b, a - b))
mx = max(abs(c[3]) for c in chk)
add('C07', 'Net capital transfers: B.101g - B.8g (101r) against D.9r - D.9p (102r S16 lines), all years held', 'B.101g - B.8g, 2024 GBP m', f(dict((c[0], c[1]) for c in chk)[2024], 0),
    'HAZC - HADR, 2024 GBP m', f(dict((c[0], c[2]) for c in chk)[2024], 0), 'max |diff| over %d years = %s GBP m' % (len(chk), f(mx, 1)), '3 GBP m (as ID10 of 101r)', 'PASS' if mx <= 3 else 'FAIL', 'measurement',
    'transfers between households net out inside the sector; the lines here are with other sectors only (S16), so TR in the account is zero in aggregate', hard=True)
# C08 survey totals against national-account totals
n = {(r['nbs_year_end'], r['nbs_line']): r for r in nbs}
for y in ('2020', '2021'):
    r = n[(y, 'S.14 net worth B.90')]; a = float(r['nbs_gbp_bn']); b = float(r['was_r8_gbp_bn'])
    add('C08.' + y, 'WAS Round 8 total wealth (GB, 2020-22, SCAPE pensions) against NBS S.14 net worth (UK, end-%s)' % y, 'NBS S.14 B.90 GBP bn', f(a, 1), 'WAS R8 total GBP bn', f(b, 1),
        '%s bn = %s%% of NBS' % (f(b - a, 1), f(100 * (b - a) / a, 1)), 'none stated (definitions differ)', 'INFO', 'definitional and coverage',
        'pensions on the SCAPE basis against national-accounts entitlements; contents and vehicles in WAS; GB against UK; mid-wave against end-year. Not reconciled; not averaged (see 102r nbs_vs_was_r8.csv)')
tot = debt['personal financial debt'] + debt['personal property debt']
for y in ('2020', '2021'):
    r = n[(y, 'S.14 total financial liabilities AF.L')]; a = float(r['nbs_gbp_bn'])
    add('C09.' + y, 'ONS 3222 personal debt (GB, persons, summed over regions) against NBS S.14 financial liabilities AF.L, end-%s' % y, 'ONS 3222 GBP bn', f(tot, 1), 'NBS AF.L GBP bn', f(a, 1),
        '%s bn; ratio %s' % (f(tot - a, 1), f(tot / a, 2)), 'none stated', 'INFO', 'coverage and definitional',
        'the two measure different populations and instruments; no WAS aggregate gross debt is held (S12, S13 unset); not used as a debt input')
# C10 price basis: CPI (pack/JST index) against the ONS household final consumption deflator, annual inflation
diffs = []
for y in range(1999, 2020):
    if y in cpi and (y - 1) in cpi and ('pi_hfce_deflator', y) in der:
        diffs.append((y, 100 * (cpi[y] / cpi[y - 1] - 1), 100 * der[('pi_hfce_deflator', y)]))
dd = [a - b for _, a, b in diffs]
mean = sum(dd) / len(dd); mxa = max(abs(x) for x in dd); big = [y for (y, a, b) in diffs if abs(a - b) > 1.0]
add('C10', 'Annual inflation: pack CPI index (deflator of the JST real returns) against the ONS household final consumption deflator (F-21), %d-%d' % (diffs[0][0], diffs[-1][0]), 'mean CPI inflation pct', f(sum(a for _, a, _ in diffs) / len(diffs), 2),
    'mean HFCE deflator inflation pct', f(sum(b for _, _, b in diffs) / len(diffs), 2), 'mean diff %s pp; max |diff| %s pp; years beyond 1 pp: %s' % (f(mean, 2), f(mxa, 2), ','.join(map(str, big)) or 'none'),
    '1 pp (reporting threshold)', 'PASS' if not big else 'FLAG', 'definitional',
    'two deflators sit in the account: CPI converts the JST returns to real; the HFCE deflator converts the ONS liability revaluation (F-21). ONS flows and stocks are nominal GBP at current prices; ratios of same-year nominal quantities are unit-free; the 094r account is real')
cols = ['check_id', 'check', 'side_a', 'value_a', 'side_b', 'value_b', 'difference', 'tolerance', 'result', 'difference_class', 'note']
with open(O + 'cross_side_checks.csv', 'w', newline='') as fh:
    ww = csv.DictWriter(fh, cols); ww.writeheader(); ww.writerows(out)
import collections
print('checks=%d %s hard_failures=%d' % (len(out), dict(collections.Counter(r['result'] for r in out)), len(fails)))
for r in out: print(r['check_id'], r['result'], r['difference'][:110])
sys.exit(1 if fails else 0)
