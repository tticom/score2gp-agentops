## Current Active Task

## Task 122 — Add read-only quarter-note candidate evidence boundary

Status: ACTIVE

Owning repo: score2gp

Context:
Product Task 120 added a generic `note-candidate-recognition` CLI and script alias. Score2GP now exposes `whole_note_candidate` and `half_note_candidate` evidence cleanly.

Goal:
Add or expose a narrow read-only candidate-evidence boundary for quarter-note-like filled noteheads/stemmed candidates only if safe existing diagnostics and fixtures support it. Stop and report if safe existing evidence or fixtures do not support it.

Non-goals:
* Do not add pitch inference.
* Do not add staff-position inference.
* Do not add rhythm or playable-duration inference.
* Do not emit ScoreIR, MusicXML, GP output, OCR, rests, eighth-note recognition, or full notation events.
* Do not broaden recognition beyond candidate evidence.

Next Step:
Execute Product Task 122 in the `score2gp` repository using the Codex-cleared PR readiness workflow.
