"""
test_engine.py — equivalence of rates_engine.run_lines against valgen_core.run_family.
Run from a directory containing valgen_core.py, wdt_core.py and WDT_Params.toml
(valgen imports wdt_fmt; supply a stub exposing out_dir / ensure_dir if absent).
"""
import numpy as np
import valgen_core as vg
import rates_engine as re_
import rates_data as rd

RP = dict(tau_0=0.15, tau_m=0.70, k=0.001, W_min=2.0)

def compare(g_series, V0, c, ir, G, label, rule='delta'):
    T = len(g_series)
    p = dict(RP, V0_m=V0)
    r = vg.run_family(p, 1.0, list(g_series), G, 'delta' if rule == 'delta' else 'fresh_entrant', 'real',
                      consumption=c, index_rate=ir, refund_rule='ratio_mirror')
    hold = np.zeros(T); heir = np.zeros(T)
    for (t, kind, paid, L) in r['receipts']:
        (hold if kind == 'tax_inkind' else heir)[t - 1] += paid
    idx = (1.0 + ir) ** np.arange(1, T + 1)
    rp = dict(tau_0=RP['tau_0'], tau_m=RP['tau_m'], k=RP['k'], wmin=RP['W_min'])
    ph = np.array([G]) if G else None
    e = re_.run_lines(np.array(g_series), idx, np.array([V0]), np.array([1.0]),
                      np.array([0]), 1, ph, G or 10**6, c, rp, heir_rule=rule)
    d_hold = np.abs((e['tax'] + e['refund']) - hold).max()
    d_heir = np.abs(e['heir'] - heir).max()
    d_stake = abs(e['stake'][-1] - r['state_stake_true_T'])
    scale = max(1.0, np.abs(hold).max())
    ok = max(d_hold, d_heir, d_stake) / scale < 1e-9
    print(f"{'PASS' if ok else 'FAIL'}  {label:46} holding {d_hold:.1e}  heir {d_heir:.1e}  stake {d_stake:.1e}"
          f"   (refund years: {(hold < -1e-12).sum()})")
    return ok

J = rd.load_jst()
uk = rd.panel(J, 'GBR')
nom = uk['capital_tr'].loc[1947:2019].to_numpy()
rng = np.random.default_rng(1)
cases = [
  (np.full(100, 0.1045), 20.0, 0.035, 0.0451, 30, 'constant g, valgen baseline'),
  (np.full(100, 0.1045), 20.0, 0.0,   0.0,    30, 'constant g, no consumption/indexing'),
  (nom,                   20.0, 0.035, 0.0451, 30, 'UK nominal capital_tr 1947-2019, G=30'),
  (nom,                    3.0, 0.035, 0.0451, 30, 'UK series, low V0 (threshold crossing)'),
  (nom,                  150.0, 0.0,   0.0451, 30, 'UK series, high V0, no consumption'),
  (rng.normal(0.06, 0.25, 90), 20.0, 0.035, 0.03, 30, 'volatile random series (many refunds)'),
  (rng.normal(0.02, 0.20, 60), 5.0,  0.05, 0.02, 20, 'volatile, G=20, c=5%'),
  (nom,                   20.0, 0.035, 0.0451, None, 'single life (no deaths)'),
  (nom,                   20.0, 0.035, 0.0451, 30, 'UK series, fresh-entrant heirs', 'fresh'),
  (rng.normal(0.06, 0.25, 90), 20.0, 0.035, 0.03, 30, 'volatile, fresh-entrant heirs', 'fresh'),
]
ok = all([compare(*c) for c in cases])
print("\nALL PASS" if ok else "\nSOME FAILED")
raise SystemExit(0 if ok else 1)
