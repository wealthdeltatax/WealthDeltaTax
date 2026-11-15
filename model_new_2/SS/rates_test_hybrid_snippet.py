# ═════════════════════════════════════════════════════════════════════════════
# hybrid design: cohorts, schedules, residual tax, Zucman check, body split
# (paste between test_engine_invariants and test_valgen_equivalence)
# ═════════════════════════════════════════════════════════════════════════════

def test_hybrid(p, J):
    section('hybrid design: schedules, cohorts, body split, residual measures')
    x = np.array([0.0, 0.3, 0.5, 1.0, 2.0, 7.0, 50.0, 1000.0])

    # -- rate schedules ------------------------------------------------------
    rp = dict(tau_0=0.04, tau_m=0.90, k=0.004, wmin=0.5, schedule='logistic')
    check("rate_vec 'logistic' equals tau_vec exactly",
          np.array_equal(wc.rate_vec(x, rp), wc.tau_vec(x, rp['tau_0'], rp['tau_m'], rp['k'], rp['wmin'])))
    ln = dict(tau_0=0.04, tau_m=0.90, k=1.0, wmin=0.5, schedule='logistic_ln')
    r1 = wc.rate_vec(x, ln)
    r2 = wc.rate_vec(10.0 * x, dict(ln, wmin=5.0))
    check("'logistic_ln' is scale-free: scaling wealth and W_min together leaves the rate unchanged",
          np.abs(r1 - r2).max() < 1e-12)
    check("'logistic_ln' is zero below W_min and tau_0 at W_min",
          r1[0] == 0.0 and r1[1] == 0.0 and abs(r1[2] - ln['tau_0']) < 1e-12)
    try:
        wc.rate_vec(x, dict(ln, wmin=0.0))
        check("'logistic_ln' needs W_min > 0", False)
    except ValueError:
        check("'logistic_ln' needs W_min > 0", True)
    lad = dict(schedule='ladder', wmin=0.5, ladder=[(0.5, 0.1), (2.0, 0.3), (50.0, 0.5)])
    rl = wc.rate_vec(np.array([0.2, 0.5, 1.0, 2.0, 10.0, 50.0, 500.0]), lad)
    exp_mid = 0.1 + 0.2 * math.log(1.0 / 0.5) / math.log(2.0 / 0.5)
    check('ladder: zero below W_min, exact at anchors, linear in ln W between, flat beyond',
          rl[0] == 0.0 and abs(rl[1] - 0.1) < 1e-12 and abs(rl[2] - exp_mid) < 1e-12
          and abs(rl[3] - 0.3) < 1e-12 and abs(rl[5] - 0.5) < 1e-12 and rl[6] == 0.5)
    pts, capped = wc.ladder_to_tau([(1.0, 0.02), (5.0, 0.02)], 'stock', 0.05, 0.01, 0.99)
    check('ladder_to_tau: stock s -> s/(r-c)', abs(pts[0][1] - 0.02 / 0.04) < 1e-12 and not capped)
    pts, _ = wc.ladder_to_tau([(1.0, 0.02), (5.0, 0.45)], 'gain', 0.05, 0.01, 0.99)
    check('ladder_to_tau: gain G -> G r/(r-c)', abs(pts[1][1] - 0.45 * 0.05 / 0.04) < 1e-12)
    for sch, kref in (('logistic', None), ('logistic_ln', None)):
        W_ref, tau_ref = 100.0, 0.5
        k = wc.fit_k(sch, 0.04, 0.9, 0.5, W_ref, tau_ref)
        got = float(wc.rate_vec(np.array([W_ref]), dict(tau_0=0.04, tau_m=0.9, k=k, wmin=0.5, schedule=sch))[0])
        check(f'fit_k [{sch}]: fitted curve passes through the anchor', abs(got - tau_ref) < 1e-10, f'{got:.12f}')

    # -- body split ----------------------------------------------------------
    dec = np.array([24.0, 159.7, 474.1, 1017.4, 1806.9, 2780.4, 3941.2, 5412.4, 7671.1])
    c1 = rc._body_cells(dec, split=1)
    check('body split = 1 returns the deciles unchanged',
          len(c1) == len(dec) and np.allclose([w for _, _, w in c1], dec))
    c5 = rc._body_cells(dec, split=5, from_frac=0.5)
    check('body split preserves total wealth and total population',
          abs(sum(w for _, _, w in c5) - dec.sum()) < 1e-9 and abs(sum(s for _, s, _ in c5) - 0.9) < 1e-12,
          f'{len(c5)} cells')
    pw = [w / s for _, s, w in c5]
    check('body-split cell means are non-decreasing (before any repair)', np.all(np.diff(pw) > -1e-9))

    # -- cohorts -------------------------------------------------------------
    share = np.array([0.5, 0.3, 0.15, 0.04, 0.01])
    V0 = np.array([0.05, 0.3, 1.0, 5.0, 60.0])
    cal = dict(share=share, V0=V0)
    spec = dict(tiers=[(0.1, -0.09), (0.3, -0.04), (0.4, 0.02), (0.2, 0.07)], premium=[(0.05, 0.01), (0.01, 0.03)])
    cs = rc.cohort_spec(cal, spec)
    wsh = share * V0 / (share * V0).sum()
    tw = np.array([t[0] for t in spec['tiers']]); td = np.array([t[1] for t in spec['tiers']])
    check('cohorts: wealth-weighted mean return differential (tier + premium) is zero',
          abs(float(wsh @ cs['cell_diff']) + float(tw @ td)) < 1e-12)
    prem = cs['cohort_diag']['premium_by_cell']
    check('cohorts: narrowest premium band wins (a level, not a sum)',
          prem[-1] == 0.03 and prem[-2] == 0.01 and prem[0] == 0.0, str(prem))
    check('cohorts: tier SD matches its definition',
          abs(cs['cohort_diag']['tier_sd'] - math.sqrt(tw @ td ** 2 - (tw @ td) ** 2)) < 1e-12)
    try:
        rc.cohort_spec(cal, dict(spec, tiers=[(0.5, 0.0), (0.4, 0.0)]))
        check('cohort weights that do not sum to 1 raise', False)
    except ValueError:
        check('cohort weights that do not sum to 1 raise', True)

    # -- parameter file ------------------------------------------------------
    rp_ = p['rates']
    check('[rates.cohorts] and [rates.schedules] parse, and scenarios reference only defined ones',
          all(s['overrides'].get('cohorts') in (None, *rp_.get('cohorts', {}))
              and s['overrides'].get('schedule') in (None, 'logistic', 'logistic_ln', *rp_.get('schedules', {}))
              for s in rp_['scenarios'].values()))
    fg = rp_['figures']
    check('every scenario named in [rates.figures] is defined and in [rates.run].scenarios',
          all(n in rp_['scenarios'] and n in rp_['run']['scenarios']
              for k in ('decomposition', 'rate_grid', 'schedules', 'cohorts', 'scope') for n in fg.get(k, [])))

    # -- Zucman check, hand-computed ----------------------------------------
    cal = dict(V0=np.array([0.5, 2000.0, 4000.0]), y_ref_gbp_m=1.0)
    L = dict(prev_b=np.array([[10., 100., 100.], [10., 100., 100.], [10., 100., 100.]]),
             net_b=np.array([[0., 3., 3.], [0., 1., 1.], [0., 5., 5.]]),
             heir_b=np.array([[0., 0., 0.], [0., 0., 0.], [0., 4., 4.]]))
    z = rc.zucman_check({'lvl': L}, cal, 0.02, 1000.0)
    # pooled over the two billionaire cells: rates 3%, 1%, 5%; excluding heirs 3%, 1%, 1%
    check('zucman_check: pooled stock rate, share of years at or above the floor, with and without heirs',
          z['zuc_cells'] == 2 and abs(z['zuc_share_years'] - 2 / 3) < 1e-12
          and abs(z['zucx_share_years'] - 1 / 3) < 1e-12 and abs(z['zuc_mean'] - 0.03) < 1e-12
          and abs(z['zuc_min'] - 0.01) < 1e-12, str(z))
    z0 = rc.zucman_check({'lvl': L}, dict(cal, V0=np.array([0.5, 1.0, 2.0])), 0.02, 1000.0)
    check('zucman_check: NaN when no cell reaches the threshold', math.isnan(z0['zuc_share_years']))

    # -- pipeline: residual measures and closure -----------------------------
    if J is None:
        skip('hybrid pipeline checks', 'JST file not found')
        return
    block = rc.run_scenario(J, p, fg['scenario'], stride=8, verbose=False)
    ov = block['headline'][fg['mode']]['overall']
    m = ov['medians']
    ref = block['calibration']['exp_ref']
    if 'nonwdt_req_net_gdp' in m:
        check('residual traditional tax + net WDT = reference expenditure',
              abs(m['nonwdt_req_net_gdp'] + m['net_gdp_mean'] - ref) < 1e-9,
              f"{m['nonwdt_req_net_gdp']:.4f} + {m['net_gdp_mean']:.4f} vs {ref:.4f}")
    else:
        check('residual measures are in the headline medians', False)
    cal_ = block['calibration']
    if p['rates']['closure'].get('replaced_tax_gdp') == 'uk_2019':
        check("closure: replaced_ref equals rev_ref when replaced_tax_gdp = 'uk_2019'",
              abs(cal_['replaced_ref'] - cal_['rev_ref']) < 1e-12, f"{cal_['replaced_ref']:.4f}")
    if block.get('windows'):
        df = wc.table_to_frame(block['windows'])
        if 'nonwdt_req_relief_gdp' in df and 'relief_gdp' in df:
            check('relief-based residual is NaN exactly where relief is censored',
                  bool((df['nonwdt_req_relief_gdp'].isna() == df['relief_gdp'].isna()).all()))
    for name in [n for n in ('cohort_central', 'gain_ladder', 'wmin_house') if n in rp_['scenarios']]:
        try:
            b = rc.run_scenario(J, p, name, stride=12, verbose=False)
            rc.validate({'scenarios': {name: b}})
            check(f'scenario [{name}] runs and validates', True, f"{b['n_rows']} windows")
        except Exception as ex:                                  # noqa: BLE001
            check(f'scenario [{name}] runs and validates', False, repr(ex))
