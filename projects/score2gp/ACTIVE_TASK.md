# Diagnostic: Fixture Admission and Baseline Classification for Rest/Tab-only Inputs v0.1

## Repository
tticom/score2gp

## Goal
Decide whether `QuarterRestThenNotes.pdf`, `TabOnlySingleNote.pdf`, and `TabOnlyTwoNotes.pdf` can become safe, admissible diagnostic fixtures, and what they prove or block, without authorising rest or tab-only implementation yet.

## Progress Baseline
* Product PR #316 merged, providing deterministic sequential event mapping for multiple already-recognised notation candidates in simple generated public notation fixtures.
* The capability handles sorting, onset_ticks accumulation, and enforcing the 1-bar cap, but explicitly without rest or tab-only support.

## Incremental Progress Check
* The next task must produce decision-useful diagnostic evidence for the three new PDFs.
* Progress is proven when the governance PR updates `ACTIVE_TASK.md` and adds a decision/governance record that changes the active blocker from deterministic sequencing to fixture admission/baseline classification for rest/tab-only inputs.

## Hypothesis
The three candidate PDFs can be classified safely and usefully into one of:
* admissible public diagnostic fixture,
* not safe/admissible as fixture,
* safe for local-only diagnostic but not commit,
* not useful for current pipeline.

## Explicit Scope & Acceptance
* Inspect the three PDFs: `QuarterRestThenNotes.pdf`, `TabOnlySingleNote.pdf`, and `TabOnlyTwoNotes.pdf`.
* Do not commit them unless explicitly proven safe/admissible and the task authorises it.
* The diagnostic must evaluate the following metrics for each file:
  * file safety/admissibility outcome;
  * whether the current production recognition path runs without crashing;
  * whether notation candidates are produced;
  * whether rest-like symbols are observed or absent;
  * whether tab-only staff geometry/string evidence is detected;
  * whether any ScoreIR/GP output is produced;
  * exact warning/error/blocker reason;
  * whether result enables rest-aware sequencing, tab-only extraction architecture, return to architecture, or stop/pivot.

## Constraints and Preservation
Explicit non-goals:
* Do not modify product code.
* Do not authorise rest implementation.
* Do not authorise tab-only implementation.
* Do not add or commit the PDFs.
* Do not create generated output fixtures (GP files, etc.).
* Do not claim support for rests or tab-only input.

## Pass/Fail Thresholds
* **Pass:** The diagnostic provides the full evaluation metrics (safety, run result, evidence summary, blocker classification, recommended next task) for all three files.
* **Fail:** The diagnostic only captures logs, creates artifacts without forcing a decision, or only says "does not work."

## Stop/Pivot Conditions
* If files are unsafe/private/not admissible, stop fixture admission and request safe public/generated replacements.
* If rest notation is detected but unsupported, authorise rest-aware sequencing architecture or implementation only if evidence is sufficient.
* If tab-only input lacks necessary geometry/string evidence, return to architecture for tab-only extraction.
* If tab-only evidence is present and production path exposes it, authorise a narrow tab-only diagnostic/implementation task.
* If none of the files can be used safely, stop and request new generated public fixtures.
