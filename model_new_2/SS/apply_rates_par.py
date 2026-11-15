"""
apply_rates_par.py -- patch rates_core.py to run the window sweep in parallel (wdt_par)
=====================================================================================
Run from Model/ (next to wdt_par.py; rates_core.py is in Model/RATES/ or beside this file):

    python apply_rates_par.py            apply
    python apply_rates_par.py --check    only check that every anchor is found exactly once

NO NUMBERS CHANGE. The patch does two things, in this order of risk:
  PAR-1  hoists work that was repeated for every window and depends only on the scenario or the country:
           panel(J, iso) + flag_years (was: twice or more per window) and resolve_rule. (_route_plan / _verification are
           already cached per scenario by _plan_ver, an earlier patch; the sweep now primes that cache in the parent so the
           workers receive it inside cal.)
           run_window / build_scenario keep their signatures (new optional keyword arguments only), so any
           other caller is unchanged.
  PAR-2  sweep() builds the flat list of (country, window, index mode) jobs and, if given a wdt_par.WorkerPool,
         runs them in chunks in worker processes; rows come back in the original order. main() gains
         --workers N (default: cores - 1; 1 = the serial path, no processes).

Behaviour that is NOT identical, by design:
  * _plan_ver / resolve_rule now run at the start of the sweep, so a bad route or verification setting raises there even in a
    scenario that happens to have zero windows (before: only at the first window).
  * With workers > 1 the progress / warning prints from inside a window (the non-finite warning in run_lines) come
    from the worker processes, interleaved.

Safety: every edit is an exact-text anchor that must occur exactly once, in the file's own line endings (CRLF is
preserved). Nothing is written unless all anchors match. The original is kept as rates_core.py.pre_par.bak.
Idempotent: refuses to run twice.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGETS = [HERE / 'RATES' / 'rates_core.py', HERE / 'rates_core.py']
MARK = 'import wdt_par as wpar'

# ─────────────────────────────────────────────────────────────────────────────
# the edits: (name, old, new) exact replacements, and (name, start, end, new) region replacements
# ─────────────────────────────────────────────────────────────────────────────

EXACT = [
    ('doc: CLI',
     "  python rates_core.py --fresh            discard the existing JSON first\n\"\"\"",
     "  python rates_core.py --fresh            discard the existing JSON first\n"
     "  python rates_core.py --workers 8        worker processes for the window sweep (default: cores - 1; 1 = serial, no processes)\n"
     "\n"
     "PARALLEL SWEEP (wdt_par)\n"
     "  The windows of one scenario are independent, so sweep() runs them in chunks in worker processes and puts the rows back in the\n"
     "  original order: the JSON is identical to the serial run (apart from meta.generated and meta.elapsed_s), whatever --workers is.\n"
     "  Stays serial in the parent: calibration, the levy calibration, headline, the bootstrap, the JSON.\n"
     "\"\"\""),

    ('import wdt_par',
     "from wdt_fmt import ensure_dir, out_dir, today_iso",
     "import wdt_par as wpar                                       # PAR: ordered process pool for the window sweep\n"
     "from wdt_fmt import ensure_dir, out_dir, today_iso"),

    ('build_scenario: optional panel',
     "def build_scenario(J, iso, years, basis, index_mode, c):",
     "def build_scenario(J, iso, years, basis, index_mode, c, d=None):"),

    ('build_scenario: use it',
     "    d = panel(J, iso)\n    yrs = list(years)",
     "    d = panel(J, iso) if d is None else d                  # PAR: a caller that already holds the country's panel passes it\n    yrs = list(years)"),

    ('run_window: signature',
     "def run_window(J, iso, win, mode, cfg, cal, p, flags=None):",
     "def run_window(J, iso, win, mode, cfg, cal, p, flags=None, pre=None):"),

    ('run_window: panel and flags from pre',
     "    rp = p['rates']\n    start = win['start']\n    scn = build_scenario(J, iso, win['years'], cfg['basis'], mode, cfg['c'])",
     "    rp = p['rates']\n    start = win['start']\n"
     "    d = None\n"
     "    if pre is not None:                      # PAR: per-sweep constants and the cached country panel (same values, computed once)\n"
     "        d, fl_ = _panel_fl(pre, J, iso, rp)\n"
     "        flags = fl_ if flags is None else flags\n"
     "    scn = build_scenario(J, iso, win['years'], cfg['basis'], mode, cfg['c'], d=d)"),

    ('run_window: stationary rebuild',
     "        scn = build_scenario(J, iso, win['years'], cfg['basis'], mode, c_used)",
     "        scn = build_scenario(J, iso, win['years'], cfg['basis'], mode, c_used, d=d)"),

    ('run_window: c_cap',
     "c_cap=wc.resolve_rule(p, cfg['rule_set'])['c_cap'],",
     "c_cap=(pre['c_cap'] if pre is not None else wc.resolve_rule(p, cfg['rule_set'])['c_cap']),"),

    ('run_scenario: signature',
     "def run_scenario(J, p, name, stride=None, countries_=None, verbose=True):",
     "def run_scenario(J, p, name, stride=None, countries_=None, verbose=True, pool=None):"),

    ('run_scenario: sweep',
     "    df, cal = sweep(J, cfg, p)\n",
     "    df, cal = sweep(J, cfg, p, pool=pool)\n"),

    ('main: --workers',
     "    ap.add_argument('--toml', default=None, help='alternative parameter file')",
     "    ap.add_argument('--toml', default=None, help='alternative parameter file')\n"
     "    ap.add_argument('--workers', type=int, default=None,\n"
     "                    help='worker processes for the window sweep (default: cores - 1; 1 = serial, no processes)')"),

    ('main: pool around the scenario loop',
     "    for n in names:\n        data['scenarios'][n] = run_scenario(J, p, n, a.stride, a.countries)\n",
     "    workers = wpar.resolve_workers(a.workers)\n"
     "    print(f'  window sweep: {workers} worker process(es)' if workers > 1 else '  window sweep: serial', flush=True)\n"
     "    with wpar.WorkerPool(workers, initializer=_w_init, initargs=(J, p), tag=_pool_tag(J, p)) as pool:\n"
     "        for n in names:\n"
     "            data['scenarios'][n] = run_scenario(J, p, n, a.stride, a.countries, pool=pool)\n"),
]

SWEEP_NEW = '''# ── PAR: per-sweep constants, worker side, and the sweep itself ──────────────────────────────────────────────────────────────────────
# run_window used to recompute, for EVERY window, things that depend only on the scenario (the rule set; _route_plan and _verification
# are already cached in cal by _plan_ver) or on the country (panel, flag_years). _sweep_ctx holds the first, pre['panels'] the second. The values are the
# same objects the old code rebuilt each time, so the rows are bit-identical. Workers do the same on their side (_w_run).

def _sweep_ctx(cfg, cal, p):
    """Constants of one sweep, for run_window(pre=...): the Route C refund cap and the panel cache. Also primes the route plan / verification cache in cal."""
    _plan_ver(cfg, cal, p)             # primes cal['_plan_ver'] (route plan cell + verification); it travels to the workers inside cal
    return {'c_cap': wc.resolve_rule(p, cfg['rule_set'])['c_cap'], 'panels': {}}


def _panel_fl(pre, J, iso, rp):
    """(panel, suspect-year flags) of one country, built once per sweep (per worker process in a pool)."""
    pn = pre['panels']
    if iso not in pn:
        d = panel(J, iso)
        pn[iso] = (d, flag_years(d, rp['flags'])['any'])
    return pn[iso]


def _pool_tag(J, p):
    """Identity of the inputs a pool was started with (J and p are sent to the workers once, at start-up)."""
    return (id(J), hashlib.md5(json.dumps(wc.json_safe(p), sort_keys=True).encode()).hexdigest())


_W = {}                               # worker-process state: J, p, the panel cache, and the current sweep's constants
_SWEEP_SEQ = itertools.count(1)       # parent side: a token per sweep, so a worker rebuilds _sweep_ctx once per sweep, not per chunk


def _w_init(J, p):
    """Pool initializer: runs once in each worker."""
    _W.clear()
    _W.update(J=J, p=p, panels={}, tok=None, pre=None)


def _w_run(task):
    """One chunk of jobs [(iso, window, mode), ...] -> list of rows, in order. ctx = (sweep token, cfg, cal)."""
    (tok, cfg, cal), jobs = task
    if _W['tok'] != tok:
        pre = _sweep_ctx(cfg, cal, _W['p'])
        pre['panels'] = _W['panels']
        _W['tok'], _W['pre'] = tok, pre
    J, p, pre = _W['J'], _W['p'], _W['pre']
    return [run_window(J, iso, w, mode, cfg, cal, p, pre=pre) for iso, w, mode in jobs]


def sweep(J, cfg, p, cal=None, pool=None):
    """
    Run every valid (country, start year, index mode) window. Returns (DataFrame, cal).
    pool: a started wdt_par.WorkerPool built with initargs (J, p) -> the windows run in worker processes (rows in the original
    order, numbers identical); None, or a pool with workers == 1 -> the serial path in this process.
    """
    rp = p['rates']
    cal = calibration(J, cfg, p) if cal is None else cal
    isos = cfg['countries'] or countries(J)
    cols = (MODEL_COLS + (['eq_capgain', 'gdpg'] if cfg['levy'] else [])
            + ([('hpg_real' if cfg['basis'] == 'real' else 'hpg')] if 'house' in cfg['index_modes'] else []))
    pre = _sweep_ctx(cfg, cal, p)
    jobs = []
    for iso in isos:
        d, fl = _panel_fl(pre, J, iso, rp)
        wins = loop_windows(usable_years(d, cols), cfg['T'], wrap=True)     # D1b; `contiguous` marks the second report
        if cfg['exclude_flagged']:
            wins = [w for w in wins if not any(fl.get(y, False) for y in w['years'])]
        for w in wins[::cfg['start_stride']]:
            for mode in cfg['index_modes']:
                jobs.append((iso, w, mode))
    if pool is not None and pool.parallel and len(jobs) > 1:
        if pool.tag != _pool_tag(J, p):
            raise ValueError('sweep: the worker pool was started with a different J / p than this sweep uses; '
                             'start a pool per (J, p): WorkerPool(..., initializer=_w_init, initargs=(J, p), tag=_pool_tag(J, p))')
        rows = pool.map_chunks(_w_run, jobs, (next(_SWEEP_SEQ), cfg, cal))
    else:
        rows = [run_window(J, iso, w, mode, cfg, cal, p, pre=pre) for iso, w, mode in jobs]
    return pd.DataFrame(rows), cal
'''

REGION = ('sweep()',
          'def sweep(J, cfg, p, cal=None):',
          '\n\n\n# ── summaries ',
          SWEEP_NEW)


def _find_target():
    for t in TARGETS:
        if t.exists():
            return t
    raise SystemExit(f'rates_core.py not found; looked in {[str(t) for t in TARGETS]}')


def build(src):
    """Return the patched source, or raise SystemExit naming the anchor that failed."""
    eol = '\r\n' if '\r\n' in src else '\n'
    cv = lambda s: s.replace('\r\n', '\n').replace('\n', eol)
    out = src
    for name, old, new in EXACT:
        n = out.count(cv(old))
        if n != 1:
            raise SystemExit(f'anchor {name!r}: found {n} times (need exactly 1). Nothing written.')
        out = out.replace(cv(old), cv(new))
    name, start, end, new = REGION
    if out.count(cv(start)) != 1:
        raise SystemExit(f'anchor {name!r} start: found {out.count(cv(start))} times (need exactly 1). Nothing written.')
    i = out.index(cv(start))
    j = out.find(cv(end), i)
    if j < 0 or out.count(cv(end)) != 1:
        raise SystemExit(f'anchor {name!r} end marker not found exactly once. Nothing written.')
    old_body = out[i:j]
    for must in ('rows.append(run_window(', 'flag_years(d, rp[', 'return pd.DataFrame(rows), cal'):
        if must not in old_body:
            raise SystemExit(f'the old sweep() does not look as expected (missing {must!r}). Nothing written.')
    out = out[:i] + cv(new).rstrip(eol) + out[j:]
    return out


def main(argv):
    path = _find_target()
    with open(path, 'r', encoding='utf-8', newline='') as fh:     # newline='' keeps CRLF (Path.read_text has no newline= before 3.13)
        src = fh.read()
    if MARK in src:
        raise SystemExit(f'{path.name} already carries the PAR patch ({MARK!r} found). Nothing to do.')
    if not (HERE / 'wdt_par.py').exists():
        raise SystemExit('wdt_par.py must sit next to this script (Model/). Copy it first.')
    new = build(src)
    compile(new, str(path), 'exec')                 # syntax check before anything is written
    if '--check' in argv:
        print(f'OK: all anchors found once in {path}; patched source compiles. Nothing written.')
        return
    bak = path.with_name(path.name + '.pre_par.bak')
    with open(bak, 'w', encoding='utf-8', newline='') as fh:
        fh.write(src)
    with open(path, 'w', encoding='utf-8', newline='') as fh:
        fh.write(new)
    print(f'Patched {path}\nBackup  {bak}\nNext: python test/test_rates_par.py   (parity: serial vs parallel, bit-identical)')


if __name__ == '__main__':
    main(sys.argv[1:])
