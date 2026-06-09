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
- Do not make any product repo modifications.
- Do not make any product schema changes.
- Do not make any snapshot changes.
- Do not implement diagnostics output.
- Do not propose semantic terms or inference heuristics.

Requirements:
- Design only.
- Output should be a governance design note only.
- Plan exactly how `PdfGeometryCandidateExtractor` will be invoked by the diagnostics runner.
- Specify how the candidates will appear in `PdfStaffNotationGeometryDiagnostics` output.
- Enforce that candidates remain strictly supplementary "evidence for candidates" and do not substitute the existing morphology or basic clustering reports.

Validation:
- `git diff --check`

Stop conditions:
- Product repo is modified.
- Schema changes are attempted.
- Snapshot changes are attempted.
- Diagnostics output implementation is attempted.
- Semantic analysis or inference is introduced.
- Output includes anything other than a governance design note.
- Governance repo is dirty before work.
- Validation fails.
