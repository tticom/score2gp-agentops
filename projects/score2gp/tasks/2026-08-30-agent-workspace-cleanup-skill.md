# Agent Workspace Cleanup Skill

Status: PROMOTED — executable authority is recorded in `ORCHESTRATION_STATE.json`.
Repository: `score2gp-agentops`
Depends on: current REC-01 cycle completion.

This task exists because stale review worktrees and generated artifacts were
found in the Codex workspace and reported in the automation environment. The
purpose is to make cleanup repeatable, identity-safe and auditable rather than
relying on ad-hoc deletion.

Use prompt: `projects/score2gp/prompts/next/rec-00a-agent-workspace-cleanup.md`.

The task must not remove active branches, dirty work, canonical repositories,
or unclassified paths. It is a governance/tooling task and must not change
Score2GP product behaviour.
