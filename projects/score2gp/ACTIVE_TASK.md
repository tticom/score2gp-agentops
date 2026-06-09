## Current Active Task

## Task 41 — Add primitive-evidence extractor skeleton

Status: ACTIVE

Owning repo: score2gp

Branch:
`feature/primitive-evidence-extractor-skeleton-v0.1`

PR title:
`feat(pdf): add primitive-evidence extractor skeleton`

Goal:
Implement a skeleton `PdfGeometryCandidateExtractor` that accepts the PR #227 diagnostic evidence arrays and returns empty structures conforming to the PR #229 geometry candidate models.

Context:
Governance design review (Task 40) explicitly approved starting the skeleton after hardening models and semantic gates. 

Hard Constraints (Stop Conditions):
- MUST BE skeleton-only.
- Do NOT implement real extraction rules.
- Do NOT implement left-margin or x-aligned candidate logic.
- Do NOT integrate reporting or modify `inspect_pdf`.
- Do NOT infer semantics.

(Refer to `projects/score2gp/tasks/2026-06-09-post-227-candidate-boundary-task-list.md` for full context).
