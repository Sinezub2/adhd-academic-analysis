# Data dictionary

## Israeli published summaries

`data/israel_table3.csv`: four summary rows, not participant records. `source`: Sarid & Lipka (2023); `outcome`: `academic_adjustment` or `social_adjustment`; `group`: ADHD only or No LD/ADHD; `n`: table's subgroup N (68 or 197); `mean`: published rounded mean; `sd`: published rounded sample SD; `units`: adapted SACQ subscale points on a 1–9 scale; `table_column`: C or A. Higher scores indicate better adjustment. Diagnostic category is self-reported with certification/phone procedures described by authors. Each outcome uses the same two groups, not separate independent student samples across outcomes. Individual values, covariance across outcomes, missingness, and distribution summaries are unavailable. [Source](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2023.1172771/full).

## Derived South African analysis variables

- `source_excel_row`: technical Sheet1 row (2–507), **not a participant ID**. No raw ID was supplied.
- `asrs_total`: strict sum of 18 `asrs1_item_*` responses, 0–72, higher = more symptoms; matches `asrs1_total.x`.
- `inattention`: strict sum of items 1–4 and 7–11, 0–36. `hyperactivity`: strict sum of 5–6 and 12–18, 0–36. Neither is a diagnosis; no reverse scoring. [Explicit item mapping](https://pmc.ncbi.nlm.nih.gov/articles/PMC11800717/).
- `aas_complete`: source `aas1_total` retained only for complete nine-item AAS responses. Intended 9–45, higher = better according to article. **Actual reversal/order history is unverified**, so score audits are provisional. `aas_as_released` preserves all 506 supplied totals, including 18 partial sums, for description only. We do not construct an assumed corrected scale.
- Covariates: `age` (years), `matric_mark` (Grade 12 %), `nbt_ave` (supplied NBT %, not recomputed), `bdi1_total` (0–63 depressive-symptom sum). These correspond to baseline/source academic records, with no causal interpretation.
- `bai1_total`, `audit1_total`, `aas_change`: included only for descriptive audit, not regression predictors or inferential outcomes. `aas_change` has only 176 values and no verifiable repeated-wave construction.
- `b1` and `b2`: absent. Weighted GPA: absent. `psy1004_grade` is not verified as weighted GPA and is excluded from GPA inference. `asrs1_total.y` conflicts with its label and is excluded.

## Output schema

`descriptive_statistics.csv`: raw `n`, denominator `total_n`, missing N/%, mean, sample SD (ddof=1), median, Q1/Q3 (linear interpolation), IQR, range, unbiased sample skewness and t-based marginal 95% mean CI. Summary rows leave uncomputable statistics blank and state why. Empty numeric fields mean unavailable/not applicable, never zero.

`statistical_tests.csv`: `source`, `population`, `role`, `family`, `method`, predictor/outcome and groups; `n` is total compared participants or pairwise N, `n1/n0` only for independent groups; units; signed `estimate`, `statistic`, `df`, `p_raw`, `p_holm`; `ci_low/high` are effect intervals for Δ, r/rho or coefficient according to `ci_method`; effect-size type and value; group tests also contain pooled SD, g and approximate g CI. `r_squared` only for regression. `supported_at_05` is adjudicated only for the two valid primary hypotheses. Non-applicable numeric fields are empty. Diagnostic p-values in separate files are not hypothesis-selection rules.

`data_dictionary.csv` and `column_inventory.csv` document every named source column, including fields excluded from inference. `data_validation.json` logs scoring inconsistencies. `regression_coefficients.csv` includes nuisance coefficient estimates/intervals but reports p-values only for the prespecified ASRS coefficient; other coefficients are not independently tested.


## Every released Sheet1 column

| Column | Meaning | Status | Direction |
| --- | --- | --- | --- |
| age | Age in years at Time 1 | mapped using article and matching descriptive statistics; use supplied NBT average | higher academic marks = better; age not an outcome |
| sex | Source header only; not used in inference | descriptive inventory only | not established |
| specify | Source header only; not used in inference | descriptive inventory only | not established |
| home_language | Source header only; not used in inference | descriptive inventory only | not established |
| have_you_ever_experienced_any_mental_health_difficulties_or_symptoms_before_starting_university_e_g_in_primary_or_high_school | Source header only; not used in inference | descriptive inventory only | not established |
| if_yes_please_list_these_difficulties_and_or_symptoms | Source header only; not used in inference | descriptive inventory only | not established |
| if_you_have_ever_experienced_difficulties_and_or_symptoms_of_a_mental_illness_how_old_were_you_when_this_started | Source header only; not used in inference | descriptive inventory only | not established |
| have_you_ever_been_diagnosed_with_a_mental_illness | Source header only; not used in inference | descriptive inventory only | not established |
| if_you_have_been_diagnosed_formally_or_informally_please_list_the_diagnosis_diagnoses | Source header only; not used in inference | descriptive inventory only | not established |
| was_this_diagnosis_made_before_or_after_you_left_high_school | Source header only; not used in inference | descriptive inventory only | not established |
| if_you_have_been_diagnosed_with_a_mental_illness_at_what_age_was_this | Source header only; not used in inference | descriptive inventory only | not established |
| have_you_ever_used_prescribed_psychiatric_medication_for_a_mental_illness_or_symptoms_of_one | Source header only; not used in inference | descriptive inventory only | not established |
| are_you_currently_using_prescribed_psychiatric_medication_for_a_mental_illness_or_symptoms_of_one | Source header only; not used in inference | descriptive inventory only | not established |
| have_you_ever_been_to_therapy_or_counselling_for_a_mental_illness_or_symptoms_of_one | Source header only; not used in inference | descriptive inventory only | not established |
| are_you_currently_in_therapy_or_counselling_for_a_mental_illness_or_symptoms_of_one | Source header only; not used in inference | descriptive inventory only | not established |
| bdi1_item_1 | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| bdi1_item_2 | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| bdi1_item_3 | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| bdi1_item_4 | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| bdi1_item_5 | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| bdi1_item_6 | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| bdi1_item_7 | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| bdi1_item_8 | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| bdi1_item_9 | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| bdi1_item_10 | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| bdi1_item_11 | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| bdi1_item_12 | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| bdi1_item_13 | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| bdi1_item_14 | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| bdi1_item_15 | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| bdi1_item_16 | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| bdi1_item_17 | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| bdi1_item_18 | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| bdi1_item_19 | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| bdi1_item_20 | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| bdi1_item_21 | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| bdi1_total | Time 1 BDI-II; items 0–3, total 0–63 | total verified against 21-item sum | higher = more depressive symptoms |
| audit1_item_1 | Released modified 9-item AUDIT | stored sum verified; conventional 10-item scoring not established; descriptive only | higher = more risky alcohol use, per article |
| audit1_item_2 | Released modified 9-item AUDIT | stored sum verified; conventional 10-item scoring not established; descriptive only | higher = more risky alcohol use, per article |
| audit1_item_3 | Released modified 9-item AUDIT | stored sum verified; conventional 10-item scoring not established; descriptive only | higher = more risky alcohol use, per article |
| audit1_item_4 | Released modified 9-item AUDIT | stored sum verified; conventional 10-item scoring not established; descriptive only | higher = more risky alcohol use, per article |
| audit1_item_5 | Released modified 9-item AUDIT | stored sum verified; conventional 10-item scoring not established; descriptive only | higher = more risky alcohol use, per article |
| audit1_item_6 | Released modified 9-item AUDIT | stored sum verified; conventional 10-item scoring not established; descriptive only | higher = more risky alcohol use, per article |
| audit1_item_7 | Released modified 9-item AUDIT | stored sum verified; conventional 10-item scoring not established; descriptive only | higher = more risky alcohol use, per article |
| audit1_item_8 | Released modified 9-item AUDIT | stored sum verified; conventional 10-item scoring not established; descriptive only | higher = more risky alcohol use, per article |
| audit1_item_9 | Released modified 9-item AUDIT | stored sum verified; conventional 10-item scoring not established; descriptive only | higher = more risky alcohol use, per article |
| audit1_total | Released modified 9-item AUDIT | stored sum verified; conventional 10-item scoring not established; descriptive only | higher = more risky alcohol use, per article |
| aas1_item_1 | Baseline AAS item, 1–5 | identity/order and prior reverse coding not independently documented | item dependent; total intended higher = better |
| aas1_item_2 | Baseline AAS item, 1–5 | identity/order and prior reverse coding not independently documented | item dependent; total intended higher = better |
| aas1_item_3 | Baseline AAS item, 1–5 | identity/order and prior reverse coding not independently documented | item dependent; total intended higher = better |
| aas1_item_4 | Baseline AAS item, 1–5 | identity/order and prior reverse coding not independently documented | item dependent; total intended higher = better |
| aas1_item_5 | Baseline AAS item, 1–5 | identity/order and prior reverse coding not independently documented | item dependent; total intended higher = better |
| aas1_item_6 | Baseline AAS item, 1–5 | identity/order and prior reverse coding not independently documented | item dependent; total intended higher = better |
| aas1_item_7 | Baseline AAS item, 1–5 | identity/order and prior reverse coding not independently documented | item dependent; total intended higher = better |
| aas1_item_8 | Baseline AAS item, 1–5 | identity/order and prior reverse coding not independently documented | item dependent; total intended higher = better |
| aas1_item_9 | Baseline AAS item, 1–5 | identity/order and prior reverse coding not independently documented | item dependent; total intended higher = better |
| aas1_total | Stored baseline AAS item sum; nine items imply range 9–45 | provisional numerical audit only; incomplete totals set missing in analysis; reverse coding unresolved | article: higher = better adjustment; actual coding uncertain |
| psy1004_grade | Header indicates a single psychology-course grade; differs from paper's weighted GPA | excluded from GPA inference; no exact GPA mapping available | higher grade intended better; exact metadata unavailable |
| nbt_completed | NBT-related source field; exact field-specific construction not independently established | not used as a substitute for nbt_ave | not established |
| nbt_year | NBT-related source field; exact field-specific construction not independently established | not used as a substitute for nbt_ave | not established |
| nbt_al | NBT-related source field; exact field-specific construction not independently established | not used as a substitute for nbt_ave | not established |
| nbt_math | NBT-related source field; exact field-specific construction not independently established | not used as a substitute for nbt_ave | not established |
| nbt_ql | NBT-related source field; exact field-specific construction not independently established | not used as a substitute for nbt_ave | not established |
| nbt_ave | Author-supplied NBT average; article specifies literacy, quantitative literacy and mathematics, 0–100% | mapped using article and matching descriptive statistics; use supplied NBT average | higher academic marks = better; age not an outcome |
| nbt_did_math | NBT-related source field; exact field-specific construction not independently established | not used as a substitute for nbt_ave | not established |
| nbt_alql_ave | NBT-related source field; exact field-specific construction not independently established | not used as a substitute for nbt_ave | not established |
| matric_mark | Grade 12 mark; average home-language and five highest other subjects, excluding Life Orientation, 0–100% | mapped using article and matching descriptive statistics; use supplied NBT average | higher academic marks = better; age not an outcome |
| asrs1_item_1 | Time 1 ASRS item 1; inattention; 0–4 | verified in Mohamad et al. Methods; no reverse scoring | higher = more symptoms |
| asrs1_item_2 | Time 1 ASRS item 2; inattention; 0–4 | verified in Mohamad et al. Methods; no reverse scoring | higher = more symptoms |
| asrs1_item_3 | Time 1 ASRS item 3; inattention; 0–4 | verified in Mohamad et al. Methods; no reverse scoring | higher = more symptoms |
| asrs1_item_4 | Time 1 ASRS item 4; inattention; 0–4 | verified in Mohamad et al. Methods; no reverse scoring | higher = more symptoms |
| asrs1_item_5 | Time 1 ASRS item 5; hyperactivity/impulsivity; 0–4 | verified in Mohamad et al. Methods; no reverse scoring | higher = more symptoms |
| asrs1_item_6 | Time 1 ASRS item 6; hyperactivity/impulsivity; 0–4 | verified in Mohamad et al. Methods; no reverse scoring | higher = more symptoms |
| asrs1_item_7 | Time 1 ASRS item 7; inattention; 0–4 | verified in Mohamad et al. Methods; no reverse scoring | higher = more symptoms |
| asrs1_item_8 | Time 1 ASRS item 8; inattention; 0–4 | verified in Mohamad et al. Methods; no reverse scoring | higher = more symptoms |
| asrs1_item_9 | Time 1 ASRS item 9; inattention; 0–4 | verified in Mohamad et al. Methods; no reverse scoring | higher = more symptoms |
| asrs1_item_10 | Time 1 ASRS item 10; inattention; 0–4 | verified in Mohamad et al. Methods; no reverse scoring | higher = more symptoms |
| asrs1_item_11 | Time 1 ASRS item 11; inattention; 0–4 | verified in Mohamad et al. Methods; no reverse scoring | higher = more symptoms |
| asrs1_item_12 | Time 1 ASRS item 12; hyperactivity/impulsivity; 0–4 | verified in Mohamad et al. Methods; no reverse scoring | higher = more symptoms |
| asrs1_item_13 | Time 1 ASRS item 13; hyperactivity/impulsivity; 0–4 | verified in Mohamad et al. Methods; no reverse scoring | higher = more symptoms |
| asrs1_item_14 | Time 1 ASRS item 14; hyperactivity/impulsivity; 0–4 | verified in Mohamad et al. Methods; no reverse scoring | higher = more symptoms |
| asrs1_item_15 | Time 1 ASRS item 15; hyperactivity/impulsivity; 0–4 | verified in Mohamad et al. Methods; no reverse scoring | higher = more symptoms |
| asrs1_item_16 | Time 1 ASRS item 16; hyperactivity/impulsivity; 0–4 | verified in Mohamad et al. Methods; no reverse scoring | higher = more symptoms |
| asrs1_item_17 | Time 1 ASRS item 17; hyperactivity/impulsivity; 0–4 | verified in Mohamad et al. Methods; no reverse scoring | higher = more symptoms |
| asrs1_item_18 | Time 1 ASRS item 18; hyperactivity/impulsivity; 0–4 | verified in Mohamad et al. Methods; no reverse scoring | higher = more symptoms |
| asrs1_total.x | Time 1 ASRS total, 18 items, 0–72 | verified against item sum in all rows | higher = more symptoms |
| bai1_item_1 | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| bai1_item_2 | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| bai1_item_3 | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| bai1_item_4 | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| bai1_item_5 | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| bai1_item_6 | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| bai1_item_7 | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| bai1_item_8 | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| bai1_item_9 | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| bai1_item_10 | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| bai1_item_11 | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| bai1_item_12 | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| bai1_item_13 | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| bai1_item_14 | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| bai1_item_15 | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| bai1_item_16 | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| bai1_item_17 | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| bai1_item_18 | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| bai1_item_19 | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| bai1_item_20 | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| bai1_item_21 | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| bai1_total | Time 1 BAI; items 0–3, total intended 0–63 | stored total conflicts with sum in 61 rows; excluded as regression covariate | higher = more anxiety symptoms |
| asrs1_total.y | Ambiguous merge artifact: values largely track BAI, not ASRS | excluded from inference; not treated as a second ASRS wave | not established |
| aas_change | Field named AAS change; may relate to article's mixed-model slopes | descriptive only; exact construction, wave data and IDs unavailable | not established |
