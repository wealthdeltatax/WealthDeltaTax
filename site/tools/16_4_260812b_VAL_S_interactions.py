"""
VAL.S Output Script 3 — Parameter Interaction Surfaces
========================================================
Generates figures for §4 of VAL.S:
  §4.1  τ₀ × N joint surface — N-crossing threshold for α = 2.0
  §4.2  k × V₀ joint surface — bracket penalty for α = 1.8
  §4.3  Governing Council calibration summary

Note: heatmap figures in this script use set_style_nogrid() rather than
set_style() to prevent grid lines overlaying imshow cells.

Canonical reference:  τ₀=20%, τ_m=70%, k=0.001, N=34, g=10.45%, V₀=£20m
Outputs to: ./OUTPUTS/VAL_S/
All simulation via wdt_core.run_sim() with caching from val_s_helpers.
"""

from val_s_helpers import *

save = save_fig           # all calls in this script use save(fig, name)
set_style = set_style_nogrid  # §4 figures are heatmaps — no grid

_P  = load_params()
_SW = _P['sweep']


# ─────────────────────────────────────────────────────────────
# §4.1  τ₀ × N SURFACE
# ─────────────────────────────────────────────────────────────

def fig_tau0_n_surface():
    """
    Heatmap surface: N-crossing threshold for α = 2.0
    as a joint function of τ₀ and N (held period at which we evaluate).
    
    Axes:
      x = τ₀ (entry rate, 5–40%)
      y = Maximum N to test up to (i.e., the ceiling of the N sweep)
          — this lets us ask: "if taxpayers only hold for up to N years,
            does the crossing occur within their horizon?"
    Colour: crossing N (how soon the overstater starts paying more).
    White = no crossing found within the sweep ceiling.
    """
    set_style()

    tau0_grid   = _SW['tau0_n_surface_tau0']
    n_ceil_grid = _SW['tau0_n_surface_nceil']

    surface = np.full((len(n_ceil_grid), len(tau0_grid)), np.nan)

    for j, tau_0 in enumerate(tau0_grid):
        p = make_p(tau_0=tau_0)
        for i, n_ceil in enumerate(n_ceil_grid):
            nc = n_crossing(p, alpha=2.0, N_sweep=list(range(5, n_ceil + 1)))
            surface[i, j] = nc  # np.nan if not found

    fig, ax = plt.subplots(figsize=(11, 7))

    vmin = 5
    vmax = 65
    cmap = plt.cm.RdYlGn_r.copy()
    cmap.set_bad(color='#cccccc')  # grey = no crossing

    masked = np.ma.masked_invalid(surface)
    im = ax.imshow(
        masked, aspect='auto', cmap=cmap, vmin=vmin, vmax=vmax,
        extent=[tau0_grid[0] * 100 - 1.5, tau0_grid[-1] * 100 + 1.5,
                n_ceil_grid[-1] + 2.5, n_ceil_grid[0] - 2.5]
    )

    # Annotate cells with the crossing N
    for i, n_ceil in enumerate(n_ceil_grid):
        for j, tau_0 in enumerate(tau0_grid):
            val = surface[i, j]
            if not np.isnan(val):
                ax.text(
                    tau_0 * 100, n_ceil, f'{val:.0f}',
                    ha='center', va='center', fontsize=7,
                    color='white' if val < 25 or val > 55 else '#1a1a1a'
                )
            else:
                ax.text(tau_0 * 100, n_ceil, '—', ha='center', va='center',
                        fontsize=7, color='#888888')

    # Mark canonical τ₀ and RATES N
    ax.axvline(CANON_TAU0 * 100, color='#1a1a1a', linewidth=1.5, linestyle='--',
               label=f'Canonical τ₀ = {CANON_TAU0*100:.0f}%')
    ax.axhline(CANON_N, color='#1a1a1a', linewidth=1.5, linestyle=':',
               label=f'RATES N = {CANON_N}')

    cbar = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
    cbar.set_label('N-crossing threshold for α = 2.0  (grey = no crossing)', fontsize=8)

    ax.set_xlabel('Entry rate τ₀ (%)')
    ax.set_ylabel('Maximum holding period (N sweep ceiling, years)')
    ax.set_title(
        'Fig S4.1 — Joint surface: N-crossing threshold for α = 2.0 across (τ₀, N)\n'
        f'τ_m = {CANON_TAUM*100:.0f}%, k = {CANON_K}, V₀ = £{CANON_V0:.0f}m, g = {CANON_G*100:.1f}%\n'
        'Green = early crossing (overstater quickly disadvantaged)  ·  Red = late  ·  Grey = never',
        fontsize=9
    )
    ax.legend(fontsize=8)
    plt.tight_layout()
    save(fig, 'val_s_fig_s4_1_tau0_n_surface.png')


# ─────────────────────────────────────────────────────────────
# §4.2  k × V₀ SURFACE
# ─────────────────────────────────────────────────────────────

def fig_k_v0_surface():
    """
    Heatmap surface: C.1 bracket penalty for α = 1.8 at canonical g,
    as a joint function of k and V₀.
    
    This extends VAL.A §C.4 (which sweeps k × V₀ for α=1, honest declaration)
    into the declaration-strategy dimension.
    """
    set_style()

    k_grid  = _SW['k_v0_surface_k']
    v0_grid = _SW['k_v0_surface_v0']

    surface = np.zeros((len(k_grid), len(v0_grid)))

    for i, k_val in enumerate(k_grid):
        for j, v0 in enumerate(v0_grid):
            p = make_p(k=k_val, V0_m=v0)
            surface[i, j] = c1(p, alpha=1.8, g=CANON_G) * 100

    fig, ax = plt.subplots(figsize=(10, 7))

    # Use diverging colourmap centred on 0
    vbound = max(abs(surface.min()), abs(surface.max()))
    norm = mcolors.TwoSlopeNorm(vmin=-vbound, vcenter=0, vmax=vbound)

    im = ax.imshow(surface, aspect='auto', cmap='RdBu_r', norm=norm)

    # Annotate each cell
    for i in range(len(k_grid)):
        for j in range(len(v0_grid)):
            v = surface[i, j]
            col = 'white' if abs(v) > vbound * 0.5 else '#1a1a1a'
            ax.text(j, i, f'{v:.1f}', ha='center', va='center', fontsize=8, color=col)

    ax.set_xticks(range(len(v0_grid)))
    ax.set_xticklabels([f'£{v:.0f}m' for v in v0_grid])
    ax.set_yticks(range(len(k_grid)))
    ax.set_yticklabels([f'{k}' for k in k_grid])
    ax.set_xlabel('Entry wealth V₀ (£m)')
    ax.set_ylabel('Steepness parameter k')

    # Mark canonical cell
    can_k_idx  = k_grid.index(CANON_K)
    can_v0_idx = v0_grid.index(CANON_V0)
    ax.add_patch(plt.Rectangle(
        (can_v0_idx - 0.5, can_k_idx - 0.5), 1, 1,
        fill=False, edgecolor='#1a1a1a', linewidth=2.5, label='Canonical cell'
    ))
    ax.legend(fontsize=8, loc='upper left')

    cbar = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
    cbar.set_label('C.1 (pp) at α = 1.8  — negative = overstater pays less', fontsize=8)

    ax.set_title(
        'Fig S4.2 — Joint surface: bracket penalty (C.1) for α = 1.8 across (k, V₀)\n'
        f'τ₀ = {CANON_TAU0*100:.0f}%, τ_m = {CANON_TAUM*100:.0f}%, N = {CANON_N}, g = {CANON_G*100:.1f}%\n'
        'Red = overstater pays more  ·  Blue = overstater pays less  ·  Bold border = canonical',
        fontsize=9
    )
    plt.tight_layout()
    save(fig, 'val_s_fig_s4_2_k_v0_surface.png')


# ─────────────────────────────────────────────────────────────
# §4.3  GOVERNING COUNCIL CALIBRATION SUMMARY
# ─────────────────────────────────────────────────────────────

def fig_calibration_summary():
    """
    Spider/dashboard chart showing how each of the four main parameters
    (τ₀, τ_m, k, N) moves the three key mechanism properties:
      1. Tolerant-zone width (α band where |C.1| < 2pp)
      2. N-crossing for α = 1.8 (when aggressive overstatement starts costing)
      3. Understater plateau ceiling at α = 0.1

    Presented as three separate mini-panels (one per property) with
    bars showing the value at each parameter level vs canonical.
    """
    set_style()

    # Parameter variants to test — four groups: τ₀, τ_m, k, W_min
    variants = {
        'τ₀ = 10%':         make_p(tau_0=0.10),
        'τ₀ = 15%':         make_p(tau_0=0.15),
        'τ₀ = 20%\n(canon)': make_p(tau_0=0.20),
        'τ₀ = 30%':         make_p(tau_0=0.30),
        'τ_m = 50%':        make_p(tau_m=0.50),
        'τ_m = 60%':        make_p(tau_m=0.60),
        'τ_m = 70%\n(canon)': make_p(tau_m=0.70),
        'τ_m = 80%':        make_p(tau_m=0.80),
        'k = 0.0001':       make_p(k=0.0001),
        'k = 0.0005':       make_p(k=0.0005),
        'k = 0.001\n(canon)': make_p(k=0.001),
        'k = 0.005':        make_p(k=0.005),
        'W_min = £1m':      make_p(W_min=1.0),
        'W_min = £2m\n(canon)': make_p(W_min=2.0),
        'W_min = £5m':      make_p(W_min=5.0),
        'W_min = £10m':     make_p(W_min=10.0),
    }

    labels   = list(variants.keys())
    p_list   = list(variants.values())

    print('  Computing calibration summary metrics...')
    tzone_widths  = []
    crossing_ns   = []
    plateau_ceils = []

    for lbl, p in variants.items():
        tzone_widths.append(tolerant_zone_width(p))
        nc = n_crossing(p, alpha=1.8)
        crossing_ns.append(nc if not np.isnan(nc) else 70.0)   # 70 = "very late / no crossing"
        plateau_ceils.append(understater_plateau(p, alpha=0.1))
        print(f'    {lbl.replace(chr(10)," ")}: tz={tzone_widths[-1]:.2f}, nc={crossing_ns[-1]:.0f}, plat={plateau_ceils[-1]:.1f}pp')

    fig, axes = plt.subplots(3, 1, figsize=(16, 12))

    group_cols = (
        ['#2166ac'] * 4 +   # τ₀ group
        ['#d73027'] * 4 +   # τ_m group
        ['#7b2d8b'] * 4 +   # k group
        ['#1a7a2a'] * 4     # W_min group
    )
    canon_flags = [False, False, True, False,
                   False, False, True, False,
                   False, False, True, False,
                   False, True, False, False]
    x = range(len(labels))

    # Panel 1: Tolerant-zone width
    axes[0].bar(x, [w * 100 for w in tzone_widths], color=group_cols,
                edgecolor='white', width=0.7)
    for xi, flag in zip(x, canon_flags):
        if flag:
            axes[0].add_patch(plt.Rectangle((xi - 0.35, 0), 0.7,
                                            tzone_widths[xi] * 100 + 0.5,
                                            fill=False, edgecolor='black', linewidth=2))
    axes[0].set_ylabel('Tolerant-zone width (% of α range\nwhere |C.1| < 2pp)')
    axes[0].set_title('Tolerant-zone width', fontsize=9)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels, fontsize=7.0)

    # Panel 2: N-crossing for α = 1.8
    axes[1].bar(x, crossing_ns, color=group_cols, edgecolor='white', width=0.7)
    axes[1].axhline(CANON_N, color='#888888', linewidth=1.0, linestyle='--',
                    label=f'RATES N = {CANON_N}')
    for xi, flag in zip(x, canon_flags):
        if flag:
            axes[1].add_patch(plt.Rectangle((xi - 0.35, 0), 0.7,
                                            crossing_ns[xi] + 0.5,
                                            fill=False, edgecolor='black', linewidth=2))
    axes[1].set_ylabel('N-crossing for α = 1.8 (years)\nlower = self-limiting mechanism activates earlier')
    axes[1].set_title('N-crossing threshold for aggressive overstatement (α = 1.8)', fontsize=9)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels, fontsize=7.0)
    axes[1].legend(fontsize=7.5)
    axes[1].set_ylim(0, 80)

    # Panel 3: Understater penalty plateau for α = 0.1
    axes[2].bar(x, plateau_ceils, color=group_cols, edgecolor='white', width=0.7)
    for xi, flag in zip(x, canon_flags):
        if flag:
            axes[2].add_patch(plt.Rectangle((xi - 0.35, 0), 0.7,
                                            plateau_ceils[xi] + 0.5,
                                            fill=False, edgecolor='black', linewidth=2))
    axes[2].set_ylabel('Understater plateau ceiling (pp)\nat α = 0.1, g > 17%')
    axes[2].set_title('Understater penalty plateau ceiling (α = 0.1)', fontsize=9)
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(labels, fontsize=7.0)

    # Group labels via text annotations on fig
    group_x = [1.5, 5.5, 9.5, 13.5]   # midpoints of τ₀, τ_m, k, W_min groups
    group_labels = ['τ₀ group', 'τ_m group', 'k group', 'W_min group']
    group_label_cols = ['#2166ac', '#d73027', '#7b2d8b', '#1a7a2a']
    for xi, gl, gc in zip(group_x, group_labels, group_label_cols):
        axes[2].annotate(
            gl, xy=(xi, -0.12), xycoords=('data', 'axes fraction'),
            ha='center', fontsize=8, color=gc, fontweight='bold'
        )

    # Bold borders = canonical
    from matplotlib.patches import Patch
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
        'Bold borders = canonical values  ·  N = {}, V₀ = £{}m, g = {:.1f}%'.format(
            CANON_N, int(CANON_V0), CANON_G * 100),
        fontsize=10
    )
    plt.tight_layout()
    save(fig, 'val_s_fig_s4_3_calibration_summary.png')


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main():
    print('VAL.S Script 3: parameter interaction surfaces')
    print(f'Canonical (from TOML): τ₀={CANON_TAU0*100:.0f}%, τ_m={CANON_TAUM*100:.0f}%, '
          f'k={CANON_K}, N={CANON_N}, V₀=£{CANON_V0:.0f}m, g={CANON_G*100:.2f}%')
    os.makedirs(OUT_DIR, exist_ok=True)

    print('\n§4.1  τ₀ × N surface...')
    fig_tau0_n_surface()

    print('\n§4.2  k × V₀ surface...')
    fig_k_v0_surface()

    print('\n§4.3  Calibration summary...')
    fig_calibration_summary()

    print(f'\nScript 3 complete. Figures in {OUT_DIR}')


if __name__ == '__main__':
    main()
