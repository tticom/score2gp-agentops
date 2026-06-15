## Current Active Task

## Product Task 156 — Infer read-only note candidate staff positions

Status: ACTIVE

Owning repo: score2gp

Goal:
Add read-only staff-position information to note candidates by comparing notehead geometry with exposed staff-line coordinates.

Scope:
- Work in `tticom/score2gp`.
- Use existing `staff_geometry.line_y_coords`.
- Use existing candidate `page_index`, `system_index`, and `staff_index` join keys.
- Infer relative staff position only.
- Add a read-only field such as `staff_position_index` or `staff_position` to note candidates where safe.
- Staff-position representation must be explicitly non-pitch:
  - no note names;
  - no octave names;
  - no clef assumptions.
- Prefer a deterministic integer index relative to staff lines/spaces.
- Handle whole, half, quarter, and eighth candidates.
- For eighth candidates, use the referenced quarter/notehead component rather than the union bbox where possible.
- Fail closed if a candidate cannot be safely mapped to staff geometry.
- Add tests proving staff-position mapping for public standard staff fixtures.
- Add tests proving unmappable or malformed candidates do not raise and do not receive unsafe positions.
- Preserve all existing generic candidate outputs.
- Preserve top-level `staff_geometry`.
- Preserve backward compatibility for `whole-note-recognition`.

Non-goals:
- Do not infer pitch names.
- Do not infer octave names.
- Do not infer playable rhythm or duration.
- Do not emit ScoreIR.
- Do not emit MusicXML.
- Do not emit Guitar Pro or GP output.
- Do not add OCR.
- Do not implement rests.
- Do not implement accidentals.
- Do not implement ledger-line handling.
- Do not implement clef recognition.
- Do not change extraction heuristics.
- Do not change staff-association heuristics.
- Do not change eighth-note composition logic unless a blocker is found; if so, stop and report.
- Do not expose raw primitives, morphology dumps, clustering internals, or private diagnostic dumps.
- Do not commit private fixtures, scratch outputs, dumps, logs, credentials, or unrelated artifacts.
