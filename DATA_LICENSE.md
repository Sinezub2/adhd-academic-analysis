# Data licenses and attribution

## South African workbook

The files `Student Mental Health Article Data.xlsx` and `adhd_statistical_analysis/data/raw/Student Mental Health Article Data.xlsx` are unchanged copies of:

Rousseau, Kim; Mohamad, Nawal; Dowlut, Fatimah; Gering, Milton; Thomas, Kevin. (2024). *ADHD and Common Mental Disorders: Effect on Academic Success in SA First-Years* [Dataset, version 1]. University of Cape Town / Figshare. **https://doi.org/10.25375/uct.24906924.v1**.

- Original record: https://figshare.com/articles/dataset/24906924
- Publisher metadata: https://api.figshare.com/v2/articles/24906924
- Original file: https://ndownloader.figshare.com/files/43834113
- License: **Creative Commons Attribution 4.0 International (CC BY 4.0)**, https://creativecommons.org/licenses/by/4.0/ .
- Accessed: 20 October 2026.
- File size: 255,537 bytes.
- MD5: `bc660db1fb08d0abf743fce735073ffa`.
- SHA-256: `84373cad739c5e315fd7a94c0fc98627936d1a9291265fca0a71545f4d561c3a`.

The source authors own and provide the data. This repository's secondary analysis does not imply their endorsement. Derived numeric variables, filtering of incomplete AAS records, statistical calculations, figures, and unresolved scoring issues are documented in the [cleaning log](adhd_statistical_analysis/outputs/cleaning_log.md) and [report](adhd_statistical_analysis/outputs/ADHD_results_report.md). No clinical diagnosis is inferred from ASRS symptoms. Original workbook bytes are unchanged; prepared CSVs and figures are derived outputs, not original source data.

## Israeli published summaries and Table 3 extract

`adhd_statistical_analysis/data/israel_table3.csv` transcribes the ADHD-only and no-LD/ADHD academic/social adjustment summaries from:

Sarid, Miriam, & Lipka, Orly. (2023). *Students with learning disabilities/attention-deficit/hyperactivity disorder in higher education dealing with remote learning: lessons learned from COVID-19 era*. Frontiers in Psychology, 14, 1172771. **https://doi.org/10.3389/fpsyg.2023.1172771**.

Copyright © 2023 Sarid and Lipka. The article is distributed under the **Creative Commons Attribution license (CC BY)**. See the [publisher's copyright statement](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2023.1172771/full) and [CC BY 4.0 terms](https://creativecommons.org/licenses/by/4.0/).

The accompanying `sarid_lipka_2023_table3.html` fixture retains the published Table 3 content, removes the surrounding website wrapper, and adds an attribution paragraph. It exists to verify the summary transcription offline. The CSV selects four summary rows; it does not contain reconstructed or simulated participants. New Welch tests, CIs, Holm corrections, and effect sizes are this repository's secondary calculations, not the authors' original four-group ANOVA/Tukey statistics. Source means/SDs are rounded. Accessed 20 October 2026.

## Other publications and repository code

Other referenced publications are cited and linked in [references.bib](references.bib), [CITATION.cff](CITATION.cff), and the report. Full downloaded article-page caches remain local and are not included in this update. Access to an article does not by itself grant a redistribution license.

Third-party materials retain their own licenses and copyright notices. The dataset's CC BY license does not automatically license the original analysis code or all repository content. No blanket software license is introduced by this data-attribution document.
