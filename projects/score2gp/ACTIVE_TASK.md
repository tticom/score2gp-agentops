# Active Task

**Task**: Req-110 / Task 33: Add product architecture review for geometry candidates
**Authorised Role**: Reviewer
**Repository**: `tticom/score2gp-agentops`

## Status
APPROVED

## Executable Task
Yes

## Completion Evidence
Reviewer must produce an architectural verification report in `projects/score2gp/reports/` validating tasks 28-32 and 36, commit it, push the branch, and open a PR.

## 1. Baseline
- Epic B implementation tasks up to Req-109 have been completed and merged.
- Geometry candidate extractor skeleton and snapshot infrastructure are established.
- Primitive geometry geometries are now exposed in the diagnostics payload.

## 2. Context
Before allowing Architect and Developer roles to proceed to Epic C (Semantic Boundary Definition & Core Interpretation), the governance process mandates a formal review of the geometry candidate layer (Epic B) to ensure it satisfies requirements without premature implementation of deferred capabilities (e.g. pitch or duration semantics).

## 3. Active Blocker
Epic C tasks (Req-111+) are formally blocked until Req-110 architecture review passes.

## 4. Goal
Produce a product architecture review report validating that the geometry candidate layer provides a safe, semantic-free foundation for future interpretation.

## 5. Non-goals
- No product code changes in `score2gp`.
- No new feature implementations.
- No changes to `ACTIVE_TASK.md` or `APPROVED_TASK_QUEUE.md`.

## 6. Repo Scope
- **Allow**:
  - `projects/score2gp/reports/2026-07-08-geometry-candidate-layer-review.md`
- **Stop before changing**:
  - `ACTIVE_TASK.md` (once authorised)
  - `TASKS.md`
  - `APPROVED_TASK_QUEUE.md`

## 7. Branch Suggestion
`governance/authorise-req-110-geometry-candidate-review`

## 8. Required Output & Outcome
A governance PR containing the architecture review report and an adversarial evaluation ledger.

## 9. Incremental Progress Check
- **What new evidence will this task produce?**: A review document evaluating Epic B compliance.
- **Which prior result must it not merely repeat?**: Must specifically audit the outputs of Tasks 28-32 and 36.
- **How will we know the task moved the project forward?**: A PR is opened containing the verified evaluation.
- **What is the smallest next decision this task enables?**: Proceeding to Epic C or resolving any found deficiencies.

## 10. Next Steps
- Promote Req-117 or Req-111 once the review PR is merged.
