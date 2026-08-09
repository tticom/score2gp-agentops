# Conversion Recovery Director Skill

## Purpose

Coordinate conversion recovery toward useful musical output. Prevent refusal
quality, file creation, aggregate counts, or synthetic tests from masquerading
as conversion progress.

## Required inputs

Read, in order:

1. AGENT_CONTROL.md, ACTIVE_TASK.md, and the skills lock and profile;
2. programmes/2026-08-09-conversion-recovery.md;
3. tasks/2026-08-09-conversion-recovery-backlog.md;
4. the master diagnosis and every source report at its exact revision;
5. the current product call graph and open PR state.

## Operating loop

1. Pin product, AgentOps, skills, private manifest, active task, and PR SHAs.
2. Select the earliest unblocked task in the dependency graph.
3. State the defect, real-source oracle, strongest false-success mode, changed
   seam, and rollback.
4. For research, require a decision-forcing probe and A, B, or C outcome. For
   implementation, require accepted architecture and a real-source failing test.
5. Publish one PR, obtain exact-head independent review, and wait for human
   merge.
6. Replay the corpus oracle after merge and record the first remaining
   divergence before promoting the next task.

## Evidence rules

- A safe refusal proves safety only.
- A parseable MXL or GP proves serialization only.
- Aggregate counts are smoke signals only.
- Musical claims require ordered bar and event evidence from fresh no-reference
  output.
- Reference data must be physically and logically isolated from generation.
- Synthetic behavioural data cannot satisfy acceptance.
- Every green regression must be demonstrated red on its known-bad branch or
  mutation.

## Prompt quality gate

Do not promote a prompt unless it names:

- exact dependencies and accepted upstream artifacts;
- repository, branch pattern, role, and allowed files;
- one architectural seam;
- real-source fixtures and provenance requirements;
- productive success and safety criteria separately;
- a known-bad disconfirmation case;
- validation and privacy checks;
- stop or pivot conditions;
- handback fields and the first remaining mismatch.

Skeleton prompts are not executable. Replace every TBD_FROM field with accepted
evidence and mark it READY_FOR_PROMOTION before copying it to ACTIVE_TASK.md.

## Mandatory secondary audit

After every task, record:

1. which instruction allowed any false-success mode;
2. whether the prompt required a reviewer-created counterexample;
3. the smallest durable instruction improvement;
4. whether that change belongs in project policy or reusable agy-skills.

Do not modify shared skills incidentally during a product task. Reusable skill
changes require a separate skills PR and later AgentOps lock update.

## Stop conditions

Stop on unresolved report contradiction, dirty or unknown worktree overlap,
missing private-fixture provenance, reference leakage, unreviewed predecessor,
cross-seam scope, or a result that improves only refusal or file creation.
