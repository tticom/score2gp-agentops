# ScoreToGP Evidence Register

This register catalogues and tracks all agentic claims and their corresponding verified statuses. Reviewer/architect agents must record entries in this schema to maintain repository transparency and historical review posture.

## Template

### [Evidence Entry ID / Title]

- **Claim**: The precise claim made by the implementation agent (e.g., "Visual DP system alignment resolved System 6 and restored 100% of lead notes").
- **Source**: Local feature branch name, commit hash, or PR number.
- **Evidence Type**: `visual` / `source` / `logs` / `generated_outputs` / `diagnostic_tables` (visual comparison and source files outrank summaries).
- **Status**: `verified` / `unverified` / `contradicted` / `blocked` (a claim is verified only when supported by coherent, reproducible evidence).
- **Artifact Location**: Local workspace folder path or brain artifact path (e.g. `work/roundtrip_eval_clean_2026_05_27_reconciled`).
- **Private-Safe Summary**: Anonymized metrics and safe structural counts without exposing private musical text or fret sequences.
- **Review Decision**: `approve` / `keep_draft` / `request_changes` / `close_supersede`.
- **Next Required Evidence**: Exact evidence or Synthetic reproducing fixture required to resolve unverified/contradicted claims.

---

## Active Evidence Log

### EV-001: Derek Trucks Stress-Research Mismatched Measures

- **Claim**: Derek Trucks PDF omitted measures 15 and 16; source-pair inequivalence was proven.
- **Source**: branch `bugfix/gp-exported-pdf-layout-research-v0.1`, PR #137
- **Evidence Type**: `visual` / `diagnostic_tables`
- **Status**: **contradicted**
- **Artifact Location**: `work/roundtrip_eval_clean_2026_05_27_reconciled/roundtrip_report.json`
- **Private-Safe Summary**: The raw visual PDF inspection of the printed pages clearly shows that Measures 15 and 16 exist and feature visible tab fret numbers. The diagnostic parser failed to capture or associate the candidates, leading to a false "omitted measures" claim.
- **Review Decision**: **keep_draft** (PR remains in Draft state).
- **Next Required Evidence**: Investigation of visual PDF coordinate mapping, string line detection boundaries, or system barlines on the final page of the PDF to determine why these measures were ignored by the extraction engine.

### EV-002: Major Triads Lesson 3 Edge Boundary Fallback Rejection Resolved

- **Claim**: Minimal Stage 1 Geometry-Normalizer successfully snaps truncated staves and clears all edge-boundary fallback rejections (pdf_bar_box_edge_boundary_fallback_rejected) for Major Triads Lesson 3 without soft pitch gates.
- **Source**: branch `bugfix/pipeline-geometry-normalizer-slice-v0.1`, PR draft #4
- **Evidence Type**: `logs` / `diagnostic_tables`
- **Status**: **verified**
- **Artifact Location**: `work/roundtrip_eval_clean_normalizer_v4/warnings.json`
- **Private-Safe Summary**: The normalizer projected margins dynamically using median coordinate columns and ignored outside noise/boundary-double-barlines. The fatal `pdf_bar_box_edge_boundary_fallback_rejected` was reduced to exactly `0` across the entire document, resolving the extraction blocker and increasing successfully boxed candidates to `399`.
- **Review Decision**: **approve**
- **Next Required Evidence**: Implement robust visual segmentation to correctly align the remaining unboxed systems (e.g. Page 2 System 13, Page 4 System 1) that feature complex multi-system layouts.

### EV-003: Melodic Soloing Safe Barline Recovery Pass

- **Claim**: Safe barline recovery pass recovered System 1 and System 3, improving matched fret candidate count from 16 to 41 for `private_input_custom_melodic_soloing` while maintaining perfect stability on Lessons 3-7.
- **Source**: branch `feature/melodic-soloing-safe-barline-recovery-v0.1`
- **Evidence Type**: `logs` / `diagnostic_tables`
- **Status**: **verified**
- **Artifact Location**: `work/private_gp_quality_audit_v0_1/summary.json`
- **Private-Safe Summary**: `private_input_custom_melodic_soloing` matched notes improved from 16 to 41. ScoreIR and GPIF note counts are equal. Lessons 3-7 are stable.
- **Review Decision**: **approve**
- **Next Required Evidence**: Implement fragmented-line grouping to resolve the remaining middle system (System 2) and recover the remaining notes.

### EV-004: Melodic Soloing Fragmented TAB Staff-Line Grouping

- **Claim**: Fragmented staff-line grouping recovered additional valid TAB evidence by safely merging horizontal staff-line fragments only when supported by neighbouring staff-line geometry. `private_input_custom_melodic_soloing` improved from 41 to 50 matched notes while public tests passed and private safety remained clean. Lesson 3 and Lesson 6 count increases were reviewed and classified as legitimate recoveries of highly fragmented staff lines.
- **Source**: branch `feature/melodic-soloing-fragmented-line-grouping-v0.1`, PR #163, merge commit `1ce31296b5589a7c8ebd45a350ab4aab4f5640c6`
- **Evidence Type**: `logs` / `diagnostic_tables` / `source`
- **Status**: **verified**
- **Artifact Location**: `work/private_gp_quality_audit_v0_1/summary.json`
- **Private-Safe Summary**: `private_input_custom_melodic_soloing` matched notes improved from 41 to 50. Lessons 3 and 6 increased to 459 and 235 matched notes respectively. ScoreIR and GPIF note counts are equal. Lessons 4, 5, and 7 are stable.
- **Review Decision**: **approve**
- **Next Required Evidence**: Run the next private-safe active-blocker audit after PR #163 merge to identify whether the remaining melodic soloing note loss is caused by timing/bar assignment, candidate extraction, MusicXML alignment, or another grouping limitation.
