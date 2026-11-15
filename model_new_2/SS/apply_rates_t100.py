"""
apply_rates_t100.py  --  RATES to T = 100, receivable reporting, Route B by band, effective-window table.
Plan D7, D4d, section 5 items 2, 3, 6; section 9 open question 3 (cap sweep) and the spread sweep.

    python apply_rates_t100.py MODEL_DIR --check     (reports anchors, writes nothing)
    python apply_rates_t100.py MODEL_DIR             (backups *.pre_t100.bak, then writes)

Prerequisites already run: apply_basis_change, apply_phase2_params / _valgen / _rates, wire_jst_loop.
Every edit needs its anchor to be found EXACTLY once, or nothing is written. CRLF files are handled.

WHAT IT CHANGES
 TOML   [rates.defaults] T 30 -> 100;  [rates.representativeness] block_years 30 -> 100 (block = T);
        run.scenarios += nine Route B scenarios; [rates.figures] route_b = [...]; scenarios appended:
        gl_rb_sale, gl_rb_lien (spread 1%), gl_rb_lien_sp0 / _sp3 / _sp6 / _sp12 (deferral spread 0, 3, 6, 12%),
        gl_rb_income (cap 100%), gl_rb_income_cap75, gl_rb_income_cap50.  All = the gain ladder with only Route B changed.
 wdt_core  scenario keys income_cap and deferral_spread (optional, validated); figures list 'route_b'.
 rates_core
   run_lines / run_cohorts : lien balance by bracket (lien_out_b).
   _route_b_cell           : income_cap and deferral_spread per scenario (else [income].cap and [route_b].r_def).
   run_window new columns  : lien_out_gdp_max, lien_out_gdp_at_fill, fund_gdp_end, fund_plus_recv_gdp_end (settled cash fund
                             plus the receivable, reported separately), and per launch-wealth band i:
                             recv_gdp_mean_band{i}, lien_out_gdp_end_band{i}, wealth_gdp_end_band{i}.
   run_scenario            : effective_windows (total / contiguous / wraps / repeat per mode and country, T stated),
                             verification (lambda_C, lambda_D, death_verifies passed through), route_b mode, spread, cap,
                             and the contiguous-only headline now carries the bootstrap too (n_eff, full loop vs contiguous).
   validate                : effective-window counts agree with the headline window counts.
 D4d: the fund already receives settled cash only (tax and refunds in units at value, income cash, lien SETTLED at deaths).
      The outstanding lien is NOT fed to the fund; it is the receivable columns above.
 D5: the engine already uses the ratio-mirror refund (run_lines, neg branch). Nothing to change.

NOT DONE: run time rises about 3x per window (T = 100) and rows rise (every usable year is a start); drift_band
[0.67, 1.5] was set for 30-year windows and will classify few 100-year windows as stable: revisit it with the first results.
Tables and charts for the new columns are not written.
"""
import re
import sys
from pathlib import Path


def rd(path):
    raw = Path(path).read_bytes().decode('utf-8')
    crlf = '\r\n' in raw
    return raw.replace('\r\n', '\n'), crlf


def wr(path, text, crlf):
    Path(path).write_bytes((text.replace('\n', '\r\n') if crlf else text).encode('utf-8'))


def plain(text, old, new, label, problems):
    n = text.count(old)
    if n != 1:
        problems.append(f'{label}: anchor found {n} times')
        return text
    return text.replace(old, new)


def rx(text, pattern, repl, label, problems, flags=re.M):
    new, n = re.subn(pattern, repl, text, flags=flags)
    if n != 1:
        problems.append(f'{label}: pattern matched {n} times')
        return text
    return new


# ───────────────────────── TOML ─────────────────────────
RB_SCENARIOS = ['gl_rb_sale', 'gl_rb_lien', 'gl_rb_lien_sp0', 'gl_rb_lien_sp3', 'gl_rb_lien_sp6', 'gl_rb_lien_sp12',
                'gl_rb_income', 'gl_rb_income_cap75', 'gl_rb_income_cap50']
_RB_DEF = {
    'gl_rb_sale': ('Gain ladder, Route B in cash-equivalent units (reference)', 'route_b_mode = "sale"'),
    'gl_rb_lien': ('Gain ladder, Route B deferred lien (spread from [route_b])', 'route_b_mode = "lien"'),
    'gl_rb_lien_sp0': ('Gain ladder, Route B lien, deferral spread 0%', 'route_b_mode = "lien"\ndeferral_spread = 0.0'),
    'gl_rb_lien_sp3': ('Gain ladder, Route B lien, deferral spread 3%', 'route_b_mode = "lien"\ndeferral_spread = 0.03'),
    'gl_rb_lien_sp6': ('Gain ladder, Route B lien, deferral spread 6%', 'route_b_mode = "lien"\ndeferral_spread = 0.06'),
    'gl_rb_lien_sp12': ('Gain ladder, Route B lien, deferral spread 12%', 'route_b_mode = "lien"\ndeferral_spread = 0.12'),
    'gl_rb_income': ('Gain ladder, Route B paid from income (cap from [income])', 'route_b_mode = "income"'),
    'gl_rb_income_cap75': ('Gain ladder, Route B from income, cap 75%', 'route_b_mode = "income"\nincome_cap = 0.75'),
    'gl_rb_income_cap50': ('Gain ladder, Route B from income, cap 50%', 'route_b_mode = "income"\nincome_cap = 0.5'),
}


def toml_block():
    out = ['', '# ═══ T100 patch (apply_rates_t100.py): Route B scenarios on the gain ladder. Only Route B differs from [rates.scenarios.gain_ladder].',
           '# Shares and income ratios come from [route_b].share_by_wealth and [income].ratio_by_wealth (PLACEHOLDERS).', '']
    for name in RB_SCENARIOS:
        label, extra = _RB_DEF[name]
        out += [f'[rates.scenarios.{name}]', f'label = "{label}"', 'wmin_house_ratio = 1.0', 'schedule = "gain_ladder"',
                'dist_kw = { body_split = 5, body_split_from = 0.5 }', extra, '']
    return '\n'.join(out)


def patch_toml(t, problems):
    if '[rates.scenarios.gl_rb_lien]' in t:
        problems.append('TOML: already patched')
        return t
    t = rx(t, r'^(T\s*=\s*)30(\s*# window length)', r'\g<1>100\g<2>', 'TOML [rates.defaults] T', problems)
    t = rx(t, r'^(block_years\s*=\s*)30\b', r'\g<1>100   # = T (D7)', 'TOML block_years', problems)
    names = ''.join(f'  "{n}",\n' for n in RB_SCENARIOS)
    t = plain(t, '  "gain_ladder_rule_base",\n]',
              '  "gain_ladder_rule_base",\n  # Route B lien / income (T100 patch)\n' + names + ']', 'TOML run.scenarios', problems)
    lst = ', '.join(f'"{n}"' for n in RB_SCENARIOS)
    t = rx(t, r'^(levy\s+=\s+\["gl_levy_cal_nominal".*\])$',
           lambda m: m.group(1) + '\n# T22b / F22b (not written yet): Route B sale, lien (spread sweep), income (cap sweep)\n'
           + f'route_b      = [{lst}]', 'TOML figures.route_b', problems)
    return t.rstrip('\n') + '\n' + toml_block()


# ───────────────────────── wdt_core ─────────────────────────
def patch_core(t, problems):
    t = plain(t, "'anchor_from', 'route_b_mode')", "'anchor_from', 'route_b_mode', 'income_cap', 'deferral_spread')",
              'wdt_core _RATES_OPTIONAL', problems)
    t = plain(t, "lists = ('decomposition', 'rate_grid', 'schedules', 'cohorts', 'scope', 'stack', 'headline', 'consumption', 'levy')",
              "lists = ('decomposition', 'rate_grid', 'schedules', 'cohorts', 'scope', 'stack', 'headline', 'consumption', 'levy', 'route_b')",
              'wdt_core figures lists', problems)
    t = plain(t, '    for k in _RATES_INTS:\n',
              "    if out.get('income_cap') is not None and not 0.0 <= float(out['income_cap']) <= 1.0:\n"
              "        raise ValueError('income_cap must be in [0, 1]')\n"
              "    if out.get('deferral_spread') is not None and float(out['deferral_spread']) <= -1.0:\n"
              "        raise ValueError('deferral_spread must be > -1')\n"
              "    if out.get('route_b_mode') not in (None, 'sale', 'lien', 'income'):\n"
              "        raise ValueError(\"route_b_mode must be sale | lien | income\")\n"
              '    for k in _RATES_INTS:\n', 'wdt_core _rates_cfg checks', problems)
    return t


# ───────────────────────── rates_core ─────────────────────────
RBANDS = '''
    # T100 patch: Route B by launch-wealth band. recv = mean annual receipts (tax, refunds, heir, lien settled; income cash counted),
    # lien_out = receivable outstanding at the window end (NOT in the fund), wealth = family wealth at the window end. Shares of GDP.
    nbd_ = len(cal['bands']['adult_share'])
    rbands = {}
    for i_, v_ in enumerate(np.bincount(cal['band_id'], weights=out['by_bracket'].mean(axis=0), minlength=nbd_)):
        rbands[f'recv_gdp_mean_band{i_}'] = float(v_)
    for i_, v_ in enumerate(np.bincount(cal['band_id'], weights=out['lien_out_b'][-1], minlength=nbd_)):
        rbands[f'lien_out_gdp_end_band{i_}'] = float(v_)
    for i_, v_ in enumerate(np.bincount(cal['band_id'], weights=out['lvl']['wealth_b'][-1] / scale[-1], minlength=nbd_)):
        rbands[f'wealth_gdp_end_band{i_}'] = float(v_)'''

RECV_KEYS = ('''
        'lien_out_gdp_max': float(out['lien_out'].max()),
        'lien_out_gdp_at_fill': (float(out['lien_out'][fy - 1]) if fy else np.nan),
        'fund_gdp_end': float(f['S'][-1] / scale[-1]),
        'fund_plus_recv_gdp_end': float(f['S'][-1] / scale[-1] + out['lien_out'][-1]),''')

EFFW = '''def effective_windows(df, T):
    """
    Effective-window table (plan 5.6): per mode and country, how many windows there are and how many survive the contiguous-only
    check. total = every usable start year (the loop); contiguous = no seam crossed, no calendar gap; wraps = cross the seam;
    repeat = T longer than the usable series, so a year appears twice (kept, flagged). Independent windows are far fewer: see
    headline.<mode>.levy_variants.<case>.bootstrap n_eff.
    """
    def cnt(g):
        return {'total': int(len(g)), 'contiguous': int(g['contiguous'].astype(bool).sum()),
                'wraps': int(g['wraps'].astype(bool).sum()), 'repeat': int(g['repeat'].astype(bool).sum())}
    out = {'T': int(T), 'by_mode': {}}
    for mode, g in df.groupby('mode'):
        tot = cnt(g)
        tot['repeat_share'] = (tot['repeat'] / tot['total']) if tot['total'] else None
        out['by_mode'][mode] = {'overall': tot, 'by_country': {iso: cnt(x) for iso, x in g.groupby('iso')}}
    return out


'''

VALID = ('''        if 'effective_windows' in sc:
            for mode, ew in sc['effective_windows']['by_mode'].items():
                assert ew['overall']['total'] == sc['headline'][mode]['overall']['windows'], f'{name}/{mode}: effective-window total differs'
                assert ew['overall']['contiguous'] <= ew['overall']['total'], f'{name}/{mode}: contiguous > total'
''')


def patch_rates(t, problems):
    if 'effective_windows' in t:
        problems.append('rates_core: already patched')
        return t
    t = rx(t, r'^([ ]*)lien_out = np\.zeros\(T\)[^\n]*$',
           lambda m: m.group(0) + f'\n{m.group(1)}lien_out_b = np.zeros((T, nb))        # by bracket (T100 patch)', 'rates run_lines init', problems)
    t = rx(t, r'^([ ]*)lien_out\[t - 1\] = \(w \* LB\)\.sum\(\)$',
           lambda m: m.group(0) + f'\n{m.group(1)}lien_out_b[t - 1] = np.bincount(group, weights=w * LB, minlength=nb)', 'rates run_lines loop', problems)
    t = plain(t, "'lien': lienv, 'lien_out': lien_out,", "'lien': lienv, 'lien_out': lien_out, 'lien_out_b': lien_out_b,", 'rates run_lines return', problems)
    t = plain(t, "    out['by_bracket'] = raw['by_bracket'] * norm[:, None]",
              "    out['by_bracket'] = raw['by_bracket'] * norm[:, None]\n    out['lien_out_b'] = raw['lien_out_b'] * norm[:, None]", 'rates run_cohorts', problems)
    t = plain(t, "    spec = {'mode': mode, 'r_def': float(rb['r_def']), 'bshare': curve(rb['share_by_wealth']),",
              "    r_def_ = ((float(rb['sovereign_real_rate']) + float(cfg['deferral_spread'])) if cfg.get('deferral_spread') is not None\n"
              "              else float(rb['r_def']))                       # T100 patch: per-scenario deferral spread\n"
              "    cap_ = float(cfg['income_cap']) if cfg.get('income_cap') is not None else (float(inc['cap']) if inc else 1.0)\n"
              "    spec = {'mode': mode, 'r_def': r_def_, 'bshare': curve(rb['share_by_wealth']),", 'rates _route_b_cell spec', problems)
    t = plain(t, "            'cap': float(inc['cap']) if inc else 1.0}", "            'cap': cap_}", 'rates _route_b_cell cap', problems)
    t = rx(t, r"^    gpc_real_gm = float\(np\.prod\(1\.0 \+ gpc_r\)[^\n]*$", lambda m: m.group(0) + RBANDS, 'rates run_window rbands', problems)
    t = rx(t, r"^(\s*)'lien_gdp_mean': float\(out\['lien'\]\.mean\(\)\), 'lien_out_gdp_end': float\(out\['lien_out'\]\[-1\]\),$",
           lambda m: m.group(0) + RECV_KEYS, 'rates run_window recv keys', problems)
    t = plain(t, '**conc, **fund, **zuc, **bands, **var,', '**conc, **fund, **zuc, **bands, **rbands, **var,', 'rates run_window spread', problems)
    t = plain(t, 'def run_scenario(J, p, name, stride=None, countries_=None, verbose=True):',
              EFFW + 'def run_scenario(J, p, name, stride=None, countries_=None, verbose=True):', 'rates effective_windows def', problems)
    t = plain(t, "'headline_contiguous': headline(df[df['contiguous']], p, boot=False),",
              "'headline_contiguous': headline(df[df['contiguous'].astype(bool)], p, boot=name in p['rates']['representativeness']['bootstrap_scenarios']),",
              'rates headline_contiguous', problems)
    t = plain(t, "        'n_rows': int(len(df)),",
              "        'n_rows': int(len(df)),\n"
              "        'effective_windows': effective_windows(df, cfg['T']),\n"
              "        'verification': p.get('verification'),\n"
              "        'route_b': {'mode': cfg.get('route_b_mode') or (p.get('route_b') or {}).get('payment_mode', 'sale'),\n"
              "                    'deferral_spread': cfg.get('deferral_spread'), 'income_cap': cfg.get('income_cap')},", 'rates run_scenario block', problems)
    t = plain(t, "        if 'windows' in sc:\n            assert len(sc['windows']['rows']) == sc['n_rows']",
              VALID + "        if 'windows' in sc:\n            assert len(sc['windows']['rows']) == sc['n_rows']", 'rates validate', problems)
    return t


def main(argv):
    if not argv or argv[0].startswith('-'):
        raise SystemExit(__doc__)
    root = Path(argv[0])
    check = '--check' in argv
    paths = {'toml': root / 'WDT_Params.toml', 'core': root / 'wdt_core.py'}
    cand = [root / 'RATES' / 'rates_core.py', root / 'rates_core.py']
    rc = next((c for c in cand if c.exists()), None)
    if rc is None:
        raise SystemExit(f'rates_core.py not found under {root}')
    paths['rates'] = rc
    for k, v in paths.items():
        if not v.exists():
            raise SystemExit(f'missing {v}')
    fns = {'toml': patch_toml, 'core': patch_core, 'rates': patch_rates}
    new, problems = {}, []
    for k, path in paths.items():
        text, crlf = rd(path)
        new[k] = (fns[k](text, problems), crlf)
    if problems:
        print('NOTHING WRITTEN. Problems:')
        for pr in problems:
            print('  -', pr)
        raise SystemExit(1)
    print('All anchors found exactly once.')
    if check:
        print('--check: no files written.')
        return
    for k, path in paths.items():
        bak = path.with_name(path.name + '.pre_t100.bak')
        if not bak.exists():
            bak.write_bytes(path.read_bytes())
        wr(path, *new[k])
        print(f'patched {path}  (backup {bak.name})')
    print('Next: python -c "import wdt_core; wdt_core.load_rates_params()"  then  rates_core.py --quick --stride 5 --countries GBR USA JPN')


if __name__ == '__main__':
    main(sys.argv[1:])
