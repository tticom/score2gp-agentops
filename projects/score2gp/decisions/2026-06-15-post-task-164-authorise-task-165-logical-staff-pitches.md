# Post-Task 164: Record Task 164 completion and authorise Task 165

## Product Task 164 Completion Summary
Product Task 164 has been verified as complete.

### Verified State
* **Product PR:** [https://github.com/tticom/score2gp/pull/284](https://github.com/tticom/score2gp/pull/284)
* **Title:** `feat(recognition): add ledger-line grouping to note candidates`
* **Merged At:** `2026-06-15T21:25:45Z`
* **Final Head SHA:** `16b7a8b85d526ade432f22af093be6f69d7e32d5`
* **Merge Commit:** `66cfdae537dd60d43260c63c236bfe1ea64792e7`

### Exact Changed Files
* `src/score2gp/whole_note_recogniser.py`
* `tests/test_note_candidate_recognition_cli.py`
* `tests/test_note_candidate_recognition_report.py`

### Product Task 164 Outcome Summary
* Added read-only ledger-line grouping between valid note candidates and valid `ledger_line_candidate` objects.
* Added `map_ledger_lines_to_note_candidates()`.
* Added output field `attached_ledger_line_candidate_ids`.
* The field stores references to existing ledger-line candidate IDs, not embedded duplicate ledger-line objects.
* Grouping runs after `staff_position_index` exists for both note candidates and ledger-line candidates.
* Grouping is gated by geometry and staff-position logic.
* Notes inside the standard staff range `0..8` do not receive ledger-line attachments.
* Notes above the staff only attach above-staff ledger lines with negative indexes that logically support the note position.
* Notes below the staff only attach below-staff ledger lines with indexes greater than `8` that logically support the note position.
* The helper fails closed for malformed or missing evidence.
* Guards include integer-only staff positions, four-value numeric bbox validation, required staff association, required ledger `candidate_id`, and safe handling for missing eighth-note component lookup.
* Positive grouping tests assert exact ledger-line candidate IDs.
* Edge-case tests cover in-staff notes, missing staff indices, malformed geometry, unrelated pages, no horizontal overlap, below/above logical mismatch, duplicate plausible ledger lines, missing eighth-note component lookup, and positive eighth-note grouping via valid `quarter_component_id`.

### Boundary and Compatibility Preservation
* **Read-only validation:** Confirmed that Product Task 164 remained read-only.
* **Extraction preservation:** Confirmed that existing note extraction and existing ledger-line extraction were preserved.
* **Suppression preservation:** Confirmed that duplicate beam/ledger suppression was preserved.
* **Position and pitch preservation:** Confirmed that existing `staff_position_index` and `assumed_treble_pitch` behaviour were preserved.
* **No feature creep:** Confirmed that no pitch inference or assumed-treble extension was added.
* **System compatibility:** Confirmed that whole-note recognition compatibility was preserved.

### Validation Recorded in PR
**Commands run:**
```text
pytest tests/test_note_candidate_recognition_report.py tests/test_note_candidate_recognition_cli.py tests/test_whole_note_recognition_cli.py
git diff --check
git diff --stat
git status --short
git status --ignored
```
**Result:** `36 passed in 12.22s`. All git checks clean.

### Codex Disposition
* Codex raised a review thread about validating malformed `staff_position_index` before range comparisons.
* The product agent replied directly to the thread explaining the explicit `type(pos) is int` fix.
* The thread was resolved before merge.

### Privacy/Artifact Hygiene
* No private fixtures or unrelated artifacts were added.
* `git ls-files` matched only pre-existing public JSON files and diagnostic fixtures.
* No new diagnostic dumps, logs, credentials, screenshots, GP files, private fixtures, or untracked payloads were added.

---

## Authorisation for Product Task 165
Product Task 165 is authorised for implementation. Implementation must not begin until this governance PR is merged.

### Title: Product Task 165 — Map logical staff pitches using clef and ledger-line grouping

### Context
You are the product implementation agent for `tticom/score2gp`.

This task must only start after the governance PR authorising Product Task 165 has been merged.

Recent completed product work:
* Product Task 163 added read-only `staff_position_index` to valid `ledger_line_candidate` objects.
* Product Task 164 added read-only grouping between valid note candidates and valid `ledger_line_candidate` objects.
* Product Task 164 added `attached_ledger_line_candidate_ids` to note candidates where ledger-line support is proven.
* Product Task 164 preserved note extraction, ledger-line extraction, duplicate beam/ledger suppression, `staff_position_index`, and `assumed_treble_pitch`.
* Product Task 164 did not implement pitch inference.

Important boundary:
This task may map logical staff pitches only for candidates where clef context is explicit, deterministic, and already available through authorised evidence. If clef context is not available in the product output, implement the smallest safe read-only preparatory step instead and stop before guessing.

### Goal
Add deterministic, read-only logical pitch mapping for note candidates using:
* existing `staff_position_index`;
* ledger-line grouping from `attached_ledger_line_candidate_ids`;
* explicit clef context, if available.

If explicit clef context is not available, stop and report the blocker. Do not guess treble clef globally unless an existing, authorised `assume_treble_clef` pathway already applies to the same output path and is explicitly preserved.

Candidate note types in scope:
* `whole_note_candidate`
* `half_note_candidate`
* `quarter_note_candidate`
* `eighth_note_candidate`

### Functional Requirements
* Inspect existing `assumed_treble_pitch` behaviour before changing anything.
* Preserve existing `assumed_treble_pitch` semantics.
* Do not replace `assumed_treble_pitch` unless explicitly authorised.
* Add a new read-only field only if it is semantically distinct and evidence-backed.
* The new field name must clearly distinguish deterministic logical pitch mapping from assumptions, for example: `logical_staff_pitch` or `clef_resolved_staff_pitch`.
* Only assign deterministic logical pitch when required evidence is present.
* Use `staff_position_index` as the vertical pitch coordinate.
* Use `attached_ledger_line_candidate_ids` only as supporting evidence for out-of-staff notes, not as an independent pitch source.
* In-staff notes may be pitch-mapped only when clef context is explicit and authorised.
* Out-of-staff notes may be pitch-mapped only when clef context is explicit and the required ledger-line support is present and unambiguous.
* Fail closed if clef context is missing, ambiguous, malformed, unsupported, or inferred only by guesswork.
* Fail closed if staff position is missing or malformed.
* Fail closed if required ledger-line support for out-of-staff notes is missing or ambiguous.
* Preserve existing note extraction.
* Preserve existing ledger-line extraction.
* Preserve duplicate beam/ledger suppression.
* Preserve existing `staff_position_index`.
* Preserve existing `attached_ledger_line_candidate_ids`.
* Preserve existing `assumed_treble_pitch`.
* Preserve whole-note recognition compatibility.

### Non-goals
* Do not implement clef recognition.
* Do not infer clef from visual symbols unless that has already been separately authorised.
* Do not implement accidentals.
* Do not implement key signatures.
* Do not implement rhythm inference.
* Do not emit ScoreIR.
* Do not emit MusicXML.
* Do not emit Guitar Pro or GP output.
* Do not implement OCR.
* Do not implement rests.
* Do not alter existing note-candidate extraction heuristics.
* Do not alter existing ledger-line extraction heuristics.
* Do not alter ledger-line grouping heuristics unless a blocker is reported.
* Do not commit private fixtures, diagnostic dumps, scratch JSON, logs, credentials, screenshots, GP files, PDFs, images, or unrelated artifacts.

### Required Pre-flight Checks
```text
git status --short
git branch --show-current
git fetch --all --prune
git checkout main
git pull --ff-only
git log --oneline --decorate --graph --max-count=20
```

Also verify that the governance PR authorising Product Task 165 is merged before making product changes.

### Implementation Guidance
* Work in `tticom/score2gp`.
* Create a focused product branch from current `main`, for example: `feature/logical-staff-pitch-mapping-v0.1`
* Inspect existing recognition flow before editing.
* Likely relevant production file: `src/score2gp/whole_note_recogniser.py`
* Likely relevant tests:
  * `tests/test_note_candidate_recognition_cli.py`
  * `tests/test_note_candidate_recognition_report.py`
  * `tests/test_whole_note_recognition_cli.py`
* First determine whether explicit clef context already exists in output data.
* If no explicit clef context exists, do not invent it.
* If the only available pitch path is `assume_treble_clef`, keep any new mapping clearly labelled as assumption-based or do not add it.
* Prefer a small helper that maps staff positions to pitch names only under an explicit clef policy.
* Keep all changes read-only and output-only.
* Do not introduce a score model yet.

### Required Tests
Add or update tests proving:
* Deterministic logical pitch mapping works only when clef context is explicit and valid.
* Missing clef context fails closed.
* Ambiguous clef context fails closed.
* Malformed staff position fails closed.
* In-staff notes map correctly only under valid clef context.
* Out-of-staff notes map correctly only when valid ledger-line grouping exists.
* Out-of-staff notes without required ledger-line grouping fail closed.
* Existing `assumed_treble_pitch` behaviour is unchanged.
* Existing `staff_position_index` behaviour is unchanged.
* Existing `attached_ledger_line_candidate_ids` behaviour is unchanged.
* Existing Task 162 ledger-line extraction and duplicate beam/ledger suppression remain unchanged.
* Existing Task 164 ledger-line grouping remains unchanged.
* Whole-note recognition compatibility remains unchanged.

### Validation
Run focused tests covering note-candidate reporting, CLI output, and whole-note compatibility. At minimum:
```text
pytest tests/test_note_candidate_recognition_report.py tests/test_note_candidate_recognition_cli.py tests/test_whole_note_recognition_cli.py
git diff --check
git diff --stat
git status --short
git status --ignored
git ls-files | grep -Ei "(private|scratch|dump|log|\.pdf$|\.gp$|\.png$|\.jpg$|\.jpeg$|\.json$)" || true
```

If tracked public fixture JSON files appear in `git ls-files`, explain whether they are pre-existing and whether this task changed them. Do not add new private or unrelated artifacts.

### Acceptance Criteria
* The task does not guess clef context.
* Pitch mapping is added only where evidence is explicit and deterministic.
* Missing, ambiguous, or malformed evidence fails closed.
* Existing `assumed_treble_pitch` behaviour is preserved.
* Existing `staff_position_index` behaviour is preserved.
* Existing `attached_ledger_line_candidate_ids` behaviour is preserved.
* Existing note extraction is preserved.
* Existing ledger-line extraction is preserved.
* Existing duplicate beam/ledger suppression is preserved.
* Whole-note recognition compatibility is preserved.
* Focused tests pass.
* Hygiene checks pass.
* PR body records exact commands, results, files changed, branch name, full head SHA, and known limitations.

### Stop Conditions
Stop and report instead of continuing if:
* Governance authorisation for Product Task 165 is not merged.
* There is no explicit clef context available and pitch mapping would require guessing.
* Existing tests fail before your changes in a way that prevents clean attribution.
* Correct implementation requires clef recognition.
* Correct implementation requires accidentals, key signatures, rhythm inference, ScoreIR, MusicXML, GP output, OCR, or rests.
* Required evidence is ambiguous or missing.
* You would need to commit private fixtures, diagnostic dumps, scratch JSON, logs, credentials, screenshots, GP files, PDFs, images, or unrelated artifacts.
* You cannot produce a small, reviewable increment.

### Reporting Format
Return:
* Branch name.
* Product PR link.
* Full head SHA.
* Exact files changed.
* Summary of implementation or blocker found.
* Output field name chosen and why, if any.
* Validation commands and results.
* Privacy/artifact hygiene result.
* Confirmation that Task 162 behaviour remains unchanged.
* Confirmation that Task 164 behaviour remains unchanged.
* Confirmation that no clef guessing was introduced.
* Known limitations.
* Suggested next task.
