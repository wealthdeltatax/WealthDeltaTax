"""
groups.py -- the output groups, named in one place (model v3, brief 084c)
========================================================================
Layer between core and runner.py (conftest LAYER). Each group is a module with NAME (its key in an evaluation), IDS (the manifest ids it fills),
`per_path(raw, env, again)` (raw core results of runner.Raw and the runner's Env in, a nested dict of per-path arrays out; `again(over, full=False)` reruns the core) and `cells(e)` (that dict of one schedule in,
{output id: {(horizon, by, line): array}} out). A group may also define `static(env)`, the same shape for outputs that depend on neither paths nor schedules (the manifest's
`once_not_per_schedule`); `samples` stores them with schedule None. Imported explicitly: no discovery, no silent skip. A new group is one line here.
"""

from model_v3.runner import out_burden, out_revenue, out_support, out_sweeps

GROUPS = (out_revenue, out_burden, out_support, out_sweeps)
