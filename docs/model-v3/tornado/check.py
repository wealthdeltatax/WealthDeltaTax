"""Second method for brief 027r: hand arithmetic with the register numbers typed in, no file reads. Run: python3 -I check.py"""
g, w0, s, e, r5, d10 = .0442, 5.94, .927, .05, .12, .242
cap = 6.6/3.0
def omega(w0=w0, s=s, e=e, r5=r5): return (w0*(s+e) + d10*cap*s)*(1-r5)
eps = .0734/(g*omega())
retired = 3.37+1.75+1.29+.77+.50+.16+.27
m1 = lambda m1a: m1a + 2.82 - 0.6 - retired
assert abs(retired-8.11) < 1e-9 and abs(m1(7.34)-1.45) < 1e-9
assert abs(m1(7.34*2.18/4.42) - (-2.27)) < 0.005          # swing, g low
assert abs(m1(7.34*7.47/4.42) - 6.52) < 0.011             # swing, g high (script prints 6.51)
assert abs(m1(7.34*omega(w0=5.80)/omega()) - 1.29) < 0.005  # swing, omega low
print("eps", round(eps, 4), "break-even g", round((retired+0.6-2.82)/7.34*4.42, 3), "ok")
