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

### EV-005: Melodic Soloing Internal Double-Barline Recovery

- **Claim**: Internal size-2 TAB double-barline clusters are now conservatively resolved by accepting one representative and marking the secondary line as `pdf_barline_double_secondary`, while larger internal clusters remain ambiguous. This recovered the missing melodic soloing bar boxes from 5 to 8 and increased matched notes from 56 to 82 without regressing Lessons 3–7.
- **Source**: branch `feature/melodic-soloing-internal-double-barline-recovery-v0.1`, PR #165, merge commit `47cf92c52408e8c1f2d08400f7e8a075d14ff266`
- **Evidence Type**: `logs` / `diagnostic_tables` / `source`
- **Status**: **verified**
- **Artifact Location**: `work/private_gp_quality_audit_v0_1/summary.json`
- **Private-Safe Summary**: `private_input_custom_melodic_soloing` matched notes improved from 56 to 82. Lessons 3–7 are stable. ScoreIR and GPIF note counts are equal at 82.
- **Review Decision**: **approve**
- **Next Required Evidence**: Run a fresh post-milestone private-safe baseline audit from product main to classify the next active blocker across all private fixtures, now that melodic soloing has reached full note coverage.

### EV-006: MusicXML Quadruplet and Quintuplet Preflight Support

- **Claim**: Narrow preflight support for quadruplet (4:3) and quintuplet (5:3) tuplets prevents fatal `musicxml_tuplet_unsupported` errors for Derek Trucks BB King (`private_input_1`), decreasing its unsupported tuplet issue count from 67 to 0 without regressing Lessons 3-7 or Melodic Soloing.
- **Source**: branch `feature/musicxml-tuplet-quintuplet-quadruplet-support-v0.1`, PR #166, commit `191e8204af0145e1a5c2e9e8770483aed592ef1f`
- **Evidence Type**: `logs` / `diagnostic_tables` / `source`
- **Status**: **verified**
- **Artifact Location**: `work/private_e2e_smoke_v0_1/private_input_1/summary.json`
- **Private-Safe Summary**: `private_input_1` unsupported tuplet error count reduced to 0. Lessons 3–7 and Melodic Soloing matched counts are perfectly stable.
- **Review Decision**: **approve**
- **Next Required Evidence**: Address the remaining fatal `musicxml_unbalanced_backup_forward` (backup-forward cursor drift) timing preflight blocker for `private_input_1`.

### EV-007: MusicXML Backup/Forward Cursor Drift Investigation

- **Claim**: The fatal `musicxml_unbalanced_backup_forward` blocker in `private_input_1` is caused by minor underflow in OMR-exported measures (e.g. stopping at 45 instead of 48 divisions), which combines with standard multi-staff backup/forward elements to create a false global parsing cursor mismatch. A narrow timing remediation can safely downgrade this error to a warning when allow_remediation is active, as per-voice timelines are completely coherent and free of overlaps.
- **Source**: branch `research/musicxml-backup-forward-cursor-drift-v0.1` in `score2gp-agentops`
- **Evidence Type**: `logs` / `diagnostic_tables`
- **Status**: **verified**
- **Artifact Location**: `projects/score2gp/research/musicxml-backup-forward-cursor-drift-v0.1.md`
- **Private-Safe Summary**: Cursor drift analyzed across all 15 measures. Deltas range from -1 to -201 divisions. No backup-before-zero, forward-after-end, or same-voice overlaps are present. Lessons 3-7 and Melodic Soloing custom fixtures use perfectly balanced backups with 0 unbalanced measures.
- **Review Decision**: **approve**
- **Next Required Evidence**: Implement and verify the recommended timing remediation task in the product repository under branch `feature/musicxml-backup-forward-remediation-v0.1`.

### EV-010: MusicXML Grace Note Support

- **Claim**: MusicXML grace notes are now parsed, deduplicated between notation and TAB voices, compiled as zero-duration pre-host events, aligned to PDF candidates, and serialized in stable event order before host notes. This increased private_input_1 from 137 / 153 matched candidates to 153 / 153, reducing unmatched PDF candidates from 16 to 0 without regressing Lessons 3–7 or Melodic Soloing.
- **Source**: branch `feature/grace-note-support-v0.1`, PR #170, merge commit `3c1941d5c8166ef3443367102ce6b25f1bd8dfef`
- **Evidence Type**: `source` / `tests` / `private-safe audit`
- **Status**: **verified**
- **Artifact Location**: `projects/score2gp/runs/2026-06-05-musicxml-grace-note-support-v0.1`
- **Private-Safe Summary**: `private_input_1` matched notes improved from 137 to 153, and unmatched PDF candidates reduced from 16 to 0. Lessons 3–7 and Melodic Soloing custom fixtures remain stable.
- **Review Decision**: **approve**
- **Next Required Evidence**: Run a fresh post-grace-note active-blocker audit from product main to determine the next highest-value project task now that private_input_1 has reached full candidate coverage.
