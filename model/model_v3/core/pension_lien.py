"""Brief 132c: the pension-secured lien, pure functions (layer 1, numpy only).

The part of a year's WDT that a line's non-pension classes cannot pay is not sold from the pension in life: it becomes a deferred balance PL against the pension (the Route B lien's rule: it accrues at the kernel's
`r_def` and is settled at death and at the horizon). The kernel's family value is net of PL (declared wealth is net of the lien, as for LB). Settlement pays PL first from the positive non-pension classes pro rata
(never beyond their net total), then, for the remainder, by a one-off draw on the pension, capped at the pension balance less the heir's share `keep` (148c, a fraction; 0 is the uncapped draw); what is still unpaid is returned as `rest`, a model alarm (expected zero).
Arrays are per line; `q` is a dict of the non-pension class balances.
"""
import numpy as np


def accrue(PL, r):
    """The balance after a year at the deferral rate r."""
    return np.asarray(PL, float) * (1.0 + r)


def add(PL, unpaid):
    """The balance with this year's unpaid tax added (a refund never reduces it: only a positive unpaid arrives here)."""
    return np.asarray(PL, float) + unpaid


def settle(q, PL, pen, keep=0.0):
    """Settle PL on the classes q (dict, non-pension) and the pension balance pen. Returns (q1, pen1, paid, drawn, rest): the classes after payment, the pension after the draw, `paid` the receipt by class
    (the classes' payment pro rata to their positive balances, and the draw in the same mix, or all in the first class when no balance is positive), `drawn` the pension draw and `rest` the unpaid remainder."""
    pos = {k: np.maximum(v, 0.0) for k, v in q.items()}
    tot, net = sum(pos.values()), sum(q.values())
    share = {k: np.where(tot > 0, pos[k] / np.where(tot > 0, tot, 1.0), 0.0) for k in q}
    first = list(q)[0]
    mix = {k: np.where(tot > 0, share[k], 1.0 * (k == first)) for k in q}
    x = np.minimum(PL, np.maximum(net, 0.0))
    d = np.minimum(PL - x, np.maximum(pen, 0.0) * (1.0 - keep))
    return ({k: q[k] - x * share[k] for k in q}, pen - d, {k: x * share[k] + d * mix[k] for k in q}, d, PL - x - d)
