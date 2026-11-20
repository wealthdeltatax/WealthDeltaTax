"""
burden.py -- burden, non-payer savings and the comparators (model v3, stage V3-8)
=================================================================================
Layer L3 (architecture.md 5.1). Imports numpy, core/pack.py and core/kernel.py. No file is read and nothing runs at import (R8). No country or tax
is named here (R11): the pack, the register and the tax names (`order`, `parts`, `payer_taxes`) arrive as arguments.

LINES AND UNITS (R6)
--------------------
`line_flows` runs the kernel once per death phase and keeps every line: arrays (T, N, P), year down, N = lines x phases, path across. Money is millions of
pounds per adult in real prices (the kernel's unit), `net` positive when the adult pays. A payer is a line at or above W_min at launch. `wt` is the share of
all adults (a line's weight divided by the phases). Windows are 1-based year bounds (lo, hi), one per path or one number.

METRICS (every ratio is in percent; `band` keys are overall, D4_5, D6_7, D8_9, D10)
-----------------------------------------------------------------------------------
M2  revenue-weighted burden: sum wt net (net / W0) over sum wt net, payers with net > 0, W0 the start-of-year wealth, pooled over the window.
M2b, M2c  payer-weighted mean of net over income (income grows with GDP per head) or over liquid assets (the line's launch share of wealth); the share of
    payers above each cut-off. Lines with no income or liquid-asset source are left out, never filled.
M3  present value of net paid over the first G years over present value of the gains (the positive real changes in net wealth, before tax), payers only.
OH1b (M3 on today's system)  the same ratio with today's liabilities: a rate over wealth by band (register) on the untaxed wealth path.
OH1c (M12)  escape share of the present value of accrued gains: exempt by law (wrapper shares of wealth) and deferral then uplift (the unrealised stock
    left at the end of the life, discounted). Realisation is a share of gain-bearing wealth a year (register), capped by the stock.
M4a, M4b, M4c, DH1c  the retired taxes' incidence by income decile of all households (the non-payers' share is taken as the decile's: no joint income and
    wealth table is held). Where the pack gives a tax's share for the top decile and the bottom five, the other deciles split the rest evenly; a retired
    tax with no row is spread in proportion to gross income; the taxes in `payer_taxes` fall on payers and give the non-payers nothing.
M5  burden of each suggested wealth tax on the same lines at launch; M6 today's liabilities over wealth (a gains-tax row over the payers' wealth is reused for the bands that have none); M8 a reform inside the existing system raising
    the revenue of M1 from the same payers (shares of wealth in its base from the pack); M11 the worker's average rate (a register row).
"""

from __future__ import annotations

import numpy as np

from model_v3.core import kernel as K
from model_v3.core import pack as pk

G = 30
BANDS = {'D4-5': 'D4_5', 'D6-7': 'D6_7', 'D8-9': 'D8_9', 'D10': 'D10'}   # pack band -> output band
DECILES = tuple(f'D{i}' for i in range(1, 11))
CUT_INCOME, CUT_LIQUID = (5, 10, 20), (25, 50, 100)
REF_DECILE = {'p25': 'D3', 'p50': 'D5', 'p75': 'D8', 'p90': 'D9'}          # a reference worker at that income percentile sits in that decile
DEATH = ('tax_death_C', 'tax_death', 'tax_heir', 'death_B', 'death_D')
IDS = {'disc': ('I-D11a', 'I-D11b', 'I-D11c'), 'worker': 'I-T1d', 'wrap': 'I-T6m',
       'today': {'D10': ('I-M6i', 'I-M6b'), 'D8_9': ('I-M6h', 'I-M6c'), 'D6_7': ('I-M6h', 'I-M6d'), 'D4_5': ('I-M6h', 'I-M6d')},
       'real': {'overall': ('I-M6h', 'I-M6a'), 'D10': ('I-M6i', 'I-M6b'), 'D8_9': ('I-M6h', 'I-M6c'), 'D6_7': ('I-M6h', 'I-M6d'), 'D4_5': ('I-M6h', 'I-M6d')},
       'realise': {'D10': 'I-T5f', 'other': 'I-T5e'},
       'm5': dict(zucman=('I-M5a', 'I-M5b', 'I-M5g'), uk=('I-M5a', 'I-M5d', 'I-M5g'), union=('I-M5h', 'I-M5i'), green=('I-M5k', 'I-M5l'), once=('I-M5o', 'I-M5p'))}


class BurdenError(ValueError):
    """An input the metric needs is missing."""


def _reg(reg, i, which='central'):
    if i not in reg or getattr(reg[i], which) is None:
        raise BurdenError(f'register row {i} is missing or has no {which} value')
    return getattr(reg[i], which)


def _cell(pack, dataset, **where):
    rows = pk.lookup(pack, dataset, **where)
    if len(rows) != 1:
        raise BurdenError(f'{dataset} {where}: {len(rows)} rows, one expected')
    return rows[0]


def _val(fl, n):
    """True value moved from the family to the state by one operation, per line (units at the true price plus income cash)."""
    return sum(fl.value.values()) + fl.income if fl.value else fl.income + np.zeros(n)


def _groups(band):
    b = np.asarray(band)
    return {'overall': np.ones(len(b), bool), **{o: b == p for p, o in BANDS.items()}}


def _window(T, lo, hi, P):
    t = np.arange(1, T + 1)[:, None]
    return (t >= np.broadcast_to(lo, (P,))[None, :]) & (t <= np.broadcast_to(hi, (P,))[None, :])


def _ratio(num, den):
    return np.where(den > 0, 100 * num / np.where(den > 0, den, 1.0), np.nan)


def line_flows(base, rate_fn, g, gdp_g, c, G=G, n_phase=6, index='gdp_pc', routes=None, lam_C=0.0, lam_D=0.0, death_verify=False, **book_kw):
    """The kernel over every path and death phase, every line kept. g and gdp_g are (T, P) real returns and GDP-per-head growth, c the consumption
    share. Returns net (tax paid, refunds negative, death and heir assessments), death (the part of net a death triggers), w0 (start-of-year wealth), delta (the real change in net wealth before
    tax: the assessed quantity), wt (N,), band (N,), payer0 (N,), idx (T, P) the threshold index, adults_k and w_min."""
    g, gdp_g = np.asarray(g, float), np.asarray(gdp_g, float)
    T, P = g.shape
    L, n = len(base.labels), P * len(base.labels)
    yy = np.cumprod(1.0 + gdp_g, axis=0)
    ix = yy if index == 'gdp_pc' else np.ones_like(yy)
    V0 = {r: np.tile(v, P) for r, v in (routes or base.V0).items()}
    has_cv = (lam_C > 0.0 or death_verify) and 'C' in V0 and np.any(V0['C'] > 0.0)
    net, w0, dl, dth = (np.zeros((T, L * n_phase, P)) for _ in range(4))
    tl = lambda x: x.reshape(P, L).T
    for i in range(n_phase):
        ph, sl = int(np.ceil((i + 1) * G / n_phase)), slice(i * L, (i + 1) * L)
        book = K.Book(n, V0, alpha0={'C': 1.0, 'D': 1.0}, has_cv=has_cv, **book_kw)
        for t in range(1, T + 1):
            il, gt = np.repeat(ix[t - 1], L), np.repeat(g[t - 1], L)
            w0[t - 1, sl] = tl(book.family_true())
            tax, dd, dx = np.zeros(n), np.zeros(n), np.zeros(n)
            for kind, fl in K.step_year(book, rate_fn, il, gt, c, 1.0, 1.0, lam_C, lam_D, False):
                if kind == 'tax':
                    tax, dd = tax + _val(fl, n), dd + fl.delta
            if t < T and t >= ph and (t - ph) % G == 0:
                for kind, fl in K.step_death(book, rate_fn, il, death_verify):
                    dx = dx + _val(fl, n) if kind in DEATH else dx
            net[t - 1, sl], dl[t - 1, sl], dth[t - 1, sl] = tl(tax + dx), tl(dd), tl(dx)
    return {'net': net, 'w0': w0, 'delta': dl, 'death': dth, 'wt': np.tile(base.weights / n_phase, n_phase), 'band': base.band * n_phase,
            'payer0': np.tile(base.wealth >= base.w_min, n_phase), 'idx': ix, 'adults_k': base.adults_k.sum(), 'w_min': base.w_min,
            'income': np.tile(base.income, n_phase), 'liq_share': np.tile(base.liquid / base.wealth, n_phase)}


def _net(fl, inlife):
    return fl['net'] - fl['death'] if inlife else fl['net']


def m2(fl, lo, hi, inlife=False):
    """M2 by band over the window, percent a year, nan where no one paid. `inlife` leaves out what a death triggers (default: all net WDT of the year)."""
    net, w0, wt = _net(fl, inlife), fl['w0'], fl['wt'][None, :, None]
    m = _window(net.shape[0], lo, hi, net.shape[2])[:, None, :] & (net > 0) & (w0 > 0)
    num, den = np.where(m, wt * net ** 2 / np.where(w0 > 0, w0, 1.0), 0.0), np.where(m, wt * net, 0.0)
    return {k: _ratio(num[:, gm].sum((0, 1)), den[:, gm].sum((0, 1))) for k, gm in _groups(fl['band']).items()}


def _cash(fl, denom, cuts, lo, hi, inlife):
    net, wt = _net(fl, inlife), fl['wt'][None, :, None]
    ok = _window(net.shape[0], lo, hi, net.shape[2])[:, None, :] & (net > 0) & np.isfinite(denom) & (denom > 0)
    r = np.where(ok, net / np.where(ok, denom, 1.0), 0.0)
    out = {}
    for k, gm in _groups(fl['band']).items():
        w = (wt * ok)[:, gm]
        sw = w.sum((0, 1))
        out[k] = {'mean': _ratio((w * r[:, gm]).sum((0, 1)), sw), **{f'share_{x}': _ratio((w * (r[:, gm] > x / 100)).sum((0, 1)), sw) for x in cuts}}
    return out


def m2b(fl, lo, hi, inlife=False):
    """M2b: net over income by band, and the share of payers above 5, 10 and 20 percent of income."""
    return _cash(fl, fl['income'][None, :, None] * fl['idx'][:, None, :], CUT_INCOME, lo, hi, inlife)


def m2c(fl, lo, hi, inlife=False):
    """M2c: net over liquid assets by band, and the share of payers above 25, 50 and 100 percent."""
    return _cash(fl, fl['liq_share'][None, :, None] * fl['w0'], CUT_LIQUID, lo, hi, inlife)


def discount(rates, T):
    """Discount factors for years 1 to T from the three schedule rates (percent): years 1 to 30, 31 to 75, 76 onwards."""
    t = np.arange(1, T + 1)
    r = np.where(t <= 30, rates[0], np.where(t <= 75, rates[1], rates[2])) / 100.0
    return np.cumprod(1.0 / (1.0 + r))


def m3(fl, rates, G=G, inlife=False):
    """M3 over the first G years: present value of net paid over present value of the gains (the positive real changes in net wealth, before tax), payers,
    percent, one value per path. A signed sum of changes can be zero or negative over a life and then has no rate."""
    d, pay, wt = discount(rates, G)[:, None, None], fl['payer0'][None, :, None], fl['wt'][None, :, None]
    num, den = ((wt * pay * d * x[:G]).sum((0, 1)) for x in (_net(fl, inlife), np.maximum(fl['delta'], 0.0)))
    return np.where(den > 0, 100 * num / np.where(den > 0, den, 1.0), np.nan)


def free_path(base, g, c, G=G):
    """Wealth of each line with no wealth tax, years 0 to G: (G + 1, L, P). g is (T, P)."""
    f = (1.0 + np.asarray(g, float)[:G]) * (1.0 - c)
    return np.concatenate([np.ones((1, 1, f.shape[1])), np.cumprod(f, axis=0)[:, None, :]]) * base.wealth[None, :, None]


def _pooled(base, W, G, rates, per_line):
    """Per band, present value of per_line(W)'s tax over present value of the gains (positive changes), payer lines, percent: {band: (P,)}."""
    d, a = discount(rates, G)[:, None, None], (base.adults_k * (base.wealth >= base.w_min))[None, :, None]
    gain, tax = (a * d * np.maximum(np.diff(W, axis=0), 0.0)).sum(0), (a * d * per_line(W[1:])).sum(0)
    return {k: _ratio(tax[gm].sum(0), gain[gm].sum(0)) for k, gm in _groups(base.band).items()}


def m3_today(base, g, c, reg, rates, G=G):
    """OH1b, M3 on today's system: today's liabilities as a rate over wealth by band (register) on the untaxed wealth path, by band, percent, per path."""
    r = {k: sum(_reg(reg, i) for i in v) / 100.0 for k, v in IDS['today'].items()}
    rl = np.array([r.get(BANDS.get(b, ''), 0.0) for b in base.band])[None, :, None]
    return _pooled(base, free_path(base, g, c, G), G, rates, lambda W: rl * W)


def _band_wealth(pack):
    rng = {'D4-5': (4, 5), 'D6-7': (6, 7), 'D8-9': (8, 9), 'D10': (10,)}
    return {p: sum(_cell(pack, 'wealth_distribution', variable='wealth_total', band=f'D{i}')['value'] for i in r) for p, r in rng.items()}


def m12(base, g, c, reg, pack, rates, G=G):
    """OH1c (M12): {band: {'deferral_uplift', 'exempt_law'}} as a percent of the present value of accrued gains, per path. Accrued gains are the positive
    real changes in untaxed wealth; the stock not realised in the life is forgiven at death; the wrapper share of wealth never accrues a charge."""
    W, d, bw = free_path(base, g, c, G), discount(rates, G), _band_wealth(pack)
    wrap = _reg(reg, IDS['wrap']) / 100.0
    pen = {r['band']: r['value'] / 100.0 for r in pk.lookup(pack, 'wealth_distribution', variable='pension_share')}
    cell = lambda p: _cell(pack, 'wealth_distribution', variable='gain_bearing_wealth', band=p)['value'] / bw[p]
    ex = np.array([pen.get(b, pen['all']) + wrap if b else 0.0 for b in base.band])[:, None]
    rho = np.array([_reg(reg, IDS['realise']['D10' if b == 'D10' else 'other']) / 100.0 * cell(b) if b else 0.0 for b in base.band])[:, None]
    a, gain = (base.adults_k * (base.wealth >= base.w_min))[:, None], np.maximum(np.diff(W, axis=0), 0.0)
    U, acc = np.zeros(W.shape[1:]), np.zeros(W.shape[1:])
    for t in range(G):
        U = U + gain[t] - np.minimum(rho * W[t + 1], U + gain[t])
        acc = acc + d[t] * gain[t]
    out = {}
    for k, gm in _groups(base.band).items():
        den = (a * acc)[gm].sum(0)
        out[k] = {'deferral_uplift': _ratio((a * (1 - ex) * d[G - 1] * U)[gm].sum(0), den), 'exempt_law': _ratio((a * ex * acc)[gm].sum(0), den)}
    return out


def incidence(pack, order, parts, payer_taxes=()):
    """The retired taxes' pounds per household a year by income decile of all households: (len(order), 10). See the module note for the rule."""
    gdp, hh = (_cell(pack, 'wealth_distribution', variable=v, band='all')['value'] for v in ('gdp', 'households'))
    inc = np.array([_cell(pack, 'household_incidence', variable='gross_income', group=d, tax=None)['value'] for d in DECILES])
    out = []
    for k in order:
        if k in payer_taxes:
            out.append(np.zeros(10))
            continue
        ms = parts.get(k, [k])
        pounds = sum(_cell(pack, 'receipts', line=m)['pct_gdp'] for m in ms) / 100.0 * gdp * 1e9 / (hh * 1e3)
        top = [pk.lookup(pack, 'household_incidence', variable='tax_share_top_decile', group='D10', tax=m) for m in ms]
        bot = [pk.lookup(pack, 'household_incidence', variable='tax_share_bottom_five', group='D1-5', tax=m) for m in ms]
        have = [(t[0]['value'], b[0]['value']) for t, b in zip(top, bot) if t and b]
        if have:
            s10, sb = have[0]
            sh = np.r_[np.full(5, sb / 5), np.full(4, (100 - sb - s10) / 4), s10] / 100.0
        else:
            sh = inc / inc.sum()
        out.append(pounds * 10 * sh)
    return np.array(out)


def pack_deciles(pack):
    """Pounds per household a year by income decile of all households: (total tax bill, gross income). The M4a and M4b denominators."""
    f = lambda v: np.array([_cell(pack, 'household_incidence', variable=v, group=d, tax=None)['value'] for d in DECILES], float)
    return f('total_tax'), f('gross_income')


def m4(years, at, inc, bill, income):
    """M4a and M4b by income decile and overall, percent, one value per path. `years` is the retirement year of each tax (P, K) (0 = never, as
    revenue.retire), `at` the year read (one per path), `inc` the (K, 10) incidence, bill and income the pack decile tables. Also the saving in pounds."""
    s = ((years > 0) & (years <= np.asarray(at)[:, None])).astype(float) @ inc
    mk = lambda den: {**{d: 100 * s[:, i] / den[i] for i, d in enumerate(DECILES)}, 'overall': 100 * s.sum(1) / den.sum()}
    return {'M4a': mk(bill), 'M4b': mk(income), 'saving_gbp': s}


def m4c(m4b, income):
    """M4c, pounds a month for a reference worker at each percentile: M4b of the worker's decile times the decile's mean income over twelve."""
    return {p: m4b[d] / 100.0 * income[DECILES.index(d)] / 12.0 for p, d in REF_DECILE.items()}


def dh1c(pack, order, parts, payer_taxes=()):
    """DH1c: the non-payers' tax bill by income decile in pounds and as a share of income, and the retired taxes' part (all retired)."""
    bill, income = pack_deciles(pack)
    ret = incidence(pack, order, parts, payer_taxes).sum(0)
    return {'bill_gbp': bill, 'income_gbp': income, 'bill_pct_income': 100 * bill / income, 'retired_gbp': ret, 'retired_pct_income': 100 * ret / income,
            'retired_pct_bill': 100 * ret / bill}


def _burden(wealth, adults_k, tax):
    """M2 form on the lines at launch: sum a T T / W over sum a T, percent a year; nan where no line pays."""
    num, den = (adults_k * tax * tax / wealth).sum(), (adults_k * tax).sum()
    return 100 * num / den if den > 0 else float('nan')


def m5(wealth, adults_k, reg, m2_wdt=None):
    """M5: the burden of each suggested wealth tax on the same lines at launch (percent a year, wealth in millions per adult) and, if `m2_wdt` is
    given, its difference from the WDT's M2. Reads only the register."""
    w, a, ids = np.asarray(wealth, float), np.asarray(adults_k, float), IDS['m5']
    r = lambda i: _reg(reg, i) / 100.0
    zr, zt, zc = ids['zucman']
    ur, ut, uc = ids['uk']
    tax = {'zucman': np.where(w >= _reg(reg, zt) * 1e3, (r(zr) - r(zc)) * w, 0.0), 'uk_minimum': np.where(w >= _reg(reg, ut), (r(ur) - r(uc)) * w, 0.0),
           'union': r(ids['union'][0]) * np.maximum(w - _reg(reg, ids['union'][1]), 0.0),
           'green': r(ids['green'][0]) * np.clip(w - _reg(reg, ids['green'][1]), 0.0, _reg(reg, ids['green'][1], 'high') - _reg(reg, ids['green'][1]))
           + _reg(reg, ids['green'][0], 'high') / 100.0 * np.maximum(w - _reg(reg, ids['green'][1], 'high'), 0.0),
           'once': np.where(w >= _reg(reg, ids['once'][1]) / 1e3, r(ids['once'][0]) / 5.0 * w, 0.0)}
    out = {k: _burden(np.where(w > 0, w, 1.0), a, np.maximum(v, 0.0)) for k, v in tax.items()}
    return {**out, **({f'{k}_diff': v - m2_wdt for k, v in out.items()} if m2_wdt is not None else {})}


def m6(reg):
    """M6: today's liabilities over wealth, percent a year, per band and overall: the two rows (a gains tax and an estate tax) and their sum."""
    return {k: {'gains': _reg(reg, a), 'estates': _reg(reg, b), 'total': _reg(reg, a) + _reg(reg, b)} for k, (a, b) in IDS['real'].items()}


def reform_shares(pack):
    """Share of each pack wealth band that a reform's base covers: property (the pack's property share) and gains (gain-bearing wealth over the band)."""
    bw = _band_wealth(pack)
    gain = {p: _cell(pack, 'wealth_distribution', variable='gain_bearing_wealth', band=p)['value'] / bw[p] for p in bw}
    prop = {p: _cell(pack, 'wealth_distribution', variable='property_share', band=p)['value'] / 100.0 for p in bw if p != 'D4-5'}
    return {'property': {**prop, 'D4-5': np.nan}, 'gains': gain}


def m8(wealth, adults_k, band, w_min, revenue_bn, shares):
    """M8: a reform raising `revenue_bn` (per path, billions) from the same payers (lines at or above W_min at launch), each paying in proportion to
    wealth in the reform's base. Returns per reform the burden (M2 form, percent, per path) and the revenue raised (equal to `revenue_bn`)."""
    w, a = np.asarray(wealth, float), np.asarray(adults_k, float)
    pay = w >= w_min
    out = {}
    for name, sh in shares.items():
        x = np.array([sh.get(b, np.nan) for b in band]) * w
        if np.isnan(x[pay]).any():
            raise BurdenError(f'reform {name}: a payer line is in a band with no base share')
        x = np.where(pay, x, 0.0)
        X, R = (a * x).sum(), np.asarray(revenue_bn, float)
        t = R[..., None] * x / X
        out[name] = {'burden': 100 * (a * t * t / np.where(pay, w, 1.0)).sum(-1) / R, 'revenue_bn': (a * t).sum(-1)}
    return out


def m11(reg):
    """M11, the worker's average income tax and employee contribution rate at median full-time earnings, percent (a register row)."""
    return _reg(reg, IDS['worker'])
