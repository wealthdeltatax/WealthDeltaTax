"""
apply_step2_rules_and_basis.py: STEP 2 (apply AFTER step 1, apply_val_rates_alignment.py).

Two things, one source of truth for each:

A. RULE SET shared by RATES and VAL
   wdt_core    parse_rule / resolve_rule: the rule-set key 'c_cap/verify_down/dauc' is parsed in ONE place.
               New TOML section [rules] names the two rule sets: base = units/allow/off, candidate = units_and_value/reset/on.
               p['rules'] is loaded by load_params AND load_rates_params.
   rates_core  run_lines gets c_cap ('units' | 'units_and_value'). Under 'units_and_value' a refund is also capped by the true
               value the line has paid net of refunds (valgen's EC cap), reset at each death. Default 'units' = old behaviour,
               bit-identical. [rates.defaults] rule_set = "candidate", so RATES now runs the rule that VAL proposes.
               verify_down and the corrective auction act only when alpha != 1, so they are inert for RATES' honest lines
               (valgen's check auction_switches_inert_for_honest_family); the rule keys carry them for when RATES gains gaming.
   TOML        new scenario gain_ladder_rule_base = the headline ladder under the BASE rule: the measured size of the value cap.

B. REAL basis for VAL (RATES default basis = "real")
   wdt_core    with_val_basis(p): if [val_gen] g_real is set, p['g'] = g_real (a REAL return); p['index_rate'] =
               [val_gen] index_rate (REAL GDP/head growth) else [budget] budget_growth. Both keys OMITTED = legacy numbers.
   valgen_core main() applies it; every index rate goes through _ir(p); meta records val_basis.
   Use print_val_real_inputs.py to get g_real and index_rate from the JST history RATES uses, then set them in [val_gen].

Numerics: with g_real and index_rate omitted, VAL is unchanged. In RATES the value cap CHANGES numbers (refunds after falls);
re-run rates_core.py (the new scenario is in [rates.run].scenarios), then tables and charts.

Usage (from the folder that holds wdt_core.py; other files are looked up here, one level up and below):
    python apply_step2_rules_and_basis.py            # dry run: checks every anchor, writes nothing
    python apply_step2_rules_and_basis.py --write    # applies, keeps <file>.bak next to each file
    python apply_step2_rules_and_basis.py --dir PATH
Every edit must match the expected number of times, or the script stops and writes NOTHING.
"""

import argparse
import re
import sys
import tomllib
from pathlib import Path

CORE_FUNCS = r'''

# ─────────────────────────────────────────────────────────────
# RULE SETS and the VAL basis (shared by RATES and VAL)
# ─────────────────────────────────────────────────────────────

_RULE_PARTS = {'c_cap': ('units', 'units_and_value'), 'verify_down': ('allow', 'reset'), 'dauc': ('off', 'on')}
_RULE_DEFAULTS = {'base': 'units/allow/off', 'candidate': 'units_and_value/reset/on'}


def parse_rule(rule):
    """
    Parse a rule-set key 'c_cap/verify_down/dauc' (trailing parts optional: units / allow / off) into
    {'c_cap', 'verify_down', 'dauc'}. Raises ValueError on an unknown part. The one parser for RATES and VAL.
      c_cap        units | units_and_value   Route C refund cap (the value cap stops a refund of more than the value paid)
      verify_down  allow | reset             correcting your own overstatement: write-down | basis reset with no refund
      dauc         off | on                  corrective auction also applies to Route D
    """
    parts = str(rule).split('/')
    if len(parts) > 3:
        raise ValueError(f'rule set {rule!r}: at most three parts (c_cap/verify_down/dauc)')
    out = {}
    for (key, allowed), val in zip(_RULE_PARTS.items(), parts + [None] * (3 - len(parts))):
        val = allowed[0] if val is None else val
        if val not in allowed:
            raise ValueError(f'rule set {rule!r}: {key} must be one of {allowed}, got {val!r}')
        out[key] = val
    return out


def _parse_rules(r):
    """[rules] section -> {'base', 'candidate'} (rule-set keys, validated). A missing section takes the defaults."""
    r = dict(r or {})
    out = {k: str(r.get(k, d)) for k, d in _RULE_DEFAULTS.items()}
    for v in out.values():
        parse_rule(v)
    return out


def resolve_rule(p, name):
    """Rule-set dict for `name`: 'base' | 'candidate' (looked up in p['rules']) or an explicit key such as 'units/reset/on'."""
    key = p['rules'].get(name, name) if isinstance(p.get('rules'), dict) else name
    return parse_rule(key)


def with_val_basis(p):
    """
    Copy of p on the basis VAL runs in. [val_gen] g_real (a REAL return) replaces p['g'] when set; [val_gen] index_rate
    (REAL GDP/head growth, the index RATES uses) is the W_min / k indexation, else [budget] budget_growth (legacy).
    Both omitted = the legacy numbers. Sets p['val_basis'] ('real' | 'legacy_nominal') and p['index_rate'].
    """
    vg = p['val_gen']
    q = dict(p)
    real = vg.get('g_real') is not None
    if real:
        q['g'] = float(vg['g_real'])
    q['index_rate'] = float(vg['index_rate']) if vg.get('index_rate') is not None else p['budget_growth']
    q['val_basis'] = 'real' if real else 'legacy_nominal'
    return q
'''

VALGEN_IR = '''def _ir(p: dict) -> float:
    """W_min / k index rate: p['index_rate'] (set by wdt_core.with_val_basis) else the legacy [budget] budget_growth."""
    return p.get('index_rate', p['budget_growth'])


'''

TOML_RULES = '''

# ─────────────────────────────────────────────────────────────
# [rules] — the two rule sets, named once for RATES and VAL
# A rule set is the key 'c_cap/verify_down/dauc' (see valgen_core, RULE SETS); wdt_core.parse_rule reads it.
#   base      the rule before the gaming fixes: Route C refund capped by units paid only
#   candidate the simple universal candidate: units and value cap, a verify-down is a basis reset, corrective auction on C and D
# [rates.defaults] rule_set = "base" | "candidate" | an explicit key. RATES honest lines feel only the c_cap part (verify_down and the
# auction act when alpha != 1); VAL searches all of it.
# ─────────────────────────────────────────────────────────────
[rules]
base      = "units/allow/off"
candidate = "units_and_value/reset/on"

[rates.scenarios.gain_ladder_rule_base]
label = "Gain ladder under the BASE rule set (units cap only): the value cap's effect"
rule_set = "base"
wmin_house_ratio = 1.0
schedule = "gain_ladder"
dist_kw = { body_split = 5, body_split_from = 0.5 }
'''

PLAN = [
    ('wdt_core.py', [
        (re.compile(re.escape("    q['rate_scenario'] = name\n    return q\n")), lambda m: m.group(0) + CORE_FUNCS, 1),
        (re.compile(re.escape("    p['rates'] = _parse_rates(raw.get('rates'))\n\n    return p\n")),
         lambda m: "    p['rates'] = _parse_rates(raw.get('rates'))\n    p['rules'] = _parse_rules(raw.get('rules'))\n\n    return p\n", 1),
        (re.compile(re.escape("    return {'rates': _parse_rates(raw.get('rates')), 'meta': raw.get('meta', {})}")),
         lambda m: "    return {'rates': _parse_rates(raw.get('rates')), 'rules': _parse_rules(raw.get('rules')), 'meta': raw.get('meta', {})}", 1),
        (re.compile(re.escape("'rate_scenario': str(vg.get('rate_scenario', '')),")),
         lambda m: (m.group(0) + "\n        'g_real': (float(vg['g_real']) if 'g_real' in vg else None),"
                    "\n        'index_rate': (float(vg['index_rate']) if 'index_rate' in vg else None),"), 1),
    ]),
    ('valgen_core.py', [
        (re.compile(re.escape(', rate_params, with_rate_scenario')), lambda m: m.group(0) + ', with_val_basis', 1),
        (re.compile(re.escape('def _plan_fixture_applies(')), lambda m: VALGEN_IR + m.group(0), 1),
        (re.compile(re.escape("p = with_rate_scenario(load_params())")),
         lambda m: "p = with_val_basis(with_rate_scenario(load_params()))", 1),
        (re.compile(re.escape("p['budget_growth']")), lambda m: '_ir(p)', 6),
        (re.compile(re.escape("'rate_scenario': p.get('rate_scenario'),")),
         lambda m: m.group(0) + " 'val_basis': p.get('val_basis', 'legacy_nominal'),", 1),
    ]),
    ('rates_core.py', [
        (re.compile(re.escape("def run_lines(g, idx, V0, w, group, nb, ph, G, c, rp, heir_rule='delta'):")),
         lambda m: "def run_lines(g, idx, V0, w, group, nb, ph, G, c, rp, heir_rule='delta', c_cap='units'):", 1),
        (re.compile(re.escape("    heir_rule 'delta' (baseline) | 'fresh' (ablation: no tax on the receipt, basis = value)\n")),
         lambda m: (m.group(0) + "    c_cap     'units' (refund capped by units paid) | 'units_and_value' (also by the true value paid, net of refunds,\n"
                    "              reset at a death: valgen's EC cap; see wdt_core.parse_rule)\n"), 1),
        (re.compile(re.escape("    Wp = V.copy()\n    tax = np.zeros(T)\n")),
         lambda m: "    Wp = V.copy()\n    EC = np.zeros(n)                      # true value paid net of refunds (units_and_value cap)\n    tax = np.zeros(T)\n", 1),
        (re.compile(re.escape("            q[neg] = np.maximum(-rate[neg] * (1.0 - Wn[neg] / Wp[neg]), -u[neg] / f[neg])\n")),
         lambda m: (m.group(0) + "            if c_cap == 'units_and_value':\n"
                    "                q[neg] = np.maximum(q[neg], -np.maximum(EC[neg], 0.0) / (V[neg] * f[neg]))\n"), 1),
        (re.compile(re.escape("        u = u + units\n        Wp = Wn\n")),
         lambda m: "        u = u + units\n        EC = EC + paid\n        Wp = Wn\n", 1),
        (re.compile(re.escape("                u[d] = 0.0\n                Wp[d] = f[d] * V[d]")),
         lambda m: "                u[d] = 0.0\n                EC[d] = 0.0\n                Wp[d] = f[d] * V[d]", 1),
        (re.compile(re.escape("                u[d] = 0.0\n                Wd = f[d] * V[d]")),
         lambda m: "                u[d] = 0.0\n                EC[d] = 0.0\n                Wd = f[d] * V[d]", 1),
        (re.compile(re.escape("                u[d] = u[d] + ud\n")),
         lambda m: m.group(0) + "                EC[d] = EC[d] + pd_\n", 1),
        (re.compile(re.escape("heir_rule='delta', c_cell=None, cell_diff=None):")),
         lambda m: "heir_rule='delta', c_cell=None, cell_diff=None, c_cap='units'):", 1),
        (re.compile(re.escape("                    heir_rule=heir_rule)\n")),
         lambda m: "                    heir_rule=heir_rule, c_cap=c_cap)\n", 1),
        (re.compile(re.escape("                      cell_diff=cal.get('cell_diff'))")),
         lambda m: "                      cell_diff=cal.get('cell_diff'), c_cap=wc.resolve_rule(p, cfg['rule_set'])['c_cap'])", 1),
    ]),
    ('WDT_Params.toml', [
        (re.compile(re.escape('schedule         = "logistic"   # "logistic" | "logistic_ln" | a name defined in [rates.schedules.*]\n')),
         lambda m: (m.group(0) + 'rule_set         = "candidate"  # "base" | "candidate" | an explicit key c_cap/verify_down/dauc: see [rules]. '
                    'RATES honest lines feel the c_cap part (the value cap)\n'), 1),
        (re.compile(re.escape('rate_scenario = "gain_ladder"\n')),
         lambda m: (m.group(0) +
                    "# g_real / index_rate : VAL on the REAL basis, as RATES (basis = \"real\"). OMITTED = legacy (nominal hist_mean, budget_growth).\n"
                    "#   g_real     real return of the VAL asset (a fraction). Take it from the JST history RATES uses: python print_val_real_inputs.py\n"
                    "#   index_rate real GDP/head growth, the W_min / k index (RATES index mode gdp_pc on a real basis)\n"
                    "# g_real     = 0.0\n# index_rate = 0.0\n"), 1),
        (re.compile(re.escape('  "gl_levy_stat_f010", "gl_levy_stat_f015", "gl_levy_stat_f020",\n]')),
         lambda m: ('  "gl_levy_stat_f010", "gl_levy_stat_f015", "gl_levy_stat_f020",\n'
                    '  # rule-set ablation: the headline ladder under the BASE rule set (units cap only)\n'
                    '  "gain_ladder_rule_base",\n]'), 1),
        (re.compile(r'\Z'), lambda m: TOML_RULES, 1),
    ]),
]


def find(name, base):
    for cand in (base / name, base.parent / name):
        if cand.exists():
            return cand
    hits = sorted(base.rglob(name)) or sorted(base.parent.rglob(name))
    return hits[0] if hits else None


def apply(text, edits, label):
    errors = []
    for i, (pat, rep, want) in enumerate(edits, 1):
        n = len(pat.findall(text))
        if n != want:
            errors.append(f'{label} edit {i}: matched {n} times, expected {want}: {pat.pattern[:70]!r}')
            continue
        if want > 1:                       # show every site of a multi-match edit so it can be eyeballed in the dry run
            for line in text.splitlines():
                if pat.search(line):
                    print(f'    [{label} edit {i}] {line.strip()[:110]}')
        text = pat.sub(rep, text)
    return text, errors


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dir', default='.')
    ap.add_argument('--write', action='store_true')
    a = ap.parse_args()
    base = Path(a.dir).resolve()
    results, errors = {}, []
    for name, edits in PLAN:
        path = find(name, base)
        if path is None:
            errors.append(f'{name}: not found under {base} or its parent')
            continue
        text, errs = apply(path.read_text(encoding='utf-8'), edits, name)
        errors += errs
        if not errs:
            try:
                if name.endswith('.py'):
                    compile(text, name, 'exec')
                else:
                    tomllib.loads(text)
            except (SyntaxError, tomllib.TOMLDecodeError) as exc:
                errors.append(f'{name}: patched text does not parse: {exc}')
        results[name] = (path, text, len(edits))
    if errors:
        print('NOTHING WRITTEN. Problems:')
        for e in errors:
            print('  -', e)
        sys.exit(1)
    for name, (path, text, n) in results.items():
        print(f'{"WRITE" if a.write else "ok   "} {path}  ({n} edits)')
        if a.write:
            path.with_suffix(path.suffix + '.bak2').write_text(path.read_text(encoding='utf-8'), encoding='utf-8')
            path.write_text(text, encoding='utf-8')
    print('\nNow: python test_rules_and_basis.py, python print_val_real_inputs.py, then rates_core.py and valgen_core.py.'
          if a.write else '\nDry run only. Re-run with --write to apply.')


if __name__ == '__main__':
    main()
