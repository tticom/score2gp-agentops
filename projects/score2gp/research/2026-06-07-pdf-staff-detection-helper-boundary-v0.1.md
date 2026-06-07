# PDF Staff Detection Helper Boundary Research v0.1

## Product state inspected
- Product main commit: `85d44eb`
- PR #188 status: Merged (`true`)
- Date: 2026-06-07

## Current dependency inventory

| Helper | Defined in | Imported by | Used by | Ownership classification | Notes |
|---|---|---|---|---|---|
| `_LineSegment` | `src/score2gp/pdf.py` | `pdf_staff_detection.py` | `pdf.py`, `pdf_staff_detection.py`, `pdf_staff_geometry.py`, and tests | Genuinely shared geometry class | Core coordinate data structure representing a vector line segment `(x0, y0, x1, y1)` in the PDF. |
| `_drawing_segments` | `src/score2gp/pdf.py` | `pdf_staff_detection.py` | `pdf.py`, `pdf_staff_detection.py` | Genuinely shared helper function | Parses vector drawing primitives from MuPDF drawings to extract horizontal/vertical lines. |
| `merge_collinear_horizontal_segments` | `src/score2gp/pdf.py` | `pdf_staff_detection.py` | `pdf.py`, `pdf_staff_detection.py`, and tests | Genuinely shared helper function | Consolidates broken horizontal segments across the page. Essential for both TAB and notation staffs. |
| `_tab_line_groups` | `src/score2gp/pdf.py` | `pdf_staff_detection.py` | `pdf.py`, `pdf_staff_detection.py` | Genuinely shared helper function | Scans the page vertically and clusters lines into staff-like groups. Shared by both 5-line standard notation and 6-line TAB detection. |
| `classify_staff_line_group` | `src/score2gp/pdf.py` | `pdf_staff_detection.py` | `pdf.py`, `pdf_staff_detection.py`, and tests | Genuinely shared helper function | Analyzes line counts, spacing (median gap), and fret overlaps to classify a group as `notation` or `tab`. |

## Test coverage map

| Behaviour/helper | Existing tests | Coverage strength | Missing tests |
|---|---|---|---|
| `_LineSegment` | Extensively tested across `test_pdf.py` and `test_pdf_staff_geometry_diagnostics.py`. | Strong | None. |
| `_drawing_segments` | Covered implicitly in page parsing and integration tests. | Strong | None. |
| `merge_collinear_horizontal_segments` | Direct unit tests (`test_merge_collinear_horizontal_segments_direct`, `test_merge_collinear_horizontal_segments_row_fragmentation_direct`). | Strong | None. |
| `_tab_line_groups` | Covered implicitly by layout classification and integration tests. | Medium | Dedicated unit tests for the vertical grouping logic on varying numbers of lines. |
| `classify_staff_line_group` | Direct unit test (`test_classify_staff_line_group_direct`). | Strong | None. |

## Circular import risks
Moving `classify_staff_line_group` to `src/score2gp/pdf_staff_detection.py` poses circular dependency risks because it requires:
1. `_has_fret_digit_intersection`, which depends on `parse_fret_text` from `tabraw.py`.
2. `_is_coherent_large_tab_group`, which is defined in `pdf.py`.

If `classify_staff_line_group` is moved to `pdf_staff_detection.py` while `_is_coherent_large_tab_group` remains in `pdf.py`, `pdf_staff_detection.py` must import it from `pdf.py`. However, `pdf.py` must import `classify_staff_line_group` from `pdf_staff_detection.py` for its TAB extraction logic (`_detect_tab_systems`). This forms a circular dependency loop.

## Candidate refactor options

### Option A: No immediate helper refactor (Recommended)
Keep all five helpers inside `pdf.py` for now. Standard notation detection continues to import them at the module level.
- **Pros**: Zero risk of breaking TAB extraction; zero circular dependencies; keeps the refactor boundary extremely small and focused.
- **Cons**: `pdf.py` remains large and retains geometry/drawing helpers.

### Option B: Isolate pure geometry primitives
Move only the three pure geometry utilities (`_LineSegment`, `_drawing_segments`, and `merge_collinear_horizontal_segments`) into a new dedicated module, such as `src/score2gp/pdf_geometry.py`.
- **Pros**: Decouples low-level geometry parsing from high-level staff/system grouping. No circular dependencies since these three helpers have zero dependencies on other parts of `pdf.py`.
- **Cons**: Requires updating imports across multiple test suites and files.

### Option C: Move all helpers including classification
Move all five helpers to `pdf_staff_detection.py`.
- **Pros**: Removes a large block of code from `pdf.py`.
- **Cons**: High risk of breaking TAB extraction. Requires moving TAB-specific classification details (`_is_coherent_large_tab_group`, `_has_fret_digit_intersection`) into a notation/staff-detection module, polluting its scope or creating circular imports.

## Recommended next refactor
Option A is recommended as the default path because standard-staff diagnostics are strictly metadata at this stage and must not impact TAB extraction.

If further clean decoupling is desired by the reviewers, **Option B** (isolating low-level geometry primitives into a new `pdf_geometry.py` module) represents the next smallest safe refactor.

## Why this is the smallest safe next step
Option B avoids circular dependencies entirely because `_LineSegment`, `_drawing_segments`, and `merge_collinear_horizontal_segments` do not call any functions defined in `pdf.py`. This separates the geometry representation layer from the staff-grouping and text-extraction layers without affecting staff classification logic.

## What must not change
- Standard staff detection and diagnostics payloads.
- TAB line detection and timing alignment.
- Fret digit and tuning classification.

## Developer prompt
Below is the developer prompt for Option B:

```text
Title: Refactor low-level PDF geometry primitives into sidecar module v0.1

Goal:
Isolate pure PDF geometry/drawing primitives out of `src/score2gp/pdf.py` into a new dedicated geometry module, preserving behaviour exactly.

Target module:
`src/score2gp/pdf_geometry.py`

Functions/classes to move:
* `_LineSegment` (class)
* `_drawing_segments` (function)
* `merge_collinear_horizontal_segments` (function)

Instructions:
1. Create `src/score2gp/pdf_geometry.py`. Move the three geometry helpers there. Keep standard typing and docstrings.
2. In `src/score2gp/pdf.py`, import the moved entities from `.pdf_geometry`.
3. In `src/score2gp/pdf_staff_detection.py`, import the moved entities from `.pdf_geometry` instead of `.pdf`.
4. Update unit tests in `tests/test_pdf.py` and `tests/test_pdf_staff_geometry_diagnostics.py` to import these helpers from their new location or via `score2gp.pdf` if exposed there.
5. Verify that all 522 tests in the suite remain green.
```

## Stop conditions
- Moving the three geometry helpers introduces any test failures or circular dependencies.
- Changes to timing alignment or ScoreIR are required.

## Privacy/artifact checks
- No private PDF fixtures or local file paths are referenced or committed.
- Large untracked directories/files are omitted from git tracking.
