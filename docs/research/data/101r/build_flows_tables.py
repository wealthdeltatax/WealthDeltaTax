#!/usr/bin/env python3
"""101r: build flows_register.csv and flows_crosswalk.csv.

Run (after the three derive_*.py scripts): python -I docs/research/data/101r/build_flows_tables.py
Numeric cells are read from the derived outputs, not typed. Rows classed unset carry no number.
"""
import csv, os, statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
D = {}
for r in csv.DictReader(open(os.path.join(HERE, "derived_ons_flows.csv"))):
    D[(r["item"], int(r["year"]))] = float(r["value"])
J = {}
for r in csv.DictReader(open(os.path.join(HERE, "jst_split_stats.csv"))):
    J[(r["period_or_check"], r["item"])] = r
H = {}
for r in csv.DictReader(open(os.path.join(HERE, "hmrc_37_coverage_vs_ons.csv"))):
    H[(r["hmrc_item"], r["ons_year"])] = r


def series(item, lo=1998, hi=2025):
    return [D[(item, y)] for y in range(lo, hi + 1) if (item, y) in D]


def rng(item, scale=100.0, unit="%", dp=1, ref=2024, lo=1998, hi=2025):
    v = [x * scale for x in series(item, lo, hi)]
    return (f"{ref}: {D[(item, ref)] * scale:.{dp}f}{unit}; {lo}-{hi} min/median/max "
            f"{min(v):.{dp}f}/{st.median(v):.{dp}f}/{max(v):.{dp}f}{unit}")


def d62_range(lo=1998, hi=2025, ref=2024):
    v = [100 * D[("D62_benefits_GBPm", y)] / D[("B6g_gdhi", y)] for y in range(lo, hi + 1)]
    r = 100 * D[("D62_benefits_GBPm", ref)] / D[("B6g_gdhi", ref)]
    return f"{ref}: {r:.1f}%; {lo}-{hi} min/median/max {min(v):.1f}/{st.median(v):.1f}/{max(v):.1f}%"


def gbpm(item, ref=2024):
    return f"{ref}: GBP {D[(item, ref)] / 1000:.1f}bn"


def jst(period, item, col="mean_or_value", dp=3):
    return f"{float(J[(period, item)][col]):.{dp}f}"


REG = []
H_ = ["id", "variable", "definition", "accounting_location", "target_cell_dimension", "classification",
      "source_reference", "calculation_and_script", "value_or_range", "uncertainty_caveats", "intended_use",
      "proposed_ruling", "relation_to_existing_row", "open_question_or_data_request"]
OF = "derive_ons_flows.py"


def add(*a):
    assert len(a) == len(H_), (len(a), a[0])
    REG.append(a)


# ---- income, transfers, taxes ---------------------------------------------------------------
add("F-01", "Labour income: compensation of employees (D.1), share of gross primary income",
    "Wages and salaries D.11 plus employers' social contributions D.12, S.14, before tax",
    "Y_L, household account, resources", "aggregate only; no wealth-band or stage split held",
    "Observed (aggregate)", "ons_ukea_household_annual.csv HAEB (D.1), HABL (B.5g), table 6.2.3/6.2.4",
    f"HAEB/HABL; {OF}", rng("D1_compensation_share_B5g"),
    "D.12 is not cash income to the household in the year; includes employer pension contributions. No cell dimension.",
    "calibration (aggregate constraint) and validation", "further data required (by cell)", "none",
    "By wealth band and stage: needs a household survey link (WAS/FRS/LCF), not held")
add("F-02", "Self-employment and housing services: gross operating surplus plus mixed income (B.2g+B.3g), share of B.5g",
    "Includes imputed rent of owner-occupiers and landlords' operating surplus (B.2g), self-employed mixed income (B.3g)",
    "Y_L/Y_P boundary; housing services in B.2g not D.45", "aggregate only", "Observed (aggregate)",
    "ons_ukea_household_annual.csv CRTY, HABM, HAXH", f"CRTY/HABL; {OF}", rng("B2gB3g_operating_mixed_share_B5g"),
    "B.2g and B.3g cannot be separated into labour and capital return here; gross of CFC",
    "constraint and validation", "further data required (split of B.2g into imputed rent and lettings)", "none",
    "ONS split of B.2g by dwelling services versus other; not held")
add("F-03", "Transfer income: social benefits in cash (D.62) share of disposable income",
    "State pension and social security cash D.621, other social insurance D.622 (includes private pension benefits), social assistance D.623",
    "TR, resources", "aggregate only; stage (retired) is the intended dimension",
    "Observed (aggregate)", "ons_ukea_household_annual.csv HAYP, L8QH, L8QV, HAYU", f"HAYP/HABN; {OF}",
    "D.62 share of B.6g " + d62_range() + "; D.622 only " + rng("D622_share_B6g"),
    "D.622 mixes private pension benefits with other insurance; no split by retired status",
    "calibration (aggregate)", "implement with scenario range", "none", "Benefit income by stage and band: needs FRS/WAS")
add("F-04", "Taxes on income and wealth (D.5), share of gross primary income",
    "Current taxes on income and wealth paid by households (T_C), excluding WDT", "T_C, uses",
    "aggregate only", "Observed (aggregate)", "ons_ukea_household_annual.csv HAYC", f"HAYC/HABL; {OF}",
    rng("D5_share_B5g"), "D.5 includes council tax; D.61 contributions are separate",
    "calibration (aggregate)", "implement with scenario range", "none", "none")
add("F-05", "Gross disposable income B.6g", "Balance of primary incomes plus social benefits and other current transfers received, less current taxes, net social contributions and other transfers paid; excludes social transfers in kind (D.63)",
    "B.6g", "aggregate", "Observed", "HABN (UKEA), RPHA (QSA)", f"HABN; {OF}",
    gbpm("B6g_gdhi"), "UKEA and QSA vintages differ by up to GBP 1m on identical years; not spliced",
    "calibration", "ready for implementation", "none", "none")
# ---- consumption and saving ----------------------------------------------------------------------
add("F-06", "Household final consumption (P.31) as a share of B.6g",
    "Individual consumption expenditure, current prices; not net depletion", "C, uses", "aggregate only",
    "Observed (aggregate)", "ABPB (UKEA 6.2.6_A; held also ons_household_consumption_annual.csv)", f"ABPB/HABN; {OF}",
    rng("consumption_share_of_B6g"), "Consumption share of income, not of wealth. No consumption by wealth band here",
    "calibration (aggregate); validation", "further data required (by band)", "does not support I-D14c as evidence",
    "Consumption by wealth band: LCF/WAS link; not held")
add("F-07", "Saving ratio, published", "B.8g/(B.6g+D.8), households; published DG5H",
    "B.8g", "aggregate", "Observed", "DG5H (UKEA), DGD8 (QSA HH_3)", f"{OF} ID2 (tolerance 0.06pp)",
    rng("saving_ratio_pct", 1.0, "%"), "Includes pension accrual (D.8). Gross of CFC", "validation",
    "ready for implementation", "none", "none")
add("F-08", "Non-pension saving: B.8g - D.8 (the part of the ratio not pension accrual)",
    "Derived by the 097r identity; ONS publishes the split as JS8S (contribution to the ratio)",
    "S, non-pension", "aggregate; band/stage unset", "Derived",
    "HADA, HAZA; QSA JS8S, JS97 (HH_3)", f"B8g-D8; {OF} (QSA1 tolerance 0.101pp, three terms at 1dp)",
    "ratio contribution " + rng("ratio_nonpension_part_pct", 1.0, "pp"),
    "Negative in some years. Gross of CFC. Saving on the income side only (Scenario B)",
    "validation (aggregate); calibration only with a labelled scenario by cell", "implement with scenario range",
    "supersedes nothing; cross-checks I-W3a to I-W3d aggregates", "Non-pension saving by wealth band and stage: unset, see data requests")
add("F-09", "Cash-basis saving ratio (CSJ8)", "ONS alternative that excludes the pension net-equity adjustment and uses cash contributions and benefits",
    "S, cash basis", "aggregate", "Observed (alternative definition)", "QSA HH_Alt CSJ8", f"{OF}",
    rng("cash_basis_saving_ratio_pct", 1.0, "%"), "Different definition from DGD8; report difference, do not average",
    "validation", "ready for implementation (as a reported alternative)", "none", "none")
# ---- pension ----------------------------------------------------------------------------------------
add("F-10", "Pension accrual: adjustment for change in pension entitlements D.8",
    "Net equity change in funded and unfunded pension schemes credited to households; counts as saving",
    "D.8 -> S (pension)", "aggregate; accumulation vs decumulation stage unset", "Observed (aggregate)",
    "HAZA (UKEA 6.2.6_B), RNMB (QSA HH_3)", f"HAZA; {OF}",
    "share of B.6g " + rng("D8_share_of_B6g") + "; of open net worth " + rng("D8_over_open_NW"),
    "Valuation basis: national-accounts net equity (ONS), not WAS Round 8 SCAPE. The difference is not quantified here. Not the Resolution Foundation basis",
    "calibration (aggregate pension flow) with named basis", "implement with scenario range", "none",
    "Reconcile ONS pension entitlements (AF.6 stock) to WAS pension wealth totals: data request DR-01")
add("F-11", "Pension contributions (employee and employer)", "D.611 employers' actual, D.613 households' actual, D.612 imputed, D.614 supplements, D.61SC charges",
    "contributions into D.8", "aggregate; contributions include National Insurance", "Proxy",
    "L8NL, MA4A, L8PT, L8Q9, M92I, HADI", f"{OF} (ID7 sum check)", "levels in derived_ons_flows.csv only; no pension-only series",
    "Valuation basis: ONS national-accounts flow series (not WAS SCAPE, not Resolution Foundation). D.611 and D.613 mix NIC and pension contributions; D.614 equals D.442 (pension income attributed and returned)",
    "context only", "further data required", "none", "DR-02: split D.611/D.613 into pension and NIC")
add("F-12", "Pension investment return", "Return on pension wealth, valuation basis named",
    "r on pension wealth; D.442 and B.103 AF.6", "unset by cell", "Unset",
    "D.442 (KZK9); B.103 AF.6 (N4EV); pension stock by instrument not held", f"{OF}", "",
    "Valuation basis: ONS national-accounts flow series (not WAS SCAPE, not Resolution Foundation). A rate needs the AF.6 stock, which is not held. B.103 AF.6 swings with actuarial discount rates ("
    + f"{D[('B103_AF6_pension_insurance', 2019)] / 1000:.0f}bn in 2019, {D[('B103_AF6_pension_insurance', 2024)] / 1000:.0f}bn in 2024"
    + "): a valuation change, not an asset return",
    "none", "remain unset", "none", "DR-01: AF.6 stock (S.14) by year")
add("F-13", "Pension withdrawal and decumulation", "Benefits paid from funded and unfunded schemes (D.622 other social insurance benefits)",
    "outflow of D.8", "stage (retired); band unset", "Proxy",
    "L8QV (D.622)", f"{OF}", "ratio D8/D622 descriptive: " + rng("D8_over_D622", 1.0, "", 2),
    "Valuation basis: ONS national-accounts flow series (not WAS SCAPE, not Resolution Foundation). D.622 includes non-pension insurance benefits; lump sums and annuity purchases not separated",
    "context only", "further data required", "none", "DR-03: D.622 split by scheme type and age group")
add("F-35", "Pension valuation basis register", "ONS national-accounts net equity (D.8, AF.6); WAS Round 8 SCAPE-method DB wealth (pack wealth base); Resolution Foundation basis (excludes DB, validation context only)",
    "basis label on every pension row", "all", "Observed (labelling)", "098r s9 (Round 8 break); 099r BF/AB class notes",
    "text", "", "The three bases are not reconciled here. Never mix. BF-02 and AB-01 use the RF basis",
    "validation context only for RF", "remain unset (no conversion factor)", "none", "DR-01")
# ---- property income and returns ------------------------------------------------------------------
add("F-14", "Retained cash property income (D.4 received excluding D.441 and D.442), share of B.6g",
    "Interest, distributed income, CIS and rent on land received by households, after removing income attributed to insurance and pension holders",
    "y W cash yield (aggregate)", "aggregate; retained fraction by band unset", "Derived",
    "HAXU, KZK8, KZK9 (UKEA 6.2.3)", f"{OF}",
    rng("D4_excl_D441_D442_share_B6g"),
    "Includes sheltered income; not net of interest paid (D.4 paid is GBP "
    + f"{D[('D4_property_paid_GBPm', 2024)] / 1000:.0f}bn in 2024); not a yield on wealth",
    "calibration (aggregate constraint)", "implement with scenario range", "none",
    "Retained share by band: unset; HMRC 3.7 is by total income, not wealth")
add("F-15", "HMRC taxable interest and dividends against ONS D.41 and D.42", "Table 3.7, 2023-24, UK taxpayers, SPI; bank interest and dividends",
    "coverage check", "total-income range, not wealth", "Observed",
    "Table 3.7 columns for interest and dividends", "derive_hmrc_37.py",
    f"interest {float(H[('HMRC bank and building society interest', '2024')]['ratio']):.2f} and dividends "
    f"{float(H[('HMRC dividends', '2024')]['ratio']):.2f} of ONS 2024 (tax-year 2023-24 against calendar 2024)",
    "Taxpayer taxable income only; ISA, pension and non-taxpayer income excluded; tax year not calendar year",
    "validation only", "ready for implementation (as a coverage check)", "none", "none")
add("F-16", "Housing services yield cross-check", "ONS B.2g over opening dwellings plus land (S.14) set against JST housing rental return (net rent/price)",
    "r housing, cash part", "aggregate", "Proxy",
    "HABM, E46V, E44N; 100r housing_y_nominal", "derive_jst_split.py",
    f"ONS {jst('cross_check_housing_1998_2019', 'ons_B2g_over_open_dwellings_land_mean', dp=2)}% vs JST {jst('cross_check_housing_1998_2019', 'jst_housing_y_nominal_mean', dp=2)}% (1998-2019 mean); difference {jst('cross_check_housing_1998_2019', 'difference_ons_minus_jst_pp', dp=2)}pp",
    "ONS is gross of CFC and includes non-dwelling operating surplus; JST is net rent over a country housing stock. Definitions differ; not spliced",
    "validation only", "remain unset (as a calibration)", "none", "DR-04: ONS CFC on dwellings and B.2g split")
for fid, nm, item, dp in (("F-17", "Cash yield, portfolio, real", "portfolio_y_real", 3), ("F-18", "Holding gain, portfolio, real", "portfolio_g_real", 3)):
    add(fid, f"{nm} (JST market portfolio, arithmetic mean of annual components)",
        "Real cash-yield (or holding-gain) contribution of the JST capital total return, weights recovered from composite returns (100r)",
        "y or g_h in W(1+g_h)+S", "market portfolio; not household or band", "Derived",
        "docs/research/data/100r/returns_decomposition.csv", "derive_jst_split.py (reproduces 100r to 0.0004pp)",
        f"1896-2019 mean {jst('all_1896_2019', item)}% (sd {float(J[('all_1896_2019', item)]['sd_or_ref']):.1f}); 1980-2019 mean {jst('1980_2019', item)}%; 1896-1939 {jst('1896_1939', item)}%; 1947-1979 {jst('1947_1979', item)}%",
        "Bond yield is a proxy (coupon or yield to maturity); bill gain is zero by convention; housing yield includes imputed rent; arithmetic only, the geometric I-D1a2 does not split additively; ends 2019; 1940-46 absent",
        "calibration with a scenario range across the period means; not household retained income", "implement with scenario range",
        "supports I-D1a (arithmetic); cannot split I-D1a2", "none")
add("F-19", "Total return, real, arithmetic (JST)", "Sum of F-17 and F-18", "r", "market portfolio", "Derived",
    "same", "derive_jst_split.py", f"1896-2019 mean {jst('all_1896_2019', 'capital_tr_real')}% (I-D1a central 4.74)",
    "As F-17", "calibration", "ready for implementation (already in the register)", "supports I-D1a", "none")
add("F-20", "Cash yield and gain by asset class (real)", "Equity, housing, bond, bill yield and gain, JST",
    "by asset class", "asset class (not band)", "Derived",
    "100r returns_decomposition.csv", "derive_jst_split.py (jst_split_stats.csv all periods)",
    f"1896-2019 mean real yield equity {jst('all_1896_2019', 'equity_y_real')}, housing {jst('all_1896_2019', 'housing_y_real')}, bond {jst('all_1896_2019', 'bond_y_real')}, bill {jst('all_1896_2019', 'bill_y_real')} (% per year)",
    "Bond and bill yields are proxies; band holdings by asset class belong to 102r", "calibration via cell asset weights (102r)",
    "implement with scenario range", "none", "Cell asset weights: 102r")
# ---- revaluations and constraints --------------------------------------------------------------------------
add("F-21", "Revaluation of nominal liabilities (real erosion)", "Opening financial liabilities x pi/(1+pi), pi from the household expenditure deflator",
    "O / real term of liabilities", "aggregate; by band belongs to 102r (debt)", "Derived",
    "NIWJ (ons_nbs_financial_annual.csv), CRXA", f"{OF}", "as share of opening net worth " + rng("real_erosion_over_open_NW", 100.0, "%", 2),
    "Loans are valued at par in B.103, so this is a real-terms identity, not a recorded flow. NIWJ mixes mortgages, other loans and payables",
    "constraint and validation", "implement with scenario range", "none", "Liabilities by band and debt type: 102r")
add("F-22", "Holding gains on financial assets (B.103) and other volume changes (B.102)", "Revaluation account, S.14 plus S.15, financial only",
    "CG", "aggregate", "Observed", "CWUR, CWU2, N4CX, N4EV (UKEA 6.1.9, 6.1.10)", f"{OF} (ID11)",
    f"B.103 {gbpm('B103_holding_gain_fin')}; of which equity {D[('B103_AF5_equity', 2024)] / 1000:.0f}bn, pension and insurance {D[('B103_AF6_pension_insurance', 2024)] / 1000:.0f}bn",
    "Financial assets only. Non-financial (housing) revaluation not held. S.14+S.15 label",
    "validation", "ready for implementation (as a reported series)", "none", "DR-05: non-financial revaluation (B.103 non-financial), S.14")
add("F-23", "Net-worth residual O", "dNW(E45V) - B.101g - B.102 - B.103; absorbs CFC, non-financial revaluation, S.15 mismatch and statistical discrepancy",
    "O", "aggregate", "Derived", "E45V, HABD, CWU2, CWUR", f"{OF}", "share of opening NW: " + rng("O_residual_over_open_NW"),
    "Reported, never absorbed into S. Not a parameter", "constraint", "ready for implementation (as a reported residual)", "none",
    "DR-05, DR-04")
add("F-24", "Aggregate saving over opening net worth (gross of CFC)", "B.8g/E45V[t-1], and non-pension (B.8g-D.8)/E45V[t-1]; no CFC series held",
    "S / W", "aggregate", "Derived", "HADA, HAZA, E45V", f"{OF}",
    "all saving " + rng("B8g_over_open_NW") + "; non-pension " + rng("nonpension_B8g_over_open_NW"),
    "Gross of CFC so an upper bound for net saving. The kernel c is not consumption: c=(y-s)/(1+r); see 093r",
    "constraint (aggregate saving over wealth)", "remain unset (as a rate)", "context for I-D14c (093r computes c); does not test it or select a replacement", "DR-04")
add("F-25", "Legacy I-D14c: 3.5% consumption share of net worth", "v2 `c` default (valgen D16); a framing value, not an estimate",
    "kernel c", "none", "Scenario (legacy comparator)", "docs/model-v3/inputs.md I-D14c; 093r",
    "none", "3.5 as legacy comparator only (range 0.5 to 5 in the register)",
    "Not UK evidence. Never used as support for a band rate", "neither", "remain unset",
    "legacy; 093r reports an aggregate arithmetic range for c of 0.4 to 3.0%; this block adds no value", "none")
# ---- existing rows --------------------------------------------------------------------------------------
add("F-26", "Existing row I-D1a (arithmetic mean real total return 4.74)", "JST UK arithmetic mean",
    "r", "market portfolio", "Observed (source JST); proxy for household return",
    "inputs.md I-D1a", "derive_jst_split.py", f"reproduced {jst('all_1896_2019', 'capital_tr_real')}%",
    "As F-19", "calibration", "ready for implementation", "supports (value reproduced to 0.001pp)", "none")
add("F-27", "Existing row I-D1a2 (geometric 4.42)", "Geometric mean real return", "r", "market portfolio", "Derived",
    "inputs.md I-D1a2", "none", "no additive split", "Geometric means do not split into yield and gain additively; the split rows are arithmetic",
    "calibration", "ready for implementation", "reclassifies the split rows as arithmetic-only", "none")
add("F-28", "Audit I-W1c: UK financial return gap, top decile minus bottom deciles (1.8 to 2.0 pp)",
    "Portfolio-composition-implied mean financial return, WAS 2016-18, Bangham and Leslie 2020 Fig 7, financial wealth only",
    "r by band (validation)", "wealth decile, financial wealth", "Proxy", "inputs.md I-W1c; AB-05 (shares in zero-return assets, 71% to 17% by decile, Advani-Bangham-Leslie)",
    "none", "row range 1.8 to 2.0 pp (as registered)",
    "Built from composition, not observed returns; excludes housing and pensions; source figure not held; direction agrees with AB-05 and the gap is described as probably larger",
    "validation only", "remain unset (as calibration); keep as validation", "supports the direction; reclassify from judgement to proxy; the numeric gap is not verifiable from held files",
    "Fagereng-style UK return by rank is not available")
add("F-29", "Audit I-W3a: net active saving rate by wealth, 6 to 8% of disposable income", "Norway, 2005-2015, Fagereng et al.; read from a figure",
    "S by wealth band", "wealth percentile (Norway)", "Proxy (foreign)", "inputs.md I-W3a (SW2); PDF not held", "none", "row range 6 to 8% (as registered)",
    "Foreign population and income concept; figure reading. For scale only (a different concept, not a test): UK non-pension saving, contribution to the ratio of B.6g+D.8, "
    + rng("ratio_nonpension_part_pct", 1.0, "pp"),
    "context only", "remain unset (UK)", "does not support as a UK value; UK evidence is aggregate or by income (F-33)", "UK saving by wealth band: not available in held data")
add("F-30", "Audit I-W3b: gross saving rate top 1% (about 35%)", "Norway 2005-2015, includes unrealised capital gains", "S+CG by band", "top 1%",
    "Proxy (foreign), different definition", "inputs.md I-W3b (SW2)", "none", "row point 35%",
    "Gross rate includes holding gains; not comparable with the household saving ratio (which excludes holding gains) or with F-08",
    "context only", "remain unset", "contradicts use as a saving rate: it is gross of holding gains, so mixes S and CG", "none")
add("F-31", "Audit I-W3c: net saving share of the change in family financial wealth (7 to 24%)", "GB financial wealth, WAS, Bangham and Leslie 2020 Fig 6; AB-01 gives passive shares 76 to 93%",
    "S share of dW (validation)", "average family, not by band", "Proxy (validation)", "inputs.md I-W3c; AB-01", "none", "row range 7 to 24% (as registered)",
    "Financial wealth only; excludes pensions and housing; RF-style counterfactual method", "validation only",
    "implement with scenario range (validation)", "supports (AB-01 passive 76 to 93% implies saving 7 to 24%)", "none")
add("F-32", "Audit I-W3d: active saving about 40% of total wealth gain, 2018-20 to 2020-22", "Before the fall (RF basis excludes DB pensions); BF-02 gives 40% active in the latest period",
    "S share of dW (validation)", "age and income, not band", "Proxy (validation)", "inputs.md I-W3d; BF-02", "none", "row point 40%",
    "Two-year window including pandemic saving; RF basis, not the WDT pension basis", "validation only", "implement with scenario range (validation)",
    "supports (BF-02 latest-period active 40%); not a basis for a central rate", "RF basis versus WDT basis: DR-01")
# ---- saving by income and surveys -----------------------------------------------------------------------------
add("F-33", "Saving by lifetime income and education (direction)", "LCFS active saving; ELSA wealth to lifetime earnings (Bozio and others 2013)",
    "S by cell (income side)", "income quintile, education; not wealth band", "Scenario",
    "095r reading; 099r none for band", "none", "direction only; gap of the order of 4 points of income (median, highest education against compulsory-only), a nearest UK bound, not a calibration",
    "Ranks by income or education, not wealth; excludes holding gains; the authors say it does not speak to the very wealthy", "scenario range (labelled)",
    "implement with scenario range", "supports a direction for working-saver cells; no row exists", "Saving by wealth band: further data required")
add("F-34", "Passive and active share of wealth change (validation moments)", "BF-02 passive 53% since 2010-12 (60% in 2018-20 to 2020-22); AB-01 passive 76 to 93% financial wealth",
    "validation of S+CG split", "average family", "Observed (moment)", "099r moments BF-02, AB-01", "none", "53%; 60%; 76 to 93% (as published)",
    "Resolution Foundation basis excludes DB pensions; validation context only; never mixed with the ONS or SCAPE basis", "validation only",
    "ready for implementation (as validation moments)", "none", "none")
add("F-36", "NMG survey saving and debt-service variables", "be2afree_c (share of household income put aside as cash savings), soa1 (change in saving excluding pension), qbe02 (left-over income change), be08free_c (mortgage instalment), be07free_c (mortgage balance), qincomev2 (income band), cv11/BOE65afree_c (savings balance)",
    "S (cash), debt service", "household, income band; no wealth band except through savings balances", "Unset",
    "nmg_variable_inventory_2011_2026.csv (variable names and labels only)", "none", "",
    "Microdata and the workbook are not held (097r: reachable but not parseable); only the variable inventory is held; wording changed across waves", "none",
    "further data required", "none", "DR-06: NMG 2011-2026 workbook contents (values), exact wave coverage per variable")

with open(os.path.join(HERE, "flows_register.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(H_)
    w.writerows(REG)

X = [["source_id", "file_or_table", "publisher_and_link", "reference_period", "population_unit_frequency_price_basis",
      "definitions_and_coverage", "available_dimensions", "revisions_and_limits", "held_file_checked_against_published", "used_for_register_rows"]]
X += [
    ["X-01", "docs/research/data/097r/ons_ukea_household_annual.csv (UKEA tables 6.2.3 to 6.2.7, 6.1.9, 6.1.10; series ids per row)", "ONS, United Kingdom Economic Accounts, https://www.ons.gov.uk/economy/grossdomesticproductgdp/datasets/unitedkingdomeconomicaccounts", "1997-2025 annual (financial 1998-2025)", "Households, sector labelled S.14 in the held file (S.14+S.15 for B.102 and B.103); GBP m; current prices; mostly NSA", "National-accounts household sector; B.2g contains imputed rent; D.8 on a net-equity basis; whether the headline saving ratio covers NPISH was not re-verified", "Time series, aggregate only; no wealth, age or income split", "Subject to ONS revision; vintage differs from QSA", "Identities pass internally (derive_ons_flows.py, 392 checks); not re-fetched, the workspace network allowlist blocks the ONS site", "F-01 to F-14, F-21 to F-24"],
    ["X-02", "docs/research/data/097r/qsa_household_annual_2026q2.csv (sheets HH_1 to HH_3, HH_Alt)", "ONS, Quarterly sector accounts, release 30 Sep 2026", "1948-2025 annual (varies by series)", "Households; GBP m or per cent; current prices", "JS8S and JS97 give the non-pension and pension contributions to the ratio; CSJ8 is the cash-basis ratio", "Time series", "Latest vintage; UKEA values differ by up to GBP 1m", "Workbook held (quarterlysectoraccounts2026q2.xlsx); the CSV was extracted by 097r; QSA1 check passes", "F-05, F-07 to F-10"],
    ["X-03", "docs/research/data/097r/ons_nbs_household_stocks_annual.csv (E45V, E46V, E44N, E462, E3VW)", "ONS National balance sheet, https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/datasets/nationalbalancesheet", "1997-2025 end-year", "S.14 and S.14+S.15 series; GBP m; current prices", "Net worth includes pension entitlements on the national-accounts basis; non-financial assets at current replacement or market value", "Aggregate stocks only", "Revisions", "Identity E45V=AN.1+AN.2+BF.90 passes (ID8); not re-fetched", "F-16, F-23, F-24"],
    ["X-04", "docs/research/data/097r/ons_nbs_financial_annual.csv (NYOH, NITF, NIWJ)", "ONS, https://www.ons.gov.uk/economy/grossdomesticproductgdp/timeseries/nyoh/nbs", "1997-2025", "S.14; GBP m", "Net financial assets, financial assets and liabilities", "No instrument split in the held file", "Revisions", "Used in ID8; not re-fetched", "F-21, F-23"],
    ["X-05", "docs/research/data/097r/ons_household_consumption_annual.csv (ABPB)", "ONS UKEA", "1997-2025", "Households; GBP m", "P.31 household use", "None", "As X-01", "Equals ABPB in X-01", "F-06"],
    ["X-06", "docs/research/data/097r/hmrc_csv/Collated_Tables_3_1_to_3_11_2324__Table_3_7.csv", "HMRC Personal Incomes Statistics, Table 3.7, 2023-24, https://www.gov.uk/government/statistics/personal-incomes-statistics-tables", "Tax year 2023-24", "UK taxpayers, SPI; thousands, GBP m, GBP", "Net property, bank interest, dividends and other income by range of total income", "Total-income range (14 ranges)", "Sampling error; amounts to 3 significant figures", "Column sums reproduce 'All ranges' within 1.5% (derive_hmrc_37.py)", "F-14, F-15"],
    ["X-07", "docs/research/data/097r/hmrc_html_summary_extracts.csv; property_rental_income_statistics_tables_2026.ods", "HMRC rental income, CGT and IHT statistics", "2023-24, 2024-25", "Individuals", "Rental income 2024-25 individuals GBP 49.81bn (HTML extract); ODS contents not parsed", "None parsed", "Not parsed", "No", "context only; no register row"],
    ["X-08", "docs/research/data/097r/nmg_variable_inventory_2011_2026.csv", "Bank of England NMG household survey", "2011-2026 (waves)", "Households", "Variable names and labels only (696)", "Income band; savings balances", "Microdata not held", "Inventory only", "F-36"],
    ["X-09", "docs/research/data/100r/returns_decomposition.csv", "Jorda-Schularick-Taylor R6 via 100r", "UK 1896-2019, 117 years (1940-46 absent)", "Market portfolio; decimal rates", "Yield and gain split, weights recovered algebraically", "Asset class", "Ends 2019; bond yield proxy", "Reproduced to 0.0004pp (derive_jst_split.py)", "F-16 to F-20, F-26, F-27"],
    ["X-10", "docs/research/095r-bozio-2013-reading.md", "Bozio, Emmerson, O'Dea, Tetlow 2013, IFS WP 13/30", "1978-2009 (LCFS), ELSA linked records", "Households; active saving", "Saving by income or education; excludes holding gains", "Income quintile, education", "Paper not re-read here; note relied on", "No", "F-33"],
    ["X-11", "docs/research/data/099r/moments.csv (BF-02, AB-01, AB-05, GB-01)", "Resolution Foundation Before the fall; Advani-Bangham-Leslie 2021; IFS Green Budget 2025", "2008-2022", "Families, GB", "Passive and active split on RF basis (excludes DB pensions)", "Average family", "Chart readings", "Rows as recorded by 099r", "F-28, F-31, F-32, F-34"],
    ["X-12", "docs/model-v3/inputs.md rows I-W3a to I-W3d, I-W1c", "Fagereng et al.; Bangham and Leslie 2020 (source PDFs not held)", "Norway 2005-15; GB 2008-22", "Households", "As the register text", "Wealth rank", "Figures not verifiable from held files", "No", "F-28 to F-32"],
]
with open(os.path.join(HERE, "flows_crosswalk.csv"), "w", newline="") as f:
    csv.writer(f).writerows(X)
print("register rows", len(REG), "crosswalk rows", len(X) - 1)
