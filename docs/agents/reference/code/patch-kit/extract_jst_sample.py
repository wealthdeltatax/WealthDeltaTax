"""
extract_jst_sample.py -- cut a small test fixture out of the full JST file (lives in Model/test/)
==================================================================================================
The full JST Macrohistory JSON (jst_r6.json) is far too big to read or paste into a conversation. This script
writes a small file with the SAME structure, so the code under test (wdt_jst, rates_core, valgen_core) loads it
unchanged. A test then reads the fixture, never the original.

    python extract_jst_sample.py                              # GBR + USA, 1950-2017, only the series the code reads
    python extract_jst_sample.py --countries GBR PRT --years 1900 2017
    python extract_jst_sample.py --gap 1975                   # blank 1975 in the first country: a calendar gap, to exercise `contiguous`
    python extract_jst_sample.py --all-series                 # keep every series (bigger)
    python extract_jst_sample.py --keep hpnom --keep rev      # force extra series in

Structure it expects (as wdt_jst.py reads it):  J['countries'][ISO] = {'years': [...], 'series': {name: [value or null, ...]}},
each series aligned with `years`. Any other top-level or country-level keys are copied through untouched. If the file
looks different, the script stops and prints what it found instead of guessing.

WHICH SERIES: by default only series whose NAME appears as a quoted string in the project code (every .py outside test/ and
OUTPUTS/), plus wdt_jst's own four (capital_tr, cpi, gdp, pop). That is what the code can read. A series the code builds
dynamically from a computed name would be missed: the script prints the list it kept, and --keep adds more.

WHICH YEARS: real_basis_inputs needs the PRIOR year of cpi / gdp / pop, so the first year of your range is kept as context.
Note T = 100 (D7): a 68-year sample makes EVERY window repeat years (flagged `repeat`). That is fine for mechanics tests and
useless for numbers; do not quote results from the sample. For a test that needs non-repeating windows, use a short T in the
sandbox TOML.

OUTPUT: Model/test/fixtures/jst_sample.json by default, with a `_sample` block recording where it came from, so nobody mistakes it
for the real data. The size and an approximate token count are printed.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tomllib
from pathlib import Path

ALWAYS = ('capital_tr', 'cpi', 'gdp', 'pop')          # wdt_jst.real_basis_inputs / real_return_series
SKIP_DIRS = {'test', 'tests', 'OUTPUTS', '__pycache__', '.git', '.venv', 'venv', '_backups', 'fixtures'}


def find_root(start: Path) -> Path:
    for d in [start, *start.parents]:
        if (d / 'WDT_Params.toml').exists():
            return d
    raise SystemExit(f'no WDT_Params.toml above {start}; run this from Model/test or pass --root')


def find_source(root: Path, explicit: str | None) -> Path:
    """The full JST file: --src, else the name in [rates].jst_path looked up where wdt_jst looks (RATES/, root, root's parent)."""
    if explicit:
        p = Path(explicit)
        if not p.exists():
            raise SystemExit(f'--src {p} does not exist')
        return p
    try:
        name = tomllib.loads((root / 'WDT_Params.toml').read_text(encoding='utf-8'))['rates']['jst_path']
    except Exception:                                                  # noqa: BLE001
        name = 'jst_r6.json'
    tried = [root / 'RATES' / name, root / name, root.parent / name]
    for p in tried:
        if p.exists():
            return p
    raise SystemExit(f'JST file {name!r} not found; tried {[str(t) for t in tried]}. Pass --src.')


def code_strings(root: Path) -> set[str]:
    """Every quoted string literal in the project's .py files (single or double quotes, no spaces): candidate series names."""
    pat = re.compile(r"""['"]([A-Za-z_][A-Za-z0-9_]*)['"]""")
    found: set[str] = set()
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            if fn.endswith('.py'):
                try:
                    found.update(pat.findall(Path(dp, fn).read_text(encoding='utf-8', errors='replace')))
                except OSError:
                    pass
    return found


def describe(J) -> str:
    if not isinstance(J, dict):
        return f'top level is a {type(J).__name__}, expected an object'
    ks = list(J)[:8]
    c = J.get('countries')
    if not isinstance(c, dict) or not c:
        return f"no 'countries' object; top-level keys: {ks}"
    iso = next(iter(c))
    v = c[iso]
    return f"countries[{iso!r}] has keys {list(v)[:8] if isinstance(v, dict) else type(v).__name__}"


def extract(J, countries, lo, hi, keep_series, all_series, gap):
    if 'countries' not in J or not isinstance(J['countries'], dict):
        raise SystemExit('unexpected JST structure: ' + describe(J))
    out = {k: v for k, v in J.items() if k != 'countries'}
    out['countries'] = {}
    kept_names: set[str] = set()
    for iso in countries:
        if iso not in J['countries']:
            raise SystemExit(f'country {iso} not in the JST file; available: {sorted(J["countries"])}')
        c = J['countries'][iso]
        if not (isinstance(c, dict) and 'years' in c and isinstance(c.get('series'), dict)):
            raise SystemExit('unexpected JST structure: ' + describe(J))
        years = [int(y) for y in c['years']]
        idx = [i for i, y in enumerate(years) if lo <= y <= hi]
        if not idx:
            raise SystemExit(f'{iso}: no years in {lo}-{hi}; the file has {min(years)}-{max(years)}')
        new = {k: v for k, v in c.items() if k not in ('years', 'series')}
        new['years'] = [years[i] for i in idx]
        new['series'] = {}
        for name, vals in c['series'].items():
            if not all_series and name not in keep_series:
                continue
            if isinstance(vals, list) and len(vals) == len(years):
                new['series'][name] = [vals[i] for i in idx]
            else:
                new['series'][name] = vals
            kept_names.add(name)
        if gap is not None and iso == countries[0] and gap in new['years']:
            g = new['years'].index(gap)
            for vals in new['series'].values():
                if isinstance(vals, list) and len(vals) == len(new['years']):
                    vals[g] = None
        out['countries'][iso] = new
    return out, kept_names


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description='Extract a small JST test fixture.')
    ap.add_argument('--root', default=None, help='model folder (default: found by walking up to WDT_Params.toml)')
    ap.add_argument('--src', default=None, help='full JST json (default: [rates].jst_path)')
    ap.add_argument('--countries', nargs='+', default=['GBR', 'USA'])
    ap.add_argument('--years', nargs=2, type=int, default=[1950, 2017], metavar=('FIRST', 'LAST'))
    ap.add_argument('--keep', action='append', default=[], help='extra series name to keep (repeatable)')
    ap.add_argument('--all-series', action='store_true', help='keep every series (bigger file)')
    ap.add_argument('--gap', type=int, default=None, help='blank this year in the first country (creates a calendar gap)')
    ap.add_argument('--out', default=None, help='default: <root>/test/fixtures/jst_sample.json')
    a = ap.parse_args(argv)

    root = Path(a.root).resolve() if a.root else find_root(Path(__file__).resolve().parent)
    src = find_source(root, a.src)
    with open(src, 'r', encoding='utf-8') as fh:
        J = json.load(fh)
    available = set()
    for c in (J.get('countries') or {}).values():
        if isinstance(c, dict) and isinstance(c.get('series'), dict):
            available |= set(c['series'])
    if not available:
        raise SystemExit('unexpected JST structure: ' + describe(J))

    wanted = (set(ALWAYS) | code_strings(root) | set(a.keep)) & available
    missing_always = [s for s in ALWAYS if s not in available]
    if missing_always:
        print(f'WARNING: wdt_jst reads {missing_always} but the file has no such series; check the file version')
    sample, kept = extract(J, a.countries, a.years[0], a.years[1], wanted, a.all_series, a.gap)
    sample['_sample'] = {'source': src.name, 'countries': a.countries, 'years': a.years, 'gap_year': a.gap,
                         'series_filter': 'all' if a.all_series else 'quoted in project code + ' + ', '.join(ALWAYS),
                         'note': 'TEST FIXTURE. Mechanics only: do not quote numbers computed from it.'}
    out = Path(a.out) if a.out else root / 'test' / 'fixtures' / 'jst_sample.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(sample, separators=(',', ':'), allow_nan=False)
    out.write_text(text, encoding='utf-8')
    print(f'source   {src}  ({src.stat().st_size / 1e6:.1f} MB)')
    print(f'wrote    {out}  ({len(text) / 1e3:.0f} kB, about {len(text) // 4:,} tokens)')
    print(f'countries {a.countries}   years {a.years[0]}-{a.years[1]}' + (f'   gap {a.gap} in {a.countries[0]}' if a.gap else ''))
    print(f'series kept ({len(kept)}): {sorted(kept)}')
    if len(text) > 400_000:
        print('NOTE: over 400 kB. Fewer countries, a shorter range or fewer series keeps it readable.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
