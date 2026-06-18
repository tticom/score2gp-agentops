# Feature: Real-input whole-note recognition acceptance for mixed notation/tab source

## Repository
tticom/score2gp

## Goal
Make Score2GP recognise the visible whole note in a real mixed notation/tab source, or prove exactly why the current approach cannot do so and pivot.
The bounded internal whole-note candidate pipeline from PR #296 and PR #297 is proven only for generated fixtures; real-score acceptance remains unproven.

## Progress Baseline
* PR #296 proved whole-note staff association and staff-position indexing only on clean generated vector fixtures.
* PR #297 proved bounded intermediate whole-note representation only from those generated fixture candidates.
* Neither PR proves whole-note recognition on real mixed notation/tab sources.
* The user-provided real mixed notation/tab example remains the active blocker because the visible whole note is not recognised.

## Incremental Progress Check
* The next task must produce new decision-useful evidence or verified capability on the real mixed notation/tab input.
* It must not merely repeat generated fixture success from PR #296 or PR #297.
* Progress is proven only by identifying the exact real-input pipeline failure stage and either:
  * implementing a bounded verified fix after architecture approval; or
  * producing a verified stop/pivot decision.
* Duplicate/no-progress result: rerunning synthetic fixtures, adding another internal helper, or producing a report that does not change the real-input readiness/blocker state.

## Scope
* Work in `tticom/score2gp`.
* Use the original PDF export if available, otherwise use the supplied screenshot as local-only diagnostic input.
* Run a pipeline-stage diagnosis first to determine where the visible whole note is lost.

## Authorised Workflow
The task must explicitly follow this loop:
Requirement → Architect real-input diagnosis/research → Reviewer architecture verification → Developer implementation only if authorised → Reviewer implementation conformance review → PR readiness review.

The Architect stage must choose exactly one outcome:
* Outcome A: current vector path is viable for the supplied real mixed notation/tab input, with a bounded implementation fix identified.
* Outcome B: current vector path is not viable for this input, but another bounded approach is viable.
* Outcome C: no viable path is identified; no Developer implementation is authorised.

The Reviewer architecture verification stage must approve or reject the Architect outcome before Developer implementation begins.
If Outcome A or B is not verified by Reviewer, Developer work must stop.
Do not authorise code changes merely because the executor believes the vector path is viable.

## Non-Goals
* Do not create another synthetic-only internal helper task.
* Do not commit private/copyrighted artifacts (PDFs, screenshots) unless explicitly authorised.
* Do not authorise GP export yet.
* Do not authorise pitch naming as the main goal.
* Do not claim real-score whole-note recognition is solved unless this example passes.
* Do not claim raster recognition works unless actually implemented.

## Required Pre-flight Checks
* Confirm PR #296 and PR #297 are merged.
* Confirm the real mixed notation/tab source is available locally.

## Required Validation
* Diagnostic output or test evidence proving the outcome.
* `git diff --check`
* `git diff --stat`
* `git status --short`
* `git status --ignored`
* `find . -path "./.git" -prune -o -type f -size +10M -print`

## Acceptance Criteria
* The pipeline either successfully extracts the whole note in the real mixed input, or a bounded architectural decision proves why the current approach fails.
* The Architect and Reviewer architecture stages are verified.
* No private or unsafe artifacts are committed.
* No product implementation is done unless a bounded fix is identified and verified by a Reviewer.

## Stop Conditions
Stop and report if:
* The original PDF or local file path is required but not supplied by the user.
* Private artifacts would be touched or committed.
* Broad product implementation/ML training would be needed without a focused fix.
