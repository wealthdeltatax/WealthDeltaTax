"""
WDT Rate Parameter Sensitivity Sweep — Markdown Tables
========================================================
Runs each of the four rate-function parameters independently,
holding the other three at Balanced baseline values, and produces a
dated Markdown report (RATES_S_Appendix_Tables.md).

Shared infrastructure (path resolution, statistical helpers, sweep
runner, formatting) comes from rates_s_helpers.py.

PARAMETERS SWEPT
  τ_0, τ_m, k, W_min, srr_ratio, lrr_years  (from TOML sweep section)

USAGE
  python3 16_6_260813_RATES_S_tables.py [params.toml] [output_dir]
"""

import sys
import datetime
from pathlib import Path
from rates_s_helpers import (
    model, DEFAULT_PARAMS, OUT_DIR_TABLES,
    run_param_sweep, fmt_pct, fmt_f, baseline_marker, dist_row,
    median, mean, success, summarise,
)

OUTPUT_DIR = OUT_DIR_TABLES

# ── Sweep grids and baseline — populated from TOML in main() ─────────────────
BASELINE        = {}
SWEEP_TAU_0     = []
SWEEP_TAU_M     = []
SWEEP_K         = []
SWEEP_WMIN      = []
SWEEP_SRR_RATIO = []
SWEEP_LRR_YEARS = []

# Aliases matching original private-name style used in write_report body
_fmt_pct        = fmt_pct
_fmt_f          = fmt_f
_baseline_marker = baseline_marker
_dist_row       = dist_row



# ── Markdown report builder ───────────────────────────────────────────────────
def _md_param_section(sweep_results, param_label, baseline_v, baseline_name,
                      value_fmt, other_params_str):
    """
    Build the Markdown for one parameter's sweep section.

    Returns a list of lines.
    """
    lines = []
    A = lines.append

    A(f'### {param_label}')
    A('')
    A(f'Other parameters held at Balanced baseline: {other_params_str}.')
    A('')

    # ── summary table ─────────────────────────────────────────
    # Columns: value | success% | SSM cov min/med/mean/max | TCM cov min/med/mean/max
    #          | LRR fill min/med | SRR fill med | LRR surplus min/med
    A('**Sweep summary — distributions across 73 historical start years**')
    A('')
    A('| Value | Success% | SSM cov (min/med/mean/max) | TCM cov (min/med/mean/max) | '
      'LRR fill yr (min/med/mean/max) | SRR fill yr (med) | LRR surplus £b (min/med) |')
    A('|:---:|:---:|:---:|:---:|:---:|:---:|:---:|')

    for r in sweep_results:
        v = r['value']
        mark = _baseline_marker(v, baseline_v)

        if r['skipped']:
            A(f'| {value_fmt(v)}{mark} | — (skipped: {r["skip_reason"]}) | — | — | — | — | — |')
            continue

        s = r['summary']
        A(f'| {value_fmt(v)}{mark} '
          f'| {s["success_rate"]:.0f}% '
          f'| {_dist_row(s["ssm_cov"], _fmt_pct)} '
          f'| {_dist_row(s["tcm_cov"], _fmt_pct)} '
          f'| {_dist_row(s["lrr_fill"], lambda v: _fmt_f(v, ".0f"))} '
          f'| {_fmt_f(s["srr_fill"]["median"], ".0f")} '
          f'| {_fmt_f(s["lrr_surplus"]["min"], ".0f")} / {_fmt_f(s["lrr_surplus"]["median"], ".0f")} |')

    A('')
    A('*◄ = Balanced baseline value. '
      'Coverage ratios: capitalisation-window averages (SRR fill to LRR fill). '
      'Distributions across all 73 historical start years 1947–2019.*')
    A('')

    # ── worst-case 2006 table ─────────────────────────────────
    A('**2006 start year (worst-case historical scenario)**')
    A('')
    A('| Value | SSM cov | TCM cov | LRR fill yr | LRR surplus £b | SRR breach covered |')
    A('|:---:|:---:|:---:|:---:|:---:|:---:|')

    for r in sweep_results:
        v = r['value']
        mark = _baseline_marker(v, baseline_v)

        if r['skipped']:
            A(f'| {value_fmt(v)}{mark} | — | — | — | — | — |')
            continue

        wc = r['summary']['worst_case_2006']
        if wc is None:
            A(f'| {value_fmt(v)}{mark} | — | — | — | — | — |')
            continue

        ssm = _fmt_pct(wc.get('ssm_post_fill_coverage'))
        tcm = _fmt_pct(wc.get('tcm_post_fill_coverage'))
        lrr = _fmt_f(wc.get('lrr_fill_year'), '.0f')
        sur = _fmt_f(wc.get('lrr_surplus_at_fill'), '.0f')
        cov_raw = wc.get('srr_breach_covered')
        cov = ('YES' if cov_raw is True
               else ('NO' if cov_raw is False else '— (no breach)'))

        A(f'| {value_fmt(v)}{mark} | {ssm} | {tcm} | {lrr} | {sur} | {cov} |')

    A('')

    return lines


def write_report(sweep_tau_0, sweep_tau_m, sweep_k, sweep_wmin,
                 sweep_srr_ratio, sweep_lrr_years,
                 p_base, output_dir):
    """Assemble and write the full Markdown report."""
    run_date = datetime.date.today().strftime('%y%m%d')
    fname    = f'RATES_S_Appendix_Tables.md'
    out_path = Path(output_dir) / fname

    lines = []
    A = lines.append

    # ── Header ────────────────────────────────────────────────
    A('# B. WDT Rate Parameter Sensitivity Sweep')
    A('')
    A(f'**Run date:** {datetime.date.today().isoformat()}  ')
    A(f'**Model version:** v6 (rates_model.py / wdt_core.py)  ')
    A(f'**Parameters file:** `{DEFAULT_PARAMS.name}`  ')
    A('')
    A('## B.1. Purpose')
    A('')
    A('This document sweeps each of the four WDT rate-function parameters independently, '
      'holding the other three at Balanced baseline values, and reports how key transition '
      'metrics vary across the full 73-year historical start-year sweep (1947–2019 UK equity '
      'return series). It is intended as orientation material for future Governing Council '
      'calibration work, not as a scenario recommendation. Parameter interactions are not '
      'modelled here; joint sweeps are a natural second-order extension.')
    A('')

    # ── Rate function ─────────────────────────────────────────
    A('### B.1.1 The Rate Function')
    A('')
    A(r'The WDT logistic marginal rate function is:')
    A('')
    A(r'$$\tau(W) = \frac{\tau_m}{1 + \left(\frac{\tau_m - \tau_0}{\tau_0}\right)'
      r'e^{-k(W - W_{\min})}}, \quad \tau(W) = 0 \text{ if } W < W_{\min}$$')
    A('')
    A('Note: the docstring in `rates_model.py` contains a typographical error writing '
      r'$(1-\tau_0)/\tau_0$ as the denominator coefficient. The implementation in '
      '`wdt_core.tau()` correctly uses $(\\tau_m - \\tau_0)/\\tau_0$. All results here '
      'use the correct formula.')
    A('')

    # ── Balanced baseline ─────────────────────────────────────
    A('### B.1.2 Balanced Baseline Parameters')
    A('')
    A('| Parameter | Baseline value | Role |')
    A('|---|---|---|')
    A(f'| $\\tau_0$ (floor rate) | {BASELINE["tau_0"]:.0%} | '
      'Marginal rate at W = W_min; determines tax on the smallest deltas |')
    A(f'| $\\tau_m$ (ceiling rate) | {BASELINE["tau_m"]:.0%} | '
      'Asymptotic ceiling; determines the maximum rate as W → ∞ |')
    A(f'| k (steepness, per £m) | {BASELINE["k"]} | '
      'Controls how rapidly the rate climbs through the wealth distribution |')
    A(f'| W_min (£m) | £{BASELINE["W_min"]}m | '
      'Entry point; below this the rate is zero regardless of δ |')
    A('')
    A('**SWF sizing parameters (Balanced baseline; swept in §§5–6):**')
    A('')
    A('| Parameter | Baseline value | Role |')
    A('|---|---|---|')
    A(f'| SRR capitalisation ratio | {p_base["srr_ratio"]}× | '
      'SRR target = ratio × (cumulative net income / N); sets how long before the refund guarantee is credible |')
    A(f'| LRR floor | {p_base["lrr_years"]} years of expenditure | '
      'LRR target = lrr_years × prevailing government expenditure; sets the Phase Two viability threshold |')
    A('')
    A('**Non-SWF parameters (held constant throughout all sweeps):**')
    A('')
    A('| Parameter | Value |')
    A('|---|---|')
    A(f'| Budget base (£b) | £{p_base["budget_base"]:,.1f}b |')
    A(f'| Budget growth (p.a.) | {p_base["budget_growth"]:.2%} |')
    A(f'| Historical mean return | {p_base["hist_mean"]:.2%} |')
    A(f'| Wealth brackets | {len(p_base["brackets"])} |')
    A(f'| Growth tiers | {len(p_base["tiers"])} |')
    A('')

    # ── Metrics glossary ──────────────────────────────────────
    A('### B.1.3 Metrics')
    A('')
    A('**Success:** LRR fills within the 71-year modelling window AND '
      '(SRR never breaches OR SRR breach is fully covered by LRR balance at time of breach).')
    A('')
    A('**SSM coverage ratio:** Average annual net SSM income over the capitalisation '
      'window (SRR fill to LRR fill) divided by average annual government expenditure '
      'over the same window. Applies the correlated-shock assumption (all taxpayers '
      'experience the same return simultaneously) — the worst-case floor.')
    A('')
    A('**TCM coverage ratio:** Average annual TCM revenue over the same capitalisation '
      'window divided by average annual government expenditure. Applies four persistent '
      'heterogeneous growth tier differentials — the persistent-heterogeneity ceiling. '
      'Together the SSM and TCM ratios bracket the plausible revenue range.')
    A('')
    A('**LRR fill year:** First year the LRR balance reaches the 3× expenditure floor. '
      'The primary transition-speed metric; gates full Phase Two fiscal replacement.')
    A('')
    A('**SRR fill year:** First year the SRR reaches its capitalisation target. '
      'Should be invariant at ~3 across most calibrations.')
    A('')
    A('**LRR surplus at fill:** LRR balance minus LRR target at the fill year, in £b. '
      'Safety margin above the floor at the breakeven point.')
    A('')
    A('*All distributions are across the 73 historical start years 1947–2019. '
      'The 2006 start year is extracted separately as the worst-case historical scenario '
      '(longest LRR fill time at Balanced parameters).*')
    A('')

    # ── Sweep sections ────────────────────────────────────────
    A('## B.2. Floor Rate (τ_0)')
    A('')
    A('τ_0 sets the marginal rate at W = W_min. A higher floor raises effective rates '
      'across the entire taxable population (since every taxpayer above W_min pays at '
      'least τ_0 on their first pound of delta); a lower floor concentrates the rate '
      'gradient in the upper distribution.')
    A('')
    lines += _md_param_section(
        sweep_tau_0, 'τ_0 sweep', BASELINE['tau_0'], 'tau_0',
        lambda v: f'{v:.0%}',
        f'τ_m = {BASELINE["tau_m"]:.0%},  k = {BASELINE["k"]},  W_min = £{BASELINE["W_min"]}m',
    )

    A('## B.3. Ceiling Rate (τ_m)')
    A('')
    A('τ_m is the asymptotic ceiling the marginal rate approaches but never reaches. '
      'Its primary effect is on the top brackets where W >> W_min; the logistic function '
      'brings effective rates close to τ_m only at very high declared wealth levels. '
      'Raising τ_m increases revenue from the highest-wealth, highest-growth cells '
      'disproportionately, since those cells also generate the largest absolute deltas.')
    A('')
    lines += _md_param_section(
        sweep_tau_m, 'τ_m sweep', BASELINE['tau_m'], 'tau_m',
        lambda v: f'{v:.0%}',
        f'τ_0 = {BASELINE["tau_0"]:.0%},  k = {BASELINE["k"]},  W_min = £{BASELINE["W_min"]}m',
    )

    A('## B.4. Steepness (k)')
    A('')
    A('k (per £m) controls how rapidly the marginal rate climbs from τ_0 toward τ_m '
      'through the wealth distribution. Low k produces a shallow gradient — most taxpayers '
      'face rates close to τ_0 even at high wealth levels, with τ_m approached only at very '
      'large holdings. High k produces a steep step — the rate reaches τ_m quickly above '
      'W_min, compressing the gradient into a narrow wealth band.')
    A('')
    A(f'*Sweep is log-spaced: {", ".join(f"{v:.4f}" for v in SWEEP_K)}*')
    A('')
    lines += _md_param_section(
        sweep_k, 'k sweep (log-spaced)', BASELINE['k'], 'k',
        lambda v: f'{v:.4f}',
        f'τ_0 = {BASELINE["tau_0"]:.0%},  τ_m = {BASELINE["tau_m"]:.0%},  '
        f'W_min = £{BASELINE["W_min"]}m',
    )

    A('## B.5. Entry Point (W_min)')
    A('')
    A('W_min (£m) is the wealth level below which the rate function produces zero liability. '
      'It is a rate design parameter, not a population boundary — all UK adults are within '
      'the taxable population regardless of W_min. Lower W_min pulls more of the 50th–80th '
      'percentile brackets into material liability; higher W_min concentrates the tax on '
      'the top percentiles. W_min also affects refund exposure in loss years, since a '
      'taxpayer below W_min receives no refund even if their delta is negative.')
    A('')
    lines += _md_param_section(
        sweep_wmin, 'W_min sweep', BASELINE['W_min'], 'W_min',
        lambda v: f'£{v}m',
        f'τ_0 = {BASELINE["tau_0"]:.0%},  τ_m = {BASELINE["tau_m"]:.0%},  '
        f'k = {BASELINE["k"]}',
    )

    A('## B.6. SRR Capitalisation Ratio (srr_ratio)')
    A('')
    A('srr_ratio sets the SRR capitalisation target as a multiple of average annual net '
      'WDT income. A higher ratio means the SRR must accumulate more before it is '
      'considered fully capitalised, which delays SRR fill and thereby reduces the flow '
      'into the LRR during the early accumulation period. A lower ratio allows faster '
      'SRR fill and faster LRR accumulation, but at the cost of a thinner refund buffer. '
      'The Governing Council recommended floor is 3×; the working SSM-derived value '
      'is 3×.')
    A('')
    A('*Note: srr_ratio does not affect the rate function or individual taxpayer burden — '
      'it affects only the milestone timing (SRR fill year and LRR fill year). '
      'The burden distribution panel in the chart companion is flat across this sweep.*')
    A('')
    lines += _md_param_section(
        sweep_srr_ratio, 'srr_ratio sweep', BASELINE['srr_ratio'], 'srr_ratio',
        lambda v: f'{v:.1f}×',
        f'τ_0 = {BASELINE["tau_0"]:.0%},  τ_m = {BASELINE["tau_m"]:.0%},  '
        f'k = {BASELINE["k"]},  W_min = £{BASELINE["W_min"]}m,  '
        f'lrr_years = {BASELINE["lrr_years"]}',
    )

    A('## B.7. LRR Floor (lrr_years)')
    A('')
    A('lrr_years sets the LRR floor as a multiple of prevailing government expenditure. '
      'The LRR target therefore grows over time as nominal expenditure grows at '
      f'{p_base["budget_growth"]:.2%} p.a. A higher floor requires the LRR to accumulate '
      'more before Phase Two becomes viable, directly extending the LRR fill year. '
      'A lower floor brings LRR fill earlier but with a thinner buffer against sustained '
      'drawdown post-fill. The recommended minimum is 3 years.')
    A('')
    A('*Note: lrr_years does not affect the rate function or individual taxpayer burden — '
      'it affects only the LRR milestone timing and the safety margin above the floor. '
      'The burden distribution panel in the chart companion is flat across this sweep.*')
    A('')
    lines += _md_param_section(
        sweep_lrr_years, 'lrr_years sweep', BASELINE['lrr_years'], 'lrr_years',
        lambda v: f'{v:.1f} yrs',
        f'τ_0 = {BASELINE["tau_0"]:.0%},  τ_m = {BASELINE["tau_m"]:.0%},  '
        f'k = {BASELINE["k"]},  W_min = £{BASELINE["W_min"]}m,  '
        f'srr_ratio = {BASELINE["srr_ratio"]}×',
    )

    # ── Reading notes ─────────────────────────────────────────
    A('# C. Reading Notes')
    A('')
    A('**Coverage ratio direction.** SSM and TCM coverage ratios move together when a '
      'parameter raises or lowers the rate on the bulk of the distribution. The gap between '
      'them (TCM − SSM) measures the sensitivity of revenue to persistent growth '
      'heterogeneity; a wide gap means higher-tier taxpayers contribute disproportionately '
      'more than the correlated-shock assumption would imply.')
    A('')
    A('**Success rate at 100%.** The Balanced baseline achieves 100% success across all '
      '73 start years. Parameters that reduce revenue significantly may bring the success '
      'rate below 100%, meaning the LRR fails to fill within the 71-year window for some '
      'historical starting conditions. This is the primary solvency constraint.')
    A('')
    A('**SRR fill year.** Should remain ~3 across most calibrations. If it rises '
      'significantly, the refund guarantee becomes credible only after more than one '
      'political cycle, which is a materially different political position.')
    A('')
    A('**LRR surplus.** A near-zero surplus at fill (see e.g. the 1953 start year at '
      'Balanced parameters, £28b surplus) indicates the mechanism passed its solvency test '
      'narrowly. A calibration that systematically reduces surplus increases the risk that '
      'a slightly worse return sequence would cause LRR non-fill.')
    A('')
    A('**Pre-behavioural baseline.** All figures are pre-behavioural. Behavioural '
      'responses — migration, restructuring, avoidance — are not modelled and will '
      'reduce actual revenue by an unknown amount. See RATES §9.1 and BEHAV.')
    A('')
    A('**Joint calibration.** These sweeps vary one parameter at a time. In practice, '
      'τ_0 and τ_m jointly determine both the level and shape of revenue; W_min and k '
      'jointly determine where in the wealth distribution the gradient falls. A second-order '
      'analysis (e.g. a τ_0 × τ_m grid, or a k × W_min grid) would capture interaction '
      'effects but is outside this document.')
    A('')
    A('**SRR and LRR interaction.** The SRR and LRR sizing parameters interact: a higher '
      'srr_ratio diverts more net income into SRR accumulation before any surplus flows to '
      'the LRR, so rising srr_ratio extends the LRR fill year even when lrr_years is held '
      'constant. Conversely, a lower srr_ratio accelerates LRR accumulation but leaves a '
      'thinner refund buffer. The single-parameter-at-a-time sweeps in §§5–6 capture the '
      'first-order effect of each; a joint srr_ratio × lrr_years grid would expose the '
      'interaction surface and is a natural second-order extension.')
    A('')
    A('**Rate parameters vs. SWF sizing parameters.** The sweeps in §§1–4 vary the rate '
      'function and therefore affect both revenue generation and individual taxpayer burden. '
      'The sweeps in §§5–6 vary only the capitalisation thresholds for the SRR and LRR; '
      'they do not alter the rate function or any individual tax liability. The burden '
      'distribution is therefore invariant across §§5–6 — those panels are flat by design, '
      'not an artefact. The sole effect is on when the SWF milestones are reached.')
    A('')
    A('---')
    A('')
    A('*Generated by `rates_param_sweep.py`. '
      'Source: `rates_model.py` / `wdt_core.py` / `7_4_…_Params.toml`. '
      'No existing project files were modified.*')

    with open(out_path, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))

    return out_path


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    toml_path  = sys.argv[1] if len(sys.argv) > 1 else None
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    # Use our resolved DEFAULT_PARAMS if no path supplied on the command line
    effective_toml = toml_path or str(DEFAULT_PARAMS)
    print(f'Loading parameters from: {effective_toml}')
    p_base = model.load_params(effective_toml)
    model.validate_params(p_base)

    # Populate module-level BASELINE and sweep grids from TOML.
    global BASELINE, SWEEP_TAU_0, SWEEP_TAU_M, SWEEP_K, SWEEP_WMIN, \
           SWEEP_SRR_RATIO, SWEEP_LRR_YEARS
    sw = p_base['sweep']
    BASELINE = {
        'tau_0':     p_base['tau_0'],
        'tau_m':     p_base['tau_m'],
        'k':         p_base['k'],
        'W_min':     p_base['W_min'],
        'srr_ratio': p_base['srr_ratio'],
        'lrr_years': p_base['lrr_years'],
    }
    SWEEP_TAU_0     = sw['rates_tau_0_sweep']
    SWEEP_TAU_M     = sw['rates_tau_m_sweep']
    SWEEP_K         = sw['rates_k_sweep']
    SWEEP_WMIN      = sw['rates_wmin_sweep']
    SWEEP_SRR_RATIO = sw['rates_srr_ratio_sweep']
    SWEEP_LRR_YEARS = sw['rates_lrr_years_sweep']

    print()
    print(f'Balanced baseline (from TOML): τ_0={p_base["tau_0"]:.0%}  τ_m={p_base["tau_m"]:.0%}  '
          f'k={p_base["k"]}  W_min=£{p_base["W_min"]}m  '
          f'srr_ratio={p_base["srr_ratio"]}×  lrr_years={p_base["lrr_years"]}')
    print()

    out_dir = Path(output_dir) if output_dir else OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    # ── τ_0 sweep ─────────────────────────────────────────────
    print('=' * 60)
    print('SWEEP 1/4: τ_0 (floor rate)')
    print('=' * 60)
    results_tau_0 = run_param_sweep(p_base, 'tau_0', SWEEP_TAU_0, 'tau_0')

    # ── τ_m sweep ─────────────────────────────────────────────
    print()
    print('=' * 60)
    print('SWEEP 2/4: τ_m (ceiling rate)')
    print('=' * 60)
    results_tau_m = run_param_sweep(p_base, 'tau_m', SWEEP_TAU_M, 'tau_m')

    # ── k sweep ───────────────────────────────────────────────
    print()
    print('=' * 60)
    print('SWEEP 3/4: k (steepness, log-spaced)')
    print('=' * 60)
    results_k = run_param_sweep(p_base, 'k', SWEEP_K, 'k')

    # ── W_min sweep ───────────────────────────────────────────
    print()
    print('=' * 60)
    print('SWEEP 4/4: W_min (entry point, £m)')
    print('=' * 60)
    results_wmin = run_param_sweep(p_base, 'W_min', SWEEP_WMIN, 'W_min')

    # ── srr_ratio sweep ───────────────────────────────────────
    print()
    print('=' * 60)
    print('SWEEP 5/6: srr_ratio (SRR capitalisation ratio)')
    print('=' * 60)
    results_srr_ratio = run_param_sweep(p_base, 'srr_ratio', SWEEP_SRR_RATIO, 'srr_ratio')

    # ── lrr_years sweep ───────────────────────────────────────
    print()
    print('=' * 60)
    print('SWEEP 6/6: lrr_years (LRR floor, years of expenditure)')
    print('=' * 60)
    results_lrr_years = run_param_sweep(p_base, 'lrr_years', SWEEP_LRR_YEARS, 'lrr_years')

    # ── Write report ──────────────────────────────────────────
    print()
    print('Writing report...')
    out_path = write_report(
        results_tau_0, results_tau_m, results_k, results_wmin,
        results_srr_ratio, results_lrr_years,
        p_base, out_dir,
    )
    print(f'Report written: {out_path}')
    print()
    print('Done.')


if __name__ == '__main__':
    main()
