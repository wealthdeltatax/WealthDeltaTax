"""patchlib -- shared helper for numbered WDT patches.

Usage in a patch:  from patchlib import Patch
    P = Patch('W2-01', __doc__)
    P.replace('rates_core.py', old, new, count=1)
    P.regex('wdt_core.py', pattern, repl, count=1)
    P.run()

Default is a DRY RUN (reports every edit, writes nothing).  --apply writes,
after saving <file>.bak-<patch>.  Any anchor whose match count differs from
the expected count aborts the whole patch before anything is written.
CRLF files are matched and written back as CRLF.
"""
import argparse, os, re, shutil, sys

def _root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(here)          # Model/

def _find(name, root):
    if os.path.isabs(name) and os.path.exists(name):
        return name
    hits = []
    for d, _, fs in os.walk(root):
        if os.sep + 'test' in d or '.bak' in d:
            pass
        if name in fs:
            hits.append(os.path.join(d, name))
    hits = [h for h in hits if '/test/' not in h.replace('\\', '/') or name.endswith('_test.py') or name.startswith('test_')]
    if len(hits) != 1:
        raise SystemExit(f'[abort] {name}: expected 1 file under {root}, found {len(hits)}: {hits}')
    return hits[0]

class Patch:
    def __init__(self, pid, doc=''):
        self.pid, self.doc, self.ops = pid, (doc or '').strip(), []
        ap = argparse.ArgumentParser(description=self.doc.splitlines()[0] if self.doc else pid)
        ap.add_argument('--apply', action='store_true', help='write changes (default: dry run)')
        ap.add_argument('--root', default=_root(), help='Model root (default: parent of test/)')
        self.args = ap.parse_args()

    # --- edit declarations -------------------------------------------------
    def replace(self, f, old, new, count=1):
        self.ops.append(('lit', f, old, new, count))
    def regex(self, f, pat, repl, count=1, flags=re.M):
        self.ops.append(('re', f, re.compile(pat, flags), repl, count))
    def append(self, f, text, marker):
        """append text unless `marker` already present (idempotent)"""
        self.ops.append(('app', f, marker, text, 1))

    def create(self, name, text):
        """create Model/<name> (root-relative) unless it exists; abort if it exists with different content"""
        self.ops.append(('new', name, None, text, 1))

    # --- execution ---------------------------------------------------------
    def run(self):
        root, state, log = self.args.root, {}, []
        news = []
        for kind, f, a, b, n in self.ops:
            if kind == 'new':
                tgt = os.path.join(root, f)
                if os.path.exists(tgt):
                    cur = open(tgt, 'rb').read().decode('utf-8').replace('\r\n', '\n')
                    if cur != b.replace('\r\n', '\n'):
                        raise SystemExit(f'[abort] {f} exists with different content')
                    log.append(f'  [skip ] {f}: already exists'); continue
                news.append((tgt, b)); log.append(f'  [new  ] {f}'); continue
            path = _find(f, root)
            if path not in state:
                raw = open(path, 'rb').read().decode('utf-8')
                crlf = '\r\n' in raw
                state[path] = [raw.replace('\r\n', '\n'), crlf, raw]
            txt = state[path][0]
            if kind == 'lit':
                a2, b2 = a.replace('\r\n', '\n'), b.replace('\r\n', '\n')
                k = txt.count(a2)
                if b2 and b2 != a2 and txt.count(b2) >= 1:      # new text present => already applied (even if new contains old)
                    log.append(f'  [skip ] {f}: already applied  ({a2[:50]!r})'); continue
                if k != n:
                    raise SystemExit(f'[abort] {f}: anchor found {k}x, expected {n}x:\n{a2[:300]}')
                txt = txt.replace(a2, b2)
            elif kind == 're':
                k = len(a.findall(txt))
                if k == 0 and n != 0:
                    log.append(f'  [skip?] {f}: regex 0 hits (already applied?) {a.pattern[:60]!r}'); continue
                if k != n:
                    raise SystemExit(f'[abort] {f}: regex found {k}x, expected {n}x: {a.pattern[:120]}')
                txt = a.sub(b, txt)
            else:
                if a in txt:
                    log.append(f'  [skip ] {f}: marker present'); continue
                txt = txt.rstrip('\n') + '\n' + b
            state[path][0] = txt
            log.append(f'  [edit ] {f}: {kind} x{n}')
        print(f'== patch {self.pid} ({"APPLY" if self.args.apply else "DRY RUN"}) ==')
        print('\n'.join(log))
        changed = [p for p, (t, c, raw) in state.items()
                   if (t.replace('\n', '\r\n') if c else t) != raw]
        if not self.args.apply:
            print(f'{len(changed) + len(news)} file(s) would change. Re-run with --apply.'); return
        for tgt, b in news:
            open(tgt, 'wb').write(b.encode('utf-8')); print(f'  created {tgt}')
        for p in changed:
            t, c, raw = state[p]
            shutil.copy2(p, f'{p}.bak-{self.pid}')
            open(p, 'wb').write((t.replace('\n', '\r\n') if c else t).encode('utf-8'))
            print(f'  wrote {p}  (backup .bak-{self.pid})')
        print(f'{len(changed)} file(s) written.')
