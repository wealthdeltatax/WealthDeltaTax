"""104r block 2: worked cases for the recommended accounting conventions.
Reads: research/tables/103r-parameter-map-assembly/worked_cell_d45.csv, 102r/band_composition_by_pack_band.csv.
Writes next to this script: worked_d45_conventions.csv, worked_household_year.csv, worked_transfer_and_fund.csv, liquidity_by_band.csv.
Everything labelled illustrative is one invented household in thousand pounds, not data and not a band. Exits 1 if an identity fails.
Run from the repository root: python -I research/scripts/conventions_worked.py"""
import csv, sys
DIRS = {'102r': 'research/tables/102r-parameter-map-stocks-and-cells/', '103r': 'research/tables/103r-parameter-map-assembly/', '104r': 'research/tables/104r-parameter-map-design/'}   # 160c: the tables moved here (docs/restructure map)
O = DIRS['104r']
bad = []
def chk(name, a, b, tol=1e-9):
    if abs(a - b) > tol: bad.append(f'{name}: {a} vs {b}')
def out(name, header, rows):
    with open(O + name, 'w', newline='') as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)

# ---------- 1. D4-5 per 100 of cell wealth, property class, three treatments ----------
d45 = {r['asset_class']: r for r in csv.DictReader(open(DIRS['103r'] + 'worked_cell_d45.csv'))}
p = d45['property']; wt = float(p['weight_pct_of_cell_wealth']); y = float(p['pounds_cash_yield_per_100']); g = float(p['pounds_holding_gain_per_100'])
chk('yield = weight x 3.758%', y, round(wt * 0.03758, 3), 0.0006); chk('gain = weight x 1.6455%', g, round(wt * 0.016455, 3), 0.0006)
rows = [
  ['A recommended: credit holding gain only; saving carries the retained yield once', 'CG', g, 'S contribution of the yield', y, 'consumption of the imputed rent', -y, g, 'dNW from the property class', 'yield is income and consumption (ONS counts imputed rent in both), so it nets to 0 in S'],
  ['B equivalent: credit total return; saving defined net of the yield already credited', 'credit r = y + g_h', round(y + g, 3), 'S - yW (saving less the retained yield)', round(-y, 3), 'consumption of the imputed rent (inside S)', 0.0, g, 'dNW from the property class', 'same answer; the kernel growth step stays W(1+r) and c is replaced by (y - s)/(1+r)'],
  ['C wrong: credit total return and leave the imputed rent unconsumed', 'credit r', round(y + g, 3), 'S contribution', 0.0, '', 0.0, round(y + g, 3), 'dNW from the property class', f'overstates by {y:.3f}: the imputed rent never arrives as cash'],
  ['D wrong: credit total return and also count the yield as retained saving', 'credit r', round(y + g, 3), 'S contribution of the yield', y, '', 0.0, round(y + g + y, 3), 'dNW from the property class', f'overstates by {2 * y:.3f}: the yield counted twice (103r shows 3.436 and 2.819 from unrounded inputs)'],
]
for r in rows[:2]: chk('A and B agree', r[7], g)
chk('C excess', rows[2][7] - g, y, 0.0015); chk('D excess', rows[3][7] - g, 2 * y, 0.003)
out('worked_d45_conventions.csv', ['treatment', 'credit_line', 'credit_per_100', 'saving_line', 'saving_per_100', 'consumption_line', 'consumption_per_100', 'dNW_per_100', 'what', 'note'], rows)

# ---------- 2. illustrative household, one year, recommended conventions (A) ----------
H0, E0, M0, PA0, D0 = 600, 200, 100, 400, 200
NW0 = H0 + E0 + M0 + PA0 - D0
cpi, hfce = 0.020, 0.025
YL, emp_pc, ee_pc = 60.0, 4.0, 4.0           # labour compensation incl employer contribution 4; employee contribution 4
rent = 0.03 * H0                              # imputed rent, income and consumption, never cash
div, int_r, int_p = 0.03 * E0, 2.0, 0.04 * D0
fund_inc = 0.03 * PA0                         # retained inside the pension fund
TC, Ccash = 12.0, 40.0
C = Ccash + rent
gE, gH, gPA = 0.02 * E0, 0.02 * H0, 0.05 * PA0
cg_cash = -cpi * M0                           # real loss on cash, CPI numeraire
ero_hfce = hfce * D0                          # F-21 as ruled: expenditure deflator
ero_cpi = cpi * D0; wedge = ero_hfce - ero_cpi
Twdt = 5.0
S = (YL + rent + div + int_r + fund_inc) - int_p - TC - C
CG = gE + gH + gPA + cg_cash + ero_hfce
dNW_flow = S + CG + 0.0 - Twdt
Hn, En, PAn = H0 + gH, E0 + gE - Twdt, PA0 + emp_pc + ee_pc + fund_inc + gPA
cash_in = (YL - emp_pc) - ee_pc + div + int_r - int_p - TC - Ccash
Mn = M0 + cash_in + cg_cash
Dn = D0 - ero_hfce
NW1 = Hn + En + Mn + PAn - Dn
chk('household identity', NW1 - NW0, dNW_flow); chk('cash closes', cash_in, 0.0)
wrong_S = S + div + rent + fund_inc                 # credit total return to assets and keep yields in S
rows = [['opening net worth', NW0, 'H 600, E 200, M 100, PA 400, D 200'],
        ['Y_L labour compensation incl employer contribution 4', YL, ''], ['imputed rent on H (3%), income', rent, 'income and consumption; never cash'],
        ['dividends on E (3%), retained', div, ''], ['interest received', int_r, ''], ['pension fund retained income (3% of PA)', fund_inc, 'retained inside the fund'],
        ['interest paid on D (4%)', -int_p, 'nominal; the real erosion is in CG'], ['T_C ordinary taxes net of benefits', -TC, 'label fix F-03: benefits sit here, not in TR'],
        ['consumption C = cash 40 + imputed rent', -C, ''], ['S net saving (yields counted once)', S, ''],
        ['CG holding gains on E (2%), H (2%), PA (5%)', gE + gH + gPA, 'real; excludes the cash yield'], ['CG real loss on cash at CPI 2.0%', cg_cash, 'nominal asset'],
        ['CG real erosion of D at the expenditure deflator 2.5% (F-21 as a CG term)', ero_hfce, f'of which at CPI 2.0 percent: {ero_cpi:.1f}; deflator wedge {wedge:.1f} reported as its own line'],
        ['T_WDT paid by selling 5 of E', -Twdt, 'composition change plus a payment to the public sector'], ['dNW flow side S + CG + TR + O - T_WDT, with TR = 0 and O = 0', dNW_flow, ''],
        ['closing H, E, M, PA, D', f'{Hn:.0f}, {En:.0f}, {Mn:.0f}, {PAn:.0f}, {Dn:.0f}', ''], ['closing net worth', NW1, ''], ['dNW stock side', NW1 - NW0, 'equals the flow side'],
        ['wrong: total return credited to assets and the yields also left in S: dNW', dNW_flow + div + rent + fund_inc, f'overstates by {div + rent + fund_inc:.1f}: yields counted twice']]
out('worked_household_year.csv', ['line', 'value_thousand_gbp', 'note'], rows)

# ---------- 3. transfers between two households and the WDT payment to the fund ----------
gift = 30.0; wdt = Twdt
rows = [['household A gives 30 cash to household B', 'A', -gift, 'TR -30', ''], ['', 'B', gift, 'TR +30', ''], ['cell total TR (A + B)', 'A+B', 0.0, 'cancels', 'no new aggregate wealth'],
        ['WDT of 5 paid by A', 'A', -wdt, 'T_WDT 5', 'household dNW -5'], ['', 'public sector', wdt, 'asset or receipt of 5', 'public net worth +5'],
        ['household plus public sector dNW', 'A+B+public', 0.0 + (-wdt + wdt), 'zero', 'the payment is a transfer, not consumption (C and S unchanged)']]
chk('transfer nets', -gift + gift, 0.0); chk('wdt nets', -wdt + wdt, 0.0)
out('worked_transfer_and_fund.csv', ['event', 'unit', 'dNW_thousand_gbp', 'account_term', 'note'], rows)

# ---------- 4. liquidity by pack band (observed composition, WAS Round 8) ----------
R8 = 'April 2020 to March 2022'
comp = [r for r in csv.DictReader(open(DIRS['102r'] + 'band_composition_by_pack_band.csv')) if r['round'] == R8]
rows = []
for r in comp:
    tot = float(r['total_gbp_bn']); fin = float(r['net_financial_gbp_bn']); pen = float(r['private_pension_gbp_bn']); prop = float(r['net_property_gbp_bn']); phy = float(r['physical_gbp_bn'])
    chk('components ' + r['pack_band'], fin + pen + prop + phy, tot, 0.01)
    rows.append([r['pack_band'], round(tot, 1), round(fin / tot * 100, 1), round(prop / tot * 100, 1), round(phy / tot * 100, 1), round(pen / tot * 100, 1),
                 round((prop + pen) / tot * 100, 1), round(fin / (prop + pen) * 100, 1) if prop + pen else '',
                 'net financial wealth is the only held liquid class (no instrument split); pension and housing are not cash before they are drawn or sold; shares of band net worth'])
out('liquidity_by_band.csv', ['pack_band', 'total_gbp_bn', 'net_financial_pct', 'net_property_pct', 'physical_pct', 'pension_pct', 'pension_plus_property_pct', 'net_financial_per_100_of_pension_plus_property', 'note'], rows)
if bad:
    print('FAILED'); [print(' ', b) for b in bad]; sys.exit(1)
print('ok: household S=%.1f CG=%.1f dNW=%.1f NW1=%.1f' % (S, CG, dNW_flow, NW1))
