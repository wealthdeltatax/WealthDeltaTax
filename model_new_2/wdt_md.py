"""
wdt_md.py — WDT Unified Markdown Assembly
==========================================
Single source of truth for all markdown table construction and document
assembly used across VAL, VAL.S, RATES, and RATES.S output scripts.

Replaces
--------
  val_helpers.md_table()                     → md_table() / MdDoc
  16_5_VAL_S_assemble.md_table()             → md_table() / MdDoc
  5_3_VAL_generate_appc_full._build_pct_table() → pct_table() / MdDoc
  The A = lines.append / lines.append patterns → MdDoc

Public API
----------
Low-level table builder
  md_table(headers, rows, col_fmt=None, fmt_fn=None) -> str

Specialised table builders
  pct_table(row_keys, col_labels, data, row_label, fmt_fn) -> list[str]
  key_value_table(rows) -> str

Document class
  MdDoc                         accumulates lines, renders, writes

Column alignment constants
  LEFT, RIGHT, CENTER           pass as elements of col_fmt list

Design notes
------------
md_table() is the single canonical builder. It replaces three
implementations that differed only in:
  - Whether a fmt_fn was accepted (val_helpers: yes; 16_5: no)
  - Whether col 0 was treated as a label (val_helpers: yes; 16_5: no)
  - Column alignment (all used ':---:' centre; 5_4 hand-wrote mixed)

The new md_table() handles all three cases through:
  - col_fmt: optional list of LEFT/RIGHT/CENTER per column
  - fmt_fn:  optional formatter applied to non-label columns
  - The caller controls whether col 0 is pre-formatted or passed
    through fmt_fn by constructing rows accordingly

pct_table() replaces _build_pct_table() from 5_3. It takes a dict
keyed by row identifier and a list of values per key, and wraps each
row-0 cell in **bold** — exactly the pattern used throughout VAL.A §C.

MdDoc replaces both the `lines = []; A = lines.append; A('...')` and
`lines = []; lines.append('...')` patterns. Both were doing the same
thing; MdDoc provides a consistent interface with convenience methods
for the most common operations (blank line, section header, caption).
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Iterable, List, Optional, Sequence

# Column alignment tokens
LEFT   = 'left'
RIGHT  = 'right'
CENTER = 'center'

# Map token → markdown separator fragment
_SEP = {
    LEFT:   ':---',
    RIGHT:  '---:',
    CENTER: ':---:',
}


# ─────────────────────────────────────────────────────────────────────────────
# LOW-LEVEL TABLE BUILDER
# ─────────────────────────────────────────────────────────────────────────────

def md_table(
    headers: Sequence,
    rows: Sequence[Sequence],
    col_fmt: Optional[Sequence[str]] = None,
    fmt_fn: Optional[Callable] = None,
) -> str:
    """
    Build a markdown table and return it as a single string (no trailing newline).

    Parameters
    ----------
    headers  : sequence of column header strings (LaTeX is fine)
    rows     : sequence of rows; each row is a sequence of cell values.
               All values are converted to str unless fmt_fn is supplied.
    col_fmt  : optional list of LEFT / RIGHT / CENTER per column.
               Length must match len(headers).
               Default: CENTER for every column.
    fmt_fn   : optional callable applied to every cell value.
               When supplied, col 0 is still passed through fmt_fn unless
               the caller pre-formats it (e.g. wraps it in **bold**).
               Pass fmt_fn=None and pre-format all cells yourself if you
               need mixed per-column formatting.

    Returns
    -------
    str   multi-line markdown table, lines joined by '\\n'

    Examples
    --------
    # All-centre, no formatter (16_5 / plain style)
    md_table(['α', 'g1', 'g2'], [['0.1', '2.34%', '5.67%']])

    # Mixed alignment, no formatter (hand-written style from 5_4/8_3)
    md_table(
        ['Metric', 'Honest', 'Under'],
        [['**Entry basis**', '£20.000m', '£16.000m']],
        col_fmt=[LEFT, RIGHT, RIGHT],
    )

    # With fmt_fn, col 0 pre-formatted (val_helpers / 5_3 style)
    from wdt_fmt import fmt_pct
    md_table(
        ['α \\\\ g', '5%', '10%'],
        [['**0.1**', 0.023, 0.041], ['**1.0**', 0.0, 0.0]],
        fmt_fn=fmt_pct,
    )

    Migration notes
    ---------------
    val_helpers.md_table(headers, rows, fmt_fn=pct_str)
        → md_table(headers, rows, fmt_fn=fmt_pct)
          [col 0 treated as pre-formatted label; same behaviour because
           val_helpers skipped fmt_fn for col 0]

    16_5.md_table(headers, rows)
        → md_table(headers, rows)
          [identical; no fmt_fn, all centre-aligned]

    5_3._build_pct_table(alpha_list, col_labels, data_dict, row_label)
        → pct_table(alpha_list, col_labels, data_dict, row_label)
          [dedicated wrapper below]
    """
    n = len(headers)

    # Resolve alignment
    if col_fmt is None:
        col_fmt = [CENTER] * n
    if len(col_fmt) != n:
        raise ValueError(
            f"col_fmt length {len(col_fmt)} must match headers length {n}"
        )

    seps = [_SEP.get(a, ':---:') for a in col_fmt]

    lines: List[str] = []

    # Header row
    lines.append('| ' + ' | '.join(str(h) for h in headers) + ' |')

    # Separator row
    lines.append('|' + '|'.join(seps) + '|')

    # Data rows
    for row in rows:
        if fmt_fn is None:
            cells = [str(c) for c in row]
        else:
            cells = [str(row[0])] + [fmt_fn(c) for c in row[1:]]
        lines.append('| ' + ' | '.join(cells) + ' |')

    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# SPECIALISED TABLE BUILDERS
# ─────────────────────────────────────────────────────────────────────────────

def pct_table(
    row_keys: Sequence,
    col_labels: Sequence[str],
    data: dict,
    row_label: str = r'$\alpha$ \ $g$',
    fmt_fn: Optional[Callable] = None,
) -> List[str]:
    """
    Build a percentage-style VAL.A §C table and return raw markdown lines.

    This is the direct replacement for 5_3._build_pct_table().

    Each row is identified by a key from row_keys.  Row labels are rendered
    as **bold** (matching VAL.A §C convention).  data[key] is a list of
    numeric values, one per col_label, formatted by fmt_fn.

    Parameters
    ----------
    row_keys  : ordered list of row identifiers (e.g. ALPHA_VALS)
    col_labels: ordered list of column header strings
    data      : dict mapping each key → list of values (one per col_label)
    row_label : top-left header cell (default α \\ g)
    fmt_fn    : formatter applied to each data value.
                Default: lambda v: f'{v * 100:.2f}%'  (2dp percentage)

    Returns
    -------
    list[str]   raw markdown lines (no trailing blank line).
                Callers extend their own lines list with these.

    Migration notes
    ---------------
    5_3._build_pct_table(alpha_list, col_labels, data_dict, row_label)
        → pct_table(alpha_list, col_labels, data_dict, row_label)
    Return type changes: was list[str], still list[str]. Callers using
    `lines += _build_pct_table(...)` need no change.
    Callers using `lines.extend(_build_pct_table(...))` need no change.
    """
    if fmt_fn is None:
        def fmt_fn(v):  # noqa: F811
            if v is None:
                return '—'
            return f'{v * 100:.2f}%'

    headers = [row_label] + list(col_labels)
    result: List[str] = []

    # Header
    result.append('| ' + ' | '.join(str(h) for h in headers) + ' |')
    result.append('|' + '|'.join(':---:' for _ in headers) + '|')

    # Data rows — col 0 is bold label, rest are formatted values
    for key in row_keys:
        cells = [f'**{key}**'] + [fmt_fn(v) for v in data[key]]
        result.append('| ' + ' | '.join(cells) + ' |')

    return result


def key_value_table(
    rows: Sequence[tuple],
    col_fmt: Optional[Sequence[str]] = None,
) -> str:
    """
    Build a simple two-column (or n-column) key-value markdown table.

    Each element of rows is a tuple of (key_str, value_str, ...).
    Intended for parameter listings, glossaries, and metric summaries.

    Parameters
    ----------
    rows    : sequence of tuples; all elements should be pre-formatted strings
    col_fmt : column alignment list; defaults to [LEFT, LEFT, ...]

    Returns
    -------
    str   markdown table (no header row; callers pass headers as first row
          via the normal md_table() if they need one)

    Example
    -------
    key_value_table([
        ('| Parameter | Value |', ),   # ← use md_table for headers
    ])
    # Better pattern:
    md_table(
        ['Parameter', 'Value'],
        [['τ₀', '15%'], ['τ_m', '70%']],
        col_fmt=[LEFT, LEFT],
    )

    Migration notes
    ---------------
    The many hand-written `A('| Parameter | Value |'); A('|---|---|')` patterns
    in 8_3 and 16_6 are better replaced by md_table() with col_fmt=[LEFT, LEFT].
    This function exists for cases where all rows are already pre-formatted
    tuples with no fmt_fn needed.
    """
    if not rows:
        return ''

    n = len(rows[0])
    if col_fmt is None:
        col_fmt = [LEFT] * n

    # We have pre-formatted cells, so build a headerless table.
    # This is unusual in markdown; callers should emit the header
    # separately via md_table() if needed.
    seps = [_SEP.get(a, ':---') for a in col_fmt]
    lines: List[str] = []
    lines.append('|' + '|'.join(seps) + '|')
    for row in rows:
        lines.append('| ' + ' | '.join(str(c) for c in row) + ' |')
    return '\n'.join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# DOCUMENT CLASS
# ─────────────────────────────────────────────────────────────────────────────

class MdDoc:
    """
    Accumulate markdown lines, then render to string or write to file.

    Replaces two patterns found across the output scripts:

        Pattern A (8_3, 16_6):
            lines = []
            A = lines.append
            A('# Title')
            A('')
            A('some text')
            ...
            fh.write('\\n'.join(lines))

        Pattern B (5_3, 5_4, 16_5):
            lines = []
            lines.append('# Title')
            lines.append('')
            lines.append('some text')
            ...
            f.write('\\n'.join(lines))

    Usage
    -----
        doc = MdDoc()
        doc.h1('My Report')
        doc.blank()
        doc.add('Some prose paragraph.')
        doc.blank()
        doc.table(['Col A', 'Col B'], [['x', 'y']])
        doc.caption('Table 1: description.')
        doc.write(path)

    All methods return self so calls can be chained if desired.

    Important: render() and write() both produce '\\n'.join(self._lines),
    which is byte-identical to the existing scripts' output.  No trailing
    newline is added (matching existing behaviour).
    """

    def __init__(self):
        self._lines: List[str] = []

    # ── primitive ────────────────────────────────────────────────────────────

    def add(self, text: str = '') -> 'MdDoc':
        """
        Append one line of text.  Empty string → blank line in output.

        Migration notes
        ---------------
        Replaces both `A('...')` and `lines.append('...')`.
        For multi-line strings, use add_block() instead.
        """
        self._lines.append(text)
        return self

    def blank(self) -> 'MdDoc':
        """Append a blank line.  Shorthand for add('')."""
        return self.add('')

    def add_block(self, text: str) -> 'MdDoc':
        """
        Append a multi-line block by splitting on newlines.

        Useful for adding the output of md_table() or pct_table()
        without manually splitting first.
        """
        for line in text.split('\n'):
            self._lines.append(line)
        return self

    def add_lines(self, lines: Iterable[str]) -> 'MdDoc':
        """
        Extend with a pre-built list of lines (e.g. from pct_table()).

        Migration notes
        ---------------
        Replaces `lines += _build_pct_table(...)` and
                 `lines.extend(_build_pct_table(...))`.
        """
        self._lines.extend(lines)
        return self

    # ── section headings ────────────────────────────────────────────────────

    def h1(self, text: str) -> 'MdDoc':
        """Append a level-1 heading."""
        return self.add(f'# {text}')

    def h2(self, text: str) -> 'MdDoc':
        """Append a level-2 heading."""
        return self.add(f'## {text}')

    def h3(self, text: str) -> 'MdDoc':
        """Append a level-3 heading."""
        return self.add(f'### {text}')

    def h4(self, text: str) -> 'MdDoc':
        """Append a level-4 heading."""
        return self.add(f'#### {text}')

    def heading(self, text: str, level: int = 2) -> 'MdDoc':
        """Append a heading at the given level (1–4)."""
        if level not in (1, 2, 3, 4):
            raise ValueError(f"heading level must be 1–4, got {level}")
        return self.add('#' * level + ' ' + text)

    # ── semantic shortcuts ───────────────────────────────────────────────────

    def caption(self, text: str) -> 'MdDoc':
        """
        Append a table caption: blank line, text, blank line.

        VAL.B convention: captions appear BELOW the table they describe.
        Callers emit the table first, then call caption().

        Migration notes
        ---------------
        Replaces the pattern:
            lines.append('')
            lines.append('Table J.1: description. params.')
            lines.append('')
        """
        return self.blank().add(text).blank()

    def note(self, text: str) -> 'MdDoc':
        """
        Append an italic note paragraph: blank line, *text*, blank line.
        Wraps text in markdown italics if not already wrapped.
        """
        if not text.startswith('*'):
            text = f'*{text}*'
        return self.blank().add(text).blank()

    def rule(self) -> 'MdDoc':
        """Append a horizontal rule (---)."""
        return self.add('---')

    # ── table convenience ────────────────────────────────────────────────────

    def table(
        self,
        headers: Sequence,
        rows: Sequence[Sequence],
        col_fmt: Optional[Sequence[str]] = None,
        fmt_fn: Optional[Callable] = None,
    ) -> 'MdDoc':
        """
        Build a table and append it as lines (no surrounding blank lines).

        Callers should add blank lines explicitly before and after as needed,
        or use table_block() which adds them automatically.

        Parameters are identical to md_table().
        """
        return self.add_block(md_table(headers, rows, col_fmt=col_fmt, fmt_fn=fmt_fn))

    def table_block(
        self,
        headers: Sequence,
        rows: Sequence[Sequence],
        col_fmt: Optional[Sequence[str]] = None,
        fmt_fn: Optional[Callable] = None,
    ) -> 'MdDoc':
        """
        Blank line + table + blank line.

        Convenience for the common pattern of surrounding a table with
        blank lines (required by many markdown renderers for correct parsing).
        """
        return self.blank().table(headers, rows, col_fmt=col_fmt, fmt_fn=fmt_fn).blank()

    def pct_table(
        self,
        row_keys: Sequence,
        col_labels: Sequence[str],
        data: dict,
        row_label: str = r'$\alpha$ \ $g$',
        fmt_fn: Optional[Callable] = None,
    ) -> 'MdDoc':
        """
        Build a VAL.A §C-style percentage table and append its lines.

        Parameters are identical to the module-level pct_table() function.
        No surrounding blank lines are added; use blank() explicitly.
        """
        return self.add_lines(pct_table(row_keys, col_labels, data, row_label, fmt_fn))

    # ── rendering and I/O ────────────────────────────────────────────────────

    def render(self) -> str:
        """
        Return the document as a single string.

        Lines are joined with '\\n' with no trailing newline, matching
        the existing scripts' '\\n'.join(lines) pattern exactly.
        """
        return '\n'.join(self._lines)

    def write(self, path: Path, verbose: bool = True) -> Path:
        """
        Write the rendered document to path (UTF-8, no trailing newline).

        Creates parent directories if they do not exist.

        Parameters
        ----------
        path    : Path   destination file
        verbose : bool   if True, prints "Written: {path}" (default True)

        Returns
        -------
        Path   the path written to

        Migration notes
        ---------------
        Replaces the pattern:
            os.makedirs(OUT_DIR, exist_ok=True)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write('\\n'.join(lines))
            print(f'Written: {out_path}')
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        text = self.render()
        path.write_text(text, encoding='utf-8')
        if verbose:
            print(f'Written: {path}')
            print(f'Lines:   {len(self._lines)}')
        return path

    # ── introspection ────────────────────────────────────────────────────────

    def __len__(self) -> int:
        """Return number of lines accumulated."""
        return len(self._lines)

    def __repr__(self) -> str:
        return f'MdDoc({len(self._lines)} lines)'
