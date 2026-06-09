## Current Active Task

## Task 44 — Read-only candidate diagnostics integration design

Status: ACTIVE

Owning repo: score2gp-agentops

Branch:
`review/read-only-candidate-diagnostics-integration-design-v0.1`

PR title:
`docs(review): read-only candidate diagnostics integration design`

Context:
Governance review of PRs #231, #232, and #233 confirmed the primitive candidate extraction boundary is complete and safely devoid of semantic leakage. The extraction boundary currently produces `LeftMarginPrimitiveCandidate` and `XAlignedPrimitiveClusterCandidate` objects accurately mapping primitive geometries. Before modifying product code to emit these inside `inspect_pdf`, a design plan is required to ensure these remain safely isolated as read-only diagnostics without affecting the core primitive clustering pipeline or inadvertently triggering semantic grouping.

Goal:
Design the architectural path for safely attaching primitive evidence candidates to the top-level diagnostics payload.

Non-goals:
- Do not write product code.
- Do not implement candidate reporting logic.
- Do not propose semantic analysis or heuristics.
- Do not modify fixtures or snapshots.

Requirements:
- Plan exactly how `PdfGeometryCandidateExtractor` will be invoked by the diagnostics runner.
- Specify how the candidates will appear in `PdfStaffNotationGeometryDiagnostics` output.
- Enforce that candidates remain strictly supplementary "evidence for candidates" and do not substitute the existing morphology or basic clustering reports.

Validation:
- `git diff --check`

Stop conditions:
- Product repo is modified.
- Proposed design introduces semantic analysis.
- Governance repo is dirty before work.
- Validation fails.
