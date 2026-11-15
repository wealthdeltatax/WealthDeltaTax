#!/usr/bin/env python3
"""
apply_phase2_valgen.py -- Route B lien / income, death verification and archetype runs in valgen_core.py
(WDT_Refactor_Plan.md D4b, D4c, D6, section 4). Additive: every new switch defaults to the earlier behaviour,
so with route_b='sale', income_ratio=0 and death_verify=False the engine is unchanged (checked by P6 check 1).

Run AFTER apply_basis_change.py and apply_phase2_params.py.   Usage: python apply_phase2_valgen.py MODEL_DIR [--check]
Backup: valgen_core.py.pre_p2.bak. Exact-match replacement, each OLD snippet exactly once; re-run safe.
New engine switches on run_family3: route_b, r_def, income_ratio, income_cap, death_verify.
New validator _p6_validate and archetype report _p6_archetypes (new JSON key 'p6'), run in main after P5.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from apply_basis_change import patch_text, locate

PATCHES = [('module constants: Route B modes',
  "_C_CAP = ('units', 'units_and_value')\n",
  "_C_CAP = ('units', 'units_and_value')\n"
  "_B_MODES = ('sale', 'lien', 'income')   # Route B payment mode (D4b/D4c)\n"),
 ('new functions _assess_B, _settle_B',
  'def _verify_C(led, t, S, lam):\n',
  'def _assess_B(led, t, kind, S, Lr, x, receipts):\n'
  '    """\n'
  "    Route B tax under the lien and income scenarios (D4b / D4c). Lr is this route's share of the\n"
  "    year's assessment (+ tax, - refund). Declared value is the true value (alpha = 1), as in sale mode.\n"
  '      lien    a tax is not collected: it is added to the deferred balance LB, which accrues at r_def\n'
  '              and is settled by sale of units at death or the horizon (_settle_B). A refund cancels LB '
  'first.\n'
  "      income  a tax is paid from external income, up to this year's allowance (inc_left); any shortfall "
  'is met\n'
  '              by the sale of units, as in sale mode. A refund returns income paid (this generation) '
  'first.\n'
  "    Any refund beyond that follows the sale-mode rule (pooled real-value cap, the state's stake in B).\n"
  '    """\n'
  "    mode = S['b_mode']\n"
  '    if Lr > 0.0:\n'
  "        if mode == 'lien':\n"
  "            S['LB'] += Lr\n"
  '            return\n'
  "        pay = min(Lr, S['inc_left'])\n"
  '        if pay > 0.0:\n'
  "            S['inc_left'] -= pay\n"
  "            S['inc_paid']  += pay\n"
  "            S['inc_total'] += pay\n"
  "            led.post(t, f'{kind}_income', 'income', 'state_cash', pay, route='B')\n"
  "            receipts.append((t, f'{kind}_B_income', pay, pay))\n"
  '        short = Lr - pay\n'
  '        if short > 0.0:\n'
  "            _p3_move(led, t, kind, S, 'B', short / x['V'])\n"
  "            S['E_cash'] += short\n"
  "            receipts.append((t, f'{kind}_B', short, short))\n"
  '        return\n'
  '    rest = -Lr\n'
  "    if mode == 'lien':\n"
  "        red = min(rest, S['LB'])\n"
  "        S['LB'] -= red\n"
  '        rest    -= red\n'
  '    else:\n'
  "        ret = min(rest, S['inc_paid'])\n"
  '        if ret > 0.0:\n'
  "            led.post(t, f'{kind}_income_refund', 'state_cash', 'income', ret, route='B')\n"
  "            S['inc_paid'] -= ret\n"
  '            rest          -= ret\n'
  "            receipts.append((t, f'{kind}_B_income', -ret, -ret))\n"
  "    val = min(rest, S['E_cash'], x['s'] * x['V'])\n"
  "    S['lost_refund'] += rest - val\n"
  '    if val > 0.0:\n'
  "        _p3_move(led, t, kind, S, 'B', -val / x['V'])\n"
  "        S['E_cash'] -= val\n"
  "        receipts.append((t, f'{kind}_B', -val, -val))\n"
  '\n'
  '\n'
  'def _settle_B(led, t, S, kind, receipts):\n'
  '    """Lien scenario: settle the deferred balance by selling Route B units at the true price (death, '
  'horizon)."""\n'
  "    x = S['R'].get('B')\n"
  "    if x is None or S['b_mode'] != 'lien' or S['LB'] <= 0.0:\n"
  "        S['LBp'] = S['LB']\n"
  '        return\n'
  "    units = min(S['LB'] / x['V'], x['f'])\n"
  "    val   = _p3_move(led, t, kind, S, 'B', units)\n"
  "    S['E_cash']   += val\n"
  "    S['unpaid_B'] += S['LB'] - val\n"
  '    receipts.append((t, kind, val, val))\n'
  "    S['LB'] = 0.0\n"
  "    S['LBp'] = 0.0\n"
  '\n'
  '\n'
  'def _verify_C(led, t, S, lam):\n'),
 ('_assess_multi: declared wealth net of the lien',
  "    R = S['R']\n"
  '    W_new, W_prev = sum(Wn.values()), sum(Wp.values())\n'
  '    rate  = tau(W_new / idx, sim_p)\n'
  '    delta = W_new - W_prev\n'
  '    d     = {r: Wn[r] - Wp[r] for r in R}\n'
  '    if delta > 0.0:\n',
  "    R = S['R']\n"
  "    lien  = S['b_mode'] == 'lien' and 'B' in R\n"
  "    adj_n = S['LB'] if lien else 0.0          # declared wealth is net of the deferred balance (D4b)\n"
  "    adj_p = S['LBp'] if lien else 0.0\n"
  '    W_new, W_prev = max(sum(Wn.values()) - adj_n, 0.0), max(sum(Wp.values()) - adj_p, 0.0)\n'
  '    rate  = tau(W_new / idx, sim_p)\n'
  '    delta = W_new - W_prev\n'
  '    d     = {r: Wn[r] - Wp[r] for r in R}\n'
  '    if lien:\n'
  "        d['B'] -= adj_n - adj_p\n"
  '    if delta > 0.0:\n'),
 ('_assess_multi: early return keeps the lien basis',
  '    else:\n        return rate, delta, 0.0\n    tot = sum(w.values())\n',
  "    else:\n        S['LBp'] = S['LB']\n        return rate, delta, 0.0\n    tot = sum(w.values())\n"),
 ('_assess_multi: Route B under lien / income',
  "        x = R[r]\n        if r in ('A', 'B'):\n",
  '        x = R[r]\n'
  "        if r == 'B' and S['b_mode'] != 'sale':\n"
  '            _assess_B(led, t, kind, S, Lr, x, receipts)\n'
  "        elif r in ('A', 'B'):\n"),
 ('_assess_multi: lien basis after the assessment',
  "                    receipts.append((t, f'{kind}_D', -val, -val))\n    return rate, delta, L\n",
  "                    receipts.append((t, f'{kind}_D', -val, -val))\n"
  "    S['LBp'] = S['LB']\n"
  '    return rate, delta, L\n'),
 ('run_family3: signature',
  '                verify_hazard_D: float = 0.0) -> dict:\n',
  "                verify_hazard_D: float = 0.0, route_b: str = 'sale', r_def: float = 0.0,\n"
  '                income_ratio: float = 0.0, income_cap: float = 1.0, death_verify: bool = False) -> '
  'dict:\n'),
 ('run_family3: docstring for the new switches',
  '    shares          route shares of V0 (A, B, C, D); zero-share routes are dropped.\n',
  "    route_b         Route B payment mode (D4b/D4c). 'sale' (default): cash-equivalent units, as before.\n"
  "                    'lien': the tax is added to a deferred balance accruing at r_def, settled by sale of "
  'units\n'
  "                    at death and the horizon; declared wealth is net of the balance. 'income': paid from "
  'external\n'
  '                    income (income_cap x income_ratio x V0_m x index per year), the shortfall by sale of '
  'units.\n'
  '    death_verify    death verifies Route C with certainty (D6): all unverified C units move to the '
  'verified tranche\n'
  '                    at the death date and the correction is assessed (needs Route C).\n'
  '    shares          route shares of V0 (A, B, C, D); zero-share routes are dropped.\n'),
 ('run_family3: validation of the new switches',
  '    if not 0.0 <= verify_hazard <= 1.0:\n'
  "        raise ValueError(f'verify_hazard must be in [0, 1], got {verify_hazard!r}')\n",
  '    if not 0.0 <= verify_hazard <= 1.0:\n'
  "        raise ValueError(f'verify_hazard must be in [0, 1], got {verify_hazard!r}')\n"
  '    if route_b not in _B_MODES:\n'
  "        raise ValueError(f'route_b must be one of {_B_MODES}, got {route_b!r}')\n"
  '    if not 0.0 <= income_cap <= 1.0:\n'
  "        raise ValueError(f'income_cap must be in [0, 1], got {income_cap!r}')\n"
  '    if income_ratio < 0.0:\n'
  "        raise ValueError(f'income_ratio must be >= 0, got {income_ratio!r}')\n"
  '    if r_def <= -1.0:\n'
  "        raise ValueError(f'r_def must be > -1, got {r_def!r}')\n"),
 ('run_family3: death verification adds the verified tranche',
  "    has_cv = verify_hazard > 0.0 and 'C' in routes\n",
  "    has_cv = (verify_hazard > 0.0 or death_verify) and 'C' in routes\n"),
 ('run_family3: ledger accounts for income and state cash',
  "                          + [f'state_{r}' for r in routes]))\n",
  "                          + [f'state_{r}' for r in routes] + ['income', 'state_cash']))\n"),
 ('run_family3: state for Route B scenarios',
  "         'verify_down': verify_down, 'vD': 0.0}\n",
  "         'verify_down': verify_down, 'vD': 0.0,\n"
  "         'b_mode': route_b, 'LB': 0.0, 'LBp': 0.0, 'unpaid_B': 0.0,\n"
  "         'inc_left': 0.0, 'inc_paid': 0.0, 'inc_total': 0.0}\n"
  "    inc_allow = income_cap * income_ratio * p['V0_m']      # external income per year at t = 0, grows "
  'with the index\n'),
 ('run_family3: yearly lien accrual and income allowance',
  '        idx = (1.0 + index_rate) ** t\n'
  '        reset_year = reset_interval > 0 and t % reset_interval == 0\n',
  '        idx = (1.0 + index_rate) ** t\n'
  "        S['LB'] *= 1.0 + r_def                       # deferred balance accrues (lien)\n"
  "        S['inc_left'] = inc_allow * idx              # this year's income available for the WDT (income)\n"
  '        reset_year = reset_interval > 0 and t % reset_interval == 0\n'),
 ('run_family3: death verifies Route C',
  "            deaths.append(t)\n            if 'D' in S['R']:\n",
  '            deaths.append(t)\n'
  '            if death_verify and has_cv:                  # death verifies Route C with certainty (D6)\n'
  '                _verify_C(led, t, S, 1.0)\n'
  "                Wn_v = {r: S['R'][r]['f'] * S['R'][r]['dd'] for r in routes}\n"
  "                Wp_v = {r: S['R'][r]['Wp'] for r in routes}\n"
  "                _assess_multi(led, t, 'tax_death_C', S, Wn_v, Wp_v, idx, sim_p, receipts)\n"
  '                for r in routes:\n'
  "                    S['R'][r]['Wp'] = S['R'][r]['f'] * S['R'][r]['dd']\n"
  "                    S['R'][r]['ppu'] = S['R'][r]['dd']\n"
  "            if 'D' in S['R']:\n"),
 ('run_family3: settle the lien at death, reset income',
  "            S['uo'] = {'C': 0.0, 'Cv': 0.0}\n            S['EC'] = 0.0\n            S['E_cash'] = 0.0\n",
  "            _settle_B(led, t, S, 'death_B', receipts)\n"
  "            S['uo'] = {'C': 0.0, 'Cv': 0.0}\n"
  "            S['EC'] = 0.0\n"
  "            S['E_cash'] = 0.0\n"
  "            S['inc_paid'] = 0.0                      # the heir starts with a clean income envelope and a "
  "full year's income\n"
  "            S['inc_left'] = inc_allow * idx\n"),
 ('run_family3: settle the lien at the horizon',
  "    _settle_D(led, T, S, 'terminal_D', receipts)\n    _p3_check(led, S, diag)\n    R = S['R']\n",
  "    _settle_D(led, T, S, 'terminal_D', receipts)\n"
  "    _settle_B(led, T, S, 'terminal_B', receipts)\n"
  '    _p3_check(led, S, diag)\n'
  "    R = S['R']\n"),
 ("run_family3: state cash in the state's holdings",
  "        'state_true_T':  sum(x['s'] * x['V'] for x in R.values()),\n",
  "        'state_true_T':  sum(x['s'] * x['V'] for x in R.values()) + led.bal['state_cash'],\n"),
 ('run_family3: Route B outputs',
  "        'lost_refund': S['lost_refund'], 'unpaid_D': S['unpaid_D'],\n"
  "        'receipts': receipts, 'rows': rows, 'ledger': led, 'diag': diag,\n"
  '    }\n',
  "        'lost_refund': S['lost_refund'], 'unpaid_D': S['unpaid_D'],\n"
  "        'route_b': route_b, 'unpaid_B': S['unpaid_B'], 'income_paid': S['inc_total'],\n"
  "        'receipts': receipts, 'rows': rows, 'ledger': led, 'diag': diag,\n"
  '    }\n'),
 ('_phase2_opts before _p5_opts',
  'def _p5_opts(p, rule, lam):\n',
  'def _phase2_opts(p):\n'
  '    """Phase 2 switches from the parameter file ([route_b], [income], [verification]); empty if absent.\n'
  "    p['archetype'] (set by _p6_archetypes) selects the external-income ratio from "
  '[income.by_archetype]."""\n'
  "    rb, inc, ver = p.get('route_b'), p.get('income'), p.get('verification')\n"
  '    out = {}\n'
  '    if rb:\n'
  "        out.update(route_b=rb['payment_mode'], r_def=rb['r_def'])\n"
  '    if inc:\n'
  "        out.update(income_ratio=inc['by_archetype'].get(p.get('archetype'), inc['default_ratio']),\n"
  "                   income_cap=inc['cap'])\n"
  '    if ver:\n'
  "        out.update(death_verify=ver['death_verifies'])\n"
  '    return out\n'
  '\n'
  '\n'
  'def _p5_opts(p, rule, lam):\n'),
 ('_p5_opts carries the phase-2 switches',
  "                verify_down=verify_down, verify_hazard_D=(lam if dauc == 'on' else 0.0))\n",
  "                verify_down=verify_down, verify_hazard_D=(lam if dauc == 'on' else 0.0),\n"
  '                **_phase2_opts(p))\n'),
 ('P6 validator and archetype runs before _clean',
  'def _clean(obj):\n',
  '# ─────────────────────────────────────────────────────────────\n'
  '# P6 — ROUTE B LIEN / INCOME, DEATH VERIFICATION, ARCHETYPES\n'
  '# ─────────────────────────────────────────────────────────────\n'
  '\n'
  "_P6_MODES = ('sale', 'lien', 'income')\n"
  '\n'
  '\n'
  'def _p6_lien_hand(pf: dict, g: float, T: int, r_def: float) -> tuple:\n'
  '    """Independent hand recursion for a Route B-only family under the lien, flat rate, honest, no '
  'deaths.\n'
  '    Declared wealth is net of the lien; the tax on a rise is tau x delta and is added to the balance, '
  'which\n'
  '    accrues at r_def from the next year. Returns (LB at T, family true wealth at T, V_T)."""\n'
  "    V, LBp, tau0 = pf['V0_m'], 0.0, pf['tau_0']\n"
  '    for _ in range(T):\n'
  '        V_prev = V\n'
  '        V *= 1.0 + g\n'
  '        LBa = LBp * (1.0 + r_def)\n'
  '        delta = (V - LBa) - (V_prev - LBp)\n'
  '        L = tau0 * delta\n'
  '        if delta <= 0.0:\n'
  "            raise ValueError('hand case needs a rising net wealth every year')\n"
  '        LBp = LBa + L\n'
  '    return LBp, V - LBp, V\n'
  '\n'
  '\n'
  'def _p6_validate(p: dict) -> tuple[dict, dict]:\n'
  '    """P6 checks: defaults inert, hand cases for the lien and income scenarios, conservation, death '
  'verification."""\n'
  '    checks, info = {}, {}\n'
  '\n'
  "    def check(name, ok, detail=''):\n"
  "        checks[name] = {'ok': bool(ok), 'detail': detail}\n"
  '        if not ok:\n'
  "            raise AssertionError(f'VALIDATION FAILED: {name} {detail}')\n"
  '\n'
  "    vg, g, rho = p['val_gen'], p['g'], p['rho']\n"
  "    T, G = vg['T'], vg['G']\n"
  "    ir = _ir(p) if vg['index_wmin'] else 0.0\n"
  '    ser = [g] * T\n'
  '    fp = _flat(p)\n'
  "    rb = p.get('route_b') or {}\n"
  "    r_def = rb.get('r_def', 0.025)\n"
  "    base = dict(consumption=vg['consumption'], index_rate=ir, shares=dict(vg['route_shares']),\n"
  "                reset_interval=vg['reset_interval'], death_waiver=vg['death_waiver'])\n"
  '    d6 = _p3_new_diag()\n'
  '\n'
  '    def absorb(run):\n'
  "        d = run['diag']\n"
  "        for key in ('cons_err', 'unit_err', 'uout_err'):\n"
  '            d6[key] = max(d6[key], d[key])\n'
  "        for key in ('min_E_cash', 'min_A_D', 'min_u_out', 'min_state_units'):\n"
  '            d6[key] = min(d6[key], d[key])\n'
  "        led = run['ledger']\n"
  "        if abs(sum(led.bal.values())) > 1e-9 * max(1.0, run['family_true_T']):\n"
  "            raise AssertionError('P6 ledger does not balance')\n"
  "        if abs(led.bal['income'] + led.bal['state_cash']) > 1e-9 * max(1.0, run['family_true_T']):\n"
  "            raise AssertionError('P6 income account does not equal state cash')\n"
  '\n'
  '    # 1. the new switches at their defaults reproduce the earlier engine exactly\n'
  '    worst = 0.0\n'
  '    for aC, aD in ((1.0, 1.0), (0.5, 0.5), (2.0, 0.5)):\n'
  "        r0 = run_family3(p, aC, aD, ser, G, 'delta', **base)\n"
  "        r1 = run_family3(p, aC, aD, ser, G, 'delta', route_b='sale', r_def=r_def, income_ratio=0.0,\n"
  '                         income_cap=1.0, death_verify=False, **base)\n'
  '        absorb(r1)\n'
  "        worst = max(worst, abs(r1['family_true_T'] - r0['family_true_T']) + abs(r1['state_true_T'] - "
  "r0['state_true_T']))\n"
  "    check('p6_defaults_reproduce_sale_engine', worst < 1e-12, f'max diff={worst:.2e}')\n"
  '\n'
  '    # 2. lien hand case: Route B only, flat rate, honest, no deaths\n'
  '    Th = 30\n'
  "    sh_b = dict(shares={'B': 1.0}, consumption=0.0, index_rate=0.0, reset_interval=0, death_waiver=0)\n"
  '    worst = 0.0\n'
  '    for rd in (0.0, 0.025, 0.06):\n'
  "        run = run_family3(fp, 1.0, 1.0, [g] * Th, None, 'delta', route_b='lien', r_def=rd, **sh_b)\n"
  '        absorb(run)\n'
  '        LB, fam, V_T = _p6_lien_hand(fp, g, Th, rd)\n'
  "        worst = max(worst, abs(run['family_true_T'] - fam) / V_T, abs(run['state_true_T'] - LB) / V_T)\n"
  "        info[f'lien_hand_LB_T_r{rd}'] = LB\n"
  "    check('p6_lien_matches_hand_recursion', worst < 1e-9, f'max rel diff={worst:.2e}')\n"
  '\n'
  '    # 3. income hand case: ample income pays every tax; no units move; the state holds cash\n'
  "    rich = run_family3(fp, 1.0, 1.0, [g] * Th, None, 'delta', route_b='income', income_ratio=1e6,\n"
  '                       income_cap=1.0, **sh_b)\n'
  '    absorb(rich)\n'
  "    V, tax = fp['V0_m'], 0.0\n"
  '    for _ in range(Th):\n'
  '        V_prev = V\n'
  '        V *= 1.0 + g\n'
  "        tax += fp['tau_0'] * (V - V_prev)\n"
  "    cash = rich['ledger'].bal['state_cash']\n"
  "    check('p6_income_hand_case_state_cash_equals_sum_of_tax',\n"
  "          abs(cash - tax) < 1e-9 * V and abs(rich['family_true_T'] - V) < 1e-9 * V and rich['unpaid_B'] "
  '== 0.0\n'
  "          and abs(rich['income_paid'] - cash) < 1e-12,\n"
  '          f\'state cash {cash:.4f} vs hand {tax:.4f}; family {rich["family_true_T"]:.4f} vs V_T '
  "{V:.4f}')\n"
  '\n'
  '    # 4. income that is too small: the shortfall is sold, and the value moved equals the tax assessed\n'
  "    short = run_family3(fp, 1.0, 1.0, [g] * Th, None, 'delta', route_b='income', income_ratio=0.002,\n"
  '                        income_cap=1.0, **sh_b)\n'
  '    absorb(short)\n'
  "    credited = sum(c_ for (_, _k, _v, c_) in short['receipts'])\n"
  "    assessed = sum(x_['L'] for x_ in short['rows'] if 'L' in x_)\n"
  "    check('p6_income_shortfall_is_sold_and_conserved',\n"
  "          0.0 < short['income_paid'] < tax and short['f_T']['B'] < 1.0\n"
  "          and abs(credited - assessed) < 1e-9 * V and short['diag']['cons_err'] < CONSERVE_TOL,\n"
  '          f"income paid {short[\'income_paid\']:.3f}; units kept {short[\'f_T\'][\'B\']:.4f}; "\n'
  '          f"credited receipts {credited:.4f} vs assessed {assessed:.4f}")\n'
  '\n'
  '    # 5. zero income = sale mode exactly\n'
  '    worst = 0.0\n'
  '    for aC, aD in ((1.0, 1.0), (0.5, 0.5)):\n'
  "        r0 = run_family3(p, aC, aD, ser, G, 'delta', route_b='sale', **base)\n"
  "        r1 = run_family3(p, aC, aD, ser, G, 'delta', route_b='income', income_ratio=0.0, **base)\n"
  '        absorb(r1)\n'
  "        worst = max(worst, abs(r1['family_true_T'] - r0['family_true_T']) + abs(r1['state_true_T'] - "
  "r0['state_true_T']))\n"
  "    check('p6_zero_income_equals_sale', worst < 1e-12, f'max diff={worst:.2e}')\n"
  '\n'
  '    # 6. a higher deferral rate leaves the family poorer (hand case and the family mix with deaths)\n'
  "    lo = run_family3(fp, 1.0, 1.0, [g] * Th, None, 'delta', route_b='lien', r_def=0.01, "
  "**sh_b)['family_true_T']\n"
  "    hi = run_family3(fp, 1.0, 1.0, [g] * Th, None, 'delta', route_b='lien', r_def=0.08, "
  "**sh_b)['family_true_T']\n"
  "    mix = dict(base, shares={'A': 0.3, 'B': 0.5, 'C': 0.1, 'D': 0.1})\n"
  "    lo2 = run_family3(p, 1.0, 1.0, ser, G, 'delta', route_b='lien', r_def=0.01, **mix)['family_true_T']\n"
  "    hi2 = run_family3(p, 1.0, 1.0, ser, G, 'delta', route_b='lien', r_def=0.08, **mix)['family_true_T']\n"
  "    check('p6_lien_family_wealth_falls_with_deferral_rate', hi < lo and hi2 < lo2,\n"
  "          f'hand {lo:.2f} -> {hi:.2f}; mix {lo2:.2f} -> {hi2:.2f}')\n"
  '\n'
  '    # 7. conservation, ledger balance and caps over modes x strategies x shares, with deaths\n'
  '    n_runs = 0\n'
  '    for mode in _P6_MODES:\n'
  "        for shares in (dict(base['shares']), {'A': 0.2, 'B': 0.5, 'C': 0.2, 'D': 0.1}):\n"
  "            for ratio in ((0.0,) if mode != 'income' else (0.0, 0.01, 0.2)):\n"
  '                for aC, aD in ((1.0, 1.0), (0.5, 0.5), (2.0, 0.5), (0.1, 2.0)):\n'
  '                    for dv in (False, True):\n'
  "                        run = run_family3(p, aC, aD, ser, G, 'delta', route_b=mode, r_def=r_def,\n"
  '                                          income_ratio=ratio, death_verify=dv, **dict(base, '
  'shares=shares))\n'
  '                        absorb(run)\n'
  '                        n_runs += 1\n'
  "    check('p6_conservation_and_caps_all_modes',\n"
  "          d6['cons_err'] < CONSERVE_TOL and d6['unit_err'] < CONSERVE_TOL and d6['min_E_cash'] > -1e-9\n"
  "          and d6['min_A_D'] > -1e-12 and d6['min_u_out'] > -1e-12 and d6['min_state_units'] > -1e-12\n"
  '          and d6[\'uout_err\'] < 1e-12, f"{n_runs} runs; cons {d6[\'cons_err\']:.1e}, unit '
  '{d6[\'unit_err\']:.1e}")\n'
  '\n'
  '    # 8. death verification is inert for the honest family\n'
  '    worst = 0.0\n'
  "    for lam in (0.0, vg['lambda_base']):\n"
  "        a0 = run_family3(p, 1.0, 1.0, ser, G, 'delta', verify_hazard=lam, **base)\n"
  "        a1 = run_family3(p, 1.0, 1.0, ser, G, 'delta', verify_hazard=lam, death_verify=True, **base)\n"
  '        absorb(a1)\n'
  "        worst = max(worst, abs(a1['family_true_T'] - a0['family_true_T']) / a0['family_true_T'],\n"
  "                    abs(a1['state_true_T'] - a0['state_true_T']) / a0['state_true_T'])\n"
  "    check('p6_death_verification_inert_for_honest_family', worst < 1e-9, f'max rel diff={worst:.2e}')\n"
  '\n'
  '    # 9. death verification takes the understatement gain away (C-heavy mix, alpha_C = 0.5)\n'
  "    heavy = dict(base, shares={'A': 0.5, 'C': 0.5})\n"
  '    gains = {}\n'
  '    for dv in (False, True):\n'
  "        h = run_family3(p, 1.0, 1.0, ser, G, 'delta', death_verify=dv, **heavy)\n"
  "        gains[dv] = family3_pair(p, 0.5, 1.0, ser, G, 'delta', rho, honest=h, death_verify=dv, "
  "**heavy)['gain']\n"
  "    info['death_verify_gain_alpha_C_0.5'] = {'off': gains[False], 'on': gains[True]}\n"
  "    check('p6_death_verification_erodes_understatement_gain', gains[True] < gains[False] - 1e-9,\n"
  "          f'{gains[False]:+.3%} without, {gains[True]:+.3%} with')\n"
  '\n'
  '    # 10. invalid switches raise\n'
  '    bad = 0\n'
  "    for kw in ({'route_b': 'x'}, {'income_cap': 1.5}, {'income_ratio': -0.1}, {'r_def': -1.5}):\n"
  '        try:\n'
  "            run_family3(p, 1.0, 1.0, ser, G, 'delta', **kw)\n"
  '        except ValueError:\n'
  '            bad += 1\n'
  "    check('p6_invalid_switch_values_raise', bad == 4, f'{bad} of 4 raised')\n"
  '    return checks, info\n'
  '\n'
  '\n'
  'def _p6_breakeven_spread(pm: dict, ser: list, target_pv: float, o: dict) -> float | None:\n'
  '    """Deferral spread over the sovereign real rate at which the PV of the state\'s receipts under the '
  'lien equals\n'
  '    the sale-mode PV (the state is indifferent to the deferral). Bisection on [-4%, +30%]; None if not '
  'bracketed."""\n'
  "    vg, rb = pm['val_gen'], pm['route_b']\n"
  '\n'
  '    def f(s):\n'
  "        q = dict(pm, route_b=dict(rb, payment_mode='lien', r_def=rb['sovereign_real_rate'] + s))\n"
  "        run = run_family3(q, 1.0, 1.0, ser, vg['G'], vg['heir_influx'], **dict(o, **_phase2_opts(q)))\n"
  "        return pv_true(run, pm['rho']) - target_pv\n"
  '    lo, hi = -0.04, 0.30\n'
  '    flo, fhi = f(lo), f(hi)\n'
  '    if flo * fhi > 0.0:\n'
  '        return None\n'
  '    for _ in range(60):\n'
  '        mid = 0.5 * (lo + hi)\n'
  '        fm = f(mid)\n'
  '        if flo * fm <= 0.0:\n'
  '            hi = mid\n'
  '        else:\n'
  '            lo, flo = mid, fm\n'
  '    return 0.5 * (lo + hi)\n'
  '\n'
  '\n'
  'def _p6_archetypes(p: dict) -> dict:\n'
  '    """The five archetypes of plan section 4 through the family engine: honest outcomes under sale, lien '
  'and\n'
  '    income, the best-response gain under the candidate rule (lambda 0 and the base lambda), and the '
  'breakeven\n'
  '    deferral spread. Empty if the parameter file has no [archetypes] / [route_b] block."""\n'
  "    arch, rb = p.get('archetypes'), p.get('route_b')\n"
  '    if not arch or not rb:\n'
  '        return {}\n'
  "    vg = p['val_gen']\n"
  "    ser = [p['g']] * vg['T']\n"
  '    strategies = _strategies(p)\n'
  "    lams = (0.0, vg['lambda_base'])\n"
  '    out = {}\n'
  '    for name, a in arch.items():\n'
  "        pa = dict(p, V0_m=a['V0_m'], val_gen=dict(vg, route_shares=dict(a['shares'])), archetype=name)\n"
  "        row = {'label': a['label'], 'V0_m': a['V0_m'], 'shares': dict(a['shares']),\n"
  "               'income_ratio': _phase2_opts(pa).get('income_ratio', 0.0), 'modes': {}}\n"
  '        for mode in _P6_MODES:\n'
  '            pm = dict(pa, route_b=dict(rb, payment_mode=mode))\n'
  '            o = _p5_opts(pm, _CANDIDATE_RULE, 0.0)\n'
  "            h = run_family3(pm, 1.0, 1.0, ser, vg['G'], vg['heir_influx'], **o)\n"
  "            cell = {'TW': h['family_true_T'], 'PV': pv_true(h, p['rho']), 'state_true_T': "
  "h['state_true_T'],\n"
  "                    'income_paid': h['income_paid'], 'unpaid_B': h['unpaid_B'], 'best': {}}\n"
  '            for lam in lams:\n'
  '                s = _p5_search(pm, _CANDIDATE_RULE, lam, strategies)\n'
  "                cell['best'][str(lam)] = {'gain': s['best']['gain'], 'label': s['best']['label'],\n"
  "                                          'BRG': s['BRG_pass'], 'SPT': s['SPT_pass'], 'SST': "
  "s['SST_pass']}\n"
  "            row['modes'][mode] = cell\n"
  "        pm = dict(pa, route_b=dict(rb, payment_mode='lien'))\n"
  "        row['breakeven_spread'] = _p6_breakeven_spread(pm, ser, row['modes']['sale']['PV'],\n"
  '                                                       _p5_opts(pm, _CANDIDATE_RULE, 0.0))\n'
  '        out[name] = row\n'
  '    return out\n'
  '\n'
  '\n'
  'def _p6_print(arch: dict):\n'
  '    if not arch:\n'
  "        print('  (no [archetypes] / [route_b] in the parameter file: archetype runs skipped)')\n"
  '        return\n'
  '    for name, r_ in arch.items():\n'
  "        sh = ' '.join(f'{k}{v:.0%}' for k, v in r_['shares'].items())\n"
  "        be = r_['breakeven_spread']\n"
  '        print(f"  {name} (V0 £{r_[\'V0_m\']:g}m; {sh}; income/wealth {r_[\'income_ratio\']:.1%}); "\n'
  '              f"breakeven deferral spread {\'not bracketed in [-4%, +30%]\' if be is None else format(be, '
  '\'+.2%\')} (state receipts PV equal to sale)")\n'
  "        for mode, c in r_['modes'].items():\n"
  "            b0, b1 = c['best']['0.0'], list(c['best'].values())[-1]\n"
  '            print(f"    {mode:<7} honest TW £{c[\'TW\']:,.1f}m, state PV £{c[\'PV\']:,.1f}m, income paid '
  '£{c[\'income_paid\']:,.1f}m, "\n'
  '                  f"unpaid B £{c[\'unpaid_B\']:,.2f}m; best response {b0[\'gain\']:+.1%} (lambda 0), '
  '{b1[\'gain\']:+.1%} (base lambda)")\n'
  '\n'
  '\n'
  'def _clean(obj):\n'),
 ('main: run P6',
  "    validation['checks'].update(p5_checks)\n",
  "    validation['checks'].update(p5_checks)\n"
  '\n'
  "    print('[9b] P6 Route B lien / income, death verification, archetypes...')\n"
  '    p6_checks, p6_info = _p6_validate(p)\n'
  '    for name, c in p6_checks.items():\n'
  '        print(f"  PASS  {name} {c[\'detail\']}")\n'
  "    validation['checks'].update(p6_checks)\n"
  '    p6_arch = _p6_archetypes(p)\n'
  '    _p6_print(p6_arch)\n'
  "    p6_out = {'checks': p6_checks, 'info': p6_info, 'archetypes': p6_arch}\n"),
 ('main: P6 output in the JSON',
  "    assert all('|' in k for k in data['p3_surface']['cells']), 'p3_surface.cells overwritten'\n",
  "    data['p6'] = p6_out\n"
  "    assert all('|' in k for k in data['p3_surface']['cells']), 'p3_surface.cells overwritten'\n")]


def main(argv):
    if len(argv) < 2 or argv[1].startswith('--'):
        print(__doc__); return 2
    root, check_only = Path(argv[1]), '--check' in argv
    path = locate(root, 'valgen_core.py', argv[argv.index('--valgen') + 1] if '--valgen' in argv else None)
    raw = path.read_bytes().decode('utf-8'); crlf = '\r\n' in raw
    text = raw.replace('\r\n', '\n')
    try:
        new_text, log = patch_text(text, PATCHES, 'valgen_core.py')
    except RuntimeError as e:
        print(f'ABORT {e}'); return 1
    print(f"{path} ({'CRLF' if crlf else 'LF'}): " + ('changes pending' if new_text != text else 'no changes'))
    print('\n'.join(log))
    if check_only or new_text == text:
        return 0
    bak = path.with_name(path.name + '.pre_p2.bak')
    if not bak.exists():
        bak.write_bytes(path.read_bytes())
    compile(new_text, str(path), 'exec')
    path.write_bytes((new_text.replace('\n', '\r\n') if crlf else new_text).encode('utf-8'))
    print(f'  wrote {path} (backup {bak.name}); syntax OK')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
