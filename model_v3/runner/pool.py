"""
pool.py -- an ordered map over worker processes (model v3, brief 150c)
======================================================================
Layer L3.8 (below sweeps.py and runner.py, which call it). `pmap(f, items, workers)` is `[f(x) for x in items]`, in the order of `items`. `workers` 1 (the default) runs the plain loop in this process, no pool;
`workers` N > 1 runs the units in N forked processes; `workers` 0 means one per core (`os.cpu_count()`). Nothing is read at import (R8).

Same results, serial or parallel: a unit must be a pure function of its item. The evaluator is (`runner.make_ev`): the seed streams are SeedSequences keyed by the
run, the chunk or the draw, never advanced, so no unit sees another's state, and the results are the same to the last digit whatever the order or the worker count.
Units arrive and return by pickle (small: a spec, a float, one evaluation's arrays); `f` itself does not, because it is a closure over the evaluator: the pool forks
after `f` is set in a module global and the workers inherit it. Forking is the one start method used (Linux, macOS); where it is absent the loop runs serially.
Units are handed out one at a time (chunksize 1), so a cheap unit (a root with no sign change, 2 evaluations) does not wait behind a dear one (about 12). An exception
in a unit is raised here, as the serial loop would raise it. Memory: each worker holds its own evaluation (about 2 GB at 1,000 paths): the worker count is the caller's choice.
"""

from __future__ import annotations

import multiprocessing as mp
import os
from concurrent.futures import ProcessPoolExecutor

_F = None


def _call(x):
    return _F(x)


def n_workers(workers):
    """The worker count for the switch: None or 1 is serial, 0 is one per core, N is N."""
    return 1 if workers is None else (os.cpu_count() or 1) if workers == 0 else max(1, int(workers))


def pmap(f, items, workers=1):
    global _F
    items, w = list(items), n_workers(workers)
    if w <= 1 or len(items) <= 1 or 'fork' not in mp.get_all_start_methods():
        return [f(x) for x in items]
    _F = f
    try:
        with ProcessPoolExecutor(min(w, len(items)), mp_context=mp.get_context('fork')) as ex:
            return list(ex.map(_call, items, chunksize=1))
    finally:
        _F = None
