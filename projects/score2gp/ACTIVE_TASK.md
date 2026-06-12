## Current Active Task

## Task 92 — Record deterministic whole-note candidate IDs and authorise report-summary follow-up

Status: ACTIVE

Owning repo: score2gp-agentops

Branch:
`governance/task-92-record-whole-note-candidate-ids-v0.1`

PR title:
`docs(governance): record whole-note candidate IDs and authorise summary follow-up`

Context:
Product PR #252 (Task 91) was successfully merged, adding deterministic candidate IDs (e.g. `whole_note_candidate_001`) and stable geometric ordering (bbox top, left, bottom, right) for whole-note candidates. It preserved diagnostic-only output boundaries and half-note exclusion.

Goal:
Create a governance PR that records Task 91 / PR #252 completion. Record the addition of deterministic IDs and geometric ordering. Record the preservation of the half-note boundary and Codex comment disposition rules. Authorise Product Task 93: adding a machine-checkable whole-note candidate summary block to the normal diagnostic report output.

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
- Do not create another CI/gate/advisory workflow/process-improvement task.

Constraints & Privacy Boundaries:
- Governance only: strictly update `ACTIVE_TASK.md` and the new decision markdown file.
- Keep output ephemeral and avoid tracking logs, GP files, or private JSON artifacts.

Acceptance criteria:
- `ACTIVE_TASK.md` is updated to Task 92.
- A new decision document records Product Task 91 / PR #252 completion.
- The decision document authorises Product Task 93 as a diagnostic summary follow-up.
- Deterministic IDs and geometric ordering are recorded as complete.
- The whole-note versus half-note boundary is preserved.
- Codex comment disposition remains required.
- No product repo files are changed.
- No generated/private/local artifacts are committed.
- A governance PR is opened.
