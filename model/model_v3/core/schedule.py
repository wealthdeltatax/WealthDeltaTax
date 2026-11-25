"""
schedule.py -- the marginal rate function tau(W)
================================================
Layer L1 (architecture.md 5.1). Imports numpy only; no project module. No file is read and nothing runs at
import (R8). No country appears here (R11): every number arrives as an argument.

The marginal rate on declared wealth W (pounds m, already deflated by the index factor, so W_min and k are
in base-year terms):

    logistic     tau(W) = tau_m / (1 + ((tau_m - tau_0) / tau_0) * exp(-k * (W - W_min)))
    logistic_ln  tau(W) = tau_m / (1 + ((tau_m - tau_0) / tau_0) * exp(-k * ln(W / W_min)))     k dimensionless

and tau(W) = 0 below W_min in both forms. tau(W_min) = tau_0 and tau rises to tau_m. The form is the one in
model v2 (`(tau_m - tau_0) / tau_0`); the ladder branch of v2 is not ported. RATES section 4 prints a different
form: a writing item, not a code question.

CONVENTIONS (R6)
----------------
Arithmetic basis: tau is a rate on pounds, applied to a change in declared wealth by the kernel. Refund =
tau x loss lives in kernel.py. R10: a schedule is progressive when its marginal rate never falls as W rises;
`rate_function` checks this on a grid before it returns and raises on a draw that is not progressive.
"""

from __future__ import annotations

import numpy as np

FORMS = ('logistic', 'logistic_ln')
_GRID_POINTS = 801
_GRID_SPAN = 60.0          # the grid reaches W_min + 60/k (or W_min * exp(60/k)): far into the saturated tail
_MONO_TOL = 1e-12


def tau(W, k, tau_0, tau_m, W_min, form='logistic'):
    """Marginal rate on declared wealth W (scalar or array, pounds m). Returns an array shaped like W; 0 below W_min."""
    if form not in FORMS:
        raise ValueError(f'form must be one of {FORMS}, got {form!r}')
    W = np.asarray(W, dtype=float)
    above = W >= W_min
    if form == 'logistic':
        z = k * (np.where(above, W, W_min) - W_min)
    else:
        if W_min <= 0.0:
            raise ValueError("form 'logistic_ln' needs W_min > 0")
        z = k * np.log(np.where(above, W, W_min) / W_min)
    out = tau_m / (1.0 + ((tau_m - tau_0) / tau_0) * np.exp(-z))
    return np.where(above, out, 0.0)


def _grid(k, W_min, form):
    """Wealth grid from W_min into the saturated tail, in the units the form is logistic in."""
    span = _GRID_SPAN / max(abs(k), 1e-9)
    s = np.linspace(0.0, span, _GRID_POINTS)
    return W_min + s if form == 'logistic' else W_min * np.exp(s)


def rate_function(k, tau_0, tau_m, W_min, form='logistic'):
    """
    Validate one schedule draw and return the callable rate_fn(W) -> tau that the kernel takes.

    Raises ValueError on a draw that is not progressive (R10): the marginal rate, evaluated on a grid from W_min
    to the saturated tail, falls anywhere. Also raises on tau_0 <= 0 or a ceiling tau_m above 1, which the
    formula cannot represent as a rate.
    """
    if form not in FORMS:
        raise ValueError(f'form must be one of {FORMS}, got {form!r}')
    if not tau_0 > 0.0:
        raise ValueError(f'tau_0 must be > 0, got {tau_0!r}')
    if not tau_m <= 1.0:
        raise ValueError(f'tau_m must be <= 1, got {tau_m!r}')
    if form == 'logistic_ln' and not W_min > 0.0:
        raise ValueError("form 'logistic_ln' needs W_min > 0")
    t = tau(_grid(k, W_min, form), k, tau_0, tau_m, W_min, form)
    if np.any(np.diff(t) < -_MONO_TOL):
        raise ValueError(
            f'schedule is not progressive: the marginal rate falls (k={k}, tau_0={tau_0}, tau_m={tau_m}, form={form})')
    return lambda W: tau(W, k, tau_0, tau_m, W_min, form)
