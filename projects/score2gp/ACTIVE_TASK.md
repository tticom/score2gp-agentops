# Rest-Aware Sequencing Architecture Diagnostic for QuarterRestThenNotes v0.1

## Repository
tticom/score2gp

## Goal
To determine if `QuarterRestThenNotes.pdf` exposes enough structural rest evidence to define a deterministic rest-aware sequencing approach, or if rest work must return to architecture/pivot. Tab-only work is explicitly deferred to a separate active task.

## Progress Baseline
* Product PR #316 merged, providing deterministic multi-note sequencing.
* Governance PR #194 authorised fixture baseline diagnostic.
* Product PR #317 admitted exactly three public diagnostic PDFs.
* Prior diagnostic found `QuarterRestThenNotes.pdf` produces note candidates but lacks rest-aware timing/representation.
* Prior diagnostic found tab-only files expose text/fret evidence but staff geometry is missing.

## Active Blocker
`QuarterRestThenNotes.pdf` cannot yet be converted with rest-aware timing because the pipeline has not proven structural rest detection or a rest-event representation/mapping strategy.

## Hypothesis
`QuarterRestThenNotes.pdf` either exposes enough structural rest evidence to define a deterministic rest-aware sequencing approach, or it does not and rest work must return to architecture/pivot.

## Explicit Scope & Acceptance
* Architecture diagnostic focused ONLY on `fixtures/public/generated_simple/simple/QuarterRestThenNotes.pdf`.
* Metrics to report:
  * whether rest-like graphical/textual evidence is present in parsed PDF structures;
  * whether current candidate extraction captures rest-like evidence anywhere;
  * whether note candidates before and after the rest are detected and ordered;
  * whether a rest duration can be inferred from spatial/timing context without hardcoded fixture hacks;
  * whether a rest event representation exists or must be introduced;
  * whether onset mapping can represent the gap without corrupting note order;
  * whether implementation can be bounded to this fixture class;
  * exact blocker if no viable path exists.
* Required Architect outcome: must explicitly select Outcome A, B, or C (see Pass/Fail Thresholds).

## Constraints and Preservation
Explicit non-goals:
* Do not authorise rest implementation yet.
* Do not authorise tab-only implementation.
* Do not authorise tab-only architecture in the same active task.
* Do not claim rest support exists.
* Do not claim tab-only support exists.
* Do not add or commit PDFs, GP files, screenshots, JSON reports, dumps, logs, or local artifacts.
* Do not modify the product repo.

## Pass/Fail Thresholds
* **Pass:** The architecture diagnostic is approved by Reviewer if it produces:
  * a concrete rest evidence map;
  * a proposed event/timing model or a justified rejection;
  * exact files/functions likely affected;
  * exact tests/fixture assertions needed for implementation;
  * explicitly chooses exactly one of: Outcome A (rest-aware sequencing is viable using current parsed evidence and a concrete deterministic approach), Outcome B (current parsed evidence is insufficient, but another bounded approach is viable and should be researched/implemented next), or Outcome C (no viable rest-aware approach is proven; no Developer work authorised);
  * a yes/no Developer authorisation decision.
* **Fail:** The diagnostic fails if it:
  * relies only on visual inference;
  * says "add rest support" generically;
  * lacks a measurable implementation approach;
  * does not classify evidence as fact/inference/hypothesis/unknown;
  * does not choose Outcome A/B/C.

## Stop/Pivot Conditions
* If rest evidence is not structurally detectable, return to architecture or request a generated fixture with clearer rest primitives.
* If rest duration cannot be inferred deterministically, stop implementation.
* If the fix requires broad OMR/model/OCR work, stop and escalate.
* If implementation would affect tab-only or chord/voice handling, stop.
* If product branch is dirty or tests fail unexplained, stop.
