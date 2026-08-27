# REC-04 — Local Scale Model

Status: SKELETON — depends on REC-03
Role: Developer
Repository: `score2gp`

## Objective

Estimate local notation, TAB, stroke and glyph scales and express new detector
policies in dimensionless units.

## Required work

1. Define typed scale estimates, support observations and uncertainty.
2. Estimate notation staff space and TAB string space independently.
3. Retain raw and normalized measurements in diagnostics.
4. Replace only constants explicitly authorized by the promoted prompt.
5. Return Unsupported rather than a default scale when evidence is inadequate.

## Acceptance and falsification

- Equivalent layouts at different sizes produce materially stable normalized data.
- Mixed-scale pages do not collapse into a misleading page-global unit.
- No fixture-specific coordinates or expected counts enter estimation.

## Validation

Require at least two real scores with different scales plus synthetic
transformation tests that are algorithmic evidence only.

