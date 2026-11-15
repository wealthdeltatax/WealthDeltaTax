import numpy as np, pandas as pd
import rates_data as rd, rates_sweep as rs
J = rd.load_jst()
pd.set_option('display.width', 200)
variants = {
 'baseline':           {},
 'upper (top1%=23%)':  {'dist_mode': 'upper'},
 'heir=fresh':         {'heir_rule': 'fresh'},
 'wealth x1.3':        {'dist_kw': {'wealth_scale': 1.3}},
 'rich consume 0.5%':  {'payout_top': 0.005},
}
for name, kw in variants.items():
    cfg = rs.make_cfg(index_modes=('gdp_pc',), wmin_gbp_m=0, tau_0=0.3, tau_m=0.9,
                      k_per_gbp_m=0.005, c_mode='stationary', start_stride=3, **kw)
    df = rs.sweep(J, cfg, verbose=False); ok = df[~df['censored']]
    drift = ok['wealth_gdp_end'] / rs.calibration(J, cfg)['wealth_to_gdp']
    print(f"{name:20s} net/GDP {100*ok['net_gdp_mean'].median():.2f}%  "
          f"relief/GDP {100*ok['relief_gdp'].median():.2f}%  drift {drift.median():.2f}")