# NPG-04D: Structural Signaling

## Objective
Add repeat barlines, endings, tempo/meter/key changes, and navigation relationships using vector-based structural signaling (e.g., stroke thickness for barlines, precise text coordinates).

## Contract
- **Input Class:** Standard staff and tablature vector strokes, barlines, and text annotations.
- **Observable Outputs:** Structural semantics attached to measures (e.g. repeat counts, alternate endings, tempo markers, key signatures).
- **Refusal/Partial-Output Behavior:** If navigational elements form a malformed cycle, refuse with `MalformedStructuralCycle`.
- **Allowed Paths:** `src/score2gp/pdf_structural_skeleton_diagnostics.py`, `src/score2gp/pdf_tab_bar_assembler.py`
- **Validation Commands:** `.venv/bin/python -m pytest tests/test_pdf_structural_skeleton_diagnostics.py`
- **Negative Controls:** Must not invent repeats or endings not explicitly present in the document.
- **Promotion Dependency:** NPG-03B, NPG-04C
- **Provenance:** Derived from the Structural Signaling requirement in `projects/score2gp/plans/2026-08-19-native-pdf-to-gp-and-audiveris-retirement.md`.
