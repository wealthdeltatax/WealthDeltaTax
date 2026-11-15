#!/usr/bin/env python3
"""
apply_phase2_params.py -- Phase 1/2 parameter layer (WDT_Refactor_Plan.md items 3, 4, 6).

  1. appends the [route_b], [income], [verification] and [archetypes.*] sections to WDT_Params.toml
     (each top-level header is checked first; if any is already present nothing is appended)
  2. adds _parse_phase2() to wdt_core.py and calls it from load_params() and load_rates_params(),
     which then return p['route_b'], p['income'], p['verification'], p['archetypes'].

Defaults reproduce the old behaviour: payment_mode='sale', lambda=0, death_verifies=false.

Usage:  python apply_phase2_params.py MODEL_DIR [--check]
Needs apply_basis_change.py in the same folder (reuses its patch helpers). Backups: <file>.pre_p2.bak
"""
import sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from apply_basis_change import patch_text, locate

TOML_ADD = r"""

# ═════════════════════════════════════════════════════════════════════════════
# Phase 1 item 3 additions (WDT_Refactor_Plan.md). All values are PLACEHOLDERS to research (plan section 8, risk 7).
# payment_mode = "sale" keeps the old behaviour everywhere; set "lien" or "income" to run the D4b scenarios.
# ═════════════════════════════════════════════════════════════════════════════

[route_b]
payment_mode        = "sale"      # sale (old: cash-equivalent units) | lien (deferred balance, settled at death) | income (paid from external income)
sovereign_real_rate = 0.015       # lien accrues at sovereign real rate + deferral_spread (D4c)
deferral_spread     = 0.01        # the breakeven spread is solved in valgen_core (plan section 6)
# RATES: Route B share of a line's holdings by launch wealth (£m); linear in ln W between points, flat beyond. From the section 4 archetypes.
share_by_wealth     = [[0.4, 0.65], [8.0, 0.10], [30.0, 0.10], [50.0, 0.25], [500.0, 0.05]]

[income]
cap             = 1.0             # share of external income that can go to WDT (sweep 0.5, 0.75, 1.0)
cap_sweep       = [0.5, 0.75, 1.0]
default_ratio   = 0.0             # external income / wealth when no archetype is named
# RATES: external income / wealth by launch wealth (£m), same interpolation as share_by_wealth (section 4.1)
ratio_by_wealth = [[0.4, 0.08], [8.0, 0.02], [30.0, 0.05], [50.0, 0.005], [500.0, 0.01]]

[income.by_archetype]
housing_pension   = 0.08
startup_founder   = 0.02
generational      = 0.005
ceo_fintech       = 0.05
resource_monopoly = 0.01

[verification]
lambda_C       = 0.0              # per-year verification hazard, Route C (D6)
lambda_D       = 0.0              # per-year corrective-auction hazard, Route D
death_verifies = false            # true: death verifies Route C with certainty (D6); Route D is always auctioned at death
lambda_sweep   = [0.0, 0.02, 0.05, 0.10]

[archetypes.housing_pension]
label = "Housing and pension"
V0_m  = 0.4
A = 0.30
B = 0.65
C = 0.02
D = 0.03

[archetypes.startup_founder]
label = "Start-up founder"
V0_m  = 8.0
A = 0.10
B = 0.10
C = 0.70
D = 0.10

[archetypes.generational]
label = "Generational wealth"
V0_m  = 50.0
A = 0.50
B = 0.25
C = 0.08
D = 0.17

[archetypes.ceo_fintech]
label = "CEO / fintech"
V0_m  = 30.0
A = 0.40
B = 0.10
C = 0.40
D = 0.10

[archetypes.resource_monopoly]
label = "Resource monopoly"
V0_m  = 500.0
A = 0.10
B = 0.05
C = 0.20
D = 0.65

"""

PARSER = """def _parse_phase2(raw):
    \"\"\"[route_b], [income], [verification], [archetypes.*] -> validated dicts (Phase 2 additions).\"\"\"
    rb = dict(raw.get('route_b', {}))
    mode = str(rb.get('payment_mode', 'sale'))
    if mode not in ('sale', 'lien', 'income'):
        raise ValueError(f"[route_b] payment_mode must be sale|lien|income, got {mode!r}")
    sw = [(float(w), float(s)) for w, s in rb.get('share_by_wealth', [])]
    for w, s in sw:
        if not (w > 0 and 0.0 <= s <= 1.0):
            raise ValueError(f"[route_b] share_by_wealth point ({w}, {s}) out of range")
    route_b = {'payment_mode': mode,
               'sovereign_real_rate': float(rb.get('sovereign_real_rate', 0.015)),
               'deferral_spread': float(rb.get('deferral_spread', 0.01)),
               'share_by_wealth': sorted(sw)}
    route_b['r_def'] = route_b['sovereign_real_rate'] + route_b['deferral_spread']
    inc = dict(raw.get('income', {}))
    cap = float(inc.get('cap', 1.0))
    if not 0.0 <= cap <= 1.0:
        raise ValueError(f"[income] cap must be in [0,1], got {cap}")
    rw = [(float(w), float(s)) for w, s in inc.get('ratio_by_wealth', [])]
    for w, s in rw:
        if not (w > 0 and s >= 0.0):
            raise ValueError(f"[income] ratio_by_wealth point ({w}, {s}) out of range")
    income = {'cap': cap, 'cap_sweep': [float(x) for x in inc.get('cap_sweep', [cap])],
              'default_ratio': float(inc.get('default_ratio', 0.0)),
              'ratio_by_wealth': sorted(rw),
              'by_archetype': {k: float(v) for k, v in dict(inc.get('by_archetype', {})).items()}}
    ver = dict(raw.get('verification', {}))
    verification = {'lambda_C': float(ver.get('lambda_C', 0.0)), 'lambda_D': float(ver.get('lambda_D', 0.0)),
                    'death_verifies': bool(ver.get('death_verifies', False)),
                    'lambda_sweep': [float(x) for x in ver.get('lambda_sweep', [0.0])]}
    for k in ('lambda_C', 'lambda_D'):
        if not 0.0 <= verification[k] <= 1.0:
            raise ValueError(f"[verification] {k} must be in [0,1]")
    arch = {}
    for name, a in dict(raw.get('archetypes', {})).items():
        sh = {r: float(a[r]) for r in 'ABCD'}
        if any(v < 0.0 for v in sh.values()) or abs(sum(sh.values()) - 1.0) > 1e-9:
            raise ValueError(f"[archetypes.{name}] shares must be >= 0 and sum to 1, got {sh}")
        arch[name] = {'label': str(a.get('label', name)), 'V0_m': float(a['V0_m']), 'shares': sh}
    return {'route_b': route_b, 'income': income, 'verification': verification, 'archetypes': arch}


"""

WDT_CORE = [
    ("add _parse_phase2 before load_rates_params",
     "def load_rates_params(toml_path=None):\n",
     PARSER + "def load_rates_params(toml_path=None):\n"),
    ("load_rates_params returns the phase-2 blocks",
     "    return {'rates': _parse_rates(raw.get('rates')), 'rules': _parse_rules(raw.get('rules')), 'meta': raw.get('meta', {})}\n",
     "    out = {'rates': _parse_rates(raw.get('rates')), 'rules': _parse_rules(raw.get('rules')), 'meta': raw.get('meta', {})}\n"
     "    out.update(_parse_phase2(raw))\n"
     "    return out\n"),
    ("load_params returns the phase-2 blocks",
     "    p['rules'] = _parse_rules(raw.get('rules'))\n\n    return p\n",
     "    p['rules'] = _parse_rules(raw.get('rules'))\n    p.update(_parse_phase2(raw))\n\n    return p\n"),
]


def append_toml(path, check_only):
    raw = path.read_bytes().decode('utf-8')
    crlf = '\r\n' in raw
    text = raw.replace('\r\n', '\n')
    heads = ['[route_b]', '[income]', '[verification]', '[archetypes.']
    present = [h for h in heads if re.search(r'^\s*' + re.escape(h), text, re.M)]
    if present:
        print(f"{path}: sections already present {present}; nothing appended")
        return
    print(f"{path}: will append sections {heads}")
    if check_only:
        return
    bak = path.with_name(path.name + '.pre_p2.bak')
    if not bak.exists():
        bak.write_bytes(path.read_bytes())
    out = text.rstrip('\n') + '\n' + TOML_ADD
    import tomllib
    tomllib.loads(out)                                   # parse check before writing
    out = out.replace('\n', '\r\n') if crlf else out
    path.write_bytes(out.encode('utf-8'))
    print(f"  appended (backup {bak.name}); TOML parses")


def main(argv):
    if len(argv) < 2 or argv[1].startswith('--'):
        print(__doc__); return 2
    root = Path(argv[1]); check_only = '--check' in argv
    tomls = [p for p in root.rglob('WDT_Params.toml') if 'OUTPUTS' not in p.parts]
    if len(tomls) != 1:
        print(f"ABORT WDT_Params.toml found {len(tomls)} times under {root}"); return 1
    path = locate(root, 'wdt_core.py')
    raw = path.read_bytes().decode('utf-8'); crlf = '\r\n' in raw
    text = raw.replace('\r\n', '\n')
    try:
        new_text, log = patch_text(text, WDT_CORE, 'wdt_core.py')
    except RuntimeError as e:
        print(f"ABORT {e}"); return 1
    print(f"{path}: " + ('changes pending' if new_text != text else 'no changes')); print('\n'.join(log))
    append_toml(tomls[0], check_only)
    if not check_only and new_text != text:
        bak = path.with_name(path.name + '.pre_p2.bak')
        if not bak.exists():
            bak.write_bytes(path.read_bytes())
        compile(new_text, str(path), 'exec')
        path.write_bytes((new_text.replace('\n', '\r\n') if crlf else new_text).encode('utf-8'))
        print(f"  wrote {path}; syntax OK")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
