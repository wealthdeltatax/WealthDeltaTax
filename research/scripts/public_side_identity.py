"""104r block 3: one public-side ledger and its reconciliation to the household account, illustrative numbers.
Two years, one household paying a WDT of 5 (thousand pounds, the worked household of conventions_worked.py), holdings in one asset class
(equity-like units, price index 1.00 at payment, holding gain 2% and cash yield 3% in the second year). Not data, not a band, no rate of tax.
Writes public_side_identity.csv; exits 1 if the identity fails.  Run from the repository root: python -I research/scripts/public_side_identity.py"""
import csv, sys
DIRS = {'104r': 'research/tables/104r-parameter-map-design/'}   # 160c: the tables moved here (docs/restructure map)
O = DIRS['104r']
bad = []
def chk(n, a, b, tol=1e-9):
    if abs(a - b) > tol: bad.append(f'{n}: {a} vs {b}')
T = 5.0; g_h = 0.02; y = 0.03
rows = []
for label, R_to_hh, payment_form in [('cash settlement: household sells 5 units to the market and pays 5 cash; the ledger buys 5 units', 0.0, 'cash'),
                                     ('in-kind: household transfers 5 units to the ledger', 0.0, 'in kind'),
                                     ('cash settlement with a payout R = 0.10 to households as a transfer in year 2', 0.10, 'cash')]:
    # year 1 (payment at year end): household -T; ledger +T; market counterparty 0 for cash settlement (it sells 5 units and receives 5 cash, then
    # sells them back to the ledger: units and cash cancel), 0 in kind
    hh1, pub1, mkt1 = -T, +T, 0.0
    chk('year1 sum ' + label, hh1 + pub1 + mkt1, 0.0)
    # year 2 against the counterfactual in which the household kept the 5 units
    hh_cf = T * (g_h + y)                      # the household forgoes gain and retained yield on 5 units
    pub_gain, pub_yield = T * g_h, T * y
    pub2 = pub_gain + pub_yield - R_to_hh      # retained ledger change; the payout leaves the ledger
    hh2 = -hh_cf + R_to_hh                     # forgone return plus the payout received as income
    rows.append([label, 1, hh1, pub1, mkt1, round(hh1 + pub1 + mkt1, 10), 'payment of the WDT: a transfer, no wealth created'])
    chk('year2 sum ' + label, hh2 + pub2, 0.0)
    rows.append([label, 2, round(hh2, 10), round(pub2, 10), 0.0, round(hh2 + pub2, 10),
                 'against the counterfactual household that kept the units; payout R is public out, household in'])
    if payment_form == 'cash':
        # market counterparty: buys 5 units from the household and sells 5 units to the ledger at the same price: composition only
        chk('market net units', 5.0 - 5.0, 0.0)
# the legacy representation: stake units grow at g and the fund recursion earns r; they agree only if r equals the stake's total return and no payout
stake2 = T * (1 + g_h + y); fund2 = T * (1 + g_h + y)
chk('two representations agree here', stake2, fund2)
rows.append(['legacy kernel and revenue code, same case with the same return', 2, '', '', '', round(stake2 - fund2, 10),
             'agree by construction when one return is used and no payout; they are separate recursions with no test that ties them (094r A3)'])
with open(O + 'public_side_identity.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['case', 'year', 'household_dNW_vs_no_wdt', 'public_ledger_dNW', 'market_counterparty_dNW', 'sum', 'note']); w.writerows(rows)
if bad:
    print('FAILED'); [print(' ', b) for b in bad]; sys.exit(1)
print('ok: %d rows, every consolidated sum is zero' % len(rows))
