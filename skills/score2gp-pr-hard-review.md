# Score2GP Review Policy Overlay

This file is a Score2GP project-policy adapter, not a standalone review skill.
Reusable review mechanics live in the exact `agy-skills` revision pinned by
`projects/score2gp/SKILLS_LOCK.md`.

## Mandatory level selection

`scripts/score2gp_got_bootstrap.py` returns `review_level`, `review_skill`,
`review_reasons`, `review_worktree`, and `review_local_head`. The reviewer
must invoke exactly that pinned skill:

- BASIC / `code-review`: genuinely low-risk documentation-only changes;
- HARD / `hard-review`: code, tests, fixtures, executable scripts, domain
  data, generated artifacts, or empirical claims;
- DEVILS_ADVOCATE / `devils-advocate-review`: AgentOps/control-plane changes,
  architecture/research, conversion correctness, and every re-review after a
  trusted review on an earlier head.

A task or current maintainer instruction may escalate this minimum but may
never weaken it. `real review` means DEVILS_ADVOCATE.

## Score2GP evidence additions

Apply, in order:

1. `projects/score2gp/REVIEW_RULES.md`;
2. `projects/score2gp/PR_REVIEW_TEMPLATE.md`;
3. `projects/score2gp/PR_EVIDENCE_CONTRACT.md`;
4. the active task, original prompt, and approved architecture.

For conversion, recognition, MusicXML, ScoreIR, GPIF, timing, grouping,
geometry, parser, fixture, or private-corpus claims:

- direct source evidence outranks generated summaries;
- a written output file is not proof of musical correctness;
- strict, remediation, semantic round-trip, and file-existence results remain
  separate channels;
- synthetic, mocked, generated-notation, invented-value, and data-free tests
  carry zero domain-acceptance weight;
- real-source tests must preserve provenance and reach the changed production
  seam;
- reference GP data is an oracle only and must never enter production input;
- skipped private tests are not approval evidence;
- fixture names, hashes, literal coordinates, counts, and expected outputs must
  not select production behavior;
- general tolerances require evidence from more than one approved real source.

HARD and DEVILS_ADVOCATE approvals require claim-to-oracle closure and the
external evidence packet required by the pinned skill. DEVILS_ADVOCATE also
requires a contradiction ledger covering developer claims and prior reviews.

## Reviewer firewall

The review worktree is read-only and must remain clean. Probes, review bodies,
packets, and notes belong outside the repository. Reviewer mode may publish
review metadata only:

- one formal exact-head review;
- useful inline review comments;
- one mandatory marked PR summary comment.

Never edit source, tests, fixtures, prompts, reports, task state, PR bodies,
branches, commits, refs, or evidence artifacts while reviewing. Never implement
a fix or process improvement in the reviewed repository.

`tticom-automation` and `tticom-gov` never merge. `tticom-codex` may merge
only in a separate operation after a current explicit instruction from
`tticom` naming the exact repository, PR number, and reviewed full head SHA.

## Publication & Mandatory PR Commenting

Reviewers MUST publish their formal decision, inline findings, and summary comments directly to the GitHub Pull Request using the guarded publisher from the pinned `code-review` skill (`scripts/score2gp_publish_review.py` or `skills/engineering/code-review/scripts/publish_review.py`). A review is incomplete if findings or decisions are only reported in conversation chat or local files.

1. **Guarded Exact-Head Publication**: Always publish through the guarded publisher, which validates inline-comment payloads, binds the formal review to the exact live head, and creates or updates the mandatory marked summary comment on the PR thread as a single atomic operation.
2. **Inline Comments**: Provide line-level review comments for specific changed files and hunks where issues are identified via the publisher's inline comment payload.
3. **Mandatory Marked Summary**: Ensure the marked summary comment containing review level, verdict, finding ledger, and executed validation commands is created or updated on the PR.

Unbound raw CLI invocations that bypass exact-head binding, summary marker generation, or post-publication validation are strictly prohibited. A chat verdict, committed review report, task-state edit, or PR-body rewrite is not a review publication.

Before returning, re-query GitHub and prove the formal review, inline findings
when present, and mandatory summary exist on the reviewed head. Re-prove local
`HEAD` equality and a clean worktree. Any head movement or repository mutation
invalidates the review.
