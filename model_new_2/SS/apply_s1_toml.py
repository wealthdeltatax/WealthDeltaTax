"""
apply_s1_toml.py -- S1 follow-up: retire reset_interval / death_waiver from the TOML and wdt_core.load_params, pass b_shift.

Run from the Model/ folder:   python apply_s1_toml.py [--dry-run]

Edits (each is exact-match, idempotent; a file is backed up to <name>.bak_s1 before its first write):
  WDT_Params.toml
    [val_gen]  remove the live keys reset_interval and death_waiver; re-comment reset_sens as the menu of voluntary reset
               CYCLES (a strategy action, D6); add b_shift (Route B share a route-shift strategy moves).
    [val_gen]  replace the header comment lines that still describe the scheduled reset and the death waiver.
    [verification]  comment: lambda_D = 0 means "couple to lambda_C" in valgen.
  wdt_core.py
    load_params  stop hard-reading reset_interval / death_waiver (a KeyError once the TOML keys are gone); pass b_shift.
Not added: reset_cycles. valgen_core reads reset_sens and falls back to a code default, so a TOML key would be dead.
"""
import shutil
import sys
from pathlib import Path

DRY = '--dry-run' in sys.argv
HERE = Path(__file__).resolve().parent

TOML_EDITS = [
    ("""reset_interval   = 10
reset_sens       = [0, 5, 10, 20]
death_waiver     = 0
""",
     """# reset_sens : voluntary Route D reset CYCLES (years) a family may choose as a STRATEGY action (D6); 0 = never.
#              Read by valgen_core._reset_cycles. It is a menu, not a rule-set clock: reset_interval and death_waiver are retired.
reset_sens       = [0, 5, 10, 20]
# b_shift : shares of Route B that a route-shift strategy moves into D or C and then understates (valgen_core._strategies).
b_shift          = [0.5, 1.0]
"""),
    ("""# reset_interval: Route D voluntary hard reset every N years (D3); 0 = never.
# death_waiver  : death auction skipped if a reset fell within this many years
#                 (CLOSE 4.1.1); 0 = never waived.
#                 (A Route D write-down at a reset always refunds: cancels accrued
#                 liability, then units, pooled cap. Decision of 2 Oct: symmetric.)
""",
     """# RETIRED (WDT_Refactor_Plan D6): reset_interval (scheduled Route D reset) and death_waiver. A reset is an action the family
#                 chooses (see reset_sens below); death always holds the Route D auction. run_family3 raises TypeError on both.
#                 (A Route D write-down at a reset always refunds: cancels accrued liability, then units, pooled cap. Symmetric.)
"""),
    ("""lambda_C       = 0.0              # per-year verification hazard, Route C (D6)
lambda_D       = 0.0              # per-year corrective-auction hazard, Route D
""",
     """lambda_C       = 0.0              # per-year verification hazard, Route C (D6)
lambda_D       = 0.0              # per-year corrective-auction hazard, Route D. In VAL, 0 = couple to lambda_C (valgen _lam_D); > 0 = used as given
"""),
]

CORE_EDITS = [
    ("""        'reset_interval': _I('reset_interval'), 'reset_sens': _IL('reset_sens'),
        'death_waiver': _I('death_waiver'),
""",
     """        'reset_sens': _IL('reset_sens'),   # voluntary Route D reset cycles a family may choose (D6); reset_interval and death_waiver are retired
        'b_shift': (_FL('b_shift') if 'b_shift' in vg else None),   # None = valgen_core default
"""),
]


def patch(path, edits):
    if not path.exists():
        print(f'  SKIP  {path.name}: not found in {HERE}')
        return False
    text = path.read_text(encoding='utf-8')
    new, todo = text, 0
    for old, rep in edits:
        n = new.count(old)
        if n == 1:
            new, todo = new.replace(old, rep), todo + 1
        elif n == 0 and rep in new:
            print(f'  ok    {path.name}: already applied ({old.splitlines()[0][:50]!r})')
        else:
            raise SystemExit(f'{path.name}: expected exactly one match, found {n} for {old.splitlines()[0][:60]!r}')
    if todo and not DRY:
        shutil.copy2(path, path.with_name(path.name + '.bak_s1'))
        path.write_text(new, encoding='utf-8')
    print(f'  {"would apply" if DRY else "applied"} {todo} edit(s) to {path.name}')
    return True


def leftover_readers():
    """Warn about any other file that still reads the retired keys."""
    import re
    pat = re.compile(r"reset_interval|death_waiver")
    for f in sorted(HERE.rglob('*.py')):
        if f.name in ('apply_s1_toml.py',):
            continue
        for i, line in enumerate(f.read_text(encoding='utf-8', errors='ignore').splitlines(), 1):
            if pat.search(line.split('#', 1)[0]):
                print(f'  LIVE? {f.relative_to(HERE)}:{i}: {line.strip()[:100]}')


if __name__ == '__main__':
    patch(HERE / 'WDT_Params.toml', TOML_EDITS)
    patch(HERE / 'wdt_core.py', CORE_EDITS)
    print('Remaining mentions of the retired keys in .py files (comments excluded):')
    leftover_readers()
