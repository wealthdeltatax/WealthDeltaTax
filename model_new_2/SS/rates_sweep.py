"""
rates_sweep.py — RATES rebuild, L5 sweep and headline summary
==============================================================
Runs the full chain (scenario -> cohort engine -> fund) for every valid
(country, start year, index mode) window in the JST data and summarises the
headline metric:

    10 years after LRR fill, the share of government expenditure that WDT
    relief could cover.

WHAT THE SWEEP IS
-----------------
A REPLAY.  Each window applies one country-history's returns, GDP-per-capita
growth, inflation and expenditure/GDP to TODAY's wealth distribution and rate
function (UK-calibrated wealth/GDP, individual-level shape).  It tests robustness
to macro history.  It is not a reconstruction of what would have happened in
that country in those years and not a forecast for any country.

CONSUMPTION / STATIONARITY
--------------------------
cfg['c_mode'] = 'fixed' (default) uses one c everywhere.  A fixed c lets the tax base drift
against GDP whenever a window's real return less real GDP/head growth differs from the
value c was calibrated for.  'stationary' sets c per window to 1 - (1+g)/(1+r) (geometric
means), so an untaxed holder's wealth/GDP ends the window where it began; the tax itself
still removes units, so family wealth/GDP ends slightly below launch.  The row records
c_used, c_rest and whether the constrained payout had to be clipped (stationary mode only;
in fixed mode an infeasible payout_top raises).

DIAGNOSTICS ADDED TO EVERY ROW
------------------------------
top{q}_share_launch / _share_end   share of family wealth held by the top q at launch / end
top{q}_wgdp_launch / _wgdp_end     the same as wealth / GDP
fund_gdp_fill, fund_gdp_fill_h     the fund's stake / GDP at fill and at fill + horizon
fund_target_gdp_fill_h             the (ms+ml) x A target / GDP at fill + horizon
fund_excess_gdp_fill_h             stake above target: returns beyond upkeep, never paid as relief
fund_income_gdp_h                  the fund's investment income / GDP over the post-fill window

SAMPLE RULES
------------
* A window needs every model column non-null for all T years.  War and
  hyperinflation episodes mostly drop out because JST has no return data there.
* Windows containing years flagged by rates_data.flag_years are KEPT by default
  and marked `flagged`; set cfg['exclude_flagged'] = True to drop them.
* Windows where the fund never fills, or fills too late for the post-fill
  horizon, are CENSORED: reported with their share, never dropped.
* Overlapping windows are strongly autocorrelated.  Counts are not independent
  observations: summaries are given per country and per era, and the headline
  weights countries equally.
"""

import numpy as np
import pandas as pd

import rates_data as rd
import rates_scenario as sc
import rates_dist as dd
import rates_engine as eng
import rates_fund as rf

DEFAULT_CFG = {
    'basis': 'real',
    'index_modes': ('cpi', 'gdp_pc', 'wealth'),
    'c': 0.035,                 # consumption share of net worth (valgen D16); used when c_mode='fixed'
    'c_mode': 'fixed',          # 'fixed' = c above in every window | 'stationary' = per-window c that
                                #   keeps an untaxed holder's wealth/GDP flat: c = 1 - (1+g)/(1+r),
                                #   r, g = that window's geometric-mean real return and real GDP/head growth
    'c_bounds': (0.0, 0.10),    # clip for the stationary c
    'diag_tops': (0.01, 0.001), # top fractions reported in the concentration diagnostics
    'dist': 'advani',           # 'advani' (evidence-based, default) | 'adjusted' | 'survey' | 'legacy'
    'dist_mode': 'central',     # advani: 'central' | 'upper'; adjusted: 'add' | 'reallocate'
    'dist_kw': {},              # overrides for rates_dist.build (s1, s01, rich_list_bn, ...)
    'wmin_pct': None,           # set W_min at this top fraction of adults at launch (e.g. 0.05)
    'wealth_to_gdp': None,      # legacy only: None -> ONS / JST, all wealth incl. pensions
    'pop_per_adult': 1.27,
    'wmin_gbp_m': 0,
    'k_per_gbp_m': 0.005,
    'tau_0': 0.40,
    'tau_m': 0.90,
    'T': 30,                    # needs fill + horizon; results are causal in T
    'exp_ref': 'uk_2019',       # fixed modern expenditure/GDP for the reference coverage
    'tiers': None,              # homogeneous returns; see engine note on tiers
    'heir_rule': 'delta',       # the mechanism as designed (valgen D6)
    'n_phase': 6,
    'G': 30,
    'ms': 3.0,
    'ml': 3.0,
    'a_window': 5,
    'horizon': 10,
    'safe_share': 0.0,
    'exclude_flagged': False,
    'payout_top': None,         # consumption share for the top cells (None = uniform c)
    'payout_top_frac': 0.06,    # which cells: top q of adults (grid edges: 0.10, 0.06, 0.02, 0.01, 0.001)
    'payout_constrained': True, # True: others adjust so the wealth-weighted mean payout stays c (stationarity)
    'exp_paths': None,          # {name: real growth of expenditure per year, or None = tracks GDP}
    'levy': None,               # corporate levy on non-attributable holders: dict(tau, f_inc, mc_gdp) or None
    'start_stride': 1,          # take every k-th start year (speed; 1 = all)
    'countries': None,
}

ERAS = [('pre-1914', 0, 1913), ('1914-45', 1914, 1945),
        ('1946-79', 1946, 1979), ('1980+', 1980, 3000)]


def _era(y):
    for name, lo, hi in ERAS:
        if lo <= y <= hi:
            return name


def make_cfg(**kw):
    cfg = {**DEFAULT_CFG, **kw}
    return cfg


def calibration(J, cfg):
    if cfg['dist'] == 'legacy':
        wy = cfg['wealth_to_gdp'] or sc.uk_wealth_to_gdp(J, 2017, True)
        cal = sc.calibrate(wy, cfg['pop_per_adult'], cfg['wmin_gbp_m'],
                           cfg['k_per_gbp_m'], cfg['tau_0'], cfg['tau_m'],
                           sc.y_ref_uk(J))
    else:
        u17 = rd.panel(J, 'GBR').loc[2017]
        adults = float(u17['pop']) * 1e3 / cfg['pop_per_adult']
        dist = dd.build(cfg['dist'], adults, cfg['dist_mode'], **cfg['dist_kw'])
        cal = sc.calibrate_dist(dist, float(u17['gdp']), cfg['pop_per_adult'],
                                cfg['wmin_gbp_m'], cfg['k_per_gbp_m'], cfg['tau_0'],
                                cfg['tau_m'], float(u17['gdp_pc']), cfg['wmin_pct'])
    ref = cfg['exp_ref']
    cal['exp_ref'] = (float(rd.panel(J, 'GBR').loc[2019, 'exp_gdp'])
                      if ref == 'uk_2019' else float(ref))
    return cal


def run_window(J, iso, start, mode, cfg, cal, flags=None):
    scn = sc.build_scenario(J, iso, start, cfg['T'], basis=cfg['basis'],
                            index_mode=mode, c=cfg['c'])
    c_used = cfg['c']
    if cfg.get('c_mode', 'fixed') == 'stationary':
        # c that makes (1+r)(1-c) = 1+g on the window's geometric means, so an untaxed
        # holder's wealth/GDP is the same at the end of the window as at launch.
        rg = float(np.prod(1.0 + scn['r']) ** (1.0 / cfg['T']) - 1.0)
        gg = float(np.prod(1.0 + scn['gpc']) ** (1.0 / cfg['T']) - 1.0)
        lo_c, hi_c = cfg['c_bounds']
        c_used = float(np.clip(1.0 - (1.0 + gg) / (1.0 + rg), lo_c, hi_c))
        scn = sc.build_scenario(J, iso, start, cfg['T'], basis=cfg['basis'],
                                index_mode=mode, c=c_used)     # idx ('wealth' mode) and c depend on it
    c_cell = None
    c_rest = np.nan
    c_rest_clipped = False
    if cfg['payout_top'] is not None:
        share = cal['share']; wsh = share * cal['V0']; wsh = wsh / wsh.sum()
        top = np.cumsum(share[::-1])[::-1] <= cfg['payout_top_frac'] * (1 + 1e-6)
        Wt = wsh[top].sum()
        c_rest = ((c_used - cfg['payout_top'] * Wt) / (1.0 - Wt)) if cfg['payout_constrained'] else c_used
        if c_rest < 0.0:
            if cfg.get('c_mode', 'fixed') == 'fixed':
                raise ValueError(
                    f"payout_top={cfg['payout_top']} with c={c_used} gives NEGATIVE consumption "
                    f"({c_rest:.4f}) for the other cells: the constraint is infeasible. "
                    f"Lower payout_top or raise c.")
            c_rest, c_rest_clipped = 0.0, True      # stationary mode: per-window c can be small
        c_cell = np.where(top, cfg['payout_top'], c_rest)
    out = eng.run_cohorts(scn, cal, tiers=cfg['tiers'], n_phase=cfg['n_phase'],
                          G=cfg['G'], heir_rule=cfg['heir_rule'], c_cell=c_cell)
    er = eng.effective_rates(out, cal)
    scale = scn['yy'] * cal['pop_per_adult']
    # concentration diagnostics: how much of the tax base the top holds at launch and at window end
    _share = cal['share']
    _cum_top = np.cumsum(_share[::-1])[::-1]
    _w0 = _share * cal['V0']; _w0 = _w0 / _w0.sum()
    _lv = out['lvl']['wealth_b']                    # (T, cells): wealth per adult, engine units
    conc = {}
    for q_ in cfg['diag_tops']:
        m_ = _cum_top <= q_ * (1 + 1e-6)
        k_ = f'top{100*q_:g}'
        conc[f'{k_}_share_launch'] = float(_w0[m_].sum())
        conc[f'{k_}_share_end'] = float(_lv[-1, m_].sum() / _lv[-1].sum())
        conc[f'{k_}_wgdp_launch'] = float(_w0[m_].sum() * cal['wealth_to_gdp'])
        conc[f'{k_}_wgdp_end'] = float(_lv[-1, m_].sum() / scale[-1])
    levy_gdp = np.zeros(cfg['T'])
    if cfg['levy']:
        lv = cfg['levy']
        # delta of listed market cap = price return; losses: no levy and no refund (CORP 5.5);
        # base is the non-attributable ownership share (foreign etc.), outside the engine's adults.
        levy_gdp = lv['tau'] * lv['f_inc'] * lv['mc_gdp'] * np.maximum(0.0, scn['eqg']) / (1.0 + scn['gpc'])
    net_l = (out['net'] + levy_gdp) * scale
    E_l = scn['exp_gdp'] * scale
    f = rf.run_fund(net_l, E_l, scn['r'], refund=out['refund'] * scale,
                    safe=scn['safe'], ms=cfg['ms'], ml=cfg['ml'],
                    a_window=cfg['a_window'], safe_share=cfg['safe_share'],
                    horizon=cfg['horizon'])
    fy = f['fill_year']
    extra = {}
    if cfg['exp_paths']:
        R, Tn = f['R'], cfg['T']
        yrs_ = np.arange(1, Tn + 1)
        for name, e in cfg['exp_paths'].items():
            E = (cal['exp_ref'] * scale if e is None
                 else cal['exp_ref'] * cal['pop_per_adult'] * (1.0 + e) ** yrs_)
            if fy and fy + cfg['horizon'] <= Tn:
                extra[f'cov_fill10_{name}'] = float(R[fy:fy + 10].sum() / E[fy:fy + 10].sum())
            for a_, b_ in ((20, 30), (40, 50)):
                if Tn >= b_:
                    extra[f'cov_y{a_+1}_{b_}_{name}'] = float(R[a_:b_].sum() / E[a_:b_].sum())
            # breakeven = first year after fill in which the TRAILING 5-YEAR relief covers >= 100% of
            # trailing 5-year expenditure (a single boom year does not count)
            cR, cE = np.cumsum(np.insert(R, 0, 0.0)), np.cumsum(np.insert(E, 0, 0.0))
            lo = np.maximum(0, yrs_ - 5)
            ratio5 = (cR[yrs_] - cR[lo]) / (cE[yrs_] - cE[lo])
            hit = np.where((yrs_ > (fy or 10**9)) & (yrs_ >= 5) & (ratio5 >= 1.0))[0] if fy else []
            extra[f'be_{name}'] = int(hit[0] + 1) if len(hit) else np.nan
            extra[f'eshare30_{name}'] = float(E[min(29, Tn - 1)] / scale[min(29, Tn - 1)])
            if Tn >= 50:
                extra[f'eshare50_{name}'] = float(E[49] / scale[49])
    cov_ref = relief_gdp = np.nan
    fund = {'fund_gdp_fill': np.nan, 'fund_gdp_fill_h': np.nan, 'fund_target_gdp_fill_h': np.nan,
            'fund_excess_gdp_fill_h': np.nan, 'fund_income_gdp_h': np.nan}
    if not f['censored']:
        sl = slice(fy, fy + cfg['horizon'])
        relief_gdp = float(f['R'][sl].sum() / scale[sl].sum())
        cov_ref = relief_gdp / cal['exp_ref']
        # the fund itself, as a share of GDP.  S_path[i] is the stake at the end of year i+1.
        S, A_ = f['S'], f['A']
        ih = fy + cfg['horizon']
        ss = cfg['safe_share']
        rr = (1.0 - ss) * scn['r'] + ss * scn['safe'] if ss > 0.0 else scn['r']
        S_prev = np.concatenate([[0.0], S[:-1]])
        tgt = (cfg['ms'] + cfg['ml']) * A_[ih - 1]
        fund = {
            'fund_gdp_fill': float(S[fy - 1] / scale[fy - 1]),
            'fund_gdp_fill_h': float(S[ih - 1] / scale[ih - 1]),
            'fund_target_gdp_fill_h': float(tgt / scale[ih - 1]),
            # stake above the (SRR+LRR) target: returns beyond what upkeep needs, not paid out as relief
            'fund_excess_gdp_fill_h': float((S[ih - 1] - tgt) / scale[ih - 1]),
            # the fund's own investment income over the post-fill window, share of GDP
            'fund_income_gdp_h': float((S_prev[sl] * rr[sl]).sum() / scale[sl].sum()),
        }
    flagged = False
    if flags is not None:
        yrs = set(range(start, start + cfg['T']))
        flagged = bool(flags.loc[flags.index.isin(yrs)].any())
    return {
        'iso': iso, 'start': start, 'mode': mode, 'era': _era(start),
        'fill_year': fy, 'srr_fill_year': f['srr_fill_year'],
        'censored': f['censored'],
        'coverage': f['coverage'], 'cov_ref': cov_ref, 'relief_gdp': relief_gdp,
        'cov_receipts': f['cov_receipts'],
        'fail': f['fail_in_window'], 'unmet_year': f['unmet_year'],
        'ring_year': f['ring_year'], 'insolvent_year': f['insolvent_year'],
        'min_buffer': f['min_buffer'], 'srr_need_mult': f.get('srr_need_mult'),
        'net_gdp_mean': float(out['net'].mean()), 'levy_gdp_mean': float(levy_gdp.mean()),
        'net_gdp_at_fill': float(out['net'][fy - 1]) if fy else np.nan,
        'paying_at_fill': float(out['share_paying'][fy - 1]) if fy else np.nan,
        'wealth_gdp_end': float(out['wealth_gdp'][-1]), 'wealth_gdp_mean': float(out['wealth_gdp'].mean()),
        'r_mean': float(scn['r'].mean()),
        'exp_gdp_mean': float(scn['exp_gdp'].mean()),
        'min_r': float(scn['r'].min()), 'flagged': flagged,
        'c_used': c_used, 'c_rest': c_rest, 'c_rest_clipped': c_rest_clipped,
        **conc, **fund,
        **{f'er_{k}': v for k, v in er.items()},
        **extra,
    }


def sweep(J, cfg=None, verbose=True):
    cfg = make_cfg() if cfg is None else cfg
    cal = calibration(J, cfg)
    isos = cfg['countries'] or rd.countries(J)
    rows, n_win = [], {}
    for iso in isos:
        d = rd.panel(J, iso)
        fl = rd.flag_years(d)['any']
        cols = rd.MODEL_COLS + (['eq_capgain_real'] if cfg['levy'] else [])
        starts = rd.valid_windows(d, cols, cfg['T'],
                                  exclude=fl if cfg['exclude_flagged'] else None)
        n_win[iso] = len(starts)
        for s in starts[::cfg['start_stride']]:
            for mode in cfg['index_modes']:
                rows.append(run_window(J, iso, s, mode, cfg, cal, flags=fl))
    df = pd.DataFrame(rows)
    if verbose:
        print(f"{len(df)} runs over {sum(n_win.values())} windows in "
              f"{sum(1 for v in n_win.values() if v)} countries "
              f"(T={cfg['T']}, wealth/GDP {cal['wealth_to_gdp']:.2f})")
    return df


# ─────────────────────────────────────────────────────────────
# SUMMARIES
# ─────────────────────────────────────────────────────────────

def _q(x, q):
    x = x.dropna()
    return float(np.quantile(x, q)) if len(x) else np.nan


def headline(df, by='mode', col='coverage'):
    """Per group: windows, censored share, coverage quantiles (windows pooled),
    country-equal-weight median, and the share of windows with a failure."""
    rows = []
    for key, g in df.groupby(by):
        ok = g[~g['censored']]
        cm = ok.groupby('iso')[col].median()
        rows.append({
            by: key, 'windows': len(g), 'countries': g['iso'].nunique(),
            'censored %': 100 * g['censored'].mean(),
            'p10 %': 100 * _q(ok[col], .10),
            'median %': 100 * _q(ok[col], .50),
            'p90 %': 100 * _q(ok[col], .90),
            'country-median of medians %': 100 * float(cm.median()) if len(cm) else np.nan,
            'fail %': 100 * float(ok['fail'].astype(float).mean()) if len(ok) else np.nan,
        })
    return pd.DataFrame(rows)


def by_country(df, mode, col='coverage'):
    g = df[(df['mode'] == mode)]
    rows = []
    for iso, x in g.groupby('iso'):
        ok = x[~x['censored']]
        rows.append({'iso': iso, 'windows': len(x), 'uncensored': len(ok),
                     'median %': 100 * _q(ok[col], .5),
                     'p10 %': 100 * _q(ok[col], .1),
                     'p90 %': 100 * _q(ok[col], .9),
                     'fail %': 100 * float(ok['fail'].astype(float).mean()) if len(ok) else np.nan,
                     'exp/GDP %': 100 * float(x['exp_gdp_mean'].mean())})
    return pd.DataFrame(rows).set_index('iso')