# ORC-04 cross-repository branch fix handoff

## Authority

- Active task: ORC-04 — Integrated PR Lifecycle and Concurrent Review Routing
- Authority source: `projects/score2gp/ORCHESTRATION_STATE.json`, revision 28
- Project profile: `projects/score2gp/WORKFLOW_SKILLS_PROFILE.md`
- Skills revision: `agy-skills` `7d48729b1a2c84ab19681215c02e1a52ef1a8fae`

## Repository state

- Repository: `tticom/score2gp-agentops`
- Base revision: `d02f7c9d0384dd714682ff492feb1acb883528d5`
- Branch: `fix/orc-04-cross-repo-base`
- Local HEAD: `aa07000f332e87a979717d65cdc90463080fc422`
- Remote HEAD: `aa07000f332e87a979717d65cdc90463080fc422`
- Worktree: clean at handoff capture
- PR: https://github.com/tticom/score2gp-agentops/pull/660

## Outcome and scope

- Outcome: Fixed missing task-branch creation to resolve the base SHA from the target task repository's `main` ref rather than the separate product checkout.
- Changed paths: `agent-runtime/assignment_adapter.py`, `tests/test_assignment_adapter.py`, this handoff
- Frozen or excluded scope: No product repository changes, branch creation retry, merge, or dispatch changes.

## Evidence

- Independently verified: Cross-repository regression test was red before the fix and green after; 112 ORC-04 tests passed; compileall passed; `git diff --check` passed; PR head matches local HEAD.
- Author-reported: Original WSL invocation failed with `gh: Object does not exist (HTTP 422)` during task branch creation.
- Intentionally unrun: A live branch-creation retry, because that would be a remote mutation before independent review and merge.

## Risks and comments

- Unresolved risks: PR #660 has no formal review yet; CI was queued at handoff capture.
- Review threads: None observed at handoff capture.

## Next authorised action

- Action: Independently review PR #660 at exact head `aa07000f332e87a979717d65cdc90463080fc422`; after maintainer merge, rerun the WSL Automation startup/dispatch flow.
- Stop condition: Do not retry remote branch creation before PR #660 is reviewed and merged; stop on any exact-head, identity, authority, or scope mismatch.
