# NPG-03B: Floating Barline Geometry Isolation

Status: SUPERSEDED by REC-07 — historical prompt, not executable

## Objective
Implement floating barline geometry isolation as defined in the ADR NPG-00R.

## Contract
- **Input Class:** PDF pages containing floating vertical barlines that do not perfectly intersect the staff bounds (e.g., instructional formats).
- **Observable Outputs:** Extracted `TabCandidate` objects split logically by the floating barline X-coordinates.
- **Refusal/Partial-Output Behavior:** If a floating line thickness matches a repeat marker but lacks dots, it must emit a diagnostic warning and degrade to a standard barline, never crashing the parser.
- **Allowed Paths:** `src/score2gp/pdf_geometry.py`, `src/score2gp/pdf_tab_bar_assembler.py`
- **Validation Commands:** `.venv/bin/python -m pytest tests/test_pdf_geometry.py tests/test_pdf_tab_bar_assembler.py`
- **Negative Controls:** Must not emit a valid-success package if a floating barline creates a measure exceeding beat capacity.
- **Promotion Dependency:** NPG-00R
- **Provenance:** Tied directly to the `Floating Barlines` structural failure evidence documented in `runs/2026-08-20-npg-00r-automation-handoff.md`.
