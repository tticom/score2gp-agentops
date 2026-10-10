# Score2GP orchestrator runbook (for Claude or Codex)

Purpose: any capable agent (Claude, or Codex when Claude is out of usage) can take over orchestration of the governed
Score2GP lifecycle from this file alone. Written 2026-10-10 from the working session notes. Keep it current: whoever
orchestrates updates "State and next steps" at the end of each work session.

## 0. Ground rules (never break)

1. **Authority:** `projects/score2gp/ORCHESTRATION_STATE.json` in `tticom/score2gp-agentops` (`main`) is the only task
   authority. Read it live (`git show origin/main:projects/score2gp/ORCHESTRATION_STATE.json`); never trust a stale note.
2. **Crossed review:** no login reviews or merges a PR it authored. Every PR needs a formal APPROVE or CHANGES_REQUESTED
   from a non-author at the exact head, with changes spelled out. Reviewers reply to and resolve their own threads.
3. **Merging:** only through the merge executor
   `python scripts/score2gp_orca_control.py merge --repository <owner/repo> --pull-request <n> --github-login <login>`
   run via `launchers/as_identity.sh <codex|gov> ...`. `tticom-automation` never merges. The author never merges its own PR
   (Codex-authored product PRs are merged as `tticomgov-code`; governance PRs by gov are merged as `tticom-codex`).
4. **Scope:** an author edits only `allowed_paths`. A scope amendment is a governance PR and **needs the maintainer's
   explicit approval in that conversation**; never invent that approval.
5. **Evidence:** AGENT_CONTROL.md domain-evidence rule: acceptance rests on real approved sources (private corpus) or
   provenance-linked extracts; synthetic/mocked/generated tests carry zero acceptance weight for recognition, grouping,
   geometry, timing or fidelity claims (they may supplement non-domain infrastructure with a stated rationale).
6. **Honesty:** report failing tests and skipped steps with the output; never claim a verdict, approval or merge that did
   not happen. Never fabricate maintainer input.
7. **Scratch:** only inside the workspace (`worktrees/<role>/.tmp`, `launchers/`); never create folders at the root of `C:\`.
   Remove scratch you no longer need. Do not delete anything outside the files you created without the maintainer.
8. **The vector-parser is a separate experiment** (`tticom/score2gp-vector-parser`, own process, `docs/MAINTAINER-DIRECTIVES.md`
   there). The governed Score2GP project continues as if it did not exist; its authors and prompts are not told about it.
   Keep the seam in mind (the pure kernels `_inside_fill`, `_fill_ratio`, `_runs`, the `get_text` calls, the scene).

## 1. Identities and places

| Role | Login | Workspace | gh config |
|---|---|---|---|
| governance, reviews, merges | `tticomgov-code` | `worktrees/gov/` | `gh-config/gov` |
| Codex author/reviewer/merger | `tticom-codex` | `worktrees/codex/` | `gh-config/codex` |
| automation author | `tticom-automation` | `worktrees/auto/` | `gh-config/auto` |
| maintainer | `tticom` | (vector-parser: `worktrees/tticom/`) | n/a |

Workspace root `C:\Users\niall\src\score2gp-workspace` (Git Bash path `/c/Users/niall/src/score2gp-workspace`). Launchers
are in `launchers/` (call by ABSOLUTE `/c/...` path; use `cygpath -w` for Windows Python). Pipeline uses Git Bash, never WSL.

## 2. The lifecycle loop (one transition at a time)

1. **Read state:** authority revision, `task` (id, status, pull_request), `next_task_proposal`, `queued_task_proposals`,
   open PRs on `tticom/score2gp` and `tticom/score2gp-agentops` (`gh pr list`).
2. **Task PROMOTED, no PR:** author it: `launchers/codex_author.sh tticom/score2gp <task.branch> <tag> <prompt-path>`
   (background; Codex gpt-6.1-sol medium; **on a Codex limit it continues on Claude under the same identity**). It
   dispatches, creates the worktree `worktrees/codex/author-<tag>`, commits, pushes, opens the PR and publishes the handback.
3. **Handback failed** (`validation run N did not complete successfully`): never make it pass by hiding a failure.
   The handback publisher needs every validation run to exit 0 and every acceptance entry PASS, and that must be true:
   (a) rerun the full suite at the exact head on a supported runtime (exact-head CI on Linux with the private corpus
   mounted is the authoritative full run; cite its run id, head, passed/skipped/xfailed counts); (b) the 15 known
   Windows-only local failures (section 4) are **kept visible**: list each id in `remaining_risks`, record the local run as
   `deselected=15` (never as a pass of those tests), and show they fail identically at the base commit; (c) set an
   acceptance entry to PASS only where independent evidence at this head supports it (the CI run or a focused real-source
   run that includes the checks). Patch `handback-evidence.json`/`handback.json` in `launchers/codex-author-logs/<tag>/`
   only to add that evidence; publish as codex with `publish-pr-handback/scripts/publish_handback.py --repo ... --pr N
   --expected-head <sha> --worktree worktrees/codex/author-<tag> --packet <json> --state AWAITING_GOVERNANCE_REVIEW
   --allowed-state AWAITING_GOVERNANCE_REVIEW` (`review_findings` items need `finding`, `disposition`, `evidence`). A new
   failure that is not in the known list is a hard stop (AGENT-RULES.md): fix it or report it; do not deselect it.
4. **Bind the PR:** the dispatcher says "governance must record pull_request N": governance PR setting `task.pull_request`,
   `authority_revision` +1, `ACTIVE_TASK.md` regenerated with `render_active_task` (precedent #772, #775).
5. **Review (non-author):** product PR authored by codex: `launchers/gov_claude_review.sh "tticom/score2gp|<n>|<note>"`
   (reviewer `tticomgov-code`; add a note with the adversarial checklist). Governance PR authored by gov:
   `launchers/review_with_fallback.sh "tticom/score2gp-agentops|<n>|<note>"` (Codex; Claude engine fallback; if the
   Codex sandbox fails on git shared memory use `launchers/claude_reviews.sh`, which runs as tticom-codex). The pinned
   publisher needs `AGENTOPS_ROLE_POLICY` (the launchers export `launchers/role-policy.json`).
6. **CHANGES_REQUESTED:** fix on the same branch (governance: edit, test, push, republish exact-head handback with
   `review_findings`, reply on threads as the author, update the PR body, rerun the review). Out-of-scope edits: stop and
   ask the maintainer about a scope amendment.
7. **Merge** per rule 3 when APPROVED at the exact head and CI is green; verify `merge_commit` in the output.
8. **Reconcile and promote:** `python scripts/score2gp_orca_control.py snapshot --repository tticom/score2gp
   --pull-request N > live.json`, then `reconcile_task(authority, live, task_id=ID)` (records COMPLETED from live data),
   promote the proposal unchanged (`status: PROMOTED`), advance `next_task_proposal` from `queued_task_proposals`, revision +1,
   regenerate ACTIVE_TASK.md; open it with `launchers/gov_open_pr.sh` (templates use `@@HEAD@@ @@BASE@@ @@PR@@`; see
   `launchers/gov-review-logs/trecon-*`); review; merge. Start the next author run.
9. **Governance PR tests:** `worktrees/gov/score2gp-agentops/.venv/Scripts/python.exe -m pytest -q --capture=sys
   -p no:cacheprovider` (560 passed, 1 skipped) and `PYTHONUTF8=1 python scripts/score2gp_governance_audit.py` (PASS).
   Branches must start with `governance/`.
10. **Idle:** select work that the authority marks READY and propose it for the maintainer's approval before it is added.

## 3. Models and usage

Claude Pro (weekly limit) and ChatGPT Plus. Defaults pinned in the launchers via env: Codex `gpt-6.1-sol` medium (authoring,
reviews), `gpt-6-luna` low (mechanical), Claude `sonnet` medium; override with `CODEX_MODEL`, `CODEX_EFFORT`,
`CLAUDE_MODEL`, `CLAUDE_EFFORT`. Spread work across both. The main Claude cost is very long sessions: keep sessions short
and write state to this file. When Claude is out, Codex orchestrates from this runbook (section 6).

## 4. Gotchas (all hit before)

- Write long texts with a file tool, not shell heredocs with nested quotes; never read a file in the same expression that
  opens it for writing; `git checkout -- .` before committing discards your edits.
- `gpif.build_gpif` writes a legacy layout if "pytest" is in any argv/path: private tests convert under `<repo>/work`.
- Local pytest on Windows: use `--capture=sys`; known 15 baseline failures (`test_omr_contract` x13,
  `test_raster_diagnostics_gate_report::test_subprocess_test_manifest_rejects_absolute_without_leaking`,
  `test_system_integration_diagnostics::test_cli_diagnose_command`).
- Background shells are reaped at low memory; check free memory before heavy work. Waiters: use an until-loop on a log
  line, not long sleeps; test the pattern against the existing log.
- Codex sandbox (workspace-write) cannot write `.git`; the launchers do every git/GitHub step outside it. Codex
  full-suite runs can fail with git shared-memory permission errors: use the exact-head CI or the Claude-engine runner.
- The merge gate denies the PR author as merger (`merge_controller_is_pr_author`); the executor denies skills-repo PRs
  (those are the maintainer's merge).
- Fixture layout is categorised (`with-score`, `no-score`, `ascii`, `hand-written`, `Books`); launchers flatten it into
  `fixtures/private/`. Never commit corpus content.

## 5. Maintainer-only decisions

Scope amendments, promoting work the maintainer has not approved, skills-repo merges, destructive cleanup outside files
you created, vector-parser checkpoints (E0..E5), changing roles/gates/identities.

## 6. If Claude is out of usage: Codex as orchestrator

Start: `launchers/orchestrator_codex.sh` (see the script header). It runs `codex exec` from the workspace root with this
file and the live authority as input and the instruction "advance the lifecycle one transition at a time and write the
state log". Constraints Codex must respect: (a) the default sandbox cannot write `.git`, so every git step goes through
the launchers (`gov_open_pr.sh`, `codex_author.sh`, `as_identity.sh`), which run outside it; run Codex with the
`--sandbox`/approval setting the maintainer has chosen (default workspace-write; a run with full access is the
maintainer's explicit choice); (b) Codex may merge only as `tticom-codex`/`tticomgov-code` per rule 3; (c) at the end it
updates section 7 and the vector-parser `docs/TASKS.md` if relevant.
Claude resumes by reading section 7 and `launchers/orchestrator.log`.

## 7. State and next steps (update each session)

Updated 2026-10-10: authority revision 120. TS-READ-01 (product #484, `30a4828`) and FIXTURE-GUARD-01 (product #485,
`dfe05d0`) are COMPLETED. Active task PDF-GROUP-03 (promoted, prompt `projects/score2gp/prompts/next/pdf-group-03-song-bar-boxes.md`,
branch `feat/pdf-group-03-song-bar-boxes`); next proposal UNREAD-01, with PERF-01 held in `queued_task_proposals`. Next action: author PDF-GROUP-03 with
`launchers/codex_author.sh tticom/score2gp feat/pdf-group-03-song-bar-boxes pdf-group-03 <prompt path>`, then steps 3-8 of
section 2. Candidate follow-ups: the key reader counts time-signature digits as accidentals on Combining_Maj_minor_pent_-_A;
Codex review sandbox failures on git shared memory (use the Claude-engine reviewer). Vector-parser: continue at E1-05 per its
`docs/TASKS.md`; maintainer directives are recorded in its `docs/MAINTAINER-DIRECTIVES.md`.
