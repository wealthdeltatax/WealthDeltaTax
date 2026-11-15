# D2 provenance and status (consumption and saving by wealth)

Date: 15 October 2026. Status: coverage census only; no values extracted. Companion: `coverage_matrix_d2.csv`.
Hook: shape curve in `_c_cell`, rescaled to the country c. Gate (spec): shape evidence for at least UK, US and one Nordic country; others pooled.

## What was opened

| Source | Status | Opened |
|:---|:---|:---|
| Saez and Zucman (2016), NBER w20625 | verified (text) | Saving-rate passage and method; text cut off mid-sentence. Appendix and data files not opened (appendix PDF located on the author site). |
| Fagereng, Holm, Moll, Natvik, NBER w26588 | partly | Abstract only. |
| Dynan, Skinner, Zeldes (2004), NBER w7906 | partly | Abstract only. |
| IFS, use of financial wealth in retirement (ELSA) | partly | Summary page. |
| Mian, Straub, Sufi | not located | Named in spec only. |
| WAS saving by wealth | not found | Only stocks seen in D3 pass. |

## Findings

1. **US.** Saving as a share of pre-tax income rises with wealth in the capitalized-income data: bottom 90% about 3%, next 9% about 15%, top 1% about 20-25%. The bottom 90% fell from 5-10% in the late 1970s to about -5% in the mid-2000s. Top 1% saving was negative in the 1930s.
2. **Norway.** Net saving rates (no capital gains) are about flat across wealth; gross rates (with capital gains) rise sharply. "Saving by holding" explains up to 80% of Norway's rise in wealth-to-income from about 4 to 7 (1995-2015).
3. **UK.** Only ELSA drawdown evidence: financial wealth, ages 50+, England. Wealthiest half drew down 39% between 70 and 90, the least wealthy half 13%. No top-tail split.
4. **Dynan-Skinner-Zeldes.** Saving rates rise with lifetime income; supports precautionary and bequest motives. Years not stated on the page.

## Definition fidelity (principle 4)

- **Concept gap.** The model's c is net drawdown over wealth (consumption minus saving, may be negative). The sources give saving over income (US, DSZ) or saving over wealth or income by percentile (Norway, normalisation not seen). Conversion needs wealth/income by group, which D1 and the US sources supply only partly.
- **Net versus gross.** Norway shows the answer depends on whether capital gains count as saving. The model taxes saving as delta and decomposes returns from saving inflow, so Norway's net measure is the like-for-like one. The US synthetic measure's treatment of gains was not confirmed.
- **Synthetic versus observed.** US saving is synthetic (derived from wealth change net of price effects), not observed.

- **Unit (added 15 Oct).** The WDT is per adult. The saving and drawdown sources rank households (Norway, ELSA, SCF-based work) or tax units, so the percentile shape is not strictly per adult. Under the equal-split baseline each adult takes the household's rank and saving profile; as-owned would need individual-level evidence.

## Gate

US: evidence exists (Saez-Zucman), pending anchor extraction and conversion. Nordic: Norway exists at abstract level. UK: only partial, via ELSA financial wealth for over-50s; no WAS saving by wealth found. Gate not yet met for the UK; fallback is a pooled shape, grade C, flagged.

## Open

1. Read the Saez-Zucman appendix and the Fagereng et al. paper body for percentile anchors.
2. Locate UK evidence (WAS saving by wealth, IFS or Resolution Foundation work).
3. Locate Mian-Straub-Sufi.
