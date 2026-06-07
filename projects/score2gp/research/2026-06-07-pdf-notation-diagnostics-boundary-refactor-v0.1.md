# ScoreToGP Research Record - PDF Notation Diagnostics Boundary Refactor

This document outlines the research and proposal for a narrow refactoring of the standard-staff notation diagnostics call path in the `score2gp` product repository.

## Current Call Path
In `src/score2gp/pdf.py`:
1. `inspect_pdf(path, out_dir)` is the main PDF inspection entry point.
2. Inside `inspect_pdf`, for each page, standard-staff notation diagnostics are collected via inline orchestration:
   ```python
   # Collect notation staves for diagnostics
   from .pdf_staff_notation_diagnostics import build_notation_diagnostics
   try:
       notation_groups = _detect_notation_staff_groups(page)
       notation_diags = build_notation_diagnostics(page, index, notation_groups)
       diags_dict = notation_diags.model_dump() if hasattr(notation_diags, "model_dump") else notation_diags.dict()
   except Exception:
       diags_dict = {"staves": [], "status": "pdf_notation_geometry_diagnostics_failed"}
   ```
   This couples `inspect_pdf` directly with group detection, error handling, Pydantic model serialization, and status fallback handling for diagnostics.

## Proposed Code Movement
To simplify `pdf.py` and modularize the boundary, we propose moving the diagnostics orchestration (the try-except wrapper, detection trigger, builder execution, and serialization) out of `inspect_pdf()` and into a clean helper function inside `src/score2gp/pdf_staff_notation_diagnostics.py`.

### Target Function
* **Module**: `src/score2gp/pdf_staff_notation_diagnostics.py`
* **Signature**:
  ```python
  def extract_notation_diagnostics_dict(page: Any, page_index: int) -> dict[str, Any]:
  ```

### Dependencies
The new `extract_notation_diagnostics_dict` function requires:
* `page` (fitz.Page) and `page_index` (int) as arguments.
* `_detect_notation_staff_groups` (imported dynamically from `score2gp.pdf` inside the function to prevent circular imports).
* `build_notation_diagnostics` (local function).

### Proposed Block inside `pdf_staff_notation_diagnostics.py`
```python
def extract_notation_diagnostics_dict(page: Any, page_index: int) -> dict[str, Any]:
    """
    Run standard-staff notation group detection and diagnostics builder,
    returning a private-safe serialized dictionary. On exception, returns
    a generic failure status.
    """
    from .pdf import _detect_notation_staff_groups
    try:
        notation_groups = _detect_notation_staff_groups(page)
        notation_diags = build_notation_diagnostics(page, page_index, notation_groups)
        return notation_diags.model_dump() if hasattr(notation_diags, "model_dump") else notation_diags.dict()
    except Exception:
        return {"staves": [], "status": "pdf_notation_geometry_diagnostics_failed"}
```

### Proposed Refactored Block inside `pdf.py`
```python
            # Collect notation staves for diagnostics
            from .pdf_staff_notation_diagnostics import extract_notation_diagnostics_dict
            diags_dict = extract_notation_diagnostics_dict(page, index)
```

---

## Coordinate Bounding-Box Validation Rules
Standard-staff notation diagnostics are constrained to specific vertical and horizontal regions calculated per staff group:
* **Horizontal Range**: Defined strictly by `[x0, x1]`, where:
  * `x0 = min(min(line.x0, line.x1) for line in group)`
  * `x1 = max(max(line.x0, line.x1) for line in group)`
* **Vertical Range**: Defined by `[y0 - 20.0, y1 + 20.0]` (representing a 20-point vertical padding above and below), where:
  * `y0 = min(line_ys)`
  * `y1 = max(line_ys)`
  * `line_ys = sorted([round((line.y0 + line.y1) / 2, 3) for line in group])`

Primitives (lines, curves, rects) and text spans must fall horizontally within `[x0, x1]` and vertically within `[y0 - 20.0, y1 + 20.0]` to be included.

---

## Error/Status Taxonomy
We enforce the following taxonomy for geometry validation failures:
* **Key**: `"status"`
* **Success state**: `"success"`
* **Geometry validation / exception fallback state**: `"pdf_notation_geometry_diagnostics_failed"`

No raw exception messages, stack traces, local filesystem paths, or file names may be returned in the failure state.

---

## Diagnostics JSON Compatibility
The returned dictionary must retain full backward compatibility with the existing JSON schema:
* Root structure: `{"staves": list, "status": str}`
* Each entry in `staves` must contain:
  * `"staff"`: Geometry coordinates matching `NotationStaffGeometry`.
  * `"primitives"`: Count totals matching `LocalPrimitivesSummary` including `line_count`, `curve_count`, `rect_count`, and `text_span_count_by_font` (restricted to count of spans per font name).
* No raw text, PUA character glyphs, or un-rounded coordinates may be serialized.

---

## Test Protection

### Existing Protective Tests
The following unit tests in `tests/test_pdf_staff_geometry_diagnostics.py` protect this boundary and are unaffected by signature changes to `build_notation_diagnostics` (which remains unchanged):
* `test_build_notation_diagnostics_mock`: Validates primitive and font sorting logic.
* `test_diagnostics_private_safety_serialization`: Asserts strict redaction of raw strings, PUA characters, and raw float coordinates.
* `test_diagnostics_out_of_zone_filtering`: Asserts vertical and horizontal coordinate bounding.

The following integration tests check standard-staff diagnostics integration via `inspect_pdf`:
* `test_inspect_pdf_notation_diagnostics_success`
* `test_inspect_pdf_notation_diagnostics_failure_handling`

### Proposed Missing/New Tests
We will add two new unit tests to `tests/test_pdf_staff_geometry_diagnostics.py` specifically for `extract_notation_diagnostics_dict`:
1. `test_extract_notation_diagnostics_dict_success`: Mocks a page returning valid notation staff groups, verifies it returns a serialized dictionary with `"status": "success"` and the expected staff metrics.
2. `test_extract_notation_diagnostics_dict_exception`: Mocks an exception inside `_detect_notation_staff_groups` or `build_notation_diagnostics`, and asserts it is gracefully caught, returning `{"staves": [], "status": "pdf_notation_geometry_diagnostics_failed"}` without leaking tracebacks.

---

## Privacy / Artifact Risks
* **No Path Leaks**: Never include raw absolute system paths (`/home/tticom/`, `/mnt/`, etc.) in test assertions or documentation files.
* **No Private File Names**: Never include actual private filenames in documentation or test outputs.
* **Redaction Verification**: Verify that the JSON output does not leak raw text or PUA characters.

---

## Developer Prompt for Implementation PR
```markdown
Title: Refactor PDF notation diagnostics orchestration into pdf_staff_notation_diagnostics.py

Task Description:
Refactor standard-staff notation diagnostics orchestration inside `src/score2gp/pdf.py` and `src/score2gp/pdf_staff_notation_diagnostics.py` to move the serialization and try-except wrapper into a dedicated helper function.

Files to Modify:
1. `src/score2gp/pdf_staff_notation_diagnostics.py`
2. `src/score2gp/pdf.py`
3. `tests/test_pdf_staff_geometry_diagnostics.py`

Instructions:

1. In `src/score2gp/pdf_staff_notation_diagnostics.py`, define:
   ```python
   def extract_notation_diagnostics_dict(page: Any, page_index: int) -> dict[str, Any]:
       """
       Orchestrates detection, extraction, and Pydantic serialization of standard-staff notation diagnostics.
       Gracefully catches exceptions and returns the standard failure dictionary on error.
       """
       from .pdf import _detect_notation_staff_groups
       try:
           notation_groups = _detect_notation_staff_groups(page)
           notation_diags = build_notation_diagnostics(page, page_index, notation_groups)
           return notation_diags.model_dump() if hasattr(notation_diags, "model_dump") else notation_diags.dict()
       except Exception:
           return {"staves": [], "status": "pdf_notation_geometry_diagnostics_failed"}
   ```

2. In `src/score2gp/pdf.py`, modify `inspect_pdf()`:
   Replace the inline `try-except` block for collecting notation staves:
   ```diff
   -            # Collect notation staves for diagnostics
   -            from .pdf_staff_notation_diagnostics import build_notation_diagnostics
   -            try:
   -                notation_groups = _detect_notation_staff_groups(page)
   -                notation_diags = build_notation_diagnostics(page, index, notation_groups)
   -                diags_dict = notation_diags.model_dump() if hasattr(notation_diags, "model_dump") else notation_diags.dict()
   -            except Exception:
   -                diags_dict = {"staves": [], "status": "pdf_notation_geometry_diagnostics_failed"}
   +            # Collect notation staves for diagnostics
   +            from .pdf_staff_notation_diagnostics import extract_notation_diagnostics_dict
   +            diags_dict = extract_notation_diagnostics_dict(page, index)
   ```

3. In `tests/test_pdf_staff_geometry_diagnostics.py`, import `extract_notation_diagnostics_dict` and implement:
   - `test_extract_notation_diagnostics_dict_success` to verify normal dictionary serialization.
   - `test_extract_notation_diagnostics_dict_exception` to verify exception catching and generic status serialization on failure.

4. Validation:
   - Run targeted tests: `env PYTHONPATH=src:. .venv/bin/pytest tests/test_pdf_staff_geometry_diagnostics.py`
   - Run the full test suite: `env PYTHONPATH=src:. .venv/bin/pytest`
   - Run lint checks and verify that no local paths or private names leak.
```

---

## Stop Conditions
* Stop at the Pull Request stage.
* Do not merge the product refactoring changes directly into `main` without maintainer oversight.
