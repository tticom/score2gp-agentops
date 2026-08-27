# REC-03 — Canonical Vector and Text Observations

Status: SKELETON — depends on REC-02
Role: Developer
Repository: `score2gp`

## Objective

Implement the vector/text evidence adapter and reconstruct canonical strokes,
glyphs and text spans without assigning musical meaning.

## Required work

1. Extract acquisition from `pdf.py` behind `observe(source)`.
2. Preserve raw primitive IDs and reconstruction derivations.
3. Normalize coordinates without losing original page-space coordinates.
4. Return typed observations and explicit adapter failures.
5. Keep the legacy path operational through a temporary compatibility adapter.

## Acceptance and falsification

- Fragmented and repeated drawing operations have provenance-preserving output.
- No output field asserts staff, barline, string, measure, duration, pitch or event.
- Private real-source probes show deterministic output at the exact revision.

## Validation

Promoted prompt must pin two differently generated PDFs, schema tests, adapter
determinism, legacy compatibility and artifact-safety commands.

