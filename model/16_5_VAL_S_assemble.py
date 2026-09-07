"""
VAL.S Output Script 4 — Appendix Table Assembly
=================================================
Generates VAL_S_Appendix_Tables.md

C.1 matrix data (sections B.1–B.3, B.8) is read from the cache produced
by 16_0_compute.py.  Sections requiring TW/Net columns (B.4, B.5) and the
surface tables (B.6, B.7) also read from the cache.  The figure index
(B.9) is pure string construction.
"""

import json
import math
from pathlib import Path
from wdt_core import load_params, run_sim
from wdt_fmt import fmt_pct as pct, fmt_pct, eff_rate, out_dir, ensure_dir, today_iso
from wdt_md import MdDoc, md_table
from wdt_analytics import init, make_p, run_sim_p, c1, n_crossing
import wdt_analytics as _A
import numpy as np

_OUT   = out_dir('VAL_S')
_CACHE = out_dir('.').parent / 'OUTPUTS' / 'sweep_cache.json'


def _load():
    with open(_CACHE, encoding='utf-8') as fh:
        return json.load(fh)


def _nc_fmt(v):
    """Format a n_crossing value: 1 dp or em-dash."""
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return '—'
    return f'{v:.1f}'


# ── Shared C.1 heatmap table builder ─────────────────────────────────────────

def _c1_sweep_section(doc, heading, description, param_vals, canon_val,
                      matrices, param_label_fn):
    """
    Append a full parameter-sweep section to doc using cached C.1 matrices.
    Each matrix is [alpha × g] in pp, already computed by 16_0_compute.py.
    heading and param_label_fn return strings that already contain markdown
    heading markers (## / ###), so doc.add() is used rather than doc.h2/h3().
    """
    doc.add(heading).blank().add(description).blank()
    for i, (val, mat_list) in enumerate(zip(param_vals, matrices)):
        canon_mark = '  *(canonical)*' if val == canon_val else ''
        doc.add(f'{param_label_fn(val)}{canon_mark}').blank()
        mat = mat_list   # list-of-lists, already in pp
        headers = [r'$\alpha$ \ $g$'] + _A.G_LABELS
        rows = [
            [f'**{alpha}**'] + [pct(mat[ai][gi] / 100) for gi in range(len(_A.G_VALS))]
            for ai, alpha in enumerate(_A.ALPHA_VALS)
        ]
        doc.add_block(md_table(headers, rows)).blank()


# ── Section functions ─────────────────────────────────────────────────────────

def section_b1_tau0(doc, d):
    _c1_sweep_section(
        doc,
        heading=r'## B.1  $\tau_0$ Sweep — C.1 metric across $\alpha$ and $g$',
        description=(
            f'**Metric:** (Net($\\alpha$) − Net(1) / TW($\\alpha$)  ·  '
            f'$\\tau_m$ = {_A.CANON_TAUM*100:.0f}%, $k$ = {_A.CANON_K}, '
            f'N = {_A.CANON_N}, $V_0$ = £{_A.CANON_V0:.0f}m.  '
            r'$\alpha$ = 1.0 row is zero by construction.'
        ),
        param_vals=_A.TAU0_VALS,
        canon_val=_A.CANON_TAU0,
        matrices=d['val_s']['tau0_c1_matrices'],
        param_label_fn=lambda v: f'### B.1.{_A.TAU0_VALS.index(v)+1}  $\\tau_0$ = {v*100:.0f}%',
    )


def section_b2_taum(doc, d):
    _c1_sweep_section(
        doc,
        heading=r'## B.2  $\tau_m$ Sweep — C.1 metric across $\alpha$ and $g$',
        description=(
            f'**Metric:** (Net($\\alpha$) − Net(1) / TW($\\alpha$)  ·  '
            f'$\\tau_0$ = {_A.CANON_TAU0*100:.0f}%, $k$ = {_A.CANON_K}, '
            f'N = {_A.CANON_N}, $V_0$ = £{_A.CANON_V0:.0f}m.'
        ),
        param_vals=_A.TAUM_VALS,
        canon_val=_A.CANON_TAUM,
        matrices=d['val_s']['taum_c1_matrices'],
        param_label_fn=lambda v: f'### B.2.{_A.TAUM_VALS.index(v)+1}  $\\tau_m$ = {v*100:.0f}%',
    )


def section_b3_k(doc, d):
    _c1_sweep_section(
        doc,
        heading=r'## B.3  $k$ Sweep — C.1 metric across $\alpha$ and $g$',
        description=(
            f'**Metric:** (Net($\\alpha$) − Net(1) / TW($\\alpha$)  ·  '
            f'$\\tau_0$ = {_A.CANON_TAU0*100:.0f}%, $\\tau_m$ = {_A.CANON_TAUM*100:.0f}%, '
            f'N = {_A.CANON_N}, $V_0$ = £{_A.CANON_V0:.0f}m.'
        ),
        param_vals=_A.K_VALS,
        canon_val=_A.CANON_K,
        matrices=d['val_s']['k_c1_matrices'],
        param_label_fn=lambda v: f'### B.3.{_A.K_VALS.index(v)+1}  $k$ = {v}',
    )


def section_b4_n(doc, d):
    doc.add('## B.4  N Sweep — C.1 metric at four holding periods').blank()
    doc.add(
        f'**Metric:** (Net($\\alpha$,N) − Net(1,N) / TW($\\alpha$,N)  ·  '
        f'$\\tau_0$ = {_A.CANON_TAU0*100:.0f}%, $\\tau_m$ = {_A.CANON_TAUM*100:.0f}%, '
        f'$k$ = {_A.CANON_K}, $V_0$ = £{_A.CANON_V0:.0f}m, '
        f'$g$ = {_A.CANON_G*100:.2f}% throughout.  '
        r'$\alpha$ = 1.0 row is zero by construction.'
    ).blank()

    n_vals = _A.N_PANEL_VALS
    p_canon = make_p()
    for i, n in enumerate(n_vals):
        canon_mark = '  *(canonical)*' if n == _A.CANON_N else ''
        doc.add(f'### B.4.{i+1}  N = {n}{canon_mark}').blank()
        headers = [r'$\alpha$', f'C.1 at $g$ = {_A.CANON_G*100:.2f}%',
                   'TW (£m)', 'Net (£m)', 'Eff rate']
        rows = []
        for alpha in _A.ALPHA_VALS:
            r = run_sim(p_canon, alpha=alpha, g=_A.CANON_G, N=n)
            b = run_sim(p_canon, alpha=1.0,   g=_A.CANON_G, N=n)
            c1_val = ((r['Net_settled'] - b['Net_settled']) / r['TW_settled']
                      if abs(r['TW_settled']) > 1e-12 else 0.0)
            rows.append([f'**{alpha}**', pct(c1_val),
                         f'{r["TW_settled"]:.2f}', f'{r["Net_settled"]:.2f}',
                         pct(eff_rate(r))])
        doc.add_block(md_table(headers, rows)).blank()

    # N-crossing summary
    doc.add('### B.4.5  N-crossing thresholds at canonical parameters').blank()
    doc.add(
        f'First N at which overstater Net > honest Net, at $g$ = {_A.CANON_G*100:.1f}%. '
        'Interpolated to one decimal place; "—" = no crossing within N = 5–65.'
    ).blank()
    rows2 = [[f'**{alpha}**', _nc_fmt(d['val_s']['n_crossing_vals'][str(alpha)])]
             for alpha in [1.5, 1.8, 2.0]]
    doc.add_block(md_table([r'$\alpha$', 'N-crossing'], rows2)).blank()


def section_b5_v0(doc, d):
    doc.add(r'## B.5  $V_0$ Sweep — C.1 metric at four wealth levels').blank()
    doc.add(
        f'**Metric:** (Net($\\alpha$) − Net(1) / TW($\\alpha$) at $g$ = {_A.CANON_G*100:.2f}%.  '
        f'$\\tau_0$ = {_A.CANON_TAU0*100:.0f}%, $\\tau_m$ = {_A.CANON_TAUM*100:.0f}%, '
        f'$k$ = {_A.CANON_K}, N = {_A.CANON_N}.'
    ).blank()

    for i, v0 in enumerate(_A.V0_VALS):
        canon_mark = '  *(canonical)*' if v0 == _A.CANON_V0 else ''
        doc.add(f'### B.5.{i+1}  $V_0$ = £{v0:.0f}m{canon_mark}').blank()
        p = make_p(V0_m=v0)
        headers = [r'$\alpha$', 'C.1', 'TW (£m)', 'Net (£m)', 'Eff rate']
        rows = []
        for alpha in _A.ALPHA_VALS:
            r = run_sim(p, alpha=alpha, g=_A.CANON_G, N=_A.CANON_N)
            b = run_sim(p, alpha=1.0,   g=_A.CANON_G, N=_A.CANON_N)
            c1_val = ((r['Net_settled'] - b['Net_settled']) / r['TW_settled']
                      if abs(r['TW_settled']) > 1e-12 else 0.0)
            rows.append([f'**{alpha}**', pct(c1_val),
                         f'{r["TW_settled"]:.2f}', f'{r["Net_settled"]:.2f}',
                         pct(eff_rate(r))])
        doc.add_block(md_table(headers, rows)).blank()


def section_b6_tau0_n_surface(doc, d):
    doc.add(r'## B.6  $\tau_0$ × N Joint Surface — N-crossing for $\alpha$ = 2.0').blank()
    doc.add(
        f'**Metric:** First N at which Net($\\alpha$=2.0) > Net($\\alpha$=1.0) '
        f'at $g$ = {_A.CANON_G*100:.1f}%.  '
        f'$\\tau_m$ = {_A.CANON_TAUM*100:.0f}%, $k$ = {_A.CANON_K}, '
        f'$V_0$ = £{_A.CANON_V0:.0f}m.  '
        '"—" = no crossing found within N sweep ceiling.'
    ).blank()

    tau0_grid   = d['val_s']['tau0_n_surface_tau0_grid']
    n_ceil_grid = d['val_s']['tau0_n_surface_nceil_grid']
    surface     = d['val_s']['tau0_n_surface']

    tau0_labels = [f'$\\tau_0$={t*100:.0f}%' for t in tau0_grid]
    headers     = [r'N ceiling \ $\tau_0$'] + tau0_labels
    rows = [
        [str(n_ceil)] + [
            (f'{v:.0f}' if v is not None else '—')
            for v in surface[i]
        ]
        for i, n_ceil in enumerate(n_ceil_grid)
    ]
    doc.add_block(md_table(headers, rows)).blank()
    doc.add(f'*Canonical cell: $\\tau_0$ = {_A.CANON_TAU0*100:.0f}%, '
            f'N ceiling = {_A.CANON_N}.*').blank()


def section_b7_k_v0_surface(doc, d):
    doc.add(r'## B.7  $k$ × $V_0$ Joint Surface — C.1 Bracket Penalty for $\alpha$ = 1.8').blank()
    doc.add(
        f'**Metric:** (Net(1.8) − Net(1.0) / TW(1.8) at $g$ = {_A.CANON_G*100:.1f}%, '
        f'N = {_A.CANON_N}.  '
        f'$\\tau_0$ = {_A.CANON_TAU0*100:.0f}%, $\\tau_m$ = {_A.CANON_TAUM*100:.0f}%.  '
        'Negative = overstater pays less than honest.'
    ).blank()

    k_grid  = d['val_s']['k_v0_surface_k_grid']
    v0_grid = d['val_s']['k_v0_surface_v0_grid']
    surface = d['val_s']['k_v0_surface']

    headers = [r'$k$ \ $V_0$'] + [f'£{v:.0f}m' for v in v0_grid]
    rows = [
        [str(k)] + [pct(surface[i][j] / 100) for j in range(len(v0_grid))]
        for i, k in enumerate(k_grid)
    ]
    doc.add_block(md_table(headers, rows)).blank()
    doc.add(f'*Canonical cell: $k$ = {_A.CANON_K}, $V_0$ = £{_A.CANON_V0:.0f}m.*').blank()


def section_b8_wmin(doc, d):
    _c1_sweep_section(
        doc,
        heading=r'## B.8  $W_{min}$ Sweep — C.1 metric across $\alpha$ and $g$',
        description=(
            f'**Metric:** (Net($\\alpha$) − Net(1) / TW($\\alpha$))  ·  '
            f'$\\tau_0$ = {_A.CANON_TAU0*100:.0f}%, $\\tau_m$ = {_A.CANON_TAUM*100:.0f}%, '
            f'$k$ = {_A.CANON_K}, N = {_A.CANON_N}, $V_0$ = £{_A.CANON_V0:.0f}m, '
            f'$g$ = {_A.CANON_G*100:.2f}% throughout.  '
            r'$W_{min}$ is the entry threshold; $\alpha$ = 1.0 row is zero by construction.'
        ),
        param_vals=_A.WMIN_VALS,
        canon_val=_A.CANON_WMIN,
        matrices=d['val_s']['wmin_c1_matrices'],
        param_label_fn=lambda v: f'### B.8.{_A.WMIN_VALS.index(v)+1}  $W_{{min}}$ = £{v:.0f}m',
    )

    # N-crossing subtable
    doc.add('### B.8.5  N-crossing thresholds by $W_{min}$').blank()
    doc.add(
        f'First N at which overstater Net > honest Net, at $g$ = {_A.CANON_G*100:.1f}%. '
        'Interpolated to one decimal place; "—" = no crossing within N = 5–65.'
    ).blank()
    headers2 = [r'$W_{min}$'] + [f'$\\alpha$ = {a}' for a in [1.5, 1.8, 2.0]]
    rows2 = []
    for w_min in _A.WMIN_VALS:
        p = make_p(W_min=w_min)
        canon_mark = ' *(canon)*' if w_min == _A.CANON_WMIN else ''
        row = [f'**£{w_min:.0f}m**{canon_mark}']
        for alpha in [1.5, 1.8, 2.0]:
            row.append(_nc_fmt(n_crossing(p, alpha)))
        rows2.append(row)
    doc.add_block(md_table(headers2, rows2)).blank()


def section_b9_figure_index(doc):
    doc.add('## B.9  Figure Index').blank()
    doc.add(
        'All figures are generated by the VAL.S output scripts and share `wdt_core.py` '
        'as the simulation engine with no modifications.  VAL.A cross-references indicate '
        'which (SWEEPS.A §A) or (SWEEPS.A §B) subsection covers the same metric at '
        'canonical parameters.'
    ).blank()

    registry = [
        ('S2.1a', 'val_s_fig_s2_1a_tau0_heatmaps.png',
         r'C.1 advantage landscape across $\tau_0$ values — 4-panel heatmap grid',
         r'Rows = $\alpha$; cols = $g$; colour = C.1 (pp)',
         f'$\\tau_m$={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, N={_A.CANON_N}, $V_0$=£{_A.CANON_V0:.0f}m', 'C.1'),
        ('S2.1b', 'val_s_fig_s2_1b_tau0_n_crossings.png',
         r'N-crossing thresholds for $\alpha$ ∈ {1.5,1.8,2.0} as a function of $\tau_0$',
         r'x=$\tau_0$ (%); y=N at crossing; line per $\alpha$',
         f'$\\tau_m$={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, g={_A.CANON_G*100:.1f}%', 'C.7, B.5.6'),
        ('S2.1c', 'val_s_fig_s2_1c_tau0_tolerant_zone.png',
         r'Tolerant-zone $\alpha$ boundaries as a function of $\tau_0$',
         r'x=$\tau_0$ (%); y=$\alpha$; filled band=tolerant zone',
         f'k={_A.CANON_K}, N={_A.CANON_N}, g={_A.CANON_G*100:.1f}%', 'B.6'),
        ('S2.2a', 'val_s_fig_s2_2a_taum_heatmaps.png',
         r'C.1 advantage landscape across $\tau_m$ values — 4-panel heatmap grid',
         r'As S2.1a; $\tau_m$ swept across panels',
         f'$\\tau_0$={_A.CANON_TAU0*100:.0f}%, k={_A.CANON_K}, N={_A.CANON_N}', 'C.1'),
        ('S2.2b', 'val_s_fig_s2_2b_taum_penalty_plateaus.png',
         r'Understater penalty plateau ceiling by $\alpha$ and $\tau_m$',
         r'x=$\alpha$ (understater range); y=plateau ceiling (pp); line per $\tau_m$',
         f'$\\tau_0$={_A.CANON_TAU0*100:.0f}%, k={_A.CANON_K}, N={_A.CANON_N}', 'C.9, B.5.4'),
        ('S2.2c', 'val_s_fig_s2_2c_taum_n_crossings.png',
         r'N-crossing thresholds for aggressive overstaters as a function of $\tau_m$',
         r'x=$\tau_m$ (%); y=N at crossing; line per $\alpha$',
         f'$\\tau_0$={_A.CANON_TAU0*100:.0f}%, k={_A.CANON_K}, g={_A.CANON_G*100:.1f}%', 'C.7, B.5.4'),
        ('S2.3a', 'val_s_fig_s2_3a_k_rate_curves.png',
         r'Rate curve $\tau(W)$ overlaid for four $k$ values',
         r'x=W (£m, log); y=$\tau(W)$ (%); line per k',
         f'$\\tau_0$={_A.CANON_TAU0*100:.0f}%, $\\tau_m$={_A.CANON_TAUM*100:.0f}%, $W_{{min}}$=£{_A.CANON_WMIN:.0f}m', 'B.3.1'),
        ('S2.3b', 'val_s_fig_s2_3b_k_heatmaps.png',
         r'C.1 advantage landscape across $k$ values — 4-panel heatmap grid',
         r'As S2.1a; $k$ swept across panels',
         f'$\\tau_0$={_A.CANON_TAU0*100:.0f}%, $\\tau_m$={_A.CANON_TAUM*100:.0f}%, N={_A.CANON_N}', 'C.1, C.5'),
        ('S2.3c', 'val_s_fig_s2_3c_k_bracket_penalty.png',
         r'Bracket penalty for $\alpha$=1.8 by k and V₀',
         r'x=k; y=C.1 (pp) at $\alpha$=1.8; line per $V_0$',
         f'$\\tau_0$={_A.CANON_TAU0*100:.0f}%, $\\tau_m$={_A.CANON_TAUM*100:.0f}%, N={_A.CANON_N}', 'C.1, B.5.2'),
        ('S2.4a', 'val_s_fig_s2_4a_wmin_rate_curves.png',
         r'Rate curve $\tau(W)$ overlaid for four $W_{min}$ values',
         r'x=W (£m, log); y=$\tau(W)$ (%); line per $W_{min}$',
         f'$\\tau_0$={_A.CANON_TAU0*100:.0f}%, $\\tau_m$={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}', 'B.3.1'),
        ('S2.4b', 'val_s_fig_s2_4b_wmin_heatmaps.png',
         r'C.1 advantage landscape across $W_{min}$ values — 4-panel heatmap grid',
         r'As S2.1a; $W_{min}$ swept across panels',
         f'$\\tau_0$={_A.CANON_TAU0*100:.0f}%, k={_A.CANON_K}, N={_A.CANON_N}', 'C.1'),
        ('S2.4c', 'val_s_fig_s2_4c_wmin_n_crossings.png',
         r'N-crossing thresholds as a function of $W_{min}$',
         r'x=$W_{min}$ (£m); y=N at crossing; line per $\alpha$',
         f'$\\tau_0$={_A.CANON_TAU0*100:.0f}%, k={_A.CANON_K}, g={_A.CANON_G*100:.1f}%', 'C.7, B.5.4'),
        ('S3.1a', 'val_s_fig_s3_1a_n_crossing_annotated.png',
         'Overstater advantage erosion and N-crossing thresholds (two-panel)',
         r'Left: x=N, y=Net diff £m. Right: bar chart of crossing N.',
         f'$\\tau_0$={_A.CANON_TAU0*100:.0f}%, k={_A.CANON_K}, g={_A.CANON_G*100:.1f}%', 'C.7, B.6'),
        ('S3.1b', 'val_s_fig_s3_1b_n_understater_panels.png',
         r'Understater C.1 penalty profile by $g$ at four N values — 4-panel',
         r'x=$g$ (%); y=C.1 (pp); line per understater $\alpha$; panel per N',
         f'$\\tau_0$={_A.CANON_TAU0*100:.0f}%, k={_A.CANON_K}', 'C.9, B.5.3'),
        ('S3.1c', 'val_s_fig_s3_1c_n_tolerant_zone.png',
         r'Tolerant-zone $\alpha$ boundaries across N values',
         r'x=N (years); y=$\alpha$; filled band=tolerant zone',
         f'$\\tau_0$={_A.CANON_TAU0*100:.0f}%, k={_A.CANON_K}, g={_A.CANON_G*100:.1f}%', 'B.6'),
        ('S3.2a', 'val_s_fig_s3_2a_v0_c1_curves.png',
         r'C.1 incentive structure by $V_0$ entry wealth — overlaid curves',
         r'x=$\alpha$ (%); y=C.1 (pp); line per $V_0$',
         f'$\\tau_0$={_A.CANON_TAU0*100:.0f}%, k={_A.CANON_K}, N={_A.CANON_N}', 'C.1'),
        ('S3.2b', 'val_s_fig_s3_2b_v0_entry_rate.png',
         r'Entry rate $\tau(V_0)$ at four wealth levels on the rate curve',
         r'x=W (£m, log); y=$\tau(W)$ (%); markers at $V_0$ levels',
         f'$\\tau_0$={_A.CANON_TAU0*100:.0f}%, k={_A.CANON_K}', 'B.3.1'),
        ('S3.2c', 'val_s_fig_s3_2c_v0_heatmaps.png',
         r'C.1 advantage landscape across $V_0$ wealth levels — 4-panel heatmap grid',
         r'As S2.1a; $V_0$ swept across panels',
         f'$\\tau_0$={_A.CANON_TAU0*100:.0f}%, k={_A.CANON_K}, N={_A.CANON_N}', 'C.1'),
        ('S4.1', 'val_s_fig_s4_1_tau0_n_surface.png',
         r'Joint surface: N-crossing for $\alpha$=2.0 across ($\tau_0$, N ceiling)',
         r'x=$\tau_0$ (%); y=N sweep ceiling; colour=N-crossing; grey=no crossing',
         f'$\\tau_m$={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, g={_A.CANON_G*100:.1f}%', 'C.7, B.6'),
        ('S4.2', 'val_s_fig_s4_2_k_v0_surface.png',
         r'Joint surface: C.1 bracket penalty for $\alpha$=1.8 across (k, $V_0$)',
         r'x=$V_0$ (£m); y=k; colour=C.1 (pp); bold border=canonical',
         f'$\\tau_0$={_A.CANON_TAU0*100:.0f}%, $\\tau_m$={_A.CANON_TAUM*100:.0f}%, N={_A.CANON_N}', 'C.1, C.5'),
        ('S4.3', 'val_s_fig_s4_3_calibration_summary.png',
         r'Calibration summary — three mechanism properties by parameter variant',
         r'Three bar-chart panels: tolerant-zone width, N-crossing (α=1.8), plateau (α=0.1)',
         f'N={_A.CANON_N}, $V_0$=£{_A.CANON_V0:.0f}m, g={_A.CANON_G*100:.1f}%', 'B.6, C.9'),
    ]

    headers = ['Fig', 'File', 'Title', 'Axes', 'Parameters', 'VAL.A ref']
    rows    = [[f'S{ref}', fn, title, axes, params, val_a]
               for ref, fn, title, axes, params, val_a in registry]
    doc.add_block(md_table(headers, rows)).blank()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print('VAL.S Script 4 — appendix table assembly (from cache)')
    p = load_params()
    init(p)
    ensure_dir(_OUT)
    d = _load()

    doc = MdDoc()
    doc.h1('VAL.S — Appendix Tables').blank()
    doc.add(f'**Generated:** {today_iso()}')
    doc.add(
        f'**Model:** Python v1.0 via wdt_core.py  ·  '
        f'Canonical: $\\tau_0$={_A.CANON_TAU0*100:.0f}%, $\\tau_m$={_A.CANON_TAUM*100:.0f}%, '
        f'k={_A.CANON_K}, $W_{{min}}$=£{_A.CANON_WMIN:.0f}m, N={_A.CANON_N}, '
        f'$V_0$=£{_A.CANON_V0:.0f}m, $g$={_A.CANON_G*100:.2f}%'
    ).blank()
    doc.add(
        '**Metric (all tables unless stated):** C.1 = (Net($\\alpha$) − Net(1)) / TW($\\alpha$).  '
        'Positive = $\\alpha$ pays more net tax than honest.  '
        r'$\alpha$ = 1.0 row is zero by construction.'
    ).blank()
    doc.add(
        '**Note on VAL.A alignment:** the live TOML canonical values may differ slightly from '
        'the VAL.A §C.1 printed snapshot (generated at a different TOML state). '
        'VAL.S uses the live TOML as its reference throughout.'
    ).blank().rule().blank()

    print('  Section B.1: τ₀ sweep...')
    section_b1_tau0(doc, d)
    print('  Section B.2: τ_m sweep...')
    section_b2_taum(doc, d)
    print('  Section B.3: k sweep...')
    section_b3_k(doc, d)
    print('  Section B.4: N sweep...')
    section_b4_n(doc, d)
    print('  Section B.5: V₀ sweep...')
    section_b5_v0(doc, d)
    print('  Section B.6: τ₀ × N surface...')
    section_b6_tau0_n_surface(doc, d)
    print('  Section B.7: k × V₀ surface...')
    section_b7_k_v0_surface(doc, d)
    print('  Section B.8: W_min sweep...')
    section_b8_wmin(doc, d)
    print('  Section B.9: figure index...')
    section_b9_figure_index(doc)

    doc.write(_OUT / 'VAL_S_Appendix_Tables.md')
    print('\nScript 4 complete.')


if __name__ == '__main__':
    main()
