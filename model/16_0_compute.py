"""
16_0_compute.py — WDT Sweep Data Pre-computation
==================================================
Runs every expensive simulation used by the 16_x output scripts and
writes the results to a single JSON cache file.

The 16_2–16_7 scripts load this cache instead of recomputing.
Re-run this script whenever WDT_Params.toml changes.

Output
------
  OUTPUTS/sweep_cache.json

What is cached
--------------
  VAL.S (16_2, 16_3, 16_4, 16_5)
    tau0_c1_matrices    c1_matrix() for each TAU0_VALS entry
    taum_c1_matrices    c1_matrix() for each TAUM_VALS entry
    k_c1_matrices       c1_matrix() for each K_VALS entry
    wmin_c1_matrices    c1_matrix() for each WMIN_VALS entry
    tau0_n_crossings    n_crossing() grid [TAU0_VALS × OVER_ALPHAS]
    taum_n_crossings    n_crossing() grid [taum_fine × OVER_ALPHAS]
    k_bracket_penalty   c1() grid [k_fine × V0_points] at alpha=1.8
    wmin_n_crossings    n_crossing() grid [wmin_fine × OVER_ALPHAS]
    tau0_tzone          tolerant_zone_bounds() for tau0_fine
    n_diffs             Net_settled diff by N for each OVER_ALPHA
    n_crossing_vals     n_crossing() for canonical p, each OVER_ALPHA
    n_understater_c1    c1() grid [N_PANEL × UNDER_ALPHAS × g_fine]
    n_tzone             tolerant_zone_bounds() for n_fine
    v0_c1_curves        c1() grid [V0_VALS × alpha_fine]
    v0_heatmaps         c1_matrix() for each V0_VALS entry
    tau0_n_surface      n_crossing() surface [tau0_grid × n_ceil_grid]
    k_v0_surface        c1() surface [k_grid × v0_grid] at alpha=1.8
    calibration         tzone_width, n_crossing, understater_plateau per variant

  RATES.S (16_6, 16_7)
    rates_tau0_sweep    run_param_sweep() for tau_0
    rates_taum_sweep    run_param_sweep() for tau_m
    rates_k_sweep       run_param_sweep() for k
    rates_wmin_sweep    run_param_sweep() for W_min
    rates_srr_sweep     run_param_sweep() for srr_ratio
    rates_lrr_sweep     run_param_sweep() for lrr_years
    burden_tau0         _tcm_burden_sweep() for tau_0
    burden_taum         _tcm_burden_sweep() for tau_m
    burden_k            _tcm_burden_sweep() for k
    burden_wmin         _tcm_burden_sweep() for W_min

What is NOT cached (cheap, recomputed in output scripts)
---------------------------------------------------------
  tau(W, p) — pure math
  matplotlib / figure layout
"""

import json
import math
from copy import deepcopy
from pathlib import Path

import numpy as np

from wdt_core import load_params, run_sim, tau
from wdt_fmt import out_dir, ensure_dir, today_iso
from wdt_analytics import (
    init, make_p, run_sim_p, c1, c1_matrix, n_crossing,
    tolerant_zone_bounds, tolerant_zone_width, understater_plateau,
    run_param_sweep, run_g_sweep, run_synthetic_sweep,
)
import wdt_analytics as _A
import rates_model as model

# ── Output path ───────────────────────────────────────────────────────────────
_ROOT_OUT = out_dir('.')          # OUTPUTS/
_CACHE    = Path(__file__).parent / 'OUTPUTS' / 'sweep_cache.json'


# ── JSON serialisation helpers ────────────────────────────────────────────────

def _jsonify(obj):
    """Recursively convert numpy types and nan/inf to JSON-safe values."""
    if isinstance(obj, dict):
        return {k: _jsonify(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonify(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return _jsonify(obj.tolist())
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        v = float(obj)
        return None if (math.isnan(v) or math.isinf(v)) else v
    if isinstance(obj, float):
        return None if (math.isnan(obj) or math.isinf(obj)) else obj
    return obj


# ── TCM burden sweep (duplicated from 16_7 to avoid import) ──────────────────

def _weighted_quantiles(vals, weights, quantiles):
    if not vals:
        return [None] * len(quantiles)
    pairs = sorted(zip(vals, weights), key=lambda x: x[0])
    sv, sw = zip(*pairs)
    total = sum(sw)
    cum, cum_w = 0.0, []
    for w in sw:
        cum_w.append(cum + 0.5 * w / total)
        cum += w / total
    results = []
    for q in quantiles:
        if q <= cum_w[0]:
            results.append(sv[0]); continue
        if q >= cum_w[-1]:
            results.append(sv[-1]); continue
        for i in range(1, len(cum_w)):
            if cum_w[i] >= q:
                span_w = cum_w[i] - cum_w[i - 1]
                frac = (q - cum_w[i - 1]) / span_w if span_w > 0 else 0.0
                results.append(sv[i - 1] + frac * (sv[i] - sv[i - 1]))
                break
    return results


def _tcm_burden_sweep(p_base, param_key, values):
    results = []
    for v in values:
        p = deepcopy(p_base)
        p[param_key] = v
        if p['tau_0'] >= p['tau_m'] or p['W_min'] < 0:
            continue
        try:
            tcm = model.run_tcm(p, N=p_base['N'], N_fill=1)
        except Exception:
            continue
        wb_vals, er_vals, pops = [], [], []
        for tier in p['tiers']:
            diff = tier['differential']
            for cell in tcm[diff]:
                wb_vals.append(cell['wealth_burden'])
                er_vals.append(cell['eff_rate'])
                pops.append(cell['cell_pop'])
        wb_q = _weighted_quantiles(wb_vals, pops, [0.0, 0.25, 0.50, 0.75, 1.0])
        er_q = _weighted_quantiles(er_vals, pops, [0.0, 0.25, 0.50, 0.75, 1.0])
        results.append({
            'value':  v, 'x_raw': v,
            'wb_min': wb_q[0], 'wb_q25': wb_q[1], 'wb_med': wb_q[2],
            'wb_q75': wb_q[3], 'wb_max': wb_q[4],
            'er_min': er_q[0], 'er_q25': er_q[1], 'er_med': er_q[2],
            'er_q75': er_q[3], 'er_max': er_q[4],
        })
    return results


# ── VAL.S section helpers ─────────────────────────────────────────────────────

def _compute_val_s(p, sw):
    print('\n── VAL.S computations ──')
    cache = {}

    # ── §2.1 τ₀ sweep ────────────────────────────────────────────────────────
    print('  §2.1 τ₀: c1_matrices ...')
    cache['tau0_c1_matrices'] = [
        c1_matrix(make_p(tau_0=t)).tolist() for t in _A.TAU0_VALS
    ]

    print('  §2.1 τ₀: n_crossings ...')
    tau0_fine = [t / 100 for t in range(5, 45)]
    cache['tau0_fine'] = tau0_fine
    cache['tau0_n_crossings'] = {
        str(alpha): [
            _A.n_crossing(make_p(tau_0=t), alpha)
            for t in tau0_fine
        ]
        for alpha in _A.OVER_ALPHAS
    }

    print('  §2.1 τ₀: tolerant zone ...')
    cache['tau0_tzone'] = [
        list(tolerant_zone_bounds(make_p(tau_0=t))) for t in tau0_fine
    ]

    # ── §2.2 τ_m sweep ───────────────────────────────────────────────────────
    print('  §2.2 τ_m: c1_matrices ...')
    cache['taum_c1_matrices'] = [
        c1_matrix(make_p(tau_m=t)).tolist() for t in _A.TAUM_VALS
    ]

    print('  §2.2 τ_m: penalty plateaus ...')
    under_alphas = [0.1, 0.2, 0.5, 0.8]
    g_plateau = [g / 100 for g in range(18, 41)]
    cache['taum_penalty_plateaus'] = {
        f'{tau_m:.2f}': {
            f'{alpha:.1f}': max(c1(make_p(tau_m=tau_m), alpha, gv) * 100
                                for gv in g_plateau)
            for alpha in under_alphas
        }
        for tau_m in [0.50, 0.60, 0.70, 0.80]
    }

    print('  §2.2 τ_m: n_crossings ...')
    taum_fine = [t / 100 for t in range(40, 85, 5)]
    cache['taum_fine'] = taum_fine
    cache['taum_n_crossings'] = {
        str(alpha): [
            _A.n_crossing(make_p(tau_m=t), alpha)
            for t in taum_fine
        ]
        for alpha in _A.OVER_ALPHAS
    }

    # ── §2.3 k sweep ─────────────────────────────────────────────────────────
    print('  §2.3 k: c1_matrices ...')
    cache['k_c1_matrices'] = [
        c1_matrix(make_p(k=k)).tolist() for k in _A.K_VALS
    ]

    print('  §2.3 k: bracket penalty ...')
    k_fine = [k / 10000 for k in range(1, 55)]
    v0_points = [20.0, 100.0, 500.0]
    cache['k_fine'] = k_fine
    cache['k_bracket_penalty'] = {
        f'{v0:.0f}': [c1(make_p(k=k, V0_m=v0), alpha=1.8, g=_A.CANON_G) * 100
                      for k in k_fine]
        for v0 in v0_points
    }

    # ── §2.4 W_min sweep ─────────────────────────────────────────────────────
    print('  §2.4 W_min: c1_matrices ...')
    cache['wmin_c1_matrices'] = [
        c1_matrix(make_p(W_min=w)).tolist() for w in _A.WMIN_VALS
    ]

    print('  §2.4 W_min: n_crossings ...')
    wmin_fine = [w / 10 for w in range(5, 110, 5)]
    cache['wmin_fine'] = wmin_fine
    cache['wmin_n_crossings'] = {
        str(alpha): [
            _A.n_crossing(make_p(W_min=w), alpha)
            for w in wmin_fine
        ]
        for alpha in _A.OVER_ALPHAS
    }

    # ── §3.1 N sweep ─────────────────────────────────────────────────────────
    print('  §3.1 N: net diff trajectories ...')
    N_sweep = list(range(5, 66))
    p_canon = make_p()
    cache['n_sweep'] = N_sweep
    cache['n_diffs'] = {
        str(alpha): [
            run_sim(p_canon, alpha=alpha, g=_A.CANON_G, N=n)['Net_settled']
            - run_sim(p_canon, alpha=1.0,   g=_A.CANON_G, N=n)['Net_settled']
            for n in N_sweep
        ]
        for alpha in _A.OVER_ALPHAS
    }

    print('  §3.1 N: crossing thresholds ...')
    cache['n_crossing_vals'] = {
        str(alpha): _A.n_crossing(p_canon, alpha, N_sweep=N_sweep)
        for alpha in _A.OVER_ALPHAS
    }

    print('  §3.1 N: understater panels ...')
    g_fine = [g / 1000 for g in range(0, 401)]
    cache['g_fine'] = g_fine
    cache['n_understater_c1'] = {
        str(n): {
            str(alpha): [c1(make_p(N=n), alpha, gv, N=n) * 100 for gv in g_fine]
            for alpha in _A.UNDER_ALPHAS
        }
        for n in _A.N_PANEL_VALS
    }

    print('  §3.1 N: tolerant zone ...')
    n_fine = list(range(5, 66, 2))
    cache['n_fine'] = n_fine
    cache['n_tzone'] = [
        list(tolerant_zone_bounds(make_p(N=n))) for n in n_fine
    ]

    # ── §3.2 V₀ sweep ────────────────────────────────────────────────────────
    print('  §3.2 V₀: c1 curves ...')
    alpha_fine = [a / 100 for a in range(10, 201, 5)]
    cache['alpha_fine'] = alpha_fine
    cache['v0_c1_curves'] = {
        f'{v0:.0f}': [c1(make_p(V0_m=v0), a, _A.CANON_G) * 100 for a in alpha_fine]
        for v0 in _A.V0_VALS
    }

    print('  §3.2 V₀: heatmaps ...')
    cache['v0_c1_matrices'] = [
        c1_matrix(make_p(V0_m=v0)).tolist() for v0 in _A.V0_VALS
    ]

    # ── §4.1 τ₀ × N surface ──────────────────────────────────────────────────
    print('  §4.1 τ₀ × N surface ...')
    tau0_grid   = sw['tau0_n_surface_tau0']
    n_ceil_grid = sw['tau0_n_surface_nceil']
    cache['tau0_n_surface_tau0_grid'] = tau0_grid
    cache['tau0_n_surface_nceil_grid'] = n_ceil_grid
    surface_tau0_n = []
    for n_ceil in n_ceil_grid:
        row = []
        for tau_0 in tau0_grid:
            nc = _A.n_crossing(make_p(tau_0=tau_0), alpha=2.0,
                               N_sweep=list(range(5, n_ceil + 1)))
            row.append(nc)
        surface_tau0_n.append(row)
    cache['tau0_n_surface'] = surface_tau0_n

    # ── §4.2 k × V₀ surface ──────────────────────────────────────────────────
    print('  §4.2 k × V₀ surface ...')
    k_grid  = sw['k_v0_surface_k']
    v0_grid = sw['k_v0_surface_v0']
    cache['k_v0_surface_k_grid'] = k_grid
    cache['k_v0_surface_v0_grid'] = v0_grid
    cache['k_v0_surface'] = [
        [c1(make_p(k=k, V0_m=v0), alpha=1.8, g=_A.CANON_G) * 100
         for v0 in v0_grid]
        for k in k_grid
    ]

    # ── §4.3 Calibration summary ──────────────────────────────────────────────
    print('  §4.3 calibration summary ...')
    variants = {
        'τ₀=10%':           make_p(tau_0=0.10),
        'τ₀=15%':           make_p(tau_0=0.15),
        'τ₀=20% (canon)':   make_p(tau_0=0.20),
        'τ₀=30%':           make_p(tau_0=0.30),
        'τ_m=50%':          make_p(tau_m=0.50),
        'τ_m=60%':          make_p(tau_m=0.60),
        'τ_m=70% (canon)':  make_p(tau_m=0.70),
        'τ_m=80%':          make_p(tau_m=0.80),
        'k=0.0001':         make_p(k=0.0001),
        'k=0.0005':         make_p(k=0.0005),
        'k=0.001 (canon)':  make_p(k=0.001),
        'k=0.005':          make_p(k=0.005),
        'W_min=£1m':        make_p(W_min=1.0),
        'W_min=£2m (canon)': make_p(W_min=2.0),
        'W_min=£5m':        make_p(W_min=5.0),
        'W_min=£10m':       make_p(W_min=10.0),
    }
    nc_raw = {lbl: _A.n_crossing(pv, alpha=1.8) for lbl, pv in variants.items()}
    cache['calibration'] = {
        lbl: {
            'tzone_width':     tolerant_zone_width(pv),
            'n_crossing_1_8':  nc_raw[lbl] if not math.isnan(nc_raw[lbl] or float('nan')) else None,
            'plateau_0_1':     understater_plateau(pv, alpha=0.1),
        }
        for lbl, pv in variants.items()
    }

    return cache


# ── RATES.S section ───────────────────────────────────────────────────────────

def _compute_rates_s(p_base, sw):
    print('\n── RATES.S computations ──')
    cache = {}

    sweeps = [
        ('rates_tau0_sweep',  'tau_0',     sw['rates_tau_0_sweep']),
        ('rates_taum_sweep',  'tau_m',     sw['rates_tau_m_sweep']),
        ('rates_k_sweep',     'k',         sw['rates_k_sweep']),
        ('rates_wmin_sweep',  'W_min',     sw['rates_wmin_sweep']),
        ('rates_srr_sweep',   'srr_ratio', sw['rates_srr_ratio_sweep']),
        ('rates_lrr_sweep',   'lrr_years', sw['rates_lrr_years_sweep']),
    ]

    for cache_key, param, values in sweeps:
        print(f'  {cache_key} ({len(values)} values × 73 start years) ...')
        cache[cache_key] = run_param_sweep(p_base, param, values, label=param)

    burden_sweeps = [
        ('burden_tau0', 'tau_0', sw['rates_tau_0_sweep']),
        ('burden_taum', 'tau_m', sw['rates_tau_m_sweep']),
        ('burden_k',    'k',     sw['rates_k_sweep']),
        ('burden_wmin', 'W_min', sw['rates_wmin_sweep']),
    ]

    for cache_key, param, values in burden_sweeps:
        print(f'  {cache_key} ...')
        cache[cache_key] = _tcm_burden_sweep(p_base, param, values)

    # ── g sweep (deterministic constant-g scenarios) ──────────────────────
    print(f'\n  rates_g_sweep ({len(sw["rates_g_sweep"])} values, 1 scenario each) ...')
    cache['rates_g_sweep'] = run_g_sweep(p_base, sw['rates_g_sweep'])

    # ── Synthetic scenario sweeps (amplitude and period) ──────────────────
    syn = p_base.get('synthetic_scenario', {})
    amp_vals = syn.get('amplitude_sweep', [])
    per_vals = syn.get('period_sweep',    [])

    print(f'\n  synthetic_amplitude_sweep ({len(amp_vals)} values) ...')
    cache['synthetic_amplitude_sweep'] = run_synthetic_sweep(
        p_base, sweep_param='amplitude', values=amp_vals,
    )

    print(f'\n  synthetic_period_sweep ({len(per_vals)} values) ...')
    cache['synthetic_period_sweep'] = run_synthetic_sweep(
        p_base, sweep_param='period', values=per_vals,
    )

    # Store the canonical synthetic series for plotting in 16_7
    from wdt_core import synthetic_returns
    cache['synthetic_canonical_series'] = synthetic_returns(
        n=80,
        mu=syn.get('mu',        p_base['hist_mean']),
        lam=syn.get('lam',      0.0),
        amplitude=syn.get('amplitude', 0.05),
        period=syn.get('period', 10.0),
    )
    cache['synthetic_params'] = {
        'mu':        syn.get('mu',        p_base['hist_mean']),
        'lam':       syn.get('lam',       0.0),
        'amplitude': syn.get('amplitude', 0.05),
        'period':    syn.get('period',    10.0),
    }

    return cache


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print('16_0_compute.py — pre-computing all sweep data')

    p = load_params()
    init(p)
    sw = p['sweep']

    ensure_dir(_CACHE.parent)

    # ── Build the full cache dict ─────────────────────────────────────────────
    cache = {
        'meta': {
            'generated':  today_iso(),
            'canon_tau0': _A.CANON_TAU0,
            'canon_taum': _A.CANON_TAUM,
            'canon_k':    _A.CANON_K,
            'canon_wmin': _A.CANON_WMIN,
            'canon_n':    _A.CANON_N,
            'canon_v0':   _A.CANON_V0,
            'canon_g':    _A.CANON_G,
            # Grid constants needed by the output scripts
            'tau0_vals':   _A.TAU0_VALS,
            'taum_vals':   _A.TAUM_VALS,
            'k_vals':      _A.K_VALS,
            'wmin_vals':   _A.WMIN_VALS,
            'v0_vals':     _A.V0_VALS,
            'alpha_vals':  _A.ALPHA_VALS,
            'over_alphas': _A.OVER_ALPHAS,
            'under_alphas':_A.UNDER_ALPHAS,
            'g_vals':      _A.G_VALS,
            'g_labels':    _A.G_LABELS,
            'n_panel_vals':_A.N_PANEL_VALS,
            'tzone_threshold': _A.TZONE_THRESHOLD,
        },
        'val_s':   _compute_val_s(p, sw),
        'rates_s': _compute_rates_s(p, sw),
    }

    # ── Serialise ─────────────────────────────────────────────────────────────
    print(f'\nSerialising to {_CACHE} ...')
    with open(_CACHE, 'w', encoding='utf-8') as fh:
        json.dump(_jsonify(cache), fh, separators=(',', ':'))

    size_mb = _CACHE.stat().st_size / 1_048_576
    print(f'Written: {_CACHE}  ({size_mb:.1f} MB)')
    print('\n16_0_compute.py complete.')


if __name__ == '__main__':
    main()
