# Runtime role policy

The container is a bounded execution environment, not an authority source.
Task selection, identity checks, review, merge, and governance decisions remain
in AgentOps and are not delegated to the container.

The launcher requires an explicit task slug and published task branch. Each
worker uses an independent clone, never shared Git administration. Live
workers have network access for checkpoint publication; Compose is offline
validation only. Review sessions verify but never publish repository changes.
See [task checkpoint policy](../../projects/score2gp/TASK_CHECKPOINT_POLICY.md).
