# Active Task

**Task**: PDFTAB-DUR-05: TabRaw Duration Evidence Pipeline Integration
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer / Pipeline Integrator
**Repository**: tticom/score2gp
**PR Branch**: `agy/pdftab-duration-tabraw-integration`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0022-pdf-tab-duration-tabraw-integration.md`

## Context

Following the merge of PR #393 (`545d0bea36513969d0e53fc56e93cbc6c3e35518`), Slice 1 (Duration Types & Spatial Associator Primitive) is fully merged in `score2gp`. This task implements Slice 2 (TabRaw Pipeline Integration) as defined in Section 7 of `docs/design/pdf-tab-duration-candidate-extraction.md`.

## Goal

Extend `TabCandidate` and `TabRaw` in `src/score2gp/tabraw.py` to store, validate, serialize, and expose optional `TabDurationEvidence` within `TabCandidate.raw["duration_evidence"]`.
Implement helper constructors and property accessors for `duration_evidence` on `TabCandidate`.
Implement comprehensive unit tests in `tests/test_tabraw_duration_metadata.py` verifying schema validation, JSON round-trip serialization, dict normalization, and fail-closed handling of malformed evidence payloads.

## Allowed Files

- `src/score2gp/tabraw.py` (in `score2gp`)
- `tests/test_tabraw_duration_metadata.py` (in `score2gp`)

## Non-goals

No edits to existing assemblers (`pdf_tab_bar_assembler.py`), premature pipeline wiring, private inputs, reference GP leakage, automatic merge, or branch deletion.

## Acceptance

`tabraw.py` is updated in `score2gp` to cleanly handle `TabDurationEvidence` in `TabCandidate.raw`. Unit tests in `tests/test_tabraw_duration_metadata.py` pass 100%, covering construction, serialization/deserialization, helper properties, and error boundary handling. `agent_verify.py` passes cleanly, product PR is opened, and handback comment is published.
