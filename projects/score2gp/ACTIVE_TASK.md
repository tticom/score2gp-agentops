# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: NPG-00A — Pin the native PDF-to-GP baseline and dependency inventory

**Status**: PROMOTED

**Repository**: tticom/score2gp-agentops

**PR Branch**: `codex/npg-00a-baseline-inventory`

**Pull Request**: TBD

**Owner Role**: architect

## Objective

Pin clean current product, governance, and skills revisions and inventory every native PDF, Audiveris, MusicXML, canonical-score, GPIF, package, test, dependency, environment, CI, and documentation path without changing product behavior.

## Allowed paths

- `projects/score2gp/reports/2026-08-19-npg-00a-baseline-and-dependency-inventory.md`

## Validation commands

- `python3 scripts/score2gp_governance_audit.py`
- `git diff --check origin/main...HEAD`
