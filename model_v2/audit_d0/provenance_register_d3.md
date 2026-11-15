# D3 provenance and status (ownership and scope share)

Date: 15 October 2026. Status: coverage census only; no series values extracted. Companion: `coverage_matrix_d3.csv`.
Role (spec): validation, not calibration. Hook: `scope_share_t` against the observed path. Gate: UK and US full series; others sparse benchmarks with interpolation.

## What was opened

| Source | Status | Opened |
|:---|:---|:---|
| DLUHC English Housing Survey 2013-14, Chapter 1 Trends in tenure | verified (text), data not extracted | Tenure rates at 1918-2013-14, source by period. Annex Table 1 behind Figure 1.1 not opened. |
| English Housing Survey live tables collection page | partly | Dataset names only ("tenure trends and cross tenure"; "owner occupiers, recent first time buyers and second homes"). No table IDs, years or formats. |
| FRED RHORUSQ156N (Census Bureau) | verified | Quarterly, Q1 1965 to Q2 2026, share of households owner-occupied. |
| dqydj historical homeownership page | partly | States 1890-present and that pre-1965 values were hand-transcribed from scanned censuses. Table not retrievable. |
| ONS Household total wealth in Great Britain, Apr 2020-Mar 2022 | verified | Unit, property-wealth definition, comparability notes. No time series extracted. |
| Eurostat ilc_lvho02 via DBnomics | partly | Structure and first ten series only. |
| Census mortgage-status question (UConn library page) | partly | ACS and 2010 census definition of free and clear. |
| Kennickell summary of the SCF 1989-2022 | partly | Waves, unit, wealth definition. No home-value tables. |
| Kohl (2017) publisher and MPIfG pages | partly | Scope only. No data link. |

## Findings

1. **UK ownership.** A 1918-2013 owner-occupation path exists: roughly 25% (1918), 32% (1953), 43% (1961), 51% (1971), 63% (2013-14), peak 71% (2006), with annual data from 1980. Of the 1939, 1981 and 1991 values the text gives only derivations. The outright/mortgage split is annual from 1980 (outright 33% in 2013-14, mortgagors 31%).
2. **US ownership.** The annual path starts only in 1965; the 1890-1960 decennial points exist but were not retrieved. The US outright-ownership span is unconfirmed.
3. **The third D3 variable cannot come from tenure series.** The share of adults above the median house value in net wealth needs micro or distributional data: UK WAS from 2006, US SCF from 1989 (triennial), euro-area HFCS not examined. There is no pre-2006 UK equivalent found, so this variable has no long history for the UK.
4. **Other countries.** Eurostat EU-SILC gives tenure from 2003 at the earliest, so benchmarks for those countries start in 2003-2010. Whether owner-with-mortgage is separated is unconfirmed. Japan, Australia and the Nordics beyond Denmark were not searched.

## Definition fidelity (principle 4)

- **Unit mismatch.** All observed ownership series are shares of households (EHS, Census) or of population (EU-SILC). The model's `scope_share_t` is a share of adults with W/idx at or above W_min. Comparison needs an adults-per-household conversion or a flagged household-basis diagnostic. This is the largest definitional gap.
- **Ownership vs scope.** Spec mapping is scope_share ≈ ownership × share of owners above W_min; the second factor is not observed over time except through WAS and SCF.
- **Net vs gross of mortgage.** Tracking full ownership, per the settled decision, ignores mortgages, so outright ownership is an upper-bound check on the net-wealth reading only.
- **Land coverage.** EHS is England only; WAS is Great Britain.

## Decisions (15 Oct)

1. **Validation tolerance (spec open item 3).** Still open. Meaning: a pass/fail band fixed before any run, for example "model scope_share_t within X percentage points of the observed value in each benchmark year". Not yet set.
2. **Basis (decided 15 Oct, superseded later the same day; see below).** Earlier: compare per household, flagged. Replaced by the per-adult rule below.
3. **UK geography: Great Britain, WAS (decided).** WAS starts 2006, so the long UK ownership path (1918 on) from the English Housing Survey stays only as a flagged England-only proxy outside the WAS years.

## Decisions (15 Oct, second round): per-adult basis and sharing parameter

The WDT is per adult with no exceptions. Wealth data are mostly household-based, so the audit adopts:

1. **Baseline unit.** Household wealth is divided equally among the household's adults (equal split). This is the data-minimal rule and equals the outcome of the intentional behaviour (assets shared between adults, each sitting lower on the rate curve or below W_min).
2. **Sharing parameter s** from 0 (as-owned, each adult holds what is in their own name) to 1 (equal split). Equal split is the baseline; as-owned is a sensitivity. Reported across the range as a stated scenario, not as an estimated behavioural response (spec section 7 keeps behavioural response out of scope). Needs individual ownership shares for s < 1: not yet located; WAS individual files hold individual pension and financial wealth, joint property treatment not checked.
3. **D3 observed target.** Share of adults living in an owner-occupier household (consistent with equal split), replacing the household ownership rate. Conversion from the household series needs adults per household by tenure (WAS or EHS tables; not yet opened). Adult age cut-off (WAS 16+ versus model convention) unconfirmed.
4. **Effect on the validation tolerance (still open).** The household/adult offset largely disappears, so the level tolerance shrinks to sampling noise plus the ownership-versus-scope gap and a level test becomes viable beside the change test. Proposal on the table, not adopted: primary test on the 10-year change (about plus or minus 5 points), secondary on level, three zones (pass within T, inconclusive T to 2T, fail beyond 2T), restricted to UK-history windows (US windows as a flagged cross-check), set and recorded before any run.
5. **Open design point (mechanism papers).** Treatment of a transfer between spouses under the WDT (UK IHT and CGT exempt spouse transfers), which decides whether splitting is free or costly; to check against the mechanism papers.

## Per-adult follow-up (15 Oct): what was found

Sources opened: EHS 2013-14 Chapter 2 (comparison of tenure groups) and a Women's Budget Group report on the WAS (September 2023, round 7).

1. **WAS already equal-splits property.** Per the WBG report, WAS distributes the main residence equally among the household's adults, assumes all adults over 16 share physical wealth equally, and records financial wealth as a mix of individual and joint assets with joint assets split equally. Pension wealth is always individual. So WAS personal-level wealth is partly equal-split by construction; the equal-split baseline matches WAS's own convention.
2. **Consequence for the as-owned sensitivity (s = 0).** Property ownership shares within households are not collected, so s < 1 for property cannot be built from WAS. It is available only for pension wealth (individual) and partly for financial wealth. Treat s = 0 as unavailable for property, and say so wherever s is reported.
3. **Evidence on within-household inequality.** WBG Table 4 (personal wealth, round 7): single women hold less than single men and than people in couples in every group: working age with no children 289,429 (women) against 313,454 (men) pounds; with children 100,043 against 214,844; above pension age 423,154 against 515,776. Couples 292,437, 226,171 and 529,641. No gender split within couples was in the text opened. This is the group the equal-split baseline treats as symmetric within a couple, so the baseline can mask the within-couple gap; the report notes equal sharing may not reflect who controls assets.
4. **Adults per household by tenure: not found.** EHS 2013-14 gives household-type shares, not average adults: outright owners 53% couples without dependent children, 29% single aged 60 or over, 82% one- or two-person households; owners with a mortgage 34% couples without dependent children and 46% with dependent children; private renters 24% couples without dependent children, 36% with dependent children. Converting the owner-occupier household rate to an adult rate still needs adults per household by tenure from EHS tables or WAS microdata.
5. **Age cut-off.** The report states adults over 16 for the sharing assumption and describes round 7 as covering adults aged 20 and over; the two statements were not reconciled. Open.
6. **Caveats from the same report.** Self-reported values; property tends to be overestimated; some figures differ between tables and text (financial wealth gap 14,299 pounds in Table 1, 13,832 in the text).

## Validation tolerance (decided 15 Oct)

**Adopted by the user: plus or minus 5 percentage points on the 10-year change.**

- Test quantity: model change in `scope_share_t` over a 10-year interval against the observed change over the same interval. For intervals shorter or longer than 10 years the band scales linearly (5 points per 10 years).
- Observed quantity: share of adults living in an owner-occupier household (adult basis, see above). Implementation note, for confirmation: `scope_share_t` is ownership times the share of owners above W_min, and the TOML sets `wmin_house_ratio = 1.0`, so the second factor is material. Where it is observed (WAS from 2006, SCF from 1989) the comparison is against ownership times that share. Before that, the observed ownership change is an upper bound and the test is one-sided.
- Windows tested: UK-history windows (the model replays each country's history onto the UK distribution); US as a flagged cross-check.
- Proposed with it and not separately confirmed: three zones (pass within 5 points; inconclusive between 5 and 10; fail beyond 10), and a secondary level test with a tolerance set from the measured household/adult and sampling gap before any run. The level tolerance is not yet set.
- To be recorded before any run: benchmark years, tested windows, and the model version.

## W_min per person (decided 15 Oct)

W_min is per person. On household data with equal split, the per-adult cut-off is half the median house price (the user's rule: a couple owning one median house is at the threshold). Consequences for D3: scope_share_t is larger than at a ratio of 1.0, so the observed target (adults above W_min) needs the same half-median cut-off in the WAS and SCF cuts; and the TOML needs `wmin_house_ratio` 0.5 (patch pending). The approximation breaks for single-adult owner households; a ratio sensitivity (0.5 to 1.0) is recommended. Record the justification as definitional, not as a revenue effect.

## Advani, Bangham and Leslie: unit of the model's distribution (checked 15 Oct)

Family basis (single adult or couple, with dependent children), wealth per adult within the family; shares are of total net family wealth. See `placeholder_register.md`. The D3 adult-basis comparison therefore needs the model cells re-expressed on an adult basis, or the family-versus-adult bias flagged.

## Gate: UK and US full series; others sparse benchmarks

UK: ownership passes in span (1918 on, annual from 1980), but with a gap in the vintage and source handovers; the third variable only from 2006. US: passes from 1965 for ownership (1890 sparse), SCF from 1989 for the distribution. Other countries: benchmarks from 2003 at best, from EU-SILC; the rest fallback grade C. Not yet a pass: neither the UK nor the US value series has been extracted.
