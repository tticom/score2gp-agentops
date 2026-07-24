# Address Current PR Review Findings

## Purpose

This reusable command handles a `CHANGES_REQUESTED` cycle on the active task's
existing pull request. It is not tied to a repository, PR number, branch,
reviewer, or defect class.

## Required Active-Task Metadata

Read these structured fields from `projects/score2gp/ACTIVE_TASK.md`:

- `Repository`
- `Pull Request`
- `PR Branch`
- `Reviewed Head`
- `Review Findings`
- `Status`

Require `Status` to be `CHANGES_REQUESTED`. If any field is missing, malformed,
does not identify one open PR, or conflicts with live GitHub state, stop and
report. Never guess a PR from recency, author, branch naming, or sidebar state.

## Identity and Environment

1. Work only in the canonical Ubuntu WSL workspace named by project controls.
2. Read `AGENT_CONTROL.md`, `ACTIVE_TASK.md`, the applicable Developer skill,
   the original task prompt, and every unresolved item at `Review Findings`.
3. Switch GitHub CLI to the task's authorised implementation identity. For
   Score2GP Agy work:

```bash
gh auth switch --hostname github.com --user tticom-automation
test "$(gh api user --jq .login)" = "tticom-automation"
```

4. Set and verify the same repository-local Git identity.
5. Require clean product and governance worktrees. Fetch without destructive
   reset, clean, branch deletion, force-push, or history rewriting.

## Resolve the Existing PR

1. Query the exact `Pull Request` URL.
2. Require it to be open and its head branch to equal `PR Branch`.
3. Require its current head to equal `Reviewed Head` before applying fixes,
   unless newer commits are already documented as part of this same review-fix
   cycle. Stop on unexplained divergence.
4. Switch to the existing local `PR Branch`, or create a local tracking branch
   from its remote head if absent.
5. Do not create a new branch or PR. Do not amend or force-push published
   commits.

## Fix Contract

1. Convert every unresolved review item into:
   - the demonstrated false-success or failure mode;
   - the smallest source correction inside the original task boundary;
   - a regression that fails on `Reviewed Head`;
   - focused and repository-wide verification.
2. Address all blocking findings, not merely wording or the happy-path test.
3. Preserve the original task's allowed files, data boundaries, product
   behavior limits, and stop conditions.
4. If a finding exposes a missing observation or requires scope expansion,
   implement the safe fail-closed behavior available inside scope and report
   the precise remaining gap. Do not invent data, ownership, timing, or
   evidence.
5. Do not resolve or dismiss reviewer findings without code/test evidence.

## Verification

Run:

```bash
.venv/bin/python -m pytest
.venv/bin/python -m score2gp.cli export-schema --out schemas
.venv/bin/python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json
.venv/bin/python scripts/artifact_audit.py
git diff --check origin/main...HEAD
git diff --exit-code -- schemas
git ls-files fixtures/private work
git status --short
```

Also run every focused regression or reproduction explicitly requested by the
review. A green full suite does not replace those reproductions.

## Publish to the Same PR

1. Stage only files inside the original task and review-fix boundary.
2. Commit follow-up changes normally; do not amend.
3. Push normally to the existing `PR Branch`; do not force-push.
4. Comment on the existing `Pull Request` using the authorised implementation
   identity. Include:
   - new head SHA;
   - each review finding and its disposition;
   - regression/reproduction results;
   - focused and full verification;
   - remaining limits or observability gaps.
5. Do not open a new PR, mark it ready, approve it, resolve independent review
   threads on the reviewer's behalf, or merge it.
6. Stop for independent re-review.
