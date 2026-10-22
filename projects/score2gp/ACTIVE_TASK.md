# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-01-FU1 — A one-accidental mid-system key change followed closely by a note at that pitch is read or refused, never carried as the old key

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-01-fu1-mid-system-key-change-ambiguity`

**Pull Request**: 508

**Owner Role**: implementation

## Objective

A one-accidental mid-system key change followed closely by a note at that pitch is read or refused, never carried as the old key. Source: authority item OMIT-01-FU1. Non-blocking follow-up from tticomgov-code's approving round-4 review of tticom/score2gp#468 (OMIT-01) at 6a40e82. Thread at src/score2gp/notation_omr/key_signature.py:217 (PLAUSIBLE): with no prefix, an attached candidate is always treated as a note accidental, so a single flat in slot 0 followed within 1.5 sp by a note at its pitch keeps the previous key with status read and no diagnostic (probe P3: gaps 0.5-1.4 sp read +1; 1.6 sp or another pitch read -1). Real-source evidence from the review (thread 4121094267, review 5337254165): note accidentals usually sit 0.19-0.31 sp from their head, but four genuine chord-displaced accidentals in Lesson 7 sit 1.34-1.46 sp away, inside the 1.5 sp window, and no real input reaches the P3 case. Decide by source geometry or refuse with a located reason, and include a displaced-note negative control (a genuine chord-displaced note accidental at 1.3-1.5 sp must stay a note accidental, not be refused or read as a key change).

## Allowed paths

- `src/score2gp/**`
- `tests/**`
- `docs/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
