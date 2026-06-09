# Candidate Diagnostics Consumption Boundary

**Status:** APPROVED
**Date:** 2026-06-09

## Verified Baseline
Product PR #234 introduced `left_margin_candidates` and `x_aligned_cluster_candidates` to `NotationStaffDiagnostics`.
These are geometry-only primitives explicitly exposed for downstream consumers, extracted safely from `left_margin_diags` and `clustering_diags` evidence.

## Candidate Diagnostics Contract
The candidate fields explicitly adhere to the following contract:
- **`None`**: Extraction was not run, or the prerequisite evidence array was unavailable.
- **`[]`**: Extraction was run against a valid evidence array, but no candidates met the criteria.
- **Populated List**: Valid geometric candidates derived entirely from real visual evidence.

## Safe Consumer Permissions
Downstream consumers (e.g., Recogniser components) are **permitted** to:
- Read `left_margin_candidates` and `x_aligned_cluster_candidates` directly from `NotationStaffDiagnostics`.
- Treat these candidates as physical regions of interest containing notation evidence.
- Rely on the `None` vs `[]` distinction to understand if a processing stage was skipped or yielded empty results.
- Map the candidates back to the parent staff using `page_index`, `system_index`, and `staff_index`.

## Explicitly Prohibited Interpretations
At this boundary, downstream consumers **must not**:
- Infer musical semantics from these candidates (e.g., assigning pitch, duration, or grouping them into chords).
- Classify candidates as specific musical objects (e.g., clefs, key signatures, time signatures, notes, rests).
- Emit or construct any ScoreIR events based on these candidates.
- Alter or synthesize the geometric bounds (`x0, y0, x1, y1`) of the candidates.

## Evidence Preservation Requirements
All consumers must preserve the original geometry, input order, primitive kind, and font metadata supplied by the candidate object. The candidate represents the exact physical evidence on the page and must not be mutated or abstractly grouped before specific recognisers are implemented.

## Missing Prerequisite Evidence
Before robust recogniser implementation can begin, the following prerequisite evidence and diagnostics may still be needed:
- Refined horizontal timelines (e.g., measure/bar box mappings).
- System-level connectivity evidence (e.g., multi-staff grouping guarantees).
- Precise stem and notehead candidate models.
- Identification of textual annotations/lyrics versus notation markings.

## Recommended Next Task
The recommended next smallest safe task is to define and implement the **first read-only primitive recogniser** strictly bounded by the extracted candidate geometry.
For instance: `Task 47 — Implement read-only Clef or Key Signature recogniser over left-margin candidates`. This task must be restricted to classification within the candidate bounds without producing ScoreIR events.

## Stop Conditions for Future Implementation
Implementation of recognisers must halt and return to governance if:
- It requires inferring geometry not explicitly provided by the candidates.
- It requires emitting ScoreIR events.
- It cannot gracefully handle `None` vs `[]` states.
- It forces premature semantic grouping across multiple disconnected primitives.

## Known Limitations
The current candidates provide pure geometric and primitive-type data. Consumers must handle cases where complex, compound musical symbols (e.g., complex time signatures or multi-character text) are represented as multiple separate primitive candidates.
