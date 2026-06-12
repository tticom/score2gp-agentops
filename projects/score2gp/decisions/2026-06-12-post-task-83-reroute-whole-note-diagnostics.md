# Governance Decision: Post-Task 83 Reroute to Whole-Note Diagnostics

## Date
2026-06-12

## Context
Product PR #248 (Task 83) was successfully merged:
- Merge commit SHA: 57f77a813c6fc8b7a5032b467b89a2ed904af197
- Final head SHA: 546402938d7838383796f70127caff02a57fa6f8
- Files changed:
  - `.github/workflows/raster-gate-advisory.yml`

Task 83 added an advisory CI workflow for the raster diagnostics gate report. The gate report is now integrated safely, proving both PASS and REVIEW subprocess gates without enforcing arbitrary thresholds on branch protection.

## Strategic Correction
The workflow has spent too long on gates, reports, CI, and governance hygiene. Process-improvement work is now explicitly **paused**. The next useful product-visible direction is whole-note candidate diagnostics, directly addressing the core goal of expanding the system's music recognition capabilities.

## Decision
We authorise **Product Task 85: read-only whole-note candidate diagnostics**.

### Task 85 Requirements
Task 85 must:
- Add diagnostic-only whole-note candidate detection.
- Use public synthetic fixtures where needed.
- Expose results through existing diagnostics structures or a small diagnostic script/report.
- Make it possible to run the system against a fixture PDF and see whole-note candidate counts or locations.
- Include regression tests proving:
  - at least one whole-note positive case;
  - at least one negative or non-whole-note case.
- Keep all output diagnostic-only.
- Preserve existing treble-clef/raster gate behaviour unless a directly related test update is required.

### Blocked Actions
Task 85 must not:
- emit ScoreIR;
- emit GP files;
- claim full semantic note recognition;
- infer pitch;
- infer rhythm duration beyond the diagnostic label `whole_note_candidate`;
- infer voices;
- infer measures;
- infer key signatures;
- infer time signatures;
- infer rests;
- infer full notation;
- use OCR;
- require private fixtures;
- commit generated outputs, screenshots, PDFs, GP files, raw JSON dumps, or local scratch artifacts unless explicitly authorised;
- alter unrelated treble-clef gate behaviour;
- update governance records during product implementation unless explicitly asked.
