# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: PERF-01 — Melodic_Expressions.pdf runs for minutes and gigabytes

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/perf-01-melodic-expressions-runtime`

**Pull Request**: 490

**Owner Role**: implementation

## Objective

In the 2026-10-08 survey Melodic_Expressions.pdf was stopped at the 300 s limit with its process tree at about 2.5 GB and still running, while every other source finished (slowest converting file Lesson-6: 29.5 s, 533 MB; tab books 114 s and 227 s under 400 MB). Profile the real file stage by stage, find what the cost follows, and either fix it with a bounded algorithm that leaves every output unchanged or add an explicit located resource gate: a conversion must finish or refuse with a code, never end by being killed. Resource use is cost (maintainer direction).

## Allowed paths

- `src/score2gp/pdf.py`
- `src/score2gp/pdf_*.py`
- `src/score2gp/notation_omr/**`
- `src/score2gp/build_ir.py`
- `src/score2gp/cli.py`
- `tests/test_perf_01_*.py`
- `tests/fixtures/pdf/perf_01/**`
- `docs/design/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
