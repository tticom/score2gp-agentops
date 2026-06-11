# Decision: Task 66 — Next Diagnostic-Only Evidence Path

**Date:** 2026-06-11
**Status:** Accepted
**Context:** Product PR #239 and Governance PR #119

## 1. Task 65 Completion and Available Evidence
Task 65 is complete and has been formally audited. The available evidence now includes:
- Synthetic negative fixtures proving exclusion of blank staves, TAB staves, and noise/text.
- Raster-negative tests successfully verifying that `treble_clef_candidate` is **not** extracted for the negative cases.
- A failure taxonomy documenting existing false negatives for treble clef extraction.
- A post-merge audit explicitly validating that the final product-code change remains strictly diagnostic-only.

## 2. Block on Semantic Promotion
Despite the strong diagnostic foundations laid in Task 65, the current evidence **does not authorise semantic promotion**.
- **Rejected:** Semantic promotion of `treble_clef_candidate` to recognised `clef` objects.
- **Rejected:** ScoreIR emission, GP package generation, or any pitch, rhythm, key signature, note, or musical inference.
- **Rejected:** Vector-based treble clef candidate extraction. This remains blocked unless a subsequent explicit governance decision scopes it properly and proactively prevents vector/raster fusion.

## 3. Selected Next Diagnostic-Only Path
The next task must be strictly diagnostic to further consolidate our baseline confidence before allowing semantic logic to take effect. 

**Decision:** We select a new product Task 67 focused on implementing a **repeatable raster diagnostics gate report**.

### Task 67 Requirements:
- Create or improve a repeatable command/script that reports raster diagnostic gate outcomes over the authorised public/synthetic fixtures.
- The report must output counts for:
  - Blank staves
  - TAB staves
  - Noise
  - Positive private fixtures (if already authorised locally)
  - False positives
  - False negatives
  - Unknowns
- The output of this report should remain ephemeral (terminal stdout) unless a small static expected fixture is explicitly safe and useful to track.
- The task must **not** commit raw JSON dumps, screenshots, rendered images, non-authorised PDFs, GP files, or private material.
- The task must **not** implement semantic recognition, ScoreIR emission, recognised clef objects, OCR, or vector/raster fusion.

## 4. Alternative Paths Considered (Not Selected)
- *Expand negative fixture coverage further:* Rejected because current coverage meets immediate bounds for testing TAB/blank exclusions.
- *Classify the 11 false-negative categories into a machine-readable manifest:* Rejected as secondary to establishing a broad counting harness.
- *Harden raster staff detection against edge cases:* Rejected until the gate report (Task 67) highlights quantitative regressions.
- *Add public-only regression tests for multi-staff suppression risk:* Documented but not selected as the primary goal over the holistic gate report.
