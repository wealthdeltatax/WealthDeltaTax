"""Second method for brief 041r: hand arithmetic, register numbers typed in, no file reads. Run: python3 -I check_v2.py"""
import math
w0, s, e, r5, d10, cap = 5.94, .927, .05, .12, .242, 6.6/3.0
om = (w0*(s+e) + d10*cap*s)*(1-r5)
eps_h = .0734/(.0442*om); eps_r = .0734/(.0474*om)
ret = 3.37+1.75+1.29+.77+.50+.16+.27
m1 = lambda m1a: m1a + 2.82 - 0.6 - ret
assert abs(ret-8.11) < 1e-9
# central
assert abs(m1(eps_r*.0474*om*100) - 1.45) < 5e-3
assert abs(m1(eps_h*.0474*om*100) - 1.98) < 5e-3
# swing 1: I-D1a, recalibrated eps: (6.07-3.41) * eps * omega
assert abs(eps_r*om*(6.07-3.41) - 4.12) < 5e-3, eps_r*om*2.66
assert abs(eps_h*om*(6.07-3.41) - 4.42) < 5e-3
# swing 2: I-D4a low/high, recalibrated
f = lambda w: (w*(s+e) + d10*cap*s)*(1-r5)
assert abs((m1(eps_r*.0474*f(7.5)*100) - m1(eps_r*.0474*f(5.8)*100)) - 1.94) < 0.01
# break-even
need = ret + 0.6 - 2.82
gh, gr = need/(eps_h*om), need/(eps_r*om)
se = (6.07-3.41)/2/1.2816
P = lambda g: .5*(1+math.erf(((g-4.74)/se)/math.sqrt(2)))
print("eps held/recal", round(eps_h,4), round(eps_r,4), "need", round(need,2), "g*", round(gh,3), round(gr,3), "se", round(se,3), "P", round(P(gh),3), round(P(gr),3))
