# Quarter-Rest-Aware Sequencing Architecture for QuarterRestThenNotes v0.1

## Repository
tticom/score2gp

## Goal
To determine where and how the extracted `quarter_rest_candidate` objects should be consumed in the deterministic sequencing pipeline, and explicitly map the required event representation for `QuarterRestThenNotes.pdf` without breaking existing note sequencing.

## Progress Baseline
* Product PR #318 merged, providing extraction-only quarter rest candidate recognition from vector flag fragments.
  * PR: `https://github.com/tticom/score2gp/pull/318`
  * Title: `feat: extract quarter rest candidates from vector fragments`
  * Merge commit: `1c42c7c76bbc2e8e462553e2330e4a32102a0158`
  * Head SHA: `36ead2853f4841947229abecbd3aa7d38c8b70d2`
* New merged product capability:
  * recognises `quarter_rest_candidate` from vector fragments;
  * filters note/clef overlaps;
  * partitions by staff context before clustering;
  * preserves `staff_index`.
* Explicit non-capabilities:
  * no rest sequencing;
  * no rest export;
  * no ScoreIR rest event integration;
  * no tab-only support;
  * no non-quarter rest extraction.

## Active Blocker
`QuarterRestThenNotes.pdf` can now emit a quarter_rest_candidate, but the deterministic sequencing/bridge path does not yet consume that candidate as a rest-duration event. Therefore rest-aware timing is not proven.

## Hypothesis
`QuarterRestThenNotes.pdf` extracted candidates can be safely integrated into the deterministic multi-note sequencing pipeline either as intermediate events or ScoreIR events, or current sequencing assumptions prevent safe integration.

## Explicit Scope & Acceptance
* Architecture diagnostic focused ONLY on rest-aware deterministic sequencing.
* Metrics to report:
  * Where in the pipeline should `quarter_rest_candidate` be consumed?
  * Is it compatible with existing deterministic note sequencing from PR #316?
  * Should it become an intermediate event before ScoreIR, a ScoreIR rest event, or a bridge input object?
  * What exact event sequence should `QuarterRestThenNotes.pdf` produce?
  * What tests would prove rest timing without overclaiming export support?
  * Can implementation remain bounded without general rest support?
* Required Architect outcome: must explicitly select Outcome A, B, or C (see Pass/Fail Thresholds).

## Constraints and Preservation
Explicit non-goals:
* implement code;
* modify tests;
* modify export;
* modify CLI;
* support half/eighth/whole rests;
* support tab-only scores;
* train a model;
* add fixtures;
* generate or commit GP output;
* claim end-to-end rest conversion.

## Pass/Fail Thresholds
* **Pass:** The architecture diagnostic is approved by Reviewer if it explicitly chooses exactly one of:
  * Outcome A: Quarter-rest-aware sequencing is viable using current `quarter_rest_candidate` evidence and a concrete deterministic approach.
  * Outcome B: Current evidence is insufficient, but another bounded approach is viable and should be researched next.
  * Outcome C: No viable rest-aware sequencing path is proven; no Developer work authorised.
* **Fail:** The diagnostic fails if it:
  * proposes implementations outside architecture scope;
  * claims rest export support exists;
  * authorises Developer directly without Reviewer approval.

## Stop/Pivot Conditions
* If rest-aware timing fundamentally breaks note sequencing and cannot be bounded, stop and pivot.
* If sequencing requires spacing inference, stop.
* If general rest support is needed, stop.
