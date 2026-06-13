## Current Active Task

## Task 116 — Add read-only half-note candidate evidence boundary

Status: ACTIVE

Owning repo: score2gp

Context:
Product Task 113 consolidated whole-note candidate evidence shaping so diagnostics and whole-note recognition consume the same safe, read-only candidate evidence structure. Score2GP currently exposes `whole_note_candidate` recognition outcomes only. The next step toward broader notation recognition is to introduce a narrow, read-only candidate-evidence boundary for half-note-like open noteheads with stems, while keeping whole-note candidate behaviour stable.

Goal:
Add or expose a read-only half-note candidate evidence boundary that can distinguish half-note-like candidates from whole-note candidates where existing diagnostics and fixtures support it. Preserve existing whole-note recognition outcomes, CLI/script behaviour, JSON privacy boundaries, and diagnostic/read-only constraints.

Non-goals:
Do not add full half-note musical recognition.
Do not infer pitch, staff position, rhythm, or playable duration.
Do not emit ScoreIR, MusicXML, GP output, or full notation events.
Do not add OCR.
Do not broaden recognition beyond candidate evidence.

Next Step:
Execute Product Task 116 in the `score2gp` repository using the Codex-cleared PR readiness workflow.
