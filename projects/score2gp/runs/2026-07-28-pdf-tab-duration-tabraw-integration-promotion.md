# Governance Record: PDFTAB-DUR-05 Task Promotion

**Task**: PDFTAB-DUR-05: TabRaw Duration Evidence Pipeline Integration
**Status**: AWAITING_EXTERNAL_REVIEW
**Author**: tticom-codex
**Repository**: tticom/score2gp-agentops
**Branch**: `codex/promote-pdf-tab-duration-tabraw-integration`

## Summary

Following the merge of PR #393 (`545d0bea36513969d0e53fc56e93cbc6c3e35518`), which delivered Slice 1 (`pdf_tab_duration_types.py` and `pdf_tab_duration_associator.py`), this governance PR promotes Task PDFTAB-DUR-05, authorizing Agy (`tticom-automation`) to implement Slice 2 of the durable architecture specification `docs/design/pdf-tab-duration-candidate-extraction.md`.

## Requirements

The task requires:
1. Extending `TabCandidate` and `make_tab_candidate` helper in `src/score2gp/tabraw.py` to support optional `duration_evidence` (instance of `TabDurationEvidence` or dictionary matching its schema).
2. Storing `duration_evidence` in `candidate.raw["duration_evidence"]` as a validated dict or model payload.
3. Exposing property `duration_evidence` on `TabCandidate` returning `TabDurationEvidence | None`.
4. Ensuring `TabRaw.from_json_file`, `TabRaw.to_json_file`, and `normalize_tabraw_payload` preserve `duration_evidence` across round-trip serialization.
5. Implementing 100% unit test coverage in `tests/test_tabraw_duration_metadata.py`.

## Target Scope

- Authorized Repository: `tticom/score2gp`
- Authorized Branch: `agy/pdftab-duration-tabraw-integration`
- Allowed Product Files:
  - `src/score2gp/tabraw.py`
  - `tests/test_tabraw_duration_metadata.py`

## Non-goals

No edits to existing assemblers, premature pipeline wiring, private inputs, reference GP leakage, automatic merge, or branch deletion.
