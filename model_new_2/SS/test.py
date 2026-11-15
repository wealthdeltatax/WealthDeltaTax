import rates_data as rd
import rates_sweep as rs

J = rd.load_jst()

# Quick first run: UK only, every 5th start year
# cfg = rs.make_cfg(countries=['GBR'], start_stride=5)
cfg = rs.make_cfg(ms=3.0, ml=3.0, horizon=20)   # reserve sizing and horizon
df = rs.sweep(J, cfg)

print(rs.headline(df))                    # grouped by index mode
print(rs.by_country(df, mode='gdp_pc'))   # per-country detail

df.to_csv('sweep_results.csv', index=False)