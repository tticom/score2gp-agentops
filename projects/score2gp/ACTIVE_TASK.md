# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: DUR-02-FU2 — test_npg03b_floating asserts the refusal the source causes, not the generic missing-durations guard

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/dur-02-fu2-npg03b-floating-asserts-real-refusal`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

test_npg03b_floating asserts the refusal the source causes, not the generic missing-durations guard. Source: authority item DUR-02-FU2. Non-blocking follow-up from tticomgov-code's approving review 5331280846 of tticom/score2gp#467 (DUR-02) at 4564a87. Thread N3 at tests/test_npg03b_floating.py:25: the test calls build_ir_from_tabraw_only without note_durations, so it hits the note_durations-is-None guard that fires for any PDF. Pass the DUR-01 records and assert the category the route produces for a source with no notation bars.

## Allowed paths

- `tests/**`
- `src/score2gp/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
