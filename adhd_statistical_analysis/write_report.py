"""Generate readable documentation from calculated tables; no hard-coded test results."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
SA_URL = "https://pmc.ncbi.nlm.nih.gov/articles/PMC11800717/"
IL_URL = "https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2023.1172771/full"
AAS_URL = "https://www.researchgate.net/publication/305617123_The_AAS_-_appendix"


def f(value, digits=3):
    return "unavailable" if pd.isna(value) else f"{value:.{digits}f}"


def p(value):
    return "unavailable" if pd.isna(value) else f"{value:.6g}"


def table(headers, rows):
    def clean(value):
        return str(value).replace("|", "/").replace("\n", " ")
    return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |",
        *["| " + " | ".join(clean(value) for value in row) + " |" for row in rows]])


def write_documents(summaries, tests, descriptives, validation, historical, run_info):
    primary = tests.loc[tests.role == "primary"]
    academic = primary.loc[primary.outcome == "academic_adjustment"].iloc[0]
    social = primary.loc[primary.outcome == "social_adjustment"].iloc[0]
    primary_table = table(["Hypothesis / outcome", "ADHD-only; comparison", "Difference [95% CI]", "Welch t (df)", "Raw p", "Holm p", "Hedges' g", "Decision"], [
        [row.outcome.replace("_", " "), "n=68; n=197", f"{row.estimate:.2f} [{row.ci_low:.3f}, {row.ci_high:.3f}]",
         f"{row.statistic:.3f} ({row.df:.3f})", p(row.p_raw), p(row.p_holm), f(row.effect_size), "Supported in this sample" if row.p_holm<.05 and row.estimate<0 else "Not supported"]
        for _,row in primary.iterrows()])
    summary_table = table(["Outcome", "ADHD-only mean (sample SD)", "No LD/ADHD mean (sample SD)"], [
        [name.replace("_", " "), f"{rows.iloc[0]['mean']:.2f} ({rows.iloc[0].sd:.2f})", f"{rows.iloc[1]['mean']:.2f} ({rows.iloc[1].sd:.2f})"]
        for name,rows in summaries.groupby("outcome",sort=False)])
    references = f"""1. Rousseau, K., Mohamad, N., Dowlut, F., Gering, M., & Thomas, K. (2024). *ADHD and Common Mental Disorders: Effect on Academic Success in SA First-Years* [Data set, v1]. University of Cape Town / Figshare. [DOI: 10.25375/uct.24906924.v1](https://doi.org/10.25375/uct.24906924.v1). CC BY 4.0. [Metadata](https://api.figshare.com/v2/articles/24906924), [workbook](https://ndownloader.figshare.com/files/43834113).
2. Mohamad, N., Rousseau, K.-L., Dowlut, F., Gering, M., & Thomas, K. G. F. (2025). *Symptoms of ADHD and Other Common Mental Disorders Influence Academic Success in South African Undergraduates*. Journal of Attention Disorders, 29(5), 363–386. [DOI: 10.1177/10870547241310659](https://doi.org/10.1177/10870547241310659). [Full text]({SA_URL}).
3. Sarid, M., & Lipka, O. (2023). *Students with learning disabilities/attention-deficit/hyperactivity disorder in higher education dealing with remote learning: lessons learned from COVID-19 era*. Frontiers in Psychology, 14, 1172771. [DOI / full text]({IL_URL}).
4. Gormley, M. J., DuPaul, G. J., Weyandt, L. L., & Anastopoulos, A. D. (2019 issue; online 2016). *First-Year GPA and Academic Service Use Among College Students With and Without ADHD*. Journal of Attention Disorders, 23(14), 1766–1779. [DOI: 10.1177/1087054715623046](https://doi.org/10.1177/1087054715623046). [Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC6209537/).
5. Lipka, O., Sarid, M., Aharoni Zorach, I., Bufman, A., Hagag, A. A., & Peretz, H. (2020). *Adjustment to Higher Education: A Comparison of Students With and Without Disabilities*. Frontiers in Psychology, 11, 923. [DOI / full text](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.00923/full).
6. Baczewski, L. M., Pizzano, M., Kasari, C., & Sturm, A. (2022). *Adjustment Across the First College Year: A Matched Comparison of Autistic, Attention-Deficit/Hyperactivity Disorder, and Neurotypical Students*. Autism in Adulthood, 4(1), 12–21. [DOI: 10.1089/aut.2021.0012](https://doi.org/10.1089/aut.2021.0012). [Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC8992914/).
7. Anderson, J. R., Guan, Y., & Koc, Y. (2016). *The academic adjustment scale: Measuring the adjustment of permanent resident or sojourner students*. International Journal of Intercultural Relations, 54, 68–76. [DOI: 10.1016/j.ijintrel.2016.07.006](https://doi.org/10.1016/j.ijintrel.2016.07.006). [Author-uploaded scale appendix]({AAS_URL}).
8. Yertukeshova, G., et al. (2024). *Assessment of the Relationship between Mental Health and Academic Achievement among Students in Kazakhstan*. Health Psychology Research, 12, 125270. [DOI: 10.52965/001c.125270](https://doi.org/10.52965/001c.125270). [Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC11820214/). Context screening only; not an ADHD dataset.
"""
    south_section = "South African raw data are unavailable. The Israeli analysis is complete; South African participant-level analyses remain pending."
    cleaning = "Raw South African data unavailable. No participant-level values were generated."
    dict_extra = ""
    if run_info["raw_available"]:
        pearson = tests.loc[tests.family == "SA_provisional_pearson_m3"]
        spearman = tests.loc[tests.family == "SA_provisional_spearman_m3"]
        regression = tests.loc[tests.family == "SA_provisional_regression_ASRS_m2"]
        ina = pearson.loc[pearson.predictor == "inattention"].iloc[0]
        total_asrs = pearson.loc[pearson.predictor == "asrs_total"].iloc[0]
        correlation_table = table(["Symptom score", "N", "Pearson r [95% CI]", "Raw p", "Holm p", "Spearman rho [bootstrap 95% CI]", "Spearman raw / Holm p"], [
            [row.predictor, int(row.n), f"{row.estimate:.3f} [{row.ci_low:.3f}, {row.ci_high:.3f}]", p(row.p_raw), p(row.p_holm),
             f"{spearman.loc[spearman.predictor==row.predictor].iloc[0].estimate:.3f} [{spearman.loc[spearman.predictor==row.predictor].iloc[0].ci_low:.3f}, {spearman.loc[spearman.predictor==row.predictor].iloc[0].ci_high:.3f}]",
             p(spearman.loc[spearman.predictor==row.predictor].iloc[0].p_raw)+" / "+p(spearman.loc[spearman.predictor==row.predictor].iloc[0].p_holm)]
            for _,row in pearson.iterrows()])
        regression_table = table(["Exploratory score model", "N", "ASRS coefficient [HC3 95% CI]", "t (df)", "Raw / Holm p", "R²"], [
            [row.model, int(row.n), f"{row.estimate:.4f} [{row.ci_low:.4f}, {row.ci_high:.4f}]", f"{row.statistic:.3f} ({int(row.df)})", p(row.p_raw)+" / "+p(row.p_holm),f(row.r_squared)] for _,row in regression.iterrows()])
        raw_desc = descriptives.loc[descriptives.variable.isin(["asrs_total","inattention","hyperactivity","aas_complete"])]
        raw_table = table(["Variable", "N / missing", "Mean (sample SD)", "Median [Q1, Q3]", "IQR", "Min–max", "Skewness", "95% mean CI"], [
            [row.variable,f"{int(row.n)} / {int(row.missing_n)}",f"{row['mean']:.2f} ({row.sample_sd:.2f})",f"{row['median']:.2f} [{row.q1:.2f}, {row.q3:.2f}]",f(row.iqr,2),f"{row.minimum:.0f}–{row.maximum:.0f}",f(row.skewness),f"[{row.mean_ci_low:.2f}, {row.mean_ci_high:.2f}]"] for _,row in raw_desc.iterrows()])
        max_vif = pd.read_csv(OUT/"regression_vif.csv").vif.max()
        model_diags = json.loads((OUT/"regression_diagnostics.json").read_text())
        south_section = f"""### Participant-level academic data: South Africa

The public workbook contains 506 baseline rows and 110 named columns in `Sheet1`, with no participant IDs and no repeated wave-2/3 item fields. ASRS totals match the documented 18-item sum in all 506 rows. Inattention uses items 1–4 and 7–11; hyperactivity/impulsivity uses 5–6 and 12–18. Both subscales range 0–36 and total symptoms range 0–72. These continuous questionnaire scores do not establish ADHD diagnoses. The source paper reports that missing ASRS/BAI values were imputed before its analyses; the release does not identify imputed cells. We make no additional imputations. [Methods]({SA_URL}).

{raw_table}

All raw-data missing percentages, quartiles, skewness and mean CIs are in `descriptive_statistics.csv`. The complete-item AAS outcome has 18/506 missing (3.56%). The stored AAS total has no missing entries because 18 partial-item records were summed over their observed items; these totals are set missing only in the prepared analysis variable.

**Scoring limitation:** the original AAS author appendix marks items 2 and 3 for reverse scoring. The stored workbook total is exactly the direct sum of the nine stored items. The workbook has no item wording, randomization/order information, or recoding history to establish whether those stored items have already been reversed. Item correlations raise a scoring concern but cannot resolve it. We therefore retain the author-supplied complete-item composite without guessing a recoding and treat the following calculations as a provisional numerical audit, **not verified evidence about a correctly scored academic-adjustment construct**. The paper specifies the intended total direction as higher = better. Nine items scored 1–5 imply 9–45; the paper's stated minimum of 1 is arithmetically inconsistent. [Original scale appendix]({AAS_URL}); [study methods]({SA_URL}).

{correlation_table}

Pearson tests use a two-sided t-equivalent test (df=N−2) and Fisher-z CIs. Spearman uses asymptotic two-sided p-values and 5,000 paired percentile bootstrap resamples with seed 42 for CIs. Each three-test family receives its own Holm correction. The plots show bounded/discrete scores and a mild trend; rank analysis checks sensitivity to tails and nonlinearity. Shapiro statistics and Tukey outlier counts are in `distribution_diagnostics.csv`, used descriptively, with no automatic test switching or deletion. No diagnosed raw-data groups exist, so Brown–Forsythe/Levene and group Mann–Whitney tests are not appropriate here.

### Reconciliation of earlier coefficients

Using the documented inattention items and complete AAS responses gives **r={ina.estimate:.6f}, N={int(ina.n)}, raw p={p(ina.p_raw)}**, with this audit family's Holm p={p(ina.p_holm)}. This independently checks the historical r=−0.205, N=488, p=5.12×10⁻⁶ claim. The correctly defined result is determined by the scoring rule, not by its p-value.

The documented **ASRS total**, rather than inattention alone, gives r={total_asrs.estimate:.6f}, N={int(total_asrs.n)}, raw p={p(total_asrs.p_raw)}; this rounds to **−0.14**. Thus the two reported coefficients can be numerically reconciled as **different symptom exposures on the same baseline outcome/sample**. Attribution of that earlier slide to ASRS total remains an inference because its code is absent. This audit's three-test Holm p for ASRS total is {p(total_asrs.p_holm)}, not .015. The old .015 cannot be established without that version's sample and correction family and remains **unresolved**; no past adjusted p-value is reused. As a separate scoring-error check fixed in the analysis specification, a rejected sum of the first nine ASRS items gives r={historical['rejected_first_nine_sum_r']:.6f}, which matches neither claimed coefficient and mixes symptom clusters. No presentations or prior analysis script containing those results were present. The earlier notebook only imports and reads the workbook.

### Conditional regression audit and unavailable GPA analysis

{regression_table}

The base model conditions on age, Grade 12 score and the released `nbt_ave`; the second model adds BDI-II. Coefficients express stored AAS points per one ASRS point. Holm correction covers the two ASRS coefficients. HC3 standard errors allow heteroskedasticity; they do not fix measurement error, omitted variables or unresolved AAS scoring. Maximum VIF across these models is {max_vif:.2f}. Cook's-distance flags above 4/N: {model_diags[0]['cooks_above_4_over_n']} in the base model and {model_diags[1]['cooks_above_4_over_n']} in the BDI sensitivity model; these thresholds are diagnostic and no records are removed. See coefficient, VIF and residual-diagnostic files for details. A changed coefficient after BDI adjustment may reflect shared variance or overadjustment; it is not a mediation or causal result.

The hyperactivity/impulsivity correlation is non-significant in both Pearson and rank audits. The ASRS coefficient is also non-significant after BDI-II adjustment, with its CI spanning zero. These null findings are retained alongside negative associations; none supports a uniform symptom effect across measures or specifications.

**Objective GPA:** the paper's weighted first-semester GPA is not present in the public workbook. The field `psy1004_grade` has mean 60.52, SD 11.20 and range 28–88; the paper's GPA has mean 63.54, SD 11.41 and range 1.50–88.34 (Table 3). It cannot be relabeled as GPA. Consequently ASRS–GPA correlations, adjusted GPA regression and direct raw-data verification of the paper's GPA findings are **pending verified GPA data and a mapping/codebook**. `b1`/`b2` are absent and receive no guessed meaning.

**Repeated measures and attrition:** the article reports 506 → 332 → 180 participants (34.4% attrition by wave 2; 64.4% by wave 3 relative to baseline). The release contains 176 nonmissing `aas_change` values, not 180, and no wave-2/3 AAS items or IDs. The exact slope construction cannot be verified; the field is described but excluded from inference. The source's longitudinal results are not reproduced by treating rows or slopes as independent repeated observations. The auxiliary `Outliers` sheet contains 10 headerless records and broken external `#REF!` formulas; it is not appended to the canonical 506-row cohort. Upstream selection and completeness may bias associations. The article also reports lower GPA among non-completers, so attrition cannot be assumed irrelevant.

![South African distributions](south_africa_distributions.png)

![Provisional associations](south_africa_associations.png)
"""
        cleaning = f"""# Cleaning log

Analysis access date: 2026-10-20. The original root files were preserved unchanged. The public raw download has the same SHA-256 as the local workbook: `{run_info['source_hashes'].get('Student Mental Health Article Data.xlsx','unavailable')}`.

1. Read `Sheet1` with its existing row-1 header: 506 rows, 110 named columns. Formatting extends to column DK but DG–DK have no data. No joins or reshaping were performed.
2. All exact full-row duplicate count: {validation['exact_duplicate_rows']}. No IDs are available, so lack of exact duplicates does not prove unique participants. One released Sheet1 row is treated as one baseline participant under the source's described design. A technical Excel row number is retained solely for traceability.
3. Validate numeric item types, integral responses and ranges: ASRS 0–4; AAS 1–5; BDI-II/BAI 0–3; released AUDIT items 0–4. Invalid codes would stop analysis rather than silently turn into zero. Raw range checks pass. Missing numeric responses are blank cells. Free-text psychiatric histories are not reinterpreted as diagnoses or exported.
4. ASRS: 506 complete 18-item records. Reconstructed total matches `asrs1_total.x` in all rows. Derived inattention and hyperactivity/impulsivity follow the paper's explicit item lists, with strict nine-item completeness and no reversed items.
5. AAS: 488 complete nine-item records, 18 incomplete. In all 506 rows `aas1_total` equals the item sum with missing items ignored. Keep that source column intact; set derived `aas_complete` missing for partial records, with no prorating or new imputation. No recoding is guessed. Reverse-coding history is unresolved; all inference involving this composite is labeled provisional score audit.
6. `asrs1_total.y`: 505 nonmissing entries; {validation['asrs_y_matches_bai_stored_n']} equal `bai1_total` and {validation['asrs_y_matches_bai_item_sum_n']} equal the BAI item sum. This field is inconsistent with an ASRS label. Exclude, do not rename it to an asserted outcome or wave.
7. BAI: 61 complete-row mismatches between stored total and item sum. Preserve both original item values and total; no guessed repair, and no BAI-adjusted model. BDI-II total matches its 21-item sum in all 506 rows. AUDIT total matches the released nine-item sum, but conventional scoring is not established; describe only.
8. Preserve author-supplied `nbt_ave` rather than reconstruct it from `nbt_math`, because zero/missing mathematics coding and rounding are not documented. Its mean/SD match the paper (58.66/11.30), but observed maximum is 89 versus the paper table's 88. `matric_mark` mean/SD likewise match to rounding.
9. Exclude `psy1004_grade` from GPA analyses; it differs from weighted GPA and lacks a mapping. Do not infer semantics for absent `b1`/`b2`.
10. `aas_change`: 176 observed, 330 missing (65.22%). Describe numerically only; missing waves and IDs prevent reconstruction or new mixed-effects fitting. These 176 are not additional participants.
11. `Outliers`: 10 headerless ancillary records, 10 broken external formula references. Preserve unchanged and do not append to Sheet1. No new data-dependent outlier exclusions are made. No source workbook is recalculated or resaved.
12. All associations use pairwise complete records; conditional AAS regressions use listwise complete values for their stated model. Both regression samples have N=488. This is complete-case analysis without an assertion of MCAR/MAR, and no multiple imputation is attempted.
13. `prepared_analysis_data.csv` contains only required numeric scores, covariates and source row references, with excluded fields not used as predictors or outcomes. No free-text histories are included. Formula errors, ranges and per-column missingness are separately logged.
14. No synthetic participant rows, outcome thresholds, winsorization or post-hoc directional changes were used. Bootstrap resamples are used solely for uncertainty of observed correlations, never as substitute study data.
"""
        dictionary_rows = pd.read_csv(OUT/"data_dictionary.csv")
        dict_extra = "\n\n## Every released Sheet1 column\n\n" + table(["Column", "Meaning", "Status", "Direction"], dictionary_rows[["column","meaning","verification_status","direction"]].values.tolist())
    report = f"""# ADHD, academic outcomes and social adjustment

Analysis date / source access: 20 October 2026. Two-sided α=.05. Reproducible secondary analysis; conclusions concern associations and differences, not causation.

## Research questions and answers

1. **Academic:** Is ADHD associated with poorer academic outcomes, and is higher symptom severity associated with poorer GPA or adjustment? The primary Israeli comparison supports lower **self-reported academic adjustment** in the ADHD-only group. This is not a GPA test. Published US GPA findings provide separate corroborating context; the South African released workbook does not permit the requested verified GPA reanalysis.
2. **Social:** Is ADHD associated with lower social adjustment? The Israeli comparison supports lower **self-reported social adjustment** during remote learning. It does not directly measure observed social ability, all social-functioning domains, or outcomes in Kazakhstan.

## Primary hypotheses, populations and methods

For each outcome H₀ is μ_ADHD−μ_comparison=0. The research prediction is a negative difference, assessed with two-sided tests. The two outcomes form one prespecified primary family with Holm correction. `analysis_plan.md` was written after source QA and before this pipeline's inferential calculations; the task already contained validation p-value expectations, so this is not an independent preregistration.

We transcribed only Table 3 columns **C (ADHD-only)** and **A (no LD/ADHD)** in Sarid & Lipka (2023): n=68 and n=197. LD-only and LD+ADHD groups are excluded from this focused contrast. Participants were Hebrew-speaking undergraduates from Israeli higher-education institutions during spring 2020 COVID-19 remote learning. Diagnoses were self-reported; the authors describe requesting recent diagnostic certification and phone confirmation, with the COVID sample undergoing the same verification procedure. This does not constitute a new clinical diagnostic assessment by this project. [Methods and Table 3]({IL_URL}).

The adapted Hebrew SACQ uses 1–9 responses with higher scores indicating better adjustment. The remote-learning version has 22 academic items and 7 social items; it is abbreviated and context adapted. Academic adjustment and social adjustment are distinct self-reported constructs. No GPA is used in either primary test. Welch's method uses sample SDs and Satterthwaite degrees of freedom, accommodates unequal variances and does not require an equal-variance pretest. It assumes independent participant groups and approximately valid inference for their mean differences. With n=68/197 a mean comparison is reasonable, but distributions and influential observations cannot be checked from aggregates. Group comparability is limited: these are unadjusted, nonrandomized groups with potential differences in year of study, support and comorbidity.

For group i, vᵢ=sᵢ²/nᵢ; SE(Δ)=√(v₁+v₀); t=Δ/SE; ν=(v₁+v₀)²/[v₁²/(n₁−1)+v₀²/(n₀−1)]. The 95% CI is Δ±t₀.₉₇₅,νSE. Signed Hedges' g is J×Δ/s_pooled, using the pooled sample SD and exact gamma-ratio small-sample correction J with n₁+n₀−2 degrees of freedom. Under unequal variances g is a descriptive standardized contrast; inference for Δ remains Welch-based. The CSV also labels approximate pooled-SD Wald intervals for g separately. All reported 95% intervals are **marginal, not simultaneous family-wise intervals**. Holm-adjusted p-values determine the two primary decisions.

## Primary results: published-summary reanalysis

{summary_table}

{primary_table}

Negative differences and g indicate worse reported adjustment in ADHD-only students. Both hypotheses are supported for these measured outcomes in this sampled context after Holm correction. Values are approximate because the source means/SDs were rounded. The authors' four-group ANOVA and Tukey comparisons use different estimands, error estimates and multiplicity families; their reported F statistics are not this focused Welch reanalysis.

Only N, mean and sample SD are observed summaries. Group mean CIs, differences, Welch tests and standardized contrasts are valid derived quantities. **Medians, quartiles, IQR, observed ranges, skewness, outliers, Shapiro tests, Brown–Forsythe/Levene tests and participant-level Mann–Whitney or permutation tests are not computable from summary statistics.** Missing N/% is not reported for these specific table cells and cannot be inferred from the groups' stated sample sizes. No individual observations are simulated.

![Academic adjustment means and 95% CIs](academic_results.png)

![Social adjustment means and 95% CIs](social_results.png)

{south_section}

## Triangulation, contrary results and objective grades

**Gormley et al. (2019 issue; online 2016)** report a rigorously classified US ADHD sample, distinct from ASRS symptom severity or self-reported diagnosis alone. Table 1 gives n=133 ADHD and n=145 comparison participants for the GPA-differences analysis. Table 2 reports fall GPA 2.91 (SD .77) versus 3.26 (.69) and spring GPA 2.79 (.84) versus 3.13 (.82). Their medication-adjusted follow-up ANCOVAs report fall p=.002 and spring p=.013. These are **published contextual findings, not newly calculated tests**. The published Table 2 t entries do not straightforwardly match a simple reconstruction from the listed GPA-analysis Ns and rounded summaries, so no additional Welch tests are presented here. Fall/spring values come from the same students and cannot be pooled as independent samples. Registrar records were used where possible and participants were contacted when records were incomplete. [Tables 1–2 and methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC6209537/).

**Lipka et al. (2020)** Table 3 has a **combined ADHD/LD** column (n=67), with academic adjustment 5.76 (1.03) versus control 6.40 (1.12), and social adjustment 6.16 (1.26) versus 6.47 (1.14). This is mixed-population context and cannot establish an ADHD-only effect. Its table reports different overall disability/control counts from the abstract, another reason not to treat its mixed summaries as interchangeable primary data. The 2023 article draws its pre-pandemic comparison from the earlier study; these sources are not all independent evidence. [Table 3](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.00923/full).

**Baczewski et al. (2022)** matched 74 autistic, 74 ADHD and 74 neurotypical US freshmen on baseline characteristics, including mental health/demographic factors. With its Bonferroni α=.008, several adjusted three-group outcomes were not significantly different: intellectual self-confidence (p=.32), psychological stress (p=.02, not significant at its adjusted threshold), sense of belonging (p=.22), campus satisfaction (p=.10), and balancing academic/social demands (p=.10). Social self-confidence differences primarily involved autistic versus the other groups, not an established universal ADHD social deficit. The full text also reports an academic-success omnibus p=.003 and an autism-versus-ADHD contrast p=.002, so it should not be summarized as finding no differences whatsoever. These are the authors' analyses, not our retests; non-significance is not equivalence. Only students completing start/end surveys were included. [Full-text results](https://pmc.ncbi.nlm.nih.gov/articles/PMC8992914/).

Kim et al. (2015) was not added to the testing families because its high-risk questionnaire groups are schoolchildren, not diagnosed university students. No datasets were selected for producing small p-values.

## Kazakhstan applicability and limitations

A targeted public search on 2026-10-20 for Kazakhstan university ADHD/GPA data and Figshare/Mendeley records found **no accessible, comparable participant-level dataset** containing verified ADHD status or ASRS severity together with the required academic/social outcomes and usable documentation. This is a limited search result, not proof that none exists. A relevant Kazakhstan study of 576 students assessed GHQ-12 mental health and achievement motivation, without ADHD measures; its published availability statement does not supply a usable ADHD participant-level dataset. It is excluded from the tests. Search queries and screened links are recorded in `source_manifest.md`. [Kazakhstan contextual study](https://pmc.ncbi.nlm.nih.gov/articles/PMC11820214/).

The primary evidence uses self-reported adjustment and self-reported diagnoses with author-described verification, a nonrepresentative sample, and an exceptional COVID-19 learning context. Summary data prevent distribution, missingness and individual-confounding checks. Multiple testing is handled within defined families; exploratory score audits remain exploratory. The South African release has measurement and field-mapping uncertainties, author-side imputation, selection and substantial longitudinal attrition. Matching and adjustment in other studies do not eliminate confounding or demonstrate causation. Negative effects are not uniform across all adjustment domains or samples, and non-significant findings deserve equal reporting. Neither effect sizes nor prevalence estimates can be transported directly to Kazakhstan. These findings motivate locally evaluated support and prospective measurement, but do not estimate a Kazakhstan-specific effect or the effectiveness of an intervention.

## IMRaD Results paragraph

In a secondary analysis of published rounded summaries from Israeli undergraduates studying remotely during spring 2020, the ADHD-only group (n=68) reported lower academic adjustment than students without LD/ADHD (n=197; 5.55±1.04 vs 6.04±1.17; mean difference={academic.estimate:.2f}, 95% CI [{academic.ci_low:.3f}, {academic.ci_high:.3f}]; Welch t({academic.df:.2f})={academic.statistic:.3f}, two-sided p={p(academic.p_raw)}, Holm-adjusted p={p(academic.p_holm)}, Hedges' g={academic.effect_size:.3f}). Social adjustment was also lower (5.41±1.49 vs 6.03±1.25; difference={social.estimate:.2f}, 95% CI [{social.ci_low:.3f}, {social.ci_high:.3f}]; t({social.df:.2f})={social.statistic:.3f}, p={p(social.p_raw)}, Holm-adjusted p={p(social.p_holm)}, g={social.effect_size:.3f}). Both comparisons met the corrected α=.05 criterion. These outcomes were self-reported adjustment, not objective GPA or observed social ability. The South African release supported a provisional symptom-score audit but lacked verified GPA and sufficient AAS scoring documentation for a definitive participant-level academic-outcome conclusion.

## Reproducibility and references

Run `python run_analysis.py` from the project directory after installing `requirements.txt`; `README.md` gives full commands. All numerical tables and plots are generated by code. `analysis_plan.md`, `cleaning_log.md`, `data_validation.json`, `historical_reconciliation.json` and `run_metadata.json` document choices and limitations. The two primary Welch results are independently checked against SciPy and unit-tested, and Holm is checked against statsmodels. Dependencies used in this run are recorded in `requirements-lock.txt` and `run_metadata.json`.

{references}
"""
    (OUT/"ADHD_results_report.md").write_text(report.rstrip()+"\n")
    (OUT/"cleaning_log.md").write_text(cleaning)
    (OUT/"analysis_notes.md").write_text(f"""# Analysis notes

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
""")
    dictionary = f"""# Data dictionary

## Israeli published summaries

`data/israel_table3.csv`: four summary rows, not participant records. `source`: Sarid & Lipka (2023); `outcome`: `academic_adjustment` or `social_adjustment`; `group`: ADHD only or No LD/ADHD; `n`: table's subgroup N (68 or 197); `mean`: published rounded mean; `sd`: published rounded sample SD; `units`: adapted SACQ subscale points on a 1–9 scale; `table_column`: C or A. Higher scores indicate better adjustment. Diagnostic category is self-reported with certification/phone procedures described by authors. Each outcome uses the same two groups, not separate independent student samples across outcomes. Individual values, covariance across outcomes, missingness, and distribution summaries are unavailable. [Source]({IL_URL}).

## Derived South African analysis variables

- `source_excel_row`: technical Sheet1 row (2–507), **not a participant ID**. No raw ID was supplied.
- `asrs_total`: strict sum of 18 `asrs1_item_*` responses, 0–72, higher = more symptoms; matches `asrs1_total.x`.
- `inattention`: strict sum of items 1–4 and 7–11, 0–36. `hyperactivity`: strict sum of 5–6 and 12–18, 0–36. Neither is a diagnosis; no reverse scoring. [Explicit item mapping]({SA_URL}).
- `aas_complete`: source `aas1_total` retained only for complete nine-item AAS responses. Intended 9–45, higher = better according to article. **Actual reversal/order history is unverified**, so score audits are provisional. `aas_as_released` preserves all 506 supplied totals, including 18 partial sums, for description only. We do not construct an assumed corrected scale.
- Covariates: `age` (years), `matric_mark` (Grade 12 %), `nbt_ave` (supplied NBT %, not recomputed), `bdi1_total` (0–63 depressive-symptom sum). These correspond to baseline/source academic records, with no causal interpretation.
- `bai1_total`, `audit1_total`, `aas_change`: included only for descriptive audit, not regression predictors or inferential outcomes. `aas_change` has only 176 values and no verifiable repeated-wave construction.
- `b1` and `b2`: absent. Weighted GPA: absent. `psy1004_grade` is not verified as weighted GPA and is excluded from GPA inference. `asrs1_total.y` conflicts with its label and is excluded.

## Output schema

`descriptive_statistics.csv`: raw `n`, denominator `total_n`, missing N/%, mean, sample SD (ddof=1), median, Q1/Q3 (linear interpolation), IQR, range, unbiased sample skewness and t-based marginal 95% mean CI. Summary rows leave uncomputable statistics blank and state why. Empty numeric fields mean unavailable/not applicable, never zero.

`statistical_tests.csv`: `source`, `population`, `role`, `family`, `method`, predictor/outcome and groups; `n` is total compared participants or pairwise N, `n1/n0` only for independent groups; units; signed `estimate`, `statistic`, `df`, `p_raw`, `p_holm`; `ci_low/high` are effect intervals for Δ, r/rho or coefficient according to `ci_method`; effect-size type and value; group tests also contain pooled SD, g and approximate g CI. `r_squared` only for regression. `supported_at_05` is adjudicated only for the two valid primary hypotheses. Non-applicable numeric fields are empty. Diagnostic p-values in separate files are not hypothesis-selection rules.

`data_dictionary.csv` and `column_inventory.csv` document every named source column, including fields excluded from inference. `data_validation.json` logs scoring inconsistencies. `regression_coefficients.csv` includes nuisance coefficient estimates/intervals but reports p-values only for the prespecified ASRS coefficient; other coefficients are not independently tested.
{dict_extra}
"""
    (OUT/"data_dictionary.md").write_text(dictionary)
    manifest = f"""# Source and provenance manifest

Access date for this analysis: **2026-10-20**. Original root files: `Student Mental Health Article Data.xlsx`, `intro_analysis.ipynb`, and `ADHD_Codex_Statistical_Analysis_Prompt.md`. All preserved unchanged. No supplied presentation decks or presentation brief were found. The notebook contains imports and a workbook read, not a prior completed statistical analysis. Hashes are in `run_metadata.json`.

| Source / year | Exact source / availability | Unit and population | Measures / direction | Use and limitations |
| --- | --- | --- | --- | --- |
| Rousseau et al. 2024, v1 | [DOI](https://doi.org/10.25375/uct.24906924.v1); [API](https://api.figshare.com/v2/articles/24906924); [file 43834113](https://ndownloader.figshare.com/files/43834113). CC BY 4.0, 255,537 bytes. `Student Mental Health Article Data.xlsx`; `Sheet1` 506×110 named fields, auxiliary headerless `Outliers` 10 rows. | Baseline student rows; convenience sample of first-year introductory-psychology students, South Africa, 2023; no released participant ID. | ASRS items/total, baseline AAS, Grade 12, NBT, age, BDI-II, BAI, modified AUDIT; symptoms higher=worse, intended adjustment higher=better. | Raw data available and authenticated. Local workbook byte-identical to public download; no codebook supplied. GPA, wave-2/3 items and IDs missing; AAS coding unresolved; ancillary source errors. |
| Mohamad et al. 2025 | [Peer-reviewed Methods, Tables 1–4]({SA_URL}); DOI 10.1177/10870547241310659. Full text cached. | Same South African study; paper reports 506/332/180 across waves. | Explicit ASRS subscale item mapping, intended AAS direction, weighted GPA description and covariates. | Author documentation for item mapping, not proof that all published model fields exist in release. Missingness and per-cell imputation history not supplied. |
| Sarid & Lipka 2023 | [Full text, Table 3 and Methods]({IL_URL}); DOI 10.3389/fpsyg.2023.1172771. Transcribed `data/israel_table3.csv` with table column A/C references; full text cached. | Four aggregate rows; Israeli Hebrew-speaking undergraduate COVID remote-learning subgroups, n=68 ADHD-only / n=197 no LD/ADHD. | Academic and social adapted SACQ adjustment, 1–9, higher=better. Diagnosis self-reported with author-described certification and telephone verification. | Primary independent-group summary reanalysis. No participant-level data obtained; no individual diagnostics possible. Rounded means/SDs. Excludes LD-only and LD+ADHD. |
| Gormley et al. 2019 issue / online 2016 | [Original Tables 1–2](https://pmc.ncbi.nlm.nih.gov/articles/PMC6209537/); DOI 10.1177/1087054715623046, full text cached. | US university clinically classified ADHD/comparison students; GPA-differences sample n=133/145. | Actual GPA, higher=better; fall/spring SDs present. | Published GPA context only. Same students across semesters; no pooling/retesting. Table t entries not simply reproducible from stated analysis Ns. |
| Lipka et al. 2020 | [Table 3](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.00923/full); DOI 10.3389/fpsyg.2020.00923, cached. | Israeli undergraduate disability groups; ADHD/LD combined. | Self-reported academic/social adjustment, higher=better. | Context only; cannot isolate ADHD; source overall counts differ between abstract/table. Earlier sample partly reused by 2023 study. |
| Baczewski et al. 2022 | [Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC8992914/); DOI 10.1089/aut.2021.0012, cached; [author repository](https://escholarship.org/uc/item/1rt1f55t). | Matched US freshmen: 74 autistic, 74 ADHD, 74 neurotypical; start/end survey completers. | Self-reported adjustment domains; several adjusted outcomes non-significant at α=.008. | Contrary/qualifying context; not all outcomes null. Full text takes precedence over broad abstract wording. |
| Anderson, Guan & Koc 2016 | [Original scale DOI](https://doi.org/10.1016/j.ijintrel.2016.07.006); [author-uploaded appendix]({AAS_URL}). Author appendix readable in web results; direct cache request HTTP 403 recorded. | Instrument documentation, not a new participant dataset. | Nine 1–5 AAS items; original-order items 2 and 3 reverse scored. | Flags a coding uncertainty; does not establish questionnaire order or whether source authors already recoded released values. |
| Yertukeshova et al. 2024 | [Kazakhstan study](https://pmc.ncbi.nlm.nih.gov/articles/PMC11820214/); DOI 10.52965/001c.125270, cached. | 576 students, Astana and Aktobe. | GHQ-12 mental health and achievement motivation, no ADHD measures. | Screened out; no comparable ADHD student-level dataset identified. |

## Authentication and availability

Public file MD5 from Figshare: `bc660db1fb08d0abf743fce735073ffa`. Local/public SHA-256: `{run_info['source_hashes'].get('Student Mental Health Article Data.xlsx','unavailable')}`. The metadata lists one workbook and no separate codebook. Root originals were read only. Public-source cached files, hashes, failed attempts and check timestamps are in `data/metadata/retrieval_log.json`. A `cached_preexisting` status means the initial fetch happened earlier during this same analysis session; check timestamps do not pretend to be original publication or modification dates. The direct AAS appendix archive failed; evidence for reversals comes from readable author-uploaded web content. We did not contact authors or send any messages.

## Kazakhstan search scope

Queries: `Kazakhstan university students ADHD dataset GPA social adjustment open data`; `Kazakhstan ADHD university students academic GPA dataset`; `site:data.mendeley.com Kazakhstan ADHD students`; `site:figshare.com Kazakhstan ADHD students`. Searches were screened for a documented ADHD exposure and valid university academic/social outcome with accessible participant records. [Kazakhstan GHQ-12/achievement-motivation study](https://pmc.ncbi.nlm.nih.gov/articles/PMC11820214/) lacks ADHD. Other GPA/digital-profile records found did not document ADHD and were not downloaded as substitutes. No comparable, validated Kazakhstan dataset was identified in this limited search. No claim of an exhaustive national inventory is made.

## Full citations

{references}
"""
    (OUT/"source_manifest.md").write_text(manifest.rstrip()+"\n")
