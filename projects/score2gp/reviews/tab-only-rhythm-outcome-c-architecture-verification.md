# Reviewer Architecture Verification: Tab-Only Rhythm Inference Outcome C

## Context
This report independently verifies the Architect Outcome C report merged in Governance PR #203. The Architect concluded that deterministic tab-only rhythm inference is unviable. The Supervisor policy direction of A+B+C has been proposed, pending this Reviewer verification.

## Verified Baseline
- **Governance PR #203**: Merged (`6c0c608205422fb54a527c15d48efa755f0e1cb1`)
- **Product Baseline**: `6afdd3195f37eca6e319caf33dbeccfbbf1d4b5c`

## Evidence Reviewed
### Governance Files
- `projects/score2gp/ACTIVE_TASK.md`
- `projects/score2gp/reports/2026-06-24-tab-only-rhythm-inference-viability.md`

### Product Files Inspected (Read-Only)
- `src/score2gp/build_ir.py` (specifically `build_ir_from_tabraw_only`)
- `src/score2gp/quarter_rest_recogniser.py` (specifically `extract_quarter_rest_candidates`)
- `src/score2gp/pdf_staff_geometry.py`
- `fixtures/public/generated_simple/simple/` (directory contents)

## Claim Verification
1. **Quarter-rest recogniser narrowness**: *Supported*. The file `src/score2gp/quarter_rest_recogniser.py` hardcodes a size-ratio check and a 30+ fragment count requirement. It does not generalize to other rest vocabularies.
2. **Tab stem/beam extraction absence**: *Supported*. `src/score2gp/pdf_staff_geometry.py` extracts flag/beam candidates only for standard notation staves (`NotationStaffGeometry`, `PdfStaffNotationGeometryDiagnostics`). Tab staves lack these diagnostic classes.
3. **`--pdf-only-tab` fallback timing**: *Supported*. In `src/score2gp/build_ir.py`, the function `build_ir_from_tabraw_only` assigns `grid_spacing` (eighth, 16th, etc.) purely based on the count `N` of horizontal candidate subgroups (`if N <= 8: ... elif N <= 16: ...`).
4. **Fixture inadequacy**: *Supported*. The available public fixtures (`TabOnlySingleNote.pdf`, `TabOnlyTwoNotes.pdf`, `TabOnlyQuarterNoteRests.pdf`, `TabOnlyThreeBarsOfRests.pdf`) are extremely simple and do not exhibit complex syncopation or diverse rhythm vocabularies.
5. **Spacing underdetermination**: *Supported*. Without explicit rhythmic markers or a full rest vocabulary, proportional horizontal spacing is fundamentally ambiguous and elastic in typical tab PDFs.
6. **Outcome C justification**: *Supported*. Deterministic precise rhythm inference from tab-only input lacking timing evidence is not credible without an extensive new pipeline or ML capabilities.
7. **A+B+C policy direction**: *Supported*. Taking the A+B+C policy direction to a later product requirement is reasonable.
8. **D should remain future/nice-to-have**: *Supported*. ML-assisted extraction is outside the scope of current authorised deterministic paths.

## Fact / Inference / Hypothesis / Unknown Assessment
The Architect report properly separates fact, inference, hypothesis, and unknown.
- **Facts** correctly describe the codebase state (`quarter_rest_recogniser.py`, `pdf_staff_geometry.py`, `build_ir.py`).
- **Inferences** logically connect the lack of explicit markers to the underdetermination of spatial context.
- **Hypotheses** are appropriately scoped and explicitly marked (e.g. pivot to MusicXML sidecar).
- **Unknowns** are material and honestly stated (userbase tolerance).

## Governance Compliance
- Developer implementation remains blocked.
- Supervisor pivot decision remained blocked until this review.
- No ML work is authorised.
- No product files have been modified by this review.

## Verdict
**approve Outcome C as evidence-backed**

The Supervisor may proceed to define the A+B+C product behaviour. Developer implementation is still not authorised until a bounded Developer requirement exists.
