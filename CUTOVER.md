# CUTOVER: from the live framework to the lean one

> **Status update (2026-10-01): superseded in part, to be reworked as `MIGRATION.md`.**
> The maintainer's decision is branch-from-`main`, chop, merge `slim-governance` in, prove,
> merge to `main`, in the SAME repositories. The fresh-history private repository in
> Phase B was a misreading: a fresh repository is only for the Rust component, a separate
> evidence-gated decision. Do not assume a drain either: the old framework keeps running.
> The current plan, conflict analysis and step mapping are in `MERGE-READINESS.md`
> (section 10 maps each step below). The reversibility labels, the scan step and the list
> of irreversible items still apply. Nothing here is to be actioned now.


Status: DRAFT checklist for the maintainer (tticom). **Nothing here has been
executed.** The old framework keeps running on `main` (CFW-04 is live under it).
Decisions this checklist rests on are recorded as decided in `SLIM-PROPOSAL.md`
section 6.

Branch role: `slim-governance` (in each repo) is the long-running trunk of the
lean experiment, standing in for `main` until you decide. The draft PRs (#752,
skills #7) are the review surface, not something to finish or merge now. The
snapshot below is taken from the tip of `slim-governance`, never from `main`,
because `main` still runs the old framework.

Conventions: **[R]** reversible, **[R*]** reversible with effort or in part,
**[I]** irreversible. Each step lists its undo. Do the steps in order; stop at any
step that does not behave as described.

What the cutover builds: a new **private repo with fresh history** holding a
current-state snapshot plus the lean framework. The old repos are kept, archived
and private. Nothing is deleted.

## What is carried over, and what is not

Carried over (the knowledge set, about 40 files instead of about 770):

- `lean/CLAUDE.md`, `lean/AGENTS.md`, `lean/TASKS.md`, `lean/PULL_REQUEST_TEMPLATE.md`,
  `lean/hooks/`, `lean/scripts/`, `lean/tests/` (promoted to the new repo root layout)
- `projects/score2gp/requirements/` (REQ-0001..0005), the two lasting architecture
  decisions (recognition architecture v1, tab timing policy A/B/C) as one `docs/decisions.md`,
  the five incident reports as `docs/incidents.md`, `REJECTED_CLAIMS.md` as
  `docs/rejected-claims.md`, one `docs/CONTEXT.md`, and a `reports/` folder of
  **decision reports**: for each past run, audit or investigation that led to a
  decision that still matters, a short summary with its evidence (counts and
  tables, no raw logs), in `lean/reports/TEMPLATE.md` form. The maintainer picks
  which old research and report files are worth condensing; default is none, so
  nothing is carried by accident
- the six lean skills (`lean/skills/` in the skills repo)

Not carried over (rule: never version what can be recreated or is not useful):

- `ORCHESTRATION_STATE.json`, `ACTIVE_TASK.md`, the generated views, the promotion
  and reconciliation machinery
- the 600+ per-task files as such: prompts, decisions, runs, reviews, research,
  reports, handoffs, templates. Where one of them led to a decision that still
  matters, a condensed decision report (with its evidence) replaces it; the
  original is not copied
- scripts S1 to S4, S6, S8, S11 and their tests, role prompts, role skills, agent JSON
- anything under `work/`, run outputs, private fixtures (they stay in the private
  fixtures repo and local workspace)

All of it remains in the archived-private old repos if it is ever needed.

## Phase A: prepare (all reversible, old framework untouched)

1. **[R] Drain.** Let CFW-04 and every PR on the old authority finish and be merged
   by you. Confirm no open task PRs and no pending governance PRs. Do not start a
   new task on the old framework. Undo: none needed.
2. **[R] Freeze marker.** Tag the final state of each old repo (`pre-lean-freeze`)
   on `main`: product `score2gp`, `score2gp-agentops`, `agentops-claude-skills`.
   Record the three SHAs. Undo: delete the tags.
3. **[R] Seed the task list.** Read (do not modify) the authority backlog in
   `ORCHESTRATION_STATE.json` at the freeze tag and write open items into
   `TASKS.md` by hand or with a one-off script run on a copy. Keep only tasks you
   still want; mark each `normal` or `risky`. Undo: discard the file.
4. **[R] Build the snapshot tree** in a scratch directory outside every repo
   (layout: `CLAUDE.md`, `AGENTS.md`, `TASKS.md` at the root, the PR template at
   `.github/`, everything else of `lean/` stays under `lean/` so the paths the
   guidance names are valid; `lean/tests` verifies the guidance paths exist):
   `git archive` of the freeze tag (old knowledge files) and of the
   `slim-governance` tip (lean files) for the files listed above only, plus the lean
   files promoted to their final paths. Do not copy `.git`.
5. **[R] Scan the snapshot before anything is pushed anywhere**: no `.pdf`, `.gp`,
   `.gpx`, `.mxl`, `.png` or other binary; no file over 1 MB; no absolute local
   paths (`<drive>:\Users\<name>\...`); no emails you do not want; no tokens
   (`gh_`, `ghp_`, `github_pat_`, `sk-`, `-----BEGIN`); no fixture names from the
   private fixtures manifest. Fix the snapshot, not the scan. Undo: none needed.
6. **[R] Run the lean tests on the snapshot**: `python -m pytest lean/tests` (or
   its promoted path), and the skills' tests. All must pass.

Decision point: stop here until you are satisfied with the snapshot contents.

## Phase B: build the new home (reversible while old repos are untouched)

7. **[R] Create the new private repo(s), empty.** Suggested: `score2gp-ops` for
   the agentops successor (with the six skills under `skills/`, which removes the
   separate skills repo), fresh history. Decide separately whether the product
   `score2gp` also gets a fresh-history private repo (recommended; see decisions
   below). Undo: delete the new repo (it is new, nothing else points at it).
8. **[R] Initial commit** in the new repo: `git init`, copy the snapshot in, one
   commit: "Snapshot of score2gp-agentops@<sha> (lean framework)", push `main`.
   Note: GitHub on a free plan does not enforce branch protection on private repos
   (decided), so no ruleset is created. Undo: delete the repo.
9. **[R] Hooks.** In every clone and worktree that will push to the new repo, run
   `python scripts/install_hooks.py` and confirm with `--check`. Test it: from a
   task branch, `git push origin HEAD:main` must be refused locally. Undo:
   `install_hooks.py --uninstall`.
10. **[R] Agent credential (the stronger control).** Preferred: one agent GitHub
    account (reuse `tticom-automation`) added as a *read* collaborator on the new
    private repo, working from its own private fork, pushing task branches to the
    fork and opening PRs into the repo. That identity then has no push right to
    `main` at all, which is real server-side enforcement for agents even on a free
    plan. Fallback: a fine-grained token for the new repo scoped to contents
    write and pull requests write, accepting that it *can* push `main`, so the
    hook is the only barrier. Never give agents the maintainer credential. State the
    chosen option in `CLAUDE.md`. Undo: remove the collaborator, revoke the token.
    To confirm before relying on it: GitHub allows private forks and
    read-collaborators on free private repositories (check the plan page).
11. **[R] CI, before any trial.** Copy `lean/ci-slim.yml` to
    `.github/workflows/ci.yml` in the new repo (forbidden-file, size, token and
    local-path scan via `lean/scripts/repo_scan.py`, tests with a skip report,
    `git diff --check`). On the free plan nothing makes it a required check, so
    the maintainer looks at it before merging; that is the agreed convention.
    Private-repo Actions minutes on the free plan are limited. Undo: delete the
    workflow.
12. **[R*] Trial.** Run one `normal` and one `risky` task end to end in the new
    repo (PR, local real-fixture check, optional review, you merge). Compare with
    the old flow. Undo: abandon the new repo and discard the trial merges; the old
    framework is still intact, but the trial changes themselves are not carried back.

Decision point: go or no-go on switching the old framework off.

## Phase C: switch off the old framework

13. **[R*] Switch the dispatcher off.** On this machine, outside the repos: stop any
    scheduled or running `go`/`got` automation and the launchers
    (`launchers/codex_author.sh`, `review_with_fallback.sh`, `claude_reviews.sh`,
    `as_identity.sh`); move them to `launchers/_retired/` rather than deleting;
    remove the `go`/`got` command aliases. Do this only when no old-framework PR is
    open. Undo: move the launchers back (works as long as the old repos can be
    cloned or unarchived).
14. **[R*] Retire the three role accounts** (`tticom-automation` kept as the agent
    identity if you chose option 10, otherwise retired too; `tticom-codex`,
    `tticomgov-code`): remove them as collaborators from the old repos, revoke
    their personal access tokens and OAuth grants, `gh auth logout` for their
    stored credentials in `gh-config`, and remove their credential stores. Do not
    delete the GitHub accounts (they keep authorship of history, and reviewer use
    stays possible). Undo: re-add the collaborator and mint a new token. Revoked
    tokens cannot be un-revoked.
15. **[R] Archive the old repos** (GitHub repo settings, Archive): `score2gp`,
    `score2gp-agentops`, `agentops-claude-skills`. Archived repos are read-only and
    can be unarchived. Leave the draft slim PRs (#752, skills #7) open or close them as you
    prefer; the `slim-governance` branches are not deleted either way.
    Undo: unarchive.

## Phase D: make private (the point of no return for public exposure)

Before step 17, finish these checks, because making a repo private does not unpublish what
was already public:

16. **[I] History audit and credential rotation.** Public history has been
    visible since each repo was created. Scan old history for private fixture
    content and secrets (`git log --all -p` against the patterns in step 5, and the
    private-fixtures manifest). Rotate any credential that ever appeared in logs
    (the history contains credential-redaction fixes, so assume at least some
    appeared). Check upstream licence obligations: `PROVENANCE.md` and the
    `NOTICE.md` files for `code-review` and `verified-implementation` (MIT notices
    must stay with the derived material in the new repo). Undo: not applicable
    (rotation is irreversible but wanted).
17. **[I] Make the old repos private.** Archive first (step 15), then change
    visibility. Consequences to accept: existing public forks and clones, the
    Wayback Machine, search caches and anyone who already copied the content keep
    their copies; stars and watchers are lost; public links and any GitHub Pages
    break; existing forks of a public repo are detached from it. Making a repo
    public again is possible but recovers none of the above. Undo: visibility can
    be flipped back, nothing else is recovered.
18. **[R] Final checks.** Open the new repo logged in as the agent identity and
    verify it cannot merge and (option 10) cannot push `main`. Verify the old
    repos are archived and private. Update your workspace notes and launchers
    documentation to point at the new repo.

## What is irreversible

- **Making the old repos private** (step 17): copies already taken stay; stars,
  watchers, Pages and detaching of forks cannot be restored.
- **Revoking tokens and logging identities out** (step 14) and **rotating
  credentials** (step 16): old values cannot be restored. Intended.
- **Anything that was public stays exposed** until step 17 and in any third-party
  copy afterwards.
- Everything else is reversible: tags, the new repo (delete it), hooks, archive
  state (unarchive), collaborators, launchers (moved, not deleted). No history is
  rewritten, nothing is deleted, no account is deleted.

## Rollback by point

- Before step 13: close the new repo; the old framework is still live and unchanged.
- After 13 and before 15: move the launchers back, re-add collaborators and tokens.
- After 15: unarchive and restore as above.
- After 17: you can restore visibility and the old workflow, but not the privacy of
  what was public.

## Decisions still needed from the maintainer

See the report that accompanied this branch and `SLIM-PROPOSAL.md` section 7:
product repo history policy, agent credential option (10), where the six skills
live, and which research files to carry.
