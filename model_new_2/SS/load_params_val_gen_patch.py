"""
Replace the whole `p['val_gen'] = {...}` block in wdt_core.load_params() with this.
`raw` is the parsed TOML dict already used in load_params. Covers every key valgen_core.py reads
(P2b to P5 + the corrective auction), validates types and the route shares.
"""
vg = raw['val_gen']
_F  = lambda k: float(vg[k])
_I  = lambda k: int(vg[k])
_S  = lambda k: str(vg[k])
_FL = lambda k: [float(x) for x in vg[k]]
_IL = lambda k: [int(x) for x in vg[k]]
_SL = lambda k: [str(x) for x in vg[k]]

rs = {k: float(v) for k, v in vg['route_shares'].items()}
if abs(sum(rs.values()) - 1.0) > 1e-9:
    raise ValueError(f"[val_gen.route_shares] must sum to 1, got {sum(rs.values())}")

p['val_gen'] = {
    'T': _I('T'), 'G': _I('G'),
    'heir_influx': _S('heir_influx'), 'envelope_unit': _S('envelope_unit'),
    'consumption': _F('consumption'), 'consumption_vals': _FL('consumption_vals'),
    'index_wmin': bool(vg['index_wmin']),
    'tol_rev': _F('tol_rev'), 'tol_rev_sens': _FL('tol_rev_sens'),
    'route_shares': rs,
    'reset_interval': _I('reset_interval'), 'reset_sens': _IL('reset_sens'),
    'death_waiver': _I('death_waiver'),
    'lambda_vals': _FL('lambda_vals'), 'lambda_base': _F('lambda_base'),
    'verified_threshold': _F('verified_threshold'),
    'c_share_sens': _FL('c_share_sens'), 'alpha_ext': _FL('alpha_ext'),
    'strategy_k': _IL('strategy_k'), 'pv_rel_min_frac': _F('pv_rel_min_frac'),
    'g1_tol': _F('g1_tol'), 'g2_tol': _F('g2_tol'),
    'conv_extra_alphas': _FL('conv_extra_alphas'), 'shock_sizes': _FL('shock_sizes'), 'shock_year': _I('shock_year'),
    'c_cap_rules': _SL('c_cap_rules'),
    'verify_down_rules': _SL('verify_down_rules'), 'd_auction_rules': _SL('d_auction_rules'),
    'growth_vals': _FL('growth_vals'), 'surface_rules': _SL('surface_rules'),
}
