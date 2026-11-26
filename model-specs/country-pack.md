# Model v3: country data pack (brief 038c)

Design note only. No loader, schema file or data file is written here, and `registry/`, `model_v2/` and `pipeline/` are untouched. R11 (`research/model-audit/synthesis.md` section 4): everything specific to one country lives in a data pack, so a second country is a new pack and no code change. This note fixes what the pack holds, how it is laid out, validated, hashed and licensed, and how to test that the code is clean of the UK.

## 1. Boundary: what is in the pack and what stays in the register

The register is `model-specs/inputs.md` (269 rows, 12 cells each). `030c` turns it into `data/input-register/inputs.json`, so scalar values, ranges and judgements stay there in the interim.

**Rule.** A row goes to the pack if and only if (a) it is one cell of a multi-cell country dataset (a series, a table by band, decile or tax line, or a rule set) **and** (b) its How cell does not carry `(J)`. Every other row stays in the register: scalar assumptions, behavioural and model parameters, and every `(J)` row, because a judgement belongs with its range and reason, not in a data file. A pack row's register entry stays as the pointer: the register keeps the row id, the pack file and column that supply it, and the pack file is the only place the number is typed (check X1 below).

Result, from the script in the appendix: **108 pack rows, 161 register rows, 269 in all.** 161 = 49 `(J)` scalar rows + 74 other scalar rows + 38 `(J)` rows that are shaped like pack data (kept in the register by rule (b); they move to the pack once their judgement is replaced by a sourced value).

| Family | Pack | Register | Total | Pack dataset |
|---|---:|---:|---:|---|
| D1 | 5 | 0 | 5 | returns |
| D4 | 2 | 5 | 7 | wealth_tail |
| D6 | 5 | 12 | 17 | household_incidence |
| D7 | 2 | 2 | 4 | receipts |
| D9 | 4 | 4 | 8 | wealth_distribution |
| H1 | 20 | 0 | 20 | household_incidence |
| H2 | 8 | 3 | 11 | wealth_distribution (H2a), household_incidence (H2b) |
| H3 | 10 | 10 | 20 | household_incidence |
| H6 | 9 | 0 | 9 | returns |
| T1 | 3 | 2 | 5 | tax_rules |
| T3 | 16 | 0 | 16 | receipts |
| T4 | 4 | 3 | 7 | wealth_distribution |
| T6 | 9 | 3 | 12 | wealth_distribution |
| T7 | 6 | 0 | 6 | tax_rules |
| W5 | 3 | 2 | 5 | wealth_distribution (W5e), wealth_tail (W5c, W5d) |
| W7 | 2 | 0 | 2 | wealth_tail |
| D5, D8, D10, D11, H4, H5, H7, M5, M6, M8, T2, T5, W1 to W4, W6, W8, W9 | 0 | 115 | 115 | none (all scalar or `(J)`) |
| **Total** | **108** | **161** | **269** | |

(The last row groups 19 families with no pack row; the script prints each.) By dataset: returns 14, wealth_distribution 25, wealth_tail 6, receipts 18, household_incidence 36, tax_rules 9 = 108. `public_expenditure` (section 4) has no register row today.

## 2. Layout

One folder per country, named by ISO 3166-1 alpha-3 code: `pack/GBR/`. Inside, plain UTF-8 CSV, one file per dataset, plus one manifest.

```
pack/GBR/
  manifest.json            # pack header and the file list with per-file sha256
  returns.csv              # annual real total returns by asset class
  wealth_distribution.csv  # shares and amounts by wealth band
  wealth_tail.csv          # top shares and the rich-list add-on
  receipts.csv             # tax receipts by line, share of GDP
  household_incidence.csv  # tax and income by income quintile or decile
  tax_rules.csv            # statutory rates, bands and rules
  public_expenditure.csv   # spending by function
  NOTICE.md                # attribution text for every licence in the pack
```

CSV, not JSON, because the data are tables and a reader can open them in a spreadsheet. Rules for every file: header row of column names exactly as in section 3; decimal point; no thousands separators; percentages as percent numbers (4.42, not 0.0442) with the unit in the schema, never in the cell; years as integers; an empty cell is missing, and the only other missing marker is none.

**`manifest.json` header fields (all required, loader fails if one is absent or empty):**

| Field | Meaning |
|---|---|
| `country` | ISO alpha-3 code, equal to the folder name |
| `currency` | ISO 4217 code of every money value in the pack (`GBP`) |
| `base_year` | year of constant prices for real money columns, or `null` if every money column is nominal and says so |
| `pack_version` | integer, bumped on any file change |
| `built` | date the manifest was written |
| `files` | list of objects, one per data file: `name`, `dataset`, `sha256`, `rows`, `source`, `licence`, `retrieved`, `vintage` |

Per file: `source` is the register source ids (`S1`, `SW7` ...) plus the held file path where one exists; `licence` is one of `ogl-v3`, `cc-by`, `cite-only`, `unverified` (section 7); `retrieved` is the date the data were obtained; `vintage` is the publication round or release (`WAS Round 8`, `JST R6`, `EFO March 2023`).

## 3. Schema per dataset

Common loader rules (R5, fail loudly): the loader reads the manifest first; refuses a pack whose folder name differs from `country`; checks each file's sha256 against the manifest; checks the header row equals the schema's column list in order; and raises on the first violation with file, row and column. It never fills, interpolates, clips or defaults a value. A missing value is allowed only where the schema says so; a missing value anywhere else is an error. Percent columns must lie in [0, 100] unless the schema gives another range.

### 3.1 returns.csv
One row per year. Real total returns, annual, in percent, deflated by the country's CPI (the deflator is a `cpi` column, so the loader can re-derive real from nominal).

| Column | Type | Unit | Missing allowed | Rule |
|---|---|---|---|---|
| `year` | int | calendar year | no | strictly increasing, no gaps inside the file's span |
| `eq_tr` | float | % a year, nominal | yes, outside the series span | -100 < x < 1000 |
| `housing_tr` | float | % a year, nominal | yes, outside the series span | same |
| `bond_tr` | float | % a year, nominal | yes, outside the series span | same |
| `capital_tr` | float | % a year, nominal | yes, outside the series span | same |
| `cpi` | float | index, any base | no | > 0, every year |
| `gdp_pc` | float | real GDP per head, a level, in the units the source publishes (brief 070c) | yes, outside the series span | > 0 |

Span rule: each return column is contiguous (missing only before its first and after its last year). Derived (not stored, computed by the model, so register rows I-D1a to I-D1e and I-H6a to I-H6i are checks): geometric and arithmetic mean, standard deviation, loss-year frequency, longest loss run, cross-correlations.

### 3.2 wealth_distribution.csv
Long form: one row per (variable, band). Round 8 of the household wealth survey, by wealth decile or threshold.

| Column | Type | Unit | Missing allowed | Rule |
|---|---|---|---|---|
| `variable` | text | key | no | one of the keys in the table below |
| `band` | text | key | no | `D1` to `D10`, `D4-5`, `D6-7`, `D8-9`, `top1`, `top10`, `ge_150000` ..., or `all` |
| `value` | float | per `unit` | no | range per `unit` |
| `unit` | text | `pct_total_wealth`, `pct_households`, `gbp_bn`, `pct_of_band` | no | fixed per variable |
| `basis` | text | `household` or `adult` | no | which unit the share is over |
| `year` | text | survey period, `2018-20` style | no | |

Keys: `net_financial_share`, `pension_share`, `property_share`, `gain_bearing_wealth` (`gbp_bn`), `isa_share`, `wealth_share` (top shares), `households_above`, `wealth_above` (the W6 threshold ladder), `share_below_wmin_by_income_decile` (H2a). **Added 2026-11-19 (guru, for the base, brief 067c):** `wealth_total` (`gbp_bn`, household net wealth by band `D1` to `D10` and `all`, `basis` household), `households` and `adults` (new unit `thousand`, same bands), `median_house_price` (new unit `gbp`, band `all`, `basis` adult; W_min is a lever ratio times it) and `gdp` (`gbp_bn`, band `all`, the pack's price year; converts the base to shares of GDP). The loader enum gains `thousand` and `gbp`; nothing else about the format changes. Uniqueness: (`variable`, `band`, `basis`, `year`) is the key. Cross-check the loader runs: for each `variable` with bands that partition the population, shares sum to 100 within 0.5.

### 3.3 wealth_tail.csv
Binned top shares plus the add-on that the survey misses. **Decision (the brief's open question): no survey microdata.** The register's tail sources (S5, S6 and the Rich List) publish top shares and a combined-wealth total, not unit records, and the WAS microdata need a licence the repo does not hold. A pack of top shares and tail points is enough for ω; a model that needs microdata is a different requirement and would say so.

| Column | Type | Unit | Missing allowed | Rule |
|---|---|---|---|---|
| `series` | text | key | no | `was_top1`, `adult_top1`, `adult_top10`, `wid_top1`, `wid_top10`, `was_missing_top`, `rich_list_total` |
| `year` | int | calendar year | no | |
| `value` | float | per `unit` | no | |
| `unit` | text | `pct_wealth` or `gbp_bn` | no | `rich_list_total` and the missing-wealth point are the only `gbp_bn` or `pct_total` |
| `low`, `high` | float | same as `value` | yes | low <= value <= high where both given |
| `basis` | text | `adult` or `household` | no | |

Tail points have no required count; a country with only top-10 and top-1 shares supplies two series. WID rows are read from `model_v2/wid_out/wid_long.csv` (variables `shweal_p99p100_992_j`, `shweal_p90p100_992_j`) and copied, not linked, so the pack is self-contained and hashable.

### 3.4 receipts.csv
One row per tax line, central forecast year, share of GDP, so the revenue closure (M1d) can read the retired lines.

| Column | Type | Unit | Missing allowed | Rule |
|---|---|---|---|---|
| `line` | text | key | no | `income_tax`, `paye`, `self_assessment`, `nics`, `vat`, `corporation_tax`, `fuel_duty`, `cgt`, `iht`, `stamp_duties`, `stamp_property`, `stamp_shares`, `business_rates`, `council_tax`, `total_hmrc`, `total_current` |
| `fiscal_year` | text | `2025-26` | no | |
| `pct_gdp` | float | % of GDP | no | 0 <= x < 100 |
| `gbp_bn` | float | £ bn nominal | yes | where the source gives it |
| `basis` | text | `forecast` or `outturn` | no | the held file is a March 2023 forecast |

Cross-checks: `paye + self_assessment` <= `income_tax`; `stamp_property + stamp_shares` <= `stamp_duties`; the lines the model sums (M1d) equal 8.11% of GDP within 0.01 (an interim check, X2 below). The stamp-duty sub-rows must not be summed with their parent; this is the double count corrected on 2026-11-17 (`drivers.md` section 1).

### 3.5 household_incidence.csv
Long form, by income group, from the household effects-of-taxes-and-benefits tables.

| Column | Type | Unit | Missing allowed | Rule |
|---|---|---|---|---|
| `variable` | text | key | no | `total_tax`, `total_tax_pct_gross`, `gross_income`, `share_receiving_net_benefit`, `tax_share_top_decile`, `tax_share_bottom_five` |
| `group` | text | key | no | `Q1` to `Q5`, `D1` to `D10`, or `all` |
| `tax` | text | line key from receipts | yes, except for the `tax_share_*` variables | |
| `value` | float | per `unit` | no | |
| `unit` | text | `gbp_per_household_year`, `pct_gross_income`, `pct_individuals`, `pct_of_tax` | no | |
| `fiscal_year` | text | `FYE 2023` or `2023-24` | no | |
| `basis` | text | `equivalised_disposable` or `original` | no | |

Quintile and decile rows for the same variable and year must agree: the mean of the ten decile values equals the mean of the five quintile values within 1%. Several decile rows exist only in the held 2023-24 tables (`data/uk-source-workbooks/etbreferencetablesfye202324final.xlsx`); the FYE 2023 quintiles are not held (section 4).

### 3.6 tax_rules.csv
The statutory rules the retired-tax and benchmark lines depend on, as rows, so a second country supplies its own.

| Column | Type | Unit | Missing allowed | Rule |
|---|---|---|---|---|
| `rule` | text | key | no | `income_tax_band`, `ni_employee`, `investment_income_rate`, `cgt_rate`, `cgt_annual_exempt`, `bador_rate`, `main_home_relief`, `death_uplift` |
| `tax_year` | text | `2026-27` | no | |
| `subject` | text | key | yes | `basic`, `higher`, `additional`, `all` |
| `lower`, `upper` | float | currency | yes | band edges; `upper` empty means no cap |
| `rate` | float | % | yes | 0 <= x <= 100 |
| `amount` | float | currency | yes | |
| `flag` | text | `true`, `false` | yes | for the rule rows (T7e, T7f) |

Exactly one of `rate`, `amount`, `flag` is non-empty per row. Band rows of one `rule` and `tax_year` must be ordered and non-overlapping.

### 3.7 public_expenditure.csv
Spending by function, share of GDP, for the benchmarks that price a retired line against other uses. A non-empty file must hold a `function` = `total` row (the reference expenditure over GDP, brief 070c); `pct_gdp` lies strictly between 0 and 100. Columns: `function` (key), `fiscal_year`, `pct_gdp` (float, % of GDP), `gbp_bn` (float, nominal, may be missing), `basis`. UK file: one row, `total`, `fiscal_year` 2019 (the reference year, v2's `exp_ref_year`), `pct_gdp` 36.82 from JST `expenditure` over `gdp` for 2019 (`data/rates/JSTdatasetR6.xlsx`, Sheet1, GBR row 1510); `gbp_bn` empty. Cross-check, not stored: `data/rates/PSS_May_2024_TES_UPDATED.xlsx`, Data_for_charts, TME over nominal GDP, 39.58 for 2019-20. No register row points here.

## 4. The UK pack: files, repo sources and what is missing

| Pack file | Rows | Source in the repo today | Missing |
|---|---:|---|---|
| `returns.csv` | 14 checks | `model_v2/jst_r6.json` (series `eq_tr` 1871-2020, `housing_tr` 1896-2020, `bond_tr` 1870-2020, `capital_tr` 1896-2019, `cpi`, and from 070c `rgdpmad` as `gdp_pc` 1870-2019); `data/rates/JSTdatasetR6.xlsx` | Years 2021 to the last full year (I-D1e gap); a licence check for JST |
| `wealth_distribution.csv` | 25 | `data/rates/totalwealthtables.xlsx` (Tables 2.2, 2.4, 2.5), `financialwealthtables.xlsx` | A later survey wave than Round 8; the 14 W6 ladder rows and 6 other rows are `(J)` and not yet sourced |
| `wealth_tail.csv` | 6 | `model_v2/wid_out/wid_long.csv` (I-W7a, I-W7b) | I-D4d, I-D4f, I-W5c, I-W5d are `no` in the register (Advani et al., Rich List: not copied into the repo) |
| `receipts.csv` | 18 | `data/rates/Revenue composition spreadsheet.xlsx` | An outturn vintage newer than the March 2023 forecast; `data/rates/maintax_2023.xlsx` is held and not cited |
| `household_incidence.csv` | 36 | `data/uk-source-workbooks/etbreferencetablesfye202324final.xlsx` (Tables 2b, 2c, 13, 16: decile rows I-H1k to I-H1t, I-H3k to I-H3t, I-H2b, I-D6a, I-D6h, I-D6o to I-D6q) | The FYE 2023 quintile rows I-H1a to I-H1j (10 rows) have no file in the repo |
| `tax_rules.csv` | 9 | none (read from gov.uk and a Deloitte PDF, register ST1 to ST3) | all 9 rows: I-T1a, I-T1b, I-T1e, I-T7a to I-T7f |
| `public_expenditure.csv` | 1 | `data/rates/JSTdatasetR6.xlsx` (`expenditure` over `gdp`, 2019; cross-check `PSS_May_2024_TES_UPDATED.xlsx` Data_for_charts, 39.58 for 2019-20, not stored) | other functions; `gbp_bn` |

Of the 108 pack rows, **23 have data not in the repo** (register "In repo" cell starts with `no`): I-D4d, I-D4f, I-H1a to I-H1j, I-T1a, I-T1b, I-T1e, I-T7a to I-T7f, I-W5c, I-W5d. The other 85 are held. Four held files are cited by no register source: `maintax_2023.xlsx`, `PSS_May_2024_TES_UPDATED.xlsx`, `7.1_260716_Rates_Data_Tables.xlsx`, `financialwealthtables.xlsx`; the research lane should say which row each supports or drop it.

## 5. Hash and provenance

**Pack hash.** `pack_sha256` = sha256 of the UTF-8 text `GBR\n` + for each file in `manifest.files` sorted by `name`: `name`, a space, the file's own sha256 and a newline. The manifest header fields (country, currency, base_year, pack_version) are hashed first as canonical JSON (sorted keys, no spaces). So any change to a data byte, a file name, the currency or the base year changes the pack hash. The manifest's `built`, `retrieved` and licence text are not hashed; they are provenance, not data.

**Run record.** The run writes `run.pack_sha256` and `run.pack_country` next to `run.inputs_sha256`. Gate G2 (`website/notes/order.md`) reads "`run.inputs_sha256` equals the hash of `data/input-register/inputs.json`"; it should read both fields, and the guru should add the second. Rule: a run is valid only if both hashes equal those of the files now in the repo; a pack change makes every earlier run stale, the same as a register change, and the output validator (`030c`) reports it as an error in final mode.

**Interim consistency.** While the register keeps the pack rows as pointers, the build checks that each register value for a pack row equals the value derived from the pack file, within 1e-9 (X1), and that M1d's lines equal 8.11% of GDP within 0.01 (X2). A mismatch fails the build. X1 goes away when `030c`'s register build reads pack-row values from the pack.

## 6. The R11 test

**Rule.** Run once against `model_v2/` and later on every model release: code files must name no country, institution, tax or currency and hold no pack-valued literal. Three classes, ripgrep with PCRE, comments excluded (`^[^#]*(...)`):

```
GLOBS=(-g '*.py' -g '!test/**' -g '!audit_d0/**' -g '!wid_out/**' -g '!wid_*.py' -g '!d0_jst_audit.py')
N='\b(UK|U\.K\.|United Kingdom|Britain|British|England|Scotland|Wales|GBR|HMRC|HMT|ONS|IFS|OBR|Treasury|Green Book|Bank of England|sterling|GBP|Sunday Times|Rich List|Wealth and Assets)\b|£'
T='(?i)\b(council tax|stamp duty|SDLT|inheritance tax|IHT|capital gains tax|CGT|national insurance|NICs?|PAYE|self assessment|business rates|corporation tax|VAT|ISAs?)\b'
A='\b[0-9][0-9,]*(\.[0-9]+)?\s*(bn|k|m)\b(?=[^a-zA-Z_])'
for p in "$N" "$T" "$A"; do rg -P -c "^[^#]*($p)" "${GLOBS[@]}" .; done      # run from model_v2/
```

Class N is the names and the `£` sign, class T is country tax names, class A is amount literals with a unit suffix. A hit is a failure unless the line is in a docstring or string that the pack does not need (the test counts it and the reviewer clears it by hand, listed in the release note). A second rule, A2, not run now: no numeric literal in a model file equals a value in the pack (needs the pack to exist).

**Run, once, 2026-11-17, on `model_v2/` (17,730 lines scanned):**

| Class | Matching lines | Outside comments | Files |
|---|---:|---:|---:|
| N | 251 | 210 | 12 |
| T | 122 | 93 | 5 |
| A | 13 | 8 | 3 |
| Union, outside comments | | **288** | 12 |

Union per file: `EVAL/eval_core.py` 127, `RATES/8_2_RATES_tables.py` 44, `wdt_fmt.py` 30, `RATES/8_3_RATES_charts.py` 22, `RATES/rates_core.py` 19, `VAL/valgen_core.py` 13, `wdt_core.py` 11, `VAL/5_6_VALGEN_tables.py` 8, `VAL/5_8_VAL_gap_tables.py` 6, `VAL/5_7_VALGEN_charts.py` 6, `wdt_md.py` 1, `VAL/5_10_VAL_examples.py` 1. Example: `wdt_core.py:1198: """UK GDP in £m."""`. The target for model v3 is zero outside the pack loader's own `country` handling and the labels read from `manifest.json`.

**What a second country must supply**, and nothing else: a folder `pack/<ISO>/` with the seven files of section 3 (a file may be absent only if the manifest says which register rows then fall back to scalar inputs), a manifest with the header of section 2, a `NOTICE.md`, and the register entries for the `(J)` rows that are specific to it (behaviour, capitalisation, and so on). Labels and currency symbols the site prints come from the manifest (`country`, `currency`), not from code.

## 7. Licences

| Pack file | Source | Licence | Status |
|---|---|---|---|
| `returns.csv` | JST Macrohistory R6 | free for research with citation (register S10, SH10) | **unverified**: the licence page fetch failed; the `jst_r6.json` meta has no licence field; cite only until checked, do not redistribute the pack publicly until then |
| `wealth_distribution.csv` | ONS WAS Round 8 and the ONS financial wealth tables | OGL v3 | redistributable with attribution |
| `wealth_tail.csv` | Advani, Bangham, Leslie 2021 (S5): licence not stated; Advani, Summers, Tarrant 2025 (S6): CC BY; WID: terms not checked; Sunday Times Rich List: News UK terms not verified | mixed | **cite only** for S5, WID and the Rich List; the Rich List total is one number with its citation, not a copy of the list |
| `receipts.csv` | IFS and OBR spreadsheet | cite only | not redistributable on the evidence held |
| `household_incidence.csv` | ONS effects of taxes and benefits tables (OGL v3); Civitas Table 4.1 (cite only) | mixed | OGL rows redistributable; Civitas-derived rows are cite only |
| `tax_rules.csv` | gov.uk (OGL v3); Deloitte PDF (free to read, cite only) | mixed | gov.uk rows redistributable |
| `public_expenditure.csv` | HM Treasury PSS | OGL v3 (to confirm) | unchecked |

The manifest's per-file `licence` field takes the **most restrictive** licence among the file's sources. A pack is publishable as a whole only if every file is `ogl-v3` or `cc-by`; today none of the UK pack's files passes that test because of the cite-only rows, so the pack stays in the repo as a private input and the site cites the sources, not the pack. `NOTICE.md` carries the OGL attribution text.

## Open flags for the guru (not mine to fix)
- `inputs.md` still has a stale "260 rows" bullet; the register has 269.
- Gate G3 in `order.md` says 70 `(J)` rows; the register has 87.
- Gate G2 needs `run.pack_sha256` (section 5).
- `synthesis.md` describes `wid_long.csv` as untracked and small; it is tracked and 52.9 MB.
- 125 register rows say "In repo: no" (23 of them pack rows).
- `project/brief-suggestions.md`: the `rates_core` import break found in 001c is wider than its current entry.

## Appendix: the tally script
`python -I tally.py model-specs/inputs.md` prints the table of section 1 and asserts: 269 rows, 12 cells each, no duplicate id, no id in two datasets, every grouped id exists, pack + register = 269. The groups below are rule (a); rule (b) is applied in the loop.

```python
GROUPS = {   # dataset -> row ids (non-(J) rows only; a (J) row always stays in the register)
 'returns':              ['I-D1a','I-D1b','I-D1c','I-D1d','I-D1e'] + [f'I-H6{c}' for c in 'abcdefghi'],
 'wealth_distribution':  ['I-D9e','I-D9f','I-D9g','I-D9h','I-W5a','I-W5b','I-W5e','I-T6m']
                         + [f'I-W6{a}{b}' for a in 'abcdefg' for b in '12']
                         + [f'I-T4{c}' for c in 'abcd'] + [f'I-T6{c}' for c in 'bcdefghij']
                         + [f'I-H2a{i}' for i in range(1,11)],
 'wealth_tail':          ['I-D4d','I-D4e','I-D4f','I-W5c','I-W5d','I-W7a','I-W7b'],
 'receipts':             [f'I-T3{c}' for c in 'abcdefghijklmnop'] + ['I-D7b','I-D7d'],
 'household_incidence':  [f'I-D6{c}' for c in 'abcdefghijklmnopq'] + [f'I-H1{c}' for c in 'abcdefghijklmnopqrst']
                         + ['I-H2b'] + [f'I-H3{c}' for c in 'abcde'] + [f'I-H3{c}' for c in 'klmnopqrst'],
 'tax_rules':            ['I-T1a','I-T1b','I-T1e'] + [f'I-T7{c}' for c in 'abcdef'],
}
rows = {}
for line in open(sys.argv[1], encoding='utf-8'):
    if re.match(r'\|\s*I-[\w]+\s*\|', line):
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        assert len(cells) == 12, cells[0]
        assert cells[0] not in rows, 'duplicate ' + cells[0]
        rows[cells[0]] = cells
want = {i: d for d, ids in GROUPS.items() for i in ids}
assert len(want) == sum(len(v) for v in GROUPS.values()), 'an id is in two datasets'
missing = sorted(set(want) - set(rows)); assert not missing, ('ids not in register', missing)
fam = lambda i: re.match(r'I-([A-Z]+\d*)', i).group(1)
side, reason = {}, {}
for i, c in rows.items():
    if i in want and '(J)' in c[6]: side[i], reason[i] = 'register', 'J'
    elif i in want:                 side[i], reason[i] = 'pack', want[i]
    else:                           side[i], reason[i] = 'register', 'scalar'
tab = collections.defaultdict(lambda: collections.Counter())
for i in rows: tab[fam(i)][side[i]] += 1
print('family  pack  register  total')
for f in sorted(tab): print(f'{f:6} {tab[f]["pack"]:5} {tab[f]["register"]:8} {sum(tab[f].values()):6}')
P = sum(1 for s in side.values() if s == 'pack'); R = sum(1 for s in side.values() if s == 'register')
print('TOTAL pack', P, 'register', R, 'sum', P + R, 'rows', len(rows)); assert P + R == len(rows) == 269
print('by dataset:', {d: sum(1 for i in rows if reason[i] == d) for d in GROUPS})
print('(J) rows kept in register though their family is pack-shaped:', sorted(i for i in rows if reason[i] == 'J'))
print('register rows total', R, '= (J) not in a pack group', sum(1 for i in rows if side[i]=='register' and reason[i]=='scalar' and '(J)' in rows[i][6]), '(J, scalar) + other scalar', sum(1 for i in rows if side[i]=='register' and reason[i]=='scalar' and '(J)' not in rows[i][6]), '+ (J, pack-shaped)', sum(1 for i in rows if reason[i]=='J'))
print('pack rows whose data is not in the repo (In repo cell starts with "no"):', sorted(i for i in rows if side[i]=='pack' and rows[i][10].lower().startswith('no')))
```
