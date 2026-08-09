# Score2GP Workflow Skills Lock

## Source

- Repository: `https://github.com/tticom/agy-skills`
- Required source commit:
  `439404f7342f4e324147efb6b0276f698fbf2bdb`
- Introduction PR: `https://github.com/tticom/agy-skills/pull/2`
- Review hardening PRs:
  `https://github.com/tticom/agy-skills/pull/4`,
  `https://github.com/tticom/agy-skills/pull/5`, and
  `https://github.com/tticom/agy-skills/pull/6`
- Reviewer-role firewall and tiered review PR:
  `https://github.com/tticom/agy-skills/pull/14`

Required skills:

- `governed-development-loop`
- `identity-safe-git`
- `durable-handoff`
- `code-review`
- `hard-review`
- `devils-advocate-review`

## Activation gate

This lock becomes active only after the required source commit is contained in
the merged history of `agy-skills/main`. Before then, this AgentOps PR may be
reviewed but must not be merged or used to authorise product work.

For each agent identity:

1. use that identity's own `agy-skills` clone;
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

1. review and merge an `agy-skills` PR;
2. validate the new skills independently;
3. update this lock in a separate AgentOps PR;
4. activate it only after that AgentOps PR merges;
5. relink each identity to the newly pinned checkout.

A skills change is never part of converting a PDF, diagnosing conversion
output, or implementing product code.
