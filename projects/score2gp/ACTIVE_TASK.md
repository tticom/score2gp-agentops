# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: DUR-03-FU4 — DUR-03 cleanups: redundant duplicate check in _recovered_segmented_tab_groups and tautological assertion

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/dur-03-fu4-cleanups`

**Pull Request**: 521

**Owner Role**: implementation

## Objective

DUR-03 cleanups: redundant duplicate check in _recovered_segmented_tab_groups and tautological assertion. Source: authority item DUR-03-FU4. Non-blocking style follow-up from tticomgov-code's approving review 5376313575 of tticom/score2gp#474 (DUR-03): a redundant duplicate check in _recovered_segmented_tab_groups (src/score2gp/pdf.py) and a few tautological mutant assertions in the edited test_private_acceptance_lesson6_duration_and_negative_control. Remove the duplicate and make each mutant assertion able to fail. Keep the written GP byte-identical.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
