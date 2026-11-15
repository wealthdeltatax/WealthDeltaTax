"""
test_patch_003_ct_retire_308.py

    python test_patch_003_ct_retire_308.py          sandbox copy, safe at any time
    python test_patch_003_ct_retire_308.py --live   the real tree, after --apply
"""

import copy
import importlib.util
import shutil
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import wdt_patchlib as wl                                    # noqa: E402

PATCH_FILE = HERE / 'patch_003_ct_retire_308.py'
LIVE = '--live' in sys.argv
spec_ = importlib.util.spec_from_file_location('the_patch', PATCH_FILE)
the_patch = importlib.util.module_from_spec(spec_)
spec_.loader.exec_module(the_patch)
SPEC, NAME = the_patch.SPEC, the_patch.NAME
T = wl.Checks(f'{NAME}: {"LIVE tree" if LIVE else "sandbox copy"}')
read = lambda p: Path(p).read_bytes()            # noqa: E731


def load(base):
    return tomllib.loads(wl._read(wl.find_file('WDT_Params.toml', base)))


def strip(d):
    d = copy.deepcopy(d)
    d['rates']['replacement']['retire'] = [r for r in d['rates']['replacement']['retire'] if r[0] != 'Corporation tax']
    return d


def section8(base, orig):
    d = load(base)
    ret = dict((n, v) for n, v in d['rates']['replacement']['retire'])
    T.check('8a Corporation tax retire share == 0.0308', ret.get('Corporation tax') == 0.0308, str(ret))
    T.check('8b CGT and IHT shares unchanged (0.0050, 0.0030)', ret.get('Capital gains tax') == 0.0050 and ret.get('Inheritance tax') == 0.0030)
    T.check('8c retire order unchanged (corporation tax last)', [n for n, _ in d['rates']['replacement']['retire']] == ['Capital gains tax', 'Inheritance tax', 'Corporation tax'])
    T.check('8d levy_calibration target still names the entry', d['rates']['levy_calibration']['target'] in ret)
    if orig is not None:
        T.check('8e nothing else in the TOML changed', strip(orig) == strip(d))


def main():
    root = wl.model_root()
    names = list(SPEC)
    if LIVE:
        rep = wl.run_patch(SPEC, NAME, root=root, apply=False, quiet=True)
        T.check('live: every op already applied', all(r['applied'] == 0 and not r['changed'] for r in rep.values()), str(rep))
        for f in names:
            wl.validate_text(f, wl.find_file(f, root).read_text(encoding='utf-8'))
        T.check('live: parses', True)
        section8(root, None)
        return T.finish()
    sb = wl.make_sandbox(root)
    try:
        before = {f: read(wl.find_file(f, sb)) for f in names}
        orig = load(sb)
        wl.run_patch(SPEC, NAME, root=sb, apply=False, quiet=True)
        T.check('1 dry run writes nothing', all(read(wl.find_file(f, sb)) == before[f] for f in names))
        rep = wl.run_patch(SPEC, NAME, root=sb, apply=True, quiet=True)
        T.check('2 apply changes each file', all(r['changed'] and r['applied'] > 0 for r in rep.values()), str(rep))
        after = {f: read(wl.find_file(f, sb)) for f in names}
        rep2 = wl.run_patch(SPEC, NAME, root=sb, apply=True, quiet=True)
        T.check('3 second run is a no-op', all(r['applied'] == 0 and not r['changed'] for r in rep2.values()) and all(read(wl.find_file(f, sb)) == after[f] for f in names))
        ok = True
        for f in names:
            try:
                wl.validate_text(f, after[f].decode('utf-8'))
            except wl.PatchError:
                ok = False
        T.check('4 parses', ok)
        T.check('5 line endings preserved', all((after[f].count(b'\n') == after[f].count(b'\r\n')) == (before[f].count(b'\n') == before[f].count(b'\r\n')) for f in names))
        same = all(read(p) == read(sb / p.relative_to(root)) for p in wl._walk(root)
                   if p.suffix in wl.CODE_SUFFIXES and p.name not in names and (sb / p.relative_to(root)).exists())
        T.check('6 files it does not name are untouched', same)
        section8(sb, orig)
    finally:
        shutil.rmtree(sb, ignore_errors=True)
    return T.finish()


if __name__ == '__main__':
    sys.exit(main())
