# REC-07 — Physical Divisions and Measure Topology

Status: SKELETON — depends on REC-06
Role: Developer
Repository: `score2gp`

## Objective

Resolve physical-division evidence into globally consistent measure-boundary and
measure-region hypotheses without equating vertical strokes with barlines.

## Required work

1. Create division hypotheses from vector and raster observations.
2. Score staff span, paired-staff alignment, neighbours, repeats and conflicts.
3. Represent fragmented, floating, double and repeat-adjacent divisions.
4. Produce competing measure topologies when evidence does not decide.
5. Do not create musical events or repair capacity in this module.

## Acceptance and falsification

- Note stems and connectors are negative controls.
- Recognizing a boundary cannot create overlapping measure regions.
- Real-source oracle reports ordered boundaries, not only counts.

## Validation

Promoted prompt must include CRP-01 regression coverage, Lesson 5/6 held-out
topology results, a second layout family and first-divergence output.

