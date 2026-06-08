## Current Active Task

## Task 12 — Add manifest-driven fixture smoke test

Status: ACTIVE

Owning repo: score2gp

Branch:
test/pdf-fixture-manifest-smoke-v0.1

PR title:
test(pdf): run standard-staff fixture smoke tests from manifest

Purpose:
Use the fixture manifest to run a generic smoke test over all standard-staff synthetic PDFs.

Likely product files:
- tests/test_pdf_standard_staff_fixture_manifest.py
- or tests/test_pdf_standard_staff_diagnostics_fixtures.py

Non-goals:
- do not replace focused fixture tests
- do not add new fixtures
- do not infer semantics

Validation:
git diff --check
.venv/bin/python -m pytest tests/test_pdf_standard_staff_fixture_manifest.py
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py

Acceptance criteria:
- every manifest fixture loads through inspect_pdf
- diagnostics status is success
- exactly expected minimum staff count is asserted
- manifest and focused tests pass
