# REC-00A — Agent Workspace Cleanup Skill

Status: PROPOSED — governance task; do not execute until promoted.
Role: Architect / Governance
Repository: `score2gp-agentops`

## Objective

Define and add a reusable cleanup skill for agent environments. It must safely
identify stale Git worktrees, prunable metadata, generated artifacts, and
untracked files across the three agent identities without deleting active or
uncommitted work.

## Required work

1. Inventory canonical workspaces, worktrees, branches, dirty state and locks.
2. Classify entries as active, recoverable, generated, prunable or unknown.
3. Require explicit preservation evidence before removing dirty or unique work.
4. Remove only validated disposable worktrees and generated artifacts; retain
   branches and commits unless separately authorised.
5. Produce a durable cleanup receipt listing every removed path and reason.
6. Add checks usable from `tticom-automation`, `tticom-gov` and `tticom-codex`.

## Safety requirements

- Never use broad recursive deletion or delete a canonical repository.
- Never discard dirty files without an explicit archive/discard decision.
- Never infer that an old branch is disposable solely from its age.
- Treat `/mnt/c` mirrors and `/tmp` paths as non-canonical until proven safe.
- Fail closed on identity, workspace-root or branch ambiguity.

## Acceptance

- A dry-run inventory is deterministic and identity-aware.
- A known stale review worktree is removable while its branch/ref remains.
- A dirty worktree is preserved and reported, not silently removed.
- The cleanup receipt is sufficient to explain and reproduce the decision.

## Validation

Governance audit, focused skill tests, `git diff --check`, and a dry-run against
all three agent environments. No product files may change.
