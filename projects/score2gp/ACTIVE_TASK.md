## Current Active Task

## Task 86 — Record Task 85 completion and authorise integrated whole-note diagnostics follow-up

Status: ACTIVE

Owning repo: score2gp-agentops

Branch:
`governance/task-86-record-whole-note-diagnostics-followup-v0.1`

PR title:
`docs(governance): record whole-note diagnostics and authorise integration follow-up`

Context:
Product PR #249 (Task 85) was successfully merged, adding diagnostic-only whole-note candidate detection. The implementation distinguished whole notes from half notes via stem exclusion and preserved strict semantic boundaries. Furthermore, a review process correction is needed: Codex comments are review evidence and must be explicitly dispositioned in reviews.

Goal:
Create a governance PR that records Task 85 completion, sets the whole-note vs half-note diagnostic boundary, records the Codex review process correction, and authorises Product Task 87: integrating whole-note diagnostics.

Non-goals:
- Do not modify the product repo.
- Do not implement product diagnostics in this governance task.
- Do not authorise ScoreIR emission.
- Do not authorise GP file emission.
- Do not authorise full semantic note recognition.
- Do not authorise pitch inference.
- Do not authorise rhythm inference beyond diagnostic labels.
- Do not authorise voice, measure, key signature, time signature, rest, or full-notation inference.
- Do not authorise OCR.
- Do not require private fixtures.
- Do not add another CI/gate/process-improvement task unless there is a serious blocker.

Constraints & Privacy Boundaries:
- Governance only: strictly update `ACTIVE_TASK.md` and the new decision markdown file.
- Keep output ephemeral and avoid tracking logs, GP files, or private JSON artifacts in the governance repo.

Acceptance criteria:
- `ACTIVE_TASK.md` is updated to Task 86.
- A new decision document records Product Task 85 completion.
- The decision document explicitly records the whole-note versus half-note distinction.
- The decision document explicitly requires reviewers to inspect and disposition Codex comments.
- The decision document authorises Product Task 87 as an integration follow-up.
- The decision document keeps all semantic and privacy boundaries intact.
- A governance PR is opened.
- No product repo files are changed.
- No generated/private artifacts are committed.

Validation:
- `git diff --check`
- `git status --short`
- `git ls-files | grep -Ei "(scratch|tmp|\.log$|screenshot|output|private_diagnostics|rendered|\.png$|\.jpg$|\.jpeg$|\.pdf$|\.gp$)" || true`
- `find . -path "./.git" -prune -o -type f -size +10M -print`
