# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: NPG-04A — One rational meter utility replacing fixed 4/4/3840 capacity

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/npg-04a-rational-meter-utility`

**Pull Request**: 531

**Owner Role**: implementation

## Objective

Replace the fixed 4/4, 3840-tick bar capacity with one rational meter utility driven by printed meter evidence, so 12/8, 6/8, 3/4 and other printed meters are read, not forced. Evidence: two private sources print 12/8 and the survey harness forced 4/4 and refused them with time_signature_conflict; this is the authority item NPG-04A (plans/2026-08-19-native-pdf-to-gp-and-audiveris-retirement.md section 16), which also absorbs RHY-03 and the Lesson 5 tempo-mismatch candidate.

## Allowed paths

- `src/score2gp/**`
- `tests/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
