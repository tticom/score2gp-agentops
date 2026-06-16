# Post-Task 166: Record Task 166 completion and authorise Task 167

## Product Task 166 Completion Summary
Product Task 166 has been verified as complete.

### Verified State
* **Product PR:** [https://github.com/tticom/score2gp/pull/286](https://github.com/tticom/score2gp/pull/286)
* **Title:** `feat(recognition): implement diagnostic boundary for clef evidence`
* **Merged At:** `2026-06-16T07:45:39Z`
* **Final Head SHA:** `2ebcb039d2ee861f6a85d6787f33d86ab4e30505`
* **Merge Commit:** `a121832025abacb968c23d33825894e588c242a3`

### Exact Changed Files
* `src/score2gp/whole_note_recogniser.py`
* `tests/test_note_candidate_recognition_report.py`

### Product Task 166 Outcome Summary
* Introduced a deterministic read-only clef candidate evidence boundary.
* Confirmed that no deterministic visual clef evidence currently exists in the standard product data flow.
* Confirmed existing raster diagnostics remain isolated and are not yet integrated into standard notation geometry.
* Added `extract_treble_clef_candidate_evidence(...)`.
  * It currently returns an empty list because no deterministic clef evidence exists in the standard geometry pipeline.
  * This prevents clef guessing.
* Added `map_treble_clef_candidates_to_read_only_outcomes(...)`.
  * It maps only valid future clef candidate evidence into read-only outcomes.
  * Output symbol type: `treble_clef_candidate`.
  * Source marker: `diagnostic_candidate_evidence`.
* Integrated the boundary into `run_recognition_on_file(...)`.
  * Since extraction currently returns no candidates, standard CLI runs do not emit clef candidates.
* `map_treble_clef_candidates_to_read_only_outcomes(...)` now fails closed for malformed or ambiguous evidence.
* It skips evidence when:
  * `candidate_id` is missing;
  * `candidate_id` is empty;
  * `candidate_id` is not a string;
  * `page_index` is missing or not an integer;
  * `system_index` is missing or not an integer;
  * `staff_index` is missing or not an integer;
  * `bbox` is missing;
  * `bbox` is malformed;
  * `bbox` is not exactly four values;
  * `bbox` contains non-numeric values;
  * `candidate_id` is duplicated.
* Duplicate candidate IDs are skipped deterministically using a `seen_ids` set.
* Added tests proving:
  * the clef evidence extractor fails closed and returns `[]`;
  * valid dummy treble clef evidence maps correctly;
  * missing `candidate_id` fails closed;
  * empty `candidate_id` fails closed;
  * missing page/system/staff indexes fail closed;
  * malformed non-integer page/system/staff indexes fail closed;
  * missing bbox fails closed;
  * malformed bbox fails closed;
  * wrong-length bbox fails closed;
  * non-numeric bbox fails closed;
  * duplicate candidate IDs do not produce ambiguous duplicate evidence.

### Boundary and Compatibility Preservation
* **Read-only validation:** Confirmed that Product Task 166 remained read-only/preparatory.
* **Extraction preservation:** Confirmed that existing note extraction and existing ledger-line extraction were preserved.
* **Suppression preservation:** Confirmed that duplicate beam/ledger suppression was preserved.
* **Position and pitch preservation:** Confirmed that existing `assumed_treble_pitch` behaviour was preserved. Confirmed that existing `staff_position_index` behaviour was preserved.
* **Grouping preservation:** Confirmed that existing `attached_ledger_line_candidate_ids` behaviour was preserved.
* **No feature creep:** Confirmed that no clef guessing was introduced. Confirmed that no visual clef recognition was introduced. Confirmed that `assume_treble_clef` was not used as visual clef evidence.
* **System compatibility:** Confirmed that whole-note recognition compatibility was preserved. Confirmed that existing `map_clef_resolved_staff_pitch(...)` behaviour was preserved.

### Validation Recorded in PR
**Commands run:**
```text
pytest tests/test_note_candidate_recognition_report.py tests/test_note_candidate_recognition_cli.py tests/test_whole_note_recognition_cli.py
```
**Result:** `40 tests passed`. `git diff --check` passed.

### Codex Disposition
* No PR comments were recorded on Product PR #286.
* No review threads were recorded on Product PR #286.

### Privacy/Artifact Hygiene
* Clean.
* No private fixtures, diagnostic dumps, scratch JSON, logs, credentials, screenshots, GP files, PDFs, images, or unrelated artifacts were committed.

### Known Limitations
* The standard geometry pipeline still does not expose deterministic visual clef evidence.
* Until a later authorised task introduces real deterministic clef evidence, the boundary safely returns no clef candidates during normal recognition.

---

## Authorisation for Product Task 167
Product Task 167 is authorised for implementation. Implementation must not begin until this governance PR is merged.

### Title: Product Task 167 — Bridge deterministic raster treble-clef diagnostics into read-only clef candidate evidence

### Context
You are the product implementation agent for `tticom/score2gp`.

This task must only start after the governance PR authorising Product Task 167 has been merged.

Recent completed product work:
- Product Task 165 added read-only preparatory helper `map_clef_resolved_staff_pitch(outcomes, explicit_clef)`.
- Product Task 166 added a read-only clef candidate evidence boundary:
  - `extract_treble_clef_candidate_evidence(...)`
  - `map_treble_clef_candidates_to_read_only_outcomes(...)`
  - output symbol type `treble_clef_candidate`
  - source marker `diagnostic_candidate_evidence`
- Product Task 166 confirmed no deterministic visual clef evidence currently exists in the standard product geometry pipeline.
- Product Task 166 confirmed existing raster diagnostics remain isolated and are not yet integrated into standard notation geometry.
- Product Task 166 did not guess clef context.
- Product Task 166 did not use `assume_treble_clef` as visual clef evidence.
- Product Task 166 did not wire `map_clef_resolved_staff_pitch(...)` into the main pipeline.

### Goal
Bridge existing deterministic raster treble-clef diagnostics into the read-only clef candidate evidence boundary introduced by Product Task 166, but only if deterministic evidence and staff association already exist.

This is still an evidence-capture task. It is not a pitch-inference task.

### Functional Requirements
- Inspect existing raster treble-clef diagnostics, staff diagnostics, page/system/staff geometry, and note-candidate recognition output before changing anything.
- Determine whether existing raster diagnostics contain deterministic treble-clef evidence that can be associated to a page/system/staff without guessing.
- If deterministic raster treble-clef evidence exists and can be associated to page/system/staff, bridge it into `extract_treble_clef_candidate_evidence(...)`.
- Output must use the existing read-only `treble_clef_candidate` shape through `map_treble_clef_candidates_to_read_only_outcomes(...)`.
- Candidate IDs must be deterministic.
- Page/system/staff association must be deterministic.
- Bbox values must be valid numeric four-value boxes.
- Source marker must distinguish raster-derived diagnostic evidence clearly, for example:
  - `raster_diagnostic_candidate_evidence`
  - or another clear project-consistent source value.
- If deterministic evidence does not exist, or association cannot be proven, do not fake candidates.
- If deterministic evidence does not exist, implement the smallest safe diagnostic/preparatory step that records the blocker in code/tests without changing production output semantics.
- Fail closed for missing, ambiguous, malformed, unsupported, or guessed evidence.
- Preserve existing note extraction.
- Preserve existing ledger-line extraction.
- Preserve duplicate beam/ledger suppression.
- Preserve existing `staff_position_index`.
- Preserve existing `attached_ledger_line_candidate_ids`.
- Preserve existing `assumed_treble_pitch`.
- Preserve existing `map_clef_resolved_staff_pitch(...)` behaviour.
- Preserve existing `map_treble_clef_candidates_to_read_only_outcomes(...)` fail-closed validation.
- Preserve whole-note recognition compatibility.

### Non-goals
- Do not implement new visual clef recognition.
- Do not guess treble clef globally.
- Do not use `assume_treble_clef` as visual clef evidence.
- Do not infer clef from pitch outcomes.
- Do not infer clef from note positions.
- Do not infer clef from ledger-line placement.
- Do not wire `map_clef_resolved_staff_pitch(...)` into the main pipeline unless deterministic explicit clef evidence is actually bridged and the task boundary clearly permits it. If unsure, do not wire it.
- Do not implement pitch inference.
- Do not implement accidentals.
- Do not implement key signatures.
- Do not implement rhythm inference.
- Do not emit ScoreIR.
- Do not emit MusicXML.
- Do not emit Guitar Pro or GP output.
- Do not implement OCR.
- Do not implement rests.
- Do not alter existing note-candidate extraction heuristics.
- Do not alter existing ledger-line extraction heuristics.
- Do not alter ledger-line grouping heuristics unless a blocker is reported.
- Do not commit private fixtures, diagnostic dumps, scratch JSON, logs, credentials, screenshots, GP files, PDFs, images, or unrelated artifacts.

### Required Pre-flight Checks
Run these before making changes:

```text
git status --short
git branch --show-current
git fetch --all --prune
git checkout main
git pull --ff-only
git log --oneline --decorate --graph --max-count=20
```

Also verify that the governance PR authorising Product Task 167 is merged before making product changes.

### Implementation Guidance
- Work in `tticom/score2gp`.
- Create a focused product branch from current `main`, for example:
  - `feature/raster-treble-clef-evidence-bridge-v0.1`
- Inspect existing recognition flow before editing.
- Likely relevant production file:
  - `src/score2gp/whole_note_recogniser.py`
- Likely relevant tests:
  - `tests/test_note_candidate_recognition_cli.py`
  - `tests/test_note_candidate_recognition_report.py`
  - `tests/test_whole_note_recognition_cli.py`
  - any existing raster treble-clef diagnostics tests, if present.
- Search for existing raster treble-clef diagnostic functions, fixture names, staff geometry mapping, and CLI/report output paths.
- Prefer a small adapter/helper that converts already-existing deterministic raster clef diagnostics into the Product Task 166 clef candidate evidence shape.
- Keep all changes read-only and output-only.
- Do not introduce a score model.

### Required Tests
Add or update tests proving:
- Existing deterministic raster treble-clef evidence maps into `treble_clef_candidate` only when evidence is explicit and valid.
- Missing raster clef evidence fails closed.
- Ambiguous raster clef evidence fails closed.
- Malformed raster clef evidence fails closed.
- Missing page/system/staff association fails closed.
- Clef evidence is associated only to the correct page/system/staff.
- `assume_treble_clef` does not create visual clef evidence.
- The existing Product Task 166 mapper still rejects malformed candidate evidence.
- Existing `assumed_treble_pitch` behaviour is unchanged.
- Existing `map_clef_resolved_staff_pitch(...)` behaviour is unchanged.
- Existing `staff_position_index` behaviour is unchanged.
- Existing `attached_ledger_line_candidate_ids` behaviour is unchanged.
- Existing Task 162 ledger-line extraction and duplicate beam/ledger suppression remain unchanged.
- Existing Task 164 ledger-line grouping remains unchanged.
- Whole-note recognition compatibility remains unchanged.

If deterministic raster evidence cannot be bridged:
- Add or update tests proving the boundary fails closed.
- Add or update a small diagnostic/preparatory helper only if it materially reduces uncertainty for the next task.
- Report the blocker clearly in the PR body.

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
- The task does not guess clef context.
- Raster-derived clef evidence is bridged only where evidence is explicit and deterministic.
- Missing, ambiguous, or malformed evidence fails closed.
- `assume_treble_clef` is not treated as visual clef evidence.
- Existing `map_treble_clef_candidates_to_read_only_outcomes(...)` fail-closed behaviour is preserved.
- Existing `assumed_treble_pitch` behaviour is preserved.
- Existing `map_clef_resolved_staff_pitch(...)` behaviour is preserved.
- Existing `staff_position_index` behaviour is preserved.
- Existing `attached_ledger_line_candidate_ids` behaviour is preserved.
- Existing note extraction is preserved.
- Existing ledger-line extraction is preserved.
- Existing duplicate beam/ledger suppression is preserved.
- Whole-note recognition compatibility is preserved.
- Focused tests pass.
- Hygiene checks pass.
- PR body records exact commands, results, files changed, branch name, full head SHA, and known limitations.

### Stop Conditions
Stop and report instead of continuing if:
- Governance authorisation for Product Task 167 is not merged.
- Existing deterministic raster clef evidence cannot be found.
- Raster clef evidence exists but cannot be deterministically associated to page/system/staff.
- Existing tests fail before your changes in a way that prevents clean attribution.
- Correct implementation requires new visual clef recognition.
- Correct implementation requires pitch inference.
- Correct implementation requires accidentals, key signatures, rhythm inference, ScoreIR, MusicXML, GP output, OCR, or rests.
- Required evidence is ambiguous or missing.
- You would need to commit private fixtures, diagnostic dumps, scratch JSON, logs, credentials, screenshots, GP files, PDFs, images, or unrelated artifacts.
- You cannot produce a small, reviewable increment.

### Commit and PR Requirements
- Commit only intentional product files.
- Push the feature branch.
- Open a product PR against `main`.
- The PR body must include:
  - Product Task 167 summary.
  - Governance PR verification result.
  - Exact files changed.
  - Output/evidence field or source marker chosen and why, if any.
  - Validation commands and results.
  - Privacy/artifact hygiene result.
  - Confirmation that Task 162 behaviour remains unchanged.
  - Confirmation that Task 164 behaviour remains unchanged.
  - Confirmation that Product Task 165 helper behaviour remains unchanged.
  - Confirmation that Product Task 166 clef evidence boundary remains unchanged or is safely extended.
  - Confirmation that no clef guessing was introduced.
  - Known limitations.

### Reporting Format
Return:
- Branch name.
- Product PR link.
- Full head SHA.
- Exact files changed.
- Summary of implementation or blocker found.
- Output/evidence field or source marker chosen and why, if any.
- Validation commands and results.
- Privacy/artifact hygiene result.
- Confirmation that Task 162 behaviour remains unchanged.
- Confirmation that Task 164 behaviour remains unchanged.
- Confirmation that Product Task 165 helper behaviour remains unchanged.
- Confirmation that Product Task 166 boundary behaviour remains unchanged or is safely extended.
- Confirmation that no clef guessing was introduced.
- Known limitations.
- Suggested next task.
