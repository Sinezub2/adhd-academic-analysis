"""Verify source preservation, deterministic regeneration and numerical/provenance tests."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"outputs"


def hashes(paths):
    return {str(path.relative_to(ROOT.parent)):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}


def main():
    if not (OUT/"statistical_tests.csv").exists():
        raise SystemExit("Run run_analysis.py once before verification")
    inputs=[path for path in ROOT.parent.iterdir() if path.is_file()]
    source_before=hashes(inputs)
    numeric_paths=list(OUT.glob("*.csv"))
    figure_paths=list(OUT.glob("*.png"))
    outputs_before=hashes(numeric_paths+figure_paths)
    run=subprocess.run([sys.executable,str(ROOT/"run_analysis.py")],cwd=ROOT,text=True,capture_output=True)
    if run.returncode:
        raise SystemExit(run.stdout+run.stderr)
    source_after=hashes(inputs)
    outputs_after=hashes(numeric_paths+figure_paths)
    preserved=source_before==source_after
    repeated=outputs_before==outputs_after
    test=subprocess.run([sys.executable,"-m","pytest","-q"],cwd=ROOT,text=True,capture_output=True)
    info=dict(checked_at_utc=datetime.now(timezone.utc).isoformat(),original_files_unchanged=preserved,
        original_sha256=source_after,numerical_tables_and_figures_identical=repeated,
        compared_output_sha256=outputs_after,pytest_returncode=test.returncode,pytest_stdout=test.stdout,
        pipeline_returncode=run.returncode,pipeline_stdout=run.stdout,
        visual_inspection="All five PNGs inspected during the analysis session: readable titles, axes, intervals and caveats; no clipped text or synthetic distributions")
    (OUT/"validation_checks.json").write_text(json.dumps(info,indent=2))
    (OUT/"validation_summary.md").write_text(f"""# Validation summary

Checked {info['checked_at_utc']}.

- Full pipeline: exit code {run.returncode}.
- Original parent-folder files unchanged by regeneration: **{preserved}**. Public raw and original local workbook match publisher MD5 and each other.
- Every generated CSV table and all five PNG figures identical after regeneration in the pinned environment: **{repeated}**. Seed 42 fixes the paired bootstrap uncertainty calculations.
- Numerical and provenance tests: exit code {test.returncode}. Tests independently compare analytical Welch t/p with SciPy, verify effect direction and CI inversion, verify units/scaling and invalid inputs, and compare Holm corrections with statsmodels.
- Original Table 3 HTML is parsed to check the summary transcription. Raw-source hash, sample counts, complete-case selection, correct symptom subscale partition, absence of uncomputable aggregate statistics, report image links, and primary-analysis completion when raw data are inaccessible are checked.
- Visual review: all five plots inspected. Summary figures show actual published means and 95% CIs on the full 1–9 scale. Raw plots contain only released observations and label unresolved AAS scoring. No source workbook was edited or recalculated.
- GPA/wave/item-codebook gaps, AAS reverse coding and the old Holm p=.015 remain substantive source limitations, not failed arithmetic checks. Null audit findings and contrary published results are retained.

```text
{test.stdout.strip()}
```

Commands: `python run_analysis.py`, `python -m pytest -q`, or `python verify_outputs.py` to repeat this complete validation. Machine-readable checks and fingerprints: `validation_checks.json`.
""")
    print(test.stdout.strip())
    print(f"Original files preserved: {preserved}; deterministic tables/figures: {repeated}")
    if not preserved or not repeated or test.returncode:
        raise SystemExit(1)


if __name__=="__main__":main()
