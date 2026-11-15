"""
apply_s1_readers.py -- S1 follow-up 2: stop the last readers of the retired switches reset_interval / death_waiver.

Run from the Model/ folder:   python apply_s1_readers.py [--dry-run]

Edits (exact-match or regex, idempotent; a file is backed up to <name>.bak_s1b before its first write):
  kernel_test.py, SS/bridge_test.py
      drop `reset_interval=0, ` and `death_waiver=0, ` from the keyword lists passed to run_family3
      (it raises TypeError on them since S1; 0 was the default, so the runs are unchanged).
  VAL/5_6_VALGEN_tables.py
      CDS caption read s['reset_interval'], a key p3_surface no longer carries (KeyError). The surface is the
      no-reset case, so the caption now says so.  RIS caption/label: "reset interval" -> the family's own cycle.
  wdt_kernel.py
      docstring line: "With reset_interval = 0 and death_waiver = 0 ..." -> current wording.
Missing files are skipped with a note.
"""
import re
import shutil
import sys
from pathlib import Path

DRY = '--dry-run' in sys.argv
HERE = Path(__file__).resolve().parent

KW = [re.compile(r"reset_interval\s*=\s*0\s*,\s*"), re.compile(r"death_waiver\s*=\s*0\s*,\s*")]

EXACT = {
    'VAL/5_6_VALGEN_tables.py': [
        ("λ = 0, reset every {s['reset_interval']} years. Cells marked",
         "λ = 0, no voluntary reset (a reset is a strategy action, not a rule). Cells marked"),
        ("by reset interval, α_C = 1. A reset re-values ",
         "by the family's own voluntary reset cycle, α_C = 1; the honest family never resets. A reset re-values "),
        ("['Reset interval \\\\ α_D']", "['Reset cycle \\\\ α_D']"),
    ],
}


def write(path, new, todo):
    if todo and not DRY:
        shutil.copy2(path, path.with_name(path.name + '.bak_s1b'))
        path.write_text(new, encoding='utf-8')
    print(f'  {"would apply" if DRY else "applied"} {todo} edit(s) to {path.relative_to(HERE)}')


def strip_kwargs(rel):
    path = HERE / rel
    if not path.exists():
        print(f'  SKIP  {rel}: not found')
        return
    text = path.read_text(encoding='utf-8')
    new, n = text, 0
    for rx in KW:
        new, k = rx.subn('', new)
        n += k
    if not n:
        print(f'  ok    {rel}: nothing to remove')
        return
    write(path, new, n)


def exact(rel, edits):
    path = HERE / rel
    if not path.exists():
        print(f'  SKIP  {rel}: not found')
        return
    new, todo = path.read_text(encoding='utf-8'), 0
    for old, rep in edits:
        c = new.count(old)
        if c == 1:
            new, todo = new.replace(old, rep), todo + 1
        elif c == 0 and rep in new:
            print(f'  ok    {rel}: already applied ({old[:40]!r})')
        else:
            raise SystemExit(f'{rel}: expected one match, found {c} for {old[:60]!r}')
    if todo:
        write(path, new, todo)


def kernel_doc():
    path = HERE / 'wdt_kernel.py'
    if not path.exists():
        print('  SKIP  wdt_kernel.py: not found')
        return
    text = path.read_text(encoding='utf-8')
    rx = re.compile(r"With reset_interval = 0 and death_waiver = 0 the kernel reproduces")
    if not rx.search(text):
        print('  ok    wdt_kernel.py: docstring already current')
        return
    new = rx.sub("With no voluntary reset (reset years empty; the scheduled reset_interval and death_waiver are retired) the kernel reproduces", text)
    write(path, new, 1)


if __name__ == '__main__':
    for rel in ('kernel_test.py', 'SS/bridge_test.py'):
        strip_kwargs(rel)
    for rel, ed in EXACT.items():
        exact(rel, ed)
    kernel_doc()
    print('Any other live reader:')
    pat = re.compile(r"reset_interval|death_waiver")
    for f in sorted(HERE.rglob('*.py')):
        if f.name.startswith('apply_') or f.name.endswith('_patch.py'):
            continue
        for i, line in enumerate(f.read_text(encoding='utf-8', errors='ignore').splitlines(), 1):
            if pat.search(line.split('#', 1)[0]):
                print(f'  LIVE? {f.relative_to(HERE)}:{i}: {line.strip()[:100]}')
