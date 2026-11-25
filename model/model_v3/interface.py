"""The contract between the runner and the output layer (architecture.md 2.9). Fixed; a build brief never edits it.

Samples maps an output id to arrays keyed by (schedule, horizon, by, line):
  schedule  a schedule name, or None for an output reported once and not per schedule
  horizon   one of the manifest horizons, or 'single'
  by        a sorted tuple of (dimension, value) pairs; () when the output has no dimension
  line      None, or a metric id for an output with several lines
Each array holds one entry per level 1 path (for level 2 results, one entry per draw).
Level2 holds, for one output, the tornado rows and the level 2 P10 and P90 of the level 1 mean (hooks.md 3.3, form C).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

Key = tuple  # (schedule | None, horizon, by, line | None)
Samples = dict  # output id -> {Key: np.ndarray}


@dataclass(frozen=True)
class TornadoRow:
    input: str          # a register id
    low_effect: float   # change in the output when the input is at its low value
    high_effect: float  # change in the output when the input is at its high value


@dataclass(frozen=True)
class Level2:
    tornado: tuple      # TornadoRow items, descending by absolute effect
    p10: float
    p90: float


Results = tuple  # (Samples, {output id: Level2})
