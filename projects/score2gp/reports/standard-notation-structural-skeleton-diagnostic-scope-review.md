# Reviewer Architecture Verification: Structural-Skeleton Diagnostic Scope

## Verdict
**approve architecture**

## Evidence Reviewed
### Governance Baseline
- PR #208 merged at commit `b10b7aa758f3a5b9bb3b1daeec018162e54fd49d`.
- `ACTIVE_TASK.md` confirms current state is Supervisor Decision Gate, and explicitly blocks both Developer implementation and Product diagnostic implementation.
- `projects/score2gp/reports/standard-notation-structural-layout-inference-viability.md` (PR #207 Architect Report) confirms Outcome B requires diagnostic-first proof of internal measure boundary extraction, bounded strictly to systems, staves, and internal barlines.

### Product Baseline
- The `tticom/score2gp` product repository was inspected.
- The following required files exist and are isolated from the core conversion pipeline:
  - `src/score2gp/pdf_staff_notation_diagnostics.py`
  - `src/score2gp/pdf_staff_geometry.py`
  - `src/score2gp/pdf_staff_detection.py`

## Fixture Verification
The required fixture set exists and provides a concrete, reproducible vector baseline:
- `tests/fixtures/pdf/generated_standard_staff_quarter_note.pdf`
- `tests/fixtures/pdf/generated_standard_staff_multi_staff.pdf`

## Scope Assessment
The proposed diagnostic hypothesis is strictly bounded. It limits verification to systems, staves, and internal barlines. It explicitly excludes polyphony, semantic voice mapping, and note association, which were the causes of failure for the broader layout inference.

## Metric and Threshold Assessment
The metrics (system count, staff count per system, barline count per staff) are measurable entirely from vector geometry.
- **Pass Threshold**: 100% correct grid extraction on the bounded public vector-PDF fixture set.
- **Fail Threshold**: Any missed barline, false barline caused by note stems, incorrect system grouping, or ambiguity preventing objective expected values.

## Ambiguity Assessment: Internal Barlines vs Note Stems
The barline-vs-stem ambiguity is the critical risk. However, it has a bounded diagnostic strategy: the diagnostic will measure if the vector geometry can distinguish vertical barline vectors from vertical note stem vectors based on height, staff crossing, and positional features without semantic interpretation.

## Product Safety Assessment
The diagnostic can be implemented in `pdf_staff_notation_diagnostics.py` and `pdf_staff_geometry.py` without changing the product conversion behaviour, `pdf.py`, or GP export behaviour. It is read-only and diagnostic-only.

## Artifact Hygiene Assessment
Clean. No private fixtures or generated PDFs are required to proceed with this diagnostic.

## Explicit Non-Authorisations
- Product feature implementation remains **blocked**.
- Polyphony, semantic voice mapping, note association, and GP export changes remain **blocked**.

## Required Next Task
The supervisor may authorise a Developer diagnostic implementation task strictly bounded to the structural-skeleton diagnostic scope.

## Stop/Pivot Conditions
If the Developer diagnostic implementation shows fragmented/inconsistent barline vectors, finds that stems are indistinguishable from barlines under available geometry, or requires semantic notation interpretation to pass, the project must stop this route and pivot to another recognition approach.
