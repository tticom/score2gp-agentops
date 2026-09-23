# Score2GP Workflow Skills Lock

## Source

- Repository: `https://github.com/tticom/agentops-claude-skills`
- Required source commit:
  `b90d4a9f43034b3196fa6b915fd95c8c89ecb11a`
- Replaces: `https://github.com/tticom/agy-skills` (last pinned at
  `439404f7342f4e324147efb6b0276f698fbf2bdb`), by maintainer direction on
  2026-09-23, adopted under `WIN-01`.
- Layout: each skill lives at `skills/<name>/SKILL.md`.

Required skills:

- `governed-development-loop`
- `identity-safe-git`
- `durable-handoff`
- `code-review`
- `hard-review`
- `devils-advocate-review`

## Activation gate

This lock becomes active only after the required source commit is contained in
the merged history of `agentops-claude-skills/main`. Before then, this AgentOps PR may be
reviewed but must not be merged or used to authorise product work.

For each agent identity:

1. use that identity's own `agentops-claude-skills` clone, the sibling of its
   `score2gp-agentops` checkout in `worktrees/<auto|gov|codex>`;
2. fetch the repository;
3. check out the required source commit in a detached, read-only worktree or
   a local tag that resolves exactly to it;
4. point installed skill links at that pinned checkout;
5. verify every required `SKILL.md` resolves below that checkout;
6. record `git rev-parse HEAD` in every durable run record.

All identities must use the same required source commit. Credentials,
worktrees, and home directories remain separate.

## Update policy

Do not pull, switch, relink, or otherwise update skills during an active
Score2GP implementation or review loop.

Upgrade only between tasks:

1. review and merge an `agentops-claude-skills` PR;
2. validate the new skills independently;
3. update this lock in a separate AgentOps PR;
4. activate it only after that AgentOps PR merges;
5. relink each identity to the newly pinned checkout.

A skills change is never part of converting a PDF, diagnosing conversion
output, or implementing product code.
