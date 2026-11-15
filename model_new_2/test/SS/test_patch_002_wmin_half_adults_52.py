"""
test_patch_002_wmin_half_adults_52.py -- test for patch_002_wmin_half_adults_52.py

    python test_patch_002_wmin_half_adults_52.py          the patch, on a COPY of the model in a temp folder. Safe at any time.
    python test_patch_002_wmin_half_adults_52.py --live   the REAL tree, after the patch has been applied.

Checks 1-7 are the generic ones (apply once, no-op the second time, TOML parses, CRLF kept, untouched files identical).
Check 8 is specific: defaults and every explicit scenario carry wmin_house_ratio 0.5, the 0.0 scenarios still 0.0, nothing 1.0 is left,
adults_m is 52.0, nothing else in the TOML changed value (ladders, taus, levy), and the two labels say 'half'.
"""

import importlib.util
import shutil
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import wdt_patchlib as wl                                    # noqa: E402

PATCH_FILE = HERE / 'patch_002_wmin_half_adults_52.py'
REGRESSION: list = []                                        # no existing test is tied to W_min; re-run the cores by hand (see the patch docstring)
LIVE = '--live' in sys.argv

spec_ = importlib.util.spec_from_file_location('the_patch', PATCH_FILE)
the_patch = importlib.util.module_from_spec(spec_)
spec_.loader.exec_module(the_patch)
SPEC, NAME = the_patch.SPEC, the_patch.NAME

T = wl.Checks(f'{NAME}: {"LIVE tree" if LIVE else "sandbox copy"}')


def read(p):
    return Path(p).read_bytes()


def load(base):
    return tomllib.loads(wl._read(wl.find_file('WDT_Params.toml', base)))


def strip_target(d):
    """The TOML with the values this patch changes removed, so everything else can be compared."""
    import copy
    d = copy.deepcopy(d)
    d['rates']['scenarios'].pop(the_patch.SENS, None)
    d['rates']['run'].pop('scenarios', None)
    d['rates']['defaults'].pop('wmin_house_ratio', None)
    d['rates']['replacement'].pop('adults_m', None)
    for name, sc in d['rates']['scenarios'].items():
        if name == the_patch.SENS:
            continue
        if sc.get('wmin_house_ratio') in (1.0, 0.5):
            sc.pop('wmin_house_ratio')
        if name in ('wmin_house', 'wmin_house_hp'):
            sc.pop('label', None)
    return d


def main():
    root = wl.model_root()
    names = list(SPEC)
    if LIVE:
        rep = wl.run_patch(SPEC, NAME, root=root, apply=False, quiet=True)
        T.check('live: every op already applied', all(r['applied'] == 0 and not r['changed'] for r in rep.values()),
                str({f: (r['applied'], r['skipped']) for f, r in rep.items()}))
        for f in names:
            wl.validate_text(f, wl.find_file(f, root).read_text(encoding='utf-8'))
        T.check('live: files parse', True)
        section8(root, None)
        return T.finish()

    sb = wl.make_sandbox(root)
    try:
        before = {f: read(wl.find_file(f, sb)) for f in names}
        orig = load(sb)

        wl.run_patch(SPEC, NAME, root=sb, apply=False, quiet=True)
        T.check('1 dry run writes nothing', all(read(wl.find_file(f, sb)) == before[f] for f in names))

        rep = wl.run_patch(SPEC, NAME, root=sb, apply=True, quiet=True)
        T.check('2 apply changes each file', all(r['changed'] and r['applied'] > 0 for r in rep.values()),
                str({f: (r['applied'], r['skipped']) for f, r in rep.items()}))
        after = {f: read(wl.find_file(f, sb)) for f in names}

        rep2 = wl.run_patch(SPEC, NAME, root=sb, apply=True, quiet=True)
        T.check('3 second run is a no-op', all(r['applied'] == 0 and not r['changed'] for r in rep2.values())
                and all(read(wl.find_file(f, sb)) == after[f] for f in names))

        ok = True
        for f in names:
            try:
                wl.validate_text(f, after[f].decode('utf-8'))
            except wl.PatchError:
                ok = False
        T.check('4 patched files parse', ok)

        def eol_ok(b0, b1):
            crlf0, lf0 = b0.count(b'\r\n'), b0.count(b'\n') - b0.count(b'\r\n')
            crlf1, lf1 = b1.count(b'\r\n'), b1.count(b'\n') - b1.count(b'\r\n')
            return (lf1 == 0) if (crlf0 and not lf0) else (crlf1 == 0)
        T.check('5 line endings preserved', all(eol_ok(before[f], after[f]) for f in names))

        same = all(read(p) == read(sb / p.relative_to(root)) for p in wl._walk(root)
                   if p.suffix in wl.CODE_SUFFIXES and p.name not in names and (sb / p.relative_to(root)).exists())
        T.check('6 files it does not name are untouched', same)
        T.check('7 (no regression tests tied to this patch)', True)

        section8(sb, orig)
    finally:
        shutil.rmtree(sb, ignore_errors=True)
    return T.finish()


def section8(base, orig):
    d = load(base)
    r = d['rates']
    T.check('8a [rates.defaults] wmin_house_ratio == 0.5', r['defaults']['wmin_house_ratio'] == 0.5)
    T.check('8b adults_m == 52.0', r['replacement']['adults_m'] == 52.0)
    sc = r['scenarios']
    ones = [n for n, s in sc.items() if s.get('wmin_house_ratio') == 1.0 and n != the_patch.SENS]
    T.check('8c no scenario still has wmin_house_ratio 1.0', not ones, str(ones))
    halves = [n for n, s in sc.items() if s.get('wmin_house_ratio') == 0.5]
    T.check('8d all explicit scenarios in the patch list carry 0.5', len(halves) >= len(the_patch.SCENARIOS), f'{len(halves)} found')
    zeros = [n for n, s in sc.items() if s.get('wmin_house_ratio') == 0.0]
    T.check('8e the 0.0 scenarios (logistic_ref, wmin_all, tau0_*, taum_*, k_*, wmin_*) are untouched', {'logistic_ref', 'wmin_all'} <= set(zeros) and (orig is None or zeros == [n for n, s in orig['rates']['scenarios'].items() if s.get('wmin_house_ratio') == 0.0]), str(zeros))
    T.check('8f labels say half the median', all('half the median house price' in sc[n]['label'] for n in ('wmin_house', 'wmin_house_hp')))
    sch = r['schedules']
    T.check('8j sensitivity scenario exists at ratio 1.0 and is in the run list',
            sc[the_patch.SENS]['wmin_house_ratio'] == 1.0 and the_patch.SENS in r['run']['scenarios'])
    T.check('8g ladder anchors unchanged here (the first anchor follows W_min in rates_core, see the second patch)',
            orig is None or sch['gain_ladder']['anchors'] == orig['rates']['schedules']['gain_ladder']['anchors']
            and sch['stock_ladder']['anchors'] == orig['rates']['schedules']['stock_ladder']['anchors'])
    if orig is not None:
        T.check('8h every other value in the TOML is identical', strip_target(orig) == strip_target(d))
        T.check('8i scenario set unchanged', set(orig['rates']['scenarios']) | {the_patch.SENS} == set(sc))
    else:
        T.check('8h (live) scenario count', len(sc) >= len(the_patch.SCENARIOS))


if __name__ == '__main__':
    sys.exit(main())