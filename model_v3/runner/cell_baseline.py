"""Brief 110c, block 1: the ten cells' starting inputs for the untaxed baseline run, and the units reconciliation. Standalone: nothing imports this module.

A cell is a pack wealth band times a stage (not retired, retired). Every number is built from the pack and the register rows passed in; nothing is read here.
Units: wealth and income in pounds bn (pack basis: 2020-22 wealth, FYE 2024 income level, no uplift), persons in persons, households in thousands.
Author decisions (brief 110c): the band income is the register's band mean household income; the lowest band (D1-3) takes the D4-5 low bound; a retired
cell takes a labelled retired fraction of the not-retired income. Stage shares of a band's wealth and households follow the person shares of cell_weights
(an assumption: the pack gives no wealth by stage). Class shares are the pack's % of band wealth (property, net_financial, physical, pension).
"""
from __future__ import annotations

from model_v3.core.household import household_step

BANDS = ('D1-3', 'D4-5', 'D6-7', 'D8-9', 'D10')
STAGES = ('not retired', 'retired')
CLASSES = ('property', 'net_financial', 'physical', 'pension')
DECILES = {'D1-3': ('D1', 'D2', 'D3'), 'D4-5': ('D4', 'D5'), 'D6-7': ('D6', 'D7'), 'D8-9': ('D8', 'D9'), 'D10': ('D10',)}
INCOME_ID = {'D4-5': 'I-D9a', 'D6-7': 'I-D9b', 'D8-9': 'I-D9c', 'D10': 'I-D9d'}


def _wd(pack, variable, band):
    (r,) = [x for x in pack.tables['wealth_distribution'] if x['variable'] == variable and x['band'] == band]
    return r['value']


def band_income(reg, band, level='central'):
    """Mean household income of a band, pounds per year; D1-3 takes the D4-5 low bound."""
    if band == 'D1-3':
        return reg['I-D9a'].low
    return getattr(reg[INCOME_ID[band]], level)


def build_cells(pack, reg, retired_fraction=0.6, level='central'):
    """The ten cells as dicts: persons, households (thousand), wealth by class (pounds bn), income (pounds bn per year), per-household and per-person means."""
    if not 0.0 < retired_fraction <= 1.5:
        raise ValueError(f'retired_fraction must be in (0, 1.5], got {retired_fraction!r}')
    weights = {(r['band'], r['stage']): r['persons'] for r in pack.tables['cell_weights']}
    raw = {(r['band'], r['class']): r['value'] for r in pack.tables['band_composition']}
    comp = {(b, k): raw[(b, k)] / sum(raw[(b, j)] for j in CLASSES) for b in BANDS for k in CLASSES}   # the pack's rounded shares, rescaled to sum to 1
    cells = []
    for b in BANDS:
        persons = {s: weights[(b, s)] for s in STAGES}
        share = {s: persons[s] / sum(persons.values()) for s in STAGES}
        hh_band = sum(_wd(pack, 'households', d) for d in DECILES[b])                       # thousand
        wealth_band = sum(_wd(pack, 'wealth_total', d) for d in DECILES[b])                  # pounds bn
        norm = share['not retired'] + retired_fraction * share['retired']                    # keeps the band mean income equal to the register's
        y_nr = band_income(reg, b, level) / norm
        for s in STAGES:
            hh = hh_band * share[s]
            y = y_nr * (retired_fraction if s == 'retired' else 1.0)
            w = wealth_band * share[s]
            cells.append(dict(
                band=b, stage=s, cell=f'{b}|{s}', persons=persons[s], households_k=hh,
                pos={k: w * comp[(b, k)] for k in CLASSES}, wealth=w,
                income=hh * 1e3 * y / 1e9, income_per_hh=y, wealth_per_hh=w * 1e9 / (hh * 1e3), wealth_per_person=w * 1e9 / persons[s]))
    return cells


def scale_income(cells, target_bn):
    """Aggregate-constrained cells: every cell's income times one factor so the total equals target_bn; band proportions and the retired split are kept."""
    k = target_bn / sum(c['income'] for c in cells)
    return [dict(c, income=c['income'] * k, income_per_hh=c['income_per_hh'] * k, income_scale=k) for c in cells]


def reconcile(cells, pack, b6g_bn, d8_bn=0.0):
    """Cell totals against the pack and the national accounts; the gaps are reported, never forced. b6g_bn: national-accounts disposable income B.6g (pounds bn); d8_bn: pension adjustment D.8."""
    wealth, income = sum(c['wealth'] for c in cells), sum(c['income'] for c in cells)
    pack_all = _wd(pack, 'wealth_total', 'all')
    deciles = sum(_wd(pack, 'wealth_total', f'D{i}') for i in range(1, 11))
    gdp = _wd(pack, 'gdp', 'all')
    return dict(
        wealth_cells=wealth, wealth_pack_all=pack_all, wealth_deciles=deciles, wealth_gap_pct=100 * (wealth / pack_all - 1),
        wealth_over_gdp=wealth / gdp, pack_wealth_over_gdp=pack_all / gdp, gdp=gdp,
        households_k=sum(c['households_k'] for c in cells), households_pack_k=_wd(pack, 'households', 'all'),
        income_cells=income, b6g=b6g_bn, b6g_plus_d8=b6g_bn + d8_bn, income_gap_pct=100 * (income / b6g_bn - 1),
        income_gap_incl_d8_pct=100 * (income / (b6g_bn + d8_bn) - 1), income_over_gdp=income / gdp,
        persons=sum(c['persons'] for c in cells))


CLASS_KEY = {'property': 'property', 'net_financial': 'financial', 'physical': 'physical', 'pension': 'pension'}


def run_cells(cells, sc, years=100, convention='A'):
    """Run the cells forward `years` untaxed (T_WDT = 0) with household_step; one dict per cell and year (year 0 is the opening position).
    sc: s (non-pension saving ratio of cell income, a fraction), g and y (class -> real gain and yield), pen (pension accrual as a fraction of opening
    net worth), gdp_g (cell income grows with real GDP), r and c (the legacy total return and consumption share), arm 'new' or 'legacy'.
    Income is Y_L, consumption is (1 - s) of it, pension accrual is Y_P and goes straight to the pension class, so the sink receives s x income."""
    out, defl = [], dict(cpi=0.0, hfce=0.0)
    for c in cells:
        pos = {CLASS_KEY[k]: v for k, v in c['pos'].items()} if sc['arm'] == 'new' else dict(financial=c['wealth'])
        out.append(dict(cell=c['cell'], year=0, **pos, nw=sum(pos.values()), dNW=0.0, S=0.0, CG=0.0, wedge=0.0, O=0.0, resid=0.0, income=c['income']))
        for t in range(1, years + 1):
            nw0, inc = sum(pos.values()), c['income'] * (1.0 + sc['gdp_g']) ** (t - 1)
            if sc['arm'] == 'legacy':
                pos, a = household_step(c['cell'], pos, dict(c=sc['c']), dict(r=sc['r']), defl, 'legacy')
            else:
                pen = sc['pen'] * nw0
                flows = dict(Y_L=inc, Y_P=pen, C=(1.0 - sc['s']) * inc, pen_in=pen)
                pos, a = household_step(c['cell'], pos, flows, dict(g=sc['g'], y=sc['y']), defl, convention, sink='financial')
            nw1 = sum(pos.values())
            out.append(dict(cell=c['cell'], year=t, **{k: float(v) for k, v in pos.items() if k != 'debt'}, nw=float(nw1), dNW=float(a['dNW']), S=float(a['S']),
                            CG=float(a['CG']), wedge=float(a['CG_wedge']), O=float(a['O']), resid=float(abs(nw1 - nw0 - a['dNW'])), income=float(inc)))
    return out


def aggregate(rows, years, gdp0, gdp_g):
    """Aggregate by year (sum over cells, pounds bn, household basis: no person or household weights are needed for a sum): wealth, wealth/GDP indexed to
    year 0, realised saving ratio (S over income), the wealth share of each band, and the largest identity residual."""
    by = {y: [r for r in rows if r['year'] == y] for y in years}
    w0 = sum(r['nw'] for r in by[0])
    out = []
    for y, rs in by.items():
        w, inc = sum(r['nw'] for r in rs), sum(r['income'] for r in rs)
        gdp = gdp0 * (1.0 + gdp_g) ** y
        band = {b: sum(r['nw'] for r in rs if r['cell'].split('|')[0] == b) / w for b in BANDS}
        out.append(dict(year=y, wealth=w, wealth_over_gdp=w / gdp, wealth_over_gdp_index=(w / gdp) / (w0 / gdp0),
                        saving_ratio=(sum(r['S'] for r in rs) / inc if y else float('nan')), resid=max(r['resid'] for r in rs), **{f'share_{b}': v for b, v in band.items()}))
    return out
