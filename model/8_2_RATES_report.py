"""
WDT Rates and Revenue — Markdown Report  (v8)
==============================================
Produces the self-contained Markdown run report:

    OUTPUTS/RATES/7_5_WDT_Rates_Revenue_Output.md

Sections
--------
  B.1  Active parameters
  B.2  SSM results — active scenario (failure years + coverage windows)
  B.3  TCM results — N periods
         B.3.1  Net worth at start and year N
         B.3.2  Net per taxpayer (capitalisation window)
         B.3.3  Annual wealth burden
         B.3.4  Effective rate on gains
         B.3.5  Lifetime average net tax
         B.3.6  Population distribution
         B.3.7  Tax collected per year (capitalisation window)
         B.3.8  Cohort proportion of total tax paid
         B.3.9  Revenue by tier + TCM coverage windows
  B.4  Start-year sweep (extremals + full 73-row table)
  B.5  Statistical pass

Usage
-----
  python3 8_2_RATES_report.py [params.toml] [output_dir]

  params.toml  defaults to WDT_Params.toml in the same directory.
  output_dir   defaults to ./OUTPUTS/RATES/

Can also be imported and called directly:

    from 8_2_RATES_report import write_report
    out_path = write_report(p, py_ssm, py_tcm, ssm_lrr_N,
                            sweep_extremals, stats, tcm_win=tcm_win)
"""

import sys
from pathlib import Path

import rates_model as model
from rates_model import COVERAGE_WINDOWS, _tcm_coverage_windows

from wdt_fmt import fmt_gbp_yr, today_iso, ensure_dir, out_dir  # fmt_rev_m intentionally not used — see _fmt_m below
from wdt_md  import MdDoc, LEFT, RIGHT, CENTER

DEFAULT_PARAMS = Path(__file__).parent / 'WDT_Params.toml'
_OUT           = out_dir('RATES')

# _fmt_gbp: suppress near-zero £/yr values (column header supplies the unit)
_fmt_gbp = fmt_gbp_yr

# _fmt_m: revenue in £m/yr — no 'm' suffix because the section heading
# already says "(£m/yr)".  Intentionally differs from wdt_fmt.fmt_rev_m
# which appends an 'm'.  Threshold matches the original 8_3 lambda.
def _fmt_m(v, threshold=5e-4):
    return '£—' if abs(v) < threshold else f'£{v:,.0f}'


# ─────────────────────────────────────────────────────────────
# PUBLIC ENTRY POINT
# ─────────────────────────────────────────────────────────────

def write_report(p, py_ssm, py_tcm, tcm_N, sweep_extremals, stats,
                 tcm_win=None, output_dir=None):
    """
    Write the full Markdown run report and return the output Path.

    Parameters
    ----------
    p               : dict   loaded params (wdt_core.load_params())
    py_ssm          : list   run_ssm() result (list of year dicts)
    py_tcm          : dict   run_tcm() result (keyed by tier differential)
    tcm_N           : int    horizon used for TCM (SSM LRR fill year)
    sweep_extremals : dict   report_start_year_sweep() return value
    stats           : dict   compute_statistics() return value
    tcm_win         : dict   _tcm_coverage_windows() return value, or None
    output_dir      : Path   override output directory; defaults to OUTPUTS/RATES/
    """
    _out = ensure_dir(Path(output_dir) if output_dir else _OUT)
    out_path = _out / '7_5_WDT_Rates_Revenue_Output.md'

    doc = MdDoc()
    _header(doc, p)
    _b1_params(doc, p)
    _b2_ssm(doc, p, py_ssm)
    _b3_tcm(doc, p, py_ssm, py_tcm, tcm_N, tcm_win)
    _b4_sweep(doc, p, sweep_extremals)
    _b5_stats(doc, stats)
    doc.write(out_path)
    return out_path


# ─────────────────────────────────────────────────────────────
# SECTION BUILDERS
# ─────────────────────────────────────────────────────────────

def _header(doc, p):
    meta     = p.get('meta', {})
    scenario = meta.get('scenario_label', 'unknown')
    doc.h1('WDT Rates and Revenue — Model Output')
    doc.blank()
    doc.add(f'**Run date:** {today_iso()}  ')
    doc.add(f'**Scenario:** {scenario}  ')
    doc.add(f'**Model version:** {meta.get("version", "v8")}  ')
    doc.add(f'**Parameters file:** `{DEFAULT_PARAMS.name}`  ')
    doc.blank()


def _b1_params(doc, p):
    doc.h2('B.1 Active Parameters')
    doc.blank()
    doc.table(
        ['Parameter', 'Value'],
        [
            [r'$\tau_0$ (floor rate)',           f'{p["tau_0"]:.0%}'],
            [r'$\tau_m$ (ceiling rate)',          f'{p["tau_m"]:.0%}'],
            [r'$k$ (steepness, per £m)',          str(p['k'])],
            [r'$W_{\min}$ (£m)',                 f'£{p["W_min"]}m'],
            ['SRR capitalisation ratio',          f'{p["srr_ratio"]}×'],
            ['LRR floor (years of expenditure)',  f'{p["lrr_years"]} years'],
            ['Budget base (£b)',                  f'£{p["budget_base"]:,.1f}b'],
            ['Budget growth (p.a.)',              f'{p["budget_growth"]:.2%}'],
            ['Historical mean return',            f'{p["hist_mean"]:.2%}'],
        ],
        col_fmt=[LEFT, LEFT],
    )
    doc.blank()
    doc.add('**Growth tiers:**')
    doc.blank()
    doc.table(
        ['Tier', 'Weight', 'Differential', 'Implied return'],
        [
            [t['label'], f'{t["weight"]:.0%}', f'{t["differential"]:+.2%}',
             f'{p["hist_mean"] + t["differential"]:.2%}']
            for t in p['tiers']
        ],
        col_fmt=[LEFT, RIGHT, RIGHT, RIGHT],
    )
    doc.blank()


def _b2_ssm(doc, p, py_ssm):
    doc.h2('B.2 SSM Results — Active Scenario')
    doc.blank()

    ssm_last    = py_ssm[-1]
    py_lrr_fill = next((r for r in py_ssm if r.get('lrr_filled')), None)

    srr_fill_yr = ssm_last.get('srr_fill_year', '—')
    lrr_fill_yr = ssm_last.get('lrr_fill_year', '—')
    lrr_fail_yr = ssm_last.get('lrr_failure_year')
    srr_fail_yr = ssm_last.get('srr_failure_year')
    fail_gap    = ssm_last.get('lrr_srr_failure_gap')

    def _fv(v, suffix=''):
        return f'{v}{suffix}' if v is not None else '—'

    srr_at_lrr    = (f'£{py_lrr_fill["srr_balance"]:,.0f}b' if py_lrr_fill else '—')
    lrr_surp      = (f'£{(py_lrr_fill["lrr_balance"] - py_lrr_fill["lrr_target"]):,.0f}b'
                     if py_lrr_fill else '—')
    budget_at_lrr = f'£{py_lrr_fill["budget"]:,.0f}b' if py_lrr_fill else '—'

    lrr_fail_cell = (_fv(lrr_fail_yr, ' (buffer exhausted)')
                     if lrr_fail_yr else 'no failure within 71-year window')
    srr_fail_cell = (_fv(srr_fail_yr, ' (refund guarantee broken)')
                     if srr_fail_yr else 'no failure within 71-year window')

    doc.table(
        ['Metric', 'Value'],
        [
            ['SRR fill year',                            _fv(srr_fill_yr)],
            ['LRR breakeven year',                       _fv(lrr_fill_yr)],
            ['Annual expenditure at LRR breakeven (£b)', budget_at_lrr],
            ['SRR balance at LRR breakeven (£b)',        srr_at_lrr],
            ['LRR surplus at breakeven (£b)',            lrr_surp],
            ['LRR failure year',                         lrr_fail_cell],
            ['SRR failure year',                         srr_fail_cell],
            ['LRR→SRR failure gap (years)',              _fv(fail_gap)],
        ],
        col_fmt=[LEFT, LEFT],
    )
    doc.blank()

    doc.add('**SSM Step-5 coverage fraction by window (average % of annual expenditure '
            'available for labour tax relief):**')
    doc.blank()

    cov_rows = []
    for W in COVERAGE_WINDOWS:
        cov   = ssm_last.get(f'ssm_cov_{W}')
        zcov  = ssm_last.get(f'ssm_zero_cov_years_{W}')
        mlrr  = ssm_last.get(f'ssm_min_lrr_bal_{W}')
        bloor = ssm_last.get(f'ssm_lrr_below_floor_years_{W}')
        cov_rows.append([
            f'{W} years',
            f'{cov:.1%}'      if cov   is not None else '—',
            str(zcov)         if zcov  is not None else '—',
            f'£{mlrr:,.0f}b'  if mlrr  is not None else '—',
            str(bloor)        if bloor is not None else '—',
        ])
    doc.table(
        ['Window', 'SSM coverage', 'Zero-coverage years',
         'Min LRR balance (£b)', 'Years LRR below floor'],
        cov_rows,
        col_fmt=[LEFT, RIGHT, RIGHT, RIGHT, RIGHT],
    )
    doc.note(
        'SSM applies uniform historical returns across the population (correlated-shock '
        'assumption — worst-case floor). Coverage fraction = Step-5 remainder / annual '
        'expenditure; zero in any year where LRR or SRR balance hits zero. TCM coverage '
        '(heterogeneous-tier ceiling) appears in §B.3.'
    )


def _b3_tcm(doc, p, py_ssm, py_tcm, tcm_N, tcm_win):
    py_lrr_fill = next((r for r in py_ssm if r.get('lrr_filled')), None)

    diffs    = [t['differential'] for t in p['tiers']]
    tlabels  = [f"{t['differential']:+.2%} ({t['label']})" for t in p['tiers']]
    blabels  = [b['label'] for b in p['brackets']]
    tweights = [t['weight'] for t in p['tiers']]

    doc.h2(f'B.3 TCM Results — N={tcm_N} periods')
    doc.blank()

    # B.3.1 — Net worth
    doc.h3('B.3.1 Net worth — start ($V_0$) and year N (£m)')
    doc.note(
        '$V_0$ is the bracket mean wealth (£m) at entry, identical across tiers within a '
        'bracket. V_N is the true wealth (before tax settlement) at the end of period N '
        'for a representative taxpayer, varying by tier due to persistent return '
        'differentials. Figures are for a single representative taxpayer; they do not '
        'reflect aggregate portfolio wealth.'
    )
    # This table has a non-uniform header (V_0 row differs from tier rows),
    # so we build it with MdDoc.add() rather than md_table().
    header = '| Net worth (£m) |' + ''.join(f' {b} |' for b in blabels)
    sep    = '|---|' + '---|' * len(blabels)
    doc.add(header)
    doc.add(sep)
    doc.add('| **$V_0$ (start, all tiers)** |'
            + ''.join(f' £{b["V0_m"]:,.3f}m |' for b in p['brackets']))
    for i, diff in enumerate(diffs):
        vals = [r['V_at_N'] for r in py_tcm[diff]]
        doc.add(f'| **V_N {tlabels[i]}** |'
                + ''.join(f' £{v:,.2f}m |' for v in vals))
    doc.blank()

    # B.3.2 — Net per taxpayer (capitalisation window)
    doc.h3('B.3.2 Net per taxpayer per year — capitalisation window average (£/yr)')
    doc.note(
        'Average annual net tax per representative taxpayer over the capitalisation '
        'window (SRR fill year to LRR breakeven year). Zeros suppressed.'
    )
    _tier_bracket_table(doc, diffs, tlabels, blabels,
                        field='post_fill_net_gbp', py_tcm=py_tcm,
                        fmt=lambda v: _fmt_gbp(v))

    # B.3.3 — Annual wealth burden
    doc.h3('B.3.3 Annual wealth burden (tax as % of net worth)')
    doc.blank()
    _tier_bracket_table(doc, diffs, tlabels, blabels,
                        field='wealth_burden', py_tcm=py_tcm,
                        fmt=lambda v: f'{v:.2%}')

    # B.3.4 — Effective rate on gains
    doc.h3('B.3.4 Effective rate on gains (tax as % of annual gain)')
    doc.blank()
    _tier_bracket_table(doc, diffs, tlabels, blabels,
                        field='eff_rate', py_tcm=py_tcm,
                        fmt=lambda v: f'{v:.1%}')

    # B.3.5 — Lifetime average net tax
    doc.h3('B.3.5 Average annual net tax per taxpayer — lifetime average (£/yr)')
    doc.blank()
    _tier_bracket_table(doc, diffs, tlabels, blabels,
                        field='avg_net_gbp', py_tcm=py_tcm,
                        fmt=lambda v: _fmt_gbp(v))

    # B.3.6 — Population distribution
    doc.h3('B.3.6 Population distribution (taxpayers per bracket per tier)')
    doc.note(
        'Cell population = bracket population × tier weight. '
        'Bracket population is constant within a bracket across tiers.'
    )
    _tier_bracket_table(doc, diffs,
                        [f'{tweights[i]:.0%} ({p["tiers"][i]["label"]})'
                         for i in range(len(diffs))],
                        blabels,
                        field='cell_pop', py_tcm=py_tcm,
                        fmt=lambda v: f'{int(round(v)):,}')

    # B.3.7 — Tax collected per year (capitalisation window)
    doc.h3('B.3.7 Tax collected per year — capitalisation window average (£m/yr)')
    doc.note(
        'Average annual revenue per bracket-tier cell over the capitalisation window. '
        'Row total is the sum across all brackets for that tier. '
        'Column total is the sum across all tiers for that bracket. '
        'Grand total is in the bottom-right cell.'
    )
    # Needs totals rows — hand-built
    grand_total = 0.0
    col_totals  = [0.0] * len(blabels)
    tier_rows   = []
    for i, diff in enumerate(diffs):
        rev_vals  = [r['post_fill_revenue_m'] for r in py_tcm[diff]]
        row_total = sum(rev_vals)
        grand_total += row_total
        for j, v in enumerate(rev_vals):
            col_totals[j] += v
        tier_rows.append(
            [f'{tweights[i]:.0%} ({p["tiers"][i]["label"]})']
            + [_fmt_m(v) for v in rev_vals]
            + [f'**£{row_total:,.1f}m**']
        )
    tier_rows.append(
        ['**Column total**']
        + [f'**£{v:,.1f}m**' for v in col_totals]
        + [f'**£{grand_total:,.1f}m**']
    )
    doc.table(
        ['Tier (weight) \\ Bracket'] + blabels + ['**Row total**'],
        tier_rows,
        col_fmt=[LEFT] + [RIGHT] * len(blabels) + [RIGHT],
    )
    doc.blank()
    doc.add('*Row totals in £b/yr:*')
    doc.blank()
    row_b_rows = []
    for i, diff in enumerate(diffs):
        row_b = sum(r['post_fill_revenue_m'] for r in py_tcm[diff]) / 1000
        row_b_rows.append([f'{tweights[i]:.0%} ({p["tiers"][i]["label"]})',
                            f'£{row_b:,.2f}b'])
    total_pf_rev = sum(
        sum(r['post_fill_revenue_m'] for r in py_tcm[t['differential']]) / 1000
        for t in p['tiers']
    )
    row_b_rows.append(['**Grand total**', f'**£{total_pf_rev:,.2f}b**'])
    doc.table(['Tier (weight)', '£b/yr'], row_b_rows, col_fmt=[LEFT, RIGHT])
    doc.blank()

    # B.3.8 — Cohort proportion
    doc.h3('B.3.8 Cohort proportion of total tax paid (%)')
    doc.note(
        "Each cell's capitalisation-window revenue as a percentage of the grand total. "
        "Row total is the tier's share; column total is the bracket's share across all tiers."
    )
    col_prop_totals = [0.0] * len(blabels)
    prop_rows = []
    for i, diff in enumerate(diffs):
        rev_vals      = [r['post_fill_revenue_m'] for r in py_tcm[diff]]
        cell_pcts     = [(v / grand_total * 100) if grand_total > 0 else 0.0
                         for v in rev_vals]
        row_pct_total = sum(cell_pcts)
        for j, pct in enumerate(cell_pcts):
            col_prop_totals[j] += pct
        prop_rows.append(
            [f'{tweights[i]:.0%} ({p["tiers"][i]["label"]})']
            + [f'{v:.1f}%' for v in cell_pcts]
            + [f'**{row_pct_total:.1f}%**']
        )
    prop_rows.append(
        ['**Column total**']
        + [f'**{v:.1f}%**' for v in col_prop_totals]
        + ['**100.0%**']
    )
    doc.table(
        ['Tier (weight) \\ Bracket'] + blabels + ['**Row total**'],
        prop_rows,
        col_fmt=[LEFT] + [RIGHT] * len(blabels) + [RIGHT],
    )
    doc.blank()

    # B.3.9 — Revenue by tier
    doc.h3('B.3.9 Revenue by tier (£b/yr)')
    doc.blank()
    total_rev = 0.0
    rev_rows  = []
    for i, diff in enumerate(diffs):
        subtotal    = sum(r['revenue_m']           for r in py_tcm[diff]) / 1000
        pf_subtotal = sum(r['post_fill_revenue_m'] for r in py_tcm[diff]) / 1000
        total_rev  += subtotal
        rev_rows.append([tlabels[i], f'£{subtotal:,.1f}b', f'£{pf_subtotal:,.1f}b'])
    rev_rows.append(['**Total**', f'**£{total_rev:,.1f}b**',
                     f'**£{total_pf_rev:,.2f}b**'])
    doc.table(
        ['Tier', 'Lifetime avg (£b/yr)', 'Capitalisation window avg (£b/yr)'],
        rev_rows,
        col_fmt=[LEFT, RIGHT, RIGHT],
    )
    doc.blank()

    if py_lrr_fill:
        doc.add('*TCM horizon N is derived from the SSM LRR breakeven year, '
                'not the TOML snapshot_N.*')
        doc.blank()
        doc.add('**TCM Step-5 coverage fraction by window:**')
        doc.blank()
        tcm_lrr_fail = (tcm_win.get('tcm_lrr_failure_year', '—') if tcm_win else '—')
        tcm_srr_fail = (tcm_win.get('tcm_srr_failure_year', '—') if tcm_win else '—')
        tcm_cov_rows = []
        for W in COVERAGE_WINDOWS:
            cov   = tcm_win.get(f'tcm_cov_{W}') if tcm_win else None
            tcm_cov_rows.append([
                f'{W} years',
                f'{cov:.1%}' if cov is not None else '—',
                str(tcm_lrr_fail),
                str(tcm_srr_fail),
            ])
        doc.table(
            ['Window', 'TCM coverage',
             'TCM failure year (LRR)', 'TCM failure year (SRR)'],
            tcm_cov_rows,
            col_fmt=[LEFT, RIGHT, RIGHT, RIGHT],
        )
        doc.note(
            'TCM applies heterogeneous tier differentials to the actual historical return '
            'series, producing higher revenue than the SSM uniform-return assumption. The SSM '
            'forms the solvency/stress-test floor; the TCM ceiling bounds the plausible range. '
            'TCM and SSM run independent SRR/LRR balance trackers.'
        )


def _b4_sweep(doc, p, sweep_extremals):
    doc.h2('B.4 Start-Year Sweep')
    doc.blank()
    doc.add(f'All figures at $\\tau_0$={p["tau_0"]:.0%}, '
            f'$\\tau_m$={p["tau_m"]:.0%}, '
            f'k={p["k"]}, $W_{{\\min}}$=£{p["W_min"]}m.')
    doc.blank()

    if not sweep_extremals:
        return

    # B.4.1 — Extremals
    doc.h3('B.4.1 Extremals — four dimensions')
    doc.blank()

    def _efmt(r):
        if r is None:
            return ['—'] * 6
        lf   = str(r.get('lrr_failure_year')) if r.get('lrr_failure_year') else 'none'
        sf   = str(r.get('srr_failure_year')) if r.get('srr_failure_year') else 'none'
        c50  = f'{r["ssm_cov_50"]:.1%}' if r.get('ssm_cov_50') is not None else '—'
        surp = (f'£{r["lrr_surplus_at_fill"]:,.0f}b'
                if r.get('lrr_fill_year') is not None else '—')
        return [str(r['calendar_year']), str(r.get('lrr_fill_year', '—')),
                surp, lf, sf, c50]

    ext_pairs = [
        ('Speed — slowest LRR fill',          sweep_extremals.get('worst_speed')),
        ('Speed — fastest LRR fill',          sweep_extremals.get('best_speed')),
        ('Margin — thinnest surplus',         sweep_extremals.get('worst_margin')),
        ('Margin — largest surplus',          sweep_extremals.get('best_margin')),
        ('Durability — lowest 50yr SSMcov',   sweep_extremals.get('worst_durable')),
        ('Durability — highest 50yr SSMcov',  sweep_extremals.get('best_durable')),
        ('Resilience — earliest LRR failure', sweep_extremals.get('worst_resilient')),
        ('Resilience — latest/no LRR failure',sweep_extremals.get('best_resilient')),
    ]
    doc.table(
        ['Dimension', 'Start year', 'LRR breakeven',
         'LRR surplus (£b)', 'LRR failure year', 'SRR failure year', 'SSM cov 50yr'],
        [[dim] + _efmt(r) for dim, r in ext_pairs],
        col_fmt=[LEFT, CENTER, CENTER, RIGHT, CENTER, CENTER, RIGHT],
    )
    doc.blank()

    nofail = sum(1 for r in sweep_extremals.get('all', [])
                 if r.get('lrr_failure_year') is None
                 and r.get('lrr_fill_year') is not None)
    if nofail:
        doc.add(f'*{nofail} start years produce no LRR failure within the '
                '71-year modelling window.*')
        doc.blank()

    # B.4.2 — Full sweep table
    all_rows       = sweep_extremals.get('all', [])
    scenario_start = p.get('scenario_start_year')

    doc.h3(f'B.4.2 Full sweep table (all {len(all_rows)} calendar years)')
    doc.blank()

    def _c(v):  return str(v)   if v is not None else '—'
    def _p(v):  return f'{v:.1%}' if v is not None else '—'

    sweep_data = []
    for r in all_rows:
        yr   = r['calendar_year']
        bold = scenario_start and yr == scenario_start
        b    = '**' if bold else ''
        lrr_s = (f'{r["lrr_surplus_at_fill"]:,.0f}'
                 if r.get('lrr_fill_year') is not None else '—')
        sweep_data.append([
            f'{b}{yr}{b}',
            f'{b}{_c(r.get("srr_fill_year"))}{b}',
            f'{b}{_c(r.get("lrr_fill_year"))}{b}',
            f'{b}{lrr_s}{b}',
            f'{b}{_c(r.get("lrr_failure_year"))}{b}',
            f'{b}{_c(r.get("srr_failure_year"))}{b}',
            f'{b}{_c(r.get("lrr_srr_failure_gap"))}{b}',
            f'{b}{_p(r.get("ssm_cov_5"))}{b}',
            f'{b}{_p(r.get("ssm_cov_10"))}{b}',
            f'{b}{_p(r.get("ssm_cov_20"))}{b}',
            f'{b}{_p(r.get("ssm_cov_50"))}{b}',
            f'{b}{_p(r.get("tcm_cov_10"))}{b}',
            f'{b}{_p(r.get("tcm_cov_50"))}{b}',
        ])
    doc.table(
        ['Start', 'SRR fill', 'LRR fill', 'LRR surplus (£b)',
         'LRR failure', 'SRR failure', 'gap',
         'SSMcov5', 'SSMcov10', 'SSMcov20', 'SSMcov50',
         'TCMcov10', 'TCMcov50'],
        sweep_data,
        col_fmt=[CENTER, CENTER, CENTER, RIGHT,
                 CENTER, CENTER, CENTER,
                 RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT],
    )
    doc.note(
        'Active scenario shown in bold. Coverage fractions = Step-5 remainder / annual '
        'expenditure, averaged over each window. Zero in failure years drags the average. '
        'LRR failure: buffer exhausted (lrr_bal = 0). SRR failure: refund guarantee broken '
        '(srr_bal = 0). Gap: years between LRR and SRR failure. SSM = correlated-shock '
        'floor; TCM = heterogeneous-tier ceiling.'
    )


def _b5_stats(doc, stats):
    doc.h2('B.5 Statistical Pass — P(success) Across Economic Cycles')
    doc.blank()
    doc.add('**Success definition (v8):** LRR fills within the 71-year window AND '
            'LRR never fails (lrr_failure_year is None).')
    doc.blank()

    if not stats:
        return

    ov = stats['overall']

    doc.h3(f'B.5.1 Overall (all {ov["n_total"]} start years)')
    doc.blank()
    doc.table(
        ['Metric', 'Value'],
        [
            ['Success rate',   f'{ov["success_rate"]:.1f}% '
                               f'({ov["n_success"]}/{ov["n_total"]})'],
            ['LRR fills',      f'{ov["lrr_fill_rate"]:.1f}% '
                               f'({ov["n_lrr_fills"]}/{ov["n_total"]})'],
            ['LRR failures',   f'{ov["lrr_failure_rate"]:.1f}% '
                               f'({ov["n_lrr_failure"]}/{ov["n_total"]})'],
            ['SRR failures',   f'{ov["srr_failure_rate"]:.1f}% '
                               f'({ov["n_srr_failure"]}/{ov["n_total"]})'],
        ],
        col_fmt=[LEFT, LEFT],
    )
    doc.blank()

    doc.h3('B.5.2 By economic cycle')
    doc.blank()
    doc.table(
        ['Period', 'N', 'Success%', 'LRR fill%'],
        [[b['label'], str(b['n']),
          f'{b["success_rate"]:.1f}%', f'{b["lrr_fill_rate"]:.1f}%']
         for b in stats['by_bucket']],
        col_fmt=[LEFT, CENTER, CENTER, CENTER],
    )
    doc.blank()

    doc.h3('B.5.3 Key metric distributions')
    doc.blank()

    def _fv2(v, fmt):
        return fmt(v) if v is not None else '—'

    fi = lambda v: f'{v:,.0f}'
    fp = lambda v: f'{v:.1%}'

    dist_headers = ['Metric', 'N', 'Min', 'Median', 'Mean', 'Max']
    dist_rows = []

    for key, label in [
        ('lrr_fill_year',        'LRR breakeven year'),
        ('srr_fill_year',        'SRR fill year'),
        ('lrr_failure_year',     'LRR failure year'),
        ('srr_failure_year',     'SRR failure year'),
        ('lrr_srr_failure_gap',  'LRR→SRR failure gap (yrs)'),
        ('lrr_surplus_at_fill',  'LRR surplus at breakeven (£b)'),
    ]:
        d = stats['distributions'].get(key, {})
        dist_rows.append([
            label, str(d.get('n', 0)),
            _fv2(d.get('min'),    fi), _fv2(d.get('median'), fi),
            _fv2(d.get('mean'),   fi), _fv2(d.get('max'),    fi),
        ])

    for W in COVERAGE_WINDOWS:
        for prefix, label_pfx in [('ssm', 'SSM'), ('tcm', 'TCM')]:
            d = stats['distributions'].get(f'{prefix}_cov_{W}', {})
            dist_rows.append([
                f'{label_pfx} coverage {W}yr avg', str(d.get('n', 0)),
                _fv2(d.get('min'),    fp), _fv2(d.get('median'), fp),
                _fv2(d.get('mean'),   fp), _fv2(d.get('max'),    fp),
            ])

    doc.table(
        dist_headers, dist_rows,
        col_fmt=[LEFT, CENTER, RIGHT, RIGHT, RIGHT, RIGHT],
    )
    doc.note(
        'Coverage fractions: Step-5 remainder / annual expenditure, '
        'averaged over each window length. Zero in any failure year. '
        'SSM = correlated-shock floor; TCM = heterogeneous-tier ceiling.'
    )


# ─────────────────────────────────────────────────────────────
# SHARED HELPER
# ─────────────────────────────────────────────────────────────

def _tier_bracket_table(doc, diffs, tlabels, blabels, field, py_tcm, fmt):
    """Emit a standard tier × bracket grid using MdDoc.table()."""
    rows = []
    for label, diff in zip(tlabels, diffs):
        vals = [r[field] for r in py_tcm[diff]]
        rows.append([label] + [fmt(v) for v in vals])
    doc.table(
        ['Tier \\ Bracket'] + blabels,
        rows,
        col_fmt=[LEFT] + [RIGHT] * len(blabels),
    )
    doc.blank()


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    toml_path  = sys.argv[1] if len(sys.argv) > 1 else None
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f'Loading parameters from: {toml_path or DEFAULT_PARAMS}')
    p = model.load_params(toml_path)
    model.validate_params(p)

    meta = p.get('meta', {})
    print()
    print('─' * 60)
    print('PARAMETERS')
    print('─' * 60)
    print(f"  scenario:   {meta.get('scenario_label', '—')}")
    print(f"  start year: {p['scenario_start_year']}")
    print(f"  tau_0={p['tau_0']:.0%}  tau_m={p['tau_m']:.0%}  "
          f"k={p['k']}  W_min=£{p['W_min']}m")
    print(f"  SRR={p['srr_ratio']}×  LRR={p['lrr_years']} yrs")

    print('\nRunning SSM (active scenario, N=1..71)...')
    py_ssm = model.run_ssm(p, max_N=71)

    py_lrr_fill = next((r for r in py_ssm if r.get('lrr_filled')), None)
    py_srr_fill = next((r for r in py_ssm
                        if r['srr_target'] > 0
                        and r['srr_balance'] >= r['srr_target'] * 0.9999), None)
    ssm_lrr_N = py_lrr_fill['year'] if py_lrr_fill else p['tcm_N']
    ssm_srr_N = py_srr_fill['year'] if py_srr_fill else 1

    print(f"  SRR fill year: {py_srr_fill['year'] if py_srr_fill else '—'}")
    print(f"  LRR fill year: {ssm_lrr_N}  (used as TCM N)")

    print(f'\nRunning TCM (N={ssm_lrr_N})...')
    py_tcm = model.run_tcm(p, N=ssm_lrr_N, N_fill=ssm_srr_N)

    print('  Computing TCM coverage windows...')
    tcm_win = _tcm_coverage_windows(p, ssm_lrr_N, ssm_srr_N) if py_lrr_fill else None

    print(f'\nRunning start-year sweep ({len(p["returns"])} calendar years)...')
    sweep           = model.run_start_year_sweep(p)
    sweep_extremals = model.report_start_year_sweep(sweep, p)

    print('\nRunning extremal scenario profiles...')
    profiles = model.run_scenario_profiles(sweep_extremals, p)
    model.report_scenario_profiles(profiles, p)

    print('\nRunning statistical pass...')
    stats = model.compute_statistics(sweep)
    model.report_statistics(stats, p)

    print('\nWriting markdown report...')
    _out     = ensure_dir(Path(output_dir) if output_dir else _OUT)
    out_path = write_report(p, py_ssm, py_tcm, ssm_lrr_N,
                            sweep_extremals, stats,
                            tcm_win=tcm_win, output_dir=_out)
    print(f'  Written: {out_path}')
    print('\nDone.')


if __name__ == '__main__':
    main()
