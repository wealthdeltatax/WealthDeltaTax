#!/usr/bin/env python3
"""
apply_phase2_rates.py -- Route B lien / income in rates_core.run_lines (vectorised), plus relief by tenth year
(WDT_Refactor_Plan.md D4b, D4c, section 4). Additive: with no Route B scenario the engine is the earlier one.

Run AFTER apply_basis_change.py (it needs the post-basis `Wp = f * V` line) and apply_phase2_params.py.
Usage: python apply_phase2_rates.py MODEL_DIR [--check]        Backups: rates_core.py.pre_p2.bak, wdt_core.py.pre_p2b.bak

What it adds
  scenario key route_b_mode = "sale" | "lien" | "income" (else [route_b].payment_mode). 'sale' = unchanged.
  Per launch-wealth cell: Route B share ([route_b].share_by_wealth), external income / wealth ([income].ratio_by_wealth).
  lien: the Route B share of each year's tax is added to a balance accruing at r_def; declared wealth is net of it;
        settled by sale of units at deaths (before the heir is taxed), counted in net receipts then. Outstanding balance
        at the window end is reported (lien_out_gdp_end), not collected.
  income: that share is paid from income (cap x ratio x V0 x index per year); the shortfall is met by sale of units.
        Income received is cash to the state (in net receipts, not in the state stake).
  new window columns: lien_gdp_mean, lien_out_gdp_end, rel_y10..rel_yT, exp_y10..exp_yT, rel_cov_year;
  new headline blocks: overall.p10 / overall.p90 (uncensored windows).
Also registers 'route_b_mode' as an optional [rates] key in wdt_core so a scenario can set it (skipped with a note if the
anchor is not found; rates_core then reads only the global [route_b].payment_mode).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from apply_basis_change import patch_text, locate

PATCHES = [('run_lines: Route B argument and helper',
  "def run_lines(g, idx, V0, w, group, nb, ph, G, c, rp, heir_rule='delta', c_cap='units'):\n",
  'def _route_b_cell(cfg, cal, p):\n'
  '    """\n'
  '    Route B scenario inputs per cell (plan D4b / D4c), or None for the sale mode (the earlier behaviour, '
  'unchanged).\n'
  "    The mode is cfg['route_b_mode'] (a scenario key) else [route_b].payment_mode. Per cell, by launch "
  'wealth in £m, linear in ln W and\n'
  "    flat beyond the end points: the Route B share of the cell's holdings ([route_b].share_by_wealth) and, "
  'for the income mode, external\n'
  '    income / wealth ([income].ratio_by_wealth). Cached on the calibration.\n'
  '    """\n'
  "    rb, inc = p.get('route_b'), p.get('income')\n"
  "    mode = cfg.get('route_b_mode') or (rb or {}).get('payment_mode', 'sale')\n"
  "    if mode not in ('sale', 'lien', 'income'):\n"
  '        raise ValueError(f"route_b_mode must be sale | lien | income, got {mode!r}")\n'
  "    if mode == 'sale' or not rb or not rb.get('share_by_wealth'):\n"
  '        return None\n'
  "    cache = cal.setdefault('_route_b', {})\n"
  '    if mode in cache:\n'
  '        return cache[mode]\n'
  "    W = np.maximum(np.asarray(cal['V0'], float) * cal['y_ref_gbp_m'], 1e-12)\n"
  '\n'
  '    def curve(points):\n'
  '        xs = np.log([a for a, _ in points])\n'
  '        return np.interp(np.log(W), xs, [b for _, b in points])\n'
  "    spec = {'mode': mode, 'r_def': float(rb['r_def']), 'bshare': curve(rb['share_by_wealth']),\n"
  "            'income': (curve(inc['ratio_by_wealth']) if mode == 'income' and inc and "
  "inc.get('ratio_by_wealth')\n"
  '                       else np.zeros(len(W))),\n'
  "            'cap': float(inc['cap']) if inc else 1.0}\n"
  '    cache[mode] = spec\n'
  '    return spec\n'
  '\n'
  '\n'
  "def run_lines(g, idx, V0, w, group, nb, ph, G, c, rp, heir_rule='delta', c_cap='units', rb=None):\n"),
 ('run_lines: Route B state',
  '    EC = np.zeros(n)                      # true value paid net of refunds (units_and_value cap)\n',
  '    EC = np.zeros(n)                      # true value paid net of refunds (units_and_value cap)\n'
  '    # Route B lien / income scenarios (plan D4b / D4c); rb = None is the earlier behaviour exactly\n'
  '    rb_on = rb is not None\n'
  '    LB = np.zeros(n)                      # deferred balance (lien), value, accrues at r_def\n'
  '    lienv = np.zeros(T)                   # lien settled by sale of units at deaths\n'
  '    lien_out = np.zeros(T)                # deferred balance outstanding at year end (weighted)\n'
  '    if rb_on:\n'
  "        bsh = np.asarray(rb['bshare'], float)\n"
  "        mode, r_def = rb['mode'], float(rb['r_def'])\n"
  "        inc_allow = float(rb['cap']) * np.asarray(rb['income'], float) * np.asarray(V0, float)\n"
  '        inc_left = np.zeros(n)\n'
  '        inc_paid = np.zeros(n)\n'),
 ('run_lines: declared wealth net of the lien, accrual and income allowance',
  '        Wn = f * V\n        rate = wc.rate_vec(Wn / idx[t - 1], rp)\n        delta = Wn - Wp\n',
  '        Wn = f * V\n'
  '        if rb_on:\n'
  '            LB = LB * (1.0 + r_def)\n'
  '            inc_left = inc_allow * idx[t - 1]\n'
  '            Wn = np.maximum(Wn - LB, 0.0)            # declared wealth is net of the deferred balance\n'
  '        rate = wc.rate_vec(Wn / idx[t - 1], rp)\n'
  '        delta = Wn - Wp\n'),
 ('run_lines: refund block skipped for Route B scenarios',
  '        neg = (delta < 0.0) & (u > 0.0) & (f > 0.0) & (Wp > 0.0)\n        if neg.any():\n',
  '        neg = (delta < 0.0) & (u > 0.0) & (f > 0.0) & (Wp > 0.0)\n'
  '        if rb_on:\n'
  '            neg = (delta < 0.0) & ((u > 0.0) | (LB > 0.0)) & (f > 0.0) & (Wp > 0.0)\n'
  '        if neg.any() and not rb_on:\n'),
 ('run_lines: Route B payments and refunds',
  '        units = f * q\n        paid = units * V\n        f = f - units\n',
  '        cashv = 0.0\n'
  '        if rb_on:\n'
  '            # tax value L on a rise; the Route B share is deferred (lien) or paid from income, the rest '
  'in units\n'
  '            L = np.zeros(n)\n'
  '            L[pos] = rate[pos] * delta[pos]\n'
  '            B_tax = bsh * L\n'
  '            units_val = L - B_tax\n'
  '            cashv = np.zeros(n)\n'
  "            if mode == 'lien':\n"
  '                LB = LB + B_tax\n'
  '            else:\n'
  '                pay = np.minimum(B_tax, inc_left)\n'
  '                inc_left = inc_left - pay\n'
  '                inc_paid = inc_paid + pay\n'
  '                cashv = pay\n'
  '                units_val = units_val + (B_tax - pay)    # shortfall: pro-rata sale of units\n'
  '            units_ref = np.zeros(n)\n'
  '            if neg.any():\n'
  '                R_ = np.zeros(n)\n'
  '                R_[neg] = rate[neg] * (1.0 - Wn[neg] / Wp[neg]) * Wn[neg]    # ratio-mirror refund, '
  'value\n'
  '                RB = bsh * R_\n'
  "                if mode == 'lien':\n"
  '                    can = np.minimum(RB, LB)\n'
  '                    LB = LB - can\n'
  '                else:\n'
  '                    can = np.minimum(RB, inc_paid)\n'
  '                    inc_paid = inc_paid - can\n'
  '                    cashv = cashv - can\n'
  '                units_ref = np.minimum((R_ - can) / V, u)       # the rest in units, capped by units '
  'paid\n'
  "                if c_cap == 'units_and_value':\n"
  '                    units_ref = np.minimum(units_ref, np.maximum(EC, 0.0) / V)\n'
  '                units_ref = np.where(neg, units_ref, 0.0)\n'
  '            units = units_val / V - units_ref\n'
  '        else:\n'
  '            units = f * q\n'
  '        paid = units * V\n'
  '        f = f - units\n'),
 ('run_lines: basis net of the lien; cash receipts counted',
  '        Wp = f * V                               # POST-surrender basis (BASIS_CHANGE)\n'
  '        wp = w * paid\n'
  '        tax[t - 1] = wp[paid > 0.0].sum()\n'
  '        ref[t - 1] = wp[paid < 0.0].sum()\n'
  '        npay[t - 1] = w[paid > 0.0].sum()\n'
  '        by_b[t - 1] = np.bincount(group, weights=wp, minlength=nb)\n',
  '        Wp = np.maximum(f * V - LB, 0.0) if rb_on else f * V     # POST-surrender basis (BASIS_CHANGE), '
  'net of the lien\n'
  '        pt = paid + cashv                        # value to the state this year: units and income cash\n'
  '        wp = w * pt\n'
  '        tax[t - 1] = wp[pt > 0.0].sum()\n'
  '        ref[t - 1] = wp[pt < 0.0].sum()\n'
  '        npay[t - 1] = w[pt > 0.0].sum()\n'
  '        by_b[t - 1] = np.bincount(group, weights=wp, minlength=nb)\n'),
 ('run_lines: lien settled at a death, before the heir is taxed',
  "            d = (t >= ph) & (((t - ph) % G) == 0)\n            if d.any() and heir_rule == 'fresh':\n",
  '            d = (t >= ph) & (((t - ph) % G) == 0)\n'
  '            if rb_on and d.any():\n'
  '                sv = np.where(d, np.minimum(LB, f * V), 0.0)     # lien settled by sale of units at the '
  'true price\n'
  '                su = sv / V\n'
  '                f = f - su\n'
  '                s = s + su\n'
  '                lienv[t - 1] = (w * sv).sum()\n'
  '                by_b[t - 1] += np.bincount(group, weights=w * sv, minlength=nb)\n'
  '                LB = np.where(d, 0.0, LB)\n'
  '                inc_paid = np.where(d, 0.0, inc_paid)\n'
  '                inc_left = np.where(d, inc_allow * idx[t - 1], inc_left)\n'
  "            if d.any() and heir_rule == 'fresh':\n"),
 ('run_lines: Route B share of the heir tax',
  '                ud = f[d] * qd\n                pd_ = ud * V[d]\n',
  '                ud = f[d] * qd\n'
  '                pd_ = ud * V[d]\n'
  '                cashd = 0.0\n'
  '                if rb_on:                                # Route B share of the heir tax: deferred (lien) '
  'or paid from income\n'
  '                    Bh = bsh[d] * pd_\n'
  "                    if mode == 'lien':\n"
  '                        LB[d] = LB[d] + Bh\n'
  '                        pd_ = pd_ - Bh\n'
  '                    else:\n'
  '                        cashd = np.minimum(Bh, inc_left[d])\n'
  '                        inc_left[d] = inc_left[d] - cashd\n'
  '                        inc_paid[d] = inc_paid[d] + cashd\n'
  '                        pd_ = pd_ - cashd\n'
  '                    ud = pd_ / V[d]\n'),
 ('run_lines: heir receipts include income cash, basis net of the lien',
  '                Wp[d] = f[d] * V[d]              # POST-heir-tax basis (BASIS_CHANGE)\n'
  '                heir[t - 1] = (w[d] * pd_).sum()\n'
  '                by_b[t - 1] += np.bincount(group[d], weights=w[d] * pd_, minlength=nb)\n'
  '                heir_b[t - 1] += np.bincount(group[d], weights=w[d] * pd_, minlength=nb)\n',
  '                Wp[d] = f[d] * V[d] - (LB[d] if rb_on else 0.0)    # POST-heir-tax basis (BASIS_CHANGE), '
  'net of the lien\n'
  '                heir[t - 1] = (w[d] * (pd_ + cashd)).sum()\n'
  '                by_b[t - 1] += np.bincount(group[d], weights=w[d] * (pd_ + cashd), minlength=nb)\n'
  '                heir_b[t - 1] += np.bincount(group[d], weights=w[d] * (pd_ + cashd), minlength=nb)\n'),
 ('run_lines: outstanding balance at year end',
  '        wealth[t - 1] = (w * f * V).sum()\n',
  '        wealth[t - 1] = (w * f * V).sum()\n        lien_out[t - 1] = (w * LB).sum()\n'),
 ('run_lines: new outputs',
  "    return {'tax': tax, 'refund': ref, 'heir': heir, 'stake': stake, 'share_paying': npay,\n",
  "    return {'tax': tax, 'refund': ref, 'heir': heir, 'stake': stake, 'share_paying': npay,\n"
  "            'lien': lienv, 'lien_out': lien_out,\n"),
 ('run_cohorts: Route B argument',
  "                heir_rule='delta', c_cell=None, cell_diff=None, c_cap='units'):\n",
  "                heir_rule='delta', c_cell=None, cell_diff=None, c_cap='units', rb_cell=None):\n"),
 ('run_cohorts: pass Route B per line',
  "    raw = run_lines(g, scn['idx'], V0, w, b_id, nb, ph, G, c_line, cal['rate'],\n"
  '                    heir_rule=heir_rule, c_cap=c_cap)\n',
  '    rb = None\n'
  '    if rb_cell is not None:\n'
  "        rb = {'mode': rb_cell['mode'], 'r_def': rb_cell['r_def'], 'cap': rb_cell['cap'],\n"
  "              'bshare': rb_cell['bshare'][b_id], 'income': rb_cell['income'][b_id]}\n"
  "    raw = run_lines(g, scn['idx'], V0, w, b_id, nb, ph, G, c_line, cal['rate'],\n"
  '                    heir_rule=heir_rule, c_cap=c_cap, rb=rb)\n'),
 ('run_cohorts: lien in the output arrays',
  "    out = {k: raw[k] * norm for k in ('tax', 'refund', 'heir', 'stake', 'wealth')}\n",
  "    out = {k: raw[k] * norm for k in ('tax', 'refund', 'heir', 'stake', 'wealth', 'lien', 'lien_out')}\n"),
 ('run_cohorts: net includes the lien settled at deaths',
  "    out['net'] = out['tax'] + out['refund'] + out['heir']\n",
  "    out['net'] = out['tax'] + out['refund'] + out['heir'] + out['lien']\n"),
 ('run_window: Route B cells',
  "cell_diff=cal.get('cell_diff'), c_cap=wc.resolve_rule(p, cfg['rule_set'])['c_cap'])\n",
  "cell_diff=cal.get('cell_diff'), c_cap=wc.resolve_rule(p, cfg['rule_set'])['c_cap'],\n"
  '                      rb_cell=_route_b_cell(cfg, cal, p))\n'),
 ('decade columns helper before _horizon_cols',
  'def _horizon_cols(fv, lp, out, scale, scn, cal, cfg):\n',
  'def _decade_cols(f, scale, scn, cfg):\n'
  '    """Relief and expenditure as a share of GDP in each tenth year (10, 20, ... T), and the first year '
  'relief covers expenditure (NaN if never)."""\n'
  "    R, T = f['R'], cfg['T']\n"
  '    out = {}\n'
  '    for k in range(10, T + 1, 10):\n'
  "        out[f'rel_y{k}'] = float(R[k - 1] / scale[k - 1])\n"
  "        out[f'exp_y{k}'] = float(scn['exp_gdp'][k - 1])\n"
  "    hit = np.where((R > 0.0) & (R >= scn['exp_gdp'] * scale))[0]\n"
  "    out['rel_cov_year'] = float(hit[0] + 1) if len(hit) else np.nan\n"
  '    return out\n'
  '\n'
  '\n'
  'def _horizon_cols(fv, lp, out, scale, scn, cal, cfg):\n'),
 ('run_window: lien and decade columns in the row',
  "        'refund_gdp_mean': float(out['refund'].mean()),\n",
  "        'refund_gdp_mean': float(out['refund'].mean()),\n"
  "        'lien_gdp_mean': float(out['lien'].mean()), 'lien_out_gdp_end': float(out['lien_out'][-1]),\n"),
 ('run_window: relief by tenth year',
  '        **conc, **fund, **zuc, **bands, **var,\n',
  '        **conc, **fund, **zuc, **bands, **var, **_decade_cols(f, scale, scn, cfg),\n'),
 ('_mode_block: p10 / p90 of every column over uncensored windows',
  "    overall['medians_all'] = {c: (None if np.isnan(v) else float(v)) for c, v in "
  'num_all.median().items()}\n',
  "    overall['medians_all'] = {c: (None if np.isnan(v) else float(v)) for c, v in "
  'num_all.median().items()}\n'
  "    for q_, key_ in ((0.10, 'p10'), (0.90, 'p90')):\n"
  '        overall[key_] = {c: (None if np.isnan(v) else float(v)) for c, v in num.quantile(q_).items()}\n')]

WDT_CORE = [
    ("register route_b_mode as an optional rates key",
     "                   'cohorts', 'wmin_house_ratio', 'anchor_from')\n",
     "                   'cohorts', 'wmin_house_ratio', 'anchor_from', 'route_b_mode')\n"),
]


def _apply(path, patches, name, check_only, tag):
    raw = path.read_bytes().decode('utf-8'); crlf = '\r\n' in raw
    text = raw.replace('\r\n', '\n')
    new_text, log = patch_text(text, patches, name)
    print(f"{path} ({'CRLF' if crlf else 'LF'}): " + ('changes pending' if new_text != text else 'no changes'))
    print('\n'.join(log))
    if check_only or new_text == text:
        return
    bak = path.with_name(path.name + tag)
    if not bak.exists():
        bak.write_bytes(path.read_bytes())
    compile(new_text, str(path), 'exec')
    path.write_bytes((new_text.replace('\n', '\r\n') if crlf else new_text).encode('utf-8'))
    print(f'  wrote {path} (backup {bak.name}); syntax OK')


def main(argv):
    if len(argv) < 2 or argv[1].startswith('--'):
        print(__doc__); return 2
    root, check_only = Path(argv[1]), '--check' in argv
    try:
        _apply(locate(root, 'rates_core.py'), PATCHES, 'rates_core.py', check_only, '.pre_p2.bak')
    except RuntimeError as e:
        print(f'ABORT {e}'); return 1
    try:
        _apply(locate(root, 'wdt_core.py'), WDT_CORE, 'wdt_core.py', check_only, '.pre_p2b.bak')
    except RuntimeError as e:
        print(f'NOTE {e}\n  (scenarios cannot set route_b_mode; set [route_b].payment_mode instead)')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
