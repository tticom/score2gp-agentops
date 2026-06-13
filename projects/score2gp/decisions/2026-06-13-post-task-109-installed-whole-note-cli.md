# Decision: Record Product Task 109 and Authorise Product Task 111 (Shared Candidate Shaping)

## Context
Product Task 109 has been implemented and successfully merged. It exposed the read-only whole-note recognition outcomes through the installed product CLI, closing the gap identified in the previous review phase.

Verified evidence:
- **Product PR URL**: https://github.com/tticom/score2gp/pull/261
- **Title**: `feat(cli): expose whole-note recognition report`
- **Head SHA**: `49dac633ebb333860e17fcf4883d928f69e1ff9e`
- **Merge Commit SHA**: `e52833c67b63067d45ad9f5f50a7fc4693692421`
- **Installed CLI command added**: `score2gp whole-note-recognition`
- **Changed Files**:
  - `src/score2gp/whole_note_recogniser.py`
  - `src/score2gp/cli.py`
  - `scripts/whole_note_recognition_report.py`
  - `tests/test_whole_note_recognition_cli.py`
- **Validation**:
  - Shared recognition report execution logic was safely moved to `src/score2gp/whole_note_recogniser.py`.
  - The script `scripts/whole_note_recognition_report.py` was kept as a backwards-compatible thin wrapper.
  - Installed CLI tests (`tests/test_whole_note_recognition_cli.py`) invoke the Typer subcommand directly, verifying structure and deep nested temporary path sanitisation.
  - Privacy-safe source metadata (`pdf_path.name`) is strictly maintained.
  - All CI tests and diagnostic gate checks passed successfully.

## Decision
We authorise Product Task 111: Extract shared whole-note candidate evidence shaping for diagnostics and recognition.

## Constraints for Product Task 111
- Extract the smallest shared helper for whole-note candidate evidence shaping if duplication is confirmed (between `scripts/raster_diagnostics_gate_report.py`, `src/score2gp/whole_note_recogniser.py`, etc.).
- Ensure that candidate ordering, ID assignment, page index handling, and privacy-safe metadata shaping stay exactly consistent across both diagnostic and recognition surfaces.
- Both paths must continue to yield identical current outputs without changing extraction thresholds.
- Preserve existing installed CLI, source-tree script, and raster diagnostics gate behaviour.
- Add regression coverage to guarantee outputs stay synchronised across these dependent paths.
- Do NOT add broader notation semantics (ScoreIR, GP output, MusicXML, pitch/rhythm inference, OCR, etc.).

Next recommended action: after this governance PR is merged, create the Product Task 111 executable prompt in ChatGPT.
