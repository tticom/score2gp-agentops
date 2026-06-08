## Current Active Task

## Task 10 — Add diagnostics field glossary to product docs

Status: ACTIVE

Owning repo: score2gp

Branch:
docs/staff-diagnostics-field-glossary-v0.1

PR title:
docs(pdf): add staff diagnostics field glossary

Purpose:
Create durable product documentation explaining each geometry diagnostics field, its intended meaning, and what it must not be used to infer yet.

Likely product files:
- docs/testing/staff-geometry-diagnostics.md

Must include:
- field names
- geometry-only meanings
- examples from fixtures
- forbidden semantic interpretations
- how to update schema snapshot intentionally

Validation:
git diff --check
grep -R -i -E "pitch|duration|clef|voice|key signature|notehead" docs/testing/staff-geometry-diagnostics.md || true

Acceptance criteria:
- glossary is product-owned
- glossary is consistent with schema snapshot
- no instruction to infer musical semantics
