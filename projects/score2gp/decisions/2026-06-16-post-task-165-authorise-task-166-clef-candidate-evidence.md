# Post-Task 165: Record Task 165 completion and authorise Task 166

## Product Task 165 Completion Summary
Product Task 165 has been verified as complete.

### Verified State
* **Product PR:** [https://github.com/tticom/score2gp/pull/285](https://github.com/tticom/score2gp/pull/285)
* **Title:** `feat(recognition): add clef-resolved logical staff pitch mapping`
* **Merged At:** `2026-06-16T06:03:47Z`
* **Final Head SHA:** `30a2c87444c242fcb45d079bcf077af04b428ab8`
* **Merge Commit:** `707c93442955cd20262f377a5f202ec84dd4f53a`

### Exact Changed Files
* `src/score2gp/whole_note_recogniser.py`
* `tests/test_note_candidate_recognition_report.py`

### Product Task 165 Outcome Summary
* Added a read-only preparatory helper: `map_clef_resolved_staff_pitch(outcomes, explicit_clef)`.
* Added the output field name `clef_resolved_staff_pitch`.
* The field name distinguishes deterministic clef-backed pitch mapping from existing assumption-based `assumed_treble_pitch`.
* Confirmed no explicit clef context currently exists in standard product output evidence.
* The helper is not wired into the main pipeline path, so regular CLI runs do not guess clef or emit clef-resolved pitches by default.
* The helper requires explicit clef policy and currently returns early unless `explicit_clef == "treble"`.
* The helper maps in-staff notes and out-of-staff notes only under explicit treble policy.
* Out-of-staff notes enforce exact ledger-line support using `attached_ledger_line_candidate_ids`.
* The zero-ledger ambiguity for out-of-staff adjacent positions such as `staff_position_index == -1` and `staff_position_index == 9` was fixed.
* Adjacent out-of-staff positions requiring zero ledger lines now map only when `attached_ledger_line_candidate_ids` is absent or an empty list.
* Adjacent out-of-staff positions fail closed when `attached_ledger_line_candidate_ids` is malformed or contains spurious IDs.
* In-staff notes `0..8` bypass ledger-line validation.
* The helper fails closed for missing, ambiguous, malformed, or unsupported evidence.
* No clef recognition was added.
* No visual clef inference was added.
* No clef guessing was introduced.
* No accidentals, key signatures, rhythm inference, ScoreIR, MusicXML, Guitar Pro output, OCR, or rests were added.

### Boundary and Compatibility Preservation
* **Read-only validation:** Confirmed that Product Task 165 remained read-only/preparatory.
* **Extraction preservation:** Confirmed that existing note extraction and existing ledger-line extraction were preserved.
* **Suppression preservation:** Confirmed that duplicate beam/ledger suppression was preserved.
* **Position and pitch preservation:** Confirmed that existing `assumed_treble_pitch` behaviour was preserved. Confirmed that existing `staff_position_index` behaviour was preserved.
* **Grouping preservation:** Confirmed that existing `attached_ledger_line_candidate_ids` behaviour was preserved.
* **No feature creep:** Confirmed that no clef guessing was introduced. Confirmed that no visual clef recognition was introduced. Confirmed that `map_clef_resolved_staff_pitch()` is not wired into the main pipeline without explicit clef context.
* **System compatibility:** Confirmed that whole-note recognition compatibility was preserved.

### Validation Recorded in PR
**Commands run:**
```text
.venv/bin/pytest tests/test_note_candidate_recognition_report.py tests/test_note_candidate_recognition_cli.py tests/test_whole_note_recognition_cli.py
```
**Result:** `37 passed`. `git diff --check` passed after whitespace cleanup.

### Codex Disposition
* Codex raised an inline review thread titled `Enforce zero-ledger cases too`.
* The issue concerned out-of-staff positions `-1` and `9`, where zero ledger lines are required but spurious `attached_ledger_line_candidate_ids` could previously be ignored.
* The product agent fixed the issue.
* A direct inline reply was added to the Codex review thread explaining the zero-ledger fix.
* The inline review thread `PRRT_kwDOShNpkc6JyGwP` was verified resolved before merge.

### Privacy/Artifact Hygiene
* No private fixtures or unrelated artifacts were added.
* Privacy/artifact hygiene was reported clean.

---

## Authorisation for Product Task 166
Product Task 166 is authorised for implementation. Implementation must not begin until this governance PR is merged.

### Title: Product Task 166 — Introduce deterministic read-only clef candidate evidence

### Context
You are the product implementation agent for `tticom/score2gp`.

This task must only start after the governance PR authorising Product Task 166 has been merged.

Recent completed product work:
* Product Task 164 added read-only grouping between valid note candidates and valid `ledger_line_candidate` objects using `attached_ledger_line_candidate_ids`.
* Product Task 165 added a read-only preparatory helper `map_clef_resolved_staff_pitch(outcomes, explicit_clef)`.
* Product Task 165 did not wire clef-resolved pitch mapping into the main pipeline because explicit clef context is not yet available in standard product outcomes.
* Product Task 165 confirmed that no clef guessing should occur.
* Existing `assumed_treble_pitch`, `staff_position_index`, and `attached_ledger_line_candidate_ids` behaviours must remain preserved.

### Goal
Introduce deterministic read-only clef candidate evidence into the note-candidate recognition output, so later tasks can connect explicit clef policy to `map_clef_resolved_staff_pitch()` without guessing.

This task is about evidence capture only. It is not about pitch inference.

Candidate clef evidence in scope:
* Read-only candidate evidence for treble clef only if deterministic existing evidence is already available.
* If no deterministic existing clef evidence is available, implement the smallest safe diagnostic/preparatory boundary and stop before guessing.

### Functional Requirements
* Inspect existing staff, page, system, and recognition diagnostics before changing anything.
* Determine whether there is already deterministic treble-clef evidence available in the product data.
* If deterministic clef evidence exists, expose it as read-only candidate evidence in standard note-candidate recognition output.
* Use a field name that is clearly evidence-based, for example: `clef_candidate`, `treble_clef_candidate`, `explicit_clef_evidence`, or another clear project-consistent name.
* The field must not imply successful full clef recognition unless that is actually proven.
* Associate clef evidence to page/system/staff only when the association is deterministic.
* Fail closed when clef evidence is missing, ambiguous, malformed, unsupported, or inferred only by guesswork.
* Do not use `assume_treble_clef` as proof of visual clef evidence.
* Do not infer clef from pitch outcomes.
* Do not infer clef from note positions.
* Do not infer clef from ledger-line placement.
* Preserve existing note extraction.
* Preserve existing ledger-line extraction.
* Preserve duplicate beam/ledger suppression.
* Preserve existing `staff_position_index`.
* Preserve existing `attached_ledger_line_candidate_ids`.
* Preserve existing `assumed_treble_pitch`.
* Preserve existing `map_clef_resolved_staff_pitch()` behaviour.
* Preserve whole-note recognition compatibility.

### Non-goals
* Do not implement full clef recognition.
* Do not guess treble clef globally.
* Do not wire `map_clef_resolved_staff_pitch()` into the main pipeline.
* Do not implement pitch inference.
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

Also verify that the governance PR authorising Product Task 166 is merged before making product changes.

### Implementation Guidance
* Work in `tticom/score2gp`.
* Create a focused product branch from current `main`, for example: `feature/read-only-clef-candidate-evidence-v0.1`
* Inspect existing recognition flow before editing.
* Likely relevant production file: `src/score2gp/whole_note_recogniser.py`
* Likely relevant tests:
  * `tests/test_note_candidate_recognition_cli.py`
  * `tests/test_note_candidate_recognition_report.py`
  * `tests/test_whole_note_recognition_cli.py`
* Search for any existing clef diagnostics, staff diagnostics, or classifier outputs already available in public test paths.
* If evidence is not deterministic enough, do not fake a clef candidate. Instead, add a clearly named helper or diagnostic boundary that reports the blocker safely and is covered by tests.
* Keep all changes read-only and output-only.
* Do not introduce a score model yet.

### Required Tests
Add or update tests proving:
* Deterministic clef evidence is emitted only when evidence is explicit and valid.
* Missing clef evidence fails closed.
* Ambiguous clef evidence fails closed.
* Malformed clef evidence fails closed.
* Clef evidence is associated only to the correct page/system/staff.
* `assume_treble_clef` does not create visual clef evidence.
* Existing `assumed_treble_pitch` behaviour is unchanged.
* Existing `map_clef_resolved_staff_pitch()` behaviour is unchanged.
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
* Clef evidence is added only where evidence is explicit and deterministic.
* Missing, ambiguous, or malformed evidence fails closed.
* `assume_treble_clef` is not treated as visual clef evidence.
* Existing `assumed_treble_pitch` behaviour is preserved.
* Existing `map_clef_resolved_staff_pitch()` behaviour is preserved.
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
* Governance authorisation for Product Task 166 is not merged.
* There is no deterministic clef evidence available and exposing a clef candidate would require guessing.
* Existing tests fail before your changes in a way that prevents clean attribution.
* Correct implementation requires visual clef recognition beyond already available deterministic evidence.
* Correct implementation requires pitch inference.
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
* Output/evidence field name chosen and why, if any.
* Validation commands and results.
* Privacy/artifact hygiene result.
* Confirmation that Task 162 behaviour remains unchanged.
* Confirmation that Task 164 behaviour remains unchanged.
* Confirmation that Product Task 165 helper behaviour remains unchanged.
* Confirmation that no clef guessing was introduced.
* Known limitations.
* Suggested next task.
