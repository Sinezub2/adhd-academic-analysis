# ADHD support in Kazakhstan — topic proposal

Open **ADHD_Support_Kazakhstan.pptx**. It contains six slides: cover, exactly four content slides, and one APA 7 References slide. Text, diagrams and the GPA chart are native, editable PowerPoint objects; the chart includes an embedded Excel data sheet. Speaker notes are embedded and also available in `SPEAKER_NOTES.md`.

The user's build brief takes precedence over the supplied ITMO PDF. The design borrows its large left-aligned titles, whitespace, outlined cards and one accent colour. No artwork or chart screenshot from the PDF is reproduced.

## Graph provenance

`charts/first_year_gpa.png`, `.svg` and `.html` are original Plotly renderings of **Gormley et al. (2019), Table 2**: fall ADHD 2.91, comparison 3.26; spring ADHD 2.79, comparison 3.13. The PowerPoint contains a native editable version of the same grouped bar chart, using the same data in `charts/gormley_2019_table2.csv`. The y-axis is 0–4. Published d values −0.48 and −0.41 are stored for audit but not displayed. No confidence intervals were invented. These descriptive group means are not support-versus-no-support data.

Source DOI: https://doi.org/10.1177/1087054715623046
Primary table: https://pmc.ncbi.nlm.nih.gov/articles/PMC6209537/
Author manuscript: https://libres.uncg.edu/ir/uncg/f/A_Anastopoulos_First_Year_2019.pdf

The mechanism and service/coaching pathways are original diagrams illustrating the proposal, not extracted data. International studies support investigating these approaches; they do not establish their effectiveness in Kazakhstan. The Kazakhstan gap is explicitly a working proposition. Nazarbayev University's documented service is acknowledged. The optional South African secondary finding is omitted to protect the four-slide limit and visual focus; no support variable is invented.

## Timing and cover

Spoken script: 675 words, approximately 5.2 minutes at 130 words/minute, plus short transitions/pauses. Presenter notes distinguish the ACCESS bundled intervention from coaching alone and the broad-disability sample from an ADHD-only sample. There is no final recommendation.

Cover: `[Presenter name(s)]` · `[Course]` · `[Presentation date]`. Bracketed fields are editable placeholders awaiting personal details.

## Fonts and editing

Inter Regular, SemiBold and Bold are packaged in `assets/fonts/` with the SIL Open Font License. Install them on another computer before editing to preserve wrapping. The PDF preview preserves the rendered appearance. The chart, text and shapes remain editable in PowerPoint.

## Rebuild

From the analysis project: `.venv/bin/python presentation/build_presentation.py`

Optional flags: `--presenter 'Name(s)' --course 'Course' --date 'Date'`. The build generates the PowerPoint, chart assets, CSV, speaker-note Markdown and metadata. Requirements are in `requirements.txt`. Plotly PNG/SVG export requires Kaleido and Chrome. Existing project-local Chrome is detected automatically. `render_presentation.applescript` exports the PPTX to a PDF with Keynote for visual checking, without rewriting the original PPTX.

See `SOURCE_AUDIT.md` for the claim-to-source checks and `QA_REPORT.md` for technical and visual validation. The `research/` working cache is excluded from version control; downloaded research papers are not redistributed as presentation assets.
