"""
apply_regime_patch.py — RATES representativeness patch
=======================================================
Adds to the RATES pipeline (all behaviour-preserving for existing outputs, except the one
caption fix noted below):

  1. window regime columns (real GDP/head growth, mean CPI inflation) and per-slice results
     (all / GBR / JPN / low growth / low inflation / today-like / each era), per levy case
  2. a block bootstrap of the median (country-period blocks and all-country period blocks)
     with design effect and effective number of windows
  3. today's expenditure and revenue ratios as inputs ([rates.representativeness]);
     reference-expenditure numbers are kept, today's are shown beside them
  4. a per-scenario levy calibration base (levy_cal_base) and seven levy scenarios
  5. Tables / Figures 23, 24, 25 (representativeness, bootstrap, levy sensitivity)
  6. caption fix: _levy_note no longer hard-codes "nominal base"

Run from the Model/ folder (or pass --model PATH):

    python apply_regime_patch.py --dry     # check every anchor, change nothing
    python apply_regime_patch.py           # back up originals (*.bak_regime) and patch

Then, in this order:

    python rates_core.py                   # FULL run: new columns need every scenario re-run
    python 8_2_RATES_tables.py
    python 8_3_RATES_charts.py
    python rates_test.py                   # checks the table / figure registries agree

The script refuses to write anything unless every anchor matches exactly once.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

# ═════════════════════════════════════════════════════════════════════════════
# NEW CODE
# ═════════════════════════════════════════════════════════════════════════════

# ── wdt_fmt.py ───────────────────────────────────────────────────────────────

FMT_ADD = r'''

# ─────────────────────────────────────────────────────────────────────────────
# WINDOW-SLICE LABELS (RATES T23 / F23)
# ─────────────────────────────────────────────────────────────────────────────

def slice_label(key: str, rr: dict) -> str:
    """
    Display text for a window-slice key written by rates_core.slice_blocks.
    rr is p['rates']['representativeness'] (thresholds are quoted from it, never typed here).
    """
    if key == 'all':
        return 'All windows (pooled)'
    if key.startswith('country:'):
        return f'{key[8:]} only'
    if key.startswith('era:'):
        return f'Start year {key[4:]}'
    return {
        'low_growth': f"Low growth (real GDP/head under {fmt_pct(rr['low_growth_max'], 1)} a year)",
        'not_low_growth': f"Higher growth ({fmt_pct(rr['low_growth_max'], 1)} a year or more)",
        'low_inflation': f"Low inflation (CPI under {fmt_pct(rr['low_infl_max'], 1)} a year)",
        'today_like': 'Low growth and low inflation (today-like)',
    }.get(key, key)
'''

# ── rates_core.py ────────────────────────────────────────────────────────────

CORE_DOC = '''
REPRESENTATIVENESS (T23-T25 / F23-F25: is the history the UK of today?)
  Every window carries gpc_real_gm (geometric-mean REAL GDP/head growth) and infl_mean (mean CPI inflation). headline.<mode>.slices
  re-states the headline numbers for slices of the windows: all, each [rates.representativeness].focus_countries, low_growth /
  not_low_growth, low_inflation, today_like (low growth AND low inflation) and each era; each slice is held for all three levy cases.
  headline.<mode>.levy_variants.<case>.bootstrap (scenarios in [rates.representativeness].bootstrap_scenarios only) is a bootstrap of the
  median: windows as independent (iid), country-period blocks and all-country period blocks of block_years. deff = var(block) / var(iid);
  n_eff = windows / max(deff, 1). Overlapping 30-year windows are not independent, so n_eff is the honest sample size.
  levy_cal_base ('' | nominal | real) sets, per scenario, the base the levy entry rate is solved on.
'''

CORE_FUNCS = r'''def _slice_masks(df, rr, eras):
    """
    Boolean masks of the window slices T23 / F23 compare (stable keys; wdt_fmt.slice_label turns them into text):
      all | country:<ISO> for each focus country | low_growth, not_low_growth (geometric-mean REAL GDP/head growth below / at or above
      low_growth_max) | low_inflation (mean CPI inflation below low_infl_max) | today_like (low growth AND low inflation)
      | era:<name> for each era of [rates.eras].
    """
    low_g = df['gpc_real_gm'] < rr['low_growth_max']
    low_i = df['infl_mean'] < rr['low_infl_max']
    masks = {'all': pd.Series(True, index=df.index)}
    for iso in rr['focus_countries']:
        masks[f'country:{iso}'] = df['iso'] == iso
    masks['low_growth'] = low_g
    masks['not_low_growth'] = ~low_g
    masks['low_inflation'] = low_i
    masks['today_like'] = low_g & low_i
    for name, _, _ in eras:
        masks[f'era:{name}'] = df['era'] == name
    return masks


def _slice_case_block(h, qs, band):
    """Trimmed headline numbers of one slice under one levy case (h is a _variant_view)."""
    ov = _group_block(h, qs, band)
    out = {k: ov[k] for k in ('windows', 'uncensored', 'censored_share', 'fail_share', 'relief_gdp', 'cov_ref',
                              'net_gdp_mean', 'drift')}
    out['gpc_real_gm'] = dist_stats(h['gpc_real_gm'], qs)
    out['infl_mean'] = dist_stats(h['infl_mean'], qs)
    return out


def slice_blocks(g, p, qs, band):
    """{slice key: {levy case: block}} for the windows g of one index mode; None for a slice with no windows."""
    rp = p['rates']
    out = {}
    for key, m in _slice_masks(g, rp['representativeness'], rp['eras']).items():
        x = g[m]
        out[key] = ({c: _slice_case_block(_variant_view(x, c), qs, band) for c in LEVY_CASES} if len(x) else None)
    return out


def block_bootstrap(h, p):
    """
    Bootstrap of the MEDIAN of relief_gdp, cov_ref (uncensored windows) and net_gdp_mean, drift (all windows) for one levy case
    (h is a _variant_view). Three resampling schemes:
      iid             windows drawn one by one (what a naive count of windows implies)
      country_period  blocks = (country, start year // block_years): keeps a country's own autocorrelation
      period          blocks = start year // block_years across ALL countries: also keeps global shocks (1970s, 2008)
    Per metric: n, median and, per scheme, the [lo, hi] interval from [rates.representativeness].boot_ci, se, number of blocks,
    deff = var(block draws) / var(iid draws), n_eff = n / max(deff, 1).
    """
    rr = p['rates']['representativeness']
    rng = np.random.default_rng(rr['boot_seed'])
    n_boot, B = rr['n_boot'], rr['block_years']
    lo_q, hi_q = rr['boot_ci']
    ok = h[~h['censored']]
    out = {'block_years': B, 'n_boot': n_boot, 'ci': [lo_q, hi_q]}
    for metric, d in (('relief_gdp', ok), ('cov_ref', ok), ('net_gdp_mean', h), ('drift', h)):
        d = d[d[metric].notna()]
        n = len(d)
        if n < 2:
            out[metric] = None
            continue
        vals = d[metric].to_numpy(float)
        period = (d['start'] // B).astype(int)
        schemes = {'country_period': (d['iso'] + '|' + period.astype(str)).to_numpy(), 'period': period.to_numpy()}
        iid = np.median(rng.choice(vals, size=(n_boot, n)), axis=1)
        res = {'n': int(n), 'median': float(np.median(vals)),
               'iid': {'lo': float(np.quantile(iid, lo_q)), 'hi': float(np.quantile(iid, hi_q)), 'se': float(iid.std())}}
        for scheme, lab in schemes.items():
            blocks = [vals[lab == u] for u in np.unique(lab)]
            nb = len(blocks)
            draws = np.empty(n_boot)
            for i in range(n_boot):
                pick = rng.integers(0, nb, nb)
                draws[i] = np.median(np.concatenate([blocks[j] for j in pick]))
            deff = float(draws.var() / iid.var()) if nb > 1 and iid.var() > 0 else None
            res[scheme] = {'blocks': int(nb), 'lo': float(np.quantile(draws, lo_q)), 'hi': float(np.quantile(draws, hi_q)),
                           'se': float(draws.std()), 'deff': deff,
                           'n_eff': (float(n / max(deff, 1.0)) if deff is not None else None)}
        out[metric] = res
    return out


'''

HEADLINE_HOOK = """out[mode]['levy_variants'] = {c: _variant_block(_variant_view(g, c), qs, band) for c in LEVY_CASES}
        out[mode]['slices'] = slice_blocks(g, p, qs, band)
        if boot:
            for c in LEVY_CASES:
                out[mode]['levy_variants'][c]['bootstrap'] = block_bootstrap(_variant_view(g, c), p)"""

VALIDATE_HOOK = """for mode, h in sc['headline'].items():
            sl = h['slices']['all']
            assert sl is not None and sl['nominal']['windows'] == h['overall']['windows'], \\
                f'{name}/{mode}: slice "all" windows differ'
        if 'windows' in sc:"""

# ── 8_2_RATES_tables.py ──────────────────────────────────────────────────────

LEVY_NOTE = r'''def _levy_note(sc):
    """Caption sentence on how the levy was calibrated, from the scenario's own JSON block (base and rates as run)."""
    lc = sc['calibration'].get('levy_cal')
    if not lc:
        return 'The CORP levy is not calibrated in this scenario.'
    base = lc.get('base', 'nominal')
    other = 'real' if base == 'nominal' else 'nominal'
    got = {'nominal': lc['achieved_nominal_gdp'], 'real': lc['achieved_real_gdp']}
    s = (f"The CORP levy is calibrated so its median receipts on the {base} base equal {lc['target'].lower()} "
         f"({fmt_pct1(lc['target_gdp'])} of GDP): tau0 = {fmt_pct1(lc['tau0'])}, tau = {fmt_pct0(lc['tau'])}; the same rates on a {other} base "
         f"raise a median {fmt_pct1(got[other])}.")
    if lc['infeasible']:
        s += (f" The calibration is INFEASIBLE: the unattributed tier alone raises {fmt_pct1(lc['unattributed_tier_gdp'])}, above the target, "
              f"so tau0 is floored at 0 and the levy overshoots.")
    return s'''

TABLES_NEW = r'''# ── tables 23-25: is the history the UK of today? ────────────────────────────

_CASE_SHORT = {'none': 'No levy', 'real': 'Real-basis levy', 'nominal': 'Nominal-basis levy'}


def t23_representativeness(data, p):
    sc, mode, _, _ = _ctx(data, p)
    rr = p['rates']['representativeness']
    case = p['rates']['replacement']['levy_case']
    exp_ref, exp_t, rev_t = sc['calibration']['exp_ref'], rr['exp_today'], rr['rev_today']
    sl = wc.scenario_headline(sc, mode)[0].get('slices')
    if not sl:
        raise SystemExit("rates_data.json has no window slices; re-run: python rates_core.py")

    def cov(b, den):
        v = b['relief_gdp']['p50']
        return '—' if v is None else fmt_pct1(v / den)

    rows = []
    for key, blk in sl.items():
        if blk is None:
            continue
        c = blk[case]
        nm = c['net_gdp_mean']['p50']
        rows.append([f'**{slice_label(key, rr)}**', c['windows'], c['uncensored'],
                     fmt_pct1(c['gpc_real_gm']['p50']), fmt_pct1(c['infl_mean']['p50']), _band(c['relief_gdp']),
                     cov(c, exp_ref), cov(c, exp_t), cov(blk['real'], exp_t), cov(blk['none'], exp_t),
                     fmt_f(c['drift']['p50'], '.2f'), '—' if not nm or nm <= 0 else fmt_f(rev_t / nm, '.2f')])
    d = MdDoc()
    d.table(['Window slice', 'Windows', 'Uncensored', 'Median real GDP/head growth', 'Median CPI inflation',
             'Relief / GDP (p10 / median / p90)', 'Spending covered, reference expenditure',
             "Spending covered, today's expenditure", "Same, real-basis levy", "Same, no levy", 'Drift (median)',
             "Base multiple needed, today's revenue"], rows, col_fmt=[LEFT] + [RIGHT] * 11)
    d.caption(f"Table 23: Is the history the UK of today? The same scenario over slices of its windows. Regime columns are medians "
              f"over the slice. Low growth = geometric-mean real GDP/head growth under {fmt_pct1(rr['low_growth_max'])} a year; low "
              f"inflation = mean CPI inflation under {fmt_pct1(rr['low_infl_max'])} (both judgment thresholds in "
              f"[rates.representativeness]). Today-like = both. Relief and the first two coverage columns use {_CASE_TXT[case]}; the "
              f"last two coverage columns re-state the slice with a real-basis levy and with none. Spending covered is relief over "
              f"expenditure: the reference column divides by the fixed {fmt_pct1(exp_ref)} of GDP (JST UK, {p['rates']['exp_ref_year']}), "
              f"the today's-expenditure columns by {fmt_pct1(exp_t)} (placeholder, [rates.representativeness].exp_today). Base multiple "
              f"needed = {fmt_pct1(rev_t)} of GDP revenue (placeholder, rev_today) over the slice's median net receipts. Medians over "
              f"windows in which the fund fills, except drift and receipts (all windows). Windows overlap and are not independent: see "
              f"Table 24 before reading a small slice as a finding. {_desc(sc, mode)}. {_levy_note(sc)}")
    return d


def t24_bootstrap(data, p):
    fg = p['rates']['figures']
    mode = fg['mode']
    rr = p['rates']['representativeness']
    rows, ci, B = [], rr['boot_ci'], rr['block_years']
    for name in rr['bootstrap_scenarios']:
        sc = _scen(data, name)
        for case in ('none', 'real', 'nominal'):
            bs = wc.levy_headline(sc, mode, case).get('bootstrap')
            m = bs.get('cov_ref') if bs else None
            if not m:
                raise SystemExit(f"scenario '{name}' has no bootstrap in rates_data.json; re-run: python rates_core.py --scenario {name}")

            def rng(s):
                return f"{fmt_pct1(s['lo'])} to {fmt_pct1(s['hi'])}"
            cp, pe = m['country_period'], m['period']
            rows.append([f"**{sc['label']}**", _CASE_SHORT[case], m['n'], fmt_pct1(m['median']), rng(m['iid']),
                         f"{rng(cp)} ({cp['blocks']})", f"{rng(pe)} ({pe['blocks']})",
                         fmt_f(cp['deff'], '.1f'), fmt_f(pe['deff'], '.1f'), fmt_f(pe['n_eff'], '.0f')])
    d = MdDoc()
    d.table(['Scenario', 'Levy', 'Windows (uncensored)', 'Median spending covered', 'Interval, windows as independent',
             'Interval, country-period blocks (blocks)', 'Interval, period blocks (blocks)', 'Design effect, country-period',
             'Design effect, period', 'Effective windows, period blocks'],
            rows, col_fmt=[LEFT, LEFT] + [RIGHT] * 8)
    d.caption(f"Table 24: How much history is there? Bootstrap of the median spending covered (relief over the reference expenditure), "
              f"{rr['n_boot']} resamples, {fmt_pct0(ci[0])} to {fmt_pct0(ci[1])} interval. Windows as independent treats each of the "
              f"overlapping {p['rates']['defaults']['T']}-year windows as a separate observation. Country-period blocks resample "
              f"(country, start year // {B}) together; period blocks resample every country's windows for a {B}-year span of start years "
              f"together, which also keeps shocks the whole panel shares. Design effect = variance of the block bootstrap over the "
              f"variance of the independent one; effective windows = windows / max(design effect, 1). The intervals describe sampling "
              f"error of a history that is assumed to be drawn from a stationary process, not the regime question of Table 23, and not "
              f"the uncertainty of any input. Medians are over windows in which the fund fills.")
    return d


def t25_levy_sensitivity(data, p):
    fg = p['rates']['figures']
    mode = fg['mode']
    rows, ref = [], _scen(data, fg['scenario'])
    for name in [fg['scenario']] + list(fg['levy']):
        sc = _scen(data, name)
        c = sc['cfg']
        lv = c['levy']
        lc = sc['calibration'].get('levy_cal')
        how = ('statutory (not calibrated)' if not c['levy_calibrate'] or not lc
               else f"solved on the {lc['base']} base" + (' (INFEASIBLE)' if lc['infeasible'] else ''))
        lev = {k: wc.levy_headline(sc, mode, k)['overall'] for k in ('none', 'real', 'nominal')}
        cov = {k: _x(v['medians'], 'cov_ref', fmt_pct1) for k, v in lev.items()}
        m_cov = {k: v['medians'].get('cov_ref') for k, v in lev.items()}
        adds = '—' if m_cov['nominal'] is None or m_cov['none'] is None else f"{(m_cov['nominal'] - m_cov['none']) * 100:+.1f} pp"
        rows.append([f"**{sc['label']}**", how, fmt_pct1(lv['f_inc']), fmt_pct1(lv['f_attr']), fmt_pct1(lv['tau0']), fmt_pct0(lv['tau']),
                     _x(lev['nominal']['medians_all'], 'levy_gdp_mean', fmt_pct), _x(lev['real']['medians_all'], 'levy_gdp_mean', fmt_pct),
                     cov['none'], cov['real'], cov['nominal'], adds])
    d = MdDoc()
    d.table(['Scenario', 'Levy entry rate', 'f_inc (unattributed)', 'f_attr (attributed non-native)', 'tau0', 'tau',
             'Median levy / GDP, nominal base', 'Median levy / GDP, real base', 'Spending covered, no levy',
             'Spending covered, real-basis levy', 'Spending covered, nominal-basis levy', 'Levy adds (nominal)'],
            rows, col_fmt=[LEFT, LEFT] + [RIGHT] * 10)
    d.caption(f"Table 25: How much of the headline rests on the corporate levy. The first row is the main scenario as run. Calibrated rows "
              f"solve tau0 so the levy's median receipts equal {ref['calibration']['levy_cal']['target'].lower() if ref['calibration'].get('levy_cal') else 'the retired tax'}; "
              f"changing f_inc there only moves the split between the two tiers, not the total, so the statutory rows (tau0 as in "
              f"[rates.defaults], f_inc varied, f_attr = overseas ownership less f_inc) are the ones that show what the levy raises on its "
              f"own terms. Two bases: the calibration base decides what the real-basis variant loses (calibrating on the real base makes "
              f"the real row hit the target and the nominal row overshoot, and the reverse). Medians over all windows for levy / GDP, over "
              f"windows in which the fund fills for spending covered. {_levy_note(ref)}")
    return d


'''

TABLES_REG = """(22, 'net_position', t22_net_position),
    (23, 'representativeness', t23_representativeness),
    (24, 'bootstrap', t24_bootstrap),
    (25, 'levy_sensitivity', t25_levy_sensitivity)"""

# ── 8_3_RATES_charts.py ──────────────────────────────────────────────────────

CHARTS_NEW = r'''# ── figures 23-25: is the history the UK of today? ───────────────────────────

def f23_representativeness(data, p):
    """Spending covered by slice of the history (left: today's expenditure filled, reference hollow) and wealth/GDP drift (right)."""
    apply_style()
    sc, mode, h = _ctx(data, p)
    rr = p['rates']['representativeness']
    case = p['rates']['replacement']['levy_case']
    exp_ref, exp_t = sc['calibration']['exp_ref'], rr['exp_today']
    sl = {k: b for k, b in h['slices'].items() if b}
    keys = list(sl)
    y = np.arange(len(keys))[::-1]
    q = {k: sl[k][case]['relief_gdp'] for k in keys}
    lo, md, hi = (np.array([_nan(q[k][s]) / exp_t for k in keys]) for s in ('p10', 'p50', 'p90'))
    ref = np.array([_nan(q[k]['p50']) / exp_ref for k in keys])
    fig, (a1, a2) = _plt().subplots(1, 2, figsize=FIG_PAIR_T, sharey=True)
    a1.errorbar(md, y, xerr=[md - lo, hi - md], fmt='o', ms=5, color=C_SSM, ecolor=C_SSM, elinewidth=1,
                label=f"Today's expenditure ({exp_t:.0%} of GDP): median, bars p10-p90")
    a1.scatter(ref, y, facecolors='none', edgecolors=C_TCM, zorder=3, label=f'Reference expenditure ({exp_ref:.0%} of GDP): median')
    a1.set_yticks(y, [_wrap(slice_label(k, rr), 30) for k in keys], fontsize=7)
    a1.set_xlabel('Relief / expenditure')
    a1.set_title(f'Spending covered by slice of history, {_CASE_TXT[case]}')
    a1.legend(loc='lower right', fontsize=7)
    _pct(a1, 'x', 0)
    lo_d, hi_d = p['rates']['run']['drift_band']
    a2.barh(y, [_nan(sl[k][case]['drift']['p50']) for k in keys], color=C_LRR, height=0.6)
    a2.axvspan(lo_d, hi_d, color=C_LRR, alpha=0.12, label='Stable base')
    a2.axvline(1.0, color=C_ANNOTATION, lw=0.8)
    a2.set_xlabel('Wealth/GDP at window end ÷ launch (median)')
    a2.set_title('Tax-base drift by slice')
    a2.legend(fontsize=7)
    fig.suptitle(_title(sc, mode, 'Is the history the UK of today?'))
    return save_fig(fig, _path(23, 'representativeness'))


def f24_bootstrap(data, p):
    """Median spending covered with three intervals per headline scenario: windows as independent, country-period blocks, period blocks."""
    apply_style()
    fg = p['rates']['figures']
    mode = fg['mode']
    rr = p['rates']['representativeness']
    case = p['rates']['replacement']['levy_case']
    scs = [_scen(data, n) for n in rr['bootstrap_scenarios']]
    y = np.arange(len(scs))[::-1]
    off = {'iid': 0.22, 'country_period': 0.0, 'period': -0.22}
    col = {'iid': C_ANNOTATION, 'country_period': C_SSM, 'period': C_TCM}
    lab = {'iid': 'Windows as independent', 'country_period': 'Country-period blocks', 'period': 'Period blocks (all countries)'}
    fig, axs = _plt().subplots(1, 2, figsize=FIG_PAIR, sharey=True)
    for ax, c in zip(axs, (case, 'none')):
        for j, s in enumerate(scs):
            bs = wc.levy_headline(s, mode, c).get('bootstrap')
            m = bs.get('cov_ref') if bs else None
            if not m:
                continue
            for sch in off:
                ax.hlines(y[j] + off[sch], m[sch]['lo'], m[sch]['hi'], color=col[sch], lw=3, label=lab[sch] if j == 0 else None)
            ax.scatter(m['median'], y[j], color=C_DARK, zorder=3, label='Median' if j == 0 else None)
        ax.set_title(_CASE_TXT[c].capitalize())
        ax.set_xlabel('Relief / reference expenditure')
        _pct(ax, 'x', 0)
    axs[0].set_yticks(y, [_wrap(s['label'], 26) for s in scs], fontsize=7)
    axs[0].legend(fontsize=7, loc='lower right')
    fig.suptitle(f'Sampling uncertainty of the median, index {mode}: overlapping windows carry less information than their count')
    return save_fig(fig, _path(24, 'bootstrap'))


def f25_levy_sensitivity(data, p):
    """Spending covered with no levy, a real-basis levy and a nominal-basis levy across the levy calibration and f_inc scenarios."""
    apply_style()
    fg = p['rates']['figures']
    mode = fg['mode']
    scs = [_scen(data, n) for n in [fg['scenario']] + list(fg['levy'])]
    cases = [('none', 'No levy', C_ANNOTATION), ('real', 'Real-basis levy', C_LRR), ('nominal', 'Nominal-basis levy', C_SSM)]
    x = np.arange(len(scs))
    w = 0.27
    fig, ax = _plt().subplots(figsize=FIG_WIDE)
    for k, (case, lab, col) in enumerate(cases):
        ds = [wc.levy_headline(s, mode, case)['overall']['cov_ref'] for s in scs]
        med = np.array([_nan(d['p50']) for d in ds])
        lo = np.array([_nan(d['p10']) for d in ds])
        hi = np.array([_nan(d['p90']) for d in ds])
        ax.bar(x + (k - 1) * w, med, w, color=col, label=lab, yerr=[med - lo, hi - med], ecolor=C_DARK, capsize=2, error_kw={'lw': 0.8})
    ax.set_xticks(x, [_wrap(s['label'], 20) for s in scs], fontsize=7)
    ax.set_ylabel('Relief / reference expenditure (median, bars p10-p90)')
    ax.set_title(f'What the levy contributes under each calibration, index {mode}')
    ax.legend(loc='upper left')
    _pct(ax, 'y', 0)
    return save_fig(fig, _path(25, 'levy_sensitivity'))


'''

CHARTS_REG = """(22, 'net_position', f22_net_position),
    (23, 'representativeness', f23_representativeness),
    (24, 'bootstrap', f24_bootstrap),
    (25, 'levy_sensitivity', f25_levy_sensitivity)"""

# ── WDT_Params.toml ──────────────────────────────────────────────────────────

TOML_NEW_SCEN = r'''

# ═════════════════════════════════════════════════════════════════════════════
# Representativeness of the history (T23-T25 / F23-F25)
# ═════════════════════════════════════════════════════════════════════════════
# Is the replayed history the UK of today? Three tools: slices of the windows by regime (T23), a block bootstrap that says how many
# independent windows there really are (T24), and the levy's dependence on its calibration base and on f_inc (T25).
#   low_growth_max    geometric-mean REAL GDP/head growth a year below which a window is "low growth". JUDGMENT: the UK has run at roughly
#                     0.5% since 2008, against about 2% for the post-war windows. VERIFY against ONS.
#   low_infl_max      mean CPI inflation a year below which a window is "low inflation" (matters for the nominal levy base). JUDGMENT.
#   focus_countries   ISO codes shown as their own slice beside the pooled panel (the UK itself, and the closest stagnation analogue)
#   exp_today         total managed expenditure / GDP today, shown beside the fixed JST 2019 reference. PLACEHOLDER: JUR gives TME of about
#                     £1,157b (2022-23) against GDP of about £2.65tn, i.e. about 44%. VERIFY (OBR) and choose the year.
#   rev_today         public sector current receipts / GDP today, for the closure test (base multiple). PLACEHOLDER. VERIFY (OBR).
#   n_boot            bootstrap resamples per metric and scheme
#   boot_seed         RNG seed
#   block_years       block length for the bootstrap, in start years. 30 = the window length: blocks of that size are close to non-overlapping
#   boot_ci           lower and upper quantile of the bootstrap interval
#   bootstrap_scenarios  scenarios that carry the bootstrap in the JSON (each adds a few seconds)
[rates.representativeness]
low_growth_max      = 0.01
low_infl_max        = 0.04
focus_countries     = ["GBR", "JPN"]
exp_today           = 0.44
rev_today           = 0.37
n_boot              = 500
boot_seed           = 20261008
block_years         = 30
boot_ci             = [0.05, 0.95]
bootstrap_scenarios = ["stock_ladder", "gain_ladder", "gain_ladder_cohort_upper", "gain_ladder_cohort_upper_c1"]

# ── Levy sensitivity (T25 / F25) on the main scenario's schedule ──────────────────────────────────────────────
# Calibrated: tau0 is solved so the levy's median receipts equal the retired corporation tax; only the BASE it is solved on differs.
# Statutory: levy_calibrate = false, so tau0 stays at its input and what the levy raises is an OUTPUT. f_inc is varied and
# f_attr = 0.588 - f_inc (overseas beneficial ownership of UK-listed equity, ONS), so the total share charged stays fixed.
[rates.scenarios.gl_levy_cal_nominal]
label = "Gain ladder, levy calibrated on the nominal base"
wmin_house_ratio = 1.0
schedule = "gain_ladder"
levy_cal_base = "nominal"
dist_kw = { body_split = 5, body_split_from = 0.5 }

[rates.scenarios.gl_levy_cal_real]
label = "Gain ladder, levy calibrated on the real base"
wmin_house_ratio = 1.0
schedule = "gain_ladder"
levy_cal_base = "real"
dist_kw = { body_split = 5, body_split_from = 0.5 }

[rates.scenarios.gl_levy_stat_f002]
label = "Gain ladder, statutory levy, f_inc 2%"
wmin_house_ratio = 1.0
schedule = "gain_ladder"
levy_calibrate = false
levy = { tau = 0.70, f_inc = 0.02, tau0 = 0.0375, f_attr = 0.568, mc_gdp = 0.89 }
dist_kw = { body_split = 5, body_split_from = 0.5 }

[rates.scenarios.gl_levy_stat_f005]
label = "Gain ladder, statutory levy, f_inc 5%"
wmin_house_ratio = 1.0
schedule = "gain_ladder"
levy_calibrate = false
levy = { tau = 0.70, f_inc = 0.05, tau0 = 0.0375, f_attr = 0.538, mc_gdp = 0.89 }
dist_kw = { body_split = 5, body_split_from = 0.5 }

[rates.scenarios.gl_levy_stat_f010]
label = "Gain ladder, statutory levy, f_inc 10%"
wmin_house_ratio = 1.0
schedule = "gain_ladder"
levy_calibrate = false
levy = { tau = 0.70, f_inc = 0.10, tau0 = 0.0375, f_attr = 0.488, mc_gdp = 0.89 }
dist_kw = { body_split = 5, body_split_from = 0.5 }

[rates.scenarios.gl_levy_stat_f015]
label = "Gain ladder, statutory levy, f_inc 15%"
wmin_house_ratio = 1.0
schedule = "gain_ladder"
levy_calibrate = false
levy = { tau = 0.70, f_inc = 0.15, tau0 = 0.0375, f_attr = 0.438, mc_gdp = 0.89 }
dist_kw = { body_split = 5, body_split_from = 0.5 }

[rates.scenarios.gl_levy_stat_f020]
label = "Gain ladder, statutory levy, f_inc 20%"
wmin_house_ratio = 1.0
schedule = "gain_ladder"
levy_calibrate = false
levy = { tau = 0.70, f_inc = 0.20, tau0 = 0.0375, f_attr = 0.388, mc_gdp = 0.89 }
dist_kw = { body_split = 5, body_split_from = 0.5 }
'''

LEVY_SCEN_NAMES = ('"gl_levy_cal_nominal", "gl_levy_cal_real", "gl_levy_stat_f002", "gl_levy_stat_f005",\n'
                   '  "gl_levy_stat_f010", "gl_levy_stat_f015", "gl_levy_stat_f020",')

# ═════════════════════════════════════════════════════════════════════════════
# PATCH MACHINERY
# ═════════════════════════════════════════════════════════════════════════════

ERRORS = []


def once(text, old, new, label):
    """Replace exactly one occurrence of `old`; record an error otherwise."""
    n = text.count(old)
    if n != 1:
        ERRORS.append(f'{label}: anchor found {n} times (need exactly 1): {old[:70]!r}')
        return text
    print(f'    ok  {label}')
    return text.replace(old, new)


def rx(text, pattern, new, label, flags=0):
    """Regex replace exactly one match; `new` is used literally."""
    hits = list(re.finditer(pattern, text, flags))
    if len(hits) != 1:
        ERRORS.append(f'{label}: pattern matched {len(hits)} times (need exactly 1): {pattern[:70]!r}')
        return text
    m = hits[0]
    print(f'    ok  {label}')
    return text[:m.start()] + new + text[m.end():]


def already(text, marker):
    return marker in text


def patch_wdt_fmt(t):
    if already(t, 'def slice_label'):
        print('    skip (already patched)')
        return t
    return t.rstrip('\n') + '\n' + FMT_ADD


def patch_wdt_core(t):
    if already(t, "'representativeness'"):
        print('    skip (already patched)')
        return t
    t = once(t, "lists = ('decomposition', 'rate_grid', 'schedules', 'cohorts', 'scope', 'stack', 'headline', 'consumption')",
             "lists = ('decomposition', 'rate_grid', 'schedules', 'cohorts', 'scope', 'stack', 'headline', 'consumption', 'levy')",
             'wdt_core: figures list "levy"')
    t = once(t, """    if defaults.get('levy_basis', 'nominal') not in ('nominal', 'real'):
        raise ValueError("[rates.defaults].levy_basis must be nominal | real")""",
             """    if defaults.get('levy_basis', 'nominal') not in ('nominal', 'real'):
        raise ValueError("[rates.defaults].levy_basis must be nominal | real")
    for n_, s_ in [('defaults', {'overrides': defaults})] + list(scenarios.items()):
        if s_['overrides'].get('levy_cal_base', '') not in ('', 'nominal', 'real'):
            raise ValueError(f"[rates.{n_}].levy_cal_base must be '' | nominal | real")""",
             'wdt_core: levy_cal_base validation')
    parse = '''    rr = r.get('representativeness')
    if not rr:
        raise ValueError("WDT_Params.toml has no [rates.representativeness] section (T23-T25)")
    representativeness = {
        'low_growth_max': float(rr['low_growth_max']), 'low_infl_max': float(rr['low_infl_max']),
        'focus_countries': [str(x) for x in rr['focus_countries']],
        'exp_today': float(rr['exp_today']), 'rev_today': float(rr['rev_today']),
        'n_boot': int(rr['n_boot']), 'boot_seed': int(rr['boot_seed']), 'block_years': int(rr['block_years']),
        'boot_ci': [float(x) for x in rr['boot_ci']],
        'bootstrap_scenarios': [str(x) for x in rr['bootstrap_scenarios']],
    }
    lo_q, hi_q = representativeness['boot_ci']
    if not 0.0 < lo_q < hi_q < 1.0:
        raise ValueError('[rates.representativeness].boot_ci must satisfy 0 < lower < upper < 1')
    if representativeness['n_boot'] < 50 or representativeness['block_years'] < 1:
        raise ValueError('[rates.representativeness]: n_boot must be >= 50 and block_years >= 1')
    bad = [n for n in representativeness['bootstrap_scenarios'] if n not in run['scenarios']]
    if bad:
        raise ValueError(f"[rates.representativeness].bootstrap_scenarios must be run by [rates.run].scenarios: {bad}")
    if not representativeness['bootstrap_scenarios']:
        raise ValueError('[rates.representativeness].bootstrap_scenarios must name at least one scenario')
'''
    t = once(t, "    return {\n        'jst_path': str(r['jst_path']), 'uk_iso': str(r['uk_iso']),",
             parse + "    return {\n        'jst_path': str(r['jst_path']), 'uk_iso': str(r['uk_iso']),",
             'wdt_core: parse [rates.representativeness]')
    t = once(t, "'replacement': replacement, 'levy_calibration': levy_calibration,",
             "'replacement': replacement, 'levy_calibration': levy_calibration,\n        'representativeness': representativeness,",
             'wdt_core: return representativeness')
    return t


def patch_rates_core(t):
    if already(t, 'def block_bootstrap'):
        print('    skip (already patched)')
        return t
    t = once(t, '\nCLI\n', CORE_DOC + '\nCLI\n', 'rates_core: docstring')
    t = once(t, "VARIANT_COLS = ('censored', 'fill_year', 'relief_gdp', 'cov_ref', 'cov_ref_uncond', 'fail', 'net_gdp_mean')",
             "VARIANT_COLS = ('censored', 'fill_year', 'relief_gdp', 'cov_ref', 'cov_ref_uncond', 'fail', 'net_gdp_mean', 'levy_gdp_mean')",
             'rates_core: VARIANT_COLS')
    t = once(t, "VARIANT_MED = ('relief_gdp', 'cov_ref', 'net_gdp_mean', 'fill_year')",
             "VARIANT_MED = ('relief_gdp', 'cov_ref', 'net_gdp_mean', 'fill_year', 'levy_gdp_mean')", 'rates_core: VARIANT_MED')
    # calibration base per scenario
    t = once(t, "key = (id(J), cfg['T'], tuple(sorted(lv.items())), lc['solve'], lc['target_gdp'], lc['base'])",
             "cal_base = cfg.get('levy_cal_base') or lc['base']          # per-scenario override of [rates.levy_calibration].base\n"
             "    key = (id(J), cfg['T'], tuple(sorted(lv.items())), lc['solve'], lc['target_gdp'], cal_base)",
             'rates_core: calibrate_levy key')
    t = once(t, "bm = base[lc['base']]", "bm = base[cal_base]", 'rates_core: calibrate_levy base')
    t = once(t, "'needed_rate': need, 'base': lc['base'],", "'needed_rate': need, 'base': cal_base,", 'rates_core: levy_cal base in diag')
    # window columns
    t = once(t, "f'net_gdp_mean__{b_}': float((out['net'] + lp).mean())})",
             "f'net_gdp_mean__{b_}': float((out['net'] + lp).mean()),\n"
             "                    f'levy_gdp_mean__{b_}': float(lp.mean())})", 'rates_core: levy_gdp_mean per case')
    t = once(t, "replaced = cal['replaced_ref']",
             "replaced = cal['replaced_ref']\n"
             "    # window regime for the representativeness slices (T23): geometric-mean REAL GDP/head growth, mean CPI inflation\n"
             "    gpc_r = scn['gpc'] if cfg['basis'] == 'real' else (1.0 + scn['gpc']) / (1.0 + scn['infl']) - 1.0\n"
             "    gpc_real_gm = float(np.prod(1.0 + gpc_r) ** (1.0 / cfg['T']) - 1.0)",
             'rates_core: regime columns (compute)')
    t = once(t, "'r_mean': float(scn['r'].mean()), 'exp_gdp_mean': float(scn['exp_gdp'].mean()),",
             "'r_mean': float(scn['r'].mean()), 'exp_gdp_mean': float(scn['exp_gdp'].mean()),\n"
             "        'gpc_real_gm': gpc_real_gm, 'infl_mean': float(scn['infl'].mean()),",
             'rates_core: regime columns (row)')
    # summaries
    t = once(t, 'def headline(df, p):', CORE_FUNCS + 'def headline(df, p, boot=False):', 'rates_core: slice / bootstrap functions')
    t = once(t, "out[mode]['levy_variants'] = {c: _variant_block(_variant_view(g, c), qs, band) for c in LEVY_CASES}",
             HEADLINE_HOOK, 'rates_core: headline hook')
    t = once(t, "'headline': headline(df, p),",
             "'headline': headline(df, p, boot=name in p['rates']['representativeness']['bootstrap_scenarios']),",
             'rates_core: run_scenario boot flag')
    t = once(t, "if 'windows' in sc:", VALIDATE_HOOK, 'rates_core: validate slices')
    t = once(t, "for key in ('decomposition', 'rate_grid', 'schedules', 'cohorts', 'scope', 'stack', 'headline', 'consumption'):",
             "for key in ('decomposition', 'rate_grid', 'schedules', 'cohorts', 'scope', 'stack', 'headline', 'consumption', 'levy'):",
             'rates_core: figure_scenarios keys')
    t = once(t, 'return list(dict.fromkeys(names))',
             "names += p['rates']['representativeness']['bootstrap_scenarios']\n    return list(dict.fromkeys(names))",
             'rates_core: figure_scenarios bootstrap list')
    return t


def patch_tables(t):
    if already(t, 'def t23_representativeness'):
        print('    skip (already patched)')
        return t
    m = re.search(r'from wdt_fmt import [^\n]*', t)
    if not m:
        ERRORS.append('8_2: wdt_fmt import line not found')
    else:
        t = t[:m.end()] + ', slice_label' + t[m.end():]
        print('    ok  8_2: import slice_label')
    t = rx(t, r'def _levy_note\(sc\):.*?(?=\n\ndef _thr)', LEVY_NOTE, '8_2: _levy_note (base-aware)', re.S)
    t = once(t, '# (number, slug, function): the numbers and slugs must match FIGURES',
             TABLES_NEW + '# (number, slug, function): the numbers and slugs must match FIGURES', '8_2: new tables')
    t = once(t, "(22, 'net_position', t22_net_position)", TABLES_REG, '8_2: TABLES registry')
    return t


def patch_charts(t):
    if already(t, 'def f23_representativeness'):
        print('    skip (already patched)')
        return t
    m = re.search(r'from wdt_fmt import [^\n]*', t)
    if not m:
        ERRORS.append('8_3: wdt_fmt import line not found')
    else:
        t = t[:m.end()] + ', slice_label' + t[m.end():]
        print('    ok  8_3: import slice_label')
    t = _imp_fig_pair_t(t)
    t = once(t, '# (number, slug, function): the numbers and slugs must match TABLES',
             CHARTS_NEW + '# (number, slug, function): the numbers and slugs must match TABLES', '8_3: new figures')
    t = once(t, "(22, 'net_position', f22_net_position)", CHARTS_REG, '8_3: FIGURES registry')
    return t


def _imp_fig_pair_t(t):
    m = re.search(r'(from wdt_style import \([^)]*?FIG_PAIR),', t)
    if not m:
        ERRORS.append('8_3: wdt_style import (FIG_PAIR) not found')
        return t
    print('    ok  8_3: import FIG_PAIR_T')
    return t[:m.end(1)] + ', FIG_PAIR_T,' + t[m.end():]


def patch_toml(t):
    if already(t, '[rates.representativeness]'):
        print('    skip (already patched)')
        return t
    t = once(t, 'levy_calibrate   = true',
             'levy_cal_base    = ""           # "" = solve the levy on [rates.levy_calibration].base | "nominal" | "real": the base THIS scenario solves on\n'
             'levy_calibrate   = true', 'toml: defaults levy_cal_base')
    t = once(t, '"gl_c_001", "gl_c_002", "gl_c_005", "gl_stationary", "gl_top6_1", "gl_top6_1_free",',
             '"gl_c_001", "gl_c_002", "gl_c_005", "gl_stationary", "gl_top6_1", "gl_top6_1_free",\n'
             '  # levy calibration base and f_inc (T25 / F25)\n  ' + LEVY_SCEN_NAMES, 'toml: run.scenarios')
    t = once(t, '"gl_stationary", "gl_top6_1", "gl_top6_1_free"]',
             '"gl_stationary", "gl_top6_1", "gl_top6_1_free"]\n'
             '# T25 / F25: levy calibration base and f_inc, on the main scenario\'s schedule (the main scenario is added in front)\n'
             'levy         = ["gl_levy_cal_nominal", "gl_levy_cal_real", "gl_levy_stat_f002", "gl_levy_stat_f005", "gl_levy_stat_f010", '
             '"gl_levy_stat_f015", "gl_levy_stat_f020"]', 'toml: figures.levy')
    return t.rstrip('\n') + '\n' + TOML_NEW_SCEN


TARGETS = [
    ('wdt_fmt.py', patch_wdt_fmt),
    ('wdt_core.py', patch_wdt_core),
    ('WDT_Params.toml', patch_toml),
    ('rates_core.py', patch_rates_core),
    ('8_2_RATES_tables.py', patch_tables),
    ('8_3_RATES_charts.py', patch_charts),
]


def locate(root, name):
    hits = [x for x in Path(root).rglob(name) if 'OUTPUTS' not in x.parts and '.git' not in x.parts and not x.name.endswith('.bak_regime')]
    if len(hits) != 1:
        ERRORS.append(f'{name}: found {len(hits)} copies under {root} (need exactly 1): {[str(h) for h in hits]}')
        return None
    return hits[0]


def main():
    ap = argparse.ArgumentParser(description='Apply the RATES representativeness patch')
    ap.add_argument('--model', default='.', help='Model/ folder (searched recursively)')
    ap.add_argument('--dry', action='store_true', help='check anchors, write nothing')
    a = ap.parse_args()

    results = []
    for name, fn in TARGETS:
        path = locate(a.model, name)
        if path is None:
            continue
        print(f'{name}  ({path})')
        raw = path.read_bytes().decode('utf-8')
        crlf = '\r\n' in raw
        text = raw.replace('\r\n', '\n')
        new = fn(text)
        results.append((path, raw, new, crlf))

    if ERRORS:
        print('\nNOTHING WRITTEN. Problems:')
        for e in ERRORS:
            print('  -', e)
        sys.exit(1)

    changed = [(p, r, n, c) for p, r, n, c in results if n.replace('\n', '\r\n' if c else '\n') != r]
    if a.dry:
        print(f'\nDry run OK: {len(changed)} file(s) would change.')
        return
    for path, raw, new, crlf in changed:
        shutil.copy2(path, str(path) + '.bak_regime')
        path.write_bytes((new.replace('\n', '\r\n') if crlf else new).encode('utf-8'))
        print(f'patched {path}  (backup: {path.name}.bak_regime)')
    print(f'\nDone: {len(changed)} file(s) patched. Next: python rates_core.py (full run), then 8_2 and 8_3, then rates_test.py')


if __name__ == '__main__':
    main()
