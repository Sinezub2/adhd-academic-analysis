# Data audit and variable decisions

This dataset does not contain a sufficiently clear variable for institutional academic support, so a support-vs-no-support comparison would not be valid.

## What was inspected

Archive: ['ADHD.xlsx']. Main sheet: [506, 110]; headerless Outliers sheet: [10, 111]. No dictionary file, cell comments, named ranges, or hidden documentation sheets were supplied. All 110 column names, types, missingness counts and descriptive statistics are printed in `analysis_log.txt` and the notebook; complete categorical value counts are in `tables/categorical_value_counts.json`. The online study was used to resolve instrument names, not to assume unseen columns.

## Important quality issues

| scale | item_complete_n | item_incomplete_n | stored_total_mismatches_among_complete |
| --- | --- | --- | --- |
| asrs1 | 506 | 0 | 0 |
| aas1 | 488 | 18 | 0 |
| bdi1 | 506 | 0 | 0 |
| bai1 | 506 | 0 | 61 |

1. `asrs1_total.x` equals the 18-item ASRS sum in all 506 rows. `asrs1_total.y` equals that sum in only 7 rows and equals the anxiety item sum in 503 rows. The latter is excluded; its exact provenance is unresolved.
2. Eighteen `aas1_total` values have at least one missing AAS item. Main adjustment analyses require all nine items (n = 488); retaining the supplied totals is explicitly a sensitivity analysis. The arithmetic minimum of nine 1–5 items is 9, not 1.
3. Sixty-one `bai1_total` values disagree with the sum of the 21 complete BAI items. Anxiety is reconstructed from the items; supplied totals are retained only for sensitivity.
4. `aas_change` has 176 observations and 330 blanks. No later-wave item/total columns or derivation script exist in this workbook. Interpret as an imported, source-described model-derived index, not raw change, and do not reproduce the paper's n = 180 by imputation.
5. `psy1004_grade` spans 28–88 and identifies a course. It is not renamed GPA. Percentage-scale interpretation is consistent with the values and academic-mark context; a workbook-specific dictionary is absent.
6. The ten headerless Outliers rows all lack course marks and contain broken spreadsheet references. They are not a second sample or grounds to delete more main-sheet rows. No exact duplicate main rows were found.
7. Literal `not applicable`, `none`, `no`, and similar responses are preserved as categories. Only actual blanks are missing in the initial profile. In particular, `not applicable` is not recoded as untreated/no support.
8. The original study reports prior imputation; the workbook has no item-level imputation flags. Complete observed workbook items are analyzed as supplied; uncertainty from prior processing cannot be recovered.

## Variable map

| Construct | Exact source / rule | Decision |
| --- | --- | --- |
| ADHD symptoms | `asrs1_item_1`–`asrs1_item_18`; validated `asrs1_total.x` | Continuous 0–72, not diagnosis |
| Inattention | items 1–4 and 7–11 of ASRS | Sum 0–36 |
| Hyperactivity/impulsivity | items 5–6 and 12–18 of ASRS | Sum 0–36 |
| ADHD screen | first six ASRS items summed, ≥14 positive | Secondary group comparison; no clinical label |
| Diagnosis | `have_you_ever_been_diagnosed_with_a_mental_illness` and free-text `if_you_have_been_diagnosed_formally_or_informally_please_list_the_diagnosis_diagnoses` | Broad diagnosis question plus mixed formal/informal narratives cannot define confirmed ADHD vs confirmed absence |
| Course performance | `psy1004_grade` | Course mark %, not semester GPA |
| Academic adjustment | nine `aas1_item_*` responses; complete-case total | 9–45, higher = better; baseline, not final adjustment |
| Adjustment change | `aas_change` | Exploratory imported model index, unavailable derivation |
| Earlier attainment | `matric_mark`, `nbt_alql_ave` | Covariate sensitivity only; not university outcomes |
| Depression / anxiety | sums of 21 `bdi1_item_*` / `bai1_item_*` | Symptom overlap only, not diagnostic comorbidity |
| Medication | ever/current prescribed psychiatric medication questions | No indication, drug, dose, ADHD specificity or institutional provider |
| Counselling | ever/current therapy or counselling for mental illness/symptoms | General mental-health care, not academic support |
| Accommodations, disability services, coaching, tutoring, advising, mentoring | No defensible fields | No comparison |
| Help-seeking / engagement | No structured service-use or engagement measure | Do not convert narratives or AAS into exposure variables |

The complete keyword search is in `tables/variable_search.csv`. Example response labels for medication and counselling are `yes`, `no`, and `not applicable`; diagnosis labels include formal diagnosis, not formally diagnosed, and no. Provider and service purpose remain unknown.

Dataset: https://doi.org/10.25375/uct.24906924. Methods: https://doi.org/10.1177/10870547241310659. Screening: https://www.hcp.med.harvard.edu/ncs/ftpdir/adhd/ASRS_v1.1_screener%286Q%29_scoring_update.pdf.
