# Feature: Real-input whole-note recognition acceptance for mixed notation/tab source

## Repository
tticom/score2gp

## Goal
Make Score2GP recognise the visible whole note in a real mixed notation/tab source, or prove exactly why the current approach cannot do so and pivot.
The internal representation pipeline (PR #296, PR #297) is complete for generated fixtures, but real-score acceptance is the missing requirement.

## Scope
* Work in `tticom/score2gp`.
* Use the original PDF export if available, otherwise use the supplied screenshot as local-only diagnostic input.
* Run a pipeline-stage diagnosis first to determine where the visible whole note is lost.
* Implement a bounded fix only if the current vector path is proven viable.
* If the vector path is not viable (e.g. raster source), produce a bounded architecture decision proving why and what replacement path is required.
* Produce acceptance test or local acceptance evidence proving the visible whole note is recognised if a fix is implemented.
* Stop/pivot if the current vector path cannot support the source type.

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
* No private or unsafe artifacts are committed.
* No product implementation is done unless a bounded fix is identified.

## Stop Conditions
Stop and report if:
* The original PDF or local file path is required but not supplied by the user.
* Private artifacts would be touched or committed.
* Broad product implementation/ML training would be needed without a focused fix.
