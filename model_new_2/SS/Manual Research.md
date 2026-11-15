Everything below is a link I saw in this session, so none are guessed. The ODS and XLSX files are the ones I couldn't download myself, but I can read them once you attach them. If a hashed gov.uk file link has gone stale, use the landing page next to it.

## Priority 1: unblocks the most

1. **WID national wealth (D1, and D8 if you want top shares)**
   - Links: [data page](https://wid.world/data/), [codes dictionary](https://wid.world/codes-dictionary/)
   - Send: a CSV of private and national wealth for AU, CA, CH, DE, DK, ES, FI, FR, GB, IT, JP, NL, NO, PT, SE, US, with the metadata or interpolation flags if the download has them. I couldn't confirm the exact indicator codes (`mweal`/`wweal`), so choose them in the custom-download screen.
   - It settles the JPN and AUS start years, and which years are interpolated for every country.
2. **OECD Revenue Statistics, UK code 1200 (D5)**
   - Links: [data explorer short link](http://data-explorer.oecd.org/s/nb), [UK country note PDF](https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/12/revenue-statistics-2025-country-notes_3708be73/united-kingdom_b41737ed/42b45291-en.pdf)
   - Send: the UK, tax type 1200, % of GDP, 1990–2024 as a CSV. If the explorer is awkward, the country note PDF is the fallback.
   - It sets the 5-year trailing average (about 2.65–2.85% on old data, against the 3.2% in the spec).
3. **HMRC tables (D5 and D6)**
   - Links: [CGT page](https://www.gov.uk/government/statistics/capital-gains-tax-statistics), [IHT page](https://www.gov.uk/government/statistics/inheritance-tax-liabilities-statistics), [Corporation Tax statistics 2025](https://www.gov.uk/government/statistics/corporation-tax-statistics-2025)
   - Send these files:
     - [CGT Table 2, size of gain](https://assets.publishing.service.gov.uk/media/6a7b240b423b0bdba0290eca/Table_2_2026_Size_of_gain.ods)
     - [CGT Table 3, size of gain by income](https://assets.publishing.service.gov.uk/media/6a85a2e654bcee010d51454b/Table_3_2026_Size_of_gain_by_income.ods)
     - [IHT Table 12.3](https://assets.publishing.service.gov.uk/media/6a60bb8534dfb74772f96d28/table_12_3_final.ods) and [Table 12.1](https://assets.publishing.service.gov.uk/media/6a61fe84243ee000f7127e8b/table_12_1_final.ods)
     - [Receipts table `NS_Table.ods`](https://assets.publishing.service.gov.uk/media/6aa923f20420ac660805f7f2/NS_Table.ods)
     - The data tables ODS from the Corporation Tax statistics 2025 page.
   - Your D6 register cites Table 12.4 for assets by net estate band (2019-20). A fetch of the 2023-24 IHT commentary pointed to 12.3 for that. Send both if you can find both.

## Priority 2: closes specific open items

4. **English Housing Survey tenure (D3)**
   - Links: [tenure trends collection](https://www.gov.uk/government/statistical-data-sets/tenure-trends-and-cross-tenure-analysis), [Chapter 1 Trends in tenure, 2013-14](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/461440/Chapter_1_Trends_in_tenure.pdf)
   - Send: [FT1101 Trends in tenure](https://assets.publishing.service.gov.uk/media/6a4d9a8892f65594cb02999e/FT1101_Trends_in_tenure.ods), and "Annex Table 1" behind Figure 1.1 (it's linked from the 2013-14 household report page, [here](https://www.gov.uk/government/statistics/english-housing-survey-2013-to-2014-household-report)).
5. **Saez-Zucman saving rates by wealth group (D2)**
   - Links: [data zip](https://gabriel-zucman.eu/files/uswealth/SaezZucman2016.zip), [main data xlsx](https://gabriel-zucman.eu/files/SaezZucman2015MainData.xlsx), [appendix PDF](https://gabriel-zucman.eu/files/SaezZucman2016QJEAppendix.pdf)
   - Send: the zip or xlsx. I need the Table B33 sheet and a top 0.1% saving rate if there is one.
6. **UK median house price (D10 placeholder)**
   - Link: [ONS HPSSA year ending December 2017, related data](https://www.ons.gov.uk/peoplepopulationandcommunity/housing/bulletins/housepricestatisticsforsmallareas/yearendingdecember2017/relateddata)
   - Send: the national/regional median price paid dataset (the page lists several, so pick the median, not the mean). Or just the 2017 median figure.
7. **ONS population (D9, D10)**
   - Links: [mid-2017 bulletin](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/bulletins/annualmidyearpopulationestimates/mid2017), [UK/E&W/Scotland/NI population estimates dataset](https://www.ons.gov.uk/Peoplepopulationandcommunity/Populationandmigration/Populationestimates/Datasets/Populationestimatesforukenglandandwalesscotlandandnorthernireland)
   - Send: the UK mid-year estimates by single year of age (the longest time series you can find, 1971 onwards). That gives the 16+/18+ split over time.
8. **JST house-price documentation (D7)**
   - Link: [macrohistory.net/database](https://www.macrohistory.net/database/), then "Documentation - House Price Data" (`NPLH_documentation.pdf`).
   - Send: the pages for Italy, Spain and Portugal. The PDF downloads as an image with no text, so I can't read it.

## Priority 3: you'll need to ask someone or find it yourself

9. **Moatsos et al. data (NLD):** email the authors. The working paper is [here](https://shs.hal.science/halshs-04104429/file/WorldInequalityLab_WP202219.pdf); it names no data link.
10. **Abildgren data (DNK):** the [journal article](https://ideas.repec.org/a/hhs/jdaecn/0021.html) says the dataset is available from the author on request.
11. **Kuvshinov and Zimmermann Data Appendix (tables E.1–E.17)**
    - Search for "The Big Bang: Stock market capitalization in the long run" (CEPR DP 14468; also MPRA 88581).
    - I never got a working URL for the appendix, so I can't give you a link.
    - Send: the appendix PDF, or the data if it is online.
12. **WAS data dictionary (SN 7215):** I didn't find a link. It's a UK Data Service record, so search there for the number. It tells us which income, tax and NI variables exist (D6).

## Lower priority, if you want completeness

- **UK saving by wealth group:** nothing found. The candidates I located but didn't open are the [IFS R71](https://ifs.org.uk/sites/default/files/output_url_files/r71.pdf) and the [Wealth Tax Commission EP1](https://www.wealthandpolicy.com/wp/EP1_Distribution.pdf).
- **HMRC Corporate Taxes vs OECD 1200 reconciliation:** the HMRC Corporation Tax statistics page named above, plus the OECD definition of code 1200.

Send items 1–3 first, and tell me which others you can get.