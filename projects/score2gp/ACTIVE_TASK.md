## Current Active Task

## Task 40 — Add candidate extraction design review

Status: ACTIVE

Owning repo: score2gp-agentops

Branch:
`review/primitive-evidence-candidate-extraction-design-v0.1`

PR title:
`docs(review): review primitive-evidence candidate extraction design`

Goal:
Perform a hard governance review before any extraction implementation. Decide whether the candidate model boundary is ready for a minimal extractor skeleton.

Allowed governance files:
- `projects/score2gp/reviews/2026-06-09-primitive-evidence-candidate-extraction-design.md`
- `projects/score2gp/ACTIVE_TASK.md`
- `projects/score2gp/tasks/2026-06-09-post-227-candidate-boundary-task-list.md`

Product repo access:
Read-only.

Required evidence:
- product main SHA
- Task 37 PR link and merge commit
- Task 38 PR link and merge commit
- Task 39 PR link and merge commit
- files inspected
- tests run
- schema status
- anti-semantic gate result
- privacy/artifact check

Verdict options:
- ready for extractor skeleton
- needs model hardening
- needs diagnostics prerequisite
- cannot verify

Non-goals:
- do not implement extraction
- do not modify product code
- do not add semantic tasks
