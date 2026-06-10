## Current Active Task

## Task 62 — Decide pre-recognition evidence-quality gates and corpus review criteria

Status: ACTIVE

Owning repo: score2gp-agentops

Branch:
`governance/task-62-decide-pre-recognition-evidence-gates-v0.1`

PR title:
`docs(score2gp): decide pre-recognition evidence-quality gates and corpus review criteria`

Context:
Task 62 is a governance-only task.
Task 62 defines the corpus evaluation criteria and evidence-quality gates required before any semantic recogniser implementation may proceed.
Task 62 ensures that before `treble_clef_candidate` objects are promoted to fully recognised clefs emitting `ScoreIR`, the existing proportional heuristics must be evaluated against the private corpus.
Task 62 depends on the merge of Governance PR #113.

Goal:
Create a governance PR that decides whether further reporting validation, corpus review, or additional evidence-quality gates are needed before any recogniser work. This note must explicitly outline the review criteria for the diagnostics summary data and block product-side recognition until those criteria are met.

Non-goals:
- Do not modify the product repo.
- Do not implement code.
- Do not create or modify tests.
- Do not create fixtures.
- Do not add screenshots, rendered images, logs, debug dumps, PDFs, GP files, or local artifacts.
- Do not authorise ScoreIR emission.
- Do not authorise recognised clef objects.
- Do not authorise pitch, rhythm, key signature, time signature, notes, rests, voices, or musical semantics.
- Do not authorise OCR.
- Do not authorise vector/raster fusion.
- Do not authorise product recogniser implementation.

Acceptance criteria:
- Governance PR opened from `governance/task-62-decide-pre-recognition-evidence-gates-v0.1` to `main`.
- `ACTIVE_TASK.md` is updated to Task 62.
- `projects/score2gp/reviews/2026-06-10-pre-recognition-evidence-gates-decision.md` is added.
- PR #113 merge is verified in the decision note.
- The note defines evidence-quality gates and corpus review criteria.
- Semantic recognition remains explicitly blocked.

Stop conditions:
- Governance PR #113 is not merged.
- Governance repo is dirty before work starts.
- The task requires product repo modifications.

Reporting format:
- Branch name
- PR link
- Exact files changed
- Commit hash
- Commands run
- Validation results
- Privacy/artifact check results
- How PR #113 merge was verified
- Boundary summary
- Known limitations
- Whether PR is ready for review
