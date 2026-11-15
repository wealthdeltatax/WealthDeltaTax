#!/usr/bin/env python3
"""
wire_jst_loop.py -- wires wdt_jst.loop_windows into rates_core.py (refactor Phase 1 item 1, D1b).

Usage
  python wire_jst_loop.py MODEL_DIR --check     report only
  python wire_jst_loop.py MODEL_DIR             apply (backup rates_core.py.pre_jst.bak; CRLF kept)
  optional: --rates PATH   if rates_core.py is found more than once

What changes in rates_core.py
  * imports loop_windows / usable_years from wdt_jst (wdt_jst.py sits in the model root).
  * sweep(): windows are the full wrapped loop (D1b). Windows containing a flagged year are dropped when
    exclude_flagged is on (same rule as before). Every row carries wraps / repeat / contiguous.
  * build_scenario() / run_window() take the window's calendar years, not start + T.
  * levy_base_median() (the CORP levy calibration sample) uses the same loop, so VAL and RATES read one
    window rule. This moves the calibrated levy rate slightly: expected, and it should be read.
  * run_scenario() adds headline_contiguous: the same headline on contiguous windows only (the second report).
valid_windows() is left in place but no longer called.
"""
import sys
from pathlib import Path

OLD_NEW = [
    ("import wdt_jst",
     "import wdt_core as wc\nfrom wdt_fmt import ensure_dir, out_dir, today_iso\n",
     "import wdt_core as wc\nfrom wdt_fmt import ensure_dir, out_dir, today_iso\n"
     "from wdt_jst import loop_windows, usable_years      # D1b: one window rule for VAL and RATES\n"),
    ("levy_base_median: loop windows",
     "            for s0 in valid_windows(d, cols, T):\n"
     "                sub = d.reindex(range(s0, s0 + T))\n",
     "            for w in loop_windows(usable_years(d, cols), T, wrap=True):\n"
     "                sub = d.reindex(w['years'])\n"),
    ("build_scenario: signature takes the window years",
     "def build_scenario(J, iso, start, T, basis, index_mode, c):\n",
     "def build_scenario(J, iso, years, basis, index_mode, c):\n"),
    ("build_scenario: years in window order (repeats and seam allowed)",
     "    yrs = list(range(start, start + T))\n    sub = d.reindex(yrs)\n",
     "    yrs = list(years)\n    T = len(yrs)\n    start = yrs[0]\n    sub = d.reindex(yrs)\n"),
    ("run_window: takes a loop window",
     "def run_window(J, iso, start, mode, cfg, cal, p, flags=None):\n"
     '    """One (country, start year, index mode) window -> one flat result row (dict)."""\n'
     "    rp = p['rates']\n"
     "    scn = build_scenario(J, iso, start, cfg['T'], cfg['basis'], mode, cfg['c'])\n",
     "def run_window(J, iso, win, mode, cfg, cal, p, flags=None):\n"
     '    """One (country, loop window, index mode) -> one flat result row (dict). `win` is a wdt_jst loop window."""\n'
     "    rp = p['rates']\n"
     "    start = win['start']\n"
     "    scn = build_scenario(J, iso, win['years'], cfg['basis'], mode, cfg['c'])\n"),
    ("run_window: stationary consumption rebuilds on the same years",
     "        scn = build_scenario(J, iso, start, cfg['T'], cfg['basis'], mode, c_used)\n",
     "        scn = build_scenario(J, iso, win['years'], cfg['basis'], mode, c_used)\n"),
    ("run_window: flagged from the window's years",
     "        yrs = set(range(start, start + cfg['T']))\n"
     "        flagged = bool(flags.loc[flags.index.isin(yrs)].any())\n",
     "        flagged = bool(any(flags.get(y, False) for y in win['years']))\n"),
    ("run_window: report the window's loop flags",
     "        'iso': iso, 'start': start, 'mode': mode, 'era': _era(start, rp['eras']),\n",
     "        'iso': iso, 'start': start, 'mode': mode, 'era': _era(start, rp['eras']),\n"
     "        'wraps': win['wraps'], 'repeat': win['repeat'], 'contiguous': win['contiguous'],\n"),
    ("sweep: full loop, flagged-year windows dropped when excluded",
     "        starts = valid_windows(d, cols, cfg['T'], exclude=fl if cfg['exclude_flagged'] else None)\n"
     "        for s in starts[::cfg['start_stride']]:\n"
     "            for mode in cfg['index_modes']:\n"
     "                rows.append(run_window(J, iso, s, mode, cfg, cal, p, flags=fl))\n",
     "        wins = loop_windows(usable_years(d, cols), cfg['T'], wrap=True)     # D1b; `contiguous` marks the second report\n"
     "        if cfg['exclude_flagged']:\n"
     "            wins = [w for w in wins if not any(fl.get(y, False) for y in w['years'])]\n"
     "        for w in wins[::cfg['start_stride']]:\n"
     "            for mode in cfg['index_modes']:\n"
     "                rows.append(run_window(J, iso, w, mode, cfg, cal, p, flags=fl))\n"),
    ("run_scenario: contiguous-only headline as the second report",
     "        'headline': headline(df, p, boot=name in p['rates']['representativeness']['bootstrap_scenarios']),\n",
     "        'headline': headline(df, p, boot=name in p['rates']['representativeness']['bootstrap_scenarios']),\n"
     "        'headline_contiguous': headline(df[df['contiguous']], p, boot=False),\n"),
]


def patch_text(text, patches, name):
    """Exact-match replacement, each OLD once. Skips an edit whose NEW is already present (old-in-new safe)."""
    log = []
    for label, old, new in patches:
        n_old = text.count(old)
        if old in new and new in text:
            log.append(f"  skip  {label} (already applied)")
            continue
        if old not in new and n_old == 0 and new in text:
            log.append(f"  skip  {label} (already applied)")
            continue
        if n_old != 1:
            raise RuntimeError(f"{name}: '{label}': OLD snippet found {n_old} times (need exactly 1)")
        text = text.replace(old, new, 1)
        log.append(f"  apply {label}")
    return text, log


def locate(root, fname, override=None):
    if override:
        return Path(override)
    hits = [p for p in root.rglob(fname)
            if '.pre_' not in p.name and 'OUTPUTS' not in p.parts and '__pycache__' not in p.parts]
    if len(hits) != 1:
        raise RuntimeError(f"{fname}: found {len(hits)} copies under {root}; pass --rates PATH")
    return hits[0]


def main(argv):
    if len(argv) < 2 or argv[1].startswith('--'):
        print(__doc__)
        return 2
    args = argv[2:]
    check_only = '--check' in args
    override = args[args.index('--rates') + 1] if '--rates' in args else None
    try:
        path = locate(Path(argv[1]), 'rates_core.py', override)
    except RuntimeError as e:
        print(f"ABORT {e}")
        return 1
    raw = path.read_bytes().decode('utf-8')
    crlf = '\r\n' in raw
    text = raw.replace('\r\n', '\n')
    try:
        new_text, log = patch_text(text, OLD_NEW, path.name)
    except RuntimeError as e:
        print(f"ABORT {e}")
        return 1
    print(f"{path} ({'CRLF' if crlf else 'LF'}):")
    print('\n'.join(log))
    if check_only or new_text == text:
        print('check only: nothing written' if check_only else 'nothing to do')
        return 0
    out = new_text.replace('\n', '\r\n') if crlf else new_text
    compile(out, str(path), 'exec')            # syntax check before anything is written
    bak = path.with_name(path.name + '.pre_jst.bak')
    if not bak.exists():
        bak.write_bytes(path.read_bytes())
    path.write_bytes(out.encode('utf-8'))
    print(f"  wrote {path} (backup {bak.name}); syntax OK")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
