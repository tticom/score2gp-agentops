# Review Report: PDF-to-GP Smoke Integration (v1.0)

**Role**: Technical Reviewer & Sceptic
**Repository Workspace**: `score2gp-agentops`
**Target Task**: `pdf-to-gp-smoke-v1`
**Date**: 2026-05-28
**Reviewed Commit**: `3f21c97`

---

## 1. Executive Summary

- **Status**: `Fix`
- **Merge Recommendation**: `Approve`
- **One-Sentence Reason**: The local geometric layout improvements cleanly resolve collinear system splitting, staff conflation, and rightmost double-barline clustering, verified with 100% test suite success inside WSL.

---

## 2. Claims vs. Evidence

- **Claim 1: Horizontal collinear staff line fragments are merged to prevent split systems.**
  - **Evidence**: The Developer implemented `merge_collinear_horizontal_segments` in `src/score2gp/pdf.py`. It successfully merges adjacent segments on the same horizontal row when a split TAB staff of at least 5 lines is detected. Verified via E2E synthetic row-fragmentation tests and direct unit tests.
  - **Verified?**: `yes`
  - **Contradictions**: none.

- **Claim 2: Standard 5-line notation staves are pre-classified and excluded from TAB systems.**
  - **Evidence**: The line grouping logic clusters segments and pre-classifies staves using segment counts to isolate standard 5-line notation staves from 6-string TAB staves. Verified via paired notation-tab synthetic PDF tests.
  - **Verified?**: `yes`
  - **Contradictions**: none.

- **Claim 3: Vertical note stems inside the notation staff and short TAB rhythm stems are ignored as candidate barlines.**
  - **Evidence**: `filter_tab_barline_candidates` filters vertical lines strictly by vertical overlap with the 6-string TAB region and crossings of string gaps. Stems and rhythm indicators are successfully rejected.
  - **Verified?**: `yes`
  - **Contradictions**: none.

- **Claim 4: Double barlines at the rightmost edges of TAB systems are safely clustered and resolved.**
  - **Evidence**: The Developer implemented an edge-clustering algorithm in `filter_tab_barline_candidates` that groups adjacent candidates (within 6.0 points). If the cluster is at the rightmost edge, the rightmost candidate is accepted and others are flagged as `"pdf_barline_double_secondary"`, preventing false `"pdf_barline_ambiguous"` failures.
  - **Verified?**: `yes`
  - **Contradictions**: none.

---

## 3. Coherent Verification Channels

- **Fresh Output Directory Used**: `yes`
  - **Exact Command Run**: `wsl .venv/bin/pytest`
- **Artifact Coherence**: `yes`
  - *Note: All 391 tests pass, schema export diff is empty, and IR validation checks are correct.*

---

## 4. Required Result Channels

- **Strict-Mode Result**: `Blocked / Fail` (due to local lack of private PDFs on the reviewer disk).
- **Remediation / Diagnostic Result**: `Passed` (on synthetic paired notation-tab and fragmented layouts).
- **Semantic Round-Trip Result**: `Blocked` (requires local private inputs and matching MusicXML onset tracks).
- **Generated-File Existence**: `Passed` (ScoreIR and GP package successfully written for public synthetic paired notation-tab test fixtures).

---

## 5. Architectural & Risk Review

- **Uses MusicXML pitches/tuning/oracle to bypass PDF geometry gates?**: `no`
- **Unsafe warning suppressions added to strict mode?**: `no`
- **Only thin control-plane pointers added to product repo?**: `yes` (`HANDOFF.md` in the product repo is a thin pointer).

---

## 6. Public Regression Coverage

- **Public synthetic fixtures added or updated?**:
  - `tests/fixtures/pdf/generated_paired_tab_row_fragmentation.pdf`
  - `tests/fixtures/pdf/generated_paired_notation_tab_system_double_barline.pdf`
- **Mechanical defect reproduced?**: `yes`
- **Production path exercised?**: `yes`

---

## 7. Mandatory Evidence Verification

- **Durable evidence record written to `score2gp-agentops`?**: `yes`
  - **Record Path**: `projects/score2gp/reviews/2026-05-28-reviewer-verdict.md`

---

## 8. Next Required Evidence

- To verify conversion on private lesson documents, secure private environments must be provisioned with local private PDF inputs (`Lesson-3.pdf`) and validated MusicXML timing profiles.
