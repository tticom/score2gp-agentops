# NPG-04C: Geometric Rhythm Extraction

## Objective
Implement geometric rhythm extraction as defined in the ADR NPG-00R.

## Contract
- **Input Class:** Standard staff vector strokes containing stems, beams, and noteheads.
- **Observable Outputs:** Rhythm durations attached to `TabCandidate` events.
- **Refusal/Partial-Output Behavior:** If stems are present but noteheads are absent, the parser must refuse to extract rhythm for that chord and emit `MissingRhythmGeometry`.
- **Allowed Paths:** `src/score2gp/pdf_geometry_candidate_extraction.py`
- **Validation Commands:** `.venv/bin/python -m pytest tests/test_pdf_geometry_candidate_extraction.py`
- **Negative Controls:** Must not infer standard rhythm if the PDF is tablature-only (must rely exclusively on TAB stems).
- **Promotion Dependency:** NPG-03B
- **Provenance:** Derived from the `Geometric Rhythm Extraction` requirement in `runs/2026-08-20-npg-00r-automation-handoff.md`.
