## Current Active Task

## Task 13 — Add expected diagnostics snapshots for four fixtures

Status: ACTIVE

Owning repo: score2gp

Branch:
test/pdf-diagnostics-fixture-snapshots-v0.1

PR title:
test(pdf): add diagnostics snapshots for standard-staff fixtures

Purpose:
Commit small expected diagnostic JSON snapshots for the four synthetic fixtures to make diagnostic drift visible.

Likely product files:
- fixtures/public/expected_diagnostics_dense_margin.json
- fixtures/public/expected_diagnostics_sparse.json
- fixtures/public/expected_diagnostics_wide_curves.json
- fixtures/public/expected_diagnostics_complex_cluster.json
- tests/test_pdf_standard_staff_diagnostics_snapshots.py

Non-goals:
- no full inspect_pdf output if it includes unstable/noisy fields
- no private paths
- no semantic fields

Validation:
git diff --check
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_snapshots.py
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py

Acceptance criteria:
- stable expected diagnostics snapshots exist
- tests compare current stable subset against snapshots
- no semantic fields appear
