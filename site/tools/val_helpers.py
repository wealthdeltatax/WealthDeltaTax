"""
val_helpers.py — Shared helpers for VAL output scripts
=======================================================
Formatting utilities and output path resolution shared across:

  5_3  VAL_generate_appc_full.py
  5_4  VAL_generate_worked_examples.py
  5_5  VAL_generate_illustrative.py
  5_6  VAL_generate_figures.py

Import with:
    from val_helpers import OUT_DIR, fm, fp, pct_str, eff_rate
"""

import os
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# OUTPUT DIRECTORY — portable, relative to this file
# ─────────────────────────────────────────────────────────────

OUT_DIR = str(Path(__file__).parent / 'OUTPUTS' / 'VAL')


# ─────────────────────────────────────────────────────────────
# FORMATTING HELPERS
# ─────────────────────────────────────────────────────────────

def fm(v, dp=3):
    """Format a £m value: £{v:.{dp}f}m"""
    return f'£{v:.{dp}f}m'


def fp(v, dp=2):
    """Format as a percentage string: {v*100:.{dp}f}%"""
    return f'{v * 100:.{dp}f}%'


def pct_str(v, decimals=2):
    """Format a fraction as a percentage string (alias of fp with named arg)."""
    return f'{v * 100:.{decimals}f}%'


def eff_rate(r):
    """Effective lifetime tax rate = Net / TW."""
    return r['Net'] / r['TW'] if abs(r['TW']) > 1e-12 else 0.0


def fmt_val(v, as_pct=True, decimals=2):
    if as_pct:
        return pct_str(v, decimals)
    return f'{v:.{decimals}f}'


def md_table(headers, rows, fmt_fn=None):
    """
    Generate a markdown table string.
    fmt_fn(val) -> str is applied to all data cells (col 1 onward).
    The first column of each row is treated as a label and left as-is.
    """
    if fmt_fn is None:
        fmt_fn = pct_str
    lines = []
    lines.append('| ' + ' | '.join(str(h) for h in headers) + ' |')
    lines.append('|' + '|'.join(':---:' for _ in headers) + '|')
    for row in rows:
        cells = [str(row[0])] + [fmt_fn(v) for v in row[1:]]
        lines.append('| ' + ' | '.join(cells) + ' |')
    return '\n'.join(lines)
