# Active Task: Candidate Staff-Identity Diagnostic Evidence

## Repository
tticom/score2gp

## Current Governance State
Current product baseline: PR #326 in tticom/score2gp, merged with commit 7565e751e0dea624a209aeb4233373338296262a.
Architect research: Completed (PR #214, Outcome B)
Reviewer architecture verification: Completed
Developer implementation: Authorised (Diagnostic evidence only)
Product feature implementation: Blocked

## Active Task
Developer diagnostic-evidence task: preserve or expose staff/system identity on notation candidate diagnostics.

Constraints:
- Must preserve or expose `page_index`, `system_index`, and `staff_index` (or equivalent) on notation candidates.
- Must remain read-only diagnostic evidence without changing ScoreIR, GP export, or note/rhythm recognition.
- Must forbid full candidate-to-measure assignment.
- See `decisions/2026-06-25-post-pr214-candidate-staff-identity-diagnostic-authorisation.md` for full acceptance criteria.

## Active Blocker
Notation candidate diagnostics currently lack staff/system identity. Without this, candidate-to-measure spatial assignment is unsafe and blocked. We must add diagnostic evidence for staff/system identity to candidates before proceeding.

## Required Next Stages
1. Developer diagnostic-evidence implementation.
2. Reviewer implementation conformance review.
3. PR readiness review.

## Explicit Non-Authorisations
These remain explicitly **blocked**:
- Full candidate-to-measure assignment;
- standard-notation conversion;
- note/rest semantic recognition;
- rhythm/duration inference;
- polyphony;
- voice mapping;
- clef/key/time interpretation;
- ScoreIR generation;
- GP export;
- tab-only timing changes;
- private fixture usage;
- generated artifact commits.
