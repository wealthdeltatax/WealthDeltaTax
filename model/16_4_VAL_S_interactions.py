"""
VAL.S Output Script 3 — Parameter Interaction Surfaces
========================================================
Generates figures for §4 of VAL.S.  All simulation data is loaded from
OUTPUTS/sweep_cache.json (produced by 16_0_compute.py).

Figures
-------
  §4.1  τ₀ × N joint surface — N-crossing threshold for α=2.0
  §4.2  k × V₀ joint surface — bracket penalty for α=1.8
  §4.3  Governing Council calibration summary
"""

import json
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch

from wdt_core import load_params
from wdt_fmt import out_dir, ensure_dir
from wdt_style import apply_style, apply_style_nogrid, save_fig
from wdt_analytics import init, tolerant_zone_width, understater_plateau
import wdt_analytics as _A

_OUT   = out_dir('VAL_S')
_CACHE = out_dir('.').parent / 'OUTPUTS' / 'sweep_cache.json'


def _load():
    with open(_CACHE, encoding='utf-8') as fh:
        return json.load(fh)


def _save(fig, name):
    return save_fig(fig, _OUT / name)


# ── §4.1  τ₀ × N surface ─────────────────────────────────────────────────────

def fig_tau0_n_surface(d):
    apply_style_nogrid()
    tau0_grid   = d['val_s']['tau0_n_surface_tau0_grid']
    n_ceil_grid = d['val_s']['tau0_n_surface_nceil_grid']
    # Restore nan from None
    surface = np.array(
        [[v if v is not None else np.nan for v in row]
         for row in d['val_s']['tau0_n_surface']],
        dtype=float,
    )

    fig, ax = plt.subplots(figsize=(11, 7))
    cmap = plt.cm.RdYlGn_r.copy()
    cmap.set_bad(color='#cccccc')
    masked = np.ma.masked_invalid(surface)
    ax.imshow(masked, aspect='auto', cmap=cmap, vmin=5, vmax=65,
              extent=[tau0_grid[0] * 100 - 1.5, tau0_grid[-1] * 100 + 1.5,
                      n_ceil_grid[-1] + 2.5,     n_ceil_grid[0] - 2.5])

    for i, n_ceil in enumerate(n_ceil_grid):
        for j, tau_0 in enumerate(tau0_grid):
            val = surface[i, j]
            if not np.isnan(val):
                ax.text(tau_0 * 100, n_ceil, f'{val:.0f}',
                        ha='center', va='center', fontsize=7,
                        color='white' if val < 25 or val > 55 else '#1a1a1a')
            else:
                ax.text(tau_0 * 100, n_ceil, '—', ha='center', va='center',
                        fontsize=7, color='#888888')

    ax.axvline(_A.CANON_TAU0 * 100, color='#1a1a1a', linewidth=1.5, linestyle='--',
               label=f'Canonical τ₀={_A.CANON_TAU0*100:.0f}%')
    ax.axhline(_A.CANON_N, color='#1a1a1a', linewidth=1.5, linestyle=':',
               label=f'RATES N={_A.CANON_N}')

    norm = mcolors.Normalize(vmin=5, vmax=65)
    fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax,
                 fraction=0.04, pad=0.02).set_label(
        'N-crossing threshold for α=2.0  (grey = no crossing)', fontsize=8)

    ax.set_xlabel('Entry rate τ₀ (%)')
    ax.set_ylabel('Maximum holding period (N sweep ceiling, years)')
    ax.set_title(
        'Fig S4.1 — Joint surface: N-crossing for α=2.0 across (τ₀, N)\n'
        f'τ_m={_A.CANON_TAUM*100:.0f}%, k={_A.CANON_K}, V₀=£{_A.CANON_V0:.0f}m, '
        f'g={_A.CANON_G*100:.1f}%\n'
        'Green = early crossing  ·  Red = late  ·  Grey = never',
        fontsize=9
    )
    ax.legend(fontsize=8)
    plt.tight_layout()
    _save(fig, 'val_s_fig_s4_1_tau0_n_surface.png')


# ── §4.2  k × V₀ surface ─────────────────────────────────────────────────────

def fig_k_v0_surface(d):
    apply_style_nogrid()
    k_grid  = d['val_s']['k_v0_surface_k_grid']
    v0_grid = d['val_s']['k_v0_surface_v0_grid']
    surface = np.array(d['val_s']['k_v0_surface'])

    fig, ax = plt.subplots(figsize=(10, 7))
    vbound = max(abs(surface.min()), abs(surface.max()))
    norm   = mcolors.TwoSlopeNorm(vmin=-vbound, vcenter=0, vmax=vbound)
    im     = ax.imshow(surface, aspect='auto', cmap='RdBu_r', norm=norm)

    for i in range(len(k_grid)):
        for j in range(len(v0_grid)):
            v   = surface[i, j]
            col = 'white' if abs(v) > vbound * 0.5 else '#1a1a1a'
            ax.text(j, i, f'{v:.1f}', ha='center', va='center', fontsize=8, color=col)

    ax.set_xticks(range(len(v0_grid)))
    ax.set_xticklabels([f'£{v:.0f}m' for v in v0_grid])
    ax.set_yticks(range(len(k_grid)))
    ax.set_yticklabels([str(k) for k in k_grid])
    ax.set_xlabel('Entry wealth V₀ (£m)')
    ax.set_ylabel('Steepness parameter k')

    # Canonical cell border
    can_k  = k_grid.index(_A.CANON_K)  if _A.CANON_K  in k_grid  else None
    can_v0 = v0_grid.index(_A.CANON_V0) if _A.CANON_V0 in v0_grid else None
    if can_k is not None and can_v0 is not None:
        ax.add_patch(plt.Rectangle((can_v0 - 0.5, can_k - 0.5), 1, 1,
                                   fill=False, edgecolor='#1a1a1a', linewidth=2.5,
                                   label='Canonical cell'))
    ax.legend(fontsize=8, loc='upper left')
    fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02).set_label(
        'C.1 (pp) at α=1.8  — negative = overstater pays less', fontsize=8)
    ax.set_title(
        'Fig S4.2 — Joint surface: bracket penalty (C.1) for α=1.8 across (k, V₀)\n'
        f'τ₀={_A.CANON_TAU0*100:.0f}%, τ_m={_A.CANON_TAUM*100:.0f}%, '
        f'N={_A.CANON_N}, g={_A.CANON_G*100:.1f}%\n'
        'Red = overstater pays more  ·  Blue = overstater pays less  ·  Bold = canonical',
        fontsize=9
    )
    plt.tight_layout()
    _save(fig, 'val_s_fig_s4_2_k_v0_surface.png')


# ── §4.3  Calibration summary ─────────────────────────────────────────────────

def fig_calibration_summary(d):
    apply_style()
    cal      = d['val_s']['calibration']
    labels   = list(cal.keys())
    tzone_w  = [cal[lbl]['tzone_width'] for lbl in labels]
    cross_ns = [cal[lbl]['n_crossing_1_8'] or 70.0 for lbl in labels]
    plateaus = [cal[lbl]['plateau_0_1'] for lbl in labels]

    group_cols   = ['#2166ac'] * 4 + ['#d73027'] * 4 + ['#7b2d8b'] * 4 + ['#1a7a2a'] * 4
    canon_flags  = [False, False, True, False,
                    False, False, True, False,
                    False, False, True, False,
                    False, True, False, False]
    x = range(len(labels))

    def _add_canon_borders(ax, heights):
        for xi, flag, ht in zip(x, canon_flags, heights):
            if flag:
                ax.add_patch(plt.Rectangle((xi - 0.35, 0), 0.7, ht + 0.5,
                                           fill=False, edgecolor='black', linewidth=2))

    fig, axes = plt.subplots(3, 1, figsize=(16, 12))

    axes[0].bar(x, [w * 100 for w in tzone_w], color=group_cols, edgecolor='white', width=0.7)
    _add_canon_borders(axes[0], [w * 100 for w in tzone_w])
    axes[0].set_ylabel('Tolerant-zone width (% of α range where |C.1| < 2pp)')
    axes[0].set_title('Tolerant-zone width', fontsize=9)
    axes[0].set_xticks(x); axes[0].set_xticklabels(labels, fontsize=7.0)

    axes[1].bar(x, cross_ns, color=group_cols, edgecolor='white', width=0.7)
    axes[1].axhline(_A.CANON_N, color='#888888', linewidth=1.0, linestyle='--',
                    label=f'RATES N={_A.CANON_N}')
    _add_canon_borders(axes[1], cross_ns)
    axes[1].set_ylabel('N-crossing for α=1.8 (years)')
    axes[1].set_title('N-crossing threshold for aggressive overstatement (α=1.8)', fontsize=9)
    axes[1].set_xticks(x); axes[1].set_xticklabels(labels, fontsize=7.0)
    axes[1].legend(fontsize=7.5); axes[1].set_ylim(0, 80)

    axes[2].bar(x, plateaus, color=group_cols, edgecolor='white', width=0.7)
    _add_canon_borders(axes[2], plateaus)
    axes[2].set_ylabel('Understater plateau ceiling (pp) at α=0.1, g>17%')
    axes[2].set_title('Understater penalty plateau ceiling (α=0.1)', fontsize=9)
    axes[2].set_xticks(x); axes[2].set_xticklabels(labels, fontsize=7.0)

    legend_elements = [
        Patch(facecolor='#2166ac', label='τ₀ variants'),
        Patch(facecolor='#d73027', label='τ_m variants'),
        Patch(facecolor='#7b2d8b', label='k variants'),
        Patch(facecolor='#1a7a2a', label='W_min variants'),
    ]
    axes[0].legend(handles=legend_elements, loc='upper right', fontsize=7.5)

    fig.suptitle(
        'Fig S4.3 — Governing Council calibration summary\n'
        'How each rate-function parameter moves the three key mechanism boundaries\n'
        f'Bold borders = canonical  ·  N={_A.CANON_N}, V₀=£{int(_A.CANON_V0)}m, '
        f'g={_A.CANON_G*100:.1f}%',
        fontsize=10
    )
    plt.tight_layout()
    _save(fig, 'val_s_fig_s4_3_calibration_summary.png')


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    p = load_params()
    init(p)
    ensure_dir(_OUT)
    d = _load()

    print('VAL.S Script 3 — parameter interaction surfaces (from cache)')

    print('\n§4.1  τ₀ × N surface...')
    fig_tau0_n_surface(d)

    print('\n§4.2  k × V₀ surface...')
    fig_k_v0_surface(d)

    print('\n§4.3  Calibration summary...')
    fig_calibration_summary(d)

    print(f'\nScript 3 complete. Figures in {_OUT}')


if __name__ == '__main__':
    main()
