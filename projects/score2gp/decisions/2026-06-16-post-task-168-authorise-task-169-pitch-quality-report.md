# Decision Record: Product Task 168 Completion and Task 169 Authorisation

## Product Task 168 Completion
Product Task 168 is complete and merged.

**Task 168 Details:**
- **Title**: Apply clef-resolved staff pitch mapping from deterministic clef evidence
- **Product PR**: [https://github.com/tticom/score2gp/pull/288](https://github.com/tticom/score2gp/pull/288)
- **PR Title**: `feat(recognition): apply clef-resolved staff pitch mapping`
- **Reported State**: merged
- **Final head SHA**: `beb99b17dd678c7794c919dfd7e714539bc002c3`
- **Merge commit**: `9ca53a20aa2f28b050bf668944f463ac30b49a31`
- **Merged at**: `2026-06-16T10:20:38Z`
- **Changed files**:
  - `src/score2gp/whole_note_recogniser.py`
  - `tests/test_note_candidate_recognition_report.py`

### Product Task 168 Outcome Summary
- Connected read-only `clef_resolved_staff_pitch` mapping into the main recognition pipeline.
- Mapping is driven only by deterministic staff-level `treble_clef_candidate` evidence.
- `clef_resolved_staff_pitch` is emitted only where exactly one valid deterministic staff-level `treble_clef_candidate` exists.
- Malformed, missing, unsupported, or ambiguous clef evidence fails closed.
- Out-of-staff notes still require required ledger-line support.
- `assumed_treble_pitch` remains separate and unchanged.
- `assume_treble_clef` was not used as visual clef evidence.
- Clef was not inferred from pitch outcomes, note positions, or ledger-line placement.
- No clef guessing was introduced.

### Strict Clef Policy Validation
- `treble_clef_candidate` evidence contributes to staff-level policy only when:
  - `candidate_id` is a non-empty string;
  - `source` is one of: `diagnostic_candidate_evidence` or `raster_diagnostic_candidate_evidence`
  - `page_index` is strictly an integer using `type(value) is int`;
  - `system_index` is strictly an integer using `type(value) is int`;
  - `staff_index` is strictly an integer using `type(value) is int`.
- Note-side staff lookup also requires strict integer `page_index`, `system_index`, and `staff_index`.
- Boolean index values fail closed.
- Unsupported source values fail closed.
- Missing or empty candidate IDs fail closed.
- Multiple valid clef candidates on the same staff fail closed.

### Validation Recorded
- Command: `.venv/bin/pytest tests/test_raster_treble_clef_bridge.py tests/test_note_candidate_recognition_report.py tests/test_note_candidate_recognition_cli.py tests/test_whole_note_recognition_cli.py`
- Result: `54 passed in 40.01s`
- PR body records clean privacy/artifact hygiene.
- CI and Raster Diagnostics Gate were green before merge.

### Behaviour Preservation
- Existing note extraction, ledger-line extraction, duplicate beam/ledger suppression, `staff_position_index`, `attached_ledger_line_candidate_ids`, and `assumed_treble_pitch` behaviour was preserved.
- Product Task 165 helper behaviour was preserved and connected only where strict evidence exists.
- Product Task 166 clef evidence boundary was preserved.
- Product Task 167 raster clef bridge was preserved.
- Whole-note recognition compatibility was preserved.
- Remained read-only/output-only.

### Codex Disposition
- No unresolved Product PR #288 Codex comments or review threads were present before merge.
- Product PR #288 review comments and review threads were checked during supervision and no active threads were present.

### Privacy / Artifact Hygiene
Clean. No new private fixtures, diagnostic dumps, scratch JSON, logs, GP files, screenshots, credentials, PDFs, or images were committed. Tracked public fixture PDFs or JSON files in hygiene checks are pre-existing and safe.

### Known Limitations
- Multi-staff systems without clear clef evidence on the specific target staff fail closed.
- Only treble clef candidates deterministically bridged by the diagnostic system are supported.
- Alternate clefs remain unsupported.
- `clef_resolved_staff_pitch` is now emitted under strict evidence boundaries, but it has not yet been reviewed as a canonical pitch representation for downstream output.

## Product Task 169 Authorisation
Product Task 169 is now authorised. Implementation must not begin until this governance PR is merged.

### Prompt: Product Task 169 — Add clef-resolved pitch quality report for public fixtures

#### Context
You are the product implementation agent for `tticom/score2gp`.

This task must only start after the governance PR authorising Product Task 169 has been merged.

Recent completed product work:
- Product Task 165 added read-only preparatory helper `map_clef_resolved_staff_pitch(outcomes, explicit_clef)`.
- Product Task 166 added the read-only clef candidate evidence boundary.
- Product Task 167 bridged deterministic raster-derived treble-clef diagnostic evidence into that boundary.
- Product Task 168 connected `clef_resolved_staff_pitch` into the main recognition pipeline under strict staff-level clef evidence policy.
- Product Task 168 preserved `assumed_treble_pitch` as a separate assumption-based field.
- Product Task 168 did not declare `clef_resolved_staff_pitch` canonical.
- Product Task 168 did not implement accidentals, key signatures, rhythm inference, ScoreIR, MusicXML, Guitar Pro output, OCR, or rests.

#### Goal
Add a read-only quality/coverage report for `clef_resolved_staff_pitch` over authorised public fixtures and/or existing public diagnostic outputs.

This task is about measuring and reporting output quality. It is not about adopting `clef_resolved_staff_pitch` as canonical pitch and not about generating playable output.

#### Functional Requirements
- Inspect existing public fixture/report infrastructure before changing anything.
- Reuse existing note-candidate recognition/reporting paths where possible.
- Add a small deterministic summary/report helper for `clef_resolved_staff_pitch` coverage.
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
- Use only authorised public fixtures or synthetic unit data.
- Do not add private PDFs or private diagnostic outputs.
- Do not declare `clef_resolved_staff_pitch` canonical.
- Do not remove or replace `assumed_treble_pitch`.
- Do not change pitch mapping semantics unless a blocker is reported.
- Preserve existing note extraction, ledger-line extraction, duplicate beam/ledger suppression, `staff_position_index`, `attached_ledger_line_candidate_ids`, clef candidate evidence extraction and mapping, `map_clef_resolved_staff_pitch(...)` behaviour, and whole-note recognition compatibility.

#### Implementation Guidance
- Work in `tticom/score2gp`.
- Create a focused product branch from current `main`, for example: `feature/clef-resolved-pitch-quality-report-v0.1`
- Inspect existing scripts and tests before editing.
- Likely relevant production files:
  - `src/score2gp/whole_note_recogniser.py`
  - any existing report script such as note-candidate recognition report scripts, if present.
- Likely relevant tests:
  - `tests/test_note_candidate_recognition_report.py`
  - `tests/test_note_candidate_recognition_cli.py`
  - `tests/test_whole_note_recognition_cli.py`
  - `tests/test_raster_treble_clef_bridge.py`
- Prefer adding a pure summary helper over adding a new large CLI surface.
- If a CLI/report command already exists for note candidates, extend it only in a backward-compatible way.
- Keep all changes read-only and diagnostic/reporting-only.

#### Non-goals
- Do not declare `clef_resolved_staff_pitch` canonical.
- Do not implement accidentals, key signatures, rhythm inference, ScoreIR, MusicXML, Guitar Pro or GP output, OCR, rests, or new visual clef recognition.
- Do not guess treble clef globally.
- Do not use `assume_treble_clef` as visual clef evidence.
- Do not infer clef from pitch outcomes, note positions, or ledger-line placement.
- Do not alter existing note-candidate extraction, ledger-line extraction, ledger-line grouping (unless blocked), raster clef detection (unless blocked) heuristics.
- Do not commit private fixtures, diagnostic dumps, scratch JSON, logs, credentials, screenshots, GP files, PDFs, images, or unrelated artifacts.

#### Required Pre-flight Checks
Run these before making changes:
    git status --short
    git branch --show-current
    git fetch --all --prune
    git checkout main
    git pull --ff-only
    git log --oneline --decorate --graph --max-count=20

Also verify that the governance PR authorising Product Task 169 is merged before making product changes.

#### Required Tests
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

#### Validation
Run focused tests covering raster bridge, note-candidate reporting, CLI output, and whole-note compatibility. At minimum:
    pytest tests/test_raster_treble_clef_bridge.py tests/test_note_candidate_recognition_report.py tests/test_note_candidate_recognition_cli.py tests/test_whole_note_recognition_cli.py
    git diff --check
    git diff --stat
    git status --short
    git status --ignored
    git ls-files | grep -Ei "(private|scratch|dump|log|\.pdf$|\.gp$|\.png$|\.jpg$|\.jpeg$|\.json$)" || true

If tracked public fixture JSON files appear in `git ls-files`, explain whether they are pre-existing and whether this task changed them. Do not add new private or unrelated artifacts.

#### Acceptance Criteria
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

#### Stop conditions
Stop and report instead of continuing if:
- Governance authorisation for Product Task 169 is not merged.
- Existing tests fail before your changes in a way that prevents clean attribution.
- Accurate quality reporting requires private fixtures or unapproved artifacts.
- Correct implementation requires canonical pitch adoption.
- Correct implementation requires accidentals, key signatures, rhythm inference, ScoreIR, MusicXML, GP output, OCR, or rests.
- Required evidence is ambiguous or missing.
- You would need to commit private fixtures, diagnostic dumps, scratch JSON, logs, credentials, screenshots, GP files, PDFs, images, or unrelated artifacts.
- You cannot produce a small, reviewable increment.

#### Commit and PR requirements
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

#### Reporting format
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
