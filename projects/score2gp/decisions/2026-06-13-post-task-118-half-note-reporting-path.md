# Decision: Post-Task 118, Half-Note Candidate Reporting Path

## Context
Product Task 118 was completed by Product PR #266.
Product PR #266 exposed `half_note_candidate` read-only recognition output alongside the existing `whole_note_candidate` recognition output.
Current capability now includes `whole_note_candidate` and `half_note_candidate` read-only outcomes.
The current `whole-note-recognition` interface name is now too narrow because the output includes more than whole-note candidates.

## Codex Comment Disposition
- Product PR #266 comments/review threads:
  - Disposition: none found at post-merge verification.

## Next Action
Product Task 120 is authorised as a compatibility-preserving generic note-candidate reporting interface task.

## Scope & Constraints
- Product Task 120 must preserve existing CLI/script behaviour.
- Product Task 120 must not add new note types or musical semantics.
- Product Task 120 must not add pitch, staff position, rhythm/playable duration, ScoreIR, MusicXML, GP output, OCR, or full notation recognition.
