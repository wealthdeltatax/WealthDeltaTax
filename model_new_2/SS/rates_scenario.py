"""
rates_scenario.py — RATES rebuild, L1 calibration + scenario builder
=====================================================================
Converts one (country, start year, horizon) window of JST history into the
arrays the engine consumes, and expresses the wealth distribution and rate
function in UNITS OF GDP PER CAPITA so that nothing in the model is tied to a
country's currency or to a £ amount.

UNITS
-----
All wealth, thresholds and tax in the engine are in units of y0 = GDP per
capita at the START of the window (nominal or real, according to `basis`).
Revenue is converted to a share of GDP using the within-window growth of GDP
per capita (`yy`) and the population/adult ratio.

    revenue / GDP  =  tax_per_adult / ( yy_t * pop_per_adult )
    mean wealth per adult (units of y0) = wealth_to_gdp * pop_per_adult

BASIS
-----
  basis='real'     returns, delta and threshold are all in real terms
                   (deflated by the country's CPI).  The tax base excludes
                   inflation.  Conservative, and the default.
  basis='nominal'  nominal returns; the delta includes inflation.

THRESHOLD INDEXATION (Phase One calibration parameter; swept)
-------------------------------------------------------------
tau is applied to W / idx_t where idx_t compounds the chosen index:
  'cpi'     prices.  Real basis: idx = 1 (real threshold constant).
  'gdp_pc'  GDP per capita growth.  Real threshold grows with real income.
  'wealth'  growth of mean wealth of an untaxed holder: (1 + r)(1 - c) - 1.
  'none'    no indexation (nominal threshold fixed; in real basis it
            is eroded by inflation only if basis='nominal').
W_min and k are indexed together, so tau keeps its shape (valgen D16).

WINDOW CONVENTION
-----------------
Window = data years start .. start+T-1.  Simulation year t (1..T) uses data
year start+t-1.  Wealth V0 is measured at the start of year `start` against
GDP per capita at the end of year start-1 (so the first year's growth applies
to both).  This is an approximation of a few percent in the first year only.

CALIBRATION STATUS
------------------
The bracket SHAPE below is the WAS 2018-20 + Pareto table from RATES §5.1.
It is a household-level shape applied to individuals and is a PLACEHOLDER
pending the L1 calibration rebuild.  Only its relative shape is used; the
level is set by `wealth_to_gdp`.
"""

import numpy as np

import rates_data as rd

# (N people, mean wealth £) — RATES §5.1.  Relative shape only.
_BRACKET_ROWS = [
    ('0-10',        6_920_000,        3_474),
    ('10-20',       6_920_000,       23_080),
    ('20-30',       6_920_000,       68_512),
    ('30-40',       6_920_000,      147_026),
    ('40-50',       6_920_000,      261_108),
    ('50-60',       6_920_000,      401_789),
    ('60-70',       6_920_000,      569_543),
    ('70-80',       6_920_000,      782_141),
    ('80-90',       6_920_000,    1_108_535),
    ('90-95',       3_460_000,    1_629_190),
    ('95-99',       2_768_000,    2_858_347),
    ('99-99.9',       622_800,    7_135_016),
    ('99.9-99.99',     62_280,   19_853_605),
    ('99.99-99.999',    6_228,   53_384_707),
    ('99.999+',           692,  139_607_368),
]

INDEX_MODES = ('cpi', 'gdp_pc', 'wealth', 'none')


def bracket_shape():
    """Return (labels, population share, wealth relative to the mean)."""
    labels = [r[0] for r in _BRACKET_ROWS]
    n = np.array([r[1] for r in _BRACKET_ROWS], float)
    v = np.array([r[2] for r in _BRACKET_ROWS], float)
    share = n / n.sum()
    mean = (share * v).sum()
    return labels, share, v / mean


def y_ref_uk(J, year=2019):
    """UK GDP per capita in £m (JST UK GDP is £bn, pop thousands => ratio is £m)."""
    d = rd.panel(J, 'GBR')
    return float(d.loc[year, 'gdp_pc'])


# Aggregate household net wealth, Great Britain, April 2016 - March 2018: £14.6tn
# (ONS Wealth and Assets Survey; private pension wealth £6.1tn = 42% of it).
# WAS covers GB, not the UK, so wealth/GDP computed against UK GDP is ~3% low.
ONS_TOTAL_WEALTH_GBP_BN_2016_18 = 14_600.0
ONS_PENSION_SHARE_2016_18 = 0.42


def uk_wealth_to_gdp(J, year=2017, include_pensions=True):
    """Aggregate UK household net wealth / GDP, ONS WAS total over JST GDP.
    JST UK gdp is in £bn."""
    d = rd.panel(J, 'GBR')
    w = ONS_TOTAL_WEALTH_GBP_BN_2016_18 * (1.0 if include_pensions
                                           else 1.0 - ONS_PENSION_SHARE_2016_18)
    return w / float(d.loc[year, 'gdp'])


def calibrate(wealth_to_gdp, pop_per_adult, wmin_gbp_m, k_per_gbp_m,
              tau_0, tau_m, y_ref_gbp_m):
    """
    Express the distribution and rate function in units of GDP per capita.

    wealth_to_gdp   aggregate household net worth / GDP
    pop_per_adult   population / adult population (~1.27 in the UK)
    wmin_gbp_m, k_per_gbp_m   statutory parameters at the reference date
    y_ref_gbp_m     GDP per capita at the reference date (£m)
    """
    labels, share, rel = bracket_shape()
    m_y = wealth_to_gdp * pop_per_adult
    return {
        'labels': labels, 'share': share, 'rel': rel,
        'V0': rel * m_y, 'mean_wealth_y': m_y,
        'pop_per_adult': pop_per_adult,
        'wealth_to_gdp': wealth_to_gdp,
        'rate': {'tau_0': tau_0, 'tau_m': tau_m,
                 'k': k_per_gbp_m * y_ref_gbp_m,
                 'wmin': wmin_gbp_m / y_ref_gbp_m},
    }


def calibrate_dist(dist, gdp_bn, pop_per_adult, wmin_gbp_m, k_per_gbp_m, tau_0, tau_m,
                   y_ref_gbp_m, wmin_pct=None):
    """
    Calibration from a rates_dist distribution (adult-level cells).  Same interface as
    calibrate().  If wmin_pct is given (e.g. 0.05), W_min is set to the wealth at that
    top fraction of the distribution at launch (the taxpayer percentile) and
    wmin_gbp_m is ignored.

    gdp_bn   GDP in the wealth-data year (£bn), to report wealth/GDP
    y_ref_gbp_m  GDP per capita in the SAME year (£m)
    """
    import rates_dist as dd
    wmin_gbp = dd.wealth_at_top_fraction(dist, wmin_pct) if wmin_pct else wmin_gbp_m
    return {
        'labels': dist['labels'], 'share': dist['share'],
        'rel': dist['mean_gbp_m'] / (dist['total_bn'] * 1e9 / dist['n_adults'] / 1e6),
        'V0': dist['mean_gbp_m'] / y_ref_gbp_m,
        'mean_wealth_y': dist['total_bn'] * 1e3 / dist['n_adults'] * 1e6 / 1e6 / y_ref_gbp_m,
        'pop_per_adult': pop_per_adult,
        'wealth_to_gdp': dist['total_bn'] / gdp_bn,
        'wmin_gbp_m': wmin_gbp,
        'dist': dist['scenario'] + '/' + dist['mode'],
        'rate': {'tau_0': tau_0, 'tau_m': tau_m,
                 'k': k_per_gbp_m * y_ref_gbp_m, 'wmin': wmin_gbp / y_ref_gbp_m},
    }


def build_scenario(J, iso, start, T, basis='real', index_mode='gdp_pc', c=0.035):
    """Engine inputs for one window.  Raises ValueError if data are missing."""
    if index_mode not in INDEX_MODES:
        raise ValueError(f'index_mode must be one of {INDEX_MODES}')
    if basis not in ('real', 'nominal'):
        raise ValueError("basis must be 'real' or 'nominal'")
    d = rd.panel(J, iso)
    yrs = list(range(start, start + T))
    sub = d.reindex(yrs)
    sfx = '_real' if basis == 'real' else ''
    cols = {'r': 'capital_tr' + sfx, 'safe': 'safe_tr' + sfx,
            'risky': 'risky_tr' + sfx, 'gpc': 'gpc' + sfx,
            'infl': 'infl', 'exp_gdp': 'exp_gdp'}
    out = {}
    for k_, col in cols.items():
        a = sub[col].to_numpy(float)
        if np.isnan(a).any():
            raise ValueError(f'{iso} {start}+{T}: missing {col}')
        out[k_] = a
    out['eqg'] = sub['eq_capgain' + sfx].to_numpy(float)   # equity PRICE return (market-cap delta); may be NaN
    r, gpc, infl = out['r'], out['gpc'], out['infl']

    if index_mode == 'cpi':
        x = np.zeros(T) if basis == 'real' else infl
    elif index_mode == 'gdp_pc':
        x = gpc
    elif index_mode == 'wealth':
        x = (1.0 + r) * (1.0 - c) - 1.0
    else:
        x = np.zeros(T)
    out.update({
        'iso': iso, 'start': start, 'T': T, 'basis': basis,
        'index_mode': index_mode, 'c': c, 'years': np.array(yrs),
        'idx': np.cumprod(1.0 + x),
        'yy': np.cumprod(1.0 + gpc),
    })
    return out
