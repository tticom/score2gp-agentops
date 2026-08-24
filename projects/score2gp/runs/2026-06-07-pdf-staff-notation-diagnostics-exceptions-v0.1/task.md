# Task List - PDF Notation Diagnostics Exception Handling Refactor

- `[x]` Propagate exceptions in standard staff grouping (`_detect_notation_staff_groups` in `pdf.py`).
- `[x]` Catch exceptions at serialization boundary inside `inspect_pdf` and set `status: "pdf_notation_geometry_diagnostics_failed"`.
- `[x]` Update Pydantic model `PdfStaffNotationGeometryDiagnostics` with an optional `status` field.
- `[x]` Replace the two silent exception contract tests in `test_pdf_staff_geometry_diagnostics.py` with tests asserting:
  - Success path returns `status: "success"`.
  - Failure path returns `status: "pdf_notation_geometry_diagnostics_failed"` without leaking traceback, raw text, or paths.
- `[x]` Run full validation checks.
- `[x]` Push branch and create product Pull Request #185.
