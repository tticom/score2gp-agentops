# AGENTS.md (lean)

Codex and other agents read this file. The full guidance is in `CLAUDE.md` in the
same directory and applies identically. The short version:

- Agents never merge, never push to `main`, never use `--admin`.
- One task at a time from `TASKS.md`, on a `task/<id>` branch in your own
  worktree, ending in a draft PR.
- No private data in commits, PR text or logs. Counts and statuses only.
- A skipped test is not a pass. No silent fallbacks. Real source judges
  conversion claims.
- `risky` tasks need the local real-fixture check to PASS before handback and
  get an advisory independent review.
- If a rule blocks you, report it. Do not route around it.

Read `CLAUDE.md` before starting.
