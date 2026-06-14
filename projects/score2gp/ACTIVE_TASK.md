## Current Active Task

## Task 126 — Add read-only quarter-note candidate reporting boundary

Status: ACTIVE

Owning repo: score2gp

Context:
Product Task 124 successfully added diagnostic support for `quarter_note_candidates`. The product now has the safe foundational evidence required to emit quarter-note candidate boundaries.

Goal:
Add a read-only quarter-note candidate reporting boundary to the product. Expose existing diagnostic `quarter_note_candidates` through the generic read-only `note-candidate-recognition` reporting path. Keep output as read-only diagnostic-derived candidate evidence. Add output only if it can be derived from the existing `quarter_note_candidates` diagnostics.

Non-goals:
* Do not add pitch inference.
* Do not add staff-position inference.
* Do not add rhythm or playable-duration inference.
* Do not emit ScoreIR, MusicXML, Guitar Pro or GP output, OCR, rests, eighth-note recognition, or full notation events.
* Do not broaden into full notation recognition.

Next Step:
Execute Product Task 126 in the `score2gp` repository using the Codex-cleared PR readiness workflow. Add tests proving quarter-note candidate reporting and preservation of whole/half-note reporting. Stop and report if the diagnostic field is unavailable or cannot safely support reporting.
