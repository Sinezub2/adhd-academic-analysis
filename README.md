# ADHD academic analysis

Start with **PRESENTATION_SUMMARY.md** for the ranked three graphs and slide wording.

See [METHODS_FAQ.md](METHODS_FAQ.md) for why Welch's test was used and what the Holm adjustment means.

- `adhd_academic_analysis.ipynb`: executed notebook with complete analysis code, tables and graphs.
- `analysis.py`: reproducible pipeline.
- `outputs/`: eight interactive, standalone Plotly HTML graphs and high-resolution PNGs when exported.
- `tables/`: full inspection, statistics, regression results, diagnostics and sensitivity checks.
- `DATA_AUDIT.md`: variable interpretation and cleaning decisions.
- `data/ADHD.xlsx`: exact supplied workbook; `analysis_variables.csv`: reproducible derived numeric variables.
- `analysis_log.txt`: printed inspection and all main numerical results.

## Rerun

```sh
cd ~/Desktop/adhd_academic_analysis
.venv/bin/python analysis.py
```

On another machine, create a Python environment and install `requirements.txt`, then run `python analysis.py`. HTML export works without a browser. PNG export requires Kaleido and its Chrome component; this machine has a project-local browser in `.browser`. Use `--skip-png` if unavailable. No source-data network access is needed.

The main findings concern associations with symptoms. The data do not measure institutional academic support, support effectiveness, or conditions in Kazakhstan. Do not describe screen-positive groups as clinically diagnosed, and do not relabel the course mark as GPA.

## Dataset attribution

Rousseau, Kim; Mohamad, Nawal; Dowlut, Fatimah; Gering, Milton; Thomas, Kevin. *ADHD and Common Mental Disorders: Effect on Academic Success in SA First-Years*. [UCT/Zivahub dataset](https://doi.org/10.25375/uct.24906924), licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), obtained through the [Kaggle mirror](https://www.kaggle.com/datasets/imtkaggleteam/adhd-mental-health). The supplied workbook is unchanged; derived variables, analyses and visualizations are documented in `DATA_AUDIT.md` and the notebook. The dataset license does not automatically license the analysis code.
