# REC-02 — Recognition Contract Schemas

Status: SKELETON — depends on REC-00
Role: Developer
Repository: `score2gp`

## Objective

Create versioned, frozen contracts for DocumentObservations, DocumentTopology,
RecognitionGraph, ResolutionResult and MusicalDocument without changing runtime
recognition or export behaviour.

## Required work

1. Translate only accepted REC-00 terms into typed contracts and JSON schemas.
2. Require stable IDs, source coordinates, modality, provenance and versions.
3. Model alternatives, conflicts and four resolution outcomes explicitly.
4. Add schema snapshots, round-trip tests and semantic-leakage negative tests.
5. Do not add adapters, detectors, inference rules or compiler integration.

## Acceptance and falsification

- Observation schemas reject staff/string/bar/measure/event semantic assignments.
- Graph relations reference existing stable node IDs.
- Invalid or cross-version payloads fail closed with useful diagnostics.

## Validation

Promoted prompt must name exact schema files, tests, regeneration command,
artifact audit and full relevant type checks.

- Schema files: `src/score2gp/recognition/schemas.py`
- Tests: `tests/recognition/test_schemas.py`
- Validation command: `python3 -m pytest tests/recognition/test_schemas.py`
