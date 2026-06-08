# Active Task

Status: APPROVED

Current Permission Tier: Tier 2 branch and PR work.

## Title

Independent Post-Merge Review of Product PR #194

## Context

Product PR #194 was merged into `score2gp/main` during the 2026-06-08 autonomy-control incident. The concern is process-control loss, not assumed code defects. The merged code must receive an independent post-merge review before further product implementation work builds on it.

This is a review and evidence task. It should determine whether PR #194 is safe to keep as-is, needs follow-up fixes, or needs architectural clarification.

## Current Verified State

* Governance repo: `/home/tticom/work/score2gp-workspace/score2gp-agentops`
* Product repo: `/home/tticom/work/score2gp-workspace/score2gp`
* Governance control plane is active.
* `ACTIVE_TASK.md` is the only execution approval source.
* `TASKS.md` is backlog only and does not self-authorize work.
* Product PR #194 was merged before the current Tier 2 controls were fully established.

## Goal

Perform an independent post-merge review of product PR #194 and produce a review record in the governance repo.

The review must answer:

* What changed in PR #194?
* Was the change consistent with the architecture and current project boundaries?
* Were tests sufficient?
* Were privacy/artifact risks avoided?
* Are there defects, missing checks, or follow-up tasks?
* Is `score2gp/main` safe to continue from?

## Non-goals

* Do not modify product implementation code.
* Do not modify product tests.
* Do not attempt to revert PR #194.
* Do not start any backlog product work.
* Do not merge PRs.
* Do not approve PRs.
* Do not delete branches.
* Do not force-push.
* Do not use `hgh`.
* Do not mark any unmerged work as merged/done.

## Allowed Repositories

Governance repo:

* `/home/tticom/work/score2gp-workspace/score2gp-agentops`

Product repo:

* `/home/tticom/work/score2gp-workspace/score2gp`

## Allowed Files

Governance repo write access:

* A new review note under `projects/score2gp/reviews/`

Product repo read-only access:

* Inspect files changed by PR #194.
* Inspect relevant tests.
* Run tests/checks.
* Do not edit product files.

## Forbidden Actions

* Do not modify product files.
* Do not commit product changes.
* Do not merge PRs.
* Do not push to `main`.
* Do not force-push.
* Do not delete branches.
* Do not run `gh pr merge`.
* Do not run commands containing `--delete-branch`.
* Do not use `hgh`.
* Do not approve own PR.
* Do not bypass failing checks.
* Do not start unrelated backlog tasks.

## Required Pre-flight Checks

From governance repo:

```bash
cd /home/tticom/work/score2gp-workspace/score2gp-agentops
git status --short
git branch --show-current
git fetch --all --prune
git switch main
git pull --ff-only human main
```

Read:

* `projects/score2gp/AGENT_CONTROL.md`
* `projects/score2gp/ACTIVE_TASK.md`
* `projects/score2gp/TASKS.md`
* relevant templates under `projects/score2gp/templates/`

From product repo:

```bash
cd /home/tticom/work/score2gp-workspace/score2gp
git status --short
git branch --show-current
git fetch --all --prune
git switch main
git pull --ff-only human main
git log --oneline --decorate --max-count=20
```

Inspect PR #194 metadata and diff using available safe commands, for example:

```bash
gh pr view 194 --json number,title,state,mergedAt,headRefName,baseRefName,mergeCommit,url,files,commits
gh pr diff 194
```

If default `gh pr view` fails due to GitHub Projects Classic GraphQL warnings, use narrower `--json` fields or local git diff against the merge parent.

## Implementation Guidance

Create a governance branch:

```bash
git switch -c review/product-pr-194-post-merge-v0.1
```

Create a review note under:

```text
projects/score2gp/reviews/2026-06-08-product-pr-194-post-merge-review.md
```

The review note must include:

* PR number and title
* merge commit or relevant commit hashes
* files changed
* evidence inspected
* commands run
* tests/checks run
* architecture assessment
* schema/versioning assessment
* privacy/artifact assessment
* defects or concerns
* required fixes, if any
* suggested next task
* final verdict

## Validation

Run the smallest meaningful checks needed to verify PR #194.

At minimum, attempt:

```bash
cd /home/tticom/work/score2gp-workspace/score2gp
git status --short
.venv/bin/python -m pytest
```

If the full test suite is too slow or unavailable, run the most relevant targeted tests for PR #194 and report exactly what was and was not run.

Also run in the governance repo before commit:

```bash
git diff --check
git status --short
```

Confirm:

* no product files were modified
* only the intended governance review note was changed
* the review note contains enough evidence for a human to judge whether PR #194 is safe

## Acceptance Criteria

* A review note is created in the governance repo.
* The review gives a clear verdict:

  * safe to continue
  * needs follow-up fixes
  * do not build on this yet
  * cannot verify
* Commands and test results are recorded.
* Known limitations are explicit.
* Any follow-up task is small and concrete.
* No product files are modified.

## Stop Conditions

Stop and report if:

* product repo is dirty before inspection
* governance repo is dirty before branch creation
* PR #194 metadata/diff cannot be inspected
* tests fail and the cause is unclear
* private/generated artifacts appear at risk of being committed
* the review would require product code changes
* wrapper blocks required safe read-only commands
* branch push or PR creation is blocked

## Reporting Format

Report:

* verdict
* commands run
* files changed
* evidence reviewed
* test/check results
* commit hash
* branch name
* PR link if opened
* known limitations
* what was not tested
* next recommended task
