"""
test_patch_NNN_slug.py -- test for patch_NNN_slug.py (copy this file, rename it to match the patch)

    python test_patch_NNN_slug.py          the patch, on a COPY of the code in a temp folder. Safe at any time.
    python test_patch_NNN_slug.py --live   the REAL tree, after the patch has been applied.

What the generic checks (1-7) prove: the patch applies once, changes the files, is a no-op the second time, leaves valid
Python / TOML, keeps each file's line endings, a dry run writes nothing, and the existing tests do no worse than before.
Section 8 is the part you write: assertions about what THIS patch is meant to do. Prefer behaviour (import the patched
module in a subprocess and call the function) over "the text is there".
"""

import importlib.util
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import wdt_patchlib as wl                                    # noqa: E402

PATCH_FILE = HERE / 'patch_NNN_slug.py'                      # <- rename with the patch
FIXTURE = HERE / 'fixtures' / 'jst_sample.json'              # made by extract_jst_sample.py; optional
REGRESSION = ['kernel_test.py']                              # existing tests that must not get worse (names; found under the model root)
LIVE = '--live' in sys.argv

spec_ = importlib.util.spec_from_file_location('the_patch', PATCH_FILE)
the_patch = importlib.util.module_from_spec(spec_)
spec_.loader.exec_module(the_patch)
SPEC, NAME = the_patch.SPEC, the_patch.NAME

T = wl.Checks(f'{NAME}: {"LIVE tree" if LIVE else "sandbox copy"}')


def read(p):
    return Path(p).read_bytes()


def run_regression(base):
    """{test name: returncode} for each REGRESSION test found under `base` (missing ones are left out)."""
    out = {}
    for t in REGRESSION:
        hits = [p for p in Path(base).rglob(t) if 'test' not in p.relative_to(base).parts[:-1]]
        if len(hits) == 1:
            r = wl.run_py(base, [str(hits[0].relative_to(base))], timeout=600)
            out[t] = r.returncode
    return out


def main():
    root = wl.model_root()
    names = list(SPEC)
    if LIVE:
        # The patch is already applied: a dry run must find every op already done, and the tree must be valid.
        rep = wl.run_patch(SPEC, NAME, root=root, apply=False, quiet=True)
        T.check('live: every op already applied', all(r['applied'] == 0 and not r['changed'] for r in rep.values()),
                str({f: (r['applied'], r['skipped']) for f, r in rep.items()}))
        for f in names:
            p = wl.find_file(f, root)
            wl.validate_text(f, p.read_text(encoding='utf-8'))
        T.check('live: files compile / parse', True)
        sb, base_rc = None, {}
        after = run_regression(root)
        T.check('live: existing tests pass', all(rc == 0 for rc in after.values()), str(after))
        section8(root, live=True)
        return T.finish()

    sb = wl.make_sandbox(root, jst_fixture=FIXTURE if FIXTURE.exists() else None)
    try:
        before = {f: read(wl.find_file(f, sb)) for f in names}
        base_rc = run_regression(sb)                                         # baseline on the untouched copy

        # 1 dry run writes nothing
        wl.run_patch(SPEC, NAME, root=sb, apply=False, quiet=True)
        T.check('1 dry run writes nothing', all(read(wl.find_file(f, sb)) == before[f] for f in names))

        # 2 first apply changes every file it names
        rep = wl.run_patch(SPEC, NAME, root=sb, apply=True, quiet=True)
        T.check('2 apply changes each file', all(r['changed'] and r['applied'] > 0 for r in rep.values()),
                str({f: (r['applied'], r['skipped']) for f, r in rep.items()}))
        after = {f: read(wl.find_file(f, sb)) for f in names}

        # 3 idempotent
        rep2 = wl.run_patch(SPEC, NAME, root=sb, apply=True, quiet=True)
        T.check('3 second run is a no-op', all(r['applied'] == 0 and not r['changed'] for r in rep2.values())
                and all(read(wl.find_file(f, sb)) == after[f] for f in names))

        # 4 valid code
        ok = True
        for f in names:
            try:
                wl.validate_text(f, after[f].decode('utf-8'))
            except wl.PatchError:
                ok = False
        T.check('4 patched files compile / parse', ok)

        # 5 line endings and encoding: a CRLF file stays all-CRLF, an LF file stays all-LF
        def eol_ok(b0, b1):
            crlf0, lf0 = b0.count(b'\r\n'), b0.count(b'\n') - b0.count(b'\r\n')
            crlf1, lf1 = b1.count(b'\r\n'), b1.count(b'\n') - b1.count(b'\r\n')
            return (lf1 == 0) if (crlf0 and not lf0) else (crlf1 == 0)
        T.check('5 line endings preserved', all(eol_ok(before[f], after[f]) for f in names))

        # 6 the patch only touches what it names: other project files are byte-identical to the originals
        same = all(read(p) == read(sb / p.relative_to(root)) for p in wl._walk(root)
                   if p.suffix in wl.CODE_SUFFIXES and p.name not in names and (sb / p.relative_to(root)).exists())
        T.check('6 files it does not name are untouched', same)

        # 7 existing tests: no worse than before the patch
        now = run_regression(sb)
        T.check('7 existing tests no worse', all(now[t] <= base_rc[t] for t in now), f'before {base_rc}, after {now}')

        section8(sb, live=False)
    finally:
        shutil.rmtree(sb, ignore_errors=True)
    return T.finish()


def section8(base, live):
    """8. WHAT THIS PATCH IS FOR. Replace the example. `base` is the sandbox (patched copy) or the real root (--live).
    Run code in a subprocess so the test does not import the real modules into this process:"""
    code = ("import wdt_core as wc; "
            "print(hasattr(wc, '_example_helper'))")                           # <- the behaviour the patch is meant to add
    r = wl.run_py(base, [_runner(base, code)])
    T.check('8 example: patched function exists', r.returncode == 0 and r.stdout.strip() == 'True', r.stderr[-200:])


def _runner(base, code):
    """Write a one-line runner next to the code and return its path relative to `base` (run_py wants a script path)."""
    p = Path(base) / '_t_runner.py'
    p.write_text(code + '\n', encoding='utf-8')
    return p.name


if __name__ == '__main__':
    sys.exit(main())
