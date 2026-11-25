"""
project/tools/to_markdown.py: convert a local PDF (or Office file) to Markdown for reading.

For agents that need to read a binary file the Read tool handles badly (long, table-heavy, many pages).
Uses Microsoft's markitdown (MIT). Local files only: no URLs, no plugins, no cloud OCR.

    pip install 'markitdown[pdf]'                    (once per environment)
    python -I project/tools/to_markdown.py paper.pdf       -> scratch/converted/paper.md
    python -I project/tools/to_markdown.py a.pdf b.pdf -o some/dir
    python -I project/tools/to_markdown.py --readable data/x/a.pdf   -> literature/readable/data/x/a.pdf.md (committed)
    python -I project/tools/to_markdown.py --readable --all [--index]              every binary under data/ and literature/ lacking a copy

Output goes to `scratch/converted/` by default, which is git-ignored: a conversion is a reading aid,
not a repo file. `--readable` writes the committed reading copy instead (brief 130c): a mirror tree under
`literature/readable/` (a file under `data/` keeps its repository path plus `.md`; a file under `literature/` drops that folder, so `literature/a.pdf` gives `literature/readable/a.pdf.md`), with a header naming the source, route, tool and
date, a row cap per sheet (`--rows`, default 300, with a visible note) and a record in `readable/status.json`.
Routes: markitdown for pdf, docx, pptx, xlsx, xls and html; ODS goes through LibreOffice (headless, to xlsx)
then markitdown; RTF goes through pandoc. Quote numbers from the source, not from the copy: tables and
multi-column layouts can come out garbled, and scanned PDFs (no text layer) come out empty (status `poor`).
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import date
from importlib import metadata
from pathlib import Path

sys.path.insert(0, '.')  # python -I drops the cwd

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = Path('scratch/converted')
SOURCES = (Path('data'), Path('literature'))     # where the binaries live
READABLE = Path('literature/readable')
INDEX_NAME = 'readable-copies-index.md'
STATUS = 'status.json'
ROWS = 300
MARKITDOWN = ('.pdf', '.docx', '.pptx', '.xlsx', '.xls', '.html', '.htm')
SHEETS = ('.xlsx', '.xls', '.ods')
FALLBACK = {'.ods': 'soffice (ods to xlsx), then markitdown', '.rtf': 'pandoc (rtf to gfm)'}
BINARY = MARKITDOWN + tuple(FALLBACK)
POOR_WORDS_PER_PAGE = 40


def _markitdown():
    try:
        from markitdown import MarkItDown
    except ImportError:
        sys.exit("markitdown is not installed: pip install 'markitdown[pdf]' (add --break-system-packages in the cloud shell)")
    return MarkItDown(enable_plugins=False)


def route(src):
    """How a file is read: 'markitdown', or the fallback named in FALLBACK."""
    ext = Path(src).suffix.lower()
    return FALLBACK.get(ext, 'markitdown' if ext in MARKITDOWN else None)


def cap_tables(text, rows=ROWS):
    """Keep the first `rows` data rows of every Markdown table; add a visible note after a cut table. Returns (text, [(sheet, total rows)])."""
    out, cut, run, sheet = [], [], [], ''

    def flush():
        if not run:
            return
        data = len(run) - 2
        if data > rows:
            out.extend(run[:2 + rows])
            out.append(f'\n> *Truncated: the first {rows} of {data} rows of this table' + (f' (sheet "{sheet}")' if sheet else '') + ' are shown; read the source for the rest.*\n')
            cut.append((sheet, data))
        else:
            out.extend(run)
        run.clear()

    for line in text.split('\n'):
        if line.startswith('|'):
            run.append(line)
            continue
        flush()
        if line.startswith('## '):
            sheet = line[3:].strip()
        out.append(line)
    flush()
    return '\n'.join(out), cut


def _convert(md, src, ext):
    """(markdown text, route) for one file."""
    r = route(src)
    if ext == '.rtf':
        if not shutil.which('pandoc'):
            raise RuntimeError('pandoc not found (needed for RTF)')
        res = subprocess.run(['pandoc', '-f', 'rtf', '-t', 'gfm', '--wrap=none', str(src)], capture_output=True, text=True, timeout=1800)
        if res.returncode:
            raise RuntimeError('pandoc failed: ' + res.stderr.strip()[:200])
        return res.stdout, r
    if ext == '.ods':
        soffice = shutil.which('soffice') or shutil.which('libreoffice')
        if not soffice:
            raise RuntimeError('LibreOffice (soffice) not found (needed for ODS)')
        with tempfile.TemporaryDirectory() as tmp:
            res = subprocess.run([soffice, '--headless', '--convert-to', 'xlsx', '--outdir', tmp, str(src)], capture_output=True, text=True, timeout=600)
            made = Path(tmp) / (Path(src).stem + '.xlsx')
            if res.returncode or not made.is_file():
                raise RuntimeError('soffice failed: ' + (res.stderr or res.stdout).strip()[:200])
            return md.convert_local(str(made)).markdown, r
    return md.convert_local(str(src)).markdown, r


def pages_or_sheets(src):
    """'N pages', 'N sheets' or '' (not known cheaply)."""
    ext = Path(src).suffix.lower()
    try:
        if ext == '.pdf':
            from pypdf import PdfReader
            return f'{len(PdfReader(str(src)).pages)} pages'
        if ext == '.xlsx':
            import openpyxl
            wb = openpyxl.load_workbook(str(src), read_only=True)
            return f'{len(wb.worksheets)} sheets'
        if ext == '.ods':
            with zipfile.ZipFile(src) as z:
                return f"{len(re.findall(rb'<table:table ', z.read('content.xml')))} sheets"
    except Exception:  # a count is a convenience, never a reason to stop
        return ''
    return ''


def copy_path(rel):
    """Where the reading copy of the repository file `rel` lives: data/x/a.pdf -> literature/readable/data/x/a.pdf.md; literature/a.pdf -> literature/readable/a.pdf.md."""
    rel = Path(rel)
    if rel.parts[0] == 'literature':
        rel = Path(*rel.parts[1:])
    return READABLE / (rel.as_posix() + '.md')


def readable_copy(src, root=ROOT, rows=ROWS, md=None):
    """Write the reading copy of one file under root/data or root/literature; returns a dict (rel, dst, words, route, status, reason, cut)."""
    root, src = Path(root).resolve(), Path(src).resolve()
    if not src.is_file() or not any((root / b).resolve() in src.parents for b in SOURCES):
        raise ValueError(f'not a file under data/ or literature/: {src}')
    if (root / READABLE).resolve() in src.parents:
        raise ValueError(f'a reading copy is not converted again: {src}')
    rel = src.relative_to(root).as_posix()
    if route(src) is None:
        raise ValueError(f'no route for {src.suffix} files: {rel}')
    res = dict(rel=rel, dst=str(root / copy_path(rel)), route=route(src), words=0, status='failed', reason='', cut=[])
    try:
        text, _ = _convert(md or _markitdown(), src, src.suffix.lower())
    except Exception as exc:  # reported in the record, not raised: one bad file does not stop a batch
        res['reason'] = str(exc)[:200]
        return res
    if src.suffix.lower() in SHEETS:
        text, res['cut'] = cap_tables(text, rows)
    res['words'] = len(text.split())
    pages = pages_or_sheets(src)
    n = int(pages.split()[0]) if pages.endswith('pages') else 0
    if not text.strip():
        res.update(status='poor', reason='empty output (probably a scanned file with no text layer)')
    elif n and res['words'] < POOR_WORDS_PER_PAGE * n:
        res.update(status='poor', reason=f"{res['words']} words for {n} pages (little or no text layer)")
    else:
        res['status'] = 'ok'
    try:
        ver = metadata.version('markitdown')
    except metadata.PackageNotFoundError:
        ver = '?'
    head = [f"> **Reading copy** of `{rel}` ({src.stat().st_size / 1e6:.1f} MB" + (f', {pages}' if pages else '') + f"). Route: {res['route']}; tool: markitdown {ver}; converted {date.today().isoformat()}.",
            '> Generated, not edited. Quote numbers from the source file, not from this text.']
    if res['cut']:
        head.append(f'> Row cap: {rows} data rows a table; cut: ' + '; '.join(f'{s or "table"} ({n} rows)' for s, n in res['cut']) + '.')
    dst = Path(res['dst'])
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text('\n'.join(head) + '\n\n' + text, encoding='utf-8')
    res['bytes'] = dst.stat().st_size
    return res


def record(root, results):
    """Merge results into readable/status.json (the index reads it)."""
    path = Path(root) / READABLE / STATUS
    data = json.loads(path.read_text()) if path.is_file() else {}
    for r in results:
        data[r['rel']] = {k: r.get(k) for k in ('status', 'reason', 'route', 'words', 'bytes')} | {'cut': [[s, n] for s, n in r['cut']]}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(sorted(data.items())), indent=1) + '\n')


def binaries(root=ROOT):
    """Every binary file under data/ and literature/ (not the reading copies themselves), sorted by repository path."""
    root = Path(root)
    return sorted(p for b in SOURCES for p in (root / b).rglob('*')
                  if p.is_file() and p.suffix.lower() in BINARY and (root / READABLE) not in p.parents)


def index(root=ROOT):
    """Write readable-copies-index.md: one row per binary file under data/ and literature/."""
    root = Path(root)
    st = {}
    if (root / READABLE / STATUS).is_file():
        st = json.loads((root / READABLE / STATUS).read_text())
    rows, total = [], 0
    for p in binaries(root):
        rel = p.relative_to(root).as_posix()
        s = st.get(rel)
        copy = root / copy_path(rel)
        size = copy.stat().st_size if copy.is_file() else 0
        total += size
        status = (s['status'] if s else 'not yet converted')
        rows.append(f"| `{rel}` | {p.suffix.lower()[1:]} | {p.stat().st_size / 1e6:.1f} MB | {pages_or_sheets(p) or '-'} | {route(p)} | {status}{': ' + s['reason'] if s and s.get('reason') else ''} | {size / 1e6:.2f} MB |")
    head = ['# Reading copies of the research files', '', 'Generated by `python -I project/tools/to_markdown.py --readable --all --index` (brief 130c). A copy is a reading aid, not a source of record: quote numbers from the source. A file is `poor` when its copy is empty or thin (scanned or garbled); it is not hand-fixed.',
            f'Files: {len(rows)}; total size of the copies: {total / 1e6:.1f} MB.', '', '| Source (repository path) | Type | Size | Pages or sheets | Route | Status | Copy size |', '|---|---|---|---|---|---|---|']
    out = root / READABLE / INDEX_NAME
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text('\n'.join(head + rows) + '\n', encoding='utf-8')
    return len(rows), total


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('files', nargs='*', help='local PDF, docx, pptx, xlsx, xls, ods, rtf or html files')
    ap.add_argument('-o', '--out', default=str(DEFAULT_OUT), help='output directory (default %(default)s)')
    ap.add_argument('--readable', action='store_true', help='write the committed reading copy under literature/readable/ (mirror path plus .md)')
    ap.add_argument('--all', action='store_true', help='with --readable: every binary under data/ and literature/ that lacks a copy')
    ap.add_argument('--force', action='store_true', help='with --all: convert again even if a copy exists')
    ap.add_argument('--rows', type=int, default=ROWS, help='with --readable: data rows kept per table in spreadsheets (default %(default)s)')
    ap.add_argument('--index', action='store_true', help='with --readable: write readable-copies-index.md at the end')
    ap.add_argument('--root', default=str(ROOT), help='repository root (default: this repository)')
    a = ap.parse_args(argv)
    if a.readable:
        root = Path(a.root)
        todo = [Path(f) for f in a.files]
        if a.all:
            todo += [p for p in binaries(root) if a.force or not (root / copy_path(p.relative_to(root).as_posix())).is_file()]
        if not todo and not a.index and not a.all:
            ap.error('nothing to do: give files, --all or --index')
        md, results, bad = (_markitdown() if todo else None), [], 0
        for f in todo:
            try:
                r = readable_copy(f, root, a.rows, md)
            except ValueError as exc:
                print(f'skip: {exc}', file=sys.stderr)
                bad = 1
                continue
            results.append(r)
            print(f"{r['rel']}: {r['status']} ({r['words']} words, {r.get('bytes', 0)} bytes, {r['route']})" + (f": {r['reason']}" if r['reason'] else ''), flush=True)
        if results:
            record(root, results)
        if a.index:
            n, total = index(root)
            print(f'index: {n} files, copies {total / 1e6:.1f} MB')
        print(f"summary: {sum(r['status'] == 'ok' for r in results)} ok, {sum(r['status'] == 'poor' for r in results)} poor, {sum(r['status'] == 'failed' for r in results)} failed, {sum(r.get('bytes', 0) for r in results)} bytes")
        return bad or int(any(r['status'] == 'failed' for r in results))
    if not a.files:
        ap.error('no files given')
    md = _markitdown()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    status = 0
    for f in a.files:
        src = Path(f)
        if not src.is_file():
            print(f'skip (not a local file): {f}', file=sys.stderr)
            status = 1
            continue
        text, _ = _convert(md, src, src.suffix.lower())
        dst = out / (src.stem.replace(' ', '_') + '.md')
        dst.write_text(text, encoding='utf-8')
        note = '' if text.strip() else '  WARNING: empty, probably a scanned PDF (no text layer)'
        print(f'{src} -> {dst}  ({len(text.split())} words){note}')
    return status


if __name__ == '__main__':
    sys.exit(main())
