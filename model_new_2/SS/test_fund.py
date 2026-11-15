"""test_fund.py — analytic and accounting checks for rates_fund.run_fund."""
import numpy as np
import rates_fund as rf

def check(name, ok, detail=''):
    print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")
    return ok

res = []
# 1. constant income N=1, r=0: SRR fills at t=ms, LRR at ms+ml; relief = N thereafter
T, N, E = 40, 1.0, 10.0
o = rf.run_fund(np.full(T, N), np.full(T, E), np.zeros(T), ms=3, ml=3, horizon=10)
res.append(check('analytic: SRR fill = ms, LRR fill = ms+ml', o['srr_fill_year'] == 3 and o['fill_year'] == 6,
                 f"srr {o['srr_fill_year']} lrr {o['fill_year']}"))
res.append(check('analytic: relief = income after fill, coverage = N/E',
                 abs(o['coverage'] - N / E) < 1e-12 and not o['fail_in_window'], f"coverage {o['coverage']:.6f}"))

# 2. with positive return the fund fills sooner and still pays N (returns stay in the fund)
o2 = rf.run_fund(np.full(T, N), np.full(T, E), np.full(T, 0.05), ms=3, ml=3, horizon=10)
res.append(check('positive return: fills no later than r=0, pays at most income',
                 o2['fill_year'] <= o['fill_year'] and o2['coverage'] <= N / E + 1e-12,
                 f"fill {o2['fill_year']}, cov {o2['coverage']:.4f}"))

# 3. accounting identity on random paths: S_t = S_{t-1}(1+r) + net - R
rng = np.random.default_rng(7)
worst = 0.0
for _ in range(200):
    T_ = 60
    net = np.abs(rng.normal(1.0, 0.8, T_)) - rng.uniform(0, 0.6) * (rng.random(T_) < 0.1)
    r = rng.normal(0.04, 0.15, T_)
    o_ = rf.run_fund(net, np.full(T_, 10.0), r, ms=3, ml=3, horizon=10)
    S_prev = 0.0
    for t in range(T_):
        pred = S_prev * (1 + r[t]) + net[t] - o_['R'][t]
        worst = max(worst, abs(pred - o_['S'][t]))
        S_prev = o_['S'][t]
res.append(check('accounting identity S_t = S_{t-1}(1+r) + net - R (200 random paths)', worst < 1e-9, f"max err {worst:.1e}"))

# 4. revenue collapse: LRR must carry the phase-in, no failure
net = np.concatenate([np.full(20, 1.0), np.zeros(10)])
o4 = rf.run_fund(net, np.full(30, 10.0), np.zeros(30), ms=3, ml=3, horizon=10)
paid_after = o4['R'][20:]
res.append(check('collapse: relief phases out over ~W years while reserves cover it',
                 paid_after[0] > 0 and paid_after[3] < 1e-9 and o4['unmet_year'] is None and o4['ring_year'] is None,
                 f"relief after collapse {np.round(paid_after[:5], 2).tolist()}"))

# 5. a refund deluge larger than the whole fund is detected as insolvency
net = np.concatenate([np.full(15, 1.0), [-50.0], np.full(10, 1.0)])
o5 = rf.run_fund(net, np.full(26, 10.0), np.zeros(26), ms=3, ml=3, horizon=5)
res.append(check('deluge: insolvency and ring-fence breach are flagged', o5['insolvent_year'] == 16 and o5['ring_year'] == 16,
                 f"insolvent {o5['insolvent_year']} ring {o5['ring_year']}"))

# 6. censoring is reported, not dropped
o6 = rf.run_fund(np.full(12, 1.0), np.full(12, 10.0), np.zeros(12), ms=3, ml=3, horizon=10)
res.append(check('censored when fill + horizon > window', o6['censored'] and np.isnan(o6['coverage']), f"fill {o6['fill_year']}"))

# 7. no income, no fill
o7 = rf.run_fund(np.zeros(30), np.full(30, 10.0), np.zeros(30))
res.append(check('zero income never fills', o7['fill_year'] is None and o7['censored']))

print("\nALL PASS" if all(res) else "\nSOME FAILED")
raise SystemExit(0 if all(res) else 1)
