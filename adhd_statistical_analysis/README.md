# ADHD statistical analysis

Executed analysis for the prompt in the parent folder. Read [the results report](outputs/ADHD_results_report.md) first. Original files remain unchanged.

Requires Python 3.11+ (executed with Python 3.12). From this directory:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python fetch_sources.py
python run_analysis.py
python -m pytest -q
python verify_outputs.py
```

If `uv` is available, the equivalent setup is:

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python fetch_sources.py
.venv/bin/python run_analysis.py
.venv/bin/python -m pytest -q
.venv/bin/python verify_outputs.py
```

The cached raw workbook and transcribed Israeli summary table are included, so `run_analysis.py` does not require network access. Use `requirements-lock.txt` instead of `requirements.txt` to reproduce the exact installed package versions. `fetch_sources.py` archives openly readable sources, checks Figshare's data license and MD5, logs failures, and never overwrites existing source files. If the download is unavailable, the pipeline uses the original parent-folder workbook when present; if neither exists, it still completes the Israeli summary analysis and marks the South African analysis pending. An explicit alternative workbook can be read using `--raw-file /path/to/workbook.xlsx`.

The GitHub distribution includes the CC BY 4.0 workbook and an attributed Table 3 extract for offline source-transcription checks. Downloaded full-article HTML/text caches stay local and can be recreated with `fetch_sources.py`. See the repository's [data attribution](../DATA_LICENSE.md), [bibliography](../references.bib), and [citation metadata](../CITATION.cff).

The two primary tests are Welch comparisons of self-reported academic and social adjustment in Sarid & Lipka (2023), ADHD-only n=68 versus no LD/ADHD n=197, with Holm correction across two tests. No pseudo-participants are created.

The South African file supports a provisional continuous-symptom score audit. Its weighted GPA is absent, the stored AAS score has unresolved reverse coding and 18 partial sums, `asrs1_total.y` is mislabeled/ambiguous, and longitudinal waves/IDs are missing. The report explains why these do not support a verified GPA model or an unconditional AAS conclusion. No diagnosis is inferred from ASRS scores.

Important outputs:

- `outputs/ADHD_results_report.md`: answers, numerical tables, figures, IMRaD paragraph, contrary findings and full references.
- `outputs/statistical_tests.csv`, `outputs/descriptive_statistics.csv`: machine-readable statistics and explicit availability/caveat columns.
- `outputs/academic_results.png`, `outputs/social_results.png`: real summary means with 95% CIs.
- `outputs/source_manifest.md`, `outputs/data_dictionary.md`, `outputs/cleaning_log.md`, `outputs/analysis_notes.md`: provenance, mappings and decisions.
- `outputs/column_inventory.csv`, `outputs/data_validation.json`: source integrity, missingness and scoring audit.
- `outputs/historical_reconciliation.json`: independent reconstruction of conflicting earlier claims.
- `outputs/south_africa_distributions.png`, `outputs/south_africa_associations.png`, `outputs/regression_diagnostics.png`: observed-data score-audit plots.
- `outputs/regression_coefficients.csv`, `outputs/regression_vif.csv`, `outputs/regression_diagnostics.json`: provisional AAS models, not GPA models.
- `outputs/run_metadata.json`, `outputs/validation_summary.md`: package versions, source hashes and verification.

See [analysis_plan.md](analysis_plan.md) for fixed test families and [data/metadata/source_review.md](data/metadata/source_review.md) for source verification. Seed 42 is used for 5,000 paired bootstrap samples for Spearman CIs. Results are associative, not causal; there is no Kazakhstan-specific effect estimate.
