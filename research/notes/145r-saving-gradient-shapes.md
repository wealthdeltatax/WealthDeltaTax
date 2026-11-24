# 145r: Saving by wealth, three gradient shapes (flat, mild, steep)

Accessed 2026-11-23. Brief `docs/briefs/145r-withdrawal-and-saving-evidence.md`. Evidence and confidence only; nothing is computed in the model and no shape is tuned to reach 0.50.

Status: done (block 2 of brief 145r).

## 1. Summary

- **No held source gives a UK saving rate by wealth band.** The nearest held statements are by *income* quintile and for *liquid savings only* (Resolution Foundation, *Before the Fall*, WAS, pandemic window: typical rise in liquid savings £80 in the lowest income quintile against £4,200 in the highest, pp. 7 and 32, text) and one foreign banded shape in the register (I-W3a, Norway: net active saving about 6 to 8% of disposable income, roughly flat above the 20th percentile, near zero around the 15th). Direction of a gradient is supported; its size by wealth is `unset`.
- Three shapes over the model's 14 lines (D1 to D9, D10a, D10b, RL3, RL2, RL1), in `saving_shapes.csv`: `flat` (today, default), `mild` (a 7 point step: the two lowest lines save less, every other line the same) and `steep` (that step plus a 7 point linear rise in wealth rank to the top). Offsets are in points of line income. **Scaling:** additive, with an income-weighted mean of zero, so aggregate saving equals `flat`'s exactly at each of the three flat values (checked to 1e-12). Magnitudes are `scenario`; the step in `mild` is `proxy` for its shape and `scenario` for its size.
- Not tuned to reach 0.50. Direction only for concentration (section 3.3); nothing is computed in the model.


## 2. What the held sources say about saving by wealth (page, flag)

Rows are in `research/tables/145r-saving-shapes-and-withdrawal-range/saving_evidence.csv`. The Resolution Foundation (RF) figures are asserted on their PDF pages by `saving_shapes.py` (RF printed page = PDF page).

| Figure | Value | Page | Flag | Limit |
|---|---|---|---|---|
| Typical family, lowest income quintile: rise in liquid savings, 2019-20 to 2021-22 | £80 | 7, 29 | text | income quintile, liquid savings, pandemic |
| Typical family, highest income quintile, same | £4,200 (£4,100 on p. 29) | 7, 32 | text | same |
| Second income quintile, against the two years before | more than £300 against £100 | 32 | text | the chart label (£310) is not used |
| Families that increased liquid savings, bottom and top income quintile | 55%; 64% | 38 | text | pandemic-era surveys showed 23%; 45% |
| Active share of the growth in average family wealth, since 2010-12; latest period | 47%; 40% | 21 | text | aggregate; includes debt repayment; excludes DB and pensions in payment |
| Adjusted household saving ratio, peak | 25% (Q2 2020) | 30 | text | aggregate |
| I-W3a Norway: net active saving, flat from about the 20th percentile, near zero around the 15th | 6 to 8% of disposable income | source pp. 2, 24-25 | read from register row; source not held | foreign; the only banded shape held |
| I-W3b Norway: gross saving rate of the top 1% | about 35% | source pp. 2, 25 | read from register row | context only by author ruling; includes capital gains; not used |
| I-W3c UK: net saving as a share of the change in financial wealth | 7 to 24% | source p. 18 | read from register row | aggregate, not by band |

The EER paper (Advani, Summers and Tarrant 2025), the IFS wealth-distribution report and the ONS Table 2.x workbooks were searched for saving: none gives saving by wealth. The 095r evidence map reaches the same conclusion ("no UK source identifies any flow by wealth band as a rate on wealth").


## 3. The three shapes and the aggregate-saving scaling

**3.1 Definition.** The model's `flat` shape gives every line one saving ratio of line income, `s` (the min, median and max of the ONS non-pension ratio: -2.61%, 1.01%, 13.54%, from `docs/model-v3/household-arm-account/account_table.csv`). A shape gives line i the ratio `s_i = s + delta_i`, with `delta_i = A (h_i - hbar)`, where `h_i` is the shape index of the line, `w_i` its share of income (adults times income per adult, as `runner/arm.py` builds it), and `hbar = sum(w_i h_i)`. Then `sum(w_i s_i) = s` for every `s`, so aggregate saving equals `flat`'s. The scaling is additive because `s` can be negative: a multiplicative scaling would make the lowest flat value deepen dissaving at the top.

| Shape | Index `h_i` | A | Evidence class |
|---|---|---|---|
| flat | 0 | 0 | default (today) |
| mild | 1 for lines above the 20th adult percentile (D3 up), 0 for D1, D2 | 7 points | shape `proxy` (Norway I-W3a: about zero below the 15th, 6 to 8 above); size `scenario` (the Norwegian step, 6 to 8 points, taken at its midpoint) |
| steep | the mild step plus a linear rise from the middle of D3 (25th percentile) to 100 | 7 points | `scenario`: direction from RF (income gradient in liquid savings), size has no evidence; twice the mild slope by choice |

**3.2 Offsets by line** (`delta_i` in points of line income; the ratio at the median flat value, 1.01%, is in the CSV together with the min and max). Income share is the weight `w_i`.

| Line | Adult percentile (mid) | Income share | mild | steep |
|---|---|---|---|---|
| D1, D2 | 5, 15 | 7.2% each | -6.00 | -9.12 |
| D3 | 25 | 7.2% | +1.00 | -2.12 |
| D4, D5 | 35, 45 | 9.0% each | +1.00 | -1.19, -0.25 |
| D6, D7 | 55, 65 | 11.2% each | +1.00 | +0.68, +1.61 |
| D8, D9 | 75, 85 | 12.7% each | +1.00 | +2.55, +3.48 |
| D10a | 94.5 | 11.4% | +1.00 | +4.37 |
| D10b | 99.5 | 1.3% | +1.00 | +4.83 |
| RL3, RL2, RL1 | about 100 | under 0.001% | +1.00 | +4.88 |

Income per adult is the pack band mean (I-D9a to I-D9d); D1 to D3 take the lower bound of I-D9a, so their income shares are equal by construction, not observed.

**3.3 Expected direction for concentration (not computed).** The model's untaxed top-band share falls from 0.41 at year 0 to 0.20 to 0.34 at year 100 across the flat values, against about 0.50 observed (`docs/model-v3/household-arm-validation.md`, BF-13; the observed figure is on a different valuation). Both shapes move saving from the bottom lines to the rest with aggregate saving fixed, so they can only raise the top share relative to `flat`. `mild` raises every line from D3 up by the same 1.0 point: its effect on concentration is small. `steep` gives the top lines +4.4 to +4.9 points: a larger effect, with the size depending on how large saving is against the return on a top line's wealth. Neither is tuned, and the note makes no claim that either reaches 0.50: the gap also includes a definitional part (valuation, per-adult families) and no transitions between lines.


## 4. Unset, and challenge note

**Unset:** the UK saving ratio by wealth decile or by tail line; saving by wealth band as a share of income; the saving of the top 1% and the named list; any link between income gradient and wealth gradient in the model's lines; the sign of saving at the bottom (the Norwegian row says near zero, the `mild` and `steep` shapes push D1, D2 to about -5 points at the median flat value, which is a scenario outcome, not an estimate).

**Challenge.**
1. **Wrong axis and asset.** RF is by income quintile and measures the change in liquid savings in pounds, not a saving ratio of income, and covers a pandemic window with furlough and lockdown saving. It supports the direction of a gradient, not a size.
2. **Foreign shape.** The only by-wealth shape is Norwegian (2005-2015), read from the register row; the source is not held here. It is flat above the 20th percentile, which is a case for `mild` and not for `steep`.
3. **Top-line magnitude.** `steep` has no evidence for its slope. The Norwegian 35% for the top 1% (I-W3b) includes capital gains and is context only by author ruling; it is not used to size the slope.
4. **Income and wealth.** Lines are ranked by wealth, the evidence by income; high-income households are not the same set as high-wealth households.
5. **Low-line income.** D1 to D3 have one income value, so a gradient inside them cannot be set.
6. **Scaling convention.** Additive offsets keep aggregate saving equal to `flat` but change the ratio at every line; a multiplicative scaling would instead keep ratios proportional and fails for the negative flat value. This is a choice for the author.
7. **Not for revenue.** Nothing here is chosen for its effect on WDT revenue or closure.


## 5. Reproduction

`python -I research/scripts/saving_shapes.py` from the repo root (needs `pdftotext`; reads the pack and register read-only through `model_v3.core.pack` and `base.build_base` at ratio 0.44). It asserts the RF figures on their PDF pages, builds the shapes, checks that aggregate saving equals `flat`'s at the three flat values for every shape, writes `saving_shapes.csv` (42 rows) and `saving_evidence.csv` (9 rows) and prints one `ok:` line; it exits 1 on any failed check. Check: `python -I pipeline/check_agent_docs.py`.

