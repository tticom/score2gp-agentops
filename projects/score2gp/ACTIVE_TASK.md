# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: CP-15 — Merge gate: a COMMENTED review must not displace the same reviewer's earlier APPROVE at the head

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `feat/cp-15-commented-review-keeps-earlier-approve`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

This task is gate-adjacent. It may only make the gate read the evidence it already reads more correctly; no review, merge or audit check may be removed, loosened or reordered, and anything that was denied for a real reason stays denied. Seen 2026-09-27 on tticom/score2gp#466: current_head_review keeps only each author's latest review state at the head, so the reviewer's thread reply (a COMMENTED review after its APPROVE) replaced the APPROVE; with no APPROVED or CHANGES_REQUESTED verdict left it returned NONE, and verify_merge_gate denied (current_head_not_approved and dependants) until the reviewer republished APPROVE. Fix: skip COMMENTED reviews when taking each author's latest verdict, keeping a later CHANGES_REQUESTED or DISMISSED decisive; test all three.

## Allowed paths

- `scripts/score2gp_orca_control.py`
- `tests/test_cp_15_*.py`
- `tests/test_score2gp_orca_control.py`

## Validation commands

- `python -m pytest`
- `PYTHONUTF8=1 python scripts/score2gp_governance_audit.py`
- `git diff --check`
