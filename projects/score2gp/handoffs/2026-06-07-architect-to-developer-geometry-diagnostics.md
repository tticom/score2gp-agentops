# Durable Handoff: Architect to Developer (pdf-staff-notation-geometry-diagnostics-v0.1)

## Context & Branch Details
- **Product Repository**: `score2gp` (active branch: `feature/pdf-staff-notation-geometry-diagnostics-v0.1`, matching product PR: #182)
- **Governance Repository**: `score2gp-agentops` (active branch: `research/pdf-staff-notation-geometry-diagnostics-v0.1`)
- **Task Goal**: Implement private-safe standard staff geometry diagnostics.

---

## 1. Private-Safe Diagnostic Schema

The diagnostic schema is designed to represent detected notation staves and summarize nearby drawing primitives without exposing any raw music notation values, unicode PUA character strings, or exact note coordinates.

Define this schema using Pydantic in `src/score2gp/pdf_staff_geometry.py`:

```python
from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field

class NotationStaffGeometry(BaseModel):
    model_config = ConfigDict(frozen=True)

    page_index: int = Field(ge=1)
    system_index: int = Field(ge=1)
    x0: float
    y0: float
    x1: float
    y1: float
    line_y_coords: list[float]

class LocalPrimitivesSummary(BaseModel):
    model_config = ConfigDict(frozen=True)

    line_count: int
    curve_count: int
    rect_count: int
    text_span_count_by_font: dict[str, int]

class NotationStaffDiagnostics(BaseModel):
    model_config = ConfigDict(frozen=True)

    staff: NotationStaffGeometry
    primitives: LocalPrimitivesSummary

class PdfStaffNotationGeometryDiagnostics(BaseModel):
    model_config = ConfigDict(frozen=True)

    staves: list[NotationStaffDiagnostics]
```

---

## 2. Bounded Developer Task

The Developer must implement this schema and gather the summary counts inside the standard-staff bounding box (extended vertically by `20.0` points padding above and below) on each page.

### Steps to implement:

1. **Create/Define Schema**:
   - Create `src/score2gp/pdf_staff_geometry.py` with the models above.

2. **Preserve Notation Staves**:
   - In `src/score2gp/pdf.py`, currently `classify_staff_line_group` is used in `_detect_tab_systems` to discard groups classified as `"notation"` or `"ambiguous"`.
   - Update `_detect_tab_systems` or extract a helper `_detect_notation_staves(page, page_index)` that identifies notation staves (5-line systems where `classify_staff_line_group` returns `"notation"` or `"ambiguous"`).
   - Represent each detected notation staff as a `NotationStaffGeometry` instance.

3. **Build Primitives Summary**:
   - For each `NotationStaffGeometry`, identify the vertical zone `[y0 - 20.0, y1 + 20.0]` and horizontal zone `[x0, x1]`.
   - Iterate through drawings (`page.get_drawings()`) and count:
     - `lines`: lines (`l`) whose bounding boxes lie within the vertical and horizontal zone.
     - `curves`: curves (`c`) whose bounding boxes lie within the zone.
     - `rects`: rectangles (`re`) whose bounding boxes lie within the zone.
   - Iterate through text spans from `page.get_text("dict")` and count text spans (grouped by font name) whose bounding boxes fall within the zone.
   - Construct `LocalPrimitivesSummary` and pair it in `NotationStaffDiagnostics`.

4. **Integrate into `inspect_pdf` Output**:
   - In `src/score2gp/pdf.py` `inspect_pdf()`, collect the `PdfStaffNotationGeometryDiagnostics` for all pages.
   - Add it to the returned summary dictionary under the key `"pdf_staff_notation_diagnostics"`. It should serialize cleanly to `inspect_pdf.json`.

5. **Test Obligations**:
   - Create `tests/test_pdf_staff_geometry_diagnostics.py`.
   - Add synthetic tests that mock/generate a page with a 5-line notation staff, some drawing paths (`fitz` drawings), and text blocks/spans.
   - Assert that `inspect_pdf` correctly captures and counts them under `"pdf_staff_notation_diagnostics"`.
   - Confirm all existing tests still pass.

---

## 3. Stop Conditions

- **Stop condition**: One valid schema is defined in `pdf_staff_geometry.py`, one task is outlined to build the diagnostics, and this handoff is written.
- **Safety check**: No raw text characters (from PUA or text blocks) or exact coordinates of individual notes/stems/beams are stored. Only aggregate counts are recorded to avoid leaks.
