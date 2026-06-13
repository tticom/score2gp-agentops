## Current Active Task

## Task 120 — Add generic read-only note-candidate reporting CLI/script alias

Status: ACTIVE

Owning repo: score2gp

Context:
Product Task 118 exposed half-note candidate evidence through the read-only recognition/reporting path. Score2GP now emits both `whole_note_candidate` and `half_note_candidate` outcomes, but the current CLI/reporting surface is still named around whole-note recognition. Before adding more notehead families, the reporting interface should be made honest and generic while preserving backwards compatibility.

Goal:
Add a generic read-only note-candidate reporting entry point, such as a CLI command and/or script alias, that exposes the existing candidate-evidence outcomes without changing recognition semantics. Preserve the existing `whole-note-recognition` command/script behaviour as a compatibility alias.

Non-goals:
Do not add new note types.
Do not add pitch inference.
Do not add staff-position inference.
Do not add rhythm or playable duration.
Do not emit ScoreIR, MusicXML, GP output, OCR, or full notation events.
Do not remove or break the existing `whole-note-recognition` command.
Do not broaden recognition beyond existing candidate evidence.

Next Step:
Execute Product Task 120 in the `score2gp` repository using the Codex-cleared PR readiness workflow.
