# Run Record: Public PDF-Tab Duration Synthetic Fixture Creation

**Task**: PDFTAB-DUR-02: Public PDF-Tab Duration Synthetic Fixture Creation
**Status**: COMPLETED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer / Fixture Author

## Provenance and Revisions

- **Product Repository**: `tticom/score2gp`
  - Base Commit: `d70d559152c5aa357a7d2eb38e65b09f288bb08f`
  - Python Executable: `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python`
- **AgentOps Repository**: `tticom/score2gp-agentops`
  - Base Commit: `14e4345bfb33747841a047eaa98bdc4dffb1dd02`
- **Workflow Skills Lock**: `0d6d84879eff0d352b444fdeceb3bb7a098e0c47`

## Created Fixture File Hashes (SHA-256)

- `tests/fixtures/pdf/make_generated_pdf_tab_duration_pdf.py`: `f244d9e6ecad5cda0a8641f308d88f3e981b43d99dc688f389c0dd90270748f6`
- `tests/fixtures/pdf/generated_pdf_tab_duration.pdf`: `e72646c50cd58aa32c533d390f880db5b17526a770d5f92092c6eecc94602ede`
- `tests/test_pdf_tab_duration_fixture.py`: `316a13da8d6f8f8d95119d6c41a1cffa244184ff2d0c4d86a58c14fb098b8062`

## Rhythmic Notation Structure & Expected Oracle

The synthetic fixture generator draws a 6-line PDF tablature staff system with two bars bounded by barlines:

1. **Bar 1**:
   - 4 quarter notes on string 1 (open fret `0`).
   - Each note possesses an explicit vertical stem drawn below the staff.
2. **Bar 2**:
   - 2 flagged eighth notes (frets `2` and `3`) with vertical stems and diagonal flag strokes.
   - 2 beamed eighth notes (frets `4` and `5`) connected by a single thick horizontal beam stroke (`width=3.0`).
   - 4 beamed sixteenth notes (fret `7`) connected by a double horizontal beam stroke.

An explicit `EXPECTED_DURATION_ORACLE` dictionary structure is defined in `make_generated_pdf_tab_duration_pdf.py` and asserted in `test_pdf_tab_duration_fixture.py`.

## Validation and Evidence

1. **Unit Test Execution**:
   - Command: `.venv/bin/python -m pytest tests/test_pdf_tab_duration_fixture.py -v`
   - Outcome: 2/2 tests passed in 0.35s.
   - Verified that horizontal staff lines (6), vertical stem & barline strokes (>=15), non-staff beam strokes (>=3), and fret numbers (>=12) are detected by morphology diagnostics.

2. **Product Verification**:
   - Product `src/score2gp/` remains untouched (0 modifications under `src/`).

3. **Disconfirmation**:
   - Verified that no reference GP files or private inputs were used in generating this synthetic fixture.
