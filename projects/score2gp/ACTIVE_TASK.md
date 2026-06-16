# Active Product Task

## Product Task 169 — Add clef-resolved pitch quality report for public fixtures

### Scope
- Work in `tticom/score2gp`.
- Add a read-only quality/coverage report for `clef_resolved_staff_pitch` over authorised public fixtures and/or existing public diagnostic outputs.
- Reuse existing note-candidate recognition/reporting paths where possible.
- The report should count, at minimum:
  - total note candidates in scope;
  - note candidates with `staff_position_index`;
  - note candidates on staves with valid `treble_clef_candidate` evidence;
  - note candidates with `clef_resolved_staff_pitch`;
  - in-staff mapped notes;
  - out-of-staff mapped notes;
  - out-of-staff notes missing required ledger support;
  - notes skipped because clef evidence was missing;
  - notes skipped because clef evidence was ambiguous;
  - notes skipped because staff association was malformed;
  - notes skipped because staff position was malformed.
- The report should include enough sample detail to diagnose failures without dumping private data.
- If existing public fixtures do not currently produce `clef_resolved_staff_pitch`, the report should still fail closed and report zero coverage honestly.
- Preserve existing note extraction, ledger-line extraction, duplicate beam/ledger suppression, `staff_position_index`, `attached_ledger_line_candidate_ids`, clef candidate evidence extraction, `map_clef_resolved_staff_pitch(...)`, and `assumed_treble_pitch` behaviour.

### Non-Goals
- Do not declare `clef_resolved_staff_pitch` canonical.
- Do not implement accidentals, key signatures, rhythm inference, ScoreIR, MusicXML, Guitar Pro or GP output, OCR, or rests.
- Do not implement new visual clef recognition.
- Do not guess treble clef globally.
- Do not use `assume_treble_clef` as visual clef evidence.
- Do not infer clef from pitch outcomes, note positions, or ledger-line placement.
- Do not alter existing note-candidate extraction, ledger-line extraction, ledger-line grouping (unless blocked), or raster clef detection (unless blocked).
- Do not commit private fixtures, diagnostic dumps, scratch JSON, logs, credentials, screenshots, GP files, PDFs, images, or unrelated artifacts.

### Required Pre-flight Checks
Run these before making changes:
    git status --short
    git branch --show-current
    git fetch --all --prune
    git checkout main
    git pull --ff-only
    git log --oneline --decorate --graph --max-count=20

Also verify that the governance PR authorising Product Task 169 is merged before making product changes.

### Required Tests
Add or update tests proving:
- The quality report counts total in-scope note candidates.
- The quality report counts notes with `clef_resolved_staff_pitch`.
- The quality report separates in-staff and out-of-staff mapped notes.
- The quality report records notes skipped because clef evidence is missing.
- The quality report records notes skipped because clef evidence is ambiguous.
- The quality report records notes skipped because staff association is malformed.
- The quality report records notes skipped because staff position is malformed.
- The quality report records out-of-staff notes missing required ledger support.
- The report handles empty outcomes safely.
- The report handles malformed outcomes safely.
- Existing `clef_resolved_staff_pitch` mapping, `assumed_treble_pitch`, `staff_position_index`, `attached_ledger_line_candidate_ids`, clef evidence extraction, Task 167 raster clef bridge, and whole-note recognition compatibility remain unchanged.

### Validation
Run focused tests covering raster bridge, note-candidate reporting, CLI output, and whole-note compatibility. At minimum:
    pytest tests/test_raster_treble_clef_bridge.py tests/test_note_candidate_recognition_report.py tests/test_note_candidate_recognition_cli.py tests/test_whole_note_recognition_cli.py
    git diff --check
    git diff --stat
    git status --short
    git status --ignored
    git ls-files | grep -Ei "(private|scratch|dump|log|\.pdf$|\.gp$|\.png$|\.jpg$|\.jpeg$|\.json$)" || true

If tracked public fixture JSON files appear in `git ls-files`, explain whether they are pre-existing and whether this task changed them. Do not add new private or unrelated artifacts.

### Acceptance Criteria
- A deterministic read-only quality report exists for `clef_resolved_staff_pitch`.
- The report measures coverage and skip reasons without changing recognition semantics.
- The report works on synthetic unit data and/or authorised public fixtures.
- The task does not declare `clef_resolved_staff_pitch` canonical.
- The task does not emit playable output.
- The task does not guess clef context.
- Existing recognition behaviour is preserved.
- Focused tests pass.
- Hygiene checks pass.
- PR body records exact commands, results, files changed, branch name, full head SHA, and known limitations.

### Stop conditions
Stop and report instead of continuing if:
- Governance authorisation for Product Task 169 is not merged.
- Existing tests fail before your changes in a way that prevents clean attribution.
- Accurate quality reporting requires private fixtures or unapproved artifacts.
- Correct implementation requires canonical pitch adoption.
- Correct implementation requires accidentals, key signatures, rhythm inference, ScoreIR, MusicXML, GP output, OCR, or rests.
- Required evidence is ambiguous or missing.
- You would need to commit private fixtures, diagnostic dumps, scratch JSON, logs, credentials, screenshots, GP files, PDFs, images, or unrelated artifacts.
- You cannot produce a small, reviewable increment.

### Commit and PR requirements
- Commit only intentional product files.
- Push the feature branch.
- Open a product PR against `main`.
- The PR body must include:
  - Product Task 169 summary.
  - Governance PR verification result.
  - Exact files changed.
  - Report fields and boundary.
  - Validation commands and results.
  - Privacy/artifact hygiene result.
  - Confirmation that Task 162 behaviour remains unchanged.
  - Confirmation that Task 164 behaviour remains unchanged.
  - Confirmation that Product Task 165 helper behaviour remains unchanged.
  - Confirmation that Product Task 166 clef evidence boundary remains unchanged.
  - Confirmation that Product Task 167 raster clef bridge remains unchanged.
  - Confirmation that Product Task 168 mapping behaviour remains unchanged.
  - Confirmation that no canonical pitch adoption or playable output was introduced.
  - Known limitations.

### Reporting format
Return:
- Branch name.
- Product PR link.
- Full head SHA.
- Exact files changed.
- Summary of implementation or blocker found.
- Report fields and boundary.
- Validation commands and results.
- Privacy/artifact hygiene result.
- Confirmation that Task 162 behaviour remains unchanged.
- Confirmation that Task 164 behaviour remains unchanged.
- Confirmation that Product Task 165 helper behaviour remains unchanged.
- Confirmation that Product Task 166 boundary behaviour remains unchanged.
- Confirmation that Product Task 167 bridge behaviour remains unchanged.
- Confirmation that Product Task 168 mapping behaviour remains unchanged.
- Confirmation that no canonical pitch adoption or playable output was introduced.
- Known limitations.
- Suggested next task.
