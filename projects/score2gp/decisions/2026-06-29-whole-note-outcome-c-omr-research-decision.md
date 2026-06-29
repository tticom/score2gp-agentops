# Decision: Whole-Note Artifact Boundary Blocker

## Baseline Evidence
- Product PR #333 merged into `tticom/score2gp` (merge commit `b38c0acc9c284379dcd0f82316db08c3fc6211ec`).
- PR #333 successfully added derived `staff_position_index` support for notehead-like `x_aligned_cluster_candidate` proxy records, but did not implement whole-note recognition, pitch, rhythm, ScoreIR, or GP export.
- Prior governance (`projects/score2gp/decisions/2026-06-27-safe-natural-fixture-candidate-approval.md`) selected the Mutopia A4 PDF as a candidate, explicitly requiring a Supervisor-approved fixture ingestion decision before download or diagnostic use.
- A diagnostic spike run on the Mutopia A4 fixture produced >120 false positives, initially prompting an Outcome C (stop/pivot) recommendation.
- However, no durable governance approval or fixture-ingestion record was added to `tticom/score2gp-agentops` prior to the diagnostic run. The prior PR #229 wording over-relied on the Mutopia diagnostic without durable approval evidence.

## Governance Decision
The governance decision is corrected as follows:
- **Whole-note Developer implementation is formally blocked.**
- **Outcome C is deferred and not yet durable** because its Mutopia evidence is artifact-boundary blocked.
- Geometric and basic connected-component paths remain suspected and diagnostically indicated as unsafe, but the Mutopia-run evidence is not yet approved as a governance basis.
- **OMR/CV Architecture Research is not authorised** from this unapproved evidence.
- The next authorised task is artifact-boundary governance, not OMR/CV research.

## Next Authorised Task
The next active task is a Supervisor approval or rejection decision for the fixture ingestion / diagnostic-use boundary of the pinned Mutopia A4 PDF (or an alternative approved false-positive fixture strategy). Only after artifact boundary approval can the diagnostic be rerun or validated inside that boundary.
