# D9 provenance and status (demographic conventions; documentation only)

Date: 15 October 2026. Hook: none. Record the convention and its historical range. Companion: `coverage_matrix_d9.csv`.

## Findings

1. **Adults per head (`pop_per_adult`, fixed at 1.27 in the model).** Not verified. The ONS mid-year estimates were not opened (the search returned local-area pages only). The convention stays recorded as 1.27, with no range established. Whether it is 16+ or 18+ is not confirmed.
2. **Age at inheritance.** From the ONS article (WAS July 2014 to June 2016, individuals): the share receiving an inheritance rises with age and is highest at 55-64. The Resolution Foundation projects that the most common age at which today's 20 to 35 year olds in the UK will inherit is 61. The article reports no average recipient age, and counts only inheritances of 1,000 pounds or more received within two years before interview. Historical range not found.
3. **Generation gap (`G`).** Not located. The model's `G` governs the death-phase lines and heir receipts in `run_family` and `rates_core`; it is a stylised parameter, not data. An age at inheritance of about 61 against a mean age at childbirth would imply a generation gap near the length of a parent's remaining life; neither figure was verified here.

## Gate

None. Documentation only.

## Open

1. ONS mid-year estimates: adults per head over a long run.
2. ONS mean age of mother at birth, and a long-run age-at-death or inheritance-age source.
