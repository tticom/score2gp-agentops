# MIGRATION: from the live framework to the lean one (same repositories)

Status: DRAFT checklist for the maintainer (tticom). **Nothing here has been executed.**
It replaces `CUTOVER.md` (renamed; the fresh-history private repository option is
removed: a fresh repository is only for the Rust component, a separate evidence-gated
decision). The old framework keeps running on `main` in parallel; there is no drain.
The proof so far is `TRIAL-REPORT.md`; the conflict analysis, chop order and gates are in
`MERGE-READINESS.md` (section numbers below refer to it).

Method: branch `lean-cutover` from `main`, chop the retired files, merge `slim-governance`,
prove, then merge to `main`. Branch name must not start with `governance/` or `architect/`.

Conventions: **[R]** reversible, **[R*]** reversible with effort or in part, **[I]**
irreversible. Do the steps in order; stop at any step that does not behave as described.
Run tests with `pytest -s` and a real file on standard input on this machine.

## What is carried over, and what is not

Carried over (about 40 files instead of about 770): `lean/` (guidance, `TASKS.md`, PR
template, hooks, scripts, tests, reports template, **including the hidden
`lean/.gitattributes`**: a plain `cp` of the folder contents misses it, and without it a
Windows checkout turns the hook's line endings to CRLF); the requirements, the two
lasting architecture decisions, the five incident reports, `REJECTED_CLAIMS.md`,
`REVIEW_RULES.md` and the four conversion-hack bans (MERGE-READINESS G1, G2); the six
lean skills (skills repo, `lean/skills/`). Not carried over: the authority state machine,
the promotion and reconciliation machinery, the 600+ per-task files, role prompts and
skills, `work/` outputs, private fixtures. Where a past run led to a decision that still
matters, a condensed decision report replaces it; default is none.

## Phase A: prepare (all reversible, old framework untouched)

1. **[R] Freeze marker.** Tag `pre-lean-merge` on `origin/main` in each of the three
   repositories; record the SHAs; save a copy of `ORCHESTRATION_STATE.json` outside the
   repos (seed source for step 2). Undo: delete the tags.
2. **[R] Seed `TASKS.md`** (MERGE-READINESS appendix A): default CFW-04, SCALE-01, CP-06; mark
   each `normal` or `risky`; give each allowed paths and a done-when. Undo: discard.
3. **[R] Chop on `lean-cutover`** in the order of section 7 (C1 to C7), each step gated on
   a green suite; swap CI in the same commit as the authority removal; never an empty suite.
   Apply the section 9 promotion-time fixes (S3 to S5) in C7. Undo: delete the branch.
4. **[R] Scan** the chopped tree: `python lean/scripts/repo_scan.py` (0 findings), also
   with `--names-file` for the private-fixture names kept outside the repo, run locally
   (CI cannot see that file). Close MERGE-READINESS G5 and G6 first. Fix the tree, not the
   scan. Undo: none needed.
5. **[R] Run the lean tests** and the skills tests on the chopped tree; record counts and
   skips (a skip is not evaluated).
6. **[R] Hooks.** `python lean/scripts/install_hooks.py` then `--check` in every clone and
   worktree that pushes. Proved in the trial: a push to `main` is refused. Undo:
   `install_hooks.py --uninstall`.
7. **[R*] Trial in a scratch repository** (acceptance item 4 of section 7): one `normal`
   and one `risky` task end to end. The `risky` half has been run once locally (see
   `TRIAL-REPORT.md`); the remaining part is a real GitHub scratch repository with Actions
   and a draft PR. Undo: delete the scratch repository.

Decision point: go or no-go on the merge. The maintainer must not be needed for anything
earlier than this point.

## Phase B: merge, keeping the old flow running

8. **[R*] Keep `lean-cutover` current** with `main` (section 8.1, delete wins, resurrection
   guard) until the quiet moment of section 8.2; handle in-flight work as in 8.3.
9. **[R*] Merge to `main`** after the acceptance list of section 7 (suite green on Windows
   and Linux 3.12, scan, fixture check PASS or a named NOT_EVALUATED, protections gate G1 to
   G3 and G5 to G7, rollback rehearsed). The product `CLAUDE.md`, `AGENTS.md`,
   `docs/agentops.md` and `HANDOFF.md` change in a product PR that lands with the cut.
   Undo: `git revert -m 1 <merge>` on a branch and PR it (section 7, Rollback).

## Phase C: switch off the old framework (after the merge, separate decisions)

10. **[R*] Agent credential (the stronger control).** Preferred: one agent account working
    from a private fork with read access to the repository, so it cannot push `main` or
    merge. Fallback: a write token plus the hook only. Note: by the standing instruction of
    2026-10-03 agents may merge product PRs as `tticom` after independent review and green
    CI; in that case record the rule in `CLAUDE.md` rule 1 and keep an audit of such merges
    (G7). Undo: remove the collaborator, revoke the token.
11. **[R*] Switch the dispatcher off.** Outside the repos, stop `go`/`got` automation and the
    launchers; move them to `launchers/_retired/` rather than deleting; remove the aliases.
    Only when no old-framework PR is open. Undo: move them back.
12. **[R*] Retire the role accounts** (keep one agent identity per step 10): remove as
    collaborators, revoke tokens, log out stored credentials. Do not delete the accounts.
    Revoked tokens cannot be un-revoked.
13. **[R] Final checks.** As the agent identity, verify what it can and cannot do; update
    the workspace notes and launcher documentation.

## Separate, later, irreversible decisions (not part of this merge)

- **[I] Making any repository private** (history audit and credential rotation first:
  public history has been visible since creation; scan it for private fixture content and
  secrets; check `PROVENANCE.md` and the `NOTICE.md` files for the MIT-derived skills).
  Copies already taken, caches, stars, watchers and fork links cannot be restored.
- **[I] Revoking tokens or rotating credentials** (step 12): old values cannot be restored.
- **[I] Anything that was public stays exposed** until made private, and in any copy after.
- A fresh-history private repository for the Rust component only, with its own evidence gate.

Everything else is reversible: tags, the `lean-cutover` branch, hooks, collaborators,
launchers (moved, not deleted). No history is rewritten, nothing is deleted, no account is
deleted.

## Rollback by point

- Before step 9: delete `lean-cutover`; `main` never changed.
- After step 9: revert the merge as above; the `pre-lean-merge` tag marks the old state.
- After step 11: move the launchers back, re-add collaborators and tokens.
- Irreversible items cannot be rolled back.
