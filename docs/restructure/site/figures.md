# Figure renderer and visual system (brief 019s, stage D)

Status: design only, drafted 2026-11-17. The author answered Q1 to Q8 on 2026-11-17, all as proposed (section 11). Builds nothing. The guru merges this file into `docs/restructure/site.md` with its siblings (`ids.md`, `hooks.md`, spoke checker, `nav.md`).

Inputs read: `docs/restructure/template.md` section 6a (figure block, drawing rules, F1 to F6), `model-specs/outputs.yml` (21 entries; every `summary`, `by`, `lines`, `per`, `kind`), `model-specs/added/*.md` (the proposed `problem`, `data_fact` and `check` roles and the extra manifest entries), `model-specs/metrics.md` (units, horizons, conventions), and the `dataviz` skill (form choice, mark specs, palette, interaction, accessibility; its palette validator was run, section 12). Nothing in `pipeline/`, `site/` or `registry/` was opened or changed.

## 1. Decisions in one screen

| Topic | Decision |
|---|---|
| Renderer | Static inline SVG written at build by one small Python module, no chart library. One shared stylesheet (about 3 KB) and one shared script (about 4 KB, no dependencies) load only on pages that contain a figure. |
| Data path | One `FigureData` object per figure, built once from the data file, the manifest and the metric register. The SVG, the reference table and the CSV are all emitted from it, and a build self-check re-reads all three and fails on any difference (section 4). |
| Palette | The `dataviz` reference palette. Three named schedules use a one-hue ordinal ramp; every other series uses fixed categorical slots tied to the entity, never to rank. Light and dark are separate validated sets. |
| Bands | A `p10_mean_p90` output is the mean line (2 px) with a p10 to p90 wash (10% opacity). When three schedules are drawn together, the band is drawn for S_central only; all three ranges are in the table and the tooltip (section 5.3, question Q6). |
| Kinds | Six drawing kinds with fixed rules (section 5). Every manifest `kind` has a default drawing kind (section 6). |
| Units | Axis units and display rounding come from the metric register; nothing is typed in a figure block (section 7, question Q4). |
| Access | Every figure has alt text, a focusable keyboard mode that reads values from the reference table, and a table view that is always on the page (section 8). |
| Print | A print stylesheet forces the light set and turns texture on; each figure also gets a standalone light-set SVG that the PDF build can embed (section 9). |

## 2. Renderer choice and page weight

Why static SVG, not a library:

- The figures are a closed set: six kinds, every one with a fixed look. A library earns its weight by flexibility the series does not use.
- Nothing needs to be computed in the browser. Quantiles, schedules and horizons are already in the data file.
- Static SVG prints, exports to PDF and reads in a screen reader without a runtime. A library adds a script that must finish before a figure exists.
- One renderer module (about 600 lines of Python, only `pyyaml` and the standard library, both already installed by the workflow) draws all six kinds, so the style cannot drift between figures.

Weight rules for the implementer:

- Each figure is emitted twice, as a **wide** layout (viewBox 720 wide) and a **narrow** layout (viewBox 360 wide), and CSS shows one at the 560 px breakpoint. Scaling a 720 wide drawing down to a phone makes 12 px text 6 px; two layouts keep type at 11 to 13 px everywhere. Budget: 40 KB per figure before compression, both layouts together.
- Colours and type are CSS classes using custom properties; no hex value is repeated inside a figure. The standalone print file (section 9) is the only place hex values are inlined.
- No fonts are loaded: `system-ui, -apple-system, "Segoe UI", sans-serif` (the `dataviz` rule: no display or serif face).
- No animation. `prefers-reduced-motion` needs no special case.

Alternative considered: Vega-Lite or Observable Plot rendered to SVG at build with Node. It gives six kinds for little code, but adds a Node dependency to the figure step, and its default look would have to be overridden mark by mark to meet the specs in section 5. Revisit only if the kinds multiply beyond six.

## 3. One palette and style

All values are the `dataviz` reference palette (`references/palette.md`). The site's own colours are not touched.

**Tokens** (CSS custom properties on `.wdt-fig`; light values, then dark):

| Token | Role | Light | Dark |
|---|---|---|---|
| `--wdt-surface` | figure surface (the page background in practice) | `#fcfcfb` | `#1a1a19` |
| `--wdt-ink-1`, `-2`, `-3` | primary, secondary and muted text | `#0b0b0b`, `#52514e`, `#898781` | `#f0efec`, `#c3c2b7`, `#898781` |
| `--wdt-grid` | gridline, 1 px solid | `#e1e0d9` | `#2c2c2a` |
| `--wdt-axis` | baseline and axis | `#c3c2b7` | `#383835` |
| `--wdt-s1` to `--wdt-s8` | categorical slots, fixed order | `#2a78d6 #eb6834 #1baf7a #eda100 #e87ba4 #008300 #6250d6 #e34948` | `#3987e5 #d95926 #199e70 #c98500 #d55181 #0ca30c #9085e9 #e66767` |
| `--wdt-o1`, `-o2`, `-o3` | ordinal ramp for S_low, S_central, S_high | `#86b6ef #2a78d6 #104281` | `#256abf #5598e7 #9ec5f4` |

Dark values apply under `@media (prefers-color-scheme: dark)` guarded for an explicit light choice, and under the site's own dark toggle. Which selector the Quarto toggle sets (a class on `body`) is to be confirmed in the first build test (M3 in `ids.md`); the figure stylesheet needs both scopes either way. The tokens are validated against `#fcfcfb` and `#1a1a19`; the implementer re-runs the validator against the site's real page background and re-steps any slot that fails (section 12).

**Entity colour rule (Color follows the entity).** Colour never follows rank or position in a particular figure.
- The WDT is always blue: the ordinal ramp when schedules are shown, slot 1 when one schedule is shown.
- The no-WDT baseline (scenario `s0` in OH1a) is always the muted ink token (`--wdt-ink-3`); the WDT line is blue. This is the emphasis form: one accent, one grey.
- Every other named entity gets a fixed slot from slot 2 up, recorded in one registry, `registry/figure-style.yml` (new): `entity id` to `slot`. Families that appear together get consecutive slots in a fixed order, so the validated adjacent-pair order holds. Initial families: the seven retired tax lines of O1d take slots 1 to 7 in the manifest's `per` order; the comparators of O5, O6 and O8 take slots 2 up in the order the research register lists them.
- A figure that needs more than eight colours is a design error: the checker fails it. The remedy is facets, not a ninth hue.
- All-pairs forms (`dot` with several comparators, `map` markers) are capped at three categorical series; a fourth folds into "Other" or the figure facets (`dataviz`: only the first three slots validate under all pairs). Adjacent forms (`line`, `stack`, `bar`) may use up to eight.

**Marks** (fixed across every figure): line 2 px, round join and cap; marker r = 4 px (8 px) with a 2 px surface ring; bars and columns at most 24 px thick, 4 px rounded at the data end, square at the baseline; a 2 px surface gap between touching marks; area and band wash at 10% opacity; gridlines and axes hairline, solid, recessive; no border drawn around a mark. Text never takes a series colour: labels, ticks and legends wear the ink tokens, with a colour key beside them.

**Type.** Axis ticks 11 px muted, `tabular-nums`; labels 12 to 13 px secondary; value labels 12 px primary. There is no chart title inside the SVG: the caption (ordinary HTML `<figcaption>`) is the title.

## 4. Same data for the drawing, the table and the CSV

How agreement is guaranteed, not hoped for:

1. **One source.** A function `figure_data(block, data_file, manifest, metrics)` returns a `FigureData`: a long list of records `(line, schedule, horizon, by, x, stat, value, unit)` plus the display rounding and labels. Nothing else reads the data file for a figure.
2. **Three emitters, one input.** `draw(fd)`, `table(fd)` and `csv(fd)` take only the `FigureData`. None of them calls the data file, rounds on its own, or sorts on its own.
3. **Indexed marks.** Every mark in the SVG carries `data-r` and `data-c`, its row and column in the reference table, and `data-v`, the displayed value. The shared script reads values for tooltips from the table cells, not from a second copy in the page.
4. **A self-check at the end of the figure step.** The build re-parses the emitted SVG, the table and the CSV and asserts: the same number of values in each; every `data-v` equals the table cell and the CSV `value` for that record; and the drawn position of every mark, inverted through the figure's scale, equals its value within half a pixel (this catches drawing bugs that rounding checks cannot). Any difference stops the build; there is no warning mode.
5. **Rounding is in one place.** The table and tooltip show the value rounded to the metric's display decimals. The CSV carries both the displayed value (`value`) and the unrounded one (`value_raw`), so a reader can rebuild the chart exactly and the check can verify `value == round(value_raw, decimals)`.

**Table shape.** The reference table in the Data block (`F-S5-1`) is wide: one row per x position (a year, or a category), one column per group (schedule, line or entity) crossed with `STAT` (`p10`, `mean`, `p90`; or `point`, `lo`, `hi` for `point_and_range`). The column header carries the unit once. A path of 100 years renders as a collapsed block (`<details>`, "Table F-S5-1, 100 rows") with a sticky header and the CSV link; it is still in the page and is printed in full.

**CSV shape.** Long (tidy), UTF-8, comma, no comment lines, one row per plotted value: `figure, output, line, schedule, horizon, by, x, stat, value, value_raw, unit, manifest_version, run_date`. The last two are constant per file so a downloaded file is self-describing. Path: `/data/csv/F-S5-1.csv` (reserved in `ids.md`). The data layer page DL5 lists every CSV.

## 5. Drawing rules

### 5.1 Rules that hold for every kind

- **Axes.** One value axis, never two. The value axis includes zero (every metric in the register is a share, a count or a year; a truncated axis misstates size); the zero line is drawn one step stronger than the grid. Linear only, never log. Ticks are round numbers, three to six, in full under 10,000. Where a set of figures compares the same quantity (the three horizons of one output, the facets of one figure), they share one value axis.
- **Labels.** Selective: label the end of a line, the mean of a `dot` row, the tip of a bar; never every point. A legend is always present for two or more series and sits above the plot; a single series has none (the caption names it). Direct labels also on up to four series. Where end labels would collide, use leader lines or facets, never nudged stacks.
- **Gaps and rings.** 2 px surface gap between touching marks; 2 px surface ring on markers.
- **Hit targets** are at least 24 px, larger than the mark.
- **Missing data.** A missing value is a gap in the line and an absent mark, never a zero. A record with a missing `p10` or `p90` in a `p10_mean_p90` output is a build error (the data file is incomplete), not a figure with a thinner band.
- **Fixture data never ships.** A data file flagged `fixture: true` makes every figure it feeds unresolved in a release build (the rule is stated in `hooks.md`; the figure step enforces it).

### 5.2 Summary forms

| Output `summary` | Drawn as | Table columns | Tooltip and caption words |
|---|---|---|---|
| `p10_mean_p90` | the mean (line, dot or bar tip) plus the interval from p10 to p90 | `p10`, `mean`, `p90` | "mean", "10th to 90th percentile of return risk" |
| `point_and_range` | the point, plus a range from `lo` to `hi` | `point`, `lo`, `hi` | "point", "low to high of the stated input range" (not percentiles) |
| `point` | the point only, no interval | `point` | |

The interval is the level-1 spread only (return risk, `metrics.md` range design). The level-2 spread (parameter ignorance) is the tornado (OT1) and is never mixed into a band; a figure may not draw both on one axis.

How the interval is drawn by kind: `line`, a wash between p10 and p90 behind the mean line; `band`, a floating range column with a 2 px mean tick across it; `dot`, a 2 px whisker with end caps behind the mean dot; `bar`, a 2 px whisker on the tip of the bar; `stack`, no per-part interval (parts do not add in quantiles), see 5.4; `map`, no interval (the cell shows the mean; p10 and p90 are in the tooltip and table).

### 5.3 Several schedules in one figure

`schedule: [S_low, S_central, S_high]` draws all three. The rule, with its rationale:

- **Colour.** S_low, S_central and S_high are three steps of one hue, in that order, so the reader sees an ordered family and not three unrelated series (the colour is not a rank of this figure; it is the schedule's own fixed identity).
- **Means for all three, interval for one.** The mean of each schedule is drawn in full. The p10 to p90 interval is drawn **for S_central only**; S_low and S_high show their means. Three overlapping washes hide each other and the lines; the table and the tooltip carry the interval of all three. The caption must say so (the F2 lint allows it: it states what is drawn). `layout: facets` draws three small panels on one shared axis, each with its own interval, when the author wants all three ranges visible (question Q2 adds this field; Q6 asks whether overlay is the right default).
- **Labels.** End labels "S_low", "S_central", "S_high" on a `line`, and a legend. Under the three-series ladder, colour alone is comfortable, but the labels remain.
- **Order.** Series are always drawn low, central, high, with S_central on top, so the band lies behind all three lines.

Fixture description (the test `FX-LINE-3S`, section 10): a line figure, x from year 0 to 100, y a share of GDP. The S_central mean is a 2 px line in step 2 of the ramp; its wash is that colour at 10% opacity, spanning p10 to p90 at each year; S_low is a 2 px line one step lighter and S_high one step darker, with no wash; the three end labels sit at the right edge, 10 px clear of the plot; the legend above the plot lists the three in order with a short line key; the zero line is stronger than the grid; the x axis is "Years since launch". The same figure passes in dark mode with the dark ramp.

### 5.4 The six kinds

Each rule says what the x axis is, what is drawn, and when the checker rejects the kind.

| Kind | x axis | What is drawn | The checker rejects it when |
|---|---|---|---|
| `line` | ordered numeric (year, grid value such as `alpha_grid`, `w_min`, `amplitude`) | one 2 px line per series; mean plus wash for `p10_mean_p90`; a marker on every point when there are twelve or fewer x positions (OP6 has four) | x is not ordered numeric; more than eight series |
| `band` | ordered categories, at most 12 (`wealth_band`, `income_decile`), vertical | one floating column per category from p10 to p90, at most 24 px wide, 4 px rounded at both ends, with a 2 px mean tick in the surface-contrasting ink; for `point_and_range`, the column runs lo to hi with a point tick | categories are unordered; more than 12 |
| `bar` | categories | one column or row per category, anchored on the zero baseline, 4 px rounded data end, the value at the tip; interval as a 2 px whisker on the tip. Vertical when there are six or fewer categories with short labels, otherwise horizontal | the quantity can be negative with no meaningful zero (use `dot`) |
| `dot` | named items as rows (systems, taxes, comparators, inputs), horizontal | one row per item: mean dot (r = 4, ringed), whisker for the interval with end caps, the mean value printed at the right of the whisker, rows in the order given by the data file (tornado: sorted by span, largest first) | more than 16 rows; more than three categorical series (all-pairs cap) |
| `stack` | ordered numeric or categories | stacked columns or an area stack of the parts of a sum, means only, 2 px gap between parts; negative parts stack below the zero line; a net line with its interval is drawn on top when the output has one (O1: M1a, M1b and M1c above zero, M1d below, net M1 as the line with its band) | the parts do not sum to the output's total in the data file within rounding; more than eight parts |
| `map` | two grid axes (`schedule_grid` by `w_min` for OF1) | a grid of cells, each one hue from the sequential ramp, lightest near zero; the feasible region (the cells that meet the stated closure, burden and saving conditions) is outlined 2 px in ink; S_low, S_central and S_high are marked by ringed dots on their cells; a colour scale with its unit sits beside the grid; one panel per line named in `lines` (OF1: F1, M2, M4a, side by side on wide, stacked on narrow) | the grid has more than 12 by 12 cells (cells fall below 24 px); the output has no two grid keys |

Notes the implementer needs:

- `stack` is the only kind that cannot draw an interval for its parts. Quantiles of components do not add up to the quantile of the sum, so the interval is drawn only for the total, and only where the data file holds one.
- `map` colours encode the mean; a sequential ramp is the correct job here (magnitude). The feasible-region outline carries information the colour does not, so it is not colour-alone.
- The tolerant-zone output (O7, `point_and_range`) and the sensitivity output (OS1) are `dot`: a point and a range on one axis, no more.
- A value that cannot be shown in the unit of its output (two numbers in different units under one output id, as OP4) is not drawn as one figure; see question Q5.

## 6. Every manifest `kind` has a drawing rule

The manifest's own field is also called `kind`; it names an output's role, not a drawing kind (question Q1). Table: manifest role, output ids, default drawing kind, notes. A figure block's own `kind:` overrides the default where section 5 allows it.

| Manifest role | Outputs | Default drawing kind | How it is drawn |
|---|---|---|---|
| `headline` | O1 | `stack` | M1a, M1b and M1c above zero, M1d below, net M1 as the line with its p10 to p90 band |
| | O2, O4a, O4b | `band` (by `wealth_band` or `income_decile`); `dot` when `by: overall` | floating interval column per band, mean tick |
| | O3 | `dot` | one row per schedule (it has no `by`) |
| `line` | O1a, O1b, O1c | `line` | one line, year on x |
| | O1d | `stack` | seven receipts lines, slots 1 to 7 in the `per` order; legend only, no direct labels |
| `comparison` | O5, O6, O8 | `dot` | one row per system compared, WDT row first; the comparator rows use their fixed entity slots |
| `supporting` | O7 | `dot` | point with its range |
| | OB1, OD1 (proposed) | `line` | x is `w_min` or `alpha_grid` |
| | OF1 (proposed) | `map` | section 5.4 |
| | OT1 (proposed) | `dot` | tornado: inputs as rows sorted by span, `point_and_range`; the three headlines as facets sharing nothing, one axis each, in their own units |
| `path` | OP1 | `bar` | years to fill, short and long reserve, with whisker |
| | OP3 | `line` | cumulative shortfall by year; the zero line is the point of the figure and is drawn stronger |
| | OP4 | `bar` | see Q5: needs one output id per number |
| | OP5 | `dot` | one row per retired tax, in retirement order; x is the year |
| | OP6 | `line` | four points (years 10, 25, 50, 100), markers on, wash between them |
| | OR1, OW3 (proposed) | `line` | by `amplitude` or by `entry_year` |
| `headline_support` | O2b, O2c | `band` | by `wealth_band`; the second `by` key is fixed with `at:` (Q2, Q5) |
| | OM1, OL1 (proposed) | `stack`, `band` | OM1 as O1; OL1 by `reference_worker` |
| `sensitivity` | OS1 | `dot` | two rows, response off and on, `point_and_range` |
| `comparison` (welfare, proposed) | OW1, OW2 | `dot`, `band` | OW1 by `tax_system`; OW2 by `holding_period` |
| `problem` (proposed) | OH1a | `line` | two scenarios: baseline in the muted ink, WDT in blue, with bands |
| | OH1b, OH1c | `dot`, `band` | by `wealth_band` |
| `data_fact` (proposed) | DH1a, DH1c | `bar`, `band` | point values; `point_and_range` for DH1c |
| | DH1b | `stack` | tax mix by head |
| `check` (proposed) | CK1 | `line` | by `amplitude` |

The proposed roles (`problem`, `data_fact`, `check`) and entries come from `model-specs/added/` and are not yet in `outputs.yml`; the table fixes their drawing so the manifest can adopt them. Roles that do not draw (a manifest entry with no figure) need no row.

## 7. Units and axis labels from the metric register

- **Value axis title:** the unit of the metric, taken from the register's `Unit` column (for example "% of GDP"), plus the denominator where the register names one. The metric name is not repeated: the caption says what is plotted.
- **X axis title:** "Years since launch" for year-indexed outputs (the register's convention: t is years since launch); for category axes the label of the `by` key (for example "Wealth band"); for grids, the key labels.
- **Money** is base-year pounds, as the register states, and the base year appears in the axis title wherever pounds are plotted.
- **Display rounding** comes from the register, per metric. `metrics.md` does not yet carry a decimals field, and the M1 unit cell holds two units ("% of GDP and real £bn"); both need a decision (question Q4). Until then the renderer refuses to draw a metric with no decimals, so no figure carries an invented precision.
- **Tick labels** are in full under 10,000 and compact above, one style per axis; horizons on facets repeat the unit once at the first panel.
- **By-keys and their values** (the names and the order of the wealth bands, the deciles, the systems, the retired taxes) come from the data file's schema. The manifest lists keys, not their labels or order; question Q4 asks for them in the data file.

## 8. Alt text and keyboard access

**Structure.** Each figure is `<figure>` with `<figcaption>` (the caption, ending in the link to its table). The SVG has `role="img"` and `aria-label` set from `alt`, `aria-describedby` pointing at the caption. A visible "Table" link and a "CSV" link sit under the caption, and the table is in the page (Data block), so every value is reachable without sight, a pointer or a script.

**Alt text.** Required. Describes the form, never the finding (template rule): "Line chart of fund assets as a share of GDP against year, with a shaded range." The alt lint (question Q8, extending F1 to F6): 20 to 250 characters; begins with the chart form ("Line chart", "Dot plot", "Bar chart", "Range chart", "Stacked chart", "Heat map"); contains none of the F2 result words and no figure of three or more digits other than years. The renderer can propose an alt from the kind, the units and the series, to be reviewed; it never fills in a finding.

**Keyboard.** One tab stop per figure (the SVG, `tabindex="0"`, role `img`, with the keyboard mode announced as a hint in `aria-description`). When focused:
- Left and right arrows move along x positions (years or categories); up and down move between series where there is more than one.
- A tooltip, shown as a live readout (`aria-live="polite"`), gives the x position and the values of every series at that x, read from the table cells the marks point to. Home and End jump to the first and last x; Escape clears.
- The same readout appears on pointer hover. Hover and focus carry identical content.

No mark is a separate tab stop: a hundred-year path would make a hundred stops.

**Colour and contrast.**
- Identity never rests on colour alone: a legend always, end labels or row labels on up to four series, ordered lightness in the schedule ramp (reads in grayscale), texture under print and forced colours.
- Three light-mode categorical slots (aqua, yellow, magenta) fall under 3:1 against the surface, a WARN in the validator. The relief the skill demands is met by construction, because the table view is always present; the rule is stated here so nobody drops the table.
- `forced-colors: active`: marks use `CanvasText` and `Highlight`, bands become hatched fills, the legend keys carry the hatch.
- `prefers-contrast: more`: gridlines move one step up in contrast.

**Touch.** Hit areas of at least 24 px; no hover-only information.

## 9. Print and PDF

- **Print stylesheet.** `@media print` switches the figure to the light set regardless of the site theme, hides the toolbar and the tooltip layer, turns on texture (the `dataviz` fill at 45 and 135 degrees on bands, areas and stacked parts, tone on tone, one step darker than the fill), and shows the wide layout. Collapsed tables print open.
- **Standalone SVG per figure** at `/data/fig/fig-S5-1.svg`: the wide layout with the light colours inlined, texture on, fonts named `"DejaVu Sans", Arial, sans-serif` so a converter without the system stack still lays out text. This is the interface for the PDF and Zenodo builds, which are designed later (question Q10 in `ids.md`): `pdf.py` converts these files, and nothing in the HTML pipeline depends on that choice.
- **Tables in the PDF.** The Data block tables print in full as ordinary tables.
- **Colour in print.** The ordinal schedule ramp reads in grayscale by its lightness steps; categorical series carry end labels and texture; the muted baseline stays muted.

## 10. Test list (fixtures from fake data)

Fixtures live with the renderer's tests when it is built. They are generated from a seeded function (seed fixed in the test), never from the real data file or the model, flagged `fixture: true`, and their output goes to the build's test folder, never to `_site`. The numbers have no meaning; they exercise geometry and rules.

| Id | What it draws | Pass condition |
|---|---|---|
| FX-LINE | `line`, one schedule, `p10_mean_p90`, 100 years, one output | mean 2 px, wash 10% opacity from p10 to p90, zero line stronger, x title "Years since launch", no legend |
| FX-LINE-3S | the three-schedule fixture of section 5.3 | wash for S_central only; three end labels; legend of three; table has nine value columns |
| FX-LINE-PTS | `line`, four x positions (OP6 shape) | markers on every point, r = 4, ringed |
| FX-BAND | `band`, `wealth_band`, ten categories | floating columns at most 24 px, mean tick, categories in the data file's order |
| FX-BAR | `bar`, six categories, one negative value | baseline at zero, rounded data end, value at the tip, whisker, negative bar extends below |
| FX-DOT | `dot`, five comparators, one WDT row | WDT first and blue, comparators in fixed slots, all-pairs cap enforced at three series |
| FX-DOT-TORNADO | `dot`, `point_and_range`, eight inputs | rows sorted by span, range labelled low to high |
| FX-STACK | `stack`, M1 shape: three positive lines, one negative, net with band | negative below zero, parts sum to the total within rounding, net line on top |
| FX-STACK-7 | `stack`, seven parts (O1d shape) | legend only, no direct labels, slots 1 to 7, adjacent gaps 2 px |
| FX-MAP | `map`, 9 by 7 grid, three panels | sequential single hue, feasible outline, three schedule markers, scale with unit |
| FX-SCEN | `line`, baseline against WDT scenario (OH1a shape) | baseline in the muted ink, WDT in blue, both with bands |
| FX-POINT | `point_and_range` and `point` outputs | "low", "high" words, no percentile words, `point` draws no interval |

Cross-cutting tests:

| Id | Check |
|---|---|
| T-ROUND | The self-check of section 4 on every fixture: counts, `data-v`, table, CSV, and inverted positions within half a pixel; each of four deliberate corruptions (one value changed in the SVG, the table, the CSV, a mark moved 3 px) is caught |
| T-CAP | `p10` missing on one record fails the build; a ninth series fails; a map of 13 by 13 fails; `fixture: true` fails a release build |
| T-LINT | Captions and alt text of every fixture pass F1 to F6 and the alt lint; one deliberately bad caption per rule is rejected |
| T-THEME | Light and dark renders of every fixture checked by screenshot; forced-colors and print renders produce texture and the light set |
| T-NARROW | Every fixture at 360 px: no clipped text, no overlapping labels, narrow layout shown |
| T-KEY | Keyboard: tab reaches the figure, arrows move along x, the readout equals the table cells, Escape clears; the same with the script disabled still leaves the table and static labels |
| T-PAL | `validate_palette.js` run on each token set against the site's real background; any FAIL stops the build of a style change |
| T-WEIGHT | Each fixture within the 40 KB budget; the page's shared CSS and script within 3 KB and 4 KB |
| T-PRINT | The standalone SVG of every fixture converts to PDF by the converter the PDF build picks, with text intact |

## 11. Questions for the author

**All eight answered 2026-11-17: each proposed answer accepted.** The text below is kept as the record of the question and the decision.

**Q1. The word `kind` has two meanings.** In `outputs.yml` it is an output's role (`headline`, `line`, `comparison`, `path`, and so on); in a figure block it is the drawing kind (`line`, `band`, `bar`, `dot`, `map`, `stack`). `line` is in both lists and means different things. *Proposed:* no file change; every document calls the manifest field the "role" and the figure field the "kind", and the checker validates a figure's kind against the role-to-kind table in section 6. If you would rather rename the manifest field to `role`, it is a one-word change in `outputs.yml` and its readers.

**Q2. Four optional fields for the figure block.** `template.md` section 6a has no way to pick one of several `lines` in an output, one of two `by` keys, one of several units, or the three-schedule layout. *Proposed additions, all optional:* `lines: [M1a]` (default: all the output's lines), `at: {share_of_payers_above_cutoff: 10%}` (fixes a second `by` key), `unit: "% of GDP"` (where the register lists more than one), `layout: overlay | facets` (default overlay). The guru owns `template.md`; this brief does not edit it.

**Q3. What does `horizon` select on a year-indexed output?** The register defines three windows (transition, short, long), but a path over years already spans them, and the transition window ends in a different year on every draw. *Proposed:* a line over years plots the full path with the three windows marked as light bands behind the x axis (at the median window ends, labelled), and `horizon` is not given for it; for outputs that hold one value per horizon, `horizon: short` picks one and `horizon: [transition, short, long]` draws three panels on one shared axis. The data file must say which of the two shapes each output has.

**Q4. Register fields the renderer needs.** (a) A `decimals` field per metric, or per output line; (b) M1's unit cell reads "% of GDP and real £bn", so which does a figure plot (the proposal above puts it in the figure block's `unit:`); (c) the labels, display order and short forms of every `by` key and its values (the ten wealth bands, the deciles, the systems, the retired taxes) in the data file's schema. *Proposed:* all three are fields of the data file written by model v3 and the metric register's generated JSON (brief 018s owns that parse); nothing is hard-coded in the renderer.

**Q5. Gaps in the manifest.** OP4 holds two numbers in different units (a ratio and a year), O2b and O2c have two `by` keys that are not both axes, and O3 is a single value. *Proposed:* the guru splits OP4 into two output ids (for example OP4a, OP4b), and the second `by` key of O2b and O2c is handled by `at:` (Q2). Neither is done here.

**Q6. Intervals when three schedules are overlaid.** The default draws the interval for S_central only (section 5.3), so the figure does not show S_low's and S_high's return-risk ranges; they are in the table and tooltip. *Proposed:* keep it. Alternatives: draw all three washes (they overlap and hide the lines, measured on the fixture description, not tried here), or default to `facets`, which shows all three at three times the space. Say which you want as the default.

**Q7. Does the hub have a Data block?** A figure's table must sit on the same page as the figure (the keyboard readout reads the table cells; rule 3 puts tables only in the Data block). *Proposed:* the hub carries a Data block like a spoke, collapsed by default at the foot of the page, listing the tables of the figures it draws.

**Q8. Alt-text lint.** `template.md` lints captions (F1 to F6) and says alt text describes form, not the finding, but nothing checks it. *Proposed:* add F7 as in section 8 (length, form word, no result words, no three-digit figures).

## 12. Checks run

| Check | Result |
|---|---|
| `validate_palette.js`, ordinal ramp light (`#86b6ef`, `#2a78d6`, `#104281`) | all checks pass: lightness monotone, steps at least 0.06 apart in L, lightest step 2.06:1 against `#fcfcfb`, one hue |
| `validate_palette.js`, ordinal ramp dark (`#256abf`, `#5598e7`, `#9ec5f4`) | all checks pass; darkest step 3.23:1 against `#1a1a19` |
| `validate_palette.js`, eight categorical slots, light | all checks pass: worst adjacent CVD pair 9.1 (yellow beside aqua), worst adjacent normal-vision pair 19.6; WARN: aqua, yellow and magenta under 3:1 on the light surface, relief by the always-present table and labels |
| `validate_palette.js`, eight categorical slots, dark | all checks pass: worst adjacent CVD pair 8.4, normal-vision 19.3, all eight at least 3:1 |
| Every `kind` value in `outputs.yml` has a drawing rule | seven values on `main` (`headline`, `line`, `comparison`, `supporting`, `path`, `headline_support`, `sensitivity`) and the three proposed (`problem`, `data_fact`, `check`): all in section 6 |
| Every `by` key on `main` | `overall`, `wealth_band`, `income_decile`, `share_of_payers_above_cutoff`: categories drive `band`, `dot`, `bar`; the proposed grid and numeric keys drive `map` and `line` |
| Not run | the palette against the site's real page background (the site's theme files were not opened); any render of a figure (nothing is built); the Quarto dark-mode selector |
| Touches | this file and brief 019's progress block only |
