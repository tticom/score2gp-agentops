# PDF-Tab Duration-Evidence Adequacy Audit
Date: 2026-07-27
Author: tticom-automation

## Pinned Provenance
- **Product SHA**: `d70d559152c5aa357a7d2eb38e65b09f288bb08f`
- **AgentOps SHA**: `266a2695326db82d0d24e62690079c5927de2ac6`
- **Skills SHA**: `0d6d84879eff0d352b444fdeceb3bb7a098e0c47`
- **Python Executable**: `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python`
- **Resolved score2gp module**: `/home/tticom-automation/work/score2gp-workspace/score2gp/src/score2gp/__init__.py`

### Fixture SHAs (Author-reported vs Independently checked)
- `tests/fixtures/pdf/generated_scorelike_tab.pdf`: `b3106b083de608db600f63822c0a31f614fd96523ac27ffb5b2c80cd41d8d564`
- `tests/fixtures/pdf/generated_uneven_spacing_tab.pdf`: `673343c7ce2527a300c5ecf0b060180bd6bc9b8d69307dbb14f1a5ca9d06ccdc`
- `tests/fixtures/pdf/generated_paired_notation_tab_system.pdf`: Not found
- `tests/fixtures/pdf/make_generated_scorelike_tab_pdf.py`: `43a75ac5315f38f5c0926d12de0051636b1904713042c233c0abf8ae3558e995`
- `tests/fixtures/pdf/make_generated_uneven_spacing_tab_pdf.py`: `974c2c09eff445e75736ca018edd2c1c2432ee7d6dd5cd9dd320c624e6683368`

## Visual / Source Fixture Audit
1. `generated_scorelike_tab.pdf` / `make_generated_scorelike_tab_pdf.py`
   - Contains tablature: Yes.
   - Varied rhythmic notation: No.
   - Beams/flags/stems present: No (generator only draws lines and text).
   - Expected durations encoded anywhere: No.
   - Multi-bar suitable for oracle: Yes (2 systems, multiple bars).
2. `generated_uneven_spacing_tab.pdf` / `make_generated_uneven_spacing_tab_pdf.py`
   - Contains tablature: Yes.
   - Varied rhythmic notation: No.
   - Beams/flags/stems present: No.
   - Expected durations encoded anywhere: No.
   - Multi-bar suitable for oracle: Yes (2 bars).
3. `generated_paired_notation_tab_system.pdf`
   - Does not exist in the repository.

## Dataflow Audit
- Flag/beam candidates are currently created in `src/score2gp/whole_note_recogniser.py`.
- They are collected as `vertical_stroke_candidate` or `curve_candidate` by `NotationStaffDiagnostics` (as shown in `tests/test_pdf_staff_geometry_diagnostics.py`).
- These candidates do not reach `TabRaw` or the PDF-only event grouper (`PdfOnlyChordEventGrouper` in `src/score2gp/pdf_tab_bar_assembler.py:102`).
- The PDF-only timing heuristic is applied in `select_pdf_tab_grid_spacing_and_duration_name` (`src/score2gp/pdf_tab_measure_timing.py:24`), which sets an equal bucket size based purely on `event_subgroup_count` (`N`), ignoring any geometric duration markings.
- The smallest ownership boundary to consume duration evidence without mixing concerns would be passing duration candidates alongside `TabCandidate`s to `assemble_pdf_tab_bar`, or expanding `PdfOnlyChordEventGrouper` to associate duration symbols with `TabCandidate` subgroups.

## Executable Disconfirmation
**Command:** `.venv/bin/python -m pytest -q tests/test_pdf_staff_geometry_diagnostics.py tests/test_quarter_rest_e2e_acceptance.py tests/test_deterministic_multinote_sequencing.py`
**Result:** 19 passed in 1.50s.

**Strongest false-success mode tested:**
> Standard-staff beam diagnostics exist, but no committed public PDF-tab fixture or production seam can connect those candidates to PDF-only tab events; therefore green tests could falsely imply implementation readiness.

**Disconfirmation result:** The false-success mode is PROVED. The standard notation tests (`test_deterministic_multinote_sequencing.py`) pass and extract eighth/sixteenth notes from standard staves. However, no public PDF-tab fixture contains visual duration evidence (they lack drawn flags/beams), and the PDF-only tab assembler explicitly discards geometry in favor of a spatial heuristic (`select_pdf_tab_grid_spacing_and_duration_name`). The green tests falsely imply readiness for tab-only duration extraction.

## Decision
**PUBLIC_FIXTURE_GAP**
The production seam is plausible, but no adequate committed public PDF-tab oracle contains visual duration evidence (beams/flags/stems) to drive the implementation.

## Follow-up Candidate
Create a synthetic generated PDF-tab fixture (`generated_pdf_tab_durations.pdf`) that explicitly draws vertical stems, beams, and flags over tablature frets, ensuring measurable rhythmic variations (e.g., quarter, eighth, sixteenth notes) are visually present.
