"""
rates_s_helpers.py — Shared helpers for RATES.S output scripts
===============================================================
Single source of truth for path resolution, statistical helpers,
sweep execution, and formatting shared across:

  16_6  RATES_S_tables.py
  16_7  RATES_S_charts.py

Import everything needed with:
    from rates_s_helpers import *
"""

import sys
import math
from pathlib import Path
from copy import deepcopy

# ─────────────────────────────────────────────────────────────
# PATH RESOLUTION — locate rates_model.py regardless of cwd
# ─────────────────────────────────────────────────────────────

_SCRIPT_DIR = Path(__file__).parent


def _find_project_dir():
    for c in [_SCRIPT_DIR, _SCRIPT_DIR.parent, Path('/mnt/project'), Path.cwd()]:
        if (c / 'rates_model.py').exists():
            return c
    raise FileNotFoundError(
        "Cannot locate rates_model.py. "
        "Run with PYTHONPATH set, or place this script alongside rates_model.py."
    )


def _find_params_toml(project_dir):
    for name in ['260812_WDT_Params.toml']:
        p = project_dir / name
        if p.exists():
            return p
    hits = list(project_dir.glob('*Rates_and_Revenue_Params.toml'))
    if hits:
        return hits[0]
    raise FileNotFoundError(
        f"Cannot find WDT_Params.toml in {project_dir}"
    )


PROJECT_DIR    = _find_project_dir()
DEFAULT_PARAMS = _find_params_toml(PROJECT_DIR)

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import rates_model as model

# Shared output directories
OUT_DIR_TABLES = _SCRIPT_DIR / 'OUTPUTS' / 'RATES_S'
OUT_DIR_CHARTS = _SCRIPT_DIR / 'OUTPUTS' / 'RATES_S'


# ─────────────────────────────────────────────────────────────
# STATISTICAL HELPERS
# These duplicate _median/_mean/_success from rates_model but are
# kept here so RATES.S scripts have a single local import; rates_model
# versions are private (_-prefixed) to that module's internal API.
# ─────────────────────────────────────────────────────────────

def median(vals):
    s = sorted(v for v in vals if v is not None)
    if not s:
        return None
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def mean(vals):
    v = [x for x in vals if x is not None]
    return sum(v) / len(v) if v else None


def success(r):
    """Mirror of rates_model._success."""
    if r['lrr_fill_year'] is None:
        return False
    return r['srr_breach_year'] is None or r['srr_breach_covered'] is True


def summarise(sweep_results):
    """
    Summarise a run_start_year_sweep() result list.

    Returns a dict with keys:
      n_total, success_rate,
      ssm_cov / tcm_cov / lrr_fill / srr_fill / lrr_surplus
        — each a {min, median, mean, max, n} dict,
      worst_case_2006 — the row for calendar_year == 2006, or None.
    """
    n_total   = len(sweep_results)
    n_success = sum(1 for r in sweep_results if success(r))

    def _dist(key):
        vals = [r[key] for r in sweep_results if r.get(key) is not None]
        if not vals:
            return {'min': None, 'median': None, 'mean': None, 'max': None, 'n': 0}
        return {
            'min':    min(vals),
            'median': median(vals),
            'mean':   mean(vals),
            'max':    max(vals),
            'n':      len(vals),
        }

    wc = next((r for r in sweep_results if r['calendar_year'] == 2006), None)

    return {
        'n_total':         n_total,
        'success_rate':    100.0 * n_success / n_total if n_total else 0.0,
        'ssm_cov':         _dist('ssm_post_fill_coverage'),
        'tcm_cov':         _dist('tcm_post_fill_coverage'),
        'lrr_fill':        _dist('lrr_fill_year'),
        'srr_fill':        _dist('srr_fill_year'),
        'lrr_surplus':     _dist('lrr_surplus_at_fill'),
        'worst_case_2006': wc,
    }


# ─────────────────────────────────────────────────────────────
# SWEEP RUNNER
# Unified version: takes an optional label (used by tables script for
# skip_reason messages); always includes all guards from both originals.
# ─────────────────────────────────────────────────────────────

def run_param_sweep(p_base, param_name, values, label=None):
    """
    Run model.run_start_year_sweep() for each value in `values`,
    overriding p_base[param_name] each time.

    Returns a list of dicts — one per value:
      {
        'value':       float,
        'label':       str | None,
        'summary':     dict | None,
        'skipped':     bool,
        'skip_reason': str | None,
      }
    """
    if label is None:
        label = param_name
    results = []
    for v in values:
        p = deepcopy(p_base)
        p[param_name] = v

        def _skip(reason):
            results.append({
                'value': v, 'label': label,
                'summary': None, 'skipped': True,
                'skip_reason': reason,
            })
            print(f"  [{label}={v:.5g}]  SKIPPED ({reason})")

        if p['tau_0'] >= p['tau_m']:
            _skip(f"τ_0={p['tau_0']:.2f} >= τ_m={p['tau_m']:.2f}")
            continue
        if p['W_min'] < 0:
            _skip(f"W_min={p['W_min']} < 0")
            continue
        if p['srr_ratio'] <= 0:
            _skip(f"srr_ratio={p['srr_ratio']} <= 0")
            continue
        if p['lrr_years'] <= 0:
            _skip(f"lrr_years={p['lrr_years']} <= 0")
            continue

        print(f"  [{label}={v:.5g}]  sweeping...", end='', flush=True)
        sweep = model.run_start_year_sweep(p)
        s = summarise(sweep)
        results.append({
            'value': v, 'label': label,
            'summary': s, 'skipped': False, 'skip_reason': None,
        })
        print(f"  done  success={s['success_rate']:.0f}%  "
              f"TCM_med={fmt_pct(s['tcm_cov']['median'])}  "
              f"LRR_med={s['lrr_fill']['median']}")

    return results


# ─────────────────────────────────────────────────────────────
# FORMATTING HELPERS
# ─────────────────────────────────────────────────────────────

def fmt_pct(v, decimals=1):
    if v is None:
        return '—'
    return f'{v * 100:.{decimals}f}%'


def fmt_f(v, fmt='.1f'):
    if v is None:
        return '—'
    return f'{v:{fmt}}'


def baseline_marker(v, baseline_v, tol=1e-9):
    return ' ◄' if abs(v - baseline_v) < tol else ''


def dist_row(d, fmt_fn):
    """Format a distribution dict as min/median/mean/max string."""
    return (f"{fmt_fn(d['min'])} / {fmt_fn(d['median'])} / "
            f"{fmt_fn(d['mean'])} / {fmt_fn(d['max'])}")
