# NPG-05: Layout Resilience & Irregular Rows

## Objective
Implement layout resilience for irregular rows.

## Contract
- **Input Class:** PDF pages containing varying numbers of bars per row (e.g. 3 bars on row 1, 4 on row 2, 1 on row 3).
- **Observable Outputs:** Accurately grouped TabCandidates across irregular staves without crashing the timeline assembler.
- **Refusal/Partial-Output Behavior:** If a staff system's width is severely truncated, emit IrregularStaffBoundsWarning.
- **Allowed Paths:** src/score2gp/pdf_tab_bar_assembler.py, src/score2gp/pdf_staff_tab_timing_aligner.py
- **Validation Commands:** .venv/bin/python -m pytest tests/test_pdf_tab_bar_assembler.py tests/test_pdf_staff_tab_timing_aligner_alignment.py
- **Negative Controls:** Must not force regular bucket distribution if evidence implies irregular groupings.
- **Promotion Dependency:** NPG-04D
- **Provenance:** Derived from the Layout Resilience & Irregular Rows requirement in uns/2026-08-20-npg-00r-automation-handoff.md.
