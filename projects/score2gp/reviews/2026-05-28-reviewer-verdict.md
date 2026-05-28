# ScoreToGP PR Review: PDF-to-GP Smoke Integration (v1.0)

**Durable Record Path**: `projects/score2gp/reviews/2026-05-28-reviewer-verdict.md`
**Reviewer ID**: `score2gp-reviewer`
**Target Commit**: `3f21c97`

---

## 1. Executive Summary

- **Status**: `Fix`
- **Merge Recommendation**: `Approve`
- **One-Sentence Reason**: The local geometric layout improvements cleanly resolve collinear splitting and staff/barline conflation, verified 100% correct on public synthetic fixtures with all 391 tests passing successfully.

---

## 2. Claims vs. Evidence

- **Claim**: Horizontal collinear staff lines are merged before grouping, eliminating collinear system splitting.
  - **Evidence**: Inspected logic in `src/score2gp/pdf.py` (specifically `merge_collinear_horizontal_segments` within `_tab_line_groups`). Verified direct tests `test_merge_collinear_horizontal_segments_row_fragmentation_direct` and E2E synthetic test `test_paired_tab_row_fragmentation_merging` in `tests/test_pdf.py` which passes cleanly.
  - **Verified?**: `yes`
  - **Contradictions**: none.

- **Claim**: Standard 5-line notation staves are pre-classified and excluded from forming TAB systems.
  - **Evidence**: Inspected `src/score2gp/pdf.py` (`_tab_line_groups`). Checked synthetic test `test_paired_tab_row_fragmentation_merging` where the 5-line notation staff is successfully ignored.
  - **Verified?**: `yes`
  - **Contradictions**: none.

- **Claim**: Vertical note stems inside the notation staff and short TAB rhythm stems are ignored as candidate barlines.
  - **Evidence**: Inspected `filter_tab_barline_candidates` in `src/score2gp/pdf.py` and unit tests in `tests/test_pdf.py` verifying stem filtering.
  - **Verified?**: `yes`
  - **Contradictions**: none.

---

## 3. Coherent Verification Channels

- **Fresh Output Directory Used**: `yes`
  - **Exact Command Run**: `wsl .venv/bin/pytest`
- **Artifact Coherence**: `yes`
  - *Note: All 391 tests pass, schemas perfectly aligned, and tiny_score.ir.json validates cleanly against scoreir schema.*

---

## 4. Required Result Channels

- **Strict-Mode Result**: Blocked / Fail (due to missing private benchmark inputs on disk, which prevents strict mode compilation of private inputs).
- **Remediation / Diagnostic Result**: Passed (on synthetic paired notation-tab fragmentation layout).
- **Semantic Round-Trip Result**: Blocked (requires clean MusicXML and private PDFs).
- **Generated-File Existence**: Passed (ScoreIR and GP package successfully written for the synthetic paired notation-tab test).

---

## 5. Architectural & Risk Review

- **Uses MusicXML pitches/tuning/oracle to bypass PDF geometry gates?**: `no`
- **Unsafe warning suppressions added to strict mode?**: `no`
- **Only thin control-plane pointers added to product repo?**: `yes` (HANDOFF.md is a thin pointer).

---

## 6. Public Regression Coverage

- **Public synthetic fixture added or updated?**: `tests/fixtures/pdf/generated_paired_tab_row_fragmentation.pdf`
- **Mechanical defect reproduced?**: `yes`
- **Production path exercised?**: `yes`

---

## 7. Mandatory Evidence Verification

- **Durable evidence record written to `score2gp-agentops`?**: `yes`
  - **Record Path**: `projects/score2gp/reviews/2026-05-28-reviewer-verdict.md`

---

## 8. Next Required Evidence

- To advance to full conversion progress, private born-digital PDF inputs (e.g., `Lesson-3.pdf`) must be loaded into a secure, private test runner environment along with clean MusicXML timing templates to verify strict-mode zero-bypass compilation.
