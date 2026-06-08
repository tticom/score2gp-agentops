# Post-Schema-Snapshot Product Backlog Review

**Date:** 2026-06-08  
**Reviewer:** ChatGPT

## Context

Product PR #203 is merged. The product baseline for the next queue segment is:

`0b73bd90898bc1f5a1bda6f5e61920d1e952c7f9`

This governance update adds a long, ordered, bounded product backlog after the diagnostics schema snapshot gate. The queue deliberately stays inside geometry diagnostics, fixture coverage, schema contracts, geometry candidate models, candidate extraction, and diagnostic reporting.

## Verified premise

- Product PR #203: `test(pdf): add schema snapshot gate for staff geometry diagnostics`
- Product PR #203 merge commit: `0b73bd90898bc1f5a1bda6f5e61920d1e952c7f9`
- Product PR #203 merged at: 2026-06-08T13:35:38Z

## Queue changes

- Earlier Tasks 1-6 are recorded as complete on the post-#203 baseline.
- Task 7 is set as the active task.
- Tasks 8-35 are added as approved or conditionally approved queue items.
- Conditional tasks remain explicitly gated by their written prerequisites and stop conditions.
- Human merge remains required for every PR.

## Deferred boundaries

The following remain explicitly not approved:

- pitch inference
- duration inference
- clef inference
- key signature inference
- voice assignment
- rhythm interpretation
- ScoreIR event generation from standard-staff glyphs
- scanned/OCR PDF handling
- real/private/copyrighted PDF fixtures

## Known limitations

This review records the control-plane update only. It does not validate product tests locally and does not modify the product repository.

The queue should be merged before agents start Task 7, so agents have a durable control-plane source of truth before continuing.
