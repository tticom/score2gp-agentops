# Raster Opening-Symbol Diagnostics Consumption Boundary

## Verified product merge
Product PR #235 in `tticom/score2gp` (`feat(pdf): add raster treble clef staff diagnostics`) was merged at `2026-06-10T10:53:20Z` with merge commit `670eebbec023d321fada7d2dd897cc7c889e67e6`. This PR successfully introduced a raster-backed diagnostic path for simple PDF fixtures, detecting left-margin candidate bounds (`raster_opening_symbol_candidate`).

## Relationship to closed PR #105
Governance PR #105 reported that the vector-only diagnostics path was insufficient for raster/image-backed PDFs containing notation evidence. PR #105 is closed unmerged and must be treated solely as historical negative vector-path evidence. It must not override the new raster diagnostics capabilities provided by PR #235, nor does it represent the current capability boundary.

## What raster diagnostics now provide
The raster path reports:
* A `status` indicating successful extraction.
* A list of `staffs` (five-line groups), including their vertical bounds (`y_coords`) and `spacing`.
* A `raster_opening_symbol_candidate` indicating the exact bounding box, width, and height of connected dark regions in the left margin area of each staff.

Raster diagnostics are evidence only. `raster_opening_symbol_candidate` is not a recognised clef, but rather a candidate bound for downstream classification or analysis.

## Consumption boundary
The extracted `raster_opening_symbol_candidate` bounds may be consumed to design a later classifier boundary. Any downstream consumer must treat the bounds strictly as spatial/pixel evidence.

## Explicit non-semantics boundary
* No `ScoreIR` emission is authorised.
* No pitch, key signature, time signature, rhythm, notes, rests, or voice semantics can be inferred from `raster_opening_symbol_candidate`.
* No grouping beyond documented raster staff/opening-symbol evidence is authorised.

## Vector/raster evidence separation
Vector diagnostics and raster diagnostics are strictly separate evidence sources. Raster candidate bounds do not imply that corresponding vector curves/strokes exist, and vice versa. They must not be intermingled without explicit rules for fallback or precedence.

## Evidence and privacy rules
Private fixtures in PR #235 were intentionally tracked and authorised; this decision is recorded and need not be relitigated. Future PR bodies must explicitly state when private PDFs are intentionally tracked.
If evidence is unavailable for a given task, agents must stop and create a prerequisite diagnostics task rather than synthesize fake evidence, logs, debug dumps, or placeholder images.

## Blocked product work
Product recogniser implementation remains strictly blocked until a classifier boundary or implementation boundary is explicitly authorised via a governance PR.

## Candidate next tasks
* Preferred next task: `Task 53 — Define read-only treble-clef candidate classifier boundary`
* Implementation task only if later authorised: `Task 53 — Implement read-only treble-clef candidate classifier diagnostics`

## Acceptance criteria for any later classifier-boundary task
Any governance task authorising a classifier boundary must:
* Specify how to process the `raster_opening_symbol_candidate` bounds.
* Prohibit emitting full `ScoreIR` without further validation.
* Establish clear metrics/rules for confirming the candidate is a treble clef (e.g. geometric proportions).

## Stop conditions
Agents consuming this boundary must stop and report if:
* The evidence requires inferring full music semantics prematurely.
* Missing evidence triggers an impulse to synthesize fake candidate geometry or artifacts.
