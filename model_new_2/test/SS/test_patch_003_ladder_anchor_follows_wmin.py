"""
test_patch_003_ladder_anchor_follows_wmin.py

    python test_patch_NNN_ladder_anchor_follows_wmin.py          sandbox copy, safe at any time
    python test_patch_NNN_ladder_anchor_follows_wmin.py --live   the real tree, after --apply

Generic checks 1-6, then 8: the helper (extracted from the patched rates_core.py and run on its own, so no JST or wdt_core is needed)
moves the first anchor to W_min only when 0 < W_min < second anchor; calibration() calls it before ladder_to_tau.
Not covered here (needs the JST): run rates_core and compare schedule_diag in the JSON, see the patch docstring.
"""

import importlib.util
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import wdt_patchlib as wl                                    # noqa: E402

PATCH_FILE = HERE / 'patch_003_ladder_anchor_follows_wmin.py'
LIVE = '--live' in sys.argv
spec_ = importlib.util.spec_from_file_location('the_patch', PATCH_FILE)
the_patch = importlib.util.module_from_spec(spec_)
spec_.loader.exec_module(the_patch)
SPEC, NAME = the_patch.SPEC, the_patch.NAME
T = wl.Checks(f'{NAME}: {"LIVE tree" if LIVE else "sandbox copy"}')
read = lambda p: Path(p).read_bytes()            # noqa: E731


def helper_from(text):
    m = re.search(r'def _anchors_at_wmin\(anchors, wmin\):.*?\n(?=\S)', text, re.S)
    ns = {}
    exec(m.group(0), ns)
    return ns['_anchors_at_wmin']


def section8(base):
    text = wl.find_file('rates_core.py', base).read_text(encoding='utf-8').replace('\r\n', '\n')
    f = helper_from(text)
    g = [[0.225, 0.03], [0.5, 0.10], [1.0, 0.15]]
    T.check('8a W_min 0.1125 -> first anchor at 0.1125, rate kept, rest unchanged', f(g, 0.1125) == [[0.1125, 0.03], [0.5, 0.10], [1.0, 0.15]])
    T.check('8b W_min 0 -> anchors as written', f(g, 0.0) == g)
    T.check('8c W_min at/above second anchor -> as written', f(g, 0.5) == g and f(g, 2.0) == g)
    T.check('8d W_min = 0.225 (old default) -> same anchors as before', f(g, 0.225) == g)
    T.check('8e input not mutated', g == [[0.225, 0.03], [0.5, 0.10], [1.0, 0.15]])
    T.check('8f calibration passes the helper result to ladder_to_tau and records it',
            "anchors = _anchors_at_wmin(sp['anchors'], wmin_gbp_m)" in text and "wc.ladder_to_tau(anchors," in text and "'anchors_target': anchors" in text)
    T.check('8g W_min is computed before the ladder is built',
            text.index("wmin_gbp_m = cfg['wmin_house_ratio'] *") < text.index("anchors = _anchors_at_wmin"))
    T.check('8h anchor_from path still reads the TOML ladder (top point)', "lad, _ = wc.ladder_to_tau(sp['anchors']," in text)


def main():
    root = wl.model_root()
    names = list(SPEC)
    if LIVE:
        rep = wl.run_patch(SPEC, NAME, root=root, apply=False, quiet=True)
        T.check('live: every op already applied', all(r['applied'] == 0 and not r['changed'] for r in rep.values()), str(rep))
        for f in names:
            wl.validate_text(f, wl.find_file(f, root).read_text(encoding='utf-8'))
        T.check('live: files compile', True)
        section8(root)
        return T.finish()
    sb = wl.make_sandbox(root)
    try:
        before = {f: read(wl.find_file(f, sb)) for f in names}
        wl.run_patch(SPEC, NAME, root=sb, apply=False, quiet=True)
        T.check('1 dry run writes nothing', all(read(wl.find_file(f, sb)) == before[f] for f in names))
        rep = wl.run_patch(SPEC, NAME, root=sb, apply=True, quiet=True)
        T.check('2 apply changes each file', all(r['changed'] and r['applied'] == 2 for r in rep.values()), str(rep))
        after = {f: read(wl.find_file(f, sb)) for f in names}
        rep2 = wl.run_patch(SPEC, NAME, root=sb, apply=True, quiet=True)
        T.check('3 second run is a no-op', all(r['applied'] == 0 and not r['changed'] for r in rep2.values()) and all(read(wl.find_file(f, sb)) == after[f] for f in names))
        ok = True
        for f in names:
            try:
                wl.validate_text(f, after[f].decode('utf-8'))
            except wl.PatchError:
                ok = False
        T.check('4 compiles', ok)
        T.check('5 line endings preserved', all((after[f].count(b'\n') == after[f].count(b'\r\n')) == (before[f].count(b'\n') == before[f].count(b'\r\n')) for f in names))
        same = all(read(p) == read(sb / p.relative_to(root)) for p in wl._walk(root)
                   if p.suffix in wl.CODE_SUFFIXES and p.name not in names and (sb / p.relative_to(root)).exists())
        T.check('6 files it does not name are untouched', same)
        section8(sb)
    finally:
        shutil.rmtree(sb, ignore_errors=True)
    return T.finish()


if __name__ == '__main__':
    sys.exit(main())
