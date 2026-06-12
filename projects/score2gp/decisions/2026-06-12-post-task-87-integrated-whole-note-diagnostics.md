# 2026-06-12 Post-Task 87: Integrated Whole-Note Diagnostics and Location Follow-up

## Status
Accepted

## Context
Product Task 87 / PR #250 is complete and merged. 
- It successfully integrated whole-note candidate diagnostics into the normal diagnostics flow (`extract_notation_diagnostics_dict` and `raster_diagnostics_gate_report.py`).
- It correctly addressed whitespace validation and Codex artifact blockers before merge.
- The diagnostic-only boundary is fully preserved.
- The mandatory distinction between whole notes (hollow oval without a stem) and half notes (hollow oval with an attached or closely adjacent vertical stem) is fully preserved.

Review Process Requirement Preserved:
Future reviews must explicitly inspect Codex comments and review threads. Every Codex comment or review thread must be dispositioned as:
- accepted as blocker;
- accepted as non-blocking;
- already fixed;
- rejected with reason.

The next priority is making these diagnostics product-visible. Currently, candidate counts are integrated, but we must expose whole-note candidate locations in normal diagnostic output.

## Decision: Authorise Product Task 89
Authorise Product Task 89 to expose whole-note candidate locations in the normal diagnostic output.

### Task 89 Requirements
- Expose whole-note candidate locations through a normal diagnostics report surface, not only raw model output.
- Include candidate bounding boxes (`bbox`) and `page_index`.
- Include candidate count per page and total count.
- Preserve the existing standalone script if useful.
- Preserve the integrated `extract_notation_diagnostics_dict` path.
- Preserve half-note exclusion.
- Include regression tests proving:
  - whole-note positive fixture reports two candidates with locations;
  - half-note fixture reports zero candidates;
  - negative/noise fixture reports zero candidates;
  - report output remains diagnostic-only;
  - no ScoreIR or GP output is produced;
  - no pitch or duration inference is introduced;
  - existing raster/treble-clef diagnostics behaviour still passes.

### Optional (If diagnostic and non-semantic)
- Task 89 may optionally include staff association only if it is clearly diagnostic and non-semantic.
  - Allowed: `nearest_staff_index`, `page_index`, `bbox`, or similar geometric fields.
  - Not allowed: pitch names, note values, duration values, voices, measures, key signatures, time signatures, rests, or full notation.

### Non-Goals for Task 89
- Do not emit ScoreIR.
- Do not emit GP files.
- Do not claim full semantic note recognition.
- Do not infer pitch.
- Do not infer duration/rhythm beyond diagnostic labels.
- Do not infer voices, measures, key signatures, time signatures, rests, or full notation.
- Do not use OCR.
- Do not require private fixtures.
- Do not commit generated raw outputs, screenshots, PDFs, GP files, logs, local scratch artifacts, or private data.
- Do not modify governance records during product implementation unless explicitly asked.
- Do not regress existing treble-clef/raster diagnostics behaviour.
