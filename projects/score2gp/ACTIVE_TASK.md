# Active Product Task

## Product Task 166 — Introduce deterministic read-only clef candidate evidence

### Scope
- Work in `tticom/score2gp`.
- Inspect existing staff, page, system, and recognition diagnostics before changing anything.
- Determine whether there is already deterministic treble-clef evidence available in the product data.
- If deterministic clef evidence exists, expose it as read-only candidate evidence in standard note-candidate recognition output (e.g., `clef_candidate` or similar).
- Associate clef evidence to page/system/staff only when the association is deterministic.
- Fail closed when clef evidence is missing, ambiguous, malformed, unsupported, or inferred only by guesswork.
- If no deterministic existing clef evidence is available, implement the smallest safe diagnostic/preparatory boundary and stop before guessing.
- Do not use `assume_treble_clef` as proof of visual clef evidence.
- Do not infer clef from pitch outcomes.
- Do not infer clef from note positions.
- Do not infer clef from ledger-line placement.

### Non-Goals
- Do not implement full clef recognition.
- Do not guess treble clef globally.
- Do not wire `map_clef_resolved_staff_pitch()` into the main pipeline.
- Do not implement pitch inference.
- Do not implement accidentals, key signatures, rhythm inference, or rests.
- Do not alter existing note-candidate extraction, ledger-line extraction, or ledger-line grouping heuristics (unless a blocker is reported).
- Do not emit ScoreIR, MusicXML, or Guitar Pro output.
- Do not commit private fixtures or sensitive data.
