# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: MEM-01 — IR provenance: stop copying the full raw candidate into every event and note

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/mem-01-ir-provenance-footprint`

**Pull Request**: 472

**Owner Role**: implementation

## Objective

Cut score.ir.json size and build memory by referencing raw candidates by id; resource use is cost (maintainer direction 2026-09-29). Promoted from the backlog item added by #731; its measurement: Measured by governance on 2026-09-29 at product main 2e8c00b (worktree at d7eef3f) on this Windows host. score.ir.json for Lesson 3 (66 bars) is 25 MB compact / 51 MB on disk: bars[].events[] carry about 25 KB of provenance each (full raw candidate, bbox and grouping evidence), duplicated again on each note. Reference raw candidates by id (tab_raw.json already holds them), keep only what the writer and diagnostics consume, and add a regression budget (IR bytes per bar). Peak working set of one CLI conversion is about 400 MB (Lessons 3 and 6, 30 s each); measure again after the change.

## Allowed paths

- `src/score2gp/**`
- `schemas/**`
- `docs/design/**`
- `docs/architecture.md`
- `scripts/artifact_audit.py`
- `tests/test_mem_01_*.py`
- `tests/fixtures/**`
- `tests/test_build_ir.py`
- `tests/test_pdf_tab_duration_regression_audit.py`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
