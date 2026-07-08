# Active Task

**Task**: Req-108 / Task 32: Add backwards compatibility test for diagnostics output
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## Status
APPROVED

## Executable Task
Yes

## Completion Evidence
Developer must implement the backwards compatibility tests, commit to `score2gp`, push the branch, and open a PR.

## 1. Baseline
- The Epic B geometry candidate extractor skeleton, snapshot tests, and reporting smoke path (Req-104, 105, 107) have been merged into product `main` (#341, #342, #343).
- The governance PR lane is clean.

## 2. Context
As we add geometry candidate extraction to the diagnostic output, we must ensure existing diagnostic keys (and their semantic structure) remain available and unchanged to prevent breaking downstream integrations.

## 3. Active Blocker
The geometry candidate output could inadvertently mutate or overwrite existing diagnostic keys. We need a test to guard against this before further geometry logic is added.

## 4. Goal
Add a backwards compatibility test that explicitly ensures existing diagnostic output keys remain available and unchanged after the candidate reporting additions.

## 5. Non-goals
- No changes to ScoreIR emission logic.
- No new candidate extraction features or rules.

## 6. Repo Scope
- **Allow**:
  - `tests/test_pdf_diagnostics_backcompat.py`
  - `fixtures/public/expected_diagnostics_*.json` if required
- **Stop before changing**:
  - `ACTIVE_TASK.md` (once authorised)
  - Unrelated product code files.

## 7. Branch Suggestion
`test/pdf-diagnostics-backcompat-v0.1`

## 8. Required Output & Outcome
A product PR implementing tests to guard the diagnostics output structure.

## 9. Incremental Progress Check
- **What new evidence will this task produce?**: Tests proving backward compatibility.
- **Which prior result must it not merely repeat?**: Must test the full diagnostics payload, not just the candidate subset.
- **How will we know the task moved the project forward?**: A PR guarding diagnostic backcompat is opened.
- **What is the smallest next decision this task enables?**: Proceeding with further extraction logic safely.

## 10. Next Steps
- Promote the next available Epic B extraction task (e.g., Task 33).
