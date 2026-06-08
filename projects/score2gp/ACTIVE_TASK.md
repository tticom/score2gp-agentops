# Active Task: score2gp

Status:
ACTIVE

Execution source:
`projects/score2gp/APPROVED_TASK_QUEUE.md`

Current product baseline after product PR #203:
`0b73bd90898bc1f5a1bda6f5e61920d1e952c7f9`

Agents may execute this task only inside its written scope.

Agents must stop at READY_FOR_HUMAN_MERGE for every product or governance PR. Human merge is still required for every PR.

Agents must not skip, reorder, invent, or materially edit queue items.

## Current Active Task

## Task 8 — Add schema snapshot regeneration helper

Status: ACTIVE

Owning repo: score2gp

Branch:
test/diagnostics-schema-snapshot-regenerator-v0.1

PR title:
test(pdf): add diagnostics schema snapshot regeneration helper

Purpose:
Add a small script that regenerates `fixtures/public/pdf_staff_geometry_diagnostics_schema.json` from `PdfStaffNotationGeometryDiagnostics`, so intentional schema changes have a reproducible update path.

Likely product files:
- tests/fixtures/pdf/make_pdf_staff_geometry_schema_snapshot.py
- fixtures/public/pdf_staff_geometry_diagnostics_schema.json
- tests/test_pdf_standard_staff_diagnostics_fixtures.py only if needed

Non-goals:
- do not change schema fields
- do not change diagnostics models
- do not add semantic candidates
- do not change parser behaviour

Validation:
git diff --check
.venv/bin/python tests/fixtures/pdf/make_pdf_staff_geometry_schema_snapshot.py
.venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py

Acceptance criteria:
- script regenerates the committed schema snapshot byte-for-byte
- snapshot test remains green
- anti-semantic schema test remains green
