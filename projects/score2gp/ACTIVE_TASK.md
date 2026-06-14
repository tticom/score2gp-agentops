## Current Active Task

## Product Task 152 — Discover staff-position and pitch inference prerequisites

Status: ACTIVE

Owning repo: score2gp

Context:
The read-only candidate surface is now stable, but pitch inference is a semantic layer. Before implementation, we must discover and document the available evidence and boundary conditions for staff-position and pitch inference.

Goal:
Discover what evidence currently exists to support safe future staff-position and pitch inference for read-only note candidates.

Scope:
- Work in `tticom/score2gp`.
- Discovery only.
- Inspect existing staff geometry, staff-line diagnostics, note candidate bboxes, and fixture data.
- Determine whether notehead centre can be derived safely from existing candidates.
- Determine whether staff-line positions and staff spacing are available at the required boundary.
- Determine whether clef assumptions exist or must be explicitly introduced.
- Determine whether octave and ledger-line handling are in scope or must be deferred.
- Determine whether accidentals exist in current diagnostics or must be deferred.
- Determine which public fixtures are sufficient to prove staff-position mapping.
- Recommend the smallest safe next product task.

Non-goals:
- Do not implement pitch inference.
- Do not infer playable rhythm or duration.
- Do not emit ScoreIR.
- Do not emit MusicXML.
- Do not emit Guitar Pro or GP output.
- Do not add OCR.
- Do not implement rests.
- Do not implement accidentals.
- Do not implement ledger-line handling unless discovery proves it already exists and is safe.
- Do not change extraction heuristics.
- Do not change staff-association heuristics.
- Do not commit private fixtures, scratch outputs, dumps, logs, credentials, or unrelated artifacts.

Next Step:
Execute Product Task 152 in the `score2gp` repository.
