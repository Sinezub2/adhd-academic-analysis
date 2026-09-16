# ADHD and academic outcomes: presentation findings

This dataset does not contain a sufficiently clear variable for institutional academic support, so a support-vs-no-support comparison would not be valid.

The supplied main sheet contains **506 students and 110 columns**. General psychiatric medication and therapy/counselling questions do not identify academic accommodations, institutional providers, ADHD-specific care, coaching, tutoring, or mentoring. No support proxy or support comparison was created.

The available university outcome is **`psy1004_grade`**, presented conservatively as a PSY1004 course mark (%), **not GPA**. The published paper describes a different, semester-wide GPA outcome; it must not be substituted for this workbook column. These are new analyses of the supplied workbook, not a replication of every published result.

### Best Graphs for the Presentation

Ranked by usefulness for this research question, not p-value alone. These are the three recommended graphs; the remaining graphs are supporting analyses.

**1. [Inattention and academic adjustment](outputs/inattention_vs_academic_adjustment.html) — best for “Why this problem matters.”**

- Shows: students with more inattentive symptoms tend to report poorer academic adjustment.
- Exact variables: `inattention` = sum of `asrs1_item_1`–`asrs1_item_4` and `asrs1_item_7`–`asrs1_item_11`; `adjustment` = sum of `aas1_item_1`–`aas1_item_9`, requiring all nine responses. This equals `aas1_total` for complete responses. Higher AAS scores mean better adjustment.
- Result: n = 488; Pearson r = -0.205, 95% CI [-0.288, -0.118]; p = 5.12e-06, Holm-adjusted p = 5.12e-05. Each 5-point increase in inattention corresponds to -0.74 adjustment points (95% HC3 CI [-1.07, -0.40]). Shared variance is 4.2%.
- Relevance / legitimate claim: identifies a modest academic-adjustment difficulty associated with inattention, a possible target for support research.
- Cannot claim: that inattention caused the difficulty, that ADHD was clinically diagnosed, that support would improve outcomes, or that this establishes a support gap in Kazakhstan. Both measures are concurrent self-reports.

Suggested slide sentence: **“In this South African first-year sample, greater inattention was associated with poorer academic adjustment (r = -0.20, n = 488).”**

**2. [Inattention and course marks](outputs/inattention_vs_academic_performance.html).**

- Shows: a small downward association with an academic mark, alongside substantial individual variation.
- Exact variables: the same nine-item `inattention` sum and `psy1004_grade` (analysis alias `course_mark`).
- Result: n = 506; Pearson r = -0.107, 95% CI [-0.193, -0.020]; p = 0.016, Holm-adjusted p = 0.080. A 5-point higher inattention score corresponds to -0.90 percentage points (95% HC3 CI [-1.65, -0.14]); shared variance = 1.1%. The association does not pass the primary-family Holm threshold.
- Relevance / legitimate claim: a small unadjusted academic-performance association supports investigating needs, while keeping its size visible. The coefficient is weaker after age and prior attainment are included (graph 3).
- Cannot claim: a strong or causal grade penalty, an independent association established after covariate adjustment, a GPA effect, or a benefit of accommodations.

**3. [Symptom dimensions and prior attainment](outputs/symptom_dimensions_vs_academic_performance.html).**

- Shows: the two symptom dimensions in the same regression, before and after adding age and earlier academic attainment.
- Exact variables: `psy1004_grade`; `inattention` as above; `hyperactivity` = sum of `asrs1_item_5`, `asrs1_item_6`, and `asrs1_item_12`–`asrs1_item_18`; covariates `age`, `matric_mark`, `nbt_alql_ave`. Symptom predictors are standardized; outcome remains percentage points.
- Result: n = 506. Joint model: inattention B = -2.16 (95% CI [-3.42, -0.91], p = 7.60e-04); hyperactivity B = 1.68 ([0.53, 2.84], p = 0.004), R² = 0.027. With covariates: inattention B = -0.93 ([-2.02, 0.16], p = 0.093); hyperactivity B = 0.42 ([-0.61, 1.45], p = 0.422), R² = 0.294. All intervals are HC3; covariate-model p-values are exploratory and nominal.
- Relevance / legitimate claim: inattention is the negatively associated dimension in the simple joint model, but prior attainment changes the interpretation. The overall ADHD total can conceal different conditional associations.
- Cannot claim: hyperactivity improves grades, a causal executive-function mechanism, or an independent inattention effect established by the covariate model. Conditional positive coefficients can reflect correlated predictors/suppression. The larger R² is for the entire model, not ADHD alone.

### Other planned results, including null findings

- Overall ADHD severity versus marks: n = 506; Pearson r = -0.041, 95% CI [-0.127, 0.047]; p = 0.360, Holm-adjusted p = 1.000. There is no clear linear association; this is not proof of no relationship.
- Screening comparison: ASRS six-item sum ≥14 defines **screen positive**, not diagnosed ADHD. Screen negative is not confirmed absence of ADHD.

| group | n | mean | median | sd | mean_ci_low | mean_ci_high |
| --- | --- | --- | --- | --- | --- | --- |
| Screen negative | 255 | 61.580 | 62.000 | 11.619 | 60.147 | 63.013 |
| Screen positive | 251 | 59.442 | 60.000 | 10.674 | 58.115 | 60.769 |

Positive-minus-negative mean difference = -2.14 percentage points, 95% CI [-4.09, -0.19]; Welch t(501.6) = -2.16, p = 0.032, Holm p = 0.126; Cohen’s d = -0.192, Hedges’ g = -0.191, bootstrap 95% CI [-0.367, -0.014]. Mann–Whitney sensitivity p = 0.042. This small contrast does not pass the primary-family Holm threshold. No diagnostic prevalence estimate is inferred.

- Imported adjustment-change index: n = 176; Pearson r = -0.328, 95% CI [-0.454, -0.189]; p = 9.02e-06, Holm-adjusted p = 1.80e-05. This is exploratory: only 176/506 have a value, wave-2/3 scores and the derivation code are absent, and model units are not raw AAS-point changes. Students with a change value have higher average course marks (62.72% versus 59.35%), so subset selection matters. The paper’s reported adjustment sample (180) differs from the workbook’s available 176.
- Targeted symptom overlap: inattention–depression r = 0.491; inattention–anxiety r = 0.448, both n = 506 and secondary Holm p < .001. These are symptom correlations, not confirmed comorbid diagnoses. They motivate studying coordinated academic and mental-health support, without establishing intervention effectiveness.
- No GPA, degree-completion, dropout, or confirmed course pass/fail variable is supplied. A mark threshold was not invented. No exploratory demographic fishing was performed.

### Interpretation for Kazakhstan

This sample can motivate a **question about support needs**. It cannot establish the availability of ADHD-specific infrastructure in Kazakhstan or estimate the benefit of support there. Those claims require local institutional evidence and a dataset measuring clearly defined support exposure and academic outcomes.

### Methods and reproducibility

Analyses use one row per student in `Sheet1`. The headerless `Outliers` sheet has ten records with missing course marks and broken references; it is documented but not appended. No new outlier trimming or imputation is used in the primary analyses. Scale sums require complete items. There is no participant identifier to independently validate longitudinal linkage.

Pearson correlations have Fisher-z 95% CIs; Spearman correlations check robustness to ranks. OLS uses HC3 robust standard errors and t-based intervals; scatter bands are confidence intervals for the mean, not individual prediction intervals. Welch’s test estimates the difference in group means without assuming equal variances. Large groups and mild skew support it; Mann–Whitney is a sensitivity test of distributions, not automatically a median test. Cohen’s d uses pooled within-group SD; Hedges’ g corrects small-sample bias; its interval uses 5,000 within-group bootstrap samples (seed 20260916).

Holm correction is applied to ten primary tests: six symptom–academic correlations, one screening Welch test, two joint-model symptom coefficients, and their standardized contrast. Four secondary correlations form a separate Holm family. CI coverage is pointwise, not simultaneous. Spearman, covariate models, and other sensitivity p-values are nominal and exploratory. Selection into the available cohort and shared self-report measurement remain limitations.

Primary model: `course_mark ~ inattention + hyperactivity`. Covariate sensitivity: add `age + matric_mark + nbt_alql`. NBT academic/quantitative-literacy average is used consistently, avoiding interpretation of math zeroes for students who did not take that test. Both symptom dimensions have the same 0–36 raw range; the comparison graph scales each by its sample SD. Direct coefficient contrast and VIFs are saved in tables. The two-sided standardized contrast is -3.85 percentage points, 95% CI [-6.00, -1.69], p = 4.84e-04, Holm p = 0.004; this is a signed conditional contrast, not a causal ranking.

### Sources

- Dataset: Rousseau, Mohamad, Dowlut, Gering & Thomas, [UCT/Zivahub, CC BY 4.0](https://doi.org/10.25375/uct.24906924); supplied locally through the [Kaggle mirror](https://www.kaggle.com/datasets/imtkaggleteam/adhd-mental-health).
- Variable interpretation: Mohamad et al. (2025), [original study methods and limitations](https://doi.org/10.1177/10870547241310659). Used for instrument meanings, item groupings, and study context; published results were not substituted for calculations.
- Screening rule: Harvard/NCS, [ASRS v1.1 six-question scoring update, February 2024](https://www.hcp.med.harvard.edu/ncs/ftpdir/adhd/ASRS_v1.1_screener%286Q%29_scoring_update.pdf). Six-item sum 0–24, positive at ≥14; screening is not diagnosis. ASRS attribution: © New York University and the President and Fellows of Harvard College. Item wording is not reproduced.

See `DATA_AUDIT.md`, the executed notebook, and `tables/` for every estimate, missingness count, data-quality decision, and sensitivity result.
