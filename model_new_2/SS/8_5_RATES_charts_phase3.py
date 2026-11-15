"""
8_5_RATES_charts_phase3.py -- RATES figures for the Phase 3 outputs (WDT_Refactor_Plan section 5)
=================================================================================================
PRESENTATION LAYER. Reads OUTPUTS/RATES/rates_data.json and writes
OUTPUTS/RATES/charts/rates_fig_{n}_{slug}.png. Figure n is the picture of table n in
8_4_RATES_tables_phase3.py: same number, same slug. Fold into 8_3_RATES_charts.py with 8_4 into 8_2 once
the numbering settles.

  26 effective_windows  windows per country: full loop, contiguous, seam-crossing, repeat years
  27 decade_relief      relief / GDP every 10 years (median, p10-p90 over filling windows) against expenditure
  28 route_b_fund       fund and receivable at window end by Route B treatment; lien spread sweep
  29 route_b_receipts   receipts by launch-wealth band: sale, lien, income; lien receivable
  30 route_b_wealth     family wealth at window end by launch-wealth band

The fund is settled cash only (D4d): the receivable is always drawn as its own bar, never stacked on the fund.
Percentiles in the JSON are over windows in which the fund fills; medians_all are over all windows.
No simulation, no import of rates_core.
"""

import sys
from pathlib import Path

import numpy as np

# wdt_* modules and WDT_Params.toml live in Model/, one level above this RATES folder
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import wdt_core as wc
from wdt_fmt import band_labels, ensure_dir, out_dir, fmt_pct
from wdt_style import (C_ANNOTATION, C_BASELINE, C_DARK, C_LRR, C_SSM, C_SURPLUS, C_TCM,
                       FIG_PAIR, FIG_SINGLE, FIG_WIDE, apply_style, save_fig)

CODE = 'RATES'


# ── helpers (same accessors as 8_4) ──────────────────────────────────────────

def _plt():
    import matplotlib.pyplot as plt
    return plt


def _path(n, slug):
    return ensure_dir(out_dir(CODE) / 'charts') / f'rates_fig_{n}_{slug}.png'


def _nan(x):
    return np.nan if x is None else float(x)


def _pct(ax, axis='y', decimals=1):
    from matplotlib.ticker import PercentFormatter
    (ax.xaxis if axis == 'x' else ax.yaxis).set_major_formatter(PercentFormatter(1.0, decimals=decimals))


def _wrap(label, width=14):
    words, lines, cur = label.split(), [], ''
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = f'{cur} {w}'.strip()
    return '\n'.join(lines + [cur])


def _hl(sc, mode, contiguous=False):
    blk = sc.get('headline_contiguous' if contiguous else 'headline') or {}
    if not blk:
        return None
    return blk[mode if mode in blk else next(iter(blk))]


def _med(h, col, all_windows=False):
    if h is None:
        return None
    ov = h['overall']
    return ((ov.get('medians_all') if all_windows else ov.get('medians')) or {}).get(col)


def _pq(h, col, key):
    if h is None:
        return None
    return (h['overall'].get(key) or {}).get(col)


def _years(med, prefix):
    return sorted(int(k[len(prefix):]) for k in med if k.startswith(prefix) and k[len(prefix):].isdigit())


def _need(data, name):
    sc = data['scenarios'].get(name)
    if sc is None:
        print(f'  skipped: scenario {name!r} is not in rates_data.json (run it: python rates_core.py --scenario {name})')
    return sc


def _route_b_names(data, p):
    return [n for n in p['rates']['figures'].get('route_b', []) if n in data['scenarios']]


def _default_of_mode(data, names, mode):
    for n in names:
        rb = data['scenarios'][n].get('route_b') or {}
        if rb.get('mode') == mode and rb.get('deferral_spread') is None and rb.get('income_cap') is None:
            return n
    return None


def _rb_label(sc):
    rb = sc.get('route_b') or {}
    m = rb.get('mode', 'sale')
    if m == 'lien':
        sp = rb.get('deferral_spread')
        return 'Lien' + (f', spread {fmt_pct(sp, 0)}' if sp is not None else ', default spread')
    if m == 'income':
        cap = rb.get('income_cap')
        return 'Income' + (f', cap {fmt_pct(cap, 0)}' if cap is not None else ', default cap')
    return 'Sale'


_MODE_COL = {'sale': C_SSM, 'lien': C_LRR, 'income': C_TCM}


# ── figures ──────────────────────────────────────────────────────────────────

def f26_effective_windows(data, p):
    """Windows per country, with the contiguous, seam-crossing and repeat-year subsets."""
    apply_style()
    fg = p['rates']['figures']
    sc = _need(data, fg['scenario'])
    if sc is None or 'effective_windows' not in sc:
        return None
    ew = sc['effective_windows']
    mode = fg['mode'] if fg['mode'] in ew['by_mode'] else next(iter(ew['by_mode']))
    blk = ew['by_mode'][mode]
    isos = sorted(blk['by_country'])
    x = np.arange(len(isos))
    w = 0.2
    fig, ax = _plt().subplots(figsize=FIG_WIDE)
    for k, (key, lab, col) in enumerate((('total', 'Full loop', C_DARK), ('contiguous', 'Contiguous only', C_SSM),
                                         ('wraps', 'Cross the seam', C_LRR), ('repeat', 'Repeat years', C_TCM))):
        ax.bar(x + (k - 1.5) * w, [blk['by_country'][i][key] for i in isos], w, color=col, label=lab)
    ax.set_xticks(x, isos)
    ax.set_ylabel('Windows')
    ax.set_title(f"Effective windows at T = {ew['T']} years, index {mode}")
    ax.legend()
    return save_fig(fig, _path(26, 'effective_windows'))


def f27_decade_relief(data, p):
    """Relief / GDP every tenth year, full loop and contiguous, against expenditure / GDP."""
    apply_style()
    fg = p['rates']['figures']
    sc = _need(data, fg['scenario'])
    if sc is None:
        return None
    mode = fg['mode']
    full, cont = _hl(sc, mode, False), _hl(sc, mode, True)
    yrs = _years(full['overall']['medians'], 'rel_y')
    if not yrs:
        print('  skipped figure 27: no rel_y* columns in the JSON')
        return None
    fig, ax = _plt().subplots(figsize=FIG_SINGLE)
    for h, lab, col, off in ((full, 'Full loop', C_SSM, -0.6), (cont, 'Contiguous only', C_LRR, 0.6)):
        if h is None:
            continue
        med = np.array([_nan(_med(h, f'rel_y{k}')) for k in yrs])
        lo = np.array([_nan(_pq(h, f'rel_y{k}', 'p10')) for k in yrs])
        hi = np.array([_nan(_pq(h, f'rel_y{k}', 'p90')) for k in yrs])
        xs = np.array(yrs) + off
        ax.errorbar(xs, med, yerr=[np.nan_to_num(med - lo), np.nan_to_num(hi - med)], fmt='o-', ms=4, color=col,
                    ecolor=col, elinewidth=1, capsize=2, label=f'Relief / GDP, {lab.lower()}')
    ax.plot(yrs, [_nan(_med(full, f'exp_y{k}')) for k in yrs], color=C_DARK, ls='--', label='Expenditure / GDP')
    ax.set_xlabel('Years from launch')
    ax.set_ylabel('Share of GDP (median, bars p10-p90 over windows that fill)')
    ax.set_title(f"Relief against expenditure by decade\n{sc['label']}, index {mode}")
    ax.legend(fontsize=8)
    _pct(ax, 'y', 1)
    return save_fig(fig, _path(27, 'decade_relief'))


def f28_route_b_fund(data, p):
    """Left: fund and receivable at window end by treatment (separate bars). Right: lien spread sweep."""
    apply_style()
    names = _route_b_names(data, p)
    if not names:
        return None
    mode = p['rates']['figures']['mode']
    scs = [data['scenarios'][n] for n in names]
    hs = [_hl(s, mode) for s in scs]
    x = np.arange(len(scs))
    w = 0.38
    fig, (a1, a2) = _plt().subplots(1, 2, figsize=FIG_PAIR)
    a1.bar(x - w / 2, [_nan(_med(h, 'fund_gdp_end', True)) for h in hs], w, color=C_SSM, label='Fund (settled cash)')
    a1.bar(x + w / 2, [_nan(_med(h, 'lien_out_gdp_end', True)) for h in hs], w, color=C_BASELINE, label='Receivable (not in the fund)')
    a1.set_xticks(x, [_wrap(_rb_label(s), 12) for s in scs], fontsize=7)
    a1.set_ylabel('Share of GDP at window end (median, all windows)')
    a1.set_title('Fund and receivable by treatment')
    a1.legend(fontsize=7)
    _pct(a1, 'y', 0)
    liens = sorted(((s['route_b']['deferral_spread'], h) for s, h in zip(scs, hs)
                    if (s.get('route_b') or {}).get('mode') == 'lien' and s['route_b'].get('deferral_spread') is not None),
                   key=lambda t: t[0])
    if len(liens) >= 2:
        sp = [t[0] for t in liens]
        a2.plot(sp, [_nan(_med(h, 'fund_gdp_end', True)) for _, h in liens], 'o-', color=C_SSM, label='Fund (settled cash)')
        a2.plot(sp, [_nan(_med(h, 'lien_out_gdp_end', True)) for _, h in liens], 's-', color=C_BASELINE, label='Receivable')
        a2.set_xlabel('Deferral spread')
        a2.set_title('Lien spread sweep')
        a2.legend(fontsize=7)
        _pct(a2, 'x', 0)
        _pct(a2, 'y', 0)
    else:
        a2.text(0.5, 0.5, 'Fewer than two lien spreads in [rates.figures].route_b', ha='center', va='center', fontsize=8,
                transform=a2.transAxes)
        a2.set_axis_off()
    fig.suptitle(f'Route B: what the fund holds and what is still owed, index {mode}')
    return save_fig(fig, _path(28, 'route_b_fund'))


def _band_figure(data, p, n, slug, series, ylabel, title, dec):
    """series: list of (mode, column prefix, label) drawn as grouped bars per launch-wealth band."""
    apply_style()
    names = _route_b_names(data, p)
    pick = {m: _default_of_mode(data, names, m) for m in ('sale', 'lien', 'income')}
    if not pick['sale'] or sum(bool(v) for v in pick.values()) < 2:
        print(f'  skipped figure {n}: needs a sale scenario and one of lien / income in [rates.figures].route_b')
        return None
    mode = p['rates']['figures']['mode']
    labels = band_labels(data['scenarios'][pick['sale']]['calibration']['bands']['edges_gbp_m'])
    series = [s for s in series if pick.get(s[0])]
    x = np.arange(len(labels))
    w = 0.8 / len(series)
    fig, ax = _plt().subplots(figsize=FIG_WIDE)
    for k, (m, prefix, lab) in enumerate(series):
        h = _hl(data['scenarios'][pick[m]], mode)
        ax.bar(x + (k - (len(series) - 1) / 2) * w, [_nan(_med(h, f'{prefix}{i}', True)) for i in range(len(labels))], w,
               color=_MODE_COL[m], label=lab)
    ax.set_xticks(x, [_wrap(l, 12) for l in labels], fontsize=7)
    ax.set_xlabel('Launch wealth band')
    ax.set_ylabel(ylabel)
    ax.set_title(f'{title}, index {mode}', fontsize=10)
    ax.legend(fontsize=8)
    _pct(ax, 'y', dec)
    return save_fig(fig, _path(n, slug))


def f29_route_b_receipts(data, p):
    return _band_figure(data, p, 29, 'route_b_receipts',
                        [('sale', 'recv_gdp_mean_band', 'Receipts, sale'), ('lien', 'recv_gdp_mean_band', 'Receipts, lien'),
                         ('income', 'recv_gdp_mean_band', 'Receipts, income')],
                        'Mean annual receipts, share of GDP (median, all windows)', 'Route B receipts by launch-wealth band (mean annual receipts; the receivable is in Table 29)', 2)


def f30_route_b_wealth(data, p):
    return _band_figure(data, p, 30, 'route_b_wealth',
                        [('sale', 'wealth_gdp_end_band', 'Family wealth, sale'), ('lien', 'wealth_gdp_end_band', 'Family wealth, lien'),
                         ('income', 'wealth_gdp_end_band', 'Family wealth, income')],
                        'Share of GDP at window end (median, all windows)',
                        'Family wealth at window end by launch-wealth band', 1)


# (number, slug, function): the numbers and slugs must match TABLES in 8_4_RATES_tables_phase3.py
FIGURES = [
    (26, 'effective_windows', f26_effective_windows),
    (27, 'decade_relief', f27_decade_relief),
    (28, 'route_b_fund', f28_route_b_fund),
    (29, 'route_b_receipts', f29_route_b_receipts),
    (30, 'route_b_wealth', f30_route_b_wealth),
]


def main(json_path=None, toml=None):
    import matplotlib
    matplotlib.use('Agg')
    p = wc.load_rates_params(toml)
    data = wc.load_json(Path(json_path) if json_path else out_dir(CODE) / 'rates_data.json')
    done = 0
    for n, slug, fn in FIGURES:
        if fn(data, p) is not None:
            done += 1
            print(f'  Figure {n}: {slug}')
    print(f'Written {done} of {len(FIGURES)} figures to {out_dir(CODE) / "charts"}')


if __name__ == '__main__':
    main()
