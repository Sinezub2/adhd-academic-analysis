# Analysis notes

- See `../analysis_plan.md` for hypotheses, families and decisions fixed before calculating this pipeline's p-values. This is an analysis specification after source inspection, not preregistration.
- Primary population: Israeli COVID-19 remote-learning undergraduate sample, ADHD-only versus no LD/ADHD. No merging of LD groups, symptom-defined samples or countries.
- Alpha .05; all inferential tests two-sided. Holm: Israel primary (2), provisional South African Pearson (3), rank sensitivity (3), conditional ASRS regression coefficients (2). These are separate questions/families; no claim of one global family-wise error rate across all analyses. CIs remain marginal 95%.
- Hedges' g uses signed ADHD-minus-comparison difference, pooled SD and exact gamma-ratio J. Its optional CSV CI is approximate pooled-SD normal inference, while raw differences use Welch intervals.
- Published-summary medians, quartiles, IQR, outliers, Shapiro, Brown–Forsythe and Mann–Whitney: **not computable from summary statistics**. Missing N/% is also unavailable rather than assumed zero.
- Raw data: no clinical ADHD grouping. Use continuous ASRS; no threshold creates a diagnosis. Pairwise complete correlations, listwise complete regressions, no additional imputation and no deletion for outliers. No equal-variance test is required for Welch, and no independent-groups raw design supports Levene here.
- AAS coding unresolved: direct sums, required reversals in original scale appendix, no recoding history. AAS-related inferential calculations are transparent provisional score audits and are not adjudicated as validated academic hypotheses. No guessed reverse coding is applied.
- Unknown `asrs1_total.y`, `aas_change` construction and absent weighted GPA are excluded from inference. AAS regression is explicitly not a GPA regression. Broken external formulas are confined to an auxiliary source sheet and are not repaired or used.
- Seed 42, 5,000 paired bootstrap resamples, percentile CIs for rho. Pearson Fisher-z CIs and parametric mean CIs do not use random sampling. Raw figures use only observed data.
- Published context statistics are attributed to their original analyses. Baczewski's p=.02 stress outcome is not significant at its corrected .008 threshold. The full text includes an academic contrast despite broader language in its abstract.
- Short bibliographic and source-verification evidence is in `data/metadata/source_review.md`; complete cached primary-source HTML is available where downloads succeeded. The AAS author appendix was readable through web search but direct archival download returned HTTP 403.
- Unit-test results and pipeline verification are recorded separately in `validation_summary.md`. All original files remain unchanged.
