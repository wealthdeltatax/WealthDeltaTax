# 099r — held research PDFs and household-flow moments

**Status: blocked before extraction.** No quantitative moments are reported in this note. The required local PDF reader could not be run in this session because the GitHub-connected environment exposes repository text but not a local checkout or readable binary attachments.

## Work attempted

- Confirmed the brief and all required upstream notes on `main`; 097r and 098r data folders are present and the 098r close-out supersedes its first-pass conclusions.
- Confirmed the held PDF inventory in `Research/`.
- Tried a shallow clone of the public repository to obtain a local checkout for `pdftotext`/equivalent. It failed: `fatal: unable to access 'https://github.com/wealthdeltatax/WealthDeltaTax.git/': Could not resolve host: github.com`.
- Tried opening the held PDFs through their raw GitHub URLs. The connector returned `DisabledError` for each attempted binary PDF.
- The brief explicitly requires page-checked extraction from the held files and says not to work from search summaries. Accordingly, no figures have been taken from search snippets or treated as verified moments.

## Held PDFs awaiting a readable local copy

The brief's named set is:

1. `Before-the-fall.pdf`
2. `Fiscal Studies - 2021 - Advani - Behavioural responses to a wealth tax.pdf`
3. `Summers 2023 (OxREP).pdf`
4. `TippetZucman2026.pdf`
5. `Koster_How-do-households_Author.pdf`
6. `1-s2.0-S0014292125001266-main.pdf`
7. `1475_5890.12286.pdf`
8. `Adam et al. (IFS).pdf`
9. `Final_The_IFS_Green_Budget_2025_full_report_amended 2.pdf`
10. `Effects of taxes and benefits on UK household income financial year ending 2024.pdf`

The Bozio, Emmerson, O'Dea and Tetlow (2013) paper is deliberately not repeated; the guru's reading is already recorded in `docs/research/095r-bozio-2013-reading.md`.

## Data not re-extracted

The existing checked data in `docs/research/data/097r/` and `docs/research/data/098r/` remain the source for ONS household flows and saving/pension split, NBS stocks, NMG variable inventory, HMRC tables, WAS tables 2.5/2.11/2.13, ONS population and qx, and ETB tables 3b/4b. No duplicate extraction or invented reconciliation is added here.

## Next step

Provide a local checkout or upload a ZIP containing the named PDFs (or the full `Research/` directory). Then run the repository's PDF conversion tool or `pdftotext -layout`, retain page breaks, read each relevant PDF in full, and complete the moments table against the held files. Do not promote any search-result figure to a parameter or validation target.

## Moments table

Not created: there are no page-verified PDF moments to enter. Creating an empty CSV would falsely imply the extraction stage had been completed.
