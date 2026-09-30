"""
val_core.py — VAL Simulation Runner
====================================
Single entry point for all VAL simulation work.  Loads parameters,
runs every simulation needed by 5_3 (tables), 5_4 (charts), and 5_5
(worked examples), then serialises the full result set to:

    OUTPUTS/VAL/val_data.json

The three creator scripts load that file via load_val_data() instead
of calling wdt_core directly.  val_core.py has no matplotlib dependency
and no markdown output — it is pure computation.

Usage
-----
    python val_core.py                  # run all simulations, write JSON
    python val_core.py --dry-run        # load params + print grid sizes, no sim

REFACTOR NOTES (N and metrics)
------------------------------
1. N.  Every individual-level table and figure runs at N = p['N_val'] (= 30).
   wdt_core no longer has an implicit N; every call below passes N explicitly.
   Each table/figure dict carries an 'N' stamp, and _validate() fails the run
   if any stamp differs from N_val or if internal cross-checks (C.11.4 == C.8,
   C.5 == C.8, C.10.1 == C.10.2, C.11 identity, in-kind payment identity)
   break.  p['N_fill'] (SSM LRR fill year) is used ONLY for the reference line
   in Fig 7.1a.

2. Metrics.  Every heatmap now carries the same three quantities on the SAME
   denominator, TW_settled(1):
       net   = (Net(a)  - Net(1))  / TW(1)      + = pays more net tax (C.1)
       tw_cost = (TW(1) - TW(a))   / TW(1)      + = worse off        (-C.5/C.8)
       pv    = (PVtrue(a) - PVtrue(1)) / TW(1)  + = pays more in PV  (C.12)
   net, tw_cost and pv share a sign convention (positive = worse off /
   pays more), so panels can share a colour scale.  C.1 previously divided by
   TW(alpha); it now divides by TW(1).  C.12 previously discounted the credited
   liability L; it now discounts the true value surrendered (L/alpha in the
   holding period).  The legacy C.12 is kept under 'c12_declared_legacy' for
   audit only.

val_data.json schema
--------------------
Top-level keys:

  meta          dict    run identity (date, param snapshot, version, validation)
  params        dict    scalar parameters used for all runs
  grids         dict    all analytical grid arrays
  tables        dict    data for 5_3 (C.1–C.12 tables)
  charts        dict    data for 5_4 (all figure series / surfaces)
  examples      dict    data for 5_5 (§J–§N worked examples)

Design principles
-----------------
- All monetary values in £m (matching wdt_core convention).
- All rates as fractions (never pre-multiplied by 100) in tables; chart
  matrices are in percentage points (pp) as before.
- JSON-safe: no numpy arrays in the output — everything is plain
  Python lists/dicts/floats/ints/strings.
- Idempotent: running twice with the same TOML produces byte-identical
  output (no timestamp in the body; date string only in meta).
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np

from wdt_core import (
    load_params, tau,
    simulate, simulate_sell, settle_tw,
    run_sim, run_sim_hist, run_pair,
    decompose_tw_advantage, npv_tax_advantage,
    g_eff as _g_eff,
)
from wdt_fmt import out_dir, ensure_dir

_OUT = out_dir('VAL')
_JSON_PATH = _OUT / 'val_data.json'

# ─────────────────────────────────────────────────────────────
# JSON SERIALISATION HELPER
# ─────────────────────────────────────────────────────────────

def _to_json_safe(obj: Any) -> Any:
    """Recursively convert numpy scalars / arrays to plain Python."""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, dict):
        return {str(k): _to_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_json_safe(v) for v in obj]
    return obj


def load_val_data(json_path: Path | None = None) -> dict:
    """
    Load the pre-computed val_data.json.

    Raises
    ------
    FileNotFoundError   if the JSON does not exist (run val_core.py first)
    """
    path = Path(json_path) if json_path else _JSON_PATH
    if not path.exists():
        raise FileNotFoundError(
            f"val_data.json not found at {path}.\n"
            "Run  python val_core.py  to generate it."
        )
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


# ─────────────────────────────────────────────────────────────
# GRID SETUP
# ─────────────────────────────────────────────────────────────

def _build_grids(p: dict) -> dict:
    """Extract all analytical grids from the param sweep section."""
    sw = p['sweep']
    return {
        'g_vals':        sw['g_vals'],
        'g_labels':      [f"{v * 100:.1f}%" for v in sw['g_vals']],
        'alpha_vals':    sw['alpha_vals'],
        'over_vals':     sw['appc_over_vals'],
        'under_alphas':  sw['under_alphas'],
        'over_alphas':   sw['over_alphas'],
        'k_vals':        sw['appc_k_vals'],
        'v0_vals':       sw['appc_v0_vals'],
        'n_actual_vals': sw['n_actual_vals'],
        # dense chart grids
        'fig_g_fine':    [g / 1000 for g in range(0, 1001)],    # 0–100% in 0.1% steps
        'fig_g_fine_400': [g / 1000 for g in range(0, 400)],   # 0–40%
        'fig_alpha_fine': [a / 100 for a in range(50, 205, 5)], # 0.5–2.0
        'fig_alpha_over': np.linspace(1.0, 2.0, 41).tolist(),
        'fig_g_decomp':  np.linspace(0.0, 0.25, 51).tolist(),
        'fig_g_surface': np.linspace(0.001, 0.28, 56).tolist(),
        'fig_n_surface': list(range(5, 62)),
        'fig_g_heatmap': np.linspace(0.0, 0.40, 101).tolist(),
        'fig_alpha_heatmap': np.linspace(0.1, 2.0, 41).tolist(),
        # Specific alpha sets used by chart figures
        'alpha_under':  [0.1, 0.2, 0.5, 0.8],
        'alpha_over':   [1.2, 1.5, 1.8, 2.0],
    }


# ─────────────────────────────────────────────────────────────
# HELPER — rate-function sweep
# ─────────────────────────────────────────────────────────────

def _rate_curve(p: dict) -> dict:
    """τ(W) for the chart fig 05."""
    sim_p = {k: p[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}
    w_vals = np.logspace(np.log10(p['W_min']), np.log10(10000), 500)
    return {
        'w_vals':   w_vals.tolist(),
        'tau_vals': [tau(w, sim_p) for w in w_vals],
    }


# ─────────────────────────────────────────────────────────────
# TABLES DATA (5_3)
# ─────────────────────────────────────────────────────────────

def _compute_tables(p: dict, grids: dict) -> dict:
    """
    Compute all data needed by 5_3_VAL_tables.py (C.1–C.12).

    String-keyed dicts (for JSON compatibility).  Every simulation runs at
    N = p['N_val'] unless the table is itself an N sweep.
    """
    N             = p['N_val']
    G_VALS        = grids['g_vals']
    ALPHA_VALS    = grids['alpha_vals']
    K_VALS        = grids['k_vals']
    V0_VALS       = grids['v0_vals']
    N_ACTUAL_VALS = grids['n_actual_vals']
    OVER_VALS     = grids['over_vals']

    def _str(v): return str(v)   # dict keys must be strings for JSON

    print(f"  [tables] N = {N} (N_fill = {p['N_fill']}, NOT used)")
    print("  [tables] C.1 / C.1-TW / C.12 — common-denominator metrics...")

    # C.1 (net tax), C.1-TW (terminal wealth) and C.12 (PV) in one pass
    t1 = {}; t1_tw = {}; t12 = {}; t12_legacy = {}
    for alpha in ALPHA_VALS:
        r_net = []; r_tw = []; r_pv = []; r_leg = []
        for g in G_VALS:
            m = run_pair(p, alpha, g, N)
            r_net.append(m['net_pct'])
            r_tw.append(m['tw_gap'])          # + = retains more (C.5/C.8 convention)
            r_pv.append(m['pv_pct'])
            r_leg.append(m['pv_declared_pct'])
        t1[_str(alpha)] = r_net
        t1_tw[_str(alpha)] = r_tw
        t12[_str(alpha)] = r_pv
        t12_legacy[_str(alpha)] = r_leg

    # C.2
    base_by_g = {g: run_sim(p, alpha=1.0, beta=0.0, g=g, N=N) for g in G_VALS}
    t2 = {}
    for alpha in ALPHA_VALS:
        row = []
        for g in G_VALS:
            r = run_sim(p, alpha=alpha, beta=0.0, g=g, N=N)
            b = base_by_g[g]
            val = (r['Net_settled'] / r['TW_settled'] - b['Net_settled'] / b['TW_settled']
                   if abs(r['TW_settled']) > 1e-12 and abs(b['TW_settled']) > 1e-12 else 0.0)
            row.append(val)
        t2[_str(alpha)] = row

    # C.3 (beta sweep, over_vals only) — denominator now TW(1, beta=0)
    print("  [tables] C.3 — beta sweep...")
    base_ref = run_sim(p, alpha=1.0, beta=0.0, g=p['g'], N=N)
    t3 = {}
    for alpha in OVER_VALS:
        row = []
        for beta_col in G_VALS:
            r = run_sim(p, alpha=alpha, beta=beta_col, g=p['g'], N=N)
            val = ((r['Net_settled'] - base_ref['Net_settled']) / base_ref['TW_settled']
                   if abs(base_ref['TW_settled']) > 1e-12 else 0.0)
            row.append(val)
        t3[_str(alpha)] = row

    # C.4 (k × V0, effective tax rate)
    print("  [tables] C.4 — k × V0 grid...")
    t4 = {}
    for k_val in K_VALS:
        row = []
        for v0 in V0_VALS:
            tp = dict(p); tp['k'] = k_val; tp['V0_m'] = float(v0)
            r = run_sim(tp, alpha=1.0, beta=0.0, g=tp['g'], N=N)
            row.append(r['TTP'] / r['TW_settled'] if abs(r['TW_settled']) > 1e-12 else 0.0)
        t4[_str(k_val)] = row

    # C.5 (k × alpha, TW difference)
    print("  [tables] C.5 — k × alpha grid...")
    t5 = {}
    for alpha in ALPHA_VALS:
        row = []
        for k_val in K_VALS:
            tp = dict(p); tp['k'] = k_val
            r = run_sim(tp, alpha=alpha, beta=0.0, g=tp['g'], N=N)
            b = run_sim(tp, alpha=1.0, beta=0.0, g=tp['g'], N=N)
            row.append((r['TW_settled'] - b['TW_settled']) / b['TW_settled']
                       if abs(b['TW_settled']) > 1e-12 else 0.0)
        t5[_str(alpha)] = row

    # C.6 (refund protection, negative g only)
    print("  [tables] C.6 — refund protection (negative g)...")
    neg_g_vals = [g for g in G_VALS if g < 0]
    neg_g_labels = [f"{g * 100:.1f}%" for g in neg_g_vals]
    base_neg = {g: run_sim(p, alpha=1.0, beta=0.0, g=g, N=N) for g in neg_g_vals}
    t6 = {}
    for alpha in ALPHA_VALS:
        row = []
        for g in neg_g_vals:
            r = run_sim(p, alpha=alpha, beta=0.0, g=g, N=N)
            b = base_neg[g]
            row.append(r['TW_settled'] / b['TW_settled'] if abs(b['TW_settled']) > 1e-12 else 0.0)
        t6[_str(alpha)] = row

    # C.7 / C.8 (N sweep)
    print("  [tables] C.7/C.8 — N sweep...")
    t7 = {}; t8 = {}
    for alpha in ALPHA_VALS:
        row7 = []; row8 = []
        for n_act in N_ACTUAL_VALS:
            r = run_sim(p, alpha=alpha, beta=0.0, g=p['g'], N=n_act)
            b = run_sim(p, alpha=1.0,   beta=0.0, g=p['g'], N=n_act)
            v7 = ((r['Net_settled'] - b['Net_settled']) / b['Net_settled']
                  if abs(b['Net_settled']) > 1e-12 else 0.0)
            v8 = ((r['TW_settled']  - b['TW_settled'])  / b['TW_settled']
                  if abs(b['TW_settled'])  > 1e-12 else 0.0)
            row7.append(v7); row8.append(v8)
        t7[_str(alpha)] = row7
        t8[_str(alpha)] = row8

    # C.9 (scenario summary, α ∈ {2.0, 1.0, 0.1})
    print("  [tables] C.9 — scenario summary...")
    t9 = []
    for g in sorted([g for g in G_VALS if g >= 0], reverse=True):
        r2  = run_sim(p, alpha=2.0, beta=0.0, g=g, N=N)
        r1  = run_sim(p, alpha=1.0, beta=0.0, g=g, N=N)
        r01 = run_sim(p, alpha=0.1, beta=0.0, g=g, N=N)
        refund_ratio = (r01['Net_settled'] / r1['Net_settled']
                        if r1['Net_settled'] < 0 and abs(r1['Net_settled']) > 1e-12 else None)
        t9.append({
            'g':         g,
            'TW_a2':     r2['TW_settled'],  'TW_a1':  r1['TW_settled'],  'TW_a01':  r01['TW_settled'],
            'Net_a2':    r2['Net_settled'], 'Net_a1': r1['Net_settled'], 'Net_a01': r01['Net_settled'],
            'refund_ratio': refund_ratio,
        })

    # C.10 (historical series) — N explicit: C.10.1 and C.10.2 now agree at N_val
    print("  [tables] C.10 — historical series...")
    base_hist = run_sim_hist(p, alpha=1.0, N=N)
    t10_alpha = []
    for alpha in ALPHA_VALS:
        r = run_sim_hist(p, alpha=alpha, N=N)
        tw_vs_honest  = ((r['TW_settled']  - base_hist['TW_settled'])  / base_hist['TW_settled']
                         if abs(base_hist['TW_settled'])  > 1e-12 else 0.0)
        net_vs_honest = ((r['Net_settled'] - base_hist['Net_settled']) / base_hist['Net_settled']
                         if abs(base_hist['Net_settled']) > 1e-12 else 0.0)
        eff_rate = r['Net_settled'] / r['TW_settled'] if abs(r['TW_settled']) > 1e-12 else 0.0
        t10_alpha.append({
            'alpha':         alpha,
            'TW':            r['TW_settled'],
            'TTP':           r['TTP'],
            'Net':           r['Net_settled'],
            'eff_rate':      eff_rate,
            'tw_vs_honest':  tw_vs_honest,
            'net_vs_honest': net_vs_honest,
            'g_mean':        r['g_mean'],
        })

    n_traj_vals = sorted({5, 10, 15, 20, 25, 30, N})
    t10_n = []
    for n in n_traj_vals:
        r = run_sim_hist(p, alpha=1.0, N=n)
        t10_n.append({'N': n, 'TW': r['TW_settled'], 'Net': r['Net_settled'], 'g_mean': r['g_mean']})

    # C.11 decomposition
    print("  [tables] C.11 — TW advantage decomposition...")
    c11a = {}; c11b = {}; c11c = {}; c11d = {}; c11e = {}
    max_id_err = 0.0
    for alpha in OVER_VALS:
        ra = []; rb = []; rc = []; rd = []; re = []
        for g in G_VALS:
            d     = decompose_tw_advantage(p, alpha, g, N)
            tw    = d['tw_honest']
            denom = tw if abs(tw) > 1e-12 else 1.0
            ra.append(d['W_sell_delta'] / denom)
            rb.append(d['refund_delta'] / denom)
            rc.append(d['settle_delta'] / denom)
            rd.append(d['tw_advantage'] / denom)
            re.append(d['f_ratio'])
            max_id_err = max(max_id_err, abs(d['identity_error']))
        c11a[_str(alpha)] = ra; c11b[_str(alpha)] = rb; c11c[_str(alpha)] = rc
        c11d[_str(alpha)] = rd; c11e[_str(alpha)] = re

    # C.11.6 excess_periodic (informational)
    sim_p = {k: p[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}
    ep_table = {}
    for alpha in OVER_VALS:
        row = []
        for g in G_VALS:
            g_ser  = [g] * N
            recs_h = simulate(p['V0_m'], g_ser, 1.0, sim_p)
            recs_a = simulate(p['V0_m'], g_ser, alpha, sim_p)
            sell_h = simulate_sell(recs_h, g, sim_p)
            tw_h, _, _ = settle_tw(sell_h, sim_p)
            hn_h = sum(r['L'] for r in recs_h[1:])
            hn_a = sum(r['L'] for r in recs_a[1:])
            denom = tw_h if abs(tw_h) > 1e-12 else 1.0
            row.append((hn_a - hn_h) / denom)
        ep_table[_str(alpha)] = row

    print(f"  [tables] C.11 identity max error: {max_id_err:.2e}")

    return {
        'N': N,
        't1': t1, 't1_tw': t1_tw, 't2': t2, 't3': t3,
        't4': t4, 't5': t5, 't6': t6,
        't7': t7, 't8': t8, 't9': t9,
        't10_alpha': t10_alpha, 't10_n': t10_n,
        'neg_g_vals':   neg_g_vals,
        'neg_g_labels': neg_g_labels,
        'c11a': c11a, 'c11b': c11b, 'c11c': c11c, 'c11d': c11d, 'c11e': c11e,
        'c11_ep': ep_table,
        'c11_max_identity_err': max_id_err,
        'c12': t12,
        'c12_declared_legacy': t12_legacy,   # audit only; superseded
        'metric_notes': {
            't1':    '(Net(a)-Net(1))/TW(1); + = pays more net tax',
            't1_tw': '(TW(a)-TW(1))/TW(1); + = retains more terminal wealth',
            'c12':   '(PVtrue(a)-PVtrue(1))/TW(1); payments valued at true value surrendered',
        },
    }


# ─────────────────────────────────────────────────────────────
# CHARTS DATA (5_4)
# ─────────────────────────────────────────────────────────────

def _pair_matrix(p, alphas, gs, N):
    """[alpha x g] matrices (pp) of net, tw_cost and pv on the common TW(1) denominator."""
    net = []; twc = []; pv = []
    for a in alphas:
        rn = []; rt = []; rp = []
        for g in gs:
            m = run_pair(p, a, g, N)
            rn.append(m['net_pct'] * 100.0)
            rt.append(m['tw_cost'] * 100.0)
            rp.append(m['pv_pct'] * 100.0)
        net.append(rn); twc.append(rt); pv.append(rp)
    return net, twc, pv


def _compute_charts(p: dict, grids: dict) -> dict:
    """
    Compute all series and surfaces needed by 5_4_VAL_charts.py.

    Each figure's data is stored under its function-name key.  Every heatmap
    figure now ships three matrices on the common TW(1) denominator:
    'matrix_net' (fiscal), 'matrix_tw_cost' (taxpayer), 'matrix_pv' (PV of
    true value surrendered).  Legacy keys are retained where the chart script
    reads them ('matrix', 'c1_matrix', 'surfaces').
    """
    N          = p['N_val']
    G_VALS     = grids['g_vals']
    ALPHA_VALS = grids['alpha_vals']
    N_ACTUAL_VALS = grids['n_actual_vals']

    def _str(v): return str(v)

    charts = {}

    # ── fig_5_rate_function ────────────────────────────────────
    print("  [charts] fig 05: rate function τ(W)...")
    charts['fig_5_rate_function'] = _rate_curve(p)

    # ── fig_5_2a_c1_heatmap ───────────────────────────────────
    print("  [charts] fig 5.2a: C.1 heatmap (net | TW | PV)...")
    net_m, twc_m, pv_m = _pair_matrix(p, ALPHA_VALS, G_VALS, N)
    charts['fig_5_2a_c1_heatmap'] = {
        'N': N,
        'matrix':         net_m,       # legacy key: net tax, pp of TW(1)
        'matrix_net':     net_m,
        'matrix_tw_cost': twc_m,
        'matrix_pv':      pv_m,
    }

    # ── fig_7_1b_equilibrium_cost_curve ───────────────────────
    print("  [charts] fig 7.1b: equilibrium cost curve...")
    alpha_fine   = grids['fig_alpha_fine']
    g_scenarios  = [0.059, 0.084, 0.1045, 0.139]
    cost_by_g    = {}          # legacy metric: % of honest Net
    net_pct_by_g = {}          # common metric: % of TW(1)
    tw_cost_by_g = {}
    for g_val in g_scenarios:
        base = run_sim(p, alpha=1.0, g=g_val, N=N)
        diffs = []; npct = []; tcst = []
        for alpha in alpha_fine:
            r = run_sim(p, alpha=alpha, g=g_val, N=N)
            diffs.append((r['Net_settled'] - base['Net_settled']) / base['Net_settled'] * 100
                         if abs(base['Net_settled']) > 1e-12 else 0.0)
            m = run_pair(p, alpha, g_val, N)
            npct.append(m['net_pct'] * 100.0)
            tcst.append(m['tw_cost'] * 100.0)
        cost_by_g[str(g_val)] = diffs
        net_pct_by_g[str(g_val)] = npct
        tw_cost_by_g[str(g_val)] = tcst

    # Historical series version (N explicit; mean_g_hist from the same N slice)
    g_series   = p['returns'][:N]
    mean_g_hist = sum(g_series) / len(g_series)
    base_hist = run_sim_hist(p, alpha=1.0, N=N)
    hist_cost = []; hist_net_pct = []; hist_tw_cost = []
    for alpha in alpha_fine:
        r = run_sim_hist(p, alpha=alpha, N=N)
        hist_cost.append((r['Net_settled'] - base_hist['Net_settled']) / base_hist['Net_settled'] * 100
                         if abs(base_hist['Net_settled']) > 1e-12 else 0.0)
        hist_net_pct.append((r['Net_settled'] - base_hist['Net_settled']) / base_hist['TW_settled'] * 100)
        hist_tw_cost.append((base_hist['TW_settled'] - r['TW_settled']) / base_hist['TW_settled'] * 100)

    charts['fig_7_1b_equilibrium_cost_curve'] = {
        'N':             N,
        'alpha_fine':    alpha_fine,
        'g_scenarios':   g_scenarios,
        'cost_by_g':     cost_by_g,         # legacy: % of honest Net
        'hist_cost':     hist_cost,
        'net_pct_by_g':  net_pct_by_g,      # common metric: % of TW(1)
        'tw_cost_by_g':  tw_cost_by_g,
        'hist_net_pct':  hist_net_pct,
        'hist_tw_cost':  hist_tw_cost,
        'mean_g_hist':   mean_g_hist,
    }

    # ── fig_7_2a_tw_gap_by_n ──────────────────────────────────
    print("  [charts] fig 7.2a: TW gap by N...")
    alpha_under = grids['alpha_under']
    alpha_over  = grids['alpha_over']
    tw_gap_const_under = {}; tw_gap_hist_under = {}
    tw_gap_const_over  = {}; tw_gap_hist_over  = {}
    for alpha in alpha_under + alpha_over:
        c_vals = []; h_vals = []
        for n in N_ACTUAL_VALS:
            r = run_sim(p, alpha=alpha, g=p['g'], N=n)
            b = run_sim(p, alpha=1.0,   g=p['g'], N=n)
            c_vals.append((r['TW_settled'] - b['TW_settled']) / b['TW_settled'] * 100
                          if abs(b['TW_settled']) > 1e-12 else 0.0)
            r2 = run_sim_hist(p, alpha=alpha, N=n)
            b2 = run_sim_hist(p, alpha=1.0,   N=n)
            h_vals.append((r2['TW_settled'] - b2['TW_settled']) / b2['TW_settled'] * 100
                           if abs(b2['TW_settled']) > 1e-12 else 0.0)
        if alpha in alpha_under:
            tw_gap_const_under[_str(alpha)] = c_vals
            tw_gap_hist_under[_str(alpha)]  = h_vals
        else:
            tw_gap_const_over[_str(alpha)] = c_vals
            tw_gap_hist_over[_str(alpha)]  = h_vals

    charts['fig_7_2a_tw_gap_by_n'] = {
        'N': 'grid',
        'n_vals': N_ACTUAL_VALS,
        'const_under': tw_gap_const_under, 'hist_under': tw_gap_hist_under,
        'const_over':  tw_gap_const_over,  'hist_over':  tw_gap_hist_over,
    }

    # ── fig_7_2b_saturation_reversal (understater C.1 vs g) ───
    print("  [charts] fig 7.2b: saturation/reversal...")
    g_fine    = grids['fig_g_fine']
    g_pct_fine = [g * 100 for g in g_fine]
    c1_curves = {}; tw_curves = {}
    for alpha in alpha_under:
        vals = []; tvals = []
        for g in g_fine:
            m = run_pair(p, alpha, g, N)
            vals.append(m['net_pct'] * 100.0)
            tvals.append(m['tw_cost'] * 100.0)
        c1_curves[_str(alpha)] = vals
        tw_curves[_str(alpha)] = tvals
    charts['fig_7_2b_saturation_reversal'] = {
        'N': N,
        'g_pct': g_pct_fine,
        'c1_curves': c1_curves,
        'tw_cost_curves': tw_curves,
    }

    # ── fig_7_2c_overstatement_reversal ───────────────────────
    print("  [charts] fig 7.2c: overstatement reversal...")
    g_fine_400 = grids['fig_g_fine_400']
    g_pct_400  = [g * 100 for g in g_fine_400]
    c1_curves_over = {}; tw_curves_over = {}
    for alpha in alpha_over:
        vals = []; tvals = []
        for g in g_fine_400:
            m = run_pair(p, alpha, g, N)
            vals.append(m['net_pct'] * 100.0)
            tvals.append(m['tw_cost'] * 100.0)
        c1_curves_over[_str(alpha)] = vals
        tw_curves_over[_str(alpha)] = tvals
    charts['fig_7_2c_overstatement_reversal'] = {
        'N': N,
        'g_pct': g_pct_400,
        'c1_curves': c1_curves_over,
        'tw_cost_curves': tw_curves_over,
    }

    # ── fig_7_1a_overstatement_coherence ──────────────────────
    print("  [charts] fig 7.1a: overstatement coherence (net | TW heatmaps + N-series)...")
    hist_mean = p['g']
    alphas_grid = np.linspace(0.1, 2.0, 41).tolist()
    g_grid      = np.linspace(0.0, 0.40, 101).tolist()
    left_net, left_twc, left_pv = _pair_matrix(p, alphas_grid, g_grid, N)
    n_right   = list(range(5, 61))
    net_diffs_right = {}
    for alpha in [1.2, 1.5, 1.8, 2.0]:
        diffs = []
        for n in n_right:
            r = run_sim(p, alpha=alpha, g=hist_mean, N=n)
            b = run_sim(p, alpha=1.0,   g=hist_mean, N=n)
            diffs.append(r['Net_settled'] - b['Net_settled'])
        net_diffs_right[_str(alpha)] = diffs
    charts['fig_7_1a_overstatement_coherence'] = {
        'N':              N,
        'alphas_grid':    alphas_grid,
        'g_grid':         g_grid,
        'c1_matrix':      left_net,        # legacy key: net tax, pp of TW(1)
        'matrix_net':     left_net,
        'matrix_tw_cost': left_twc,
        'matrix_pv':      left_pv,
        'n_right':        n_right,
        'net_diffs':      net_diffs_right,  # £m, [alpha → list by N]
        'hist_mean':      hist_mean,
        'N_ssm':          p['N_fill'],      # reference line only (fund mechanics)
        'N_fill':         p['N_fill'],
        'N_val':          N,
    }

    # ── fig_5_2b_tw_decomposition ─────────────────────────────
    print("  [charts] fig 5.2b: TW decomposition...")
    alpha_over_fine = grids['fig_alpha_over']
    g_decomp        = grids['fig_g_decomp']
    wsd_v = []; rd_v = []; sd_v = []; tw_v = []; ep_v = []
    for alpha in alpha_over_fine:
        d     = decompose_tw_advantage(p, alpha, hist_mean, N)
        denom = d['tw_honest'] if abs(d['tw_honest']) > 1e-12 else 1.0
        wsd_v.append(d['W_sell_delta'] / denom * 100)
        rd_v.append(d['refund_delta']  / denom * 100)
        sd_v.append(d['settle_delta']  / denom * 100)
        tw_v.append(d['tw_advantage']  / denom * 100)
        ep_v.append(d['excess_periodic'] / denom * 100)
    f_matrix = []
    for alpha in alpha_over_fine:
        row = []
        for g in g_decomp:
            d = decompose_tw_advantage(p, alpha, g, N)
            row.append(d['f_ratio'])
        f_matrix.append(row)
    charts['fig_5_2b_tw_decomposition'] = {
        'N': N,
        'alpha_over_fine': alpha_over_fine,
        'g_decomp':        g_decomp,
        'wsd':  wsd_v, 'rd':  rd_v, 'sd':  sd_v,
        'tw':   tw_v,  'ep':  ep_v,
        'f_matrix': f_matrix,          # [alpha × g]
    }

    # ── fig_7_1c_tw_advantage_gN_surface ──────────────────────
    print("  [charts] fig 7.1c: (g, N) surfaces — TW, net tax, PV (this takes a while)...")
    g_surf = grids['fig_g_surface']
    n_surf = grids['fig_n_surface']
    surfaces = {}; surfaces_net = {}; surfaces_pv = {}
    for alpha in [1.2, 1.5, 1.8, 2.0]:
        mat_tw = []; mat_net = []; mat_pv = []
        for g in g_surf:
            r_tw = []; r_net = []; r_pv = []
            for n in n_surf:
                m = run_pair(p, alpha, g, n)
                r_tw.append(m['tw_gap'] * 100.0)     # legacy: + = retains more
                r_net.append(m['net_pct'] * 100.0)   # + = pays more
                r_pv.append(m['pv_pct'] * 100.0)
            mat_tw.append(r_tw); mat_net.append(r_net); mat_pv.append(r_pv)
        surfaces[_str(alpha)]     = mat_tw           # [g × N]
        surfaces_net[_str(alpha)] = mat_net
        surfaces_pv[_str(alpha)]  = mat_pv

    charts['fig_7_1c_tw_advantage_gN_surface'] = {
        'N': 'grid', 'N_canonical': N,
        'g_surf':    g_surf,
        'n_surf':    n_surf,
        'surfaces':  surfaces,          # TW gap (+ = retains more)
        'surfaces_net': surfaces_net,   # net tax gap (+ = pays more)
        'surfaces_pv':  surfaces_pv,    # PV of true value surrendered gap
    }

    # ── fig_7_1d_c1_vs_c12_heatmap ────────────────────────────
    print("  [charts] fig 7.1d: net | TW | PV heatmaps...")
    leg = []
    for alpha in ALPHA_VALS:
        leg.append([run_pair(p, alpha, g, N)['pv_declared_pct'] * 100.0 for g in G_VALS])
    charts['fig_7_1d_c12_heatmap'] = {
        'N': N,
        'matrix':         pv_m,          # legacy key, now the CORRECTED C.12 (pp of TW(1))
        'matrix_net':     net_m,         # C.1 on TW(1)
        'matrix_tw_cost': twc_m,
        'matrix_pv':      pv_m,
        'matrix_c12_declared_legacy': leg,   # audit only
        'rho':    p['rho'],
    }

    return charts


# ─────────────────────────────────────────────────────────────
# WORKED EXAMPLES DATA (5_5)
# ─────────────────────────────────────────────────────────────

def _compute_examples(p: dict) -> dict:
    """
    Compute all data for 5_5_VAL_generate_worked_examples.py (§J–§N).
    Each example carries its own explicit N.
    """

    def _records_to_list(records):
        return [dict(r) for r in records]

    def _sell_to_dict(sell):
        return dict(sell)

    examples = {}

    # ── §J: Deferred delta ────────────────────────────────────
    print("  [examples] §J: deferred delta...")
    j_p = dict(p); j_p['g'] = 0.07; j_p['V0_m'] = 20.0
    j_alphas = [1.0, 0.8, 0.5]
    j_results = {}
    for alpha in j_alphas:
        r = run_sim(j_p, alpha=alpha, g=0.07, N=5)
        j_results[str(alpha)] = {
            'TW_settled':   r['TW_settled'],
            'Net_settled':  r['Net_settled'],
            'records':      _records_to_list(r['records']),
            'sell':         _sell_to_dict(r['sell']),
        }
    examples['J'] = {'alphas': j_alphas, 'results': j_results, 'g': 0.07, 'N': 5, 'V0_m': 20.0}

    # ── §K: Dilution compounds with growth ────────────────────
    print("  [examples] §K: dilution compounds...")
    k_p = dict(p); k_p['g'] = 0.15; k_p['V0_m'] = 20.0
    k_alphas = [1.0, 0.6]
    k_results = {}
    for alpha in k_alphas:
        r = run_sim(k_p, alpha=alpha, g=0.15, N=3)
        k_results[str(alpha)] = {
            'TW_settled':  r['TW_settled'],
            'Net_settled': r['Net_settled'],
            'records':     _records_to_list(r['records']),
            'sell':        _sell_to_dict(r['sell']),
        }
    examples['K'] = {'alphas': k_alphas, 'results': k_results, 'g': 0.15, 'N': 3, 'V0_m': 20.0}

    # ── §L: Route D vs annual ─────────────────────────────────
    print("  [examples] §L: Route D vs annual...")
    sim_p = {k: p[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}
    V0_l = 8.0; g_l = 0.05; N_annual = 5; N_route_d = 15
    annual_rows = []
    V_prev = V0_l; cum_liab = 0.0
    for yr in range(1, N_annual + 1):
        V = V_prev * (1.0 + g_l)
        delta = V - V_prev
        rate  = tau(V, sim_p)
        liab  = rate * delta
        cum_liab += liab
        annual_rows.append({'yr': yr, 'V': V, 'liab': liab, 'cum_liab': cum_liab})
        V_prev = V
    V15    = V0_l * (1.0 + g_l) ** N_route_d
    rate15 = tau(V15, sim_p)
    liab15 = rate15 * (V15 - V0_l)
    examples['L'] = {
        'V0': V0_l, 'g': g_l, 'N_annual': N_annual, 'N_route_d': N_route_d,
        'annual_rows': annual_rows, 'cum_liab': cum_liab,
        'V15': V15, 'rate15': rate15, 'liab15': liab15,
    }

    # ── §M: Voluntary settlement ──────────────────────────────
    print("  [examples] §M: voluntary settlement...")
    B0 = 5.0; g_m = 0.05; N_reset = 10; N_death = 15
    V10 = B0 * (1.0 + g_m) ** N_reset
    V15_m = B0 * (1.0 + g_m) ** N_death
    V10_soft = V10 * 0.944
    gain_soft  = V10_soft - B0
    rate_soft  = tau(V10_soft, sim_p)
    liab_soft  = rate_soft * gain_soft
    gain_hard  = V10 - B0
    rate_hard  = tau(V10, sim_p)
    liab_hard  = rate_hard * gain_hard
    auction_cost = V10 * 0.02
    gain_death = V15_m - B0
    rate_death = tau(V15_m, sim_p)
    liab_death = rate_death * gain_death
    examples['M'] = {
        'B0': B0, 'g': g_m, 'N_reset': N_reset, 'N_death': N_death,
        'V10': V10, 'V15': V15_m, 'V10_soft': V10_soft,
        'soft': {'gain': gain_soft, 'rate': rate_soft, 'liab': liab_soft},
        'hard': {'gain': gain_hard, 'rate': rate_hard, 'liab': liab_hard, 'auction_cost': auction_cost},
        'death': {'gain': gain_death, 'rate': rate_death, 'liab': liab_death},
    }

    # ── §N: Forecast exposure ─────────────────────────────────
    print("  [examples] §N: forecast exposure...")
    n_p = dict(p); n_p['V0_m'] = 8.0; n_p['g'] = 0.07
    n_alphas = [1.0, 0.6, 1.4]
    n_results = {}
    for alpha in n_alphas:
        r = run_sim(n_p, alpha=alpha, g=0.07, N=10)
        n_results[str(alpha)] = {
            'TW_settled':  r['TW_settled'],
            'Net_settled': r['Net_settled'],
            'TTP':         r['TTP'],
            'Refunds':     r['Refunds'],
            'records':     _records_to_list(r['records']),
            'sell':        _sell_to_dict(r['sell']),
        }
    examples['N'] = {'alphas': n_alphas, 'results': n_results, 'g': 0.07, 'N': 10, 'V0_m': 8.0}

    return examples


# ─────────────────────────────────────────────────────────────
# VALIDATION HARNESS
# ─────────────────────────────────────────────────────────────

def _validate(p: dict, grids: dict, tables: dict, charts: dict) -> dict:
    """
    Fail the run if N stamps or internal cross-checks are wrong.
    Returns a report dict (stored in meta['validation']).
    """
    N = p['N_val']
    G_VALS     = grids['g_vals']
    ALPHA_VALS = grids['alpha_vals']
    OVER_VALS  = grids['over_vals']
    K_VALS     = grids['k_vals']
    NA         = grids['n_actual_vals']
    report = {'N_val': N, 'N_fill': p['N_fill'], 'checks': {}}

    def check(name, ok, detail=''):
        report['checks'][name] = {'ok': bool(ok), 'detail': detail}
        if not ok:
            raise AssertionError(f"VALIDATION FAILED: {name} {detail}")

    # 1. N stamps
    check('tables_N_stamp', tables['N'] == N, f"tables N={tables['N']}")
    for name, fig in charts.items():
        if 'N' not in fig:
            continue                       # rate curve etc.
        if fig['N'] == 'grid':
            continue
        check(f'chart_N_stamp:{name}', fig['N'] == N, f"{name} N={fig['N']}")

    # 2. C.11.4 == C.8 at N_val (same sims; should agree to machine precision)
    ig = G_VALS.index(p['g']) if p['g'] in G_VALS else None
    inn = NA.index(N)
    if ig is not None:
        worst = 0.0
        for a in OVER_VALS:
            worst = max(worst, abs(tables['c11d'][str(a)][ig] - tables['t8'][str(a)][inn]))
        check('C11.4_equals_C8', worst < 1e-9, f'max|diff|={worst:.2e}')

    # 3. C.5 at canonical k == C.8 at N_val
    ik = K_VALS.index(p['k'])
    worst = 0.0
    for a in ALPHA_VALS:
        worst = max(worst, abs(tables['t5'][str(a)][ik] - tables['t8'][str(a)][inn]))
    check('C5_equals_C8', worst < 1e-9, f'max|diff|={worst:.2e}')

    # 4. C.11 identity
    check('C11_identity', tables['c11_max_identity_err'] < 1e-9,
          f"max err={tables['c11_max_identity_err']:.2e}")

    # 5. C.10.1 honest == C.10.2 row at N_val
    hon = [r for r in tables['t10_alpha'] if r['alpha'] == 1.0][0]['TW']
    row = [r for r in tables['t10_n'] if r['N'] == N][0]['TW']
    check('C10_1_equals_C10_2', abs(hon - row) < 1e-9, f'{hon:.4f} vs {row:.4f}')

    # 6. Honest row is zero in every common-denominator table
    for key in ('t1', 't1_tw', 'c12'):
        check(f'{key}_honest_row_zero',
              max(abs(x) for x in tables[key]['1.0']) < 1e-12)

    # 7. C.1 (net) at N_val equals direct recomputation with TW(1) denominator
    worst = 0.0
    for a in (0.5, 1.5):
        for j, g in enumerate(G_VALS):
            r = run_sim(p, alpha=a, beta=0.0, g=g, N=N)
            b = run_sim(p, alpha=1.0, beta=0.0, g=g, N=N)
            direct = (r['Net_settled'] - b['Net_settled']) / b['TW_settled']
            worst = max(worst, abs(direct - tables['t1'][str(a)][j]))
    check('C1_matches_direct_TW1_denominator', worst < 1e-9, f'max|diff|={worst:.2e}')

    # 8. In-kind identity: (f_{t-1} - f_t) * V_t == L_t / alpha
    sim_p = {k: p[k] for k in ('k', 'tau_0', 'tau_m', 'W_min')}
    worst = 0.0
    for a in ALPHA_VALS:
        for g in G_VALS:
            recs = simulate(p['V0_m'], [g] * N, a, sim_p)
            for i in range(1, len(recs)):
                lhs = (recs[i - 1]['f'] - recs[i]['f']) * recs[i]['V']
                rhs = recs[i]['L'] / a
                worst = max(worst, abs(lhs - rhs))
    check('in_kind_payment_identity', worst < 1e-8, f'max|diff|={worst:.2e}')

    # 9. Sign agreement: corrected PV vs TW-cost, and legacy for contrast
    def sign_disagree(pv_tab):
        bad = 0; tot = 0
        for a in ALPHA_VALS:
            if a == 1.0:
                continue
            for j, g in enumerate(G_VALS):
                pv  = pv_tab[str(a)][j]
                twc = -tables['t1_tw'][str(a)][j]        # + = worse off
                if abs(pv) < 1e-4 or abs(twc) < 1e-4:
                    continue
                tot += 1
                bad += (pv > 0) != (twc > 0)
        return bad, tot
    b_new, t_new = sign_disagree(tables['c12'])
    b_old, t_old = sign_disagree(tables['c12_declared_legacy'])
    report['sign_agreement'] = {
        'corrected_C12_vs_TW': {'disagree': b_new, 'cells': t_new},
        'legacy_C12_vs_TW':    {'disagree': b_old, 'cells': t_old},
    }
    report['ok'] = True
    return report


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

def main(dry_run: bool = False):
    print("val_core.py — VAL simulation runner")
    print("=" * 50)
    p = load_params()
    print(f"Parameters: k={p['k']}, tau_0={p['tau_0']}, tau_m={p['tau_m']}, "
          f"W_min=£{p['W_min']}m, N_val={p['N_val']} (canonical), "
          f"N_fill={p['N_fill']} (SSM, fund mechanics only), g={p['g']:.4f}")

    grids = _build_grids(p)
    print(f"\nGrids: {len(grids['g_vals'])} g-vals, {len(grids['alpha_vals'])} alpha-vals, "
          f"{len(grids['k_vals'])} k-vals, {len(grids['v0_vals'])} V0-vals, "
          f"{len(grids['n_actual_vals'])} N-vals")

    if dry_run:
        print("\nDry run — skipping simulations.")
        return

    print("\n[1/4] Computing table data (C.1–C.12)...")
    tables = _compute_tables(p, grids)

    print("\n[2/4] Computing chart data...")
    charts = _compute_charts(p, grids)

    print("\n[3/4] Computing worked-example data (§J–§N)...")
    examples = _compute_examples(p)

    print("\n[4/4] Validating...")
    validation = _validate(p, grids, tables, charts)
    for name, c in validation['checks'].items():
        print(f"  PASS  {name} {c['detail']}")
    sa = validation['sign_agreement']
    print(f"  INFO  sign agreement corrected C.12 vs TW: "
          f"{sa['corrected_C12_vs_TW']['disagree']}/{sa['corrected_C12_vs_TW']['cells']} disagree; "
          f"legacy: {sa['legacy_C12_vs_TW']['disagree']}/{sa['legacy_C12_vs_TW']['cells']}")

    meta = {
        'generated':    date.today().isoformat(),
        'model':        'Python v1.1 standalone · Route C simulation throughout',
        'convention':   'TW_settled / Net_settled; common TW(1) denominator; explicit N',
        'params': {
            'tau_0':  p['tau_0'],  'tau_m':  p['tau_m'],
            'k':      p['k'],      'W_min':  p['W_min'],
            'N':      p['N_val'],  'N_val':  p['N_val'], 'N_fill': p['N_fill'],
            'N_demo': p['N_demo'],
            'V0_m':   p['V0_m'],   'g':      p['g'],
            'rho':    p['rho'],
        },
        'scenario_start_year': p['scenario_start_year'],
        'validation': validation,
    }

    val_data = {
        'meta':     meta,
        'params':   meta['params'],
        'grids':    grids,
        'tables':   tables,
        'charts':   charts,
        'examples': examples,
    }

    ensure_dir(_OUT)
    safe = _to_json_safe(val_data)
    with open(_JSON_PATH, 'w', encoding='utf-8') as fh:
        json.dump(safe, fh, indent=2, allow_nan=False)

    size_kb = _JSON_PATH.stat().st_size / 1024
    print(f"\nWritten: {_JSON_PATH}")
    print(f"Size:    {size_kb:.0f} KB")
    print("Done. Run 5_3, 5_4, 5_5 to generate outputs.")


if __name__ == '__main__':
    dry = '--dry-run' in sys.argv
    main(dry_run=dry)
