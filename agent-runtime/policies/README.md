# Runtime role policy

The container is a bounded execution environment, not an authority source.
Task selection, identity checks, review, merge, and governance decisions remain
in AgentOps and are not delegated to the container.

The launcher accepts only an explicit task slug and one explicit product git
worktree. A future role-specific launcher may add commands, but must preserve
the same mount and credential restrictions.
