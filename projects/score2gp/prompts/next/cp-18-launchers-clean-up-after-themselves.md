# CP-18: Launchers clean up after themselves: remove merged author worktrees, review checkouts and pytest temp directories

- **Repository:** `tticom/score2gp-agentops`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Branch:** `feat/cp-18-launchers-clean-up-after-themselves`
- **Depends on:** none

## Goal

Measured by governance on 2026-09-29 at product main 2e8c00b (worktree at d7eef3f) on this Windows host. worktrees/codex holds about 60 entries: 3 merged author worktrees (3-5 GB each, mostly gitignored work/), about 30 review checkouts (up to 231 MB each) and about 12 empty pytest temp directories; worktrees/gov holds 6 review checkouts of about 217 MB each. Remove review checkouts when the review publishes, author worktrees after merge (keeping any requested deliverables), and temp directories on exit; preserve dirty or locked worktrees and record a receipt, as the workspace-cleanup skill does.

## Acceptance

1. Measure first: count and size the worktrees under worktrees/codex and worktrees/gov by kind (merged author, review checkout, empty pytest temp, dirty, locked) as they stand now; counts and sizes only.
2. Remove detached review checkouts (disposable, never an author worktree) once their review is published even while the PR is open, author worktrees only after their PR is merged or closed, and pytest temp directories on exit, keeping any requested deliverables. Dirty, locked or unclassified worktrees are preserved and listed, never removed.
3. A receipt records what was removed and what was kept and why, as the workspace-cleanup skill does. Removal never touches the author worktree of an open PR; the only open-PR path removed is a clean, unlocked, detached review checkout whose review is published.
4. Tests cover: merged clean worktree (removed), dirty (kept), locked (kept), open-PR author worktree (kept), published-review detached checkout of an open PR (removed), unclassified (kept); the named mutants (remove dirty, ignore lock, remove open-PR worktree) are rejected.
5. Launcher scripts that live in the workstation repo are listed, not edited here. Validation commands pass; handback complete.

## Rules

- Do not weaken, skip or reorder any merge, review or audit gate; this task touches no gate. Cleanup removes only what the acceptance names and never anything dirty, locked, unclassified or an author worktree of an open PR.
- Tests must be able to fail: for each new test, name the wrong implementation it rejects and show that mutant failing.
- Never edit CI, private fixtures, agent instruction files or `ORCHESTRATION_STATE.json`.
- Stop and say so if the task needs any gate change beyond the one the acceptance names.
