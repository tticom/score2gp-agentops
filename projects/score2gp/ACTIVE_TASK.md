# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: SHORT-01A — Close the REQ-0005 silent gaps that contradict fail-closed rules (G5, G7, G8)

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/short-01a-close-fail-closed-silent-gaps`

**Pull Request**: 534

**Owner Role**: implementation

## Objective

First slice of the accepted REQ-0005 (explained shortfalls): the three silent gaps that its research map (projects/score2gp/research/2026-09-26-res-req-0005-explained-shortfalls/01-current-state-map.md, section 'silent gaps named') says already contradict existing fail-closed rules, as measured at product SHA 3af1925 in September: G7 inferred rhythm reported as `success`, G8 synthesised rests carried at confidence 1.0, and G5 `generate-sidecar` crashing without a reason code. They may already be fixed or changed since; re-measure each on the current runtime.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
