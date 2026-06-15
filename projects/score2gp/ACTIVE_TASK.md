# Active Task

**Product Task 160 — Add explicit assumed-treble read-only pitch mapping for generated public fixtures**

## Goal
Add an explicit opt-in assumed-treble mode that maps existing `staff_position_index` values to read-only pitch names for natural notes within the standard five-line treble staff.

## Scope
* Work in `tticom/score2gp`.
* Add an explicitly named opt-in flag or parameter, such as `assume_treble_clef`.
* The mode must be disabled by default.
* When disabled, no pitch fields must be emitted.
* When enabled, map only in-staff `staff_position_index` values `0` through `8`.
* Use the mapping:
  * `0` = `F5`
  * `1` = `E5`
  * `2` = `D5`
  * `3` = `C5`
  * `4` = `B4`
  * `5` = `A4`
  * `6` = `G4`
  * `7` = `F4`
  * `8` = `E4`
* Add a clearly named read-only field such as `assumed_treble_pitch`.
* The field name must make the assumption explicit.
* Add CLI support to `scripts/note_candidate_recognition_report.py`, for example `--assume-treble-clef`.
* Add tests proving pitch fields are absent by default.
* Add tests proving pitch fields appear only when the explicit assumed-treble option is enabled.
* Add tests proving out-of-range staff positions fail closed and do not receive pitch fields.
* Add tests proving the exact mapping for generated public fixtures.
* Preserve existing `staff_position_index`.
* Preserve existing `staff_geometry`.
* Preserve all existing generic candidate outputs.
* Preserve backward compatibility for `whole-note-recognition`.

## Non-goals
* Do not implement generic pitch inference.
* Do not implement clef recognition.
* Do not infer clef from notation.
* Do not infer sounding pitch.
* Do not implement transposition.
* Do not implement ledger-line pitch mapping.
* Do not implement accidentals.
* Do not implement key signatures.
* Do not infer playable rhythm or duration.
* Do not emit ScoreIR.
* Do not emit MusicXML.
* Do not emit Guitar Pro or GP output.
* Do not add OCR.
* Do not implement rests.
* Do not change extraction heuristics.
* Do not change staff-association heuristics.
* Do not change eighth-note composition logic.
* Do not change staff-position inference logic unless a blocker is found; if so, stop and report.
* Do not expose raw primitives, morphology dumps, clustering internals, or private diagnostic dumps.
* Do not commit private fixtures, scratch outputs, dumps, logs, credentials, or unrelated artifacts.
