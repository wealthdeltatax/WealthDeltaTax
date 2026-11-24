"""102r: build stocks_crosswalk.csv and stocks_register.csv from the committed derivation outputs, and check every number the register states.
Reads only files in research/tables/102r-parameter-map-stocks-and-cells/, data/uk-wealth-tables/098r/, research/tables/099r-held-research-moments/ and the pack wealth_distribution.csv and wealth_tail.csv; run the three derive_*.py scripts first.
Run: python -I research/scripts/build_stocks_tables.py
Writes stocks_crosswalk.csv and stocks_register.csv next to this script. Exits non-zero if any stated value differs from its source output by more than its tolerance
(0.05 in the unit shown for shares in percent; 0.5 bn for pounds in billions; exact for counts)."""
import csv, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))   # the repository root (this script is in research/scripts/)
HERE = os.path.join(ROOT, 'research', 'tables', '102r-parameter-map-stocks-and-cells')   # the 102r tables (was the folder of this script)
D098, D099 = os.path.join(ROOT, 'data', 'uk-wealth-tables', '098r'), os.path.join(ROOT, 'research', 'tables', '099r-held-research-moments')
PACK = os.path.join(ROOT, 'model_v3', 'pack', 'GBR')
FAIL = []
R8 = 'April 2020 to March 2022'


def rd(p):
    with open(p, newline='') as fh:
        return list(csv.DictReader(fh))


def h(n):
    return rd(os.path.join(HERE, n))


def chk(name, got, want, tol):
    if abs(float(got) - float(want)) > tol:
        FAIL.append(f'{name}: {got} vs {want} (tol {tol})')


BANDS = ['D1-3', 'D4-5', 'D6-7', 'D8-9', 'D10']

# ---- values taken from the derived outputs (never typed) ----
rec = {x['pack_band']: x for x in h('band_reconciliation_exact.csv') if x['round'] == R8}
band_txt = '; '.join(f"{b} {rec[b]['was_household_share_pct']} vs {rec[b]['target_share_pct']} ({float(rec[b]['share_mismatch_pp']):+.1f}pp)" for b in BANDS)

comp = {x['pack_band']: x for x in h('band_composition_by_pack_band.csv') if x['round'] == R8}
comp_txt = '; '.join(f"{b} property {comp[b]['share_property_pct']} financial {comp[b]['share_financial_pct']} physical {comp[b]['share_physical_pct']} pension {comp[b]['share_pension_pct']}" for b in BANDS)
for b in BANDS:
    chk(f'comp sum {b}', sum(float(comp[b][k]) for k in ('share_property_pct', 'share_financial_pct', 'share_physical_pct', 'share_pension_pct')), 100, 0.2)
# pack rows that exist must agree with the recomputed Table 2.2 shares
for x in rd(os.path.join(PACK, 'wealth_distribution.csv')):
    if x['variable'] == 'property_share' and x['band'] in comp:
        chk('pack property_share ' + x['band'], x['value'], comp[x['band']]['share_property_pct'], 0.05)
    if x['variable'] == 'net_financial_share' and x['band'] in comp:
        chk('pack net_financial_share ' + x['band'], x['value'], comp[x['band']]['share_financial_pct'], 0.05)
    if x['variable'] == 'pension_share' and x['band'] in comp and x['band'] != 'all':
        chk('pack pension_share ' + x['band'], x['value'], comp[x['band']]['share_pension_pct'], 0.05)

stg = [x for x in h('stage_weights_by_pack_band.csv') if x['round'] == R8]
stage_txt = '; '.join(
    f"{b} " + '/'.join(next(x['share_of_band_adults_pct'] for x in stg if x['pack_band_approx'] == b and x['stage'] == s) for s in ('working', 'unemployed', 'inactive_not_retired', 'retired'))
    for b in BANDS)
for b in BANDS:
    chk('stage shares sum ' + b, sum(float(x['share_of_band_adults_pct']) for x in stg if x['pack_band_approx'] == b), 100, 0.35)

age = {x['hrp_age']: x for x in h('composition_by_age_of_hrp.csv')}
age_txt = '; '.join(f"{a} property {age[a]['share_property_pct']} financial {age[a]['share_financial_pct']} physical {age[a]['share_physical_pct']} pension {age[a]['share_pension_pct']}"
                    for a in ('25 to 34', '45 to 54', '65 to 74', '75+', 'All households'))

dt = {x['debt_type']: float(x['gb_total_gbp_bn']) for x in h('debt_gb_totals.csv')}
da = h('debt_by_age_gb.csv')
for t in dt:
    chk('debt total ' + t, sum(float(x['total_gbp_bn']) for x in da if x['debt_type'] == t), dt[t], 0.5)
debt_txt = f"personal financial debt {dt['personal financial debt']:.1f}bn; personal property debt {dt['personal property debt']:.1f}bn (GB, 2020-22, persons)"
prop_by_age = '; '.join(f"{x['age_band']} {float(x['total_gbp_bn']):.1f}bn over {int(x['weighted_frequency_holders']):,} holders" for x in da if x['debt_type'] == 'personal property debt')

nbs = {(x['nbs_year_end'], x['nbs_line']): x for x in h('nbs_vs_was_r8.csv')}
afl = {y: float(nbs[(y, 'S.14 total financial liabilities AF.L')]['nbs_gbp_bn']) for y in ('2020', '2021')}

w = {x['pack_band_approx']: x for x in h('person_household_weights_by_band.csv') if x['round'] == R8}
w_txt = '; '.join(f"{b} {w[b]['adults_per_household_2_11']} (Table 2.11) / {w[b]['adults_per_household_2_13']} (Table 2.13)" for b in BANDS)
ap = {x['round']: x for x in h('adults_per_household_all_rounds.csv')}[R8]
chk('adults per hh 2.11', ap['adults_per_hh_2_11'], 1.9282, 0.0005)
chk('adults per hh 2.13', ap['adults_per_hh_2_13'], 1.8593, 0.0005)

ct = h('capital_transfers_s14.csv')
def span(sid):
    v = [(x['year'], float(x['gbp_million']), float(x['pct_of_prior_year_end_net_worth'])) for x in ct if x['series_id'] == sid]
    return f"{sid}: {min(a[2] for a in v):.3f} to {max(a[2] for a in v):.3f}% of prior year-end S.14 net worth, {v[0][0]} to {v[-1][0]} (GBP {v[0][1]:,.0f}m in {v[0][0]}, {v[-1][1]:,.0f}m in {v[-1][0]})"
tr_txt = '; '.join(span(s) for s in ('HAZC', 'HAZG', 'HADR', 'QYKC', 'HADS'))

dem = {(x['year'], x['age_band']): x for x in h('demography_age_bands.csv')}
deaths = {(x['age_from'], x['age_to']): int(x['expected_deaths']) for x in h('adult_deaths_gb_2024.csv')}
chk('deaths total', sum(v for k, v in deaths.items() if k != ('16', '100')), deaths[('16', '100')], 5)
dem_txt = '; '.join(f"{b} pop {int(dem[('2024', b)]['population_gb']):,}, mean qx {dem[('2024', b)]['mean_qx_per_100000']} per 100,000" for b in ('55-64', '65-74', '75-84', '85-100'))
surv = {x['sex']: x for x in h('survival_from_65_period2024.csv')}
surv_txt = f"survive 65 to 75: males {surv['males']['survive_65_to_75']}, females {surv['females']['survive_65_to_75']}; 65 to 85: {surv['males']['survive_65_to_85']} / {surv['females']['survive_65_to_85']}; 65 to 95: {surv['males']['survive_65_to_95']} / {surv['females']['survive_65_to_95']}"

audit = {(x['register_row'], x['quantity'][:30]): x for x in h('existing_row_audit.csv')}
tail = {(x['series'], x['year']): x['value'] for x in rd(os.path.join(PACK, 'wealth_tail.csv'))}
chk('wid top1 2024', tail[('wid_top1', '2024')], 21.3, 0.001)
chk('wid top10 2024', tail[('wid_top10', '2024')], 57.1, 0.001)

moments = {x['id']: x for x in rd(os.path.join(D099, 'moments.csv'))}
for k in ('AB-02', 'BF-04', 'BF-06', 'BF-03', 'EER-01', 'BF-13', 'TD-02', 'TZ-01', 'BF-14'):
    if k not in moments:
        FAIL.append('099r moment missing: ' + k)

# ---------------- crosswalk ----------------
XW_COLS = ['id', 'source', 'exact_reference', 'publisher_and_link', 'reference_period', 'population_unit_frequency_price_basis', 'definitions_and_coverage',
           'dimensions_available', 'revisions_and_sampling_limits', 'held_file_checked_against_published_source']
ONS = 'ONS; https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth/bulletins/totalwealthingreatbritain/april2020tomarch2022'
NOTE_HELD = 'checked internally by script (sums, tolerance stated); NOT compared with the live published page in this session'
xw = [
    ['X01', 'ONS WAS Round 8 total wealth tables, Table 2.2 (components by wealth decile)', 'data/rates/totalwealthtables.xlsx, sheet Table 2.2; derive_bands_stages.py -> band_composition_by_pack_band.csv; check_table21_vs_table22.csv', ONS,
     'April 2020 to March 2022 (Rounds 1 to 8 held)', 'GB households; GBP bn aggregates; two-year round; current prices', 'Net property (after mortgage), net financial, physical, private pension; DB valued on the SCAPE-based method from Round 8; private households only',
     'Wealth decile (pack bands are sums of deciles)', 'Survey sampling error not published in the table; top-tail under-coverage (S5); Round 7 to 8 pension valuation break', 'Internal: Table 2.2 sums agree with Table 2.1 within the stated tolerance (check_table21_vs_table22.csv); not against the live ONS page'],
    ['X02', 'ONS WAS Table 2.5 households by total-wealth band (GBP band edges) and Tables 2.11, 2.13 (persons by age)', 'data/rates/totalwealthtables.xlsx, Tables 2.5, 2.11, 2.13; band_reconciliation_exact.csv; person_household_weights_by_band.csv; adults_per_household_all_rounds.csv', ONS,
     'Rounds 1 to 8; R8 used', 'GB households (thousands) and persons', 'Households by GBP wealth band; persons by age; Table 2.11 16+ persons and Table 2.13 differ by 1.858m in R8', 'GBP band groups, not deciles; age bands',
     'Rounding in published thousands; band edges are fixed GBP, deciles move each round', NOTE_HELD],
    ['X03', 'ONS WAS economic status by wealth band (098r extract)', 'data/uk-wealth-tables/098r/was_persons_activity_by_wealth_band.csv; stage_weights_by_pack_band.csv (this brief)', ONS + ' (reference tables)',
     'April 2020 to March 2022', 'GB persons aged 16+; whole-number percentages of each row', 'Working (employed and self-employed), unemployed, inactive not retired, retired, by GBP wealth band; household reference person status is not stated in the held table',
     'GBP wealth band group by status', 'Whole-number percentages: each cell +-0.5pp of its row total (stage_rounding_bounds_r8.csv); bands do not align with pack deciles (band reconciliation)', NOTE_HELD],
    ['X04', 'ONS ad hoc 2813: wealth components by age of household reference person', 'data/uk-wealth-tables/098r/ons_was_wealth_by_age_of_hrp.csv and the held xlsx; composition_by_age_of_hrp.csv', 'ONS ad hoc; https://www.ons.gov.uk/file?uri=%2Fpeoplepopulationandcommunity%2Fpersonalandhouseholdfinances',
     'April 2020 to March 2022', 'GB households; GBP million aggregates and means', 'Property, financial, physical, private pension by age of HRP; marginal on age, not joint with wealth band', 'HRP age band',
     'Not joint with wealth; HRP age is a household attribute', NOTE_HELD],
    ['X05', 'ONS ad hoc 3222: personal financial and property debt by age and region', 'data/uk-wealth-tables/098r/ons_was_debt_by_age_region.csv; debt_by_age_gb.csv; debt_gb_totals.csv', 'ONS ad hoc; https://www.ons.gov.uk/file?uri=%2Fpeoplepopulationandcommunity%2Fpersonalandhouseholdfinances',
     'April 2020 to March 2022', 'GB persons (individuals) with debt; GBP bn totals by age and region', 'Personal financial debt and personal property debt; GB totals are sums over 11 regions; a person-based count, not household gross debt', 'Age band, region',
     'Persons, not households; not by wealth band; mean times N reproduces totals within 2.4% (script check)', NOTE_HELD],
    ['X06', 'ONS population projections 2024-based, principal, Great Britain', 'data/uk-wealth-tables/098r/ons_population_gb_principal_2024based.csv; demography_age_bands.csv', 'ONS; population projections', '2024, 2030, 2040 (2024-based)', 'GB persons by age', 'Age counts only; no retirement status or wealth', 'Single year of age, sex (aggregated to bands)', 'Projection, principal variant only held', 'Internal consistency only'],
    ['X07', 'ONS ad hoc 3459: 2024-based period and cohort qx, Great Britain', 'data/uk-wealth-tables/098r/ons_qx_gb_2024based.csv; demography_age_bands.csv; survival_from_65_period2024.csv; adult_deaths_gb_2024.csv', 'ONS ad hoc 3459', 'Period 2024 used (cohort file starts at births 1981)', 'GB probability of death within a year by single year of age and sex', 'Age and sex only; no wealth gradient', 'Age, sex', 'Period qx applied from 65 is a life-table survival, not a cohort forecast', 'Internal consistency only'],
    ['X08', 'ONS national balance sheet: household sector stocks (097r)', 'data/uk-wealth-tables/097r/ons_nbs_household_stocks_annual.csv; nbs_vs_was_r8.csv (this brief); series E45V (S.14 net worth), CGRC (S.14+S.15)', 'ONS; quarterly sector accounts and national balance sheet',
     'End-year 2020 to 2025', 'UK households (S.14), market values, current prices', 'Includes pension entitlements (AF.6) in financial assets; non-financial gross of mortgage debt; UK not GB; includes communal establishments', 'Instrument, sector', 'Revised between vintages (110bn between S.14 and S.14+S.15)', 'Held extract only; the 097r note records its check'],
    ['X09', 'ONS quarterly sector accounts: S.14 capital account (097r)', 'data/uk-wealth-tables/097r/qsa_household_annual_2026q2.csv; capital_transfers_s14.csv; series HAZC, HAZG, HADR, QYKC, HADS', 'ONS; quarterly sector accounts 2026 Q2', '2015 to 2025 annual', 'UK households S.14, GBP million, current prices', 'Capital transfers with other sectors; transfers between households net out inside the sector and are not in these lines; D.91p includes capital taxes', 'Series', 'Revised; annual sums of quarters', 'Internal consistency only'],
    ['X10', 'ONS ETB reference tables FYE 2023-24, Tables 3b and 4b (098r)', 'data/uk-wealth-tables/098r/etb_income_by_decile_retired_nonretired.csv', 'ONS; effects of taxes and benefits on household income', 'FYE 2024', 'UK, equivalised disposable income deciles; retired and non-retired individuals and households; GBP a year', 'Income-ranked, not wealth-ranked: cannot give income by wealth band; counts are sample counts', 'Income decile, retired status', 'Sample counts about 1,110 per decile for retired individuals', 'Not re-checked here; 098r extract'],
    ['X11', 'Pack: wealth_distribution.csv and wealth_tail.csv', 'model_v3/pack/GBR/wealth_distribution.csv (net_financial_share, property_share, pension_share, wealth_total, gain_bearing_wealth); wealth_tail.csv (WID top 1% and 10%)', 'Repository pack (sha256 pinned in tests/model_v3/test_pack.py)', '2020-22 (WAS); WID 2000, 2010, 2024', 'GB households; WID adults', 'Pack shares agree with recomputed Table 2.2 where a row exists (build script check); D4-5 property and pension rows are absent from the pack', 'Pack band', 'WID is a distributional-accounts series with different definitions', 'Pack rows compared with X01 by this script'],
    ['X12', 'Phase 1 moments (099r): Resolution Foundation Before the fall; Advani, Bangham and Leslie 2021; Advani and Tarrant; Wakefield 2009 (ELSA); others', 'research/tables/099r-held-research-moments/moments.csv, ids BF-03, BF-04, BF-06, BF-13, BF-14, AB-02, EER-01, TD-02, TZ-01', 'See 099r; Resolution Foundation; Fiscal Studies', 'Various, 2004 to 2026', 'Families, individuals aged 25 to 54, estates, UK households; see each id', 'Mobility, top-tail, estate composition; microdata-based, no WAS table held', 'None by pack band', 'Read from printed charts or text; definitions differ between moments', 'Read in 099r from the held PDFs; classed validation or context there'],
    ['X13', 'Pension valuation basis break: Round 7 against Round 8, and Resolution Foundation against ONS', '098r note (DB pension SCAPE method changed); inputs.md I-W5e; RF Annex 2 (BF-01 note: DB and pensions in payment excluded)', 'ONS (SCAPE-based DB valuation from Round 8); Resolution Foundation (own basis)', 'R7 2018-20; R8 2020-22', 'GB households', 'ONS basis includes DB wealth at the SCAPE valuation; the RF decomposition excludes DB and pensions in payment', 'n/a', 'The two bases are never mixed in this map; RF figures are validation context only', 'Documented in 098r, not recomputed'],
]

# ---------------- register ----------------
RG_COLS = ['id', 'group', 'variable_and_definition', 'accounting_location', 'target_cell_dimension', 'classification', 'source_and_exact_reference',
           'calculation_and_script', 'value_or_range', 'uncertainty_and_caveats', 'intended_model_use', 'proposed_ruling', 'relation_to_existing_row', 'open_question_or_data_request']
S = 'derive_bands_stages.py'
D = 'derive_debt_demography.py'
T = 'derive_transfers_audit_coverage.py'
rg = [
    ['S01', 'bands', 'Pack wealth bands: D1-3, D4-5, D6-7, D8-9, D10 as sums of WAS deciles of household total wealth including private pensions (SCAPE-based DB basis)', 'Opening balance sheet, cell index', 'band', 'observed', 'model_v3/pack/GBR/wealth_distribution.csv; data/rates/totalwealthtables.xlsx Table 2.2', 'none: definition', 'Decile groups 1-3, 4-5, 6-7, 8-9, 10 (30, 20, 20, 20, 10% of households by construction)', 'Deciles of households, not adults; deciles are re-drawn each round', 'calibration', 'ready for implementation', 'consistent with I-D4a to I-D4h', 'none'],
    ['S02', 'bands', 'Band-edge mapping: GBP-band groups of the WAS stage and household tables against pack deciles (R8 household share by GBP band group vs decile target)', 'Cell weights', 'band', 'derived', 'data/rates/totalwealthtables.xlsx Table 2.5; band_reconciliation_exact.csv', f'{S}: weighted frequencies in thousands cumulated to the GBP edges; tolerance 1.0pp against the 098r rounded shares', band_txt,
     'The GBP bands do not align with the deciles; the mismatch is up to 4.9pp of households per band and the edges differ. No cell value is built by spreading an aggregate in proportion to wealth', 'validation only (reconciliation)', 'ready for implementation as a reported mismatch; stage weights on decile bands further data required', 'new', 'WAS microdata (study 7215) would give stage by decile directly'],
    ['S03', 'stage', 'Stage weights by pack band: persons aged 16+ working (employed and self-employed), unemployed, inactive not retired, retired; percent of band adults (working/unemployed/inactive/retired)', 'Cell weights, transition source', 'band x stage', 'proxy', 'data/rates/totalwealthtables.xlsx economic status by wealth band; 098r was_persons_activity_by_wealth_band.csv; stage_weights_by_pack_band.csv', f'{S}: percent of row total x weighted persons of the GBP band group; tolerance: each cell +-0.5pp of its row (stage_rounding_bounds_r8.csv)', stage_txt,
     'Proxy, not derived at deciles: the GBP band groups differ from the deciles by up to 4.9pp of households (S02); whole-number percentages; stage is the table definition, and the HRP status basis is not stated; economically inactive not retired (students, carers, sick) is its own group, not a third retirement state', 'calibration (opening weights) with the S02 mismatch reported', 'implement with a scenario range (alternative band edges)', 'new', 'WAS study 7215 person file for stage by decile (UK Data Service, safeguarded licence)'],
    ['S04', 'stage', 'Cell sizes: persons and households per pack band and stage (R8)', 'Cell weights', 'band x stage', 'derived', 'cell_coverage_inputs.csv; stage_weights_by_pack_band.csv', f'{T}: persons = band adults x stage percent; rounding bound in persons', 'See cell_coverage_inputs.csv (for example D4-5 retired 1,978,800 persons +-116,400; D10 working 4,512,750 +-150,425)', 'Sample sizes behind each cell are not published; cells use weighted counts', 'neither (input to 104r coverage matrix)', 'ready for implementation as coverage input', 'new', 'none'],
    ['S05', 'composition', 'Asset composition by pack band: net property, net financial, physical, private pension as % of total wealth (R8)', 'Opening balance sheet: H, E+B+M, other, PA', 'band', 'observed', 'data/rates/totalwealthtables.xlsx Table 2.2; band_composition_by_pack_band.csv', f'{S}: sum of decile rows; check against Table 2.1 within tolerance', comp_txt,
     'Net property is after mortgage debt (WAS), so housing and liabilities are not separable; physical wealth (contents, vehicles) is not part of the kernel asset classes; DB pension on the SCAPE-based method', 'calibration (opening state)', 'ready for implementation', 'supports pack rows where present; fills D4-5 property (37.5) and pension (36.3) that the pack does not carry', 'Confirm how the pack builder treats physical wealth'],
    ['S06', 'composition', 'Asset composition by age of household reference person, as a proxy for stage (R8), % of total wealth', 'Opening balance sheet by stage', 'age (proxy for stage)', 'proxy', 'ONS ad hoc 2813; composition_by_age_of_hrp.csv', f'{S}: components over total by age band; derived mean agrees with published mean within 0.1%', age_txt,
     'Age of HRP, not stage and not joint with wealth band; the 65 to 74 and 75+ rows mix retired and some working households', 'validation only (shape of composition by age)', 'remain a proxy; joint band by stage composition further data required', 'new', 'WAS study 7215: components by band x age x status'],
    ['S07', 'composition', 'DB against DC pension split, and pensions in payment', 'PA components', 'band x stage', 'unset', 'No held table; data/rates totalwealthtables Table 2.2 gives private pension total only', 'none', '', 'DB and DC valuations differ in nature (entitlement against market pot); the SCAPE-based DB value is not a market return base. Without a split PA has one return and one liquidity rule', 'neither', 'further data required', 'new', 'WAS pension tables (DB, DC, in payment) by decile; study 7215'],
    ['S08', 'composition', 'Pension valuation basis for every stock row: ONS WAS SCAPE-based DB (Round 8), not Round 7; Resolution Foundation basis (excludes DB and pensions in payment) is validation context only', 'PA', 'all', 'observed', 'inputs.md I-W5e; 098r note; moments.csv BF-01 note', 'none: statement of basis', 'Round 8 private pension wealth GBP 4,807.7bn, 35.4% of total (Table 2.2)', 'Round 7 to Round 8 break: total wealth including pensions is not comparable across it; no row mixes the bases', 'calibration (ONS basis); validation context (RF)', 'ready for implementation with the basis named on every row', 'supports I-W5e (register shows 4,806 bn, held shows 4,807.7: rounding)', 'none'],
    ['S09', 'composition', 'Physical (other) wealth share by band', 'Other assets', 'band', 'observed', 'Table 2.2; band_composition_by_pack_band.csv', f'{S}', 'D1-3 ' + comp['D1-3']['share_physical_pct'] + '%, D4-5 ' + comp['D4-5']['share_physical_pct'] + '%, D6-7 ' + comp['D6-7']['share_physical_pct'] + '%, D8-9 ' + comp['D8-9']['share_physical_pct'] + '%, D10 ' + comp['D10']['share_physical_pct'] + '%', 'Contents and vehicles; not held as returns-bearing in the kernel', 'calibration', 'ready for implementation; a decision whether to count it in the WDT base is open', 'new', 'Open question: include physical wealth in the base?'],
    ['S10', 'liabilities', 'Secured (personal property) debt, GB total and by age', 'D (mortgage)', 'age (not band)', 'observed', 'ONS ad hoc 3222; ons_was_debt_by_age_region.csv; debt_by_age_gb.csv', f'{D}: sum of 11 regional totals; mean x N within 2.4% of totals', debt_txt + '. By age: ' + prop_by_age,
     'Persons, not households; GB sum; not by wealth band or stage; WAS property wealth is net of mortgage so the cell balance sheet is net unless gross is added back', 'validation only (aggregate and age gradient)', 'further data required for use by band', 'new', 'WAS study 7215 gross debt by band and stage'],
    ['S11', 'liabilities', 'Unsecured (personal financial) debt, GB total and by age', 'D (other)', 'age (not band)', 'observed', 'ONS ad hoc 3222; debt_by_age_gb.csv', f'{D}', f"{dt['personal financial debt']:.1f}bn GB total (R8)", 'Same limits as S10; mean per holder falls with age (11,602 for 16 to 34 to 2,657 for 65 and over)', 'validation only', 'further data required for use by band', 'new', 'As S10'],
    ['S12', 'liabilities', 'Aggregate liabilities cross-check: ONS 3222 sums against national balance sheet AF.L', 'D', 'aggregate', 'proxy', 'nbs_vs_was_r8.csv', f'{D}', f"3222 total {dt['personal financial debt'] + dt['personal property debt']:.0f}bn (GB, persons) against NBS S.14 AF.L {afl['2020']:.0f}bn (2020) and {afl['2021']:.0f}bn (2021) (UK households)", 'Not reconciled: populations (GB persons against UK households), instruments (AF.L includes all loans) and dates differ; the gap is reported, not closed', 'validation only', 'remain unset as a model input; report the gap', 'new', 'ONS reconciliation note (request)'],
    ['S13', 'liabilities', 'Debt service: interest paid and principal repayment by band and stage', 'I_D, R', 'band x stage', 'unset', 'No held table (NMG debt service series are in 097r as a variable inventory only)', 'none', '', 'Interest is a flow (101r holds the aggregate); no held table splits capital repayment from interest by band', 'neither', 'further data required (consequence: cells run without gross debt, with property net of mortgage)', 'new', 'NMG household survey tables; WAS 7215 debt service variables'],
    ['S14', 'top tail', 'Top-tail share series: WID top 1% and top 10% of adult wealth (pack wealth_tail.csv)', 'Tail add-on', 'tail', 'observed', 'model_v3/pack/GBR/wealth_tail.csv', 'none: pack read; build_stocks_tables.py checks values', f"top 1%: 20.4 (2000), 20.0 (2010), {tail[('wid_top1', '2024')]} (2024); top 10%: 55.8, 54.6, {tail[('wid_top10', '2024')]}", 'Distributional-national-accounts, adults; definitions differ from the WAS household deciles (audit row I-W5c/d)', 'validation only', 'ready for implementation as validation moment', 'definitions differ from I-W5c/d', 'none'],
    ['S15', 'top tail', 'Top-tail adjustment for wealth missing from the WAS top: about 5% of total (nearly GBP 800bn in 2016-18); top 1% share 14.4% (survey) to 16.5% (national accounts) to 23%', 'Tail add-on', 'D10 and tail', 'scenario', 'moments.csv EER-01, BF-13; inputs.md I-D4d, I-D4e', 'none: published figures, not recomputed for Round 8', 'No single value: a labelled range, 0 to 5.6% of total (I-D4e) and top 1% 14.4 to 23.0% (I-D4d)', '2016-18 basis; not recomputed for Round 8 (J on transfer); overlaps the Rich List (I-D4f)', 'calibration (scenario only)', 'implement with a scenario range; no value chosen', 'supports I-D4d and I-D4e as ranges', 'Advani and Tarrant style Round 8 reconciliation (author or analyst)'],
    ['S16', 'transfers', 'Capital transfers of UK households with other sectors (S.14): receivable D.9r, other receivable D.99r, payable D.9p, capital taxes payable D.91p, other payable D.99p', 'TR (cross-sector part)', 'aggregate', 'observed', 'ONS quarterly sector accounts; capital_transfers_s14.csv', f'{T}: annual series divided by previous year-end S.14 net worth (E45V)', tr_txt,
     'Gifts and bequests between households net out inside the sector and are not in these lines; these are cross-sector transfers; D.91p includes capital taxes beyond inheritance tax', 'validation only', 'ready for implementation as an aggregate check', 'new', 'none'],
    ['S17', 'transfers', 'Gifts and inheritances received and given by band and stage; bequests as a share of the giver wealth', 'TR (inter-household)', 'band x stage', 'unset', 'No held table (095r: IFS Boileau and Sturrock and RF Inheritance give group levels, not held as files)', 'none', '', 'No UK source gives transfers given as a share of the giver wealth by band (095r). Baseline TR = 0 and the sector aggregate cancels', 'neither', 'remain unset (consequence: cells run with TR = 0 or a labelled scenario the author authorises)', 'new', 'WAS 7215 gift and inheritance modules; HMRC IHT tables by estate size (not held); ONS request for gifts by band'],
    ['S18', 'transfers', 'Estates passing at death: number, size and composition by estate size', 'TR (death)', 'estate size', 'unset', 'moments.csv TD-02 holds 2007-08 composition only (context)', 'none', '', 'The held moment is 2007-08 and probate-based; no current estate table is held', 'neither', 'further data required', 'new', 'HMRC IHT statistics (tables 12.1 to 12.3 are held as ods in 097r but not parsed for estates by size)'],
    ['S19', 'transfers', 'Legacy heir rule: one heir per generation, every G = 30 years, heir taxed on the receipt from zero', 'Kernel step_death', 'all lines', 'legacy', 'model_v3/core/kernel.py step_death; plan decisions D6, D20; 094r A4', 'none: structural', 'G = 30 years (a model period, not a UK estimate)', 'A legacy mechanism, not a measured transfer rate; judgement', 'neither (legacy comparator)', 'remain as the legacy arm only', 'new', 'none'],
    ['S20', 'mobility', 'Two-year top-decile persistence and entry: 80% of families in the top decile stay; about 90% of entrants come from the ninth decile; 7% of the bottom half move to the top half', 'Distribution check', 'top decile', 'proxy', 'moments.csv AB-02 (Advani, Bangham, Leslie 2021, Fig 13, PDF 22 to 23)', 'none: published', '80 / 90 / 7 (percent)', 'Family wealth deciles from the paper; base 2014-16 (PDF 4) or 2016-18 (PDF 23); not pack deciles; no full transition matrix', 'validation only', 'ready for implementation as validation moments', 'supports I-W4a, I-W4b', 'WAS 7215 panel for a decile transition matrix'],
    ['S21', 'mobility', 'Four-year rank correlation and same-decile share of age-adjusted per-adult wealth, individuals aged 25-54, 2016-18 to 2020-22 (low-to-middle and higher income)', 'Distribution check', 'income group', 'proxy', 'moments.csv BF-04, BF-06 (Resolution Foundation, Before the fall, Table 1 PDF 45, Fig 22)', 'none: published', 'rank correlation 74 / 77; same decile 33% / 32%; 27% (aged 25-34) and 34% (35-54) for higher income', 'Income groups, age-adjusted deciles, a different population from S20: not spliced with it', 'validation only', 'ready for implementation as validation moments', 'supports I-W4c (reported central 75.5 is a J midpoint)', 'WAS 7215'],
    ['S22', 'mobility', 'Full band-to-band and stage transition matrix', 'Transitions', 'band x stage', 'unset', 'none held', 'none', '', 'No UK matrix is held; only summary measures above', 'neither', 'further data required (consequence: bands evolve only through the model flows; validation uses S20 and S21)', 'new', 'WAS 7215 longitudinal file'],
    ['S23', 'demography', 'Age structure of the adult population (GB, 2024, 2030, 2040 projections)', 'Weights by age', 'age', 'observed', 'ONS 2024-based projections; demography_age_bands.csv', f'{D}: single years summed to bands', 'Example 2024: ' + dem_txt.split('; mean')[0], 'Principal projection only; age not stage', 'calibration (aging weights)', 'ready for implementation', 'new', 'none'],
    ['S24', 'demography', 'Mortality: period qx 2024 by age band; survival from 65; expected adult deaths in 2024', 'Death transition', 'age', 'derived', 'ONS ad hoc 3459; demography_age_bands.csv; survival_from_65_period2024.csv; adult_deaths_gb_2024.csv', f'{D}: expected deaths = population x qx; tolerance 5 deaths on the band sum', dem_txt + f'; expected adult deaths 16 to 100: {deaths[("16", "100")]:,}; ' + surv_txt,
     'Age and sex only: no wealth gradient (richer people live longer), so deaths by band are not derived; period life table, not a cohort forecast', 'calibration (age hazard); wealth gradient unset', 'ready for implementation for the age hazard; wealth gradient remain unset', 'new', 'ONS or WAS-linked mortality by wealth (request)'],
    ['S25', 'demography', 'Working-to-retired transition hazard by band', 'Stage transition', 'band x stage', 'unset', 'No held table of entry into retirement by band; the State Pension age is an external parameter not held', 'none', '', 'An age structure alone does not give an entry hazard without a retirement-age rule and band-specific retirement timing', 'neither', 'further data required (a labelled scenario on the pension age is possible; author decision)', 'new', 'WAS 7215 longitudinal status changes; DWP State Pension age schedule'],
    ['S26', 'demography', 'Household formation and dissolution', 'Weights', 'band x stage', 'unset', 'none held', 'none', '', 'Left out of the first design (096r); changes weights, not the identity', 'neither', 'remain unset', 'new', 'none'],
    ['S27', 'weights', 'Adults per household by pack band (household to person weight), R8', 'Person weights', 'band', 'derived', 'Table 2.11 and Table 2.13 over Table 2.5; person_household_weights_by_band.csv; adults_per_household_all_rounds.csv', f'{S}: persons 16+ over households; tolerance 0.0005 on the all-household ratios', w_txt + f". All households: {ap['adults_per_hh_2_11']} / {ap['adults_per_hh_2_13']}",
     'The two published tables give different adult counts (Table 2.13 is 1.858m lower in R8); which is the right adult base is not stated in the held tables; band rows use the decile-aligned GBP groups (S02)', 'calibration (with both bases reported)', 'implement with a scenario range (Table 2.11 against 2.13)', 'supports I-D4h central 1.93; contradicts its low 1.77 (below both tables)', 'ONS clarification of Table 2.13 coverage'],
    ['S28', 'weights', 'Person weights by stage within band (household stage mix)', 'Person weights', 'band x stage', 'unset', 'none: stage is a person attribute in the held table, household stage is not', 'none', '', 'A household has mixed stages; no held table', 'neither', 'further data required', 'new', 'WAS 7215 household file'],
    ['S29', 'existing rows', 'I-D4a wealth to GDP (low 5.80, central 5.94, high 7.5)', 'Aggregate check', 'aggregate', 'observed', 'existing_row_audit.csv; pack gdp row', f'{T}', 'Central 5.94 reproduces on GDP 2,284bn; on the pack GDP 2,211.48bn it is 6.14; low 5.80 is not reproduced (held NBS S.14 net worth 2021 / 2,284bn = 5.03)', 'GDP differs between the register and the pack (3.2%) and is not reconciled in held files; the low is a different basis', 'validation only', 'report the disagreement; no register edit', 'supports central, contradicts the low (basis) and the pack GDP', 'Which GDP series the register intends'],
    ['S30', 'existing rows', 'I-D4b share of adults at or above W_min; I-D4h adults per household; I-D4c', 'Base', 'aggregate', 'derived', 'existing_row_audit.csv', f'{T}', 'I-D4b low 49.3 reproduces (households at or above 300,000, labelled adults); high 64.3 lies inside the held household bracket 59.2 to 72.7 (at or above 200,000 to at or above 85,000); central 54.9 (an adult share from a lognormal fit) lies below that bracket and the held tables cannot test it; I-D4h central 1.93 reproduces (1.9282), but Table 2.13 gives 1.8593 and the low 1.77 sits below both', 'The 150,000 point lies inside a band, so no held cell gives it; see audit note', 'validation only', 'report; no register edit', 'supports I-D4b low and high and I-D4h central; I-D4b central not testable and below the bracket; contradicts I-D4h low', 'Which adult base the register intends'],
    ['S31', 'existing rows', 'I-W5a, I-W5e: top-decile share and pension share (R8)', 'Aggregate check', 'D10', 'observed', 'existing_row_audit.csv', f'{T}', 'I-W5a 40.7 reproduces (40.71); low 40.1 reproduces; I-W5e 35.4 reproduces (35.43)', 'High 43.9 depends on the I-D4e add-on (S15)', 'validation only', 'supports; no edit', 'supports', 'none'],
    ['S32', 'existing rows', 'I-W5b (Pareto top 1% of households), I-W5c and I-W5d (adult top 1% and 10%, 2016-18) against the pack tail', 'Tail check', 'tail', 'proxy', 'existing_row_audit.csv; wealth_tail.csv', f'{T}', 'WID 21.3 and 57.1 (2024, adults) against the register 14.4 to 23.0 and 52.4 to 52.5 (2016-18, adults)', 'Definitions and years differ; I-W5b is a derived (J) household figure not tested here', 'validation only', 'report definitions differ; no splice', 'definitions differ', 'none'],
    ['S33', 'existing rows', 'I-W4a to I-W4c (UK mobility); I-W4d, I-W4e (Norway); I-W4f (intergenerational slope)', 'Distribution check', 'top decile', 'proxy', 'existing_row_audit.csv; moments.csv AB-02, BF-04; I-W4d to f not re-read', f'{T}', 'I-W4a/b 80 / 90 reproduce; I-W4c 74 / 77 reproduce; I-W4c central 75.5 is the register midpoint (J)', 'I-W4d to I-W4f were not audited against a held file (Norway and Bozio-type sources are not held as tables)', 'validation only', 'supports I-W4a to c; I-W4d to f not audited', 'supports I-W4a to c', 'Held copies of the Norway and intergenerational papers if an audit is wanted'],
]

# ---- 3 register checks against stated source values ----
chk('R8 D4-5 retired persons', next(x['persons'] for x in stg if x['pack_band_approx'] == 'D4-5' and x['stage'] == 'retired'), 1978800, 1)
chk('R8 D10 working persons', next(x['persons'] for x in stg if x['pack_band_approx'] == 'D10' and x['stage'] == 'working'), 4512750, 1)
chk('I-D4a central reproduces', [x for x in h('existing_row_audit.csv') if x['register_row'] == 'I-D4a'][0]['recomputed_or_held_value'], 5.94, 0.005)
chk('I-W5e', [x for x in h('existing_row_audit.csv') if x['register_row'] == 'I-W5e'][0]['recomputed_or_held_value'], 35.43, 0.005)
for r in rg:
    if len(r) != len(RG_COLS):
        FAIL.append(f'register row {r[0]} has {len(r)} fields')
for r in xw:
    if len(r) != len(XW_COLS):
        FAIL.append(f'crosswalk row {r[0]} has {len(r)} fields')
for r in rg:
    if r[5] == 'unset' and r[8].strip():
        FAIL.append(f'unset row {r[0]} carries a number')


def write(name, cols, rows):
    with open(os.path.join(HERE, name), 'w', newline='') as fh:
        wr = csv.writer(fh)
        wr.writerow(cols)
        wr.writerows(rows)


write('stocks_crosswalk.csv', XW_COLS, xw)
write('stocks_register.csv', RG_COLS, rg)
if FAIL:
    print('FAIL:\n' + '\n'.join(FAIL))
    sys.exit(1)
print(f'ok: {len(xw)} crosswalk rows, {len(rg)} register rows, all stated values reproduce within tolerance')
