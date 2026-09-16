# Why Welch's test, and what is Holm?

## Why use Welch if the variances were similar?

They were fairly similar: the screen-negative group had SD 11.62 and the screen-positive group SD 10.67 (variance ratio 1.18). The median-centred Levene test gave p = 0.120, so it did not provide strong evidence of unequal population variances. That does not prove equality.

Welch's t-test was a deliberate default for comparing independent group means without requiring equal population variances. Unequal variances do not have to be demonstrated before using it. The pooled-variance Student t-test would also be reasonable here, and gives practically the same answer:

| Test | Two-sided, unadjusted p-value |
| --- | --- |
| Welch | 0.03154 |
| Student, pooled variance | 0.03165 |

Thus the result is not being driven by the choice of Welch. These are ASRS screen-positive versus screen-negative groups, not clinically confirmed ADHD versus non-ADHD groups.

[SciPy's test documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html) distinguishes the equal-variance Student test from Welch's test, which does not assume equal population variances.

## What does “Holm” mean on the graphs?

The graphs say **Holm**, rather than “Horn.” Holm is a multiple-testing adjustment, not another comparison of group means. Testing several hypotheses increases the chance of at least one false-positive finding. Holm adjusts p-values to control that chance across a defined family of tests (at 5% when using alpha = 0.05).

It orders the p-values from smallest to largest and applies progressively less stringent thresholds, beginning at alpha divided by the number of tests. Here, ten primary tests form one family; four secondary correlations form another. Sensitivity-model p-values are explicitly nominal.

For the screening-group comparison, the unadjusted Welch p = 0.03154 becomes **Holm-adjusted p = 0.12617** across the ten primary tests. It therefore does not meet the 0.05 threshold after correction. This does not prove that the groups are identical. The estimated difference is still −2.14 percentage points; Holm changes the strength of the statistical evidence, not that estimate.

[R's official documentation](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/p.adjust.html) describes Holm's method and its control of the family-wise error rate.

To reproduce the pooled-versus-Welch comparison:

```python
import pandas as pd
from scipy.stats import ttest_ind

d = pd.read_csv('data/analysis_variables.csv')
positive = d.loc[d.screen_positive == 1, 'course_mark'].dropna()
negative = d.loc[d.screen_positive == 0, 'course_mark'].dropna()
print(ttest_ind(positive, negative, equal_var=False))  # Welch
print(ttest_ind(positive, negative, equal_var=True))   # Student
```
