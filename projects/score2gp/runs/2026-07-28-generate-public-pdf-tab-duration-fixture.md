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

- `tests/fixtures/pdf/make_generated_pdf_tab_duration_pdf.py`: `60a1d532ec79783490bd9005329c8593c8bdfb39973d864acf2facec8fa8b1f7`
- `tests/fixtures/pdf/generated_pdf_tab_duration.pdf`: `e18d4aaedb51eed6135c75ee7aa280f604ac19753d49e98f14bfa152633e57fd`
- `tests/test_pdf_tab_duration_fixture.py`: `5e8e104c689781b233ef497c70a5545222044ba14dc50fdaeaadd9399f6bc202`

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
