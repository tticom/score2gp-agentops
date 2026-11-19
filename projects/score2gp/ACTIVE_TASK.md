# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: DEC-02 — Reconcile ADR-006 and product ADR-0004 into one ADR: observed TAB positions are authoritative; inference only for notation-only notes, labelled with provenance

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `feat/dec-02-reconcile-position-adr`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Reconcile ADR-006 (forbids biomechanical position inference) and product ADR-0004 (retains the position optimizer) into one decision record with status Proposed: observed TAB positions are authoritative, inference only for notation-only notes and labelled with provenance. Records only: no product edit; migrating product ADRs is DEC-03. Leads, not facts: re-read the code and both ADRs.

## Allowed paths

- `projects/score2gp/ARCHITECTURE_DECISIONS.md`
- `projects/score2gp/decisions/**`
- `projects/score2gp/prompts/next/dec-02-reconcile-position-adr.md`

## Validation commands

- `python -m pytest`
- `PYTHONUTF8=1 python scripts/score2gp_governance_audit.py`
- `git diff --check`
