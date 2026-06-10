# Raster Treble-Clef Diagnostic Consumer Boundary

## Verified Prerequisites
- Product PR #236 is merged, introducing `classify_raster_opening_symbol_candidate`.
- Governance PR #109 is merged, establishing the diagnostic classifier merge boundary.

## Purpose
This note defines the consumer contract for `raster_opening_symbol_classification`. It establishes how downstream diagnostic tooling and research may consume this field without silently crossing into semantic music recognition, vector/raster fusion, or `ScoreIR` production.

## Diagnostic Field Contract
The `raster_opening_symbol_classification` dictionary must contain:
- `kind`: Identifies the classifier (e.g., `"treble_clef_candidate_classifier"`).
- `label`: The assigned classification. Currently allowed labels are `"treble_clef_candidate"` and `"unknown"`.
- `reason`: Human-readable text explaining the label.
- `features`: Dictionary of extracted spatial heuristics (e.g., height-to-spacing ratio).

Any later addition to the allowed labels must be explicitly authorised by governance before consumers rely on them.

## Allowed Consumers
The field may be consumed by:
- Governance notes.
- Diagnostic reports.
- Read-only summary tooling.
- Research notes that explicitly preserve evidence caveats.
- Later product diagnostics **only if explicitly authorised** by a later implementation task.

## Allowed Uses
- Count candidate labels for diagnostics.
- Summarise which pages/staves have diagnostic candidates.
- Surface `unknown` rates and malformed-evidence rates.
- Compare candidate features for research.
- Identify fixtures or pages needing further diagnostic inspection.
- Inform later classifier or diagnostics design.

## Disallowed Uses
Consumers **must not**:
- Emit `ScoreIR`.
- Create clef objects.
- Infer pitch, rhythm, key signature, time signature, notes, rests, voices, or musical semantics.
- Decide that a staff is musically parsed.
- Fuse vector/raster evidence unless a later governance task defines precedence and fallback rules.
- Run or introduce OCR.
- Treat `"treble_clef_candidate"` as a confirmed treble clef.
- Suppress `"unknown"` cases to make results look better.
- Use synthetic or placeholder geometry to satisfy consumer expectations.

## Required Interpretation Rules
- `"treble_clef_candidate"` means only “diagnostic candidate matching current conservative spatial heuristics.”
- `"unknown"` is a first-class result, not a failure to hide.
- Staff-lines-only evidence must remain `"unknown"`.
- Malformed evidence must remain `"unknown"`.
- Missing candidate evidence must remain `"unknown"`.
- Consumers must preserve page/staff context when available.
- Consumers must preserve the distinction between evidence, candidate classification, semantic recognition, and `ScoreIR` production.

## Acceptance Criteria for Later Implementation
A later implementation task may be proposed only if it:
- Is read-only and diagnostic-only.
- Consumes existing diagnostic output without mutating musical models.
- Preserves `"unknown"` cases.
- Does not create `ScoreIR`.
- Does not create recognised clef objects.
- Does not infer pitch/key/time/rhythm/notes/rests/voices.
- Does not introduce OCR.
- Does not introduce vector/raster fusion.
- Uses real existing diagnostics or authorised fixtures.
- Includes tests proving no `ScoreIR` or semantic fields are emitted.
- Includes tests proving `"unknown"` is preserved and surfaced.

## Candidate Next Tasks
- `Task 57 — Implement read-only raster treble-clef diagnostics summary`
- `Task 57 alternative — Add governance-only diagnostics summary acceptance criteria before implementation`

## Recommended Next Task
The explicitly recommended next task is:
**Task 57 — Implement read-only raster treble-clef diagnostics summary**

Because this boundary note clearly defines the read-only consumer contract, it is now safe to authorise the implementation of a read-only diagnostics summary tool.

## Stop Conditions
Any implementation that attempts to consume this diagnostic field to build a semantic recogniser, emit `ScoreIR`, or fuse evidence prematurely must be blocked.
