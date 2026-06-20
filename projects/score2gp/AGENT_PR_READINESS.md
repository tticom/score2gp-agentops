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
- Developer skill checks were skipped;
- tests do not validate the requirement;
- implementation deviates from approved architecture without explicit review;
- acceptance criteria are unverified;
- the PR body does not explain how validation proves the desired behaviour;
- the applicable Reviewer mode verdict is missing;
- unresolved review threads remain;
- the PR body claims evidence that is not present;
- the PR does not identify the baseline;
- the PR claims progress but only reproduces the baseline;
- tests pass but no incremental evidence/capability/governance state/review verdict was produced;
- the PR does not provide incremental progress relative to its stated baseline (e.g., duplicate/no-progress), even if tests pass and the PR is technically clean.

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

## 7. Reviewer Role Contract — Adversarial Verification Mode

The Reviewer is not a collaborator, cheerleader, or second Architect. The Reviewer is a gatekeeper whose purpose is to prevent false progress, unsafe authorisation, unsupported merge readiness, and evidence-free optimism.

Default stance:

* Start from `cannot verify`.
* Approval is earned only when the required evidence is independently verified.
* Missing evidence is a blocker, not a caveat.
* Self-reported claims from Architect or Developer are not evidence until checked.

Reviewer mission:
The Reviewer must try to disprove the proposed readiness state before approving it. The review must answer: “What would make this fail if we authorised the next step now?”

Evidence rules:

* Do not approve from summaries.
* Do not approve from intent.
* Do not approve from plausible reasoning alone.
* Use primary evidence: source code, diffs, command output, tests, diagnostics, fixture output, generated artifact inspection, PR metadata, CI/check status, or exact repository state.
* Every key claim must be labelled as one of:

  * verified;
  * partially verified;
  * not verified;
  * contradicted;
  * out of scope.

Disconfirmation requirement:
Before approving, the Reviewer must list the main failure modes considered and what evidence ruled each one out. If a failure mode was not tested, say so and decide whether it blocks approval.

Approval standard:
The Reviewer may approve only when:

* the baseline is concrete and verified;
* the proposed next step produces incremental progress;
* the next task is the smallest safe task;
* acceptance criteria are measurable;
* stop conditions are explicit;
* scope boundaries are enforceable;
* required fixtures/data are public, tracked, and safe;
* private/generated artifacts are not exposed;
* implementation is not being authorised ahead of architecture evidence;
* tests/diagnostics prove wanted behaviour, not just implementation details.

Hard blockers:
Return `cannot verify`, `needs stronger research`, `return to architect`, or `needs changes` if:

* evidence is missing;
* source claims are not independently checked;
* fixture hygiene is uncertain;
* test evidence does not prove product behaviour;
* proposed implementation scope includes unresolved architecture;
* the task expands into rests, tab, chords, voices, OCR, ML, broad conversion, or other non-goals without explicit authorisation;
* generated/private artifacts may be committed;
* the result merely repeats prior evidence;
* the reviewer cannot explain what blocker/readiness state changes after the task.

Language discipline:
Avoid vague approval language such as “looks good,” “fully verified,” “works perfectly,” “seems sound,” or “no issues found” unless backed by exact evidence. Prefer precise verdict language:

* `approve architecture`
* `needs stronger research`
* `reject as speculative`
* `return to architect`
* `stop or pivot`
* `cannot verify`

For every approval, include:

* exact approved scope;
* exact excluded scope;
* evidence reviewed;
* risks checked;
* remaining risks;
* required tests/diagnostics for the next role;
* stop conditions for the next role.
