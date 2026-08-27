# REC-05 — Raster Observation Adapter

Status: SKELETON — depends on REC-02
Role: Developer
Repository: `score2gp`

## Objective

Add deterministic page rendering and a typed raster evidence adapter that is a
peer of vector/text evidence, not a fallback source of final semantics.

## Required work

1. Pin renderer, scale, color mode and coordinate transform provenance.
2. Emit typed line/region/glyph observations with source pixel boxes.
3. Map raster coordinates into canonical page coordinates losslessly enough for
   cross-modal comparison.
4. Never mutate, overwrite or silently prefer vector observations.
5. Keep model loading outside the interface; the initial adapter may be classical.

## Acceptance and falsification

- Repeated rendering is deterministic at the accepted tolerance.
- Missing renderer or transform metadata fails closed.
- Raster disagreement remains observable rather than averaged away.

## Validation

Promoted prompt must include renderer provenance, coordinate round trips,
real-source probes, privacy checks and no-network execution.

