# 2026-06-12 Post-Task 89: Whole-Note Location Output

## Summary

Product Task 89 has been completed via PR #251. The normal diagnostic report output now explicitly exposes whole-note candidate totals, per-page counts (`whole_note_candidate_pages`), and exact bounding box locations (`whole_note_candidate_locations`). This makes the extraction logic significantly more visible to developers and pipelines without promoting it to semantic inference.

## Review and Process Rules Preserved

*   **Codex Comment Disposition:** Every future review must explicitly inspect Codex comments and review threads. Every Codex comment or review thread must be dispositioned as one of: accepted as blocker; accepted as non-blocking; already fixed; rejected with reason.
*   **Whole-note vs Half-note Boundary:** The mandatory distinction (whole notes = hollow ovals without an attached or nearby vertical stem) remains fully enforced by the extraction logic.

## Authorisation: Product Task 91

We are authorising Product Task 91 to improve the diagnostic usability of the newly exposed whole-note candidate locations.

**Task 91 Goals:**

*   Add deterministic candidate IDs for whole-note candidates in normal diagnostic report output.
*   Preserve stable ordering of whole-note candidates by `page_index`, then a documented geometric sort key (e.g., bbox top/left).
*   Include IDs in both `whole_note_candidate_locations` and any detailed report surface where candidates are listed.
*   Keep `whole_note_candidate`, `whole_note_candidate_pages`, and `whole_note_candidate_locations` backwards compatible unless there is a strong reason to version the report schema.
*   Include regression tests proving:
    *   Candidate IDs are deterministic across repeated runs on the same fixture.
    *   Ordering is deterministic.
    *   Positive whole-note fixture reports two candidates with IDs, page index, and bbox.
    *   Half-note fixture reports zero candidates.
    *   Negative/noise fixture reports zero candidates.
    *   Report output remains diagnostic-only.
    *   No ScoreIR or GP output is produced.
    *   No pitch or duration inference is introduced.
    *   Existing raster/treble-clef diagnostics behaviour still passes.

**Allowed Additions:**

Task 91 may optionally include purely diagnostic geometric metadata inside the reporting payloads:
*   `candidate_id`
*   `page_index`
*   `bbox`
*   `nearest_staff_index`
*   Geometric sort keys or similar non-semantic fields.

**Strict Boundaries (Task 91 must not):**

*   Emit ScoreIR or GP files.
*   Claim full semantic note recognition.
*   Infer pitch.
*   Infer duration/rhythm beyond diagnostic labels.
*   Infer voices, measures, key signatures, time signatures, rests, or full notation.
*   Use OCR.
*   Require private fixtures.
*   Commit generated raw outputs, screenshots, PDFs, GP files, logs, local scratch artifacts, PR body files, or private data.
*   Modify governance records during product implementation unless explicitly asked.
*   Regress existing treble-clef/raster diagnostics behaviour.
