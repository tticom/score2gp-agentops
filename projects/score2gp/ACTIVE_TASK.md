# Active Task

**Task**: CR-03B: Merge-integrity remediation for CR-03A
**Authorised Role**: Project Director / independent Reviewer
**Repository**: `tticom/score2gp-agentops` (governance), with read-only inspection of `tticom/score2gp`

## Status

CHANGES_REQUESTED

## Task Authorised

Yes, Tier 1 governance and review remediation only. CR-04A is suspended.

## Permissions and Boundaries

- Do not start CR-04A or any new product feature work.
- Inspect product PR #373 and the merged product `main` revision against the CR-03A approved file and behaviour boundary.
- Record the scope drift, merge-control breach, actual validation coverage, and whether each merged change is salvageable, must be reverted, or needs a clean follow-up branch.
- Define one clean, narrowly scoped remediation task rooted at product `origin/main`; it must state its allowed files and measurable public-test and output evidence.
- Do not modify product code, create a product branch, or treat the prior self-review as independent approval.

## Completion Evidence

1. A merge-integrity review in `projects/score2gp/reviews/` with direct PR #373 evidence.
2. A corrected backlog state that blocks CR-04A until CR-03B is independently reviewed and resolved.
3. A separate Reviewer disposition; only then may a new clean product remediation task be authorised.

## Unattended Continuation

This task suspends automatic product merges for the recovery programme. Agents
may continue the governance review and rework loop, but no product promotion is
eligible until CR-03B has independently closed the merge-integrity finding.
