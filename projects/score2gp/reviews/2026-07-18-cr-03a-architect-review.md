# CR-03A Independent Architecture Review

## Verdict
`approve architecture with clean-base limitation`

## Evidence Reviewed
- `projects/score2gp/reports/2026-07-18-cr-03a-architect-report.md`
- `projects/score2gp/reviews/2026-07-17-cr-03-recovery-review.md`
- Product `origin/main`: `src/score2gp/whole_note_recogniser.py` candidate
  composition and `build_staff_timeline_preview` pipeline.
- Product `origin/main`: existing MusicXML/IR tuplet support.

## Independent Findings
The Architect report now defines a staff-local span model before timeline
slicing, an above-staff-only marker lane, exact ownership and ordered candidate
identities, and a unique-or-ambiguous association outcome. Its public synthetic
fixture design exercises the required adversarial text and geometry cases.

Product `origin/main` does not contain the recovery branch deterministic
MusicXML emitter. The Developer task is therefore limited to the local
candidate-association model and public tests. It must not claim end-to-end PDF
conversion recovery or import code from the unreviewed recovery stack.

## Required Developer Boundary
Branch from current product `origin/main`; modify only
`whole_note_recogniser.py` and focused public tests. An independent Reviewer
must review the resulting product PR before any merge.
