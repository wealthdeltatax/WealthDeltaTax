#!/usr/bin/env python3
"""
apply_plan_s1_fixtures.py -- one step: replace the PLAN_S1 fixtures in valgen_core.py with the values derived on the
post-settlement basis (check_params_and_plan_s1.py, 11 Oct 2026) and remove the post-basis gate in _plan_fixture_applies.

Usage:  python apply_plan_s1_fixtures.py MODEL_DIR [--check]        Backup: valgen_core.py.pre_s1.bak
Needs apply_basis_change.py in the same folder. Exact-match edits; re-run safe.

What the fixtures are: a regression guard. The gains were derived by this code, so they freeze its behaviour; they are not an
outside check. The flat-rate stake IS independently checked: (1 - tau g / (1 + g))^30 = 0.651285 at tau = 15%, g = 10.45%.
The calibration gate (baseline tau_0, tau_m, k, W_min, V0_m, g and the logistic schedule) is kept.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from apply_basis_change import patch_text, locate

PATCHES = [
    ("PLAN_S1_GAIN: post-basis values",
     "PLAN_S1_GAIN = {(30, 0.1): 0.025, (30, 0.5): 0.014,\n"
     "                (90, 0.1): 1.09,  (90, 0.5): 0.25, (90, 2.0): -0.20, (90, 5.0): -0.40}\n",
     "PLAN_S1_GAIN = {(30, 0.1): 0.031, (30, 0.5): 0.017,           # derived on the POST-settlement basis (11 Oct 2026):\n"
     "                (90, 0.1): 2.818, (90, 0.5): 0.546, (90, 2.0): -0.356, (90, 5.0): -0.64}   # a regression guard, not an outside check\n"),
    ("PLAN_S1_FLAT_STAKE: post-basis value",
     "PLAN_S1_FLAT_N, PLAN_S1_FLAT_STAKE = 30, 0.685117\n",
     "PLAN_S1_FLAT_N, PLAN_S1_FLAT_STAKE = 30, 0.651285   # post basis; hand value (1 - tau g/(1+g))^30\n"),
    ("remove the post-basis gate",
     "    if BASIS_CONVENTION == 'post':\n"
     "        return False                      # plan fixtures are on the pre-settlement basis (BASIS_CHANGE); re-derive before use\n",
     ""),
]


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
    bak = path.with_name(path.name + '.pre_s1.bak')
    if not bak.exists():
        bak.write_bytes(path.read_bytes())
    compile(new_text, str(path), 'exec')
    path.write_bytes((new_text.replace('\n', '\r\n') if crlf else new_text).encode('utf-8'))
    print(f'  wrote {path} (backup {bak.name}); syntax OK')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
