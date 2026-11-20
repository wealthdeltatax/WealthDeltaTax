"""
groups.py -- the output groups, named in one place (model v3, brief 084c)
========================================================================
Layer between core and runner.py (conftest LAYER). Each group is a module with NAME (its key in an evaluation), IDS (the manifest ids it fills),
`per_path(raw, again)` (raw core results of runner.Raw in, a nested dict of per-path arrays out) and `cells(e)` (that dict of one schedule in,
{output id: {(horizon, by, line): array}} out). Imported explicitly: no discovery, no silent skip. A new group is one line here.
"""

from model_v3.runner import out_burden, out_revenue, out_support, out_sweeps

GROUPS = (out_revenue, out_burden, out_support, out_sweeps)
