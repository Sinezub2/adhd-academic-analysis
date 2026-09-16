"""Build a self-contained notebook from the exact pipeline definitions and execute it."""
import argparse
import ast
import json
import sys
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parent
source = (ROOT/'analysis.py').read_text()
tree = ast.parse(source)
lines = source.splitlines()
functions = {n.name: '\n'.join(lines[n.lineno-1:n.end_lineno])
             for n in tree.body if isinstance(n, ast.FunctionDef)}
first_def = min(n.lineno for n in tree.body if isinstance(n, ast.FunctionDef))
imports = '\n'.join(lines[:first_def-1])
cells = []


def md(text):
    cells.append(nbformat.v4.new_markdown_cell(text))


def code(text, collapsed=False):
    cell = nbformat.v4.new_code_cell(text)
    if collapsed:
        cell.metadata['jupyter'] = {'source_hidden': True}
    cells.append(cell)


def definitions(*names):
    code('\n\n\n'.join(functions[n] for n in names), collapsed=True)


md('''# ADHD symptoms and academic outcomes

Complete, reproducible analysis of the supplied `archive.zip` / `ADHD.xlsx`.
The notebook contains the same implementation as `analysis.py`, with execution outputs and all final graphs.

**Research question:** Do students with ADHD benefit academically from institutional support?
First establish whether this dataset measures that exposure; if not, analyze defensible academic associations.

**Source:** [UCT/Zivahub dataset](https://doi.org/10.25375/uct.24906924), via the Kaggle mirror.
Instrument interpretation follows the [original study](https://doi.org/10.1177/10870547241310659).
These analyses use the workbook's PSY1004 course mark, not the paper's semester GPA.

Run all cells from this project folder with the packages in `requirements.txt`.
Implementation cells are collapsed for readability but contain the full code.''')
code(imports + '\n\nROOT = Path.cwd()\nif not (ROOT / "data/ADHD.xlsx").exists():\n    raise FileNotFoundError("Run this notebook from the adhd_academic_analysis folder.")\nfrom IPython.display import display, Markdown, Image\n')
definitions('pstr','mdtable','load_workbook','inspect_dataset')
md('''## 1. Load and inspect all data

Print shape, every column, data types, missing values, descriptive statistics and treatment/diagnosis labels.
Inspect both sheets and spreadsheet metadata. Literal `no`, `none` and `not applicable` are preserved.
Complete categorical unique-value counts are also saved locally; participant narratives never appear in graphs.''')
code('raw, metadata = load_workbook(ROOT / "data/ADHD.xlsx", ROOT)\nschema = inspect_dataset(raw, metadata, ROOT)')
md('''## 2. Support feasibility and variable validation

**This dataset does not contain a sufficiently clear variable for institutional academic support, so a support-vs-no-support comparison would not be valid.**

Medication and counselling are general psychiatric history questions, with no academic purpose or institutional provider specified. No support exposure is constructed.

Validate questionnaire totals against their constituent items, require complete items, and distinguish symptoms from diagnosis. The six-item screening sum uses the [Harvard/NCS research rule](https://www.hcp.med.harvard.edu/ncs/ftpdir/adhd/ASRS_v1.1_screener%286Q%29_scoring_update.pdf): ≥14 is screen positive, not a diagnosis. No arbitrary median split is used.

Main adjustment analyses use only complete nine-item AAS responses. Anxiety is reconstructed because some provided totals disagree with the items. The `asrs1_total.y` field is not used as ADHD severity.''')
definitions('prepare_data')
code('d, checks = prepare_data(raw, metadata, ROOT)\ndisplay(checks)')
md('''## 3. Focused statistical analyses

Primary comparisons: ADHD total, inattention and hyperactivity against course marks and baseline adjustment; screening groups; both symptom dimensions in a joint mark model and their standardized contrast.

Report Pearson and Spearman associations, mean/median/SD, 95% CIs, Welch and Mann–Whitney results, Cohen's d, Hedges' g, regression coefficients, p-values and R². HC3 intervals allow unequal residual variance. Ten primary tests use Holm adjustment. Four separate, targeted secondary correlations assess the imported adjustment-change index and overlap with depression/anxiety.

Sensitivity models add age, matric mark and NBT literacy average. Retain null results. Inference is observational, with no causal effect or Kazakhstan-specific inference. Covariate and sensitivity p-values are nominal; intervals are pointwise.''')
definitions('association','compare_groups','fit_model','analyze')
code('result = analyze(d, ROOT)')
code('display(result["tests"])\ndisplay(result["diagnostics"])')
md('''## 4. Presentation graphs

Full 0–100 scales are used for course marks; AAS uses its mathematical 9–45 range. Scatter bands show confidence intervals for the fitted mean, not prediction intervals. Figures are saved as standalone Plotly HTML and as PNG when Kaleido/Chrome is available. The final section ranks exactly three recommended graphs.''')
definitions('style','scatter_figure','create_figures','export_figures')
code('figures = create_figures(d, result)\nmanifest = export_figures(figures, ROOT, png=True)\ndisplay(pd.DataFrame(manifest))')
for name, title in [
    ('adhd_severity_vs_academic_performance','A. Overall ADHD severity and course marks'),
    ('inattention_vs_academic_performance','B. Inattention and course marks'),
    ('adhd_vs_academic_adjustment','C. Overall ADHD symptoms and academic adjustment'),
    ('inattention_vs_academic_adjustment','C. Inattention and academic adjustment'),
    ('adhd_screening_vs_academic_performance','D. ADHD screening groups and course marks'),
    ('symptom_dimensions_vs_academic_performance','E. Symptom dimensions, with and without prior attainment'),
    ('inattention_vs_adjustment_change','Secondary: imported academic-adjustment change index'),
    ('inattention_and_mental_health_symptoms','Secondary: overlap with depressive and anxiety symptoms'),
]:
    md(f'### {title}\n\n[Open interactive graph](outputs/{name}.html)')
    code(f'png_path = ROOT / "outputs/{name}.png"\nif png_path.exists():\n    display(Image(filename=str(png_path), width=1000))\nelse:\n    display(figures["{name}"])')
md('''## 5. Audit, limitations, and presentation recommendations

The summary below reports the calculated results and ranks three graphs by their relevance to the support-needs question. The best graph for “Why this problem matters” is identified explicitly. Generalizing to Kazakhstan and testing support effectiveness require different evidence.''')
definitions('write_reports')
code('summary = write_reports(d, result, metadata, checks, ROOT)\ndisplay(Markdown((ROOT / "DATA_AUDIT.md").read_text()))')
code('display(Markdown(summary))')
nb = nbformat.v4.new_notebook(cells=cells, metadata={
    'kernelspec': {'name':'python3','display_name':'Python 3 (analysis environment)','language':'python'},
    'language_info': {'name':'python','version':sys.version.split()[0]}})
target = ROOT/'adhd_academic_analysis.ipynb'
nbformat.write(nb,target)

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--execute',action='store_true')
    args=parser.parse_args()
    if args.execute:
        from nbclient import NotebookClient
        from jupyter_client import KernelManager
        from jupyter_client.kernelspec import KernelSpecManager
        kernel_root=ROOT/'.kernels'
        kernel_dir=kernel_root/'adhd-analysis'
        kernel_dir.mkdir(parents=True,exist_ok=True)
        (kernel_dir/'kernel.json').write_text(json.dumps({
            'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],
            'display_name':'ADHD analysis','language':'python'}))
        km=KernelManager(kernel_name='adhd-analysis',kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(kernel_root)]))
        client=NotebookClient(nb,km=km,timeout=240,resources={'metadata':{'path':str(ROOT)}})
        client.execute()
        nbformat.write(nb,target)
        print('Executed successfully:',target)
    else:
        print('Created:',target)
