# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: MEM-01-FU1 — Tighten the MEM-01 IR bytes-per-bar budget

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/mem-01-fu1-tighten-ir-bytes-per-bar-budget`

**Pull Request**: 523

**Owner Role**: implementation

## Objective

Tighten the MEM-01 IR bytes-per-bar budget. Source: authority item MEM-01-FU1. Non-blocking follow-up 1 from tticomgov-code's approving review of tticom/score2gp#472 (MEM-01) at caf71f3. The budget bound in tests/test_mem_01_budget.py is 20,000 bytes per bar, but the compact IR measures about 9,040 bytes per bar on the public fixture, so a re-inflation of about 2x would not fail the test. Tighten the bound (or add per-fixture bounds) when more public engraved fixtures exist; keep the negative control that restores the full raw payload and must fail.

## Allowed paths

- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
