#!/usr/bin/env python3
"""Spoke gate checker (order.md 4.1 to 4.3, build item B17).

    python model/tools/check_gate.py --page <ID>     G1 to G5 for one page; exit 0 only if its needs are met
    python model/tools/check_gate.py --all           the table of order.md 4.2 for the 26 units; exit 0 only if all are open

The five checks (order.md 4.1):
    G1 model v3 complete and accepted     G2 data final (one run, marked final)
    G3 input judgement rows decided       G4 the page's own data is complete
    G5 tooling works (resolver, Data block, figures, checker)

Which checks a page needs is the PAGES table below (order.md 4.2), a data table, not prose. Everything the checks
run or read is named in Config, so a test can point the same code at a fixture repository (--root) and a stub command.
Read-only: the only side effects are the commands Config names (acceptance run, validator, pytest, fixture build).
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field, replace
from pathlib import Path

import yaml

ALL5 = ('G1', 'G2', 'G3', 'G4', 'G5')

# order.md 4.2. Page id -> checks it needs. A page that cites outputs (manifest `element:` or front matter `outputs:`)
# always falls under the first row ("a page whose front matter later lists an output falls under the first row").
_OUT = ALL5
_VAL = ('G3', 'G5')
_NONE = ('G5',)           # plus G3 when the page's front matter lists `inputs:`
PAGES = {
    'HUB': _OUT, 'MECH': _OUT, 'FISC': _OUT, 'PAY': _OUT, 'FUND': _OUT, 'CORP': _OUT, 'DECL': _OUT, 'BEHAV': _OUT,
    'WELF': _OUT, 'FIRST': _OUT, 'WIDER': _OUT, 'POL': _OUT, 'UNCER': _OUT, 'FALS': _OUT, 'HYPO': _OUT,
    'VAL': _VAL,
    'FAIR': _NONE, 'LIT': _NONE, 'GOV': _NONE, 'ATTR': _NONE, 'LIMIT': _NONE, 'ADOPT': _NONE, 'PILOT': _NONE,
    'ADD': _NONE, 'INST': _NONE, 'SCOPE': _NONE,
}
HUB_SECTION = re.compile(r'^H\d$')      # manifest `element:` entries H0..H7 belong to the hub page

# G5: build briefs that must be merged, as the files each puts on main (site.md section 8, Touches). "Merged" = present.
BRIEF_FILES = {
    'B2': ['model/tools/build_inputs.py', 'model/tools/build_metrics.py', 'model/tools/validate_outputs.py'],
    'B3': ['website/build/hooks.py', 'website/build/hook_format.py'],
    'B4': ['website/build/data_block.py', 'website/build/figure_data.py'],
    'B5': ['website/build/figures'],
    'B6': ['website/build/check_spokes.py', 'website/build/check_spokes_lists.py'],
    'B15': ['website/wdt-site-architecture.md', 'website/site/pages/draft.qmd'],
}
G5_TEST_DIRS = ['tests/model/data', 'tests/website/hooks', 'tests/data_block', 'tests/figures', 'tests/spokes']


@dataclass(frozen=True)
class Config:
    root: Path = Path(__file__).resolve().parent.parent.parent
    manifest: str = 'model-specs/outputs.yml'
    register_md: str = 'model-specs/inputs.md'
    decisions_md: str = 'model-specs/judgement-decisions.md'
    architecture: str = 'model-specs/architecture.md'
    acceptance: str = 'model-specs/acceptance.md'
    brief_011g: str = 'project/briefs/done/011g-model-v3-design.md'
    outputs_json: str = 'model_v3/OUTPUTS/outputs.json'
    inputs_json: str = 'data/input-register/inputs.json'
    pages_yml: str = 'website/registry/pages.yml'
    hooks_report: str = '_build/hooks-report.json'
    # flag names are B2's (brief 030c): --final, --fixture
    validator: tuple = (sys.executable, 'model/tools/validate_outputs.py', '--final', '{outputs_json}')
    # a spoke built under WDT_MODE=release; not defined until B15 wires the build, so G5 fails until it is set here
    fixture_build: tuple | None = None
    timeout: int = 3600


# ---------------------------------------------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------------------------------------------
Result = tuple   # (ok: bool, reason: str)


def ok(reason: str = '') -> Result:
    return True, reason


def fail(reason: str) -> Result:
    return False, reason


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def same_hash(recorded, actual: str) -> bool:
    return isinstance(recorded, str) and recorded.lower().removeprefix('sha256:') == actual


def run(cmd, cfg: Config, env_extra: dict | None = None) -> tuple:
    """Run a command in the repo root; returns (exit code or None, last output line)."""
    cmd = [str(c).format(outputs_json=cfg.outputs_json) for c in cmd]
    env = dict(os.environ, **(env_extra or {}))
    try:
        p = subprocess.run(cmd, cwd=cfg.root, capture_output=True, text=True, timeout=cfg.timeout, env=env)
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, f'{type(e).__name__}: {e}'
    tail = (p.stdout + p.stderr).strip().splitlines()
    return p.returncode, (tail[-1][:160] if tail else '')


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def table_rows(path: Path) -> list:
    """Markdown table rows whose first cell is a register id (I-...), as lists of stripped cells."""
    rows = []
    for line in path.read_text(encoding='utf-8').splitlines():
        if re.match(r'\|\s*I-', line):
            rows.append([c.strip() for c in line.strip().strip('|').split('|')])
    return rows


# ---------------------------------------------------------------------------------------------------------------
# G1  model v3 complete and accepted
# ---------------------------------------------------------------------------------------------------------------
ACCEPT_CMD = re.compile(r'^\s*(?:[-*]\s*)?(?:\*\*)?acceptance (?:command|run)(?:\*\*)?\s*:\s*`([^`]+)`', re.I)


def check_g1(cfg: Config) -> Result:
    missing = [f for f in (cfg.architecture, cfg.acceptance, cfg.brief_011g) if not (cfg.root / f).is_file()]
    if missing:
        return fail('missing: ' + ', '.join(missing))
    cmds = [m.group(1) for line in (cfg.root / cfg.acceptance).read_text(encoding='utf-8').splitlines()
            if (m := ACCEPT_CMD.match(line))]
    if len(cmds) != 1:
        return fail(f'{cfg.acceptance} names {len(cmds)} acceptance commands, not one (011g stage D is incomplete: '
                    'return it); expected a line "Acceptance command: `...`"')
    import shlex
    code, tail = run(shlex.split(cmds[0]), cfg)
    if code != 0:
        return fail(f'acceptance command `{cmds[0]}` exited {code}: {tail}')
    return ok(f'acceptance command `{cmds[0]}` exited 0')


# ---------------------------------------------------------------------------------------------------------------
# G2  data final
# ---------------------------------------------------------------------------------------------------------------
def check_g2(cfg: Config) -> Result:
    out = cfg.root / cfg.outputs_json
    if not out.is_file():
        return fail(f'{cfg.outputs_json} does not exist')
    try:
        data = load_json(out)
        run_ = data['run']
    except (ValueError, KeyError, TypeError) as e:
        return fail(f'{cfg.outputs_json} unreadable or has no run object ({type(e).__name__})')
    problems = []
    if run_.get('status') != 'final':
        problems.append(f'run.status is {run_.get("status")!r}, not final')
    if 'parts' in run_:   # 178c: a partial run (--parts) is a development file, never the release data
        problems.append(f'run.parts is {run_["parts"]!r}: a partial run is not the release run')
    if run_.get('fixture') is not False:
        problems.append(f'run.fixture is {run_.get("fixture")!r}, not false')
    manifest = cfg.root / cfg.manifest
    if not manifest.is_file():
        problems.append(f'{cfg.manifest} missing')
    else:
        version = load_yaml(manifest).get('version')
        if run_.get('manifest_version') != version:
            problems.append(f'run.manifest_version {run_.get("manifest_version")!r} != manifest version {version!r}')
        if not same_hash(run_.get('manifest_sha256'), sha256(manifest)):
            problems.append('run.manifest_sha256 differs from the hash of the manifest')
    inputs = cfg.root / cfg.inputs_json
    if not inputs.is_file():
        problems.append(f'{cfg.inputs_json} missing')
    elif not same_hash(run_.get('inputs_sha256'), sha256(inputs)):
        problems.append(f'run.inputs_sha256 differs from the hash of {cfg.inputs_json}')
    if problems:
        return fail('; '.join(problems))
    code, tail = run(cfg.validator, cfg)
    if code != 0:
        return fail(f'validator exited {code} in final mode: {tail}')
    return ok('run is final, hashes match, validator exit 0')


# ---------------------------------------------------------------------------------------------------------------
# G3  input judgement rows decided
# ---------------------------------------------------------------------------------------------------------------
DECIDED = re.compile(r'^(accepted|fixed at\s+\S.*|replaced by\s+I-\S+)$', re.I)
DATE = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def check_g3(cfg: Config) -> Result:
    reg, dec = cfg.root / cfg.register_md, cfg.root / cfg.decisions_md
    for f in (reg, dec):
        if not f.is_file():
            return fail(f'{f.relative_to(cfg.root)} missing')
    rows = table_rows(reg)
    ids = {r[0] for r in rows}
    flagged = {r[0] for r in rows if any('(J)' in c for c in r)}
    lines = {r[0]: r for r in table_rows(dec)}
    problems = []
    if flagged - set(lines):
        problems.append(f'{len(flagged - set(lines))} flagged rows have no line in the decisions file: '
                        + ', '.join(sorted(flagged - set(lines))[:5]))
    if set(lines) - flagged:
        problems.append(f'{len(set(lines) - flagged)} lines in the decisions file are not flagged (J): '
                        + ', '.join(sorted(set(lines) - flagged)[:5]))
    pending, bad, decided = [], [], 0
    for i in sorted(flagged & set(lines)):
        cells = lines[i]
        decision, date = (cells[-2], cells[-1]) if len(cells) >= 2 else ('', '')
        if decision.lower() == 'pending' or not decision:
            pending.append(i)
        elif not DECIDED.match(decision) or not DATE.match(date):
            bad.append(i)
        elif decision.lower().startswith('replaced by') and decision.split()[-1] not in ids:
            bad.append(i)
        else:
            decided += 1
    if pending:
        problems.append(f'{len(flagged)} flagged (J) rows, {len(pending)} pending, {decided} decided')
    if bad:
        problems.append(f'{len(bad)} decision lines are malformed (want accepted, fixed at <value> or replaced by '
                        '<row id>, with a date): ' + ', '.join(bad[:5]))
    if problems:
        return fail('; '.join(problems))
    return ok(f'{len(flagged)} flagged (J) rows, all decided')


# ---------------------------------------------------------------------------------------------------------------
# G4  the page's own data is complete (per page)
# ---------------------------------------------------------------------------------------------------------------
def page_outputs(manifest: dict, page: str) -> list:
    """Manifest outputs whose `element:` lists the page (the hub: any H0..H7)."""
    hit = (lambda e: bool(HUB_SECTION.match(e))) if page == 'HUB' else (lambda e: e == page)
    return [o for o in manifest['outputs'] if any(hit(e) for e in o.get('element', []))]


def page_front_matter(cfg: Config, page: str):
    """Front matter dict of the page source, or None if no source file is found."""
    cands = []
    pages = cfg.root / cfg.pages_yml
    if pages.is_file():
        data = load_yaml(pages) or {}
        rows = data.get('pages', data) if isinstance(data, dict) else data
        for r in rows if isinstance(rows, list) else rows.values():
            if isinstance(r, dict) and str(r.get('id', '')).upper() == page and r.get('source'):
                cands.append(cfg.root / r['source'])
    cands += [cfg.root / 'papers' / 'legacy' / f'{page.lower()}.md', cfg.root / 'papers' / 'legacy' / f'{page}.md']
    for c in cands:
        if c.is_file():
            m = re.match(r'---\s*\n(.*?)\n---\s*(\n|$)', c.read_text(encoding='utf-8'), re.S)
            return (yaml.safe_load(m.group(1)) or {}) if m else {}
    return None


def hook_id(x) -> str:
    m = re.fullmatch(r'\{\{\s*[io]:\s*([^}\s]+)\s*\}\}', str(x))
    return m.group(1) if m else str(x)


def register_ids(path: Path) -> set:
    d = load_json(path)
    if isinstance(d, dict) and 'inputs' in d:
        d = d['inputs']
    if isinstance(d, dict):
        return set(d)
    return {r['id'] for r in d if isinstance(r, dict) and 'id' in r}


NUMS = {'p10_mean_p90': ('p10', 'mean', 'p90'), 'point_and_range': ('point', 'lo', 'hi')}


def expected_cells(manifest: dict, o: dict):
    """The cell keys the manifest implies, or None when a `by` has no vocabulary to expand (B2's V7 owns that)."""
    horizons = o.get('horizons') or manifest['horizons']
    schedules = [None] if o.get('once_not_per_schedule') else manifest['schedules']
    by = o.get('by')
    if isinstance(by, list):
        return None
    dims = [(k, v) for k, v in (by or {}).items()]
    combos = itertools.product(schedules, horizons, *[[(k, x) for x in v] for k, v in dims])
    return {(s, h, tuple(sorted(rest))) for s, h, *rest in combos}


def check_outputs_complete(cfg: Config, manifest: dict, data: dict, o: dict) -> list:
    entry = data.get('outputs', {}).get(o['id'])
    if not entry or not entry.get('cells'):
        return [f'{o["id"]} has no cells in outputs.json']
    problems, seen = [], set()
    fields = NUMS.get(o['summary'], ())
    for c in entry['cells']:
        for f in fields:
            v = c.get(f)
            if not isinstance(v, (int, float)) or isinstance(v, bool):
                problems.append(f'{o["id"]} cell {c.get("schedule")}/{c.get("horizon")}/{c.get("by")} has {f}={v!r}')
                break
        seen.add((c.get('schedule'), c.get('horizon'), tuple(sorted((c.get('by') or {}).items()))))
    want = expected_cells(manifest, o)
    if want is not None:
        if o.get('once_not_per_schedule'):
            seen = {(None, h, b) for _, h, b in seen}
        gap = want - seen
        if gap:
            problems.append(f'{o["id"]} is missing {len(gap)} of {len(want)} cells')
    return problems[:3]


def check_g4(cfg: Config, page: str) -> Result:
    manifest_path = cfg.root / cfg.manifest
    if not manifest_path.is_file():
        return fail(f'{cfg.manifest} missing')
    manifest = load_yaml(manifest_path)
    outs = page_outputs(manifest, page)
    fm = page_front_matter(cfg, page)
    problems = []
    if fm is None:
        problems.append('no page source file (website/registry/pages.yml row or papers/legacy/<id>.md)')
        fm = {}
    fm_out = {hook_id(x) for x in fm.get('outputs') or []}
    el_out = {o['id'] for o in outs}
    if fm is not None and el_out != fm_out and not (fm == {} and not fm_out and not el_out):
        if el_out - fm_out:
            problems.append('R1: manifest lists the page for ' + ', '.join(sorted(el_out - fm_out)) +
                            ' but front matter `outputs:` does not')
        if fm_out - el_out:
            problems.append('R1: front matter `outputs:` names ' + ', '.join(sorted(fm_out - el_out)) +
                            ' but the manifest does not list this page in `element:`')
    if outs:
        out = cfg.root / cfg.outputs_json
        if not out.is_file():
            problems.append(f'{cfg.outputs_json} does not exist')
        else:
            try:
                data = load_json(out)
                for o in outs:
                    problems += check_outputs_complete(cfg, manifest, data, o)
            except (ValueError, KeyError, TypeError) as e:
                problems.append(f'{cfg.outputs_json} unreadable ({type(e).__name__})')
    want_in = [hook_id(x) for x in fm.get('inputs') or []]
    if want_in:
        reg = cfg.root / cfg.inputs_json
        if not reg.is_file():
            problems.append(f'{cfg.inputs_json} does not exist ({len(want_in)} inputs listed)')
        else:
            absent = sorted(set(want_in) - register_ids(reg))
            if absent:
                problems.append(f'{len(absent)} front matter inputs not in {cfg.inputs_json}: ' + ', '.join(absent[:5]))
    if problems:
        return fail('; '.join(problems))
    return ok(f'{len(outs)} outputs complete, {len(want_in)} inputs in the register, R1 both ways agree')


# ---------------------------------------------------------------------------------------------------------------
# G5  tooling works
# ---------------------------------------------------------------------------------------------------------------
def check_g5(cfg: Config) -> Result:
    problems = []
    for brief, files in BRIEF_FILES.items():
        gone = [f for f in files if not (cfg.root / f).exists()]
        if gone:
            problems.append(f'{brief} not merged (missing {", ".join(gone)})')
    gone = [d for d in G5_TEST_DIRS if not (cfg.root / d).is_dir()]
    if gone:
        problems.append('no test folder: ' + ', '.join(gone))
    elif not problems:
        code, tail = run([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', *G5_TEST_DIRS], cfg)
        if code != 0:
            problems.append(f'pytest {" ".join(G5_TEST_DIRS)} exited {code}: {tail}')
    if cfg.fixture_build is None:
        problems.append('no fixture-spoke release build is defined (set Config.fixture_build when B15 wires the build)')
    elif not problems:
        code, tail = run(cfg.fixture_build, cfg, {'WDT_MODE': 'release'})
        if code != 0:
            problems.append(f'fixture build under WDT_MODE=release exited {code}: {tail}')
        else:
            rep = cfg.root / cfg.hooks_report
            try:
                un = load_json(rep).get('unresolved')
                n = len(un) if isinstance(un, list) else un
                if n != 0:
                    problems.append(f'{cfg.hooks_report} shows {n!r} unresolved hooks')
            except (OSError, ValueError, AttributeError):
                problems.append(f'{cfg.hooks_report} missing or unreadable after the fixture build')
    if problems:
        return fail('; '.join(problems))
    return ok('briefs merged, tests pass, fixture spoke builds with zero unresolved hooks')


# ---------------------------------------------------------------------------------------------------------------
# per page and for all pages
# ---------------------------------------------------------------------------------------------------------------
def needs_of(cfg: Config, page: str, manifest: dict | None) -> tuple:
    """Checks the page needs (order.md 4.2), with escalation when the page cites outputs or lists inputs."""
    base = PAGES[page]
    if base == ALL5:
        return base
    cites = bool(manifest and page_outputs(manifest, page))
    fm = page_front_matter(cfg, page) or {}
    if cites or fm.get('outputs'):
        return ALL5
    return tuple(sorted(set(base) | ({'G3'} if fm.get('inputs') else set())))


def evaluate(cfg: Config, pages: list) -> dict:
    """{page: {'needs': (...), 'G1'..'G5': (ok, reason)}}; G1, G2, G3 and G5 are run once."""
    manifest_path = cfg.root / cfg.manifest
    manifest = load_yaml(manifest_path) if manifest_path.is_file() else None
    needs = {p: needs_of(cfg, p, manifest) for p in pages}
    used = set().union(*needs.values()) | set()
    glob = {}
    for g, fn in (('G1', check_g1), ('G2', check_g2), ('G3', check_g3), ('G5', check_g5)):
        glob[g] = fn(cfg)
    res = {}
    for p in pages:
        res[p] = {'needs': needs[p], **glob, 'G4': check_g4(cfg, p)}
    return res


def open_of(r: dict) -> bool:
    return all(r[g][0] for g in r['needs'])


def print_page(page: str, r: dict) -> None:
    print(f'page {page}: needs {", ".join(r["needs"])}')
    for g in ALL5:
        good, why = r[g]
        mark = 'pass' if good else 'FAIL'
        need = '' if g in r['needs'] else ' (not needed)'
        print(f'  {g} {mark}{need}: {why}')
    print(f'  => {"OPEN" if open_of(r) else "CLOSED"}')


def print_all(res: dict) -> None:
    print(f'{"page":<7}' + ''.join(f'{g:<6}' for g in ALL5) + 'gate')
    for p, r in res.items():
        cells = ''.join(f'{("pass" if r[g][0] else "FAIL") if g in r["needs"] else "-":<6}' for g in ALL5)
        print(f'{p:<7}{cells}{"OPEN" if open_of(r) else "CLOSED"}')
    n_open = sum(open_of(r) for r in res.values())
    print(f'\n{n_open} of {len(res)} pages open. "-" = check not needed by that page.\n')
    first = next(iter(res.values()))
    print('Failing checks')
    for g in ('G1', 'G2', 'G3', 'G5'):
        users = [p for p, r in res.items() if g in r['needs']]
        if not first[g][0] and users:
            print(f'  {g} FAIL ({len(users)} pages): {first[g][1]}')
    g4 = [(p, r['G4'][1]) for p, r in res.items() if 'G4' in r['needs'] and not r['G4'][0]]
    if g4:
        print(f'  G4 FAIL ({len(g4)} pages):')
        for p, why in g4:
            print(f'    {p}: {why}')


def main(argv=None, cfg: Config | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--page', metavar='ID', help='one of the 26 units (hub: HUB)')
    g.add_argument('--all', action='store_true', help='the order.md 4.2 table for all 26 units')
    ap.add_argument('--root', help='repository root (default: this repository)')
    a = ap.parse_args(argv)
    cfg = cfg or Config()
    if a.root:
        cfg = replace(cfg, root=Path(a.root).resolve())
    if a.all:
        res = evaluate(cfg, list(PAGES))
        print_all(res)
        return 0 if all(open_of(r) for r in res.values()) else 1
    page = a.page.upper()
    if page not in PAGES:
        print(f'unknown page {a.page!r}; the 26 units are: {", ".join(PAGES)}', file=sys.stderr)
        return 2
    res = evaluate(cfg, [page])
    print_page(page, res[page])
    return 0 if open_of(res[page]) else 1


if __name__ == '__main__':
    sys.exit(main())
