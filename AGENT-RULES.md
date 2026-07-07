# Agent Rules

## Bootstrapping and Agent Loading

At the very start of any conversation session, the agent MUST:
1. Run `./scripts/bootstrap.py --session-dir <session_brain_dir>` (using the active conversation/brain folder) to verify that the repository is up to date and link local session planning files (`implementation_plan.md`, `task.md`, `walkthrough.md`) to the repository's active run folder. If the script fails, the agent must stop and report the error to the user.
2. Read the output of `./scripts/bootstrap.py --session-dir <session_brain_dir>` and register the custom subagents (`architect`, `developer`, `reviewer`) using the `define_subagent` tool before invoking them.

## Global rules

1. Tier B (compressed loop) is the default workflow loop for low-risk, bounded public-fixture and product tasks. Tier A (full loop) is required only for architecture uncertainty, private benchmark claims, broad behavior changes, policy exceptions, or failed review.
2. Keep private copyrighted or licence-unclear fixtures local and untracked. Private fixtures reside in the sibling repository `score2gp-private-fixtures`.
3. Do not place private PDFs, GP files, MXL/MusicXML files, screenshots, overlays, logs, or generated conversion artifacts in Git.
4. Use sanitized evidence only: counts, statuses, warning categories, command names, and artifact paths. Leverage product automation scripts (`scripts/agent_verify.py`, `scripts/agent_status.py`, `scripts/pr_body.py`, and `scripts/artifact_audit.py`) to gather status and generate reports rather than copy/pasting raw CLI outputs.
5. Do not claim full PDF-to-GP conversion works unless proven by reproducible tests.
6. Prefer public fixtures for automated tests.
7. Do not let multiple agents edit the same source worktree.
8. Do not allow documentation-only churn to masquerade as implementation progress.
9. Every proposed implementation slice must have a test or a clear explanation of why no test is possible.


## Role ownership

Architect:
- Must inspect current code and prior PR state before issuing a task.
- Must identify whether the task is implementable with existing data.
- Must propose the smallest valid implementation route.
- Must explicitly call out blockers.
- Must not hand vague tasks to developers.
- Research solution for design PRs and provide feasibility, implementation routes, evidence requirements, and stop conditions.
- Adhere to the "No fake progress rule": If required source evidence is unavailable, do not simulate it. Report the missing prerequisite.

Developer:
- Must implement only the assigned task.
- Must not carry unrelated previous task files unless the PR is explicitly stacked.
- Must not invent data to satisfy tests.
- Must run required tests and write tests to cover all new system code.
- Must report changed files, commands, results, branch base, dependency PRs, and limitations.

Reviewer:
- Must check out the PR or inspect the diff deeply enough to verify it.
- Must run targeted tests unless impossible.
- Must verify requirement fit, branch hygiene, artifacts, privacy, fake-data risks, and semantic-boundary compliance.
- Must use verdicts: merge, needs changes, do not merge, blocked, or cannot verify. “CI passed” is not a verdict.
- Check empirical validation: What tests passed or failed? What commands were run?
- Must ensure that all comments raised by Codex on the PR are addressed before claiming that the PR is ready for review.

Orchestrator:
- Must maintain the queue state and dependency graph.
- Must decide whether the next action is feature work, cleanup, rebase, close duplicate PRs, or architecture redesign.
- Must not keep feeding developers when the active blocker is branch hygiene or a design gap.

Integrator:
- Must manage branch bases, stacked PRs, duplicate PRs, conflicts, PR bodies, and cleanup.
- Must never merge to main.
- Must not modify product logic unless explicitly instructed.
