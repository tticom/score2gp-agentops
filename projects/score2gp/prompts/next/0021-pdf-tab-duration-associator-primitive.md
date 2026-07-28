# Developer Task: PDFTAB-DUR-04 (PDF-Tab Duration Types & Spatial Associator Primitive)

Execute Slice 1 of the PDF-Tab Duration Candidate Extraction Architecture defined in `docs/design/pdf-tab-duration-candidate-extraction.md`.

## Preflight

1. Work exclusively as `tticom-automation` in `/home/tticom-automation/work/score2gp-workspace/score2gp`.
2. Verify identity, HOME, GitHub CLI user, Git global user (`tticom-automation`), and canonical workspace path.
3. Read:
   - `docs/design/pdf-tab-duration-candidate-extraction.md`
   - `src/score2gp/pdf_staff_geometry.py`
   - `src/score2gp/pdf_staff_notation_diagnostics.py`
4. Checkout branch `agy/pdftab-duration-associator-primitive` from `origin/main` (`44ab38ca0ad8e0460469360f7ab3e9db29f98aa8`).

## Requirements

1. **Dataclasses (`src/score2gp/pdf_tab_duration_types.py`)**:
   Implement `TabDurationEvidence`:
   ```python
   from dataclasses import dataclass
   from typing import Literal

   @dataclass(frozen=True)
   class TabDurationEvidence:
       duration_name: Literal["whole", "half", "quarter", "eighth", "16th", "32nd", "64th"]
       duration_ticks: int
       stem_present: bool = False
       beam_count: int = 0
       flag_count: int = 0
       confidence: float = 1.0
       source: Literal["visual_morphology", "equal_spacing_fallback"] = "visual_morphology"
   ```

2. **Spatial Associator Primitive (`src/score2gp/pdf_tab_duration_associator.py`)**:
   Implement functions to associate vertical stem candidates, horizontal beams, and diagonal flags to event subgroup horizontal positions ($x_E$) on a staff system:
   - Stem attachment tolerance: $\Delta x \le \max(6.0\text{ pt}, 0.6 \times \text{staff\_space})$, vertical contact $\le 1.5 \times \text{staff\_space}$.
   - Beam attachment: horizontal overlap $\epsilon = 4.0\text{ pt}$, vertical extension $\le 6.0\text{ pt}$.
   - Flag attachment: contact radius $\le 8.0\text{ pt}$.
   - Resolution table:
     - 0 stems -> `source = "equal_spacing_fallback"`
     - Stem + 0 beams / 0 flags -> `quarter` (960 ticks)
     - Stem + 1 beam / 1 flag -> `eighth` (480 ticks)
     - Stem + 2 beams / 2 flags -> `16th` (240 ticks)
     - Stem + 3 beams -> `32nd` (120 ticks)

3. **Unit Tests (`tests/test_pdf_tab_duration_associator.py`)**:
   Test against extracted diagnostic primitives from `tests/fixtures/pdf/generated_pdf_tab_duration.pdf`.
   Verify correct nominal duration resolution for quarter, eighth, and sixteenth notes.

4. **Validation**:
   Run `.venv/bin/python scripts/agent_verify.py` and ensure all tests pass cleanly.

5. **Publication**:
   Open PR on `tticom/score2gp` and publish exact-head handback comment with `AWAITING_CODEX_REVIEW`.
