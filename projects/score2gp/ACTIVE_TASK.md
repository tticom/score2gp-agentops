## Current Active Task

## Task 11 — Add fixture manifest

Status: ACTIVE

Owning repo: score2gp

Branch:
test/pdf-fixture-manifest-v0.1

PR title:
test(pdf): add manifest for synthetic standard-staff fixtures

Purpose:
Create a machine-readable manifest of synthetic PDF fixtures and their source JSON specs.

Likely product files:
- fixtures/public/standard_staff_fixture_manifest.json
- tests/test_pdf_standard_staff_fixture_manifest.py

Manifest entries:
- dense-margin
- sparse
- wide-curves
- complex-cluster

Each entry should include:
- fixture id
- JSON path
- PDF path
- generator script
- expected diagnostic focus
- synthetic=true
- private=false
- scanned=false
- ocr=false
- semantic_inference=false

Validation:
git diff --check
.venv/bin/python -m pytest tests/test_pdf_standard_staff_fixture_manifest.py
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py

Acceptance criteria:
- manifest paths exist
- manifest asserts all fixtures are synthetic
- no private/copyrighted/scanned/OCR fixture is listed
