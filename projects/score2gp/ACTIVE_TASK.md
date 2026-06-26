# Active Task

**Task**: Reviewer Architecture Verification: Measure-Bucket Candidate Ordering
**Authorised Role**: Reviewer
**Repository**: `tticom/score2gp-agentops`

## Context
- The Architect has chosen **Outcome A** in `projects/score2gp/decisions/2026-06-26-architect-next-measure-diagnostic-step.md`.
- Measure-local candidate ordering / measure-bucket diagnostic is deemed viable using current public-fixture evidence.
- A Developer diagnostic task is proposed, but NOT YET authorised.
- Developer implementation is blocked.

## Required Next Review
The Reviewer must verify that the proposed architecture decision (Outcome A) satisfies all criteria, bounds the next step strictly to read-only geometric ordering, and does not leak into semantic inference or ScoreIR/GP generation.

After the Reviewer architecture verification task is completed: **Governance Authorisation** (to authorise Developer implementation if approved)
Before this architecture PR merges: **PR readiness review**
