## Current Active Task

## Task 88 — Record whole-note diagnostics integration and authorise location-focused follow-up

Status: ACTIVE

Owning repo: score2gp-agentops

Branch:
`governance/task-88-record-integrated-whole-note-diagnostics-v0.1`

PR title:
`docs(governance): record integrated whole-note diagnostics and authorise location follow-up`

Context:
Product PR #250 (Task 87) was successfully merged. It integrated whole-note candidate diagnostics into the normal diagnostics flow, updated `raster_diagnostics_gate_report.py`, and proved the expected behaviour. It also correctly addressed trailing whitespace and local artifacts flagged by Codex. The half-note exclusion boundary is intact. Future reviews must include a “Codex comment disposition” section.

Goal:
Create a governance PR that records Task 87 completion, notes the integration of whole-note diagnostics, reaffirms the half-note boundary, and authorises Product Task 89: exposing whole-note candidate locations in the normal diagnostic output.

Non-goals:
- Do not modify the product repo.
- Do not implement product diagnostics in this governance task.
- Do not authorise ScoreIR emission.
- Do not authorise GP file emission.
- Do not authorise full semantic note recognition.
- Do not authorise pitch inference.
- Do not authorise rhythm/duration inference beyond diagnostic labels.
- Do not authorise voice, measure, key signature, time signature, rest, or full-notation inference.
- Do not authorise OCR.
- Do not require private fixtures.
- Do not create another CI/gate/process-improvement task unless there is a serious blocker.

Constraints & Privacy Boundaries:
- Governance only: strictly update `ACTIVE_TASK.md` and the new decision markdown file.
- Keep output ephemeral and avoid tracking logs, GP files, or private JSON artifacts in the governance repo.

Acceptance criteria:
- `ACTIVE_TASK.md` is updated to Task 88.
- A new decision document records Product Task 87 / PR #250 completion.
- The decision document authorises Product Task 89 as a product-visible diagnostic-location follow-up.
- The whole-note versus half-note boundary is preserved.
- Codex comment disposition remains required for future reviews.
- No product repo files are changed.
- No generated/private artifacts are committed.
- A governance PR is opened.

Validation:
- `git diff --check`
- `git status --short`
- `git ls-files | grep -Ei "(scratch|tmp|\.log$|screenshot|output|private_diagnostics|rendered|\.png$|\.jpg$|\.jpeg$|\.pdf$|\.gp$)" || true`
- `find . -path "./.git" -prune -o -type f -size +10M -print`
