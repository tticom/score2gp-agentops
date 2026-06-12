## Current Active Task

## Task 90 — Record whole-note location output and authorise diagnostic usability follow-up

Status: ACTIVE

Owning repo: score2gp-agentops

Branch:
`governance/task-90-record-whole-note-location-output-v0.1`

PR title:
`docs(governance): record whole-note location output and authorise usability follow-up`

Context:
Product PR #251 (Task 89) was successfully merged, exposing whole-note candidate totals, per-page counts, and exact locations in the normal diagnostic output via fields like `whole_note_candidate_pages` and `whole_note_candidate_locations`. It preserved the strict half-note exclusion boundary and verified that output remains purely diagnostic (no ScoreIR or GP generation, no semantic mapping).

Goal:
Create a governance PR that records Task 89 / PR #251 completion. Record that normal diagnostic report output now exposes whole-note candidate totals, per-page counts, and locations. Ensure the half-note exclusion boundary and the Codex comment disposition rule are preserved. Authorise Product Task 91: improving diagnostic usability for whole-note candidates by adding stable candidate IDs and deterministic ordering.

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
- `ACTIVE_TASK.md` is updated to Task 90.
- A new decision document records Product Task 89 / PR #251 completion.
- The decision document authorises Product Task 91 as a diagnostic usability follow-up.
- The whole-note versus half-note boundary is preserved.
- Codex comment disposition remains required.
- No product repo files are changed.
- No generated/private/local artifacts are committed.
- A governance PR is opened.
