## Current Active Task

## Task 84 — Reroute from advisory CI to visible whole-note diagnostic progress

Status: ACTIVE

Owning repo: score2gp-agentops

Branch:
`governance/task-84-reroute-whole-note-diagnostics-v0.1`

PR title:
`docs(governance): reroute from advisory CI to whole-note diagnostics`

Context:
Product PR #248 (Task 83) was successfully merged, adding an advisory CI workflow for the raster gate report. This completes the current process-improvement sequence. The workflow has spent too long on gates, reports, CI, and governance hygiene, and will now explicitly pause process-improvement work to return to product capabilities.

Goal:
Create a governance PR that records Task 83 completion, pauses process improvements, and authorises Product Task 85: read-only whole-note candidate diagnostics.

Non-goals:
- Do not modify the product repo.
- Do not implement whole-note detection in this governance task.
- Do not add another CI, gate, report, advisory workflow, process-control, or governance-hygiene task.
- Do not authorise ScoreIR emission.
- Do not authorise GP file emission.
- Do not authorise full semantic note recognition.
- Do not authorise pitch inference.
- Do not authorise rhythm inference beyond the diagnostic label `whole_note_candidate`.
- Do not authorise voice, measure, key signature, time signature, rest, or full-notation inference.
- Do not authorise OCR.
- Do not require private fixtures.

Constraints & Privacy Boundaries:
- Governance only: strictly update `ACTIVE_TASK.md` and the new decision markdown file.
- Keep output ephemeral and avoid tracking logs, GP files, or private JSON artifacts in the governance repo.

Acceptance criteria:
- `ACTIVE_TASK.md` is updated to Task 84.
- A new decision document records Task 83 completion and the strategic pivot.
- The document explicitly pauses further process-improvement work after Task 83.
- The document authorises Product Task 85 as read-only whole-note candidate diagnostics.
- The document preserves the semantic boundaries listed above.
- A governance PR is opened.
- No product repo files are changed.
- No generated/private artifacts are committed.

Stop conditions:
- PR #248 is not actually merged.
- Governance PR #128 is not actually merged.
- The governance repo is dirty before your changes.
- Required commands show unexpected product or private artifacts.
- You would need to modify the product repo.
- The task would drift into more CI/gate/report/process work instead of whole-note diagnostics.

Required validation:
- `git diff --check`
- `git status --short`
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
- summary of Task 84 decision
- exact Product Task 85 authorisation wording
- known limitations
- whether PR is ready for review
