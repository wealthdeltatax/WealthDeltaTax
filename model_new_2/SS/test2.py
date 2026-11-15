import pandas as pd
d = pd.read_csv('sweep_out/baseline_windows.csv')
d = d[(d['mode']=='gdp_pc') & ~d['censored']]
d['drift'] = d['wealth_gdp_end'] / 7.21
s = d[d['drift'].between(0.67, 1.5)]
print(len(s), len(d))
print(s['relief_gdp'].describe(percentiles=[.1,.5,.9]))
print(s.groupby('era')['relief_gdp'].agg(['size','median']))