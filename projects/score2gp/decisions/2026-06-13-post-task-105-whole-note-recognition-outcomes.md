# Decision: Record Product Task 105 and Authorise Product Task 107 (Whole-Note Recognition Surface)

## Context
Product Task 105 has been successfully implemented and verified. It successfully added the first read-only whole-note recognition outcome mapping, bounded to existing validated diagnostic candidate evidence.

Verified evidence:
- **Product PR URL**: https://github.com/tticom/score2gp/pull/259
- **Title**: `feat(recognition): map whole-note candidates to read-only outcomes`
- **Head SHA**: `9b4ea7a535dbc856f8354bffbdb4ee77b7493e6c`
- **Merge Commit SHA**: `54504ce1e9bbeb2b30c2fd6473a309b7e25c53be`
- **Changed Files**:
  - `scripts/raster_diagnostics_gate_report.py`
  - `src/score2gp/whole_note_recogniser.py`
  - `tests/test_raster_diagnostics_gate_report.py`
  - `tests/test_whole_note_recognition_outcome.py`
- **Validation**:
  - `test_subprocess_json_read_only_recognition_outcomes_custom_case_id` regression test is present.
  - All tests passed.
  - CI and advisory checks were green.
- **Codex Disposition**: 
  - The comment “Emit outcomes for all whole-note candidate cases” was accepted as a blocker. It was fully addressed by emitting outcomes based on the fixture path or category, rather than a hardcoded alias, and enforced with a custom test case.

## Decision
We authorise Product Task 107: Expose read-only whole-note recognition outcomes through a narrow product-facing CLI/report surface. 

This will provide a machine-checkable JSON surface specifically for safe public whole-note fixtures or properly vetted PDF paths without adding full notation recognition.

## Constraints for Product Task 107
- Consume existing diagnostic whole-note candidate evidence and the Product Task 105 read-only recogniser.
- Keep the output explicitly diagnostic-derived/read-only.
- Do NOT add ScoreIR, GP output, MusicXML output, OCR, pitch inference, or full notation semantics.
- Preserve existing raster diagnostics gate behaviour and tests.

Next recommended action: after this governance PR is merged, create the Product Task 107 executable prompt in ChatGPT.
