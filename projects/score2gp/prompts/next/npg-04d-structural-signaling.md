# NPG-04D: Vector-Based Structural Signaling

## Objective
Vector-Based Structural Signaling

## Contract
- **Input Class:** PDFs with textual section markers (e.g., "Chorus") and thick/thin vector repeat signs.
- **Observable Outputs:** `Section` and `Repeat` tags injected into the IR timeline.
- **Refusal/Partial-Output Behavior:** Unrecognized bold text above the staff must be classified as standard lyrics, not a structural section.
- **Allowed Paths:** `src/score2gp/pdf_geometry_candidates.py`
- **Validation Commands:** `.venv/bin/python -m pytest tests/test_timeline_repeats.py tests/test_pdf_geometry_candidates.py`
- **Negative Controls:** Must not inject a `Section` if the Y-offset heuristic exceeds the configured sensible default threshold (e.g. 50 points).
- **Promotion Dependency:** NPG-04C
- **Provenance:** Derived from the `Vector-Based Structural Signaling` requirement in `runs/2026-08-20-npg-00r-automation-handoff.md`.
