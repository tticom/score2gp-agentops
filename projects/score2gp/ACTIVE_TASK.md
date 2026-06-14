## Current Active Task

## Task 124 — Add read-only filled/stemmed notehead diagnostic support

Status: ACTIVE

Owning repo: score2gp

Context:
Product Task 122 identified that current read-only geometry diagnostics do not process filled noteheads. A safe read-only reporting boundary cannot be added until the foundational diagnostics explicitly support filled/stemmed notehead candidates.

Goal:
Add the smallest safe diagnostic support for filled/stemmed notehead-like candidates, if existing public/generated fixtures can support it. Keep the output strictly diagnostic and read-only.

Non-goals:
* Do not add pitch inference.
* Do not add staff-position inference.
* Do not add rhythm or playable-duration inference.
* Do not emit ScoreIR, MusicXML, GP output, OCR, rests, eighth-note recognition, or full notation events.
* Do not broaden into full notation recognition.

Next Step:
Execute Product Task 124 in the `score2gp` repository using the Codex-cleared PR readiness workflow.
