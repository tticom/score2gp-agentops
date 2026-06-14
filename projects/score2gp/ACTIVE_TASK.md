## Current Active Task

## Product Task 150 — Validate read-only eighth-note candidate reporting across public fixtures

Status: ACTIVE

Owning repo: score2gp

Context:
Product Task 148 has only added a read-only candidate-composition boundary for eighth notes. Before semantic inference, we need a validation/reporting step that proves the new `eighth_note_candidate` behaves safely across the existing public fixtures and does not create unwanted candidates in non-eighth-note fixtures.

Goal:
Validate the newly added read-only `eighth_note_candidate` reporting across existing public fixtures and confirm it appears only where expected.

Scope:
- Work in `tticom/score2gp`.
- Use existing public fixtures only.
- Run generic `note-candidate-recognition` reporting across public generated staff fixtures.
- Confirm `eighth_note_candidate` appears in `generated_standard_staff_eighth_notes.pdf`.
- Confirm `eighth_note_candidate` does not appear in fixtures where only whole, half, quarter, sparse, or unrelated geometry is expected.
- Add or update tests only where they prove fixture-level reporting stability.
- Preserve all existing generic outputs.
- Preserve backward compatibility for `whole-note-recognition`.
- Produce a concise validation summary in the PR body.

Non-goals:
- Do not infer pitch.
- Do not infer playable rhythm or duration.
- Do not emit ScoreIR.
- Do not emit MusicXML.
- Do not emit Guitar Pro or GP output.
- Do not add OCR.
- Do not implement rests.
- Do not implement full notation recognition.
- Do not alter extraction heuristics.
- Do not alter staff-association heuristics.
- Do not change `eighth_note_candidate` composition logic unless a failing regression proves the current logic is unsafe. If that happens, stop and report instead of broadening scope.
- Do not add private fixtures, scratch outputs, logs, generated dumps, credentials, or unrelated artifacts.

Next Step:
Execute Product Task 150 in the `score2gp` repository.
