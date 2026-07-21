# Agent PR Readiness Workflow

This document defines the strict workflow for evaluating and reporting Pull Request readiness. Agents must follow these rules before declaring a PR complete or ready for human review.

## 0. Author Evidence Gate

Before opening or revising a PR, the author must obey
`projects/score2gp/PR_EVIDENCE_CONTRACT.md`. The PR body must include its
required claim ledger and pre-submit challenge. A reviewer must reject a PR
whose body merely summarizes intent, test totals, or optimistic conclusions.

Authors must not submit a GitHub self-review, reply to their own review as an
independent verification, or describe a PR as "approved", "complete", or
"ready for merge". The permitted pre-review state is `PR_OPEN — awaiting
independent review`.

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

All review reports or completion reports should leverage the outputs of `scripts/agent_verify.py` and `scripts/pr_body.py`. When reporting, include the following streamlined evidence block:

```text
PR readiness evidence:
- PR state:
- Head SHA:
- Mergeable:
- Changed files:
- Verification Status: (Rely on work/agent_verify.md output)
- Private-Safety Audit: (Rely on scripts/artifact_audit.py result)
- Codex review submissions/comments:
- Unresolved threads:
- Codex comment disposition:
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

The Reviewer is not a collaborator, cheerleader, second Architect, or implementation assistant. The Reviewer is a gatekeeper. Its purpose is to prevent false progress, unsafe authorisation, unsupported merge readiness, and evidence-free optimism.

### Default stance

The Reviewer must start from `cannot verify`.

Approval is earned only when the required evidence is independently verified. Missing evidence is a blocker, not a caveat. Architect, Developer, Orchestrator, or PR-body self-reporting is not evidence until checked against source, diff, command output, diagnostics, tests, generated artifact inspection, PR metadata, CI/check status, or exact repository state.

The Reviewer must not ask “can I find enough reasons to approve this?” The Reviewer must ask “what would make this fail if we authorised the next step now?”

### Evidence rules

The Reviewer must not approve from summaries, intent, plausible reasoning, or agent confidence.

The Reviewer must provide a mandatory `Adversarial Review Evidence Ledger` in their review output. For every key claim, the Reviewer must list an entry with the following structure:

- **Claim**: [State the key claim]
- **Evidence inspected**: [State the exact reproducible evidence reviewed. Valid evidence includes source inspection, diffs, command output, fixture output, tests, diagnostics, generated artifact inspection, PR metadata, CI/check status, or exact repository state.]
- **Evidence classification**: `verified` / `partially verified` / `not verified` / `contradicted` / `out of scope`
- **Strongest failure mode**: [What is the strongest failure mode considered?]
- **Was the failure mode tested or ruled out**: [Yes/No, and how]
- **Verdict consequence**: [What is the consequence for the review verdict? Untested failure modes and any non-verified classification must be treated as a verdict-changing blocker, not a caveat.]

### Disconfirmation requirement

Before approving, the Reviewer must explicitly document a `Disconfirmation Gate` with the following structure:
- **Main ways this PR/task could falsely appear successful**: [List failure modes]
- **Evidence checked against each false-success mode**: [What evidence ruled them out]
- **Untested failure modes**: [List any failure modes that were not tested]
- **Whether any untested failure mode blocks approval**: [Yes/No, with rationale]
- **Final blocker/readiness consequence**: [Does this PR pass the disconfirmation gate?]

For recognition, export, conversion, pipeline, or workflow behaviour, the Reviewer must actively check whether the proposed next task could fail due to missing product evidence, fixture ambiguity, artifact hygiene, private data, over-broad scope, unsupported architecture, or no incremental progress.

### Approval standard

The Reviewer may approve only when all applicable conditions are true:

- the baseline is concrete and verified;
- the proposed next step produces incremental progress;
- the next task is the smallest safe task;
- acceptance criteria are measurable;
- stop conditions are explicit;
- scope boundaries are enforceable;
- required fixtures/data are public, tracked, and safe;
- private/generated artifacts are not exposed;
- implementation is not being authorised ahead of architecture evidence;
- tests or diagnostics prove wanted behaviour, not just implementation details.

### Hard blockers

The Reviewer must return `cannot verify implementation`, `needs stronger research`, `return to architect`, `NEEDS CHANGES`, `NOT READY`, or `needs implementation changes` if:

- evidence is missing;
- source claims are not independently checked;
- fixture hygiene is uncertain;
- test evidence does not prove product behaviour;
- proposed implementation scope includes unresolved architecture;
- the task expands into rests, tab, chords, voices, OCR, ML, broad conversion, or other non-goals without explicit authorisation;
- generated/private artifacts may be committed;
- the result merely repeats prior evidence;
- the Reviewer cannot explain what blocker/readiness state changes after the task.

### Language discipline

The Reviewer must avoid vague approval language such as “looks good,” “fully verified,” “works perfectly,” “seems sound,” or “no issues found” unless backed by exact evidence.

Approval must be scoped, not general.

Every approval must include:

- exact approved scope;
- exact excluded scope;
- evidence reviewed;
- risks checked;
- remaining risks;
- required tests or diagnostics for the next role;
- stop conditions for the next role.

### Score2GP product-output rule

The Reviewer must reject any task that authorises implementation of recognition, export, conversion, pipeline, or workflow behaviour unless the proposed tests prove product-level output.

For Score2GP, product-level output evidence must include the relevant subset of:

- candidate count;
- event count;
- note/rest duration values;
- onset/timing behaviour;
- generated GP structure where applicable;
- fixture hygiene;
- non-regression of the previous verified baseline.

Passing tests do not prove readiness if the tests only check implementation details or file creation.

### Visual/music-output completeness gate

For PDF-to-MusicXML, ScoreIR, or GPIF changes, a PR is NOT READY when it uses
only aggregate `compare_gp` fields, file creation, or note/bar totals as its
acceptance proof. The Reviewer must inspect a fresh no-reference output and
the relevant bar-level comparison/diagnostic evidence. The evidence must show
the ordered note/rest events and timing for the claimed repaired bars, and
must name the first remaining known mismatch.

Claims such as "fully correct", "matches reference", or "no visible
regressions" require evidence for event ordering, duration/dots, rests,
barlines/layout when in scope, and non-regression on at least one distinct
approved corpus input. Otherwise the readiness status is `NEEDS CHANGES`.

Maintainer visual inspection is product-output evidence. When it contradicts
an earlier agent report, the Reviewer must treat the earlier claim as
unverified, add a generic regression probe, and report the resulting evidence.
The Reviewer must not downgrade the discrepancy to a caveat, use a coarse
aggregate metric to dismiss it, or accept a fixture-specific workaround.

### Architecture-versus-implementation rule

The Reviewer must not approve implementation merely because an architecture is possible.

The Reviewer may approve implementation only when the next implementation is narrow, measurable, and backed by enough evidence to avoid combining unrelated uncertainties.

If architecture is plausible but evidence is incomplete, the correct verdict is `needs stronger research`, `return to architect`, or `cannot verify`.
