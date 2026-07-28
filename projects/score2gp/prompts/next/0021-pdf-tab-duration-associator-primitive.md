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

## Empirical Hypothesis & Provisional Tolerances

The spatial association tolerances specified in `docs/design/pdf-tab-duration-candidate-extraction.md` ($\Delta x_{\text{stem\_tol}} \le \max(6.0\text{ pt}, 0.6 \times \text{staff\_space})$, beam horizontal overlap $\epsilon = 4.0\text{ pt}$, flag contact radius $r \le 8.0\text{ pt}$) are **provisional hypotheses**. Slice 1 implementation must empirically validate and refine these tolerances using exact boundary tests rather than assuming they are unshakeable facts.

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
   - Stem attachment, beam overlap, and flag contact logic.
   - Duration resolution mapping to nominal durations (`quarter` 960, `eighth` 480, `16th` 240, `32nd` 120 ticks).
   - Unstemmed fallback emission (`source = "equal_spacing_fallback"`).
   - **Fail-Closed Ambiguity Handling**: If multiple candidate stems/beams/flags are equidistant or conflicting, or if association is ambiguous, the associator must fail closed or assign fallback with reduced confidence / raise explicit associator error.

3. **Mandatory Test Cases (`tests/test_pdf_tab_duration_associator.py`)**:
   The unit test suite MUST include explicit coverage for:
   - **Measured Public Fixture Coordinates**: Exact coordinates and margins extracted from `generated_pdf_tab_duration.pdf`.
   - **Positive & Negative Association Cases**: Confirming matching strokes attach correctly and distant strokes are ignored.
   - **Just-Inside / Just-Outside Boundary Tests**: Testing values at $\text{tolerance} - \epsilon$ (attaches) vs $\text{tolerance} + \epsilon$ (fails/ignored) for stem, beam, and flag tolerances.
   - **Barline & Staff-Line Rejection**: Proving vertical barlines and horizontal staff lines are rejected and never misclassified as stems or beams.
   - **Neighbouring-Event & Ambiguous-Candidate Tests**: Testing closely spaced adjacent fret events sharing nearby strokes, ensuring correct assignment or fail-closed disambiguation.
   - **Scaled Synthetic Geometry Test**: At least one test case evaluating primitives under scaled page dimensions (e.g. $1.5\times$ or $0.75\times$ staff scaling).
   - **Fail-Closed Ambiguity Verification**: Testing ambiguous input geometry where association cannot be uniquely determined.

4. **Validation**:
   Run `.venv/bin/python scripts/agent_verify.py` and ensure all unit tests pass cleanly.

5. **Publication**:
   Open PR on `tticom/score2gp` and publish exact-head handback comment with `AWAITING_CODEX_REVIEW`.
