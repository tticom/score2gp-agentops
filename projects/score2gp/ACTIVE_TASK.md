# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-05 — Title, credits and page header/footer

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-05-title-credits-header-footer`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Carry the printed title and credits into `Score/Title` and `Score/Music`, and write Guitar Pro's header/footer templates where the reference has them. The output currently writes the invented placeholders 'PDF-Only Inferred Score', 'Unknown Composer' and 'Unknown', and hard-codes all four header/footer fields as empty (`gpif.py`, around lines 412-415).

## Allowed paths

- `src/score2gp/pdf.py`
- `src/score2gp/pdf_*.py`
- `src/score2gp/notation_omr/**`
- `src/score2gp/recognition/**`
- `src/score2gp/ir.py`
- `src/score2gp/tabraw.py`
- `src/score2gp/build_ir.py`
- `src/score2gp/gpif.py`
- `src/score2gp/gp_package.py`
- `src/score2gp/version_adapter.py`
- `src/score2gp/cli.py`
- `schemas/**`
- `tests/test_dur_02_oracle.py`
- `docs/design/**`
- `docs/architecture.md`
- `tests/test_omit_05_*.py`
- `tests/fixtures/pdf/omit_05/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
