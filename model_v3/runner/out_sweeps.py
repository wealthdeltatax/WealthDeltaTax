"""
out_sweeps.py -- output group: the sweep-owned ids (stub, filled by brief 088c)
===============================================================================
Interface: see groups.py. An empty group changes no number.
"""

NAME = 'sweeps'
IDS = ()


def per_path(raw, again):
    """Per-path arrays from the raw core results of runner.Raw; `again(override)` reruns the core with the spec changed."""
    return {}


def cells(e):
    """{output id: {(horizon, by, line): array}} from this group's per-path results of one schedule."""
    return {}
