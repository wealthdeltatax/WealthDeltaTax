"""
out_burden.py -- output group: burden, non-payer savings and the comparators (stub, filled by brief 086c)
=========================================================================================================
Interface: see groups.py. An empty group changes no number.
"""

NAME = 'burden'
IDS = ()


def per_path(raw, env, again):
    """Per-path arrays from the raw core results of runner.Raw; `env` and `again(override, full=False)` reruns the core with the spec changed."""
    return {}


def cells(e):
    """{output id: {(horizon, by, line): array}} from this group's per-path results of one schedule."""
    return {}
