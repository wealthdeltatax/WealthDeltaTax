"""
Patch for table 31 / figure 31 (and the Route B income column name in 30).

rates_core.py never writes data['archetype_sweep']. It writes ordinary scenarios (gl_arch_*), each with
cfg.route_mix, cfg.route_b_mode, headline.<mode>.overall.medians / medians_all, and the archetype definitions
live in the TOML ([archetypes.*], read as p['archetypes']). So T31/F31 now read those.

=== 1. 8_2_RATES_tables.py: DELETE _arch_block and t31_archetype_sweep; paste this in their place ===
"""

# ---------------------------------------------------------------- TABLES
def _arch_rows(data, p):
    """One row per gl_arch_* scenario, from the scenario blocks rates_core writes."""
    fg = p['rates']['figures']
    mode, grp = fg['mode'], fg['group']
    arch = p.get('archetypes') or {}
    rows = []
    for name, sc in data['scenarios'].items():
        if not name.startswith('gl_arch_'):
            continue
        h = _hl(sc, mode)
        if h is None:
            continue
        cfg = sc['cfg']
        mix = cfg.get('route_mix') or 'none'
        shares = V0 = None
        if mix in arch:                                   # one archetype in every cell
            shares, V0 = arch[mix]['shares'], arch[mix]['V0_m']
        elif mix == 'blend':                              # same blend in every cell
            w = cfg.get('route_mix_weights') or {}
            shares = {r: sum(w.get(k, 0.0) * arch[k]['shares'][r] for k in arch) for r in 'ABCD'}
        rows.append({'name': name, 'label': sc['label'], 'mix': mix, 'V0_m': V0, 'shares': shares,
                     'b_mode': (sc.get('route_b') or {}).get('mode', 'sale'),
                     'censored_share': h['overall']['censored_share'],
                     'cov_ref': _med(h, 'cov_ref'), 'fill_year': _med(h, 'fill_year'),
                     'stock': _med(h, f'er_stock_{grp}', True), 'gain': _med(h, f'er_gain_{grp}', True),
                     'income_cum': _med(h, 'income_cum_gdp', True)})
    return rows, mode, grp


def t31_archetype_sweep(data, p):
    rows_, mode, grp = _arch_rows(data, p)
    if not rows_:
        print("  skipped: no gl_arch_* scenarios in rates_data.json (python rates_core.py --scenario gl_arch_wealth ...)")
        return None
    rows = []
    for r in rows_:
        s = r['shares']
        rows.append([f"**{r['label']}**", f"£{r['V0_m']:g}m" if r['V0_m'] else 'by cell',
                     ' / '.join(fmt_pct0(s[k]) for k in 'ABCD') if s else 'by launch wealth',
                     r['b_mode'], fmt_pct(r['stock']), fmt_pct1(r['gain']), fmt_pct1(r['cov_ref']),
                     fmt_pct(r['censored_share'], 0), fmt_f0(r['fill_year']),
                     fmt_pct(r['income_cum']) if r['b_mode'] == 'income' else DASH])
    d = MdDoc()
    d.table(['Scenario', 'Entry wealth', 'Route mix A / B / C / D', 'Route B', f'Stock rate ({group_label(grp)})',
             f'Gain rate ({group_label(grp)})', 'Spending covered', 'Never fills', 'Fill year',
             'Cumulative income paid, years of GDP'], rows, col_fmt=[LEFT, RIGHT, RIGHT, LEFT] + [RIGHT] * 6)
    d.caption(f"Table 31: Revenue, burden and fund outcomes by route-mix scenario (gl_arch_*), index = {mode}. Route mix is the share of "
              f"holdings on Route A (listed, annual cash), B (property), C (self-declared, settled in kind) and D (appraised, cash); a "
              f"single archetype applies to every cell, 'by launch wealth' interpolates the archetypes in ln W. Stock and gain rates are "
              f"realised WDT over wealth and over accrued return, wealth-weighted, medians over all windows. Spending covered and fill year are "
              f"medians over windows in which the fund fills; 'never fills' is the share of all windows. Cumulative income paid is the external "
              f"income handed to WDT over the window (income mode only), reported apart from wealth. Mixes, entry wealth and income ratios are "
              f"placeholders in [archetypes.*] and [income.by_archetype].")
    return d
# also change the import line in 8_2 to include group_label (it is already imported there: group_label is in the wdt_fmt import).


# ---------------------------------------------------------------- CHART
"""
=== 2. 8_3_RATES_charts.py: DELETE f31_archetype_sweep; paste this in its place ===
"""
def f31_archetype_sweep(data, p):
    """Route mix (left), realised burden (middle), spending covered with the never-fills share (right), by gl_arch_* scenario."""
    apply_style()
    fg = p['rates']['figures']
    mode, grp = fg['mode'], fg['group']
    arch = p.get('archetypes') or {}
    scs = []
    for name, sc in data['scenarios'].items():
        h = _hl(sc, mode) if name.startswith('gl_arch_') else None
        if h is not None:
            scs.append((sc, h))
    if not scs:
        print("  skipped figure 31: no gl_arch_* scenarios in rates_data.json")
        return None
    x = np.arange(len(scs))
    labels = [_wrap(sc['label'].replace('Gain ladder, ', ''), 16) for sc, _ in scs]

    def shares(sc):
        cfg, mix = sc['cfg'], sc['cfg'].get('route_mix') or 'none'
        if mix in arch:
            return arch[mix]['shares']
        if mix == 'blend':
            w = cfg.get('route_mix_weights') or {}
            return {r: sum(w.get(k, 0.0) * arch[k]['shares'][r] for k in arch) for r in 'ABCD'}
        return None                                                 # 'wealth': varies by cell, no single mix

    fig, (a1, a2, a3) = _plt().subplots(1, 3, figsize=FIG_TRIPLE)
    bottom = np.zeros(len(scs))
    for key, col in zip('ABCD', (C_SSM, C_LRR, C_TCM, C_SURPLUS)):
        v = np.array([(shares(sc) or {}).get(key, 0.0) for sc, _ in scs])
        a1.bar(x, v, bottom=bottom, color=col, label=f'Route {key}')
        bottom += v
    for i, (sc, _) in enumerate(scs):
        if shares(sc) is None:
            a1.text(x[i], 0.5, 'by\nwealth', ha='center', va='center', fontsize=6)
    a1.set_title('Route mix (single-mix scenarios)')
    a1.legend(fontsize=7, loc='lower right')
    _pct(a1, 'y', 0)
    w = 0.38
    a2.bar(x - w / 2, [_nan(_med(h, f'er_stock_{grp}', True)) for _, h in scs], w, color=C_SSM, label='Stock rate (left axis)')
    a2.set_ylabel('Realised stock rate per year')
    _pct(a2, 'y', 1)
    a2b = a2.twinx()
    a2b.bar(x + w / 2, [_nan(_med(h, f'er_gain_{grp}', True)) for _, h in scs], w, color=C_TCM, label='Gain rate (right axis)')
    a2b.set_ylabel('Realised gain rate per year')
    _pct(a2b, 'y', 0)
    a2b.grid(False)
    a2.set_title('Burden (wealth-weighted)')
    a3.bar(x - w / 2, [_nan(_med(h, 'cov_ref')) for _, h in scs], w, color=C_LRR, label='Spending covered (median, filling windows)')
    a3.bar(x + w / 2, [_nan(h['overall']['censored_share']) for _, h in scs], w, color=C_BASELINE, label='Never fills (share of windows)')
    a3.set_title('Fund outcome')
    a3.legend(fontsize=7)
    _pct(a3, 'y', 0)
    for ax in (a1, a2, a3):
        ax.set_xticks(x, labels, fontsize=5, rotation=60, ha='right')
    fig.suptitle(f'Route-mix scenarios (gl_arch_*), index {mode}')
    return save_fig(fig, _path(31, 'archetype_sweep'))


"""
=== 3. Tables 29/30 and figure 30 read columns rates_core does not write ===
rates_core writes   income_cum_gdp_band{i}      (cumulative income paid, years of GDP, by launch band)
the presentation reads income_paid_cum_gdp_band{i}   -> rename in:
  8_2 t30_route_b_wealth :  f'income_paid_cum_gdp_band{i}'  ->  f'income_cum_gdp_band{i}'
  8_3 f30_route_b_wealth :  f'income_paid_cum_gdp_band{i}'  ->  f'income_cum_gdp_band{i}'
rates_core does not write income_short_share_band{i} at all; t30's last column will show a dash until the core adds it
(run_lines already has b_sold_b; it needs a share = sold value / liability per band in run_window).

Also delete the old docstring contract for data['archetype_sweep'] in 8_2 (and its mention in 8_3), since no such block exists.
"""
