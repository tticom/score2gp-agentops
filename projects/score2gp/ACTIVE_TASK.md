## Current Active Task

## Product Task 154 — Expose staff geometry in read-only recognition report payload

Status: ACTIVE

Owning repo: score2gp

Context:
Governance PR #164 authorised Product Task 152 for discovery. The discovery found that staff geometry exists internally but is discarded before the read-only recognition/report boundary. This blocks safe future staff-position mapping.

Goal:
Expose staff geometry alongside read-only recognition outcomes so future tasks can map note candidates to staff-line positions.

Scope:
- Work in `tticom/score2gp`.
- Modify the recognition/report payload so staff geometry is available to read-only consumers.
- Prefer a top-level `staff_geometry` array in the returned report payload, not entries inside `read_only_recognition_outcomes`, because staff geometry is context rather than a note candidate.
- Include only clean geometric fields:
  - `page_index`
  - `system_index`
  - `staff_index`
  - `bbox`
  - `line_y_coords`
  - `staff_space`, if already available from existing diagnostics without heuristic changes
- Preserve all existing `read_only_recognition_outcomes`.
- Preserve backward compatibility for `whole-note-recognition`.
- Add tests proving `staff_geometry` is exported for public fixtures.
- Add tests proving note candidates and staff geometry can be joined by `page_index`, `system_index`, and `staff_index`.

Non-goals:
- Do not implement pitch inference.
- Do not implement staff-position inference.
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
- Do not change eighth-note composition logic.
- Do not expose raw primitives, morphology dumps, clustering internals, or private diagnostic dumps.
- Do not commit private fixtures, scratch outputs, dumps, logs, credentials, or unrelated artifacts.

Next Step:
Execute Product Task 154 in the `score2gp` repository.
