"""
test_wdt_md.py — Tests for wdt_md.py
=====================================
Each group verifies:
  1. Correct markdown is produced
  2. Drop-in compatibility with the predecessor it replaces
  3. Edge cases (empty rows, None values, special chars)

Run with:
    python test_wdt_md.py
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import wdt_md as M
from wdt_md import LEFT, RIGHT, CENTER

# ── test runner ──────────────────────────────────────────────────────────────
_PASS = 0
_FAIL = 0


def check(label: str, got, expected):
    global _PASS, _FAIL
    if got == expected:
        _PASS += 1
    else:
        _FAIL += 1
        print(f"  FAIL  {label}")
        print(f"        got:      {got!r}")
        print(f"        expected: {expected!r}")


def section(title: str):
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")


# ─────────────────────────────────────────────────────────────────────────────
# 1. md_table — basic cases
# ─────────────────────────────────────────────────────────────────────────────

section("md_table — basic structure")

# Minimal table
result = M.md_table(['A', 'B'], [['x', 'y']])
lines = result.split('\n')
check("header line",    lines[0], '| A | B |')
check("sep line",       lines[1], '|:---:|:---:|')
check("data line",      lines[2], '| x | y |')
check("line count",     len(lines), 3)

# Three columns
result = M.md_table(['H1', 'H2', 'H3'], [['a', 'b', 'c'], ['d', 'e', 'f']])
lines = result.split('\n')
check("3col header",   lines[0], '| H1 | H2 | H3 |')
check("3col sep",      lines[1], '|:---:|:---:|:---:|')
check("3col row1",     lines[2], '| a | b | c |')
check("3col row2",     lines[3], '| d | e | f |')
check("3col count",    len(lines), 4)


section("md_table — column alignment")

result = M.md_table(
    ['Metric', 'Value'],
    [['**Entry basis**', '£20.000m']],
    col_fmt=[LEFT, RIGHT],
)
lines = result.split('\n')
check("left+right header", lines[0], '| Metric | Value |')
check("left+right sep",    lines[1], '|:---|---:|')
check("left+right data",   lines[2], '| **Entry basis** | £20.000m |')

result = M.md_table(
    ['A', 'B', 'C'],
    [['x', 'y', 'z']],
    col_fmt=[LEFT, CENTER, RIGHT],
)
lines = result.split('\n')
check("mixed sep", lines[1], '|:---|:---:|---:|')


section("md_table — fmt_fn applied to cols 1+")

def _pct(v):
    if v is None:
        return '—'
    return f'{v * 100:.2f}%'

result = M.md_table(
    [r'$\alpha$ \ $g$', '5%', '10%'],
    [['**0.1**', 0.023, 0.041]],
    fmt_fn=_pct,
)
lines = result.split('\n')
check("fmt_fn col0 untouched", lines[2].startswith('| **0.1**'), True)
check("fmt_fn col1",           '2.30%' in lines[2],             True)
check("fmt_fn col2",           '4.10%' in lines[2],             True)

# None passes through fmt_fn
result = M.md_table(['A', 'B'], [['label', None]], fmt_fn=_pct)
check("fmt_fn None", '—' in result, True)


section("md_table — col_fmt length mismatch raises")

try:
    M.md_table(['A', 'B'], [['x', 'y']], col_fmt=[LEFT])
    check("length mismatch raises", False, True)  # should not reach here
except ValueError:
    check("length mismatch raises", True, True)


# ─────────────────────────────────────────────────────────────────────────────
# 2. Compatibility with predecessor implementations
# ─────────────────────────────────────────────────────────────────────────────

section("md_table — drop-in for val_helpers.md_table")

# val_helpers.md_table(headers, rows, fmt_fn=None)
# - default fmt_fn was pct_str (2dp), col 0 untouched
# - all columns centre-aligned

def _old_val_md_table(headers, rows, fmt_fn=None):
    if fmt_fn is None:
        fmt_fn = lambda v: f'{v * 100:.2f}%'
    lines = []
    lines.append('| ' + ' | '.join(str(h) for h in headers) + ' |')
    lines.append('|' + '|'.join(':---:' for _ in headers) + '|')
    for row in rows:
        cells = [str(row[0])] + [fmt_fn(v) for v in row[1:]]
        lines.append('| ' + ' | '.join(cells) + ' |')
    return '\n'.join(lines)

# fn=_pct: must produce identical output to val_helpers with explicit fmt_fn
old = _old_val_md_table(['α', 'g1'], [['**0.1**', 0.023], ['**1.0**', 0.0]], fmt_fn=_pct)
new = M.md_table(         ['α', 'g1'], [['**0.1**', 0.023], ['**1.0**', 0.0]], fmt_fn=_pct)
check("val_helpers compat fn=_pct", new, old)

# fn=None: val_helpers used pct_str as a hidden default; the new md_table
# does NOT do this (hidden defaults cause bugs). Callers that relied on the
# default must now pass fmt_fn explicitly.  Verify new behaviour: str() applied.
new_no_fn = M.md_table(['α', 'g1'], [['**0.1**', 0.023], ['**1.0**', 0.0]])
check("no fmt_fn uses str()", '| **0.1** | 0.023 |' in new_no_fn, True)


section("md_table — drop-in for 16_5.md_table")

# 16_5.md_table(headers, rows) — no fmt_fn, all pre-formatted strings
def _old_16_5_md_table(headers, rows):
    lines = ['| ' + ' | '.join(str(h) for h in headers) + ' |']
    lines.append('|' + '|'.join(':---:' for _ in headers) + '|')
    for row in rows:
        lines.append('| ' + ' | '.join(str(c) for c in row) + ' |')
    return '\n'.join(lines)

for headers, rows in [
    (['α \\ g', '5%', '10%'], [['**0.1**', '2.30%', '4.10%']]),
    (['N', 'TW', 'Net'],       [['5', '22.4', '1.2'], ['10', '28.1', '2.5']]),
]:
    old = _old_16_5_md_table(headers, rows)
    new = M.md_table(headers, rows)
    check(f"16_5 compat headers={headers}", new, old)


# ─────────────────────────────────────────────────────────────────────────────
# 3. pct_table
# ─────────────────────────────────────────────────────────────────────────────

section("pct_table — basic structure")

data = {0.1: [0.023, 0.041], 1.0: [0.0, 0.0]}
result_lines = M.pct_table([0.1, 1.0], ['5%', '10%'], data)

check("returns list",     isinstance(result_lines, list),    True)
check("header in list",   result_lines[0].startswith('|'),   True)
check("sep row",          ':---:' in result_lines[1],        True)
check("bold row label",   '**0.1**' in result_lines[2],      True)
check("bold row label2",  '**1.0**' in result_lines[3],      True)
check("default fmt 2dp",  '2.30%' in result_lines[2],        True)


section("pct_table — custom row_label")

lines = M.pct_table(
    [1.0, 1.8], ['k1', 'k2'],
    {1.0: [0.1, 0.2], 1.8: [0.3, 0.4]},
    row_label=r'$\alpha$ \ $k$',
)
check("custom row_label in header", r'$\alpha$ \ $k$' in lines[0], True)


section("pct_table — custom fmt_fn")

from wdt_fmt import fmt_pct
lines = M.pct_table(
    [0.1], ['5%'],
    {0.1: [0.0232]},
    fmt_fn=lambda v: fmt_pct(v, dp=1),
)
check("custom fmt_fn 1dp", '2.3%' in lines[2], True)


section("pct_table — drop-in for 5_3._build_pct_table")

def _old_build_pct_table(row_alpha_list, col_labels, data_dict,
                          row_label=r'$\alpha$ \ $g$'):
    def pct_str(v, decimals=2):
        return f'{v * 100:.{decimals}f}%'
    lines = []
    header_cells = [row_label] + col_labels
    lines.append('| ' + ' | '.join(header_cells) + ' |')
    lines.append('|' + '|'.join(':---:' for _ in header_cells) + '|')
    for alpha in row_alpha_list:
        cells = [f'**{alpha}**'] + [pct_str(v, 2) for v in data_dict[alpha]]
        lines.append('| ' + ' | '.join(cells) + ' |')
    return lines

test_data  = {0.1: [0.023, 0.041], 0.5: [0.015, 0.031], 1.0: [0.0, 0.0]}
test_cols  = ['5.9%', '10.5%']
test_keys  = [0.1, 0.5, 1.0]
old_result = _old_build_pct_table(test_keys, test_cols, test_data)
new_result = M.pct_table(test_keys, test_cols, test_data)

check("pct_table compat length", len(new_result), len(old_result))
for i, (old_line, new_line) in enumerate(zip(old_result, new_result)):
    check(f"pct_table compat line {i}", new_line, old_line)


# ─────────────────────────────────────────────────────────────────────────────
# 4. MdDoc — primitive operations
# ─────────────────────────────────────────────────────────────────────────────

section("MdDoc — add and blank")

doc = M.MdDoc()
doc.add('line one')
doc.blank()
doc.add('line three')
rendered = doc.render()
check("render 3 lines", rendered, 'line one\n\nline three')
check("len", len(doc), 3)
check("repr", 'MdDoc' in repr(doc), True)


section("MdDoc — heading methods")

doc = M.MdDoc()
doc.h1('Title').h2('Section').h3('Sub').h4('Sub-sub')
lines = doc.render().split('\n')
check("h1", lines[0], '# Title')
check("h2", lines[1], '## Section')
check("h3", lines[2], '### Sub')
check("h4", lines[3], '#### Sub-sub')

doc2 = M.MdDoc()
doc2.heading('Dynamic', level=2)
check("heading(level=2)", doc2.render(), '## Dynamic')

try:
    doc2.heading('Bad', level=5)
    check("heading level 5 raises", False, True)
except ValueError:
    check("heading level 5 raises", True, True)


section("MdDoc — add_block and add_lines")

doc = M.MdDoc()
doc.add_block('line A\nline B\nline C')
check("add_block splits", len(doc), 3)
check("add_block first",  doc._lines[0], 'line A')
check("add_block last",   doc._lines[2], 'line C')

doc2 = M.MdDoc()
doc2.add_lines(['x', 'y', 'z'])
check("add_lines", doc2.render(), 'x\ny\nz')


section("MdDoc — caption and note")

doc = M.MdDoc()
doc.add('Table content').caption('Table 1: description.')
lines = doc.render().split('\n')
check("caption blank before", lines[1], '')
check("caption text",         lines[2], 'Table 1: description.')
check("caption blank after",  lines[3], '')

doc2 = M.MdDoc()
doc2.note('A note.')
lines2 = doc2.render().split('\n')
check("note blank before", lines2[0], '')
check("note italic",       lines2[1], '*A note.*')
check("note blank after",  lines2[2], '')

# note with already-italicised text
doc3 = M.MdDoc()
doc3.note('*Already italic.*')
check("note already italic", doc3._lines[1], '*Already italic.*')


section("MdDoc — rule")

doc = M.MdDoc()
doc.rule()
check("rule", doc.render(), '---')


section("MdDoc — table convenience")

doc = M.MdDoc()
doc.table(['A', 'B'], [['x', 'y']])
lines = doc.render().split('\n')
check("table no blanks", len(lines), 3)

doc2 = M.MdDoc()
doc2.table_block(['A', 'B'], [['x', 'y']])
lines2 = doc2.render().split('\n')
check("table_block blank before", lines2[0], '')
check("table_block content",      lines2[1], '| A | B |')
check("table_block blank after",  lines2[-1], '')


section("MdDoc — pct_table method")

doc = M.MdDoc()
data = {0.1: [0.023], 1.0: [0.0]}
doc.pct_table([0.1, 1.0], ['5%'], data)
rendered = doc.render()
check("pct_table via MdDoc", '**0.1**' in rendered, True)
check("pct_table fmt",       '2.30%'   in rendered, True)


section("MdDoc — chaining")

doc = (M.MdDoc()
       .h1('Report')
       .blank()
       .add('Intro paragraph.')
       .blank()
       .table(['Col'], [['val']])
       .blank())

lines = doc.render().split('\n')
check("chain h1",    lines[0], '# Report')
check("chain blank", lines[1], '')
check("chain prose", lines[2], 'Intro paragraph.')


# ─────────────────────────────────────────────────────────────────────────────
# 5. MdDoc.write()
# ─────────────────────────────────────────────────────────────────────────────

section("MdDoc.write — file I/O")

with tempfile.TemporaryDirectory() as tmp:
    p = Path(tmp) / 'sub' / 'out.md'
    doc = M.MdDoc()
    doc.add('# Hello').blank().add('World.')
    returned = doc.write(p, verbose=False)

    check("write creates file",    p.exists(), True)
    check("write returns path",    returned,   p)
    content = p.read_text(encoding='utf-8')
    check("write content",         content,    '# Hello\n\nWorld.')
    check("no trailing newline",   content.endswith('World.'), True)

    # Check parent directories created
    p2 = Path(tmp) / 'deep' / 'nested' / 'dir' / 'file.md'
    M.MdDoc().add('x').write(p2, verbose=False)
    check("write creates parents", p2.exists(), True)


# ─────────────────────────────────────────────────────────────────────────────
# 6. MdDoc — exact output equivalence with existing scripts
# ─────────────────────────────────────────────────────────────────────────────

section("MdDoc — equivalence with 5_4 lines.append pattern")

# Reproduce the header block from 5_4 main() using MdDoc
# Original:
#   lines = []
#   lines.append("# VAL.B Worked Examples — Numerical Figures")
#   lines.append(f"")
#   lines.append(f"**Generated:** 2026-08-13  ")
#   ...
#   md = '\n'.join(lines)

original_lines = [
    "# VAL.B Worked Examples — Numerical Figures",
    "",
    "**Generated:** 2026-08-13  ",
    "**Model:** Python v1.0 standalone  ",
    "",
]
original = '\n'.join(original_lines)

doc = M.MdDoc()
doc.add("# VAL.B Worked Examples — Numerical Figures")
doc.blank()
doc.add("**Generated:** 2026-08-13  ")
doc.add("**Model:** Python v1.0 standalone  ")
doc.blank()

check("5_4 header equivalence", doc.render(), original)


section("MdDoc — equivalence with 8_3 A = lines.append pattern")

# Reproduce a fragment from 8_3 write_output_md using MdDoc
# Original:
#   A('## B.1 Active Parameters')
#   A('')
#   A('| Parameter | Value |')
#   A('|---|---|')
#   A('| τ₀ | 15% |')
#   A('')

original_lines = [
    '## B.1 Active Parameters',
    '',
    '| Parameter | Value |',
    '|---|---|',
    '| τ₀ | 15% |',
    '',
]
original = '\n'.join(original_lines)

doc = M.MdDoc()
doc.h2('B.1 Active Parameters')
doc.blank()
# The 8_3 tables have custom separators (|---|---|) not supported by md_table,
# so we keep those as raw add() calls — the point is MdDoc handles both
doc.add('| Parameter | Value |')
doc.add('|---|---|')
doc.add('| τ₀ | 15% |')
doc.blank()

check("8_3 fragment equivalence", doc.render(), original)


# ─────────────────────────────────────────────────────────────────────────────
# 7. Edge cases
# ─────────────────────────────────────────────────────────────────────────────

section("Edge cases")

# Empty rows list
result = M.md_table(['A', 'B'], [])
lines = result.split('\n')
check("empty rows — header present", lines[0], '| A | B |')
check("empty rows — sep present",    lines[1], '|:---:|:---:|')
check("empty rows — line count",     len(lines), 2)

# Single column table
result = M.md_table(['Only'], [['val']])
lines = result.split('\n')
check("single col header", lines[0], '| Only |')
check("single col sep",    lines[1], '|:---:|')

# LaTeX in headers
result = M.md_table([r'$\alpha$ \ $g$', r'$\tau$'], [[r'**0.1**', '15%']])
check("LaTeX in header survives", r'$\alpha$' in result, True)

# Integer values without fmt_fn
result = M.md_table(['N', 'Count'], [[5, 42]])
check("int values", '| 5 | 42 |' in result, True)

# MdDoc empty render
doc = M.MdDoc()
check("empty doc render", doc.render(), '')
check("empty doc len",    len(doc),     0)


# ─────────────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────────────

print(f"\n{'═' * 60}")
print(f"  Results: {_PASS} passed, {_FAIL} failed")
print(f"{'═' * 60}")

if _FAIL > 0:
    sys.exit(1)
