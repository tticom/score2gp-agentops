# Active Task

**Product Task 158 — Discover clef and pitch-mapping boundary for read-only candidates**

## Goal
Discover what explicit evidence, assumptions, and fixtures are required before read-only pitch inference can be safely implemented.

## Scope
* Work in `tticom/score2gp`.
* Discovery only.
* Inspect current read-only candidate outputs, `staff_position_index`, `staff_geometry`, fixtures, exporter code, and tests.
* Determine whether any clef evidence is available in the recognition/reporting layer.
* Determine whether treble clef is explicit, implicit, or absent in fixtures and code.
* Determine whether a future pitch task should use:
  * detected clef;
  * explicit fixture metadata;
  * a clearly named assumed-clef mode;
  * or no pitch mapping yet.
* Determine whether octave mapping can be defined safely from current staff-position indexes.
* Determine whether ledger-line notes are represented or must be deferred.
* Determine whether accidentals are represented or must be deferred.
* Determine whether current public fixtures are sufficient to prove natural treble-clef pitch mapping.
* Determine the smallest safe next product task.

## Non-goals
* Do not implement pitch inference.
* Do not infer pitch names.
* Do not infer octave names.
* Do not infer playable rhythm or duration.
* Do not emit ScoreIR.
* Do not emit MusicXML.
* Do not emit Guitar Pro or GP output.
* Do not add OCR.
* Do not implement rests.
* Do not implement accidentals.
* Do not implement ledger-line handling.
* Do not implement clef recognition.
* Do not change extraction heuristics.
* Do not change staff-association heuristics.
* Do not change eighth-note composition logic.
* Do not change staff-position inference logic.
* Do not expose raw primitives, morphology dumps, clustering internals, or private diagnostic dumps.
* Do not commit private fixtures, scratch outputs, dumps, logs, credentials, or unrelated artifacts.
