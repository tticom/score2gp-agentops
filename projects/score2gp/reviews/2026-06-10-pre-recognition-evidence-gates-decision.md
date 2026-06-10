# Pre-Recognition Evidence-Quality Gates Decision

## Verified Prerequisites
- Governance PR #113 is merged, requiring a governance-only decision on evidence-quality gates and corpus review before authorising any semantic product recognition.

## Purpose
This note establishes the specific review criteria required to evaluate the raw raster diagnostic candidates (`treble_clef_candidate`) against the private corpus. It defines the quality gates that must be cleared before these candidates can be promoted into `ScoreIR` or trusted for musical semantic parsing.

## Required Corpus Review Actions
A subsequent evaluation phase must be conducted by reviewing the locally generated, untracked smoke-script JSON output. The evaluation must answer the following questions against a ground truth established explicitly by human-reviewed private fixture expectations or fixture-level manual review:
1. **False Positive Rate:** How often do the existing proportional heuristics incorrectly flag non-clef objects (e.g., dense clusters of notes, text, or noise) as `treble_clef_candidate`?
2. **False Negative Rate:** How often do legitimate treble clefs fail the proportional checks due to fragmentation, unusual fonts, or scanning artifacts?
3. **Staff-line Exclusion:** Are the bounding boxes strictly enclosing the clef symbols, or do they erroneously encompass the staff lines themselves, leading to false positives on blank staves?

## Evidence-Quality Gates
Task 63 must produce a governance review table listing fixture/page/staff, expected opening-symbol status, observed summary label, false-positive/false-negative classification, and notes.

Task 63 does not decide recogniser readiness. A subsequent governance PR must define explicit numeric thresholds before authorising semantic promotion. Any secondary validation gates (such as an ML-based shape classifier, strict contour analysis, or template matching) are possible later research/design tasks only, not authorised by Task 62 or Task 63.

## Prohibitions
The following product implementation actions remain **strictly prohibited**:
- Authorising or emitting `ScoreIR` payloads containing recognised clefs.
- Using `treble_clef_candidate` bounding boxes to infer pitch, key signatures, or time signatures.
- Modifying product logic to perform vector/raster fusion.
- Modifying product logic to perform OCR on the diagnostic boundaries.
- Adding product logic to interpret diagnostic candidates as semantic music objects.

## Recommended Next Task
The explicitly recommended next task is:
**Task 63 — Execute raster diagnostics corpus review against private fixtures**
*(Note: Task 63 is a read-only evaluation task. It does not authorise product recognition.)*
