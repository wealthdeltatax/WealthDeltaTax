"""
pipeline/to_markdown.py: convert a local PDF (or Office file) to Markdown for reading.

For agents that need to read a PDF the Read tool handles badly (long, table-heavy, many pages).
Uses Microsoft's markitdown (MIT). Local files only: no URLs, no plugins, no cloud OCR.

    pip install 'markitdown[pdf]'                    (once per environment)
    python -I pipeline/to_markdown.py paper.pdf       -> scratch/converted/paper.md
    python -I pipeline/to_markdown.py a.pdf b.pdf -o some/dir

Output goes to `scratch/converted/` by default, which is git-ignored: a conversion is a reading aid,
not a repo file. Quote numbers from the PDF itself, not from this text, when they matter: tables and
multi-column layouts can come out garbled, and scanned PDFs (no text layer) come out empty.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, '.')  # python -I drops the cwd

DEFAULT_OUT = Path('scratch/converted')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('files', nargs='+', help='local PDF, docx, pptx, xlsx or html files')
    ap.add_argument('-o', '--out', default=str(DEFAULT_OUT), help='output directory (default %(default)s)')
    a = ap.parse_args(argv)
    try:
        from markitdown import MarkItDown
    except ImportError:
        sys.exit("markitdown is not installed: pip install 'markitdown[pdf]' (add --break-system-packages in the cloud shell)")
    md = MarkItDown(enable_plugins=False)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    status = 0
    for f in a.files:
        src = Path(f)
        if not src.is_file():
            print(f'skip (not a local file): {f}', file=sys.stderr)
            status = 1
            continue
        text = md.convert_local(str(src)).markdown
        dst = out / (src.stem.replace(' ', '_') + '.md')
        dst.write_text(text, encoding='utf-8')
        note = '' if text.strip() else '  WARNING: empty, probably a scanned PDF (no text layer)'
        print(f'{src} -> {dst}  ({len(text.split())} words){note}')
    return status


if __name__ == '__main__':
    sys.exit(main())
