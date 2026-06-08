# Post-Schema-Snapshot Product Backlog Review

**Date:** 2026-06-08  
**Reviewer:** ChatGPT

## Context

Product PR #203 is merged. The product baseline for the next queue segment is:

`0b73bd90898bc1f5a1bda6f5e61920d1e952c7f9`

This governance update adds a long, ordered, bounded product backlog after the diagnostics schema snapshot gate. The queue deliberately stays inside geometry diagnostics, fixture coverage, schema contracts, geometry candidate models, candidate extraction, and diagnostic reporting.

A later human design discussion added a longer playability-oriented recognition roadmap. That roadmap is recorded separately in:

`projects/score2gp/reviews/2026-06-08-playability-oriented-recognition-backlog.md`

The roadmap is intentionally not treated as immediate permission to implement broad musical semantics. It records the future direction: visual evidence capture, candidate grouping, interpretation, reconciliation, recovery search, playable export, and human-facing reporting.

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

## Playability roadmap summary

The roadmap records Tasks 36-100 as planned future work, grouped by priority:

- Priority 0: benchmark observations and playability target.
- Priority 1: structural and layout recognition.
- Priority 2: note-event evidence layer.
- Priority 3: duration and rhythm interpretation.
- Priority 4: pitch, TAB, simultaneity, and chords.
- Priority 5: guitar articulations and performance techniques.
- Priority 6: dynamics, expression, text, and navigation.
- Priority 7: reconciliation, recovery, and export.
- Priority 8: long-term completeness coverage.

The roadmap is shaped by observed current failures: whole/full-bar duration loss, double-barline section breaks, terminal crotchet-after-quavers duration handling, and same-x stacked/chord event recognition.

## Deferred boundaries

The following remain explicitly not approved for immediate implementation by this PR:

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
