# Active Product Task

## Product Task 167 — Bridge deterministic raster treble-clef diagnostics into read-only clef candidate evidence

### Scope
- Work in `tticom/score2gp`.
- Inspect existing raster treble-clef diagnostics, staff diagnostics, page/system/staff geometry, and note-candidate recognition output before changing anything.
- Determine whether existing raster diagnostics contain deterministic treble-clef evidence that can be associated to a page/system/staff without guessing.
- If deterministic raster treble-clef evidence exists and can be associated to page/system/staff, bridge it into `extract_treble_clef_candidate_evidence(...)`.
- Output must use the existing read-only `treble_clef_candidate` shape through `map_treble_clef_candidates_to_read_only_outcomes(...)`.
- Source marker must distinguish raster-derived diagnostic evidence clearly, for example: `raster_diagnostic_candidate_evidence`.
- If deterministic evidence does not exist, or association cannot be proven, do not fake candidates. Instead, implement the smallest safe diagnostic/preparatory step that records the blocker in code/tests without changing production output semantics.
- Fail closed for missing, ambiguous, malformed, unsupported, or guessed evidence.

### Non-Goals
- Do not implement new visual clef recognition.
- Do not guess treble clef globally.
- Do not use `assume_treble_clef` as visual clef evidence.
- Do not infer clef from pitch outcomes.
- Do not infer clef from note positions.
- Do not infer clef from ledger-line placement.
- Do not wire `map_clef_resolved_staff_pitch(...)` into the main pipeline unless deterministic explicit clef evidence is actually bridged and the task boundary clearly permits it.
- Do not implement pitch inference, accidentals, key signatures, rhythm inference, or rests.
- Do not alter existing note-candidate extraction, ledger-line extraction, or ledger-line grouping heuristics.
- Do not emit ScoreIR, MusicXML, or Guitar Pro output.
- Do not commit private fixtures or sensitive data.
