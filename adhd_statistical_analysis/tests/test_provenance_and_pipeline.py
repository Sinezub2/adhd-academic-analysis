"""Checks against source evidence and independent library calculations."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from bs4 import BeautifulSoup
from scipy import stats
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parents[1]


def test_summary_transcription_matches_cached_original_table3():
    source=ROOT/"data/metadata/sarid_lipka_2023_table3.html"
    if not source.exists():source=ROOT/"data/metadata/sarid_lipka_2023.html"
    soup = BeautifulSoup(source.read_text(),"html.parser")
    tables = [t for t in soup.find_all("table") if "Total Adjustment" in t.get_text(" ",strip=True)]
    assert len(tables) == 1
    source_rows = {}
    for row in tables[0].find_all("tr"):
        cells = [cell.get_text(" ",strip=True) for cell in row.find_all(["td","th"])]
        if cells and cells[0] in ["Academic","Social"]:
            source_rows[cells[0]] = cells
    summaries = pd.read_csv(ROOT/"data/israel_table3.csv")
    assert len(summaries) == 4  # Aggregate rows, never fabricated participant observations.
    for _, row in summaries.iterrows():
        source = source_rows["Academic" if row.outcome=="academic_adjustment" else "Social"]
        mean_sd = tuple(map(float,re.findall(r"\d+\.\d+",source[4 if row.group=="ADHD only" else 2])))
        assert (row["mean"],row.sd) == mean_sd
        assert row.n == (68 if row.group=="ADHD only" else 197)


def test_workbook_authenticated_and_no_new_subject_selection():
    path = ROOT/"data/raw/Student Mental Health Article Data.xlsx"
    if not path.exists():pytest.skip("Public raw data unavailable")
    expected = json.loads((ROOT/"data/metadata/figshare_metadata.json").read_text())["files"][0]["computed_md5"]
    assert hashlib.md5(path.read_bytes()).hexdigest() == expected
    if (ROOT.parent/path.name).exists():
        assert (ROOT.parent/path.name).read_bytes() == path.read_bytes()
    raw = pd.read_excel(path,sheet_name="Sheet1")
    assert len(raw) == 506
    output = ROOT/"outputs/prepared_analysis_data.csv"
    if not output.exists():pytest.skip("Run pipeline before integration checks")
    prepared = pd.read_csv(output)
    assert len(prepared) == len(raw)
    assert np.array_equal(prepared.source_excel_row,np.arange(2,508))
    assert prepared.aas_complete.notna().sum() == raw[[f"aas1_item_{i}" for i in range(1,10)]].notna().all(axis=1).sum() == 488
    assert np.array_equal(prepared.asrs_total,prepared.inattention+prepared.hyperactivity)
    assert not {"psy1004_grade","asrs1_total.y","b1","b2"} & set(prepared.columns)


def test_executed_families_holm_and_pearson_independently():
    result_path=ROOT/"outputs/statistical_tests.csv"
    if not result_path.exists():pytest.skip("Run pipeline before integration checks")
    tests=pd.read_csv(result_path)
    assert len(tests.loc[tests.role=="primary"]) == 2
    for family,rows in tests.groupby("family"):
        assert rows.p_holm.to_numpy() == pytest.approx(multipletests(rows.p_raw,method="holm")[1],rel=1e-10)
        assert (rows.p_holm>=rows.p_raw-1e-12).all()
    prepared_path=ROOT/"outputs/prepared_analysis_data.csv"
    if prepared_path.exists():
        data=pd.read_csv(prepared_path)
        for _,row in tests.loc[tests.family=="SA_provisional_pearson_m3"].iterrows():
            sample=data[[row.predictor,row.outcome]].dropna()
            expected=stats.pearsonr(sample[row.predictor],sample[row.outcome])
            assert row.n == len(sample)
            assert row.estimate == pytest.approx(expected.statistic,rel=1e-10)
            assert row.p_raw == pytest.approx(expected.pvalue,rel=1e-10)
        observed=tests.loc[(tests.family=="SA_provisional_pearson_m3") & (tests.predictor=="inattention")].iloc[0]
        assert observed.estimate == pytest.approx(-.205,abs=.0005)
        assert observed.p_raw == pytest.approx(5.12e-6,abs=5e-9)


def test_report_image_links_and_summary_unavailable_values():
    report_path=ROOT/"outputs/ADHD_results_report.md"
    if not report_path.exists():pytest.skip("Run pipeline before integration checks")
    report=report_path.read_text()
    for relative in re.findall(r"!\[[^]]*\]\(([^)]+)\)",report):
        assert (report_path.parent/relative).is_file()
    d=pd.read_csv(ROOT/"outputs/descriptive_statistics.csv")
    aggregate=d.loc[d.data_type=="published rounded summaries only"]
    for column in ["median","q1","q3","iqr","minimum","maximum","skewness","missing_n","missing_percent"]:
        assert aggregate[column].isna().all()
    assert aggregate.unavailable_statistics.str.contains("not computable from summary statistics").all()


def test_unavailable_raw_data_does_not_block_summary_analysis(tmp_path):
    project=tmp_path/"isolated_analysis"
    project.mkdir()
    for name in ["run_analysis.py","write_report.py","statistics_helpers.py"]:
        shutil.copyfile(ROOT/name,project/name)
    (project/"data").mkdir()
    shutil.copyfile(ROOT/"data/israel_table3.csv",project/"data/israel_table3.csv")
    run=subprocess.run([sys.executable,str(project/"run_analysis.py")],capture_output=True,text=True,timeout=60)
    assert run.returncode==0,run.stdout+run.stderr
    output=pd.read_csv(project/"outputs/statistical_tests.csv")
    assert len(output)==2
    assert (output.role=="primary").all()
    assert output.p_holm.max()<.05
    report=(project/"outputs/ADHD_results_report.md").read_text()
    assert "South African raw data are unavailable" in report
    assert not (project/"outputs/prepared_analysis_data.csv").exists()
