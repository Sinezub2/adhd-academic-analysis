# Presentation QA report

- **Slides:** 6 total: cover, 4 content slides, references.
- **Timing:** 675 spoken words; estimated 5.19 minutes at 130 words per minute.
- **Editability:** the GPA comparison is a native PowerPoint chart; all other graphics are editable PowerPoint shapes.
- **Speaker notes:** notes are embedded on every slide; the references slide is marked as not part of the timed script.
- **Sources:** eight sources are listed on the references slide and mapped in `SOURCE_AUDIT.md`.
- **Placeholders:** cover uses `[Presenter name(s)]`, `[Course]`, and `[Presentation date]` until supplied.
- **Assets:** each Plotly chart has HTML and PNG exports in `charts/`; the presentation also includes packaged Inter font files.
- **Methodological checks:** no support variable was invented; published GPA values are labeled as U.S. evidence; intervention claims distinguish combined ACCESS CBT-plus-mentoring from coaching evidence; no causal recommendation is made.
- **Automated structural check:** `python-pptx` opens the file successfully, reports six slides, and finds one embedded chart on the GPA slide. Keynote PDF export was attempted but did not complete in the local environment, so final visual review should also be done by opening the `.pptx` in PowerPoint or Keynote.
