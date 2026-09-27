# CP-13 — Let Codex author assigned tasks, with crossed review

- **Repository:** `tticom/score2gp-agentops`
- **Branch:** `feat/cp-13-codex-author-lane`
- **Maintainer direction, 2026-09-27:** "Could we delegate some more of the work load to codex to make better use of its usage allowance? I.e. Codex could be doing the research/architecture tasks."

## Why

The authority already lists `tticom-codex` in the `implementation` and `architect` roles. The dispatcher still refuses it any author work: `SLOT_ROLES` in `scripts/score2gp_dispatch.py` gives the `codex` slot only `governance` and `reviewer`.

So every task is authored by `tticom-automation`, which runs on Claude, and work stops whenever Claude's usage allowance is used up. Codex's allowance goes unused except for reviews.

## Goal

A task can be assigned to a specific author login. The dispatcher lets that login author the task from its own slot, and review stays crossed:

- a Codex-authored PR is reviewed by `tticom-automation` or `tticomgov-code`;
- a Claude-authored PR is reviewed by `tticom-codex`;
- the merge executor still requires a merger who is not the PR's author.

## Acceptance

1. **Slot roles.** `SLOT_ROLES["codex"]` allows `architect` and `implementation` as well as `governance` and `reviewer`. The `auto` and `gov` slots are unchanged.
2. **Author assignment.** A task or proposal may declare `author_login`.
   - `validate_authority` rejects an `author_login` that is not listed in the task's `owner_role` `github_logins`.
   - When `author_login` is set, the dispatcher authorises the author role only for that login. Any other login gets a terminal, non-authorising state that names the assigned author.
   - When `author_login` is unset, behaviour is unchanged.
3. **Self-review and self-merge stay refused.**
   - A reviewer assignment is refused when the reviewer login authored the PR.
   - The merge gate still denies a merger who authored the PR.
   - Tests cover both cases for a Codex-authored PR.
4. **Routing tests.**
   - A task assigned to `tticom-codex` is authorised in `worktrees/codex` and refused in `worktrees/auto`.
   - An unassigned task keeps today's routing.
   - A characterisation test shows that resolution of the current task is unchanged.
5. **Documentation.** `CLAUDE.md` (the AgentOps root), `AGENT_CONTROL.md` and `TASK_RECORDING_CONVENTION.md` describe:
   - author assignment;
   - the crossed-review rule;
   - the convention that governance assigns research and architecture tasks to `tticom-codex` by default and product-code tasks to `tticom-automation`, overridable per task.
6. **Validation.** `python -m pytest` and the governance audit pass, and `git diff --check` is clean.

## Constraints

- Do not weaken any identity, workspace, self-review or merge gate. The change only widens which slot may author, and only for an assigned task.
- Running two tasks at once is out of scope. That is a separate follow-up.
