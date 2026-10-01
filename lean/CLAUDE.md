# Lean agent guidance (replaces AGENT-RULES.md, AGENTS.md, CLAUDE.md at cutover)

One page. Nothing here is a state machine. The task list is `TASKS.md`. The
maintainer (tticom) is the only one who merges.

## Roles

- **Author** (an agent): does one task at a time, in its own worktree, on a
  branch `task/<id>`, and opens a draft PR.
- **Reviewer** (an optional fresh agent session): reads a risky PR and posts an
  advisory comment. Never edits the PR and never merges.
- **Maintainer**: decides, reviews as they wish, merges.

No other roles. No dispatcher, no promotion PRs, no handback comments.

## Ground rules (each one is here because the failure happened)

1. **Agents never merge.** No `gh pr merge`, no auto-merge, no `--admin`, no
   approving your own PR. Opening a PR and stopping is the finish line.
2. **Never push to `main`.** Not directly, not by force, not with the
   maintainer's credential. Install the pre-push hook
   (`python lean/scripts/install_hooks.py`) in every clone. This is convention
   plus a local hook, not server enforcement: `--no-verify` bypasses it. If a
   push is refused, report it; never retry around it.
3. **No private data in commits, PR bodies, comments or logs.** No raw private
   PDF, GP, MXL or MusicXML files, screenshots, overlays or generated conversion
   output. Report counts, statuses and warning categories, never raw output or
   private paths. Private fixtures stay in the private fixtures repo and local
   workspace.
4. **No false green.** A skipped test is `NOT_EVALUATED`, not a pass. Never add or
   widen a skip or xfail to get a green. A test command counts only when it
   finished and its exit code and totals were captured.
5. **No silent fallbacks in the converter.** Missing or invalid input fails closed
   with a named error. Never invent notes, rests, timings or fingerings to make a
   result look complete.
6. **Judge claims against the source file.** Mock-only or synthetic-only tests
   cannot prove a conversion-fidelity claim. Conversion output is checked by
   semantic comparison against the real source, not by "a file was produced".
   Use a real-fixture check (below) for any `risky` conversion change.
7. **Report results in four parts for conversion work:** strict-mode result,
   remediation-mode result, semantic result, file-exists. One "success" must not
   hide failures. The five claims in `projects/score2gp/REJECTED_CLAIMS.md` (moved to `docs/rejected-claims.md` at cutover) are known to be
   false; do not repeat them.
8. **Stay in scope.** Work inside the task's allowed paths. Needing another path
   means asking, not widening. Do not pad progress with docs churn.
9. **Branch hygiene.** One agent per worktree. Check the branch before every
   commit. Off-task work goes on a new branch. Never carry another task's files.
10. **Stop on unexplained failure.** A failing test, script or validation warning
    is a hard stop until understood. No soft bypasses.
11. **Diagnostics are bounded.** If two diagnostic passes do not change the next
    decision, stop and ask the maintainer rather than writing another report.
12. **Nobody waits on the maintainer.** Green checks are the author's go-ahead to
    move on; review for `risky` work is advisory and runs in parallel. Anything
    that needs a human decision is written down once, in the PR or in a decision
    report, and the author continues with other work.

## Risk

`TASKS.md` marks each task `normal` or `risky`.

`risky` means any of: conversion logic or the compiler; parsers; geometry or
timing; any fallback; anything touching private fixtures; CI, hooks or these
guidance files; a PR that has been disputed. A `risky` task must pass the local
real-fixture check before it is handed back, and gets an independent advisory
review (the `review` skill, adversarial mode). Normal tasks may merge on green CI
with no review; the maintainer may still ask for one.

## Author flow

1. Take the next `todo` entry in `TASKS.md` (or the one the maintainer names).
   Set it to `doing` in your branch.
2. Create a worktree and a `task/<id>` branch from `main` (`safe-git` skill).
3. Implement (`implement` skill): tests first where practical, full suite at the
   end, clean-head pre-flight.
4. For `risky` tasks, on the maintainer machine:
   `python lean/scripts/real_fixture_check.py --product <product checkout>`.
   It must report PASS (NOT_EVALUATED is not a pass). Put the sanitised counts in
   the PR.
5. Open a draft PR from `lean/PULL_REQUEST_TEMPLATE.md`. Mark it ready when CI is
   green. Remove the task from `TASKS.md` in the same PR (done entries are
   deleted; git history is the record). The PR is now "ready to merge": the
   maintainer merges, in their own time and in batches.
6. **Do not wait for the merge.** Take the next `todo` task. If it depends on the
   unmerged one, branch from that task's branch and say so in the PR (stacked), or
   mark it `blocked` in `TASKS.md` and take a different task. If no task can
   proceed, stop and report; do not invent work.
7. For `risky` tasks, request the independent review yourself (fresh session,
   `review` skill, adversarial mode) as soon as checks are green, and keep working.
   Its comment is advice for the maintainer; findings are fixed with
   `address-review`. Never resolve a reviewer's threads.

## Knowledge (what is versioned)

Rule of thumb: never version what can be recreated or is not useful. A run output
or a per-task log is only useful for making the next decision, not for posterity.

- Versioned: this guidance, `TASKS.md`, requirements, architecture decisions,
  `docs/incidents.md`, and **decision reports** in `reports/`.
- A **decision report** is what a run, experiment or investigation leaves behind
  when it led to a decision: a short summary (one page or less) of the question,
  the sanitised evidence that decided it (counts, tables, small excerpts), the
  decision, and links to the PR. It is versioned together with that evidence
  (`lean/reports/TEMPLATE.md`). Write one only when a decision came out of the
  work; otherwise write nothing.
- Not versioned, delete after the decision: raw logs, full run outputs, generated
  conversion artifacts, per-task prompts, handbacks, review transcripts, status
  reports. Raw output stays in a local log directory outside the repository.

## Local setup (once per clone)

- `python lean/scripts/install_hooks.py` then `... --check`.
- Agents use a token or identity that can push feature branches and open PRs but
  not push `main` or merge (see `CUTOVER.md`, step on tokens). If the only
  credential available is the maintainer's, say so in the PR and stop at the
  PR; do not use it for merging.
- Python helpers run with the platform's native `python`.
