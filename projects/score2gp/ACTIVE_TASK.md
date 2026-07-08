# Active Task

**Task**: Product PR readiness and merge progression for Epic B geometry candidate stack
**Authorised Role**: Reviewer / Integrator
**Repository**: `tticom/score2gp`

## Status
APPROVED

## Executable Task
Yes

## Completion Evidence
Product PRs #341, #342, and #343 successfully reviewed, tested, and merged into `tticom/score2gp` `main` branch.

## 1. Baseline
- The governance PR lane is clean.
- Req-102 is blocked and recorded by merged agentops PR #251.
- Req-104 review approval is recorded by merged agentops PR #255.
- Product PRs #341, #342, and #343 are open with passing CI/checks.

## 2. Context
We have three open product PRs (#341, #342, #343) that implement Epic B geometry candidate extraction requirements (Req-104, Req-105/106, Req-107). They are stacked and must be reviewed and merged in sequence to safely progress product functionality.

## 3. Active Blocker
Product work cannot progress to Req-108 until the preceding PRs are merged.

## 4. Goal
Resume product functionality by safely reviewing and merging the product stack in order.

## 5. Non-goals
- Do not revive governance PRs #252-#254.
- Do not implement new product work in this governance PR.
- Do not modify product code from the governance repo.
- Do not attempt single-prompt autonomous cycle implementation while Req-102 remains blocked.

## 6. Repo Scope
- **Allow**:
  - `ACTIVE_TASK.md` update.
  - Review and merge of PRs #341, #342, #343 in `tticom/score2gp`.
- **Stop before changing**:
  - Unrelated product code files.

## 7. Branch Suggestion
`governance/authorise-epic-b-product-progression`

## 8. Required Output & Outcome
Product PRs #341, #342, and #343 are merged into `tticom/score2gp`.

## 9. Incremental Progress Check
- **What new evidence will this task produce?**: Merged PRs on `main` representing Epic B functionality.
- **Which prior result must it not merely repeat?**: Must not duplicate work; we are merging completed work.
- **How will we know the task moved the project forward?**: Product `main` has the Epic B features.
- **What is the smallest next decision this task enables?**: Proceeding to Req-108.

## 10. Next Steps
- Review/merge #341.
- Review/merge #342.
- Review/merge #343.
- Proceed to Req-108.
