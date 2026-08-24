# Implementation Plan - PDF Notation Diagnostics Exception Handling Refactor

This plan describes how we will refactor standard-staff notation diagnostics exception handling inside the product repository on branch `refactor/pdf-staff-notation-diagnostics-exceptions-v0.1` to replace silent exception catching with a private-safe warning/status.

## Proposed Changes

### Product Code changes (`score2gp`):
* **Pydantic Schema (`src/score2gp/pdf_staff_geometry.py`)**:
  * Add `status: str | None = "success"` to `PdfStaffNotationGeometryDiagnostics` class.
* **Exceptions Propagation (`src/score2gp/pdf.py`)**:
  * Propagate exceptions from `_detect_notation_staff_groups` by removing the try-except wrapper.
  * In `inspect_pdf()`, wrap both standard staff detection and diagnostics building inside a single `try-except` block.
  * When an exception is caught, set `diags_dict = {"staves": [], "status": "pdf_notation_geometry_diagnostics_failed"}`.

### Tests (`tests/test_pdf_staff_geometry_diagnostics.py`):
* Re-use the contract tests from PR #183 (safety, filtering, and schema shape).
* Replace the two silent-exception tests with tests asserting the new status behavior:
  * `test_silent_exception_handling_behavior`: Verifies that a failure during `build_notation_diagnostics` is caught, records `pdf_notation_geometry_diagnostics_failed` in status, and ensures no exception text or sensitive path substrings leak.
  * `test_detect_notation_staff_groups_exception_handling`: Verifies that a failure during standard staff detection propagates and is handled as `pdf_notation_geometry_diagnostics_failed` status with no raw details leak.

---

## Verification Plan

### Automated Tests
* Run the target test file:
  ```bash
  env PYTHONPATH=src:. .venv/bin/pytest tests/test_pdf_staff_geometry_diagnostics.py -v
  ```
* Run the full test suite to ensure no regressions:
  ```bash
  env PYTHONPATH=src:. .venv/bin/pytest
  ```
* Run git diff checks to ensure code is clean and no private/large files are tracked:
  ```bash
  git diff --check
  git status
  git ls-files fixtures/private work
  find . -path "./.git" -prune -o -type f -size +10M -print
  ```
