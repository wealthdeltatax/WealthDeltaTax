"""
WDT Rate Parameter Sensitivity Sweep — Markdown Tables
========================================================
Loads all sweep results from OUTPUTS/sweep_cache.json (produced by
16_0_compute.py) and writes RATES_S_Appendix_Tables.md.

No simulation is run here; this script is pure formatting.
"""

import json
import sys
from pathlib import Path

from wdt_core import load_params

from wdt_fmt import (fmt_pct1 as fmt_pct, fmt_f, baseline_marker,
                     dist_row, out_dir, ensure_dir, today_iso)
from wdt_md import MdDoc

from wdt_analytics import (
    init, HEADLINE_WINDOW,
    model, DEFAULT_PARAMS,
    run_g_sweep, run_synthetic_sweep,
)
import wdt_analytics as _A

import importlib, sys
_mod = importlib.import_module('8_3a_RATES_report')
write_report = _mod.write_report

_OUT   = out_dir('RATES_S')
_CACHE = out_dir('.').parent / 'OUTPUTS' / 'sweep_cache.json'


def _load():
    with open(_CACHE, encoding='utf-8') as fh:
        return json.load(fh)


# ── Per-parameter section builder ─────────────────────────────────────────────

def _param_section(doc, sweep_results, param_label, baseline_v,
                   value_fmt, other_params_str):
    """
    Append one parameter's sweep section to doc, using cached sweep_results.
    Produces two tables: distribution summary and worst-case 2006.
    """
    hw = HEADLINE_WINDOW

    doc.h3(f'### {param_label}').blank()
    doc.add(f'Other parameters held at Balanced baseline: {other_params_str}.').blank()

    # ── Summary table ────────────────────────────────────────────────────────
    doc.add('**Sweep summary — distributions across 73 historical start years**').blank()
    header = (f'| Value | Success% | SSMcov{hw} (min/med/mean/max) '
              f'| TCMcov{hw} (min/med/mean/max) '
              f'| SSMcov50 (min/med) | LRR fail n '
              f'| LRR fill yr (min/med/mean/max) | SRR fill yr (med) '
              f'| LRR surplus £b (min/med) |')
    sep    = '|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|'
    doc.add(header).add(sep)

    for r in sweep_results:
        v    = r['value']
        mark = baseline_marker(v, baseline_v)
        if r['skipped']:
            doc.add(f'| {value_fmt(v)}{mark} | — (skipped: {r["skip_reason"]}) '
                    '| — | — | — | — | — | — | — |')
            continue
        s      = r['summary']
        s50    = s['ssm_cov_50']
        n_fail = s['n_lrr_failure']
        doc.add(
            f'| {value_fmt(v)}{mark} '
            f'| {s["success_rate"]:.0f}% '
            f'| {dist_row(s["ssm_cov"], fmt_pct)} '
            f'| {dist_row(s["tcm_cov"], fmt_pct)} '
            f'| {fmt_f(s50["min"], ".1f")}% / {fmt_f(s50["median"], ".1f")}% '
            f'| {n_fail} '
            f'| {dist_row(s["lrr_fill"], lambda v: fmt_f(v, ".0f"))} '
            f'| {fmt_f(s["srr_fill"]["median"], ".0f")} '
            f'| {fmt_f(s["lrr_surplus"]["min"], ".0f")} / '
            f'{fmt_f(s["lrr_surplus"]["median"], ".0f")} |'
        )

    doc.blank().add(
        f'*◄ = Balanced baseline value. '
        f'SSMcov{hw}/TCMcov{hw}: Step-5 coverage fraction averaged over {hw} post-fill years. '
        f'SSMcov50: 50yr window showing long-run trajectory. '
        f'LRR fail n: start years where LRR buffer hits zero within 71-year window. '
        f'Distributions across all 73 historical start years 1947–2019.*'
    ).blank()

    # ── Worst-case 2006 table ────────────────────────────────────────────────
    doc.add('**2006 start year (worst-case historical scenario)**').blank()
    doc.add(f'| Value | SSMcov{hw} | TCMcov{hw} | LRR fill yr | LRR surplus £b | LRR failure yr |')
    doc.add('|:---:|:---:|:---:|:---:|:---:|:---:|')

    for r in sweep_results:
        v    = r['value']
        mark = baseline_marker(v, baseline_v)
        if r['skipped']:
            doc.add(f'| {value_fmt(v)}{mark} | — | — | — | — | — |')
            continue
        wc = r['summary']['worst_case_2006']
        if wc is None:
            doc.add(f'| {value_fmt(v)}{mark} | — | — | — | — | — |')
            continue
        ssm  = fmt_pct(wc.get(f'ssm_cov_{hw}'))
        tcm  = fmt_pct(wc.get(f'tcm_cov_{hw}'))
        lrr  = fmt_f(wc.get('lrr_fill_year'), '.0f')
        sur  = fmt_f(wc.get('lrr_surplus_at_fill'), '.0f')
        fail = (str(wc['lrr_failure_year']) if wc.get('lrr_failure_year') is not None
                else '— (no failure)')
        doc.add(f'| {value_fmt(v)}{mark} | {ssm} | {tcm} | {lrr} | {sur} | {fail} |')

    doc.blank()


# ── Report builder ────────────────────────────────────────────────────────────

def _single_scenario_table(doc, sweep_results, param_label, baseline_v,
                            value_fmt, note):
    """
    Table for deterministic (single-scenario) sweeps: g sweep and synthetic
    scenario sweeps.  Unlike _param_section, there is no start-year
    distribution — each row is one deterministic run, so the table shows
    point values rather than min/med/mean/max ranges.
    """
    hw = HEADLINE_WINDOW
    doc.add(f'**{param_label}**').blank()
    if note:
        doc.add(f'*{note}*').blank()

    doc.add(
        f'| Value | LRR fill yr | LRR surplus £b | SSMcov{hw} | TCMcov{hw} '
        f'| SSMcov50 | LRR failure yr |'
    )
    doc.add('|:---:|:---:|:---:|:---:|:---:|:---:|:---:|')

    for r in sweep_results:
        v    = r['value']
        mark = baseline_marker(v, baseline_v)
        if r['skipped']:
            doc.add(f'| {value_fmt(v)}{mark} | — | — | — | — | — | — |')
            continue
        s   = r['summary']
        raw = s.get('_raw', {})
        doc.add(
            f'| {value_fmt(v)}{mark} '
            f'| {fmt_f(raw.get("lrr_fill_year"), ".0f")} '
            f'| {fmt_f(raw.get("lrr_surplus_at_fill"), ".0f")} '
            f'| {fmt_pct(s["ssm_cov"]["median"])} '
            f'| {fmt_pct(s["tcm_cov"]["median"])} '
            f'| {fmt_pct(s["ssm_cov_50"]["median"])} '
            f'| {fmt_f(raw.get("lrr_failure_year"), ".0f") if raw.get("lrr_failure_year") else "— (none)"} |'
        )
    doc.blank()

def build_rates_s_doc(d, p_base): 
    hw   = HEADLINE_WINDOW
    bl   = p_base   # shorter alias
    sw   = d['rates_s']
    doc  = MdDoc()

    # ── Header ───────────────────────────────────────────────────────────────
    doc.h1('B. WDT Rate Parameter Sensitivity Sweep').blank()
    doc.add(f'**Run date:** {today_iso()}  ')
    doc.add(f'**Model version:** v8 (rates_model.py / wdt_core.py)  ')
    doc.add(f'**Headline coverage window:** {hw} years '
            f'(SSMcov{hw}/TCMcov{hw} columns; change HEADLINE_WINDOW in wdt_analytics.py)  ')
    doc.add(f'**Parameters file:** `{DEFAULT_PARAMS.name}`  ').blank()

    # ── Purpose ──────────────────────────────────────────────────────────────
    doc.h2('## B.1. Purpose').blank()
    doc.add(
        'This document sweeps each of the four WDT rate-function parameters independently, '
        'holding the other three at Balanced baseline values, and reports how key transition '
        'metrics vary across the full 73-year historical start-year sweep (1947–2019 UK equity '
        'return series). It is intended as orientation material for future Governing Council '
        'calibration work, not as a scenario recommendation. Parameter interactions are not '
        'modelled here; joint sweeps are a natural second-order extension.'
    ).blank()

    doc.h3('### B.1.1 The Rate Function').blank()
    doc.add(
        r'$$\tau(W) = \frac{\tau_m}{1 + \left(\frac{\tau_m - \tau_0}{\tau_0}\right)'
        r'e^{-k(W - W_{\min})}}, \quad \tau(W) = 0 \text{ if } W < W_{\min}$$'
    ).blank()
    doc.add(
        'Note: the docstring in `rates_model.py` contains a typographical error writing '
        r'$(1-\tau_0)/\tau_0$ as the denominator coefficient. The implementation in '
        '`wdt_core.tau()` correctly uses $(\\tau_m - \\tau_0)/\\tau_0$.'
    ).blank()

    doc.h3('### B.1.2 Balanced Baseline Parameters').blank()
    doc.add('| Parameter | Baseline value | Role |').add('|---|---|---|')
    doc.add(f'| $\\tau_0$ (floor rate) | {bl["tau_0"]:.0%} | Marginal rate at W = W_min |')
    doc.add(f'| $\\tau_m$ (ceiling rate) | {bl["tau_m"]:.0%} | Asymptotic ceiling |')
    doc.add(f'| k (steepness, per £m) | {bl["k"]} | Controls rate climb speed |')
    doc.add(f'| W_min (£m) | £{bl["W_min"]}m | Entry point; below this rate = 0 |').blank()
    doc.add('**SWF sizing parameters (Balanced baseline; swept in §§5–6):**').blank()
    doc.add('| Parameter | Baseline value | Role |').add('|---|---|---|')
    doc.add(f'| SRR capitalisation ratio | {bl["srr_ratio"]}× | SRR target sizing |')
    doc.add(f'| LRR floor | {bl["lrr_years"]} years of expenditure | Phase Two viability threshold |').blank()
    doc.add('**Non-SWF parameters (held constant throughout):**').blank()
    doc.add('| Parameter | Value |').add('|---|---|')
    doc.add(f'| Budget base (£b) | £{bl["budget_base"]:,.1f}b |')
    doc.add(f'| Budget growth (p.a.) | {bl["budget_growth"]:.2%} |')
    doc.add(f'| Historical mean return | {bl["hist_mean"]:.2%} |')
    doc.add(f'| Wealth brackets | {len(bl["brackets"])} |')
    doc.add(f'| Growth tiers | {len(bl["tiers"])} |').blank()

    doc.h3('### B.1.3 Metrics').blank()
    doc.add(
        f'**Success (v8):** LRR fills within the 71-year modelling window AND '
        'the LRR buffer never hits zero (lrr_failure_year is None).'
    ).blank()
    doc.add(
        f'**SSMcov{hw} / TCMcov{hw} (headline window):** '
        f'Average Step-5 coverage fraction over the first {hw} post-fill years. '
        'SSM applies uniform historical returns (worst-case floor); '
        'TCM applies heterogeneous tier differentials (ceiling). '
        f'The headline window is {hw} years; change HEADLINE_WINDOW in wdt_analytics.py '
        'to switch all tables and charts simultaneously.'
    ).blank()
    doc.add(
        '**SSMcov50:** Same metric averaged over 50 post-fill years. '
        'Rising values indicate WDT revenue compounds faster than expenditure.'
    ).blank()
    doc.add(
        '**LRR fail n:** Count of the 73 historical start years where the LRR balance '
        'reaches zero within the 71-year modelling window. At Balanced parameters this is 0.'
    ).blank()
    doc.add(
        '*All distributions are across the 73 historical start years 1947–2019. '
        'The 2006 start year is extracted separately as the worst-case historical scenario.*'
    ).blank()

    # ── Sweep sections ────────────────────────────────────────────────────────
    doc.h2('## B.2. Floor Rate (τ_0)').blank()
    doc.add(
        'τ_0 sets the marginal rate at W = W_min. A higher floor raises effective rates '
        'across the entire taxable population; a lower floor concentrates the rate gradient '
        'in the upper distribution.'
    ).blank()
    _param_section(doc, sw['rates_tau0_sweep'], 'τ_0 sweep', bl['tau_0'],
                   lambda v: f'{v:.0%}',
                   f'τ_m = {bl["tau_m"]:.0%},  k = {bl["k"]},  W_min = £{bl["W_min"]}m')

    doc.h2('## B.3. Ceiling Rate (τ_m)').blank()
    doc.add(
        'τ_m is the asymptotic ceiling the marginal rate approaches but never reaches. '
        'Its primary effect is on the top brackets where W >> W_min.'
    ).blank()
    _param_section(doc, sw['rates_taum_sweep'], 'τ_m sweep', bl['tau_m'],
                   lambda v: f'{v:.0%}',
                   f'τ_0 = {bl["tau_0"]:.0%},  k = {bl["k"]},  W_min = £{bl["W_min"]}m')

    doc.h2('## B.4. Steepness (k)').blank()
    doc.add(
        'k (per £m) controls how rapidly the marginal rate climbs from τ_0 toward τ_m. '
        'Low k produces a shallow gradient; high k produces a steep step.'
    ).blank()
    _param_section(doc, sw['rates_k_sweep'], 'k sweep (log-spaced)', bl['k'],
                   lambda v: f'{v:.4f}',
                   f'τ_0 = {bl["tau_0"]:.0%},  τ_m = {bl["tau_m"]:.0%},  W_min = £{bl["W_min"]}m')

    doc.h2('## B.5. Entry Point (W_min)').blank()
    doc.add(
        'W_min (£m) is the wealth level below which the rate function produces zero liability. '
        'It is a rate design parameter, not a population boundary.'
    ).blank()
    _param_section(doc, sw['rates_wmin_sweep'], 'W_min sweep', bl['W_min'],
                   lambda v: f'£{v}m',
                   f'τ_0 = {bl["tau_0"]:.0%},  τ_m = {bl["tau_m"]:.0%},  k = {bl["k"]}')

    doc.h2('## B.6. SRR Capitalisation Ratio (srr_ratio)').blank()
    doc.add(
        'srr_ratio sets the SRR capitalisation target as a multiple of average annual net '
        'WDT income. Affects milestone timing only; does not alter individual taxpayer burden.'
    ).blank()
    _param_section(doc, sw['rates_srr_sweep'], 'srr_ratio sweep', bl['srr_ratio'],
                   lambda v: f'{v:.1f}×',
                   f'τ_0={bl["tau_0"]:.0%}, τ_m={bl["tau_m"]:.0%}, '
                   f'k={bl["k"]}, W_min=£{bl["W_min"]}m, lrr_years={bl["lrr_years"]}')

    doc.h2('## B.7. LRR Floor (lrr_years)').blank()
    doc.add(
        f'lrr_years sets the LRR floor as a multiple of prevailing government expenditure '
        f'(growing at {bl["budget_growth"]:.2%} p.a.). Affects LRR milestone timing only.'
    ).blank()
    _param_section(doc, sw['rates_lrr_sweep'], 'lrr_years sweep', bl['lrr_years'],
                   lambda v: f'{v:.1f} yrs',
                   f'τ_0={bl["tau_0"]:.0%}, τ_m={bl["tau_m"]:.0%}, '
                   f'k={bl["k"]}, W_min=£{bl["W_min"]}m, srr_ratio={bl["srr_ratio"]}×')

    doc.h2('## B.8. Mean Growth Rate (g)').blank()
    doc.add(
        'Each row is a single deterministic run with a constant growth rate '
        'replacing the historical return series. There is no start-year '
        'distribution; the columns show point values from one SSM pass. '
        f'The hist_mean value ({bl["hist_mean"]:.2%}) appears in the table as '
        'the canonical historical baseline.'
    ).blank()
    _single_scenario_table(
        doc, sw['rates_g_sweep'],
        param_label='g sweep — deterministic constant-g scenarios',
        baseline_v=bl['hist_mean'],
        value_fmt=lambda v: f'{v:.2%}',
        note='◄ = hist_mean (canonical). No start-year distribution; one SSM/TCM run per value.',
    )

    doc.h2('## B.9. Synthetic Growth Scenario').blank()
    syn = p_base.get('synthetic_scenario', {})
    doc.add(
        r'Growth path: $g(t) = \mu + \lambda t + A \sin(2\pi t / T)$  ·  '
        f'Canonical: μ={syn.get("mu", 0.1045):.2%}, '
        f'λ={syn.get("lam", 0.0):.4f}/yr, '
        f'A={syn.get("amplitude", 0.05):.2%}, '
        f'T={syn.get("period", 10):.0f} yr.'
    ).blank()

    doc.h3('### B.9.1  Amplitude sweep (μ, λ, T fixed at canonical)')
    doc.add(
        f'λ={syn.get("lam",0.0):.4f}, μ={syn.get("mu",0.1045):.2%}, '
        f'T={syn.get("period",10):.0f} yr.'
    ).blank()
    _single_scenario_table(
        doc, sw['synthetic_amplitude_sweep'],
        param_label='Amplitude sweep',
        baseline_v=syn.get('amplitude', 0.05),
        value_fmt=lambda v: f'{v:.2%}',
        note='A=0 degenerates to a linear-trend-only scenario.',
    )

    doc.h3('### B.9.2  Period sweep (μ, λ, A fixed at canonical)')
    doc.add(
        f'λ={syn.get("lam",0.0):.4f}, μ={syn.get("mu",0.1045):.2%}, '
        f'A={syn.get("amplitude",0.05):.2%}.'
    ).blank()
    _single_scenario_table(
        doc, sw['synthetic_period_sweep'],
        param_label='Period sweep',
        baseline_v=syn.get('period', 10),
        value_fmt=lambda v: f'{v:.0f} yr',
        note='Shorter periods produce more volatile annual revenue; longer periods '
             'approach the linear-trend limit.',
    )

    # ── Reading notes ─────────────────────────────────────────────────────────
    doc.h1('C. Reading Notes').blank()
    for note in [
        ('Coverage window direction', 'SSMcov and TCMcov move together when a parameter '
         'raises or lowers revenue. The SSM–TCM gap measures sensitivity to persistent growth '
         'heterogeneity. The 50yr window is typically larger than the headline window because '
         'WDT revenue compounds on a growing wealth base.'),
        ('LRR failure vs. non-fill', 'Two distinct failure modes: (1) LRR never fills — the '
         'mechanism does not reach Phase Two; (2) LRR fails post-fill — the buffer is later '
         'exhausted. Both are solvency constraints.'),
        ('Success rate at 100%', 'The Balanced baseline achieves 100% success across all '
         '73 start years. Parameters that reduce revenue may bring the success rate below 100%.'),
        ('Pre-behavioural baseline', 'All figures are pre-behavioural. Behavioural responses '
         '— migration, restructuring, avoidance — are not modelled. See RATES §9.1 and BEHAV.'),
        ('Joint calibration', 'These sweeps vary one parameter at a time. In practice, '
         'τ_0 and τ_m jointly determine revenue level and shape; W_min and k jointly '
         'determine the gradient location.'),
    ]:
        doc.add(f'**{note[0]}.** {note[1]}').blank()

    doc.rule().blank()
    doc.add(
        '*Generated by `16_6_RATES_S_tables.py` from `sweep_cache.json`. '
        'Source: `rates_model.py` / `wdt_core.py` / `WDT_Params.toml`. '
        'No existing project files were modified.*'
    )

    out_path = _OUT / 'RATES_S_Appendix_Tables.md'
    doc.write(out_path)
    return out_path


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print('16_6 RATES_S tables (from cache)')
    p_base = load_params()
    model.validate_params(p_base)
    init(p_base)
    ensure_dir(_OUT)
    d = _load()

    print(f'Balanced baseline: τ_0={p_base["tau_0"]:.0%}  τ_m={p_base["tau_m"]:.0%}  '
          f'k={p_base["k"]}  W_min=£{p_base["W_min"]}m  '
          f'srr_ratio={p_base["srr_ratio"]}×  lrr_years={p_base["lrr_years"]}')

    out_path = build_rates_s_doc(d, p_base)
    print(f'  Written: {out_path}')


if __name__ == '__main__':
    main()
