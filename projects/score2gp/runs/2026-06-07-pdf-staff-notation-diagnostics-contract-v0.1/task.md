# Task List - Strengthen PDF Staff Notation Diagnostics Contract Tests

- `[x]` Add contract tests to `tests/test_pdf_staff_geometry_diagnostics.py`
  - `[x]` `test_diagnostics_private_safety_serialization`: Assert no raw span text, PUA glyph strings, or coordinate dumps are emitted.
  - `[x]` `test_diagnostics_out_of_zone_filtering`: Assert drawings/text outside padded zone are ignored and empty spans are skipped.
  - `[x]` `test_diagnostics_shape_and_staff_index`: Assert stable schema shape and staff_index preservation.
  - `[x]` `test_inspect_pdf_integration_boundary`: Assert `pdf_staff_notation_diagnostics` is integrated and serialized without leaking text under `inspect_pdf()`.
  - `[x]` `test_silent_exception_handling_behavior`: Document current silent exception handling behavior returning empty staves.
- `[x]` Run validation checks
  - `[x]` Run specific pytest on geometry diagnostics.
  - `[x]` Run complete pytest suite.
  - `[x]` Verify git diff, status, and search for large files.
- `[x]` Create Walkthrough document and present final report.
