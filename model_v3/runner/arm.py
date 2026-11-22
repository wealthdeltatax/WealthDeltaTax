"""
arm.py -- the hooks that carry the household's year through the kernel's five sites (model v3, brief 114c, kernel-wiring-design 3.2 and 3.6)
============================================================================================================================================
Layer 3.6: numpy only; the runner builds a hook and passes it down through revenue.run_lines, burden.line_flows and support.wdt_run in the place of `c`.
A hook has `pre(book, t, g) -> (g_N, x)` (the growth rate and the signed flow share of the year: legacy returns g and -c), `post(book, fl)` (after
settlement) and one method for each site that read `c`: `grown` (revenue.run_lines, wealth after growth and flow), `gain` (revenue.identity, the accrued gain
rate) and `free` (burden.free_path, the untaxed growth factor). `LegacyHook(c)` does exactly what `c` did, operation for operation (bit equal);
the comparators' `support.system_run` stay legacy in this wiring (design 3.6, site 5).
"""

import numpy as np


class LegacyHook:
    """The legacy arm: every class grows at g, then a share c is consumed, W(1 + g)(1 - c)."""

    def __init__(self, c):
        self.c = c

    def pre(self, book, t, g):
        return g, -self.c

    def post(self, book, fl):
        """Nothing after settlement."""

    def grown(self, W0, g):
        return W0 * (1.0 + g) * (1.0 - self.c)

    def gain(self, g):
        return np.maximum((1.0 + g) * (1.0 - self.c) - 1.0, 0.0)

    def free(self, g):
        return (1.0 + g) * (1.0 - self.c)
