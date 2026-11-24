"""131r block 2: the pension valuation basis (IFS gilt discounting against ONS SCAPE) as a side table on the pack's starting stock.

Run: python -I research/scripts/basis_sensitivity.py
Reads (read-only): model_v3/pack/GBR/{wealth_distribution,decile_composition,band_composition}.csv, research/tables/102r-parameter-map-stocks-and-cells/band_composition_by_pack_band.csv (exact 2020-22 sums, a rounding diagnostic),
research/tables/131r-pension-basis-sensitivity/ifs_published.csv (block 1). Writes basis_sensitivity.csv (by decile, band and all) and basis_checks.csv. No pack, register or model file is written.

Method (all money in the pack's nominal 2020-22 pounds; the report's 2026 prices enter only as ratios, so no price index is needed):
 1. ONS column = the pack: band pension stock = band wealth_total x band_composition pension share (as model_v3/core/cells.py builds it).
 2. IFS compares total wealth after cutting home contents (physical wealth) by 75% in both measures (its footnote 20) and excluding business wealth. So the uplift in percent is on W_adj = W - 0.75 x physical.
    In 2020-22 the only difference between the two measures is the pension discount rate (report p17), so the uplift in pounds is a pension revaluation: pension_IFS = pension_ONS + uplift.
 3. Deciles 2 to 9: the percent uplift is read from Figure 4 at the decile edges (p10 ... p90, which are the chart's points); a decile takes the mean of its two edges (trapezoid), +-2 points (chart reading).
    Decile 1 (below p10) has no published value: unset (its uplift is bounded by the p10 reading, 4%, on a base of about zero); counted as 0.
 4. Decile 10 (above p90) has no published value either: closed by the published aggregate, uplift_D10 = (IFS total - ONS total, 22.3 and 16.3 trillion) x W_adj - the sum of deciles 2 to 9.
    Checks that the closure is sane: it must land near the published p90 uplift (34%) and reproduce the published top-10% share (42% under both).
 Quantile-matched, not household-matched: Figure 4 compares the p-th percentile under each measure, so a band here is 'the band of that rank under each basis'; re-ranking of households between the measures is not measured.
"""
import csv, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))                                                                # python -I does not add the folder; the model is imported read-only for check C1
PACK = ROOT / 'model_v3/pack/GBR'
HERE = ROOT / 'research/tables/131r-pension-basis-sensitivity'   # the 131r tables (was the folder of this script)
rd = lambda p: list(csv.DictReader(open(p, encoding='utf-8')))

wd = rd(PACK / 'wealth_distribution.csv')
W = {r['band']: float(r['value']) for r in wd if r['variable'] == 'wealth_total'}       # GBP bn, D1..D10, all
HH = {r['band']: float(r['value']) for r in wd if r['variable'] == 'households'}         # thousand
GDP = next(float(r['value']) for r in wd if r['variable'] == 'gdp')
DC = {(r['decile'], r['class']): float(r['value']) for r in rd(PACK / 'decile_composition.csv')}
BC = {(r['band'], r['class']): float(r['value']) for r in rd(PACK / 'band_composition.csv')}
EX = {r['pack_band']: r for r in rd(ROOT / 'research/tables/102r-parameter-map-stocks-and-cells/band_composition_by_pack_band.csv') if r['round'] == 'April 2020 to March 2022'}
IFS = {r['id']: r for r in rd(HERE / 'ifs_published.csv')}
v = lambda i: float(IFS[i]['value'])

BANDS = {'D1-3': (1, 2, 3), 'D4-5': (4, 5), 'D6-7': (6, 7), 'D8-9': (8, 9), 'D10': (10,)}
CUT = v('IFS-36') / 100                                                                    # home contents cut, both measures
PH = {d: W[f'D{d}'] * DC[(f'D{d}', 'physical')] / 100 for d in range(1, 11)}
WADJ = {d: W[f'D{d}'] - CUT * PH[d] for d in range(1, 11)}                                  # contents-adjusted ONS-basis decile wealth, GBP bn
WADJ_ALL = sum(WADJ.values())

# Figure 4 percentage-difference line at p10 ... p90 (read from chart, +-2 points); p30 and p90 agree with the text (49, 34)
U = {p: v('IFS-C%02d' % (p // 10)) / 100 for p in range(10, 100, 10)}
CHART_ERR = 0.02
# aggregate uplift: stated totals (one decimal, so +-0.05 tn) and the stated 37%
U_AGG = v('IFS-09') / v('IFS-08') - 1
U_AGG_LO, U_AGG_HI = (v('IFS-09') - .05) / (v('IFS-08') + .05) - 1, (v('IFS-09') + .05) / (v('IFS-08') - .05) - 1


def uplifts(shift, agg):
    """Decile uplifts in GBP bn for chart error `shift` (added to every chart reading) and aggregate uplift `agg`."""
    up = {1: 0.0}
    for d in range(2, 10):
        up[d] = (U[10 * (d - 1)] + U[10 * d] + 2 * shift) / 2 * WADJ[d]
    up[10] = agg * WADJ_ALL - sum(up[d] for d in range(1, 10))
    return up


mid, lo, hi = uplifts(0, U_AGG), uplifts(+CHART_ERR, U_AGG_LO), uplifts(-CHART_ERR, U_AGG_HI)   # lo: low D10 (lower deciles high, aggregate low); hi: high D10
PEN = {d: W[f'D{d}'] * DC[(f'D{d}', 'pension')] / 100 for d in range(1, 11)}                # decile pension stock, two-decimal shares
BPEN = {b: sum(W[f'D{d}'] for d in ds) * BC[(b, 'pension')] / 100 for b, ds in BANDS.items()}  # the pack's own band stock (cells.py): band wealth x band pension share (one decimal)
BW = {b: sum(W[f'D{d}'] for d in ds) for b, ds in BANDS.items()}
CLASS = {1: 'unset', **{d: 'proxy' for d in range(2, 10)}, 10: 'proxy'}

rows = []
def row(level, name, ds, pens_ons):
    w, wa = sum(W[f'D{d}'] for d in ds), sum(WADJ[d] for d in ds)
    u, ulo, uhi = (sum(x[d] for d in ds) for x in (mid, lo, hi))
    ulo, uhi = min(ulo, uhi), max(ulo, uhi)
    unset = ds == (1,)
    cls = 'unset' if unset else ('proxy' if all(CLASS[d] == 'proxy' for d in ds) else 'proxy (decile 1 unset, counted as 0)')
    rows.append(dict(level=level, band=name, wealth_ons_gbp_bn=round(w, 3), pension_ons_gbp_bn=round(pens_ons, 3), pension_share_ons_pct=round(100 * pens_ons / w, 2) if w else '',
                     contents_adjusted_wealth_ons_gbp_bn=round(wa, 3), uplift_gbp_bn=round(u, 3), uplift_low_gbp_bn=round(ulo, 3), uplift_high_gbp_bn=round(uhi, 3),
                     uplift_pct_of_adjusted_wealth=round(100 * u / wa, 2) if wa > 0 else '', pension_ifs_gbp_bn=round(pens_ons + u, 3), pension_multiplier=round((pens_ons + u) / pens_ons, 3),
                     wealth_ifs_gbp_bn=round(w + u, 3), pension_share_ifs_pct=round(100 * (pens_ons + u) / (w + u), 2), class_=cls,
                     mapping='Figure 4 decile-edge mean (chart, +-2 points)' if not unset and ds != (10,) else ('no published value: counted 0' if unset else 'closed by the published aggregate (22.3 over 16.3 trillion)')))
for d in range(1, 11):
    row('decile', f'D{d}', (d,), PEN[d])
for b, ds in BANDS.items():
    row('band', b, ds, BPEN[b])
row('all', 'all', tuple(range(1, 11)), sum(BPEN.values()))

fields = list(rows[0]); fields[fields.index('class_')] = 'class'
with (HERE / 'basis_sensitivity.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(fields)
    for r in rows: w.writerow([r[k if k != 'class' else 'class_'] for k in fields])

# ---------------------------------------------------------------- checks
allr = rows[-1]
P_ONS, P_IFS, W_ONS, W_IFS = allr['pension_ons_gbp_bn'], allr['pension_ifs_gbp_bn'], allr['wealth_ons_gbp_bn'], allr['wealth_ifs_gbp_bn']
HH_ALL = HH['all']                                                                           # thousand
K = v('IFS-08') * 1000 / WADJ_ALL                                                            # implied price factor, 2026 prices over 2020-22 pounds, from the stated ONS-basis aggregate
sh = lambda x, tot: x / tot
d10 = rows[9]
checks = []
def chk(name, got, want, tol, note=''):
    ok = abs(got - want) <= tol
    checks.append(dict(check=name, got=round(got, 4), expected=round(want, 4), tolerance=tol, passed=ok, note=note))
# C1: the ONS column equals the pension stock the model's own cell table starts from (model_v3.core.cells.cell_table, read-only import), in GBP bn, band by band and in total
from model_v3.core import cells as ce, pack as pk
_pack, _reg = pk.load_pack(ROOT / 'model_v3' / 'pack' / 'GBR'), pk.load_register(ROOT / 'registry' / 'inputs.json')
_cells = ce.cell_table(_pack, _reg, 0.44)
_model = {b: sum(c['households'] * c['pos']['pension'] for c in _cells if c['band'] == b) * ce.UNIT / 1e9 for b in BANDS}   # households x pension per household, thousands of pounds -> GBP bn
chk('C1a ONS column equals the model cell-table pension stock, largest band difference (GBP bn)', max(abs(_model[b] - BPEN[b]) for b in BANDS), 0.0, 1e-6, 'model_v3/core/cells.py cell_table(pack, register, 0.44); the retired fraction does not enter the stock')
chk('C1b ONS column total equals the model cell-table pension total (GBP bn)', P_ONS, sum(_model.values()), 1e-2, 'the CSV rounds to 3 decimals')
# C2: the pack's one-decimal band shares against the exact held sums (a rounding diagnostic, GBP bn)
exact = sum(float(EX[b]['private_pension_gbp_bn']) for b in BANDS)
chk('C2 pack stock against exact held 2020-22 sums (rounding of the 0.1 shares)', P_ONS, exact, 0.0025 * exact, 'tolerance 0.25% of the stock')
# C3: IFS 'ONS' mean pension wealth, from the pack stock and the implied price factor, against the stated 230,000
chk('C3 ONS-basis mean pension wealth (GBP 2026) against 230,000', P_ONS * 1e9 / (HH_ALL * 1e3) * K, v('IFS-02'), 5000, f'implied price factor {K:.4f} from 16.3tn over contents-adjusted pack wealth; stated to the nearest 10,000')
# C4: ONS-basis pension share of contents-adjusted wealth against the stated 38%
chk('C4 ONS-basis pension share of contents-adjusted wealth (pct) against 38', 100 * P_ONS / WADJ_ALL, v('IFS-04'), 0.5, 'tolerance is the rounding of a whole percent')
# C5: IFS-basis mean pension wealth against 450,000
chk('C5 IFS-basis mean pension wealth (GBP 2026) against 450,000', P_IFS * 1e9 / (HH_ALL * 1e3) * K, v('IFS-01'), 5000, 'tolerance is the rounding of a figure stated to the nearest 10,000; mostly consistency with the stated aggregate, since the uplift total is fixed by it')
# C6: IFS-basis pension share of contents-adjusted wealth against 54%
chk('C6 IFS-basis pension share of contents-adjusted wealth (pct) against 54', 100 * P_IFS / (WADJ_ALL + allr['uplift_gbp_bn']), v('IFS-03'), 0.5, 'tolerance is the rounding of a whole percent; not loosened after seeing the result')
chk('C11 IFS-basis mean total wealth, contents-adjusted (GBP 2026) against 830,000', (WADJ_ALL + allr['uplift_gbp_bn']) * 1e9 / (HH_ALL * 1e3) * K, v('IFS-05'), 5000, 'uses the same price factor; the published +37% and 830,000/600,000 = +38% differ by rounding')
# C7: the decile 10 closure lands near the published p90 uplift
u10 = d10['uplift_gbp_bn'] / WADJ[10]
_lo10, _hi10 = d10['uplift_low_gbp_bn'] / WADJ[10], d10['uplift_high_gbp_bn'] / WADJ[10]
chk('C7 the p90 reading 34% lies inside the decile 10 closure range (share of contents-adjusted D10)', v('IFS-19') / 100, (_lo10 + _hi10) / 2, (_hi10 - _lo10) / 2, f'closure {u10:.4f}, range {_lo10:.4f} to {_hi10:.4f}; the p90 point is the lower edge of D10, so a nearby value is expected, not equality')
# C8: top-10% share: ONS basis (contents-adjusted) and IFS basis against the published 42 and 42
s_ons, s_ifs = WADJ[10] / WADJ_ALL, (WADJ[10] + d10['uplift_gbp_bn']) / (WADJ_ALL + allr['uplift_gbp_bn'])
chk('C8a top-10% share, ONS basis, contents-adjusted, against 42', 100 * s_ons, v('IFS-20'), 0.5, 'pack decile 10 over pack total after the contents cut')
chk('C8b top-10% share, IFS basis, side table, against 42', 100 * s_ifs, v('IFS-20'), 0.5, 'a test of the closure: the published share is unchanged by the basis')
# C9: Figure 4 bars at p90 and p50 against the text: IFS bar minus ONS bar
chk('C9a Figure 4 p90 bars (IFS minus ONS, GBP) against 490,000', v('IFS-C12') - v('IFS-C13'), v('IFS-16'), 40000, 'chart reading')
chk('C9b Figure 4 p50 bars (IFS minus ONS, GBP) against 130,000', v('IFS-C10') - v('IFS-C11'), v('IFS-17'), 40000, 'chart reading')
# C10: published numbers against each other
chk('C10 aggregate ratio 22.3/16.3 against the stated 37%', 100 * U_AGG, v('IFS-07'), 0.75, 'rounding of the totals')
# C12: the published pension difference from the shares (54% of 22.3 minus 38% of 16.3, trillions, 2026 prices) against the published total difference (22.3 minus 16.3), within the combined rounding
_pd = v('IFS-03') / 100 * v('IFS-09') - v('IFS-04') / 100 * v('IFS-08')
_tol = .005 * v('IFS-09') + .005 * v('IFS-08') + .05 + .05 + .05                              # shares +-0.5 point, totals +-0.05 each (the total difference counts both)
chk('C12 published pension difference from the shares (tn, 2026 prices) against the published total difference 6.0', _pd, v('IFS-09') - v('IFS-08'), _tol, 'a test of the published figures against each other; the side table sits at the high end of both')
with (HERE / 'basis_checks.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(checks[0])); w.writeheader(); w.writerows(checks)

# headline ratios against the 125c rows (printed in the note, written here too)
head = [
 ('wealth_over_gdp_pack_definition_ons', W['all'] / GDP), ('wealth_over_gdp_pack_definition_ifs', W_IFS / GDP),
 ('wealth_over_gdp_pack_definition_ifs_low', (W['all'] + sum(lo.values())) / GDP), ('wealth_over_gdp_pack_definition_ifs_high', (W['all'] + sum(hi.values())) / GDP),
 ('wealth_over_gdp_contents_adjusted_ons', WADJ_ALL / GDP), ('wealth_over_gdp_contents_adjusted_ifs', (WADJ_ALL + allr['uplift_gbp_bn']) / GDP),
 ('top_decile_share_pack_definition_ons', W['D10'] / W['all']), ('top_decile_share_pack_definition_ifs', (W['D10'] + d10['uplift_gbp_bn']) / W_IFS),
 ('top_decile_share_contents_adjusted_ons', s_ons), ('top_decile_share_contents_adjusted_ifs', s_ifs),
 ('top_decile_share_pack_definition_ifs_low', (W['D10'] + d10['uplift_low_gbp_bn']) / (W['all'] + sum(lo.values()))), ('top_decile_share_pack_definition_ifs_high', (W['D10'] + d10['uplift_high_gbp_bn']) / (W['all'] + sum(hi.values()))),
 ('implied_price_factor_2026_over_2020_22', K), ('d10_uplift_pct_of_adjusted', 100 * u10),
]
with (HERE / 'basis_headline.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['quantity', 'value']); [w.writerow([k, round(x, 5)]) for k, x in head]
bad = [c['check'] for c in checks if not c['passed']]
print(f"basis_sensitivity.csv {len(rows)} rows; basis_checks.csv {len(checks)} checks, {len(checks) - len(bad)} pass" + (f"; FAILED: {'; '.join(bad)}" if bad else ''))
