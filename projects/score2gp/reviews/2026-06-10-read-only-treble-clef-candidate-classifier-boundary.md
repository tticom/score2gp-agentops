# Read-Only Treble-Clef Candidate Classifier Boundary

## Verified Prerequisites
* Product PR #235 (`feat(pdf): add raster treble clef staff diagnostics`) is merged.
* Governance PR #106 (`docs(score2gp): define raster opening-symbol diagnostics consumption boundary`) is merged, confirming that raster diagnostics are evidence only.
* Governance PR #105 is closed and cordoned off as historical negative evidence.

## Purpose
This note defines the boundaries for a future diagnostic-only classifier. The classifier's role is to inspect raw candidate evidence emitted by the raster path and categorize it as a treble-clef-like candidate or not, without inferring full musical semantics or emitting `ScoreIR`.

## Allowed Inputs
The future classifier may strictly consume existing diagnostic evidence only:
* Staff vertical bounds (`y_coords`), staff horizontal span (`x0` / `x1`), and `spacing`.
* Candidate bounding box geometry (`raster_opening_symbol_candidate.bbox`), `width`, and `height`.
* Render scale and threshold metadata (where available).
* No OCR implementation is authorised.
* No new image recognition pipeline outside the authorised raster diagnostic evidence is permitted.
* No vector/raster evidence fusion unless explicit fallback or precedence rules are defined in a later governance task.

## Allowed Outputs
The classifier must output a read-only diagnostic result only, preferably a tri-state label or equivalent (e.g., `treble_clef_candidate`, `not_treble_clef_candidate`, `unknown`).
* It must not emit `ScoreIR`.
* It must not emit a recognised clef object into the music model.
* It must not mutate existing staff diagnostics unless designed as a safely appended read-only diagnostics field.

## Explicit Non-Goals
* No semantic recognition of clefs.
* No inference of pitch, rhythm, key signature, time signature, notes, rests, voices, or musical semantics.
* The diagnostic label does not imply the document parsing is "complete" or production-ready.

## Candidate Classifier Boundary
The boundary separates purely spatial and proportional pixel candidate boundaries from the strict structural requirements of a real musical ScoreIR. The classifier operates strictly inside the diagnostics domain and provides an intermediate categorical label based on geometric heuristics rather than deep musical synthesis.

## Evidence Requirements
* Empirical validation against real, existing diagnostics is required.
* The safe default when evidence is weak, missing, ambiguous, or outside expected bounds must be `unknown`.
* Guessing based on assumptions is prohibited.

## Suggested Classifier Criteria (Non-Binding)
A later implementation task may design the classifier using spatial ratios such as:
* Candidate height relative to staff spacing.
* Candidate width relative to staff spacing.
* Vertical overlap/span relative to the five staff lines.
* Horizontal location relative to the staff starting point (`x0`).
* Presence within the left-margin search region.
*These criteria are heuristics for classification, not sufficient to establish true semantic recognition.*

## Required Validation for a Later Implementation Task
A future implementation task must prove:
* It consumes real raster diagnostics directly from the existing pipeline.
* It includes tests backed by existing authorised fixtures or explicitly authorised new fixtures.
* It preserves `None` (not run) versus `[]` (run but none found) semantics.
* It gracefully falls back to `unknown` instead of inventing data.
* It emits strictly diagnostic results, not ScoreIR.
* It does not infer or fabricate full music semantics.
* It does not synthesize fake staff geometry or fake bounding boxes.
* It explicitly preserves the existing vector diagnostics behavior untouched.

## Privacy and Artifact Rules
Private fixtures are permitted only when explicitly authorised and documented. No new private PDFs or fixtures are relitigated or introduced in this governance boundary note. No generated artifacts, screenshots, logs, or debug dumps may be committed.

## Stop Conditions
Agents working under this boundary must stop and report if:
* The classification relies on unverified or missing private fixtures.
* Implementing the classifier requires modifying existing vector components or product schemas beyond an added diagnostic field.
* They are prompted to guess an output rather than gracefully failing to `unknown`.

## Candidate Next Task
* **Task 54 — Implement read-only treble-clef candidate classifier diagnostics**
