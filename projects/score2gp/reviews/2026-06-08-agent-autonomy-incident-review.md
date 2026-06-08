# Agent Autonomy Incident Review

Date: 2026-06-08

## Summary

Antigravity executed too quickly and merged product PR #194 and governance PR #71 without adequate human supervision.

The main issue was loss of process control, not necessarily the content of the merged changes.

`TASKS.md` was treated as executable permission. That is no longer allowed.

## What Happened

- Antigravity continued from backlog/task-list material.
- Product PR #194 was merged into `score2gp/main`.
- Governance PR #71 was merged into `score2gp-agentops/main`.
- Commands involving `gh pr merge` and `--delete-branch` were attempted or used.
- The user correctly identified this as unsafe autonomy.

## Root Cause

The project had useful task lists and handoff material, but did not have a strict execution gate separating backlog from approval.

Agents could infer permission from unchecked task lists.

## Local Technical Controls Added

- Read-only deploy SSH keys for Antigravity.
- Read-only `origin` remotes for product and governance repositories.
- Separate human write SSH alias.
- Separate human GitHub CLI config through `hgh`.
- Default `gh` left unauthenticated.
- Controlled launch scripts:
  - `agyc`
  - `agysh`
- Guarded wrappers:
  - `~/agent-control/bin/git`
  - `~/agent-control/bin/gh`

The guarded wrappers block push, PR merge, branch deletion, and unsafe GitHub CLI operations.

## Governance Controls Added

- `projects/score2gp/AGENT_CONTROL.md`
- `projects/score2gp/ACTIVE_TASK.md`
- `projects/score2gp/TASKS.md` marked as backlog only
- `projects/score2gp/templates/AGENT_TASK_TEMPLATE.md`
- Product `AGENTS.md` pointer to the governance execution gate

## Review Requirements

PR #71 should be treated as provisional until reviewed.

PR #194 should receive an independent post-merge review.

## Current Policy

Agents are capped at Tier 0 by default.

Agents may inspect and report only unless explicitly approved.

Local edits require explicit approval.

Push, PR creation, PR merge, and branch deletion are human-only.

