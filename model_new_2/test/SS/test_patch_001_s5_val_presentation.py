"""
test_patch_NNN_s5_val_presentation.py -- test for patch_NNN_s5_val_presentation.py (finds the patch by its slug, so renaming NNN is safe)

    python test_patch_NNN_s5_val_presentation.py          the patch, on a COPY of the code in a temp folder. Safe at any time.
    python test_patch_NNN_s5_val_presentation.py --live   the REAL tree, after the patch has been applied.

Checks 1-7 are the generic patch checks. Section 8 runs every new table and figure builder (and the rebuilt RIS) on a SYNTHETIC
valgen_data.json (s5_fixture.py, same shape valgen_core writes; random numbers, mean nothing) and asserts:
  * tables and figures declare the same ids and JSON keys, and every id is in [names.val];
  * every table builds a non-empty markdown table and every figure writes a PNG (figures go to a temp folder, never to OUTPUTS);
  * pairing: every number a table prints is in the paired figure's series;
  * a skipped part (no replay, no archetypes, no RATES JSON) gives a note / no figure, not an exception.
Needs matplotlib. It tests the presentation code, not valgen_core; the real JSON is checked by running the two scripts.
"""

import glob
import importlib.util
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import wdt_patchlib as wl                                    # noqa: E402

PATCH_FILE = sorted(HERE.glob('patch_*_s5_val_presentation.py'))[0]
REGRESSION = ['kernel_test.py']
LIVE = '--live' in sys.argv
NEW_IDS = ['RPL', 'ARC', 'BES', 'RSP', 'LCD', 'BAND', 'HLP']

spec_ = importlib.util.spec_from_file_location('the_patch', PATCH_FILE)
the_patch = importlib.util.module_from_spec(spec_)
spec_.loader.exec_module(the_patch)
SPEC, NAME = the_patch.SPEC, the_patch.NAME

T = wl.Checks(f'{NAME}: {"LIVE tree" if LIVE else "sandbox copy"}')

RUNNER = r'''
import importlib.util, json, math, sys, tempfile, tomllib
from pathlib import Path
sys.path.insert(0, r"%(here)s")
from s5_fixture import make_data
import wdt_core
root = Path(r"%(base)s")
def load(n, f):
    s = importlib.util.spec_from_file_location(n, f); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
tb = load('s5t', r"%(f_tables)s")
ch = load('s5c', r"%(f_charts)s")
ch._OUT = Path(tempfile.mkdtemp())
p = wdt_core.load_params()
d = make_data(p)
res = {'ids_equal': set(tb.PAIRS) == set(ch.PAIRS),
       'keys_equal': all(tb.PAIRS[k]['json'] == ch.PAIRS[k]['json'] for k in tb.PAIRS if k in ch.PAIRS),
       'builders': {}}
names = tomllib.loads(Path(r"%(f_toml)s").read_text(encoding='utf-8'))['names']['val']
res['names_ok'] = all(i in names and names[i]['kind'] == 'output' for i in %(ids)r + ['RIS'])
res['ris_name'] = names['RIS']['name']
def flat(ser):
    out = []
    for v in ser.values():
        out += [x for x in v if isinstance(x, (int, float)) and not isinstance(x, bool)]
    return out
for pid in %(ids)r + ['RIS']:
    t = tb.BUILDERS[pid](d, p); c = ch.BUILDERS[pid](d, p)
    fl = flat(c['series'])
    miss = [v for v in t['values'] if not any(math.isclose(v, x, rel_tol=1e-9, abs_tol=1e-12) for x in fl)]
    res['builders'][pid] = {'table_rows': t['md'].count('\n|'), 'values': len(t['values']), 'missing': len(miss),
                            'png': bool(c['path']) and Path(c['path']).exists()}
# skipped parts
d2 = make_data(p)
d2['replay'] = {'skipped': True}; d2['p6'] = {'archetypes': {}}; d2['p5']['hlc_pair'] = {'skipped': True, 'reason': 'no RATES JSON'}
skip = {}
for pid in ('RPL', 'ARC', 'BES', 'HLP'):
    t = tb.BUILDERS[pid](d2, p); c = ch.BUILDERS[pid](d2, p)
    skip[pid] = (t['md'].startswith(f'Table {pid}: not built') and t['values'] == [] and c['path'] is None)
res['skip_ok'] = skip
print('S5RESULT' + json.dumps(res))
'''


def read(p):
    return Path(p).read_bytes()


def run_regression(base):
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
        rep = wl.run_patch(SPEC, NAME, root=root, apply=False, quiet=True)
        T.check('live: every op already applied', all(r['applied'] == 0 and not r['changed'] for r in rep.values()),
                str({f: (r['applied'], r['skipped']) for f, r in rep.items()}))
        for f in names:
            wl.validate_text(f, wl.find_file(f, root).read_text(encoding='utf-8'))
        T.check('live: files compile / parse', True)
        after = run_regression(root)
        T.check('live: existing tests pass', all(rc == 0 for rc in after.values()), str(after))
        section8(root)
        return T.finish()

    sb = wl.make_sandbox(root)
    try:
        before = {f: read(wl.find_file(f, sb)) for f in names}
        base_rc = run_regression(sb)
        wl.run_patch(SPEC, NAME, root=sb, apply=False, quiet=True)
        T.check('1 dry run writes nothing', all(read(wl.find_file(f, sb)) == before[f] for f in names))
        rep = wl.run_patch(SPEC, NAME, root=sb, apply=True, quiet=True)
        already = all(r['applied'] == 0 for r in rep.values())
        if already:
            print('  NOTE  the tree already has this patch applied, so the sandbox test cannot show it applying; run it before --apply for that.')
        T.check('2 apply changes each file (or tree already patched)', already or all(r['changed'] and r['applied'] > 0 for r in rep.values()),
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
        T.check('4 patched files compile / parse', ok)

        def eol_ok(b0, b1):
            crlf0, lf0 = b0.count(b'\r\n'), b0.count(b'\n') - b0.count(b'\r\n')
            crlf1, lf1 = b1.count(b'\r\n'), b1.count(b'\n') - b1.count(b'\r\n')
            return (lf1 == 0) if (crlf0 and not lf0) else (crlf1 == 0)
        T.check('5 line endings preserved', all(eol_ok(before[f], after[f]) for f in names))
        same = all(read(p) == read(sb / p.relative_to(root)) for p in wl._walk(root)
                   if p.suffix in wl.CODE_SUFFIXES and p.name not in names and (sb / p.relative_to(root)).exists())
        T.check('6 files it does not name are untouched', same)
        now = run_regression(sb)
        T.check('7 existing tests no worse', all(now[t] <= base_rc[t] for t in now), f'before {base_rc}, after {now}')
        section8(sb)
    finally:
        shutil.rmtree(sb, ignore_errors=True)
    return T.finish()


def section8(base):
    """8. every new builder runs on the synthetic JSON, pairs table to figure, and degrades to a note when a part was skipped."""
    p = Path(base) / '_t_s5_runner.py'
    p.write_text(RUNNER % {'here': str(HERE), 'base': str(base), 'ids': NEW_IDS,
                                  'f_tables': str(wl.find_file('5_6_VALGEN_tables.py', base)),
                                  'f_charts': str(wl.find_file('5_7_VALGEN_charts.py', base)),
                                  'f_toml': str(wl.find_file('WDT_Params.toml', base))}, encoding='utf-8')
    r = wl.run_py(base, [p.name], timeout=600)
    line = [x for x in r.stdout.splitlines() if x.startswith('S5RESULT')]
    if r.returncode != 0 or not line:
        T.check('8 builders run on the synthetic JSON', False, (r.stderr or r.stdout)[-600:])
        return
    res = json.loads(line[0][len('S5RESULT'):])
    T.check('8a tables and figures declare the same ids and JSON keys', res['ids_equal'] and res['keys_equal'])
    T.check('8b every new id (and RIS) is in [names.val] as an output; RIS renamed', res['names_ok'] and 'Voluntary' in res['ris_name'], res['ris_name'])
    for pid, b in res['builders'].items():
        T.check(f'8c {pid}: table has rows, figure written, every printed number plotted',
                b['table_rows'] > 0 and b['png'] and b['missing'] == 0 and b['values'] > 0, str(b))
    T.check('8d skipped parts give a note and no figure, not an error', all(res['skip_ok'].values()), str(res['skip_ok']))


if __name__ == '__main__':
    sys.exit(main())