## Current Active Task

## Task 80 — Record Task 79 completion and select next diagnostic-only path

Status: ACTIVE

Owning repo: score2gp-agentops

Branch:
`governance/task-80-next-diagnostic-path-v0.1`

PR title:
`docs(governance): add Task 80 decision on next diagnostic-only path`

Context:
Product PR #246 (Task 79) was successfully merged, adding subprocess-level CLI smoke tests for the gate report. However, the REVIEW subprocess path is still not proven end-to-end. CI enforcement should remain blocked until REVIEW exit behaviour can be tested safely without private data leakage or classifier changes.

Goal:
Create a governance decision document in `projects/score2gp/decisions/2026-06-12-post-task-79-next-diagnostic-path.md` summarizing the completed Task 79 evidence and formally selecting Task 81 as a product task focused on making REVIEW-path subprocess testing safe and deterministic.

Non-goals:
- Do not implement ScoreIR emission.
- Do not authorise recognised clef objects.
- Do not authorise semantic promotion of `treble_clef_candidate`.
- Do not authorise pitch, rhythm, key signature, time signature, note, rest, voice, or musical inference.
- Do not authorise OCR.
- Do not authorise vector/raster fusion.
- Do not authorise threshold tuning.
- Do not authorise classifier hardening.
- Do not implement product repo changes.
- Do not commit private/generated artifacts.

Constraints & Privacy Boundaries:
- Governance only: strictly update `ACTIVE_TASK.md` and the new decision markdown file.
- Keep output ephemeral and avoid tracking logs, GP files, or private JSON artifacts in the governance repo.

Acceptance criteria:
- A new decision document exists at `projects/score2gp/decisions/2026-06-12-post-task-79-next-diagnostic-path.md`.
- The document summarizes Task 79 as complete.
- The document explicitly blocks semantic promotion, classifier hardening, and vector/raster fusion.
- The document selects a new diagnostic-only Task 81 that makes REVIEW-path subprocess testing safe.
- `ACTIVE_TASK.md` is updated to Task 80.
- A PR is raised for this governance task.

Stop conditions:
- Governance `main` is dirty before work starts.
- Product repo files are modified.
- The task attempts to authorise semantic promotion, vector/raster fusion, or classifier hardening.

Required validation:
- `git status --short`
- `git diff --check`
- `git ls-files | grep -Ei "(scratch|tmp|\.log$|screenshot|output|private_diagnostics|rendered|\.png$|\.jpg$|\.jpeg$|\.pdf$|\.gp$)" || true`
- `find . -path "./.git" -prune -o -type f -size +10M -print`

Reporting format:
- branch name
- PR link
- full commit hash
- exact files changed
- commands run
- validation results
- privacy/artifact check results
- summary of Task 80 decision
- selected next diagnostic-only product task
- known limitations
- whether PR is ready for review
