# Model 1 Operating Decision

## Decision

The human maintainer selected Model 1 after the second unauthorized merge
attempt: Agy may retain GitHub write access for task branches and pull requests.
GitHub `Main_Protect` is the technical containment for `main` updates and
merges.

## Invariants

- Agy must never invoke a pull-request merge command, merge API, `--admin`,
  bypass flag, direct `main` push, force push, or destructive cleanup command.
- Agy may open and update task PRs only, and must leave accepted PRs for an
  externally authenticated human maintainer to merge.
- Any further prohibited-command attempt stops unattended execution for the
  current cycle. The active task becomes `BLOCKED`; no agent selects the next
  operating response.

## Current Consequence

FS-02 is complete because its independently reviewed evidence is now on
`main`. FS-03A is authorised as an Architect task to define the supported
timing-source route. It is research and governance only; it does not authorise
product implementation or the planned refactor.
