# Raster Diagnostics Reporting Merge and Next Boundary

## Verified Prerequisites
- Product PR #238 is merged, safely implementing stdout JSON reporting of the diagnostics summary in the private smoke script.
- Governance PR #112 is merged, establishing the safe boundary rules for that reporting.

## Purpose
This note records the successful and compliant implementation of Task 60. It also defines the next smallest safe boundary, preventing premature semantic recognition.

## Prohibitions
Before any code is written that attempts to promote `treble_clef_candidate` into a fully recognised clef, emits `ScoreIR`, or parses pitch and rhythm, a deliberate governance decision must be made regarding the evidence quality.

The following product implementation actions remain **strictly prohibited**:
- Authorising or emitting `ScoreIR` payloads containing recognised clefs.
- Using `treble_clef_candidate` bounding boxes to infer pitch, key signatures, or time signatures.
- Modifying product logic to perform vector/raster fusion.
- Modifying product logic to perform OCR on the diagnostic boundaries.

## Defining the Pre-Recognition Boundary
The current state provides raw raster diagnostics through an ephemeral smoke script. Jumping straight into semantic recognition is a high-risk leap.

The next governance step must evaluate the current diagnostic output against the private test corpus to determine if the existing proportional heuristics and any future explicitly authorised structural checks are sufficient, or if further validation gates (like machine learning classifiers, or additional structural checks) are required before allowing semantic product logic to trust the diagnostic candidates.

## Recommended Next Task
The explicitly recommended next task is:
**Task 62 — Decide pre-recognition evidence-quality gates and corpus review criteria**
*(Note: Task 62 is a governance-only task. It does not authorise product implementation.)*
