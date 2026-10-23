# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: DUR-02-FU2 — A TAB-only source with no notation keeps its bars and writes no notes (retargeted from asserting a refusal)

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/dur-02-fu2-npg03b-floating-asserts-real-refusal`

**Pull Request**: 510

**Owner Role**: implementation

## Objective

Retargeted on the maintainer's direction (2026-10-23): the author's preflight (2026-10-22) showed the named private PDF has notation (3 systems, 8 bars, 82 events), so the premise 'a source with no notation staff' was false for it. The maintainer added a genuine no-notes source to the fixtures (no-score/No Notes.pdf with reference no-notes.gp, 9 bars and no beats) and said: 'I think the output should retain the bars but write no notes'. Make a source whose staves are printed but empty keep its bars and write no notes, with no note or rhythm invented, instead of refusing. test_npg03b_floating keeps its original numeric checks and asserts what the route now does.

## Allowed paths

- `tests/**`
- `src/score2gp/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
