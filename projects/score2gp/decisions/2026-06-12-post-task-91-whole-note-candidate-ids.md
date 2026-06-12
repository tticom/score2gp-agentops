# 2026-06-12 Post-Task 91: Whole-Note Candidate IDs

## Summary

Product Task 91 has been completed via PR #252. The diagnostic engine now explicitly exposes deterministic `candidate_id` values (e.g. `whole_note_candidate_001`, `whole_note_candidate_002`) inside the candidate locations list. The extracted whole-note candidates are output in a stable geometric ordering strictly dictated by their bounding box coordinates (top, left, bottom, right). This significantly improves the developer usability of the raw extraction results.

## Review and Process Rules Preserved

*   **Codex Comment Disposition:** Every future review must explicitly inspect Codex comments and review threads. Every Codex comment or review thread must be dispositioned as one of: accepted as blocker; accepted as non-blocking; already fixed; rejected with reason.
*   **Whole-note vs Half-note Boundary:** The mandatory distinction (whole notes = hollow ovals without an attached or nearby vertical stem) remains fully enforced.
*   **Diagnostic Boundaries:** No ScoreIR or GP emission occurs, and output remains strictly diagnostic.

## Authorisation: Product Task 93

We are authorising Product Task 93 to add a machine-checkable summary block to the normal diagnostic report output, further enhancing report usability without adding process.

**Task 93 Goals:**

*   Add a machine-checkable `whole_note_candidate_summary` block to normal diagnostic report output.
*   Include at least:
    *   `total_count`
    *   `pages_with_candidates`
    *   `candidate_ids`
    *   `candidate_count_by_page`
*   Keep existing fields backwards compatible (`whole_note_candidate`, `whole_note_candidate_pages`, `whole_note_candidate_locations`).
*   Ensure summary data is perfectly derived from the identically sorted candidate list as `whole_note_candidate_locations`.
*   Include regression tests proving:
    *   Positive whole-note fixture summary reports total count 2.
    *   `candidate_ids` array matches the emitted location IDs exactly.
    *   `candidate_count_by_page` array matches `whole_note_candidate_pages`.
    *   Half-note fixture summary reports total count 0.
    *   Negative/noise fixture summary reports total count 0.
    *   Report output remains diagnostic-only.
    *   No ScoreIR or GP output is produced.
    *   No pitch or duration inference is introduced.
    *   Existing raster/treble-clef diagnostics behaviour still passes.

**Allowed Additions:**

Task 93 may optionally include purely diagnostic geometric metadata:
*   `candidate_id`
*   `page_index`
*   `bbox`
*   `candidate_count_by_page`
*   `pages_with_candidates`
*   Geometric sort key, or similar non-semantic fields.

**Strict Boundaries (Task 93 must not):**

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
