# Active Task: Reviewer Architecture Verification — Standard-Notation Structural Layout Inference

## Repository
tticom/score2gp

## Current Governance State
PR #324 is merged.
Architect research report (Outcome B) produced.
No Developer implementation is currently authorised.

## Authorised Task
Reviewer architecture verification is required next.
The Reviewer must verify the Architect's research report and choose one of:
- approve architecture
- needs stronger research
- reject as speculative
- return to architect
- stop or pivot
- cannot verify

Since the Architect outcome is B (narrowed scope), the Reviewer must verify the evidence before any Developer task can be authorised.

### Reviewer Task Contract
- **Report Path**: `projects/score2gp/reports/standard-notation-structural-layout-inference-viability.md`
- **Product Baseline**: PR #324 (SHA: `67e31602eb280a225b0608e6bfd8255acdeacfc0`) and PR #206
- **Evidence to Inspect**:
  - `tests/fixtures/pdf/generated_standard_staff_quarter_note.pdf`
  - `tests/fixtures/pdf/generated_standard_staff_multi_staff.pdf`
  - `src/score2gp/pdf_staff_notation_diagnostics.py`
- **Validation Criteria**:
  - Verify that Outcome B remains diagnostic-first.
  - Ensure Developer implementation is NOT authorised until the diagnostic hypothesis is proven.
  - Polyphony and semantic note association must remain excluded.

## Developer Implementation Authorised
No.
