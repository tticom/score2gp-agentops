# Active Task

**Task**: GOV-GO-GOT-01: State-Aware Agent Handoff Dispatch
**Status**: APPROVED
**Assigned Identity**: tticom-codex
**Authorised Role**: Project Director / Governance Developer (Tier 2)
**Repository**: tticom/score2gp-agentops
**PR Branch**: `codex/go-got-dispatcher`
**Original Prompt**: `projects/score2gp/prompts/next/go-got-dispatcher.md`

## Context

PR #382 merged at `3dcf5eef2761683125c3cbf2899a81dde58129ba`.
The previous static `NEXT.md` pointer remained aimed at completed Prompt 0017,
so `go` could repeat merged work. Review handback also depended on the
maintainer copying prose between Agy and Codex.

## Goal

Make `go` and `got` permanent role-specific dispatch commands that derive the
current phase from stable task identity and the exact live GitHub PR.

## Allowed Files

- `projects/score2gp/ACTIVE_TASK.md`
- `projects/score2gp/AGENT_CONTROL.md`
- `projects/score2gp/prompts/NEXT.md`
- `projects/score2gp/prompts/next/go-dispatch.md`
- `projects/score2gp/prompts/next/got-dispatch.md`
- `tests/test_governance_audit.py`

## Non-goals

No product edits, automatic merges, branch deletion, credential switching,
or automatic promotion of an unauthorised follow-up candidate.

## Acceptance

`go` cannot repeat a merged task, `got` cannot review an unpinned handback,
review fixes stay on the same PR, and governance tests enforce the permanent
dispatcher pointers and stop states.
