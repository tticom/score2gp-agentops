# Architect Research: Quarter-Rest GP Export Integration v0.1

## Repository
tticom/score2gp

## Goal
To determine if existing GP export can safely handle quarter-rest ScoreIR events sequenced by PR #319, or if an alternate bounded export path is required, without breaking existing note export.

## Progress Baseline
* Product PR #319 merged, providing deterministic sequencing of quarter rest candidates as ScoreIR rest events.
  * PR URL: `https://github.com/tticom/score2gp/pull/319`
  * Head SHA: `d19a149b7d915a737f247891b6be89dfb7a36181`
  * Merge commit: `07b2552e625581771239f3178b24d9c7d25578f8`
  * Merge status: ALREADY MERGED
* Files changed:
  * `src/score2gp/notation_bridge.py`
  * `src/score2gp/quarter_rest_recogniser.py`
  * `tests/test_notation_bridge_quarter_rest_candidate_sequencing.py`
  * `tests/test_deterministic_multinote_sequencing_quarter_rest.py`
  * `tests/test_quarter_rest_recogniser_extraction.py`
* Tests/checks reported: All checks successful
* Verdicts: Implementation conformance approved, PR readiness READY.
* Known non-capability preserved: GP export was explicitly not tested and intentionally excluded.

## Active Blocker
Quarter-rest ScoreIR events exist after sequencing, but GP export handling for rest events has not been verified. The next task must not assume export works.

## Hypothesis
The existing ScoreIR-to-GP export mechanism can be safely extended to emit quarter rest durations without breaking existing multi-note timing, or a bounded alternate strategy is necessary.

## Explicit Scope & Acceptance
* Architecture diagnostic focused ONLY on quarter-rest GP export integration.
* The Architect task must include:
  * Current export path inventory.
  * Where ScoreIR note events are converted into GP output.
  * Whether rest events are represented in the existing ScoreIR/export model.
  * Whether quarter rests require measure/timing validation.
  * Existing tests that cover export timing/duration.
  * Proposed smallest Developer task only if evidence supports it.
  * Clear risks around breaking existing note export behaviour.
* Required Architect outcome: must explicitly select Outcome A, B, or C.

## Constraints and Preservation
Explicit non-goals:
* Do not change product code, tests, or fixtures.
* Do not claim GP export support exists before evidence is provided.
* Do not authorise direct implementation of GP export without architecture research.
* Do not add support for other rest types (whole, half, eighth).
* Do not broaden the task to tab-only export or full notation coverage.
* Do not include private PDFs, GP files, screenshots, generated dumps, logs, or local artifacts.

## Pass/Fail Thresholds
* **Pass:** The architecture diagnostic is approved by Reviewer if it explicitly chooses exactly one of:
  * Outcome A: Existing GP export path can safely export quarter-rest ScoreIR events with a narrow Developer implementation task.
  * Outcome B: Existing GP export path cannot safely handle quarter-rest events as-is, but a bounded alternate export approach is viable.
  * Outcome C: No safe bounded export path is currently viable; stop and return to supervisor.
* **Fail:** The diagnostic fails if it assumes export works without research, proposes changing existing note export without mitigation, authorises Developer work directly, or relies on unbounded implementation tasks.

## Stop/Pivot Conditions
* If the existing export model structurally prohibits rest events entirely without an unbounded rewrite, stop and pivot to Outcome C.
* If general rest support (handling arbitrary durations) is required to emit a single quarter rest, stop.
