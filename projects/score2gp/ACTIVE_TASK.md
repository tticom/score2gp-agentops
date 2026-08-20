# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: NPG-00R — Decide recognition-engine ownership and Audiveris suitability

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `codex/npg-00r-architect-decision`

**Pull Request**: TBD

**Owner Role**: architect

## Objective

Use the Automation evidence handoff plus independent Architect research to decide whether Score2GP should consume a suitable third-party recognition object, build and own the required recognition layer, or adopt a bounded hybrid; convert the decision into explicit system requirements and a sequenced task boundary without implementing product behavior.

## Allowed paths

- `projects/score2gp/runs/2026-08-20-npg-00r-automation-handoff.md`
- `projects/score2gp/decisions/2026-08-20-npg-00r-recognition-engine-ownership.md`
- `projects/score2gp/ARCHITECTURE_DECISIONS.md`
- `projects/score2gp/plans/2026-08-19-native-pdf-to-gp-and-audiveris-retirement.md`

## Validation commands

- `python3 scripts/score2gp_governance_audit.py`
- `git diff --check origin/main...HEAD`
