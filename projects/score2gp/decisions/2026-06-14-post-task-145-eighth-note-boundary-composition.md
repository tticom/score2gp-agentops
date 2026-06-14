# Decision: Authorise Eighth-Note Boundary Composition (Post Task 145)

## Context

Product Task 145 successfully added generated public fixture evidence (`generated_standard_staff_eighth_notes.pdf`) that emits `quarter_note_candidate`, `flag_candidate`, and `beam_candidate` evidence, all perfectly joined with explicit bounds (`page_index`, `system_index`, `staff_index`, `bbox`).

*   Product PR #275 Final head SHA: `9a3f537c251b6ee395fc5d35e5df82841f529c97`
*   Product PR #275 Merge commit: `f597491e4d80a06cc53bafbb0294b34c715113e3`

The testing implemented in Product Task 145 proves that the explicit wide-curve flag geometry and thick rectangle beam geometry are safely extracted and map properly to structural constraints. It also enforces that flag bounding boxes actually map to the flag curve, ruling out arbitrary non-zero counts caused by generic lower-notehead quadrant extraction.

No `eighth_note_candidate` reporting was implemented.
No extraction heuristics were changed.

## Decision

We authorise Product Task 148 to implement the `eighth_note_candidate` boundary.

The candidate composition rule must remain strictly **read-only** and bound to structural identity. It must compose `eighth_note_candidate` out of `quarter_note_candidate` plus nearby `flag_candidate` or `beam_candidate` evidence.

Composition constraints:

1.  **Identity Matching:** Explicitly require matching `page_index`, `system_index`, and `staff_index` for all components.
2.  **Geometric Safety:** Ensure overlap, touching, or tightly bounded proximity. Avoid staff-space margins unless staff-height parameters are available safely.

We explicitly keep out of scope any implementation of pitch, playable rhythm, ScoreIR, MusicXML, GP output, OCR, or rests. The boundary must just report structural generic candidates.
