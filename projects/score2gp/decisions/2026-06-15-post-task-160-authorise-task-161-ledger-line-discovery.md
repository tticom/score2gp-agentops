# Post-Task 160: Record Assumed-Treble Pitch Mapping and Authorise Ledger-Line Discovery

## Context
Product Task 160 is complete.

*   **Product PR #280 URL**: https://github.com/tticom/score2gp/pull/280
*   **Final head SHA**: `67ae5a3c75ba1791b7abd3c68a0f97e7f84e6245`
*   **Merge commit**: `5527c91d7d4917be7fb084c70b343ee971d0c1c3`
*   **Merged timestamp**: `2026-06-15T07:59:29Z`

**Exact files changed**:
*   `src/score2gp/cli.py`
*   `src/score2gp/whole_note_recogniser.py`
*   `scripts/note_candidate_recognition_report.py`
*   `tests/test_note_candidate_recognition_cli.py`
*   `tests/test_note_candidate_recognition_report.py`

## Decisions Recorded

**Opt-in assumed-treble behaviour**:
*   Added explicit opt-in assumed-treble pitch mapping.
*   Opt-in flag/parameter: CLI: `--assume-treble-clef`, Python API: `assume_treble_clef`.
*   Output field: `assumed_treble_pitch` (String value, e.g., `F5`).
*   The mapper uses strictly existing `staff_position_index`.
*   It is disabled by default. No pitch field is emitted unless explicitly enabled.

**Exact staff_position_index to assumed_treble_pitch mapping**:
*   `0` = `F5`
*   `1` = `E5`
*   `2` = `D5`
*   `3` = `C5`
*   `4` = `B4`
*   `5` = `A4`
*   `6` = `G4`
*   `7` = `F4`
*   `8` = `E4`

**Validation command and result**:
```bash
pytest tests/test_note_candidate_recognition_cli.py tests/test_note_candidate_recognition_report.py tests/test_whole_note_recognition_cli.py
```
*   Result: `32 passed`

**Codex disposition**:
*   Codex correctly identified missing installed CLI wiring. The finding was accepted, fixed, tested, and resolved before merge.

**Boundary limitations and explicitly rejected semantics**:
*   No generic pitch inference, clef recognition, accidentals, ledger-line pitch mapping, key signatures, or rhythm inference was implemented.
*   No ScoreIR, MusicXML, Guitar Pro, GP output, OCR, or rests were implemented.
*   Extraction, staff-association, eighth-note composition, and staff-position inference logic were not changed.

## Next Step
Product Task 161 is authorised.

**Product Task 161 is discovery and design only.**
It must explore `pdf_raster_staff_diagnostics.py`, determine how ledger-line primitives exist in current unboxed diagnostics, and propose a semantic boundary. It must produce a design document in the product repository `tticom/score2gp` (e.g., `docs/design/`), not in the governance repository. It must not implement extraction or update pitch mapping logic.
