"""131r block 1: the published figures of the IFS report (Delestre and O'Brien, April 2026) as ifs_published.csv.

Run: python -I research/scripts/extract_ifs_published.py
Reads the held PDF literature/IFS Report - How is wealth distributed across British households.pdf with pdftotext (page breaks kept).
Every row flagged `text` carries a needle: a phrase that must appear, whitespace-normalised, on the stated PDF page, or the script stops.
Rows flagged `read from chart` are read by eye from the rendered figure (110 dpi) and carry a stated precision; they have no needle.
Printed page = PDF page index minus 1 (the cover is unnumbered). Money is in 2026 prices as the report states (footnote 19); 2020-22 is April 2020 to March 2022 (WAS Round 8).
"""
import csv, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / 'literature/IFS Report - How is wealth distributed across British households.pdf'
OUT = ROOT / 'research/tables/131r-pension-basis-sensitivity/ifs_published.csv'
txt = subprocess.run(['pdftotext', '-layout', str(PDF), '-'], capture_output=True, text=True, check=True).stdout.split('\f')
norm = lambda s: re.sub(r'\s+', ' ', s)
pages = {i + 1: norm(p) for i, p in enumerate(txt)}

T, C = 'text', 'read from chart'
# id, measure, value, unit, period, basis, population, pdf_page, locator, flag, precision, needle
R = [
 ('IFS-01', 'mean household pension wealth', 450000, 'gbp_2026', '2020-22', 'IFS', 'GB households', 3, 'executive summary, key finding 1', T, 'stated to the nearest 10,000', '(£450,000, compared with £230,000'),
 ('IFS-02', 'mean household pension wealth', 230000, 'gbp_2026', '2020-22', 'ONS', 'GB households', 3, 'executive summary, key finding 1', T, 'stated to the nearest 10,000', '(£450,000, compared with £230,000'),
 ('IFS-03', 'pension share of household wealth', 54, 'pct', '2020-22', 'IFS', 'GB households', 3, 'executive summary, key finding 1', T, 'whole percent', 'Around 54% of total household wealth was held in pensions under our methodology, compared with just 38% under the ONS methodology'),
 ('IFS-04', 'pension share of household wealth', 38, 'pct', '2020-22', 'ONS', 'GB households', 3, 'executive summary, key finding 1', T, 'whole percent', 'Around 54% of total household wealth was held in pensions under our methodology, compared with just 38% under the ONS methodology'),
 ('IFS-05', 'mean total household wealth (excl. business wealth)', 830000, 'gbp_2026', '2020-22', 'IFS', 'GB households', 17, 'section 3, opening paragraph', T, 'nearest 10,000; "37% higher"', '37% higher under our methodology: £830,000, compared with £600,000 under the ONS methodology'),
 ('IFS-06', 'mean total household wealth (excl. business wealth)', 600000, 'gbp_2026', '2020-22', 'ONS', 'GB households', 17, 'section 3, opening paragraph', T, 'nearest 10,000', '37% higher under our methodology: £830,000, compared with £600,000 under the ONS methodology'),
 ('IFS-07', 'mean total wealth, IFS over ONS', 37, 'pct', '2020-22', 'IFS vs ONS', 'GB households', 17, 'section 3, opening paragraph', T, 'whole percent', '37% higher under our methodology'),
 ('IFS-08', 'aggregate household wealth (excl. business wealth)', 16.3, 'gbp_tn_2026', '2020-22', 'ONS', 'GB households', 17, 'section 3, opening paragraph', T, 'one decimal', 'from £16.3 trillion to £22.3 trillion'),
 ('IFS-09', 'aggregate household wealth (excl. business wealth)', 22.3, 'gbp_tn_2026', '2020-22', 'IFS', 'GB households', 17, 'section 3, opening paragraph', T, 'one decimal', 'from £16.3 trillion to £22.3 trillion'),
 ('IFS-10', 'real 15-year index-linked gilt yield, average', -1.9, 'pct_pa', 'Apr 2020 to Mar 2022', 'IFS discount rate', 'market', 17, 'section 3, after the aggregate figures', T, 'one decimal', '–1.9% a year to the purchaser'),
 ('IFS-11', 'real SCAPE rate used by ONS, fixed', 2.4, 'pct_pa', '2020-22', 'ONS discount rate', 'method', 18, 'section 3, start of page', T, 'one decimal', 'was set at a fixed real rate of 2.4% throughout the period'),
 ('IFS-12', 'mean total household wealth', 530000, 'gbp_2026', '2006-08', 'ONS', 'GB households', 18, 'Figure 1 discussion', T, 'nearest 10,000', 'from £530,000 to £720,000 under the ONS approach compared with an increase from £550,000 to £750,000'),
 ('IFS-13', 'mean total household wealth', 720000, 'gbp_2026', '2018-20', 'ONS', 'GB households', 18, 'Figure 1 discussion', T, 'nearest 10,000', 'from £530,000 to £720,000 under the ONS approach compared with an increase from £550,000 to £750,000'),
 ('IFS-14', 'mean total household wealth', 550000, 'gbp_2026', '2006-08', 'IFS', 'GB households', 18, 'Figure 1 discussion', T, 'nearest 10,000', 'from £530,000 to £720,000 under the ONS approach compared with an increase from £550,000 to £750,000'),
 ('IFS-15', 'mean total household wealth', 750000, 'gbp_2026', '2018-20', 'IFS', 'GB households', 18, 'Figure 1 discussion', T, 'nearest 10,000', 'from £530,000 to £720,000 under the ONS approach compared with an increase from £550,000 to £750,000'),
 ('IFS-16', 'total wealth at the 90th percentile, IFS minus ONS', 490000, 'gbp_2026', '2020-22', 'IFS minus ONS', 'GB households', 21, 'Figure 4 discussion', T, 'nearest 10,000', 'we value total household wealth in 2020–22 at £490,000 higher than official statistics'),
 ('IFS-17', 'total wealth at the 50th percentile, IFS minus ONS', 130000, 'gbp_2026', '2020-22', 'IFS minus ONS', 'GB households', 21, 'Figure 4 discussion', T, '"only around"; nearest 10,000', 'the increase in measured household wealth as a result of our method is only around £130,000'),
 ('IFS-18', 'total wealth at the 30th percentile, IFS over ONS', 49, 'pct', '2020-22', 'IFS vs ONS', 'GB households', 22, 'Figure 4 discussion (page break from p21)', T, 'whole percent', 'the 30th percentile see a 49% increase in measured wealth under the IFS measure, compared with just a 34% increase for households at the 90th percentile'),
 ('IFS-19', 'total wealth at the 90th percentile, IFS over ONS', 34, 'pct', '2020-22', 'IFS vs ONS', 'GB households', 22, 'Figure 4 discussion (page break from p21)', T, 'whole percent', 'the 30th percentile see a 49% increase in measured wealth under the IFS measure, compared with just a 34% increase for households at the 90th percentile'),
 ('IFS-20', 'top 10% share of household wealth', 42, 'pct', '2020-22', 'IFS and ONS (identical)', 'GB households', 22, 'after Figure 4', T, 'whole percent; no business wealth, no top-tail adjustment', 'is virtually identical under the two methodologies, at 42%'),
 ('IFS-21', 'top 10% share of household wealth', 45, 'pct', '2006-08', 'IFS', 'GB households', 4, 'executive summary, key finding 2', T, 'whole percent', 'declined from 45% in 2006–08 to 42% in 2018–20'),
 ('IFS-22', 'top 10% share of household wealth', 42, 'pct', '2018-20', 'IFS', 'GB households', 4, 'executive summary, key finding 2', T, 'whole percent', 'declined from 45% in 2006–08 to 42% in 2018–20'),
 ('IFS-23', 'top 10% share of household wealth', 46, 'pct', '2006-08', 'ONS', 'GB households', 4, 'executive summary, key finding 2', T, 'whole percent', 'fell only marginally, from 46% to 45%'),
 ('IFS-24', 'top 10% share of household wealth', 45, 'pct', '2018-20', 'ONS', 'GB households', 4, 'executive summary, key finding 2', T, 'whole percent', 'fell only marginally, from 46% to 45%'),
 ('IFS-25', 'Gini coefficient of household wealth', 0.60, 'ratio', '2020-22', 'IFS and ONS (identical)', 'GB households', 23, 'Figure B2 discussion', T, '"around 60%"', 'essentially identical coefficients in the latest version of the data, at around 60%'),
 ('IFS-26', 'pension share of wealth, age 65+', 31, 'pct', '2020-22', 'ONS', 'GB individuals aged 65+', 26, 'Figure 7 discussion', T, 'whole percent', 'attributable to pensions from 31% to 38%'),
 ('IFS-27', 'pension share of wealth, age 65+', 38, 'pct', '2020-22', 'IFS', 'GB individuals aged 65+', 26, 'Figure 7 discussion', T, 'whole percent', 'attributable to pensions from 31% to 38%'),
 ('IFS-28', 'pension share of wealth, age 40-64', 59, 'pct', '2020-22', 'IFS', 'GB individuals aged 40-64', 26, 'Figure 7 discussion (ONS about 40)', T, 'whole percent', 'to 59% for 40- to 64-year-olds and to 73% for 20- to 39-year-olds'),
 ('IFS-29', 'pension share of wealth, age 20-39', 73, 'pct', '2020-22', 'IFS', 'GB individuals aged 20-39', 26, 'Figure 7 discussion (ONS about 40)', T, 'whole percent', 'to 59% for 40- to 64-year-olds and to 73% for 20- to 39-year-olds'),
 ('IFS-30', 'share of aggregate individual wealth, age 20-39', 18, 'pct', '2020-22', 'IFS', 'GB individuals aged 20-39', 27, 'Figure 8 discussion', T, 'whole percent', 'held 18% of aggregate wealth under our measure, compared with 11% under the ONS measure'),
 ('IFS-31', 'share of aggregate individual wealth, age 20-39', 11, 'pct', '2020-22', 'ONS', 'GB individuals aged 20-39', 27, 'Figure 8 discussion', T, 'whole percent', 'held 18% of aggregate wealth under our measure, compared with 11% under the ONS measure'),
 ('IFS-32', 'share of aggregate individual wealth, age 65+', 29, 'pct', '2020-22', 'IFS', 'GB individuals aged 65+', 27, 'Figure 8 discussion', T, 'whole percent', 'aged 65 and over fell from 36% to 29%'),
 ('IFS-33', 'share of aggregate individual wealth, age 65+', 36, 'pct', '2020-22', 'ONS', 'GB individuals aged 65+', 27, 'Figure 8 discussion', T, 'whole percent', 'aged 65 and over fell from 36% to 29%'),
 ('IFS-34', 'median individual wealth, age 30-39, IFS over ONS', 50, 'pct', '2020-22', 'IFS vs ONS', 'GB individuals in their 30s', 26, 'Figure 8 discussion', T, '"50% higher"', 'Median wealth for individuals in their 30s is 50% higher under our measure than under the ONS measure'),
 ('IFS-35', 'median individual wealth, age 70+, IFS over ONS (upper bound)', 10, 'pct', '2020-22', 'IFS vs ONS', 'GB individuals aged 70+', 26, 'Figure 8 discussion', T, '"less than 10%": an upper bound', 'for individuals aged 70 and over, the increase is less than 10%'),
 ('IFS-36', 'home contents reduced by 75% in both measures', 75, 'pct', '2020-22', 'IFS and ONS', 'method', 17, 'footnote 20', T, 'method note; business wealth excluded in both (main text, p16)', 'we therefore reduce the reported values of home contents by 75%'),
 ('IFS-37', 'business wealth excluded in both measures', '', 'note', '2020-22', 'IFS and ONS', 'method', 17, 'section 3, opening paragraph', T, 'method note', 'we exclude business wealth in both measures'),
 ('IFS-38', 'gap expected to narrow in 2022-24 as gilt yields rose', '', 'note', '2022-24', 'IFS vs ONS', 'method', 20, 'after Figure 2', T, 'qualitative', 'The discrepancy between the two measures will therefore be considerably smaller in 2022–24 than in 2020–22'),
]
CH = [  # Figure 4 (printed p21, pdf 22), right axis, percentage difference IFS over ONS in total household wealth by percentile; read by eye, +-2 percentage points
 *[('IFS-C%02d' % (i + 1), 'total wealth at the %dth percentile, IFS over ONS' % p, v, 'pct', '2020-22', 'IFS vs ONS', 'GB households', 22, 'Figure 4, percentage-difference line, right axis', C, '+-2 percentage points; p30 and p90 agree with the text (49, 34)', '')
   for i, (p, v) in enumerate([(10, 4), (20, 41), (30, 49), (40, 45), (50, 38), (60, 35), (70, 37), (80, 34.5), (90, 33.5)])],
 ('IFS-C10', 'total wealth at the 50th percentile, IFS bar', 470000, 'gbp_2026', '2020-22', 'IFS', 'GB households', 22, 'Figure 4, bar, left axis', C, '+-20,000; IFS minus ONS bar agrees with the text (130,000)', ''),
 ('IFS-C11', 'total wealth at the 50th percentile, ONS bar', 340000, 'gbp_2026', '2020-22', 'ONS', 'GB households', 22, 'Figure 4, bar, left axis', C, '+-20,000', ''),
 ('IFS-C12', 'total wealth at the 90th percentile, IFS bar', 1940000, 'gbp_2026', '2020-22', 'IFS', 'GB households', 22, 'Figure 4, bar, left axis', C, '+-30,000; IFS minus ONS bar agrees with the text (490,000)', ''),
 ('IFS-C13', 'total wealth at the 90th percentile, ONS bar', 1450000, 'gbp_2026', '2020-22', 'ONS', 'GB households', 22, 'Figure 4, bar, left axis', C, '+-30,000', ''),
]
# Figure B3 (printed p41, pdf 42): ratio of total individual pension wealth, IFS over ONS, round Apr 2020 to Mar 2022 (blue line); read by eye, +-10 percentage points
CH += [('IFS-C%02d' % (14 + i), 'pension wealth ratio IFS over ONS, %s' % a, v, 'pct_ratio', '2020-22', 'IFS vs ONS', 'GB individuals, ' + a, 42, 'Figure B3, Apr 2020 - Mar 2022 line', C, '+-10 percentage points (a ratio: 100 = no change)', '') for i, (a, v) in enumerate([('up to age 34', 470), ('age 35-49', 265), ('age 50-59', 182), ('age 60-69', 147), ('age 70+', 131)])]
rows = R + CH
bad = [r[0] for r in rows if r[11] and norm(r[11]) not in pages[r[7]]]
if bad:
    sys.exit('needle not found on the stated page: ' + ', '.join(bad))
with OUT.open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow('id measure value unit period basis population pdf_page printed_page locator flag precision'.split())
    for r in rows:
        w.writerow(list(r[:7]) + [r[7], r[7] - 1] + list(r[8:11]))
print(f'ifs_published.csv: {len(rows)} rows ({sum(1 for r in rows if r[9] == T)} text, {sum(1 for r in rows if r[9] == C)} read from chart); every text needle found on its page')
