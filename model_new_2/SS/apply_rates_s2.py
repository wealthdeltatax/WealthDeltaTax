#!/usr/bin/env python3
"""
apply_rates_s2.py  --  Work Order Wave 1, S2 (RATES engine on wdt_kernel).  Idempotent, CRLF-safe, anchor-asserting.

  python apply_rates_s2.py [--model-dir DIR]     DIR holds WDT_Params.toml and RATES/rates_core.py (default: this file's folder, then ..)

rates_core.py
  * run_lines: the inline engine is replaced by wdt_kernel (Book / step_year / step_death). Deaths act on one phase's lines at a time:
    the lines are cut out of the Book, run through step_death and written back (kernel feature request: step_death(..., mask)).
  * run_cohorts: plan_cell / ver replace rb_cell; net = tax + refund + heir + lien + dsettle.
  * new: _route_plan (A/B/C/D shares by band from the archetype mixture, the archetype sweep), _verification (lambda pass-through),
    check_inputs; new window columns (route D settled / accrued, external income paid, cumulative).
  * removed: valid_windows (unused), the local load_jst (wdt_jst's is used), _route_b_cell.
WDT_Params.toml
  * [rates.defaults]: route_mix, route_mix_weights, lam_C, lam_D, death_verify (defaults reproduce the earlier numbers).
  * [rates.scenarios.gl_arch_*] and the run list. [route_b] / [income] / [archetypes.*] unchanged.
Original files are kept as <name>.pre_s2.
"""
import argparse
import re
import sys
from pathlib import Path

MARK = 'S2 (Work Order Wave 1 S2, plan D12)'

BLOCK_A = '# ── S2 (Work Order Wave 1 S2, plan D12): the route engine is wdt_kernel ──────────────────────────────────────────────────────────────\n# rates_core builds the population of lines (cell x tier x death phase), runs the years through wdt_kernel and tallies the flows.\n# The route mechanics (growth, consumption, declared W, ONE assessment on total W, allocation across routes, settlement per route,\n# ratio-mirror refund, verification, death and heir) are the kernel\'s; nothing in this layer duplicates them. See the module\n# docstring, ROUTES AND THE KERNEL.\n\n_ABCD = (\'A\', \'B\', \'C\', \'D\')\n_RB_MODES = (\'sale\', \'lien\', \'income\')\n_KERNEL_DEATH_KINDS = (\'verify_death\', \'tax_death_C\', \'tax_death\', \'death_D\', \'death_B\', \'tax_heir\')\n\n\ndef _archetype_table(p):\n    """The [archetypes.*] blocks, ordered by launch wealth: (names, V0 in £m (k,), route shares over A B C D (k, 4), external income / wealth (k,))."""\n    arch = p.get(\'archetypes\')\n    if not arch:\n        raise ValueError("p[\'archetypes\'] is missing: wdt_core.load_params must expose the [archetypes.*] blocks (valgen reads them too)")\n    names = sorted(arch, key=lambda k: float(arch[k][\'V0_m\']))\n    V0m = np.array([float(arch[k][\'V0_m\']) for k in names])\n    S = np.array([[float(arch[k][r]) for r in _ABCD] for k in names])\n    if np.abs(S.sum(axis=1) - 1.0).max() > 1e-9:\n        bad = [k for k, s in zip(names, S.sum(axis=1)) if abs(s - 1.0) > 1e-9]\n        raise ValueError(f\'[archetypes.*] route shares A + B + C + D must sum to 1; check {bad}\')\n    inc = p.get(\'income\') or {}\n    by = inc.get(\'by_archetype\') or {}\n    ratio = np.array([float(by.get(k, inc.get(\'default_ratio\', 0.0))) for k in names])\n    return names, V0m, S, ratio\n\n\ndef _curve(W, points):\n    """Linear in ln W between the anchor points (W in £m, value), flat beyond the end points."""\n    return np.interp(np.log(W), np.log([a for a, _ in points]), [b for _, b in points])\n\n\ndef _route_plan(cfg, cal, p):\n    """\n    Route plan of one calibration: how each cell\'s holdings split across the routes, and how Route B is paid. Returns\n    {\'cell\': dict | None, \'diag\': JSON-safe, \'summary\': JSON-safe}; \'cell\' is None for the earlier behaviour (everything in kind).\n    Route B mode: cfg[\'route_b_mode\'] (a scenario key) else [route_b].payment_mode:  sale | lien | income  (plan D4a / D4b).\n    cfg[\'route_mix\'] decides the shares:\n      \'none\'      all holdings in kind (Route C) except, in lien / income mode, the Route B share from [route_b].share_by_wealth\n                  (the earlier behaviour: with mode \'sale\' it reproduces the numbers the inline engine gave)\n      \'wealth\'    the archetype mixture by launch wealth: each of A / B / C / D is interpolated in ln W between the [archetypes.*]\n                  anchors (at their V0_m), flat beyond. External income / wealth likewise from [income.by_archetype]\n      \'blend\'     the same shares in every cell: the weights cfg[\'route_mix_weights\'] (archetype -> weight, sum 1) over the archetypes\n      <name>      one archetype ([archetypes.<name>]) everywhere: the archetype sweep\n    """\n    rb, inc = p.get(\'route_b\') or {}, p.get(\'income\') or {}\n    mode = cfg.get(\'route_b_mode\') or rb.get(\'payment_mode\', \'sale\')\n    if mode not in _RB_MODES:\n        raise ValueError(f"route_b_mode must be sale | lien | income, got {mode!r}")\n    mix = cfg.get(\'route_mix\') or \'none\'\n    W = np.maximum(np.asarray(cal[\'V0\'], float) * cal[\'y_ref_gbp_m\'], 1e-12)       # launch wealth per cell, £m\n    nc = len(W)\n    spread = cfg.get(\'deferral_spread\')\n    if spread is not None:\n        r_def = float(rb[\'sovereign_real_rate\']) + float(spread)                   # per-scenario deferral spread (D4c)\n    elif \'r_def\' in rb:\n        r_def = float(rb[\'r_def\'])\n    else:\n        r_def = float(rb[\'sovereign_real_rate\']) + float(rb[\'deferral_spread\'])\n    cap = float(cfg[\'income_cap\']) if cfg.get(\'income_cap\') is not None else float(inc.get(\'cap\', 1.0))\n    names = None\n    if mix == \'none\':\n        if mode == \'sale\':\n            shares, income = {\'C\': np.ones(nc)}, np.zeros(nc)\n        else:\n            if not rb.get(\'share_by_wealth\'):\n                raise ValueError(f"route_b_mode {mode!r} with route_mix \'none\' needs [route_b].share_by_wealth")\n            b = _curve(W, rb[\'share_by_wealth\'])\n            shares = {\'B\': b, \'C\': 1.0 - b}\n            income = (_curve(W, inc[\'ratio_by_wealth\']) if mode == \'income\' and inc.get(\'ratio_by_wealth\') else np.zeros(nc))\n    else:\n        names, V0m, S, ratio = _archetype_table(p)\n        if mix == \'wealth\':\n            lw, lx = np.log(W), np.log(V0m)\n            M = np.column_stack([np.interp(lw, lx, S[:, j]) for j in range(4)])\n            inc_c = np.interp(lw, lx, ratio)\n        elif mix == \'blend\':\n            wts = dict(cfg.get(\'route_mix_weights\') or {})\n            if not wts or set(wts) - set(names) or min(wts.values()) < 0.0 or abs(sum(wts.values()) - 1.0) > 1e-9:\n                raise ValueError(f"route_mix \'blend\' needs route_mix_weights: archetype -> weight >= 0, summing to 1, over {names}; got {wts}")\n            wv = np.array([float(wts.get(k, 0.0)) for k in names])\n            M, inc_c = np.tile(wv @ S, (nc, 1)), np.full(nc, float(wv @ ratio))\n        elif mix in names:\n            k = names.index(mix)\n            M, inc_c = np.tile(S[k], (nc, 1)), np.full(nc, float(ratio[k]))\n        else:\n            raise ValueError(f"route_mix must be \'none\' | \'wealth\' | \'blend\' | one of {names}, got {mix!r}")\n        M = M / M.sum(axis=1, keepdims=True)\n        shares = {r: M[:, j] for j, r in enumerate(_ABCD)}\n        income = inc_c if mode == \'income\' else np.zeros(nc)\n    baseline = mix == \'none\' and mode == \'sale\'\n    cell = None if baseline else {\'shares\': shares, \'mode\': mode, \'r_def\': r_def, \'cap\': cap, \'income\': income}\n\n    # JSON diagnostics: wealth-weighted route shares and external income / wealth by launch-wealth band\n    bid, nbd = cal[\'band_id\'], len(cal[\'bands\'][\'adult_share\'])\n    wsh = np.asarray(cal[\'share\'], float) * np.asarray(cal[\'V0\'], float)\n    den = np.bincount(bid, weights=wsh, minlength=nbd)\n\n    def by_band(x):\n        num = np.bincount(bid, weights=wsh * np.asarray(x, float), minlength=nbd)\n        return [float(a / b) if b > 0 else None for a, b in zip(num, den)]\n    diag = {\'mix\': mix, \'archetypes\': names, \'b_mode\': mode, \'r_def\': r_def, \'income_cap\': cap, \'in_kind_baseline\': bool(baseline),\n            \'note\': ("C = all holdings, settled in kind (the earlier engine)" if mix == \'none\'\n                     else \'A / B / D settle in cash-equivalent units at the true price, C in kind, D at death (plan D4a)\'),\n            \'band_edges_gbp_m\': cal[\'bands\'][\'edges_gbp_m\'],\n            \'band_wealth_share\': {r: by_band(s) for r, s in shares.items()},\n            \'band_income_ratio\': by_band(income)}\n    summary = {\'mode\': mode, \'deferral_spread\': cfg.get(\'deferral_spread\'), \'income_cap\': cfg.get(\'income_cap\'),\n               \'r_def\': r_def, \'cap\': cap, \'mix\': mix}\n    return {\'cell\': cell, \'diag\': diag, \'summary\': summary}\n\n\ndef _verification(cfg, p):\n    """\n    Verification inputs of a run (plan D6): lam_C, lam_D, death_verify, and the verify_down part of the rule set. Each of lam_C / lam_D /\n    death_verify is \'toml\' (read [verification]) or the scenario\'s own value. The corrective auction on Route D follows the rule set\'s\n    `dauc`, as in VAL. RATES lines are honest (alpha = 1), so these PASS THROUGH the kernel: with verify_down = \'allow\' they change nothing;\n    with \'reset\' a verification in a year the price FELL is a basis reset (no write-down credit), so an honest holder pays a little more.\n    """\n    v = p.get(\'verification\') or {}\n    rule = wc.resolve_rule(p, cfg[\'rule_set\'])\n\n    def lam(key, toml_key):\n        x = cfg.get(key, \'toml\')\n        return float(v.get(toml_key, 0.0)) if x == \'toml\' else float(x)\n    dv = cfg.get(\'death_verify\', \'toml\')\n    if dv not in (\'toml\', \'on\', \'off\'):\n        raise ValueError(f"death_verify must be \'toml\' | \'on\' | \'off\', got {dv!r}")\n    dauc = rule.get(\'dauc\', \'off\')\n    dauc_on = dauc is True or str(dauc).lower() in (\'on\', \'true\', \'1\')\n    lam_d = lam(\'lam_D\', \'lambda_D\')\n    return {\'lam_C\': lam(\'lam_C\', \'lambda_C\'), \'lam_D\': lam_d if dauc_on else 0.0, \'lam_D_input\': lam_d, \'dauc\': bool(dauc_on),\n            \'death_verify\': (bool(v.get(\'death_verifies\', False)) if dv == \'toml\' else dv == \'on\'),\n            \'verify_down\': rule.get(\'verify_down\', \'allow\')}\n\n\ndef _verification_block(cfg, p):\n    """JSON block: the [verification] table as read, and what this scenario ran with."""\n    ver = _verification(cfg, p)\n    return {\'toml\': p.get(\'verification\'), \'applied\': ver,\n            \'note\': \'honest lines (alpha = 1): lambda passes through the kernel; it can only bite via verify_down = reset in price-fall years\'}\n\n\ndef check_inputs(p):\n    """Fail early, with the fix, if the TOML / wdt_core do not carry what the kernel engine reads; warn on duplicated route inputs."""\n    d = p[\'rates\'][\'defaults\']\n    for k in (\'route_mix\', \'route_mix_weights\', \'lam_C\', \'lam_D\', \'death_verify\'):\n        if k not in d:\n            raise SystemExit(f"[rates.defaults] has no {k!r}: add it (apply_rates_s2.py does), and if it is in the TOML, "\n                             f"wdt_core\'s [rates] parser is dropping it: it must pass [rates.defaults] through")\n    _archetype_table(p)\n    rb, inc = p.get(\'route_b\') or {}, p.get(\'income\') or {}\n    names, V0m, S, ratio = _archetype_table(p)\n    for label, pts, ref in ((\'[route_b].share_by_wealth\', rb.get(\'share_by_wealth\'), S[:, 1]),\n                            (\'[income].ratio_by_wealth\', inc.get(\'ratio_by_wealth\'), ratio)):\n        if pts and (len(pts) != len(names) or any(abs(a - v) > 1e-9 or abs(b - r) > 1e-9 for (a, b), v, r in zip(pts, V0m, ref))):\n            print(f\'  WARNING {label} no longer matches the [archetypes.*] anchors (V0_m, B share / external income); \'\n                  f"route_mix \'none\' reads the former, route_mix \'wealth\' the latter", flush=True)\n\n\n# ── per-line state slicing: a death hits only the lines of one phase, and the kernel\'s step_death has no line mask ───────────────────\n# (request to the kernel owner: step_death(..., mask=None). Until it exists the lines that die are cut out of the Book, run through\n# step_death as a smaller Book and written back; every per-line array of the Book has shape (n,).)\n\ndef _take(v, m, n):\n    if isinstance(v, np.ndarray) and v.shape == (n,):\n        return v[m].copy()\n    if isinstance(v, dict):\n        return {k: _take(x, m, n) for k, x in v.items()}\n    return v\n\n\ndef _put(dst, src, m):\n    for k, v in src.items():\n        if isinstance(v, np.ndarray):\n            dst[k][m] = v\n        elif isinstance(v, dict):\n            _put(dst[k], v, m)\n\n\ndef _sub_book(book, m):\n    sub = copy.copy(book)\n    for k, v in vars(book).items():\n        setattr(sub, k, _take(v, m, book.n))\n    sub.n = int(m.sum())\n    return sub\n\n\ndef _write_back(book, sub, m):\n    for k, v in vars(sub).items():\n        if isinstance(v, np.ndarray):\n            getattr(book, k)[m] = v\n        elif isinstance(v, dict):\n            _put(getattr(book, k), v, m)\n\n\ndef _flow_value(fl, n):\n    """True value moved family -> state by one operation, per line (units sold at the true price, plus income cash)."""\n    v = np.zeros(n)\n    for x in fl.value.values():\n        v = v + x\n    return v + fl.income\n\n\ndef run_lines(g, idx, V0, w, group, nb, ph, G, c, rp, heir_rule=\'delta\', c_cap=\'units\', plan=None, ver=None):\n    """\n    The RATES engine: n weighted lines through wdt_kernel (S2; replaces the inline engine, plan D12).\n    g      (T, n) or (T,)  asset growth per year per line\n    idx    (T,)            threshold index factor for years 1..T\n    V0, w  (n,)            initial value and weight (weights sum to 1)\n    group  (n,) int        bracket id, for the by-bracket output;  nb = number of brackets\n    ph     (n,) int | None first-death year per line (None = no deaths);  G generation gap\n    c      float or (n,)   consumption share per year\n    rp     dict            tau_0, tau_m, k, wmin (engine units); optional schedule / ladder\n    heir_rule \'delta\' (baseline) | \'fresh\' (ablation: no tax on the receipt, basis = value)\n    c_cap     \'units\' | \'units_and_value\' (see wdt_core.parse_rule)\n    plan   dict | None     per-LINE route plan {\'shares\': {route: (n,)}, \'mode\', \'r_def\', \'cap\', \'income\': (n,)}; None = everything in kind (Route C)\n    ver    dict | None     {\'lam_C\', \'lam_D\', \'death_verify\', \'verify_down\'} (see _verification); None = no verification\n\n    Honest lines (alpha = 1). The fund counts SETTLED value only (D4d): a Route B lien balance and an accrued Route D liability are\n    returned as receivables (lien_out, accr_d_out), never as receipts; the horizon does not settle them.\n    Returns weighted length-T arrays: tax, refund, heir, lien (Route B lien settled at deaths), dsettle (Route D settled at deaths),\n    stake, share_paying, wealth, lien_out, accr_d_out, income (net external income paid to the state), plus by_bracket (T, nb),\n    heir_by_bracket, lien_out_b, income_b, income_gross_b, b_sold_b, wealth_by_bracket and wealth0_by_bracket.\n    """\n    T = len(idx)\n    n = len(V0)\n    g = np.asarray(g, float)\n    if g.ndim == 1:\n        g = np.repeat(g[:, None], n, axis=1)\n    V0 = np.asarray(V0, float)\n    w = np.asarray(w, float)\n    if heir_rule not in (\'delta\', \'fresh\'):\n        raise ValueError(f"heir_rule must be \'delta\' or \'fresh\', got {heir_rule!r}")\n    heir_influx = \'delta\' if heir_rule == \'delta\' else \'fresh_entrant\'\n    ver = ver or {}\n    lam_C, lam_D = float(ver.get(\'lam_C\', 0.0)), float(ver.get(\'lam_D\', 0.0))\n    death_verify, verify_down = bool(ver.get(\'death_verify\', False)), ver.get(\'verify_down\', \'allow\')\n    rate_fn = lambda x: wc.rate_vec(np.asarray(x, float), rp)\n\n    if plan is None:\n        shares, mode, r_def, cap, income = {\'C\': np.ones(n)}, \'sale\', 0.0, 0.0, np.zeros(n)\n    else:\n        shares, mode, r_def, cap, income = plan[\'shares\'], plan[\'mode\'], float(plan[\'r_def\']), float(plan[\'cap\']), np.asarray(plan[\'income\'], float)\n    routes = {r: s * V0 for r, s in shares.items() if np.any(np.asarray(s) > 0.0)}\n    has_cv = (lam_C > 0.0 or death_verify) and \'C\' in routes\n    book = wk.Book(n, routes, has_cv=has_cv, b_mode=mode, c_cap=c_cap, verify_down=verify_down, r_def=r_def,\n                   inc_allow=cap * income * V0)\n\n    tax = np.zeros(T)\n    ref = np.zeros(T)\n    heir = np.zeros(T)\n    lienv = np.zeros(T)\n    dsettle = np.zeros(T)\n    stake = np.zeros(T)\n    npay = np.zeros(T)\n    wealth = np.zeros(T)\n    lien_out = np.zeros(T)\n    accr_d = np.zeros(T)\n    inc_net = np.zeros(T)\n    by_b = np.zeros((T, nb))\n    heir_b = np.zeros((T, nb))\n    wealth_b = np.zeros((T, nb))\n    lien_out_b = np.zeros((T, nb))\n    inc_b = np.zeros((T, nb))\n    inc_gross_b = np.zeros((T, nb))\n    sold_b = np.zeros((T, nb))\n    wealth0_b = np.bincount(group, weights=w * V0, minlength=nb)\n    bc = lambda x: np.bincount(group, weights=x, minlength=nb)\n\n    for t in range(1, T + 1):\n        pt = np.zeros(n)                 # assessments this year (the year\'s, and the death corrections): units sold + income cash\n        hv = np.zeros(n)                 # heir tax\n        lv = np.zeros(n)                 # Route B lien settled at death\n        dv = np.zeros(n)                 # Route D settled at death\n        iv = np.zeros(n)                 # net external income paid\n        ig = np.zeros(n)                 # ... gross (positive parts)\n        sg = np.zeros(n)                 # Route B units sold (income mode: the shortfall)\n\n        def note(fl, m, size):\n            i = fl.income\n            iv_ = (iv if m is None else iv[m])\n            if m is None:\n                iv[:] += i\n                ig[:] += np.maximum(i, 0.0)\n            else:\n                iv[m] += i\n                ig[m] += np.maximum(i, 0.0)\n            if mode == \'income\' and \'B\' in fl.value:\n                sb = np.maximum(fl.value[\'B\'], 0.0)\n                if m is None:\n                    sg[:] += sb\n                else:\n                    sg[m] += sb\n\n        for kind, fl in wk.step_year(book, rate_fn, idx[t - 1], g[t - 1], c, 1.0, 1.0, lam_C, lam_D, False):\n            if kind == \'tax\':\n                pt += _flow_value(fl, n)\n                note(fl, None, n)\n\n        if ph is not None and t < T:\n            d = (t >= ph) & (((t - ph) % G) == 0)\n            if d.any():\n                sub = _sub_book(book, d)\n                for kind, fl in wk.step_death(sub, rate_fn, idx[t - 1], heir_influx, death_verify):\n                    if kind not in _KERNEL_DEATH_KINDS:\n                        raise ValueError(f\'wdt_kernel.step_death returned an operation this engine does not tally: {kind!r}\')\n                    v = _flow_value(fl, sub.n)\n                    if kind in (\'tax_death_C\', \'tax_death\'):\n                        pt[d] += v\n                    elif kind == \'tax_heir\':\n                        hv[d] += v\n                    elif kind == \'death_B\':\n                        lv[d] += v\n                    elif kind == \'death_D\':\n                        dv[d] += v\n                    note(fl, d, sub.n)\n                _write_back(book, sub, d)\n\n        pt = np.where(np.abs(pt) < 1e-12, 0.0, pt)      # rounding dust is neither tax nor refund\n        wp, wh, wl, wd = w * pt, w * hv, w * lv, w * dv\n        tax[t - 1] = wp[pt > 0.0].sum()\n        ref[t - 1] = wp[pt < 0.0].sum()\n        npay[t - 1] = w[pt > 0.0].sum()\n        heir[t - 1] = wh.sum()\n        lienv[t - 1] = wl.sum()\n        dsettle[t - 1] = wd.sum()\n        by_b[t - 1] = bc(wp + wh + wl + wd)\n        heir_b[t - 1] = bc(wh)\n        inc_net[t - 1] = (w * iv).sum()\n        inc_b[t - 1] = bc(w * iv)\n        inc_gross_b[t - 1] = bc(w * ig)\n        sold_b[t - 1] = bc(w * sg)\n        fam = book.family_true()\n        stake[t - 1] = (w * sum(x[\'s\'] * x[\'V\'] for x in book.R.values())).sum()\n        wealth[t - 1] = (w * fam).sum()\n        wealth_b[t - 1] = bc(w * fam)\n        lien_out[t - 1] = (w * book.LB).sum()\n        lien_out_b[t - 1] = bc(w * book.LB)\n        accr_d[t - 1] = (w * book.A_D).sum()\n\n    for name, a in ((\'tax\', tax), (\'wealth\', wealth), (\'stake\', stake), (\'dsettle\', dsettle)):\n        if not np.isfinite(a).all():\n            print(f\'\\nNon-finite {name} in the kernel engine: first at t={int(np.flatnonzero(~np.isfinite(a))[0]) + 1}\', flush=True)\n    return {\'tax\': tax, \'refund\': ref, \'heir\': heir, \'stake\': stake, \'share_paying\': npay,\n            \'lien\': lienv, \'lien_out\': lien_out, \'lien_out_b\': lien_out_b, \'dsettle\': dsettle, \'accr_d_out\': accr_d,\n            \'income\': inc_net, \'income_b\': inc_b, \'income_gross_b\': inc_gross_b, \'b_sold_b\': sold_b,\n            \'by_bracket\': by_b, \'heir_by_bracket\': heir_b, \'wealth\': wealth,\n            \'wealth_by_bracket\': wealth_b, \'wealth0_by_bracket\': wealth0_b}\n\n\n'
BLOCK_B = 'def run_cohorts(scn, cal, tiers=None, n_phase=6, G=30, deaths=True,\n                heir_rule=\'delta\', c_cell=None, cell_diff=None, c_cap=\'units\', plan_cell=None, ver=None):\n    """\n    Aggregate honest WDT receipts for one scenario and calibration, through wdt_kernel (S2).\n    plan_cell  _route_plan(...)[\'cell\'] (per CELL route shares / Route B mode / income) or None = everything in kind\n    ver        _verification(...) dict or None\n    """\n    tiers = tiers or [(1.0, 0.0)]\n    tw = np.array([t[0] for t in tiers], float)\n    td = np.array([t[1] for t in tiers], float)\n    if abs(tw.sum() - 1.0) > 1e-9:\n        raise ValueError(\'tier weights must sum to 1\')\n    nb = len(cal[\'V0\'])\n    phs = _phases(n_phase, G) if deaths else [None]\n    lines = list(itertools.product(range(nb), range(len(tiers)), phs))\n    b_id = np.array([l[0] for l in lines])\n    t_id = np.array([l[1] for l in lines])\n    p_id = [l[2] for l in lines]\n    w = cal[\'share\'][b_id] * tw[t_id] / len(phs)\n    V0 = cal[\'V0\'][b_id]\n    cd = np.zeros(nb) if cell_diff is None else np.asarray(cell_diff, float)\n    g = scn[\'r\'][:, None] + td[t_id][None, :] + cd[b_id][None, :]\n    ph = np.array(p_id, int) if deaths else None\n    c_line = scn[\'c\'] if c_cell is None else np.asarray(c_cell, float)[b_id]\n    plan = None\n    if plan_cell is not None:\n        plan = {\'shares\': {r: np.asarray(s, float)[b_id] for r, s in plan_cell[\'shares\'].items()},\n                \'mode\': plan_cell[\'mode\'], \'r_def\': plan_cell[\'r_def\'], \'cap\': plan_cell[\'cap\'],\n                \'income\': np.asarray(plan_cell[\'income\'], float)[b_id]}\n    raw = run_lines(g, scn[\'idx\'], V0, w, b_id, nb, ph, G, c_line, cal[\'rate\'],\n                    heir_rule=heir_rule, c_cap=c_cap, plan=plan, ver=ver)\n\n    norm = 1.0 / (scn[\'yy\'] * cal[\'pop_per_adult\'])\n    out = {k: raw[k] * norm for k in (\'tax\', \'refund\', \'heir\', \'stake\', \'wealth\', \'lien\', \'lien_out\', \'dsettle\', \'accr_d_out\', \'income\')}\n    out[\'wealth_gdp\'] = out.pop(\'wealth\')            # family-held net worth / GDP: stationarity diagnostic\n    out[\'income_gdp\'] = out.pop(\'income\')            # external income paid to the state (Route B income mode), net of any refund\n    out[\'net\'] = out[\'tax\'] + out[\'refund\'] + out[\'heir\'] + out[\'lien\'] + out[\'dsettle\']\n    out[\'coverage\'] = out[\'net\'] / scn[\'exp_gdp\']\n    out[\'share_paying\'] = raw[\'share_paying\']\n    out[\'by_bracket\'] = raw[\'by_bracket\'] * norm[:, None]\n    out[\'lien_out_b\'] = raw[\'lien_out_b\'] * norm[:, None]\n    out[\'income_b_gdp\'] = raw[\'income_b\'] * norm[:, None]\n    prev_w = np.vstack([raw[\'wealth0_by_bracket\'][None, :], raw[\'wealth_by_bracket\'][:-1]])\n    out[\'lvl\'] = {\'net_b\': raw[\'by_bracket\'], \'wealth_b\': raw[\'wealth_by_bracket\'],\n                  \'gain_b\': scn[\'r\'][:, None] * prev_w, \'prev_b\': prev_w,\n                  \'heir_b\': raw[\'heir_by_bracket\'], \'income_b\': raw[\'income_b\'],\n                  \'income_gross_b\': raw[\'income_gross_b\'], \'b_sold_b\': raw[\'b_sold_b\'],\n                  \'wealth0_b\': raw[\'wealth0_by_bracket\']}\n    out[\'exp_gdp\'] = scn[\'exp_gdp\']\n    out[\'years\'] = scn[\'years\']\n    return out\n\n\n'

RUN_WINDOW_CALL_OLD = """cell_diff=cal.get('cell_diff'), c_cap=wc.resolve_rule(p, cfg['rule_set'])['c_cap'],
                      rb_cell=_route_b_cell(cfg, cal, p))"""
RUN_WINDOW_CALL_NEW = """cell_diff=cal.get('cell_diff'), c_cap=wc.resolve_rule(p, cfg['rule_set'])['c_cap'],
                      plan_cell=_route_plan(cfg, cal, p)['cell'], ver=_verification(cfg, p))"""

REXTRA_ANCHOR = "    return {\n        'iso': iso, 'start': start, 'mode': mode, 'era': _era(start, rp['eras']),"
REXTRA_NEW = """    # S2: Route D settled / accrued, external income paid (Route B income mode; INCLUDED in tax_gdp_mean and net, shown separately), shares of GDP.
    # accr_d_out is a receivable (NOT in the fund, like lien_out). Cumulative = sum over the window's years.
    rextra = {'dsettle_gdp_mean': float(out['dsettle'].mean()), 'accr_d_gdp_end': float(out['accr_d_out'][-1]),
              'accr_d_gdp_max': float(out['accr_d_out'].max()),
              'income_gdp_mean': float(out['income_gdp'].mean()), 'income_cum_gdp': float(out['income_gdp'].sum())}
    for i_, v_ in enumerate(np.bincount(cal['band_id'], weights=out['income_b_gdp'].sum(axis=0), minlength=nbd_)):
        rextra[f'income_cum_gdp_band{i_}'] = float(v_)
    return {
        'iso': iso, 'start': start, 'mode': mode, 'era': _era(start, rp['eras']),"""
RETURN_TAIL_OLD = "        **extra,\n    }\n\n\ndef sweep("
RETURN_TAIL_NEW = "        **extra, **rextra,\n    }\n\n\ndef sweep("

RB_BLOCK_OLD = """        'route_b': {'mode': cfg.get('route_b_mode') or (p.get('route_b') or {}).get('payment_mode', 'sale'),
                    'deferral_spread': cfg.get('deferral_spread'), 'income_cap': cfg.get('income_cap')},
    }"""
RB_BLOCK_NEW = """        'route_b': {'mode': cfg.get('route_b_mode') or (p.get('route_b') or {}).get('payment_mode', 'sale'),
                    'deferral_spread': cfg.get('deferral_spread'), 'income_cap': cfg.get('income_cap')},
        'routes': _route_plan(cfg, cal, p)['diag'],                      # S2: A/B/C/D shares by launch-wealth band, mix, Route B mode
        'verification_applied': _verification_block(cfg, p),             # S2: lambda pass-through
    }"""

TOML_DEFAULTS_ANCHOR = "start_stride     = 1            # take every k-th start year (speed; 1 = all)\n"
TOML_DEFAULTS_NEW = TOML_DEFAULTS_ANCHOR + """# S2 (Work Order Wave 1 S2): routes and verification. The defaults below reproduce the earlier engine (all in kind; Route B only via route_b_mode).
route_mix        = "none"       # "none" | "wealth" (archetype mixture interpolated by launch wealth) | "blend" (route_mix_weights, same in every cell) | an [archetypes.*] name
route_mix_weights = {}          # for route_mix = "blend": archetype -> weight, summing to 1
lam_C            = "toml"       # Route C verification hazard: "toml" = [verification].lambda_C, or a number
lam_D            = "toml"       # Route D corrective-auction hazard: "toml" = [verification].lambda_D, or a number (acts only if the rule set's dauc is on)
death_verify     = "toml"       # "toml" = [verification].death_verifies | "on" | "off"
"""

TOML_RUNLIST_ANCHOR = '  "gl_rb_income_cap50",\n]\n'
TOML_RUNLIST_NEW = ('  "gl_rb_income_cap50",\n'
                    '  # route mixture and archetype sweep (S2)\n'
                    '  "gl_arch_wealth", "gl_arch_housing_pension", "gl_arch_startup_founder", "gl_arch_generational", "gl_arch_ceo_fintech",\n'
                    '  "gl_arch_resource_monopoly", "gl_arch_blend", "gl_arch_wealth_lien", "gl_arch_wealth_income",\n'
                    '  "gl_arch_wealth_lam005", "gl_arch_wealth_lam005_dv",\n]\n')

TOML_SCEN = '''
# ═══ S2 patch (apply_rates_s2.py): route mixture and archetype sweep on the gain ladder. Only the route inputs differ from [rates.scenarios.gain_ladder].
# route_mix "wealth" = the [archetypes.*] shares interpolated by launch wealth; an archetype name = that archetype in every cell.
# Route B mode stays "sale" (cash-equivalent units) unless a scenario sets route_b_mode.
'''
_ARCH = [('gl_arch_wealth', 'Gain ladder, A/B/C/D mixture by launch wealth (archetypes interpolated)', 'route_mix = "wealth"'),
         ('gl_arch_housing_pension', 'Gain ladder, every cell the Housing and pension archetype', 'route_mix = "housing_pension"'),
         ('gl_arch_startup_founder', 'Gain ladder, every cell the Start-up founder archetype', 'route_mix = "startup_founder"'),
         ('gl_arch_generational', 'Gain ladder, every cell the Generational wealth archetype', 'route_mix = "generational"'),
         ('gl_arch_ceo_fintech', 'Gain ladder, every cell the CEO / fintech archetype', 'route_mix = "ceo_fintech"'),
         ('gl_arch_resource_monopoly', 'Gain ladder, every cell the Resource monopoly archetype', 'route_mix = "resource_monopoly"'),
         ('gl_arch_blend', 'Gain ladder, 50/50 blend of Housing and pension and Generational wealth', 'route_mix = "blend"\nroute_mix_weights = { housing_pension = 0.5, generational = 0.5 }'),
         ('gl_arch_wealth_lien', 'Gain ladder, wealth mixture, Route B deferred lien', 'route_mix = "wealth"\nroute_b_mode = "lien"'),
         ('gl_arch_wealth_income', 'Gain ladder, wealth mixture, Route B paid from income', 'route_mix = "wealth"\nroute_b_mode = "income"'),
         ('gl_arch_wealth_lam005', 'Gain ladder, wealth mixture, lambda_C = lambda_D = 5% (pass-through)', 'route_mix = "wealth"\nlam_C = 0.05\nlam_D = 0.05'),
         ('gl_arch_wealth_lam005_dv', 'Gain ladder, wealth mixture, lambda 5%, death verifies Route C', 'route_mix = "wealth"\nlam_C = 0.05\nlam_D = 0.05\ndeath_verify = "on"')]
for _n, _l, _b in _ARCH:
    TOML_SCEN += (f'\n[rates.scenarios.{_n}]\nlabel = "{_l}"\nwmin_house_ratio = 1.0\nschedule = "gain_ladder"\n'
                  f'dist_kw = {{ body_split = 5, body_split_from = 0.5 }}\n{_b}\n')


def read(path):
    raw = path.read_bytes().decode('utf-8')
    crlf = '\r\n' in raw
    return raw.replace('\r\n', '\n'), crlf


def write(path, text, crlf):
    path.write_bytes((text.replace('\n', '\r\n') if crlf else text).encode('utf-8'))


def once(text, old, new, what):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'ANCHOR FAILED ({what}): found {n} times, expected 1. Nothing written for this file.')
    return text.replace(old, new)


def span(text, start, end, new, what):
    """Replace text[start:end) where `start` and `end` are line-start markers (each must occur once)."""
    if text.count(start) != 1 or text.count(end) != 1:
        raise SystemExit(f'ANCHOR FAILED ({what}): start x{text.count(start)}, end x{text.count(end)}, expected 1 each.')
    i, j = text.index(start), text.index(end)
    if j < i:
        raise SystemExit(f'ANCHOR FAILED ({what}): end before start.')
    return text[:i] + new.rstrip('\n') + '\n\n\n' + text[j:]


def patch_rates(text):
    t = text
    t = once(t, 'import argparse\nimport hashlib\n', 'import argparse\nimport copy\nimport hashlib\n', 'import copy')
    t = once(t, 'import wdt_core as wc\n', 'import wdt_core as wc\nimport wdt_kernel as wk                                      # S2: the route engine\n', 'import wdt_kernel')
    t = span(t, 'def load_jst(rp):', 'def countries(J):', '', 'remove duplicate load_jst')
    t = span(t, 'def valid_windows(d, cols, length, exclude=None):', '# ═════════════════════════════════════════════════════════════════════════════\n# L1  DIST', '', 'remove valid_windows')
    t = span(t, 'def _route_b_cell(cfg, cal, p):', 'def _phases(n_phase, G):', BLOCK_A, 'replace route-b cell + run_lines')
    t = span(t, 'def run_cohorts(scn, cal,', 'def effective_rates(out, cal,', BLOCK_B, 'replace run_cohorts')
    t = once(t, RUN_WINDOW_CALL_OLD, RUN_WINDOW_CALL_NEW, 'run_window call')
    t = once(t, REXTRA_ANCHOR, REXTRA_NEW, 'rextra')
    t = once(t, RETURN_TAIL_OLD, RETURN_TAIL_NEW, 'rextra return')
    t = once(t, RB_BLOCK_OLD, RB_BLOCK_NEW, 'run_scenario block')
    t = once(t, "    J = load_jst(p['rates'])\n", "    check_inputs(p)\n    J = load_jst(p['rates']['jst_path'])\n", 'main')
    return t


def patch_toml(text):
    t = once(text, TOML_DEFAULTS_ANCHOR, TOML_DEFAULTS_NEW, 'toml defaults')
    t = once(t, TOML_RUNLIST_ANCHOR, TOML_RUNLIST_NEW, 'toml run list')
    return t.rstrip('\n') + '\n' + TOML_SCEN


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--model-dir', default=None)
    a = ap.parse_args(argv)
    here = Path(__file__).resolve().parent
    cands = [Path(a.model_dir)] if a.model_dir else [here, here.parent]
    mdir = next((c for c in cands if (c / 'WDT_Params.toml').exists() and (c / 'RATES' / 'rates_core.py').exists()), None)
    if mdir is None:
        raise SystemExit(f'WDT_Params.toml and RATES/rates_core.py not found in {[str(c) for c in cands]}; use --model-dir')
    rc, tm = mdir / 'RATES' / 'rates_core.py', mdir / 'WDT_Params.toml'
    rtext, rcr = read(rc)
    ttext, tcr = read(tm)
    r_done, t_done = MARK in rtext, 'route_mix' in ttext and 'gl_arch_wealth' in ttext
    if r_done and t_done:
        print('already applied; nothing to do')
        return 0
    if r_done != t_done:
        raise SystemExit('PARTIAL STATE: one of rates_core.py / WDT_Params.toml is patched, the other not. Restore the .pre_s2 copy and rerun.')
    new_r, new_t = patch_rates(rtext), patch_toml(ttext)       # both computed before anything is written
    compile(new_r, str(rc), 'exec')
    for src in (rc, tm):
        bak = src.with_name(src.name + '.pre_s2')
        if not bak.exists():
            bak.write_bytes(src.read_bytes())
    write(rc, new_r, rcr)
    write(tm, new_t, tcr)
    print(f'patched {rc} and {tm} (backups: *.pre_s2)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
