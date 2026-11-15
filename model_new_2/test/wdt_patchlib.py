"""
wdt_patchlib.py -- helpers for patch scripts and their tests (lives in Model/test/)
====================================================================================
Copy this file into Model/test/ once. Every patch_NNN_*.py and test_patch_NNN_*.py imports it.
 
Why it exists: the big files (wdt_core.py, valgen_core.py, rates_core.py, WDT_Params.toml) are too
large to rewrite or hold in context, so edits are made by a script that finds an ANCHOR in the file and
replaces / inserts text there. The library makes that safe:
 
  * the anchor must match EXACTLY ONCE (zero or several matches abort the patch, nothing is written);
  * a patch is idempotent: running it twice leaves the file as after the first run;
  * the result is syntax-checked (.py compiles, .toml parses) BEFORE anything is written;
  * line endings (CRLF on Windows) and UTF-8 (£, tau) are preserved;
  * the original is copied to Model/test/_backups/<patch>/ before the first write;
  * the default is a DRY RUN. Nothing changes without --apply.
 
It also finds the model folder and the files in it, so a patch never hardcodes a path:
 
  model_root()          the folder that holds WDT_Params.toml, found by walking up from this file
  find_file(name)       the ONE file with that name under the model root (error if 0 or >1)
  add_import_paths()    puts the model root and every folder with a *_core.py / wdt_*.py on sys.path
  layout()              {file name: relative path} of every project .py / .toml / .bat (for printing)
 
and the test side (same PASS/FAIL style as kernel_test.py):
 
  make_sandbox(...)     copy the code (not OUTPUTS, not test) to a temp folder; the JST fixture goes where
                        [rates].jst_path is looked up, so the real big JST is never needed
  run_py(sandbox, ...)  run a script in the sandbox in a subprocess (smoke runs)
  Checks                check(name, ok, detail); finish() exits non-zero on any failure
 
Run `python wdt_patchlib.py` to print the layout it sees, and `python wdt_patchlib.py next` for the next
patch number.
"""
 
from __future__ import annotations
 
import argparse
import datetime as _dt
import os
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path
 
MARKER = 'WDT_Params.toml'
SKIP_DIRS = {'test', 'tests', 'OUTPUTS', '__pycache__', '.git', '.venv', 'venv', 'node_modules', '_backups', 'fixtures'}
CODE_SUFFIXES = {'.py', '.toml', '.bat'}
 
 
class PatchError(RuntimeError):
    """An anchor did not match exactly once, or the patched text is invalid. Nothing was written."""
 
 
# ─────────────────────────────────────────────────────────────
# FINDING THINGS
# ─────────────────────────────────────────────────────────────
 
def model_root(start=None) -> Path:
    """Walk up from `start` (default: this file) to the first folder containing WDT_Params.toml, looking one level down as a fallback."""
    here = Path(start or __file__).resolve()
    here = here if here.is_dir() else here.parent
    for d in [here, *here.parents]:
        if (d / MARKER).exists():
            return d
    for d in [here, *here.parents]:
        hits = [c for c in d.iterdir() if c.is_dir() and (c / MARKER).exists()] if d.exists() else []
        if len(hits) == 1:
            return hits[0]
    raise FileNotFoundError(f'no {MARKER} above {here}; run from inside the model folder (Model/test)')
 
 
def _walk(root: Path):
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            yield Path(dp) / fn
 
 
def layout(root=None) -> dict:
    """{file name: [relative paths]} for every .py / .toml / .bat outside test/ and OUTPUTS/."""
    root = Path(root) if root else model_root()
    out: dict = {}
    for p in _walk(root):
        if p.suffix in CODE_SUFFIXES:
            out.setdefault(p.name, []).append(str(p.relative_to(root)))
    return dict(sorted(out.items()))
 
 
def find_file(name: str, root=None) -> Path:
    """The single file called `name` under the model root. Raises with the candidates if there are none or several."""
    root = Path(root) if root else model_root()
    hits = [p for p in _walk(root) if p.name == name]
    if len(hits) != 1:
        found = ', '.join(str(h.relative_to(root)) for h in hits) or 'none'
        raise FileNotFoundError(f'{name}: expected exactly one match under {root}, found {found}')
    return hits[0]
 
 
def import_dirs(root=None) -> list:
    """Folders that must be on sys.path to import the project modules: the root and any folder holding *_core.py / wdt_*.py."""
    root = Path(root) if root else model_root()
    dirs = [root]
    for p in _walk(root):
        if p.suffix == '.py' and (p.name.endswith('_core.py') or p.name.startswith('wdt_')) and p.parent not in dirs:
            dirs.append(p.parent)
    return dirs
 
 
def add_import_paths(root=None) -> list:
    """Put import_dirs() at the front of sys.path (idempotent). Returns the list. Call before importing wdt_core etc."""
    dirs = import_dirs(root)
    for d in reversed(dirs):
        if str(d) not in sys.path:
            sys.path.insert(0, str(d))
    return dirs
 
 
def next_number(root=None) -> str:
    """Next free patch number, 3 digits, from patch_NNN_*.py already in Model/test."""
    root = Path(root) if root else model_root()
    tdir = root / 'test'
    nums = [int(m.group(1)) for p in tdir.glob('patch_*.py') if (m := re.match(r'patch_(\d+)_', p.name))] if tdir.exists() else []
    return f'{(max(nums) + 1) if nums else 1:03d}'
 
 
# ─────────────────────────────────────────────────────────────
# EDIT OPERATIONS (text -> text)
# ─────────────────────────────────────────────────────────────
 
@dataclass
class Op:
    """One edit. kind: replace | insert_after | insert_before | delete. `done` is an optional marker: text that is present only after the edit
    (defaults to `new`); if it is already in the file and the anchor is gone, the op counts as already applied."""
    kind: str
    anchor: str
    new: str = ''
    label: str = ''
    done: str | None = None
 
 
def Replace(old, new, label='', done=None):
    return Op('replace', old, new, label or 'replace', done)
 
 
def InsertAfter(anchor, new, label='', done=None):
    return Op('insert_after', anchor, new, label or 'insert_after', done)
 
 
def InsertBefore(anchor, new, label='', done=None):
    return Op('insert_before', anchor, new, label or 'insert_before', done)
 
 
def Delete(old, label=''):
    return Op('delete', old, '', label or 'delete', None)
 
 
def _nl(text: str) -> str:
    return '\r\n' if '\r\n' in text else '\n'
 
 
def _line_of(text: str, idx: int) -> int:
    return text.count('\n', 0, idx) + 1
 
 
def apply_op(text: str, op: Op):
    """Apply one op. Returns (new_text, status) with status 'applied' or 'skipped' (already applied). Raises PatchError."""
    nl = _nl(text)
    fix = (lambda s: s.replace('\r\n', '\n').replace('\n', nl))
    anchor, new = fix(op.anchor), fix(op.new)
    done = fix(op.done if op.done is not None else op.new)
    n = text.count(anchor)
    # Already applied? An insert (or a replace whose new text still contains the old) leaves the anchor in place, so "anchor found
    # once" alone would apply it a second time on a re-run: for those, the marker `done` is checked FIRST. For a replace that removes
    # its anchor, the edit counts as done only when the anchor is gone AND the marker is present. A marker shorter than 12
    # characters is too generic to trust (it would match unrelated text and hide a mistyped anchor), so the op demands `done=`.
    survives = op.kind in ('insert_after', 'insert_before') or (op.kind == 'replace' and anchor in new)
    if op.kind != 'delete' and done and ((survives and n >= 1) or n == 0):
        if done in text:
            if len(done.strip()) < 12:
                raise PatchError(f'[{op.label}] cannot tell whether this is already applied: the marker {done.strip()!r} is too short; pass done="<distinctive text that exists only after the edit>"')
            return text, 'skipped'
    if n == 0:
        if op.kind == 'delete':
            return text, 'skipped'
        raise PatchError(f'[{op.label}] anchor not found (0 matches). First line: {op.anchor.strip().splitlines()[0][:100]!r}')
    if n > 1:
        lines = ', '.join(str(_line_of(text, m.start())) for m in re.finditer(re.escape(anchor), text))
        raise PatchError(f'[{op.label}] anchor matches {n} times (lines {lines}); lengthen it until it is unique')
    i = text.index(anchor)
    if op.kind == 'replace':
        return text[:i] + new + text[i + len(anchor):], 'applied'
    if op.kind == 'insert_after':
        j = i + len(anchor)
        return text[:j] + new + text[j:], 'applied'
    if op.kind == 'insert_before':
        return text[:i] + new + text[i:], 'applied'
    if op.kind == 'delete':
        return text[:i] + text[i + len(anchor):], 'applied'
    raise PatchError(f'[{op.label}] unknown op kind {op.kind!r}')
 
 
def validate_text(name: str, text: str) -> None:
    """Syntax-check patched text: .py must compile, .toml must parse. Raises PatchError."""
    try:
        if name.endswith('.py'):
            compile(text, name, 'exec')
        elif name.endswith('.toml'):
            tomllib.loads(text)
    except (SyntaxError, tomllib.TOMLDecodeError, ValueError) as e:
        raise PatchError(f'{name}: patched text is invalid: {e}') from e
 
 
def _read(path: Path) -> str:
    with open(path, 'r', encoding='utf-8', newline='') as fh:
        return fh.read()
 
 
def _write(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + '.tmp')
    with open(tmp, 'w', encoding='utf-8', newline='') as fh:
        fh.write(text)
    os.replace(tmp, path)
 
 
def run_patch(spec: dict, name: str, root=None, apply=False, quiet=False) -> dict:
    """
    Apply `spec` = {file name: [Op, ...]} to the files under `root` (default: the real model root).
    All files are patched in memory and validated first; only if every op on every file succeeds are any written,
    so a failed patch never leaves a half-edited tree. apply=False is a dry run.
    Returns {file name: {'path', 'applied': n, 'skipped': n, 'changed': bool, 'lines_before', 'lines_after'}}.
    """
    root = Path(root) if root else model_root()
    staged, report = {}, {}
    for fname, ops in spec.items():
        path = find_file(fname, root)
        text = _read(path)
        a = s = 0
        for op in ops:
            text, st = apply_op(text, op)
            a += st == 'applied'
            s += st == 'skipped'
            if not quiet:
                print(f'  {fname}: {st:8s} {op.label}')
        validate_text(fname, text)
        staged[fname] = (path, text, text != _read(path))
        report[fname] = {'path': str(path), 'applied': a, 'skipped': s, 'changed': text != _read(path),
                         'lines_before': _read(path).count('\n'), 'lines_after': text.count('\n')}
    if apply:
        bdir = root / 'test' / '_backups' / name
        for fname, (path, text, changed) in staged.items():
            if not changed:
                continue
            bdir.mkdir(parents=True, exist_ok=True)
            if not (bdir / fname).exists():
                shutil.copy2(path, bdir / fname)
            _write(path, text)
    return report
 
 
def patch_cli(spec: dict, name: str, doc: str = '') -> int:
    """Command line for a patch script: dry run by default, --apply to write, --root to point at another tree (the tests do)."""
    ap = argparse.ArgumentParser(description=doc or name)
    ap.add_argument('--apply', action='store_true', help='write the changes (default is a dry run)')
    ap.add_argument('--root', default=None, help='model folder to patch (default: the real one)')
    a = ap.parse_args()
    print(f'{name}: {"APPLY" if a.apply else "DRY RUN"} on {Path(a.root).resolve() if a.root else model_root()}')
    try:
        rep = run_patch(spec, name, root=a.root, apply=a.apply)
    except (PatchError, FileNotFoundError) as e:
        print(f'ABORTED, nothing written: {e}')
        return 1
    for f, r in rep.items():
        print(f'  {f}: {r["applied"]} applied, {r["skipped"]} already applied, lines {r["lines_before"]} -> {r["lines_after"]}')
    if not a.apply:
        print('dry run only; re-run with --apply to write')
    else:
        print(f'originals saved under test/_backups/{name}/')
    return 0
 
 
# ─────────────────────────────────────────────────────────────
# TEST SIDE
# ─────────────────────────────────────────────────────────────
 
def make_sandbox(root=None, jst_fixture=None, extra_files=()) -> Path:
    """
    Copy every .py / .toml / .bat of the model (not test/, not OUTPUTS/) to a fresh temp folder, keeping the relative layout.
    If `jst_fixture` is given, copy it to the places wdt_jst.load_jst looks first (sandbox/RATES/ and the sandbox root), under the
    file name [rates].jst_path gives, so the real JST is never needed. Caller removes the sandbox with shutil.rmtree.
    """
    root = Path(root) if root else model_root()
    sb = Path(tempfile.mkdtemp(prefix='wdt_sandbox_'))
    for p in _walk(root):
        if p.suffix in CODE_SUFFIXES or p.name in set(extra_files):
            dst = sb / p.relative_to(root)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dst)
    if jst_fixture:
        toml = sb / MARKER
        try:
            jst_name = tomllib.loads(_read(toml))['rates']['jst_path']
        except Exception:                                      # noqa: BLE001
            jst_name = 'jst_r6.json'
        for d in (sb / 'RATES', sb):
            d.mkdir(parents=True, exist_ok=True)
            shutil.copy2(jst_fixture, d / jst_name)
    return sb
 
 
def run_py(sandbox, args, timeout=300, env_extra=None):
    """Run `python <args>` with cwd = the folder of the script (so relative paths behave as in real use) and the sandbox's import dirs on PYTHONPATH.
    Returns the CompletedProcess (stdout/stderr as text). `args[0]` is a path relative to the sandbox."""
    sandbox = Path(sandbox)
    script = sandbox / args[0]
    env = dict(os.environ)
    env['PYTHONPATH'] = os.pathsep.join(str(d) for d in import_dirs(sandbox)) + os.pathsep + env.get('PYTHONPATH', '')
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env.update(env_extra or {})
    return subprocess.run([sys.executable, str(script), *map(str, args[1:])], cwd=script.parent, env=env,
                          capture_output=True, text=True, timeout=timeout)
 
 
def compiles(path) -> bool:
    try:
        py_compile.compile(str(path), doraise=True, cfile=os.devnull)
        return True
    except py_compile.PyCompileError:
        return False
 
 
class Checks:
    """kernel_test.py style: check(name, ok, detail) prints PASS/FAIL; finish() prints the tally and returns the exit code."""
 
    def __init__(self, title=''):
        self.results = []
        if title:
            print(title)
 
    def check(self, name, ok, detail=''):
        self.results.append((name, bool(ok), detail))
        print(f"  {'PASS' if ok else 'FAIL'}  {name} {detail}")
        return bool(ok)
 
    def raises(self, name, fn, exc=Exception, contains=''):
        try:
            fn()
        except exc as e:
            return self.check(name, contains in str(e), f'({type(e).__name__}: {str(e)[:90]})')
        return self.check(name, False, '(no exception raised)')
 
    def finish(self) -> int:
        bad = [r for r in self.results if not r[1]]
        print(f'\n{len(self.results) - len(bad)} passed, {len(bad)} failed')
        return 1 if bad else 0
 
 
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'next':
        print(next_number())
    else:
        r = model_root()
        print(f'model root: {r}   (today {_dt.date.today()})')
        for n, paths in layout(r).items():
            print(f'  {n:34s} {", ".join(paths)}')
        print('import dirs:', [str(d.relative_to(r)) or '.' for d in import_dirs(r)])
        print('next patch number:', next_number(r))
