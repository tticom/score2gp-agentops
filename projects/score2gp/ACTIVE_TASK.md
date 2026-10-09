# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: TS-READ-01 — Read the printed time signature from the PDF instead of requiring --time-signature

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/ts-read-01-printed-time-signature`

**Pull Request**: 484

**Owner Role**: implementation

## Objective

Read each system's printed time signature (vector-drawn, so shape recognition, as OMIT-01 reads the key signature) and use the caller-declared value only when none is printed or readable; refuse with a located reason when the two disagree. Evidence: the 2026-10-08 survey converted all 39 sources at the declared 4/4, and Combining_Maj_minor_pent_-_A (printed 12/8) refuses all 8 bars with 'bar_total_mismatch, 6 of 4 quarters'. Promoted from the backlog candidate TS-READ-01: Candidate from the PDF-GROUP-02 investigation (2026-10-03), not promoted. The time signature is a caller input (--time-signature) today. Combining_Maj_minor_pent_-_A is printed in 12/8: with the declared 4/4 it refuses (bar_total_mismatch 5, tuplet_number_unassociated 3), with 12/8 and no code change it converts 5 of 8 bars. Read the printed signature from the source and use the declared one only when none is printed or readable; if the two disagree, refuse with a located reason rather than choose. Never invent a value, never loosen a gate to raise a count; byte-identical GPIF for every file that converts today when its declared signature matches the printed one. UPDATE 2026-10-03 (BARTOTAL-01 close-out): the time signature is vector-drawn on these pages (no text match), so a reader needs shape recognition rather than text; and no file shown so far needs the check for correctness (E_Chord's bars are metrically correct under 4/4; its printed signature is still unconfirmed).

## Allowed paths

- `src/score2gp/pdf.py`
- `src/score2gp/pdf_*.py`
- `src/score2gp/notation_omr/**`
- `src/score2gp/recognition/**`
- `src/score2gp/ir.py`
- `src/score2gp/tabraw.py`
- `src/score2gp/build_ir.py`
- `src/score2gp/gpif.py`
- `src/score2gp/cli.py`
- `schemas/**`
- `tests/test_dur_02_oracle.py`
- `tests/test_dur_01_lesson3.py`
- `docs/design/**`
- `docs/architecture.md`
- `tests/test_ts_read_01_*.py`
- `tests/fixtures/pdf/ts_read_01/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
