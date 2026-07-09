# Req-125 Implementation Conformance Review

Date: 2026-07-09
Reviewer role: Reviewer
Task: Req-125 / Task 62/63
Governance PR: pending
Governance main SHA: pending

## Implementation Conformance Verdict

`approve implementation`

The implementation satisfies Req-125. The Developer extended the left-margin classifier heuristics in [logical_clef_candidate_classifier.py](file:///home/tticom/work/score2gp-workspace/score2gp/src/score2gp/logical_clef_candidate_classifier.py) to recognize Bass and Alto clef curve geometries on public fixtures. Robust filters (including horizontal offset checks) were added to prevent false matches from note flags or beams. All Pydantic model validations were hardened to use ValueError instead of assert, and snapshot files were successfully updated.

## PR Readiness Status

`READY`

Product PR #359 was merged cleanly. All tests and verification steps passed.

## Evidence Reviewed

Product files changed:

- `src/score2gp/logical_clef_candidate_classifier.py`: implemented Bass and Alto heuristics and horizontal offset checks.
- `src/score2gp/pdf_candidate_semantic_gate.py`: updated mapping for bass/alto, added `"alto"` to `LogicalClefKind`, and changed assert checks to raise ValueError in validator.
- `tests/test_logical_clef_candidate_classifier.py`: added unit tests for Bass and Alto clefs.
- `tests/test_pdf_semantic_candidate_snapshots.py`: registered bass_clef and alto_clef fixtures in snapshot checks.
- `fixtures/public/expected_semantic_candidates_*.json`: generated/updated expected snapshots.

Verification reviewed:

- `make verify`: passed (all tests passed, schema validation passed)
- `git diff --check`: passed
- `artifact_audit.py`: passed

## Claim-by-Claim Verification

### Claim 1: Extend left-margin candidate classification for Bass and Alto

Status: verified.

Implemented specific bounding box and proportional ratio checks for Bass clefs (`2.5 <= height_to_spacing <= 4.2` etc.) and Alto clefs (`3.0 <= height_to_spacing <= 4.5` etc.) on curve groups.

### Claim 2: Prevent false matches from flags/beams

Status: verified.

Added horizontal offset checks `(-2.0 * staff_spacing <= x0_offset <= 3.0 * staff_spacing)` which correctly ignores note flags/beams that are further right.

### Claim 3: Pydantic validators use ValueError instead of assert

Status: verified.

`LogicalClefCandidate.validate_clef_state` was modified to use explicit ValueError checks rather than assert statement.

### Claim 4: Deterministic validation on public fixtures

Status: verified.

The snapshot test verifies that `"bass"` and `"alto"` clefs are correctly identified on the new public fixtures.

## Tests Prove Wanted Behaviour

Yes. The classifier tests and the snapshot files confirm that Bass and Alto clefs are successfully classified and output in semantic diagnostics.

## Unsupported Claims

None.

## Required Fixes

None.
