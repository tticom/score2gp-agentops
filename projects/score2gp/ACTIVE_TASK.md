# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: FIXTURE-GUARD-01 — Private-corpus tests that skip silently

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/fixture-guard-01-private-corpus-skip-guard`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

A rerun of product main's CI on the categorised fixtures (run 37831924173) went from 1784 passed, 10 skipped to 1783 passed, 11 skipped and stayed green: fixtures PR #5 renamed 'Finger postition tips TAB (1).pdf', so the SCALE-01 control test_tab_only_private_controls_have_no_notation_staves skips silently. Fix the name, and add a guard so that, with the private corpus mounted in CI, a private-corpus skip fails the job and lists the test ids.

## Allowed paths

- `tests/test_scale_01_geometry.py`
- `tests/conftest.py`
- `tests/private_corpus_guard.py`
- `tests/test_private_corpus_guard.py`
- `scripts/check_private_skips.py`
- `.github/workflows/pylint.yml`
- `docs/setup.md`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
