## Current Active Task

## Task 37 — Define geometry candidate boundary from primitive evidence

Status: ACTIVE

Owning repo: score2gp

Branch:
`docs/primitive-evidence-candidate-boundary-v0.1`

PR title:
`docs(pdf): define candidate boundary from primitive evidence`

Context:
Product PR #227 (`feat(pdf): expose primitive-level geometry diagnostics`) was merged on 2026-06-09.

Verified baseline for this task:
- PR #227 head SHA: `3276e27a6cd0877fdbdb0eaa3d8a5a0af67b6f02`
- PR #227 merge commit: `44508b260fd9e7677faed8654a40ecdb4a1c94ef`

Goal:
Add a product architecture note that defines the candidate boundary, allowed model concepts, input evidence, non-goals, stop conditions, and fixture proof required before any extractor implementation.

Non-goals:
- Do not implement candidate extraction.
- Do not add candidate model classes.
- Do not integrate candidates into `inspect_pdf`.
- Do not emit ScoreIR.
- Do not infer musical semantics.
- Do not use private files or generated work artifacts.

Required pre-flight checks:
- Fetch and update product `main`.
- Confirm product PR #227 is merged.
- Confirm the product working tree is clean.

Likely product files:
- `docs/testing/primitive-evidence-candidate-boundary.md`
- optionally update `docs/testing/staff-geometry-diagnostics.md` only if it already exists and is the right home

Implementation guidance:
The document must define candidate inputs from:
- `StaffLeftMarginAggregateDiagnostics.evidence`
- `XAlignedClusterAggregateDiagnostics.evidence`
- `PrimitiveGeometryEvidence`
- `XAlignedPrimitiveClusterEvidence`

The document must define only geometry/visual concepts. Suggested allowed names:
- `PrimitiveEvidenceCandidate`
- `LeftMarginPrimitiveCandidate`
- `XAlignedPrimitiveClusterCandidate`
- `TextSpanPrimitiveCandidate`
- `CurvePrimitiveCandidate`
- `VerticalStrokePrimitiveCandidate`
- `HorizontalStrokePrimitiveCandidate`
- `DiagonalStrokePrimitiveCandidate`
- `RectanglePrimitiveCandidate`

Acceptance criteria:
- Document exists in product repo.
- It names PR #227 evidence arrays as the required source of truth.
- It forbids aggregate-derived, placeholder, and synthetic candidate coordinates.
- It defines model/input/output boundaries before implementation.
- It includes stop conditions for missing evidence.
- It does not approve extraction implementation.

Stop conditions:
- PR #227 is not present on product `main`.
- Evidence arrays are missing from schema or public fixtures.
- The design requires semantic names or musical inference.
- The document would need private examples.

Reporting format:
- Branch name
- PR link
- Files changed
- Commands run
- Validation result
- Known limitations
- Next recommended task
