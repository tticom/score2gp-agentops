# 0033 - CR-07A Bounded Visual Vibrato and Slide Glyphs Evidence Seam

## Objective

Implement bounded Developer slice `CR-07A` in `tticom/score2gp`, as authorized by the merged architecture report `docs/design/cr07-bounded-embellishment-attachments-architecture.md`.

Introduce `VisualVibratoEvidence` and `VisualSlideEvidence` candidate extraction models in `src/score2gp/pdf_geometry.py` and visual drawing path parsing in `src/score2gp/pdf.py` to capture raw embellishment drawing evidence from vector PDF path primitives (`"c"` bezier curves, line segments) before note assignment and pitch resolution.

## Authorized Product Files

- `src/score2gp/pdf_geometry.py`
- `src/score2gp/pdf.py`
- `tests/test_cr07_embellishment_attachments.py`

No other product files in `src/` or `tests/` may be edited in this task. Do not edit `docs/design/cr07-bounded-embellishment-attachments-architecture.md` during this Developer implementation slice.

## Start

1. Work only in the canonical Ubuntu WSL repositories below `/home/tticom-automation/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `projects/score2gp/AGENT_CONTROL.md`, `projects/score2gp/ACTIVE_TASK.md`, `projects/score2gp/prompts/next/0033-cr07a-bounded-visual-vibrato-and-slide-glyphs-evidence-seam.md`, `docs/design/cr07-bounded-embellishment-attachments-architecture.md`, and product repository `AGENTS.md`.
4. Require clean governance and product worktrees.
5. Create product branch `agy/cr07a-bounded-visual-vibrato-and-slide-glyphs-evidence-seam` in `tticom/score2gp`.
6. Run `python scripts/agent_verify.py` in `score2gp` before making code modifications.

## Implementation Scope & Seam Contract

1. **`src/score2gp/pdf_geometry.py`**:
   - Define `VisualVibratoEvidence` Pydantic model with fields: `bbox: tuple[float, float, float, float]`, `cycles: int`, `amplitude: float`, `staff_index: int | None = None`.
   - Define `VisualSlideEvidence` Pydantic model with fields: `bbox: tuple[float, float, float, float]`, `slope: float`, `direction: str` (`"up"` | `"down"`), `string_index: int | None = None`.

2. **`src/score2gp/pdf.py`**:
   - In PyMuPDF drawing path extraction (`get_drawings`), detect wavy bezier curve sequences (`"c"`) near TAB staves as `VisualVibratoEvidence`.
   - Detect diagonal line primitives near TAB fret numbers as `VisualSlideEvidence`.
   - Attach extracted visual embellishments to `PDFStaffGeometry` candidate lists.

3. **`tests/test_cr07_embellishment_attachments.py`**:
   - Add unit tests verifying `VisualVibratoEvidence` and `VisualSlideEvidence` extraction from synthetic bezier and line drawing path inputs.
   - Verify negative controls (flat horizontal line segments are ignored as staff/barlines).

## Validation Commands

1. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python -m pytest tests/test_cr07_embellishment_attachments.py`
2. `/home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python scripts/agent_verify.py`

## Non-goals

- Downstream compiler/ScoreIR/GPIF embellishment note assignment changes are deferred to subsequent task slices.
- Audio/OMR pitch resolution changes are deferred.
