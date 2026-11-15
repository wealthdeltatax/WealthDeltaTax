"""
patch_NNN_slug.py -- ONE LINE: what this changes and why.

Files edited : wdt_core.py, WDT_Params.toml            (names only; wdt_patchlib finds them under the model root)
Changes numbers?  no | YES: <which outputs move, and what to re-run: core -> tables/charts>
Plan / decision   : <D-number or plan item, if any>

Run from Model/test:
    python patch_NNN_slug.py            dry run: shows what would change, writes nothing
    python patch_NNN_slug.py --apply    writes the changes (originals go to test/_backups/patch_NNN_slug/)
Test:
    python test_patch_NNN_slug.py       checks the patch on a COPY of the code (never touches the real files)
    python test_patch_NNN_slug.py --live   after --apply: checks the real tree
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wdt_patchlib import Delete, InsertAfter, InsertBefore, Replace, patch_cli   # noqa: E402,F401

NAME = Path(__file__).stem

# Anchors are copied VERBATIM from the file (Grep -n with a little context, then Read just that range).
# Each must match exactly once: add a neighbouring line until it does. Use '\n' in the strings whatever the file uses;
# the library converts to the file's own line endings. `done` is text that exists ONLY after the edit; it is what
# makes a re-run a no-op (default: `new`). Give it explicitly when `new` is generic or when the anchor survives the edit.
SPEC = {
    'wdt_core.py': [
        Replace(
            old="    return out\n\n\ndef rate_params(p):",
            new="    return out\n\n\ndef _example_helper(p):\n    \"\"\"What it does, one line.\"\"\"\n    return p\n\n\ndef rate_params(p):",
            label='add _example_helper before rate_params',
            done='def _example_helper(p):',
        ),
    ],
    # 'WDT_Params.toml': [
    #     InsertAfter(anchor='[val_gen]\n', new='new_key = 1.0   # units and meaning\n', label='new_key', done='new_key = 1.0'),
    # ],
}

if __name__ == '__main__':
    sys.exit(patch_cli(SPEC, NAME, __doc__))
