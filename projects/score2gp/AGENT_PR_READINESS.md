# Agent PR Readiness Workflow

This document defines the strict workflow for evaluating and reporting Pull Request readiness. Agents must follow these rules before declaring a PR complete or ready for human review.

## 1. Readiness Verification

Do not report a PR as ready until CI/checks have completed and all Codex comments, review submissions, inline review threads, unresolved review threads, and normal PR comments have been inspected and explicitly dispositioned.

If Codex has not appeared yet, do not call the PR ready. Report one of:
- READY — Codex checked and all comments dispositioned
- NOT READY — awaiting Codex
- NEEDS SUPERVISOR DECISION — Codex did not appear after bounded checks
- NEEDS CHANGES — Codex or reviewer found blockers

A PR is also NOT ready if:
- required role skill checks were skipped;
- Architect references were not provided for uncertain technical strategy;
- Reviewer reference verification was required but not done;
- unresolved review threads remain;
- the PR body claims evidence that is not present.

## 2. Codex Disposition Rule

Every Codex comment or review thread must be dispositioned as one of:
- accepted as blocker;
- accepted as non-blocking;
- already fixed;
- rejected with reason.

When Codex leaves an inline review comment or review thread, the assigned agent must reply directly to that thread with:
- disposition: accepted as blocker, accepted as non-blocking, already fixed, or rejected with reason;
- fix evidence when the disposition is accepted as blocker or already fixed: commit SHA, changed file(s), and regression test or validation evidence;
- rationale when the disposition is accepted as non-blocking or rejected with reason;
- remaining status: resolved, unresolved, or human resolution required.

A top-level PR comment is not sufficient for inline Codex feedback. If the agent has permission to resolve the thread, it must resolve it after verifying the fix. If it cannot resolve the thread, it must report that human thread resolution is required and must not mark the PR as READY.

If a Codex comment identifies a plausible correctness bug, require or add a regression test unless there is a clear written reason not to.

## 3. Separation of Opening and Completion

Opening a PR is not completion. After opening a PR, the assigned agent must observe checks and the Codex/comment surface, address blockers on the same branch where possible, and only then report readiness.

## 4. PR Readiness Evidence Block

All review reports or completion reports must include the following evidence block:

```text
PR readiness evidence:
- PR state:
- Head SHA:
- Mergeable:
- Changed files:
- CI/checks:
- Codex review submissions:
- Codex inline comments:
- Review threads:
- Unresolved threads:
- Codex comment disposition:
- Regression tests added/updated:
- Known limitations:
```

## 5. Fast-Lane Rule

Fast-lane review is allowed only for tiny corrective PRs where:
- scope is limited to tests or governance docs;
- CI/checks are green;
- Codex comments/review threads are absent or fully dispositioned;
- the PR directly fixes a previously accepted blocker;
- no product/governance boundary is crossed.

## 6. Role-Specific Rules

**Product agents:**
- implement the authorised product task only;
- open the product PR;
- inspect CI, comments, Codex review submissions, and review threads;
- address Codex blockers before reporting ready;
- report READY/NOT READY/NEEDS CHANGES/NEEDS SUPERVISOR DECISION.

**Governance agents:**
- verify live product PR state before recording completion;
- verify Codex/comment disposition before authorising the next product task;
- keep governance records minimal and factual.

**Reviewers:**
- do not trust self-reports;
- verify live PR state, diff, checks, comments, reviews, review threads, branch/head SHA, and evidence;
- include a Codex comment disposition section in every review.
