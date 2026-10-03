# TASKS

The only task list. It replaces the authority state machine. Open work only:
when a task is done, delete its entry in the PR that finishes it. History is in
git and the merged PR, not here. The maintainer edits this file (or an agent
proposes an edit in a PR); an agent never invents a task.

Order is priority: take the first `todo` unless the maintainer names another.
At most one `doing` entry per agent. Claiming: the claim is the pushed branch
`task/<id>`, not an edit to this file (an edit on a branch is invisible to other
authors). Before starting, `git ls-remote --heads origin task/<id>`: if it exists,
the task is taken. Push an empty branch to claim, then work.
A task that cannot start until another is merged is `blocked` (say on what).

## Entry format

```
### <ID>: <one-sentence outcome>

- status: todo | doing | blocked
- risk: normal | risky
- serves: <requirement id, e.g. REQ-0003, or "none (tooling)">
- allowed paths: <globs the PR may touch; anything else is out of scope>
- done when: <observable acceptance, including the real-fixture expectation if risky>
- notes: <optional: constraints, known traps, links to the PR or issue>
```

`risky` means conversion logic, compiler, parsers, geometry or timing, any
fallback, private fixtures, CI/hooks/guidance files, or a disputed PR.

## Open tasks

### EXAMPLE-01: Replace this entry with a real task or delete it

- status: todo
- risk: normal
- serves: none (template)
- allowed paths: `docs/**`
- done when: the maintainer has seeded the list from the old authority backlog
- notes: seeding is a one-off, read-only extraction at cutover (see MIGRATION.md)
