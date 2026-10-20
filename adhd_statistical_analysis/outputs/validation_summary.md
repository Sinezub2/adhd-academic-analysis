# Validation summary

Checked 2026-10-20T15:24:15.220937+00:00.

- Full pipeline: exit code 0.
- Original parent-folder files unchanged by regeneration: **True**. Public raw and original local workbook match publisher MD5 and each other.
- Every generated CSV table and all five PNG figures identical after regeneration in the pinned environment: **True**. Seed 42 fixes the paired bootstrap uncertainty calculations.
- Numerical and provenance tests: exit code 0. Tests independently compare analytical Welch t/p with SciPy, verify effect direction and CI inversion, verify units/scaling and invalid inputs, and compare Holm corrections with statsmodels.
- Original Table 3 HTML is parsed to check the summary transcription. Raw-source hash, sample counts, complete-case selection, correct symptom subscale partition, absence of uncomputable aggregate statistics, report image links, and primary-analysis completion when raw data are inaccessible are checked.
- Visual review: all five plots inspected. Summary figures show actual published means and 95% CIs on the full 1–9 scale. Raw plots contain only released observations and label unresolved AAS scoring. No source workbook was edited or recalculated.
- GPA/wave/item-codebook gaps, AAS reverse coding and the old Holm p=.015 remain substantive source limitations, not failed arithmetic checks. Null audit findings and contrary published results are retained.

```text
.................                                                        [100%]
17 passed in 8.31s
```

Commands: `python run_analysis.py`, `python -m pytest -q`, or `python verify_outputs.py` to repeat this complete validation. Machine-readable checks and fingerprints: `validation_checks.json`.
