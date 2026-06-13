## Current Active Task

## Task 118 — Expose half-note candidate evidence in read-only recognition/reporting path

Status: ACTIVE

Owning repo: score2gp

Context:
Product Task 116 added a narrow read-only half-note candidate evidence boundary. Score2GP now has `whole_note_candidate` read-only recognition outcome support and `half_note_candidates` diagnostic candidate evidence support. The next small product step is to make half-note candidate evidence visible through a read-only recognition/reporting path where repo evidence supports it, without adding musical semantics.

Goal:
Expose half-note candidate evidence through the read-only recognition/reporting surface in a way that preserves whole-note behaviour, diagnostic/read-only boundaries, deterministic candidate IDs, JSON privacy boundaries, and existing CLI/script behaviour.

Non-goals:
Do not add pitch inference.
Do not add staff-position inference.
Do not add rhythm or playable duration.
Do not emit ScoreIR, MusicXML, GP output, OCR, or full notation events.
Do not broaden recognition beyond candidate evidence.

Next Step:
Execute Product Task 118 in the `score2gp` repository using the Codex-cleared PR readiness workflow.
