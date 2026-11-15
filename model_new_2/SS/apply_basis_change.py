#!/usr/bin/env python3
"""
apply_basis_change.py -- applies the post-settlement basis (claude/BASIS_CHANGE.md, option 1)
to wdt_core.py, valgen_core.py and rates_core.py by exact string replacement.

Usage
  python apply_basis_change.py MODEL_DIR            apply; originals kept as <file>.pre_basis.bak
  python apply_basis_change.py MODEL_DIR --check    report only, write nothing
  optional: --core PATH  --valgen PATH  --rates PATH   if a name is found more than once

File layout: wdt_core.py is in MODEL_DIR. valgen_core.py and rates_core.py are one folder down
(each imports the model root as parent.parent), so they are located by a search under MODEL_DIR.

Rules
  * Each OLD snippet must occur exactly once in its file (line endings normalised to LF for the
    match, then restored: rates_core.py is CRLF). Otherwise the script stops before writing that file.
  * A snippet whose NEW text is already present is skipped, so a re-run is safe.
  * Functional edits only. Docstrings are not touched.
  * After writing, each file is compiled (no .pyc written) as a syntax check.

What is NOT done here (see BASIS_CHANGE.md section 4): the validator fixtures in valgen_core
(gated by BASIS_CONVENTION, which this script adds to the import line) and the c7 rewrite are part of
this patch; the numerical threshold checks in the validators have not been re-run.
"""
import sys
from pathlib import Path

WDT_CORE = [
    ("add BASIS_CONVENTION constant",
     "_DEFAULT_TOML = Path(__file__).parent / 'WDT_Params.toml'\n",
     "_DEFAULT_TOML = Path(__file__).parent / 'WDT_Params.toml'\n\n"
     "# Basis convention of the holding-period and settlement mechanics (BASIS_CHANGE.md).\n"
     "BASIS_CONVENTION = 'post'\n"),
    ("settle_tw_flows: initial basis = post-sale cash",
     "    basis = sell_result['W_sell']\n",
     "    basis = sell_result['TW']              # post-sale basis = post-sale cash (BASIS_CHANGE)\n"),
    ("settle_tw_flows: basis moves after the payment",
     "        basis = cash\n        cash  = cash - L\n        cum  += L\n",
     "        cash  = cash - L\n        basis = cash                       # BASIS_CHANGE\n        cum  += L\n"),
    ("simulate: record and state carry the post-surrender value",
     "        cum  += L\n        W     = W_new\n        records.append({\n            't': t, 'V': V, 'W': W_new, 'f': f, 'cum': cum,\n",
     "        cum  += L\n        W     = f * alpha * V                    # POST-surrender basis (BASIS_CHANGE)\n"
     "        records.append({\n            't': t, 'V': V, 'W': W, 'f': f, 'cum': cum,\n"),
    ("simulate_declared: same change on the declared value",
     "        W     = W_new\n        a_t   = D[t - 1] / V\n        records.append({'t': t, 'V': V, 'W': W_new, 'f': f, 'cum': cum, 'L': L,\n",
     "        W     = f * D[t - 1]                     # POST-surrender basis (BASIS_CHANGE)\n"
     "        a_t   = D[t - 1] / V\n        records.append({'t': t, 'V': V, 'W': W, 'f': f, 'cum': cum, 'L': L,\n"),
]

VALGEN_CORE = [
    ("import BASIS_CONVENTION",
     "from wdt_core import load_params, tau, simulate, run_pair, run_sim_hist, settle_tw_flows, rate_params, with_rate_scenario, with_val_basis\n",
     "from wdt_core import load_params, tau, simulate, run_pair, run_sim_hist, settle_tw_flows, rate_params, with_rate_scenario, with_val_basis, BASIS_CONVENTION\n"),
    ("plan fixtures gated off on the post basis",
     '    """True when the parameters the fixtures depend on equal the baseline (all of them, or just `keys`)."""\n',
     '    """True when the parameters the fixtures depend on equal the baseline (all of them, or just `keys`)."""\n'
     "    if BASIS_CONVENTION == 'post':\n"
     "        return False                      # plan fixtures are on the pre-settlement basis (BASIS_CHANGE); re-derive before use\n"),
    ("_holding_year: post-surrender basis",
     "    q, paid = _pay_in_kind(led, t, 'tax_inkind', st, V, L, q)\n    st['W'] = W_new\n",
     "    q, paid = _pay_in_kind(led, t, 'tax_inkind', st, V, L, q)\n"
     "    W_new = st['f'] * alpha * V                  # POST-surrender basis (BASIS_CHANGE)\n"
     "    st['W'] = W_new\n"),
    ("_heir_arrival: post-heir-tax basis",
     "    _, paid = _pay_in_kind(led, t, 'tax_heir', st, V, L, q)\n    st['W'] = W_new\n",
     "    _, paid = _pay_in_kind(led, t, 'tax_heir', st, V, L, q)\n"
     "    st['W'] = st['f'] * alpha * V                # POST-heir-tax basis (BASIS_CHANGE)\n"),
    ("run_life: settlement basis = post-sale cash",
     "    cash, basis, i = tw_naive, W_sell, 0\n",
     "    cash, basis, i = tw_naive, tw_naive, 0      # post-sale basis = post-sale cash (BASIS_CHANGE)\n"),
    ("run_life: basis moves after the payment",
     "        basis = cash\n        cash -= L\n        cum  += L\n        i    += 1\n",
     "        cash -= L\n        basis = cash\n        cum  += L\n        i    += 1\n"),
    ("run_family3: year-end basis after settlement, re-base D on reset",
     "        for r in routes:\n            S['R'][r]['Wp'] = Wn[r]\n            S['R'][r]['ppu'] = S['R'][r]['dd']\n"
     "        if reset_year:\n            S['last_reset'] = t\n            _settle_D(led, t, S, 'reset_D', receipts)\n",
     "        for r in routes:                         # POST-settlement basis (BASIS_CHANGE)\n"
     "            S['R'][r]['Wp'] = S['R'][r]['f'] * S['R'][r]['dd']\n"
     "            S['R'][r]['ppu'] = S['R'][r]['dd']\n"
     "        if reset_year:\n            S['last_reset'] = t\n            _settle_D(led, t, S, 'reset_D', receipts)\n"
     "            if 'D' in S['R']:                    # a reset sells units: re-base Route D\n"
     "                S['R']['D']['Wp'] = S['R']['D']['f'] * S['R']['D']['dd']\n"),
    ("run_family3: death auction basis",
     "S['R'][r]['Wp'] = Wn2[r]",
     "S['R'][r]['Wp'] = S['R'][r]['f'] * S['R'][r]['dd']"),
    ("run_family3: heir block basis after heir tax",
     "                S['R'][r]['Wp'] = Wn[r]\n                S['R'][r]['ppu'] = S['R'][r]['dd']\n            rows.append({'t': t, 'gen': gen, 'event': 'heir'",
     "                S['R'][r]['Wp'] = S['R'][r]['f'] * S['R'][r]['dd']   # POST-heir-tax basis (BASIS_CHANGE)\n"
     "                S['R'][r]['ppu'] = S['R'][r]['dd']\n            rows.append({'t': t, 'gen': gen, 'event': 'heir'"),
    ("_oscillation_check: legacy flows are empty; engine shows one heir tax then zero",
     "    _, net_leg, _, leg = settle_tw_flows({'TW': V, 'W_sell': 0.0, 'cum_after': 0.0}, p)\n"
     "    worst = max(abs(a - b) for a, b in zip(flows, leg))\n",
     "    _, net_leg, _, leg = settle_tw_flows({'TW': V, 'W_sell': V, 'cum_after': 0.0}, p)\n"
     "    expect = tau(V, sim_p) * V                  # one-off heir tax on the whole stake (post basis)\n"
     "    later = max((abs(x) for x in flows[1:]), default=0.0)\n"
     "    worst = max(abs(flows[0] - expect), later, abs(net_leg), max((abs(x) for x in leg), default=0.0))\n"),
    ("c7 check rewritten for the post basis",
     "    check('c7_oscillation_matches_legacy_settle_flows',\n"
     "          o['max_flow_diff'] < 1e-9 and abs(o['net_engine'] - o['net_legacy']) < 1e-6,\n"
     "          f\"net {o['net_engine']:.6f} vs legacy {o['net_legacy']:.6f}\")\n",
     "    check('c7_post_basis_one_off_heir_tax_then_zero_flows',\n"
     "          o['max_flow_diff'] < 1e-9 and o['n_legacy_flows'] == 0,\n"
     "          f\"engine net {o['net_engine']:.6f} = tau(V) V; later and legacy flows zero (max {o['max_flow_diff']:.2e})\")\n"),
    ("round trip: exact post-basis value 1 - tau^2/9",
     "    check('ratio_mirror_round_trip_cannot_exceed_paid', f_m['f'] <= 1.0 + 1e-12 and f_m['f'] > 0.99,\n"
     "          f\"f={f_m['f']:.6f}\")\n",
     "    check('ratio_mirror_round_trip_cannot_exceed_paid',\n"
     "          f_m['f'] <= 1.0 + 1e-12 and abs(f_m['f'] - (1.0 - fp['tau_0'] ** 2 / 9.0)) < 1e-9,\n"
     "          f\"f={f_m['f']:.6f}, hand value 1 - tau^2/9 = {1.0 - fp['tau_0'] ** 2 / 9.0:.6f}\")\n"),
]

RATES_CORE = [
    ("run_lines: year-end basis after the in-kind payment",
     "        EC = EC + paid\n        Wp = Wn\n",
     "        EC = EC + paid\n        Wp = f * V                               # POST-surrender basis (BASIS_CHANGE)\n"),
    ("run_lines: heir basis after the heir tax",
     "                Wp[d] = Wd\n",
     "                Wp[d] = f[d] * V[d]              # POST-heir-tax basis (BASIS_CHANGE)\n"),
]

CORE_FILES = {'wdt_core.py': WDT_CORE, 'valgen_core.py': VALGEN_CORE, 'rates_core.py': RATES_CORE}

def patch_text(text, patches, name):
    """Apply each (label, old, new) in order. Returns (new_text, log). Raises on a missing or ambiguous snippet.

    State of a patch in the current text:
      OLD occurs once            -> apply (this is the normal case)
      OLD absent, NEW present    -> already applied, skip
      anything else              -> error
    Where NEW extends OLD (OLD is a prefix of NEW), OLD still occurs after applying, so the test is
    instead "NEW present -> skip". Checking NEW alone is not safe in general: a NEW can be a substring
    of another patch's NEW, which would skip the edit.
    """
    log = []
    for label, old, new in patches:
        n_old = text.count(old)
        if old in new:
            if new in text:
                log.append(f"  skip  {label} (already applied)")
                continue
        elif n_old == 0 and new in text:
            log.append(f"  skip  {label} (already applied)")
            continue
        if n_old != 1:
            raise RuntimeError(f"{name}: '{label}': OLD snippet found {n_old} times (need exactly 1)")
        text = text.replace(old, new, 1)
        log.append(f"  apply {label}")
    return text, log


def locate(root, fname, override=None):
    """Path of one core. wdt_core.py sits in the model root; valgen_core.py and rates_core.py sit in
    subfolders (they import the root as parent.parent). Searches under root for the name, ignoring
    backups and OUTPUTS/. Exactly one match is required; use --core / --valgen / --rates to pick one."""
    if override:
        return Path(override)
    hits = [p for p in root.rglob(fname)
            if '.pre_basis' not in p.name and 'OUTPUTS' not in p.parts and '__pycache__' not in p.parts]
    if len(hits) != 1:
        raise RuntimeError(f"{fname}: found {len(hits)} copies under {root} (need exactly 1): "
                           + ', '.join(str(h) for h in hits) + ". Pass the path explicitly.")
    return hits[0]


def main(argv):
    if len(argv) < 2 or argv[1].startswith('--'):
        print(__doc__)
        return 2
    root = Path(argv[1])
    args = argv[2:]
    check_only = '--check' in args
    override = {}
    for flag, fname in (('--core', 'wdt_core.py'), ('--valgen', 'valgen_core.py'), ('--rates', 'rates_core.py')):
        if flag in args:
            override[fname] = args[args.index(flag) + 1]
    failed = False
    for fname, patches in CORE_FILES.items():
        try:
            path = locate(root, fname, override.get(fname))
        except RuntimeError as e:
            print(f"ABORT {e}")
            failed = True
            continue
        if not path.exists():
            print(f"{fname}: NOT FOUND at {path}")
            failed = True
            continue
        raw = path.read_bytes().decode('utf-8')
        crlf = '\r\n' in raw
        text = raw.replace('\r\n', '\n')
        try:
            new_text, log = patch_text(text, patches, fname)
        except RuntimeError as e:
            print(f"ABORT {e}")
            failed = True
            continue
        changed = new_text != text
        print(f"{path} ({'CRLF' if crlf else 'LF'}): " + ('no changes' if not changed else 'changes pending'))
        print('\n'.join(log))
        if check_only or not changed:
            continue
        bak = path.with_name(path.name + '.pre_basis.bak')
        if not bak.exists():
            bak.write_bytes(path.read_bytes())
        out = new_text.replace('\n', '\r\n') if crlf else new_text
        compile(out, str(path), 'exec')          # syntax check before anything is written
        path.write_bytes(out.encode('utf-8'))
        print(f"  wrote {path} (backup {bak.name}); syntax OK")
    if check_only:
        print('check only: nothing written')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
