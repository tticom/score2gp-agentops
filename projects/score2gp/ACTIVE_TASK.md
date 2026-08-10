# Active Task

**Task**: Task 92 — Real-Source Oracle and Harness (CRP-04)
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Architect
**Repository**: tticom/score2gp-agentops
**PR Branch**: `agy/crp-04-real-source-oracle-harness`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0047-real-source-oracle-harness.md`

## Context

Task 91 (CRP-03) enabled page-continuous measure indexing and cumulative offsets in PR #424 (merged).
Task 92 (CRP-04) is the fourth stage of the Conversion Recovery Programme. It implements the reference-isolated real-source oracle harness and private-fixture runner for end-to-end PDF-to-GP conversion verification.

## Goal

Implement the generic semantic oracle and private-fixture runner with process-level reference isolation to evaluate PDF-to-GP conversion correctness without synthetic test fallbacks or reference GP leakage.

## Allowed Files

- `projects/score2gp/ACTIVE_TASK.md`
- `projects/score2gp/prompts/next/0047-real-source-oracle-harness.md`
- `scripts/score2gp_review_evidence_gate.py`
- `tests/test_governance_audit.py`

## Non-goals

- Do not use synthetic or mocked musical evidence to prove conversion behaviour.
- Do not grant the generator process access to the reference GP path.
- Do not broad-delete legacy unit tests before replacement fixtures are verified red/green.

## Acceptance

- `python3 scripts/score2gp_review_evidence_gate.py` passes all evidence gates.
- `python3 scripts/private_e2e_smoke.py` runs non-skipped on private fixtures (`Lesson-5.pdf`, `Lesson-6.pdf`).
- `python3 scripts/score2gp_governance_audit.py` passes with zero privacy/leakage errors.



