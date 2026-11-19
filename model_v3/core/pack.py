"""core/pack.py: country pack and register loader (architecture.md 2.1; country-pack.md sections 2, 3 and 5). Layer L0: numpy and the standard library only.

Reads a pack folder as country-pack.md says: manifest first, folder name equals `country`, per-file sha256, header equals the schema, and the first
violation raises PackError('<file>:<row>:<column>: <reason>'), the header being row 1. Nothing is filled, interpolated, clipped or defaulted: a missing
cell stays None. Percent columns hold percent numbers and are never rescaled. This module names no country, currency or tax line. The part-of relation
between tax lines, the lines a retirement sums and the pointers of X1 come from the caller (levers.json), by the author's ruling of 2026-11-18.

Conventions (R6). pack_sha256 is the sha256 of '<country>\\n', then the canonical JSON (sorted keys, no spaces) of {country, currency, base_year,
pack_version} and '\\n', then one '<name> <file sha256>\\n' per file sorted by name. A file whose hash differs from the manifest raises with the file; row
and column are added when the changed file also fails its schema (a changed value that stays valid cannot be located from a hash alone).
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np


class PackError(ValueError):
    pass


LICENCES = {'ogl-v3', 'cc-by', 'cite-only', 'unverified'}
HEADER = ('country', 'currency', 'base_year', 'pack_version', 'built', 'files')
FILE_KEYS = ('name', 'dataset', 'sha256', 'rows', 'source', 'licence', 'retrieved', 'vintage')
F, I, T = 'float', 'int', 'text'
PCT, RET, SHARE, BASIS = ('in', 0, 100), ('ex', -100, 1000), ('rh', 0, 100), ('enum', {'household', 'adult'})
SCHEMA = {   # dataset -> [(column, kind, missing allowed, check)]; country-pack.md section 3
    'returns': [('year', I, 0, None), ('eq_tr', F, 1, RET), ('housing_tr', F, 1, RET), ('bond_tr', F, 1, RET),
                ('capital_tr', F, 1, RET), ('cpi', F, 0, ('gt', 0)), ('gdp_pc', F, 1, ('gt', 0))],
    'wealth_distribution': [('variable', T, 0, None), ('band', T, 0, None), ('value', F, 0, None),
                            ('unit', T, 0, ('enum', {'pct_total_wealth', 'pct_households', 'gbp_bn', 'pct_of_band', 'thousand', 'gbp'})),
                            ('basis', T, 0, BASIS), ('year', T, 0, None)],
    'wealth_tail': [('series', T, 0, None), ('year', I, 0, None), ('value', F, 0, None),
                    ('unit', T, 0, ('enum', {'pct_wealth', 'gbp_bn', 'pct_total'})), ('low', F, 1, None), ('high', F, 1, None),
                    ('basis', T, 0, BASIS)],
    'receipts': [('line', T, 0, None), ('fiscal_year', T, 0, None), ('pct_gdp', F, 0, SHARE), ('gbp_bn', F, 1, None),
                 ('basis', T, 0, ('enum', {'forecast', 'outturn'}))],
    'household_incidence': [('variable', T, 0, None), ('group', T, 0, None), ('tax', T, 1, None), ('value', F, 0, None),
                            ('unit', T, 0, ('enum', {'gbp_per_household_year', 'pct_gross_income', 'pct_individuals', 'pct_of_tax'})),
                            ('fiscal_year', T, 0, None), ('basis', T, 0, ('enum', {'equivalised_disposable', 'original'}))],
    'tax_rules': [('rule', T, 0, None), ('tax_year', T, 0, None), ('subject', T, 1, None), ('lower', F, 1, None),
                  ('upper', F, 1, None), ('rate', F, 1, PCT), ('amount', F, 1, None), ('flag', T, 1, ('enum', {'true', 'false'}))],
    'public_expenditure': [('function', T, 0, None), ('fiscal_year', T, 0, None), ('pct_gdp', F, 0, ('ex', 0, 100)), ('gbp_bn', F, 1, None),
                           ('basis', T, 0, None)],
}


@dataclass(frozen=True)
class Pack:
    country: str
    currency: str
    base_year: int | None
    version: int
    built: str
    files: dict      # file name -> its manifest entry
    tables: dict     # dataset -> list of row dicts (typed; None where the cell is empty)
    sha256: str      # pack_sha256


@dataclass(frozen=True)
class Row:
    id: str
    low: float | None
    central: float | None
    high: float | None
    unit: str
    judgement: bool


def _bad(v, chk):
    k = chk[0]
    if k == 'enum':
        return None if v in chk[1] else f'{v!r} is not one of {sorted(chk[1])}'
    ok = {'in': lambda: chk[1] <= v <= chk[2], 'ex': lambda: chk[1] < v < chk[2], 'rh': lambda: chk[1] <= v < chk[2],
          'gt': lambda: v > chk[1]}[k]()
    return None if ok else f'{v} outside the range {chk[0]} {chk[1:]}'


def _cell(s, kind):
    if kind == T:
        return s
    v = int(s) if kind == I else float(s)
    if kind == F and not math.isfinite(v):
        raise ValueError(s)
    return v


def _read(path, ds):
    """Rows of one CSV as typed dicts; the first schema violation raises with file, row and column."""
    name, spec = path.name, SCHEMA[ds]
    with open(path, newline='', encoding='utf-8') as fh:
        raw = list(csv.reader(fh))
    cols = tuple(c[0] for c in spec)
    if not raw or tuple(raw[0]) != cols:
        raise PackError(f'{name}:1:header: want {list(cols)}, got {raw[0] if raw else "an empty file"}')
    out = []
    for r, cells in enumerate(raw[1:], 2):
        if len(cells) != len(spec):
            raise PackError(f'{name}:{r}:-: {len(cells)} cells, want {len(spec)}')
        row = {}
        for (col, kind, null, chk), s in zip(spec, cells):
            if s == '':
                if not null:
                    raise PackError(f'{name}:{r}:{col}: empty cell where the schema allows none')
                row[col] = None
                continue
            try:
                v = _cell(s, kind)
            except ValueError:
                raise PackError(f'{name}:{r}:{col}: {s!r} is not a {kind}') from None
            if chk and _bad(v, chk):
                raise PackError(f'{name}:{r}:{col}: {_bad(v, chk)}')
            row[col] = v
        if row.get('unit', '').startswith('pct') and not 0 <= row['value'] <= 100:
            raise PackError(f'{name}:{r}:value: {row["value"]} is a percent outside [0, 100]')
        out.append(row)
    return out


def _unique(n, rows, cols):
    seen = {}
    for r, row in enumerate(rows, 2):
        k = tuple(row[c] for c in cols)
        if k in seen:
            raise PackError(f'{n}:{r}:{cols[0]}: duplicate of row {seen[k]} on {list(cols)}')
        seen[k] = r


def _x_returns(n, rows):
    for r, (a, b) in enumerate(zip(rows, rows[1:]), 3):
        if b['year'] != a['year'] + 1:
            raise PackError(f'{n}:{r}:year: {b["year"]} does not follow {a["year"]} (strictly increasing, no gaps)')


def _x_wealth(n, rows):
    _unique(n, rows, ('variable', 'band', 'basis', 'year'))
    groups = defaultdict(list)
    for r, row in enumerate(rows, 2):
        groups[(row['variable'], row['basis'], row['year'], row['unit'])].append((r, row))
    for (var, _, _, unit), g in groups.items():
        if unit in ('pct_total_wealth', 'pct_households') and all(re.fullmatch(r'D\d+', x['band']) for _, x in g):
            if abs(sum(x['value'] for _, x in g) - 100) > 0.5:
                raise PackError(f'{n}:{g[0][0]}:value: bands of {var} partition the population but sum to '
                                f'{sum(x["value"] for _, x in g):.3f}, not 100 within 0.5')
        bands = {x['band']: x['value'] for _, x in g}
        part, tol = sum(v for b, v in bands.items() if b != 'all'), max(0.5, 1e-4 * bands.get('all', 0))   # the printed 'all' is rounded, the bands are not
        if unit in ('gbp_bn', 'thousand') and len(bands) > 1 and 'all' in bands and all(re.fullmatch(r'D\d+|all', b) for b in bands) and abs(part - bands['all']) > tol:
            raise PackError(f'{n}:{g[0][0]}:value: bands D1 to D10 of {var} sum to {part:.3f}, not the printed all {bands["all"]} within {tol:.3f}')
    bad = next(((r, x['variable']) for r, x in enumerate(rows, 2) if x['variable'] in ('median_house_price', 'gdp') and x['value'] <= 0), None)
    if bad: raise PackError(f'{n}:{bad[0]}:value: {bad[1]} must be greater than 0')


def _x_tail(n, rows):
    for r, row in enumerate(rows, 2):
        for col, ok in (('low', lambda b, v: b <= v), ('high', lambda b, v: v <= b)):
            if row[col] is not None and not ok(row[col], row['value']):
                raise PackError(f'{n}:{r}:{col}: low <= value <= high does not hold')


def _x_household(n, rows):
    groups = defaultdict(lambda: ([], []))
    for r, row in enumerate(rows, 2):
        if row['variable'].startswith('tax_share_') and row['tax'] is None:
            raise PackError(f'{n}:{r}:tax: empty for a tax_share variable')
        k = (row['variable'], row['tax'], row['fiscal_year'], row['basis'], row['unit'])
        side = groups[k][0] if row['group'].startswith('Q') else groups[k][1] if row['group'].startswith('D') else None
        if side is not None:
            side.append((r, row['value']))
    for q, d in groups.values():
        if len(q) == 5 and len(d) == 10:
            mq, md = sum(v for _, v in q) / 5, sum(v for _, v in d) / 10
            if abs(md - mq) > 0.01 * abs(mq):
                raise PackError(f'{n}:{d[0][0]}:value: decile mean {md:.4g} differs from quintile mean {mq:.4g} by more than 1%')


def _x_rules(n, rows):
    last = {}
    for r, row in enumerate(rows, 2):
        if sum(row[c] is not None for c in ('rate', 'amount', 'flag')) != 1:
            raise PackError(f'{n}:{r}:rate: exactly one of rate, amount and flag must be non-empty')
        if row['lower'] is None:
            continue
        k = (row['rule'], row['tax_year'])
        if k in last and (last[k][1] is None or row['lower'] < last[k][1]):
            raise PackError(f'{n}:{r}:lower: bands of {k[0]} must be ordered and not overlap')
        last[k] = (row['lower'], row['upper'])


def _no_total(n):
    raise PackError(f'{n}:-:function: a non-empty file needs a total row (the reference expenditure over GDP)')


CROSS = {'returns': _x_returns, 'wealth_distribution': _x_wealth, 'wealth_tail': _x_tail, 'receipts': lambda n, rows: _unique(n, rows, ('line', 'fiscal_year', 'basis')),
         'household_incidence': _x_household, 'tax_rules': _x_rules, 'public_expenditure': lambda n, rows: rows and not any(x['function'] == 'total' for x in rows) and _no_total(n)}


def _pack_hash(m, shas):
    head = json.dumps({k: m[k] for k in ('country', 'currency', 'base_year', 'pack_version')}, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256((f'{m["country"]}\n{head}\n' + ''.join(f'{k} {shas[k]}\n' for k in sorted(shas))).encode('utf-8')).hexdigest()


def load_pack(folder):
    """Read and validate the pack in `folder` (named by its country code); returns a Pack or raises PackError."""
    folder = Path(folder)
    if not (folder / 'manifest.json').is_file():
        raise PackError(f'{folder.name}: manifest.json is missing')
    m = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    for k in HEADER:
        if k not in m or (k != 'base_year' and m[k] in ('', [], None)):
            raise PackError(f'manifest.json:{k}: missing or empty')
    if m['country'] != folder.name:
        raise PackError(f'manifest.json:country: {m["country"]!r} differs from the folder name {folder.name!r}')
    tables, files = {}, {}
    for f in m['files']:
        gone = [k for k in FILE_KEYS if f.get(k) in (None, '')]
        if gone or f['licence'] not in LICENCES or f['dataset'] not in SCHEMA or f['dataset'] in tables:
            raise PackError(f'manifest.json:files:{f.get("name")}: bad entry (missing {gone}, licence, dataset or a repeated dataset)')
        path = folder / f['name']
        if not path.is_file():
            raise PackError(f'{f["name"]}: listed in the manifest and not found')
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        try:
            rows, err = _read(path, f['dataset']), None
        except PackError as e:
            rows, err = None, e
        if actual != f['sha256']:
            raise PackError(f'{f["name"]}: sha256 mismatch (manifest {f["sha256"][:12]}, file {actual[:12]})'
                            + (f'; first violation {err}' if err else ''))
        if err:
            raise err
        CROSS[f['dataset']](f['name'], rows)
        if len(rows) != f['rows']:
            raise PackError(f'{f["name"]}: manifest says {f["rows"]} rows, file has {len(rows)}')
        tables[f['dataset']], files[f['name']] = rows, f
    return Pack(m['country'], m['currency'], m['base_year'], m['pack_version'], m['built'], files, tables,
                _pack_hash(m, {k: v['sha256'] for k, v in files.items()}))


def load_register(path):
    """registry/inputs.json as {id: Row}: low, central and high per id (None where the register has no number), the (J) flag and the unit."""
    out = {}
    for r in json.loads(Path(path).read_text(encoding='utf-8'))['inputs']:
        i, v = r.get('id'), [r.get(k) for k in ('low', 'central', 'high')]
        if i in out or any(x is not None and (isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x)) for x in v):
            raise PackError(f'register:{i}: duplicate id, or low, central or high is neither a finite number nor null')
        out[i] = Row(i, *(None if x is None else float(x) for x in v), str(r.get('unit', '')), bool(r['judgement']))
    return out


def lookup(pack, dataset, **where):
    """Rows of a dataset whose columns equal `where`."""
    return [r for r in pack.tables[dataset] if all(r[k] == v for k, v in where.items())]


def series(pack, column):
    """(years, values) of a returns column as arrays; an empty cell is nan, never filled."""
    rows = pack.tables['returns']
    return np.array([r['year'] for r in rows]), np.array([np.nan if r[column] is None else r[column] for r in rows])


def _by_line(pack, fiscal_year=None, basis=None):
    out = defaultdict(dict)
    for r in pack.tables['receipts']:
        if (fiscal_year in (None, r['fiscal_year'])) and (basis in (None, r['basis'])):
            out[(r['fiscal_year'], r['basis'])][r['line']] = r['pct_gdp']
    return out


def _one(pack, fiscal_year, basis):
    sets = _by_line(pack, fiscal_year, basis)
    if len(sets) != 1:
        raise PackError(f'receipts: {len(sets)} (fiscal_year, basis) sets match; say which')
    return next(iter(sets.values()))


def check_parts(pack, parts):
    """Each parent line (key of `parts`) is at least the sum of its listed parts, in every fiscal year and basis."""
    for key, lines in _by_line(pack).items():
        for parent, kids in parts.items():
            if parent in lines and sum(lines[k] for k in kids) > lines[parent] + 1e-9:
                raise PackError(f'receipts {key}: parts of {parent} sum to more than {parent}')


def receipts_sum(pack, lines, parts=None, fiscal_year=None, basis=None):
    """Sum of pct_gdp over `lines`; refuses a line summed with one of its own parts (`parts` maps parent -> parts)."""
    have = _one(pack, fiscal_year, basis)
    for parent, kids in (parts or {}).items():
        if parent in lines and any(k in lines for k in kids):
            raise PackError(f'receipts_sum: {parent} is summed with its own parts')
    if [x for x in lines if x not in have]:
        raise PackError(f'receipts_sum: no such line: {[x for x in lines if x not in have]}')
    return sum(have[x] for x in lines)


def check_x1(pack, register, pointers, tol=1e-9):
    """X1: the register's central value of each pointed id equals the pack value. pointers: {id: (dataset, where, column)}."""
    for i, (ds, where, col) in pointers.items():
        rows = lookup(pack, ds, **where)
        if len(rows) != 1 or abs(rows[0][col] - register[i].central) > tol:
            raise PackError(f'X1 {i}: register {register[i].central} differs from the pack ({len(rows)} matching rows)')
    return len(pointers)


def check_x2(pack, lines, target, tol=0.01, parts=None, fiscal_year=None, basis=None):
    """X2: the lines a retirement sums add to `target` (percent of GDP) within `tol`; returns the sum."""
    s = receipts_sum(pack, lines, parts, fiscal_year, basis)
    if abs(s - target) > tol:
        raise PackError(f'X2: the lines sum to {s:.4f}, not {target} within {tol}')
    return s


def dh1a(pack):
    """DH1a: each top-share series of the tail file in percent, latest year as the point with its range, and the history."""
    by = defaultdict(list)
    for r in pack.tables['wealth_tail']:
        if r['unit'] == 'pct_wealth':
            by[r['series']].append(r)
    out = {}
    for s, rows in by.items():
        rows.sort(key=lambda r: r['year'])
        out[s] = {'point': rows[-1]['value'], 'lo': rows[-1]['low'], 'hi': rows[-1]['high'], 'year': rows[-1]['year'],
                  'basis': rows[-1]['basis'], 'history': [(r['year'], r['value']) for r in rows]}
    return out


def dh1b(pack, groups=None, fiscal_year=None, basis=None):
    """DH1b: receipts as percent of GDP by line, and by the caller's groups ({group: [lines]}, each line in one group)."""
    have = _one(pack, fiscal_year, basis)
    flat = [x for g in (groups or {}).values() for x in g]
    if len(flat) != len(set(flat)) or [x for x in flat if x not in have]:
        raise PackError('dh1b: a line is in two groups, or a grouped line is not in the pack')
    return {'lines': dict(have), 'groups': {g: sum(have[x] for x in xs) for g, xs in (groups or {}).items()}}
