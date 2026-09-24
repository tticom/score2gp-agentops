# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: WIN-03 — Product Repository OS-Agnostic Tooling

**Status**: COMPLETED

**Repository**: tticom/score2gp

**PR Branch**: `feat/win-03-product-os-agnostic-tooling`

**Pull Request**: 463

**Owner Role**: implementation

## Objective

Remove WSL references and POSIX-only virtualenv assumptions from the product repository's tooling and agent guidance.

## Allowed paths

- `scripts/corpus_harness.py`
- `tests/test_corpus_harness.py`
- `Makefile`
- `CLAUDE.md`

## Validation commands

- `python -m pytest tests/test_corpus_harness.py`
- `python scripts/artifact_audit.py`
- `git diff --check`
