# 2026-06-25 Post-PR #327: Staff Identity Diagnostic Completion

## Context
Score2GP has now completed the diagnostic evidence loop for candidate staff/system identity.

Relevant baseline chain:

- Product PR #326 merged measure-grid diagnostics.
  - Merge commit: `7565e751e0dea624a209aeb4233373338296262a`

- Architecture PR #214 approved Outcome B.
  - Merge commit: `c3b5d3bfad5d1a5c01f4819dd7730b3127726cfc`
  - Conclusion: measure-grid is useful, but notation candidates lacked staff/system identity.

- Governance PR #215 authorised a narrow Developer diagnostic-evidence task.
  - Merge commit: `752a6756bb76321d596d0039168dab727ec726d8`

- Product PR #327 implemented nullable heuristic staff/system identity on notation candidate diagnostics.
  - PR: `https://github.com/tticom/score2gp/pull/327`
  - Head SHA: `9f30bbd741115d93b59f83b00eae082da2522c4c`
  - Merge commit: `963bbf393bc5e619e30d82ebff22652c1a94615a`
  - Merged at: `2026-06-25T21:22:32Z`

## Verified state
PR #327 added diagnostic-only identity fields to notation candidate diagnostics:
- `page_index`
- `system_index`
- `staff_index`

The fields are nullable and default to `None`, avoiding false-positive `1,1,1` identity.

The identity assignment is explicitly a nearest-staff-center geometric heuristic, not true extraction-context preservation.

Candidate-to-measure assignment was not added.

ScoreIR and GP export were not changed.

Full notation conversion remains unproven.

## Active blocker
Score2GP now has:
- measure-grid regions from PR #326;
- nullable heuristic staff/system identity on notation candidates from PR #327.

But it is still not known whether this is enough to safely assign notation candidates into measure regions.

The active blocker is:
Can the system safely and deterministically assign notation candidates to measure regions using PR #326 measure-grid diagnostics and PR #327 nullable heuristic staff/system identity, without relying on false identity, overclaiming heuristic evidence, or introducing semantic note/rhythm recognition?

## Goal
Update governance state so the next authorised task is Architect research/decision on candidate-to-measure assignment viability.

The Architect must determine whether PR #326 + PR #327 evidence is sufficient, insufficient, or not viable.

## Required Architect task
The Architect must evaluate whether candidate-to-measure assignment can be safely designed using:
- `MeasureGridDiagnostics` from PR #326;
- nullable candidate `page_index`, `system_index`, and `staff_index` from PR #327;
- existing candidate geometry, especially `bbox`, `width`, `height`, `aspect_ratio`, and `stem_bbox`;
- approved public fixtures only.

The Architect must choose exactly one:

### Outcome A
Candidate-to-measure assignment architecture is viable using current measure-grid and nullable heuristic identity evidence.

Outcome A is allowed only if the Architect provides:
- a deterministic assignment rule;
- explicit treatment of `None` identity;
- explicit treatment of heuristic identity limitations;
- handling for candidates near measure boundaries;
- handling for multi-staff systems;
- handling for ledger-line candidates;
- handling for double/repeat adjacent barlines already collapsed by PR #326;
- fixture-level evidence;
- failure/ambiguity rules;
- tests required before Developer implementation.

Outcome A does not itself authorise Developer implementation. Reviewer architecture verification must approve it first.

### Outcome B
Current evidence is useful but insufficient.

The Architect must define the smallest additional diagnostic evidence needed before implementation can be authorised.

Examples might include:
- true extraction-context candidate grouping;
- candidate ambiguity scores;
- staff-distance thresholds;
- nearest-staff confidence diagnostics;
- public fixture with real multi-staff note candidates;
- explicit identity source metadata.

### Outcome C
Current raster/vector diagnostic path is not viable for candidate-to-measure assignment.

No Developer work is authorised. Pivot is required.

## Non-goals
Do not authorise:
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
