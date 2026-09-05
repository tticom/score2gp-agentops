# Container task checkpoints — implementation handoff

## Authority

- Authority: direct maintainer request to implement container improvements and
  require all authored work on GitHub-published task branches, including WIP.
- Product active task REC-04 remains unchanged. This does not promote L3-00.
- Profile: `../WORKFLOW_SKILLS_PROFILE.md`; persistence contract:
  `../TASK_CHECKPOINT_POLICY.md`.
- Skills revision: `439404f7342f4e324147efb6b0276f698fbf2bdb`.

## Repository state

- Repository: `tticom/score2gp-agentops`.
- Base: `1d428ee782a6465e8ff5eb916979848d470d1972`.
- Branch: `codex/container-task-checkpoints`.
- Tested implementation local and verified remote HEAD:
  `adb2431e03e1a05ede123158aacf64e279b2a943`.
- Worktree clean at that checkpoint. This record is a subsequent docs-only
  checkpoint; its containing commit is the handoff revision.
- No PR opened; no formal review, checks, or review threads exist for this branch.
- Previously local Lesson 3 plan was also published, on
  `codex/lesson3-native-working-slice-plan` at
  `c63c5aaa0006b0adfc19dd1abf1cc7f150936211`.

## Outcome and scope

- Added project-wide task publication policy, explicit task branches,
  independent role/task clones, remote checkpoint verification before launch
  and disposal, reviewer verify-only mode, retained failed sessions, and safer
  bootstrap fast-forward behavior. Updated launchers, image build contexts,
  entrypoint, offline validation, documentation, and regression tests.
- Changed paths: `agent-runtime/`, runtime tests, root agent instructions, and
  project control/profile/recording policy pointers; see branch diff.
- Frozen: product source, active-task authority, shared skills, existing
  production image tags, private fixtures, and Lesson 3 implementation.

## Evidence

- Author-executed, not an independent review:
  `SCORE2GP_DOCKER_TESTS=1 ../score2gp/.venv/bin/python -m pytest -q`:
  **186 passed**, including real Git recovery/rejection tests and two real
  container entrypoint stdin/exit-status tests.
- Both Dockerfiles built successfully under `:task-checkpoints` tags.
  Initial build-context exclusion and stdin regressions were observed and
  fixed before the passing run. Existing deployment tags were not replaced.
- `git diff --check` passed; GitHub branch readback matched the full tested SHA.
- Launcher tests use real Git with a local bare transport, but substitute
  Docker, gcloud, gh, and ACL commands. The two image smoke tests use real
  Docker with offline validation, not live client authentication.
- Intentionally unrun: live GCP-authenticated AGY/Codex author/reviewer
  sessions, cross-host rollout, real GitHub rejection during container exit,
  host-loss/signal recovery matrix, and independent adversarial review.

## Risks and next authorised action

- Continue runtime validation with live role credentials and explicit assigned
  test branches; exercise successful checkpoint and rejected publication,
  interruption/recovery, reviewer no-write behavior, and bootstrap ahead/dirty
  preservation. Do not label the rollout complete on mocked evidence.
- Review mode is policy plus exit verification, not a read-only filesystem or
  per-command Git authorization sandbox. Hard host loss can lose changes since
  the last checkpoint; no automatic blind staging is used. Local recovery
  volumes and image caches are not substitutes for GitHub publication.
- Once validated, open the bounded AgentOps PR for independent review. Stop
  before deployment/merge without the applicable gate and explicit integration
  authority. Do not self-review or alter the existing product task PR.
