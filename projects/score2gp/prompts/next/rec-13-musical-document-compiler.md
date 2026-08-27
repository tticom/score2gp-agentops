# REC-13 — MusicalDocument and ScoreIR Compiler Seam

Status: SKELETON — depends on REC-12
Role: Developer
Repository: `score2gp`

## Objective

Introduce the typed MusicalDocument seam and compile validated semantics to
ScoreIR without `Any`, dictionary introspection or implicit fallback shapes.

## Required work

1. Finalize MusicalDocument invariants from resolved recognition output.
2. Add a new compiler interface accepting exactly one MusicalDocument.
3. Preserve observed versus optimized fingering provenance.
4. Keep GPIF serialization behaviour unchanged.
5. Maintain a temporary legacy adapter with explicit deprecation ownership.

## Acceptance and falsification

- Unresolved or contradictory musical content cannot reach ScoreIR.
- No-note, capacity and ownership errors remain human-readable and located.
- Existing format/schema tests and productive real-source exports remain green.

## Validation

Require type checks, compiler contract tests, GPIF regression tests, artifact
audit and REC-01 full-score evaluation.

