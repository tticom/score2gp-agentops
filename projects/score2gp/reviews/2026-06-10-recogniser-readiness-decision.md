# Governance Decision: Raster Treble Clef Recogniser Readiness

## Context and Evidence Interpretation
Task 63 completed the read-only evidence collection for raster diagnostics against the private corpus.
The review demonstrated the following:
- **True Positives:** 253
- **False Positives:** 0
- **False Negatives:** 11
- **True Negatives:** 3
- **False Positive Rate:** 0%
- **False Negative Rate:** ~4.1%

Staff-line exclusion was successful in the reviewed corpus. However, the evidence interpretation reveals critical gaps:
- 0 false positives is promising but not enough by itself to authorise semantic promotion.
- Only 3 true negatives is too small to prove robust staff-line/TAB/noise exclusion.
- 11 false negatives may be acceptable for a conservative diagnostic candidate detector, but not as proof of recogniser readiness.

## Numeric and Qualitative Threshold Gates
The following gates must be met before any semantic recognition can be authorised:

1. **False-positive tolerance:**
   - 0 false positives required in the reviewed gate corpus before any later semantic-recognition proposal.
   - Any false positive against empty staff, TAB staff, lyrics/text, staff lines, barlines, or noise blocks semantic promotion.

2. **False-negative tolerance:**
   - For diagnostic candidate detection, the current 11/264 false negatives is acceptable only as a conservative evidence signal.
   - For semantic recognition readiness, false-negative tolerance must be revisited with broader corpus evidence and failure classification.

3. **Staff-line exclusion:**
   - Empty staves, TAB staves, and staff-line-only evidence must remain `unknown`.
   - Current 3 true negatives is insufficient as a full exclusion proof; more negative examples are required.

4. **Minimum corpus coverage:**
   - Keep Task 63 as useful evidence.
   - Require a larger and more balanced gate set before semantic promotion, including more blank staves, TAB staves, dense notation, merged barline cases, unusual fonts, multi-staff pages, and non-clef opening symbols.

## Readiness Decision
Semantic promotion is **blocked**.
Current evidence is sufficient to continue diagnostic-only exploration.
Current evidence is not sufficient to authorise recognised clef objects or ScoreIR emission.

## Additional Evidence Required
Before semantic promotion is reconsidered, the following must be provided:
- More negative fixtures.
- Explicit TAB/blank/noise cases.
- Failure taxonomy for false negatives.
- A repeatable validation command or fixture manifest.
- A reviewable product task boundary that consumes diagnostics without semantic promotion.

## Implementation Boundary for Task 65
Task 65 may only define a constrained product implementation prompt if it remains diagnostic-only.
Task 65 must **NOT** implement:
- ScoreIR emission.
- Recognised clef objects.
- Pitch/rhythm/key/time inference.
- OCR.
- Vector/raster fusion.
- Semantic promotion of `treble_clef_candidate`.
