# Record Product Task 163 completion and authorise Product Task 164

## Product Task 163 Completion

Product Task 163 implemented read-only `staff_position_index` extraction for `ledger_line_candidate` objects. The task was recorded in PR #283 in `tticom/score2gp`.

* **PR URL**: https://github.com/tticom/score2gp/pull/283
* **PR Title**: `feat(recognition): add staff-position indexes to ledger-line candidates`
* **Final head SHA**: `a308b0f43375624a0ce3130e11509c30243b47f2`
* **Merge commit**: `1558c00eee501479aff8c3993a9e355fdcbabcd8`
* **Merged timestamp**: `2026-06-15T17:31:20Z`

### Exact Files Changed
* `src/score2gp/whole_note_recogniser.py`
* `tests/test_note_candidate_recognition_cli.py`
* `tests/test_note_candidate_recognition_report.py`

### Staff-Position Convention Preserved
The existing convention was rigorously preserved:
* `0` = top staff line
* `1` = first space below top staff line
* `2` = second staff line
* values increase downward
* `8` = bottom staff line
* positions above the staff are negative
* positions below the staff are greater than `8`

### Product Task 163 Outcome Summary
* Added read-only `staff_position_index` to valid `ledger_line_candidate` objects.
* Reused the existing deterministic staff-position mapping logic in `map_staff_position_to_read_only_outcomes()`.
* Added `ledger_line_candidate` to the candidate types processed by staff-position mapping.
* Explicitly skipped `ledger_line_candidate` in `map_assumed_treble_pitch_to_read_only_outcomes()` so ledger lines do not receive `assumed_treble_pitch`.
* Tests verify ledger lines above the staff receive negative indexes.
* Tests verify ledger lines below the staff receive indexes greater than `8`.
* Tests verify no `assumed_treble_pitch` is added to `ledger_line_candidate`.
* Missing or malformed bbox/staff geometry fails closed.
* Product Task 163 remained strictly read-only.
* Existing note-candidate `staff_position_index` behaviour is preserved.
* Existing `assumed_treble_pitch` behaviour is preserved.
* Ledger-line extraction and duplicate beam suppression from Task 162 are preserved.
* Whole-note recognition compatibility is preserved.
* Existing note extraction is preserved.

### Validation
* Validation Command: `pytest tests/test_note_candidate_recognition_report.py tests/test_note_candidate_recognition_cli.py tests/test_whole_note_recognition_cli.py`
* Validation Result: `46 passed`

### Codex Disposition
The handover states no PR comments or review threads were present before merge, and no contrary evidence was found in GitHub's live state.

### Privacy/Artifact Hygiene Statement
No private fixtures, diagnostic dumps, scratch JSON, logs, credentials, screenshots, GP files, PDFs, images, or unrelated artifacts were committed. The only touched files were source files and tests, and existing public fixture data was fully preserved.

## Authorised Next Task
**Product Task 164 — Add ledger-line grouping to note candidates**

## Prompt for Product Task 164
```markdown
Title: Product Task 164 — Add ledger-line grouping to note candidates

Context:
You are the product implementation agent for `tticom/score2gp`.

This task must only start after the governance PR authorising Product Task 164 has been merged.

Recent completed product work:
- Product Task 162 preserved ledger-line extraction and duplicate beam suppression.
- Product Task 163 added read-only `staff_position_index` to valid `ledger_line_candidate` objects.
- Product Task 163 preserved note-candidate `staff_position_index`, preserved `assumed_treble_pitch`, and explicitly prevented `assumed_treble_pitch` from being added to `ledger_line_candidate`.

Product Task 163 staff-position convention:
- `0` = top staff line
- `1` = first space below top staff line
- `2` = second staff line
- values increase downward
- `8` = bottom staff line
- positions above the staff are negative
- positions below the staff are greater than `8`

Goal:
Add read-only grouping between valid note candidates and valid `ledger_line_candidate` objects.

Candidate note types in scope:
- `whole_note_candidate`
- `half_note_candidate`
- `quarter_note_candidate`
- `eighth_note_candidate`

Expected output:
Add an output field such as `attached_ledger_line_candidate_ids` or similar.

The field name must make clear these are references to existing ledger-line candidates, not embedded duplicate objects.

Functional requirements:
- Grouping must run after `staff_position_index` exists for both notes and ledger lines.
- A ledger line should attach only when geometry and staff-position logic both support it.
- Notes inside the standard staff range `0..8` should not receive ledger-line attachments unless a later evidence-based exception is explicitly authorised.
- Notes above the staff should only attach above-staff ledger lines with negative indexes that logically support the note position.
- Notes below the staff should only attach below-staff ledger lines with indexes greater than `8` that logically support the note position.
- Fail closed if the ledger line is ambiguous, missing geometry, missing staff association, or does not logically support the note.
- Preserve existing note extraction.
- Preserve existing ledger-line extraction.
- Preserve duplicate beam/ledger suppression.
- Preserve existing `staff_position_index`.
- Preserve `assumed_treble_pitch`.
- Preserve whole-note recognition compatibility.

Non-goals:
- Do not implement pitch inference.
- Do not implement ledger-line pitch mapping.
- Do not extend `assumed_treble_pitch` to ledger-line-supported notes.
- Do not implement clef recognition.
- Do not implement accidentals.
- Do not implement key signatures.
- Do not implement rhythm inference.
- Do not emit ScoreIR, MusicXML, Guitar Pro, GP output, OCR, or rests.
- Do not alter existing note-candidate extraction heuristics.
- Do not alter existing ledger-line extraction heuristics unless a blocker is reported.
- Do not commit private fixtures, diagnostic dumps, scratch JSON, logs, credentials, screenshots, GP files, PDFs, images, or unrelated artifacts.

Required pre-flight checks:
    git status --short
    git branch --show-current
    git fetch --all --prune
    git checkout main
    git pull --ff-only
    git log --oneline --decorate --graph --max-count=20

Also verify that the governance PR authorising Product Task 164 is merged before making product changes.

Implementation guidance:
- Work in `tticom/score2gp`.
- Create a focused product branch, for example:
  - `feature/ledger-line-note-grouping-v0.1`
- Inspect the existing candidate recognition flow before editing.
- Likely relevant file:
  - `src/score2gp/whole_note_recogniser.py`
- Likely relevant tests:
  - `tests/test_note_candidate_recognition_cli.py`
  - `tests/test_note_candidate_recognition_report.py`
  - `tests/test_whole_note_recognition_cli.py`
- Reuse existing candidate IDs.
- Do not duplicate ledger-line candidate objects inside note candidates.
- Prefer a deterministic helper that maps note candidates to supporting ledger-line candidate IDs after staff-position indexes have been assigned.
- The grouping logic should require both:
  - compatible staff-position relationship; and
  - compatible geometry.
- If either evidence path is missing or ambiguous, do not attach.
- Keep the field absent or empty consistently with existing project conventions. Inspect existing output style before deciding.
- Keep the change read-only and diagnostic/recognition-output-only.

Required tests:
Add or update tests proving:
- Correct grouping for notes above the staff.
- Correct grouping for notes below the staff.
- In-staff notes do not get spurious ledger-line attachments.
- Ambiguous or unrelated ledger lines remain ungrouped.
- No pitch inference is added.
- No `assumed_treble_pitch` extension occurs for ledger-line-supported notes.
- Existing Task 162 ledger-line extraction and duplicate beam/ledger suppression behaviour remains unchanged.
- Existing Task 163 ledger-line `staff_position_index` behaviour remains unchanged.
- Existing note-candidate `staff_position_index` behaviour remains unchanged.
- Existing `assumed_treble_pitch` behaviour remains unchanged.
- Whole-note recognition compatibility remains unchanged.

Validation:
Run focused tests covering note candidate reporting, CLI output, and whole-note compatibility. At minimum:

    pytest tests/test_note_candidate_recognition_report.py tests/test_note_candidate_recognition_cli.py tests/test_whole_note_recognition_cli.py
    git diff --check
    git diff --stat
    git status --short
    git status --ignored
    git ls-files | grep -Ei "(private|scratch|dump|log|\.pdf$|\.gp$|\.png$|\.jpg$|\.jpeg$|\.json$)" || true

If tracked public fixture JSON files appear in `git ls-files`, explain whether they are pre-existing and whether this task changed them. Do not add new private or unrelated artifacts.

Acceptance criteria:
- Valid out-of-staff note candidates can reference supporting valid ledger-line candidates by ID.
- Notes above the staff only attach logically supporting above-staff ledger-line candidates.
- Notes below the staff only attach logically supporting below-staff ledger-line candidates.
- In-staff notes do not receive spurious ledger-line attachments.
- Ambiguous, unrelated, malformed, missing-geometry, or missing-staff-association ledger lines remain ungrouped.
- Ledger-line candidate objects are not duplicated inside note candidate objects.
- Existing note extraction is preserved.
- Existing ledger-line extraction is preserved.
- Existing duplicate beam/ledger suppression is preserved.
- Existing `staff_position_index` behaviour is preserved.
- Existing `assumed_treble_pitch` behaviour is preserved.
- No pitch inference or treble-pitch extension is introduced.
- Whole-note recognition compatibility is preserved.
- Focused tests pass.
- Hygiene checks pass.
- PR body records exact commands, results, files changed, branch name, full head SHA, and known limitations.

Stop conditions:
Stop and report instead of continuing if:
- Governance authorisation for Product Task 164 is not merged.
- Existing tests fail before your changes in a way that prevents clean attribution.
- Correct grouping requires changing note extraction heuristics.
- Correct grouping requires changing ledger-line extraction heuristics.
- Correct grouping requires pitch inference, clef recognition, rhythm inference, accidentals, key signatures, ScoreIR, MusicXML, GP output, OCR, or rests.
- Required evidence is ambiguous or missing.
- You would need to commit private fixtures, diagnostic dumps, scratch JSON, logs, credentials, screenshots, GP files, PDFs, images, or unrelated artifacts.
- You cannot produce a small, reviewable increment.

Reporting format:
Return:
- Branch name.
- Product PR link.
- Full head SHA.
- Exact files changed.
- Summary of implementation.
- Output field name chosen and why.
- Validation commands and results.
- Privacy/artifact hygiene result.
- Confirmation that Product Task 162 behaviour remains unchanged.
- Confirmation that Product Task 163 behaviour remains unchanged.
- Confirmation that no pitch inference or assumed-treble extension was added.
- Known limitations.
- Suggested next task.
```
