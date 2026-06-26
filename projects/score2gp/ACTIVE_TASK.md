# Active Task: Candidate-to-Measure Assignment Architecture Decision

## Repository
tticom/score2gp

## Current Governance State
Product baseline PR #326 merged.
Diagnostic identity baseline PR #327 merged.

Current evidence:
- measure-grid regions exist;
- candidate geometry exists;
- nullable heuristic staff/system identity exists;
- missing context yields `None`;
- identity is heuristic, not true extraction-context preservation.

Developer implementation: Blocked
Full candidate-to-measure assignment: Blocked
Next authorised role: Architect
Required next review after Architect research: Reviewer architecture verification

## Active Task
Architect research/decision on candidate-to-measure assignment viability.

The Architect must evaluate whether candidate-to-measure assignment can be safely designed using:
- `MeasureGridDiagnostics` from PR #326;
- nullable candidate `page_index`, `system_index`, and `staff_index` from PR #327;
- existing candidate geometry, especially `bbox`, `width`, `height`, `aspect_ratio`, and `stem_bbox`;
- approved public fixtures only.

See `decisions/2026-06-25-post-pr327-staff-identity-diagnostic-completion.md` for full context and Outcome A/B/C requirements.

## Active Blocker
Can the system safely and deterministically assign notation candidates to measure regions using PR #326 measure-grid diagnostics and PR #327 nullable heuristic staff/system identity, without relying on false identity, overclaiming heuristic evidence, or introducing semantic note/rhythm recognition?

## Explicit Non-Authorisations
These remain explicitly **blocked**:
- Developer implementation;
- candidate-to-measure assignment implementation;
- rhythm/duration inference;
- whole-note recognition;
- note/rest semantic recognition;
- ScoreIR changes;
- GP export changes;
- MusicXML changes;
- OCR;
- ML/training;
- tab-only timing changes;
- private fixture usage;
- generated artifact commits.
